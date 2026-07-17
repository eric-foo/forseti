# Tower 28 Beauty — Phase 1 Company-Intelligence CSB Commission v1

```yaml
retrieval_header_version: 1
artifact_role: Research artifact (Phase 1 CSB commission — company competitive intelligence, commission stage)
scope: >
  Sealed Commission Signal Board commission for the restarted Tower 28 Beauty
  two-phase lane. Binds the Phase 1 company-intelligence coverage plan,
  customer-world venue map requirements, adjudicated information priorities,
  recency contract, seed observations, and typed gaps/requests before any
  Scanning or Capture execution. Decision-aware, decision-neutral.
use_when:
  - Executing the bounded CSB-first Phase 1 Tower 28 scan.
  - Checking which venues, routes, and information families the Phase 1 scan is accountable to.
  - Tracing the provenance of Phase 1 observations back to their commissioned coverage rows.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_beauty_tower28_company_intelligence_to_gtm_handoff_v0.md
  - forseti/product/spines/commission_signal_board/prompts/forseti_commission_signal_board_prompt_structure_v0.md
  - forseti/product/spines/scanning/README.md
  - docs/decisions/forseti_company_intelligence_information_architecture_v0.md
stale_if:
  - The owner changes the two-phase company-intelligence-then-GTM sequence.
  - Tower 28 is replaced as the named first company.
  - The CSB company competitive-intelligence contract or validator changes materially.
```

## Commission Stage Note

This artifact is the **commission** for the Phase 1 Tower 28 company-intelligence
run, expressed in the CSB `company_competitive_intelligence` ten-section
contract so it is mechanically validatable before Scanning. Coverage rows with
`status: not_checked` are the commissioned scan routes. The observation ledger
carries only the seed observations already source-backed by the selection
companion (`docs/research/forseti_beauty_us_company_selection_v0.json`, row
`USBEAUTY-019`, observed 2026-07-16). All other lenses are typed gaps that the
Phase 1 scan (`docs/research/forseti_beauty_tower28_company_intelligence_scan_v1.md`)
and CI report (`docs/research/forseti_beauty_tower28_company_intelligence_report_v1.md`)
must close or hold. Authorizing packet:
`docs/workflows/forseti_beauty_tower28_company_intelligence_to_gtm_handoff_v0.md`
(transport commit `567ff854`).

## Adjudicated Information Priorities (binding lenses for the scan)

Per the accepted company-intelligence information architecture
(`docs/decisions/forseti_company_intelligence_information_architecture_v0.md`),
the scan looks for decision-relevant information families and decomposes them
into atomic facts. These are lenses, not a universal checklist:

1. **Customer choice and product failure** — what customers choose Tower 28
   for; named substitutes and switching reasons; use context, recurrent failure
   modes, complaints, rejection, and repeat behavior.
2. **Demand durability** — sell-through or its explicit absence; repeat,
   reorder interval, replenishment, returns; dependence on a hero SKU, launch
   burst, creator, promotion, retailer, geography, or founder audience.
3. **Retail and channel productivity** — distribution and assortment state;
   productive doors/SKUs, placement, velocity, replenishment, markdowns,
   returns; channel concentration, economics, terms, inventory behavior.
4. **Versioned offer, claims, and substantiation** — exact product/SKU,
   formula, ingredient, package, price, promotion, and claim versions; testing
   basis, claim changes, complaints/challenges, jurisdiction, version history.
5. **Financial economics and concentration** — revenue and margin trajectory
   where observable; contribution economics, working capital, cash need;
   customer, SKU, channel, geography, supplier, or partner concentration.
6. **Execution capacity and resilience** — leadership continuity and actual
   role ownership; forecasting, inventory, launch coordination,
   supply/manufacturing capacity, lead time, defects, contingency.
7. **Safety, regulatory, legal, and strategic constraints** — adverse events,
   affected lots/versions, severity, reporting duty, corrective action;
   litigation, regulatory status, substantiation risk, retailer response,
   commitments that constrain action.

