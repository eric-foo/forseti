# Orca Fragrance-Native Database Live Probe v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: CSB-first live probe and capture-route pinning receipt for fragrance-native databases.
use_when:
  - Seeding Capture from a bounded Scanning/probe pass over Fragrantica, Parfumo, and Basenotes.
  - Reconstructing why Fragrantica and Parfumo are preservation candidates while Basenotes is not pinned in this environment.
authority_boundary: retrieval_only
source_paths:
  - docs/research/orca_specialist_fragrance_precursor_surface_csb_board_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
  - orca/product/spines/foundation/vertical_exploration/orca_vertical_exploration_guide_v0.md
  - orca/product/spines/scanning/README.md
stale_if:
  - Any probed site changes access posture or page substrate.
  - A later packet-grade Capture run preserves raw source bodies and supersedes these screen-light observations.
  - Basenotes becomes reachable through a new anti-bot, proxy, archive, or entitled manual route.
```

## Scan Intake Receipt

```yaml
commission_id: fragrance_native_db_live_probe_v0
scan_date: 2026-06-29
mode: forward
subject: Fragrance-native database capture route probe for Fragrantica, Parfumo, and Basenotes.
market_or_geography: US-first fragrance within beauty and personal care.
source_context_status: SOURCE_CONTEXT_READY
csb_board: docs/research/orca_specialist_fragrance_precursor_surface_csb_board_v0.md
run_caps:
  max_screening_moves_total: 16
  max_exact_queries_total: 4
screening_moves_used: 13
exact_queries_used: 2
hidden_venue_pointers: 1
capture_requests: 2
closeout_state: capture_preservation_only
```

## Broad Scout Return

This bounded `broad_scout_return` checked three fragrance-native database frontiers from the CSB board: Fragrantica, Parfumo, and Basenotes. It included exact-query discovery for Basenotes and Parfumo URL resolution, venue evaluation by direct HTTP, anti-block HTTP, and visible browser reads, hidden venue pointers for correct Parfumo product routing, negatives and access notes for Basenotes, and recency/current-state preservation pressure where public product pages returned source-visible body markers. Recommended main deepening: run packet-grade preservation only for Fragrantica and Parfumo using their pinned direct-HTTP product routes; keep Basenotes as a no-pin re-probe target until a new access fact appears.

The probe did not rank databases, prove demand, scrape at volume, create monitoring, stage packets, touch ECR, or authorize Data Lake work.

## CSB Board Intake

Board source: `docs/research/orca_specialist_fragrance_precursor_surface_csb_board_v0.md`.

Rows consumed as route map: SBR-001, SBR-002, SBR-003, SBR-007, SBR-010.

## Exact Query Discovery Ledger

| Query ID | Query text | Intent | Result class | Next-route decision |
| --- | --- | --- | --- | --- |
| EQ-001 | Parfumo internal perfume search for `Baccarat Rouge 540` | Resolve a correct Parfumo product locator without guessing. | hidden_venue_pointer | Pin `https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum` for product-page probe. |
| EQ-002 | Public search snippet mining for `site:basenotes.com/fragrances Baccarat Rouge 540 Maison Francis Kurkdjian` and generic Basenotes query | Test snippet route after Basenotes direct, anti-block, and browser routes hit Cloudflare. | access_note | No usable Basenotes locator surfaced; search surface returned anomaly/challenge pages. |

## Venue Evaluation Move Log

| Move | CSB row(s) | Frontier | Value class | What happened | Stop check |
| --- | --- | --- | --- | --- | --- |
| M01 | SBR-001 | Fragrantica homepage direct HTTP | venue_value | Response exceeded initial 350 KB cap, indicating reachable but large source body. | a:no b:no c:no |
| M02 | SBR-001 | Fragrantica Baccarat Rouge 540 product direct HTTP | venue_value | Direct HTTP returned 200 with about 1.8 MB source HTML and no known block signature. | a:no b:no c:no |
| M03 | SBR-001 | Fragrantica search direct HTTP | venue_value | Direct HTTP returned 200 with about 658 KB source HTML and search page title. | a:no b:no c:no |
| M04 | SBR-001 | Parfumo homepage direct HTTP | venue_value | Direct HTTP returned 200 with about 120 KB source HTML. | a:no b:no c:no |
| M05 | SBR-001 | Guessed Parfumo product direct HTTP | negative | Guessed URL redirected to `/404`; useful as a false locator. | a:no b:no c:no |
| M06 | SBR-001 | Parfumo general search direct HTTP | venue_value | Direct HTTP returned 200 with search page, but initial results did not target Baccarat Rouge 540. | a:no b:no c:no |
| M07 | SBR-001 | Parfumo perfume search direct HTTP | hidden_venue_pointer | Direct HTTP redirected to `s_perfumes_x.php` and exposed the correct Baccarat Rouge 540 Eau de Parfum product URL. | a:no b:no c:no |
| M08 | SBR-001 | Parfumo Baccarat Rouge 540 product direct HTTP | venue_value | Direct HTTP returned 200 with about 117 KB source HTML and no known block signature. | a:no b:no c:no |
| M09 | SBR-001 | Basenotes homepage direct HTTP | access_note | Direct HTTP returned 403 Cloudflare interstitial. | a:no b:no c:no |
| M10 | SBR-001 | Basenotes search direct HTTP | access_note | Direct HTTP returned 403 Cloudflare interstitial. | a:no b:no c:no |
| M11 | SBR-001 | Basenotes homepage and search anti-block HTTP | access_note | Anti-block HTTP also returned 403 with `cf-mitigated` challenge signal. | a:no b:no c:no |
| M12 | SBR-001 | Basenotes homepage and search visible browser read | access_note | Visible browser read rendered Cloudflare security-verification text, not source content. | a:no b:no c:no |
| M13 | SBR-007 | Basenotes public search snippet mining | access_note | DuckDuckGo HTML returned anomaly/challenge pages and no usable Basenotes result links. | a:no b:branch-close c:no |

## Hidden Venue Pointers

```yaml
hidden_venue_pointer_id: HVP-001
source_move_id: M07
url: https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum
reason: >
  Parfumo internal perfume search resolved the correct product URL after a
  guessed product URL redirected to a 404 page.
