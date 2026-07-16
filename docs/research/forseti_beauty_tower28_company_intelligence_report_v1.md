# Tower 28 Beauty — Phase 1 Company-Intelligence Report v1

```text
retrieval_header_version: 1
artifact_role: Research artifact (Phase 1 decision-neutral company-intelligence report)
scope: Sealed Phase 1 synthesis for the restarted Tower 28 lane. Company substrate and
  customer-world venue map with facts, proxies, inference, counterevidence, dates, and
  gaps separated. Decision-aware, decision-neutral. Built only from the sealed commission
  (docs/research/forseti_beauty_tower28_company_intelligence_csb_v1.md) and sealed scan
  (docs/research/forseti_beauty_tower28_company_intelligence_scan_v1.md).
use_when:
  - Running the Phase 2 Tower 28 GTM adjudication (every material Phase 2 claim must cite OBS ids here or fresh supplementary evidence).
  - Re-checking what is fact, proxy, inference, counterevidence, or gap about Tower 28 as of 2026-07-17.
authority_boundary: retrieval_only
stale_if:
  - Material Tower 28 company or channel state changes after 2026-07-17.
  - A later Phase 1 report supersedes this one.
note: header uses a text fence so the first yaml block is Section 1's receipt.
```

## How To Read This Report

Every material claim resolves to an observation row (OBS-NNN) carrying source,
dates, evidence class, access, independence, contradiction state, and
limitations. The deterministic recency ladder is anchored to
`as_of_date: 2026-07-17`: over-180-day material is chronology/baseline only and
never carries a current-pressure claim. Proxies are labeled with their ceilings
— review counts and ratings are reception context, never sell-through, repeat
purchase, or representative demand; community language is external customer
evidence, never internal company fact; job postings are org motion, never
execution capacity. Scan-move provenance (M/EQ/SOBS/CR ids) lives in the sealed
scan receipt.

### 1. Company Commission And Identity Receipt

```yaml
company_commission_receipt:
  commission_id: tower28_ci_phase1_2026_07_16
  mode: forward
  commission_profile: company_competitive_intelligence
  subject_count: 1
  subject_identity:
    raw_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
  as_of_date: "2026-07-17"
  time_posture: recency_first
  longitudinal_period: null
  longitudinal_rationale: not_applicable
  initial_proving_run: true
```

### 2. Decision-Neutral Boundary

This report records observable company and external-response evidence for one
subject, Tower 28 Beauty. Permitted lenses are the adjudicated
information-priority families (customer choice/product failure, demand
durability, retail/channel productivity, versioned claims, economics and
concentration, execution capacity, and constraints), applied strictly as
observable substrate. It may expose candidate decision surfaces; it assigns no
pain, buyer, ICP, urgency, willingness to pay, outreach, offer, or wedge value
and reaches no demand conclusion. Named alternatives appear only as bounded
comparator pointers that interpret the subject; deep competitor treatment
requires a separately named follow-up commission. Community evidence is
external customer evidence only — never representative demand, sell-through,
repeat purchase, internal company fact, or buyer proof.

### 3. Source-Family And Venue Coverage Ledger

```yaml
coverage_ledger:
  - coverage_id: COV-001
    source_family: owned_channels
    source_surface: brand_site
    venue: tower28beauty.com (home, about, stores pages)
    relevance_rationale: "First-party positioning, identity, and channel-set statements."
    route_or_query: https://www.tower28beauty.com/
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16
    access: public_web_intermittent_503_then_ok
    relevance: relevant
    gap_id: null
  - coverage_id: COV-002
    source_family: retail_pdp
    source_surface: retailer_search
    venue: Sephora search
    relevance_rationale: "Carriage corroboration from the selection run."
    route_or_query: https://www.sephora.com/search?keyword=Tower+28+Beauty
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-003
    source_family: retail_pdp
    source_surface: retailer_search
    venue: Revolve
    relevance_rationale: "Second observed US retail partner."
    route_or_query: https://www.revolve.com/r/Search.jsp?search=Tower+28+Beauty
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16
    access: public_web_selection_run_observation_direct_reread_bot_blocked
    relevance: relevant
    gap_id: null
  - coverage_id: COV-004
    source_family: forums_community
    source_surface: bounded_subreddit_scout
    venue: Reddit
    relevance_rationale: "Mandatory bounded customer-world scout (old.reddit subreddit-restricted searches via the sanctioned screening route) across r/MakeupAddiction, r/SkincareAddiction, r/Sephora, r/beauty, r/30PlusSkinCare, r/eczema."
    route_or_query: old.reddit.com/r/<sub>/search?q=Tower%2028&restrict_sr=on&sort=new&t=year
    requirement: mandatory_bounded_scout
    status: checked
    yield: evidence_found
    recency: listings_current_to_2026-07-17
    access: listings_public_thread_bodies_login_walled
    gap_id: GAP-002
    relevance: relevant
  - coverage_id: COV-005
    source_family: forums_community
    source_surface: answer_forum_scout
    venue: Quora
    relevance_rationale: "Experimental scout required for the initial proving run."
    route_or_query: quora.com/search?q="Tower 28" beauty plus site:quora.com web search
    requirement: experimental_initial_proving_run
    status: blocked
    yield: blocked
    recency: unknown
    access: login_wall_plus_zero_search_index_presence
    relevance: unknown
    gap_id: GAP-006
  - coverage_id: COV-006
    source_family: forums_community
    source_surface: category_specialist_venues
    venue: Sephora Beauty Insider Community (read-only archive), Thingtesting, eczema-reviewer blogs, MakeupAlley
    relevance_rationale: "Category-aware hidden-venue discovery from need-state cues."
    route_or_query: discovered via EQ-012, EQ-013, EQ-018 (see scan)
    requirement: category_aware
    status: checked
    yield: evidence_found
    recency: mixed_2023_to_2026
    access: BIC_browser_readable_thingtesting_403_makeupalley_zero_index
    relevance: relevant
    gap_id: null
  - coverage_id: COV-007
    source_family: reviews
    source_surface: retailer_reviews_state
    venue: Sephora ratings and review counts (brand-page level)
    relevance_rationale: "Reception dispersion and volume context across the line."
    route_or_query: https://www.sephora.com/brand/tower-28
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16
    access: public_web_browser
    relevance: relevant
    gap_id: GAP-008
  - coverage_id: COV-008
    source_family: reviews
    source_surface: retailer_reviews_and_qa
    venue: Ulta
    relevance_rationale: "Carriage state was itself the fact to establish."
    route_or_query: brand stores page plus retailer-expansion web search (EQ-015)
    requirement: conditional
    status: checked
    yield: zero_yield
    recency: current_as_of_2026-07-16
    access: direct_site_read_bot_blocked_fact_established_via_first_party_list
    relevance: relevant
    gap_id: null
  - coverage_id: COV-009
    source_family: retail_pdp
    source_surface: marketplace_presence
    venue: Amazon
    relevance_rationale: "Marketplace presence and seller-control state."
    route_or_query: amazon search from SG vantage (geo-redirected)
    requirement: conditional
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-17
    access: US_vantage_unavailable_geo_redirect_to_amazon_sg
    relevance: relevant
    gap_id: GAP-004
  - coverage_id: COV-010
    source_family: retail_pdp
    source_surface: retailer_brand_page_state
    venue: Sephora Tower 28 brand page
    relevance_rationale: "Current assortment, price, and reception state."
    route_or_query: https://www.sephora.com/brand/tower-28
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16
    access: public_web_browser
    relevance: relevant
    gap_id: null
  - coverage_id: COV-011
    source_family: owned_channels
    source_surface: brand_pdp_claims_price
    venue: tower28beauty.com collections and ingredients pages
    relevance_rationale: "Exact current product, price, promotion, availability, and claim versions."
    route_or_query: tower28beauty.com/collections/* and /pages/ingredients
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-012
    source_family: creator_social_video
    source_surface: tiktok_public
    venue: TikTok
    relevance_rationale: "Complaint-theme and comparison content indexed by search engines."
    route_or_query: search-indexed titles/URLs only; live reads not authorized in this lane
    requirement: conditional
    status: blocked
    yield: blocked
    recency: index_current_2026
    access: not_separately_authorized
    relevance: relevant
    gap_id: GAP-003
  - coverage_id: COV-013
    source_family: creator_social_video
    source_surface: instagram_public
    venue: Instagram
    relevance_rationale: "Brand and creator surfaces."
    route_or_query: not accessed; live reads not authorized in this lane
    requirement: conditional
    status: blocked
    yield: blocked
    recency: unknown
    access: not_separately_authorized
    relevance: unknown
    gap_id: GAP-003
  - coverage_id: COV-014
    source_family: creator_social_video
    source_surface: youtube_public
    venue: YouTube
    relevance_rationale: "Comparison/review genre density and framing."
    route_or_query: YouTube search and video pages (screen-light, no login)
    requirement: conditional
    status: checked
    yield: evidence_found
    recency: snippet_dated_2025_estimates_unverified
    access: JS_pages_limit_metadata_verification
    relevance: relevant
    gap_id: null
  - coverage_id: COV-015
    source_family: search_discovery
    source_surface: search_surface_mgt
    venue: public search surfaces
    relevance_rationale: "Market language, comparison pairs, hidden venues, counterevidence queries."
    route_or_query: EQ-010 through EQ-020 (see scan exact-query ledger)
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_2026-07-16
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-016
    source_family: aeo_answer_engines
    source_surface: answer_visibility
    venue: answer engines
    relevance_rationale: "Visibility annotation only; conditional row."
    route_or_query: not run this pass
    requirement: conditional
    status: not_checked
    yield: unknown
    recency: not_applicable
    access: not_attempted
    relevance: unknown
    gap_id: GAP-005
  - coverage_id: COV-017
    source_family: news_editorial_trade
    source_surface: trade_press
    venue: BeautyMatter, Drug Store News, Cosmetics Business; WWD paywalled
    relevance_rationale: "Dated chronology for distribution, launches, leadership, ownership."
    route_or_query: targeted trade searches (see scan EQ-016, EQ-017, EQ-020)
    requirement: required
    status: checked
    yield: evidence_found
    recency: items_dated_2025-05_to_2026-05
    access: wwd_tollbit_402_paywall_others_open
    relevance: relevant
    gap_id: GAP-009
  - coverage_id: COV-018
    source_family: professional_org_motion
    source_surface: careers_ats_and_leadership
    venue: tower28beauty.com/pages/careers-new
    relevance_rationale: "Hiring posture and role ownership signals (org motion only)."
    route_or_query: https://www.tower28beauty.com/pages/careers-new
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-019
    source_family: owned_channels
    source_surface: press_and_announcements
    venue: tower28beauty.com blog; no dedicated press page exists
    relevance_rationale: "Official chronology with stated dates."
    route_or_query: https://www.tower28beauty.com/blogs/sensitive-content
    requirement: required
    status: checked
    yield: evidence_found
    recency: posts_dated_2019_to_2025-05
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-020
    source_family: professional_org_motion
    source_surface: registries_and_filings
    venue: USPTO (via aggregators)
    relevance_rationale: "Owning-entity resolution and mark portfolio."
    route_or_query: trademark registry searches
    requirement: conditional
    status: checked
    yield: evidence_found
    recency: registrations_2022_and_2024
    access: trademarkelite_open_uspto_report_403
    relevance: relevant
    gap_id: null
```

