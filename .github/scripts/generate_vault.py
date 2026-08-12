#!/usr/bin/env python3
"""
generate_vault.py - build a derived Obsidian vault from the archive.

The repository stays canonical; this emits a disposable, regenerable vault
in ./obsidian-vault/ (add that folder to .gitignore). Never edit the vault
by hand - rerun this script after commits instead.

What it builds:
  Messages/<year>/<month>/<YYYY-MM-DD Message Title>.md   one note per
      message, mirroring the repository's year/month folders and FILENAMED
      DATE-FIRST so the file explorer sorts chronologically. The human
      title lives in the `title` property; install the community plugin
      "Front Matter Title" with ONLY its Graph feature enabled and the
      graph displays titles while the explorer keeps dated names.
      Wikilinks already display titles via aliases. (The message_id is
      preserved as a property and in the note body):
      - STRUCTURED PROPERTIES mirroring the archive schema: the original
        field names and values (message_id, date, spirit, medium, location,
        message_type, primary_subject, secondary_subjects, keywords,
        collections, essential_teachings, chains, mentions), with wikilinks
        inside properties wherever a hub page exists - so the metadata is
        searchable per-field ( ["primary_subject":Mind] ), browsable, and
        feeds the graph, without collapsing anything into tags
      - title property and alias so wikilinks display the human title
      - excerpt as an epigraph above the text (the spirit's own words as
        the threshold; the door stays on browse surfaces, not here), then
        the full message text, then the description as an afterword,
        related-message wikilinks, chain wikilinks, and "Questions this
        message answers" (full-text searchable)
  Subjects Index.md                 the full subjects.yml hierarchy as a
      linked tree - the taxonomy browser, replacing the old nested tags
  Chains/<Display Title>.md         one hub per thread: theme, argument, a
      structural-health line (member count, missing Foundation/anchor,
      unconfirmed back-search roles), then members grouped in role-section
      order (Foundation first), chronological within each section, anchors
      marked (anchor). Each member carries the curator's EVIDENCE PROSE from
      chains-log.md - the facet claimed, the quoted passage, the fence - plus
      the log line number to edit at the source. Witness- and sighting-level
      NOTEs are listed at the foot rather than discarded.
  Chains Index.md                   all threads in two tables, those with
      structural gaps first, so an incomplete chain is visible in one scan
  Subjects/<Name>.md, Spirits/<Display Name>.md, Collections/<Name>.md
      category hub pages, FILENAMED BY DISPLAY NAME so the explorer,
      graph, and quick switcher read in human language (no plugin needed
      for hubs; spirit and chain hubs carry their id/slug as an alias).
      Each lists its member messages (filter these out of the graph
      with  -path:"Subjects"  etc. if the hubs dominate)
  Ask the Archive.md                every question in the archive, grouped
      by top-level subject category, each linking to its answering message
  Books/, Practices/, Talks/        carried verbatim from content/, each as
      its own top-level folder, internal structure preserved (see
      CONTENT_MIRROR)
  Browse.md                         the browse page, carried to the top
      level of the vault as a standalone note (see CONTENT_PAGES)
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
CONTENT_DIR = ROOT / "content"
MESSAGES_DIR = CONTENT_DIR / "messages"

# Content folders carried into the vault verbatim, as their own top-level
# folders: {source directory under content/: vault folder name}. Messages,
# collections and essential teachings are deliberately absent, since the
# script builds richer notes for those; templates are scaffolding, not
# archive content. Add a pair here to carry a new folder across.
CONTENT_MIRROR = {
    "books": "Books",
    "practices": "Practices",
    "talks": "Talks",
}

# Standalone pages copied to the top level of the vault, rather than into a
# folder: {source path under content/: vault filename}. content/browse.md is
# written by generate_browse.py, so run that first if the browse page is
# stale.
CONTENT_PAGES = {
    "browse.md": "Browse.md",
}
SUBJECTS_PATH = ROOT / "metadata" / "subjects.yml"
SPIRITS_DIR = ROOT / "spirits"
MEDIUMS_DIR = ROOT / "mediums"
GEN_COLLECTIONS = ROOT / ".github" / "scripts" / "generate_collections.py"
GEN_ET = ROOT / ".github" / "scripts" / "generate_essential_teachings.py"
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


def load_profiles(directory):
    """spirits/*.yml or mediums/*.yml -> {file_stem: {display, aliases,
    description, notes}}. Field names vary slightly across files, so read
    the likely keys defensively."""
    profiles = {}
    if not directory.exists():
        return profiles
    for p in sorted(directory.glob("*.yml")):
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        display = d.get("name") or d.get("spirit_name") or d.get("display_name") \
            or p.stem.replace("-", " ").title()
        desc = d.get("description") or d.get("spirit_description") \
            or d.get("bio") or ""
        aliases = d.get("aliases") or []
        notes = d.get("notes") or ""
        profiles[p.stem] = {"display": display, "aliases": aliases,
                            "description": str(desc).strip(),
                            "notes": str(notes).strip()}
    return profiles


def load_definitions_from_generator(script_path):
    """
    The collection / essential-teaching definitions are the single source of
    truth inside the generator scripts (generate_collections.py,
    generate_essential_teachings.py) as a module-level DESCRIPTIONS dict.
    Import the script in isolation and read that dict, so the vault always
    matches exactly what the site's own browse pages use. Returns {name: text}.
    """
    if not script_path.exists():
        return {}
    import importlib.util
    try:
        spec = importlib.util.spec_from_file_location(
            f"_gen_{script_path.stem}", script_path)
        mod = importlib.util.module_from_spec(spec)
        # These scripts guard execution behind __main__, so importing is safe.
        spec.loader.exec_module(mod)
        desc = getattr(mod, "DESCRIPTIONS", {}) or {}
        return {k: " ".join(str(v).split()) for k, v in desc.items()}
    except Exception as e:
        print(f"  (could not read definitions from {script_path.name}: {e})")
        return {}


def load_subject_definitions():
    """{name: definition} plus {parent: [children]} from subjects.yml."""
    data = yaml.safe_load(SUBJECTS_PATH.read_text(encoding="utf-8"))
    defs, children = {}, {}
    for cat in data.get("main_categories", []):
        defs[cat["name"]] = str(cat.get("definition") or "").strip()
        kids = [s["name"] for s in cat.get("subcategories", []) or []]
        children[cat["name"]] = kids
        for sub in cat.get("subcategories", []) or []:
            defs[sub["name"]] = str(sub.get("definition") or "").strip()
    return defs, children


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


def _clean_evidence(text):
    """
    Tidy the prose that follows a member line's **[Role]** marker so it reads
    as a sentence in the hub: drop the leading separator colon, collapse the
    hard-wrapped continuation whitespace, and trim.
    """
    t = re.sub(r"^\s*:\s*", "", text or "")
    return re.sub(r"\s+", " ", t).strip()


PRIVATE_MARKER = " -- "


def split_evidence(text):
    """
    Split a log entry's prose into (public, private) at the ' -- ' marker.

    Everything before the marker is reader-facing and appears on the
    published chain hubs. Everything after it is curatorial: demote-if
    conditions, judgment calls addressed to the curator, notes about what an
    earlier pass missed. That half is parsed and kept, but written only to
    the working mirror, which is excluded from Obsidian Publish.

    An entry with no marker is entirely public, so the convention costs
    nothing on entries that do not need it.
    """
    if not text:
        return "", ""
    head, sep, tail = text.partition(PRIVATE_MARKER)
    return head.strip(), tail.strip() if sep else ""


def open_capital(text):
    """
    Capitalize the opening letter of an entry's public prose.

    Log entries are often written as continuations of the role marker
    ("maps the two paths onto the two minds..."), which reads fine in the
    log but looks like a fragment once the prose stands on its own in a
    published hub. Left alone when the entry opens with a code span (a
    slug) or with quoted words from a message, since altering either would
    misrepresent it.
    """
    if not text:
        return text
    first = text[0]
    if first in "`\"'\u201c\u2018[(" or not first.isalpha():
        return text
    return first.upper() + text[1:]


def parse_chain_memberships():
    """
    From chains-log.md: two products, both keyed by message_id.

      members[mid]  -> [(slug, role, is_anchor, evidence, log_line)]
      notes[mid]    -> [(slug, tier, evidence, log_line)]

    Member lines are the bold ones (- `slug` **[Role...]**) and are the only
    thing that feeds the graph and the role sections, unchanged from before.
    NOTE lines (- NOTE (tier, `slug`): ...) are now captured too, so the
    witnesses and sightings that were previously discarded can be listed at
    the foot of each chain hub instead of being findable only by grepping
    the log.

    `evidence` is the curator's prose for that line: the facet claimed, the
    quoted passage, the fence, the demote-if condition. `log_line` is the
    1-based line number in chains-log.md, so a hub can point at the exact
    spot to edit when a correction is needed.

    Continuation lines (hard-wrapped, two-space indented) are folded into
    the entry they belong to, so the parser is indifferent to whether an
    entry was written on one line or wrapped across many.
    """
    members = defaultdict(list)
    notes = defaultdict(list)
    if not CHAINS_LOG.exists():
        return members, notes

    current_id = None
    pending = None          # ("member"|"note", target_list, index) to append to

    def flush_continuation(raw):
        """Append a wrapped continuation line to whatever entry is open."""
        if pending is None:
            return False
        kind, bucket, idx = pending
        row = list(bucket[idx])
        row[-2] = _clean_evidence(row[-2] + " " + raw)
        bucket[idx] = tuple(row)
        return True

    for lineno, line in enumerate(CHAINS_LOG.read_text(encoding="utf-8").splitlines(), 1):
        # Heading format per schema.md: "### id | Title | date", with an
        # optional trailing bracketed tag after the date (e.g.
        # [back-search]), which re.match ignores as an unanchored suffix.
        # The log was migrated to pipes on 2026-07-19; legacy separator
        # support has been retired.
        h = re.match(r"### (\S+) \| .+ \| \d{4}-\d{2}-\d{2}", line)
        if h:
            current_id = h.group(1)
            pending = None
            continue

        m = re.match(r"- `([a-z0-9-]+)` \*\*\[([^\]]+)\]\*\*(.*)", line)
        if m and current_id:
            chain_slug = m.group(1)
            role = m.group(2).split()[0].split(";")[0].split(",")[0]
            role = role.replace("\u2014", "").strip() or "Elaboration"
            tail = m.group(2) + m.group(3)
            anchor = "presumptive anchor" in tail.lower() \
                     or "presumptive section anchor" in tail.lower() \
                     or "anchor upgraded" in tail.lower()
            members[current_id].append(
                (chain_slug, role, anchor, _clean_evidence(m.group(3)), lineno))
            pending = ("member", members[current_id], len(members[current_id]) - 1)
            continue

        # NOTE lines, three shapes seen in the log:
        #   - NOTE (witness, `slug`): prose      current convention
        #   - NOTE: prose mentioning `slug`      earlier entries
        #   - (holding, candidate `slug` ...)    parenthetical observations
        # The tier is read from the parenthetical when present; the slug is
        # taken from the parenthetical first, then from the prose. A note
        # with no slug anywhere is kept under "(general)" and reported by
        # the lint pass rather than silently dropped.
        n = re.match(r"- NOTE\s*\(([^)]*)\)\s*:?\s*(.*)", line) \
            or re.match(r"- NOTE\s*:\s*()(.*)", line) \
            or re.match(r"- \(([^)]*)\)\s*:?\s*(.*)", line)
        if n and current_id:
            inside, prose = n.group(1), n.group(2)
            s = re.search(r"`([a-z0-9-]+)`", inside) or \
                re.search(r"`([a-z0-9-]+)`", prose)
            note_slug = s.group(1) if s else "(general)"
            tier = (inside.split(",")[0].strip() if inside else "") or "note"
            notes[current_id].append(
                (note_slug, tier, _clean_evidence(prose or inside), lineno))
            pending = ("note", notes[current_id], len(notes[current_id]) - 1)
            continue

        if line.startswith("  ") and line.strip():
            flush_continuation(line.strip())
            continue

        if not line.strip():
            pending = None

    return members, notes


def wiki(msg_id, titles, notenames):
    """Link by note filename; display the human title."""
    name = notenames.get(msg_id, msg_id)
    title = titles.get(msg_id, msg_id)
    return f"[[{name}|{title}]]" if name != title else f"[[{name}]]"


MSGID_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2}-[a-z]{2}-[a-z][a-z0-9-]*)\b")


def linkify_ids(text, notenames):
    """
    Replace bare message_id strings in prose with wikilinks that jump to the
    message note while DISPLAYING the id exactly as written. Only ids present
    in `notenames` (real messages) are linked; anything that merely looks
    id-shaped but is not a known message is left untouched, so no false edges
    are created. Ids already inside a [[...]] wikilink are skipped.
    """
    if not text:
        return text
    out, last = [], 0
    for m in MSGID_RE.finditer(text):
        mid = m.group(1)
        # skip if this id is already inside a wikilink (preceded by [[ )
        if text[max(0, m.start() - 2):m.start()] == "[[":
            continue
        if mid in notenames:
            out.append(text[last:m.start()])
            name = notenames[mid]
            out.append(f"[[{name}|{mid}]]")
            last = m.end()
    out.append(text[last:])
    return "".join(out)


MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+?)(?:\s+\"[^\"]*\")?\)")


def rewrite_carried_links(text, notenames, hub_targets):
    """
    Rewrite a carried page's web links into vault wikilinks.

    Pages under content/ (browse.md, books, practices, talks) are written for
    the published website, so their links are site-relative paths like
    `messages/2019/01/2019-01-21-af-augustine.md`. Those resolve on the web
    and nowhere in Obsidian, whose notes are named for their titles. Every
    link whose target carries a known message_id becomes a wikilink to that
    note, keeping the original link text as the display text; links to other
    known destinations (spirits, collections, subjects) resolve through
    `hub_targets`. Anything unrecognised (external URLs, anchors, assets) is
    left exactly as written.
    """
    if not text:
        return text, 0, 0

    fixed = rewritten = 0

    def repl(m):
        nonlocal fixed, rewritten
        label, target = m.group(1), m.group(2)
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        stem = target.split("#")[0].rstrip("/").split("/")[-1]
        stem = re.sub(r"\.(md|html?)$", "", stem)
        if stem in notenames:
            fixed += 1
            return f"[[{notenames[stem]}|{label}]]"
        key = (target.split("#")[0].strip("/").lower(), stem.lower())
        for k in key:
            if k in hub_targets:
                rewritten += 1
                return f"[[{hub_targets[k]}|{label}]]"
        return m.group(0)

    out = MD_LINK_RE.sub(repl, text)
    return out, fixed, rewritten


def main():
    if not MESSAGES_DIR.exists():
        print("Run from the repository root (content/messages not found).")
        sys.exit(1)

    parents = load_subject_hierarchy()
    subj_defs, subj_children = load_subject_definitions()
    spirit_profiles = load_profiles(SPIRITS_DIR)
    medium_profiles = load_profiles(MEDIUMS_DIR)
    collection_defs = load_definitions_from_generator(GEN_COLLECTIONS)
    et_defs = load_definitions_from_generator(GEN_ET)
    registry = parse_chain_registry()
    memberships, chain_notes_log = parse_chain_memberships()

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

    # Hub notes are FILENAMED BY DISPLAY NAME ("Spirits/John the Beloved.md",
    # "Chains/Who Jesus Was.md", "Collections/Mind & Soul.md") so the file
    # explorer, graph, and quick switcher all read in human language with no
    # plugin needed. These maps resolve ids/slugs to note names, and
    # disambiguate the rare display-name collision with the id in parens.
    def display_map(pairs):
        """[(key, display)] -> {key: (note_name, display)}, collision-safe."""
        out, taken = {}, set()
        for key, disp in sorted(pairs):
            name = filename(disp)
            if name.lower() in taken:
                name = f"{name} ({key})"
            taken.add(name.lower())
            out[key] = (name, disp)
        return out

    all_spirit_ids = set(spirit_profiles)
    for _mid, (_fm, _b) in messages.items():
        if _fm.get("spirit_id"):
            all_spirit_ids.add(_fm["spirit_id"])
        all_spirit_ids.update(_fm.get("spirits") or [])
    spirit_notes = display_map(
        (sp, spirit_profiles.get(sp, {}).get("display")
             or sp.replace("-", " ").title())
        for sp in all_spirit_ids)

    def spirit_link(sp, label=None):
        name, disp = spirit_notes.get(sp, (sp, sp))
        return f"[[Spirits/{name}|{label or disp}]]"

    all_chain_slugs = set(registry)
    for _mems in memberships.values():
        all_chain_slugs.update(cs for cs, _r, _a, _e, _l in _mems)
    for _nts in chain_notes_log.values():
        all_chain_slugs.update(cs for cs, _t, _e, _l in _nts
                               if cs != "(general)")
    chain_notes = display_map(
        (cs, cs.replace("-", " ").title()) for cs in all_chain_slugs)

    def chain_link(cs):
        name, _disp = chain_notes.get(cs, (cs, cs))
        return f"[[Chains/{name}]]"

    # Note filenames are DATE-PREFIXED titles ("YYYY-MM-DD Title") so the
    # file explorer sorts chronologically; the graph shows the human title
    # via the `title` property + the Front Matter Title plugin (Graph
    # feature only). Two messages may still collide (same date AND title),
    # so disambiguate with the message_id, and keep a map from
    # message_id -> note name for every link the vault emits.
    notenames = {}
    folders = {}          # message_id -> "YYYY/MM"
    used = defaultdict(set)   # folder -> {lowercase filenames already taken}
    for mid in sorted(messages):
        date = str(messages[mid][0].get("date", ""))
        year = date[:4] or "undated"
        month = date[5:7] or "00"
        folder = f"{year}/{month}"
        folders[mid] = folder
        base = filename(titles[mid])
        if date:
            base = f"{date} {base}"
        key = base.lower()
        # Disambiguate only against files landing in the SAME folder.
        if key in used[folder]:
            base = f"{base} ({mid})"
            key = base.lower()
        used[folder].add(key)
        notenames[mid] = base

    # Rebuild ONLY the generated folders. Everything else in the vault -
    # your Obsidian config in .obsidian/, and anything you write in Notes/ -
    # is preserved across runs and never touched by this script.
    GENERATED = ["Messages", "Chains", "Chains (working)", "Subjects",
                 "Spirits", "Collections", "Mediums", "Essential Teachings"]
    GENERATED += [v for k, v in CONTENT_MIRROR.items()
                  if (CONTENT_DIR / k).is_dir()]
    GENERATED_FILES = ["Ask the Archive.md", "Subjects Index.md", "Home.md",
                       "Chains Index.md"]
    GENERATED_FILES += sorted(set(CONTENT_PAGES.values()))
    VAULT.mkdir(exist_ok=True)
    for d in GENERATED:
        p = VAULT / d
        if p.exists():
            shutil.rmtree(p)
        p.mkdir(parents=True)
    for f in GENERATED_FILES:
        (VAULT / f).unlink(missing_ok=True)
    # A configured content/ folder that no longer exists would otherwise
    # leave its vault folder behind from an earlier run, so clear those too.
    for vault_name in CONTENT_MIRROR.values():
        stale = VAULT / vault_name
        if stale.exists() and vault_name not in GENERATED:
            shutil.rmtree(stale)

    # Carry the configured content/ folders and standalone pages into the
    # vault verbatim, preserving internal structure. These are generated
    # output in the repository, so they are copied rather than rebuilt: the
    # repository stays the single source of truth.
    # Map the website's own path segments onto vault hub notes, so a carried
    # page's links to spirits, collections and subjects resolve as well.
    hub_targets = {}
    for sp, (nname, _disp) in spirit_notes.items():
        hub_targets[sp.lower()] = f"Spirits/{nname}"
        hub_targets[f"spirits/{sp}".lower()] = f"Spirits/{nname}"
    for cs, (nname, _disp) in chain_notes.items():
        hub_targets[cs.lower()] = f"Chains/{nname}"
    for cname in collection_defs:
        hub_targets[slug(cname)] = f"Collections/{filename(cname)}"
        hub_targets[f"collections/{slug(cname)}"] = f"Collections/{filename(cname)}"

    mirrored, mirrored_into, missing = 0, [], []
    links_fixed = 0

    def carry(src_file, dest):
        """Copy one file, rewriting links if it is markdown."""
        nonlocal links_fixed
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src_file.suffix.lower() == ".md":
            body = src_file.read_text(encoding="utf-8")
            body, a, b = rewrite_carried_links(body, notenames, hub_targets)
            dest.write_text(body, encoding="utf-8")
            links_fixed += a + b
        else:
            shutil.copy2(src_file, dest)
    for src_name, vault_name in CONTENT_MIRROR.items():
        src = CONTENT_DIR / src_name
        if not src.is_dir():
            missing.append(f"content/{src_name}")
            continue
        n = 0
        for f in sorted(src.rglob("*")):
            if not f.is_file() or f.name.startswith("."):
                continue
            carry(f, VAULT / vault_name / f.relative_to(src))
            n += 1
        mirrored += n
        mirrored_into.append(f"{vault_name} ({n})")
    pages_done = set()
    for src_name, vault_name in CONTENT_PAGES.items():
        src = CONTENT_DIR / src_name
        if vault_name in pages_done or not src.is_file():
            continue
        carry(src, VAULT / vault_name)
        pages_done.add(vault_name)
        mirrored += 1
        mirrored_into.append(vault_name)
    for vault_name in sorted(set(CONTENT_PAGES.values()) - pages_done):
        missing.append(vault_name)
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
    by_mention = defaultdict(list)    # spirit_id -> messages that mention them
    by_collection = defaultdict(list)
    by_medium = defaultdict(list)
    by_et = defaultdict(list)
    questions_by_category = defaultdict(list)
    chain_members = defaultdict(list)     # slug -> [(role, anchor, msg_id, date, evidence, log_line)]
    chain_witnesses = defaultdict(list)   # slug -> [(date, msg_id, tier, evidence, log_line)]

    # Pass 2: write message notes
    for mid, (fm, body) in sorted(messages.items()):
        date = str(fm.get("date", ""))
        spirit = fm.get("spirit_name") or fm.get("spirit_id", "")
        subjects = [fm.get("primary_subjects")] if fm.get("primary_subjects") else []
        subjects += [s for s in (fm.get("secondary_subjects") or []) if s]
        for chain_slug, role, anchor, evidence, log_line in memberships.get(mid, []):
            chain_members[chain_slug].append(
                (role, anchor, mid, date, evidence, log_line))
        for chain_slug, tier, evidence, log_line in chain_notes_log.get(mid, []):
            if chain_slug != "(general)":
                chain_witnesses[chain_slug].append(
                    (date, mid, tier, evidence, log_line))

        def q(v):
            return '"' + str(v).replace('"', "'") + '"'

        def subj_link(name):
            return q(f"[[Subjects/{filename(name)}|{name}]]")

        loc = fm.get("location") or {}
        loc_str = ", ".join(x for x in [loc.get("city"), loc.get("region"),
                                        loc.get("country")] if x)
        props = ["---",
                 f"title: {q(titles[mid])}",
                 f"message_id: {mid}",
                 f"aliases: [{mid}]",
                 f"date: {date}",
                 f"spirit: {q(spirit_link(fm.get('spirit_id',''), fm.get('spirit_name')))}",
                 f"medium: {q('[[Mediums/' + filename(fm.get('medium','')) + '|' + fm.get('medium','') + ']]')}",
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
            props += [f"  - {q('[[Collections/' + filename(c) + '|' + c + ']]')}" for c in colls]
        ets = fm.get("essential_teachings") or []
        if ets:
            props.append("essential_teachings:")
            props += [f"  - {q('[[Essential Teachings/' + filename(e) + '|' + e + ']]')}" for e in ets]
        mem_props = memberships.get(mid, [])
        if mem_props:
            props.append("chains:")
            props += [f"  - {q(chain_link(cs))}" for cs, *_ in mem_props]
        mentions = fm.get("spirits") or []
        if mentions:
            props.append("mentions:")
            props += [f"  - {q(spirit_link(sp))}" for sp in mentions]
        if fm.get("canonical_url"):
            props.append(f"canonical_url: {q(fm['canonical_url'])}")
        lines = props + ["---",
                 "",
                 f"# {titles[mid]}",
                 "",
                 f"**Spirit:** {spirit_link(fm.get('spirit_id',''), spirit)} · "
                 f"**Medium:** {fm.get('medium','')} · **Date:** {date}",
                 ""]
        # --- Reading order: excerpt, message, description, related, chains,
        # questions. The door is deliberately NOT shown here: the message
        # page lets the text interpret itself (excerpt = the spirit's own
        # words as epigraph). Doors live on browse surfaces where the
        # invitation belongs.
        excerpt = (fm.get("excerpt") or "").strip()
        if excerpt:
            # italicised, line by line so multi-line excerpts stay in italics
            lines += [f"*{e}*" for e in excerpt.splitlines() if e.strip()] + [""]

        lines += ["---", "", body.strip(), "", "---", ""]

        desc = (fm.get("description") or "").strip()
        if desc:
            lines += ["> [!abstract] Description"]
            lines += [f"> {d}" for d in desc.splitlines() if d.strip()] + [""]

        rel = fm.get("related_messages") or []
        if rel:
            lines += ["## Related messages", ""]
            lines += [f"- {wiki(r, titles, notenames)}" for r in rel] + [""]
        mem = memberships.get(mid, [])
        if mem:
            lines += ["## Chains", ""]
            for chain_slug, role, anchor, _ev, _ln in mem:
                mark = " **(anchor)**" if anchor else ""
                lines += [f"- {chain_link(chain_slug)} - {role}{mark}"]
            lines += [""]
        qs = fm.get("questions") or []
        if qs:
            # collapsed by default: the ">%" foldable callout keeps the
            # reading view clean while remaining fully searchable and visible
            lines += ["> [!question]- Questions this message answers"]
            lines += [f"> - {q}" for q in qs] + [""]
            top = parents.get(subjects[0]) or subjects[0] if subjects else "General"
            for q in qs:
                questions_by_category[top].append((q, mid))

        out_dir = VAULT / "Messages" / folders[mid]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{notenames[mid]}.md").write_text(
            "\n".join(lines), encoding="utf-8")

        for s in subjects:
            by_subject[s].append((date, mid))
        by_spirit[fm.get("spirit_id", "unknown")].append((date, mid))
        for sp in mentions:
            by_mention[sp].append((date, mid))
        for c in fm.get("collections") or []:
            by_collection[c].append((date, mid))
        by_medium[fm.get("medium", "Unknown")].append((date, mid))
        for e in ets:
            by_et[e].append((date, mid))

    # Chain hubs
    #
    # Each hub is the chain as it currently stands: the argument it traces,
    # then the members grouped in role-section order and chronological within
    # each section, EACH WITH THE CURATOR'S EVIDENCE PROSE from chains-log.md
    # (the facet claimed, the quoted passage, the fence, any demote-if
    # condition). A structural-health line sits at the top so gaps are
    # visible without reading the whole hub, and every entry carries its
    # chains-log.md line number so a correction can be made at the source.
    # Witness- and sighting-level NOTEs are listed at the foot rather than
    # discarded.
    health_rows = []          # for the Chains Index
    for chain_slug in sorted(set(chain_members) | set(chain_witnesses)):
        mem = chain_members.get(chain_slug, [])
        cname, cdisp = chain_notes.get(chain_slug, (chain_slug, chain_slug))
        theme, argument = registry.get(chain_slug, ("", ""))

        by_role = defaultdict(list)
        for role, anchor, mid, date, evidence, log_line in mem:
            by_role[role].append((date, anchor, mid, evidence, log_line))

        provisional = sum(1 for _r, _a, _m, _d, ev, _l in mem
                          if "[back-search]" in ev.lower())
        has_foundation = "Foundation" in by_role
        has_anchor = any(a for _r, a, _m, _d, _e, _l in mem)
        minted = chain_slug in registry
        flags = []
        # Flag wording is reader-facing (this vault is published), so it
        # says what is missing in plain language rather than in the log's
        # working vocabulary.
        if not minted:
            flags.append("still being gathered")
        if not has_foundation:
            flags.append("opening message not yet identified")
        if not has_anchor:
            flags.append("main statement not yet chosen")
        if provisional:
            flags.append(f"{provisional} message(s) awaiting a full reading")
        if mem and all(r in ("Testimony",) for r, *_ in mem):
            flags.append("first-hand accounts only so far")
        health_rows.append((chain_slug, cname, cdisp, len(mem),
                            len(chain_witnesses.get(chain_slug, [])), flags))

        # Two renderings of the same chain: the public hub carries only the
        # reader-facing half of each entry; the working mirror carries
        # everything, including the curatorial asides. Exclude the
        # "Chains (working)" folder in Obsidian Publish.
        lines = ["---", f"aliases: [{chain_slug}]", "---", "",
                 f"# Chain: {cdisp}", ""]
        work = ["---", f"aliases: [{chain_slug} working]", "---", "",
                f"# Chain (working): {cdisp}", "",
                f"Curatorial view of [[Chains/{cname}|{cdisp}]]. "
                "Not published.", ""]
        if theme:
            lines += [f"> {theme}", ""]
        if argument:
            lines += [f"**The argument it traces:** {argument}", ""]

        status = f"**{len(mem)}** messages"
        if chain_witnesses.get(chain_slug):
            status += f" · **{len(chain_witnesses[chain_slug])}** supporting"
        status += " · " + ("; ".join(flags) if flags else "complete")
        lines += [status, "", "---", ""]

        ordered = [r for r in ROLE_ORDER if r in by_role] + \
                  [r for r in sorted(by_role) if r not in ROLE_ORDER]
        for role in ordered:
            lines += [f"## {role}", ""]
            work += [f"## {role}", ""]
            for date, anchor, mid, evidence, log_line in sorted(by_role[role]):
                mark = " **(anchor)**" if anchor else ""
                pub, priv = split_evidence(evidence)
                head = f"### {date} - {wiki(mid, titles, notenames)}{mark}"
                # The chains-log.md line reference is a curator's tool, so it
                # appears only in the working mirror; the published hub shows
                # the evidence alone.
                ref = f"<small>[{log_line}]</small>"
                lines += [head, "", linkify_ids(open_capital(pub), notenames), ""]
                work += [head, "",
                         f"{linkify_ids(pub, notenames)} {ref}".strip(), ""]
                if priv:
                    work += ["> [!note] Curator",
                             "> " + linkify_ids(priv, notenames), ""]

        wits = chain_witnesses.get(chain_slug, [])
        if wits:
            lines += ["---", "", "## Also touches on this", "",
                      "*These messages restate or echo the idea rather than "
                      "carry it forward, so they sit alongside the thread "
                      "rather than in it.*", ""]
            work += ["---", "", "## Also touches on this", ""]
            for date, mid, tier, evidence, log_line in sorted(wits):
                head = f"- **{date}** {wiki(mid, titles, notenames)} ({tier})"
                pub, priv = split_evidence(evidence)
                lines += [f"{head} - {linkify_ids(open_capital(pub), notenames)}"]
                work += [f"{head} - {linkify_ids(pub, notenames)}"
                         + (f" **[curator]** {linkify_ids(priv, notenames)}" if priv else "")
                         + f" <small>[{log_line}]</small>"]
            lines += [""]
            work += [""]

        (VAULT / "Chains" / f"{cname}.md").write_text("\n".join(lines), encoding="utf-8")
        (VAULT / "Chains (working)" / f"{cname}.md").write_text("\n".join(work), encoding="utf-8")

    # Chains Index: every thread with its structural health, so gaps are
    # visible in one scan instead of one hub at a time.
    idx_lines = ["# Chains Index", "",
                 f"**{len(health_rows)}** threads traced so far. Each follows a "
                 "single idea across the archive, in the order the messages "
                 "were given. This layer is a work in progress: threads still "
                 "being gathered are listed first, with what they are waiting "
                 "for.", ""]
    needs_work = [r for r in health_rows if r[5]]
    if needs_work:
        idx_lines += ["## Still being gathered", "",
                      "| Thread | Messages | Supporting | Waiting for |",
                      "|---|---|---|---|"]
        for cslug, cname, cdisp, nmem, nwit, flags in needs_work:
            idx_lines.append(
                f"| [[Chains/{cname}\\|{cdisp}]] | {nmem} | {nwit} | {'; '.join(flags)} |")
        idx_lines.append("")
    clean = [r for r in health_rows if not r[5]]
    if clean:
        idx_lines += ["## Complete", "",
                      "| Thread | Messages | Supporting |", "|---|---|---|"]
        for cslug, cname, cdisp, nmem, nwit, flags in clean:
            idx_lines.append(
                f"| [[Chains/{cname}\\|{cdisp}]] | {nmem} | {nwit} |")
        idx_lines.append("")
    (VAULT / "Chains Index.md").write_text("\n".join(idx_lines), encoding="utf-8")

    # Category hubs - each opens with its definition / biography, then messages
    def write_hub(folder, name, items, heading, intro=None):
        lines = [f"# {heading}", ""]
        if intro:
            lines += intro
        lines += [f"## Messages ({len(items)})", ""]
        lines += [f"- {d} - {wiki(m, titles, notenames)}" for d, m in sorted(items)] + [""]
        (VAULT / folder / f"{filename(name)}.md").write_text("\n".join(lines), encoding="utf-8")

    for s, items in by_subject.items():
        intro = []
        if subj_defs.get(s):
            intro += [f"> {subj_defs[s]}", ""]
        parent = parents.get(s)
        if parent:
            plink = f"[[Subjects/{filename(parent)}|{parent}]]" if parent in by_subject else parent
            intro += [f"Part of: {plink}", ""]
        kids = subj_children.get(s) or []
        if kids:
            intro += ["Subcategories: " + " · ".join(
                f"[[Subjects/{filename(k)}|{k}]]" if k in by_subject else f"{k}"
                for k in kids), ""]
        write_hub("Subjects", s, items, f"Subject: {s}", intro)

    # A spirit deserves a hub page if they delivered a message, are mentioned
    # in one, or have a curated profile file - otherwise mentions: wikilinks
    # (e.g. [[Spirits/sri-yukteswar]]) dangle as empty unresolved notes.
    for sp in sorted(set(by_spirit) | set(by_mention) | set(spirit_profiles)):
        prof = spirit_profiles.get(sp, {})
        sname, sdisp = spirit_notes.get(
            sp, (filename(sp.replace("-", " ").title()),
                 sp.replace("-", " ").title()))
        lines = ["---", f"aliases: [{sp}]", "---", "",
                 f"# {sdisp}", ""]
        if prof.get("aliases"):
            lines += ["*Also known as: " + ", ".join(prof["aliases"]) + "*", ""]
        if prof.get("description"):
            lines += [linkify_ids(prof["description"], notenames), ""]
        if prof.get("notes"):
            lines += ["## From the archive's notes", "",
                      linkify_ids(prof["notes"], notenames), ""]
        delivered = by_spirit.get(sp, [])
        if delivered:
            lines += [f"## Messages ({len(delivered)})", ""]
            lines += [f"- {d} - {wiki(m, titles, notenames)}"
                      for d, m in sorted(delivered)] + [""]
        mentioned = by_mention.get(sp, [])
        if mentioned:
            lines += [f"## Mentioned in ({len(mentioned)})", ""]
            lines += [f"- {d} - {wiki(m, titles, notenames)}"
                      for d, m in sorted(mentioned)] + [""]
        (VAULT / "Spirits" / f"{sname}.md").write_text(
            "\n".join(lines), encoding="utf-8")

    for c, items in by_collection.items():
        intro = [f"> {collection_defs[c]}", ""] if collection_defs.get(c) else []
        write_hub("Collections", c, items, f"Collection: {c}", intro)

    for mname, items in by_medium.items():
        prof = medium_profiles.get(slug(mname), {})
        intro = []
        if prof.get("description"):
            intro += [linkify_ids(prof["description"], notenames), ""]
        if prof.get("notes"):
            intro += ["## From the archive's notes", "",
                      linkify_ids(prof["notes"], notenames), ""]
        write_hub("Mediums", mname, items, f"Medium: {mname}", intro)

    for e, items in by_et.items():
        intro = [f"> {et_defs[e]}", ""] if et_defs.get(e) else []
        write_hub("Essential Teachings", e, items, f"Essential Teaching: {e}", intro)

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

    # Subjects Index - the taxonomy as a linked tree
    data = yaml.safe_load(SUBJECTS_PATH.read_text(encoding="utf-8"))
    idx = ["# Subjects Index", "",
           "The archive's full subject hierarchy. Subjects with messages",
           "link to their hub pages.", ""]
    for cat in data.get("main_categories", []):
        n = cat["name"]
        idx.append(f"- {'[[Subjects/' + filename(n) + '|' + n + ']]' if n in by_subject else n}")
        for sub in cat.get("subcategories", []) or []:
            sn = sub["name"]
            idx.append(f"    - {'[[Subjects/' + filename(sn) + '|' + sn + ']]' if sn in by_subject else sn + ' *(no messages yet)*'}")
    idx.append("")
    (VAULT / "Subjects Index.md").write_text("\n".join(idx), encoding="utf-8")

    # Home
    home = [
        "# Divine Love Messages Archive", "",
        f"- **{len(messages)}** messages · **{len(chain_members)}** chains · "
        f"**{len(by_subject)}** subjects in use · **{total_q}** questions answered", "",
        "## Start here",
        "- [[Ask the Archive]] - search any question",
        "- [[Subjects Index]] - browse the full taxonomy",
        "- [[Chains Index]] - every thread, with structural gaps flagged",
        "- Browse the `Chains/` folder for the argument threads",
        "- Open the graph view; filter with `-path:\"Subjects\"` if hubs dominate", "",
    ]
    (VAULT / "Home.md").write_text("\n".join(home), encoding="utf-8")

    # Lint pass over chains-log.md: report rather than drop silently.
    orphan_ids = sorted(mid for mid in set(memberships) | set(chain_notes_log)
                        if mid not in messages)
    slugless = [(mid, ln) for mid, nts in chain_notes_log.items()
                for cs, _t, _e, ln in nts if cs == "(general)"]
    unregistered = sorted({cs for cs, *_ in
                           ((c, ) for v in memberships.values() for c, *_r in v)}
                          - set(registry))
    if orphan_ids:
        print(f"chains-log lint: {len(orphan_ids)} entry id(s) with no message "
              f"file: {', '.join(orphan_ids[:5])}"
              + (" ..." if len(orphan_ids) > 5 else ""))
    if unregistered:
        print(f"chains-log lint: {len(unregistered)} slug(s) used in member "
              f"lines but absent from the registry table: {', '.join(unregistered)}")
    if slugless:
        print(f"chains-log lint: {len(slugless)} NOTE line(s) with no slug "
              f"(not shown on any chain hub); first at line {slugless[0][1]}")

    written = sum(1 for _ in (VAULT / "Messages").rglob("*.md"))
    if written != len(messages):
        print(f"WARNING: {len(messages)} messages loaded but {written} notes written "
              f"- a filename collision may have overwritten a note.")
    print(f"Vault built: {len(messages)} messages, {len(chain_members)} chain hubs, "
          f"{len(by_subject)} subject hubs, {total_q} questions indexed.")
    if mirrored_into:
        print(f"Carried from content/: {mirrored} file(s) into "
              f"{', '.join(mirrored_into)}; {links_fixed} link(s) rewritten "
              f"as wikilinks.")
    if missing:
        print(f"NOTE: configured but not found, nothing carried: "
              f"{', '.join(missing)}.")
    print("Preserved: .obsidian/ (your settings) and Notes/ (your own writing).")
    print(f"Open {VAULT.resolve()} as a vault in Obsidian.")


if __name__ == "__main__":
    main()