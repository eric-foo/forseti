# Data Capture Spine Source-Observability Scoping Authorization v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Owner authorization for a bounded docs-only source-observability requirements scoping lane after the first all-slot Data Capture pressure-test synthesis.
use_when:
  - Checking whether source-observability requirements scoping is authorized after the first all-slot pressure-test synthesis.
  - Confirming what the next scoping lane may and may not cover.
  - Confirming that tooling, runtime, source-access implementation, contract hardening, ECR, Cleaning, and Judgment work remain out of scope.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_all_slot_synthesis_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_all_slot_synthesis_blast_radius_recheck_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_execution_authorization_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_commissioning_plan_v0.md
stale_if:
  - A later owner decision supersedes this authorization.
  - The all-slot synthesis is materially revised.
  - The blast-radius recheck is materially revised or superseded.
  - The obligation contract, commissioning plan, or execution authorization is materially amended before source-observability scoping begins.
```

## Status And Decision

Status: `AUTHORIZED_SOURCE_OBSERVABILITY_REQUIREMENTS_SCOPING_V0`.

Owner decision: `AUTHORIZE_BOUNDED_DOCS_ONLY_SOURCE_OBSERVABILITY_SCOPING`.

The owner authorizes one bounded docs-only scoping lane to turn the recurring
source-observability pressure surfaced by the first all-slot Data Capture
pressure-test synthesis into explicit requirements and owner-decision inputs.

This decision authorizes scoping only. It does not authorize implementation,
tools, runtime source systems, scrapers, APIs, browser automation, storage,
schemas, dashboards, tests, ECR design, Cleaning implementation, Judgment design,
contract hardening, or source-access method-plan amendment.

## Source Basis

Decision inputs:

- Current owner instruction: "proceed till writing owner authorization artifact".
- `docs/product/data_capture_spine_pressure_test_all_slot_synthesis_v0.md`,
  SHA256 `A0021F1EF42F101C2029FADEDE062461A136D082EF03B7339411BE19270FB0E5`.
- `docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_all_slot_synthesis_blast_radius_recheck_v0.md`,
  SHA256 `46FE71284AA146971719E153AD710FC92C0CB3D455B0BC37BF495924ABFCC68D`,
  recommendation `safe_for_owner_decision_input`.
- `docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md`,
  SHA256 `BCA50C80A7EAA889DC0B01377FFB80635BAC6DDC30F3A4FA654B42CC319CACA3`.
- `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md`,
  SHA256 `3D9AC208A8AF68160A43F3EB3512082BF0F9B10D3840331FE82F544E307820EB`.

The all-slot synthesis classifies the recurring source-observability findings
as `patchable` rather than `architecture-threatening` on the current record. The
blast-radius recheck closes the two major review findings and says the synthesis
is safe for owner decision input.

## Authorized Lane

Authorized lane: bounded docs-only source-observability requirements scoping.

The lane may define requirements, decision questions, and possible future
authorization gates for source-observable capture support. It may compare
requirement alternatives and identify what a later owner would need to decide
before any implementation or contract work begins.

The lane must keep the output at requirements/scoping level. It must not write a
source-access method plan, implementation plan, worker prompt, automation design,
runtime design, schema design, or contract patch.

## Allowed Scoping Targets

The scoping lane may cover only these pressure-test-derived requirement areas:

- verbatim and source-structure preservation;
- archive snapshot body retrieval;
- screenshot-grade, media, or multimodal preservation when layout or media
  carries meaning;
- in-bound public-host access handling for cases like Teal 403;
- source-language anchors from the start for forum or text captures where later
  artifact-internal inspection depends on source language.

The lane may also identify cross-cutting requirement properties for those areas,
such as inspectability, preservation posture, failure visibility, source cutoff,
operator-mode disclosure, and recapture triggers.

## Forbidden Outputs

This authorization does not permit:

- source-access implementation;
- runtime source systems;
- scraper, API, browser automation, crawler, proxy, anti-detect, package,
  deployment, test, storage, dashboard, or database design;
- source-access method-plan amendment;
- Data Capture obligation-contract amendment or hardening;
- ECR field, key, ID, receipt, table, schema, storage, or file-format design;
- Cleaning implementation, normalization rules, clustering rules, dedupe rules,
  or transformation pipelines;
- Judgment rules, credibility rules, exclusion rules, discounting rules, Signal
  Use, Decision Strength, Action Ceiling, or synthesis logic;
- buyer proof, commercial-readiness claims, or production-readiness claims.

## Stop Conditions

The scoping lane must stop and route back to the owner if it encounters any of
these conditions:

- requirements cannot be stated without selecting a concrete tool, runtime,
  scraper, API, browser automation pattern, storage pattern, or package;
- requirements cannot be stated without changing the source-access boundary;
- requirements cannot be stated without amending the Data Capture obligation
  contract or source-access method plan;
- requirements require ECR, Cleaning, or Judgment schema/behavior decisions;
- source-observability pressure starts looking architecture-threatening rather
  than patchable under the commissioning plan's re-architecture trigger logic;
- the lane would need to run new captures, pressure tests, live source access,
  browser sessions, archive retrieval, or implementation experiments.

## Next Gate

The next gate after scoping is an owner decision on what, if anything, the
requirements authorize next.

Possible later owner decisions include:

- authorize implementation scoping for a narrow source-observability support
  slice;
- authorize a source-access method-plan patch proposal;
- authorize a Data Capture obligation-contract patch proposal;
- narrow the requirements and rerun scoping;
- reject or defer implementation/source-access work.

No later gate is pre-selected by this authorization.

## Review Timing

Do not run adversarial review merely because this authorization exists.

Adversarial review is recommended after the docs-only source-observability
scoping artifact is written, before using it to authorize implementation,
runtime/tooling work, source-access method changes, or contract amendments.

Adversarial review should also run earlier if the scoping artifact starts
defining methods, implementation architecture, source-access policy, contract
language, or downstream ECR/Cleaning/Judgment behavior instead of requirements.

## Non-Claims

This decision is not validation, readiness, source-of-truth promotion,
pressure-test discharge, Data Capture Spine acceptance, production adequacy,
contract hardening, obligation-contract amendment, source-access method-plan
amendment, runtime authorization, tooling authorization, source-system
authorization, scraper authorization, API authorization, browser-automation
authorization, schema authorization, ECR design, Cleaning implementation,
Judgment design, buyer proof, or commercial-readiness evidence.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "The owner authorized a bounded docs-only source-observability requirements scoping lane after the all-slot Data Capture pressure-test synthesis, without authorizing implementation, runtime/tooling, contract hardening, or downstream design."
  trigger: lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/data_capture_spine_source_observability_scoping_authorization_v0.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/product/data_capture_spine_pressure_test_all_slot_synthesis_v0.md
    - docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_all_slot_synthesis_blast_radius_recheck_v0.md
    - docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md
    - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: "The workspace rule already requires explicit bounded authorization for implementation/runtime work; this decision applies that rule without changing top-level instructions."
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: "The source hierarchy and propagation contract did not change; this decision applies the existing lifecycle-boundary propagation trigger."
    - path: docs/product/data_capture_spine_pressure_test_all_slot_synthesis_v0.md
      reason: "The synthesis remains the reviewed decision input; this artifact records the owner authorization that follows from it."
    - path: docs/review-outputs/adversarial-artifact-reviews/data_capture_spine_pressure_test_all_slot_synthesis_blast_radius_recheck_v0.md
      reason: "The recheck remains historical review evidence for the patched synthesis; this artifact records the downstream owner decision."
    - path: docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md
      reason: "The original pressure-test execution authorization remains closed; this decision authorizes follow-on docs-only scoping, not a new pressure-test execution."
    - path: docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
      reason: "The commissioning plan remains the source for pressure-test interpretation; this decision does not change its batch shape or trigger logic."
  stale_language_search: "rg -n \"direction_change_propagation[_]blocker|not final propagation closur[e]|runtime/tooling.*authoriz[e]|contract hardening.*authoriz[e]|ECR design.*authoriz[e]|Cleaning implementation.*authoriz[e]|Judgment design.*authoriz[e]|source-access implementation.*authoriz[e]|ready for implementatio[n]|validation[-]ready\" docs/decisions/data_capture_spine_source_observability_scoping_authorization_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md"
  non_claims:
    - "not validation"
    - "not readiness"
    - "not implementation authorization"
    - "not runtime authorization"
    - "not contract hardening"
```
