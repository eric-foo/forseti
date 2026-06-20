# Reddit Candidate Intake Operator Pilot Parameter Packet v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow parameter packet
scope: >
  Captures the smallest complete parameters needed to run one no-live bounded
  Reddit Candidate URL Intake operator pilot.
use_when:
  - Filling the first operator pilot run before executing Candidate URL Intake.
  - Checking whether the pilot has enough declared inputs to run without scope drift.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/reddit_candidate_intake_operator_pilot_plan_v0.md
  - docs/workflows/reddit_candidate_intake_no_live_dry_use_receipt_v0.md
  - orca/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
stale_if:
  - The operator pilot plan changes required parameters, stop gates, or live-access posture.
  - The operator supplies final HTML input, requiring this packet to be completed or superseded.
```

## Status

Status: `PILOT_PARAMETERS_FILLED_EXECUTED_CAPS_REACHED`.

The operator selected `r/b2bmarketing` as the seed subreddit and supplied a
thread URL as topic context. The thread URL was not used as intake input. The
pilot used the valid old Reddit search/listing URL below and the matching
operator-supplied static HTML file.

## Pilot Parameters

```yaml
pilot_parameters:
  run_id: reddit_candidate_pilot_001
  mode: pilot_no_live_operator_supplied_html
  seed_subreddits:
    - b2bmarketing

  planning_intent:
    declared_topic_theme_query: "B2B marketing meetings generation / outbound pipeline growth"
    why_this_query_matters: >
      Probe whether old Reddit listing/search surfaces in a B2B marketing
      subreddit can yield planning-only candidate thread URLs about generating
      sales meetings, outbound pipeline, or demand generation execution.
    operator_decision_this_informs: >
      Decide whether Candidate URL Intake is useful enough to continue to a
      bounded live-access pilot, whether the query needs narrowing, or whether
      any candidate should later enter a separate promotion gate.
    rejected_context_url_not_used_as_input: "https://old.reddit.com/r/b2bmarketing/comments/1teaipg/went_from_0_to_35_meetingsmo_in_6_months_heres/"

  source_input:
    source_surface: reddit_search_listing
    old_reddit_source_url: "https://old.reddit.com/r/b2bmarketing/search/?q=meetings&restrict_sr=on&sort=top&t=year"
    html_input:
      type: file_path
      value: docs/_inbox/reddit_candidate_intake_operator_inputs/reddit_candidate_pilot_001_b2bmarketing_meetings_old_reddit.html
    known_input_limitations:
      - operator_supplied_static_html_required
      - html_file_observed_for_execution
      - source_url_declared_not_live_verified_by_candidate_intake
      - thread_url_used_only_as_topic_context_not_intake_input

  bounds:
    cap_type: probe
    coverage_claim: bounded_probe_only
    max_subreddits: 5
    max_threads_per_subreddit: 25
    max_pages_or_result_surfaces: 2
    time_window_days: 30
    sort_order: top
    exclusions: []

  allowed_surfaces:
    candidate_surface_allowlist:
      - reddit_search_listing

  expected_stop:
    stop_reason_if_candidates_found: caps_reached
    stop_reason_if_no_candidates: empty_result
    stop_reason_if_input_blocked: blocked_result
    caps_are_sufficiency_claim: no

  output_expectations:
    output_directory: orca-harness/_test_runs/reddit_candidate_pilot_001
    allowed_outputs:
      - candidate_thread_url_rows
      - run_provenance_receipt
      - local_json_output
      - local_markdown_receipt
    forbidden_outputs:
      - raw_html
      - parser_output
      - thread_body
      - comments
      - user_profile_or_author_data
      - source_capture_packet
      - data_capture_handoff
      - ecr_cleaning_judgment
      - source_quality_score

  promotion_posture:
    promote_candidate_now: deferred
    promotion_requires_separate_gate: yes
```

## Execution Gate

This packet was used for a no-live pilot after:

1. `source_input.html_input.value` exists on disk and contains saved/static HTML
   for the declared old Reddit source URL;
2. any non-empty `bounds.exclusions`, if applicable;
3. any lower caps, if the operator wants stricter-than-probe limits.

The executed pilot closeout records `caps_reached`, not completion, sufficiency,
or topic coverage.

## Acceptance Checks

Before execution, confirm:

- the source URL is old Reddit listing/search, not a thread page;
- the source URL is not a Reddit `.json` URL;
- the HTML input is static/operator-supplied, not fetched by Candidate URL
  Intake;
- no live Reddit, CloakBrowser, proxy, Source Capture Armory, archive, API, or
  browser runner is invoked;
- `candidate_surface_allowlist` includes only `reddit_search_listing` for this
  first pilot;
- caps stay at or below `probe` defaults;
- `coverage_claim` remains `bounded_probe_only`;
- output directory is local scratch/workflow output, not durable corpus,
  packet, fixture-admission, or Data Capture storage.

## Pilot Closeout Required Fields

When the pilot is executed, the closeout must record:

```yaml
pilot_closeout_required_fields:
  run_id: reddit_candidate_pilot_001
  mode: pilot_no_live_operator_supplied_html
  declared_topic_theme_query: "B2B marketing meetings generation / outbound pipeline growth"
  source_surface: reddit_search_listing
  old_reddit_source_url: "https://old.reddit.com/r/b2bmarketing/search/?q=meetings&restrict_sr=on&sort=top&t=year"
  html_input_reference: docs/_inbox/reddit_candidate_intake_operator_inputs/reddit_candidate_pilot_001_b2bmarketing_meetings_old_reddit.html
  caps_applied:
    max_subreddits: 5
    max_threads_per_subreddit: 25
    max_pages_or_result_surfaces: 2
    time_window_days: 30
  sort_order: top
  row_counts:
    candidate_subreddits:
    candidate_threads:
    outbound_urls:
  stop_reason:
  output_artifacts:
    json_path:
    receipt_path:
  forbidden_output_checks:
    raw_html_absent:
    body_comment_absent:
    user_profile_absent:
    source_capture_packet_absent:
    data_capture_handoff_absent:
  operator_decision:
    promote_candidate_now: yes | no | deferred
    reason:
```

## Non-Claims

This packet is not validation, readiness, live Reddit authorization,
CloakBrowser/proxy authorization, Source Capture Armory authorization, Source
Capture Packet output, Data Capture handoff, ECR, Cleaning, Judgment,
source-quality scoring, fixture admission, broad crawling, commercial-use
permission, deployment, production runtime, commit authorization, push
authorization, or PR authorization.
