#!/usr/bin/env python3
"""check_dashes.py - repository-wide em/en dash sweep. Report-only.

Finds every em dash (U+2014) and en dash (U+2013) in the repository's
markdown, YAML, and text files, reporting file, line number, and context so
each occurrence can be judged: curator-written fields get corrected per the
schema.md ruling; body-text occurrences need curator approval per message.
Changes nothing.

Run from the repository root:  python .github/scripts/check_dashes.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve()
while not (ROOT / "content").is_dir():
    if ROOT == ROOT.parent:
        raise SystemExit("Could not find the repository root above this script.")
    ROOT = ROOT.parent

SKIP_DIRS = {".git", "node_modules", "obsidian-vault", ".obsidian"}
EXTS = {".md", ".yml", ".yaml", ".txt"}
DASHES = {"\u2014": "EM", "\u2013": "EN"}

hits, files_hit, scanned = [], set(), 0
for f in sorted(ROOT.rglob("*")):
    if not f.is_file() or f.suffix.lower() not in EXTS:
        continue
    if any(part in SKIP_DIRS for part in f.parts):
        continue
    scanned += 1
    try:
        text = f.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        hits.append((f, 0, "??", "file is not valid UTF-8"))
        continue
    for lineno, line in enumerate(text.splitlines(), 1):
        for ch, label in DASHES.items():
            if ch in line:
                col = line.index(ch)
                ctx = line[max(0, col - 30):col + 30].strip()
                hits.append((f, lineno, label, ctx))
                files_hit.add(f)

print(f"Scanned {scanned} files.")
if not hits:
    print("No em or en dashes found.")
else:
    print(f"{len(hits)} occurrence(s) in {len(files_hit)} file(s):\n")
    for f, lineno, label, ctx in hits:
        print(f"  {f.relative_to(ROOT)}:{lineno} [{label}] ...{ctx}...")
    print("\nReminder: curator fields correct per the ruling; body text needs")
    print("per-message curator approval; en dashes in bodies may be legitimate.")