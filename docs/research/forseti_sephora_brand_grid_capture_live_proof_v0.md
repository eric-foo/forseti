# Forseti Sephora Brand-Grid Capture Live Proof v0

```yaml
retrieval_header_version: 1
artifact_role: Research / implementation validation receipt
scope: >
  Records the bounded 2026-07-20 UTC live Summer Fridays Sephora brand-grid
  capture, typed view-only projection, raw-file integrity check, completeness
  reconciliation, and page-kind-specific storefront-country/currency results.
use_when:
  - Reviewing the first live proof for the reusable Sephora brand-grid route.
  - Rechecking the captured Summer Fridays grid count, projection, or market-pin limitation.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/retail_pdp/retailer_information_extraction_standard_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_storefront_pin_registry_v0.md
stale_if:
  - The Sephora grid profile, market assertion, or retail-grid projection changes.
  - This dated receipt is cited as current storefront or assortment evidence.
```

## Outcome

`MIXED_PAGE_KIND_PIN_RESULT`.

The supported runner preserved a complete 34-of-34 Summer Fridays parent-product
projection. Under the historical implementation it exited nonzero because the
grid exposed no explicit selected currency code. Under the current country-only
grid assertion, read-only re-evaluation still rejects that packet because its
preserved DOM retains the country-dialog diagnostic marker; it is not
retroactively forced through.

The later warmed Clinique page states satisfy the US country route — country
dialog absent plus rendered `country=US` — under read-only re-evaluation of
their preserved bytes. Both were captured before the country-only grid rule
existed, so their own manifests remain immutable failed-pin records; no
runtime-confirmed grid packet exists yet. Neither exposes an explicit currency
code, so currency remains unpinned. Dollar glyphs are never promoted to `USD`.

## Run Boundary

- URL:
  `https://www.sephora.com/brand/summer-fridays?country_switch=us`.
- Capture time: `2026-07-20T21:50:55Z`.
- Session: anonymous and ephemeral; no browser profile, storage state, proxy,
  VPN, credential, cookie injection, or login.
- Data root: `C:\tmp\forseti-sephora-brand-grid-data`.
- Raw packet: `raw/260/01KY0R5E8MFSZWT456KKMEYRWK`.
- Typed projection:
  `derived/sephora_brand_grid/summer_fridays_brand_grid_projection_20260721_02.json`.
- Projection SHA-256:
  `b0b09bf0fd67eb229cd9a28f7762fbdaee91876405cffd9c531ca4a2f9304756`.
- Projection certification:
  `view_only; not_cleaned; not_normalized; not_judgment_ready`.

## Exact Command

```powershell
python -B forseti-harness/runners/run_source_capture_cloakbrowser_packet.py `
  --url 'https://www.sephora.com/brand/summer-fridays?country_switch=us' `
  --source-family retail_pdp `
  --source-surface cloakbrowser_snapshot `
  --decision-question 'What parent products are present in the Summer Fridays Sephora US brand grid?' `
  --data-root 'C:\tmp\forseti-sephora-brand-grid-data' `
  --retail-capture-profile sephora_grid_aggregate `
  --sephora-market US `
  --retail-grid-projection-output 'C:\tmp\forseti-sephora-brand-grid-data\derived\sephora_brand_grid\summer_fridays_brand_grid_projection_20260721_01.json' `
  --timeout-seconds 90