```

## Screen-Light Observations

```yaml
observations:
  - observation_id: OBS-001
    source_move_id: M02
    url: https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html
    retrieval_date: 2026-06-29
    short_quote_or_summary: >
      Direct HTTP returned status 200, about 1.8 MB of source HTML, title for
      Baccarat Rouge 540, and body markers for reviews, longevity, sillage,
      rating, and perfume.
    signal_stage: venue_value
    claim_it_might_support: Fragrantica product pages are capture-preservation candidates for scent-language and performance/review substrate.
    gate_role: none
    independence_hypothesis: Fragrance-native enthusiast database; not purchase verified, but independent of major retailer PDPs.
    uncertainty_or_limits: Screen-light probe only; no packet, no review extraction, no demand verdict, and source content not parsed into fields.
  - observation_id: OBS-002
    source_move_id: M08
    url: https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum
    retrieval_date: 2026-06-29
    short_quote_or_summary: >
      Direct HTTP returned status 200, about 117 KB of source HTML, title for
      Baccarat Rouge 540 by Maison Francis Kurkdjian, and body markers for
      reviews, statements, longevity, sillage, rating, score, and scent.
    signal_stage: venue_value
    claim_it_might_support: Parfumo product pages are capture-preservation candidates for statements/reviews and performance-rating substrate.
    gate_role: none
    independence_hypothesis: Fragrance-native enthusiast database; not purchase verified, but independent of major retailer PDPs.
    uncertainty_or_limits: Screen-light probe only; exact field extraction and review-date preservation remain packet-grade Capture work.
  - observation_id: OBS-003
    source_move_id: M09
    url: https://basenotes.com/
    retrieval_date: 2026-06-29
    short_quote_or_summary: Direct HTTP returned HTTP 403 with Cloudflare interstitial/block-shell classification.
    signal_stage: access_note
    claim_it_might_support: Basenotes direct HTTP is not currently a pinned working route.
    gate_role: none
    independence_hypothesis: Access note only; no source content observed.
    uncertainty_or_limits: Public content may still be reachable by a stronger browser/anti-bot route, proxy profile, archive, or manual route.
  - observation_id: OBS-004
    source_move_id: M11
    url: https://basenotes.com/search?q=Baccarat%20Rouge%20540
    retrieval_date: 2026-06-29
    short_quote_or_summary: Anti-block HTTP returned HTTP 403 with `cf-mitigated` challenge signal.
    signal_stage: access_note
    claim_it_might_support: Basenotes anti-block HTTP is not currently a pinned working route.
    gate_role: none
    independence_hypothesis: Access note only; no source content observed.
    uncertainty_or_limits: Do not repeat anti-block HTTP without a new route fact or environment change.
  - observation_id: OBS-005
    source_move_id: M12
    url: https://basenotes.com/search?q=Baccarat%20Rouge%20540
    retrieval_date: 2026-06-29
    short_quote_or_summary: Visible browser read showed security-verification text and no source-native Basenotes content.
    signal_stage: access_note
    claim_it_might_support: Basenotes browser route remains blocked in this environment.
    gate_role: none
    independence_hypothesis: Access note only; no source content observed.
    uncertainty_or_limits: The browser wrapper reported visible text only; classify the visible security-verification page as blocked for source purposes.
  - observation_id: OBS-006
    source_move_id: M13
    url: https://duckduckgo.com/html/?q=site%3Abasenotes.com%2Ffragrances+Baccarat+Rouge+540+Maison+Francis+Kurkdjian
    retrieval_date: 2026-06-29
    short_quote_or_summary: Public search snippet mining returned anomaly/challenge pages and no usable Basenotes links.
    signal_stage: access_note
    claim_it_might_support: Search-snippet fallback did not produce a usable Basenotes locator in this run.
    gate_role: none
    independence_hypothesis: Search access note only; no Basenotes source content observed.
    uncertainty_or_limits: A different search surface or manual search could change this result.
