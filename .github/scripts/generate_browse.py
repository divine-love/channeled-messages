#!/usr/bin/env python3
"""
generate_browse.py
Generates content/browse.md from the `door` field in all message YAML front matter.

Usage:
    python .github/scripts/generate_browse.py

Output:
    content/browse.md  (or the path set in OUTPUT_PATH below)

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
OUTPUT_PATH  = Path("content/browse.md")
SPIRITS_DIR  = Path("spirits")
MEDIUMS_DIR  = Path("mediums")

# Link templates for the Spirit and Medium columns, relative to
# content/browse.md. Both directories sit at the repository root, hence the
# leading "../". A cell is only linked when its target file actually exists,
# so a spirit or medium without a file stays as plain text rather than
# becoming a broken link.
SPIRIT_LINK = "../spirits/{stem}.yml"
MEDIUM_LINK = "../mediums/{stem}.yml"

HEADER = '''\
---
title: "Browse All Messages"
description: "Augustine teaches that hidden within each channeled message is a great door to growing your souls and making yourselves a clearer channel of Love in the world. This index collects those doors - one per message - as an invitation to enter."
last_updated: {today}
---

# Browse All Messages

> "Remember the words we have spoken to you, beloveds. Contemplate these words, these teachings, for hidden within each lesson is a great door to growing your souls and making yourselves a clearer channel of Love in the world."
> — Augustine, April 19, 2016

---

| Message | Spirit | Medium | Date | The Door |
|---|---|---|---|---|
'''

ROW_TEMPLATE = (
    "| [{title}]({path}) | {spirit} | {medium} | {date_fmt} | {door} |\n"
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


def load_profile_stems(directory: Path) -> dict:
    """
    Map the names used in message front matter to profile file stems.

    Returns {lowercased name: stem} covering each file's own stem, its
    display name and any aliases, so that "Al Fike", "Jesus of Nazareth" and
    "Keea atta Kem" all resolve to the right file whatever casing or variant
    a message happens to use.
    """
    stems = {}
    if not directory.exists():
        return stems
    try:
        import yaml
    except ImportError:
        return stems
    for p in sorted(directory.glob("*.yml")):
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        names = [p.stem, p.stem.replace("-", " ")]
        for key in ("name", "spirit_name", "medium_name", "display_name"):
            if d.get(key):
                names.append(str(d[key]))
        for key in ("aliases", "spirit_aliases", "medium_aliases"):
            names.extend(str(a) for a in (d.get(key) or []))
        for n in names:
            stems.setdefault(n.strip().lower(), p.stem)
    return stems


def link_cell(label: str, stem: str, template: str, directory: Path) -> str:
    """Wrap a table cell's text in a Markdown link, if the target exists."""
    if not label or not stem:
        return label
    if not (directory / f"{stem}.yml").exists():
        return label
    return f"[{label}]({template.format(stem=stem)})"


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

    spirit_stems = load_profile_stems(SPIRITS_DIR)
    medium_stems = load_profile_stems(MEDIUMS_DIR)

    entries = []
    unlinked = set()

    for md_file in sorted(MESSAGES_DIR.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        fm = parse_front_matter(text)

        door = fm.get("door")
        if not door:
            continue  # skip messages without a door

        title    = fm.get("title", md_file.stem)
        spirit   = fm.get("spirit_name") or fm.get("spirit_id", "")
        medium   = fm.get("medium", "")
        raw_date = fm.get("date")
        relative = make_relative_path(md_file)

        # The message's own spirit_id is authoritative; fall back to matching
        # the displayed name for messages that carry no id.
        sp_stem = fm.get("spirit_id") or spirit_stems.get(str(spirit).lower(), "")
        md_stem = medium_stems.get(str(medium).lower(), "")
        spirit_cell = link_cell(spirit, sp_stem, SPIRIT_LINK, SPIRITS_DIR)
        medium_cell = link_cell(medium, md_stem, MEDIUM_LINK, MEDIUMS_DIR)
        if spirit and spirit_cell == spirit:
            unlinked.add(f"spirit: {spirit}")
        if medium and medium_cell == medium:
            unlinked.add(f"medium: {medium}")

        entries.append({
            "date":   raw_date,
            "title":  title,
            "spirit": spirit_cell,
            "medium": medium_cell,
            "door":   door.strip(),
            "path":   relative,
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
            medium   = e["medium"],
            date_fmt = format_date(e["date"]),
            door     = e["door"],
        ))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("".join(lines), encoding="utf-8")

    print(f"Generated {OUTPUT_PATH} with {len(entries)} door(s).")
    if unlinked:
        print(f"NOTE: {len(unlinked)} name(s) had no profile file, left as "
              f"plain text: {', '.join(sorted(unlinked))}")


if __name__ == "__main__":
    main()