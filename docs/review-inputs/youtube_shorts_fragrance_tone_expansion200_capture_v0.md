# YouTube Shorts Fragrance Tone Expansion200 Capture v0

```yaml
retrieval_header_version: 1
artifact_role: Review input / expansion capture summary
scope: Expand the YouTube Shorts fragrance transcript-bearing pool to 200 total admitted Shorts; capture/admission only, no new tone labels.
use_when:
  - Inspecting the 200-row transcript-bearing Shorts pool.
  - Preparing cross-lane creator joins or the next tone-labeling pass.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.md
  - docs/review-inputs/youtube_shorts_fragrance_tone_expansion100_capture_v0.md
  - docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md
```

## Summary

- Generated at: `2026-06-26T18:52:15Z`
- Data root: `F:\orca-data-lake`
- Data root UUID: `01KW1E6N133JT0XCN2KCN0V5A4`
- Prior admitted total: 100
- New admitted rows: 100
- Cumulative admitted total: 200
- Attempts in this expansion: 152
- Minimum word count gate: 20
- New word-count range: 20 to 610
- Cumulative word-count range: 20 to 610

## Decision

Admit the captured rows as a 200-Short expansion pool, not a labeled benchmark. The new 100 rows are real public YouTube Shorts with caption packets in the data lake; no transcript bodies are committed to the repo.

## Admission Status Counts

| Status | Count |
| --- | ---: |
| `admitted` | 100 |
| `dropped_no_caption_asr_deferred` | 5 |
| `dropped_relevance_title_no_match` | 43 |
| `dropped_transcript_under_min_word_count` | 4 |

## New Admitted By Handle

| Handle | Count |
| --- | ---: |
| `BowTieFragranceGuy` | 2 |
| `ChaosFragrances` | 5 |
| `Cubaknow` | 3 |
| `CurlyFragrance` | 1 |
| `CurlyScents` | 4 |
| `DemiRawling` | 5 |
| `FragranceKnowledge` | 3 |
| `FragranceView` | 4 |
| `GentsScents` | 5 |
| `JeremyFragrance` | 3 |
| `JusDeRose` | 5 |
| `MilaLeBlanc` | 4 |
| `MonikaCioch` | 4 |
| `OliviaOlfactory` | 4 |
| `PostCologne` | 5 |
| `Redolessence` | 5 |
| `Scentbird` | 2 |
| `ScentedMoments` | 1 |
| `Scenteno` | 4 |
| `SchoolofScent` | 5 |
| `SimplyPutScents` | 5 |
| `SokiLondon` | 2 |
| `TheFragranceApprentice` | 1 |
| `ThePerfumeGuy` | 4 |
| `ThePerfumeNest` | 5 |
| `TheScented` | 2 |
| `TheScentinel` | 3 |
| `TiffBenson` | 3 |
| `funmimonet` | 1 |

## Cumulative By Handle

| Handle | Count |
| --- | ---: |
| `BowTieFragranceGuy` | 5 |
| `ChaosFragrances` | 9 |
| `Cubaknow` | 3 |
| `CurlyFragrance` | 1 |
| `CurlyScents` | 10 |
| `DemiRawling` | 6 |
| `FragranceKnowledge` | 7 |
| `FragranceView` | 4 |
| `GentsScents` | 12 |
| `JeremyFragrance` | 10 |
| `JusDeRose` | 7 |
| `MilaLeBlanc` | 8 |
| `MonikaCioch` | 5 |
| `OliviaOlfactory` | 5 |
| `PostCologne` | 5 |
| `ProfessorPerfume` | 1 |
| `Redolessence` | 12 |
| `Scentbird` | 4 |
| `ScentedMoments` | 3 |
| `Scenteno` | 6 |
| `SchoolofScent` | 12 |
| `SimplyPutScents` | 5 |
| `SokiLondon` | 9 |
| `TLTGReviews` | 6 |
| `TheFragranceApprentice` | 8 |
| `ThePerfumeGuy` | 11 |
| `ThePerfumeNest` | 9 |
| `TheScented` | 2 |
| `TheScentinel` | 4 |
| `TiffBenson` | 3 |
| `funmimonet` | 8 |

## New Admitted Rows

