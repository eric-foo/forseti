# Beauty Retailer Surface Probe Results v0

```yaml
retrieval_header_version: 1
artifact_role: Point-in-time beauty retailer surface probe results
scope: >
  Records bounded, subject-bound retailer page-state observations commissioned
  by the Beauty Retailer Surface Probe handoff. Target x Naturium, Nordstrom x
  Nécessaire, and Luckyscent x Pearfat Parfum are complete with their pin and
  projection limitations typed explicitly. Owner-authorized Tower 28 price,
  certification-directory, and diversion add-on reads are also recorded.
use_when:
  - Comparing public retailer assortment, offer, review, and claims surfaces for accepted beauty-pool companies.
  - Retrieving canonical packet locators and limits for the three completed probes and the Tower 28 add-on reads.
authority_boundary: evidence_register_only
open_next:
  - docs/workflows/forseti_capture_beauty_retailer_surface_probe_handoff_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_storefront_pin_registry_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_sidecar_operator_playbook_v0.md
stale_if:
  - A later capture supersedes a recorded point-in-time page state.
  - A recorded packet is unavailable or fails its preserved-file hash check.
```

## Execution status

| Sequence | Retailer x subject | Status |
| --- | --- | --- |
| 1 | Target x Naturium | `COMPLETE_POINT_IN_TIME_PROBE` |
| 2 | Nordstrom x Nécessaire | `COMPLETE_US_USD_STOREFRONT_DELIVERY_UNPINNED` |
| 3 | Luckyscent x Pearfat Parfum | `COMPLETE_POINT_IN_TIME_PROBE_CONTEXT_UNPINNED` |
| Add-on | Tower 28 price / certification / diversion reads | `COMPLETE_WITH_TYPED_AMAZON_MAKEWAVES_GAP` |

This artifact completes the three-retailer sequence and separately records the
owner-authorized Tower 28 add-on reads. The add-on used the existing Sephora
and Amazon US routes for its bound subjects; it did not begin the separate
Sephora storefront-pin reconciliation.

## Target x Naturium

### Method and preservation

- Retrieval date: `2026-07-17`
- Route: anonymous CloakBrowser through the existing Capture Spine runner,
  six-second settle and one scroll pass per supplied URL.
- Admission: not access-blocked; at least 1,000 visible-text bytes; literal
  Naturium binding; visible dollar price; PDP additionally required the bound
  Vitamin C Complex Serum title.
- The fixture-bound `target_*` capture profile was not used. The generic runner
  received subject-specific sufficiency checks instead.
- Existing local mechanical projections were run over the preserved packets:
  `retail_grid_mechanical_projection` for the brand grid and
  `retail_pdp_mechanical_projection` for the PDP. Both are view-only,
  not-cleaned, not-normalized, and not judgment-ready.
- Raw packets are canonical under `F:\forseti-data-lake`. Projection files were
  local validation artifacts, not a new lake schema or durable authority.
- The runner's normal viewport screenshot was preserved in each packet. No
  additional full-page screenshot was taken because layout was not the
  conclusion-bearing evidence.

### Capture receipts

#### Brand grid

- URL: `https://www.target.com/b/naturium/-/N-q643le8pm3h`
- Packet: `F:\forseti-data-lake\raw\8e5\01KXR815Q70AD0CSH3PT69KCYJ`
- Packet ID: `01KXR815Q70AD0CSH3PT69KCYJ`
- Slice capture time: `2026-07-17T14:34:59Z`
- Receipt generation time: `2026-07-17T14:35:03Z`
- Admission marker: `source_detail_sufficiency_passed`
- Warnings: none
- Preserved-file SHA-256:
  - rendered DOM: `bc4657727967ddbdd5703f6f4b7ac219ece4e1382d4ea2680a6189a800efa298`
  - visible text: `a8b313967cedf3ff85a1b9a2477a1451dfebf20fadd3811276c4a47a77ba5431`
  - viewport screenshot: `d95960268a26550e22c84cd2620d81c81e87df11b63e38a4b2a35f5aadfbe1af`
  - snapshot metadata: `cbdcdfd3d5407a7b6833cb0212ad206fd1672f42078dd94b5db68d3346e4ec51`

#### Bound PDP

- URL: `https://www.target.com/p/-/A-80184023`
- Packet: `F:\forseti-data-lake\raw\7d6\01KXR823YS3V5M9E01QXP71ETC`
- Packet ID: `01KXR823YS3V5M9E01QXP71ETC`
- Slice capture time: `2026-07-17T14:35:33Z`
- Receipt generation time: `2026-07-17T14:35:34Z`
- Admission marker: `source_detail_sufficiency_passed`
- Warnings: none
- Preserved-file SHA-256:
  - rendered DOM: `3729d4dd1d21c53104cbbff9022c05069ffee80eb25bae757b28d27b2cbc7ece`
  - visible text: `4f72f57f34e208054efc873f2af1caadb31fdfece5c4c9ce83521ddff561ba25`
  - viewport screenshot: `611dbe65c49838812db93340777da3482c77d9d5b6e0cc3ef30df9947d4be142`
  - snapshot metadata: `1097943a13dd25b5fea5d7a8be2cf19e431f732c9362af8dae8dd09eb1298cbd`

### SOBS-style observation rows

```yaml
observations:
  - observation_id: SOBS-TRG-001
    retailer: Target
    subject: Naturium
    url: https://www.target.com/b/naturium/-/N-q643le8pm3h
    retrieval_date: "2026-07-17"
    short_quote_or_summary: >
      The captured Target Naturium grid produced 24 raw-anchored product rows
      after one scroll pass. Visible prices ranged from $5.99 to $37.99 and
      visible average ratings ranged from 3.8 to 4.9.
    signal_stage: candidate_support
    claim_it_might_support: current visible Target assortment breadth and point-in-time price/reception dispersion for Naturium
    gate_role: none
    independence_hypothesis: retailer catalog state; independent of brand announcements in form, though assortment is a joint brand-retailer decision
    packet_locator: F:\forseti-data-lake\raw\8e5\01KXR815Q70AD0CSH3PT69KCYJ
    uncertainty_or_limits: >
      Twenty-four means tiles loaded in this bounded capture, not a certified
      full Target catalog count. Ratings and prices are page state, not demand,
      velocity, sell-through, productivity, or representative market performance.

  - observation_id: SOBS-TRG-002
    retailer: Target
    subject: Naturium
    url: https://www.target.com/p/-/A-80184023
    retrieval_date: "2026-07-17"
    short_quote_or_summary: >
      Target displayed Naturium Vitamin C Complex Serum 1 fl oz at $14.69,
      down from $17.89, labeled "New lower price" with $3.20 saved and an
      18% reduction. The mechanical offer row bound seller "Target".
    signal_stage: candidate_support
    claim_it_might_support: current Target offer and promotional price state for the bound Naturium SKU
    gate_role: none
    independence_hypothesis: retailer offer state
    packet_locator: F:\forseti-data-lake\raw\7d6\01KXR823YS3V5M9E01QXP71ETC
    uncertainty_or_limits: >
      Point-in-time online offer only. The capture inherited "Ship to 52404"
      page state but did not establish an operator-set location, locale, or
      currency pin. It does not establish historical pricing, nationwide
      availability, sales, or realized transaction price.

  - observation_id: SOBS-TRG-003
    retailer: Target
    subject: Naturium
    url: https://www.target.com/p/-/A-80184023
    retrieval_date: "2026-07-17"
    short_quote_or_summary: >
      Target displayed a 4.45/5 aggregate over 1,771 star ratings. The rendered
      review widget exposed a 5-to-1-star distribution of 74%, 11%, 5%, 3%,
      and 6%, plus 757 reviews matching the current widget filter.
    signal_stage: candidate_support
    claim_it_might_support: current retailer review substrate and rating dispersion for the bound Naturium SKU
    gate_role: none
    independence_hypothesis: aggregated customer contributions on one retailer platform; platform conventions and syndicated reviews may couple observations
    packet_locator: F:\forseti-data-lake\raw\7d6\01KXR823YS3V5M9E01QXP71ETC
    uncertainty_or_limits: >
      Target visibly labels 1,771 as reviews/star ratings, while the Capture
      Spine conservatively binds it as rating_count; a distinct written-review
      total was not observed. The page states that its review summary is
      AI-generated and includes incentivized reviews. Ratings are not demand,
      repeat purchase, sell-through, or representative customer sentiment.

  - observation_id: SOBS-TRG-004
    retailer: Target
    subject: Naturium
    url: https://www.target.com/p/-/A-80184023
    retrieval_date: "2026-07-17"
    short_quote_or_summary: >
      Target's PDP carried "At a glance" labels including Clean, Paraben Free,
      Cruelty Free, No Synthetic Fragrance, Plant Based, Gluten Free, Vegan,
      Contains Vitamin C, Contains Hyaluronic Acid, and Dermatologist Tested.
      Highlights said the serum helps improve the appearance of fine lines and
      wrinkles, helps skin look radiant and bright, and shields skin from
      environmental stressors; the description said the formula is clinically
      proven to improve the appearance of fine lines and wrinkles in four weeks.
    signal_stage: candidate_support
    claim_it_might_support: current claims language presented by Target for the bound Naturium SKU
    gate_role: none
    independence_hypothesis: retailer-hosted PDP copy; likely supplied by or coordinated with the brand and therefore not an independent efficacy source
    packet_locator: F:\forseti-data-lake\raw\7d6\01KXR823YS3V5M9E01QXP71ETC
    uncertainty_or_limits: >
      This records claims language, not substantiation or verified product
      performance. No underlying clinical study was retrieved or assessed.
```

