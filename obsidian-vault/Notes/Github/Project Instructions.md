# Divine Love Messages Archive — Project Instructions

# For use as project knowledge in Claude conversations

# Last updated: 2026-08-12

# THE REPOSITORY IS CANONICAL. These instructions carry only what the repo

# cannot: session workflow, collaboration preferences, and current state.

# All cataloguing conventions live in the repo and are followed from there.

---

## Canon (single sources of truth)

- **`schema/schema.md`** — ALL cataloguing conventions: field semantics, text handling, curator style, the door standard, subjects policy, translations. Follow it exactly. If anything here appears to conflict with schema.md, schema.md wins (and flag the conflict).
- **`schema/message.schema.yml`** — machine-validated structure and caps (description 600 max; excerpt aim under 200, 300 hard max; door 300 max).
- **`metadata/subjects.yml`** — the subject vocabulary. Validate every subject value against it with code before finalizing; never from memory.
- **Collection and essential-teaching definitions** live in the DESCRIPTIONS dicts inside `.github/scripts/generate_collections.py` and `generate_essential_teachings.py`. The `content/collections/` and `content/essential-teachings/` folders are generated output; never read them as a source.
- **`spirits/*.yml`** and **`mediums/*.yml`** — biography and doctrine. When a message reveals biographical detail, update the file in the same session, citing the source message_id; never infer beyond what is stated. Ask before creating a new spirit or medium file (one may already exist).
- **`metadata/chains-threads.md`** and **`metadata/chains-log.md`** — the chains layer. Their shared front-matter design blocks are the chain rules: role sections in argument order, chronological within each section, one anchor per section, witnesses included rather than discarded, [back-search] roles provisional until confirmed at full text. Build the `chains/` directory only after the archive is caught up through 2026.
- **Retrieval caution:** project-knowledge search can return stale chunks of repo files. Files uploaded or pasted in the session, and the live published site, take precedence over retrieved chunks. Before reporting a suspected error in a repo file based on retrieval, ask the curator to confirm against the actual file.

## Workflow (per message)

For published messages: the curator sends the URL; fetch and verify against the published text before processing. For unpublished messages: the curator pastes the text with a header block (title, spirit, medium, location, date); leave `canonical_url: ""` and add "Not publicly posted online." to notes.

1. Check the message_id for collisions against the existing index
2. Review the message text per schema.md Text Handling (report corrections in chat; flag grammar, fragments, and punctuation for approval)
3. Determine message_type (exactly one; Teaching reserved for structured doctrine; when in doubt between Blessing and Guidance, choose Guidance)
4. Assign essential_teachings if warranted (sparingly)
5. Assign collections (biblical-figure and Jesus rules per schema.md 4b)
6. Write description, excerpt, door, questions, keywords
7. Identify related_messages (subject-only, sparing, chronological)
8. Validate all subjects against subjects.yml and all field caps with code
9. Create the .md file: YAML front matter + full message text
10. Update spirit files for any revealed biography (same session, cite source)
11. Add any named spiritual Law as a secondary subject immediately
12. Provide reciprocal related_messages links as full field blocks, inserted in chronological position (sort existing out-of-order lists on touch)
13. Log to chains-log.md (and update chains-threads.md) when the message warrants it — members, witnesses, or NOTE-level sightings
14. Batch commit approximately every five messages

## Collaboration preferences

- Surface judgment calls (message_type edge cases, collections, essential_teachings, chain roles, possible anchors) with reasoning; apply schema-resolved decisions without narration
- Report body-text corrections in chat, not in the notes field
- Chain reasoning is always explained; pattern-level observations (thread candidates, missing witnesses, structural drift) are raised proactively
- All output files go to `/mnt/user-data/outputs/`
- Confirm every description, excerpt, and door fits its cap with code before delivering
- Provide reciprocal related_messages lines explicitly in chat so the curator can paste them
- Session handoff: the curator commits all files, then re-pastes these instructions, subjects.yml, chains-log.md, and chains-threads.md at the start of the next session

## Current state

- Processing position: not a single frontier. The sequential catch-up is filling the 2016 backlog (batches currently at 2016-09-02); messages from later years are catalogued as they surface, so the archive already holds material through 2023 (latest: 2023-02-10-af-augustine). Check the index for collisions rather than assuming a message is unprocessed because of its date
- Archive spans 1963-2023; earliest message 1963-12-26-ds-mary (earliest member of any chain, via who-jesus-was)
- 32 minted threads (`portals` minted 2026-08-06, most recent); 14 candidates in the holding pen
- Active workstream: the [back-search] confirmation pass. 41 of the original 49 entries still carry the tag; each is read in full, its role confirmed or upgraded, evidence prose added, and the tag removed. Highest-value remaining are the anchors and presumptive anchors: 2015-03-29-af-seretta-kem, 2015-05-03-af-confucius, 2017-06-15-af-augustine, 2018-07-19-af-matthew, 2018-09-01-af-augustine, 2018-10-16-af-seretta-kem
- Portal watch closed 2026-08-06 on the minting of `portals`; portal sightings continue as ordinary thread traffic (2016-03-25 loose → 2016-08-25 established → 2018-11-21 and 2019-01-26 doctrine → 2019-04-06 boundary)
- Mediums on file: Al Fike (af), Maureen Cardoso (mc), Dr. Daniel Samuels (ds), Jimbeau Walsh (jw), anonymous (xx)
- New spirit file: sri-yukteswar (Yogananda's guru; channels later, distinct from sri-yarisupta)
- Kay Dunbar (passed 2019-04): mother of Jeanne Fike (wife of Al Fike) and Judy Dunbar; her "dear Albert" is Al Fike; watch for her later message through him
- Subject vocabulary: 116 names; CI validates every subject and prints a usage census on every push

## Deferred / pending

- audio_url to be populated as recordings are found
- Possible tenth collection for children/the young (Children & Future Generations subject exists; watch volume)
- Usage census data to inform a possible future merge of the two Surrender subjects
- Keyword frequency analysis (curator's Obsidian note): hub pages for 5+ frequency keywords if warranted
- The who-jesus-was Foundation anchor is a three-way build-time choice (1963-12-26-ds-mary, 2018-11-26-af-jesus, 2019-01-27-af-jesus)
- The `two-paths` Capstone is a two-way build-time choice (2016-05-02-af-andrew, which holds the role, and 2018-05-12-af-luke, which names the at-onement gate)
- Natural-love rehabilitation watch stands at three instances; a fourth triggers qualifying clauses on the `two-paths` spine and the `earth-conditions-and-prayer` remedy wording
- Obsidian vault: regenerate with `python .github/scripts/generate_vault.py` after commits; vault is derived and disposable; .obsidian/ and Notes/ are preserved; obsidian-vault/* is gitignored except Notes/