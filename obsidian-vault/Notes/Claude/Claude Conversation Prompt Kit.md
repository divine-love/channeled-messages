# Claude Conversation Prompt Kit: Cataloguing One Message at a Time
## Divine Love Messages Archive

Save this file; paste the prompts as you need them. Messages are catalogued one at a time, reviewed together in conversation. This kit replaces the Cowork Prompt Kit, which was written for batches.

Last updated: 2026-11-20

---

## Before you start a session (for you)

- Commit and push everything first. Claude reads the repo as it stands on GitHub and cannot see anything that exists only on your computer.
- Start the session inside the Divine Love Messages Archive project, so the project instructions and the repo connection come with it.
- Nothing needs attaching when Claude can read the repo. If a session cannot reach the repo, use the attachment list at the end of this kit.

---

## PROMPT 1: Start of session (paste first, wait for the report)

We are continuing to catalogue messages for the Divine Love Messages archive, one message at a time, reviewing each one together. The repository divine-love/channeled-messages is canonical and is connected to this project. I review every change and commit it myself.

Before we begin, please get oriented:

1. Read the project instructions. Then pull the latest repo and read `schema/schema.md`, `schema/message.schema.yml`, `metadata/subjects.yml`, `metadata/chains-log.md`, `metadata/chains-threads.md`, and the project doc `claude/chains-layer-handoff.md`. Read year files, roster files, spirit files and messages as each message needs them, not all at once.
2. Run `validate_messages.py` and `validate_chains.py`, so we both know the starting state.
3. Then tell me, briefly:
    - the commit you are working from (its short id, date and message)
    - what the two checks reported: the message count, the log entries, year files and rosters, and any debt counter above 0
    - the `last_updated` date and the registry row count in `chains-threads.md`
    - anything in the project instructions' Current state, or in the handoff, that disagrees with the repo
    - any question you need answered before we begin

Working agreements for the session:

- **Message text is never changed without my approval.** Spacing artifacts and clear typos are fixed silently and listed in chat. Grammar, sentence fragments and punctuation are flagged, and wait for my answer.
- **Full reading only.** Every log entry and roster line comes from reading the whole message. Anything in quotation marks is the message's own words. Check every quote against the message text with code, and check again after any approved text fix.
- **Keep the chains (threads) language very simple.** Write every log entry, roster line and holding-pen note so a child could follow it: short everyday words and plain sentences. Say what the message says and why it belongs to the thread. Avoid shorthand such as "asserted rather than argued" or "given as a closed list".
- **Check with code, never from memory:** every subject against `subjects.yml`, and every subject a subcategory name, never a main category name; every cap (description 600, excerpt aiming under 200 and never over 300, door 300); no em dashes in any file; both validators before you deliver.
- **Decisions the schema settles** are applied without comment. **Judgment calls** (message_type edge cases, essential_teachings, collections, chain roles, anchors, a possible Chrysalis, a link you are unsure of) work differently: choose what you would recommend, apply it, and list each one with a sentence of reasoning so I can overrule it.
- **Raise patterns as you notice them:** a candidate thread, a missing witness, a roster out of order, a place where the repo breaks its own rules.
- **Never commit or push,** even if the environment prompts you to. Message files, spirit files and practice files come to me as downloads. Chains changes and reciprocal `related_messages` come as paste blocks, each naming its file and the line it goes after and before. When a change touches many files, give me one zip laid out like the repo, with a short review guide.
- **If I have not yet committed files you sent earlier, build on those files,** not on GitHub.
- `last_edited` uses the date in Eastern time.
- Write to me in plain language, with no em dashes. When you list a message's subjects, list them vertically, primary first.
- You can only open web pages whose address I have pasted into the chat. If you need one, ask me for it.

Then wait for the first message.

---

## PROMPT 2: A published message (one per message)

Next message: [paste the URL]

[Optional: anything you know that the page does not say, such as the gathering, who a named person is, or a correction to the header.]