```

## Negatives And Access Notes

- `NEG-001`: The initially guessed Parfumo product URL redirected to `/404`; the correct product URL came from Parfumo perfume search.
- `ACCESS-001`: Basenotes direct HTTP returned Cloudflare 403 for homepage and search.
- `ACCESS-002`: Basenotes anti-block HTTP returned Cloudflare `cf-mitigated` challenge pages for homepage and search.
- `ACCESS-003`: Basenotes visible browser read rendered security-verification text, not source-native content.
- `ACCESS-004`: DuckDuckGo snippet mining for Basenotes returned anomaly/challenge pages and no usable result links.

## Capture Triage

```yaml
capture_requests:
  - capture_request_id: CR-001
    source_scan: fragrance_native_db_live_probe_v0
    candidate_or_observation_ids:
      - OBS-001
    urls:
      - url: https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html
        venue: Fragrantica
        observation_supported: OBS-001
        gate_role: none
    what_capture_should_verify: >
      Preserve raw source body and verify which product-page fields can be
      extracted without losing source-visible markers for reviews, longevity,
      sillage, rating, scent-language, and page timing.
    decision_window: current forward probe window, 2026-06-29
    route_binding_state: cited_current
    screening_evidence_summary: Direct HTTP returned 200 and a large product-page HTML body with relevant substrate markers.
    uncertainty_or_access_limits: Capture owns packet route execution and field extraction; this request is not a demand verdict or Data Lake routine.
    not_requested:
      - route expansion
      - packet commitment by scanning
      - ECR, Cleaning, or Judgment work
  - capture_request_id: CR-002
    source_scan: fragrance_native_db_live_probe_v0
    candidate_or_observation_ids:
      - OBS-002
    urls:
      - url: https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum
        venue: Parfumo
        observation_supported: OBS-002
        gate_role: none
    what_capture_should_verify: >
      Preserve raw source body and verify which product-page fields can be
      extracted without losing source-visible markers for statements, reviews,
      longevity, sillage, rating, score, scent-language, and page timing.
    decision_window: current forward probe window, 2026-06-29
    route_binding_state: cited_current
    screening_evidence_summary: Direct HTTP returned 200 on the exact product page after internal perfume-search URL resolution.
    uncertainty_or_access_limits: Capture owns packet route execution and field extraction; this request is not a demand verdict or Data Lake routine.
    not_requested:
      - route expansion
      - packet commitment by scanning
      - ECR, Cleaning, or Judgment work
```

## Packet Completeness Addendum

```yaml
packet_check_date: 2026-06-29
operator_request: Check Fragrantica and Parfumo completeness; run full CloakBrowser for Basenotes.
packet_scope:
  - one Fragrantica product URL
  - one Parfumo product URL
  - one Basenotes search URL
not_claimed:
  - full fragrance database capture
  - all-product review corpus completion
  - ECR, Cleaning, Judgment, buyer proof, monitoring, or commercial readiness
```

### Fragrantica Direct HTTP Packet

```yaml
packet_id: 01KW7SGXRZHFTS372X391Z8GHV
packet_lifecycle_note: >
  This packet was written to the configured ORCA_DATA_ROOT path observed as
  F:/orca-data-lake/raw/930/01KW7SGXRZHFTS372X391Z8GHV because the environment
  variable overrode the requested scratch output. Treat this as a generated
  packet fact, not fixture admission, not routine Data Lake handoff, and not a
  source-completeness claim.
