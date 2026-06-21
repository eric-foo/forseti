from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, DataLakeRootError
from ecr.deriver import (
    derive_identity_postures,
    derive_inspectability_postures,
    derive_source_visibility_postures,
    derive_timing_postures,
)
from ecr.lake import ECR_LANES, derive_ecr_into_lake
from source_capture.models import SourceCapturePacket, known_fact
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


def _expected_bytes(postures) -> bytes:
    return (
        f"{json.dumps([posture.model_dump(mode='json') for posture in postures], indent=2, sort_keys=True)}\n"
    ).encode("utf-8")


def test_derives_four_sibling_ecr_records(tmp_path: Path) -> None:
    # capture -> committed raw -> read by key (verified) -> 4 sibling Silver records.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture(root, tmp_path).packet.packet_id

    paths = derive_ecr_into_lake(data_root=root, packet_id=pid)

    # one derivation -> four siblings (one per epistemic kind), sharing one record_id
    assert set(paths) == set(ECR_LANES.values())
    assert len({path.name for path in paths.values()}) == 1
    for lane, path in paths.items():
        assert path.parent == root.path / "derived" / pid / lane
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
        assert len(list((root.path / "derived" / pid / lane).glob("*.json"))) == 2


def test_explicit_record_id_is_create_only(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture(root, tmp_path).packet.packet_id

    derive_ecr_into_lake(data_root=root, packet_id=pid, record_id="rec1")
    with pytest.raises(DataLakeRootError):
        derive_ecr_into_lake(data_root=root, packet_id=pid, record_id="rec1")
