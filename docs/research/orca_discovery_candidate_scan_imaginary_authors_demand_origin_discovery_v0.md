# Orca Discovery Candidate Scan - Imaginary Authors Demand-Origin Discovery v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact (fresh CSB-first demand-origin discovery scan)
scope: >
  Fresh bounded follow-up to the Imaginary Authors core-satellite CSB scan.
  Starts from the CSB board and returned scan, then tests the unresolved public
  buyer-origin and hidden-venue question for A Little Secret, Dipped in
  Chocolate, and First Peach of the Season. Records venue value, exact-query
  negatives, access notes, capture-preservation triage, and candidate decision
  without editing the returned scan artifact or minting proof by implication.
use_when:
  - Reviewing the post-CSB discovery pass for Imaginary Authors.
  - Deciding whether public buyer-origin venues exist beyond owned, retailer,
    editorial, and partner/channel surfaces.
  - Triage-reading the returned scan's capture requests before any Capture-owned
    preservation work.
authority_boundary: retrieval_only
open_next:
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md
  - docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md
  - orca/product/spines/scanning/README.md
  - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  - orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
stale_if:
  - Any observation is used after 2026-07-13 without fresh re-verification.
  - Imaginary Authors, Ministry of Scent, Luckyscent, Anthropologie, Allure,
    Livingetc, Food & Wine, or cited search results change the observed source
    state.
  - Capture verifies, rejects, or supersedes the preservation-only capture
    requests carried forward below.
```

## Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S0 + scanning CSB/MGT target pack
  edit_permission: docs-write
  target_scope: docs/research fresh scanning discovery artifact plus repo-map pointer
  dirty_state_checked: yes
  blocked_if_missing: source context, public-source reads, validation checks
```

```yaml
commission_id: scanning_mgt_imaginary_authors_demand_origin_discovery_v0
scan_date: 2026-06-22
mode: forward
subject: Imaginary Authors
market_or_geography: US indie/DTC fragrance
source_context_status: SOURCE_CONTEXT_READY
public_source_status: PUBLIC_READS_READY
entry_route: CSB-first follow-up
returned_scan_artifact_read_only: docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md
run_caps:
  max_screening_moves_total: 18
  max_exact_queries_total: 6
  max_promoted_observations: 4
  max_hidden_venue_pointers_new: 2
  max_capture_requests_new: 1
screening_moves_used: 15
exact_queries_used: 6
promoted_observations: 4
hidden_venue_pointers_new: 0
capture_requests_new: 0
capture_requests_carried_forward: 2
closeout_state: no_candidate_after_discovery
```

Non-goals preserved: no crawler, monitor, registry, atlas, standing source map,
scraping, login, private or auth-gated access, LinkedIn live read,
TikTok/Instagram live read, person dossier, packet-grade capture, route binding,
ECR, Cleaning, Judgment, gate clearance, demand proof, buyer proof, source-class
ratification, outreach, buyer contact, or client-facing output.

## Discovery Objective

The returned CSB-first scan is treated as a routing artifact, not a candidate
artifact. This pass tests only the unresolved question: whether a public venue
can expose independent demand-origin evidence or a new hidden venue that the
CSB scan did not surface.

Promotion floor applied from scan core:

- retail presence, owned availability, editorial visibility, partner-channel
  motion, and review counts are venue value or G4/org-motion corroboration;
  they do not count as independent demand-origin evidence;
- qualifying demand-origin support needs public buyer-origin material from a
  sourced demand family, with distinct origination and at least one gradeable
  costly-behavior floor;
- precursor language is limited to route choice. Ordinary weak owned/channel
  or editorial evidence is recorded as venue value, pointer, negative, access
  note, or unknown.

## Source Loading Ledger

