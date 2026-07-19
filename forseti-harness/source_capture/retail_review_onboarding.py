"""Shared acquisition decision for retailer PDP review onboarding.

Retailers keep ownership of sort controls, continuation controls, and row
parsing. This module decides only whether an already source-ordered review
window is sufficient for onboarding.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date, timedelta


RETAIL_REVIEW_ONBOARDING_POLICY = "recent_window_30d_then_most_recent_30"
RETAIL_REVIEW_ONBOARDING_POLICY_VERSION = "v1"
RETAIL_REVIEW_WINDOW_DAYS = 30
RETAIL_REVIEW_WINDOW_MINIMUM = 12
RETAIL_REVIEW_CONTEXT_TARGET = 30


def assess_retail_review_onboarding(
    review_dates: Sequence[date],
    *,
    reference_date: date,
    continuation_available: bool,
    source_exhausted: bool,
    structure_valid: bool,
) -> dict[str, object]:
    """Assess a Most Recent review window without prescribing browser actions."""
    dates = list(review_dates)
    cutoff = reference_date - timedelta(days=RETAIL_REVIEW_WINDOW_DAYS)
    captured_count = len(dates)
    in_window_count = sum(review_date >= cutoff for review_date in dates)
    historical_count = captured_count - in_window_count
    newest = dates[0] if dates else None
    oldest = dates[-1] if dates else None
    descending = all(
        dates[index] >= dates[index + 1]
        for index in range(max(0, captured_count - 1))
    )

    if (
        not structure_valid
        or not dates
        or not descending
        or captured_count > RETAIL_REVIEW_CONTEXT_TARGET
    ):
        status = "invalid"
    elif (
        captured_count >= RETAIL_REVIEW_CONTEXT_TARGET
        and oldest is not None
        and oldest >= cutoff
    ):
        # At the cap with the oldest row still on or inside the window, the
        # 30-day cohort is not proven complete (more rows may share the oldest
        # date), so the receipt is truthfully truncated rather than complete.
        status = "recent_window_truncated"
    elif oldest is not None and oldest < cutoff:
        # in_window_count is inclusive of the cutoff day (>= cutoff), so the
        # cohort is proven complete only after observing a row strictly older
        # than the cutoff; oldest == cutoff may still hide same-day in-window
        # rows behind the continuation control.
        if in_window_count >= RETAIL_REVIEW_WINDOW_MINIMUM:
            status = "recent_window_complete"
        elif captured_count >= RETAIL_REVIEW_CONTEXT_TARGET:
            status = "historical_context_complete"
        elif source_exhausted:
            status = "source_exhausted"
        elif continuation_available:
            status = "needs_more_historical_context"
        else:
            status = "invalid"
    elif source_exhausted:
        status = "source_exhausted"
    elif continuation_available:
        status = "needs_more_recent_window"
    else:
        status = "invalid"

    admitted = status in {
        "recent_window_complete",
        "recent_window_truncated",
        "historical_context_complete",
        "source_exhausted",
    }
    return {
        "policy": RETAIL_REVIEW_ONBOARDING_POLICY,
        "policy_version": RETAIL_REVIEW_ONBOARDING_POLICY_VERSION,
        "admitted": admitted,
        "status": status,
        "reference_date": reference_date.isoformat(),
        "window_days": RETAIL_REVIEW_WINDOW_DAYS,
        "cutoff_date": cutoff.isoformat(),
        "recent_window_minimum": RETAIL_REVIEW_WINDOW_MINIMUM,
        "historical_context_target": RETAIL_REVIEW_CONTEXT_TARGET,
        "captured_review_count": captured_count,
        "in_window_review_count": in_window_count,
        "historical_context_review_count": historical_count,
        "newest_review_date": newest.isoformat() if newest is not None else None,
        "oldest_review_date": oldest.isoformat() if oldest is not None else None,
        "continuation_available": continuation_available,
        "source_exhausted": source_exhausted,
        "window_truncated": status == "recent_window_truncated",
        "fallback_triggered": in_window_count < RETAIL_REVIEW_WINDOW_MINIMUM,
        "review_scope_claim": _review_scope_claim(status),
    }


def _review_scope_claim(status: str) -> str:
    if status == "recent_window_complete":
        return "all_source_ordered_reviews_in_last_30_days"
    if status == "recent_window_truncated":
        return "most_recent_30_rows;_30_day_window_incomplete"
    if status == "historical_context_complete":
        return "all_last_30_days_plus_nearest_older_context_to_30_rows"
    if status == "source_exhausted":
        return "all_source_available_rows_in_observed_most_recent_route"
    return "not_admitted"


__all__ = [
    "RETAIL_REVIEW_CONTEXT_TARGET",
    "RETAIL_REVIEW_ONBOARDING_POLICY",
    "RETAIL_REVIEW_ONBOARDING_POLICY_VERSION",
    "RETAIL_REVIEW_WINDOW_DAYS",
    "RETAIL_REVIEW_WINDOW_MINIMUM",
    "assess_retail_review_onboarding",
]
