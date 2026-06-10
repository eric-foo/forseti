# Judgment Spine v0.14 Step A Harness Rebuild Handoff Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Fresh-thread implementation handoff for rebuilding the v0.14 deterministic judgment harness and running the quarantined TR/Casetext plumbing fixture.
use_when:
  - Starting Step A implementation in a separate coding thread after owner authorization.
  - Rebuilding the v0.14 deterministic scorer from specs before any fresh judgment-quality case work.
  - Preserving the pre-code review decisions that close schema, fixture, disclaimer, and regression-test ambiguities.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/index.md
  - docs/research/judgment-spine/harness/v0_14/action_band_mapping_table_numbers.md
  - docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md
  - docs/hygiene/precompact_orca_judgment_tr_casetext_ledger_v0.md
stale_if:
  - v0.14 mapping constants, scorer formulas, or schema reference are superseded.
  - The TR/Casetext adjudicated labels or quarantine disposition are reopened.
  - Owner decides to code Canoo/Walmart before Step A plumbing is complete.
```

- Status: STEP_A_HANDOFF_SCOPE_V0
- Output mode of this artifact: file-write durable handoff prompt.
- Output mode this prompt commissions: source-changing implementation, but only after explicit owner authorization in the receiving coding thread.
- Current artifact does not itself authorize implementation, validation success, commits, pushes, installs, external network, or lifecycle actions.

## How To Use

Open this prompt in a fresh coding thread. The owner should explicitly authorize the bounded Step A implementation in that thread before any code or tests are written or run.

If the owner does not explicitly authorize implementation in the receiving thread, the receiver must stop after preflight with `BLOCKED_BY_AUTHORIZATION`.

## Objective

Rebuild the v0.14 deterministic Judgment Spine harness and produce the first real-case plumbing `ScoringResult` using the quarantined TR/Casetext fixture.

This proves only that fixed fixture inputs can flow through schema validation, deterministic mapping, shallow scoring checks, and report/closeout discipline.

Required claim string in any green report, README, generated case report, or chat closeout:

```text
plumbing works only; not judgment quality
```

## Non-Goals

- Do not claim TR/Casetext demonstrates judgment quality.
- Do not relabel TR/Casetext.
- Do not weaken, bypass, or remove quarantine.
- Do not add Canoo/Walmart to this build.
- Do not run LLM contestants.
- Do not build capture, cleaning, dashboards, semantic evidence checking, memory retrieval, rule promotion, or product proof.
- Do not commit, push, install, deploy, fetch external sources, or perform destructive cleanup unless separately and explicitly authorized.

## Required Preflight

1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. Read the narrow overlay pack needed for implementation authority and validation:
   - `.agents/workflow-overlay/source-of-truth.md`
   - `.agents/workflow-overlay/source-loading.md`
   - `.agents/workflow-overlay/safety-rules.md`
   - `.agents/workflow-overlay/validation-gates.md`
   - `.agents/workflow-overlay/artifact-folders.md`
   - `.agents/workflow-overlay/artifact-roles.md`
4. Confirm workspace path: `C:\Users\vmon7\Desktop\projects\orca`.
5. Confirm `orca-harness/` is absent before rebuilding. If it exists, stop and ask the owner whether to inspect, reuse, or remove it.
6. Record an `orca_start_preflight` receipt:

```yaml
orca_start_preflight:
  agents_read:
  overlay_read:
  source_pack: custom S0 + v0.14 harness specs + TR/Casetext checkpoint
  edit_permission: implementation-authorized | read-only
  target_scope: orca-harness/ Step A harness rebuild and TR/Casetext plumbing fixture only
  dirty_state_checked:
  blocked_if_missing: explicit owner authorization in this coding thread
