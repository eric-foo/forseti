# Forseti Research Engine First Peach Repeatability Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Executed scanning-to-Capture target-transfer repeatability receipt
scope: >
  One bounded transfer of the merged P0 scanning-to-Capture spine from Dipped
  in Chocolate to First Peach of the Season, using the same two source-family
  route classes and stopping before ECR, Cleaning, Judgment, or Company Surface.
use_when:
  - Evaluating whether the P0 spine transferred to a second target.
  - Inspecting the disclosed operator intervention and packet-grade evidence.
authority_boundary: retrieval_only
open_next:
  - docs/research/forseti_research_engine_first_peach_repeatability_capture_request_lifecycle_v0.json
  - docs/research/forseti_research_engine_p0_golden_thread_receipt_v0.md
  - forseti-harness/docs/source_capture_agent_runbook.md
stale_if:
  - Either referenced Data Lake packet fails hash/schema verification.
  - Scan receipt v1 or capture-request lifecycle v0 changes.
  - The named packet IDs or manifest hashes no longer match the preserved evidence.
```

## Result

`TARGET_TRANSFER_REPEATABILITY_DEMONSTRATED_WITH_DISCLOSED_OPERATOR_INTERVENTION`.

The merged P0 spine transferred to a different Imaginary Authors product
without code, schema, source-family, or route-class changes. Both requested
URLs produced schema-valid, hash-verified packets. This demonstrates technical
target-transfer repeatability for the bounded spine. It does not demonstrate
zero-intervention operational repeatability: the first Reddit invocation used
an invalid free-text cutoff posture, published no packet, and required one
metadata-only correction before the same URL and capture route succeeded.

## Scan Intake Receipt

```yaml
scan_receipt_version: 1
commission_id: forseti_research_engine_repeatability_first_peach_20260716
scan_date: 2026-07-16
mode: forward
subject: Imaginary Authors / First Peach of the Season
market_or_geography: US indie fragrance, public-web current state
source_context_status: SOURCE_CONTEXT_READY
run_caps:
  max_screening_moves_total: 4
  max_exact_queries_total: 3
screening_moves_used: 4
exact_queries_used: 3
hidden_venue_pointers: 0
capture_requests: 2
closeout_state: candidate_ready_for_next_lane
```

## Broad Scout Return

The bounded `broad_scout_return` revisited the existing fragrance-native and
independent buyer-language frontiers, ran three exact queries, evaluated venue
value, accounted for zero hidden venue pointers, retained a negative subreddit
result and access notes, and prioritized current-state evidence. Recommended
main deepening was the exact First Peach Parfumo product page plus the exact
public r/Perfumes launch thread. The scout did not decide demand or bind a
Capture route.

## CSB Board Intake

Board source:
`docs/research/orca_commission_signal_board_imaginary_authors_forward_v0.md`.

Rows consumed as route map: SBR-005, SBR-006, and SBR-007.

## Exact Query Discovery Ledger

| Query ID | Query text | Intent | Result class | Next-route decision |
| --- | --- | --- | --- | --- |
| EQ-001 | `site:parfumo.com/Perfumes/Imaginary_Authors "First Peach of the Season"` | Find the exact fragrance-native product surface. | candidate_surface | Select the exact Parfumo product URL. |
| EQ-002 | `site:reddit.com/r/Perfumes "First Peach of the Season" "Imaginary Authors"` | Find independent product-specific launch discussion. | candidate_surface | Select the exact r/Perfumes launch thread. |
| EQ-003 | `site:reddit.com/r/fragrance "First Peach of the Season" "Imaginary Authors"` | Check an adjacent fragrance community without widening the target. | negative | Stop; no stronger exact target route was selected. |

## Venue Evaluation Move Log

| Move | CSB row(s) | Frontier | Value class | What happened | Stop check |
| --- | --- | --- | --- | --- | --- |
| M01 | SBR-005 | Parfumo First Peach product page | candidate_surface | Exact public product page exposed current rating, review, and statement markers. | a:no b:no c:no |
| M02 | SBR-006, SBR-007 | Reddit r/Perfumes exact launch thread | candidate_surface | Exact public product discussion surfaced on the existing old-Reddit route class. | a:no b:no c:no |
| M03 | SBR-006 | Reddit r/fragrance exact query | negative | No stronger target-specific route displaced the selected thread. | a:no b:branch-close c:no |
| M04 | SBR-005, SBR-007 | Paired target-transfer selection | route_ready | One URL per P0 source-family class was emitted for Capture. | a:no b:no c:stop-cap-reached |

## Hidden Venue Pointers

None. The run emitted `hidden_venue_pointers: 0`; it reused the two P0
source-family route classes and created no registry, atlas, or standing map.

## Observations

```yaml
observation_id: OBS-RPT-001
source_move_id: M01
url: https://www.parfumo.com/Perfumes/Imaginary_Authors/first-peach-of-the-season
retrieval_date: 2026-07-16
short_quote_or_summary: >
  The public page returned HTTP 200 and preserved First Peach of the Season,
  Imaginary Authors, rating 7.6, 43 ratings, 6 reviews, and 18 statements.
