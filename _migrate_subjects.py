import os, re

TODAY = '2026-06-26'

MAPPINGS = {
    "Soul Awakening & Spiritual Growth": "Soul Awakening",
    "World Service & God's Plan": "Divine Plan & Timing",
    "God's Will & Surrender": "Surrender to God's Will",
    "At-onement with God": "At-onement",
    "Soul Gifts & Purpose": "Unique Soul Gifts",
    "Spiritual Friendship & Fellowship": "Spiritual Community & Fellowship",
    "God's Love, Care & Provision": "God's Mercy & Unconditional Love",
    "Spiritual Comfort & Encouragement": "Reassurance & Strength",
    "Free Will & Choice": "Law of Free Will",
    "Spiritual Gifts & Mediumship": "Mediumship & Developing as an Instrument",
    "Mediumship & Spirit Communication": "Mediumship & Developing as an Instrument",
    "Soul Mind versus Material Mind": "Mind vs Soul Conflict",
    "Faith, Trust & Surrender": "Faith & Trust",
    "Angels, Spirit Guides & Celestial Helpers": "Spirit Guides & Angels",
    "Truth & Spiritual Knowledge": "Discernment & Truth-Seeking",
    "Joy & Spiritual Happiness": "Beauty & Spiritual Joy",
    "Soul Faculties, Perception & Knowing": "Nature of the Soul",
    "Errors in Religion & Theology": "Religious Error & Reformation",
    "Mind, Soul & Their Relationship": "Mind vs Soul Conflict",
    "Soul Transformation": "Soul Transformation & Development",
    "Judgment & Self-Judgment": "Releasing Judgment",
    "Lattice of Light, Chain of Light & Sphere of Light": "Lattice of Light & Global Prayer Network",
    "Non-Judgment & Acceptance": "Releasing Judgment",
    "Lattice of Light": "Lattice of Light & Global Prayer Network",
    "Discerning & Following God's Will": "Divine Will, Guidance & Orchestration",
    "Trust & Surrender to God": "Surrender & Trust in God",
    "Prophecy & Visions of the Future": "Earth Changes & Prophecy",
    "Outreach & Sharing the Truth": "Teaching & Sharing the Message",
    "Spiritual Warfare & Dark Forces": "Spiritual Warfare & Opposition",
    "Eternal Progression": "Soul Spheres & Progression",
    "Humility & Innocence": "Humility",
    "God's Healing Power": "Healing Through Prayer",
    "Divine Healing": "Divine Love Healing",
    "Spiritual Encouragement & Affirmation": "Reassurance & Strength",
    "Healing Path & Soul Expiation": "Cleansing & Expiation",
    "Prayer & Spiritual Practice": "Prayer & Devotion",
    "Judgment, Acceptance & Unconditional Love": "Releasing Judgment",
    "Soul Spheres & Natural Love Progression": "Soul Spheres & Progression",
    "Praying for Children & Loved Ones": "Prayer & Devotion",
    "Humility & Selfless Service": "Humility",
    "Nature & God's Creation": "Nature, Environment & God's Creation",
    "Discipleship & Following the Divine Love Path": "Discipleship",
    "Diversity & Inclusion": "Unity in Diversity",
    "Love for Difficult People": "Compassion & Empathy",
    "Spiritual Growth & Progression": "Soul Transformation & Development",
    "Universal Love & Brotherhood": "Unity in Diversity",
    "Prayer & Communion with God": "Prayer & Devotion",
    "Channels & Instruments of God": "Service, Ministry & Being a Channel of Love",
    "God's Plan & Divine Timing": "Divine Plan & Timing",
    "Spiritual Growth & Soul Development": "Soul Transformation & Development",
    "Mind vs Soul": "Mind vs Soul Conflict",
    "Celestial Heavens & Spirit Spheres": "Celestial Heavens & At-onement",
    "Surrender & Detachment": "Surrender & Trust in God",
    "Inner Peace & Stillness": "Reassurance & Strength",
    "Purpose & Meaning of Life": "Purpose of Physical Life",
    "Individual Soul Calling": "Divine Purpose",
    "Law of Attraction & Spiritual Laws": "Law of Attraction",
    "Soul Purpose & Pre-Birth Commitment": "Divine Purpose",
    "Soul Progression through the Spirit Spheres": "Soul Spheres & Progression",
    "Soul Growth & Transformation through Divine Love": "Soul Transformation & Development",
    "Fear & Anxiety": "Overcoming Fear & Doubt",
    "Celestial Heavens": "Celestial Heavens & At-onement",
    "Prayer for the Departed": "Prayer & Devotion",
    "Spirit World & Afterlife": "Soul Spheres & Progression",
    "Reformation of Religious Doctrine": "Religious Error & Reformation",
    "Emotional Healing & Inner Peace": "Soul Healing & Emotional Restoration",
    "Hope & Spiritual Encouragement": "Reassurance & Strength",
    "Celestial Heavens & Progression": "Celestial Heavens & At-onement",
    "Core Teachings & Doctrine": "Teaching, Testimony & Instruction",
    "Environmental Stewardship": "Reverence for the Earth",
    "Historical Figures & Letters from History": "Historical Context & Spiritual Legacy",
    "Spiritual Courage & Perseverance": "Perseverance & Steadfastness",
    "Shared Purpose": "Supporting One Another",
    "Future of Humanity": "Redemption of Humanity",
    "Sharing the Truth of Divine Love": "Teaching & Sharing the Message",
    "Natural Love Path vs. Divine Love Path": "Natural Love Path vs Divine Love Path",
}

