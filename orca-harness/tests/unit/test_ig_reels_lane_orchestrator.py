"""Offline tests for the IG Reels vertical lane orchestrator."""
from __future__ import annotations

import json
from typing import Any

import pytest

from data_lake.root import DataLakeRoot
from runners import run_ig_reels_lane_orchestrator as orchestrator_runner
from schemas.audience_comment_models import AudienceComment
from runners.run_ig_reels_lane_orchestrator import run_ig_reels_lane_orchestrator
from runners.run_source_capture_ig_reels_creator_deep_capture import CapturedReel, RankedReel
from source_capture.ig_reels_deep_capture import ReelDeepCaptureResult
from source_capture.ig_reels_deep_capture_lake import deep_capture_record_id, write_reel_deep_capture_into_lake

_SHORTCODE = "DZ69knlsDb1"


def _cues() -> list[dict[str, Any]]:
    return [
        {"start_ms": 1000, "end_ms": 3000, "text": "Today I'm testing Dior Sauvage Elixir"},
        {"start_ms": 3000, "end_ms": 6000, "text": "and it is an absolute beast in the heat"},
    ]


def _deep_result(shortcode: str = _SHORTCODE, *, comment_id: str = "c1") -> ReelDeepCaptureResult:
    return ReelDeepCaptureResult(
        reel_shortcode=shortcode,
        comments=(
            AudienceComment(
                comment_id=comment_id,
                reel_shortcode=shortcode,
                author_username="zoe",
                text="works",
                like_count=1,
                created_at_unix=1782400000,
            ),
        ),
        transcript_posture="transcribed",
        transcript_cues=tuple(_cues()),
        media_url_used="https://x.fbcdn.net/o1/v/clip.mp4",
    )


