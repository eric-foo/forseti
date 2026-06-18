# Demand-Read Core — Adoption + Ledger-First Learning Direction v0

```yaml
retrieval_header_version: 1
artifact_role: Product direction + owner-decision record (records owner sign-off on the demand-read core and sets the ledger-first learning priority)
scope: >
  Records the owner decisions made 2026-06-14 on the demand-read core
  architecture: ADOPT the core (Decision B), RESOLVE the retest-vs-cross-test
  question (Decision D), and prioritize the signal-reliability LEDGER as the
  first learning mechanism. Sets the direction a downstream lane picks up. No
  implementation authorized.
use_when:
  - Picking up the demand-read core / Judgment-Spine learning work after this session.
  - Checking what the owner has accepted vs what remains gated, and why the ledger comes first.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md   # the core architecture this adopts (Decisions B/D recorded here supersede its "unsigned" status)
  - orca/product/spines/judgment/learning_loops/near_half/near_half_signal_reliability_ledger_v0.md                 # the LEDGER this prioritizes (the first learning mechanism)
  - orca/product/spines/judgment/learning_loops/near_half/near_half_backtest_learning_architecture_v0.md             # the lesson loop + promotion gate (the second mechanism; harvested later)
stale_if:
  - The owner amends or reverses adoption, the ledger-first priority, or the retest/cross-test resolution.
  - The signal-reliability ledger schema changes (e.g., PR #64 lands) — re-reconcile the ledger-read references.
```

## Status

Owner decisions recorded **2026-06-14** (Eric, owner). The demand-read core
architecture object (`judgment_spine_demand_read_machinery_architecture_v0.md`,
commit `e794b8f`) is **PROPOSED**; this note records the owner's sign-off on its
two open decisions and sets direction. **No implementation is authorized** — the
pre-build assumption-gate's separate "authorize the build" step is NOT cleared by
adoption (see Boundaries).

## Owner Decisions

- **Decision B — ADOPTED.** The demand-read core (C0 Frame → C1 Allow → C2 Weight
  → C3 Verdict+Action-Ceiling → C4 Counterfactual) is accepted as the demand-read
  judgment procedure. It is a thin sibling: backtest mode = the core's sealed
  C3/C4 surface run as the FROZEN conductor's JSG-06 contestant (nothing grafted
  in); live mode = the core fills the far-half decision-object `sealed_call`. It
  CONSUMES the near-half / far-half / signal-reliability-ledger by pointer.
- **Decision D — RESOLVED.** The retest and the cross-test are **complementary and
  sequential, not competing**:
  - **Retest (PROVE)** = re-run the *same* case on a fresh same-family instance
    armed with the candidate lesson; keep if materially better. It proves the
    **distillation works** (the lesson is real and usable). Runnable now (N=1).
  - **Cross-test** = run the lesson on *another* case to prove **generalization**.
    Setup: lessons must be stated as **family-scoped firing patterns** (trigger +
    adjustment + `decision_family`), tested on other cases **in the same
    decision_family** with **report-all** (helped / hurt / not-applicable /
    unscoreable). "Too different to apply" cases are reported as `not_applicable`
    and correctly withhold promotion — heterogeneity withholds, it does not break.
    The cross-test is **data-blocked now** (too few cases per family); the lever to
    make it reachable is **deliberately selecting backtest cases in same-family
    clusters** instead of one case per family.

## Direction: Ledger First

Between the two learning mechanisms, **prioritize the signal-reliability ledger**
(`near_half_signal_reliability_ledger_v0.md`) as the durable spine and first
focus. Rationale:

- **Heterogeneity-robust:** a *signal* (org-motion, review-velocity) recurs across
  many cases even when the cases differ; a compound *lesson* recurs rarely. The
  ledger accumulates usefully now; lessons stay data-blocked longer.
- **Honest by construction:** K-of-N report-all, `decision_family`-scoped,
  `product_learning` cap, small-N caveats travel with every use — it is the moat
  and it is hard to fake.
- **Lessons are the bonus, not the first build:** they are the client-facing
  door-opener (insight) and the tail-catcher (manufactured-demand traps), harvested
  opportunistically as patterns recur. (Reasoned recommendation, not buyer-validated.)

### How the two are used together (C2 Weight)

Layered, both qualitative and shown in the reasoning trace:
1. **Ledger** sets the baseline trust on each allowed signal (reliability prior).
2. **Lessons** fire as configuration-level **overrides on top** when a validated,
   citation-disjoint, family-matched trigger appears (discount / flip a divergence
   / cap the ceiling), justified per-case.
3. **Guard against double-counting** a signal that appears in both (ledger = per-signal
   trust; lesson = joint-configuration flag — keep them at different levels).

### Conductor vs Core (clarification)

The **Core** makes the judgment; the **Conductor** only *grades* the Core's
backtests against known outcomes (never judges — its No-Authority Invariant).
Market the Core's judgment; back it with the Conductor's blind-scored receipts —
**which do not exist yet** (no contestant-execution runner; by-hand cap;
`product_learning`).

## Boundaries / Non-Claims

- PROPOSED + `product_learning`; not validated, not buyer-proof, not readiness.
- **INV-1 no scoring engine** (qualitative LLM-in-session weighting; the ledger is
  a track record the read interprets, never a number it multiplies, and a weight
  must be re-justified per case in the trace).
- **INV-2** don't edit the FROZEN JSG-01..10 conductor; consume siblings by pointer.
- **No implementation authorized.** Adoption signs Decisions B/D only. Building or
  populating the ledger, authoring an implementation-facing core spec, or running a
  by-hand case all require an **explicit bounded owner authorization** that does not
  yet exist (the conductor's own run-gate + the overlay's bounded-implementation
  rule). The assumption-gate BLOCKED the build pending that authorization.

## Next

A ledger-focused continuation lane (see the handoff in
`docs/prompts/handoffs/`) picks this up: deepen / pressure-test the
signal-reliability ledger as the first learning mechanism, within the boundaries
above. Implementation remains gated on an explicit owner build authorization.
