# Divine Love Messages Schema & Contribution Guide 

This document explains how to structure, name, and describe message files in this repository so they’re easy to browse, search, and reuse.

It complements the machine-readable file [`message.schema.yml`](./message.schema.yml), which enforces structure through automated validation.

---


## 1. Repository layout & naming

/  
├─ schema.md  
├─ README.md  
├─ CONTRIBUTING.md  
├─ content/  
│  └─ messages/  
│&nbsp;&nbsp;&nbsp;&nbsp;└─ YYYY/  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─ MM/  
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─ {ID}.md  
└─ media/  
&nbsp;&nbsp;&nbsp;   ├─ audio/  
&nbsp;&nbsp;&nbsp;   └─ images/  



### Folder Structure
content/  
&nbsp;messages/  
&nbsp;&nbsp;YYYY/  
&nbsp;&nbsp;&nbsp;MM/  
&nbsp;&nbsp;&nbsp;&nbsp;<ID>.md  

 - Message file path: content/messages/YYYY/MM/DD/{ID}.md  
 - Message file name {ID}.md uses the ID field (defined below).


## 2. Message ID Pattern
Each message needs a globally unique id.

### Pattern:

YYYY-MM-DD-{MediumInitials}-{SpiritName}(-2|-3|...)

 - YYYY-MM-DD — Gregorian calendar date of the message.  
 - {MediumInitials} — first letter of the medium’s first name + first letter of their last name, both uppercase.  
 - Examples: Al Fike → AF · Leslie Stone → LS · James Padgett → JP  
 - {SpiritName} — Spirit’s full name with standard capitalization (spaces allowed).  
 - Example: John the Beloved, Alec Gaunt, Mary, King Solomon, Seretta Kem  
 - Uniqueness suffix: If multiple messages share the same date, medium initials, and spirit name, append -2, -3, etc.  
 - Hyphens: Used only within the message ID or URL in place of spaces (e.g., John-the-Beloved in the ID, but “John the Beloved” in metadata).  

### Examples

2015-10-12-AF-John-the-Beloved
2015-10-12-AF-Mary
2015-10-12-AF-Mary-2
2015-10-26-AF-Aman

The ID string is also the filename: {ID}.md


---

## 3. Message file format

Each message file is a **Markdown document** with a **YAML front matter** block followed by the **message text**.

```yaml
---
id: 2015-10-12-AF-John-the-Beloved
title: God will embrace all in time
date: 2015-10-12
spirit: John the Beloved
medium: Al Fike
location:
  city: West Vancouver
  region: BC        # optional
  country: Canada   # optional
messageType: ["Guidance"]  # any of: Blessing, Guidance, Teaching; can be multiple
description: "Encouragement to release fear and trust God's protection amid changing earthly conditions."
primarySubjects: "Divine Love & Relationship with God"   # exactly one main subject
secondarySubjects: ["Spiritual Discipline & Daily Living", "Earthly Challenges & Human Condition"]  # up to two
people: []          # living humans mentioned (not the medium)
spirits: []         # other spirits mentioned besides `spirit`
keywords: ["trust", "protection", "fear", "peace"]
relatedMessages: ["2015-10-12-AF-Mary"]
audioUrl: https://example.org/audio/2015-10-12-john.mp3
canonicalUrl: https://example.org/messages/2015-10-12-john-the-beloved
locationNotes: "Evening prayer circle."
---
I am John. There is nothing to fear, my beloveds...

```

### Required Fields

 - id — must follow the pattern above.  
 - title — human-readable title.  
 - date — YYYY-MM-DD.  
 - spirit — e.g., John the Beloved, Alec Gaunt, Mary, King Solomon.  
 - medium — full name, e.g., Al Fike.  
 - messageType — array containing one or more of: Blessing, Guidance, Teaching.  
 - primarySubjects — one single subject selected from the main category list.  

### Optional but recommended

 - location.city (string)  
 - location.region (string; optional)  
 - location.country (string; optional)  
 - description (1–3 sentences)  
 - secondarySubjects — array of up to two additional subcategories for nuance.  
 - people (array of living persons mentioned, excluding the medium)  
 - spirits (array of spirits mentioned, excluding spirit)  
 - keywords (array of strings)  
 - relatedMessages (array of message IDs)  
 - audioUrl (URL to recording, if any)  
 - canonicalUrl (URL to canonical page if hosted elsewhere)  
 - locationNotes (free text)

### Note:
Light formatting (paragraphs, italics, etc.) is fine.
Do not paraphrase or edit the teaching content.

