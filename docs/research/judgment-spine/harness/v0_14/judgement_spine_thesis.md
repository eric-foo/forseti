# Orca Judgement Spine Thesis v0.14

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness v0.14 spec
scope: Top-level Judgment Harness thesis for v0.14.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


## Single Thesis

Orca is a **judgement harness**, not a trained model.

Because the base LLM weights cannot be edited, judgement improvement must come from the external system around the model:

```yaml
trainable_substrate:
  - prompts
  - case packets
  - schemas
  - deterministic scoring tables
  - runner contracts
  - failure logs
  - later memory files
  - baseline comparisons
```

The harness thesis is:

```yaml
judgement_spine_thesis: >
  For bounded evidence-constrained decisions, a frontier LLM can make better
  practical judgements when its output is forced through a repeatable harness:
  frozen evidence packet, frozen facilitator ledger, action-band derivation,
  schema validation, mechanical scoring, shallow evidence checking, baseline
  comparison, and failure logging.
```

## What the Harness Trains

It does not train the model internally. It trains the **environment of judgement**.

```yaml
not_training:
  - model weights
  - hidden reasoning ability
  - general wisdom

training:
  - what the model must output
  - how action is bounded
  - what counts as overreach
  - what counts as underreach
  - what evidence must be cited
  - what failures are logged
  - what later versions are allowed to use
```

## Core Spine

```yaml
spine:
  1_frozen_case:
    - participant_packet.md
    - facilitator_ledger.yaml
    - evidence_units.yaml

  2_frozen_band_inputs:
    - evidence_strength
    - evidence_independence
    - reversibility
    - authority
    - capability
    - loss_shape
    - opportunity_cost
    - information_decay
    - option_value
    - upside_shape
    - urgency

  3_deterministic_action_band:
    output:
      - action_floor
      - action_ceiling
      - band_status

  4_blind_judgement:
    contestant: raw_llm | strong_prompt | structured_pipeline | later_orca_harness

  5_mechanical_score:
    - in_band / over_band / under_band
    - overreach_distance
    - underreach_distance
    - evidence_id_presence
    - must_address_coverage

  6_failure_log:
    - records failures
    - does not promote rules in Phase 1
```

## Why Action Band, Not Ceiling Alone

Ceiling-only judgement prevents overreach but can train timidity.

Action-band judgement scores both sides:

```yaml
overreach: recommended_level > action_ceiling
underreach: recommended_level < action_floor
in_band: action_floor <= recommended_level <= action_ceiling
```

God-tier judgement is not maximal caution. It is **right-sized action**.

## Why Deterministic Scoring

LLMs may assist. They may propose labels, generate contestant outputs, run probes, and later critique.

They may not be the sole final authority for the scoring band used to grade themselves.

```yaml
phase_1_scoring_truth:
  source: frozen facilitator ledger inputs + mapping_table.py
  not: LLM judgement of whether the output was good
```

## What Phase 1 Can Claim

```yaml
allowed_claims:
  - plumbing works
  - scoring is repeatable given fixed inputs and fixed output
  - failures are logged
  - baseline outputs can be compared mechanically

forbidden_claims:
  - Orca improves judgement
  - Orca learned a rule
  - memory compounds
  - harness beats structured pipeline
  - semantic evidence support is validated
```

## First Real Proof Target

The first non-plumbing proof target is not broad superiority.

```yaml
first_real_target: >
  In one bounded decision family, the harness reduces one repeatable failure
  mode versus a strong baseline without worsening its paired guard.
```

Examples:

```yaml
valid_first_wins:
  - overreach decreases while underreach does not increase
  - underreach decreases while overreach does not increase
  - unsupported evidence IDs decrease while claim coverage does not collapse
  - false abstention decreases without reckless over-action
```

## The Spine in One Sentence

> Orca improves LLM judgement by turning judgement into a repeatable, scored, failure-logged interaction between frozen evidence, deterministic action-band scoring, and baseline comparison.
