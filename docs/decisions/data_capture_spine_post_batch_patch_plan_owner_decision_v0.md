# Data Capture Spine Post-Batch Patch Plan Owner Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Owner decision accepting the minor-patched post-batch Data Capture patch plan as bounded input for downstream docs-only patch drafts.
use_when:
  - Checking whether the post-batch patch plan has been accepted, narrowed, revised, or rejected.
  - Routing the next Data Capture docs-only obligation-contract or source-access method patch draft.
  - Confirming whether contract hardening, source-access implementation, runtime work, or downstream ECR/Cleaning/Judgment design is authorized.
authority_boundary: retrieval_only
open_next:
  - docs/product/data_capture_spine/data_capture_spine_post_batch_patch_plan_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_post_batch_patch_plan_adversarial_artifact_review_v0.md
  - docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/product/data_capture_spine/data_capture_source_access_method_plan_v0.md
stale_if:
  - The post-batch patch plan is materially revised after this decision.
  - A later owner decision supersedes this decision.
  - The obligation contract or source-access method plan is materially amended in response to this decision.
```

## Status And Decision

Status: `ACCEPTED_POST_BATCH_PATCH_PLAN_FOR_DRAFTING_V0`.

Owner decision: `ACCEPT_PATCH_PLAN_FOR_CONTRACT_AND_METHOD_PATCH_DRAFTS`.

The minor-patched post-batch Data Capture patch plan is accepted as the bounded planning basis for downstream docs-only patch drafts. This decision accepts the plan for drafting authority only. It does not amend or harden the obligation contract, amend the source-access method plan, promote MSP, require checker standards, authorize runtime/source-system work, or authorize ECR, Cleaning, or Judgment design.

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes - AGENTS.md supplied in current task context
  overlay_read: yes
  source_pack: custom Data Capture post-batch patch-plan owner gate
  edit_permission: docs-write
  target_scope: owner decision accepting the post-batch Data Capture patch plan for bounded docs-only patch drafts
  dirty_state_checked: yes - worktree dirty; overlay and controlling product sources are modified/untracked; advisory-only boundaries preserved except for this explicit owner decision
  blocked_if_missing: none
```

## Source Basis

Decision inputs:

- Current owner instruction: "yes accept".
- `docs/product/data_capture_spine_post_batch_patch_plan_v0.md`, status `POST_BATCH_PATCH_PLAN_MINOR_PATCH_APPLIED_FOR_OWNER_GATE_INPUT_V0`.
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_post_batch_patch_plan_adversarial_artifact_review_v0.md`, recommendation `use_as_owner_gate_input_after_minor_patch`.
- `docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md`, which authorized docs-only patch planning and rejected contract hardening, source-access implementation, runtime/source-system work, and downstream ECR/Cleaning/Judgment design.

The adversarial review produced no blocking findings and recommended use as owner-gate input after a minor patch. The patch plan records that the minor patch was applied.

## Accepted Scope

Accepted for downstream docs-only patch drafting:

- CPC-01 through CPC-05 as obligation-contract patch proposal inputs.
- SAMP-01 through SAMP-07 as source-access method plan patch proposal inputs.
- MSP next-gate options as an owner-decision queue, not as a selected option.
- COMR-01 and COMR-02 as checker operating-model patch proposal inputs.
- COMR-03 as a checker-comparability planning question only.

COMR-03 owner clarification: checker invocation equivalence may travel into a future patch draft as a question about comparability between separate checker invocation, artifact-internal self-check, and missing checker pass. It is not accepted as a required checker standard, validation rule, approval rule, model-agreement rule, or readiness criterion.

## Authorized Next Work

This decision authorizes separate docs-only draft artifacts for:

1. An obligation-contract patch proposal covering vocabulary, Obligation #16, Obligation #6, and checker glossary/comparability questions.
2. A source-access method plan patch proposal covering verbatim/structure capture, archive-content retrieval, screenshot/media preservation, access degradation, thread-graph capture, timestamp discipline, and raw-preserving projection.
3. Optional review prompts or adversarial review prompts for those draft artifacts.

Those drafts may propose language, compare alternatives, and name owner decisions. They must not directly edit or harden the controlling obligation contract or source-access method plan unless a later turn explicitly authorizes applying the patch.

## Deferred Or Rejected Moves

Still deferred:

- applying or hardening any obligation-contract patch;
- applying or hardening any source-access method plan patch;
- selecting an MSP next-gate option;
- promoting MSP into a final contract obligation;
- making pass-2 vocabulary checking required;
- making checker invocation count, checker agreement, or checker self-check equivalent to validation, approval, readiness, proof, or source adequacy;
- running another pressure-test batch;
- source-access implementation, runtime tools, scrapers, APIs, dashboards, storage, schemas, tests, packages, deployment, commits, pushes, or PRs;
- ECR design, Cleaning implementation, Judgment rules, buyer proof, or commercial-readiness claims.

## Next Gate

The next gate is a docs-only patch draft or pair of drafts. After each draft is written, it should be reviewed before any controlling source is amended.

Recommended sequencing:

1. Draft the obligation-contract patch proposal first, because it defines the vocabulary and handoff language that the source-access method plan should not contradict.
2. Draft the source-access method plan patch proposal second, using the accepted source-access boundary and the obligation-contract proposal as constraints.
3. Review each draft before asking the owner to apply changes to controlling sources.

## Non-Claims

This decision is not validation, readiness, source-of-truth promotion, final contract hardening, obligation-contract amendment, source-access method plan amendment, runtime authorization, tooling authorization, source-system authorization, schema authorization, ECR design, Cleaning implementation, Judgment design, buyer proof, commercial-readiness evidence, pressure-test discharge, or authorization to run another pressure-test batch.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "The owner accepted the minor-patched post-batch Data Capture patch plan as bounded authority for downstream docs-only patch drafts, without amending the obligation contract or source-access method plan."
  trigger: lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/product/data_capture_spine_post_batch_patch_plan_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/product/data_capture_source_access_method_plan_v0.md
    - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_post_batch_patch_plan_adversarial_artifact_review_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: "The workspace rule already permits bounded docs/decision work and still requires explicit authorization for implementation/runtime work; this decision does not change that rule."
    - path: CLAUDE.md
      reason: "The shim remains subordinate to AGENTS.md and the Orca overlay; no Claude-specific instruction changed."
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: "The source hierarchy and propagation contract did not change; this decision applies the existing propagation contract."
    - path: docs/product/data_capture_spine_post_batch_patch_plan_v0.md
      reason: "The patch plan remains the accepted input artifact; this decision records owner acceptance rather than rewriting the plan itself."
    - path: docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
      reason: "This decision authorizes a future patch proposal draft; it does not apply or harden contract changes."
    - path: docs/product/data_capture_source_access_method_plan_v0.md
      reason: "This decision authorizes a future method-plan patch proposal draft; it does not amend the method plan."
    - path: docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_post_batch_patch_plan_adversarial_artifact_review_v0.md
      reason: "The review report remains historical input for the pre-acceptance patch plan state; this decision records the owner gate after the minor patch."
  stale_language_search: "rg -n \"owner-gate input, not patch authority|Until one of those decisions is recorded|REVISE_PATCH_PLAN_BEFORE_USE|REJECT_PATCH_PLAN|contract hardening now authorized|runtime/source-system implementation now authorized|source-access implementation now authorized|validation-ready|ready for implementation\" docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not final contract hardening"
    - "not runtime authorization"
    - "not implementation authorization"
```
