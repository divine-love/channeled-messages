#!/usr/bin/env python3
"""Convert door field from plain scalar to folded block scalar (door: >)."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CONTENT_DIR = REPO_ROOT / "content" / "messages"

# Matches a plain-scalar door field (not already a block scalar)
DOOR_PLAIN_RE = re.compile(r'^door: (?![>|])(.+)$', re.MULTILINE)

updated = skipped = 0

for md_file in sorted(CONTENT_DIR.rglob("*.md")):
    text = md_file.read_text(encoding="utf-8")
    m = DOOR_PLAIN_RE.search(text)
    if not m:
        skipped += 1
        continue

    value = m.group(1)
    new_field = f"door: >\n  {value}"
    new_text = text[:m.start()] + new_field + text[m.end():]
    md_file.write_text(new_text, encoding="utf-8")
    updated += 1

print(f"Done. Updated: {updated}  Skipped: {skipped}")
