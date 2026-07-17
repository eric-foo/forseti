# Retail/PDP Storefront Pin Registry v0

```yaml
retrieval_header_version: 1
artifact_role: Current operating registry for Retail/PDP storefront pins
scope: >
  Records the current retailer capture route and independently typed session,
  storefront-country, currency, and delivery-location pin state. It prevents a
  working capture route or observed page context from being misreported as a
  confirmed geographic or fulfillment pin.
use_when:
  - Selecting a known Retail/PDP capture route.
  - Checking which storefront dimensions were actually pinned for a retailer.
  - Locating the latest evidence and re-probe trigger for a retailer route.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/demand_durability_us_storefront_pin_recon_verdict_v0.md
  - docs/research/forseti_beauty_retailer_surface_probe_results_v0.md
stale_if:
  - A listed route, confirmation signal, packet, or retailer surface changes.
  - A later live receipt proves or disproves a pin dimension below.
  - The source-family route home or Source Capture Packet pin contract changes.
```

## Registry semantics

This is the thin current-operating lookup. The capture recon index remains the
historical evidence ledger, and retailer probe result artifacts remain the
claim-level page-state evidence.

Pin dimensions are independent:

- `CONFIRMED_*` requires an explicit retailer signal and a receipt-backed route.
- `OBSERVED_*_UNPINNED` records source-visible context without claiming the
  runner held it fixed.
- `UNKNOWN_NOT_REVERIFIED` means a capture route exists, but this work unit did
  not fresh-read a receipt proving that dimension.
- A product's country of origin, a dollar glyph, a retailer hostname, or a
  working product capture is not a storefront, currency, or delivery pin.

## Current operating registry

| Retailer | Current capture route | Session posture | Storefront country | Currency | Delivery location | Last verified evidence | Limits and re-probe trigger |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Amazon US | Anonymous CloakBrowser with `--delivery-zip 10001`; Amazon delivery widget confirmation plus PDP `currencyOfPreference=USD`. | Logged-out public. | `CONFIRMED_US` | `CONFIRMED_USD` | `CONFIRMED_ZIP_10001` | `demand_durability_us_storefront_pin_recon_verdict_v0.md`; `retail_pdp_sidecar_operator_playbook_v0.md` reports the 2026-06-16/17 sidecar smoke. No canonical lake receipt was re-read in this work unit. | Re-probe if the delivery widget selectors, displayed ZIP, or `currencyOfPreference` signal changes. |
| Sephora | Anonymous rendered Retail/PDP route; five-second settle and progressive review scroll where required. | Working route present; not reverified here. | `UNKNOWN_NOT_REVERIFIED` | `UNKNOWN_NOT_REVERIFIED` | `UNKNOWN_NOT_REVERIFIED` | Current capture profiles and sidecar operator playbook; no pin-proving lake receipt was re-read in this work unit. | Do not promote the working capture route into a geographic pin. Re-probe before geographic comparison. |
| Ulta | Existing rendered Retail/PDP profiles using JSON-LD and `__APOLLO_STATE__`. | Working route present; not reverified here. | `UNKNOWN_NOT_REVERIFIED` | `UNKNOWN_NOT_REVERIFIED` | `UNKNOWN_NOT_REVERIFIED` | Current capture profiles and sidecar operator playbook; no pin-proving lake receipt was re-read in this work unit. | Re-probe if Apollo substrate or page route changes; geographic comparison still needs explicit pin evidence. |
| Walmart | Existing direct-HTTP grid/PDP routes using `__NEXT_DATA__`; rendered route for review distribution. | Working route present; not reverified here. | `UNKNOWN_NOT_REVERIFIED` | `UNKNOWN_NOT_REVERIFIED` | `UNKNOWN_NOT_REVERIFIED` | Current capture profiles; no pin-proving lake receipt was re-read in this work unit. | Re-probe before geographic comparison or if `__NEXT_DATA__`/review rendering changes. |
| Target | Anonymous CloakBrowser with six-second settle, one scroll pass, and subject-specific sufficiency gates. | `logged_out_public` observed. | `OBSERVED_US_CONTEXT_UNPINNED` | `OBSERVED_USD_UNPINNED` | `OBSERVED_LOCATION_UNPINNED` | Naturium grid `01KXR815Q70AD0CSH3PT69KCYJ`; PDP `01KXR823YS3V5M9E01QXP71ETC`; both 2026-07-17. | The page displayed US-style Target context and USD offers, but packet pins were null. Re-probe only with an explicit retailer confirmation mechanism. |
| Nordstrom | Anonymous CloakBrowser with `--nordstrom-country US`; retailer country UI must yield selected US/USD plus shopper context `CountryCode=US`, `CurrencyCode=USD`, `IsInternationalShopping=false`. | `logged_out_public`; no profile, storage state, proxy, geo-IP, or credential. | `CONFIRMED_US` | `CONFIRMED_USD` | `UNPINNED` | Nécessaire PDP `01KXRBDXGG092NXVRKJWJFB5JB`; grid `01KXRBHKAA6D64K31BY54JKGJN`; both 2026-07-17 with `pin_confirmed=true`. | PDP still displayed `Shipping to 518225`. Re-probe if the country control or shopper-context signal changes; never infer US delivery from the storefront pin. |
| Luckyscent | Direct HTTP for the brand grid; anonymous CloakBrowser PDP with five-second settle, 500-pixel scroll steps, and four passes. | `logged_out_public`; no profile, storage state, proxy, geo-IP, cookie, credential, or login. | `UNKNOWN_CONFLICTING_CONTEXT` | `OBSERVED_USD_OFFER_UNPINNED` | `UNPINNED` | Pearfat grid `01KXRDAWN0DC727R66HMDDYJ2D`; Bread and Roses PDP `01KXRDEEQX391STPRWH21RTSMA`; both captured 2026-07-17 UTC / 2026-07-18 Asia/Singapore. | Grid state exposed a US market context alongside `buyerCountry=SG`; the PDP explicitly encoded USD offers but packet currency and locale pins remained null. Re-probe if either route stops binding the commissioned subject or the context signals converge under a retailer-controlled pin. |

## Non-claims

This registry does not establish inventory depth, fulfillment availability,
realized transaction price, demand, velocity, revenue, sell-through, market
share, customer sentiment, monitoring readiness, or commercial readiness.