### 4. Observation Ledger

```yaml
observation_ledger:
  - observation_id: OBS-001
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-001
    source_url_or_packet_locator: https://www.tower28beauty.com/
    source_family: owned_channels
    source_surface: brand_site
    publisher_or_venue: Tower 28 Beauty
    source_class: official_first_party
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-16"
    age_anchor_basis: current_page_observation
    exact_locator: "homepage hero and promo banner"
    evidence_excerpt: "Live DTC storefront; mission line 'High-performance makeup and skincare that is safe for even the most sensitive skin'; free US shipping over $30; first-order gift promo."
    lawful_access_route: public_web
    access_limitation: "homepage promo content rotates"
    independence_syndication_group: tower28_owned
    independent_corroboration_ids: []
    ambiguity_limitation: "brand identity resolved; marketing copy is self-description"
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: primary_current
    consumed_by_sections: [5, 9]
  - observation_id: OBS-002
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-001
    source_url_or_packet_locator: https://www.tower28beauty.com/pages/about-2-0
    source_family: owned_channels
    source_surface: brand_site
    publisher_or_venue: Tower 28 Beauty
    source_class: official_first_party
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-16"
    age_anchor_basis: current_page_observation
    exact_locator: "about page founder section"
    evidence_excerpt: "Founder/CEO Amy Liu; Los Angeles origin; founder's chronic-eczema history framed as brand origin; 'Sensitive skin is not an afterthought. It is the starting point for everything we do.'"
    lawful_access_route: public_web
    access_limitation: "self-reported narrative; founder history not independently dated"
    independence_syndication_group: tower28_owned
    independent_corroboration_ids: []
    ambiguity_limitation: "leadership continuity corroborated only by absence of contrary press (OBS-016)"
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: primary_current
    consumed_by_sections: [5, 6]
  - observation_id: OBS-003
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-011
    source_url_or_packet_locator: https://www.tower28beauty.com/pages/ingredients
    source_family: owned_channels
    source_surface: brand_pdp_claims_price
    publisher_or_venue: Tower 28 Beauty
    source_class: official_first_party
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-16"
    age_anchor_basis: current_page_observation
    exact_locator: "ingredients/philosophy page and about page seal claims"
    evidence_excerpt: "Claims architecture: excluded-ingredient list, third-party sensitive-skin/irritation testing language, 'Certified Clean at Sephora/Credo', EU-regulation and Prop-65 compliance claims; 'first and only brand' with National Eczema Association, National Rosacea Society, and National Psoriasis Foundation seals on all skincare; the page does not use the words non-comedogenic or vegan."
    lawful_access_route: public_web
    access_limitation: "claim copy versions rotate; no version history preserved"
    independence_syndication_group: tower28_owned
    independent_corroboration_ids: [OBS-029]
    ambiguity_limitation: "the 'first and only' claim and per-product seal scope are unverified"
    contradiction_state: divergence_with_retailer_pdp_copy_see_OBS-023
    fact_domain: company_fact
    current_state_use: primary_current
    consumed_by_sections: [5, 8, 9]
  - observation_id: OBS-004
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-011
    source_url_or_packet_locator: https://www.tower28beauty.com/collections/complexion
    source_family: owned_channels
    source_surface: brand_pdp_claims_price
    publisher_or_venue: Tower 28 Beauty
    source_class: official_first_party
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-16"
    age_anchor_basis: current_page_observation
    exact_locator: "complexion, lip, and cheek collection grids"
    evidence_excerpt: "DTC catalog state: Swipe concealer $24 (21 shades, brand-labeled Bestseller); SunnyDays tint $32 (17 shades, several shades sold out); GetSet powder $28; ShineOn Plumping $18 (NEW); LipSoftie $16; GetSet blush $22 (9 shades); SuperDew $18 sold out; bundles $50-$88; LipSoftie Deluxe set marked down from $128 to $118."
    lawful_access_route: public_web
    access_limitation: "point-in-time availability; per-shade sold-out states are volatile"
    independence_syndication_group: tower28_owned
    independent_corroboration_ids: [OBS-008]
    ambiguity_limitation: "brand labels (Bestseller, TikTok Viral) are self-designations, not verified rankings"
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: primary_current
    consumed_by_sections: [5, 9]
  - observation_id: OBS-005
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-001
    source_url_or_packet_locator: https://www.tower28beauty.com/pages/stores
    source_family: owned_channels
    source_surface: brand_site
    publisher_or_venue: Tower 28 Beauty
    source_class: official_first_party
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-16"
    age_anchor_basis: current_page_observation
    exact_locator: "stores and sellers page"
    evidence_excerpt: "Brand-listed channel set: DTC, Sephora (US, Canada, UK, Middle East), Sephora at Kohl's, Credo Beauty (six cities), Mecca (Australia), TikTok Shop, Revolve. Ulta absent. Amazon absent."
    lawful_access_route: public_web
    access_limitation: "page may lag actual channel reality"
    independence_syndication_group: tower28_owned
    independent_corroboration_ids: [OBS-008, OBS-010]
    ambiguity_limitation: "Amazon omission unresolved against brand-attributed Amazon GMV (OBS-012); see GAP-004"
    contradiction_state: amazon_channel_listing_vs_gmv_attribution
    fact_domain: company_fact
    current_state_use: primary_current
    consumed_by_sections: [5, 8, 9]
  - observation_id: OBS-006
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-018
    source_url_or_packet_locator: https://www.tower28beauty.com/pages/careers-new
    source_family: professional_org_motion
    source_surface: careers_ats_and_leadership
    publisher_or_venue: Tower 28 Beauty
    source_class: official_first_party
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-16"
    age_anchor_basis: current_page_observation
    exact_locator: "careers page role list"
    evidence_excerpt: "Five open roles, all marketing/e-commerce/content: Brand Marketing Director, Brand Marketing Senior Manager, Ecommerce Director/Senior Manager, Social Media Manager, Director of Content (West LA hybrid where stated)."
    lawful_access_route: public_web
    access_limitation: "listings churn; a Field Sales AE role appeared in stale search indexing but not on the live page"
    independence_syndication_group: tower28_owned
    independent_corroboration_ids: []
    ambiguity_limitation: "org-motion evidence only; a single-day snapshot is not an org chart and never execution-capacity fact"
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: primary_current
    consumed_by_sections: [6]
  - observation_id: OBS-007
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-019
    source_url_or_packet_locator: https://www.tower28beauty.com/blogs/sensitive-content
    source_family: owned_channels
    source_surface: press_and_announcements
    publisher_or_venue: Tower 28 Beauty
    source_class: official_first_party
    publication_date: "2025-05-12"
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: day
    recency_tier: days_over_180
    age_anchor_date: "2025-05-12"
    age_anchor_basis: publication
    exact_locator: "blog post 'SPF Shouldn't Be This Hard—So We Fixed It', dated 2025-05-12"
    evidence_excerpt: "On-site dated post corroborating the SPF category entry window; WWD reportedly covered SOS FaceGuard SPF 30 launch ~2025-05 (headline-level, paywalled, dates unverified)."
    lawful_access_route: public_web
    access_limitation: "WWD primary text not read (Tollbit 402); launch effective dates snippet-level"
    independence_syndication_group: tower28_owned
    independent_corroboration_ids: []
    ambiguity_limitation: "brand blog has only six visible posts (2019-2025); official chronology surface is thin"
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: chronology_historical_baseline
    consumed_by_sections: [6]
  - observation_id: OBS-008
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-010
    source_url_or_packet_locator: https://www.sephora.com/brand/tower-28
    source_family: retail_pdp
    source_surface: retailer_brand_page_state
    publisher_or_venue: Sephora
    source_class: retailer
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-16"
    age_anchor_basis: current_page_observation
    exact_locator: "brand page product grid (25 items) read from page state"
    evidence_excerpt: "Sephora US carries 25 Tower 28 items including a seven-product SOS skincare family (spray $12-$68 with jumbo refill, moisturizer, cleanser, serum, lip balm, body wash, FaceGuard SPF $18-$32) alongside makeup heroes (Swipe $24, ShineOn $16, BeachPlease $20, MakeWaves $12-$20)."
    lawful_access_route: public_web_browser
    access_limitation: "assortment state only; not velocity, productivity, or sell-through"
    independence_syndication_group: sephora_catalog
    independent_corroboration_ids: [OBS-004]
    ambiguity_limitation: "assortment is a joint brand-retailer decision; breadth is not performance"
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: primary_current
    consumed_by_sections: [5, 6, 9]
  - observation_id: OBS-009
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-007
    source_url_or_packet_locator: https://www.sephora.com/brand/tower-28
    source_family: reviews
    source_surface: retailer_reviews_state
    publisher_or_venue: Sephora
    source_class: retailer
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-16"
    age_anchor_basis: current_page_observation
    exact_locator: "brand page rating and review-count fields per product"
    evidence_excerpt: "Reception dispersion: GetSet blush 4.57 (436), ShineOn 4.46 (5,608), BeachPlease 4.47 (1,902), FaceGuard SPF 4.46 (599), Swipe 4.34 (3,652) versus SOS spray 4.09 (4,855), SunnyDays tint 3.98 (1,941), MakeWaves mascara 3.82 (2,953), GetSet powder 3.71 (542), SuperDew 3.56 (356)."
    lawful_access_route: public_web_browser
    access_limitation: "aggregate ratings only; review text not sampled this pass (GAP-008)"
    independence_syndication_group: sephora_reviews_aggregate
    independent_corroboration_ids: []
    ambiguity_limitation: "ratings/counts are reception proxies — proxy ceiling: not sell-through, repeat purchase, representative demand, or complaint rate"
    contradiction_state: dispersion_between_hero_and_secondary_items
    fact_domain: external_customer_evidence
    current_state_use: primary_current
    consumed_by_sections: [7, 8, 9]
  - observation_id: OBS-010
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-003
    source_url_or_packet_locator: "https://www.revolve.com/r/Search.jsp?search=Tower+28+Beauty (recorded in docs/research/forseti_beauty_us_company_selection_v0.json row USBEAUTY-019)"
    source_family: retail_pdp
    source_surface: retailer_search
    publisher_or_venue: Revolve
    source_class: retailer
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-16"
    age_anchor_basis: current_page_observation
    exact_locator: "Revolve search results (selection-run observation)"
    evidence_excerpt: "Revolve returned Tower 28 Beauty products at observation time; brand stores page independently lists Revolve as a seller."
    lawful_access_route: public_web
    access_limitation: "direct re-read this pass was bot-blocked; carriage rests on the 2026-07-16 selection-run observation plus first-party listing"
    independence_syndication_group: revolve_catalog
    independent_corroboration_ids: [OBS-005]
    ambiguity_limitation: "carriage only; no assortment or velocity detail"
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: current_corroboration
    consumed_by_sections: [5]
  - observation_id: OBS-011
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-009
    source_url_or_packet_locator: https://www.amazon.sg/s?k=Tower+28+Beauty
    source_family: retail_pdp
    source_surface: marketplace_presence
    publisher_or_venue: Amazon (International Store, SG vantage)
    source_class: retailer
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-17"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-17"
    age_anchor_basis: current_page_observation
    exact_locator: "amazon.sg search results for Tower 28 Beauty"
    evidence_excerpt: "Amazon International Store sells Tower 28 (SunnyDays SPF tint at S$51.94 versus US$32 list; listing shows 905 ratings); over 1,000 results returned for the brand query."
    lawful_access_route: public_web_browser
    access_limitation: "geo-redirect prevented a US amazon.com read; seller-of-record identity unknown"
    independence_syndication_group: amazon_marketplace
    independent_corroboration_ids: []
    ambiguity_limitation: "cannot distinguish official storefront from third-party or gray-market flow (GAP-004, capture request CR-003)"
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: current_corroboration
    consumed_by_sections: [5, 8]
  - observation_id: OBS-012
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-017
    source_url_or_packet_locator: https://beautymatter.com/articles/tower-28-expands-its-sephora-footprint
    source_family: news_editorial_trade
    source_surface: trade_press
    publisher_or_venue: BeautyMatter
    source_class: independent
    publication_date: "2026-04-30"
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: day
    recency_tier: days_31_90
    age_anchor_date: "2026-04-30"
    age_anchor_basis: publication
    exact_locator: "article body and Amy Liu interview quotes"
    evidence_excerpt: "Sephora North America footprint doubled from 4 to 8 shelves across ~500 doors; brand-attributed $119M GMV across Amazon, Sephora, and Sephora at Kohl's 'in the past year'; Swipe cited as a top-3 Sephora NA concealer; birthday-gift most-redeemed claim; recent Sephora Middle East launch across 55 doors; Europe/LatAm under evaluation; quote: 'we were literally bursting out of our space.'"
    lawful_access_route: public_web
    access_limitation: "figures are brand-supplied in an interview — one origin; unaudited; trailing period undefined"
    independence_syndication_group: brand_interview_expansion_story
    independent_corroboration_ids: []
    ambiguity_limitation: "independent outlet but dependent content; expansion effective dates not separately stated"
    contradiction_state: amazon_gmv_vs_brand_channel_list_see_OBS-005
    fact_domain: company_fact
    current_state_use: current_corroboration
    consumed_by_sections: [5, 6, 8, 9]
  - observation_id: OBS-013
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-017
    source_url_or_packet_locator: https://drugstorenews.com/tower-28-announces-pvolve-partnership
    source_family: news_editorial_trade
    source_surface: trade_press
    publisher_or_venue: Drug Store News
    source_class: independent
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: undated
    recency_tier: undated_unknown
    age_anchor_date: null
    age_anchor_basis: unknown
    exact_locator: "article page (event framed as February 2026 in scan-time search context; article publication date not captured)"
    evidence_excerpt: "SOS line placed into Pvolve fitness studios — an experiential/wellness channel partnership beyond beauty retail. Month-level event framing only; neither the event date nor the publication date is established, so this row carries no current-state weight."
    lawful_access_route: public_web
    access_limitation: "article publication date not captured; partnership scope, door count, and terms unstated"
    independence_syndication_group: pvolve_announcement
    independent_corroboration_ids: []
    ambiguity_limitation: "announcement-sourced — one origin; page-read time must not date the underlying event"
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: not_applicable
    consumed_by_sections: [6]
  - observation_id: OBS-014
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-020
    source_url_or_packet_locator: https://www.trademarkelite.com/trademark/trademark-detail/97499966/TOWER-28
    source_family: professional_org_motion
    source_surface: registries_and_filings
    publisher_or_venue: USPTO (via TrademarkElite)
    source_class: official_regulatory
    publication_date: null
    event_or_effective_date: "2022-12-13"
    observation_at: "2026-07-16"
    effective_time_precision: day
    recency_tier: days_over_180
    age_anchor_date: "2022-12-13"
    age_anchor_basis: event_effective
    exact_locator: "USPTO Reg. 6925089, Serial 97499966"
    evidence_excerpt: "Word mark TOWER 28 registered 2022-12-13 to Tower 28 Beauty, Inc., Los Angeles, CA (Class 003: cosmetics, cosmetic sunscreen, non-medicated skincare). A 2024 services-class registration and additional applications (including WATERBREAK and SCULPTINO) surfaced snippet-level."
    lawful_access_route: public_web
    access_limitation: "second registration and extra marks unverified by direct read (uspto.report 403)"
    independence_syndication_group: uspto_registry
    independent_corroboration_ids: []
    ambiguity_limitation: "no parent or holding company surfaced in any source; parent question resolves toward an independent operating company, but absence is not proof (GAP-007 boundary)"
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: chronology_historical_baseline
    consumed_by_sections: [6, 9]
  - observation_id: OBS-015
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-017
    source_url_or_packet_locator: "docs/research/forseti_beauty_tower28_company_intelligence_scan_v1.md (EQ-016, EQ-017 negative bundle)"
    source_family: news_editorial_trade
    source_surface: trade_press
    publisher_or_venue: aggregate web search
    source_class: unknown
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: undated
    recency_tier: undated_unknown
    age_anchor_date: null
    age_anchor_basis: unknown
    exact_locator: "scan exact-query ledger rows EQ-016 and EQ-017"
    evidence_excerpt: "Targeted searches found no 2025-2026 funding round, acquisition, leadership change, National Advertising Division challenge, FDA action, recall, or lawsuit involving Tower 28. Earlier-round investors (Prelude Growth Partners, Concept to Co) appear only in aggregator profiles."
    lawful_access_route: public_web
    access_limitation: "absence bounded by search coverage; paywalled trade press could hold unseen events"
    independence_syndication_group: search_negative_bundle
    independent_corroboration_ids: []
    ambiguity_limitation: "absence of evidence is not evidence of absence"
    contradiction_state: none_observed
    fact_domain: unknown
    current_state_use: not_applicable
    consumed_by_sections: [6, 8]
  - observation_id: OBS-016
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-004
    source_url_or_packet_locator: https://old.reddit.com/r/MakeupAddiction/comments/1unb090/tower_28_lipgloss_causing_makeup_separation/
    source_family: forums_community
    source_surface: bounded_subreddit_scout
    publisher_or_venue: r/MakeupAddiction
    source_class: customer_community
    publication_date: "2026-07-04"
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: day
    recency_tier: days_0_30
    age_anchor_date: "2026-07-04"
    age_anchor_basis: publication
    exact_locator: "thread title and submission datetime from sanctioned listing read"
    evidence_excerpt: "Thread titled 'Tower 28 lipgloss causing makeup separation?' posted 2026-07-04 — a dated product-specific failure-mode question."
    lawful_access_route: sanctioned_screening_read_listing
    access_limitation: "thread body login-walled; title-level evidence only (CR-001)"
    independence_syndication_group: reddit_mua_1unb090
    independent_corroboration_ids: []
    ambiguity_limitation: "single post; a question title is not a complaint rate and never representative demand"
    contradiction_state: none_observed
    fact_domain: external_customer_evidence
    current_state_use: supporting_or_recurrence
    consumed_by_sections: [7]
  - observation_id: OBS-017
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-004
    source_url_or_packet_locator: https://old.reddit.com/r/MakeupAddiction/comments/1ty47dw/anyone_elses_tower_28_concealer_suck/
    source_family: forums_community
    source_surface: bounded_subreddit_scout
    publisher_or_venue: r/MakeupAddiction
    source_class: customer_community
    publication_date: "2026-06-06"
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: day
    recency_tier: days_31_90
    age_anchor_date: "2026-06-06"
    age_anchor_basis: publication
    exact_locator: "thread title and submission datetime from sanctioned listing read"
    evidence_excerpt: "Thread titled 'anyone elses tower 28 concealer suck?' posted 2026-06-06 — dated rejection language on the hero concealer. Companion acquisition/use threads in the same venue: 'My first tower 28 haul' (2026-06-18) and 'What powder goes well with the Tower 28 concealer?' (2026-06-23)."
    lawful_access_route: sanctioned_screening_read_listing
    access_limitation: "bodies login-walled; title-level (CR-001)"
    independence_syndication_group: reddit_mua_1ty47dw
    independent_corroboration_ids: []
    ambiguity_limitation: "provocative titles are not measured dissatisfaction; single instances"
    contradiction_state: rejection_and_advocacy_coexist_in_same_venue
    fact_domain: external_customer_evidence
    current_state_use: supporting_or_recurrence
    consumed_by_sections: [7, 8]
  - observation_id: OBS-018
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-004
    source_url_or_packet_locator: https://old.reddit.com/r/Sephora/comments/1tsw0kd/
    source_family: forums_community
    source_surface: bounded_subreddit_scout
    publisher_or_venue: r/Sephora
    source_class: customer_community
    publication_date: "2026-05-31"
    event_or_effective_date: null
    observation_at: "2026-07-17"
    effective_time_precision: day
    recency_tier: days_31_90
    age_anchor_date: "2026-05-31"
    age_anchor_basis: publication
    exact_locator: "thread title from sanctioned listing read"
    evidence_excerpt: "Thread titled 'Don't like Tower 28 mascara - where to go from here?' (2026-05-31) — rejection plus explicit switching intent; a comparison thread 'Tower 28 vs Ciele skin tint review' (2026-05-15) sits in the same venue."
    lawful_access_route: sanctioned_screening_read_listing
    access_limitation: "bodies login-walled (CR-001)"
    independence_syndication_group: reddit_sephora_1tsw0kd
    independent_corroboration_ids: []
    ambiguity_limitation: "coheres with MakeWaves 3.82 rating state (OBS-009) but neither proves a dissatisfaction rate"
    contradiction_state: none_observed
    fact_domain: external_customer_evidence
    current_state_use: supporting_or_recurrence
    consumed_by_sections: [7, 8]
  - observation_id: OBS-019
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-004
    source_url_or_packet_locator: https://old.reddit.com/r/beauty/comments/1ulo4kf/
    source_family: forums_community
    source_surface: bounded_subreddit_scout
    publisher_or_venue: r/beauty
    source_class: customer_community
    publication_date: "2026-07-02"
    event_or_effective_date: null
    observation_at: "2026-07-17"
    effective_time_precision: day
    recency_tier: days_0_30
    age_anchor_date: "2026-07-02"
    age_anchor_basis: publication
    exact_locator: "thread title from sanctioned listing read"
    evidence_excerpt: "Thread titled 'What are people's thoughts on Tower 28?' posted 2026-07-02 — an open, current brand-evaluation conversation."
    lawful_access_route: sanctioned_screening_read_listing
    access_limitation: "responses unread (CR-001)"
    independence_syndication_group: reddit_beauty_1ulo4kf
    independent_corroboration_ids: []
    ambiguity_limitation: "title-level"
    contradiction_state: none_observed
    fact_domain: external_customer_evidence
    current_state_use: supporting_or_recurrence
    consumed_by_sections: [7]
  - observation_id: OBS-020
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-004
    source_url_or_packet_locator: https://old.reddit.com/r/eczema/comments/1sum1co/tower_28_skincare/
    source_family: forums_community
    source_surface: bounded_subreddit_scout
    publisher_or_venue: r/eczema
    source_class: customer_community
    publication_date: "2026-04-24"
    event_or_effective_date: null
    observation_at: "2026-07-17"
    effective_time_precision: day
    recency_tier: days_31_90
    age_anchor_date: "2026-04-24"
    age_anchor_basis: publication
    exact_locator: "thread titles and dates from sanctioned listing read"
    evidence_excerpt: "The eczema need-state community actively discusses the brand and its ingredient class: 'tower 28 skincare' (2026-04-24), 'Make up for Eczema prone skin?' (2026-05-15), hypochlorous-acid comparison threads (2025-12)."
    lawful_access_route: sanctioned_screening_read_listing
    access_limitation: "bodies login-walled (CR-001)"
    independence_syndication_group: reddit_eczema_1sum1co
    independent_corroboration_ids: []
    ambiguity_limitation: "venue relevance established; sentiment and outcomes unknown"
    contradiction_state: none_observed
    fact_domain: external_customer_evidence
    current_state_use: supporting_or_recurrence
    consumed_by_sections: [7]
  - observation_id: OBS-021
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-004
    source_url_or_packet_locator: https://old.reddit.com/r/beauty/comments/1q4k9hv/
    source_family: forums_community
    source_surface: bounded_subreddit_scout
    publisher_or_venue: r/beauty
    source_class: customer_community
    publication_date: "2026-01-05"
    event_or_effective_date: null
    observation_at: "2026-07-17"
    effective_time_precision: day
    recency_tier: days_over_180
    age_anchor_date: "2026-01-05"
    age_anchor_basis: publication
    exact_locator: "thread title from sanctioned listing read"
    evidence_excerpt: "A pale-olive concealer request explicitly excludes 'Tower 28 BU' as unsuitable — shade-range boundary language at the edges of the 21-shade Swipe range."
    lawful_access_route: sanctioned_screening_read_listing
    access_limitation: "title-level; over-180-day tier"
    independence_syndication_group: reddit_beauty_1q4k9hv
    independent_corroboration_ids: []
    ambiguity_limitation: "chronology/recurrence context only; never a current-pressure claim"
    contradiction_state: none_observed
    fact_domain: external_customer_evidence
    current_state_use: chronology_historical_baseline
    consumed_by_sections: [7]
  - observation_id: OBS-022
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-006
    source_url_or_packet_locator: https://community.sephora.com/t5/Skincare-Aware/tower-28-SOS-spray/m-p/6587314
    source_family: forums_community
    source_surface: category_specialist_venues
    publisher_or_venue: Sephora Beauty Insider Community (read-only archive)
    source_class: customer_community
    publication_date: "2023-06-20"
    event_or_effective_date: null
    observation_at: "2026-07-17"
    effective_time_precision: day
    recency_tier: days_over_180
    age_anchor_date: "2023-06-20"
    age_anchor_basis: publication
    exact_locator: "thread posts of 2023-06-19 to 2023-06-24, verified in browser"
    evidence_excerpt: "Verified 2023 language: eczema flare relief ('I'm going through yet another flare up of eczema and it calms right down'; 'great for really bad flare ups where even touching my skin would irritate it') and price-substitution advice ('other hypochlorus acid sprays... cost quite a bit less', naming SkinSmart). Forum now read-only — this venue is archival."
    lawful_access_route: public_web_browser
    access_limitation: "no new conversation accrues; read-only start date unknown"
    independence_syndication_group: bic_sos_thread_2023
    independent_corroboration_ids: []
    ambiguity_limitation: "platform has commercial interest in brands it sells; individual experiences"
    contradiction_state: none_observed
    fact_domain: external_customer_evidence
    current_state_use: chronology_historical_baseline
    consumed_by_sections: [7, 8]
  - observation_id: OBS-023
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-006
    source_url_or_packet_locator: https://community.sephora.com/t5/Customer-Support/Tower-28-concealer/m-p/6907386
    source_family: forums_community
    source_surface: category_specialist_venues
    publisher_or_venue: Sephora Beauty Insider Community (read-only archive)
    source_class: customer_community
    publication_date: "2024-04-25"
    event_or_effective_date: null
    observation_at: "2026-07-17"
    effective_time_precision: day
    recency_tier: days_over_180
    age_anchor_date: "2024-04-25"
    age_anchor_basis: publication
    exact_locator: "complaint post and follow-ups of 2024-04-25, verified in browser"
    evidence_excerpt: "Verified complaint: Swipe 'marketed as an acne safe brand and concealer but it has pore clogging ingredients that broke me out', naming Polyglyceryl-3 Diisostearate against Sephora PDP copy quoted in-thread as 'non-comedogenic'. Sidebar shows recurrence pointers: 'Tower 28 concealer creasing' (2025-07-21), further concealer threads (2025-06), 'tower 28 spray..' (2024-11)."
    lawful_access_route: public_web_browser
    access_limitation: "related 2025 threads unread; single complaint, 3,199 views (context only)"
    independence_syndication_group: bic_concealer_thread_2024
    independent_corroboration_ids: []
    ambiguity_limitation: "the comedogenicity assertion is the customer's, not a test result; one complaint is not a rate"
    contradiction_state: retailer_pdp_claim_vs_customer_experience_and_vs_brand_page_wording_see_OBS-003
    fact_domain: external_customer_evidence
    current_state_use: contradiction
    consumed_by_sections: [7, 8, 9]
  - observation_id: OBS-024
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-006
    source_url_or_packet_locator: https://whimsysoul.com/is-tower-28-review/
    source_family: forums_community
    source_surface: category_specialist_venues
    publisher_or_venue: Whimsy Soul (independent eczema-reviewer blog)
    source_class: independent
    publication_date: "2026-04-16"
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: day
    recency_tier: days_91_180
    age_anchor_date: "2026-04-16"
    age_anchor_basis: publication
    exact_locator: "review body (verified fetch)"
    evidence_excerpt: "Dated first-person eczema experience: 'my skin has genuinely never looked better... I haven't had a rash on my face'; explicit repurchase intent ('I'll keep buying from them'); yet prefers a Typology concealer over Tower 28's."
    lawful_access_route: public_web
    access_limitation: "gifting/PR-sample status undisclosed; independence unproven"
    independence_syndication_group: whimsysoul_review
    independent_corroboration_ids: []
    ambiguity_limitation: "single reviewer; supporting-tier recency"
    contradiction_state: praise_and_partial_substitution_coexist
    fact_domain: external_customer_evidence
    current_state_use: supporting_or_recurrence
    consumed_by_sections: [7]
  - observation_id: OBS-025
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-015
    source_url_or_packet_locator: https://www.tiktok.com/discover/tower-28-spray-broke-me-out
    source_family: creator_social_video
    source_surface: tiktok_public
    publisher_or_venue: TikTok topic/discover pages (titles observed via the search-discovery route only; platform not accessed)
    source_class: creator_social
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: undated
    recency_tier: undated_unknown
    age_anchor_date: null
    age_anchor_basis: unknown
    exact_locator: "search-index title state; pages not accessed in this lane; underlying video dates unknown, so no current-state tier is claimed"
    evidence_excerpt: "Indexed topic-page titles: 'Tower 28 Spray Broke Me Out', 'Does Tower 28 Spray Cause Purging', 'Tower 28 Concealer Made Me Breakout' — a recurring public breakout/purging complaint theme set against the sensitive-skin positioning."
    lawful_access_route: search_index_only_no_platform_access
    access_limitation: "titles are aggregator metadata; underlying video volume, dates, and content unverified (CR-002)"
    independence_syndication_group: tiktok_topic_titles
    independent_corroboration_ids: []
    ambiguity_limitation: "beauty TikTok is heavily gifted/sponsored in both praise and complaint directions; theme-level only"
    contradiction_state: complaint_theme_vs_sensitive_skin_positioning_unverified
    fact_domain: external_customer_evidence
    current_state_use: contradiction
    consumed_by_sections: [7, 8]
  - observation_id: OBS-026
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-014
    source_url_or_packet_locator: https://www.youtube.com/watch?v=NfTCoaa3AnQ
    source_family: creator_social_video
    source_surface: youtube_public
    publisher_or_venue: YouTube (multiple channels)
    source_class: creator_social
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: undated
    recency_tier: undated_unknown
    age_anchor_date: null
    age_anchor_basis: unknown
    exact_locator: "search-result and video-page titles (channel/dates mostly unverifiable screen-light)"
    evidence_excerpt: "A dense comparison genre surrounds the heroes: 'Tower 28 vs NARS Concealer', 'Tower 28 VS Saie', Kosas skin-tint comparisons, Hourglass shorts, 'Worth $24 or Overhyped Clean Beauty?', 'Is Tower 28 Worth The Money Over Drugstore?' — value-skepticism framing recurs."
    lawful_access_route: public_web_no_login
    access_limitation: "upload dates are snippet estimates; sponsorship disclosures unverifiable; titles are not content"
    independence_syndication_group: youtube_comparison_genre
    independent_corroboration_ids: []
    ambiguity_limitation: "campaign/affiliate overlap unknown"
    contradiction_state: none_observed
    fact_domain: external_customer_evidence
    current_state_use: not_applicable
    consumed_by_sections: [7, 8]
  - observation_id: OBS-027
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-015
    source_url_or_packet_locator: https://skinsort.com/products/tower-28-beauty/dupes
    source_family: search_discovery
    source_surface: search_surface_mgt
    publisher_or_venue: dupe aggregators (SkinSort, Brandefy, SkinsKool, Beautymasterlist, Temptalia)
    source_class: independent
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-16"
    age_anchor_basis: current_page_observation
    exact_locator: "dupe listing pages surfaced by EQ-012 and EQ-014"
    evidence_excerpt: "An organized lower-price substitution ecosystem targets both hero franchises: Prequel Universal Skin Solution ($17/4oz) framed against SOS spray ($28); NYX Bare With Me ($12) against Swipe ($24); SkinSort lists ~50 SOS dupes (page labeled 2026); comparison pairs include Saie, Kosas, NARS, Hourglass, Ciele, Supergoop, Summer Fridays, Rhode, Merit."
    lawful_access_route: public_web_search_snippets_some_403
    access_limitation: "several aggregators block fetchers; snippet-level in part"
    independence_syndication_group: dupe_aggregator_ecosystem
    independent_corroboration_ids: []
    ambiguity_limitation: "SEO/affiliate-monetized content — commercial motive; dupe-page existence is not switching volume"
    contradiction_state: none_observed
    fact_domain: competitor_context
    current_state_use: supporting_or_recurrence
    consumed_by_sections: [8]
  - observation_id: OBS-028
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-001
    source_url_or_packet_locator: https://www.tower28beauty.com/pages/stores
    source_family: owned_channels
    source_surface: brand_site
    publisher_or_venue: Tower 28 Beauty stores page (Ulta carriage-absence check)
    source_class: official_first_party
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-16"
    age_anchor_basis: current_page_observation
    exact_locator: "brand stores page (Ulta absent) plus EQ-015 retailer-expansion search corroboration"
    evidence_excerpt: "Tower 28 is not carried at Ulta: the brand's own channel list omits Ulta and no retailer-expansion coverage names it — US specialty-retail exposure concentrates in the Sephora ecosystem."
    lawful_access_route: public_web
    access_limitation: "direct ulta.com read was bot-blocked; absence rests on first-party listing plus search corroboration"
    independence_syndication_group: tower28_owned
    independent_corroboration_ids: []
    ambiguity_limitation: "carriage could change without the stores page updating promptly"
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: primary_current
    consumed_by_sections: [5, 8, 9]
  - observation_id: OBS-029
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-017
    source_url_or_packet_locator: https://nationaleczema.org/press-release/tower28scholarshipfund/
    source_family: news_editorial_trade
    source_surface: trade_press
    publisher_or_venue: National Eczema Association
    source_class: independent
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: undated
    recency_tier: undated_unknown
    age_anchor_date: null
    age_anchor_basis: unknown
    exact_locator: "NEA press-release page (undated at read time)"
    evidence_excerpt: "NEA press item on a Tower 28 scholarship fund; evidences that an institutional relationship behind the brand's seal claims (OBS-003) has existed, without dating it — the currency of the relationship rests on the brand's current pages, not this item."
    lawful_access_route: public_web
    access_limitation: "press-release class; page date not captured"
    independence_syndication_group: nea_press
    independent_corroboration_ids: [OBS-003]
    ambiguity_limitation: "NEA has a funding relationship with the brand — partial dependence; per-product seal scope unverified; undated item carries no current-state weight"
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: not_applicable
    consumed_by_sections: [5, 8]
```

