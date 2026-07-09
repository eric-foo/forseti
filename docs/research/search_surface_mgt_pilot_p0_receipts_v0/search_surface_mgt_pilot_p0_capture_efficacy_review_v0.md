# Search-Surface MGT Pilot P0 Capture Efficacy Review v0

```yaml
retrieval_header_version: 1
artifact_role: Research synthesis artifact
scope: Evaluates whether the Search-Surface MGT P0 Google SERP capture set is materially useful for Capture and Scanning routing.
use_when:
  - Deciding whether the Search-Surface MGT pilot should proceed to P1 direct-source capture.
  - Comparing search-surface capture value against generic search research or brand-level MGT scans.
  - Checking the accepted residuals before using the P0 search captures downstream.
open_next:
  - docs/research/search_surface_mgt_pilot_p0_receipts_v0/search_surface_mgt_pilot_p0_capture_receipt_v0.md
  - docs/research/search_surface_mgt_pilot_p0_receipts_v0/capture_manifest.json
  - forseti/product/spines/scanning/scan_core/forseti_scanning_intelligent_walk_mgt_operating_model_v0.md
  - forseti/product/spines/scanning/source_families/answer_engine/demand_search_interest_sourcing_and_gate_delta_spec_v0.md
stale_if:
  - The P0 Google SERP captures are recaptured under a different route or judged from a different session state.
  - A P1 direct-source capture pass supersedes this routing review.
  - Forseti changes the scanning, capture, search-interest, or answer-engine surface boundaries.
authority_boundary: retrieval_only
```

## Verdict

`PROCEED_TO_P1_CAPTURE_EFFICACY`.

The P0 search-surface capture set is materially better than generic search research for one job: deciding what Capture and Scanning should inspect next. It exposes market language, SERP module shape, AI answer-surface visibility, comparison language, product/retailer surfaces, forum/video surfaces, and follow-up query vectors in one bounded packet.

It is not complete enough for Judgment, Product Lead, buyer proof, willingness-to-pay proof, durable-demand proof, search scoring, or market-size claims. Its value is routing value.

## What Got Better

| Capability | P0 evidence | Why it matters |
| --- | --- | --- |
| Market language | `niche perfume discovery set sale`, `niche perfume discovery sets reddit`, `perfume samples before buying full bottle`, `Le Labo Santal 33 dupe reddit`, `Baccarat Rouge 540 dupe Zara`, `pistachio perfume KAYALI`, `vanilla skin perfume` | Gives Scanning and Capture the words buyers/searchers actually use instead of analyst labels. |
| Venue discovery | Each query preserved product/shopping, video, forum, image, PAA/PAS, or discussion modules; Q01 also preserved autocomplete. | Shows where to look next: retailer PDPs, Reddit threads, YouTube/TikTok surfaces, Fragrantica, editorial lists, and Google product modules. |
| Comparison/confusion map | Dupe queries surfaced alternatives such as Dossier, Fine'ry, Maison Louis Marie, Cremo, Armaf, Lattafa, Zara, Ariana Grande Cloud, and Sol de Janeiro. | Reveals substitution language, price anchoring, and competitor sets that a brand-level scan may miss. |
| Format/offer surface | Discovery/sample queries exposed discovery sets, vouchers, decants, travel sprays, tiny vials vs. 5-10ml trials, and retailer sampling routes. | Useful for identifying decision surfaces around trial, conversion, full-bottle purchase, and mini/travel formats. |
| Currentness cues | Examples include a 2026 sample-buying guide, Jan. 21 2026 dupe coverage, 7-10 month video/forum surfaces, and fresh short-video modules. | Helps prioritize next reads, while staying inside the rule that recency is attention priority, not proof. |
| AI answer-surface state | Q01, Q02, Q05 show `ai_overview_shown`; Q06 shows `ai_overview_shown_no_ai_mode_tab`; Q03 and Q04 show `ai_mode_tab_only_no_ai_overview`. | Makes both the AI Overview box and its absence first-class routing observations, and gives a bounded reason to compare against search-interest/Trends later without treating either as proof. |

## Comparison To Existing Inputs

The ChatGPT Pro beauty sub-niche intake was useful for choosing the first test area: founder-led indie/DTC fragrance, scent layering, body mist, discovery/travel formats, inventory, and retail-depth decisions. It was directional, not a verified Forseti scan.

