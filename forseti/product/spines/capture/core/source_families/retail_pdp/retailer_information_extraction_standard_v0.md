# Retailer PDP Information-Extraction Standard v0

```yaml
retrieval_header_version: 1
artifact_role: Retail/PDP onboarding information-extraction standard
scope: >
  Defines the evidence categories, discovery behavior, preservation contract,
  and source-specific profile needed to onboard a retailer PDP for broad
  information extraction. Sephora is the first reference profile.
use_when:
  - Reconnoitring a new retailer PDP before writing its extractor or Cleaning adapter.
  - Deciding whether a retailer onboarding capture inventoried the valuable
    source-visible product, variant, review, sentiment, and Q&A evidence.
  - Comparing raw retailer evidence with retained content, an in-packet summary, or Cleaning adaptation.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_content_cleaning_contract_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_storefront_pin_registry_v0.md
  - docs/research/forseti_beauty_retailer_surface_probe_results_v0.md
```

## Bound outcome

A retailer onboarding is complete only when it has attempted every evidence
category below, recorded what the source actually exposed, preserved the exact
raw substrate required by the route, and compared the raw field inventory with
the retained content or in-packet summary and its Cleaning handoff. The
standard is an attempt-and-evidence contract, not a claim that every retailer
exposes Sephora's controls.

Each category gets one status:

- `observed`: source evidence and its locator are preserved;
- `not_exposed`: the bounded discovery procedure found no source control or
  field;
- `blocked`: access, continuation, or parsing failed and the failure evidence
  is preserved;
- `not_applicable`: the source clearly does not offer that feature.

Absence is never encoded as zero, `false`, or an empty list unless the source
explicitly supplied that value. A retailer profile records exact source labels,
parameters, selectors, and continuation behavior; the shared standard does not
pretend those mechanics are portable.

## Information inventory

| Evidence category | Valuable fields to seek and preserve |
| --- | --- |
| Target identity | Requested, final, canonical, product, style, group, SKU and variant identifiers; retailer; brand; title; category and breadcrumb path. |
| Storefront state | Country, locale, currency, seller, shopper context, delivery destination, membership/login state, and every independent pin or residual required by the storefront registry. |
| Variants | Every source variant in source order; name, swatch, size, pack, SKU, price, compare-at price, availability, out-of-stock, limited edition, limited-time offer, new, back-in-stock treatment, selected/default state, images, and variant-specific claims or ingredients. |
| Offer and fulfillment | Price, currency, promotion, inventory/availability label, seller, pickup, shipping, delivery promise, subscription, gift and loyalty treatments. Displayed destination is not delivery proof. |
| Product content | Description, claims, directions, ingredients, warnings, specifications, badges, certifications, merchandising labels, bundles, related content, and source section labels. |
| Media | Every product and variant image/video reference, alt text, ordering, colour/variant binding, and media-fetch status. |
| Review aggregate | Rating value/scale, exact review count, histogram, recommendation percentage, source rounding, and structured-vs-rendered disagreements. |
| Review rows | Source order/rank, review id, title, body, rating, source date, author, declared demographics, verified status, recommendation, helpful/unhelpful counts, variant, incentive/disclosure state, syndication, badges, media, tags, and the complete raw field-name inventory. |
| AI review sentiment | Summary prose and disclosure as context; every positive/green and negative/red chip as a primary fact with exact polarity, label, and displayed count. Same-label polarity collisions remain separate facts. |
| Q&A | Aggregate question count, selected sort, question id/body/date/author, declared answer count, included answer bodies, answer metadata, continuation state, and every declared-vs-included difference. |
| Source mechanics | Visible sort/filter labels, selected-state evidence, displayed ranges/counts, continuation control semantics, first-party request parameters, response totals, source timestamps, and access failures. |

Unknown fields discovered in raw source are not silently ignored. Add them to
the retailer profile or name them in the loss ledger as raw-preserved but not
summarized or retained in canonical content.

## Behavioral discovery procedure

1. Start from the exact commissioned PDP and a confirmed storefront posture.
   Preserve the initial rendered/structured source before changing controls.
