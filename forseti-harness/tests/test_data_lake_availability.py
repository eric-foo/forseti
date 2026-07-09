from __future__ import annotations

import shutil
from pathlib import Path

from data_lake.root import DataLakeRoot
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet


def _reddit_capture(root: DataLakeRoot, tmp_path: Path, body: str = "thread body"):
    # A reddit-family packet from a local fixture standing in for a captured
    # B2B-marketing thread. The lake round trip is identical for a live capture;
    # only the bytes' origin differs (live fetch is the runner's job + your env).
    src = tmp_path / "reddit_thread.json"
    src.write_text(body, encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family="reddit",
        source_surface="r/B2BMarketing",
        source_locator=known_fact("https://www.reddit.com/r/B2BMarketing/comments/x/"),
        decision_question="is this B2B tool getting unusual attention?",
        capture_context="b2b marketing screening",
    )


def test_reddit_capture_round_trip_by_key(tmp_path: Path) -> None:
    # The anchor capability: capture -> committed raw -> derived (availability)
    # -> retrieve both by key.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    result = _reddit_capture(root, tmp_path)
    pid = result.packet.packet_id

    # raw committed and findable by key
    container = root.find_packet(pid)
    assert container is not None and container == root.path / "raw" / pid
    assert (container / "manifest.json").is_file()

    # the derived (content-free availability) record is findable by key
    entry = root.read_availability(pid)
    assert entry is not None
    assert entry["source_family"] == "reddit"
    assert entry["source_surface"] == "r/B2BMarketing"
    assert entry["raw_path"] == f"raw/{pid}"
    assert entry["manifest_sha256"]

    # discoverable by family
    assert pid in root.list_available(source_family="reddit")
    assert root.list_available(source_family="instagram") == []


def test_availability_rebuilds_from_raw(tmp_path: Path) -> None:
    # Re-derivability: wipe the index, rebuild from raw, get an identical entry.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    result = _reddit_capture(root, tmp_path)
    pid = result.packet.packet_id
    before = root.read_availability(pid)
    assert before is not None

    shutil.rmtree(root.path / "indexes" / "availability")
    assert root.read_availability(pid) is None
    assert root.find_packet(pid) is not None  # raw truth survives an index wipe

    indexed = root.rebuild_availability()
    assert indexed == 1
    assert root.read_availability(pid) == before  # rebuilt identically from raw
    assert pid in root.list_available()


def test_record_availability_requires_committed_raw(tmp_path: Path) -> None:
    from data_lake.root import DataLakeRootError
    import pytest

    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    from harness_utils import generate_ulid

    with pytest.raises(DataLakeRootError):
        root.record_availability(generate_ulid())  # nothing committed at that key


# -- live-runner seam: packet_assembly -> lake (no network) -----------------

def _reddit_slice():
    from source_capture.models import (
        PacketTiming,
        SourceCaptureSlice,
        known_fact,
        not_applicable,
        not_attempted,
        unknown_with_reason,
    )

    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason("not supplied"),
        source_edit_or_version=unknown_with_reason("not supplied"),
        capture_time=known_fact("2026-06-21T00:00:00Z"),
        recapture_time=not_applicable("first capture"),
        cutoff_posture=unknown_with_reason("not supplied"),
    )
    return SourceCaptureSlice(
        slice_id="slice_01",
        locator=known_fact("https://www.reddit.com/r/B2BMarketing/comments/x/"),
        timing=timing,
        access_posture=known_fact("direct_http succeeded with HTTP 200"),
        archive_history_posture=not_attempted("archive not queried"),
        media_modality_posture=not_attempted("linked media not fetched"),
        re_capture_relationship=not_applicable("first capture"),
        preserved_file_ids=["file_01"],
    )


def test_stage_and_write_packet_routes_to_lake(tmp_path: Path) -> None:
    # The seam every runner uses: packet_assembly stages off-tree and commits
    # into the lake (recording availability), exactly like a live capture minus
    # the network fetch.
    from source_capture.models import known_fact
    from source_capture.packet_assembly import stage_and_write_packet

    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    result = stage_and_write_packet(
        data_root=root,
        staged_artifacts=[("http_response_body.bin", b"<reddit thread bytes>")],
        source_slices=[_reddit_slice()],
        source_family="reddit",
        source_surface="r/B2BMarketing",
        source_locator=known_fact("https://www.reddit.com/r/B2BMarketing/comments/x/"),
        decision_question="is this B2B tool getting unusual attention?",
        capture_context="b2b marketing screening",
        access_posture=known_fact("direct_http succeeded with HTTP 200"),
        archive_history_posture=not_attempted_fact(),
        media_modality_posture=not_attempted_fact(),
        re_capture_relationship=not_applicable_fact(),
    )
    pid = result.packet.packet_id
    assert Path(result.output_directory) == root.path / "raw" / pid
    assert root.find_packet(pid) is not None
    entry = root.read_availability(pid)
    assert entry is not None and entry["source_family"] == "reddit"
    assert pid in root.list_available(source_family="reddit")


def test_stage_and_write_packet_requires_exactly_one_target(tmp_path: Path) -> None:
    import pytest
    from source_capture.packet_assembly import stage_and_write_packet

    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    artifacts = [("body.bin", b"x")]
    with pytest.raises(ValueError):
        stage_and_write_packet(staged_artifacts=artifacts, source_slices=[_reddit_slice()])  # neither
    with pytest.raises(ValueError):
        stage_and_write_packet(  # both
            output_directory=tmp_path / "out",
            data_root=root,
            staged_artifacts=artifacts,
            source_slices=[_reddit_slice()],
        )


def not_attempted_fact():
    from source_capture.models import not_attempted

    return not_attempted("not attempted")


def not_applicable_fact():
    from source_capture.models import not_applicable

    return not_applicable("not applicable")
