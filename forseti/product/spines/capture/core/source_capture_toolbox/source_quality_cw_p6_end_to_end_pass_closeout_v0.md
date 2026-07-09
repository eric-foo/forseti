# Source Quality CW-P6 End-To-End Pass Closeout v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Closeout for one bounded Mini God-Tier source-quality pass on Canoo/Walmart source unit CW-P6.
use_when:
  - Checking whether the Mini God-Tier queue-to-report loop handles a preserved current official body with visible limitations.
  - Inspecting how Direct HTTP packet evidence differs from archive-body packet evidence.
  - Planning the next source-quality pass after CW-P6.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mixed_source_trial_closeout_v0.md
  - forseti-harness/docs/source_capture_agent_runbook.md
stale_if:
  - The CW-P6 scratch packet under forseti-harness/_test_runs/ is unavailable or changed.
  - The Mini God-Tier profile changes result tokens, criteria, or lifecycle states.
  - The Source Quality report-skeleton helper changes result-token behavior.
```

## Status

Status: `SOURCE_QUALITY_CW_P6_END_TO_END_PASS_CLOSEOUT_V0`.

This artifact closes a bounded one-source Mini God-Tier source-quality pass for
`CW-P6`. The pass exercised the intended loop:

```text
source-unit queue posture -> packet inspection -> helper skeleton ->
operator-finalized report block -> queue row reported
```

The pass did not discover, select, rank, score, admit, or judge sources. The
packet remains scratch lifecycle evidence under `_test_runs/`, not an admitted
fixture or durable raw-source repository.

## Source-Unit Queue Row

| source_id | case_or_slot | locator | decision_relevance | current_state | target_posture | primary_runner | fallback_runner | cutoff | row_status | result_token | packet_lifecycle | visible_limitations | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CW-P6` | Canoo/Walmart v0.14 source unit | `https://www.sec.gov/Archives/edgar/data/1750153/000162828022013637/goev-20220331.htm` | SEC filing body relevant to the bounded Canoo/Walmart source unit; not a relevance ranking or Judgment weight. | Existing Direct HTTP source-capture packet in scratch. | Current official SEC Archives filing body preserved and inspectable, with archive/history not attempted. | Direct HTTP runner output already present; no rerun performed. | `none` | Filing period ended `2022-03-31`; current retrieval of stable SEC Archives URL. | `reported` | `mini_god_tier_with_visible_limitations` | `scratch` | Direct HTTP did not query archive/history; media assets not fetched; inline XBRL anchor extraction is noisy; packet is not fixture-admitted. | Final token is operator-finalized from packet/body inspection, not helper output alone. |

## Packet Evidence Inspected

Packet path:
`forseti-harness/_test_runs/source_quality_mixed_trial_20260603_153531/cw_p6_direct_http`.

Fresh read showed:

```yaml
packet_id: 01KT66JNHC06TQGBP97KYXN5QB
source_surface: direct_http
source_locator: https://www.sec.gov/Archives/edgar/data/1750153/000162828022013637/goev-20220331.htm
access_posture: direct_http succeeded with HTTP 200 OK
archive_history_posture: not_attempted - direct HTTP adapter does not query archive or history services
media_modality_posture: not_attempted - direct HTTP adapter preserves the response body only and does not fetch linked media assets
source_slice_count: 1
preserved_file_count: 2
```

Preserved files:

| File | Size bytes | SHA256 |
| --- | ---: | --- |
| `raw/01_http_response_body.bin` | 943628 | `77CCE11600E168CA67B97FEEA5521411B0FFAC6A64E2A811EC10B1C2F8E19D95` |
| `raw/02_http_response_metadata.json` | 514 | `2A634AFDA140366B69BBFED1F300D7D86F1FA9376A018806D6FAA15544616EEC` |

Source slice:

| slice_id | Preserved files | Access posture | Archive posture | Timing / cutoff |
| --- | --- | --- | --- | --- |
| `slice_01` | `file_01`, `file_02` | Direct HTTP HTTP 200. | Not attempted; Direct HTTP does not query archive/history. | Capture time `2026-06-03T07:36:14Z`; cutoff posture says official SEC Archives filing body for period ended `2022-03-31`, retrieved currently from stable archive URL. |

HTTP metadata:

```yaml
requested_url: https://www.sec.gov/Archives/edgar/data/1750153/000162828022013637/goev-20220331.htm
final_url: https://www.sec.gov/Archives/edgar/data/1750153/000162828022013637/goev-20220331.htm
status: 200
reason: OK
content_type: text/html
byte_count: 943628
last_modified: Tue, 10 May 2022 20:50:29 GMT
capture_timestamp: 2026-06-03T07:36:14Z
```

## Helper Skeleton Output

The report-skeleton helper was run against the packet and wrote:

```text
forseti-harness/_test_runs/source_quality_cw_p6_end_to_end_20260603/cw_p6_skeleton.yaml
```

Fresh read showed the helper output:

```yaml
suggested_result_token: mini_god_tier_with_visible_limitations
result_token_finalization: operator_review_required
best_in_bound_body:
  posture: preserved
  preserved_body_path: raw/01_http_response_body.bin
  sha256: 77cce11600e168ca67b97feea5521411b0ffac6a64e2a811ec10b1c2f8e19d95
  byte_count: 943628
  source_or_snapshot_time: official SEC Archives filing body for period ended 2022-03-31; current retrieval of stable archive URL
visible_limitations:
  - "archive_history_posture: not_attempted - direct HTTP adapter does not query archive or history services"
  - "media_modality_posture: not_attempted - direct HTTP adapter preserves the response body only and does not fetch linked media assets"
operator_completion_required:
  - review suggested_result_token against the Mini God-Tier profile
  - supply bounded source-language anchors or not_applicable_with_reason
  - supply coverage_or_drift_note
lifecycle_state: scratch
lifecycle_decision_reference: none
```