### 5. Positioning, Offerings, Markets, And Channels

Tower 28 Beauty positions as sensitive-skin-first makeup and skincare
("safe for even the most sensitive skin", OBS-001; founder-eczema origin story,
OBS-002), with a claims architecture built on excluded ingredients, third-party
sensitive-skin testing language, and dermatological-association seals
(OBS-003, OBS-029). The current offer spans complexion, lip, cheek, eye, and a
seven-product SOS sensitive-skin skincare family, at $12-$34 single-item price
points (with a $68 jumbo-refill ceiling) and bundles to $88 (OBS-004, OBS-008).
Sephora US carries 25 items
(OBS-008). The brand-listed channel set is DTC, the Sephora ecosystem (US,
Canada, UK, Middle East, and Sephora at Kohl's), Credo, Mecca (Australia),
TikTok Shop, and Revolve (OBS-005, OBS-010); Ulta is decisively absent
(OBS-028), and Amazon flows exist (international store observed, OBS-011;
brand-attributed GMV includes Amazon, OBS-012) despite Amazon's absence from
the brand's own channel list — an unresolved channel-control question
(GAP-004). Sephora is the largest *observed* specialty-retail footprint, and
the brand says that footprint doubled in 2026 (OBS-012, brand-supplied
figures); economic channel concentration, however, is unknown — channel
revenue shares are unobservable externally and the Amazon flows are unresolved,
so no single-retailer-concentration claim is made. Shade-level sold-outs on
SunnyDays and a SuperDew
sold-out state were visible on DTC at observation time (OBS-004) —
availability facts only, not velocity claims.

### 6. Strategic And Operating Chronology

Dated, source-anchored chronology (observation time separated from effective
time throughout): entity registered as Tower 28 Beauty, Inc., Los Angeles, with
the core mark registered 2022-12-13 (OBS-014); SPF category entry (first
sunscreen, an OTC-drug category in the US) in the 2025-05 window per the
brand's dated blog post, with paywalled trade coverage unverified (OBS-007);
Sephora Middle East launch across 55 doors reported as recent in the 2026-04-30
trade interview (OBS-012); a Pvolve fitness-studio partnership for the SOS line
framed as February 2026 in the article text (OBS-013 — month-level framing,
undated tier, no current-state weight); Sephora North America footprint doubling
from 4 to 8 shelves across ~500 doors reported 2026-04-30 with brand-attributed
$119M GMV across Amazon/Sephora/Kohl's (OBS-012 — brand-supplied, unaudited,
trailing period undefined); current hiring concentrated in brand
marketing/e-commerce/content roles (OBS-006, org motion only). No funding,
acquisition, leadership-change, NAD, FDA, recall, or lawsuit events surfaced
for 2025-2026 within search coverage (OBS-015 — absence bounded by coverage;
WWD paywall limits, GAP-009). Snippet-level trademark applications (WATERBREAK,
SCULPTINO) hint at unreleased product-name pipeline but are unverified
(OBS-014). No longitudinal question was commissioned; this chronology is
context, not a manufactured trajectory claim.

