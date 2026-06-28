# Fragrance Purchase-Review Widget Expansion Probe v0

```yaml
retrieval_header_version: 1
artifact_role: Capture widget-route probe receipt / fragrance purchase-review lane
scope: Records the bounded review-widget probe over the five locked fragrance purchase-review fixtures, including pagination, rating-filter, media-filter, and source-route findings.
use_when:
  - Deciding whether to use direct review-widget endpoints instead of rendered PDP packets for the five locked fragrance review fixtures.
  - Checking how to get month/rating/media/verified fields for candidate review-row filtering.
  - Diagnosing why review media was not found in the current fixture set.
authority_boundary: retrieval_only; no live capture authorization, crawler, Attachment Record writer, ECR, Cleaning, Judgment, pain/pleasure labeling, integrity scoring, or source-wide completeness claim.
open_next:
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_site_registry_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_capture_pilot_v0.md
stale_if:
  - Any widget endpoint, product id, Shopify shop domain, app key, or response shape changes.
  - A fixture is replaced or a review count changes materially.
  - A row adapter physicalizes widget responses into durable Attachment Records.
  - A later probe finds source-visible review media on these fixtures.
```

## Decision

Use direct review-widget routes for the Judge.me subset of the fragrance purchase-review lane, and keep ZGO on its direct static PDP route for now.

This is the smallest complete MGT/SCI move: it upgrades row access, pagination, rating filters, verified flags, dates, and media diagnostics without creating a standing crawler, durable Attachment Records, source-wide archive, review-integrity scorer, or pain/pleasure labeling lane.

## Widget Route Results

| Source | Widget route result | Fixture coverage result | Media result |
| --- | --- | --- | --- |
| Ministry of Scent | Judge.me endpoint works when keyed to `tigerlily-perfume.myshopify.com`, product id `451146516`. | Confirms 4 total rows; page 2 returns no rows; rating filters work. | `with_pictures` returns 0; no real review media images found. |
| Luckyscent / Scent Bar | Judge.me endpoint works when keyed to `lucky-scent-site.myshopify.com`, product id `8675663642945`; public `www.luckyscent.com` key returned 404. | Page 2 returns the 4 rows missing from the rendered page-1 packet; fixture total is 14. Rating filters work for 2, 3, 4, and 5 star rows. | `with_pictures` returns 0; no source-visible review media for this fixture. |
| Twisted Lily | Judge.me endpoint works for product id `7457873363002`; response shape is widget JSON with `reviews`, not HTML. | Page 2 with `per_page=5` returns the 1 missing row; fixture total is 6. Rating filters work for 3, 4, and 5 star rows. | `with_pictures` returns 0; `photo_gallery` is false; per-review picture/video arrays are empty. |
| ZGO Perfumery | Public Yotpo widget endpoints responded but returned zero reviews and zero bottomline for the observed app key/product ids. | Keep the Direct HTTP static Yotpo PDP section as the only current row-positive route. | Widget API cannot verify media because it returns zero rows; static PDP row has no source-visible review media. |
| Indigo Perfumery | Judge.me endpoint works when keyed to `indigo-perfumery.myshopify.com`, product id `1243179588`; public `indigoperfumery.com` also worked for page 1. | Page 1 returns 10 rows and page 2 returns 3 rows; fixture total is 13. This supersedes the earlier schema-only row-completeness path, while the visible PDP still lacks obvious widget controls. | `with_pictures` returns 0; no real review media images found. |

## Public Judge.me Request Shape

The working endpoint is:

```text
GET https://api.judge.me/reviews/reviews_for_widget
```

Working parameters:

```text
url=<Shopify.shop domain or accepted public domain>
shop_domain=<same domain>
platform=shopify
product_id=<source-visible Shopify product id>
page=<1-based page>
per_page=<widget page size>
sort_by=<optional sort key>
sort_dir=<optional direction>
filter_rating=<optional 1..5 star filter>
```

Observed sort/filter posture:

| Need | Observed parameter |
| --- | --- |
| Most recent window | Default page order, or `sort_by=created_at&sort_dir=desc` where the legacy widget honors it. |
| Lowest rating | `sort_by=rating&sort_dir=asc`. |
| Pictures only | `sort_by=with_pictures`. |
| Pictures first | `sort_by=pictures_first`. |
| Exact rating bucket | `filter_rating=1`, `2`, `3`, `4`, or `5`. |

Month windows are not a server-side widget filter in this probe. Derive
`review_month` mechanically from source-visible review dates after capture.

## Media Diagnosis

The current lack of review media is source data, not only extractor weakness, for the Judge.me fixtures:

- Ministry, Luckyscent, and Indigo returned zero rows for `with_pictures`.
- Twisted Lily returned zero rows for `with_pictures`, `photo_gallery=false`, and empty per-review picture/video arrays.
- ZGO's public Yotpo API returned zero rows despite the PDP static section exposing one row, so the widget API is not a reliable media route for that fixture.
- Product PDP gallery images are not review media and must not satisfy `media_attached_flag`.

## Steps Performed

1. Read the current five-site registry, row contract, and row-capture pilot receipt.
2. Inspected preserved packet DOM/raw bodies for widget vendors, product ids, page controls, sort controls, and Shopify shop domains.
3. Fetched the public Judge.me scripts and derived the actual request shape from `jdgm.shopParams()`, `jdgm.ajaxParamsFor()`, pagination setup, and sort/filter handlers.
4. Ran bounded `curl_cffi` live probes against public Judge.me and Yotpo widget endpoints at human-scale request volume.
5. Saved raw widget responses only under ignored `_test_runs/` paths because they contain review bodies.
6. Parsed body-free summaries for status code, response shape, total count, page count, row count, native review id presence, rating filter behavior, and media indicators.

## Ignored Probe Artifacts

Raw and summary artifacts are local scratch output:

```text
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/widget_probe_20260629/js_probe/js_probe_summary.json
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/widget_probe_20260629/judgeme_param_probe/judgeme_param_probe_summary.json
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/widget_probe_20260629/secondary_fixture_probe/secondary_fixture_probe_summary.json
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/widget_probe_20260629/rating_filter_probe/rating_filter_probe_summary.json
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/widget_probe_20260629/yotpo_deeper_probe/yotpo_deeper_probe_summary.json
```

Do not move the raw `.raw.txt` widget responses into tracked docs.

## Accepted Residuals

- No durable Attachment Records or production row adapter were built.
- No full source-wide review archives were created; counts are fixture-level widget totals observed during this probe.
- No review body text is committed in tracked docs.
- ZGO widget/API mismatch remains unresolved; the static PDP route is the current row-positive route.
- Comment scope, pain/pleasure, integrity, authenticity, and buyer-proof interpretation remain downstream lanes.
- Scent-profile tagging is intentionally not part of the capture row/filter contract unless the source explicitly displays it as source-visible review metadata.