2. Inventory the entire target product/variant subtree and every visible
   section, sort, filter, tab, accordion, badge, chip, and continuation control.
   Do not begin from the existing summary, content record, or Cleaning row list.
3. Change one source control at a time. Preserve the exact source label,
   selected-state evidence, displayed range/count, and resulting row order.
   A requested parameter without source-state or response evidence is intent,
   not proof.
4. Exercise continuation until the bound evidence condition is met or the
   source exhausts/blocks. Record every activation/request, offset/cursor, rows
   added, duplicates, oldest/newest source date, non-progress, toggle behavior,
   and exhaustion signal. A fixed click count is never coverage evidence.
5. When a rendered control is defective or insufficient, inspect only the
   first-party configuration and requests declared by the page. A structured
   companion may preserve the missing evidence, but it must also preserve the
   rendered failure and may not claim UI success.
6. Compare rendered, embedded, and structured values field by field. Preserve
   every disagreement with both values and exact source anchors; never silently
   choose the more convenient value.
7. Inventory all raw top-level and row-level field names before summarization
   or canonical-content retention.
   Classify every omitted valuable field in the loss ledger and rerun the
   raw-to-retained comparison after repair.

The behavioral procedure discovers source-specific mechanics. It is not
generic cross-site clicking, permission for broad crawling, or authorization
to bypass access controls.

## Review onboarding depth

The unfiltered initial review view is retained once so the source's incentive
mix and default posture remain observable. All analytical review views then
apply the retailer's exact non-incentivized filter when it exists:

1. Preserve a source-labelled `Most Helpful` snapshot with selected sort/filter
   evidence and every available review-row field in the inventory above.
2. Preserve a source-labelled newest/`Most Recent` response with the
   non-incentivized filter. This response establishes the monitoring anchor.
   Continue to a 30-day cohort only when that deeper corpus window is
   commissioned; a bounded onboarding response must otherwise remain labelled
   as bounded rather than complete.
3. Inventory the live rendered demographic vocabulary rather than promoting a
   generic embedded configuration. Preserve each exact label, request value,
   count, denominator, share of declared-demographic subset, coverage of all
   non-incentivized reviews, and every rendered/structured mismatch.
4. Keep the unfiltered baseline separate from filtered analytical cohorts.
   Never describe either bounded cohort as the complete review corpus or a
   representative sentiment sample.

## Q&A onboarding depth

Attempt the source-labelled answer-rich ordering (`Most Answers` or the exact
retailer equivalent) and expand until the commissioned bound, source
exhaustion, or a preserved failure. Keep aggregate questions, captured question
rows, per-question declared answer counts, included answer bodies, and their
differences separate. An include block is not a complete answer corpus merely
because it contains many rows.

## Preservation and adaptation acceptance

Every onboarding packet requires:

- exact raw bytes for every consumed source and continuation page, with hashes;
- a secret-safe request/control manifest and parent packet identity;
- content qualification over the exact preserved bytes or operator scratch
  inputs used by the route;
- raw-to-summary or scratch-to-content row accounting for counts, identifiers,
  source order, body presence, aggregates, and filtered/demographic counts;
- compact summaries that carry identifiers, counts, dates, and raw-file
  references without duplicating review, question, or answer bodies already
  preserved in the exact raw response;
- an explicit loss ledger covering bounded windows, missing nested rows,
  absent demographics, unknown raw fields, disagreements, and access limits;
- a raw failure fallback that commits all bytes acquired before acquisition,
  summary adaptation, or content qualification failure and exits nonzero;
- append-only retention: legacy and failed raw packets are never retroactively
  deleted or rewritten.

Legacy sampled-raw packets may describe the same historical evidence as
`parser-fit` or `projection equivalence`. Current Retail/PDP content routes do
not create a Projection packet: canonical content is retained at capture,
in-packet summaries stay capture evidence, and Cleaning owns downstream
adaptation. The Sephora brand-grid route is a narrow exception: it writes a
separate mechanical parent-product projection from the preserved raw packet,
certified `view_only; not_cleaned; not_normalized; not_judgment_ready`. That
grid projection is not PDP content, Cleaning, or Silver.

