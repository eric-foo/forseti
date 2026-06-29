# Orca Commission Signal Board - Imaginary Authors Forward v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact (Commission Signal Board output; forward collection board)
scope: >
  Durable CSB board for Imaginary Authors as a forward US indie/DTC fragrance
  subject. Uses the existing Imaginary Authors scanning artifact as supplied
  source-backed context and produces a source-family / venue route map for
  scanning-owned venue-value evaluation. It does not retrieve new sources,
  classify demand, build a graph, authorize capture, or prove buyer demand.
use_when:
  - Testing the Commission Signal Board lane before scanning evaluates venues.
  - Starting a scanning run from CSB source-family rows instead of a loose seed.
  - Comparing CSB-nominated venues against hidden venues discovered by scanning.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_structure_v0.md
  - orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - docs/research/orca_discovery_candidate_scan_imaginary_authors_mgt_v0.md
  - orca/product/spines/scanning/README.md
stale_if:
  - The Commission Signal Board output contract or validator changes.
  - The Imaginary Authors scan artifact is superseded, rejected, or re-run.
  - Any row is used after the scan artifact's 21-day forward freshness window without re-verification.
```

### 1. Commission Intake Receipt

```yaml
commission_id: csb_imaginary_authors_forward_v0
mode: forward
candidate_or_subject: Imaginary Authors
decision_context: >
  Route source families and venues for checking current or imminent public
  allocation, assortment, SKU, launch, restock, channel, or discontinuation
  decisions in US indie/DTC fragrance.
market_or_geography: US indie/DTC fragrance
time_window: current as of 2026-06-21; forward freshness window through 2026-07-12
evidence_cutoff_at: not_applicable
input_status: complete
missing_required_inputs: []
cutoff_rule: not_applicable_forward_mode
non_goals_preserved:
  - no retrieval beyond supplied scan context
  - no demand classification
  - no graph construction
  - no capture authorization
  - no buyer-proof or readiness claim
