# Target Canonical PDP Content — Live Capture Proof and Loss Ledger

```yaml
retrieval_header_version: 1
artifact_role: Research proof record
scope: >
  Live-capture proof, raw-to-content reconstruction result, and loss ledger for
  the Target canonical PDP content route
  (retail_pdp_target_aggregate_content_v1 / parser_v1).
use_when:
  - Judging what Target canonical content does and does not retain.
  - Designing the Amazon content route, which faces the same SSR/DOM split.
  - Deciding whether a Target content packet is fit for a downstream claim.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_content_cleaning_contract_v0.md
stale_if:
  - Target changes which CDUI datasources server-side rendering hydrates.
  - The target_pdp_aggregate capture profile changes its scroll or settle posture.
```

## 1. What Landed

`retail_pdp_target_aggregate_content_v1` with
`retail_pdp_target_aggregate_parser_v1`, built from the Target-owned
`__NEXT_DATA__` CDUI page state plus the rendered offer and review regions.
`target_pdp_aggregate` is now a content-eligible profile and defaults to
`content` retention.

The existing `target_bazaarvoice_onboarding` companion is unchanged. It remains
the owner of exact review and Q&A bodies.

## 2. Source Shape — The Decisive Finding

Target's PDP server-side renders **one** hydrated CDUI datasource:

| CDUI data-source module | SSR state |
| --- | --- |
| `ProductDetailWebDatasourceCore` | hydrated — full Redsky product object |
| `ProductDetailWebDatasourceCircleOffers` | declared, `null` |
| `ProductDetailWebDatasourceFulfillmentAndVariations` | declared, `null` |
| `ProductDetailWebDatasourcePersonalized` | declared, `null` |
| `ProductDetailWebDatasourceWithStore` | declared, `null` |

The layout declares `ProductDetailPrice`, `ProductDetailVariationSelector`, and
`ProductDetailFulfillment`, but their data arrives only after client hydration.
Across the entire `__NEXT_DATA__` document, `current_retail`, `"price"`,
`availability_status`, and `child_tcin` each occur **zero** times.

Consequence: page state alone cannot produce an offer. Price, fulfillment, and
store context are recovered from the rendered DOM; identity, copy, ingredients,
media, classification, and review aggregates come from page state. Declared
modules are inventoried with their hydration state rather than silently omitted.

## 3. Proof Runs

**Offline reconstruction** against the admitted parent packet
`01KXR823YS3V5M9E01QXP71ETC` (TCIN `80184023`, captured 2026-07-17):

- 29 of 29 checked fields reconstruct exactly from source — identity (TCIN,
  DPCI, barcode, brand, linking id), copy (title, description, 8 bullets,
  3 soft bullets), ingredients, warning, media counts, package dimensions,
  wellness attributes, and every review aggregate.
- `run_content_qualification.py --route target` returns `status: match`, exit 0
  on the real 495,130-byte DOM.
- Negative control: corrupting one field yields `status: drift`, exit 1,
  `changed_top_level_keys: ["tcin"]`, scratch preserved. The gate can fail.

**Live dogfood.** The original dogfood ran at ZIP `52404`, which is **not an
admitted Target destination**. `retail_storefront_pin_registry_v0.md` admits
`CONFIRMED_ZIP_10001` only, and `52404` is the ZIP recorded in that registry's
`NO_GO_SPLIT_LOCATION_SIGNAL` probe. Packets `01KY2E0Q5C2V598GSEGG6ABZRM` and
`01KY2E4GG7J3CN93S6ZA4CRQT2` therefore carry `pin_confirmed: true` for a
destination the registry does not admit. They remain append-only historical
evidence of the extraction shape and are **superseded for pin evidence**; the
shared retailer-baseline gate now rejects that ZIP outright.

Re-dogfooded 2026-07-22 at the admitted pin, one PDP navigation each:

| Packet | Posture | Result |
| --- | --- | --- |
| `01KY32AAVCG3JMCM08JGPSJS8T` | content, ZIP `10001` | `succeeded` / `content`, `pin_confirmed: true`, `Ship to 10001` |
| `01KY32E2RH3B60W0MCQ899WZY9` | raw diagnostic, ZIP `10001` | `pin_confirmed: true`; DOM retained for diagnosis |
| `01KY32KG4DVVV5AEYW9P4P5S89` | content attempt, ZIP `10001` | `target_delivery_zip_pin_failed`; `retention_outcome: raw_failure`, all inputs preserved |

The content packet retains 18 rows, TCIN `80184023`, rating `4.45` / `1772`
ratings / `758` reviews, and full fulfillment. Storage: 441,592 disposable bytes
in, 23,826 retained — **5.4%, 18.5x**, matching the earlier run. The offline
parent packet measures 500,420 in / 23,800 out (4.76%, 21.0x).

Two intermittency findings, both recorded rather than tuned away:

- **The ZIP-10001 pin was not reliable**: one of three attempts returned
  `target_delivery_zip_pin_failed` at the `wait_for_zip_control` step. The route
  failed correctly — raw preserved, no admitted content. Root cause: the
  plugin's inner readiness cap was 10s while the operator's setup budget is 30s,
  so it forfeited roughly 20s it had been granted. The cap is now 20s, still
  bounded and still yielding to the caller's deadline. This is a readiness wait
  on the already-open setup surface — no extra request, navigation, or retry.
