---
retrieval_header_version: 1
artifact_role: RATIFIED conductor addendum v1 (requirements + routed-out change proposals; supersedes v0; owner-ratified 2026-06-16). Subordinate to the conductor operating model.
scope: >
  Redraft of the conductor construction-integrity + probe addendum after the
  cross-vendor NEEDS_ARCHITECTURE_PASS review and the owner's architecture
  decisions (2026-06-12). States the REQUIREMENTS the conductor change must meet
  and ROUTES the enactment to the owner sources; the addendum itself enacts
  nothing. Folds in the decision-framing / whitelist leak-safety rule surfaced by
  the Beauty Pie packet review.
use_when:
  - Deciding whether to ratify the conductor construction-integrity / probe change.
  - Running a by-hand judgment pilot before ratification (apply as discipline).
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/judgment/conductor/conductor_construction_integrity_probe_addendum_proposal_v0.md   # superseded; review history
  - docs/review-outputs/adversarial-artifact-reviews/conductor_construction_integrity_probe_addendum_adversarial_review_v0.md
  - orca/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md
stale_if:
  - The conductor JSG-02 / JSG-03 / JSG-05 / JSG-06 / JSG-08 definitions change.
  - The owner amends any of the five architecture decisions recorded below.
  - This redraft is ratified (it becomes historical; the conductor + owner files govern).
---

# Conductor Construction-Integrity + Probe Addendum v1 (requirements + routed-out)

**Status: RATIFIED v1 — owner-ratified 2026-06-16 (supersedes v0, which carried
NEEDS_ARCHITECTURE_PASS). The cross-vendor delegated re-review RETURNED (2026-06-12,
codex-gpt-5, cross_vendor_discovery): prior AR-01/AR-02/AR-03 resolved at addendum
level; one minor finding (ARV1-01, R4 field-name precision) accepted by the home
model and patched below. The addendum still ratifies nothing by itself — it STATES
requirements and ROUTES enactment to owner sources; with owner ratification its
requirements are adopted and that enactment is now carried by those sources (the
finder-frame operative bar + the judgement case construction protocol; see the R5
propagation map). Per this doc's own `stale_if`, the redraft is now historical and
the conductor + owner files govern. It edits no gate, field, predicate, or protocol
itself. Re-review report:
`docs/review-outputs/adversarial-artifact-reviews/conductor_construction_integrity_probe_addendum_v1_adversarial_re_review_v0.md`. This ratification and the identity-masking adoption layered on it (finder-frame operative bar, 2026-06-16) are routed to adversarial artifact review before downstream lanes treat them as final (doctrine-change review gate).**

Owner architecture decisions (2026-06-12) folded in: (1) drop active recall; (2)
recognized arm = record-as-data/quarantine (not discard); (3) JSG-08 tell = hard
contaminated route on a *confirmed* tell, strict derivability bar; (4)
single-operator memory leak = pilot-acceptable residual + subagent-delegation norm
(no hard two-actor gate); (5) intent-not-topic invocation trigger ratified. Plus
the decision-framing / whitelist leak-safety rule from the Beauty Pie packet review.

## R1 — Invocation (intent, not topic)

REQUIREMENT: work that is *running a Judgment Spine case, planning one through
JSG-01->JSG-10, or standing up that gate sequence (incl. pre-gate
feasibility/scope/outcome setup)* loads the conductor as framing, on the authority
of the conductor's own `use_when` — NOT on the consolidation map (which is
`retrieval_only`). Work that merely *mentions* judgment does not trip it. The
conductor is by-hand; a future auto-firing skill is out of scope.

## R2 — Outcome-blind construction (evidence-backed, not self-attested)

