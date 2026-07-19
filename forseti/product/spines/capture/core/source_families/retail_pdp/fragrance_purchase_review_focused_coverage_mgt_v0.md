# Fragrance Purchase-Review Focused Coverage MGT v0

```yaml
retrieval_header_version: 1
artifact_role: Capture operating target / focused review-coverage MGT receipt
scope: Defines the mini god-tier focused review coverage shape for fragrance purchase-review rows, anchored by the Luckyscent pinned Judge.me route probe and adaptable to widget or PDP drift.
use_when:
  - Building or reviewing the first focused review-row adapter for Luckyscent.
  - Deciding which purchase-review rows should enter a bounded reader corpus without capturing every public row.
  - Porting the focused review-coverage shape to other locked fragrance purchase-review sources.
authority_boundary: retrieval_only; no live capture authorization, crawler, durable Attachment Record writer, ECR, Cleaning, Judgment, pain/pleasure labeling, review-integrity scoring, or source-wide completeness claim.
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_site_registry_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_contract_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_widget_expansion_probe_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
stale_if:
  - The Luckyscent pinned product, Shopify product id, Judge.me shop domain, widget endpoint, response shape, or aggregate PDP JSON-LD shape changes.
  - A later owner decision asks for full public review archives instead of focused review coverage.
  - Durable Attachment Record physicalization or review-body storage policy changes the row lifecycle.
  - A production adapter implements a different selection policy, cap, or coverage receipt.
```

## Decision

The mini god-tier version of fragrance purchase-review capture is **Focused
Review Coverage**, not "all public review rows."

The target is enough row diversity and source-visible metadata for a downstream
reader to interpret product-related pain points, pleasure points, and review-data
integrity without turning the lane into a full crawler or a context-window dump.

The focused corpus must include:

- aggregate product review context when source-visible;
- native review ids or candidate-key basis;
- rating, month, body-length bucket, media, verified-purchase, and source-app or
  transparency fields where source-visible;
- a selected row set biased toward 1-star, 4-star, media, long, and recent rows;
- a skipped-row receipt so omissions are visible; and
- accepted residuals explaining what the focused set deliberately leaves out.

This focused reader view is not the retailer onboarding acquisition sample.
Retailer PDP onboarding follows the chronological rule in
`retail_pdp_projection_playbook_v0.md`: complete last-30-day cohort first, then
Most Recent historical context to 30 rows or proven source exhaustion when the
cohort has fewer than 12. The acquired chronological corpus and aggregate rating
distribution are the basis for general product understanding. This document's
rating/media/length-biased subset is only an explicitly labelled context-budget
view over an already acquired corpus; it must never be presented as
representative sentiment or used to replace that chronological corpus.

## Luckyscent Pinned Route Probe

Target product:

```text
https://www.luckyscent.com/products/memoirs-of-a-trespasser-by-imaginary-authors
```

Pinned row route:

```text
GET https://api.judge.me/reviews/reviews_for_widget
url=lucky-scent-site.myshopify.com
shop_domain=lucky-scent-site.myshopify.com
platform=shopify
product_id=8675663642945
page=<1-based page>
per_page=<page size>
filter_rating=<optional 1..5>
sort_by=<optional sort key>
sort_dir=<optional direction>
```

Observed companion aggregate route:

- PDP JSON-LD `ProductGroup.aggregateRating` exposes `ratingValue=3.71`,
  `reviewCount=14`, `bestRating=5`, and `worstRating=1`.
- The Judge.me widget route exposes `total_count=14` but does not expose the
  average rating in the observed response body.

Ignored local probe receipts:

```text
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/luckyscent_focused_mgt_probe_20260629/luckyscent_focused_mgt_probe_summary.json
orca-harness/_test_runs/fragrance_purchase_review_probe_20260629/luckyscent_focused_mgt_probe_20260629/luckyscent_focused_mgt_aggregate_check_20260629.json
```

Raw `.raw.txt` files in the same ignored folder contain review bodies and must
not be moved into tracked docs.

## Observed Coverage Receipt

The pinned Luckyscent route returned 14 deduped review rows for the fixture.