| Field                 | Type                       | Description                                                                                                                                | Example                                                                                      |                                                                                                                                                                                                                                                                                                                               |                       |
| --------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| **id**                | string                     | Unique identifier for each message in the format `YYYY-MM-DD-{MediumInitials}-{SpiritName}{-2 -3}                                         | `2015-11-30-AF-Jesus` 
| **title**             | string                     | The given title of the message. If none exists, create one (concise and meaningful) and append an asterisk (*) to show it was added later. | `You are my disciples`                                                                       |                                                                                                                                                          
| **date**              | string (YYYY-MM-DD)        | The date the message was received, always using ISO format.                                                                                | `2015-11-30`                                                                                 |                                                                                                                                                          
| **spirit**            | string                     | The full name of the spirit author, written in normal capitalization (e.g., “John the Beloved”).                                           | `John the Beloved`                                                                           |                                                                                                                                                          
| **medium**            | string                     | The full name of the human medium who received the message. These initials form the `{MediumInitials}` in the ID.                          | `Al Fike`                                                                                    |                                                                                                                                                          
| **location.city**     | string                     | The city or locality where the message was received.                                                                                       | `Gibsons`                                                                                    |                                                                                                                                                          
| **location.region**   | string                     | The state, province, or region. Optional; leave blank if not applicable.                                                                   | `BC`                                                                                         |                                                                                                                                                          
| **location.country**  | string                     | The country where the message was received. Optional.                                                                                      | `Canada`                                                                                     |                                                                                                                                                          
| **messageType**       | array of strings           | One or more of: **Blessing**, **Guidance**, **Teaching**. Messages may include multiple types.                                             | `["Guidance", "Teaching"]`                                                                   |                                                                                                                                              
| **description**       | string                     | A short (1–2 sentence) summary describing the purpose or insight of the message.                                                           | `Encouragement to release fear and trust God's protection amid changing earthly conditions.` |                                                                                                                                                          
| **primarySubjects**   | string                     | The single main subject category chosen from the subject hierarchy. Represents the central theme.                                          | `Divine Love & Relationship with God`                                                        |                                                                                                                                               
| **secondarySubjects** | array of strings (up to 2) | Up to two related subjects drawn from the same hierarchy to reflect secondary themes.                                                      | `["Spiritual Discipline & Daily Living", "Earthly Challenges & Human Condition"]`            |                                                                                                                                                          
| **people**            | array of strings           | Names of living human beings mentioned (excluding the medium).                                                                             | `["James Padgett", "Helen Padgett"]`                                                         |                                                                                                                                                          
| **spirits**           | array of strings           | Names of other spirits mentioned besides the main `spirit` field.                                                                          | `["Alec Gaunt", "Mary"]`                                                                     |                                                                                                                                                          
| **keywords**          | array of strings           | Free-form topical tags or short phrases to improve search and categorization.                                                              | `["trust", "peace", "faith", "guidance"]`                                                    |                                                                                                                                                    
| **relatedMessages**   | array of strings           | Message IDs of other texts connected by subject, author, or event. Use full ID format.                                                     | `["2015-11-28-AF-Mary", "2015-11-26-AF-Augustine"]`                                          |                                                                                                                                                        
| **audioUrl**          | string (URL)               | A direct link to an audio recording of the message (MP3 or stream). Leave blank if none.                                                   | `https://example.org/audio/2015-11-30-jesus.mp3`                                             |                                                                                                                                
| **canonicalUrl**      | string (URL)               | The permanent public URL where the message is officially published. Used for citation and linking.                                         | `https://divinelovesanctuary.com/messages/2015-11-30-jesus`                                  |                                                                                                                                
| **locationNotes**     | string                     | Optional free-text field for contextual notes about where or how the message was received.                                                 | `Evening prayer circle at Gibsons, BC`                                                       |                                                                                                                                                          





