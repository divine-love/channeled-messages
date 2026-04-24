# Divine Love Messages Schema & Contribution Guide 

This document defines the metadata standard for cataloguing the Divine Love Messages collection.
All contributors should follow these conventions to ensure consistency, searchability, and compatibility across future platforms.

This document complements the machine-readable file [`message.schema.yml`](./message.schema.yml), which enforces structure through automated validation.

---


## 1. File layout & naming

Each message is stored in its own `.yml` file within a structured directory tree:

```
├─ content/
│  └─ messages/
│     └─ 2015/
│        └─ 11/
│           └─ 2015-11-30-af-jesus.md
│        └─ 12/
│           └─ 2015-12-07-af-andrew.md
│     └─ 2016/
│        └─ 01/
│           └─ 2016-01-03-af-augustine.md
│  └─ books/
│     └─ judas-of-kerioth.md
│     └─ book-template.md
│  └─ practices/
│     └─ healing-merkaba.md
│     └─ prayer-for-divine-love-original.md
│     └─ prayer-for-divine-love-padgett-contemporary.md
│     └─ prayer-for-divine-love-dlsf.md
│  └─ templates/
│     └─ medium-template.yml
│     └─ message-template.yml
│     └─ spirit-template.yml
│  └─ doors.md
├─ mediums/
│  └─ al-fike.yml
├─ metadata/
│  └─ subjects.yml
│  └─ theme_clusters.yml
├─ schema/
│  └─ message.schema.yml
│  └─ schema.md
├─ spirits/
│  └─ andrew.yml
│  └─ augustine.yml
│  └─ jesus.yml
```

 - `/content/messages/` contains all message entries organized by year, as Markdown files (`.md`) with YAML front matter.
 - `/content/books/` contains recommended reading entries — books and resources relevant to the Divine Love archive.
 - `/content/doors.md` — a curated index of the spiritual insight (the "door") hidden within each message, linking to the full text.
 - `/content/templates/` contains template files for messages, spirits, and mediums.
 - `/spirits/` and `/mediums/` store background metadata about spirit authors and mediums.
 - `/metadata/` contains controlled vocabulary files such as `subjects.yml` and `theme_clusters.yml`.
 - `/schema/` contains this documentation and the machine-readable schema definition.


## 2. Message ID Pattern
Each message has a unique id using this format:

### Pattern for message_id:

`YYYY-MM-DD-{medium_initials}-{spirit_id}{-2|-3|...}`

### Rules:

 - `{medium_initials}` = the first letter of the medium's first and last name, **always lowercase**.
   Example: Al Fike → `af`
 - **Anonymous mediums** — when a medium wished to remain unnamed, use `xx` as the medium initials.
   Example: `2015-01-05-xx-jesus`
 - `{spirit_id}` = the spirit's unique identifier, corresponding to the name in the spirit file. Naming pattern is the spirit's full name with **each space replaced by a hyphen (-)**.
   Example: John the Beloved → `john-the-beloved`
 - `spirit_id` is **never capitalized**. It must match the spirit file name exactly. 
 - If more than one message is received by the same spirit and medium on the same day, append `-2`, `-3`, etc. to keep all IDs unique.
 - **Never include spaces** in the ID — use hyphens instead. This ensures compatibility across URLs, filenames, and YAML parsing.
 - **IDs are always lowercase** — including `medium_initials`. Never use uppercase anywhere in an ID.

### Example Message IDs

```yaml
2015-10-12-af-john-the-beloved
2015-11-30-af-jesus
2015-11-30-af-jesus-2
2015-12-01-af-augustine
```

### Filename Example

```yaml
2015-10-12-af-john-the-beloved.yml
```

### YAML Field Example

```yaml
message_id: 2015-10-12-af-john-the-beloved
spirit_id: john-the-beloved
spirit_name: "John the Beloved"
```

---

## 3. Message file format

Each message file is a **Markdown document** with a **YAML front matter** block followed by the **message text**.

