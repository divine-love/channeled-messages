# Chains Layer Handoff

State as of 2026-11-03. Read this before any work on `metadata/chains-log.md` or `metadata/chains-threads.md`.

## Starting a session

1. Work from the curator's committed files, never from memory or from project-knowledge search chunks, which can be stale. Ask for the current `chains-log.md` and `chains-threads.md` at the start, or pull the repo when it is attached, and diff any copy against them before delivering changes. If the curator has not yet committed the last delivered files, build on those files, not on GitHub.
2. Run `python .github/scripts/validate_chains.py` (from anywhere in the repo) before and after every change. The ledger says what moved.
3. Anything the curator needs to see goes in the reply itself. Output printed inside a tool step is not visible to them.
4. Preserve line endings. In Python, open both files with `newline=''` on read and write. `Path.read_text` and `write_text` convert line endings silently and would rewrite every line of the file.
5. Commit text fixes and validator changes together, or the build fails on the gap between them.
6. When rewrapping roster prose, keep each section label (Foundation, Elaborations, Witnesses, Fences, What is awaited, Structural note and the rest) at the start of its own line. A line ending in a closing quote (`."`) is a sentence end too.
7. Anything in quotation marks in the log or a roster is the message's own words. Check every quote against the message text before delivering, and check again after any approved body-text edit: a log quote taken before an edit no longer matches the message once the edit is made (2016-12-08-af-augustine, "each and every one", was caught this way; 2017-04-20-af-augustine's "has been praying" and "No, my beloveds," were updated the same way).
8. Log lines start at column 0. A heading or NOTE line pasted with leading spaces breaks the build; check new entries for indentation before delivering.
9. Delivery: chains changes go to the curator as paste blocks with exact insertion points (the heading or line to insert after and before), not as zips or whole files, unless she asks for a batch.
10. After the curator commits, check that each delivered paste landed as delivered. A roster paste once replaced the `divine-love-mediumship` witness line with Patterns text; it was found only by diffing every delivered roster change against the repo, and repaired with paste blocks.
11. `last_updated` must be a zero-padded ISO date (`2026-11-01`, not `2026-11-1`). The validator fails the build otherwise.

## Reviewing a message already in the archive

The curator often asks for the chains on a message that was catalogued before the current rules. Read it in full, propose the log entry and any roster changes, and bring the file up to the current rules in the same pass:
- em dashes removed from curator fields
- an excerpt that paraphrases or joins sentences replaced with an exact quote
- notes that assert beyond the text, or that report body-text corrections, trimmed (corrections go in chat)
- a bare `gathering:` set to `""`, unless the message has a gathering
- the door ends with a full stop
- related lists sorted by date; links that share only a spirit, a setting or general encouragement dropped, since links are subject-specific only; links added where a message shares the subject closely
- message_type, primary subject, essential_teachings and missing Law subjects checked against their definitions

Body-text items still need the curator's approval. Give reciprocal blocks for every added link; a dropped link needs removing at the other end only if it was reciprocated.

## Standing rulings

These are the curator's rulings. Most are written into the design blocks of the two files. The reasoning is recorded here so it is not lost.

**The archive is mutable.** Messages arrive out of order, at both ends and in the middle, and role assignments stay provisional until a chain is built. So an entry states what its thread argues, never how much of it has been found, and the AI never interprets messages by quantity. In rosters and log records this rules out:
- counts of members, roles, messages, witnesses, spirits or instances
- spans of years
- rank claims (earliest, latest, fullest, clearest, strongest), including the hedged form "in hand", which is still a rank against a growing set
- claims about the whole set ("no other member carries this", "the thread lacks", "every other entry", "unusually for the thread", "so far", "otherwise only"); state the new facet positively, against a named message where a comparison helps
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

**Log order.** Entries are chronological by message date, and entries sharing a date go alphabetically by message_id (2016-12-10-af-andrew before 2016-12-10-af-james). Messages are not catalogued in date order, so a new entry is inserted at its position, not added at the end. One record per line; records are never wrapped. A message may carry more than one line for the same thread and role when each line covers a different passage; they count as one role, read in the order the lines give.

**Log headings** are `### message_id | title | date`, with the title exactly as in the message file. The medium is carried by the message_id and is not tagged in the heading. Whether a message is posted online is not tagged either; `canonical_url` in the message file records that.

