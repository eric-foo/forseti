# Orca Specialist Fragrance Precursor Surface CSB Board v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Commission Signal Board output for specialist-fragrance precursor-surface qualification.
use_when:
  - Seeding the Scanning lane for specialist-fragrance precursor-surface broad-scout work.
  - Reconstructing the CSB boundary before any Capture or Data Lake expansion.
authority_boundary: retrieval_only
source_paths:
  - docs/prompts/wrappers/specialist_fragrance_precursor_surface_csb_commission_wrapper_v0.md
  - orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md
  - orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - orca/product/spines/scanning/README.md
  - orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md
  - orca/product/satellites/beauty/beauty_venue_card_set_v0.md
stale_if:
  - The CSB prompt output contract changes.
  - The Scanning CSB-first broad-scout rule changes.
  - Later Scanning returns source-backed observations that supersede these to_retrieve rows.
```

### 1. Commission Intake Receipt

```yaml
commission_id: specialist_fragrance_precursor_surface_csb_v0
mode: forward
candidate_or_subject: Specialist fragrance precursor surfaces for US indie and DTC fragrance demand.
decision_context: >
  Identify and structure the source-family rows needed to decide which
  specialist-fragrance surfaces should be sent to Scanning for precursor-demand
  qualification before Capture or Data Lake expansion.
market_or_geography: US-first fragrance within beauty and personal care.
time_window: Current forward source-qualification pass.
evidence_cutoff_at: not_applicable_forward_mode
input_status: complete
missing_required_inputs: []
cutoff_rule: forward mode; no historical cutoff applied; do not use this board as a backtest artifact.
non_goals_preserved:
  - no public web retrieval in this CSB run
  - no scraping, crawling, capture, monitoring, graph construction, scoring, demand classification, judgment, buyer proof, or readiness claim
  - no selection of final top specialist stores
  - no Capture or Data Lake authorization
