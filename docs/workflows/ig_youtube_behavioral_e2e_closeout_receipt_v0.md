# IG YouTube Behavioral E2E Closeout Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow receipt
scope: Evidence-first closeout for the Instagram/YouTube behavioral-sync lane after IG residual burn-down and current merged-main projection code.
use_when:
  - Checking whether IG and YouTube can be claimed behaviorally complete.
  - Recovering the current canonical F-lake IG behavioral status counts and residuals.
  - Recovering the bounded canonical F-lake YouTube e2e case-set evidence.
open_next:
  - docs/workflows/ig_behavioral_sync_from_youtube_contract_handoff_v0.md
  - docs/workflows/ig_vs_youtube_behavioral_gap_ledger_v0.md
  - docs/workflows/ig_behavioral_missing_input_capture_receipt_v0.md
  - docs/workflows/youtube_behavioral_contract_from_merged_main_v0.md
  - docs/workflows/youtube_behavioral_measurement_corpus_receipt_v0.md
  - orca-harness/source_capture/ig_reels_behavioral_lake.py
  - orca-harness/youtube_capture/behavioral_projection.py
stale_if:
  - A later canonical F-lake IG or YouTube behavioral read supersedes the counts below.
  - IG or YouTube behavioral projection, lake adapter, Silver lineage, or product-extraction semantics change.
  - The F-lake availability index is rebuilt or the bounded YouTube case set is expanded, removed, or superseded.
authority_boundary: retrieval_only
```

## Short Answer

The IG/YT behavioral-sync lane is **not globally behaviorally complete**.

Current evidence supports this narrower claim:

- IG canonical `F:/orca-data-lake` behavioral projection is working and currently reads 19 items:
  12 `complete`, 2 `complete_with_residuals`, and 5 `no_extraction_eligible_sources`.
- YouTube behavioral projection contract is present on merged main and focused projection tests pass.
- The expanded canonical YouTube F-lake caption-route corpus now reads back as 31 complete
  videos: watch metadata/comments packets, caption transcript packets, source-lineage-bearing
  Silver product-mention records, and behavioral projections all read back complete.
- YouTube platform-wide e2e is **not** proven: the observed set is seed-biased, uses
  operator/Codex parser-guarded extraction rather than provider-API extraction, and does not cover
  ASR/no-caption fallback or broad creator-scale behavior.

Therefore the correct closeout status is:

```text
BEHAVIORAL_CONTRACT_SYNC_IMPLEMENTED
CANONICAL_IG_E2E_OBSERVED_WITH_RESIDUALS
CANONICAL_YT_F_LAKE_CAPTION_ROUTE_E2E_OBSERVED_N31
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
original_receipt_source_read_HEAD: a7dc8693da40e01596a3ddfd1340b198e6ccdf06
followup_youtube_e2e_branch_before_docs_update: c71c8d9e
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
  index and `rebuild_availability()` is a write. The initial receipt did not rebuild the F-lake index; the later leading-dash residual-burndown verification rebuilt availability before the fresh YouTube readback.

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

## Initial F-Lake Availability And YouTube Probe

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

- At the initial read, YouTube canonical F-lake e2e was blocked by absent canonical F-lake YouTube packets, not by a
  projection-code failure observed in that pass. The follow-up section below supersedes that initial YouTube absence finding for the bounded two-video case set.
- The default IG projection read depends on the existing availability index for packet-backed grid
  inputs. Because rebuilding availability is a write, this receipt did not rebuild it. The observed
  IG matrix is therefore the current default-read state, not a claim that every raw IG packet in
  `F:/orca-data-lake/raw` is indexed.

## Follow-Up Canonical YouTube F-Lake E2E Run

After the initial receipt found no YouTube packets in `F:/orca-data-lake`, the owner authorized
continuing with material steps 2 and 3. This follow-up created a bounded canonical YouTube case set
and ran it through the behavioral projection path.

Packet writes observed from the runner output:

