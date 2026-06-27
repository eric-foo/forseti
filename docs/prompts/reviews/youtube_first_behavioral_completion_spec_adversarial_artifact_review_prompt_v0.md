# YouTube-First Behavioral Completion Spec Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Prompt for a read-only adversarial artifact review of the YouTube-first
  behavioral completion spec before any implementation uses it as authority.
use_when:
  - Commissioning adversarial artifact review of the YouTube-first behavioral completion spec.
  - Checking whether the spec safely preserves behavioral parity without machinery parity.
authority_boundary: retrieval_only
review_target: docs/workflows/youtube_first_behavioral_completion_spec_v0.md
review_target_sha256: 77F0446CE0E2197CD6BE9155CA591AB6D25FF9A5257EFFF6A4A4C3BE23609A14
intended_report_path: docs/review-outputs/adversarial-artifact-reviews/youtube_first_behavioral_completion_spec_adversarial_artifact_review_v0.md
stale_if:
  - docs/workflows/youtube_first_behavioral_completion_spec_v0.md changes from the hash above.
  - docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md changes materially.
  - Any named IG or YouTube source in the source pack changes.
```

## Orca Prompt Preflight

- Output mode: `review-report`; reviewer writes only `docs/review-outputs/adversarial-artifact-reviews/youtube_first_behavioral_completion_spec_adversarial_artifact_review_v0.md`.
- Template kind: `review`; adversarial artifact review.
- Edit permission / targets / branch: read-only review of `docs/workflows/youtube_first_behavioral_completion_spec_v0.md` on branch `codex/unify-capture-core-planning`; no source edits, no patch queue, no implementation.
- Reviews: findings-first adversarial artifact review; severity labels allowed as `critical | major | minor`; findings are decision input only.
- Doctrine change: none authorized. If the reviewer finds doctrine change is required, flag it; do not patch.
- Destinations: this prompt is the input prompt; write the report at the intended report path above.

## Objective

Review the YouTube-first behavioral completion spec for whether it gives a safe,
smallest-complete contract for making YouTube the first complete behavioral
capture lane, while preserving the owner's boundary: behavioral parity is the
goal; shared acquisition machinery is not.

## Required Source Loading

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Read these overlay authority files: `.agents/workflow-overlay/source-loading.md`, `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/prompt-orchestration.md`, `.agents/workflow-overlay/artifact-roles.md`, `.agents/workflow-overlay/retrieval-metadata.md`.
3. REFERENCE-LOAD `workflow-deep-thinking`. Do not apply it until source context is ready.
4. REFERENCE-LOAD `workflow-adversarial-artifact-review`. Do not apply it until source context is ready.
5. SOURCE-LOAD the review target and this comparison source pack:
   - `docs/workflows/youtube_first_behavioral_completion_spec_v0.md` at SHA256 `77F0446CE0E2197CD6BE9155CA591AB6D25FF9A5257EFFF6A4A4C3BE23609A14`
   - `docs/workflows/shared_capture_core_ig_youtube_tiktok_planning_v0.md`
   - `orca-harness/youtube_capture/capture_youtube_v0.py`
   - `orca-harness/youtube_capture/shorts_scroll_capture_v0.py`
   - `orca-harness/source_capture/transcript/youtube_captions.py`
   - `orca-harness/source_capture/transcript/caption_packet.py`
   - `orca-harness/source_capture/transcript/asr_packet.py`
   - `orca-harness/runners/run_transcript_product_extract.py`
   - `orca-harness/source_capture/ig_reels_grid.py`
   - `orca-harness/source_capture/ig_reels_deep_capture.py`
   - `orca-harness/source_capture/ig_reels_deep_capture_lake.py`
6. Declare `SOURCE_CONTEXT_READY` only after the target and source pack are read. If any load-bearing source is unavailable, declare `SOURCE_CONTEXT_INCOMPLETE` and write a blocked/advisory report instead of strict findings.
7. After source readiness, APPLY `workflow-deep-thinking` to frame failure modes, then APPLY `workflow-adversarial-artifact-review` to produce findings.

## Review Axes To Attack

Attack at least these failure modes:

1. The spec accidentally reintroduces machinery parity under behavioral-parity language.
2. The spec underfixes YouTube by leaving candidate ranking, comments, transcript, persistence, or extraction correlation too vague for implementation scoping.
3. The spec copies IG mechanics instead of using IG as a behavioral prompt.
4. Acceptance criteria are fake-pass-prone or test only prose, not behavior.
5. Persistence/correlation language lets metadata/comments, captions/ASR, and extraction remain human-correlated by convention.
6. MGT accepted residuals silently drop a material slice of the intended capability, lack upgrade triggers, or hide risk.
7. The spec leaks implementation authorization, production readiness, live-capture validation, access/legal approval, or TikTok claims.
8. The spec fails to preserve YouTube-specific strengths: caption-first transcript, served-HTML metadata, `youtubei` comment route, and ASR fallback.

## Output Contract

Write a durable report at:

`docs/review-outputs/adversarial-artifact-reviews/youtube_first_behavioral_completion_spec_adversarial_artifact_review_v0.md`

The report must include:

- retrieval header;
- target path and target hash checked against `77F0446CE0E2197CD6BE9155CA591AB6D25FF9A5257EFFF6A4A4C3BE23609A14`;
- `reviewed_by` and `authored_by` fields, using `unrecorded` only when not supplied by the operator;
- source-read ledger for load-bearing sources;
- compact `review_summary` YAML before detailed findings;
- findings first, ordered by severity;
- for every actionable finding: evidence citation, impact, `minimum_closure_condition`, and `next_authorized_action`;
- non-findings only when they rule out plausible material failures;
- residual risk and review-use boundary.

Do not emit `patch_queue_entry`. Do not edit source files. Do not claim approval,
validation, readiness, implementation authorization, or mandatory remediation.