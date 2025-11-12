# Divine Love Messages Schema & Contribution Guide 

This document defines the metadata standard for cataloguing the Divine Love Messages collection.
All contributors should follow these conventions to ensure consistency, searchability, and compatibility across future platforms.

THis document complements the machine-readable file [`message.schema.yml`](./message.schema.yml), which enforces structure through automated validation.

---


## 1. File layout & naming

Each message is stored in its own `.yml` file within a structured directory tree:

├─ content/  
│  └─ messages/  
│&nbsp;&nbsp;&nbsp;&nbsp;└─ 2015/  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─ 11/  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─2015-11-30-AF-Jesus.yml  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─ 12/  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─2015-12-07-AF-Andrew.yml  
│&nbsp;&nbsp;&nbsp;&nbsp;└─ 2016/  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─ 01/  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─2016-01-03-AF-Augustine.yml  
├─ spirits/  
│  └─ Jesus.yml  
│  └─ Andrew.yml  
│  └─ Augustine.yml  
├─ mediums/    
│  └─ Al-Fike.yml  
├─ schema/  
│  └─ schema.yml  
│  └─ schema.md    

 - `/messages/` contains all message entries organized by year.
 - `/spirits/` and `/mediums/` store background metadata about authors and mediums.
 - `/schema/` contains this documentation and the JSON/YAML schema definition.


## 2. Message ID Pattern
Each message has a unique id using this format:

### Pattern:

YYYY-MM-DD-{MediumInitials}-{SpiritName}{-2|-3|...}

### Rules:

 - `{MediumInitials}` = the first letter of the medium’s first and last name (capitalized).
Example: Al Fike → AF
 - `{SpiritName}` = the spirit’s full name with **each space replaced by a hyphen (-)**.
Example: John the Beloved → John-the-Beloved
 - Use **standard capitalization** for each part of the spirit’s name (capitalize first letter of each word).
 - If more than one message is received by the same spirit and medium on the same day, append `-2`, `-3`, etc. to keep all IDs unique.
 - **Never include spaces** in the ID — use hyphens instead. This ensures compatibility across URLs, filenames, and YAML parsing.

### Example IDs

```yaml
2015-10-12-AF-John-the-Beloved
2015-11-30-AF-Jesus
2015-11-30-AF-Jesus-2
2015-12-01-AF-Augustine
```

### Filename Example

```yaml
2015-10-12-AF-John-the-Beloved.yml
```

### YAML Field Example

```yaml
id: 2015-10-12-AF-John-the-Beloved
spirit: John the Beloved
```

---

## 3. Message file format

Each message file is a **Markdown document** with a **YAML front matter** block followed by the **message text**.

```yaml
---
# YAML front matter (metadata)
id: 2015-11-30-AF-Jesus
title: You are my disciples
date: 2015-11-30
spirit: Jesus
medium: Al Fike
location:
  city: Gibsons
  region: BC        # optional
  country: Canada   # optional
messageType: ["Teaching", "Guidance"]  # any of: Blessing, Guidance, Teaching; can be multiple
description: A message encouraging disciples to walk confidently in God's light and share His Love with the world.
primarySubjects: Divine Love & Relationship with God   # exactly one main subject
secondarySubjects: ["Spiritual Discipline & Daily Living", "Service & Ministry"]  # up to two
people: []          # living humans mentioned (not the medium)
spirits: ["Andrew", "Augustine"]         # other spirits mentioned besides `spirit`
keywords: ["discipleship", "service", "light", "divine love"]
relatedMessages: ["2015-11-28-AF-Mary"]
audioUrl: https://example.org/audio/2015-11-30-jesus.mp3
canonicalUrl: https://divinelovesanctuary.com/messages/2015-11-30-jesus
notes: Message received during evening circle in Gibsons, BC.
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
| **id** | string | Unique identifier formatted `YYYY-MM-DD-{MediumInitials}-{SpiritName}{-2 -3...}`. Braces show the pattern only, do **not** include them in real IDs. `{MediumInitials}` are the capitalized first and last initials of the medium (e.g., Al Fike → AF). `{SpiritName}` uses normal capitalization (e.g., “John the Beloved”). If multiple messages share the same date/medium/spirit, append `-2`, `-3`, etc. | `2015-11-30-AF-Jesus-2` |
| **title** | string | The given title of the message. If none exists, create one (concise and meaningful) and append an asterisk (*) to show it was added later. | `You are my disciples` |
| **date** | string (YYYY-MM-DD) | The date the message was received, always using ISO format. | `2015-11-30` |
| **spirit** | string | The full name of the spirit author, written in normal capitalization (e.g., “John the Beloved”). | `John the Beloved` |
| **medium** | string | The full name of the human medium who received the message. These initials form the {MediumInitials} in the ID. | `Al Fike` |
| **location.city** | string | The city or locality where the message was received. | `Gibsons` |
| **location.region** | string | The state, province, or region. Optional; leave blank if not applicable. | `BC` |
| **location.country** | string | The country where the message was received. Optional. | `Canada` |
| **messageType** | array of strings | One or more of: **Blessing, Guidance, Teaching**. Messages may include multiple types. | `["Guidance", "Teaching"]` |
| **description** | string | A short (1–2 sentence) summary describing the purpose or insight of the message. | `Encouragement to release fear and trust God's protection amid changing earthly conditions.` |
| **primarySubjects** | string | The single main subject category chosen from the subject hierarchy. Represents the central theme. | `Divine Love & Relationship with God` |
| **secondarySubjects** | array of strings (up to 2) | Up to two related subjects drawn from the same hierarchy to reflect secondary themes. | `["Spiritual Discipline & Daily Living", "Earthly Challenges & Human Condition"]` |
| **people** | array of strings | Names of living human beings mentioned (excluding the medium). | `["James Padgett", "Helen Padgett"]` |
| **spirits** | array of strings | Names of other spirits mentioned besides the main `spirit` field. | `["Alec Gaunt", "Mary"]` |
| **keywords** | array of strings | Free-form topical tags or short phrases to improve search and categorization. | `["trust", "peace", "faith", "guidance"]` |
| **relatedMessages** | array of strings | Message IDs of other texts connected by subject, author, or event. Use full ID format. | `["2015-11-28-AF-Mary", "2015-11-26-AF-Augustine"]` |
| **audioUrl** | string (URL) | A direct link to an audio recording of the message (MP3 or stream). Leave blank if none. | `https://example.org/audio/2015-11-30-jesus.mp3` |
| **canonicalUrl** | string (URL) | The permanent public URL where the message is officially published. Used for citation and linking. | `https://divinelovesanctuary.com/messages/2015-11-30-jesus` |
| **notes** | string | Optional free-text field for contextual notes about where or how the message was received. | Evening prayer circle at Gibsons, BC |