| Field               | Type                        | Description                                                                                                                                                                                                                                                                                                                                                                                                                 | Example                                                                                            |
| ------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `id`                | string                      | Unique identifier for each message in the format `YYYY-MM-DD-MediumInitials-SpiritName`. MediumInitials use the **first and last capital letters** of the medium’s full name (e.g. Al Fike → `AF`). SpiritName uses **standard capitalization** (first letter of each name capitalized). If multiple messages are received by the same medium and spirit on the same date, append `-2`, `-3`, etc., to maintain uniqueness. | `2015-12-27-AF-Augustine`                                                                          |
| `title`             | string                      | The official title of the message as it should appear in the index.                                                                                                                                                                                                                                                                                                                                                         | Awakening of the Soul Mind                                                                         |
| `spirit`            | string                      | Name of the spirit author of the message.                                                                                                                                                                                                                                                                                                                                                                                   | Augustine                                                                                          |
| `medium`            | string                      | Name of the human medium who received the message.                                                                                                                                                                                                                                                                                                                                                                          | Al Fike                                                                                            |
| `location`          | string                      | City and (optional) region and country where the message was received.                                                                                                                                                                                                                                                                                                                                                      | Gibsons, BC                                                                                        |
| `date`              | date                        | Date the message was received, in ISO 8601 format (`YYYY-MM-DD`).                                                                                                                                                                                                                                                                                                                                                           | 2015-12-27                                                                                         |
| `description`       | string                      | A brief (1–2 sentence) overview summarizing the message.                                                                                                                                                                                                                                                                                                                                                                    | A teaching on the awakening of soul perception and the difference between mind and soul awareness. |
| `messageType`       | array of strings            | One or more of: `Blessing`, `Guidance`, `Teaching`.                                                                                                                                                                                                                                                                                                                                                                         | `[ "Guidance", "Teaching" ]`                                                                       |
| `primarySubjects`   | array of strings            | Primary subject(s) from the *Hierarchy of Subjects in the Messages* reference table.                                                                                                                                                                                                                                                                                                                                        | `[ "Divine Love & Relationship with God" ]`                                                        |
| `secondarySubjects` | array of strings            | Secondary or related subject(s) from the same hierarchy.                                                                                                                                                                                                                                                                                                                                                                    | `[ "Soul Transformation & Development", "Spiritual Discipline & Daily Living" ]`                   |
| `themeClusters`     | array of strings (optional) | Optional broader themes connecting multiple messages.                                                                                                                                                                                                                                                                                                                                                                       | `[ "Service and Circles of Light", "Healing and Renewal" ]`                                        |
| `people`            | array of strings (optional) | Names of living participants mentioned or involved (not spirits).                                                                                                                                                                                                                                                                                                                                                           | `[ "Geoff Cutler", "Al Fike" ]`                                                                    |
| `spirits`           | array of strings (optional) | Other spirit communicators mentioned besides the main author.                                                                                                                                                                                                                                                                                                                                                               | `[ "Jesus", "Mary" ]`                                                                              |
| `locationNotes`     | string (optional)           | Additional contextual notes about the setting or circumstances.                                                                                                                                                                                                                                                                                                                                                             | “Shared at the West Vancouver prayer circle.”                                                      |
| `canonicalUrl`      | string (optional)           | Permanent link to the message on an external site.                                                                                                                                                                                                                                                                                                                                                                          | `https://divinelovesanctuary.com/messages/awakening-of-the-soul-mind`                              |
| `audioUrl`          | string (optional)           | Link to the original or corresponding audio recording.                                                                                                                                                                                                                                                                                                                                                                      | `https://soundcloud.com/divine-love/2015-12-27-augustine.mp3`                                      |
| `relatedMessages`   | array of strings (optional) | IDs of related or follow-up messages.                                                                                                                                                                                                                                                                                                                                                                                       | `[ "2015-12-21-AF-Peter", "2015-12-28-AF-Keea-Atta-Kem" ]`                                         |
| `notes`             | string (optional)           | Freeform notes, editor comments, or additional context.                                                                                                                                                                                                                                                                                                                                                                     | “Delivered during the final circle of 2015.”                                                       |


3. Field-by-Field Reference
Required Fields
Field	Type	Description
id	string	Unique ID using the pattern YYYY-MM-DD-Medium-Spirit. If multiple messages share a date and medium/spirit, append -2, -3, etc.
title	string	Concise title (≤100 chars) expressing the essence of the message.
date	string	ISO date (YYYY-MM-DD) of delivery.
language	string	IETF language code (e.g., en, pt-br).
spirit	slug	The spirit author (e.g., andrew, jesus, mary, etc.).
medium	slug	The human medium (e.g., al-fike).
location	object	{ city, region?, country } — region optional.
message_types	array	One or more of [Blessing, Guidance, Teaching].
primary_subjects	array	1–3 main subjects from the Hierarchy of Subjects.
description	string	1–2 sentence summary (neutral tone).
license	string	Usually CC-BY-ND-4.0+Translations.
status	enum	draft or published.

Recommended Fields
Field	Type	Description
secondary_subjects	array	Supporting topics from the hierarchy.
keywords	array	Free-form tags (not official subjects).
cross_references	array	IDs of related messages.
people	array	Living participants (mediums, organizers).
spirits_mentioned	array	Spirits referenced within the message.
source.canonical_url	string	External canonical link (if hosted elsewhere).
source.audio_url	string	Audio recording of the message.
translations.available	array	Which translations exist (e.g., [pt-br, es]).
translations.translation_of	string / null	For translated files, reference the original message ID.

🕊️ 4. Subjects, People, and Spirits
Keep canonical lists under:

Copy code
taxonomies/
  subjects.yml
  spirits.yml
  people.yml
Each uses a simple key/value format (slug → display name + notes).

