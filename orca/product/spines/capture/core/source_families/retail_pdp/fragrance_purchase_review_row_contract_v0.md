# Fragrance Purchase-Review Row Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Capture row contract / candidate review-row view
scope: Defines the packet-local candidate row shape for fragrance purchase-review PDP rows before ECR, Cleaning, Judgment, or Attachment Record physicalization.
use_when:
  - Extracting or reviewing individual purchase-review rows from the locked fragrance retailer capture set.
  - Deciding whether a captured review row has enough source-visible data for downstream pain/pleasure and review-integrity analysis.
  - Preventing aggregate review substrate or widget configuration from being mistaken for review rows.
authority_boundary: retrieval_only; defines candidate rows only. It does not authorize live capture, adapter build, Attachment Record storage, ECR, Cleaning, Judgment, scoring, or production use.
open_next:
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_site_registry_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_retailer_recon_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_row_capture_pilot_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_widget_expansion_probe_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md
  - orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
stale_if:
  - Attachment Record physicalization lands and changes how candidate rows become durable bodies.
  - A source route stops exposing review row bodies or starts exposing native review IDs not represented here.
  - Downstream ECR/Cleaning/Judgment contracts add or remove required raw fields.
```

## Decision

`candidate_fragrance_review_row_v0` is a packet-local view over preserved source
bytes. Raw packet material remains canonical. This contract says what a usable
row must preserve; it does not create a durable Attachment Record writer.

The current Retail/PDP projection contract only covers aggregate review
substrate (`retail_review_substrate`). This row contract is the next capture
surface for individual purchase reviews, but it must remain raw/source-visible:
no pain-point label, no pleasure label, no sentiment score, no integrity score,
no dedupe, no reviewer identity resolution, and no cross-retailer product
normalization.

## Minimum Usable Row

A row is usable for the first fragrance pilot only if it has all of the following:

| Requirement | Why it is required |
| --- | --- |
| `source_id`, requested/final URL, capture route, capture time, packet/slice identity when available | Provenance and replayability. |
| Product context: source product title or URL-bound product handle, plus variant/size when source-visible | Prevents a review from floating away from the product/variant it describes. |
| Raw row anchor: visible row ordinal plus selector/fragment/hash basis when available | Lets a reviewer trace the candidate row back to preserved source bytes. |
| `review_body_verbatim` or source-visible body text equivalent | Pain/pleasure extraction requires actual language, not only stars or counts. |
| At least one date/timing field when source-visible, or an explicit timing residual | Review integrity and velocity analysis need temporal evidence or visible absence. |
| Rating when source-visible, or explicit rating residual | Rating helps separate pain/pleasure language from satisfaction level. |
| Per-field residual list | Missing source-visible fields must stay visible rather than becoming silent nulls. |

Rows that only contain aggregate rating/count, widget configuration, CSS strings,
empty review containers, or no-review text are not `candidate_fragrance_review_row_v0`.

## Field Contract

| Field | Required posture | Meaning | Residual rule |
| --- | --- | --- | --- |
| `row_schema_version` | Required literal | `candidate_fragrance_review_row_v0`. | None. |
| `source_id` | Required | Registry ID such as `fragrance_retail_ministry_of_scent`. | No row without it. |
| `source_site` / `source_domain` | Required | Human-readable site and domain. | No row without it. |
| `capture_packet_id` / `slice_id` | Required when packeted | Packet/slice provenance. | If absent in scratch-only diagnostics, mark `packet_identity_absent`. |
| `capture_time` | Required when packeted | Capture timestamp from packet/runner. | If absent, mark `capture_time_absent`. |
| `capture_route` / `route_rung` | Required | Route used, e.g. Direct HTTP or CloakBrowser render+scroll. | No row without route. |
| `requested_url` / `final_url` | Required | Source locator and any redirect/variant-normalized locator. | No row without at least one URL. |
| `raw_row_anchor` | Required | Selector, visible ordinal, native row id, or raw fragment/hash basis. | If only ordinal exists, mark `weak_raw_anchor`. |
| `source_product_title` | Required when source-visible | Product title as shown by source. | `product_title_absent`. |
| `source_product_id_or_handle` | Required when source-visible | Source product handle, Shopify product id, or equivalent. | `product_id_absent`. |
| `brand_label` | Required when source-visible | Brand as source displays it. | `brand_absent`. |
| `variant_label` | Required when source-visible | Size, format, concentration, set/variant, or scent option. | `variant_absent`. |
| `source_native_review_id` | Preserve if visible | Native review id from Judge.me/Bazaarvoice/PowerReviews/etc. | If absent, set `review_key_status=candidate_key_only`. |
| `candidate_review_key` | Required when native id absent | Deterministic packet-local key from source_id, final_url, row ordinal, date text, reviewer label, rating, and review body hash. | Must carry `candidate_key_basis`; not a dedupe claim. |
| `review_key_status` | Required | `native_id_present`, `candidate_key_only`, or `unkeyed_row`. | `unkeyed_row` blocks durable use. |
| `row_ordinal_visible` | Required when native id absent | Visible order in captured review window. | `row_ordinal_absent`. |
| `review_title_verbatim` | Preserve if visible | Source title text. | `title_absent`. |
| `review_body_verbatim` | Required for usable row | Source body text exactly as captured. | If absent, do not emit usable row. |
| `rating_value` / `rating_scale` | Preserve if visible | Source-visible star/rating. | `rating_absent`; do not infer from aggregate. |
| `review_date_source_text` | Preserve if visible | Source-visible date/timestamp text. | `date_absent`. |
| `review_date_precision` | Required if date exists | `date`, `datetime`, `relative`, or `unknown`; mechanical description only. | `date_precision_unknown`. |
| `reviewer_display_label` | Preserve if visible | Displayed reviewer name/initial/anonymous label. | `reviewer_label_absent`. |
| `source_native_reviewer_id` / `reviewer_profile_url` | Preserve if visible | Source-native reviewer/account/profile key. | `reviewer_native_id_absent`; do not invent or resolve identity. |
| `reviewer_profile_metadata_text` | Preserve if visible | Badges, rank, review count, tenure/age, or other source-displayed reviewer metadata. | `reviewer_profile_metadata_absent`; no person-level dossier expansion. |
| `reviewer_location_label` | Preserve if visible | Country/city/state/location text. | `reviewer_location_absent`. |
| `verified_purchase_label` / `verified_purchase_flag` | Preserve only if explicit | Verified buyer/purchase/source label. | `verified_status_absent`; do not treat absence as false. |
| `source_app_label` | Preserve if visible | Shop App, store invitation, Google, Etsy, or equivalent source label. | `source_app_absent`. |
| `transparency_badge_text` | Preserve if visible | Review-source or reward disclosure badge text. | `transparency_badge_absent`. |
| `incentive_disclosure_text` | Preserve if visible | Free sample, reward, sweepstakes, or incentive disclosure. | `incentive_disclosure_absent`; absence is not proof of no incentive. |
| `syndication_source_text` | Preserve if visible | Syndication/source network label if exposed. | `syndication_source_absent`. |
| `helpful_positive_count` / `helpful_negative_count` | Preserve if visible | Source-visible helpful/vote counts. | `helpful_counts_absent`. |
| `media_attached_flag` | Preserve if visible | Photo/video attachment indicator. | `media_indicator_absent`; absence is not proof of no media unless source says so. |
| `brand_response_present` | Preserve if visible | Brand/merchant reply present. | `brand_response_absent_or_unchecked`. |
| `pagination_or_window_label` | Required when visible | Sort/window context, e.g. most recent, page, viewing range. | `review_window_absent`. |
| `per_field_residuals` | Required | List of absent, weak, mismatched, or fallback fields. | No row without residual list, even if empty. |
| `row_scope_residuals` | Required | Corpus limits: visible rows only, sampled PDP only, no source-wide completeness. | No row without scope residuals. |

## Source-Specific Expectations

| Source | Expected row path | Native ID posture | Field caveats |
| --- | --- | --- | --- |
| Ministry of Scent | Direct HTTP Judge.me row HTML, or Judge.me widget endpoint when native ids/filter state are needed. | Preserve native id when present; candidate key is acceptable for pilot if raw row anchor and body exist. | Body/title/verified/source-app/product/vote fields may be visible; blank title is allowed with `title_absent`. |
| Luckyscent / Scent Bar | Judge.me widget endpoint keyed to `lucky-scent-site.myshopify.com` and Shopify product id. | Native Judge.me ids should be preserved from the widget response. | Preserve date, reviewer/country, variant, verified/store-invitation labels when visible; rendered PDP remains fallback context. |
| Twisted Lily | Judge.me widget JSON endpoint keyed to the Shopify product id. | Native Judge.me ids should be preserved from the widget response. | Preserve reviewer/date/location/verified/Shop App labels when visible; record final Shopify variant URL when using rendered fallback packets. |
| ZGO Perfumery | Yotpo v3 storefront endpoint keyed to Yotpo guid `LotcNgdZUJLtOh7iQPZPMJPRTLfGpWs2nlS5U8eh` and Shopify product id `10788875403567`; static PDP section is fallback only. | Native Yotpo review id is present on the v3 route. | Preserve created datetime, verified-buyer flag, rating, body, reviewer display label, media arrays, aggregate rating, and star distribution. Older Yotpo v1 route is row-empty; do not reuse the original zero-count Orpheon fixture. |
| Indigo Perfumery | Judge.me widget endpoint keyed to `indigo-perfumery.myshopify.com` and Shopify product id. | Native Judge.me ids should be preserved from the widget response. | Widget endpoint supersedes schema-only completion; carry a visible-widget-control residual if citing the PDP DOM. Do not emit rows from the original empty fixture. |

## Companion Aggregate Substrate

Per-review rows are not enough by themselves. Each captured PDP should also carry
a packet-level review-substrate companion, separate from row records:

| Field | Preserve when source-visible | Boundary |
| --- | --- | --- |
| `aggregate_rating_value` / `aggregate_rating_scale` | Overall rating shown for the product/PDP. | Context only; not a row rating. |
| `aggregate_review_count` | Total review count shown for the product/PDP. | Context only; not source-wide proof if pagination/window is partial. |
| `rating_distribution_histogram` | 5/4/3/2/1 counts or percentages when visible. | Demand/integrity context only; no static-shape verdict. |
| `review_sort_order` / `filter_state` | Most recent, highest, lowest, pictures-first, verified-only, etc. | Required to interpret the row window. |
| `review_window_label` | Page, visible range, loaded count, or widget batch size. | Makes partial coverage explicit. |
| `review_vendor_or_widget` | Judge.me, Bazaarvoice, PowerReviews, Yotpo, Shopify Product Reviews, etc. | Capture substrate context, not vendor quality scoring. |

This companion substrate may reuse the existing `retail_review_substrate` posture,
but it must not be collapsed into individual row fields and must not stand in for
missing row bodies.

## Mechanical Filter View

A downstream agent may need to reduce context before reading review language. The
allowed v0 filter view is mechanical or source-visible only. It may be derived
from candidate rows, but it must not replace the raw row and must not become a
pain/pleasure, authenticity, buyer-proof, demand, or sentiment label.

| Field | How to derive | Boundary |
| --- | --- | --- |
| `review_month` | `YYYY-MM` from source-visible review date when date precision supports it. | Mechanical recency window only; keep date residuals when date is absent or relative. |
| `review_body_word_count` | Count words in `review_body_verbatim`. | Context-budget aid only; not quality, credibility, or salience. |
| `review_length_bucket` | `<20`, `20_39`, `40_74`, or `75_plus` from word count. | Use to prioritize rows; do not discard raw rows without recording the filter. |
| `rating_exact` / `rating_bucket` | Source-visible `rating_value`; bucket may include exact `1`..`5`, `low_1_2`, `mixed_or_negative_le_3`, and `positive_ge_4`. | Include 4-star and 5-star rows, not only negative rows. |
| `media_attached_flag` | Source-visible review media indicator or widget media arrays/filter result. | Product gallery images do not count as review media. Absence is `unknown` unless the widget says the media-filter row count is zero. |
| `verified_purchase_flag` | Explicit source label or widget field only. | Never infer false from a missing verified label. |
| `comment_scope_hint` | Optional thin pre-filter from the review body: `product_related`, `fulfillment_or_service`, `sample_discovery_or_gift`, `non_product_or_unclear`, or `mixed`. | A routing hint only; not a Cleaning/Judgment label. Preserve the raw body and scope residual. |

Default context-window posture for review-reading agents:

- Always include rows with `review_body_word_count >= 75` when within the bounded fixture window.
- Include `40_74` rows when recent or carrying useful rating/media/verified/source-app fields.
- Include `20_39` rows only when recent or needed for rating balance.
- Ignore `<20` rows by default unless they are very recent low-rating rows or the fixture is otherwise too sparse.

Scent-profile tags are intentionally out of the capture row/filter contract unless
the source explicitly displays them as source-visible review metadata.

## Candidate Key Rule

When `source_native_review_id` is absent, a pilot may use a packet-local
`candidate_review_key`. The key is only a replay handle, not dedupe, identity, or
a claim that two rows across captures are the same review.

Recommended basis:

```text
sha256(source_id | final_url | row_ordinal_visible | review_date_source_text | reviewer_display_label | rating_value | sha256(review_body_verbatim))
```

The row must store `candidate_key_basis` so the key can be recomputed or rejected
later. If the body text is absent, do not produce a usable row.

## Extraction Hard Lines

- Do not emit rows from aggregate count/rating, JSON-LD aggregate only, widget
  configuration, CSS, empty containers, or no-review text.
- Do not infer `verified_purchase_flag=false` from a missing verified label.
- Do not normalize reviewer identity, product identity, or cross-retailer product
  equivalence.
- Do not add inferred scent-profile tags, unless the source explicitly displays
  them as review metadata.
- Do not assign pain point, pleasure point, sentiment, integrity, authenticity,
  salience, demand, or buyer-proof labels.
- Do not fetch pagination, reviewer profiles, or adjacent products from this row
  contract. Those are separate source-access/corpus-scope decisions.
- Do not promote candidate rows into durable Attachment Records until the
  Attachment Record physical writer/layout seam is bound by its owning lane.

## Pilot Acceptance

The first pilot passes this row-contract stage when each locked fixture produces
at least one candidate row with:

- body text;
- source URL and route;
- product binding;
- raw row anchor;
- rating/date/reviewer/verified/source-app fields where source-visible;
- explicit per-field residuals; and
- a row-scope residual saying sampled visible rows are not source-wide coverage.

The pilot fails for a source if the preserved material only contains aggregate
review substrate, widget configuration, or empty containers. In that case, do not
fill the gap with prose or downstream interpretation; either choose another
known-reviewed SKU under the registry promotion rule or leave the fixture partial.

## Non-Claims

- Not an Attachment Record schema or writer implementation.
- Not a parser/adapter implementation spec.
- Not ECR, Cleaning, Judgment, source-quality scoring, pain/pleasure extraction,
  review-integrity analysis, or buyer proof.
- Not source-wide review coverage or full-corpus capture.
- Not authorization for auth bypass, challenge solving, scraping scale, standing
  monitoring, or reviewer-profile expansion.
