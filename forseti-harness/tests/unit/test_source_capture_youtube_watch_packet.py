from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, raw_shard
from runners.run_source_capture_youtube_watch_packet import run_source_capture_youtube_watch_packet
from source_capture.models import SourceCapturePacket
from source_capture.youtube_watch_packet import (
    YoutubeWatchCommentPage,
    YoutubeWatchFetch,
    write_youtube_watch_packet,
)

_VIDEO_ID = "vid12345678"
_CAPTURE_TS = "2026-06-22T10:00:00Z"


def _metric_observed(value: int, path: str, artifact: str) -> dict[str, object]:
    return {
        "posture": "observed",
        "value": value,
        "source_route": path.rsplit(".", 1)[0],
        "source_path": path,
        "artifact": artifact,
    }


def _metric_gap(reason: str) -> dict[str, object]:
    return {"posture": "unavailable_with_reason", "reason": reason, "routes_checked": ["fixture_route"]}


def _packet(
    *,
    like: int | None = 34,
    total_comments: int | None = 12,
    comments_state: str = "comments_sample_captured",
    canonical_url: str | None = f"https://www.youtube.com/watch?v={_VIDEO_ID}",
) -> dict[str, object]:
    metric_receipts = {
        "view_count": _metric_observed(1200, "ytInitialPlayerResponse.videoDetails.viewCount", "youtube_watch_capture.json"),
        "like_count": _metric_observed(like, "ytInitialPlayerResponse.microformat.playerMicroformatRenderer.likeCount", "youtube_watch_capture.json")
        if like is not None
        else _metric_gap("microformat.likeCount was not exposed"),
        "comment_sample_count": _metric_observed(1, "youtubei_next.commentEntityPayload", "youtube_watch_capture.json")
        if comments_state == "comments_sample_captured"
        else _metric_gap("served watch route did not expose a comments continuation token"),
        "total_comment_count": _metric_observed(total_comments, "youtubei_next.commentsHeaderRenderer.countText", "youtube_watch_capture.json")
        if total_comments is not None
        else _metric_gap("source-native total comment count was not exposed as an exact count"),
    }
    return {
        "video_id": _VIDEO_ID,
        "surface_type": "long_form",
        "watch_url": f"https://www.youtube.com/watch?v={_VIDEO_ID}",
        "canonical_url": canonical_url,
        "channel": {"channel_id": "UC_fixture", "author": "Reviewer"},
        "metadata": {"title": "Fragrance review", "length_seconds": 42, "publish_date": "2026-06-20"},
        "engagement": {
            "view_count": 1200,
            "view_count_source_path": "ytInitialPlayerResponse.videoDetails.viewCount",
            "like_count": like,
            "like_count_source_path": "ytInitialPlayerResponse.microformat.playerMicroformatRenderer.likeCount" if like is not None else None,
            "comment_sample_count": 1 if comments_state == "comments_sample_captured" else None,
            "total_comment_count": total_comments,
            "total_comment_count_source_path": "youtubei_next.commentsHeaderRenderer.countText" if total_comments is not None else None,
        },
        "availability": {
            "video_state": "playable",
            "video_state_reason": "fixture playable",
            "comments_state": comments_state,
            "comments_state_reason": "fixture comments state",
        },
        "metric_receipts": metric_receipts,
        "comments_posture": comments_state,
        "comment_count_text": "12 comments" if total_comments is not None else None,
        "comment_capture_coverage": {
            "requested_page_limit": 1,
            "pages_fetched": 1 if comments_state == "comments_sample_captured" else 0,
            "selected_comment_count": 1 if comments_state == "comments_sample_captured" else 0,
            "continuation_remaining_after_stop": False,
            "ordering_posture": "source_default_order_as_served",
        },
        "comments": [
            {
                "comment_id": "comment-001",
                "author": "A",
                "text": "wear test?",
                "published_time": "1 day ago",
                "like_count": 2,
                "reply_count": 1,
                "source_page_number": 1,
                "source_order_in_page": 1,
                "source_order_global": 1,
            }
        ]
        if comments_state == "comments_sample_captured"
        else [],
        "receipts": {"http_status": 200, "retrieval_time_utc": _CAPTURE_TS, "auth": "logged_out", "js_executed": False},
    }


