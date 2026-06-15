# Judgment-Spine C2 Qualitative-Read Feasibility Probe v0 (PROPOSED — does INV-1's qualitative tally-read actually exist?)

```yaml
retrieval_header_version: 1
artifact_role: Feasibility probe (design/docs demonstration — pressure-tests whether a coherent, non-vacuous qualitative read of a K-of-N tally exists, as INV-1 asserts; verdict PENDING de-correlated grading; binds no row, builds nothing, runs nothing)
scope: >
  A pre-registered, crossed-cell pressure-test of the single load-bearing
  assumption under the C2 ledger read-contract: INV-1's premise that a reasoning
  step can read a K-of-N report-all tally and set a per-case trust prior WITHOUT
  collapsing into a deterministic/ordinal scoring rule (F1) and WITHOUT being
  unfalsifiable narration (F2). All cases are synthetic (example_not_a_real_row).
  The probe author pre-registers directional predictions and attempts the reads;
  the PASS/FAIL verdict is reserved for a de-correlated grader, because the author
  asserts the premise and must not self-confirm it.
use_when:
  - Deciding whether the C2 ledger read-contract rests on a sound premise before hardening or building on it.
  - Grading whether a qualitative tally-read is genuine (F3), scoring-in-disguise (F1), or vacuous (F2).
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md       # the spec whose premise this probes
  - docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md          # the ledger schema the synthetic cases instantiate (#54)
stale_if:
  - The de-correlated grader returns a verdict (replace PENDING; route F1/F2/F3 per the verdict map).
  - INV-1 (no-scoring boundary) is amended by the owner.
  - The ledger schema changes (#64 lands) in a way that changes the tally/caveat fields the cases use.
```

## Status

`PROPOSED` — design/docs feasibility probe, `product_learning` tier. All cases
are **synthetic illustrations (`example_not_a_real_row`)**; the probe **binds no
signal, populates no real row, builds no runner, and edits neither the ledger nor
the FROZEN conductor.** The PASS/FAIL **verdict is `PENDING` a de-correlated
grader** (see Self-Correlation Disclosure). Authored 2026-06-14 in the
ledger-first continuation lane.

## What This Probe Decides

The C2 ledger read-contract assumes INV-1's claim that a **coherent, non-vacuous
qualitative read** of a tally exists. The owner adopted the *policy* (no scoring
engine); the *feasibility* has never been demonstrated. Three outcomes:

- **F1 — collapse to scoring.** The "read" is really a function of the tally
  (ratio/rank); case facts add no independent variance. → INV-1 unachievable as
  written; architecture/owner reconcile.
- **F2 — vacuity.** The "read" produces some weight with some words, but nothing
  could count as a *wrong* read. → INV-1 "coherent" only by being empty; needs an
  adequacy standard.
- **F3 — holds.** Case-specific reasons produce explainable, bounded, auditable
  variance; caveats can override raw ratio; bad reads are rejectable. → premise
  demonstrated; the spec's foundation is sound.

The discriminator that separates F3 from F1: a coherent read makes the tally
**informative but insufficient** — the *same tally* yields *different* priors
across cases, each tied to case facts. The discriminator that separates F3 from
F2: a coherent read can mark a *bad* read as bad.

## Pre-Registration (committed BEFORE the reads — the falsifiable part)

These directional predictions are fixed in advance. The reads below must honor
them with case-grounded reasons, or the probe fails.

- **PR-α:** Across α1 and α2 (identical signal, identical tally **2-of-3**,
  identical decision_family), the prior for **α1 must be materially HIGHER than
  α2**, justified by case-to-record correspondence — NOT by the tally (which is
  identical). If a read gives them the same weight, that is **F1**.
- **PR-β:** Across β1 (8-of-12, fresh) and β2 (3-of-3, N=3, stale), a defensible
  read **may rate β1 ≥ β2 despite β2's perfect ratio**, because small-N +
  staleness undercut it. A read that ranks β2 > β1 *solely because 3/3 > 8/12* is
  **ordinal scoring**.
- **PR-bad:** The three planted bad reads (ratio-restatement, non-bearing/vibes,
  outcome-contaminated) **must be rejected** by the rubric. If any survives, the
  discipline is vacuous → **F2**.

## Synthetic Cases (`example_not_a_real_row` — illustration only)

Decision family: `beauty-consumer-demand`. Signal under read in pair α:
`org-motion-hiring-composition`.

### Pair α — fixed tally (2-of-3), varied context

Ledger row read in BOTH α-cells (identical):
`tally{k_correct: 2, n_scoreable: 3, excluded: 0}`, fresh, validation_status
`product_learning`. The 3 prior pre-committed uses: two `correct_direction`, one
`wrong_direction`; the miss was driven by a one-off retail-partnership hiring
ramp that distorted org-motion.

- **α1 — context argues UP.** New case: a founder-led clean-beauty DTC brand with
  a public ATS board. The three prior uses were *also* founder-led DTC brands with
  public boards — structurally like this case — and the single miss's distortion
  (a retail-partnership ramp) is **absent** here.
- **α2 — context argues DOWN.** New case: a legacy mass-market brand pivoting to
  "clean." The three prior uses were small DTC brands (unlike this legacy pivot),
  and the single miss was **itself a legacy-pivot case** — the record's one known
  failure mode is exactly this case's profile.

