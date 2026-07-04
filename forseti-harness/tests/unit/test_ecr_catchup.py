"""Offline behavioral tests for the ECR catch-up runner (consumption-seam entrypoint).

No network, no credentials. Commits real packets into a temp lake and asserts the
handoff's S-signals: the runner finds its own backlog (S1), does nothing twice with a
byte-unchanged lake tree (S2), re-surfaces on a deriver-policy bump (S3 — the packet
manifest is immutable and ECR reads no derived records, so the policy token is the
lane's ONLY growable input class), fails loud without acking on a damaged packet
(S4), isolates per-packet failure (S5), and honors the seam boundaries (S6: registered
ack namespace, committed anchors only, non-raising obligation).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from data_lake.consumption import find_acks
from data_lake.root import DataLakeRoot, DataLakeRootError
from ecr.lake import ECR_COMPLETION_LANE, ECR_LANES
from runners import run_ecr_catchup as ecr_runner
from runners.run_ecr_catchup import main, pending_packets, run_catchup
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet


def _commit_packet(data_root, tmp_path: Path, name: str = "thread") -> str:
    src = tmp_path / f"{name}.json"
    src.write_text(json.dumps({"body": f"a reddit thread: {name}"}), encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=data_root,
        input_files=[src],
        source_family="reddit",
        source_surface="r/test",
        source_locator=known_fact(f"https://www.reddit.com/r/test/comments/{name}/"),
        decision_question="q",
        capture_context="ecr catchup test",
    ).packet.packet_id


def _lake_tree_state(data_root) -> dict[str, str]:
    """Every file under the lake root -> sha256, for byte-unchanged idempotence asserts."""
    return {
        str(p.relative_to(data_root.path)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(data_root.path.rglob("*"))
        if p.is_file()
    }


def _tamper_packet(data_root, packet_id: str) -> None:
    """Corrupt a committed packet's preserved bytes so the verified read fails closed."""
    preserved = next((data_root.path / "raw").glob(f"*/{packet_id}/raw/*"))
    preserved.write_bytes(b"tampered bytes\n")


def _corrupt_manifest(data_root, packet_id: str) -> None:
    container = data_root.find_packet(packet_id)
    assert container is not None
    (container / "manifest.json").write_text("{not-json\n", encoding="utf-8")


def test_catchup_finds_backlog_derives_and_acks(tmp_path) -> None:
    # S1: a committed packet nobody pointed a per-packet command at is discovered
    # and derived by ONE catch-up run, with the completed set as ack evidence.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(data_root, tmp_path)
    assert pending_packets(data_root=data_root) == [pid]

    results = run_catchup(data_root=data_root)
    assert len(results) == 1
    assert results[0]["packet_id"] == pid
    assert results[0]["status"] == "derived"
    record_id = results[0]["record_id"]

    # the four sibling records + completion marker are committed and complete
    assert data_root.is_record_set_complete(
        subtree="derived", raw_anchor=pid, record_id=record_id,
        completion_lane=ECR_COMPLETION_LANE,
    )
    for lane in ECR_LANES.values():
        lane_dir = next((data_root.path / "derived").glob(f"*/{pid}/{lane}"))
        assert [p.name for p in lane_dir.iterdir()] == [record_id]

    # the ack is the lane-owned completion fact, under the registered ecr_set
    # namespace, carrying the minimum envelope + the completed-set evidence
    acks = find_acks(data_root, raw_anchor=pid, ack_namespace=ECR_COMPLETION_LANE)
    assert len(acks) == 1
    assert acks[0]["obligation"]["consumer"] == "ecr_catchup"
    assert acks[0]["obligation"]["deriver_version"] == ecr_runner.ECR_DERIVER_VERSION
    assert acks[0]["evidence"] == [
        {
            "kind": "record_set_complete",
            "raw_anchor": pid,
            "completion_lane": ECR_COMPLETION_LANE,
            "record_id": record_id,
        }
    ]
    assert pending_packets(data_root=data_root) == []


def test_catchup_second_run_is_byte_unchanged_noop(tmp_path) -> None:
    # S2: an immediate second run over the unchanged lake emits ZERO status entries
    # and performs ZERO lake writes (byte-unchanged tree, not merely no failures).
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_packet(data_root, tmp_path)
    assert [r["status"] for r in run_catchup(data_root=data_root)] == ["derived"]

    before = _lake_tree_state(data_root)
    assert run_catchup(data_root=data_root) == []
    assert _lake_tree_state(data_root) == before


