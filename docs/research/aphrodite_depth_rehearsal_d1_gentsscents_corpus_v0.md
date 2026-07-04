# Aphrodite Depth Rehearsal - D-1 GentsScents Corpus v0

```yaml
retrieval_header_version: 1
artifact_role: Research record (frozen D-1 GentsScents rehearsal corpus; evidence lane only)
scope: >
  Freezes the bounded input corpus for the GentsScents Aphrodite D-1 dress
  rehearsal: 15 existing YouTube video packet pairs, packet IDs, read counts,
  corpus hash, and named limitations. No new capture or lake mutation occurred.
use_when:
  - Resolving source_refs in the GentsScents D-1 claim record.
  - Checking whether the D-1 rehearsal stayed inside the authorized bounded slice.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md
  - docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json
  - docs/research/aphrodite_depth_rehearsal_round2_gentsscents_grade_v0.md
stale_if:
  - The selected raw packet IDs are superseded or restamped.
  - A later GentsScents corpus freeze replaces this bounded corpus.
```

## Status

`FROZEN_D1_REHEARSAL_CORPUS` - assembled for the fused D-1 dress rehearsal from existing data-lake packets only. This is evidence-lane documentation, not validation, readiness, capture authorization, or a durable lake lane.

## Creator and Buyer Inputs

- Creator: GentsScents (`UC9IImcLkUdmURWtQhxu8VwQ`), existing registry match `acct_yt_fragrance_010`, round-2 status `allowed`; creator choice owner-locked during fused preflight.
- Buyer profile: synthetic skeptical dupe-first or clone-house buyer, focused on whether GentsScents can reveal demand around Dior Sauvage, Creed Aventus, and adjacent clone/original shopping behavior.
- Structured intake state: `buyer_segment`, `buyer_house_tier`, `dupe_target_originals`, `note_family_targets`, `occasion_targets`, and `target_tier_position` are encoded in `docs/research/aphrodite_depth_rehearsal_d1_gentsscents_claims_v0.json`; each coordinate carries `intake_source_state` or an explicit withheld state.
- Source branch: `claude/recipe-v1-second-opinion-adjudication`; rehearsal branch: `codex/aphrodite-d1-depth-rehearsal`.

## Corpus Hash and Read Summary

- Selection rule: newest available watch packet plus newest available caption packet for each of the 15 videos named below.
- `corpus_input_hash`: `6fce3584d0bf057d306861c85ea90d0d02d13d0e0517c07d1937322871755f2f`
- Extraction timestamp: `2026-07-05T03:10:10.7702653+08:00`
- Parsed current pass totals: 15 videos, 552,859 total views, 26,305 total likes, 600 visible comments parsed, 55,572 caption/transcript words parsed.
- Prior round-2 record totals: 15 videos, 552,859 total views, 591 comments, 53,749 transcript words, 85 affiliate links.

The count mismatch is carried forward as a limitation instead of being normalized away. The current pass used a broader visible comment/text parse; the round-2 record used its own counting method. Aggregates that depend on comment-text texture cite the current parse. Link inventory cites the round-2 exact count because the current crude URL regex over-counted malformed snippets.

## Selected Corpus

