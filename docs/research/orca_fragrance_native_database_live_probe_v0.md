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

## Route Pins
| Pin ID | Source | Step 0 access classification | Signal substrate | Cheapest working route | Verdict | Re-probe trigger |
| --- | --- | --- | --- | --- | --- | --- |
| PIN-001 | Fragrantica | publicly-viewable public web content | large product-page HTML plus search HTML | `direct_http` with at least 2 MB cap for product pages | pinned_for_capture_probe | route returns block shell, body degrades, product markers disappear, or packet field extraction cannot preserve source-visible content |
| PIN-002 | Parfumo | publicly-viewable public web content | product-page HTML; perfume-search locator route | `direct_http`; resolve exact product URL through `s_perfumes_x.php` when needed | pinned_for_capture_probe | route returns block shell, product URL changes, search locator changes, or packet field extraction cannot preserve source-visible content |
| PIN-003 | Basenotes | publicly-viewable but bot-mitigated in current environment | source content not reached; Cloudflare challenge seen across direct, anti-block, browser, and search-snippet routes | none pinned | no_working_pin_current_environment | new anti-bot/proxy route, manual visible-browser success, usable archive/snippet locator, or owner-supplied entitled bytes |

## Candidate Decision

```yaml
candidate_decision:
  closeout_state: capture_preservation_only
  independent_origins_seen:
    - Fragrantica product page substrate reachable by direct HTTP
    - Parfumo product page substrate reachable by direct HTTP
  reason: >
    The probe found two preservation-worthy public product-page substrates and
    one high-value but currently blocked source. This supports packet-grade
    preservation requests for Fragrantica and Parfumo only, not demand proof,
    not full database capture, and not a Basenotes capture route.
```

## Closeout

`capture_preservation_only`.

Fragrantica and Parfumo are pinned as direct-HTTP product-page preservation routes, but neither is complete review-corpus capture. Basenotes is explicitly not pinned in this environment; direct HTTP, anti-block HTTP, screening browser, and full anonymous CloakBrowser all failed to reach source content. One Fragrantica packet landed in the configured ORCA data root during the completeness check; that is a generated packet fact only, not fixture admission, routine Data Lake handoff, ECR, Cleaning, Judgment, monitoring, commercial readiness, or full-database crawling.
