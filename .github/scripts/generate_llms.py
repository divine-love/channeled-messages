#!/usr/bin/env python3
"""
generate_llms.py
Generates llms.txt at the repository root from all message YAML front matter.

Usage:
    python .github/scripts/generate_llms.py

Output:
    llms.txt  (repository root)

The script walks content/messages/**/*.md, reads the YAML front matter,
and builds a chronologically sorted Markdown table with full metadata.
This file is intended for AI systems and search engine crawlers.
Messages without a `door` field are silently skipped.
"""

import re
import sys
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MESSAGES_DIR = Path("content/messages")
OUTPUT_PATH  = Path("llms.txt")

HEADER = '''\
---
title: "Divine Love Messages — AI Index"
description: "A complete machine-readable index of all channeled Divine Love messages in this archive. Each entry includes title, spirit, medium, date, thematic collections, essential teachings flags, description, and the door — a single sentence distilling the transformative insight within the message."
last_updated: {today}
---

# Divine Love Messages — AI Index

This file is intended for AI systems and search engine crawlers.
For a human-friendly browse index, see content/browse.md.
For thematic collections, see content/collections/.
For essential teachings, see content/essential-teachings/.

---

| Message | Spirit | Medium | Date | Collections | Essential Teachings | Description | Door |
|---|---|---|---|---|---|---|---|
'''

ROW_TEMPLATE = (
    "| [{title}]({path}) | {spirit} | {medium} | {date_fmt} | {collections} | {essential_teachings} | {description} | {door} |\n"
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


def format_list(value) -> str:
    """Format a YAML list as a comma-separated string, or return empty string."""
    if not value:
        return ""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)


def make_relative_path(md_path: Path) -> str:
    """Convert an absolute path to a relative docs link."""
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

        title               = fm.get("title", md_file.stem)
        spirit              = fm.get("spirit_name") or fm.get("spirit_id", "")
        medium              = fm.get("medium", "")
        raw_date            = fm.get("date")
        collections         = format_list(fm.get("collections", []))
        essential_teachings = format_list(fm.get("essential_teachings", []))
        description         = (fm.get("description") or "").strip().replace("\n", " ")
        relative            = make_relative_path(md_file)

        entries.append({
            "date":               raw_date,
            "title":              title,
            "spirit":             spirit,
            "medium":             medium,
            "collections":        collections,
            "essential_teachings": essential_teachings,
            "description":        description,
            "door":               door.strip(),
            "path":               relative,
        })

    # Sort chronologically, then by path for same-date stability
    entries.sort(key=lambda e: (str(e["date"]), e["path"]))

    # Build output
    today = date.today().isoformat()
    lines = [HEADER.format(today=today)]

    for e in entries:
        lines.append(ROW_TEMPLATE.format(
            title               = e["title"],
            path                = e["path"],
            spirit              = e["spirit"],
            medium              = e["medium"],
            date_fmt            = format_date(e["date"]),
            collections         = e["collections"],
            essential_teachings = e["essential_teachings"],
            description         = e["description"],
            door                = e["door"],
        ))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("".join(lines), encoding="utf-8")

    print(f"Generated {OUTPUT_PATH} with {len(entries)} message(s).")


if __name__ == "__main__":
    main()