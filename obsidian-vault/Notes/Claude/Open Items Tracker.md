# Divine Love Messages Archive

# Compiled 2026-07-19. No em dashes; safe to commit or paste into any session.

## A. Land this week (mechanical, no judgment needed)

1. Confirm the migrated chains-log.md (68 comma headings to pipes) is committed.
2. Drop the updated generate_vault.py into .github/scripts/ and regenerate the vault. Expect the chain layer to roughly double: 68 of 127 log entries were previously invisible to the parser.
3. After regeneration, spot-check two or three chain hubs to confirm the recovered members appear, and glance at the graph.
4. Check the Notes/ folder for any pathed slug-style hub links (for example [[Subjects/receiving-the-divine-love-through-prayer]]). These dangle after the display-name rename and want updating. Bare message-id links are fine.
5. Front Matter Title plugin: confirmed working for message notes in the graph. Nothing further needed unless a regeneration resets .obsidian settings.

## B. Batch 1 review pass (Opus output, your review loop)

6. REVIEW.md flag 4: confirm the four message_type edge calls (Andrew Guidance, Confucius Guidance, Francis Guidance, Keea Teaching).
7. REVIEW.md flag 6: confirm collections. Keea Service & Mission versus empty; Goldie empty.
8. REVIEW.md flag 7: second look at two subjects. Goldie primary Harmony with Nature; Andrew secondary Soul's True Nature (drop if thin).
9. Paste the five reciprocal related_messages lines into the existing files, in chronological position, sorting any out-of-order list touched.
10. Check each of the five messages against the online archive; set canonical_url and remove the "Not publicly posted online." note where published.
11. Back-search check the five batch 1 ids against chains-log.md (the old kit did not instruct this): confirm or contradict any provisional roles now that full text is in hand.
12. Merge approved chains-proposed.md entries into chains-log.md (remove the [batch-proposed] tag, keep chronological placement) and update the chains-threads.md Holding Pen for approved sightings.
13. Apply approved spirit updates: francis-of-assisi notes addition (ready); keea-atta-kem "Keea" alias note (only if the file keeps alias forms); confucius Celestial Kingdom line (optional, Opus recommends leaving out).
14. Run validate_messages.py and commit the batch.

## C. Curation decisions waiting on you (bring to a project session)

15. MINTING DECISION, threshold met: the conduit candidate. Two members in hand, Keea 2016-04-12 (recorded messages carry ongoing angelic accompaniment to each reader) and Moses 2016-04-12 (Objection-removed: the words are not sacred, the rapport is; the message stays useful as conduit). Candidate slugs: conduit-not-scripture (closer to the argument) or message-as-living-channel. Note the same-evening, same-word (rapport) pairing, and Moses's compatible service to religious-error. Decide slug, confirm roles, walk the argument order.
16. divine-love-healing checkpoint ambiguity: the Holding Pen has been waiting on 2016-04-13 since June, but batch 1's 2016-04-13 (Confucius, Breath of God) has nothing healing-related. Check the Holding Pen entry in chains-threads.md to see which message it actually names. If it is a Seretta Kem message, it may be among the six inventory rows skipped as repo duplicates, meaning the witness check belongs to a curation session against the existing file, not to Cowork. Remaining checkpoints: 2017-12-12 and 2018-07-14 af-seretta-kem.
17. Three new holding-pen candidates proposed by batch 1, to add if approved: joy as soul-marker (Andrew 2016-04-12, one sighting); simplicity of the path (Francis 2016-04-17, statement plus Testimony, distinct from purpose-of-life); the Earth as healing ground (Goldie 2016-04-19, distinct from earth-changes and earth-conditions-and-prayer).
18. Excerpt-writing preference: the new vault layout makes the excerpt the threshold of every message page. Decide deliberately whether to prefer direct-quote excerpts over curator-written ones going forward, rather than drifting there.

## D. Kit and tooling refinements (small, decided or near-decided)

19. Kit slug-guard adjustment, awaiting your yes: change the final sentence of the chains bullet to "do not mint anything; never use an unregistered slug in an entry line, though you may suggest candidate slug names inside the curator-decision note." Batch 1 showed slug suggestions are useful; the danger was only unregistered slugs in member lines.
20. Kit preamble: the four task lines that preceded the kit title in your paste (Take DLSF Messages 2016 doc, etc.) were left out of the produced file. Say if they belong in as a preamble.
21. Next Cowork session: attach the UPDATED kit, batch 1's MANIFEST.md, and freshly exported reference files.
22. Possible retirement of the [medium: ...] heading tag class in the chain log: it duplicates the medium initials already in the message id. Future tidy, not urgent.
23. Chain display names in the vault are title-cased slugs. If one ever reads awkwardly, add a display-title column to chains-threads.md and teach generate_vault.py to read it.

## E. Standing deferred (carried from earlier sessions, unchanged)

24. Fold validate_subjects.py into the CI pipeline.
25. chains/ directory (full chain files with build-time ordering) waits until the archive is caught up through 2026. At build time: the who-jesus-was Foundation anchor is a three-way choice (1963-12-26-ds-mary, 2018-11-26-af-jesus, 2019-01-27-af-jesus).
26. Portal watch ongoing in the log (2016-03-25 through 2019-04-06 boundary).
27. Possible tenth collection for children and the young; watch the volume of the Children & Future Generations subject.
28. Usage census data to inform a possible merge of the two Surrender subjects.
29. audio_url to be populated as recordings are found.
30. Public website (Astro plus Pagefind on Cloudflare Pages or Netlify) as a considered future direction.
31. Series file architecture revisit flagged at an earlier milestone. This note predates the series-to-collections rename and the archive passing that count, so confirm whether it is overtaken before acting on it.