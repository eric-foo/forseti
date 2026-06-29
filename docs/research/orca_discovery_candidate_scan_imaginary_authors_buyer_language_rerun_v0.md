# Orca Discovery Candidate Scan - Imaginary Authors Buyer-Language Rerun v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact (bounded scanning rerun)
scope: >
  Fresh bounded buyer-language rerun for the Imaginary Authors CSB-first scan.
  Exercises the missing non-orchestrator venue rungs for Parfumo, Basenotes,
  and Fragrantica across A Little Secret, Dipped in Chocolate, and First Peach
  of the Season. Records venue value, access notes, candidate-support
  observations, candidate decision, and capture_request without editing the
  prior scan artifact.
use_when:
  - Reviewing the buyer-language rerun after the CSB-first Imaginary Authors scan.
  - Deciding whether Parfumo/Basenotes/Fragrantica changed the no-candidate closeout.
  - Routing candidate-support observations to Capture or a later gate without treating scanning evidence as proof.
authority_boundary: retrieval_only
open_next:
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_demand_origin_discovery_v0.md
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md
  - docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md
  - orca/product/spines/scanning/README.md
  - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  - orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md
stale_if:
  - Any observation is used after 2026-07-13 without fresh re-verification.
  - Parfumo, Basenotes, Fragrantica, Imaginary Authors, Ministry of Scent, Luckyscent, or Allure changes the observed page state.
  - Capture verifies, rejects, or supersedes the capture_request below.
```

## Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S0 + scanning CSB/MGT target pack + buyer-language rerun sources
  edit_permission: docs-write
  target_scope: docs/research fresh scanning rerun artifact plus repo-map pointer
  dirty_state_checked: yes
  blocked_if_missing: source context, public-source reads, validation checks
```

```text
Smallest complete outcome: Fresh rerun artifact answering whether the missing buyer-language rungs change the prior no-candidate closeout.
Regime: Complicated.
Why: The route is source-backed and bounded, but candidate promotion depends on scan-core gate vocabulary and source-access boundaries.
Decomposition: Layer-based source read, then bounded public venue probes, then candidate-decision packaging.
Current bottleneck: Whether public buyer-language venues expose gradeable independent demand-origin support.
Riskiest assumption: A readable community review venue may count only if it maps to the sourced forums_community family rather than unsourced review_surfaces.
Stop or pivot condition: Stop when Parfumo/Basenotes/Fragrantica cheap rungs either produce candidate-support observations or decay to access/noisy-search notes.
Allowed next move: Public-only direct pages, native search, site-snippet checks, and Wayback CDX checks.
Disallowed next move: No crawler, monitor, registry, atlas, Capture runner, login, anti-bot solving, live Reddit read, outreach, ECR, Cleaning, Judgment, or candidate proof by implication.
```

```yaml
commission_id: scanning_mgt_imaginary_authors_buyer_language_rerun_v0
scan_date: 2026-06-22
mode: forward
subject: Imaginary Authors
market_or_geography: US indie/DTC fragrance
entry_route: CSB-first buyer-language rerun
source_context_status: SOURCE_CONTEXT_READY
public_source_status: PUBLIC_READS_READY_WITH_ACCESS_NOTES
run_caps:
  max_screening_moves_total: 36
  max_exact_queries_total: 9
  max_archive_checks_total: 9
  max_candidate_entries: 2
  max_capture_requests_new: 1
screening_moves_used: 30
exact_queries_used: 9
archive_checks_used: 9
venues_tested:
  - Parfumo
  - Basenotes
  - Fragrantica
promoted_observations: 3
candidate_entries: 2
hidden_venue_pointers_new: 1
capture_requests_new: 1
closeout_state: candidate_ready_for_next_lane
prior_artifact_non_edit_statement: >
  docs/research/orca_discovery_candidate_scan_imaginary_authors_demand_origin_discovery_v0.md
  and docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md
  were read only as prior-run context. They were not edited.
```

