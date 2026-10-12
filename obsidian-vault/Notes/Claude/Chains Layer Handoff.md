
State as of 2026-10-12. Read this before any work on `metadata/chains-log.md` or `metadata/chains-threads.md`.

## Starting a session

1. Work from the curator's committed files, never from memory or from project-knowledge search chunks, which can be stale. Ask for the current `chains-log.md` and `chains-threads.md` at the start, and diff any copy against them before delivering changes. If the curator has not yet committed the last delivered files, build on those files, not on GitHub.
2. Run `python .github/scripts/validate_chains.py` (from anywhere in the repo) before and after every change. The ledger says what moved.
3. Anything the curator needs to see goes in the reply itself. Output printed inside a tool step is not visible to them.
4. Preserve line endings. In Python, open both files with `newline=''` on read and write. `Path.read_text` and `write_text` convert line endings silently and would rewrite every line of the file.
5. Commit text fixes and validator changes together, or the build fails on the gap between them.
6. When rewrapping roster prose, keep each section label (Foundation, Elaborations, Witnesses, Fences, What is awaited, Structural note and the rest) at the start of its own line. A line ending in a closing quote (`."`) is a sentence end too.
7. Anything in quotation marks in the log or a roster is the message's own words. Check every quote against the message text before delivering.

## Standing rulings

These are the curator's rulings. Most are written into the design blocks of the two files. The reasoning is recorded here so it is not lost.

**The archive is mutable.** Messages arrive out of order, at both ends and in the middle, and role assignments stay provisional until a chain is built. So an entry states what its thread argues, never how much of it has been found, and the AI never interprets messages by quantity. In rosters and log records this rules out:

- counts of members, roles, messages, witnesses, spirits or instances
- spans of years
- rank claims (earliest, latest, fullest, clearest, strongest), including the hedged form "in hand", which is still a rank against a growing set
- claims about the whole set ("no other member carries this", "the thread lacks", "every other entry", "unusually for the thread"); state the new facet positively, against a named message where a comparison helps
- claims that nothing is logged between two points
- intervals between messages ("three weeks earlier", "predates it by two years", "earlier in date than", "the next day"); the message_ids carry the dates
- intervals measured against a role ("three weeks before the Foundation"), since the role can move
- watches that wait on a count ("settle when a third message arrives", "look for a second instance"); write "a message that develops X" instead
- stale states ("the anchor is still awaited", "not yet logged", "anchors the new thread")

Instead, state the relation between named messages: one develops what another asserts, answers it, or repeats it without developing it. A count of passages inside one fixed message is fine, because a message's text does not change.

**The log is the history of the messages, not the history of the log.** No mint dates, pen dates, session or reading dates, or curator attributions in records. Where a standing ruling governs a decision, name it descriptively ("the argument-not-image ruling"), never by the date it was made. A roster entry likewise explains its thread, never its own existence. Essential-teaching labels (Core Teaching, Spirit Biography and the rest) live in the message files, not in the log or the rosters.

**Full reading only.** Every log entry is made from a full reading of the message, never from its description or summary. The old `[back-search]` tag, for entries logged from a description, is retired: those entries proved unreliable (paraphrases and invented lines presented as quotes), all of them were read in full and rewritten, and the tag was removed from the log, the rosters' design block, the vault generator and the project instructions.

**Voice.** Curator notes are impersonal: no "I", "my reading", or "JUDGMENT CALL". A question left for the builder reads "open question for build:". Recommendations addressed to the curator belong in Open questions in chains-threads, not in the log.

**Plain language.** All curatorial prose, including notes meant only for a builder, is written so anyone can understand it. Simpler wording, not dumbed down, and no jargon standing between the reader and the meaning.

**Log order.** Entries are chronological by message date. Messages are not catalogued in date order, so a new entry is inserted at its date's position, not added at the end. One record per line; records are never wrapped. A message may carry more than one line for the same thread and role when each line covers a different passage; they count as one role, read in the order the lines give.

**Log headings** are `### message_id | title | date`, with the title exactly as in the message file. The medium is carried by the message_id and is not tagged in the heading. Whether a message is posted online is not tagged either; `canonical_url` in the message file records that.

**NOTE vocabulary.** Exactly six kinds:

- `(witness,` slug`)`, `(sighting,` slug`)`, `(considered and set aside,` slug`)`: grades the message as evidence for a thread. Working distinction: a witness states a step of the thread's argument without developing it; a sighting touches the thread's territory or wording without stating its argument. Notes for holding-pen candidates are sightings.
- `(build,` slug`)`: addressed to whoever builds that thread (a tension, a fence, a caveat about the text, an open anchor question, a pairing to read together)
- `(pattern, described and not penned)`: a recurring observation not yet a candidate thread, including the lattice of Light material
- `(context)`: bears on no thread (medium or spirit biography, family relationships, paired receptions, unidentified spirits, practice files, collection questions, subject-level connections)