source_surface: fragrantica_product_page_direct_http
url: https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html
http_status: 200
preserved_body_bytes: 1806640
title: Baccarat Rouge 540 Maison Francis Kurkdjian perfume - a fragrance for women and men 2015
observed_source_visible_counts:
  rating_votes: 28808
  inline_review_ids: 210
  review_read_more_components: 210
  perfume_id_refs:
    - "33519"
completeness_verdict: partial_product_page_body
why_not_complete: >
  The packet preserves the current Direct HTTP response body and 210 inline
  review bodies, but it does not prove the full Fragrantica review universe was
  exhausted. The preserved body contains component and load-more vocabulary, so
  a separate endpoint/browser-exhaustion pass is required before claiming full
  review completeness.
```

### Parfumo Direct HTTP Packet

```yaml
packet_id: 01KW7SJ8F4M6ZTGVWMBB9ZVXCR
packet_lifecycle_note: Local ignored scratch packet, not fixture-admitted.
scratch_path: orca-harness/_test_runs/fragrance_native_20260629/parfumo_direct_http_packet
source_surface: parfumo_product_page_direct_http
url: https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum
http_status: 200
preserved_body_bytes: 116651
title: Baccarat Rouge 540 by Maison Francis Kurkdjian (Eau de Parfum) & Perfume Facts
observed_source_visible_counts:
  rating_count: 5176
  declared_reviews: 369
  declared_statements: 1390
  inline_review_articles: 5
  perfume_id_refs:
    - "67720"
completeness_verdict: partial_initial_page_body
why_not_complete: >
  The packet preserves the initial Direct HTTP product page and source-visible
  aggregate counts, but not the complete review or statement corpus. The body
  declares 369 reviews and 1390 statements, embeds only 5 review articles in the
  initial page, and includes JavaScript that loads more reviews through
  /action/perfume/get_reviews.php in 5-review increments.
```

### Parfumo Pagination Diagnosis Addendum

```yaml
pagination_check_date: 2026-06-29
operator_request: Diagnose Parfumo after Fragrantica current-window diagnosis.
source_packet:
  packet_id: 01KW7SJ8F4M6ZTGVWMBB9ZVXCR
  scratch_path: orca-harness/_test_runs/fragrance_native_20260629/parfumo_direct_http_packet
  preserved_body_bytes: 116651
  source_family: fragrance_native_database
  source_surface: parfumo_product_page_direct_http
product_locator: https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum
product_id: "67720"
page_hash_parameter: 7536fa6f9c01a6637a935e7717b53101
initial_page_observations:
  declared_reviews: 369
  declared_statements: 1390
  inline_review_articles: 5
  rating_count: 5176
  scent_rating: 7.7
  longevity_rating: 8.7
  sillage_rating: 8.5
  first_party_review_endpoint: /action/perfume/get_reviews.php
  first_party_statement_endpoint: /action/perfume/get_statements.php
endpoint_shape:
  reviews_post_fields:
    - f
    - n
    - t
    - o
    - full
    - p_id
    - append
    - h
  statements_post_fields:
    - f
    - n
    - t
    - o
    - p_id
    - append
    - h
  default_order: order_relevance_desc
live_probe_results:
  - route: reviews f=5 n=5
    http_status: 200
    response_bytes: 17039
    unique_review_articles: 5
    cloudflare_or_login_marker_seen: false
  - route: statements f=5 n=5
    http_status: 200
    response_bytes: 11475
    unique_statement_ids: 5
    cloudflare_or_login_marker_seen: false
  - route: reviews f=5 n=20
    http_status: 200
    response_bytes: 69691
    unique_review_articles: 20
    cloudflare_or_login_marker_seen: false
  - route: statements f=5 n=20
    http_status: 200
    response_bytes: 44897
    unique_statement_ids: 20
    cloudflare_or_login_marker_seen: false
  - route: reviews f=5 n=100
    http_status: 200
    response_bytes: 371298
    unique_review_articles: 100
    cloudflare_or_login_marker_seen: false
  - route: statements f=5 n=100
    http_status: 200
    response_bytes: 214799
    unique_statement_ids: 100
    cloudflare_or_login_marker_seen: false
capture_route_verdict: pinned_completeable_with_first_party_ajax_batches
recommended_capture_route: >
  Preserve the initial direct product page, then preserve paginated first-party
  POST responses for reviews and statements as raw batch bodies plus request
  metadata. `n=100` worked in this diagnosis and would make the 369-review /
  1390-statement corpus practical, but a future capture runner should retain a
  conservative fallback to `n=20` if the route degrades.
