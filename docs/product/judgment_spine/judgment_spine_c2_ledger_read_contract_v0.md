# Judgment-Spine C2 Ledger Read-Contract v0 (PROPOSED — how the demand-read core's C2 CONSUMES the signal-reliability ledger)

```yaml
retrieval_header_version: 1
artifact_role: Implementation-facing behavior/contract spec (PROPOSED consumer-side interface — what must be true when the demand-read core's C2 reads the signal-reliability ledger; binds no row, builds nothing, runs nothing)
scope: >
  The consumer-side contract for one named-but-unspecified step: how the
  demand-read core's C2 (Weight) reads the signal-reliability ledger and turns a
  per-signal K-of-N report-all tally into a QUALITATIVE reliability prior it
  interprets per-case in the reasoning trace — never a number it multiplies
  (INV-1). Fixes the query key, the mandatory caveats that travel into the trace,
  the absence/non-informative handling, the double-counting guard vs lessons, the
  INV-1 disqualifiers, and the advisory-only boundary. Producer side (how rows
  are written) stays owned by the ledger + near-half postmortem; this spec edits
  neither.
use_when:
  - Scoping or implementing how the demand-read core's C2 weights an allowed signal using the ledger.
  - Reviewing whether a C2 reasoning trace reads the ledger within INV-1 (no scoring engine).
  - Reconciling the ledger (per-signal trust) against the validated-lesson library (joint-configuration flag) at C2.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md             # the ledger this consumes (producer-side schema + discipline; #54)
  - docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md # the demand-read core whose C2(c) this specifies (commit e794b8f, branch-only)
stale_if:
  - The ledger schema changes (e.g., PR #64 lands — adds a per-row pre-specified resolution criterion + full denominator); re-reconcile the consumed-fields list.
  - The owner lifts the no-scoring boundary (INV-1); numeric weighting becomes admissible and the INV-1 disqualifiers below relax.
  - The core architecture amends C2's step shape or the de-correlate/diverge sub-steps.
  - The validated-lesson library's own read-contract lands and changes the ledger-vs-lesson level boundary.
```

## Status