A note touching several threads is split into one NOTE per thread. Notes made redundant by a later role line are kept as `build` notes, not deleted.

**Roster entries** follow the shape in the chains-threads design block: an opener naming the thread and its arc, then role sections in argument order (facet groups allowed within a section), then Witnesses, Fences, What is awaited, Structural note, in that order. Sightings stay in the log, except where one marks a thread's boundary. A message named in a roster as a member or witness should have a log entry that agrees with it. Rosters are alphabetical.

**Prayer files.** Spirit-given prayers, including prayers a spirit offers for the circle and words a group is given to say together, get a practice file (`content/practices/prayer-{message_id}.md`, template in `content/templates/prayer-template.md`, checked by `validate_prayers.py`), and the log carries a context note pointing to it.

**Posted or not.** `canonical_url` alone records whether a message is posted online: blank means no known public URL. The notes field does not carry "Not publicly posted online.", because messages are still being posted and the note goes stale.

**Thread scope rulings.**

- `divine-accompaniment` (pen; replaced `angelic-accompaniment`) is one argument in steps: the soul that earnestly seeks Divine Love is accompanied from spirit, and how closely depends on how it seeks. Help comes on the asking (an angel sent in answer to a request). Earnest prayer for the Love brings an angel close, one God assigns to each earnest soul and present when it prays, not necessarily at other times. Those who keep praying for the Love are promised a standing accompaniment in their lives; promises worded as "always" or "in your life" (2018-07-07-af-aaron, 2019-02-18-af-augustine) are personal to that company, not addressed to everyone in the world. And Jesus assigns Celestial spirits as guides to mortals who walk the path of Love (2019-01-30-af-seretta-kem). Fence against the assistance gate in `free-will-and-self-responsibility`.
- `two-paths` includes natural love as a gift from God whose road leads to real harmony and joy: the roads differ in how far they reach, not in whether the love is good. This is a step in the registry spine, carried by an Objection-removed section (anchor 2016-09-02-af-augustine).
- `soul-purpose-emergence` covers a purpose designed by God, the soul's commitment to it made before birth, and growing into a purpose already seen as well as coming to know it. A place within a collective work belongs to `vanguards-of-change`.
- `healing-channel` is a channel for healing; a channel of Love with no healing language is set aside (2016-11-26-af-andrew).

## The validator

`.github/scripts/validate_chains.py`, stdlib only, with its own workflow `.github/workflows/validate-chains.yml` triggered by changes to either chains file or the script. Every message names the file and line.

**Hard checks (any occurrence fails the build):** both files carry an ISO `last_updated`; the registry and rosters are alphabetical and every roster has a registry row; every slug in the log is in the registry or the holding pen; one record per line; entries chronological with no duplicate message_id; role lines match `-` slug`**[Role]** :` and use the seven link roles; every NOTE uses one of the six kinds.

**Debt counters** (fail only if a count rises above its baseline), as of 2026-10-12: all nine at 0, including `minted_without_roster`. Every minted thread now has a roster, so a newly minted thread needs its roster in the same commit.

When work clears items, the script prints the new baseline to set. To get a worklist for a category, set its baseline to 0 temporarily: the run lists the items with line numbers. Restore the real count before committing.

The checks catch mechanical forms only. Ordinary-language stale claims ("the two purpose statements", "three are in hand", "the anchor is still awaited", "the thread lacks") and misquotes get past them, so the written rules above are the real protection. A pattern that flags good sentences was tried and reverted; precision matters more than coverage.

## The punch list: done