def _fetch(**kwargs) -> YoutubeWatchFetch:
    return YoutubeWatchFetch(
        video_id=_VIDEO_ID,
        raw_watch_html=b"<html>ytInitialPlayerResponse</html>",
        packet=_packet(**kwargs),
        comment_page_bodies=(
            YoutubeWatchCommentPage(
                filename="youtubei_next_page_01.json",
                raw_json_bytes=b'{"commentsHeaderRenderer":{},"commentEntityPayload":{}}',
            ),
        ),
    )


def test_write_youtube_watch_packet_records_metrics_states_and_route_receipts(tmp_path: Path) -> None:
    output = tmp_path / "yt_watch_packet"

    code, message = write_youtube_watch_packet(
        _fetch(), output_directory=output, decision_question="capture YouTube watch metrics"
    )

    assert code == 0
    assert Path(message) == output.resolve()
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    packet = SourceCapturePacket(**manifest)
    assert packet.source_family == "youtube"
    assert packet.source_surface == "youtube_watch_metadata_comments"
    assert [item.relative_packet_path for item in packet.preserved_files] == [
        "raw/01_youtube_watch_capture.json",
    ]

    metadata_metrics = {obs["metric"]: obs for obs in manifest["source_slices"][0]["metric_observations"]}
    comments_metrics = {obs["metric"]: obs for obs in manifest["source_slices"][1]["metric_observations"]}
    assert metadata_metrics["view_count"]["value"] == 1200
    assert metadata_metrics["like_count"]["value"] == 34
    assert comments_metrics["comment_sample_count"]["value"] == 1
    assert comments_metrics["total_comment_count"]["value"] == 12

    payload_path = output / "raw" / "01_youtube_watch_capture.json"
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    assert payload["capture_schema_version"] == "youtube_watch_metadata_comments_capture_v1"
    assert payload["selected_observable_policy_version"] == "youtube_watch_selected_observables_v1"
    assert payload["source_response_retention"]["watch_html"] == {
        "posture": "not_persisted_after_validated_extraction",
        "received_byte_size": len(b"<html>ytInitialPlayerResponse</html>"),
    }
    assert payload["source_response_retention"]["comment_pages"]["received_page_count"] == 1
    assert payload["availability"]["comments_state"] == "comments_sample_captured"
    assert payload["metric_receipts"]["total_comment_count"]["source_route"] == "youtubei_next.commentsHeaderRenderer"
    assert payload["packet"]["comments"][0]["like_count"] == 2
    assert not (output / "raw" / "raw_watch.html").exists()
    assert not any("youtubei_next_page" in path.name for path in (output / "raw").iterdir())
    assert (
        "youtube_watch_metric_postures:"
        "view_count=observed;like_count=observed;comment_sample_count=observed;total_comment_count=observed"
    ) in manifest["visible_mode_changes"]
    assert not any("view_count=0" in item for item in manifest["visible_mode_changes"])


def test_selected_comment_rows_require_identity_text_and_source_order(tmp_path: Path) -> None:
    output = tmp_path / "yt_watch_bad_selected_comment"
    packet = _packet()
    del packet["comments"][0]["comment_id"]

    code, message = write_youtube_watch_packet(
        YoutubeWatchFetch(
            video_id=_VIDEO_ID,
            raw_watch_html=b"<html>ytInitialPlayerResponse</html>",
            packet=packet,
            comment_page_bodies=(),
        ),
        output_directory=output,
        decision_question="capture YouTube watch metrics",
    )

    assert code == 5
    assert "selected comment row 1 lacks comment_id" in message
    assert not output.exists()


