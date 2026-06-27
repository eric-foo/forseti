# YouTube Shorts Fragrance Tone Expansion100 Capture v0

```yaml
retrieval_header_version: 1
artifact_role: Review input / expansion capture summary
scope: Expand the YouTube Shorts fragrance transcript-bearing pool to 100 total admitted Shorts; capture/admission only, no new tone labels.
use_when:
  - Inspecting the 100-row transcript-bearing Shorts pool.
  - Deciding whether to run second-pass labels after rubric adjudication.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_tone_expansion100_capture_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.md
  - docs/review-inputs/youtube_shorts_fragrance_tone_expansion30_capture_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/youtube_shorts_transcript_tone_rubric_delegated_review_adjudication_v0.md
```

## Summary

- Generated at: `2026-06-26T10:50:01Z`
- Data root: `F:\orca-data-lake`
- Data root UUID: `01KW1E6N133JT0XCN2KCN0V5A4`
- Prior admitted total: 60
- New admitted rows: 40
- Cumulative admitted total: 100
- Attempts in this expansion: 48
- Minimum word count gate: 20
- New word-count range: 20 to 607
- Cumulative word-count range: 20 to 609

## Decision

Admit the captured rows as a 100-Short expansion pool, not a labeled benchmark. Tone labeling still waits on the second independent hard-30 pass and agreement check under the adjudicated rubric.

## Admission Status Counts

| Status | Count |
| --- | ---: |
| `admitted` | 40 |
| `dropped_no_caption_asr_deferred` | 2 |
| `dropped_relevance_title_no_match` | 3 |
| `dropped_transcript_under_min_word_count` | 3 |

## New Admitted By Handle

| Handle | Count |
| --- | ---: |
| `BowTieFragranceGuy` | 2 |
| `ChaosFragrances` | 2 |
| `CurlyScents` | 1 |
| `DemiRawling` | 1 |
| `FragranceKnowledge` | 2 |
| `GentsScents` | 2 |
| `JeremyFragrance` | 2 |
| `JusDeRose` | 2 |
| `MilaLeBlanc` | 2 |
| `MonikaCioch` | 1 |
| `OliviaOlfactory` | 1 |
| `Redolessence` | 2 |
| `Scentbird` | 2 |
| `ScentedMoments` | 2 |
| `Scenteno` | 2 |
| `SchoolofScent` | 2 |
| `SokiLondon` | 2 |
| `TLTGReviews` | 1 |
| `TheFragranceApprentice` | 2 |
| `ThePerfumeGuy` | 2 |
| `ThePerfumeNest` | 2 |
| `TheScentinel` | 1 |
| `funmimonet` | 2 |

## Cumulative By Handle

| Handle | Count |
| --- | ---: |
| `BowTieFragranceGuy` | 3 |
| `ChaosFragrances` | 4 |
| `CurlyScents` | 6 |
| `DemiRawling` | 1 |
| `FragranceKnowledge` | 4 |
| `GentsScents` | 7 |
| `JeremyFragrance` | 7 |
| `JusDeRose` | 2 |
| `MilaLeBlanc` | 4 |
| `MonikaCioch` | 1 |
| `OliviaOlfactory` | 1 |
| `ProfessorPerfume` | 1 |
| `Redolessence` | 7 |
| `Scentbird` | 2 |
| `ScentedMoments` | 2 |
| `Scenteno` | 2 |
| `SchoolofScent` | 7 |
| `SokiLondon` | 7 |
| `TLTGReviews` | 6 |
| `TheFragranceApprentice` | 7 |
| `ThePerfumeGuy` | 7 |
| `ThePerfumeNest` | 4 |
| `TheScentinel` | 1 |
| `funmimonet` | 7 |

## New Admitted Rows

