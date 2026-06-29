# Search-Surface MGT P1 Direct-Source Capture Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Research capture receipt
scope: P1 direct-source capture and routing read for the five Priority A Search-Surface MGT fragrance sources selected by decision effect.
use_when:
  - Reviewing whether P1 converted P0 search-surface results into Scanning frontiers, Capture requests, or negatives.
  - Checking the boundary between search-surface routing and Judgment/Product Lead proof.
  - Preparing a downstream Capture request from the Search-Surface MGT pilot.
open_next:
  - docs/research/search_surface_mgt_pilot_p1_decision_source_triage_v0.md
  - docs/research/search_surface_mgt_pilot_p1_direct_source_capture_v0/capture_manifest.json
  - docs/research/search_surface_mgt_pilot_p1_direct_source_capture_v0/hashes_sha256.txt
  - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
stale_if:
  - The five Priority A source URLs are recaptured through a different route.
  - Reddit access becomes packet-grade locally available and supersedes the screen-light web/browser read.
  - P1 is promoted into a formal Capture packet, Scanning frontier, or Judgment source set.
authority_boundary: retrieval_only
```

## Boundary

This is P1 direct-source capture for routing. It is not Judgment evidence, buyer proof, durable-demand proof, willingness-to-pay proof, market sizing, Product Lead action, or AI Overview causality.

P1 was run under the owner direction: prioritize a search result when it can affect a decision, even if it is only light support. AI-box presence is metadata only and did not drive source priority.

## Source Set

| Source ID | Cluster | URL | Capture state |
| --- | --- | --- | --- |
| `p1_s01_reddit_fragrance_testing` | Discovery / sampling | `https://www.reddit.com/r/FragranceStories/comments/1mydzqk/how_do_you_test_a_fragrance_before_buying/` | Browser/web observed; direct HTTP blocked by Reddit network-policy page; no local raw source body. |
| `p1_s02_ministry_sample_sets` | Discovery / sampling | `https://ministryofscent.com/collections/sample-sets-1` | Local compressed HTML, text extraction, and Shopify products JSON preserved. |
| `p1_s03_twisted_lily_discovery_sets` | Discovery / sampling | `https://twistedlily.com/collections/samples-discovery-sets` | Local compressed HTML, text extraction, and Shopify products JSON preserved. |
| `p1_s04_reddit_santal_33_dupes` | Dupe / comparison | `https://www.reddit.com/r/fragrance/comments/15fp22s/what_is_the_best_alternative_to_santal_33_by_le/` | Browser/web observed; direct HTTP blocked by Reddit network-policy page; no local raw source body. |
| `p1_s05_reddit_br540_dupes` | Dupe / comparison | `https://www.reddit.com/r/Colognes/comments/1nwmudi/im_looking_for_close_dupes_of_baccarat_rouge_540/` | Browser/web observed; direct HTTP blocked by Reddit network-policy page; no local raw source body. |

## Local Files Preserved

```text
docs/research/search_surface_mgt_pilot_p1_direct_source_capture_v0/source_receipts/p1_s02_ministry_sample_sets.html.gz
docs/research/search_surface_mgt_pilot_p1_direct_source_capture_v0/source_receipts/p1_s02_ministry_sample_sets.txt
docs/research/search_surface_mgt_pilot_p1_direct_source_capture_v0/source_receipts/p1_s02_ministry_sample_sets_products.json
docs/research/search_surface_mgt_pilot_p1_direct_source_capture_v0/source_receipts/p1_s03_twisted_lily_discovery_sets.html.gz
docs/research/search_surface_mgt_pilot_p1_direct_source_capture_v0/source_receipts/p1_s03_twisted_lily_discovery_sets.txt
docs/research/search_surface_mgt_pilot_p1_direct_source_capture_v0/source_receipts/p1_s03_twisted_lily_discovery_sets_products.json
```

Hash ledger: `docs/research/search_surface_mgt_pilot_p1_direct_source_capture_v0/hashes_sha256.txt`.

## Discovery / Sampling Read

### Buyer-Origin Thread

Reddit thread observed: `How do you test a fragrance before buying?`

Decision-useful signals:

- Buyers describe a sequence from card/bottle smell to skin testing to repeat wears.
- Visible comments mention decants, 2ml, 5ml, 10ml, travel size, full bottle, discovery sets, in-store sampling, and blind-buy thresholds.
- The thread exposes buyer grammar around avoiding costly blind buys, testing skin chemistry, using samples across multiple wears/seasons, and upgrading from sample/decant to travel-size or bottle.

