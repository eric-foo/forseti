from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard
from ecr.deriver import (
    derive_identity_postures,
    derive_inspectability_postures,
    derive_source_visibility_postures,
    derive_timing_postures,
)
from ecr.lake import ECR_COMPLETION_LANE, ECR_LANES, derive_ecr_into_lake
from ecr.models import (
    EcrIdentityPosture,
    EcrInspectabilityPosture,
    EcrSourceVisibilityPosture,
    EcrTimingPosture,
)
from source_capture.models import (
    PacketTiming,
    SourceCapturePacket,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.writer import write_local_source_capture_packet


def _capture(root: DataLakeRoot, tmp_path: Path):
    # Any committed packet works; the ECR derivers are pure over the packet. The
    # capture path is the data_root seam already on main.
    src = tmp_path / "thread.json"
    src.write_text('{"body": "a reddit thread"}', encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family="reddit",
        source_surface="r/test",
        source_locator=known_fact("https://www.reddit.com/r/test/comments/x/"),
        decision_question="q",
        capture_context="ecr lake pilot",
    )


def _slice_timing(cutoff_posture: str) -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=unknown_with_reason("not supplied for test"),
        source_edit_or_version=unknown_with_reason("not supplied for test"),
        capture_time=known_fact("2026-06-21T00:00:00Z"),
        recapture_time=not_applicable("first capture in test fixture"),
        cutoff_posture=known_fact(cutoff_posture),
    )


def _source_slice(*, slice_id: str, file_id: str, cutoff_posture: str) -> SourceCaptureSlice:
    return SourceCaptureSlice(
        slice_id=slice_id,
        locator=known_fact(f"https://www.reddit.com/r/test/comments/x/#{slice_id}"),
        timing=_slice_timing(cutoff_posture),
        access_posture=known_fact("local_file_only"),
        archive_history_posture=not_attempted("archive/history was not probed in test"),
        media_modality_posture=not_attempted("media requirements were not probed in test"),
        re_capture_relationship=not_applicable("no recapture relationship in test"),
        preserved_file_ids=[file_id],
    )


def _multi_slice_capture(root: DataLakeRoot, tmp_path: Path):
    first = tmp_path / "thread-current.json"
    second = tmp_path / "thread-archive.json"
    first.write_text('{"body": "current reddit thread"}', encoding="utf-8")
    second.write_text('{"body": "archived reddit thread"}', encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=root,
        input_files=[first, second],
        source_family="reddit",
        source_surface="r/test",
        source_locator=known_fact("https://www.reddit.com/r/test/comments/x/"),
        decision_question="q",
        capture_context="ecr lake multi-slice pilot",
        source_slices=[
            _source_slice(slice_id="slice_01", file_id="file_01", cutoff_posture="pre_cutoff"),
            _source_slice(slice_id="slice_02", file_id="file_02", cutoff_posture="post_cutoff"),
        ],
    )


def _expected_bytes(postures) -> bytes:
    return (
        f"{json.dumps([posture.model_dump(mode='json') for posture in postures], indent=2, sort_keys=True)}\n"
    ).encode("utf-8")


_POSTURE_MODEL_BY_LANE = {
    ECR_LANES["timing"]: EcrTimingPosture,
    ECR_LANES["inspectability"]: EcrInspectabilityPosture,
    ECR_LANES["identity"]: EcrIdentityPosture,
    ECR_LANES["source_visibility"]: EcrSourceVisibilityPosture,
}


def test_derives_four_sibling_ecr_records(tmp_path: Path) -> None:
    # capture -> committed raw -> read by key (verified) -> 4 sibling Silver records.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture(root, tmp_path).packet.packet_id

    paths = derive_ecr_into_lake(data_root=root, packet_id=pid)

    # one derivation -> four siblings (one per epistemic kind), sharing one record_id
    assert set(paths) == set(ECR_LANES.values())
    assert len({path.name for path in paths.values()}) == 1
    for lane, path in paths.items():
        assert path.parent == root.path / "derived" / raw_shard(pid) / pid / lane
        assert path.suffix == ".json"
        assert path.is_file()

    # each record byte-matches its deriver's output on the verified-read packet
    packet = SourceCapturePacket.model_validate(root.load_raw_packet(pid).manifest)
    assert paths[ECR_LANES["timing"]].read_bytes() == _expected_bytes(derive_timing_postures(packet))
    assert paths[ECR_LANES["inspectability"]].read_bytes() == _expected_bytes(
        derive_inspectability_postures(packet)
    )
    assert paths[ECR_LANES["identity"]].read_bytes() == _expected_bytes(derive_identity_postures(packet))
    assert paths[ECR_LANES["source_visibility"]].read_bytes() == _expected_bytes(
        derive_source_visibility_postures(packet)
    )

    # raw untouched
    assert root.load_raw_packet(pid).manifest["packet_id"] == pid


