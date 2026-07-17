# Beauty Retailer Surface Probe Results v0

```yaml
retrieval_header_version: 1
artifact_role: Point-in-time beauty retailer surface probe results
scope: >
  Records bounded, subject-bound retailer page-state observations commissioned
  by the Beauty Retailer Surface Probe handoff. Target x Naturium is complete;
  Nordstrom x Nécessaire and Luckyscent x Pearfat Parfum remain unexecuted.
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
| 2 | Nordstrom x Nécessaire | `NOT_EXECUTED` |
| 3 | Luckyscent x Pearfat Parfum | `NOT_EXECUTED` |

This artifact stops at Target as commissioned. It does not re-run the existing
Sephora, Ulta, Walmart, or Amazon US coverage.

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

## Non-claims

These observations do not establish demand, velocity, revenue, sell-through,
market share, repeat purchase, retailer productivity, claim substantiation, or
monitoring readiness. They are bounded public page-state evidence only.
