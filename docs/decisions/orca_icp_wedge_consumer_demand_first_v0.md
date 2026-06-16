# Orca ICP Wedge — Consumer-Demand-First (Beauty) Direction Proposal v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record (wedge direction lock — owner co-ratified)
scope: >
  The first-proof wedge decision: consumer-demand decision intelligence,
  beauty/personal-care first, operator-brand first door, under the owner's
  no-warm-leads reachability constraint. Prepared 2026-06-11; co-ratified by
  the owner 2026-06-12 (see Status). Supersedes the pricing-first record as
  first-proof wedge authority. Reconciles the wedge chain (dev-facing
  pricing v0 -> break-in-first -> pricing-first un-flip) with the
  owner-signed beauty backtest batch and the org-motion/demand discovery
  input.
supersedes:
  - docs/decisions/orca_icp_wedge_pricing_first_v0.md
use_when:
  - Owner sign-off on the first ICP/wedge for the consumer-demand/beauty direction.
  - Checking how the proposed wedge reconciles with the pricing-first lock.
  - Planning the post-ratification product-doc cascade.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_icp_wedge_pricing_first_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
  - docs/research/orgmotion_demand_signal_wedge_discovery_v0.md
stale_if:
  - The owner amends this record (dated amendments only; no silent rewrites).
  - Batch-1 distillation lands a contrary decide-vs-confirm read on the demand substrate.
  - The no-buyer-contact-before-full-spine-MVP gate is reopened or changed.
