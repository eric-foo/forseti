# Orca Action-Band Mapping Executable Spec v0.14

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness v0.14 spec
scope: Pure deterministic action-band mapping function interface and required behavior for v0.14.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


## Purpose

This document specifies the first executable action-band mapping table.

The source of truth is the implementation:

```text
scoring/mapping_table.py
```

This document defines the interface and required behavior.

## Core Rule

```yaml
core_rule: >
  The mapping table must be expressible as a pure function from frozen enum
  inputs to an ActionBandResult. No natural-language conditionals, OR clauses,
  hidden judgement calls, or LLM calls are allowed inside the function.
```

## Function Interface

```python
MAPPING_TABLE_VERSION = "v0_14_mvp"

class BandStatus(Enum):
    NORMAL = "normal"
    LOW_PRECISION_BAND = "low_precision_band"
    CONFLICT_ESCALATE = "conflict_escalate"


def derive_action_band(inputs: BandInputs) -> ActionBandResult:
    """Pure deterministic function. No I/O. No LLM calls."""
    ...
```

Properties:

```yaml
function_properties:
  pure: true
  deterministic: true
  no_llm_calls: true
  no_io: true
  no_prompting: true
  enum_inputs_only: true
  path_coverage_required: true
```

## Action Ladder

```yaml
action_ladder:
  0_hold: no action; preserve current state
  1_watch: monitor defined signals
  2_narrow: reduce scope, segment, or limit exposure
  3_test: reversible probe
  4_option: create option value without full commitment
  5_phase: staged rollout or staged commitment
  6_escalate: seek authority, context, or decision-owner input
  7_move: material but reversible/controllable action
  8_commit: high-conviction hard-to-reverse commitment
```

Phase 1 simplification:

```yaml
ladder_assumption_note: >
  Phase 1 treats the action ladder as a contiguous ordered integer scale. This
  is a simplifying device. Later versions may represent the band as a set of
  permitted action levels rather than a contiguous range.
```

## Canonical Escalation Rule

```yaml
escalate_policy:
  canonical_meaning: action_ladder_level_6
  judgement_class_escalate: must_map_to_recommended_level_6
  band_conflict_default: scoring_band_6_to_6
```

If conflict resolution forces escalation while authority/capability caps appear to forbid it, the result must include a warning rather than silently hiding the contradiction.

```yaml
warning_example:
  - escalation_forced_under_authority_cap_below_6
```

## Band Inputs

All inputs are frozen in the facilitator ledger using `band_input_labeling_rubric.md`.

```yaml
band_inputs:
  evidence_strength: none | weak | moderate | strong
  evidence_independence: correlated | partially_independent | independent
  reversibility_feasibility: low | medium | high
  reversibility_cost: low | medium | high | ruinous
  authority: absent | partial | full
  authority_acquisition_cost: low | medium | high | impossible
  capability: absent | partial | full
  capability_build_cost: low | medium | high | impossible
  loss_shape: symmetric | asymmetric_down | ruinous_tail | unknown
  opportunity_cost: none | low | moderate | severe
  information_decay: none | slow | fast | expiring
  option_value: none | low | moderate | high
  upside_shape: none | symmetric | asymmetric_up | convex | once_only_window
  urgency: none | low | medium | critical
```

## Output

```yaml
action_band_result:
  mapping_table_version:
  action_floor:
  action_ceiling:
  band_status:
    - normal
    - low_precision_band
    - conflict_escalate
  band_width:
  mapping_trace:
    - step:
      input:
      value:
      effect:
  warnings:
```

## Derivation Order

The implementation must use a fixed order.

```yaml
derivation_order:
  1_base_ceiling_from_evidence:
    output: base_ceiling

  2_adjust_ceiling_for_evidence_independence:
    output: evidence_adjusted_ceiling

  3_apply_constraint_caps:
    inputs:
      - loss_shape
      - reversibility_feasibility
      - reversibility_cost
      - authority
      - authority_acquisition_cost
      - capability
      - capability_build_cost
    output: raw_ceiling

  4_compute_action_pressure_floors:
    inputs:
      - opportunity_cost
      - information_decay
      - option_value
      - upside_shape
      - urgency
    output: raw_floor

  5_apply_floor_dampeners:
    inputs:
      - evidence_strength
      - loss_shape
      - authority
      - capability
    output: dampened_floor

  6_resolve_conflict:
    condition: dampened_floor > raw_ceiling
    output_if_conflict:
      floor: 6
      ceiling: 6
      status: conflict_escalate

  7_mark_low_precision:
    condition: ceiling - floor > 3
    status_if_true: low_precision_band
```

Floor dampeners always run **after** raw floor calculation.

## Path Coverage Requirement

Full cross-product coverage is not required in unit tests because the enum cross-product is too large.

Required coverage means:

```yaml
coverage_required:
  - every cap path exercised
  - every floor path exercised
  - every dampener exercised
  - every status transition exercised
  - every warning path exercised
  - monotonicity property tests for major inputs
```

## Version Pinning

```yaml
version_pinning:
  mapping_table_version: v0_14_mvp
  facilitator_ledger_requires: mapping_table_version_pin
  scoring_result_requires: mapping_table_version
  mismatch_policy: refuse_to_score_unless_allow_rescore_flag
```

A rescore must write a new scoring result. It must never overwrite old scoring results.

## Mandatory Unit Tests Before Runner Work

```yaml
minimum_tests:
  - base ceiling by each evidence_strength value
  - evidence independence adjustments
  - each loss cap value
  - reversibility feasibility caps
  - reversibility cost caps
  - authority caps
  - capability caps
  - each opportunity cost floor
  - each information decay floor
  - each option value floor
  - each upside shape floor
  - each urgency floor
  - each floor dampener
  - conflict escalation
  - low precision band
  - mapping version mismatch
  - monotonicity property tests
  - no LLM imports in scoring/**
```


---

# v0.14 Code-Readiness Patch

v0.14 freezes the numeric table in `action_band_mapping_table_numbers.md`.

Implementation must import those constants or encode the same values exactly.

```yaml
mapping_table_version: v0_14_mvp
numeric_source: action_band_mapping_table_numbers.md
scorer_formulas: scorer_formula_spec.md
```

The mapping table is not code-ready unless these numeric values and formulas are implemented exactly.
