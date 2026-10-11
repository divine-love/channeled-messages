---
# === Spirit-Given Prayer (TEMPLATE) ===

practice_id: prayer-2025-01-01-af-spirit-id   # REQUIRED. Always the filename without .md.

title: "Words from the Prayer"         # REQUIRED. In double quotes. Taken from the prayer's own words, e.g. "Father, I Need You".

type: prayer                           # REQUIRED. Always "prayer".

source_message: 2025-01-01-af-spirit-id   # REQUIRED. The message_id of the message the prayer comes from.

spirit_id: spirit-id                   # REQUIRED. The spirit who gives the prayer. Must have a file in spirits/ and be the message's spirit_id or one of its spirits[].

spirit_name: "Spirit Name"             # REQUIRED. As written in the spirit file, e.g. "John the Beloved".

medium: Firstname Lastname             # REQUIRED. Same as the source message, e.g. Al Fike.

date_received: 2025-01-01              # REQUIRED. Same as the source message's date (YYYY-MM-DD).

primary_subjects: "Main Subject"       # REQUIRED. Exactly one subject from metadata/subjects.yml.

secondary_subjects:                    # OPTIONAL. Up to five subjects from metadata/subjects.yml.
  - "Prayer & Devotion"
  - "Teaching the Prayer Practice"

description: >                         # REQUIRED. 600 characters at most. No em dashes.
  A [kind of] prayer given by [spirit] within the message "[message title]".
  Offered as the words by which a soul [what the prayer does].

language: en                           # REQUIRED. Language code, "en" for English.

notes: >                               # OPTIONAL. Plain-language context. No em dashes.
  Appears in the source message in italics, introduced with "[the words just
  before the prayer]". Given in the context of [what the spirit is teaching].
  [Any punctuation supplied, or words added in square brackets, and why.]

last_edited: 2025-01-01                # Today's date whenever this file is changed (YYYY-MM-DD).
---
The prayer text goes here, exactly as it appears in the message, without the italics and quotation marks that surround it there. A final full stop may be supplied if the prayer ends mid-sentence in the message. Any other words the curator adds go in [square brackets].

---
*Given by Spirit Name through Firstname Lastname, January 1, 2025. The full message is at [2025-01-01-af-spirit-id](../messages/2025/01/2025-01-01-af-spirit-id.md).*