not_complete_yet:
  - No full 369-review or 1390-statement Parfumo corpus was captured in this addendum.
  - No endpoint response bodies from the live pagination probes were admitted as packets.
  - No ECR, Cleaning, Judgment, monitoring, or commercial-readiness claim is created.
```
### Basenotes Full CloakBrowser Packet

```yaml
packet_id: 01KW7SJNGK7PCDVTBG3XA1S4NW
packet_lifecycle_note: Local ignored scratch packet, not fixture-admitted.
scratch_path: orca-harness/_test_runs/fragrance_native_20260629/basenotes_cloakbrowser_packet
source_surface: basenotes_search_cloakbrowser_snapshot
url_requested: https://basenotes.com/search?q=Baccarat%20Rouge%20540
url_landed: https://basenotes.com/search?q=Baccarat+Rouge+540
rendered_dom_bytes: 27444
visible_text_bytes: 261
viewport_screenshot_bytes: 26357
title: Just a moment...
visible_text_result: Cloudflare security verification page, not Basenotes source content.
fragrance_markers_seen:
  review: 0
  longevity: 0
  sillage: 0
  Baccarat Rouge 540: 0
  Maison Francis Kurkdjian: 0
packet_limitation: >
  Rendered DOM still contained a residual Cloudflare challenge marker; visible
  text was an interstitial/security-verification page. Full anonymous
  CloakBrowser without proxy, stored session, credentials, or CAPTCHA solving
  did not reach Basenotes source content in this environment.
completeness_verdict: access_block_packet_only
next_route_condition: >
  Do not repeat direct HTTP, anti-block HTTP, screening browser, or anonymous
  full CloakBrowser without a new route fact. Useful new facts would be an exact
  Basenotes product URL, an approved proxy/profile route, a manual visible
  browser success, a usable archive/snippet route, or owner-supplied entitled
  bytes.
```

### Basenotes Exact Product Re-Diagnosis Addendum

```yaml
operator_question: >
  Should Basenotes wait for the Fragrantica lane structure, or should it be
  diagnosed now?
route_answer: >
  Do not wait for Fragrantica to complete before diagnosing Basenotes access.
  Wait for Fragrantica/Parfumo before building the shared projection and
  Cleaning shape, but Basenotes has a separate access bottleneck that must be
  proven independently before it can adopt the same wrapper structure.
new_route_fact:
  kind: known_exact_basenotes_product_url
  source: local code fixture evidence
  url: https://www.basenotes.com/fragrances/mojave-ghost-by-byredo.26143979/
direct_http_result:
  http_status: 403
  final_url: https://basenotes.com/fragrances/mojave-ghost-by-byredo.26143979/
  server: cloudflare
  cf_mitigated: challenge
  title: Just a moment...
  source_content_seen: false
  product_markers_seen:
    Mojave Ghost: false
    Reviews: false
br540_locator_pass:
  public_search_locator_result: no usable Basenotes BR540 product URL surfaced
  candidate_slug_direct_http_result: Cloudflare 403 challenge; no BR540 marker
  wayback_available_result: no closest snapshot for tested candidate BR540 URL variants
exact_product_cloakbrowser_packet:
  packet_id: 01KW7WT678TBFK1609QTE07B5E
  packet_lifecycle_note: Local ignored scratch packet, not fixture-admitted.
  scratch_path: orca-harness/_test_runs/fragrance_native_20260629/basenotes_exact_product_cloakbrowser_packet
  source_surface: basenotes_exact_product_cloakbrowser_snapshot
  url_requested: https://www.basenotes.com/fragrances/mojave-ghost-by-byredo.26143979/
  url_landed: https://basenotes.com/fragrances/mojave-ghost-by-byredo.26143979/
  rendered_dom_bytes: 27498
  visible_text_bytes: 262
  viewport_screenshot_bytes: 26232
  title: Just a moment...
  visible_text_result: Cloudflare security verification page, not Basenotes source content.
  receipt_warning: residual Cloudflare challenge marker
  integrity_note: >
    The packet metadata recorded `access_blocked: false`, but the rendered
    title and visible text show an interstitial. Under the source-capture
    playbook's rendered-access honesty rule, this is classified as blocked
    source access, not a successful source read.
diagnosis_verdict: no_working_pin_current_environment_reconfirmed_exact_product
why_this_matters: >
  The failure is no longer just a Basenotes search-page or BR540 locator issue.
  A known exact product URL also fails through direct HTTP and anonymous
  CloakBrowser, so Basenotes should remain CSB/Scanning value plus access-note,
  not Capture-wrapper work, until a materially different access route is proven.