### Projection residuals carried forward

- Grid rows did not observe a distinct written-review count, exact inventory
  quantity, sold units, selected variant, or a pinned location.
- PDP projection did not observe exact inventory quantity, sold units, or a
  distinct written-review count.
- The PDP projection collapsed two cart/notify chrome matches while retaining
  the bound variant-availability row; this is recorded in its loss ledger.
- No top-level grid projection residual was emitted; all 24 rows retained raw
  DOM anchors to the preserved packet.

## Nordstrom x Nécessaire

### Method and typed outcome

- Retrieval date: `2026-07-17`
- Direct HTTP was attempted first for the brand grid and bound PDP. Both
  requests returned HTTP 200 and preserved non-empty bodies, but neither body
  exposed the commissioned brand, product, price, review, or claims fields.
  They are retained as `HTTP_200_CONTENT_INSUFFICIENT` controls.
- Each insufficient surface then received its single permitted anonymous
  CloakBrowser attempt with a five-second settle and one scroll pass.
- Both rendered packets passed their subject-specific brand/price admission
  gates, but the visible session was `Singapore` with `SGD` pricing. Locale,
  currency, and session-location pins remained null.
- That initial outcome remains `PARTIAL_LOCALE_DRIFT`: it is a dated control,
  not a US/USD comparison.
- An owner-commissioned no-proxy diagnostic supplement then used Nordstrom's
  own country-preference UI before main-page navigation. Confirmation required
  rendered `selectedCountryCode=US`, `selectedCurrencyCode=USD`, and shopper
  context `CountryCode=US`, `CurrencyCode=USD`,
  `IsInternationalShopping=false`; dollar glyphs and `nordcountrycode=US`
  alone were explicitly insufficient.
- The first durable diagnostic control failed to open the country control and
  honestly remained Singapore/SGD. After binding the measured header flag
  control, five-second homepage render allowance, and post-Save navigation
  barrier, both the bound PDP and brand grid passed their subject/price gates
  with `pin_confirmed=true`.
- Current outcome: `US_USD_STOREFRONT_CONFIRMED_DELIVERY_LOCATION_UNPINNED`.
  No proxy, stored profile, storage state, raw-cookie injection, geo-IP mode,
  or credential was used. The PDP still displayed `Shipping to 518225`, so
  this evidence does not establish a US delivery destination or fulfillment
  promise.
- No Nordstrom retailer adapter or projection schema expansion was added.

### Capture receipts

| Surface | Method and outcome | Packet and capture time | Preserved-file SHA-256 |
| --- | --- | --- | --- |
| Brand grid | Direct HTTP; `HTTP_200_CONTENT_INSUFFICIENT` | `F:\forseti-data-lake\raw\dce\01KXR970GGKWDYFNFHZPRP0SPJ`; `2026-07-17T14:55:41Z` | body `ed78d2123dc301bb584d536e9448921ded79df152441e32445dbedd720612678`; metadata `b11b347e900f9034912d5d773352a73ddf3a456d0f5b236c56edb62c7159b384` |
| Bound PDP | Direct HTTP; `HTTP_200_CONTENT_INSUFFICIENT` | `F:\forseti-data-lake\raw\7c3\01KXR97J3F219RHS9BZRVDC9DG`; `2026-07-17T14:56:00Z` | body `42fd589bfd9c306ba70fc2d2c8cef93ea7bb0fc431d4907e14999c24245972ff`; metadata `429d34ca704af5e221d220179f51cc7af7034532e3f7a9353b8973a5676cdf7f` |
| Brand grid | CloakBrowser; subject gate passed, Singapore/SGD drift | `F:\forseti-data-lake\raw\830\01KXR9ARJSA3HRRA6HEWF9C9VB`; `2026-07-17T14:57:44Z` | DOM `0f5db0bac62939fcf697d2145f4f12349783d9aae21eb9fd15537dd006a55e6c`; text `707d2340b8900e368397c1936839a44d196d088945dca753de918692eacc7bc2`; screenshot `104e109debe14364396d5d603f88501b732b44aebeff5fd7615131b6532d6953`; metadata `7acccafdaf16127b34bb0d4c768d22b09423a79f5f33c656fba8d0d78b2a9d57` |
| Bound PDP | CloakBrowser; subject gate passed, Singapore/SGD drift | `F:\forseti-data-lake\raw\194\01KXR9BNWBP8R8XKPKFJHZJTPN`; `2026-07-17T14:58:14Z` | DOM `c562e9083cfb44f3d7ead4e3683eeea00e6a96edea5fdb29b6724ff848921218`; text `7b27e3bf82b298dd8e8ae769a2cb76a6e12ee9f1e3bc034e603a46dc7e8e4997`; screenshot `445c1672c2deba00f80904280cacb077b3092da6ff4df75d5d8891adef045f5f`; metadata `a900d36a7c908befc4982a8d6c10684f8d9b13d2d5f64cb4760be1bb8293cfa4` |
| Bound PDP pin diagnostic control | CloakBrowser; country-control open failed, pin unconfirmed, Singapore/SGD retained | `F:\forseti-data-lake\raw\90f\01KXRAWC09HS9GP7AAF7BBB8DW`; `2026-07-17T15:24:51Z` | DOM `0dcd9cc1157c5b46341bc311d817c8e67623a4129e92593045a0142f04eff2da`; text `54ade94843d94d7186c91621f3484909d16f5fe6eb750a9040a5adb0b0863090`; screenshot `a3330afc612821baae7f25e01ef697b4973846feaa853aadb91a1837d79c5fd3`; metadata `8520beda3b397ed7baa2ac1224d969bfa24a3096f921abcaf86885b3beb014ad` |
| Bound PDP US supplement | CloakBrowser; US/USD pin confirmed and subject/price gate passed | `F:\forseti-data-lake\raw\9df\01KXRBDXGG092NXVRKJWJFB5JB`; `2026-07-17T15:34:26Z` | DOM `1f1388d3497b4576690cc3b593797d229374e82eb291ed9cd38e88ba8290107d`; text `81f79bd0d2420ba41391c0683c77f206bd875717940c739bd5c2e04c493f39a2`; screenshot `8c32c91ef457d028c61c596acfa23b34d4f3fbca0b950a6e01fa55f3a1dbafbb`; metadata `bc0c5d81ea36b320681431cfdb3436e236ed4b9c0d7d045c58c053195db233a5` |
| Brand grid US supplement | CloakBrowser; US/USD pin confirmed and subject/price gate passed | `F:\forseti-data-lake\raw\af6\01KXRBHKAA6D64K31BY54JKGJN`; `2026-07-17T15:36:27Z` | DOM `81e286cc91781236110e97369db91568c6c8cb2862a45c76dab4ce753a2c63a8`; text `36bf4194ac264a2024479e3531ae251235befa907b6f9fa0c4bbf37d099b1d76`; screenshot `1493fa6aa3943fde1a4b1897c8ce45e0dd7918055189ab952a84d8ea12700934`; metadata `1c3d4724c273d636727fdbc26c4ca408da18c02d0cfc8a163d3df93a5493327b` |

