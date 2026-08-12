#!/usr/bin/env python3
"""
check_names.py - find invisible or unusual characters in generated note names.

A zero-width space, non-breaking space, soft hyphen or bidi mark in a name is
invisible in every editor, matches itself perfectly inside Obsidian, and then
fails on Obsidian Publish, which normalizes them out of URLs. The symptom is a
link that works locally and 404s on the site.

Usage (from the repository root):
    python .github/scripts/check_names.py
"""
import sys
import unicodedata
from pathlib import Path

VAULT = Path("obsidian-vault")

# Characters that are legal in a filename but invisible or easily confused.
SUSPECT = {
    "\u00a0": "NO-BREAK SPACE",
    "\u200b": "ZERO WIDTH SPACE",
    "\u200c": "ZERO WIDTH NON-JOINER",
    "\u200d": "ZERO WIDTH JOINER",
    "\u200e": "LEFT-TO-RIGHT MARK",
    "\u200f": "RIGHT-TO-LEFT MARK",
    "\u2060": "WORD JOINER",
    "\ufeff": "ZERO WIDTH NO-BREAK SPACE (BOM)",
    "\u00ad": "SOFT HYPHEN",
    "\u2011": "NON-BREAKING HYPHEN",
    "\u2013": "EN DASH",
    "\u2014": "EM DASH",
    "\u2018": "LEFT SINGLE QUOTE",
    "\u2019": "RIGHT SINGLE QUOTE",
    "\u201c": "LEFT DOUBLE QUOTE",
    "\u201d": "RIGHT DOUBLE QUOTE",
}


def inspect(label, text, where):
    hits = []
    for i, ch in enumerate(text):
        if ch in SUSPECT:
            hits.append((i, ch, SUSPECT[ch]))
        elif ord(ch) > 127 and unicodedata.category(ch) in ("Cf", "Zs"):
            hits.append((i, ch, unicodedata.name(ch, "UNNAMED")))
    if hits:
        print(f"\n{where}: {label!r}")
        for i, ch, name in hits:
            print(f"    position {i}: U+{ord(ch):04X}  {name}")
    return bool(hits)


def main():
    if not VAULT.exists():
        print("Run from the repository root, after generate_vault.py.")
        sys.exit(1)

    found = 0
    for path in sorted(VAULT.rglob("*.md")):
        rel = path.relative_to(VAULT)
        if inspect(path.stem, path.stem, f"FILENAME  {rel.parent}"):
            found += 1

    # Wikilink targets: a link can carry a character its target does not.
    import re
    link_re = re.compile(r"\[\[([^\]|#]+)")
    seen = set()
    for path in sorted(VAULT.rglob("*.md")):
        for m in link_re.finditer(path.read_text(encoding="utf-8")):
            target = m.group(1).strip()
            if target in seen:
                continue
            seen.add(target)
            if inspect(target, target, f"LINK TARGET  (in {path.name})"):
                found += 1

    print(f"\n{'-' * 60}")
    if found:
        print(f"{found} name(s) carry invisible or unusual characters.")
        print("Fix the source (the DESCRIPTIONS dict, subjects.yml, a message's")
        print("front matter) rather than the generated file, then rebuild.")
    else:
        print("No invisible characters found in note names or link targets.")


if __name__ == "__main__":
    main()