# Data Capture Spine Post-Batch Patch Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact - post-batch patch plan
scope: Post-batch patch plan for the first bounded N=3 Data Capture pressure-test batch, sequencing contract candidates, source-access refinements, MSP next gate, checker refinements, and owner/deferred gates without applying patches.
use_when:
  - Planning the docs-only Data Capture refinements authorized by the first N=3 pressure-test batch classification decision.
  - Separating patch candidates from obligation-contract hardening, source-access implementation, or ECR/Cleaning/Judgment design.
  - Preparing the next owner gate or adversarial artifact review for Data Capture patch planning.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md
  - docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md
  - orca/product/spines/capture/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/spines/capture/contracts/source_access_boundary/data_capture_source_access_method_plan_v0.md
stale_if:
  - The first N=3 batch classification decision is superseded.
  - The N=3 synthesis is materially revised.
  - The obligation contract, source-access method plan, Data Capture/Cleaning boundary, or MSP intake surface is materially amended.
```

## Status

Status: `POST_BATCH_PATCH_PLAN_MINOR_PATCH_APPLIED_FOR_OWNER_GATE_INPUT_V0`.

This artifact covers the scoped post-batch patch-planning route:

- source grounding;
- artifact shell and boundary;
- contract patch candidates;
- source-access method plan refinements;
- MSP next gate.
- checker operating-model refinements;
- deferred-until-owner-acceptance register;
- owner-gate section;
- navigation/retrievability treatment;
- local validation checks.

Adversarial artifact review completed at `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_post_batch_patch_plan_adversarial_artifact_review_v0.md` with recommendation `use_as_owner_gate_input_after_minor_patch`. This version applies that minor patch. It is still not owner-acceptance authority or patch authority.

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom Data Capture Intake Surface / MSP Pressure-Test Target Pack
  edit_permission: docs-write
  target_scope: post-batch Data Capture patch plan minor-patched for owner-gate input
  dirty_state_checked: yes - worktree dirty; overlay and controlling product sources are modified/untracked; advisory-only boundary applies to this artifact; no strict readiness, validation, or proof claims made
  blocked_if_missing: none
```

## Source Basis

Controlling source basis for this patch plan:

- `docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md`
- `docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/data_capture_source_access_method_plan_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`
- `docs/product/data_capture_spine_intake_surface_consolidation_v0.md`
- `docs/product/data_capture_harness_operating_model_architecture_v2.md`

The classification decision authorizes docs-only patch planning for vocabulary, Obligation #16, Obligation #6, checker glossary questions, and source-access method planning refinement. It explicitly does not authorize obligation-contract hardening, runtime/source-system implementation, ECR design, Cleaning implementation, Judgment rules, buyer proof, or commercial-readiness claims.

## Patch-Planning Boundary

This artifact organizes candidate patch work. It does not apply any patch.

Allowed in this artifact:

- name patch candidates surfaced by the first N=3 pressure-test batch;
- sequence candidate questions for later owner decision;
- keep source-access requirements at method-planning level;
- keep MSP as a candidate helper over preserved raw;
- preserve non-claims and deferred gates.

Forbidden in this artifact:

- amending or hardening the obligation contract;
- changing the source-access method plan;
- authorizing runtime, source-system work, APIs, scrapers, dashboards, storage, schemas, tests, packages, deployment, commits, pushes, or PRs;
- designing ECR, Cleaning, or Judgment behavior;
- treating checker output as validation, readiness, approval, or proof.

## Contract Patch Candidates

These candidates should travel into a later obligation-contract patch proposal. They are not contract amendments in this artifact.

### CPC-01: `cannot_assess` / `indeterminate`

Source signal:

- Slot 1 reached for `indeterminate` / `cannot_assess` in F-C because source-fidelity loss made a fairness ceiling unevaluable.
- Slot 2 used `cannot_assess` for #6 and #12 when zero raw observable and zero related context could not be represented cleanly by the current six-state vocabulary.
- The classification decision treats Slot 1 as a patch-planning warning signal and Slot 2 as the explicit discharge-vocabulary break.

Patch-planning question:

Should the obligation contract add a state for "required and attempted, but not assessable from the captured observable," or should affected obligations be rewritten so assessment is explicitly conditional on faithful capture?

Boundary:

This candidate must not become a permission to skip capture. It only names a visible state for cases where capture limits prevent assessment.

### CPC-02: `insufficient` / `assessed_not_met`

Source signal:

