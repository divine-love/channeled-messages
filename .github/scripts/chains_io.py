#!/usr/bin/env python3
"""
chains_io.py
Reads the chains layer from its split layout and hands it to
validate_chains.py and generate_vault.py as continuous text.

This is a helper, not a script to run. The other two scripts load it
themselves. Stdlib only.

The layout it reads:

  metadata/chains-log.md            the log's design block and rules, no entries
  metadata/chains-log/2016.md       the entries, one file per year of message
  metadata/chains-log/2026-01.md    (a heavy year may be divided by month)

  metadata/chains-threads.md        design notes, registry, holding pen,
                                    patterns, open questions; no rosters
  metadata/chains-threads/SLUG.md   one roster per minted thread, named by slug

Both loaders return a Text: the lines in reading order, exactly as they stood
when each was a single file, plus a record of which file and line every line
came from. The checks and the vault generator therefore work on the same
continuous text as before the split, and can still point at the exact place
to make a correction.

Reading order is by file name. For the log that is chronological (2016.md
before 2017.md, 2026-01.md before 2026-02.md); for the rosters it is
alphabetical by slug, the same order as the registry table.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
METADATA = ROOT / "metadata"
LOG_DOOR = METADATA / "chains-log.md"
LOG_DIR = METADATA / "chains-log"
THREADS_DOOR = METADATA / "chains-threads.md"
THREADS_DIR = METADATA / "chains-threads"

# The rosters are read into chains-threads.md just above this heading, which
# is where they sat when the file was whole.
PEN_HEADING = "# Holding pen"


class Text:
    """Lines in reading order, each remembering the file and line it came from."""

    def __init__(self):
        self.lines = []
        self.origins = []       # (label, 1-based line number) or None for a join

    def add(self, lines, label):
        for number, line in enumerate(lines, 1):
            self.lines.append(line)
            self.origins.append((label, number))

    def gap(self):
        """The blank line that separates one file's content from the next."""
        self.lines.append("")
        self.origins.append(None)

    def _origin(self, index):
        index = max(0, min(index, len(self.origins) - 1))
        while index > 0 and self.origins[index] is None:
            index -= 1
        return self.origins[index] or ("chains", 0)

    def where(self, index):
        """'chains-log/2018.md line 142' for the 0-based index given."""
        label, number = self._origin(index)
        return f"{label} line {number}"

    def ref(self, index):
        """('2018.md', 142) for the 0-based index given: a short pointer."""
        label, number = self._origin(index)
        return (label.split("/")[-1], number)

    def file_of(self, index):
        """The label of the file the 0-based index came from."""
        return self._origin(index)[0]


def read_lines(path):
    """A file's lines, with Windows line endings and trailing blanks removed."""
    lines = path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def label(path):
    """A path as written in messages: relative to metadata/, forward slashes."""
    return path.relative_to(METADATA).as_posix()


def log_files():
    """The log's entry files, in reading order."""
    if not LOG_DIR.is_dir():
        return []
    return sorted(LOG_DIR.glob("*.md"), key=lambda p: p.stem)


def roster_files():
    """The roster files, in reading order."""
    if not THREADS_DIR.is_dir():
        return []
    return sorted(THREADS_DIR.glob("*.md"), key=lambda p: p.stem)


def load_log():
    """chains-log.md followed by every entry file, as one Text."""
    text = Text()
    if LOG_DOOR.exists():
        text.add(read_lines(LOG_DOOR), label(LOG_DOOR))
    for path in log_files():
        if text.lines:
            text.gap()
        text.add(read_lines(path), label(path))
    return text


def load_threads():
    """chains-threads.md with every roster read in above the holding pen."""
    text = Text()
    if not THREADS_DOOR.exists():
        return text
    door = read_lines(THREADS_DOOR)
    name = label(THREADS_DOOR)
    pen = next((i for i, line in enumerate(door)
                if line.startswith(PEN_HEADING)), len(door))
    head, tail = door[:pen], door[pen:]
    for number, line in enumerate(head, 1):
        text.lines.append(line)
        text.origins.append((name, number))
    for path in roster_files():
        text.add(read_lines(path), label(path))
        text.gap()
    for number, line in enumerate(tail, pen + 1):
        text.lines.append(line)
        text.origins.append((name, number))
    return text
