# Review guide: seven 2017 message files brought up to the current rules

Prepared 2026-11-18 against commit 2122f78. This zip does not overlap the earlier one (`2026-11-18-dashes-and-2017-chains.zip`); commit both. All files are laid out like the repo and replace their originals.

Checked on a copy of the repo with both zips in place: `validate_messages.py` passes all 634 files, `validate_chains.py` passes, the vault build reports 0 quoted passages not located, and the 67 log quotes for these seven messages still match the text after the two body fixes.

## The seven message files

Every file: `gathering: ""`, the door ends with a full stop, the excerpt is the message's exact words, `related_messages` is subject-only and in date order, `last_edited: 2026-11-18`.

- `2017/05/2017-05-22-af-andrew.md`: notes cleared (they repeated the description and reported a text correction); links to 2016-03-26-af-andrew and 2016-08-16-af-james dropped as general.
- `2017/09/2017-09-12-af-augustine.md`: notes cleared (they guessed at the order of the evening); excerpt replaced so it is not the same line as the door; links to 2016-07-10-af-augustine and 2017-06-15-af-augustine dropped.
- `2017/09/2017-09-12-af-confucius.md`: notes cleared (the same guess); "Prophecy" removed from essential_teachings; secondary subject "Celestial Governance & Spiritual Law" replaced with "Divine Plan & Timing"; three general links dropped.
- `2017/09/2017-09-12-af-martin-luther.md`: notes cut to the context line (the order reference and the text correction removed); link to 2017-09-12-af-confucius (same evening only) and 2016-04-12-af-moses dropped; link to 2017-12-18-af-martin-luther added. Primary subject "Celestial Governance & Spiritual Law" changed to "Law of Love", since the message uses the Law of Divine Love as a working Law and a top-level category cannot be tagged with one of its own subjects. Body: "waiver" to "waver", and "within in the flow" to "within the flow", both approved.
- `2017/12/2017-12-12-af-seretta-kem.md`: notes cleared (text corrections only); secondary subject "Mediumship & Developing as an Instrument" replaced with "Teaching & Sharing the Message"; four links dropped (healing merkaba, the healing-energy and mediumship talks, 2017-09-12-af-martin-luther); link to 2023-02-10-af-augustine added.
- `2017/12/2017-12-14-af-jesus.md`: message_type stays Blessing; all three links dropped as general encouragement.
- `2017/12/2017-12-18-af-martin-luther.md`: message_type Teaching to Guidance; link to 2017-06-15-af-augustine dropped.

## `metadata/law-mentions-reviewed.yml`

2017-09-12-af-martin-luther removed from the "Law of Love" list, now that the message carries that subject. It stays under "Laws of Creation".

## Reciprocal related_messages (files in the zip, or paste these)

Each block replaces the whole `related_messages` field. Each of these files also needs `last_edited: 2026-11-18`, already set in the zipped copy.

### `content/messages/2016/04/2016-04-14-af-john-the-beloved.md`

Replace:
```yaml
related_messages:
  - 2016-03-18-af-john-the-beloved
  - 2015-10-19-af-john-the-beloved
```
With:
```yaml
related_messages:
  - 2015-10-19-af-john-the-beloved
  - 2016-03-18-af-john-the-beloved
  - 2017-05-22-af-andrew
```

### `content/messages/2017/01/2017-01-23-af-alec-gaunt.md`

Replace:
```yaml
related_messages:
  - 2016-06-13-af-james
  - 2016-07-10-af-augustine
  - 2018-07-14-af-seretta-kem
```
With:
```yaml
related_messages:
  - 2016-06-13-af-james
  - 2016-07-10-af-augustine
  - 2017-09-12-af-augustine
  - 2017-12-18-af-martin-luther
  - 2018-07-14-af-seretta-kem
```

### `content/messages/2016/08/2016-08-15-af-mary.md`

Replace:
```yaml
related_messages:
  - 2016-05-11-af-jesus
  - 2016-04-19-af-augustine
  - 2015-11-23-af-jesus
```
With:
```yaml
related_messages:
  - 2015-11-23-af-jesus
  - 2016-04-19-af-augustine
  - 2016-05-11-af-jesus
  - 2017-09-12-af-confucius
```

### `content/messages/2016/05/2016-05-02-af-andrew.md`

Replace:
```yaml
related_messages:
  - 2014-10-11-af-judas
  - 2015-06-08-af-joseph
  - 2016-02-15-af-augustine
  - 2016-04-12-af-moses
  - 2016-05-02-af-mary
  - 2019-01-21-af-augustine
```
With:
```yaml
related_messages:
  - 2014-10-11-af-judas
  - 2015-06-08-af-joseph
  - 2016-02-15-af-augustine
  - 2016-04-12-af-moses
  - 2016-05-02-af-mary
  - 2017-09-12-af-martin-luther
  - 2019-01-21-af-augustine
```

### `content/messages/2023/02/2023-02-10-af-augustine.md`

Replace:
```yaml
related_messages: []
```
With:
```yaml
related_messages:
  - 2017-12-12-af-seretta-kem
```

No dropped link needs removing at the other end: the dropped links were not reciprocated, apart from those kept.
