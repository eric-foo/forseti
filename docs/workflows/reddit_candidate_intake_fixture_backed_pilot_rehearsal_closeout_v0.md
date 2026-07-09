# Reddit Candidate Intake Fixture-Backed Pilot Rehearsal Closeout v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow closeout
scope: >
  Records a no-live fixture-backed rehearsal of the Reddit Candidate URL Intake
  operator pilot path through projection, output assembly, writer, and readback.
use_when:
  - Checking whether the operator-pilot execution path works before a real operator-supplied HTML input is available.
  - Distinguishing fixture-backed pilot rehearsal evidence from an actual operator-supplied old Reddit pilot.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/reddit_candidate_intake_operator_pilot_plan_v0.md
  - docs/workflows/reddit_candidate_intake_operator_pilot_parameter_packet_v0.md
  - docs/workflows/reddit_candidate_intake_no_live_dry_use_receipt_v0.md
  - forseti-harness/_test_runs/reddit_candidate_pilot_001/reddit_candidate_url_intake.json # nonresolving: gitignored run scratch
  - forseti-harness/_test_runs/reddit_candidate_pilot_001/reddit_candidate_url_intake_receipt.md # nonresolving: gitignored run scratch
```

## Status

Status: `FIXTURE_BACKED_PILOT_REHEARSAL_COMPLETE`.

This is a no-live rehearsal using the existing static fixture:

```text
orca-harness/tests/fixtures/reddit_candidate_intake/old_reddit_listing_noisy.html
```

It is not an actual operator-supplied old Reddit pilot. The operator pilot
parameter packet remains blocked for a real pilot until the operator supplies
the actual old Reddit source URL and static HTML input.

## Pilot Closeout

```yaml
pilot_closeout:
  run_id: reddit_candidate_pilot_001
  mode: fixture_backed_no_live_pilot_rehearsal
  declared_topic_theme_query: "durable Reddit source capture / old Reddit capture"
  seed_subreddits:
    - orca_test
  source_surface: reddit_search_listing
  source_url: "https://old.reddit.com/r/orca_test/search/?q=durable+Reddit+source+capture&sort=top&t=month"
  html_input_reference: orca-harness/tests/fixtures/reddit_candidate_intake/old_reddit_listing_noisy.html
  cap_type: probe
  coverage_claim: bounded_probe_only
  caps_applied:
    max_subreddits: 5
    max_threads_per_subreddit: 25
    max_pages_or_result_surfaces: 2
    time_window_days: 30
  sort_order: top
  time_window_days: 30
  exclusions: []
  method_category: static_old_reddit_html_fixture_rehearsal
  row_counts:
    candidate_subreddits: 0
    candidate_threads: 3
    outbound_urls: 0
  stop_reason: scope_exhausted
  output_artifacts:
    json_path: orca-harness/_test_runs/reddit_candidate_pilot_001/reddit_candidate_url_intake.json
    receipt_path: orca-harness/_test_runs/reddit_candidate_pilot_001/reddit_candidate_url_intake_receipt.md
  forbidden_output_checks:
    raw_html_absent: observed_no_match
    body_comment_absent: observed_no_match
    user_profile_absent: observed_no_match
    source_capture_packet_absent: non_claim_only_no_packet_artifact
    data_capture_handoff_absent: non_claim_only_no_handoff_artifact
  operator_decision:
    promote_candidate_now: deferred
    reason: >
      This was a fixture-backed rehearsal, not a real operator-supplied pilot.
      Promotion remains separately gated.
```

## Observed Execution

Command run from `orca-harness/`:

```text
python - <inline package exercise>
rows=3
json_path=_test_runs\reddit_candidate_pilot_001\reddit_candidate_url_intake.json
receipt_path=_test_runs\reddit_candidate_pilot_001\reddit_candidate_url_intake_receipt.md
```

The inline exercise used only existing Candidate URL Intake package functions:

- `project_old_reddit_html_listing`;
- `build_candidate_intake_output`;
- `write_candidate_intake_output`.

No live Reddit, CloakBrowser, proxy, browser, API, archive, Armory runner, or
Source Capture Packet path was invoked.

## Observed Validation

Command observed from `orca-harness/`:

```text
python -m pytest -p no:cacheprovider tests/unit/test_reddit_candidate_intake.py tests/contract/test_reddit_candidate_intake_contract.py
...............                                                          [100%]
15 passed in 0.09s
```

Boundary readback observed:

- JSON output contains 3 `candidate_threads` rows.
- JSON output contains 0 `candidate_subreddits` rows.
- JSON output contains 0 `outbound_urls` rows.
- Receipt records `Stop reason: scope_exhausted`.
- Receipt records `Candidate threads: 3`.
- Output non-claims include `not Source Capture Packet output`.
- Output non-claims include `not Data Capture handoff`.

Forbidden fixture-noise scan:

```text
rg -n "ordinary_person|body text not allowed|Comment body text|<html>|https://old\.reddit\.com/r/orca_test/\.json|example\.com/outbound-source|crosspost source candidate surface only" orca-harness\_test_runs\reddit_candidate_pilot_001\reddit_candidate_url_intake.json orca-harness\_test_runs\reddit_candidate_pilot_001\reddit_candidate_url_intake_receipt.md
```

Observed result: no matches.

## Output Hashes

```yaml
reddit_candidate_url_intake_json: EC3D7341A87651EC37DAC3F1D086D2F0A3C28171E5FCE03D02F9745BBB6A0009
reddit_candidate_url_intake_receipt_md: B8BE6FF51856D56C6D0AFCBCDDD8BF6A21E4236FB88BF7E434F8363FB2AA41F7
```

## Meaning For Next Step

The execution path is now rehearsed end to end with a static fixture. The next
success signal is no longer "can the package write candidate-only output from a
fixture"; it is:

```text
Can an operator-supplied old Reddit HTML page produce useful candidate rows for
the declared planning decision under the same gates?
```

That next step still requires the missing real pilot inputs:

- actual old Reddit listing/search provenance URL;
- static HTML file path or pasted HTML text supplied by the operator.

Live old.reddit/CloakBrowser/proxy execution remains separately gated.

## Non-Claims

This closeout is not live Reddit access, operator-supplied pilot completion,
CloakBrowser/proxy validation, Reddit `.json` intake authorization, broad
crawling, Source Capture Armory execution, Source Capture Packet output,
automatic promotion, Data Capture handoff, ECR, Cleaning, Judgment,
source-quality scoring, fixture admission, commercial-use permission,
deployment, production runtime, commit authorization, push authorization, or PR
authorization.