The two successful US manifests had zero warnings at fresh read. Both recorded
`proxy_used=false`, `persistent_profile_loaded=false`,
`storage_state_loaded=false`, `geoip_used=false`, and `pin_confirmed=true`.
Their source-detail sufficiency gates passed. This does not retroactively
upgrade the direct-HTTP controls or the earlier Singapore packets.

### SOBS-style observation rows

```yaml
observations:
  - observation_id: SOBS-NDS-001
    retailer: Nordstrom
    subject: Nécessaire
    url: https://www.nordstrom.com/browse/beauty?filterByBrand=necessaire
    retrieval_date: "2026-07-17"
    short_quote_or_summary: >
      Nordstrom's rendered brand grid visibly stated "34 items" and exposed
      34 Nécessaire product tiles spanning body care, hair care, hand care,
      lip care, deodorant, fragrance, and sets. Visible SGD prices ranged from
      SGD 19.92 to SGD 86.33; rated tiles ranged from 3.8 to 5.0.
    signal_stage: candidate_support
    claim_it_might_support: current visible Nordstrom assortment breadth and point-in-time price/reception dispersion for Nécessaire
    gate_role: none
    independence_hypothesis: retailer catalog state; independent of brand announcements in form, though assortment is a joint brand-retailer decision
    packet_locator: F:\forseti-data-lake\raw\830\01KXR9ARJSA3HRRA6HEWF9C9VB
    uncertainty_or_limits: >
      The page was rendered for Singapore in SGD, not pinned US/USD. The
      item count is a bounded page-state observation, not demand, velocity,
      sell-through, productivity, or market performance.

  - observation_id: SOBS-NDS-002
    retailer: Nordstrom
    subject: Nécessaire
    url: https://www.nordstrom.com/s/the-lip-balm/8260802
    retrieval_date: "2026-07-17"
    short_quote_or_summary: >
      Nordstrom displayed Nécessaire The Lip Balm, One Size, at current price
      SGD 37.19 with an Add to Bag control.
    signal_stage: candidate_support
    claim_it_might_support: current Nordstrom Singapore offer state for the bound Nécessaire PDP
    gate_role: none
    independence_hypothesis: retailer-hosted offer state
    packet_locator: F:\forseti-data-lake\raw\194\01KXR9BNWBP8R8XKPKFJHZJTPN
    uncertainty_or_limits: >
      This is not a US/USD price. No separate seller-of-record label was
      visible; Nordstrom hosted the PDP and bag control, but seller identity
      is not promoted beyond that observation. No historical or realized
      transaction price is established.

  - observation_id: SOBS-NDS-003
    retailer: Nordstrom
    subject: Nécessaire
    url: https://www.nordstrom.com/s/the-lip-balm/8260802
    retrieval_date: "2026-07-17"
    short_quote_or_summary: >
      The Lip Balm displayed 4.6/5 across 118 reviews. The visible 5-to-1-star
      distribution was 81%, 7%, 3%, 5%, and 3%, respectively.
    signal_stage: candidate_support
    claim_it_might_support: current Nordstrom review substrate and rating dispersion for the bound Nécessaire SKU
    gate_role: none
    independence_hypothesis: aggregated customer contributions on one retailer platform; at least one visible critical review was labeled "Reposted from Nécessaire"
    packet_locator: F:\forseti-data-lake\raw\194\01KXR9BNWBP8R8XKPKFJHZJTPN
    uncertainty_or_limits: >
      Percentages sum to 99% because of source rounding. Syndicated/reposted
      reviews reduce source independence. Ratings and counts are not demand,
      repeat purchase, sell-through, or representative customer sentiment.

  - observation_id: SOBS-NDS-004
    retailer: Nordstrom
    subject: Nécessaire
    url: https://www.nordstrom.com/s/the-lip-balm/8260802
    retrieval_date: "2026-07-17"
    short_quote_or_summary: >
      Nordstrom described the balm as instant relief for dry, chapped, or
      compromised lips and carried claims for essential ceramides,
      niacinamide, hyaluronic acid, omega 6/9, centella asiatica, and shea
      butter to help repair dryness and soothe chapped lips. It also displayed
      cruelty-free, hypoallergenic, dermatologist-tested, noncomedogenic,
      B Corp, and Nordstrom Responsible Brands language.
    signal_stage: candidate_support
    claim_it_might_support: current claims language presented by Nordstrom for the bound Nécessaire PDP
    gate_role: none
    independence_hypothesis: retailer-hosted PDP copy; likely supplied by or coordinated with the brand and therefore not an independent efficacy source
    packet_locator: F:\forseti-data-lake\raw\194\01KXR9BNWBP8R8XKPKFJHZJTPN
    uncertainty_or_limits: >
      This records claims language, not substantiation, certification audit,
      ingredient stability, or verified product performance.

  - observation_id: SOBS-NDS-005
    retailer: Nordstrom
    subject: Nécessaire
    url: https://www.nordstrom.com/browse/beauty?filterByBrand=necessaire
    retrieval_date: "2026-07-17"
    short_quote_or_summary: >
      In a confirmed US/USD storefront, Nordstrom displayed "34 items" for
      Nécessaire. Visible current and sale prices included The Lip Duo at sale
      price $39, The Body Lotion at sale price $41.60 and after-sale price $52,
      The Lip Balm at $28, and other visible offers from $15 to $65.
    signal_stage: candidate_support
    claim_it_might_support: current visible US Nordstrom assortment breadth and point-in-time price/promotion state for Nécessaire
    gate_role: none
    independence_hypothesis: retailer catalog state; independent of brand announcements in form, though assortment is a joint brand-retailer decision
    packet_locator: F:\forseti-data-lake\raw\af6\01KXRBHKAA6D64K31BY54JKGJN
    uncertainty_or_limits: >
      The count and prices are current rendered page state, not inventory
      depth, realized transaction price, demand, velocity, sell-through,
      productivity, or market performance. Delivery location was not pinned.

  - observation_id: SOBS-NDS-006
    retailer: Nordstrom
    subject: Nécessaire
    url: https://www.nordstrom.com/s/the-lip-balm/8260802
    retrieval_date: "2026-07-17"
    short_quote_or_summary: >
      In a confirmed US/USD storefront, Nordstrom displayed Nécessaire The Lip
      Balm, One Size, at current price $28.00, with "Sold by Nordstrom" and an
      Add to Bag control.
    signal_stage: candidate_support
    claim_it_might_support: current US Nordstrom offer and seller state for the bound Nécessaire PDP
    gate_role: none
    independence_hypothesis: retailer-hosted offer state
    packet_locator: F:\forseti-data-lake\raw\9df\01KXRBDXGG092NXVRKJWJFB5JB
    uncertainty_or_limits: >
      The page also said "Shipping to 518225"; the US/USD storefront pin does
      not establish a US delivery location, available inventory quantity, or
      realized transaction price.

  - observation_id: SOBS-NDS-007
    retailer: Nordstrom
    subject: Nécessaire
    url: https://www.nordstrom.com/s/the-lip-balm/8260802
    retrieval_date: "2026-07-17"
    short_quote_or_summary: >
      The confirmed-US PDP displayed 4.6/5 across 118 reviews. The visible
      5-to-1-star distribution was 81%, 7%, 3%, 5%, and 3%, respectively.
    signal_stage: candidate_support
    claim_it_might_support: current Nordstrom review substrate and rating dispersion for the bound Nécessaire SKU
    gate_role: none
    independence_hypothesis: aggregated customer contributions on one retailer platform; at least one visible critical review was labeled "Reposted from Nécessaire"
    packet_locator: F:\forseti-data-lake\raw\9df\01KXRBDXGG092NXVRKJWJFB5JB
    uncertainty_or_limits: >
      Percentages sum to 99% because of source rounding. Syndicated/reposted
      reviews reduce source independence. Ratings and counts are not demand,
      repeat purchase, sell-through, or representative customer sentiment.

  - observation_id: SOBS-NDS-008
    retailer: Nordstrom
    subject: Nécessaire
    url: https://www.nordstrom.com/s/the-lip-balm/8260802
    retrieval_date: "2026-07-17"
    short_quote_or_summary: >
      The confirmed-US PDP described the balm as instant relief for dry,
      chapped, or compromised lips and carried claims for essential ceramides,
      niacinamide, hyaluronic acid, omega 6/9, centella asiatica, and shea
      butter to help repair dryness and soothe chapped lips. It also displayed
      cruelty-free, hypoallergenic, B Corp, and Nordstrom Responsible Brands
      language.
    signal_stage: candidate_support
    claim_it_might_support: current claims language presented by Nordstrom for the bound Nécessaire PDP
    gate_role: none
    independence_hypothesis: retailer-hosted PDP copy; likely supplied by or coordinated with the brand and therefore not an independent efficacy source
    packet_locator: F:\forseti-data-lake\raw\9df\01KXRBDXGG092NXVRKJWJFB5JB
    uncertainty_or_limits: >
      This records claims language, not substantiation, certification audit,
      ingredient stability, or verified product performance.
```

