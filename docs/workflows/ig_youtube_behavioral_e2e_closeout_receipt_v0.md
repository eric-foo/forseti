# IG YouTube Behavioral E2E Closeout Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow receipt
scope: Evidence-first closeout for the Instagram/YouTube behavioral-sync lane after IG residual burn-down and current merged-main projection code.
use_when:
  - Checking whether IG and YouTube can be claimed behaviorally complete.
  - Recovering the current canonical F-lake IG behavioral status counts and residuals.
  - Distinguishing YouTube projection-contract proof from canonical F-lake YouTube e2e evidence.
open_next:
  - docs/workflows/ig_behavioral_sync_from_youtube_contract_handoff_v0.md
  - docs/workflows/ig_vs_youtube_behavioral_gap_ledger_v0.md
  - docs/workflows/ig_behavioral_missing_input_capture_receipt_v0.md
  - docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md
  - orca-harness/source_capture/ig_reels_behavioral_lake.py
  - orca-harness/youtube_capture/behavioral_projection.py
stale_if:
  - A later canonical F-lake IG or YouTube behavioral read supersedes the counts below.
  - IG or YouTube behavioral projection, lake adapter, Silver lineage, or product-extraction semantics change.
  - The F-lake availability index is rebuilt or canonical YouTube packets are added to F:/orca-data-lake.
authority_boundary: retrieval_only
```

## Short Answer

The IG/YT behavioral-sync lane is **not globally behaviorally complete**.

Current evidence supports this narrower claim:

- IG canonical `F:/orca-data-lake` behavioral projection is working and currently reads 19 items:
  12 `complete`, 2 `complete_with_residuals`, and 5 `no_extraction_eligible_sources`.
- YouTube behavioral projection contract is present on merged main and focused projection tests pass.
- Canonical YouTube F-lake e2e is **not observed**: the F-lake availability index has no
  `source_family=youtube` packets, and a raw manifest scan found no YouTube raw packet manifests.

Therefore the correct closeout status is:

```text
BEHAVIORAL_CONTRACT_SYNC_IMPLEMENTED
CANONICAL_IG_E2E_OBSERVED_WITH_RESIDUALS
CANONICAL_YT_F_LAKE_E2E_NOT_OBSERVED
PLATFORM_WIDE_COMPLETENESS_NOT_CLAIMED
```

## Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom IG/YT behavioral closeout pack
  edit_permission: docs-write
  target_scope: evidence-first IG/YT behavioral e2e closeout receipt, no code patch
  dirty_state_checked: yes
  blocked_if_missing: current origin/main worktree, F:/orca-data-lake read, IG projection read, YouTube packet probe, focused projection tests
```

Worktree and revision:

```text
workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\ig-youtube-behavioral-e2e-closeout
branch: codex/ig-youtube-behavioral-e2e-closeout
HEAD: a7dc8693da40e01596a3ddfd1340b198e6ccdf06
data_root: F:\orca-data-lake
```

## Source Basis

Fresh-read workflow and overlay sources:

- `AGENTS.md` was supplied in the current task context.
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `docs/workflows/ig_behavioral_sync_from_youtube_contract_handoff_v0.md`
- `docs/workflows/ig_vs_youtube_behavioral_gap_ledger_v0.md`
- `docs/workflows/ig_behavioral_missing_input_capture_receipt_v0.md`
- `docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`

Fresh code-source checks:

- `orca-harness/source_capture/ig_reels_behavioral_lake.py` wires product-mention read status
  through `silver_record_source_backed_status(...)` and downgrades complete record sets when
  source lineage is not source-backed complete.
- `orca-harness/source_capture/ig_reels_behavioral_projection.py` exposes
  `behavioral_completeness`, `complete_with_residuals`, and source-backed extraction status fields.
- `orca-harness/youtube_capture/behavioral_projection.py` exposes metadata/comment normalization,
  transcript-source discovery, extraction rollup, residuals, and read-only lake projection.
- `orca-harness/data_lake/root.py` confirms `list_available(...)` reads the existing availability
  index and `rebuild_availability()` is a write. This receipt did not rebuild the F-lake index.

