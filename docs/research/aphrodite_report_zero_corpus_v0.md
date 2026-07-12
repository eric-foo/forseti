# Aphrodite Report Zero — Frozen Corpus Record v0

```yaml
retrieval_header_version: 1
artifact_role: Research record (frozen rehearsal corpus — canonical packet set + five-hash chain for the D-1 dress rehearsal extraction)
scope: >
  The frozen GentsScents corpus for Report Zero (the D-1 dress rehearsal):
  the canonical caption+watch packet per video (newest complete set, deduping
  the round-2 double-captures), the recipe-v1 five-hash chain per video, the
  corpus_input_hash, and the buyer-intake hash. Every corpus-level hash cited
  by aphrodite-rehearsal-extraction-v1 claims is re-derivable from this record
  plus the named lake packets.
use_when:
  - Hand-running or re-checking the Report Zero extraction (claims cite these hashes).
  - Auditing which lake packets are the canonical rehearsal substrate.
authority_boundary: retrieval_only
open_next:
  - docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md
  - docs/research/aphrodite_report_zero_buyer_intake_v0.yaml
stale_if:
  - A later capture cycle or corpus supersedes this freeze for rehearsal use.
  - The lake packets named here are pruned or restructured (re-pin by hash).
```

## Freeze identity

- Creator: GentsScents (`Gents Scents`, channel `UC9IImcLkUdmURWtQhxu8VwQ`;
  registry `acct_yt_fragrance_010` per the round-2 capture preflight — the
  linkage lives in the registry, not on the packets).
- Lake root: `F:\orca-data-lake` (marker-verified). Packet paths below are
  relative to `raw/`.
- Canonical rule: newest packet per (video_id, surface); completeness asserted
  (non-empty normalized cues; watch packet carries metadata + comments).
  12 of 15 videos were double-captured on 2026-07-04; the later capture is
  canonical. The 3 single-captured videos use their only packet.
- Recipe order (hash order): ascending canonical-caption `captured_at`.
- Normalization (mechanical, no model):
  - transcript: json3 events -> `{video_id, cues:[{s,d,t}]}`; cue text =
    joined segs; whitespace-only cues dropped; canonical JSON (sorted keys,
    compact separators, UTF-8) -> `transcript_hash`.
  - watch subset: `{video_id, title, publish_date, length_seconds,
    short_description, view_count, like_count, comment_sample_count,
    total_comment_count, comments_panel_count_text,
    paid_content_overlay:"not_captured"}` -> canonical JSON ->
    `watch_metadata_hash`.
  - comments: author + author_channel_id DROPPED at normalization
    (person-level boundary); positional refs `c01..c40` minted (packets carry
    no platform comment_id — named limitation); hash line =
    `ref:text:like_count_raw:reply_count_raw` (verbatim raw count strings),
    joined with `\n` -> `comments_hash`.
  - `video_input_hash = sha256(video_id:transcript_hash:watch_metadata_hash:comments_hash)`;
    `corpus_input_hash = sha256(join("\n", video_id:video_input_hash in recipe order))`.
- Freeze executed 2026-07-10 by the rehearsal lane (scratch script; mechanical
  bookkeeping only — no extraction, no model judgment, no lake mutation).

## Corpus hashes


