# Orca Judgement Harness Proof and Memory Plan v0.14

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness v0.14 spec
scope: Proof constraints and Phase 1 memory boundaries for v0.14.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


## Purpose

This document defines proof and memory discipline for the Phase 1 infrastructure version of the judgement harness.

v0.14 is not trying to prove judgement quality yet.

It is trying to prove that the infrastructure can run, score deterministically, and log failures without prematurely creating rule memory.

## Phase 1 Claim Discipline

```yaml
first_30_days:
  allowed_claim:
    - executable_plumbing_works
    - scorer_repeatable_given_fixed_inputs_and_fixed_contestant_output
    - five_cases_run_end_to_end
    - failure_events_logged

  forbidden_claims:
    - Orca_improves_judgement
    - Orca_beats_baselines
    - Orca_compounds_memory
    - rule_promotion
    - moat_claims
    - harness_beats_structured_pipeline
```

## Phase 1 Contestants

```yaml
phase_1_contestants:
  raw_frontier_llm:
    role: model-only baseline

  strong_single_prompt:
    role: strongest short prompt baseline
    requirement: frozen_before_orca_specific_prompt_iteration

  fixed_structured_pipeline:
    role: same schema, no memory, no lifecycle

  orca_harness:
    role: optional interface only
    proof_status: no superiority claim in Phase 1
```

Operator-with-Orca and autonomous-Orca are not Phase 1 proof targets.

## Primary Phase 1 Scores

```yaml
scores:
  schema_validity:
    type: deterministic

  action_band_position:
    type: deterministic_given_mapping_table
    values: in_band | over_band | under_band

  overreach_distance:
    type: deterministic

  underreach_distance:
    type: deterministic
    caveat: primary_only_if_underreach_observability_present

  evidence_id_presence:
    type: deterministic_shallow

  claim_coverage:
    type: deterministic_shallow

  memorization_probe_result:
    type: protocolized_llm_probe

  failure_event_logged:
    type: deterministic_if_failure_condition_met
```

## Evidence-to-Claim Policy

Phase 1 does not prove semantic support.

```yaml
phase_1_evidence_policy:
  checks:
    - cited evidence IDs exist
    - cited evidence is not excluded/post-decision
    - load-bearing claims cite at least one evidence unit
    - must-address item IDs are covered

  does_not_check:
    - semantic relevance
    - direct vs inferential support
    - contradiction
```

## Memory Policy

Phase 1 memory is only failure logging.

```yaml
phase_1_memory:
  location: memory/logs/failure_events.yaml
  allowed:
    - log mechanical failures
    - count repeated failure types
    - inspect failures manually

  forbidden:
    - promoted rules
    - reusable judgement rules
    - automatic memory retrieval
    - memory-based contestant enhancement
    - compounding claims
```

## Rule Candidate Policy

Rule candidates are deferred.

```yaml
rule_candidates:
  first_30_days: forbidden
  first_90_days: optional_log_only
  promotion: forbidden_until_after_held_out_validation
```

## First 90 Days Claim Discipline

```yaml
first_90_days:
  allowed:
    - one_failure_mode_identified
    - rule_candidates_identified
    - baseline_comparison_run
    - no_promotion_claim

  forbidden:
    - rule_promoted
    - harness_generally_improves_judgement
    - memory_compounds
    - broad_benchmark_claim
```

## Kill Criteria

```yaml
kill_or_patch_if:
  mapping_table_cannot_be_expressed_as_pure_function:
    action: simplify input set until it compiles

  band_input_labeling_disagreement_unstable:
    action: strengthen rubric; quarantine unstable cases

  scorer_not_repeatable_given_fixed_inputs_and_output:
    action: reduce scorer to smaller deterministic subset

  evidence_id_checker_never_fails:
    action: rebuild unsupported_claim_trap case and checker fixtures

  structured_pipeline_matches_orca_harness:
    action: do not claim harness improvement; keep pipeline as baseline

  memory_log_becomes_rule_store:
    action: delete promoted/retrieval directories and restore failure-log-only policy
```


---

# v0.14 Code-Readiness Patch

Phase 1 deterministic formulas are frozen in `scorer_formula_spec.md`.

```yaml
overreach_distance: max(0, recommended_level - action_ceiling)
underreach_distance: max(0, action_floor - recommended_level)
in_band: action_floor <= recommended_level <= action_ceiling
```

Rule memory remains forbidden in Phase 1. Failure logging only.