```text
01KWBNR61N28QRN3Z40FQ68MMR  youtube_watch_metadata_comments  ljZ7_JHXNdw
01KWBNRPGW6CQ021CWCSTNFJF0  youtube_captions                 ljZ7_JHXNdw
01KWBNS5VA6QJJV5SZPXCEVEPE  youtube_watch_metadata_comments  VOGZUccarFc
01KWBNSQ9VS2GBHYM2XZKF9CYV  youtube_captions                 VOGZUccarFc
```

Fresh lake read after capture:

```text
YOUTUBE_AVAILABLE_COUNT 4
01KWBNR61N28QRN3Z40FQ68MMR youtube_watch_metadata_comments
01KWBNRPGW6CQ021CWCSTNFJF0 youtube_captions
01KWBNS5VA6QJJV5SZPXCEVEPE youtube_watch_metadata_comments
01KWBNSQ9VS2GBHYM2XZKF9CYV youtube_captions
```

Silver product-mention records written through the validated product-mention write boundary:

```text
01KWBNRPGW6CQ021CWCSTNFJF0  ljZ7_JHXNdw  mentions_codex_operator_manual_v0__49f6b5ed7347c215.json  mention_count=2
01KWBNSQ9VS2GBHYM2XZKF9CYV  VOGZUccarFc  mentions_codex_operator_manual_v0__6ae6f45ebdbc94db.json  mention_count=10
```

Extraction caveat: no `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `ORCA_PRODUCT_EXTRACT_PROVIDER`, or
`ORCA_PRODUCT_EXTRACT_MODEL` was present in the environment. The silver records therefore use
`extraction_backend=codex_operator_manual_current_thread`, not `provider_api`. The write still used
`parse_mentions(...)`, which rejects items whose `source_pointer` is not a real transcript substring,
and the records carry the existing Silver source-lineage fields from the consumed caption packet.

Observed behavioral projection readback:

| Video id | Metadata | Comments | Transcript source | Product extraction | Projection status | Complete | Residuals |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ljZ7_JHXNdw` | present | sample captured:20 | caption:auto, 37 cues | extracted, 2 mentions | `complete` | true | none |
| `VOGZUccarFc` | present | sample captured:20 | caption:auto, 29 cues | extracted, 10 mentions | `complete` | true | none |

Interpretation:

- Step 2 is done for a bounded two-video canonical YouTube F-lake case set.
- Step 3 is done for that bounded caption-route set: watch packet -> caption packet -> labeled
  operator product extraction -> behavioral projection.
- This closes the earlier "no canonical YouTube F-lake packet" blocker for a bounded caption-route
  e2e claim.
- This does not prove YouTube platform-wide completeness, ASR/no-caption fallback, live provider-API
  extraction, scheduler behavior, or production scale.
- This two-video section is superseded for expanded-corpus measurement by
  `docs/workflows/youtube_behavioral_measurement_corpus_receipt_v0.md`.

## Expanded YouTube Caption-Route Measurement Follow-Up

The expanded measurement receipt now supersedes the initial two-video YouTube evidence for
caption-route measurement.

Fresh canonical `F:/orca-data-lake` readback after the operator/Codex extraction batch and leading-dash residual retry:

```text
YOUTUBE_PACKET_COUNT 64
YOUTUBE_VIDEO_COUNT 33
SURFACE_COMBOS
youtube_captions+youtube_watch_metadata_comments 31
youtube_watch_metadata_comments 2
YOUTUBE_PRODUCT_RECORDS_COMPLETE 31
YOUTUBE_PRODUCT_MENTIONS_TOTAL 122
YOUTUBE_PRODUCT_BACKENDS {"codex_operator_assisted": 1, "codex_operator_manual_current_thread": 2, "codex_operator_measurement_batch_current_thread": 28}
YOUTUBE_PRODUCT_LINEAGE_SURFACES {"youtube_captions": 31}
PROJECTION_STATUS_COUNTS
complete 31
no_extraction_eligible_sources 2
```

Operator/Codex product-extraction batch receipt, plus one later leading-dash retry record reflected in the readback above:

