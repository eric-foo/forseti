# IG Canonical F Deep-Capture Product Extraction Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow receipt
scope: Bounded canonical F-lake validation for IG one-render deep-capture, no-network product extraction, and behavioral projection after PR #460 follow-up patches.
use_when:
  - Checking whether IG deep-capture can persist comments/transcript records into F:/orca-data-lake.
  - Checking whether IG product extraction can consume deep-capture transcript records with exact Silver lineage.
  - Checking the residual that a complete extraction rollup must not become behavioral complete when non-extraction residuals remain.
open_next:
  - docs/workflows/ig_behavioral_live_validation_receipt_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca-harness/runners/run_source_capture_ig_reels_creator_deep_capture.py
  - orca-harness/runners/run_source_capture_ig_reels_deep_capture.py
  - orca-harness/runners/run_ig_reels_product_extract.py
  - orca-harness/source_capture/ig_reels_behavioral_projection.py
  - orca-harness/source_capture/ig_reels_behavioral_lake.py
stale_if:
  - PR #460 is superseded or the named IG deep-capture/product/projection files materially change.
  - A later canonical F-lake live validation receipt supersedes this bounded run.
authority_boundary: retrieval_only
```

## Purpose

Record the observed canonical `F:/orca-data-lake` run after the IG exact-key/deep-capture
patch path. This receipt is evidence of the bounded run only. It is not shared-core work, not
production readiness, not durable media/video preservation, not a logged-in/proxy route, and not a
claim that every IG Reel will expose audio.

## Sources Re-read

- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/decision-routing.md`
- `docs/workflows/ig_behavioral_live_validation_receipt_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md`
- `orca-harness/runners/run_source_capture_ig_reels_creator_deep_capture.py`
- `orca-harness/runners/run_source_capture_ig_reels_deep_capture.py`
- `orca-harness/runners/run_ig_reels_product_extract.py`
- `orca-harness/source_capture/ig_reels_behavioral_lake.py`
- `orca-harness/source_capture/ig_reels_behavioral_projection.py`

## Live Canonical Writes

Environment/root observed before running:

```text
ORCA_DATA_ROOT=F:\orca-data-lake
F:\orca-data-lake present
```

Creator grid -> top-N deep-capture command:

```powershell
python orca-harness/runners/run_source_capture_ig_reels_creator_deep_capture.py --handle jeremyfragrance --top-n 3 --model tiny --data-root F:\orca-data-lake --max-rows 6
```

Observed output:

```text
creator=jeremyfragrance reels_in_grid=6 deep_captured=3 top_n=3
  rank=1 shortcode=DaK3uKxBlKy engagement=102 comments=10 transcript_posture=no_speech persisted=persisted: 2 silver lanes under derived/.../DaK3uKxBlKy/ (deepcap_DaK3uKxBlKy__a6f648620b3b18db.json)
  rank=2 shortcode=DaK3va8MYT_ engagement=36 comments=0 transcript_posture=render_unavailable persisted=persisted: 2 silver lanes under derived/.../DaK3va8MYT_/ (deepcap_DaK3va8MYT___8f4a132b9a833adc.json)
  rank=3 shortcode=DaLBRQiMJhQ engagement=31 comments=0 transcript_posture=render_unavailable persisted=persisted: 2 silver lanes under derived/.../DaLBRQiMJhQ/ (deepcap_DaLBRQiMJhQ__354900b9f359f821.json)
```

Direct shortcode deep-capture follow-ups:

```powershell
python orca-harness/runners/run_source_capture_ig_reels_deep_capture.py --shortcode DaA8n7EhqTR --model tiny --data-root F:\orca-data-lake
python orca-harness/runners/run_source_capture_ig_reels_deep_capture.py --shortcode DaKeK7vMoR0 --model tiny --data-root F:\orca-data-lake
```

Observed output:

```text
reel=DaA8n7EhqTR comments=15 transcript_posture=transcribed transcript_cues=14 audio_handle=used
  persisted: 2 silver lanes under derived/.../DaA8n7EhqTR/ (deepcap_DaA8n7EhqTR__aa26a50cb3f6a657.json)

reel=DaKeK7vMoR0 comments=0 transcript_posture=no_audio_handle transcript_cues=0 audio_handle=none
  note: no media handle in the rendered DOM
  persisted: 2 silver lanes under derived/.../DaKeK7vMoR0/ (deepcap_DaKeK7vMoR0__d5332f0410744206.json)
```

## F-Lake Transcript Inventory Observed

A fresh read of `F:/orca-data-lake/derived/*/*/silver__capture__reel_transcript/*` observed 8 IG
deep-capture transcript records, 3 with `transcript_posture=transcribed`:

