#!/usr/bin/env python3
"""
generate_doors.py
Generates docs/doors.md from the `door` field in all message YAML front matter.

Usage:
    python .github/scripts/generate_doors.py

Output:
    docs/doors.md  (or the path set in OUTPUT_PATH below)

The script walks content/messages/**/*.md, reads the YAML front matter,
and builds a chronologically sorted Markdown table. Messages without a
`door` field are silently skipped.
"""

import os
import re
import sys
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MESSAGES_DIR = Path("content/messages")
OUTPUT_PATH  = Path("content/doors.md")

HEADER = '''\
---
title: "The Doors"
description: "Augustine teaches that hidden within each channeled message is a great door to growing your souls and making yourselves a clearer channel of Love in the world. This index collects those doors - one per message - as an invitation to enter."
last_updated: {today}
---

# The Doors

> "Remember the words we have spoken to you, beloveds. Contemplate these words, these teachings, for hidden within each lesson is a great door to growing your souls and making yourselves a clearer channel of Love in the world."
> — Augustine, April 19, 2016

---

| Message | Spirit | Date | The Door |
|---|---|---|---|
'''

ROW_TEMPLATE = (
    "| [{title}]({path}) | {spirit} | {date_fmt} | {door} |\n"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def parse_front_matter(text: str) -> dict:
    """Extract and parse YAML front matter from a Markdown string."""
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return {}
    try:
        import yaml
        return yaml.safe_load(match.group(1)) or {}
    except Exception:
        return {}


def format_date(d) -> str:
    """Format a date as YYYY‑MM‑DD with non-breaking hyphens for the table."""
    if isinstance(d, date):
        return str(d).replace("-", "\u2011")
    return str(d).replace("-", "\u2011")


def make_relative_path(md_path: Path) -> str:
    """Convert an absolute path to a relative docs link."""
    # e.g. content/messages/2015/05/2015-05-03-af-confucius.md
    # → messages/2015/05/2015-05-03-af-confucius.md
    try:
        return str(md_path.relative_to("content")).replace("\\", "/")
    except ValueError:
        return str(md_path).replace("\\", "/")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not MESSAGES_DIR.exists():
        print(f"ERROR: Messages directory not found: {MESSAGES_DIR}", file=sys.stderr)
        sys.exit(1)

    entries = []

    for md_file in sorted(MESSAGES_DIR.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        fm = parse_front_matter(text)

        door = fm.get("door")
        if not door:
            continue  # skip messages without a door

        title        = fm.get("title", md_file.stem)
        spirit       = fm.get("spirit_name") or fm.get("spirit_id", "")
        raw_date     = fm.get("date")
        relative     = make_relative_path(md_file)

        entries.append({
            "date":    raw_date,
            "title":   title,
            "spirit":  spirit,
            "door":    door.strip(),
            "path":    relative,
        })

    # Sort chronologically, then by path for same-date stability
    entries.sort(key=lambda e: (str(e["date"]), e["path"]))

    # Build output
    today = date.today().isoformat()
    lines = [HEADER.format(today=today)]

    for e in entries:
        lines.append(ROW_TEMPLATE.format(
            title    = e["title"],
            path     = e["path"],
            spirit   = e["spirit"],
            date_fmt = format_date(e["date"]),
            door     = e["door"],
        ))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("".join(lines), encoding="utf-8")

    print(f"Generated {OUTPUT_PATH} with {len(entries)} door(s).")


if __name__ == "__main__":
    main()