- Slot 2 used `insufficient` for #16 when handoff sufficiency was judgeable and judged not satisfied because capture access failed.
- The current vocabulary includes `partial`, `blocked`, and `unavailable_by_source`, but no clean value for "required, attempted, assessed, and not satisfied."

Patch-planning question:

Should the obligation contract add a judged-failed state distinct from `partial`, `blocked`, and `unavailable_by_source`?

Boundary:

This candidate should stay tied to capture-owned obligations. It must not import Judgment conclusions about usefulness, credibility, or decision support.

### CPC-03: Tool-Origin Block Versus Boundary `blocked`

Source signal:

- Slot 1 and Slot 2 exposed tool-layer or origin-layer capture failures: paraphrase instead of verbatim source observable, archive content tool-block, and Teal 403 block.
- The source-access method plan distinguishes tool constraints from hard-stop boundary limits.

Patch-planning question:

Should the obligation contract distinguish "capture/access method failed" from "source boundary or project boundary blocks collection," so operators do not overload `blocked`?

Boundary:

This candidate must preserve hard stops. It must not weaken source-access boundaries or convert blocked collection into authorization for no-entitlement gate bypass, nonconsensual sessions, exploits, stolen credentials/cookies, or obvious cross-account/private/admin spillover once noticed.

### CPC-04: Obligation #16 Handoff-Readiness Versus Actual ECR Receipt

Source signal:

- Slot 1 treated #16 as impossible in phase because no ECR receiver existed, while the underlying issue was handoff-readiness.
- Slot 2 assessed #16 and judged the handoff insufficient, producing a visible blocker.
- Slot 3 completed a bounded first-pass categorical handoff with limitations.

Patch-planning question:

Should #16 separate "capture-owned handoff-readiness posture" from "actual ECR receipt / handoff act"?

Boundary:

This candidate must not define ECR fields, IDs, keys, tables, storage, schemas, or receipt mechanics. It may only clarify what Capture must make visible before ECR can receipt categorically.

### CPC-05: Obligation #6 Raw Observable Fidelity Split

Source signal:

- Slot 1 captured pricing facts but not faithful source wording, layout, emphasis, table placement, nesting, proximity, or visible packaging cues.
- Slot 2 captured no verbatim observable under full content block.
- Slot 3 preserved Reddit raw JSON, screenshots, and projected rows, while WSO remained pointer-level without local raw HTML or screenshot corpus.

Patch-planning question:

Should #6 distinguish fact preservation, source-language preservation, visible-structure preservation, modality preservation, and frame-keyed sufficiency?

Boundary:

This candidate should clarify capture fidelity. It must not become Cleaning normalization, semantic summarization, or Judgment discounting.

## Source-Access Method Plan Refinements

These refinements should travel into a later source-access method planning patch. They do not authorize building, installing, running, testing, or operating any tool.

### SAMP-01: Verbatim And Structure Capture

Batch signal:

- Slot 1 showed that paraphrase can preserve prices and product names while losing source wording, layout, and packaging signal.
- Slot 2 showed the lower bound: zero verbatim content makes source-backed capture fail.

Planning refinement:

The method plan should distinguish methods that return source-visible text and structure from methods that return paraphrase or summary. Human-led browser capture, raw HTTP/HTML capture, browser automation, or sanctioned APIs should be evaluated by whether they preserve the needed observable, not merely whether they reach the URL.

### SAMP-02: Archive Content Retrieval

Batch signal:

- Slot 1 and Slot 2 could observe archive availability, but archive content retrieval was tool-blocked.
- Slot 3 did not attempt external archive lookup for Reddit or WSO.

Planning refinement:

The method plan should distinguish archive existence, archive content access, not-attempted archive posture, and local-only preservation. Archive lookup should not be treated as satisfied merely because snapshot metadata exists.

### SAMP-03: Screenshot, Media, And Modality Preservation

Batch signal:

- Slot 1 surfaced layout and bundle packaging pressure.
- Slot 3 surfaced linked image/gallery and screenshot/media limitations.

Planning refinement:

The method plan should state when screenshots, gallery/media archiving, or visual-state preservation are required because layout, resume images, page chrome, galleries, or other modality cues carry signal.

### SAMP-04: Anti-Block And Access-Degradation Handling

Batch signal:

- Slot 2 produced Teal 403 blocks.
- WSO had public-page and prior fetch limitation pressure.
- The source-access method plan already accepts discoverable-or-entitled, disclosable, hard-stop-excluding methods, including anti-blocking techniques within that boundary.

Planning refinement:

