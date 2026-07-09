#!/usr/bin/env python3
"""
validate_messages.py
Validates all message .yml files in /content/messages/ against message.schema.yml.
Also performs additional checks not covered by JSON Schema, such as:
  - spirit_id matches a file in /spirits/
  - medium matches a file in /mediums/ (or is "Anonymous")
  - related_messages IDs reference existing message files
  - last_edited is a valid date
  - title is wrapped in quotes (cannot be checked by schema, flagged as warning only)
  - primary_subjects and secondary_subjects match names defined in
    metadata/subjects.yml (the single source of truth for the vocabulary)
  - subjects.yml itself contains no duplicate names

After validation, prints a SUBJECT USAGE CENSUS: every subject in
subjects.yml with the number of messages using it, so unpopulated
subjects and drift trends are visible on every push.

Run locally:  python .github/scripts/validate_messages.py
Run in CI:    automatically triggered by GitHub Actions on push/pull_request
"""

import sys
import yaml
import jsonschema
import datetime
from collections import Counter
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schema" / "message.schema.yml"
MESSAGES_DIR = ROOT / "content" / "messages"
SPIRITS_DIR = ROOT / "spirits"
MEDIUMS_DIR = ROOT / "mediums"
SUBJECTS_PATH = ROOT / "metadata" / "subjects.yml"          # NEW

# ── Colours for terminal output ───────────────────────────────────────────────
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"


def convert_dates(data):
    """Recursively convert date objects to ISO string format for JSON Schema validation."""
    if isinstance(data, dict):
        return {k: convert_dates(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_dates(v) for v in data]
    elif isinstance(data, (datetime.date, datetime.datetime)):
        return data.isoformat()
    return data


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        # Strip YAML front matter delimiter if present
        content = f.read()
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[1]
        data = yaml.safe_load(content)
        return convert_dates(data)


def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f.read())


def get_spirit_ids():
    return {p.stem for p in SPIRITS_DIR.glob("*.yml")}


def get_medium_ids():
    return {p.stem for p in MEDIUMS_DIR.glob("*.yml")}


def get_all_message_ids():
    ids = set()
    for path in MESSAGES_DIR.rglob("*.md"):
        data = load_yaml(path)
        if data and "message_id" in data:
            ids.add(data["message_id"])
    return ids


# ── NEW: subject vocabulary ───────────────────────────────────────────────────
def get_valid_subjects():
    """
    Read metadata/subjects.yml (the single source of truth) and return
    (ordered_names, duplicate_names). Names include every top-level
    category and every subcategory, in file order.
    """
    with open(SUBJECTS_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f.read())
    names = []
    for cat in data.get("main_categories", []):
        names.append(cat["name"])
        for sub in cat.get("subcategories", []) or []:
            names.append(sub["name"])
    duplicates = sorted({n for n, c in Counter(names).items() if c > 1})
    return names, duplicates


def extract_subjects(data):
    """Return the list of subject values used by one message's front matter."""
    used = []
    primary = data.get("primary_subjects")
    if isinstance(primary, str) and primary.strip():
        used.append(primary.strip())
    secondary = data.get("secondary_subjects") or []
    if isinstance(secondary, list):
        used.extend(s.strip() for s in secondary if isinstance(s, str) and s.strip())
    return used


def build_subject_census(subject_names):
    """Count how many messages use each subject (primary or secondary)."""
    census = Counter({name: 0 for name in subject_names})
    for path in MESSAGES_DIR.rglob("*.md"):
        data = load_yaml(path)
        if not data:
            continue
        # Count each subject once per message even if repeated in the file
        for s in set(extract_subjects(data)):
            if s in census:
                census[s] += 1
    return census
# ──────────────────────────────────────────────────────────────────────────────