Non-goals preserved: no broad crawl, monitor, registry, atlas, standing source
map, scraping-at-scale, login, private/auth-gated access, Reddit live read,
Capture execution, route binding, ECR, Cleaning, Judgment, outreach, buyer
contact, buyer-proof claim, validation claim, readiness claim, or client-facing
output.

## Source Loading Ledger

| Source | Why read | Claim supported |
| --- | --- | --- |
| `AGENTS.md` from current task context | Project behavior and verification gates. | Docs-write allowed; completion needs fresh validation. |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint. | Orca overlay is project authority. |
| `.agents/workflow-overlay/decision-routing.md` | Non-trivial rerun and dirty-worktree routing. | Bounded rerun, not broad scan or Capture. |
| `.agents/workflow-overlay/source-loading.md` | Source pack and start-preflight contract. | Custom source pack and source ledger. |
| `.agents/workflow-overlay/artifact-folders.md` | Placement. | `docs/research/` is accepted for research artifacts. |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval header contract. | This durable artifact carries retrieval-only metadata. |
| `.agents/workflow-overlay/validation-gates.md` | Closeout validation expectations. | Hygiene checks listed and run below. |
| `docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md` | CSB board. | Rows SBR-005, SBR-006, and SBR-007 define buyer-language and exact-query gaps. |
| `docs/research/orca_discovery_candidate_scan_imaginary_authors_core_satellite_csb_v0.md` | Returned scan baseline. | Prior buyer-language branch was dry/access-limited. |
| `docs/research/orca_discovery_candidate_scan_imaginary_authors_demand_origin_discovery_v0.md` | Reviewed follow-up baseline. | Prior no-candidate closeout depended on no public buyer-origin venue found. |
| Current-thread adversarial review summary and local readback | Advisory rerun trigger only. | IA-CSB-AR-01 named the missing Parfumo/Basenotes/Fragrantica cheap rungs. |
| `orca/product/spines/scanning/README.md` | Scanning front door. | CSB-first load order, exact-query discovery, hidden venue, and precursor limits. |
| `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md` | MGT walk contract. | Run cap, exact-query, access-note, and capture_request boundaries. |
| `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md` | Promotion rules. | One independent gradeable origin can create a low-commitment candidate; material action needs stronger convergence. |
| `orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md` | Walker Equipment Kit. | Public-only URL/snippet/archive rungs before final access notes. |
| `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` | Targeted access-wall seam. | Anti-bot/public access is a route problem; scanning records the need and does not run Capture. |

The adversarial review finding is treated as current-thread advisory context; this artifact is self-contained on the rerun results and committed sources.

## Rerun Scope

Target SKUs:

| SKU | Why included |
| --- | --- |
| A Little Secret | Current owned launch/availability row and prior no-review venue gap. |
| Dipped in Chocolate | Prior official availability contradiction, Salt & Straw collab route, and limited/collab demand question. |
| First Peach of the Season | Fresh peach-fragrance editorial route and specialist-retailer listing gap. |

Target venues:

| Venue | Rerun role |
| --- | --- |
| Parfumo | Specialist fragrance community/review venue. Public pages reachable. |
| Basenotes | Specialist forum/community venue. Direct public search is Cloudflare-challenged in this environment. |
| Fragrantica | Specialist fragrance database/community venue. Static search page reachable but did not expose product results through direct HTML. |

## Public Source Ledger