The method plan should separate access-degradation categories: destination 403, tool-layer block, paraphrase/post-processing loss, archive-content block, account/free-login access, entitled paid/client/coworker access, and obvious spillover once noticed.

### SAMP-05: Thread Graph And Related-Context Capture

Batch signal:

- Slot 3 showed that Reddit raw/projection-backed capture can preserve a large thread corpus, while WSO remained pointer-level without full comment graph or local raw corpus.

Planning refinement:

The method plan should specify what "thread graph" means for forum/review sources: original post, signal-bearing comments, parent-child chains, visible continuations, deleted/edited/locked posture, and related-chain context needed by the Decision Frame.

### SAMP-06: Timestamp And Acquisition Discipline

Batch signal:

- Slot 3 showed that source timestamps and artifact dates are useful but not the same as exact operator acquisition timestamps.

Planning refinement:

The method plan should separate source timestamps, source edit timestamps, operator acquisition timestamps, archive timestamps, and artifact-write timestamps where feasible.

### SAMP-07: Raw-Preserving Projection

Batch signal:

- Slot 3 Reddit used MSP to produce inspectable projected rows while preserving raw JSON.

Planning refinement:

The method plan should treat projection as raw-preserving inspectability support. Projection cannot replace raw preservation, screenshots, archive attempts, source timestamps, or row reachability.

## MSP Next Gate

Current evidence:

- MSP was used only in Slot 3 Reddit.
- It made a high-volume threaded source inspectable without replacing preserved raw.
- It preserved visibility of at least one continuation marker.
- It did not prove MSP works across WSO, pricing/product pages, archive snapshots, image/gallery media, or blocked hosts.

Planning posture:

MSP should remain a Data Capture-owned helper over preserved raw at this stage.

Next-gate options to preserve for owner decision:

1. Keep MSP as an optional helper and do not promote it into a contract obligation.
2. Run a second MSP pressure point before deciding whether any contract language is warranted.
3. Draft a narrow projection-packet candidate obligation only if it remains subordinate to raw preservation and evidence-row reachability.

Do not choose among these options in this patch plan. Choosing is an owner-gate decision after adversarial review.

## Checker Operating-Model Refinements

These refinements should travel into a later checker or obligation-contract patch proposal. They do not make checker output validation, readiness, approval, or proof.

### COMR-01: Pass-2 Vocabulary-Consistency Checker

Source signal:

- Slot 1 pass 2 identified a look-alike vocabulary/prose issue while preserving labeled contract proposals as proposals.
- Slot 2 pass 2 treated out-of-contract values as labeled proposals rather than hidden divergences.
- Slot 3 checker posture was not fully equivalent because the WSO checker was artifact-internal rather than a separate manual GPT-5.5 invocation.

Patch-planning question:

Should pass-2 vocabulary-consistency checking become required, optional, or retired for future pressure-test runs?

Boundary:

Pass 2 may expose vocabulary drift or proposal labeling. It must not certify capture quality, source adequacy, readiness, validation, or handoff sufficiency.

### COMR-02: Checker Token Glossary

Source signal:

- Slot 1 and Slot 2 used `capture_closure_blocker`.
- Slot 3 used `visible_capture_limitation`.
- The synthesis surfaced potential confusion around tokens that sound like closure or validation but actually signal visible capture state.

Patch-planning question:

Should checker tokens such as `capture_closure_blocker`, `visible_capture_limitation`, `vocabulary_divergence`, and `vocabulary_consistent` receive mandatory glosses?

Boundary:

Glosses should name what the token does and does not mean. They should prevent "checker passed" from being read as validation, readiness, approval, or source adequacy.

### COMR-03: Checker Invocation Equivalence

Source signal:

- Slot 1 and Slot 2 used explicit pass-1 / pass-2 checker posture.
- Slot 3 included Reddit and WSO limitation visibility, but WSO checker posture was artifact-internal rather than a separate manual GPT-5.5 invocation.

Authorization note:

Checker invocation equivalence derives from the classification decision's broad "patchable operating-model refinement" authorization for checker behavior rather than a named item. Owner confirmation during owner-gate review is recommended before this candidate travels into a future patch draft.

Patch-planning question:

Should future pressure-test artifacts distinguish separate checker invocation, artifact-internal self-check, and missing checker pass?

Boundary:

This should improve evidence comparability. It must not turn checker invocation count or model agreement into acceptance, proof, validation, or source-of-truth promotion.

## Deferred Until Owner Acceptance

The following are explicitly deferred until after adversarial review and owner acceptance of this patch plan:

