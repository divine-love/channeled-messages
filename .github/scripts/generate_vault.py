#!/usr/bin/env python3
"""
generate_vault.py — build a derived Obsidian vault from the archive.

The repository stays canonical; this emits a disposable, regenerable vault
in ./obsidian-vault/ (add that folder to .gitignore). Never edit the vault
by hand — rerun this script after commits instead.

What it builds:
  Messages/<year>/<Message Title>.md   one note per message, FILENAMED BY
      TITLE so the graph and quick-switcher read in human language (the
      message_id is preserved as a property and in the note body):
      - STRUCTURED PROPERTIES mirroring the archive schema: the original
        field names and values (message_id, date, spirit, medium, location,
        message_type, primary_subject, secondary_subjects, keywords,
        collections, essential_teachings, chains, mentions), with wikilinks
        inside properties wherever a hub page exists — so the metadata is
        searchable per-field ( ["primary_subject":Mind] ), browsable, and
        feeds the graph, without collapsing anything into tags
      - title alias so wikilinks display the human title
      - door callout, description, "Questions this message answers"
        (full-text searchable), related-message wikilinks, chain wikilinks,
        then the full message text
  Subjects Index.md                 the full subjects.yml hierarchy as a
      linked tree — the taxonomy browser, replacing the old nested tags
  Chains/<slug>.md                  one hub per minted thread: theme,
      argument, members grouped in role-section order (Foundation first),
      chronological within each section, anchors marked (anchor)
  Subjects/<name>.md, Spirits/<id>.md, Collections/<name>.md
      category hub pages listing member messages (filter these out of the
      graph with  -path:"Subjects"  etc. if the hubs dominate)
  Ask the Archive.md                every question in the archive, grouped
      by top-level subject category, each linking to its answering message
  Home.md                           dashboard with counts and entry points

Run from the repo root:
    python .github/scripts/generate_vault.py
Then open ./obsidian-vault/ as a vault in Obsidian.

Search behaviour: Obsidian's search matches question text inside notes, so
a seeker typing words from a real question ("responsible for people who
reject") lands on the message that answers it. The Ask the Archive index
gives the same corpus as a browsable FAQ.
"""

import re
import sys
import shutil
import yaml
from pathlib import Path
from collections import defaultdict

ROOT = Path(".")
MESSAGES_DIR = ROOT / "content" / "messages"
SUBJECTS_PATH = ROOT / "metadata" / "subjects.yml"
CHAINS_LOG = ROOT / "metadata" / "chains-log.md"
CHAINS_THREADS = ROOT / "metadata" / "chains-threads.md"
VAULT = ROOT / "obsidian-vault"

ROLE_ORDER = ["Foundation", "Elaboration", "Objection-removed", "Reframe",
              "Testimony", "Chrysalis", "Capstone"]


def slug(text):
    """Tag-safe slug: lowercase, & -> and, spaces -> hyphens."""
    t = text.lower().replace("&", "and")
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")