Every material element the scan or report produces must separate: source
evidence → directly observed fact → structured measurement (if any) → proxy
relationship and proxy ceiling → analyst inference → counterevidence →
observed/published/effective dates → access, rights, and coverage limitations
→ strongest permitted claim. A proxy is never stored or presented as the
underlying fact: review volume is not sell-through; community excitement is not
repeat purchase; job postings are not execution capacity; hiring, virality,
stockout badges, or press repetition are never standalone evidence of company
pressure.

## Customer-World Venue Map Requirements (binding for the scan)

For every venue the scan touches, record: venue and exact route; participant or
need-state population; behavior visible there; Tower 28 product/version
relevance; recency and activity quality; independence, seeding, affiliate, PR,
or campaign-overlap risk; lawful access and capture status; what the venue can
and cannot establish; coverage limitations and next query or route.

Mandatory source-family treatment:

- **Reddit** — bounded exact-thread scout is mandatory; zero yield is valid.
  The separate subreddit-graphing lane output is not supplied; the graph seam
  is `DEPENDENCY_PENDING` (GAP-001). Do not duplicate the graph build and do
  not claim mapped Reddit-neighborhood coverage.
- **Retail communities** — retailer reviews, product Q&A, assortment,
  availability, price, promotion, and response behavior.
- **Creator/social** — TikTok, Instagram, YouTube, and comment surfaces only
  through currently authorized lawful routes; distinguish campaign attention
  from independent customer language.
- **Specialist/niche venues** — discovered from need-state and hidden-venue
  cues, category-aware, not a universal forum list.
- **Quora** — current experimental bounded scout; report actual yield,
  recency, access, relevance; no pre-labeling.
- **Search/answer engines** — route discovery and changing-question context
  only, never demand proof; AEO is visibility annotation only.

## Recency Contract

`time_posture: recency_first` with the deterministic ladder: 0–30 days primary
current-state; 31–90 days current corroboration; 91–180 days supporting or
recurrence; over 180 days chronology/baseline/contradiction only and never a
current-pressure carrier; undated visibly limited and never promoted to
current. Freshness is not proof of pain. The prior Tower 28 diagnostic
(`codex/beauty-tower28-decision-pressure-commission` @ `5c243e14`) may seed
routes and counterevidence only; every material fact must be refreshed.

## Scan Bounds

The Phase 1 scan is bounded, not a crawl: run the default broad-scout phase
first (miss-check the board: hidden venues, exact-query risks, decisive
negatives, access walls, obvious current-state changes), then deepen only the
routes below. Reddit exact-thread scouting stays bounded (on the order of ten
threads, chosen by relevance not volume). Preserve exact queries, venues,
negatives, access notes, dates, source dependence, and counterevidence. No
standing crawler, monitor, registry, dashboard, or new research infrastructure.
Bounded effort is search hygiene; report completeness stays
necessary-complete with typed gaps, never capped.

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
  as_of_date: "2026-07-16"
  time_posture: recency_first
  longitudinal_period: null
  longitudinal_rationale: not_applicable
  initial_proving_run: true
