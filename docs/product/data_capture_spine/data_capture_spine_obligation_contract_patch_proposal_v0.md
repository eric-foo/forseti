# Data Capture Spine Obligation Contract Patch Proposal v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Docs-only patch proposal for Data Capture Spine obligation-contract vocabulary, Obligation #6, Obligation #16, and checker-adjacent wording after the first bounded N=3 pressure-test batch.
use_when:
  - Reviewing candidate obligation-contract language before any contract amendment.
  - Preparing adversarial review of Data Capture obligation-contract patch proposals.
  - Deciding which proposed changes may be applied to the controlling obligation contract in a later owner-authorized patch.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md
  - docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md
  - docs/product/data_capture_spine/data_capture_spine_post_batch_patch_plan_v0.md
  - docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md
  - docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
stale_if:
  - A later owner decision supersedes the obligation-contract patch proposal owner decision.
  - A later adversarial artifact review supersedes the review report named in open_next.
  - A later owner decision supersedes the post-batch patch-plan owner decision.
  - The N=3 synthesis or batch classification decision is materially revised.
  - The controlling obligation contract is amended in response to this proposal.
  - A later obligation-contract patch proposal supersedes this artifact.
```

## Status

Status: `OBLIGATION_CONTRACT_PATCH_PROPOSAL_PATCHED_AFTER_ADVERSARIAL_REVIEW_V0`.

This artifact is a docs-only patch proposal. It does not amend, harden, or supersede `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`.

Patch note: this revision addresses the targeted findings from `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md`. It remains a proposal, not an owner acceptance or contract amendment.

Owner decision note: `docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md` accepts PCP-01 through PCP-08 for later bounded obligation-contract amendment drafting. This proposal remains the candidate-language source; the owner decision is the lifecycle gate.

## Start Preflight

```yaml
orca_start_preflight:
  agents_read: yes - AGENTS.md supplied in current task context
  overlay_read: yes
  source_pack: custom Data Capture obligation-contract patch proposal
  edit_permission: docs-write
  target_scope: proposal for downstream obligation-contract patch language without applying the patch
  dirty_state_checked: yes - worktree dirty; overlay and controlling product sources are modified/untracked; this artifact makes no strict validation, readiness, hardening, or implementation claim
  blocked_if_missing: none
