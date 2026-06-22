# Data Capture Spine Intake Surface Consolidation v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture consolidation capsule
scope: Consolidates the pre-Judgment Data Capture intake surface across raw capture, optional Mechanical Source Projection, categorical ECR receipt, and Cleaning handoff.
use_when:
  - Preparing bounded Data Capture pressure-test planning.
  - Checking the pre-contract Capture to ECR to Cleaning intake boundary.
  - Avoiding drift from Mechanical Source Projection into Cleaning, ECR schema, Judgment, or runtime/tooling design.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md
  - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_commissioning_plan_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_execution_authorization_v0.md
stale_if:
  - A later owner decision rejects, narrows, or supersedes this intake-surface consolidation.
  - The Data Capture obligation contract, Data Capture/Cleaning boundary, v2 operating model, or v2 acceptance decision is materially amended.
  - Pressure-test evidence fires v2's Stop Conditions And Re-Architecture Triggers.
```

## Status

Status: `ACCEPTED_AS_BOUNDED_PRESSURE_TEST_TARGET_V0`.

Owner decision recorded 2026-05-30:

```text
Owner decision: ACCEPT_PROPOSED_CONSOLIDATION_AS_PRESSURE_TEST_TARGET.

This consolidation is accepted as the bounded target for the next Data Capture
pressure-test gate. It is accepted only as a pre-contract intake-surface target,
not as a final Capture Spine contract, not as pressure-test validation, and not
as acceptance of ECR, Cleaning, Judgment, runtime, tooling, source-system,
schema, or implementation design.
```

This artifact is a bounded consolidation capsule and decision/dependency register. It is not a final Capture Spine contract, not a pressure-test result, and not acceptance of ECR, Cleaning, Judgment, runtime, tooling, source-system, schema, or implementation design.

## Source Surface

Controlling sources:

- `docs/product/data_capture_harness_operating_model_architecture_v2.md`
- `docs/product/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`
- `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`

Support sources:

- `docs/product/data_capture_spine_lane_product_thesis_v0.md`
- `docs/product/data_capture_obligation_baseline_decision_v0.md`
- `docs/product/data_capture_harness_product_goal_direction_signal_decision_v0.md`
- `docs/product/data_capture_source_access_boundary_decision_v0.md`
- `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md`
- `docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md`
- `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md`

Operational prompt surface, not doctrine:

- `docs/prompts/data_capture_pressure_test_reddit_mechanical_source_projection_worker_prompt_v0.md`

Excluded by design:

- commercial/product-proof docs;
- research corpus and source-discovery artifacts;
- `_inbox` captures and generated source-projection outputs;
- source-access method plans unless source-access mechanics are the contested issue;
- ECR schema work, Cleaning implementation work, Judgment design, runtime plans, source-system plans, scrapers, APIs, storage, dashboards, and tests.

## Pre-Judgment Intake Surface

The bounded intake surface is:

```text
Decision Frame -> Raw Capture -> optional Data Capture Projection Packet -> categorical ECR receipt -> Cleaning handoff
```

Data Capture owns acquisition, preservation, source visibility, timing, cutoff/archive posture, source identity, capture mode disclosure, failures/blockers, optional Mechanical Source Projection, projection receipt warnings, and categorical handoff sufficiency.

Data Capture must not own credibility, integrity classification, discounting, exclusion, Signal Use, Decision Strength, Action Ceiling, semantic dedupe, Cleaning transformations, source maps as core architecture, runtime implementation, or final ECR field architecture.

## Mechanical Source Projection Rule

Mechanical Source Projection is a Data Capture-owned helper. It is not Cleaning, not ECR schema, not Judgment, and not a standalone spine layer.

When raw source is too transport-heavy for later inspection, Data Capture may create a Data Capture Projection Packet consisting of:

- preserved raw source;
- source-projected mechanical rows or equivalent inspectable source view;
- projection receipt warnings.

Projection may remove source-envelope noise from the working view, such as API transport wrappers, UI chrome, report fields, award/embed scaffolding, client-voting scaffolding, and other non-evidence source envelope fields.

Projection must not remove evidence rows because they look low-value, repetitive, deleted, bot-like, low-score, embarrassing, or unhelpful. Warnings, counts, omissions, missing-continuation markers, and raw-reference pointers may be recorded, but they do not certify Cleaning, normalization, credibility, relevance, or downstream use.

## ECR Receipt Boundary

ECR receipts the captured source or projection packet categorically before Cleaning.

This capsule may say ECR needs enough receipt context to reference:

- raw observation;
- projection packet where used;
- provenance, timing, and capture context;
- inspectability and preservation posture;
- handoff state and visible blockers.

This capsule must not define ECR fields, keys, IDs, storage, schema, table shape, file format, runtime receipt mechanism, or normalization certification.

## Cleaning Handoff Boundary

Cleaning begins after ECR receipt.

Cleaning may verify raw-to-projected traceability where a projection packet exists and may record non-destructive transformation history: normalization, translation, summarization, dedupe, clustering, and raw-to-cleaned traceability.

Any effect on independence, credibility, uncertainty, exclusion, discounting, Decision Strength, or Action Ceiling belongs to Judgment, not Cleaning.

## Open Owner Decisions And Candidate Open Knobs

This artifact does not close the open stack. It carries these items forward for owner decision, pressure-test evidence, or later bounded follow-up:

- whether Evidence Candidate Record is the final canonical name or a working name;
- how Capture handoff obligations become ECR receipt fields without turning Capture into ECR schema;
- how Data Capture Projection Packet references are receipted without turning ECR into projection schema;
- where ECR draws the line between related-chain context and irrelevant source exhaust;
- whether Snapshot Integrity Class belongs in Capture, ECR, or later Judgment/ECR consolidation;
- which source families require archive attempts versus recorded archive/history posture;
- which source families require human-led capture by default until the engine is trained and checked;
- minimum agent-assisted logging that is useful without creating source-log bloat;
- recapture thresholds for meaningful source change without churn;
- when, if ever, runtime/source-system Data Capture planning becomes authorized.

## Pressure-Test Dependency

The contract surface must not be hardened from abstract reasoning alone. Real commissioned pressure tests remain the dependency for deciding whether the intake surface holds, needs patching, or exposes re-architecture triggers.

Pressure-test evidence should adjudicate:

- whether Capture stays out of ECR, Cleaning, and Judgment;
- whether projection packets preserve raw/source-row traceability;
- whether categorical ECR handoff is sufficient;
- whether Cleaning can proceed without recollecting source history;
- whether source-family rules should remain satellite or become core.

## Recommended Next Gate

Owner gate status: closed by `ACCEPT_PROPOSED_CONSOLIDATION_AS_PRESSURE_TEST_TARGET`.

Execution gate status: now paired with
`docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md`.

This intake-surface target now routes to the bounded three-slot execution batch
defined by the commissioning plan and execution authorization artifact.

The next move after those captures is pressure-test evidence synthesis rather
than another pre-execution authorization pass.

The next move should not resolve the whole open-decision stack at once, write a
final Capture Spine contract, design ECR schema, design Cleaning
implementation, design Judgment behavior, or authorize runtime/source-system
work.

## Doctrine Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "The intake-surface consolidation is now accepted as the bounded pressure-test target for the next Data Capture gate."
  trigger: architecture_doctrine
  controlling_sources_updated:
    - docs/product/data_capture_spine_intake_surface_consolidation_v0.md
    - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
  intentionally_not_updated:
    - path: docs/product/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md
      reason: "v2 acceptance remains accepted for pressure-test commissioning planning; this consolidation narrows the target surface without amending v2."
    - path: docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
      reason: "The obligation contract remains draft and must not be hardened before pressure-test evidence."
    - path: docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
      reason: "The MSP and layer-boundary doctrine was already patched there; this turn only accepts the consolidation as the pressure-test target."
  stale_language_search: "rg -n \"PROPOSED_CONSOLIDATION_CAPSULE_V0|accept or reject this consolidation|off-narrative|unlikely to matter|thumbnails|CSS flair|EF9CA7F6EAD00584782CC0C58DC2E4E2E31A7F038101C211524F9205DC3D2357\" docs/product/data_capture_spine_intake_surface_consolidation_v0.md docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md | Select-String -NotMatch \"stale_language_search\""
  non_claims:
    - "not validation"
    - "not readiness"
    - "not final contract hardening"
    - "not pressure-test execution authorization"
```

## Non-Claims

This is not validation, readiness, acceptance, pressure-test discharge, source-of-truth promotion, ECR design, Cleaning implementation, Judgment design, runtime authorization, tooling authorization, schema authorization, buyer proof, commercial-readiness evidence, or final contract hardening.
