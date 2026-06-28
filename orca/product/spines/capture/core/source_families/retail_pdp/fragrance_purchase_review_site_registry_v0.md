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
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_retailer_recon_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
stale_if:
  - A later probe changes any source route, status, or row-level verdict below.
  - A primary source stops exposing review rows under the pinned route.
  - A fixture re-probe changes any row-positive / row-empty status below.
  - The review-row contract changes the minimum fields needed for v0 capture.
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

- ZGO row bodies are in a PDP-served Yotpo review section under Direct HTTP.
- Indigo row bodies are in rendered JSON-LD / Judge.me `Review` objects under
  CloakBrowser; the visible page text still shows only the customer-review
  section label.

## Registry

| Source ID | Site | Current status | Route pin | Capture fixture | Row substrate | Use now | Required next fact to change status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `fragrance_retail_ministry_of_scent` | Ministry of Scent | `LOCKED_CAPTURE_FIXTURE_V0` | Direct HTTP first; CloakBrowser only if rows disappear or lazy-load appears. | `https://ministryofscent.com/products/memoirs-of-a-trespasser` | Static HTML exposed Judge.me row bodies (`jdgm-rev__body`) plus verified/source-app/product metadata. | Use as the cheapest row-capture source. | Re-probe if Judge.me markup or PDP template changes. |
| `fragrance_retail_luckyscent` | Luckyscent / Scent Bar | `LOCKED_CAPTURE_FIXTURE_V0` | Direct HTTP aggregate control, then CloakBrowser with `--settle-seconds 5 --scroll-step-px 500 --scroll-passes 4` for rows. | `https://www.luckyscent.com/products/memoirs-of-a-trespasser-by-imaginary-authors` | Rendered review rows exposed body text, dates, reviewer labels, country, variant, verified/store-invitation labels. | Use for rendered row capture. | Re-probe if render+scroll stops loading row bodies or only aggregate JSON remains. |
| `fragrance_retail_twisted_lily` | Twisted Lily | `LOCKED_CAPTURE_FIXTURE_V0` | Direct HTTP aggregate/config control, then CloakBrowser with `--settle-seconds 5 --scroll-step-px 500 --scroll-passes 4` for rows. Record final variant URL when Shopify normalizes it. | `https://twistedlily.com/products/essential-parfums-discovery-set-1` | Rendered review rows exposed body text, rating summary, reviewer names, dates, verified labels, locations, and Shop App labels. | Use for rendered row capture. | Re-probe if rendered rows become config-only or variant routing changes target product binding. |
| `fragrance_retail_zgo` | ZGO Perfumery | `LOCKED_CAPTURE_FIXTURE_V0` | Direct HTTP on the known-reviewed fixture. Do not reuse the original zero-count Orpheon fixture for row capture. | `https://zgoperfumery.com/products/d-s-durga-concrete-lightning-eau-de-parfum` | Static HTML exposed a Yotpo review section with one review body, reviewer label, rating, and aggregate review count; date was not visible in the extracted section. | Use for direct row capture with date residual. | Re-probe if Yotpo section data disappears, count/body diverges, or only aggregate remains. |
| `fragrance_retail_indigo` | Indigo Perfumery | `LOCKED_CAPTURE_FIXTURE_V0_SCHEMA_ONLY` | CloakBrowser with `--settle-seconds 5 --scroll-step-px 500 --scroll-passes 4` on the known-reviewed fixture. Direct HTTP and anti_blocking_http had local certificate failures in this environment. | `https://indigoperfumery.com/products/indigo-perfumery-sampler-set` | Rendered DOM exposed JSON-LD / Judge.me `Review` objects with five `reviewBody` rows plus rating, date, author, review title/name, and product binding. Visible text did not expose row bodies. | Use for rendered structured-row capture with visible-row residual. | Re-probe if rendered schema rows disappear or if a visible-row fixture is found. |

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
without claiming source-wide completeness.

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