def test_re_derive_appends_new_siblings(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture(root, tmp_path).packet.packet_id

    first = derive_ecr_into_lake(data_root=root, packet_id=pid)
    second = derive_ecr_into_lake(data_root=root, packet_id=pid)

    for lane in ECR_LANES.values():
        assert first[lane] != second[lane]
        assert len(list((root.path / "derived" / raw_shard(pid) / pid / lane).glob("*.json"))) == 2


def test_explicit_record_id_is_create_only(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture(root, tmp_path).packet.packet_id

    derive_ecr_into_lake(data_root=root, packet_id=pid, record_id="rec1")
    with pytest.raises(DataLakeRootError):
        derive_ecr_into_lake(data_root=root, packet_id=pid, record_id="rec1")


def test_preflights_sibling_collision_before_any_ecr_write(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture(root, tmp_path).packet.packet_id
    existing = root.append_record(
        subtree="derived",
        raw_anchor=pid,
        lane=ECR_LANES["inspectability"],
        record_id="rec1.json",
        data=b"existing sibling\n",
    )

    with pytest.raises(DataLakeRootError, match="partial record set"):
        derive_ecr_into_lake(data_root=root, packet_id=pid, record_id="rec1")

    assert existing.read_bytes() == b"existing sibling\n"
    for lane in ECR_LANES.values():
        path = root.path / "derived" / raw_shard(pid) / pid / lane / "rec1.json"
        assert path.exists() is (lane == ECR_LANES["inspectability"])


def test_serialized_ecr_records_round_trip_through_posture_models(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture(root, tmp_path).packet.packet_id

    paths = derive_ecr_into_lake(data_root=root, packet_id=pid)

    for lane, path in paths.items():
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(payload, list)
        assert payload
        for item in payload:
            _POSTURE_MODEL_BY_LANE[lane].model_validate(item)


def test_multi_slice_packet_preserves_slice_grain_for_per_slice_rows(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _multi_slice_capture(root, tmp_path).packet.packet_id

    paths = derive_ecr_into_lake(data_root=root, packet_id=pid)

    timing = json.loads(paths[ECR_LANES["timing"]].read_text(encoding="utf-8"))
    inspectability = json.loads(paths[ECR_LANES["inspectability"]].read_text(encoding="utf-8"))
    identity = json.loads(paths[ECR_LANES["identity"]].read_text(encoding="utf-8"))
    source_visibility = json.loads(paths[ECR_LANES["source_visibility"]].read_text(encoding="utf-8"))

    assert [item["slice_id"] for item in timing] == ["slice_01", "slice_02"]
    assert [item["slice_id"] for item in inspectability] == ["slice_01", "slice_02"]
    assert len(identity) == 1
    assert identity[0]["packet_id"] == pid
    assert len(source_visibility) == 1
    assert source_visibility[0]["packet_id"] == pid


def test_ecr_derivation_writes_a_completion_marker_and_is_complete(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture(root, tmp_path).packet.packet_id

    paths = derive_ecr_into_lake(data_root=root, packet_id=pid)
    record_name = next(iter(paths.values())).name

    marker = root.path / "derived" / raw_shard(pid) / pid / ECR_COMPLETION_LANE / record_name
    assert marker.is_file()
    assert json.loads(marker.read_text(encoding="utf-8")) == {
        "member_lanes": sorted(ECR_LANES.values()),
        "record_id": record_name,
    }
    assert root.is_record_set_complete(
        subtree="derived",
        raw_anchor=pid,
        record_id=record_name,
        completion_lane=ECR_COMPLETION_LANE,
    )


def test_ecr_set_missing_marker_reads_incomplete(tmp_path: Path) -> None:
    # A crash before the marker leaves members but no marker -> detectable incomplete.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture(root, tmp_path).packet.packet_id
    paths = derive_ecr_into_lake(data_root=root, packet_id=pid)
    record_name = next(iter(paths.values())).name

    (root.path / "derived" / raw_shard(pid) / pid / ECR_COMPLETION_LANE / record_name).unlink()
    assert not root.is_record_set_complete(
        subtree="derived",
        raw_anchor=pid,
        record_id=record_name,
        completion_lane=ECR_COMPLETION_LANE,
    )