```

### 2. Decision-Neutral Boundary

This commission and the Phase 1 run it binds are decision-aware but
decision-neutral. Permitted lenses are the adjudicated information priorities
above, applied as observable company substrate and customer-world evidence.
One company at a time: Tower 28 Beauty is the only subject; named alternatives
enter only as bounded comparator pointers where needed to interpret Tower 28
customer substitution, price/claim context, channel overlap, or a specific
Tower 28 decision surface; deep competitor treatment requires a separately
named follow-up commission. Phase 1 may reveal candidate decision surfaces but
must not assign pain, buyer intent, urgency, priority, wedge, outreach, or
offer value; no willingness-to-pay, ICP, or demand conclusion is permitted.
Community evidence remains external customer evidence — never representative
demand, sell-through, repeat purchase, internal company fact, or buyer proof.

### 3. Source-Family And Venue Coverage Ledger

```yaml
coverage_ledger:
  - coverage_id: COV-001
    source_family: owned_channels
    source_surface: brand_site_home
    venue: tower28beauty.com
    relevance_rationale: First-party current DTC storefront, positioning, and claims surface; seed observation exists from the selection run.
    route_or_query: https://www.tower28beauty.com/
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-002
    source_family: retail_pdp
    source_surface: retailer_search
    venue: Sephora
    relevance_rationale: Named US specialty-beauty retail partner; carriage observed during the selection run.
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
    relevance_rationale: Second observed US retail partner; carriage observed during the selection run.
    route_or_query: https://www.revolve.com/r/Search.jsp?search=Tower+28+Beauty
    requirement: required
    status: checked
    yield: evidence_found
    recency: current_as_of_2026-07-16
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-004
    source_family: forums_community
    source_surface: bounded_subreddit_scout
    venue: Reddit
    relevance_rationale: Mandatory bounded customer-world scout; comparison, troubleshooting, praise, rejection, and switching language for Tower 28 products and need states.
    route_or_query: site:reddit.com "Tower 28" plus exact-thread scouting in makeup/skin-sensitivity need-state communities discovered by the scan
    requirement: mandatory_bounded_scout
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web_expected
    relevance: relevant
    gap_id: GAP-001
  - coverage_id: COV-005
    source_family: forums_community
    source_surface: answer_forum_scout
    venue: Quora
    relevance_rationale: Experimental bounded scout required for the initial proving run; report actual yield, recency, access, relevance without pre-labeling.
    route_or_query: site:quora.com "Tower 28"
    requirement: experimental_initial_proving_run
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web_expected
    relevance: unknown
    gap_id: null
  - coverage_id: COV-006
    source_family: forums_community
    source_surface: category_specialist_forum
    venue: category-aware discovery (specialist makeup, sensitive-skin, and beauty-community boards surfaced by need-state cues)
    relevance_rationale: Hidden-venue discovery for where Tower 28 customers and adjacent need-state participants actually gather; not a universal forum list.
    route_or_query: exact-query walk from customer language discovered in COV-004/COV-007/COV-015
    requirement: category_aware
    status: not_checked
    yield: unknown
    recency: unknown
    access: unknown
    relevance: unknown
    gap_id: null
  - coverage_id: COV-007
    source_family: reviews
    source_surface: retailer_reviews_and_qa
    venue: Sephora product reviews and Q&A
    relevance_rationale: Experience claims, complaints, recency, repeat-use hints, and contradiction checks on carried Tower 28 SKUs; preserve recency and source conventions, not aggregate stars.
    route_or_query: Sephora PDP review and Q&A tabs for Tower 28 SKUs found via COV-002/COV-010
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web_expected
    relevance: relevant
    gap_id: null
  - coverage_id: COV-008
    source_family: reviews
    source_surface: retailer_reviews_and_qa
    venue: Ulta (carriage unconfirmed)
    relevance_rationale: Ulta carriage state is itself a channel fact to establish; if carried, its reviews/Q&A are a second independent retail-community surface.
    route_or_query: https://www.ulta.com/ search "Tower 28"
    requirement: conditional
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web_expected
    relevance: unknown
    gap_id: null
  - coverage_id: COV-009
    source_family: retail_pdp
    source_surface: marketplace_presence
    venue: Amazon
    relevance_rationale: Marketplace presence, seller identity (first-party vs third-party/gray), price state, and review surface; channel-control evidence.
    route_or_query: https://www.amazon.com/ search "Tower 28 Beauty"
    requirement: conditional
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web_expected
    relevance: unknown
    gap_id: null
  - coverage_id: COV-010
    source_family: retail_pdp
    source_surface: retailer_pdp_state
    venue: Sephora Tower 28 brand page and PDPs
    relevance_rationale: Current assortment, placement, price, promotion, availability, badges, and stock state; retail/channel-productivity proxies with explicit proxy ceilings.
    route_or_query: https://www.sephora.com/brand/tower-28 and SKU PDPs
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web_expected
    relevance: relevant
    gap_id: null
  - coverage_id: COV-011
    source_family: owned_channels
    source_surface: brand_pdp_claims_price
    venue: tower28beauty.com product pages
    relevance_rationale: Exact current product/SKU, formula/ingredient framing, package, price, promotion, and claim versions; official commitment and claims-substantiation surface.
    route_or_query: tower28beauty.com collection and product pages, ingredient/claims sections
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-012
    source_family: creator_social_video
    source_surface: tiktok_public
    venue: TikTok public posts and comments
    relevance_rationale: Attention spread, audience language, campaign vs independent separation for Tower 28 products; lawful public routes only.
    route_or_query: TikTok public search "Tower 28" and product-name queries surfaced by the scan
    requirement: conditional
    status: not_checked
    yield: unknown
    recency: unknown
    access: lawful_public_routes_only
    relevance: unknown
    gap_id: null
  - coverage_id: COV-013
    source_family: creator_social_video
    source_surface: instagram_public
    venue: Instagram public posts and comments
    relevance_rationale: Brand-owned and creator posts, comment language, campaign-overlap risk; lawful public routes only.
    route_or_query: Instagram public profiles/hashtags for Tower 28
    requirement: conditional
    status: not_checked
    yield: unknown
    recency: unknown
    access: lawful_public_routes_only
    relevance: unknown
    gap_id: null
  - coverage_id: COV-014
    source_family: creator_social_video
    source_surface: youtube_public
    venue: YouTube videos and comments
    relevance_rationale: Longer-form reviews and comparison content; comment surfaces carry switching and rejection language; distinguish sponsored from independent.
    route_or_query: YouTube search "Tower 28" review / comparison queries
    requirement: conditional
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web_expected
    relevance: unknown
    gap_id: null
  - coverage_id: COV-015
    source_family: search_discovery
    source_surface: search_surface_mgt
    venue: public search surfaces (exact-query walk)
    relevance_rationale: Market language, comparison/confusion pairs, hidden-venue pointers, changing questions, and counterevidence queries; route discovery only, never demand proof.
    route_or_query: bounded exact-query walk seeded from Tower 28 product names, claims, and customer language
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-016
    source_family: aeo_answer_engines
    source_surface: answer_visibility
    venue: answer engines (AI overviews / assistants)
    relevance_rationale: Visibility annotation only — how Tower 28 and its need states are answered and which sources are cited; never an independent demand-origin surface.
    route_or_query: bounded answer-engine queries mirroring COV-015 exact queries
    requirement: conditional
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web
    relevance: unknown
    gap_id: null
  - coverage_id: COV-017
    source_family: news_editorial_trade
    source_surface: trade_press
    venue: beauty trade and editorial press (e.g., Glossy, Business of Beauty, WWD, Beauty Independent, consumer beauty editorial)
    relevance_rationale: Dated chronology for launches, distribution moves, leadership, funding/ownership, and official commitments; independence vs announcement-syndication must be checked.
    route_or_query: trade-press site searches "Tower 28" with date filters per the recency ladder
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web_expected_some_paywalled
    relevance: relevant
    gap_id: null
  - coverage_id: COV-018
    source_family: professional_org_motion
    source_surface: careers_ats_and_leadership
    venue: Tower 28 careers/ATS pages and public leadership statements
    relevance_rationale: Role ownership, hiring posture, and organizational shape; job postings are org-motion evidence only, never execution-capacity fact.
    route_or_query: tower28beauty.com careers page / linked ATS; founder and executive public statements
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web_expected
    relevance: relevant
    gap_id: null
  - coverage_id: COV-019
    source_family: owned_channels
    source_surface: press_and_announcements
    venue: Tower 28 press page, launch announcements, brand socials as official chronology
    relevance_rationale: Official chronology and claim framing; high chronology value, low independence; separates observation time from effective time.
    route_or_query: tower28beauty.com press/blog pages and official announcement posts
    requirement: required
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web
    relevance: relevant
    gap_id: null
  - coverage_id: COV-020
    source_family: professional_org_motion
    source_surface: registries_and_filings
    venue: trademark and corporate registries
    relevance_rationale: Ownership state and parent resolution (parent currently unresolved in the selection companion); identity and commitment facts with effective dates.
    route_or_query: USPTO/state registry searches for Tower 28 Beauty entities
    requirement: conditional
    status: not_checked
    yield: unknown
    recency: unknown
    access: public_web
    relevance: relevant
    gap_id: GAP-002
