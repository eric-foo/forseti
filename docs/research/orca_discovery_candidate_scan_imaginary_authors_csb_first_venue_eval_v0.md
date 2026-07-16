# Orca Discovery Candidate Scan - Imaginary Authors CSB-First Venue Evaluation v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact (fresh CSB-first MGT venue-evaluation scan)
scope: >
  One fresh forward-mode bounded intelligent-walk scan of Imaginary Authors,
  run from the Commission Signal Board first. Evaluates CSB-nominated venues
  for current public venue value, records hidden venue pointers, screen-light
  observations, negatives, access notes, and bounded capture_request handoffs
  without capture, route binding, gate clearance, demand proof, buyer proof, or
  client-facing output.
use_when:
  - Reviewing the corrected CSB-first scanning rehearsal for Imaginary Authors.
  - Comparing CSB-nominated venues against hidden venues found by scanning.
  - Deciding whether Capture should preserve specific volatile public source states.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/product-planning/imaginary_authors_csb_first_venue_eval_scanning_commission_prompt_v0.md
  - docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md
  - orca/product/spines/scanning/README.md
  - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  - orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_mgt_v0.md
stale_if:
  - Any promoted observation is used after the 21-day forward scan-to-use window
    without fresh re-verification.
  - Imaginary Authors, Ministry of Scent, Anthropologie, or the cited editorial
    surfaces change the observed availability, review-count, listing, or article state.
  - Capture verifies, rejects, or supersedes any capture_request below.
```

## Scan Intake Receipt

```yaml
scan_receipt_version: 0
commission_id: scanning_mgt_imaginary_authors_csb_first_venue_eval_v0
scan_date: 2026-06-21
mode: forward
subject: Imaginary Authors
market_or_geography: US indie/DTC fragrance
run_caps:
  max_screening_moves_total: 18
  max_active_venue_frontier_branches: 5
  max_promoted_observations: 4
  max_hidden_venue_pointers: 4
  max_capture_requests: 2
source_context_status: SOURCE_CONTEXT_READY
screening_moves_used: 14
active_frontier_branches_used: 5
promoted_observations: 4
hidden_venue_pointers: 1
capture_requests: 2
closeout_state: SCAN_COMPLETE
prior_artifact_non_edit_statement: >
  docs/research/orca_discovery_candidate_scan_imaginary_authors_mgt_v0.md was
  read only as prior-run context and anti-repeat evidence. It was not edited.
