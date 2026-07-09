---
case_id: kinderbeauty_box_pivot_2023_v0
decision_question: >
  At the cutoff (2023-03-01), should Kinder Beauty pivot its subscription box economics —
  including pricing, box frequency, tier structure, or curation model — to address apparent
  strain in the DTC beauty box segment, and how confidently can that recommendation be made
  on the available pre-cutoff public evidence, given the absence of subscriber count, churn,
  and margin data?
decision_date_or_cutoff: "2023-03-01"
role_frame: >
  Founder and CEO of Kinder Beauty, a DTC subscription beauty box brand, deciding whether
  to restructure the subscription model — pricing, box frequency, tier design, or curation
  approach — using pre-cutoff public evidence only. The decision is yours alone; the brand
  is founder-operated with no disclosed external board authority over product structure or
  pricing.
authority_constraints: >
  Full founder authority over all subscription pricing, box construction, curation model,
  tier structure, and cancellation policy. Binding constraints are subscriber trust — the
  Kinder Beauty audience has opted in on the promise of clean, cruelty-free, vegan beauty
  products at accessible prices — and clean beauty positioning, which restricts which brands
  and product types can be included in boxes without eroding the brand's core credibility.
capability_constraints: >
  Can immediately implement any pricing or structural change to the subscription via the
  Shopify storefront and subscription management backend. Cannot observe post-cutoff
  subscriber reactions, churn rates, or revenue effects before deciding. No access to
  internal subscriber count, monthly recurring revenue, cost-of-goods, or churn data through
  this packet; judgment must rest on what is publicly visible in the DTC storefront,
  subscription selection flows, and supporting pages at the time of the pre-cutoff snapshots.
permitted_assumptions:
  - Treat the packet as pre-cutoff only (on or before 2023-03-01).
  - Treat prices, offers, and mechanics in the evidence as real at the time of each snapshot.
  - Treat the subscription model as under some economic pressure (a permitted framing assumption, not derived from evidence).
  - Score only the fixed judgement included on disk.
forbidden_information_notice: >
  Make your recommendation using only the evidence units in this packet. Do not use, recall,
  or look up any post-cutoff announcements, brand news, subscriber reactions, or information
  dated after 2023-03-01.
source_manifest:
  - source_id: E1
    source: "kinderbeauty.com homepage, 2023-02-27, cutoff-proximate"
    retrieval_timestamp: 2026-06-15T12:32:13Z
    hash: 45309ab72b0ce41f4eff0548fe50d0f1634ae89cf949eeaeb3c8d123a7439bbf
  - source_id: E2
    source: "kinderbeauty.com homepage, 2022-08-31, ~6mo before cutoff"
    retrieval_timestamp: 2026-06-15T12:34:12Z
    hash: 46eb60f22c7edc8bb873959d9179d6b81955d0f063d0b0e9e426dacb5198c44e
  - source_id: E3
    source: "kinderbeauty.com homepage, 2022-02-27, ~1y before cutoff"
    retrieval_timestamp: 2026-06-15T12:34:18Z
    hash: 31a8498bd86f6af0ce92988fa31c5298c686add57922c225a9d248f439f2edd0
  - source_id: E4
    source: "kinderbeauty.com/pages/bundler, box bundling/checkout mechanism, 2023-02-06"
    retrieval_timestamp: 2026-06-15T13:07:00Z
    hash: 3b51d570bce9acfef6fa7c6c20417e5aae9d5ebadd467fde3babc0f3da830236
  - source_id: E5
    source: "kinderbeauty.com/pages/choose-your-box, subscription selection page, 2023-02-05"
    retrieval_timestamp: 2026-06-15T13:07:46Z
    hash: 4297195b0d100caafe5d97319a2a611b9c3fe594c02aebd5560325c8043f65ef
  - source_id: E6
    source: "kinderbeauty.com/pages/how-to-cancel, cancellation policy, 2023-02-05"
    retrieval_timestamp: 2026-06-15T13:12:21Z
    hash: fbc3d7f62766b1c439026bf7358e2002d85c210514af5bd591324e8e130be3dc
  - source_id: E7
    source: "kinderbeauty.com/pages/16-first-box, first-box acquisition offer, 2022-12-08"
    retrieval_timestamp: 2026-06-15T13:08:17Z
    hash: ac2be6afd3337acd2c24a68fb01d5c200583cc0c401f813bd3b916349daad394
  - source_id: E8
    source: "kinderbeauty.com/pages/customer-help, FAQ/support page, 2023-02-05"
    retrieval_timestamp: 2026-06-15T13:12:28Z
    hash: d47c932ef38d5e3b0e50f2f343f381793f9d71b8e96d3d7ff039c53896df883d
  - source_id: E10
    source: "kinderbeauty.com/collections/bestsellers, featured products, 2023-02-05"
    retrieval_timestamp: 2026-06-15T13:13:56Z
    hash: 832d3c099dd12d189da4bc9f9087c39ac201be0f14281463c278a4b56769e03a
  - source_id: E11
    source: "kinderbeauty.com/pages/brands, featured brand curation page, 2022-11-30"
    retrieval_timestamp: 2026-06-15T13:09:01Z
    hash: 9a3010085b3e3d6bd26fba9bc4fa5f49580d75a06cffe10da4b59903eb19b5f1
  - source_id: E12
    source: "kinderbeauty.com/pages/april-2022-box, example monthly box page, 2023-02-01"
    retrieval_timestamp: 2026-06-15T13:14:46Z
    hash: b33c015f423b624ca3ab6f0d51209afcd9aca80c6fb8cf8dd0970d8fae78ce8e
