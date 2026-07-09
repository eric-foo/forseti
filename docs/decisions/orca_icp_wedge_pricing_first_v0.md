# Orca ICP Wedge — Pricing-First Direction (Un-Flip) v0

> **SUPERSEDED AS FIRST-PROOF WEDGE (2026-06-12)**
> The first-proof wedge moves to beauty consumer-demand
> (`docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md`,
> owner-co-ratified 2026-06-12). Pricing-first is RETAINED as (a) an engine
> application reachable from the same spine and (b) the two RETRO SaaS dev
> cases as cross-vertical method anchors. The original (c) — default re-entry
> candidate on a beauty-wedge kill — was WITHDRAWN the same day by owner word
> ("we cant call any wind for that"); on kill, re-entry re-forms toward the
> harder / more-profitable buyer-ladder doors (fund screen, PE/FO diligence),
> owner-decided. The SUGGESTED pricing-as-sensitivity-read block below remains a
> non-frozen historical suggestion inside a superseded record. This record's
> open `direction_change_propagation_blocker` is closed by supersession
> EXCEPT the two discovery instruments (propagation AR-01), whose
> realignment transferred to the consumer-demand cascade: the
> target-selection brief was superseded by
> `docs/product/product_lead/orca_discovery_consumer_demand_target_selection_brief_v0.md`
> and the customer-discovery prompt is queued for a prompt-orchestration
> lane (ORCA-HYGIENE-018).

```yaml
retrieval_header_version: 1
artifact_role: Decision record
scope: Owner-locked UN-FLIP. After two de-correlated verification runs disconfirmed the break-in flip, the first-proof wedge reverts to PRICING — outside-in slice (competitor-/AI-monetization-/backlash-triggered), framed as a decision input on the outside-in competitive/market intelligence engine. Break-in retained as a clean-substrate test + retainer horizon. Carries the doctrine-change propagation blocker.
use_when:
  - Checking the CURRENT first-proof wedge direction.
  - Executing the downstream product-doc cascade in the product lane.
  - Preparing commercial-frame or discovery inputs for the first proof.
authority_boundary: retrieval_only
supersedes:
  - docs/decisions/orca_icp_wedge_convergence_break_in_first_v0.md
superseded_by: docs/decisions/orca_icp_wedge_consumer_demand_first_v0.md
open_next:
  - docs/research/orca_icp_redo_evidence_targets_v0.md
  - docs/research/orca_wedge_alternatives_register_v0.md
  - forseti/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md
  - forseti/product/spines/product_lead/icp_wedge/orca_product_lead_first_icp_wedge_decision_v0.md
stale_if:
  - Owner accepts a different first-proof wedge.
  - The "decide-vs-confirm" method-validation test flips the call.
  - The downstream product-doc cascade lands.
  - The AI-monetization beachhead window matures — target firms commonly gain
    internal AI-pricing history — at which point the "flying-blind" qualifier
    empties out and the beachhead must be re-evaluated.
```

## Status

`OWNER_LOCKED_DIRECTION` — un-flip; owner sign-off 2026-06-08. Supersedes the
break-in-first lock. Locks a DIRECTION, not a result: not validation, WTP,
readiness, buyer pull, or proof the wedge will win.

## Decision

First-proof wedge = PRICING, outside-in slice — competitor-/AI-monetization-/
backlash-triggered repricing and repackaging, framed as a decision INPUT (NOT a
monitoring feed, NOT a private-margin elasticity number). AI-monetization is its
sharpest live instance.

- Engine (unchanged): outside-in competitive & market intelligence. Pricing is
  the FIRST APPLICATION of that engine. Competition stays the spine; pricing is
  the competitive decision with the cleanest public substrate (competitor
  prices/packaging) and the highest decision density.
