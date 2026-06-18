# Reddit Candidate Intake Subreddit Projection SEO 002 Closeout v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow closeout
scope: >
  Records the bounded `r/SEO` old Reddit sidebar-related subreddit projection
  pilot for Reddit Candidate URL Intake.
use_when:
  - Checking whether old Reddit sidebar markdown related links may be projected
    as candidate subreddit rows.
  - Distinguishing structural candidate projection from semantic relevance
    filtering or promotion.
  - Resuming B2B-adjacent subreddit discovery after the `r/b2bmarketing` seed
    projection.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md
  - orca/product/spines/capture/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - orca-harness/_test_runs/reddit_candidate_subreddit_discovery_seo_002/reddit_candidate_url_intake.json # nonresolving: gitignored run scratch
  - orca-harness/_test_runs/reddit_candidate_subreddit_discovery_seo_002/reddit_candidate_url_intake_receipt.md # nonresolving: gitignored run scratch
stale_if:
  - Candidate subreddit row fields change.
  - Old Reddit sidebar markup changes.
  - A later projection layer adds semantic relevance labels or suppression rules.
```

## Status

Status: `SIDEBAR_RELATED_SUBREDDIT_PROJECTION_COMPLETE`.

This closeout records candidate subreddit projection from a declared old Reddit
sidebar markdown surface. It does not claim semantic scoring, promotion, thread
capture, body capture, or recommended-subreddit sufficiency.

## Access Note

The `r/SEO` input was acquired by a bounded single-page shell fetch of:

```text
https://old.reddit.com/r/SEO/
```

The first sandboxed fetch failed with a connection refusal. The approved
escalated fetch succeeded and wrote the raw old Reddit HTML to scratch input:

```text
docs/_inbox/reddit_candidate_intake_operator_inputs/reddit_candidate_pilot_002_seo_old_reddit.html
```

The raw HTML is input material only. It contains Reddit page configuration and
must not be promoted, committed as a fixture, treated as a Source Capture Packet,
or used as Data Capture input.

## Implementation Slice

The parser now supports:

- declared related/recommendation/cross-post/search containers with nested HTML;
- old Reddit sidebar markdown links inside the subreddit titlebox/usertext area
  as `related_subreddit` candidates when that surface is declared;
- exclusion of header navigation, popular bars, footer links, search forms,
  moderator contact links, and the current subreddit self-link;
- visible subreddit volume capture only from old Reddit `titlebox` number spans,
  so listing score spans are not mistaken for subscriber counts.

The delegated review-and-patch sidecar found a real containment issue in the
prior related-surface depth handling. Home adjudication kept the containment
intent but replaced the raw stack patch with explicit region-depth tracking and
regression tests.

## Observed Validation

Command:

```text
python -m pytest -p no:cacheprovider tests/unit/test_reddit_candidate_intake.py tests/contract/test_reddit_candidate_intake_contract.py
.....................                                                    [100%]
21 passed in 0.11s
```

## Observed Projection

Run output:

```text
candidate_subreddits=4
row=webmarketing|surface=related_subreddit|traverse=False
row=socialmedia|surface=related_subreddit|traverse=False
row=PPC|surface=related_subreddit|traverse=False
row=analytics|surface=related_subreddit|traverse=False
json_path=_test_runs\reddit_candidate_subreddit_discovery_seo_002\reddit_candidate_url_intake.json
receipt_path=_test_runs\reddit_candidate_subreddit_discovery_seo_002\reddit_candidate_url_intake_receipt.md
```

Receipt:

```text
Run ID: reddit_candidate_subreddit_discovery_seo_002
Cap type: probe
Coverage claim: bounded_probe_only
Stop reason: scope_exhausted
Candidate subreddits: 4
Candidate threads: 0
Outbound URL candidates: 0
```

## Semantic Planning Note

From the candidate names alone, `/r/webmarketing` is the most directly related
candidate for the current B2B marketing discovery theme. That observation is a
planning note only:

- it is not a source-quality score;
- it is not a relevance score emitted by Candidate URL Intake;
- it does not suppress `/r/socialmedia`, `/r/PPC`, or `/r/analytics` from the
  declared candidate output;
- it does not authorize same-run traversal into `/r/webmarketing`;
- it does not promote `/r/webmarketing` into a capture unit.

A later projection or planning layer may use this note to choose the next
bounded seed subreddit run.

## Boundary Checks

The output is candidate/provenance only:

- four candidate subreddit rows;
- no candidate thread rows;
- no outbound URL rows;
- no raw HTML;
- no body/comment/profile/user data;
- no Source Capture Packet output;
- no Source Capture Armory execution;
- no auto-promotion;
- no Data Capture handoff;
- no same-run traversal.

## Non-Claims

This closeout is not broad Reddit crawling, not general subreddit discovery, not
semantic candidate scoring, not source-quality scoring, not capture
authorization, not promotion, not fixture admission, not commercial-use
permission, not ECR, not Cleaning, not Judgment, not Source Capture Armory
execution, not Source Capture Packet output, not Data Capture handoff, not
deployment, not production runtime, not commit authorization, not push
authorization, and not PR authorization.
