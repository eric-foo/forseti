# Judgment-Spine C2 Qualitative-Read Feasibility Probe v2 (PROPOSED — supersedes v1; BLIND consistency test)

```yaml
retrieval_header_version: 1
artifact_role: Feasibility probe v2 (design/docs experiment — tests the F4 consistency property with BLIND, author-independent reads instead of author-synchronized ones; verdict PENDING de-correlated grading; binds no row, builds nothing on the real machinery, populates no ledger)
scope: >
  v2 answers the two findings a cross-vendor (OpenAI GPT-5) grading raised against
  v1: (major) v1's F4 consistency test was author-synchronized — the same author
  wrote both framings knowing they should match, so the "pass" was illusory;
  (minor) v1 printed the bad-read answer key inline. v2 runs the consistency test
  BLIND: four isolated same-model subagents produced reads of the same case under
  two framings, each blind to the others and to the consistency-test purpose, so
  the author did not author the reads. Result recorded as observed, not as a
  demonstration the author controlled. Bad-read diagnoses moved to a hidden
  adjudication key.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_qualitative_read_feasibility_probe_v1.md  # v1 + its graded result (provenance)
  - forseti/product/spines/judgment/demand_read/c2_weighting/judgment_spine_c2_ledger_read_contract_v0.md                # the spec this informs (F4 → consistency/auditability requirement)
stale_if:
  - The de-correlated grader returns a v2 verdict (replace PENDING; route per the verdict map).
  - INV-1 (no-scoring boundary) is amended by the owner.
```

## Status

`PROPOSED` — design/docs feasibility experiment, `product_learning` tier. The
case is synthetic (`example_not_a_real_row`); **this binds no signal, populates
no real ledger row, edits neither the ledger nor the FROZEN conductor, and does
not run the production judgment machinery.** The four reads were produced by
**isolated subagents** as a paper-tier blind-consistency experiment; the verdict
is reserved for a de-correlated grader.

## Why v2 Exists (the v1 grading)

A cross-vendor grading of v1 (OpenAI GPT-5, `cross_vendor_discovery`) returned
**F3, all six tests pass, `probe_soundness: sound`**, with two accepted findings:

- **Major:** v1's F4/consistency test (γ1 vs γ2) was passable by a **same-author,
  answer-aware** read — the author wrote both framings *after* pre-registering
  that they should match, so synchronized wording satisfied T5 without showing
  operational stability under independent/blind framing. → v2 runs γ **blind**.
- **Minor:** v1 printed each bad read's "(Wrong: …)" diagnosis inline, handing the
  grader the answer key. → v2 hides the diagnoses in a separate adjudication key.

## The Blind Protocol (the major-finding fix)

Four **isolated subagents** were each given **one framing** of the **same**
synthetic case + the same ledger/INV-1 operating rules, and asked to produce a
qualitative C2 trust weight for `org-motion-hiring-composition`, **with no
knowledge of the other reads and no knowledge that consistency was being tested.**
Two received a **strengths-first** framing (A1, A2); two a **concerns-first**
framing (B1, B2). The author did **not** author the reads.

- **Genuine blindness:** each read was produced in an isolated context — no
  cross-contamination, no answer-awareness. This is the property v1 lacked.
- **Named caveat (same-model-family):** all four subagents are the same model
  family (Claude). So this tests whether a **Claude-class** C2 read is
  framing-stable — *within-model* operational consistency — not model-independence.
  Cross-model blind consistency is a further, owner-gated step.
