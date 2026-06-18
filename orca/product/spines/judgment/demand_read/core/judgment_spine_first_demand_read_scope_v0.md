# Judgment-Spine First Demand-Read Scope v0 (PROPOSED — the run plan for the lane's first honestly-graded by-hand demand read)

```yaml
retrieval_header_version: 1
artifact_role: Run-scope / non-executing plan (PROPOSED — scopes the first by-hand demand read under the new C0–C4 core; authorizes no capture or run by itself; each capture + the run remain owner-gated)
scope: >
  The bounded plan for the demand-read lane's first earned-trust deliverable: one
  honestly-graded by-hand demand read on a real historical beauty case, run under
  the new qualitative C0–C4 core (C2 ledger read-contract + C3 verdict/ceiling
  contract), graded against a facilitator-only sealed outcome. Mode = historical
  BACKTEST, screened for persistence richness (owner decision 2026-06-15). Frames
  the case choice, the run procedure, the blind/isolation discipline, the
  enrichment captures needed + their authorization surface, the honest-grading
  method, and the stop conditions. Caps at product_learning.
use_when:
  - Authorizing or running the lane's first by-hand demand read.
  - Checking what the first read proves, what it does not, and which captures it still needs owner authorization for.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/judgment/demand_read/core/judgment_spine_demand_read_machinery_architecture_v0.md  # the C0–C4 core being run
  - orca/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md             # C2 (Weight) contract
  - orca/product/spines/judgment/demand_read/c3_verdict_action/judgment_spine_c3_verdict_action_ceiling_contract_v0.md  # C3 (Verdict + Ceiling) contract
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md               # the batch-1 case ledger (dev/holdout marking, anti-cherry-pick, execution rules)
  - docs/hygiene/topicals_case2_lane_log_v0.md                                           # the existing Topicals fixture state + blind rules + issue log
stale_if:
  - The owner changes the mode, the case, or the build-gate authorization.
  - The C2 or C3 contract, or the batch-1 execution rules / blind discipline, are amended.
  - The taxonomy/read-grammar is owner-adjudicated (re-derive the read against the operative grammar).
```

## Status

`PROPOSED` — run-scope, `product_learning` tier. Authored 2026-06-15 in the
demand-read first-earned-trust lane (worktree
`demand-read-first-earned-trust-slice1` off `origin/main`), under an owner
build-gate lift (2026-06-15) bounded to the first by-hand read work unit. **This
scope authorizes no capture and no run by itself**: each per-source archive
capture and the read execution remain owner-gated (per-operation network
authorization + the conductor run-gate). Owner decisions folded: build gate
lifted; mode = **historical backtest, screened for richness** (2026-06-15).

## Objective

Produce the lane's first **honestly-graded** demand read: run the new qualitative
C0–C4 core on one real historical beauty case, **outcome-blind**, emit a sealed
two-axis verdict + action ceiling, then **grade it against the facilitator-only
sealed outcome**. The point is evidence about the **method** — does C0–C4 produce
a coherent, defensible, honestly-graded durable/transient call — not a validated
demand call and not judgment quality.

## Case (CONFIRMED by owner 2026-06-15)

**Confirmed: enrich Topicals (batch-1 dev case #4 — DTC→nationwide Sephora at
~month 9, 2020–21).** Reuse its already-built, blind-safe assets on `origin/main`
(the facilitator-only sealed outcome
`docs/research/topicals_sephora_expansion_sealed_outcome_facilitator_only_v0.md`;
cutoff ≤ 2021-03-15; the frozen case dir
`orca-harness/cases/product_learning/topicals_retail_expansion_2021_v0/`), but
build a **richer information set** than its current single-org-motion-point packet.

Why this case over the alternatives:
- **Dev-eligible** — does not burn the #5 Lime Crime / #6 REFY holdouts on an
  exploratory first read.
