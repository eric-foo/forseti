"""No-new-core-field enforcement gate (fail-capable).

Enforces the No-New-Core-Field Enforcement section of
`orca/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md`:
a deterministic gate rejects new direct source-family payload fields on
`SourceCapturePacket`, `SourceCaptureSlice`, or lake-core manifest/index
structures unless a later owner decision cites a cross-family promotion rule.

Each test pins one lake-core structure's exact field/key set. ANY drift --
a field added or removed -- fails the matching test. Updating a pin here is
the deliberate act the contract requires: do it only in the same change as
the owner decision that cites the cross-family promotion rule (or, for a
removal, the decision retiring the field). Convenience or first-consumer
pressure is insufficient per the contract.

The pins enforce schema shape only; they say nothing about field semantics,
values, or the truth of any packet.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.attachment_record_entry import derive_entries_by_key
from data_lake.root import DataLakeRoot
from source_capture.models import (
    PreservedFile,
    SourceCapturePacket,
    SourceCaptureSlice,
    known_fact,
)
from source_capture.writer import write_local_source_capture_packet

_PROMOTION_RULE_MESSAGE = (
    "lake-core field set changed. The write-boundary contract's No-New-Core-Field "
    "Enforcement section requires an owner decision citing a cross-family promotion "
    "rule before a new direct source-family payload field lands on lake-core "
    "structures (removals need the retiring decision). Update this pin only in the "
    "same change as that cited decision."
)

_SOURCE_CAPTURE_PACKET_FIELDS = [
    "access_posture",
    "actor_audience_context",
    "archive_history_posture",
    "capture_context",
    "capture_mode",
    "cold_start_at",
    "intended_cadence",
    "limitations",
    "manifest_version",
    "media_modality_posture",
    "obligation_contract_version",
    "operator_category",
    "packet_id",
    "pre_coverage_history_posture",
    "preserved_files",
    "re_capture_relationship",
    "receipt_metadata",
    "requested_decision_context",
    "series_id",
    "session_identity",
    "source_family",
    "source_locator",
    "source_slices",
    "source_surface",
    "timing",
    "visible_mode_changes",
    "warnings",
]

_SOURCE_CAPTURE_SLICE_FIELDS = [
    "access_posture",
    "archive_history_posture",
    "currency_pin",
    "limitations",
    "locale_pin",
    "locator",
    "media_modality_posture",
    "metric_observations",
    "preserved_file_ids",
    "re_capture_relationship",
    "session_visibility_pin",
    "slice_id",
    "timing",
    "variant_pin",
    "warning_notes",
]

_PRESERVED_FILE_FIELDS = [
    "file_id",
    "hash_basis",
    "original_path",
    "relative_packet_path",
    "sha256",
    "size_bytes",
]

_ATTACHMENT_RECORD_ENTRY_KEYS = [
    "attachment_record_id",
    "attachment_record_id_basis",
    "attachment_record_physicalization",
    "attachment_record_schema_version",
    "body_ref",
    "body_ref_kind",
    "body_sha256",
    "derivation_rule_version",
    "entry_serialization_version",
    "file_id",
    "hash_basis",
    "manifest_relpath",
    "manifest_sha256",
    "original_path",
    "packet_id",
    "payload_kind",
    "payload_kind_basis",
    "payload_schema_version",
    "posture_summary",
    "raw_packet_manifest_version",
    "raw_path",
    "relative_packet_path",
    "replay_version_pins",
    "size_bytes",
    "source_family",
    "source_locator",
    "source_slice_ids",
    "source_surface",
]


@pytest.fixture(scope="module")
def fixture_packet(tmp_path_factory: pytest.TempPathFactory):
    tmp = tmp_path_factory.mktemp("core-field-gate")
    src = tmp / "body.json"
    src.write_text(json.dumps({"b": 1}, sort_keys=True), encoding="utf-8")
    root = DataLakeRoot.for_test(tmp / "lake")
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family="reddit",
        source_surface="r/CoreFieldGate",
        source_locator=known_fact("https://www.reddit.com/r/test/core-field-gate/"),
        decision_question="q",
        capture_context="core field gate fixture",
    )
    return root, result


def test_source_capture_packet_field_set_is_pinned() -> None:
    assert sorted(SourceCapturePacket.model_fields) == _SOURCE_CAPTURE_PACKET_FIELDS, (
        _PROMOTION_RULE_MESSAGE
    )


def test_source_capture_slice_field_set_is_pinned() -> None:
    assert sorted(SourceCaptureSlice.model_fields) == _SOURCE_CAPTURE_SLICE_FIELDS, (
        _PROMOTION_RULE_MESSAGE
    )


def test_preserved_file_field_set_is_pinned() -> None:
    assert sorted(PreservedFile.model_fields) == _PRESERVED_FILE_FIELDS, (
        _PROMOTION_RULE_MESSAGE
    )


def test_manifest_top_level_key_set_is_pinned(fixture_packet) -> None:
    _, result = fixture_packet
    manifest = json.loads(Path(result.manifest_path).read_text(encoding="utf-8"))
    assert sorted(manifest) == _SOURCE_CAPTURE_PACKET_FIELDS, _PROMOTION_RULE_MESSAGE


def test_preserved_files_entry_key_set_is_pinned(fixture_packet) -> None:
    _, result = fixture_packet
    manifest = json.loads(Path(result.manifest_path).read_text(encoding="utf-8"))
    assert manifest["preserved_files"], "fixture produced no preserved files; pin would be vacuous"
    for entry in manifest["preserved_files"]:
        assert sorted(entry) == _PRESERVED_FILE_FIELDS, _PROMOTION_RULE_MESSAGE


def test_attachment_record_entry_key_set_is_pinned(fixture_packet) -> None:
    root, result = fixture_packet
    entries = derive_entries_by_key(root, result.packet.packet_id)
    assert entries, "fixture packet produced no entries; pin would be vacuous"
    for entry in entries:
        assert sorted(entry) == _ATTACHMENT_RECORD_ENTRY_KEYS, _PROMOTION_RULE_MESSAGE