```

### 2. Boundary Statement

This is an evidence/signals-only Commission Signal Board output for routing Scanning work. It is not a demand verdict, proof claim, graph artifact, forecast, judgment, buyer-proof packet, Capture request, Data Lake schedule, or client-facing output.

### 3. Source-Family Coverage Plan

| Source family | Subfamily / surface | Capture posture | Why check it | Expected observable | Evidence status | Surface cutoff status | Cutoff status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| forums_community | Basenotes, Fragrantica forums, Parfumo, Reddit fragrance communities | manual_only | Community/tracker surfaces can expose niche fragrance demand before mainstream retail or press. | Dated threads, product pages, discontinued tags, comparison language, repeat questions, objections. | mixed_source_backed_and_to_retrieve | not_applicable | not_applicable | Basenotes and Fragrantica route value is source-backed by the Beauty Venue Card Set; product-specific observations still require Scanning. |
| reviews | specialist fragrance blogs and review pages | manual_only | Outcome-gauge review density can show reception before broad retail. | Dated posts, review language, cross-blog density, product-specific reception. | mixed_source_backed_and_to_retrieve | not_applicable | not_applicable | The blog cluster role is source-backed; exact current product observations remain to_retrieve. |
| retail_pdp | LuckyScent, Scent Bar, Twisted Lily, Ministry of Scent, ZGO, Aedes, Arielle Shoshana | manual_only | Specialist retail may expose precursor commercial behavior after community/tracker uptake but before Sephora/Ulta/Amazon durability. | Review counts/text, sample availability, full-bottle availability, sold-out/restock cues, discovery/list position. | to_retrieve | not_applicable | not_applicable | Treat as candidate route, not proof or capture authorization. |
| retail_pdp | Scent Split, Surrender to Chance, The Perfumed Court, DecantX | manual_only | Sampling and decant behavior may show costly trial demand before full-bottle mainstreaming. | Decant availability, size options, sold-out/restock cues, product breadth, review/comment cues if exposed. | to_retrieve | not_applicable | not_applicable | Needs Scanning to distinguish demand from catalog breadth or supply constraints. |
| retail_pdp | Ulta, Sephora, Amazon | planned_lane | Major retail PDP/review capture is downstream corroboration and durability context. | Review velocity, review text, stock/discount/assortment posture. | source_backed | not_applicable | not_applicable | Existing retail/PDP contracts cover these major retailers; they are not the first precursor route here. |
| search_discovery | Google search, exact-query snippets, marketplace/on-site search | manual_only | Search can reveal hidden venue pointers and access alternatives for walled community surfaces. | Exact-query results, snippets, current indexed pages, query language, absence/decay. | to_retrieve | not_applicable | not_applicable | Scanning owns exact-query discipline; no public web retrieval occurred in this CSB run. |
| creator_social_video | TikTok, YouTube, Instagram fragrance creators | deferred | Creator attention can explain propagation and campaign risk. | Dated posts, repeated audience language, affiliate clusters, propagation timing. | to_retrieve | not_applicable | not_applicable | Use as counterevidence and duplication-risk route before treating it as demand signal. |
| aeo_answer_engines | Google AI Overviews, Gemini, ChatGPT and related answer surfaces | manual_only | AEO can show visibility loops or cited-source ecosystems, not origin demand. | Answer visibility and cited-source loops. | gap | not_applicable | not_applicable | Visibility annotation only; never classifier handoff by itself. |
| news_editorial_trade | Specialist blogs, fragrance newsletters, trade/editorial coverage | manual_only | Editorial coverage can establish chronology and laundering of community discoveries into citable records. | Dated coverage, launch chronology, source mentions, third-party framing. | mixed_source_backed_and_to_retrieve | not_applicable | not_applicable | Blogs are source-backed as a route; current product-specific evidence remains to_retrieve. |
| owned_channels | Brand sites, brand socials, product pages, press releases | manual_only | Owned channels anchor official chronology but are low-independence signals. | Launch dates, product claims, stock language, assortment changes. | to_retrieve | not_applicable | not_applicable | Useful for chronology and contradiction checks only. |
| professional_org_motion | Hiring, partnerships, founder/executive public statements | deferred | May explain supply, launch, or distribution movement but is secondary for fragrance consumer demand. | Hiring, partnership, distribution, founder/executive statements. | not_applicable | not_applicable | not_applicable | Not a priority unless Scanning finds a product-specific reason. |

### 4. Signal Board Rows

| Row ID | Source family | Subfamily | Surface | Observable | Signal role | Row purpose | Recency status | Recency attention | Graph role | Graph weight hint | Evidence status | Provenance needed | Surface cutoff status | Cutoff status | Handoff note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SBR-001 | forums_community | fragrance tracker | Basenotes | Thread and tag routes for niche fragrance demand and discontinued or brand-specific discussion | consumer_language | source_route | current_state | high | seed | high | source_backed | Beauty Venue Card Set card 8 plus later Scanning URLs, dates, snippets, and access notes | not_applicable | not_applicable | Source-backed route for Scanning; not classifier handoff until product-specific dated observations are retrieved. |
| SBR-002 | forums_community | tracker aggregator | Fragrantica | Product pages, news, designer pages, and discontinued-status confirmations | consumer_language | source_route | current_state | high | seed | high | source_backed | Beauty Venue Card Set card 9 plus later Scanning URLs, dates, snippets, and access notes | not_applicable | not_applicable | Source-backed route for Scanning; direct HTTP wall must remain an access note. |
| SBR-003 | news_editorial_trade | specialist fragrance blogs | The Scented Hound, The Plum Girl, CaFleureBon | Dated specialist reviews and cross-blog reception density | review_experience | source_route | current_state | high | node_candidate | medium | source_backed | Beauty Venue Card Set card 12 plus later Scanning URLs and publication dates | not_applicable | not_applicable | Source-backed route for Scanning; product-specific reception still needs retrieval. |
| SBR-004 | retail_pdp | specialist fragrance retail | LuckyScent, Scent Bar, Twisted Lily, Ministry of Scent, ZGO, Aedes, Arielle Shoshana | Review text/counts, sample availability, stock/restock, discovery position, assortment breadth | retail_corroboration | source_route | stale_or_unknown | high | node_candidate | medium | to_retrieve | Current public URLs, observation date, page fields exposed, and access constraints | not_applicable | not_applicable | Candidate specialist-store route; no Capture request until Scanning proves useful public observables. |
| SBR-005 | retail_pdp | sampling and decant retail | Scent Split, Surrender to Chance, The Perfumed Court, DecantX | Decant availability, size options, sold-out/restock cues, catalog breadth, review/comment cues if exposed | retail_corroboration | source_route | stale_or_unknown | high | node_candidate | medium | to_retrieve | Current public URLs, observation date, exposed fields, and supply-context notes | not_applicable | not_applicable | Candidate costly-trial route; Scanning must separate demand from catalog breadth or supply limits. |
| SBR-006 | retail_pdp | major retailer PDP reviews | Ulta, Sephora, Amazon | Review velocity, review text, stock/discount/assortment posture | retail_corroboration | contradiction | current_state | normal | counterevidence_path | medium | source_backed | Existing retail/PDP projection and rendered-capture contracts plus later product-specific capture if authorized | not_applicable | not_applicable | Downstream corroboration or contradiction only; not the first precursor-discovery route. |
| SBR-007 | search_discovery | exact-query and snippets | Google search and marketplace/on-site search | Hidden venue pointers, snippets for walled surfaces, exact product and brand query language | search_interest | source_route | stale_or_unknown | high | propagation_path | medium | to_retrieve | Exact queries, result dates where visible, result URLs, and snippet text | not_applicable | not_applicable | Scanning broad-scout input; search visibility does not prove demand. |
| SBR-008 | creator_social_video | fragrance creator discussion | TikTok, YouTube, Instagram | Dated attention spread, creator clusters, audience language, affiliate/campaign overlap | creator_attention | contradiction | stale_or_unknown | normal | campaign_overlap_check | medium | to_retrieve | Public URLs, post dates, affiliate markers, repeated phrasing, and audience-language excerpts | not_applicable | not_applicable | Counterevidence and campaign-risk route before treating creator attention as demand signal. |
| SBR-009 | forums_community | adjacent public communities | Reddit fragrance communities and public specialist boards | Repeat questions, objections, comparisons, purchase intent language, rejection or no-uptake evidence | consumer_language | contradiction | stale_or_unknown | high | counterevidence_path | high | to_retrieve | Public thread URLs, thread dates, search path, excerpts, and access notes | not_applicable | not_applicable | Mandatory counterevidence route; no login or private-community access. |
| SBR-010 | aeo_answer_engines | answer visibility | Google AI Overviews, Gemini, ChatGPT | Answer visibility, cited-source loops, entity association | aeo_visibility | gap | stale_or_unknown | low | none | none | gap | Current answer surface observations if separately authorized and policy-safe | not_applicable | not_applicable | Visibility annotation only; never demand-origin or classifier handoff by itself. |
| SBR-011 | owned_channels | brand owned surfaces | Brand site, brand socials, product pages, press releases | Official launch chronology, claims, assortment and availability language | owned_claim | source_route | stale_or_unknown | normal | node_candidate | low | to_retrieve | Official URLs, access date, source date, and claim text | not_applicable | not_applicable | Chronology and contradiction context only; low independence. |
| SBR-012 | news_editorial_trade | broader editorial and trade | fragrance newsletters, trade press, indie beauty press | Launch chronology, third-party narrative, laundering of community discoveries into citable records | review_experience | source_route | stale_or_unknown | normal | propagation_path | low | to_retrieve | Article URLs, publication dates, cited sources, and chronology notes | not_applicable | not_applicable | Useful for chronology and propagation, not earliest-origin proof by itself. |

### 5. Mandatory Counterevidence Paths

| Path ID | What could disconfirm or weaken the signal | Source families to check | Why it matters | Evidence status | Cutoff rule |
| --- | --- | --- | --- | --- | --- |
| CEP-001 | Forum/community rejection, indifference, or no repeat discussion despite specialist retail presence | forums_community, search_discovery | Prevents mistaking retail stocking for consumer demand. | to_retrieve | not_applicable_forward_mode |
| CEP-002 | Specialist-store availability reflects distribution breadth or catalog policy, not demand | retail_pdp, owned_channels | Prevents over-reading assortment breadth or sample listings. | to_retrieve | not_applicable_forward_mode |
| CEP-003 | Sampling/decant sold-out cues reflect supply constraints, small batch sizes, or listing gaps | retail_pdp, owned_channels | Prevents mistaking scarcity for costly trial demand. | to_retrieve | not_applicable_forward_mode |
| CEP-004 | Creator or affiliate concentration drives attention without independent community uptake | creator_social_video, forums_community, search_discovery | Separates manufactured hype from distributed demand. | to_retrieve | not_applicable_forward_mode |
| CEP-005 | Major retailer review/PDP evidence contradicts specialist-surface enthusiasm or shows poor durability | retail_pdp | Uses existing major-retailer capture routes only as later corroboration/contradiction. | to_retrieve | not_applicable_forward_mode |
| CEP-006 | AEO/search visibility is a cited-source loop without underlying origin signal | aeo_answer_engines, search_discovery, news_editorial_trade | Prevents treating answer visibility as demand origin. | gap | not_applicable_forward_mode |

### 6. Campaign And Duplication Risk

| Risk ID | Possible duplication/campaign pattern | Surfaces implicated | Required check | Evidence status | Handoff note |
| --- | --- | --- | --- | --- | --- |
| RISK-001 | Affiliate or PR creator cluster creates repeat language before independent uptake | TikTok, YouTube, Instagram, blogs | Check post dates, affiliate markers, repeated phrasing, and non-creator community uptake. | to_retrieve | Scanning counterevidence route. |
| RISK-002 | Retailer merchandising or paid placement appears as discovery/list position | specialist retail PDP and category pages | Check whether list position is editorial, paid, new-arrivals, bestseller, or alphabetic/catalog ordering. | to_retrieve | Do not infer demand from placement alone. |
| RISK-003 | Review-widget syndication duplicates the same review corpus across brand and retail pages | brand PDP, specialist retail, major retail | Check widget provider, duplicate review text, date stamps, and source page identity. | to_retrieve | Important before any Capture expansion. |
| RISK-004 | Search/AEO loops cite the same blogs or retailer pages repeatedly | search_discovery, aeo_answer_engines, blogs | Check cited source diversity and whether snippets point back to a single origin. | gap | Visibility loop is not origin demand. |
| RISK-005 | Fragrance community cross-posting makes one discussion look like multiple independent signals | Basenotes, Fragrantica, Parfumo, Reddit | Check usernames where public, dates, linked references, and repeated language. | to_retrieve | Use only public, bounded, policy-safe observations. |

### 7. Graph Retrieval Brief

```yaml
graph_retrieval_brief:
  seed_entities:
    - Basenotes
    - Fragrantica
    - Parfumo
    - LuckyScent / Scent Bar
    - Twisted Lily
    - Ministry of Scent
    - ZGO Perfumery
    - Aedes Perfumery
    - Arielle Shoshana
    - Scent Split
    - Surrender to Chance
    - The Perfumed Court
    - DecantX
    - CaFleureBon
    - The Scented Hound
    - The Plum Girl
  adjacent_entities_to_check:
    - Reddit fragrance communities
    - TikTok fragrance creator discussion
    - YouTube fragrance reviewers
    - Google exact-query and snippet routes
    - Ulta, Sephora, and Amazon as downstream corroboration context
  creator_slices:
    - fragrance creators with dated public posts
    - affiliate-linked fragrance posts
    - reviewer clusters around indie or niche fragrances
  source_families:
    - forums_community
    - reviews
    - retail_pdp
    - search_discovery
    - creator_social_video
    - aeo_answer_engines
    - news_editorial_trade
    - owned_channels
  mandatory_counterevidence_paths:
    - CEP-001 forum/community rejection or no uptake
    - CEP-002 distribution breadth masquerading as demand
    - CEP-003 sample/decant scarcity caused by supply limits
    - CEP-004 creator or affiliate concentration
    - CEP-005 major retailer contradiction or weak durability
    - CEP-006 AEO/search loop without origin signal
  node_types_to_retrieve:
    - source surface
    - product page
    - dated thread
    - dated review or blog post
    - dated search result or snippet
    - creator post
    - official product page
  edge_types_to_retrieve:
    - product_to_surface
    - brand_to_surface
    - surface_to_source_family
    - creator_to_product
    - retailer_to_product
    - blog_to_product
    - query_to_surface
    - source_to_cited_source
  campaign_overlap_checks:
    - affiliate markers
    - repeated phrasing
    - duplicate review text
    - paid placement or retailer merchandising
    - search/AEO citation loops
  graph_weight_notes: >
    Graph weight is relation utility only. Basenotes and Fragrantica are high
    utility source-route seeds; specialist retail and decant surfaces are medium
    utility node candidates until Scanning proves public observables.
  surface_cutoff_notes: forward mode; no historical cutoff applied.
  forecast_targets_supported_without_probabilities:
    - later review velocity
    - sample and decant availability change
    - specialist-store stockout or restock behavior
    - major-retailer review/PDP durability
    - search-interest decay or persistence
    - campaign-concentration decay
  backtest_cutoff_date: null
  future_info_exclusion_rule: not_applicable_forward_mode