```yaml
---
# YAML front matter (metadata)
message_id: 2015-11-30-af-jesus
title: "You Are My Disciples"
date: 2015-11-30
spirit_id: jesus
spirit_name: Jesus
medium: Al Fike
location:
  city: Gibsons
  region: BC        # optional
  country: Canada   # optional
gathering:                             # optional — name of retreat or event, leave blank for regular circles
message_type: ["Teaching", "Guidance"]  # any of: Blessing, Guidance, Teaching; can be multiple
description: >
  A message encouraging disciples to walk confidently in God's light
  and share His Love with the world.
primary_subjects: Divine Love & Relationship with God   # exactly one main subject
secondary_subjects: ["Spiritual Discipline & Daily Living", "Service & Ministry"]  # up to five
people: []          # living humans mentioned (not the medium)
spirits: ["andrew", "augustine"]         # other spirits mentioned besides `spirit`
keywords: ["discipleship", "service", "light", "divine love"]
questions:
  - "How can I serve God's Love in the world?"
  - "What does it mean to be a disciple of Jesus?"
  - "How do I walk in God's Light every day?"
related_messages: ["2015-11-28-af-mary"]
audio_url: https://example.org/audio/2015-11-30-jesus.mp3
canonical_url: https://divinelovesanctuary.com/messages/2015-11-30-jesus
notes: >
  Message received during evening circle in Gibsons, BC.
significance: ["Key Teaching", "Prophetic"]
language: en
excerpt: >
  Oh what wonders your Heavenly Father may manifest through you,
  oh what love will flow.
series: []
last_edited: 2025-06-01
---
<message text here>
```

### Note:
Light formatting (paragraphs, italics, etc.) is fine.
All messages have been read and approved by the medium prior to posting. Please do not paraphrase or edit the teaching content in such a way as to change the meaning (nuanced or otherwise). 


---

## 4. Field-by-Field Reference


| Field | Type | Description | Example |
|-------|------|------------|----------|
| **message_id** | string | Unique identifier formatted `YYYY-MM-DD-{medium_initials}-{spirit_id}{-2\|-3...}`. Braces show the pattern only, do **not** include them in real IDs. `{medium_initials}` are the first and last initials of the medium, always lowercase (e.g., Al Fike → `af`). `{spirit_id}` matches spirit file name (e.g., `john-the-beloved`). If multiple messages share the same date/medium/spirit, append `-2`, `-3`, etc. **IDs are always fully lowercase.** | `2015-11-30-af-jesus-2` |
| **title** | string | The given title of the message. Always wrap in double quotes. If none exists, create one (concise and meaningful) and append an asterisk (*) to show it was added later. | `"You Are My Disciples"` |
| **date** | string (YYYY-MM-DD) | The date the message was received, always using ISO format. | `2015-11-30` |
| **spirit_id** | string | The name of the spirit author chosen from the spirits list (e.g., `john-the-beloved`). Always lowercase; must match the spirit's filename exactly. | `john-the-beloved` |
| **spirit_name** | string | The full name of the spirit author, written in normal capitalization (e.g., "John the Beloved"). | `John the Beloved` |
| **medium** | string | The full name of the human medium who received the message. These initials form the `{medium_initials}` in the ID. | `Al Fike` |
| **location.city** | string | The city or locality where the message was received. | `Gibsons` |
| **location.region** | string | The state, province, or region. Optional; leave blank if not applicable. | `BC` |
| **location.country** | string | The country where the message was received. Optional. | `Canada` |
| **gathering** | string | The name of the retreat, gathering, or event at which the message was received. Leave blank for regular prayer circles. Use a consistent name for all messages from the same event. | `"August 2015 Gibsons Retreat"` |
| **message_type** | array of strings | One or more of: **Blessing, Guidance, Teaching**. Messages may include multiple types. | `["Guidance", "Teaching"]` |
| **description** | string (block scalar) | A short (1–2 sentence) summary describing the purpose or insight of the message. Use YAML block scalar format (`>`) to prevent long lines. | `description: >`<br>`  Encouragement to release fear and trust God's protection.` |
| **primary_subjects** | string | The single most relevant subject drawn from any level of the subject hierarchy — top category or subcategory. Represents the central theme of the message. | `"Free Will & Human Error"` |
| **secondary_subjects** | array of strings (up to 5) | Up to five additional subjects drawn from any level of the subject hierarchy — top category or subcategory. Choose the most relevant subjects regardless of hierarchy level. | `["Divine Will, Guidance & Orchestration", "Earthly Challenges & Human Condition"]` |
| **people** | array of strings | Names of living human beings mentioned (excluding the medium). | `["James Padgett", "Helen Padgett"]` |
| **spirits** | array of strings | `spirit_id` values of other spirits mentioned besides the primary spirit author. Must match filenames in `/spirits/` exactly — always lowercase kebab-case. Using `spirit_id` rather than display names ensures consistent searchability across the archive. | `["john-the-beloved", "mary"]` |
| **keywords** | array of strings | Free-form topical tags or short phrases to improve search and categorization. | `["trust", "peace", "faith", "guidance"]` |
| **questions** | array of strings | Natural language questions this message addresses, written as a seeker might type them into a search engine. Include as many as are relevant — the more specific, the better for discoverability. | `["How does Divine Love change the soul?", "Can any soul be redeemed?"]` |
| **related_messages** | array of strings | Message IDs of other texts connected by subject, author, or event. Use full ID format — **always lowercase**, matching the same convention as `message_id`. | `["2015-11-28-af-mary", "2015-11-26-af-augustine"]` |
| **audio_url** | string (URL) | A direct link to an audio recording of the message (MP3 or stream). Leave blank (`""`) if none. | `https://example.org/audio/2015-11-30-jesus.mp3` |
| **canonical_url** | string (URL) | The permanent public URL where the message is officially published. Used for citation and linking. Leave blank (`""`) if none. | `https://divinelovesanctuary.com/messages/2015-11-30-jesus` |
| **notes** | string | Optional free-text field for contextual notes. Leave blank (`notes: ""`) if none. Use YAML block scalar format (`>`) when content is present. | `notes: ""` or `notes: >`<br>`  Message received during evening circle.` |
| **significance** | array of strings | Optional flags marking a message as particularly important. Values: `Key Teaching`, `Prophetic`, `Historical`, `Healing`, `Biographical`, `Milestone`. Use sparingly. | `["Key Teaching", "Prophetic"]` |
| **language** | string | Language code (ISO 639-1). Always include. Defaults to `en` for English. Required for multilingual site rendering. | `en` |
| **excerpt** | string (block scalar) | A short, punchy pull quote or highlight for social sharing, homepage teasers, and search snippets. May be a direct quote from the message or curator-written. More evocative than `description`. Use YAML block scalar format (`>`) for longer excerpts. | `excerpt: >`<br>`  Drink deep these Living waters and open yourselves wide.` |
| **series** | array of strings | Optional thematic groupings for curated website collections. Leave empty if not yet assigned. | `[]` |
| **last_edited** | string (YYYY-MM-DD) | The date this record was last modified. Helps track which translation files may need updating after source edits. | `2025-06-01` |

