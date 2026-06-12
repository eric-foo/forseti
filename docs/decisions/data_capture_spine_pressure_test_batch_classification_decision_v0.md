# Data Capture Spine Pressure-Test Batch Classification Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Owner decision artifact
scope: Commissioner classification for the completed first bounded N=3 Data Capture pressure-test batch.
use_when:
  - Checking whether the first Data Capture pressure-test batch classified as patchable or architecture-threatening.
  - Routing post-batch Data Capture obligation-contract, source-access-method, MSP, or checker refinements.
  - Confirming whether re-architecture pause, contract hardening, runtime work, or source-access implementation is authorized.
authority_boundary: retrieval_only
open_next:
  - docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_batch_synthesis_n3of3_adversarial_review_v0.md
  - docs/product/data_capture_spine/data_capture_spine_pressure_test_commissioning_plan_v0.md
  - docs/product/data_capture_spine/data_capture_spine_pressure_test_execution_authorization_v0.md
  - docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - docs/product/data_capture_spine/data_capture_source_access_method_plan_v0.md
stale_if:
  - The N=3 synthesis is materially revised.
  - A later commissioner or owner decision supersedes this classification.
  - The obligation contract, source-access method plan, commissioning plan, or Data Capture boundary is materially revised in response to this decision.
```

## Status And Decision

Status: `CLASSIFIED_PATCHABLE_DATA_CAPTURE_PRESSURE_TEST_BATCH_V0`.

Commissioner decision: `CLASSIFY_BATCH_AS_PATCHABLE_NOT_ARCHITECTURE_THREATENING`.

The first bounded N=3 Data Capture pressure-test batch surfaces **patchable contract, vocabulary, source-access-method, MSP, and checker refinements**. It does **not** trigger a re-architecture pause, architecture-threatening confirmation, v2 status yield, contract hardening, source-family promotion, runtime/source-system work, or ECR/Cleaning/Judgment design.

## Source Basis

Primary decision inputs:

- `docs/research/data_capture_spine_pressure_test_batch_synthesis_n3of3_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_batch_synthesis_n3of3_adversarial_review_v0.md`
- `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md`
- `docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`

The N=3 synthesis was adversarially reviewed and patched before this decision. The decisive reviewed issue was the vocabulary-count question: whether Slot 1 F-C should count with Slot 2's explicit vocabulary break as a 2-of-3 architecture-threatening threshold signal.

## Count Determination

The Slot 1 F-C vocabulary reach is counted as a **patch-planning warning signal**, not as a threshold-crossing explicit contract failure.

Rationale:

- Slot 1 surfaced a real vocabulary strain: the operator reached for `indeterminate` / `cannot_assess` in finding F-C because source-fidelity loss made a fairness ceiling unevaluable.
- Slot 1 did **not** use an out-of-vocabulary state inside the obligation-discharge table; the capture still exposed the limitation using the current artifact form.
- Slot 2 did use explicit out-of-vocabulary discharge values: `cannot_assess` for #6/#12 and `insufficient` for #16.
- Slot 3 stayed inside the existing discharge vocabulary.

Classification result:

- Explicit discharge-vocabulary break: **1 of 3** (Slot 2).
- Related vocabulary strain that must travel into patch planning: **Slot 1 F-C**.
- Threshold result: **patchable**, not architecture-threatening under the commissioning plan's 2-of-3 pause rule.

This does not minimize the Slot 1 signal. It means the first batch shows a vocabulary refinement pattern that the contract can absorb without changing the Data Capture architecture's shape.

## Finding Classification

| Evidence family | Classification | Decision |
| --- | --- | --- |
| Discharge vocabulary pressure | Patchable, high-priority | Carry `cannot_assess` / `indeterminate`, `insufficient` / `assessed_not_met`, and tool-origin block vs boundary `blocked` into obligation-contract patch planning. Do not amend the contract in this decision. |
| Obligation #16 handoff wording | Patchable, high-priority | Carry handoff-readiness vs actual ECR receipt split into patch planning. |
| Obligation #6 source fidelity wording | Patchable, high-priority | Carry fact preservation vs source-language / structure / modality preservation into patch planning. |
| Source-access / fetcher limitations | Patchable source-access-method gap | Authorize docs-only source-access method planning for verbatim/structure capture, archive-content retrieval, screenshot/media preservation, anti-block handling, thread-graph capture, timestamp discipline, and raw-preserving projection. |
| Mechanical Source Projection | Candidate helper, not hardened | Keep MSP as Data Capture-owned helper over preserved raw. Do not promote to final contract obligation from one Reddit data point. |
| Checker behavior | Patchable operating-model refinement | Carry pass-2 vocabulary-consistency checker and checker-token glossary into patch planning. Do not treat checker output as validation or readiness. |
| Capture/ECR/Cleaning/Judgment boundary | Held under stress | No ECR schema, Cleaning transform, Judgment rule, source-quality score, exclusion, discounting, Decision Strength, or Action Ceiling design is authorized. |
| Source-family satellite behavior | Held at synthesis level | Do not promote a source-family rule to core from this batch. |

## Authorized Next Work

This decision authorizes **docs-only patch planning** for the next Data Capture work unit:

1. Obligation-contract patch planning for vocabulary, #16, #6, and checker glossary questions.
2. Source-access method planning refinement under the existing discoverable-or-entitled, disclosable, hard-stop-excluding boundary.
3. Optional prompt or review-prompt preparation for those docs-only planning lanes.

This decision does not authorize applying the obligation-contract patch itself. Proposed contract changes require a separate patch artifact and owner acceptance before the obligation contract is hardened or amended.

This decision does not authorize runtime/source-system implementation, scrapers, APIs, dashboards, storage, schemas, tests, packages, deployment, commits, pushes, PRs, ECR design, Cleaning implementation, Judgment rules, buyer proof, or commercial-readiness claims.

## Deferred Or Rejected Moves

- **Re-architecture pause:** not triggered by this batch.
- **v2 status yield:** not triggered by this batch.
- **Further pressure testing before patch planning:** deferred. Another batch may be useful later, especially for multimodal capture or a second MSP pressure point, but the current evidence is sufficient to plan patches.
- **Contract hardening now:** rejected. The batch supports patch planning, not final hardening.
- **Source-access implementation now:** rejected. The batch supports docs-only method planning, not runtime work.

## Not-Proven Boundaries

- This decision does not prove the Data Capture Spine is validated, ready, complete, or buyer-facing.
- This decision does not prove the source-access methods are feasible or implemented.
- This decision does not prove MSP works outside the Reddit pressure point.
- This decision does not prove pass-2 checker adoption is correct; it only authorizes patch planning.
- This decision does not resolve final ECR, Cleaning, or Judgment boundaries.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "The completed first three-slot Data Capture pressure-test batch is classified as patchable rather than architecture-threatening, authorizing docs-only patch planning while leaving contract hardening and runtime/source-system work unauthorized."
  trigger: lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md
    - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/product/data_capture_source_access_method_plan_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: "The workspace rule already permits bounded docs/decision work and requires explicit authorization for implementation/runtime work; this decision does not change that rule."
    - path: CLAUDE.md
      reason: "The shim remains subordinate to AGENTS.md and the Orca overlay; no Claude-specific instruction changed."
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: "The source hierarchy and propagation contract did not change; this decision applies the existing contract."
    - path: docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md
      reason: "The execution authorization remains historical authority for running the first batch; this decision classifies the post-execution evidence rather than amending that authorization."
    - path: docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
      reason: "The commissioning thresholds and batch shape remain the basis for this classification; no threshold rule changed."
    - path: docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
      reason: "This decision authorizes patch planning but does not directly amend or harden the obligation contract."
    - path: docs/product/data_capture_source_access_method_plan_v0.md
      reason: "This decision authorizes source-access method planning refinement but does not itself change the source-access method plan."
  stale_language_search: "rg -n \"CLASSIFIED_PATCHABLE_DATA_CAPTURE_PRESSURE_TEST_BATCH|architecture-threatening confirmed|v2 controlling status yields|contract hardening now authorized|runtime/source-system implementation now authorized|source-access implementation now authorized\" docs/decisions/data_capture_spine_pressure_test_batch_classification_decision_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md docs/product/data_capture_source_access_method_plan_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not final contract hardening"
    - "not runtime authorization"
    - "not implementation authorization"
```

## Non-Claims

This decision is not validation, readiness, pressure-test discharge in the sense of final contract hardening, Data Capture Spine completion, ECR design, Cleaning design, Judgment design, runtime authorization, source-system authorization, tooling authorization, schema authorization, buyer proof, or commercial-readiness evidence.
