# IG Behavioral Live Validation Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Bounded live validation receipt for the Instagram/Reels behavioral lake adapter after PR #441 and PR #447.
use_when:
  - Checking what the IG behavioral adapter did with a real public logged-out IG grid packet.
  - Recovering the live residuals and the follow-on route diagnostic before deciding the next IG behavior-sync patch.
  - Distinguishing grid/live-lake validation from shared-core, canonical-lake validation, or full live media validation.
open_next:
  - docs/workflows/ig_vs_youtube_behavioral_gap_ledger_v0.md
  - docs/workflows/ig_behavioral_sync_from_youtube_contract_handoff_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca-harness/source_capture/ig_reels_behavioral_lake.py
  - orca-harness/runners/run_source_capture_ig_reels_grid_packet.py
  - orca-harness/runners/run_source_capture_ig_reels_audio_packet.py
branch_or_commit: codex/ig-behavioral-live-validation from origin/main @ b2e0d638 before this receipt was added
stale_if:
  - PR #441 or PR #447 is reverted or superseded by a different IG behavioral adapter/closeout.
  - Any named IG grid, audio, deep-capture, behavioral projection, lake adapter, or focused test source changes.
  - A later live IG validation receipt supersedes this bounded run or the post-receipt route diagnostic.
authority_boundary: retrieval_only
```

## Purpose

This receipt records one bounded live IG validation pass after the IG behavioral
lake adapter landed, plus a later no-write route diagnostic explaining the
standalone-audio failure class. It is evidence of the observed runs only. It is
not shared core work, not a production-readiness claim, not canonical F-lake
validation, and not a claim that full IG media/video preservation is live-green.

## Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom capture-method plus live IG runner/adapter/test sources
  edit_permission: implementation-authorized for bounded live validation/report only
  target_scope: IG behavior-record live validation after the merged IG lane, excluding shared core
  dirty_state_checked: yes
  blocked_if_missing: public logged-out IG capture route, data-lake packet, adapter projection, focused IG tests
```

