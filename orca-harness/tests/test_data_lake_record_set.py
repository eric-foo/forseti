from __future__ import annotations

from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, DataLakeRootError

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
        assert path == root.path / "derived" / _RA / lane / "r1.json"
        assert path.is_file()
    # marker written (last) and the set reads complete
    assert (root.path / "derived" / _RA / "set_marker" / "r1.json").is_file()
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
    assert not (root.path / "derived" / _RA / "lane_b" / "r1.json").exists()


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
    (root.path / "derived" / _RA / "lane_a" / "r1.json").unlink()
    assert not root.is_record_set_complete(
        subtree="derived", raw_anchor=_RA, record_id="r1.json", completion_lane="set_marker"
    )


def test_absent_set_reads_incomplete(tmp_path: Path) -> None:
    root = _root(tmp_path)
    assert not root.is_record_set_complete(
        subtree="derived", raw_anchor=_RA, record_id="nope.json", completion_lane="set_marker"
    )
