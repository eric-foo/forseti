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
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_site_registry_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_capture_pilot_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md
stale_if:
  - Any widget endpoint, product id, Shopify shop domain, app key, or response shape changes.
  - A fixture is replaced or a review count changes materially.
  - A row adapter physicalizes widget responses into durable Attachment Records.
  - A later probe finds source-visible review media on these fixtures.
  - The focused review-coverage MGT policy changes row-selection or receipt
    expectations for this lane.
```

## Decision

Use direct review-widget routes for all five locked fragrance purchase-review fixtures: Judge.me for Ministry, Luckyscent, Twisted Lily, and Indigo; Yotpo v3 storefront for ZGO.

This is the smallest complete MGT/SCI move: it upgrades row access, pagination, rating filters, verified flags, dates, and media diagnostics without creating a standing crawler, durable Attachment Records, source-wide archive, review-integrity scorer, or pain/pleasure labeling lane.

## Widget Route Results

| Source | Widget route result | Fixture coverage result | Media result |
| --- | --- | --- | --- |
| Ministry of Scent | Judge.me endpoint works when keyed to `tigerlily-perfume.myshopify.com`, product id `451146516`. | Confirms 4 total rows; page 2 returns no rows; rating filters work. | `with_pictures` returns 0; no real review media images found. |
| Luckyscent / Scent Bar | Judge.me endpoint works when keyed to `lucky-scent-site.myshopify.com`, product id `8675663642945`; public `www.luckyscent.com` key returned 404. | Page 2 returns the 4 rows missing from the rendered page-1 packet; fixture total is 14. Rating filters work for 2, 3, 4, and 5 star rows. | `with_pictures` returns 0; no source-visible review media for this fixture. |
| Twisted Lily | Judge.me endpoint works for product id `7457873363002`; response shape is widget JSON with `reviews`, not HTML. | Page 2 with `per_page=5` returns the 1 missing row; fixture total is 6. Rating filters work for 3, 4, and 5 star rows. | `with_pictures` returns 0; `photo_gallery` is false; per-review picture/video arrays are empty. |
| ZGO Perfumery | Yotpo v3 storefront endpoint works when `store` is the source-visible Yotpo app key/guid `LotcNgdZUJLtOh7iQPZPMJPRTLfGpWs2nlS5U8eh` and `product` is the Shopify product id `10788875403567`. Older Yotpo v1 widget endpoints remain row-empty for this fixture. | Confirms 1 total row, native review id, source date, verified-buyer flag, 5-star distribution, and 5.0 average rating. Rating/media filters work via POST body, not GET query params. | Review row has empty image/video arrays; `reviewsMedia` total is 0. |
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

## Public Yotpo v3 Request Shape

The working ZGO endpoint is:

```text
GET https://api-cdn.yotpo.com/v3/storefront/store/<YOTPO_GUID>/product/<SHOPIFY_PRODUCT_ID>/reviews?page=1&perPage=10
```

For the locked ZGO fixture:

```text
YOTPO_GUID=LotcNgdZUJLtOh7iQPZPMJPRTLfGpWs2nlS5U8eh
SHOPIFY_PRODUCT_ID=10788875403567
```

Companion endpoints:

```text
GET https://api-cdn.yotpo.com/v3/storefront/store/<YOTPO_GUID>/product/<SHOPIFY_PRODUCT_ID>/ratings
GET https://api-cdn.yotpo.com/v3/storefront/stores/<YOTPO_GUID>/products/<SHOPIFY_PRODUCT_ID>/reviewsMedia?page=1&perPage=10
```

Server-side review filters use POST to the same reviews path with a JSON body:

```json
{"scores":[5]}
{"scores":[1]}
{"pictured":true}
```

Observed ZGO fixture validation:

| Field | Observed |
| --- | --- |
| `pagination.total` | `1` |
| `bottomline.totalReview` / `averageScore` | `1` / `5.0` |
| native review id | Present |
| review created field | Present as datetime |
| verified buyer | `true` |
| review body word count | `99` |
| score distribution | 5-star: 1; 1/2/3/4-star: 0 |
| review media | image count 0, video count 0, `reviewsMedia.total=0` |

Do not use the older Yotpo v1 route for ZGO row completion:

```text
GET https://api-cdn.yotpo.com/v1/widget/<YOTPO_GUID>/products/<PRODUCT_ID>/reviews.json
```

That route recognized the product mapping but returned zero reviews/bottomline for the observed fixture.

## Media Diagnosis

The current lack of review media is source data, not only extractor weakness, for the locked fixtures:

- Ministry, Luckyscent, and Indigo returned zero rows for `with_pictures`.
- Twisted Lily returned zero rows for `with_pictures`, `photo_gallery=false`, and empty per-review picture/video arrays.
- ZGO Yotpo v3 returned one review row with empty image/video arrays, and the `reviewsMedia` endpoint returned total 0. The older v1 widget endpoint is not a reliable media or row route for this fixture.
- Product PDP gallery images are not review media and must not satisfy `media_attached_flag`.

## Steps Performed

1. Read the current five-site registry, row contract, and row-capture pilot receipt.
2. Inspected preserved packet DOM/raw bodies for widget vendors, product ids, page controls, sort controls, and Shopify shop domains.
3. Fetched the public Judge.me scripts and derived the actual request shape from `jdgm.shopParams()`, `jdgm.ajaxParamsFor()`, pagination setup, and sort/filter handlers.
4. Ran bounded `curl_cffi` live probes against public Judge.me and Yotpo widget endpoints at human-scale request volume.
5. After ZGO v1 Yotpo routes returned zero rows, fetched the Yotpo loader/runtime assets and derived the current v3 storefront endpoint shape.
6. Validated ZGO v3 product reviews, ratings, media, and POST filter bodies with body-free summaries.
7. Saved raw widget responses only under ignored `_test_runs/` paths because they contain review bodies.
8. Parsed body-free summaries for status code, response shape, total count, page count, row count, native review id presence, rating filter behavior, verified fields, date fields, and media indicators.

## Ignored Probe Artifacts

Raw and summary artifacts are local scratch output:

```text
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/widget_probe_20260629/js_probe/js_probe_summary.json
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/widget_probe_20260629/judgeme_param_probe/judgeme_param_probe_summary.json
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/widget_probe_20260629/secondary_fixture_probe/secondary_fixture_probe_summary.json
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/widget_probe_20260629/rating_filter_probe/rating_filter_probe_summary.json
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/widget_probe_20260629/yotpo_deeper_probe/yotpo_deeper_probe_summary.json
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/zgo_completion_probe_20260629/zgo_pdp_metadata_summary.json
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/zgo_completion_probe_20260629/zgo_yotpo_asset_endpoint_summary.json
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/zgo_completion_probe_20260629/v3_endpoint_probe/zgo_v3_endpoint_probe_summary.json
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/zgo_completion_probe_20260629/v3_validation_probe/zgo_v3_validation_probe_summary.json
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/zgo_completion_probe_20260629/v3_filter_post_probe/zgo_v3_filter_post_probe_summary.json
```

Do not move the raw `.raw.txt` widget responses into tracked docs.

## Accepted Residuals

- No durable Attachment Records or production row adapter were built.
- No full source-wide review archives were created; counts are fixture-level widget totals observed during this probe.
- No review body text is committed in tracked docs.
- ZGO remains a low-volume fixture with only one observed review row; the old v1 Yotpo API mismatch is explained by the current widget using v3 storefront routes, not by source-wide ZGO absence.
- Comment scope, pain/pleasure, integrity, authenticity, and buyer-proof interpretation remain downstream lanes.
- Scent-profile tagging is intentionally not part of the capture row/filter contract unless the source explicitly displays it as source-visible review metadata.
