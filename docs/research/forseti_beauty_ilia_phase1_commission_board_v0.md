# ILIA Beauty Phase 1 — Sealed Company Commission Board v0

```yaml
retrieval_header_version: 1
artifact_role: Sealed company competitive-intelligence commission board
scope: >
  Historical sealed Phase 1 commission boundary for ILIA Beauty, pool row
  USBEAUTY-021, preserved as the pre-scan input to the withdrawn report.
use_when:
  - Auditing the historical ILIA Phase 1 commissioned routes and pre-scan boundary.
  - Tracing the withdrawn report back to its sealed commission input.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_beauty_ilia_phase1_scan_receipt_v0.md
stale_if:
  - Always as a reusable commission or current-report router; the associated report was withdrawn from decision-facing use on 2026-07-19.
  - The owner supersedes the ILIA Phase 1 commission or its governing CSB contract.
```

> **Historical sealed input only.** Do not reuse this board to dispatch a
> current ILIA commission or to select a current report. Its associated report,
> `docs/research/forseti_beauty_ilia_phase1_company_competitive_intelligence_report_v0.md`,
> remains present only as historical provenance; no replacement exists yet.

Seal timing note: the 2026-07-18 handoff and eligibility-pool row bound the
subject and routes before Capture reconnaissance began. This board translates
that already-bound commission into the CSB contract shape before the Scanning
walk, classification, and typed synthesis. It contains no conclusions from the
reconnaissance packets.

### 1. Company Commission And Identity Receipt

```yaml
company_commission_receipt:
  commission_id: ilia_beauty_phase1_20260718
  mode: forward
  commission_profile: company_competitive_intelligence
  subject_count: 1
  subject_identity:
    raw_name: ILIA Beauty
    subject_kind: brand
    identity_state: resolved
  as_of_date: "2026-07-18"
  time_posture: recency_first
  longitudinal_period: null
  longitudinal_rationale: not_applicable
  initial_proving_run: true
```

### 2. Decision-Neutral Boundary

This commission records observable positioning, offerings, claims, channels,
ownership and entity context, operating chronology, and external customer
response for ILIA Beauty only. Parent-owned identity is tested explicitly, but
the report makes no pain, buyer, ICP, priority, urgency, willingness-to-pay,
outreach, offer, wedge, or GTM conclusion. Deep competitor treatment requires a
separately named follow-up.

### 3. Source-Family And Venue Coverage Ledger

