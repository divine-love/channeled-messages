# Keeping the Archive: A Guide for Whoever Comes Next

This guide is for a person who wants to keep adding to the Divine Love Messages archive and has never seen how it is put together. It explains what every part is for, what each script does, and how to do the ordinary jobs, one step at a time.

It describes how the archive works, not where the work currently stands. Counts and positions change every week, so this guide tells you how to find them instead of stating them.

You do not need to be a programmer. You need patience, care with detail, and a willingness to read the rulebook before changing anything.

---

## 1. The archive in one page

**What it is.** A collection of channeled messages, each stored as one text file. Every file holds the message exactly as it was received, plus a block of catalogue information above it: who spoke, who received it, when, what it is about, and the questions it answers.

**Where it lives.** In a repository on GitHub called `divine-love/channeled-messages`. A repository is a folder of files with a complete history of every change ever made to it. Nothing is ever truly lost: any earlier version of any file can be brought back.

**What readers see.** A website, thewayofdivinelove.com, which is built from the repository. Nobody edits the website directly. You change the files in the repository, rebuild, and publish.

**The three things to hold onto:**

1. **The repository is the source of truth.** If the website and the repository disagree, the repository is right.
2. **The message text is never altered.** Every message was read and approved by its medium before posting. Fixing a clear typing error is allowed. Changing wording, grammar or meaning is not, without the permission of the Divine Love Sanctuary Foundation. Everything a curator writes sits around the message, never inside it.
3. **Some files you write, and some files are written for you.** Scripts build the index pages and the whole website copy from the message files. If you edit one of those built files by hand, your edit is erased the next time the script runs. Section 4 says which is which.

---

## 2. How a message travels

```
A message is received and transcribed
        |
        v
You write its file:  content/messages/YEAR/MONTH/<message_id>.md
        |
        |   you commit and push to GitHub
        v
GitHub checks every file ............ a red X means something needs fixing
GitHub rebuilds the index pages ..... browse page, collections, essential teachings, llms.txt
        |
        |   you pull, then run:  python .github/scripts/generate_vault.py
        v
obsidian-vault/  .................... a throwaway copy of the archive, laid out as a website
        |
        |   in Obsidian you choose Publish changes
        v
thewayofdivinelove.com
```

Each stage is explained below. If you ever feel lost, come back to this picture and ask which stage you are at.

---

## 3. What you need

**Tools, all free except Obsidian Publish:**

| Tool | What it is for |
|---|---|
| A GitHub account with permission to change `divine-love/channeled-messages` | Saving your changes to the repository |
| Git | The program that sends changes between your computer and GitHub |
| VS Code | The editor for the files. Its Source Control panel shows every change before you commit it |
| Python 3 | Runs the scripts. After installing it, run `pip install pyyaml jsonschema` once |
| Obsidian, with an Obsidian Publish subscription | Opens the built copy of the archive and publishes it to the website |