`PROPOSED` — consumer-side behavior/contract spec, `product_learning` tier. It
**stabilizes what must be true** when C2 reads the ledger; it **binds no real
row, builds no query mechanism, runs no case, and edits neither the ledger
schema nor the FROZEN conductor.** It fills the consumer half of an interface the
core architecture names ("C2 weights per `decision_family` by *reading* the
ledger, qualitative, LLM-in-session, explained") but does not specify. Authored
2026-06-14 in the ledger-first continuation lane (worktree
`ledger-c2-read-contract-v0` off `origin/main`). Rule 3 (risk-state weighting) folded 2026-06-15,
re-grounded onto main's two-axis demand-state model — the cap lives on the
manufactured/integrity axis; persistence-axis patterns are transient verdicts
routed to C3, not caps.

## Input Basis (accepted)

- **Owner-ADOPTED demand-read core** (Decision B, 2026-06-14): the C0–C4 core is
  the demand-read judgment procedure; C2(c) reads the ledger. This spec
  operationalizes that read; it does not re-derive the core.
- **Ledger-first direction** (owner, 2026-06-14): the signal-reliability ledger
  is the *first* learning mechanism. Making it the *working* C2-weight substrate
  is exactly this spec's job.
- **Ledger `#54`** verified on `origin/main` (blob sha256[:16] `388352b83bac9860`,
  2026-06-14). PR #64 hardening **not landed**; this contract reads the `#54`
  field shape (see `stale_if`).
- **Consistency posture (owner decision, 2026-06-14 — amendment):** the C2 read's
  load-bearing, reproducible output is **direction + reasoning**; the qualitative
  weight *level* carries a **two-sided tolerance** (it may sit a band higher or
  lower), not a precise point. Informed
  by blind-read probe v2
  (`judgment_spine_c2_qualitative_read_feasibility_probe_v2.md`), which found the
  weight level drifts one qualitative band with framing while direction,
  load-bearing facts, and counterfactual stay stable. Adds Required Behavior
  items 7–8 below. Cross-model runs (4 brands) confirmed direction + reasoning are
  brand-independent and the dial sits within ≈one band; the residual reduced to a
  single open doctrine question — how C2 treats a known risk across evidentiary
  states (present / unconfirmed / absent) — now **resolved by Rule 3 below**
  (folded 2026-06-15, re-grounded onto main's two-axis demand-state model: the cap
  is on the manufactured axis; persistence-axis patterns are transient, routed to C3).

## Required Behavior

When C2 weights an allowed signal (one past the C1 gate) under an active `decision_family`, it must:

1. **Query by `(decision_family, signal_id)`.** Retrieve the signal's K-of-N
   report-all tally *scoped to that `decision_family`*, together with its
   `staleness` and `validation_status`. Reliability is read **within** a
   `decision_family`, never globally.
2. **Interpret the tally as a qualitative reliability prior, not a value.** The
   retrieved tally informs — but never determines — the in-session weight. The
   reasoning trace must carry a **per-case justification** for the weight C2
   assigns; the weight is the read's interpretation, not a quantity read off or
   computed from the tally.
3. **Make the honesty caveats travel.** Whenever the ledger informs a weight, the
   trace must carry: `N` (`n_scoreable`); a **small-N flag** when the ledger marks
   the tally small-N; the **staleness state** (a hit `stale_if` predicate or an
   aged `last_reviewed`); and the **excluded** `not_applicable` + `unscoreable`
   counts. A weight informed by a tally whose caveats are dropped is
   non-compliant.
4. **Handle absence as absence.** A signal with **no row**, an **empty tally**
   (`n_scoreable = 0`), or a tally with **no scoreable uses** (only
   `not_applicable`/`unscoreable`) yields **no reliability prior**: C2 weights the
   signal on its in-case merits and records "no ledger track record" in the trace.
   Absence is never read as a low — or high — reliability verdict.
5. **Keep ledger and lesson at different levels (double-counting guard).** A
   signal that appears both in the ledger and in a fired validated-lesson is
   carried as **two distinct trace entries**: the ledger as a **per-signal trust
   prior**, the lesson as a **configuration-level override**. The two are never
   summed, merged, or treated as mutually reinforcing into a single inflated
   weight.
6. **Stay advisory.** The read informs the weight inside the open (non-blind) C2
   assembly only. It never overrides a blind call, never admits/binds/unfreezes
   the signal's source-family, and never lifts the signal above its own evidence
   ceiling.
7. **Emit a direction with a two-sided tolerance on the level, not a precise point
   (owner decision, 2026-06-14).** The load-bearing output is the signal's
   **direction** (does it support / oppose / hedge the demand call) plus its
   **load-bearing facts and counterfactual** — not a precise weight level. The
   qualitative weight carries a **two-sided tolerance**: a read states a level
   (e.g., "moderate"), and a faithful re-read may land **one band higher *or*
   lower** without conflict — the give is **bounded (≈ one band) and runs either
   direction**, neither a precise point nor a wide swing — *provided* the reads
   agree on **direction, load-bearing facts, and counterfactual**. **Consistency is
   judged on direction + reasoning, not the exact level.** The tolerance is
   *qualitative* (a band, either way), never a number ± on a score — no number
   exists, so INV-1 holds.
8. **Classify each ambiguous caveat (ambiguity-handling rule).** For any caveat
   whose bearing is genuinely uncertain — e.g., "a risk with no evidence it is
   active," a small N, a borderline staleness — the trace must **state whether C2
   treats it as a cap (red flag), a discount (mark-down), or neutral, and why.** An
   ambiguous caveat that silently moves, or silently fails to move, the weight is
   non-compliant. (Probe v2 traced the entire band drift to one ambiguous caveat
   read as a cap under one framing and as neutral under another.)
9. **Apply Rule 3 — risk-state weighting across evidentiary states.** For a known
   **dispositive manufactured-axis (integrity) risk** to the signal — one that, if
   active, means the demand is **not real** — weight by the state the evidence is
   in: **confirmed-present → cap** (defeater); **unconfirmed → ceiling discount**
   banded on reversibility; **confirmed-absent → neutral baseline** (never
   positive). Persistence-axis patterns (resale/flip, event/one-time,
   scarcity/panic) are **not capped here** — they reclassify the read as
   **transient** and route to C3 (verdict + horizon-matched ceiling). The full
   rule, discriminator requirement, and the C3 hand-off are in the **Rule 3**
   section below.

## Rule 3 — Risk-State Weighting Across Evidentiary States (folded 2026-06-15)

Rule 3 governs how C2 weights a **known dispositive manufactured-axis (integrity)
risk** to an allowed signal across the three states evidence can leave it in. It is
re-grounded onto main's two-axis demand-state model (durable/transient +
real/manufactured): the **cap lives on the manufactured axis**; persistence-axis
patterns are **transient verdicts, not caps** (routed to C3). Qualitative,
INV-1-safe, advisory.

