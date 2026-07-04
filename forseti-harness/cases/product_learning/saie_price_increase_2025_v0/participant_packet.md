---
case_id: saie_price_increase_2025_v0
decision_question: "Given sustained tariff-driven cost pressure on the US beauty supply chain as of mid-2025, should Saie raise its DTC product prices by $1–4 per product, hold prices at current levels, or pursue a different approach to protect margin while preserving brand equity?"
decision_date_or_cutoff: "2025-06-01"
role_frame: "You are the Founder/CEO of Saie, a clean makeup DTC brand. You are deciding whether to adjust product pricing in response to tariff-related cost pressure affecting the beauty supply chain. You have access only to pre-cutoff public evidence (on or before 2025-06-01). You must recommend: raise prices $1–4, hold, or take a different approach."
authority_constraints: "Full founder-led pricing authority over DTC prices. Binding constraints are (a) consistency with premium-clean brand positioning and (b) long-run margin sustainability. Wholesale channel pricing, retailer relationships, and investor approval are out of scope for this decision."
capability_constraints: "Price changes can be implemented immediately on the DTC site (saiehello.com). The decision-maker cannot observe post-cutoff customer reactions, competitive responses, or downstream sales data before committing. No internal COGS, margin, or tariff pass-through data is available in this evidence set."
permitted_assumptions:
  - Treat the packet as pre-cutoff only (on or before 2025-06-01).
  - Treat prices in the evidence as real current prices at the time of each snapshot.
  - Treat tariff cost pressure on beauty brands as real and non-trivial.
  - Score only the fixed judgement included on disk.
forbidden_information_notice: "Make your recommendation using only the evidence provided in this packet. Do not draw on your training knowledge of Saie's actual pricing decisions, any post-cutoff brand announcements or market reports, or any information about events after the June 1, 2025 cutoff."
source_manifest:
  - source_id: E1
    source: "saiehello.com homepage — Wayback Machine snapshot 2025-05-23 (cutoff-proximate)"
    retrieval_timestamp: 2026-06-15T13:44:32Z
    hash: 3730750cec3d4c408671943907b3e2dbefffc2a1c382d781b6ea0903e93ad5f3
  - source_id: E2
    source: "saiehello.com homepage — Wayback Machine snapshot 2024-11-26 (mid-window, ~6 months before cutoff)"
    retrieval_timestamp: 2026-06-15T13:53:04Z
    hash: c8bf892a362adfd334564633701e15c694d98153f7fee61e292acde0170d9f29
  - source_id: E3
    source: "saiehello.com homepage — Wayback Machine snapshot 2024-07-14 (~10 months before cutoff)"
    retrieval_timestamp: 2026-06-15T13:55:08Z
    hash: 29afbef3cd0ce048af4f18a7a9ea8abe7d5bc505f585b490fe321a3095c922fc
  - source_id: E4
    source: "saiehello.com/collections/all — Wayback Machine snapshot 2025-04-28 (full catalog grid)"
    retrieval_timestamp: 2026-06-15T13:53:31Z
    hash: a47a3a8090626494fb4afc4804df27656a8d3282f1c9c31aef9c8987e18f5223
  - source_id: E5
    source: "saiehello.com/collections/bestsellers — Wayback Machine snapshot 2025-05-22 (hero product lineup)"
    retrieval_timestamp: 2026-06-15T13:48:00Z
    hash: b2db2d0c68dfd29fc835d76d2623983a58b3d3b9124c945e2a44fa1e98e2d6f3
  - source_id: E6
    source: "saiehello.com/products/dew-blush — Wayback Machine snapshot 2025-05-14 (Dew Blush PDP)"
    retrieval_timestamp: 2026-06-15T13:48:23Z
    hash: 3483537934e342f60293f3db2457391ddc8492b0417257616c166843896d21af
  - source_id: E7
    source: "saiehello.com/products/clean-mascara-101 — Wayback Machine snapshot 2025-04-28 (Clean Mascara 101 PDP)"
    retrieval_timestamp: 2026-06-15T13:54:29Z
    hash: e088d95c1c9cfcaddd3c93670b77e19533485987e3a04c8cd3b581dd733bb001
  - source_id: E8
    source: "saiehello.com/products/airset — Wayback Machine snapshot 2025-04-28 (AirSet setting spray PDP)"
    retrieval_timestamp: 2026-06-15T13:49:58Z
    hash: ddce3c3b4172705115d1aed52adb4ab3f9ebf7ca3b21c1de55fe8a7d56d24b0f
  - source_id: E9
    source: "saiehello.com/products/blush-n-glow — Wayback Machine snapshot 2025-03-20 (Blush & Glow PDP)"
    retrieval_timestamp: 2026-06-15T13:50:20Z
    hash: 52cbbedf0825e32b45c99e34ffebfa099e776e82f597fb68208554b4e9946e87
  - source_id: E10
    source: "saiehello.com/products/complexion-boost — Wayback Machine snapshot 2025-04-28 (Complexion Boost PDP)"
    retrieval_timestamp: 2026-06-15T13:50:56Z
    hash: e82a4c1679dd400a5065dda410d6be3008f3acaaaf78d1516613888e5fdf9143
---

# Participant Packet

## Decision Context

Saie is a US-based direct-to-consumer clean makeup brand operating primarily through its own website (saiehello.com). The brand occupies a positioning space that combines clean-ingredient standards with accessible premium pricing — typically in the $20–$36 range per product — and competes against both masstige (e.g., Merit, Kosas) and conventional prestige (e.g., NARS, Benefit) brands. Saie's value proposition centers on clean formulas, sustainability commitments, and a strong brand identity anchored to a particular customer community. Its DTC channel is the primary expression of that identity and gives the brand full control over pricing, presentation, and customer relationship.

