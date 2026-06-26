# YouTube Shorts fragrance transcript probe summary v0

```yaml
retrieval_header_version: 1
artifact_role: Review input / transcript availability probe summary
scope: Early transcript availability probe for YouTube Shorts fragrance fixture candidates.
use_when:
  - Auditing the first transcript-readiness probe and ASR fallback residuals.
  - Understanding why later durable hard-30 recapture superseded scratch paths.
authority_boundary: retrieval_only
open_next:
  - docs/review-inputs/youtube_shorts_fragrance_tone_fixture_candidates_v0.json
  - docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.md
```

Generated: `2026-06-26T08:55:02Z`

Purpose: transcript availability probe for the YouTube Shorts fragrance rhetorical-tone fixture spike. This is a capture-readiness artifact only; it does not admit fixtures or label tone.

## Inputs

- Candidate pool: `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\youtube-shorts-tone-viability-prompt\docs\review-inputs\youtube_shorts_fragrance_tone_fixture_candidates_v0.json`
- Candidate JSON SHA256: `860cd06c0276da241f5b4555e81ec2034d143f8b7b58e94e038ee0269b83f6fc`
- Initial caption summary: `C:\tmp\youtube_shorts_fragrance_transcript_probe_v0\caption_probe_summary.json`
- Initial caption summary SHA256: `e1b55f95192b97a80d12286128dcb58a4c2ce5cffef371117822c7e2115d7b4f`
- Caption packet temp root: `C:\tmp\youtube_shorts_fragrance_transcript_probe_v0`
- ASR temp data root: `C:\tmp\youtube_shorts_fragrance_asr_lake_v0`
- ASR data-root UUID: `01KW1HX111RQT6VWYJ4BKXE0V1`

## Counts

- Total candidates: 30
- Known Shorts serving-surface rows: 30
- Initial caption batch: {'total': 30, 'captured': 26, 'asr_required': 3, 'failed': 1}
- Caption packets after leading-dash rerun: 27
- ASR fallback records: 3
- Text-bearing transcripts: 28
- ASR `no_speech` records: 2
- Missing after probe: 0

Transcript statuses:

- `asr_no_speech`: 2
- `asr_transcribed`: 1
- `caption_captured`: 27

## ASR Fallback Rows

| Index | Creator | Video ID | ASR posture | Cues | Text-bearing | Derived record |
| --- | --- | --- | --- | ---: | --- | --- |
| 1 | JeremyFragrance | `as7hye0qgYc` | `transcribed` | 9 | yes | `C:\tmp\youtube_shorts_fragrance_asr_lake_v0\derived\ce1\01KW1HXDV6N1D45FG9RJA1GSV2\transcript_asr\asr_small__3228907943726a1b` |
| 2 | JeremyFragrance | `t4mAPmthgO0` | `no_speech` | 0 | no | `C:\tmp\youtube_shorts_fragrance_asr_lake_v0\derived\a98\01KW1HY67DAN5698PH6YPV5WWX\transcript_asr\asr_small__d5d62da57f0f5f2d` |
| 3 | JeremyFragrance | `s7F2VDKEIPk` | `no_speech` | 0 | no | `C:\tmp\youtube_shorts_fragrance_asr_lake_v0\derived\3a0\01KW1HYQ2NKT404AHJV4WZ7YQ3\transcript_asr\asr_small__609c2b671ce19e5b` |

## Operational Notes

- The initial caption batch failed for `-V7MN2IWMpA` because the leading dash was parsed as an option; rerun with `--video-id=-V7MN2IWMpA` succeeded.
- Caption packets use `youtube_captions` and canonicalize transcript locators to `/watch?v=...`; Shorts identity comes from the candidate pool serving-surface verification.
- ASR fallback used `faster-whisper` model `small`; raw audio packets and derived ASR records live only under the temp data root.
- `asr_no_speech` is a successful capture posture with zero cues, not a runner failure, and should abstain from transcript-tone scoring.

## Non-Claims

- Not fixture admission.
- Not tone labeling or tone scoring.
- Not an energy/prosody measure.
- Not a claim that captions are clean human transcripts.
- Not comment capture or engagement-context capture.
- Raw transcript/audio packets remain in `C:\tmp` and are not committed to the repository.

Machine-readable per-video detail is in `docs/review-inputs/youtube_shorts_fragrance_transcript_probe_summary_v0.json`.