```

Source context loaded before applying the MGT model: `AGENTS.md`,
`.agents/workflow-overlay/README.md`, Orca Cynefin routing, the CSB board,
scanning README, MGT intelligent-walk operating model, vertical exploration
guide, targeted forward / promotion / capture_request sections of the demand
scan-core spec, and the prior Imaginary Authors MGT scan for anti-repeat only.

Non-goals preserved: no crawler, monitor, registry, atlas, scraping, login,
private/auth-gated access, LinkedIn live read, TikTok/Instagram live read,
creator/social access, packet-grade capture, ECR, Cleaning, Judgment, gate
verdict, buyer proof, demand proof, source-class ratification, route binding,
or client-facing output.

## CSB Board Intake

Board source:
`docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md`.

Rows consumed as route map: SBR-001 through SBR-010.

Rows skipped for live access:

- `SBR-008 AEO`: consumed as visibility provenance only; no live answer-engine
  read was run.
- `SBR-009 creator/social`: recorded as planned/deferred per commission; no
  live TikTok, Instagram, or creator-surface read was run.
- LinkedIn portions of `SBR-010`: skipped per commission; org-motion checks
  used public official, retailer, partner, and editorial surfaces only.

## Venue Evaluation Ledger

### Move Log

| Move | CSB row(s) | Venue / frontier | Value class | What happened | Stop check |
| --- | --- | --- | --- | --- | --- |
| M01 | SBR-001 | Imaginary Authors fragrance collection, `https://imaginaryauthors.com/collections/frontpage` | valuable venue | Official fragrance surface listed current assortment, including `A LITTLE SECRET`, `Dipped in Chocolate`, and 22 fragrance products; the visible filter showed 21 in stock and 1 out of stock. | a:no b:no c:no |
| M02 | SBR-001, SBR-010 | Imaginary Authors all-products collection, `https://imaginaryauthors.com/collections/all` | valuable venue | Broader official assortment showed 71 products with 68 in stock and 5 out of stock; it exposed `A LITTLE SECRET`, `Dipped in Chocolate`, and current candle assortment context. | a:no b:no c:no |
| M03 | SBR-001 | Official `A LITTLE SECRET` PDP, `https://imaginaryauthors.com/products/a-little-secret` | valuable venue | PDP exposed current SKU/variant state: 50ml and 2ml purchasable, with the 50ml + Mug bundle sold out and restock-notify UI present. | a:no b:no c:no |
| M04 | SBR-001, SBR-010 | Official `Dipped in Chocolate` PDP, `https://imaginaryauthors.com/products/dipped-in-chocolate` | valuable venue | PDP exposed current product story, Salt & Straw partnership language, and official product availability context. | a:no b:no c:no |
| M05 | SBR-002, SBR-006 | Ministry of Scent Imaginary Authors collection, `https://ministryofscent.com/collections/imaginary-authors` | valuable venue | Retailer collection showed current assortment and sample/review route value, including `First Peach of the Season` with sample add enabled and one review. | a:no b:no c:no |
| M06 | SBR-002, SBR-006 | Ministry product-detail / quickview attempts for `A Little Secret`, `First Peach of the Season`, and `Dipped in Chocolate` | access_note | Direct product-detail routes did not yield stable readable PDP text through the scan tool; the collection page remained readable enough for listing/review-count venue evaluation. | a:no b:no c:no |
| M07 | SBR-003, SBR-007 | Allure peach-fragrance trend article, `https://www.allure.com/story/peach-perfumes-trend-summer-2026` | low-value venue / visibility route | June 19, 2026 editorial article included `First Peach of the Season` in a peach-fragrance trend list and supplied category visibility, not demand-origin proof. | a:no b:no c:no |
| M08 | SBR-004, SBR-010 | Livingetc Anthropologie candle-collab article, `https://www.livingetc.com/shopping/imaginary-authors-anthropologie-candles` | valuable pointer | January 23, 2026 editorial article pointed to Imaginary Authors x Anthropologie candle products and named the three-candle discovery set route. | a:no b:no c:no |
| M09 | SBR-007, SBR-010 | Anthropologie UK partner PDP, `https://www.anthropologie.com/en-gb/shop/imaginary-authors-x-anthropologie-discovery-set` | hidden_venue_pointer | Direct partner PDP showed the discovery set live with add-to-basket flow, 2 reviews, and product details. Surface is UK/Anthropologie, so it is partner/org-motion context, not US demand-origin proof. | a:no b:no c:no |
| M10 | SBR-001, SBR-010 | Imaginary Authors candles collection, `https://imaginaryauthors.com/collections/candles-1` | low-value venue / negative | Official candle collection showed 12 in-stock owned candles, including `IS THIS STILL LIFE`, but did not expose the Anthropologie collaboration products on the owned collection surface. | a:no b:no c:no |
| M11 | SBR-010 | Imaginary Authors wholesale page, `https://imaginaryauthors.com/pages/wholesale` | low-value venue | Public wholesale page showed stockist-intake posture only; useful as channel context, not a current allocation, launch, or retailer decision signal. | a:no b:no c:no |
| M12 | SBR-005, SBR-006, SBR-007 | Exact product/community/review searches for `A Little Secret`, `Dipped in Chocolate`, and `First Peach of the Season` | negative | Public search surfaced editorial/retailer context already read, but no better independent public community-origin venue inside the cap. | a:no b:branch-close c:no |
| M13 | SBR-005, SBR-006, SBR-007 | Specialist review/forum search cluster: Fragrantica, Parfumo, Basenotes, Reddit keywords | access_note / negative | Search and direct-route attempts did not surface readable product-specific review text through public unauthenticated paths. Reddit/Basenotes-style real reads remain orchestrator-mediated, not direct scan work. | a:no b:branch-close c:no |
| M14 | SBR-007, SBR-010 | Salt & Straw partnership search cluster, including Food & Wine 2022 Salt & Straw/Imaginary Authors coverage | observation / low-value venue | Found historical collaboration context for Salt & Straw and Imaginary Authors, but no current original Salt & Straw source for `Dipped in Chocolate` inside the cap. | a:no b:no c:no |

Declared frontier branches:

- B1 owned official surfaces: productive for chronology, current SKU, and
  availability state; not independent demand proof.
