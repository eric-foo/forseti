# Data Capture Obligation Baseline Decision Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial artifact review prompt for the proposed Data Capture obligation-baseline decision.
use_when:
  - Reviewing whether `ACCEPT_BASELINE` is justified before owner acceptance.
  - Testing whether manual-harness or BT2-04 P2 issues were misclassified away from the obligation baseline.
  - Checking whether the proposed baseline decision overclaims authority, validation, readiness, or downstream architecture permission.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/data_capture_obligation_baseline_decision_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
stale_if:
  - The review target is materially revised.
  - Owner accepts, rejects, or patches the Data Capture obligation-baseline decision.
  - The Data Capture obligation contract or direction-signal decision is superseded.
```

- Review lane: adversarial artifact review.
- Prompt artifact path: `docs/prompts/reviews/data_capture_obligation_baseline_decision_adversarial_artifact_review_prompt_v0.md`.
- Required report path: `docs/review-outputs/adversarial-artifact-reviews/data_capture_obligation_baseline_decision_adversarial_artifact_review_v0.md`.
- Output mode: `review-report`.
- Reviewer edit permission: read-only except writing the required review report.
- Patch queue authorized: no.
- Patch execution authorized: no.
- Harness architecture authorized: no.
- Runtime/source-system/ECR/Cleaning/Judgment work authorized: no.
- Created: 2026-05-28.

## Paste-Ready Prompt

```text
You are performing a read-only adversarial artifact review for Orca.

Review target:
- `docs/product/data_capture_obligation_baseline_decision_v0.md`

Required durable report path:
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_obligation_baseline_decision_adversarial_artifact_review_v0.md`

Review purpose:
Adversarially test whether the proposed `ACCEPT_BASELINE` decision is justified
before owner acceptance. Focus narrowly on whether the review target correctly
classifies issues as baseline-level, harness-level, dry-run-level,
fixture/synthesis-level, downstream-level, or optional hardening; whether dirty
or untracked working evidence weakens the acceptance path; and whether the
artifact overclaims authority, validation, readiness, source-of-truth promotion,
or downstream architecture permission.

Do not re-review the entire Data Capture Spine. Do not architecture-plan the
Data Capture Harness. Do not patch anything.

Required source hierarchy:
1. Current launch instruction for this review.
2. Orca `AGENTS.md`.
3. Orca overlay under `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with the overlay.
5. Reusable workflow methods only for generic review mechanics, not Orca facts.

Do not import `jb` rules, paths, lifecycle mechanics, product policy,
validation habits, review labels, or handoff rules as Orca authority.

Worktree preflight:
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: `main`
- Expected HEAD at prompt creation: `b7627d3`
- Dirty-state allowance: dirty and untracked named sources are in scope because
  the target and several supporting sources are current working evidence.
- Dirty-state caveat to test: dirty/untracked sources may support advisory
  review findings, but they do not prove owner acceptance, validation,
  readiness, source-of-truth promotion, or implementation authorization.
- If the workspace, branch, or target artifact is unavailable, return a blocked
  review result instead of reviewing a substitute checkout.

Before review work, record:

orca_start_preflight:
  agents_read: yes/no
  overlay_read: yes/no
  source_pack: custom S3/S4 bounded baseline-decision review pack
  edit_permission: read-only review plus review-report write only
  target_scope:
    - docs/product/data_capture_obligation_baseline_decision_v0.md
  report_path:
    - docs/review-outputs/adversarial-artifact-reviews/data_capture_obligation_baseline_decision_adversarial_artifact_review_v0.md
  dirty_state_checked: yes/no
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/data_capture_obligation_baseline_decision_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md

Required method sequence:
1. REFERENCE-LOAD `workflow-deep-thinking`.
2. REFERENCE-LOAD `workflow-adversarial-artifact-review`.
3. Do not APPLY either method yet. Before source readiness, use them only to
   prepare neutral source-reading questions.
4. SOURCE-LOAD the required Orca sources below.
5. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
6. Only after source readiness, APPLY `workflow-deep-thinking` to frame the
   boundary problem, decision criteria, and failure modes.
7. Then APPLY `workflow-adversarial-artifact-review` to produce findings.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or cannot
be applied after `SOURCE_CONTEXT_READY`, return a blocked or advisory-only
result. Do not emit formal verdicts, severity authority, blocked/ready status,
validation claims, readiness claims, mandatory remediation, patch queues,
executor-ready handoffs, or alignment-complete claims.

Required control and review-lane sources:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/product-proof.md`

Required target and decision sources:
- `docs/product/data_capture_obligation_baseline_decision_v0.md`
- `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md`

Required baseline and boundary sources:
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_pressure_test_synthesis_usage_note_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_full_fixture_synthesis_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/product/core_spine_v0_product_contract.md`
- `docs/product/core_spine_v0_information_production_foundation_v0.md`

Required review evidence:
- `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_full_fixture_synthesis_adversarial_review_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/core_spine_v0_data_capture_spine_manual_harness_bt204_dry_run_adversarial_review_v0.md`

Default exclusions:
- Do not read `docs/_inbox/`.
- Do not bulk-load all product, prompt, review, research, workflow, proof-run,
  or method-validation replay files.
- Do not read implementation folders or create implementation scope.
- Do not widen into ECR, Cleaning, Judgment, runtime, automation, source-system,
  scraper, API, dashboard, storage, schema, tests, package, commit, push, or PR
  work.
