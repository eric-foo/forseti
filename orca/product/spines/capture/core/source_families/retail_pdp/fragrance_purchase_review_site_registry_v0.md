# Fragrance Purchase-Review Site Registry v0

```yaml
retrieval_header_version: 1
artifact_role: Capture source registry / current operating surface
scope: Current operating registry for the fragrance purchase-review Retail/PDP lane: which row-positive fixtures are in the v0 capture set, which route to use, and which substrate residuals apply.
use_when:
  - Selecting fragrance purchase-review PDP sources for row-level capture.
  - Checking the current route/status for Luckyscent, Twisted Lily, Ministry of Scent, ZGO, or Indigo.
  - Distinguishing the current operating set from the historical recon evidence ledger.
authority_boundary: retrieval_only; no live capture, adapter build, scraping scale, ECR, Cleaning, Judgment, or source-quality scoring authority.
open_next:
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_capture_pilot_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_widget_expansion_probe_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_retailer_recon_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
stale_if:
  - A later probe changes any source route, status, or row-level verdict below.
  - A primary source stops exposing review rows under the pinned route.
  - A fixture re-probe changes any row-positive / row-empty status below.
  - A widget endpoint, product id, Shopify shop domain, app key, or response
    shape changes for any source below.
  - The review-row contract changes the minimum fields needed for v0 capture.
  - The focused review-coverage MGT policy changes source selection, row
    selection, or coverage-receipt expectations.
```

## Decision

Yes: this lane should have a site registry. It should not replace the recon index.

- `capture_recon_index_v0.md` is the evidence ledger: what has been probed, where
  the detailed card lives, and what verdict was reported.
- This registry is the current operating surface: what to use now, what route to
  run, what is excluded from the v0 capture set, and what must be true before a
  source changes status.

This avoids treating a long recon index as a runbook. The registry is the thin
source-of-current-truth; recon remains the proof behind it.

## Current Capture Set

Status: `FRAGRANCE_PURCHASE_REVIEW_FIXTURE_SET_V0_LOCKED_5_SITES`.

Row-level capture fixture set for the first pilot:

1. Ministry of Scent
2. Luckyscent / Scent Bar
3. Twisted Lily
4. ZGO Perfumery
5. Indigo Perfumery

The reason is not brand quality. The reason is row substrate. The first three
sampled sources exposed usable row-level purchase-review bodies on the original
fixtures. ZGO and Indigo needed known-reviewed fixture re-probes. Both now have
row-positive fixtures, with narrower substrate caveats:

- Ministry, Luckyscent, Twisted Lily, and Indigo have direct public Judge.me
  widget routes once keyed to the source-visible Shopify product id and correct
  shop domain. These routes expose native review ids, pagination, rating filters,
  verified flags, dates, and media-filter diagnostics.
- ZGO has a direct public Yotpo v3 storefront route once keyed to the
  source-visible Yotpo app key/guid and Shopify product id. The older Yotpo v1
  widget route remains row-empty for this fixture and is not the operating route.

## Registry

