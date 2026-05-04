#!/usr/bin/env python3
"""Remove stray YAML document-end '...' markers inserted into front matter."""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CONTENT_DIR = REPO_ROOT / "content"

FRONT_MATTER_RE = re.compile(r'^(---\n)(.*?)(\n---\n)', re.DOTALL)

fixed = 0
clean = 0

for md_file in CONTENT_DIR.rglob("*.md"):
    text = md_file.read_text(encoding="utf-8")
    m = FRONT_MATTER_RE.match(text)
    if not m:
        continue

    fm_body = m.group(2)
    # A bare '...' on its own line inside the front matter is a yaml.dump artifact
    if "\n...\n" not in fm_body and not fm_body.endswith("\n..."):
        clean += 1
        continue

    new_fm = re.sub(r'\n\.\.\.$', '', fm_body)   # at end of fm body
    new_fm = re.sub(r'\n\.\.\.\n', '\n', new_fm)  # mid fm body

    if new_fm == fm_body:
        clean += 1
        continue

    new_text = text.replace(m.group(0), f"{m.group(1)}{new_fm}{m.group(3)}", 1)
    md_file.write_text(new_text, encoding="utf-8")
    print(f"  fixed: {md_file.relative_to(REPO_ROOT)}")
    fixed += 1

print(f"\nDone. Fixed: {fixed}  Already clean: {clean}")
