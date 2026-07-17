# Tower 28 Beauty — V2 Rerun Company-Intelligence CSB Commission (Upgraded Contract)

```yaml
retrieval_header_version: 1
artifact_role: Research artifact (v2 rerun CSB commission — company competitive intelligence, commission stage)
scope: >
  Sealed Commission Signal Board commission for the Tower 28 Beauty v2 rerun
  under the upgraded CSB company-profile contract (comparison-loop arm).
  Evidence base B+: reuses v1's typed observation rows and coverage results as
  the sealed evidence base and commissions fresh evidence only where the
  upgraded contract demands classes v1 never collected (substantive review
  sampling, preservation captures for conclusion-bearing rows, and the
  add-on-task observations: price ladder raw material, certification
  directories, diversion read / Amazon US seller state). Produced blind to v1
  report synthesis per the rerun commission handoff blindness rule.
use_when:
  - Executing the bounded v2 supplement acquisitions and the v2 report synthesis.
  - Tracing v2 observations back to their commissioned coverage rows or reused v1 rows.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_beauty_tower28_rerun_commission_handoff_v0.md
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - docs/research/forseti_beauty_tower28_company_intelligence_report_v1.md
stale_if:
  - The v2 report lands and the external comparison is adjudicated.
  - The owner changes the comparison design (blindness, evidence base, lens).
  - The CSB company competitive-intelligence contract or validator changes materially.
```

## Commission Stage Note

This artifact is the **commission** for the Tower 28 v2 rerun, expressed in the
CSB `company_competitive_intelligence` ten-section contract so it is
mechanically validatable before the supplement acquisitions execute. It is the
rerun arm of the ledger-bound comparison loop commissioned by
`docs/workflows/forseti_beauty_tower28_rerun_commission_handoff_v0.md` with
owner dispatch decision **evidence base B+** (reuse + targeted supplement).

- **Reused evidence base:** the v1 typed observation rows (OBS-001 through
  OBS-029, carried verbatim in Section 4 below) and the v1 coverage results
  (COV-001 through COV-020, carried with their earned statuses and original
  read dates). Evidence rows are evidence; their v1 observation dates are
  preserved and no claim inherits recency it did not earn.
