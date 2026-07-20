# Retail/PDP Content and Cleaning Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Retail/PDP capture and Cleaning contract
scope: >
  Retailer-owned content extraction, retention, Cleaning adaptation, source
  binding, residuals, and Silver handoff for rendered Retail/PDP routes.
use_when:
  - Adding or changing a Retail/PDP content-eligible capture profile.
  - Checking retailer target binding, storefront pins, review coverage, or Cleaning/Silver lineage.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/foundation/product_contract/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_storefront_pin_registry_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_silver_producer_contract_v0.md
stale_if:
  - A retailer content schema, extractor, pin, review-coverage rule, Cleaning adapter, or Silver producer changes.
```

Status: current contract, revised 2026-07-20.

## Current boundary

Rendered Retail/PDP capture may retain either raw source evidence or one
retailer-owned canonical `content_record.json`. There is no Retail/PDP capture
Projection packet, sidecar writer, post-hoc Projection runner, admitted sample
mode, or third admitted qualification packet.

For `content` retention, the retailer-owned extractor runs only after access,
profile sufficiency, exact target-product binding, and every required storefront
pin succeed. The runner then hashes and discards declared disposable DOM/text,
while preserving browser metadata, receipt, extraction metadata, and the normal
active-capture screenshot when the route requires one. Any failed gate
preserves all supplied original artifacts and returns its typed nonzero failure.

Ephemeral qualification compares operator scratch DOM/text with a retained
content record. It does not create or admit a packet.

Cleaning validates the retained record, checks retailer/profile/source URL and
pin metadata, and binds every row to the real packet plus an honest JSON pointer.
Historical raw and Projection-era packets remain readable through the isolated
legacy decoder. Retail Silver consumes this Cleaning result and carries source
anchors, not a persisted Projection record.

## Required retailer facts

Each family-owned extractor carries only source-visible target-product facts:

- product identity and requested/selected SKU or variant;
- seller, shipper, price, currency, availability, and delivery/storefront facts
  only when honestly target-bound;
- retailer-specific structured variants and offers;
- rating surfaces, review counts/distributions, review bodies, dates, visible
  engagement, and source order;
- descriptions, classifications, shipping/loyalty/recommendation/FAQ modules
  only when the retailer contract declares them valuable; and
- residuals for disagreements, absent anchors, truncation, or unpinned state.

Recommendation, footer, or unrelated-product facts may not bind to the target.
Compactness never authorizes dropping valuable rows.

## Current content-eligible profiles

- `sephora_pdp_aggregate`
- `luckyscent_pdp_aggregate`
- `nordstrom_pdp_aggregate`

Every other Retail/PDP or grid profile remains raw until separately proven.
Direct-HTTP grids remain raw.

Nordstrom review onboarding captures the complete Most Recent 30-day cohort.
If fewer than 12 reviews fall in that window, it continues in the same source
order to 30 total rows or proven exhaustion, while retaining the separately
visible most-helpful positive/critical pair. Each `Load 6 more reviews`
activation is one six-row append; a 30-row cap inside the recent window is
explicitly truncated.

Nordstrom content v2 retains the exact target-bound
`window.__INITIAL_CONFIG__.productDisplay` product subtree and selected-option
state, not the unrelated shopper/configuration envelope. It also flattens every
source SKU, salability/OOS signal, quantity, price, media reference, claim,
taxonomy field, and source order for direct use. Rendered review rows retain
their complete microdata inventory plus source card id/order, helpful count,
verified-purchase badge, reposted/syndication label, and media references.
The record carries an explicit omission/not-exposed ledger for the initial
main-list view, incentive filtering, reviewer demographics, absent review
fields, AI sentiment, product Q&A, merchandising flags, and unfetched media
bytes. A newly exposed incentive, demographic, AI-sentiment, or Q&A surface
without a lossless parser fails extraction so the runner retains raw inputs and
exits nonzero.

## Non-claims

This contract is not live capture authority, corpus completeness, price truth,
delivery proof when the destination is unpinned, demand proof, sentiment
judgment, or commercial readiness. It does not authorize generic clicking,
challenge automation, cookie/storage export, or treating screenshots as access
proof.
