from __future__ import annotations

# First-act live receipt: one bounded logged-out GET on the old.reddit search surface.
# This closes the capture-lane residual documented in capture_recon_index_v0.md
# (Reddit thread DISCOVERY row, "Residual" paragraph).
#
# Run manually to produce the receipt; NOT included in CI (requires outbound network).
# Usage: pytest tests/integration/test_reddit_screening_read_live.py -v -s
#
# Commission reference: §7 validation — "the first-act live search GET as a bounded
# human-rate receipt."

import pytest

from source_capture.screening_reddit_read import RedditScreenLight, reddit_screening_read

pytestmark = pytest.mark.integration


LIVE_SEARCH_URL = (
    "https://old.reddit.com/r/beauty/search"
    "?q=skincare+moisturizer&restrict_sr=on&sort=new"
)


@pytest.mark.skip(reason="Live network — run manually to produce the first-act receipt")
def test_first_act_live_reddit_search_receipt() -> None:
    """
    Bounded logged-out GET on old.reddit search surface.

    Receipt fields recorded: status / byte_count / comments_marker_count /
    rate_ceiling_note. Confirms direct-HTTP rung is GO for the search surface
    (the one unproven leg from capture_recon_index_v0.md).
    """
    result = reddit_screening_read(
        url=LIVE_SEARCH_URL,
        timeout_seconds=20.0,
        max_bytes=500_000,
    )

    print("\n--- FIRST-ACT LIVE RECEIPT ---")
    print(f"url:                   {LIVE_SEARCH_URL}")

    if isinstance(result, RedditScreenLight):
        print(f"status:                {result.status}")
        print(f"final_url:             {result.final_url}")
        print(f"byte_count:            {result.byte_count}")
        print(f"comments_marker_count: {result.comments_marker_count}")
        print(f"rate_ceiling_note:     {result.rate_ceiling_note}")
        print("--- END RECEIPT ---\n")

        assert result.status == 200, (
            f"Expected HTTP 200 from old.reddit search surface; got {result.status}. "
            "If gated, escalate to visible-browser rung per recon index pattern 1."
        )
        assert result.byte_count > 0, "Expected non-empty body from old.reddit search."
        # comments markers may be 0 if the search returns no results for the query,
        # but the surface should still be reachable.
        print(
            f"RECEIPT: HTTP {result.status}, {result.byte_count} bytes, "
            f"{result.comments_marker_count} /comments/ markers. "
            f"Rate ceiling: {result.rate_ceiling_note}"
        )
    else:
        print(f"REFUSED: reason={result.reason!r}, message={result.message}")
        print("--- END RECEIPT ---\n")
        pytest.fail(
            f"Live old.reddit search GET was refused: {result.reason!r} — {result.message}. "
            "Check entitlement gate logic or escalate per recon index."
        )