next_route_condition: >
  Re-probe only with a new access fact: approved proxy/profile route, stored
  manual browser session success, owner-supplied entitled/rendered bytes, a
  verified exact BR540 URL that returns source-visible content, or a usable
  archive/snippet route that exposes product or thread content rather than an
  access interstitial.
```

### Basenotes Authorized Chrome Extension Route Addendum

```yaml
operator_authorization: >
  Owner explicitly authorized Chrome extension/profile access for Basenotes
  diagnosis after anonymous direct HTTP and CloakBrowser routes failed.
access_route:
  method: chrome_extension_profile_browser_read
  posture: profile_backed_visible_browser_access
  non_claims:
    - not anonymous automation
    - not direct_http
    - not CloakBrowser
    - not login-state assertion
    - not complete Basenotes database capture
known_product_probe:
  url_requested: https://www.basenotes.com/fragrances/mojave-ghost-by-byredo.26143979/
  url_landed: https://basenotes.com/fragrances/mojave-ghost-by-byredo.26143979
  title: Mojave Ghost by Byredo - Basenotes
  visible_text_length: 3804
  source_content_seen: true
  product_fields_seen:
    - perfume house
    - parent company
    - parent at launch
    - fragrance notes split by head, heart, and base
    - latest review cards
    - review sentiment breakdown
    - same-house links
  review_window_seen:
    declared_visible_total: 18
    visible_sentiment_breakdown: 4 Positive / 8 Neutral / 6 Negative
basenotes_search_probe:
  query: Baccarat Rouge 540
  url_landed: https://basenotes.com/search/1023503/?q=Baccarat+Rouge+540&o=relevance
  title: "Search results for query: Baccarat Rouge 540 | Basenotes"
  visible_text_length: 5359
  source_content_seen: true
  useful_result_classes:
    - current forum mentions
    - exact BR540 Extrait thread
    - appraisal/authenticity thread
    - scent-of-day and weekend-sync mentions
br540_forum_thread_probe:
  url_page_1: https://basenotes.com/threads/baccarat-rouge-540-extrait.571027/
  url_page_2: https://basenotes.com/threads/baccarat-rouge-540-extrait.571027/page-2
  title_page_1: Baccarat Rouge 540 Extrait | Basenotes
  title_page_2: Baccarat Rouge 540 Extrait | Page 2 | Basenotes
  start_date: 2026-01-01
  latest_observed_post_date: 2026-02-10
  pages_observed: 2
  posts_observed: 24
  visible_text_lengths:
    page_1: 12798
    page_2: 5560
  tags_seen:
    - baccarat
    - baccarat rouge 540
    - extrait
    - rouge
  signal_categories_seen:
    - purchase intent
    - price objection
    - EDP versus extrait comparison
    - anosmia or nose-blindness complaints
    - projection and scent-cloud language
    - clone substitution and dupe comparisons
    - Amazon or third-party buying discussion
    - headache or cloying complaints
    - compliments and public reaction language
  similar_thread_markers_seen:
    - BR540 scented body oil authenticity/appraisal thread from 2026-04
    - BR540 Extrait authenticity/appraisal thread from 2024-09
    - BR540 news/discussion thread from 2024-04 with 68 replies and 13K views
directory_product_locator_probe:
  directory_home_accessible: true
  product_search_form_seen: true
  query: Baccarat Rouge 540
  result: unresolved
  observed_failure: >
    The Directory product search remained at `Searching Perfumes`; one direct
    GET using the form query contract hung long enough to reset the Chrome
    control session. No BR540 Basenotes product-page URL was pinned in this run.
capture_route_verdict: profile_backed_capture_probe_pinned_for_forum_and_known_product_surfaces
why_this_matters: >
  Basenotes should no longer be treated as globally no-pin. It is blocked for
  anonymous direct/CloakBrowser capture, but authorized Chrome/profile access
  reaches source-visible product and forum content. Capture can proceed only if
  the packet clearly records the profile-backed/human-led route and does not
  claim anonymous repeatability.
next_capture_step: >
  Build or run a profile-backed/human-led source packet path for Basenotes forum
  and known-product pages: preserve rendered DOM, visible text, screenshot, final
  URL, title, route posture, profile/session non-claims, and pagination state.
  Keep product-directory search as an unresolved locator gap until it returns
  product cards or a stable BR540 product URL.
