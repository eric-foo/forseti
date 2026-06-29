# YouTube Downstream ECR Cleaning Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for de-correlated adversarial implementation/code review
  of the YouTube caption -> ECR source-side receipts -> CleaningPacket smoke
  runner patch and the YouTube transcript product-mention cleaning validation.
use_when:
  - Commissioning an independent reviewer to inspect the YouTube downstream ECR
    cleaning implementation lane.
  - Checking the prompt source, scope, and output binding for this review.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
  - docs/prompts/handoffs/youtube_downstream_ecr_cleaning_lane_handoff_v0.md
branch_or_commit: codex/youtube-downstream-ecr-cleaning at 014eeb77339665e4d7885d53b8fc2fdf195a62b5
stale_if:
  - The target branch is rebased, merged, or materially updated.
  - Any target implementation file changes after this prompt is filed.
  - The review-output destination already exists and the operator has not authorized a new version.
```

## Orca Prompt Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_youtube_downstream_ecr_cleaning_code_review
  edit_permission: read-only
  target_scope: >
    Read-only adversarial code review of the YouTube downstream ECR-cleaning
    implementation diff on branch codex/youtube-downstream-ecr-cleaning.
  dirty_state_checked: yes
  branch: codex/youtube-downstream-ecr-cleaning
  expected_head: 014eeb77339665e4d7885d53b8fc2fdf195a62b5
  dirty_state_allowance: >
    The review target branch should be clean at the expected head. Do not modify
    files, stage, commit, push, or open/modify PRs. If the branch is dirty,
    report the dirty paths and continue only if they are exactly the filed
    prompt artifact or review output you are writing.
  output_mode: review-report
  prompt_artifact_path: docs/prompts/reviews/youtube_downstream_ecr_cleaning_adversarial_code_review_prompt_v0.md
  review_output_path: docs/review-outputs/youtube_downstream_ecr_cleaning_adversarial_code_review_v0.md
  template_kind: review
  template_source: >
    Orca-local repo-code-review template is unbound; this prompt uses the
    workflow-prompt-orchestrator review frame plus Orca overlay review doctrine.
  blocked_if_missing:
    - orca-harness/runners/run_capture_ecr_cleaning_smoke.py
    - orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
    - orca-harness/tests/unit/test_transcript_product_lake.py
```

## Cynefin Route

Smallest complete outcome: a read-only adversarial implementation/code review of
the three-file YouTube downstream ECR-cleaning diff, with findings as decision
input for the home model.

Regime: Complicated.

Why: the task crosses implementation correctness, prompt routing, review-lane
authority, and the provisional delegated-review-patch convention, but the target
files and validation evidence are bounded.

Decomposition: layer-based, with prompt/review authority checked before code
claims, then implementation source review.

Current bottleneck: the receiving reviewer must verify the target branch and
source context before applying review methods.

Riskiest assumption: a de-correlated receiving controller with repo access is
available. If not, the review may still return advisory findings, but must not
claim cross-vendor discovery or no-new-seam.

Stop or pivot condition: if the branch/head differs, required target files are
missing, or the receiving controller cannot establish source context, return
`SOURCE_CONTEXT_INCOMPLETE` or the nearest blocker instead of reviewing a
summary.

Allowed next move: read-only adversarial code review and durable review report.

Disallowed next move: local self-review by the authoring lane, patching,
staging, committing, pushing, live capture, live LLM transport, projection,
derived retrieval, or gold/Judgment verdict work.

## Delegated Review-Patch Route Decision

This prompt was prepared after an explicit `workflow-delegated-review-patch`
request. The target is a multi-file implementation/code diff, not a single
high-stakes authored artifact with bounded patch authority. Per
`.agents/workflow-overlay/delegated-review-patch.md`, do not force this into the
single-artifact delegated review-and-patch convention.

Route this as a read-only adversarial implementation/code review. Patch
execution is not commissioned by this prompt.

## Actor And De-Correlation Receipt

- author_home_model_family: OpenAI / GPT-family Codex, recorded from the authoring lane.
- controller_model_family: `operator_to_fill`; must be a different upstream vendor/model lineage to claim cross-vendor discovery.
- current_receiving_actor_role: controller.
- dispatch_mode: external-controller-courier.
- de_correlation_status: `operator_to_fill`; if controller model family is missing, undisclosed, same-vendor, or otherwise not provably different from the author/home family, return advisory findings only and do not claim cross-vendor discovery or no-new-seam.
- no runtime model recommendation is made by this prompt.

