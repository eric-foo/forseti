from __future__ import annotations

import json

import pytest
from runners import run_ig_creator_momentum_projection

from source_capture.ig_projection import (
    IG_PROJECTION_METHOD,
    build_ig_creator_momentum_projection,
    build_ig_creator_momentum_projection_from_packet_directory,
)
from source_capture.models import (
    CaptureModeCategory,
    CoverageWindow,
    MetricObservation,
    MetricPosture,
    PacketTiming,
    PreservedFile,
    ReceiptMetadata,
    SourceCapturePacket,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)


CAPTURE_TIME = "2026-06-16T20:32:17Z"


def test_ig_projection_indexes_metric_rows_with_identity_and_raw_anchors() -> None:
    packet, raw = _packet()

    projection = build_ig_creator_momentum_projection(
        packet=packet,
        raw_file_bytes_by_file_id=raw,
    )

    assert projection.packet_id == "pkt-ig"
    assert projection.loss_ledger.preserved_metric_rows == 4
    assert projection.loss_ledger.identity_complete is True
    assert projection.loss_ledger.structure_preserved is True
    assert projection.residuals == []

    follower = next(row for row in projection.rows if row.metric == "follower_count")
    assert follower.row_kind == "ig_creator_metric"
    assert follower.entity_id == "5802114508"
    assert follower.username == "hyram"
    assert follower.content_kind == "profile"
    assert follower.value == 724000
    assert follower.raw_anchor.file_id == "file_02"
    assert follower.raw_anchor.json_pointer == "/follower_count"

    view = next(row for row in projection.rows if row.metric == "view_count")
    assert view.row_kind == "ig_media_metric"
    assert view.entity_id == "5802114508"
    assert view.content_kind == "post"
    assert view.content_shortcode == "AAA"
    assert view.content_url == "https://www.instagram.com/hyram/p/AAA/"
    assert view.posture is MetricPosture.NOT_APPLICABLE
    assert view.value is None
    assert view.reason == "IG profile-feed JSON marks this media as non-video"
    assert view.raw_anchor.file_id == "file_02"
    assert view.raw_anchor.json_pointer == "/media/AAA/video_view_count"
    assert view.source_visible_fields["is_video"] is False
    assert view.source_visible_fields["taken_at_timestamp"] == 1722470400
    assert view.source_visible_fields["status"] == "captured"


def test_ig_projection_preserves_observed_zero_view_count() -> None:
    packet, raw = _packet(
        locator="https://www.instagram.com/hyram/reel/BBB/",
        shortcode="BBB",
        is_video=True,
        view_observation=MetricObservation(
            metric="view_count",
            posture=MetricPosture.OBSERVED,
            value=0,
            coverage_window=CoverageWindow(end=CAPTURE_TIME),
        ),
    )

    projection = build_ig_creator_momentum_projection(packet=packet, raw_file_bytes_by_file_id=raw)

    view = next(row for row in projection.rows if row.metric == "view_count")
    assert view.content_kind == "reel"
    assert view.content_shortcode == "BBB"
    assert view.posture is MetricPosture.OBSERVED
    assert view.value == 0
    assert view.reason is None


def test_ig_projection_marks_identity_incomplete_without_numeric_id() -> None:
    packet, raw = _packet(numeric_id=None)

    projection = build_ig_creator_momentum_projection(packet=packet, raw_file_bytes_by_file_id=raw)

    assert projection.loss_ledger.identity_complete is False
    assert projection.loss_ledger.structure_preserved is False
    assert "ig_numeric_id_absent" in projection.residuals
    assert all(row.entity_id is None for row in projection.rows)


def test_ig_projection_rejects_non_ig_packet() -> None:
    packet, raw = _packet(source_family="reddit")

    with pytest.raises(ValueError, match="source_family='instagram_creator'"):
        build_ig_creator_momentum_projection(packet=packet, raw_file_bytes_by_file_id=raw)