| Source | Retrieval date | Result | Demand-origin status |
| --- | --- | --- | --- |
| `https://www.parfumo.com/s_perfumes.php?filter=A%20Little%20Secret%20Imaginary%20Authors` | 2026-06-22 | Public search page returned a direct product route for A Little Secret. | Valuable venue route. |
| `https://www.parfumo.com/s_perfumes.php?filter=Dipped%20in%20Chocolate%20Imaginary%20Authors` | 2026-06-22 | Public search page returned a direct product route for Dipped in Chocolate. | Valuable venue route. |
| `https://www.parfumo.com/s_perfumes.php?filter=First%20Peach%20of%20the%20Season%20Imaginary%20Authors` | 2026-06-22 | Public search page returned a direct product route for First Peach of the Season. | Valuable venue route. |
| `https://www.parfumo.com/Perfumes/Imaginary_Authors/a-little-secret` | 2026-06-22 | Product page exposed aggregate rating, 68 ratings, 7 reviews, 22 statements, review dates, and user text. | Buyer-language venue value; no promoted candidate from this SKU. |
| `https://www.parfumo.com/Perfumes/Imaginary_Authors/dipped-in-chocolate` | 2026-06-22 | Product page exposed aggregate rating, 36 ratings, 5 reviews, 12 statements, limited/discontinued page copy, dated reviews, and buyer-action language. | Candidate-support observation. |
| `https://www.parfumo.com/Perfumes/Imaginary_Authors/first-peach-of-the-season` | 2026-06-22 | Product page exposed aggregate rating, 41 ratings, 6 reviews, 17 statements, April-June 2026 reviews, and buyer-action language. | Candidate-support observation. |
| `https://basenotes.com/search/?q=<sku>%20Imaginary%20Authors` | 2026-06-22 | Direct public search returned Cloudflare challenge pages for all three SKU queries. | Access note, not a negative. |
| `https://www.fragrantica.com/search/?query=<sku>%20Imaginary%20Authors` | 2026-06-22 | Static HTML returned Fragrantica search shell but no product-result terms for the three SKU queries. | Access/search-surface note, not a negative. |
| Bing RSS exact site queries for Parfumo/Basenotes/Fragrantica x three SKUs | 2026-06-22 | RSS search returned generic dictionary/letter results rather than faithful site snippets. | Noisy search-surface note, not a negative. |
| Wayback CDX for Parfumo product pages | 2026-06-22 | A Little Secret returned one 2025 capture; Dipped in Chocolate returned 2024 and 2025 captures; First Peach returned no 200 capture in this check. | Archive rung exercised; current preservation still needed. |
| Wayback CDX for Basenotes and Fragrantica search URLs | 2026-06-22 | Basenotes search URLs returned empty CDX arrays; Fragrantica search CDX calls returned partial errors/empty outputs. | Archive rung did not produce product-specific evidence. |

## Exact Query Discovery Ledger

| Query ID | Query text | Intent | Result class | Next-route decision |
| --- | --- | --- | --- | --- |
| EQR-001 | `site:fragrantica.com/perfume/Imaginary-Authors "A Little Secret" "Imaginary Authors"` | Snippet-mine Fragrantica for A Little Secret. | noisy_search_surface | Bing RSS returned generic letter results; no Fragrantica product route credited. |
| EQR-002 | `site:fragrantica.com/perfume/Imaginary-Authors "Dipped in Chocolate" "Imaginary Authors"` | Snippet-mine Fragrantica for Dipped. | noisy_search_surface | Bing RSS returned dictionary-style results; no Fragrantica product route credited. |
| EQR-003 | `site:fragrantica.com/perfume/Imaginary-Authors "First Peach of the Season" "Imaginary Authors"` | Snippet-mine Fragrantica for First Peach. | noisy_search_surface | Bing RSS returned generic results; no Fragrantica product route credited. |
| EQR-004 | `site:basenotes.com "A Little Secret" "Imaginary Authors"` | Snippet-mine Basenotes for A Little Secret. | noisy_search_surface | Bing RSS was unfaithful; native Basenotes search remained Cloudflare-challenged. |
| EQR-005 | `site:basenotes.com "Dipped in Chocolate" "Imaginary Authors"` | Snippet-mine Basenotes for Dipped. | noisy_search_surface | Bing RSS was unfaithful; native Basenotes search remained Cloudflare-challenged. |
| EQR-006 | `site:basenotes.com "First Peach of the Season" "Imaginary Authors"` | Snippet-mine Basenotes for First Peach. | noisy_search_surface | Bing RSS was unfaithful; native Basenotes search remained Cloudflare-challenged. |
| EQR-007 | `site:parfumo.com/Perfumes/Imaginary_Authors "A Little Secret" "Imaginary Authors"` | Snippet-mine Parfumo for A Little Secret. | route_found_by_native_search | Native Parfumo search supplied the product route; product page read was higher value than noisy RSS. |
| EQR-008 | `site:parfumo.com/Perfumes/Imaginary_Authors "Dipped in Chocolate" "Imaginary Authors"` | Snippet-mine Parfumo for Dipped. | route_found_by_native_search | Native Parfumo search supplied the product route; product page read promoted candidate support. |
| EQR-009 | `site:parfumo.com/Perfumes/Imaginary_Authors "First Peach of the Season" "Imaginary Authors"` | Snippet-mine Parfumo for First Peach. | route_found_by_native_search | Native Parfumo search supplied the product route; product page read promoted candidate support. |