## Source-Gated Method Contract

1. REFERENCE-LOAD `workflow-deep-thinking` and `workflow-code-review` if
   available in your environment. Do not APPLY them yet.
2. Read the required Orca authority and task sources below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing
   sources, conflicts, unavailable tools, or branch/head mismatch.
4. Only after source readiness, APPLY deep-thinking to frame material failure
   modes, then APPLY workflow-code-review to produce findings-first
   implementation/code review.
5. If `workflow-code-review` is unavailable, use findings-only advisory code
   review from the prompt text below, but mark strict review claims
   `NOT_CLAIMED`.

## Review Objective

Review whether the branch honestly makes YouTube caption packets first-class in
the Capture -> ECR source-side receipt -> CleaningPacket smoke path, and whether
the existing transcript product-mention cleaning path is validated on YouTube
without overclaiming beyond silver cleaning records.

Attack especially:

- whether YouTube packet handling preserves raw source slices, file anchors,
  hashes, packet keys, and ECR refs without projection refs;
- whether SP-1/2/3/6 ECR postures are derived through the existing
  source-agnostic derivers without a YouTube-specific override;
- whether non-clear timing/source-visibility residuals remain visible instead
  of being smoothed into false success;
- whether Cleaning input handles are file-level and source-backed rather than
  invented row/projection anchors;
- whether the product-mention cleaning validation proves only offline silver
  product-mention records, not live transport, gold verdicts, projection,
  derived retrieval, Judgment readiness, or end-to-end production readiness;
- whether the tests actually catch the failure modes this implementation is
  meant to protect.

## Worktree And Target State

Workspace:
`C:\Users\vmon7\Desktop\projects\orca\worktrees\youtube-downstream-ecr-cleaning`

Expected branch/head:

```text
branch: codex/youtube-downstream-ecr-cleaning
HEAD: 014eeb77339665e4d7885d53b8fc2fdf195a62b5
tracking: origin/codex/youtube-downstream-ecr-cleaning
status at prompt authoring before this prompt file: clean
```

Target diff against `origin/main` at prompt authoring:

```text
M	orca-harness/runners/run_capture_ecr_cleaning_smoke.py
M	orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
M	orca-harness/tests/unit/test_transcript_product_lake.py
```

Commit under review:

```text
014eeb77 feat: wire youtube captions into ecr smoke runner
3 files changed, 231 insertions(+), 3 deletions(-)
```

## Required Reads

Read these authority and routing sources first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/safety-rules.md`
- `docs/prompts/handoffs/youtube_downstream_ecr_cleaning_lane_handoff_v0.md`

Read these target implementation files:

- `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
- `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`
- `orca-harness/tests/unit/test_transcript_product_lake.py`

Read these adjacent implementation sources as needed for correctness:

- `orca-harness/ecr/deriver.py`
- `orca-harness/ecr/models.py`
- `orca-harness/ecr/__init__.py`
- `orca-harness/ecr/lake.py`
- `orca-harness/source_capture/transcript/caption_packet.py`
- `orca-harness/source_capture/transcript/asr_packet.py`
- `orca-harness/runners/run_transcript_product_extract.py`
- `orca-harness/cleaning/transcript_product_extractor.py`
- `orca-harness/cleaning/transcript_product_lake.py`
- `orca-harness/schemas/product_mention_models.py`

Read these product/contract sources only to resolve boundary claims:

- `orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_frame_source_visibility_slice_architecture_plan_v0.md`
- `orca/product/spines/ecr/evidence_candidate_record/ecr_consolidation_v0_sp1_sp2_sp3_source_side_slice_plan_v0.md`
- `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md`
- `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md`

## Validation Evidence To Inspect

The authoring lane reported these checks:

```powershell
cd orca-harness
python -m pytest -p no:cacheprovider -q tests/unit/test_capture_ecr_cleaning_smoke_runner.py::test_runner_writes_ecr_receipts_and_cleaning_packet_for_youtube tests/unit/test_transcript_product_lake.py::test_runner_extracts_caption_transcript tests/contract/test_no_llm_imports.py
```

