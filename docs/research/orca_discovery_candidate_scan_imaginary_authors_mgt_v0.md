# Orca Discovery Candidate Scan - Imaginary Authors MGT v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact (bounded MGT screen-light targeted scan)
scope: >
  One commissioned forward-mode bounded intelligent-walk scan of Imaginary
  Authors as a US indie/DTC fragrance seed. Records public venue-value signals,
  hidden-venue gaps, negatives, access notes, and only capture_request handoffs
  that satisfy the capture-request promotion bar, without capture, judgment,
  demand proof, route binding, or buyer proof.
use_when:
  - Reviewing the first controlled targeted scanning-lane rehearsal for a
    CSB-derived fragrance brand.
  - Deciding whether any Imaginary Authors public assortment, SKU, launch,
    restock, channel, or discontinuation signal should route to Capture.
  - Checking why no forward candidate observation was minted from this scan.
authority_boundary: retrieval_only
open_next:
  - docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md
  - docs/prompts/product-planning/imaginary_authors_csb_seeded_scanning_mgt_commission_prompt_v0.md
  - orca/product/spines/scanning/README.md
  - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  - orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
stale_if:
  - Any promoted observation is used after the 21-day forward scan-to-use window
    without fresh re-verification.
  - Imaginary Authors changes the observed official PDP, collection,
    availability, or restock-notify state.
  - Capture verifies, rejects, or supersedes any capture_request below.
```

## Scan Intake Receipt

```yaml
commission_id: scanning_mgt_imaginary_authors_csb_seed_v0
scan_date: 2026-06-21
mode: forward
subject: Imaginary Authors
market_or_geography: US indie/DTC fragrance
run_caps:
  max_screening_moves_total: 18
  max_active_frontier_branches: 5
  max_promoted_observations: 4
  max_capture_requests: 3
source_context_status: SOURCE_CONTEXT_READY
screening_moves_used: 10
active_frontier_branches_used: 5
promoted_observations: 4
capture_requests: 2
closeout_state: SCAN_COMPLETE
```

Source context loaded: `AGENTS.md`, `.agents/workflow-overlay/README.md`,
Orca Cynefin routing, scanning README, MGT intelligent-walk operating model,
vertical exploration guide, targeted demand scan-core sections, Commission
Signal Board playbook, AEO phase-0 seed evidence, the fragrance candidate pool
handoff, and the CSB forward board at
`docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md`.
This follow-up treats the CSB board as the upstream venue/source-family map;
fresh public re-checks on 2026-06-21 found no material drift from the prior
screen-light observations and no new independent demand-origin venue inside the
run cap. The historical Imaginary Authors pool row was used only as a
decision-shape precedent; it is not cited below as forward evidence.

Non-goals: no crawler, monitor, registry, atlas, capture packet, ECR, Cleaning,
Judgment, buyer contact, gate verdict, demand proof, buyer proof, route binding,
or client-facing output.

## Frontier Ledger

| Move | Frontier | Yield class | What happened | Stop check |
| --- | --- | --- | --- | --- |
| M01 | Official Imaginary Authors fragrance collection, `https://imaginaryauthors.com/collections/frontpage` | EVIDENCE | Current official fragrance surface listed 22 products, with `UNTAMABLE`, `A LITTLE SECRET`, `HOW TO SAY BICYCLE IN FRENCH`, and a sold-out `Beach Reads` sample set visible; collection availability summary showed 21 in stock and 1 out of stock on the first page. | a:no b:no c:no |
| M02 | Official all-products collection, `https://imaginaryauthors.com/collections/all` | EVIDENCE | Broader official assortment showed `A LITTLE SECRET - FRAGRANCE` marked `New`, `Dipped in Chocolate - FRAGRANCE` marked sold out, `IS THIS STILL LIFE - CANDLE` marked `New`, and 68 in-stock / 5 out-of-stock products across 71 results. | a:no b:no c:no |
| M03 | Official `A LITTLE SECRET` PDP, `https://imaginaryauthors.com/products/a-little-secret` | EVIDENCE | Current official PDP showed 50ml and 2ml purchasable while `50ml + Mug` was sold out; notes and launch story are visible. | a:no b:no c:no |
| M04 | Official `Dipped in Chocolate` PDP, `https://imaginaryauthors.com/products/dipped-in-chocolate` | EVIDENCE | Current official PDP showed the 50ml SKU sold out, restock-notify UI, and Salt & Straw partnership language. | a:no b:no c:no |
| M05 | Ministry of Scent Imaginary Authors collection, `https://ministryofscent.com/collections/imaginary-authors` | EVIDENCE | Retailer collection showed 28 Imaginary Authors products, including `A Little Secret`, `Untamable`, sample-set sellouts, and `First Peach of the Season` with sample add enabled and one review. | a:no b:no c:no |
| M06 | Allure peach-trend article, `https://www.allure.com/story/peach-perfumes-trend-summer-2026` | EVIDENCE | Fresh editorial surface published 2026-06-19 placed an Imaginary Authors peach perfume inside a 2026 peach-fragrance trend. | a:no b:no c:no |
| M07 | Livingetc Anthropologie candle-collab article, `https://www.livingetc.com/shopping/imaginary-authors-anthropologie-candles` | EVIDENCE | January 2026 editorial surface reported an Imaginary Authors x Anthropologie candle trio/discovery-set collaboration. | a:no b:no c:no |
| M08 | Exact public search for `First Peach of the Season`, `Dipped in Chocolate`, and `A Little Secret` community/review traces | VENUE-DRY | Search did not surface a better public, product-specific community origin within the cap beyond the retailer/editorial surfaces already read. | a:no b:branch-close c:no |
| M09 | Public search around `Whispered Myths`, `Telegrama`, and discontinued-tag vocabulary | VENUE-DRY | No current public forward-mode source surfaced inside the cap; an irrelevant generic `telegram` result appeared and was discarded. Historical pool row not used as evidence. | a:no b:branch-close c:no |
| M10 | CSB/AEO seed-query family search around `top indie perfume brands in the US` | INFLUENCE-OBS | Current search returned broader category surfaces, including fresh peach/niche fragrance coverage; useful as visibility annotation only, not demand-origin proof. | a:no b:no c:no |

