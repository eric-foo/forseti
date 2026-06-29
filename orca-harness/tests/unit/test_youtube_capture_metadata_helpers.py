"""Network-free tests for YouTube watch metadata helper honesty."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

YOUTUBE_CAPTURE_DIR = Path(__file__).resolve().parents[2] / "youtube_capture"
sys.path.insert(0, str(YOUTUBE_CAPTURE_DIR))

from capture_youtube_v0 import (  # noqa: E402
    comments_disabled_signal,
    detect_video_state,
    extract_like_count,
    parse_exact_count_text,
)
from shorts_scroll_capture_v0 import captured_with_comments_count  # noqa: E402


def _player(status: str | None = None, reason: str | None = None, messages=None) -> dict[str, object]:
    playability = {}
    if status is not None:
        playability["status"] = status
    if reason is not None:
        playability["reason"] = reason
    if messages is not None:
        playability["messages"] = messages
    return {"playabilityStatus": playability, "videoDetails": {"videoId": "abcdefghijk"}}


def _html(player_response: dict[str, object]) -> str:
    return "<script>var ytInitialPlayerResponse = " + json.dumps(player_response) + ";</script>"


def test_detect_video_state_playable_status_wins_over_logged_out_chrome():
    state, reason = detect_video_state(
        status=200,
        final_url="https://www.youtube.com/watch?v=abcdefghijk",
        html='<html><button>Sign in</button></html>',
        player=_player("OK"),
    )

    assert state == "playable"
    assert reason == "ytInitialPlayerResponse.playabilityStatus.status=OK"


def test_detect_video_state_specific_region_block_wins_over_logged_out_chrome():
    state, reason = detect_video_state(
        status=200,
        final_url="https://www.youtube.com/watch?v=abcdefghijk",
        html='<html><button>Sign in</button></html>',
        player=_player("ERROR", "Video not available in your country"),
    )

    assert state == "region_blocked"
    assert "region restriction" in reason


def test_detect_video_state_specific_non_ok_states():
    cases = [
        (_player("ERROR", "This video has been removed by the uploader"), "removed_by_uploader"),
        (_player("ERROR", "This video is private"), "private"),
        (_player("AGE_CHECK_REQUIRED", "Sign in to confirm your age"), "age_restricted"),
        (_player("LOGIN_REQUIRED", "Please sign in to watch this video"), "login_required"),
    ]

    for player, expected in cases:
        state, _ = detect_video_state(
            status=200,
            final_url="https://www.youtube.com/watch?v=abcdefghijk",
            html='<html><button>Sign in</button></html>',
            player=player,
        )
        assert state == expected


def test_detect_video_state_player_present_fallback_is_not_shadowed_by_chrome_login():
    state, reason = detect_video_state(
        status=200,
        final_url="https://www.youtube.com/watch?v=abcdefghijk",
        html='<html><button>Sign in</button></html>',
        player={"videoDetails": {"videoId": "abcdefghijk"}},
    )

    assert state == "playable"
    assert "ytInitialPlayerResponse present" in reason


def test_parse_exact_count_text_accepts_only_exact_integer_text():
    assert parse_exact_count_text("1,234 Comments") == 1234
    assert parse_exact_count_text("1234 comments") == 1234
    assert parse_exact_count_text("1,234,567 views") == 1234567

    for text in ["12K comments", "1.2K comments", "1.2K", "2.5M views", "1.2 comments"]:
        assert parse_exact_count_text(text) is None


def test_comments_disabled_signal_distinguishes_disabled_from_absent():
    assert comments_disabled_signal("<html>Comments are turned off</html>", {}) is True
    assert comments_disabled_signal("<html></html>", {"x": "comments are disabled"}) is True
    assert comments_disabled_signal("<html><button>Sign in</button></html>", {}) is False


def test_extract_like_count_uses_microformat_only_when_exact_count_present():
    count, source_path = extract_like_count(
        _html({"microformat": {"playerMicroformatRenderer": {"likeCount": "42"}}})
    )

    assert count == 42
    assert source_path == "ytInitialPlayerResponse.microformat.playerMicroformatRenderer.likeCount"
    assert extract_like_count(_html({"microformat": {"playerMicroformatRenderer": {"likeCount": "1.2K"}}})) == (
        None,
        None,
    )


def test_shorts_summary_counts_sample_captured_posture():
    postures = Counter(["comments_sample_captured", "comments_sample_captured", "comments_not_exposed"])

    assert captured_with_comments_count(postures) == 2
    assert captured_with_comments_count(Counter({"captured": 5})) == 0