Observed output:

```text
... [100%]
```

```powershell
cd orca-harness
python -m pytest -p no:cacheprovider -q tests/unit/test_capture_ecr_cleaning_smoke_runner.py tests/unit/test_transcript_product_lake.py
```

Observed output after one test-regex correction:

```text
.............................................................. [100%]
```

```powershell
cd orca-harness
python -m pytest -p no:cacheprovider -q
```

Observed output ended:

```text
.......................................                                  [100%]
============================== warnings summary ===============================
tests\integration\test_reddit_screening_read_live.py:17
  PytestUnknownMarkWarning: Unknown pytest.mark.integration ...
```

You may rerun read-only tests or checks if your environment permits. If you do
not rerun them, report validation as author-supplied and not independently
revalidated.

## Review Questions

1. Does the YouTube entry point mirror the correct existing source-family shape,
   or does it accidentally inherit retail/IG projection assumptions?
2. Are the YouTube packet `source_slices` converted into Cleaning input handles
   with correct file-level anchors, no projection refs, and valid ECR refs?
3. Are SP-3 timing and SP-6 source-visibility residuals surfaced honestly for
   YouTube caption packets, rather than incorrectly treated as clear?
4. Does the runner validate packet source family and manifest consistency tightly
   enough to prevent cross-family false positives?
5. Does the summary/count output distinguish YouTube source files and handles in
   a way future smoke users can inspect?
6. Does the transcript product lake test assert the meaningful silver record
   fields: mention count, `transcript_source`, quote, and timestamps?
7. Are there missing negative tests that would let a broken caption packet,
   missing preserved source, wrong source family, bad ECR ref, or live LLM import
   pass unnoticed?
8. Does any code or test imply validation, readiness, gold/Judgment output,
   live transport, projection, derived retrieval, or production E2E proof that
   the lane did not establish?

## Strict-Claim Boundary

This review must not claim formal implementation-review authority, readiness,
acceptance, validation, approval, merge safety, or pass/fail verdict unless Orca
overlay authority is supplied separately. Use findings-only advisory review.

Do not emit `patch_queue_entry`. Do not edit source files. Do not commit, push,
PR, run live capture, wire live LLM transport, build projection, build
derived-retrieval, build gold verdicts, or touch IG lanes.

If you find no blocker or major issue, say so and state residual risks or
validation gaps. If you find an issue, findings lead the report and must include:

- finding id
- severity as `blocker`, `major`, or `minor` for prioritization only, not formal Orca verdict authority
- target file and stable line/anchor
- evidence from the implementation
- authority or evidence basis
- concrete impact
- minimum closure condition
- next authorized action
- validation expectation

## Output Contract

Write the full review report to:

`docs/review-outputs/youtube_downstream_ecr_cleaning_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by: operator_to_fill`
- `authored_by: gpt-family-codex`
- `de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded`
- `same_vendor_rationale:` required if `de_correlation_bar` is `same_vendor_sanity`
- source-read ledger
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`
- findings first
- open questions and residual risk
- validation evidence inspected and validation not-run gaps
- review-use boundary: findings are decision input only, not approval, validation, mandatory remediation, or executor-ready patch authority until separately accepted or authorized

After writing the report, return only a compact summary plus:

```yaml
review_courier:
  output_mode: filesystem-output
  report_path: docs/review-outputs/youtube_downstream_ecr_cleaning_adversarial_code_review_v0.md
  commission: adversarial implementation/code review of YouTube downstream ECR-cleaning diff
  target:
    - orca-harness/runners/run_capture_ecr_cleaning_smoke.py
    - orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
    - orca-harness/tests/unit/test_transcript_product_lake.py
  authority: advisory implementation/code review; formal review verdict NOT_CLAIMED
  decision_criteria: YouTube packet-to-ECR traceability, honest residual visibility, Cleaning silver validation, no scope drift
  evidence_summary: <short source-backed summary>
  reviewer_verdict: NOT_CLAIMED
  finding_ids: []
  minimum_closure_conditions: []
  next_authorized_action: home model adjudicates findings before keeping any change
  non_claims:
    - not approval
    - not validation
    - not readiness
    - not patch authority
    - not live transport
    - not projection
    - not derived retrieval
    - not gold or Judgment output
```
