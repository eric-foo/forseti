from __future__ import annotations

import pytest

from capture_spine.creator_profile_current.creator_onboarding_selection import (
    CreatorOnboardingSelectionError,
    eligible_creator_onboarding_candidates,
    select_creator_onboarding_candidate,
)


def _profile(
    platform: str,
    account_id: str,
    handle: str,
    onboarding_state: str,
) -> dict[str, object]:
    return {
        "profile_subject_id": account_id,
        "profile_subject_kind": "platform_account",
        "onboarding": {"onboarding_state": onboarding_state},
        "platform_accounts": [
            {
                "platform": platform,
                "platform_account_id": account_id,
                "public_handle": handle,
                "public_profile_url": f"https://example.test/{platform}/{handle}",
            }
        ],
    }


def _registry() -> dict[str, object]:
    return {
        "creator_profile_current_view": {
            "profiles": [
                _profile("tiktok", "tt_done", "done_tt", "onboarded"),
                _profile("tiktok", "tt_next", "next_tt", "not_onboarded"),
                _profile("instagram", "ig_next", "next_ig", "not_onboarded"),
                _profile("youtube", "yt_done", "done_yt", "onboarded"),
                _profile("youtube", "yt_first", "first_yt", "not_onboarded"),
                _profile("youtube", "yt_second", "second_yt", "not_onboarded"),
            ]
        }
    }


@pytest.mark.parametrize(
    ("platform", "expected_account_id"),
    [("tiktok", "tt_next"), ("instagram", "ig_next")],
)
def test_select_creator_onboarding_candidate_auto_selects_cross_social_singleton(
    platform: str,
    expected_account_id: str,
) -> None:
    candidate = select_creator_onboarding_candidate(
        _registry(),
        platform=platform,
    )

    assert candidate["platform_account_id"] == expected_account_id
    assert candidate["selection_policy"] == "sole_not_onboarded_platform_account"


def test_eligible_candidates_exclude_onboarded_accounts() -> None:
    candidates = eligible_creator_onboarding_candidates(
        _registry(),
        platform="youtube",
    )

    assert [row["platform_account_id"] for row in candidates] == [
        "yt_first",
        "yt_second",
    ]


def test_selection_requires_exact_account_when_multiple_are_eligible() -> None:
    with pytest.raises(
        CreatorOnboardingSelectionError,
        match="select one exact platform_account_id",
    ):
        select_creator_onboarding_candidate(
            _registry(),
            platform="youtube",
        )

    candidate = select_creator_onboarding_candidate(
        _registry(),
        platform="youtube",
        platform_account_id="yt_second",
    )
    assert candidate["platform_account_id"] == "yt_second"
    assert candidate["selection_policy"] == "exact_platform_account_id"


def test_selection_fails_loud_when_platform_has_no_eligible_account() -> None:
    registry = {
        "creator_profile_current_view": {
            "profiles": [_profile("instagram", "ig_done", "done", "onboarded")]
        }
    }

    with pytest.raises(
        CreatorOnboardingSelectionError,
        match="no not_onboarded instagram account",
    ):
        select_creator_onboarding_candidate(
            registry,
            platform="instagram",
        )
