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

Status: current contract, revised 2026-07-21.

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
- `ulta_pdp_aggregate`
- `target_pdp_aggregate`
- `amazon_pdp_aggregate`

Content schema versions are retailer-local revisions, not a shared maturity
scale. Amazon remains explicitly raw-unflipped: its ASIN-bound aggregate PDP is
preserved as raw and enters this same Cleaning/Silver floor through the
read-only historical decoder. That compatibility path is not canonical content,
does not hide route maturity, and does not authorize a separate Amazon lake.
The current canonical-content acquisition census is:

| Profile | Content schema | Parser | Current mark |
| --- | --- | --- | --- |
| `sephora_pdp_aggregate` | `retail_pdp_sephora_aggregate_content_v3` | `retail_pdp_sephora_aggregate_parser_v3` | Current canonical content. |
| `luckyscent_pdp_aggregate` | `retail_pdp_luckyscent_aggregate_content_v1` | `retail_pdp_luckyscent_aggregate_parser_v1` | Current canonical content; `v1` does not mean legacy. |
| `nordstrom_pdp_aggregate` | `retail_pdp_nordstrom_aggregate_content_v2` | `retail_pdp_nordstrom_aggregate_parser_v5` | Current canonical content. |
| `ulta_pdp_aggregate` | `retail_pdp_ulta_aggregate_content_v2` | `retail_pdp_ulta_aggregate_parser_v2` | Current canonical content. |
| `target_pdp_aggregate` | `retail_pdp_target_aggregate_content_v1` | `retail_pdp_target_aggregate_parser_v2` | Current canonical content; `v1` does not mean legacy. |
| `amazon_pdp_aggregate` | `retail_pdp_amazon_aggregate_content_v1` | `retail_pdp_amazon_aggregate_parser_v2` | Current canonical content; schema `v1` does not mean legacy. Parser v2 inventories `celwidget` class lists without rewriting historical parser-v1 packets. Content retention is admitted only at the pre-v3 envelope's single US pin (ZIP `10001`). |

`RETAIL_CAPTURE_PROFILE_SCHEMA_VERSION = 4` versions the shared profile-registry
metadata only; it is not a retailer content version. Renaming a current `v1`
record to `v2` without a real schema or retention change would be a misleading
label and is not allowed.

For Sephora, `sephora_pdp_aggregate` is the sole normal deep-page capture route
for new packets. It defaults to `content` retention and writes
`retail_pdp_sephora_aggregate_content_v3` with
`retail_pdp_sephora_aggregate_parser_v3`. Sampled-raw/full-derived v2 and
Projection-era methods are superseded for new acquisition but remain readable
through legacy compatibility. Explicit `raw` is diagnosis/recovery posture, not
a second normal deep-capture route. Bazaarvoice review and Q&A evidence remains
a separate companion governed by `retailer_information_extraction_standard_v0.md`.

Every other Retail/PDP profile remains raw until separately proven. Admitted
CloakBrowser retailer-grid profiles follow the separate derived-first monitoring
posture in `retailer_information_extraction_standard_v0.md`; Direct-HTTP grids
remain raw.

| Retailer / route | Current deep-PDP mark |
| --- | --- |
| Amazon `amazon_pdp_distribution` | `raw_unflipped`; no content schema exists, and its extra `customers mention` gate is not admitted for information capture. |
| Walmart `walmart_pdp_aggregate` | `raw_unflipped`; the Direct HTTP runner does not yet support content retention. |
| Credo Direct HTTP PDP | `raw_unflipped`; no admitted content profile exists. |
| Kohl's unattended real-Chrome PDP | `raw_unflipped`; no content profile exists and the real-Chrome runner does not yet support content retention. |
| Beauty Pie product route | `unknown_unproven`; no product-level route is admitted. |

The migration goal is to move each proven raw aggregate PDP route to its own
lossless canonical-content contract, not to label every retailer `v2`. A
content-version increment requires a real retailer-local schema or retention
change plus raw-to-content equivalence, explicit loss, fail-loud raw fallback,
and Cleaning/Silver lineage. Grid and distribution profiles are separate
support surfaces, not automatic deep-PDP conversion targets.

Ulta content retains the requested product/SKU, target offer, aggregate rating
and count, the target-bound Apollo product module subtree, and every
source-ordered variant state. The full Apollo/loader envelope is not canonical
content: its supplied-input hash remains in extraction metadata, while
recommendation products and unrelated loader state are not retained. Historical
Ulta raw packets remain readable through the legacy decoder.

Target content is built from the Target-owned `__NEXT_DATA__` CDUI page state
plus the rendered offer and review regions. Server-side rendering hydrates only
the core product datasource; the price, offer, fulfillment, variation, and store
datasources are declared in the layout and left null, so the offer is recovered
from the rendered DOM and the declared-but-unhydrated modules are inventoried
with their hydration state. Review and Q&A bodies stay in the separate
`target_bazaarvoice_onboarding` companion: Target content retains body-free
review identity only, and the Target-native review UUIDs do not join the
companion's Bazaarvoice review IDs. Guest session and bot-defense material
carried in the page state is never retained, and its presence alone is
recorded.

Amazon content is built from the rendered PDP's own `celwidget` feature
modules, each of which Amazon stamps with the page's target ASIN. Price,
availability, ship-from/sold-by, delivery promise, and the bought-in-past-month
badge are read only from modules bound to the requested ASIN; a module carrying
another ASIN, or a page-global merchandising signal that no bound module
carries, fails extraction rather than binding to the target. Amazon declares far
more detail-page modules than the server fills, so all of them are inventoried
with their render and target-binding state in one inventory row. Variants come
from Amazon's own `desktop-twister-sort-filter-data` page state; a twister
module that renders without parsable state fails extraction rather than
reporting variants as observed.

**Amazon content retains the exact review bodies.** This is the one place
Amazon deliberately diverges from Target. Amazon has no separate raw
review-response companion: `amazon_pdp_review_onboarding_v2` writes only a
control manifest and a body-free summary over an already-preserved raw parent,
so the bodies exist solely in the parent PDP DOM that content mode hashes and
discards. Each body is read from the reviewer's own rich-content block, not from
the surrounding accessibility and expander chrome, and every exposed row is
kept, including separately labelled international rows; the eight US rows are
the default US-market analysis window rather than the whole set. That companion
therefore remains valid over raw-retained Amazon parents and is redundant for
content-retained captures. Guest session and anti-CSRF material carried in the
DOM is never retained, and its presence alone is recorded. Amazon exposes
neither retailer AI review sentiment nor customer product Q&A on the admitted
target PDP; a newly exposed AI-summary or Q&A surface without a lossless parser
fails extraction so the runner retains raw inputs and exits nonzero.

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
verified-purchase badge, reposted/syndication label, source-visible reviewed
size/color, and media references.
The record carries an explicit omission/not-exposed ledger for the initial
main-list view, incentive filtering, reviewer demographics, absent review
fields, AI sentiment, product Q&A, merchandising flags, and unfetched media
bytes. A newly exposed incentive, recommendation, unhelpful count, unsupported
reviewed variant, demographic declaration, review-tag, AI-sentiment, or Q&A
surface without a lossless parser fails extraction so the runner retains raw
inputs and exits nonzero.

## Non-claims

This contract is not live capture authority, corpus completeness, price truth,
delivery proof when the destination is unpinned, demand proof, sentiment
judgment, or commercial readiness. It does not authorize generic clicking,
challenge automation, cookie/storage export, or treating screenshots as access
proof.
