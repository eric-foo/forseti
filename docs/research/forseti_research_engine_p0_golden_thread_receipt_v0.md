# Forseti Research Engine P0 Golden Thread Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Executed P0 research receipt
scope: >
  One bounded Imaginary Authors / Dipped in Chocolate scan-to-Capture golden
  thread across two independent demand-origin source families, stopping before
  ECR, Cleaning, Judgment, or Company Surface materialization.
use_when:
  - Verifying the first executed Research Engine P0 golden thread.
  - Inspecting the paired v1 scan receipt, terminal Capture lifecycle, packet evidence, and cost/yield rows.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_research_engine_p0_capture_request_lifecycle_v0.json
  - docs/research/forseti_research_engine_first_peach_repeatability_receipt_v0.md
  - docs/research/forseti_research_engine_p0_golden_thread_commission_v0.md
  - docs/research/forseti_research_engine_god_tier_strategy_v0.md
stale_if:
  - Either referenced Data Lake packet fails hash/schema verification.
  - Scan receipt v1 or capture-request lifecycle v0 changes.
```

## Currentness

This remains the historical first-run P0 baseline. The later First Peach
repeatability receipt compares against it; it does not supersede or rewrite the
evidence from this run.

## Result

`P0_EXECUTED_WITH_TWO_HANDOFF_READY_SOURCE_FAMILIES`.

The run reused the existing Imaginary Authors CSB chain and selected one narrow
decision context: whether current independent source activity around `Dipped in
Chocolate` merits preserving a low-commitment continuation / resale-interest
candidate. Parfumo and Reddit each produced a distinct, schema-valid,
hash-verified Source Capture Packet. This is an executed P0 golden thread, not a
GT, MGT, demand-proof, or readiness claim.

## Scan Intake Receipt

```yaml
scan_receipt_version: 1
commission_id: forseti_research_engine_p0_imaginary_authors_20260716
scan_date: 2026-07-16
mode: forward
subject: Imaginary Authors / Dipped in Chocolate
market_or_geography: US indie fragrance, public-web current state
source_context_status: SOURCE_CONTEXT_READY
run_caps:
  max_screening_moves_total: 6
  max_exact_queries_total: 3
screening_moves_used: 4
exact_queries_used: 3
hidden_venue_pointers: 0
capture_requests: 2
closeout_state: candidate_ready_for_next_lane
```

## Broad Scout Return

The bounded `broad_scout_return` checked two public buyer-language frontiers,
ran three exact queries, evaluated venue value, accounted for hidden venue
pointers, preserved negatives and access notes, and prioritized current-state
source drift. Recommended main deepening was one Dipped in Chocolate Parfumo
page plus one recent exact Reddit resale thread. The scout did not decide
demand, bind Capture routes, or authorize downstream use.

## CSB Board Intake

Board source: `docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md`.

Rows consumed as route map: SBR-002, SBR-005, SBR-006, and SBR-007.

## Exact Query Discovery Ledger

| Query ID | Query text | Intent | Result class | Next-route decision |
| --- | --- | --- | --- | --- |
| EQ-001 | `site:reddit.com/r/fragrance "Dipped in Chocolate" "Imaginary Authors"` | Find independent product-specific buyer language. | candidate_surface | Preserve one bounded Reddit thread route; do not count cross-post duplicates. |
| EQ-002 | `site:reddit.com/r/fragrance "First Peach of the Season" "Imaginary Authors"` | Test a fresher launch thread for the existing candidate family. | candidate_surface | Keep as comparison only; the P0 decision remains Dipped in Chocolate. |
| EQ-003 | `site:reddit.com "Imaginary Authors" "A Little Secret" perfume` | Check adjacent IA launch discussion without widening the target. | duplicate_or_adjacent | Stop expansion; retain Dipped in Chocolate target. |

## Venue Evaluation Move Log

| Move | CSB row(s) | Frontier | Value class | What happened | Stop check |
| --- | --- | --- | --- | --- | --- |
| M01 | SBR-005 | Parfumo Dipped in Chocolate product page | candidate_surface | Existing fragrance-native route remained public and product-specific. | a:no b:no c:no |
| M02 | SBR-005, SBR-006 | Reddit Dipped in Chocolate search | candidate_surface | Product review, resale, and purchase-language threads surfaced; cross-posts were not overcounted. | a:no b:no c:no |
| M03 | SBR-002 | Retail and owned-source context | corroboration_only | Existing retail/owned rows remained non-independent corroboration and were not commissioned. | a:no b:branch-close c:no |
| M04 | SBR-007 | Exact old Reddit thread route | route_ready | One June 2026 resale thread was selected as the fresh bounded Capture unit. | a:no b:no c:stop-cap-reached |

## Hidden Venue Pointers

None. The run emitted `hidden_venue_pointers: 0`; it used two already-pinned
public source-family routes and created no registry, atlas, or standing map.

## Observations

```yaml
observation_id: OBS-P0-001
source_move_id: M01
url: https://www.parfumo.com/Perfumes/Imaginary_Authors/dipped-in-chocolate
retrieval_date: 2026-07-16
short_quote_or_summary: >
  The public Parfumo product page returned HTTP 200 and preserved the Dipped in
  Chocolate product identity plus review, statement, and rating surface markers.