REQUIREMENT: an outcome-blind claim on the JSG-02/JSG-03 freezes clears only with
evidence, modeled on the JSG-04 provenance template ("a bare computed value does
not clear"): (a) actor separation (`constructor_session_ref` != outcome-holder);
(b) input separation (the outcome material withheld, named); (c) hash binding to
the frozen packet/ledger; (d) not-proven default if any of a-c is missing.
BY-HAND FORM (adopted norm, validated by the Beauty Pie run): construction is
delegated to an **outcome-blind subagent**, and its **outcome-excluded prompt /
transcript IS the receipt** (a reviewer reads it; it demonstrates exclusion). This
also satisfies actor-separation in practice (distinct context). RESIDUAL (recorded,
per owner decision 4): a single human orchestrating both the blind subagent and the
sealing could bridge via memory — disclosed, not gated, at product-learning tier.

## R3 — Contamination detection (rehomed; active recall dropped)

REQUIREMENT, three parts:
- **JSG-05 = a non-inducing pre-judgment screen only.** Structural isolation
  evidence (`web_search_disabled` -> `isolation_result == proven`) + an operator
  obscurity screen about the case. **Active recall is DROPPED entirely** (owner
  decision 1): forcing a contestant to recall manufactures recognition and would
  invalidate legitimately-clean work — a survivorship trap. JSG-05 reads nothing
  from JSG-06.
- **The passive contamination audit is homed on JSG-08, not JSG-05** (it
  structurally needs the revealed outcome, which only exists at JSG-08). It reuses
  the existing `calibration_frame` / `comparison_inputs` / `contaminated_or_invalid`
  scaffolding.
- **Contamination = outcome-USE, not recognition-capacity.** A contestant who
  *recognized* the brand but did not use the outcome is a LEGITIMATE arm, not
  contaminated. Only a confirmed *tell* contaminates.

## R4 — The tell test runs on the reasoning trace (owner decisions 2 + 3)

REQUIREMENT: the blind judgment MUST include a **reasoning trace** (JSG-06
requirement; reuses the existing `blind_judgement.contestant_band_claim.reasoning` field, made a required receipt field by its owner per routed change 5 below). The JSG-08
tell-audit discriminates on **derivability against the trace**: a correct call
*derived* from brief facts (traceable in the trace) is a lucky/legit prediction; a
call that *asserts* the outcome or cites non-brief knowledge with no derivation is
a **confirmed tell**. A confirmed tell is a **hard contaminated route** (owner
decision 3) into the existing contaminated branch; the strictness lives in the
"confirmed" bar (derivability), never in a post-reveal graded frame (gameable). A
contaminated arm is **quarantined = recorded-as-data, NOT deleted** (owner decision
2; reconcile the protocol `reject` branch to mean "not clean evidence for that
model family," not "data removed").

## R5 — Decision-framing, never test-framing (leak-safety; from the packet review)

REQUIREMENT (this is the recurrence-proof fix for the enumerated-spoiler leak):
- The participant packet is a **genuine decision brief** — "advise [company] at
  [cutoff]; what is the best way forward?" — **never a test.** No "you cannot
  observe the outcome / do not use [categories]" warning, because a decision brief
  has no hidden answer to warn about.
- **Whitelist, never blacklist.** The only surviving meta-instruction is generic:
  "decide using only the information in this brief; not outside or later
  knowledge." No enumerated forbidden categories on ANY contestant-readable or
  blind-constructor-readable surface.
- **Spoiler taxonomy lives ONLY in the sealed facilitator-only record** — never the
  ledger body or the packet.
- The reasoning trace doubles as the contamination probe (mini-god-tier: one
  artifact, two jobs). Foregone limitation, named: a passive trace catches
  contamination that shows, not clean concealment.

## R6 — Pre-freeze leakage-review gate (now load-bearing)

REQUIREMENT: a participant packet cannot clear JSG-02 (freeze) without passing an
independent leakage review. RATIONALE (proven on Beauty Pie): outcome-blind
construction can *manufacture* a leak it cannot see (the blind constructor wrote
the forbidden-list it couldn't tell was a spoiler). The independent review is the
only thing that catches this class — so it is a **gate, not optional hardening.**

## Routed-out owner-territory changes (the addendum proposes; owners enact; then re-review)

1. Rewrite the JSG-05 probe protocol: non-inducing pre-judgment screen; remove
   active recall entirely. (Probe-protocol owner.)
2. Add a JSG-08 `outcome_knowledge_audit` field (tell_present | packet_derivable |
   not_assessed), provenance-bound to packet + sealed-output hashes. (JSG-08 owner.)
3. Add the conductor transition entry mapping `tell_present` -> contaminated/blocked.
   (Conductor.)
4. Author the four R2 outcome-blind fields as JSG-02/JSG-03 freeze-receipt fields
   with a clear-predicate. (Evidence-ladder / packing owners.)
5. Make the JSG-06 reasoning-trace a required receipt field. (No-tools contract owner.)
6. Add the R6 pre-freeze leakage-review checkpoint to JSG-02; and add R5
   decision-framing / whitelist + sealed-only-spoiler rules to the construction
   protocol + case-frame template (incl. an audit of the FeedHaven/Inoreader
   exemplars for the same blacklist pattern). (Construction-protocol + template owners.)
7. (Optional) a read-pack cue routing case-run work to the conductor, by its owner.

## Boundary / non-claims

Requirements + routed proposals only. Enacts nothing; ratifies nothing; clears no
gate (predicates stay `indeterminate_until_authored` until owners author them).
Product-learning tier; the rules apply as by-hand discipline meanwhile.
Cross-vendor delegated re-review returned (2026-06-12); the one minor finding
(ARV1-01) is patched; pending owner ratification.