```

The command historically returned exit code `4` with
`sephora_market_pin_failed`; both the raw packet and initial `_01` projection
were preserved. Its manifest remains immutable and continues to record that
historical runtime result.

A read-only current-assertion replay over the preserved DOM returned
`confirmed=False` because the country-dialog diagnostic marker remains in the
bytes. This is now the decisive country-route failure; absent explicit currency
is retained only as an independently typed `UNPINNED` currency result.

## Raw Integrity

Every manifest-declared raw hash was recomputed from the stored bytes and
matched:

| Preserved file | SHA-256 |
| --- | --- |
| `raw/01_cloakbrowser_rendered_dom.html` | `52a750e6aef8e592dbabb14d6eb807818bf26a5289275e75f2fe42ab567b1320` |
| `raw/02_cloakbrowser_visible_text.txt` | `ed9677594147e81d667544f1de73c159e8af22479fda8ac64defabc2ff7a9861` |
| `raw/03_cloakbrowser_viewport_screenshot.png` | `1d39003c2f4738b5dd2b10365b98f302bb90f735aca41aca90b85cd156964d2e` |
| `raw/04_cloakbrowser_snapshot_metadata.json` | `60f3fa7c63b02ee878be443222bf051000cdc11d79d1faeeea9e3d0e09ee323c` |

## Post-Review Projection Correction

The delegated review returned `NO_PATCH_NEEDED` but flagged ranged Sephora
`listPrice` handling as a low-severity residual. Home-lane adjudication checked
that observation against the preserved source and found five explicit price
ranges. The initial `_01` projection had retained each exact string in
`price_display` but incorrectly left `price_range` null and carried the range as
a scalar `price`; that contradicted the commissioned price/range requirement.

The implementation was corrected and the projection was regenerated append-only
from the same hash-verified packet:

```powershell
python -B forseti-harness/runners/run_retail_grid_projection.py `
  --packet-dir 'C:\tmp\forseti-sephora-brand-grid-data\raw\260\01KY0R5E8MFSZWT456KKMEYRWK' `
  --output 'C:\tmp\forseti-sephora-brand-grid-data\derived\sephora_brand_grid\summer_fridays_brand_grid_projection_20260721_02.json'
