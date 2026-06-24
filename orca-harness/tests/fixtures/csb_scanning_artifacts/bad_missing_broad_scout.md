<!-- fixture_expected: fail -->
<!-- fixture_purpose: CSB-first scan artifacts must account for the default broad-scout phase -->

# Fixture CSB-First Scan Missing Scout

```yaml
retrieval_header_version: 1
artifact_role: Research artifact (fixture)
scope: Fixture for the CSB-first scanning artifact checker.
use_when:
  - Testing the checker.
authority_boundary: retrieval_only
```

## Scan Intake Receipt

```yaml
commission_id: fixture_csb_first_scan_missing_scout
scan_date: 2026-06-23
mode: forward
subject: Fixture Brand
market_or_geography: US
source_context_status: SOURCE_CONTEXT_READY
run_caps:
  max_screening_moves_total: 8
  max_exact_queries_total: 3
screening_moves_used: 1
exact_queries_used: 1
hidden_venue_pointers: 0
capture_requests: 0
closeout_state: no_candidate_after_discovery
```

## CSB Board Intake

Rows consumed as route map: SBR-001.

## Exact Query Discovery Ledger

| Query ID | Query text | Intent | Result class | Next-route decision |
| --- | --- | --- | --- | --- |
| EQ-001 | `"Fixture Product" review` | Test buyer language. | negative | Record gap. |

## Venue Evaluation Move Log

| Move | CSB row(s) | Frontier | Value class | What happened | Stop check |
| --- | --- | --- | --- | --- | --- |
| M01 | SBR-001 | Official PDP | venue_value | Current state observed. | a:no b:no c:no |

## Hidden Venue Pointers

No new hidden venue surfaced.

## Observations

```yaml
observation_id: OBS-001
source_move_id: M01
url: https://example.test/fixture-product
retrieval_date: 2026-06-23
short_quote_or_summary: >
  Fixture official PDP had current-state availability.
signal_stage: access_note
claim_it_might_support: preservation pressure only
gate_role: none
independence_hypothesis: owned source only; no independent demand origin
uncertainty_or_limits: fixture text is not buyer-origin support
```

## Negatives And Access Notes

- `NEG-001`: No public buyer-language venue surfaced.

## Capture Triage

No capture_requests emitted.

## Candidate Decision

```yaml
candidate_decision:
  closeout_state: no_candidate_after_discovery
  reason: Fixture scan has no candidate.
```

## Closeout

`no_candidate_after_discovery`.