def test_orchestrator_exports_operator_packet_and_marks_lane_blocked(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_path = tmp_path / "operator_packet.json"

    def grid_runner(**_kwargs):  # noqa: ANN001
        return 0, "raw/packet"

    def deep_capture_runner(**_kwargs):  # noqa: ANN001
        result = _deep_result()
        write_reel_deep_capture_into_lake(
            data_root=data_root,
            result=result,
            generated_at="2026-06-29T00:01:00Z",
        )
        ranked = RankedReel(
            rank=1,
            shortcode=_SHORTCODE,
            engagement=10,
            like_count=8,
            comment_count=2,
            view_count=100,
        )
        return [ranked], [CapturedReel(ranked=ranked, result=result, persisted="persisted: ok")]

    def projection_builder(**_kwargs):  # noqa: ANN001
        return {
            "behavioral_completeness": {
                "status": "not_attempted",
                "complete": False,
                "residuals": [f"ig_transcript_extraction_not_attempted:{_SHORTCODE}"],
            }
        }

    summary = run_ig_reels_lane_orchestrator(
        data_root=data_root,
        handle="creator",
        lanes=("grid", "deep_capture", "product_extract", "projection"),
        operator_packet_out=packet_path,
        grid_runner=grid_runner,
        deep_capture_runner=deep_capture_runner,
        projection_builder=projection_builder,
    )

    receipts = {receipt["lane"]: receipt for receipt in summary.to_dict()["receipts"]}
    assert summary.complete is False
    assert receipts["grid"]["status"] == "succeeded"
    assert receipts["deep_capture"]["status"] == "succeeded"
    expected_source_key = f"{_SHORTCODE}:asr:{deep_capture_record_id(_deep_result())}"
    assert receipts["deep_capture"]["outputs"]["selected_platform_item_id"] == _SHORTCODE
    assert receipts["deep_capture"]["outputs"]["selected_transcript_source_key"] == expected_source_key
    assert receipts["product_extract"]["status"] == "blocked_operator_action_required"
    assert receipts["product_extract"]["outputs"]["status"] == "operator_packet_exported"
    assert receipts["product_extract"]["outputs"]["transcript_source_key"] == expected_source_key
    assert receipts["projection"]["status"] == "incomplete"
    assert packet_path.is_file()
    packet = json.loads(packet_path.read_text(encoding="utf-8"))
    assert packet["transcript_identity"]["video_id"] == _SHORTCODE


def test_orchestrator_uses_new_exact_deep_capture_key_when_old_same_shortcode_exists(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    old_result = _deep_result(comment_id="old")
    write_reel_deep_capture_into_lake(
        data_root=data_root,
        result=old_result,
        generated_at="2026-06-29T00:00:00Z",
    )
    new_result = _deep_result(comment_id="new")
    packet_path = tmp_path / "operator_packet.json"

    def deep_capture_runner(**_kwargs):  # noqa: ANN001
        write_reel_deep_capture_into_lake(
            data_root=data_root,
            result=new_result,
            generated_at="2026-06-29T00:01:00Z",
        )
        ranked = RankedReel(rank=1, shortcode=_SHORTCODE, engagement=1, like_count=1, comment_count=0)
        return [ranked], [CapturedReel(ranked=ranked, result=new_result, persisted="persisted: ok")]

    summary = run_ig_reels_lane_orchestrator(
        data_root=data_root,
        handle="creator",
        lanes=("deep_capture", "product_extract"),
        operator_packet_out=packet_path,
        deep_capture_runner=deep_capture_runner,
    )

    receipts = {receipt["lane"]: receipt for receipt in summary.to_dict()["receipts"]}
    new_key = f"{_SHORTCODE}:asr:{deep_capture_record_id(new_result)}"
    old_key = f"{_SHORTCODE}:asr:{deep_capture_record_id(old_result)}"
    assert receipts["deep_capture"]["outputs"]["selected_transcript_source_key"] == new_key
    assert receipts["product_extract"]["outputs"]["transcript_source_key"] == new_key
    assert json.loads(packet_path.read_text(encoding="utf-8"))["transcript_identity"]["transcript_source_key"] == new_key
    assert old_key != new_key


def test_orchestrator_does_not_fall_back_to_old_transcript_after_unpersisted_capture(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    old_result = _deep_result(comment_id="old")
    write_reel_deep_capture_into_lake(
        data_root=data_root,
        result=old_result,
        generated_at="2026-06-29T00:00:00Z",
    )
    new_result = _deep_result(comment_id="new")
    packet_path = tmp_path / "operator_packet.json"

    def deep_capture_runner(**_kwargs):  # noqa: ANN001
        ranked = RankedReel(rank=1, shortcode=_SHORTCODE, engagement=1, like_count=1, comment_count=0)
        return [ranked], [CapturedReel(ranked=ranked, result=new_result, persisted="persist-failed: disk full")]

    summary = run_ig_reels_lane_orchestrator(
        data_root=data_root,
        handle="creator",
        lanes=("deep_capture", "product_extract"),
        operator_packet_out=packet_path,
        deep_capture_runner=deep_capture_runner,
    )

    receipts = {receipt["lane"]: receipt for receipt in summary.to_dict()["receipts"]}
    assert receipts["deep_capture"]["status"] == "failed"
    assert receipts["deep_capture"]["outputs"]["selected_transcript_source_key"] is None
    assert receipts["product_extract"]["status"] == "not_attempted"
    assert receipts["product_extract"]["residuals"] == ["ig_product_selector_absent"]
    assert not packet_path.exists()


def test_projection_false_completeness_keeps_summary_incomplete(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")

    def projection_builder(**_kwargs):  # noqa: ANN001
        return {"behavioral_completeness": {"status": "not_attempted", "complete": False, "residuals": []}}

    summary = run_ig_reels_lane_orchestrator(
        data_root=data_root,
        handle="creator",
        lanes=("projection",),
        platform_item_id=_SHORTCODE,
        projection_builder=projection_builder,
    )

    receipt = summary.to_dict()["receipts"][0]
    assert receipt["status"] == "incomplete"
    assert summary.complete is False


def test_orchestrator_requires_packet_path_for_operator_export(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    summary = run_ig_reels_lane_orchestrator(
        data_root=data_root,
        handle="creator",
        lanes=("product_extract",),
        platform_item_id=_SHORTCODE,
    )

    receipt = summary.to_dict()["receipts"][0]
    assert receipt["lane"] == "product_extract"
    assert receipt["status"] == "blocked_operator_action_required"
    assert receipt["residuals"] == ["ig_product_operator_packet_output_path_absent"]


def test_orchestrator_keeps_explicit_target_when_deep_capture_selects_other_reel(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    explicit_result = _deep_result(_SHORTCODE, comment_id="explicit")
    write_reel_deep_capture_into_lake(
        data_root=data_root,
        result=explicit_result,
        generated_at="2026-06-29T00:00:00Z",
    )
    captured_shortcode = "DaALKgOsWn0"
    captured_result = _deep_result(captured_shortcode, comment_id="captured")
    packet_path = tmp_path / "operator_packet.json"

    def deep_capture_runner(**_kwargs):  # noqa: ANN001
        write_reel_deep_capture_into_lake(
            data_root=data_root,
            result=captured_result,
            generated_at="2026-06-29T00:01:00Z",
        )
        ranked = RankedReel(rank=1, shortcode=captured_shortcode, engagement=1, like_count=1, comment_count=0)
        return [ranked], [CapturedReel(ranked=ranked, result=captured_result, persisted="persisted: ok")]

    def projection_builder(**kwargs):  # noqa: ANN001
        assert kwargs["platform_item_id"] == _SHORTCODE
        return {"behavioral_completeness": {"status": "complete", "complete": True, "residuals": []}}

    summary = run_ig_reels_lane_orchestrator(
        data_root=data_root,
        handle="creator",
        lanes=("deep_capture", "product_extract", "projection"),
        platform_item_id=_SHORTCODE,
        operator_packet_out=packet_path,
        deep_capture_runner=deep_capture_runner,
        projection_builder=projection_builder,
    )

    receipts = {receipt["lane"]: receipt for receipt in summary.to_dict()["receipts"]}
    explicit_key = f"{_SHORTCODE}:asr:{deep_capture_record_id(explicit_result)}"
    captured_key = f"{captured_shortcode}:asr:{deep_capture_record_id(captured_result)}"
    assert receipts["deep_capture"]["outputs"]["selected_transcript_source_key"] == captured_key
    assert receipts["deep_capture"]["residuals"] == [
        f"deep_capture_target_differs_from_explicit_platform_item:{_SHORTCODE}:{captured_shortcode}"
    ]
    assert receipts["product_extract"]["outputs"]["transcript_source_key"] == explicit_key
    assert json.loads(packet_path.read_text(encoding="utf-8"))["transcript_identity"]["video_id"] == _SHORTCODE


def test_orchestrator_marks_multi_reel_deep_capture_as_single_downstream_target(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    first = _deep_result("FIRST", comment_id="first")
    second = _deep_result("SECOND", comment_id="second")

    def deep_capture_runner(**_kwargs):  # noqa: ANN001
        for result in (first, second):
            write_reel_deep_capture_into_lake(
                data_root=data_root,
                result=result,
                generated_at="2026-06-29T00:01:00Z",
            )
        ranked = [
            RankedReel(rank=1, shortcode="FIRST", engagement=2, like_count=1, comment_count=1),
            RankedReel(rank=2, shortcode="SECOND", engagement=1, like_count=1, comment_count=0),
        ]
        return [
            *ranked
        ], [
            CapturedReel(ranked=ranked[0], result=first, persisted="persisted: ok"),
            CapturedReel(ranked=ranked[1], result=second, persisted="persisted: ok"),
        ]

    summary = run_ig_reels_lane_orchestrator(
        data_root=data_root,
        handle="creator",
        lanes=("deep_capture",),
        top_n=2,
        deep_capture_runner=deep_capture_runner,
    )

    receipt = summary.to_dict()["receipts"][0]
    assert receipt["outputs"]["persisted_count"] == 2
    assert receipt["outputs"]["selected_platform_item_id"] == "FIRST"
    assert receipt["residuals"] == ["orchestrator_product_projection_single_target:FIRST:persisted_count=2"]


def test_orchestrator_main_returns_nonzero_when_operator_action_required(tmp_path, monkeypatch, capsys) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")

    def fake_resolve(cls, *, explicit=None, **_kwargs):  # noqa: ANN001
        assert explicit is None
        return data_root

    monkeypatch.setattr(DataLakeRoot, "resolve", classmethod(fake_resolve))
    code = orchestrator_runner.main([
        "--handle",
        "creator",
        "--lanes",
        "product_extract",
        "--platform-item-id",
        _SHORTCODE,
    ])

    assert code == 4
    assert '"complete": false' in capsys.readouterr().out


def test_orchestrator_main_returns_nonzero_when_projection_incomplete(tmp_path, monkeypatch, capsys) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")

    def fake_resolve(cls, *, explicit=None, **_kwargs):  # noqa: ANN001
        assert explicit is None
        return data_root

    monkeypatch.setattr(DataLakeRoot, "resolve", classmethod(fake_resolve))
    code = orchestrator_runner.main([
        "--handle",
        "creator",
        "--lanes",
        "projection",
        "--platform-item-id",
        _SHORTCODE,
    ])

    assert code == 1
    assert '"status": "incomplete"' in capsys.readouterr().out


def test_orchestrator_rejects_empty_lane_list(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    with pytest.raises(ValueError, match="at least one IG lane"):
        run_ig_reels_lane_orchestrator(data_root=data_root, handle="creator", lanes=())