```

## Status

`OWNER_LOCKED_DIRECTION` — co-ratified by the owner 2026-06-12, in-thread
(owner words: "co-ratify ok"; thesis ask 2). This record is now the wedge
direction lock and supersedes
`docs/decisions/orca_icp_wedge_pricing_first_v0.md` as first-proof wedge
authority. The executed `direction_change_propagation` receipt for the
ratification event (one receipt covering thesis + wedge cascades) lives in
`docs/decisions/orca_product_thesis_consumer_demand_v0.md`
("Doctrine-Change Propagation — Executed"). The owner's ask-1 amendment
(measured-ToS-risk capture posture) is recorded there and in the decision
memo; it changes this record's org-motion route citations from hard walls to
capture-lane-owned bindings (see the dated notes below).

Historical: proposed as `PROPOSED_PENDING_OWNER_SIGNOFF` by the product-lead
lane 2026-06-11; until ratification the pricing-first record was the current
wedge authority.

A direction lock, if granted, locks a DIRECTION, not a result: not validation,
willingness-to-pay, readiness, buyer pull, or proof the wedge will win.

## Commercial Target Selection Amendment (2026-06-16)

Owner direction on 2026-06-16 confirms the first commercial target class as:

**US-market tractioned indie/DTC beauty or personal-care operators** with a
named founder, head of brand, growth, insights, strategy, or equivalent
decision owner facing a live 30-90 day demand-allocation decision where
internal data is not conclusive and public creator/social/review/search/retail
signals can be fused across at least two independent venue families.

This sharpens the already-ratified operator-first door; it does not create
buyer validation, outreach authority, willingness-to-pay proof, or commercial
readiness. The first decision-family bias is retail/channel expansion,
launch/reposition, and inventory or purchase-depth commitment; tier/price,
taste-shift pivot, and defend/hold against suspected hollow or manufactured
demand remain eligible when they satisfy the same gates.

Retailer/category teams are not the first door because they often have
stronger proprietary sell-through, basket, loyalty, and vendor data, making
the "internal data not conclusive" gate much harder to satisfy. That is a
sequencing risk, not an existential product kill: if operator pull fails, the
standing fallback remains the harder / more-profitable buyer ladder already
named here -- consumer fund screen and then PE/family-office diligence -- by
owner decision at kill time. Agencies and incubators may later help source or
route brand decision owners, but their interest is not buyer proof unless the
accountable brand decision owner enters the proof loop.

Customer-provided proprietary data is a later augmentation path, not a first
proof dependency. Orca may eventually reconcile its public-signal judgment
against buyer-provided sell-through, CRM, panel, retail, or cohort data under a
separately authorized data-spine or proof lane. For this first door, the claim
remains public-first: a manual memo plus evidence appendix must be credible
before proprietary-data intake, data-science work, dashboards, integrations, or
source-system buildout. Public evidence relevance is a plausibility premise,
not a buyer-proof shortcut; Orca still has to observe decision-owner use or
pull before making proof claims.

```yaml
direction_change_propagation:
  doctrine_changed: >
    The consumer-demand first-proof door is sharpened from generic
    indie/DTC beauty operators to US-market tractioned indie/DTC beauty or
    personal-care operators with a named decision owner and live 30-90 day
    demand-allocation decision, biasing first toward retail/channel,
    launch/reposition, and inventory/purchase-depth decisions while
    documenting retailer/category teams as deferred because proprietary
    internal data weakens the first-door public-signal premise, and treating
    customer-provided proprietary data as later augmentation rather than a
    first-proof dependency.
  trigger: product_doctrine
  related_triggers:
    - output_authority
  controlling_sources_updated:
    - docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
    - docs/product/product_lead/orca_offer_hypothesis_v0.md
    - docs/product/product_lead/orca_buyer_proof_packet_v0.md
    - docs/product/product_lead/orca_product_proof_lead_charter_v0.md
    - docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/product-proof.md
    - docs/decisions/orca_product_thesis_consumer_demand_v0.md
    - docs/product/source_capture_toolbox/ig_creator_roster_frontier_ledger_spec_v0.md @ codex/beauty-creator-roster-ledger:7e19ab42
  intentionally_not_updated:
    - path: docs/decisions/orca_product_thesis_consumer_demand_v0.md
      reason: >
        The thesis owns the broader buyer ladder and already delegates first
        application specifics to this wedge record; this patch sharpens the
        wedge and proof instruments without changing the thesis center.
    - path: docs/product/source_capture_toolbox/ig_creator_roster_frontier_ledger_spec_v0.md
      reason: >
        The roster spec is on pending branch
        codex/beauty-creator-roster-ledger at observed HEAD 7e19ab42 and is a
        proposed non-authorizing source-capture spec. Its open question asks
        which first commercial beauty sub-niche, buyer decision, and creator
        universe should anchor the 500-record slice; this patch answers only
        the buyer-class/decision-family side and does not edit that branch.
  stale_language_search: >
    rg -n "inventory/replenishment vs channel expansion|indie/DTC beauty brand
    decision owner|retailer/category teams|agency/incubator|agencies and
    incubators|Consumer fund screen|consumer fund screen|PE/family-office|tractioned"
    docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
    docs/product/product_lead/orca_offer_hypothesis_v0.md
    docs/product/product_lead/orca_buyer_proof_packet_v0.md
    docs/product/product_lead/orca_product_proof_lead_charter_v0.md
    docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md
  stale_language_search_result: >
    Executed 2026-06-16 after this patch. Hits were confined to intended
    target-selection update language, the existing fund/PE ladder references,
    and the retained historical candidate-grid labels. No hit retained the old
    "inventory/replenishment vs channel expansion" mixed-family diagnostic or
    a live first-door phrase that omits the tractioned US-market operator
    narrowing.
  non_claims:
    - not validation
    - not readiness
    - not buyer proof
    - not willingness-to-pay proof
    - not outreach authorization
    - not candidate scan authorization
    - not creator roster construction authorization
    - not implementation authorization
