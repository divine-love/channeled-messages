#!/usr/bin/env python3
"""
validate_chains.py
Validates the chains layer: metadata/chains-log.md and metadata/chains-threads.md,
against the conventions declared in their own design blocks.

Companion to validate_messages.py. That script validates the message corpus;
this one validates the thematic layer built on top of it. Stdlib only.

Two tiers of check:

  ERRORS  Conditions that are clean today. Any occurrence fails the build.
          - registry table and thread rosters in alphabetical order, and the
            roster is a subsequence of the registry
          - every slug used in the log exists in the registry or holding pen
          - one record per line in the log (no continuation lines)
          - entries in chronological order, no duplicate message_ids
          - role lines match '- `slug` **[Role]** : ' and use the controlled
            link-role vocabulary
          - both files carry an ISO last_updated in front matter

  DEBT    Conditions with known outstanding work. The current count is recorded
          in BASELINE below, and the build fails only if a count rises. When
          some are cleared, lower the number in BASELINE in the same commit;
          the script prints the value to use.

After validation, prints a DEBT LEDGER so drift is visible on every push,
in the same spirit as the subject usage census in validate_messages.py.

Run locally:  python .github/scripts/validate_chains.py
Run in CI:    automatically triggered by GitHub Actions on push/pull_request
"""

import re
import sys
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[2]
LOG_PATH = ROOT / "metadata" / "chains-log.md"
THREADS_PATH = ROOT / "metadata" / "chains-threads.md"

# ── Colours for terminal output ───────────────────────────────────────────────
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

# ── Debt baselines ────────────────────────────────────────────────────────────
# Lower these as the work is done. Never raise one to make a build pass.
BASELINE = {
    "minted_without_roster": 5,   # threads awaiting a roster entry
    "records_without_tier": 29,   # bare '- NOTE:' and bare '- (' records
    "roster_datestamps": 5,       # session dates inside roster entries
    "log_datestamps": 32,         # session dates inside log records
    "roster_counts": 37,          # size claims; some are benign back-references
    "roster_spans": 3,            # year spans and archive-extremum claims
    "stale_pen_notes": 2,         # pen-stage notes on already-minted slugs
}

# ── Controlled vocabulary, per the design blocks in both files ───────────────
ROLES = {
    "Foundation", "Elaboration", "Objection-removed", "Reframe",
    "Testimony", "Chrysalis", "Capstone",
}

ROLE_LINE = re.compile(r"^- `([a-z0-9-]+)` \*\*\[([\w-]+)\]\*\* : ")
NOTE_LINE = re.compile(r"^- NOTE\b")
RECORD = re.compile(r"^- (?:`|NOTE)")
ENTRY = re.compile(r"^### (\S+)")
MSG_ID = re.compile(r"\b\d{4}-\d{2}-\d{2}-[a-z]{2}-[a-z0-9-]+\b")
SESSION_DATE = re.compile(r"\b202[6-9]-\d{2}-\d{2}\b")
PEN_WORD = re.compile(r"\b(candidate|holding[ -]pen|penned)\b", re.I)

NUMBER = (r"\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven"
          r"|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen"
          r"|nineteen|twenty|thirty|forty|fifty|sixty"
          r"|[a-z]+ty-(?:one|two|three|four|five|six|seven|eight|nine)")
SIZE_NOUN = (r"member roles?|members|messages|spirits|witnesses|sightings"
             r"|elaborations")

# A count of what an entry currently holds goes stale as the archive grows.
COUNT = re.compile(r"\b(" + NUMBER + r")\s+(" + SIZE_NOUN + r")\b", re.I)

# A span is a count in different units: derived from the current earliest and
# latest members, so it breaks when one arrives outside the range. Likewise a
# claim that something is the earliest or latest thing in the archive, since
# messages are still being added at both ends.
SPAN = re.compile(
    r"\b(?:spanning|spans|span of|covering)\s+(?:" + NUMBER + r")\s+"
    r"(?:years|months|weeks|days)\b"

    r"|\b(?:19|20)\d{2}\s+to\s+(?:19|20)\d{2}\b"
    r"|\b(?:the\s+)?(?:earliest|latest|oldest|newest|first|last)\b"
    r"(?=(?:\W+\w+){0,6}?\W+(?:archive|corpus|collection|chain)\b)"
    r"|\barchive(?:'s)?(?:\W+\w+){0,3}?"
    r"\W+(?:earliest|latest|oldest|newest|first|last)\b", re.I)

