# Orca Judgement Harness Strategy v0.14

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness v0.14 spec
scope: Judgment Harness strategy, identity, and Phase 1 claim discipline for v0.14.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


## Purpose

Orca is a **judgement harness**, not a trained base model.

Orca does not edit model weights. It improves bounded judgement tasks by controlling the environment around frontier LLMs:

```yaml
trainable_substrate:
  - prompts
  - files
  - schemas
  - case packets
  - scoring functions
  - failure logs
  - later memory files
  - baseline comparisons
```

The base model is not trained internally. The harness is improved externally.

## v0.14 Phase 1 Patch

v0.14 keeps the v0.12 infrastructure freeze and adds three operational fixes:

```yaml
v0_14_fixes:
  1_labeling_rubric:
    problem: frozen band inputs were operator-authored without a published rubric
    fix: every enum value now requires definition, include_if, exclude_if, examples, and common_confusions

  2_failure_event_log_only:
    problem: memory could become premature rule memory
    fix: Phase 1 logs failures only; no promoted rules, retrieval, or compounding claim

  3_baseline_scope:
    problem: structured_pipeline and orca_harness are not distinct while memory/retrieval are deferred
    fix: Phase 1 may implement harness interface, but does not claim harness beats pipeline
```

## Core Identity

```yaml
identity: judgement_harness
not: trained_model
not: long_prompt_only
not: benchmark_claim_engine
not: commercial_product_lane
```

A real harness must be mechanically distinct from one long inference call.

```yaml
minimum_harness_requirements:
  - frozen participant packet
  - frozen facilitator ledger
  - band input labeling rubric
  - executable action-band mapping function
  - blind contestant output
  - schema validation
  - mechanical scoring
  - baseline comparison
  - failure-event logging
```

## Phase 1 Goal

```yaml
phase_1_goal: >
  Build an executable judgement harness loop that can run five plumbing cases
  end-to-end with deterministic scoring given frozen inputs and fixed contestant
  outputs, while logging failures without promoting rules.

first_claim_allowed: plumbing_works
first_claim_forbidden: judgement_improvement
```

## LLM Role

v0.14 keeps the precise fix from v0.11/v0.12.

```yaml
allowed_llm_roles:
  - contestant
  - advisory proposer of band input labels
  - explainer of evidence-to-input mapping
  - schema repair assistant after failed validation
  - memorization probe target
  - cross-family sanity-check deriver
  - adversarial reviewer in later phases

forbidden_llm_role:
  - sole final authority for the scoring band used to grade itself
```

The LLM may help. It may not be the sole final judge of the target it is scored against.

## Band Input Labeling Boundary

```yaml
band_input_labeling_policy:
  primary_labeler: operator_or_case_constructor
  second_labeler: second_operator_if_available_else_separate_model_family_advisory
  required_artifact: second_label_diffs
  freeze_required_before: contestant_run
```

Second-labeling does not create expert truth. It creates an audit trail and surfaces unstable labels.

## Memory Policy

Phase 1 memory is a log, not a memory system.

```yaml
phase_1_memory:
  allowed:
    - failure_event_log
    - run_id
    - case_id
    - contestant_id
    - score_result_refs
    - overreach_or_underreach
    - evidence_id_failures
    - schema_failures
    - notes_on_failure_mode

  forbidden:
    - promoted_rules
    - reusable_judgement_rules
    - retrieval_augmented_memory
    - compounding_claims
    - orca_learned_x_language
```

## Phase 1 Baseline Scope

```yaml
phase_1_contestants:
  required:
    - raw_frontier_llm
    - strong_single_prompt
    - fixed_structured_pipeline

  optional_interface_only:
    - orca_harness
```

Phase 1 does **not** claim that Orca harness beats fixed structured pipeline.

```yaml
why: >
  While memory, retrieval, and lifecycle are deferred, the harness is not yet
  mechanically distinct enough from the structured pipeline for a superiority
  claim.
```

## Current Build Priority

```yaml
build_order:
  1: band_input_labeling_rubric
  2: scoring/mapping_table.py
  3: tests/test_mapping_table.py
  4: facilitator_ledger_schema_with_freeze_and_disagreement_fields
  5: schema_validator
  6: band_scorer
  7: deterministic_evidence_id_checker
  8: run_contestant.py
  9: memory/logs/failure_events.yaml
  10: case_001_end_to_end
```