```yaml
coverage_ledger:
  - coverage_id: COV-001
    source_family: other
    source_surface: eligibility_pool
    venue: Forseti beauty eligibility pool
    relevance_rationale: Binds the commissioned subject and resolved parent before external scanning.
    route_or_query: docs/research/forseti_beauty_us_company_eligibility_pool_v0.md#USBEAUTY-021
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_commission_input
    access: local_public_research_artifact
    relevance: relevant
    gap_id: null
  - coverage_id: COV-002
    source_family: owned_channels
    source_surface: official_site_and_product_pages
    venue: ILIA Beauty
    relevance_rationale: Current positioning, offering, claims, hero products, and direct-commerce mechanics.
    route_or_query: https://iliabeauty.com/ and named hero PDPs
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: route_commissioned
    relevance: relevant
    gap_id: null
  - coverage_id: COV-003
    source_family: reviews
    source_surface: substantive_purchase_reviews
    venue: ILIA Beauty and Sephora
    relevance_rationale: Customer experience and claim-attack evidence with verified-purchase handling where exposed.
    route_or_query: ILIA and Sephora hero-product review surfaces
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: route_commissioned
    relevance: relevant
    gap_id: null
  - coverage_id: COV-004
    source_family: retail_pdp
    source_surface: retailer_product_and_brand_pages
    venue: Sephora and Ulta Beauty
    relevance_rationale: Current US assortment, pricing, availability, claims corroboration, and review aggregates.
    route_or_query: ILIA brand and hero-product pages at Sephora and Ulta
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: route_commissioned
    relevance: relevant
    gap_id: null
  - coverage_id: COV-005
    source_family: forums_community
    source_surface: bounded_subreddit_scout
    venue: Reddit
    relevance_rationale: Mandatory bounded scout for customer-world experience, claim attacks, and cited substitutes.
    route_or_query: ILIA and hero-product queries in category-relevant subreddits
    requirement: mandatory_bounded_scout
    status: not_checked
    yield: unknown
    recency: unknown
    access: route_commissioned
    relevance: relevant
    gap_id: null
  - coverage_id: COV-006
    source_family: forums_community
    source_surface: answer_forum_scout
    venue: Quora
    relevance_rationale: Initial-proving-run compatibility scout for a non-duplicative company or product job.
    route_or_query: site:quora.com "ILIA Beauty"
    requirement: experimental_initial_proving_run
    status: not_checked
    yield: unknown
    recency: unknown
    access: route_commissioned
    relevance: mixed
    gap_id: null
  - coverage_id: COV-007
    source_family: search_discovery
    source_surface: category_aware_hidden_venue_discovery
    venue: Public web search
    relevance_rationale: Finds category-specific customer, certifier, regulatory, and entity surfaces without assuming a fixed venue list.
    route_or_query: ILIA beauty claims reviews certification trademark ownership careers
    requirement: category_aware
    status: not_checked
    yield: unknown
    recency: unknown
    access: route_commissioned
    relevance: relevant
    gap_id: null
  - coverage_id: COV-008
    source_family: news_editorial_trade
    source_surface: dated_trade_reporting
    venue: Beauty and fashion trade press
    relevance_rationale: Ownership, distribution, leadership, revenue, and operating chronology with dated caveats.
    route_or_query: ILIA Famille C acquisition distribution leadership
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: route_commissioned
    relevance: relevant
    gap_id: null
  - coverage_id: COV-009
    source_family: professional_org_motion
    source_surface: official_registry_terms_and_careers
    venue: Trademark registry, ILIA legal pages, and ILIA careers
    relevance_rationale: Resolves brand, operating-entity, trademark-owner, parent, and current organizational boundaries.
    route_or_query: ILIA Inc trademark owner terms careers Famille C
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: route_commissioned
    relevance: relevant
    gap_id: GAP-001
  - coverage_id: COV-010
    source_family: other
    source_surface: certifier_directory
    venue: Leaping Bunny
    relevance_rationale: Checks the certifier only because ILIA currently displays the seal.
    route_or_query: Leaping Bunny directory ILIA Inc
    requirement: conditional
    status: not_checked
    yield: unknown
    recency: unknown
    access: route_commissioned
    relevance: relevant
    gap_id: null
  - coverage_id: COV-011
    source_family: retail_pdp
    source_surface: amazon_us_distribution
    venue: Amazon US
    relevance_rationale: Tests seller of record, authorized-reseller alignment, US storefront pin, and diversion state.
    route_or_query: ILIA hero products on Amazon.com with US delivery pin
    requirement: conditional
    status: not_checked
    yield: unknown
    recency: unknown
    access: route_commissioned
    relevance: relevant
    gap_id: null
  - coverage_id: COV-012
    source_family: creator_social_video
    source_surface: public_video_and_comments
    venue: Public creator video
    relevance_rationale: Conditional route for a non-duplicative use demonstration or customer-response job.
    route_or_query: ILIA hero-product creator video and comments
    requirement: conditional
    status: not_checked
    yield: unknown
    recency: unknown
    access: route_commissioned
    relevance: mixed
    gap_id: null
```

### 4. Observation Ledger

```yaml
observation_ledger:
  - observation_id: OBS-001
    subject_name: ILIA Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-001
    source_url_or_packet_locator: docs/research/forseti_beauty_us_company_eligibility_pool_v0.md#USBEAUTY-021
    source_family: other
    source_surface: eligibility_pool
    publisher_or_venue: Forseti
    source_class: unknown
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-18T03:30:00Z"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-18"
    age_anchor_basis: current_page_observation
    exact_locator: Final 20 row USBEAUTY-021
    evidence_excerpt: The accepted commission input identifies ILIA Beauty as a scaling makeup brand with Famille C as resolved parent.
    lawful_access_route: local_repository_read
    access_limitation: Commission input only; external entity, trademark, and ownership checks remain commissioned.
    independence_syndication_group: forseti_eligibility_pool_ilia_001
    independent_corroboration_ids: []
    ambiguity_limitation: The pool resolves the parent for dispatch but does not by itself bind the current legal operating entity.
    contradiction_state: parent_entity_verification_open
    fact_domain: company_fact
    current_state_use: primary_current
    consumed_by_sections: [2, 6, 8, 9]
```

### 5. Positioning, Offerings, Markets, And Channels