| ID | Handle | Video | Words | Cues | Source |
| --- | --- | --- | ---: | ---: | --- |
| `ytshorts-fragrance-tone-expansion100-v0-001` | `JeremyFragrance` | `syjxpoKWbRM` | 124 | 39 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-002` | `GentsScents` | `sNQKEWZ6rTM` | 121 | 37 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-003` | `ThePerfumeGuy` | `ESyg9QXm8MU` | 342 | 97 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-004` | `SchoolofScent` | `ZVU5kePvD2w` | 225 | 67 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-005` | `funmimonet` | `moiH3xaltg0` | 218 | 59 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-006` | `SokiLondon` | `dhFp3M6oMc8` | 153 | 41 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-007` | `TLTGReviews` | `zHTuK2_Ouf0` | 20 | 9 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-008` | `Redolessence` | `gvRng8Hkwyw` | 184 | 57 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-009` | `TheFragranceApprentice` | `fnAGBzFSQnw` | 170 | 45 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-010` | `ChaosFragrances` | `vjzHIMn3b4w` | 538 | 155 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-011` | `FragranceKnowledge` | `9wB39dxIL6M` | 52 | 15 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-012` | `BowTieFragranceGuy` | `n9U1c-QRSO8` | 67 | 23 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-013` | `MilaLeBlanc` | `kgSCH6-SN_A` | 94 | 29 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-014` | `ThePerfumeNest` | `7EdjxOC-MNI` | 415 | 121 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-015` | `Scentbird` | `m3Tnv4p7TAg` | 23 | 9 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-016` | `Scenteno` | `7_kbaCJR_o0` | 47 | 13 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-017` | `JusDeRose` | `G9fk8bgFv8k` | 145 | 41 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-018` | `OliviaOlfactory` | `8iyV0R5D9B4` | 356 | 99 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-019` | `MonikaCioch` | `2tuGZN1vtUw` | 347 | 105 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-020` | `ScentedMoments` | `bGFqsPZ7bWc` | 119 | 37 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-021` | `JeremyFragrance` | `iohVc61b9Bk` | 83 | 41 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-022` | `GentsScents` | `inl7gtQd4EM` | 153 | 49 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-023` | `ThePerfumeGuy` | `-wS9yaoumW8` | 355 | 101 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-024` | `SchoolofScent` | `3UE8ZN1I8zM` | 178 | 49 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-025` | `CurlyScents` | `usFrt5XnBic` | 607 | 187 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-026` | `funmimonet` | `ieDgm6dPS3s` | 161 | 49 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-027` | `SokiLondon` | `wf8wjYjytuI` | 278 | 81 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-028` | `Redolessence` | `Ifa-qYlGEfM` | 281 | 81 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-029` | `TheFragranceApprentice` | `mCNfOHwUYt4` | 188 | 51 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-030` | `ChaosFragrances` | `NJmP-Otw57s` | 572 | 163 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-031` | `FragranceKnowledge` | `uRzXOOZeTSE` | 36 | 9 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-032` | `BowTieFragranceGuy` | `G74XHCSr_CQ` | 398 | 121 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-033` | `MilaLeBlanc` | `hK8RaqDTqo8` | 61 | 23 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-034` | `ThePerfumeNest` | `_zQeVk1r3fg` | 541 | 151 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-035` | `Scentbird` | `hy443hJNeu8` | 22 | 5 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-036` | `Scenteno` | `ZUnhHKu-cgk` | 123 | 35 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-037` | `DemiRawling` | `qP0WyLE4Brc` | 103 | 27 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-038` | `JusDeRose` | `mxS8HENWII8` | 169 | 49 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-039` | `ScentedMoments` | `QGh0xaigTvo` | 105 | 31 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion100-v0-040` | `TheScentinel` | `fDtI1QsNNqY` | 31 | 9 | `youtube_caption_auto` |

## Residuals

- Caption-only expansion biases toward Shorts with usable caption tracks; no-caption candidates are deferred, not treated as nonexistent.
- No tone labels are added in this step because the next uncertainty is second-pass label agreement on hard-30.
- The cumulative 100-row index stores data-lake pointers and metadata only; transcript text bodies remain outside the repo.
- Exploratory handles are opportunistic and handle-verified at capture time; failed handles are logged, not silently replaced.

## Non-Claims

- not benchmark validation
- not inter-rater reliability
- not buyer proof
- not a tone-label expansion
- not an energy/prosody measure
- not proof that loose rubric fields are repeatable

Energy, pace, volume, and prosodic excitement remain audio-feature questions. They are not inferred from transcript text in this 100-row pool.