signal_stage: candidate_support
claim_it_might_support: repeatable preservation of a second target on the fragrance-native route class
gate_role: demand_origin
independence_hypothesis: fragrance-native database source family, independent of Reddit and owned sources
uncertainty_or_limits: targeted current-page sample only; no complete review or statement corpus was captured
```

```yaml
observation_id: OBS-RPT-002
source_move_id: M02
url: https://old.reddit.com/r/Perfumes/comments/1s9hx08/imaginary_authors_first_peach_of_the_season_april/
retrieval_date: 2026-07-16
short_quote_or_summary: >
  The exact public launch thread returned HTTP 200 and preserved the First
  Peach target identity; deterministic consolidation emitted 13 comments.
signal_stage: candidate_support
claim_it_might_support: repeatable preservation of a second target on the independent Reddit route class
gate_role: demand_origin
independence_hypothesis: Reddit thread source family, independent of Parfumo and owned sources
uncertainty_or_limits: one thread only; the first invocation required metadata correction and published no packet
```

## Negatives And Access Notes

- `NEG-RPT-001`: The exact r/fragrance query did not yield a stronger target-specific route than the selected r/Perfumes thread.
- `ACCESS-RPT-001`: Parfumo direct HTTP returned caller-bound page content, so no rendered escalation was needed.
- `ACCESS-RPT-002`: Reddit used one exact old-Reddit thread; no crawl, profile read, link following, login, proxy, or commercial API.
- `ACCESS-RPT-003`: The first Reddit invocation fetched but published no packet because a free-text cutoff posture was outside the runner's closed vocabulary. The corrected invocation changed metadata only, then succeeded on the same URL and route.

## Capture Triage

```yaml
capture_request_id: cr_repeat_parfumo
source_scan: forseti_research_engine_repeatability_first_peach_20260716
candidate_or_observation_ids:
  - OBS-RPT-001
urls:
  - url: https://www.parfumo.com/Perfumes/Imaginary_Authors/first-peach-of-the-season
    venue: Parfumo
    observation_supported: OBS-RPT-001
    gate_role: demand_origin
what_capture_should_verify: exact product identity plus current rating, review, and statement surface markers
decision_window: 2026-07-16 target-transfer repeatability window
route_binding_state: unknown
creator_registry_match_preflight:
  required_when: not_applicable
screening_evidence_summary: exact public product page matched the P0 fragrance-native route class
uncertainty_or_access_limits: targeted sample only; scanning does not bind the Capture route
not_requested:
  - route_expansion
  - packet_commitment_by_scanning
  - ecr_cleaning_or_judgment_work
```

```yaml
capture_request_id: cr_repeat_reddit
source_scan: forseti_research_engine_repeatability_first_peach_20260716
candidate_or_observation_ids:
  - OBS-RPT-002
urls:
  - url: https://old.reddit.com/r/Perfumes/comments/1s9hx08/imaginary_authors_first_peach_of_the_season_april/
    venue: Reddit r/Perfumes
    observation_supported: OBS-RPT-002
    gate_role: demand_origin
what_capture_should_verify: exact public thread identity and source-visible comment states
decision_window: 2026-07-16 target-transfer repeatability window
route_binding_state: unknown
creator_registry_match_preflight:
  required_when: not_applicable
screening_evidence_summary: exact public thread matched the P0 old-Reddit route class
uncertainty_or_access_limits: one exact thread; scanning does not bind the route; metadata correction disclosed
not_requested:
  - route_expansion
  - packet_commitment_by_scanning
  - ecr_cleaning_or_judgment_work