**Scope.** Rule 3 governs risks that, if active, mean the demand **is not real**
(fabrication / coordination — bots, fake accounts, review-stuffing, laundered
origination, costly-behavior staged inside a coordinated layer). It does **not**
govern: (i) **persistence-axis** patterns (resale/flip, event/one-time,
scarcity/panic) — real-but-decaying demand, reclassified **transient** and routed to
**C3** (verdict + horizon-matched ceiling), with their discriminator families
(use-vs-flip, repeat/persistence, persistence-after-normalization,
sell-through-vs-sell-in) re-homing there; (ii) **magnitude-only** markdowns
(ordinary C2 weighting); (iii) the gross genuine-vs-manufactured filter already
owned by the **C1 gate** (ratified G1/G2 — consumed, not reopened). Rule 3 is the
**per-signal residual**: a known manufactured-mechanism risk to a signal the gate
let through. Channel **sell-in ≠ sell-through** is an **owner judgment call**
(integrity-artifact vs transient), not auto-capped.

**Monotone chain:** on the trust ceiling, **cap ≤ discount ≤ neutral** (present ≤
unconfirmed ≤ absent); inherent-limit caps sit orthogonal, lowest applicable binds.
**Advisory, not control:** the read certifies a withheld/granted ceiling; it never
prohibits the owner's action.

