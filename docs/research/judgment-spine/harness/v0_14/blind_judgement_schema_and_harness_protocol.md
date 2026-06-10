# Orca Blind Judgement Schema and Harness Protocol v0.14

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness v0.14 spec
scope: Contestant blind-judgment output schema and harness run protocol for v0.14.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


## Purpose

This document defines the contestant output contract and run protocol for Phase 1.

v0.14 separates:

```yaml
contestant_output: model-produced judgement
scoring_band: deterministic result from frozen facilitator ledger inputs
scoring_result: mechanical comparison of contestant output to scoring band
failure_event_log: non-compounding record of what failed
```

## Repeatability Policy

```yaml
scorer_repeatability:
  meaning: same fixed ledger + same fixed contestant output -> same score
  required: true

model_output_repeatability:
  meaning: same prompt/model may produce same output on rerun
  required: best_effort_only
  controls:
    - temperature_zero_where_supported
    - seed_where_supported
    - model_snapshot_logged
    - prompt_hash_logged
```

Do not claim model-output determinism unless the provider contract supports it.

## Contestant Runner Policy

```yaml
runner_policy:
  one_runner_for_all_contestants: true
  runner: runners/run_contestant.py
  contestant_manifest: config/contestants.yaml
  no_separate_baseline_runner: true
```

Baselines are contestants with different prompt/config manifests.

## Phase 1 Contestants

```yaml
required:
  - raw_frontier_llm
  - strong_single_prompt
  - fixed_structured_pipeline

optional_interface_only:
  - orca_harness
```

`orca_harness` may exist as an interface, but v0.14 forbids claiming that it beats `fixed_structured_pipeline` in Phase 1.

## Blind Judgement Output

```yaml
blind_judgement:
  case_id:
  contestant_id:
  run_id:
  model_id:
  model_family:
  model_snapshot_if_available:
  prompt_hash:
  temperature:
  seed_if_supported:
  harness_version: v0_14

  decision_shape:
    - action_band
    - ceiling_trap
    - underreach_trap
    - abstention_required
    - false_abstention_trap
    - escalation_required
    - forecast_shaped
    - high_conviction_action
    - option_creation
    - unsupported_load_bearing_claim_trap
    - private_context_dominant

  judgement_class:
    - recommend
    - abstain
    - wait
    - escalate
    - irreducible_uncertainty

  recommended_action:
    ladder_level:
    action_name:
    action_description:

  contestant_band_claim:
    claimed_floor:
    claimed_ceiling:
    reasoning:
    advisory_only: true

  evidence_used:
    - claim_id:
      claim_text:
      claim_role:
        - load_bearing
        - supporting
        - contextual
      evidence_unit_ids:

  must_address_items_covered:
    - must_address_item_id:

  load_bearing_assumption:
    statement:
    evidence_unit_ids:
    would_flip_if_false:

  advisory_phase_1_fields:
    judgement_class_probabilities:
    severe_error_assessment:
    reversal_triggers:
```

Fields under `advisory_phase_1_fields` may be captured but are not primary Phase 1 scores.

## Schema Repair Policy

```yaml
schema_repair_policy:
  repair_attempts_allowed: 1
  repair_role: schema_repair_assistant
  no_prompt_rerun: true
  if_repair_fails:
    - save raw_model_output.txt
    - mark schema_validity: false
    - continue other contestants
```

Do not retry the actual judgement prompt. Retrying hides model variance.

## Artifact Policy

```text
cases/<batch>/<case_id>/runs/<contestant_id>/<run_id>/
├── run_config.yaml
├── rendered_prompt.txt
├── raw_model_output.txt
├── blind_judgement.yaml
└── validation_result.yaml
```

`run_id` should be a ULID or timestamp plus short hash. Never overwrite prior runs.

## Required Run Metadata

```yaml
run_config:
  case_id:
  contestant_id:
  run_id:
  model_id:
  model_family:
  model_snapshot_if_available:
  temperature:
  seed_if_supported:
  prompt_path:
  prompt_hash:
  participant_packet_hash:
  facilitator_ledger_hash:
  mapping_table_version_pin:
  created_at:
```


---

# v0.14 Code-Readiness Patch

See `pydantic_schema_reference.md` for Pydantic-ready schemas.

## Judgement Class to Ladder Mapping

```yaml
abstain: level_0_only
wait: level_1_only
escalate: level_6_only
irreducible_uncertainty: level_0_only_with_must_address_coverage
recommend: allowed_levels_[2,3,4,5,7,8]
```

Invalid combinations are schema-invalid and must create a `schema_invalid` failure event.