```

### Basenotes Additional Chrome Route Pins And Lightweight Capture Plan

```yaml
operator_request: >
  Probe and pin the additional Basenotes routes surfaced from the Chrome-readable
  BR540 thread/search path, then plan lower-ceremony access and capture options
  while the Fragrantica lane settles.
access_route:
  method: chrome_extension_profile_browser_read
  posture: profile_backed_visible_browser_access
  still_blocked_routes:
    - anonymous direct_http
    - anonymous anti-block HTTP
    - anonymous CloakBrowser
additional_pinned_surfaces:
  - route_id: basenotes_tag_baccarat_rouge_540
    url: https://basenotes.com/tags/baccarat-rouge-540/
    title: baccarat rouge 540 | Basenotes
    source_visible: true
    visible_text_length: 3079
    route_value: discovery index for BR540-tagged Basenotes content
    observed_links:
      - https://basenotes.com/threads/baccarat-rouge-540-extrait.571027/
      - https://basenotes.com/threads/is-my-baccarat-rouge-540-extrait-real.555383/
      - https://basenotes.com/threads/is-my-baccarat-real.549626/
      - https://basenotes.com/threads/best-place-online-to-purchase-baccarat.523600/
    capture_note: >
      Use as a bounded discovery seed, not as proof that every linked page was
      captured or that tag ordering is complete.
  - route_id: basenotes_body_oil_legit_check_thread
    url: https://basenotes.com/threads/legit-check-mfk-baccarat-rouge-540-scented-body-oil-70ml-atomizer-question.572639/
    title: Legit Check - MFK Baccarat Rouge 540 Scented Body Oil (70ml) - Atomizer Question | Basenotes
    source_visible: true
    visible_text_length: 6673
    observed_post_range: 1-3
    observed_date_range: 2026-04-15 to 2026-04-17
    tags_seen:
      - atomizer
      - br540
      - mfk
      - oil
      - perfumed oil
      - question
    route_value: authenticity/appraisal and packaging-detail demand-adjacent thread
  - route_id: basenotes_baccarat_rouge_540_extrait_real_thread
    url: https://basenotes.com/threads/is-my-baccarat-rouge-540-extrait-real.555383/
    title: Is My Baccarat Rouge 540 Extrait Real? | Basenotes
    source_visible: true
    visible_text_length: 6761
    observed_post_range: 1-6
    observed_date_range: 2024-09-04 to 2024-11-06
    tags_seen:
      - baccarat
      - baccarat rouge 540
      - extrait
      - real
      - rouge
    route_value: authenticity/appraisal, seller-source, attachment-dependent evidence, and performance concern thread
    media_note: >
      This thread includes visible attachment metadata. A raw page packet can
      preserve DOM/screenshot/link references, but image-level authenticity work
      needs explicit media preservation and must not be inferred from text alone.
  - route_id: basenotes_baccarat_rouge_540_news_discussion_thread
    url_page_1: https://basenotes.com/threads/baccarat-rouge-540-just-read-about-it-in-the-news.551237/
    url_page_4: https://basenotes.com/threads/baccarat-rouge-540-just-read-about-it-in-the-news.551237/page-4
    title: Baccarat Rouge 540 , just read about it in the news ? | Basenotes
    source_visible: true
    pages_observed: 4
    observed_post_range: 1-69
    observed_date_range: 2024-04-18 to 2024-09-21
    visible_text_lengths:
      page_1: 15959
      page_4: 10443
    route_value: media/status-symbol diffusion discussion with high reply/view context
    capture_note: >
      Page navigation is deterministic with `/page-N`; a complete packet needs
      pages 1 through 4, not only first/latest page snapshots.
capture_options_ranked:
  - option: selected_url_profile_packet
    rank: 1
    description: >
      Use Chrome/profile access for a small URL list: known product pages, tag
      pages, and selected forum pages. Preserve rendered DOM, visible text,
      screenshot, final URL, title, route posture, and pagination state.
    why: smallest complete route that captures what anonymous routes cannot reach
  - option: search_or_tag_seed_then_selected_capture
    rank: 2
    description: >
      Use Basenotes tag pages or forum search only to discover candidate URLs,
      then capture selected pages as separate source packets.
    why: useful for Scanning, but discovery output must not be confused with full capture
  - option: product_directory_capture
    rank: 3
    description: >
      Keep Directory/product lookup as an unresolved route. Re-probe only if the
      search form returns stable product cards or a known product URL is supplied.
    why: current directory search hung and is weaker than tag/thread routes for immediate signal capture
  - option: full_basenotes_crawler
    rank: eliminated
    description: Avoid broad crawling, guessed IDs, or route expansion before selected URL packets work.
    why: high lock-in and unnecessary for current CSB/Capture proof
  - option: anonymous_route_retry
    rank: eliminated
    description: Avoid repeated anonymous direct HTTP or CloakBrowser attempts without a new access fact.
    why: already failed across direct, anti-block, search-page, and exact-product probes
