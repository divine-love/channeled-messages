#!/usr/bin/env python3
"""check_body_endings.py - flag message bodies that look truncated.

The 2016-01-08-af-jesus truncation ended mid-sentence on a comma. Files
catalogued before the batch kit's programmatic body-fidelity check have never
been verified against their sources, so this sweep applies a cheap heuristic
to every message: a channelled message body should end in terminal
punctuation (usually a benediction). Flags bodies ending in a comma,
semicolon, colon, dash, or a bare lowercase word, plus suspiciously short
bodies. Heuristic only: it catches mid-sentence truncation, not a cleanly
dropped final paragraph. Report-only; changes nothing.

Run from the repository root:  python .github/scripts/check_body_endings.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve()
while not (ROOT / "content" / "messages").is_dir():
    if ROOT == ROOT.parent:
        raise SystemExit("Could not find content/messages above this script.")
    ROOT = ROOT.parent

OK_ENDINGS = tuple('.!?"\u201d\u2019' + "'" + ')]')
flagged, checked = [], 0

for f in sorted((ROOT / "content" / "messages").rglob("*.md")):
    text = f.read_text(encoding="utf-8")
    parts = re.split(r"^---\s*$", text, flags=re.M)
    if len(parts) < 3:
        flagged.append((f, "no front-matter fences found"))
        continue
    body = "---".join(parts[2:]).strip()
    checked += 1
    if not body:
        flagged.append((f, "empty body"))
    elif len(body) < 200:
        flagged.append((f, f"very short body ({len(body)} chars)"))
    elif not body.endswith(OK_ENDINGS):
        last = body[-60:].replace("\n", " ")
        flagged.append((f, f"non-terminal ending: ...{last!r}"))

print(f"Checked {checked} message bodies.")
if flagged:
    print(f"{len(flagged)} flagged for review:")
    for f, why in flagged:
        print(f"  {f.relative_to(ROOT)}: {why}")
else:
    print("No suspicious endings found.")