```text
DRY_PARSE requested_mentions=108 accepted_mentions=108 rejected_mentions=0
WRITE_MODEL codex_operator_youtube_measurement_batch_v0
WRITE_BACKEND codex_operator_measurement_batch_current_thread
WRITTEN_COUNT 28
WRITTEN_MENTION_TOTAL 108
EMPTY_COMPLETE_WRITES 2
```

Interpretation:

- The prior YouTube caption-route evidence is no longer just two videos; the measurable caption-route
  cell is now `31/31` complete in the behavioral projection.
- The two remaining YouTube videos are watch-only/no-transcript current-source failures:
  `JcwT5rvhXIc` and `as7hye0qgYc`.
- This remains non-provider extraction. The batch and leading-dash retry used explicit operator/Codex extraction with the
  existing `parse_mentions(...)` quote guard and the existing source-lineage write boundary.
- ASR/no-caption fallback remains the main YouTube residual for platform-wide completeness.

## YouTube Contract Evidence

Current source and tests show the YouTube behavioral projection contract exists and still passes
focused validation:

```text
$env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider --no-header --no-summary --basetemp '..\pytest_tmp_ig_youtube_e2e_closeout' tests/unit/test_ig_reels_behavioral_projection.py tests/unit/test_ig_reels_behavioral_lake.py tests/contract/test_ig_reels_behavioral_projection_no_runtime_imports.py tests/unit/test_youtube_behavioral_projection.py tests/contract/test_youtube_behavioral_projection_no_runtime_imports.py tests/unit/test_transcript_product_lake.py tests/unit/test_transcript_product_extractor.py tests/unit/test_youtube_caption_product_extract.py
........................................................................ [ 68%]
.................................                                        [100%]
105 passed in 4.51s
```

This focused test result remains contract/projection evidence. The follow-up section above is the bounded canonical F-lake YouTube e2e evidence.

## Closeout Decision

Use these claim levels:

| Claim | Status | Basis |
| --- | --- | --- |
| IG projection code can produce per-item behavioral completeness and residuals | observed | 19-item F-lake read through current IG lake adapter |
| IG canonical F-lake has complete items | observed | 12 items read as `complete=true` |
| IG canonical F-lake is globally complete | not proven | 2 residual-complete items and 5 no-eligible-source items remain |
| YT behavioral projection contract exists and focused tests pass | observed | current source read plus 105-test focused run |
| YT canonical F-lake bounded caption-route e2e is complete | observed | 31-video F-lake readback: watch packets, caption packets, source-lineage-bearing product-mention records, and complete projections |
| YT canonical F-lake platform-wide e2e is complete | not proven | ASR/no-caption and creator-scale behavior are not covered; product extraction is operator/Codex, not provider API |
| IG/YT behaviorally complete platform-wide | not proven | IG residuals remain and YouTube ASR/no-caption remains unmeasured |

Recommended next lane, if the owner wants to continue:

1. Add reachable ASR/no-caption YouTube cases and rerun projection readback; this is now the main
   YouTube platform-wide residual.
2. Decide whether operator/Codex parser-guarded product extraction is sufficient caption-route
   evidence, or whether the caption corpus must be rerun through a provider API when credentials
   exist.
3. Separately decide whether IG status semantics should split extraction completeness from
   grid/ranking completeness for grid-missing but extraction-complete items.
4. Do not start shared-core extraction until the bounded YouTube caption-route evidence is accepted
   as sufficient or the ASR/no-caption case set is added.

## Non-Claims

- Not full IG behavioral completeness.
- Not YouTube platform-wide F-lake e2e validation, ASR/no-caption fallback validation, or live provider-API extraction.
- Not shared IG/YT core.
- Not a scheduler, production, live-scale, proxy, login, private-account, durable media/video, ECR, Cleaning, Judgment, or gold-verdict claim.
- Not a data-lake availability-index schema or semantics change.
- Not a broad runtime behavior change beyond the bounded YouTube runner argv-normalization patch documented in the YouTube corpus receipt.