### Projection and remaining Nordstrom boundaries

- The hash-verified PDP projection was appended at
  `F:\forseti-data-lake\derived\9df\01KXRBDXGG092NXVRKJWJFB5JB\projection_retail_pdp\01KXRBFPNMYZGQQP654RYEP7RQ.json`.
  It retained raw JSON-LD anchoring Nécessaire, The Lip Balm, USD `28.00`, and
  `InStock`, and emitted the mechanical SKU/variant-price binding.
- The hash-verified grid projection was appended at
  `F:\forseti-data-lake\derived\af6\01KXRBHKAA6D64K31BY54JKGJN\projection_retail_pdp\01KXRBJ71B5SPNT9K98WED3DHK.json`.
- The existing projection enum does not include Nordstrom, so both projections
  type the retailer as `unknown`. The grid projector did not mechanically bind
  its visible product-tile prices and emitted
  `variant_offer_absent`; the PDP projector emitted
  `review_substrate_absent`. These are explicit projection gaps, not absence
  claims about the rendered source.
- The US/USD storefront is confirmed, but the delivery destination remains
  unpinned. No US shipping, pickup, inventory, or fulfillment conclusion is
  supported.

## Luckyscent x Pearfat Parfum

### Method and typed outcome

- Retrieval date: `2026-07-18` Asia/Singapore (`2026-07-17` UTC capture time).
- The Pearfat Parfum brand grid used the cheapest known route: one Direct HTTP
  capture. HTTP 200 preserved 150,809 body bytes and bound nine distinct
  Pearfat product handles plus source-visible `$5` and `$120` price tokens.
- The bound Bread and Roses PDP used the established anonymous rendered route:
  five-second settle, 500-pixel progressive scroll steps, and four scroll
  passes. No proxy, stored profile, storage state, cookies, credentials, login,
  or geo-IP mode was used.
- PDP admission required no access block, at least 1,000 visible-text bytes,
  exact Pearfat Parfum and Bread and Roses bindings, a visible price, and a
  non-zero rating/review aggregate. The packet passed
  `source_detail_sufficiency_passed`.
- Initial probe outcome: `COMPLETE_POINT_IN_TIME_PROBE_CONTEXT_UNPINNED`. The grid
  embedded a US market context alongside `buyerCountry=SG`; the PDP explicitly
  encoded USD offers, but locale and currency pins remained null and no
  delivery destination was established. The later US-market verification below
  supersedes only the storefront-country and currency status; it does not
  rewrite the initial packet or establish a delivery destination.
- No Luckyscent adapter, retail-grid projection, public API, schema, crawler,
  monitoring surface, Judge.me expansion, or extra full-page screenshot was
  added.

### Capture receipts

#### Brand grid

- URL: `https://www.luckyscent.com/brands/pearfat-parfum`
- Packet: `F:\forseti-data-lake\raw\416\01KXRDAWN0DC727R66HMDDYJ2D`
- Packet ID: `01KXRDAWN0DC727R66HMDDYJ2D`
- Capture time: `2026-07-17T16:07:43Z`
- Receipt generation time: `2026-07-17T16:07:44Z`
- Access: HTTP 200, final URL matched the requested URL
- Warnings: none
- Preserved-file SHA-256:
  - HTTP body: `08f2d4e8e9d716c562e18814597149a05ca259bab1841d2a4a8eeef996544b1d`
  - HTTP metadata: `40087ca204e7846417a559796b02e06f02bf1c5b5fdd7a5a29f05b45067709ad`

#### Bound PDP