signal_stage: candidate_support
claim_it_might_support: independent fragrance-native buyer-response context for a low-commitment continuation candidate
gate_role: demand_origin
independence_hypothesis: fragrance-native database source family, independent of Reddit and owned/retail pages
uncertainty_or_limits: direct HTTP preserves the current page only; no full review or statement corpus was captured
```

```yaml
observation_id: OBS-P0-002
source_move_id: M04
url: https://old.reddit.com/r/fragranceswap/comments/1u5qg1g/wts_mancera_jousset_missing_person_imaginary/
retrieval_date: 2026-07-16
short_quote_or_summary: >
  A June 2026 public resale post listed Imaginary Authors Dipped in Chocolate as
  discontinued, 50 mL, about 95 percent full, at USD 110; six comment nodes were
  mechanically consolidated, including source-visible removed states.
signal_stage: candidate_support
claim_it_might_support: independent current resale-market activity around a discontinued SKU
gate_role: demand_origin
independence_hypothesis: Reddit thread source family, independent of Parfumo and owned/retail pages
uncertainty_or_limits: one seller listing is not a completed sale, price validation, broad market demand, or source completeness
```

## Negatives And Access Notes

- `NEG-P0-001`: Multiple Reddit cross-posts repeating the same review were not counted as independent origins.
- `ACCESS-P0-001`: Parfumo's rendered-session route remains primary for targeted samples; the cheaper direct-HTTP canary returned real caller-bound content in this run, so no rendered escalation was needed.
- `ACCESS-P0-002`: Reddit used one exact public old-Reddit thread only; no subreddit crawl, profile read, link following, retry, login, or commercial API route was used.

## Capture Triage

```yaml
capture_request_id: cr_p0_parfumo
source_scan: forseti_research_engine_p0_imaginary_authors_20260716
candidate_or_observation_ids:
  - OBS-P0-001
urls:
  - url: https://www.parfumo.com/Perfumes/Imaginary_Authors/dipped-in-chocolate
    venue: Parfumo
    observation_supported: OBS-P0-001
    gate_role: demand_origin
what_capture_should_verify: product identity plus current review, statement, and rating surface markers with packet-grade provenance
decision_window: 2026-07-16 P0 current-state window
route_binding_state: unknown
creator_registry_match_preflight:
  required_when: not_applicable
screening_evidence_summary: public product page was already a proven fragrance-native route candidate
uncertainty_or_access_limits: targeted sample only; scanning does not bind the Capture route
not_requested:
  - route expansion
  - packet commitment by scanning
  - ECR, Cleaning, or Judgment work
```

```yaml
capture_request_id: cr_p0_reddit
source_scan: forseti_research_engine_p0_imaginary_authors_20260716
candidate_or_observation_ids:
  - OBS-P0-002
urls:
  - url: https://old.reddit.com/r/fragranceswap/comments/1u5qg1g/wts_mancera_jousset_missing_person_imaginary/
    venue: Reddit r/fragranceswap
    observation_supported: OBS-P0-002
    gate_role: demand_origin
what_capture_should_verify: exact public post body, SKU condition, discontinued wording, asking price, and source-visible comment postures
decision_window: 2026-07-16 P0 current-state window
route_binding_state: unknown
creator_registry_match_preflight:
  required_when: not_applicable
