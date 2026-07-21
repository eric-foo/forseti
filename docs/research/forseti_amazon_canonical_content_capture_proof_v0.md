# Amazon Canonical PDP Content — Live Capture Proof and Loss Ledger

```yaml
retrieval_header_version: 1
artifact_role: Research proof record
scope: >
  Live-capture proof, raw-to-content reconstruction result, and loss ledger for
  the Amazon canonical PDP content route
  (retail_pdp_amazon_aggregate_content_v1 / parser_v2), built strictly inside
  the owner-approved pre-v3 Amazon information-capture envelope.
use_when:
  - Judging what Amazon canonical content does and does not retain.
  - Deciding whether an Amazon content packet is fit for a downstream claim.
  - Checking why Amazon retains exact review bodies where Target does not.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_content_cleaning_contract_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/amazon_demand_signal_route_candidates_v0.md
stale_if:
  - Amazon changes celwidget module stamping, twister page state, or the review row hooks.
  - The amazon_pdp_aggregate capture profile changes its scroll, settle, or pin posture.
  - The pre-v3 Amazon information-capture envelope is renegotiated with the owner.
```

## 1. What Landed

`retail_pdp_amazon_aggregate_content_v1` with
`retail_pdp_amazon_aggregate_parser_v2`. `amazon_pdp_aggregate` is now a
content-eligible profile and defaults to `content` retention; content retention
is admitted only at the envelope's single US pin, `--delivery-zip 10001`.
Explicit `--retention-mode raw` remains available at any destination for
diagnosis, recovery, and the existing demand-signal reads.

Qualification is served by the existing runner: `run_content_qualification.py
--route amazon`. No second drift-check runner was introduced.

## 2. The Decisive Divergence From Target — Exact Review Bodies

Target's route retains **body-free** review identity because the separate
`target_bazaarvoice_onboarding` companion owns exact bodies in its own raw
responses. Amazon inverts this.

`amazon_pdp_review_onboarding_v1` writes exactly two files —
`amazon_review_onboarding_control_manifest.json` and a deliberately body-free
`amazon_review_onboarding_summary.json` — over an already-preserved raw parent.
It holds **no raw response bytes of its own**. Verified on companion packet
`01KY0S1ZACF3AG467GV6VA8CJN`: `summary_duplicates_review_bodies: false`,
`all_captured_bodies_remain_in_parent_raw: true`.

The bodies therefore exist only inside the parent PDP DOM, which content mode
hashes and discards. This record retains them
(`review_body_retention: exact_bodies_retained_in_this_record`). Without that,
flipping Amazon to content retention would destroy them.

Consequence for the companion: it remains valid over raw-retained Amazon
parents and is redundant for content-retained captures.

## 3. Source Shape

Amazon's PDP renders one `celwidget` `div` per declared detail-page feature
module and stamps the page's target ASIN on it as `data-csa-c-asin`. On the
proof packet:

| Measure | Value |
| --- | ---: |
| Declared feature modules | 391 |
| Server-side hydrated | 135 |
| Declared but left empty | 256 |
| Stamped with the target ASIN | 331 |

This is Amazon's analogue of Target's declared-but-null CDUI datasources, and
it is inventoried rather than omitted. The attribute is also the only
page-native proof that a merchandising signal belongs to the requested ASIN
rather than to a recommendation rail, so every offer, seller, delivery, media,
feature-bullet, and badge read is scoped to a target-bound module and fails
loud otherwise.

Amazon also carries embedded `a-state` page state. Two keys are load-bearing:
`desktop-twister-sort-filter-data` (the complete source-ordered variant
dimension list) and `social-proofing-page-state` (which names the ASIN the
bought-in-past-month faceout belongs to).

**The buybox exposes more than one offer for the same ASIN.** The one-time
purchase accordion row (`newAccordionRow_0`, initial active) reads `$24.00` and
the Subscribe & Save row (`snsAccordionRowMiddle`) reads `$22.80`. Both are
target-bound facts, not a misbinding, so both are retained with their accordion
slot identity and caption; the initial active row supplies the headline price.
An apex display price that no target-bound buying option carries fails loud.

## 4. Proof Runs

### Raw-to-content reconstruction

