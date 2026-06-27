# IG Back-Fix And Shared Capture Contract Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Prompt for a read-only adversarial artifact review of the IG back-fix spec and
  shared capture behavioral contract extraction spec before any implementation
  uses them as authority.
use_when:
  - Commissioning adversarial artifact review of the step-3 IG back-fix and step-4 shared contract extraction specs.
  - Checking whether the specs preserve behavioral parity without shared machinery parity.
  - Checking whether IG deep-capture, standalone audio, and shared extraction are correlated without fake completion.
authority_boundary: retrieval_only
review_targets:
  - docs/workflows/ig_backfix_against_youtube_behavioral_contract_spec_v0.md
  - docs/workflows/shared_capture_behavioral_contract_extraction_spec_v0.md
review_target_sha256:
  docs/workflows/ig_backfix_against_youtube_behavioral_contract_spec_v0.md: FD44B9A9AE00DF9D3F31E2B77F196B05184A4B4F9B04BD8D877616EFEA049E1A
  docs/workflows/shared_capture_behavioral_contract_extraction_spec_v0.md: 13A45F12EF75C1C4E9F55BDEEAD875E4E4B55FF1AB5B627C4AB1BC8EFC1C47B5
intended_report_path: docs/review-outputs/adversarial-artifact-reviews/ig_backfix_shared_capture_contract_adversarial_artifact_review_v0.md
stale_if:
  - Either review target changes from the hashes above.
  - docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md changes materially from SHA256 0B656D08C33379F8AE12568B16D0E9EB1FC8C5C20DB5AC874ADEAFF153C3E1F1.
  - docs/workflows/youtube_first_behavioral_completion_spec_v0.md changes materially from SHA256 1D4C8A4B763FC36EF51179A7118516076AE59B90A6F7951677B6B90F75A63590.
  - Any named IG, YouTube, writer, transcript extraction, or product lake source changes.
