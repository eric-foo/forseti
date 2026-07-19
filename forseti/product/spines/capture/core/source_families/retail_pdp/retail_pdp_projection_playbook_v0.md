# Retail/PDP Projection Playbook v0

```yaml
retrieval_header_version: 1
artifact_role: Product playbook (Retail/PDP raw-packet-to-projection contract; non-authorizing)
scope: >
  Stabilizes the Amazon, Luckyscent, Nordstrom, Sephora, and Ulta Retail/PDP projection slice as a
  repeatable view over Source Capture Packets (CapturePacket): what raw capture must provide,
  what projection may emit, what residuals mean, and which retailer-specific
  target-binding limits must stay visible before ECR, Cleaning, or Judgment consume
  the view.
use_when:
  - Deciding whether Retail/PDP work should proceed through projection playbook, projection wiring, ECR sequencing, or a bounded implementation patch.
  - Checking what Amazon, Luckyscent, Nordstrom, Sephora, and Ulta PDP projection may carry from raw packets and what it must residualize.
  - Reviewing the current `retail_pdp_mechanical_projection` helper against product/source-capture doctrine.
open_next:
  - forseti/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/demand_durability_multi_retailer_rendered_capture_spec_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca-harness/source_capture/retail_pdp_projection.py
  - orca-harness/tests/unit/test_retail_pdp_projection.py
branch_or_commit: origin/main @ d78e94ed
stale_if:
  - The core projection doctrine changes carry-or-residualize, loss-ledger, source-envelope, or Retail/PDP family rules.
  - The Retail/PDP projection helper changes row kinds, required bindings, residual vocabulary, or retailer extraction behavior.
  - A new Amazon, Luckyscent, Nordstrom, Sephora, or Ulta capture recon verdict changes the target substrate or access posture.
  - Auto-project-after-capture wiring lands and changes where projection is invoked or persisted.
authority_boundary: retrieval_only
```