```

## Candidate Decision

```yaml
candidate_observation_id: CAND-RPT-001
candidate: First Peach target-transfer repeatability evidence
supporting_observations:
  - OBS-RPT-001
  - OBS-RPT-002
why_promoted: >
  A second target produced handoff-ready packets from the same two independent
  source-family route classes without implementation or contract changes.
decision_window: 2026-07-16 target-transfer repeatability window
competing_or_defeating_observations:
  - The Reddit path required one operator metadata correction.
  - Two targets do not establish broad source-agnostic or unattended operation.
capture_needed: "no"
```

```yaml
candidate_decision:
  closeout_state: candidate_ready_for_next_lane
  independent_origins_seen:
    - Parfumo fragrance_native_database packet 01KXMWTRSJ4AY3PBP9FP4T3WE6
    - Reddit reddit_thread packet 01KXMWXF3RPTMFKMQYN5X46A0M
  commitment_ceiling: technical_repeatability_only
  material_action_eligible: false
  reason: >
    The frozen spine transferred successfully, but the run does not establish
    unattended operation, broad source agnosticism, demand, or material action.
```

## Closeout

`candidate_ready_for_next_lane`.

Both emitted requests reached `handoff_ready`. The machine-verifiable history is
`docs/research/forseti_research_engine_first_peach_repeatability_capture_request_lifecycle_v0.json`.

## Capture Results

| Request | Capture-owned route | Packet | Manifest SHA-256 | Caller-bound detail check | Terminal state |
| --- | --- | --- | --- | --- | --- |
| cr_repeat_parfumo | `parfumo_product_page_direct_http` | `01KXMWTRSJ4AY3PBP9FP4T3WE6` | `5c04b5fb2050c0fde3a10a8583a3931f21c2963c6ef15bca198452c278fa7f30` | First Peach, Imaginary Authors, 7.6, 43 ratings, 6 reviews, and 18 statements present; preserved-file hashes recomputed equal. | `handoff_ready` |
| cr_repeat_reddit | `old_reddit_direct_http` | `01KXMWXF3RPTMFKMQYN5X46A0M` | `da6e4ce86de9faacbdbd679a9d5a4c34644b91ec572c8a893f871c05a0c90413` | Exact First Peach launch thread preserved; 13 comments consolidated; preserved-file hashes recomputed equal. | `handoff_ready` |

## Baseline Comparison

| Dimension | P0 Dipped in Chocolate | First Peach repeatability run | Assessment |
| --- | --- | --- | --- |
| source families | Parfumo + Reddit | Parfumo + Reddit | repeated |
| route classes | direct Parfumo + exact old Reddit | same | repeated |
| implementation/schema changes | none during run | none during run | repeated |
| terminal verified packets | 2 | 2 | repeated |
| target | Dipped in Chocolate | First Peach of the Season | transferred |
| operator intervention | none disclosed | one Reddit metadata correction | residual |

## Cost And Yield

| Stage | Measured wall clock | Token / model cost posture | Venues | Requests emitted | Fulfilled | Declined | Packets |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| bounded scan | 16.214 s | unknown-with-reason: search interface exposed no token metering | 2 | 2 | 2 | 0 | 2 |
| Parfumo capture | 1.924 s | no metered model used by deterministic runner | 1 | 0 | 1 | 0 | 1 |
| Reddit attempts + successful capture + consolidation | 7.088 s | no metered model used by deterministic runners | 1 | 0 | 1 | 0 | 1 |

The Reddit row includes the 3.607-second failed metadata invocation, the
2.692-second corrected capture, and the 0.789-second consolidation. These are
observed runner durations, not total human time or production economics.

## Compounding Memory Boundary

- Scanning/Capture memory owns route selection, request lifecycle, access
  posture, packet IDs, hashes, operator corrections, and cost/yield.
- Company Surface may later consume only company-linked observations with
  source time and provenance. It must not ingest route attempts, request states,
  operator corrections, or capture cost rows.
- No Company Surface record was written because this run stopped at verified
  Capture handoff.

## Non-Claims

- not GT or MGT certification;
- not zero-intervention, unattended, or scheduled repeatability;
- not broad source/target agnosticism from only two targets and two source families;
- not demand, buyer-proof, product merit, or material-action evidence;
- not full Parfumo or Reddit corpus capture;
- not ECR, Cleaning, Judgment, Company Surface, monitoring, registry, or atlas work.