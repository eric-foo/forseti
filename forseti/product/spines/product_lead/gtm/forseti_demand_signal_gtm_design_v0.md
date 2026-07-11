# Forseti Demand-Signal GTM Design v0 — Consented SP-API Micro-Panel Motion

```yaml
retrieval_header_version: 1
artifact_role: GTM design capture (owner-directed 2026-07-10; decision-prep pending owner sign-off; not ratified GTM, not an ICP decision)
scope: >
  Captures the consented SP-API micro-panel as the selected calibration +
  go-to-market motion for the demand-signal product direction (institutional
  buyers, earnings-print proving ground), with the detailed rationale the
  owner commissioned, the compliance input-class rule for the sold signal
  chain, the quarantine rule for Amazon seller-account analytics, and the
  owner dispositions on the alternatives (license bootstrap, become-a-seller,
  seller-SaaS panel).
use_when:
  - Designing or reviewing the demand-signal calibration/GTM motion.
  - Checking which data-input classes are allowed in the sold signal chain.
  - Picking up the micro-panel design for formalization or execution planning.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_demand_signal_backtest_probe_findings_v0.md
  - docs/decisions/forseti_product_thesis_consumer_demand_v0.md
  - docs/decisions/forseti_unbackfillable_signal_moat_doctrine_v0.md # nonresolving: on PR #832 until that PR merges; Class A/B/C vocabulary used here
  - forseti/product/spines/creator_signal/aphrodite_research_engine_gtm_design_v0.md
stale_if:
  - The owner signs off and this motion is promoted into a ratified GTM/offer artifact (point here to it).
  - The institutional ICP lean is formalized differently, or the earnings-print proving ground is dropped.
  - Amazon SP-API consent mechanics or data-protection terms change materially.
```

## Status

