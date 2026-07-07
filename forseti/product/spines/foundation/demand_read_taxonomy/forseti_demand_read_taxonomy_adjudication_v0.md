# Forseti Demand-Read Taxonomy — Adjudication Prep v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact (adjudication-prep companion to the PROPOSED demand-read taxonomy)
scope: >
  Brings forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_v0.md from a
  fleshed sketch to an owner-adjudicable state: operative definitions
  (what-counts / anti-trigger / boundary) for every signal layer and read
  type, the internal tensions named as tensions, and an explicit owner-decision
  queue (Q0 demand-state model [decided 2026-06-14], Q1 pricing refinement, Q2
  wind-caller primacy, Q3 channel-vs-person boundary). Prepares the
  adopt/amend/reject decision; does not make it.
use_when:
  - Adjudicating the demand-read taxonomy (adopt / amend / reject) in one pass.
  - Checking the operative definition or anti-trigger for a signal layer or read type before scanning.
  - Resolving the pricing-signal refinement, wind-caller primacy, or channel-vs-person boundary.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_v0.md          # the PROPOSED grammar this prepares
  - docs/decisions/forseti_product_thesis_consumer_demand_v0.md          # controlling thesis (costly-behavior primitive, action ceilings)
  - docs/decisions/wind_caller_calibration_carveout_v0.md             # the carve-out reconciled in Q3 (incl. 2026-06-14 amendment)
  - forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md           # Demand-Substrate Hard Gate (anti-trigger source)
stale_if:
  - The owner adjudicates (adopt / amend / reject) — fold the decided word into the taxonomy as v1 or a dated amendment, then retire or supersede this prep.
  - The thesis, wedge, buyer-proof packet, or wind-caller carve-out is amended (re-derive against the amended text).
