# Orca Fragrance-Native Database Live Probe v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: CSB-first live probe and capture-route pinning receipt for fragrance-native databases.
use_when:
  - Seeding Capture from a bounded Scanning/probe pass over Fragrantica, Parfumo, and Basenotes.
  - Reconstructing why Fragrantica and Parfumo are preservation candidates, and the Basenotes capture route (anonymous egress Cloudflare-challenged; residential-proxy CloakBrowser pinned 2026-06-30 -- see the Proxy Route Verification Addendum).
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
  - The Parfumo Chrome-extension/user-visible browser route stops reaching real product DOM, direct HTTP/AJAX becomes reliably reachable again, or the targeted-sample objective changes.
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

This bounded `broad_scout_return` checked three fragrance-native database frontiers from the CSB board: Fragrantica, Parfumo, and Basenotes. It included exact-query discovery for Basenotes and Parfumo URL resolution, venue evaluation by direct HTTP, anti-block HTTP, and visible browser reads, hidden venue pointers for correct Parfumo product routing, negatives and access notes for Basenotes, and recency/current-state preservation pressure where public product pages returned source-visible body markers. Recommended main deepening: run packet-grade preservation for Fragrantica and Parfumo via their pinned direct-HTTP product routes, and for Basenotes via the residential-proxy CloakBrowser route now pinned 2026-06-30 (anonymous routes are Cloudflare-challenged; see the Proxy Route Verification Addendum).

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

### Parfumo Chrome Extension Route Re-Pin Addendum

```yaml
route_repin_date: 2026-06-30
operator_question: >
  Diagnose whether Parfumo can use a non-extension route, or whether the current
  targeted high-value capture route should use the Chrome extension/user-visible
  browser session after the operator verified the page works in their browser.
current_access_diagnosis:
  direct_http_and_first_party_ajax:
    status: blocked_in_current_environment
    notes: >
      The June 29 direct/AJAX route remains a historical route fact, but current
      probes with the correct Parfumo product id and hash returned Cloudflare
      access-denial/block shells rather than source content.
  anonymous_rendered_browser:
    status: blocked_in_current_environment
    notes: >
      Anonymous rendered capture landed on a Cloudflare "Just a moment" /
      security-verification page, not Parfumo source content.
  proxied_rendered_browser:
    status: blocked_in_current_environment
    notes: >
      The owner-authorized residential proxy profile also landed on the
      Cloudflare verification page for Parfumo in this run.
  chrome_extension_user_visible_browser:
    status: working_current_route
    notes: >
      The Codex Chrome extension route using the operator's visible Chrome
      browser loaded the real Parfumo product DOM. No browser cookies, storage
      state, or Cloudflare clearance values were exported into the saved receipt.
observed_chrome_extension_facts:
  product_id: "67720"
  declared_reviews: 369
  declared_statements: 1390
  rating_display: "7.7 / 10"
  rating_count_observed: 5179
  first_party_review_endpoint_seen: /action/perfume/get_reviews.php
  first_party_statement_endpoint_seen: /action/perfume/get_statements.php
  scrubbed_receipt_path: orca-harness/_scratch/parfumo_chrome_extension_probe_20260630_2000/route_receipt.json
target_scope_correction:
  status: full_corpus_no_longer_active_target
  target: targeted_current_window_plus_high_value_review_statement_sample
  emphasis:
    - recency_focused_latest_reviews_and_statements
    - source_visible_high_low_rating_buckets_where_present
    - preserve aggregate declared corpus counts as context while residualizing uncaptured corpus
  rating_scale_note: >
    Operator shorthand such as 4-star / 5-star / 1-star maps here to
    source-visible rating buckets, not an assumed Parfumo star scale. Preserve
    Parfumo's own review fields and labels as raw facts, then bucket in
    projection only when the source-visible values support it.
route_verdict: >
  For the current Parfumo targeted-corpus lane, use the Chrome extension /
  user-visible browser route as the primary capture route. Preserve the initial
  rendered DOM/visible text/screenshot and pursue bounded same-tab first-party
  page/AJAX interactions only for targeted high-value review/statement coverage.
  Direct HTTP/AJAX remains an opportunistic canary/fallback if it becomes
  reachable again, not a success dependency. Anonymous or proxied non-extension
  rendered capture is not ruled out forever, but it is currently blocked and
  should not gate this lane. Full 369-review / 1390-statement exhaustion is not
  the active target unless separately re-authorized.
safety_boundaries:
  - no cookie export or clearance-token transfer
  - no CAPTCHA solving service
  - no stealth/fingerprint-spoofing work
  - no proxy rotation or retry storm
  - no live capture without current owner network authorization
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

### Basenotes Proxy Route Verification Addendum (2026-06-30)

```yaml
verification_date: 2026-06-30
operator_request: Test Basenotes with CloakBrowser; if blocked, proxied CloakBrowser (one residential profile).
method: >
  Existing CloakBrowser adapter (no evasion built); proxy referenced by label only; scratch
  only, nothing written to the data lake.