- B2 retailer/review surfaces: productive for assortment and review-count
  routing; product-review text did not become readable inside the scan.
- B3 editorial/trade/partner surfaces: useful for visibility and partner
  pointers; mostly downstream/corroborative.
- B4 public community/review discovery: dry or access-limited inside the cap.
- B5 AEO/creator/social/org-boundary surfaces: mostly deferred by commission
  or limited to public non-social org surfaces.

Stop reason: the CSB-nominated and discovered public venues had decayed to low
or boundary-bound expected value after 14 moves. The remaining useful work
would be Capture-owned preservation or orchestrator-mediated public community
screening, not more screen-light scan moves.

### CSB Row Disposition

| CSB row | Value class | Dry / blocked state | Stop reason |
| --- | --- | --- | --- |
| SBR-001 owned channels | Valuable venue | Productive | Official pages reveal current assortment, SKU availability, sold-out/restock-notify states, and owned chronology. |
| SBR-002 retail/PDP | Valuable venue | Productive with detail-route access note | Ministry of Scent gives assortment and review-count context; retail remains channel corroboration, not demand-origin proof. |
| SBR-003 editorial/trade | Low-value venue / visibility route | Productive but non-origin | Allure provides fresh category visibility for `First Peach of the Season`; no independent buyer-origin signal. |
| SBR-004 editorial/channel article | Valuable pointer | Productive | Livingetc points to a partner PDP; editorial itself is visibility/channel context only. |
| SBR-005 forums/community | Access note / negative | Boundary-bound | No public product-specific community origin surfaced through unauthenticated search; Reddit/Basenotes-style reads stay orchestrator-mediated. |
| SBR-006 reviews | Low-value venue with access note | Partially productive | Review counts surfaced on Ministry and Anthropologie; review text was not readable enough for demand-origin use. |
| SBR-007 search discovery | Valuable for route discovery | Productive then decayed | Found one hidden partner PDP and decisive negatives; search is route discovery only. |
| SBR-008 AEO | Observation / skipped live | Deferred by boundary | Treated as visibility provenance only; no live AEO read. |
| SBR-009 creator/social | Planned/deferred | Skipped by boundary | No TikTok, Instagram, or creator/social live read. |
| SBR-010 org motion | Valuable pointer / low-value venue | Productive | Anthropologie partner PDP and official wholesale page provide org/channel context; LinkedIn skipped. |

## Hidden Venue Pointers

```yaml
hidden_venue_pointer_id: HVP-001
source_move_id: M09
venue: Anthropologie UK partner PDP
url: https://www.anthropologie.com/en-gb/shop/imaginary-authors-x-anthropologie-discovery-set
retrieval_date: 2026-06-21
why_hidden_from_csb: >
  The CSB row named the Livingetc editorial article, not the direct partner PDP
  exposed through the article's product route.
why_value_bearing: >
  The direct PDP exposes current product availability posture, review count,
  partner product details, and original retailer context for the Imaginary
  Authors x Anthropologie candle discovery set.
limits: >
  The reached page is an Anthropologie UK surface. It is useful for org-motion
  and channel evaluation, but not US demand-origin proof and not route binding.
recommended_next_owner: Capture, only if partner-surface preservation matters.
```

## Screen-Light Observations

```yaml
observation_id: OBS-001
source_move_id: M01, M02, M03, M05
url:
  - https://imaginaryauthors.com/collections/frontpage
  - https://imaginaryauthors.com/collections/all
  - https://imaginaryauthors.com/products/a-little-secret
  - https://ministryofscent.com/collections/imaginary-authors
retrieval_date: 2026-06-21
short_quote_or_summary: >
  Official owned surfaces show current `A LITTLE SECRET` assortment; the PDP
  shows 50ml and 2ml purchase routes with the 50ml + Mug bundle sold out, while
  Ministry of Scent lists the brand/SKU route.
signal_stage: venue_value
claim_it_might_support: >
  Current launch/assortment and variant-availability venue value for an
  Imaginary Authors fragrance SKU.
gate_role: decision_event
independence_hypothesis: >
  Owned official state plus retailer listing are channel/chronology
  corroboration, not independent demand-origin evidence.
uncertainty_or_limits: >
  No public buyer-origin review/community language was reached for this SKU
  inside the cap; no candidate minted.
```