## Fresh IG F-Lake Read

Command shape:

```powershell
python - <<read-only projection script using DataLakeRoot.resolve(explicit="F:\orca-data-lake") and project_ig_reels_behavioral_index_from_lake(...)>>
```

Observed counts:

```text
IG_INDEX_ITEMS 19
IG_STATUS_COUNTS
complete: 12
complete_with_residuals: 2
no_extraction_eligible_sources: 5
IG_RESIDUAL_PREFIX_COUNTS
ig_comments_render_unavailable: 1
ig_grid_candidate_absent: 4
ig_transcript_source_no_audio_handle: 1
ig_transcript_source_not_extraction_eligible: 3
ig_transcript_source_render_unavailable: 2
```

Observed per-item matrix:

| Shortcode | Status | Complete | Candidate | Comments | Transcript sources | Eligible | Transcript postures | Extraction statuses | Residuals |
| --- | --- | --- | --- | --- | ---: | ---: | --- | --- | --- |
| `DC9vnmgJWPf` | `complete` | true | present | captured:11 | 1 | 1 | transcribed | extracted |  |
| `DEntAFPpiCv` | `complete` | true | present | captured:15 | 1 | 1 | transcribed | extracted |  |
| `DF3CdyJv79A` | `complete` | true | present | captured:15 | 1 | 1 | transcribed | extracted |  |
| `DZ69knlsDb1` | `complete_with_residuals` | false | absent | captured:15 | 2 | 1 | render_unavailable, transcribed | not_extraction_eligible, extracted | `ig_grid_candidate_absent`; `ig_transcript_source_render_unavailable`; `ig_transcript_source_not_extraction_eligible` |
| `DaA8n7EhqTR` | `complete_with_residuals` | false | absent | captured:15 | 1 | 1 | transcribed | extracted | `ig_grid_candidate_absent` |
| `DaGUhsKsYL9` | `complete` | true | present | captured:5 | 1 | 1 | transcribed | extracted |  |
| `DaH3L1Isdrc` | `complete` | true | present | captured:14 | 1 | 1 | transcribed | extracted |  |
| `DaINMZCCb6N` | `complete` | true | present | captured:4 | 1 | 1 | transcribed | extracted |  |
| `DaIr5aRsp8p` | `complete` | true | present | captured:15 | 1 | 1 | transcribed | extracted |  |
| `DaK3uKxBlKy` | `no_extraction_eligible_sources` | false | present | captured:10 | 1 | 0 | no_speech | not_extraction_eligible |  |
| `DaK3va8MYT_` | `no_extraction_eligible_sources` | false | absent | render_unavailable:0 | 1 | 0 | render_unavailable | not_extraction_eligible | `ig_grid_candidate_absent`; `ig_comments_render_unavailable`; `ig_transcript_source_render_unavailable`; `ig_transcript_source_not_extraction_eligible` |
| `DaKd8E9skt8` | `complete` | true | present | empty:0 | 1 | 1 | transcribed | extracted |  |
| `DaKeK7vMoR0` | `no_extraction_eligible_sources` | false | absent | empty:0 | 1 | 0 | no_audio_handle | not_extraction_eligible | `ig_grid_candidate_absent`; `ig_transcript_source_no_audio_handle`; `ig_transcript_source_not_extraction_eligible` |
| `DaKeXcVM0sx` | `no_extraction_eligible_sources` | false | present | captured:10 | 1 | 0 | no_speech | not_extraction_eligible |  |
| `DaKkXGQBE9i` | `complete` | true | present | captured:3 | 1 | 1 | transcribed | extracted |  |
| `DaKkwCiB_2B` | `no_extraction_eligible_sources` | false | present | captured:3 | 1 | 0 | no_speech | not_extraction_eligible |  |
| `DaLBRQiMJhQ` | `complete` | true | present | captured:8 | 1 | 1 | transcribed | extracted |  |
| `DaLBhRbskFa` | `complete` | true | present | captured:4 | 1 | 1 | transcribed | extracted |  |
| `DaLK8b9s9z9` | `complete` | true | present | captured:9 | 1 | 1 | transcribed | extracted |  |

Interpretation:

