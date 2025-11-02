# 📜 Divine Love Messages Metadata Schema  
*A Contributor’s Guide to Structure, Tagging, and Organization*  

This document explains how each **message file** in the Divine Love Digital Canon should be organized, described, and tagged for discoverability, translation, and long-term preservation.  

It complements the machine-readable file [`message.schema.yml`](./message.schema.yml), which enforces structure through automated validation.

---

## 🗂️ 1. File Layout and Naming

### Folder Structure
content/
messages/
2015/
05/
2015-05-19-al-fike-andrew.md
12/
2015-12-27-al-fike-augustine.md

shell
Copy code

### Filename Pattern
YYYY-MM-DD-<medium-slug>-<spirit-slug>.md

markdown
Copy code

- Use **lowercase kebab-case** (e.g., `al-fike`, `john-the-beloved`).
- If multiple messages were received from the **same spirit and medium** on the **same date**, append an increment:
  - `...-2.md`, `...-3.md`, etc.
- Example:
2015-09-27-al-fike-augustine.md
2015-09-27-al-fike-augustine-2.md

yaml
Copy code

---

## ✍️ 2. Message File Structure

Each message file is a **Markdown document** with a **YAML front matter** block followed by the **verbatim transcript**.

```yaml
---
id: 2015-05-19-al-fike-andrew
title: Lay Down False Judgments; Walk Together in Love
date: 2015-05-19
language: en
spirit: andrew
medium: al-fike
location:
city: Gibsons
region: BC        # optional
country: CA
message_types: [Blessing, Guidance]
primary_subjects: [divine-love-relationship-with-god, spiritual-discipline-daily-living]
secondary_subjects: [community-and-service, unity-and-humility]
description: A call to drop mental judgments, accept one another’s gifts, and let the soul’s light lead.
keywords: [judgment, unity, humility, soul-mind, harmony]
cross_references: [2015-09-27-al-fike-augustine, 2015-11-02-al-fike-john]
people: [al-fike]
spirits_mentioned: [faith, john-the-beloved]
source:
canonical_url: https://example.org/messages/2015/05/19/andrew
audio_url: https://example.org/audio/2015-05-19-andrew.mp3
license: CC-BY-ND-4.0+Translations
status: published
translations:
available: [pt-br, es]
translation_of: null
---

(message body here — verbatim transcript)
Note:
Light formatting (paragraphs, italics, etc.) is fine.
Do not paraphrase or edit the teaching content.

🧩 3. Field-by-Field Reference
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