- URL: `https://www.luckyscent.com/products/bread-and-roses-by-pearfat-parfum`
- Packet: `F:\forseti-data-lake\raw\f31\01KXRDEEQX391STPRWH21RTSMA`
- Packet ID: `01KXRDEEQX391STPRWH21RTSMA`
- Capture time: `2026-07-17T16:09:40Z`
- Receipt generation time: `2026-07-17T16:09:41Z`
- Admission marker: `source_detail_sufficiency_passed`
- Access classification: `no_block_marker`
- Route flags: settle `5.0` seconds, scroll step `500` pixels, four passes
- Warnings: none
- Preserved-file SHA-256:
  - rendered DOM: `abc4ebe05a1983f02e4104e75cf40fc7c18f0512acb5e187b78faf60afe9b802`
  - visible text: `407ce559917a90a3c372fa5c9e09047f7c5b0cbb4431f50cb4a19a6c0001523e`
  - viewport screenshot: `9f7c984511c06d6a9bf299286ee8cb4d0ac47ba547ba374ac63c995a53300da0`
  - snapshot metadata: `c99e60da6b3cd362901f9ddd2eadc131d0a96e340ba917b7fff767751ee66d35`

### SOBS-style observation rows

```yaml
observations:
  - observation_id: SOBS-LSC-001
    retailer: Luckyscent
    subject: Pearfat Parfum
    url: https://www.luckyscent.com/brands/pearfat-parfum
    retrieval_date: "2026-07-18"
    short_quote_or_summary: >
      The preserved Luckyscent brand grid bound nine distinct Pearfat Parfum
      products: Up North, Knee High, Sister Hildegard, Bread and Roses,
      Stomped on Bed of Lettuce, Rabbit Rabbit, Multiball, Amicus Cumulus,
      and 2030 Park Avenue. Each grid offer exposed a $5-to-$120 range.
    signal_stage: candidate_support
    claim_it_might_support: current visible Luckyscent assortment breadth and point-in-time offer range for Pearfat Parfum
    gate_role: none
    independence_hypothesis: retailer catalog state; independent of brand announcements in form, though assortment is a joint brand-retailer decision
    packet_locator: F:\forseti-data-lake\raw\416\01KXRDAWN0DC727R66HMDDYJ2D
    uncertainty_or_limits: >
      The nine products are the bounded served grid state, not inventory depth,
      historical assortment, realized price, demand, velocity, sell-through,
      revenue, productivity, or market performance.

  - observation_id: SOBS-LSC-002
    retailer: Luckyscent
    subject: Pearfat Parfum
    url: https://www.luckyscent.com/products/bread-and-roses-by-pearfat-parfum
    retrieval_date: "2026-07-18"
    short_quote_or_summary: >
      Luckyscent displayed Bread and Roses with Add to Cart and Online Only
      state. Structured product data bound three in-stock variants sold by
      Luckyscent: 50ml at USD 120, 15ml at USD 45, and 1ml spray at USD 5.
    signal_stage: candidate_support
    claim_it_might_support: current Luckyscent offer, variant, seller, and availability state for the bound Pearfat PDP
    gate_role: none
    independence_hypothesis: retailer-hosted offer state
    packet_locator: F:\forseti-data-lake\raw\f31\01KXRDEEQX391STPRWH21RTSMA
    uncertainty_or_limits: >
      USD is explicit offer data, but the packet currency pin is null. InStock
      and Add to Cart do not establish inventory quantity, delivery to a
      particular location, or realized transaction price.

  - observation_id: SOBS-LSC-003
    retailer: Luckyscent
    subject: Pearfat Parfum
    url: https://www.luckyscent.com/products/bread-and-roses-by-pearfat-parfum
    retrieval_date: "2026-07-18"
    short_quote_or_summary: >
      The PDP displayed a rounded 3.8 rating with 8 reviews; the Customer
      Reviews section and structured data reported 3.75 out of 5 across 8
      reviews. Progressive scrolling exposed all eight dated review bodies.
    signal_stage: candidate_support
    claim_it_might_support: current Luckyscent review substrate and rating state for Bread and Roses
    gate_role: none
    independence_hypothesis: customer-contributed rows on one retailer platform; purchaser verification and representativeness were not established
    packet_locator: F:\forseti-data-lake\raw\f31\01KXRDEEQX391STPRWH21RTSMA
    uncertainty_or_limits: >
      The 3.8 versus 3.75 difference is source display rounding. Eight reviews
      are a small, mutable platform sample and are not demand, repeat purchase,
      review velocity, representative sentiment, or product-performance proof.

  - observation_id: SOBS-LSC-004
    retailer: Luckyscent
    subject: Pearfat Parfum
    url: https://www.luckyscent.com/products/bread-and-roses-by-pearfat-parfum
    retrieval_date: "2026-07-18"
    short_quote_or_summary: >
      Luckyscent presented Bread and Roses as an Eau de Parfum centered on
      fresh baguette, sweet orange, red rose petals, cocoa, nutmeg, and
      labdanum, and classified it across floral, spicy-floral, gourmand,
      resinous/balsamic, and spicy styles.
    signal_stage: candidate_support
    claim_it_might_support: current descriptive and claims language presented by Luckyscent for the bound Pearfat PDP
    gate_role: none
    independence_hypothesis: retailer-hosted PDP copy; likely supplied by or coordinated with the brand and therefore not independent product-performance evidence
    packet_locator: F:\forseti-data-lake\raw\f31\01KXRDEEQX391STPRWH21RTSMA
    uncertainty_or_limits: >
      This records retailer-presented fragrance description and classification,
      not ingredient verification, blind-smell validation, claim
      substantiation, or verified consumer experience.
```

### Projection and remaining Luckyscent boundaries

- The hash-verified PDP projection was appended at
  `F:\forseti-data-lake\derived\f31\01KXRDEEQX391STPRWH21RTSMA\projection_retail_pdp\01KXRDHCMGCP1Z812715G33YSB.json`.
- It retained raw JSON-LD anchoring Pearfat Parfum, Bread and Roses, aggregate
  rating `3.75` across `8` reviews, and the 50ml variant at USD `120.0` with
  `InStock` availability.
- The existing projection enum does not include Luckyscent, so rows type the
  retailer as `unknown`. It emitted `review_substrate_absent` despite the eight
  rendered review rows and projected only the first of three source-visible
  variants. Cart chrome collapse also made `structure_preserved=false`. These
  are explicit projection gaps, not absence claims about the rendered source.
- No retail-grid projection was run because the existing grid projector is
  explicitly scoped to Walmart and Target. The brand-grid observation was
  validated directly against the preserved HTTP body.
- In this initial packet, USD offer encoding was explicit, while storefront
  country, packet currency pin, and delivery destination remained unpinned.
  The later verification below confirms the storefront context independently;
  the initial packet remains unchanged.

### US storefront pin verification

- Verification date: `2026-07-18` Asia/Singapore (`2026-07-17` UTC capture
  time).
- Luckyscent exposes no country selector. Requests to `/en-us`, `/us`, and
  `?country=US` canonicalized to the same unprefixed product route and did not
  change the separate `buyerCountry=SG` signal. No undocumented cart mutation
  was used to manufacture a country result.
- `run_source_capture_cloakbrowser_packet.py --luckyscent-market US` therefore
  performs no preference mutation. It confirms the retailer's canonical
  default storefront only when one serialized `i18n` loader object binds all
  three values together: `country=US`, `market=market-us`, and `currency=USD`.
  Loose dollar glyphs, product-offer currency, and `buyerCountry` do not
  satisfy the check.
- The fresh Bread and Roses capture reused the anonymous five-second settle,
  500-pixel scroll steps, and four-pass route. It passed the subject, price,
  review, and access-block admission checks and recorded
  `pin_confirmed=true`.
- Outcome:
  `US_USD_DEFAULT_STOREFRONT_CONFIRMED_DELIVERY_LOCATION_UNPINNED`.
  `buyerCountry=SG` remains a distinct origin-derived shopper signal; no US
  shopper origin, shipping address, inventory location, or delivery
  destination is claimed.