```yaml
observation_id: OBS-002
source_move_id: M02, M04, M14
url:
  - https://imaginaryauthors.com/collections/all
  - https://imaginaryauthors.com/products/dipped-in-chocolate
  - https://www.foodandwine.com/news/edible-perfume-ice-cream-salt-straw
retrieval_date: 2026-06-21
short_quote_or_summary: >
  Official surfaces keep `Dipped in Chocolate` visible as a fragrance product
  and the PDP describes a Salt & Straw partnership; historical Food & Wine
  coverage confirms earlier Salt & Straw/Imaginary Authors collaboration
  context but not current `Dipped in Chocolate` demand.
signal_stage: precursor
claim_it_might_support: >
  Current owned product/partnership context for a collaboration fragrance, with
  possible volatile availability state to preserve if this lane is continued.
gate_role: decision_event
independence_hypothesis: >
  The official PDP and old editorial/history route share brand/partner context;
  they do not create independent demand-origin support.
uncertainty_or_limits: >
  No current original Salt & Straw page or independent buyer-origin venue was
  found inside the cap.
```

```yaml
observation_id: OBS-003
source_move_id: M05, M07
url:
  - https://ministryofscent.com/collections/imaginary-authors
  - https://www.allure.com/story/peach-perfumes-trend-summer-2026
retrieval_date: 2026-06-21
short_quote_or_summary: >
  Ministry of Scent lists `First Peach of the Season` with sample add enabled
  and one review; Allure's June 19, 2026 peach-fragrance trend article includes
  Imaginary Authors' `First Peach of the Season` in a product list.
signal_stage: precursor
claim_it_might_support: >
  Current retail/editorial visibility and route value for an Imaginary Authors
  peach fragrance during a fresh peach-fragrance editorial cycle.
gate_role: influence
independence_hypothesis: >
  Retail listing and editorial trend placement are downstream visibility/channel
  surfaces; they do not establish independent demand-origin behavior.
uncertainty_or_limits: >
  Review text and official product metadata were not reached through a better
  public route inside the scan cap.
```

```yaml
observation_id: OBS-004
source_move_id: M08, M09, M10, M11
url:
  - https://www.livingetc.com/shopping/imaginary-authors-anthropologie-candles
  - https://www.anthropologie.com/en-gb/shop/imaginary-authors-x-anthropologie-discovery-set
  - https://imaginaryauthors.com/collections/candles-1
  - https://imaginaryauthors.com/pages/wholesale
retrieval_date: 2026-06-21
short_quote_or_summary: >
  Livingetc points to an Imaginary Authors x Anthropologie candle set; the
  direct Anthropologie UK PDP shows a live discovery set with two reviews and
  product details; owned IA candle and wholesale surfaces give adjacent channel
  context but do not expose the collaboration directly.
signal_stage: venue_value
claim_it_might_support: >
  Partner-channel/org-motion venue value adjacent to fragrance, especially
  where hidden direct retailer PDPs can reveal availability and review-count
  state.
gate_role: org_motion
independence_hypothesis: >
  Partner retailer plus editorial article are useful channel surfaces, but the
  candle category is adjacent to the commissioned fragrance seed and the reached
  partner PDP is UK-surfaced.
uncertainty_or_limits: >
  Not a fragrance-demand origin; no LinkedIn live access, creator/social access,
  or route binding was performed.
```

## Candidate Observation Decision

No candidate minted.

Reason: the fresh scan found useful venue value and precursor surfaces, but did
not meet promotion rules for a candidate observation. The strongest signals are
owned availability/product chronology, retailer listings or review counts,
editorial visibility, and partner-channel context. These do not show two
effectively independent demand-origin venues, do not expose gradeable
costly-behavior evidence from an independent origin, and do not clear the
commission's no-demand-proof boundary.

Forward-mode note: if a future lane wants to use any load-bearing observation
for slot qualification, the 21-day scan-to-use window applies from
2026-06-21 and the observation must be re-verified after 2026-07-12.

## Capture Requests