⚙️ Subjects should align with the Hierarchy of Subjects in the Messages.
If a new subject is needed, propose it via pull request updating subjects.yml.

💬 5. The Message Body
After the front matter, include the verbatim transcript.
You may:

Preserve paragraphs and line breaks.

Fix clear transcription errors (document in PR notes).

Use minimal Markdown for clarity.

You may not:

Alter meaning or phrasing.

Add commentary or interpretation inline.

🌍 6. Translations
Translations are permitted and encouraged under the repository license.

Each translation = its own Markdown file.

Example filename:

yaml
Copy code
2015-11-23-al-fike-jesus.pt-br.md
Example front matter for a translated file:

yaml
Copy code
language: pt-br
translations:
  available: [pt-br]
  translation_of: 2015-11-23-al-fike-jesus
⚖️ 7. Licensing
License: CC-BY-ND-4.0+Translations

Allows:
✅ Redistribution
✅ Translation
✅ Reformatting (HTML, PDF, etc.)

Prohibits:
❌ Alteration of message text or meaning

See LICENSE for full legal details.

🧭 8. Adding a New Message
Quick Checklist
Create a new file in content/messages/YYYY/MM/.

Name it: YYYY-MM-DD-<medium-slug>-<spirit-slug>.md.

Add YAML front matter and fill all required fields.

Paste the verbatim message below it.

Verify links, tags, and spelling.

Commit with a clear message, e.g.:

sql
Copy code
Add 2015-12-27 message from Augustine: Awakening of the Soul Mind
🪶 9. Template Snippets
New Message
yaml
Copy code
---
id: 2015-11-23-al-fike-jesus
title: It Shall Start in the West and Circle the World
date: 2015-11-23
language: en
spirit: jesus
medium: al-fike
location:
  city: Gibsons
  region: BC
  country: CA
message_types: [Teaching]
primary_subjects: [divine-love-relationship-with-god]
secondary_subjects: [mission-and-service, circles-of-light, prayer]
description: Jesus encourages steadfast prayer and unity, foretelling a widening network of Light that will encircle the world.
keywords: [circles of light, prayer, mission]
cross_references: [2015-11-16-al-fike-confucius]
people: [al-fike]
spirits_mentioned: []
source:
  canonical_url: https://example.org/messages/2015/11/23/jesus
  audio_url: https://example.org/audio/2015-11-23-jesus.mp3
license: CC-BY-ND-4.0+Translations
status: published
translations:
  available: []
  translation_of: null
---
(message text)
Translation
yaml
Copy code
---
id: 2015-11-23-al-fike-jesus
title: Começará no Oeste e Dará a Volta ao Mundo
date: 2015-11-23
language: pt-br
spirit: jesus
medium: al-fike
location:
  city: Gibsons
  region: BC
  country: CA
message_types: [Teaching]
primary_subjects: [divine-love-relationship-with-god]
secondary_subjects: [mission-and-service, circles-of-light, prayer]
description: Jesus incentiva oração e unidade, prevendo uma rede de Luz que se ampliará ao redor do mundo.
keywords: [círculos de luz, oração, rede, missão]
cross_references: [2015-11-16-al-fike-confucius]
people: [al-fike]
spirits_mentioned: []
source:
  canonical_url: https://example.org/messages/2015/11/23/jesus
  audio_url: https://example.org/audio/2015-11-23-jesus.mp3
license: CC-BY-ND-4.0+Translations
status: published
translations:
  available: [pt-br]
  translation_of: 2015-11-23-al-fike-jesus
---
(traduzido texto da mensagem)
🧠 10. Validation & Quality Checks
✅ Dates must be ISO format (YYYY-MM-DD).

✅ Slugs must match taxonomy lists.

✅ Message types only from [Blessing, Guidance, Teaching].

✅ Locations should include valid countries.

✅ URLs should be absolute and reachable.

⚙️ Automated validation can be added later using a YAML schema validator.

💡 11. Common Questions
Q: Can I leave some fields blank?
A: Yes — only the required ones are mandatory.

Q: Why use slugs?
A: For stability across languages and systems; display names live in taxonomies/*.yml.

Q: Can I make notes about edits?
A: Yes, in your pull request description, not in the message text.

Q: How do translations link back to the source?
A: Use the translations.translation_of field with the original message’s ID.

🤝 12. Contributing via Pull Requests
Each pull request should include:

One new message or small metadata update.

A clear commit message describing the change.

For translations, a link to the original message.

Example commit:

pgsql
Copy code
Add 2015-12-27 message by Augustine: Awakening of the Soul Mind
🌹 Closing Note
This schema is the living framework of the Divine Love Digital Canon — preserving every word faithfully, while inviting collaboration, translation, and discovery.
