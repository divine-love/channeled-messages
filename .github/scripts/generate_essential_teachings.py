#!/usr/bin/env python3
"""
generate_essential_teachings.py
Generates one Markdown file per category in content/essential-teachings/.

Usage:
    python .github/scripts/generate_essential_teachings.py

Output:
    content/essential-teachings/{category-slug}.md  (one file per category)

The script walks content/messages/**/*.md, reads the YAML front matter,
and groups messages by their `essential_teachings` field. One file is
generated per category that has at least one message. Categories with no
messages are skipped. Messages may belong to multiple categories.

Valid categories are defined in metadata/essential-teachings.yml.
"""

import re
import sys
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MESSAGES_DIR = Path("content/messages")
OUTPUT_DIR   = Path("content/essential-teachings")

# Valid categories and their slugs
CATEGORIES = {
    "Core Teaching":   "core-teaching",
    "Divine Healing":  "divine-healing",
    "Historical":      "historical",
    "Milestone":       "milestone",
    "Prophecy":        "prophecy",
    "Spirit Biography": "spirit-biography",
}

# Descriptions for each category (shown at top of each generated file)
DESCRIPTIONS = {
    "Core Teaching": (
        "Messages that establish or clarify core doctrine, vision, or mission "
        "of the Divine Love path. These are the messages that form the "
        "theological and spiritual foundation of the archive — teachings a "
        "newcomer would be directed to first, and that curators return to "
        "when seeking clarity on the path's central truths."
    ),
    "Divine Healing": (
        "Messages that describe, demonstrate, or teach the mechanics of divine "
        "healing. Includes both accounts of healing events and instruction on "
        "how divine healing works — through prayer, soul purity, and the "
        "inflowing of God's Love."
    ),
    "Historical": (
        "Messages of particular historical importance in the archive — marking "
        "a significant moment in the history of the Divine Love movement, the "
        "development of a circle, or the record of an event that will be of "
        "lasting interest to researchers and historians of the movement."
    ),
    "Milestone": (
        "Messages marking a significant moment in the archive's history — the "
        "establishment of a circle, the beginning or end of a major gathering, "
        "a notable first, or another event that represents a threshold in the "
        "unfolding of the Divine Love mission."
    ),
    "Prophecy": (
        "Messages containing specific predictions about the world, humanity, "
        "or the Divine Love movement. Prophecies in the archive are given by "
        "Celestial spirits and concern future events, spiritual shifts, and "
        "the unfolding of God's plan for humanity."
    ),
    "Spirit Biography": (
        "Messages in which a spirit provides significant information about "
        "their own Earth life, identity, or experience in spirit. These "
        "messages are valuable both spiritually and historically, offering "
        "first-person testimony from spirits whose lives are part of the "
        "broader human and sacred record."
    ),
}

FILE_HEADER = '''\
---
title: "{category}"
description: "{description}"
last_updated: {today}
---

# {category}

{description}

---

| Message | Date | Description |
|---|---|---|
'''

ROW_TEMPLATE = (
    "| [{title}]({path}) | {date_fmt} | {description} |\n"
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

    # Group messages by category
    category_entries: dict[str, list[dict]] = {name: [] for name in CATEGORIES}

    for md_file in sorted(MESSAGES_DIR.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        fm = parse_front_matter(text)

        essential_teachings = fm.get("essential_teachings", [])
        if not essential_teachings:
            continue

        if isinstance(essential_teachings, str):
            essential_teachings = [essential_teachings]

        title       = fm.get("title", md_file.stem)
        raw_date    = fm.get("date")
        description = (fm.get("description") or "").strip().replace("\n", " ")
        relative    = make_relative_path(md_file)

        for category in essential_teachings:
            if category in category_entries:
                category_entries[category].append({
                    "date":        raw_date,
                    "title":       title,
                    "description": description,
                    "path":        relative,
                })

    # Generate one file per category that has messages
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    generated = 0

    for category_name, entries in category_entries.items():
        if not entries:
            continue  # skip categories with no messages

        # Sort chronologically, then by path for same-date stability
        entries.sort(key=lambda e: (str(e["date"]), e["path"]))

        slug        = CATEGORIES[category_name]
        output_file = OUTPUT_DIR / f"{slug}.md"
        description = DESCRIPTIONS.get(category_name, "")

        lines = [FILE_HEADER.format(
            category    = category_name,
            description = description,
            today       = today,
        )]

        for e in entries:
            lines.append(ROW_TEMPLATE.format(
                title       = e["title"],
                path        = e["path"],
                date_fmt    = format_date(e["date"]),
                description = e["description"],
            ))

        output_file.write_text("".join(lines), encoding="utf-8")
        print(f"Generated {output_file} with {len(entries)} message(s).")
        generated += 1

    print(f"\nDone. {generated} essential teachings file(s) generated in {OUTPUT_DIR}.")


if __name__ == "__main__":
    main()