By mid-2025, US beauty brands with supply chains sourcing from overseas manufacturers — particularly those dependent on Chinese-origin raw materials, packaging components, or finished goods — were facing materially higher landed costs as a result of tariff escalation. This created a familiar but acute tension for DTC brands: absorb the cost pressure (protecting near-term consumer price perception at the cost of margin compression), pass through some or all of the cost increase (protecting margin at the risk of demand sensitivity), or pursue hybrid approaches such as selective SKU repricing, reformulation, or promotional restructuring. The tariff environment as of early-to-mid 2025 was characterized by elevated uncertainty — rates had shifted materially, and further changes remained possible — making it difficult to calibrate the precise long-run cost exposure any brand should price against.

This decision brief presents pre-cutoff public evidence only. None of the evidence units contain post-cutoff outcome information. The evidence set is limited to archived snapshots of Saie's own website — product pages, collection pages, and homepage states — captured between July 2024 and late May 2025. The evidence does not include internal financial data, COGS disclosures, competitive price benchmarking from third-party sources, or consumer sentiment surveys. All reasoning in this exercise must be grounded exclusively in what can be observed in these snapshots plus general pre-cutoff knowledge of beauty DTC economics and tariff dynamics. Do not import any knowledge of what Saie actually did after June 1, 2025.

## Evidence Units

- **E1** — saiehello.com homepage, Wayback Machine snapshot 2025-05-23: Cutoff-proximate homepage capture showing Saie's brand messaging, hero product placement, and featured product lineup as of approximately one week before the decision cutoff. Provides a near-final pre-cutoff read on how the brand was presenting itself and what products it was foregrounding.

- **E2** — saiehello.com homepage, Wayback Machine snapshot 2024-11-26: Homepage capture from approximately six months before the decision cutoff. Provides a mid-window reference point for brand messaging and product emphasis, useful for comparing to E1 and E3 to identify any shift in homepage positioning across the ~10-month window.

- **E3** — saiehello.com homepage, Wayback Machine snapshot 2024-07-14: Homepage capture from approximately ten months before the decision cutoff. Provides the earliest longitudinal anchor in the homepage series, establishing a baseline for brand messaging, product lineup, and any observable changes in tone or emphasis over the period leading up to the cutoff.

- **E4** — saiehello.com/collections/all, Wayback Machine snapshot 2025-04-28: Full catalog grid page captured approximately five weeks before the decision cutoff. Provides breadth coverage of the full product lineup as of late April 2025, including product names and listed prices across all categories, enabling a catalog-wide view of the brand's price architecture at that point.

- **E5** — saiehello.com/collections/bestsellers, Wayback Machine snapshot 2025-05-22: Bestsellers collection page captured approximately ten days before the decision cutoff. Provides a curated view of Saie's highest-priority SKUs as of late May 2025, including listed prices for hero products, and signals which products the brand was choosing to lead with commercially.

- **E6** — saiehello.com/products/dew-blush, Wayback Machine snapshot 2025-05-14: Product detail page for the Dew Blush, captured approximately two and a half weeks before the decision cutoff. Provides the listed price, product description, ingredient messaging, and any promotional or badging signals present on a key blush SKU at near-cutoff.

- **E7** — saiehello.com/products/clean-mascara-101, Wayback Machine snapshot 2025-04-28: Product detail page for Clean Mascara 101, captured approximately five weeks before the decision cutoff. Provides listed price, product copy, and positioning signals for one of Saie's mascara SKUs in the eye category.

- **E8** — saiehello.com/products/airset, Wayback Machine snapshot 2025-04-28: Product detail page for the AirSet setting spray, captured approximately five weeks before the decision cutoff. Provides listed price, product description, and positioning language for a finishing/setting product SKU.

- **E9** — saiehello.com/products/blush-n-glow, Wayback Machine snapshot 2025-03-20: Product detail page for Blush & Glow, captured approximately ten weeks before the decision cutoff. The earliest individual PDP in the evidence set; provides a March 2025 price and positioning reference for this product.

- **E10** — saiehello.com/products/complexion-boost, Wayback Machine snapshot 2025-04-28: Product detail page for Complexion Boost, captured approximately five weeks before the decision cutoff. Provides listed price, product description, and category positioning for a complexion/base product SKU.

## Known Uncertainties

- **No internal cost structure data**: None of the evidence units contain COGS, gross margin, supplier invoices, or landed-cost disclosures. The actual magnitude of tariff pass-through burden on Saie's margin is unobservable from this evidence set alone.

- **No competitive price benchmarking**: The evidence is limited to Saie's own website. No contemporaneous price data for comparable clean beauty DTC brands (Merit, Kosas, Ilia, Tower28, etc.) is included, making it impossible to assess where Saie's prices sit relative to the competitive set from the evidence alone.

- **No consumer price sensitivity data**: No customer survey, review sentiment analysis, or sales volume data is present in the evidence. The degree to which Saie's customer base would tolerate a $1–4 price increase cannot be estimated from this evidence set.

- **Snapshot clustering and gaps**: The homepage series (E1–E3) spans July 2024 to May 2025, but the product detail pages (E6–E10) cluster tightly around April–May 2025. There is no individual PDP evidence from mid-2024 to early 2025, so SKU-level price trajectory over that period is not directly observable.

- **Tariff trajectory uncertainty**: As of June 2025, the future path of US tariff rates remained uncertain. Evidence that cost pressure is real and non-trivial is treated as a permitted assumption, but the duration, severity, and product-category scope of the tariff impact on Saie's specific supply chain is not resolvable from public website snapshots alone.