def test_missing_like_and_total_comment_counts_are_gaps_not_zeroes(tmp_path: Path) -> None:
    output = tmp_path / "yt_watch_gaps"
    fetch = YoutubeWatchFetch(
        video_id=_VIDEO_ID,
        raw_watch_html=b"<html>ytInitialPlayerResponse</html>",
        packet=_packet(like=None, total_comments=None, comments_state="comments_not_exposed"),
        comment_page_bodies=(),
    )

    code, _message = write_youtube_watch_packet(
        fetch, output_directory=output, decision_question="capture YouTube watch metrics"
    )

    assert code == 0
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    metadata_metrics = {obs["metric"]: obs for obs in manifest["source_slices"][0]["metric_observations"]}
    comments_metrics = {obs["metric"]: obs for obs in manifest["source_slices"][1]["metric_observations"]}
    assert metadata_metrics["like_count"]["posture"] == "unavailable_with_reason"
    assert "value" not in metadata_metrics["like_count"] or metadata_metrics["like_count"]["value"] is None
    assert comments_metrics["total_comment_count"]["posture"] == "unavailable_with_reason"
    assert "value" not in comments_metrics["total_comment_count"] or comments_metrics["total_comment_count"]["value"] is None
    assert "like_count_not_exposed:no_zero_fill" in manifest["limitations"]
    assert "total_comment_count_not_exposed:no_zero_fill" in manifest["limitations"]



def test_metric_value_without_receipt_is_rejected(tmp_path: Path) -> None:
    output = tmp_path / "yt_watch_bad_metric"
    packet = _packet()
    del packet["metric_receipts"]["view_count"]

    code, message = write_youtube_watch_packet(
        YoutubeWatchFetch(
            video_id=_VIDEO_ID,
            raw_watch_html=b"<html>ytInitialPlayerResponse</html>",
            packet=packet,
            comment_page_bodies=(),
        ),
        output_directory=output,
        decision_question="capture YouTube watch metrics",
    )

    assert code == 5
    assert "missing metric receipt for view_count" in message
    assert not output.exists()


def test_observed_metric_receipt_requires_route_path_and_artifact(tmp_path: Path) -> None:
    output = tmp_path / "yt_watch_bad_observed_receipt"
    packet = _packet()
    packet["metric_receipts"]["like_count"] = {"posture": "observed", "value": 34}

    code, message = write_youtube_watch_packet(
        YoutubeWatchFetch(
            video_id=_VIDEO_ID,
            raw_watch_html=b"<html>ytInitialPlayerResponse</html>",
            packet=packet,
            comment_page_bodies=(),
        ),
        output_directory=output,
        decision_question="capture YouTube watch metrics",
    )

    assert code == 5
    assert "observed metric receipt for like_count missing source_route, source_path, artifact" in message
    assert not output.exists()


def test_unavailable_metric_receipt_requires_reason_and_routes_checked(tmp_path: Path) -> None:
    output = tmp_path / "yt_watch_bad_unavailable_receipt"
    packet = _packet(like=None)
    packet["metric_receipts"]["like_count"] = {"posture": "unavailable_with_reason", "reason": "not exposed"}

    code, message = write_youtube_watch_packet(
        YoutubeWatchFetch(
            video_id=_VIDEO_ID,
            raw_watch_html=b"<html>ytInitialPlayerResponse</html>",
            packet=packet,
            comment_page_bodies=(),
        ),
        output_directory=output,
        decision_question="capture YouTube watch metrics",
    )

    assert code == 5
    assert "unavailable metric receipt for like_count requires non-empty routes_checked" in message
    assert not output.exists()


def test_metric_receipt_value_must_match_engagement_value(tmp_path: Path) -> None:
    output = tmp_path / "yt_watch_mismatched_metric"
    packet = _packet()
    packet["engagement"]["view_count"] = 9999

    code, message = write_youtube_watch_packet(
        YoutubeWatchFetch(
            video_id=_VIDEO_ID,
            raw_watch_html=b"<html>ytInitialPlayerResponse</html>",
            packet=packet,
            comment_page_bodies=(),
        ),
        output_directory=output,
        decision_question="capture YouTube watch metrics",
    )

    assert code == 5
    assert "metric receipt for view_count value 1200 does not match engagement value 9999" in message
    assert not output.exists()


def test_unavailable_metric_receipt_rejects_stale_engagement_value(tmp_path: Path) -> None:
    output = tmp_path / "yt_watch_stale_metric"
    packet = _packet()
    packet["metric_receipts"]["like_count"] = _metric_gap("microformat.likeCount was not exposed")

    code, message = write_youtube_watch_packet(
        YoutubeWatchFetch(
            video_id=_VIDEO_ID,
            raw_watch_html=b"<html>ytInitialPlayerResponse</html>",
            packet=packet,
            comment_page_bodies=(),
        ),
        output_directory=output,
        decision_question="capture YouTube watch metrics",
    )

    assert code == 5
    assert "like_count has engagement value 34 but metric receipt posture is 'unavailable_with_reason'" in message
    assert not output.exists()