---


## 5. Example YAML Files

### Full Example

```yaml
message_id: 2015-11-30-af-jesus
title: "You Are My Disciples"
date: 2015-11-30
spirit_id: jesus
spirit_name: Jesus
medium: Al Fike
location:
  city: Gibsons
  region: BC
  country: Canada
message_type: ["Teaching", "Guidance"]
description: >
  A message encouraging disciples to walk confidently in God's light
  and share His Love with the world.
primary_subjects: "Receiving the Divine Love through Prayer"
secondary_subjects: ["Spiritual Discipline & Daily Living", "Service & Ministry"]
people: []
spirits: ["andrew", "augustine"]
keywords: ["discipleship", "service", "light", "divine love"]
questions:
  - "How can I serve God's Love in the world?"
  - "What does it mean to be a disciple of Jesus?"
  - "How do I walk in God's Light every day?"
related_messages: ["2015-11-28-af-mary"]
audio_url: https://example.org/audio/2015-11-30-jesus.mp3
canonical_url: https://divinelovesanctuary.com/messages/2015-11-30-jesus
notes: >
  Message received during evening circle in Gibsons, BC.
significance: ["Key Teaching"]
language: en
excerpt: >
  Oh what wonders your Heavenly Father may manifest through you,
  oh what love will flow.
series: []
last_edited: 2025-06-01
```

### Minimal Example

```yaml
message_id: 2015-12-07-af-andrew
title: "Be Open To God As A Flower Opens To The Sun"
date: 2015-12-07
spirit_id: andrew
spirit_name: Andrew
medium: Al Fike
location:
  city: Vancouver
  region: BC
  country: Canada
message_type: ["Blessing"]
description: >
  Encouragement to open the soul to God's Love like a flower to the sun.
primary_subjects: "Receiving the Divine Love through Prayer"
secondary_subjects: []
people: []
spirits: []
keywords: ["openness", "prayer", "faith"]
questions:
  - "How do I open my soul to God's Love?"
  - "What does it feel like to receive Divine Love?"
related_messages: []
audio_url: ""
canonical_url: ""
notes: >
  Morning gathering in a private home circle.
significance: []
language: en
excerpt: ""
series: []
last_edited: 2025-06-01
```