#### Verification receipt

- URL:
  `https://www.luckyscent.com/products/bread-and-roses-by-pearfat-parfum`
- Packet:
  `F:\forseti-data-lake\raw\1c3\01KXRG2C722GPTCVF6V8MFR4Y5`
- Packet ID: `01KXRG2C722GPTCVF6V8MFR4Y5`
- Capture time: `2026-07-17T16:55:31Z`
- Receipt generation time: `2026-07-17T16:55:31Z`
- Admission marker: `source_detail_sufficiency_passed`
- Access classification: `no_block_marker`
- Pin metadata:
  `pre_capture=luckyscent_us_market_assertion`,
  `market_preference_action=none_default_market_assertion`,
  `country_code_requested=US`, `currency_code_requested=USD`,
  `pin_confirmed=true`
- Access posture: no proxy, geo-IP, stored profile, storage state, credential,
  login, or cookie injection.
- Warnings: none
- Preserved-file SHA-256:
  - rendered DOM:
    `c4f6ae538a141ec7351e597ac7e4e304c0e5584494b698036ca733571d8f4b78`
  - visible text:
    `407ce559917a90a3c372fa5c9e09047f7c5b0cbb4431f50cb4a19a6c0001523e`
  - viewport screenshot:
    `9f7c984511c06d6a9bf299286ee8cb4d0ac47ba547ba374ac63c995a53300da0`
  - snapshot metadata:
    `4190247c38916c71e0e5c5383e1145276d87a3cd69a5c9c6ad4921455724ed54`

## Tower 28 subject-bound add-on reads

### Method, preservation, and admission

- Owner authorization date: `2026-07-18` Asia/Singapore. Capture timestamps
  below are `2026-07-17` UTC.
- Price-ladder subjects: LipSoftie Lip Treatment, MakeWaves Mascara, and SOS
  Rescue Spray. Tower 28 DTC pages were preserved by Direct HTTP; their three
  bound Sephora US PDPs were preserved through anonymous CloakBrowser with a
  five-second settle, progressive scrolling, and fail-closed subject, price,
  Auto-Replenish, and access checks.
- This was an ordinary-operation shelf read. No event code, first-order code,
  account, login, stored profile, cookie injection, proxy, or cart interaction
  was used. Displayed shelf, bundle, and recurring-plan allocations are kept
  distinct.
- The certification read used Tower 28's captured PDP claims, PETA's own
  company page and directory PDF, and Leaping Bunny's own directory form and
  exact `title=Tower28 Beauty` query. Third-party trackers were not cited.
- The diversion read re-preserved Tower 28's stores page because its
  conclusion-bearing authorized-channel and anti-diversion wording met the
  handoff's preservation trigger. Amazon discovery and PDPs used the existing
  anonymous ZIP `10001` route. Two PDPs confirmed the US pin; MakeWaves
  redirected to Amazon Singapore and is a typed gap.
- All 17 manifests and receipts were fresh-read after capture. Every packet ID
  matched its directory, every receipt carried that ID, and every preserved
  file matched its manifest SHA-256 and byte length.

### Price-ladder arithmetic

All prices are displayed USD page state. Percent differences use the DTC
single-purchase unit price as the base unless stated otherwise.

| SKU and compared size | DTC single | DTC recurring allocation | DTC bundle / larger state | Sephora US shelf | Sephora Auto-Replenish |
| --- | --- | --- | --- | --- | --- |
| LipSoftie, 11 g / 0.38 oz | `$16 / 11 g = $1.45/g` | `$14.40 / 11 g = $1.31/g`; `(16 - 14.40) / 16 = 10%` | Duo: `$30 / 2 = $15 each`, `$30 / 22 g = $1.36/g`, `6.25%` below single. Four-set: `$56 / 4 = $14 each`, `$56 / 44 g = $1.27/g`, `12.5%` below single. | `$16 / 11 g = $1.45/g`; no package-price divergence from DTC single | `$15.20 / 11 g = $1.38/g`; `5%` below shelf |
| MakeWaves, nominal 0.29 fl oz | DTC labels `8.5 mL`; `$20 / 8.5 = $2.35/mL` | `$18 / 8.5 = $2.12/mL`; `10%` below DTC single | Two 8.5 mL full sizes plus one 5 mL mini: `$44 / 22 mL = $2.00/mL`, `15%` below the DTC-single per-mL rate | Sephora labels the same nominal `0.29 oz` as `8 mL`; package price `$20`, equal to DTC single. Its displayed-mL rate is `$20 / 8 = $2.50/mL`, but that is not treated as a clean cross-retailer per-mL comparison. | `$19 / 8 mL = $2.38/mL`; `5%` below shelf, with the same mL-label mismatch |
| SOS standard, 4 fl oz / 120 mL | `$28 / 4 oz = $7.00/oz` | `$25.20 / 4 oz = $6.30/oz`; `10%` below DTC single | Duo, 4 oz + 1 oz: `$30 / 5 oz = $6.00/oz`, `14.29%` below single, but displayed sold out. Jumbo refill: `$68 / 16 oz = $4.25/oz`, `39.29%` below single, also displayed sold out. | `$28 / 4 oz = $7.00/oz`; no shelf divergence from DTC single | `$26.60 / 4 oz = $6.65/oz`; `5%` below shelf |

The repeated finding is price parity between DTC single purchase and Sephora
US shelf across all three subjects. DTC's captured recurring allocations were
10% below single purchase, versus Sephora's displayed 5% Auto-Replenish
reduction. Bundle and larger-size arithmetic sometimes produced lower
effective unit prices, but the SOS duo and jumbo were unavailable page states.
No redemption, realized checkout price, margin, agreement, or promotion-
funding conclusion follows.

### Certification-directory comparison

- Tower 28's LipSoftie and MakeWaves PDPs state that all Tower 28 products are
  vegan and cruelty-free; MakeWaves also displays a compact `Vegan` badge. The
  captured product HTML includes generic images titled `Product certification
  or award`, but does not label them as PETA or Leaping Bunny marks. Their
  certifier identity is therefore unresolved from the owned PDP bytes.