Success means the declared capture bound is proven. It does not mean source
completeness, demographic representativeness, ranking-algorithm validation,
Cleaning, Judgment, buyer proof, or monitoring readiness.

## Sephora reference profile

Reference PDP:
`https://www.sephora.com/product/lip-sleeping-mask-P420652?country_switch=us&lang=en`.

Sephora's current proven mechanics are a source-specific benchmark:

| Area | Reference behavior |
| --- | --- |
| Canonical deep-page capture | Every new Sephora deep-page capture uses `sephora_pdp_aggregate` with `content` retention; omitting `--retention-mode` defaults this profile to `content`. The retained record is `retail_pdp_sephora_aggregate_content_v3`, produced by `retail_pdp_sephora_aggregate_parser_v3`. This supersedes sampled-raw/full-derived v2 and Projection-era methods for new acquisition. Existing older packets remain append-only, readable historical evidence and are not rewritten. Explicit `raw` is diagnostic/recovery-only; a failed access, pin, sufficiency, target-binding, or extraction gate preserves acquired raw inputs and exits nonzero. |
| Product/variants | The complete `linkStore.page.product` subtree is the broad structured inventory. Preserve every `regularChildSkus` row and exact `isOutOfStock`, `isLimitedEdition`, `isLimitedTimeOffer`, `isNew`, and back-in-stock fields. The content record may store fields once across canonical rows plus `additional_source_fields` only when the extractor proves that those rows reconstruct the complete subtree exactly; unknown root fields must therefore remain captured rather than vanish on a page change. |
| AI sentiment | Green and red chips are primary facts; polarity, exact label, and count are separate. The verified sample included positive `Softness`, `Scent`, and `Texture`, plus negative `Irritation` and `Scent`. |
| Helpful reviews | On onboarding, preserve one `Most Helpful` response with `Non-Incentivized Reviews Only`, `TotalPositiveFeedbackCount:desc`, review bodies, and supported filtered review statistics. Preserve exact response order without claiming Sephora's proprietary ranking algorithm. |
| Recent reviews | On onboarding, preserve one `Most Recent` response with `Non-Incentivized Reviews Only` and `SubmissionTime:desc`; a passively observed page-load response may satisfy this role only when its exact bytes are archived and qualified. It establishes the last-seen review ID for monitoring and is not a 30-day corpus claim. |
| Reviewer demographics | Promote the live age, skin-type, and skin-concern distributions. The live age labels are exactly `20s`, `30s`, `40s`, and `50s +`; their observed Bazaarvoice values are `20s`, `30s`, `40s`, and `50s`. Retain other returned distributions and statistics in the raw response without promoting them into the compact summary. These self-reported rows form an analytically useful observed subset, not the full reviewer population or a representative census. |
| Q&A | On onboarding, preserve one `Most Answers` response using `TotalAnswerCount:desc`, including returned answer bodies, within the commissioned limit. It is a bounded answer-rich window, not the complete Q&A corpus. |
| Monitoring | Request `Most Recent` only. Stop as soon as the prior last-seen review ID is found; follow source offsets only when the first response does not contain it. Do not routinely refresh `Most Helpful` or Q&A. |
| Companion role | The accepted low-footprint target has three response roles: Helpful plus statistics, Recent, and Q&A. Exact bodies remain in raw responses; the summary carries compact facts and raw-file references. The current `sephora_bazaarvoice_onboarding_summary_v3` runner predates this target and remains append-only historical evidence until a later implementation proves the new route. |
| Brand grid | `sephora_grid_aggregate` preserves the rendered raw packet and mechanically projects one row per unique parent product from retailer-owned `linkStore.page.nthBrand.products`. Every serialized placement retains its source-order position and JSON-pointer anchor. Admission reconciles the page-declared result count, serialized placements, unique parent count, subject slug/target binding, and termination; mismatches remain explicit and exit nonzero. The grid market assertion is page-kind-specific and requires `Sephora.renderQueryParams.country=US`, the country-routing dialog absent, and an explicit selected `USD` currency code in retailer-owned grid state. A dollar glyph never supplies that code. |