```

## Status

`ADJUDICATION_PREP_PENDING_OWNER` — prepared 2026-06-14 by the product-direction
lane from the PROPOSED taxonomy (`forseti_demand_read_taxonomy_v0.md`,
`PROPOSED_PENDING_OWNER_ADJUDICATION`) and the controlling thesis, wedge,
buyer-proof packet, venue card set, and wind-caller carve-out (read off fresh
`origin/main`). This is a companion, not a replacement: the taxonomy stays the
PROPOSED grammar; this artifact fleshes it to adjudication-readiness and queues
the owner's open decisions. **The lane prepares the decision; it does not
decide.** No layer ranking is chosen here; Q2 is surfaced as an owner value-call.

This is not validation, readiness, buyer proof, or judgment-quality evidence.
It authorizes no scan, capture, monitoring, or outreach.

**Update 2026-06-14 (owner-authorized in-thread — "fix the 1 thing"):** the
*residual-text inconsistency* flagged below (Tension C, Q3, the Part-1
calibration boundary, and the Part-5 plan item) — the taxonomy's
wind-caller-calibration read-type line and Non-Claims line still saying
"channel-level only" while Signal Layer 2 was already reconciled — **has been
fixed in the taxonomy** (`forseti_demand_read_taxonomy_v0.md`, dated note in its
Status). Those passages are retained below as written, for the audit trail of
what prep found. With that fix landed, **Q3 now reduces to two open items**: (a)
your confirmation of the boundary *policy*, and (b) the optional org-motion-≠-
wind-caller distinction sentence (the conflation guard), which was *not* added —
it is a separate recommendation, not part of the inconsistency that was fixed.

**Update 2026-06-14 (owner-decided in-thread — the demand-state model, Q0):** the
central axis moved from **durable vs hollow** to **durable vs transient**
(persistence) × **real vs manufactured** (integrity). "Hollow" is retired (it
conflated transient-real with manufactured-fake). Three actionable states —
durable (commit), transient (move, short horizon), manufactured (discount /
avoid). Transient gets **equal billing** with durable (owner call); the
decay-timing problem is later **dissolved** by the calling sequence (observe
persistence, not predict decay — see the Q0 *Refined* note below), so transient
reads are **built-to-not-proven-at** until a decay-curve capability exists,
rather than capped by a standing guardrail (reconciled 2026-06-14, OF-01 —
consistency with the dissolve, no policy change). The taxonomy's layers and read
types are restructured to this model (its dated amendment); the controlling
thesis is amended by dated pointer (receipt at the end of the thesis). Part 1's
read types and Part 3's queue below are updated accordingly — Q0 is added as the
now-decided lead, and Q1/Q2 inherit the horizon dimension.

**Update 2026-06-14 (owner adjudication — Q1–Q3 all decided):** Q1 ratified; Q2
adopted (wind-callers primary-at-trigger / earned, buy-side primary at the durable
upgrade, conservative default + an evidence-to-prove note); Q3 confirmed + refined
(≤5 / attended cap scoped to IG/TikTok platform capture; broader named-public-figure
calibration allowed, non-permanent; the carve-out was amended). **Q0–Q3 are now all
decided** and folded into the taxonomy (plus the carve-out and the thesis pointer).

> **Updated 2026-06-15 (owner):** cap now counts own operating/capture accounts
> (≤10, starting ≤5), not subject creators; subject-creator roster is uncapped
> (all creators in the vertical). Active capture = attended (human-initiated);
> passive monitoring = human-initiated, time-bounded, self-terminating. See
> carve-out 2026-06-15 amendment.

## How To Read This (for the owner, one pass)

1. **Operative definitions** — the grammar fleshed so the scanning lane could
   hunt from it: for each signal layer and read type, *what counts*, the
   *anti-trigger* (what looks like signal but is not), and the *boundary*.
2. **Tensions** — three places where the grammar pulls against itself. Named,
   not averaged away.
3. **Owner-decision queue (Q1–Q3)** — each framed as a decision, with the
   lane's reasoning and a clearly-labelled *recommendation* where the lane has a
   defensible call. A recommendation is not a decision; the owner adjudicates.
4. **Capture build-order join point** — one note naming who re-ranks capture on
   adjudication (the capture lane, not this one).
5. **Propagation plan (prepared, not executed)** — what the thesis and the
   taxonomy owe on adoption.

---

## Part 1 — Operative Definitions

Each definition is anchored to its controlling source. The action-ceiling verb
set (`act / phase / narrow / hold / defend`) is carried verbatim from the
taxonomy, value proposition, and buyer-proof packet; per the thesis, the verb
may never exceed what signal integrity supports.

### Signal Layers

**Layer 1 — Trend vector (TrendVector)** (the object of the read)
- *What counts:* a directional movement in demand toward or away from an
  ingredient, category, format, or claim, carrying **direction + velocity + the
  durability question** (owner example: peptides).
- *Anti-trigger:* bare momentum, a coverage spike, or an engagement surge
  reported *as* a trend without the durability question attached; a one-venue
  spike treated as a vector.
- *Boundary:* a trend vector is the **object** of a read, never itself a read,
  and is **never reported as bare momentum** (taxonomy). Durability stays an
  open question until the buy-side layer grades it.

**Layer 2 — Wind callers (WindCaller)** (the leading indicators)
- *What counts:* per vertical × sub-niche, the specific channels, accounts,
  communities, or detectors whose **early public calls (Call) precede the move**,
  tracked through their public output and call record. Worked in-repo exemplars:
  INCIDecoder (card 11 — root-receipt detector whose commissioned SPF tests
  became the receipt the whole Purito chain cites); ingredient-audit blog
  cluster (card 10 — silent-reformulation detection by INCI diff); Reddit
  r/BeautyGuruChatter (card 5 — detector-collective).
- *Anti-trigger:* follower count or reach treated as wind-calling **without a
  call-vs-outcome record**; sponsored/promotional posts treated as organic
  calls (these are integrity-flagged, not calls); a loud account with no
  precede-the-move track record.
- *Boundary:* **channel-level public output by default**; under the bounded
  internal carve-out (`docs/decisions/wind_caller_calibration_carveout_v0.md`,
  owner-signed 2026-06-13, amended 2026-06-14) named **public-figure**
  creator/influencer wind-callers may additionally be calibrated by public
  handle + public name + public calls + public stats + call-vs-outcome record —
  **≤10 own operating/capture accounts (starting ≤5); subject-creator roster
  uncapped within the vertical; active capture: attended (human-initiated),
  faster-than-human pace; passive monitoring: human-initiated, time-bounded,
  self-terminating (no discovery during); pre-commercial, internal-only**.
  Person-level dossiers in any **sold or external** surface remain forbidden
  (charter exclusion, unchanged). **This boundary is distinct from
  org-motion's** (Layer 4) — see Tension C / Q3.

**Layer 3 — Buy-side corroboration** (PRIMARY — owner word)
- *What counts:* **costly behavior** — sellouts, waitlists, restock pressure,
  review velocity and content shifts, pain-point convergence, dupe-seeking and
  switching **with stated cause**, effortful UGC. Per the thesis costly-behavior
  primitive: payment, switching, workarounds, churn, durable buyer pressure.
- *Anti-trigger:* **attention/engagement/resonance volume standing alone** (likes, views,
  comment counts, coverage volume) — it *caps* the action ceiling and can never
  carry a Commit; public engagement should still be read as qualitative resonance
  weight below proof. Virality / creator attention used as a buyer filter (per the
  Hard Gate these are **trigger and candidate-context ordering only**).
- *Boundary:* the **primary** layer (owner word). Must clear the **Demand-
  Substrate Hard Gate** (buyer-proof packet, re-derived 2026-06-12): at least
  **two independent venue families** + costly-behavior anchoring + applicable
  integrity labels, else **disqualify or hold** — never a single-venue or
  engagement/resonance-only memo.

**Layer 4 — Supply-side org motion** (SUPPLEMENT — owner word)
- *What counts:* operators' revealed bets — ad launches, hiring direction and
  composition, headcount trend at **brand and parent level**,
  product-pipeline / launch signals, retail placements. An insider demand
  forecast expressed in spend.
- *Anti-trigger:* org-motion **leading** the read (it corroborates or
  contradicts, it never leads); a single job posting read as a trend; any
  person-level hiring read.
- *Boundary:* **corroboration inside the artifact, never a standalone product**;
  **always org-level** (hiring composition, headcount) — **never person-level
  dossiers** (thesis + wedge boundary). Route bindings are capture-lane-owned
  under the measured-ToS-risk posture. **The wind-caller carve-out does NOT
  touch this rule** — org-motion has no carve-out (see Q3).

**Layer 5 — Integrity layer** (the discriminator)
- *What counts:* manufactured-versus-organic labels — paid-promotion flags,
  engagement anomalies, astroturf / bot marks, dupe-wave distortion, incentive
  distortion, copied/coordinated marks; and **cross-venue disagreement**.
- *Anti-trigger:* **averaging cross-venue disagreement away as noise** (it is
  itself a divergence signal); treating **absence of a flag as proof of
  organic** — manufactured-demand separation is a forward/live capability;
  backtests cannot recover historical paid-proxy spend (thesis honest-scoping).
- *Boundary:* the layer **labels and discounts; it never produces manipulation**
  (Orca detects, never astroturfs). Manufactured-vs-organic is claimed only at
  forward/live strength, with cross-signal consistency as a *partial* flag.
  Integrity caveats travel with every signal into the artifact.

### Read Types

> Read types now follow the demand-state model (Q0, decided 2026-06-14): two
> axes — durable vs transient × real vs manufactured — yielding three actionable
> states. Divergence is a *technique*, not a read.

**Durable-demand (Reading) read** — real + projected to stay strong →
*commit / scale as earned*
- *What counts:* effectively independent demand origins + wind callers + org
  motion pointing the **same way**, costly-behavior anchored, with a named basis
  for projecting persistence over the decision horizon (owner example:
  peptides). Observed persistence is one support path, not the definition.
- *Anti-trigger:* convergence asserted on engagement/resonance volume; single-venue
  agreement dressed up as multi-venue; convergence without costly behavior; a
  **spike mistaken for persistence** (decay not assessed).
- *Boundary:* must clear the Hard Gate; ceiling capped by signal integrity.

**Transient-spike (Reading) read** — real + strong current-window demand →
*probe / commit in-window*, time-boxed (NEW; owner equal-billing 2026-06-14)
- *What counts:* real strong costly behavior with a **short expected lifespan**
  or without enough basis to project persistence — a genuine spike that will
  normalize (viral surge, time-limited dupe wave, seasonal pop).
- *Anti-trigger:* a spike treated as durable (commit long → stranded inventory);
  a manufactured pump mistaken for a real spike (integrity layer must clear it first).
- *Boundary:* **equal billing as a read**; weak, attention-only, or resonance-only
  input is not transient demand, and manufactured hype is not transient demand. Durability is
  a projected persistence call with a named evidence basis; monitoring builds or
  defeats that basis. A transient call is **built-to, not proven-at** on its
  exact lifespan until a decay-curve capability exists (reconciled 2026-06-14,
  OF-01; clarified 2026-06-23).

**Manufactured-demand (Reading) read** — fake / amplified → *discount / avoid*
- *What counts:* demand that is not real — promotion-engagement mismatch,
  astroturf, coordinated/bot amplification, dupe-wave distortion.
- *Anti-trigger:* a single contrarian voice promoted to "manufactured"; treating
  **absence of a flag as proof of organic**.
- *Boundary:* identifying manufactured demand is **decision-critical in its own
  right** (owner) — the contamination check protecting both real reads; acting on
  someone else's manufactured spike commits to demand that was never yours.

*Divergence is a technique, not a verdict* (owner 2026-06-14): signals
disagreeing — promotion-engagement mismatch (an influencer promotes X but ad
engagement runs **below their own baseline**), venue sentiment splits (TikTok
disagrees with IG), a quality attack where marketing is loudest (Reddit attacking
quality under a promo push) — is *evidence used to classify* a candidate as
transient or manufactured. No longer synonymous with "hollow."

**Brand-decision event (Reading) read** — the monetization unit
- *What counts:* a **named brand (Brand)'s** live allocation decision — launch /
  reposition; retail or channel entry; restock / sellout; discontinuation /
  moratorium; defend-versus-hype; **event-triggered pricing** (batch-1's Beauty
  Pie 2023 repricing is exactly this). Trend vector + wind-caller state +
  integrity labels are the context that makes it decide-grade.
- *Anti-trigger:* a "decision event" with no named brand or no live/imminent
  allocation choice; **price-complaint chatter triggering a pricing-event read**
  (see Q1).
- *Boundary:* the monetization unit; carries an explicit action ceiling
  (`monitor / probe / commit / hold / scale / avoid / reduce`) capped by signal integrity; tied to a
  named decision owner + allocation consequence per the buyer-proof packet.

**Wind-caller calibration (Reading)** — the compounding asset
- *What counts:* grading each niche's wind callers' **public calls against
  observed outcomes (Outcome) over time**; dated, anti-cherry-picked receipts ("who
  actually calls beauty winds, with receipts"). The outcome-memory moat applied
  to sources.
- *Anti-trigger:* cherry-picked hits; calibration with no dated pre-declaration;
  reach / follower count used as a calibration proxy.
- *Boundary:* channel-level by default; under the carve-out, **named
  public-figure calibration** is permitted (internal-only; ≤10 own
  operating/capture accounts, starting ≤5; subject-creator roster uncapped
  within the vertical; active: attended human-initiated pace; passive:
  human-initiated, time-bounded, self-terminating). **Unreconciled-text flag:**
  the taxonomy's calibration line and its Non-Claims still read "channel-level
  only," while Signal Layer 2 was already reconciled with the carve-out —
  adoption must reconcile all three (Q3).

---

## Part 2 — Tensions (named, not resolved)

**Tension A — buy-side-primary vs "maybe the main wind callers actually."**
The taxonomy locks buy-side corroboration as primary (owner word) and org-motion
as supplement, consistent with the OWNER_LOCKED thesis ("demand means costly
behavior"). But the same owner flagged influencers as **"maybe the main wind
callers actually."** Wind callers are currently typed as a *leading-indicator*
layer feeding a buy-side-primary read; the owner's aside would make them a
*primary* layer in their own right. These cannot both be the headline without a
ranking call. → **Q2.**

**Tension B — price-complaint-as-anti-trigger vs price-rerouting-as-signal.**
Both are "price-driven," and the grammar treats them oppositely: complaint
*volume* is an anti-trigger (chronic, non-discriminating, ungradeable, almost
never resolves into an event), while price-driven *rerouting* (dupe adoption,
trade-down, switching with stated cause) is one of the most legible buy-side
signals beauty offers. The risk is conflation in scanning — a complaint wave
mistaken for rerouting, or rerouting suppressed because it is "just price." The
discriminator is **costly behavior with stated cause** (rerouting = gradeable
switching) vs **ungradeable chatter** (complaint = attention volume). → **Q1.**

**Tension C — channel-not-person boundary vs the carve-out's named-public-figure
calibration.** The taxonomy's founding line was "wind callers are channels, not
persons." The owner-signed carve-out (2026-06-13, amended 2026-06-14) permits
**named public-figure** creator/influencer calibration at small internal scale.
Signal Layer 2 of the live taxonomy was updated to the reconciled form, but **two
other lines were not** (the wind-caller-calibration read-type and the Non-Claims
both still say "channel-level only"). Separately, the wedge is explicit that this
carve-out is **distinct from org-motion**, which stays org-level-only with **no**
carve-out — a conflation risk if the two person-boundaries are read as one. →
**Q3.**

---

## Part 3 — Owner-Decision Queue (explicit; recommendation ≠ decision)

> Each entry is a decision the **owner** makes. The lane's *recommendation*,
> where given, is a defensible call offered for efficiency — it is **not** the
> decision and binds nothing until the owner adjudicates.

### Q0 — Demand-state model (DECIDED 2026-06-14; the lead decision)

**Decided (owner, in-thread):** replace **durable vs hollow** with **durable vs
transient** (persistence) × **real vs manufactured** (integrity). Three actionable
states — durable (commit/scale), transient (commit, reversible — reduce on decay),
manufactured (avoid). **Transient gets equal billing**
with durable (owner: spikes are still capital-allocation decisions and occur more
often). Divergence becomes a **technique, not a verdict**. Identifying
manufactured demand is **decision-critical in its own right** (owner).

**Refined 2026-06-14 (owner) — the calling sequence dissolves the decay-timing
problem; clarified 2026-06-23:** the read opens **current-window transient**
unless a durability basis is already in the information set, acts in-window (buy
or avoid/reduce), then uses monitoring to strengthen, revise, scale, or reduce
the persistence projection — no decay curve to predict; the earlier
decay-timing-confidence guardrail is superseded by basis-don't-guess. The
recurring monitoring is **decision-linked retainer billing** (upgraded billing),
never a feed — every output is a calibrated decision with an action ceiling,
which keeps the retainer off the buyer-proof "monitoring-only pull" kill and out
of the social-listening category. Monitored outcomes are also the calibration
data that earns the judgment moat.

**Differentiation floor (owner insight):** the mechanical layers (costly-behavior
primitive, org-motion fusion, entity resolution) beat a social listener's inputs
but are replicable features — a survivable fallback business, not a moat. Judgment
+ outcome memory is the uncopyable differentiator and the category-definer; don't
sell the plumbing.

**Status:** executed into the taxonomy (Calling Sequence kept as *grammar*) and
the controlling thesis (dated amendment + body integration 2026-06-14: central
read, value proposition, strategic center, boundary). Commercial/positioning
parts re-homed to their owners — billing shape → offer hypothesis (Commercial
Frame Status, as input to the pricing CA run); never-a-feed invariant →
buyer-proof packet (Orca Promise); differentiation floor → thesis (Strategic
Center). Grammar ≠ ontology: decision-grade validation is a separate, already-
commissioned ontology pass, not this taxonomy. Q1 and Q2 below inherit the
horizon dimension. Nothing pending on Q0.

### Q1 — Pricing-signal refinement

**DECIDED 2026-06-14 (owner): ratified as written** ("yes i believe this is
adequate"). The Pricing Refinement section is now owner-ratified; the framing
below is retained.

**Decision:** ratify, amend, or reject the taxonomy's proposed final take on the
owner's pricing question:
- price-**complaint volume** = anti-trigger (never a scan trigger);
- price-driven **rerouting** = real buy-side signal (costly, gradeable switching);
- **pricing-decision family** = retained, **event-triggered only** (a price move
  that happened or is visibly imminent; complaint chatter alone never triggers).

**Lane reasoning:** the three-way split is coherent with the thesis
costly-behavior primitive and the Hard Gate (engagement/chatter volume caps the
ceiling; costly switching anchors a read). The only live failure mode is
*conflation at scan time* — a checker that cannot tell complaint volume from
rerouting will either over-trigger on chatter or miss real rerouting.

**Lane recommendation (not a decision):** *ratify as written*, with one
adjudication-time clarification folded in — the scan discriminator is **stated
cause + switching behavior** (rerouting) vs **standing chatter** (complaint).
That clarification is wording, not a new decision; it is offered so the scanning
lane inherits an unambiguous test.

### Q2 — Wind-caller primacy (owner value-call; the lead decision)

**DECIDED 2026-06-14 (owner): adopted** ("yeah i think that's okay — but note down
on the evidence thing to prove"). The new-model resolution: wind-callers are
**primary at the trigger** (their early call opens the transient read); **buy-side
costly behavior is primary at the durable upgrade**; standalone trigger-weight is
**calibration-gated**, with the **conservative default** (Hard-Gate corroboration
even for a transient move) holding until evidence. **Evidence to prove
(owner-flagged):** that beauty wind-callers actually precede the move reliably —
the calibration ledger must demonstrate it before trigger-weight shifts toward
wind-callers. Folded into taxonomy Layer 2. (The (a)/(b) framing below is the
pre-adjudication queue; the sequence-position resolution supersedes it.)

**Decision:** are wind-callers / influencers the **primary** signal layer, or a
**leading indicator** feeding a buy-side-primary read?
- **(a) Leading-indicator** (current default): buy-side costly behavior is
  primary; wind callers are the early-warning layer; org-motion supplements.
  Matches the OWNER_LOCKED thesis and the taxonomy as written.
- **(b) Wind-caller-primary:** influencers/detectors become the headline layer
  ("the main wind callers actually"), with buy-side as confirmation. This would
  re-rank the grammar and change what the scanning lane leads with.

**Lane reasoning:** this is a **value-call, not derivable** from current sources
— it is the one Complex seam. (a) is what the thesis locks and what the Hard
Gate's costly-behavior anchoring assumes; moving to (b) would put a layer whose
own anti-trigger is "reach without a call-vs-outcome record" in the lead, which
raises the manufactured-demand exposure the integrity layer exists to contain.
But the owner's instinct is real: in beauty, wind-callers frequently *precede*
and arguably *cause* the buy-side move, so calibrated wind-callers could be the
highest-information layer once the calibration moat exists.

**Lane recommendation (not a decision):** keep **(a) leading-indicator as the
operative ranking now**, and treat **(b) as an earn-in**: wind-callers graduate
toward primary *for a given niche* only once their calibration ledger
(Q3-permitted) shows a dated, anti-cherry-picked precede-the-move record. This
preserves the thesis lock while honoring the owner's instinct as a measurable
promotion path rather than an upfront re-rank. **The owner may simply choose (a)
or (b); the recommendation is a middle path, not the decision.**

> **STOP-condition check:** fleshing did **not** force this choice — both
> rankings are fully fleshed above and the grammar stands under either. Per the
> commission, had fleshing forced the ranking, the lane would stop and surface
> it as the lead decision; it is surfaced as the lead decision regardless, but
> no fleshing was blocked.

### Q3 — Channel-not-person boundary (confirm the reconciliation)

**DECIDED 2026-06-14 (owner): confirmed + refined.** The ≤5-accounts / attended
cap is scoped to **IG/TikTok-style platform creator capture**; named public-figure
calibration from other public outputs is **broadly allowed and non-permanent**;
internal-use only and the external/product boundary are unchanged. The
**carve-out was amended** (dated) and the taxonomy boundary (Layer 2 / calibration
read-type / non-claims) + the thesis pointer updated to match.

> **Updated 2026-06-15 (owner):** cap now counts own operating/capture accounts
> (≤10, starting ≤5); subject-creator roster uncapped (all creators in the
> vertical). See carve-out 2026-06-15 amendment.

**Decision:** confirm the wind-caller boundary as reconciled with the carve-out:
- channel-level public-output calibration of **named public-figure**
  wind-callers is **allowed** (≤5 accounts, human-mimicking attended-automated
  pace, pre-commercial, internal-only);
- person-level dossiers in any **sold or external** surface remain **forbidden**;
- this is **distinct from org-motion**, which stays **org-level-only with no
  carve-out**.

**Lane reasoning:** the reconciliation already exists in the carve-out (live on
`origin/main`, including the 2026-06-14 attended-automated-pace amendment) and in
Signal Layer 2 of the taxonomy. Two cheap, load-bearing defects remain: (1) the
taxonomy's **wind-caller-calibration read-type line** and its **Non-Claims line**
still say "channel-level only," contradicting the reconciled Layer 2 — an
internal inconsistency in the live doc; (2) nothing in the taxonomy yet states
the **org-motion ≠ wind-caller** boundary distinction the wedge is explicit
about, leaving a conflation risk.

> **Updated 2026-06-15 (owner):** cap now counts own operating/capture accounts
> (≤10, starting ≤5); subject-creator roster uncapped (all creators in the
> vertical); active/passive method redefined — see carve-out 2026-06-15
> amendment.

**Lane recommendation (not a decision):** *confirm the reconciled boundary*, and
on adoption fix both residual lines (calibration read-type + Non-Claims) to the
Layer-2 reconciled form **and** add one sentence stating the org-motion boundary
is separate and uncarved. This is the cheapest way to make the live grammar
internally consistent. **The owner may instead amend the boundary itself; the
recommendation only addresses the text drift, not the policy.**

---

## Part 4 — Capture Build-Order Join Point (named, not owned)

On adjudication, the **capture-spine lane** (not this lane) re-ranks its
historical-capture build order to match the adjudicated layer priority. Under the
current buy-side-primary default, the capture lane's own sequencing leads with
the most archive-backtestable layers — **org-motion** (LinkedIn company pages /
Greenhouse boards at cutoff, owner-probed) and **web wind-callers** (direct-fetch
detector venues: INCIDecoder, ingredient-audit blogs, Reddit detector
collectives). This lane **names** the join; it does **not** own, design, or
re-order capture, and produces no capture authorization. A Q2 outcome of (b)
would change which layer the capture lane builds first — another reason the
ranking is the lead decision.

---

## Part 5 — Direction-Change Propagation Plan (PREPARED, NOT EXECUTED)

Per the Doctrine Change Propagation Contract
(`.agents/workflow-overlay/source-of-truth.md`), adopting the taxonomy is a
`product_doctrine` change: the thesis owes a **dated pointer** and the taxonomy
itself is folded forward. This plan lists the surfaces; **the owner's adoption is
the act that executes it.** Nothing below is edited by this lane.

```yaml
direction_change_propagation_PLAN:   # prepared only — not a completion receipt
  executes_on: owner adoption of the demand-read taxonomy
  doctrine_changed: >
    The demand-read taxonomy becomes Forseti's operative scan→capture→clean→judge
    read grammar (signal layers, read types, pricing refinement, wind-caller
    boundary), at the adjudicated Q1–Q3 outcomes.
  trigger: product_doctrine
  related_triggers: []   # confirm at execution; add only if a surface-routing dimension is materially touched
  controlling_sources_to_update:
    - path: forseti/product/spines/foundation/demand_read_taxonomy/forseti_demand_read_taxonomy_v0.md
      change: fold the adjudicated word in as v1 or a dated amendment; flip status off PROPOSED; fix the Q3 residual lines if Q3 confirmed
    - path: docs/decisions/forseti_product_thesis_consumer_demand_v0.md
      change: add a dated pointer to the adopted taxonomy (the thesis's owed pointer); no thesis rewrite
  downstream_surfaces_to_check:
    - path: forseti/product/spines/product_lead/buyer_proof/forseti_buyer_proof_packet_v0.md
      why: Demand-Substrate Hard Gate is the anti-trigger source; confirm no drift if Q1 amends pricing handling
    - path: docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
      why: org-motion-vs-wind-caller boundary distinction (Q3) is asserted there; keep consistent
    - path: docs/decisions/wind_caller_calibration_carveout_v0.md
      why: Q3 boundary owner; confirm taxonomy text matches the carve-out's reconciled form
    - path: docs/prompts/product-planning/consumer_demand_scanning_lane_commission_prompt_v0.md
      why: the scanning lane hunts from this grammar; Q1/Q2 outcomes change what it leads with
    - path: docs/workflows/orca_repo_map_v0.md
      why: optional Product Anchor / row entry if the adopted taxonomy becomes a routing surface (advisory; repo-map-ack otherwise)
  direction_change_propagation_note_2026-06-15: >
    Downstream surface of carve-out 2026-06-15 cap-redefinition: cap now counts
    own operating/capture accounts (≤10, starting ≤5), not subject creators;
    subject-creator roster is uncapped (all creators in the vertical);
    active capture = attended (human-initiated); passive monitoring =
    human-initiated, time-bounded, self-terminating (no discovery during).
    All three live boundary sites in this file updated accordingly. Dated-historical
    Q3 sites (Status block, Q3 decided record, Q3 lane-reasoning) received
    forward-pointing notes only — not retro-edited.
  stale_language_search_at_execution: >
    rg -n "channels, not persons|channel-level public-output|PROPOSED_PENDING_OWNER_ADJUDICATION|buy-side primary"
    docs/product/product_lead docs/decisions
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not a completed propagation receipt (this is a plan; adoption executes it)
```

---

## Validation Gates (this lane's own checks)

1. `SOURCE_CONTEXT_READY` declared before APPLY — **met** (ledger in the
   handoff; sources read off fresh `origin/main`; stale working-tree taxonomy
   caught and corrected to the origin/main version).
2. Every signal layer (5) and read type (4) has an operative definition with
   anti-trigger + boundary — **met** (Part 1).
3. The three named tensions preserved as tensions, not silently resolved —
   **met** (Part 2; each routed to a Q, none averaged away).
4. Owner-decision queue explicit; Q1–Q3 each framed as a decision with a
   labelled recommendation and the decision withheld — **met** (Part 3).
5. Non-claims preserved (still PROPOSED-pending-owner; no
   validation/readiness/buyer-proof; no scan/capture authorization) — **met**
   (Status + Non-Claims).
6. `direction_change_propagation` plan prepared (surfaces listed), not executed —
   **met** (Part 5; labelled PLAN, not a receipt).

## Non-Claims

- `ADJUDICATION_PREP_PENDING_OWNER`. The taxonomy remains
  `PROPOSED_PENDING_OWNER_ADJUDICATION`; this companion changes its readiness by
  nothing. No validation, readiness, buyer proof, or judgment-quality claim;
  closeout state for any such claim: `no_durable_evidence`.
- The lane does **not** decide the layer ranking (Q2) or any owner-decision; the
  owner adjudicates adopt / amend / reject in one pass.
- Authorizes **no** scan, capture, monitoring, or outreach. Names the capture
  build-order join point; owns no capture.
- Does **not** amend the thesis. On adoption the thesis gains a dated pointer via
  the propagation contract — the owner's act, not this lane's.
- Wind-caller tracking stays channel-level public-output plus the bounded
  internal carve-out (named public-figure calibration; ≤10 own
  operating/capture accounts, starting ≤5; subject-creator roster uncapped
  within the vertical; active: attended human-initiated; passive:
  human-initiated, time-bounded, self-terminating; internal-only);
  person-level dossiers in any sold or external surface remain forbidden;
  org-motion stays org-level-only with no carve-out.
- Mints no evidence-ladder vocabulary and redefines no overlay-owned semantics.
```