```

### 2. Boundary Statement

This is an evidence/signals-only Commission Signal Board. It organizes source
families, venues, observables, gaps, counterevidence paths, and graph-light
retrieval hints; it is not a demand verdict, proof claim, graph artifact,
forecast, judgment, capture packet, or client output.

### 3. Source-Family Coverage Plan

| Source family | Subfamily / surface | Capture posture | Why check it | Expected observable | Evidence status | Surface cutoff status | Cutoff status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| owned_channels | Imaginary Authors collection and PDP surfaces | available_now | Establish official chronology, SKU availability, new labels, sold-out/restock state. | Current product state, variant availability, partnership language. | source_backed | not_applicable | not_applicable | Source-backed through scan artifact; re-fetch before downstream use. |
| retail_pdp | Ministry of Scent Imaginary Authors collection | available_now | Check retailer/channel corroboration and route into reviews. | Retail listing, sample availability, review count or review text. | source_backed | not_applicable | not_applicable | Retail is channel corroboration, not demand-origin by itself. |
| news_editorial_trade | Allure peach-fragrance trend article | available_now | Check category/trend visibility and cited-source routes. | Editorial inclusion, product naming, category frame. | source_backed | not_applicable | not_applicable | Visibility row, not demand proof. |
| news_editorial_trade | Livingetc Anthropologie candle collaboration article | available_now | Check adjacent home-fragrance/channel expansion signal. | Collab chronology, product format, retailer context. | source_backed | not_applicable | not_applicable | Adjacent to fragrance; keep out of classifier handoff unless subject broadens. |
| forums_community | Reddit, Basenotes, Fragrantica forums, specialist boards | manual_only | Look for independent buyer language, objections, repeat questions, or rejection. | Dated public discussions and product-specific language. | to_retrieve | not_applicable | not_applicable | Wall-prone; scanning should record venue value/access notes, not scrape. |
| reviews | Retailer, brand-site, and specialist fragrance reviews | available_now | Look for experience claims and review recency. | Review text, review date, rating context, repeat-use hints. | to_retrieve | not_applicable | not_applicable | Do not collapse to stars; preserve source conventions. |
| search_discovery | Exact-query discovery | available_now | Find hidden venues, better origin surfaces, and negatives. | Exact public queries, query language, absent/present product-specific surfaces. | to_retrieve | not_applicable | not_applicable | Scanning owns bounded exact-query discovery; not proof, search-volume, or monitoring. |
| aeo_answer_engines | ChatGPT / Google AIO seed-query family | manual_only | Preserve why Imaginary Authors entered the workstream and what cited-source ecosystem appears. | Answer visibility, cited sources, entity association. | source_backed | not_applicable | not_applicable | Visibility annotation only; excluded from classifier handoff. |
| creator_social_video | YouTube, TikTok, Instagram creator surfaces | planned_lane | Check attention spread only if separately routed. | Creator clusters, affiliate/campaign overlap, repeated language. | not_authorized | not_applicable | not_applicable | No live TikTok/Instagram access in this board. |
| professional_org_motion | Partnerships, retailer collaborations, careers/ATS if relevant | available_now | Check org motion around Salt & Straw / Anthropologie or future channel moves. | Partner claim, retailer collaboration, role movement. | to_retrieve | not_applicable | not_applicable | Prefer original partnership/official surfaces over LinkedIn live access. |

### 4. Signal Board Rows

| Row ID | Source family | Subfamily | Surface | Observable | Signal role | Row purpose | Graph role | Graph weight hint | Evidence status | Provenance needed | Surface cutoff status | Cutoff status | Handoff note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SBR-001 | owned_channels | brand site PDPs | Imaginary Authors collections and PDPs | New labels, current SKU availability, sold-out/restock UI, partnership copy | owned_claim | chronology | seed | medium | source_backed | URL, retrieval date, exact product/variant state | not_applicable | not_applicable | Eligible as chronology/source-route row; not demand proof. |
| SBR-002 | retail_pdp | retailer collection | Ministry of Scent Imaginary Authors collection | Retail listing, sample availability, review count, assortment context | retail_corroboration | source_route | node_candidate | medium | source_backed | URL, retrieval date, listing/review state | not_applicable | not_applicable | Eligible as channel corroboration/source-route row; retail is not demand-origin by itself. |
| SBR-003 | news_editorial_trade | editorial trend article | Allure peach-fragrance article | Fresh editorial category visibility for an Imaginary Authors peach fragrance | none | source_route | propagation_path | low | source_backed | URL, publication date, product naming | not_applicable | not_applicable | Eligible as visibility/source-route row; classifier owns whether it matters. |
| SBR-004 | news_editorial_trade | editorial channel article | Livingetc Anthropologie candle-collab article | Adjacent home-fragrance/candle collaboration context | org_motion | source_route | edge_candidate | low | source_backed | URL, publication date, collaboration details | not_applicable | not_applicable | Keep adjacent unless subject broadens beyond fragrance. |
| SBR-005 | forums_community | specialist forums | Reddit, Basenotes, Fragrantica, specialist boards | Product-specific buyer language, objections, repeat questions, rejection | consumer_language | signal_unit | node_candidate | high | to_retrieve | Public URL, thread date, access boundary | not_applicable | not_applicable | Scanning should evaluate venue value and access wall before Capture. |
| SBR-006 | reviews | retailer and specialist reviews | Ministry of Scent reviews, brand reviews, fragrance review sites | Dated experience claims and review recency | review_experience | signal_unit | node_candidate | medium | to_retrieve | Review URL, review date, source convention | not_applicable | not_applicable | Needs review-content retrieval; aggregate count is insufficient. |
| SBR-007 | search_discovery | exact-query discovery | Product and discontinued-term query set | Hidden venues, better origin surfaces, decisive absence | search_interest | source_route | counterevidence_path | medium | to_retrieve | Exact query string, retrieval date, result route, no-yield note | not_applicable | not_applicable | Exact-query discovery row for scanning; not proof, search-volume, or monitoring. |
| SBR-008 | aeo_answer_engines | seed query | Top indie perfume brands answer-engine family | Answer visibility and cited-source ecosystem that surfaced Imaginary Authors | aeo_visibility | source_route | propagation_path | low | source_backed | Query text, answer date/source, cited sources | not_applicable | not_applicable | Excluded from classifier handoff; visibility annotation only. |
| SBR-009 | creator_social_video | creator surfaces | YouTube, TikTok, Instagram | Creator attention, repeated language, affiliate/campaign overlap | creator_attention | gap | campaign_overlap_check | medium | not_authorized | Separate route authorization and platform boundary | not_applicable | not_applicable | Planned/deferred; do not run live here. |
| SBR-010 | professional_org_motion | partnerships and org surfaces | Salt & Straw, Anthropologie, careers/ATS if relevant | Partnership chronology, retailer collab, org movement | org_motion | source_route | edge_candidate | medium | to_retrieve | Original partner/official URL and date | not_applicable | not_applicable | Prefer original surfaces; LinkedIn live access not authorized. |

### 5. Mandatory Counterevidence Paths

| Path ID | What could disconfirm or weaken the signal | Source families to check | Why it matters | Evidence status | Cutoff rule |
| --- | --- | --- | --- | --- | --- |
| CEP-001 | Owned-site availability without buyer uptake. | forums_community; reviews; search_discovery | Prevents owned chronology from becoming false demand evidence. | to_retrieve | not_applicable_forward |
| CEP-002 | Retail listing exists but reviews are stale, sparse, syndicated, or negative. | retail_pdp; reviews | Retail presence is channel corroboration only and may not reflect demand. | to_retrieve | not_applicable_forward |
| CEP-003 | Editorial/creator visibility is campaign-driven or laundered from press copy. | news_editorial_trade; creator_social_video; search_discovery | Avoids double-counting PR/affiliate propagation as organic demand. | to_retrieve | not_applicable_forward |
| CEP-004 | Search/AEO visibility does not lead to independent origin surfaces. | search_discovery; aeo_answer_engines | Keeps answer visibility out of demand-origin claims. | source_backed_gap | not_applicable_forward |
| CEP-005 | Community venues are access-walled, inactive, or too noisy for repeatable public reads. | forums_community | Determines venue value and whether Capture/source-access is needed. | to_retrieve | not_applicable_forward |

### 6. Campaign And Duplication Risk

| Risk ID | Possible duplication/campaign pattern | Surfaces implicated | Required check | Evidence status | Handoff note |
| --- | --- | --- | --- | --- | --- |
| DUP-001 | Brand PDP, retailer listing, and editorial copy repeat launch/availability claims from the same source. | owned_channels; retail_pdp; news_editorial_trade | Compare wording, dates, and cited origin before treating surfaces as independent. | to_retrieve | Scanning should record duplication risk, not score it. |
| DUP-002 | Peach-fragrance trend visibility may reflect editorial trend packaging rather than product-specific demand. | news_editorial_trade; search_discovery; reviews | Look for buyer-origin review/community language tied to the exact SKU. | to_retrieve | Keep Allure as route/visibility unless independent origin appears. |
| DUP-003 | Creator/social attention could be affiliate or campaign clustered. | creator_social_video | Requires separate authorized creator-surface read and duplication check. | not_authorized | Do not run live creator access in this board. |
| DUP-004 | AEO answer visibility may loop through the same cited editorial/category sources. | aeo_answer_engines; search_discovery; news_editorial_trade | Check cited-source overlap before graph use. | source_backed_gap | AEO excluded from classifier handoff. |

### 7. Graph Retrieval Brief

```yaml
graph_retrieval_brief:
  seed_entities:
    - Imaginary Authors
    - A Little Secret
    - Dipped in Chocolate
    - First Peach of the Season
  adjacent_entities_to_check:
    - Salt & Straw
    - Anthropologie
    - Ministry of Scent
    - Allure peach-fragrance trend article
    - Livingetc Anthropologie candle article
  creator_slices:
    - fragrance reviewers mentioning exact SKU names
    - peach-fragrance trend creators
    - collaboration/limited-SKU coverage if separately authorized
  source_families:
    - owned_channels
    - retail_pdp
    - reviews
    - forums_community
    - search_discovery
    - news_editorial_trade
    - aeo_answer_engines
    - creator_social_video
    - professional_org_motion
  mandatory_counterevidence_paths:
    - owned chronology without buyer uptake
    - retail listing without review/experience support
    - editorial visibility without independent origin
    - AEO/search visibility loop
    - community/access wall or no-yield venue
  node_types_to_retrieve:
    - brand
    - product
    - retailer
    - editorial article
    - review surface
    - community venue
    - partner entity
  edge_types_to_retrieve:
    - brand_to_product
    - product_to_retailer
    - product_to_editorial_mention
    - product_to_review_surface
    - product_to_community_thread
    - brand_to_partner
  campaign_overlap_checks:
    - repeated launch phrasing
    - affiliate/creator clustering
    - cited-source overlap in search/AEO surfaces
    - retailer/brand syndicated copy
  graph_weight_notes: relation utility only; graph weight is not signal strength.
  surface_cutoff_notes: forward mode; surface cutoff not applicable, but all rows expire with the scan freshness window unless re-verified.
  forecast_targets_supported_without_probabilities:
    - review velocity
    - restock or stockout persistence
    - retailer assortment changes
    - editorial/creator decay
    - hidden venue yield
  backtest_cutoff_date: null
  future_info_exclusion_rule: not_applicable_forward_mode