```

### 4. Observation Ledger

```yaml
observation_ledger:
  - observation_id: OBS-001
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-001
    source_url_or_packet_locator: https://www.tower28beauty.com/ (recorded in docs/research/forseti_beauty_us_company_selection_v0.json row USBEAUTY-019)
    source_family: owned_channels
    source_surface: brand_site_home
    publisher_or_venue: Tower 28 Beauty
    source_class: official_first_party
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-16"
    age_anchor_basis: current_page_observation
    exact_locator: brand site homepage, live DTC storefront state
    evidence_excerpt: Live first-party Tower 28 Beauty DTC storefront observed during the US beauty selection run.
    lawful_access_route: public_web
    access_limitation: screen-light current-availability evidence only; observation time is not the underlying event effective date
    independence_syndication_group: tower28_owned_001
    independent_corroboration_ids: []
    ambiguity_limitation: Brand identity resolved; parent/ownership state unresolved.
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: primary_current
    consumed_by_sections: [5, 6, 9]
  - observation_id: OBS-002
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-002
    source_url_or_packet_locator: https://www.sephora.com/search?keyword=Tower+28+Beauty (recorded in docs/research/forseti_beauty_us_company_selection_v0.json row USBEAUTY-019)
    source_family: retail_pdp
    source_surface: retailer_search
    publisher_or_venue: Sephora
    source_class: retailer
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-16"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-16"
    age_anchor_basis: current_page_observation
    exact_locator: Sephora keyword-search results for "Tower 28 Beauty"
    evidence_excerpt: Sephora search results returned Tower 28 Beauty products, evidencing carriage at observation time.
    lawful_access_route: public_web
    access_limitation: search-result carriage state only; establishes neither assortment depth, velocity, nor sales
    independence_syndication_group: sephora_catalog_001
    independent_corroboration_ids: []
    ambiguity_limitation: Carriage at observation time; not a dated distribution event.
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: current_corroboration
    consumed_by_sections: [5, 6, 9]
  - observation_id: OBS-003
    subject_name: Tower 28 Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-003
    source_url_or_packet_locator: https://www.revolve.com/r/Search.jsp?search=Tower+28+Beauty (recorded in docs/research/forseti_beauty_us_company_selection_v0.json row USBEAUTY-019)
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
    exact_locator: Revolve search results for "Tower 28 Beauty"
    evidence_excerpt: Revolve search results returned Tower 28 Beauty products, evidencing carriage at observation time.
    lawful_access_route: public_web
    access_limitation: search-result carriage state only; establishes neither assortment depth, velocity, nor sales
    independence_syndication_group: revolve_catalog_001
    independent_corroboration_ids: []
    ambiguity_limitation: Carriage at observation time; not a dated distribution event.
    contradiction_state: none_observed
    fact_domain: company_fact
    current_state_use: current_corroboration
    consumed_by_sections: [5, 6, 9]