### 7. Customer And Community Response

All evidence in this section is external customer evidence — never
representative demand, sell-through, repeat purchase, internal company fact, or
buyer proof. The live customer-world shows both poles. Advocacy and acquisition:
haul and pairing threads in r/MakeupAddiction (OBS-017), a current open
brand-evaluation thread in r/beauty (OBS-019, 2026-07-02), dated eczema-relief
praise with repurchase intent from an independent reviewer (OBS-024), and
archival 2023 flare-relief language (OBS-022). Failure modes and rejection:
lipgloss/makeup separation question (OBS-016, 2026-07-04), concealer rejection
title (OBS-017, 2026-06-06), mascara rejection with switching intent (OBS-018,
2026-05-31), a verified 2024 claims-contradiction complaint on the concealer
(OBS-023), an unverified but recurring TikTok breakout/purging complaint theme
(OBS-025), and historical shade-range boundary language (OBS-021). Reception
dispersion at Sephora separates heroes (4.3-4.6 ratings) from a sub-4.0 cluster
— mascara, pressed powder, highlighter, skin tint — with the hero SOS spray
itself at 4.09 across 4,855 reviews (OBS-009; ratings are reception proxies
with explicit ceilings). The eczema need-state community discusses the brand
and its ingredient class directly (OBS-020). Value-skepticism and comparison
framing dominate creator titles (OBS-026). Decisive coverage limits: Reddit
thread bodies are unread (login-walled to the sanctioned route; CR-001), TikTok
content is unverified beyond titles (CR-002), Quora is blocked (GAP-006), and
the subreddit-graph dependency remains unsupplied (GAP-001) — no mapped
Reddit-neighborhood coverage is claimed.

