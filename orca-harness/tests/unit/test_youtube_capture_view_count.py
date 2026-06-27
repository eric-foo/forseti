"""Network-free tests for YouTube per-video view-count source paths."""
from __future__ import annotations

import json
import sys
from pathlib import Path

YOUTUBE_CAPTURE_DIR = Path(__file__).resolve().parents[2] / "youtube_capture"
sys.path.insert(0, str(YOUTUBE_CAPTURE_DIR))

from capture_youtube_v0 import extract_view_count


def _html(player_response: dict) -> str:
    return "<script>var ytInitialPlayerResponse = " + json.dumps(player_response) + ";</script>"


def test_view_count_prefers_video_details_path():
    count, source_path = extract_view_count(
        _html(
            {
                "videoDetails": {"viewCount": "123"},
                "microformat": {"playerMicroformatRenderer": {"viewCount": "456"}},
            }
        )
    )

    assert count == 123
    assert source_path == "ytInitialPlayerResponse.videoDetails.viewCount"


def test_view_count_falls_back_to_microformat_path_for_shorts_shape():
    count, source_path = extract_view_count(
        _html(
            {
                "videoDetails": {"videoId": "abcdefghijk"},
                "microformat": {"playerMicroformatRenderer": {"viewCount": "456"}},
            }
        )
    )

    assert count == 456
    assert source_path == "ytInitialPlayerResponse.microformat.playerMicroformatRenderer.viewCount"


def test_view_count_records_regex_fallback_path_when_player_json_is_missing():
    count, source_path = extract_view_count('<html>{"viewCount":"789"}</html>')

    assert count == 789
    assert source_path == "served_html.regex.first_viewCount"
