#!/usr/bin/env python3
"""Insert door field into message front matter from doors.md table."""

import re
import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DOORS_FILE = REPO_ROOT / "content" / "doors.md"
CONTENT_DIR = REPO_ROOT / "content"

# Matches a table row: | [Title](path) | Spirit | Date | Door text |
ROW_RE = re.compile(
    r'^\|\s*\[.*?\]\(([^)]+)\)\s*\|[^|]+\|[^|]+\|\s*(.*?)\s*\|$'
)

# Matches the YAML front matter block
FRONT_MATTER_RE = re.compile(r'^---\n(.*?)\n---\n', re.DOTALL)


def yaml_scalar(value: str) -> str:
    """Return a properly quoted YAML scalar for the given string value."""
    # Wrap in a dict so PyYAML produces "k: <scalar>\n" — no document markers
    dumped = yaml.dump({"k": value}, allow_unicode=True, width=float("inf"))
    _, scalar = dumped.split("k: ", 1)
    return scalar.rstrip("\n")


def parse_doors_table(doors_path: Path) -> list[tuple[str, str]]:
    """Return list of (relative_path, door_text) from the doors.md table."""
    rows = []
    for line in doors_path.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line.strip())
        if m:
            path, door = m.group(1).strip(), m.group(2).strip()
            rows.append((path, door))
    return rows


def insert_door(file_path: Path, door_text: str) -> bool:
    """
    Insert `door:` into YAML front matter if not already present.
    Returns True if file was modified, False if skipped.
    """
    content = file_path.read_text(encoding="utf-8")

    fm_match = FRONT_MATTER_RE.match(content)
    if not fm_match:
        print(f"  WARNING: no front matter found in {file_path.name}", file=sys.stderr)
        return False

    fm_body = fm_match.group(1)

    # Skip if door field already exists
    if re.search(r'^door\s*:', fm_body, re.MULTILINE):
        return False

    door_line = f"door: {yaml_scalar(door_text)}"

    # Insert before last_edited if present, otherwise at end of front matter
    if re.search(r'^last_edited\s*:', fm_body, re.MULTILINE):
        new_fm_body = re.sub(
            r'^(last_edited\s*:.*)$',
            door_line + r'\n\1',
            fm_body,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        new_fm_body = fm_body + "\n" + door_line

    new_content = content.replace(fm_match.group(0), f"---\n{new_fm_body}\n---\n", 1)
    file_path.write_text(new_content, encoding="utf-8")
    return True


def main():
    rows = parse_doors_table(DOORS_FILE)
    print(f"Parsed {len(rows)} rows from doors.md")

    updated = 0
    skipped = 0
    missing = 0

    for rel_path, door_text in rows:
        msg_file = CONTENT_DIR / rel_path

        if not msg_file.exists():
            print(f"  MISSING: {rel_path}", file=sys.stderr)
            missing += 1
            continue

        if insert_door(msg_file, door_text):
            print(f"  updated: {rel_path}")
            updated += 1
        else:
            skipped += 1

    print(f"\nDone. Updated: {updated}  Skipped (already had door): {skipped}  Missing: {missing}")


if __name__ == "__main__":
    main()