- applying any obligation-contract patch;
- applying any source-access method plan patch;
- choosing whether MSP remains optional, receives a second pressure point, or becomes a candidate obligation;
- making pass-2 vocabulary checking required;
- renaming or hardening checker tokens;
- running another pressure-test batch;
- authorizing source-access implementation, runtime tooling, scrapers, APIs, dashboards, storage, schemas, tests, packages, deployment, commits, pushes, or PRs;
- designing ECR, Cleaning, or Judgment behavior.

## Owner Gate

Recommended gate sequence:

1. Review the completed adversarial artifact review report and this minor-patched version.
2. Owner accepts, narrows, or rejects the patch plan.
3. Only after owner acceptance, authorize a separate obligation-contract patch draft or source-access method plan patch.

Owner decision options:

- `ACCEPT_PATCH_PLAN_FOR_CONTRACT_AND_METHOD_PATCH_DRAFTS`
- `ACCEPT_PATCH_PLAN_WITH_NARROWING`
- `REVISE_PATCH_PLAN_BEFORE_USE`
- `REJECT_PATCH_PLAN`

Until one of those decisions is recorded, this artifact remains a planning input and review target, not patch authority.

## Navigation And Retrievability Treatment

This completion pass updates retrievability surfaces narrowly:

- `.agents/workflow-overlay/source-loading.md` names this artifact for post-batch patch planning and review.
- `docs/workflows/orca_repo_map_v0.md` lists this artifact in the Data Capture product-method surface.

The updates are navigation and source-loading treatment only. They do not amend the obligation contract, source-access method plan, ECR/Cleaning/Judgment boundaries, runtime authorization, or pressure-test status.

## Validation Readback

Authoring-time validation for this artifact includes:

- full file readback after edits;
- targeted key-anchor search for required sections and non-claims;
- claim-safety search for validation, readiness, hardening, runtime/tooling, ECR, Cleaning, Judgment, buyer-proof, and commercial-readiness overclaims;
- `git diff --check` on touched files.

This readback is authoring hygiene only. It is not validation, readiness, acceptance, source-of-truth promotion, or proof.

Validation execution receipt for the adversarial-review minor patch:

- full file readback: completed after the minor patch;
- key-anchor search: completed; required sections and patched status anchor were present;
- navigation anchor search: completed; source-loading and repo-map point to this patch plan;
- stale-language search: completed; only expected self-reference appeared inside the recorded search string;
- claim-safety search: completed; expected matches were boundary, non-claim, owner-gate, or recorded-search contexts only;
- `git diff --check`: run on touched patch-plan/navigation files; no whitespace errors; existing LF/CRLF warnings appeared for source-loading and repo-map only.

## Non-Claims

This patch plan is not validation, readiness, acceptance, source-of-truth promotion, final contract hardening, obligation-contract amendment, source-access method plan amendment, runtime authorization, tooling authorization, source-system authorization, schema authorization, ECR design, Cleaning implementation, Judgment design, buyer proof, commercial-readiness evidence, pressure-test discharge, or authorization to run another pressure-test batch.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "The completed post-batch Data Capture patch plan is registered as the next docs-only routing artifact for adversarial review and owner gating, without amending the obligation contract or authorizing implementation."
  trigger: workflow_authority
  controlling_sources_updated:
    - docs/product/data_capture_spine_post_batch_patch_plan_v0.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/product/data_capture_source_access_method_plan_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: "This patch plan registers and minor-patches a docs-only routing artifact for owner-gate input; it does not change project operating rules, docs-write defaults, or the explicit-authorization boundary for implementation/runtime work."
    - path: CLAUDE.md
      reason: "The shim remains subordinate to AGENTS.md and the Orca overlay; no Claude-specific instruction changed."
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: "The source hierarchy and propagation contract did not change; this artifact applies the existing propagation contract."
    - path: docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
      reason: "This artifact plans candidate obligation-contract changes but does not apply or harden them."
    - path: docs/product/data_capture_source_access_method_plan_v0.md
      reason: "This artifact plans source-access method refinements but does not amend the method plan."
  stale_language_search: "rg -n \"PARTIAL_DRAFT_STEP_01_05|partial draft|partial artifact|contract hardening now authorized|runtime/source-system implementation now authorized|source-access implementation now authorized|validation-ready|ready for owner acceptance\" docs/product/data_capture_spine_post_batch_patch_plan_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not final contract hardening"
    - "not runtime authorization"
    - "not implementation authorization"
```