- **R3(a) Confirmed-present → cap (defeater).** Evidence the risk is active (the
  discriminator's stated **sufficiency bar** met) caps the read: withhold the
  positive verdict on this dimension, regardless of positive evidence elsewhere —
  there is no real demand to weight. References the C1 gate's independence logic; it
  does not re-implement it.
- **R3(b) Unconfirmed → ceiling discount, two reversibility bands.** Boundary =
  whether the **committed portion** of the action is recoverable before its cost
  sinks (not the verb): recoverable → **mild** (proceed); not recoverable →
  **near-cap** (advise the recoverable path until checked). Recoverability is
  multi-dimensional — economic, reputational, operational, evidence-contamination —
  and the **least-recoverable dimension binds** (anti-slicing; a "small test" that
  manufactures the signal it would read is material, not reversible).
- **R3(c) Confirmed-absent → neutral baseline, never positive.** Verified-clean and
  risk-not-applicable both sit at the risk-absent baseline, above unverified (which
  bears the R3(b) discount); verified-clean earns **no positive credit** over
  not-applicable (anti-gaming; preserves AR-05).
- **R3(d) Discriminator companion (required) + status triple.** Each governed risk
  carries a present-fingerprint + an absent-clearing-check, each with a stated
  **sufficiency bar**. Core owns the requirement, shape, and per-class families; the
  vertical deck owns the specific tells. Status: **set-run** (fingerprint → cap /
  clearing-check → neutral / neither → inconclusive → near-cap, owner bets);
  **missing-but-buildable** (withhold the material green-light, advise the
  recoverable path, build the set); **impossible** (→ R3(e)). **Unlock rule:** a
  material/irreversible action earns a durable-grade green-light only by *running*
  the discriminator.
- **R3(e) Falsifiability filter + inherent-limit caps.** A risk with no possible
  clearing-check does not block via (a)–(c); it is a standing **inherent-limit cap**
  (orthogonal, not verification-clearable — archetype small-N) or discarded as noise.
- **FP/FN asymmetry.** C2 advises more strongly against a suspected-but-unproven risk
  the more **irreversible** the action it would authorize; the asymmetry is
  **bounded** (a judge that never certifies is inert), hardening toward a cap only as
  the bet becomes un-undoable. Verification is the unlock.

**Mini-god-tier / v2.** Qualitative now (bands, no probabilities; named limits:
thin-deck early conservatism, LLM-in-session residual variance, manual lesson
install, dispositive-checkable coverage, forward-capture cold-start). Numeric v2 is
an **intended migration hypothesis** (may decompose the bands into separate
variables: likelihood, evidence-quality, severity, action-lock-in), gated on a
calibration spine **and** the owner lifting INV-1.

## Non-Goals

- **No numeric/ordinal weight or apply-rule from the tally.** No fraction, score,
  rank, threshold table, formula, or deterministic lookup mapping K-of-N → weight.
  (INV-1; graduates only when the owner explicitly lifts the no-scoring boundary.)
- **No ledger-schema edit.** The contract consumes the ledger by pointer;
  ledger amendments go through the delegated-review-patch discipline, not here.
- **No producer-side behavior.** How rows are written (the firewall-clean
  pre-committed-use unit, the postmortem inflow) stays owned by the ledger + the
  near-half postmortem loop.
- **No cross-signal interaction.** De-correlation (`derived_from`) and divergence
  (`diverges_from`) across signals are C2 sub-steps (a)/(b); this contract is the
  per-signal ledger read, sub-step (c), one signal at a time.
- **No lesson read-contract.** This spec fixes only the *level separation*
  between ledger and lesson; the validated-lesson library's own read-contract is
  a separate object.
- **No build/run.** No row population, no query implementation, no by-hand case
  (build-tier, owner-gated).
- **No precise/reproducible point weight.** C2 is not required or expected to
  reproduce an identical weight *level* across reads; direction + reasoning are the
  reproducible outputs (item 7). Demanding exact-level reproducibility is out of
  scope and would push toward a scoring rule (INV-1).

## Interfaces / Contracts

- **Query key:** `(decision_family, signal_id)`. A tally from one
  `decision_family` must not be read as the signal's reliability in another.
- **Consumed ledger fields (read-only, by pointer):**
  `reliability.tally{k_correct, n_scoreable, excluded}`,
  `applicable_decision_families`, `validation_status`,
  `staleness{stale_if, last_reviewed}`, `provenance`. No field is mutated.
- **Output surface — the C2 portion of the required reasoning trace** must, for
  each signal the ledger informed, contain: the `(decision_family, signal_id)`
  read; the tally **as reported** (`K` of `N`, excluded counts); the caveats
  (small-N, staleness); and the per-case weight justification narrative.
- **Invariant honored:** INV-1 — the trace shows **interpretation, not
  arithmetic**; `validation_status` caps at `product_learning` and travels with
  the read.
- **Boundary honored:** the read cannot change source-family admission state
  (INV-6 / the ledger's no-promotion cap) or touch the blind-call firewall.

## Acceptance Criteria

- **INV-1 disqualifier:** for a signal with a ledger row in the active
  `decision_family`, the trace cites `(decision_family, signal_id)`, the K-of-N
  tally, and a per-case justification, and an auditor can find **no** step where
  the weight is a quantity computed from the tally alone. A computed/looked-up
  weight fails.
- **Scoping:** for one `signal_id` with rows in two `decision_family` values, a
  read that uses the **wrong-family** tally fails.
- **Caveat-travel:** for a tally the ledger marks small-N (or stale), the trace
  carries the small-N (or staleness) caveat; its absence fails.
- **Absence:** for a signal with no row / empty tally / no scoreable uses, the
  trace records "no ledger track record" and the weight rests on in-case merits;
  treating absence as a reliability verdict fails.
- **Double-counting:** for a signal present in both the ledger and a fired
  lesson, the trace shows two entries at different levels; a single
  combined/summed weight fails.
- **Advisory-only:** for a high K/N tally, the read does not promote/admit the
  source-family and does not raise the signal above its evidence ceiling; doing
  either fails.
- **Direction/band tolerance (item 7):** two faithful reads of the same case that
  agree on **direction, load-bearing facts, and counterfactual** but differ by one
  qualitative **band** are both compliant; a read that diverges on direction or
  load-bearing facts fails. Judging consistency on exact level (failing an
  adjacent-band read) is itself a violation of this criterion.
- **Ambiguity classification (item 8):** for a case carrying an ambiguous caveat,
  the trace explicitly labels it **cap / discount / neutral, with a reason**; an
  ambiguous caveat that moves or fails to move the weight without a stated
  classification fails.
- **Rule 3 axis scoping (item 9):** a persistence-axis pattern (resale / event /
  scarcity) treated as a **cap** fails — it must be classified transient and routed
  to C3; a confirmed-present manufactured-axis risk (sufficiency bar met) that does
  not cap fails.
- **Rule 3 evidentiary state (item 9):** an unconfirmed risk on an irreversible move
  that draws only a mild discount fails (least-recoverable binds); a verified-clean
  signal credited above risk-not-applicable fails (anti-gaming); a material
  green-light granted without *running* the discriminator fails.

## Checking Items 7–8 (enforcement posture)

These are **trace obligations audited as judgment, not gated as code** (INV-1 — no
automated scorer):

- **Enforce (per read):** the cap/discount/neutral classification (item 8) and the
  direction + load-bearing facts + counterfactual (item 7) are **required trace
  content**. A review / tell-audit of the reasoning trace flags any ambiguous
  caveat left unlabeled or any weight that moves on an unlabeled caveat; such a
  trace **fails review** — the same posture by which INV-1 itself is enforced (read
  the trace, not run a scorer).
- **Test (pre-use and ongoing):** the **blind paired-read** method (probe v2) — run
  the same case under ≥2 framings; pass requires agreement on direction +
  load-bearing facts + counterfactual, the level within the two-sided tolerance,
  and **every band difference attributable to a declared classification**, not
  silent drift.

## Open Questions

- **Small-N threshold and staleness-age cutoff — DEFERRED (safe).** The numeric
  cutoffs are the ledger producer's parameters (`staleness.stale_if`, the N-honesty
  rule). This consumer contract requires only that **whatever the ledger marks as
  small-N or stale travels into the trace** — not the cutoff value. Deferring it
  here cannot change the consumer behavior, only which tallies trip the caveat.

## Downstream Handoff

```yaml
spec_handoff:
  status: SPEC_COMPLETE_READY_FOR_SCOPING
  required_behavior: >
    C2 reads the ledger by (decision_family, signal_id), interprets the K-of-N
    report-all tally as a qualitative per-case reliability prior (never a computed
    weight), makes N/small-N/staleness/excluded caveats travel into the reasoning
    trace, treats no-row/empty/no-scoreable as no prior (weight on in-case merits),
    keeps the ledger (per-signal trust) and any fired lesson (joint-configuration
    flag) at different trace levels, stays advisory (no blind override, no
    source-family promotion, no ceiling lift), emits direction + reasoning with a
    two-sided tolerance on the level (one band either way, not a precise point;
    owner decision 2026-06-14), labels each ambiguous caveat
    cap/discount/neutral with a reason, and applies Rule 3 (risk-state weighting):
    a known dispositive manufactured-axis risk caps when confirmed-present,
    discounts (reversibility-banded) when unconfirmed, sits at a neutral baseline
    when confirmed-absent, while persistence-axis patterns are not capped but
    reclassified transient and routed to C3 (folded 2026-06-15, two-axis reground).
  non_goals:
    - numeric/ordinal weight or deterministic apply-rule from the tally (INV-1)
    - ledger-schema edits (consume by pointer; amend via delegated-review-patch)
    - producer-side row-writing behavior
    - cross-signal de-correlation/divergence (C2 sub-steps a/b)
    - the validated-lesson library's own read-contract
    - any build, row population, query implementation, or by-hand run
    - precise/reproducible point weight (direction + reasoning are the reproducible outputs)
  interfaces_contracts:
    - query_key: (decision_family, signal_id)
    - consumed_fields_read_only: [reliability.tally{k_correct,n_scoreable,excluded}, applicable_decision_families, validation_status, staleness{stale_if,last_reviewed}, provenance]
    - output_surface: the C2 portion of the required reasoning trace
    - invariant: INV-1 (interpretation not arithmetic); product_learning cap travels
  acceptance_criteria:
    - INV-1 disqualifier (no tally-computed weight in the trace)
    - decision_family scoping (wrong-family tally rejected)
    - caveat-travel (small-N / staleness present)
    - absence handling (no-row/empty -> "no ledger track record")
    - double-counting guard (ledger vs lesson at different levels)
    - advisory-only (no promotion, no ceiling lift)
    - direction/band tolerance (consistency judged on direction + reasoning, not exact level)
    - ambiguity classification (each ambiguous caveat labeled cap/discount/neutral with a reason)
    - rule 3 axis scoping (manufactured-axis risk caps; persistence-axis pattern not capped -> transient -> C3)
    - rule 3 evidentiary state (present->cap, unconfirmed->reversibility-banded discount, absent->neutral baseline; discriminator must be run for a material green-light)
  deferred_open_questions:
    - small-N threshold + staleness-age cutoff: ledger-owned; consumer only requires the caveat to travel
  review_timing_advisory:
    adversarial_review: recommended
    highest_value_checkpoint: after_artifact_pre_implementation
    review_target: docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md
    why_this_checkpoint: >
      This spec encodes INV-1 (no scoring engine) at the single point it is most
      tempting to cross — turning a K-of-N tally into a weight. A flaw here would
      let a deterministic scoring rule slip into C2 under cover of "qualitative."
      Review before an implementation-scoping lane or a by-hand run relies on it.
  scoping_may_rely_on: >
    the (decision_family, signal_id) query key; the qualitative-interpretation-
    not-arithmetic contract; the mandatory caveats; the absence handling; the
    ledger-vs-lesson level separation; and the advisory-only / no-promotion
    boundary. Open: the small-N/staleness numeric cutoffs (ledger-owned).
```

## Source-Read Ledger

- `docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md` — the
  ledger consumed; producer-side schema + discipline (K-of-N report-all,
  firewall-clean unit, product_learning cap, N7 field map). Compare target:
  sha256[:16] `388352b83bac9860` on `origin/main` (`#54`, verified 2026-06-14);
  reread-required if #64 lands.
- `docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md`
  — the demand-read core whose C2(c) this specifies; owner-ADOPTED, commit
  `e794b8f` (branch-only, not on `origin/main`). Reread-required; obtain from the
  sender branch.

## Claim Classification

```yaml
judgment_spine_claim_classification:
  evaluated_claim_surface: C2 ledger read-contract (consumer-side behavior/contract spec)
  source_quality_state: design/control artifacts only (ledger #54 + owner-adopted core architecture, read fresh); no real rows, no run
  execution_quality_state: no C2 read executed, no tally interpreted, no row populated
  closeout_state: no_durable_evidence
  claim_cap: design input / product-learning context only
  weakest_missing_or_failed_gate: no C2 read exists to test against; the ledger holds no real rows; review of this spec not yet run
  receipt_artifact_or_gap: first real test comes from a by-hand demand-read C2 read against a populated ledger (both owner-gated)
  non_claims:
    - not validation unless separately proven
    - not readiness unless separately proven
    - not buyer proof unless the buyer-proof receipt is complete
    - not judgment-quality evidence unless the judgment-quality receipt is complete
```

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    C2 read-contract Rule 3 (risk-state weighting across present / unconfirmed /
    absent evidentiary states) folded into this spec, re-grounded onto main's
    two-axis demand-state model: the cap lives on the manufactured / integrity
    axis; persistence-axis patterns (resale / event / scarcity) are transient
    verdicts routed to C3, not caps. Same edit renames the C1-derived object
    "admitted signal" -> "allowed signal" (the C1 step verb Admit -> Allow).
  trigger: product_doctrine
  related_triggers:
    - architecture_doctrine
  controlling_sources_updated:
    - docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md
    - docs/product/judgment_spine/judgment_spine_demand_read_machinery_architecture_v0.md
  downstream_surfaces_checked:
    - docs/product/product_lead/orca_demand_read_taxonomy_v0.md   # already two-axis + Calling Sequence (C3 transient handling); "hollow" hits are the retirement explanation, kept
  intentionally_not_updated:
    - path: source-family "admission"/"admissibility" + Demand-Substrate Hard Gate vocabulary (this spec's source-family admission lines; read-machinery "admission inputs"/"admissible")
      reason: the rename targets the C1 demand-signal step verb only; the ratified G1/G2 gate concept and the source-family admission state are consumed, not renamed or reopened.
    - path: docs/decisions/orca_c2_risk_state_weighting_v0.md (sender, ecr-sp3)
      reason: stale-frame INPUT superseded by this folded + re-grounded Rule 3; lives on a stale branch, retired by the reground.
  stale_language_search: >
    rg -i "admit|admitt|admiss|hollow" across the two edited spine docs (2026-06-15):
    residual hits are all intended-keep (source-family admission, gate
    admissibility, lesson-admission, the "hollow is retired" explanation); no "C1
    Admit", no "admitted signal", no live "durable-vs-hollow" verdict remains.
  non_claims:
    - not validation
    - not readiness
    - not a live fold to origin/main (per-lane PR pending)
```

## Non-Claims

- Behavior/contract spec only; binds no real row, builds no query mechanism,
  runs no case, edits neither the ledger schema nor the FROZEN conductor.
- Authorizes no implementation, scoring engine, automated scoring, runner, or
  storage. INV-1 holds: the ledger is a track record the C2 read interprets,
  never a number it multiplies.
- Mints no evidence-ladder vocabulary; reuses `signal_id` / `decision_family` /
  K-of-N report-all from the ledger and architecture.
- A reliability read is `product_learning` evidence about signal usefulness —
  never judgment-quality, never a source-family admission, never causation.
- PROPOSED only; not owner-adopted. On adoption it owes a dated pointer via the
  Doctrine-Change Propagation Contract (`.agents/workflow-overlay/source-of-truth.md`).
```text
This is advisory design input only. It is not a verdict, not implementation
authority, and not proof of readiness.
```