### 8. Competitor Context, Contradictions, And Gaps

Bounded comparator pointers (interpreting the subject only; deep competitor
treatment requires a separately named follow-up commission): customers and
creators compare Tower 28 heroes against Saie, Kosas, NARS, Hourglass, Ciele,
Supergoop, Summer Fridays, Rhode, and Merit (OBS-026, OBS-018), while an
organized lower-price substitution ecosystem frames Prequel ($17) against SOS
($28) and NYX Bare With Me ($12) against Swipe ($24) (OBS-027); historical
community advice already steered toward cheaper hypochlorous-acid alternatives
in 2023 (OBS-022).

Named contradictions and tensions held open: (1) claims-surface divergence —
Sephora PDP copy says "non-comedogenic" while the brand's own ingredients page
avoids the word, and a verified 2024 complaint names a specific ingredient
against that retailer claim, with recurrence pointers into 2025 (OBS-023 vs
OBS-003); (2) the TikTok breakout/purging complaint theme sits against the
sensitive-skin positioning but is unverified beyond titles (OBS-025); (3)
Amazon GMV attribution versus Amazon's absence from the brand's channel list
(OBS-012 vs OBS-005, OBS-011); (4) rejection and advocacy coexist in the same
venues at similar recency (OBS-016 through OBS-019); (5) reception dispersion
between hero and secondary items (OBS-009).

