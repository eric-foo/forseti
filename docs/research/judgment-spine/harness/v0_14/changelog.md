# Orca Judgement Harness v0.14 Change Log

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness v0.14 spec
scope: Context changelog explaining why v0.14 exists.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


## Status

v0.14 is a **code-readiness patch** on top of v0.13.

It does not reopen strategy or infrastructure architecture.

## Why v0.14 Exists

The implementation-readiness review found that v0.13 was architecturally frozen enough but still not code-ready.

The core blocker was:

```yaml
blocker: mapping_table_numbers_unspecified
meaning: >
  v0.13 defined the mapping-table interface and derivation order, but not the
  actual numeric values needed to implement mapping_table.py.
```

If coding started at v0.13, the implementer would invent scoring numbers during implementation. That would hide subjective judgement inside a pure-function shell.

## v0.14 Decisive Patches

```yaml
patches:
  numeric_mapping_table:
    file: action_band_mapping_table_numbers.md
    adds:
      - base ceilings
      - evidence-independence deltas
      - constraint caps
      - floor pressures
      - floor dampeners
      - conflict-escalate numerics
      - low-precision boundary

  scorer_formulas:
    file: scorer_formula_spec.md
    adds:
      - in_band formula
      - overreach_distance formula
      - underreach_distance formula
      - underreach primary/advisory gate
      - mapping-version mismatch behavior

  judgement_class_ladder_mapping:
    adds:
      - abstain -> level 0
      - wait -> level 1
      - escalate -> level 6
      - irreducible_uncertainty -> level 0 with must-address coverage
      - recommend -> levels 2/3/4/5/7/8

  memorization_probe_protocol:
    file: memorization_probe_protocol.md
    adds:
      - prompt template
      - pass/fail/ambiguous criteria
      - artifact schema
      - quarantine behavior

  pydantic_schema_reference:
    file: pydantic_schema_reference.md
    adds:
      - Participant packet frontmatter
      - FacilitatorLedger
      - BlindJudgement
      - ActionBandResult
      - ScoringResult
      - CaseReport
      - FailureEvent

  failure_event_log_format:
    adds:
      - multi-doc YAML stream
      - ULID event IDs
      - append-only semantics
      - scoring_result_hash
```

## Before / After

```yaml
before_v0_14:
  architecture: frozen_enough
  implementation: blocked_by_missing_numeric_table_and_schema_specifics

after_v0_14:
  architecture: frozen
  implementation: ready_to_start_first_week_build_sequence
```

## What v0.14 Still Does Not Build

```yaml
deferred:
  - semantic evidence checker
  - real memory store
  - rule promotion
  - adversarial review runner
  - perturbation harness
  - dashboard / polished reports
  - harness-vs-pipeline superiority claim
```