```

## Source Basis

Accepted authority:

- `docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md` accepted the minor-patched post-batch patch plan for downstream docs-only patch drafts.
- `docs/product/data_capture_spine_post_batch_patch_plan_v0.md` accepted CPC-01 through CPC-05 and COMR-01 through COMR-03 as patch-proposal inputs, with COMR-03 narrowed to checker comparability.
- `docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md` classified the first bounded N=3 batch as patchable, not architecture-threatening.
- `docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md` organized the pressure-test evidence.
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` is the controlling contract this proposal is about, but not amended here.
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md` recommended targeted proposal patches before owner consideration.

## Proposal Boundary

Allowed here:

- propose contract-language changes;
- compare candidate labels and preferred wording;
- identify owner decisions needed before applying changes;
- preserve source-access, ECR, Cleaning, Judgment, and runtime boundaries.

Forbidden here:

- directly amending the controlling obligation contract;
- changing the source-access method plan;
- authorizing runtime/source-system work, APIs, scrapers, dashboards, storage, schemas, tests, packages, deployment, commits, pushes, or PRs;
- designing ECR fields, IDs, keys, tables, storage, schemas, or receipt mechanics;
- designing Cleaning transformations or Judgment rules;
- treating checker output as validation, readiness, approval, proof, source adequacy, or model-agreement authority.

## Proposal Summary

Preferred candidate package:

1. Add three proposal-only discharge vocabulary candidates: `cannot_assess`, `assessed_not_met`, and `access_failed`.
2. Clarify that `blocked` remains reserved for source boundary, project boundary, or allowed-boundary hard-stop blocks, not ordinary tool/origin access failure.
3. Split Obligation #16 into capture-owned handoff readiness and downstream actual ECR receipt.
4. Split Obligation #6 raw-observable preservation into fact/content, source language, visible structure, modality, and frame-keyed fidelity context.
5. Add checker-token glossary language and checker-invocation comparability language that cannot be read as validation or readiness.

## PCP-01: `cannot_assess` For Attempted But Unassessable Obligations

Current contract problem:

The current six discharge states allow `partial`, `blocked`, `unavailable_by_source`, and `not_attempted`, but they do not cleanly represent a required obligation that was attempted and visible, yet cannot be assessed because the captured observable is not faithful enough.

Pressure-test signal:

- Slot 1 reached for `indeterminate` / `cannot_assess` in F-C because source-fidelity loss made a fairness ceiling unevaluable.
- Slot 2 used `cannot_assess` for #6 and #12 where zero raw observable and zero related context could not be represented cleanly by the current vocabulary.
- The batch classification counted Slot 1 as a warning signal and Slot 2 as the explicit vocabulary break.

Preferred candidate language:

Candidate language only. Not yet operative. Subject to owner decision and separate amendment authorization.

```text
`cannot_assess`: the obligation was required and attempted, but the captured
observable is not faithful, complete, or inspectable enough to assess whether
the obligation was satisfied. The limitation and reason must be visible.
```

Rejected alias:

- Do not add `indeterminate` as a second canonical state unless the owner explicitly prefers it. It is less operationally precise than `cannot_assess` and risks becoming a generic uncertainty bucket.

What this fixes:

It gives operators a precise state for attempted capture where the artifact can show the failure without pretending the obligation was `partial`, `blocked`, or `not_attempted`.

What this must not authorize:

- skipping capture attempts;
- hiding unavailable raw material;
- converting weak capture into downstream admissibility;
- letting Capture decide credibility, usefulness, exclusion, discounting, Decision Strength, or Action Ceiling.

Owner decision needed:

Accept, revise, or reject `cannot_assess` as a candidate discharge state.

## PCP-02: `assessed_not_met` For Judgeable Failed Capture Obligations

Current contract problem:

The current vocabulary does not cleanly represent a required, attempted, judgeable obligation that is assessed and found not satisfied. `partial` implies some satisfaction; `blocked` implies boundary block; `unavailable_by_source` implies source non-exposure.

Pressure-test signal:

- Slot 2 used `insufficient` for #16 when handoff sufficiency was judgeable and judged not satisfied because capture access failed.
- The patch plan surfaced this as `insufficient` / `assessed_not_met`.

Preferred candidate language:

Candidate language only. Not yet operative. Subject to owner decision and separate amendment authorization.

```text
`assessed_not_met`: the obligation was required and attempted, and the available
capture is sufficient to assess that the obligation was not satisfied. The
failure reason must be visible.
```

Rejected alias:

- Do not add `insufficient` as the canonical state unless the owner explicitly prefers it. `insufficient` can be confused with downstream usefulness or Judgment sufficiency; `assessed_not_met` ties the state to capture-owned obligation discharge.

What this fixes:

It keeps a visible failed capture obligation from being softened into `partial` or misclassified as a boundary `blocked` state.

What this must not authorize:

- importing Judgment conclusions about decision support;
- treating downstream unusability as a Capture failure when Capture obligations were actually met;
- turning ECR receipt absence into an ECR schema design problem.

Owner decision needed:

Accept, revise, or reject `assessed_not_met` as a candidate discharge state.

## PCP-03: `access_failed` Versus Boundary `blocked`

Current contract problem:

The current `blocked` state can be overloaded. The pressure test showed cases where access to otherwise in-bound material failed because of tool, host, archive-content, or origin-layer limitations. That is different from a project/source-boundary hard stop.

Pressure-test signal:

- Slot 1 surfaced paraphrase instead of verbatim source observable and archive-content tool block.
- Slot 2 surfaced Teal 403 blocks and archive-content tool block.
- The synthesis states that using `blocked` for a 403 would corrupt later classification because `blocked` was reserved for source-boundary or out-of-bounds access.

Preferred candidate language:

Candidate language only. Not yet operative. Subject to owner decision and separate amendment authorization.

```text
`access_failed`: the source material appears within the allowed Orca source
access boundary, and capture attempted access, but the capture method, tool,
host, archive, or origin failed to return the needed observable. The failed
path, fallback path if any, and visible limitation must be recorded.
```

Boundary clarification for `blocked`:

```text
`blocked` remains reserved for obligations that cannot be satisfied under the
allowed Orca boundary, including source boundary limits, project boundary
limits, or hard-stop exclusions. It must not be used as the generic label for
ordinary tool, host, origin, archive-content, or method failure against
otherwise in-bound material.
```

Sequencing note:

This candidate should travel to a contract amendment only after or in coordination with the source-access method-plan patch, so Obligation #2 prose and `access_failed` vocabulary reference a consistent operative boundary standard. "Within the allowed Orca source access boundary" means the operative boundary at the time of amendment. The hard-stop exclusions below remain operative regardless of how the boundary definition is later worded.

What this fixes:

It keeps operators from confusing "we cannot use this path because it is out of bounds" with "we are allowed to seek this observable, but the current capture method failed."

What this must not authorize:

- no-entitlement payment/access gate bypass;
- nonconsensual sessions;
- stolen credentials or cookies;
- security exploits, malware, or credential stuffing;
- obvious cross-account/private/admin spillover once noticed;
- source acquisition Orca would refuse to disclose internally.

Owner decision needed:

Accept, revise, or reject `access_failed` as a candidate state and the narrowed `blocked` clarification.

## PCP-04: Obligation #16 Handoff Readiness Versus Actual ECR Receipt

Current contract problem:

Obligation #16 currently blends capture-owned handoff sufficiency with the actual ECR receipt or handoff act. That made Slot 1 treat #16 as impossible in phase because no ECR receiver existed, while Slot 2 assessed #16 and judged it insufficient.

Pressure-test signal:

- Slot 1 treated #16 as impossible in phase because no ECR receiver existed, but the real issue was handoff readiness.
- Slot 2 assessed #16 and judged the handoff insufficient, producing a visible blocker.
- Slot 3 completed a bounded first-pass categorical handoff with limitations.

Preferred candidate language:

Candidate language only. Not yet operative. Subject to owner decision and separate amendment authorization.

```text
### 16. Categorical Handoff Readiness