```

## Reconciliation With The Wedge Chain (not a fresh decision)

The commissioning prompt named
`docs/decisions/orca_icp_wedge_convergence_break_in_first_v0.md` as the prior
convergence decision. **Source-state correction:** that record is itself
SUPERSEDED (2026-06-08) by `docs/decisions/orca_icp_wedge_pricing_first_v0.md`
(the un-flip). The chain this proposal reconciles with is:

dev-facing SaaS pricing (v0) -> break-in-first (superseded) -> **pricing-first
un-flip (current lock: AI-monetization B2B SaaS repricing/repackaging, on the
outside-in competitive/market intelligence engine)**.

Preserved unchanged from the chain (these carry forward, not re-decided):

- The ENGINE: one outside-in market & competitive intelligence engine; every
  wedge is an application of it. Consistent with the thesis
  (`docs/decisions/turn_08_product_thesis_v0.md`), which is sector-agnostic and
  already lists pricing/package changes, category entry, and roadmap bets as
  decision families.
- Decision-INPUT framing: a bounded decision artifact (memo + evidence appendix
  substrate; executive deck as the buyer surface), never a monitoring feed,
  dashboard, or source dump (thesis Product Boundary; offer hypothesis).
- The crux question: does public signal DECIDE the decision or merely CONFIRM
  it — still open, now being tested where the proof engine actually runs
  (batch 1, below).
- PE / commercial-diligence = highest-value END-STATE, explicitly "not now"
  (pricing-first retainer map). The discovery note independently converged on
  the same call (PE/family-office = destination, not first door).
- Buyer-as-situation, not segment: a company at a moment where the decisive
  input lives outside its walls (break-in record; retained).

What changes (the supersession being proposed): the FIRST APPLICATION moves
from B2B SaaS AI-monetization repricing to beauty consumer-demand allocation
decisions, and the first door is chosen by reachability under the owner's
no-warm-leads constraint (stated 2026-06-11, discovery note).

Why move off a lock that was not disproven (the honest core):

1. The proof engine has already materially committed to beauty consumer-demand:
   the owner signed backtest batch 1 (2026-06-11,
   `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md`;
   tracked as of the 2026-06-12 ratification) — 4 of 6 cases are beauty consumer-demand decisions and
   the owner relaxed the case family to "any beauty-vertical consumer-demand
   decision." The pricing-first wedge's own decide-vs-confirm cases exist only
   as the two RETRO SaaS dev cases inside that same beauty batch. Doctrine and
   practice have split; the wedge decision should either follow the proof
   engine or explicitly re-aim it (owner option 2 below).
2. Reachability is the binding constraint. The owner has no warm leads in
   either wedge; the primary door-opener is therefore public backtest proof —
   and the proof being produced is beauty, not AI-monetization pricing.
3. The pricing wedge's latest refinement had already moved onto this substrate:
   the SUGGESTED pricing-as-sensitivity-read block (2026-06-09, pending
   product-lead) relocated the differentiated half of the pricing read to the
   demand-side substrate (forum/social reaction). The clean-substrate advantage
   that decided the un-flip had already eroded inside its own record.
4. Same engine either way: beauty consumer-demand exercises capture, cleaning,
   entity-resolution, judgment, and calibration on the same spine. Pricing
   remains an application the engine can re-enter (re-entry candidacy later
   withdrawn by owner word 2026-06-12 — see the amended disposition below).

## Proposed Decision 1 — First ICP / Wedge

First-proof wedge = **beauty / personal-care consumer-demand decision
intelligence**, operator-first.

- Engine (unchanged): outside-in market & competitive intelligence.
  Consumer-demand allocation is its first application.
- First door — buyer: a **US-market tractioned indie/DTC beauty or
  personal-care brand decision owner** (founder, head of brand / insights /
  growth / strategy, or equivalent operator) facing a live 30-90 day
  consumer-demand allocation decision where internal data is not conclusive
  (US-market qualifier per the thesis geography doctrine, owner-adopted
  2026-06-12). Priority decision families: retail/channel expansion or
  contraction, launch / moratorium / reposition, and inventory or
  purchase-depth commitment. Tier/price change, taste-shift pivot, and
  defend/hold against suspected hollow or manufactured demand remain eligible
  when they satisfy the buyer-proof gates.
- The decision the product informs: "is this demand real, durable, and big
  enough to commit inventory, retail, or launch budget to — and at what action
  ceiling (act / phase / narrow / hold / defend)?"
- Lead signal: consumer demand (reviews, forums, social, search). Corroboration:
  org-motion (hiring composition + headcount trend at brand AND parent level),
  kept at org level — never person-level dossiers for org-motion (thesis
  boundary; note: the creator wind-caller calibration carve-out is DISTINCT
  from org-motion — it applies only to internal calibration of public-figure
  wind-callers per `docs/decisions/wind_caller_calibration_carveout_v0.md`
  and does not touch the org-level-only rule here; LinkedIn
  routes per the owning capture decisions — official/manual/entitled today;
  dated note 2026-06-12: route bindings are capture-lane-owned under the
  owner's measured-ToS-risk posture, not hard thesis walls). Divergence reads
  (demand↑+staffing↑ durable; demand↑+staffing-flat flash or
  capital-constrained; staffing↑+demand-flat betting-ahead) are the premium
  element. Org-motion is corroboration inside the artifact, not a standalone
  product.
- Second door (kept warm, NOT first): a consumer-focused seed/VC fund using the
  same read as a deal screen (rank-and-shortlist; a screen has a lower
  reliability bar). This becomes the first door only if operator pull fails or
  the owner re-orders.
- Destination (unchanged): PE / family-office commercial diligence — retainer
  horizon, gatekept, reached after proof exists.
- Pricing-first wedge disposition on ratification: SUPERSEDED as first proof;
  retained as (a) an engine application reachable from the same spine, and
  (b) the two RETRO SaaS dev cases as cross-vertical method anchors.
  [AMENDED 2026-06-12, owner word: "do NOT do poricing - first actually.
  that's too... we cant call any wind for that. we need to hit the harder
  ones / profitable ones"] The original (c) — pricing-first as default
  re-entry candidate on a beauty-wedge kill — is WITHDRAWN: the wedge offers
  too weak a wind-calling demonstration. On kill, re-entry re-forms toward
  the harder / more-profitable end of the buyer ladder (fund screen,
  PE/family-office diligence path), decided by the owner at kill time.

Good-proof-wedge vs durable-market (kept separate, per product-lead method):
beauty is the proof vertical — chosen for substrate richness, running proof
engine, and reachable-cold buyers — not a claim that beauty alone is the
durable market. The engine and entity spine are built narrow (this wedge's
entities) and designed to widen across consumer verticals. Widening is a later
owner decision, not implied by ratification.

## Proposed Decision 2 — Value Proposition / Offer Framing

The sold thing is the **decided answer on one named live decision**, not the
platform, the consolidation, the entity spine, or a feed.

- Buyer-facing artifact: an executive-grade decision deck (deck-first
  preserved from the offer hypothesis), derived from the internal memo +
  evidence appendix substrate that remains the reasoning and proof gate.
- The read it sells: the greatest evidence-supported path for the live
  consumer-demand decision, with an explicit action ceiling (act / phase /
  narrow / hold / defend), what the public signal can and cannot support, and
  what would change the answer.
- The differentiated mechanism (offer-hypothesis mechanism, re-targeted):
  source-backed signal-quality judgment over the demand substrate — cleaning,
  dedup, provenance, artificial-amplification flags — FUSED with org-motion
  corroboration rolled up the brand->parent hierarchy, calibrated by published
  backtests. Not "AI research," not social listening, not trend dashboards.
- Anti-positioning (thesis boundary, restated because this wedge sits closest
  to it): not a social-listening dashboard, not a trend-report subscription,
  not monitoring, not a data broker, not person-level profiles. Incumbent
  beauty trend-analytics vendors exist (unverified context, not researched this
  turn); the differentiation hypothesis is the decided answer + calibration
  receipts, and it must be tested, not asserted.
- Broad offer unchanged: the Strategic Decision Evidence Deck framing and the
  broad decision families in the offer hypothesis stay; this narrows only the
  FIRST-PROOF surface.

## Proposed Decision 3 — Minimum Proof To Open The Door

Under no-warm-leads, the door-opener is **public zero-spoiler backtest
receipts**, in claim-honest form:

- Primary content: batch-1 beauty backtest results (already owner-authorized
  and active; 2 dev + 2 holdout beauty cases plus 2 RETRO SaaS dev cases),
  published as "method called at cutoff vs what happened," including misses —
  the all-results commitment is the credibility asset.
- One org-motion-fused extension (proposed, needs its own authorization): score
  at least one beauty case with the archived org-motion layer (Greenhouse job
  boards / LinkedIn company pages at cutoff via the existing archive adapter)
  to demonstrate the fusion/divergence read in public. This is a dated batch-1
  ledger amendment or a batch-2 item — owner-owned either way; beauty-brand
  ATS/archive coverage is unverified and must be checked per brand first.
- Claim discipline: every published result stays at `product_learning` tier
  (ladder cap; the by-hand surface is permanently non-gate-clearing). Publishing
  is demonstration content, NOT validation, buyer-proof, or judgment-quality
  claims. Zero-spoiler rules apply to any participant-facing reuse.

Is the judgment-batch the minimum proof? It is the minimum **door-opening
content**. It is not buyer proof and does not start the buyer-proof clock:
the first buyer-proof event remains a qualified live decision + memo +
readback under the buyer-proof packet's unchanged gates (trust ladder,
pull-vs-praise, kill/graduation). And it does not open outreach: the standing
owner gate — no buyer contact before full-spine MVP
(`docs/decisions/advisory_proof_slice_definition_v0.md`) — is untouched by this
proposal. Ratifying the wedge orients the MVP and the proof content; opening
outreach is a separate owner decision (sign-off item 4).

## Candidate Grid (fixed comparison fields, compressed)

| Field | A. Pricing-first (current lock) | B. Beauty operator (proposed) | C. Consumer fund screen | D. PE/FO diligence |
| --- | --- | --- | --- | --- |
| Buyer / sponsor | VP Product / pricing lead, B2B SaaS | Indie/DTC beauty founder / insights-growth lead | Seed/VC partner or platform lead | PE/FO deal team |
| Decision informed | Reprice / repackage (AI-monetization) | Demand allocation: inventory, channel, launch, reposition | Invest screen / shortlist | Deal conviction |
| Urgency trigger | Competitor/AI pricing move | Retail window, virality spike, taste shift | Deal pacing (continuous) | Live deal |
| Consequence if wrong | Churn, backlash, revenue capture | Inventory + retail commitment waste, launch misfire | Missed / bad deal | Bad acquisition |
| Public-signal availability | Competitor prices clean; response half sits on demand substrate (sensitivity-read) | Demand venues rich and probe-verified in beauty; org-motion archived | Same as B, portfolio-wide | Eventually needs private data |
| Cold reachability (no warm leads) | Cold; mid gatekeeping | Claimed best: publicly identifiable, proof-receptive (discovery-tier, untested) | Plausible: funds consume public content | Worst: gatekept |
| Paid-first plausibility | Software-budget norms | Smaller budgets; category buys trend reports (unverified context) | Pays for deal-flow edge | Highest value, latest |
| Repeatability | High (repricing recurs structurally) | Medium-high: launch/expansion cadence per brand + cross-brand | High (screen is continuous) | Episodic per deal |
| Proof asset in hand | 2 RETRO SaaS dev cases | Owner-signed active beauty batch + archived org-motion substrate probed | Derived from B's assets | None (interview-gated) |
| Main open risk | Substrate-newness (AR-S2); decide-vs-confirm open | Demand-read reliability open (batch 1 tests it); budget size | Screen interest ≠ artifact pull | Access |

First-door verdict proposed: **B**, C kept warm as second door, A retained as
engine application only (re-entry candidacy withdrawn by owner word
2026-06-12), D destination.

## Load-Bearing Assumption — Assessed (does "lead with demand" survive?)

Assumption under test: the social/demand spines can actually produce a
reliable demand signal; if they are weaker than the org-motion layer, the
sequencing flips.

Assessment: **no flip — lead-with-demand stands**, on three grounds.

1. Capture maturity (repo evidence,
   `docs/product/source_capture_toolbox/capture_recon_index_v0.md`,
   untracked): the demand side has MORE verified capture coverage than
   org-motion, including beauty-specific surfaces — Sephora PDP reviews GO via
   incremental scroll (HIGH, corrected a prior false anti-bot claim), Ulta SPA
   embedded-state HIGH (lane, pending keep-gate), Reddit multiple GO /
   bounded-GO probes plus an offline packet parser spec, Trustpilot/G2
   moderate. Org-motion live is the weaker layer: LinkedIn is a policy
   boundary (no scraping; official/API/manual/entitled routes only),
   senior-moves rosters sit behind auth (not archive-backtestable), and no
   live ATS adapter exists. Org-motion's verified strength is the ARCHIVED
   layer (LinkedIn company pages, Greenhouse boards — owner-attended probes,
   2026-06-11) — a backtest/corroboration substrate, not a live primary signal.
2. Buyer fit: both candidate buyer classes want demand as the primary signal
   (discovery-tier); org-motion alone is a screen, not a thesis.
3. What remains open is not capture but DECISION-GRADE RELIABILITY of the
   demand read — precisely what batch 1 scores (decide-vs-confirm, in-band /
   over / under). The assumption is already under test by an authorized probe;
   no new build is needed before sign-off.

Honest tension carried forward: the pricing-first un-flip demoted reviews as
biased (J-curve) and polluted (FTC 16 CFR 465) for the B2B competitor-customer
read. The consumer-demand wedge knowingly moves the differentiated read onto
that harder substrate — mitigated by multi-venue fusion (forums/social/search,
not reviews-only), org-motion corroboration, and Orca's signal-quality
judgment (the thesis's strategic center), and measured by the batch-1
calibration. That bias risk is a feature of the wedge to be priced in, not
argued away.

Named pivot condition (binds the no-flip verdict): if the batch-1 distillation
shows the demand reads landing confirm-only or unreliable (persistently
out-of-band), the first wedge re-forms around the lower-bar screen — fund-first
(C) and/or org-motion-led shortlist with demand as check — and this record's
operator-first ordering is void.

## Standing Gates Sign-Off Does NOT Change

- No buyer contact before full-spine MVP
  (`docs/decisions/advisory_proof_slice_definition_v0.md`) — owner-owned;
  untouched here.
- Claim tiers and `closeout_state` ownership (evidence ladder; product-proof
  overlay). Batch-1 results stay `product_learning`; no closeout_state is
  minted or upgraded by this record.
- Buyer-proof packet gates: trust_objection vs trust_refusal, pull-vs-praise,
  kill and graduation criteria, paid-first conditions — re-targeted by the
  cascade, not weakened.
- Not-build boundaries: no source systems, dashboards, pipelines, source maps,
  data-spine designs, scoring engines, automation, entity-resolution builds, or
  org-motion adapters are authorized by ratification. The entity-resolution
  spine ("narrow now, widen") is an architecture implication for its own lane,
  not authorized here.
- LinkedIn/social capture policy boundary (official/manual/entitled routes
  only) and Reddit pre-commercial ordering remain as bound in their owning
  decisions.

## Doctrine-Change Propagation — Executed (2026-06-12; receipt in the thesis record)

Co-ratified with the thesis in one ratification event; the single executed
`direction_change_propagation` receipt covering both cascades lives in
`docs/decisions/orca_product_thesis_consumer_demand_v0.md`
("Doctrine-Change Propagation — Executed"). The prepared map below was
consumed by `docs/product/product_lead/orca_ratification_day_runbook_v0.md`
and is retained as history:

| Surface | Change on ratification | Priority |
| --- | --- | --- |
| This record | Status -> `OWNER_LOCKED_DIRECTION`; `supersedes` pricing-first added | P0 |
| `docs/decisions/orca_icp_wedge_pricing_first_v0.md` | Supersession banner (mirror of the break-in banner) | P0 |
| `docs/product/product_lead/orca_offer_hypothesis_v0.md` | First-proof offer layer, ICP status, first-proof fit gates -> consumer-demand/beauty; broad offer unchanged | P0 |
| `docs/product/product_lead/orca_buyer_proof_packet_v0.md` | Proof standard, target buyer, triggers, disqualifiers -> beauty consumer-demand; the reviews-confirmatory-only hard-gate language must be RE-DERIVED for the demand wedge (largest semantic rewrite) | P1 |
| `docs/product/product_lead/orca_product_proof_lead_charter_v0.md` | First-proof lane re-target (named by prior cascades; not re-read this turn) | P1 |
| `orca-product-lead` skill (`.agents/skills/` + `.claude/skills/` copies) | Pins pricing-first as current; needs an authorized skill-edit lane (sha256 pinned in skill-adoption.md) | P2 |
| Discovery instruments (`docs/product/orca_discovery_batch_0_target_selection_brief_v0.md`, `docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md`) | Already flagged stale by pricing-first AR-01 (still hard-gated to dev-facing B2B SaaS); now doubly stale — realign or retire | P2 |
| Checked, no change expected | Thesis (families cover consumer-demand decisions); `product-proof.md` (wedge-agnostic semantics); `source-loading.md` / repo map (wedge is not a routing surface); `AGENTS.md` / `CLAUDE.md` (no wedge content) | — |

## Owner Sign-Off Asks (decided 2026-06-12 — outcomes in Status; retained as asked)

1. **Wedge**: ratify B (beauty operator first door, fund second, PE
   destination, pricing-first superseded-with-re-entry) — or hold the
   pricing-first lock and explicitly re-aim the proof engine back to the
   pricing decide-vs-confirm cases — or amend (e.g., fund-first ordering).
2. **Offer framing**: confirm the decided-answer framing (deck-first decision
   artifact with action ceiling; demand lead + org-motion corroboration inside
   one artifact; no platform/feed positioning).
3. **Proof path**: confirm publish-the-backtests as the door-opening motion at
   `product_learning` claim discipline, and decide whether the org-motion-fused
   case enters batch 1 by dated ledger amendment or waits for batch 2.
4. **Outreach gate**: explicitly keep the no-buyer-contact gate closed (default)
   or name its opening condition (e.g., after batch-1 distillation + N
   published receipts). Ratifying 1–3 does not open it.

## Non-Claims

- Co-ratified 2026-06-12 (see Status) — a direction lock only, not a result.
- Not validation, willingness-to-pay, paid conversion, repeatability, ROI,
  buyer pull, buyer-proof, judgment-quality, product/feature/implementation/
  commercial readiness, or proof the wedge will win.
- The discovery note remains non-authoritative input; this record does not
  promote it. Probe findings cited from it are scouting evidence, not
  method-validation. The capture recon index and batch-1 ledger (both
  tracked as of the 2026-06-12 ratification) are reported as read, with
  acceptance status as stated in those documents.
- Batch-1 results are not prejudged; the no-flip verdict on sequencing binds
  only until the named pivot condition or owner amendment.
- Authorizes no outreach, no implementation, no entity-spine or org-motion
  build, no live-source calls, and no commits/pushes. The downstream product
  corpus cascade ran at ratification (2026-06-12) per the runbook; further
  edits need their own authorization.
- Mints no evidence-ladder vocabulary and changes no overlay rule.