## Sources Re-read

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `docs/workflows/ig_behavioral_sync_from_youtube_contract_handoff_v0.md`
- `docs/workflows/ig_vs_youtube_behavioral_gap_ledger_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
- `orca-harness/source_capture/ig_reels_behavioral_lake.py`
- `orca-harness/source_capture/ig_reels_behavioral_projection.py`
- `orca-harness/source_capture/transcript/ig_reels_audio_packet.py`
- `orca-harness/source_capture/transcript/audio_asr.py`
- `orca-harness/runners/run_source_capture_ig_reels_audio_packet.py`
- `orca-harness/runners/run_source_capture_ig_reels_deep_capture.py`
- `orca-harness/tests/unit/test_ig_reels_behavioral_lake.py`
- `orca-harness/tests/unit/test_ig_reels_behavioral_projection.py`
- `orca-harness/tests/contract/test_ig_reels_behavioral_projection_no_runtime_imports.py`

## Live Run

Disposable data root:

```text
C:\tmp\orca-ig-live-validation-20260629
```

Grid capture command:

```powershell
python runners/run_source_capture_ig_reels_grid_packet.py --handle jeremyfragrance --decision-question "Live validate IG behavioral lake adapter after PR 441 merge using a bounded public logged-out reels grid capture." --data-root C:\tmp\orca-ig-live-validation-20260629 --max-rows 3 --timeout-seconds 45 --settle-seconds 2
```

Observed grid packet:

```text
C:\tmp\orca-ig-live-validation-20260629\raw\028\01KW99HGKT8Y3MBQSCY00BSGFG
```

Observed packet inventory after the live run and bounded audio attempts:

```json
{
  "packet_count": 1,
  "packets": [
    {
      "packet_id": "01KW99HGKT8Y3MBQSCY00BSGFG",
      "preserved_file_count": 1,
      "source_family": "instagram_creator",
      "source_surface": "ig_reels_grid_dom_passive_json"
    }
  ]
}
```

## Behavioral Projection Observed

The adapter projected three shortcode-keyed items from the live grid packet:

| Shortcode | Grid packet ids | Ranking basis | Transcript sources | Status | Complete | Residuals |
| --- | --- | --- | ---: | --- | --- | --- |
| `DaKeK7vMoR0` | `01KW99HGKT8Y3MBQSCY00BSGFG` | `views_then_engagement` | 0 | `no_extraction_eligible_sources` | false | `ig_comments_not_attempted:DaKeK7vMoR0`; `ig_transcript_source_absent:DaKeK7vMoR0` |
| `DaKeTvDs6vO` | `01KW99HGKT8Y3MBQSCY00BSGFG` | `views_then_engagement` | 0 | `no_extraction_eligible_sources` | false | `ig_comments_not_attempted:DaKeTvDs6vO`; `ig_transcript_source_absent:DaKeTvDs6vO` |
| `DaKeXcVM0sx` | `01KW99HGKT8Y3MBQSCY00BSGFG` | `views_then_engagement` | 0 | `no_extraction_eligible_sources` | false | `ig_comments_not_attempted:DaKeXcVM0sx`; `ig_transcript_source_absent:DaKeXcVM0sx` |

This observed run shows the live grid packet can be discovered and projected by the IG
behavioral lake adapter. It also shows the adapter did not fake completeness:
comments and transcript sources remained absent residuals, and every projected
item stayed incomplete.

## Audio Probe Residual

The standalone audio runner was attempted once per projected shortcode, using
the same disposable data root and `--model tiny`:

```powershell
python runners/run_source_capture_ig_reels_audio_packet.py --shortcode DaKeK7vMoR0 --data-root C:\tmp\orca-ig-live-validation-20260629 --model tiny
python runners/run_source_capture_ig_reels_audio_packet.py --shortcode DaKeTvDs6vO --data-root C:\tmp\orca-ig-live-validation-20260629 --model tiny
python runners/run_source_capture_ig_reels_audio_packet.py --shortcode DaKeXcVM0sx --data-root C:\tmp\orca-ig-live-validation-20260629 --model tiny
```

Each attempt exited before ASR with the same anonymous media-fetch failure class:

```text
audio unavailable for <shortcode>: ERROR: [Instagram] <shortcode>: Instagram sent an empty media response. Check if this post is accessible in your browser without being logged-in. If it is not, then use --cookies-from-browser or --coo
```

No cookies, login, session, or proxy escalation was attempted. The packet
inventory check above observed no `ig_reels_audio` packet in the disposable lake.

## Post-Receipt Route Diagnostic Addendum

After the receipt above was first written, the same lane ran no-write diagnostics
to classify the audio failure before turning it into an IG residual. The shell
environment had `ORCA_DATA_ROOT` cleared and no `--data-root` was passed for the
deep-capture CLI, because the runner persists when either `--data-root` or
`ORCA_DATA_ROOT` is set.

Observed route facts:

- Direct no-write calls to `download_ig_reel_audio(...)` returned
  `status=unavailable` with Instagram's empty-media response for both
  `DaA8n7EhqTR` (the prior legacy successful audio packet in the old lake epoch)
  and `DaKeK7vMoR0` (one of the grid-projected shortcodes from this receipt).
- A direct browser snapshot for `DaA8n7EhqTR` rendered a public Instagram page
  with visible login/signup chrome, caption text, and comments, so the empty
  media response was not enough to classify the public reel page as unavailable.
- `run_source_capture_ig_reels_deep_capture.py --shortcode DaA8n7EhqTR --model tiny`
  first returned `render_unavailable` once, then reran successfully with
  `comments=15`, `transcript_posture=transcribed`, `transcript_cues=14`, and
  `audio_handle=used`.
- `run_source_capture_ig_reels_deep_capture.py --shortcode DaKeK7vMoR0 --model tiny`
  returned `comments=0`, `transcript_posture=transcribed`, `transcript_cues=2`,
  and `audio_handle=used`.

Interpretation: the original audio residual is route-specific. The standalone
anonymous `yt-dlp` route is currently stale or brittle for these live reels; the
browser/deep-capture route can still recover a transient media handle and ASR it
immediately. Future live IG transcript recovery should prefer deep-capture for
this failure class, while preserving the standalone audio route as a legacy or
fallback packet path until repaired. This addendum does not claim canonical
F-root writes, durable media/video preservation, logged-in access, proxy use, or
live-scale cadence.

## Interpretation

- Grid-to-lake-to-behavior projection is live-validated for this bounded public
  logged-out run.
- The standalone anonymous audio route did not produce a live audio packet for
  the three grid-projected reels, so standalone audio-packet live validation
  remains a residual for this run.
- The follow-on no-write diagnostic showed that deep-capture can recover ASR for
  at least one grid-projected shortcode and one prior legacy-success shortcode
  even when standalone `yt-dlp` returns empty media. This narrows the failure to
  the route, not the platform transcript possibility.
- Product-extraction live validation, canonical F-root persistence, full media
  preservation, and shared-core work remain out of scope.

## Verification

Doc and diff checks observed before commit:

```text
python .agents/hooks/check_retrieval_header.py --strict docs/workflows/ig_behavioral_live_validation_receipt_v0.md docs/workflows/orca_repo_map_v0.md
# exit 0, no output

git diff --check
# exit 0, no output

python .agents/hooks/check_retrieval_header.py --changed --strict
# exit 0, no output

python .agents/hooks/check_repo_map_freshness.py --changed --strict --message "Record IG behavioral live validation receipt"
# exit 0, no output
```

Focused IG behavioral tests:

```text
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider --no-header tests/unit/test_ig_reels_behavioral_projection.py tests/unit/test_ig_reels_behavioral_lake.py tests/contract/test_ig_reels_behavioral_projection_no_runtime_imports.py
......................                                                   [100%]
22 passed in 0.76s
```

Broad IG selector:

```text
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider --no-header tests/unit tests/contract -k "ig_reels or ig_"
........................................................................ [ 33%]
........................................................................ [ 67%]
......................................................................   [100%]
214 passed, 1539 deselected in 7.47s
```

## Non-Claims

This receipt does not claim:

- full IG behavioral completeness;
- standalone audio-packet transcript-source live validation;
- canonical-lake deep-capture persistence validation;
- product-extraction live validation;
- shared IG/YT core implementation or readiness;
- live-scale cadence, scheduler, or production readiness;
- legal/access approval beyond the owner-authorized pre-commercial public-content probe posture.