Decisive gaps: internal facts — sell-through, repeat/reorder, margin,
inventory, claims-substantiation files, retailer terms — are not publicly
observable and no proxy here may substitute for them (GAP-007); Reddit thread
bodies (GAP-002/CR-001); TikTok/Instagram content (GAP-003/CR-002); Amazon US
seller state (GAP-004/CR-003); AEO visibility not run (GAP-005); Quora blocked
(GAP-006); per-review text sampling not performed (GAP-008); WWD-paywalled
dates (GAP-009); subreddit-graph dependency (GAP-001).

### 9. Company Surface Candidate Ledger

```yaml
company_surface_candidate_ledger:
  - candidate_id: CSC-001
    observation_ids: [OBS-001, OBS-005, OBS-028]
    candidate_only: true
    import_status: not_imported
    candidate_fact_class: company_fact
    bounded_fact: "As observed 2026-07-16, Tower 28 Beauty operated a live DTC storefront and listed its channel set as Sephora (US/CA/UK/ME), Sephora at Kohl's, Credo, Mecca, TikTok Shop, and Revolve, with Ulta and Amazon absent from the first-party list."
    identity_state: resolved
    time_scope: observed_current_page_at_2026-07-16
    limitations: "First-party listing; Amazon flows exist despite omission (see CSC-004 contradiction)."
  - candidate_id: CSC-002
    observation_ids: [OBS-008, OBS-004]
    candidate_only: true
    import_status: not_imported
    candidate_fact_class: company_fact
    bounded_fact: "As observed 2026-07-16, Sephora US carried 25 Tower 28 items including a seven-product SOS skincare family; DTC price architecture ran $12-$34 single items with bundles to $88."
    identity_state: resolved
    time_scope: observed_current_page_at_2026-07-16
    limitations: "Assortment and price state only; no velocity, productivity, or sell-through."
  - candidate_id: CSC-003
    observation_ids: [OBS-014]
    candidate_only: true
    import_status: not_imported
    candidate_fact_class: company_fact
    bounded_fact: "Owning legal entity resolves to Tower 28 Beauty, Inc., Los Angeles, CA (USPTO Reg. 6925089, registered 2022-12-13); no parent organization surfaced in any consulted source."
    identity_state: resolved
    time_scope: registration_effective_2022-12-13_checked_2026-07-16
    limitations: "Absence of a parent is bounded by source coverage, not proven."
  - candidate_id: CSC-004
    observation_ids: [OBS-012, OBS-005, OBS-011]
    candidate_only: true
    import_status: not_imported
    candidate_fact_class: company_fact
    bounded_fact: "A 2026-04-30 trade interview reported the Sephora NA footprint doubling (4 to 8 shelves, ~500 doors), a Sephora Middle East launch (55 doors), and brand-attributed $119M GMV across Amazon/Sephora/Kohl's, while the brand's own channel list omits Amazon."
    identity_state: resolved
    time_scope: published_2026-04-30_checked_2026-07-16
    limitations: "Figures brand-supplied and unaudited; the Amazon attribution-vs-listing contradiction is explicitly unresolved."
  - candidate_id: CSC-005
    observation_ids: [OBS-003, OBS-029]
    candidate_only: true
    import_status: not_imported
    candidate_fact_class: company_fact
    bounded_fact: "As observed 2026-07-16, the brand claimed NEA, National Rosacea Society, and National Psoriasis Foundation seals across skincare ('first and only' per brand), excluded-ingredient and third-party-testing claims, without using the word non-comedogenic on its ingredients page."
    identity_state: resolved
    time_scope: observed_current_page_at_2026-07-16
    limitations: "Seal scope and 'first and only' unverified; retailer PDP copy diverges (see CSC-006)."
  - candidate_id: CSC-006
    observation_ids: [OBS-023, OBS-009]
    candidate_only: true
    import_status: not_imported
    candidate_fact_class: external_customer_evidence
    bounded_fact: "A verified 2024-04-25 customer complaint asserted the Swipe concealer broke them out and named Polyglyceryl-3 Diisostearate against retailer 'non-comedogenic' copy, with related concealer threads recurring into 2025; Sephora reception dispersion separates heroes (4.3-4.6) from a sub-4.0 cluster including the mascara, pressed powder, highlighter, and skin tint."
    identity_state: resolved
    time_scope: complaint_2024-04-25_ratings_observed_2026-07-16
    limitations: "External customer evidence only — not a complaint rate, not representative demand, not internal fact; comedogenicity assertion is the customer's."
  - candidate_id: CSC-007
    observation_ids: [OBS-007]
    candidate_only: true
    import_status: not_imported
    candidate_fact_class: company_fact
    bounded_fact: "Tower 28 entered the sunscreen category (SOS FaceGuard SPF 30) in the 2025-05 window per its own dated blog post."
    identity_state: resolved
    time_scope: published_2025-05-12
    limitations: "Exact launch effective dates unverified (paywalled trade coverage)."
```

