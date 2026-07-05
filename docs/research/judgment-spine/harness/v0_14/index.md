# Forseti Judgement Harness v0.14 Index

```yaml
retrieval_header_version: 1
artifact_role: Judgment Harness spec index
scope: Navigation index for the imported v0.14 Judgment Harness code-readiness spec and Forseti-local execution-isolation additions.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Choosing the controlling v0.14 harness file for schemas, scoring, cases, or runner contracts.
  - Checking that Judgment Harness work is not being confused with Data Capture, ECR, or Cleaning work.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/README.md
  - .agents/workflow-overlay/source-of-truth.md
```

## Status

v0.14 is the **Phase 1 code-readiness spec**.

It freezes the final details needed before implementing the first runnable harness loop.

In Forseti workspace allocation, this folder is the working Judgment Harness spec under Judgment Spine. It does not authorize implementation by itself, and it does not define Data Capture Spine, Evidence Candidate Record, or Cleaning Spine.

## Bridge Foundation

| Path | Use | Status |
| --- | --- | --- |
| `case_to_v0_14_bridge_foundation_v0.md` | Non-implementation bridge for mapping existing Judgment Spine case material into the v0.14 harness-entry shape. | Working bridge foundation; does not authorize implementation, validation, scoring, or proof claims. |
| `unity_v0_14_fixture_extraction_plan_v0.md` | Docs-only Unity Runtime Fee fixture-admission extraction plan covering participant-packet, evidence-registry, facilitator-ledger, leakage, probe, sealed-memo, and Daimler fallback gates. | Working extraction plan; does not authorize implementation, probe execution, validation, scoring, or proof claims. |
| `fixtures/unity_runtime_fee_2023_v0_14/fixture_authoring_receipt_v0.md` | Docs-only Unity Runtime Fee v0.14 draft fixture pack receipt and inventory. | Draft fixture pack; blocked before scoring; does not authorize implementation, probe execution, model runs, validation, scoring, proof, product proof, or lesson promotion. |
| `fixtures/canoo_walmart_2022_v0_14/fixture_authoring_receipt_v0.md` | Docs-only Canoo/Walmart v0.14 draft fixture pack receipt and inventory. | Draft fixture pack; blocked before scoring; does not authorize implementation, probe execution, model runs, validation, scoring, proof, product proof, or lesson promotion. |
| `packing_to_harness_foundation_interface_architecture_v3.md` (current; v0/v1/v2 superseded) | Docs-only target architecture for the Packing Phase -> v0.14 Judgment Harness Foundation interface. Names Packing-owned outputs, the Facilitator labeling step, Harness-owned freeze inputs, the contestant-visible boundary, deterministic checks, report meaning, inadmissibility states, and the three named adapter slots (sealed-memo, source-visibility-gap, protocol-to-Pydantic). **v3 is the current review-corrected recommendation and supersedes v2; v0 (off-spec attempt), v1 (consumed GPT candidate), and v2 (adjudicated) remain only as historical/provenance — see ORCA-HYGIENE-002. The `..._daimler_pressure_test_v0.md` companion references v2's hash as a historical record and must not be rewritten.** | Working architecture artifact; current = v3; does not authorize implementation, probe execution, model runs, scoring, validation, proof, product proof, or lesson promotion. |
| `contestant_no_tools_execution_contract_v0.md` | Docs-only local execution-isolation contract for contestant probes and blind judgment runs. Names required no-tools evidence fields, clean-pass semantics, conservative fail caveats, and tool-violation invalidation. | Local harness contract; does not authorize implementation, probe execution, model runs, scoring, validation, proof, product proof, or lesson promotion. |
| `no_case_smoke_test_authorization_checklist_v0.md` | Docs-only operator checklist for non-gate-clearing no-case raw-API smoke tests. Defines synthetic input convention, required concrete authorization fields, and out-of-band execution provenance capture. | Smoke-test checklist; does not authorize live calls, real probes, participant-packet exposure, model runs beyond a separately authorized smoke test, scoring, validation, fixture admission, proof, product proof, or lesson promotion. |

## Reading Order

```yaml
1: judgement_spine_thesis.md
2: judgement_harness_strategy.md
3: phase_1_infrastructure_architecture.md
4: action_band_mapping_table_numbers.md
5: action_band_mapping_executable_spec.md
6: scorer_formula_spec.md
7: pydantic_schema_reference.md
8: band_input_labeling_rubric.md
9: blind_judgement_schema_and_harness_protocol.md
10: judgement_case_construction_protocol.md
11: memorization_probe_protocol.md
12: contestant_no_tools_execution_contract_v0.md
13: no_case_smoke_test_authorization_checklist_v0.md
14: failure_event_log_spec.md
15: proof_and_memory_plan.md
16: changelog.md
```

## Review Prompts

```yaml
review_prompts:
  implementation_readiness: review_prompts/opus_implementation_readiness_prompt.md
  code_ready_sanity_review: review_prompts/opus_code_ready_sanity_review_prompt.md
```

## Source-of-Truth Roles

```yaml
thesis: overall judgement spine
strategy: why the harness exists
architecture: Phase 1 repo/build scope
numeric_mapping: exact scoring constants
executable_spec: mapping function interface and behavior
scorer_formulas: score computation
pydantic_reference: implementation schema contract
labeling_rubric: how ledger inputs are frozen
case_protocol: how cases are constructed
probe_protocol: memorization probe behavior
contestant_execution_isolation: no-tools evidence required for clean contestant gate clearing
no_case_smoke_test: non-gate-clearing raw-API plumbing check and provenance checklist
failure_log: failure logging only, not memory
proof_memory_plan: proof constraints and Phase 1 claim discipline
```

## Code-Ready Gate

```yaml
ready_to_code_if:
  - mapping table numbers are frozen
  - judgement_class ladder mapping is frozen
  - overreach/underreach formulas are frozen
  - conflict_escalate is deterministic
  - memorization probe protocol exists
  - contestant no-tools execution contract exists for clean gate-clearing semantics
  - scoring_result and case_report schemas exist
```

v0.14 satisfies this gate.
