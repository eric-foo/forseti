# Reddit Candidate Intake No-Live Dry-Use Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow validation receipt
scope: >
  Records the first no-live dry-use of old Reddit static HTML projection through
  Candidate URL Intake output assembly and writer readback.
use_when:
  - Checking whether the bounded Reddit Candidate URL Intake foundation has a local end-to-end dry-use signal.
  - Deciding whether to scope the next layer above foundation for Candidate URL Intake.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md
  - orca/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
  - orca-harness/tests/unit/test_reddit_candidate_intake.py
  - orca-harness/tests/fixtures/reddit_candidate_intake/old_reddit_listing_noisy.html
downstream_consumers:
  - docs/workflows/reddit_candidate_intake_operator_pilot_plan_v0.md
```

## Receipt

Status: `NO_LIVE_DRY_USE_FOUNDATION_PRESENT`.

This receipt records a local dry-use foundation only. It is not live Reddit
access, source-access readiness, deployment readiness, fixture admission,
Source Capture Armory authorization, Source Capture Packet permission, Data
Capture handoff, ECR, Cleaning, Judgment, or source-quality scoring.

## Dry-Use Shape

The dry-use exercises the public Candidate URL Intake package surface:

1. Read one static old Reddit HTML fixture:
   `orca-harness/tests/fixtures/reddit_candidate_intake/old_reddit_listing_noisy.html`.
2. Construct a declared, capped `RunEnvelope`.
3. Project the fixture with `project_old_reddit_html_listing`.
4. Assemble output with `build_candidate_intake_output`.
5. Write and read back output with `write_candidate_intake_output`.
6. Assert candidate-only rows, provenance, stop reason, and forbidden-output
   absence.

The fixture intentionally includes valid thread candidates plus noise:

- author/user-looking elements;
- selftext/body/comment-looking text;
- outbound link noise;
- `.json` listing noise;
- a beyond-cap candidate.

## Observed Validation

Command observed from `orca-harness/`:

```text
python -m pytest -p no:cacheprovider tests/unit/test_reddit_candidate_intake.py tests/contract/test_reddit_candidate_intake_contract.py
...............                                                          [100%]
15 passed in 0.07s
```

The dry-use test added in this slice is:

```text
test_no_live_dry_use_projects_fixture_through_writer_with_candidate_only_output
```

## Success Signals Checked

The local dry-use asserts:

- output contains candidate thread URL rows only for projected thread
  candidates;
- output preserves `source_surface = reddit_search_listing`;
- output preserves `allowed_downstream_use = planning_only`;
- output preserves `same_run_traversal_authorized = false`;
- provenance records `stop_reason = caps_reached`;
- provenance records row counts for candidate subreddits, candidate threads,
  and outbound URLs;
- receipt readback records `Candidate threads: 2`;
- receipt readback records `Stop reason: caps_reached`;
- output non-claims include `not Source Capture Packet output`;
- output non-claims include `not Data Capture handoff`;
- raw HTML is not persisted;
- body/comment/selftext-like fixture text is not persisted;
- user/profile/author-looking fixture values are not persisted;
- `.json` fixture noise is not emitted;
- outbound-link fixture noise is not emitted;
- beyond-cap candidate is not emitted.

## Foundation Assessment

This is enough foundation to evaluate the next layer above foundation because
the current lane now has:

- an architecture and parent contract;
- default-policy decision coverage;
- implementation skeleton;
- old Reddit static projection;
- `.json` refusal;
- no-live/no-Armory contract tests;
- delegated review and CA adjudication for the projection slice;
- one local no-live dry-use that runs projection through writer readback.

The layer above foundation should not be another foundation artifact by
default. The next layer is an **operator pilot / bounded-run layer**, defined in
`docs/workflows/reddit_candidate_intake_operator_pilot_plan_v0.md`: deciding
which single bounded old Reddit intake run to exercise next, under no-live or
live-access constraints depending on owner authorization.

## Non-Claims

This receipt does not claim:

- live Reddit access;
- CloakBrowser/proxy validation;
- Reddit `.json` intake authorization;
- broad Reddit crawling;
- thread body/comment capture;
- user/profile capture;
- Source Capture Armory execution;
- Source Capture Packet output;
- fixture admission;
- automatic promotion into capture units;
- Data Capture Spine handoff;
- ECR, Cleaning, Judgment, or source-quality behavior;
- commercial-use permission;
- deployment or production readiness.
