"""Pinned A2 AttachmentRecordEntry serializer tests (fail-capable).

Covers the ratified A2 contract (schema + derivation rule canonical): version
pins on every entry, canonical-bytes determinism, centralized manifest-version
dispatch that fails closed on unknown versions, required-field refusal, the
locator-not-identity boundary, and canonical-part equality between by-key
derivation and the materialized catalog rows.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.attachment_record_entry import (
    ATTACHMENT_RECORD_SCHEMA_VERSION,
    DERIVATION_RULE_VERSION,
    ENTRY_SERIALIZATION_VERSION,
    derive_attachment_record_entries,
    derive_entries_by_key,
    serialize_entries,
    serialize_entry,
)
from data_lake.catalog import rebuild_catalog, source_surface_catalog_rows
from data_lake.root import DataLakeRoot, DataLakeRootError
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet

_CATALOG_ONLY_KEYS = {"authority", "catalog_version", "catalog_schema_version", "stable_query_paths"}


def _capture(root: DataLakeRoot, tmp_path: Path, body: str):
    src = tmp_path / f"{body}.json"
    src.write_text(json.dumps({"b": body}, sort_keys=True), encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family="reddit",
        source_surface="r/EntrySerializer",
        source_locator=known_fact(f"https://www.reddit.com/r/test/{body}/"),
        decision_question="q",
        capture_context="entry serializer fixture",
    )


def _canonical_projection(row: dict) -> dict:
    """Strip catalog-only decorations from a materialized row, leaving the
    canonical entry the pinned serializer owns."""
    canonical = {key: value for key, value in row.items() if key not in _CATALOG_ONLY_KEYS}
    pins = dict(canonical["replay_version_pins"])
    pins.pop("catalog_schema_version", None)
    canonical["replay_version_pins"] = pins
    return canonical


def test_every_entry_carries_the_ratified_version_pins(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _capture(root, tmp_path, "alpha").packet.packet_id

    entries = derive_entries_by_key(root, packet_id)

    assert entries, "fixture packet produced no entries; pin test would be vacuous"
    for entry in entries:
        assert entry["attachment_record_schema_version"] == ATTACHMENT_RECORD_SCHEMA_VERSION
        assert entry["entry_serialization_version"] == ENTRY_SERIALIZATION_VERSION
        assert entry["derivation_rule_version"] == DERIVATION_RULE_VERSION
        assert entry["replay_version_pins"]["entry_serialization_version"] == (
            ENTRY_SERIALIZATION_VERSION
        )
        assert entry["replay_version_pins"]["derivation_rule_version"] == DERIVATION_RULE_VERSION
        assert "locator only" in entry["attachment_record_id_basis"]


def test_canonical_bytes_are_deterministic_and_newline_terminated(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _capture(root, tmp_path, "alpha").packet.packet_id

    first = serialize_entries(derive_entries_by_key(root, packet_id))
    second = serialize_entries(derive_entries_by_key(root, packet_id))

    assert first == second
    assert first.endswith("\n")
    line = first.splitlines()[0]
    parsed = json.loads(line)
    assert list(parsed.keys()) == sorted(parsed.keys()), "canonical bytes must sort keys"


def test_by_key_derivation_equals_canonical_part_of_catalog_rows(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _capture(root, tmp_path, "alpha").packet.packet_id
    assert rebuild_catalog(root)["status"] == "rebuilt"
    rows = source_surface_catalog_rows(
        root, source_family="reddit", source_surface="r/EntrySerializer"
    )["attachment_record_rows"]
    materialized_canonical = serialize_entries(
        [_canonical_projection(row) for row in rows if row["packet_id"] == packet_id]
    )

    derived = serialize_entries(derive_entries_by_key(root, packet_id))

    assert derived == materialized_canonical, (
        "the materialized catalog row must be exactly the canonical entry plus "
        "catalog decorations; any other difference means the serializer is not "
        "the single derivation rule"
    )


def test_dispatch_fails_closed_on_unknown_manifest_version() -> None:
    manifest = {
        "manifest_version": "source_capture_packet_manifest_v99_future",
        "preserved_files": [],
    }

    with pytest.raises(DataLakeRootError, match="unsupported raw packet manifest_version"):
        derive_attachment_record_entries(
            packet_id="0" * 26,
            raw_path="raw/000/" + "0" * 26,
            manifest_relpath="raw/000/" + "0" * 26 + "/manifest.json",
            manifest_sha256="0" * 64,
            manifest=manifest,
            bodies={},
        )


def test_legacy_manifest_without_version_string_dispatches(tmp_path: Path) -> None:
    manifest = {"preserved_files": []}

    entries = derive_attachment_record_entries(
        packet_id="0" * 26,
        raw_path="raw/000/" + "0" * 26,
        manifest_relpath="raw/000/" + "0" * 26 + "/manifest.json",
        manifest_sha256="0" * 64,
        manifest=manifest,
        bodies={},
    )

    assert entries == []


def test_missing_required_preserved_field_is_refused(tmp_path: Path) -> None:
    manifest = {
        "manifest_version": "source_capture_packet_manifest_v1",
        "preserved_files": [{"file_id": "file_01", "relative_packet_path": "raw/a.json"}],
    }

    with pytest.raises(DataLakeRootError, match="missing required string field"):
        derive_attachment_record_entries(
            packet_id="0" * 26,
            raw_path="raw/000/" + "0" * 26,
            manifest_relpath="raw/000/" + "0" * 26 + "/manifest.json",
            manifest_sha256="0" * 64,
            manifest=manifest,
            bodies={"file_01": b"{}"},
        )


def test_serialize_entry_round_trips(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _capture(root, tmp_path, "alpha").packet.packet_id

    entry = derive_entries_by_key(root, packet_id)[0]

    assert json.loads(serialize_entry(entry)) == entry
