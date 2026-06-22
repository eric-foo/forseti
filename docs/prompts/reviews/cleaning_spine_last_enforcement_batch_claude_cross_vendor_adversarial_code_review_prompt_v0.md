# Cleaning Spine Last Enforcement Batch Claude Cross-Vendor Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for a de-correlated cross-vendor adversarial
  implementation/code review of the latest Cleaning spine enforcement batch:
  raw-pull triggers, transform original-value provenance, no-network audit guard,
  and source-family audit adapter coverage.
use_when:
  - Commissioning a different-vendor reviewer to inspect the last Cleaning spine hardening batch.
  - Checking the prompt source, scope, and output binding for this delegated code review.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
implementation_under_review: 0d2f3be955a469f7bfae1727e551f771e5e771be..aef50b05efdb57fbe57a71433d7e2f30db861b4e
branch_or_commit: codex/cleaning-spine-continuation at aef50b05efdb57fbe57a71433d7e2f30db861b4e
prompt_carrier_note: >
  This prompt may be committed after the implementation commits. The implementation
  target under review ends at aef50b05efdb57fbe57a71433d7e2f30db861b4e; prompt-only
  carrier commits do not change the implementation target unless they modify the
  named target files.
stale_if:
  - Any named implementation target file changes after aef50b05efdb57fbe57a71433d7e2f30db861b4e and before review.
  - The review-output destination already exists and the operator has not authorized a new version.
  - The receiving actor is not a different-vendor controller but still claims cross_vendor_discovery.
```

## Orca Prompt Preflight

- preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` v0 - constants bound; deltas stated here.
- Output mode: file-write review prompt; receiver output mode is filesystem-output to `docs/review-outputs/cleaning_spine_last_enforcement_batch_claude_cross_vendor_adversarial_code_review_v0.md`.
- Template kind: review; Orca-local implementation/code-review template is unbound, so this uses the generic prompt-orchestrator review frame plus Orca overlay bindings.
- Edit permission, targets, branch: reviewer is read-only. Target worktree is `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\cleaning-spine-continuation`, branch `codex/cleaning-spine-continuation`, implementation range `0d2f3be955a469f7bfae1727e551f771be..aef50b05efdb57fbe57a71433d7e2f30db861b4e`, dirty state allowed only for this prompt artifact or later prompt-carrier commits that do not touch target files.
- Reviews: findings-first. This is advisory implementation/code review unless a later Orca binding grants formal implementation-review authority. Do not emit formal PASS, readiness, mandatory remediation, or patch queue.
- Doctrine change: none intended. This prompt routes a review; it does not alter review, prompt, implementation, ECR, Cleaning, Capture, scheduler, Data Lake, product-proof, or Judgment doctrine.
- Destinations: this prompt is the input artifact; the receiver writes the full report to `docs/review-outputs/cleaning_spine_last_enforcement_batch_claude_cross_vendor_adversarial_code_review_v0.md`.
- thread_operating_target_continuity: carried_forward: no; reason: no_visible_active_target.

## What This Is For

Goal: determine whether the latest Cleaning spine hardening batch actually makes the no-network periodic audit catch important Projection and Cleaning breakages without overclaiming live capture-to-cleaning readiness.

Done looks like: a de-correlated reviewer can state, with file/line evidence, whether each intended enforcement is closed, partially closed, not closed, or not assessed, and whether any blocker/major regression remains in the touched scope.

## Commission

Run an adversarial implementation/code review of the Cleaning spine hardening batch ending at commit `aef50b05efdb57fbe57a71433d7e2f30db861b4e`. This is a cross-vendor controller prompt intended for a reviewer whose vendor/model lineage differs from the OpenAI/GPT-family author. If the receiving reviewer is Anthropic/Claude-family, record that as the controller family. That family label is a who-constraint for de-correlation, not a runtime-model recommendation, ranking, or selection rule.

