#!/usr/bin/env python3
"""
validate_prayers.py
Checks the spirit-given prayer files in content/practices/.

A prayer file is any file in content/practices/ whose name starts with
"prayer-" followed by a message_id, for example
prayer-2016-09-04-af-john-the-beloved.md. Its shape is set out in
content/templates/prayer-template.md and in schema.md, section 6,
"Spirit-Given Prayers". Other files in content/practices/ (the Prayer for
Divine Love versions, healing-merkaba.md) are a different kind of page and
are not checked here.

Checks, each reported as an error:
  - the front matter parses and uses only the fields in the template
  - every required field is present
  - type is "prayer"
  - practice_id is the filename, and the filename is prayer-{source_message}
    (with -2, -3 ... if one message gives more than one prayer)
  - source_message is a real message
  - spirit_id has a spirit file, and is the spirit who delivers the source
    message or one listed in its spirits[]
  - medium and date_received match the source message
  - primary_subjects is one subject, secondary_subjects is at most five,
    and every subject is defined in metadata/subjects.yml
  - description is no longer than 600 characters
  - no em dashes in title, description or notes
  - last_edited is a date
  - the footer line names the right spirit, medium and date, and links to
    the source message
  - the prayer text appears in the source message word for word. Italics and
    the enclosing quotation marks are ignored, and so is the final
    punctuation mark, since one may be supplied for the standalone text.
    Words in [square brackets] are curator additions and are set aside
    before the comparison.

Run locally:  python .github/scripts/validate_prayers.py
Run in CI:    automatically, by the Validate and Generate workflow
"""

import re
import sys
import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
PRACTICES_DIR = ROOT / "content" / "practices"
MESSAGES_DIR = ROOT / "content" / "messages"
SPIRITS_DIR = ROOT / "spirits"
SUBJECTS_PATH = ROOT / "metadata" / "subjects.yml"

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

REQUIRED = [
    "practice_id", "title", "type", "source_message", "spirit_id",
    "spirit_name", "medium", "date_received", "primary_subjects",
    "description", "language", "last_edited",
]
OPTIONAL = ["secondary_subjects", "notes"]
ALLOWED = set(REQUIRED) | set(OPTIONAL)

PRAYER_FILE = re.compile(r"^prayer-\d{4}-\d{2}-\d{2}-[a-z]{2}-[a-z0-9-]+$")
FOOTER = re.compile(
    r"^\*Given by (?P<spirit>.+?) through (?P<medium>.+?), "
    r"(?P<date>[A-Z][a-z]+ \d{1,2}, \d{4})\. The full message is at "
    r"\[(?P<label>[^\]]+)\]\(\.\./messages/(?P<path>[^)]+)\)\.\*$"
)
EM_DASH = "—"


def split_front_matter(text):
    """Return (front matter dict, body text) for a file with --- fences."""
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return yaml.safe_load(text[4:end]) or {}, text[end + 5:]


def load_messages():
    """Index every message by message_id: its front matter and body."""
    messages = {}
    for path in MESSAGES_DIR.rglob("*.md"):
        fm, body = split_front_matter(path.read_text(encoding="utf-8"))
        if fm and fm.get("message_id"):
            messages[fm["message_id"]] = (path, fm, body)
    return messages


def load_subjects():
    data = yaml.safe_load(SUBJECTS_PATH.read_text(encoding="utf-8"))
    names = set()
    for cat in data.get("main_categories", []):
        names.add(cat["name"])
        for sub in cat.get("subcategories", []) or []:
            names.add(sub["name"])
    return names


def normalise(text):
    """Reduce text to its words and marks, for a word-for-word comparison."""
    text = text.replace("*", "")
    text = text.translate(str.maketrans({"“": '"', "”": '"',
                                         "‘": "'", "’": "'"}))
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r" ([.,;:!?])", r"\1", text)
    return text.strip()


def prayer_found(prayer, source_body):
    """True if the prayer appears in the source message as received."""
    source = normalise(source_body)
    candidates = [prayer, re.sub(r"\[[^\]]*\]", " ", prayer)]
    for c in candidates:
        c = normalise(c).strip(" \"'.,;:!?")
        if c and c in source:
            return True
    return False


def as_date(value):
    if isinstance(value, datetime.date):
        return value
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError:
        return None


