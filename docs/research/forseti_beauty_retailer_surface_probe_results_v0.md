# Beauty Retailer Surface Probe Results v0

```yaml
retrieval_header_version: 1
artifact_role: Point-in-time beauty retailer surface probe results
scope: >
  Records bounded, subject-bound retailer page-state observations commissioned
  by the Beauty Retailer Surface Probe handoff. Target x Naturium is complete;
  Nordstrom x Nécessaire returned a typed locale-drift partial; Luckyscent x
  Pearfat Parfum remains unexecuted.
use_when:
  - Comparing public retailer assortment, offer, review, and claims surfaces for accepted beauty-pool companies.
  - Retrieving the canonical packet locators and limits for the Target x Naturium probe.
authority_boundary: evidence_register_only
open_next:
  - docs/workflows/forseti_capture_beauty_retailer_surface_probe_handoff_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_sidecar_operator_playbook_v0.md
stale_if:
  - A later capture supersedes a recorded point-in-time page state.
  - A recorded packet is unavailable or fails its preserved-file hash check.
```

## Execution status

| Sequence | Retailer x subject | Status |
| --- | --- | --- |
| 1 | Target x Naturium | `COMPLETE_POINT_IN_TIME_PROBE` |
| 2 | Nordstrom x Nécessaire | `PARTIAL_LOCALE_DRIFT` |
| 3 | Luckyscent x Pearfat Parfum | `NOT_EXECUTED` |

This artifact stops after Nordstrom. It does not re-run the existing Sephora,
Ulta, Walmart, or Amazon US coverage.

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

## Non-claims

These observations do not establish demand, velocity, revenue, sell-through,
market share, repeat purchase, retailer productivity, claim substantiation, or
monitoring readiness. They are bounded public page-state evidence only.
