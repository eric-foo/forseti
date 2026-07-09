# Source Quality Mixed-Source Trial Closeout v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Closeout for the first mixed-source Mini God-Tier source-quality trial across already-bounded Canoo/Walmart source units.
use_when:
  - Scoping helper automation for Mini God-Tier source-quality report blocks.
  - Checking what the mixed-source trial proved and did not prove.
  - Distinguishing packet-write success from source-quality result tokens.
authority_boundary: trial_closeout
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/source_quality_mini_god_tier_profile_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_quality_source_unit_queue_template_v0.md
  - forseti-harness/docs/source_capture_agent_runbook.md
stale_if:
  - The Mini God-Tier profile changes result tokens, lifecycle vocabulary, or required report fields.
  - The Source Capture Armory packet manifest shape changes materially.
  - A fixture-admission, rights, retention, or sensitivity policy becomes controlling for generated packet outputs.
```

## Status

Status: `SOURCE_QUALITY_MIXED_SOURCE_TRIAL_CLOSEOUT_V0`.

This artifact closes the first mixed-source trial of the Mini God-Tier
source-quality structure. It records what the trial showed about the current
profile, queue template, runbook report block, and Source Capture Armory
packet outputs.

The trial used already-bounded Canoo/Walmart source units. It did not discover,
select, rank, score, admit, or judge sources.

## Trial Question

Can the Mini God-Tier structure produce consistent, inspectable source-quality
report outcomes across different source postures without relying on agent
memory or informal packet-success inference?

The trial answer is yes for operating structure, with one clear next helper
need: agents need a small report-skeleton helper that reads packet manifests and
raw metadata into profile-shaped report blocks so they do not manually rebuild
the same posture logic each time.

## Source Units

| source_id | Source posture tested | Runner outcome | Result token | Lifecycle |
| --- | --- | --- | --- | --- |
| `CW-P4` | PRNewswire historical source where archive body could satisfy cutoff posture | Archive.org packet preserved availability metadata and selected snapshot body | `mini_god_tier_met` | `scratch` |
| `CW-P1` | Walmart historical source where archive availability existed but no eligible cutoff body was selected | Archive.org packet preserved availability metadata only | `archive_body_not_preserved` | `scratch` |
| `CW-P6` | SEC filing body where stable current official body could be preserved by Direct HTTP | Direct HTTP packet preserved SEC inline XBRL body and response metadata | `mini_god_tier_with_visible_limitations` | `scratch` |

All rows reached `reported` state for this trial. None reached
`separately_admitted`.

## Packet Evidence

### CW-P4

```yaml
mini_god_tier_source_quality_report:
  source_id: CW-P4
  result_token: mini_god_tier_met
  packet_path: forseti-harness/_test_runs/source_quality_cw_p4_20260603_052930/archive_cw_p4
  best_in_bound_body:
    posture: preserved
    preserved_body_path: raw/02_archive_snapshot_body.bin
    sha256: 1e4cfc078afc878e9430ef1e7be20c7587afdb857ab7eaefae7acca7c5d17c7c
    byte_count: 298903
    source_or_snapshot_time: 20220511053411
  provenance:
    original_locator: https://www.prnewswire.com/news-releases/canoo-inc-announces-fourth-quarter-and-fiscal-year-2021-results-301492051.html
    final_or_snapshot_locator: https://web.archive.org/web/20220511053411/https://www.prnewswire.com/news-releases/canoo-inc-announces-fourth-quarter-and-fiscal-year-2021-results-301492051.html
    access_status: archive_org snapshot body direct_http succeeded with HTTP 200 OK
    content_type: unknown_with_reason
    capture_time: 2026-06-02T21:31:03Z
  source_language_anchors:
    - "title anchor: CANOO INC. ANNOUNCES FOURTH QUARTER AND FISCAL YEAR 2021 RESULTS"
    - "date/place anchor: JUSTIN, Texas, Feb. 28, 2022"
    - "bounded term anchors: 1,000 vehicles; Advanced Manufacturing Facility; Cash and cash equivalents"
  coverage_or_drift_note: improves prior posture by preserving a cutoff-compatible archive body, not only a current page or pointer.
  visible_limitations:
    - "Archive.org metadata is collapse=digest availability; not archive completeness proof."
  lifecycle_state: scratch
  lifecycle_decision_reference: none
  non_claims:
    - not validation
    - not source completeness proof
    - not fixture admission unless separately decided
    - not Judgment scoring