Capture must make enough categorical context available for ECR, Cleaning, and
Judgment to proceed without recollecting source history.

This obligation assesses Capture-owned handoff readiness. It does not require
that ECR has already receipted the material, and it does not define ECR fields,
keys, IDs, tables, data types, receipt structures, storage, schema, or file
formats.
```

Candidate minimum handoff accomplishments to retain or clarify:

- captured signal is inspectable;
- raw observable and related context are preserved or limitations are visible;
- source claim remains separate from Orca interpretation;
- source identity, actor category, timing, modality, visibility, cutoff, archive/history, and recapture posture are visible where knowable;
- source-slice relationships remain visible when archive/history or recapture states differ, including original locator, historical/archive/cache locator, current or migrated locator, fallback path, failed access attempt, changed source state, supersede/supplement/conflict relationship, and the relevant source-slice level where knowable;
- bundled-offer structure and visible packaging cues are preserved when relevant;
- capture obligations and limitations are visible;
- Cleaning can proceed without reconstructing collection history;
- Judgment can inspect capture limits without Capture making judgment calls.

Retention note:

This proposal does not intentionally drop the current Obligation #16 archive/locator specificity. Any later contract amendment must either retain that detail in the Capture-owned handoff-readiness side or explicitly allocate it between Capture-owned readiness and downstream ECR receipt.

What this fixes:

It lets Capture assess and prepare handoff readiness even when no actual ECR receiver is executing in the current artifact, while still allowing `assessed_not_met` when the handoff surface is visibly insufficient.

What this must not authorize:

- ECR schema design;
- actual ECR receipt mechanics;
- storage or table design;
- Cleaning transformation rules;
- Judgment use, exclusion, or discounting rules.

Owner decision needed:

Accept, revise, or reject the #16 rename/split as a future contract amendment.

## PCP-05: Obligation #6 Raw Observable Fidelity Split

Current contract problem:

Obligation #6 requires raw observable preservation but does not distinguish which aspect of the observable is preserved. The pressure test showed that preserving extracted facts is not the same as preserving source wording, layout, modality, or source-visible structure.

Pressure-test signal:

- Slot 1 preserved pricing facts but not faithful source wording, layout, emphasis, table placement, nesting, proximity, or packaging cues.
- Slot 2 preserved no verbatim observable under full content block.
- Slot 3 preserved Reddit raw JSON, screenshots, and projected rows, while WSO remained pointer-level without local raw HTML or screenshot corpus.

Preferred candidate language:

Candidate language only. Not yet operative. Subject to owner decision and separate amendment authorization.

```text
### 6. Raw Observable Fidelity