- Do not review the obligation contract from scratch except where needed to
  test the target artifact's baseline decision and issue classification.

Source readiness gate:
Before findings, declare one of:
- `SOURCE_CONTEXT_READY`
- `SOURCE_CONTEXT_INCOMPLETE`

If ready, include a compact source ledger in the report: source, why read, and
what claim or finding it supports.

If incomplete, name missing sources, what review claims cannot be made, and the
smallest complete source capsule needed. If missing sources could change the
decision, write a blocked review report instead of proceeding with findings.

Review questions:
1. Is `ACCEPT_BASELINE` justified by the target's cited sources, or does the
   artifact skip a contract-level defect that should force
   `PATCH_BEFORE_ACCEPTANCE` or `REJECT_BASELINE`?
2. Did the target correctly classify manual harness and BT2-04 P2 findings as
   harness/dry-run defects rather than baseline-contract blockers?
3. Did the target correctly handle full-fixture synthesis adversarial findings
   as synthesis clarity / optional hardening rather than baseline blockers?
4. Does the target rely on dirty or untracked working evidence in a way that
   weakens owner acceptance, source-of-truth promotion, validation, or
   readiness claims?
5. Does the target's downstream implication stay tight enough to prevent a
   later harness architecture lane from drifting into runtime, ECR, Cleaning,
   Judgment, source systems, scrapers, APIs, dashboards, storage, automation,
   schemas, tests, packages, commits, pushes, or PRs?
6. Does the target preserve the accepted direction-signal demotion and avoid
   letting BT2-04 become controlling architecture?
7. Does the target overclaim validation, readiness, approval, buyer proof,
   commercial proof, implementation authority, or source-of-truth promotion?

Finding severity:
Use these labels only as finding-priority labels:
- `critical`: a defect that invalidates `ACCEPT_BASELINE`, hides a baseline
  blocker, or makes owner acceptance materially unsafe.
- `major`: a defect that should be patched before owner acceptance or before
  architecture planning can rely on the artifact.
- `minor`: a clarity, retrieval, caveat, or wording issue that does not block
  owner acceptance but should be cleaned up when practical.

These severity labels do not create approval, rejection, validation, readiness,
mandatory remediation, or patch authority.

Recommendation vocabulary:
Use exactly one:
- `accept`
- `accept_with_friction`
- `patch_before_acceptance`
- `reject`
- `blocked`

Use `accept` only if no findings materially weaken owner acceptance.
Use `accept_with_friction` if owner acceptance is reasonable but minor or
non-blocking caveats should travel forward.
Use `patch_before_acceptance` if any critical or major issue should be fixed
before owner acceptance.
Use `reject` only if the target's baseline decision is materially wrong.
Use `blocked` if required source, write destination, method invocation, or
preflight is missing.

Report output contract:
Write the full review report to:

`docs/review-outputs/adversarial-artifact-reviews/data_capture_obligation_baseline_decision_adversarial_artifact_review_v0.md`

The durable report must include:

1. Title
   - `# Data Capture Obligation Baseline Decision Adversarial Artifact Review v0`

2. Retrieval Header
   - Use the Orca retrieval header shape.
   - `artifact_role: Review report`
   - `authority_boundary: retrieval_only`

3. Review Summary
   - Recommendation using the vocabulary above.
   - Findings count.
   - Blocking findings, if any.
   - Advisory findings, if any.
   - Next action.

4. Source Readiness
   - `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
   - Preflight receipt.
   - Compact source ledger.
   - Dirty/untracked source caveats.

5. Commission And Target
   - Commission: narrow adversarial review of the proposed baseline decision.
   - Target: exact artifact path.
   - Explicit non-targets.

6. Decision Criteria
   - The review questions and failure modes actually applied.

7. Findings
   - Findings first, ordered by severity.
   - For each finding include:
     - severity;
     - location;
     - issue;
     - evidence;
     - impact;
     - minimum_closure_condition;
     - next_authorized_action;
     - recommended correction or advisory remediation direction.

8. Non-Findings / Confirmed Boundaries
   - State material high-risk areas checked where no issue was found.

9. Residual Risks
   - Name risks not eliminated by this review.

10. Review-Use Boundary
   - State that this read-only review is decision input only, not approval,
     validation, readiness, mandatory remediation, patch authority, or
     implementation authority.

Do not include `patch_queue_entry`. Do not provide executor-ready edit steps.
Recommended corrections may state the end state needed, but not an executable
patch plan.

After the durable report is written successfully, return only the compact YAML
summary in chat:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/data_capture_obligation_baseline_decision_adversarial_artifact_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  summary: "One sentence describing the review result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step"
```

If the report cannot be written after `review-report` mode is selected, do not
use `report_path`. Return:

```yaml
review_summary:
  status: failed
  review_location: chat_only_current_thread
  recommendation: blocked
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/data_capture_obligation_baseline_decision_adversarial_artifact_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve the report write failure, then rerun the review-report prompt."
```

Review-use boundary:
This is a read-only adversarial artifact review. Findings and non-findings are
decision input only. They are not owner acceptance, approval, validation,
product proof, readiness, mandatory remediation, patch authority, or
executor-ready implementation guidance unless a separate authorized Orca
decision or execution lane accepts them.
```