```

The `_02` projection is the current typed view for this receipt. It contains 34
rows, remains `complete`, and has SHA-256
`b0b09bf0fd67eb229cd9a28f7762fbdaee91876405cffd9c531ca4a2f9304756`
over 106,619 stored bytes. The append-only `_01` output remains historical and
is superseded for typed price use; no raw bytes were recaptured or rewritten.

## Projection and Completeness

| Check | Observed result |
| --- | --- |
| Subject binding | `Summer Fridays`; requested slug and target/canonical URL agree |
| Page-declared total | `34` |
| Serialized placements | `34` |
| Unique parent products | `34` |
| Duplicate placements | `0` |
| Completeness status | `complete` |
| Termination | `retailer_serialized_count_reconciled` |
| Projection-level residuals | none |
| Explicit currency codes | none |
| Explicit price ranges | `5`, retained as exact display plus typed minimum/maximum |

Each typed row has a unique Sephora parent product ID and a raw JSON-pointer
anchor into the preserved `linkStore.page.nthBrand.products` array. Missing
source-visible fields remain per-row residuals, including exact inventory,
sold units, selected variant, delivery-location pin, category, availability
summary, and explicit currency code.

## Repeat-Capture Comparison

The earlier diagnostic packet
`raw/37c/01KY0JRJSVJH3JDB05QW9Q4DF7` was captured at
`2026-07-20T20:16:31Z`. Compared with the final packet:

- declared, serialized, and unique counts remained `34 / 34 / 34`;
- no product IDs were added or removed;
- no products changed position;
- no source rows changed price, rating, review count, or badges;
- the first five parent IDs remained
  `P455936`, `P525302`, `P520759`, `P522826`, and `P518147`;
- the DOM hash changed from
  `7ea9700d8a3d559aaaf5bac19d6af8e218e52e503eae489f401beef0a65ea664`
  to
  `52a750e6aef8e592dbabb14d6eb807818bf26a5289275e75f2fe42ab567b1320`.

This comparison establishes stability across the two bounded observations, not
longitudinal assortment stability.

## Clinique Multi-Page Follow-Up

A live Clinique follow-up on 2026-07-21 established the lowest-footprint
multi-page behavior. CloakBrowser launched with `humanize=True`; the Sephora
market plugin used the same page object to warm the commissioned URL, scope and
activate the exact country-dialog continuation when present, and navigate the
main target. The grid profile then performed one bottom scroll, settled for two
seconds, and activated the unique retailer-owned `Show More Products` control.

Packet
`C:\tmp\forseti-sephora-brand-grid-data\raw\c31\01KY2MDZ61BNYMAKP39SAKJ6ZG`
records one scroll and one humanized click. Sephora changed the URL to
`currentPage=2`, displayed `1-79 of 79 Results`, and removed the continuation
button. The rendered `linkStore.page.nthBrand.products` array nevertheless
remained the first page's 60 rows, so projection
`clinique_brand_grid_projection_20260721_05.json` correctly remained
`incomplete` (SHA-256
`ec5f723c608db178d6590c993c586c2499737b5716e50eb196c6291aff22c7f4`).

A second same-tab capture of Sephora's retailer-generated
`currentPage=2` state, packet
`C:\tmp\forseti-sephora-brand-grid-data\raw\369\01KY2MHMTGDXDTFGHYWQDZW1W5`,
serialized the remaining 19 rows. Its page-local projection is
`clinique_brand_grid_projection_20260721_06.json` (SHA-256
`8d82cccbe631f2bde79e6ebb7ec677c13413e9de27cd9768a6f12c02d502be0d`).
The two page states reconcile to 79 unique parent IDs with zero overlap and
zero duplicate IDs. All 79 rows retain a price or price range, rating, and
review count; 66 have scalar prices, 13 have price ranges, and 9 have one or
more source-visible badges.

The comparison-only union is preserved outside the repository as:

- `C:\tmp\forseti-sephora-brand-grid-data\derived\sephora_brand_grid\clinique_brand_grid_two_page_comparison_20260721_01.json`
  (SHA-256
  `211700fdb2e21216cd4c43ef0645c00664cdae3d9ed8172bfaa1f41e2bfcf525`);
- `C:\tmp\forseti-sephora-brand-grid-data\derived\sephora_brand_grid\clinique_brand_grid_two_page_comparison_20260721_01.csv`
  (SHA-256
  `eaa7fa3f7a089a90c16364ea07289b29aa228f21fa135bf3496a7c44ad03c324`).

That union is explicitly not a single certified Projection packet: each source
row retains its own packet, slice, and raw anchor. The result proves that
Sephora's visible continuation and serialized product state have different
lifecycles; displayed `1-N` plus a vanished button cannot upgrade one
page-local `linkStore` array to complete. Read-only replay through the current
page-kind assertion returns `confirmed=True` for both packets: the
country-routing dialog is absent and `Sephora.renderQueryParams.country=US`.

Both manifests are immutable and still record the historical runtime result,
because the implementation in force at capture time required an explicit grid
currency code. Each carries `sephora_market_pin_failed: US/USD rendered-market
conjunction was not confirmed; packet preserved but MUST NOT be admitted as
Sephora US/USD storefront evidence`, and a `declared_storefront_market`
limitation ending `treat storefront country and currency as un-pinned (honest
gap)`. The US country-route reading is therefore this offline re-evaluation of
the preserved rendered bytes, not the packets' own recorded runtime result; a
runtime-confirmed grid packet requires a fresh run under the current assertion.
Neither grid state exposes an explicit currency code, so currency remains
unpinned and no USD claim is made.

The append-only diagnostic sequence remains preserved. The initial no-pagination
capture (`_01`) held 60/79; `_02` exposed a non-waiting selector race; `_03`
confirmed the selector action still did not fire; `_04` recorded
`ElementNotStableError` under humanization; `_05` proved the settled
humanized click; and `_06` isolated the 19-row serialized second page.

## Non-Claims

The warmed Clinique packets read as US country-route evidence only through
current offline re-evaluation of their preserved bytes; their own manifests
remain immutable failed-pin records and are not restated as runtime
confirmations. This receipt is not USD admission for either grid, current assortment authority,
delivery-location proof, exact inventory, realized transaction price, sales,
demand, velocity, Cleaning, Silver, Judgment, buyer proof, monitoring readiness,
or commercial readiness. It does not infer `USD` from a dollar glyph. The older
Summer Fridays packet remains country-route-rejected because its preserved DOM
retains the dialog diagnostic marker. Re-run the supported route for any claim
that depends on current source state; evaluate country, currency, delivery, and
completeness as separate typed facts.