- **Named method limitation:** the two framings differ in **order** *and* in how
  the confound is characterized (A: "no strong evidence of a surge"; B: "a risk —
  the exact condition behind the failure — though no strong evidence active"). So
  this is not a perfectly clean order-only manipulation; part of any drift may be
  the framing wording, not pure reader sensitivity. The finding is therefore
  stated as sensitivity to **how an ambiguous caveat is characterized**, which is
  itself operationally relevant.

## The Case (synthetic; `example_not_a_real_row`)

Decision: is consumer demand for a founder-led DTC clean-beauty brand durable?
Signal: `org-motion-hiring-composition`. Record (in `beauty-consumer-demand`):
2-of-3 — P1 (founder-DTC, correct), P2 (prestige, correct), P3 (mass-market during
a category-wide hiring surge, wrong). Case facts (identical across framings):
expansionary org-motion weighted to growth functions; founder-led DTC (matches
P1); no strong evidence of a category-wide surge now; one recent senior-marketing
departure; thin record (N=3). Framing A presents strengths first; framing B
presents concerns first (see method limitation above for the confound wording).

## Observed Blind Reads (verbatim weights + reasoning; NOT authored by the probe author)

| Read | Framing | Weight | Load-bearing facts | Counterfactual |
| --- | --- | --- | --- | --- |
| A1 | strengths-first | **moderate** (upper) | confound absent → reliable regime; DTC matches a correct prior; expansionary clear; thin record + departure cap it | up: more in-family uses / growth-function concentration / departure benign; down: surge activates / capital-funded / clustered departures |
| A2 | strengths-first | **moderate** | right family + DTC archetype; known failure mode absent; thin record caps; departure = composition noise | up: demand-pulled growth functions / surge stays absent / departure backfilled; down: surge appears / departure pattern / back-office hiring |
| B1 | concerns-first | **weak-to-moderate** | in-family + best-matching prior pull up; thin record; **surge confound live/unexcluded** caps; departure contradicts | up: surge excluded / demand-pull functions / seat backfilled / more in-family DTC; down: surge active / undifferentiated hiring / more departures |
| B2 | concerns-first | **weak-to-moderate** | **surge confound unverified-not-excluded = dominant cap**; small N; DTC analogue pulls up; expansionary; departure contradicts | up: evidence no surge active / more in-family DTC / departure benign; down: surge active / non-demand functions / clustered departures |

## Analysis (observed, not controlled)

- **Within-framing: consistent.** A1≈A2 (moderate); B1≈B2 (weak-to-moderate).
- **Across-framing: a systematic half-notch drift.** Strengths-first → *moderate*;
  concerns-first → *weak-to-moderate*. Every read, same direction.
- **Single driver:** the **identical** confound fact ("no strong evidence of a
  surge") was read as **absent** under framing A (reassurance) and as
  **unexcluded/live** under framing B (cap). The weight tracked that valence.
- **Stable underneath:** all four cite the **same load-bearing facts** (in-family,
  DTC analogue, confound, thin N, departure) and the **same counterfactuals** (up
  if surge ruled out / more in-family cases; down if surge activates). The
  *reasoning structure* is framing-invariant; the *weight calibration* is not.

**Honest reading:** **partial F4.** A Claude-class qualitative C2 read is **not
fully framing-invariant** on ambiguous inputs — the weight drifts with how an
unresolved caveat is characterized — but it is **not arbitrary** (¬catastrophic
F4): facts and counterfactuals are stable and auditable, so the drift is
*visible and attributable* to one ambiguity, not hidden. (Caveat: same-model-only;
framings not perfectly order-clean — see method limitation.)

## Implication For The Spec (the durable lesson)

The C2 read-contract currently guards F1 (no scoring) and F2 (per-case
justification) but says nothing about consistency. v2 shows the live operational
gap is **ambiguity handling**: without a convention for how a "risk with no
evidence it is active" is treated (cap vs discount vs neutral), two faithful
reads of the same case land a notch apart. Candidate spec requirement (for owner
review): C2 must (a) state, per ambiguous caveat, whether it is treated as a cap,
a discount, or neutral, and why; and (b) expose the counterfactual — so that even
residual calibration drift is auditable and adjudicable.

## Bad Reads (plausible-but-wrong; diagnoses HIDDEN — minor-finding fix)

Judge each independently BEFORE reading the adjudication key at the end.
- **BAD-α:** "2-of-3 with two clear successes; this brand resembles both our
  founder-DTC and prestige winners; the miss was a special-case surge, none here —
  positives apply, failure doesn't. **Strong.**"
- **BAD-β:** "β1 0.80, β2 0.60. I note β1 is adjacent sub-family, β2 exact-match,
  family scoping matters. On balance β1's stronger record (0.80 vs 0.60) makes it
  more reliable; weight β1 above β2." *(β1/β2 as defined in v1: β1 higher ratio +
  family mismatch; β2 lower ratio + exact match.)*
- **BAD-γ:** "Under a strengths-first framing org-motion is **strong**; under a
  concerns-first framing it is **weak**. Each framing supports its read."

## Grading Rubric (for the de-correlated grader)

The central question for v2 is **T5 on the BLIND reads**: do the four reads
converge enough — on **weight** and on **load-bearing facts** — to count as
operationally consistent, or does the observed half-notch framing drift count as
**F4**? This is a judgment the grader owns. Also grade T6 (every read exposes a
counterfactual — observed: yes) and T3 (reject the three bad reads, diagnoses
withheld). Then attack: were the framings fair (the order-vs-characterization
limitation)? Is same-model blindness sufficient? Does "facts stable, weight
drifts" read as F3-with-caveat or as F4? Is there a 5th failure mode?

**Verdict map (v2):** reasoning + weight both stable across blind framings → F3.
Facts stable but weight framing-drifts (the observed result) → the grader decides
**F3-with-named-residual** vs **partial-F4**; state which and why. Weight swings
widely or facts differ by framing → F4.

## Verdict

`PENDING_DE_CORRELATED_GRADING`.

## Cross-Model Addendum (4 brands; baseline + disciplined)

Run after the same-model blind test, to close the same-model caveat.
- **Baseline (10 reads; Claude/GPT/Qwen/Grok, 2 framings):** direction +
  load-bearing facts + counterfactual **unanimous across all 4 brands**; only the
  dial drifted, within ≈one band (Qwen/Grok run ≈one band hot). The convergence is
  **not** a single-model artifact.
- **Disciplined re-run (8 reads; forced cap/discount/neutral classification, NO
  convention):** the discipline **recentered** the dial — only **2/8 hard-capped**
  an unconfirmed risk; most said neutral/discount, correcting a framing-induced
  over-cap — **and localized the entire residual spread to one doctrine question:**
  is an unconfirmed-known-risk / an inherent small-N a **cap or a discount**? Net
  weight tracked the count of hard CAPs applied. Several models independently
  proposed: **absence of a known risk = floor-clearing, not positive evidence.**
- **Routed:** that convention — how C2 treats a known risk across evidentiary
  states (present / unconfirmed / absent) — is handed to a dedicated owner thread;
  this probe established it is the **single remaining lever** on consistency.
- Caveat: synthetic single case; `product_learning`; not validation or real-world
  reliability.

## Non-Claims

- Synthetic paper experiment; binds/populates/runs nothing on the real machinery.
- The blind reads show **within-Claude-family** framing behavior on one case; not
  model-independent, not multi-case, not real-world reliability.
- `product_learning`; not validation, readiness, or buyer-proof.
```text
This is advisory design input only. It is not a verdict, not implementation
authority, and not proof of readiness.
```

## Bad-Read Adjudication Key (do NOT read until you have judged the bad reads)

- **BAD-α — cherry-picked correspondence:** calls a loose partial analogue a clean
  match to *both* winners, and dismisses the confound as absent when the case has
  *mild* category growth (a partial recurrence of the miss-driver). Real facts,
  selectively inflated. Must be rejected.
- **BAD-β — caveat laundering:** names the family mismatch, then ranks by ratio
  anyway (0.80 > 0.60), letting the caveat do no work. Ordinal scoring behind a
  qualitative label. Must be rejected.
- **BAD-γ — framing-dependent / F4:** same case, weight swings strong↔weak with
  presentation order — unconstrained discretion. Must be rejected. (Note: the v2
  blind reads show a *bounded, half-notch* version of this drift even among
  faithful reads — which is the v2 finding; BAD-γ is its catastrophic form.)
