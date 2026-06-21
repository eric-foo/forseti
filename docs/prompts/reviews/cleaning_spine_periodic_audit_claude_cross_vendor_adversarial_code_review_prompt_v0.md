# Cleaning Spine Periodic Audit Claude Cross-Vendor Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for Anthropic/Claude-family cross-vendor adversarial
  implementation/code review of the no-network Cleaning spine periodic audit
  runner patch after same-vendor review findings were adjudicated and patched.
use_when:
  - Commissioning Claude to inspect the final periodic-audit runner patch.
  - Checking the prompt source, scope, and output binding for this cross-vendor review.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
implementation_under_review: codex/cleaning-spine-continuation at 6eb99a0f
prompt_carrier_note: >
  This prompt may be committed after the implementation commit. The implementation
  target under review is commit 6eb99a0f; prompt-only carrier commits do not change
  the implementation target unless they modify the named target files.
stale_if:
  - Any named implementation target file changes after commit 6eb99a0f and before review.
  - The review-output destination already exists and the operator has not authorized a new version.
  - The receiving actor is not Anthropic/Claude-family but still claims cross_vendor_discovery.
```

## Orca Prompt Preflight

- Output mode: file-write review prompt; receiver output mode is filesystem-output to `docs/review-outputs/cleaning_spine_periodic_audit_claude_cross_vendor_adversarial_code_review_v0.md`.
- Template kind: review; Orca-local implementation/code-review template is unbound, so this uses the generic prompt-orchestrator review frame plus Orca overlay bindings.
- Edit permission, targets, branch: reviewer is read-only. Target worktree is `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\cleaning-spine-continuation`, branch `codex/cleaning-spine-continuation`, implementation commit `6eb99a0f`, dirty state allowed only for this prompt artifact or a later prompt-carrier commit that does not touch target files.
- Reviews: findings-first. This is advisory implementation/code review unless a later Orca binding grants formal implementation-review authority. Do not emit formal PASS, readiness, mandatory remediation, or patch queue.
- Doctrine change: none intended. This prompt routes a review; it does not alter review, prompt, implementation, ECR, Cleaning, Capture, scheduler, or Data Lake doctrine.
- Destinations: this prompt is the input artifact; the receiver writes the full report to `docs/review-outputs/cleaning_spine_periodic_audit_claude_cross_vendor_adversarial_code_review_v0.md`.

## Commission

Run an adversarial implementation/code review of the no-network Cleaning spine periodic audit patch at commit `6eb99a0f`. This is a cross-vendor controller prompt intended for an Anthropic/Claude-family reviewer. That family label is a who-constraint for de-correlation from the OpenAI/GPT-family author, not a runtime-model recommendation, rank, or selection rule.

This prompt follows `workflow-delegated-review-patch` route-out, but the target is a multi-file implementation/code diff. Per Orca `.agents/workflow-overlay/delegated-review-patch.md`, do not force this into the single-artifact delegated review-and-patch convention. Route it through implementation/code review instead. The reviewer is read-only and must not patch source files.

Review purpose:

1. Independently attack the final periodic audit implementation for blocker/major correctness, scope, validation, source-boundary, or false-confidence issues.
2. Verify whether the prior same-vendor findings were actually closed by the final implementation: F-01 shallow projection signatures, F-02 Lane A smoke findings not status-affecting, and F-03 stale rebuild output collision risk.
3. Scan only the touched implementation scope for patch-caused or newly visible blocker/major issues. Minor findings are allowed, but do not widen into unrelated structural review.

## Actor And De-Correlation Receipt

- author_home_model_family: OpenAI / GPT-family Codex, recorded from the authoring lane.
- controller_model_family: Anthropic / Claude-family, if and only if the receiving reviewer is actually Claude-family.
- current_receiving_actor_role: controller.
- dispatch_mode: external-controller-courier.
- de_correlation_status: `cross_vendor_discovery` only if the reviewer is Anthropic/Claude-family and the author family remains OpenAI/GPT-family; otherwise set `same_vendor_sanity` or `self_fallback` and do not claim cross-vendor discovery or no-new-seam.
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
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
- `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`

Then read the review target:

- `orca-harness/runners/run_cleaning_spine_periodic_audit.py`
- `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`
- `docs/workflows/orca_repo_map_v0.md` only for the periodic-audit runner route/update

Read these review-context artifacts without inheriting them as truth:

- `docs/review-outputs/cleaning_spine_periodic_audit_adversarial_code_review_v0.md` — same-vendor sanity review that found F-01, F-02, F-03 before the final patch.
- `docs/prompts/reviews/cleaning_spine_periodic_audit_adversarial_code_review_prompt_v0.md` — prior same-vendor prompt, now stale for implementation target but useful for route history.

Read adjacent implementation context as needed, but do not widen the review target:

- `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
- `orca-harness/cleaning/models.py`
- `orca-harness/ecr/deriver.py`
- `orca-harness/source_capture/models.py`
- `orca-harness/source_capture/ig_projection.py`
- `orca-harness/source_capture/retail_pdp_projection.py`
- `orca-harness/source_capture/reddit_consolidation/consolidator.py`
- adjacent tests that define expected projection, Cleaning, ECR, or smoke-runner behavior

If `docs/hygiene/cleaning_spine_lane_handoff_v0.md` exists in your target worktree, read it as orientation. If absent, report it absent and continue from the prompt target plus current sources; do not block solely on that absence.

## Target Diff And Dirty-State Allowance

Implementation target commit:

```text
6eb99a0f Add cleaning spine periodic audit runner
```

Observed implementation target files in that commit:

```text
A docs/prompts/reviews/cleaning_spine_periodic_audit_adversarial_code_review_prompt_v0.md
A docs/review-outputs/cleaning_spine_periodic_audit_adversarial_code_review_v0.md
M docs/workflows/orca_repo_map_v0.md
A orca-harness/runners/run_cleaning_spine_periodic_audit.py
M orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
```

Target files for this Claude review are:

- `orca-harness/runners/run_cleaning_spine_periodic_audit.py`
- `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`
- the periodic-audit-related edit in `docs/workflows/orca_repo_map_v0.md`

The same-vendor prompt/report files are review context only. This Claude prompt file is not a code target.

If the branch contains a later prompt-only commit, verify whether the three target files above still match commit `6eb99a0f`. If they changed, report `SOURCE_CONTEXT_INCOMPLETE` or review the newer target only if the operator explicitly authorizes that retarget.

## Validation Evidence To Inspect

The author observed this command passed after patching the same-vendor findings:

```powershell
python -B -m pytest -p no:cacheprovider --no-header --no-summary -q tests\unit\test_capture_ecr_cleaning_smoke_runner.py tests\unit\test_cleaning_core.py tests\unit\test_cleaning_projection_integration.py tests\unit\test_source_capture_ig_projection.py tests\unit\test_retail_pdp_projection.py tests\unit\test_reddit_consolidation.py
```

Observed output:

```text
........................................................................ [ 81%]
................                                                         [100%]
```

Also observed:

```powershell
python -B runners\run_cleaning_spine_periodic_audit.py --help
```

exited 0 and printed the CLI help for `--audit-manifest` and `--output-dir`.

Environment notes:

- A direct `py_compile` attempt hit local `__pycache__` permission errors. Do not treat that as implementation failure unless your environment reproduces a code error independent of bytecode writes.
- Use `python -B` for no-bytecode validation if rerunning tests.
- Do not run live capture, network capture, crawler behavior, scheduler behavior, API/dashboard code, storage/Data Lake operations, product-proof checks, or Judgment readiness checks.

You may rerun no-network tests if your environment permits. If you do not rerun them, report validation as author-supplied and not independently revalidated.

## Review Scope

Attack these questions:

- Does `run_cleaning_spine_periodic_audit.py` truly stay no-network and consume only frozen smoke manifests plus existing packet/projection/consolidation/ECR/Cleaning artifacts?
- Does the audit classify failures into the intended breakpoints: capture preflight, Lane A existing-package checks, Lane B projection/consolidation rebuild, and Lane B Cleaning/ECR rebuild?
- Does capture preflight catch packet manifest, preserved-file path containment, missing file, and hash mismatch failures without masking downstream failures as success?
- Does Lane A validate CleaningPacket shape, ECR receipt coupling, raw packet/file/hash anchors, JSON/text/html/script anchor specificity, and absence of Judgment vocabulary without overclaiming live E2E readiness?
- Does Lane A now surface smoke-summary findings as audit findings so a blocked capture, unverified row anchor, or non-preserved structure cannot produce a clean pass?
- Does Lane B projection rebuild now compare stable signatures that include source-visible row payloads, binding/provenance fields, and Reddit post/comment payloads while excluding only intentionally volatile fields?
- Does Lane B Cleaning rebuild compare stable Cleaning and ECR signatures against Lane A without fabricating pass when Lane A artifacts are malformed?
- Is the cross-slice IG raw-anchor behavior handled correctly: packet/file/hash/json-pointer must resolve, but a metric row may anchor to profile momentum JSON while the observation slice is a post slice.
- Are output overwrite guards coherent for a future scheduler caller, including stale `lane_b_projection_rebuild` and `lane_b_cleaning_rebuild` directories?
- Do tests exercise pass, projection residual drift, projection source-visible field drift, Cleaning package drift, capture packet hash mismatch, Lane A smoke-summary finding promotion, and stale rebuild directory refusal without network or live capture?
- Does the repo-map update accurately route to the new runner without overclaiming scheduling, live capture, Data Lake readiness, product proof, or full e2e readiness?

## Prior Findings Closure Check

Treat these prior findings as claims to verify, not accepted truth:

- F-01: Projection breakpoint comparison was too shallow to catch source-visible row corruption.
- F-02: Existing smoke findings were counted but did not affect audit status.
- F-03: Output collision guard checked report files but not rebuild subdirectories.

For each, report one of:

- `closed`: implementation and tests now cover the failure mode.
- `partially_closed`: some protection exists but a material variant remains.
- `not_closed`: the original failure mode remains.
- `not_assessed`: source or environment prevented assessment.

If `partially_closed` or `not_closed`, include evidence and a minimum closure condition.

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

`docs/review-outputs/cleaning_spine_periodic_audit_claude_cross_vendor_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by: operator_to_fill_claude_identity`
- `authored_by: gpt-family-codex`
- `de_correlation_bar: cross_vendor_discovery` only if the reviewer is Anthropic/Claude-family; otherwise use `same_vendor_sanity` or `self_fallback`
- `same_vendor_rationale:` required if `de_correlation_bar` is `same_vendor_sanity`
- source-read ledger
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`
- findings first
- prior findings closure table for F-01/F-02/F-03
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
- prior finding closure statuses for F-01/F-02/F-03
- proposed patch, diff, or exact requested edits, if authorized
- citations
- reviewer verdict
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```
