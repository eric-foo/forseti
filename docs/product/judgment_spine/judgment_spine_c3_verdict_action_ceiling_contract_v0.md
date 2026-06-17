# Judgment-Spine C3 Verdict + Action-Ceiling Contract v0 (PROPOSED — how the demand-read core's C3 turns weighted signals into a verdict + action ceiling)

```yaml
retrieval_header_version: 1
artifact_role: Implementation-facing behavior/contract spec (PROPOSED binding-side interface — what must be true when the demand-read core's C3 emits the demand-state verdict + action ceiling; binds no row, builds nothing, runs nothing)
scope: >
  The binding-side contract for one owner-ADOPTED-but-unspecified step: how the
  demand-read core's C3 (Verdict + Action Ceiling) turns the C2-weighted allowed
  signals into a two-axis demand-state verdict (durable / transient, given real)
  and an action ceiling (act / phase / narrow / hold / defend) matched to the
  demand's lifespan, filling the far-half decision-object sealed_call. Specifies
  C3 to the depth the C2 ledger read-contract already has. Qualitative,
  LLM-in-session, explained — never a number (INV-1). Consumes the C1 gate and
  the C2 weighting + Rule 3 routing by pointer; edits neither.
use_when:
  - Scoping or running the demand-read core's C3 (emitting a verdict + action ceiling).
  - Reviewing whether a C3 reasoning trace stays within INV-1 (no scoring engine) and the buyer-proof ceiling-cap rule.
  - Checking that a verdict obeys the calling sequence (transient-default; durable earned via observed persistence) and the two-axis model.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md  # the demand-read core whose C3 this specifies (C3 step shape; owner-ADOPTED Decision B)
  - docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md             # the C2 step C3 consumes (weighted signals; Rule 3 routes persistence patterns here)
  - docs/product/product_lead/orca_buyer_proof_packet_v0.md                              # the action-ceiling cap rule (floor vs ceiling; >=2 converging origins; engagement-only caps)
  - docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md      # the sealed_call output surface C3 fills (recommendation / confidence_band / signals_used / reasoning_trace)
  - docs/product/search/orca_demand_read_taxonomy_v0.md                            # the read grammar (two-axis model + calling sequence + read types) C3 verdicts in
stale_if:
  - The core architecture amends C3's step shape, the two-axis verdict, or the calling sequence.
  - The buyer-proof action-ceiling cap rule (floor/ceiling, >=2 converging origins, engagement-only cap) is re-derived.
  - The far-half decision-object sealed_call slot shape or the contestant confidence-band vocabulary changes.
  - The owner lifts the no-scoring boundary (INV-1); a numeric/ordinal ceiling mapping then becomes admissible and the INV-1 disqualifiers below relax.
  - The taxonomy/read-grammar is owner-adjudicated and amends the read types or the durable/transient/manufactured states.
```

## Status

`PROPOSED` — binding-side behavior/contract spec, `product_learning` tier. It
**stabilizes what must be true** when C3 emits the verdict + action ceiling; it
**binds no real row, runs no case, and edits neither the C1 gate, the C2
contract, the FROZEN conductor, nor the far-half loop.** It fills the binding
half of a step the core architecture names and the owner ADOPTED (Decision B,
2026-06-14: "C3 Verdict+Action-Ceiling") but does not specify to contract depth —
only C2 had a read-contract. Authored 2026-06-15 in the demand-read first-earned-trust
lane (worktree `demand-read-first-earned-trust-slice1` off `origin/main`), under an
owner build-gate lift bounded to the first by-hand read work unit. C3 is the
step whose output the first read's whole claim rests on; specifying it to C2's
depth is what lets a read be run without inventing the verdict+ceiling intent.

## Input Basis (accepted)

- **Owner-ADOPTED demand-read core** (Decision B, 2026-06-14): the C0–C4 core is
  the demand-read judgment procedure; **C3 emits the verdict + action ceiling.**
  This spec operationalizes that step; it does not re-derive the core.
