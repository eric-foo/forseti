# Marc Jacobs Beauty Relaunch Understanding Commission Board v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Completed company report for the Marc Jacobs Beauty relaunch Understanding Acquire & Seal turn.
use_when:
  - Consuming the sealed acquisition in a separately authorized Deliver turn.
  - Auditing current owned, retailer, review, community, and independent evidence.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_beauty_marc_jacobs_beauty_relaunch_understanding_scan_receipt_v0.md
  - docs/workflows/forseti_beauty_marc_jacobs_beauty_relaunch_understanding_acquisition_seal_v0.md
stale_if:
  - A cited current surface materially changes or acquisition is reopened.
```

### Capture Locator Resolution

Packet locators in this board preserve the acquisition-time `.acquisition/`
prefix. After collection and evaluator replay, the unchanged 78-file capture
root was moved to the placement-excluded worktree scratch path
`C:\tmp\forseti-marc-jacobs-stopping-dogfood\_acquisition\`. Resolve a recorded
`.acquisition/` locator by replacing that prefix with this bound scratch root.
The move changed no packet ID or checkpoint bytes.

### 1. Company Commission And Identity Receipt

```yaml
company_commission_receipt:
  commission_id: marc_jacobs_beauty_relaunch_understanding_csb_20260719
  intelligence_cycle:
    cycle_id: marc_jacobs_beauty_relaunch_understanding_20260719
    phase: understanding
    turn: acquire_and_seal
    bound_question: What does current public evidence show about how the relaunched Marc Jacobs Beauty proposition is expressed across owned claims, assortment, Sephora presentation, and early user experience, and where do those surfaces align, conflict, or remain unproven?
    intended_consumer: Forseti Intelligence Cycle Deliver turn
    intended_use: decision-neutral company understanding
    phase_scope: Current Marc Jacobs Beauty relaunch proposition across owned, Sephora, independent editorial, and early community surfaces.
  mode: forward
  commission_profile: company_competitive_intelligence
  subject_count: 1
  subject_identity:
    raw_name: Marc Jacobs Beauty
    subject_kind: brand
    identity_state: resolved
  as_of_date: "2026-07-19"
  time_posture: recency_first
  longitudinal_period: null
  longitudinal_rationale: not_applicable
  initial_proving_run: false