---

# Participant Packet

## Decision Context

Kinder Beauty is a DTC subscription beauty box brand positioned around clean, cruelty-free,
and vegan beauty. Subscribers pay a monthly fee to receive a curated box of full-size and
deluxe-size products from vetted clean beauty brands, delivered on a recurring basis.
The brand's identity is built around ethical sourcing standards — all included products must
be cruelty-free and vegan — which narrows the curation universe relative to mainstream beauty
boxes and differentiates the service for a values-aligned customer segment. The brand operates
its storefront and subscription management through Shopify and sells exclusively direct to
consumer; the website is the only purchase channel visible in the evidence.

The structural economics of DTC beauty box subscriptions in 2022–2023 are materially
constrained. Cost of goods must stay below the subscription price net of shipping and
fulfillment to generate box-level margin, while curation standards — particularly strict
cruelty-free and vegan certification requirements — compress the supplier pool and limit
negotiating leverage. Subscriber acquisition costs in the DTC beauty category ran
meaningfully above what the first-month box margin can recover, placing pressure on lifetime
value: a subscriber must remain active for several billing cycles before the cohort turns
profitable. Churn is structurally high in the beauty box segment — subscribers cancel when
the curation does not match their preferences or when household discretionary budgets
tighten — and acquisition discounts, such as reduced-price first-box offers, compound the
problem by attracting subscribers with lower inherent stickiness. The combination of high
acquisition cost, elevated churn risk, and constrained curation margin makes the unit
economics of a clean-beauty subscription box particularly sensitive to pricing and box
value positioning.

This packet contains only what was publicly observable via the Kinder Beauty DTC storefront
on or before the decision cutoff of 2023-03-01. It consists of Wayback Machine archive
captures of kinderbeauty.com across three points in time (one cutoff-proximate and two
earlier longitudinal snapshots), the live subscription selection and box bundler pages, the
cancellation policy page, a first-box acquisition offer page, the customer FAQ, a featured
bestsellers collection, a brand curation page, and an example monthly box page. No internal
subscriber count, churn rate, monthly recurring revenue, cost-of-goods, or margin data is
available. Decide using only what is in this packet.

## Evidence Units

- `E1`: **kinderbeauty.com homepage, February 2023** — Wayback Machine snapshot captured
  2023-02-27, two days before the decision cutoff, showing the brand's DTC storefront
  homepage in its cutoff-proximate state. Provides the most current available view of how
  the brand presents its subscription offer, featured messaging, and overall storefront
  positioning.

