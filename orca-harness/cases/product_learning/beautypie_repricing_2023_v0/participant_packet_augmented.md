---
case_id: beautypie_repricing_2023_v0
decision_question: At the cutoff, how aggressively should Beauty Pie restructure its membership pricing — specifically whether to eliminate the £5/mo entry tier (moving those members to £10/mo, a doubling for them) and scrap the monthly spending limits — watch, hold, soften, phase/grandfather, or commit to the full elimination-and-doubling?
decision_date_or_cutoff: 2023-02-28
role_frame: Founder/CEO and commercial leadership of Beauty Pie, a UK factory-direct membership beauty brand, deciding how aggressively to restructure membership pricing on pre-cutoff public evidence only.
authority_constraints: Full founder-led pricing and membership-structure authority; the binding constraint is reversibility and member trust, not authority.
capability_constraints: Can ship any membership/pricing structure immediately; decides on evidence available on or before the 2023-02-28 cutoff.
permitted_assumptions:
  - Treat the packet as pre-cutoff only (on or before 2023-02-28).
  - Distinguish general membership/subscription base rates from evidence specific to Beauty Pie's pre-cutoff situation.
  - Treat the prices, tiers, and monthly spending limits in the evidence as real.
  - Judge only on this packet; produce a single blind judgement from it alone.
forbidden_information_notice: Decide using only the evidence in this packet. Do not use, recall, or look up any outside or later knowledge about this company or this decision; base the judgement solely on the packet.
source_manifest:
  - source_id: E1
    source: 'Beauty Pie membership model — factory-direct; members pay a membership fee to buy products at cost (public brand/product description, pre-cutoff). Captured: beautypie.com homepage, Wayback snapshot 2023-02-25 (web.archive.org/web/20230225210430/), evidencing the no-middlemen/no-markup, members-buy-near-making-cost model. SourceCapturePacket: source_captures/e1_homepage_20230225/'
    retrieval_timestamp: 2023-02-25T21:04:30Z
    hash: sha256:1dad75a206688f81309e71af41f4f4c7576f30e1b9760cc7e29627cd0c03745d
  - source_id: E2
    source: 'Beauty Pie membership pricing context for the scenario — public site how-it-works, Wayback snapshot 2022-12-01 (web.archive.org/web/20221201032019/), evidencing the £10/mo monthly membership and the factory-direct/at-cost model. SourceCapturePacket: source_captures/e2_howitworks_20221201/'
    retrieval_timestamp: 2022-12-01T03:20:19Z
    hash: sha256:07aab0838c202da050881c51407f0144dfccfb694cc811f51be87aca415ef425
  - source_id: E3
    source: 'UK cost-of-living / elevated-inflation context, early 2023 (neutral macro context bearing on discretionary spend). Captured: ONS Consumer Price Inflation bulletin, Wayback snapshot 2023-02-16 (web.archive.org/web/20230216220653/). SourceCapturePacket: source_captures/e3_ons_cpi_20230216/'
    retrieval_timestamp: 2023-02-16T22:06:53Z
    hash: sha256:cd358676ff1ece94a31d1af771e57f29d3997928d75683a2ae5243664af5f3fe
  - source_id: E4
    source: 'General base rate — eliminating an entry tier / raising the floor price is a recognized retention-risk repricing lever. source_type general_base_rate: a standing analytic prior, true at and before the cutoff by construction; asserted, not retrieved (no source document or bytes). Freeze-integrity of the asserted text is carried by ledger_freeze_hash.'
    retrieval_timestamp: not_applicable_base_rate
    hash: not_applicable_base_rate
  - source_id: E5
    source: 'Generic comparable consumer-subscription repricings exist across the market. source_type general_base_rate: a standing analytic prior, true at and before the cutoff by construction; asserted, not retrieved (no source document or bytes).'
    retrieval_timestamp: not_applicable_base_rate
    hash: not_applicable_base_rate
  - source_id: E6
    source: 'Organizational-motion arm (augmented only) — Beauty Pie public Greenhouse jobs board, cutoff-proximate Wayback snapshot 2023-01-31 (web.archive.org/web/20230131034812/https://boards.eu.greenhouse.io/beautypie); 8 open roles. SourceCapturePacket: source_captures/e6_greenhouse_20230131/'
    retrieval_timestamp: 2023-01-31T03:48:12Z
    hash: sha256:31e77e7fbee2500135ee68392ec2ffac37d1b2ff673e650e36d65e427e13e38d
  - source_id: E7
    source: 'Organizational-motion arm (augmented only) — Beauty Pie Greenhouse jobs board, Wayback snapshot 2022-10-02 (trajectory point); 7 open roles. SourceCapturePacket: source_captures/e7_greenhouse_20221002/'
    retrieval_timestamp: 2022-10-02T13:53:05Z
    hash: sha256:69487a062389eddb1d65053c81b83f23944ba6e30d37723d1586a9c79f2c8757
  - source_id: E8
    source: 'Organizational-motion arm (augmented only) — Beauty Pie Greenhouse jobs board, Wayback snapshot 2022-06-29 (trajectory point); 7 open roles. SourceCapturePacket: source_captures/e8_greenhouse_20220629/'
    retrieval_timestamp: 2022-06-29T04:24:06Z
    hash: sha256:7dae8856471a729be5a1940371d854f2c6494b7c731ab685f7f27c493dc7920e
  - source_id: E9
    source: 'Organizational-motion arm (augmented only) — Beauty Pie Greenhouse jobs board, Wayback snapshot 2022-01-23 (trajectory point); 11 open roles. SourceCapturePacket: source_captures/e9_greenhouse_20220123/'
    retrieval_timestamp: 2022-01-23T23:47:00Z
    hash: sha256:096e5f113658bbb344b310a37216d46eac17af589467afcabc8a1533c864c7ef