This is the expected helper behavior. The helper did not finalize
`mini_god_tier_met`; it only shaped the packet evidence and left
source-language anchors and coverage/drift to operator completion.

## Operator-Finalized Mini God-Tier Report

```yaml
mini_god_tier_source_quality_report:
  source_id: CW-P6
  result_token: mini_god_tier_with_visible_limitations
  packet_path: forseti-harness/_test_runs/source_quality_mixed_trial_20260603_153531/cw_p6_direct_http
  best_in_bound_body:
    posture: preserved
    preserved_body_path: raw/01_http_response_body.bin
    sha256: 77CCE11600E168CA67B97FEEA5521411B0FFAC6A64E2A811EC10B1C2F8E19D95
    byte_count: 943628
    source_or_snapshot_time: "period ended 2022-03-31; current retrieval of stable SEC Archives URL; HTTP Last-Modified Tue, 10 May 2022 20:50:29 GMT"
  provenance:
    original_locator: https://www.sec.gov/Archives/edgar/data/1750153/000162828022013637/goev-20220331.htm
    final_or_snapshot_locator: https://www.sec.gov/Archives/edgar/data/1750153/000162828022013637/goev-20220331.htm
    access_status: direct_http succeeded with HTTP 200 OK
    content_type: text/html
    capture_time: 2026-06-03T07:36:14Z
  source_language_anchors:
    - "SEC/XBRL identity anchors: dei:DocumentType; dei:EntityRegistrantName; CANOO INC.; 10-Q"
    - "filing timing anchors: 2022-03-31; May&#160;10, 2022"
    - "bounded filing/source terms: GOEV; us-gaap:CashAndCashEquivalentsAtCarryingValue; Inline XBRL"
  coverage_or_drift_note: standardizes current official SEC Archives filing body possession for CW-P6 and supplements the prior source state; it does not prove archive/history posture because no archive/history service was queried.
  visible_limitations:
    - "Direct HTTP did not query archive or history services."
    - "Media or linked assets were not fetched; Direct HTTP preserved the response body and response metadata only."
    - "Inline XBRL is preserved, but anchor extraction is noisy because much content is embedded in long HTML/XBRL lines."
    - "Actor/audience context was not supplied to the Direct HTTP runner."
    - "The packet is scratch lifecycle output under _test_runs/ and is not a separately admitted fixture."
    - "No source completeness, rights, retention, sensitivity, or Judgment-quality claim is made."
  lifecycle_state: scratch
  lifecycle_decision_reference: none
  non_claims:
    - not validation
    - not source completeness proof
    - not fixture admission unless separately decided
    - not Judgment scoring
```

## Six-Criteria Check

| Mini God-Tier criterion | CW-P6 result |
| --- | --- |
| Best in-bound body possession | Satisfied with visible limitations. The current official SEC Archives filing body is preserved at `raw/01_http_response_body.bin`; archive/history posture remains not attempted. |
| Identity and provenance | Satisfied with visible limitations. Original/final locator, HTTP status, content type, capture time, last-modified header, byte count, and SHA256 are visible; source edit/version is not inferred beyond packet metadata. |
| Source-language anchors | Satisfied for bounded literal anchors. The preserved body contains SEC/XBRL identity, timing, ticker, and filing-term anchors; no Judgment meaning is inferred from them. |
| Coverage or drift note | Satisfied with visible limitations. The pass standardizes current official SEC Archives body possession and supplements prior state, but does not prove archive/history posture. |
| Visible limitations | Satisfied. Archive/history, media, inline-XBRL noise, actor/audience context, scratch lifecycle, and non-claim limits are explicit. |
| Lifecycle state | Satisfied. Lifecycle is `scratch`; no separate fixture admission is implied. |

## Pass Finding

The CW-P6 pass confirms the Mini God-Tier loop works end to end for a preserved
current official body where limitations still matter:

1. the queue row represented the bounded source unit without discovering or
   ranking sources;
2. packet inspection confirmed an inspectable SEC filing body, not merely a
   pointer or metadata shell;
3. the skeleton helper preserved conservative behavior and did not finalize a
   clean token;
4. operator completion supplied bounded anchors and coverage/drift from the
   preserved body;
5. row status reached `reported` only after the final report block existed.

No helper code change or result-token vocabulary change is required from this
pass.

## Friction

- The packet is under `_test_runs/`, so future strict source-quality claims
  depend on that scratch packet still being available unless a separate
  fixture-admission or retention decision preserves it durably.
- Direct HTTP preserves the current official SEC Archives filing body but does
  not query archive/history services.
- Inline XBRL is source-body possession but remains awkward for manual anchor
  extraction because important terms can occur on very long HTML/XBRL lines.

## Next Learning

The next highest-value source-quality pass should test either a source unit
where media or browser rendering materially affects source-quality posture, or
a source unit where existing packet evidence produces a true
`archive_body_not_preserved` / `body_possession_not_proven` outcome.

Do not treat this CW-P6 pass as proof that current-body capture is sufficient
for every source family.

## Non-Claims

This closeout is not validation, readiness, source completeness proof, fixture
admission, rights clearance, retention policy, sensitivity review, source
discovery, source selection, source-quality scoring, Judgment scoring, ECR
design, Cleaning implementation, buyer proof, commercial-readiness evidence,
source-access boundary amendment, or authorization for new adapters, APIs,
crawlers, browser fallback, commercial fetch, or production runtime.