The Imaginary Authors MGT scan was useful at brand-level current state. It found official PDPs, retailer collections, sold-out/restock UI, editorial/trend surfaces, and capture requests. But within its cap it did not find independent buyer-origin evidence, and exact product/community searches were dry.

The P0 search-surface capture is stronger for a different layer: it maps the category's public search language and hidden next venues before a brand is chosen. It should feed Scanning broad-scout work and Capture requests; it should not replace either lane.

## Complete Enough?

Complete enough for:

- choosing a P1 direct-source capture route;
- generating exact-query/frontier candidates for Scanning;
- identifying which surfaces are likely worth capture: forums, video/short-video, retailer/product modules, editorial lists, and community/social surfaces;
- comparing whether search-surface capture adds information beyond generic search research;
- selecting which query clusters deserve a bounded search-interest/Trends correlation probe against AI-answer-surface shown/not-shown state.

Not complete enough for:

- durable-demand or buyer-proof claims;
- product readiness or Product Lead action;
- willingness-to-pay evidence;
- market sizing or search-volume inference;
- explaining why Google did or did not show an AI Overview box without a separate bounded Trends/search-interest probe and repeated capture;
- proving US physical locality;
- classifying whether a surfaced result is real demand, SEO/editorial content, paid placement, affiliate content, or seeded launch amplification without direct source reads.

## Accepted Residuals

- The route is US-parameterized (`hl=en&gl=us&pws=0`, `en-US`, logged out) but not physically US-local. Google footer reported unknown location and browser timezone was `Asia/Singapore`.
- Queries were not captured under one identical Google session. Q01-Q02 used one visible batch; Q03-Q06 used separate fresh visible profiles.
- The P0 query set is small and intentionally shaped. It does not cover the full fragrance search universe.
- SERP modules are forward snapshots. They decay and can change with Google rendering, localization, personalization controls, or time.
- Search/AEO surfaces remain attention/routing surfaces. Under the search-interest and AEO source spec, they do not clear the demand floor.
- AI Overview `not_shown` / no-box states are visibility observations only; they are not absence-of-demand and do not reveal Google internal trigger logic by themselves.

## P1 Route

Run P1 as direct-source capture, not more broad Google recapture.

1. Discovery and sampling cluster:
   - Start from Q01 and Q02.
   - Preserve direct reads for Twisted Lily, Ministry of Scent, Sephora sampler/voucher surfaces, high-signal Reddit threads, and one sample-buying guide if it exposes buyer-language or retailer route detail.
   - Goal: determine whether trial/discovery-set language produces capture-worthy buyer-origin or retailer-depth evidence.

2. Dupe and comparison cluster:
   - Start from Q05 and Q06.
   - Preserve direct reads for the top Reddit threads, product alternative surfaces, and one short-video/video surface where visible metadata is accessible.
   - Goal: determine whether dupe language exposes substitution pressure, price anchors, and independent buyer-origin comparison behavior.

3. AI-answer / Trends correlation cluster, optional but now first-class:
   - Compare Q03 and Q04 (`ai_mode_tab_only_no_ai_overview`) against Q01/Q02/Q05/Q06 (`ai_overview_shown*`) using a bounded Google Trends/search-interest read if sourcing is authorized.
   - Goal: test whether search-interest posture, query ambiguity, category maturity, or commercial-result density helps explain no-AI-box state. Do not infer Google causality, demand absence, or score priority.

4. Trend-note cluster, optional:
   - Use Q03 and Q04 only if P1 needs a trend-language/control cluster.
   - Goal: compare note/trend language (`pistachio`, `vanilla skin`) against format/comparison language without over-expanding the pilot.

## Success Bar For Continuing

Continue the Search-Surface MGT method if P1 direct reads convert at least two clusters into one of:

- a concrete Scanning frontier;
- a Capture request with specific URL/surface, acquisition route, and verification question;
- a negative that cheaply closes a tempting but weak route.

Stop or narrow if P1 mostly yields SEO/editorial lists, affiliate pages, uninspectable social surfaces, or repeated SERP module noise without buyer-origin language or route value.

## Lane Implication

Do not create a standalone Search branch from this. Treat Search-Surface MGT as a front-door method that strengthens Scanning and Capture:

```text
search-surface P0
-> market-language and venue-route map
-> P1 direct-source capture
-> Scanning frontier / capture_request / negative
-> later Judgment only if preserved sources meet the separate proof contract
```

This develops the spine by giving Scanning better frontiers and giving Capture better target asks. It does not mint candidates or make demand calls by itself.
