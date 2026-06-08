# Reddit Candidate Intake Subreddit Projection B2B 001 Closeout v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow closeout
scope: >
  Records the first no-live candidate subreddit projection for the B2B Reddit
  Candidate URL Intake lane, using `r/b2bmarketing` as the seed subreddit.
use_when:
  - Resuming candidate subreddit projection after the B2B thread-candidate pilot.
  - Checking whether `r/b2bmarketing` has been emitted as a planning-only
    candidate subreddit row.
  - Distinguishing seed subreddit projection from recommended/correlated
    subreddit discovery.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md
  - docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - docs/product/data_capture_spine_candidate_url_intake_contract_v0.md
  - orca-harness/_test_runs/reddit_candidate_subreddit_discovery_b2b_001/reddit_candidate_url_intake.json
  - orca-harness/_test_runs/reddit_candidate_subreddit_discovery_b2b_001/reddit_candidate_url_intake_receipt.md
stale_if:
  - Candidate subreddit row fields change.
  - Subreddit projection is rerun against a different source input.
  - A later run emits recommended/correlated subreddit rows.
```

## Status

Status: `SEED_SUBREDDIT_PROJECTION_COMPLETE`.

This closeout records seed candidate subreddit projection only. It does not
claim that recommended, correlated, related, or "more like this" B2B subreddits
were found.

## Implementation Slice

Implemented the smallest complete projection support:

- `CandidateSubredditRow` now carries optional visible volume fields:
  - `visible_subscriber_count_or_none`;
  - `visible_active_user_count_or_none`;
  - `visible_volume_signal_absent_reason_or_none`.
- `project_old_reddit_html_candidate_subreddits` emits candidate subreddit rows
  from declared candidate surfaces only.
- Seed subreddit projection can emit the declared seed subreddit as a
  planning-only candidate row.
- Declared related/recommended-style projection rejects header navigation,
  popular bars, account chrome, and footer links by requiring a declared
  surface container.

## Observed Validation

Command:

```text
python -m pytest -p no:cacheprovider tests/unit/test_reddit_candidate_intake.py tests/contract/test_reddit_candidate_intake_contract.py
..................                                                       [100%]
18 passed in 0.20s
```

## Observed Projection

Input:

```text
docs/_inbox/reddit_candidate_intake_operator_inputs/reddit_candidate_pilot_001_b2bmarketing_meetings_old_reddit.html
```

Run output:

```text
candidate_subreddits=1
json_path=_test_runs\reddit_candidate_subreddit_discovery_b2b_001\reddit_candidate_url_intake.json
receipt_path=_test_runs\reddit_candidate_subreddit_discovery_b2b_001\reddit_candidate_url_intake_receipt.md
row=b2bmarketing|subscribers=None|active=None|absent=visible_volume_not_present_on_declared_surface
```

Related-surface sanity check against the same saved HTML:

```text
related_candidate_subreddits=0
```

Interpretation: the saved page did not expose a declared related-subreddit
surface. The projection correctly avoided turning header/navigation/popular
links into B2B subreddit recommendations.

## Output Readback

Receipt:

```text
Run ID: reddit_candidate_subreddit_discovery_b2b_001
Cap type: probe
Coverage claim: bounded_probe_only
Stop reason: scope_exhausted
Candidate subreddits: 1
Candidate threads: 0
Outbound URL candidates: 0
```

Candidate row:

```yaml
candidate_subreddit: b2bmarketing
source_surface: seed_subreddits
source_url: https://old.reddit.com/r/b2bmarketing/
visible_subscriber_count_or_none: null
visible_active_user_count_or_none: null
visible_volume_signal_absent_reason_or_none: visible_volume_not_present_on_declared_surface
same_run_traversal_authorized: false
allowed_downstream_use: planning_only
```

## Output Hashes

```yaml
reddit_candidate_url_intake_json: 66C5B694A5B42E644DE7CC81758DD79B23CFBF7DE4AC6BA171D8FC7D3F898B6A
reddit_candidate_url_intake_receipt_md: 3EFD4BC1B5EC47CEE02D3B3B91B5D4BD66FD8601613203410C79ED157DA8FCAA
```

## Boundary Checks

Forbidden-output scan for raw HTML, parser output, author/profile/user fields,
comments/body fields, logged-in account markers, and known navigation subreddit
noise returned no matches.

The output is candidate/provenance only:

- one seed candidate subreddit row;
- no candidate thread rows;
- no outbound URL rows;
- no raw HTML;
- no thread body;
- no comments;
- no user/profile/author data;
- no Source Capture Packet output;
- no Source Capture Armory execution;
- no auto-promotion;
- no Data Capture handoff;
- no same-run traversal.

## Next Decision

To find recommended/correlated B2B subreddits with volume, run a separate
no-live candidate-subreddit discovery pilot from an operator-supplied page that
visibly contains a declared related, recommendation, more-like-this, cross-post,
or subreddit-search surface. This seed projection does not provide that surface.

## Non-Claims

This closeout is not recommended-subreddit discovery, not correlated-subreddit
discovery, not visible-volume proof, not broad crawling, not thread capture, not
comment capture, not user/profile capture, not raw HTML persistence by
Candidate URL Intake, not Reddit `.json` intake, not live Reddit access by
Candidate URL Intake, not CloakBrowser/proxy validation, not Source Capture
Armory execution, not Source Capture Packet output, not Data Capture handoff,
not ECR, not Cleaning, not Judgment, not source-quality scoring, not fixture
admission, not commercial-use permission, not promotion, not capture
authorization, not deployment, not production runtime, not commit authorization,
not push authorization, and not PR authorization.
