# Forseti Sephora Brand-Grid Capture Live Proof v0

```yaml
retrieval_header_version: 1
artifact_role: Research / implementation validation receipt
scope: >
  Records the bounded 2026-07-20 UTC live Summer Fridays Sephora brand-grid
  capture, typed view-only projection, raw-file integrity check, completeness
  reconciliation, and fail-closed US/USD market result.
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

`BLOCKED_GRID_USD_PIN_EXPLICIT_CODE_ABSENT`.

The supported runner preserved a complete 34-of-34 Summer Fridays parent-product
projection, then exited nonzero because the rendered Sephora grid exposed
retailer-owned `country=US` but no explicit selected currency code. Dollar
glyphs in price displays were not promoted to `USD`. The packet is therefore
not admitted as Sephora US/USD storefront evidence.

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

The command returned exit code `4` with
`sephora_market_pin_failed`; both the raw packet and initial `_01` projection
were preserved.

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

## Non-Claims

This receipt is not a Sephora US/USD-admitted packet, current assortment
authority, delivery-location proof, exact inventory, realized transaction
price, sales, demand, velocity, Cleaning, Silver, Judgment, buyer proof,
monitoring readiness, or commercial readiness. It does not infer `USD` from a
dollar glyph. Re-run the supported route for any claim that depends on current
source state; admit it as US/USD evidence only if the independent retailer-owned
country and explicit currency conjunction passes.