```

### 5. Positioning, Offerings, Markets, And Channels

At commission stage the sealed substrate is deliberately thin: Tower 28 Beauty
operates a live first-party DTC storefront (OBS-001) and is carried by Sephora
(OBS-002) and Revolve (OBS-003) at observation time, consistent with the
selection companion's scaling-stratum classification (DTC plus specialty
beauty). No positioning, claims, price, promotion, or assortment observations
have been made yet in this lane; those are commissioned to COV-010, COV-011,
and COV-002/COV-003 deepening. Everything beyond observed carriage is a typed
gap, not an inference.

### 6. Strategic And Operating Chronology

No dated chronology exists in this ledger yet. The only observations are
current-page observations from the selection run (OBS-001, OBS-002, OBS-003),
whose observation time deliberately does not date any underlying launch,
distribution agreement, ownership, or company event. Dated chronology is
commissioned to COV-017 (trade press), COV-019 (official announcements), and
COV-020 (registries/filings), with observed, published, and effective dates
kept separate under the recency contract. `time_posture` remains
`recency_first`; no longitudinal question is manufactured at commission stage.

### 7. Customer And Community Response

No customer or community observations exist yet in this ledger; the only seed
observations are company-side (OBS-001, OBS-002, OBS-003). The customer-world
venue map is commissioned to COV-004 (mandatory bounded Reddit scout,
exact-thread only while the separate subreddit-graph lane output remains
unsupplied — GAP-001), COV-005 (experimental Quora scout), COV-006
(category-aware specialist venues), COV-007/COV-008 (retail communities), and
COV-012 through COV-014 (creator/social surfaces through lawful routes). All
community evidence gathered under this commission remains external customer
evidence — never representative demand, sell-through, repeat purchase,
internal company fact, or buyer proof.

### 8. Competitor Context, Contradictions, And Gaps

No comparator observations exist yet (the seed observations OBS-001 through
OBS-003 concern the subject only). Named alternatives may enter the Phase 1
scan solely as bounded comparator pointers where needed to interpret Tower 28
customer substitution, price/claim context, or channel overlap; deep
competitor treatment requires a separately named follow-up commission. No
contradictions have been observed among the three seed observations, and the
scan is required to actively seek counterevidence and contradiction rather
than confirmations. Open typed gaps: the subreddit-graph dependency (GAP-001),
unresolved parent/ownership state (GAP-002), and the standing boundary that
internal company facts — sell-through, repeat rates, margin, inventory,
claims files — are not publicly observable and must produce explicit holds
rather than attention proxies (GAP-003).

### 9. Company Surface Candidate Ledger

```yaml
company_surface_candidate_ledger:
  - candidate_id: CSC-001
    observation_ids: [OBS-001]
    candidate_only: true
    import_status: not_imported
    candidate_fact_class: company_fact
    bounded_fact: Tower 28 Beauty operated a live first-party DTC storefront at tower28beauty.com as observed on 2026-07-16.
    identity_state: resolved
    time_scope: observed_current_page_at_2026-07-16
    limitations: Screen-light observation; no Company Surface import, identity resolution beyond the Brand, or effective-date claim.
  - candidate_id: CSC-002
    observation_ids: [OBS-002, OBS-003]
    candidate_only: true
    import_status: not_imported
    candidate_fact_class: company_fact
    bounded_fact: Sephora and Revolve search surfaces returned Tower 28 Beauty products on 2026-07-16, evidencing carriage at observation time.
    identity_state: resolved
    time_scope: observed_current_page_at_2026-07-16
    limitations: Carriage state only; no assortment depth, velocity, terms, or dated distribution event; no Company Surface import.