def test_ig_projection_requires_raw_bytes_for_preserved_files() -> None:
    packet, raw = _packet()
    raw.pop("file_02")

    with pytest.raises(ValueError, match="file_02"):
        build_ig_creator_momentum_projection(packet=packet, raw_file_bytes_by_file_id=raw)


def test_ig_projection_builds_from_existing_packet_directory(tmp_path) -> None:
    packet, raw = _packet()
    packet_dir = _write_packet_dir(tmp_path, packet=packet, raw=raw)

    projection = build_ig_creator_momentum_projection_from_packet_directory(
        packet_or_manifest_path=packet_dir,
    )

    assert projection.packet_id == "pkt-ig"
    assert projection.projection_method == IG_PROJECTION_METHOD
    assert projection.loss_ledger.preserved_metric_rows == 4


def test_ig_projection_runner_writes_existing_packet_projection(tmp_path, capsys) -> None:
    packet, raw = _packet()
    packet_dir = _write_packet_dir(tmp_path, packet=packet, raw=raw)
    output_path = tmp_path / "projection" / "ig_projection.json"

    result = run_ig_creator_momentum_projection.main(
        ["--packet", str(packet_dir / "manifest.json"), "--output", str(output_path)]
    )

    assert result == 0
    assert capsys.readouterr().out.strip() == str(output_path)
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["projection_method"] == IG_PROJECTION_METHOD
    assert payload["certification"] == "view_only; not_cleaned; not_normalized; not_judgment_ready"
    assert len(payload["rows"]) == 4


