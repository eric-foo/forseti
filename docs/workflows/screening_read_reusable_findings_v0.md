# Screening Read Reusable Findings v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow pattern note
scope: >
  Generalizes the screening-read findings for other public websites with the
  same browser-interstitial or structured-listing shape.
use_when:
  - Applying `screening_browser_read` to another public challenge-walled page.
  - Adding a same-shaped listing/search page extractor without inventing a site crawler.
  - Reviewing whether an extraction is targeted and range-sane rather than page-wide.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/screening_read_service_build_receipt_v0.md
  - forseti-harness/source_capture/screening_browser_read.py
  - forseti-harness/source_capture/screening_extraction.py
stale_if:
  - `screening_browser_read.py` changes what it classifies or returns.
  - `screening_extraction.py` changes `StructuredListingExtractionSpec` semantics.
  - A later source-access decision changes the screening/public-only boundary.
```

## Status

Status: `ACTIVE_PATTERN_NOTE`.

This is a reuse pattern for already-authorized screening reads. It is not a new
source-access route, fetcher, crawler, scheduler, packet runner, ECR path, or
site-specific authorization.

## Browser/Interstitial Pattern

Use this when a public page needs rendering to pass an interstitial or anti-bot
shell, and the page is still a logged-out public surface.

Rule: classify `block_shell` on the rendered visible text returned to screening,
not on full DOM. A passed challenge page can retain residual challenge scripts in
DOM, including paths like `/cdn-cgi/challenge-platform/`. DOM classification can
therefore false-positive `BLOCK_SHELL` after the visible page is clean.

Implementation pointer: `source_capture.screening_browser_read.screening_browser_read(...)`.
It wraps `cloakbrowser_snapshot`, passes no proxy profile and no pre-capture hook,
and returns visible text only. It does not stage packets, write manifests, return
screenshots/DOM to the caller, or touch ECR.

## Structured Listing Pattern

Use this when a public listing/search page has repeated row/card containers, and
each candidate item is represented by a row-local title link plus optional
row-local datetime.

Required evidence before adding a same-shaped extractor:

- a repeated container locator, such as a row/card class;
- a title-anchor locator inside that container;
- an optional href shape filter or canonicalizer;
- an optional row-local datetime locator;
- a fixture proving page chrome/sidebar datetimes do not pollute candidate dates;
- a range-sanity fixture when the screen has an expected date window.

Do not extract by page-wide aggregate. In particular, do not compute `min()` over
all page datetimes. That repeats the old Reddit failure mode where sidebar or
site-age widgets can look like the candidate date.

Implementation pointer:
`source_capture.screening_extraction.extract_structured_listing_candidates(...)`
with `StructuredListingExtractionSpec`.

Example shape:

```python
from source_capture.screening_extraction import (
    StructuredListingExtractionSpec,
    extract_structured_listing_candidates,
)

rows = extract_structured_listing_candidates(
    body_text=html,
    spec=StructuredListingExtractionSpec(
        container_classes=("listing-card",),
        anchor_classes=("listing-title",),
        href_must_contain=("/forums/",),
        datetime_classes=("published-at",),
        datetime_label="published datetime",
    ),
    item_min_datetime="2025-01-01T00:00:00Z",
    item_max_datetime="2026-06-21T23:59:59Z",
)
```

Returned rows are screen-light locator records: URL, title, source anchor class,
source container class, row-local datetime, datetime state, and datetime detail.
They do not include raw HTML, post/comment bodies, author profiles, packet
metadata, ECR fields, Cleaning fields, Judgment fields, scores, or semantic
meaning.

## Add-A-Site Checklist

1. Confirm the page is logged-out public content and the orchestrator has a
   bounded screen/question.
2. Pick the existing read route (`direct_http`, `anti_blocking_http`, or
   `screening_browser_read`) without adding new fetch/search infrastructure.
3. Define the structured listing spec from targeted row-local locators.
4. Add fixture tests for row extraction, page-chrome datetime pollution, and date
   range sanity.
5. Return screen-light fields only; do not emit packets, manifests, ECR, Cleaning,
   Judgment, ranking, credibility, or coverage claims.

## Non-Claims

This pattern note is not validation, readiness, source completeness proof,
commercial-use permission, broad crawling authorization, source-quality scoring,
fixture admission, Source Capture Packet output, ECR, Cleaning, Judgment, or
buyer proof.