- PETA's own company page uses the entity label `Tower28 Beauty`, marks `All
  products are vegan`, and exposes its licensed-logo indicator. PETA's own
  directory PDF, last updated `02-11-2025`, defines `V` as strictly vegan and
  `L` as licensed to use PETA's official cruelty-free bunny logo. Page 180
  visually aligns both markers, `V L`, with `Tower28 Beauty`.
- Leaping Bunny's own shopping-guide form accepts the `title` query. Its exact
  `Tower28 Beauty` response retained that query and returned zero result rows.
  This is `NO_ENTRY_RETURNED_FOR_EXACT_OFFICIAL_QUERY`, not a misconduct,
  animal-testing, eligibility, or deceptive-label claim.
- None of these sources surfaced a legal-incorporation name. The observed
  directory/brand labels are `Tower28 Beauty` at PETA and `Tower 28 Beauty` on
  the DTC pages; they must not be upgraded to a legal-entity assertion.

### Authorized-channel and Amazon seller read

- Tower 28's captured stores page says customers should shop only through its
  listed authorized retail partners; purchases outside those channels are not
  guaranteed authentic and Tower 28 disclaims responsibility. The page lists
  Tower28Beauty.com, Sephora by named regions (including Sephora at Kohl's),
  Credo, Mecca, the Tower 28 and Revolve official TikTok shops, and
  Revolve.com. Amazon is not in that displayed list.
- The ZIP-`10001` Amazon US LipSoftie and SOS PDPs nevertheless both displayed
  `Ships from Amazon` and `Sold by Tower28 Beauty`. LipSoftie was `$16` for
  `0.38 oz`; SOS was `$28` for `4 oz`. Those prices equal the captured DTC
  single and Sephora US shelf prices.
- These are third-party marketplace offers fulfilled by Amazon, not
  first-party `Sold by Amazon` offers. The seller display label is not proof
  of corporate identity or authorization, but it is a direct falsifier to a
  claim that the observed offers necessarily came from independent diversion
  sellers.
- The commissioned strong form is not met: authorized-list absence was
  observed, but multiple independent sellers were not. Both admitted PDPs
  showed the same brand-named seller, while the third subject was not
  observable in the pinned US state. Quiet distributor authorization,
  brand-controlled marketplace operation, and an incomplete/stale authorized
  list remain named falsifiers. Leak origin and volumes remain outside claim
  reach.

### Receipt inventory

- DTC price and claim packets:
  `F:\forseti-data-lake\raw\2bf\01KXRNEC04CRF4QHVSXGDGVHX3`,
  `F:\forseti-data-lake\raw\423\01KXRNEF82J8P6HG8DGEFGDQ83`,
  `F:\forseti-data-lake\raw\717\01KXRNEJD79S5G6V0DHSB47FD7`,
  `F:\forseti-data-lake\raw\152\01KXRNENXSJ4TYDJXCVGH4YBMN`, and
  `F:\forseti-data-lake\raw\554\01KXRNESH7Y4R9T0JNBDWK604T`.
- Tower 28 stores packet:
  `F:\forseti-data-lake\raw\d71\01KXRNEWHV36K2268ASD0G5VEQ`.
- PETA company-page and PDF packets:
  `F:\forseti-data-lake\raw\e33\01KXRNEZARQKABVBMJ6SFXF2C3` and
  `F:\forseti-data-lake\raw\20f\01KXRNF1E2SD2VJQZC33E8MDPS`.
- Leaping Bunny directory and exact-query packets:
  `F:\forseti-data-lake\raw\911\01KXRNF4G5HVZ0XWHR9CS0SRDK` and
  `F:\forseti-data-lake\raw\7cb\01KXRNR9HNKBW2K188NQVY7ET4`.
- Sephora US LipSoftie, MakeWaves, and SOS packets:
  `F:\forseti-data-lake\raw\1fb\01KXRP0JEX98W982ENNPWW8Z1G`,
  `F:\forseti-data-lake\raw\f30\01KXRP25GT38A88M33ACXJB8VS`, and
  `F:\forseti-data-lake\raw\812\01KXRP3NBRS5P9M6ATH9ANJDCB`.
- Amazon discovery, LipSoftie, MakeWaves gap, and SOS packets:
  `F:\forseti-data-lake\raw\2ba\01KXRP77TV6Q2GCG9DM27Z0VTP`,
  `F:\forseti-data-lake\raw\04c\01KXRPBRXVJJ4THQXW63BTV9R2`,
  `F:\forseti-data-lake\raw\e99\01KXRPD65YCFHVDTMV3QV0HPA7`, and
  `F:\forseti-data-lake\raw\55f\01KXRPF84BA1AZNSVWDACNVSVV`.

The Amazon discovery packet confirmed ZIP `10001` but failed an extra literal
USD-DOM sufficiency check; it was used only to discover subject-bound ASINs.
The MakeWaves packet failed the US pin and seller checks after redirecting to
Amazon Singapore. Both failures remain preserved and typed.

### SOBS-style observation rows

```yaml
observations:
  - observation_id: SOBS-T28-ADDON-001
    observation_class: price_ladder
    subject: Tower 28 LipSoftie Lip Treatment
    retrieval_date: "2026-07-18"
    short_quote_or_summary: >
      DTC single and Sephora US shelf were both USD 16 for 11 g. DTC recurring
      allocation was USD 14.40; Sephora Auto-Replenish was USD 15.20. DTC duo
      was USD 30 for two (USD 15 each), and the four-set was USD 56
      (USD 14 each).
    arithmetic: >
      16/11 = 1.45 USD/g; 14.40/11 = 1.31; 30/22 = 1.36;
      56/44 = 1.27; 15.20/11 = 1.38. Duo and four-set are 6.25%
      and 12.5% below DTC single per unit.
    signal_stage: candidate_support
    claim_it_might_support: point-in-time same-size DTC, bundle, recurring, and Sephora US price parity/divergence
    independence_hypothesis: DTC and retailer-hosted public offer states; commercial coordination is unknown
    packet_locators:
      - 'F:\forseti-data-lake\raw\2bf\01KXRNEC04CRF4QHVSXGDGVHX3'
      - 'F:\forseti-data-lake\raw\423\01KXRNEF82J8P6HG8DGEFGDQ83'
      - 'F:\forseti-data-lake\raw\717\01KXRNEJD79S5G6V0DHSB47FD7'
      - 'F:\forseti-data-lake\raw\1fb\01KXRP0JEX98W982ENNPWW8Z1G'
    hard_limit: >
      Displayed shelf and recurring-plan allocations only; no cart,
      redemption, realized price, margin, promotion funding, or agreement
      inference.

  - observation_id: SOBS-T28-ADDON-002
    observation_class: price_ladder
    subject: Tower 28 MakeWaves Mascara
    retrieval_date: "2026-07-18"
    short_quote_or_summary: >
      DTC and Sephora US package prices were both USD 20 at a nominal 0.29 fl
      oz. DTC recurring allocation was USD 18; Sephora Auto-Replenish was USD
      19. The DTC set was USD 44 for two 8.5 mL full sizes plus one 5 mL mini.
    arithmetic: >
      DTC single 20/8.5 = 2.35 USD/mL; recurring 18/8.5 = 2.12;
      set 44/(8.5+8.5+5) = 2.00, 15% below DTC single per mL.
      Sephora labels 0.29 oz as 8 mL, so its 20/8 = 2.50 and 19/8 = 2.38
      displayed-mL rates are not treated as clean cross-retailer normalization.
    signal_stage: candidate_support
    claim_it_might_support: package-price parity plus DTC recurring and set divergence
    independence_hypothesis: DTC and retailer-hosted public offer states; package-size labeling differs
    packet_locators:
      - 'F:\forseti-data-lake\raw\152\01KXRNENXSJ4TYDJXCVGH4YBMN'
      - 'F:\forseti-data-lake\raw\f30\01KXRP25GT38A88M33ACXJB8VS'
    hard_limit: >
      The 8.5 mL versus 8 mL labels prevent a clean cross-retailer per-mL
      claim. No cart, redemption, margin, or agreement inference.

  - observation_id: SOBS-T28-ADDON-003
    observation_class: price_ladder
    subject: Tower 28 SOS Rescue Spray
    retrieval_date: "2026-07-18"
    short_quote_or_summary: >
      DTC single and Sephora US shelf were both USD 28 for 4 fl oz. DTC
      recurring allocation was USD 25.20; Sephora Auto-Replenish was USD
      26.60. The DTC 5 oz duo was USD 30 and the 16 oz jumbo was USD 68, but
      both were displayed sold out.
    arithmetic: >
      Single 28/4 = 7.00 USD/oz; DTC recurring 25.20/4 = 6.30;
      duo 30/5 = 6.00, 14.29% below single; jumbo 68/16 = 4.25,
      39.29% below single; Sephora recurring 26.60/4 = 6.65.
    signal_stage: candidate_support
    claim_it_might_support: point-in-time same-size parity and volume-ladder divergence
    independence_hypothesis: DTC and retailer-hosted public offer states; unavailable variants are non-purchasable page state
    packet_locators:
      - 'F:\forseti-data-lake\raw\554\01KXRNESH7Y4R9T0JNBDWK604T'
      - 'F:\forseti-data-lake\raw\812\01KXRP3NBRS5P9M6ATH9ANJDCB'
    hard_limit: >
      Sold-out bundle/refill arithmetic is not an attainable transaction.
      No cart, redemption, margin, promotion-funding, or agreement inference.

  - observation_id: SOBS-T28-ADDON-004
    observation_class: certification_directory
    subject: Tower 28 vegan and cruelty-free claims
    retrieval_date: "2026-07-18"
    short_quote_or_summary: >
      Tower 28's owned PDPs state vegan and cruelty-free claims. PETA's own
      company page labels Tower28 Beauty vegan and logo-licensed; its own PDF
      page 180 aligns V and L with Tower28 Beauty, with the legend defining
      those markers as strictly vegan and licensed for PETA's official
      cruelty-free bunny logo.
    signal_stage: candidate_support
    claim_it_might_support: alignment between owned wording and PETA's own directory state
    independence_hypothesis: brand claim and certifier-maintained directory are distinct source classes
    packet_locators:
      - 'F:\forseti-data-lake\raw\2bf\01KXRNEC04CRF4QHVSXGDGVHX3'
      - 'F:\forseti-data-lake\raw\152\01KXRNENXSJ4TYDJXCVGH4YBMN'
      - 'F:\forseti-data-lake\raw\e33\01KXRNEZARQKABVBMJ6SFXF2C3'
      - 'F:\forseti-data-lake\raw\20f\01KXRNF1E2SD2VJQZC33E8MDPS'
    hard_limit: >
      The observed entity label is Tower28 Beauty, not a verified legal name.
      Directory listing and logo licensing do not independently audit every
      formula, supplier, current package, or claim substantiation.

  - observation_id: SOBS-T28-ADDON-005
    observation_class: certification_directory_absence
    subject: Tower 28 at Leaping Bunny
    retrieval_date: "2026-07-18"
    short_quote_or_summary: >
      Leaping Bunny's own exact title query for Tower28 Beauty returned HTTP
      200, retained the supplied query, and exposed zero directory result rows.
    typed_outcome: NO_ENTRY_RETURNED_FOR_EXACT_OFFICIAL_QUERY
    signal_stage: candidate_support
    claim_it_might_support: point-in-time absence from the exact official query response
    independence_hypothesis: certifier-owned public directory response
    packet_locator: 'F:\forseti-data-lake\raw\7cb\01KXRNR9HNKBW2K188NQVY7ET4'
    hard_limit: >
      Zero query rows are not proof of misconduct, animal testing, failed
      eligibility, application history, or deceptive labeling. Query and
      directory drift remain possible.

  - observation_id: SOBS-T28-ADDON-006
    observation_class: diversion
    subject: Tower 28 authorized channels versus Amazon US
    retrieval_date: "2026-07-18"
    short_quote_or_summary: >
      Amazon was absent from Tower 28's displayed authorized-retailer list.
      The pinned Amazon US LipSoftie and SOS PDPs were both fulfilled by Amazon
      and sold by the same display seller, Tower28 Beauty, at USD 16 and USD
      28 respectively, equal to DTC single and Sephora US shelf prices.
    typed_outcome: STRONG_DIVERSION_FORM_NOT_MET
    signal_stage: candidate_support
    claim_it_might_support: authorized-list mismatch with same-seller, price-parity Amazon offers
    independence_hypothesis: brand-owned channel list versus marketplace-hosted seller and offer state
    packet_locators:
      - 'F:\forseti-data-lake\raw\d71\01KXRNEWHV36K2268ASD0G5VEQ'
      - 'F:\forseti-data-lake\raw\04c\01KXRPBRXVJJ4THQXW63BTV9R2'
      - 'F:\forseti-data-lake\raw\55f\01KXRPF84BA1AZNSVWDACNVSVV'
    hard_limit: >
      A seller display label is not proof of corporate identity or
      authorization. Multiple independent sellers were not observed. Quiet
      distributor authorization, brand operation, and list staleness remain
      falsifiers; leak origin and volumes are outside claim reach.

  - observation_id: SOBS-T28-ADDON-GAP-001
    observation_class: typed_surface_gap
    subject: Tower 28 MakeWaves Mascara on Amazon US
    retrieval_date: "2026-07-18"
    short_quote_or_summary: >
      The commissioned amazon.com PDP redirected to amazon.sg, displayed
      Singapore-dollar state, and did not preserve the ZIP 10001 or Sold by
      bindings required for the US seller read.
    typed_outcome: GEO_REDIRECT_US_SELLER_UNOBSERVABLE
    signal_stage: unresolved
    claim_it_might_support: none until a subject-bound US PDP is admitted
    independence_hypothesis: not applicable
    packet_locator: 'F:\forseti-data-lake\raw\e99\01KXRPD65YCFHVDTMV3QV0HPA7'
    hard_limit: >
      The Singapore page cannot answer the Amazon US seller or price question
      and is not substituted into the diversion comparison.
