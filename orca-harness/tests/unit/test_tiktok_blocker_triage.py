from __future__ import annotations

from source_capture.tiktok.blocker_triage import (
    TIKTOK_BLOCKER_ACTION_CONTINUE,
    TIKTOK_BLOCKER_ACTION_DISMISS_ONCE_CANDIDATE,
    TIKTOK_BLOCKER_ACTION_RELOAD_ONCE_CANDIDATE,
    TIKTOK_BLOCKER_ACTION_STOP,
    TIKTOK_BLOCKER_CLASS_AMBIGUOUS,
    TIKTOK_BLOCKER_CLASS_BENIGN_DISMISSIBLE_OVERLAY,
    TIKTOK_BLOCKER_CLASS_CHALLENGE_OR_SECURITY,
    TIKTOK_BLOCKER_CLASS_INFRASTRUCTURE_RELOAD,
    TIKTOK_BLOCKER_CLASS_NO_BLOCKER,
    classify_tiktok_blocker,
)


def test_blocker_triage_challenge_wins_over_dismiss_control() -> None:
    triage = classify_tiktok_blocker(
        final_url="https://www.tiktok.com/@funmi/video/7390000000000000001",
        title="Verify to continue",
        visible_text="Drag the slider to verify to continue. Close",
        hydration_present=False,
        item_struct_present=False,
        dismiss_candidate_count=1,
    )

    assert triage.blocker_class == TIKTOK_BLOCKER_CLASS_CHALLENGE_OR_SECURITY
    assert triage.action == TIKTOK_BLOCKER_ACTION_STOP
    assert triage.reason == "platform_challenge_observed"
    assert triage.challenge_marker_seen is True
    receipt = triage.to_receipt()
    assert receipt["marker_family"] == "challenge_or_security"
    assert receipt["matched_marker"] == "verify to continue"
    assert receipt["challenge_kind"] == "slider"


def test_blocker_triage_login_url_is_security_stop() -> None:
    triage = classify_tiktok_blocker(
        final_url="https://www.tiktok.com/login?redirect_url=%2F%40funmi%2Fvideo%2F739",
        title="TikTok",
        visible_text="Not now",
        hydration_present=False,
        item_struct_present=False,
        dismiss_candidate_count=1,
    )

    assert triage.blocker_class == TIKTOK_BLOCKER_CLASS_CHALLENGE_OR_SECURITY
    assert triage.action == TIKTOK_BLOCKER_ACTION_STOP
    assert triage.reason == "login_or_auth_wall_observed"
    receipt = triage.to_receipt()
    assert receipt["matched_marker"] == "/login"
    assert receipt["challenge_kind"] == "login_or_auth_wall"


def test_blocker_triage_benign_overlay_is_one_dismiss_candidate() -> None:
    triage = classify_tiktok_blocker(
        final_url="https://www.tiktok.com/@funmi/video/7390000000000000001",
        title="TikTok",
        visible_text="Open app or continue in browser. Not now",
        hydration_present=True,
        item_struct_present=True,
        dismiss_candidate_count=1,
    )

    assert triage.blocker_class == TIKTOK_BLOCKER_CLASS_BENIGN_DISMISSIBLE_OVERLAY
    assert triage.action == TIKTOK_BLOCKER_ACTION_DISMISS_ONCE_CANDIDATE
    receipt = triage.to_receipt()
    assert receipt["dismiss_candidate_count"] == 1
    assert "Open app" not in str(receipt)
    assert "Not now" not in str(receipt)


def test_blocker_triage_intro_ok_overlay_is_benign_dismiss_candidate() -> None:
    triage = classify_tiktok_blocker(
        final_url="https://www.tiktok.com/@funmi/video/7390000000000000001",
        title="TikTok",
        visible_text="Scroll, use the buttons, then press OK to continue",
        hydration_present=True,
        item_struct_present=True,
        dismiss_candidate_count=1,
    )

    assert triage.blocker_class == TIKTOK_BLOCKER_CLASS_BENIGN_DISMISSIBLE_OVERLAY
    assert triage.action == TIKTOK_BLOCKER_ACTION_DISMISS_ONCE_CANDIDATE
    assert triage.reason == "benign_overlay_marker_with_dismiss_control"

def test_blocker_triage_missing_hydration_is_reload_candidate_not_dismiss() -> None:
    triage = classify_tiktok_blocker(
        final_url="https://www.tiktok.com/@funmi/video/7390000000000000001",
        title="TikTok",
        visible_text="Something went wrong. Reload",
        hydration_present=False,
        item_struct_present=False,
        reload_candidate_count=1,
    )

    assert triage.blocker_class == TIKTOK_BLOCKER_CLASS_INFRASTRUCTURE_RELOAD
    assert triage.action == TIKTOK_BLOCKER_ACTION_RELOAD_ONCE_CANDIDATE
    assert triage.reason == "missing_item_struct_or_empty_shell"


def test_blocker_triage_hydration_without_item_struct_is_empty_shell() -> None:
    triage = classify_tiktok_blocker(
        final_url="https://www.tiktok.com/@funmi/video/7390000000000000001",
        title="TikTok",
        visible_text="video shell loaded",
        hydration_present=True,
        item_struct_present=False,
    )

    assert triage.blocker_class == TIKTOK_BLOCKER_CLASS_INFRASTRUCTURE_RELOAD
    assert triage.action == TIKTOK_BLOCKER_ACTION_RELOAD_ONCE_CANDIDATE
    assert triage.reason == "missing_item_struct_or_empty_shell"


def test_blocker_triage_close_text_without_candidate_does_not_stop() -> None:
    triage = classify_tiktok_blocker(
        final_url="https://www.tiktok.com/@funmi/video/7390000000000000001",
        title="TikTok",
        visible_text="Close",
        hydration_present=True,
        item_struct_present=True,
    )

    assert triage.blocker_class == TIKTOK_BLOCKER_CLASS_NO_BLOCKER
    assert triage.action == TIKTOK_BLOCKER_ACTION_CONTINUE


def test_blocker_triage_unknown_x_only_is_ambiguous_stop() -> None:
    triage = classify_tiktok_blocker(
        final_url="https://www.tiktok.com/@funmi/video/7390000000000000001",
        title="TikTok",
        visible_text="",
        hydration_present=True,
        item_struct_present=True,
        dismiss_candidate_count=1,
    )

    assert triage.blocker_class == TIKTOK_BLOCKER_CLASS_AMBIGUOUS
    assert triage.action == TIKTOK_BLOCKER_ACTION_STOP
    assert triage.reason == "unclassified_dismiss_control"


def test_blocker_triage_no_markers_continues() -> None:
    triage = classify_tiktok_blocker(
        final_url="https://www.tiktok.com/@funmi/video/7390000000000000001",
        title="TikTok",
        visible_text="video loaded",
        hydration_present=True,
        item_struct_present=True,
    )

    assert triage.blocker_class == TIKTOK_BLOCKER_CLASS_NO_BLOCKER
    assert triage.action == TIKTOK_BLOCKER_ACTION_CONTINUE
    assert triage.to_receipt()["challenge_marker_seen"] is False