egress_direct_anonymous:
  ip: 121.7.247.114
  geo: Singapore / SG
  network: AS9506 Singtel
  outcome: challenged_by_cloudflare
egress_residential_proxy:
  label: reddit-res-01
  category: residential_rotating
  ip_observed: 72.89.223.118
  geo: New York / US
  network: AS701 Verizon
  outcome: renders_real_content
results:
  anonymous_cloakbrowser: access_blocked (residual_challenge_marker; title "Just a moment..."; ~261 chars)
  proxy_cloakbrowser_product_page: no_block_marker; 3/3 clean repeat runs; ~3825 chars; title "Mojave Ghost by Byredo - Basenotes"
  proxy_cloakbrowser_homepage: no_block_marker (generalizes beyond a single product page)
  url_verified: https://www.basenotes.com/fragrances/mojave-ghost-by-byredo.26143979/
finding: >
  The block is egress-reputation, not a hard wall. This host's direct Singapore Singtel egress
  is Cloudflare-challenged (likely flagged from prior probe volume plus geo mismatch on a
  US-leaning site); a fresh US residential proxy exit renders real content reliably. Basenotes
  capture route = proxied CloakBrowser through reddit-res-01.
review_surface_resolved: >
  RESOLVED by a 2026-06-30 DOM inspection: the reviews ARE on the product page, embedded as
  schema.org JSON-LD Review objects (author, reviewBody, reviewRating.ratingValue, datePublished)
  plus HTML `fragreview*` containers; this product showed "18 Reviews". The earlier "review bodies
  not on the page" reading was a visible-text-extraction artifact (a 220-char viewport filter on the
  text extractor), not reality -- the rendered DOM carries them. The FULL-corpus surface is the
  `/fragrances/<slug>/reviews/` sub-URL plus sentiment tabs (`/reviews/positive|neutral|negative/`),
  each reachable via the same proxy route. Projection extraction = parse the JSON-LD review array
  from the captured rendered DOM (and fetch the /reviews/ sub-URL for the complete set); no tab-click.
not_claimed:
  - full Basenotes review corpus captured
  - run-to-run guarantee (Cloudflare is probabilistic; treat an occasional challenge as retry/limitation)
  - fixture admission or Data Lake handoff
```

### Basenotes Capture-Route Re-climb Addendum (2026-07-16)

```yaml
verification_date: 2026-07-16
owner_authorization: >
  One additional proof using the user-cleared persistent Chrome tab after the
  bounded fresh-context proof returned a visible Cloudflare gate.
target_url: https://basenotes.com/fragrances/mojave-ghost-by-byredo.26143979
fresh_route_observations:
  current_proxy_wrapper_preflight: >
    failed before network because profile metadata for reddit-res-01 was absent;
    the historical profile was not revived or replaced with an invented proxy
  direct_public: 403 Cloudflare challenge; insufficient product/review evidence
  no_proxy_cloakbrowser: challenge-only; packet 01KXKD38XB4YDVMY45XCK95581
  fresh_headed_chrome: >
    challenge-only after 15-second settle; 261 visible-text bytes; packet
    01KXKDHJ4DY984MDB161QSRR31
  user_cleared_persistent_chrome: >
    sufficient public product page after the user personally completed the
    visible Cloudflare verification; 87268 rendered-DOM bytes, 3820 visible-text
    bytes, exact product path, Product JSON-LD, review, and reviewBody present
proof_packet:
  packet_id: 01KXKE3KFBY0J8XNQ4FJC4PACR
  source_family: fragrance_native_database
  source_surface: basenotes_product_page_user_cleared_persistent_chrome_current_window
  preserved_files: 4
  cookie_or_credential_export: false
  proxy_used: false
downstream_proof:
  projection_review_cards: 6
  cleaning_silver_records: 6
  physically_verified_silver_records: 6
  ecr_record_id: 01KXKFVKXJXS3TJH4X7J1ZGC9F.json
  ecr_posture_siblings: 4
  ecr_member_hashes_verified: 4
  ecr_acknowledged: true
  ecr_identity: resolved
  ecr_inspectability: inspectable_verifiable
  ecr_source_visibility: current_capture_only; does_not_clear_source_visibility
  ecr_timing: unknown_cutoff; does_not_clear_pre_cutoff
selected_route: >
  User-cleared persistent visible Chrome public-page export, followed by the
  fail-closed four-file bundle runner. The user completes the access gate; the
  runner never automates it and never reads or exports cookies, credentials, or
  browser-profile data.
retired_executable_default: >
  CloakBrowser plus reddit-res-01 is historical evidence only. Its missing
  profile metadata and lack of fresh replacement proof make it ineligible as the
  current executable default.