| Source | Why read | Claim supported |
| --- | --- | --- |
| `AGENTS.md` from current task context | Project behavior and validation gates. | Docs-write allowed; completion needs verification. |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint. | Orca overlay is project authority. |
| `.agents/workflow-overlay/decision-routing.md` | Non-trivial cross-lane routing. | Regime is complicated; allowed next move is a bounded scan artifact. |
| `.agents/workflow-overlay/source-loading.md` | Start-preflight and source-pack contract. | Custom source pack and read ledger. |
| `.agents/workflow-overlay/artifact-folders.md` and `artifact-roles.md` | Placement and artifact role. | `docs/research/` is accepted for research artifacts. |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval header contract. | This durable artifact carries a retrieval-only header. |
| `.agents/workflow-overlay/validation-gates.md` | Closeout checks. | Required hygiene checks are listed and run below. |
| `docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md` | CSB starting board. | Rows SBR-001 through SBR-010 govern source-family questions. |
| `docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md` | Returned scan to follow up without editing. | CR-001/CR-002, venue ledgers, and no-candidate baseline. |
| `orca/product/spines/scanning/README.md` | Scanning front door. | CSB-first load order, exact-query discovery, shared vocabulary. |
| `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md` | MGT walk contract. | Frontier selection, exact-query, branch decay, capture_request boundary. |
| `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md` | Promotion rules. | Retail excluded from demand-origin count; candidate gate mechanics. |
| `orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md` | Walker Equipment Kit targeted section. | Public-only screening, no logins, access-note treatment. |

## Public Source Ledger

| Source | Retrieval date | What changed the route | Demand-origin status |
| --- | --- | --- | --- |
| `https://imaginaryauthors.com/products/a-little-secret` | 2026-06-22 | Official PDP showed 50ml Add to Bag, 14ml/2ml sold out, restock notification UI, and product notes. | Owned chronology and volatility only. Not independent demand-origin evidence. |
| `https://imaginaryauthors.com/products/dipped-in-chocolate` | 2026-06-22 | Official PDP showed 50ml Add to Bag and Salt & Straw partnership copy. | Owned contradiction/current-state surface only. Not demand proof. |
| `https://ministryofscent.com/collections/imaginary-authors` | 2026-06-22 | Specialist retailer page showed 28 Imaginary Authors products; A Little Secret had no reviews; First Peach had one review count; Dipped in Chocolate did not appear in the read section. | Retail venue value and review-count route. Review text not reached. |
| `https://www.luckyscent.com/brands/imaginary-authors` | 2026-06-22 | Specialist retailer brand page listed A Little Secret and First Peach of the Season in current assortment; Dipped in Chocolate was not found on the opened brand page. | Retail venue value. No buyer-origin text reached. |
| `https://www.allure.com/story/peach-perfumes-trend-summer-2026` | 2026-06-22 | 2026-06-19 editorial article named First Peach of the Season in a peach-fragrance trend list and linked to Imaginary Authors. | Editorial/category visibility only. Not buyer-origin. |
| `https://www.anthropologie.com/en-gb/shop/imaginary-authors-x-anthropologie-discovery-set` | 2026-06-22 | Partner PDP showed 2 reviews, GBP 48, low-stock language, and Add to Basket for the Anthropologie candle discovery set. | Reverified prior hidden partner venue; adjacent candle/org-motion route only. |
| `https://www.livingetc.com/shopping/imaginary-authors-anthropologie-candles` | 2026-06-22 | 2026-01-23 editorial article routed to the Imaginary Authors x Anthropologie candle discovery set and individual candle SKUs. | Partner-channel pointer, not independent demand. |
| `https://www.foodandwine.com/news/edible-perfume-ice-cream-salt-straw` | 2026-06-22 | 2022 article confirmed older Salt & Straw / Imaginary Authors perfume collaboration history. | Historical partner context. Not current Dipped in Chocolate proof. |

## Exact Query Discovery Ledger