Against parent packet `01KY0PHPN10205MKKCK1GB7YH1` (Laneige Sleeping Berry,
ASIN `B07XXPHQZK`, captured 2026-07-20T21:22:38Z, DOM sha256
`d8deed57…8de7877`, matching the companion's recorded `parent_dom_sha256`):

**42 of 42 checked fields reconstruct exactly**, each re-read from the
preserved parent bytes by an independent reader that never calls the extractor.
Covered: ASIN and `#ASIN` input agreement; title, brand store label/URL/logo,
four breadcrumbs, Amazon's Choice badge; active-option price, both buying-option
prices, `currencyOfPreference`, availability, bought-in-past-month, ship-from,
sold-by, two delivery promises, pinned delivery destination; rating, rating
count, five-bucket percent histogram, 13 captured rows, 8 US / 5 international
split, global-ratings text, Bazaarvoice marker count (0), A+ FAQ count (5);
detail-bullet declared ASIN, feature-bullet count, Best Sellers Rank presence,
A+ presence, 30 target-bound image references; 13 variant ASINs, display texts
and selected state; 13 review IDs in source order, **13 exact bodies and their
sha256s**, 13 author profile names, verified-purchase count; and the declared
and target-bound module counts.

### Qualification

`run_content_qualification.py --route amazon` on the exact 2,303,352-byte
parent DOM: `status: match`, exit 0.

Negative control: corrupting one target fact in the DOM
(`70K+ bought` → `80K+ bought`) yields `status: drift`, exit 1,
`changed_top_level_keys: ["rows"]`, with every scratch input preserved. The
gate can fail.

### Cleaning

An Amazon content packet flows through `build_retail_pdp_cleaning_input` with
`cleaning_basis == "content_record"`, producing `ProductEntity`,
`RetailOfferObservation`, and `RetailReviewAggregateObservation` with
`json_pointer` anchors into `content_record.json`.

### Raw-failure fallback

A drifted PDP returns `CONTENT_EXTRACTION_FAILED_EXIT_CODE`, writes no
`content_record.json`, preserves all four raw inputs plus extraction metadata,
and records `retention_outcome: raw_failure` with an `extraction_status`
beginning `failed:`.

### Live dogfood

One anonymous PDP navigation, ZIP `10001`, content retention, packet
`01KY2RW7NS71G7G4D6AT062AWT` (2026-07-22):

- `pin_confirmed: true`, `access_blocked: false`, `delivery_zip_requested: 10001`,
  `wait_until: domcontentloaded`, `settle_seconds: 0.0`;
- `extraction_status: succeeded`, `retention_outcome: content`;
- the rendered DOM and visible text were hashed and discarded
  (`preserved: false`); only the content record, screenshot, and metadata remain.

**Storage impact, measured on that run**: 2,329,573 + 20,881 = 2,350,454
disposable bytes in, 267,896 bytes retained — **11.4% retained, 8.8x
reduction**. The offline parent packet measures 2,324,785 in / 265,808 out at
the same serialization (11.4%, 8.7x).

**Live-versus-parent comparison** (2 days apart) shows the route stable and the
drift real, not parser noise: identical ASIN, price `24.00`, bought-in-past-month
`70K+`, availability `In Stock`, seller `Amazon.com`, rating `4.6`, 13 review
rows in the same 8-US/5-international split, and an identical 383/134/249
parser-v1 module inventory. Parser v2 subsequently recognized eight additional
class-list `celwidget` declarations on the preserved parent (391/135/256); the
append-only live v1 content packet was not rewritten. Genuinely changed: `rating_count` 37,045 → 37,047 (two new ratings)
and the twister variant list 13 → 15 (two new style variants).

The live run also used **fewer** actions than the envelope admits: it completed
with `scroll_passes: 0` and still rendered all 13 review rows, so the admitted
single bounded scroll was not needed on this page.

## 5. Companion Defect Found And Measured

The shared Amazon review parser had a real defect that this route could not
ship on top of, so it was extended **additively** rather than re-shaped.

Amazon repeats each review's header markup (title, star rating, by-line, date,
badges, variation) inside the same `data-hook="review"` element, and it wraps
the body in accessibility teaser sentences plus a Read more/less footer.
`data-hook="review-by-line"` now wraps only the date and carries no author name;
the reviewer's name is in `genome-widget > .a-profile-name`.

Consequences in the landed body-free companion summary, verified against
`01KY0S1ZACF3AG467GV6VA8CJN`:

- `author` holds the review date, not the reviewer;
- `title`, `rating_text`, `source_date_text`, `variant_text`, and
  `badge_labels` are doubled, and `review_location` is mangled;
- `body_sha256` / `body_character_count` describe the body **plus** page chrome;
- `verified_purchase_rows: 10` is an undercount. Independently counted from the
  parent DOM, **all 13 rows carry a Verified Purchase badge**; the three rows
  whose header repeats (`R1S7HOZY4X45ZI`, `R37KGGZNE5015V`, `R19DMS79306A5Y`)
  fail the companion's exact-equality check.

The parser now also exposes `body_rich_text` and `author_profile_names`. No
existing key changed, and the companion summary was proven byte-identical:
rebuilding `01KY0S1ZACF3AG467GV6VA8CJN`'s summary from the same parent yields
sha256 `fa9184f5…9dd8c8` before and after. The content record uses the precise
fields and preserves the chrome-bearing text alongside as
`review_text_hook_with_page_chrome`, so the difference stays visible.