| Field | Observed |
| --- | --- |
| Aggregate average rating | `3.71` from PDP JSON-LD |
| Aggregate review count | `14` from PDP JSON-LD and Judge.me `total_count` |
| Rating distribution | 2-star: 2; 3-star: 4; 4-star: 4; 5-star: 4; 1-star: 0 |
| Month range | 2017-12 through 2026-04 |
| Recent observed months | 2025-12: 2 rows; 2026-04: 1 row |
| Body-length buckets | `<20`: 2; `20_39`: 3; `40_74`: 5; `75_plus`: 4 |
| Native review ids | Present on all 14 rows |
| Verified-buyer true | 3 rows |
| Review media | 0 rows by real picture/video container scan |
| Source media filter | `with_pictures` returned 0 rows |

Focused selection under the current policy selected 10 rows and skipped 4 rows.

| Selection view | Count |
| --- | ---: |
| Selected rows | 10 |
| Selected 2-star rows | 2 |
| Selected 3-star rows | 1 |
| Selected 4-star rows | 4 |
| Selected 5-star rows | 3 |
| Selected rows with native ids | 10 |
| Selected verified-buyer rows | 3 |
| Selected media-attached rows | 0 |
| Skipped rows | 4 |

The four skipped rows were lower-priority context rows under the focused policy:
three short or mid-length 3-star rows and one older 40-to-74-word 5-star row.
Their existence remains visible in the skipped-row receipt; they are not silently
erased.

## Focused Selection Policy

The first implementation should capture all row metadata in the bounded widget
window, but only pass a focused subset of review bodies to downstream readers
when context is tight.

Always select:

- all 1-star rows;
- all 4-star rows;
- all rows with source-visible review media;
- all rows with `review_body_word_count >= 75`;
- recent low-rating rows, including 2-star rows when no 1-star rows exist.

Usually select:

- 5-star rows when recent or `review_body_word_count >= 75`;
- 2-star and 3-star controls when recent or `review_body_word_count >= 75`;
- `40_74` rows when they add rating balance, verified-purchase evidence, media,
  or recency.

Usually skip from the reader body set, while retaining metadata in the receipt:

- `<20` rows unless they are recent low-rating rows or the product has too few
  rows;
- older `20_39` rows unless needed for rating balance;
- older 5-star rows below the `75_plus` length threshold when the product already has
  enough positive coverage.

Month windows are derived after capture from source-visible review dates. Do not
depend on Judge.me for server-side month filtering in v0.

## Adaptive Cap

The adapter should not hard-code "10 rows" as the permanent target. Use a
budget-aware cap:

1. Capture and normalize the bounded widget window first.
2. Build the coverage receipt from all normalized rows.
3. Select rows in priority order: 1-star, 4-star, media, `75_plus`, recent low
   rating, verified, recent or long 5-star, then recent or long 2/3-star controls.
4. If the selected body set is still too large, keep the highest-priority rows
   by rating diversity and recency, but preserve skipped-row counts and reasons.
5. If the fixture is small enough, include all row bodies.

This keeps the operating shape adaptable across small one-row sources such as
the current ZGO fixture and larger sources where all bodies would overflow the
reader context.

## Adapter Shape

The first implementation should be a small adapter with replaceable route
modules, not a retailer-specific one-off parser.

| Component | Responsibility |
| --- | --- |
| `SourceRouteProbe` | Resolve the current product route, widget vendor, shop/app key, product id, and endpoint shape from the pinned registry entry and PDP evidence. |
| `ReviewPageFetcher` | Fetch bounded pages and rating/media filter controls at human-scale volume. |
| `AggregateCompanionParser` | Preserve PDP aggregate rating/count separately from row fields. |
| `RowNormalizer` | Normalize native id, rating, timestamp/month, body hash/body pointer, word count, length bucket, verified flag, media flag, helpful counts, transparency/source-app badges, product title/url attrs, and residuals. |
| `FocusedSelector` | Apply the focused selection policy and adaptive cap. |
| `CoverageReceipt` | Emit totals, distributions, selected/skipped counts, route health, and accepted residuals without raw body text in tracked docs. |
| `RouteHealth` | Decide whether to proceed, rederive route parameters, or fall back to rendered capture. |

The row normalizer should rely on native widget data attributes before visible
text. For Luckyscent Judge.me rows, observed useful anchors include
`data-review-id`, `.jdgm-rev__rating[data-score]`, `.jdgm-rev__timestamp`
`data-content`, `data-verified-buyer`, product title/url attributes,
thumb-count attributes, and review-source badge attributes.

## Drift And Fallback Contract

The route is healthy when all of these are true:

- endpoint status is successful;
- response is parseable JSON with an `html` field and `total_count`;
- `.jdgm-rev` rows are present when `total_count > 0`;
- native ids are present or candidate keys can be generated with an explicit
  weaker-key residual;
