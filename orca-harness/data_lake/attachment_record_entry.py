"""Pinned AttachmentRecordEntry schema + deterministic derivation rule (A2).

This module is the canonical A2 object the owner ratified
(`forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_a2_attachment_record_entry_serialization_adr_v0.md`,
2026-07-03): the durable thing is the versioned entry schema plus the
deterministic derivation rule below — never any materialized row. Every
materialization (the generated Bronze catalog, any future engine under the
rebuildable index) is regenerable output of this serializer and carries no
authority; raw packet material stays the only truth.

Contract highlights (ADR Required Outputs 1-8):

- every entry carries `attachment_record_schema_version`,
  `entry_serialization_version`, `derivation_rule_version`, and
  `attachment_record_physicalization` pins, plus the raw replay pins;
- canonical bytes are sorted-key, ASCII-safe, compact-separator UTF-8 JSON
  with newline termination — no object-ordering or filesystem-order leakage;
- version branching is centralized here (``_require_supported_manifest_version``);
  consumers must not fork per-version logic — an unknown manifest version
  fails closed until a new derivation rule version is added deliberately;
- ``derive_entries_by_key`` derives canonical entries for a committed packet
  with zero indexes present (shard recompute -> verified raw read -> rule);
- the hash-derived ``attachment_record_id`` is a cache/query locator only;
  the canonical address stays `packet_id` + packet-scoped file key +
  packet-relative body ref + `body_sha256`/`hash_basis`;
- sealed packets are never rewritten: an old manifest version is either
  dispatchable by a frozen rule here or refused for a separate hold/replay
  decision.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import PurePosixPath
from typing import Any

from data_lake.root import DataLakeRoot, DataLakeRootError

from harness_utils import hash_file
from source_capture.models import HASH_BASIS_VALUES

ATTACHMENT_RECORD_SCHEMA_VERSION = "bronze_attachment_record_v0_schema_3"
ATTACHMENT_RECORD_PHYSICALIZATION = "manifest_equivalent_entry_over_raw_packet_body_v0"
ENTRY_SERIALIZATION_VERSION = "attachment_record_entry_serialization_v1"
DERIVATION_RULE_VERSION = "attachment_record_derivation_rule_v1"

RAW_PACKET_BODY_REF_KIND = "raw_packet_relative_path"
SUPPORTED_ATTACHMENT_RECORD_BODY_REF_KINDS = frozenset({RAW_PACKET_BODY_REF_KIND})
SUPPORTED_ATTACHMENT_RECORD_HASH_BASIS = frozenset({"raw_stored_bytes"})

# Central dispatch registry: raw manifest versions this derivation rule
# version knows how to derive from. Legacy packets with an absent/null
# manifest_version dispatch through the same v1 rule (incumbent-compatible).
# Adding a version here is a deliberate, reviewed act paired with a
# DERIVATION_RULE_VERSION decision, never a consumer-side fork.
SUPPORTED_RAW_PACKET_MANIFEST_VERSIONS = frozenset({"source_capture_packet_manifest_v1"})


def string_or_none(value: object) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return None


def required_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise DataLakeRootError(f"missing required string field for Attachment Record: {field}")
    return value


def visible_fact_value(value: object) -> str | None:
    if isinstance(value, dict) and value.get("status") == "known":
        return string_or_none(value.get("value"))
    return None


def visible_fact_summary(value: object) -> dict[str, str | None] | None:
    if not isinstance(value, dict):
        return None
    status = string_or_none(value.get("status"))
    if status is None:
        return None
    return {
        "status": status,
        "value": string_or_none(value.get("value")),
        "reason": string_or_none(value.get("reason")),
    }


def attachment_record_id(
    *, packet_id: str, file_id: str, relative_packet_path: str, body_sha256: str
) -> str:
    """Generated cache/query locator ONLY — never canonical identity (ADR
    Required Output 6). The canonical address is the packet handle plus the
    packet-scoped file key plus the body ref/hash fields."""
    material = json.dumps(
        [packet_id, file_id, relative_packet_path, body_sha256],
        ensure_ascii=True,
        separators=(",", ":"),
    )
    return f"ar_{hashlib.sha256(material.encode('utf-8')).hexdigest()[:32]}"


def require_supported_hash_basis(hash_basis: str, *, file_id: str) -> None:
    if hash_basis not in HASH_BASIS_VALUES:
        allowed_list = ", ".join(sorted(HASH_BASIS_VALUES))
        raise DataLakeRootError(
            f"unsupported preserved file hash_basis {hash_basis!r} for {file_id!r}; "
            f"expected Source Capture hash_basis in {{{allowed_list}}}"
        )
    if hash_basis not in SUPPORTED_ATTACHMENT_RECORD_HASH_BASIS:
        allowed_list = ", ".join(sorted(SUPPORTED_ATTACHMENT_RECORD_HASH_BASIS))
        raise DataLakeRootError(
            f"preserved file hash_basis {hash_basis!r} for {file_id!r} is valid upstream "
            "but unsupported by generated Attachment Record raw body resolution; "
            f"expected one of {{{allowed_list}}}"
        )


def _require_supported_manifest_version(manifest: dict[str, Any]) -> str | None:
    """Centralized version dispatch (ADR Required Output 4). Fails closed on
    an unknown manifest version: sealed packets are never coerced through a
    rule that does not know their format."""
    if "manifest_version" not in manifest or manifest.get("manifest_version") is None:
        return None
    manifest_version = manifest["manifest_version"]
    if (
        not isinstance(manifest_version, str)
        or not manifest_version
        or manifest_version not in SUPPORTED_RAW_PACKET_MANIFEST_VERSIONS
    ):
        allowed_list = ", ".join(sorted(SUPPORTED_RAW_PACKET_MANIFEST_VERSIONS))
        raise DataLakeRootError(
            f"unsupported raw packet manifest_version {manifest_version!r} for "
            f"Attachment Record entry derivation under {DERIVATION_RULE_VERSION}; "
            f"supported: {{{allowed_list}}} (plus legacy packets with absent/null "
            "manifest_version). Add a new derivation rule version deliberately in "
            "data_lake.attachment_record_entry; do not fork per-version logic in a "
            "consumer, and never rewrite the sealed packet."
        )
    return manifest_version


def source_slice_ids_by_file(source_slices: object) -> dict[str, list[str]]:
    by_file: dict[str, list[str]] = {}
    if not isinstance(source_slices, list):
        return by_file
    for item in source_slices:
        if not isinstance(item, dict):
            continue
        slice_id = string_or_none(item.get("slice_id"))
        preserved_file_ids = item.get("preserved_file_ids")
        if slice_id is None or not isinstance(preserved_file_ids, list):
            continue
        for file_id in preserved_file_ids:
            if isinstance(file_id, str) and file_id:
                by_file.setdefault(file_id, []).append(slice_id)
    return {file_id: sorted(set(slice_ids)) for file_id, slice_ids in by_file.items()}


def posture_summary(manifest: dict[str, Any]) -> dict[str, dict[str, str | None] | None]:
    return {
        "access_posture": visible_fact_summary(manifest.get("access_posture")),
        "archive_history_posture": visible_fact_summary(manifest.get("archive_history_posture")),
        "media_modality_posture": visible_fact_summary(manifest.get("media_modality_posture")),
        "re_capture_relationship": visible_fact_summary(manifest.get("re_capture_relationship")),
    }


def payload_schema_version(manifest: dict[str, Any], preserved: dict[str, Any]) -> str | None:
    preserved_value = string_or_none(preserved.get("payload_schema_version"))
    if preserved_value is not None:
        return preserved_value
    return string_or_none(manifest.get("payload_schema_version"))


def payload_kind(relative_packet_path: str, body: bytes) -> str:
    suffix = PurePosixPath(relative_packet_path).suffix.lower()
    if suffix == ".json":
        try:
            json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            return "text_body"
        return "json_body"
    if suffix in {".html", ".htm"}:
        return "html_body"
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError:
        return "binary_body"
    stripped = text.lstrip().lower()
    if stripped.startswith("<!doctype html") or stripped.startswith("<html"):
        return "html_body"
    return "text_body"


def derive_attachment_record_entries(
    *,
    packet_id: str,
    raw_path: str,
    manifest_relpath: str,
    manifest_sha256: str,
    manifest: dict[str, Any],
    bodies: dict[str, bytes],
) -> list[dict[str, Any]]:
    """The deterministic derivation rule: committed packet material in,
    canonical AttachmentRecordEntry dicts out. Pure derivation — no
    filesystem writes, no ordering leakage (entries sorted by locator id)."""
    manifest_version = _require_supported_manifest_version(manifest)
    preserved_files = manifest.get("preserved_files")
    if not isinstance(preserved_files, list):
        return []
    slices_by_file = source_slice_ids_by_file(manifest.get("source_slices"))
    entries: list[dict[str, Any]] = []
    for preserved in preserved_files:
        if not isinstance(preserved, dict):
            continue
        file_id = required_string(preserved.get("file_id"), "preserved_files.file_id")
        relative_packet_path = required_string(
            preserved.get("relative_packet_path"), "preserved_files.relative_packet_path"
        )
        body_sha256 = required_string(preserved.get("sha256"), "preserved_files.sha256")
        hash_basis = required_string(preserved.get("hash_basis"), "preserved_files.hash_basis")
        require_supported_hash_basis(hash_basis, file_id=file_id)
        size_bytes = preserved.get("size_bytes")
        if type(size_bytes) is not int:
            raise DataLakeRootError(f"preserved file {file_id!r} missing integer size_bytes")
        body = bodies.get(file_id)
        if body is None:
            raise DataLakeRootError(f"preserved body {file_id!r} missing after verified load")
        record_id = attachment_record_id(
            packet_id=packet_id,
            file_id=file_id,
            relative_packet_path=relative_packet_path,
            body_sha256=body_sha256,
        )
        entries.append(
            {
                "attachment_record_schema_version": ATTACHMENT_RECORD_SCHEMA_VERSION,
                "attachment_record_physicalization": ATTACHMENT_RECORD_PHYSICALIZATION,
                "entry_serialization_version": ENTRY_SERIALIZATION_VERSION,
                "derivation_rule_version": DERIVATION_RULE_VERSION,
                "attachment_record_id": record_id,
                "attachment_record_id_basis": (
                    "sha256(json_array[packet_id,file_id,relative_packet_path,body_sha256]); "
                    "cache/query locator only, never canonical identity"
                ),
                "packet_id": packet_id,
                "raw_path": raw_path,
                "manifest_relpath": manifest_relpath,
                "manifest_sha256": manifest_sha256,
                "source_family": string_or_none(manifest.get("source_family")),
                "source_surface": string_or_none(manifest.get("source_surface")),
                "source_locator": visible_fact_value(manifest.get("source_locator")),
                "source_slice_ids": slices_by_file.get(file_id, []),
                "file_id": file_id,
                "original_path": string_or_none(preserved.get("original_path")),
                "relative_packet_path": relative_packet_path,
                "body_ref_kind": RAW_PACKET_BODY_REF_KIND,
                "body_ref": {
                    "kind": RAW_PACKET_BODY_REF_KIND,
                    "packet_id": packet_id,
                    "file_id": file_id,
                    "relative_packet_path": relative_packet_path,
                    "body_sha256": body_sha256,
                    "hash_basis": hash_basis,
                },
                "body_sha256": body_sha256,
                "hash_basis": hash_basis,
                "size_bytes": size_bytes,
                "payload_kind": payload_kind(relative_packet_path, body),
                "payload_kind_basis": "generic_body_classification",
                "payload_schema_version": payload_schema_version(manifest, preserved),
                "raw_packet_manifest_version": manifest_version,
                "replay_version_pins": {
                    "raw_packet_manifest_version": manifest_version,
                    "source_capture_obligation_contract_version": string_or_none(
                        manifest.get("obligation_contract_version")
                    ),
                    "attachment_record_schema_version": ATTACHMENT_RECORD_SCHEMA_VERSION,
                    "entry_serialization_version": ENTRY_SERIALIZATION_VERSION,
                    "derivation_rule_version": DERIVATION_RULE_VERSION,
                },
                "posture_summary": posture_summary(manifest),
            }
        )
    return sorted(entries, key=lambda item: item["attachment_record_id"])


def serialize_entry(entry: dict[str, Any]) -> str:
    """Canonical bytes (ADR Required Output 3): sorted keys, ASCII-safe,
    compact separators, newline-terminated. JSONL-compatible."""
    return (
        json.dumps(entry, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n"
    )


def serialize_entries(entries: list[dict[str, Any]]) -> str:
    return "".join(serialize_entry(entry) for entry in entries)


def derive_entries_by_key(root: DataLakeRoot, packet_id: str) -> list[dict[str, Any]]:
    """Zero-index by-key derivation (ADR Required Output 5): recompute the
    shard from packet_id, verified-read the committed packet, and derive the
    canonical entries. Needs no index, locator, catalog, or queue; fails
    closed on missing packets, hash mismatches, and unknown manifest
    versions."""
    loaded = root.load_raw_packet(packet_id)
    container = loaded.container
    manifest_path = container / "manifest.json"
    return derive_attachment_record_entries(
        packet_id=packet_id,
        raw_path=container.relative_to(root.path).as_posix(),
        manifest_relpath=manifest_path.relative_to(root.path).as_posix(),
        manifest_sha256=hash_file(manifest_path),
        manifest=loaded.manifest,
        bodies=loaded.bodies,
    )