def test_deriver_version_bump_resurfaces_and_rederives(tmp_path, monkeypatch) -> None:
    # S3: the deriver policy token is ECR's only re-trigger input (immutable raw,
    # no derived-record inputs). Bumping it re-surfaces the SAME anchor, derives a
    # FRESH sibling set under the new policy, and re-acks under the new
    # fingerprint; the run after that is silent again.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(data_root, tmp_path)
    original_version = ecr_runner.ECR_DERIVER_VERSION

    first = run_catchup(data_root=data_root)
    assert [r["status"] for r in first] == ["derived"]
    assert run_catchup(data_root=data_root) == []

    monkeypatch.setattr(ecr_runner, "ECR_DERIVER_VERSION", "test-policy-vnext")
    third = run_catchup(data_root=data_root)
    assert [r["status"] for r in third] == ["derived"]
    assert third[0]["record_id"] != first[0]["record_id"]  # fresh set, never overwrite

    acks = find_acks(data_root, raw_anchor=pid, ack_namespace=ECR_COMPLETION_LANE)
    assert len(acks) == 2
    assert {ack["obligation"]["deriver_version"] for ack in acks} == {
        original_version,
        "test-policy-vnext",
    }
    assert run_catchup(data_root=data_root) == []


def test_late_committed_packet_is_found_by_key(tmp_path) -> None:
    # Missed-event recovery flavor of S1: a packet committed AFTER the first run is
    # found purely by key on the next run; the already-acked packet stays silent.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_packet(data_root, tmp_path, "first")
    assert [r["status"] for r in run_catchup(data_root=data_root)] == ["derived"]

    late_pid = _commit_packet(data_root, tmp_path, "late")
    second = run_catchup(data_root=data_root)
    assert [(r["packet_id"], r["status"]) for r in second] == [(late_pid, "derived")]


def test_damaged_packet_fails_loud_without_ack_and_resurfaces(tmp_path) -> None:
    # S4: a damaged packet (verified read fails closed) is a typed failure with NO
    # ack, re-surfacing every run — never a silent skip or a fake completion fact.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(data_root, tmp_path)
    _tamper_packet(data_root, pid)

    results = run_catchup(data_root=data_root)
    assert len(results) == 1
    assert results[0]["packet_id"] == pid
    assert results[0]["status"] == "derive_failed"
    assert results[0]["error"]
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=ECR_COMPLETION_LANE) == []
    for lane in ECR_LANES.values():
        assert list((data_root.path / "derived").glob(f"*/{pid}/{lane}/*")) == []

    second = run_catchup(data_root=data_root)
    assert [r["status"] for r in second] == ["derive_failed"]
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=ECR_COMPLETION_LANE) == []


def test_corrupt_manifest_reconcile_failure_still_processes_healthy_packet(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    bad = _commit_packet(data_root, tmp_path, "bad")
    good = _commit_packet(data_root, tmp_path, "good")
    _corrupt_manifest(data_root, bad)

    results = run_catchup(data_root=data_root)
    by_packet = {r["packet_id"]: r for r in results}

    assert by_packet[bad]["status"] == "availability_reconcile_failed"
    assert "JSONDecodeError" in by_packet[bad]["error"]
    assert by_packet[good]["status"] == "derived"
    good_acks = find_acks(data_root, raw_anchor=good, ack_namespace=ECR_COMPLETION_LANE)
    assert len(good_acks) == 1
    assert find_acks(data_root, raw_anchor=bad, ack_namespace=ECR_COMPLETION_LANE) == []


def test_pending_packets_blocks_on_corrupt_manifest_reconcile_failure(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(data_root, tmp_path)
    _corrupt_manifest(data_root, pid)

    with pytest.raises(
        DataLakeRootError, match="availability reconcile failed before pending check"
    ):
        pending_packets(data_root=data_root)


def test_per_packet_failure_is_isolated(tmp_path) -> None:
    # S5: one damaged packet leaves its anchor unacknowledged while the batch
    # continues and the healthy packet completes and acks.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    good = _commit_packet(data_root, tmp_path, "good")
    bad = _commit_packet(data_root, tmp_path, "bad")
    _tamper_packet(data_root, bad)

    results = run_catchup(data_root=data_root)
    by_packet = {r["packet_id"]: r["status"] for r in results}
    assert by_packet == {good: "derived", bad: "derive_failed"}
    assert len(find_acks(data_root, raw_anchor=good, ack_namespace=ECR_COMPLETION_LANE)) == 1
    assert find_acks(data_root, raw_anchor=bad, ack_namespace=ECR_COMPLETION_LANE) == []


def test_check_cli_prints_pending_count(tmp_path, monkeypatch, capsys) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_packet(data_root, tmp_path)

    def fake_resolve(cls, *, explicit=None, **_kwargs):  # noqa: ANN001
        assert explicit is None
        return data_root

    monkeypatch.setattr(DataLakeRoot, "resolve", classmethod(fake_resolve))
    assert main(["--check"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "1\n"

    assert main(["--run"]) == 0
    captured = capsys.readouterr()
    assert len(captured.out.strip().splitlines()) == 1
    assert json.loads(captured.out.strip())["status"] == "derived"

    assert main(["--check"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "0\n"