This request was triggered through `workflow-delegated-review-patch`, but the target is a multi-file implementation/code diff. Per Orca `.agents/workflow-overlay/delegated-review-patch.md`, do not force this into the single-artifact delegated review-and-patch convention. Route it through implementation/code review instead. The reviewer is read-only and must not patch source files.

Review purpose:

1. Independently attack the latest enforcement batch for blocker/major correctness, scope, validation, source-boundary, or false-confidence issues.
2. Verify whether the four intended enforcement moves are actually enforced by code and tests:
   - E-04 failed/blocked capture handles must carry a raw-pull trigger.
   - E-05 Cleaning transform `original_value` must resolve to projection source-visible values or raw bytes, not arbitrary invented text.
   - E-06 periodic audit execution must be guarded against network access.
   - E-07 every supported source family in the periodic audit must declare row-kind and anchor-kind coverage, and the audit must flag unsupported rows/anchors.
3. Scan only the touched implementation scope for patch-caused or newly visible blocker/major issues. Minor findings are allowed, but do not widen into unrelated Cleaning, Capture, Data Lake, scheduler, product-proof, or Judgment review.

## Actor And De-Correlation Receipt

- author_home_model_family: OpenAI / GPT-family Codex, recorded from the authoring lane.
- controller_model_family: operator_to_fill; must be a different vendor/model lineage from OpenAI/GPT-family to claim `cross_vendor_discovery`.
- current_receiving_actor_role: controller.
- dispatch_mode: external-controller-courier.
- de_correlation_status: `cross_vendor_discovery` only if the reviewer vendor/model lineage differs from OpenAI/GPT-family; otherwise set `same_vendor_sanity` or `self_fallback` and do not claim cross-vendor discovery or no-new-seam.
- no runtime model recommendation is made by this prompt.

## Source-Gated Method Contract

1. REFERENCE-LOAD these method instructions if available in your environment. Do not APPLY them yet:
   - `workflow-deep-thinking`
   - `workflow-code-review`
   - `workflow-delegated-review-patch` only for the commission and return-courier contract.
2. Read the required Orca authority and target sources below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, unavailable tools, and any target-file drift.
4. Only after source readiness, APPLY deep-thinking to frame material failure modes, then APPLY workflow-code-review to produce findings-first implementation/code review.
5. If `workflow-code-review` is unavailable, use its zero-config findings-only advisory semantics from this prompt text, but mark strict review claims `NOT_CLAIMED`.

## Required Reads

Read these authority and boundary files first:

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
- `docs/workflows/ecr_spine_submap_v0.md`

Then read the review target:

- `orca-harness/runners/run_cleaning_spine_periodic_audit.py`
- `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`
- `git diff 0d2f3be955a469f7bfae1727e551f771e5e771be..aef50b05efdb57fbe57a71433d7e2f30db861b4e -- orca-harness/runners/run_cleaning_spine_periodic_audit.py orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`

Read adjacent implementation context as needed, but do not widen the review target:

