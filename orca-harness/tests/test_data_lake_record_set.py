from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard

_RA = "anchor01"  # a valid raw-anchor segment; the set API validates the segment, not packet existence


def _root(tmp_path: Path) -> DataLakeRoot:
    return DataLakeRoot.for_test(tmp_path / "orca-data")


def test_append_record_set_writes_members_and_marker_complete(tmp_path: Path) -> None:
    root = _root(tmp_path)
    written = root.append_record_set(
        subtree="derived",
        raw_anchor=_RA,
        record_id="r1.json",
        members={"lane_a": b"a\n", "lane_b": b"b\n"},
        completion_lane="set_marker",
    )
    assert set(written) == {"lane_a", "lane_b"}
    for lane, path in written.items():
        assert path == root.path / "derived" / raw_shard(_RA) / _RA / lane / "r1.json"
        assert path.is_file()
    # marker written (last) and the set reads complete
    marker = root.path / "derived" / raw_shard(_RA) / _RA / "set_marker" / "r1.json"
    assert marker.is_file()
    # ADDITIVE manifest: the marker commits each member's lake-computed content sha256 (acceptance #1).
    body = json.loads(marker.read_text(encoding="utf-8"))
    assert body["member_sha256"] == {
        "lane_a": hashlib.sha256(b"a\n").hexdigest(),
        "lane_b": hashlib.sha256(b"b\n").hexdigest(),
    }
    assert root.is_record_set_complete(
        subtree="derived", raw_anchor=_RA, record_id="r1.json", completion_lane="set_marker"
    )


def test_append_record_set_preflight_refuses_partial(tmp_path: Path) -> None:
    # A pre-existing member for this record_id must fail the whole set before any new write.
    root = _root(tmp_path)
    root.append_record(subtree="derived", raw_anchor=_RA, lane="lane_a", record_id="r1.json", data=b"pre\n")
    with pytest.raises(DataLakeRootError, match="partial record set"):
        root.append_record_set(
            subtree="derived",
            raw_anchor=_RA,
            record_id="r1.json",
            members={"lane_a": b"a\n", "lane_b": b"b\n"},
            completion_lane="set_marker",
        )
    assert not (root.path / "derived" / raw_shard(_RA) / _RA / "lane_b" / "r1.json").exists()


def test_append_record_set_rejects_completion_lane_collision(tmp_path: Path) -> None:
    root = _root(tmp_path)
    with pytest.raises(DataLakeRootError, match="completion_lane"):
        root.append_record_set(
            subtree="derived",
            raw_anchor=_RA,
            record_id="r1.json",
            members={"lane_a": b"a\n"},
            completion_lane="lane_a",
        )


def test_append_record_set_requires_members(tmp_path: Path) -> None:
    root = _root(tmp_path)
    with pytest.raises(DataLakeRootError):
        root.append_record_set(
            subtree="derived", raw_anchor=_RA, record_id="r1.json", members={}, completion_lane="set_marker"
        )


def test_append_record_set_rejects_non_appendable_subtree(tmp_path: Path) -> None:
    root = _root(tmp_path)
    with pytest.raises(DataLakeRootError):
        root.append_record_set(
            subtree="raw", raw_anchor=_RA, record_id="r1.json", members={"lane_a": b"a\n"}, completion_lane="set_marker"
        )


def test_missing_member_reads_incomplete(tmp_path: Path) -> None:
    # Marker present but a member removed (simulated partial) -> not complete.
    root = _root(tmp_path)
    root.append_record_set(
        subtree="derived",
        raw_anchor=_RA,
        record_id="r1.json",
        members={"lane_a": b"a\n", "lane_b": b"b\n"},
        completion_lane="set_marker",
    )
    (root.path / "derived" / raw_shard(_RA) / _RA / "lane_a" / "r1.json").unlink()
    assert not root.is_record_set_complete(
        subtree="derived", raw_anchor=_RA, record_id="r1.json", completion_lane="set_marker"
    )


def test_marker_record_id_mismatch_reads_incomplete(tmp_path: Path) -> None:
    root = _root(tmp_path)
    root.append_record_set(
        subtree="derived",
        raw_anchor=_RA,
        record_id="r1.json",
        members={"lane_a": b"a\n", "lane_b": b"b\n"},
        completion_lane="set_marker",
    )
    marker = root.path / "derived" / raw_shard(_RA) / _RA / "set_marker" / "r1.json"
    marker.write_text(
        json.dumps({"record_id": "other.json", "member_lanes": ["lane_a", "lane_b"]}) + "\n",
        encoding="utf-8",
    )

    assert not root.is_record_set_complete(
        subtree="derived", raw_anchor=_RA, record_id="r1.json", completion_lane="set_marker"
    )


