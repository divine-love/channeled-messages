# Message Validation

This repository uses an automated validator to ensure all message files are correctly formatted before they are accepted into the archive.

---

## How It Works

Every time a contributor pushes a commit or opens a pull request that includes changes to files in `/content/messages/`, `/spirits/`, or `/mediums/`, GitHub automatically runs a validation check. If any files contain errors, the check will fail and the contributor will be notified.

The validator checks each message `.yml` file against the rules defined in `schema/message.schema.yml` and performs additional cross-reference checks.

---

## What Gets Checked

### Schema validation
- All required fields are present (`message_id`, `title`, `date`, `spirit_id`, `medium`, `message_type`, `primary_subjects`)
- All field values match their expected types and formats
- `message_id` and `spirit_id` match the required lowercase kebab-case pattern
- `message_type` contains only valid values (`Blessing`, `Guidance`, `Teaching`)
- `description` is between 1 and 600 characters
- `secondary_subjects` contains no more than 3 entries
- `audio_url` and `canonical_url` are valid URLs if provided
- `date` and `last_edited` are valid ISO dates (YYYY-MM-DD)

### Cross-reference checks
- `spirit_id` matches an existing file in `/spirits/`
- Each entry in `spirits` matches an existing file in `/spirits/`
- Each entry in `related_messages` matches an existing `message_id` in the archive
- `message_id` matches the filename of the file

### Additional checks
- `message_id` is fully lowercase

---

## Understanding the Results

When validation runs, each file is checked and results are reported as:

| Result | Meaning |
|--------|---------|
| ✅ Passed | No issues found |
| ❌ ERROR | A required rule was violated — must be fixed before the commit is accepted |
| ⚠️ WARNING | A potential issue worth reviewing — does not block the commit |

---

## Fixing Errors

If your commit fails validation, GitHub will show a red ✗ next to your commit. To see what went wrong:

1. Go to your repository on GitHub
2. Click on the failed check (red ✗) next to your commit
3. Click **Details** to see the full error output
4. Fix the errors in your files in VSCode
5. Commit and push again — the validator will run automatically

---

## Running Validation Locally

You can also run the validator on your own computer before pushing, to catch errors early.

### First time setup
Open Terminal and run:
```bash
pip install pyyaml jsonschema
```

### Run the validator
From your repository's root folder in Terminal:
```bash
python .github/scripts/validate_messages.py
```

---

## File Locations

| File | Purpose |
|------|---------|
| `.github/workflows/validate-messages.yml` | GitHub Actions workflow — triggers the validator automatically |
| `.github/scripts/validate_messages.py` | The validation script itself |
| `schema/message.schema.yml` | The schema rules all message files must follow |

---

## Questions?

If you're unsure why a file is failing validation, refer to the `schema/schema.md` file for a full explanation of every field and its requirements, or reach out to the project curator.