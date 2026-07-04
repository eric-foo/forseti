---
case_id: inoreader_repricing_2019_v0
decision_question: At the cutoff, how aggressively should Inoreader gate power-user functionality (notably Rules automation) into higher paid tiers when repackaging — watch, hold, narrow, phase, or commit to aggressive gating?
decision_date_or_cutoff: 2019-02-06
role_frame: Founder/CEO of Innologica, a small bootstrapped RSS-reader company, deciding how aggressively to gate power-user features when repackaging, on pre-cutoff public evidence only.
authority_constraints: Full founder-led pricing and packaging authority; the binding constraint is reversibility and user trust, not authority.
capability_constraints: Can ship any tier structure immediately; cannot observe the actual user reaction before deciding.
permitted_assumptions:
  - Treat the packet as pre-cutoff only (on or before 2019-02-06).
  - Distinguish a pre-existing base rate from a reaction to this specific move.
  - Treat prices and limits in the evidence as real.
  - Score only the fixed judgement included on disk.
forbidden_information_notice: Do not use the actual February 2019 announcement, the user reaction, any walk-back, later pricing evolution, post-cutoff outcomes, or hidden facilitator labels.
source_manifest:
  - source_id: E1
    source: 'Inoreader blog — How to Save Time with Rules (Rules positioned as a Pro feature)'
    retrieval_timestamp: 2026-06-10T00:00:00Z
    hash: 897911383af5e61503e949ad6df513ebe99b04ca79417be082549b4597143107
  - source_id: E2
    source: 'Inoreader pre-2019 pricing/upgrade brochure (tier structure + per-tier Rules/active-search limits)'
    retrieval_timestamp: 2026-06-10T00:00:00Z
    hash: 57c210924f6e57b16abf6c9cb1a329e75eccc7a281305e678b534cf478607a5c
  - source_id: E3
    source: 'The Old Reader blog — "You Are Not a Product: Why Premium Pricing Is Here" (verbatim user objections)'
    retrieval_timestamp: 2026-06-10T00:00:00Z
    hash: 6c85358548226e20e3bbb5795f2e5c8fedc27435592ef80670147303293fb987
  - source_id: E4
    source: 'Computerworld — Feedly launches paid RSS service (search/integrations gated behind Pro)'
    retrieval_timestamp: 2026-06-10T00:00:00Z
    hash: fc5ac9dfcf67f161d3ba18c02af36eaa3075ddd00bb7bcd1bb1713e36276814a
  - source_id: E5
    source: 'Hacker News — RSS reader monetization / willingness-to-pay discussion (2017)'
    retrieval_timestamp: 2026-06-10T00:00:00Z
    hash: dd4b42bf5f53a87fb61df87034ee9e9726cda98fc79ad81e58e4dff52fd57dd7
---

# Participant Packet

## Decision Context

Inoreader is repackaging its plans. The live question, before any decision is announced, is **how aggressively to move power-user functionality — especially Rules automation — into higher paid tiers**. Rules are the feature power users came to Inoreader for. The packet is intentionally narrow: it preserves the pre-decision uncertainty and excludes any later announcement, reaction, or outcome. The options span watch / hold / narrow / phase-in / commit-to-aggressive-gating.

## Evidence Units

- `E1`: Inoreader's own prior positioning of Rules as a **Pro / power-user feature** — a multi-year anchor that Rules are the differentiator power users pay for and rely on.
- `E2`: Inoreader's pre-2019 **tier structure** (Free / Starter / Plus / Professional) with Rules and active-searches already tiered — power-user value concentrated in the upper tiers, but a generous low end.
- `E3`: an analogous RSS reader's move to premium pricing that drew **verbatim "why pay for something that's always been free / RSS is part of the free internet" objections** — a documented base rate of power-user resistance to paywalling RSS.
- `E4`: the **category leader (Feedly)** gating search and integrations behind Pro — evidence that gating power features is *industry-normal* — while the search paywall *specifically* drew documented backlash.
- `E5`: a power-user discussion showing an **accepted willingness-to-pay band** for RSS readers and that sustainability-via-payment is tolerated, while steep jumps meet pushback.

## Known Uncertainties

- The evidence shows gating power features is normal **and** that aggressive gating of an expected feature draws backlash; it does not settle how far is too far.
- There is no pre-cutoff measurement of *Inoreader's own* users' tolerance for tightening Rules specifically.
- Whether the second-order base rate (E3, E4, E5) is enough to *decide* the calibration in advance — versus only being legible in hindsight — is exactly what this case tests.