```

## Controlling Sources

Read these before coding:

- `docs/research/judgment-spine/harness/v0_14/index.md`
- `docs/research/judgment-spine/harness/v0_14/phase_1_infrastructure_architecture.md`
- `docs/research/judgment-spine/harness/v0_14/action_band_mapping_table_numbers.md`
- `docs/research/judgment-spine/harness/v0_14/action_band_mapping_executable_spec.md`
- `docs/research/judgment-spine/harness/v0_14/scorer_formula_spec.md`
- `docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md`
- `docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md`
- `docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md`
- `docs/research/judgment-spine/harness/v0_14/blind_judgement_schema_and_harness_protocol.md`
- `docs/research/judgment-spine/harness/v0_14/failure_event_log_spec.md`
- `docs/research/judgment-spine/harness/v0_14/proof_and_memory_plan.md`
- `docs/hygiene/precompact_orca_judgment_tr_casetext_ledger_v0.md`

Use the current file only as handoff scope and resolved decision context. If it conflicts with the v0.14 spec files, report the conflict before coding.

## Resolved Pre-Code Review Decisions

These decisions close the pre-code review findings and must be implemented consistently.

1. Pydantic-ready schema names win for `RecommendedAction`.
   - Use `action_label` and `rationale`.
   - Do not author fixture `blind_judgement.yaml` with `action_name` or `action_description`.
   - If protocol docs still mention those names, treat them as protocol prose superseded by `pydantic_schema_reference.md` for implementation.

2. Evidence hash fallback is required for WebFetch/chat-only evidence.
   - If raw source bytes are unavailable, use a deterministic fallback hash basis, such as `sha256` of a canonical evidence-unit payload containing source URL, timestamp, retrieval timestamp, and summary.
   - Add an explicit `hash_basis` field to the EvidenceUnit model and evidence unit YAML.
   - Do not leave `hash` blank.

3. Protocol ledger metadata must not be silently dropped.
   - Expand `FacilitatorLedger` to include `case_family`, `decision_shape`, structured `ledger_authors`, and structured `leakage_audit`.
   - Do not rely on permissive `extra="allow"` for these fields.
   - Preserve `second_labeler_type: separate_model_family_advisory` for the TR/Casetext ledger.
   - Preserve `memorization_probe_required` and `known_fame_risk` in leakage metadata.

4. `MustAddressItem.evidence_unit_ids` must be modeled or preserved.
   - Add `evidence_unit_ids: list[str] = []` to the MustAddressItem model.
   - Do not treat it as unvalidated metadata.

5. `underreach_observability.basis` must include `option_value_loss`.
   - Add `option_value_loss` to the allowed basis vocabulary even though TR/Casetext uses `present: false`.
   - This prevents case_002 underreach fixture work from failing later on a known protocol/schema mismatch.

6. Disclaimer enforcement is mechanical for Step A.
   - Add a required `non_claim_notice` field to the generated case report or report summary, and set it exactly to `plumbing works only; not judgment quality`.
   - Add a test asserting the generated report or report summary contains that exact string.
   - Also include the string in the final chat closeout.

7. The Step A `blind_judgement.yaml` must be a real fixture file.
   - The runner must read a fixed `blind_judgement.yaml` from disk and score it.
   - Do not hard-code the contestant answer in the runner.
   - The fixed judgement for the green TR/Casetext run should use `judgement_class: escalate` and ladder level `6`.

8. The knife-edge mutation test must be two-sided.
   - Baseline TR/Casetext inputs with `option_value: high` must derive `band_status: conflict_escalate`, floor `6`, ceiling `6`.
   - Mutated inputs changing only `option_value: moderate` must derive `band_status: normal`, floor `3`, ceiling `3`.
   - This guards against a scorer that always returns conflict escalation.

9. `ceiling_trap` is not a scorer status.
   - `BandStatus` must contain only `normal`, `low_precision_band`, and `conflict_escalate`.
   - `ceiling_trap` may appear only as fixture/decision-shape vocabulary, not as `BandStatus`.
   - For the fixed TR/Casetext green judgement, use `decision_shape: escalation_required`.

10. `memorization_probe_result: not_run` is acceptable for Step A.
    - The case is quarantined and no LLM contestant is run.
    - The absence of a memorization probe must not be converted into a judgment-quality claim.

## Frozen TR/Casetext Fixture Inputs

Use these exact frozen band inputs:

```yaml
evidence_strength: moderate
evidence_independence: partially_independent
reversibility_feasibility: low
reversibility_cost: high
authority: partial
authority_acquisition_cost: medium
capability: partial
capability_build_cost: high
loss_shape: asymmetric_down
opportunity_cost: moderate
information_decay: fast
option_value: high
upside_shape: asymmetric_up
urgency: medium
```

Expected deterministic derivation from v0.14 constants:

```yaml
raw_ceiling: 3
dampened_floor: 4
conflict_condition: 4 > 3
action_floor: 6
action_ceiling: 6
band_status: conflict_escalate
```

The TR/Casetext fixture must be marked `QUARANTINED` and plumbing-grade. It cannot support judgment-quality claims.

## Must-Address Items

Include these as facilitator-ledger must-address items and ensure the fixed blind judgement covers them:

- `MA-01`: The passed-the-bar / category-leader signal is amplification of one vendor-affiliated source and echoes, not independent corroboration.
- `MA-02`: Moderate, partly amplified evidence supports scoped, reversible moves, not a low-reversibility $650M acquisition.
- `MA-03`: Competitive FOMO is real but unquantified; no pre-cutoff evidence proves an imminent rival bid.
- `MA-04`: Separate the genuine GenAI-in-legal opportunity from the unverified claim that Casetext is the leader.
- `MA-05`: Distinguish independent signal from echo and press reprinting.

## Implementation Route

STEP-01: Create the minimal `orca-harness/` package layout from the v0.14 architecture spec.

STEP-02: Implement schema models, including the resolved schema/protocol decisions above.

STEP-03: Implement the pure mapping table from `action_band_mapping_table_numbers.md`.

STEP-04: Implement band scoring formulas, shallow evidence ID checks, must-address coverage, and append-only failure event logging.

STEP-05: Implement a fixed-output runner that reads case files and `blind_judgement.yaml` from disk and writes a new `ScoringResult`; never overwrite prior scores.

STEP-06: Author the TR/Casetext plumbing fixture under `orca-harness/cases/plumbing/`, including participant packet, evidence units, facilitator ledger, fixed blind judgement, and scores directory.

STEP-07: Add tests:
- mapping constants and cap/floor paths needed for this fixture;
- conflict escalation;
- no `CEILING_TRAP` band status;
- TR/Casetext high-side expected result `[6, 6] conflict_escalate`;
- two-sided knife-edge mutation: `option_value: moderate` -> `[3, 3] normal`;
- report includes exact non-claim string;
- fixed runner reads `blind_judgement.yaml` from disk;
- no LLM imports in `scoring/**` and deterministic report paths;
- mapping version mismatch refuses scoring unless explicitly allowed by the spec.

STEP-08: Run validation and produce closeout with changed files, commands run, exact ScoringResult summary, knife-edge regression result, disclaimer enforcement evidence, and remaining blockers.

## Validation Expectations

Validation must be able to fail. At minimum:

- Unit tests for mapping constants and TR/Casetext derivation.
- Schema validation test for the TR/Casetext ledger, evidence units, and fixed blind judgement.
- Runner integration test against the fixture file.
- Two-sided knife-edge regression test.
- No-LLM-import guard for deterministic scoring/reporting paths.
- Report/summary string test for `plumbing works only; not judgment quality`.

If dependency installation is needed, ask for explicit owner authorization before installing.

## Stop Conditions

Stop and ask the owner before continuing if:

- `orca-harness/` already exists.
- Any v0.14 spec files conflict in a way not resolved above.
- Implementing the schema requires a broader redesign than the resolved decisions above.
- TR/Casetext labels would need to be changed.
- The expected TR/Casetext result does not derive from the constants.
- The mutation test does not produce `[3, 3] normal`.
- Any step would require external fetching, dependency installation, destructive cleanup, commits, pushes, or lifecycle actions without explicit authorization.

## Closeout Contract

Return:

- `orca_start_preflight` receipt.
- Files changed.
- Commands run and results.
- Exact `ScoringResult` summary.
- Knife-edge regression summary.
- Evidence that report/closeout includes `plumbing works only; not judgment quality`.
- Remaining blockers and non-goals.

End with:

```text
plumbing works only; not judgment quality
```