Declared frontiers closed:

- Official owned site and product surfaces: productive, but owned-only.
- Retail/PDP surfaces: productive through Ministry of Scent; retail is G4/channel corroboration only.
- Specialist community surfaces: dry inside cap; Reddit/Basenotes-style real reads remain orchestrator-mediated if needed.
- Search/AEO surfaces: visibility annotation only; no independent demand-origin proof.
- News/editorial/trade mentions: productive for trend/channel context; not sufficient to mint a candidate.

Stop reason: all remaining public frontiers had decayed to low expected value
inside the move cap, and the next useful work would be Capture-owned
preservation or orchestrator-mediated public community screening.

## CSB-First Venue Evaluation

| Venue eval ID | CSB row(s) checked | Venue / route | Current venue value | Capture / route decision |
| --- | --- | --- | --- | --- |
| VE-001 | SBR-001 | Imaginary Authors official collections and PDPs | High venue value for volatile owned chronology: official collection/all-products surfaces still show current assortment, `A LITTLE SECRET` as `New`, `Dipped in Chocolate` sold out, and PDP-level variant/restock UI. | Keep CR-001 and CR-002; Capture owns preservation and route binding. Owned state is not demand proof. |
| VE-002 | SBR-002, SBR-006 | Ministry of Scent collection/review route | Medium venue value for retailer corroboration and review routing: collection shows 28 Imaginary Authors products, `A Little Secret` with no reviews, and `First Peach of the Season` with sample add enabled and one review. | No new capture request. Useful child route if a later lane needs review text, but aggregate counts are insufficient. |
| VE-003 | SBR-003 | Allure peach-fragrance article | Low-to-medium venue value as current editorial/category visibility: 2026-06-19 article includes `First Peach of the Season`. | No capture request. Treat as visibility/source route and campaign-overlap check, not demand-origin evidence. |
| VE-004 | SBR-004, SBR-010 | Livingetc / Anthropologie candle collaboration | Low venue value for this fragrance-scoped run, but useful adjacent org-motion context for home fragrance/channel expansion. | No capture request unless the subject broadens to home fragrance or partner-channel movement. |
| VE-005 | SBR-005, SBR-006, SBR-007 | Public community, review, and exact-query discovery | Low yield inside this cap: exact public searches did not surface a better independent product-specific origin than owned/retail/editorial routes. | No hidden venue pointer promoted. Reddit/Basenotes-style reads remain orchestrator-mediated public screening if later justified. |
| VE-006 | SBR-008 | Search/AEO seed-query family | Visibility annotation only: seed evidence explains why Imaginary Authors entered the workstream and where cited-source ecosystems may point. | Excluded from demand-origin and classifier claims. No capture request. |

## Hidden Venue Pointer Decision