Please catalogue it. Fetch the page and work from the published text. A "(DV)" in the source title means a Direct Voice sitting: set `gathering: "Direct Voice"` and leave "(DV)" out of the catalogued title. Then give me, in one reply:

1. **The message_id,** and whether it collides with a file already in the archive.
2. **Text review:** the silent corrections you made, and the grammar, fragment and punctuation flags waiting for my approval (not applied).
3. **Your calls:** each judgment call, the choice you applied, and a sentence of reasoning.
4. **The description, excerpt and door,** so I can read them without opening the file, with their lengths confirmed against the caps.
5. **Related messages:** each link with the subject it shares, and for every other file a full `related_messages:` block in date order, ready to paste.
6. **Spirit and medium files:** any biography the message states that the file does not carry, citing the message_id. Ask before creating a new spirit or medium file.
7. **Chains:** the log entry, in very simple language, the year file it goes in and where, any roster, holding-pen or pattern changes, and the reasoning for each role. A message that joins no thread gets the single line "- Read in full; joins no thread." The log holds only what develops threads: no context notes. Anything else about the message goes in its own `notes`, or in the spirit or medium file.
8. **Prayer:** if a spirit gives a prayer, its practice file. Nothing else points to it: no note in the log and no line in the message's `notes`.
9. **The files** as downloads.

End with a short list of what is waiting on my decision.

---

## PROMPT 3: An unpublished message (one per message)

Next message, not published. Leave `canonical_url: ""` and add no note about it.

```
Title:
Spirit:
Medium:
Location:
Date:
Gathering:
```

[Paste the message text below the header block.]

Please catalogue it the same way as a published message, working from the pasted text exactly as given.

---

## PROMPT 4: A message already in the archive

Please read [message_id] in full, log it for chains, and bring its file up to the current rules in the same pass, as the handoff's "Reviewing a message already in the archive" section describes. Give me the same reply as for a new message, and say which rules the file was breaking.

---

## PROMPT 5: After you commit

Committed. Please check that GitHub matches what you sent, and that both checks pass on what is there now.

---

## PROMPT 6: End of session

We are wrapping up. Please:

1. List anything still waiting for my commit or my decision.
2. Update the Chains Layer Handoff note to the current state, and send it to me as a download. Once I have committed it, replace the project doc `claude/chains-layer-handoff.md` with the same text.
3. Give me new wording for the Current state section of the project instructions, ready to paste.
4. Tell me where the next session should pick up.

---

## Session hygiene (for you)

- One message per turn. Read the reply, decide the calls, and review the files before the next message goes in.
- Commit about every five messages, or at a natural stopping point, then paste Prompt 5 so Claude checks the commit landed as delivered.
- Start a fresh session when the conversation has grown long. The signs are slower replies, or Claude losing track of a ruling made earlier in the session. Paste Prompt 6 first, so nothing is lost between sessions.
- Any ruling you make that should outlast the session belongs in schema.md, the design blocks, or the handoff. Ask Claude to write it there; do not rely on it being remembered.
- For the quality bar on doors, questions and descriptions, point Claude at 2019-04-08-mc-mary and 2019-02-22-af-augustine.

---

## If a session cannot reach the repo

Attach these, freshly exported, and say in Prompt 1 that the repo is not connected:

- `schema/schema.md`, `schema/message.schema.yml`, `metadata/subjects.yml`
- the project instructions
- `llms.txt` (the index of existing messages, for collision checks and related_messages candidates)
- `metadata/chains-log.md` and `metadata/chains-threads.md` (the rules, registry, holding pen, patterns and open questions)
- the year files from `metadata/chains-log/` for the years you expect to work in
- the roster files from `metadata/chains-threads/` for the threads likely to come up, or all of them if unsure
- the Chains Layer Handoff note
- `spirits-digest.txt`, regenerated first with `python .github/scripts/generate_spirits_digest.py`

Without the repo, Claude cannot run the checks on the whole archive, so run both validators yourself before each commit.