```

### 2. Decision-Neutral Boundary

This report covers one brand. Coty appears only as the publicly named operating
and licensing partner. The evidence supports a current-state comparison of
owned expression, retailer translation, and attributable early experience. It
does not establish representative demand, defect prevalence, internal company
fact from community sources, local availability, a competitor verdict, or a
purchase recommendation.

### 3. Source-Family And Venue Coverage Ledger

```yaml
coverage_ledger:
  - coverage_id: COV-001
    source_family: owned_channels
    source_surface: current_relaunch_announcement
    venue: Coty
    relevance_rationale: Required R0 official relaunch frame, partnership identity, proposition, assortment, price, and named launch channels.
    route_or_query: https://www.coty.com/news/coty-launches-marc-jacobs-beauty-one-of-the-most-requested-luxury-comebacks
    requirement: required
    status: checked
    yield: evidence_found
    recency: recent
    access: direct HTTP packet passed
    relevance: load-bearing
    gap_id: null
  - coverage_id: COV-002
    source_family: owned_channels
    source_surface: current_brand_and_product_pages
    venue: Marc Jacobs
    relevance_rationale: Required R1 current assortment, product claims, packaging, texture, and experience language.
    route_or_query: current Marc Jacobs Beauty category and seven exact product URLs
    requirement: required
    status: checked
    yield: evidence_found
    recency: current
    access: category and indexed official product content read; exact Joystick packet routes preserved access denial
    relevance: load-bearing
    gap_id: GAP-001
  - coverage_id: COV-003
    source_family: retail_pdp
    source_surface: current_brand_and_product_pages
    venue: Sephora
    relevance_rationale: Required R2 retail translation of assortment, claims, price, and current page state without delivery or local-stock inference.
    route_or_query: Sephora US brand page plus canonical captures of Joystick, Born Star, and Heart On PDPs
    requirement: required
    status: checked
    yield: evidence_found
    recency: current
    access: source-confirmed US market and USD offers; delivery location unpinned
    relevance: load-bearing
    gap_id: GAP-002
  - coverage_id: COV-004
    source_family: reviews
    source_surface: dated_retail_review_records
    venue: Sephora
    relevance_rationale: Required R2 early product-experience evidence with dates and incentive markers preserved.
    route_or_query: dated rows on the three selected canonical PDP captures
    requirement: required
    status: checked
    yield: evidence_found
    recency: current
    access: target-anchored review substrates preserved
    relevance: load-bearing
    gap_id: GAP-003
  - coverage_id: COV-005
    source_family: forums_community
    source_surface: bounded_subreddit_scout_and_selected_threads
    venue: Reddit
    relevance_rationale: Mandatory R3 scout and exact-thread preservation for attributable experience, corrections, and counterevidence.
    route_or_query: four old-Reddit search surfaces and seven exact selected threads
    requirement: mandatory_bounded_scout
    status: checked
    yield: evidence_found
    recency: current
    access: canonical screening service plus old_reddit_direct_http content packets
    relevance: load-bearing
    gap_id: GAP-003
  - coverage_id: COV-006
    source_family: forums_community
    source_surface: answer_forum_scout
    venue: Quora
    relevance_rationale: No decision-material job survived substitution by owned, retailer-review, Reddit, and independent editorial evidence.
    route_or_query: not_applicable
    requirement: conditional
    status: not_applicable
    yield: not_applicable
    recency: unknown
    access: not attempted
    relevance: dominated
    gap_id: null
  - coverage_id: COV-007
    source_family: creator_social_video
    source_surface: public_brand_or_creator_video
    venue: TikTok
    relevance_rationale: No unique non-dominated current proposition or experience job remained after R2, R3, and R4.
    route_or_query: not_applicable
    requirement: conditional
    status: not_applicable
    yield: not_applicable
    recency: current
    access: not attempted
    relevance: dominated
    gap_id: null
  - coverage_id: COV-008
    source_family: news_editorial_trade
    source_surface: independent_current_launch_coverage
    venue: independent editorial and trade sources
    relevance_rationale: Required R4 independent corroboration and contradiction check with disclosure and syndication boundaries.
    route_or_query: Allure, The Looker or Daily Beast, and LiftBakeLove hands-on reviews
    requirement: required
    status: checked
    yield: evidence_found
    recency: recent
    access: public rendered editorial reads
    relevance: load-bearing
    gap_id: null
  - coverage_id: COV-009
    source_family: search_discovery
    source_surface: bounded_broad_scout_and_hidden_venue_discovery
    venue: public search and source-native discovery surfaces
    relevance_rationale: Required R4 better-origin, syndication, hidden-venue, contradiction, and decisive-negative discovery.
    route_or_query: bounded exact relaunch, review, product, and venue queries
    requirement: category_aware
    status: checked
    yield: evidence_found
    recency: current
    access: public search and source-native reads
    relevance: load-bearing
    gap_id: null
