# YouTube Shorts Fragrance Tone Expansion30 Capture v0

```yaml
retrieval_header_version: 1
artifact_role: Review input / expansion capture summary
scope: Step 5 bounded expansion pool for YouTube Shorts transcript-only tone work; capture/admission only, no new tone labels.
use_when:
  - Inspecting the larger transcript-bearing Shorts pool collected after hard-30.
  - Deciding whether to run labels after the delegated rubric review returns.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_tone_expansion30_capture_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.md
  - docs/prompts/reviews/youtube_shorts_transcript_tone_rubric_delegated_adversarial_artifact_review_patch_prompt_v0.md
```

## Summary

- Generated at: `2026-06-26T09:52:50Z`
- Data root: `F:\orca-data-lake`
- Data root UUID: `01KW1E6N133JT0XCN2KCN0V5A4`
- Target new admitted rows: 30
- Actual admitted rows: 30
- Attempts: 43
- Minimum word count gate: 20
- Word-count range: 55 to 609
- Cue-count range: 14 to 159

## Decision

Admit the captured rows as an expansion pool, not a labeled benchmark. This step expands the data foundation while the delegated rubric review is pending. Tone labeling should wait for rubric adjudication.

## Admission Status Counts

| Status | Count |
| --- | ---: |
| `admitted` | 30 |
| `dropped_no_caption_asr_deferred` | 1 |
| `dropped_relevance_title_no_match` | 10 |
| `dropped_transcript_under_min_word_count` | 2 |

## Admitted By Handle

| Handle | Count |
| --- | ---: |
| `BowTieFragranceGuy` | 1 |
| `ChaosFragrances` | 2 |
| `CurlyScents` | 2 |
| `FragranceKnowledge` | 2 |
| `GentsScents` | 2 |
| `JeremyFragrance` | 2 |
| `MilaLeBlanc` | 2 |
| `ProfessorPerfume` | 1 |
| `Redolessence` | 2 |
| `SchoolofScent` | 2 |
| `SokiLondon` | 2 |
| `TLTGReviews` | 2 |
| `TheFragranceApprentice` | 2 |
| `ThePerfumeGuy` | 2 |
| `ThePerfumeNest` | 2 |
| `funmimonet` | 2 |

## Admitted Rows

| ID | Handle | Video | Words | Cues | Source |
| --- | --- | --- | ---: | ---: | --- |
| `ytshorts-fragrance-tone-expansion30-v0-001` | `ChaosFragrances` | `xZ6vd9fyBbw` | 402 | 113 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-002` | `FragranceKnowledge` | `xK8bmugSpgQ` | 105 | 35 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-003` | `ProfessorPerfume` | `vtwo-iaOszA` | 169 | 55 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-004` | `JeremyFragrance` | `JcwT5rvhXIc` | 141 | 43 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-005` | `GentsScents` | `jo03W7cBwBM` | 138 | 35 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-006` | `ThePerfumeGuy` | `17mhHUkRLvg` | 345 | 101 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-007` | `SchoolofScent` | `1K9ej-6aP6g` | 219 | 65 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-008` | `CurlyScents` | `ekaQONEC2ys` | 297 | 93 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-009` | `funmimonet` | `DIMlwC1LsHg` | 112 | 33 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-010` | `SokiLondon` | `frHbes9NwZI` | 180 | 49 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-011` | `TLTGReviews` | `rnJjtCdMZyo` | 117 | 85 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-012` | `Redolessence` | `I_IBUdYJQ6U` | 170 | 53 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-013` | `TheFragranceApprentice` | `EPcHN1WaGBY` | 136 | 43 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-014` | `ChaosFragrances` | `54Ue3UL7XU4` | 609 | 159 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-015` | `FragranceKnowledge` | `weBLSbBqBbs` | 206 | 59 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-016` | `BowTieFragranceGuy` | `hiAWZwgYwQA` | 311 | 87 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-017` | `MilaLeBlanc` | `WLjJ0J4QFBo` | 66 | 29 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-018` | `ThePerfumeNest` | `vDvnnG2iaGQ` | 401 | 109 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-019` | `JeremyFragrance` | `tQ0RKdd1o9g` | 135 | 39 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-020` | `GentsScents` | `KorM3KkSUrs` | 187 | 53 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-021` | `ThePerfumeGuy` | `BhA4y28lmt0` | 246 | 14 | `youtube_caption_manual` |
| `ytshorts-fragrance-tone-expansion30-v0-022` | `SchoolofScent` | `cc7MLqJl9SY` | 227 | 73 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-023` | `CurlyScents` | `vLiFRCQhV0s` | 260 | 71 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-024` | `funmimonet` | `GcAIds8HW38` | 177 | 49 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-025` | `SokiLondon` | `3Abc0p30r9c` | 201 | 55 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-026` | `TLTGReviews` | `wBzGGKsOdyY` | 193 | 61 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-027` | `Redolessence` | `Az4cCq5L0NE` | 293 | 87 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-028` | `TheFragranceApprentice` | `YWnj7wFOqO0` | 105 | 27 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-029` | `MilaLeBlanc` | `hwRSgl1RUL8` | 55 | 17 | `youtube_caption_auto` |
| `ytshorts-fragrance-tone-expansion30-v0-030` | `ThePerfumeNest` | `W3HTpUsaHiA` | 481 | 137 | `youtube_caption_auto` |

## Residuals

- Caption-only expansion biases toward Shorts with usable caption tracks; no-caption ASR candidates are deferred, not treated as nonexistent.
- No tone labels are added in this step because the delegated rubric review may change the instrument.
- The exploratory handle list is opportunistic and handle-verified at capture time; failed handles are logged, not silently replaced.
- No transcript text bodies are stored in this repo artifact; durable transcript pointers resolve to the external data lake.

## Non-Claims

- not benchmark validation
- not inter-rater reliability
- not buyer proof
- not a tone-label expansion
- not an energy/prosody measure
- not a claim that the rubric survived delegated review

Energy, pace, volume, and prosodic excitement remain audio-feature questions. They are not inferred from transcript text in this expansion pool.
