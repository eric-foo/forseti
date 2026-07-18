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
- `UNKNOWN_REQUIRED_SIGNAL_ABSENT` means a live bound probe ran, but the
  commissioned retailer-owned confirmation signal was absent.
- A product's country of origin, a dollar glyph, a retailer hostname, or a
  working product capture is not a storefront, currency, or delivery pin.

## Current operating registry

| Retailer | Current capture route | Session posture | Storefront country | Currency | Delivery location | Last verified evidence | Limits and re-probe trigger |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Amazon US | Fresh anonymous CloakBrowser packet with `--delivery-zip 10001`; the runner requires the requested ZIP in a recognized Amazon location anchor plus an `amazon.com` US-marketplace marker on the final page. `currencyOfPreference=USD` is independent currency evidence, not ZIP proof. | Logged-out public; no stored profile, cookie injection, proxy, VPN, credential, or login. | `CONFIRMED_US` | `CONFIRMED_USD` | `CONFIRMED_ZIP_10001` | Discovery packet `01KXRP77TV6Q2GCG9DM27Z0VTP` confirmed the ZIP-plus-marketplace conjunction on 2026-07-17 UTC / 2026-07-18 Asia/Singapore. LipSoftie `01KXRPBRXVJJ4THQXW63BTV9R2` and SOS `01KXRPF84BA1AZNSVWDACNVSVV` independently preserved Amazon US/USD PDP state, but their historical USD-only confirmation notes do not prove the ZIP. | Each future packet repeats the retailer UI flow. A homepage/final marketplace redirect or missing final ZIP conjunction preserves `amazon_delivery_zip_pin_failed` evidence and exits nonzero; do not project or admit that packet as US delivery-pinned. Re-probe if selectors or confirmation anchors change. |
| Sephora | Anonymous CloakBrowser with `--sephora-market US` and requested `country_switch=us`; assertion-only confirmation requires `Sephora.renderQueryParams.country=US` plus a Sephora-sold JSON-LD `Offer` with `priceCurrency=USD`. Five-second settle and progressive review scroll remain available where required. | `logged_out_public`; no profile, storage state, proxy, VPN, geo-IP, cookie injection, credential, or login. | `CONFIRMED_US` | `CONFIRMED_USD` | `UNPINNED` | Tower 28 LipSoftie packet `01KXRZQJBKNKC91SXH2C7MKF1C`, captured 2026-07-17 UTC / 2026-07-18 Asia/Singapore with `pin_confirmed=true`; all four raw hashes and the availability-index manifest hash fresh-verified. | The URL switch is request intent, not proof; the rendered conjunction and final Sephora host decide admission. A missing or contradictory conjunction preserves `sephora_market_pin_failed` and exits nonzero. No delivery destination was established. |
| Ulta | Existing anonymous CloakBrowser `ulta_pdp_aggregate` profile on the canonical Night Shift PDP; no current market-pin flag is admitted. | `logged_out_public`; no profile, storage state, proxy, VPN, geo-IP, cookie injection, credential, or login. | `UNKNOWN_REQUIRED_SIGNAL_ABSENT` | `OBSERVED_USD_UNPINNED` | `UNPINNED` | Failed pin packet `01KXSSJBMN6T4Z480ZX1RHA3MB`, captured 2026-07-18 UTC with `pin_confirmed=false`; all four raw hashes and byte lengths fresh-verified. | The bound PDP retained SKU `2645443`, USD JSON-LD offers, price, and reviews, but rendered neither `window.__LOCALE__='en-US'` nor `data-locale="en_US"`. USD offer state alone is not a country/currency pin. Re-probe only after those commissioned signals reappear or the owner commissions a different retailer-owned conjunction. |
| Walmart | Existing direct-HTTP grid/PDP routes using `__NEXT_DATA__`; rendered route for review distribution. | Working route present; not reverified here. | `UNKNOWN_NOT_REVERIFIED` | `UNKNOWN_NOT_REVERIFIED` | `UNKNOWN_NOT_REVERIFIED` | Current capture profiles; no pin-proving lake receipt was re-read in this work unit. | Re-probe before geographic comparison or if `__NEXT_DATA__`/review rendering changes. |
| Target | Anonymous CloakBrowser with six-second settle, one scroll pass, and subject-specific sufficiency gates. | `logged_out_public` observed. | `OBSERVED_US_CONTEXT_UNPINNED` | `OBSERVED_USD_UNPINNED` | `OBSERVED_LOCATION_UNPINNED` | Naturium grid `01KXR815Q70AD0CSH3PT69KCYJ`; PDP `01KXR823YS3V5M9E01QXP71ETC`; both 2026-07-17. | The page displayed US-style Target context and USD offers, but packet pins were null. Re-probe only with an explicit retailer confirmation mechanism. |
| Nordstrom | Anonymous CloakBrowser with `--nordstrom-country US`; retailer country UI must yield selected US/USD plus shopper context `CountryCode=US`, `CurrencyCode=USD`, `IsInternationalShopping=false`. | `logged_out_public`; no profile, storage state, proxy, geo-IP, or credential. | `CONFIRMED_US` | `CONFIRMED_USD` | `UNPINNED` | Nécessaire PDP `01KXRBDXGG092NXVRKJWJFB5JB`; grid `01KXRBHKAA6D64K31BY54JKGJN`; both 2026-07-17 with `pin_confirmed=true`. | PDP still displayed `Shipping to 518225`. Re-probe if the country control or shopper-context signal changes; never infer US delivery from the storefront pin. |
| Luckyscent | Direct HTTP for the brand grid; anonymous CloakBrowser PDP with `--luckyscent-market US`, five-second settle, 500-pixel scroll steps, and four passes. The flag performs no mutation: it confirms one serialized storefront `i18n` object binds `country=US`, `market=market-us`, and `currency=USD`. | `logged_out_public`; no profile, storage state, proxy, geo-IP, cookie injection, credential, or login. | `CONFIRMED_US` | `CONFIRMED_USD` | `UNPINNED` | Bread and Roses US-market verification `01KXRG2C722GPTCVF6V8MFR4Y5`, captured 2026-07-17 UTC / 2026-07-18 Asia/Singapore with `pin_confirmed=true`; earlier grid `01KXRDAWN0DC727R66HMDDYJ2D` and PDP `01KXRDEEQX391STPRWH21RTSMA`. | Luckyscent exposes no country selector; the confirmed pin is its canonical default storefront market, not a mutated preference. `buyerCountry=SG` remained a separate origin-derived shopper signal, and no US delivery destination was established. Re-probe if the loader context structure or values change, `pin_confirmed` becomes false, or either route stops binding the commissioned subject. |

## Non-claims

This registry does not establish inventory depth, fulfillment availability,
realized transaction price, demand, velocity, revenue, sell-through, market
share, customer sentiment, monitoring readiness, or commercial readiness.