### 10. Completion Ledger And Run Boundary

```yaml
completion_ledger:
  coverage_status: complete_with_typed_gap
  observation_status: traceable
  candidate_status: candidate_only_not_imported
  completeness_policy: necessary_complete_no_arbitrary_caps
  hidden_venue_discovery: category_aware
  reddit_scout_status: checked_positive_yield
  quora_scout_status: blocked_with_typed_gap
  customer_community_boundary: external_evidence_not_representative_demand_or_internal_fact
  deep_competitor_treatment: separate_named_follow_up_required
  classifier_handoff: omitted
  required_lens_coverage:
    positioning: {status: complete, observation_ids: [OBS-001, OBS-002, OBS-003], rationale: "first-party positioning and claims architecture verified current"}
    offerings_and_claims: {status: complete, observation_ids: [OBS-003, OBS-004, OBS-008, OBS-007], rationale: "catalog, price, availability, claim versions, and SPF category entry dated"}
    markets_and_channels: {status: complete, observation_ids: [OBS-005, OBS-008, OBS-010, OBS-011, OBS-012, OBS-028], rationale: "channel set, Sephora concentration, Ulta absence, Amazon ambiguity typed"}
    strategic_and_operating_moves: {status: complete, observation_ids: [OBS-006, OBS-007, OBS-012, OBS-013, OBS-014, OBS-015], rationale: "dated chronology with observation/effective time separated"}
    customer_and_community_response: {status: gap, observation_ids: [OBS-016, OBS-017, OBS-018, OBS-019, OBS-020, OBS-021, OBS-022, OBS-023, OBS-024, OBS-025, OBS-009], rationale: "both poles captured with dates, but the lens is title-level and aggregate-level only — per-review text unsampled (GAP-008), thread bodies unread (GAP-002), TikTok content undated (GAP-003); adequate for company understanding, not for reception-dependent GTM interpretation"}
    competitor_and_substitute_context: {status: complete, observation_ids: [OBS-026, OBS-027, OBS-022], rationale: "bounded comparator pointers only"}
    contradictions: {status: complete, observation_ids: [OBS-023, OBS-025, OBS-005, OBS-009], rationale: "five named contradictions held open in Section 8"}
    evidence_gaps: {status: complete, observation_ids: [], rationale: "nine typed gaps below"}
  gaps:
    - gap_id: GAP-001
      gap_type: dependency_pending
      status: open
      description: "Subreddit-graph lane output not supplied; bounded exact-thread scouting only; no mapped Reddit-neighborhood coverage claimed."
      affected_coverage_ids: [COV-004]
      request_ids: []
    - gap_id: GAP-002
      gap_type: access
      status: open
      description: "Reddit thread bodies login-walled to the sanctioned screening route; title-level evidence only."
      affected_coverage_ids: [COV-004]
      request_ids: [REQ-001]
    - gap_id: GAP-003
      gap_type: access
      status: open
      description: "TikTok/Instagram live reads not authorized in this lane; complaint-theme evidence is title-level."
      affected_coverage_ids: [COV-012, COV-013]
      request_ids: [REQ-002]
    - gap_id: GAP-004
      gap_type: coverage
      status: open
      description: "Amazon US seller/storefront state unobservable from SG vantage; brand channel list omits Amazon while brand-attributed GMV includes it."
      affected_coverage_ids: [COV-009]
      request_ids: [REQ-003]
    - gap_id: GAP-005
      gap_type: coverage
      status: open
      description: "AEO answer-engine visibility annotation not run (conditional row)."
      affected_coverage_ids: [COV-016]
      request_ids: [REQ-004]
    - gap_id: GAP-006
      gap_type: access
      status: open
      description: "Quora search login-walled and zero search-index presence; experimental scout blocked."
      affected_coverage_ids: [COV-005]
      request_ids: []
    - gap_id: GAP-007
      gap_type: access_boundary
      status: open
      description: "Internal facts (sell-through, repeat/reorder, margin, inventory, claims files, terms, intent) are not publicly observable; any later claim they control must hold, not proxy."
      affected_coverage_ids: []
      request_ids: []
    - gap_id: GAP-008
      gap_type: coverage
      status: open
      description: "Per-review text sampling on Sephora PDPs not performed; reception evidence is aggregate-level."
      affected_coverage_ids: [COV-007]
      request_ids: [REQ-004]
    - gap_id: GAP-009
      gap_type: access
      status: open
      description: "WWD articles paywalled (Tollbit 402); several launch/expansion effective dates remain snippet-level."
      affected_coverage_ids: [COV-017]
      request_ids: []
  requests:
    - request_id: REQ-001
      request_type: capture_preservation
      owner: capture
      status: requested
      description: "Preserve shortlisted Reddit thread bodies (scan CR-001) under Capture's own route authority."
      source_surface: old.reddit thread pages
    - request_id: REQ-002
      request_type: capture_preservation
      owner: capture
      status: requested
      description: "Lawful verification of TikTok complaint-theme content (scan CR-002)."
      source_surface: tiktok_topic_pages
    - request_id: REQ-003
      request_type: capture_acquisition
      owner: capture
      status: requested
      description: "US-vantage Amazon seller-of-record and storefront state (scan CR-003)."
      source_surface: amazon_us_search_and_pdp
    - request_id: REQ-004
      request_type: bounded_scan_extension
      owner: scanning
      status: requested
      description: "If commissioned: AEO visibility annotation pass and bounded per-review text sampling on hero/sub-4.0 Sephora PDPs."
      source_surface: answer_engines_and_sephora_pdp_reviews
  run_boundary: COMPANY_REPORT_COMPLETE_NO_DOWNSTREAM_EXECUTION
  next_authorized_step: "Apply the Phase 1 gate; if it clears, run the Phase 2 GTM adjudication citing these observation ids; typed requests execute only under their own lane authority."
```

