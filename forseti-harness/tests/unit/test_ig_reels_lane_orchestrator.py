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


def _deep_result(
    shortcode: str = _SHORTCODE,
    *,
    comment_id: str = "c1",
    posture: str = "transcribed",
    cues: list[dict[str, Any]] | None = None,
) -> ReelDeepCaptureResult:
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
        transcript_posture=posture,
        transcript_cues=tuple(_cues() if cues is None else cues),
        media_url_used="https://x.fbcdn.net/o1/v/clip.mp4",
    )


def test_orchestrator_surfaces_retired_deep_capture_and_blocks_downstream(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_out = tmp_path / "operator_packet.json"

    def grid_runner(**_kwargs):  # noqa: ANN001
        return 0, "raw/packet"

    def deep_capture_runner(**_kwargs):  # noqa: ANN001
        result = _deep_result()
        write_reel_deep_capture_into_lake(
            data_root=data_root,
            result=result,
            generated_at="2026-06-29T00:01:00Z",
        )

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
        operator_packet_out=packet_out,
        grid_runner=grid_runner,
        deep_capture_runner=deep_capture_runner,
        projection_builder=projection_builder,
    )

    receipts = {receipt["lane"]: receipt for receipt in summary.to_dict()["receipts"]}
    assert summary.complete is False
    assert receipts["grid"]["status"] == "succeeded"
    assert receipts["deep_capture"]["status"] == "failed"
    assert "eligible_bronze_required" in receipts["deep_capture"]["message"]
    assert receipts["product_extract"]["status"] == "not_attempted"
    assert receipts["projection"]["status"] == "not_attempted"
    assert not any(path.name.startswith("operator_packet") for path in tmp_path.iterdir())


