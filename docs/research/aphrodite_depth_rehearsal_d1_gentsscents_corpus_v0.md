# Aphrodite D-1 Depth Rehearsal - GentsScents Corpus v0

```yaml
retrieval_header_version: 1
artifact_role: Research record (D-1 rehearsal corpus freeze - one real captured creator)
scope: >
  Canonical newest-per-video packet selection for the Aphrodite D-1
  GentsScents dress rehearsal: 15 recent YouTube long-form videos, caption
  packets, watch/comment packets, per-video hashes, corpus hash, buyer profile,
  and read-boundary notes.
use_when:
  - Auditing the D-1 GentsScents claim record's `input_content_hash`.
  - Checking which raw lake packets the panel projection cites.
  - Re-running or adversarially reviewing the D-1 rehearsal without recapturing.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md
  - docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json
stale_if:
  - The GentsScents corpus is refreshed or recaptured for a later D-1 run.
  - The recipe hash rule changes.
```

## Status

`D1_CORPUS_FREEZE_V0` - one real captured creator, newest-per-video dedupe over
the existing 2026-07-04 GentsScents capture. No new capture was run in this
lane. The lake was read-only; no packet, registry, silver lane, or schema was
mutated. The raw lake root (`F:/orca-data-lake/raw`) remains an external local
source boundary, not a repo-relative `open_next` target.

## Creator And Buyer Inputs

- Creator: GentsScents / Gents Scents.
- Platform account id: `UC9IImcLkUdmURWtQhxu8VwQ`.
- Registry status from round-2 record: existing account
  `acct_yt_fragrance_010`, preflight `existing_match` / `allowed`.
- Buyer profile: `synthetic_skeptical_dupe_first_clone_house_v1`.
- Buyer segment: `dupe_first_clone_house`.
- Buyer target originals: `product:creed.aventus`,
  `product:dior.sauvage`.
- Proof posture: skeptical; weak rows must downgrade or withhold.

## Corpus Hash

- `corpus_input_hash`: `6fce3584d0bf057d306861c85ea90d0d02d13d0e0517c07d1937322871755f2f`
- Hash recipe: `aphrodite-rehearsal-extraction-v1`.
- Extraction timestamp for the D-1 claim projection:
  `2026-07-05T03:10:10.7702653+08:00`.

## Read Summary

| Measure | Current D-1 packet parse |
| --- | ---: |
| Videos selected | 15 |
| Total captured views | 552,859 |
| Total captured likes | 26,305 |
| Sampled visible comments parsed from newest packets | 600 |
| Caption words parsed from selected json3 packets | 55,572 |

The prior round-2 grade records 591 sampled comments and 53,749 transcript
words after its own dedupe/counting pass. This corpus record uses the newest
packet parse observed in this lane and keeps the discrepancy visible; it does
not silently normalize the two counting methods.

## Selected Video Packets