Capture must preserve the raw observable enough for downstream inspection.
Capture should make visible which fidelity dimensions were preserved, limited,
not applicable, not attempted, access-failed, or unable to be assessed when
those dimensions are relevant to the Decision Frame or were visibly encountered
during capture.

Relevant fidelity dimensions include:

- fact or content-claim preservation;
- source-language preservation;
- visible-structure preservation, including layout, headings, tables, nesting,
  ordering, grouping, proximity, emphasis, and packaging cues where material;
- modality preservation, including screenshots, images, gallery/media state,
  page chrome, audio, video, dynamic rendering, or interaction state where
  material;
- frame-keyed fidelity context, meaning the fidelity dimensions the Decision
  Frame caused Capture to seek, preserve, limit, or fail to preserve. Capture
  reports fidelity state by dimension; downstream Judgment decides which
  dimensions are decision-material.

Capture may add context notes, but it must not replace the observable with
interpretation.
```

What this fixes:

It prevents a capture from passing as "raw observable preserved" merely because a fact row or paraphrase exists.

What this must not authorize:

- Cleaning normalization;
- semantic summarization as a replacement for source observables;
- Judgment discounting or credibility conclusions;
- Capture deciding which fidelity dimensions are decision-material;
- a universal requirement to screenshot every source regardless of Decision Frame materiality.

Owner decision needed:

Accept, revise, or reject the #6 fidelity split.

## PCP-06: Checker Token Glossary

Current contract problem:

Checker tokens can sound like discharge states, validation outcomes, or closure claims. `capture_closure_blocker` was especially risky because it can be confused with `blocked` or a mandatory rerun directive.

Pressure-test signal:

- Slot 1 and Slot 2 used `capture_closure_blocker`.
- Slot 3 used `visible_capture_limitation`.
- The synthesis warned that checker behavior is useful but uneven and not validation.

Preferred candidate language:

Candidate language only. Not yet operative. Subject to owner decision and separate amendment authorization.

```text
Checker vocabulary, when used in pressure-test or review artifacts, must carry
explicit glosses:

- `capture_closure_blocker`: a checker-visible reason the capture artifact
  should not be treated as cleanly closed under the current contract posture.
  It is not the discharge state `blocked`, not validation failure, and not a
  mandatory rerun command by itself.
- `visible_capture_limitation`: a checker-visible limitation that must remain
  visible to downstream layers. It is not proof that capture is adequate.
- `vocabulary_divergence`: a checker-visible mismatch between contract
  vocabulary and artifact language that is not clearly labeled as a proposal.
- `vocabulary_consistent`: checker-visible contract vocabulary appears
  consistent for the checked surface. It is not capture adequacy, validation,
  readiness, approval, source adequacy, or proof.