```

### 4. Observation Ledger

```yaml
observation_ledger:
  - observation_id: OBS-001
    subject_name: Marc Jacobs Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-001
    source_url_or_packet_locator: .acquisition/captures/r0_coty_relaunch/manifest.json
    source_family: owned_channels
    source_surface: current_relaunch_announcement
    publisher_or_venue: Coty
    source_class: official_first_party
    publication_date: "2026-05-20"
    event_or_effective_date: "2026-05-20"
    observation_at: "2026-07-19T11:43:28Z"
    effective_time_precision: day
    recency_tier: days_31_90
    age_anchor_date: "2026-05-20"
    age_anchor_basis: publication
    exact_locator: packet 01KXX30ECGZPFHG4GVE3BCTX79; launch, proposition, assortment, price, packaging, and channel paragraphs
    evidence_excerpt: Coty described Joyride Sensoriality, bold self-expression, seven opening products, tactile charm-led packaging, prices from 26 to 42 dollars, and staged Marc Jacobs, Sephora, and Selfridges distribution.
    lawful_access_route: public first-party page preserved by direct HTTP
    access_limitation: First-party framing cannot establish performance, experience, prevalence, or local availability.
    independence_syndication_group: coty_relaunch_origin_20260520
    independent_corroboration_ids: []
    ambiguity_limitation: Launch language and forward channel timing are publisher claims.
    contradiction_state: none_within_official_frame
    fact_domain: company_fact
    current_state_use: current_corroboration
    consumed_by_sections: [5, 6, 8]
  - observation_id: OBS-002
    subject_name: Marc Jacobs Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-002
    source_url_or_packet_locator: https://www.marcjacobs.com/us-en/the-marc-jacobs/beauty-fragrance/view-all/
    source_family: owned_channels
    source_surface: current_brand_and_product_pages
    publisher_or_venue: Marc Jacobs
    source_class: official_first_party
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-19T11:45:26Z"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-19"
    age_anchor_basis: current_page_observation
    exact_locator: current face, eyes, lips category pages and Joystick, Legally Bronze, Money Shot, Born Star, Flashes, Drawn This Way, and Heart On URLs
    evidence_excerpt: Owned surfaces presented seven products across face, eyes, and lips with playful shape-and-charm packaging, multi-use or sensorial textures, broad shade ranges, and specific wear claims up to 24 hours.
    lawful_access_route: public category pages and indexed official PDP content; exact Joystick packet attempts preserved
    access_limitation: Exact Joystick direct HTTP returned 403 and browser capture returned Akamai access denial.
    independence_syndication_group: marc_jacobs_owned_current_20260719
    independent_corroboration_ids: [OBS-003, OBS-010, OBS-011, OBS-012]
    ambiguity_limitation: Owned performance language is not an independent wear test.
    contradiction_state: product_specific_conflicts_below
    fact_domain: company_fact
    current_state_use: primary_current
    consumed_by_sections: [5, 6, 8]
  - observation_id: OBS-003
    subject_name: Marc Jacobs Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-003
    source_url_or_packet_locator: .acquisition/captures/r2_sephora_joystick_blush_verified/manifest.json
    source_family: retail_pdp
    source_surface: cloakbrowser_snapshot
    publisher_or_venue: Sephora
    source_class: retailer
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-19T11:52:52Z"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-19"
    age_anchor_basis: current_page_observation
    exact_locator: Joystick packet 01KXX3HN463G98Y4QQH3WJM0QD plus Born Star 01KXX3MEN3B0CXA2PNR2EWSA1F and Heart On 01KXX3PYBM91TSMP5GA6D3H9ZJ
    evidence_excerpt: Sephora translated the line as playful, upgraded, multi-use, and long-wearing and exposed selected USD offers at 35, 29, and 34 dollars.
    lawful_access_route: anonymous registry-authorized Sephora US CloakBrowser capture with country_switch=us
    access_limitation: US market and USD offers were confirmed; delivery location and local stock were not pinned.
    independence_syndication_group: sephora_retail_current_20260719
    independent_corroboration_ids: [OBS-001, OBS-002]
    ambiguity_limitation: Retail product copy may derive from brand-supplied copy.
    contradiction_state: retailer_subset_and_experience_conflicts_below
    fact_domain: company_fact
    current_state_use: primary_current
    consumed_by_sections: [5, 6, 8]
  - observation_id: OBS-004
    subject_name: Marc Jacobs Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-004
    source_url_or_packet_locator: .acquisition/projections/r2_sephora_joystick_blush_verified_projection.json
    source_family: reviews
    source_surface: dated_retail_review_records
    publisher_or_venue: Sephora Joystick PDP
    source_class: customer_community
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-19T11:52:52Z"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-14"
    age_anchor_basis: publication
    exact_locator: target review substrate and dated rows through 2026-07-14; DOM 161 reviews at capture
    evidence_excerpt: Rows frequently praised smooth buildability and blendability, while a non-incentivized three-star row described lighter-than-packaging pigment and cute but impractical cheap-feeling packaging.
    lawful_access_route: target-anchored Sephora projection from canonical captured DOM
    access_limitation: DOM showed 161 reviews while LD JSON showed 162; incentive markers and row dates were preserved.
    independence_syndication_group: sephora_joystick_reviews_20260719
    independent_corroboration_ids: [OBS-007, OBS-010, OBS-011, OBS-012]
    ambiguity_limitation: Dated rows are attributable examples, not representative prevalence.
    contradiction_state: buildability_aligns_wear_and_packaging_mixed
    fact_domain: external_customer_evidence
    current_state_use: primary_current
    consumed_by_sections: [5, 7, 8]
  - observation_id: OBS-005
    subject_name: Marc Jacobs Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-004
    source_url_or_packet_locator: .acquisition/projections/r2_sephora_born_star_verified_projection.json
    source_family: reviews
    source_surface: dated_retail_review_records
    publisher_or_venue: Sephora Born Star PDP
    source_class: customer_community
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-19T11:54:24Z"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-18"
    age_anchor_basis: publication
    exact_locator: target review substrate and ten dated rows through 2026-07-18; 247 reviews at capture
    evidence_excerpt: Rows split between smooth, easy, no-crease wear and breakage or shrinkage in the pan, creasing, weak pigment, warm-shade mismatch, and bulky-price concerns.
    lawful_access_route: target-anchored Sephora projection from canonical captured DOM
    access_limitation: Incentive markers and row dates were preserved; rows do not establish a defect rate.
    independence_syndication_group: sephora_born_star_reviews_20260719
    independent_corroboration_ids: [OBS-007, OBS-010, OBS-011, OBS-012]
    ambiguity_limitation: Product, shade, application, and reviewer differences remain material.
    contradiction_state: wear_and_packaging_mixed
    fact_domain: external_customer_evidence
    current_state_use: primary_current
    consumed_by_sections: [5, 7, 8]
  - observation_id: OBS-006
    subject_name: Marc Jacobs Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-004
    source_url_or_packet_locator: .acquisition/projections/r2_sephora_heart_on_verified_projection.json
    source_family: reviews
    source_surface: dated_retail_review_records
    publisher_or_venue: Sephora Heart On PDP
    source_class: customer_community
    publication_date: null
    event_or_effective_date: null
    observation_at: "2026-07-19T11:55:45Z"
    effective_time_precision: current_page_observation
    recency_tier: days_0_30
    age_anchor_date: "2026-07-15"
    age_anchor_basis: publication
    exact_locator: target review substrate and ten dated rows through 2026-07-15; 240 reviews at capture
    evidence_excerpt: Rows praised smooth moisturizing buildability but also reported shade-photo mismatches, a loose cap, returns, and one two-to-three-hour wear result.
    lawful_access_route: target-anchored Sephora projection from canonical captured DOM
    access_limitation: Incentive markers and row dates were preserved; rows are nonrepresentative.
    independence_syndication_group: sephora_heart_on_reviews_20260719
    independent_corroboration_ids: [OBS-010, OBS-012]
    ambiguity_limitation: Wear and shade findings are reviewer- and shade-specific.
    contradiction_state: absolute_all_day_non_fading_language_not_uniformly_supported
    fact_domain: external_customer_evidence
    current_state_use: primary_current
    consumed_by_sections: [5, 7, 8]
  - observation_id: OBS-007
    subject_name: Marc Jacobs Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-005
    source_url_or_packet_locator: .acquisition/captures/r3_reddit_selected_threads/sephora_review_packet/manifest.json
    source_family: forums_community
    source_surface: old_reddit_direct_http
    publisher_or_venue: Reddit r/Sephora
    source_class: customer_community
    publication_date: "2026-06-05"
    event_or_effective_date: "2026-06-05"
    observation_at: "2026-07-19T12:03:09Z"
    effective_time_precision: day
    recency_tier: days_31_90
    age_anchor_date: "2026-06-05"
    age_anchor_basis: publication
    exact_locator: packet 01KXX44G0E513PCQHG42RS2VKN; post and 39 parsed comments
    evidence_excerpt: The post found creamy eyeshadow and blendable blush, then updated that blush lasted only a couple of hours while eyeshadow lasted all night; comments split on visual fun versus light, cheap, bulky, or flimsy hand-feel.
    lawful_access_route: exact selected public old-Reddit thread preserved in content mode
    access_limitation: Self-selected community discussion is not representative demand or defect prevalence.
    independence_syndication_group: reddit_sephora_review_1txln4q
    independent_corroboration_ids: [OBS-004, OBS-005, OBS-010, OBS-012]
    ambiguity_limitation: Packaging preference and product performance are person- and use-specific.
    contradiction_state: texture_aligns_but_blush_wear_and_luxury_handfeel_conflict
    fact_domain: external_customer_evidence
    current_state_use: current_corroboration
    consumed_by_sections: [5, 7, 8]
  - observation_id: OBS-008
    subject_name: Marc Jacobs Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-005
    source_url_or_packet_locator: .acquisition/captures/r3_reddit_selected_threads/sephora_liner_negative_packet/manifest.json
    source_family: forums_community
    source_surface: old_reddit_direct_http
    publisher_or_venue: Reddit r/Sephora and r/MakeupAddiction
    source_class: customer_community
    publication_date: "2026-06-12"
    event_or_effective_date: "2026-06-12"
    observation_at: "2026-07-19T12:03:17Z"
    effective_time_precision: day
    recency_tier: days_31_90
    age_anchor_date: "2026-06-12"
    age_anchor_basis: publication
    exact_locator: liner packets 01KXX44QSK79C36TDD0PMMTCR1, 01KXX44VBXETVR2E8S8VQD8K1N, 01KXX44YQJQHGS9XVY016818QG, and 01KXX45276A0FK374ZBV9ECEX5
    evidence_excerpt: Black, brown, and some colorful shades were reported smooth and extremely durable, while Delulu and bright-blue reports described softness, breakage, patchiness, weak payoff, smudging, or short waterline wear.
    lawful_access_route: exact selected public old-Reddit threads preserved in content mode
    access_limitation: Shade, skin, application, and technique differences prevent a line-wide conclusion.
    independence_syndication_group: reddit_selected_liner_threads_20260719
    independent_corroboration_ids: [OBS-010]
    ambiguity_limitation: A same-formula or manufacturer inference from ingredient lists remains unverified and is not adopted.
    contradiction_state: sharply_shade_dependent
    fact_domain: external_customer_evidence
    current_state_use: current_corroboration
    consumed_by_sections: [5, 7, 8]
  - observation_id: OBS-009
    subject_name: Marc Jacobs Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-005
    source_url_or_packet_locator: .acquisition/captures/r3_reddit_selected_threads/sephora_money_shot_issue_packet/manifest.json
    source_family: forums_community
    source_surface: old_reddit_direct_http
    publisher_or_venue: Reddit r/Sephora
    source_class: customer_community
    publication_date: "2026-06-05"
    event_or_effective_date: "2026-06-05"
    observation_at: "2026-07-19T12:03:13Z"
    effective_time_precision: day
    recency_tier: days_31_90
    age_anchor_date: "2026-06-05"
    age_anchor_basis: publication
    exact_locator: packet 01KXX44KM2MAGS9GMBVJ9G2900; post and 31 parsed comments
    evidence_excerpt: Multiple users described Money Shot arriving dried or shrunken, tiny, patchy, or goopy and reported replacements or returns.
    lawful_access_route: exact selected public old-Reddit thread preserved in content mode
    access_limitation: Material quality-control evidence, not a severe safety signal or defect-rate estimate.
    independence_syndication_group: reddit_money_shot_1tx2d4i
    independent_corroboration_ids: [OBS-012]
    ambiguity_limitation: Shipping, storage, batch, and user handling were not independently resolved.
    contradiction_state: fresh_feel_and_smooth_distribution_not_uniformly_supported
    fact_domain: external_customer_evidence
    current_state_use: current_corroboration
    consumed_by_sections: [5, 7, 8]
  - observation_id: OBS-010
    subject_name: Marc Jacobs Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-008
    source_url_or_packet_locator: https://www.allure.com/story/marc-jacobs-beauty-relaunch-2026-review
    source_family: news_editorial_trade
    source_surface: independent_current_launch_coverage
    publisher_or_venue: Allure
    source_class: independent
    publication_date: "2026-05-28"
    event_or_effective_date: "2026-05-28"
    observation_at: "2026-07-19T12:10:00Z"
    effective_time_precision: day
    recency_tier: days_31_90
    age_anchor_date: "2026-05-28"
    age_anchor_basis: publication
    exact_locator: multi-tester eyeliner, Born Star, Joystick, and Heart On sections
    evidence_excerpt: Testers corroborated creamy liner, blendability, and some eight-to-twelve-hour wear, but one Born Star shade migrated after five hours and Heart On did not survive eating, drinking, or kissing.
    lawful_access_route: public rendered editorial page
    access_limitation: Small tester set with product, shade, and method differences.
    independence_syndication_group: allure_mjb_review_20260528
    independent_corroboration_ids: [OBS-004, OBS-005, OBS-006, OBS-007, OBS-008]
    ambiguity_limitation: Results conflict within the tester set and should remain conditional.
    contradiction_state: independent_mixed_product_specific
    fact_domain: external_customer_evidence
    current_state_use: current_corroboration
    consumed_by_sections: [5, 7, 8]
  - observation_id: OBS-011
    subject_name: Marc Jacobs Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-008
    source_url_or_packet_locator: https://thelooker.thedailybeast.com/marc-jacobs-beauty-relaunched-review/
    source_family: news_editorial_trade
    source_surface: independent_current_launch_coverage
    publisher_or_venue: The Looker / Daily Beast
    source_class: independent
    publication_date: "2026-06-01"
    event_or_effective_date: "2026-06-01"
    observation_at: "2026-07-19T12:11:00Z"
    effective_time_precision: day
    recency_tier: days_31_90
    age_anchor_date: "2026-06-01"
    age_anchor_basis: publication
    exact_locator: disclosed pre-launch sample tests for bronzer, blush, eyeshadow, and mascara
    evidence_excerpt: The author reported buildable bronzer, more-than-typical blush staying power, no-crease all-day eyeshadow, and eight-to-ten-hour mascara wear with easy removal.
    lawful_access_route: public rendered editorial page
    access_limitation: Products were brand-supplied and the author did not choose shades.
    independence_syndication_group: daily_beast_mjb_review_20260601
    independent_corroboration_ids: [OBS-004, OBS-005, OBS-007]
    ambiguity_limitation: Positive experience does not erase contrary shade- and user-specific evidence.
    contradiction_state: independent_positive_with_disclosed_sample_context
    fact_domain: external_customer_evidence
    current_state_use: current_corroboration
    consumed_by_sections: [5, 7, 8]
  - observation_id: OBS-012
    subject_name: Marc Jacobs Beauty
    subject_kind: brand
    identity_state: resolved
    coverage_id: COV-008
    source_url_or_packet_locator: https://liftbakelove.com/2026/06/12/i-bought-too-much-from-the-marc-jacobs-beauty-relaunch-so-you-dont-have-to/
    source_family: news_editorial_trade
    source_surface: independent_current_launch_coverage
    publisher_or_venue: LiftBakeLove
    source_class: independent
    publication_date: "2026-06-12"
    event_or_effective_date: "2026-06-12"
    observation_at: "2026-07-19T12:12:00Z"
    effective_time_precision: day
    recency_tier: days_31_90
    age_anchor_date: "2026-06-12"
    age_anchor_basis: publication
    exact_locator: self-purchase disclosure and product-by-product bronzer, Born Star, Money Shot, Joystick, and Heart On sections
    evidence_excerpt: The author praised bronzer and Born Star, but reported Joystick lasting about one hour even when set, bulky and light packaging, online shade mismatch, Money Shot patchiness alone, and a lingering Heart On aftertaste.
    lawful_access_route: public rendered self-purchased review
    access_limitation: One author, affiliate links disclosed, and short post-launch testing window.
    independence_syndication_group: liftbakelove_mjb_review_20260612
    independent_corroboration_ids: [OBS-004, OBS-005, OBS-006, OBS-007, OBS-009, OBS-010]
    ambiguity_limitation: Skin, shade, taste, storage, and use context remain person-specific.
    contradiction_state: independent_mixed_with_material_negatives
    fact_domain: external_customer_evidence
    current_state_use: current_corroboration
    consumed_by_sections: [5, 7, 8]
