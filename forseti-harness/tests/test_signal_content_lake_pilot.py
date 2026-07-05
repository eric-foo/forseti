from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard
from signal_content.deriver import derive_signal_content
from signal_content.lake import SIGNAL_CONTENT_LANE, derive_signal_content_into_lake
from source_capture.models import SourceCapturePacket, known_fact
from source_capture.writer import write_local_source_capture_packet


def _capture(root: DataLakeRoot, tmp_path: Path):
    # A text-bodied packet so the slice has a supplied body and SCR emits a record.
    src = tmp_path / "thread.json"
    src.write_text('{"body": "a reddit thread with content"}', encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family="reddit",
        source_surface="r/test",
        source_locator=known_fact("https://www.reddit.com/r/test/comments/x/"),
        decision_question="q",
        capture_context="scr lake pilot",
    )


def _bodies(root: DataLakeRoot, packet_id: str) -> dict[str, str]:
    loaded = root.load_raw_packet(packet_id)
    return {file_id: body.decode("utf-8", "replace") for file_id, body in loaded.bodies.items()}


def test_derives_signal_content_record_into_lake(tmp_path: Path) -> None:
    # capture -> committed raw -> read by key (verified) -> SCR Silver record.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture(root, tmp_path).packet.packet_id

    derived_path = derive_signal_content_into_lake(data_root=root, packet_id=pid)

    assert derived_path.parent == root.path / "derived" / raw_shard(pid) / pid / SIGNAL_CONTENT_LANE
    assert derived_path.suffix == ".json"
    assert derived_path.is_file()

    # byte-matches the deriver's output on the verified-read packet
    packet = SourceCapturePacket.model_validate(root.load_raw_packet(pid).manifest)
    expected = derive_signal_content(packet, preserved_bodies=_bodies(root, pid))
    expected_bytes = (
        f"{json.dumps([scr.model_dump(mode='json') for scr in expected], indent=2, sort_keys=True)}\n"
    ).encode("utf-8")
    assert derived_path.read_bytes() == expected_bytes
    # the slice with a supplied body actually produced a record (not silently empty)
    assert len(expected) == 1

    # raw untouched
    assert root.load_raw_packet(pid).manifest["packet_id"] == pid


def test_re_derive_appends_a_sibling_not_overwrite(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture(root, tmp_path).packet.packet_id

    _first = derive_signal_content_into_lake(data_root=root, packet_id=pid)
    _second = derive_signal_content_into_lake(data_root=root, packet_id=pid)

    lane_dir = root.path / "derived" / raw_shard(pid) / pid / SIGNAL_CONTENT_LANE
    assert _first != _second
    assert len(list(lane_dir.glob("*.json"))) == 2


def test_explicit_record_id_is_create_only(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture(root, tmp_path).packet.packet_id

    derive_signal_content_into_lake(data_root=root, packet_id=pid, record_id="rec1")
    with pytest.raises(DataLakeRootError):
        derive_signal_content_into_lake(data_root=root, packet_id=pid, record_id="rec1")
