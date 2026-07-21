from __future__ import annotations

import json
import shutil
from pathlib import Path

from data_lake.derived_retrieval_views import (
    current_generation_root,
    prove_derived_retrieval_rebuildability,
    rebuild_derived_retrieval,
)
from data_lake.root import DataLakeRoot
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet

_STAMP = {"generation_id": "0" * 32, "generated_at": "2026-07-02T00:00:00+00:00"}

_POLICY = {"policy_version": "v0", "policy_fingerprint_sha256": "a" * 64}

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
        if p.is_file() and "cache" not in p.parts and ".sqlite3" not in p.name
    }


def test_indexes_rebuild_byte_identical_from_authoritative_truth(tmp_path: Path) -> None:
    # Prove-rebuildability for every populated index kind in this fixture:
    # indexes/ holds no unique truth. Wiping the ENTIRE cache tier and
    # rebuilding from authoritative raw/ (+ committed derived/ack material)
    # yields byte-identical published entries. The disposable SQLite working
    # notebook is excluded from byte comparison; its deletion/reconstruction
    # is covered by the incremental-state recovery test. Silver Vault views
    # are rebuilt under a fixed generation stamp — the runner's
    # --prove-rebuildability does the same with the stamp recorded in the
    # stored manifest, so determinism here is the same claim it checks.
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_ids = [_capture(root, tmp_path, body).packet.packet_id for body in ("alpha", "beta", "gamma")]

    indexes = root.path / "indexes"
    rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
    before = _snapshot(indexes)
    assert {f"availability/{packet_id}.json" for packet_id in packet_ids} <= set(before)
    generation_prefix = (
        "derived_retrieval/silver_vault/core/generations/"
        f"{_STAMP['generation_id']}"
    )
    assert f"{generation_prefix}/query_tables/undone.json" in before
    assert f"{generation_prefix}/manifests/by_mention.json" in before

    shutil.rmtree(indexes)  # wipe the entire cache tier
    assert root.rebuild_availability() == 3
    rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)

    after = _snapshot(root.path / "indexes")
    assert after == before, "an index did not rebuild byte-identically -> it is smuggling non-rebuildable state"


def test_prove_classifies_malformed_stored_policy_as_unreadable_manifest(tmp_path: Path) -> None:
    # A by_mention manifest whose stored product_mention_policy is present but
    # malformed (not lowercase 64-hex) is manifest corruption. Prove must classify
    # it as a per-view failed_unreadable_manifest -- consistent with a missing key
    # -- rather than raising and aborting the whole proof run (which would lose the
    # per-view accounting the proof exists to produce).
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _capture(root, tmp_path, "alpha")
    rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)

    manifest_path = (
        current_generation_root(root)[0] / "manifests" / "by_mention.json"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["selection_policy_versions"]["product_mention_policy"][
        "policy_fingerprint_sha256"
    ] = "not-64-hex"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    result = prove_derived_retrieval_rebuildability(root)

    assert result["results"]["by_mention"] == "failed_unreadable_manifest"
    assert result["status"] == "failed"
    assert "by_mention" in result["failures"]
