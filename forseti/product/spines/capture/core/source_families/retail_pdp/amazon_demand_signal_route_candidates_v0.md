# Amazon Demand-Signal Route Candidates + Seller-Surface Posture v0

```yaml
retrieval_header_version: 1
artifact_role: Capture source-family candidate/posture record plus pinned logged-out investigation route
scope: >
  Records the Amazon-side capture candidates for the demand-signal direction
  (bought-in-past-month badge, bestseller rank, price/stockout state,
  cart-quantity inventory-drawdown, vendor fallbacks) and the owner-directed
  posture for Amazon seller-account surfaces: BSA-covered analytics are
  quarantined internal-only; consented SP-API panel data is the sanctioned
  calibration input. Route binding remains a separate capture-lane act.
use_when:
  - Planning or adjudicating Amazon capture routes for demand-signal work.
  - Checking what may and may not touch the sold signal chain from Amazon surfaces.
  - Designing the tracked-SKU capture set for the pilot categories.
  - Reusing the proven logged-out Amazon route for a bounded product investigation.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/product_lead/gtm/forseti_demand_signal_gtm_design_v0.md
  - docs/research/forseti_demand_signal_backtest_probe_findings_v0.md
  - forseti/product/spines/capture/core/contracts/source_access_boundary/data_capture_source_access_boundary_decision_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_sidecar_operator_playbook_v0.md
  - docs/workflows/retail_pdp_amazon_first_silver_lane_handoff_v0.md
stale_if:
  - The capture lane binds, rejects, or supersedes any candidate route below (point here to the binding record).
  - Amazon changes the badge, rank rendering, cart-quantity behavior, or SP-API/BSA terms materially.
  - The GTM micro-panel design is ratified or dropped.
  - PR 865 is superseded, rejected, or changes the anonymous session and per-page confirmation posture.
```

## Status

`CANDIDATES_CAPTURED_PENDING_ADJUDICATION`. Owner-directed capture from the
2026-07-10 demand-signal readout thread. Nothing here is a bound route, live
capture authorization, build authorization, or validation. The quarantine
rule below is operative as a CONSTRAINT (it forbids; it authorizes nothing).
Evidence receipts cited from the probe findings are screening-tier.

## Pinned Logged-Out Investigation Route (2026-07-11)

Status:
PINNED_OPERATOR_POSTURE__SINGLE_URL_IMPLEMENTED__MULTI_URL_RUNTIME_PROOF_ONLY.

For future bounded Amazon product investigations, use the rendered anonymous
browser route in the Retail/PDP sidecar playbook and PR 865. Do not substitute
direct HTTP merely because it returns HTTP 200: prior probes returned the wrong
marketplace/currency or lacked the required US offer and review envelope.

Single-URL route:

1. Use the product-specific Amazon Retail/PDP capture profile.
2. Apply declared US ZIP 10001 through the bounded delivery-location plugin.
3. Let the profile choose domcontentloaded and zero configured settle unless an
   operator has evidence for an explicit override.
4. Accept success only when the page-specific content gate and US storefront
   confirmation both pass.

Multi-URL posture, proven in one bounded runtime probe but not yet a durable
batch interface:

1. Create one anonymous ephemeral browser context.
2. Apply ZIP 10001 once, then reuse only that context's in-memory cookies for
   the bounded URL set.
3. Re-run the correct profile and storefront confirmation independently on
   every page. Cookie presence is never a batch-level success shortcut.
4. Close the context after the batch. Do not write storage state, persist a
   profile, expose cookie values, or introduce credential/session custody.

The runtime proof captured a PDP and grid page after one ZIP setup and passed
both pages' data and pin gates. Its timings and lifecycle evidence are recorded
in PR 865; they are not a claim that a reusable batch runner exists. Exact stock
quantity and exact sold units remained unavailable. Preserve only the observed
availability, rounded bought-in-past-month badge, rank, price, and review facts,
with explicit unknowns or residuals for absent exact values.

## Candidate capture routes (demand-intensity, tracked-SKU set)