Route value:

- This is strong enough to become a Scanning frontier: `trial_to_full_bottle_behavior`.
- It is also a Capture request because Reddit is volatile/community-hosted and direct HTTP source-body preservation was blocked.

### Retailer Shelves

Ministry of Scent preserved observations:

- `products.json` count: 97 products.
- The collection text says full bottles ship within 1-2 days and sample-only orders within 5 days.
- The page positions sample sets as a way to experience niche fragrance brands before choosing favorites.
- First preserved product rows include `Curated by Cammy: The Gummy Set` at `$65.00`, `Indult Discovery Set` at `$45.00`, and `Comme des Garçons Discovery Set` at `$60.00`.
- The shelf exposes filters for brand, scent style, note, notable details, season, gender/unisex, and product type.

Twisted Lily preserved observations:

- `products.json` count: 59 products.
- First preserved product rows include `Twisted Lily Best Sellers Sample Pack` at `$52.00`, `Essential Parfums Discovery Set` at `$35.00`, and `Twisted Lily x After Hours` at `$35.00`.
- Browser observation showed discovery-set shelf rows with prices/reviews; direct HTML text extraction was too navigation-heavy, so the structured products JSON is the cleaner local receipt.
- Navigation preserves `SAMPLING`, `Samples`, `Discovery Sets`, and `Travel-sized Fragrances` as retail taxonomy.

Route value:

- Retailer pages are useful for offer mechanics: product count, price ladder, sold-out state, reviews, sample/travel taxonomy, and category filters.
- They do not prove demand by themselves, but they make the trial/discovery frontier concrete enough for Capture to preserve selected shelf/product pages.

## Dupe / Comparison Read

### Santal 33 Thread

Reddit thread observed: `What is the best alternative to Santal 33 by Le Labo?`

Decision-useful signals:

- The initiating motive is price pressure around a loved premium fragrance.
- Buyer language splits use-cases: keep the original for collection/signature use, but use cheaper alternatives for everyday low-stakes wear.
- Visible alternatives include Maison Louis Marie `Bois de Balincourt`, Cremo `Palo Santal`, Fine'ry `Jungle Santal`, Dossier, ArabianPerfumeOil, Perfume Parlour, Dime, and Costco/Sam's Club original-price references.
- Comments distinguish "closest", "better than Santal", "not a dupe", "not satisfied with alternatives", and "body wash/lotion layering base".

Route value:

- This becomes a Scanning frontier: `premium_dupe_substitution_pressure`.
- It also becomes a Capture request for Reddit thread preservation and follow-on product-page checks for repeated alternatives.

### Baccarat Rouge 540 Thread

Reddit thread observed: `I'm looking for close dupes of Baccarat Rouge 540`

Decision-useful signals:

- Visible alternatives include Lattafa `Ana Abiyedh Rouge`, Maison Alhambra `Baroque Rouge 540`, The Woods Collection `Flame`, Al Haramain `Amber Oud Ruby`, Dossier `Ambery Saffron`, Ariana Grande `Cloud`, Club de Nuit `Untold`, Dubai Mirza, and Montagne `Le Bon Bon`.
- Comments include both positive and negative comparison language: close, not close, alcohol-heavy, performance/longevity, price/value, and "scratch that itch" language.
- The thread is stronger than editorial listicles because it exposes disagreement and repeated buyer-origin comparison language.

Route value:

- This supports the same `premium_dupe_substitution_pressure` frontier.
- It also produces a Capture request for repeated alternative product pages and source-preserved comparison language.

## Classification

| Cluster | P1 result | Why |
| --- | --- | --- |
| Discovery / sampling | `scanning_frontier_plus_capture_request` | Buyer-origin testing language plus retailer shelf mechanics can affect the next Capture/Scanning decision. |
| Dupe / comparison | `scanning_frontier_plus_capture_request` | Buyer-origin substitution language plus repeated alternatives can affect competitor/substitute Capture requests and Scanning comparison frontiers. |
| AI answer-surface state | `metadata_only` | AI-box presence did not materially affect P1 source priority. |
| Editorial/listicle surfaces | `deferred` | Lower priority than buyer-origin Reddit and direct retailer shelves for this P1 purpose. |
| Sephora sampler/voucher | `deferred_access_limited` | Still potentially useful for voucher mechanics, but not needed to satisfy P1 once Ministry/Twisted Lily plus buyer testing thread were observed. |

