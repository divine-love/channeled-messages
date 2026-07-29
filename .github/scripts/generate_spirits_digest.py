#!/usr/bin/env python3
"""generate_spirits_digest.py - concatenate spirits/*.yml into one file.

Produces spirits-digest.txt at the repository root: every spirit biography in
a single file, for attaching to Cowork batch-cataloguing sessions so the model
can cross-check biographical statements against what the files already carry.

Run from the repository root:  python .github/scripts/generate_spirits_digest.py
Regenerate before every Cowork session; a stale digest means wrong
confirmation calls.
"""
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve()
while not (ROOT / "spirits").is_dir():
    if ROOT == ROOT.parent:
        raise SystemExit("Could not find the spirits/ folder above this script.")
    ROOT = ROOT.parent

files = sorted((ROOT / "spirits").glob("*.yml"))
if not files:
    raise SystemExit("No spirit files found in spirits/.")

lines = [
    "SPIRITS DIGEST",
    f"Generated {date.today().isoformat()} from spirits/*.yml "
    f"({len(files)} files). Read-only reference for biography cross-checks;",
    "the individual spirit files remain canonical.",
    "",
]
for f in files:
    lines += [
        "=" * 72,
        f"FILE: spirits/{f.name}",
        "=" * 72,
        f.read_text(encoding="utf-8").rstrip(),
        "",
    ]

out = ROOT / "spirits-digest.txt"
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {out} ({len(files)} spirit files).")