def test_marker_invalid_member_lane_reads_incomplete(tmp_path: Path) -> None:
    root = _root(tmp_path)
    root.append_record_set(
        subtree="derived",
        raw_anchor=_RA,
        record_id="r1.json",
        members={"lane_a": b"a\n"},
        completion_lane="set_marker",
    )
    marker = root.path / "derived" / raw_shard(_RA) / _RA / "set_marker" / "r1.json"
    marker.write_text(
        json.dumps({"record_id": "r1.json", "member_lanes": ["../escape"]}) + "\n",
        encoding="utf-8",
    )

    assert not root.is_record_set_complete(
        subtree="derived", raw_anchor=_RA, record_id="r1.json", completion_lane="set_marker"
    )


def test_is_record_set_complete_rejects_non_appendable_subtree(tmp_path: Path) -> None:
    root = _root(tmp_path)
    with pytest.raises(DataLakeRootError, match="subtree"):
        root.is_record_set_complete(
            subtree="raw", raw_anchor=_RA, record_id="r1.json", completion_lane="set_marker"
        )


def test_absent_set_reads_incomplete(tmp_path: Path) -> None:
    root = _root(tmp_path)
    assert not root.is_record_set_complete(
        subtree="derived", raw_anchor=_RA, record_id="nope.json", completion_lane="set_marker"
    )


# -- derivation-time durable content hash: read_record_set_member_sha256 ---------------------------


def _marker_path(root: DataLakeRoot, record_id: str = "r1.json") -> Path:
    return root.path / "derived" / raw_shard(_RA) / _RA / "set_marker" / record_id


def test_read_member_sha256_returns_committed_sha(tmp_path: Path) -> None:
    root = _root(tmp_path)
    root.append_record_set(
        subtree="derived",
        raw_anchor=_RA,
        record_id="r1.json",
        members={"lane_a": b"a\n", "lane_b": b"b\n"},
        completion_lane="set_marker",
    )
    assert root.read_record_set_member_sha256(
        subtree="derived",
        raw_anchor=_RA,
        record_id="r1.json",
        completion_lane="set_marker",
        member_lane="lane_a",
    ) == hashlib.sha256(b"a\n").hexdigest()


def test_read_member_sha256_absent_marker_returns_none(tmp_path: Path) -> None:
    # A truly ABSENT marker (legacy markerless record) is the ONLY legitimate None -- the caller's
    # stitch-time fallback path.
    root = _root(tmp_path)
    root.append_record(
        subtree="derived", raw_anchor=_RA, lane="transcript_asr", record_id="r1.json", data=b"x\n"
    )
    assert (
        root.read_record_set_member_sha256(
            subtree="derived",
            raw_anchor=_RA,
            record_id="r1.json",
            completion_lane="set_marker",
            member_lane="lane_a",
        )
        is None
    )


def test_read_member_sha256_corrupt_marker_raises(tmp_path: Path) -> None:
    # A PRESENT-but-malformed marker (bad JSON) is corruption -> RAISE (never collapse to None).
    root = _root(tmp_path)
    root.append_record_set(
        subtree="derived",
        raw_anchor=_RA,
        record_id="r1.json",
        members={"lane_a": b"a\n"},
        completion_lane="set_marker",
    )
    _marker_path(root).write_text("{not valid json", encoding="utf-8")
    with pytest.raises(DataLakeRootError, match="malformed"):
        root.read_record_set_member_sha256(
            subtree="derived",
            raw_anchor=_RA,
            record_id="r1.json",
            completion_lane="set_marker",
            member_lane="lane_a",
        )


def test_read_member_sha256_missing_member_sha_raises(tmp_path: Path) -> None:
    # A PRESENT marker that lacks the member's sha (e.g. an OLD marker with no member_sha256 field,
    # or one missing this lane) is corruption for a record that has a __set lane -> RAISE.
    root = _root(tmp_path)
    root.append_record_set(
        subtree="derived",
        raw_anchor=_RA,
        record_id="r1.json",
        members={"lane_a": b"a\n"},
        completion_lane="set_marker",
    )
    # Rewrite the marker WITHOUT member_sha256 (mimics a pre-this-lane marker).
    _marker_path(root).write_text(
        json.dumps({"record_id": "r1.json", "member_lanes": ["lane_a"]}) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(DataLakeRootError, match="member_sha256"):
        root.read_record_set_member_sha256(
            subtree="derived",
            raw_anchor=_RA,
            record_id="r1.json",
            completion_lane="set_marker",
            member_lane="lane_a",
        )


def test_is_record_set_complete_unchanged_with_member_sha256_field(tmp_path: Path) -> None:
    # The additive member_sha256 field does not disturb the presence-only completeness check.
    root = _root(tmp_path)
    root.append_record_set(
        subtree="derived",
        raw_anchor=_RA,
        record_id="r1.json",
        members={"lane_a": b"a\n", "lane_b": b"b\n"},
        completion_lane="set_marker",
    )
    assert root.is_record_set_complete(
        subtree="derived", raw_anchor=_RA, record_id="r1.json", completion_lane="set_marker"
    )
