# Retired one-time scripts

The scripts in this folder are not part of the normal work. Each was written to make one change across the archive when the `door` field was added to the message files, was run once, and is kept here only as a record of what was done.

| Script | What it did |
|---|---|
| `insert_doors.py` | Copied each message's door from a table in `content/doors.md` into the message's front matter. That table no longer exists |
| `fix_door_block_scalar.py` | Rewrote each door field in the block form the other long fields use (`door: >`) |
| `fix_door_ellipsis.py` | Removed stray `...` marker lines that had been inserted into front matter |
| `fix_door_spaces.py` | Removed doubled spaces in door fields caused by line wrapping |

Do not run them. The scripts in use are in `.github/scripts/`, and `MAINTAINERS-GUIDE.md` at the top of the repository explains each one.