| Source ID | Site | Current status | Route pin | Capture fixture | Row substrate | Use now | Required next fact to change status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `fragrance_retail_ministry_of_scent` | Ministry of Scent | `LOCKED_CAPTURE_FIXTURE_V0_WIDGET_CONFIRMED` | Direct HTTP remains cheapest for the original 4-row packet; Judge.me widget endpoint is available with `shop_domain=tigerlily-perfume.myshopify.com`, `product_id=451146516` for native ids and rating/media filters. | `https://ministryofscent.com/products/memoirs-of-a-trespasser` | Static HTML and Judge.me widget endpoint both expose the same 4 total row bodies; page 2 and `with_pictures` return zero rows. | Use Direct HTTP for cheapest body capture; use widget endpoint when native ids or server-side rating/media filters matter. | Re-probe if Judge.me markup, widget endpoint, Shopify shop domain, or product id changes. |
| `fragrance_retail_luckyscent` | Luckyscent / Scent Bar | `LOCKED_CAPTURE_FIXTURE_V0_WIDGET_EXPANDABLE` | Judge.me widget endpoint with `shop_domain=lucky-scent-site.myshopify.com`, `product_id=8675663642945` is the preferred row-completion route; CloakBrowser render+scroll remains the packeted PDP fallback. | `https://www.luckyscent.com/products/memoirs-of-a-trespasser-by-imaginary-authors` | Rendered page exposed 10 rows; widget page 2 exposed the 4 missing rows for a fixture total of 14. Rating filters work; `with_pictures` returns zero. | Use widget route for complete fixture window, native review ids, rating filters, verified/date fields, and media absence diagnostics. | Re-probe if the widget route returns 404/empty, total count changes unexpectedly, or the rendered PDP diverges from widget totals. |
| `fragrance_retail_twisted_lily` | Twisted Lily | `LOCKED_CAPTURE_FIXTURE_V0_WIDGET_EXPANDABLE` | Judge.me widget endpoint with `product_id=7457873363002` is the preferred row-completion route; response shape is widget JSON with `reviews`. CloakBrowser remains the packeted PDP fallback. | `https://twistedlily.com/products/essential-parfums-discovery-set-1` | Embedded widget JSON exposed 5 rows; widget page 2 exposed the 1 missing row for a fixture total of 6. Rating filters work; `with_pictures` returns zero. | Use widget route for complete fixture window, native review ids, rating filters, verified/date fields, and media absence diagnostics. | Re-probe if the app-block JSON shape, product id, or widget endpoint changes. |
| `fragrance_retail_zgo` | ZGO Perfumery | `LOCKED_CAPTURE_FIXTURE_V0_YOTPO_V3_CONFIRMED` | Yotpo v3 storefront endpoint with `store=LotcNgdZUJLtOh7iQPZPMJPRTLfGpWs2nlS5U8eh` and `product=10788875403567` is the preferred row-completion route; Direct HTTP static PDP section remains fallback. Do not reuse the original zero-count Orpheon fixture for row capture. | `https://zgoperfumery.com/products/d-s-durga-concrete-lightning-eau-de-parfum` | Yotpo v3 exposes 1 total row with native review id, date, verified-buyer flag, rating, body, aggregate 5.0 average, and 5-star distribution. POST filters with `scores` and `pictured` work; `reviewsMedia` total is zero. Older Yotpo v1 widget calls returned zero rows/bottomline. | Use Yotpo v3 for complete fixture window, native review id, date, verified flag, rating/media filters, and media absence diagnostics. Use static PDP only as fallback. | Re-probe if the v3 route returns empty/error, the product id/app key changes, count/body diverges, or the static PDP disagrees with v3 totals. |
| `fragrance_retail_indigo` | Indigo Perfumery | `LOCKED_CAPTURE_FIXTURE_V0_WIDGET_EXPANDABLE` | Judge.me widget endpoint with `shop_domain=indigo-perfumery.myshopify.com`, `product_id=1243179588` is the preferred row-completion route; CloakBrowser schema rows are fallback context. | `https://indigoperfumery.com/products/indigo-perfumery-sampler-set` | The rendered PDP exposed only schema rows in the previous packet, but the direct widget endpoint exposed 13 total rows over two pages. Rating filter confirms all rows are 5-star; `with_pictures` returns zero. | Use widget route for complete fixture window, native review ids, verified/date fields, and media absence diagnostics. Preserve a visible-widget-control residual if citing the PDP DOM. | Re-probe if the widget endpoint disappears, the visible PDP starts exposing row controls, or the total count changes unexpectedly. |

## Promotion Rule

A source enters `LOCKED_CAPTURE_FIXTURE_V0` only when a sampled public PDP
exposes actual review row bodies, not only aggregate counts, review-widget
configuration, CSS, empty containers, or zero-count widget state. The row must
be capturable into `candidate_fragrance_review_row_v0` with raw source anchors
and per-field residuals.

The raw row anchor may be a visible rendered review element, a static review
section, or a PDP-served structured `Review` object. Schema-only rows are usable
only with an explicit visible-row residual; do not silently treat them as visible
customer-review widget rows.

A fixture stays out of the row-capture set when the only preserved evidence is a
PDP shell, review container, aggregate count, widget script/config, or empty/no-
review state. A second product fixture is allowed when there is a new fact that
it is known to have reviews.

## Route Policy

Do not blindly climb every rung on every run. Use the pinned cheapest route that
preserved row bodies for that source, with Direct HTTP as a cheap control where
useful.

Run intermediate rungs again only when the failure signature points to that
hypothesis:

| Symptom | Recheck route |
| --- | --- |
| Static page returns aggregate/config only, but rendered widget likely holds rows | CloakBrowser render+scroll. |
| Direct HTTP fails or changes with UA/header-sensitive behavior | `anti_blocking_http` rung 1. |
| Passive TLS/JA3 fingerprint wall suspected and no JS/render dependency is evident | `curl_cffi` rung 2, once a packeted runner exists or as a clearly marked diagnostic. |
| Rendered route returns shell/no rows | Known-reviewed-SKU re-probe before source-wide NO-GO. |

For this lane, rung 1 and the ad hoc rung 2 diagnostic did not unlock the
original ZGO or Indigo sampled fixtures. Known-reviewed fixture selection was
the correct next move: it promoted both sites to row-positive fixture status
without claiming source-wide completeness. A later ZGO widget-generation probe
then promoted the known-reviewed ZGO fixture from static-only to Yotpo v3
endpoint-backed capture.

## Pilot Unit

The first pilot should capture one row-producing PDP per locked fixture and emit
packet-local candidate rows under
`fragrance_purchase_review_row_contract_v0.md`.

Pilot success is not source-wide coverage. It is only proof that the five-site
fixture set can produce review rows with body text, provenance, product binding,
source-visible metadata, and explicit residuals.

## Non-Claims

- Not a claim that the five fixture-positive sources are the best fragrance
  sources.
- Not a source-wide completeness claim for any retailer.
- Not a durable Attachment Record implementation plan.
- Not ECR, Cleaning, Judgment, pain/pleasure labeling, review integrity scoring,
  or buyer proof.
- Not authorization for scaled scraping, auth bypass, challenge solving, or a
  standing crawler.