headless_route_posture: >
  failed on 2026-07-16 in one separately owner-authorized probe using the same
  isolated profile after the user cleared Cloudflare while headed. Headless Chrome
  returned HTTP 403, title "Just a moment...", 261 visible-text bytes, and no
  Product/review/reviewBody markers. The caller-bound path appeared only through
  the requested URL. A separate direct headed CloakBrowser attempt remained in
  Cloudflare's human-verification loop after the user checked the box, so it never
  established cleared state and was not relaunched headlessly. Do not promote
  headless persistence from either browser route.
not_claimed:
  - unattended reliability
  - site-wide or full-review-corpus completeness
  - headless persistence
  - scale or production readiness
  - CAPTCHA automation or agent-performed solving
```
## Route Pins
| Pin ID | Source | Step 0 access classification | Signal substrate | Cheapest working route | Verdict | Re-probe trigger |
| --- | --- | --- | --- | --- | --- | --- |
| PIN-001 | Fragrantica | publicly-viewable public web content | large product-page HTML plus search HTML | `direct_http` with at least 2 MB cap for product pages | pinned_for_capture_probe | route returns block shell, body degrades, product markers disappear, or packet field extraction cannot preserve source-visible content |
| PIN-002 | Parfumo | publicly-viewable public web content, but bot-mitigated for anonymous/proxied automation in the current environment | product-page DOM plus first-party review/statement AJAX hooks observed in the operator's visible Chrome browser | `chrome_extension_user_visible_rendered_session`; direct HTTP/AJAX is canary/fallback only | pinned_for_current_targeted_capture_route | Chrome extension route returns Cloudflare/block shell, product DOM markers disappear, AJAX hook shape changes, owner withdraws live-browser authorization, target-sampling objective changes, or direct HTTP/AJAX becomes reliably reachable again |
| PIN-003 | Basenotes | publicly-viewable; fresh anonymous/fresh-browser contexts are Cloudflare-challenged, while a user-cleared persistent visible Chrome tab reaches the page | product-page HTML with reviews embedded as schema.org JSON-LD (author/reviewBody/rating/date) + HTML containers; full corpus at `/reviews/` + sentiment sub-URLs | user-cleared persistent visible Chrome four-file public-page export; no cookie, credential, profile, or proxy export | pinned_for_current_user_assisted_capture_route (2026-07-16: one packet projected to 6 Cleaning/Silver records and all 6 passed physical-source verification) | persistent visible Chrome returns a challenge after user clearance, product URL/JSON-LD markers change, export metadata cannot prove no secret/profile export, owner withdraws user-assisted authorization, or an isolated headless route is separately proven |

## Candidate Decision

```yaml
candidate_decision:
  closeout_state: capture_preservation_only
  independent_origins_seen:
    - Fragrantica product page substrate reachable by direct HTTP
    - Parfumo product page substrate reachable by visible Chrome extension route
    - Basenotes product page substrate reachable via user-cleared persistent visible Chrome (2026-07-16)
  reason: >
    The probe found three preservation-worthy public product-page substrates:
    Fragrantica via direct HTTP, Parfumo via the operator-visible Chrome
    extension route (the June 29 direct/AJAX route is demoted to canary/fallback
    after current Cloudflare blocks), and Basenotes via the user-cleared
    persistent visible Chrome bundle route (verified 2026-07-16). This supports packet-grade
    preservation requests for all three; it is not demand proof, not full
    database capture, and not full review-corpus extraction.
```

## Closeout

`capture_preservation_only`.

Fragrantica is pinned as a direct-HTTP product-page preservation route and current-window review substrate, but it is not complete review-corpus capture. Parfumo's June 29 direct product-page plus first-party AJAX route is retained as historical evidence and a future canary/fallback, but the current targeted high-value route is the Chrome extension / operator-visible browser route; this addendum does not target or claim the full 369-review / 1390-statement corpus. Basenotes is now pinned (2026-07-16) to the user-cleared persistent visible Chrome bundle route: fresh direct, no-proxy CloakBrowser, fresh headed Chrome, and same-cleared-profile headless Chrome contexts were Cloudflare-challenged, while the owner-cleared persistent Chrome tab produced one mechanically sufficient packet whose six projected review cards became six physically verified Cleaning/Silver records. A separate direct headed CloakBrowser attempt could not progress beyond Cloudflare's human-verification loop even after the user checked the box, so no cleared CloakBrowser state existed for a valid headless-reuse test. The 2026-06-30 residential-proxy CloakBrowser observation remains historical evidence, not the executable default, because `reddit-res-01` currently lacks registered profile metadata. One Fragrantica packet landed in the configured ORCA data root during the completeness check; that is a generated packet fact only, not fixture admission, routine Data Lake handoff, ECR, Cleaning, Judgment, monitoring, commercial readiness, or full-database crawling.