| Query ID | Query text | Intent | Result class | Next-route decision |
| --- | --- | --- | --- | --- |
| EQD-001 | `Imaginary Authors A Little Secret perfume review Fragrantica Parfumo Basenotes Reddit` | Find independent public buyer-language venue for A Little Secret. | negative / access-limited | No better public buyer-origin venue surfaced through the search route. Keep as buyer-language gap. |
| EQD-002 | `Imaginary Authors Dipped in Chocolate perfume review Fragrantica Parfumo Basenotes Reddit` | Find independent public buyer-language venue for Dipped in Chocolate. | negative / access-limited | No demand-origin venue surfaced; owned PDP remains volatile state only. |
| EQD-003 | `Imaginary Authors First Peach of the Season fragrance review Reddit Basenotes Parfumo` | Find review/community support for First Peach. | negative / route-thin | Allure/retailer visibility remains route value only. |
| EQD-004 | `site:anthropologie.com/shop Imaginary Authors Discovery Set -en-gb` | Test whether the Anthropologie pointer has a US public counterpart. | negative | No US counterpart surfaced through exact query or direct no-region URL attempt. Keep UK page as partner/org-motion only. |
| EQD-005 | `Dipped in Chocolate Salt & Straw Imaginary Authors` | Find original or current partner source for Dipped in Chocolate. | negative | No current original Salt & Straw route surfaced. Official IA PDP remains the source for the Dipped partnership copy. |
| EQD-006 | `A Whiff of Waffle Cone Salt & Straw Imaginary Authors` | Check older partner provenance route. | historical route | Food & Wine and related editorial routes confirm older collaboration history, not current buyer demand. |

## Venue Evaluation Move Log

| Move | CSB row(s) | Frontier | Value class | What happened | Stop check |
| --- | --- | --- | --- | --- | --- |
| M01 | SBR-001 | Official A Little Secret PDP | venue_value / contradiction candidate rejected | Current owned state reverified: 50ml available, smaller sizes sold out, restock notification visible. | a:no b:no c:no |
| M02 | SBR-001, SBR-010 | Official Dipped in Chocolate PDP | venue_value / contradiction | Current owned state reverified: 50ml available and Salt & Straw copy visible. This preserves volatility, not a restock claim. | a:no b:no c:no |
| M03 | SBR-003, SBR-007 | Official First Peach route search | access_note | Allure linked First Peach to Imaginary Authors, but exact official PDP route did not surface through public search/direct route attempts. | a:no b:no c:no |
| M04 | SBR-002, SBR-006 | Ministry of Scent collection | venue_value | Specialist collection showed product breadth, sample/full-bottle price bands, A Little Secret no-review count, and First Peach one-review count. | a:no b:no c:no |
| M05 | SBR-002, SBR-006 | Luckyscent brand page | venue_value | Brand page showed A Little Secret and First Peach in current assortment. Product-level review text was not reached. | a:no b:no c:no |
| M06 | SBR-006 | Retail product-review deepening | access_note | Product-detail click/search attempts did not expose dated buyer review text for the three target SKUs. Counts only are insufficient. | a:no b:no c:no |
| M07 | SBR-006 | Official review widget / embedded review route | access_note | Official PDP review area was present but did not expose readable dated buyer review text in this public read. | a:no b:no c:no |
| M08 | SBR-003, SBR-007 | Allure peach-fragrance article | venue_value / pointer | Article supplied current editorial visibility and a First Peach route. It did not supply buyer-origin behavior. | a:no b:no c:no |
| M09 | SBR-004, SBR-010 | Anthropologie UK partner PDP | venue_value / prior HVP reverified | Partner PDP state reverified; no new hidden venue was discovered. UK and candle-category limits carry. | a:no b:no c:no |
| M10 | SBR-007, SBR-010 | Anthropologie US counterpart search | negative | Exact search and direct no-region route did not surface a US counterpart. | a:no b:no c:no |
| M11 | SBR-004, SBR-010 | Livingetc collaboration article | pointer | Article routed to the Anthropologie set and individual candles. Editorial remains channel context. | a:no b:no c:no |
| M12 | SBR-010 | Salt & Straw partner route search | negative / historical pointer | No current Salt & Straw source for Dipped in Chocolate surfaced; Food & Wine confirmed older edible-perfume collaboration history. | a:no b:no c:no |
| M13 | SBR-005, SBR-006, SBR-007 | A Little Secret buyer-origin exact query | negative | No public product-specific review/community venue surfaced. | a:no b:branch-close c:no |
| M14 | SBR-005, SBR-006, SBR-007 | Dipped in Chocolate buyer-origin exact query | negative | No public product-specific review/community venue surfaced. | a:no b:branch-close c:no |
| M15 | SBR-005, SBR-006, SBR-007 | First Peach buyer-origin exact query | negative | No public product-specific review/community venue surfaced. | a:no b:branch-close c:no |