def test_orchestrator_does_not_create_exact_key_for_retired_deep_capture(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    new_result = _deep_result(comment_id="new")

    def deep_capture_runner(**_kwargs):  # noqa: ANN001
        write_reel_deep_capture_into_lake(
            data_root=data_root,
            result=new_result,
            generated_at="2026-06-29T00:01:00Z",
        )

    summary = run_ig_reels_lane_orchestrator(
        data_root=data_root,
        handle="creator",
        lanes=("deep_capture",),
        deep_capture_runner=deep_capture_runner,
    )

    receipts = {receipt["lane"]: receipt for receipt in summary.to_dict()["receipts"]}
    assert receipts["deep_capture"]["status"] == "failed"
    assert "eligible_bronze_required" in receipts["deep_capture"]["message"]
    record_id = deep_capture_record_id(new_result)
    assert not data_root.record_path(
        subtree="derived",
        raw_anchor=_SHORTCODE,
        lane="silver__capture__reel_transcript",
        record_id=record_id,
    ).exists()


def test_orchestrator_does_not_fall_back_to_old_transcript_after_unpersisted_capture(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    new_result = _deep_result(comment_id="new")
    packet_out = tmp_path / "operator_packet.json"

    def deep_capture_runner(**_kwargs):  # noqa: ANN001
        ranked = RankedReel(rank=1, shortcode=_SHORTCODE, engagement=1, like_count=1, comment_count=0)
        return [ranked], [CapturedReel(ranked=ranked, result=new_result, persisted="persist-failed: disk full")]

    summary = run_ig_reels_lane_orchestrator(
        data_root=data_root,
        handle="creator",
        lanes=("deep_capture", "product_extract"),
        operator_packet_out=packet_out,
        deep_capture_runner=deep_capture_runner,
    )

    receipts = {receipt["lane"]: receipt for receipt in summary.to_dict()["receipts"]}
    assert receipts["deep_capture"]["status"] == "failed"
    assert receipts["deep_capture"]["outputs"]["selected_targets"] == []
    assert receipts["product_extract"]["status"] == "not_attempted"
    assert receipts["product_extract"]["residuals"] == ["ig_product_selector_absent"]
    assert not packet_out.exists()
    assert not (tmp_path / f"operator_packet.{_SHORTCODE}.json").exists()


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


def test_orchestrator_keeps_retired_capture_failure_visible_for_explicit_target(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    captured_shortcode = "DaALKgOsWn0"
    captured_result = _deep_result(captured_shortcode, comment_id="captured")

    def deep_capture_runner(**_kwargs):  # noqa: ANN001
        ranked = RankedReel(rank=1, shortcode=captured_shortcode, engagement=1, like_count=1, comment_count=0)
        return [ranked], [
            CapturedReel(
                ranked=ranked,
                result=captured_result,
                persisted="persist-failed: ValueError: eligible_bronze_required",
            )
        ]

    summary = run_ig_reels_lane_orchestrator(
        data_root=data_root,
        handle="creator",
        lanes=("deep_capture",),
        platform_item_id=_SHORTCODE,
        deep_capture_runner=deep_capture_runner,
    )

    receipts = {receipt["lane"]: receipt for receipt in summary.to_dict()["receipts"]}
    deep = receipts["deep_capture"]
    assert deep["status"] == "failed"
    assert deep["outputs"]["persisted_count"] == 0
    assert deep["outputs"]["selected_targets"] == []
    assert any("eligible_bronze_required" in residual for residual in deep["residuals"])


def test_orchestrator_fans_out_every_extraction_eligible_reel(tmp_path) -> None:
    """The reported @jeremyfragrance case: a render-empty top reel must not mask eligible lower reels."""
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_out = tmp_path / "operator_packet.json"

    rank1 = _deep_result("RANK1RENDER", comment_id="r1", posture="render_unavailable", cues=[])
    rank2 = _deep_result("RANK2TRANS", comment_id="r2")
    rank3 = _deep_result("RANK3NOSPCH", comment_id="r3", posture="no_speech", cues=[])
    rank4 = _deep_result("RANK4TRANS", comment_id="r4")
    ranked_results = [rank1, rank2, rank3, rank4]

    def deep_capture_runner(**_kwargs):  # noqa: ANN001
        ranked = [
            RankedReel(rank=index, shortcode=result.reel_shortcode, engagement=10 - index, like_count=1, comment_count=1)
            for index, result in enumerate(ranked_results, start=1)
        ]
        captured = [
            CapturedReel(
                ranked=ranked[index],
                result=result,
                persisted="persist-failed: ValueError: eligible_bronze_required",
            )
            for index, result in enumerate(ranked_results)
        ]
        return ranked, captured

    projected: list[str] = []

    def projection_builder(**kwargs):  # noqa: ANN001
        projected.append(kwargs["platform_item_id"])
        return {"behavioral_completeness": {"status": "complete", "complete": True, "residuals": []}}

    summary = run_ig_reels_lane_orchestrator(
        data_root=data_root,
        handle="creator",
        lanes=("deep_capture", "product_extract", "projection"),
        top_n=4,
        operator_packet_out=packet_out,
        deep_capture_runner=deep_capture_runner,
        projection_builder=projection_builder,
    )

    receipts = {receipt["lane"]: receipt for receipt in summary.to_dict()["receipts"]}
    deep = receipts["deep_capture"]["outputs"]
    assert receipts["deep_capture"]["status"] == "failed"
    assert deep["persisted_count"] == 0
    assert deep["eligible_count"] == 0
    assert deep["selected_targets"] == []
    residuals = receipts["deep_capture"]["residuals"]
    assert sum("eligible_bronze_required" in residual for residual in residuals) == 4

    assert projected == []
    assert receipts["product_extract"]["status"] == "not_attempted"
    assert receipts["projection"]["status"] == "not_attempted"
    assert not any(path.name.startswith("operator_packet") for path in tmp_path.iterdir())


def test_orchestrator_fan_out_keeps_content_empty_when_no_reel_is_eligible(tmp_path) -> None:
    """A genuinely content-empty batch (all reels render-empty) must stay content-empty."""
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_out = tmp_path / "operator_packet.json"

    first = _deep_result("EMPTYONE", comment_id="e1", posture="render_unavailable", cues=[])
    second = _deep_result("EMPTYTWO", comment_id="e2", posture="no_audio_handle", cues=[])

    def deep_capture_runner(**_kwargs):  # noqa: ANN001
        ranked = [
            RankedReel(rank=1, shortcode="EMPTYONE", engagement=2, like_count=1, comment_count=1),
            RankedReel(rank=2, shortcode="EMPTYTWO", engagement=1, like_count=1, comment_count=0),
        ]
        return ranked, [
            CapturedReel(
                ranked=ranked[0],
                result=first,
                persisted="persist-failed: ValueError: eligible_bronze_required",
            ),
            CapturedReel(
                ranked=ranked[1],
                result=second,
                persisted="persist-failed: ValueError: eligible_bronze_required",
            ),
        ]

    summary = run_ig_reels_lane_orchestrator(
        data_root=data_root,
        handle="creator",
        lanes=("deep_capture", "product_extract", "projection"),
        top_n=2,
        operator_packet_out=packet_out,
        deep_capture_runner=deep_capture_runner,
    )

    receipts = {receipt["lane"]: receipt for receipt in summary.to_dict()["receipts"]}
    assert receipts["deep_capture"]["status"] == "failed"
    assert receipts["deep_capture"]["outputs"]["persisted_count"] == 0
    assert receipts["deep_capture"]["outputs"]["eligible_count"] == 0
    assert receipts["deep_capture"]["outputs"]["selected_targets"] == []
    assert receipts["product_extract"]["status"] == "not_attempted"
    assert receipts["product_extract"]["residuals"] == ["ig_product_selector_absent"]
    assert receipts["projection"]["status"] == "not_attempted"
    assert not any(p.name.startswith("operator_packet") for p in tmp_path.iterdir() if p.is_file())


def test_orchestrator_rejects_mismatched_explicit_selectors(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    with pytest.raises(ValueError, match="different reels"):
        run_ig_reels_lane_orchestrator(
            data_root=data_root,
            handle="creator",
            lanes=("product_extract",),
            platform_item_id="AAA111",
            transcript_source_key="BBB222:asr:deepcap_BBB222__x.json",
        )


def test_orchestrator_source_key_only_targets_one_consistent_reel(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    projected: list[str] = []

    def projection_builder(**kwargs):  # noqa: ANN001
        projected.append(kwargs["platform_item_id"])
        return {"behavioral_completeness": {"status": "complete", "complete": True, "residuals": []}}

    summary = run_ig_reels_lane_orchestrator(
        data_root=data_root,
        handle="creator",
        lanes=("projection",),
        transcript_source_key="ZZZ123:asr:deepcap_ZZZ123__abc.json",
        projection_builder=projection_builder,
    )

    receipts = {receipt["lane"]: receipt for receipt in summary.to_dict()["receipts"]}
    # Source-key-only used to leave projection not_attempted (no shortcode); the orchestrator now
    # derives the shortcode from the key so product extraction and projection target the same reel.
    assert projected == ["ZZZ123"]
    assert receipts["projection"]["status"] == "succeeded"


def test_orchestrator_product_lane_treats_partial_cleanup_as_operator_action(tmp_path, monkeypatch) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")

    def fake_export(**kwargs):  # noqa: ANN001
        return {"video_id": kwargs.get("platform_item_id"), "status": "partial_needs_cleanup"}

    monkeypatch.setattr(orchestrator_runner, "export_operator_packet", fake_export)
    summary = run_ig_reels_lane_orchestrator(
        data_root=data_root,
        handle="creator",
        lanes=("product_extract",),
        platform_item_id="PARTIAL1",
        operator_packet_out=tmp_path / "operator_packet.json",
    )

    receipt = summary.to_dict()["receipts"][0]
    # partial_needs_cleanup is an operator-action state (standalone runner exit 4), not a hard
    # failure -- it must not collapse into "failed"/exit 3.
    assert receipt["lane"] == "product_extract"
    assert receipt["status"] == "blocked_operator_action_required"
    assert receipt["outputs"]["targets"][0]["status"] == "partial_needs_cleanup"


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