## 6. Curator Conventions

The following conventions have been established through the curation process and should be followed by all contributors.

### Text Handling

- **Never alter message text** without explicit permission from the archive curator.
- **Spacing artifacts** (double spaces, space before punctuation): fix silently.
- **Clear typos** (e.g., "yolk" for "yoke", "froth" for "forth"): fix silently.
- **Grammar errors**: flag but do not auto-fix without permission.
- **Transcriber insertions** — words or phrases added by the transcriber for clarity should be wrapped in **square brackets** `[]`, not parentheses. Example: `He walked with them [after the resurrection] for forty days.`

### Notes Field

The `notes` field should only record curatorially significant information such as:
- Context about where or how the message was received
- Biographical details revealed in the message
- Connections to other messages or events
- Incomplete transcriptions or missing portions

Routine typo corrections do not need to be noted.

### Questions Field

Questions should be written as a real seeker would type them into a search engine at 2am. Aim for:
- Natural, human phrasing ("Why do I keep failing?" not "What causes repeated spiritual failure?")
- Universally applicable — not specific to people or events in the message
- A mix of spiritual, emotional, and practical angles
- Questions born from fear, doubt, grief, or confusion are particularly valuable

### Spirit Names in Keywords

If a spirit has a spirit file in `/spirits/`, do **not** include their name in the `keywords` field — they are already indexed via `spirit_id` and `spirits[]`. Only include spirit names in `keywords` if they are mentioned but have no spirit file.

Exception: the word "faith" is always treated as a concept keyword, never removed as a spirit name reference, unless the message is specifically by or about Faith Nyquist.

### Related Messages

`related_messages` should reflect **subject connections only** — not date proximity, same retreat, or same location. Two messages received on the same day are only linked if their content is thematically connected.

### Em Dashes

Avoid em dashes (—) in curator-written content (descriptions, excerpts, questions, notes, doors). Use a single hyphen (-) when a dash is needed, or rephrase to avoid it. Em dashes are a common AI writing pattern and reduce the human feel of the archive.

---

## 7. YAML Entry Style Guide

When adding or editing messages, please follow these YAML guidelines.

