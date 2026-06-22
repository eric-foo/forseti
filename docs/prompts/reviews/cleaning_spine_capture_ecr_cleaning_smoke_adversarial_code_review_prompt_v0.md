# Cleaning Spine Capture/ECR/Cleaning Smoke Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for adversarial implementation/code review of the
  no-network Capture/ECR/Cleaning smoke stitcher patch on the Cleaning spine lane.
use_when:
  - Commissioning an independent reviewer to inspect the smoke-runner patch.
  - Checking the prompt source, scope, and output binding for this review.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
branch_or_commit: codex/cleaning-spine-continuation at bc950cdfeeb3a02f33bf52217d71e049aa9093f2
stale_if:
  - The smoke-runner patch target files change after this prompt is filed.
  - The worktree branch or HEAD differs from the pinned branch/head below.
  - The review-output destination already exists and the operator has not authorized a new version.
```

## Orca Prompt Preflight

- Output mode: file-write review prompt; receiver output mode is filesystem-output to `docs/review-outputs/cleaning_spine_capture_ecr_cleaning_smoke_adversarial_code_review_v0.md`.
- Template kind: review; Orca-local implementation/code-review template is unbound, so this uses the generic prompt-orchestrator review frame plus Orca overlay bindings.
- Edit permission, targets, branch: reviewer is read-only. Target worktree is `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\cleaning-spine-continuation`, branch `codex/cleaning-spine-continuation`, HEAD `bc950cdfeeb3a02f33bf52217d71e049aa9093f2`, dirty state allowed exactly as listed below.
- Reviews: findings-first. This is advisory implementation/code review unless a later Orca binding grants formal implementation-review authority. Do not emit formal PASS, readiness, mandatory remediation, or patch queue.
- Doctrine change: none intended. This prompt routes a review; it does not alter review, prompt, implementation, ECR, Cleaning, or Capture doctrine.
- Destinations: this prompt is the input artifact; the receiver writes the full report to `docs/review-outputs/cleaning_spine_capture_ecr_cleaning_smoke_adversarial_code_review_v0.md`.

## Commission

Run an adversarial implementation/code review of the no-network Capture -> ECR -> Cleaning smoke stitcher patch. This prompt was prepared after an explicit `workflow-delegated-review-patch` invocation, but the target is a multi-file implementation/code diff. Per Orca `.agents/workflow-overlay/delegated-review-patch.md`, do not force this into the single-artifact delegated review-and-patch convention. Route it through implementation/code review instead.

The review purpose is to find blocker or major correctness, scope, validation, source-boundary, or false-confidence issues in the smoke-runner patch before the home model keeps, commits, or PRs it.

## Actor And De-Correlation Receipt

- author_home_model_family: OpenAI / GPT-family Codex, recorded from the current authoring lane.
- controller_model_family: `operator_to_fill`; must be a different upstream vendor/model lineage to claim cross-vendor discovery.
- current_receiving_actor_role: controller.
- dispatch_mode: external-controller-courier.
- de_correlation_status: `operator_to_fill`; if controller model family is missing or same-vendor, return advisory findings only and do not claim cross-vendor discovery or no-new-seam.
- no runtime model recommendation is made by this prompt.

## Source-Gated Method Contract

1. REFERENCE-LOAD `workflow-code-review` and `workflow-deep-thinking` if available in your environment. Do not APPLY them yet.
2. Read the required Orca authority and target sources below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, and unavailable tools.
4. Only after source readiness, APPLY deep-thinking to frame material failure modes, then APPLY workflow-code-review to produce findings-first implementation/code review.
5. If `workflow-code-review` is unavailable, use its zero-config findings-only advisory semantics from the prompt text below, but mark strict review claims `NOT_CLAIMED`.

## Required Reads

Read these first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/safety-rules.md`
- `docs/hygiene/cleaning_spine_lane_handoff_v0.md` if present in this worktree; if absent, report it absent and continue from the prompt target plus current sources.

Then read the review target:

- `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
- `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`
- `docs/workflows/orca_repo_map_v0.md` only for the added smoke-runner route/update

Read adjacent implementation context as needed, but do not widen the review target:

- `orca-harness/cleaning/models.py`
- `orca-harness/cleaning/projection.py`
- `orca-harness/ecr/deriver.py`
- `orca-harness/source_capture/models.py`
- `orca-harness/source_capture/retail_pdp_projection.py`
- `orca-harness/source_capture/reddit_consolidation/consolidator.py`
- existing tests adjacent to the runner's dependencies

## Dirty-State Allowance

The lane is intentionally dirty. Review only the target patch unless a dirty dependency directly affects target correctness.

Observed status at prompt creation:

```text
## codex/cleaning-spine-continuation...origin/main [behind 6]
 M docs/workflows/orca_repo_map_v0.md
 M orca-harness/cleaning/models.py
 M orca-harness/tests/unit/test_cleaning_core.py