**NOTE vocabulary.** Exactly six kinds:
- `(witness, `slug`)`, `(sighting, `slug`)`, `(considered and set aside, `slug`)`: grades the message as evidence for a thread. Working distinction: a witness states a step of the thread's argument without developing it; a sighting touches the thread's territory or wording without stating its argument. Notes for holding-pen candidates are sightings. The validator requires exactly one slug in the parentheses and nothing after it, so a role that was considered goes in the prose: `NOTE (considered and set aside, `slug`): considered as a Chrysalis. ...`
- `(build, `slug`)`: addressed to whoever builds that thread (a tension, a fence, a caveat about the text, an open anchor question, a pairing to read together)
- `(pattern, described and not penned)`: a recurring observation not yet a candidate thread, including the lattice of Light material
- `(context)`: bears on no thread (medium or spirit biography, family relationships, paired receptions, unidentified spirits, practice files, the setting of a message, collection questions, subject-level connections)

A note touching several threads is split into one NOTE per thread. Notes made redundant by a later role line are kept as `build` notes, not deleted.

**Chrysalis.** The role is for a message that describes the transformed state itself, from within or as it stands, not one that forecasts what will follow a step. Elaboration had become the default for such passages, so whenever a message describes the transformed state, ask whether it is a Chrysalis and flag it to the curator rather than defaulting to Elaboration. A forecast is logged as considered and set aside (2016-12-10-af-james, "you will walk with a new stride", for `vanguards-of-change`). Chrysalis roles on file: `bell-toll-instrumentality`, `mind-vs-soul` (two lines) and `soul-faculties`.

**Roster headings.** Each roster sits under its own `### slug` heading, so it can be found and linked; the validator accepts the headings.

**Roster entries** follow the shape in the chains-threads design block: an opener naming the thread and its arc, then role sections in argument order (facet groups allowed within a section), then Witnesses, Fences, What is awaited, Structural note, in that order. Sightings stay in the log, except where one marks a thread's boundary. A message named in a roster as a member or witness should have a log entry that agrees with it. Rosters are alphabetical, and so is the holding pen. When a roster's single "Witness." gains a second message, the label becomes "Witnesses." A new role section goes after the role sections that come before it in argument order (an Objection-removed after the Elaborations, before the Witnesses).

**Prayer files.** Spirit-given prayers, including prayers a spirit offers for the circle and words a group is given to say together, get a practice file (`content/practices/prayer-{message_id}.md`, template in `content/templates/prayer-template.md`, checked by `validate_prayers.py`), and the log carries a context note pointing to it. Two kinds of words get no practice file, and the log's context note says why: a declaration the seeker is given to affirm rather than a prayer addressed to God (2016-12-02-af-jesus, "I am a child of God"), and a prayer the circle already says that a spirit quotes rather than gives (2016-12-05-af-augustine, "Dear Father make me an instrument of your peace, a channel of your love"). Where one message gives several lines of the same prayer, one practice file holds them (2017-04-20-af-augustine). Prayer files show their title as a heading in the Obsidian vault, through `add_title_heading` in `generate_vault.py`.

**Questions in message files** never imply something the messages deny for the Divine Love path. For example, a question must not suggest that a soul far enough along that path could fall back into darkness.

**Posted or not.** `canonical_url` alone records whether a message is posted online: blank means no known public URL. The notes field does not carry "Not publicly posted online.", because messages are still being posted and the note goes stale.

**Direct Voice.** Messages received while the Direct Voice circle sits, praying for the physical manifestation of celestial spirits, carry `gathering: "Direct Voice"` (source titles mark them "(DV)"). It is provenance, not content: it is not a subject or a keyword, and the Direct Voice subjects stay for messages about the gift. A Direct Voice sitting held during a retreat takes the retreat name as its gathering and records the Direct Voice setting in notes. The vault now shows any gathering in the byline under the title, since Publish hides properties and notes are not written to the message page. The log needs no context note for the setting.