No `hidden_venue_pointer` was promoted in this CSB-first follow-up. The only
child routes worth preserving as follow-up notes were Ministry of Scent
product/review pages for exact SKUs and orchestrator-mediated public community
reads; neither met the bar for a high-yield hidden venue requiring Capture-owned
acquisition in this run.

## Screen-Light Observations

```yaml
observation_id: OBS-001
source_move_id: M02, M03, M05
url:
  - https://imaginaryauthors.com/collections/all
  - https://imaginaryauthors.com/products/a-little-secret
  - https://ministryofscent.com/collections/imaginary-authors
retrieval_date: 2026-06-21
short_quote_or_summary: >
  Official all-products collection marks A LITTLE SECRET as New; official PDP
  shows 50ml and 2ml available, while 50ml + Mug is sold out; Ministry of
  Scent also lists A Little Secret.
signal_stage: venue_value
claim_it_might_support: >
  Current launch/assortment signal for a new Imaginary Authors fragrance SKU
  with a limited/bundled variant already unavailable.
gate_role: decision_event
independence_hypothesis: >
  Owned official source plus retailer listing are corroborative channel
  surfaces, not independent demand-origin receipts.
uncertainty_or_limits: >
  No public demand-origin or costly-behavior floor was found inside the scan
  cap; no candidate minted.
```

```yaml
observation_id: OBS-002
source_move_id: M02, M04
url:
  - https://imaginaryauthors.com/collections/all
  - https://imaginaryauthors.com/products/dipped-in-chocolate
retrieval_date: 2026-06-21
short_quote_or_summary: >
  Official all-products collection marks Dipped in Chocolate sold out; the PDP
  shows the 50ml SKU sold out, restock-notify UI, and a Salt & Straw
  partnership.
signal_stage: venue_value
claim_it_might_support: >
  Current sold-out/restock venue-value signal for a collaboration fragrance SKU.
gate_role: decision_event
independence_hypothesis: >
  Owned official availability state only; partnership language indicates org
  motion but not independent demand.
uncertainty_or_limits: >
  The scan did not find current independent buyer-origin evidence or a restock
  date; the signal is capture-worthy only if the lane wants to preserve the
  official availability state.
```

```yaml
observation_id: OBS-003
source_move_id: M05, M06, M10
url:
  - https://ministryofscent.com/collections/imaginary-authors
  - https://www.allure.com/story/peach-perfumes-trend-summer-2026
retrieval_date: 2026-06-21
short_quote_or_summary: >
  Ministry of Scent lists First Peach of the Season with sample add enabled and
  one review; Allure's 2026-06-19 peach-fragrance trend includes an Imaginary
  Authors peach perfume.
signal_stage: venue_value
claim_it_might_support: >
  Current retail/editorial signal around an Imaginary Authors peach SKU and a
  fresh category trend surface.
gate_role: influence
independence_hypothesis: >
  Retail and editorial surfaces are likely downstream visibility/channel
  surfaces; they do not establish independent buyer demand.
uncertainty_or_limits: >
  The official PDP for First Peach of the Season was not reached inside the cap,
  and the article did not expose enough product metadata in the accessible text
  to bind the exact SKU without Capture re-check.
```

```yaml
observation_id: OBS-004
source_move_id: M02, M07
url:
  - https://imaginaryauthors.com/collections/all
  - https://www.livingetc.com/shopping/imaginary-authors-anthropologie-candles
retrieval_date: 2026-06-21
short_quote_or_summary: >
  Official all-products collection marks Is This Still Life candle New; a
  January 2026 Livingetc article reports an Imaginary Authors x Anthropologie
  trio of nostalgic candles.
signal_stage: venue_value
claim_it_might_support: >
  Assortment/channel expansion signal adjacent to fragrance, especially home
  fragrance/candle SKU activity.
gate_role: org_motion
independence_hypothesis: >
  Official assortment plus editorial/channel coverage are useful org-motion
  context, not demand-origin evidence.
uncertainty_or_limits: >
  Candle/home-fragrance signal is adjacent to the commissioned fragrance seed;
  no capture request emitted unless a later lane broadens the subject to home
  fragrance assortment decisions.
```

## Candidate Observation Decision

No candidate minted.

Reason: the scan found several current venue-value signals worth preserving or
checking, but none met the forward candidate-promotion threshold. The live
signals were owned availability states, retailer listings, and editorial/search
visibility. They did not show a gradeable costly-behavior floor in an
independent demand-origin venue, and laundered/channel surfaces cannot be
double-counted as demand origins. Retail presence stays G4/channel
corroboration only.

