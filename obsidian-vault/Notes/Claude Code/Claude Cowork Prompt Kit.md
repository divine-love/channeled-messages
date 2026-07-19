# Cowork Prompt Kit: Batch Cataloguing with Opus

## Divine Love Messages Archive

Save this file; paste the prompts in order. Attach the listed files each session.

Last updated: 2026-07-19 (chains staging expanded: back-search confirmations, holding-pen witness sightings, portal watch; slug guard refined: unregistered slugs banned from entry lines, candidate slug suggestions welcome in curator-decision notes; pipe heading format stated explicitly; Prompt 2 restatement now covers chain observations)

---

## Files to attach to the Cowork session (every time)

- The Word document of messages
- schema/schema.md (the rulebook; canonical)
- schema/message.schema.yml (structure and caps)
- metadata/subjects.yml (subject vocabulary)
- project-instructions.md (workflow and current state)
- llms.txt (index of all existing messages: for ID collision checks and related_messages candidates)
- metadata/chains-threads.md (thread registry: for chain proposals)
- metadata/chains-log.md (chain evidence log: for chain proposals)
- Two or three finished message .md files from the repo, chosen by the curator as exemplars of the quality bar (strong doors, questions, descriptions)
    - 2019-04-08-mc-mary.md
    - 2019-02-22-af-augustine.md
    - 1963-12-26-ds-mary.md

---

## PROMPT 1: Setup and extraction (paste first, wait for the inventory)

You are cataloguing channeled messages for the Divine Love Messages archive. The attached schema.md is the complete rulebook and is canonical; read it fully before doing anything. project-instructions.md carries the workflow and current state. Follow both exactly. Where they conflict, schema.md wins.

Rules that override everything else, even if you think you have a better idea:

- NEVER alter message body text beyond the corrections schema.md explicitly permits (spacing artifacts and clear typos, fixed silently but LISTED in your report; grammar, fragments, and punctuation are flagged in the report, never fixed).
- Every subject value must exist, exactly, in the attached subjects.yml. Verify with code, not from memory. If no subject fits, use the closest valid one and flag it in the report. Never invent a subject name.
- Enforce every cap with code: description max 600 characters, excerpt under 200, door under 300, secondary_subjects max 5, exactly one message_type.
- No em dashes anywhere, in any file you produce.
- The notes field holds reference items only, per schema.md section 6. Never restate the description. Never record your cataloguing reasoning.
- Never declare any message a "first" of anything.
- spirits[] may only contain spirit_ids that already have a file in /spirits/ per the index. If a message mentions a spirit with no file, leave them in the body and keywords and flag it in the report.
- medium field is a plain "First Last" name, no honorifics.
- When you are uncertain about ANY judgment, choose the conservative option and flag it in the report. In this batch workflow, flagging replaces asking.
- STOP CONDITIONS: if message boundaries in the document are unclear, if header fields conflict, or if a message body appears truncated or corrupted, stop the batch and report the problem. Never produce a best guess for a message you cannot cleanly extract.

The attached finished message files are exemplars: match their quality, especially in the door, questions, and description fields. When producing later batches, always imitate these exemplars, never your own earlier output.

Your first task, before any cataloguing: read the attached Word document and produce an INVENTORY ONLY. For each message you find, list: proposed message_id (per the schema ID pattern, checking llms.txt and the other inventory entries for collisions), title (mark with * if you had to create one), spirit, medium, date, location, and approximate word count. Flag any message where the boundaries are unclear (where one message may have bled into another), any missing header fields, any duplicate of a message already in llms.txt, and any message whose spirit or medium has no existing file.

Do not create any files yet. Show me the inventory and wait.

---

## PROMPT 2: Confirm inventory (after you review and correct the list)

The inventory is confirmed [with these corrections: ...]. Before we begin processing, restate in your own words: the five hard caps you will enforce with code, what goes in the notes field, what you will do with chain observations, and what you will do when uncertain. Then wait.

(This restatement step is cheap insurance that the rules survived into working memory.)

---

## PROMPT 3: Process a batch (repeat this prompt for each batch)

