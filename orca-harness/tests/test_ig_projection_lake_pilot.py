from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard
from source_capture.ig_projection import (
    PROJECTION_IG_LANE,
    build_ig_creator_momentum_projection_from_packet_directory,
    project_ig_creator_momentum_into_lake,
)
from source_capture.models import (
    CoverageWindow,
    MetricObservation,
    MetricPosture,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.writer import write_local_source_capture_packet


_CAPTURE_TIME = "2026-06-16T20:32:17Z"


def _json_bytes(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True).encode("utf-8")


def _timing(publication) -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=publication,
        source_edit_or_version=unknown_with_reason("not inferred"),
        capture_time=known_fact(_CAPTURE_TIME),
        recapture_time=not_applicable("no prior capture"),
        cutoff_posture=unknown_with_reason("not supplied"),
    )


def _slice(slice_id: str, locator: str, preserved_file_ids, metric_observations) -> SourceCaptureSlice:
    return SourceCaptureSlice(
        slice_id=slice_id,
        locator=known_fact(locator),
        timing=_timing(
            known_fact("August 1, 2024") if slice_id.startswith("ig_call") else unknown_with_reason("profile slice")
        ),
        access_posture=known_fact("ig_logged_out_browser_snapshot"),
        archive_history_posture=not_attempted("IG calls runner does not query archive or history services"),
        media_modality_posture=known_fact("og:description and profile-feed JSON checked"),
        re_capture_relationship=not_applicable("no prior packet"),
        preserved_file_ids=preserved_file_ids,
        metric_observations=metric_observations,
    )


def _commit_ig_packet(root: DataLakeRoot, tmp_path: Path):
    # Stage a real IG packet THROUGH the lake writer so the manifest carries real
    # sha256 hashes (the loader re-verifies them). The packet shape mirrors the IG
    # projection unit test; file naming matches what the writer assigns (raw/NN_<name>),
    # which IG's reader classifies by path substring.
    profile_raw = {
        "profile_url": "https://www.instagram.com/hyram/",
        "stats": {"followers": "724K", "following": "2,339", "posts": "321"},
    }
    momentum_raw = {
        "username": "hyram",
        "numeric_id": "5802114508",
        "follower_count": 724000,
        "metric_registry_version": "ig_creator_momentum_metrics_v0",
        "identity_conflict_policy_version": "ig_numeric_id_username_policy_v0",
        "media": {
            "AAA": {
                "shortcode": "AAA",
                "is_video": False,
                "video_view_count": None,
                "like_count": 1693,
                "comment_count": 26,
                "caption": "caption omitted from projection rows",
                "taken_at_timestamp": 1722470400,
            }
        },
    }
    call_raw = {
        "url": "https://www.instagram.com/hyram/p/AAA/",
        "status": "captured",
        "likes": 1693,
        "comments": 26,
        "date": "August 1, 2024",
        "is_ad": False,
        "caption_truncated": False,
    }

    input_files = []
    for name, payload in (
        ("ig_profile.json", profile_raw),
        ("ig_profile_momentum.json", momentum_raw),
        ("ig_call_01.json", call_raw),
    ):
        path = tmp_path / name
        path.write_bytes(_json_bytes(payload))
        input_files.append(path)

    profile_slice = _slice(
        "ig_profile_00",
        "https://www.instagram.com/hyram/",
        ["file_01", "file_02"],
        [
            MetricObservation(
                metric="follower_count",
                posture=MetricPosture.OBSERVED,
                value=724000,
                coverage_window=CoverageWindow(end=_CAPTURE_TIME),
            )
        ],
    )
    call_slice = _slice(
        "ig_call_01",
        "https://www.instagram.com/hyram/p/AAA/",
        ["file_03"],
        [
            MetricObservation(
                metric="like_count",
                posture=MetricPosture.OBSERVED,
                value=1693,
                coverage_window=CoverageWindow(end=_CAPTURE_TIME),
            ),
            MetricObservation(
                metric="comment_count",
                posture=MetricPosture.OBSERVED,
                value=26,
                coverage_window=CoverageWindow(end=_CAPTURE_TIME),
            ),
            MetricObservation(
                metric="view_count",
                posture=MetricPosture.NOT_APPLICABLE,
                reason="IG profile-feed JSON marks this media as non-video",
                coverage_window=CoverageWindow(end=_CAPTURE_TIME),
            ),
        ],
    )

    return write_local_source_capture_packet(
        data_root=root,
        input_files=input_files,
        source_family="instagram_creator",
        source_surface="ig_calls_browser_snapshot",
        source_locator=known_fact("https://www.instagram.com/hyram/"),
        decision_question="is this creator gaining momentum?",
        capture_context="ig calls lake pilot",
        source_slices=[profile_slice, call_slice],
    )


def test_projects_committed_ig_raw_into_a_derived_record(tmp_path: Path) -> None:
    # capture -> committed raw -> read by key (verified) -> Silver record appended.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_ig_packet(root, tmp_path).packet.packet_id

    projection, derived_path = project_ig_creator_momentum_into_lake(data_root=root, packet_id=pid)

    assert derived_path.parent == root.path / "derived" / raw_shard(pid) / pid / PROJECTION_IG_LANE
    assert derived_path.suffix == ".json"
    assert derived_path.is_file()
    assert projection.packet_id == pid

    # the lake path is byte-identical to the canonical directory projection
    container = root.find_packet(pid)
    assert container is not None
    expected = build_ig_creator_momentum_projection_from_packet_directory(packet_or_manifest_path=container)
    expected_bytes = (
        f"{json.dumps(expected.model_dump(mode='json'), indent=2, sort_keys=True)}\n"
    ).encode("utf-8")
    assert derived_path.read_bytes() == expected_bytes

    # raw is untouched: a fresh verified read still succeeds
    assert root.load_raw_packet(pid).manifest["packet_id"] == pid


def test_re_derive_appends_a_sibling_not_overwrite(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_ig_packet(root, tmp_path).packet.packet_id

    _, first = project_ig_creator_momentum_into_lake(data_root=root, packet_id=pid)
    _, second = project_ig_creator_momentum_into_lake(data_root=root, packet_id=pid)

    lane_dir = root.path / "derived" / raw_shard(pid) / pid / PROJECTION_IG_LANE
    assert first != second
    assert len(list(lane_dir.glob("*.json"))) == 2


def test_explicit_record_id_is_create_only(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _commit_ig_packet(root, tmp_path).packet.packet_id

    project_ig_creator_momentum_into_lake(data_root=root, packet_id=pid, record_id="rec1")
    with pytest.raises(DataLakeRootError):
        project_ig_creator_momentum_into_lake(data_root=root, packet_id=pid, record_id="rec1")