**Access.** No accounts or passwords are kept in the repository, because the repository is public. To take up this work, reach out to the Divine Love Sanctuary Foundation, whose site is [divinelovesanctuary.com](https://divinelovesanctuary.com). Ask the Foundation about:

- access to the GitHub organization `divine-love`
- access to the Obsidian Publish account for the site
- the domain thewayofdivinelove.com and its renewal
- permission for any change to message text
- new messages, and the transcripts of messages that have not been published

**Git in four words.** *Pull* brings the latest files from GitHub to your computer. You *edit*. *Commit* records a set of changes with a short note saying what you did. *Push* sends your commits to GitHub. Always pull before you start work (section 6 explains why).

---

## 4. A map of the repository

| Folder or file | What it holds | Who writes it |
|---|---|---|
| `content/messages/YEAR/MONTH/` | One file per message | You |
| `content/practices/` | Prayers and practices, including a file for each prayer a spirit gives | You |
| `content/books/`, `content/talks/` | Recommended books, and talks that are not channeled messages | You |
| `content/templates/` | Blank starting files for a message, spirit, medium, prayer and book | You, rarely |
| `content/browse.md` | The browse page: every message with its "door" | A script |
| `content/collections/` | One page per thematic collection | A script |
| `content/essential-teachings/` | One page per essential-teaching category | A script |
| `llms.txt` | An index of every message for AI systems and search engines | A script |
| `spirits/` | One file per spirit: who they are and what they have said of themselves | You |
| `mediums/` | One file per medium | You |
| `metadata/subjects.yml` | The list of subjects a message may be filed under | You, with care |
| `metadata/collections.yml`, `metadata/essential-teachings.yml` | The collections and essential-teaching categories, with their rules | You, with care |
| `metadata/law-mentions-reviewed.yml` | Messages that mention a spiritual Law only in passing, reviewed and left untagged | You |
| `metadata/chains-log.md` and the `chains-log/` folder | The chains layer: the rules, then the evidence for each message, one file per year | You |
| `metadata/chains-threads.md` and the `chains-threads/` folder | The chains layer: the list of threads, then one file per thread | You |
| `schema/schema.md` | **The rulebook.** Every cataloguing rule is here | You, when a rule changes |
| `schema/message.schema.yml` | The same rules in a form the checker can read | You, when a rule changes |
| `.github/scripts/` | The scripts (section 5) | You, rarely |
| `.github/workflows/` | Instructions telling GitHub when to run the scripts | You, rarely |
| `.github/assets/` | The website's home page text (`home.md`), its other hand-written pages (the `pages/` folder), and its styling (`publish.css`) | You |
| `obsidian-vault/` | The built copy of the archive for the website | A script, except `Notes/` |
| `obsidian-vault/Notes/` | The keeper's own working notes. The only part of the vault that is kept in the repository | You |
| `scripts/` | A few old one-time repair scripts, kept for the record. Not part of the normal work | Nobody now |
| `spirits-digest.txt` | Every spirit file joined into one, for handing to an AI assistant | A script |
| `README.md` | The public welcome page of the repository | You |

**The rule of thumb:** if a script writes it, never edit it by hand. Change the message files or the rulebooks, and let the script rebuild it.

---

## 5. What each script does

All the scripts live in `.github/scripts/`. Run any of them from the top folder of the repository, like this:

```
python .github/scripts/validate_messages.py
```

### Scripts that check

These change nothing. They read the files and report problems.

| Script | What it checks | Runs |
|---|---|---|
| `validate_messages.py` | Every message file against the rulebook: required fields, lengths, subjects that really exist, spirits and mediums that have files, links to messages that exist, collection rules. Ends with a count of how often each subject is used | On GitHub at every push, and by you before committing |
| `validate_prayers.py` | Every spirit-given prayer file in `content/practices/`: that it points to a real message and that its words match that message exactly | On GitHub at every push, and by you |
| `validate_chains.py` | The chains layer: every thread name is real, entries are in date order, each entry is in the right year's file, each roster file is named for its thread, the no-thread line is written exactly | On GitHub when a chains file changes, and by you |
| `check_dashes.py` | Lists every em dash and en dash in the repository, so curator-written ones can be removed | By you, now and then |
| `check_body_endings.py` | Lists messages whose text seems to stop mid-sentence, which can mean a message was cut short when copied | By you, now and then |
| `check_names.py` | Looks for invisible characters in page names, which make links work in Obsidian but fail on the website | By you, when a link on the site is broken |

### Scripts that build

These write files. Never edit what they write.

| Script | What it builds | Runs |
|---|---|---|
| `generate_browse.py` | `content/browse.md` | On GitHub at every push |
| `generate_llms.py` | `llms.txt` | On GitHub at every push |
| `generate_collections.py` | The pages in `content/collections/` | On GitHub at every push |
| `generate_essential_teachings.py` | The pages in `content/essential-teachings/` | On GitHub at every push |
| `generate_vault.py` | The whole `obsidian-vault/` folder: a page for every message, spirit, medium, gathering, subject, collection and chain, plus the home page and indexes | By you, before publishing the website |
| `generate_spirits_digest.py` | `spirits-digest.txt` | By you, when an AI assistant needs all the spirit files at once |

### A helper

| Script | What it does |
|---|---|
| `chains_io.py` | Reads the many chains files and hands them to `validate_chains.py` and `generate_vault.py` as one text. You never run it yourself; those two scripts load it |

Each script begins with a plain description of what it does. If this guide and a script disagree, the script is right, and this guide needs correcting.

---

## 6. What happens when you push

GitHub watches the repository. When you push, it starts one or both of these jobs by itself. You can watch them under the **Actions** tab of the repository on GitHub.

**"Validate and Generate"** runs when you push a change to a message, a practice, a spirit or medium file, the subject or collection lists, or a script. It:

1. checks every message file and every prayer file;
2. rebuilds the browse page, `llms.txt`, the collection pages and the essential-teaching pages;
3. saves those rebuilt pages back to the repository as a commit of its own, named "chore: regenerate index and collection files".

**"Validate Chains Layer"** runs when you push a change to any chains file. It only checks; it builds nothing.

**Two things follow from this:**

- **A green tick means the checks passed. A red X means one failed.** Click the X, then **Details**, and the report names the file and the rule. Fix the file, commit and push again.
- **GitHub has usually added a commit after yours.** So before you start your next piece of work, pull. If you forget, your next push is refused until you pull, and the history gains a "Merge branch" entry. That does no harm, but pulling first avoids it.

---

## 7. Reading the rulebooks

Before cataloguing anything, read `schema/schema.md` from start to finish. It is the rulebook, and it settles almost every question you will have: how a message is named, what each field means, how to write a description, what goes in the notes, how subjects are chosen.

| File | What it settles |
|---|---|
| `schema/schema.md` | Every cataloguing rule. If anything else disagrees with it, it wins |
| `schema/message.schema.yml` | The limits the checker enforces: which fields are required, how long a description may be |
| `metadata/subjects.yml` | The only subjects a message may use, each with its definition |
| `metadata/collections.yml` | The collections, and which spirits must or must not be in each |
| `metadata/essential-teachings.yml` | The essential-teaching categories and when to use each |
| The opening sections of `metadata/chains-log.md` and `metadata/chains-threads.md` | The rules of the chains layer |

**When you make a new ruling, write it into the rulebook.** A decision that lives only in someone's memory is lost with them. That is the reason this guide exists.

---

## 8. What a message file looks like

A message file has two parts, separated by lines of three dashes.

```
---
message_id: 2019-02-22-af-augustine
title: "The Power to Change Needs Your Conscious Understanding of the Power of Free Will"
date: 2019-02-22
spirit_id: augustine
medium: Al Fike
... more catalogue fields ...
---

I am your teacher Augustine. I cannot resist this opportunity to speak to you ...
```

The top part is the **front matter**: the catalogue information, written by the curator. The bottom part is the **message**, exactly as received.

**How a message is named.** Its `message_id` is the date, the medium's initials, and the spirit's id: `2019-02-22-af-augustine` is a message from Augustine through Al Fike on 22 February 2019. The file has the same name with `.md` on the end, and sits in the folder for its year and month: `content/messages/2019/02/2019-02-22-af-augustine.md`.

**The fields a reader meets first:**

- **description**: what the message is about, in the curator's words.
- **excerpt**: one passage of the spirit's own words, copied exactly.
- **door**: one or two spare sentences by the curator that open the message to a newcomer, within 300 characters.
- **questions**: questions a seeker might type into a search, which this message answers.
- **subjects, collections, essential_teachings**: where the message is filed.
- **related_messages**: a few other messages on the same subject. Every link goes both ways.

Section 4 of `schema/schema.md` explains every field. `content/templates/message-template.yml` is a blank one to start from.

---

## 9. Adding a message, step by step

1. **Pull**, so you have the latest files.
2. **Work out the `message_id`** and make sure no file already has it. Messages are not catalogued in date order, so never assume a date is free.
3. **Create the file** in the folder for its year and month, starting from the template.
4. **Paste in the message text.** If it is published at divinelovesanctuary.com, check it against the published page and put that page's address in `canonical_url`. If it is not published, leave `canonical_url` empty.
5. **Review the text.** Fix spacing faults and clear typing errors. Leave grammar and wording alone.
6. **Fill in the catalogue fields,** following `schema/schema.md`. Take every subject from `metadata/subjects.yml`, spelled exactly as it is there.
7. **Check the spirit and medium have files.** If the spirit is new, create `spirits/<spirit_id>.yml` from its template. If the message tells you something about the spirit's life, add it to the spirit's file and name the message it came from. Record only what a message says.
8. **Add related messages,** and add this message to each of theirs, so the links go both ways. Keep each list in date order.
9. **If a spirit gives a prayer,** make its practice file from `content/templates/prayer-template.md`, named `prayer-<message_id>.md`.
10. **Log the message in the chains layer** if it belongs to a thread (section 11).
11. **Run the checks:**
    ```
    python .github/scripts/validate_messages.py
    python .github/scripts/validate_prayers.py
    python .github/scripts/validate_chains.py
    ```
12. **Look over your changes** in VS Code's Source Control panel, then commit and push.
13. **Watch the Actions tab** for a green tick.

**Working with an AI assistant.** This archive has been catalogued with the help of Claude, one message at a time, with the keeper reviewing every change before committing it. The prompts used are in `obsidian-vault/Notes/Claude/Claude Conversation Prompt Kit.md`, and the instructions given to the assistant are in `obsidian-vault/Notes/Github/Project Instructions.md`. An assistant makes the work faster. It does not replace reading the message yourself, and it must never be allowed to change message text or to commit on its own.

---

## 10. Other jobs

**Add a spirit or a medium.** Copy the template from `content/templates/` into `spirits/` or `mediums/`, name the file for the id (`john-the-beloved.yml`), and fill it in. First make sure the spirit does not already have a file under another spelling.

**Name or describe a gathering.** Each gathering named in the messages gets its own page in the vault's Gatherings folder: a retreat, an event, a named prayer circle that meets regularly, or the Direct Voice circle. Use the gathering's own name, exactly as it is given. Do not add words such as "Retreat" to a name that does not use them, and spell it the same way in every message, since each spelling makes its own page. To put a short description at the top of a gathering's page, add it to `GATHERING_DESCRIPTIONS` near the top of `.github/scripts/generate_vault.py`, then rebuild the vault.

**Add a subject.** Add it to `metadata/subjects.yml` with a definition. Do this rarely: a new subject is only worth having if several messages need it and no existing subject fits.

**Add a collection.** A collection is named in four places, and all four must agree:

1. `metadata/collections.yml` (its name and rules)
2. `schema/message.schema.yml` (the list of allowed collections)
3. `.github/scripts/generate_collections.py` (its page name and its description)
4. `schema/schema.md`, section 4b (so the rulebook lists it)

The same holds for an essential-teaching category, with `metadata/essential-teachings.yml`, `generate_essential_teachings.py` and section 4a.

**Correct a typing error in a message.** Fix it in the message file and change `last_edited`. If the chains layer quotes that passage, correct the quote too: the next vault build will tell you if a quote no longer matches (section 12).

**Add a translation.** A translation is a second file beside the original, with the language code before `.md`: `2015-11-30-af-jesus.pt-br.md`. Section 9 of `schema/schema.md` has the rules.

**Change the website's home page or its look.** Edit `.github/assets/home.md` or `.github/assets/publish.css`, then rebuild the vault.

**Change or add a hand-written page.** The pages a newcomer meets first, Begin Here and How This Archive Is Organized, are plain files in `.github/assets/pages/`. Each file becomes a page named for its first heading. To add a page, add a file there; to remove one, delete the file. Then rebuild the vault. Inside these pages and the home page, a few markers are filled in for you at build time:

| You write | The page shows |
|---|---|
| `@message[2019-03-14-af-jesus]` | A link to that message, shown by its title |
| `@door[2019-03-14-af-jesus]` | That message's door |
| `@spirit[Augustine]`, `@medium[Al Fike]`, `@collection[Two Paths]` | A link to that spirit's, medium's or collection's page |
| `{messages}`, `{subjects}` | The current number of messages or subjects |

To change which messages Begin Here offers, change the message ids in `begin-here.md`. Their titles and doors follow by themselves.

---

## 11. The chains layer

Most of the archive files a message under subjects. The chains layer does something different: it follows a single idea as an argument, step by step, across many messages. A chain is laid out in the order the argument needs, not the order of the calendar. The angels return to an important teaching again and again over the years, so messages given years apart may stand side by side at the same step. Dates settle the order only among the messages that share a step. Each idea followed this way is a **thread**. Within a thread, each message has a **role**: the one that lays the idea down, the ones that develop it, the ones that answer an objection, and so on.

It exists so that a reader can follow a teaching as a whole instead of meeting it in fragments, and so that no single line is lifted out of its message.

**Where it lives:**

| File | What it holds |
|---|---|
| `metadata/chains-threads.md` | How the layer works, the list of every thread, ideas being watched that are not yet threads, and open questions |
| `metadata/chains-threads/<thread>.md` | One file per thread: its messages, in role order |
| `metadata/chains-log.md` | The rules for logging a message |
| `metadata/chains-log/<year>.md` | The evidence: for each message, which threads it joins, in what role, and the passage that earns it. One file per year of message |

**Before touching it,** read the opening sections of `chains-threads.md` and `chains-log.md`, and then `obsidian-vault/Notes/Claude/Chains Layer Handoff.md`, which records the standing rulings and why each was made.

**The rules that matter most:**

- An entry is written only after reading the whole message.
- Every message read for chains gets an entry. One that joins no thread gets its heading and the single line `- Read in full; joins no thread.`, written exactly so. A message with no entry is one not yet read for chains.
- Anything in quotation marks is the message's own words, copied exactly.
- No counts, no "the first" or "the fullest". Messages are still being added, so any such claim goes out of date.
- A new thread gets its line in the list and its own file in the same commit.

---

## 12. Building and publishing the website

1. **Pull**, so you have the index pages GitHub rebuilt.
2. **Build the vault:**
   ```
   python .github/scripts/generate_vault.py
   ```
   This deletes and rebuilds everything in `obsidian-vault/` except the `Notes/` folder and your Obsidian settings. It takes a few seconds.
3. **Read what it prints.** Among other things it reports "Quotes in context ... not located". That number should be 0. If it is not, a quotation in the chains layer no longer matches its message; find it in `Chains (working)` in the vault and correct the log.
4. **Open `obsidian-vault/` in Obsidian** and look at what changed.
5. **Publish.** In Obsidian, choose Publish changes, review the list, and publish.

**What must not be published:** two folders are left out of publishing.

- `Chains (working)` is the keeper's private view of the chains layer, with working notes and the paragraph behind every quotation.
- `Notes` holds the keeper's own working notes.

Everything else in the vault is published.

**How Obsidian is set up.** Besides Obsidian Publish itself, the vault uses two community plugins:

- **Front Matter Title**, with only its Graph feature switched on. Message pages are named with their date first so they sort in order, and this plugin makes the graph show each message's title instead.
- **Sync Graph Settings**, which keeps the graph's display settings consistent.

**After publishing, nothing is changed by hand.** The live site is exactly what Obsidian Publish makes from the vault. If something on the site is wrong, correct it in the repository, rebuild the vault, and publish again.

**On the public site, a chain page links to whole messages and never to a passage.** This is deliberate. The messages are meant to be read in full.

---

## 13. When something goes wrong

| What you see | What it usually means | What to do |
|---|---|---|
| A red X on GitHub after a push | A file broke a rule | Click the X, then Details. The report names the file and the rule. Fix, commit, push |
| "Subject not found" or similar | A subject is misspelled or not in `subjects.yml` | Copy the name exactly from `metadata/subjects.yml` |
| A related message "does not exist" | A mistyped `message_id` in `related_messages` | Correct it to match a real file name |
| Your push is refused | GitHub added a commit after your last pull | Pull, then push again |
| A link works in Obsidian but not on the website | An invisible character in a page name | Run `check_names.py` |
| A chains check fails | An entry is in the wrong year's file, out of date order, or uses a thread name that does not exist | The message names the file and line |
| You edited a built file and the change vanished | A script rebuilt it | Make the change in the message file or rulebook instead |
| You have made a mess and want to go back | | Every earlier version is kept. In VS Code, discard your uncommitted changes; or on GitHub, open the file's History and copy back the version you want |

Nothing you do on your own computer can damage the archive until you push. And once pushed, any change can be undone, because the history keeps everything.

---

## 14. Words used here

| Word | Meaning |
|---|---|
| **Anchor** | In a thread, the message that states one step of the idea most clearly |
| **Canonical URL** | The address of the message's published page |
| **Chain, thread** | One idea followed as an argument across many messages, in the order the argument needs. "Thread" is the working name; a "chain" is the finished form a thread will take |
| **Commit** | A saved set of changes, with a note saying what was done |
| **Door** | One or two sentences by the curator that open a message to a newcomer |
| **Excerpt** | A passage of the spirit's own words, shown above the message |
| **Front matter** | The catalogue information at the top of a file, between the lines of three dashes |
| **Generated** | Written by a script. Never edited by hand |
| **Hub** | A page that gathers messages: one per spirit, subject, collection or chain |
| **Medium** | The person through whom a message was received |
| **Pull, push** | Bring changes from GitHub to your computer; send yours to GitHub |
| **Repository** | The folder of all the archive's files, with its full history, kept on GitHub |
| **Roster** | The file listing one thread's messages in role order |
| **Vault** | The built copy of the archive that Obsidian opens and publishes |
| **Witness** | A message that restates a thread's idea without carrying it further |
| **YAML** | The simple format the front matter is written in: `name: value`, one per line |

---

## 15. Where to read more

| To learn about | Read |
|---|---|
| Every cataloguing rule | `schema/schema.md` |
| What the checker looks for | `schema/VALIDATION.md` and the opening of `validate_messages.py` |
| The chains layer and its rulings | The opening of `metadata/chains-threads.md` and `metadata/chains-log.md`; `obsidian-vault/Notes/Claude/Chains Layer Handoff.md` |
| How the vault is built | The opening of `.github/scripts/generate_vault.py` |
| Where the work stands and what is planned | `obsidian-vault/Notes/Github/Project Instructions.md` (its "Current state" and "Deferred" sections) and the Chains Layer Handoff |
| Working with an AI assistant | `obsidian-vault/Notes/Claude/Claude Conversation Prompt Kit.md` |
| What the archive is for | `README.md` |

---

## 16. In the spirit of the work

Three habits have kept this archive trustworthy. They matter more than any script.

- **Read the whole message.** Every description, door, question and chain entry comes from a full reading, never from a skim or a search.
- **Let the messages speak for themselves.** The curator's words point toward a message. They do not interpret it, argue for it, or stand in for it.
- **Bring things to light instead of quietly fixing them.** When something looks wrong, write it down and decide it in the open, so the next person can see what was decided and why.

*These messages were received in love. May they find you in yours.*