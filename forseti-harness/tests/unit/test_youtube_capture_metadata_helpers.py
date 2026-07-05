"""Network-free tests for YouTube watch metadata helper honesty."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

YOUTUBE_CAPTURE_DIR = Path(__file__).resolve().parents[2] / "youtube_capture"
sys.path.insert(0, str(YOUTUBE_CAPTURE_DIR))

import capture_youtube_v0  # noqa: E402
from capture_youtube_v0 import (  # noqa: E402
    COMMENTS_PANEL_BADGE_SOURCE_PATH,
    comments_disabled_signal,
    detect_video_state,
    extract_comments_panel_count,
    extract_like_count,
    fetch_youtube_watch,
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


def test_detect_video_state_blocking_playability_status_is_never_playable():
    # Observed lake failure shape: playabilityStatus ERROR "Video unavailable"
    # with no videoDetails must not fall through to the playable fallback.
    cases = [
        {"playabilityStatus": {"status": "ERROR", "reason": "Video unavailable"}},
        {"playabilityStatus": {"status": "UNPLAYABLE", "reason": "This video cannot be played here"}},
    ]

    for player in cases:
        state, reason = detect_video_state(
            status=200,
            final_url="https://www.youtube.com/watch?v=abcdefghijk",
            html=_html(player),
            player=player,
        )
        assert state != "playable"
        assert state == "unknown"
        assert player["playabilityStatus"]["status"] in reason


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


def _comments_panel(badge_text: str | None, *, title_text: str = "Comments") -> dict[str, object]:
    header: dict[str, object] = {"title": {"runs": [{"text": title_text}]}}
    if badge_text is not None:
        header["contextualInfo"] = {"runs": [{"text": badge_text}]}
    return {
        "engagementPanelSectionListRenderer": {
            "header": {"engagementPanelTitleHeaderRenderer": header}
        }
    }


def _initial_data(*panels: dict[str, object]) -> dict[str, object]:
    return {"engagementPanels": list(panels)}


def test_extract_comments_panel_count_reads_exact_integer_badge():
    assert extract_comments_panel_count(_initial_data(_comments_panel("38"))) == (38, "38")
    assert extract_comments_panel_count(_initial_data(_comments_panel("1,234"))) == (1234, "1,234")
    # non-Comments panels never contribute a count
    assert extract_comments_panel_count(
        _initial_data(_comments_panel("999", title_text="Transcript"), _comments_panel("38"))
    ) == (38, "38")


def test_extract_comments_panel_count_fails_closed_on_rounded_or_absent_badge():
    # rounded badge text is preserved but never parsed into a count
    assert extract_comments_panel_count(_initial_data(_comments_panel("1.4K"))) == (None, "1.4K")
    # zero-comment shape: Comments panel present with no contextualInfo badge
    assert extract_comments_panel_count(_initial_data(_comments_panel(None))) == (None, None)
    assert extract_comments_panel_count(_initial_data()) == (None, None)
    assert extract_comments_panel_count(None) == (None, None)


def _watch_html(*, badge_text: str | None, include_comments_panel: bool = True) -> bytes:
    player = {
        "playabilityStatus": {"status": "OK"},
        "videoDetails": {"videoId": "abcdefghijk", "viewCount": "23071"},
        "microformat": {"playerMicroformatRenderer": {"likeCount": "1075"}},
    }
    panels = [_comments_panel(badge_text)] if include_comments_panel else []
    initial_data = _initial_data(*panels)
    return (
        "<script>var ytInitialPlayerResponse = " + json.dumps(player) + ";</script>"
        "<script>var ytInitialData = " + json.dumps(initial_data) + ";</script>"
    ).encode("utf-8")


def _fake_http_get(html_bytes: bytes):
    def fake(url, data=None):
        return 200, url, html_bytes

    return fake


def test_fetch_youtube_watch_observes_total_comment_count_from_panel_badge(monkeypatch):
    monkeypatch.setattr(capture_youtube_v0, "http_get", _fake_http_get(_watch_html(badge_text="38")))

    fetch = fetch_youtube_watch("abcdefghijk")

    receipt = fetch.packet["metric_receipts"]["total_comment_count"]
    assert receipt["posture"] == "observed"
    assert receipt["value"] == 38
    assert receipt["source_path"] == COMMENTS_PANEL_BADGE_SOURCE_PATH
    assert receipt["source_route"] == "ytInitialData"
    assert receipt["artifact"] == "raw_watch.html"
    assert fetch.packet["engagement"]["total_comment_count"] == 38
    assert fetch.packet["comments_panel_count_text"] == "38"
    # no continuation token in the fixture: the sample stays a loud gap, never zero
    assert fetch.packet["metric_receipts"]["comment_sample_count"]["posture"] == "unavailable_with_reason"
    assert fetch.packet["engagement"]["view_count"] == 23071
    assert fetch.packet["engagement"]["like_count"] == 1075


def test_fetch_youtube_watch_rounded_badge_fails_closed(monkeypatch):
    monkeypatch.setattr(capture_youtube_v0, "http_get", _fake_http_get(_watch_html(badge_text="1.4K")))

    fetch = fetch_youtube_watch("abcdefghijk")

    receipt = fetch.packet["metric_receipts"]["total_comment_count"]
    assert receipt["posture"] == "unavailable_with_reason"
    assert "'1.4K'" in receipt["reason"]
    assert receipt["routes_checked"] == [COMMENTS_PANEL_BADGE_SOURCE_PATH]
    assert fetch.packet["engagement"]["total_comment_count"] is None
    assert fetch.packet["comments_panel_count_text"] == "1.4K"


def test_fetch_youtube_watch_absent_badge_keeps_continuation_gap_reason(monkeypatch):
    monkeypatch.setattr(
        capture_youtube_v0,
        "http_get",
        _fake_http_get(_watch_html(badge_text=None, include_comments_panel=False)),
    )

    fetch = fetch_youtube_watch("abcdefghijk")

    receipt = fetch.packet["metric_receipts"]["total_comment_count"]
    assert receipt["posture"] == "unavailable_with_reason"
    assert "did not expose a comments continuation token" in receipt["reason"]
    assert "Comments panel badge" in receipt["reason"]
    assert receipt["routes_checked"] == [COMMENTS_PANEL_BADGE_SOURCE_PATH]
    assert fetch.packet["comments_panel_count_text"] is None
