from __future__ import annotations

from datetime import date

from source_capture.retail_review_onboarding import (
    RETAIL_REVIEW_ONBOARDING_POLICY,
    assess_retail_review_onboarding,
)


_REFERENCE_DATE = date(2026, 7, 20)


def _dates(*values: str) -> list[date]:
    return [date.fromisoformat(value) for value in values]


def test_dense_window_completes_after_crossing_cutoff() -> None:
    result = assess_retail_review_onboarding(
        _dates(
            "2026-07-19",
            "2026-07-18",
            "2026-07-17",
            "2026-07-16",
            "2026-07-15",
            "2026-07-14",
            "2026-07-13",
            "2026-07-12",
            "2026-07-11",
            "2026-07-10",
            "2026-07-09",
            "2026-07-08",
            "2026-06-19",
        ),
        reference_date=_REFERENCE_DATE,
        continuation_available=True,
        source_exhausted=False,
        structure_valid=True,
    )

    assert result["policy"] == RETAIL_REVIEW_ONBOARDING_POLICY
    assert result["status"] == "recent_window_complete"
    assert result["admitted"] is True
    assert result["in_window_review_count"] == 12
    assert result["historical_context_review_count"] == 1
    assert result["fallback_triggered"] is False


def test_thin_window_requires_historical_context_until_thirty() -> None:
    result = assess_retail_review_onboarding(
        _dates(
            "2026-07-19",
            "2026-07-01",
            "2026-06-01",
            "2026-05-01",
            "2026-04-01",
            "2026-03-01",
        ),
        reference_date=_REFERENCE_DATE,
        continuation_available=True,
        source_exhausted=False,
        structure_valid=True,
    )

    assert result["status"] == "needs_more_historical_context"
    assert result["admitted"] is False
    assert result["in_window_review_count"] == 2
    assert result["fallback_triggered"] is True


def test_thin_window_admits_thirty_most_recent_as_historical_context() -> None:
    review_dates = [
        date(2026, 7, 19),
        date(2026, 7, 1),
        *[date(2026, 6, 1) for _ in range(28)],
    ]

    result = assess_retail_review_onboarding(
        review_dates,
        reference_date=_REFERENCE_DATE,
        continuation_available=True,
        source_exhausted=False,
        structure_valid=True,
    )

    assert result["status"] == "historical_context_complete"
    assert result["captured_review_count"] == 30
    assert result["historical_context_review_count"] == 28
    assert result["review_scope_claim"] == (
        "all_last_30_days_plus_nearest_older_context_to_30_rows"
    )


def test_source_exhaustion_admits_fewer_than_thirty_without_fabricating_window() -> None:
    result = assess_retail_review_onboarding(
        _dates("2026-06-01", "2026-05-01", "2026-04-01"),
        reference_date=_REFERENCE_DATE,
        continuation_available=False,
        source_exhausted=True,
        structure_valid=True,
    )

    assert result["status"] == "source_exhausted"
    assert result["admitted"] is True
    assert result["review_scope_claim"] == (
        "all_source_available_rows_in_observed_most_recent_route"
    )


def test_dense_thirty_row_window_is_truthfully_truncated() -> None:
    result = assess_retail_review_onboarding(
        [date(2026, 7, 19) for _ in range(30)],
        reference_date=_REFERENCE_DATE,
        continuation_available=True,
        source_exhausted=False,
        structure_valid=True,
    )

    assert result["status"] == "recent_window_truncated"
    assert result["admitted"] is True
    assert result["window_truncated"] is True


def test_oldest_on_cutoff_day_keeps_loading_not_prematurely_complete() -> None:
    # Cutoff for the reference date is 2026-06-20. The oldest captured rows sit
    # exactly on that day, so more same-day in-window rows may remain behind the
    # continuation control: completeness is not proven and loading must continue.
    result = assess_retail_review_onboarding(
        [date(2026, 7, 1) for _ in range(13)]
        + [date(2026, 6, 20) for _ in range(5)],
        reference_date=_REFERENCE_DATE,
        continuation_available=True,
        source_exhausted=False,
        structure_valid=True,
    )

    assert result["cutoff_date"] == "2026-06-20"
    assert result["oldest_review_date"] == "2026-06-20"
    assert result["in_window_review_count"] == 18
    assert result["status"] == "needs_more_recent_window"
    assert result["admitted"] is False


def test_oldest_on_cutoff_day_truncates_at_cap_without_false_completion() -> None:
    # At the 30-row cap with the oldest row still on the cutoff day, the cohort
    # is unproven-complete, so the receipt is truthfully truncated, never
    # recent_window_complete.
    result = assess_retail_review_onboarding(
        [date(2026, 7, 1) for _ in range(25)]
        + [date(2026, 6, 20) for _ in range(5)],
        reference_date=_REFERENCE_DATE,
        continuation_available=True,
        source_exhausted=False,
        structure_valid=True,
    )

    assert result["status"] == "recent_window_truncated"
    assert result["window_truncated"] is True
    assert result["admitted"] is True


def test_unsorted_or_uncontinued_partial_window_fails_closed() -> None:
    unsorted = assess_retail_review_onboarding(
        _dates("2026-07-01", "2026-07-19"),
        reference_date=_REFERENCE_DATE,
        continuation_available=True,
        source_exhausted=False,
        structure_valid=True,
    )
    stranded = assess_retail_review_onboarding(
        _dates("2026-07-19", "2026-07-01"),
        reference_date=_REFERENCE_DATE,
        continuation_available=False,
        source_exhausted=False,
        structure_valid=True,
    )

    assert unsorted["status"] == "invalid"
    assert stranded["status"] == "invalid"
