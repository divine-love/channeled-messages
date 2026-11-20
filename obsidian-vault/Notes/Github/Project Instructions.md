# Divine Love Messages Archive: Project Instructions

# For use as project knowledge in Claude conversations

# Last updated: 2026-11-20

# THE REPOSITORY IS CANONICAL. These instructions carry only what the repo

# cannot: session workflow, collaboration preferences, and current state.

# All cataloguing conventions live in the repo and are followed from there.

---

## Canon (single sources of truth)

- **`schema/schema.md`**: ALL cataloguing conventions: field semantics, text handling, curator style, the door standard, subjects policy, translations. Follow it exactly. If anything here appears to conflict with schema.md, schema.md wins (and flag the conflict).
- **`schema/message.schema.yml`**: machine-validated structure and caps (description 600 max; excerpt aim under 200, 300 hard max; door 300 max).
- **`metadata/subjects.yml`**: the subject vocabulary. Validate every subject value against it with code before finalizing; never from memory.
- **Collection and essential-teaching definitions** live in the DESCRIPTIONS dicts inside `.github/scripts/generate_collections.py` and `generate_essential_teachings.py`. The `content/collections/` and `content/essential-teachings/` folders are generated output; never read them as a source.
- **`spirits/*.yml`** and **`mediums/*.yml`**: biography and doctrine. When a message reveals biographical detail, update the file in the same session, citing the source message_id; never infer beyond what is stated. Ask before creating a new spirit or medium file (one may already exist).
- **`metadata/chains-threads.md`** and **`metadata/chains-log.md`**: the chains layer. These two files hold the rules, the registry, the holding pen, the patterns and the open questions. The log entries are in `metadata/chains-log/`, one file per year of message (`2018.md`), and each minted thread's roster is its own file in `metadata/chains-threads/`, named for its slug (`soul-expiation.md`). Their shared front-matter design blocks are the chain rules: role sections in argument order, chronological within each section, one anchor per section, witnesses included rather than discarded, every entry made from a full reading of the message. A chain follows an argument, not a timeline. Build the `chains/` directory only once the messages through 2026 are all in the archive.
- **`MAINTAINERS-GUIDE.md`**: how the whole repository fits together, written for a person taking up the work. When a script, a folder or a routine changes, check whether the guide needs to change with it.
- **Retrieval caution:** project-knowledge search can return stale chunks of repo files. Files uploaded or pasted in the session, and the live published site, take precedence over retrieved chunks. Before reporting a suspected error in a repo file based on retrieval, ask the curator to confirm against the actual file.

## Workflow (per message)

Messages are catalogued one at a time and reviewed together in conversation, not in batches. The prompts for a session are in `obsidian-vault/Notes/Claude/Claude Conversation Prompt Kit.md`.

For published messages: the curator sends the URL; fetch and verify against the published text before processing. For unpublished messages: the curator pastes the text with a header block (title, spirit, medium, location, date); leave `canonical_url: ""`. A blank canonical_url is the only record that no public copy is known; do not add a note about it to notes.

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
11. Add any spiritual Law the message uses as a working Law as a secondary subject (see schema.md, Subjects; record general mentions in metadata/law-mentions-reviewed.yml)
12. Provide reciprocal related_messages links as full field blocks, inserted in chronological position (sort existing out-of-order lists on touch)
13. Log to the message's year file in `metadata/chains-log/` (and update the thread's roster file in `metadata/chains-threads/`, or chains-threads.md for the holding pen and patterns): members, witnesses, or NOTE-level sightings, or the single line "- Read in full; joins no thread." Insert the entry at its date's position in that year's file, and check every quote against the message text. The log holds only what develops threads, never context notes: a fact about the message goes in its `notes`, a fact about a spirit or medium in that file
14. For a spirit-given prayer, create its practice file. Nothing else points to it: no note in the log and no line in the message's `notes`
15. Batch commit approximately every five messages

## Collaboration preferences

- Surface judgment calls (message_type edge cases, collections, essential_teachings, chain roles, possible anchors, a possible Chrysalis) with reasoning; apply schema-resolved decisions without narration
- Report body-text corrections in chat, not in the notes field
- Chain reasoning is always explained; pattern-level observations (thread candidates, missing witnesses, structural drift) are raised proactively
- Never commit or push. The curator reviews every change and commits it herself, because reviewing is how she stays familiar with the repo
- All output files go to `/mnt/user-data/outputs/`. Message, spirit and practice files come as downloads. Chains changes and reciprocal related_messages come as paste blocks, each naming its file and the line it goes after and before. A change that touches many files comes as one zip laid out like the repo, with a short review guide
- Confirm every description, excerpt, and door fits its cap with code before delivering
- Provide reciprocal related_messages lines explicitly in chat so the curator can paste them
- If the curator has not yet committed files delivered earlier, build on those files, not on GitHub
- Session handoff: the curator commits all files. A session that can read the repo starts from Prompt 1 of the Conversation Prompt Kit and reads the repo directly. A session that cannot read the repo needs the files listed at the end of the kit. At the end of a session, update the Chains Layer Handoff note and the project doc `claude/chains-layer-handoff.md`, and give the curator new wording for Current state

## Current state