## Customer-World Venue Map

Venue-map fields per the commission (participants, visible behavior, relevance,
recency quality, independence risk, access, what the venue can and cannot
establish, next route):

| Venue / route | Participants | Behavior visible | Tower 28 relevance | Recency quality | Independence / seeding risk | Access + capture state | Can establish / cannot establish | Next route |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r/MakeupAddiction (old.reddit sub-search) | general makeup buyers | choice, pairing, hauls, failure-mode questions | high — dated Tower-28-titled threads incl. hero products | high (weekly fresh threads to 2026-07-15) | organic-appearing; seeding possible, undetectable at title level | listings readable via sanctioned route; bodies login-walled (CR-001) | can: dated buyer questions/complaint titles; cannot: sentiment rates, outcomes, demand | capture thread bodies |
| r/Sephora | Sephora shoppers | rejection, switching, comparison, points/haul economics | high | high | organic-appearing | same as above | can: switching intent titles; cannot: rates | capture bodies |
| r/beauty | broad consumers | brand evaluation, shade-range asks | medium-high | high | organic-appearing | same | same | capture bodies |
| r/eczema | need-state population (brand's core claim audience) | ingredient-class troubleshooting, product asks | high for SOS line | medium-high | organic-appearing | same | can: need-state venue relevance; cannot: efficacy or demand | capture bodies |
| r/SkincareAddiction (old.reddit.com/r/SkincareAddiction/search?q=Tower%2028&restrict_sr=on) | skincare-focused | Tower 28 appears in comments, not titles | low direct at title level | listings current | organic-appearing | same as Reddit rows above | little at title level | only if bodies captured |
| r/30PlusSkinCare (old.reddit.com/r/30PlusSkinCare/search?q=Tower%2028&restrict_sr=on) | 30+ skincare-focused | generic titles only; no Tower-28-titled threads in the window | low | listings current | organic-appearing | same as Reddit rows above | little at title level | close branch unless bodies captured |
| Sephora Beauty Insider Community | Sephora customers | troubleshooting, praise, complaints 2023-2025 | high historical | archival — forum read-only | platform sells the brand (moderate dependence) | browser-readable | can: verified dated historical language incl. claims contradiction; cannot: current conversation | treat as archive |
| Sephora ratings/reviews (PDP aggregate) | verified-ish purchasers | aggregate reception | high | current | platform conventions; incentivized reviews possible | brand-page state read; per-review text not sampled (GAP-008) | can: dispersion context; cannot: sell-through, complaint rate | bounded review-text sampling (REQ-004) |
| TikTok topic pages | trend-driven beauty audience | breakout/purging complaint themes, comparisons | high (theme level) | current indexing; content undated | high gifting/sponsorship risk both directions | not authorized in-lane; titles only (CR-002) | can: theme existence; cannot: volume, dates, authenticity | capture under TikTok posture |
| YouTube | review/comparison creators | vs-brand comparisons, value skepticism | medium-high | mostly 2025 (snippet-dated) | sponsorship state unverifiable | screen-light, no login | can: comparison-set names; cannot: dates, disclosure, content | targeted verified reads if needed |
| Instagram | brand + creator audiences | unknown | unknown | unknown | high | not authorized in-lane | nothing this pass | capture lane if needed |
| Quora | Q&A audience | unknown | unknown | unknown | unknown | login-walled + zero index (GAP-006) | nothing | drop unless a route appears |
| Dupe aggregators — per-venue routes: skinsort.com/products/tower-28-beauty/dupes; brandefyskin.com/blogs/beauty/tower-28-sos-dupe; skinskoolbeauty.com/dupes/tower-28/…; beautymasterlist.com/products/tower-28/…; temptalia.com/makeup-dupe-list/tower-28-… | price/ingredient-conscious switchers | structured substitution and price comparison | high for heroes | SkinSort labeled 2026; others undated — treat per venue | SEO/affiliate motive (each venue independently monetized; not one syndication group but shared genre incentives) | SkinSort/Thingtesting 403 to fetchers; Brandefy open; Temptalia open | can: named substitute set, price gaps; cannot: switching volume | monitor not authorized; reread per venue on demand |
| Thingtesting | DTC early adopters | repurchase-style voting | medium | unknown | self-selected testers | 403 to fetchers | unverified | capture if needed |
| Independent need-state blogs (e.g., Whimsy Soul) | eczema-population reviewers | dated first-person experience, substitution notes | high | 2026-04 dated | gifting undisclosed | open | can: dated individual experience; cannot: representativeness | discover more via need-state queries |
| Trade press (BeautyMatter, Drug Store News; WWD paywalled) | industry | distribution, launches, interviews | high | 2025-2026 dated | announcement syndication; brand-supplied figures | WWD 402 (GAP-009) | can: dated company events; cannot: audited figures | paywalled access decision is owner's |
| MakeupAlley | legacy reviewers | unknown | unknown — zero index yield | unknown | unknown | not surfaced | nothing this pass | drop unless surfaced |
| Search surfaces (exact-query walk) | public askers | question/comparison language | high as route discovery | current | n/a | open | can: language, venue discovery; cannot: demand | rerun per commission only |
| Answer engines (AEO) | answer consumers | visibility only | untested | n/a | n/a | not run (GAP-005) | nothing this pass | conditional pass (REQ-004) |

## Phase 1 Gate

Gate condition: a cold reader can trace each material company fact to source,
date, evidence class, limitation, and counterevidence (Sections 3-4 carry
this); the customer-world map is adequate for the candidate decision surfaces
this substrate exposes (map above, with typed access boundaries); no proxy is
presented as its underlying fact (proxy ceilings stated inline throughout).

Assessment: **PHASE_1_GATE_CLEARS_FOR_COMPANY_UNDERSTANDING** — the substrate
is traceable, proxy-disciplined, and adequate as decision-neutral company
understanding. It does **not** clear for reception-dependent GTM
interpretation: the customer-and-community lens is title-level and
aggregate-level only (per-review text unsampled — GAP-008; Reddit thread
bodies unread — GAP-002; TikTok content undated — GAP-003), so any Phase 2
pattern whose trigger depends on interpreting current product reception or
community-language depth must first consume CR-001/CR-002 captures or the
REQ-004 review-text sampling, or state a coverage hold. This constraint was
applied in Phase 2's adjudication (result: company understanding only, leading
candidate held as hypothesis). The subreddit-graph dependency remains open
(GAP-001); no Reddit-neighborhood coverage completeness is claimed anywhere in
this report.

Post-review note (2026-07-17): this report was corrected after adversarial
artifact review — recency anchors on three undated/month-level observations
(OBS-013, OBS-025, OBS-029) were downgraded to `undated_unknown`; the
single-retailer-concentration phrasing in Section 5 was replaced with a
bounded footprint statement; OBS-028 was retyped to its true first-party
source family; the customer-response lens was marked `gap`; and the gate
statement above was narrowed. reviewed_by: unrecorded; authored_by:
claude-fable-5.