The exact-query search surface was degraded, so the rerun does not treat RSS
non-results as absence. The decisive positive came from Parfumo's native public
search and product pages.

## Venue Evaluation Move Log

| Move | CSB row(s) | Frontier | Value class | What happened | Stop check |
| --- | --- | --- | --- | --- | --- |
| M01-M03 | SBR-005, SBR-006, SBR-007 | Parfumo native search for the three SKUs | hidden_venue_pointer / valuable venue | Parfumo surfaced direct product pages for all three SKUs. | a:no b:no c:no |
| M04-M06 | SBR-005, SBR-006 | Parfumo product pages | candidate_support / venue_value | Product pages exposed dated user reviews, aggregate counts, and buyer-language text. | a:partial b:no c:no |
| M07-M09 | SBR-005, SBR-007 | Basenotes native search for the three SKUs | access_note | Direct search returned Cloudflare challenge shells. | a:no b:no c:no |
| M10-M12 | SBR-005, SBR-007 | Fragrantica native search for the three SKUs | access_note | Static search shell did not expose product results for the target terms. | a:no b:no c:no |
| M13-M21 | SBR-005, SBR-007 | Site-snippet exact queries across Parfumo/Basenotes/Fragrantica x three SKUs | noisy_search_surface | Bing RSS returned irrelevant generic results; not counted as absence. | a:no b:branch-close c:no |
| M22-M30 | SBR-005, SBR-006 | Wayback CDX checks for page/archive rung | archive_note | Parfumo A Little Secret and Dipped pages had 200 capture pointers; First Peach and the Basenotes/Fragrantica search URLs did not yield useful product captures. | a:no b:branch-close c:no |

## Hidden Venue Pointer

```yaml
hidden_venue_pointer_id: HVP-RERUN-001
venue: Parfumo
url:
  - https://www.parfumo.com/Perfumes/Imaginary_Authors/a-little-secret
  - https://www.parfumo.com/Perfumes/Imaginary_Authors/dipped-in-chocolate
  - https://www.parfumo.com/Perfumes/Imaginary_Authors/first-peach-of-the-season
retrieval_date: 2026-06-22
source_family: forums_community / specialist fragrance community review surface
why_hidden_or_underweighted: >
  The CSB row named Reddit, Basenotes, Fragrantica, and specialist boards but
  did not make Parfumo an explicit product-page venue. The prior discovery pass
  bundled Parfumo into exact-query strings without product-page retrieval.
value: >
  Parfumo publicly exposed direct product routes, review counts, statement
  counts, review dates, review IDs, user review pages, and buyer-language text
  for all three target SKUs.
not_a_claim_of:
  - demand proof
  - buyer proof
  - material-action eligibility
  - Capture route binding
```

## Observations

