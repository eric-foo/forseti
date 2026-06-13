# Judgment-Spine C2 Qualitative-Read Feasibility Probe v1 (PROPOSED — supersedes v0; harder, F4-aware, externally pre-registered)

```yaml
retrieval_header_version: 1
artifact_role: Feasibility probe v1 (design/docs demonstration — pressure-tests whether a coherent, non-vacuous, CONSISTENT/AUDITABLE qualitative read of a K-of-N tally exists; supersedes v0 after a cross-vendor grading judged v0 weak; verdict PENDING de-correlated grading; binds no row, builds nothing, runs nothing)
scope: >
  v1 rebuilds the v0 probe to answer the four findings a cross-vendor (OpenAI
  GPT-5) grading raised against v0: AR-01 cases too clean, AR-02 pre-registration
  not externally evidenced, AR-03 bad reads strawmen, AR-04 a missing fourth
  failure mode (F4: non-scoring + non-vacuous but UNCONSTRAINED / INCONSISTENT /
  unauditable discretion). v1 uses genuinely ambiguous cases, plausible-but-wrong
  bad reads, an explicit F4 consistency/auditability test, and — for AR-02 — a
  two-commit structure: THIS pre-registration (cases + predictions + rubric, no
  reads) is committed BEFORE the attempted reads exist, so the predictions are
  externally checkable as un-retrofitted.
authority_boundary: retrieval_only
open_next:
  - docs/product/judgment_spine/judgment_spine_c2_qualitative_read_feasibility_probe_v0.md  # the v0 probe + its graded-weak result (provenance)
  - docs/product/judgment_spine/judgment_spine_c2_ledger_read_contract_v0.md                # the spec whose premise this tests
  - docs/product/judgment_spine/near_half_signal_reliability_ledger_v0.md                   # the ledger schema the synthetic cases instantiate (#54)
stale_if:
  - The de-correlated grader returns a v1 verdict (replace PENDING; route per the verdict map).
  - INV-1 (no-scoring boundary) is amended by the owner.
  - The ledger schema changes (#64 lands) in a way that changes the tally/caveat fields the cases use.
```

## Status

`PROPOSED` — design/docs feasibility probe, `product_learning` tier. All cases
are **synthetic illustrations (`example_not_a_real_row`)**; the probe **binds no
signal, populates no real row, builds no runner, and edits neither the ledger nor
the FROZEN conductor.**

**THIS FILE IS THE PRE-REGISTRATION STAGE (AR-02 fix).** It contains the cases,
the frozen predictions, and the rubric — **but NOT the attempted reads.** The
attempted reads (the answers being graded) are added in a **separate, later
commit**, so the git history is externally-checkable evidence that the
predictions below were committed *before* any read existed and therefore cannot
be retrofitted. The PASS/FAIL verdict is reserved for a de-correlated grader.

## Why v1 Exists (the v0 grading)

A cross-vendor grading of v0 (OpenAI GPT-5, `de_correlation_bar:
cross_vendor_discovery`) returned **verdict F3 but `probe_soundness:
rigged_or_weak`** with four findings, all CA-adjudicated as **accepted**:

- **AR-01 (major):** v0's cases were too clean — decisive cues almost forced the
  desired contrast, so F3 showed the author could follow planted cues, not that a
  read handles ambiguity. → v1 uses **genuinely ambiguous cases** (competing
  pulls, no single decisive tell).
- **AR-02 (major):** v0 asserted pre-registration inside the same artifact as the
  reads — an internal claim, not checkable. → v1 commits **pre-registration in a
  separate prior commit** (this file, before the reads).
- **AR-03 (major):** v0's planted bad reads were strawmen. → v1 uses
  **plausible-but-wrong bad reads** (cherry-picked correspondence, caveat
  laundering, framing-dependent) that require substantive judgment to reject.
- **AR-04 (minor finding, elevated):** v0's F1/F2/F3 map missed a fourth failure
  mode. → v1 adds **F4** and an explicit **consistency/auditability test**.

## The Four Failure Modes (v1)

- **F1 — scoring in disguise.** The read is a function of the tally (ratio/rank);
  case facts add no independent variance.
- **F2 — vacuity.** Some weight, some words, but nothing could count as a *wrong*
  read.
- **F4 — unconstrained discretion (NEW).** The read *is* non-scoring and
  *is* non-vacuous (uses case facts, rejects absurd reads), **but** is
  inconsistent / path-dependent / unauditable: the same situation can be
  rationalized to different weights depending on framing, and you cannot tell a
  principled read from a post-hoc story. This is the most realistic failure of a
  qualitative-weighting scheme and the one v0 could not see.