**Thread scope rulings.**
- `divine-accompaniment` (pen; replaced `angelic-accompaniment`) is one argument in steps: the soul that earnestly seeks Divine Love is accompanied from spirit, and how closely depends on how it seeks. Help comes on the asking (an angel sent in answer to a request). Earnest prayer for the Love brings an angel close, one God assigns to each earnest soul and present when it prays, not necessarily at other times. Those who keep praying for the Love are promised a standing accompaniment in their lives; promises worded as "always" or "in your life" (2018-07-07-af-aaron, 2019-02-18-af-augustine) are personal to that company, not addressed to everyone in the world. And Jesus assigns Celestial spirits as guides to mortals who walk the path of Love (2019-01-30-af-seretta-kem). Fence against the assistance gate in `free-will-and-self-responsibility`.
- `two-paths` includes natural love as a gift from God whose road leads to real harmony and joy: the roads differ in how far they reach, not in whether the love is good. This is a step in the registry spine, carried by an Objection-removed section (anchor 2016-09-02-af-augustine).
- `soul-purpose-emergence` covers a purpose designed by God, the soul's commitment to it made before birth, and growing into a purpose already seen as well as coming to know it. A place within a collective work belongs to `vanguards-of-change`. The purpose can surface on the natural love path as well as the Divine, so the registry does not make the Love its cause: members that name the Love give it as what makes the purpose clearer, and 2016-11-29-af-care has the plan unfold without naming it.
- `vanguards-of-change` now has an Objection-removed section: 2016-12-10-af-james clears the belief that answering the call costs the people who depend on you. 2016-05-12-af-alec-gaunt gives the same assurance in one sentence and stays an Elaboration.
- `no-turning-back` (pen): once a soul has received enough Divine Love on the Divine Love path it cannot fall back into darkness; a soul with natural love only can fall from however high it has risen (the first parents at 2016-05-29-af-aman). Mint when a message states the threshold itself rather than promising the seekers they cannot turn back.
- `the-whole-requirement` (pen) stays open until a message settles it beyond doubt. 2016-11-29-af-judas promises provision, but for hard encounters with people rather than for an undertaking, so it is recorded as not the settling case.
- `healing-channel` is a channel for healing; a channel of Love with no healing language is set aside (2016-11-26-af-andrew).
- `love-the-greatest-influence` (pen): many influences act on a person (planets, the Earth, other people's thoughts, parents, spirit), and the Divine Love, once received, becomes the greatest of them. Seen at 2017-03-09-af-aekarius (the ranking) and 2017-01-16-af-keea-atta-kem (protection only). Mint when a message develops the ranking of influences rather than promising protection.
- `unique-in-harmony` (pen): souls of every tradition who come to the Love keep their distinctness, and the differences joined in harmony make the Truth fuller rather than divide it. Seen at 2017-05-13-af-yogananda (stated) and 2018-08-01-af-andrew (developed from the Celestial Heavens; that message has no log entry yet and should get one at its turn, from a full reading). Fenced from `divine-love-without-knowing`, `judgment-to-love` and `religious-error`. Mint when a message develops why the differences enrich rather than only affirming them.

**Patterns.** The lattice of Light stays a pattern, not a thread (curator's ruling); 2016-12-21-af-jesus and 2017-02-12-af-augustine added its direction and its mechanism, and the thread-or-layer decision is made at build. A second pattern is recorded, testing the truth against God rather than against other people (2016-12-28-af-alec-gaunt, 2017-01-04-af-james, 2018-08-06-af-solomon, 2019-01-30-af-jesus), touching `divine-love-mediumship` and `spiritual-fellowship` without belonging to either.

## The validator

`.github/scripts/validate_chains.py`, stdlib only, with its own workflow `.github/workflows/validate-chains.yml` triggered by changes to either chains file or the script. Every message names the file and line.

**Hard checks (any occurrence fails the build):** both files carry an ISO `last_updated`; the registry and rosters are alphabetical and every roster has a registry row; every slug in the log is in the registry or the holding pen; one record per line; entries chronological with no duplicate message_id; role lines match `- `slug` **[Role]** : ` and use the seven link roles; every NOTE uses one of the six kinds, with exactly one slug where the kind takes one.

**Debt counters** (fail only if a count rises above its baseline), as of 2026-11-03: all nine at 0, including `minted_without_roster`. Every minted thread has a roster, so a newly minted thread needs its roster in the same commit. The last run checked 287 log entries and 42 rosters.

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
10. **Roster messages without log entries.** Read in full and logged: 2016-03-30-af-augustine (`religious-error` Testimony, now also in that roster's Testimony section, plus a `mind-vs-soul` witness), 2015-08-13-af-jesus (`who-jesus-was` witness), 2015-12-21-af-peter (`prayer-changes-world-conditions` and `preparation-to-be-a-rock` witnesses), 2015-11-02-af-augustine (`challenges-as-blessings` and `free-will-and-self-responsibility` witnesses), 2018-08-06-af-solomon (`mind-vs-soul` witness; a `challenges-as-blessings` sighting, since it says life tests the soul without saying the testing strengthens it). Messages still named in rosters without a log entry are named deliberately as not admitted, considered and not logged, or checkpoints: 2016-03-13-af-faith-nyquist, 2016-03-25-af-mary, 2017-12-12-af-seretta-kem, 2018-03-13-af-jesus. (2017-01-23-af-alec-gaunt has since been read and logged.)
11. **Open questions settled** (see Thread scope rulings). `angelic-accompaniment` became the wider `divine-accompaniment` pen candidate, with sightings at 2014-07-26-af-augustine, 2016-05-30-af-augustine, 2016-09-10-af-andrew, 2016-10-26-af-augustine, 2017-05-11-af-jesus, 2018-07-07-af-aaron (newly logged), 2019-01-30-af-seretta-kem, 2019-02-18-af-augustine, 2019-02-21-af-elijah and 2019-02-27-af-andrew. `two-paths` gained the natural-love step and an Objection-removed section (2016-09-02-af-augustine anchor, 2018-05-12-af-luke member); 2016-08-27-af-brother-mandus became a witness. `soul-purpose-emergence` spine now includes the God-designed purpose, the commitment before birth and the growing-into; 2016-10-15-af-confucius gained a `vanguards-of-change` witness for its place in the collective work. 2016-11-26-af-andrew set aside from `healing-channel`. 2019-02-21-af-elijah became a `preparation-to-be-a-rock` witness. The armour-of-the-world build notes stay as context.
12. **2016-12-02-af-white-cloud** logged at its date's position.

Prayer files added during the cleanup: 2015-08-17-af-jesus, 2016-01-04-af-seretta-kem, 2016-02-29-af-confucius, 2017-01-25-af-alec-gaunt; prayer-2016-09-08-af-jesus restored after it had been overwritten; prayer-2018-05-21-af-matthew renamed with its `af`.

The Obsidian vault generator now links thread slugs written in backticks (in log prose and in "The argument it traces") to their chain hubs.

## Since the last handoff

**Catalogued and logged**, each from a full reading with quotes checked: 2016-12-12-af-augustine, 2016-12-21-af-alec-gaunt, 2016-12-21-af-jesus and 2016-12-28-af-alec-gaunt; 2017-01-02-af-seretta-kem, 2017-01-04-af-james, 2017-01-11-af-luke, 2017-01-15-af-peter, 2017-01-30-af-augustine, 2017-02-12-af-augustine, 2017-02-15-af-confucius, 2017-02-23-af-andrew, 2017-03-05-af-luke, 2017-03-08-af-confucius, 2017-03-09-af-aekarius, 2017-03-30-af-jesus and 2017-04-20-af-augustine (Direct Voice).

**Archived messages reviewed and logged**, with their files brought up to the current rules: 2017-01-02-af-jesus, 2017-01-16-af-keea-atta-kem, 2017-01-23-af-alec-gaunt, 2017-01-25-af-alec-gaunt, 2017-03-27-af-james, 2017-04-10-af-james and 2017-05-13-af-yogananda.

**Prayer files added:** 2016-12-09-af-martin-luther ("Father, Use Me as Your Channel of Love"), 2017-01-30-af-augustine, 2017-03-05-af-luke and 2017-04-20-af-augustine ("I Lay Down My Will for Your Will").

**Repairs:** the `divine-love-mediumship` witness line overwritten by a paste (see Starting a session, item 10); duplicate `related_messages:` keys in 2017-09-13-af-keea-atta-kem, 2018-09-30-af-augustine and 2019-03-13-af-stephen; an empty placeholder file for 2017-02-23-af-andrew.

**Build notes worth knowing before a build:**
- `preparation-to-be-a-rock`: if a Capstone is wanted, weigh 2017-04-20-af-augustine ("essentially you have come to a place where you are ready") with 2018-09-01-af-seretta-kem's readiness turn.
- `divine-love-without-knowing`: Yogananda's messages, read together, give the thread's run within one life (the Love known within his own tradition at 2017-05-13-af-yogananda and 2019-04-01-jw-yogananda, the Celestial Kingdom reached in spirit at 2018-11-22-af-yogananda). Weigh whether they form a Testimony section.
- `religious-error`: 2017-05-13-af-yogananda holds that the root of his teaching was the Truth of God's Love, so it belongs beside his later reincarnation corrections at build, to keep them from reading as a disowning of everything he taught.

New spirit file: `aekarius`.

## Next

Three steps, in this order:

1. **Close the 2016 backlog.** The sequential catch-up has catalogued through the end of 2016 and moved on into 2017 (latest 2017-04-20-af-augustine). What remains is chains reading of 2016 messages catalogued before the chains layer that carry no log entry. Some may warrant none, but nothing records whether they were read for chains, so each needs a full reading and either an entry or a decision that it needs none: 2016-01-04-af-confucius, 2016-01-09-af-augustine, 2016-01-09-af-confucius, 2016-01-09-af-faith-nyquist, 2016-01-11-af-matthew, 2016-01-13-af-andrew, 2016-01-18-af-mary, 2016-01-25-af-peter, 2016-01-26-af-john-the-beloved, 2016-02-15-af-confucius, 2016-03-06-af-goldie, 2016-03-07-af-victor-summers, 2016-03-12-af-faith-nyquist, 2016-03-12-af-james, 2016-03-13-af-faith-nyquist, 2016-03-14-af-mary, 2016-03-21-af-augustine, 2016-03-25-af-mary, 2016-03-26-af-andrew, 2016-03-26-af-goldie, 2016-03-30-af-alec-gaunt, 2016-03-30-af-confucius, 2016-03-30-af-faith-nyquist, 2016-03-31-af-mary, 2016-04-04-af-jesus, 2016-04-04-af-keea-atta-kem, 2016-04-05-af-gandhi, 2016-04-12-af-augustine, 2016-04-13-af-confucius, 2016-04-14-af-john-the-beloved, 2016-04-14-af-mary, 2016-04-19-af-augustine, 2016-04-27-af-alec-gaunt, 2016-05-11-af-jesus, 2016-06-13-af-james, 2016-06-27-af-brother-mandus, 2016-07-04-af-francis-of-assisi, 2016-07-09-af-confucius, 2016-07-10-af-augustine, 2016-08-15-af-mary, 2016-08-16-af-james, 2016-12-29-af-matthew. Five of these are named as "Seen" in holding-pen candidates without a log sighting (2016-01-09-af-faith-nyquist, 2016-01-11-af-matthew, 2016-03-12-af-james, 2016-03-14-af-mary, 2016-07-04-af-francis-of-assisi); 2016-03-13-af-faith-nyquist and 2016-03-25-af-mary are named in rosters deliberately (see the punch list, item 10). In 2017, 2017-05-22-af-andrew is the next archived message without a log entry. Keep watching for messages that develop `divine-accompaniment` rather than asserting a step of it, and for possible Chrysalis passages (see Chrysalis above).
2. **Chrysalis audit**, before the split. Review about a dozen threads whose arcs end in a transformed state and list candidate passages for the curator's ruling. Candidates already noted: `soul-expiation` (the end state in 2016-05-16-af-keea-atta-kem, and the "new creature" in 2016-12-08-af-confucius); `fear-of-full-immersion`, which awaits one; `knowing-your-own-soul`.
3. **Split the chains files**, after the 2016 chains reading; the curator decides whether to split before continuing with 2017. The log goes by year (`metadata/chains-log/2016.md` and so on) and the rosters become one file per thread. The split must update `validate_chains.py`, `generate_vault.py`, the design blocks, this doc and schema.md together, in one commit.

Standing watch, `vanguards-of-change`, What is awaited. The things to give up read as a series, each closer to the self than the last: possessions (2016-03-06-af-jesus), one's own plans (2016-08-27-af-augustine), one's own needs (2016-09-16-af-john-the-beloved), and the safety of the loving circle (2016-12-05-af-augustine). 2016-12-10-af-james restates the plans step ("not to formulate plans and ideas that are purely of your mental imaginations and ambitions") without carrying it further, and 2017-04-20-af-augustine joins it to security ("ideas and dreams that I have concocted to give me a sense of security"); both lean toward one idea restated. A message that names the series, or carries it further, may settle the question.

## Open questions awaiting the curator

- In 2017-05-13-af-yogananda, is "J W" Jimbeau Walsh? Yogananda tells him, "I am with you often and we have many conversations in spirit as you sleep." If so: "Jimbeau Walsh" goes in `people`, a `divine-love-mediumship` witness goes into that log entry (an earlier sign of the rapport 2019-04-01-jw-yogananda describes), and the line goes in the Yogananda spirit file.
- Earlier Direct Voice messages: 2017-04-20-af-augustine is the only message marked so far. If source titles carry "(DV)" elsewhere, a sweep would set the gathering on each.

The Open questions section of `chains-threads.md` holds the longer-running ones (the fence between `prayer-changes-world-conditions` and `bell-toll-instrumentality`, the consequences of two promotions, a minted thread's image returning with the opposite meaning, the `free-will-and-gods-plan` connection, anchoring below the whole message, two possible collections, and the fence test case recorded there). The `earth-conditions-and-prayer` remedy wording is settled at build, per that roster's structural note.