- **The price does not always bind to the target's price module.** The content
  packet at `10001` bound no price, while the raw diagnostic captured minutes
  later contains one `data-module-type="ProductDetailPrice"` module carrying
  `$14.69`, and the module-scoped extractor returns `14.69` when run against it.
  The capture profile's own sufficiency gate requires a visible `$n.nn` and
  passed on the content run, so a price was on that page too. That case now
  **fails loud** instead of retaining a priceless offer: a rendered price the
  parser cannot bind is an exposed surface without a lossless parse, which the
  owning standard requires to force raw fallback. Failing keeps the rendered
  DOM — exactly the evidence that was discarded and unavailable when this first
  appeared. A page that genuinely shows no price is still an honest absence and
  keeps its residual.

**Live-versus-parent comparison** (4 days apart) shows the route stable and the
drift real, not parser noise: identical structure (18 rows; 1 product, 1 offer,
1 review substrate, 1 module subtree, 6 carried modules, 8 review identity rows),
identical TCIN/DPCI/barcode/brand, identical price `14.69`, identical
`structured_review_count` 758 and `question_count` 34. Genuinely changed:
`rating_count` 1771 → 1772 (one new rating) and the shipping date.

**Cleaning**: a Target content packet flows through
`build_retail_pdp_cleaning_input` with `cleaning_basis == "content_record"`,
producing `ProductEntity`, `RetailOfferObservation`, and
`RetailReviewAggregateObservation` with `json_pointer` anchors into
`content_record.json`.

**Raw fallback**: a drifted PDP returns `CONTENT_EXTRACTION_FAILED_EXIT_CODE`,
writes no `content_record.json`, preserves all four raw inputs plus extraction
metadata, and records `retention_outcome: raw_failure` with an
`extraction_status` beginning `failed:`.

## 4. Loss Ledger and Non-Claims

- **No variants.** `relationship_type_code` is `SA` (standalone) and the
  variation datasource is unhydrated, so `variant_module_state` is
  `not_exposed`. No variant is inferred. A hydrated variation datasource flips
  this to `observed`.
- **No review or Q&A bodies.** Retained review identity is body-free:
  Target-native UUID, author external id, rating, timestamp, `body_present`, and
  `body_char_count`. Bodies live in the companion's raw responses.
- **Target-native review IDs do not join Bazaarvoice review IDs.** The page
  state uses UUIDs (`2e6c916e-2add-…`); the companion uses numeric Bazaarvoice
  ids (`348134971`). Measured on the proof pair: **0 of 8** ids overlap while
  **7 of 8** bodies match by text. There is no shared key, and none is invented.
- **The 8 page-state most-recent rows are not nested inside the companion's 100
  Most Recent rows.** One of the eight had no body match in the companion
  window, so neither surface is a superset of the other.
- **Three review totals disagree and all three are preserved**: rendered star
  ratings (1771/1772), CDUI `review_count` (758), and the rendered filtered
  match count (757, when the widget paints). None is reconciled away.
- **The rendered review widget is lazy and below the fold.** Under the admitted
  profile posture it frequently does not paint, so the filtered match count and
  percent distribution can be absent. When that happens the record carries
  `target_rendered_filtered_review_count_not_observed` and
  `target_rendered_percent_distribution_not_observed_structured_counts_retained`.
  A `scroll_passes=1` probe was measured and **did not** recover them (visible
  text 2,204 bytes either way), so no scroll change was adopted. The CDUI
  per-star **counts** (1319/195/94/51/112) are always retained and are stricter
  than the rendered percentages.
- **No price history, promotion, or Circle offer.** The offers datasource is
  unhydrated; only the currently rendered price is retained.
- **No exact inventory quantity and no sold units.** Not exposed.
- **Guest session and bot-defense material is never retained.** The page state
  carries a `site-top-of-funnel/get-cookies` query with access/refresh/id tokens
  and PerimeterX cookies. The builder collects those values and refuses to emit
  a record containing any of them; only their presence is recorded.
- **Non-claims**: no corpus completeness, no price truth over time, no delivery
  proof beyond the pinned ZIP's rendered text, no demand or sentiment inference,
  and no production monitoring readiness.

## 5. Capture Envelope

Unchanged and not widened: one anonymous PDP navigation under the existing
`target_pdp_aggregate` profile with its ZIP pin. No review-portal entry, no
authentication, no pagination, no API probe, and no media download were added.

## 6. Profile Correction

`target_pdp_aggregate` required the literal `BYOMA Liptide Lip Mask` in visible
text — the brand-grid fixture product, which never appears on a Target PDP. The
requirement was therefore unsatisfiable and the profile had never qualified a
real PDP capture; the existing Target PDP packets in the lake were captured with
no profile at all (`pin_confirmed: null`). It now pins this profile's own proof
product, as the Sephora, Ulta, and Nordstrom PDP profiles do.
