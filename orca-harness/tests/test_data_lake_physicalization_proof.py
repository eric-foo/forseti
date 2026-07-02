"""PROOF-01..06: deterministic fixture-lake proof of the six Bronze lake
invariants under the ratified packet-member relationship (Gate 1 body-layout
ADR, owner-ratified 2026-07-02; Gate 2 erasure posture stays a ratified
deferral and is not exercised here).

One named proof per invariant, each in two halves exercised through the same
public API surface a real producer/consumer uses (DataLakeRoot, the packet
writer, and the public catalog/AR helpers — never private paths or fixture
internals):

- a clean half proving the invariant holds on a well-formed fixture lake;
- a seeded-violation half proving the gate can FAIL: the violation must be
  refused or surfaced loudly, so a silent success here is itself a defect.

Fixture-lake tier only. This is not production-lake validation, all-source
coverage, A2/backend selection, readiness, or a Bronze full-GT claim.
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from data_lake.catalog import (
    load_attachment_record_body,
    rebuild_catalog,
    source_surface_catalog_rows,
)
from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet

_SOURCE_FAMILY = "reddit"
_SOURCE_SURFACE = "r/PhysicalizationProof"


def _capture(root: DataLakeRoot, tmp_path: Path, body: str):
    src = tmp_path / f"{body}.json"
    src.write_text(json.dumps({"b": body}, sort_keys=True), encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family=_SOURCE_FAMILY,
        source_surface=_SOURCE_SURFACE,
        source_locator=known_fact(f"https://www.reddit.com/r/test/{body}/"),
        decision_question="q",
        capture_context="physicalization proof fixture",
    )


def _packet_container(root: DataLakeRoot, packet_id: str) -> Path:
    return root.path / "raw" / raw_shard(packet_id) / packet_id


def _corrupt_preserved_body(root: DataLakeRoot, packet_id: str, body: str) -> Path:
    """Overwrite the preserved body file's stored bytes (tamper simulation)."""
    assert body, "tamper helper requires a non-empty body"
    original = json.dumps({"b": body}, sort_keys=True).encode("utf-8")
    replacement_body = "z" * len(body)
    if replacement_body == body:
        replacement_body = "y" * len(body)
    tampered = json.dumps({"b": replacement_body}, sort_keys=True).encode("utf-8")
    assert len(tampered) == len(original), "tamper must preserve size to prove SHA checking"
    for path in sorted(_packet_container(root, packet_id).rglob("*")):
        if path.is_file() and path.read_bytes() == original:
            path.write_bytes(tampered)
            return path
    raise AssertionError("preserved body file not found in packet container")


def _index_snapshot(root: DataLakeRoot) -> dict[str, bytes]:
    indexes = root.path / "indexes"
    return {
        p.relative_to(indexes).as_posix(): p.read_bytes()
        for p in sorted(indexes.rglob("*"))
        if p.is_file()
    }


# --- PROOF-01: write-once raw -------------------------------------------------


