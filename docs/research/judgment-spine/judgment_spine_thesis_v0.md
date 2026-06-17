# Judgment Spine Thesis v0

```yaml
retrieval_header_version: 1
artifact_role: Judgment Spine thesis
scope: Long-term optimization thesis for Orca's Judgment Spine.
use_when:
  - Setting the north-star goal before Judgment Spine architecture, CA setup, harness work, case learning, or lesson promotion.
  - Checking whether a proposed Judgment Spine move serves right-sized decision judgment rather than artifact churn or premature implementation.
  - Distinguishing the parent Judgment Spine goal from the v0.14 Judgment Harness spec.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md
  - docs/research/judgment-spine/README.md
  - docs/research/judgment-spine/harness/v0_14/index.md
  - docs/product/foundation/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
```

- Status: WORKING_THESIS_V0
- Artifact type: Long-term Judgment Spine thesis
- Scope: Goal, optimization target, boundary, and success signal for Judgment Spine development
- Source basis: current owner direction, `docs/research/judgment-spine/README.md`, `docs/research/judgment-spine/harness/v0_14/judgement_spine_thesis.md`, `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md`, `docs/product/core_spine_v0_information_production_foundation_v0.md`
- Implementation authorized: no
- Feature planning authorized: no
- CA prompt authorized: bounded thesis operating-contract prompt exists; no general CA execution or implementation authority

## Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S1 plus Judgment Spine thesis targets
  edit_permission: docs-write
  target_scope: Create a parent Judgment Spine thesis for long-term optimization before CA setup.
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Thesis

Orca's Judgment Spine is the durable judgment-improvement layer for turning bounded approved evidence into right-sized action.

It improves judgment by accumulating case-law-quality examples, sealed blind judgments, deterministic harness comparisons, failure logs, and transferable lessons about what evidence can and cannot support.

Case-law-quality means the case preserves the decision frame, evidence boundary, blind judgment, reveal/readout, failure mode, and lesson status well enough that future agents can reuse it without re-litigating what happened.

The point is not to make the model generally wiser. The point is to make the judgment environment harder to fool: better packets, clearer decision frames, explicit action bands, preserved misses, sharper failure categories, and promotion rules that stop single-case insight from becoming premature doctrine.

## Long-Term Optimization Goal

Optimize the Judgment Spine for **right-sized action under evidence constraints**.

Right-sized action means:

- not overreaching beyond what the evidence, authority, capability, reversibility, and downside can support;
- not hiding behind false caution when action pressure, option value, urgency, or underreach risk makes inaction costly;
- preserving uncertainty, counterevidence, and unsupported claims in a form that improves future judgment;
- making each new case, score, failure, or lesson easier to reuse without contaminating blind evaluation.

## What The Spine Trains

The Judgment Spine does not train model weights. It trains the surrounding judgment system:

```yaml
trainable_surface:
  - case selection standards
  - clean participant packets
  - sealed blind judgment discipline
  - facilitator ledgers and frozen band inputs
  - action-band mapping and scoring
  - evidence citation and must-address checks
  - failure-event logging
  - reveal readouts and outcome calibration
  - reusable lesson promotion rules
  - prompts and harness interfaces
```

The scarce asset is not more text. It is accumulated correction: specific records of where a judgment overreached, underreached, ignored evidence, relied on unsupported claims, failed to escalate, or abstained when a bounded action was warranted.

## Parent Spine Versus Harness Spec

Judgment Spine is the parent layer. The v0.14 Judgment Harness is one executable-spec candidate inside it.

```yaml
parent_judgment_spine:
  owns:
    - long-term judgment-improvement thesis
    - case-law loop
    - spoiler safety and blind evaluation discipline
    - transferable lesson promotion
    - relationship between qualitative case learning and mechanical harness scoring

v0_14_judgment_harness:
  owns:
    - Phase 1 harness schemas
    - action-band mapping table
    - band scorer formulas
    - runner contracts
    - plumbing case protocol
    - memorization probe
    - failure-event log spec
```

Do not force every Judgment Spine artifact into the v0.14 harness. Case learning, owner critique, reveal readouts, and qualitative lessons can remain Judgment Spine material even before they become harness fixtures.

Do not let the harness spec become generic product architecture. Data Capture Spine, Evidence Candidate Record, and Cleaning Spine remain separate layers.

## Layer Boundary

Judgment Spine owns inference and decision-use effects:

- Signal Integrity effects;
- Signal Use Classification;
- uncertainty and alternative explanations;
- counterevidence;
- discounting and exclusion;
- Decision Strength;
- Action Floor, Action Ceiling, and action-band judgment;
- overreach, underreach, escalation, abstention, and unsupported-claim failure modes;
- reusable lessons from blind judgment versus reveal.

Judgment Spine must not own:

- source acquisition or preservation obligations, which belong to Data Capture Spine;
- the pre-cleaning captured-signal receipt, which belongs to Evidence Candidate Record;
- normalization, dedupe, translation, summarization, and transformation trace, which belong to Cleaning Spine;
- memo or deck production as communication output;
- runtime systems, source maps, dashboards, scrapers, packages, tests, or implementation work without later bounded authorization.

## Operating Loop

The mature Judgment Spine should make this loop easier and stricter over time:

```text
Decision Frame
-> clean participant packet or source packet
-> spoiler-safety receipt
-> sealed blind judgment
-> action-band, Action Floor, or Action Ceiling comparison
-> evidence and must-address checks
-> failure-event logging
-> reveal or owner critique
-> outcome calibration
-> transferable lesson extraction
-> guarded promotion into future cases, prompts, rubrics, or harness specs
```

The loop should preserve misses. A Judgment Spine that records only attractive wins becomes marketing residue, not judgment infrastructure.

## Promotion Standard

A lesson should move from case-local insight toward reusable Judgment Spine guidance only when it meets at least one strong condition:

- it appears across multiple cases;
- it strongly explains a major revealed outcome without violating blind/reveal separation or turning hindsight into doctrine;
- it fixes a repeated operator or model failure mode;
- it improves a later blind judgment or harness result;
- it names where the lesson does not apply.

Single-case lessons can be valuable. They should remain provisional unless transfer is shown or an owner explicitly accepts the exception.

## First Success Signal

The first durable success signal is not a broad claim that Orca improves judgment.

The first success signal is architectural and evidentiary:

```yaml
first_success_signal: >
  A future agent can add or evaluate a Judgment Spine case, harness spec change,
  failure event, or reusable lesson while preserving the Data Capture / ECR /
  Cleaning / Judgment boundary, spoiler safety, action-support discipline, and
  no-premature-implementation rule.
```

The first later empirical success signal is narrower:

```yaml
first_empirical_signal: >
  In one bounded decision family, the Judgment Spine or harness reduces one
  repeatable failure mode versus a strong baseline without worsening its paired
  guard.
```

Examples:

- overreach decreases without underreach increasing;
- underreach decreases without overreach increasing;
- unsupported evidence use decreases without must-address coverage collapsing;
- false abstention decreases without reckless over-action;
- escalation improves where authority, capability, or missing context makes direct recommendation unsafe.

## Non-Claims

This thesis does not claim Judgment Spine validation, buyer validation, product readiness, feature readiness, implementation readiness, commercial readiness, model-training readiness, harness superiority, memory compounding, or proof-run readiness.

It does not authorize implementation, runtime design, source maps, schemas, scrapers, automation, tests, deployment, commits, pushes, PRs, or CA execution.

It is a north-star artifact for future Judgment Spine architecture and CA setup.