def validate_file(path, schema, spirit_ids, medium_ids, all_message_ids, valid_subjects):
    errors = []
    warnings = []

    try:
        data = load_yaml(path)
    except yaml.YAMLError as e:
        errors.append(f"YAML parse error: {e}")
        return errors, warnings

    if not data:
        errors.append("File is empty or could not be parsed.")
        return errors, warnings

    # ── JSON Schema validation ────────────────────────────────────────────────
    validator = jsonschema.Draft7Validator(schema)
    for error in sorted(validator.iter_errors(data), key=str):
        errors.append(f"Schema: {error.message} (at {' > '.join(str(p) for p in error.path)})")

    # ── spirit_id cross-reference ─────────────────────────────────────────────
    spirit_id = data.get("spirit_id")
    if spirit_id and spirit_id not in spirit_ids:
        errors.append(f"spirit_id '{spirit_id}' has no matching file in /spirits/{spirit_id}.yml")

    # ── spirits array cross-reference ────────────────────────────────────────
    for sid in data.get("spirits", []):
        if sid not in spirit_ids:
            errors.append(f"spirits entry '{sid}' has no matching file in /spirits/{sid}.yml")

    # ── medium cross-reference ────────────────────────────────────────────────
    medium = data.get("medium", "")
    if medium and medium != "Anonymous":
        medium_id = medium.lower().replace(" ", "-")
        if medium_id not in medium_ids:
            warnings.append(f"medium '{medium}' has no matching file in /mediums/{medium_id}.yml")

    # ── related_messages cross-reference ─────────────────────────────────────
    for related_id in data.get("related_messages", []):
        if related_id not in all_message_ids:
            errors.append(f"related_messages entry '{related_id}' does not match any known message_id")

    # ── message_id matches filename ───────────────────────────────────────────
    message_id = data.get("message_id", "")
    expected_stem = path.stem
    if message_id and message_id != expected_stem:
        errors.append(f"message_id '{message_id}' does not match filename '{expected_stem}.yml'")

    # ── ID is lowercase ───────────────────────────────────────────────────────
    if message_id and message_id != message_id.lower():
        errors.append(f"message_id '{message_id}' must be fully lowercase")

    # ── NEW: subject vocabulary cross-reference ──────────────────────────────
    for s in extract_subjects(data):
        if s not in valid_subjects:
            errors.append(f"subject '{s}' is not defined in metadata/subjects.yml")

    return errors, warnings


def main():
    print(f"\nLoading schema from {SCHEMA_PATH.relative_to(ROOT)}...")
    try:
        schema = load_schema()
    except Exception as e:
        print(f"{RED}Could not load schema: {e}{RESET}")
        sys.exit(1)

    # ── NEW: load subject vocabulary ─────────────────────────────────────────
    print(f"Loading subject vocabulary from {SUBJECTS_PATH.relative_to(ROOT)}...")
    try:
        subject_names, duplicate_subjects = get_valid_subjects()
    except Exception as e:
        print(f"{RED}Could not load subjects.yml: {e}{RESET}")
        sys.exit(1)
    valid_subjects = set(subject_names)

    spirit_ids = get_spirit_ids()
    medium_ids = get_medium_ids()

    print("Building message ID index...")
    all_message_ids = get_all_message_ids()

    message_files = sorted(MESSAGES_DIR.rglob("*.md"))
    if not message_files:
        print(f"{YELLOW}No message files found in {MESSAGES_DIR.relative_to(ROOT)}{RESET}")
        sys.exit(0)

    print(f"Validating {len(message_files)} message file(s)...\n")

    total_errors = 0
    total_warnings = 0
    files_with_issues = 0

    # ── NEW: duplicate names inside subjects.yml are themselves an error ─────
    if duplicate_subjects:
        print(f"  metadata/subjects.yml")
        for d in duplicate_subjects:
            print(f"    {RED}ERROR{RESET}   subject name '{d}' is defined more than once")
            total_errors += 1
        print()

    for path in message_files:
        rel = path.relative_to(ROOT)
        errors, warnings = validate_file(path, schema, spirit_ids, medium_ids, all_message_ids, valid_subjects)

        if errors or warnings:
            files_with_issues += 1
            print(f"  {rel}")
            for e in errors:
                print(f"    {RED}ERROR{RESET}   {e}")
                total_errors += 1
            for w in warnings:
                print(f"    {YELLOW}WARNING{RESET} {w}")
                total_warnings += 1
            print()

    # ── NEW: subject usage census ─────────────────────────────────────────────
    census = build_subject_census(subject_names)
    used = [(n, c) for n, c in census.items() if c > 0]
    unused = [n for n, c in census.items() if c == 0]
    print("─" * 60)
    print("SUBJECT USAGE CENSUS")
    print(f"  {len(used)} of {len(subject_names)} subjects in use across {len(message_files)} message(s)\n")
    for name, count in sorted(used, key=lambda x: (-x[1], x[0])):
        print(f"  {count:4d}  {name}")
    if unused:
        print(f"\n  Not yet used ({len(unused)}) - expected while the archive backlog is being processed:")
        for name in unused:
            print(f"     -  {name}")
    print()

    # ── Summary ───────────────────────────────────────────────────────────────
    print("─" * 60)
    if total_errors == 0 and total_warnings == 0:
        print(f"{GREEN}✅ All {len(message_files)} file(s) passed validation with no issues.{RESET}\n")
        sys.exit(0)
    else:
        print(f"Files with issues: {files_with_issues} / {len(message_files)}")
        if total_errors > 0:
            print(f"{RED}Errors:   {total_errors}{RESET}")
        if total_warnings > 0:
            print(f"{YELLOW}Warnings: {total_warnings}{RESET}")
        print()
        if total_errors > 0:
            print(f"{RED}❌ Validation failed. Please fix errors before committing.{RESET}\n")
            sys.exit(1)
        else:
            print(f"{YELLOW}⚠️  Validation passed with warnings. Please review.{RESET}\n")
            sys.exit(0)


if __name__ == "__main__":
    main()