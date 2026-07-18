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
- `UNKNOWN_REQUIRED_SIGNAL_SHAPE_MISMATCH` means a live bound probe exposed a
  related retailer-owned value, but not in the exact commissioned shape.
- `UNKNOWN_REQUIRED_ACCESS_BLOCKED` means a live bound probe preserved a
  retailer access-block response before the commissioned signal could be
  observed.
- A product's country of origin, a dollar glyph, a retailer hostname, or a
  working product capture is not a storefront, currency, or delivery pin.

## Current operating registry

| Retailer | Current capture route | Session posture | Storefront country | Currency | Delivery location | Last verified evidence | Limits and re-probe trigger |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Amazon US | Fresh anonymous CloakBrowser packet with `--delivery-zip 10001`; the runner requires the requested ZIP in a recognized Amazon location anchor plus an `amazon.com` US-marketplace marker on the final page. `currencyOfPreference=USD` is independent currency evidence, not ZIP proof. Direct network posture remains the first attempt. If that attempt preserves an Amazon Singapore redirect or SG marketplace state, one owner-authorized fallback may connect the pre-existing Surfshark app to its United States / New York route before repeating the same retailer UI flow and admission checks. | Logged-out public; no stored browser profile, cookie injection, capture credential, or login. Default attempt uses no proxy or VPN. The conditional Surfshark retry is allowed only after a typed SG result; preserve the failed pre-VPN packet and record the external VPN posture in the operator receipt without exposing account details. | `CONFIRMED_US` | `CONFIRMED_USD` | `CONFIRMED_ZIP_10001` | Discovery packet `01KXRP77TV6Q2GCG9DM27Z0VTP` confirmed the ZIP-plus-marketplace conjunction on 2026-07-17 UTC / 2026-07-18 Asia/Singapore. LipSoftie `01KXRPBRXVJJ4THQXW63BTV9R2` and SOS `01KXRPF84BA1AZNSVWDACNVSVV` independently preserved Amazon US/USD PDP state, but their historical USD-only confirmation notes do not prove the ZIP. Surfshark 6.13.0 availability was observed on 2026-07-19 Asia/Singapore with the app running but disconnected and the United States / New York route listed; no VPN-backed Amazon packet has yet been commissioned or admitted. | Each future packet repeats the retailer UI flow. A homepage/final marketplace redirect or missing final ZIP conjunction preserves `amazon_delivery_zip_pin_failed` evidence and exits nonzero; do not project or admit that packet as US delivery-pinned. VPN geography is transport posture, not pin evidence: even after the conditional retry, admission still requires Amazon-owned US marketplace, exact `USD`, and delivery ZIP `10001` signals in the final packet. Preserve both pre-VPN failure and post-VPN result. Re-probe if selectors, confirmation anchors, or marketplace behavior change. |
| Sephora | Anonymous CloakBrowser with `--sephora-market US` and requested `country_switch=us`; assertion-only confirmation requires `Sephora.renderQueryParams.country=US` plus a Sephora-sold JSON-LD `Offer` with `priceCurrency=USD`. Five-second settle and progressive review scroll remain available where required. | `logged_out_public`; no profile, storage state, proxy, VPN, geo-IP, cookie injection, credential, or login. | `CONFIRMED_US` | `CONFIRMED_USD` | `UNPINNED` | Tower 28 LipSoftie packet `01KXRZQJBKNKC91SXH2C7MKF1C`, captured 2026-07-17 UTC / 2026-07-18 Asia/Singapore with `pin_confirmed=true`; all four raw hashes and the availability-index manifest hash fresh-verified. | The URL switch is request intent, not proof; the rendered conjunction and final Sephora host decide admission. A missing or contradictory conjunction preserves `sephora_market_pin_failed` and exits nonzero. No delivery destination was established. |
| Ulta | Existing anonymous CloakBrowser `ulta_pdp_aggregate` profile on the canonical Night Shift PDP; no current market-pin flag is admitted. | `logged_out_public`; no profile, storage state, proxy, VPN, geo-IP, cookie injection, credential, or login. | `UNKNOWN_REQUIRED_SIGNAL_ABSENT` | `OBSERVED_USD_UNPINNED` | `UNPINNED` | Failed pin packet `01KXSSJBMN6T4Z480ZX1RHA3MB`, captured 2026-07-18 UTC with `pin_confirmed=false`; all four raw hashes and byte lengths fresh-verified. | The bound PDP retained SKU `2645443`, USD JSON-LD offers, price, and reviews, but rendered neither `window.__LOCALE__='en-US'` nor `data-locale="en_US"`. USD offer state alone is not a country/currency pin. Re-probe only after those commissioned signals reappear or the owner commissions a different retailer-owned conjunction. |
| Walmart | Existing anonymous Direct HTTP grid/PDP routes using `__NEXT_DATA__`; no current market-pin flag is admitted. | `logged_out_public`; explicit no-proxy opener, with no VPN, cookie injection, profile, credential, login, or delivery mutation. | `UNKNOWN_REQUIRED_SIGNAL_SHAPE_MISMATCH` | `OBSERVED_USD_UNPINNED` | `OBSERVED_LOCATION_UNPINNED` | Failed pin packet `01KXSV9HFFEPNEXVA407318KW1`, captured 2026-07-18 UTC with `pin_confirmed=false`; both raw hashes and byte lengths fresh-verified. | The bound item `2150828728`, exact `currencyUnit=USD`, and matching page/product postal `95829` were present. Immediate targeting serialized `countryCode=["US"]`, not the commissioned scalar `countryCode=="US"`. No country or currency pin was promoted, and postal `95829` remains origin-derived rather than operator-set. Re-probe only if the commissioned scalar appears or the owner explicitly commissions list-membership semantics. |
| Target | Anonymous CloakBrowser with six-second settle, one scroll pass, and subject-specific sufficiency gates; no current `--target-zip` route is admitted. | `logged_out_public`; no profile, storage state, proxy, VPN, geo-IP, cookie injection, credential, or login. | `OBSERVED_US_CONTEXT_UNPINNED` | `OBSERVED_USD_UNPINNED` | `OBSERVED_LOCATION_UNPINNED` | Naturium grid/PDP `01KXR815Q70AD0CSH3PT69KCYJ` / `01KXR823YS3V5M9E01QXP71ETC`; earlier split-signal packets `01KXRK26RMXSBSEGVP8BKRG9GX` / `01KXRKJNQZCMKM6ATV55B0AYG5`; current failed recovery grid `01KXSXGCKNJQCRKNPYDPY944HY`, captured 2026-07-18 UTC with all four raw hashes and byte lengths fresh-verified. | Shipping ZIP and store/pickup ZIP are independently labelled concepts: the earlier header showed shipping `10001` while store context remained `52404`. In the current bounded recovery, the public `#zip-code-id-btn` existed on the final page but could not be opened during pre-capture setup, even after a five-second render settle; the PDP was not attempted and the unproven route was removed. Re-probe only after the public control is interactable in the bounded setup or the owner commissions another retailer-owned mechanism. |
| Nordstrom | Anonymous CloakBrowser with `--nordstrom-country US`; retailer country UI must yield selected US/USD plus shopper context `CountryCode=US`, `CurrencyCode=USD`, `IsInternationalShopping=false`. | `logged_out_public`; no profile, storage state, proxy, geo-IP, or credential. | `CONFIRMED_US` | `CONFIRMED_USD` | `UNPINNED` | Nécessaire PDP `01KXRBDXGG092NXVRKJWJFB5JB`; grid `01KXRBHKAA6D64K31BY54JKGJN`; both 2026-07-17 with `pin_confirmed=true`. | PDP still displayed `Shipping to 518225`. Re-probe if the country control or shopper-context signal changes; never infer US delivery from the storefront pin. |
| Luckyscent | Direct HTTP for the brand grid; anonymous CloakBrowser PDP with `--luckyscent-market US`, five-second settle, 500-pixel scroll steps, and four passes. The flag performs no mutation: it confirms one serialized storefront `i18n` object binds `country=US`, `market=market-us`, and `currency=USD`. | `logged_out_public`; no profile, storage state, proxy, geo-IP, cookie injection, credential, or login. | `CONFIRMED_US` | `CONFIRMED_USD` | `UNPINNED` | Bread and Roses US-market verification `01KXRG2C722GPTCVF6V8MFR4Y5`, captured 2026-07-17 UTC / 2026-07-18 Asia/Singapore with `pin_confirmed=true`; earlier grid `01KXRDAWN0DC727R66HMDDYJ2D` and PDP `01KXRDEEQX391STPRWH21RTSMA`. | Luckyscent exposes no country selector; the confirmed pin is its canonical default storefront market, not a mutated preference. `buyerCountry=SG` remained a separate origin-derived shopper signal, and no US delivery destination was established. Re-probe if the loader context structure or values change, `pin_confirmed` becomes false, or either route stops binding the commissioned subject. |
| Kohl's | No current capture route is admitted. Packet-backed ordinary Direct HTTP and header-complete `anti_blocking_http` are exhausted on the commissioned PDP and policy surfaces; both produced typed access denial. Anonymous CloakBrowser also rendered Akamai `Access Denied` both cold and after a successful humanized homepage warm-up; the disproven warm-up adapter/CLI route was removed. Canonical/bare/mobile host variants, `/api/amp`, typeahead, and anonymous first-party app/config candidates were explored only as unpreserved scouting and carry no current operating verdict. | `logged_out_public`; no profile, storage state, cookie injection, credential, token, login, cart, or delivery mutation. No proxy was loaded because no registered US residential proxy profile was available. | `UNKNOWN_REQUIRED_ACCESS_BLOCKED` | `UNKNOWN_REQUIRED_ACCESS_BLOCKED` | `UNPINNED` | Direct PDP `01KXT0245PZBHZSYJHM5376BCA`; cold browser PDP `01KXT04HA0TT33RH7BAWQ38H58`; Direct FAQ `01KXT09ERZ6584J7M4J07WS706`; warmed policy/PDP `01KXT3432PEF0NXEZE0VWEWMMD` / `01KXT38WKZMXVMMY18CDX3SC66`; header-complete HTTP PDP/policy `01KXTZ76J5BGQJTEP2QDCZDYHY` / `01KXTZ77WYTPH15N1F8XNK87HC`; all captured 2026-07-18 UTC with requested/final URLs, raw SHA-256 values, and byte lengths fresh-verified. | `.com`, a dollar glyph, a search snippet, or a US proxy exit is not pin evidence. The packet-backed anonymous HTTP rungs are exhausted; the unpreserved scouting matrix is not. The remaining admissible experiments require new external state: a registered US residential profile with US geo-IP, `en-US`, and a US timezone; an entitled Kohl's affiliate feed; or an owner-approved paid provider. Any route still requires retailer-owned US policy evidence plus a separate bound product offer with exact `USD`; proxy geography alone remains insufficient. |

## Non-claims

This registry does not establish inventory depth, fulfillment availability,
realized transaction price, demand, velocity, revenue, sell-through, market
share, customer sentiment, monitoring readiness, or commercial readiness.