---


## 5. Example YAML Files

### Full Example

```yaml
id: 2015-11-30-AF-Jesus
title: You are my disciples
date: 2015-11-30
spirit: Jesus
medium: Al Fike
location:
  city: Gibsons
  region: BC
  country: Canada
messageType: ["Teaching", "Guidance"]
description: A message encouraging disciples to walk confidently in God's light and share His Love with the world.
primarySubjects: Divine Love & Relationship with God
secondarySubjects: ["Spiritual Discipline & Daily Living", "Service & Ministry"]
people: []
spirits: ["Andrew", "Augustine"]
keywords: ["discipleship", "service", "light", "divine love"]
relatedMessages: ["2015-11-28-AF-Mary"]
audioUrl: https://example.org/audio/2015-11-30-jesus.mp3
canonicalUrl: https://divinelovesanctuary.com/messages/2015-11-30-jesus
notes: Message received during evening circle in Gibsons, BC.
```

### MInimal Example

```yaml
id: 2015-12-07-AF-Andrew
title: Be open to God as a flower opens to the sun
date: 2015-12-07
spirit: Andrew
medium: Al Fike
location:
  city: Vancouver
  region: BC
  country: Canada
messageType: ["Blessing"]
description: Encouragement to open the soul to God's Love like a flower to the sun.
primarySubjects: Divine Love & Relationship with God
secondarySubjects: []
people: []
spirits: []
keywords: ["openness", "prayer", "faith"]
relatedMessages: []
audioUrl: ""
canonicalUrl: ""
notes: Morning gathering in a private home circle.
```

## 6. YAML Entry Style Guide

When adding or editing messages, please follow these YAML guidelines.

### Basics

 - Use two spaces per indentation level (no tabs).
 - Quote any string that includes special characters (`:`, `&`, `?`, etc.).
 - Use square brackets `[]` for short lists or multiple lines for readability.
 - Do not add blank lines at the beginning or end of the YAML block.
 - Save in UTF-8 encoding.

### Example of good formatting

```yaml
messageType: ["Guidance", "Teaching"]
secondarySubjects:
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
| Using tabs instead of spaces	| YAML is indentation-sensitive	| Use 2 spaces |
| Missing quotes around `:` or `&`	| YAML misreads it as a key separator	| `"Love & Truth"` |
| Empty array as `""` |	Not valid	| `[]` |
| Unclosed brackets	| Parsing error	| `["Teaching", "Guidance"]` |
| Capitalized field names	| Must match schema	| `spirit: Jesus`, not `Spirit:` |


## 7. Contributor Checklist

Before committing a new message:

 - ✅ The **ID** matches `YYYY-MM-DD-{MediumInitials}-{SpiritName}` format
 - ✅ The **SpiritName** uses hyphens for multi-word names (e.g., John-the-Beloved)
 - ✅ The **title**, **date**, **spirit**, and **medium** are filled in
 - ✅ At least one **messageType** and one **primarySubject**
 - ✅ Optional fields are blank if unknown (not omitted)
 - ✅ YAML validates without syntax errors (`yaml-validator` or VSCode plugin)
 - ✅ A short **description** is included
 - ✅ The file is saved as `.yml` under the correct year folder


## 8. Translations

Translations are permitted and encouraged under the repository license.

Each translation should be saved as **its own Markdown** (`.md`) file in the same folder as the source message.

### Example filename:

```yaml
2015-11-23-AF-Jesus.pt-br.md
```

### Example front matter for a translated file:

```yaml
language: pt-br
translations:
  available: [pt-br]
  translation_of: 2015-11-23-AF-Jesus
```

Translation files should:

 - Retain the same metadata structure and fields as the original.
 - Include a translator’s note or credit at the end if desired.
 - Use the same `id` pattern for cross-referencing (e.g., `translation_of` links back to the main `.yml`).
 - Be reviewed for fidelity to the original meaning.

## 9. Licensing

**License:** `CC-BY-ND-4.0+Translations`

This license allows:
✅ **Redistribution**
✅ **Translation**
✅ **Reformatting** (HTML, PDF, etc.)

It prohibits:
❌ **Alteration of message text or meaning**

Translations are permitted provided they preserve meaning and acknowledge the source.
See the LICENSE file for full legal details.
