# Data Capture Spine Pressure-Test Execution Authorization v0

```yaml
retrieval_header_version: 1
artifact_role: Owner decision artifact
scope: Authorizes one bounded batch of three Data Capture pressure-test captures against the accepted intake-surface target and commissioning plan.
use_when:
  - Checking whether the first bounded Data Capture pressure-test batch may be executed.
  - Checking the exact capture boundary for the three authorized pressure-test slots.
  - Routing post-execution synthesis requirements and non-authorized adjacent work.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_intake_surface_consolidation_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_commissioning_plan_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
stale_if:
  - A later owner decision narrows, pauses, or supersedes this execution authorization.
  - The accepted intake-surface target or commissioning plan is materially amended or superseded before the three authorized captures are executed.
  - Pressure-test evidence triggers a pause or re-architecture review that supersedes this batch authorization.
```

## Status And Owner Decision

Status: `AUTHORIZED_BOUNDED_DATA_CAPTURE_PRESSURE_TEST_EXECUTION_V0`.

Owner decision: `AUTHORIZE_BOUNDED_DATA_CAPTURE_PRESSURE_TEST_EXECUTION`.

Bounded pressure-test execution is authorized against the accepted intake-surface
target in `docs/product/data_capture_spine_intake_surface_consolidation_v0.md`
and the batch plan in
`docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md`.

This is not validation, not readiness, not pressure-test discharge, not final
contract hardening, and not runtime/tooling authorization.

## Source Readiness

`SOURCE_CONTEXT_READY`

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 Data Capture intake-surface / execution-authorization pack
  edit_permission: docs-write
  target_scope:
    - docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md
    - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
    - docs/product/data_capture_spine_intake_surface_consolidation_v0.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - docs/product/data_capture_spine_intake_surface_consolidation_v0.md
    - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/product/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md
