from __future__ import annotations

import shutil
from pathlib import Path

from data_lake.root import DataLakeRoot
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet


def _capture(root: DataLakeRoot, tmp_path: Path, body: str):
    src = tmp_path / f"{body}.json"
    src.write_text(f'{{"b": "{body}"}}', encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family="reddit",
        source_surface="s",
        source_locator=known_fact(f"https://www.reddit.com/r/test/{body}/"),
        decision_question="q",
        capture_context="rebuild proof",
    )


def _snapshot(index_dir: Path) -> dict[str, bytes]:
    return {
        p.relative_to(index_dir).as_posix(): p.read_bytes()
        for p in sorted(index_dir.rglob("*"))
        if p.is_file()
    }


def test_indexes_rebuild_byte_identical_from_authoritative_truth(tmp_path: Path) -> None:
    # Prove-rebuildability for every populated index kind in this fixture:
    # indexes/availability holds no unique truth. Wiping the ENTIRE cache tier
    # and rebuilding from authoritative raw/ yields byte-identical entries.
    # indexes/derived_retrieval is build-deferred here; v4.1 creates its
    # directory skeleton, but any files must have a rebuilder before the claim survives.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_ids = [_capture(root, tmp_path, body).packet.packet_id for body in ("alpha", "beta", "gamma")]

    indexes = root.path / "indexes"
    derived_retrieval = indexes / "derived_retrieval"
    assert derived_retrieval.is_dir()
    assert not any(p.is_file() for p in derived_retrieval.rglob("*")), (
        "derived_retrieval has no current rebuilder; populate and rebuild it before claiming coverage"
    )
    before = _snapshot(indexes)
    assert set(before) == {f"availability/{packet_id}.json" for packet_id in packet_ids}

    shutil.rmtree(indexes)  # wipe the entire cache tier
    assert root.rebuild_availability() == 3
    # future populated index kinds: rebuild them here too (e.g. derived_retrieval)

    after = _snapshot(root.path / "indexes")
    assert after == before, "an index did not rebuild byte-identically -> it is smuggling non-rebuildable state"