```

### CW-P1

```yaml
mini_god_tier_source_quality_report:
  source_id: CW-P1
  result_token: archive_body_not_preserved
  packet_path: forseti-harness/_test_runs/source_quality_mixed_trial_20260603_153531/cw_p1_archive
  best_in_bound_body:
    posture: metadata_only
    preserved_body_path: none
    sha256: none
    byte_count: none
    source_or_snapshot_time: "earliest observed availability timestamp 20230920050729; no selected snapshot at or before cutoff"
  provenance:
    original_locator: https://corporate.walmart.com/news/2022/01/05/walmart-to-expand-inhome-delivery-reaching-30-million-u-s-homes-in-2022
    final_or_snapshot_locator: none
    access_status: archive_org availability direct_http succeeded with HTTP 200 OK
    content_type: availability metadata
    capture_time: 2026-06-03T07:35:51Z
  source_language_anchors:
    - "not_applicable_with_reason: no archive snapshot body was preserved"
  coverage_or_drift_note: standardizes archive availability posture only; does not improve body possession.
  visible_limitations:
    - "Availability metadata was preserved, but selected_snapshot was null."
    - "Observed snapshot_count was 13, but the earliest observed timestamp was 20230920050729, after cutoff 20220701000000."
    - "Packet limitations were empty, so result-token logic must inspect archive/body posture rather than treating exit code 0 as clean capture."
  lifecycle_state: scratch
  lifecycle_decision_reference: none
  non_claims:
    - not validation
    - not source completeness proof
    - not fixture admission unless separately decided
    - not Judgment scoring
```

### CW-P6

```yaml
mini_god_tier_source_quality_report:
  source_id: CW-P6
  result_token: mini_god_tier_with_visible_limitations
  packet_path: forseti-harness/_test_runs/source_quality_mixed_trial_20260603_153531/cw_p6_direct_http
  best_in_bound_body:
    posture: preserved
    preserved_body_path: raw/01_http_response_body.bin
    sha256: 77cce11600e168ca67b97feea5521411b0ffac6a64e2a811ec10b1c2f8e19d95
    byte_count: 943628
    source_or_snapshot_time: "period ended 2022-03-31; current retrieval of stable SEC Archives URL"
  provenance:
    original_locator: https://www.sec.gov/Archives/edgar/data/1750153/000162828022013637/goev-20220331.htm
    final_or_snapshot_locator: https://www.sec.gov/Archives/edgar/data/1750153/000162828022013637/goev-20220331.htm
    access_status: direct_http succeeded with HTTP 200 OK
    content_type: text/html
    capture_time: 2026-06-03T07:36:14Z
  source_language_anchors:
    - "bounded inline-XBRL anchors: DocumentType; EntityRegistrantName; CANOO INC.; 10-Q"
    - "bounded financial/source terms: CashAndCashEquivalentsAtCarryingValue; VehiclesMember; GOEV"
  coverage_or_drift_note: improves body possession for the SEC filing detail body while leaving historical archive lookup not attempted.
  visible_limitations:
    - "Direct HTTP adapter does not query archive or history services."
    - "Inline XBRL is preserved, but line-based human anchor extraction is noisy because much content is on very long lines."
    - "This is current retrieval of a stable SEC Archives URL, not separate fixture admission."
  lifecycle_state: scratch
  lifecycle_decision_reference: none
  non_claims:
    - not validation
    - not source completeness proof
    - not fixture admission unless separately decided
    - not Judgment scoring
```

## Trial Findings

1. The profile successfully separated packet-write success from source-quality
   status. CW-P1 had exit code 0 and empty manifest limitations, but still
   correctly classified as `archive_body_not_preserved` because no eligible
   archive body was selected.
2. The queue/report split worked: after packet inspection, all three rows could
   move from packet-written posture to `reported` with profile-owned result
   tokens.
3. The runbook network-permission discipline worked: live network-backed
   runners were run with per-operation network permission instead of spending a
   first failed attempt on sandbox network refusal.
4. The current packet manifests contain enough structured fields to support
   report skeleton generation, but humans still have to inspect raw metadata and
   selected files to classify archive/body and anchor posture correctly.
5. SEC inline XBRL is body-preserved but awkward for manual source-language
   anchor extraction. Future helper work should support term-window or
   source-visible anchor probes without scoring or interpreting source meaning.

## Helper Requirements Implied

A smallest complete helper for the next checkpoint should:

- read one or more Source Capture Packet `manifest.json` files;
- emit a Mini God-Tier report-block skeleton using existing profile fields;
- carry packet path, preserved files, hashes, byte counts, access posture,
  archive posture, media posture, cutoff posture, capture time, and non-claims;
- detect archive packets where availability metadata exists but no snapshot body
  is preserved;
- avoid treating empty `limitations` as clean capture;
- leave source-language anchors as operator-fillable by default, with optional
  bounded term probes only when explicitly supplied;
- never admit fixtures, score source quality, decide Judgment meaning, run ECR
  or Cleaning, discover sources, fetch new sources, or change packet outputs.

The helper should optimize for report consistency, not inference.

## Non-Claims

This closeout is not validation, readiness, source completeness proof, fixture
admission, rights clearance, retention policy, sensitivity review, source
discovery, source selection, source-quality scoring, Judgment scoring, ECR
design, Cleaning implementation, buyer proof, commercial-readiness evidence, or
authorization for new adapters, APIs, crawlers, browser fallback, commercial
fetch, or production runtime.
