# Work-Unit Fitness Reference (Goal + Success Signal) v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: >
  Proposed doctrine: bind a carried goal + success-signal "fitness reference"
  that intent-bearing reviews consume as their alignment bar, and that a scoped
  fused/scoping entry-gate requires before source-changing edits on
  goal-fitness-judged work. Enacted 2026-06-08 into review-lanes.md,
  prompt-orchestration.md, and the adversarial review template.
use_when:
  - Deciding how an Orca review checks an artifact's intent/direction, not just
    its internal consistency and doctrine conformance.
  - Deciding whether implementation (fused/scoping) may begin without a concrete
    goal and success signal.
  - Checking the review-side fitness-reference back-pressure rule.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/prompts/templates/review/adversarial_artifact_review_v0.md
downstream_consumers:
  - Orca review prompts (adversarial artifact review, code review)
  - fused / implementation-scoping entry for goal-fitness-judged work
branch_or_commit: ecr-sp3-timing-deriver-slice1 @ 518d844
stale_if:
  - Owner rejects or materially edits this proposal.
  - review-lanes.md Review Doctrine changes the commission-bound target/purpose model.
  - The workflow-goal-framing output shape (anchor goal + success signal) changes.
  - A later decision relocates goal/success-signal authoring into the overlay.
```

## Status

`ACCEPTED` and `ENACTED` 2026-06-08. The owner accepted this proposal and the
smallest-complete edits were applied in the same turn to `review-lanes.md`,
`prompt-orchestration.md`, and
`docs/prompts/templates/review/adversarial_artifact_review_v0.md`. The completed
propagation receipt is in Direction Change Propagation below. Enactment changes
durable review and workflow doctrine; it claims no validation, readiness, or
proof. Scope locked at enactment: adversarial artifact review only (code review
deferred); the reference lives in the review template plus a review-lanes rule
plus a prompt-orchestration default and the scoped gate — no new preflight schema
or validation gate.

## Decision

```yaml
decision_id: work_unit_fitness_reference_v0
status: proposed
reference_object: goal_plus_success_signal     # NOT the prompt; NOT intended-output-as-template
reference_form: pointer_preferred              # cite the controlling contract/decision when one exists; else compact prose
authoring_home: framing_scoping                # reuse workflow-goal-framing output; do NOT relocate into overlay
review_consumption: required_for_intent_bearing_targets   # back-pressure; reviewer never silently invents the bar
enforcement: review_backpressure_plus_scoped_fused_gate
fused_scoping_gate_scope: goal_fitness_judged_work_only    # technical/consistency work exempt
guardrail: reference_is_alignment_axis_to_attack_not_pass_bar
prompt_body_injection: no
goal_framing_relocation: no
```

The four bound elements:

1. **Reference object = goal + success signal.** Reviews of intent-bearing
   artifacts check the target against a stated goal and an observable success
   signal — *pointer-preferred*: cite the controlling upstream contract,
   decision, or gate that already carries the signal, and write fresh compact
   prose only when none exists. The reference is **not** the generating prompt
   (correlated with the commission; invites conformance-collapse) and **not** an
   intended-output template (pre-writes the answer; collapses review into
   diff-checking).

2. **Authored upstream, carried, not relocated.** The reference is authored at
   framing/scoping by reusing the existing `workflow-goal-framing` output
   (anchor goal + success signal) and carried with the work unit. The overlay
   *routes* that output; it does not restate or fork goal-framing.

3. **Review lanes consume it (back-pressure).** For an intent-bearing target, the
   review checks the target against the bound fitness reference. If no reference
   is bound, the review **names "no checkable success bar bound" as the gap**
   rather than silently reconstructing intent. This is the enforcement that pulls
   the reference upstream without a universal gate.

4. **Scoped fused/scoping entry-gate.** Goal-fitness-judged work must have a
   concrete goal + success signal bound before source-changing edits begin.
   Internal/technical work is exempt (see Discriminator). This is
   `back-pressure + scoped fused gate`, the owner-selected enforcement strength —
   not a standing overlay mandate on every work unit.

## Why — Problem And Evidence

**Original gap.** Orca review checks an artifact against doctrine (the overlay
authority sources) and against itself (internal consistency, downstream
executability). That catches *incoherent* or *rule-violating*, but not
*coherent-and-rule-clean-but-wrong-direction* — drift from the upstream intent
the work was meant to serve.

**Empirical finding (past-week corpus).** The gap is real but **already worked
around ad hoc**, not unaddressed:

- **Every review prompt already injects a fitness bar.** A census of
  `docs/prompts/reviews/` found success/decision-criteria language in **40 of 40**
  review prompts (1–5 instances each). The bar exists — it is hand-authored,
  per review, every time, and never carried.
- The mini-god-tier operating-structure review adjudicated against **ten explicit
  success-questions**, including Q10 *"safe for checkpoint 4 mixed-source trial?"*
  — a success signal in all but name
  (`docs/review-outputs/adversarial-artifact-reviews/source_capture_mini_god_tier_operating_structure_adversarial_review_v0.md`).
- The cross-family ECR plan review caught three real defects, all
  **claim-vs-ground-truth** (plan claim vs producer code / its own table /
  cited lines), not goal-drift
  (`docs/review-outputs/adversarial-artifact-reviews/ecr_consolidation_v0_plan_cross_family_review_v0.md`).
- Corpus drift findings are overwhelmingly **technical-consistency** (schema-key
  drift, hash mismatch, protocol/Pydantic mismatch, citation staleness) or fitness
  checked **against a bar the prompt supplied**.

**What this means for value (calibrated).** Binding the fitness reference does
**not** mainly unlock defects the careful reviews miss — those reviews already
author bespoke criteria. Its value is **consolidation, consistency, durability,
and a floor**: author the bar once upstream instead of re-authoring it in 40
prompts; guarantee every review (not just the meticulous ones, and not just the
prompts whose author remembered good questions) gets a fitness check; make the
bar falsifiable and carried. This is a reliability/cost/upstream-leverage gain,
not a new-detection gain. Confidence: high on the prompt census; moderate-high on
"drift findings are mostly technical" (two reports read in full plus a corpus
grep, not all reports read in full).

## Discriminator — What The Fused/Scoping Gate Covers

Gate trigger question: **is the work's correctness judged by fitness to an
external goal, or by internal/technical consistency against a known substrate?**

- **Fitness-judged — GATED** (requires a bound goal + success signal): proof
  packets, fixtures, calibration gates/receipts, operating structures, plans,
  product-proof artifacts, runbooks. Correctness = "does it achieve the intended
  outcome."
- **Consistency-judged — EXEMPT**: schema reconciliation, citation/grounding
  fixes, mechanical patches, vocabulary-enforcement edits, hash/provenance
  corrections. Correctness = "is it internally/technically consistent with the
  substrate."
- **Ambiguous:** prefer binding the reference when a pointer is cheap, but do not
  block source-changing edits absent the gate trigger; name the ambiguity rather
  than inventing a goal.

## Guardrail (Load-Bearing)

The fitness reference is an **added alignment axis the reviewer must also
attack** — the reviewer asks whether the goal/signal itself is the right one —
**never a pass-if-matches gate.** This matters precisely because the corpus shows
reviewers adjudicate rigorously against whatever bar they are handed: a *wrong*
bar would propagate just as rigorously. Reviews stay findings-first and remain
maximally adversarial about the bound bar's own fitness. The reference adds an
axis; it never narrows the commission-bound adversarial posture.

## Claim Boundary — What This Record Does Not Do

- Does not make the prompt the review bar.
- Does not relocate or fork `workflow-goal-framing`; it routes that skill's output.
- Does not add a multi-review synthesis lane.
- Does not change Orca review-lane model-neutrality.
- Does not create approval, validation, readiness, mandatory remediation, or
  patch authority; reviews remain findings-first decision input.
- Does not edit any overlay file or template; doctrine is unchanged until a
  separate accepted turn enacts the Propagation Plan.

## Direction Change Propagation

Completed receipt for this enactment, per the Doctrine Change Propagation
Contract in `.agents/workflow-overlay/source-of-truth.md`.

```yaml
direction_change_propagation:
  doctrine_changed: >
    Intent-bearing adversarial artifact reviews now anchor their decision
    criteria to a bound fitness reference (goal plus observable success signal,
    pointer-preferred); reviews name the gap when none is bound; and
    goal-fitness-judged source-changing work must bind a goal and success signal
    before edits begin. The reference is an alignment axis to attack, never a
    pass bar.
  trigger: review_authority
  related_triggers:
    - workflow_authority
    - lifecycle_boundary
  controlling_sources_updated:
    - .agents/workflow-overlay/review-lanes.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - docs/prompts/templates/review/adversarial_artifact_review_v0.md
    - docs/decisions/work_unit_fitness_reference_v0.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/communication-style.md
    - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/skill-adoption.md
    - AGENTS.md
    - CLAUDE.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/communication-style.md
      reason: >
        CA consumption item 4 ("Decision criteria: the criteria the review was
        asked to apply") already accommodates the fitness reference; no change
        needed.
    - path: docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
      reason: >
        Shared review rules defer to prompt-orchestration and review-lanes; the
        new rule lives there and is inherited. No fork added.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        The fitness reference is pointer-preferred to existing contracts already
        in source-loading scope; no new read-pack rule required.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The change creates no new validation gate and claims no validation;
        existing gates unchanged.
    - path: .agents/workflow-overlay/skill-adoption.md
      reason: >
        The scoped gate is overlay doctrine that fused / implementation-scoping
        read from the overlay; no adoption-status change.
    - path: AGENTS.md
      reason: >
        Existing terse pointers to review lanes and prompt orchestration already
        route to the owning overlay files; no duplication added.
    - path: CLAUDE.md
      reason: >
        Thin shim that loads AGENTS.md; must not duplicate Orca rules.
  scope_locked:
    - adversarial artifact review only; code/implementation review deferred
    - reference lives in the review template plus a review-lanes rule plus a
      prompt-orchestration default and the scoped gate; no new preflight schema
      or validation gate
  stale_language_search: >
    Ran rg -ni for
    "findings-first|decision criteria|commission-bound|review purpose|self-derive|fitness|success signal|goal"
    across review-lanes.md, prompt-orchestration.md, and the adversarial review
    template. Result: no contradicting language. Existing "decision criteria",
    "findings-first", and "commission-bound" usage is consistent with the new
    rule, which anchors decision criteria to a carried goal+signal for
    intent-bearing targets and stays findings-first. Existing ad-hoc review
    usage already includes "success signal" and "long-term goal" questions,
    corroborating the vocabulary.
  non_claims:
    - not validation
    - not readiness
    - not acceptance beyond the owner acceptance recorded here
    - not proof
```

## Deferred Work

- Extend the fitness reference to `workflow-code-review` if and when wanted; this
  enactment is adversarial artifact review only.
- Optional confirming trial: bind an explicit goal + success signal on one
  upcoming intent-bearing review and compare against the prior ad-hoc bar. The
  40/40 census already supplies most of this evidence, so the trial is
  confirmation, not a blocker.
- Watch the scoped gate's ambiguous-classification cases in early use; tighten
  the discriminator only if real misclassifications appear.
