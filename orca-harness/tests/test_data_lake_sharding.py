"""Raw + derived/ack directory sharding, by-key resolution, the one-time relocate
migration, and the two adversarial-review (Codex) hardening fixes:
  - relocate FAILS CLOSED on a flat/sharded collision (never a hidden duplicate);
  - rebuild SKIPS a packet sitting in the wrong shard (no wrong-path availability).

Network-free, no heavy deps."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import (
    DataLakeRoot,
    DataLakeRootError,
    RAW_SHARD_HEX_WIDTH,
    raw_shard,
)

_PID = "01KVXAHFD3DFP8M0738Y33181G"  # a valid Crockford-26 packet_id / raw-anchor


def _lake(tmp_path: Path) -> DataLakeRoot:
    return DataLakeRoot.for_test(tmp_path / "lake")


def _manifest_bytes(pid: str) -> bytes:
    return (json.dumps({"packet_id": pid, "source_family": "test",
                        "source_surface": "s", "preserved_files": []}) + "\n").encode("utf-8")


def test_raw_shard_is_deterministic_3_hex():
    assert raw_shard(_PID) == raw_shard(_PID)
    assert len(raw_shard(_PID)) == RAW_SHARD_HEX_WIDTH == 3
    assert all(c in "0123456789abcdef" for c in raw_shard(_PID))


def test_raw_write_lands_sharded_and_reads_by_key(tmp_path):
    root = _lake(tmp_path)
    container = root.allocate_raw_packet_dir(_PID)
    assert container == root.path / "raw" / raw_shard(_PID) / _PID
    # by-key read recomputes the shard from packet_id -- no index/locator needed.
    assert root.find_packet(_PID) == container


def test_derived_and_acks_write_sharded_by_anchor(tmp_path):
    root = _lake(tmp_path)
    d = root.append_record(subtree="derived", raw_anchor=_PID, lane="lane_x",
                           record_id="r1", data=b"{}")
    assert d == root.path / "derived" / raw_shard(_PID) / _PID / "lane_x" / "r1"
    a = root.append_record(subtree="acknowledgements", raw_anchor=_PID, lane="ack_x",
                           record_id="a1", data=b"{}")
    assert a == root.path / "acknowledgements" / raw_shard(_PID) / _PID / "ack_x" / "a1"


def test_record_set_complete_round_trip_sharded(tmp_path):
    root = _lake(tmp_path)
    root.append_record_set(subtree="derived", raw_anchor=_PID, record_id="r1",
                           members={"lane_a": b"{}", "lane_b": b"{}"},
                           completion_lane="set_marker")
    base = root.path / "derived" / raw_shard(_PID) / _PID
    assert (base / "lane_a" / "r1").is_file()
    assert (base / "set_marker" / "r1").is_file()
    assert root.is_record_set_complete(subtree="derived", raw_anchor=_PID,
                                       record_id="r1", completion_lane="set_marker") is True


def test_record_path_and_lane_dir_resolve_by_key(tmp_path):
    root = _lake(tmp_path)
    root.append_record(subtree="derived", raw_anchor=_PID, lane="lane_x",
                       record_id="r1", data=b"{}")
    assert root.record_path(subtree="derived", raw_anchor=_PID, lane="lane_x",
                            record_id="r1").is_file()
    ld = root.lane_dir(subtree="derived", raw_anchor=_PID, lane="lane_x")
    assert ld == root.path / "derived" / raw_shard(_PID) / _PID / "lane_x"
    assert {f.name for f in ld.iterdir()} == {"r1"}


def test_relocate_moves_legacy_flat_then_idempotent_and_rebuildable(tmp_path):
    root = _lake(tmp_path)
    # simulate a legacy FLAT raw packet (pre-sharding layout).
    flat = root.path / "raw" / _PID
    flat.mkdir(parents=True)
    (flat / "manifest.json").write_bytes(_manifest_bytes(_PID))
    assert root.find_packet(_PID) is None  # by-key (sharded) does not see the flat packet

    assert root.relocate_to_sharded() == 1
    assert (root.path / "raw" / raw_shard(_PID) / _PID / "manifest.json").is_file()
    assert root.find_packet(_PID) is not None  # now found by key
    assert root.relocate_to_sharded() == 0  # idempotent re-run
    assert root.rebuild_availability() == 1  # 2-level walk picks it up


def test_relocate_fails_closed_on_flat_sharded_collision(tmp_path):
    # Codex fix: a flat packet whose sharded target ALSO exists is a hidden
    # duplicate -> fail closed, never silently skip / overwrite.
    root = _lake(tmp_path)
    flat = root.path / "raw" / _PID
    flat.mkdir(parents=True)
    (flat / "manifest.json").write_bytes(_manifest_bytes(_PID))
    sharded = root.path / "raw" / raw_shard(_PID) / _PID
    sharded.mkdir(parents=True)
    (sharded / "manifest.json").write_bytes(_manifest_bytes(_PID))
    with pytest.raises(DataLakeRootError, match="relocate collision"):
        root.relocate_to_sharded()


def test_rebuild_skips_packet_in_wrong_shard(tmp_path):
    # Codex fix: a packet under the WRONG shard dir is corruption -> rebuild does
    # not record it at a recomputed (wrong) path; failure stays visible as absence.
    root = _lake(tmp_path)
    wrong_shard = "000" if raw_shard(_PID) != "000" else "111"
    misplaced = root.path / "raw" / wrong_shard / _PID
    misplaced.mkdir(parents=True)
    (misplaced / "manifest.json").write_bytes(_manifest_bytes(_PID))
    assert root.rebuild_availability() == 0
    assert root.read_availability(_PID) is None