- Break-in / competitor-customer: DEMOTED to (a) a cheap clean-substrate TEST
  (can non-review public signal + judgment carry the "why are customers leaving
  competitor X" read), and (b) a retainer horizon — NOT the first proof.

## Why (corroborated by two de-correlated verification runs)

The break-in flip rested on ONE argument — the in-house-vs-bought axis (firms
"already buy" win/loss ~36% vs pricing in-house ~6%). Both verification runs (Opus
parallel + owner external o3) independently found:

- The axis has NO independent denominator — every buy-rate is vendor-published;
  there is NO pricing buy-rate at all. The flip's load-bearing reason is a mirage.
- HARD GATE favors pricing. Break-in's differentiated read (a competitor's
  CUSTOMERS' reasons) has only a REVIEW substrate — independently biased
  (self-selection / J-curve) AND polluted (FTC 16 CFR 465; live manipulation
  cases) — and the market is INTERVIEW-GATED (no independent proof a
  public-signal-only read is decision-grade; public-signal products exist only as
  MONITORING). Pricing's read uses competitor PRICES — clean, public, FTC-exempt,
  causally used by 44% of firms (Hinterhuber & Liozu, MIT Sloan, peer-reviewed
  INDEPENDENT).
- The 5-champion Opus tournament converged: every champion (including the
  break-in defender) returned conditional/no; pricing is the least-blocked wedge
  — the only one putting Orca's DIFFERENTIATED read on a clean, decision-moving,
  dense substrate.

Net: the reason to flip TO break-in was disproven; the hard gate + density +
best-evidenced status favor pricing. The break-in detour was not wasted — it
stress-tested pricing and produced a far better-grounded, better-framed pricing
wedge (outside-in / competitive-triggered / AI-monetization, cross-sector-open,
competition-as-engine).

## Retainer map (end-game)

- Near-term retainer: pricing's own density (94-98% reprice yearly, ~40%
  quarterly) — the decision recurs structurally.
- Retainer anchor: positioning / competitive-narrative (continuous), grown into
  after a pricing land.
- High-value end-state: PE / commercial-diligence — the cleanest recurring buyer,
  but interview-built; requires a later interview/first-party method evolution
  (the logged Palantir-esque private-data horizon). Not now.

## The crux test (resolves the residual uncertainty)

Both pricing and break-in pivot on ONE question: does public signal DECIDE the
decision or merely CONFIRM it? Test it in the EXISTING method-validation portfolio
(no buyer contact -> clears the MVP gate): add two cases — (1) a pricing-repricing
case, (2) a clean-substrate competitor-displacement case — each scored on
decide-vs-confirm. This settles the pricing condition (does competitor pricing
decide a repricing move) AND the break-in escape-hatch (can clean non-review
signal carry the customer read) in one move.

## Doctrine-change propagation

product_doctrine change (un-flip). The original product corpus was already
PRICING-centric (offer hypothesis + ICP wedge v0 = dev-facing pricing), so this
un-flip REDUCES propagation distance — the cascade REFINES the existing pricing
framing rather than replacing it. Propagation incomplete -> blocker:

```yaml
direction_change_propagation_blocker:
  doctrine_changed: >
    First-proof wedge reverts from break-in to PRICING (outside-in slice,
    competitor-/AI-monetization-/backlash-triggered), on the outside-in
    competitive/market intelligence engine; break-in demoted to test + retainer
    horizon.
  trigger: product_doctrine
  related_triggers: []
  blocking_surface: >
    docs/product/orca_offer_hypothesis_v0.md,
    docs/product/orca_product_lead_first_icp_wedge_decision_v0.md,
    docs/product/orca_buyer_proof_packet_v0.md,
    docs/product/orca_product_proof_lead_charter_v0.md still carry the OLD
    dev-facing pricing framing, not the outside-in / competitive-triggered /
    AI-monetization / cross-sector-open framing. Durable home is the product lane
    on main; untracked on the ECR branch.
  attempted_check: >
    Locked the un-flip in this record; superseded the break-in-first record;
    pointed the research ledger here.
  allowed_next_step: >
    Owner-authorized product-lane cascade (preferably on main) refining the
    pricing framing: (1) ICP wedge v1, (2) offer hypothesis v1, (3) buyer-proof
    packet + proof-lead charter patches — each with its own DCP receipt. Plus the
    two method-validation cases (decide-vs-confirm).
  non_claims:
    - not validation
    - not readiness
    - not willingness-to-pay
    - not buyer proof
    - not ICP proven
```

## Review adjudication (2026-06-08)

Three Opus adversarial reviews (propagation, non-claims, soundness) of the
product-doc cascade were run and adjudicated (home model). No critical findings;
in-target alignment, non-claims, decision-family stability, and the supersede
marker verified clean, and the cascade correctly held "competitor price DECIDES"
as OPEN, not settled. Accepted major fixes:

- Beachhead RATIONALE re-attached (AR-S1): the "first-time AI-monetization /
  flying-blind" qualifiers are the test INSTRUMENT for the open decide-vs-confirm
  question — they exist because that is where public signal can plausibly DECIDE
  the repricing move (no internal AI-pricing history to fall back on), NOT an
  arbitrary segment filter. Added to the three product-doc refinement banners.