Process the next 5 messages from the confirmed inventory, one at a time, completely, before moving to the next. For each message:

- Extract the body text exactly, preserving paragraphs and italics.
- Apply the full workflow from project-instructions.md steps 2-9.
- Since these transcripts are not yet verified against any published source: set canonical_url: "" and add "Not publicly posted online." to notes. I will replace these for any message I find published.
- Validate the finished file with code: YAML parses, all caps pass, all subjects exist in subjects.yml, spirits[] entries all exist in the spirit index, no em dashes anywhere in the file. Then verify body fidelity with code: the body text of the finished file must match the text you extracted from the source, compared programmatically after normalizing whitespace, with any permitted silent corrections accounted for on an explicit list. Report the comparison result per message; a mismatch you cannot explain stops the batch.
- Save the file as outputs/messages/{message_id}.md

Do NOT edit any existing file. Instead, stage proposals:

- outputs/REVIEW.md (append per message): text corrections made silently (each one listed); flags needing my decision (grammar, fragments, ambiguous subjects, message_type edge calls, essential_teachings suggestions, spirits without files); proposed related_messages with the exact reciprocal lines I would paste into the other files, in chronological position.
    
- outputs/chains-proposed.md (append per message): draft chain entries in the exact format of chains-log.md (pipe-separated headings: ### id | Title | date), each line tagged [batch-proposed]. Use the thread registry and design blocks in chains-threads.md to choose roles; never use a thread slug that does not appear in chains-threads.md. For EVERY proposed member role you must include: (a) which existing member of that thread is closest to this message, and (b) one sentence stating what NEW facet this message adds that the closest member does not already carry. If you cannot name a new facet, do not propose a member role; record a witness-level NOTE instead. When unsure between two roles, choose the more modest one. Additionally, for every message: (1) check chains-log.md for an existing entry under that message_id tagged [back-search]; if found, confirm or contradict the provisional role now that the full text is in hand, quoting the deciding passage; (2) check the Holding Pen in chains-threads.md and record a witness sighting for any candidate this message supports (divine-love-healing has a flagged checkpoint at 2016-04-13, inside this document's range); (3) record any sighting relevant to the portal watch in the log. If a message seems to warrant a new thread or holding-pen candidate, describe the pattern; do not mint anything; never use an unregistered slug in an entry line, though you may suggest candidate slug names inside the curator-decision note.
    
- outputs/spirit-updates-proposed.md: for any biographical detail a message reveals about a spirit, the exact notes text I would add to that spirit's file, citing the message_id. For any new spirit or medium a message requires, a complete draft file, clearly marked DRAFT.
    

After the batch of 5, stop and give me a one-paragraph summary of the batch and anything that worried you. Wait for me to say continue.

---

## PROMPT 4: Session wrap (paste at the end of a Cowork session)

Produce outputs/MANIFEST.md: every file created this session, the message ids processed, the ids remaining in the inventory, and every unresolved flag from REVIEW.md in one list. Note anything about this batch that the next session should know.

---

## Session hygiene (for you)

Cap each Cowork session at three or four batches (15-20 messages); quality drifts in long sessions. Start every new session with Prompt 1 and the Prompt 2 restatement, attaching the previous session's MANIFEST.md and FRESHLY exported copies of the reference files (a stale subjects.yml or chains file means instant drift).

Review the first batch at 100%. After that, per batch: read every door and every REVIEW.md flag, and spot-check one full message end to end (front matter and body against the Word document). If a spot-check fails twice, return to full review for a batch.

---

## Your review loop (for you, not for Opus)

For each batch: read REVIEW.md flags and decide them; check each message against the online archive and set canonical_url where published (removing the "Not publicly posted online." note); paste reciprocal lines into the existing files; review chains-proposed.md and merge approved entries into chains-log.md (removing the [batch-proposed] tag; keep the log's chronological placement) and record approved witness sightings and back-search confirmations in chains-threads.md where they touch the Holding Pen; apply approved spirit updates; run validate_messages.py; commit. Any judgment you want a second opinion on, bring back to this project.