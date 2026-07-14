# Beauty Decision-Adjudication Product Profile v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact (beauty application profile)
scope: >
  Beauty-specific application of the Forseti decision-adjudication product:
  decision admission, evidence families, Decision Sprint form, proof contract,
  current capability boundary, learning path, and terminal transfer test.
use_when:
  - Applying the controlling Forseti product thesis to beauty.
  - Testing whether a beauty decision belongs in a Decision Sprint.
  - Separating beauty-domain assets from buyer and GTM choices.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_product_thesis_decision_adjudication_v0.md
  - forseti/product/spines/foundation/product_contract/core_spine_v0_product_contract.md
  - forseti/product/satellites/beauty/beauty_venue_card_set_v0.md
  - forseti/product/satellites/beauty/beauty_manufactured_demand_tells_v0.md
  - .agents/workflow-overlay/product-proof.md
stale_if:
  - Beauty is no longer Forseti's first application.
  - GTM selects a first beauty buyer and decision family that requires a narrower product binding.
  - Current implementation or proof evidence changes the capability or non-claim boundary.
```

## Status And Boundary

Status: `FIRST_APPLICATION_BOUND_DECISION_FAMILY_UNSELECTED`.

Beauty is Forseti's first product application. This profile does not select the
first buyer, leading decision family, offer, price, competitor position, market
size, or distribution route. Those are next-lane GTM decisions.

The product is not "beauty research." It is a decision artifact for an
accountable beauty-company owner. Beauty supplies the domain ontology, evidence
world, timing, source behavior, contradiction patterns, and outcome routes. The
Core Spine supplies the decision-adjudication contract.

## Beauty Decision Admission

A beauty decision is admitted only if it meets the controlling thesis's full
admission contract. Non-ranked candidate families include:

| Decision family | Consequential action | Why broad evidence may change it |
| --- | --- | --- |
| Concept or portfolio go/no-go | fund, reformulate, sequence, defer, or kill | unmet-need language, claims/formulation crowding, retailer movement, competitor intent, creator diffusion, and regulatory constraints can disagree |
| Positioning, messaging, or claims | choose the promise, proof burden, audience, and claim boundary | consumer language, reviews, specialist communities, competitor claims, ingredient evidence, advertising, and enforcement history expose different risks |
| Channel or retail entry | enter, sequence, limit, negotiate, or avoid a channel | assortment, placement, price/promotion, availability, reviews, retailer strategy, brand readiness, and competitor motion resolve on different clocks |
| Launch intervention | continue, reallocate, reposition, replenish, narrow, or stop | early retail, creator, search, review, inventory, promotion, competitor, and organizational evidence can separate a fixable launch from noise |
| Competitive response | ignore, monitor, defend, counter-position, accelerate, or retreat | product-page changes, hiring, trademarks, claims, distribution, ads, creator activity, and consumer response reveal both action and intent |
| Price or promotion | hold, test, raise, lower, bundle, or sequence | price ladders, promotion depth, availability, reviews, resale, competitor behavior, and brand-position evidence expose demand-versus-position tradeoffs |
| Creator or marketing allocation | select, cap, reallocate, sequence, or stop | sponsorship, content fit, audience response, comment quality, diffusion, affiliate behavior, and downstream retail/search response can contradict headline reach |
| Reputation, safety, or claims response | investigate, communicate, amend, withdraw, or defend | complaints, specialist discussion, regulator actions, litigation, product changes, creator response, and retailer actions determine the defensible action ceiling |

This table is a product-admission universe, not a priority order. A decision that
depends decisively on representative transactions, internal margin, inventory,
or another unavailable privileged input must use
`ADMIT_WITH_AUTHORIZED_PRIVATE_CONTEXT` or `HOLD_DECISIVE_INPUT_MISSING`.

## Beauty Evidence Model

The initial external baseline may combine:

- retailer assortment, placement, price, promotion, availability, review,
  rating, inventory-proxy, and product-page change history;
- consumer reviews, specialist communities, forums, Reddit, and other
  buyer-language venues;
- creator content, sponsorship disclosure, comments, audience response,
  affiliate behavior, and diffusion patterns;
- search behavior, answer-engine visibility, and changing questions;
- brand sites, claims, ingredients, formulations, launches, discontinuations,
  messaging, and archives;
- advertising, creative, affiliate, and promotional behavior;
- hiring, applicant-tracking systems, leadership, team shape, and organizational
  priority changes;
- trademarks, patents, regulatory actions, litigation, corporate filings, and
  investor communications;
- distributor, retailer, supplier, manufacturing, channel, marketplace, resale,
  pricing, and availability evidence;
- purchased/entitled sources and authorized customer context when decision-relevant.

Triangulation is material when evidence from a differently positioned direction
changes a claim, reveals dependence or strategic bias, distinguishes attention
from behavior, separates consumer pull from distribution, or changes the action
ceiling. Source count is not a quality metric.

Representative transaction data is decision-specific. It may be decisive for
inventory depth, precise forecasting, or transfer across channels; it may only
tighten confidence for positioning, competitor-intent, claims-risk, or early
warning. The Sprint must state which is true. Marketplace or Amazon evidence is
one venue family, not the product center.

## Current Beauty Assets And Ownership

Reusable now:

- the beauty venue card set and manufactured-demand tell set;
- beauty and fragrance ontology assets, entities, relationships, and venue
  knowledge where their current source contracts permit reuse;
- historical beauty cases and cutoff discipline as candidate product-learning
  material, subject to zero-spoiler and case-admission gates;
- current research-engine, Capture, ECR, bounded Cleaning, evidence-unit,
  decision-frame, and manual Judgment disciplines;
- Aphrodite creator evidence when authorized and decision-relevant.

Ownership does not collapse:

- Capture owns source retrieval and preservation claims;
- Silver is the trustworthy read layer and may expose bounded coverage receipts;
- ECR and Cleaning own their respective structuring and reconciliation contracts;
- Aphrodite owns creator-signal product logic and Studio remains independent;
- Forseti owns the cross-evidence decision adjudication and buyer-facing action.

Forseti may consume Aphrodite information in the ultimate product. It may not
silently claim Aphrodite's evidence, clients, validation, or distribution as
Forseti-owned proof.

## Initial Beauty Product Form

The initial form is one beauty **Decision Sprint**, admitted and bounded by one
Decision Frame. The buyer receives:

- the exact decision, options, deadline, constraints, and private-context
  boundary;
- a decision-relevant evidence-world map with captured, missing, dependent,
  contradictory, and excluded evidence made visible;
- a recommendation at the strongest defensible action ceiling;
- alternatives, counter-case, uncertainty, and reversal conditions;
- an evidence appendix and decision trace;
- a reveal/outcome plan.

The next action follows from the memo; the product is not complete when it only
describes the market. Generic AI, social-listening tools, dashboards, agencies,
and research providers may retrieve or summarize pieces. Forseti's hypothesized
increment is the bounded, inspectable reconciliation of differently positioned
evidence into an accountable action and hold state. That increment remains to
be proven with buyers.

Minimum private context is `none` for
`ADMIT_PUBLIC_OR_PURCHASED`; a narrow constraint set for
`ADMIT_WITH_AUTHORIZED_PRIVATE_CONTEXT`; and unavailable/unknown for a held
decision. A company-data integration is not required to demonstrate the
external baseline.

## Proving Ground

The proving ground must test the same beauty decision family the eventual paid
Sprint serves. Until GTM selects that family, this profile binds the method but
does not nominate a case.

Minimum protocol:

1. predeclare the beauty Decision Frame, decision owner proxy, evidence cutoff,
   action vocabulary, and decisive unknowns;
2. reconstruct only evidence available before cutoff;
3. produce and seal the full Sprint artifact without post-cutoff spoilers;
4. reveal the company's action and observable outcome evidence;
5. compare recommendation, action sizing, reasoning, misses, and unavailable
   private constraints;
6. state what live-buyer transfer remains unproven.

Earliest product kill: no beauty decision family can show a useful external
baseline, faithful same-decision proof, repeated workflow, and a plausible path
to observable buyer action without decisive unavailable private ground truth.

Historical launch lists, forecasts, or outcome databases do not clear this
gate. A case earns learning only when its pre-cutoff evidence, decision trace,
private-context boundary, and later reveal are honestly separated.

## Learning And Product Evolution

Manual learning needed now:

- which evidence changes each admitted beauty decision rather than merely
  enriching a report;
- where domain expertise changes entity resolution, interpretation, and action;
- which work repeats and which remains bespoke;
- what decision owners treat as inspectable and decision-useful;
- which reveals resolve quickly enough to support learning.

Later proprietary inputs may add internal sell-through, margin, inventory,
consumer cohorts, CRM, channel terms, intended action, overrides, and outcomes.
They should narrow uncertainty or reveal missing context; they do not replace
the external baseline. Contractual retention of derived learning must be
explicit.

Later Cleaning maturity should lower analyst labor and improve longitudinal
entity resolution, deduplication, normalization, contradiction handling,
independence-versus-amplification treatment, and reproducibility. Later
Judgment maturity should reuse decision traces and outcomes to improve analogous
case retrieval, signal reliability, action ceilings, calibration, and
throughput. Neither is proven superior today.

The beauty Decision Desk is earned only after repeated Decisions Sprints expose
a stable decision workflow and longitudinal monitoring targets. Production-
scale broad monitoring is a destination capability, not a prerequisite for the
first Sprint.

## Terminal Transfer Test

Beauty can bridge to a larger consumer-demand company only if the next category
reuses a meaningful bundle of:

- entity and relationship schemas;
- longitudinal source-history and evidence-state structures;
- reconciliation and independence logic;
- decision-frame, action-ceiling, and reveal workflow;
- decision traces and outcome-linked lessons;
- buyer relationships or distribution.

The fact that another category also has products, creators, reviews, retailers,
or launches is insufficient. If the transferable bundle is thin, Forseti has a
beauty business, not yet a horizontal consumer-demand platform.

## Explicit Non-Claims

This profile does not claim:

- a selected beauty buyer, leading decision, offer, price, TAM, SAM, SOM,
  competitor position, or distribution route;
- retailer-side assortment, inventory, launch intervention, or any other
  candidate is rejected or preferred;
- public or purchased evidence is sufficient for every admitted decision;
- current universal source completeness or production-scale monitoring;
- mature Cleaning, autonomous Judgment, calibrated superiority, forecasting
  superiority, or buyer proof;
- transaction, Amazon, launch-history, private-data, creator-signal, or
  dashboard centrality;
- implementation, source acquisition, outreach, publishing, or Studio authority.
