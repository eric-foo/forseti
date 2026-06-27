# YouTube Shorts fragrance tone hard-30 fixture v0

```yaml
retrieval_header_version: 1
artifact_role: Review input / hard-30 fixture summary
scope: Canonical hard-30 transcript-bearing YouTube Shorts fragrance fixture summary.
use_when:
  - Inspecting the hard-30 fixture behind tone-label viability work.
  - Tracing durable transcript pointers for the first balanced fixture.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md
```

Generated: `2026-06-26T09:29:45Z`

Decision: `ADMIT_HARD30_TEXT_BEARING_BALANCED_DURABLE_LAKE_FIXTURE_V0`

This supersedes the earlier 28-row admission artifact. The hard-30 fixture has 30 unique public YouTube Shorts, 3 per selected creator, all admitted through durable `F:\orca-data-lake` transcript pointers, with a minimum transcript word count of 20.

## Counts

- Fixtures: 30
- Unique video IDs: 30
- Minimum observed word count: 26
- Maximum observed word count: 608
- Data root: `F:\orca-data-lake`
- Data root UUID: `01KW1E6N133JT0XCN2KCN0V5A4`

Creator distribution:

- CurlyScents: 3
- GentsScents: 3
- JeremyFragrance: 3
- Redolessence: 3
- SchoolofScent: 3
- SokiLondon: 3
- TLTGReviews: 3
- TheFragranceApprentice: 3
- ThePerfumeGuy: 3
- funmimonet: 3

Transcript routes:

- `youtube_audio_asr_packet`: 1
- `youtube_caption_packet`: 29

## Admission Contract

Required gates:

- Verified Shorts serving surface.
- Transcript route is caption packet or ASR packet.
- `word_count >= 20` and `cue_count > 0`.
- Transcript pointer lives under the verified durable Orca data root.
- Exactly 3 rows per selected creator.

Automatic abstain gates:

- `asr_no_speech`.
- Missing transcript.
- Zero cues.
- Word count below 20.
- Scratch-only provenance pointer.

## Fixture Rows

| Fixture ID | Creator | Video ID | Route | Words | Cues | Origin |
| --- | --- | --- | --- | ---: | ---: | --- |
| `ytshorts-fragrance-tone-hard30-v0-001` | JeremyFragrance | `as7hye0qgYc` | `asr_transcribed` | 26 | 9 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-002` | GentsScents | `ljZ7_JHXNdw` | `caption_captured` | 133 | 37 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-003` | GentsScents | `VOGZUccarFc` | `caption_captured` | 91 | 29 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-004` | GentsScents | `sy-rczzFrYg` | `caption_captured` | 153 | 47 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-005` | ThePerfumeGuy | `rmDwkTrzNxo` | `caption_captured` | 370 | 105 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-006` | ThePerfumeGuy | `5QDcTenklxg` | `caption_captured` | 307 | 85 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-007` | ThePerfumeGuy | `hfyoVdOAYt4` | `caption_captured` | 273 | 17 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-008` | SchoolofScent | `vl-QUTwtneY` | `caption_captured` | 209 | 61 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-009` | SchoolofScent | `WEqUWKA4FUI` | `caption_captured` | 201 | 63 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-010` | SchoolofScent | `uaCSynFfPpc` | `caption_captured` | 235 | 75 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-011` | CurlyScents | `MN3AI-mrPWk` | `caption_captured` | 99 | 31 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-012` | CurlyScents | `FqTrOZbh_DE` | `caption_captured` | 88 | 29 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-013` | funmimonet | `bPJCH9iQUhI` | `caption_captured` | 201 | 55 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-014` | funmimonet | `Uj4bVTM6dm8` | `caption_captured` | 179 | 53 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-015` | SokiLondon | `XDscn2sgW3w` | `caption_captured` | 160 | 45 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-016` | SokiLondon | `Fd-aChpt_Ss` | `caption_captured` | 100 | 31 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-017` | TLTGReviews | `7S40eU8FDCY` | `caption_captured` | 146 | 43 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-018` | TLTGReviews | `-V7MN2IWMpA` | `caption_captured` | 608 | 191 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-019` | TLTGReviews | `Ln1LUflj8d0` | `caption_captured` | 252 | 89 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-020` | Redolessence | `JMmEIv_oG4o` | `caption_captured` | 153 | 47 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-021` | Redolessence | `_Gp2AmN74E8` | `caption_captured` | 165 | 47 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-022` | Redolessence | `Tb-_V-JVNfk` | `caption_captured` | 177 | 53 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-023` | TheFragranceApprentice | `6k8ebJw50tU` | `caption_captured` | 105 | 27 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-024` | TheFragranceApprentice | `5e4y5yNagRI` | `caption_captured` | 33 | 13 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-025` | TheFragranceApprentice | `WcSRnnwSAJM` | `caption_captured` | 166 | 49 | `retained_recapture` |
| `ytshorts-fragrance-tone-hard30-v0-026` | JeremyFragrance | `doNVRDk0X_Y` | `caption_captured` | 149 | 45 | `replacement_capture` |
| `ytshorts-fragrance-tone-hard30-v0-027` | JeremyFragrance | `DUafgG-TLms` | `caption_captured` | 147 | 47 | `replacement_capture` |
| `ytshorts-fragrance-tone-hard30-v0-028` | CurlyScents | `oFSnzMS8yxA` | `caption_captured` | 30 | 9 | `replacement_capture` |
| `ytshorts-fragrance-tone-hard30-v0-029` | funmimonet | `zJVS5UnoHIY` | `caption_captured` | 191 | 55 | `replacement_capture` |
| `ytshorts-fragrance-tone-hard30-v0-030` | SokiLondon | `XTgiBsIaokI` | `caption_captured` | 136 | 37 | `replacement_capture` |

## Dropped Prior Rows

| Creator | Video ID | Reason | Words | Cues |
| --- | --- | --- | ---: | ---: |
| JeremyFragrance | `t4mAPmthgO0` | `asr_no_speech` |  |  |
| JeremyFragrance | `s7F2VDKEIPk` | `asr_no_speech` |  |  |
| CurlyScents | `t2ZqtfUc56k` | `below_min_word_count` | 2 | 3 |
| funmimonet | `ddGipRGnWrI` | `below_min_word_count` | 9 | 5 |
| SokiLondon | `Rxufi0kOFaM` | `below_min_word_count` | 1 | 1 |

## Storage Posture

Prior `C:\tmp` packets are superseded for fixture admission. This fixture points to recaptured/replacement packets under the verified external Orca data root `F:\orca-data-lake`.

## Non-Claims

- Not tone labeling or final scoring.
- Not an energy/prosody measure.
- Not a benchmark-grade labeled corpus.
- Not comment capture, visual analysis, or audio-feature extraction.
- Auto captions and the single ASR row still require downstream cleaning/adjudication before labels are trusted.

Machine-readable detail is in `docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.json`.