| ID | Handle | Video | Words | Cues | Source |
| --- | --- | --- | ---: | ---: | --- |
| `ytshorts-fragrance-tone-expansion200-v0-001` | `JeremyFragrance` | `ynjAOe4E3yY` | 20 | 9 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-002` | `GentsScents` | `fFWwETz72jk` | 135 | 39 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-003` | `ThePerfumeGuy` | `yL5b44KBD_0` | 311 | 95 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-004` | `SchoolofScent` | `AH_dvrV1NJ0` | 164 | 51 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-005` | `Redolessence` | `0Ym-iX_z7YM` | 245 | 69 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-006` | `TheFragranceApprentice` | `GmM1VNI95P8` | 211 | 61 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-007` | `ChaosFragrances` | `mCUCoxt-rZI` | 467 | 129 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-008` | `FragranceKnowledge` | `jMTtpG8H_mI` | 212 | 77 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-009` | `MilaLeBlanc` | `xzCCRtlvVzU` | 79 | 23 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-010` | `ThePerfumeNest` | `5OKgUA5QiNs` | 314 | 91 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-011` | `DemiRawling` | `_BTBlKLMptw` | 57 | 17 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-012` | `JusDeRose` | `lopKFyja1zk` | 103 | 29 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-013` | `OliviaOlfactory` | `zL3-O1DRo5w` | 302 | 87 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-014` | `MonikaCioch` | `DnE0_jvsbIE` | 22 | 9 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-015` | `Scentbird` | `N3qy8SBGzhQ` | 43 | 11 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-016` | `Scenteno` | `WcUT14n93ic` | 143 | 41 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-017` | `TheScentinel` | `CkYI0Aceeik` | 134 | 37 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-018` | `TiffBenson` | `mrXyKjkwBRc` | 109 | 29 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-019` | `PostCologne` | `aFIDu_KEWL4` | 470 | 137 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-020` | `Cubaknow` | `6o6A5eaHASg` | 364 | 107 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-021` | `SimplyPutScents` | `OG1MpeV31xM` | 167 | 53 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-022` | `TheScented` | `L_V4z_VkDVQ` | 188 | 55 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-023` | `JeremyFragrance` | `biRWOkRX1oM` | 88 | 31 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-024` | `GentsScents` | `mUXNqYZdcg8` | 166 | 45 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-025` | `ThePerfumeGuy` | `gXTvb8CgAbo` | 315 | 95 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-026` | `SchoolofScent` | `cwWxnZEOrBc` | 187 | 55 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-027` | `CurlyScents` | `5Zm0H43FZYo` | 93 | 29 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-028` | `Redolessence` | `PkkvfJyBBLw` | 187 | 53 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-029` | `ChaosFragrances` | `xOsoS19CbGw` | 607 | 175 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-030` | `FragranceKnowledge` | `1wWElbY3320` | 255 | 81 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-031` | `ThePerfumeNest` | `DvJEkb4hYnA` | 393 | 107 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-032` | `DemiRawling` | `Pe5dwQ4Z0bs` | 74 | 19 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-033` | `JusDeRose` | `HdTxGjz1HW0` | 43 | 13 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-034` | `OliviaOlfactory` | `xPfrk0L77Q8` | 330 | 93 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-035` | `MonikaCioch` | `5FPTyaAtaUU` | 219 | 65 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-036` | `Scentbird` | `4zmPW2mcy1w` | 84 | 27 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-037` | `Scenteno` | `queVnhn2wmU` | 134 | 43 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-038` | `TheScentinel` | `WsDv2UYDQOw` | 82 | 23 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-039` | `TiffBenson` | `pWmdISiovo0` | 112 | 31 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-040` | `PostCologne` | `yA4_B0PfdWw` | 402 | 115 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-041` | `Cubaknow` | `eGTJ0-DMo78` | 105 | 35 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-042` | `FragranceView` | `AOiv2vVPsp4` | 337 | 99 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-043` | `SimplyPutScents` | `pXWm5biQUik` | 112 | 33 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-044` | `GentsScents` | `BTUCQByXTqc` | 140 | 39 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-045` | `SchoolofScent` | `aqpNhTTYEpE` | 176 | 53 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-046` | `CurlyScents` | `bXC5K1ti4yM` | 173 | 49 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-047` | `Redolessence` | `1iE5B35c9vU` | 199 | 59 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-048` | `ChaosFragrances` | `U6udcCN59bQ` | 344 | 101 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-049` | `BowTieFragranceGuy` | `IE9zy--St_I` | 306 | 87 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-050` | `MilaLeBlanc` | `n1IqsKklH_Y` | 43 | 11 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-051` | `ThePerfumeNest` | `z_syvxnGcnA` | 271 | 73 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-052` | `DemiRawling` | `Rf1ko3gn7uw` | 49 | 13 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-053` | `JusDeRose` | `AzkdSEdu3Wc` | 189 | 57 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-054` | `MonikaCioch` | `H48OhdYh_Es` | 270 | 79 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-055` | `Scenteno` | `EnJsAPKDVhY` | 86 | 23 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-056` | `PostCologne` | `6LNdYQBpiL0` | 170 | 51 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-057` | `FragranceView` | `ADJiPcUWfEo` | 272 | 75 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-058` | `SimplyPutScents` | `QNlZ-pzV_Ag` | 143 | 45 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-059` | `GentsScents` | `Ht9EY5ZRjMk` | 181 | 51 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-060` | `ThePerfumeGuy` | `iVfrnPwItv4` | 271 | 16 | `youtube_caption_manual` |
| `ytshorts-fragrance-tone-expansion200-v0-061` | `SchoolofScent` | `EmpTsCc11Mc` | 189 | 55 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-062` | `CurlyScents` | `JeEyRK8Lb_E` | 610 | 248 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-063` | `funmimonet` | `djskjcat9dM` | 228 | 61 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-064` | `SokiLondon` | `af9cI-rVLe4` | 159 | 47 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-065` | `Redolessence` | `OCjdJb8N6iw` | 282 | 83 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-066` | `ChaosFragrances` | `Zp3l5dXDTRA` | 574 | 157 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-067` | `BowTieFragranceGuy` | `KFv8wOy5JiI` | 264 | 97 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-068` | `MilaLeBlanc` | `0S4XNBakgIk` | 78 | 19 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-069` | `ThePerfumeNest` | `kgY9lx0SPBI` | 450 | 125 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-070` | `DemiRawling` | `QMkcLt3_Lz8` | 59 | 17 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-071` | `JusDeRose` | `fcPtowOt_x4` | 93 | 21 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-072` | `OliviaOlfactory` | `HBYfgnXGjx0` | 339 | 97 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-073` | `MonikaCioch` | `0WPDt_ZL5aY` | 269 | 79 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-074` | `ScentedMoments` | `ss1HX00gQTY` | 114 | 37 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-075` | `PostCologne` | `XQmKy-y8wY4` | 190 | 59 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-076` | `Cubaknow` | `zi0XLDb_PPw` | 129 | 43 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-077` | `FragranceView` | `V8c4fasUTr4` | 155 | 49 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-078` | `SimplyPutScents` | `z15MdpzcdIQ` | 89 | 25 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-079` | `TheScented` | `Rf3KCzjvwMs` | 377 | 105 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-080` | `JeremyFragrance` | `ZRxgla8xoM8` | 53 | 19 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-081` | `GentsScents` | `u42iSPG_VUI` | 148 | 43 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-082` | `ThePerfumeGuy` | `dsRsi7lPjds` | 220 | 61 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-083` | `SchoolofScent` | `z9OAKSSI--4` | 120 | 35 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-084` | `CurlyScents` | `KVvyF6RUwQY` | 578 | 233 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-085` | `SokiLondon` | `HN_EY29j59w` | 279 | 81 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-086` | `Redolessence` | `gD0MizuZ6NI` | 206 | 57 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-087` | `ChaosFragrances` | `kFP9htAwpUY` | 546 | 151 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-088` | `FragranceKnowledge` | `WCpQz3c_9hM` | 253 | 77 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-089` | `MilaLeBlanc` | `bDHR_1JZBSQ` | 76 | 19 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-090` | `ThePerfumeNest` | `BKRnLvtygSw` | 204 | 61 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-091` | `DemiRawling` | `n9vklEyQbk4` | 52 | 17 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-092` | `JusDeRose` | `nE3LgYFM_Lg` | 167 | 49 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-093` | `OliviaOlfactory` | `74Btp3z6S5I` | 142 | 41 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-094` | `Scenteno` | `QdD_K7VcWnI` | 93 | 25 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-095` | `TheScentinel` | `08KKTawHeUQ` | 122 | 37 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-096` | `TiffBenson` | `5WwfT2Awx2w` | 116 | 35 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-097` | `PostCologne` | `b84JZYXiyxc` | 138 | 43 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-098` | `FragranceView` | `SuqNH9oQ3Rw` | 20 | 9 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-099` | `SimplyPutScents` | `xFUwll4sT9k` | 141 | 39 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion200-v0-100` | `CurlyFragrance` | `HqhdDretITA` | 463 | 127 | `youtube_caption_auto` |

## Residuals

- Caption-only expansion biases toward Shorts with usable caption tracks; no-caption candidates are deferred, not treated as nonexistent.
- The prior 100 rows are retained as previously admitted, including known off-topic/abstain residuals surfaced by labeling.
- The new-row title keyword gate improves topical precision but does not prove every admitted Short is fragrance-relevant after full transcript review.
- The cumulative 200-row index stores data-lake pointers and metadata only; transcript text bodies remain outside the repo.
- Exploratory handles are opportunistic and handle-observed at capture time; failed or non-admitted handles are logged, not silently replaced.
- The companion creator ledger is an observed handle/channel ledger, not a creator identity graph.

## Non-Claims

- not benchmark validation
- not inter-rater reliability
- not buyer proof
- not a tone-label expansion
- not an energy/prosody measure
- not proof that loose rubric fields are repeatable
- not creator identity verification

Energy, pace, volume, and prosodic excitement remain audio-feature questions. They are not inferred from transcript text in this 200-row pool.

Machine-readable detail is in `docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.json`.