- IG is behaviorally complete for 12 observed F-lake items under the current projection semantics.
- IG still has visible residuals for grid absence, stale/render-unavailable transcript sources, no-audio, and no-speech cases.
- `complete_with_residuals` correctly keeps `complete=false`; the lane is not faking whole-item completeness.
- No-speech items with captured comments remain incomplete because there is no extraction-eligible creator transcript source.

## F-Lake Availability And YouTube Probe

Read-only F-lake packet inventory:

```text
AVAILABLE_TOTAL 37
AVAILABILITY_SOURCE_FAMILIES
fragrance_native_database: 6
fragrance_purchase_review_pdp: 1
instagram_creator: 2
reddit: 10
web_page: 18
YOUTUBE_AVAILABLE []
RAW_MANIFESTS 41
RAW_SOURCE_FAMILIES
fragrance_native_database: 6
fragrance_purchase_review_pdp: 1
instagram_creator: 6
reddit: 10
web_page: 18
```

IG availability-index caveat:

```text
IG_AVAILABLE_IDS
01KW9T6R7BFDJKG7WSW7PMVSMP
01KWA193403TYNTBJVWAP5W5NE
IG_RAW_NOT_IN_AVAILABILITY
01KW9T4ESARHD545RRPGCWWY1P
01KW9T5SGKBYD8HRVP3154F4Y8
01KW9T70AM3SZE4VXKWG17ANZG
01KW9WD600VE4NXCKF364N8ZH9
```

Interpretation:

- YouTube canonical F-lake e2e is blocked by absent canonical F-lake YouTube packets, not by a
  projection-code failure observed in this pass.
- The default IG projection read depends on the existing availability index for packet-backed grid
  inputs. Because rebuilding availability is a write, this receipt did not rebuild it. The observed
  IG matrix is therefore the current default-read state, not a claim that every raw IG packet in
  `F:/orca-data-lake/raw` is indexed.

## YouTube Contract Evidence

Current source and tests show the YouTube behavioral projection contract exists and still passes
focused validation:

```text
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider --no-header tests/unit/test_ig_reels_behavioral_projection.py tests/unit/test_ig_reels_behavioral_lake.py tests/contract/test_ig_reels_behavioral_projection_no_runtime_imports.py tests/unit/test_youtube_behavioral_projection.py tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py
............................................                             [100%]
44 passed in 2.18s
```

This is contract/projection evidence. It is not canonical F-lake YouTube e2e evidence because no
YouTube raw packet or availability entry was observed in `F:/orca-data-lake`.

## Closeout Decision

Use these claim levels:

| Claim | Status | Basis |
| --- | --- | --- |
| IG projection code can produce per-item behavioral completeness and residuals | observed | 19-item F-lake read through current IG lake adapter |
| IG canonical F-lake has complete items | observed | 12 items read as `complete=true` |
| IG canonical F-lake is globally complete | not proven | 2 residual-complete items and 5 no-eligible-source items remain |
| YT behavioral projection contract exists and focused tests pass | observed | current source read plus 44-test focused run |
| YT canonical F-lake e2e is complete | not observed | no `source_family=youtube` packets in availability or raw manifests |
| IG/YT behaviorally complete platform-wide | not proven | platform-wide evidence and YT canonical F-lake data absent |

Recommended next lane, if the owner wants to continue:

1. Decide whether to create or capture a bounded canonical YouTube F-lake case set.
2. If yes, run a YT packet -> transcript -> extraction -> projection receipt against `F:/orca-data-lake`.
3. Separately decide whether IG status semantics should split extraction completeness from grid/ranking completeness for grid-missing but extraction-complete items.
4. Do not start shared-core extraction until the canonical YT F-lake evidence gap is closed or explicitly accepted as out-of-scope.

## Non-Claims

- Not full IG behavioral completeness.
- Not canonical YouTube F-lake e2e validation.
- Not shared IG/YT core.
- Not a scheduler, production, live-scale, proxy, login, private-account, durable media/video, ECR, Cleaning, Judgment, or gold-verdict claim.
- Not a data-lake availability-index rebuild.
- Not a code patch or runtime behavior change.
