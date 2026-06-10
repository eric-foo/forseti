# Orca Band Input Labeling Rubric v0.14

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness v0.14 spec
scope: Band-input labeling workflow and enum rubric for v0.14 facilitator ledgers.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


## Purpose

The action-band mapping function is deterministic only after its inputs are frozen.

This rubric governs how those inputs are labeled in the facilitator ledger.

```yaml
core_problem: >
  If band inputs are labeled by vibes, deterministic scoring only hides upstream
  subjective judgement.

core_fix: >
  Every band-input label must be attached to a rubric version, author, second
  label, and disagreement log before the ledger is frozen.
```

## Labeling Workflow

```yaml
workflow:
  1_primary_label:
    actor: operator_or_case_constructor
    output: proposed_band_input_set

  2_second_label:
    actor: second_operator_if_available_else_separate_model_family_advisory
    output: second_band_input_set

  3_diff:
    actor: operator
    output: second_label_diffs

  4_resolution:
    actor: operator
    output: frozen_band_input_set

  5_freeze:
    output:
      - ledger_freeze_hash
      - committed_at
      - labeling_rubric_version
```

Second-labeling does not create truth. It creates an audit trail.

## Required Ledger Fields

```yaml
facilitator_ledger_required_fields:
  labeling_rubric_version: v0_14
  ledger_authors:
    - primary_labeler
    - second_labeler
  second_label_diffs:
    - input_name:
      primary_label:
      second_label:
      final_label:
      resolution_reason:
  frozen_band_inputs:
  mapping_table_version_pin:
  ledger_freeze_hash:
  committed_at:
```

## Band Inputs

### evidence_strength

```yaml
values:
  none:
    include_if:
      - no packet evidence directly bears on the decision question
      - evidence is purely contextual or speculative
    exclude_if:
      - any evidence unit supports a directional claim
    example: no customer, market, operational, technical, or historical signal relevant to the decision
    common_confusion: weak evidence is not none

  weak:
    include_if:
      - evidence suggests a direction but is thin, anecdotal, single-source, or low-integrity
    exclude_if:
      - multiple independent sources support the same directional claim
    example: one credible but isolated complaint suggests a packaging issue
    common_confusion: loud attention is not automatically moderate evidence

  moderate:
    include_if:
      - multiple sources or one high-integrity source support a directional claim
      - evidence can justify a reversible test or scoped action
    exclude_if:
      - evidence supports a hard-to-reverse commitment
    example: pricing-page change plus repeated forum objections plus observed usage friction
    common_confusion: correlated sources do not become strong merely by quantity

  strong:
    include_if:
      - high-integrity, independent, decision-relevant evidence supports the same conclusion
      - evidence is sufficient for material action if other constraints allow
    exclude_if:
      - evidence is strong only because the case outcome is known post hoc
    example: audited data plus direct behavioral signal plus independent corroboration
    common_confusion: strong evidence still may not justify action if authority or capability is missing
```

### evidence_independence

```yaml
values:
  correlated:
    include_if:
      - evidence units likely share the same source, narrative, actor, or causal origin
    example: three articles quoting the same original company announcement

  partially_independent:
    include_if:
      - evidence units come from different sources but may share a common incentive or propagation path
    example: pricing page plus partner blog plus forum thread about the same change

  independent:
    include_if:
      - evidence units arise from meaningfully separate sources or mechanisms
    example: customer behavior data, external pricing page, and independent technical benchmark
```

### reversibility_feasibility

```yaml
values:
  low:
    include_if: action would be hard or impossible to reverse operationally, legally, reputationally, or technically
    example: permanent contract change or irreversible public commitment

  medium:
    include_if: reversal is possible but requires meaningful coordination, cost, or delay
    example: staged rollout can be rolled back but causes customer confusion

  high:
    include_if: reversal can be done quickly with bounded cost and little external damage
    example: limited internal test, reversible config change, opt-in beta
```