- `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
- `orca-harness/cleaning/models.py`
- `orca-harness/ecr/models.py`
- `orca-harness/ecr/deriver.py`
- `orca-harness/source_capture/models.py`
- `orca-harness/source_capture/ig_projection.py`
- `orca-harness/source_capture/retail_pdp_projection.py`
- `orca-harness/source_capture/reddit_consolidation/consolidator.py`
- adjacent tests that define expected projection, Cleaning, ECR, or smoke-runner behavior.

## Target Diff And Dirty-State Allowance

Implementation target range:

```text
0d2f3be955a469f7bfae1727e551f771e5e771be..aef50b05efdb57fbe57a71433d7e2f30db861b4e
```

Target commits:

```text
406883d1b28797f3f53593b8877e5cbf3d727e36 Enforce raw-pull triggers for failed capture handles
9bd0a0405fcc6c2ac43c2642ab106fcfa95510e4 Enforce transform original-value provenance
45d9146d84ca44683e5b0b7ed878dc600b91ed76 Guard periodic audit against network access
aef50b05efdb57fbe57a71433d7e2f30db861b4e Enforce source-family audit adapter coverage
```

Observed target files in that range:

```text
orca-harness/runners/run_cleaning_spine_periodic_audit.py
orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
```

Observed diff size:

```text
2 files changed, 640 insertions(+), 16 deletions(-)
```

Per-file numstat:

```text
368  16  orca-harness/runners/run_cleaning_spine_periodic_audit.py
272   0  orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
```

If the branch contains a later prompt-only commit, verify whether the two target files above still match `aef50b05efdb57fbe57a71433d7e2f30db861b4e`. If they changed, report `SOURCE_CONTEXT_INCOMPLETE` or review the newer target only if the operator explicitly authorizes that retarget.

## Validation Evidence To Inspect

The author observed these new tests pass after the final source-family adapter patch:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1; python -B -m pytest -p no:cacheprovider --tb=short tests\unit\test_capture_ecr_cleaning_smoke_runner.py::test_periodic_audit_supported_source_families_have_adapter_coverage tests\unit\test_capture_ecr_cleaning_smoke_runner.py::test_periodic_audit_flags_projection_row_kind_outside_source_family_adapter tests\unit\test_capture_ecr_cleaning_smoke_runner.py::test_periodic_audit_flags_anchor_kind_outside_source_family_adapter -q
```

Observed output:

```text
...                                                                      [100%]
```