1. **C2, the log language pass.** The line-by-line record is the project doc `claude/c2-worklist.md`.
2. **chains-threads pass.** Holding pen, Patterns and Open questions restructured and cleaned; every roster brought under the rules above.
3. **E2.** Medium tags removed from log headings; log phrases the C2 pass had missed cleared; roster layout repaired.
4. **E4.** The repeated-lines rule (see Log order above).
5. **B3.** Anchors: Testimony in `two-paths` (2016-05-29-af-aman) and `religious-error` (2015-03-28-af-augustine), Reframe in `soul-expiation` (2016-03-11-af-luke), Capstone in `judgment-to-love` (2018-07-16-af-andrew).
6. **Back-search reading pass.** All 36 back-search messages read in full and rewritten; the tag is now retired (see Full reading only). `judgment-to-love` gained a Foundation (2017-06-15-af-augustine); a `religious-error` role at 2015-06-21-af-martin-luther rested on an invented sentence and was removed; three log headings had wrong titles (every heading now matches its message).
7. **Quote audit.** Every quote in the log and rosters checked against the messages. Cross-references confirmed; near-misses corrected to the message's words; paraphrases written as quotes reworded as plain prose. What remains unmatched is deliberate: single quote marks standing in for a message's own inner double quotes, a few checker misreads where quotes sit side by side, and subject or collection names.
8. **B2.** Rosters written for `death-transition`, `reincarnation-progression`, `divine-love-without-knowing`, `healing-channel` and `soul-faculties`; `self-love-foundation` rebuilt with 2016-02-29-af-confucius as Foundation. Along the way 2016-01-08-af-jesus moved from `healing-channel` Elaboration to witness, and several Foundations whose log lines had no quotes were rewritten from the message text.
9. **"Not publicly posted online." removed.** Taken out of the notes of 217 messages (112 now have empty notes) with `last_edited` untouched; `[not publicly posted]` removed from 107 log headings; the `canonical_url` row in schema.md section 4 no longer asks for the note. The project instructions and the Cowork prompt kit were updated to match, and their current-state and chains sections brought up to date.
10. **Roster messages without log entries.** Read in full and logged: 2016-03-30-af-augustine (`religious-error` Testimony, now also in that roster's Testimony section, plus a `mind-vs-soul` witness), 2015-08-13-af-jesus (`who-jesus-was` witness), 2015-12-21-af-peter (`prayer-changes-world-conditions` and `preparation-to-be-a-rock` witnesses), 2015-11-02-af-augustine (`challenges-as-blessings` and `free-will-and-self-responsibility` witnesses), 2018-08-06-af-solomon (`mind-vs-soul` witness; a `challenges-as-blessings` sighting, since it says life tests the soul without saying the testing strengthens it). Messages still named in rosters without a log entry are named deliberately as not admitted, considered and not logged, or checkpoints: 2016-03-13-af-faith-nyquist, 2016-03-25-af-mary, 2017-01-23-af-alec-gaunt, 2017-12-12-af-seretta-kem, 2018-03-13-af-jesus.
11. **Open questions settled** (see Thread scope rulings). `angelic-accompaniment` became the wider `divine-accompaniment` pen candidate, with sightings at 2014-07-26-af-augustine, 2016-05-30-af-augustine, 2016-09-10-af-andrew, 2016-10-26-af-augustine, 2017-05-11-af-jesus, 2018-07-07-af-aaron (newly logged), 2019-01-30-af-seretta-kem, 2019-02-18-af-augustine, 2019-02-21-af-elijah and 2019-02-27-af-andrew. `two-paths` gained the natural-love step and an Objection-removed section (2016-09-02-af-augustine anchor, 2018-05-12-af-luke member); 2016-08-27-af-brother-mandus became a witness. `soul-purpose-emergence` spine now includes the God-designed purpose, the commitment before birth and the growing-into; 2016-10-15-af-confucius gained a `vanguards-of-change` witness for its place in the collective work. 2016-11-26-af-andrew set aside from `healing-channel`. 2019-02-21-af-elijah became a `preparation-to-be-a-rock` witness. The armour-of-the-world build notes stay as context.

Prayer files added during the cleanup: 2015-08-17-af-jesus, 2016-01-04-af-seretta-kem, 2016-02-29-af-confucius, 2017-01-25-af-alec-gaunt; prayer-2016-09-08-af-jesus restored after it had been overwritten; prayer-2018-05-21-af-matthew renamed with its `af`.

The Obsidian vault generator now links thread slugs written in backticks (in log prose and in "The argument it traces") to their chain hubs.

## Next

- **Cataloguing resumes with the 2016 backlog after 2016-11-27-af-james-reid-2**, the last message batch-processed. Some later messages (2016-11-28 onward, and material through 2023) are already catalogued, so check the index for collisions. Log each new message at full reading, with quotes checked, and add it to the rosters it joins. Watch for messages that develop `divine-accompaniment` rather than asserting a step of it.

## Open questions awaiting the curator

None from the cleanup. The Open questions section of `chains-threads.md` holds the longer-running ones (the fence between `prayer-changes-world-conditions` and `bell-toll-instrumentality`, the consequences of two promotions, a minted thread's image returning with the opposite meaning, the `free-will-and-gods-plan` connection, anchoring below the whole message, and two possible collections). The `earth-conditions-and-prayer` remedy wording is settled at build, per that roster's structural note.