screening_evidence_summary: exact public thread surfaced in the bounded product query and satisfied the old-Reddit URL gate
uncertainty_or_access_limits: one exact thread only; scanning does not bind the Capture route
not_requested:
  - route expansion
  - packet commitment by scanning
  - ECR, Cleaning, or Judgment work
```

## Candidate Decision

```yaml
candidate_observation_id: CAND-P0-001
candidate: Dipped in Chocolate low-commitment continuation / resale-interest candidate
supporting_observations:
  - OBS-P0-001
  - OBS-P0-002
why_promoted: >
  Two independent source families produced product-specific, hash-verified
  handoff-ready packets within the bounded P0 run.
decision_window: 2026-07-16 P0 current-state window
competing_or_defeating_observations:
  - The Reddit observation is one asking-price listing, not a completed sale.
  - The Parfumo capture is a targeted page sample, not a complete response corpus.
capture_needed: "no"
```

```yaml
candidate_decision:
  closeout_state: candidate_ready_for_next_lane
  independent_origins_seen:
    - Parfumo fragrance_native_database packet 01KXKDKV2G93R8QAZNQWNT120P
    - Reddit reddit_thread packet 01KXKDPFM3WWAE24BC2Q1JHV50
  commitment_ceiling: hold_low_commitment
  material_action_eligible: false
  reason: >
    Two independently owned public source families now preserve product-specific
    activity, but the run is one bounded P0 and does not establish demand,
    completed resale, continuation merit, or material-action eligibility.
```

## Closeout

`candidate_ready_for_next_lane`.

Every emitted request reached `handoff_ready`; none remained unknown or open.
The machine-verifiable event history is
`docs/research/forseti_research_engine_p0_capture_request_lifecycle_v0.json`.

## Capture Results

| Request | Capture-owned route | Packet | Manifest SHA-256 | Caller-bound detail check | Terminal state |
| --- | --- | --- | --- | --- | --- |
| cr_p0_parfumo | `parfumo_product_page_direct_http` | `01KXKDKV2G93R8QAZNQWNT120P` | `3c1fe849a8fcdc6e7a26ea214dcb98656f671e044db3f4e013bdcbc6688ed6c5` | Dipped in Chocolate plus review/statement/rating markers present; both preserved-file hashes recomputed equal. | `handoff_ready` |
| cr_p0_reddit | `old_reddit_direct_http` | `01KXKDPFM3WWAE24BC2Q1JHV50` | `57c6c99215a18dcfab4cb99a1303864c46248ff4c34eea2166f48a44c69a5b83` | Dipped in Chocolate, discontinued, 95 percent full, USD 110 present; six comments consolidated; both preserved-file hashes recomputed equal. | `handoff_ready` |

## Cost And Yield

| Stage | Measured wall clock | Token / model cost posture | Venues | Requests emitted | Fulfilled | Declined | Packets |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| bounded scan query call | 2.300 s | unknown-with-reason: search interface exposed no token metering | 2 | 2 | 2 | 0 | 2 |
| Parfumo capture | 2.061 s | no metered model used by deterministic runner | 1 | 0 | 1 | 0 | 1 |
| Reddit capture + consolidation | 2.958 s | no metered model used by deterministic runners | 1 | 0 | 1 | 0 | 1 |

The wall-clock values are the observed tool/runner durations named above, not a
claim about total human analysis time or recurring production economics.

## Compounding Memory Boundary

- Capture/scanning provenance owns the scan route, request lifecycle, access
  posture, packet IDs, hashes, declines, mode-ladder receipts, and cost/yield.
- Company Surface may later consume only company-linked observations and their
  source time/provenance, such as a time-bounded resale listing or official
  company activity. It must not ingest route attempts, request states, cost rows,
  or capture operator mechanics.
- No Company Surface record was written in this P0 because the commissioned stop
  boundary was ECR-handoff-ready Capture evidence, not downstream semantic
  materialization.

## Non-Claims

- not GT or MGT certification;
- not repeatability proof (the commissioned improvement 3 remains later work);
- not demand, buyer-proof, completed-sale, price-validity, or material-action evidence;
- not source completeness or full Parfumo corpus capture;
- not ECR, Cleaning, Judgment, Company Surface, monitoring, scheduler, registry, or atlas work;
- not commercial Reddit authority or broad crawling.