?? docs/prompts/reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_prompt_v0.md
?? docs/review-outputs/adversarial-artifact-reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_claude_cross_vendor_v0.md
?? docs/review-outputs/adversarial-artifact-reviews/cleaning_contract_to_code_obligation_comparison_adversarial_review_v0.md
?? docs/workflows/cleaning_contract_to_code_reconciliation_checklist_v0.md
?? orca-harness/runners/run_capture_ecr_cleaning_smoke.py
?? orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
```

Target patch files for this review are:

- `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
- `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`
- the smoke-runner-related edits in `docs/workflows/orca_repo_map_v0.md`

The modified `orca-harness/cleaning/models.py`, `orca-harness/tests/unit/test_cleaning_core.py`, and untracked cleaning reconciliation artifacts pre-existed this smoke-runner patch. Treat them as context only unless they invalidate the target.

## Validation Evidence To Inspect

The author reported this command passed after the patch:

```powershell
python -m pytest -p no:cacheprovider --no-header --no-summary -q tests\unit\test_capture_ecr_cleaning_smoke_runner.py tests\unit\test_cleaning_projection_integration.py tests\unit\test_cleaning_core.py tests\unit\test_ecr_identity_deriver.py tests\unit\test_ecr_inspectability_deriver.py tests\unit\test_ecr_timing_deriver.py tests\unit\test_ecr_source_visibility_deriver.py tests\unit\test_ecr_source_side_composition.py
```

Reported output:

```text
........................................................................ [ 97%]
..                                                                       [100%]
```

Also reported:

- `python runners\run_capture_ecr_cleaning_smoke.py --help` exited 0.
- `python .agents\hooks\check_repo_map_freshness.py --changed` exited 0.
- `python .agents\hooks\check_placement.py --check` exited 0 with pre-existing `.gitattributes`, `.github`, and `.githooks` placement warnings.

You may rerun read-only tests or checks if your environment permits. If you do not rerun them, report validation as author-supplied and not independently revalidated.

## Review Scope

Attack these questions:

- Does the runner truly stay no-network and consume only existing packet/projection/consolidation artifacts?
- Does it preserve raw packet anchors, projection refs, ECR refs, and packet-key coupling without fabricating success?
- Does the Reddit consolidation adapter use row-level `data-fullname` / ID anchors only when verifiable in raw HTML, and downgrade/report file-level anchors otherwise?
- Does the Retail/PDP path verify projection rows against preserved raw files and report `structure_preserved=false` without treating residuals as failure?
- Does the ECR receipt path derive all four source-side postures for every packet and avoid turning residuals into validation/readiness claims?
- Are overwrite, empty-manifest, packet mismatch, path-containment, and hash-mismatch failure modes visible?
- Do tests exercise the intended boundary without relying on live capture, network, crawler behavior, storage, API, dashboard, or Judgment semantics?
- Does the repo-map update accurately route to the new runner without overclaiming capture execution or ECR/Cleaning readiness?

## Strict-Claim Boundary

This review must not claim formal implementation-review authority, readiness, acceptance, validation, or pass/fail verdict unless Orca overlay authority is supplied separately. Use findings-only advisory review. Do not emit `patch_queue_entry`; do not edit source files; do not commit, push, PR, or run live capture.

If you find no blocker or major issue, say so and state residual risks or validation gaps. If you find an issue, findings lead the report and must include:

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

`docs/review-outputs/cleaning_spine_capture_ecr_cleaning_smoke_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by: operator_to_fill`
- `authored_by: gpt-family-codex`
- `de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback`
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
  report_path: docs/review-outputs/cleaning_spine_capture_ecr_cleaning_smoke_adversarial_code_review_v0.md
  commission: adversarial implementation/code review of no-network Capture/ECR/Cleaning smoke stitcher patch
  target:
    - orca-harness/runners/run_capture_ecr_cleaning_smoke.py
    - orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
    - docs/workflows/orca_repo_map_v0.md smoke-runner route/update
  authority: advisory implementation/code review; formal review verdict NOT_CLAIMED
  decision_criteria: smoke-runner no-network boundary, raw/projection/ECR traceability, failure visibility, test adequacy
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
    - not live capture execution
```