```yaml
observation_id: OBS-RERUN-001
mode: forward
brand: Imaginary Authors
product_or_sku: A Little Secret
trend_vector: sweet-gourmand / cherry-rum limited-new-fragrance discussion
read_type: transient
demand_state: transient
signal_layer: buy_side
venue: Parfumo product page
venue_class: subtle
venue_family: forums_community
gate_family: forums_community
gate_family_basis: >
  Parfumo is treated here as a public specialist community review surface, not
  as retail_presence and not as the unsourced review_surfaces family.
origination_ref:
  - parfumo_a_little_secret_review_661354
  - parfumo_a_little_secret_review_635512
derived_from: unknown
costly_behavior: gradeable
integrity_notes: >
  One review records sample use and rejection; another records sample ownership
  and reluctance to buy a full bottle. This is buyer-language venue value, but
  not enough positive direction to promote A Little Secret as a candidate here.
divergence_basis: mixed reviews cap promotion
event_dates:
  - 2026-04-01
  - 2026-02-25
retrieval_date: 2026-06-22
provenance:
  url: https://www.parfumo.com/Perfumes/Imaginary_Authors/a-little-secret
  page_state_summary: >
    Page showed 68 ratings, 7 reviews, 22 statements, a 2025 release marker,
    and multiple dated user reviews.
decision_relevance: >
  Establishes Parfumo as a valuable buyer-language venue for A Little Secret,
  but does not create a candidate entry because the observed buyer behavior is
  mixed/low-commitment and not clearly convergent.
us_flag: border
signal_stage: candidate_support
candidate_promotion: not_promoted
```

```yaml
observation_id: OBS-RERUN-002
mode: forward
brand: Imaginary Authors
product_or_sku: Dipped in Chocolate
trend_vector: limited Salt & Straw / gourmand collab SKU demand
read_type: transient
demand_state: transient
signal_layer: buy_side
venue: Parfumo product page
venue_class: subtle
venue_family: forums_community
gate_family: forums_community
gate_family_basis: >
  Public specialist community reviews provide user-origin buyer behavior. The
  observation is not retail_presence and does not rely on the unsourced
  review_surfaces family.
origination_ref:
  - parfumo_dipped_review_425431
  - parfumo_dipped_review_424849
derived_from: unknown
costly_behavior: gradeable
integrity_notes: >
  Load-bearing support is concentrated in one venue family, so it is
  candidate-support only and needs Capture/gate review before downstream use.
divergence_basis: >
  Reviews are generally positive on gourmand execution but include redundancy
  caveats against A Whiff of Waffle Cone.
event_dates:
  - 2024-12-09
  - 2024-12-08
retrieval_date: 2026-06-22
provenance:
  url: https://www.parfumo.com/Perfumes/Imaginary_Authors/dipped-in-chocolate
  page_state_summary: >
    Page showed 36 ratings, 5 reviews, 12 statements, limited/discontinued page
    copy, and dated reviews. One reviewer said they "purchased a full bottle
    immediately"; another sampled first and then "hit BIN on the full bottle".
decision_relevance: >
  Supports a next-lane candidate around Dipped in Chocolate as a limited/collab
  SKU with observed user purchase behavior, especially when paired with prior
  official-page volatility and Salt & Straw context.
us_flag: border
signal_stage: candidate_support
candidate_promotion: promoted_to_candidate_entry
```

```yaml
observation_id: OBS-RERUN-003
mode: forward
brand: Imaginary Authors
product_or_sku: First Peach of the Season
trend_vector: peach-fragrance seasonal launch / fresh editorial visibility
read_type: transient
demand_state: transient
signal_layer: buy_side
venue: Parfumo product page
venue_class: subtle
venue_family: forums_community
gate_family: forums_community
gate_family_basis: >
  Public specialist community reviews provide user-origin buyer behavior. The
  observation is not retail_presence and does not rely on the unsourced
  review_surfaces family.
origination_ref:
  - parfumo_first_peach_review_663946
  - parfumo_first_peach_review_688526
derived_from: unknown
costly_behavior: gradeable
integrity_notes: >
  Load-bearing support is concentrated in one venue family and includes mixed
  review direction, so it is candidate-support only and needs Capture/gate
  review before downstream use.
divergence_basis: >
  One review shows full-bottle purchase after a release email; another shows
  secondary-market sample acquisition and rejection for personal collection fit.
event_dates:
  - 2026-04-04
  - 2026-06-04
retrieval_date: 2026-06-22
provenance:
  url: https://www.parfumo.com/Perfumes/Imaginary_Authors/first-peach-of-the-season
  page_state_summary: >
    Page showed 41 ratings, 6 reviews, 17 statements, a 2026 release marker,
    and dated April-June 2026 user reviews. One reviewer said they "blindly
    scooped up a full bottle"; another "got my hands on a sample".
decision_relevance: >
  Supports a next-lane candidate around First Peach of the Season as a fresh
  peach-fragrance launch with public user-origin buyer behavior, paired with
  prior retailer/editorial visibility.
us_flag: border
signal_stage: candidate_support
candidate_promotion: promoted_to_candidate_entry
```

