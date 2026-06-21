# Cleaning Spine Periodic Audit Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for adversarial implementation/code review of the
  no-network Cleaning spine periodic audit runner patch on the Cleaning lane.
use_when:
  - Commissioning an independent reviewer to inspect the periodic audit runner patch.
  - Checking the prompt source, scope, and output binding for this review.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
branch_or_commit: codex/cleaning-spine-continuation at ebd85d11
stale_if:
  - The periodic-audit patch target files change after this prompt is filed.
  - The worktree branch or HEAD differs from the pinned branch/head below.
  - The review-output destination already exists and the operator has not authorized a new version.
```

## Orca Prompt Preflight

- Output mode: file-write review prompt; receiver output mode is filesystem-output to `docs/review-outputs/cleaning_spine_periodic_audit_adversarial_code_review_v0.md`.
- Template kind: review; Orca-local implementation/code-review template is unbound, so this uses the generic prompt-orchestrator review frame plus Orca overlay bindings.
- Edit permission, targets, branch: reviewer is read-only. Target worktree is `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\cleaning-spine-continuation`, branch `codex/cleaning-spine-continuation`, HEAD `ebd85d11`, dirty state allowed exactly as listed below.
- Reviews: findings-first. This is advisory implementation/code review unless a later Orca binding grants formal implementation-review authority. Do not emit formal PASS, readiness, mandatory remediation, or patch queue.
- Doctrine change: none intended. This prompt routes a review; it does not alter review, prompt, implementation, ECR, Cleaning, Capture, scheduler, or Data Lake doctrine.
- Destinations: this prompt is the input artifact; the receiver writes the full report to `docs/review-outputs/cleaning_spine_periodic_audit_adversarial_code_review_v0.md`.

## Commission

Run an adversarial implementation/code review of the no-network Cleaning spine periodic audit patch. This prompt was prepared after explicit `workflow-goal-framing`, `workflow-assumption-gate`, `fused`, and `workflow-delegated-review-patch` user direction. The target is a multi-file implementation/code diff, so per Orca `.agents/workflow-overlay/delegated-review-patch.md`, do not force this into the single-artifact delegated review-and-patch convention. Route it through implementation/code review instead.

The review purpose is to find blocker or major correctness, scope, validation, source-boundary, or false-confidence issues before the home model keeps, commits, pushes, or PRs the periodic audit patch.

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
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`
- `docs/hygiene/cleaning_spine_lane_handoff_v0.md`
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
- `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`

Then read the review target:

- `orca-harness/runners/run_cleaning_spine_periodic_audit.py`
- `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`
- `docs/workflows/orca_repo_map_v0.md` only for the added periodic-audit runner route/update

Read adjacent implementation context as needed, but do not widen the review target:

- `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
- `orca-harness/cleaning/models.py`
- `orca-harness/ecr/deriver.py`
- `orca-harness/source_capture/models.py`
- `orca-harness/source_capture/ig_projection.py`
- `orca-harness/source_capture/retail_pdp_projection.py`
- `orca-harness/source_capture/reddit_consolidation/consolidator.py`
- existing tests adjacent to the runner's dependencies

## Dirty-State Allowance

The lane is intentionally dirty. Review only the target patch unless a dirty dependency directly affects target correctness.

Observed status at prompt creation:

```text
## codex/cleaning-spine-continuation...origin/codex/cleaning-spine-continuation
 M docs/workflows/orca_repo_map_v0.md
 M orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
?? orca-harness/runners/run_cleaning_spine_periodic_audit.py
?? docs/prompts/reviews/cleaning_spine_periodic_audit_adversarial_code_review_prompt_v0.md
```

Target patch files for this review are:

- `orca-harness/runners/run_cleaning_spine_periodic_audit.py`
- `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`
- the periodic-audit-related edit in `docs/workflows/orca_repo_map_v0.md`

The prompt file itself is not a code target. Treat it only as commission metadata unless it is internally contradictory enough to block review.

## Validation Evidence To Inspect

The author observed this command passed after the patch:

```powershell
python -B -m pytest -p no:cacheprovider --no-header --no-summary -q tests\unit\test_capture_ecr_cleaning_smoke_runner.py tests\unit\test_cleaning_core.py tests\unit\test_cleaning_projection_integration.py tests\unit\test_source_capture_ig_projection.py tests\unit\test_retail_pdp_projection.py tests\unit\test_reddit_consolidation.py
```

Observed output:

```text
........................................................................ [ 84%]
.............                                                            [100%]
```

Earlier sandboxed pytest failed with `WinError 5` creating the project `_scratch` tmp directory; the successful run was rerun with filesystem escalation and `python -B` to avoid bytecode writes. A direct `py_compile` attempt also hit a local `__pycache__` permission issue. Treat those as environment notes, not validation failures, unless your rerun shows a real code error.

You may rerun read-only tests or checks if your environment permits. If you do not rerun them, report validation as author-supplied and not independently revalidated.

## Review Scope

Attack these questions:

- Does `run_cleaning_spine_periodic_audit.py` truly stay no-network and consume only frozen smoke manifests plus existing packet/projection/consolidation/ECR/Cleaning artifacts?
- Does the audit classify failures into the intended breakpoints: capture preflight, Lane A existing-package checks, Lane B projection/consolidation rebuild, and Lane B Cleaning/ECR rebuild?
- Does capture preflight catch packet manifest, preserved-file path containment, missing file, and hash mismatch failures without masking downstream failures as success?
- Does Lane A validate CleaningPacket shape, ECR receipt coupling, raw packet/file/hash anchors, JSON/text/html/script anchor specificity, and absence of Judgment vocabulary without overclaiming live E2E readiness?
- Does Lane B projection rebuild compare stable signatures for Retail/PDP, Instagram, and Reddit without treating expected residuals as false failures?
- Does Lane B Cleaning rebuild compare stable Cleaning and ECR signatures against Lane A without fabricating pass when Lane A artifacts are malformed?
- Is the cross-slice IG raw-anchor behavior handled correctly: packet/file/hash/json-pointer must resolve, but a metric row may anchor to profile momentum JSON while the observation slice is a post slice.
- Are output overwrite guards, report shape, Markdown report, CLI exit semantics, and non-claims coherent for a future scheduler to call without becoming the scheduler now?
- Do tests exercise pass, projection drift, Cleaning package drift, and capture packet hash mismatch without network, live capture, crawler behavior, storage, API, dashboard, product proof, or Judgment semantics?
- Does the repo-map update accurately route to the new runner without overclaiming scheduling, live capture, Data Lake readiness, product proof, or full e2e readiness?

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

`docs/review-outputs/cleaning_spine_periodic_audit_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by: operator_to_fill`
- `authored_by: gpt-family-codex`
- `de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback`
- `same_vendor_rationale:` required if `de_correlation_bar` is `same_vendor_sanity`
- source-read ledger
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`
- findings first
- open questions and residual risk
- validation rerun status
- strict-only blockers and non-claims
- `DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL` courier block

Do not write outside that report path. If the report path already exists, stop and report `BLOCKED_OUTPUT_DESTINATION_COLLISION` unless the operator explicitly provides a new output path.

## Delegated Code Review Return Courier

Append this block at the end of the report:

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

Include:
- original commission or review target
- implementation context, diff, and reviewed files
- findings and implementation evidence
- proposed patch, diff, or exact requested edits, if authorized
- citations
- reviewer verdict
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```
