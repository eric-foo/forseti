---
case_id: cocokind_holdprice_2025_v0
decision_question: At the cutoff, should cocokind hold current prices, raise prices to offset tariff cost pressure, or selectively adjust specific SKUs — and how confidently can this recommendation be made on the available evidence alone?
decision_date_or_cutoff: "2025-06-01"
role_frame: Founder/CEO of Cocokind, a direct-to-consumer clean beauty brand, deciding how to respond to tariff-driven cost pressure on pre-cutoff public evidence only.
authority_constraints: Full founder-led pricing authority; the binding constraint is brand positioning, customer trust, and margin sustainability, not authority.
capability_constraints: Can implement any price change immediately across the DTC site; cannot observe post-cutoff customer or competitor reactions before deciding.
permitted_assumptions:
  - Treat the packet as pre-cutoff only (on or before 2025-06-01).
  - Treat prices in the evidence as real current prices at the time of each snapshot.
  - Treat tariff cost pressure on beauty brands as real and non-trivial.
  - Score only the fixed judgement included on disk.
forbidden_information_notice: Make your recommendation using only the evidence provided in this packet. Do not draw on your training knowledge of cocokind's actual pricing decisions, any founder interviews or brand announcements, post-cutoff market reports, or any information about events after the June 1, 2025 cutoff.
source_manifest:
  - source_id: E1
    source: cocokind.com homepage — Wayback Machine snapshot 2025-05-30 (cutoff-proximate)
    retrieval_timestamp: 2026-06-15T13:41:34Z
    hash: 22ab4e993b9ba4773fdae4d5540f06d60f65a999b2f0f8df7823ef9f3cd6420d
  - source_id: E2
    source: cocokind.com homepage — Wayback Machine snapshot 2024-11-29 (mid-window, ~6 months before cutoff)
    retrieval_timestamp: 2026-06-15T13:43:52Z
    hash: b55fc904a63ca02975660a947181be0a94f15cc9c4ca4beac249782760d224e0
  - source_id: E3
    source: cocokind.com homepage — Wayback Machine snapshot 2024-06-25 (~1 year before cutoff)
    retrieval_timestamp: 2026-06-15T13:44:08Z
    hash: 1ef64f521b33d4200208fd8713e5c00340a0c033f701172730e69c91de01057b
  - source_id: E4
    source: cocokind.com/collections/bestsellers — Wayback Machine snapshot 2025-05-23 (featured products with prices)
    retrieval_timestamp: 2026-06-15T13:45:02Z
    hash: 11bbd8fd41d3a2906ee114cd4813bcdc269db7ff2b34ba26634ba570c846a966
  - source_id: E5
    source: cocokind.com/collections/all — Wayback Machine snapshot 2025-04-18 (full catalog with prices)
    retrieval_timestamp: 2026-06-15T13:45:20Z
    hash: 0a32b22d3a81909bc953418ce5f9af7c29dc1dad65552cf6222e6723341ab828
  - source_id: E6
    source: cocokind.com/products/ceramide-barrier-serum — Wayback Machine snapshot 2025-05-22 (hero SKU product page)
    retrieval_timestamp: 2026-06-15T13:47:14Z
    hash: f74b527479d09854ae46d8a01678245ab195c870978608bc13a6ac0919ba8a9f
  - source_id: E7
    source: cocokind.com/products/aha-jelly-cleanser — Wayback Machine snapshot 2025-04-18 (cleanser product page)
    retrieval_timestamp: 2026-06-15T13:47:36Z
    hash: 7a3e1a9e3b929c4b6cb944865d70f2629d2250a7e08aafce95816df993373d10
  - source_id: E8
    source: cocokind.com/products/beginner-retinol-gel — Wayback Machine snapshot 2025-05-22 (retinol product page)
    retrieval_timestamp: 2026-06-15T13:48:26Z
    hash: 78bb8600542f97899b132f3be713ccb0ea05592375662d48c0dca7413a772eb2
  - source_id: E9
    source: cocokind.com/products/ceramide-lip-blur-balm — Wayback Machine snapshot 2025-05-01 (lip balm product page)
    retrieval_timestamp: 2026-06-15T13:49:12Z
    hash: a07288ceab2c13da358604bdd212893b2f6c18ad8b075bfda82fc19d23ae11bd
  - source_id: E10
    source: cocokind.com/products/chagaglo-highlighter — Wayback Machine snapshot 2025-04-18 (color SKU product page)
    retrieval_timestamp: 2026-06-15T13:49:31Z
    hash: 304d378d7c3935b7b8217542eb47dab89f2c36c73e8e8a1ddf16bf35767032ed
---

# Participant Packet

## Decision Context

Cocokind is a direct-to-consumer clean beauty brand that markets itself on accessibility and ingredient transparency. In mid-2025, US tariff policy is adding cost pressure across the beauty supply chain, affecting brands with manufacturing or ingredient sourcing exposure. The question at the cutoff is whether to hold prices and absorb margin pressure, raise prices to pass costs through to consumers, or selectively adjust pricing on specific SKUs.

This packet is intentionally bounded: it preserves pre-cutoff uncertainty and excludes any later announcement, reaction, or outcome. Evidence consists of Wayback Machine snapshots of cocokind's public website taken before the June 1, 2025 cutoff — capturing the brand's homepage trajectory over approximately one year and individual product pages with listed prices.

## Evidence Units

- `E1`: Cocokind homepage as of **May 30, 2025** (cutoff-proximate) — most recent pre-cutoff snapshot of brand messaging, featured collections, and homepage layout at the decision point.
- `E2`: Cocokind homepage as of **November 29, 2024** (~6 months before cutoff) — mid-window snapshot enabling comparison of brand messaging and positioning evolution over the six-month approach to the decision.
- `E3`: Cocokind homepage as of **June 25, 2024** (~1 year before cutoff) — baseline snapshot establishing the earliest reference point for site and positioning changes across the full window.
- `E4`: `/collections/bestsellers` as of **May 23, 2025** — shows which products the brand highlights as bestsellers with their listed prices approximately one week before the cutoff.
- `E5`: `/collections/all` as of **April 18, 2025** — full catalog listing providing the broadest pre-cutoff view of the product lineup and listed prices across the full SKU range.
- `E6`: Ceramide Barrier Serum product page as of **May 22, 2025** — an apparent hero SKU; captures the product description, positioning copy, and listed price approximately 10 days before cutoff.
- `E7`: AHA Jelly Cleanser product page as of **April 18, 2025** — cleanser SKU with listed price and product description.
- `E8`: Beginner Retinol Gel product page as of **May 22, 2025** — retinol SKU with listed price and product description.
- `E9`: Ceramide Lip Blur Balm product page as of **May 1, 2025** — lip balm SKU with listed price.
- `E10`: Chagaglo Highlighter product page as of **April 18, 2025** — color/makeup SKU with listed price (provides price-range reference for a non-skincare category).

## Known Uncertainties

- The evidence captures **what prices are listed** but not the underlying cost structure, gross margin, or tariff exposure of any specific SKU. Any recommendation about pricing must account for the absence of direct cost data.
- The homepage trajectory (E1–E3) shows site evolution over ~one year, but interpreting that evolution as a brand signal requires assumptions about intent that are not independently confirmed in this packet.
- The **full catalog capture (E5) is from April 2025**, approximately six weeks before the cutoff; it is the most comprehensive price view but not the most temporally proximate.
- There is no competitive pricing data, no brand sentiment survey, and no third-party industry report in this packet. Recommendations must rest on internal-evidence-only signals and account for that limitation explicitly.