OBS-001 binds only the commissioned subject and parent pointer; no external
scan conclusion is earned at seal time. Official claims, hero
offerings, direct commerce, and US retail channels are commissioned in
COV-002 through COV-004 and COV-011.

### 6. Strategic And Operating Chronology

The commission input supplies only the parent pointer (OBS-001). Acquisition,
leadership, distribution, and organization chronology remain commissioned in
COV-008 and COV-009; no trajectory is inferred.

### 7. Customer And Community Response

OBS-001 contains no customer evidence, so no customer or community conclusion
is earned at seal time. The substantive
review, mandatory Reddit, experimental Quora, category-aware discovery, and
conditional creator routes remain unrun.

### 8. Competitor Context, Contradictions, And Gaps

Comparator pointers may be collected only when they interpret ILIA. Deep
competitor treatment remains a separately named follow-up. The load-bearing
pre-scan gap is the parent-owned identity boundary: ILIA the brand is resolved,
while the relationship among ILIA Inc., the trademark owner, Famille C, and any
operating entity requires external checks (OBS-001; GAP-001).

### 9. Company Surface Candidate Ledger

```yaml
company_surface_candidate_ledger:
  - candidate_id: CSC-001
    observation_ids: [OBS-001]
    candidate_only: true
    import_status: not_imported
    candidate_fact_class: company_fact
    bounded_fact: The accepted commission input identifies ILIA Beauty as the subject and Famille C as its resolved parent for this run.
    identity_state: resolved
    time_scope: commission_input_observed_2026-07-18
    limitations: External entity, trademark, and ownership checks are still commissioned; no Company Surface import occurred.
```

### 10. Completion Ledger And Run Boundary

```yaml
completion_ledger:
  completion_scope: csb_planning_only_not_acquisition
  coverage_status: complete_with_typed_gap
  observation_status: traceable
  candidate_status: candidate_only_not_imported
  completeness_policy: necessary_complete_no_arbitrary_caps
  hidden_venue_discovery: category_aware
  reddit_scout_status: commissioned_not_yet_run
  quora_scout_status: commissioned_not_yet_run
  customer_community_boundary: external_evidence_not_representative_demand_or_internal_fact
  deep_competitor_treatment: separate_named_follow_up_required
  classifier_handoff: omitted
  required_lens_coverage:
    positioning: {status: gap, observation_ids: [], rationale: official source routes are commissioned but not yet scanned}
    offerings_and_claims: {status: gap, observation_ids: [], rationale: product and retailer routes are commissioned but not yet scanned}
    markets_and_channels: {status: gap, observation_ids: [], rationale: direct and retail channel routes are commissioned but not yet scanned}
    strategic_and_operating_moves: {status: gap, observation_ids: [OBS-001], rationale: parent pointer exists but acquisition and organization chronology remain unscanned}
    customer_and_community_response: {status: gap, observation_ids: [], rationale: review and community routes are commissioned but not yet scanned}
    competitor_and_substitute_context: {status: gap, observation_ids: [], rationale: bounded comparator pointers may be collected only if they interpret ILIA}
    contradictions: {status: complete, observation_ids: [OBS-001], rationale: parent and operating-entity verification boundary is explicit}
    evidence_gaps: {status: complete, observation_ids: [OBS-001], rationale: GAP-001 names the parent-owned identity stressor}
  gaps:
    - gap_id: GAP-001
      gap_type: identity
      status: open
      description: The brand subject and parent pointer are bound, but current trademark-owner, operating-entity, and parent relationships require external verification.
      affected_coverage_ids: [COV-009]
      request_ids: [REQ-002]
  requests:
    - request_id: REQ-001
      request_type: bounded_fresh_scan
      owner: scanning
      status: requested
      description: Execute the commissioned source-family walk and stop at necessary completeness with typed access outcomes.
      source_surface: multi_source_company_scan
    - request_id: REQ-002
      request_type: entity_identity_verification
      owner: scanning
      status: requested
      description: Verify ILIA brand, ILIA Inc trademark ownership, Famille C parent ownership, and any current operating-entity boundary without rewriting the CSB contract.
      source_surface: official_registry_terms_and_careers
  run_boundary: COMMISSION_SEALED_PRE_SCAN
  next_authorized_step: Scanning and Capture may execute only the commissioned ILIA routes; no Company Surface import, classifier handoff, GTM conclusion, or next-company dispatch is authorized.
```
