# Validation

This repository checks itself. Every time someone pushes a change, GitHub runs a set of checks, so a file that breaks a rule is caught before it reaches readers.

For how the checks fit into the rest of the work, see [`MAINTAINERS-GUIDE.md`](../MAINTAINERS-GUIDE.md).

---

## What runs, and when

| Check | Script | Runs on GitHub when you change |
|---|---|---|
| Message files | `.github/scripts/validate_messages.py` | a message, a practice, a spirit or medium file, `subjects.yml`, `collections.yml`, `law-mentions-reviewed.yml`, the schema, or a script |
| Spirit-given prayer files | `.github/scripts/validate_prayers.py` | the same |
| The chains layer | `.github/scripts/validate_chains.py` | `chains-log.md`, `chains-threads.md`, or any file in the `chains-log/` and `chains-threads/` folders |

After the message and prayer checks pass, GitHub also rebuilds the browse page, `llms.txt`, the collection pages and the essential-teaching pages, and saves them to the repository.

---

## What the message check looks for

Each message is a Markdown file (`.md`) with a block of catalogue fields at the top. The check reads that block.

### Against the schema (`schema/message.schema.yml`)

- The required fields are present: `message_id`, `title`, `date`, `spirit_id`, `medium`, `message_type`, `primary_subjects`
- Each field holds the right kind of value
- `message_id` and `spirit_id` are lowercase words joined by hyphens, in the pattern set out in `schema.md`, section 2
- `message_type` is exactly one of `Blessing`, `Guidance`, `Teaching`
- `description` is no longer than 600 characters
- `secondary_subjects` has no more than 5 entries
- `excerpt` and `door` are each no longer than 300 characters
- `essential_teachings` and `collections` use only the names the schema lists
- `date` and `last_edited` are real dates, written `YYYY-MM-DD`

### Against the rest of the archive

- `message_id` matches the name of its file
- `spirit_id`, and every entry in `spirits`, has a file in `/spirits/`
- Every entry in `related_messages` is a message that exists
- Every subject is defined in `metadata/subjects.yml`, spelled exactly as it is there
- `subjects.yml` has no name listed twice
- The collection rules in `metadata/collections.yml` hold: a spirit a collection requires carries it, and a spirit a collection excludes does not

### Warnings

A warning does not fail the check. It asks for a second look.

- The `medium` has no file in `/mediums/`
- The `title` is not wrapped in quotation marks
- The message names a spiritual Law, but that Law is not among its subjects or keywords and the message is not listed in `metadata/law-mentions-reviewed.yml`

The check ends with a count of how many messages use each subject.

---

## What the prayer check looks for

A prayer file is any file in `content/practices/` named `prayer-` followed by a `message_id`. The check confirms that:

- its fields match `content/templates/prayer-template.md`
- it points to a real message, by the right spirit, medium and date
- its subjects exist and its description is within 600 characters
- the prayer's words appear in the source message exactly. Words in [square brackets] are the curator's additions and are set aside before comparing

---

## What the chains check looks for

- Every thread name used in the log exists in `metadata/chains-threads.md`
- Entries are in date order, and each is in the file for its own year
- Every roster file is named for its thread and holds that one roster
- Every thread in the list has a roster file
- The record format the log's own rules set out

The opening of `validate_chains.py` lists every check.

---

## Reading the results

| Result | Meaning |
|---|---|
| ✅ Passed | Nothing to fix |
| ❌ ERROR | A rule was broken. It must be fixed |
| ⚠️ WARNING | Worth a look. It does not fail the check |

On GitHub, a green tick beside a commit means the checks passed, and a red X means one failed. To see why:

1. Open the repository on GitHub
2. Click the red X beside the commit
3. Click **Details** to read the report. It names the file and the rule
4. Fix the file, commit, and push again. The checks run again by themselves

---

## Running the checks on your own computer

Running them before you push catches problems early.

### First time only

Install Python 3, then run this once in PowerShell (or any terminal):

```
pip install pyyaml jsonschema
```

### Each time

From the top folder of the repository:

```
python .github/scripts/validate_messages.py
python .github/scripts/validate_prayers.py
python .github/scripts/validate_chains.py
```

---

## Where things are

| File | Purpose |
|---|---|
| `.github/workflows/validate-messages.yml` | Tells GitHub when to check messages and prayers and rebuild the index pages |
| `.github/workflows/validate-chains.yml` | Tells GitHub when to check the chains layer |
| `.github/scripts/` | The check scripts themselves |
| `schema/message.schema.yml` | The limits every message file must keep |
| `schema/schema.md` | Every field and rule, explained |

---

## Questions?

If you are not sure why a file is failing, `schema/schema.md` explains every field and its rules.