### Pair β — fixed case, varied tally/caveats

New case: a clean-beauty DTC brand. Two signals, two record-states:

- **β1 — `review-venue-candidate-yield`:** `tally{k:8, n:12, excluded:1}`, fresh,
  `last_reviewed` recent.
- **β2 — `embedded-price-payload-movement`:** `tally{k:3, n:3, excluded:0}`, but
  **N=3 and stale** — a `stale_if` predicate hit (the underlying price-payload
  source schema changed since those three uses).

## Attempted Qualitative Reads (the demonstration — author-produced, to be adjudicated)

These are the author's attempt to perform the read INV-1 claims is possible. They
are **claims for the grader to adjudicate**, not a self-declared pass.

- **α1 read:** "Org-motion sits at 2-of-3 in beauty-consumer-demand. The decisive
  point is correspondence: all three prior uses were founder-led DTC brands with
  public ATS boards — structurally this case — and the one miss came from a
  retail-partnership ramp that isn't present here. The record is on-pattern and
  its known failure mode doesn't apply, so I treat org-motion as a **moderately
  strong supporting** signal — while flagging N=3 is thin, so it informs the call
  rather than carrying it." *(No number; weight tied to record↔case fit.)*
- **α2 read:** "Same 2-of-3 org-motion record, but the correspondence breaks: the
  three prior uses were small DTC brands, unlike this legacy mass pivot, and the
  single miss was itself a legacy-pivot — the record's failure mode is this case's
  profile. I treat org-motion's direction as **low-trust here** and lean on other
  signals; a thin, off-pattern record with its one miss pointing right at this
  configuration cannot bear the call." *(Same tally, opposite weight, by case
  facts.)*
- **β read:** "Between review-yield at 8-of-12 fresh and price-payload at 3-of-3
  stale: the 3-of-3 looks perfect, but N=3 with a `stale_if` hit means the source
  changed since those three — I don't trust the ratio to still hold. The 8-of-12
  is a worse raw ratio but current and better-sampled. I lean on **review-yield**
  as the more trustworthy prior and treat price-payload as a **weak corroborator
  pending a fresh review**." *(Caveats override ratio.)*

## Planted Bad Reads (calibration — the rubric MUST reject all three)

- **BAD-1 (ratio restatement / F1 tell):** "Org-motion is 2 of 3, about 67%, so
  medium-high confidence." → no case facts; pure ratio.
- **BAD-2 (non-bearing / F2 tell):** "Org-motion felt strong and the brand's vibe
  is positive, so high trust." → reasons don't connect to the record or case
  mechanics; nothing could falsify it.
- **BAD-3 (contamination tell):** "We know this brand later sold out, so org-motion
  was clearly reliable here." → uses the post-reveal outcome to justify a
  pre-reveal weight; firewall breach.

## Grading Rubric (for the de-correlated grader)

A PASS (F3) requires **all four**:

1. **Sensitivity (¬F1):** α1's prior is materially higher than α2's, and the
   difference is grounded in stated case-to-record facts, not the (identical)
   tally. *Fail → F1.*
2. **Caveat-load-bearing (¬ordinal):** the β read can justify trusting the
   lower-ratio-but-fresh-higher-N signal over the perfect-but-stale-tiny one.
   *Fail → ordinal scoring (a sub-form of F1).*
3. **Falsifiability (¬F2):** all three planted bad reads are rejected for the
   stated reason. *Any survives → F2.*
4. **No reconstructable table:** the grader cannot derive a stable
   tally→weight lookup from the α + β outputs (the same 2-of-3 maps to two
   different weights for case reasons). *Reconstructable → scoring.*

Verdict map: all four hold → **F3** (route to delegated review of the spec
wording). Test 1 or 2 fails → **F1** (owner: lift the no-scoring boundary with an
auditable rubric, or narrow what C2 may emit). Test 3 fails → **F2**
(architecture: add an adequacy standard for qualitative justifications, then
re-spec).

## Verdict

`PENDING_DE_CORRELATED_GRADING` — not self-graded by the author. See disclosure.

## Self-Correlation Disclosure

The probe author also authored the C2 read-contract spec and asserts INV-1's
premise. Author-graded, this probe would self-confirm. Two mitigations are in
force: **(1) pre-registration** — the directional predictions (PR-α, PR-β,
PR-bad) were committed above before the reads, so the probe can fail; **(2)
de-correlated grading** — the PASS/FAIL verdict is reserved for a different-family
grader via `workflow-delegated-review-patch`. The author's attempted reads are
**claims to adjudicate, not premises to inherit**.

## Non-Claims

- Synthetic feasibility probe only; binds no signal, populates no real row, builds
  no runner, runs no case, edits neither the ledger nor the FROZEN conductor.
- A PASS (F3) would demonstrate the qualitative read is **non-vacuous and
  non-scoring on cases built to stress it** — exactly INV-1's premise. It would
  **NOT** prove the read is accurate or reliable in the wild; that is a separate,
  later validation question.
- The attempted reads are the author's claims, pending de-correlated adjudication;
  the verdict is `PENDING`.
- `product_learning` cap; not validation, readiness, or buyer-proof.
```text
This is advisory design input only. It is not a verdict, not implementation
authority, and not proof of readiness.
```
