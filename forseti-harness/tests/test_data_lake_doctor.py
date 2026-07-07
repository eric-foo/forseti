from __future__ import annotations

import json
import shutil
from pathlib import Path

from data_lake.root import DataLakeRoot, raw_shard
from harness_utils import generate_ulid
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
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
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
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
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
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    pid = _capture_packet(root, tmp_path)
    availability_path = root.path / "indexes" / "availability" / f"{pid}.json"
    entry = json.loads(availability_path.read_text(encoding="utf-8"))
    entry["manifest_sha256"] = "stale"
    availability_path.write_text(json.dumps(entry, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = doctor.inspect_data_lake(root)

    assert report["status"] == "issues_found"
    assert report["stale_availability"] == [{"packet_id": pid, "fields": ["manifest_sha256"]}]


def test_inspect_data_lake_reports_wrong_shard_packet(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
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
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
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


def test_inspect_data_lake_reports_read_failure_on_corrupt_body(tmp_path: Path) -> None:
    # The most dangerous false-pass: a committed, indexed packet whose preserved
    # body bytes are corrupt. The availability index still matches the untouched
    # manifest, so only the load_raw_packet read-verification pass can catch it.
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    pid = _capture_packet(root, tmp_path)
    container = root.find_packet(pid)
    assert container is not None
    manifest = json.loads((container / "manifest.json").read_text(encoding="utf-8"))
    preserved = manifest["preserved_files"][0]
    body_path = container.joinpath(*preserved["relative_packet_path"].split("/"))
    body_path.write_bytes(body_path.read_bytes() + b"corruption")

    report = doctor.inspect_data_lake(root)

    assert report["status"] == "issues_found"
    assert report["raw_packet_count"] == 1
    assert report["verified_raw_packet_count"] == 0
    assert [failure["packet_id"] for failure in report["read_failures"]] == [pid]
    # Index looks clean; the corruption is surfaced only by the read pass.
    assert report["missing_availability"] == []
    assert report["stale_availability"] == []


def test_inspect_data_lake_reports_missing_manifest_container(tmp_path: Path) -> None:
    # A packet-id-named container with no manifest (aborted allocate / half
    # publish / deleted manifest) must not read as a clean lake.
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _capture_packet(root, tmp_path)
    orphan_pid = generate_ulid()
    partial = root.path / "raw" / raw_shard(orphan_pid) / orphan_pid
    partial.mkdir(parents=True)

    report = doctor.inspect_data_lake(root)

    assert report["status"] == "issues_found"
    assert report["missing_manifest_raw_containers"] == [
        f"raw/{raw_shard(orphan_pid)}/{orphan_pid}"
    ]
    # The partial container must not inflate the valid/verified packet counts.
    assert report["raw_packet_count"] == 1
    assert report["verified_raw_packet_count"] == 1


def test_inspect_data_lake_reports_legacy_flat_missing_manifest(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _capture_packet(root, tmp_path)
    legacy_pid = generate_ulid()
    legacy_partial = root.path / "raw" / legacy_pid
    legacy_partial.mkdir(parents=True)

    report = doctor.inspect_data_lake(root)

    assert report["status"] == "issues_found"
    assert report["missing_manifest_raw_containers"] == [f"raw/{legacy_pid}"]
    assert report["raw_packet_count"] == 1
    assert report["verified_raw_packet_count"] == 1


def test_main_packet_lookup_reports_missing_packet_error(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    # A --packet-id lookup for an absent packet must surface an error and a
    # non-zero exit, never hide it behind a zero-exit "ok" report.
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _capture_packet(root, tmp_path)
    absent_pid = generate_ulid()

    monkeypatch.setattr(
        doctor.DataLakeRoot, "resolve", staticmethod(lambda *, explicit=None: root)
    )

    exit_code = doctor.main(["--data-root", str(root.path), "--packet-id", absent_pid])

    assert exit_code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "issues_found"
    assert payload["packet"]["packet_id"] == absent_pid
    assert "error" in payload["packet"]