# "in hand" is the honest hedge: it scopes a claim to what has been read so far
# rather than to the archive's extent, so it stays true as the archive grows.
SPAN_OK = re.compile(r"\bin\s+hand\b", re.I)

errors = []
debt = {key: [] for key in BASELINE}


def read(path):
    if not path.exists():
        print(f"{RED}Could not find {path}{RESET}")
        sys.exit(1)
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")


def check_frontmatter(lines, path):
    for line in lines[:20]:
        if line.startswith("last_updated:"):
            value = line.split(":", 1)[1].strip()
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                errors.append(f"{path.name}: last_updated is not ISO: {value!r}")
            return
    errors.append(f"{path.name}: no last_updated in front matter")


def roster_entries(threads):
    """Yield (slug, line_no, joined_text, lines) for each thread roster entry."""
    start = next(i for i, l in enumerate(threads)
                 if l.startswith("## Thread rosters"))
    end = next(i for i, l in enumerate(threads)
               if l.startswith("# Holding pen"))
    heads = [i for i in range(start, end) if re.match(r"^- `", threads[i])]
    for a, b in zip(heads, heads[1:] + [end]):
        slug = re.match(r"^- `([a-z0-9-]+)`", threads[a]).group(1)
        yield slug, a + 1, " ".join(x.strip() for x in threads[a:b]), threads[a:b]