## Capture Requests

```yaml
capture_request_id: CR-001
source_scan: scanning_mgt_imaginary_authors_csb_seed_v0
candidate_or_observation_ids:
  - OBS-001
urls:
  - url: https://imaginaryauthors.com/products/a-little-secret
    venue: Imaginary Authors official PDP
    observation_supported: A Little Secret current launch/new SKU and variant availability state
    gate_role: decision_event
  - url: https://ministryofscent.com/collections/imaginary-authors
    venue: Ministry of Scent retailer collection
    observation_supported: Retail channel listing for A Little Secret
    gate_role: org_motion
what_capture_should_verify: >
  Preserve current official PDP state, exact variants, availability, and
  retailer listing; check whether any review/community origin is reachable
  through Capture-approved public routes.
decision_window: 2026-06-21 to 2026-07-12
route_binding_state: unknown
screening_evidence_summary: >
  Official all-products page marks A Little Secret as New; official PDP shows
  active 50ml/2ml purchase options and a sold-out 50ml + Mug option; Ministry
  of Scent lists the SKU.
uncertainty_or_access_limits: >
  Screening did not resolve launch date, review provenance, or buyer-origin
  demand; Capture owns any route and preservation method.
not_requested:
  - route expansion
  - packet commitment by scanning
  - ECR, Cleaning, or Judgment work
```

```yaml
capture_request_id: CR-002
source_scan: scanning_mgt_imaginary_authors_csb_seed_v0
candidate_or_observation_ids:
  - OBS-002
urls:
  - url: https://imaginaryauthors.com/products/dipped-in-chocolate
    venue: Imaginary Authors official PDP
    observation_supported: Sold-out 50ml SKU, restock-notify UI, Salt & Straw partnership
    gate_role: decision_event
what_capture_should_verify: >
  Preserve the official sold-out/restock-notify state and determine whether a
  public restock, launch, or limited-allocation explanation exists on
  Capture-approved public surfaces.
decision_window: 2026-06-21 to 2026-07-12
route_binding_state: unknown
screening_evidence_summary: >
  Official PDP showed Dipped in Chocolate sold out with Notify Me/restock UI
  and partnership language.
uncertainty_or_access_limits: >
  Owned-only signal; no independent demand-origin evidence found in screening.
not_requested:
  - route expansion
  - packet commitment by scanning
  - ECR, Cleaning, or Judgment work
```

## Venue Follow-Up Notes

- `VFN-001`: Ministry of Scent plus Allure peach-fragrance visibility remains a
  venue-value note, not a Capture request under the tightened promotion bar.
  It is useful for a later review/community venue test, but it lacks volatile
  source state, source-access blockage, near-promoted candidate support, or a
  high-yield hidden venue requiring Capture-owned acquisition.

## Negatives And Access Notes

- `NEG-001`: Exact public searches for `Whispered Myths`, `Telegrama`, and
  discontinued-tag vocabulary did not surface a current forward-mode public
  signal inside the cap. The known historical SKU-kill row remains decision
  shape only, not current evidence.
- `NEG-002`: Exact product/community searches around `First Peach of the
  Season`, `Dipped in Chocolate`, and `A Little Secret` did not surface a
  better public origin than the official/retailer/editorial surfaces above.
- `ACCESS-001`: Reddit/Basenotes-style real community reads were not pursued
  directly. The loaded walk contract treats these as wall-prone or
  orchestrator-mediated screening reads; this scan records the need rather than
  crossing into direct capture or auth-gated access.
- `NEG-003`: AEO/search surfaces produced visibility and category context, not
  independent demand-origin proof, and were not promoted beyond venue-value
  routing.

## Closeout

`SCAN_COMPLETE`.

Next lane may:

- re-fetch and preserve the two capture_request URL sets under Capture-owned
  route, entitlement, and provenance rules;
- run an orchestrator-mediated public community screening read only if Capture
  or the owner wants to test independent demand-origin surfaces for the three
  venue-value clusters;
- discard this scan after 2026-07-12 for forward slot use unless the
  load-bearing observations are freshly re-verified.

Next lane must not:

- treat this artifact as validation, readiness, demand proof, buyer proof, gate
  clearance, candidate admission, or source-class ratification;
- use the 2024 historical Imaginary Authors backtest row as a forward-mode slot
  source;
- infer route binding, capture permission, packet commitment, ECR, Cleaning, or
  Judgment work from this scan.