| # | Video | Published | Views | Comments | Watch packet | Caption packet | Video input hash |
| ---: | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | `ctcEju1AvGw` - 21 Best BLUE Fragrances BRUTALLY RANKED From S Tier To Trash | 2026-07-02 | 64,827 | 40 | `01KWPFX146F2G9NVP18NJRNXJ3` | `01KWPFWGPNRAF8BXQVGS9TA1Y8` | `6fbf29e9e15c5b33b6fed50d8ee3cf1bc3e9c05f7f0931095a4aeea97f371fd4` |
| 2 | `m-cJ9GVzzbc` - NEW Rasasi Hawas Chrome - #1 Hawas Release Of 2026? | 2026-07-01 | 27,206 | 40 | `01KWPG0TG8P9J01299Y1S60NZT` | `01KWPG0D8P1VY7ZVJ5ASJ13MMB` | `72d85413213a08e878f2bc8eea96be7a9196f89488a3539b55ca18bb56727f73` |
| 3 | `eH93HPAWucE` - 12 Fragrances SO GOOD I Wear Them Every Single Day ALL YEAR ROUND | 2026-06-30 | 44,605 | 40 | `01KWPG1R779AV458XJQ2RD97DV` | `01KWPG1APGW58V05M404W3RMT6` | `56f17770e63424c987b8ea0337d6accaefef439eefaad047cde6a4bab474c76c` |
| 4 | `8QpC36Q_eeM` - 20 PERFECT Fragrances I Will Recommend FOREVER | 2026-06-29 | 36,569 | 40 | `01KWPG3Y1STP6YDRNPYYK4Z2F9` | `01KWPG3GED26F74NFX5F4PAVQH` | `5fe536d2d021c62658a5b2a9b1f1cc3b2cd0cc8b36710f4ba1278e7f3c3eec24` |
| 5 | `q0oiKqeghks` - 12 FRESH Cheap Clone Fragrances Perfect For Summer | 2026-06-28 | 33,111 | 40 | `01KWPG4VZ1AWCYYV2JPB3C3S8J` | `01KWPG4DZFZAP7CPQ84ABFMG7R` | `721abe29c5370ed75b19c279d2d9df17232180037a3e16e29fe9dc327b62fdbd` |
| 6 | `FBda5R_1GGg` - Fake Fragrances Are STILL Flooding The Market - Don't Get Scammed! | 2026-06-27 | 20,653 | 40 | `01KWPG5QV9S8REG3Z0NB2VT9YX` | `01KWPG5B07BJE0HR3DEC8AMZ0B` | `8804cdcc12e3d8c1df25bbfb77e3f5460ede53aecbfc50e8e844c41ba5d8eb9d` |
| 7 | `4OdcF9S6hxU` - BRUTALLY Ranking The 25 MOST Popular Men's Fragrances On A Tier List | 2026-06-26 | 51,897 | 40 | `01KWPG6MYPFBCJ0EEEGJMZNV93` | `01KWPG67A6JS5FHBHEH06TA8F9` | `1d96635bd33a0af80ff8a98fa9462bbe80b1777e4e0b14f3fa4fe34e97f32ef4` |
| 8 | `V7q8PrAebz8` - NEW Armaf Dunescape - The PERFECT Summertime Clone Fragrance | 2026-06-25 | 24,868 | 40 | `01KWPG7HGR1XMTNZ86VEZDR2GR` | `01KWPG74KXB9FMCAKHP38GG7KT` | `1e99e29ce0df379853846e58cf097e0a63f437b277a25779086655694fb2384e` |
| 9 | `_FUdh1ryqWI` - NEW Ahmed Al Maghribi Kaaf Noir - Best Clone Release Of The Year?! | 2026-06-24 | 36,307 | 40 | `01KWPG8EBFV7ESR74ZJZGKD4ZT` | `01KWPG81GDXHK2GAP9WJB7JY32` | `9b790dd71dff5491fb614aea0bd193be46131ea7af6bf13839903a562218a3b1` |
| 10 | `hzqxkp3OqQw` - Top 20 Most Popular ELIXIR Fragrances Ranked From S-Tier To TRASH | 2026-06-24 | 25,128 | 40 | `01KWPG9HXXRN7E4BXAGRR56G83` | `01KWPG94S4D75F7VF63H17A46E` | `6826f29624a1bafc47db145b4ba00f9e568d0acc9297aeaef5279ac8a37bd127` |
| 11 | `sw34VzzWlvA` - 15 Cheap Fragrances That Are 10/10 In EVERY Situation | 2026-06-23 | 32,524 | 40 | `01KWPGAFJMJR3WHCQ10Q8KPSP4` | `01KWPGA1W9PN23F48ET9TTVCRG` | `6e73806c6b4c3957aab81ed7f8916c5c7b6e6c85fe18f66af68ae569bd52357d` |
| 12 | `lecfbS6qOIw` - Ultimate Year-Round Fragrance Lineup - 4 Fragrances Per 4 Seasons | 2026-06-22 | 40,390 | 40 | `01KWPGBC6PGKM2QRVF0HQEB0DG` | `01KWPGAZ19PKFRD084NKGFNCSE` | `ba76d324c7e3e9e78e3ee48e69dcb483ccadf451c501cd16ef99dedc0da08621` |
| 13 | `nySgot9sqMY` - NEW Rasasi Hawas Gold Digger | Hawas La Mer | Hawas Sapphire | CDNIM Absolu + MORE | 2026-06-21 | 53,759 | 40 | `01KWPGC8X6762MZME76W08PQMR` | `01KWPGBVB6WCKEDFHMTTZY3PS3` | `4c3fcf7fcd51a7fe8120276ff03f960044cab50982153691d7c92ffa55dd0ee0` |
| 14 | `tVUqAYGT3SE` - 10 BRAND NEW Must Know Cheap Clone Fragrances For Men | 2026-06-20 | 32,530 | 40 | `01KWPGD615XK0QB56TF6TS9VHP` | `01KWPGCRHT6RE61HW9SF3XXBH3` | `37ab0d92a1f2955337612948ef6bedeebf394e00cd68367333d20bcf74a5c72a` |
| 15 | `1N44B-O7VzE` - 10 Underrated Designer Fragrances EVERY MAN SHOULD OWN | 2026-06-19 | 28,485 | 40 | `01KWPGE2C90SBKRHYSJFMP7D4D` | `01KWPGDNGVD1CQ742Y094JJSZQ` | `69cfcb1da66cba660c9939d990aae910ceb2e22b41b5ddb6e04ad59a75e9ab56` |

## Corpus Limitations

- Caption packets are public YouTube caption json3, not media preservation.
- Comments are top-sort/page-1 visible samples, not the full comment graph.
- The newest-packet parse in this lane counts 600 sampled comment objects; the
  earlier round-2 grade counts 591 after its own dedupe. Both are evidence
  records; the limitation travels with the panels.
- Product mention totals reuse the prior round-2 share-of-voice rehearsal as a
  product-learning extraction substrate and are cross-checked with targeted
  caption receipts in the D-1 claim record. They are not silver-lane records.

## Non-Claims

This corpus freeze is not validation, readiness, buyer proof, a registry
current-view update, a silver-lane write, or durable storage architecture.