The main Sephora deep-capture package is the canonical v3 page capture plus the
separate Bazaarvoice companion roles when the commissioned bound requires them:
Helpful plus statistics, Recent, and Q&A for onboarding; Recent only for routine
monitoring. The page record does not replace or supersede those review and Q&A
responses.

The Sephora profile is a quality bar for search depth and loss visibility. It
is not a template that licenses invented fields on another retailer. The
packet-backed evidence, unarchived observation boundary, storage measurements,
and cross-retailer compatibility findings behind this target are recorded in
`docs/research/forseti_beauty_retailer_surface_probe_results_v0.md`. The first
Summer Fridays grid-route proof is recorded in
`docs/research/forseti_sephora_brand_grid_capture_live_proof_v0.md`; its
34-of-34 projection reconciled, but its US/USD assertion failed closed because
the grid exposed no explicit currency code.

## Nordstrom reference profile

Reference PDP:
`https://www.nordstrom.com/s/the-lip-balm/8260802`.

Nordstrom applies the shared standard through its own source vocabulary:

| Area | Reference behavior |
| --- | --- |
| Product/variants | Retain only the target-bound `window.__INITIAL_CONFIG__.productDisplay` product subtree and selected options, then flatten every core product, core choice, item, SKU, UPC, size, skin type, price, salability, exact quantity, sellable/previewable/sold-out list, and source order. Never copy unrelated shopper configuration. |
| OOS and merchandising | Treat explicit salability, `isAvailable`, and sold-out SKU lists as OOS evidence. Preserve `isFinalSale` and source enticements. If limited-edition, limited-time-offer, new, or back-in-stock fields are absent, record `not_exposed`; do not infer them from recommendations or marketing copy. |
| Media and product content | Retain every ordered/editorial media reference with its metadata and variant binding, plus exact claims, ingredients, taxonomy, certifications, services, and product-state raw field paths. Record that linked binary bytes were not independently fetched. |
| Review provider | Bazaarvoice is Nordstrom's declared ratings/reviews and syndication network. Nordstrom renders the captured reviews through retailer-owned HTML and schema, so provider identification is source context rather than proof that a literal Bazaarvoice widget marker will appear in every raw DOM. |
| Helpful reviews | Retain Nordstrom's persistent source-labelled most-helpful positive and critical cards, including body, rating, date, author, helpful count, verified-purchase status, reposted/syndication label, and any source-visible reviewed size/color. This is a two-card snapshot, not proof of the retailer's ranking algorithm. |
| Recent reviews | Select `Most Recent`; retain the complete inclusive 30-day cohort. If it has fewer than 12 rows, continue in the same source order to 30 rows or proven exhaustion. Preserve each six-row continuation count and label the fallback cohort as historical context rather than recent reviews. |
| Review filters/demographics | Preserve the unfiltered rendered evidence. The verified reference exposes a Verified Purchases control but no non-incentivized filter and no reviewer-age vocabulary, so reviews are not claimed as non-incentivized and no demographic distribution is invented. A newly exposed incentive, recommendation, unhelpful count, unsupported reviewed variant, demographic declaration, or review-tag surface without a lossless parser forces raw fallback. |
| AI sentiment and Q&A | The verified reference exposes neither retailer AI sentiment nor product Q&A. Record both as `not_exposed_on_target_pdp`; generic footer FAQs, assistant text, and unrelated recommendations are not product Q&A. Newly exposed target surfaces without a lossless parser force raw fallback. |
| Adaptation | Current content v2 flows directly into Cleaning. Acceptance is exact content-to-Cleaning row-id/residual accounting; no current Projection packet or retroactive mutation of historical sample/raw packets is permitted. |

This profile demonstrates cross-retailer behavioral discovery: inspect
page-declared state and controls first, preserve the retailer's exact
vocabulary, fail closed on newly exposed unsupported surfaces, and use the
shared field classes without forcing Sephora-specific mechanics onto
Nordstrom.