def main():
    print(f"\nLoading {LOG_PATH.relative_to(ROOT)} "
          f"and {THREADS_PATH.relative_to(ROOT)}...")
    log = read(LOG_PATH)
    threads = read(THREADS_PATH)

    check_frontmatter(log, LOG_PATH)
    check_frontmatter(threads, THREADS_PATH)

    registry = [l.split("`")[1] for l in threads if l.startswith("| `")]
    rosters = list(roster_entries(threads))
    roster_slugs = [slug for slug, _, _, _ in rosters]

    pen_start = next(i for i, l in enumerate(threads)
                     if l.startswith("# Holding pen"))
    pen = set(re.findall(r"^- `([a-z0-9-]+)`",
                         "\n".join(threads[pen_start:]), re.M))
    known = set(registry) | pen

    entry_lines = [i for i, l in enumerate(log) if l.startswith("### ")]
    first = entry_lines[0]

    print(f"Checking {len(entry_lines)} log entries "
          f"and {len(roster_slugs)} thread rosters...\n")

    # ── Registry and roster ordering ─────────────────────────────────────────
    registry_lines = [i + 1 for i, l in enumerate(threads)
                      if l.startswith("| `")]
    for (a, la), (b, lb) in zip(zip(registry, registry_lines),
                                zip(registry[1:], registry_lines[1:])):
        if b < a:
            errors.append(f"chains-threads line {lb}: registry out of "
                          f"alphabetical order, `{a}` then `{b}`")
            break
    roster_lines = [ln for _, ln, _, _ in rosters]
    for (a, la), (b, lb) in zip(zip(roster_slugs, roster_lines),
                                zip(roster_slugs[1:], roster_lines[1:])):
        if b < a:
            errors.append(f"chains-threads line {lb}: rosters out of "
                          f"alphabetical order, `{a}` then `{b}`")
            break
    for slug, lineno, _, _ in rosters:
        if slug not in set(registry):
            errors.append(f"chains-threads line {lineno}: roster `{slug}` has "
                          "no row in the registry table")

    # ── Every slug used in the log is known ──────────────────────────────────
    for i, line in enumerate(log):
        m = re.match(r"^- (?:NOTE \([^)]*?, )?`([a-z0-9-]+)`", line)
        if m and m.group(1) not in known:
            errors.append(f"chains-log line {i+1}: `{m.group(1)}` is in "
                          "neither the registry nor the holding pen")

    # ── One record per line ──────────────────────────────────────────────────
    for i, line in enumerate(log):
        if i > first and line.startswith("  ") and line.strip():
            errors.append(f"chains-log line {i+1}: continuation line; each "
                          "record must be a single line")

    # ── Entry order and uniqueness ───────────────────────────────────────────
    seen, prev = {}, None
    for i in entry_lines:
        mid = ENTRY.match(log[i]).group(1)
        if mid in seen:
            errors.append(f"chains-log line {i+1}: duplicate entry for {mid} "
                          f"(first at line {seen[mid]})")
        elif prev and mid[:10] < prev[0]:
            errors.append(f"chains-log line {i+1}: {mid} is out of order, it "
                          f"follows {prev[1]} at line {prev[2]}")
        seen[mid] = i + 1
        prev = (mid[:10], mid, i + 1)

    # ── Role line format and vocabulary ──────────────────────────────────────
    # Any record opening with a backticked slug is a role line and must be well
    # formed; losing the bold markers must not slip through unnoticed.
    for i, line in enumerate(log):
        if line.startswith("- `"):
            m = ROLE_LINE.match(line)
            if not m:
                errors.append(f"chains-log line {i+1}: role line does not "
                              "match '- `slug` **[Role]** : '")
            elif m.group(2) not in ROLES:
                errors.append(f"chains-log line {i+1}: '{m.group(2)}' is not "
                              "in the link-role vocabulary")

    # ── Debt ─────────────────────────────────────────────────────────────────
    registry_row = dict(zip(registry, registry_lines))
    for slug in sorted(set(registry) - set(roster_slugs)):
        debt["minted_without_roster"].append(
            f"chains-threads line {registry_row[slug]}: `{slug}` is minted "
            "but has no roster entry")

    for i, line in enumerate(log):
        if i <= first or not line.startswith("- "):
            continue
        if not RECORD.match(line):
            debt["records_without_tier"].append(
                f"chains-log line {i+1}: record has no tier")
        elif NOTE_LINE.match(line) and not line.startswith("- NOTE ("):
            debt["records_without_tier"].append(
                f"chains-log line {i+1}: NOTE has no tier")

    for i, line in enumerate(log):
        if not RECORD.match(line):
            continue
        found = SESSION_DATE.search(line)
        if found:
            debt["log_datestamps"].append(
                f"chains-log line {i+1}: {found.group(0)}")
        m = re.match(r"^- NOTE \(([^)]*)\)", line)
        if m and PEN_WORD.search(m.group(1)):
            minted_here = [s for s in re.findall(r"`([a-z0-9-]+)`", m.group(1))
                           if s in set(registry)]
            if minted_here:
                debt["stale_pen_notes"].append(
                    f"chains-log line {i+1}: pen note on minted "
                    f"`{minted_here[0]}`")

    for slug, lineno, text, body in rosters:
        for offset, raw in enumerate(body):
            for m in SESSION_DATE.finditer(raw):
                debt["roster_datestamps"].append(
                    f"chains-threads line {lineno + offset}: {slug}, "
                    f"{m.group(0)}")
        # Every count is reported as a candidate. Some are back-references to a
        # list named on the spot and are fine; those are triaged by hand.
        # Deliberately no cleverness: a heuristic that guesses which counts are
        # safe will hide real ones.
        norm = MSG_ID.sub("@ID@", text)
        norm = re.sub(r"\b\d{4}-\d{2}(-\d{2})?\b", "@", norm)
        for m in COUNT.finditer(norm):
            debt["roster_counts"].append(
                f"chains-threads line {lineno}: {slug}, \"{m.group(0)}\"")
        for m in SPAN.finditer(text):
            if SPAN_OK.search(text[m.end():m.end() + 60]):
                continue
            debt["roster_spans"].append(
                f"chains-threads line {lineno}: {slug}, "
                f"\"{text[m.start():m.start()+45].strip()}...\"")

    # ── Report ───────────────────────────────────────────────────────────────
    failed = False

    if errors:
        failed = True
        for e in errors:
            print(f"    {RED}ERROR{RESET}   {e}")
        print()

    print("─" * 60)
    print("CHAINS DEBT LEDGER")
    print("  fails only if a count rises above its recorded baseline\n")
    for key, found in debt.items():
        n, base = len(found), BASELINE[key]
        if n > base:
            failed = True
            label = f"{RED}OVER{RESET} "
        elif n < base:
            label = f"{GREEN}DOWN{RESET} "
        else:
            label = "     "
        print(f"  {label} {n:4d} / {base:<4d} {key}")
        if n > base:
            for item in found[:12]:
                print(f"            {item}")
            if len(found) > 12:
                print(f"            ... and {len(found) - 12} more")
        elif n < base:
            print(f"            cleared {base - n}; set "
                  f"BASELINE['{key}'] = {n}")
    print()

    # ── Summary ──────────────────────────────────────────────────────────────
    print("─" * 60)
    if not failed:
        print(f"{GREEN}✅ Chains layer passed validation with no issues.{RESET}\n")
        sys.exit(0)
    if errors:
        print(f"{RED}Errors: {len(errors)}{RESET}")
    print(f"{RED}❌ Validation failed. Please fix before committing.{RESET}\n")
    sys.exit(1)


if __name__ == "__main__":
    main()