def check(path, messages, spirit_ids, subjects):
    errors = []
    stem = path.stem
    try:
        fm, body = split_front_matter(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        return [f"front matter does not parse: {e}"]
    if fm is None:
        return ["no front matter between --- lines at the top of the file"]

    extra = sorted(set(fm) - ALLOWED)
    if extra:
        errors.append(f"fields not in the prayer template: {', '.join(extra)}")
    missing = [f for f in REQUIRED if f not in fm or fm[f] in (None, "")]
    if missing:
        errors.append(f"required fields missing or empty: {', '.join(missing)}")

    if fm.get("type") not in (None, "prayer"):
        errors.append(f"type is '{fm.get('type')}', expected 'prayer'")

    if fm.get("practice_id") and fm["practice_id"] != stem:
        errors.append(f"practice_id '{fm['practice_id']}' does not match the "
                      f"filename '{stem}'")

    # ── source message ────────────────────────────────────────────────────────
    src_id = fm.get("source_message")
    src = messages.get(src_id) if src_id else None
    if src_id and not src:
        errors.append(f"source_message '{src_id}' is not a known message_id")
    if src_id and not re.fullmatch(rf"prayer-{re.escape(src_id)}(-\d+)?", stem):
        errors.append(f"filename should be prayer-{src_id}.md "
                      f"(or prayer-{src_id}-2.md for a second prayer)")

    sid = fm.get("spirit_id")
    if sid and sid not in spirit_ids:
        errors.append(f"spirit_id '{sid}' has no file in spirits/")

    if src:
        src_path, src_fm, src_body = src
        speakers = [src_fm.get("spirit_id")] + list(src_fm.get("spirits") or [])
        if sid and sid not in speakers:
            errors.append(f"spirit_id '{sid}' is neither the spirit who "
                          f"delivers {src_id} nor listed in its spirits[]")
        if fm.get("medium") and fm["medium"] != src_fm.get("medium"):
            errors.append(f"medium '{fm['medium']}' does not match the source "
                          f"message ('{src_fm.get('medium')}')")
        d, sd = as_date(fm.get("date_received")), as_date(src_fm.get("date"))
        if fm.get("date_received") and d != sd:
            errors.append(f"date_received {fm.get('date_received')} does not "
                          f"match the source message date {src_fm.get('date')}")

    # ── subjects ──────────────────────────────────────────────────────────────
    primary = fm.get("primary_subjects")
    if primary is not None and not isinstance(primary, str):
        errors.append("primary_subjects must be a single subject, not a list")
    secondary = fm.get("secondary_subjects") or []
    if not isinstance(secondary, list):
        errors.append("secondary_subjects must be a list")
        secondary = []
    if len(secondary) > 5:
        errors.append(f"secondary_subjects has {len(secondary)} entries; "
                      f"the most allowed is five")
    for s in ([primary] if isinstance(primary, str) else []) + secondary:
        if s not in subjects:
            errors.append(f"subject '{s}' is not defined in metadata/subjects.yml")

    # ── curator-written fields ────────────────────────────────────────────────
    desc = fm.get("description") or ""
    if len(str(desc).strip()) > 600:
        errors.append(f"description is {len(str(desc).strip())} characters; "
                      f"the most allowed is 600")
    for field in ("title", "description", "notes"):
        if EM_DASH in str(fm.get(field) or ""):
            errors.append(f"{field} contains an em dash")
    if fm.get("last_edited") and not as_date(fm["last_edited"]):
        errors.append(f"last_edited '{fm['last_edited']}' is not a date")

    # ── body: prayer text, then a --- line, then the footer ──────────────────
    parts = re.split(r"\n---\n", body.strip("\n"), maxsplit=1)
    prayer = parts[0].strip()
    footer = parts[1].strip() if len(parts) > 1 else ""
    if not prayer:
        errors.append("no prayer text after the front matter")
    m = FOOTER.match(footer)
    if not m:
        errors.append("footer line missing or not in the template's form: "
                      "*Given by {spirit} through {medium}, {Month D, YYYY}. "
                      "The full message is at [{id}](../messages/YYYY/MM/{id}.md).*")
    else:
        target = (PRACTICES_DIR / "../messages" / m["path"]).resolve()
        if not target.is_file():
            errors.append(f"footer link ../messages/{m['path']} does not "
                          f"point to a file")
        if src_id and (m["label"] != src_id or Path(m["path"]).stem != src_id):
            errors.append(f"footer link should name and point to {src_id}")
        if fm.get("spirit_name") and m["spirit"] != fm["spirit_name"]:
            errors.append(f"footer names '{m['spirit']}' but spirit_name is "
                          f"'{fm['spirit_name']}'")
        if fm.get("medium") and m["medium"] != fm["medium"]:
            errors.append(f"footer names '{m['medium']}' but medium is "
                          f"'{fm['medium']}'")
        d = as_date(fm.get("date_received"))
        if d and m["date"] != f"{d:%B} {d.day}, {d.year}":
            errors.append(f"footer date '{m['date']}' does not match "
                          f"date_received {d}")

    if src and prayer and not prayer_found(prayer, src[2]):
        errors.append(f"the prayer text does not appear word for word in "
                      f"{src_id}; check it against the message (words the "
                      f"curator adds go in [square brackets])")

    return errors


def main():
    messages = load_messages()
    spirit_ids = {p.stem for p in SPIRITS_DIR.glob("*.yml")}
    subjects = load_subjects()

    files = sorted(p for p in PRACTICES_DIR.glob("*.md")
                   if PRAYER_FILE.match(p.stem))
    print(f"\nChecking {len(files)} prayer file(s) in content/practices/...\n")

    total = 0
    for path in files:
        errors = check(path, messages, spirit_ids, subjects)
        if errors:
            print(f"  {path.relative_to(ROOT)}")
            for e in errors:
                print(f"    {RED}ERROR{RESET}   {e}")
            print()
            total += len(errors)

    print("─" * 60)
    if total:
        print(f"{RED}❌ {total} error(s) in prayer files.{RESET}\n")
        sys.exit(1)
    print(f"{GREEN}✅ All {len(files)} prayer file(s) passed validation.{RESET}\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
