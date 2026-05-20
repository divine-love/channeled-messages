#!/usr/bin/env python3
"""
generate_collections.py
Generates one Markdown file per thematic collection in content/collections/.

Usage:
    python .github/scripts/generate_collections.py

Output:
    content/collections/{collection-slug}.md  (one file per collection)

The script walks content/messages/**/*.md, reads the YAML front matter,
and groups messages by their `collections` field. One file is generated
per collection that has at least one message. Collections with no messages
are skipped. Messages may belong to multiple collections.

Valid collections are defined in metadata/collections.yml.
"""

import re
import sys
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MESSAGES_DIR    = Path("content/messages")
OUTPUT_DIR      = Path("content/collections")
COLLECTIONS_YML = Path("metadata/collections.yml")

# Valid collections and their slugs — order determines file sort order
COLLECTIONS = {
    "Awakening Humanity":          "awakening-humanity",
    "Healing Path":                "healing-path",
    "Jesus Speaks":                "jesus-speaks",
    "Letters from History":        "letters-from-history",
    "Mind & Soul":                 "mind-and-soul",
    "Prism of the Soul":           "prism-of-the-soul",
    "Service & Mission":           "service-and-mission",
    "The Saints & Apostles Speak": "saints-and-apostles",
    "Two Paths":                   "two-paths",
}

# Descriptions for each collection (shown at top of each generated file)
DESCRIPTIONS = {
    "Awakening Humanity": (
        "Messages concerning the broader spiritual awakening of humanity — "
        "the global shift in consciousness that the Divine Love teachings "
        "anticipate and call forth. Includes teachings on the role of prayer "
        "circles, light workers, and the awakening mission in the world."
    ),
    "Healing Path": (
        "Messages about healing in all its dimensions — physical, emotional, "
        "and spiritual. Includes teachings on how Divine Love heals, the "
        "mechanics of spirit healing, and the restoration of the soul and body "
        "through prayer and God's Love."
    ),
    "Jesus Speaks": (
        "Messages channelled directly from Jesus of Nazareth. Jesus is the "
        "foremost teacher in the Divine Love archive, speaking on prayer, "
        "the soul, at-onement, service, and the truth of God's Love as the "
        "heart of his original mission."
    ),
    "Letters from History": (
        "Messages from historical figures beyond the biblical canon — "
        "philosophers, rulers, mystics, scientists, and others speaking "
        "from their perspective in spirit about Divine Love, truth, and the "
        "soul's journey."
    ),
    "Mind & Soul": (
        "Messages exploring the relationship between the material mind and "
        "the soul — how the mind can assist or obstruct the soul's growth, "
        "the integration of mind and soul, and the soul's faculties of "
        "perception and knowing."
    ),
    "Prism of the Soul": (
        "Messages exploring the nature, faculties, and gifts of the soul — "
        "its capacity for Divine Love, its unique expression, its senses, "
        "and the gifts that emerge as it is awakened and transformed."
    ),
    "Service & Mission": (
        "Messages about service, mediumship, and the mission of those "
        "called to carry Divine Love to the world. Covers the development "
        "of gifts, the challenges of being a channel of love, and the "
        "calling to awaken others."
    ),
    "The Saints & Apostles Speak": (
        "Messages from the biblical apostles and saints speaking directly "
        "from their perspective in spirit — Andrew, James, John the Beloved, "
        "Peter, Matthew, Mark, Luke, Francis of Assisi, and others. These "
        "spirits offer personal testimony, teaching, and encouragement "
        "grounded in their own experience of Divine Love."
    ),
    "Two Paths": (
        "Messages contrasting the natural love path and the Divine Love path — "
        "the two ways a soul may progress after physical life. Clarifies the "
        "distinction between natural love (which leads to the soul spheres) "
        "and Divine Love (which leads to the Celestial Heavens and "
        "at-onement with God)."
    ),
}

FILE_HEADER = '''\
---
title: "{collection}"
description: "{description}"
last_updated: {today}
---

# {collection}

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
        return "../" + str(md_path.relative_to("content")).replace("\\", "/")
    except ValueError:
        return str(md_path).replace("\\", "/")


def slugify(name: str) -> str:
    """Return the slug for a collection name."""
    return COLLECTIONS.get(name, name.lower().replace(" ", "-").replace("&", "and"))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not MESSAGES_DIR.exists():
        print(f"ERROR: Messages directory not found: {MESSAGES_DIR}", file=sys.stderr)
        sys.exit(1)

    # Group messages by collection
    collection_entries: dict[str, list[dict]] = {name: [] for name in COLLECTIONS}

    for md_file in sorted(MESSAGES_DIR.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        fm = parse_front_matter(text)

        collections = fm.get("collections", [])
        if not collections:
            continue

        if isinstance(collections, str):
            collections = [collections]

        title       = fm.get("title", md_file.stem)
        raw_date    = fm.get("date")
        description = (fm.get("description") or "").strip().replace("\n", " ")
        relative    = make_relative_path(md_file)

        for collection in collections:
            if collection in collection_entries:
                collection_entries[collection].append({
                    "date":        raw_date,
                    "title":       title,
                    "description": description,
                    "path":        relative,
                })

    # Generate one file per collection that has messages
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    generated = 0

    for collection_name, entries in collection_entries.items():
        if not entries:
            continue  # skip collections with no messages

        # Sort chronologically, then by path for same-date stability
        entries.sort(key=lambda e: (str(e["date"]), e["path"]))

        slug        = slugify(collection_name)
        output_file = OUTPUT_DIR / f"{slug}.md"
        description = DESCRIPTIONS.get(collection_name, "")

        lines = [FILE_HEADER.format(
            collection  = collection_name,
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

    print(f"\nDone. {generated} collection file(s) generated in {OUTPUT_DIR}.")


if __name__ == "__main__":
    main()