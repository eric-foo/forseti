---
retrieval_header_version: 1
artifact_role: PROPOSED conductor addendum (NOT yet ratified; pending owner sign-off + review). Subordinate to the conductor operating model.
scope: >
  Three proposed additions to the judgment conductor: (1) an invocation expectation
  (judgment-spine runs load the conductor as framing first), (2) an outcome-blind
  construction rule (a constraint on the JSG-02/03 freezes), and (3) a JSG-05
  memorization-probe refinement (passive-primary detection; drop the familiarity
  probe; aggressive recall only as a post-seal forensic). Folds into the conductor
  on sign-off.
use_when:
  - Deciding whether to ratify these conductor additions.
  - Running a by-hand judgment pilot before ratification (apply as proposed discipline).
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md
  - forseti/product/spines/product_lead/proof_charter/orca_claim_defense_doctrine_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
stale_if:
  - The conductor's JSG-02 / JSG-03 / JSG-05 definitions change.
  - These additions are ratified (this proposal becomes historical; the conductor governs).
---

# PROPOSED Conductor Addendum - Construction Integrity + Probe Refinement (v0)

**Status: PROPOSED, pending owner sign-off + review (recommend the defense-doctrine
delegated review). Not yet part of the conductor; do not cite as ratified.**

Motivated by the org-motion Beauty Pie pilot. Three additions, none of which adds a
new gate - each is a constraint on an existing gate or an invocation note.

**SUPERSEDED 2026-06-12 by `conductor_construction_integrity_probe_addendum_v1.md`** (the
architecture-resolved requirements + routed-out redraft); v0 is retained for review history only.

**Delegated review outcome (2026-06-12): NEEDS_ARCHITECTURE_PASS.** A cross-vendor
review (`docs/review-outputs/adversarial-artifact-reviews/conductor_construction_integrity_probe_addendum_adversarial_review_v0.md`)
returned three accepted findings - AR-01 critical (Rule 3's passive read cannot be a
JSG-05 refinement: JSG-05 precedes JSG-06, so the sealed judgment does not yet exist),
AR-02 major (the outcome-blind receipt is hollow if only self-attested), AR-03 major
(Rule 1 over-claims the consolidation map's authority). **This proposal is BLOCKED from
ratification pending an architecture pass** that resolves all three. The three rules
below are the as-authored design and must NOT fold into the conductor as written.

## 1. Invocation expectation (activation)

The conductor is a by-hand operating model, not an auto-firing runtime; it governs a
run only when an actor loads and follows it. To make that reliable:

- **Any judgment-spine run loads the conductor as its framing before planning** -
  even in setup phases (feasibility, scope, outcome) that precede the gate sequence
  - so the work is gate-aware (which gates it is prepping for, the by-hand
  product-learning cap, the seams) from the first move.
- Routing hook (overlay-owned): the judgment consolidation map already routes
  "open first -> conductor / ECR / ladder"; the front door should treat that as a
  hard first read for judgment work, not optional.
- A future auto-firing conductor *skill* would be the strongest activation, but is a
  JQ-machinery build; the routing rule is the present mechanism.

## 2. Outcome-blind construction (constraint on JSG-02 / JSG-03)

The participant packet (JSG-02) and facilitator ledger (JSG-03), and any case
re-skin / anonymization, are **built by an actor that does not hold the sealed
outcome.** The outcome-aware facilitator performs reveal/calibration (JSG-08) only.

- Rationale: an outcome-aware constructor can (consciously or not) tilt the
  with/without arms or the anonymization toward the known answer - contaminating
  construction neutrality and selection integrity. Outcome-blindness removes that
  degree of freedom at the source.
- Receipt: the JSG-02 / JSG-03 freeze receipts should attest that construction was
  outcome-blind (the constructor did not hold the sealed outcome).
- Pairs with the batch pre-commitment (anti-selection) in the batch ledger; together
  they answer the hostile-reviewer "you cherry-picked / you steered" attack (see the
  claim defense doctrine).

## 3. JSG-05 memorization-probe refinement

The probe flags a contestant who already knows the outcome - without *manufacturing*
the recognition it measures (asking a model to recall can induce recognition;
conductor :368 and the finder frame :56 already note this). Refinement:

- **Default / primary = passive contamination detection.** Read the *sealed* blind
  judgment for outcome-knowledge it could not have from the packet (post-cutoff
  specifics, the actual result, suspicious certainty). Non-inducing; the strongest
  signal; the default.
- **Drop the light "did this feel familiar?" probe.** Familiarity is not
  outcome-knowledge; it over-fires (models pattern-match to similar cases without
  knowing the specific result) - too many false positives.
- **Active recall ("name the case + its outcome") is a post-seal forensic only.** Run
  it - if at all - only after the judgment is sealed, to confirm a passive flag;
  never as a pre-judgment gate (that is the self-pwn).  Accept that it manufactures
  some recognition.
- Unchanged: over-rejection is the safe direction; a recognized arm is recorded as
  data, not discarded.