| # | Video ID | Published title (short) | Views | Watch packet | Caption packet | Input hash |
|---|---|---|---:|---|---|---|
| 1 | `ctcEju1AvGw` | 21 Best BLUE... | 64,827 | `01KWPFX146F2G9NVP18NJRNXJ3` | `01KWPFWGPNRAF8BXQVGS9TA1Y8` | `6fbf29e9e15c5b33b6fed50d8ee3cf1bc3e9c05f7f0931095a4aeea97f371fd4` |
| 2 | `m-cJ9GVzzbc` | Recent fragrance video | 27,206 | `01KWPG0TG8P9J01299Y1S60NZT` | `01KWPG0D8P1VY7ZVJ5ASJ13MMB` | `72d85413213a08e878f2bc8eea96be7a9196f89488a3539b55ca18bb56727f73` |
| 3 | `eH93HPAWucE` | Recent fragrance video | 44,605 | `01KWPG1R779AV458XJQ2RD97DV` | `01KWPG1APGW58V05M404W3RMT6` | `56f17770e63424c987b8ea0337d6accaefef439eefaad047cde6a4bab474c76c` |
| 4 | `8QpC36Q_eeM` | Recent fragrance video | 36,569 | `01KWPG3Y1STP6YDRNPYYK4Z2F9` | `01KWPG3GED26F74NFX5F4PAVQH` | `5fe536d2d021c62658a5b2a9b1f1cc3b2cd0cc8b36710f4ba1278e7f3c3eec24` |
| 5 | `q0oiKqeghks` | Recent fragrance video | 33,111 | `01KWPG4VZ1AWCYYV2JPB3C3S8J` | `01KWPG4DZFZAP7CPQ84ABFMG7R` | `721abe29c5370ed75b19c279d2d9df17232180037a3e16e29fe9dc327b62fdbd` |
| 6 | `FBda5R_1GGg` | Recent fragrance video | 20,653 | `01KWPG5QV9S8REG3Z0NB2VT9YX` | `01KWPG5B07BJE0HR3DEC8AMZ0B` | `8804cdcc12e3d8c1df25bbfb77e3f5460ede53aecbfc50e8e844c41ba5d8eb9d` |
| 7 | `4OdcF9S6hxU` | Recent fragrance video | 51,897 | `01KWPG6MYPFBCJ0EEEGJMZNV93` | `01KWPG67A6JS5FHBHEH06TA8F9` | `1d96635bd33a0af80ff8a98fa9462bbe80b1777e4e0b14f3fa4fe34e97f32ef4` |
| 8 | `V7q8PrAebz8` | Recent fragrance video | 24,868 | `01KWPG7HGR1XMTNZ86VEZDR2GR` | `01KWPG74KXB9FMCAKHP38GG7KT` | `1e99e29ce0df379853846e58cf097e0a63f437b277a25779086655694fb2384e` |
| 9 | `_FUdh1ryqWI` | Recent fragrance video | 36,307 | `01KWPG8EBFV7ESR74ZJZGKD4ZT` | `01KWPG81GDXHK2GAP9WJB7JY32` | `9b790dd71dff5491fb614aea0bd193be46131ea7af6bf13839903a562218a3b1` |
| 10 | `hzqxkp3OqQw` | Recent fragrance video | 25,128 | `01KWPG9HXXRN7E4BXAGRR56G83` | `01KWPG94S4D75F7VF63H17A46E` | `6826f29624a1bafc47db145b4ba00f9e568d0acc9297aeaef5279ac8a37bd127` |
| 11 | `sw34VzzWlvA` | Recent fragrance video | 32,524 | `01KWPGAFJMJR3WHCQ10Q8KPSP4` | `01KWPGA1W9PN23F48ET9TTVCRG` | `6e73806c6b4c3957aab81ed7f8916c5c7b6e6c85fe18f66af68ae569bd52357d` |
| 12 | `lecfbS6qOIw` | Recent fragrance video | 40,390 | `01KWPGBC6PGKM2QRVF0HQEB0DG` | `01KWPGAZ19PKFRD084NKGFNCSE` | `ba76d324c7e3e9e78e3ee48e69dcb483ccadf451c501cd16ef99dedc0da08621` |
| 13 | `nySgot9sqMY` | NEW Rasasi Hawas Gold Digger / Hawas La Mer / Hawas Fire | 53,759 | `01KWPGC8X6762MZME76W08PQMR` | `01KWPGBVB6WCKEDFHMTTZY3PS3` | `4c3fcf7fcd51a7fe8120276ff03f960044cab50982153691d7c92ffa55dd0ee0` |
| 14 | `tVUqAYGT3SE` | Recent fragrance video | 32,530 | `01KWPGD615XK0QB56TF6TS9VHP` | `01KWPGCRHT6RE61HW9SF3XXBH3` | `37ab0d92a1f2955337612948ef6bedeebf394e00cd68367333d20bcf74a5c72a` |
| 15 | `1N44B-O7VzE` | Recent fragrance video | 28,485 | `01KWPGE2C90SBKRHYSJFMP7D4D` | `01KWPGDNGVD1CQ742Y094JJSZQ` | `69cfcb1da66cba660c9939d990aae910ceb2e22b41b5ddb6e04ad59a75e9ab56` |

