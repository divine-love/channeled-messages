#!/usr/bin/env python3
"""
validate_chains.py
Validates the chains layer against the conventions declared in the design
blocks of metadata/chains-log.md and metadata/chains-threads.md.

The layer is kept in split files, read through chains_io.py:

  metadata/chains-log.md            the log's rules, no entries
  metadata/chains-log/YEAR.md       the entries, by year of message
  metadata/chains-threads.md        design, registry, holding pen, patterns,
                                    open questions; no rosters
  metadata/chains-threads/SLUG.md   one roster per minted thread

The checks run on the joined text, so they are the same checks as when each
was a single file. Every message names the file and line to correct.

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
          - chains-log.md and chains-threads.md carry an ISO last_updated
            in front matter
          - every entry sits in the file for its own year, and an entry file
            holds entries and nothing else
          - every roster file is named for its slug and holds that one roster
          - no entries or rosters left in chains-log.md or chains-threads.md,
            and no stray files in either folder

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

# chains_io.py sits beside this script and reads the split files.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import chains_io  # noqa: E402

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = chains_io.ROOT
LOG_PATH = chains_io.LOG_DOOR
THREADS_PATH = chains_io.THREADS_DOOR

# ── Colours for terminal output ───────────────────────────────────────────────
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

# ── Debt baselines ────────────────────────────────────────────────────────────
# Lower these as the work is done. Never raise one to make a build pass.
BASELINE = {
    "minted_without_roster": 0,   # threads awaiting a roster entry
    "records_without_tier": 0,    # bare '- NOTE:' and bare '- (' records
    "roster_datestamps": 0,       # session dates inside roster entries
    "log_datestamps": 0,          # session dates inside log records
    "log_in_hand": 0,             # rank or sufficiency claims scoped by "in hand"
    "roster_counts": 0,           # size claims about what a thread holds
    "roster_spans": 0,            # year spans and archive-extremum claims
    "roster_role_intervals": 0,   # intervals measured against a floating role
    "roster_in_hand": 0,          # rank or sufficiency claims scoped by "in hand"
}

# ── Controlled vocabulary, per the design blocks in both files ───────────────
ROLES = {
    "Foundation", "Elaboration", "Objection-removed", "Reframe",
    "Testimony", "Chrysalis", "Capstone",
}

ROLE_LINE = re.compile(r"^- `([a-z0-9-]+)` \*\*\[([\w-]+)\]\*\* : ")
NOTE_LINE = re.compile(r"^- NOTE\b")
# The closed NOTE vocabulary, per the chains-log design block.
NOTE_OK = re.compile(
    r"^- NOTE \((?:context|pattern, described and not penned"
    r"|(?:witness|sighting|considered and set aside|build), `[a-z0-9-]+`)\): ")
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

# An interval measured against a role label breaks when the role moves, and roles
# stay provisional until a chain is built. "Three weeks before the Foundation" is
# a fact about one fixed date and one floating label. Naming the other message
# instead is stable, because the message_id carries its own date.
ROLE_INTERVAL = re.compile(
    r"\b(?:" + NUMBER + r")\s+(?:years?|months?|weeks?|days?)\s+"
    r"(?:before|after|later|earlier|apart)\b"
    r"(?=.{0,70}?\b(?:Foundation|Elaborations?|Objections?[- ]removed|Reframe"
    r"|Testimony|Chrysalis|Capstone|anchor)\b)"
    r"|\b(?:predates|postdates|precedes|follows)\s+(?:the\s+)?(?:first\s+)?"
    r"(?:Foundation|Elaborations?|Objections?[- ]removed|Reframe|Testimony"
    r"|Chrysalis|Capstone|anchor)\s+by\s+(?:" + NUMBER + r")\s+"
    r"(?:years?|months?|weeks?|days?)\b", re.I)

# "in hand" scopes a claim to what has been read so far. It still ranks or sizes
# messages against a set that keeps growing, and roles stay provisional until
# build, so it is counted rather than exempted.
IN_HAND = re.compile(r"\bin\s+hand\b", re.I)

errors = []
debt = {key: [] for key in BASELINE}


def require(path):
    if not path.exists():
        print(f"{RED}Could not find {path}{RESET}")
        sys.exit(1)


FULL_ID = re.compile(r"\d{4}-\d{2}-\d{2}-[a-z]{2}-[a-z0-9-]+")


def check_layout():
    """The split itself: every entry and roster is in the file it belongs in."""
    # chains-log.md holds the rules only.
    for n, line in enumerate(chains_io.read_lines(LOG_PATH), 1):
        m = ENTRY.match(line)
        if (m and FULL_ID.fullmatch(m.group(1))) or RECORD.match(line):
            errors.append(
                f"chains-log.md line {n}: entries belong in the file for "
                "their year under metadata/chains-log/, not in chains-log.md")
            break

    # Entry files: named for a year (or a year and month), entries only,
    # each entry in the file its message_id names.
    stems = []
    for path in chains_io.log_files():
        name, stem = chains_io.label(path), path.stem
        if not re.fullmatch(r"\d{4}(-\d{2})?", stem):
            errors.append(f"{name}: an entry file is named for its year, as "
                          "2016.md, or for a year and month, as 2026-01.md")
            continue
        stems.append(stem)
        lines = chains_io.read_lines(path)
        if not lines:
            errors.append(f"{name}: empty entry file")
            continue
        if not lines[0].startswith("### "):
            errors.append(f"{name} line 1: an entry file opens with its first "
                          "entry heading and holds nothing but entries")
        for n, line in enumerate(lines, 1):
            if not line.strip() or line.startswith("  "):
                continue        # blank separators; continuation lines are
                                # reported by the one-record-per-line check
            m = ENTRY.match(line)
            if line.startswith("### "):
                mid = m.group(1) if m else ""
                if not FULL_ID.fullmatch(mid):
                    errors.append(f"{name} line {n}: heading does not open "
                                  "with a message_id")
                elif not mid.startswith(stem):
                    errors.append(
                        f"{name} line {n}: {mid} belongs in "
                        f"chains-log/{mid[:len(stem)]}.md")
            elif not line.startswith("- "):
                errors.append(f"{name} line {n}: not an entry heading or a "
                              "record; an entry file holds entries only")
    for year in sorted({s[:4] for s in stems}):
        if year in stems and any(s.startswith(year + "-") for s in stems):
            errors.append(
                f"chains-log/{year}.md: {year} has both a year file and month "
                "files; move its entries into the month files")

    # Roster files: named for the slug, one roster each, in the roster shape.
    for path in chains_io.roster_files():
        name, stem = chains_io.label(path), path.stem
        lines = chains_io.read_lines(path)
        if len(lines) < 3 or lines[0] != f"### {stem}" or lines[1] != "" \
                or not lines[2].startswith(f"- `{stem}`:"):
            errors.append(
                f"{name}: a roster file opens with '### {stem}', a blank "
                f"line, then '- `{stem}`: ...'; the file name must be the "
                "slug")
            continue
        for n, line in enumerate(lines[3:], 4):
            if not line.strip():
                errors.append(f"{name} line {n}: blank line inside the "
                              "roster; it is one indented block")
            elif not line.startswith("  "):
                errors.append(f"{name} line {n}: a roster file holds one "
                              "roster, every line after the first indented "
                              "two spaces")
                break

    # chains-threads.md holds no rosters, and keeps the two headings the
    # rosters are read in between.
    door = chains_io.read_lines(THREADS_PATH)
    start = next((i for i, l in enumerate(door)
                  if l.startswith("## Thread rosters")), None)
    end = next((i for i, l in enumerate(door)
                if l.startswith(chains_io.PEN_HEADING)), None)
    if start is None or end is None or end < start:
        print(f"{RED}chains-threads.md must keep its '## Thread rosters' "
              f"heading, with '{chains_io.PEN_HEADING}' after it.{RESET}")
        sys.exit(1)
    for i in range(start + 1, end):
        if door[i].startswith("### ") or door[i].startswith("- `"):
            errors.append(
                f"chains-threads.md line {i + 1}: rosters belong in their own "
                "files under metadata/chains-threads/, not in "
                "chains-threads.md")
            break

    # Nothing else lives in either folder.
    for folder in (chains_io.LOG_DIR, chains_io.THREADS_DIR):
        if not folder.is_dir():
            print(f"{RED}Could not find {folder}{RESET}")
            sys.exit(1)
        for path in sorted(folder.iterdir()):
            if path.name.startswith("."):
                continue
            if path.is_dir() or path.suffix != ".md":
                errors.append(f"{chains_io.label(path)}: only .md files "
                              "belong in this folder")


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
    require(LOG_PATH)
    require(THREADS_PATH)
    print(f"\nLoading {LOG_PATH.relative_to(ROOT)} with "
          f"{len(chains_io.log_files())} entry file(s) and "
          f"{THREADS_PATH.relative_to(ROOT)} with "
          f"{len(chains_io.roster_files())} roster file(s)...")
    check_layout()
    logt = chains_io.load_log()
    thrt = chains_io.load_threads()
    log, threads = logt.lines, thrt.lines

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
            errors.append(f"{thrt.where(lb - 1)}: registry out of "
                          f"alphabetical order, `{a}` then `{b}`")
            break
    roster_lines = [ln for _, ln, _, _ in rosters]
    for (a, la), (b, lb) in zip(zip(roster_slugs, roster_lines),
                                zip(roster_slugs[1:], roster_lines[1:])):
        if b < a:
            errors.append(f"{thrt.where(lb - 1)}: rosters out of "
                          f"alphabetical order, `{a}` then `{b}`")
            break
    for slug, lineno, _, _ in rosters:
        if slug not in set(registry):
            errors.append(f"{thrt.where(lineno - 1)}: roster `{slug}` has "
                          "no row in the registry table")

    # ── Every slug used in the log is known ──────────────────────────────────
    for i, line in enumerate(log):
        m = re.match(r"^- (?:NOTE \([^)]*?, )?`([a-z0-9-]+)`", line)
        if m and m.group(1) not in known:
            errors.append(f"{logt.where(i)}: `{m.group(1)}` is in "
                          "neither the registry nor the holding pen")

    # ── One record per line ──────────────────────────────────────────────────
    for i, line in enumerate(log):
        if i > first and line.startswith("  ") and line.strip():
            errors.append(f"{logt.where(i)}: continuation line; each "
                          "record must be a single line")

    # ── Entry order and uniqueness ───────────────────────────────────────────
    seen, prev = {}, None
    for i in entry_lines:
        mid = ENTRY.match(log[i]).group(1)
        if mid in seen:
            errors.append(f"{logt.where(i)}: duplicate entry for {mid} "
                          f"(first at {seen[mid]})")
        elif prev and mid[:10] < prev[0]:
            errors.append(f"{logt.where(i)}: {mid} is out of order, it "
                          f"follows {prev[1]} at {prev[2]}")
        seen[mid] = logt.where(i)
        prev = (mid[:10], mid, logt.where(i))

    # ── Role line format and vocabulary ──────────────────────────────────────
    # Any record opening with a backticked slug is a role line and must be well
    # formed; losing the bold markers must not slip through unnoticed.
    for i, line in enumerate(log):
        if line.startswith("- `"):
            m = ROLE_LINE.match(line)
            if not m:
                errors.append(f"{logt.where(i)}: role line does not "
                              "match '- `slug` **[Role]** : '")
            elif m.group(2) not in ROLES:
                errors.append(f"{logt.where(i)}: '{m.group(2)}' is not "
                              "in the link-role vocabulary")

    # ── NOTE vocabulary ──────────────────────────────────────────────────────
    for i, line in enumerate(log):
        if i > first and line.startswith("- NOTE (") and not NOTE_OK.match(line):
            m = re.match(r"^- NOTE \(([^)]*)\)", line)
            inner = m.group(1) if m else line[:30]
            head = inner.split(",")[0].strip()
            if head in ("witness", "sighting", "considered and set aside", "build"):
                why = ("needs exactly one slug and nothing after it, as in "
                       f"'{head}, `slug`'")
            else:
                why = ("is not one of witness, sighting, considered and set "
                       "aside, build (each with a slug), pattern, or context")
            errors.append(f"{logt.where(i)}: NOTE ({inner}) {why}")

    # ── Debt ─────────────────────────────────────────────────────────────────
    registry_row = dict(zip(registry, registry_lines))
    for slug in sorted(set(registry) - set(roster_slugs)):
        debt["minted_without_roster"].append(
            f"{thrt.where(registry_row[slug] - 1)}: `{slug}` is minted "
            f"but has no roster file, chains-threads/{slug}.md")

    for i, line in enumerate(log):
        if i <= first or not line.startswith("- "):
            continue
        if not RECORD.match(line):
            debt["records_without_tier"].append(
                f"{logt.where(i)}: record has no tier")
        elif NOTE_LINE.match(line) and not line.startswith("- NOTE ("):
            debt["records_without_tier"].append(
                f"{logt.where(i)}: NOTE has no tier")

    for i, line in enumerate(log):
        if not RECORD.match(line):
            continue
        found = SESSION_DATE.search(line)
        if found:
            debt["log_datestamps"].append(
                f"{logt.where(i)}: {found.group(0)}")
        for m in IN_HAND.finditer(line):
            debt["log_in_hand"].append(
                f"{logt.where(i)}: "
                f"\"...{line[max(0, m.start()-40):m.end()].strip()}\"")

    for slug, lineno, text, body in rosters:
        for offset, raw in enumerate(body):
            for m in SESSION_DATE.finditer(raw):
                debt["roster_datestamps"].append(
                    f"{thrt.where(lineno - 1 + offset)}: {slug}, "
                    f"{m.group(0)}")
        # Every count is reported as a candidate. Some are back-references to a
        # list named on the spot and are fine; those are triaged by hand.
        # Deliberately no cleverness: a heuristic that guesses which counts are
        # safe will hide real ones.
        norm = MSG_ID.sub("@ID@", text)
        norm = re.sub(r"\b\d{4}-\d{2}(-\d{2})?\b", "@", norm)
        for m in COUNT.finditer(norm):
            debt["roster_counts"].append(
                f"{thrt.where(lineno - 1)}: {slug}, \"{m.group(0)}\"")
        for m in ROLE_INTERVAL.finditer(text):
            debt["roster_role_intervals"].append(
                f"{thrt.where(lineno - 1)}: {slug}, "
                f"\"{text[m.start():m.start()+55].strip()}...\"")
        # Scanned on the joined text: the phrase often wraps across a line break.
        for m in IN_HAND.finditer(text):
            debt["roster_in_hand"].append(
                f"{thrt.where(lineno - 1)}: {slug}, "
                f"\"...{text[max(0, m.start()-40):m.end()].strip()}\"")
        for m in SPAN.finditer(text):
            debt["roster_spans"].append(
                f"{thrt.where(lineno - 1)}: {slug}, "
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