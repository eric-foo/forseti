# Reddit Candidate Intake Operator Pilot 001 Executed Closeout v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow closeout
scope: >
  Records the first real no-live operator-supplied old Reddit HTML pilot for
  bounded Reddit Candidate URL Intake.
use_when:
  - Resuming from the first operator-supplied Reddit Candidate URL Intake pilot.
  - Deciding whether candidate output from `r/b2bmarketing` justifies a
    promotion gate, narrower pilot, or bounded live-access pilot.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/reddit_candidate_intake_operator_pilot_parameter_packet_v0.md
  - forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md
  - forseti/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - forseti-harness/_test_runs/reddit_candidate_pilot_001_operator_supplied_html/reddit_candidate_url_intake.json # nonresolving: gitignored run scratch
  - forseti-harness/_test_runs/reddit_candidate_pilot_001_operator_supplied_html/reddit_candidate_url_intake_receipt.md # nonresolving: gitignored run scratch
stale_if:
  - The output artifacts are regenerated.
  - The parser or Candidate URL Intake contract changes candidate row semantics.
```

## Status

Status: `REAL_NO_LIVE_OPERATOR_PILOT_COMPLETE_CAPS_REACHED`.

The pilot consumed an operator-supplied static HTML file saved from old Reddit.
Candidate URL Intake did not fetch Reddit, invoke CloakBrowser/proxy, invoke
Source Capture Armory, read a thread page as input, call a `.json` endpoint, or
emit a Source Capture Packet.

## Pilot Closeout

```yaml
pilot_closeout:
  run_id: reddit_candidate_pilot_001
  mode: pilot_no_live_operator_supplied_html
  declared_topic_theme_query: "B2B marketing meetings generation / outbound pipeline growth"
  seed_subreddits:
    - b2bmarketing
  source_surface: reddit_search_listing
  source_url: "https://old.reddit.com/r/b2bmarketing/search/?q=meetings&restrict_sr=on&sort=top&t=year"
  html_input_reference: docs/_inbox/reddit_candidate_intake_operator_inputs/reddit_candidate_pilot_001_b2bmarketing_meetings_old_reddit.html
  html_input_sha256: B3DFAE7AF3DC3620786D95A0500646C1FF5D6CC58B0E554D056F03CA9D965C09
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
  method_category: static_old_reddit_html_operator_supplied
  row_counts:
    candidate_subreddits: 0
    candidate_threads: 25
    outbound_urls: 0
  stop_reason: caps_reached
  output_artifacts:
    json_path: orca-harness/_test_runs/reddit_candidate_pilot_001_operator_supplied_html/reddit_candidate_url_intake.json
    receipt_path: orca-harness/_test_runs/reddit_candidate_pilot_001_operator_supplied_html/reddit_candidate_url_intake_receipt.md
  output_hashes:
    reddit_candidate_url_intake_json: D79ACF39FCD8B96FA1D00263615D9B79E720AD244BD0910A48B3B9FC1E227824
    reddit_candidate_url_intake_receipt_md: 025824505F0BD622996938F213CA70AE7497A93BBEF75539D450B6BE90187776
  forbidden_output_checks:
    raw_html_absent: observed_no_match
    body_comment_absent: observed_no_match
    user_profile_absent: observed_no_match
    source_capture_packet_absent: non_claim_only_no_packet_artifact
    data_capture_handoff_absent: non_claim_only_no_handoff_artifact
  operator_decision:
    promote_candidate_now: deferred
    reason: >
      The pilot reached the probe cap and produced candidate URLs. Candidate
      selection still requires a separate promotion gate.
```

## Observed Execution

The first run against the saved search page produced zero rows because old
Reddit search result titles use `search-title`, while the parser previously
recognized only `title`. Treating that as a true empty result would have hidden
a parser-surface gap.

Smallest complete implementation patch applied:

- `orca-harness/capture_spine/reddit_candidate_intake/projection.py` now
  recognizes `search-title` anchors as candidate title anchors;
- `orca-harness/tests/unit/test_reddit_candidate_intake.py` now covers
  `search-title` while still ignoring `search-comments` and thumbnail links.

Validation after the patch:

```text
python -m pytest -p no:cacheprovider tests/unit/test_reddit_candidate_intake.py tests/contract/test_reddit_candidate_intake_contract.py
................                                                         [100%]
16 passed in 0.11s
```

Pilot rerun result:

```text
rows=25
stop_reason=caps_reached
json_path=_test_runs\reddit_candidate_pilot_001_operator_supplied_html\reddit_candidate_url_intake.json
receipt_path=_test_runs\reddit_candidate_pilot_001_operator_supplied_html\reddit_candidate_url_intake_receipt.md
first_candidate=https://old.reddit.com/r/b2bmarketing/comments/1mk4ivy/a_friend_of_mine_closed_a_72k_deal_from_a/
```

Receipt readback:

```text
Run ID: reddit_candidate_pilot_001
Cap type: probe
Coverage claim: bounded_probe_only
Stop reason: caps_reached
Candidate subreddits: 0
Candidate threads: 25
Outbound URL candidates: 0
```

Output row-count readback:

```text
candidate_subreddits 0
candidate_threads 25
outbound_urls 0
stop_reason caps_reached
```

First three candidate URLs:

```text
https://old.reddit.com/r/b2bmarketing/comments/1mk4ivy/a_friend_of_mine_closed_a_72k_deal_from_a/
https://old.reddit.com/r/b2bmarketing/comments/1szt837/marketing_is_slowly_turning_into_engineering_and/
https://old.reddit.com/r/b2bmarketing/comments/1rqglht/i_run_cold_email_for_49_clients_right_now_heres/
```

The operator-supplied topic-context thread URL also appeared as a candidate row
because it was present in the saved search listing. It was not used as an intake
input.

## Boundary Checks

Observed output scan for raw HTML, parser output, author fields, user/profile
fields, comments fields, body fields, and the rejected thread title found no
forbidden output. The scan did find the originally supplied thread URL as a
candidate URL, which is allowed.

The output is candidate/provenance only:

- 0 candidate subreddit rows;
- 25 candidate thread URL rows;
- 0 outbound URL rows;
- no raw HTML;
- no thread body;
- no comments;
- no user/profile/author fields;
- no Source Capture Packet artifact;
- no Source Capture Armory execution;
- no Data Capture handoff;
- no ECR, Cleaning, Judgment, fixture admission, or source-quality score.

## Meaning

The first real no-live operator pilot succeeded at producing bounded candidate
thread URLs from an operator-supplied old Reddit search page. `caps_reached` is
not a coverage or sufficiency claim. It means the probe found at least the cap
limit and stopped.

The next decision is not more intake by default. The next decision is whether to:

1. open a separate promotion gate for one or more candidate URLs;
2. run a narrower or differently sorted no-live pilot if the candidate set is
   too broad;
3. scope a bounded live-access pilot only if live access is needed to improve
   candidate intake usefulness.

## Non-Claims

This closeout is not broad Reddit crawling, not thread capture, not comment
capture, not user/profile capture, not raw HTML persistence by Candidate URL
Intake, not Reddit `.json` intake, not live Reddit access by Candidate URL
Intake, not CloakBrowser/proxy validation, not Source Capture Armory execution,
not Source Capture Packet output, not Data Capture handoff, not ECR, not
Cleaning, not Judgment, not source-quality scoring, not fixture admission, not
commercial-use permission, not promotion, not capture authorization, not
deployment, not production runtime, not commit authorization, not push
authorization, and not PR authorization.