def test_proof_01_write_once_raw_clean_publish_lands_and_verifies(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _capture(root, tmp_path, "alpha").packet.packet_id

    assert _packet_container(root, packet_id).is_dir()
    loaded = root.load_raw_packet(packet_id)
    assert loaded.manifest["packet_id"] == packet_id


def test_proof_01_violation_second_publish_of_same_packet_id_is_refused(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _capture(root, tmp_path, "alpha").packet.packet_id

    # Write-once fires at staging reservation for an occupied packet_id...
    with pytest.raises(DataLakeRootError, match="write-once"):
        root.stage_raw_packet(packet_id)

    # ...and again at publish time even when staging bypasses the reservation.
    bypass_staging = tmp_path / "bypass_staging"
    bypass_staging.mkdir()
    (bypass_staging / "manifest.json").write_text("{}", encoding="utf-8")
    with pytest.raises(DataLakeRootError, match="write-once"):
        root.publish_raw_packet(bypass_staging, packet_id)


# --- PROOF-02: append-only derived/ack ---------------------------------------


def test_proof_02_derived_and_ack_records_are_create_only(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _capture(root, tmp_path, "alpha").packet.packet_id

    for subtree in ("derived", "acknowledgements"):
        written = root.append_record(
            subtree=subtree,
            raw_anchor=packet_id,
            lane="proof_probe",
            record_id="record_01.json",
            data=b'{"ok": true}',
        )
        assert written.is_file()


def test_proof_02_violation_rewriting_an_existing_record_is_refused(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _capture(root, tmp_path, "alpha").packet.packet_id

    for subtree in ("derived", "acknowledgements"):
        root.append_record(
            subtree=subtree,
            raw_anchor=packet_id,
            lane="proof_probe",
            record_id="record_01.json",
            data=b'{"ok": true}',
        )
        with pytest.raises(DataLakeRootError, match="refusing to overwrite existing record"):
            root.append_record(
                subtree=subtree,
                raw_anchor=packet_id,
                lane="proof_probe",
                record_id="record_01.json",
                data=b'{"ok": "rewritten"}',
            )


# --- PROOF-03: read-by-key without any index ----------------------------------


def test_proof_03_by_key_read_recomputes_shard_and_needs_no_index(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _capture(root, tmp_path, "alpha").packet.packet_id

    shutil.rmtree(root.path / "indexes")

    loaded = root.load_raw_packet(packet_id)
    assert loaded.manifest["packet_id"] == packet_id


def test_proof_03_violation_missing_packet_fails_closed(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    _capture(root, tmp_path, "alpha")

    with pytest.raises(DataLakeRootError, match="raw packet not committed"):
        root.load_raw_packet("0" * 26)


# --- PROOF-04: hash verification under raw_stored_bytes ------------------------


def test_proof_04_verified_read_rehashes_stored_bytes(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    body = "alpha"
    packet_id = _capture(root, tmp_path, body).packet.packet_id

    loaded = root.load_raw_packet(packet_id)
    expected = json.dumps({"b": body}, sort_keys=True).encode("utf-8")
    assert any(body_bytes == expected for body_bytes in loaded.bodies.values())


def test_proof_04_violation_tampered_body_fails_verified_read(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    body = "alpha"
    packet_id = _capture(root, tmp_path, body).packet.packet_id

    _corrupt_preserved_body(root, packet_id, body)

    with pytest.raises(DataLakeRootError, match="preserved file sha256 mismatch"):
        root.load_raw_packet(packet_id)


# --- PROOF-05: public Attachment Record body resolution ------------------------


def test_proof_05_public_ar_surface_resolves_and_verifies_packet_member_body(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    body = "alpha"
    packet_id = _capture(root, tmp_path, body).packet.packet_id

    assert rebuild_catalog(root)["status"] == "rebuilt"
    rows = source_surface_catalog_rows(
        root, source_family=_SOURCE_FAMILY, source_surface=_SOURCE_SURFACE
    )
    records = [r for r in rows["attachment_record_rows"] if r["packet_id"] == packet_id]
    assert len(records) == 1
    record = records[0]

    assert record["hash_basis"] == "raw_stored_bytes"
    assert record["body_ref_kind"] == "raw_packet_relative_path"

    resolved = load_attachment_record_body(root, record)
    assert hashlib.sha256(resolved).hexdigest() == record["body_sha256"]
    assert resolved == json.dumps({"b": body}, sort_keys=True).encode("utf-8")


def test_proof_05_violation_tampered_body_fails_public_ar_resolution(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    body = "alpha"
    packet_id = _capture(root, tmp_path, body).packet.packet_id

    assert rebuild_catalog(root)["status"] == "rebuilt"
    rows = source_surface_catalog_rows(
        root, source_family=_SOURCE_FAMILY, source_surface=_SOURCE_SURFACE
    )
    record = next(r for r in rows["attachment_record_rows"] if r["packet_id"] == packet_id)

    _corrupt_preserved_body(root, packet_id, body)

    with pytest.raises(DataLakeRootError, match="preserved file sha256 mismatch"):
        load_attachment_record_body(root, record)


# --- PROOF-06: index rebuild from committed packet material --------------------


def test_proof_06_all_indexes_rebuild_byte_identical_including_catalog(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    for body in ("alpha", "beta"):
        _capture(root, tmp_path, body)
    assert rebuild_catalog(root)["status"] == "rebuilt"

    before = _index_snapshot(root)
    assert before, "fixture produced no index files; the rebuild proof would be vacuous"

    shutil.rmtree(root.path / "indexes")
    root.rebuild_availability()
    assert rebuild_catalog(root)["status"] == "rebuilt"

    assert _index_snapshot(root) == before, (
        "an index did not rebuild byte-identically from committed packet material "
        "-> it is smuggling non-rebuildable state"
    )


def test_proof_06_violation_reads_survive_index_loss_so_indexes_carry_no_authority(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    body = "alpha"
    packet_id = _capture(root, tmp_path, body).packet.packet_id
    assert rebuild_catalog(root)["status"] == "rebuilt"

    shutil.rmtree(root.path / "indexes")

    loaded = root.load_raw_packet(packet_id)
    assert loaded.manifest["packet_id"] == packet_id
    # The generated catalog is gone and must fail loudly (stale reads refused),
    # while raw truth stays readable by key: indexes are caches, never authority.
    with pytest.raises(DataLakeRootError, match="Bronze catalog is not current"):
        source_surface_catalog_rows(
            root, source_family=_SOURCE_FAMILY, source_surface=_SOURCE_SURFACE
        )