SECTION_C = {"Awakening Humanity", "Service & Mission", "Two Paths"}


def unquote(s):
    s = s.strip()
    if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
        return s[1:-1], s[0]
    return s, None


def try_replace_value(raw_val):
    """Return (new_raw_val, changed, section_c_hit) for a raw YAML scalar value."""
    value, quote_char = unquote(raw_val)
    sc_hit = value if value in SECTION_C else None
    if value in MAPPINGS and MAPPINGS[value] != value:
        new_val = MAPPINGS[value]
        new_raw = (quote_char + new_val + quote_char) if quote_char else new_val
        return new_raw, True, sc_hit
    return raw_val, False, sc_hit


def process_file(fpath):
    with open(fpath, encoding='utf-8') as f:
        original = f.read()

    if not original.startswith('---'):
        return False, []

    end_idx = original.find('\n---', 3)
    if end_idx == -1:
        return False, []

    fm_text = original[3:end_idx]
    body = original[end_idx:]

    fm_lines = fm_text.split('\n')
    in_subject = False
    changed = False
    section_c_hits = []
    new_lines = []

    for line in fm_lines:
        # Detect subject keys — handle both scalar and list forms
        m_key = re.match(r'^(primary_subjects|secondary_subjects)\s*:\s*(.*)', line)
        if m_key:
            inline_val = m_key.group(2).strip()
            if inline_val:
                # Scalar form: primary_subjects: "Value"
                new_raw, did_change, sc_hit = try_replace_value(inline_val)
                if sc_hit:
                    section_c_hits.append(sc_hit)
                if did_change:
                    changed = True
                    key_part = line[:line.index(':') + 1]
                    line = key_part + ' ' + new_raw
                in_subject = False  # no list follows
            else:
                # List form: primary_subjects:\n  - ...
                in_subject = True
            new_lines.append(line)
            continue

        if in_subject:
            if line == '' or (line and not line[0].isspace()):
                in_subject = False
            elif re.match(r'^\s*-\s+', line):
                m = re.match(r'^(\s*-\s+)(.+)$', line)
                if m:
                    prefix = m.group(1)
                    raw_val = m.group(2).rstrip()
                    new_raw, did_change, sc_hit = try_replace_value(raw_val)
                    if sc_hit:
                        section_c_hits.append(sc_hit)
                    if did_change:
                        changed = True
                        line = prefix + new_raw

        new_lines.append(line)

    if changed:
        updated_lines = []
        for line in new_lines:
            if re.match(r'^last_edited\s*:', line):
                updated_lines.append('last_edited: ' + TODAY)
            else:
                updated_lines.append(line)
        new_fm = '\n'.join(updated_lines)
        new_content = '---' + new_fm + body
        with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)

    return changed, section_c_hits


section_c_files = {}
changed_count = 0
root = 'content/messages'

for dirpath, dirs, files in os.walk(root):
    dirs.sort()
    for fname in sorted(files):
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(dirpath, fname)
        changed, sc_hits = process_file(fpath)
        if changed:
            changed_count += 1
        if sc_hits:
            relpath = os.path.relpath(fpath, '.').replace(os.sep, '/')
            section_c_files[relpath] = sc_hits

print(f"Additional files modified: {changed_count}")
print(f"\nSection C files: {len(section_c_files)}")
for fp, hits in sorted(section_c_files.items()):
    print(f"  {fp}: {hits}")