- `E2`: **kinderbeauty.com homepage, August 2022** — Wayback Machine snapshot captured
  2022-08-31, approximately six months before the decision cutoff. Provides a longitudinal
  reference point for comparing homepage messaging, subscription framing, and any visible
  offer changes between mid-2022 and early 2023.

- `E3`: **kinderbeauty.com homepage, February 2022** — Wayback Machine snapshot captured
  2022-02-27, approximately one year before the decision cutoff. Provides the earliest
  longitudinal reference point in the packet, enabling comparison of the subscription offer,
  pricing presentation, and storefront structure across a full year of observable history.

- `E4`: **kinderbeauty.com/pages/bundler, February 2023** — Snapshot of the box bundling
  and checkout mechanism page captured 2023-02-06, showing how the subscription checkout
  flow is structured, what choices subscribers make at the point of conversion, and what
  box-construction mechanics are surfaced to customers.

- `E5`: **kinderbeauty.com/pages/choose-your-box, February 2023** — Snapshot of the
  subscription selection page captured 2023-02-05, showing the available subscription tier
  or box options presented to prospective subscribers at the time of the evidence capture.

- `E6`: **kinderbeauty.com/pages/how-to-cancel, February 2023** — Snapshot of the
  cancellation policy page captured 2023-02-05, showing the publicly stated terms and
  mechanics for cancellation, including any notice requirements, billing cycle rules, or
  retention messaging directed at subscribers considering cancellation.

- `E7`: **kinderbeauty.com/pages/16-first-box, December 2022** — Snapshot of a first-box
  acquisition offer page captured 2022-12-08, showing a discounted or promotional entry
  price for new subscribers, including the offer terms, price point, and any conditions
  or messaging associated with the acquisition incentive.

- `E8`: **kinderbeauty.com/pages/customer-help, February 2023** — Snapshot of the customer
  FAQ and support page captured 2023-02-05, showing what questions and concerns the brand
  surfaces as frequently asked, including policies around billing, shipping, skipping,
  cancellation, and box contents.

- `E10`: **kinderbeauty.com/collections/bestsellers, February 2023** — Snapshot of the
  featured bestsellers collection page captured 2023-02-05, showing which individual
  products or brands the storefront promotes as top performers available for purchase
  outside the subscription box.

- `E11`: **kinderbeauty.com/pages/brands, November 2022** — Snapshot of the featured brand
  curation page captured 2022-11-30, showing which clean beauty brands Kinder Beauty
  publicly associates itself with and features as part of its curation roster. Provides
  signal on the scope and positioning of the brand partner network.

- `E12`: **kinderbeauty.com/pages/april-2022-box, February 2023** — Snapshot of an
  example monthly box page for the April 2022 box, retrieved 2023-02-01, showing the
  contents, brands, and product value claims for a historical box. Provides a reference
  point for evaluating how box curation, product value, and brand mix have been presented
  to subscribers in practice.

## Known Uncertainties

- **No subscriber or churn data is available.** The packet contains no information about
  active subscriber count, cohort retention rates, month-over-month churn, or the
  distribution of subscribers across any tier or box variant. Assessing the severity of
  any subscriber-side strain requires inference from pricing signals and offer structure
  only; the public storefront does not surface these figures.

- **No unit economics or margin data is available.** Cost of goods, box-level margin,
  fulfillment costs, and customer acquisition cost are not disclosed anywhere in the
  evidence. Whether any given pricing or tier structure is profitable at current subscriber
  volume cannot be evaluated from the packet alone.

- **Snapshot timing is uneven across evidence units.** E1 is cutoff-proximate (2023-02-27);
  E4, E5, E6, E8, and E10 are from early February 2023; E7 is from December 2022; E11 is
  from November 2022; E3 is approximately one year before the cutoff (2022-02-27).
  Changes to pricing, offer terms, or box structure between any of these dates and the
  2023-03-01 cutoff may not be captured in the evidence.

- **No direct competitor or segment data is included.** The broader DTC beauty box segment
  context — competitor pricing, peer churn rates, industry-level subscriber acquisition
  trends — is not present in the packet. The decision must be made without direct benchmarking
  against how comparable brands were faring at the same point in time.
