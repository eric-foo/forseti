from __future__ import annotations

import json
import shutil
from pathlib import Path

from data_lake.root import DataLakeRoot, raw_shard
from runners import run_data_lake_doctor as doctor
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet


def _capture_packet(root: DataLakeRoot, tmp_path: Path, body: str = "thread body") -> str:
    source = tmp_path / "source.json"
    source.write_text(body, encoding="utf-8")
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[source],
        source_family="reddit",
        source_surface="r/B2BMarketing",
        source_locator=known_fact("https://www.reddit.com/r/B2BMarketing/comments/x/"),
        decision_question="is this B2B tool getting unusual attention?",
        capture_context="doctor test capture",
    )
    return result.packet.packet_id


def test_inspect_data_lake_reports_clean_root(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture_packet(root, tmp_path)

    report = doctor.inspect_data_lake(root)

    assert report["status"] == "ok"
    assert report["raw_packet_count"] == 1
    assert report["verified_raw_packet_count"] == 1
    assert report["availability_count"] == 1
    assert report["missing_availability"] == []
    assert report["wrong_shard_packets"] == []
    assert report["root"]["lake_epoch"] == "v4.1"
    assert root.find_packet(pid) is not None


def test_inspect_data_lake_dry_run_reports_missing_availability_then_rebuilds(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture_packet(root, tmp_path)
    availability_path = root.path / "indexes" / "availability" / f"{pid}.json"
    availability_path.unlink()

    dry_run = doctor.inspect_data_lake(root)

    assert dry_run["status"] == "issues_found"
    assert dry_run["missing_availability"] == [pid]
    assert not availability_path.exists()

    repaired = doctor.inspect_data_lake(root, rebuild_availability=True)

    assert repaired["status"] == "ok"
    assert repaired["rebuild_availability_count"] == 1
    assert repaired["missing_availability"] == []
    assert availability_path.is_file()


def test_inspect_data_lake_reports_stale_availability(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture_packet(root, tmp_path)
    availability_path = root.path / "indexes" / "availability" / f"{pid}.json"
    entry = json.loads(availability_path.read_text(encoding="utf-8"))
    entry["manifest_sha256"] = "stale"
    availability_path.write_text(json.dumps(entry, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = doctor.inspect_data_lake(root)

    assert report["status"] == "issues_found"
    assert report["stale_availability"] == [{"packet_id": pid, "fields": ["manifest_sha256"]}]


def test_inspect_data_lake_reports_wrong_shard_packet(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture_packet(root, tmp_path)
    committed = root.find_packet(pid)
    assert committed is not None
    wrong_shard = "000" if raw_shard(pid) != "000" else "111"
    misplaced = root.path / "raw" / wrong_shard / pid
    shutil.copytree(committed, misplaced)

    report = doctor.inspect_data_lake(root)

    assert report["status"] == "issues_found"
    assert report["wrong_shard_packets"] == [f"raw/{wrong_shard}/{pid}"]


def test_main_prints_json_packet_lookup(tmp_path: Path, monkeypatch, capsys) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    pid = _capture_packet(root, tmp_path)

    def resolve_root(*, explicit=None):
        assert explicit == str(root.path)
        return root

    monkeypatch.setattr(doctor.DataLakeRoot, "resolve", staticmethod(resolve_root))

    assert doctor.main(["--data-root", str(root.path), "--packet-id", pid]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "ok"
    assert payload["packet"]["packet_id"] == pid
    assert payload["packet"]["source_family"] == "reddit"