`GTM_DESIGN_CAPTURED_DEFERRED_FAR_FUTURE`. Owner-directed capture from the
2026-07-10 demand-signal probe readout thread ("micro panel - that's very
interesting. let's put that in the GTM document and explain why in detail").
Enacts nothing: no panel exists, no recruitment is authorized, no SP-API
developer registration has been performed, no build. The institutional-ICP
direction referenced here is an in-thread owner lean the owner explicitly
declined to formalize yet ("we dont formalize it yet"); this document designs
one motion inside that unformalized direction. Claims are
`product_learning`-capped.

**Sequencing (owner, 2026-07-11): the SP-API panel is deferred to the far
future.** Once the developer-registration / app-review / seller-recruitment
weight was clear, the owner deferred it. Consequence — deferring the panel
defers ABSOLUTE-UNIT calibration, not the demand-signal product: the
near-term work (public capture of rank/badge/price per the Amazon
route-candidate note; the retrospective and forward earnings-print backtest)
runs on RELATIVE signals plus Wikipedia pageviews and EDGAR outcomes, none of
which need the panel — this is exactly what the probe scored. If absolute-unit
levels are wanted before the panel exists, the interim option is a paid vendor
licence (Keepa/Cobalt, derive-rights check required), not a reason to pull the
panel forward. The design below is preserved intact for whenever calibration
is picked up.

## What a consented SP-API micro-panel is

Amazon's Selling Partner API (SP-API) is Amazon's official programmatic access
to a seller's OWN account data — orders, units, revenue, inventory, and
traffic reports. Access to another seller's data works only one way: that
seller authorizes a registered developer application (an OAuth-style grant,
revocable by the seller), and the developer operates under Amazon's Data
Protection Policy (registration + data-handling audit).

The micro-panel takes two separate consents, not one (do not conflate them
with being a seller — being a seller only exposes one's OWN data):
1. Amazon approves Forseti as a developer with a registered PUBLIC
   application. Registration path matters: via Seller Central it requires a
   Professional selling account, but via the **Solution Provider Portal** it
   does NOT require any selling account — that portal is the path for a
   data/software provider, so Forseti does not have to become an Amazon
   seller to run the panel.
2. Each of 5–20 pilot-category (beauty, beverage/CPG) sellers separately
   authorizes that public app against their own account via Login with
   Amazon (Amazon's OAuth), revocable anytime — granting Forseti read access
   to their own sales history (SP-API exposes roughly two years back) and
   ongoing sales.
Scope note: the calibration inputs (aggregate units/sales/traffic) sit in
SP-API's normal tier; PII-bearing order reports need a separate restricted-
role approval Forseti deliberately does not need and should not request
(verify exact per-report restricted boundary at build). Their per-seller data is used for exactly one
internal purpose — calibration ground truth: fitting the curves that map the
public signals Forseti captures (bestseller rank, bought-in-past-month badge
buckets, review velocity) to actual unit sales, per category. In exchange,
panel members receive Forseti's calibrated demand reads for their category.
Panel data is never sold, never shown at individual-seller grain, and never
leaves the calibration layer.

"Micro" is load-bearing: the aim is calibration curves for tracked
categories, not marketplace coverage. Twenty consenting sellers in two
categories is sufficient; thousands are not needed.

## Why this motion (the commissioned rationale)

1. **It supplies the one thing public capture cannot: absolute ground
   truth.** Public signals (rank, badge buckets, review velocity) give
   precise RELATIVE demand movement but only bracketed absolute units. A
   small set of real per-SKU sales series per category pins the
   rank-to-units and badge-bucket-to-units curves, converting relative
   signals into calibrated absolute estimates — with our own calibration
   rather than a vendor's black box.
2. **It is the clean replacement for the contract-restricted weak link.**
   Amazon's own Seller Central analytics (e.g., Opportunity Explorer) are
   use-restricted by the Business Solutions Agreement; anything derived from
   them taints the sold chain for a conservative alt-data diligence desk.
   Consented SP-API sharing is Amazon's OWN sanctioned mechanism for exactly
   this data flow — the panel gives equivalent-or-better calibration with a
   provenance chain a compliance desk can approve in one pass.
3. **It makes the sold signal chain DDQ-clean by construction.** With the
   panel in place, every input class in the sold chain is one of: public
   logged-out capture (documented per-venue), licensed data with derive
   rights, consented panel data, or first-party data. That input-class rule
   (below) is the compliance posture institutional buyers diligence for —
   and Forseti's existing provenance architecture (capture packets, per-venue
   route records, evidence drill-back) means the DDQ answer is a product
   feature, not a scramble.
4. **The acquisition cost is reciprocal value, not cash.** Panel members are
   paid in the product itself (category demand reads they cannot get
   elsewhere at their size). This prices the panel at near-zero cash and
   creates the correct incentive: members want the reads to be good.
5. **It doubles as the GTM flywheel.** Panel members are simultaneously
   design partners (they tell us which reads matter), the first reference
   accounts, and the case-study substrate for the institutional pitch ("our
   calibration is consented ground truth from operators in the category" is
   a diligence-friendly sentence). If a brand-side buyer class ever opens,
   the panel is its seed. This mirrors the reciprocal-value shape already
   designed in the Aphrodite research-engine GTM, applied to the
   demand-signal direction.
6. **Exclusivity honesty (moat classification).** Panel data is exclusive by
   CONSENT (contract), not un-backfillable by time: a competitor could in
   principle recruit the same sellers. It is therefore not a Class-A clock —
   but SP-API's ~2-year history window means each joining member backfills
   calibration history immediately (cheap backtest fuel), and panel
   relationships compound socially even though the data class does not. The
   two real clocks (live Class-A capture; the forward track record) remain
   the moat; the panel is calibration + distribution, not moat.

## How the panel calibrates public signals (the mechanism)

The panel exists to answer one question the public signals cannot answer
alone: *how many units is this movement actually worth?* Public capture
(badge buckets, rank, price) is precise about DIRECTION and RELATIVE change
but bracketed about ABSOLUTE units. Panel members' SP-API sales series are
the absolute ground truth that pins the conversion.

The pairing (per panel SKU, per day/week): join Forseti's own publicly
captured signals for that ASIN — bestseller rank, bought-in-past-month
bucket, price, review velocity — to the member's SP-API actual units sold
for the same SKU and window. That yields matched pairs of
(public signal state -> true units), which is exactly the training data the
vendors' consented panels give them and we otherwise lack.

Three calibration outputs from those pairs:

1. **Rank -> units curve, per category.** Bestseller rank maps to unit
   velocity along a category-specific power curve (steeper in fast-moving
   CPG, flatter in apparel). Panel SKUs supply enough (rank, units) points
   per category to fit that curve, so a NON-panel competitor's public rank
   can then be read as an estimated unit rate with a stated error band.
2. **Badge-bucket -> rate bounds.** The bought-in-past-month bucket
   ("10K+", "40K+") is coarse, but panel members whose true monthly units
   fall inside a bucket calibrate what that bucket actually means in units,
   and bucket-transition dates (captured daily) tighten the estimate between
   the bracket edges.
3. **Signal-blend weighting.** With true units in hand, fit how much each
   public signal should count when they disagree (rank moving without badge
   change, price cuts inflating rank, etc.) — turning several noisy proxies
   into one calibrated demand-intensity read per SKU.

Aggregation to the tradeable object: SKU-level calibrated units roll up to
brand-level demand intensity via the entity-resolution layer
(brand -> SKUs -> parent/ticker), which is the input to the earnings-print
prediction. The panel calibrates the SKU rung; entity resolution carries it
to the ticker rung; the Judgment spine turns the calibrated series into the
scored call.

Honest limits (stated, not solved): the fitted curves are only as
representative as the panel is (consenting sellers skew small/cooperative —
a per-category bias note is required when curves are fitted); panel SKUs and
the competitor SKUs being estimated may differ in listing structure; and
calibration drifts as Amazon changes rank/badge behavior, so curves need
periodic refit against fresh panel data. None of this blocks the mechanism;
all of it is disclosed at read time as part of the methodology the buyer
diligences.

## The input-class rule for the sold signal chain

Every input to any sold read must belong to one of these classes, and be
labeled per class in provenance:

1. Public logged-out capture, documented per-venue (badge, rank, price,
   archives, Wikipedia pageviews, EDGAR).
2. Licensed data whose license permits derived-product sale to financial
   buyers (verify the derive-rights clause before contracting).
3. Consented panel data (SP-API grants under Amazon's Data Protection
   Policy), aggregate-calibration use only.
4. First-party data.

**Quarantine rule (owner-directed this thread): Amazon seller-account
analytics (Opportunity Explorer and BSA-covered surfaces) stay internal-only
— research and sanity checks that never enter the sold signal chain. This is
an architecture rule, not an argument: severability is what a diligence desk
accepts, not a justification narrative.** Realistic downside of internal use
is Amazon account action (contract termination), not litigation-scale
exposure at this size — knowledge-tier claim; counsel review is a named open
question at commercialization.

## Alternatives considered (owner dispositions 2026-07-10, in-thread)

| Option | Disposition | Why |
| --- | --- | --- |
| Consented SP-API micro-panel | **Selected for design (this doc)** | Rationale above. |
| License bootstrap (Jungle Scout Cobalt / SmartScout API) | Fallback only; no free path (checked 2026-07-10) | Cobalt is enterprise custom pricing (no free tier; third-party estimates ~$500-700/mo); SmartScout API is Enterprise-only (~$399+/mo custom; $29+/mo standard plans exclude API). Viable paid bootstrap for absolute-level estimates, but vendor-modeled (their calibration, not ours) and requires a derive-rights license check before any financial-buyer product. Keepa (~EUR 19-29/mo) remains the budget option for badge/rank history only. |
| Become a real seller (first-party ground truth) | **Owner-rejected** ("way too much effort") | Coverage too small for the effort; superseded by the panel's consented ground truth. |
| Seller-facing SaaS to grow a large panel | **Owner-rejected** | Multi-year company pivot into the Helium10/Jungle Scout knife fight; off-thesis (moat is judgment + track record, not tool distribution). |

## Design bounds (what the panel is not)

- 5–20 members, pilot categories only; growth is a later owner decision.
- Members share only their own data via Amazon's consent rails; grants are
  revocable; per-member data is never sold, never displayed, never
  benchmarked against a named other member.
- No lead-gen, no outreach lists, no person-level anything (parent-thesis
  boundary unchanged). Panel recruitment, when executed, routes through the
  proper outreach-motion lane with its own discipline — this doc authorizes
  no outreach.
- The panel does not replace public capture; it calibrates it. If the panel
  died tomorrow, the Class-A capture clocks keep running.

## Open questions (named, not resolved)

- Consent/terms drafting for panel members (counsel; includes the
  aggregate-use grant and revocation mechanics).
- SP-API developer registration + Data Protection Policy audit: effort and
  timeline unknown; Amazon vets the public app (non-trivial, not exotic).
  Register via the Solution Provider Portal (no selling account) rather than
  Seller Central (Pro selling account required); confirm the current
  restricted-role boundary so the app requests only the normal-tier
  units/sales/traffic scope.
- Panel-selection bias: consenting sellers skew small/cooperative; per-
  category curve validity needs a bias note when fitted.
- Recruiting motion design (who, in what order, with what pitch) — product-
  lead work when the owner formalizes the direction.
- Counsel pass on the quarantine rule and the derive-rights standard at
  commercialization.

## Non-claims

Not ratified GTM, not an ICP decision, not buyer proof, not
willingness-to-pay evidence, not a panel (none exists), not recruitment or
outreach authorization, not SP-API registration, not build authority, not
legal advice, and not a moat claim for panel data (exclusivity-by-consent is
weaker than the two clocks and is labeled as such above).