### Basics

 - Use two spaces per indentation level (no tabs).
 - Quote any string that includes special characters (`:`, `&`, `?`, etc.).
 - Use square brackets `[]` for short lists or multiple lines for readability.
 - Do not add blank lines at the beginning or end of the YAML block.
 - Save in UTF-8 encoding.
 - **Use YAML block scalar format (`>`) for `description`, `excerpt`, and `notes` fields.** This prevents long lines and improves readability. Example:
   ```yaml
   description: >
     A message encouraging disciples to walk confidently in God's light
     and share His Love with the world.
   ```
 - All field names must be **snake_case exactly as shown** — do not capitalize them (e.g., `spirit:` not `Spirit:`, `message_type:` not `MessageType:`).
 - The **`spirits` field uses `spirit_id` values** (lowercase kebab-case, matching the spirit's filename), not display names. This ensures consistent searchability. Example: `["john-the-beloved", "mary"]` not `["John the Beloved", "Mary"]`. The **`people` field** is the exception — since living people don't have profile files, use their full display names there.
 - **`primary_subjects` and `secondary_subjects`** can reference any level of the subject hierarchy — top category or subcategory. Always choose the most specific and relevant subject, regardless of its level. `secondary_subjects` is capped at five.

### Example of good formatting

```yaml
message_type: ["Guidance", "Teaching"]
secondary_subjects:
  - Spiritual Discipline & Daily Living
  - Service & Ministry
location:
  city: Gibsons
  region: BC
  country: Canada
```

### Common mistakes to avoid

| Mistake | Why It's Wrong | Correct Form |
|-------|------|------------|
| Using tabs instead of spaces | YAML is indentation-sensitive | Use 2 spaces |
| Unquoted title | Titles should always be in double quotes | `title: "Express Your Yearnings to God"` |
| Missing quotes around `:` or `&` | YAML misreads it as a key separator | `"Love & Truth"` |
| Empty array as `""` | Not valid | `[]` |
| Unclosed brackets | Parsing error | `["Teaching", "Guidance"]` |
| Capitalized field names | Must match schema exactly | `spirit: Jesus`, not `Spirit: Jesus` |
| Uppercase in IDs or `related_messages` | IDs must always be lowercase | `2015-11-28-af-mary`, not `2015-11-28-AF-Mary` |
| Using camelCase field names | All fields use snake_case | `message_type`, not `messageType`; `audio_url`, not `audioUrl` |
| Omitting optional fields entirely | Omitting fields breaks validators | Leave blank: `audio_url: ""` or `spirits: []` |


## 8. Contributor Checklist

Before committing a new message:

 - ✅ The **message_id** matches `YYYY-MM-DD-{medium_initials}-{spirit_id}` format and is **fully lowercase**; anonymous mediums use `xx` as medium_initials
 - ✅ The **spirit_id** matches a filename in the `/spirits/` folder exactly
 - ✅ The **title**, **date**, **spirit_id**, and **medium** are filled in
 - ✅ At least one **message_type** and one **primary_subjects** are present
 - ✅ **Optional fields are present but left blank if unknown** (e.g., `audio_url: ""` or `spirits: []`) — do not omit them entirely, as validators expect all fields to be present
 - ✅ All IDs in **related_messages** are lowercase and match existing `message_id` values exactly
 - ✅ All entries in **spirits** use `spirit_id` values (lowercase kebab-case) matching filenames in `/spirits/`
 - ✅ At least one **question** is included in the `questions` field to aid search discoverability
 - ✅ YAML validates without syntax errors (`yaml-validator` or VSCode plugin)
 - ✅ A short **description** is included
 - ✅ **language** is set (default `en`)
 - ✅ **excerpt** is filled in with an evocative pull quote or curator highlight
 - ✅ **series** is present (leave as `[]` if not yet assigned)
 - ✅ **significance** is present (leave as `[]` if none applies)
 - ✅ The file is saved as `.md` under the correct year/month folder
 - ✅ **last_edited** is set to today's date
 - ✅ Spirit names are **not** in `keywords` if that spirit has a file in `/spirits/`
 - ✅ Transcriber insertions use **square brackets** `[]` not parentheses


## 9. Translations

Translations are permitted and encouraged under the repository license.

Each translation should be saved as **its own Markdown** (`.md`) file in the same folder as the source message.

### Example filename:

```
2015-11-23-af-jesus.pt-br.md
```

### Example front matter for a translated file:

```yaml
---
language: pt-br
translation_of: 2015-11-23-af-jesus
message_id: 2015-11-23-af-jesus
title: Você São Meus Discípulos
date: 2015-11-23
spirit_id: jesus
spirit_name: Jesus
medium: Al Fike
location:
  city: Gibsons
  region: BC
  country: Canada
message_type: ["Teaching", "Guidance"]
description: >
  Uma mensagem encorajando os discípulos a caminharem com confiança
  na luz de Deus.
primary_subjects: Amor Divino & Relacionamento com Deus
secondary_subjects: []
people: []
spirits: []
keywords: ["discipulado", "serviço", "luz", "amor divino"]
related_messages: []
audio_url: ""
canonical_url: ""
notes: ""
last_edited: 2025-06-01
translations:
  available: [pt-br]
---
<translated message text here>

---
*Translated by [Translator Name]. Translation reviewed for fidelity to the original.*
```

Translation files should:

 - Retain the **same metadata structure and fields** as the original source file.
 - Include `translation_of` linking back to the source `message_id`.
 - Use the same `message_id` value as the source for cross-referencing.
 - Be reviewed for fidelity to the original meaning before committing.
 - Include a translator's note or credit at the end if desired.
 - Update `last_edited` if the translation is revised after the source message changes.

## 10. Licensing

**License:** `CC-BY-ND-4.0+Translations`

This license allows:
✅ **Redistribution**
✅ **Translation**
✅ **Reformatting** (HTML, PDF, etc.)

It prohibits:
❌ **Alteration of message text or meaning**

Translations are permitted provided they preserve meaning and acknowledge the source.
See the LICENSE file for full legal details.