- **Launch/demand family** — richer demand substrate than a subscription repricing
  (the thinness you flagged on Beauty Pie #3).
- **Blind scaffolding already exists and is verified** — sealed outcome is
  facilitator-only and never read by the main agent/owner; cutoff fixed; R6/freeze
  discipline already exercised on this case.
- **Contamination-manageable** — on a *first* read, a model "knowing" the outcome
  is the chief threat to the grade. Topicals' 2021 expansion outcome is far less
  memorized than a famous restock saga; manage residual fame via the JSG-08
  tell-audit and, if a recognition screen warrants, partial anonymization +
  decoy specifics (owner Q2 direction, must not alter any decision-relevant fact).

Documented alternative (NOT recommended for the first read): **The Ordinary
salicylic-acid restock-vs-reformulate (swap pool)** — the richest archive-visible
persistence signal (restock pressure is heavily archived in skincare communities),
but **high brand fame → high contamination risk**, and a full build from scratch.
Better held for a later read once the method's honesty is established.

Honest limit (structural, accepted): even enriched, a backtest stays **thin on the
forward-only axes** — archives do not preserve sellouts, restock magnitude, or
paid-promotion spend (taxonomy: durable is "the one persistence backtests can
support"; manufactured separation is forward/live-only). The first read is framed
as a **durable-vs-transient persistence read** on the axis backtests *can* support,
with the costly-behavior/integrity thinness named, not hidden.

## Run Procedure (C0–C4, by hand)

1. **C0 Frame.** The Topicals retail-expansion decision as a Decision Frame
   (decision question + live trigger + cutoff ≤ 2021-03-15).
2. **Information set (enriched, outcome-blind).** A zero-spoiler participant packet
   built by a constructor **not holding the sealed outcome**, carrying the
   archive-visible signals as of the cutoff (see Enrichment Captures).
3. **C1 Allow.** Apply the ratified G1/G2 Demand-Substrate Hard Gate (≥2 independent
   venue families; gradeable costly-behavior floor; integrity labels). Fail →
   disqualify/hold.
4. **C2 Weight.** Per the C2 contract: de-correlate (`derived_from`), map divergence
   (`diverges_from`), and read the **empty** signal-reliability ledger → record
   "no ledger track record," weight on in-case merits; carry caveats; apply Rule 3
   (manufactured-axis risk states; persistence-axis patterns routed to C3).
5. **C3 Verdict + Ceiling.** Per the C3 contract: emit the two-axis verdict
   (durable | transient, given real), defaulting to **transient** unless observed
   post-trigger persistence is in the information set; classify any persistence-axis
   pattern as transient with a cited discriminator; emit an action ceiling
   {act/phase/narrow/hold/defend} matched to horizon, capped by the floor/ceiling
   rule (≥2 converging origins for a material verb; engagement-only caps; weakest
   load-bearing evidence binds). Fill the sealed_call (recommendation, qualitative
   confidence_band, signals_used, required reasoning_trace).
6. **C4 Counterfactual.** "What evidence would change the answer?"

## Enrichment Captures (each owner-gated; this scope authorizes none)

Built only via the Source-Capture Armory runner ladder (`archive_org` adapter →
SourceCapturePacket → into the case dir `source_captures/`), never ad-hoc fetches;
gate-0 by-hand reads are exempt scouting and bind nothing. Each capture is a
**separate per-source network authorization** the owner must grant:

- **Org-motion trajectory** — additional ≤cutoff careers/ATS snapshots to lift the
  single 2021-03-03 point toward a trajectory (ISSUE-01 fix).
- **Community sentiment** — archived ≤cutoff threads (e.g. Reddit beauty subs,
  Mumsnet) on Topicals demand around the expansion, captured as raw bodies.
- **Trade press** — archived ≤cutoff coverage (Glossy / BeautyMatter / Retail Dive)
  of the expansion, as the org-motion / retail-placement corroborant.

Gate-0 feasibility (archive-visibility check) runs first per source; a source that
is not archive-backtestable ≤cutoff is reported as a gap, never inflated.

## Blind / Isolation Discipline

- **Outcome-blind, permanently:** the main agent and owner never read the
  `*sealed_outcome*` file; only a delegated outcome-aware subagent touches it (for
  gate-0 blind-safety and the eventual grade).
- **Constructor ≠ contestant ≠ facilitator:** the enriched packet is built
  outcome-blind; the read runs in a **fresh isolated session, web-off** (recorded);
  the required reasoning trace is emitted for the tell-audit.
- **R6 pre-freeze leakage review** of the enriched packet before any reveal
  (independent outcome-aware reviewer), as on the prior Topicals freeze.

## Honest-Grading Method

By hand, `product_learning`-capped:
- Reveal the sealed outcome (delegated outcome-aware subagent); compare the sealed
  **verdict + ceiling** against what actually happened on the **persistence axis**
  (did the demand persist past the trigger — durable — or decay — transient).
- Run the **JSG-08 tell-audit** on the reasoning trace: a call that asserts the
  outcome or cites non-brief knowledge with no derivation is a confirmed tell →
  contaminated / quarantined-as-data (recognition capacity alone is not
  contamination).
- Record direction-correct / ceiling-appropriate / cap-reasons-sound, and every
  miss, honestly.

## What This Proves / Does Not Prove

- **Proves (if it passes):** the C0–C4 method produces one coherent, defensible,
  honestly-graded durable/transient read on a real case — first earned trust at
  `product_learning` tier.
- **Does NOT prove:** judgment quality (needs N≥K + running contestants + reveal /
  calibration, JSG-08); validation; readiness; buyer proof; any transient-timing /
  decay-curve claim; manufactured-separation capability (forward-only).

## Stop Conditions

- Stop at this **scope** until the owner confirms the case and authorizes the
  specific enrichment captures (each its own network authorization).
- Stop the read at a graded result + an honest findings record; no key/harness
  iteration conditioned on a holdout; no promotion of any signal to a standing
  source-family; no ledger-row population beyond what the read records as "no track
  record"; claims stay `product_learning`.

## Next Authorized Step

Owner: (1) confirm the case (Topicals-enrich, or redirect); (2) authorize the
first enrichment capture(s) by source. Then: gate-0 feasibility per source →
build the enriched outcome-blind packet → R6 review → run the read in isolation →
grade. No capture or run proceeds without (2).

## Non-Claims

- Run-scope only; authorizes no capture, no run, no fixture admission, no ledger
  population, no live-API call. Each capture + the run are separately owner-gated.
- Not validation, readiness, buyer proof, or judgment-quality evidence; the first
  read caps at `product_learning`, N=1.
- Reuses the batch-1 case substrate and blind discipline; mints no new ladder,
  closeout-state, or claim-tier vocabulary. INV-1 holds (qualitative, no scoring).
- PROPOSED; reflects owner decisions of 2026-06-15 (gate lift; backtest-screened-
  for-richness mode; case = Topicals-enrich, owner-confirmed 2026-06-15). The
  enrichment captures and the run remain owner-gated.
```text
This is a non-executing run plan. It is not a run, not validation, and not proof
of readiness.
```