- **F3 — holds.** Case-specific reasons produce explainable, bounded variance
  (¬F1); bad reads are rejectable (¬F2); **and the read is stable across framing
  and exposes what would change it (¬F4).**

## Pre-Registration (FROZEN in this commit — committed BEFORE any read exists)

- **PR-α (sensitivity under ambiguity, ¬F1):** α1 and α2 share an identical
  2-of-3 tally and identical decision_family but have **different competing
  pulls**. A valid read must (i) produce priors whose **load-bearing facts
  differ** between α1 and α2 (not a restated tally), and (ii) **engage both pulls
  in each case** (not seize one cue). Predicted: both priors land in the
  *moderate* band but for **structurally different reasons**; a read that gives an
  identical justification for both, or that ignores α1's partial confound or α2's
  signal-quality weakness, **fails (→ F1 or F4)**.
- **PR-β (caveats override ratio, ¬ordinal):** β1 has the **higher** raw ratio
  (0.80) but a **partial decision_family mismatch**; β2 has the **lower** ratio
  (0.60) but an **exact family match**. Because the ledger defines reliability
  *within* a decision_family, a valid read must treat β1's family-mismatch as
  **load-bearing** — discounting its higher ratio — not rank by ratio. Predicted:
  a defensible read rates **β2 ≥ β1** *or* hedges β1 heavily on the mismatch;
  ranking β1 over β2 *purely because 0.80 > 0.60* **fails (→ F1)**.
- **PR-γ (consistency/auditability, ¬F4):** γ1 and γ2 are the **same case, same
  signal, same tally**, presented with **reordered/reframed evidence** (strengths-
  first vs concerns-first). A valid read must give **materially the same prior**
  in γ1 and γ2 and cite the **same load-bearing facts** both times. Predicted: a
  principled read is framing-invariant; a prior that **swings with framing**, or
  that cites different load-bearing facts under each framing, **fails (→ F4)**.
- **PR-audit (auditability hook, ¬F4):** **every** attempted read must end with a
  specific falsifiable counterfactual — "this weight would move to ___ if [named
  fact] were different." A read that cannot name what would change its weight
  **fails (→ F4)**.
- **PR-bad (falsifiability against plausible error, ¬F2):** three
  **plausible-but-wrong** bad reads (specified below; texts added in the reads
  commit) must each be **rejected for a substantive reason**. Any that survives
  the rubric **fails (→ F2)**.

## Synthetic Cases (`example_not_a_real_row` — illustration only)

Decision family: `beauty-consumer-demand`. Pair-α/γ signal:
`org-motion-hiring-composition`.

**Shared prior record for the 2-of-3 tally (α and γ).** `tally{k:2, n:3,
excluded:0}`, fresh. The three pre-committed uses were deliberately
**heterogeneous**: P1 (`correct`) a founder-led DTC brand; P2 (`correct`) a
prestige department-store brand; P3 (`wrong`) a mass-market brand during a
**category-wide hiring surge** (a macro confound that made org-motion look
expansionary for everyone).

### Pair α — fixed tally (2-of-3), genuinely AMBIGUOUS context (AR-01)

- **α1:** New case = a **hybrid mid-market brand** (part DTC like P1, part
  wholesale like P2) during a period of **mild** category hiring growth (a
  *partial* version of P3's confound). Competing pulls: two prior successes are
  *loosely* analogous; the failure condition (macro confound) is *mildly* present.
  No decisive tell.
- **α2:** New case = a brand **strongly analogous to P2** (prestige), with **no
  macro confound** — but the case's **own org-motion signal is thin/noisy** (the
  ATS board is partly private, so the observed hiring direction is low-confidence).
  Competing pulls: strong success-analogue + no confound (argues up) vs weak
  current signal quality (argues hedge). Different pulls than α1.

### Pair β — caveat-vs-ratio under subtlety (AR-01)

New case: a clean-beauty DTC brand. Two candidate signals:
- **β1 — `review-venue-candidate-yield`:** `tally{k:8, n:10, excluded:0}` (ratio
  **0.80 — the higher ratio**), fresh, but recorded in an **adjacent sub-family**
  (`prestige-skincare`, not `beauty-consumer-demand`) — a **partial
  decision_family mismatch**.