```

### 8. Demand-Classifier Handoff Packet

```yaml
classifier_handoff_packet:
  candidate_or_subject: Specialist fragrance precursor surfaces for US indie and DTC fragrance demand.
  decision_context: >
    Identify and structure the source-family rows needed to decide which
    specialist-fragrance surfaces should be sent to Scanning for precursor-demand
    qualification before Capture or Data Lake expansion.
  mode: forward
  cutoff_date: null
  signal_rows_for_handoff: []
  counterevidence_rows_for_handoff: []
  source_family_gaps:
    - SBR-001 Basenotes route value is source-backed, but product-specific dated observations remain to_retrieve.
    - SBR-002 Fragrantica route value is source-backed, but product-specific dated observations remain to_retrieve.
    - SBR-003 specialist blog route value is source-backed, but product-specific dated observations remain to_retrieve.
    - SBR-004 specialist retail observables are to_retrieve.
    - SBR-005 sampling and decant observables are to_retrieve.
    - SBR-006 major retailer PDP evidence is downstream corroboration only until a later product-specific request.
    - SBR-007 exact-query and search snippet routes are to_retrieve.
    - SBR-008 creator/social campaign-risk routes are to_retrieve.
    - SBR-009 forum/community counterevidence routes are to_retrieve.
    - SBR-010 AEO answer visibility is a gap and cannot enter classifier handoff by itself.
    - SBR-011 owned-channel chronology is to_retrieve and low-independence.
    - SBR-012 broader editorial/trade chronology is to_retrieve.
  provenance_gaps:
    - product-specific public URL
    - source observation date
    - source publication or page date where available
    - access route and access-wall note
    - review text/count provenance if exposed
    - stockout, restock, sample-availability, or listing-position provenance if exposed
  cutoff_uncertainties: []
  durability_projection_evidence_or_gap: No durability evidence yet; later Scanning/Capture would need dated repeat observations or review/PDP changes.
  decay_lifespan_evidence_or_gap: No decay/lifespan evidence yet; later Scanning would need dated recurrence, absence, or drop-off observations.
  manufactured_hype_dedup_risk: High enough to check before any demand read; creator, affiliate, review-widget, retailer-placement, and search/AEO-loop risks remain to_retrieve.
  classifier_mapping_status: classifier_owned
  prohibited_claims:
    - no demand verdict
    - no buyer-proof claim
    - no validation or readiness claim
    - no graph score
    - no forecast probability
    - no Capture authorization
    - no Data Lake routine authorization
```

### 9. Visible Limitations

- This CSB run used supplied repo context only; it did not perform public web retrieval.
- Basenotes and Fragrantica route value is source-backed by the Beauty Venue Card Set, but their current product-specific observations remain to_retrieve.
- Specialist retail, sampling/decant, creator/social, exact-query, owned-channel, and broader editorial rows remain unverified until Scanning returns dated observations or negatives.
- The board does not rank stores, prove precursor value, decide Capture routes, authorize scraping, create a source registry, schedule Data Lake checks, or classify demand.
- The classifier handoff is intentionally empty because no product-specific source-backed observations were retrieved in this run.

### 10. Board Status And Run Boundary

```yaml
board_status: READY_FOR_RETRIEVAL_HANDOFF
run_boundary: CHAT_ONLY_BOARD_COMPLETE
next_authorized_step: Run CSB-first Scanning broad-scout against this board; Capture remains blocked until Scanning emits a bounded capture_request.
```
