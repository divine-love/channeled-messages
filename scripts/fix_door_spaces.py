#!/usr/bin/env python3
"""Collapse double spaces in door fields caused by YAML multi-line wrapping."""

import re
import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CONTENT_DIR = REPO_ROOT / "content" / "messages"

FRONT_MATTER_RE = re.compile(r'^(---\n)(.*?)(\n---\n)', re.DOTALL)
# Matches the door key plus any indented continuation lines
DOOR_FIELD_RE = re.compile(r'^(door:[ \t]*.*(?:\n[ \t]+.*)*)', re.MULTILINE)


def yaml_scalar(value: str) -> str:
    dumped = yaml.dump({"k": value}, allow_unicode=True, width=float("inf"))
    _, scalar = dumped.split("k: ", 1)
    return scalar.rstrip("\n")


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    fm_match = FRONT_MATTER_RE.match(text)
    if not fm_match:
        return False

    fm_body = fm_match.group(2)
    door_match = DOOR_FIELD_RE.search(fm_body)
    if not door_match:
        return False

    raw_door_block = door_match.group(1)

    # Parse just the door field as YAML to get the real string value
    parsed = yaml.safe_load(raw_door_block)
    if not isinstance(parsed, dict) or "door" not in parsed:
        print(f"  WARNING: could not parse door field in {path.name}", file=sys.stderr)
        return False

    current_value = parsed["door"]
    if not isinstance(current_value, str):
        return False

    normalized = re.sub(r" {2,}", " ", current_value).strip()

    if normalized == current_value and "\n" not in raw_door_block:
        return False  # already a clean single-line field, nothing to do

    new_door_line = f"door: {yaml_scalar(normalized)}"
    new_fm_body = fm_body[:door_match.start()] + new_door_line + fm_body[door_match.end():]
    new_text = text.replace(
        fm_match.group(0),
        f"{fm_match.group(1)}{new_fm_body}{fm_match.group(3)}",
        1,
    )
    path.write_text(new_text, encoding="utf-8")
    return True


def main():
    updated = 0
    skipped = 0
    for md_file in sorted(CONTENT_DIR.rglob("*.md")):
        if fix_file(md_file):
            print(f"  fixed: {md_file.relative_to(REPO_ROOT)}")
            updated += 1
        else:
            skipped += 1

    print(f"\nDone. Fixed: {updated}  Skipped: {skipped}")


if __name__ == "__main__":
    main()