**Superseded by the companion v2 fix.** The byte-identity recorded above held
for `amazon_pdp_review_onboarding_v1` and was the correct no-re-surface result
for that change. The separate out-of-lane fix has since landed: the companion
summary now consumes `body_rich_text`, `author_profile_names`, and
`_amazon_undoubled`, which deliberately changes its output and therefore bumps
the route to `amazon_pdp_review_onboarding_v2` /
`amazon_review_onboarding_summary_v2`. Rebuilding `01KY0S1ZACF3AG467GV6VA8CJN`
under v2 no longer reproduces `fa9184f5…9dd8c8` — that break is the intended
re-surface signal, not a regression. The landed v1 packet is append-only and is
not rewritten.

## 6. Loss Ledger and Non-Claims

- **Rows are labelled top reviews.** No Most Helpful and no Most Recent role is
  claimed, and no ordering guarantee is asserted.
- **No monitoring anchor.** `last_seen_monitoring_anchor_available: false`. This
  route does not establish a last-seen review id.
- **Not the complete review corpus.** 13 exposed rows against 37,045 declared
  ratings. Bounded, and labelled bounded.
- **International rows are preserved but excluded from the US analysis window.**
  Five separately labelled rows are retained in full with their source section;
  the eight `top_reviews_united_states` rows are the default US-market analysis
  window.
- **No reviewer demographics.** No age, skin-type, or skin-concern distribution
  is exposed on the captured rows. None is invented.
- **No customer product Q&A.** The five brand-authored A+ FAQ entries are
  counted separately and are explicitly not customer Q&A.
- **No AI review summary.** The `Customers say` / `cr-summarization` surface is
  absent on the target PDP. If either it or a customer Q&A surface appears
  without a lossless parser, extraction fails and the runner keeps raw inputs.
- **Review media references are retained; media bytes are not fetched.** The
  reference list is the whole review-row subtree, so it also includes reviewer
  avatar and placeholder image URLs; the record labels that scope rather than
  claiming they are all review photos.
- **The route is Amazon-native rendered PDP content and is not Bazaarvoice.**
  `bazaarvoice_marker_count: 0` on the proof packet.
- **Twister variant prices are not exposed.** The dimension state carries a
  price slot whose `priceToPay` is empty, so `variant_price` is `null` with
  `variant_price_posture: not_exposed_in_twister_state`. No variant price is
  inferred from the selected offer.
- **Hydrated module bodies other than the named target-bound ones are not
  retained as canonical content.** They are hashed with the disposable DOM; the
  record states this in the inventory row rather than implying full retention.
- **The `#pqv-bought-in-last-month` anchor is not the bought-in-past-month
  badge.** On the proof packet it is `aok-hidden` and reads `1K+ bought in past
  week` — a different window from the faceout's `70K+ bought in past month`.
  Both are preserved and the disagreement is residualized; neither is chosen
  away. A prior, never-landed Amazon attempt bound to this anchor.
- **No exact inventory quantity and no sold units.** Not exposed.
- **Guest session and anti-CSRF material is never retained.** The DOM carries a
  `session-id`, `anti-csrftoken-a2z` tokens, an `aapiCsrfToken`, and a glow
  delivery-validation token. Those values are collected by key name plus a
  length floor — never by length alone, which on Target matched an ordinary
  product word — and the builder refuses to emit a record containing any of
  them. Only their presence is recorded.
- **Non-claims**: no corpus completeness, no price truth over time, no delivery
  proof beyond the pinned ZIP's rendered text, no demand or sentiment inference,
  no ranking-algorithm validation, and no production monitoring readiness.

## 7. Capture Envelope

Unchanged and not widened. One anonymous US-pinned `amazon_pdp_aggregate` PDP
navigation at ZIP `10001`, the profile's `domcontentloaded` and zero-settle
defaults kept, and at most one bounded scroll to `#customerReviews` (not needed
on the live run). Zero review-portal entries, zero authentications, zero
pagination requests, zero API or Bazaarvoice probes, and zero media downloads
were added. `amazon_pdp_distribution` was not substituted.

## 8. Profile Check

`amazon_pdp_aggregate` was checked for the unsatisfiable-product-literal defect
that Phase 1 found on `target_pdp_aggregate`. It has none: its
`visible_text_contains` requirement is the ZIP pin `New York 10001`, and its
per-target identity check is derived from the captured URL's own ASIN
(`derive_target_asin_from_url`). The profile had already qualified the proof
packet (`pin_confirmed: true`), and it qualified the live dogfood capture. No
profile change was needed.