minimal_packet_contract:
  required_raw_artifacts:
    - rendered_dom_html
    - visible_text_txt
    - viewport_or_fullpage_screenshot_png
    - method_metadata_json
  required_route_fields:
    - source_family=fragrance_native_database
    - source_surface=basenotes_profile_backed_thread_or_product
    - access_route=chrome_extension_profile_browser_read
    - profile_backed_access=true
    - anonymous_repeatability=false
    - final_url
    - title
    - capture_timestamp
    - pagination_scope
    - login_or_reply_wall_visible
  extraction_after_raw_packet:
    - product/review fields for known product pages
    - thread/post metadata for forum pages
    - signal tags such as purchase_intent, price_objection, authenticity, performance_complaint, dupe_comparison, and media_diffusion
next_action_recommendation: >
  Build or run the smallest profile-backed source-packet runner for selected
  Basenotes URLs first. Do not wait for Fragrantica to decide access posture;
  do wait for Fragrantica/Parfumo before normalizing shared review projections.
```

## Route Pins
| Pin ID | Source | Step 0 access classification | Signal substrate | Cheapest working route | Verdict | Re-probe trigger |
| --- | --- | --- | --- | --- | --- | --- |
| PIN-001 | Fragrantica | publicly-viewable public web content | large product-page HTML plus search HTML | `direct_http` with at least 2 MB cap for product pages | pinned_for_capture_probe | route returns block shell, body degrades, product markers disappear, or packet field extraction cannot preserve source-visible content |
| PIN-002 | Parfumo | publicly-viewable public web content | product-page HTML; perfume-search locator route | `direct_http`; resolve exact product URL through `s_perfumes_x.php` when needed | pinned_for_capture_probe | route returns block shell, product URL changes, search locator changes, or packet field extraction cannot preserve source-visible content |
| PIN-003 | Basenotes | publicly-viewable through authorized Chrome/profile route, bot-mitigated for anonymous automation | source content reached for known product, tag, search, appraisal/authenticity, and BR540 forum surfaces; directory product locator unresolved | `chrome_extension_profile_browser_read` / human-led packet route | profile_backed_capture_probe_pinned_for_selected_product_tag_and_forum_surfaces | Chrome/profile route blocks, login wall appears, thread/product/tag markers disappear, directory product locator starts returning stable product URLs, or a non-profile route becomes available |

## Candidate Decision

```yaml
candidate_decision:
  closeout_state: capture_preservation_plus_profile_backed_basenotes_probe
  independent_origins_seen:
    - Fragrantica product page substrate reachable by direct HTTP
    - Parfumo product page substrate reachable by direct HTTP
    - Basenotes product, tag, search, appraisal/authenticity, and forum substrates reachable by authorized Chrome/profile route
  reason: >
    The probe found two direct-HTTP preservation-worthy public product-page
    substrates and one high-value Basenotes substrate that is blocked for
    anonymous automation but reachable through an authorized Chrome/profile
    route. This supports packet-grade preservation for Fragrantica and Parfumo
    by direct route, plus a separate profile-backed/human-led Basenotes capture
    probe. It is not demand proof, not full database capture, and not an
    anonymous Basenotes capture route.
```

## Closeout

`capture_preservation_plus_profile_backed_basenotes_probe`.

Fragrantica is pinned as a direct-HTTP product-page preservation route and current-window review substrate, but it is not complete review-corpus capture. Parfumo is pinned as a direct product-page plus first-party AJAX pagination route for a future complete reviews/statements capture, but this addendum did not run the full 369-review / 1390-statement corpus. Basenotes remains blocked for anonymous direct HTTP, anti-block HTTP, screening browser, search-page CloakBrowser, and known exact-product CloakBrowser, but authorized Chrome/profile access reached source-visible product, tag, search, appraisal/authenticity, and BR540 forum-thread content. One Fragrantica packet landed in the configured ORCA data root during the completeness check; that is a generated packet fact only, not fixture admission, routine Data Lake handoff, ECR, Cleaning, Judgment, monitoring, commercial readiness, full-database crawling, or anonymous Basenotes repeatability.
