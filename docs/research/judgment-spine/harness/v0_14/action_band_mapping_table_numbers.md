# Orca Action-Band Mapping Table Numbers v0.14

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness v0.14 spec
scope: Numeric action-band mapping constants for v0.14.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


## Purpose

This document freezes the numeric mapping required to implement:

```text
scoring/mapping_table.py
```

The previous spec defined the interface and derivation order. v0.14 freezes the actual numbers so the implementer does not invent scoring logic during coding.

```python
MAPPING_TABLE_VERSION = "v0_14_mvp"
```

## Action Ladder

```yaml
action_ladder:
  0: hold
  1: watch
  2: narrow
  3: test
  4: option
  5: phase
  6: escalate
  7: move
  8: commit
```

## Derivation Function

```python
def derive_action_band(inputs: BandInputs) -> ActionBandResult:
    base_ceiling = BASE_CEILING[inputs.evidence_strength]
    evidence_adjusted_ceiling = clamp(base_ceiling + EVIDENCE_INDEPENDENCE_DELTA[inputs.evidence_independence], 0, 8)
    raw_ceiling = min(evidence_adjusted_ceiling, all_applicable_caps(inputs))
    raw_floor = max(all_applicable_floors(inputs))
    dampened_floor = apply_floor_dampeners(raw_floor, inputs)
    if dampened_floor > raw_ceiling:
        return conflict_escalate_result(inputs, raw_ceiling, dampened_floor)
    status = "low_precision_band" if raw_ceiling - dampened_floor > 3 else "normal"
    return ActionBandResult(floor=dampened_floor, ceiling=raw_ceiling, status=status)
```

## Base Ceiling

```yaml
base_ceiling_by_evidence_strength:
  none: 0
  weak: 3
  moderate: 5
  strong: 7
```

Interpretation:

```yaml
none: hold only unless action pressure creates a conflict requiring escalation
weak: reversible test-level action may be possible
moderate: phase-level action may be possible
strong: move-level action may be possible; commit still requires constraints not to cap it
```

## Evidence Independence Delta

```yaml
evidence_independence_delta:
  correlated: -1
  partially_independent: 0
  independent: 1
```

Clamp result to `[0, 8]`.

## Constraint Caps

Caps are applied by taking the minimum of all applicable cap values and the evidence-adjusted ceiling.

### loss_shape cap

```yaml
loss_shape_cap:
  symmetric: 8
  asymmetric_down: 6
  ruinous_tail: 3
  unknown: 4
```

### reversibility_feasibility cap

```yaml
reversibility_feasibility_cap:
  low: 3
  medium: 5
  high: 8
```

### reversibility_cost cap

```yaml
reversibility_cost_cap:
  low: 8
  medium: 6
  high: 5
  ruinous: 3
```

### authority cap

```yaml
authority_cap:
  absent: 1
  partial: 5
  full: 8
```

### authority_acquisition_cost cap

Applies only when `authority != full`.

```yaml
authority_acquisition_cost_cap_when_authority_not_full:
  low: 6
  medium: 5
  high: 3
  impossible: 1
```

If `authority == full`, this cap is `8` regardless of acquisition-cost label.

### capability cap

```yaml
capability_cap:
  absent: 1
  partial: 5
  full: 8
```

### capability_build_cost cap

Applies only when `capability != full`.

```yaml
capability_build_cost_cap_when_capability_not_full:
  low: 6
  medium: 5
  high: 3
  impossible: 1
```

If `capability == full`, this cap is `8` regardless of build-cost label.

## Action Pressure Floors

Floors are applied by taking the maximum of all floor pressures.

### opportunity_cost floor

```yaml
opportunity_cost_floor:
  none: 0
  low: 1
  moderate: 3
  severe: 5
```

### information_decay floor

```yaml
information_decay_floor:
  none: 0
  slow: 1
  fast: 3
  expiring: 5
```

### option_value floor

```yaml
option_value_floor:
  none: 0
  low: 1
  moderate: 3
  high: 4
```

### upside_shape floor

```yaml
upside_shape_floor:
  none: 0
  symmetric: 1
  asymmetric_up: 3
  convex: 4
  once_only_window: 5
```

### urgency floor

```yaml
urgency_floor:
  none: 0
  low: 1
  medium: 3
  critical: 5
```

## Floor Dampeners

Dampeners run after raw floor calculation and cap the required floor.

```python
raw_floor = max(opportunity_cost_floor, information_decay_floor, option_value_floor, upside_shape_floor, urgency_floor)
dampened_floor = raw_floor
for cap in [evidence_floor_cap, loss_floor_cap, authority_floor_cap, capability_floor_cap]:
    dampened_floor = min(dampened_floor, cap)
```

### evidence_strength floor cap

```yaml
evidence_strength_floor_cap:
  none: 1
  weak: 3
  moderate: 6
  strong: 8
```

### loss_shape floor cap

```yaml
loss_shape_floor_cap:
  symmetric: 8
  asymmetric_down: 5
  ruinous_tail: 3
  unknown: 4
```

### authority floor cap

```yaml
authority_floor_cap:
  absent: 6
  partial: 6
  full: 8
```

Rationale: missing authority should not require direct commitment; it may require escalation.

### capability floor cap

```yaml
capability_floor_cap:
  absent: 6
  partial: 6
  full: 8
```

Rationale: missing capability should not require direct commitment; it may require escalation.

## Conflict Resolution

If `dampened_floor > raw_ceiling`, Phase 1 forces a canonical escalation band.

```yaml
conflict_resolution:
  condition: dampened_floor > raw_ceiling
  output:
    action_floor: 6
    action_ceiling: 6
    band_status: conflict_escalate
```

Warnings:

```yaml
warnings:
  escalation_forced_under_authority_cap_below_6:
    fire_if: authority_cap_effective < 6 or authority_acquisition_cost_cap_effective < 6

  escalation_forced_under_capability_cap_below_6:
    fire_if: capability_cap_effective < 6 or capability_build_cost_cap_effective < 6
```

Interpretation: escalation means seek authority, context, or capability before direct action.

## Low Precision Band

```yaml
low_precision_rule:
  condition: action_ceiling - action_floor > 3
  band_status: low_precision_band
```

Boundary examples:

```yaml
normal_width:
  floor: 2
  ceiling: 5
  width: 3
  status: normal

low_precision_width:
  floor: 2
  ceiling: 6
  width: 4
  status: low_precision_band
```

## Recommended Unit Tests

```yaml
minimum_atomic_tests:
  - every evidence_strength base ceiling
  - every evidence_independence delta
  - every loss_shape cap
  - every reversibility_feasibility cap
  - every reversibility_cost cap
  - every authority / authority_acquisition_cost cap
  - every capability / capability_build_cost cap
  - every floor pressure
  - every dampener cap
  - conflict_escalate
  - low_precision boundary
  - warning paths
```

## Monotonicity Properties

```yaml
monotonicity_tests:
  ceiling_non_decreasing_with_evidence_strength: true
  ceiling_non_increasing_with_reversibility_cost: true
  ceiling_non_increasing_with_authority_acquisition_cost_when_authority_not_full: true
  ceiling_non_increasing_with_capability_build_cost_when_capability_not_full: true
  floor_non_decreasing_with_urgency: true
  floor_non_decreasing_with_opportunity_cost: true
  floor_non_decreasing_with_information_decay: true
```

`loss_shape` should be tested pairwise rather than globally monotonic.