```

What this fixes:

It reduces fake-pass and fake-fail risk from checker labels being read as contract discharge or validation.

What this must not authorize:

- treating checker output as approval;
- treating checker output as validation or readiness;
- treating checker output as source adequacy;
- treating model agreement as source-of-truth promotion.

Owner decision needed:

Accept, revise, or reject mandatory checker-token glosses in future pressure-test artifacts.

## PCP-07: Pass-2 Vocabulary Consistency Checker

Current contract problem:

The pressure test found useful signal from pass-2 vocabulary-consistency checking, but the batch did not prove pass 2 should become permanent contract doctrine.

Pressure-test signal:

- Slot 1 pass 2 found a look-alike vocabulary/prose issue while preserving labeled proposals as proposals.
- Slot 2 pass 2 treated out-of-contract values as labeled proposals, not hidden divergences.
- Slot 3 checker posture was not fully equivalent for WSO because it was artifact-internal rather than a separate manual GPT-5.5 invocation.

Preferred candidate language:

Candidate language only. Not yet operative. Subject to owner decision and separate amendment authorization.

```text
During pressure-test patching, a second vocabulary-consistency check may be
used to distinguish unlabeled vocabulary drift from clearly labeled proposal
language. The check may expose contract-language pressure. It must not certify
capture quality, source adequacy, validation, readiness, approval, or handoff
sufficiency.
```

Disposition:

Do not make pass 2 required in the controlling contract from this batch alone. Carry it as optional or pressure-test-specific until a later owner decision makes it required, retires it, or moves it to a separate checker operating model.

Owner decision needed:

Choose whether pass 2 remains optional, becomes required for future pressure tests, or is retired. This menu is surfaced here for the first time: the accepted patch plan authorized raising the checker operating-model question, but the owner has not yet been asked to choose among these options.

## PCP-08: Checker Invocation Comparability

Current contract problem:

The batch compared checker results that were not fully equivalent. Separate checker invocation, artifact-internal self-check, and missing checker pass should not be collapsed.

Pressure-test signal:

- Slot 1 and Slot 2 used explicit pass-1 / pass-2 checker posture.
- Slot 3 WSO checker posture was artifact-internal, not equivalent to a separate manual GPT-5.5 checker invocation.
- The owner decision accepts COMR-03 only as a checker-comparability planning question.

Preferred candidate language:

Candidate language only. Not yet operative. Subject to owner decision and separate amendment authorization.

```text
Pressure-test artifacts that use checker language should disclose checker
posture categorically: separate checker invocation, artifact-internal
self-check, or missing checker pass. This posture supports comparability only.
It must not become a quality rank, validation rule, approval rule, readiness
rule, or model-agreement rule.
```

What this fixes:

It prevents future synthesis from treating uneven checker surfaces as equivalent evidence.

What this must not authorize:

- requiring a specific model;
- requiring checker invocation count as proof;
- treating separate checker agreement as validation;
- using checker posture to override source evidence.

Owner decision needed:

Accept, revise, or reject checker invocation comparability language.

## Patch Disposition Queue

| ID | Candidate | Proposal disposition | Review focus |
| --- | --- | --- | --- |
| PCP-01 | `cannot_assess` | Carry into future contract amendment proposal unless review finds a narrower obligation rewrite is safer. | Ensure it cannot become permission to skip capture. |
| PCP-02 | `assessed_not_met` | Carry into future contract amendment proposal as preferred label over `insufficient`. | Ensure it stays capture-owned and not Judgment sufficiency. |
| PCP-03 | `access_failed` plus narrowed `blocked` | Carry into future contract amendment proposal and cross-check against source-access method plan. | Ensure it preserves hard stops and does not widen access. |
| PCP-04 | #16 handoff-readiness split | Carry into future contract amendment proposal while retaining current archive/locator specificity unless the owner explicitly reallocates it. | Ensure it does not define ECR receipt schema or silently weaken current handoff detail. |
| PCP-05 | #6 fidelity split | Carry into future contract amendment proposal with explicit Judgment-owned materiality boundary. | Ensure it is frame-keyed and not universal screenshot/media bloat or Capture-owned materiality. |
| PCP-06 | checker token glossary | Carry into future contract or pressure-test operating language proposal. | Ensure tokens are not validation/readiness claims. |
| PCP-07 | pass-2 vocabulary checker | Defer required/optional/retire decision to owner review; keep optional in proposal. | Ensure one batch does not over-harden checker doctrine. |
| PCP-08 | checker invocation comparability | Carry as comparability disclosure only. | Ensure it does not become model-agreement authority. |

## Next Gate

Recommended next gate: bounded amendment scoping or direct bounded docs-only amendment drafting against `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`, using the owner decision as the scope authority.

No PCP item becomes an actual obligation-contract amendment without a separate explicit amendment authorization.

## Validation Readback

Authoring-time validation for this proposal should include:

- full file readback after edits;
- targeted anchor search for PCP-01 through PCP-08, `Status`, `Proposal Boundary`, `Patch Disposition Queue`, `Next Gate`, `Non-Claims`, and `Direction Change Propagation`;
- claim-safety search for hardening, amendment, runtime, tooling, ECR, Cleaning, Judgment, validation, readiness, approval, proof, buyer-proof, and commercial-readiness overclaims;
- `git diff --check` on touched files.

This is authoring hygiene only. It is not validation, readiness, approval, source-of-truth promotion, proof, or contract acceptance.

Validation execution receipt:

- full file readback: completed after proposal patching;
- targeted anchor search: completed after patching; required anchors for status, proposal boundary, PCP-01 through PCP-08, disposition, next gate, non-claims, and propagation were present;
- adversarial-review patch response: completed for AR-01, AR-02, AR-03, AR-04, AR-05, and AR-06 in this revision;
- navigation anchor search: completed; source-loading and repo-map point to this proposal;
- stale-language search: completed; only expected self-reference appeared inside the recorded search string;
- claim-safety search: completed; expected matches were boundary, non-claim, proposal, next-gate, or recorded-search contexts only;
- `git diff --check`: run on touched files; no whitespace errors; existing LF/CRLF warnings appeared for source-loading and repo-map only.

## Non-Claims

This proposal is not validation, readiness, approval, source-of-truth promotion, final contract hardening, obligation-contract amendment, source-access method plan amendment, runtime authorization, tooling authorization, source-system authorization, schema authorization, ECR design, Cleaning implementation, Judgment design, buyer proof, commercial-readiness evidence, pressure-test discharge, or authorization to run another pressure-test batch.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "A docs-only obligation-contract patch proposal was patched after adversarial review and then consumed by an owner decision accepting PCP-01 through PCP-08 for later bounded amendment drafting, without amending the controlling obligation contract."
  trigger: lifecycle_boundary
  controlling_sources_updated:
    - docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md
    - docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md
    - docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md
    - docs/product/data_capture_spine_post_batch_patch_plan_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/product/data_capture_source_access_method_plan_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: "The workspace rule already permits bounded docs/decision work and still requires explicit authorization for implementation/runtime work; this proposal does not change that rule."
    - path: CLAUDE.md
      reason: "The shim remains subordinate to AGENTS.md and the Orca overlay; no Claude-specific instruction changed."
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: "The source hierarchy and propagation contract did not change; this proposal applies the existing propagation contract."
    - path: docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md
      reason: "The owner decision already authorizes this docs-only proposal draft; this proposal does not revise that decision."
    - path: docs/product/data_capture_spine_post_batch_patch_plan_v0.md
      reason: "The patch plan remains the accepted planning basis; this proposal consumes its contract-facing candidates without changing it."
    - path: docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
      reason: "This artifact proposes candidate contract language but does not apply or harden it."
    - path: docs/product/data_capture_source_access_method_plan_v0.md
      reason: "Source-access method refinements remain a separate later proposal; this artifact does not amend the method plan."
  stale_language_search: "rg -n \"contract hardening now authorized|runtime/source-system implementation now authorized|source-access implementation now authorized|ECR schema now authorized|Cleaning implementation now authorized|Judgment rules now authorized|validation-ready|ready for implementation|amends the controlling obligation contract|supersedes the controlling obligation contract|Recommended next gate: owner decision|current docs-only owner-decision input\" docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not final contract hardening"
    - "not runtime authorization"
    - "not implementation authorization"
```