- Substrate-newness tension recorded as a risk the crux test MUST probe (AR-S2):
  in a genuinely first-time AI-monetization wave the competitors are also pricing
  AI for the first time, so the competitor-price substrate is newest/sparsest/
  least-converged — "publicly rich" is NOT yet "clean/decision-grade/stable." The
  decide-vs-confirm method-validation cases must test whether the substrate is
  decision-grade for newly-set prices, or narrow the substrate requirement to
  cases with at least one observable pricing iteration/anchor. (This sharpens "The
  crux test" above.)
- Confirm-vs-decide precision (AR-S5): the "44% causally use competitor prices"
  evidence (Hinterhuber-Liozu) supports competitor price as a USED INPUT
  (CONFIRM-grade), NOT that competitor price DECIDES the move — which remains the
  open crux. The un-flip rests on "least-blocked + clean substrate," NOT on a
  decide-grade reading of the 44% stat; do not read it as stronger than that.
- Beachhead-window staleness trigger added (AR-S3): see `stale_if` above.
- Propagation-completeness gap recorded (propagation AR-01): two LIVE downstream
  qualification instruments still hard-gate to "developer-facing B2B SaaS" and
  were outside the cascade scope —
  `docs/product/orca_discovery_batch_0_target_selection_brief_v0.md` and
  `docs/prompts/product-planning/orca_product_proof_lead_customer_discovery_prompt_v0.md`.
  Until they are realigned (a discovery-lane patch), propagation is INCOMPLETE and
  those instruments would misroute discovery to the demoted dev-facing default.
  Treat them as additional `blocking_surface` for the propagation blocker above.

Deferred / owner-owned: realigning the two discovery instruments (discovery-lane
patch); committing the cascade to `main` for a diff-auditable baseline
(non-claims AR-03). Minor/optional hardening noted, not blocking: offer ICP
review-scope wording (AR-S4), in-body "enough signal" phrasing (AR-S7), banner
reread scope (AR-03), copy-paste DCP prose (AR-04). Full reports:
`docs/review-outputs/adversarial-artifact-reviews/orca_pricing_first_cascade_{propagation,nonclaims,soundness}_review_v0.md`.

These refine the direction record; they do not change the pricing-first
direction. Still not validation / WTP / readiness / ICP-proven.

## SUGGESTED — Pricing-as-Sensitivity-Read framing (NOT FROZEN; pending product-lead)

Status: `SUGGESTED_PENDING_PRODUCT_LEAD` — owner working-direction recorded
2026-06-09; decision-prep only. Not adjudicated, not frozen, and not a change to
the locked pricing-first direction above.

What the pricing product actually is (refinement of "decision INPUT, not a
monitoring feed"):

- The deliverable is a price-SENSITIVITY / reaction read, NOT competitor
  price-CHANGE tracking. Tracking competitor price moves is commodity ("anyone
  can do that") — it is the stimulus, not the product.
- Stimulus (clean / public / dated): the competitor price or packaging move —
  the x-axis of the read, not the deliverable.
- Response (the differentiated, harder half): the public reaction to that move on
  forums / social / reviews (complaint volume, sentiment swing, switching/churn
  chatter, backlash).
- The read pairs stimulus with response across three axes — across a competitor's
  own move history (time), across competitors (cross-section), and the buyer's own
  customers — to graph reaction-to-an-X%-price-change (sensitivity / anchoring).
- Market-level asset: the same read is reusable across every player in a market (a
  later commercial-frame / trust-conflict question, not now).
- It stays a decision INPUT; it is NOT a private-margin elasticity number
  (consistent with the locked Decision above) and NOT a monitoring feed.

Substrate consequence (sharpens "The crux test" and AR-S2): the sensitivity read
moves onto the demand-side substrate (forums/social) — partly the same
biased/polluted substrate flagged for the break-in wedge — so the open
decide-vs-confirm question HARDENS: not "did they use the competitor price" (easy)
but "can public signal carry a DECISION-GRADE sensitivity read" (hard). It stays
better-anchored than break-in because the price move is a clean, dated event to
measure reactions against. The decide-vs-confirm method-validation cases should be
scored on this sensitivity read off real price-move events, not on
price-as-used-input.

Displacement-read reframing (corrects the break-in characterization): the
competitor-displacement read is "why am I NOT occupying competitor Y's customer X"
(winnability / switching-barrier / fit-gap) — NOT "why are customers leaving"
(churn-cause). Different read, possibly cleaner (competitive-positioning)
substrate than the review-only substrate the demotion was scored against; the
displacement method-validation case should be scored on this winnability framing.

Non-claims for this SUGGESTED block: not adjudicated, not frozen, not validation,
not WTP, not readiness, not a change to the locked pricing-first direction;
pending product-lead freeze.

## Non-claims

Not validation, WTP, readiness, buyer-proof, or ICP-proven. Pricing wins by being
LEAST-BLOCKED on the evidence, not by being proven; no buyer has paid Orca. The
two verification runs are corroborated market-context, not buyer validation.