## Capture Requests

### `capture_request_search_p1_trial_discovery_v0`

```yaml
capture_request_id: capture_request_search_p1_trial_discovery_v0
source_scan: Search-Surface MGT P1 direct-source capture
candidate_or_observation_ids:
  - discovery_sampling_reddit_testing_behavior
  - discovery_sampling_retailer_shelf_mechanics
urls:
  - url: https://www.reddit.com/r/FragranceStories/comments/1mydzqk/how_do_you_test_a_fragrance_before_buying/
    venue: Reddit / fragrance community
    observation_supported: buyer testing grammar around decants, repeated wears, sample size, travel size, and full-bottle upgrade
    gate_role: none
  - url: https://ministryofscent.com/collections/sample-sets-1
    venue: retailer / niche fragrance sample-set shelf
    observation_supported: product count, price ladder, sample-only shipping, filters, reviews, sold-out states
    gate_role: none
  - url: https://twistedlily.com/collections/samples-discovery-sets
    venue: retailer / niche fragrance discovery-set shelf
    observation_supported: product count, price ladder, sampling/travel taxonomy, reviews
    gate_role: none
what_capture_should_verify: Preserve packet-grade Reddit/source body if permitted, plus selected retailer shelf/product pages that show trial-to-bottle offer mechanics.
decision_window: current forward snapshot; source surfaces can change.
route_binding_state: unknown
screening_evidence_summary: P1 observed buyer-origin testing language and locally preserved two retailer shelves with 97 and 59 structured product rows.
uncertainty_or_access_limits: Reddit direct HTTP blocked; retailer product pages are current snapshots and do not prove demand.
not_requested:
  - route expansion
  - packet commitment by scanning
  - ECR, Cleaning, or Judgment work
```

### `capture_request_search_p1_dupe_comparison_v0`

```yaml
capture_request_id: capture_request_search_p1_dupe_comparison_v0
source_scan: Search-Surface MGT P1 direct-source capture
candidate_or_observation_ids:
  - premium_dupe_substitution_pressure_santal33
  - premium_dupe_substitution_pressure_br540
urls:
  - url: https://www.reddit.com/r/fragrance/comments/15fp22s/what_is_the_best_alternative_to_santal_33_by_le/
    venue: Reddit / fragrance community
    observation_supported: Santal 33 price-pressure and closest-alternative comparison language
    gate_role: none
  - url: https://www.reddit.com/r/Colognes/comments/1nwmudi/im_looking_for_close_dupes_of_baccarat_rouge_540/
    venue: Reddit / fragrance community
    observation_supported: Baccarat Rouge 540 closest-dupe comparison language and repeated alternatives
    gate_role: none
what_capture_should_verify: Preserve packet-grade Reddit/source body if permitted, then inspect repeated alternative product pages only where buyer-origin repetition justifies it.
decision_window: current forward snapshot; Reddit threads are archived but visible rendering/access can change.
route_binding_state: unknown
screening_evidence_summary: P1 observed repeated alternatives and comparison language across both premium-dupe threads.
uncertainty_or_access_limits: Reddit direct HTTP blocked; screen-light read is enough for routing but not enough for Judgment.
not_requested:
  - route expansion
  - packet commitment by scanning
  - ECR, Cleaning, or Judgment work
```

## P1 Verdict

`P1_CONVERTED_TO_TWO_FRONTIERS_PLUS_CAPTURE_REQUESTS`.

Continue Search-Surface MGT as a front-door method. It produced decision-useful routing beyond generic search:

- Scanning frontier: `trial_to_full_bottle_behavior`.
- Scanning frontier: `premium_dupe_substitution_pressure`.
- Capture request: preserve trial/discovery buyer thread plus retailer shelf/product mechanics.
- Capture request: preserve dupe/comparison threads plus repeated alternative product pages.

Do not move to Judgment yet. P1 is strong enough to tell Capture and Scanning where to look next; it is not strong enough to make a durable-demand or buyer-proof call.

## Non-Claims

- Not Judgment evidence.
- Not durable-demand proof.
- Not buyer proof.
- Not willingness-to-pay proof.
- Not Product Lead action.
- Not market sizing.
- Not source exhaustiveness.
- Not a standalone Search branch.
- Not proof that AI Overview presence affects source priority.