- **β2 — `embedded-price-payload-movement`:** `tally{k:6, n:10, excluded:0}`
  (ratio **0.60 — the lower ratio**), fresh, **exact family match**, solid sample.

### Pair γ — consistency / framing (AR-04, the F4 test)

**Same case, same signal, same 2-of-3 record, presented twice.** New case = a
founder-led DTC clean-beauty brand whose org-motion is expansionary, with one
mild concern (a recent senior-marketing departure).
- **γ1 (strengths-first framing):** the analogous prior successes and the
  expansionary hiring are presented first; the senior departure and the P3-style
  confound risk are noted afterward.
- **γ2 (concerns-first framing):** the **same facts**, but the senior departure,
  the thin N, and the confound risk are presented first; the expansionary hiring
  and analogues afterward.

## Bad-Read Slots (specifications now; texts added in the reads commit — AR-03)

Each must be **plausible** (uses real case facts) yet **wrong**, requiring
substantive judgment to reject:
- **BAD-α (cherry-picked correspondence):** for α1, emphasizes only the analogous
  successes and the *absence of the full confound*, silently dropping the partial
  confound and the loose/mixed analogue → inflated trust. Rejection requires
  spotting selective use of the record (report-all spirit at the reasoning level).
- **BAD-β (caveat laundering):** for β, **names** small-N / family-mismatch but
  assigns the weight as if they did not bear — effectively ratio-ranks 7/10 vs
  4/5. Rejection requires noticing the caveats were mentioned but not load-bearing
  (ordinal scoring behind qualitative labels).
- **BAD-γ (framing-dependent / F4 tell):** gives high trust under γ1's framing and
  low under γ2's, each "justified." Rejection requires noticing the **same facts
  produced different weights by framing** → unconstrained discretion.

## Grading Rubric (for the de-correlated grader)

A PASS (**F3**) requires **all six**:
1. **T1 Sensitivity under ambiguity (¬F1):** α1 vs α2 priors rest on **different
   load-bearing facts** and each **engages both competing pulls**; not a restated
   tally. *Fail → F1.*
2. **T2 Caveat-load-bearing (¬ordinal):** the β read lets family-match /
   resolution-quality caveats **actually move** the weight against the raw ratio.
   *Fail → F1.*
3. **T3 Falsifiability vs plausible error (¬F2):** all three **plausible-but-wrong**
   bad reads are rejected for substantive reasons. *Any survives → F2.*
4. **T4 No reconstructable table (¬scoring):** no stable tally→weight lookup is
   derivable from the α + β + γ outputs. *Reconstructable → F1.*
5. **T5 Consistency (¬F4):** γ1 and γ2 yield **materially the same prior** and the
   **same load-bearing facts**; framing does not swing it. *Swings → F4.*
6. **T6 Auditability (¬F4):** every read names a **specific falsifiable
   counterfactual** (what fact would change the weight). *Missing → F4.*

**Verdict map:** all six → **F3**. T1/T2/T4 fail → **F1**. T3 fails → **F2**.
T5/T6 fail → **F4** (unconstrained/inconsistent discretion). The grader should
**also attack the rubric and cases themselves** (are they still too clean? is any
test gameable? is F3 sufficient evidence for INV-1's operational soundness?).

## Verdict

`PENDING_DE_CORRELATED_GRADING` — not self-graded by the author.

## Self-Correlation Disclosure (strengthened for AR-02)

The probe author also authored the spec and asserts INV-1's premise. v0's
pre-registration was an in-file claim (AR-02). v1 strengthens it: **this
pre-registration file is committed in its own commit, containing no attempted
reads**; the reads are added in a later commit. Anyone with repo access can
`git show` the pre-registration commit and confirm the predictions existed with
**no reads present** — so they cannot have been retrofitted to the reads. The
pre-registration commit hash is recorded in the reads commit's message. Grading
remains reserved for a different-family reviewer.

## Non-Claims

- Synthetic feasibility probe only; binds no signal, populates no real row, builds
  no runner, runs no case, edits neither the ledger nor the FROZEN conductor.
- A PASS (F3) would demonstrate the qualitative read is non-scoring, non-vacuous,
  **and consistent/auditable on cases built to stress it** — a stronger result
  than v0, but still **NOT** proof of accuracy or real-world reliability (a
  separate, later validation question).
- `product_learning` cap; not validation, readiness, or buyer-proof.
```text
This is advisory design input only. It is not a verdict, not implementation
authority, and not proof of readiness.
```
