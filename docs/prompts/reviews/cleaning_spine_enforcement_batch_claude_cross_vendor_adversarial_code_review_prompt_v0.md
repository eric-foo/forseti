# Cleaning Spine Enforcement Batch Claude Cross-Vendor Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Filed route-out prompt for Anthropic/Claude-family cross-vendor adversarial
  implementation/code review of the Cleaning spine enforcement batch covering
  projection row-ref resolution, ambiguous text-anchor detection, and typed ECR
  smoke receipts.
use_when:
  - Commissioning Claude to inspect the committed Cleaning spine enforcement batch.
  - Checking the prompt source, scope, and output binding for this cross-vendor review.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
implementation_under_review: 0ad2292c4d13e76597c5191d9157503c780a5145..db0bcdfb6d9279f53f49195fbbea2d9572bc564a
prompt_carrier_note: >
  This prompt may be committed after the implementation commits. The implementation
  target under review ends at db0bcdfb6d9279f53f49195fbbea2d9572bc564a; prompt-only
  carrier commits do not change the implementation target unless they modify the
  named target files.
stale_if:
  - Any named implementation target file changes after db0bcdfb6d9279f53f49195fbbea2d9572bc564a and before review.
  - The review-output destination already exists and the operator has not authorized a new version.
  - The receiving actor is not Anthropic/Claude-family but still claims cross_vendor_discovery.
