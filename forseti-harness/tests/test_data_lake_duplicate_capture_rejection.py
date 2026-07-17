from __future__ import annotations

from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot
from source_capture.models import known_fact
from source_capture.writer import DuplicateCapturePacketError, write_local_source_capture_packet


def _capture(
    root: DataLakeRoot,
    tmp_path: Path,
    *,
    locator: str = "https://www.reddit.com/r/B2BMarketing/comments/x/",
    files: dict[str, str] | None = None,
    stage_dirname: str = "stage",
) -> object:
    """Write one source capture packet. ``files`` maps staged filenames to their
    text content (default: a single ``body.txt``); order of ``input_files`` is the
    dict's insertion order, so callers can reorder keys to exercise order-independent
    duplicate comparison."""
    files = files if files is not None else {"body.txt": "thread body"}
    stage_dir = tmp_path / stage_dirname
    stage_dir.mkdir(exist_ok=True)
    input_paths = []
    for filename, content in files.items():
        path = stage_dir / filename
        path.write_text(content, encoding="utf-8")
        input_paths.append(path)
    return write_local_source_capture_packet(
        data_root=root,
        input_files=input_paths,
        source_family="reddit",
        source_surface="r/B2BMarketing",
        source_locator=known_fact(locator),
        decision_question="is this B2B tool getting unusual attention?",
        capture_context="b2b marketing screening",
    )


def test_byte_identical_recapture_same_locator_rejected(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    first = _capture(root, tmp_path, stage_dirname="stage1")
    first_packet_id = first.packet.packet_id

    with pytest.raises(DuplicateCapturePacketError) as excinfo:
        _capture(root, tmp_path, stage_dirname="stage2")

    assert excinfo.value.existing_packet_id == first_packet_id
    assert first_packet_id in str(excinfo.value)
    # Only the one, original packet is committed -- the duplicate write never
    # reached staging/publish.
    assert root.list_available(source_family="reddit") == [first_packet_id]


def test_duplicate_error_is_catchable_as_distinct_type(tmp_path: Path) -> None:
    # A deliberate unchanged-content-monitor flow can catch this exception
    # explicitly (it is a ValueError subclass, but a distinct, named type).
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    first = _capture(root, tmp_path, stage_dirname="stage1")

    try:
        _capture(root, tmp_path, stage_dirname="stage2")
        raise AssertionError("expected DuplicateCapturePacketError")
    except DuplicateCapturePacketError as exc:
        assert exc.existing_packet_id == first.packet.packet_id
    except ValueError:
        raise AssertionError(
            "duplicate rejection must raise the distinct DuplicateCapturePacketError type"
        )


def test_changed_bytes_same_locator_accepted(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    first = _capture(root, tmp_path, stage_dirname="stage1", files={"body.txt": "version one"})
    second = _capture(root, tmp_path, stage_dirname="stage2", files={"body.txt": "version two"})

    assert second.packet.packet_id != first.packet.packet_id
    assert set(root.list_available(source_family="reddit")) == {
        first.packet.packet_id,
        second.packet.packet_id,
    }


def test_identical_bytes_different_locator_accepted(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    first = _capture(
        root,
        tmp_path,
        stage_dirname="stage1",
        locator="https://www.reddit.com/r/B2BMarketing/comments/x/",
    )
    second = _capture(
        root,
        tmp_path,
        stage_dirname="stage2",
        locator="https://www.reddit.com/r/B2BMarketing/comments/y/",
    )

    assert second.packet.packet_id != first.packet.packet_id
    assert set(root.list_available(source_family="reddit")) == {
        first.packet.packet_id,
        second.packet.packet_id,
    }


def test_multi_file_packet_duplicate_compared_order_independently(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    first = _capture(
        root,
        tmp_path,
        stage_dirname="stage1",
        files={"a.txt": "alpha content", "b.txt": "beta content"},
    )
    first_packet_id = first.packet.packet_id

    # Same two files' bytes, staged/supplied in the OPPOSITE order: the sha256
    # multiset comparison must be order-independent, so this is still rejected
    # as a duplicate of the first packet.
    with pytest.raises(DuplicateCapturePacketError) as excinfo:
        _capture(
            root,
            tmp_path,
            stage_dirname="stage2",
            files={"b.txt": "beta content", "a.txt": "alpha content"},
        )

    assert excinfo.value.existing_packet_id == first_packet_id


def test_multi_file_packet_with_one_changed_file_accepted(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    first = _capture(
        root,
        tmp_path,
        stage_dirname="stage1",
        files={"a.txt": "alpha content", "b.txt": "beta content"},
    )
    second = _capture(
        root,
        tmp_path,
        stage_dirname="stage2",
        files={"a.txt": "alpha content", "b.txt": "beta content CHANGED"},
    )

    assert second.packet.packet_id != first.packet.packet_id