## Access Notes And Negatives

- `ACCESS-RERUN-001`: Basenotes native search returned Cloudflare challenge
  shells for all three SKU queries. Bing RSS exact site queries were unfaithful,
  and Wayback CDX checks of the search URLs returned empty arrays. This is not a
  product-specific negative.
- `ACCESS-RERUN-002`: Fragrantica direct search pages returned a static search
  shell but no product-result terms in direct HTML. Bing RSS exact site queries
  were unfaithful, and Fragrantica search-URL CDX checks produced partial
  errors/empty output. This is not a product-specific negative.
- `NEG-RERUN-001`: No additional readable public buyer-language venue beyond
  Parfumo surfaced inside the non-orchestrator rung cap. This is not a global
  absence proof for Basenotes, Fragrantica, Reddit, or other community venues.
- `ARCHIVE-RERUN-001`: Wayback CDX returned 200 capture pointers for Parfumo
  A Little Secret and Dipped in Chocolate, but not First Peach of the Season in
  this run. Current Parfumo preservation remains useful if these observations
  are carried forward.

## Candidate Entries

```yaml
candidate_id: CAND-RERUN-001
mode: forward
brand: Imaginary Authors
vertical_subniche: US indie/DTC fragrance
decision_context: >
  Dipped in Chocolate limited/collab SKU availability, continuation, or restock
  posture after prior official-page volatility and current public buyer-language
  support.
decision_family: launch_moratorium_reposition
demand_state: transient
venue_class: subtle
observations:
  - OBS-RERUN-002
gate_check:
  independent_origins_seen:
    - observation_id: OBS-RERUN-002
      origination_ref: parfumo_dipped_review_425431
      independence_basis: user-origin review event; no shared derivation observed inside scan
    - observation_id: OBS-RERUN-002
      origination_ref: parfumo_dipped_review_424849
      independence_basis: user-origin review event; no shared derivation observed inside scan
  costly_behavior_floor: cleared
  commitment_ceiling: hold_low_commitment
  divergence_result: caps_ceiling
  integrity_labels_applicable: yes
  org_motion_route: available_cited
  retail_corroboration: present_g4
decision_owner_pointer: unknown
flags:
  - CORR
freshness:
  retrieval_date: 2026-06-22
  stale_after: 2026-07-13
not_a_claim_of:
  - buyer proof
  - demand proof
  - material-action eligibility
  - Capture route binding
```

```yaml
candidate_id: CAND-RERUN-002
mode: forward
brand: Imaginary Authors
vertical_subniche: US indie/DTC fragrance
decision_context: >
  First Peach of the Season fresh peach-fragrance launch and channel visibility
  with public user-origin buyer-language support.
decision_family: launch_moratorium_reposition
demand_state: transient
venue_class: subtle
observations:
  - OBS-RERUN-003
gate_check:
  independent_origins_seen:
    - observation_id: OBS-RERUN-003
      origination_ref: parfumo_first_peach_review_663946
      independence_basis: user-origin review event; no shared derivation observed inside scan
    - observation_id: OBS-RERUN-003
      origination_ref: parfumo_first_peach_review_688526
      independence_basis: user-origin review event; no shared derivation observed inside scan
  costly_behavior_floor: cleared
  commitment_ceiling: hold_low_commitment
  divergence_result: caps_ceiling
  integrity_labels_applicable: yes
  org_motion_route: available_cited
  retail_corroboration: present_g4
decision_owner_pointer: unknown
flags:
  - CORR
freshness:
  retrieval_date: 2026-06-22
  stale_after: 2026-07-13
not_a_claim_of:
  - buyer proof
  - demand proof
  - material-action eligibility
  - Capture route binding
```