```text
DEntAFPpiCv  deepcap_DEntAFPpiCv__759f94a331540d1d.json  transcribed  cue_count=31
DZ69knlsDb1  deepcap_DZ69knlsDb1__c746f8a6352b0df8.json  transcribed  cue_count=17
DaA8n7EhqTR  deepcap_DaA8n7EhqTR__aa26a50cb3f6a657.json  transcribed  cue_count=14
```

## No-Network Product Extraction

The product-extraction handoff route was followed: no provider/network call; transcript cues were
read as data and a fake Anthropic-shaped transport returned authored JSON arrays through the existing
validator/writer. The two pending transcripts without specific named fragrance products were written
as `[]`. The Bath & Body Works ASR transcript yielded one low-confidence exact-quote mention from
`teach blossom and neck their spray perfume`.

Observed no-LLM counts:

```text
before: extractable=3 partial_needs_cleanup=0
after:  extractable=0 partial_needs_cleanup=0
```

Written product-mention records fresh-read after persistence:

```text
F:\orca-data-lake\derived\676\DEntAFPpiCv\silver__cleaning__product_mentions\mentions_codex-extraction-v0__63f61275e7dfb1e0.json
  mention_count=0 lineage_schema_version=silver_lineage_v0 source_surface=ig_reels_deep_capture_render_audio
  derived_ref=silver__capture__reel_transcript/deepcap_DEntAFPpiCv__759f94a331540d1d.json

F:\orca-data-lake\derived\85a\DZ69knlsDb1\silver__cleaning__product_mentions\mentions_codex-extraction-v0__853a60a00f9e64db.json
  mention_count=0 lineage_schema_version=silver_lineage_v0 source_surface=ig_reels_deep_capture_render_audio
  derived_ref=silver__capture__reel_transcript/deepcap_DZ69knlsDb1__c746f8a6352b0df8.json

F:\orca-data-lake\derived\a28\DaA8n7EhqTR\silver__cleaning__product_mentions\mentions_codex-extraction-v0__1ed5956f2615a05d.json
  mention_count=1 lineage_schema_version=silver_lineage_v0 source_surface=ig_reels_deep_capture_render_audio
  derived_ref=silver__capture__reel_transcript/deepcap_DaA8n7EhqTR__aa26a50cb3f6a657.json
  mention: brand=unknown line="teach blossom and neck their spray perfume" source_pointer="teach blossom and neck their spray perfume"
```

## Behavioral Projection Observed After Patch

Fresh projection reads after product extraction and the stricter completeness patch:

```text
DEntAFPpiCv:  status=complete complete=true residuals=[]
DZ69knlsDb1:  status=complete_with_residuals complete=false residuals=[grid candidate absent; older render_unavailable transcript residual]
DaA8n7EhqTR:  status=complete_with_residuals complete=false residuals=[grid candidate absent]
```

Interpretation: extraction completion and behavioral completeness are now separated. A transcript
source can be fully extracted while the overall behavior record remains incomplete when grid or
source-quality residuals are present.

## Verification

Local focused/wide tests observed passing after the code patches:

```text
python -m pytest -q orca-harness/tests/unit/test_transcript_product_lake.py orca-harness/tests/unit/test_transcript_product_extractor.py orca-harness/tests/unit/test_source_capture_ig_reels_projection.py orca-harness/tests/unit/test_source_capture_ig_reels_grid_packet.py orca-harness/tests/unit/test_silver_lineage.py orca-harness/tests/unit/test_ig_reels_product_extract.py orca-harness/tests/unit/test_ig_reels_grid.py orca-harness/tests/unit/test_ig_reels_deep_capture_lake.py orca-harness/tests/unit/test_ig_reels_deep_capture.py orca-harness/tests/unit/test_ig_reels_creator_deep_capture.py orca-harness/tests/unit/test_ig_reels_comments.py orca-harness/tests/unit/test_ig_reels_behavioral_projection.py orca-harness/tests/unit/test_ig_reels_behavioral_lake.py orca-harness/tests/unit/test_ig_reels_audio_packet.py orca-harness/tests/contract/test_ig_reels_behavioral_projection_no_runtime_imports.py orca-harness/tests/contract/test_no_llm_imports.py
# exit 0, progress reached [100%]
```

`git diff --check` exited 0 with no output.

## Non-Claims

- Not shared IG/YT core.
- Not proof that every public IG Reel yields audio or transcript.
- Not durable media/video preservation; transient media handles remain redacted and unpersisted.
- Not logged-in, proxy, private-account, or access-gate capture.
- Not production scheduler/cadence readiness.
- Not a gold/Judgment product verdict.