The author also observed the adjacent no-network Cleaning/ECR/projection suite pass after the final patch:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1; python -B -m pytest -p no:cacheprovider --tb=short tests\unit\test_cleaning_core.py tests\unit\test_cleaning_projection_integration.py tests\unit\test_ecr_models.py tests\unit\test_ecr_identity_models.py tests\unit\test_ecr_inspectability_models.py tests\unit\test_ecr_timing_deriver.py tests\unit\test_ecr_source_visibility_models.py tests\unit\test_ecr_source_side_composition.py tests\unit\test_reddit_consolidation.py tests\unit\test_capture_ecr_cleaning_smoke_runner.py -q
```

Observed output:

```text
........................................................................ [ 47%]
........................................................................ [ 94%]
.........                                                                [100%]
```

Also observed after the final patch:

```powershell
git diff --check
$env:PYTHONDONTWRITEBYTECODE=1; python -B runners\run_cleaning_spine_periodic_audit.py --help
```

`git diff --check` exited 0 with Git CRLF normalization warnings only. The audit CLI help exited 0 and printed usage for `--audit-manifest` and `--output-dir`.

Environment notes:

- A restricted-sandbox pytest attempt failed at test setup with `_scratch` write `PermissionError`; the same targeted suite passed when rerun with workspace-local write permission. Do not treat the restricted-sandbox error as implementation failure unless your environment reproduces a code error independent of sandbox write ACLs.
- Use `python -B` for no-bytecode validation if rerunning tests.
- Do not run live capture, network capture, crawler behavior, scheduler behavior, API/dashboard code, storage/Data Lake operations, product-proof checks, or Judgment readiness checks.
- If you do not rerun validation, report validation as author-supplied and not independently revalidated.

## Review Scope

Attack these questions:

### E-04 Raw-pull triggers for failed or blocked capture handles

- Does `_verify_failed_capture_handle_raw_pull_trigger()` actually catch Cleaning handles whose warnings or residuals indicate failed/blocked capture posture but whose `raw_pull_triggers` are empty?
- Are the trigger tokens specific enough to catch `capture_validity_not_supported`, blocked/failed capture, and source structure failure without catching unrelated benign Cleaning residuals?
- Does the finding severity affect the periodic audit status rather than appearing as a non-blocking note while the audit reports clean?
- Do tests build a failed retail capture shape and prove that stripping raw-pull triggers creates a finding?

### E-05 Transform original-value provenance

- Does `_verify_cleaning_transform_original_value()` prove that a Cleaning transform ledger `original_value` came from the referenced projection row's `source_visible_fields` or from raw preserved bytes?
- Does the check avoid accepting arbitrary capture metadata, invented strings, empty strings, or values from an unrelated handle/packet/row?
- Are nested dict/list/bool/number values in `source_visible_fields` handled deliberately, without introducing broad substring false positives that make arbitrary values look sourced?
- Does this enforcement preserve the Cleaning boundary: no credibility, salience, independence, demand, actionability, product-proof, or Judgment vocabulary introduced as a Cleaning decision?
- Do tests cover both a valid projection-sourced transform value and an invented `original_value` that must fail?

### E-06 No-network guard around periodic audit execution

- Does `test_periodic_audit_execution_does_not_open_network_socket()` cover the actual periodic audit execution path, including Lane B projection and Cleaning rebuilds?
- Is the socket monkeypatch broad enough for the runner's known implementation path, and are any subprocess, browser, request, or network-capable helpers still reachable from this audit path?
- Does the audit remain bounded to frozen packet/projection/consolidation/ECR/Cleaning artifacts rather than running capture, discovery, crawler/scraper behavior, scheduler behavior, API/dashboard code, storage, product-proof, or Judgment readiness?
- Does the no-network test avoid false confidence by clearly covering only the periodic audit runner, not all future automation or live capture code?

### E-07 Source-family adapter coverage

- Does `_validate_source_family_adapter_contract()` require every supported source family to declare non-empty row-kind and anchor-kind coverage, and require anchor kinds to have validators?
- Does `_projection_rows_by_id()` flag unsupported projection row kinds for the source family while preserving enough row index information for other findings?
- Does `_verify_source_family_anchor_adapter_coverage()` flag valid core anchor kinds that are not allowed for the Cleaning handle's source family, especially Instagram `text_pattern` where only JSON pointer anchors are expected?
- Is the mapping from Cleaning `source_family` values (`retail_pdp`, `reddit_thread`, `instagram_creator`) to audit source types complete and correctly failure-visible for unknown families?
- Do the tests prove contract coverage, unsupported row-kind finding, and unsupported anchor-kind finding without relying only on model validation rejecting impossible rows earlier?

### Cross-cutting false-pass checks

- Can any new enforcement fail silently because a malformed CleaningPacket, projection artifact, ECR receipt, or packet index causes an earlier exception that masks the specific finding and still allows a clean audit status?
- Does the audit distinguish failed/blocked capture handles at the handle level, or does failure context remain only in summary side channels?
- Are file/hash/raw anchors still verified before source-visible provenance or anchor-specific checks are trusted?
- Does any enforcement make known residuals invisible, especially file-level Reddit anchor downgrades or ambiguous text-pattern anchors?
- Do the changes remain lane-correct: Cleaning may preserve and normalize mechanical references, but must not decide credibility, demand, salience, independence, actionability, or Judgment readiness?

## Intended Enforcement Closure Check

Treat these enforcement goals as claims to verify, not accepted truth:

- E-04 raw-pull trigger: failed/blocked capture posture on a Cleaning handle requires a non-empty raw-pull trigger.
- E-05 transform provenance: non-empty transform `original_value` must resolve to projection source-visible values or raw bytes.
- E-06 no-network guard: the periodic audit test fails if the runner attempts to open a network socket.
- E-07 source-family adapter coverage: supported source families declare row kinds and anchor kinds, and unsupported rows/anchors become findings.

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

`docs/review-outputs/cleaning_spine_last_enforcement_batch_claude_cross_vendor_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by: operator_to_fill_reviewer_identity`
- `authored_by: gpt-family-codex`
- `de_correlation_bar: cross_vendor_discovery` only if the reviewer vendor/model lineage differs from OpenAI/GPT-family; otherwise use `same_vendor_sanity` or `self_fallback`
- `same_vendor_rationale:` required if `de_correlation_bar` is `same_vendor_sanity`
- source-read ledger
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`
- findings first
- intended enforcement closure table for E-04/E-05/E-06/E-07
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
- intended enforcement closure statuses for E-04/E-05/E-06/E-07
- proposed patch, diff, or exact requested edits, if authorized
- citations
- reviewer verdict
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```