def filename(title):
    """
    Filesystem-safe note name from a message title, preserving human
    readability. Strips characters illegal in filenames on Windows and macOS
    (asterisk, quote, backslash, slash, angle brackets, colon, pipe, question
    mark), drops the curator asterisk, and collapses whitespace.
    """
    name = title.strip().rstrip("*").strip()
    name = name.replace("/", "-").replace("\\", "-").replace(":", " -")
    name = re.sub(r'[*"<>|?]', "", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    return name or "Untitled"


def load_front_matter(path):
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return None, None
    end = raw.find("\n---", 3)
    if end == -1:
        return None, None
    fm = yaml.safe_load(raw[3:end])
    body = raw[end + 4:].lstrip("\n")
    return fm, body


def load_subject_hierarchy():
    """Return {subject_name: parent_name_or_None}."""
    data = yaml.safe_load(SUBJECTS_PATH.read_text(encoding="utf-8"))
    parents = {}
    for cat in data.get("main_categories", []):
        parents[cat["name"]] = None
        for sub in cat.get("subcategories", []) or []:
            parents[sub["name"]] = cat["name"]
    return parents


def parse_chain_registry():
    """From chains-threads.md registry table: {slug: (theme, argument)}."""
    reg = {}
    if not CHAINS_THREADS.exists():
        return reg
    for line in CHAINS_THREADS.read_text(encoding="utf-8").splitlines():
        if line.startswith("| `"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 3:
                reg[cells[0].strip("`")] = (cells[1], cells[2])
    return reg


def parse_chain_memberships():
    """
    From chains-log.md member lines: {message_id: [(slug, role, is_anchor)]}.
    Only bold member lines (- `slug` **[Role...]**) count; NOTEs/sightings
    are intentionally excluded from the graph.
    """
    members = defaultdict(list)
    if not CHAINS_LOG.exists():
        return members
    current_id = None
    for line in CHAINS_LOG.read_text(encoding="utf-8").splitlines():
        h = re.match(r"### (\S+) — .+ — \d{4}-\d{2}-\d{2}", line)
        if h:
            current_id = h.group(1)
            continue
        m = re.match(r"- `([a-z0-9-]+)` \*\*\[([^\]]+)\]\*\*(.*)", line)
        if m and current_id:
            chain_slug = m.group(1)
            role = m.group(2).split()[0].split(";")[0].split(",")[0]
            role = role.replace("—", "").strip() or "Elaboration"
            anchor = "presumptive anchor" in (m.group(2) + m.group(3)).lower() \
                     or "presumptive section anchor" in (m.group(2) + m.group(3)).lower()
            members[current_id].append((chain_slug, role, anchor))
    return members


def wiki(msg_id, titles, notenames):
    """Link by note filename; display the human title."""
    name = notenames.get(msg_id, msg_id)
    title = titles.get(msg_id, msg_id)
    return f"[[{name}|{title}]]" if name != title else f"[[{name}]]"


def main():
    if not MESSAGES_DIR.exists():
        print("Run from the repository root (content/messages not found).")
        sys.exit(1)

    parents = load_subject_hierarchy()
    registry = parse_chain_registry()
    memberships = parse_chain_memberships()

    # Pass 1: load all messages
    messages = {}
    for path in sorted(MESSAGES_DIR.rglob("*.md")):
        if path.name.count(".") > 1:      # translation files like *.pt-br.md
            continue
        fm, body = load_front_matter(path)
        if not fm or "message_id" not in fm:
            continue
        if fm.get("translation_of"):
            continue
        messages[fm["message_id"]] = (fm, body)
    titles = {mid: fm.get("title", mid).strip() for mid, (fm, _) in messages.items()}

    # Note filenames are the titles. Two messages may legitimately share a
    # title, so disambiguate collisions with the date, and keep a map from
    # message_id -> note name for every link the vault emits.
    notenames = {}
    used = {}
    for mid in sorted(messages):
        base = filename(titles[mid])
        key = base.lower()
        if key in used:
            base = f"{base} ({str(messages[mid][0].get('date',''))})"
            key = base.lower()
            while key in used:
                base = f"{base} ({mid})"
                key = base.lower()
        used[key] = mid
        notenames[mid] = base

    # Rebuild ONLY the generated folders. Everything else in the vault -
    # your Obsidian config in .obsidian/, and anything you write in Notes/ -
    # is preserved across runs and never touched by this script.
    GENERATED = ["Messages", "Chains", "Subjects", "Spirits", "Collections",
                 "Mediums", "Essential Teachings"]
    GENERATED_FILES = ["Ask the Archive.md", "Subjects Index.md", "Home.md"]
    VAULT.mkdir(exist_ok=True)
    for d in GENERATED:
        p = VAULT / d
        if p.exists():
            shutil.rmtree(p)
        p.mkdir(parents=True)
    for f in GENERATED_FILES:
        (VAULT / f).unlink(missing_ok=True)
    # Your own space: created once, never regenerated, safe to write in.
    notes = VAULT / "Notes"
    notes.mkdir(exist_ok=True)
    readme = notes / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Notes\n\n"
            "This folder is yours. `generate_vault.py` never touches it.\n\n"
            "Everything else in this vault (Messages, Chains, Subjects,\n"
            "Spirits, Collections, Mediums, Essential Teachings, Home,\n"
            "Ask the Archive, Subjects Index) is GENERATED and is deleted\n"
            "and rebuilt on every run. Never edit those by hand - edit the\n"
            "repository instead, then regenerate.\n\n"
            "Link freely from here into the generated notes; wikilinks like\n"
            "[[2019-04-04-af-matthew]] resolve normally.\n",
            encoding="utf-8")

    by_subject = defaultdict(list)
    by_spirit = defaultdict(list)
    by_collection = defaultdict(list)
    by_medium = defaultdict(list)
    by_et = defaultdict(list)
    questions_by_category = defaultdict(list)
    chain_members = defaultdict(list)     # slug -> [(role, anchor, msg_id, date)]

    # Pass 2: write message notes
    for mid, (fm, body) in sorted(messages.items()):
        date = str(fm.get("date", ""))
        spirit = fm.get("spirit_name") or fm.get("spirit_id", "")
        subjects = [fm.get("primary_subjects")] if fm.get("primary_subjects") else []
        subjects += [s for s in (fm.get("secondary_subjects") or []) if s]
        for chain_slug, role, anchor in memberships.get(mid, []):
            chain_members[chain_slug].append((role, anchor, mid, date))

        def q(v):
            return '"' + str(v).replace('"', "'") + '"'

        def subj_link(name):
            return q(f"[[Subjects/{slug(name)}|{name}]]")

        loc = fm.get("location") or {}
        loc_str = ", ".join(x for x in [loc.get("city"), loc.get("region"),
                                        loc.get("country")] if x)
        props = ["---",
                 f"message_id: {mid}",
                 f"aliases: [{mid}]",
                 f"date: {date}",
                 f"spirit: {q('[[Spirits/' + fm.get('spirit_id','') + '|' + (fm.get('spirit_name') or fm.get('spirit_id','')) + ']]')}",
                 f"medium: {q('[[Mediums/' + slug(fm.get('medium','')) + '|' + fm.get('medium','') + ']]')}",
                 f"location: {q(loc_str)}"]
        if fm.get("gathering"):
            props.append(f"gathering: {q(fm['gathering'])}")
        mt = (fm.get("message_type") or [""])[0]
        props.append(f"message_type: {q(mt)}")
        if fm.get("primary_subjects"):
            props.append(f"primary_subject: {subj_link(fm['primary_subjects'])}")
        sec = fm.get("secondary_subjects") or []
        if sec:
            props.append("secondary_subjects:")
            props += [f"  - {subj_link(s)}" for s in sec]
        kws = fm.get("keywords") or []
        if kws:
            props.append("keywords:")
            props += [f"  - {q(k)}" for k in kws]
        colls = fm.get("collections") or []
        if colls:
            props.append("collections:")
            props += [f"  - {q('[[Collections/' + slug(c) + '|' + c + ']]')}" for c in colls]
        ets = fm.get("essential_teachings") or []
        if ets:
            props.append("essential_teachings:")
            props += [f"  - {q('[[Essential Teachings/' + slug(e) + '|' + e + ']]')}" for e in ets]
        mem_props = memberships.get(mid, [])
        if mem_props:
            props.append("chains:")
            props += [f"  - {q('[[Chains/' + cs + ']]')}" for cs, _, _ in mem_props]
        mentions = fm.get("spirits") or []
        if mentions:
            props.append("mentions:")
            props += [f"  - {q('[[Spirits/' + sp + ']]')}" for sp in mentions]
        if fm.get("canonical_url"):
            props.append(f"canonical_url: {q(fm['canonical_url'])}")
        lines = props + ["---",
                 "",
                 f"# {titles[mid]}",
                 "",
                 f"**Spirit:** [[Spirits/{fm.get('spirit_id','')}|{spirit}]] · "
                 f"**Medium:** {fm.get('medium','')} · **Date:** {date}",
                 ""]
        door = (fm.get("door") or "").strip()
        if door:
            lines += ["> [!quote] The Door", f"> {door}", ""]
        desc = (fm.get("description") or "").strip()
        if desc:
            lines += [desc, ""]
        qs = fm.get("questions") or []
        if qs:
            lines += ["## Questions this message answers", ""]
            lines += [f"- {q}" for q in qs] + [""]
            top = parents.get(subjects[0]) or subjects[0] if subjects else "General"
            for q in qs:
                questions_by_category[top].append((q, mid))
        rel = fm.get("related_messages") or []
        if rel:
            lines += ["## Related messages", ""]
            lines += [f"- {wiki(r, titles, notenames)}" for r in rel] + [""]
        mem = memberships.get(mid, [])
        if mem:
            lines += ["## Chains", ""]
            for chain_slug, role, anchor in mem:
                mark = " **(anchor)**" if anchor else ""
                lines += [f"- [[Chains/{chain_slug}]] — {role}{mark}"]
            lines += [""]
        lines += ["---", "", body.strip(), ""]

        year = date[:4] or "undated"
        (VAULT / "Messages" / year).mkdir(exist_ok=True)
        (VAULT / "Messages" / year / f"{notenames[mid]}.md").write_text(
            "\n".join(lines), encoding="utf-8")

        for s in subjects:
            by_subject[s].append((date, mid))
        by_spirit[fm.get("spirit_id", "unknown")].append((date, mid))
        for c in fm.get("collections") or []:
            by_collection[c].append((date, mid))
        by_medium[fm.get("medium", "Unknown")].append((date, mid))
        for e in ets:
            by_et[e].append((date, mid))

    # Chain hubs
    for chain_slug, mem in sorted(chain_members.items()):
        theme, argument = registry.get(chain_slug, ("", ""))
        lines = [f"# Chain: {chain_slug.replace('-', ' ').title()}", ""]
        if theme:
            lines += [f"> {theme}", ""]
        if argument:
            lines += [f"**The argument it traces:** {argument}", ""]
        by_role = defaultdict(list)
        for role, anchor, mid, date in mem:
            by_role[role].append((date, anchor, mid))
        ordered = [r for r in ROLE_ORDER if r in by_role] + \
                  [r for r in sorted(by_role) if r not in ROLE_ORDER]
        for role in ordered:
            lines += [f"## {role}", ""]
            for date, anchor, mid in sorted(by_role[role]):
                mark = " **(anchor)**" if anchor else ""
                lines += [f"- {date} — {wiki(mid, titles, notenames)}{mark}"]
            lines += [""]
        (VAULT / "Chains" / f"{chain_slug}.md").write_text("\n".join(lines), encoding="utf-8")

    # Category hubs
    def write_hub(folder, name, items, heading):
        lines = [f"# {heading}", ""]
        lines += [f"- {d} — {wiki(m, titles, notenames)}" for d, m in sorted(items)] + [""]
        (VAULT / folder / f"{slug(name)}.md").write_text("\n".join(lines), encoding="utf-8")

    for s, items in by_subject.items():
        write_hub("Subjects", s, items, f"Subject: {s}")
    for sp, items in by_spirit.items():
        write_hub("Spirits", sp, items, f"Spirit: {sp}")
    for c, items in by_collection.items():
        write_hub("Collections", c, items, f"Collection: {c}")
    for mname, items in by_medium.items():
        write_hub("Mediums", mname, items, f"Medium: {mname}")
    for e, items in by_et.items():
        write_hub("Essential Teachings", e, items, f"Essential Teaching: {e}")

    # Ask the Archive
    lines = ["# Ask the Archive", "",
             "Every question the archive answers, grouped by subject area.",
             "Type any part of your question into Obsidian's search to find",
             "the message that answers it.", ""]
    total_q = 0
    for cat in sorted(questions_by_category):
        lines += [f"## {cat}", ""]
        for q, mid in sorted(set(questions_by_category[cat])):
            lines += [f"- {q} → {wiki(mid, titles, notenames)}"]
            total_q += 1
        lines += [""]
    (VAULT / "Ask the Archive.md").write_text("\n".join(lines), encoding="utf-8")

    # Subjects Index — the taxonomy as a linked tree
    data = yaml.safe_load(SUBJECTS_PATH.read_text(encoding="utf-8"))
    idx = ["# Subjects Index", "",
           "The archive's full subject hierarchy. Subjects with messages",
           "link to their hub pages.", ""]
    for cat in data.get("main_categories", []):
        n = cat["name"]
        idx.append(f"- {'[[Subjects/' + slug(n) + '|' + n + ']]' if n in by_subject else n}")
        for sub in cat.get("subcategories", []) or []:
            sn = sub["name"]
            idx.append(f"    - {'[[Subjects/' + slug(sn) + '|' + sn + ']]' if sn in by_subject else sn + ' *(no messages yet)*'}")
    idx.append("")
    (VAULT / "Subjects Index.md").write_text("\n".join(idx), encoding="utf-8")

    # Home
    home = [
        "# Divine Love Messages Archive", "",
        f"- **{len(messages)}** messages · **{len(chain_members)}** chains · "
        f"**{len(by_subject)}** subjects in use · **{total_q}** questions answered", "",
        "## Start here",
        "- [[Ask the Archive]] — search any question",
        "- [[Subjects Index]] — browse the full taxonomy",
        "- Browse the `Chains/` folder for the argument threads",
        "- Open the graph view; filter with `-path:\"Subjects\"` if hubs dominate", "",
    ]
    (VAULT / "Home.md").write_text("\n".join(home), encoding="utf-8")

    print(f"Vault built: {len(messages)} messages, {len(chain_members)} chain hubs, "
          f"{len(by_subject)} subject hubs, {total_q} questions indexed.")
    print("Preserved: .obsidian/ (your settings) and Notes/ (your own writing).")
    print(f"Open {VAULT.resolve()} as a vault in Obsidian.")


if __name__ == "__main__":
    main()