---

# Participant Packet

## Decision Context

Beauty Pie is weighing a membership repricing. The live question, before any decision is announced, is **how aggressively to restructure its membership pricing** — specifically whether to **eliminate the £5/mo entry tier** (moving those members to £10/mo, a doubling for them) and **scrap the monthly spending limits**. The £5/mo tier is the lowest-commitment way into the membership, and the spending limits are part of the current structure. The packet is intentionally narrow: it presents only what was knowable on or before the cutoff (28 February 2023); decide using only the information in this brief. The options span watch / hold / soften / phase-or-grandfather / commit-to-the-full-elimination-and-doubling.

## Evidence Units

- `E1`: Beauty Pie's **membership business model** — factory-direct; members pay a membership fee to buy beauty products at cost. The membership fee is the revenue gate, and the cheapest tier is the low-commitment on-ramp into the model.
- `E2`: Beauty Pie's **membership structure at the cutoff** — two monthly tiers, £5/mo and £10/mo, plus a £59/yr annual "Beauty Pie Plus" (introduced in a 2021 relaunch), each carrying monthly spending limits. The £5/mo tier is the lowest-commitment entry point.
- `E3`: **UK cost-of-living pressure in early 2023** — elevated inflation and squeezed discretionary household spend — a neutral macro context bearing on price sensitivity for discretionary beauty.
- `E4`: Eliminating an entry tier or raising the floor price is a **recognized retention-risk repricing lever** in subscription/membership businesses — a documented general base rate.
- `E5`: **Comparable consumer-subscription repricings** exist across the market — a generic base rate.

## Organizational Motion Signal

A supplementary, lower-grade signal about the company's public hiring activity in the period leading up to the cutoff. Source: Beauty Pie's public Greenhouse jobs board (`boards.eu.greenhouse.io/beautypie`), captured from dated Wayback archive snapshots on or before the cutoff (provenance: source_manifest E6–E9).

Open roles on the board at dated pre-cutoff snapshots:

- **2022-01-23 — 11:** Email & CRM Manager; Senior Customer Service Manager UK; NPD Manager (Supplements); Digital Designer (Paid Social); Talent Partner; Mid-Level UX Designer; Creative Resource Manager; Social Content Creator; Anaplan Model Builder; Senior Software Engineer (×2, Node/TypeScript).
- **2022-06-29 — 7:** Management Accountant; Senior Marketing Analyst; Senior Demand Planning Manager; Supplier Relationship Manager; Senior Software Engineer; Senior Web Analyst; Tech Lead.
- **2022-10-02 — 7:** Head of Brand Performance; Senior NPD Manager (Skincare, maternity cover); Senior Packaging Designer; Packaging Technologist; Engineering Manager; Senior Software Engineer (Frontend); Senior Technical Programme Manager.
- **2023-01-31 (cutoff-proximate) — 8:** Product Lead (Acquisition); Product Lead (Core Shopping Experience); Product Lead (Retention); Demand Planning Analyst; Inventory Planning & Analysis Manager; Senior Engineer; Senior UX Designer; Mid-Weight Digital Designer (maternity-cover fixed-term contract).

Open-role count across the window: **11 → 7 → 7 → 8** (not monotonic; highest at the start of the window). The cutoff-proximate snapshot concentrates in product roles (three Product Leads, including Retention) and demand/inventory planning.

Signal class: **hiring INTENT (open roles), base-rate-discounted — not confirmed net headcount adds.** Open postings are roles the company was seeking to fill at the snapshot date; they are gross hiring intent, not realized hires, and are not evidence of net headcount change.

## Known Uncertainties

- The evidence shows entry-tier removal and floor-price increases are a normal repricing lever **and** that raising the floor on the most price-sensitive members during a cost-of-living squeeze carries retention risk; it does not settle how far is too far.
- There is no pre-cutoff measurement of *Beauty Pie's own* members' tolerance for the doubling, or for scrapping the monthly spending limits specifically.
- Whether the second-order base rate (E3, E4, E5) is enough to *decide* the calibration in advance — versus only being legible in hindsight — is the crux of this decision.