```yaml
capture_request_id: CR-001
source_scan: scanning_mgt_imaginary_authors_csb_first_venue_eval_v0
candidate_or_observation_ids:
  - OBS-001
  - OBS-002
urls:
  - url: https://imaginaryauthors.com/products/a-little-secret
    venue: Imaginary Authors official PDP
    observation_supported: Current variant availability for A Little Secret, including sold-out bundle state.
    gate_role: decision_event
  - url: https://imaginaryauthors.com/products/dipped-in-chocolate
    venue: Imaginary Authors official PDP
    observation_supported: Current official product and Salt & Straw partnership context for Dipped in Chocolate.
    gate_role: decision_event
what_capture_should_verify: >
  Preserve the current official PDP states, exact variants, availability /
  restock-notify posture, and visible partnership copy if the next lane wants
  packet-grade provenance for these volatile owned source states.
decision_window: 2026-06-21 to 2026-07-12
route_binding_state: unknown
screening_evidence_summary: >
  Screen-light reads found current official SKU/availability and partnership
  context, but no independent demand-origin evidence.
uncertainty_or_access_limits: >
  Capture owns route choice, entitlement/source policy, and packet-grade
  preservation. Scanning is not asking for route expansion, ECR, Cleaning, or
  Judgment.
not_requested:
  - route expansion
  - packet commitment by scanning
  - ECR, Cleaning, or Judgment work
```

```yaml
capture_request_id: CR-002
source_scan: scanning_mgt_imaginary_authors_csb_first_venue_eval_v0
candidate_or_observation_ids:
  - OBS-004
urls:
  - url: https://www.anthropologie.com/en-gb/shop/imaginary-authors-x-anthropologie-discovery-set
    venue: Anthropologie UK partner PDP
    observation_supported: Hidden partner PDP for Imaginary Authors x Anthropologie discovery set, with add-to-basket posture and two reviews.
    gate_role: org_motion
what_capture_should_verify: >
  Preserve the direct partner PDP state if partner-channel evidence matters,
  including whether the visible reachable surface is UK-only and whether any
  Capture-approved public counterpart exists.
decision_window: 2026-06-21 to 2026-07-12
route_binding_state: unknown
screening_evidence_summary: >
  The CSB named the Livingetc article; scanning found a direct partner PDP
  through the article route. This is a hidden venue pointer and org-motion
  surface, not demand proof.
uncertainty_or_access_limits: >
  UK partner page and adjacent candle category limit direct fit to US
  indie/DTC fragrance. Capture owns any route and provenance method.
not_requested:
  - route expansion
  - packet commitment by scanning
  - ECR, Cleaning, or Judgment work
```

## Negatives And Access Notes

- `NEG-001`: `SBR-005` public forum/community search did not surface a better
  product-specific public origin venue for `A Little Secret`, `Dipped in
  Chocolate`, or `First Peach of the Season` inside the cap.
- `ACCESS-001`: Reddit/Basenotes-style real community reads were not pursued
  directly. The loaded walk contract treats these as wall-prone or
  orchestrator-mediated screening reads; this scan records the need rather than
  crossing into direct capture, scraping, or auth-gated access.
- `ACCESS-002`: Ministry of Scent collection text was readable and useful, but
  direct product-detail / quickview routes did not yield stable review text
  through the scan tool.
- `NEG-002`: `SBR-006` review venues yielded review counts, not readable dated
  review language sufficient for demand-origin use.
- `NEG-003`: `SBR-008` AEO and `SBR-009` creator/social were not run live;
  they remain visibility/deferred lanes under the commission boundary.
- `NEG-004`: Official candles and wholesale pages provided adjacent channel
  context, but no owned official page for the Anthropologie collaboration was
  found in the owned candle collection during this scan.
- `NEG-005`: Salt & Straw searches found historical collaboration context, but
  no current original Salt & Straw source for `Dipped in Chocolate` inside the
  cap.

## Closeout

`SCAN_COMPLETE`.

Next lane may:

- use the venue ledger to compare CSB-nominated venues against actual venue
  value;
- route `CR-001` and/or `CR-002` to Capture if volatile official or partner
  source-state preservation matters;
- run orchestrator-mediated public community screening only if the owner wants
  independent demand-origin testing beyond this scan;
- discard or re-verify this artifact after 2026-07-12 for any forward
  load-bearing use.

Next lane must not:

- treat this artifact as validation, readiness, demand proof, buyer proof, gate
  clearance, candidate admission, source-class ratification, or a client-facing
  output;
- use the prior MGT scan artifact as fresh forward evidence;
- infer route binding, capture permission, packet commitment, ECR, Cleaning,
  Judgment, outreach, buyer contact, live social access, or standing monitoring
  from this scan.