- Order of work: messages are not added in date order. The curator chooses each message, so any year may have gaps, and messages arrive at both ends of the archive and in the middle. Never describe the work as a "catch-up" or say where it "resumes". Before cataloguing, check the index for a collision rather than assuming a message is new because of its date
- Chains reading: every message in the archive should end up with a log entry. The messages still to be read for chains are exactly those with no entry in `metadata/chains-log/`; compare the log headings with `content/messages/` to list them
- Chains layer: 44 minted threads, each with its own roster file; 19 candidates in the holding pen; 2 patterns recorded and not penned. All validator debt counters are at 0, so a newly minted thread needs its registry row, its roster file and its `CHAIN_GROUPS` entry in `generate_vault.py` in the same commit
- Chains layout (split 2026-11-14): `chains-log.md` and `chains-threads.md` hold the rules, registry, holding pen, patterns and open questions; entries are in `metadata/chains-log/` by year, rosters in `metadata/chains-threads/` by slug. `chains_io.py` reads them together for `validate_chains.py` and `generate_vault.py`. `last_updated` is carried by the two front-door files only
- Context notes are retired (2026-11-20): the log holds only what develops threads. Older context notes stay until the context-note audit moves them (see Deferred); the validator still accepts the kind until then
- Quotes in context (2026-11-14): in the unpublished Threads (working) pages, every record has a fold-out showing the paragraph its quoted words come from. `generate_vault.py` reports how many quoted passages it could not locate; that number is 0 and should stay 0. The published thread pages link to whole messages only, never to a passage, by the curator's ruling
- Read the project doc `claude/chains-layer-handoff.md` before any chains work: it carries the standing rulings (no counts, intervals or rank claims; plain language; quotes are the message's own words; the NOTE kinds), how the validator works, what was noticed and not yet dealt with, and the open questions
- No rank claims anywhere in the repository (2026-11-20): never call a message the first, earliest or latest, whether in the archive or "in hand", in notes, spirit files or the chains layer
- Subjects are subcategory names only (2026-11-20): main category names are never used as subjects. Some older messages still carry one (the subject census at the end of `validate_messages.py` counts them)
- The door is one or two sentences within 300 characters (ruling 2026-11-15)
- Direct Voice: a "(DV)" in a source title means a Direct Voice sitting. Set `gathering: "Direct Voice"` and leave "(DV)" out of the catalogued title. A Direct Voice sitting held during a retreat keeps the retreat name, with the setting in `notes`. These sittings become frequent in the later years
- Spirit-given prayers, including words a group is given to say together, get a practice file (`content/practices/prayer-{message_id}.md`, from `content/templates/prayer-template.md`, checked by `validate_prayers.py`), and nothing else points to it. Declarations to affirm, and a circle's own prayer that a spirit quotes, get no practice file
- "Not publicly posted online." is retired (2026-10-12): a blank `canonical_url` alone records that no public copy is known
- Portal watch closed 2026-08-06 on the minting of `portals`; portal sightings continue as ordinary thread traffic (2016-03-25 loose → 2016-08-25 established → 2018-11-21 and 2019-01-26 doctrine → 2019-04-06 boundary)
- Mediums on file: Al Fike (af), Barbara Davies (bd), Maureen Cardoso (mc), Dr. Daniel Samuels (ds), Jimbeau Walsh (jw), anonymous (xx)
- sri-yukteswar (Yogananda's guru) has a spirit file; he channels later and is distinct from sri-yarisupta
- Kay Dunbar (passed 2019-04): mother of Jeanne Fike (wife of Al Fike) and Judy Dunbar; her "dear Albert" is Al Fike; watch for her later message through him
- Alec Gaunt hosted Direct Voice prayer circles in his earth life, by the curator's account. His spirit file records only what messages state, so add it when a message says so
- Publishing: the site is made by Obsidian Publish from the generated vault, with `Threads (working)` and `Notes` left out; nothing is changed by hand once it is live. On the site, chains are called threads; the repository keeps its own names. The vault uses the Front Matter Title plugin (Graph feature only) and Sync Graph Settings
- Subject vocabulary: 117 names; CI validates every subject and prints a usage census on every push

## Deferred / pending

- Chains reading of the messages that have no log entry (the handoff lists the 2014 and 2016 ones)
- Context-note audit: move each older context note in the log to the message's `notes` or the spirit or medium file, drop the prayer-file pointers, then retire the `(context)` kind in `validate_chains.py`, the `chains-log.md` design block and the handoff together. Propose the moves to the curator first
- Main category sweep: give each older message that carries a main category name a subcategory instead (the subject census at the end of `validate_messages.py` shows which main category names are still used)
- Chrysalis audit (the handoff lists the candidates; `soul-expiation` holds 2018-07-14-af-seretta-kem as a candidate)
- The Cowork Prompt Kit is retired in favour of the Conversation Prompt Kit; remove it when ready
- audio_url to be populated as recordings are found
- Possible tenth collection for children and the young (Children & Future Generations subject exists)
- Usage census data to inform a possible future merge of the two Surrender subjects
- Keyword frequency analysis (curator's Obsidian note): hub pages for 5+ frequency keywords if warranted
- The who-jesus-was Foundation anchor is a three-way build-time choice (1963-12-26-ds-mary, 2018-11-26-af-jesus, 2019-01-27-af-jesus)
- The `two-paths` Capstone is a two-way build-time choice (2016-05-02-af-andrew, which holds the role, and 2018-05-12-af-luke, which names the at-onement gate)
- The `earth-conditions-and-prayer` remedy wording (daily prayer, widened by messages to love in ordinary contact, joy, and the standing alliance with Heaven) is settled once at build, per that roster's structural note
- Obsidian vault: regenerate with `python .github/scripts/generate_vault.py` after commits; vault is derived and disposable; .obsidian/ and Notes/ are preserved; obsidian-vault/* is gitignored except Notes/