Stop reason: after 15 moves, the remaining path had decayed to
orchestrator-mediated Reddit/Basenotes-style screening, Capture-owned
preservation, or repeated search over dry exact queries. Continuing would
mostly restate absence from wall-prone venues and inflate false confidence.

## Capture Triage

The returned scan's capture requests remain useful only as preservation
requests:

```yaml
capture_request_id: CR-001
source_scan: scanning_mgt_imaginary_authors_core_satellite_csb_v0
triage_result: carry_forward_preservation_only
urls:
  - https://imaginaryauthors.com/products/a-little-secret
  - https://imaginaryauthors.com/products/dipped-in-chocolate
why: >
  Official PDP state is volatile and could matter if a later lane wants
  packet-grade provenance for current availability, variant sellout, restock
  notification UI, or partnership copy.
not_proven:
  - demand proof
  - restock proof
  - gate clearance
route_binding_state: unknown
```

```yaml
capture_request_id: CR-002
source_scan: scanning_mgt_imaginary_authors_core_satellite_csb_v0
triage_result: carry_forward_preservation_only
urls:
  - https://www.anthropologie.com/en-gb/shop/imaginary-authors-x-anthropologie-discovery-set
why: >
  Direct partner PDP state is volatile enough to preserve if partner-channel
  evidence matters, especially the review count, low-stock language, price, and
  UK-only/candle-category limits.
not_proven:
  - US fragrance demand
  - buyer-origin proof
  - route binding
route_binding_state: unknown
```

No new capture_request is emitted. The scan does not route Capture, set a route,
or ask for ECR, Cleaning, Judgment, or packet commitment.

## Observations

```yaml
observation_id: OBS-DISC-001
source_move_id: M01, M02
url:
  - https://imaginaryauthors.com/products/a-little-secret
  - https://imaginaryauthors.com/products/dipped-in-chocolate
retrieval_date: 2026-06-22
short_quote_or_summary: >
  Official PDPs show current owned availability states for A Little Secret and
  Dipped in Chocolate; Dipped also carries Salt & Straw partnership copy.
signal_stage: contradiction
claim_it_might_support: >
  Volatile owned current-state preservation for SKU availability, variant state,
  and partner copy.
gate_role: decision_event
independence_hypothesis: >
  Owned official source only. Not independent demand-origin evidence.
uncertainty_or_limits: >
  Requires Capture only if packet-grade preservation matters; no buyer behavior
  surfaced from these owned pages.
```

```yaml
observation_id: OBS-DISC-002
source_move_id: M04, M05, M06
url:
  - https://ministryofscent.com/collections/imaginary-authors
  - https://www.luckyscent.com/brands/imaginary-authors
retrieval_date: 2026-06-22
short_quote_or_summary: >
  Specialist retailers continue to show Imaginary Authors assortment, including
  A Little Secret and First Peach, but product-level dated review text was not
  reached.
signal_stage: venue_value
claim_it_might_support: >
  Specialist retail channel corroboration and routing value.
gate_role: org_motion
independence_hypothesis: >
  Retail presence is G4/org-motion corroboration under scan-core semantics and
  is excluded from the demand-origin count.
uncertainty_or_limits: >
  Review counts alone are not gradeable buyer-origin evidence.
```

```yaml
observation_id: OBS-DISC-003
source_move_id: M03, M08, M15
url:
  - https://www.allure.com/story/peach-perfumes-trend-summer-2026
retrieval_date: 2026-06-22
short_quote_or_summary: >
  Allure's 2026-06-19 peach-fragrance article names First Peach of the Season
  and routes readers to Imaginary Authors.
signal_stage: venue_value
claim_it_might_support: >
  Editorial visibility and route value for a fresh peach-fragrance context.
gate_role: influence
independence_hypothesis: >
  Editorial trend inclusion is downstream visibility, not buyer-origin demand.
uncertainty_or_limits: >
  The official First Peach PDP was not reached, and no public buyer-origin
  discussion surfaced inside the exact-query cap.
```