- **Commissioned supplements (the `not_checked` rows):** COV-021 substantive
  Sephora per-review text sampling (closes v1 GAP-008 for the upgraded
  contract's Section 7 six-field classification rows and chain cards); COV-022
  Amazon US seller/storefront state with US delivery pin plus diversion read
  (fulfills v1 REQ-003/CR-003 and the diversion add-on task); COV-023
  certification-directory verification (NEA / NRS / NPF seal directories —
  certifier-side check of the brand's seal claims); COV-024 preservation
  captures of conclusion-bearing brand pages (CR mechanism) plus price-ladder
  raw material from current catalog price state.
- **Blindness rule (binding on this lane):** this lane loads the upgraded
  contract files, raw evidence rows (v1 typed observation/scan ledger rows,
  capture receipts, retailer-probe observations), and nothing of v1's report
  synthesis: Sections 5-8 narrative, Section 9 company surface candidates,
  the Executive-brief-equivalent conclusions, the external assessments of v1,
  and `docs/decisions/forseti_ci_report_external_review_adjudication_ledger_v0.md`
  are not loaded. The upgraded contract alone drives the v2 synthesis.
- **Comparison neutrality:** "beat v1" is not a synthesis instruction; the
  lane simply runs the upgraded contract against the evidence base.

## Recency Contract

`time_posture: recency_first` with the deterministic ladder anchored to
`as_of_date: 2026-07-18`. Reused v1 rows keep their original observation dates
(2026-07-16/17) and tier accordingly; supplement observations carry their own
capture dates. Freshness is not proof; no claim inherits recency it did not
earn.

### 1. Company Commission And Identity Receipt

```yaml
company_commission_receipt:
  commission_id: tower28_ci_v2_rerun_2026_07_18
  mode: forward
  commission_profile: company_competitive_intelligence
  subject_count: 1
  subject_identity:
    raw_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
  as_of_date: "2026-07-18"
  time_posture: recency_first
  longitudinal_period: null
  longitudinal_rationale: not_applicable
  initial_proving_run: false
```

### 2. Decision-Neutral Boundary

This commission and the v2 run it binds are decision-aware but
decision-neutral. Permitted lenses are the adjudicated information-priority
families (customer choice/product failure, demand durability, retail/channel
productivity, versioned claims, economics and concentration, execution
capacity, and constraints), applied strictly as observable substrate. One
company at a time: Tower 28 Beauty is the only subject; named alternatives
enter only as bounded comparator pointers that interpret the subject; deep
competitor treatment requires a separately named follow-up commission. The v2
report may expose candidate decision surfaces but assigns no pain, buyer, ICP,
urgency, willingness to pay, outreach, offer, or wedge value and reaches no
demand conclusion. Community evidence is external customer evidence only —
never representative demand, sell-through, repeat purchase, internal company
fact, or buyer proof.

### 3. Source-Family And Venue Coverage Ledger

Rows COV-001 through COV-020 are the reused v1 coverage results, carried with
their earned statuses and original read dates (evidence base B+). Rows COV-021
through COV-024 are the commissioned v2 supplement routes.

```yaml
coverage_ledger:
  - coverage_id: COV-001
    source_family: owned_channels
    source_surface: brand_site
    venue: tower28beauty.com (home, about, stores pages)
    relevance_rationale: "Reused v1 result: first-party positioning, identity, and channel-set statements."
    route_or_query: https://www.tower28beauty.com/
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16_reused_v1
    access: public_web_intermittent_503_then_ok
    relevance: relevant
    gap_id: null
  - coverage_id: COV-002
    source_family: retail_pdp
    source_surface: retailer_search
    venue: Sephora search
    relevance_rationale: "Reused v1 result: carriage corroboration from the selection run."
    route_or_query: https://www.sephora.com/search?keyword=Tower+28+Beauty
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16_reused_v1
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-003
    source_family: retail_pdp
    source_surface: retailer_search
    venue: Revolve
    relevance_rationale: "Reused v1 result: second observed US retail partner."
    route_or_query: https://www.revolve.com/r/Search.jsp?search=Tower+28+Beauty
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16_reused_v1
    access: public_web_selection_run_observation_direct_reread_bot_blocked
    relevance: relevant
    gap_id: null
  - coverage_id: COV-004
    source_family: forums_community
    source_surface: bounded_subreddit_scout
    venue: Reddit
    relevance_rationale: "Reused v1 result: mandatory bounded customer-world scout (old.reddit subreddit-restricted searches via the sanctioned screening route) across r/MakeupAddiction, r/SkincareAddiction, r/Sephora, r/beauty, r/30PlusSkinCare, r/eczema."
    route_or_query: old.reddit.com/r/<sub>/search?q=Tower%2028&restrict_sr=on&sort=new&t=year
    requirement: mandatory_bounded_scout
    status: checked
    yield: evidence_found
    recency: listings_current_to_2026-07-17_reused_v1
    access: listings_public_thread_bodies_login_walled
    relevance: relevant
    gap_id: GAP-002
  - coverage_id: COV-005
    source_family: forums_community
    source_surface: answer_forum_scout
    venue: Quora
    relevance_rationale: "Reused v1 result: experimental scout for the v1 initial proving run; blocked by login wall plus zero search-index presence. Not re-attempted: no named non-dominated decision-material job for the rerun."
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
    relevance_rationale: "Reused v1 result: category-aware hidden-venue discovery from need-state cues."
    route_or_query: discovered via EQ-012, EQ-013, EQ-018 (see v1 scan)
    requirement: category_aware
    status: checked
    yield: evidence_found
    recency: mixed_2023_to_2026_reused_v1
    access: BIC_browser_readable_thingtesting_403_makeupalley_zero_index
    relevance: relevant
    gap_id: null
  - coverage_id: COV-007
    source_family: reviews
    source_surface: retailer_reviews_state
    venue: Sephora ratings and review counts (brand-page level)
    relevance_rationale: "Reused v1 result: reception dispersion and volume context across the line; per-review text sampling commissioned separately at COV-021."
    route_or_query: https://www.sephora.com/brand/tower-28
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16_reused_v1
    access: public_web_browser
    relevance: relevant
    gap_id: GAP-008
  - coverage_id: COV-008
    source_family: reviews
    source_surface: retailer_reviews_and_qa
    venue: Ulta
    relevance_rationale: "Reused v1 result: bounded no-carriage-observed outcome via first-party list and retailer-expansion search; direct site read bot-blocked."
    route_or_query: brand stores page plus retailer-expansion web search (v1 EQ-015)
    requirement: conditional
    status: checked
    yield: zero_yield
    recency: current_as_of_2026-07-16_reused_v1
    access: direct_site_read_bot_blocked_no_carriage_observed_via_first_party_list_and_search
    relevance: relevant
    gap_id: null
  - coverage_id: COV-009
    source_family: retail_pdp
    source_surface: marketplace_presence
    venue: Amazon
    relevance_rationale: "Reused v1 result: SG-vantage read only; US seller/storefront state commissioned separately at COV-022."
    route_or_query: amazon search from SG vantage (geo-redirected)
    requirement: conditional
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-17_reused_v1
    access: US_vantage_unavailable_geo_redirect_to_amazon_sg
    relevance: relevant
    gap_id: GAP-004
  - coverage_id: COV-010
    source_family: retail_pdp
    source_surface: retailer_brand_page_state
    venue: Sephora Tower 28 brand page
    relevance_rationale: "Reused v1 result: current assortment, price, and reception state."
    route_or_query: https://www.sephora.com/brand/tower-28
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16_reused_v1
    access: public_web_browser
    relevance: relevant
    gap_id: null
  - coverage_id: COV-011
    source_family: owned_channels
    source_surface: brand_pdp_claims_price
    venue: tower28beauty.com collections and ingredients pages
    relevance_rationale: "Reused v1 result: exact current product, price, promotion, availability, and claim versions; preservation re-read commissioned at COV-024."
    route_or_query: tower28beauty.com/collections/* and /pages/ingredients
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16_reused_v1
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-012
    source_family: creator_social_video
    source_surface: tiktok_public
    venue: TikTok
    relevance_rationale: "Reused v1 result: complaint-theme and comparison content indexed by search engines; live reads not authorized in this lane."
    route_or_query: search-indexed titles/URLs only; live reads not authorized in this lane
    requirement: conditional
    status: blocked
    yield: blocked
    recency: index_current_2026_reused_v1
    access: not_separately_authorized
    relevance: relevant
    gap_id: GAP-003
  - coverage_id: COV-013
    source_family: creator_social_video
    source_surface: instagram_public
    venue: Instagram
    relevance_rationale: "Reused v1 result: brand and creator surfaces; live reads not authorized in this lane."
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
    relevance_rationale: "Reused v1 result: comparison/review genre density and framing (screen-light, no login)."
    route_or_query: YouTube search and video pages (screen-light, no login)
    requirement: conditional
    status: checked
    yield: evidence_found
    recency: snippet_dated_2025_estimates_unverified_reused_v1
    access: JS_pages_limit_metadata_verification
    relevance: relevant
    gap_id: null
  - coverage_id: COV-015
    source_family: search_discovery
    source_surface: search_surface_mgt
    venue: public search surfaces
    relevance_rationale: "Reused v1 result: market language, comparison pairs, hidden venues, counterevidence queries."
    route_or_query: EQ-010 through EQ-020 (see v1 scan exact-query ledger)
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_2026-07-16_reused_v1
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-016
    source_family: aeo_answer_engines
    source_surface: answer_visibility
    venue: answer engines
    relevance_rationale: "Reused v1 result: visibility annotation not run (conditional row); not commissioned for the v2 supplement set — no named non-dominated decision-material job; remains a typed gap."
    route_or_query: not run
    requirement: conditional
    status: not_applicable
    yield: not_applicable
    recency: not_applicable
    access: not_attempted
    relevance: unknown
    gap_id: GAP-005
  - coverage_id: COV-017
    source_family: news_editorial_trade
    source_surface: trade_press
    venue: BeautyMatter, Drug Store News, Cosmetics Business; WWD paywalled
    relevance_rationale: "Reused v1 result: dated chronology for distribution, launches, leadership, ownership."
    route_or_query: targeted trade searches (see v1 scan EQ-016, EQ-017, EQ-020)
    requirement: required
    status: checked
    yield: evidence_found
    recency: items_dated_2025-05_to_2026-05_reused_v1
    access: wwd_tollbit_402_paywall_others_open
    relevance: relevant
    gap_id: GAP-009
  - coverage_id: COV-018
    source_family: professional_org_motion
    source_surface: careers_ats_and_leadership
    venue: tower28beauty.com/pages/careers-new
    relevance_rationale: "Reused v1 result: hiring posture and role ownership signals (org motion only)."
    route_or_query: https://www.tower28beauty.com/pages/careers-new
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16_reused_v1
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-019
    source_family: owned_channels
    source_surface: press_and_announcements
    venue: tower28beauty.com blog; no dedicated press page exists
    relevance_rationale: "Reused v1 result: official chronology with stated dates."
    route_or_query: https://www.tower28beauty.com/blogs/sensitive-content
    requirement: required
    status: checked
    yield: evidence_found
    recency: posts_dated_2019_to_2025-05_reused_v1
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-020
    source_family: professional_org_motion
    source_surface: registries_and_filings
    venue: USPTO (via aggregators)
    relevance_rationale: "Reused v1 result: owning-entity resolution and mark portfolio."
    route_or_query: trademark registry searches
    requirement: conditional
    status: checked
    yield: evidence_found
    recency: registrations_2022_and_2024_reused_v1
    access: trademarkelite_open_uspto_report_403
    relevance: relevant
    gap_id: null
  - coverage_id: COV-021
    source_family: reviews
    source_surface: retailer_pdp_review_text
    venue: Sephora Tower 28 hero and sub-4.0 PDPs (Swipe, SOS spray, ShineOn, SunnyDays, MakeWaves)
    relevance_rationale: "Commissioned v2 supplement: substantive per-review text sampling (stars, dates, bodies, verified/incentivized markers, sort order as selection route) required by the upgraded contract's Section 7 six-field classification rows and chain cards; closes the class v1 never collected (GAP-008). Could change the rival assessment of each hero claim by replacing aggregate-star proxies with claim-referenced complaint evidence."
    route_or_query: Sephora PDP review widgets via the Capture spine CloakBrowser runner (canonical Sephora route)
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web_expected
    relevance: relevant
    gap_id: null
  - coverage_id: COV-022
    source_family: retail_pdp
    source_surface: marketplace_seller_state
    venue: Amazon US (search plus two PDPs, US delivery pin)
    relevance_rationale: "Commissioned v2 supplement: US-vantage Amazon seller-of-record and storefront state (fulfills v1 REQ-003/CR-003) plus the diversion add-on read against the brand's authorized-seller list. Could change the channel-control and diversion assessment that v1 could only hold as a contradiction."
    route_or_query: amazon.com search "Tower 28 Beauty" and two PDPs via Capture spine runner with declared US delivery ZIP
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web_expected_geo_pin_uncertain
    relevance: relevant
    gap_id: null
  - coverage_id: COV-023
    source_family: other
    source_surface: certification_directories
    venue: National Eczema Association, National Rosacea Society, National Psoriasis Foundation public seal/product directories
    relevance_rationale: "Commissioned v2 supplement (add-on task): certifier-side verification of the brand's seal claims ('first and only brand' with NEA/NRS/NPF seals). Could change the versioned-claims assessment: directory presence/absence is checkable counter-evidence to a load-bearing claim."
    route_or_query: nationaleczema.org/eczema-products/, rosacea.org seal-of-acceptance directory, psoriasis.org seal-of-recognition directory
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web_expected
    relevance: relevant
    gap_id: null
  - coverage_id: COV-024
    source_family: owned_channels
    source_surface: preservation_captures_and_price_state
    venue: tower28beauty.com stores, ingredients, and collections pages
    relevance_rationale: "Commissioned v2 supplement: preservation captures (CR mechanism) of conclusion-bearing, disputable, or likely-to-disappear pages — channel list with anti-diversion language, claims architecture, current catalog price state (price-ladder add-on raw material). Anchors the diversion read and claim-version conclusions to preserved packets."
    route_or_query: Capture spine runner preservation captures to the canonical lake
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web_expected
    relevance: relevant
    gap_id: null
```

### 4. Observation Ledger

The rows below are the reused v1 typed observation rows (evidence base B+),
carried verbatim from `docs/research/forseti_beauty_tower28_company_intelligence_report_v1.md`
Section 4 with their original observation dates. Supplement observations from
COV-021 through COV-024 land in the v2 report's observation ledger, not here.

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
    ambiguity_limitation: "leadership continuity corroborated only by absence of contrary press (OBS-015)"
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
    evidence_excerpt: "Sephora US carries 25 Tower 28 items including a seven-product SOS skincare family (spray $12-$68 with jumbo refill, moisturizer, cleanser, serum $34, lip balm, body wash, FaceGuard SPF $18-$32) alongside makeup heroes (Swipe $24, ShineOn $16, BeachPlease $20, MakeWaves $12-$20)."
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
    evidence_excerpt: "Indexed topic-page titles: 'Tower 28 Spray Broke Me Out', 'Does Tower 28 Spray Cause Purging', 'Tower 28 Concealer Made Me Breakout' — a breakout/purging complaint theme repeated across multiple indexed topic titles, set against the sensitive-skin positioning."
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
    publisher_or_venue: Tower 28 Beauty stores page (bounded Ulta carriage check)
    source_class: official_first_party
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-16"
    age_anchor_basis: current_page_observation
    exact_locator: "brand stores page (Ulta omitted) plus EQ-015 retailer-expansion search"
    evidence_excerpt: "No Ulta carriage surfaced in the bounded checks: the brand's own channel list omits Ulta and the retailer-expansion search did not name it. US specialty-retail exposure observed in this pass concentrates in the Sephora ecosystem."
    lawful_access_route: public_web
    access_limitation: "direct ulta.com read was bot-blocked; this is a bounded no-carriage-observed result, not proof of non-carriage"
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

Commission-stage narrative only; the v2 synthesis is commissioned to the v2
report under the upgraded contract. The reused substrate already carries
current first-party positioning and claims architecture (OBS-001, OBS-002,
OBS-003), catalog and price state (OBS-004), the brand-listed channel set with
Ulta and Amazon absent (OBS-005, OBS-028), Sephora assortment state (OBS-008),
Revolve and Amazon-International carriage reads (OBS-010, OBS-011), and the
trade-press expansion account with brand-attributed GMV (OBS-012). No v2
positioning conclusion is stated at commission stage; visible-concentration
synthesis is deferred to the report after the COV-021 through COV-024
supplements land.

### 6. Strategic And Operating Chronology

Commission-stage narrative only. The reused substrate carries dated chronology
raw material: the SPF category entry window (OBS-007), the Sephora footprint
expansion account (OBS-012), the Pvolve partnership item with its undated
limitation (OBS-013), trademark registrations (OBS-014), the negative search
bundle for funding/leadership/regulatory events (OBS-015), and hiring posture
(OBS-006). Under `time_posture: recency_first` no longitudinal question is
manufactured. Chronology synthesis with invalidation conditions is deferred to
the v2 report.

### 7. Customer And Community Response

Commission-stage narrative only. The reused substrate carries aggregate
reception dispersion (OBS-009), dated title-level community threads across
need-state venues (OBS-016 through OBS-021), verified archival community
language (OBS-022, OBS-023), an independent eczema-reviewer account (OBS-024),
the indexed TikTok complaint-theme titles (OBS-025), and the YouTube
comparison genre (OBS-026). The upgraded contract's substantive
review-classification rows and per-hero choice-mechanism chain cards require
per-review text that v1 never collected; that class is commissioned at
COV-021 and lands in the v2 report's Section 7. All community evidence remains
external customer evidence — never representative demand or internal company
fact.

### 8. Competitor Context, Contradictions, And Gaps

Commission-stage narrative only. The reused substrate carries the dupe/
substitution ecosystem read (OBS-027), the YouTube comparison genre (OBS-026),
and archival substitution language (OBS-022). Open contradictions carried in
the reused rows include the Amazon channel-listing-versus-GMV-attribution
ambiguity (OBS-005 vs OBS-012, commissioned to COV-022), the retailer-PDP-copy
versus customer-experience versus brand-wording divergence (OBS-003 vs
OBS-023), and the indexed complaint-theme versus sensitive-skin positioning
tension (OBS-025). These stay open at commission stage; the v2 report
adjudicates none of them beyond what the evidence bounds. Deep competitor
treatment requires a separately named follow-up commission.

### 9. Company Surface Candidate Ledger

```yaml
company_surface_candidate_ledger:
  - candidate_id: CSC-001
    observation_ids: [OBS-001, OBS-004]
    candidate_only: true
    import_status: not_imported
    candidate_fact_class: company_fact
    bounded_fact: Tower 28 Beauty operated a live first-party DTC storefront with a current makeup and SOS-skincare catalog at observed prices on 2026-07-16.
    identity_state: resolved
    time_scope: observed_current_page_at_2026-07-16
    limitations: Point-in-time page state; no Company Surface import; per-shade availability volatile.
  - candidate_id: CSC-002
    observation_ids: [OBS-005, OBS-008, OBS-010, OBS-028]
    candidate_only: true
    import_status: not_imported
    candidate_fact_class: company_fact
    bounded_fact: The brand-listed channel set on 2026-07-16 comprised DTC, the Sephora ecosystem (US/CA/UK/ME plus Sephora at Kohl's), Credo, Mecca, TikTok Shop, and Revolve, with Ulta and Amazon absent from the brand's own list while Sephora carried 25 items.
    identity_state: resolved
    time_scope: observed_current_page_at_2026-07-16
    limitations: Channel-list and assortment page state only; not velocity, terms, or dated distribution events; no Company Surface import.
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
  reddit_scout_status: checked_positive_yield
  quora_scout_status: blocked_with_typed_gap
  commission_stage_note: >
    This artifact is the sealed pre-scan v2 rerun commission (evidence base
    B+). Rows COV-001 through COV-020 carry v1's earned results and reused
    observation rows; rows COV-021 through COV-024 are the commissioned v2
    supplement acquisitions. The Reddit and Quora scout statuses carry the v1
    earned values because their evidence is reused, not re-scouted; the v2
    report keeps or updates them only with evidence actually earned.
  customer_community_boundary: external_evidence_not_representative_demand_or_internal_fact
  deep_competitor_treatment: separate_named_follow_up_required
  classifier_handoff: omitted
  required_lens_coverage:
    positioning: {status: complete, observation_ids: [OBS-001, OBS-002, OBS-003], rationale: "reused v1 substrate current as of 2026-07-16; re-anchored by COV-024 preservation captures"}
    offerings_and_claims: {status: complete, observation_ids: [OBS-003, OBS-004, OBS-008, OBS-007], rationale: "reused v1 substrate; claim-version verification deepened by COV-023 certification directories and COV-024 preservation"}
    markets_and_channels: {status: complete, observation_ids: [OBS-005, OBS-008, OBS-010, OBS-011, OBS-012, OBS-028], rationale: "reused v1 substrate; Amazon US seller state and diversion read commissioned at COV-022"}
    strategic_and_operating_moves: {status: complete, observation_ids: [OBS-006, OBS-007, OBS-012, OBS-013, OBS-014, OBS-015], rationale: "reused v1 dated chronology with observation/effective time separated"}
    customer_and_community_response: {status: gap, observation_ids: [OBS-009, OBS-016, OBS-017, OBS-018, OBS-019, OBS-020, OBS-021, OBS-022, OBS-023, OBS-024, OBS-025], rationale: "reused substrate is title-level and aggregate-level; substantive per-review text commissioned at COV-021 (GAP-008); thread bodies remain unread (GAP-002); TikTok content undated (GAP-003)"}
    competitor_and_substitute_context: {status: complete, observation_ids: [OBS-026, OBS-027, OBS-022], rationale: "bounded comparator pointers only"}
    contradictions: {status: complete, observation_ids: [OBS-023, OBS-025, OBS-005, OBS-009], rationale: "reused contradictions held open; Amazon ambiguity commissioned to COV-022"}
    evidence_gaps: {status: complete, observation_ids: [], rationale: "typed gaps below"}
  gaps:
    - gap_id: GAP-001
      gap_type: dependency_pending
      status: open
      description: "Subreddit-graph lane output not supplied; bounded exact-thread scouting only; no mapped Reddit-neighborhood coverage claimed (reused v1 gap)."
      affected_coverage_ids: [COV-004]
      request_ids: []
    - gap_id: GAP-002
      gap_type: access
      status: open
      description: "Reddit thread bodies login-walled to the sanctioned screening route; title-level evidence only (reused v1 gap; body preservation remains a Capture-owned request outside the B+ supplement classes)."
      affected_coverage_ids: [COV-004]
      request_ids: []
    - gap_id: GAP-003
      gap_type: access
      status: open
      description: "TikTok/Instagram live reads not authorized in this lane; complaint-theme evidence is title-level (reused v1 gap)."
      affected_coverage_ids: [COV-012, COV-013]
      request_ids: []
    - gap_id: GAP-004
      gap_type: coverage
      status: open
      description: "Amazon US seller/storefront state unobservable from SG vantage in v1; commissioned for v2 at COV-022 (REQ-002 below)."
      affected_coverage_ids: [COV-009]
      request_ids: [REQ-002]
    - gap_id: GAP-005
      gap_type: coverage
      status: open
      description: "AEO answer-engine visibility annotation not run (conditional row, not commissioned for v2; no named non-dominated decision-material job)."
      affected_coverage_ids: [COV-016]
      request_ids: []
    - gap_id: GAP-006
      gap_type: access
      status: open
      description: "Quora search login-walled and zero search-index presence; experimental scout blocked (reused v1 result, not re-attempted)."
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
      description: "Per-review text sampling on Sephora PDPs not performed in v1; commissioned for v2 at COV-021 (REQ-001 below)."
      affected_coverage_ids: [COV-007, COV-021]
      request_ids: [REQ-001]
    - gap_id: GAP-009
      gap_type: access
      status: open
      description: "WWD articles paywalled (Tollbit 402); several launch/expansion effective dates remain snippet-level (reused v1 gap)."
      affected_coverage_ids: [COV-017]
      request_ids: []
  requests:
    - request_id: REQ-001
      request_type: capture_acquisition
      owner: capture
      status: requested
      description: "Substantive per-review text sampling on the five commissioned Sephora Tower 28 PDPs (stars, dates, bodies, markers, sort order as selection route), via the canonical Sephora CloakBrowser route, packets to the canonical lake."
      source_surface: sephora_pdp_review_widgets
    - request_id: REQ-002
      request_type: capture_acquisition
      owner: capture
      status: requested
      description: "Amazon US search and two PDP captures with declared US delivery ZIP; record seller-of-record, storefront linkage, price, and rating states; typed gap if the US pin fails."
      source_surface: amazon_us_search_and_pdp
    - request_id: REQ-003
      request_type: capture_acquisition
      owner: capture
      status: requested
      description: "Certifier-side directory reads for NEA, NRS, and NPF seal/product directories recording Tower 28 presence or absence with route, date, and query."
      source_surface: certification_directories
    - request_id: REQ-004
      request_type: capture_preservation
      owner: capture
      status: requested
      description: "Preservation captures of conclusion-bearing brand pages (stores/anti-diversion language, ingredients/claims architecture, collections/price state) to the canonical lake under the CR trigger rule."
      source_surface: tower28beauty_com_pages
  run_boundary: COMMISSION_SEALED_PRE_SCAN
  next_authorized_step: "Execute REQ-001 through REQ-004 under Capture authority at human rate; then synthesize the v2 report under the upgraded contract with the delta declaration, validate it, and assemble the v2 bundle for the owner's same-lens external comparison."
```
