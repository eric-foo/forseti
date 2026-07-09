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
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
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

## Amendment — 2026-06-20 (owner-directed): Optimization Target Sharpened To Decision-Quality Regret (Expected Value)

Owner-directed in-thread. This **sharpens, and does not replace,** the
optimization goal above: right-sized action stays a load-bearing **component**,
but the target is the **highest-expected-value decision under evidence
constraints**, evaluated as **decision-quality regret**. The thesis operating
contract's "Owner Decisions Required → changing the long-term optimization
target" gate is cleared by this owner direction. It is consistent with the
evidence ladder's Measurement Target ("the quality of the decision under the
case's evidence constraints"; "no outcome/resulting bias") and adds no claim
tier or score.

- **Target = highest-EV decision, expressed qualitatively.** Expected value is
  the conceptual north star, not a computed number; the calls are qualitative.
  Operationally the target is **decision-quality regret**: the qualitatively
  assessed gap between the move made and the **best move the evidence available
  at the decision point supported**.
- **Right-sizing is a necessary component, not the whole target.** Avoiding
  overreach and underreach is required but not sufficient — a within-band call
  can still leave expected value on the table by passing a better
  evidence-supported move. Optimizing only against over/under-reach yields
  defensibly-sized but sub-optimal decisions; the target is closing the regret
  gap, of which gross mis-sizing is one source.
- **Regret is measured at the contemporaneous evidence frontier.** "Could have
  been better" means *a higher-EV move was supported by the evidence at the
  time* — never *a different move would have had a better outcome*. An
  evidence-right call that draws an unlucky outcome carries **zero regret**.
  This preserves the no-outcome-bias rule (evidence ladder Measurement Target):
  judgment is graded on the best move under the available evidence, not on
  correctness against the later outcome.
This refines the optimization target only. It stays qualitative (no numeric EV
or regret score; the evidence ladder and its no-scoring boundary still govern)
and asserts no validation, readiness, buyer proof, judgment-quality evidence, or
run authorization.

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Judgment Spine long-term optimization target is sharpened from
    "right-sized action under evidence constraints" to the highest-expected-value
    decision under evidence constraints, evaluated qualitatively as
    decision-quality regret (the gap to the best move the contemporaneous
    evidence supported). Right-sized action (over/under-reach) is retained as a
    necessary component, not the whole target. Regret is measured at the
    time-of-decision evidence frontier (an evidence-right but unlucky call
    carries zero regret; no outcome/resulting bias). Owner-directed; the
    operating contract's owner-decision gate for changing the optimization target
    is thereby cleared.
  trigger: validation_philosophy
  related_triggers:
    - product_doctrine
  controlling_sources_updated:
    - docs/research/judgment-spine/judgment_spine_thesis_v0.md
    - docs/research/judgment-spine/judgment_spine_thesis_operating_contract_v0.md
    - orca/product/spines/judgment/judgment_current_state_and_decomposition_v0.md
  downstream_surfaces_checked:
    - orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
    - docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
    - docs/decisions/orca_product_thesis_consumer_demand_v0.md
    - AGENTS.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
      reason: >
        Controlling claim-tier doc. Its Measurement Target already states "the
        quality of the decision under the case's evidence constraints" and "no
        outcome (resulting) bias"; the EV-regret sharpening is consistent with it
        and changes no claim tier, closeout state, cap, or the measurement-target
        principle. Checked, not changed.
    - path: docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
      reason: >
        Retrieval map; its "right-sized action under evidence constraints" Frozen
        Orientation Primitive is an excerpt that stays true (right-sized action
        remains the named component). The map's own rule is "the source wins on
        conflict"; a light excerpt refresh is deferred, not silently forked.
    - path: docs/decisions/orca_product_thesis_consumer_demand_v0.md
      reason: >
        OWNER_LOCKED product thesis. This is lane-internal judgment-evaluation
        doctrine, consistent with its "calibrated judgment + outcome memory" moat
        and "best move under evidence" central read; no product-thesis edit is
        authorized or required by this pass.
    - path: AGENTS.md
      reason: Behavior kernel; carries no judgment optimization-goal statement; routes lane doctrine to its owning docs.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: Source hierarchy + propagation contract owner; carries no judgment optimization target to update.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: Repo map routes to the judgment consolidation map and carries no optimization-goal statement.
  stale_language_search: >
    rg -in "right-sized action|over.?reach|under.?reach|best move under|highest.?(expected.?value|EV)"
    docs/research/judgment-spine orca/product/spines/judgment
  stale_language_search_result: >
    Executed 2026-06-20. Live judgment-doctrine surfaces carrying the
    optimization/measurement framing: this thesis (amended), the thesis operating
    contract (updated — "What The Thesis Optimizes For"), the evidence ladder
    Measurement Target (consistent, no outcome bias — not changed), the
    current-state decomposition Forecasting Boundary (note added), and the
    consolidation-map Frozen Orientation Primitive (excerpt, source-wins, refresh
    deferred). All other hits are historical/derived surfaces — review
    inputs/outputs, harness fixtures, prompts, migration proposals — not live
    controlling doctrine; none states an optimization target that now contradicts
    the sharpened goal (right-sized action is retained as a component).
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not judgment-quality evidence
    - mints no claim-tier or scoring vocabulary; target stays qualitative (no numeric EV/regret)
```

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