```

### 10. Completion Ledger And Run Boundary

```yaml
completion_ledger:
  coverage_status: complete_with_typed_gap
  observation_status: traceable
  candidate_status: candidate_only_not_imported
  completeness_policy: necessary_complete_no_arbitrary_caps
  hidden_venue_discovery: category_aware
  reddit_scout_status: commissioned_not_yet_run
  quora_scout_status: commissioned_not_yet_run
  commission_stage_note: >
    This artifact is the sealed pre-scan commission. The Reddit and Quora scout
    statuses use the contract's commission-stage value commissioned_not_yet_run
    because writing a checked/blocked value would be false before the scan
    executes; the Phase 1 CI report replaces them with the enum values actually
    earned by the scan. The commission-stage vocabulary (run_boundary
    COMMISSION_SEALED_PRE_SCAN plus commissioned_not_yet_run) was added to the
    CSB company-profile contract on 2026-07-17 in response to adversarial
    review finding AR-07 against an earlier revision of this artifact, which
    had to borrow the completed-report boundary.
  customer_community_boundary: external_evidence_not_representative_demand_or_internal_fact
  deep_competitor_treatment: separate_named_follow_up_required
  classifier_handoff: omitted
  required_lens_coverage:
    positioning: {status: gap, observation_ids: [OBS-001], rationale: only a live-storefront observation exists; positioning observations commissioned to COV-010/COV-011}
    offerings_and_claims: {status: gap, observation_ids: [], rationale: product, price, and claim-version observations commissioned to COV-010/COV-011/COV-019}
    markets_and_channels: {status: gap, observation_ids: [OBS-001, OBS-002, OBS-003], rationale: carriage observed at DTC, Sephora, Revolve; assortment, availability, promotion, and channel state commissioned to COV-008/COV-009/COV-010}
    strategic_and_operating_moves: {status: gap, observation_ids: [], rationale: dated chronology commissioned to COV-017/COV-019/COV-020}
    customer_and_community_response: {status: gap, observation_ids: [], rationale: customer-world venues commissioned to COV-004 through COV-008 and COV-012 through COV-014}
    competitor_and_substitute_context: {status: gap, observation_ids: [], rationale: bounded comparator pointers permitted only where needed to interpret the subject; none observed yet}
    contradictions: {status: gap, observation_ids: [], rationale: no contradictions observed among seed observations; scan must actively seek counterevidence}
    evidence_gaps: {status: complete, observation_ids: [], rationale: typed gaps GAP-001 through GAP-003 and requests REQ-001/REQ-002 enumerated below}
  gaps:
    - gap_id: GAP-001
      gap_type: dependency_pending
      status: open
      description: The separate subreddit-graphing lane output (exact artifact path/commit) is not supplied. Phase 1 proceeds with bounded exact-thread Reddit scouting only and must not claim mapped Reddit-neighborhood coverage. Ask the owner for the exact artifact when community-route coverage becomes decision-material.
      affected_coverage_ids: [COV-004]
      request_ids: []
    - gap_id: GAP-002
      gap_type: identity
      status: open
      description: Parent/ownership state for Tower 28 Beauty is unresolved in the selection companion; registry/filing routes are commissioned to establish it with effective dates.
      affected_coverage_ids: [COV-001, COV-020]
      request_ids: []
    - gap_id: GAP-003
      gap_type: access_boundary
      status: open
      description: Internal company facts (sell-through, repeat/reorder, margin, inventory, claims substantiation files, intent) are not publicly observable. Where such a fact controls a later claim, the report must hold explicitly rather than substitute attention proxies.
      affected_coverage_ids: []
      request_ids: []
  requests:
    - request_id: REQ-001
      request_type: bounded_csb_first_scan
      owner: scanning
      status: requested
      description: Execute the bounded CSB-first Phase 1 scan over all not_checked coverage rows, including the default broad-scout phase, exact-query discovery, hidden-venue discovery, negatives, access notes, and counterevidence, under the scan bounds and recency contract in this commission.
      source_surface: all_not_checked_coverage_rows
    - request_id: REQ-002
      request_type: capture_preservation
      owner: capture
      status: requested
      description: Where the scan surfaces decision-relevant material on creator/social or paywalled surfaces requiring preservation beyond screen-light reads, request lawful capture routes; no scraping or platform-access authorization is granted by this commission.
      source_surface: creator_social_and_walled_surfaces_found_by_scan
  run_boundary: COMMISSION_SEALED_PRE_SCAN
  next_authorized_step: Execute REQ-001 (bounded CSB-first Phase 1 scan) and REQ-002 as authorized; seal and validate the scan artifact before writing the Phase 1 CI report.
```