def test_metric_receipt_rejects_unsupported_posture(tmp_path: Path) -> None:
    output = tmp_path / "yt_watch_bad_posture"
    packet = _packet(like=None)
    packet["metric_receipts"]["like_count"] = {
        "posture": "not_applicable",
        "reason": "not needed",
        "routes_checked": ["fixture_route"],
    }

    code, message = write_youtube_watch_packet(
        YoutubeWatchFetch(
            video_id=_VIDEO_ID,
            raw_watch_html=b"<html>ytInitialPlayerResponse</html>",
            packet=packet,
            comment_page_bodies=(),
        ),
        output_directory=output,
        decision_question="capture YouTube watch metrics",
    )

    assert code == 5
    assert "metric receipt for like_count has unsupported posture 'not_applicable'" in message
    assert not output.exists()


@dataclass(frozen=True)
class _Fetched:
    packet: dict[str, object]
    raw_watch_html: bytes
    comment_page_bodies: tuple[YoutubeWatchCommentPage, ...]


def test_youtube_watch_runner_can_commit_to_data_lake(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")

    def fake_fetcher(video_id: str, *, comment_pages: int) -> _Fetched:
        assert video_id == _VIDEO_ID
        assert comment_pages == 2
        return _Fetched(
            packet=_packet(),
            raw_watch_html=b"<html>ytInitialPlayerResponse</html>",
            comment_page_bodies=(
                YoutubeWatchCommentPage(filename="youtubei_next_page_01.json", raw_json_bytes=b"{}"),
            ),
        )

    code, message = run_source_capture_youtube_watch_packet(
        video_id=_VIDEO_ID,
        data_root=root,
        decision_question="capture YouTube watch metrics",
        capture_fetcher=fake_fetcher,
    )

    assert code == 0
    packet_dir = Path(message)
    assert packet_dir.parent == root.path / "raw" / raw_shard(packet_dir.name)
    assert root.find_packet(packet_dir.name) is not None
    assert root.read_availability(packet_dir.name) is not None


@pytest.mark.parametrize(
    ("canonical_url", "expected_state"),
    [
        ("https://www.youtube.com/watch?v=other123456", "subject_identity_mismatch"),
        (None, "subject_identity_unavailable"),
    ],
)
def test_youtube_watch_runner_rejects_unbound_served_identity_before_publication(
    tmp_path: Path,
    canonical_url: str | None,
    expected_state: str,
) -> None:
    packet = _packet(canonical_url=canonical_url)

    def fake_fetcher(_video_id: str, *, comment_pages: int) -> _Fetched:
        assert comment_pages == 1
        return _Fetched(
            packet=packet,
            raw_watch_html=b"<html>ytInitialPlayerResponse</html>",
            comment_page_bodies=(
                YoutubeWatchCommentPage(filename="youtubei_next_page_01.json", raw_json_bytes=b"{}"),
            ),
        )

    output = tmp_path / f"yt_watch_{expected_state}"
    code, message = run_source_capture_youtube_watch_packet(
        video_id=_VIDEO_ID,
        output_directory=output,
        decision_question="capture YouTube watch metrics",
        comment_pages=1,
        capture_fetcher=fake_fetcher,
    )

    assert code == 5
    assert expected_state in message
    assert not output.exists()

    root = DataLakeRoot.for_test(tmp_path / f"forseti-data-{expected_state}")
    lake_before = sorted(path.relative_to(root.path).as_posix() for path in root.path.rglob("*"))
    code, message = run_source_capture_youtube_watch_packet(
        video_id=_VIDEO_ID,
        data_root=root,
        decision_question="capture YouTube watch metrics",
        comment_pages=1,
        capture_fetcher=fake_fetcher,
    )

    assert code == 5
    assert expected_state in message
    assert sorted(path.relative_to(root.path).as_posix() for path in root.path.rglob("*")) == lake_before
