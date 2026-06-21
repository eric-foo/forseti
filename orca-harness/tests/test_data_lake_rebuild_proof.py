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
        str(p.relative_to(index_dir)): p.read_bytes()
        for p in sorted(index_dir.rglob("*"))
        if p.is_file()
    }


def test_indexes_rebuild_byte_identical_from_authoritative_truth(tmp_path: Path) -> None:
    # Prove-rebuildability: indexes/ holds no unique truth. Wiping the ENTIRE cache
    # tier and rebuilding from the authoritative raw/ (+ derived/) yields
    # byte-identical entries. When a new index kind gains a rebuilder, rebuild it
    # in the wipe-then-rebuild step below so this proof keeps covering every index.
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    for body in ("alpha", "beta", "gamma"):
        _capture(root, tmp_path, body)

    indexes = root.path / "indexes"
    before = _snapshot(indexes)
    assert before, "expected availability index entries before the wipe"

    shutil.rmtree(indexes)  # wipe the entire cache tier
    assert root.rebuild_availability() == 3
    # future index kinds: rebuild them here too (e.g. derived_retrieval)

    after = _snapshot(root.path / "indexes")
    assert after == before, "an index did not rebuild byte-identically -> it is smuggling non-rebuildable state"