```yaml
observation_id: OBS-DISC-004
source_move_id: M09, M10, M11
url:
  - https://www.anthropologie.com/en-gb/shop/imaginary-authors-x-anthropologie-discovery-set
  - https://www.livingetc.com/shopping/imaginary-authors-anthropologie-candles
retrieval_date: 2026-06-22
short_quote_or_summary: >
  Anthropologie UK partner PDP and Livingetc article reverify the candle
  collaboration route; no US counterpart surfaced in this bounded follow-up.
signal_stage: venue_value
claim_it_might_support: >
  Partner-channel/org-motion evidence adjacent to fragrance.
gate_role: org_motion
independence_hypothesis: >
  Partner PDP and editorial article are channel surfaces; they do not establish
  US fragrance buyer demand.
uncertainty_or_limits: >
  UK surface, candle category, and lack of public buyer-origin text cap this at
  preservation/venue value.
```

## Negatives And Access Notes

- `NEG-DISC-001`: Exact buyer-origin searches for A Little Secret, Dipped in
  Chocolate, and First Peach of the Season did not surface a public,
  product-specific community/review venue inside this run.
- `ACCESS-DISC-001`: Reddit/Basenotes-style real community reads remain
  orchestrator-mediated under the Walker Equipment Kit. This session did not
  expose a `screening_read` route, so the scan records the need rather than
  crossing into direct scraping, auth-gated access, or ad hoc capture.
- `NEG-DISC-002`: Ministry of Scent, Luckyscent, official PDPs, and the
  Anthropologie PDP exposed review counts or review containers, not readable
  dated buyer-language sufficient for demand-origin use.
- `NEG-DISC-003`: No public US Anthropologie counterpart for the Imaginary
  Authors x Anthropologie Discovery Set surfaced through the exact query or
  direct no-region route attempt.
- `NEG-DISC-004`: No current original Salt & Straw source for Dipped in
  Chocolate surfaced through the exact-query route; the useful Salt & Straw
  context reached here is older collaboration history.
- `NEG-DISC-005`: No new hidden venue was found beyond the returned scan's
  Anthropologie UK pointer.

## Candidate Decision

No candidate minted.

```yaml
candidate_decision:
  closeout_state: no_candidate_after_discovery
  independent_origins_seen: []
  costly_behavior_floor: not_cleared
  retail_corroboration: present_g4
  org_motion_route: available_cited
  capture_preservation_option: available_for_CR_001_and_CR_002
  reason: >
    The fresh pass reverified owned volatility, specialist-retailer channel
    value, editorial visibility, and partner-channel context. It did not find
    public buyer-origin text, distinct independent demand origins, or gradeable
    costly behavior. Retail review counts and partner low-stock language are
    not enough to clear the candidate promotion floor.
```

The strongest remaining next action is optional Capture-owned preservation of
CR-001 and CR-002 if those source states matter. It is not a scanning candidate,
slot qualification, gate pass, route binding, or demand proof.

## Closeout

`no_candidate_after_discovery`.

Next lane may:

- route CR-001 or CR-002 to Capture if source-state preservation is worth the
  duplicate acquisition effort;
- commission orchestrator-mediated public community screening if the owner
  wants to test Reddit/Basenotes-style buyer-language surfaces;
- discard or re-verify this artifact after 2026-07-13 before any forward use.

Next lane must not:

- treat this artifact as validation, readiness, buyer proof, gate clearance,
  candidate admission, source-class ratification, or a client-facing output;
- treat owned availability, retailer assortment, review counts, editorial
  visibility, partner-channel context, or low-stock language as demand-origin
  proof;
- use prior Imaginary Authors scans as fresh evidence without re-verification;
- infer route binding, capture permission, packet commitment, ECR, Cleaning,
  Judgment, outreach, buyer contact, live social access, or standing monitoring
  from this artifact.