```

## Authorized Target

Accepted bounded pressure-test target:

- `docs/product/data_capture_spine_intake_surface_consolidation_v0.md`

Authorized batch plan:

- `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md`

Controlling support:

- `docs/product/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md`
- `docs/product/data_capture_harness_operating_model_architecture_v2.md`
- `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`

This authorization is bounded to those sources. It does not authorize a broader
Capture Spine contract, runtime plan, or adjacent system design.

## Authorized Batch

The authorized batch is exactly these three slots:

1. Slot 1: Mergers & Inquisitions pricing/product/bundle posture across a 12-24 month window.
2. Slot 2: Teal public docs/pricing/features/recent change history across ~12 months.
3. Slot 3: Non-target US-domestic candidate forum/review discourse on resume-driven interview-getting pain, primary venues Reddit and Wall Street Oasis, cutoff Q2 2026.

If a slot cannot be captured within boundary, it must record a visible stop or
visible blocker. Capture must not invent, widen, or substitute a frame to keep
the batch count at three.

## Authorized Capture Activities

Authorized activities are limited to:

- human-led source capture inside the current source-access boundary;
- agent-assisted source capture within the current obligation-contract
  allow/forbid line;
- structured access only when it stays discoverable-or-entitled, permits free or
  account-created access, remains disclosable, avoids use of obvious
  cross-account/private/admin spillover once noticed, and avoids hard-stop
  access paths;
- archive/history lookup only when the access path is disclosable and stays
  inside the current source-access boundary;
- Mechanical Source Projection only as a Data Capture-owned projection helper.

This authorization does not extend to runtime systems, automated extraction
builds, source-system planning, or capture tooling beyond bounded public-source
execution of the three named slots.

## Required Per-Capture Output

Each authorized capture must produce the commissioning plan's capture-session
Markdown artifact shape with these sections:

- `Decision Frame`
- `Source Boundary`
- `Capture Mode`
- `Per-Obligation Discharge States` for all 16 obligations
- `Per-Slice Posture`
- `Raw Observable Pointers`
- `Failures, Blockers, and Limitations`
- `Agent-Assistance Context`
- `Categorical Handoff Or Visible Stop`
- `LLM Capture-Visibility Checker Output`

All 16 obligation rows must declare one of `met`, `partial`,
`assessed_not_met`, `cannot_assess`, `access_failed`, `blocked`,
`unavailable_by_source`, `not_applicable`, or `not_attempted`. Blank
obligation cells are forbidden. Every non-`met` obligation state must carry a
visible reason.

## Mechanical Source Projection Boundary

Mechanical Source Projection may remove source-envelope noise from a working
view.

Mechanical Source Projection must not remove evidence rows because they look
low-value, repetitive, deleted, bot-like, low-score, embarrassing, or
unhelpful.

Mechanical Source Projection does not certify Cleaning, normalization,
credibility, relevance, or downstream use.

## Stop And Pause Conditions

Stop or mark blocked when:

- source access requires no-entitlement gate bypass, stolen credentials/cookies,
  nonconsensual sessions, security exploits, malware, credential stuffing,
  use of obvious cross-account/private/admin spillover once noticed,
  private/confidential account areas without consent, methods Orca would refuse
  to disclose internally, or otherwise clearly illegal / morally compromising
  methods;
- the capture cannot preserve enough raw observable context for downstream
  inspection;
- a slot cannot be executed inside the authorized discoverable-or-entitled,
  free/account-created, disclosable, obvious-spillover-avoiding,
  hard-stop-avoiding source boundary.

Pause the batch or route for owner review when:

- Capture drifts into ECR schema, Cleaning, Judgment, source-quality scoring,
  or runtime design;
- repeated same-obligation stop conditions appear across captures.

Carry forward the commissioning plan's threshold logic:

- `1 of 3`: patchable unless the failure is unambiguous and severe in itself;
- `2 of 3`: architecture-threatening signal and pause before further pressure
  tests;
- `3 of 3`: architecture-threatening confirmed and v2 controlling status yields
  per the re-architecture trigger clause.

## Post-Execution Gate

After execution, a pressure-test evidence synthesis is required before the
obligation contract is hardened.

That synthesis must classify findings as `patchable` or
`architecture-threatening`.

No contract hardening, no source-family promotion, and no downstream doctrine
promotion occurs inside this execution authorization.

## Explicit Non-Authorization

This artifact does not authorize:

- runtime or source-system planning;
- scrapers, APIs, dashboards, storage, schemas, tests, packages, deployment,
  commits, pushes, or PRs;
- ECR field design;
- Cleaning implementation;
- Judgment rules;
- buyer proof or commercial-readiness claims;
- a final Capture Spine contract.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: "Pressure-test execution remains authorized for the first bounded three-slot Data Capture batch, and execution surfaces now use the amended obligation contract's nine discharge states and checker vocabulary while adjacent runtime, schema, Cleaning, Judgment, and hardening work remains unauthorized."
  trigger: lifecycle_boundary
  controlling_sources_updated:
    - docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md
    - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
    - docs/prompts/data_capture_spine_pressure_test_llm_capture_visibility_checker_prompt_v0.md
    - docs/product/data_capture_spine_intake_surface_consolidation_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - CLAUDE.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
    - docs/prompts/data_capture_spine_pressure_test_llm_capture_visibility_checker_prompt_v0.md
    - docs/product/data_capture_spine_intake_surface_consolidation_v0.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: "The workspace rule already permits bounded implementation or execution only when the current turn explicitly authorizes it; no Orca instruction text changed."
    - path: CLAUDE.md
      reason: "The shim already routes doctrine-changing work through the overlay and does not encode the prior execution boundary."
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: "The propagation contract and source hierarchy did not change; this turn applies the existing contract."
    - path: docs/product/data_capture_harness_operating_model_architecture_v2_acceptance_decision_v0.md
      reason: "v2 acceptance remains commissioning-planning authority plus re-architecture trigger logic; this turn adds execution authorization in a separate owner-decision artifact rather than amending v2 acceptance scope."
    - path: docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
      reason: "The obligation contract remains draft and pressure-tested, not hardened, by this execution authorization."
  stale_language_search: "rg -n \"The remaining bar before execution is a separate owner authorization to run the 3 captures against this plan\\.|Until that authorization exists|authorize bounded pressure-test execution against this intake surface; or|The next move should be one of:|one of the six allowed values|Allowed states per cell: `met`, `partial`, `blocked`|Raw Observable Preservation|Categorical Handoff Sufficiency|no_visible_capture_blocker_found\" docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md docs/prompts/data_capture_spine_pressure_test_llm_capture_visibility_checker_prompt_v0.md docs/product/data_capture_spine_intake_surface_consolidation_v0.md .agents/workflow-overlay/source-loading.md docs/workflows/orca_repo_map_v0.md | Select-String -NotMatch \"stale_language_search\""
  non_claims:
    - "not validation"
    - "not readiness"
    - "not pressure-test discharge"
    - "not final contract hardening"
    - "not runtime authorization"
```

## Non-Claims

This is not validation, readiness, pressure-test discharge, final contract
hardening, ECR design, Cleaning design, Judgment design, runtime authorization,
tooling authorization, schema authorization, buyer proof, or
commercial-readiness evidence.