## Supporting Reads

Round-2 share-of-voice record:

- 417 raw product mentions, 415 after intra-video dedupe, 340 distinct products.
- Top attention products include YSL Y EDP (5 videos, 199,244 views, 1.3%), Creed Aventus (5 videos, 183,116 views, 1.2%), Chanel Bleu de Chanel (5 videos, 167,049 views, 1.1%), Dior Sauvage (5 videos, 167,049 views, 1.1%), Coach for Men (3 videos, 149,248 views, 0.9%), JPG Ultra Male (4 videos, 141,980 views, 0.9%), Paco Rabanne Invictus Parfum (3 videos, 141,852 views, 0.9%), and Versace Pour Homme (3 videos, 130,085 views, 0.8%).
- Long tail: 340 distinct products; 85% appear in only one video; stance mix 211 positive, 138 neutral, 20 negative, 48 unclear; 55/417 low-confidence mentions, mostly clone/niche tail.

Current targeted raw keyword cross-check:

- `Aventus`: found in six caption/watch texts; official SoV aggregate remains 5 videos / 183,116 attention views after extraction rules.
- `Sauvage` or ASR `Savage`: found in eight caption/watch texts; official SoV aggregate remains 5 videos / 167,049 attention views after extraction rules.
- Other buyer-adjacent products observed in raw keyword pass include Bleu de Chanel, YSL Y EDP, Coach for Men, Invictus/Invictus Parfum, Versace Pour Homme, and JPG Ultra Male.

Comment keyword pass:

| Texture bucket | Raw comments | Sum like_count | Example receipt |
|---|---:|---:|---|
| Future-buy watchlist | 23 | 130 | `eH93HPAWucE` comment 9: "Reflection man is on my list to eventually get. One day!" |
| Bought or bought-because | 36 | 264 | `q0oiKqeghks` comment 4: "I purchased Raees Luxury edition the day I saw this video and it was in stock and shipped already." |
| Dupe request or clone | 42 | 211 | `m-cJ9GVzzbc` comment 4: "Rasasi should make a solid Acqua Di Gio Profondo EDP clone Hawas version" |
| Comparison shopping | 15 | 104 | Comments comparing named alternatives and flankers. |
| Price objection | 9 | 61 | Comments objecting to price or value. |
| Where-to-buy | 3 | 8 | Weak bucket; includes possible false positives from stock/shopping wording. |

Per M2, these counts and `sum(like_count)` values stay separate. No engagement-weighted scalar is emitted.

## Named Limitations

- Single capture cycle: no trend, follower delta, moving average, breakout frequency, or fit-relevant participation trend can be shown.
- Comment sample is visible/top-sort only. It supports texture, not prevalence.
- Product resolution came from the prior SoV rehearsal and operator-side targeted checks, not a durable silver lane update.
- The official SoV table and raw keyword pass differ because keyword matching sees ASR variants and repeated raw mentions before extraction/dedupe rules.
- Link inventory uses the round-2 exact count of 85 affiliate links; the current URL regex was too crude for a binding link count.
- The ontology has no citable dupe relationships, so clone-tail roll-ups must withhold even when comments ask for dupes.

## Non-Claims

- Not validation, readiness, D-1 passage, buyer proof, commercial-use clearance, or FLAG-1 resolution.
- Not a new capture, crawler, data-lake schema, or silver-lane mutation.
- Not evidence-grade for a sold report.