- **corpus_input_hash:** `0362007ee16d7466ef0ca3ef9973d841727d24f0bb75ca5aa15843c219871ed5`
- **buyer_intake_sha256:** `3adf664bb9a478e1e739345c34430f59c7837f33ec0afb7bf1ff5b17ac3eb73b` (docs/research/aphrodite_report_zero_buyer_intake_v0.yaml)
- **Totals:** 15 videos - 8014 cues - 53749 transcript words - 600 sampled comments (40/video, pre-dedup; cross-checks the round-2 grade's 53,749 words exactly).

## Canonical packet table (recipe order)

| # | video_id | title | published | views | likes | words | caption packet (canonical) | watch packet (canonical) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `ctcEju1AvGw` | 21 Best BLUE Fragrances BRUTALLY RANKED From S Tier To Trash | 2026-07-02 | 64827 | 4651 | 4036 | `7ba/01KWPFWGPNRAF8BXQVGS9TA1Y8` @ 2026-07-04T11:58:08Z | `8f6/01KWPFX146F2G9NVP18NJRNXJ3` @ 2026-07-04T11:58:21Z |
| 2 | `m-cJ9GVzzbc` | NEW Rasasi Hawas Chrome - #1 Hawas Release Of 2026? | 2026-07-01 | 27206 | 1204 | 3344 | `691/01KWPG0D8P1VY7ZVJ5ASJ13MMB` @ 2026-07-04T12:00:15Z | `655/01KWPG0TG8P9J01299Y1S60NZT` @ 2026-07-04T12:00:27Z |
| 3 | `eH93HPAWucE` | 12 Fragrances SO GOOD I Wear Them Every Single Day ALL YEAR  | 2026-06-30 | 44605 | 1642 | 3247 | `85c/01KWPG1APGW58V05M404W3RMT6` @ 2026-07-04T12:00:46Z | `6d6/01KWPG1R779AV458XJQ2RD97DV` @ 2026-07-04T12:00:58Z |
| 4 | `8QpC36Q_eeM` | 20 PERFECT Fragrances I Will Recommend FOREVER | 2026-06-29 | 36569 | 1959 | 3825 | `f40/01KWPG3GED26F74NFX5F4PAVQH` @ 2026-07-04T12:01:57Z | `287/01KWPG3Y1STP6YDRNPYYK4Z2F9` @ 2026-07-04T12:02:09Z |
| 5 | `q0oiKqeghks` | 12 FRESH Cheap Clone Fragrances Perfect For Summer | 2026-06-28 | 33111 | 1470 | 3301 | `58d/01KWPG4DZFZAP7CPQ84ABFMG7R` @ 2026-07-04T12:02:27Z | `f9a/01KWPG4VZ1AWCYYV2JPB3C3S8J` @ 2026-07-04T12:02:40Z |
| 6 | `FBda5R_1GGg` | Fake Fragrances Are STILL Flooding The Market - Don’t Get Sc | 2026-06-27 | 20653 | 1229 | 4303 | `540/01KWPG5B07BJE0HR3DEC8AMZ0B` @ 2026-07-04T12:02:57Z | `47c/01KWPG5QV9S8REG3Z0NB2VT9YX` @ 2026-07-04T12:03:09Z |
| 7 | `4OdcF9S6hxU` | BRUTALLY Ranking The 25 MOST Popular Men&#39;s Fragrances On | 2026-06-26 | 51897 | 1928 | 5410 | `6f8/01KWPG67A6JS5FHBHEH06TA8F9` @ 2026-07-04T12:03:26Z | `ec6/01KWPG6MYPFBCJ0EEEGJMZNV93` @ 2026-07-04T12:03:38Z |
| 8 | `V7q8PrAebz8` | NEW Armaf Dunescape - The PERFECT Summertime Clone Fragrance | 2026-06-25 | 24868 | 1144 | 2791 | `914/01KWPG74KXB9FMCAKHP38GG7KT` @ 2026-07-04T12:03:56Z | `851/01KWPG7HGR1XMTNZ86VEZDR2GR` @ 2026-07-04T12:04:08Z |
| 9 | `_FUdh1ryqWI` | NEW Ahmed Al Maghribi Kaaf Noir - Best Clone Release Of The  | 2026-06-24 | 36307 | 1338 | 2829 | `b43/01KWPG81GDXHK2GAP9WJB7JY32` @ 2026-07-04T12:04:26Z | `b03/01KWPG8EBFV7ESR74ZJZGKD4ZT` @ 2026-07-04T12:04:37Z |
| 10 | `hzqxkp3OqQw` | Top 20 Most Popular ELIXIR Fragrances Ranked From S-Tier To  | 2026-06-24 | 25128 | 1242 | 3727 | `bfd/01KWPG94S4D75F7VF63H17A46E` @ 2026-07-04T12:05:02Z | `c3d/01KWPG9HXXRN7E4BXAGRR56G83` @ 2026-07-04T12:05:14Z |
| 11 | `sw34VzzWlvA` | 15 Cheap Fragrances That Are 10/10 In EVERY Situation | 2026-06-23 | 32524 | 1464 | 3468 | `cb0/01KWPGA1W9PN23F48ET9TTVCRG` @ 2026-07-04T12:05:32Z | `308/01KWPGAFJMJR3WHCQ10Q8KPSP4` @ 2026-07-04T12:05:44Z |
| 12 | `lecfbS6qOIw` | Ultimate Year-Round Fragrance Lineup - 4 Fragrances Per 4 Se | 2026-06-22 | 40390 | 1743 | 3393 | `270/01KWPGAZ19PKFRD084NKGFNCSE` @ 2026-07-04T12:06:02Z | `c11/01KWPGBC6PGKM2QRVF0HQEB0DG` @ 2026-07-04T12:06:13Z |
| 13 | `nySgot9sqMY` | NEW Rasasi Hawas Gold Digger / Hawas La Mer / Hawas Sapphire | 2026-06-21 | 53759 | 2064 | 3292 | `04b/01KWPGBVB6WCKEDFHMTTZY3PS3` @ 2026-07-04T12:06:31Z | `93e/01KWPGC8X6762MZME76W08PQMR` @ 2026-07-04T12:06:43Z |
| 14 | `tVUqAYGT3SE` | 10 BRAND NEW Must Know Cheap Clone Fragrances For Men | 2026-06-20 | 32530 | 1948 | 3656 | `7e5/01KWPGCRHT6RE61HW9SF3XXBH3` @ 2026-07-04T12:07:00Z | `1e0/01KWPGD615XK0QB56TF6TS9VHP` @ 2026-07-04T12:07:12Z |
| 15 | `1N44B-O7VzE` | 10 Underrated Designer Fragrances EVERY MAN SHOULD OWN | 2026-06-19 | 28485 | 1279 | 3127 | `c1f/01KWPGDNGVD1CQ742Y094JJSZQ` @ 2026-07-04T12:07:30Z | `791/01KWPGE2C90SBKRHYSJFMP7D4D` @ 2026-07-04T12:07:42Z |

## Per-video hash chain

| video_id | transcript_hash | watch_metadata_hash | comments_hash | video_input_hash |
| --- | --- | --- | --- | --- |
| `ctcEju1AvGw` | `3e744cca8dcd3d8472e418754e6a90ff2bd34001de39e463e19a68948c50122c` | `d3fa0417f598123b5970563d287877d664350779a4f047f7fcbd047d6921289e` | `90c21cf81b25e1004970432f685a0ebb91a81f186c5c328944566d15db4f38c9` | `7144065d3cbc337f1f09efdacae665f3f842278658130379d17e9672295871bb` |
| `m-cJ9GVzzbc` | `23376b61574d9e09c0f79dda4315db6a171408c6991beae5c1f4a54cf2c33755` | `eb82a675a3e58db02e56b8ffd2c173f5eafb3d683dbd3e4ce6f8ad97cd9f615c` | `56ba9c5815c5d6b04a6da7cc25eebf7ed869cfdea8cfdc7a8a0867a9f0f62b07` | `df4be91220897070d572128fb189b06e704e98ff1ecbc33149be68579f639866` |
| `eH93HPAWucE` | `3a66390c3e73769f6d6c4b82c14590225153539481a0218c37f4baec49b698ca` | `aaf9f72c4e659a827d28b519ab95e0c4ff29e17db3b98cf1dacfdcf695d9aa4f` | `de78fdc466579ba1e0319f517d2b0557099ddfb10fc6037672c7a01e782425cb` | `5fcea0bf11764aa4be98f638e41d4db00979fdfac7f6b1e3a9ee0ccb98846932` |
| `8QpC36Q_eeM` | `8bb6d8634efe88024ba8c63d2c1b02f7bf616c09fdd9867d3ffa1f9a649e3eef` | `a8db64f6ee70ba9872f3c99f4a4373b3da7dad6fc2e79c90489ec37ae0d5183f` | `d133d23ed23d59a240b9f252cb6d60f478a4d375e5b531860bdacd8ebb5ee27a` | `41d110f418936fe410d59ca5fc1b9987a8284d67463c94f250e0382e56c5aadc` |
| `q0oiKqeghks` | `c7c4a41295f7c2a3f3bf79f6a38237df94032226849fd51b811b3af92a61f9ce` | `6c78c43b18b012eadffd04dbc98a3759f7d1049521f4a2c88f6f1895064dd251` | `b8452f9b8888602df582d9c973f640e214de6cfe5f07405e4b5bcb282ae469a0` | `0362d378b95aeeebb196ee4b70edea797539c1522dd175be987b577f9f4656c5` |
| `FBda5R_1GGg` | `82ba8a9c3ae98b491c7fc998e244547089cd73b149952222069f0a6f4d6be040` | `e780f64527a2f998da3e879748a634fc071d63d6d8d38abc5f06e0bebb4e96b1` | `03ef69b20929222c5f8a20b73b227b738e070c3ec2833326da55adaa2b55cc1a` | `7a528f86513e12ef432af134ece38e3e2156d5667722efe7f77e7be0d1941ce8` |
| `4OdcF9S6hxU` | `52d80c6a56482f981e653f4c09215afc2e5ac575e678795fc3b6649584f12f0b` | `b3a61893aebe45f9bbdae58437412e49b903a0452c8f9488b67bd692c9fbf3e0` | `b203860ac4af4bc7c86942f1cb53892ac4faf80395aec264fb7746098a510d08` | `259cd0a21601572fb21e9cb15b9b22ae8adbf0b5672ed501530b1b568a24bd1d` |
| `V7q8PrAebz8` | `bd9a200145645b32a388cebdc120063bc8c132cd6026e947e72cb301e7d743ca` | `8a8f5e2346bdae3d49b2fccf2883d7e5c128995d4968542967004bf0649b9d38` | `672421e7a40c4873168c254a7ce9e20aaeb1fce780667078d2e11edad765386f` | `70eb1e306ca6cb00d688a7fb1ef7186944610a51c172f4bf34c3d02f6f89356e` |
| `_FUdh1ryqWI` | `2178e73387e9faf13072daa4c7743d620c81c15ee37a231a02c751e5761a03bd` | `3a9a60105f8c83d248a55d18464b45666cc03c02819f4e2ae494adc2682b5de5` | `b983c1c3d05a6c2901d8840620315d5f128985a6991f5ac85467f8060a5cff74` | `d241bfca0737bb5ddad0fb4979cb8dd0c16dc70ddc745f30f777d91aa7b5ff0a` |
| `hzqxkp3OqQw` | `53315accc45e41e6e71242047fa55582c348d0a9d9b106344bcf979489adfe50` | `724ce7083273decb82f65f55d11b5eb19150a7a4574e99192946292524fac5b5` | `c045b527cdaad47a5cd6e2674710189f928b02311140cd94f715183c766f986d` | `029ed1f71f6822ac8888c869c44136af05a47e99839bfae5ebef7835222ac9ca` |
| `sw34VzzWlvA` | `af1fe3f48df36d78ab008915e59163af9d5babf2082d19965d8366509458ded6` | `88a6c3c8a3d8dcfa705cce82462e611d53838ba8445acab5ee653ba800cf3505` | `705e2fcda16b5b75e6facf4ba01a14d4076520b3f0e46c14658967724ee62b44` | `d237b67dbc111dee1920b68f8e491bf079e76cad9634524dac7d6ee389efc180` |
| `lecfbS6qOIw` | `50831715be9629a3f83d882243ce69a2eb6d36f96cff97c39c09bdc5f7067873` | `4180c5b04c4cb836471e28004f046f4b80e2c802aa9e823b01bddb9b9c932a18` | `59cc2babf4e6c6aca27813348104ab4807629cb59284a19ac01b672089d28b29` | `bcb33f0b08750a4983c2ad9655858c43951fc61d8e90ae794a34112211f70858` |
| `nySgot9sqMY` | `6a540f3bb6d006fd4b1ab4aa62703fab6552b18280bbaae731c886ae3dd334f2` | `34b219725ec3bca763689143eae07908564129359da844d2933d821868a5886f` | `36d9077f148ce9596c0bc9da0f23bdd778ad294eb31d75da8d77a09555147a37` | `56fc576f31e5dc06e295280712b22682e818747e5d234c272cdd9e1670ac7e6b` |
| `tVUqAYGT3SE` | `da1573f6e9249b1eac213827aaf4f870b713ffea76a6223937ea9d41694081f0` | `36c6102574a3b292450f1ff3c80d5e58ca298ee477313bceddf827710451ee45` | `5d006c5314613766259f3a292d1967920637a9c6f62c1b95d60b614904c8ac06` | `4342e446b15fa3b546a6fbf53658af24270e940d626ddbb4af0b5ed58dd4d5a2` |
| `1N44B-O7VzE` | `c26c10a8fcd72929ad35c5751467784d9a841cba8e63d06874dd5c97c7fd401e` | `de42ed5130c3ba3c1ff4074b12b54c655f35c0118e923bb3c551cfb68b957910` | `bfa626c4492de7fae6776c21f5f716b12a7699c868fdb9ec00fe34df6edc812f` | `a9fe5fa123f2da6bf5340d3e451baa64ec644f66ad724dc1f2dfcf3b7cd4f190` |

## Named limitations

- Captured comments carry no platform comment_id; receipts use the positional
  ref (`video_id#cNN`) resolvable in the normalized comments record and,
  transitively, the canonical watch packet's parsed comment list (order
  preserved). Whitespace/unparseable count strings are preserved verbatim in
  `*_raw`; parsed ints are convenience fields (null when unparseable).
- `paidContentOverlay` is absent from these watch captures (recorded
  `not_captured`); absence is never treated as organic proof (recipe
  ad-detection rule).
- 40 top-sort comments per video is the page-1 sampling knob; the total
  available counts (e.g. panel text "3.1K") are recorded in the watch subset.
- Comment sample is per-video pre-dedup (600 total); cross-video duplicate
  text, if any, is an extraction-time concern, not a freeze concern.

## Non-claims

Mechanical freeze only: not extraction, not validation, not capture
authorization (packets were captured 2026-07-04 under the round-2
owner-authorized run), not a storage schema; `product_learning`-capped.