def _packet(
    *,
    source_family: str = "instagram_creator",
    numeric_id: str | None = "5802114508",
    username: str = "hyram",
    locator: str = "https://www.instagram.com/hyram/p/AAA/",
    shortcode: str = "AAA",
    is_video: bool = False,
    view_observation: MetricObservation | None = None,
) -> tuple[SourceCapturePacket, dict[str, bytes]]:
    profile_raw = {
        "profile_url": "https://www.instagram.com/hyram/",
        "stats": {"followers": "724K", "following": "2,339", "posts": "321"},
    }
    media_record = {
        "shortcode": shortcode,
        "is_video": is_video,
        "video_view_count": 0 if is_video else None,
        "like_count": 1693,
        "comment_count": 26,
        "caption": "caption omitted from projection rows",
        "taken_at_timestamp": 1722470400,
    }
    momentum_raw = {
        "username": username,
        "follower_count": 724000,
        "metric_registry_version": "ig_creator_momentum_metrics_v0",
        "identity_conflict_policy_version": "ig_numeric_id_username_policy_v0",
        "media": {shortcode: media_record},
    }
    if numeric_id is not None:
        momentum_raw["numeric_id"] = numeric_id
    call_raw = {
        "url": locator,
        "status": "captured",
        "likes": 1693,
        "comments": 26,
        "date": "August 1, 2024",
        "is_ad": False,
        "caption_truncated": False,
    }
    raw = {
        "file_01": _json_bytes(profile_raw),
        "file_02": _json_bytes(momentum_raw),
        "file_03": _json_bytes(call_raw),
    }
    profile_slice = _slice(
        "ig_profile_00",
        "https://www.instagram.com/hyram/",
        ["file_01", "file_02"],
        [
            MetricObservation(
                metric="follower_count",
                posture=MetricPosture.OBSERVED,
                value=724000,
                coverage_window=CoverageWindow(end=CAPTURE_TIME),
            )
        ],
    )
    call_slice = _slice(
        "ig_call_01",
        locator,
        ["file_03"],
        [
            MetricObservation(
                metric="like_count",
                posture=MetricPosture.OBSERVED,
                value=1693,
                coverage_window=CoverageWindow(end=CAPTURE_TIME),
            ),
            MetricObservation(
                metric="comment_count",
                posture=MetricPosture.OBSERVED,
                value=26,
                coverage_window=CoverageWindow(end=CAPTURE_TIME),
            ),
            view_observation
            or MetricObservation(
                metric="view_count",
                posture=MetricPosture.NOT_APPLICABLE,
                reason="IG profile-feed JSON marks this media as non-video",
                coverage_window=CoverageWindow(end=CAPTURE_TIME),
            ),
        ],
    )
    packet = SourceCapturePacket(
        packet_id="pkt-ig",
        manifest_version="source_capture_packet_manifest_v1",
        obligation_contract_version="core_spine_v0_data_capture_spine_obligation_contract_v0",
        source_family=source_family,
        source_surface="ig_calls_browser_snapshot",
        source_locator=known_fact("https://www.instagram.com/hyram/"),
        requested_decision_context=known_fact("q"),
        capture_context=known_fact("logged-out IG wind-caller calls capture"),
        actor_audience_context=known_fact("public creator"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="ig_calls_browser_snapshot_cli_operator",
        session_identity="",
        timing=_timing(unknown_with_reason("profile slice is the enumeration source")),
        access_posture=known_fact("ig_logged_out_browser_snapshot"),
        archive_history_posture=not_attempted("IG calls runner does not query archive or history services"),
        media_modality_posture=known_fact("og:description and profile-feed JSON checked"),
        re_capture_relationship=not_applicable("no prior packet"),
        source_slices=[profile_slice, call_slice],
        preserved_files=[
            _preserved_file("file_01", "raw/01_ig_profile.json", raw["file_01"]),
            _preserved_file("file_02", "raw/02_ig_profile_momentum.json", raw["file_02"]),
            _preserved_file("file_03", "raw/03_ig_call_01.json", raw["file_03"]),
        ],
        receipt_metadata=ReceiptMetadata(
            title="Source Capture Packet Receipt",
            generated_at="2026-06-16T20:33:46Z",
            summary="summary",
            non_claims=["not projection fold"],
        ),
    )
    return packet, raw


def _slice(
    slice_id: str,
    locator: str,
    preserved_file_ids: list[str],
    metric_observations: list[MetricObservation],
) -> SourceCaptureSlice:
    return SourceCaptureSlice(
        slice_id=slice_id,
        locator=known_fact(locator),
        timing=_timing(known_fact("August 1, 2024") if slice_id.startswith("ig_call") else unknown_with_reason("profile slice")),
        access_posture=known_fact("ig_logged_out_browser_snapshot"),
        archive_history_posture=not_attempted("IG calls runner does not query archive or history services"),
        media_modality_posture=known_fact("og:description and profile-feed JSON checked"),
        re_capture_relationship=not_applicable("no prior packet"),
        preserved_file_ids=preserved_file_ids,
        metric_observations=metric_observations,
    )


def _timing(publication) -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=publication,
        source_edit_or_version=unknown_with_reason("not inferred"),
        capture_time=known_fact(CAPTURE_TIME),
        recapture_time=not_applicable("no prior capture"),
        cutoff_posture=unknown_with_reason("not supplied"),
    )


def _preserved_file(file_id: str, relative_path: str, body: bytes) -> PreservedFile:
    return PreservedFile(
        file_id=file_id,
        original_path=relative_path,
        relative_packet_path=relative_path,
        sha256="a" * 64,
        hash_basis="raw_stored_bytes",
        size_bytes=len(body),
    )


def _write_packet_dir(tmp_path, *, packet: SourceCapturePacket, raw: dict[str, bytes]):
    packet_dir = tmp_path / "packet"
    for preserved_file in packet.preserved_files:
        raw_path = packet_dir / preserved_file.relative_packet_path
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_bytes(raw[preserved_file.file_id])
    (packet_dir / "manifest.json").write_text(
        f"{json.dumps(packet.model_dump(mode='json'), indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    return packet_dir


def _json_bytes(payload: dict[str, object]) -> bytes:
    return json.dumps(payload, sort_keys=True).encode("utf-8")