## Capture Request

```yaml
capture_request_id: CR-RERUN-001
source_scan: scanning_mgt_imaginary_authors_buyer_language_rerun_v0
candidate_or_observation_ids:
  - CAND-RERUN-001
  - CAND-RERUN-002
  - OBS-RERUN-002
  - OBS-RERUN-003
urls:
  - url: https://www.parfumo.com/Perfumes/Imaginary_Authors/dipped-in-chocolate
    venue: Parfumo
    observation_supported: Dipped in Chocolate buyer-language candidate-support observation
    gate_role: forums_community demand-origin / costly-behavior floor
  - url: https://www.parfumo.com/Perfumes/Imaginary_Authors/first-peach-of-the-season
    venue: Parfumo
    observation_supported: First Peach of the Season buyer-language candidate-support observation
    gate_role: forums_community demand-origin / costly-behavior floor
what_capture_should_verify: >
  Preserve the public Parfumo product pages and the cited visible review state:
  aggregate rating/review/statement counts, dated review IDs, author-visible
  public review pages, and the buyer-action language supporting OBS-RERUN-002
  and OBS-RERUN-003. Confirm whether individual review URLs preserve the same
  visible text and dates.
decision_window: 2026-06-22 through 2026-07-13
route_binding_state: unknown
screening_evidence_summary: >
  Scanning reached Parfumo public product pages directly and observed enough
  user-origin buyer behavior to promote two low-commitment candidate entries.
  First Peach did not return a Wayback CDX 200 capture in this run, increasing
  preservation value if the candidate is carried forward.
uncertainty_or_access_limits: >
  All load-bearing demand-origin support is concentrated in one public
  specialist community venue. Basenotes and Fragrantica remain access/noisy
  search notes, not negatives.
not_requested:
  - route expansion by scanning
  - anti-bot solving
  - packet commitment by scanning
  - ECR, Cleaning, or Judgment work
  - buyer contact or outreach
```

## Candidate Decision

```yaml
candidate_decision:
  closeout_state: candidate_ready_for_next_lane
  candidate_entries:
    - CAND-RERUN-001
    - CAND-RERUN-002
  independent_origins_seen:
    - parfumo_dipped_review_425431
    - parfumo_dipped_review_424849
    - parfumo_first_peach_review_663946
    - parfumo_first_peach_review_688526
  costly_behavior_floor: cleared
  commitment_ceiling: hold_low_commitment
  material_action_eligible: no
  retail_corroboration: present_g4
  org_motion_route: available_cited
  capture_preservation_option: CR-RERUN-001
  reason: >
    The rerun found Parfumo as a valuable public buyer-language venue and
    observed user-origin purchase/sample behavior for Dipped in Chocolate and
    First Peach of the Season. Under scan-core, that is enough to emit
    candidate entries for next-lane preservation/gate review, but not enough to
    claim buyer proof, demand proof, material-action eligibility, or durable
    demand. A Little Secret remains venue value only in this rerun.
```

Next lane may use this artifact to route Capture preservation or a later gate
review for the two candidate entries. It must not treat the scan as validation,
readiness, buyer proof, demand proof, material-action evidence, Capture route
binding, ECR, Cleaning, Judgment, outreach, buyer contact, or standing
monitoring.

## Validation Plan

Run after writing:

- `git diff --check`
- `python .agents/hooks/check_retrieval_header.py --changed`
- `python .agents/hooks/check_repo_map_freshness.py --changed`
- `python .agents/hooks/check_placement.py --check`
- `python .agents/hooks/check_map_links.py --strict`
- targeted stale-language search for crawler/monitor/registry/atlas claims,
  Capture route binding, demand-proof overclaims, and precursor leakage.
