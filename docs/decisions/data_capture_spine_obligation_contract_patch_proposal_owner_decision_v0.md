# Data Capture Spine Obligation Contract Patch Proposal Owner Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Owner decision accepting the patched Data Capture Spine obligation-contract patch proposal as bounded authority for a later obligation-contract amendment draft.
use_when:
  - Checking whether PCP-01 through PCP-08 were accepted, narrowed, deferred, or rejected.
  - Scoping a later amendment to the Data Capture Spine obligation contract.
  - Confirming whether this decision authorizes runtime/source-system work, source-access method-plan amendment, ECR design, Cleaning implementation, or Judgment design.
authority_boundary: retrieval_only
open_next:
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_method_plan_v0.md
  - docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md
stale_if:
  - The patched obligation-contract patch proposal is materially revised.
  - A later owner decision supersedes this decision.
  - The controlling obligation contract is amended in response to this decision.
  - The source-access method plan is amended in a way that changes PCP-03 sequencing.
```

## Status And Decision

Status: `ACCEPTED_OBLIGATION_CONTRACT_PATCH_PROPOSAL_FOR_AMENDMENT_DRAFTING_V0`.

Owner decision: `ACCEPT_PCP_PACKAGE_FOR_OBLIGATION_CONTRACT_AMENDMENT_DRAFTING`.

The patched obligation-contract patch proposal is accepted as bounded authority for a later docs-only amendment draft to `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`.

This decision accepts PCP-01 through PCP-08 for amendment drafting with the constraints below. It does not itself amend or harden the obligation contract, amend the source-access method plan, authorize runtime/source-system work, authorize ECR/Cleaning/Judgment design, or validate the Data Capture Spine.

## Source Basis

Decision inputs:

- Current owner instruction: "pcp01 - yes"; "2 - yes"; "4 - agree"; "5 - great then"; "6- yes"; "7 - yes i think thats okay especially for immature program"; "8 - yes"; and "i guess we can just use source then."
- `docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md`, status `OBLIGATION_CONTRACT_PATCH_PROPOSAL_PATCHED_AFTER_ADVERSARIAL_REVIEW_V0`.
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md`, recommendation `safe_for_owner_consideration_after_minor_patch`, with targeted findings patched in the proposal.
- `docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md`, which authorized downstream docs-only obligation-contract patch proposal drafting but not direct contract hardening.
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`, the controlling contract to be amended later.

## Accepted PCP Decisions

### PCP-01: `cannot_assess`

Accepted for amendment drafting.

The amendment draft should add `cannot_assess` as the preferred discharge state for required, attempted obligations where the captured observable is not faithful, complete, or inspectable enough to assess whether the obligation was satisfied.

Constraint: this must not become permission to skip capture attempts, hide unavailable raw material, convert weak capture into downstream admissibility, or let Capture decide credibility, usefulness, exclusion, discounting, Decision Strength, or Action Ceiling.

### PCP-02: `assessed_not_met`

Accepted for amendment drafting.

The amendment draft should add `assessed_not_met` as the preferred discharge state for required, attempted obligations where the available capture is sufficient to assess that the obligation was not satisfied.

Constraint: this must stay capture-owned and must not import Judgment sufficiency, downstream usefulness, or ECR schema conclusions.

### PCP-03: `access_failed` Versus Boundary `blocked`

Accepted for amendment drafting with sequencing constraint.

The amendment draft should add `access_failed` as the preferred state for otherwise in-bound source access attempts where the method, tool, host, archive, or origin failed to return the needed observable. The draft should also narrow `blocked` so it remains reserved for source boundary, project boundary, or hard-stop exclusions.

Terminology decision: keep `source` language. Do not replace it wholesale with `target`. When the amendment needs more precision, it may distinguish source, locator, observable, and capture attempt, but it should not introduce a new global terminology layer merely to avoid the word `source`.

Sequencing constraint: PCP-03 should be applied to the obligation contract only after or in coordination with the source-access method-plan patch, so Obligation #2 prose and `access_failed` vocabulary reference a consistent operative boundary standard. Hard-stop exclusions remain operative regardless of later boundary wording.

Constraint: this must not authorize no-entitlement payment/access gate bypass, nonconsensual sessions, stolen credentials or cookies, security exploits, malware, credential stuffing, obvious cross-account/private/admin spillover once noticed, or source acquisition Orca would refuse to disclose internally.

### PCP-04: Obligation #16 Categorical Handoff Readiness

Accepted for amendment drafting.

The amendment draft should split Capture-owned handoff readiness from actual downstream ECR receipt. Capture may satisfy handoff readiness when enough categorical context is available for ECR, Cleaning, and Judgment to proceed without recollecting source history, even if ECR has not yet receipted the material.

Constraint: retain the current archive/locator and source-slice specificity unless a later owner decision explicitly reallocates it. The draft must preserve visibility of original locator, historical/archive/cache locator, current or migrated locator, fallback path, failed access attempt, changed source state, supersede/supplement/conflict relationship, and relevant source-slice level where knowable.

Constraint: this must not define ECR fields, keys, IDs, tables, data types, receipt structures, storage, schema, or file formats.

### PCP-05: Obligation #6 Raw Observable Fidelity

Accepted for amendment drafting.

The amendment draft should split raw-observable preservation into the smallest complete fidelity dimensions: fact/content preservation, source-language preservation, visible-structure preservation, modality preservation, and frame-keyed fidelity context.

Decision rationale: this split is complete enough to prevent paraphrase or fact-row capture from masquerading as raw observable preservation, while avoiding universal screenshot/media bloat.

Constraint: Capture reports what fidelity dimensions it preserved, limited, did not attempt, could not access, or could not assess. Downstream Judgment decides which dimensions are decision-material. Capture must not make decision-materiality, credibility, exclusion, discounting, Decision Strength, or Action Ceiling calls.

### PCP-06: Checker Token Glossary

Accepted for amendment drafting.

The amendment draft should add or route checker-token glossary language so checker vocabulary cannot be misread as discharge states, validation outcomes, approval, readiness, source adequacy, or proof.

Constraint: checker output must remain review/checking signal only. It must not become source-of-truth promotion or model-agreement authority.

### PCP-07: Pass-2 Vocabulary Consistency Checker

Accepted for amendment drafting as immature-program discipline, not permanent validation doctrine.

The amendment draft may keep pass-2 vocabulary-consistency checking optional or pressure-test-specific unless the owner later chooses to make it required. The immediate accepted direction is that pass 2 is useful for an immature program because it exposes unlabeled vocabulary drift and proposal/operative-language confusion.

Constraint: one N=3 batch does not prove pass 2 should become permanent contract doctrine. Pass 2 must not certify capture quality, source adequacy, validation, readiness, approval, or handoff sufficiency.

### PCP-08: Checker Invocation Comparability

Accepted for amendment drafting.

The amendment draft should require pressure-test or checker-bearing artifacts to disclose checker posture categorically when relevant: separate checker invocation, artifact-internal self-check, or missing checker pass.

Constraint: checker posture supports comparability only. It must not become a quality rank, validation rule, approval rule, readiness rule, model-agreement rule, or proof of source adequacy.

## Authorized Next Work

This decision authorizes a later bounded docs-only amendment draft for `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` that applies the accepted PCP decisions above.

The amendment draft may:

- rewrite obligation-contract discharge vocabulary to add `cannot_assess`, `assessed_not_met`, and `access_failed`;
- clarify `blocked`;
- split Obligation #16 into Capture-owned handoff readiness without defining ECR receipt schema;
- split Obligation #6 into raw-observable fidelity dimensions without assigning materiality to Capture;
- add checker glossary and checker comparability language where it belongs in the obligation contract or pressure-test operating language.

The amendment draft must preserve PCP-03 sequencing with the source-access method-plan patch. If the contract amendment would make Obligation #2 and `access_failed` inconsistent, stop and route the source-access method-plan patch first or in the same bounded docs-only patch lane.

## Deferred Or Rejected Moves

Still deferred:

- applying the obligation-contract amendment in this owner-decision artifact;
- applying or hardening a source-access method-plan patch;
- resolving all future source-access method planning;
- making pass-2 vocabulary checking permanent validation doctrine;
- treating checker output, checker agreement, or checker posture as validation, approval, readiness, proof, source adequacy, or model authority;
- running another pressure-test batch;
- runtime/source-system work, scrapers, APIs, dashboards, storage, schemas, tests, packages, deployment, commits, pushes, or PRs;
- ECR design, Cleaning implementation, Judgment rules, buyer proof, or commercial-readiness claims.

## Next Gate

The next gate is amendment scoping or direct bounded docs-only amendment drafting for the controlling obligation contract.

Recommended sequencing:

1. Scope the actual obligation-contract amendment against the accepted PCP decisions.
2. Apply the amendment only in a separately authorized docs-only patch turn or accepted handoff.
3. Run adversarial review or targeted recheck after the controlling contract is patched, because that is the step where proposal language becomes operative doctrine.

## Non-Claims

This decision is not validation, readiness, source-of-truth promotion, final contract hardening, obligation-contract amendment, source-access method plan amendment, runtime authorization, tooling authorization, source-system authorization, schema authorization, ECR design, Cleaning implementation, Judgment design, buyer proof, commercial-readiness evidence, pressure-test discharge, or authorization to run another pressure-test batch.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "The owner accepted PCP-01 through PCP-08 from the patched obligation-contract patch proposal as bounded authority for a later obligation-contract amendment draft, without amending the controlling contract in this artifact."
  trigger: lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md
    - docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md
    - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md
    - docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md
    - docs/product/data_capture_spine_post_batch_patch_plan_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/product/data_capture_source_access_method_plan_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: "The workspace rule already permits bounded docs/decision work and still requires explicit authorization for implementation/runtime work; this decision does not change that rule."
    - path: CLAUDE.md
      reason: "The shim remains subordinate to AGENTS.md and the Orca overlay; no Claude-specific instruction changed."
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: "The source hierarchy and propagation contract did not change; this decision applies the existing propagation contract."
    - path: docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_obligation_contract_patch_proposal_adversarial_artifact_review_v0.md
      reason: "The review report remains historical input for the pre-decision proposal state; this decision records the owner gate after targeted patching."
    - path: docs/decisions/data_capture_spine_post_batch_patch_plan_owner_decision_v0.md
      reason: "The prior owner decision remains the authority for proposal drafting; this decision consumes the resulting proposal without revising that earlier gate."
    - path: docs/product/data_capture_spine_post_batch_patch_plan_v0.md
      reason: "The patch plan remains the accepted planning basis; this decision records acceptance of the downstream obligation-contract proposal."
    - path: docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
      reason: "This decision authorizes later bounded amendment drafting but does not itself apply or harden contract changes."
    - path: docs/product/data_capture_source_access_method_plan_v0.md
      reason: "PCP-03 sequencing with the method plan is recorded, but this decision does not amend the method plan."
  stale_language_search: "rg -n \"current docs-only owner-decision input|owner decision on which PCP items|Recommended next gate: owner decision|OBLIGATION_CONTRACT_PATCH_PROPOSAL_PATCHED_AFTER_ADVERSARIAL_REVIEW_V0|contract hardening now authorized|runtime/source-system implementation now authorized|source-access implementation now authorized|validation-ready|ready for implementation\" docs/decisions/data_capture_spine_obligation_contract_patch_proposal_owner_decision_v0.md docs/product/data_capture_spine_obligation_contract_patch_proposal_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not final contract hardening"
    - "not runtime authorization"
    - "not implementation authorization"
```