```

## Orca Prompt Preflight

- Output mode: file-write review prompt; receiver output mode is filesystem-output to `docs/review-outputs/cleaning_spine_enforcement_batch_claude_cross_vendor_adversarial_code_review_v0.md`.
- Template kind: review; Orca-local implementation/code-review template is unbound, so this uses the generic prompt-orchestrator review frame plus Orca overlay bindings.
- Edit permission, targets, branch: reviewer is read-only. Target worktree is `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\cleaning-spine-continuation`, branch `codex/cleaning-spine-continuation`, implementation range `0ad2292c4d13e76597c5191d9157503c780a5145..db0bcdfb6d9279f53f49195fbbea2d9572bc564a`, dirty state allowed only for this prompt artifact or later prompt-carrier commits that do not touch target files.
- Reviews: findings-first. This is advisory implementation/code review unless a later Orca binding grants formal implementation-review authority. Do not emit formal PASS, readiness, mandatory remediation, or patch queue.
- Doctrine change: none intended. This prompt routes a review; it does not alter review, prompt, implementation, ECR, Cleaning, Capture, scheduler, Data Lake, or Judgment doctrine.
- Destinations: this prompt is the input artifact; the receiver writes the full report to `docs/review-outputs/cleaning_spine_enforcement_batch_claude_cross_vendor_adversarial_code_review_v0.md`.

## Commission

Run an adversarial implementation/code review of the Cleaning spine enforcement batch ending at commit `db0bcdfb6d9279f53f49195fbbea2d9572bc564a`. This is a cross-vendor controller prompt intended for an Anthropic/Claude-family reviewer. That family label is a who-constraint for de-correlation from the OpenAI/GPT-family author, not a runtime-model recommendation, rank, or selection rule.

This prompt follows `workflow-delegated-review-patch` route-out, but the target is a multi-file implementation/code diff. Per Orca `.agents/workflow-overlay/delegated-review-patch.md`, do not force this into the single-artifact delegated review-and-patch convention. Route it through implementation/code review instead. The reviewer is read-only and must not patch source files.

Review purpose:

1. Independently attack the enforcement batch for blocker/major correctness, scope, validation, source-boundary, or false-confidence issues.
2. Verify whether the three intended enforcement moves are actually enforced by code and tests:
   - E-01 projection refs: every Cleaning `projection_ref.row_id` must resolve inside the named projection artifact.
   - E-02 ambiguous anchors: repeated raw `text_pattern` anchors must be detected and surfaced instead of silently implying precise traceability.
   - E-03 typed ECR receipts: smoke/audit ECR receipt artifacts must be schema-validated instead of trusted as loose dicts.
3. Scan only the touched implementation scope for patch-caused or newly visible blocker/major issues. Minor findings are allowed, but do not widen into unrelated Cleaning, Capture, Data Lake, scheduler, product-proof, or Judgment review.

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
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, unavailable tools, and any target-file drift.
4. Only after source readiness, APPLY deep-thinking to frame material failure modes, then APPLY workflow-code-review to produce findings-first implementation/code review.
5. If `workflow-code-review` is unavailable, use its zero-config findings-only advisory semantics from the prompt text below, but mark strict review claims `NOT_CLAIMED`.

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
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md`
- `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`
- `orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `orca/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md`
- `docs/workflows/ecr_spine_submap_v0.md`

Then read the review target:

- `orca-harness/ecr/__init__.py`
- `orca-harness/ecr/models.py`
- `orca-harness/runners/run_capture_ecr_cleaning_smoke.py`
- `orca-harness/runners/run_cleaning_spine_periodic_audit.py`
- `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py`
- `orca-harness/tests/unit/test_ecr_models.py`

Read adjacent implementation context as needed, but do not widen the review target:

- `orca-harness/cleaning/models.py`
- `orca-harness/ecr/deriver.py`
- `orca-harness/source_capture/models.py`
- `orca-harness/source_capture/ig_projection.py`
- `orca-harness/source_capture/retail_pdp_projection.py`
- `orca-harness/source_capture/reddit_consolidation/consolidator.py`
- adjacent tests that define expected projection, Cleaning, ECR, or smoke-runner behavior

If `docs/hygiene/cleaning_spine_lane_handoff_v0.md` exists in your target worktree, read it as orientation. If absent, report it absent and continue from the prompt target plus current sources; do not block solely on that absence.

## Target Diff And Dirty-State Allowance

Implementation target range:

```text
0ad2292c4d13e76597c5191d9157503c780a5145..db0bcdfb6d9279f53f49195fbbea2d9572bc564a
```

Target commits:

```text
3111c52f7bc000786a5309dbcfb092123ca799bf Enforce Cleaning projection row references
9009151e59b90a17787191b229ca2e0963609d08 Flag ambiguous Cleaning text anchors
db0bcdfb6d9279f53f49195fbbea2d9572bc564a Enforce typed ECR smoke receipts
```

Observed target files in that range:

```text
M orca-harness/ecr/__init__.py
M orca-harness/ecr/models.py
M orca-harness/runners/run_capture_ecr_cleaning_smoke.py
M orca-harness/runners/run_cleaning_spine_periodic_audit.py
M orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
M orca-harness/tests/unit/test_ecr_models.py
```

Use `git diff 0ad2292c4d13e76597c5191d9157503c780a5145..db0bcdfb6d9279f53f49195fbbea2d9572bc564a -- <target files>` as the reviewed implementation diff. If the branch contains a later prompt-only commit, verify whether the six target files above still match `db0bcdfb6d9279f53f49195fbbea2d9572bc564a`. If they changed, report `SOURCE_CONTEXT_INCOMPLETE` or review the newer target only if the operator explicitly authorizes that retarget.

## Validation Evidence To Inspect

The author observed these checks after the ECR receipt patch:

```powershell
python -B -m pytest -p no:cacheprovider --tb=short tests\unit\test_ecr_models.py tests\unit\test_capture_ecr_cleaning_smoke_runner.py -q
```

Observed output:

```text
..................................................                       [100%]
```

Broader no-network suite:

```powershell
python -B -m pytest -p no:cacheprovider --no-header --no-summary -q tests\unit\test_ecr_models.py tests\unit\test_ecr_timing_deriver.py tests\unit\test_ecr_source_visibility_models.py tests\unit\test_ecr_source_visibility_deriver.py tests\unit\test_ecr_source_side_composition.py tests\unit\test_ecr_packet_builder.py tests\unit\test_ecr_inspectability_models.py tests\unit\test_ecr_inspectability_deriver.py tests\unit\test_ecr_identity_models.py tests\unit\test_ecr_identity_deriver.py tests\unit\test_capture_ecr_cleaning_smoke_runner.py tests\unit\test_cleaning_core.py tests\unit\test_cleaning_projection_integration.py tests\unit\test_source_capture_ig_projection.py tests\unit\test_retail_pdp_projection.py tests\unit\test_reddit_consolidation.py
```

Observed output:

```text
........................................................................ [ 34%]
........................................................................ [ 68%]
..................................................................       [100%]
```

Also observed:

```powershell
python -B runners\run_capture_ecr_cleaning_smoke.py --help
python -B runners\run_cleaning_spine_periodic_audit.py --help
git diff --check
```

Both help checks exited 0 and printed usage. `git diff --check` exited 0 with Git CRLF normalization warnings only.

Environment notes:

- A restricted-sandbox pytest attempt failed at test setup with `_scratch` write `PermissionError`; the same targeted suite passed when rerun with workspace-local write permission. Do not treat the restricted-sandbox error as implementation failure unless your environment reproduces a code error independent of sandbox write ACLs.
- Use `python -B` for no-bytecode validation if rerunning tests.
- Do not run live capture, network capture, crawler behavior, scheduler behavior, API/dashboard code, storage/Data Lake operations, product-proof checks, or Judgment readiness checks.
- If you do not rerun validation, report validation as author-supplied and not independently revalidated.

## Review Scope

Attack these questions:

- Does projection-ref enforcement actually resolve every Cleaning handle's `projection_ref.row_id` against the named projection artifact, including retail/PDP, IG, and Reddit-shaped artifacts where row containers differ?
- Does the projection-ref check fail closed when the projection artifact is absent, malformed, points outside the preserved packet, or contains duplicate or structurally ambiguous row ids?
- Does ambiguous `text_pattern` detection correctly identify duplicate raw-text matches without treating HTML/script/JSON anchors as equivalent when their anchor type has stronger specificity?
- Does the ambiguous-anchor finding preserve failure visibility in the smoke summary and periodic audit result instead of remaining advisory-only while the audit reports clean?
- Does the ambiguous-anchor logic avoid false positives for intentionally file-level anchors, empty anchors, unavailable-with-reason rows, or non-text anchors?
- Does the typed ECR receipt model require identity, inspectability, timing, and source_visibility posture buckets, required clear keys, non-empty receipts, unique packet/ref keys, and the exact `ecr:<packet_id>:source_side_postures` coupling?
- Does the typed ECR receipt model correctly reject clear-flag mismatches between aggregate `clears` and posture rows, including partial false values and empty posture lists?
- Does the smoke runner now construct ECR receipt artifacts through the schema rather than dumping a loose dict that can drift?
- Does the periodic audit validate both Lane A existing-package ECR receipts and Lane B rebuilt ECR receipts through the same schema?
- Do tests include negative fixtures for projection-ref miss, ambiguous anchors, invalid ECR receipt shape, clear mismatch, ref packet mismatch, and duplicate receipt keys?
- Does the implementation keep Cleaning in its lane: no credibility, salience, independence, demand, actionability, product-proof, or Judgment vocabulary introduced as a Cleaning decision?
- Does the implementation remain no-network and bounded to existing packet/projection/consolidation/smoke artifacts?
- Does any enforcement accidentally make a known residual invisible, for example by turning a failed/blocked capture handle into a clean-looking Cleaning handle or by hiding source-family-specific adapter gaps?
- Does any new schema strictness break existing valid smoke artifacts without a migration path or clear residual report?

## Intended Enforcement Closure Check

Treat these enforcement goals as claims to verify, not accepted truth:

- E-01 projection refs: every `projection_ref.row_id` in Cleaning resolves inside the named projection artifact.
- E-02 ambiguous anchors: duplicate raw `text_pattern` anchors are flagged so cleaned text does not imply stronger traceability than raw supports.
- E-03 typed ECR receipts: ECR receipt artifacts are explicit Pydantic models with required posture kinds, required clear aggregation, packet/ref coupling, and duplicate-key rejection.

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

`docs/review-outputs/cleaning_spine_enforcement_batch_claude_cross_vendor_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by: operator_to_fill_claude_identity`
- `authored_by: gpt-family-codex`
- `de_correlation_bar: cross_vendor_discovery` only if the reviewer is Anthropic/Claude-family; otherwise use `same_vendor_sanity` or `self_fallback`
- `same_vendor_rationale:` required if `de_correlation_bar` is `same_vendor_sanity`
- source-read ledger
- `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`
- findings first
- intended enforcement closure table for E-01/E-02/E-03
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
- intended enforcement closure statuses for E-01/E-02/E-03
- proposed patch, diff, or exact requested edits, if authorized
- citations
- reviewer verdict
- validation evidence and not-run checks
- residual risk
- blockers, off-scope flags, and not-proven boundaries
```
