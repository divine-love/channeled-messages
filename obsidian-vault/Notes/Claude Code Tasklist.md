Take DLSF Messages 2016 doc
Separate messages into individual files
Read through each file and convert it to a .md file according to the project instructions
You can read the messages in the repo or the vault for reference to related links


# Cowork Prompt Kit — Batch Cataloguing with Opus

# Divine Love Messages Archive

# Save this file; paste the prompts in order. Attach the listed files each session.

---

## Files to attach to the Cowork session (every time)

1. The Word document of messages
2. schema/schema.md (the rulebook; canonical)
3. schema/message.schema.yml (structure and caps)
4. metadata/subjects.yml (subject vocabulary)
5. project-instructions.md (workflow and current state)
6. llms.txt (index of all existing messages: for ID collision checks and related_messages candidates)
7. metadata/chains-threads.md (thread registry: for chain proposals)
8. metadata/chains-log.md (chain evidence log: for chain proposals)

---

## PROMPT 1 — Setup and extraction (paste first, wait for the inventory)

You are cataloguing channeled messages for the Divine Love Messages archive. The attached schema.md is the complete rulebook and is canonical; read it fully before doing anything. project-instructions.txt carries the workflow and current state. Follow both exactly. Where they conflict, schema.md wins.

Rules that override everything else, even if you think you have a better idea:

1. NEVER alter message body text beyond the corrections schema.md explicitly permits (spacing artifacts and clear typos, fixed silently but LISTED in your report; grammar, fragments, and punctuation are flagged in the report, never fixed).
2. Every subject value must exist, exactly, in the attached subjects.yml. Verify with code, not from memory. If no subject fits, use the closest valid one and flag it in the report. Never invent a subject name.
3. Enforce every cap with code: description max 600 characters, excerpt under 200, door under 300, secondary_subjects max 5, exactly one message_type.
4. No em dashes anywhere, in any file you produce.
5. The notes field holds reference items only, per schema.md section 6. Never restate the description. Never record your cataloguing reasoning.
6. Never declare any message a "first" of anything.
7. spirits[] may only contain spirit_ids that already have a file in /spirits/ per the index. If a message mentions a spirit with no file, leave them in the body and keywords and flag it in the report.
8. medium field is a plain "First Last" name, no honorifics.
9. When you are uncertain about ANY judgment, choose the conservative option and flag it in the report. In this batch workflow, flagging replaces asking.

Your first task, before any cataloguing: read the attached Word document and produce an INVENTORY ONLY. For each message you find, list: proposed message_id (per the schema ID pattern, checking llms.txt and the other inventory entries for collisions), title (mark with * if you had to create one), spirit, medium, date, location, and approximate word count. Flag any message where the boundaries are unclear (where one message may have bled into another), any missing header fields, any duplicate of a message already in llms.txt, and any message whose spirit or medium has no existing file.

Do not create any files yet. Show me the inventory and wait.

---

## PROMPT 2 — Confirm inventory (after you review and correct the list)

The inventory is confirmed [with these corrections: ...]. Before we begin processing, restate in your own words: the five hard caps you will enforce with code, what goes in the notes field, and what you will do when uncertain. Then wait.

(This restatement step is cheap insurance that the rules survived into working memory.)

---

## PROMPT 3 — Process a batch (repeat this prompt for each batch)

Process the next 5 messages from the confirmed inventory, one at a time, completely, before moving to the next. For each message:

1. Extract the body text exactly, preserving paragraphs and italics.
2. Apply the full workflow from project-instructions.md steps 2-9.
3. Since these transcripts are not yet verified against any published source: set canonical_url: "" and add "Not publicly posted online." to notes. I will replace these for any message I find published.
4. Validate the finished file with code: YAML parses, all caps pass, all subjects exist in subjects.yml, spirits[] entries all exist in the spirit index, no em dashes anywhere in the file.
5. Save the file as outputs/messages/{message_id}.md

Do NOT edit any existing file. Instead, stage proposals:

- outputs/REVIEW.md (append per message): text corrections made silently (each one listed); flags needing my decision (grammar, fragments, ambiguous subjects, message_type edge calls, essential_teachings suggestions, spirits without files); proposed related_messages with the exact reciprocal lines I would paste into the other files, in chronological position.
- outputs/chains-proposed.md (append per message): draft chain entries in the exact format of chains-log.md, each line tagged [batch-proposed]. Use the thread registry and design blocks in chains-threads.md to choose roles. If a message seems to warrant a new thread or holding-pen candidate, describe it here; do not mint anything.
- outputs/spirit-updates-proposed.md: for any biographical detail a message reveals about a spirit, the exact notes text I would add to that spirit's file, citing the message_id. For any new spirit or medium a message requires, a complete draft file, clearly marked DRAFT.

After the batch of 5, stop and give me a one-paragraph summary of the batch and anything that worried you. Wait for me to say continue.

---

## PROMPT 4 — Session wrap (paste at the end of a Cowork session)

Produce outputs/MANIFEST.md: every file created this session, the message ids processed, the ids remaining in the inventory, and every unresolved flag from REVIEW.md in one list. Note anything about this batch that the next session should know.

---

## Your review loop (for you, not for Opus)

For each batch: read REVIEW.md flags and decide them; check each message against the online archive and set canonical_url where published (removing the "Not publicly posted online." note); paste reciprocal lines into the existing files; review chains-proposed.md and merge approved entries into chains-log.md (removing the [batch-proposed] tag; keep the log's chronological placement); apply approved spirit updates; run validate_messages.py; commit. Any judgment you want a second opinion on, bring back to this project.
