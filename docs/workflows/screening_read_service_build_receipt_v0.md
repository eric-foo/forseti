# Screening Read Service Build Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow build receipt
scope: >
  Records the 2026-06-21 bounded screening-read service and screening-browser
  wrapper build: entry points, boundaries, validation, first-act old Reddit
  receipt, and clean-agent usage pointers.
use_when:
  - A clean agent needs to use or review the screening-read service.
  - Checking the no-packet/no-ECR boundary for screening posture.
  - Replaying the old Reddit extraction and Cloudflare visible-text findings.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/screening_reddit_read_route_decision_v0.md
  - orca-harness/source_capture/screening_read.py
  - orca-harness/source_capture/screening_browser_read.py
  - orca-harness/source_capture/screening_extraction.py
  - docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md
branch_or_commit: codex/screening-read-service-build; initial implementation commit 5f10d5be07b6e4401f0cd0e8de42d544318d5a77
stale_if:
  - The screening-read service API changes.
  - `cloakbrowser_snapshot.py` changes the snapshot result shape.
  - `block_shell.py` changes Cloudflare/interstitial classification.
  - Old Reddit search/listing markup changes candidate title or datetime locators.
```

## Status

Status: `IMPLEMENTED_ON_PR_BRANCH`.

Implementation branch: `codex/screening-read-service-build`.
Draft PR: `https://github.com/eric-foo/orca/pull/324`.

This receipt records what was built on the PR branch. It is not a merge,
acceptance, runtime-readiness, source-proof, or production-service claim.

## Entry Points

- `source_capture.screening_read.screening_read(...)` is the consolidated
  orchestrator-invoked screening-read service for `reddit_screening_read`,
  `direct_http`, and `anti_blocking_http`.
- `source_capture.screening_read.close_old_reddit_search_surface_receipt(...)`
  is the first-act helper for the route-decision residual.
- `source_capture.screening_browser_read.screening_browser_read(...)` is the
  CloakBrowser-backed screening browser wrapper for public pages that need a
  browser/interstitial rung.
- `source_capture.screening_extraction.extract_screening_fields(...)` owns
  bounded locator-style extraction, including old Reddit candidate rows.

Minimal usage shape:

```python
from source_capture.screening_read import (
    ScreeningReadDispatch,
    ScreeningReadRoute,
    screening_read,
)

dispatch = ScreeningReadDispatch(
    screen_id="screen-123",
    question="What does this one public source say about the candidate?",
)

result = screening_read(
    url="https://old.reddit.com/r/beauty/search?q=moisturizer&restrict_sr=on&sort=new",
    route=ScreeningReadRoute.REDDIT_SCREENING_READ,
    dispatch=dispatch,
)
```

Browser/interstitial rung:

```python
from source_capture.screening_browser_read import screening_browser_read

result = screening_browser_read(
    url="https://example.com/public-page",
    dispatch=dispatch,
)
```

## Boundary

The service is screening posture only:

- orchestrator-invoked, not walker-direct;
- one screen, one source, one bounded question;
- logged-out public URLs only;
- entitlement gate before fetch;
- human-rate;
- no standing service, crawler, scheduler, monitor, dashboard, or production
  runtime;
- no new fetch/search infrastructure;
- no Source Capture Packet, packet manifest, packet staging, ECR, Cleaning, or
  Judgment touch.

The browser wrapper passes `proxy_profile=None` and `pre_capture=None` to
`cloakbrowser_snapshot` and returns visible text. It does not return DOM,
screenshots, packet paths, manifests, or ECR fields.

## Findings Encoded

`block_shell` is applied to rendered visible text for
`screening_browser_read(...)`, not to full DOM. A passed Cloudflare page can
retain `/cdn-cgi/challenge-platform/` scripts in the DOM; classifying the DOM
would false-positive `BLOCK_SHELL` after the visible page is usable.

Old Reddit extraction is locator-targeted and range-sane. Candidate rows come
from old Reddit result containers (`thing` or `search-result`) and title anchors
(`title` or `search-title`). Submission date comes from the targeted `<time>`
inside that candidate container. Do not compute `min()` over all page datetimes:
sidebar widgets can expose old subreddit-creation dates such as 2011 and pollute
the result.

## First-Act Receipt

The first-act helper was run live against:

`https://old.reddit.com/r/beauty/search?q=skincare+moisturizer&restrict_sr=on&sort=new`

Observed result:

- status: `200`;
- byte count: `112317`;
- content class: `content_unverified`;
- `/comments/` marker count: `75`;
- old Reddit thread candidate count: `0`.

This closed the old.reddit search-surface residual as a screening-read service
receipt. It wrote no packet, manifest, ECR artifact, or disk artifact.

## Validation

Targeted unit bundle:

```text
python -m pytest -q tests\unit\test_screening_read_service.py tests\unit\test_screening_browser_read.py tests\unit\test_screening_reddit_read.py
40 passed
```

Expanded capture-adapter bundle:

```text
python -m pytest -q tests\unit\test_screening_read_service.py tests\unit\test_screening_browser_read.py tests\unit\test_screening_reddit_read.py tests\unit\test_block_shell.py tests\unit\test_anti_blocking_http_adapter.py tests\unit\test_source_capture_direct_http.py tests\unit\test_source_capture_cloakbrowser_snapshot.py
130 passed
```

`git diff --check` exited `0`; Git warned only that LF would replace CRLF in
some files.

## Source Drift Note

The build commission referenced an "Old Reddit Post-Date (Submission Date)
Rule" in
`docs/workflows/reddit_candidate_intake_old_reddit_search_surface_handling_v0.md`.
That section was not present in the checked-out source before this propagation
patch. This branch adds the rule to that workflow note so future agents have a
durable source for the targeted-date and range-sanity behavior.

## Non-Claims

This receipt is not validation, readiness, merge acceptance, production runtime,
source completeness proof, source-quality scoring, fixture admission, capture
authorization beyond the commissioned build, broad crawling authorization, ECR,
Cleaning, Judgment, buyer proof, or commercial-use permission.