```

### 8. Demand-Classifier Handoff Packet

```yaml
classifier_handoff_packet:
  candidate_or_subject: Imaginary Authors
  decision_context: >
    Current or imminent public allocation, assortment, SKU, launch, restock,
    channel, or discontinuation decisions in US indie/DTC fragrance.
  mode: forward
  cutoff_date: null
  signal_rows_for_handoff:
    - SBR-001
    - SBR-002
    - SBR-003
  counterevidence_rows_for_handoff: []
  source_family_gaps:
    - SBR-005 forums/community buyer-language venues need venue-value evaluation.
    - SBR-006 review-content rows need retrieval beyond listing/review count.
    - SBR-007 exact-query discovery rows should look for hidden venues and decisive negatives.
    - SBR-009 creator/social surfaces are not authorized for live access in this run.
    - SBR-010 partner/org-motion rows need original source retrieval.
  provenance_gaps:
    - exact review text and review dates
    - public community URL/date/access boundary
    - original partner or official collaboration source
    - duplicate/campaign overlap check
  cutoff_uncertainties: []
  classifier_mapping_status: classifier_owned
  prohibited_claims:
    - no demand verdict
    - no buyer-proof claim
    - no validation or readiness claim
    - no graph score
    - no forecast probability
```

### 9. Visible Limitations

- This board did not perform new retrieval; it uses the existing scan artifact
  as supplied source-backed context.
- Source-backed rows must be re-fetched before any downstream evidentiary use
  after the forward freshness window.
- Forums/community and reviews remain the largest demand-origin gaps.
- Search/AEO visibility is a route and propagation clue only.
- Creator/social surfaces are deferred without explicit authorization.
- Retail and editorial rows are not independent demand proof.
- Graph roles describe retrieval utility only, not signal strength.
- The board does not authorize Capture, route binding, ECR, Cleaning, Judgment,
  gate clearance, or client-facing use.

### 10. Board Status And Run Boundary

```yaml
board_status: READY_FOR_RETRIEVAL_HANDOFF
run_boundary: CHAT_ONLY_BOARD_COMPLETE
next_authorized_step: >
  Use this board as the upstream route map for a bounded scanning run that
  evaluates venue value, records hidden venues CSB missed, and emits
  capture_request only when the capture-request promotion bar is met.
```