```

### 5. Positioning, Offerings, Markets, And Channels

The owned proposition is coherent at the identity level: playful maximalism,
bold self-expression, sensorial textures, category-coded charms, and a
seven-product face/eye/lip opening assortment are consistent across Coty, Marc
Jacobs, and Sephora (OBS-001, OBS-002, OBS-003). Prices and selected USD offers
also align. Retail assortment can be narrower than owned breadth: Heart On and
Legally Bronze shade counts differ between owned and Sephora, which is
consistent with a retailer subset rather than proof of a formula contradiction
(OBS-002, OBS-003).

Product experience is less uniform than the proposition. Blendability and
creaminess recur, but wear, color payoff, shade representation, and luxury
hand-feel vary by product, shade, and tester (OBS-004, OBS-005, OBS-006,
OBS-007, OBS-008, OBS-009, OBS-010, OBS-011, OBS-012). Sephora US/USD is
confirmed; delivery and local stock remain unpinned (OBS-003).

### 6. Strategic And Operating Chronology

Coty publicly announced the relaunch on May 20, 2026, with MarcJacobs.com,
Sephora, and Selfridges channel timing and later Sephora-store rollout
(OBS-001). Current owned and retailer surfaces observed July 19 show the
opening assortment live online (OBS-002, OBS-003). This chronology is public
surface evidence only; it does not establish internal launch performance.

### 7. Customer And Community Response

Early attributable response is mixed rather than uniformly positive or
negative. Mascara texture and removal, eyeshadow creaminess, bronzer
blendability, and some eyeliner shades receive strong favorable reports
(OBS-005, OBS-007, OBS-008, OBS-010, OBS-011, OBS-012). Counterevidence
clusters around short blush wear, shade-photo mismatch, light or bulky
packaging, liner softness or breakage in some shades, Heart On wear or taste,
and Money Shot shrinkage or texture (OBS-004, OBS-005, OBS-006, OBS-007,
OBS-008, OBS-009, OBS-010, OBS-012).

These rows and threads establish attributable examples only. Incentive markers,
sample disclosure, self-purchase disclosure, and source-specific limitations
remain attached; none of the evidence establishes representative demand or
defect prevalence.

### 8. Competitor Context, Contradictions, And Gaps

Comparator references are interpretive, not a competitor verdict. Users and
reviewers compare Joystick with Rhode, Money Shot with Half Magic, and Drawn
This Way with lower-priced liners; one Reddit author inferred formula
equivalence from ingredient lists, but that inference remains unverified
(OBS-004, OBS-007, OBS-008, OBS-009, OBS-012).

The clearest contradictions are narrower than a line-wide failure: Heart On's
absolute-sounding all-day or non-fading language is not supported by every wear
test (OBS-006, OBS-010); Joystick's wear varies from roughly one or two hours
to longer favorable reports (OBS-004, OBS-007, OBS-011, OBS-012); Born Star
varies by shade and tester from no-crease longevity to migration or creasing
(OBS-005, OBS-010, OBS-011, OBS-012); and eyeliner performance is sharply
shade-dependent (OBS-008, OBS-010). Money Shot has repeated attributable
quality-control concerns, but no defect rate or severe safety signal is
established (OBS-009, OBS-012).

### 9. Company Surface Candidate Ledger

```yaml
company_surface_candidate_ledger: []
```

### 10. Completion Ledger And Run Boundary

```yaml
completion_ledger:
  completion_scope: completed_understanding_acquire_and_seal
  coverage_status: required_routes_checked_or_explicitly_not_applicable
  observation_status: twelve_current_or_recent_observations
  candidate_status: no_company_surface_candidate_commissioned
  completeness_policy: necessary_complete_no_arbitrary_caps
  hidden_venue_discovery: category_aware
  reddit_scout_status: checked_positive_yield
  quora_scout_status: not_required_no_decision_material_job
  customer_community_boundary: external_evidence_not_representative_demand_or_internal_fact
  deep_competitor_treatment: separate_named_follow_up_required
  classifier_handoff: omitted
  required_lens_coverage:
    positioning: {status: complete, observation_ids: [OBS-001, OBS-002, OBS-003], rationale: owned and retailer proposition surfaces were checked}
    offerings_and_claims: {status: complete, observation_ids: [OBS-002, OBS-003, OBS-004, OBS-005, OBS-006], rationale: current assortment, claims, and selected experience rows were checked}
    markets_and_channels: {status: complete, observation_ids: [OBS-001, OBS-003], rationale: named channels and Sephora US/USD were confirmed with delivery explicitly unpinned}
    strategic_and_operating_moves: {status: complete, observation_ids: [OBS-001, OBS-002, OBS-003], rationale: public relaunch and current online expression were bounded}
    customer_and_community_response: {status: complete, observation_ids: [OBS-004, OBS-005, OBS-006, OBS-007, OBS-008, OBS-009, OBS-010, OBS-011, OBS-012], rationale: dated reviews, mandatory Reddit scout, selected threads, and independent reviews were checked}
    competitor_and_substitute_context: {status: complete, observation_ids: [OBS-007, OBS-008, OBS-009, OBS-012], rationale: bounded comparator references were retained without expanding to a competitor verdict}
    contradictions: {status: complete, observation_ids: [OBS-004, OBS-005, OBS-006, OBS-007, OBS-008, OBS-009, OBS-010, OBS-011, OBS-012], rationale: product-, shade-, tester-, and disclosure-specific conflicts were preserved}
    evidence_gaps: {status: complete, observation_ids: [OBS-002, OBS-003, OBS-004, OBS-008], rationale: residuals are typed below and do not block the bounded report}
  gaps:
    - gap_id: GAP-001
      gap_type: access_provenance
      status: accepted_residual
      description: Exact owned Joystick packet capture is partial because direct HTTP and browser routes preserved access denial.
      affected_coverage_ids: [COV-002]
      request_ids: []
    - gap_id: GAP-002
      gap_type: location_pin
      status: bounded_unknown
      description: Sephora US market and USD offers were confirmed, but delivery and local stock were not pinned.
      affected_coverage_ids: [COV-003]
      request_ids: []
    - gap_id: GAP-003
      gap_type: representativeness
      status: evidence_boundary
      description: Dated reviews and community threads are attributable external evidence, not prevalence or representative demand.
      affected_coverage_ids: [COV-004, COV-005]
      request_ids: []
    - gap_id: GAP-004
      gap_type: unverified_inference
      status: not_adopted
      description: A user-inferred formula or manufacturer equivalence from ingredient lists remains unverified.
      affected_coverage_ids: [COV-005]
      request_ids: []
  requests: []
  run_boundary: COMPANY_REPORT_COMPLETE_NO_DOWNSTREAM_EXECUTION
  next_authorized_step: A separately authorized Deliver turn may consume the acquisition seal; no further acquisition runs by default.
```