## Source-Loading Receipt

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write
  target_scope: docs/product/source_capture_toolbox Retail/PDP projection playbook and narrow retrieval/index pointers
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md, .agents/workflow-overlay/README.md, source-loading, source-of-truth, decision-routing, projection doctrine, data-capture submap, Source Capture Armory README, Retail/PDP projection helper/tests
```

## Decision

The immediate move is **projection playbook first**, not auto-project-after-capture
wiring and not ECR sequencing.

Reason: current code already contains a bounded mechanical helper for Retail/PDP
projection, but the owner-observable contract was scattered across core projection
doctrine, capture recon docs, a rendered-capture spec, and helper tests. Wiring now
would risk converting helper behavior into a hidden product contract, especially
where fallbacks are carried but unsafe, where review counts can come from a
recommendation module, or where a URL/requested SKU differs from the rendered SKU.

This playbook is the contract a wiring or implementation patch must obey. It does
not authorize a runner, schema migration, live capture, ECR production, Cleaning
transform, Judgment read, validation claim, readiness claim, or buyer-proof claim.

## Cynefin Routing

- Regime: **Complicated with a Complex edge**.
- Smallest complete outcome: one retrievable playbook that says what gets captured,
  what projection emits, what residuals mean, and how Amazon/Sephora/Luckyscent/Ulta differ.
- Bottleneck: target binding, not raw capture alone. The risky cases are unanchored
  Amazon price fallback, Sephora recommendation-review noise, Ulta LD JSON versus
  Apollo mismatch, and requested SKU versus rendered SKU drift.
- Stop/pivot rule: if this contract conflicts with current code, treat the code as
  implementation reality and the conflict as a bounded patch candidate. Do not hide
  it behind ECR or Cleaning.
- Disallowed next move: auto-ECR, Cleaning, Judgment, or auto-project wiring that
  does not first preserve the projection residuals and binding gaps named here.

## Packet Input Contract

Projection starts only from a preserved `SourceCapturePacket`. Raw remains
canonical for unflipped and historical routes. The pinned
`sephora_pdp_aggregate`, `luckyscent_pdp_aggregate`, and
`nordstrom_pdp_aggregate` routes default to retailer-owned parser-versioned
content records after their retailer-owned US/USD and all other admission gates pass;
projection is re-derivable from that record without rereading discarded
DOM/text.

Minimum input for Retail/PDP projection:

| Input | Required posture |
| --- | --- |
| Packet and slice identity | Carry `packet_id`, `slice_id`, source locator, slice locator, series id, locale pin, currency pin, variant pin, capture time, cutoff posture, and archive-history posture when known. Unknowns stay as visible packet facts or projection residuals. |
| Preserved bytes | The helper needs hash-verified bytes for every file it consumes. A valid Sephora, Luckyscent, or Nordstrom content record is preferred when present; otherwise missing raw bytes are a hard error, not an empty projection. |
| Rendered DOM | Raw, sample, legacy, and unflipped routes preserve the rendered DOM. A successful Sephora, Luckyscent, or Nordstrom content packet may omit it after recording its hash and byte count; failed admission preserves it. |
| Visible text | Use only as a source-visible companion to DOM. If a value comes only from position-dependent visible text, carry it with an isolation flag and residual. |
| Structured payloads | Preserve embedded `application/ld+json` and `window.__APOLLO_STATE__` verbatim when present. Parsed values may guide row fields, but raw JSON text remains carried. |
| Capture/recon posture | Capture decides access, tool route, and block limits. Projection must not fetch, retry, bypass, or decide capturability. |
| Sephora content record | `retail_pdp_sephora_aggregate_content_v2` carries Sephora parser output, residuals, source-anchor descriptions, and loss entries without packet/file placeholders. It preserves the complete rendered `linkStore.page.product` subtree plus the currently rendered review and Q&A components; v1 remains readable as a legacy input. Consumers bind real packet identity and JSON pointers; manifest envelope facts remain authoritative. |
| Luckyscent content record | `retail_pdp_luckyscent_aggregate_content_v1` carries only target-bound Bread and Roses parser output: two small structured-JSON rows, all three variants in one offer row, and all eight rendered Judge.me reviews in one review-substrate row. Consumers bind real packet identity and JSON pointers; the confirmed default US/USD storefront does not claim US delivery, and the separate origin-derived `buyerCountry=SG` remains non-pin context. |
| Nordstrom content record | `retail_pdp_nordstrom_aggregate_content_v1` carries target-bound Product JSON-LD, the one Nordstrom offer, displayed review aggregate/histogram, rendered review microdata, each rendered card's visible helpful count when present, the source-selected review sort posture, the separate source-labelled most-helpful positive/critical review pair, claims, and the unpinned shipping-destination residual. Consumers bind real packet identity and JSON pointers; the US/USD browser pin remains authoritative and does not establish US delivery. |

If a Retail/PDP packet was commissioned because Commission Signal Board or
Scanning marked a product URL recent/current-state high-attention, that marker is
projection provenance only. Carry capture time, source-visible state, and
residuals; do not fetch, retry, change access/route posture, or treat
current-state capture as buyer proof or Judgment readiness.

## Projection Output Contract

The current helper emits `RetailPdpProjectionPacket` with:

- `projection_method: retail_pdp_mechanical_projection`;
- `projection_version: v1`;
- `certification: view_only; not_cleaned; not_normalized; not_judgment_ready`;
- `rows[]`;
- `binding_map[]`;
- `loss_ledger`;
- packet-level `residuals[]`.

Allowed row kinds:

| Row kind | Meaning | Not allowed to mean |
| --- | --- | --- |
| `retail_pdp_product` | Product/PDP context and source/slice/cadence pins carried from packet facts. | Product truth, normalized product identity, or cross-retailer equivalence. |
| `retail_variant_offer` | Source-visible variant/offer fields such as SKU/product id, variant name, price, currency, availability, and binding source. | Cleaned offer, trusted price, comparable price series, or buy/sell signal. |
| `retail_review_substrate` | Target review substrate fields such as count/rating/source and substrate conflict markers. | Full review corpus, per-review text rows, review quality, sentiment, demand, or credibility. |
| `retail_embedded_structured_json` | Verbatim embedded JSON text plus parse status and raw anchor. | Parsed ontology authority or cleaned product schema. |
| `retail_carried_module` | Frame-sensitive modules such as shipping, loyalty, and recommendations carried as source-visible modules. | Noise by default, demand signal by default, or salience decision. |

Required binding posture for `structure_preserved = true`:

| Binding | Requirement |
| --- | --- |
| `sku_variant_price` | SKU/variant/price fields stay bound together at the row that emitted them. |
| `variant_availability` | Availability stays bound to the same SKU/variant row, not to the page as a whole. |
| `review_substrate_for_product` | Review count/rating/substrate source stays bound to the product/PDP row. |
| `series_locale_currency` | Series id, locale, currency, and variant pins stay carried with the offer row. |

Additional bindings such as `structured_json_for_product` and `module_carried`
are useful, but they do not by themselves prove Retail/PDP structure is
preserved.

## Loss And Residual Rules

Projection may collapse only source-envelope PDP chrome that is logged and
raw-anchored, currently:

- `RETAIL_HERO_IMAGERY_COLLAPSED`;
- `RETAIL_CART_NOTIFY_STATE_COLLAPSED`.

Everything else is carry-or-residualize:

| Residual / posture | Meaning |
| --- | --- |
| `retail_pdp_rendered_dom_absent` | The packet lacks a rendered DOM body for the slice. Projection cannot reconstruct a PDP view. |
| `variant_offer_absent` | The helper did not find source-visible fields sufficient to emit a variant offer row. |
| `review_substrate_absent` | The helper did not find target review substrate fields. |
| `*_malformed_json` | Embedded structured JSON was preserved but could not be parsed. |
| `amazon_price_from_unanchored_visible_text_fallback` | A dollar amount was found only by visible-text fallback. It is carried as unsafe, not trusted as target price. |
| `sephora_review_count_from_unanchored_fallback` | Review count came from a bare visible-text pattern rather than the target "Ratings & Reviews (N)" widget. |
| `sephora_ld_json_review_count_differs_from_target_dom` | LD JSON and target DOM review count disagree. Keep both facts visible. |
| `luckyscent_displayed_structured_rating_mismatch` | Luckyscent's product header rating and structured aggregate rating differ. Keep both source-visible values. |
| `luckyscent_rendered_structured_review_count_mismatch` | The target-bound rendered Judge.me rows do not match the target ProductGroup review count. Content-mode projection fails closed rather than discarding the incomplete DOM/text substrate. |
| `ulta_ld_json_apollo_*_mismatch` | LD JSON and Apollo state disagree for SKU, product id, price, availability, review count, or rating. Keep both substrates visible. |
| `ulta_requested_sku_rendered_sku_mismatch` | Ulta Apollo requested SKU differs from the rendered SKU. Keep both values visible and do not treat the URL/request parameter as the target-bound SKU. |
| `nordstrom_shipping_destination_display_is_not_delivery_pin` | Nordstrom displayed a shipping destination string, but no delivery-location pin was commissioned or confirmed. Preserve the exact display without promoting it to US delivery evidence. |
| `nordstrom_rating_distribution_source_rounding_total_*` | The displayed 5-to-1 percentages do not total exactly 100 because of source rounding. Preserve every displayed bucket and the arithmetic residual. |

Residuals are visible gaps. They are not failures, not suppressions, and not
permission for ECR or Cleaning to author a value from prose.

## Retailer Binding Posture

| Retailer | Capture substrate | Projection binding posture | Residual hard line |
| --- | --- | --- | --- |
| Amazon | Rendered DOM in a US storefront session when commissioned; US storefront pin has a single-probe GO via public delivery ZIP widget, with bot-wall and selector fragility still visible. | Target-anchored ASIN/price/availability/review fields are carried from DOM/visible text. The DOM price input is the target price source when present. Shipping, loyalty, and recommendation modules are carried as frame-sensitive modules. | If price comes only from a visible `$N` fallback, residualize it. Do not let store-card, shipping, or recommendation dollars become target price. Amazon access posture remains the strictest and does not become commercial-scale authority. |
| Nordstrom | Anonymous rendered PDP after the retailer-owned country-preference flow confirms selected US/USD plus the US shopper context. | The numeric PDP id binds target Product JSON-LD, one offer row, the `Sold by Nordstrom` label, details/claims, displayed 4.6/118 review aggregate, star histogram, and currently rendered review microdata. Ordinary captures preserve the source-selected sort posture and each rendered card's visible helpful count; absence of a count stays null rather than becoming zero. The explicit onboarding posture preserves Nordstrom's source-labelled most-helpful positive/critical pair, selects `Most Recent`, and retains every review in the last 30 days with a six-row low-density context floor and 30-row cap. Each continuation activation adds and records six rows. Unrelated recommendation Product JSON-LD is rejected. | `Shipping to 518225` remains an independent display residual. It is not US delivery, inventory depth, or fulfillment proof; source-rounded histogram totals remain explicit. `Most Helpful` and the highlighted pair are retailer UI postures, not proof of the ranking algorithm, representativeness, or engagement quality. A low-density floor is context, not a false claim that older reviews fall inside the 30-day window; a cap hit is explicitly truncated. |
| Sephora | Rendered PDP with Bazaarvoice-backed reviews first-party-rendered after progressive/incremental scroll when review bodies are needed. | Product/variant fields are carried from the complete rendered `linkStore.page.product` subtree; target review substrate uses the "Ratings & Reviews (N)" widget where present. The v2 content parser carries currently rendered review and Q&A components, while recommendation-review counts remain examples/noise posture rather than target substrate. | A bare "`N Reviews`" count is unanchored fallback and must be residualized. A recommendation card count must not become target review count. Currently rendered component rows are a bounded window, not the full review or Q&A corpus and not candidate review-row physicalization. |
| Ulta | Rendered PDP with embedded `application/ld+json` and `window.__APOLLO_STATE__`. | Preserve both LD JSON and Apollo verbatim. Merge source-visible offer/review fields only when substrates are coherent, residualize LD/Apollo mismatches, and residualize requested-SKU versus rendered-SKU mismatch. Carry `apollo_requested_sku` when present. | Requested-SKU versus rendered-SKU mismatch is a target-binding risk. Do not treat the URL/request parameter as target-bound when the rendered SKU differs. |

### Sephora review and Q&A onboarding continuation

When a future Sephora commission includes review or Q&A onboarding, the
capture receipt must preserve the following source-visible state. This is an
operator contract for a commissioned capture, not standing live-capture
authority or a claim that the `2026-07-19` LANEIGE sample already satisfies it.

- Preserve every `regularChildSkus` entry and its exact source flags, including
  `isOutOfStock`, `isLimitedEdition`, `isLimitedTimeOffer`, `isNew`, and
  back-in-stock treatment where present. Do not infer limited-edition state
  from review or Q&A prose.
- Treat Sephora's green and red AI review-sentiment chips as the primary
  summary fields: preserve polarity, exact label, and displayed count for every
  chip. Preserve same-label polarity collisions as separate facts (for
  example, positive `Scent` and negative `Scent`). The AI summary prose and its
  disclosure may be carried as secondary context; neither is a substitute for
  review bodies.
- Capture one unfiltered first-page review baseline so the source's incentive
  mix remains observable. Then explicitly select `Most Helpful` together with
  `Non-Incentivized Reviews Only`, preserve the selected-state evidence, the
  displayed range/count, every rendered review body, helpful votes, disclosure,
  date, rating, author metadata, variant, and media references.
- Explicitly select the source's newest/most-recent review order together with
  `Non-Incentivized Reviews Only`. Activate the review continuation control
  until the oldest retained review reaches at least 30 days before capture, or
  until the source exhausts or blocks continuation. Record the sort/filter
  state, activation count, row count, oldest source date, and any exhaustion or
  access residual. A fixed click count is not evidence of 30-day coverage.
- Inventory the exact source age buckets without collapsing them into decade
  labels. With `Non-Incentivized Reviews Only` active, preserve the displayed
  count for every nonempty bucket and the exact filter state used. If the page
  exposes only `13-17`, `18-24`, `25-34`, `35-44`, `45-54`, and `Over54`,
  those are the authoritative source labels; product-level
  `skuRefinements.ageRange` values are merchandising metadata, not reviewer
  demographic counts. Filtered review bodies by age are a separate,
  commissioned depth step; the minimum onboarding requirement is the complete
  bucket-count breakdown.
- For Q&A, explicitly select `Most Answers`, preserve selected-state evidence,
  the aggregate question count, and every question plus nested answer in the
  initially rendered sorted window. Record the rendered question and answer
  counts separately and preserve any remaining continuation control as a
  bounded-window residual unless deeper Q&A loading was commissioned.

This posture adds one baseline review read, two explicitly sorted/filtered
review views, up to six age-bucket count reads, and one Q&A sort selection to a
future Sephora onboarding. The recurring cost catches silent default-sort
drift, incentive-filter erasure, false 30-day claims, collapsed demographic
labels, and question/answer count conflation.

### Nordstrom review continuation

The bound Nordstrom PDP initially renders six main-list review cards. The
continuation control reads `Load 6 more reviews`: one deliberate activation
appends one additional six-review batch. Capture receipts must count
activations and resulting rendered rows separately. Do not describe the
initial six as a pagination action, and do not describe “every six reviews” as
a click.

For the bounded onboarding posture, use
`--nordstrom-review-posture recent_window_30d`. The retailer-owned action
preserves the separately highlighted most-helpful positive and critical
reviews, selects `Most Recent`, and retains every review dated within the last
30 days. The floor is six main-list rows, so a low-density or empty 30-day
window still carries the nearest six context reviews. The cap is 30 rows (four
continuation activations); if all 30 remain inside the window, the receipt says
`window_truncated` rather than continuing unbounded. The source-state receipt
records cutoff, newest/oldest date, in-window and captured counts, continuation
availability, and the exact activation count. A stale sort, missing highlighted
card, non-consecutive/six-row batch, unsorted dates, missing required
continuation, or failed action preserves supplied raw artifacts and exits
nonzero.

## What ECR May Consume

ECR may consume the projection only as source-visible substrate:

- raw anchors;
- row kinds;
- binding map entries;
- source-visible fields;
- loss ledger;
- residuals.

ECR must not consume:

- a missing residual as if it were a value;
- `structure_preserved = true` as proof of Judgment readiness;
- module presence as salience;
- unanchored fallback fields as target-bound facts;
- review-substrate rows as full review corpus rows;
- a projected row as a cleaned, normalized, deduped, or trusted fact.

## Next Move Selector

Use this selector after the playbook:

| If the next goal is... | Correct move |
| --- | --- |
| Owner-observable contract for the slice | This playbook is the artifact. |
| Capture-time content projection | Standard only for `sephora_pdp_aggregate`, `luckyscent_pdp_aggregate`, and `nordstrom_pdp_aggregate`; use `sample` for parser-fit and `raw` for explicit fallback. Every sibling retail profile remains on the raw/post-hoc path. |
| ECR sequencing | Wait until projection output carries residuals through the ECR handoff. ECR consumes source-visible facts and residuals only; it does not repair projection gaps. |
| Bounded implementation patch | Target one remaining gap: explicit per-review body row support, or runner invocation of the existing helper. Do not combine with ECR or Cleaning work. |

## Non-Claims

This playbook is not validation, readiness, buyer proof, capture authorization,
live-source authorization, commercial scraping authority, ECR design, Cleaning
design, Judgment design, schema ratification, source-quality scoring, fixture
admission, or a claim that the existing Retail/PDP helper is complete. It does
not authorize auto-project-after-capture wiring or implementation work by
itself.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The Retail/PDP projection slice now has a retrievable product playbook that
    binds the existing `retail_pdp_mechanical_projection` helper to the core
    projection doctrine, names Amazon/Sephora/Ulta target-binding posture, and
    records that playbook-first is the correct next move before auto-project
    wiring or ECR sequencing.
  trigger: product_doctrine
  related_triggers:
    - output_authority
    - workflow_authority
  controlling_sources_updated:
    - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_projection_playbook_v0.md
    - forseti/product/spines/capture/core/source_capture_toolbox/README.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/decision-routing.md
    - forseti/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
    - forseti/product/spines/capture/core/source_families/retail_pdp/demand_durability_multi_retailer_rendered_capture_spec_v0.md
    - forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
    - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
    - orca-harness/source_capture/retail_pdp_projection.py
    - orca-harness/tests/unit/test_retail_pdp_projection.py
  intentionally_not_updated:
    - path: orca-harness/source_capture/retail_pdp_projection.py
      reason: >
        This lane resolves the missing product/playbook contract first. Runtime
        patching remains a bounded follow-up once the owner accepts the target
        binding gap or authorizes a specific implementation patch.
    - path: forseti/product/shared/projection_doctrine/core_spine_v0_projection_doctrine_v0.md
      reason: >
        The core projection doctrine already has the Retail/PDP family rule,
        carry-or-residualize discipline, loss-ledger rule, and no-ECR/Cleaning/
        Judgment smuggling boundary. This playbook specializes that doctrine
        without changing it.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The Data Capture submap is the source-loading route for this slice and
        now indexes the playbook. The top-level repo map already routes Data
        Capture detail through the submap and Source Capture Armory README.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not auto-project wiring
    - not live capture authorization
    - not ECR, Cleaning, Judgment, source-quality scoring, fixture admission, or buyer proof
```
