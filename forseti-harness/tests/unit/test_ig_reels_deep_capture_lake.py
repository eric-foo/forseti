"""Retirement tests for the source-less legacy reel deep-capture Silver writer."""
from __future__ import annotations

from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot
from runners import run_source_capture_ig_reels_deep_capture as deep_capture_runner
from schemas.audience_comment_models import AudienceComment
from source_capture.ig_reels_deep_capture import ReelDeepCaptureResult
from source_capture.ig_reels_deep_capture_lake import (
    AUDIENCE_COMMENTS_LANE,
    DEEP_CAPTURE_SET_LANE,
    REEL_TRANSCRIPT_LANE,
    deep_capture_record_id,
    write_reel_deep_capture_into_lake,
)


def _root(tmp_path: Path) -> DataLakeRoot:
    return DataLakeRoot.for_test(tmp_path / "forseti-data")


def _result() -> ReelDeepCaptureResult:
    return ReelDeepCaptureResult(
        reel_shortcode="DaA8n7EhqTR",
        comments=(
            AudienceComment(
                comment_id="c1",
                reel_shortcode="DaA8n7EhqTR",
                author_username="zoe",
                text="love this",
                like_count=9,
                created_at_unix=1782400000,
            ),
        ),
        transcript_posture="transcribed",
        transcript_cues=({"start_ms": 0, "end_ms": 90, "text": "hi there"},),
        media_url_used="https://x.fbcdn.net/o1/v/clip.mp4",
    )


def test_record_id_remains_stable_for_historical_audit_lookup() -> None:
    assert deep_capture_record_id(_result()).startswith("deepcap_DaA8n7EhqTR__")


def test_legacy_writer_fails_before_any_bytes_without_eligible_bronze(tmp_path: Path) -> None:
    root = _root(tmp_path)
    with pytest.raises(ValueError, match="eligible_bronze_required"):
        write_reel_deep_capture_into_lake(
            data_root=root,
            result=_result(),
            generated_at="2026-07-15T00:00:00Z",
        )

    for lane in (AUDIENCE_COMMENTS_LANE, REEL_TRANSCRIPT_LANE, DEEP_CAPTURE_SET_LANE):
        assert not root.lane_dir(
            subtree="derived", raw_anchor="DaA8n7EhqTR", lane=lane
        ).exists()


def test_runner_persistence_path_surfaces_eligible_bronze_required(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _root(tmp_path)
    monkeypatch.setattr(
        deep_capture_runner.DataLakeRoot,
        "resolve",
        staticmethod(lambda **_kwargs: root),
    )

    with pytest.raises(ValueError, match="eligible_bronze_required"):
        deep_capture_runner._persist_deep_capture(_result(), data_root_arg=None)
