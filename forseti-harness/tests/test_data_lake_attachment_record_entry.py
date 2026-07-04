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
from data_lake.catalog import (
    BRONZE_CATALOG_SCHEMA_VERSION,
    BRONZE_CATALOG_VERSION,
    rebuild_catalog,
    source_surface_catalog_rows,
)
from data_lake.root import DataLakeRoot, DataLakeRootError
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet

_CATALOG_ONLY_KEYS = {"authority", "catalog_version", "catalog_schema_version", "stable_query_paths"}
_CATALOG_REPLAY_PIN_KEYS = {"catalog_schema_version"}


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


def _assert_row_is_canonical_plus_catalog_decorations(row: dict, canonical: dict) -> None:
    assert set(row) == set(canonical) | _CATALOG_ONLY_KEYS
    assert row["catalog_version"] == BRONZE_CATALOG_VERSION
    assert row["catalog_schema_version"] == BRONZE_CATALOG_SCHEMA_VERSION
    assert isinstance(row["authority"], str) and row["authority"]
    stable_query_paths = row["stable_query_paths"]
    assert set(stable_query_paths) == {"by_attachment_record", "by_packet"}
    assert stable_query_paths["by_attachment_record"] == (
        f"attachment_records/by_attachment_record/{row['attachment_record_id']}.json"
    )
    assert stable_query_paths["by_packet"].startswith("attachment_records/by_packet/")
    assert stable_query_paths["by_packet"].endswith(".jsonl")
    row_pins = row["replay_version_pins"]
    canonical_pins = canonical["replay_version_pins"]
    assert set(row_pins) == set(canonical_pins) | _CATALOG_REPLAY_PIN_KEYS
    assert row_pins["catalog_schema_version"] == BRONZE_CATALOG_SCHEMA_VERSION


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
    derived_entries = derive_entries_by_key(root, packet_id)
    derived_by_id = {entry["attachment_record_id"]: entry for entry in derived_entries}
    rows_by_id = {
        row["attachment_record_id"]: row for row in rows if row["packet_id"] == packet_id
    }
    assert set(rows_by_id) == set(derived_by_id)
    for record_id, row in rows_by_id.items():
        _assert_row_is_canonical_plus_catalog_decorations(row, derived_by_id[record_id])
    materialized_canonical = serialize_entries(
        [_canonical_projection(rows_by_id[record_id]) for record_id in sorted(rows_by_id)]
    )

    derived = serialize_entries([derived_by_id[record_id] for record_id in sorted(derived_by_id)])

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


@pytest.mark.parametrize(
    "malformed_manifest_version",
    [
        "",
        12,
        ["source_capture_packet_manifest_v1"],
        {"version": "source_capture_packet_manifest_v1"},
    ],
)
def test_dispatch_fails_closed_on_malformed_manifest_version(
    malformed_manifest_version: object,
) -> None:
    manifest = {
        "manifest_version": malformed_manifest_version,
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


@pytest.mark.parametrize(
    "manifest",
    [
        {"preserved_files": []},
        {"manifest_version": None, "preserved_files": []},
    ],
)
def test_legacy_manifest_without_version_string_dispatches(manifest: dict) -> None:
    entries = derive_attachment_record_entries(
        packet_id="0" * 26,
        raw_path="raw/000/" + "0" * 26,
        manifest_relpath="raw/000/" + "0" * 26 + "/manifest.json",
        manifest_sha256="0" * 64,
        manifest=manifest,
        bodies={},
    )

    assert entries == []


def test_moved_string_fields_preserve_catalog_trim_semantics() -> None:
    body = b"{}"
    manifest = {
        "manifest_version": "source_capture_packet_manifest_v1",
        "source_family": " reddit ",
        "source_surface": " r/EntrySerializer ",
        "source_locator": {
            "status": "known",
            "value": " https://example.invalid/item ",
        },
        "source_slices": [{"slice_id": " slice_01 ", "preserved_file_ids": ["file_01"]}],
        "preserved_files": [
            {
                "file_id": "file_01",
                "relative_packet_path": "raw/body.json",
                "sha256": "0" * 64,
                "hash_basis": "raw_stored_bytes",
                "size_bytes": len(body),
                "original_path": " body.json ",
                "payload_schema_version": " schema-v1 ",
            }
        ],
        "access_posture": {
            "status": "known",
            "value": " local_file_only ",
            "reason": " fixture ",
        },
    }

    entries = derive_attachment_record_entries(
        packet_id="0" * 26,
        raw_path="raw/000/" + "0" * 26,
        manifest_relpath="raw/000/" + "0" * 26 + "/manifest.json",
        manifest_sha256="0" * 64,
        manifest=manifest,
        bodies={"file_01": body},
    )

    assert len(entries) == 1
    entry = entries[0]
    assert entry["source_family"] == "reddit"
    assert entry["source_surface"] == "r/EntrySerializer"
    assert entry["source_locator"] == "https://example.invalid/item"
    assert entry["source_slice_ids"] == ["slice_01"]
    assert entry["original_path"] == "body.json"
    assert entry["payload_schema_version"] == "schema-v1"
    assert entry["posture_summary"]["access_posture"] == {
        "status": "known",
        "value": "local_file_only",
        "reason": "fixture",
    }


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