- rating/date/body fields are recoverable from source-visible row material; and
- media diagnostics distinguish real review media from generic product, avatar,
  star, or tracking images.

If the route changes:

| Failure signature | Next move |
| --- | --- |
| Widget endpoint 404 or empty, but PDP loads | Re-derive `shop_domain`, product id, and Judge.me config from PDP scripts, Shopify product JSON, and widget params before changing source status. |
| `product_id` no longer matches | Re-read the pinned PDP for current Shopify product id or variant/product group ids. |
| Widget HTML selector shape changes | Prefer data attributes and native row ids; if row fields are no longer parseable, run a rendered PDP packet as a body-possession fallback. |
| Rating/media filter params stop working | Capture default pages and post-filter locally; record server-filter failure in the receipt. |
| PDP aggregate disappears | Preserve widget `total_count`; mark `aggregate_average_absent` unless a visible PDP aggregate is recovered elsewhere. |
| Media filter and row scan disagree | Trust real review media containers and source media-filter counts, not generic images. Carry `media_diagnostic_mismatch` if unresolved. |
| Known fixture returns zero rows | Re-probe one known-reviewed SKU before downgrading the whole retailer. |

Do not escalate from this adapter into broad product discovery, standing
monitoring, auth bypass, challenge solving, or source-wide crawling.

## Accepted Residuals

| Residual | Why accepted now | Remaining risk | Upgrade trigger |
| --- | --- | --- | --- |
| Not all public review bodies enter the reader set | Focused coverage preserves the rows most likely to carry pain, pleasure, and integrity signals while controlling context. | A skipped row could contain a rare issue. | A product decision requires exhaustive review-language audit, litigation-grade evidence, or model error traces to skipped rows. |
| Fixture-level, not source-wide | The current lane is proving purchase-review capture on bounded fragrance fixtures. | Source-level review behavior may differ across products. | Owner asks for source-wide coverage or a selected source becomes a recurring production source. |
| Widget route is preferred over full rendered PDP | It gives native ids, filters, dates, verified flags, and pagination more cheaply. | PDP-visible presentation could diverge from widget payload. | Widget/PDP total mismatch, row text mismatch, or source display controls become decision-critical. |
| Aggregate average split across PDP and widget | PDP JSON-LD carries average rating; widget carries rows and total count. | If one substrate changes, aggregate context may be partial. | Average rating is missing or conflicts with widget totals on re-probe. |
| No review media on the pinned Luckyscent fixture | Both real media scan and `with_pictures` filter returned zero. | Another product may have media, and media fields remain untested on positive media rows. | A fixture or source with media-positive reviews is selected. |
| No pain/pleasure or integrity labels in capture | Capture should preserve source-visible fields only. | Reader still needs downstream interpretation. | Cleaning/Judgment lane binds label schema and storage. |
| No durable Attachment Records yet | Current raw bodies are ignored scratch outputs. | Reuse depends on local scratch unless a later lane physicalizes storage. | Attachment Record writer/layout is authorized for review rows. |

## Steps Performed

1. Used the existing site registry to pin Luckyscent to the Judge.me route with
   `shop_domain=lucky-scent-site.myshopify.com` and product id `8675663642945`.
2. Fetched the pinned PDP and Judge.me widget pages/filters into ignored scratch
   output.
3. Parsed Judge.me widget JSON and row HTML for native review ids, ratings,
   source timestamps, verified flags, product attrs, helpful counts,
   transparency/source-app badge attributes, body word counts, and real media
   containers.
4. Tested default pagination, exact rating filters, media-oriented sort/filter
   routes, and recent sort controls.
5. Diagnosed media by separating generic images from real review picture/video
   containers and by checking `with_pictures`.
6. Parsed PDP JSON-LD separately to recover aggregate average rating and review
   count.
7. Built a body-free focused selection summary with selected/skipped counts and
   distributions.
8. Kept raw review bodies in ignored `_test_runs/` output only.

## Non-Claims

- Not validation, readiness, source completeness proof, or fixture admission.
- Not a production adapter implementation.
- Not source-wide review coverage.
- Not a full public review archive.
- Not durable Attachment Record physicalization.
- Not ECR, Cleaning, Judgment, review-integrity scoring, pain/pleasure labeling,
  sentiment, demand, buyer proof, or commercial-readiness evidence.
- Not authorization for broad scraping, standing monitoring, auth bypass,
  challenge solving, proxy behavior, or source discovery.