```

## Orca Prompt Preflight

- Output mode: `review-report`; reviewer writes only `docs/review-outputs/adversarial-artifact-reviews/ig_backfix_shared_capture_contract_adversarial_artifact_review_v0.md`.
- Template kind: `review`; adversarial artifact review.
- Edit permission / targets / branch: read-only review of the two review targets on branch `codex/unify-capture-core-planning`; no source edits, no patch queue, no implementation.
- Reviews: findings-first adversarial artifact review; severity labels allowed as `critical | major | minor`; findings are decision input only.
- Doctrine change: none authorized. If the reviewer finds doctrine change is required, flag it; do not patch.
- Destinations: this prompt is the input prompt; write the report at the intended report path above.

## Objective

Review the IG back-fix spec and shared capture behavioral contract extraction
spec for whether they provide a safe, smallest-complete plan for steps 3 and 4:
back-fix IG against the reviewed YouTube behavioral contract, then extract only
the stable shared behavioral contracts into a thin core.

The owner boundary is load-bearing: behavioral parity is the goal; shared
acquisition machinery, shared transcript priority, shared packet anchors, shared
runner shape, and runtime implementation authority are not.

## Required Source Loading

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Read these overlay authority files: `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/artifact-roles.md`, `.agents/workflow-overlay/retrieval-metadata.md`.
3. REFERENCE-LOAD `workflow-deep-thinking`. Do not apply it until source context is ready.
4. REFERENCE-LOAD `workflow-adversarial-artifact-review`. Do not apply it until source context is ready.
5. SOURCE-LOAD the review targets and compare their hashes against:
   - `docs/workflows/ig_backfix_against_youtube_behavioral_contract_spec_v0.md` = `FD44B9A9AE00DF9D3F31E2B77F196B05184A4B4F9B04BD8D877616EFEA049E1A`
   - `docs/workflows/shared_capture_behavioral_contract_extraction_spec_v0.md` = `13A45F12EF75C1C4E9F55BDEEAD875E4E4B55FF1AB5B627C4AB1BC8EFC1C47B5`
6. SOURCE-LOAD this comparison source pack:
   - `docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md`
   - `docs/workflows/youtube_first_behavioral_completion_spec_v0.md`
   - `docs/review-outputs/adversarial-artifact-reviews/youtube_first_behavioral_completion_spec_review_adjudication_v0.md`
   - `orca-harness/source_capture/ig_reels_grid.py`
   - `orca-harness/source_capture/ig_reels_grid_capture.py`
   - `orca-harness/runners/run_source_capture_ig_reels_grid_packet.py`
   - `orca-harness/source_capture/ig_reels_deep_capture.py`
   - `orca-harness/source_capture/ig_reels_deep_capture_lake.py`
   - `orca-harness/source_capture/transcript/ig_reels_audio_packet.py`
   - `orca-harness/runners/run_ig_reels_product_extract.py`
   - `orca-harness/youtube_capture/capture_youtube_v0.py`
   - `orca-harness/source_capture/transcript/youtube_captions.py`
   - `orca-harness/source_capture/transcript/caption_packet.py`
   - `orca-harness/source_capture/transcript/asr_packet.py`
   - `orca-harness/runners/run_transcript_product_extract.py`
   - `orca-harness/source_capture/writer.py`
   - `orca-harness/cleaning/transcript_product_extractor.py`
   - `orca-harness/cleaning/transcript_product_lake.py`
7. Declare `SOURCE_CONTEXT_READY` only after the target and source pack are read. If any load-bearing source is unavailable, declare `SOURCE_CONTEXT_INCOMPLETE` and write a blocked/advisory report instead of strict findings.
8. After source readiness, APPLY `workflow-deep-thinking` to frame failure modes, then APPLY `workflow-adversarial-artifact-review` to produce findings.

## Review Axes To Attack

Attack at least these failure modes:

1. The IG back-fix spec accidentally copies YouTube mechanics: caption priority,
   served-HTML/`youtubei`, packet-id anchoring, runner shape, or source-specific
   transcript selection.
2. The IG spec underfixes IG by letting deep-capture transcript records remain
   stranded, letting standalone audio and deep capture disagree silently, or
   leaving shortcode-to-anchor lookup as human convention.
3. The shared extraction spec smuggles in a framework, scheduler, base adapter,
   acquisition ladder, or source-changing migration under contract-extraction
   language.
4. The shared contracts are too vague to test: field presence passes but
   correlation does not resolve from item id to candidate/comments/transcript/
   extraction anchors.
5. The canonical transcript rules are unsafe or overfit: they ignore source
   provenance, do not preserve all sources, or hide IG ASR-only reality and
   YouTube caption-first reality.
6. Transient IG media URL redaction and non-durable media-handle posture are
   weakened by the proposed contract language.
7. Acceptance criteria allow fake success, stdout-only completion, manual lookup,
   implementation by convention, or product-extraction compatibility without
   capture-core validation.
8. The specs overclaim: YouTube runtime completion, adversarial re-review of the
   patched YouTube spec, implementation authorization, production readiness,
   live-scale validation, shared acquisition approval, or TikTok coverage.
9. MGT accepted residuals are too broad, lack upgrade triggers, or hide a
   material behavioral gap needed before source-changing implementation.
10. The use of `platform_item_id` over the current extractor field `video_id`
    either hides a real schema migration problem or overstates the need to rename
    working runtime fields.

## Output Contract

Write a durable report at:

`docs/review-outputs/adversarial-artifact-reviews/ig_backfix_shared_capture_contract_adversarial_artifact_review_v0.md`

The report must include:

- retrieval header;
- target paths and target hashes checked against the two hashes above;
- `reviewed_by` and `authored_by` fields, using `unrecorded` only when not supplied by the operator;
- source-read ledger for load-bearing sources;
- compact `review_summary` YAML before detailed findings;
- findings first, ordered by severity;
- for every actionable finding: evidence citation, impact, `minimum_closure_condition`, and `next_authorized_action`;
- non-findings only when they rule out plausible material failures;
- residual risk and review-use boundary.

Do not emit `patch_queue_entry`. Do not edit source files. Do not claim approval,
validation, readiness, implementation authorization, mandatory remediation, or a
runtime model recommendation.