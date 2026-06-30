import os, re, json
from collections import Counter

VALID = {
    # main categories
    'Divine Love & Relationship with God', 'Soul Transformation & Development',
    'Spiritual Discipline & Daily Living', 'Earthly Challenges & Human Condition',
    'Spiritual Community & Fellowship', 'Divine Will, Guidance & Orchestration',
    'Preparation for Earth Mission', 'Service, Ministry & Being a Channel of Love',
    'Soul Healing & Emotional Restoration', 'Earth Changes & Prophecy',
    "Nature, Environment & God's Creation", 'Spiritual Warfare & Opposition',
    'Spiritual Identity & Destiny', 'Collective Awakening & Redemption',
    'Interdimensional & Spirit Communication', 'Teaching, Testimony & Instruction',
    'Celestial Governance & Spiritual Law', 'Historical Context & Spiritual Legacy',
    'Spiritual Empowerment & Encouragement', 'Creation and Incarnation',
    'Manifestations & Direct Voice',
    # subcategories
    'Receiving the Divine Love through Prayer', 'Rebirth of the Soul (New Birth)',
    'At-onement', 'Knowing God', "God's Nature & Essence", "God's Mercy & Unconditional Love",
    'Soul Awakening', 'Personal Transformation Journey', 'Cleansing & Expiation',
    'Soul Growth through Challenges', 'Self-Love & Acceptance', 'Guilt & Regret',
    'Prayer & Devotion', 'Surrender & Trust in God', 'Joyful Living',
    'Walking the Divine Path', 'Humility', 'Compassion & Empathy', 'Releasing Judgment',
    'Faith & Trust', 'Emotional Struggles', 'Mind vs Soul Conflict',
    'Temptations & Attachments', 'Free Will & Human Error', 'Grief & Loss',
    'Circle of Light & Prayer Circles', 'Lattice of Light & Global Prayer Network',
    'Unity in Diversity', 'Supporting One Another', 'Sanctuary & Sacred Space',
    "Surrender to God's Will", 'Divine Plan & Timing', "God's Guidance",
    'Alignment with Divine Flow', 'Readiness & Spiritual Maturity', 'Unique Soul Gifts',
    'Mediumship & Developing as an Instrument', 'Overcoming Fear & Doubt',
    'Discipleship', 'Teaching & Sharing the Message', "Testimony of God's Love",
    'Interfaith & Universal Truth', 'Divine Love Healing', 'Letting Go of Wounds',
    'Healing Through Prayer', 'Future World Events', 'Acceleration of Change',
    'Cleansing of the Earth', 'Two Choices for Humanity', 'Beauty & Spiritual Joy',
    'Reverence for the Earth', 'Harmony with Nature', 'Earthbound Spirits & Dark Influences',
    'Darkness vs Light', 'Protection from Negative Influences', 'Divine Purpose',
    "Soul's True Nature", 'Celestial Destiny', 'Redemption of Humanity',
    'Awakening Mass Consciousness', 'Global Spiritual Work', 'Soul Spheres & Progression',
    'Celestial Heavens & At-onement', 'The Hells & Dark Spheres', 'Spirit Guides & Angels',
    'Spirit Testimony & Personal Story', 'Teaching the Prayer Practice',
    'Discernment & Truth-Seeking', 'Religious Error & Reformation', 'Law of Attraction',
    'Law of Compensation', 'Law of Free Will', 'Law of Activation', 'Law of Love',
    'Law of Communication & Rapport', 'Life of Jesus', 'Padgett Messages & Legacy',
    'Confidence in the Path', 'Reassurance & Strength', 'Overcoming Inadequacy & Doubt',
    'Nature of the Soul', 'Purpose of Physical Life', 'Natural Love & Human Development',
    'Soul Mates & Sacred Union', 'Direct Voice Communication', 'Physical Manifestations',
    'Signs & Wonders',
    # 3 new subjects
    'Perseverance & Steadfastness', "God's Protection & Care",
    'Natural Love Path vs Divine Love Path',
}


def extract_subjects(content):
    """Return list of (field, value) from primary_subjects and secondary_subjects."""
    if not content.startswith('---'):
        return []
    end = content.find('\n---', 3)
    if end == -1:
        return []
    fm_text = content[3:end]
    fm_lines = fm_text.split('\n')

    results = []
    in_subject = False
    current_field = None

    for line in fm_lines:
        m_key = re.match(r'^(primary_subjects|secondary_subjects)\s*:\s*(.*)', line)
        if m_key:
            current_field = m_key.group(1)
            inline_val = m_key.group(2).strip()
            if inline_val:
                if inline_val.startswith('['):
                    # Inline array: parse each element
                    try:
                        items = json.loads(inline_val)
                        for item in items:
                            results.append((current_field, item.strip()))
                    except Exception:
                        results.append((current_field, inline_val))  # unparseable
                else:
                    # Scalar (possibly quoted)
                    v = inline_val.strip('"\'')
                    results.append((current_field, v))
                in_subject = False
            else:
                in_subject = True
            continue

        if in_subject:
            if line == '' or (line and not line[0].isspace()):
                in_subject = False
                current_field = None
            elif re.match(r'^\s*-\s+', line):
                m = re.match(r'^\s*-\s+(.+)$', line)
                if m:
                    raw = m.group(1).rstrip().strip('"\'')
                    results.append((current_field, raw))

    return results


per_file = {}
counter = Counter()
root = 'content/messages'

for dirpath, dirs, files in os.walk(root):
    dirs.sort()
    for fname in sorted(files):
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, encoding='utf-8') as f:
            content = f.read()
        invalids = [(field, val) for field, val in extract_subjects(content) if val not in VALID]
        if invalids:
            relpath = os.path.relpath(fpath, '.').replace(os.sep, '/')
            per_file[relpath] = invalids
            for _, val in invalids:
                counter[val] += 1

if not per_file:
    print('CLEAN: no invalid subject strings found.')
else:
    print(f'FILES WITH INVALID SUBJECTS: {len(per_file)}')
    print()
    for fp, issues in sorted(per_file.items()):
        print(fp)
        for field, val in issues:
            print(f'  [{field}] {val}')
    print()
    print(f'DISTINCT INVALID VALUES ({len(counter)}):')
    for val, cnt in counter.most_common():
        print(f'  {cnt:3d}  {val}')