- **Two-axis demand-state model** (settled, main #78 `c36e09c2`): durable/transient
  (persistence) + real/manufactured (integrity); "hollow" retired. C3 verdicts on
  this model.
- **Calling sequence** (taxonomy, owner 2026-06-14): first call defaults to
  **transient** (the conservative default — durable is the over-claimable label);
  **durable is earned via observed persistence, not predicted at the trigger.**
- **C2 contract** (`SPEC_COMPLETE`, Rule 3 folded): C3 consumes C2's per-signal
  weighted reads (direction + reasoning + qualitative band + caveats) and the
  **persistence-axis discriminator findings Rule 3 routes to C3**; the
  **manufactured-axis** integrity defeaters are resolved **upstream** (C1 gate +
  C2 Rule 3), so C3 receives a **real** (or already-disqualified/held) input.
- **Action-ceiling cap rule** (buyer-proof packet, ratified): **floor** = gradeable
  costly behavior (can you act at all); **ceiling** = integrity/independence (how
  bold); material/irreversible commitment requires **≥2 independent converging
  origins**; single origin caps at hold/low-commitment; engagement/attention alone
  cannot carry Commit-grade and caps the ceiling.
- **Output surface** (far-half decision-object): C3 fills the `sealed_call`
  (`recommendation`, `confidence_band`, `signals_used`, `reasoning_trace`); the
  sealed C3/C4 + trace is the JSG-06 scoreable child.

## Required Behavior

When C3 runs over the C2-weighted allowed signals for a **real** (not
manufactured) demand under an active `decision_family` and Decision Frame (C0), it must:

1. **Emit a two-axis demand-state verdict.** State the **persistence** verdict —
   **durable** or **transient** — given the **real** integrity disposition resolved
   upstream. The verdict is on main's two-axis model; a single-axis or "hollow"
   verdict is non-compliant.
2. **Default to transient unless observed persistence is in the information set.**
   **Durable requires observed post-trigger persistence evidence in the read's
   information set.** A read whose information set ends at (or before) the trigger —
   no observed persistence — **cannot call durable**; it calls **transient** and
   acts **in-window**. (A historical/backtest read whose window shows persistence
   past the trigger may call durable; a live t=0 read may not — durability is the
   *earned* state.)
3. **Classify persistence-axis patterns here as transient, not as caps.** A
   persistence-axis pattern (resale/flip, event/one-time, scarcity/panic), carried
   in via C2 Rule 3 with its discriminator family, **reclassifies the read as
   transient** and sets a **horizon-matched, time-boxed** ceiling. It is **never**
   treated as a manufactured-axis cap (that axis is upstream). The trace must cite
   the discriminator that supports a transient classification.
4. **Emit an action ceiling from the fixed vocabulary** `{act, phase, narrow, hold,
   defend}`, **matched to the demand's lifespan**: durable → long-horizon **commit**;
   transient → short-horizon **move**, time-boxed to the in-window action. The
   ceiling verb is the read's interpretation, justified per-case in the trace.
5. **Cap the ceiling by the weakest load-bearing evidence (floor/ceiling rule).**
   - A **material/irreversible** verb (act / phase / narrow / a costly-or-committing
     defend) requires **≥2 independent converging origins**; on a **single**
     independent origin the ceiling caps at **hold / low-commitment**.
   - **Engagement / attention-only** evidence (no gradeable costly behavior) **cannot
     carry a Commit-grade** recommendation; it caps the ceiling.
   - The ceiling is **tiered by costly-behavior strength** (one gradeable instance →
     hold/low-commitment; a corroborated pattern → higher) and is **never stronger
     than the weakest load-bearing evidence** supports.
   - **Defend is not automatically low-commitment**: a costly/committing defend is
     material and takes the ≥2-origin bar.
6. **Consume, don't re-adjudicate, the manufactured axis and the gate.** The
   manufactured-axis defeat (and the ratified G1/G2 Demand-Substrate Hard Gate) are
   settled upstream (C1 + C2 Rule 3). C3 receives a real-or-disqualified input and
   **does not reopen** either; if upstream disqualified/held the read, C3 emits no
   stronger verdict than that disposition allows.
7. **Fill the sealed_call output surface.** Populate `recommendation` (option +
   action shape consistent with the ceiling), `confidence_band` (a **qualitative
   band**, **reusing the contestant band-claim vocabulary — not a new one**),
   `signals_used` (each tagged with its `signal_id`), and a **required
   `reasoning_trace`** carrying the verdict, the persistence basis (or its
   absence), the horizon, the ceiling verb, and **every cap reason** (independence
   count, costly-behavior strength, engagement-only). The sealed C3/C4 + trace is
   the JSG-06 scoreable child.
8. **Stay qualitative (INV-1).** The verdict, horizon, ceiling verb, and
   confidence_band are **qualitative classifications with reasons** — no number,
   score, formula, or deterministic table maps an independence-count, weight band,
   or signal strength to a ceiling. (The ≥2-origin bar is the ratified gate's
   **structural independence count**, consumed as a gate condition — not a computed
   weight.) `validation_status` caps at `product_learning` and travels with the read.

## Non-Goals

- **No manufactured-axis re-adjudication.** The integrity defeat and the G1/G2 gate
  are upstream (C1 + C2 Rule 3); C3 consumes their disposition, does not reopen it.
- **No numeric/ordinal ceiling or apply-rule.** No score, fraction, rank, threshold
  table, or formula mapping independence-count / weight band / signal strength → a
  ceiling verb. (INV-1; graduates only when the owner explicitly lifts no-scoring.)
- **No decay-curve prediction / transient-timing forecast.** Durability is
  **observed via monitoring, not predicted**; C3 does not forecast a decay window or
  a persistence probability. The decay-curve capability does not exist.
- **No new confidence vocabulary.** `confidence_band` reuses the contestant
  band-claim shape by pointer; C3 mints none.
- **No beauty-specific verb-tiering.** Which verbs map to which ceiling in beauty
  (and the per-vertical discriminator *tells*) is **satellite** (vertical deck), not
  this core contract; C3 owns only the requirement that the mapping and the
  transient discriminator be cited in the trace.
- **No C2 re-weighting.** C3 consumes C2's weighted signals; it does not re-run the
  ledger read, the de-correlate/diverge sub-steps, or Rule 3.
- **No live-loop / monitoring behavior.** Seal-before-disclose, the monitor that
  earns the transient→durable upgrade, and resolution are owned by the far-half
  shell; C3 is the single-read verdict step that fills the sealed_call.
- **No build/run beyond the authorized first by-hand read.** No row population, no
  runner, no automated scorer.

## Interfaces / Contracts

- **Inputs (read-only, by pointer):** the active `(decision_family, Decision Frame)`
  (C0); the **C2-weighted allowed signals** (each: direction, per-case reasoning,
  qualitative weight band, `signal_id`, travelled caveats); the **integrity
  disposition** (real / disqualified-or-held) from C1 + C2 Rule 3; the
  **persistence-axis discriminator findings** routed from C2 Rule 3.
- **Outputs:** the `sealed_call` slots — `recommendation`, `confidence_band`
  (qualitative band, contestant vocabulary), `signals_used` (each tagged
  `signal_id`), `reasoning_trace` (required) — plus the **demand-state verdict**
  (`durable | transient`, given `real`) and the **action ceiling**
  (`act | phase | narrow | hold | defend`) with its **horizon** (`commit | move`).
- **Invariants honored:** INV-1 (qualitative, no scoring; `product_learning` cap
  travels); the **calling-sequence default** (transient unless observed persistence;
  durable earned, never asserted at t=0); INV-6 (consume the ratified gate, don't
  reopen).
- **Boundary honored:** C3 fills the sealed surface only; it does not run the live
  monitor, predict decay, re-adjudicate the manufactured axis, promote a
  source-family, or lift a signal above its evidence ceiling.

## Acceptance Criteria

- **Two-axis verdict:** a read that emits a single-axis or "hollow" verdict, or omits
  the persistence (durable|transient) call, fails.
- **Transient-default / earned-durable:** a read whose information set shows **no
  observed post-trigger persistence** that nonetheless calls **durable** fails;
  durable requires persistence evidence in the information set.
- **Persistence-pattern routing:** a persistence-axis pattern (resale / event /
  scarcity) treated as a **manufactured cap** fails — it must classify the read
  **transient** with a time-boxed ceiling and **cite its discriminator**.
- **Ceiling vocabulary:** a ceiling verb outside `{act, phase, narrow, hold, defend}`
  fails.
- **Independence cap:** a **material/irreversible** verb (act/phase/narrow/costly-defend)
  emitted on a **single** independent origin fails (must cap at hold/low-commitment
  unless ≥2 converging independent origins).
- **Engagement-only cap:** a **Commit-grade** ceiling carried by engagement/attention-only
  evidence (no gradeable costly behavior) fails.
- **Weakest-evidence cap:** a ceiling stronger than the weakest load-bearing evidence
  supports fails.
- **Sealed_call fill:** a read that omits `recommendation`, `confidence_band`,
  `signals_used` (tagged `signal_id`), or `reasoning_trace` fails; a `confidence_band`
  stated as a number or a newly-minted vocabulary fails.
- **INV-1 disqualifier:** an auditor can find **no** step where the ceiling verb or
  the confidence_band is computed from a number/formula/threshold; a computed ceiling
  fails.
- **Trace content:** the trace carries the verdict + persistence basis (or its
  absence) + horizon + ceiling + **every cap reason**; a verdict or ceiling that moves
  without a stated reason fails.
- **Consume-don't-reopen:** a read that re-adjudicates the manufactured-axis defeat
  (settled at C1/C2) or reopens the G1/G2 gate fails.

## Open Questions

- **Contestant `confidence_band` vocabulary — DEFERRED (safe).** The exact band
  levels are owned by the contestant / decision-object contract; this spec requires
  only that C3 **reuse** that vocabulary (no new one) and state a qualitative band.
  Deferring the level list cannot change C3's behavior, only which label a band
  carries.
- **Per-vertical discriminator *tells* and verb→ceiling mapping — DEFERRED (safe).**
  Satellite-owned (the beauty deck). C3 owns the *requirement* that a transient
  classification cite a discriminator and that the verb→ceiling mapping be justified;
  the specific beauty tells are not core.
- **Observed-persistence threshold for the transient→durable upgrade — DEFERRED
  (safe).** Owned by the far-half monitoring loop, not the single-read verdict step.
  A first read cannot reach durable without persistence in its information set, so
  deferring the live-monitor threshold cannot change first-read behavior.

## Downstream Handoff

```yaml
spec_handoff:
  status: SPEC_COMPLETE_READY_FOR_SCOPING
  required_behavior: >
    C3 turns the C2-weighted allowed signals (for a real, not-manufactured demand)
    into a two-axis demand-state verdict (durable | transient, given real) and an
    action ceiling (act | phase | narrow | hold | defend) matched to the demand's
    lifespan (durable -> commit, transient -> move, time-boxed). It defaults to
    transient unless observed post-trigger persistence is in the information set
    (durable is earned, never asserted at t=0); classifies persistence-axis patterns
    (resale / event / scarcity, routed from C2 Rule 3 with a cited discriminator) as
    transient, not as caps; caps the ceiling by the weakest load-bearing evidence
    (>=2 independent converging origins for a material/irreversible verb; single
    origin -> hold/low-commitment; engagement-only cannot carry Commit-grade; defend
    is not automatically low-commitment); consumes (does not reopen) the manufactured
    axis and the ratified G1/G2 gate; fills the sealed_call (recommendation,
    qualitative confidence_band in the contestant vocabulary, signals_used tagged
    by signal_id, required reasoning_trace carrying verdict + persistence basis +
    horizon + ceiling + every cap reason); and stays qualitative (INV-1, no number).
  non_goals:
    - manufactured-axis re-adjudication or G1/G2 reopen (upstream C1 + C2 Rule 3)
    - numeric/ordinal ceiling or deterministic apply-rule from independence-count/strength (INV-1)
    - decay-curve prediction / transient-timing forecast (durability observed, not predicted)
    - new confidence vocabulary (reuse the contestant band-claim shape)
    - beauty-specific verb-tiering and per-vertical discriminator tells (satellite)
    - C2 re-weighting (consume C2's output; do not re-run the ledger/de-correlate/diverge/Rule 3)
    - live-loop / monitoring / resolution behavior (far-half shell)
    - any build, row population, runner, or automated scorer beyond the authorized first by-hand read
  interfaces_contracts:
    - inputs_read_only: [active (decision_family, Decision Frame), C2-weighted allowed signals (direction + reasoning + qualitative band + signal_id + caveats), integrity disposition (real | disqualified/held) from C1+C2, persistence-axis discriminator findings from C2 Rule 3]
    - outputs: [demand_state_verdict (durable|transient, given real), action_ceiling (act|phase|narrow|hold|defend) + horizon (commit|move), sealed_call{recommendation, confidence_band, signals_used, reasoning_trace}]
    - invariants: [INV-1 (qualitative, no scoring; product_learning cap travels), calling-sequence default (transient unless observed persistence), INV-6 (consume the gate, don't reopen)]
  acceptance_criteria:
    - two-axis verdict present (no single-axis / hollow verdict)
    - transient-default / earned-durable (no durable without observed persistence in the information set)
    - persistence-pattern routed to transient with a cited discriminator (not a manufactured cap)
    - ceiling drawn from {act, phase, narrow, hold, defend}
    - independence cap (material verb needs >=2 converging origins; single origin -> hold/low-commitment)
    - engagement-only cap (no Commit-grade on attention-only evidence)
    - weakest-load-bearing-evidence cap
    - sealed_call filled (recommendation + qualitative confidence_band + tagged signals_used + reasoning_trace)
    - INV-1 disqualifier (no number/formula-computed ceiling or band)
    - trace carries verdict + persistence basis + horizon + ceiling + every cap reason
    - consume-don't-reopen (no manufactured re-adjudication, no G1/G2 reopen)
  deferred_open_questions:
    - contestant confidence_band vocabulary (decision-object owned; consumer reuses by pointer)
    - per-vertical discriminator tells + verb->ceiling mapping (satellite / beauty deck)
    - observed-persistence threshold for transient->durable upgrade (far-half monitoring loop; unreachable in a first read)
  review_timing_advisory:
    adversarial_review: recommended
    highest_value_checkpoint: after_artifact_pre_implementation
    review_target: docs/product/judgment_spine/judgment_spine_c3_verdict_action_ceiling_contract_v0.md
    why_this_checkpoint: >
      C3 is the step whose verdict + ceiling the first by-hand read's whole claim
      rests on, and it encodes INV-1 at a tempting crossing point — turning an
      independence-count and a costly-behavior strength into a ceiling verb. A flaw
      here would let a deterministic ceiling rule slip in under cover of
      "qualitative," or let a first read overclaim durable. Review before the
      first-read scope relies on it.
  scoping_may_rely_on: >
    the two-axis verdict contract; the transient-default / earned-durable rule;
    the persistence-pattern -> transient routing; the {act,phase,narrow,hold,defend}
    ceiling vocabulary; the floor/ceiling cap rule (>=2 converging origins,
    engagement-only cap, weakest-evidence cap); the consume-don't-reopen boundary;
    the sealed_call output surface; and INV-1. Open: the contestant band vocabulary,
    the per-vertical discriminator tells, and the live-monitor persistence threshold
    (all deferred-safe, none blocking a first read).
```

## Source-Read Ledger

- `docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md`
  — the core whose C3 this specifies (C3 step shape; two-axis C3 verdict; persistence
  patterns classified at C3; owner-ADOPTED Decision B). Compare target: `C1 — Allow`
  + C3 two-axis verdict present on `origin/main` (#125 squash `2b45001b`). reread-required.
- `docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md` — the C2
  step C3 consumes; Rule 3 routes persistence-axis patterns to C3. Compare target:
  `Rule 3 — Risk-State Weighting` present on `origin/main` (#124 squash `3ccc86ef`).
  reread-required.
- `docs/product/product_lead/orca_buyer_proof_packet_v0.md` — the action-ceiling cap
  rule (floor vs ceiling; ≥2 converging origins for material commitment; engagement-only
  caps the ceiling; defend not auto-low-commitment; Scoring engines on the do-not-build
  list). On `origin/main` (re-grounded #130). reread-required.
- `docs/product/judgment_spine/prospective_decision_loop_target_architecture_v0.md` —
  the sealed_call output surface (recommendation / confidence_band / signals_used /
  reasoning_trace). On `origin/main`. reread-required.
- `docs/product/search/orca_demand_read_taxonomy_v0.md` — the read grammar
  (two-axis model + calling sequence + read types) C3 verdicts in. Status
  `PROPOSED_PENDING_OWNER_ADJUDICATION` on `origin/main`. reread-required; the grammar
  is not yet owner-adjudicated as operative.

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: C3 verdict + action-ceiling contract (binding-side behavior/contract spec)
  source_quality_state: design/control artifacts only (owner-adopted core architecture + C2 contract + ratified buyer-proof cap rule + far-half sealed_call + taxonomy, read fresh on origin/main); no real read, no run
  execution_quality_state: no C3 verdict executed, no ceiling emitted, no case run
  closeout_state: no_durable_evidence
  claim_cap: design input / product-learning context only
  weakest_missing_or_failed_gate: no C3 read exists to test against; the first by-hand read against this contract is not yet run; review of this spec not yet run
  receipt_artifact_or_gap: first real test comes from the authorized first by-hand demand read emitting a C3 verdict + ceiling against this contract
  non_claims:
    - not validation unless separately proven
    - not readiness unless separately proven
    - not buyer proof unless the buyer-proof receipt is complete
    - not judgment-quality evidence unless the judgment-quality receipt is complete
```

## Non-Claims

- Behavior/contract spec only; binds no real row, runs no case, edits neither the C1
  gate, the C2 contract, the FROZEN conductor, nor the far-half loop.
- Authorizes no scoring engine, automated scorer, runner, or storage. INV-1 holds: the
  verdict, horizon, ceiling, and confidence_band are qualitative classifications the
  read justifies, never numbers it computes.
- Mints no evidence-ladder or confidence vocabulary; reuses `decision_family` /
  `signal_id` / the two-axis states / the action-ceiling vocab / the contestant
  band-claim shape from the architecture, taxonomy, buyer-proof packet, and far-half loop.
- **Stabilizes, does not change, the adopted C3 step.** C3's shape is already
  owner-ADOPTED (Decision B); this spec specifies it to contract depth. It is PROPOSED
  and not yet owner-adopted as the operative C3 contract; on adoption it owes a dated
  pointer via the Doctrine-Change Propagation Contract
  (`.agents/workflow-overlay/source-of-truth.md`). It changes no other live doc, so no
  propagation receipt is owed now.
- A C3 verdict is `product_learning` evidence about a demand read — never validated,
  decision-grade, buyer-proven, or judgment-quality.
```text
This is advisory design input only. It is not a verdict, not implementation
authority, and not proof of readiness.
```
