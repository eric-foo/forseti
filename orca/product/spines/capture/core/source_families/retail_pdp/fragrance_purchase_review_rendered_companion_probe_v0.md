# Fragrance Purchase-Review Rendered Companion Probe v0

```yaml
retrieval_header_version: 1
artifact_role: Capture probe / rendered PDP companion assessment
scope: >
  Records the completed no-scroll rendered-browser companion capture for the
  five locked fragrance purchase-review fixtures and compares first-viewport
  shopper-visible signals against the direct widget review routes.
use_when:
  - Deciding whether rendered PDP capture should accompany direct widget review
    receipts in the fragrance purchase-review lane.
  - Checking what shopper-visible above-the-fold fields are unavailable from
    widget-only review-row capture.
  - Assessing whether rendered capture should replace, supplement, or remain a
    fallback to direct widget routes.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_site_registry_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_widget_expansion_probe_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md
```

## Result

Rendered PDP capture should be a separate companion signal, not a replacement
for the direct widget review route.

The completed rendered pass captured all five locked fixtures in two no-scroll
viewports, desktop `1365x900` and mobile `390x844`. All ten packets reported
`access_blocked=false` and `rendered_access_classification=no_block_marker`.
Each packet preserved rendered DOM, visible text, viewport screenshot, and
browser metadata. Geometry JSON was also written for each viewport to separate
first-viewport evidence from whole-page visible text.

Scratch evidence root:

`orca-harness/_test_runs/fragrance_rendered_companion_20260629/`

This scratch root is evidence for this probe only. It is not a durable
Attachment Record, not source-wide review coverage, not a review-integrity
score, and not ECR/Cleaning/Judgment input by itself.

## What Rendered Adds

Widget-only review capture answers: which review rows exist, their native ids,
rating/date/verified/media fields when visible, total counts, filters, and body
text for focused review reading.

Rendered companion capture answers: what a shopper is likely to see first on
the PDP before scrolling. It adds presentation and salience fields that widget
routes do not carry: product image placement, title/brand prominence, price or
currency presentation, size choices, CTA placement, stock or pickup cues,
review-count prominence, and whether the review section is visible before a
scroll.

## Fixture Comparison

| Source | Direct widget route without rendered | Rendered first-viewport companion | Assessment |
| --- | --- | --- | --- |
| Ministry of Scent | Widget/static route confirms 4 total review rows; page 2 and `with_pictures` return zero. | Desktop first viewport shows title, price, size choices, quantity, stock cue, and Add to Cart. Mobile first viewport reaches title and price but CTA starts below the first viewport. No above-fold review count is visible in the geometry read. | Rendered adds purchase-context and stock/CTA salience. It does not improve review-row coverage. |
| Luckyscent / Scent Bar | Judge.me route completes the fixture at 14 rows, including rows missing from the rendered page-1 packet; rating filters work; `with_pictures` returns zero. | Desktop and mobile first viewport show product title, brand, `3.7 (14)`, price, and size choices. Desktop also shows Add to Cart, wishlist, store availability, and product taxonomy before the fold. | Rendered adds shopper salience and confirms aggregate count is prominent. Widget remains required because rendered previously missed 4 rows. |
| Twisted Lily | Judge.me widget JSON completes the fixture at 6 rows; rating filters work; per-review media arrays are empty. | Desktop and mobile first viewport show title, price, `4.50 stars`, `6 review(s)`, brand, size, quantity, and CTA. The rendered browser observed `S$45.27 SGD`, so price/currency is locale/session-sensitive unless pinned. | Rendered strongly adds review prominence and purchase context, but price must be residualized unless storefront locale is pinned. Widget remains the row source. |
| ZGO Perfumery | Yotpo v3 route confirms 1 row with native id, date, verified-buyer flag, 5-star distribution, aggregate 5.0, and media absence. | Desktop first viewport shows title, brand, fragrance-note teaser, price, `1 Review`, sizes, and the top of quantity/add-to-cart/pickup context. Mobile first viewport mainly shows promo/header, image, title, brand, and teaser; price and review count are below the first viewport. | Rendered adds major desktop shopper context and proves mobile review salience is weak above fold. Widget remains required for the actual row and verified flag. |
| Indigo Perfumery | Judge.me route completes the fixture at 13 rows over two pages; rendered PDP had previously exposed only schema/fallback context. | Desktop and mobile first viewport show product title, price, quantity, Add to Cart, wishlist, and a visible `CUSTOMER REVIEW` tab. No above-fold rating/count/body is visible in the geometry read. | Rendered confirms the PDP underexposes review strength above fold. Widget is essential for row coverage. |

## With Rendered vs Without Rendered

Without rendered capture, the lane can still build focused review-row receipts
for all five fixtures, but it cannot honestly say what shoppers see first. It
misses first-screen price, CTA, stock/pickup, product image, variant options,
review-count prominence, and whether review cues are hidden below the fold.

With rendered companion capture, the lane gains a shopper-salience layer that
can sit beside the review receipt:

- `above_fold_rating_visible`: whether rating/count is actually visible before scroll;
- `above_fold_review_section_visible`: whether review controls/body/tab appear before scroll;
- `above_fold_cta_visible`: whether Add to Cart or equivalent is visible before scroll;
- `above_fold_price_visible`: whether price is visible before scroll;
- `above_fold_stock_or_pickup_visible`: whether stock, availability, or pickup cues are visible;
- `rendered_locale_residuals`: currency, delivery, region, consent, or session-sensitive fields that need pinning before they become buyer-facing claims.

The smallest complete next implementation is not to parse rendered pages into
review rows. It is to add an optional `rendered_companion` sidecar next to the
focused review receipt, with separate certification and residuals. The widget
route remains the row-integrity substrate.

## Residuals

- Rendered first viewport is viewport-dependent. Desktop and mobile materially
differ for Luckyscent, ZGO, and Ministry of Scent.
- Price/currency is not yet US-storefront-pinned. Twisted Lily rendered as SGD
in this run, so price should be treated as display-context evidence, not stable
US pricing.
- The browser snapshot runner preserves screenshots, but this probe's field
summary uses DOM geometry, not OCR or manual pixel inspection.
- These captures were no-scroll. They intentionally do not measure what appears
after scroll, review-widget expansion, or load-more actions.
- Scratch packet evidence is ignored test output and not a durable Attachment
Record.

## Steps Taken

1. Read the current site registry and widget-expansion probe to recover the five
   locked fixture URLs and the widget-only baseline.
2. Ran `run_source_capture_browser_packet.py` for all five fixtures at desktop
   `1365x900` and mobile `390x844`, with `wait_until=load`, `settle_seconds=3`,
   `timeout_seconds=45`, and no scroll.
3. Verified all ten packet metadata files: every capture reported
   `access_blocked=false` and `no_block_marker`.
4. Ran a bounded Playwright geometry read for each same URL and viewport to
   record elements intersecting the first viewport.
5. Compared first-viewport rendered signals against the direct widget route
   baseline from the registry and widget-expansion probe.