| # | Candidate | What it yields | Evidence state (2026-07-10) | Adjudication needed |
| --- | --- | --- | --- | --- |
| R1 | Bought-in-past-month badge, daily | Published purchase-rate state, coarse buckets; bucket-transition dates bracket true monthly rate | VERIFIED server-rendered logged-out ("40K+ bought in past month", archived 2025-06-12 CELH PDP, `loggedIn:false`); exact count NOT client-recoverable (bucketing is server-side; DOM/XHR carry only the display string) | Standard public-capture binding; cadence + SKU set |
| R2 | Bestseller rank (category + subcategory), daily | Precise relative demand velocity | Rendered in every probe-sampled snapshot incl. late-2025 | Same binding as R1 (same page read) |
| R3 | Price / availability / stockout state | Demand-shock context; promo detection | Rendered in all sampled snapshots | Same binding as R1 |
| R4 | Cart-quantity inventory drawdown (the "999 trick") | Near-exact unit sales on suitable listings (single-seller FBA, no max-order-quantity cap), via daily stock deltas with restock-sawtooth differencing | NOT probed; known industry method; current cap prevalence unverified | Separate adjudication: ToS-gray cart interaction; needs a per-SKU suitability probe first; fail-visible rule — capped SKUs record `capped`, never estimated silently |
| R5 | Vendor fallback (Keepa ~EUR 19-29/mo) | Badge/rank history for ASINs Keepa tracked | Vendor-captured, coverage-window-limited; possible review-field cut Apr 2025 (unverified) | License check only; no capture risk |

Review-count velocity is deliberately NOT a candidate here: demoted to
cross-check per the probe findings' signal-role hierarchy (drifting review
propensity; pool-identity instability — see the CROX 38 -> 336,875 re-parent
receipt).

## Owner-directed posture: Amazon seller-account surfaces (2026-07-10)

1. **BSA-covered analytics (Seller Central: Opportunity Explorer and
   similar): QUARANTINED internal-only.** Usable for internal research,
   sanity checks, and cross-validation. Never an input to the sold signal
   chain, directly or via derived calibration. Rationale: Amazon's Business
   Solutions Agreement restricts that data to use in connection with one's
   own selling; alt-data diligence desks look through derived signals and
   treat contract-breaching inputs as contaminating. Severability is the
   accepted answer; a justification narrative is not. Realistic downside of
   internal use is seller-account action by Amazon (knowledge-tier claim);
   counsel pass named for commercialization.
2. **Consented SP-API panel data: the sanctioned calibration input — and
   NOT capture-lane capture.** Amazon's Selling Partner API with per-seller
   authorization grants is the officially provided rail for receiving
   sellers' own data. This is a consented, authorized inbound data feed: it
   does NOT route through the Source Capture Armory / Runner Ladder, uses no
   anti-block rungs, and emits no Source Capture Packets — it is a data
   partnership, not scraping. Only R1-R4 (public/interactive Amazon reads)
   are capture-lane routes; R5 is a vendor licence; the panel is a third
   category (authorized feed) owned by the GTM lane. Panel data enters ONLY
   the calibration layer (never sold, never per-seller exposed). Motion
   design + rationale + input-class rule for the sold chain + calibration
   mechanics are owned by
   `forseti/product/spines/product_lead/gtm/forseti_demand_signal_gtm_design_v0.md`.
   SP-API developer registration and panel recruitment are NOT authorized by
   this capture note.
3. **Sold-chain input classes** (mirror of the GTM rule, for capture-side
   reference): public logged-out capture (documented per-venue) · licensed
   data with verified derive rights · consented panel data · first-party
   data. Everything else stays out of sold reads.

## Sequencing sketch (when capture is commissioned; not authorized here)

1. Bind R1-R3 as one tracked-SKU public-capture route (hero SKUs, pilot
   categories; daily; armory-routed packets).
2. Run the R4 suitability probe (one week, hero ASINs; record
   capped/suitable per SKU) -> adjudicate R4 for survivors only.
3. GTM lane separately advances the SP-API panel (registration, consent
   terms, first members) -> calibration pairs begin accruing; R5 only if a
   coverage gap survives 1-3.

## Non-claims

Not route bindings, not live-capture or build authorization, not SP-API
registration, not validation or readiness, not legal advice, not ECR /
Cleaning / Judgment authority, and not a change to the source-access
boundary decision (which this note operates under, not over).
