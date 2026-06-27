# YouTube Shorts fragrance tone fixture admission v0

```yaml
retrieval_header_version: 1
artifact_role: Review input / fixture admission summary
scope: Admission decision for the initial YouTube Shorts fragrance transcript-bearing fixture candidates.
use_when:
  - Checking how early fixture candidates were admitted or abstained.
  - Tracing pre-hard30 fixture-admission residuals.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_tone_fixture_admission_v0.json
```

Generated: `2026-06-26T09:01:20Z`

Decision: `ADMIT_28_TEXT_BEARING_ROWS_ABSTAIN_2_NO_SPEECH_ROWS`

This admits candidates only for the transcript-rhetorical-tone lane. It does not label tone, does not admit energy/prosody scoring, and does not make the scratch captures production-durable.

## Admission Contract

Required gates:

- Candidate row has `serving_surface == shorts` from the prior Shorts serving-surface verification.
- Transcript route is `youtube_caption_packet` or `youtube_audio_asr_packet`.
- `text_bearing_transcript == true` and `cue_count > 0`.
- A caption packet path or ASR record path is present.

Automatic abstain gates:

- `asr_no_speech`.
- Missing transcript after probe.
- Zero cues.
- Unknown or unverified Shorts serving surface.

## Counts

- Source candidates: 30
- Admitted: 28
- Abstained: 2

Admitted transcript statuses:

- `asr_transcribed`: 1
- `caption_captured`: 27

Admitted creator distribution:

- CurlyScents: 3
- GentsScents: 3
- JeremyFragrance: 1
- Redolessence: 3
- SchoolofScent: 3
- SokiLondon: 3
- TLTGReviews: 3
- TheFragranceApprentice: 3
- ThePerfumeGuy: 3
- funmimonet: 3

Abstain reasons:

- `asr_no_speech_zero_cues`: 2

## Admitted Rows

| Fixture ID | Creator | Video ID | Transcript | Cues |
| --- | --- | --- | --- | ---: |
| `ytshorts-fragrance-tone-v0-001` | JeremyFragrance | `as7hye0qgYc` | `asr_transcribed` | 9 |
| `ytshorts-fragrance-tone-v0-002` | GentsScents | `ljZ7_JHXNdw` | `caption_captured` | 37 |
| `ytshorts-fragrance-tone-v0-003` | GentsScents | `VOGZUccarFc` | `caption_captured` | 29 |
| `ytshorts-fragrance-tone-v0-004` | GentsScents | `sy-rczzFrYg` | `caption_captured` | 47 |
| `ytshorts-fragrance-tone-v0-005` | ThePerfumeGuy | `rmDwkTrzNxo` | `caption_captured` | 105 |
| `ytshorts-fragrance-tone-v0-006` | ThePerfumeGuy | `5QDcTenklxg` | `caption_captured` | 85 |
| `ytshorts-fragrance-tone-v0-007` | ThePerfumeGuy | `hfyoVdOAYt4` | `caption_captured` | 17 |
| `ytshorts-fragrance-tone-v0-008` | SchoolofScent | `vl-QUTwtneY` | `caption_captured` | 61 |
| `ytshorts-fragrance-tone-v0-009` | SchoolofScent | `WEqUWKA4FUI` | `caption_captured` | 63 |
| `ytshorts-fragrance-tone-v0-010` | SchoolofScent | `uaCSynFfPpc` | `caption_captured` | 75 |
| `ytshorts-fragrance-tone-v0-011` | CurlyScents | `t2ZqtfUc56k` | `caption_captured` | 3 |
| `ytshorts-fragrance-tone-v0-012` | CurlyScents | `MN3AI-mrPWk` | `caption_captured` | 31 |
| `ytshorts-fragrance-tone-v0-013` | CurlyScents | `FqTrOZbh_DE` | `caption_captured` | 29 |
| `ytshorts-fragrance-tone-v0-014` | funmimonet | `bPJCH9iQUhI` | `caption_captured` | 55 |
| `ytshorts-fragrance-tone-v0-015` | funmimonet | `Uj4bVTM6dm8` | `caption_captured` | 53 |
| `ytshorts-fragrance-tone-v0-016` | funmimonet | `ddGipRGnWrI` | `caption_captured` | 5 |
| `ytshorts-fragrance-tone-v0-017` | SokiLondon | `XDscn2sgW3w` | `caption_captured` | 45 |
| `ytshorts-fragrance-tone-v0-018` | SokiLondon | `Rxufi0kOFaM` | `caption_captured` | 1 |
| `ytshorts-fragrance-tone-v0-019` | SokiLondon | `Fd-aChpt_Ss` | `caption_captured` | 31 |
| `ytshorts-fragrance-tone-v0-020` | TLTGReviews | `7S40eU8FDCY` | `caption_captured` | 43 |
| `ytshorts-fragrance-tone-v0-021` | TLTGReviews | `-V7MN2IWMpA` | `caption_captured` | 191 |
| `ytshorts-fragrance-tone-v0-022` | TLTGReviews | `Ln1LUflj8d0` | `caption_captured` | 89 |
| `ytshorts-fragrance-tone-v0-023` | Redolessence | `JMmEIv_oG4o` | `caption_captured` | 47 |
| `ytshorts-fragrance-tone-v0-024` | Redolessence | `_Gp2AmN74E8` | `caption_captured` | 47 |
| `ytshorts-fragrance-tone-v0-025` | Redolessence | `Tb-_V-JVNfk` | `caption_captured` | 53 |
| `ytshorts-fragrance-tone-v0-026` | TheFragranceApprentice | `6k8ebJw50tU` | `caption_captured` | 27 |
| `ytshorts-fragrance-tone-v0-027` | TheFragranceApprentice | `5e4y5yNagRI` | `caption_captured` | 13 |
| `ytshorts-fragrance-tone-v0-028` | TheFragranceApprentice | `WcSRnnwSAJM` | `caption_captured` | 49 |

## Abstained Rows

| Creator | Video ID | Status | Reason | Cues |
| --- | --- | --- | --- | ---: |
| JeremyFragrance | `t4mAPmthgO0` | `asr_no_speech` | `asr_no_speech_zero_cues` | 0 |
| JeremyFragrance | `s7F2VDKEIPk` | `asr_no_speech` | `asr_no_speech_zero_cues` | 0 |

## Storage Posture

- `ORCA_DATA_ROOT` was observed unset in the capture session.
- Caption packets are file-packet outputs under `C:\tmp`, not durable lake commits.
- ASR packets are in Orca data-lake format, but under a temporary initialized root at `C:\tmp\youtube_shorts_fragrance_asr_lake_v0`, not the operator durable lake.
- Before production fixture use, recapture or migrate admitted transcript/audio packets into the operator-configured external `ORCA_DATA_ROOT` and refresh pointers.

## Accepted Residuals

- The admitted set is 28, not 30; two public Shorts yielded ASR `no_speech` with zero cues.
- Creator balance is uneven: JeremyFragrance has 1 admitted row while the other selected creators have 3 each.
- This is acceptable for lane viability and prompt/procedure testing, but not for a balanced cross-creator benchmark unless replacements are captured.
- Transcript-only tone must carry an abstain path and must not include text-derived energy claims.

## Hard-30 Replacement Rule

If the fixture must be exactly 30 text-bearing rows, capture 2 replacements and rerun admission. Prefer JeremyFragrance replacements if preserving the original 3-per-creator structure matters; otherwise use any fragrance creator that passes the same public Shorts and transcript gates.

Machine-readable detail is in `docs/review-inputs/youtube_shorts_fragrance_tone_fixture_admission_v0.json`.