### reversibility_cost

```yaml
values:
  low:
    include_if: reversal cost is minor relative to decision value
  medium:
    include_if: reversal cost is material but survivable
  high:
    include_if: reversal cost is large enough to affect action band
  ruinous:
    include_if: reversal would create existential, regulatory, trust, or unrecoverable financial harm
```

### authority

```yaml
values:
  absent:
    include_if: decision owner lacks authority to execute the action
  partial:
    include_if: decision owner can execute some actions but not the strongest possible actions
  full:
    include_if: decision owner can execute the relevant action without additional authorization
```

### authority_acquisition_cost

```yaml
values:
  low:
    include_if: authority can be obtained quickly with low friction
  medium:
    include_if: authority requires meaningful approval, coordination, or delay
  high:
    include_if: authority acquisition is costly, slow, or politically difficult
  impossible:
    include_if: authority cannot realistically be obtained under case constraints
```

### capability

```yaml
values:
  absent:
    include_if: actor lacks the operational/technical/financial capability to execute the action
  partial:
    include_if: actor can execute a narrower or lower-intensity action but not full action
  full:
    include_if: actor can execute the relevant action with available resources
```

### capability_build_cost

```yaml
values:
  low:
    include_if: missing capability can be built quickly and cheaply
  medium:
    include_if: capability build is feasible but requires real time/resource investment
  high:
    include_if: capability build is major and likely changes the action band
  impossible:
    include_if: capability cannot be built under case constraints
```

### loss_shape

```yaml
values:
  symmetric:
    include_if: upside and downside are roughly balanced and reversible
  asymmetric_down:
    include_if: downside meaningfully exceeds upside or is harder to recover from
  ruinous_tail:
    include_if: downside includes existential, regulatory, trust-destroying, or unrecoverable harm
  unknown:
    include_if: downside cannot be estimated from available evidence
```

### opportunity_cost

```yaml
values:
  none:
    include_if: inaction preserves options and does not materially worsen position
  low:
    include_if: delay has minor cost
  moderate:
    include_if: delay loses some value, time, or positioning
  severe:
    include_if: inaction likely destroys major option value, causes lost window, or creates status-quo commitment
```

### information_decay

```yaml
values:
  none:
    include_if: waiting is likely to improve information or preserve optionality
  slow:
    include_if: information value decays gradually
  fast:
    include_if: decision window is closing or delayed action materially worsens position
  expiring:
    include_if: there is a once-only or near-term window after which action value drops sharply
```

### option_value

```yaml
values:
  none:
    include_if: action does not preserve or create meaningful future option value
  low:
    include_if: action creates minor optionality
  moderate:
    include_if: action creates a useful future choice or learning path
  high:
    include_if: action creates major option value with bounded downside
```

### upside_shape

```yaml
values:
  none:
    include_if: no meaningful upside exists from acting now
  symmetric:
    include_if: upside and downside are roughly similar magnitude
  asymmetric_up:
    include_if: upside materially exceeds bounded downside
  convex:
    include_if: small action can create disproportionately large upside
  once_only_window:
    include_if: upside depends on acting before a closing window
```

### urgency

```yaml
values:
  none:
    include_if: timing does not materially affect decision quality
  low:
    include_if: timing matters but there is room to wait or gather evidence
  medium:
    include_if: delay imposes real cost or reduces options
  critical:
    include_if: delay itself is a likely severe error
```

## Labeling Disagreement Rules

```yaml
disagreement_rules:
  diff_required_if: primary_label != second_label
  resolution_required: true
  case_quarantine_if:
    - more_than_3_band_inputs_disagree
    - disagreement_on_evidence_strength_exceeds_one_level
    - disagreement_on_loss_shape_includes_ruinous_tail
    - disagreement_on_information_decay_includes_expiring
```

Quarantined cases may still be used as plumbing fixtures, but cannot support later judgement-quality claims.