```

### Sephora US/USD storefront pin supplement

- A single follow-up capture reused the commissioned Tower 28 LipSoftie PDP:
  `https://www.sephora.com/product/tower-28-lipsoftie-hydrating-tinted-lip-treatment-balm-P509397?country_switch=us&lang=en`.
- The new `--sephora-market US` route performed no preference mutation. Request
  intent (`country_switch=us`) was admitted only when the final rendered page
  also contained retailer-owned `Sephora.renderQueryParams.country=US` and a
  Sephora-sold JSON-LD `Offer` with `priceCurrency=USD`.
- Packet `01KXRZQJBKNKC91SXH2C7MKF1C` at
  `F:\forseti-data-lake\raw\827\01KXRZQJBKNKC91SXH2C7MKF1C` recorded
  `pin_confirmed=true`, `access_blocked=false`, `proxy_used=false`,
  `persistent_profile_loaded=false`, `storage_state_loaded=false`, and
  `geoip_used=false`. Receipt capture time was `2026-07-17T21:29:14Z`.
- Fresh verification matched all four raw file hashes and byte lengths to the
  manifest. The availability index matched manifest SHA-256
  `f1cf38e79eb11964668e0dcfcc57fd0c6cb2039771a92db4142344bcdb6f1c93`.
- The generic Retail/PDP projection produced one anchored product row and one
  offer row for product `P509397`, SKU `2843068`, price `16.00`, currency
  `USD`. It retained
  `sephora_ld_json_review_count_differs_from_target_dom` as an explicit
  residual.
- Current outcome:
  `US_USD_STOREFRONT_CONFIRMED_DELIVERY_LOCATION_UNPINNED`. This supplement
  changes only storefront-country and currency status; it does not duplicate
  the earlier price-ladder SOBS observations or establish a delivery address.

## Non-claims

These observations do not establish demand, velocity, revenue, sell-through,
market share, repeat purchase, retailer productivity, claim substantiation, or
monitoring readiness. They also do not establish margin, realized transaction
price, redemption, retailer agreement, seller authorization, leak origin, or
diverted volume. They are bounded public page-state evidence only.
