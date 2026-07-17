"""Rebuildable Bronze catalog indexes over committed raw packets.

The catalog is generated read state under ``indexes/derived_retrieval``. It is
never authority: raw packet manifests and preserved bytes remain the source of
truth, and this module rebuilds catalog files from verified raw packets.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable

from data_lake.attachment_record_entry import (
    ATTACHMENT_RECORD_PHYSICALIZATION,
    ATTACHMENT_RECORD_SCHEMA_VERSION,
    RAW_PACKET_BODY_REF_KIND,
    SUPPORTED_ATTACHMENT_RECORD_BODY_REF_KINDS,
    SUPPORTED_ATTACHMENT_RECORD_HASH_BASIS,
    attachment_record_id,
    derive_attachment_record_entries,
    require_supported_hash_basis,
    required_string,
    string_or_none,
    visible_fact_value,
)
from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard
from harness_utils import hash_file

BRONZE_CATALOG_VERSION = "bronze_catalog_v0"
BRONZE_CATALOG_SCHEMA_VERSION = "bronze_catalog_v0_schema_3"
# Canonical A2 objects live in data_lake.attachment_record_entry (the pinned
# serializer); these names are compatibility aliases for existing consumers.
BRONZE_ATTACHMENT_RECORD_SCHEMA_VERSION = ATTACHMENT_RECORD_SCHEMA_VERSION
BRONZE_ATTACHMENT_RECORD_PHYSICALIZATION = ATTACHMENT_RECORD_PHYSICALIZATION
BRONZE_BASELINE_STATUS = "bronze_full_gt_ratified_v0"
BRONZE_BASELINE_SEMANTICS = (
    "full_god_tier_typed_raw_truth_retrievability_and_physicalization; "
    "fixture-proof tier only, under the ratified Gate 2 claim ceiling; "
    "ratified per core_spine_v0_data_lake_bronze_full_gt_declaration_v0, "
    "which is authoritative for the claim and its full exclusion list -- "
    "this field only surfaces it, non-authoritative; named exclusions "
    "include no production-lake validation, no backend/engine selection, "
    "and no erasure capability"
)
CATALOG_RELATIVE_ROOT = ("indexes", "derived_retrieval", "bronze_catalog", "v0")
_PACKET_ID_RE = re.compile(r"[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{26}")
_CATALOG_AUTHORITY = "generated_from_raw_packet_manifests; raw remains authoritative"
_RAW_PACKET_BODY_REF_KIND = RAW_PACKET_BODY_REF_KIND
_SUPPORTED_ATTACHMENT_RECORD_HASH_BASIS = SUPPORTED_ATTACHMENT_RECORD_HASH_BASIS
_SUPPORTED_ATTACHMENT_RECORD_BODY_REF_KINDS = SUPPORTED_ATTACHMENT_RECORD_BODY_REF_KINDS
_SOURCE_SURFACE_COMPLETENESS = (
    "observed_source_surface_coverage_only; not capture_support, silver_readiness, "
    "projection_coverage, source_family_completeness, or validation"
)
_SOURCE_SURFACE_FIELD_SEMANTICS = {
    "attachment_record_count": (
        "count of generated Attachment Record entries for packets in this observed "
        "source-surface bucket; not source-family completeness or payload validation"
    ),
    "attachment_records_path": (
        "relative generated JSONL bucket for Attachment Record query rows sharing "
        "this source_surface string when present; consumers must still filter rows "
        "by source_family when needed"
    ),
    "by_source_surface_path": (
        "relative generated JSONL bucket for this source_surface string when present; "
        "the bucket may include multiple source families and consumers must still "
        "filter rows by source_family when needed"
    ),
    "facet_extractor": (
        "registered means a source-specific facet extractor is wired for this "
        "observed source_family/source_surface pair; universal_only means only "
        "universal packet facets were emitted; neither value claims semantic "
        "completeness, capture support, Silver readiness, or projection coverage"
    ),
    "facet_namespaces": (
        "sorted union of facet namespaces observed across packets in the "
        "source-surface bucket; namespace presence does not mean every packet has "
        "that namespace"
    ),
}
_ATTACHMENT_RECORD_COMPLETENESS = (
    "physicalized_manifest_equivalent_attachment_records_over_preserved_raw_packet_bodies; "
    "body remains a hash-checked raw packet member, not a copied attachments/ body; "
    "not Manifest v2, not source-family payload validation, and not downstream currentness"
)
_ATTACHMENT_RECORD_FIELD_SEMANTICS = {
    "attachment_record_id": (
        "stable generated key derived from packet_id, preserved file_id, "
        "relative_packet_path, and body_sha256; it is not the positional file_id"
    ),
    "attachment_record_physicalization": (
        "manifest_equivalent_entry_over_raw_packet_body_v0 means the typed entry is "
        "generated under the Bronze catalog and resolves an immutable preserved body "
        "inside its raw packet; no body copy is created"
    ),
    "body_ref": (
        "structured reference to the preserved raw packet member; it repeats packet_id, "
        "file_id, relative_packet_path, body_sha256, and hash_basis so consumers do not "
        "inherit positional file_id or staging-path semantics"
    ),
    "body_ref_kind": (
        "raw_packet_relative_path means the body remains in the raw packet and is "
        "resolved through DataLakeRoot.load_raw_packet rather than copied into a new store"
    ),
    "payload_kind": (
        "generic byte-shape classification from path/content only; source-family semantic "
        "kinds require a future registry and are not lake-core fields"
    ),
}


_COVERAGE_CENSUS_SEMANTICS = (
    "read_only_observed_bronze_coverage_from_verified_raw_packet_manifests; "
    "not a capture-lane registry, not source-family completeness, not generated-catalog "
    "currentness unless catalog_status is ok, not Silver readiness, and not validation"
)
_COVERAGE_CENSUS_FIELD_SEMANTICS = {
    "catalog_status": (
        "status from inspect_catalog; ok means generated catalog files byte-match the "
        "raw-derived expected snapshot, issues_found means consumers must treat query "
        "path hints as stale/missing/orphan-risk until rebuild; the census carries "
        "bounded issue samples only, and full lists stay in inspect mode"
    ),
    "expected_packet_count": (
        "raw-derived expected committed packet total from verified manifests; not "
        "proof that generated packet index files are current"
    ),
    "indexed_packet_count": (
        "readable generated by_packet entry total observed under the catalog root"
    ),
    "attachment_record_count": (
        "raw-derived expected generated Attachment Record row total over preserved "
        "packet bodies; body remains a hash-checked raw packet member, not a copied attachments/ body"
    ),
    "indexed_attachment_record_count": (
        "parseable row total observed in generated "
        "attachment_records/all_attachment_records.jsonl; currentness is still governed "
        "by catalog_status and catalog_issue_summary"
    ),
    "source_family_count": (
        "count of non-null observed source_family buckets; unknown/null packets are "
        "reported separately and do not increase the named-family headline"
    ),
    "unknown_source_family_packet_count": (
        "raw-derived packet total for manifests without a non-blank source_family"
    ),
    "unknown_source_family_attachment_record_count": (
        "raw-derived generated Attachment Record row total for manifests without a "
        "non-blank source_family"
    ),
    "source_surface_count": (
        "raw-derived expected observed (source_family, source_surface) bucket total"
    ),
    "source_families": (
        "observed packet totals grouped by source_family, including null when manifests "
        "do not carry a non-blank source_family; not a supported-lane registry"
    ),
    "source_surfaces": (
        "observed (source_family, source_surface) buckets with packet and generated "
        "Attachment Record counts; rows are source-family-agnostic and include future "
        "surfaces without requiring a lake-core schema change"
    ),
}

_COVERAGE_CENSUS_ISSUE_SAMPLE_LIMIT = 25

@dataclass(frozen=True)
class CatalogFacet:
    facet_type: str
    namespace: str
    value: str
    role: str
    source: str
    slice_id: str | None = None
    json_pointer: str | None = None

    def to_dict(self) -> dict[str, str]:
        data = {
            "facet_type": self.facet_type,
            "namespace": self.namespace,
            "value": self.value,
            "role": self.role,
            "source": self.source,
        }
        if self.slice_id is not None:
            data["slice_id"] = self.slice_id
        if self.json_pointer is not None:
            data["json_pointer"] = self.json_pointer
        return data


FacetExtractor = Callable[[dict[str, Any], dict[str, bytes]], Iterable[CatalogFacet]]


def rebuild_catalog(root: DataLakeRoot) -> dict[str, Any]:
    """Rebuild the generated Bronze catalog from verified committed raw packets."""
    entries = _build_entries(root)
    attachment_records = _attachment_records(entries)
    source_surfaces = _source_surface_summary(entries)
    snapshot = _catalog_snapshot(entries, source_surfaces, attachment_records)
    root._reverify()
    catalog_root = _catalog_root(root)
    if catalog_root.exists():
        shutil.rmtree(catalog_root)
    _write_snapshot(catalog_root, snapshot)
    return {
        "status": "rebuilt",
        "catalog_version": BRONZE_CATALOG_VERSION,
        "catalog_schema_version": BRONZE_CATALOG_SCHEMA_VERSION,
        "bronze_baseline_status": BRONZE_BASELINE_STATUS,
        "bronze_baseline_semantics": BRONZE_BASELINE_SEMANTICS,
        "packet_count": len(entries),
        "attachment_record_count": len(attachment_records),
        "source_surface_count": len(source_surfaces),
        "source_surfaces": source_surfaces,
        "file_count": len(snapshot),
        "catalog_root": _rel(root, catalog_root),
    }


def inspect_catalog(root: DataLakeRoot) -> dict[str, Any]:
    """Compare generated catalog files to the raw-derived expected catalog."""
    expected = _build_entries(root)
    attachment_records = _attachment_records(expected)
    source_surfaces = _source_surface_summary(expected)
    expected_snapshot = _catalog_snapshot(expected, source_surfaces, attachment_records)
    catalog_root = _catalog_root(root)
    actual_snapshot, read_failures = _read_snapshot(root, catalog_root)
    missing_files = sorted(set(expected_snapshot) - set(actual_snapshot))
    orphaned_files = sorted(set(actual_snapshot) - set(expected_snapshot))
    stale_files = sorted(
        path
        for path in set(expected_snapshot) & set(actual_snapshot)
        if actual_snapshot[path] != expected_snapshot[path]
    )
    indexed_attachment_record_count = _indexed_attachment_record_count(
        actual_snapshot.get("attachment_records/all_attachment_records.jsonl")
    )

    by_packet = catalog_root / "by_packet"
    existing: dict[str, dict[str, Any]] = {}
    if by_packet.is_dir():
        for path in sorted(by_packet.glob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                read_failures.append({"path": _rel(root, path), "error": str(exc)})
                continue
            if isinstance(payload, dict) and isinstance(payload.get("packet_id"), str):
                existing[payload["packet_id"]] = payload
            else:
                read_failures.append(
                    {"path": _rel(root, path), "error": "catalog entry is not a packet object"}
                )

    expected_by_packet = {entry["packet_id"]: _packet_index_entry(entry) for entry in expected}
    missing = sorted(set(expected_by_packet) - set(existing))
    orphaned = sorted(set(existing) - set(expected_by_packet))
    stale = sorted(
        packet_id
        for packet_id in set(expected_by_packet) & set(existing)
        if existing[packet_id] != expected_by_packet[packet_id]
    )
    issues = bool(
        missing
        or orphaned
        or stale
        or read_failures
        or missing_files
        or orphaned_files
        or stale_files
    )
    return {
        "status": "issues_found" if issues else "ok",
        "catalog_version": BRONZE_CATALOG_VERSION,
        "catalog_schema_version": BRONZE_CATALOG_SCHEMA_VERSION,
        "bronze_baseline_status": BRONZE_BASELINE_STATUS,
        "bronze_baseline_semantics": BRONZE_BASELINE_SEMANTICS,
        "expected_packet_count": len(expected),
        "indexed_packet_count": len(existing),
        "attachment_record_count": len(attachment_records),
        "indexed_attachment_record_count": indexed_attachment_record_count,
        "source_surface_count": len(source_surfaces),
        "source_surfaces": source_surfaces,
        "missing_packets": missing,
        "orphaned_packets": orphaned,
        "stale_packets": stale,
        "catalog_read_failures": read_failures,
        "missing_files": missing_files,
        "orphaned_files": orphaned_files,
        "stale_files": stale_files,
        "catalog_root": _rel(root, catalog_root),
    }


def catalog_coverage_census(root: DataLakeRoot) -> dict[str, Any]:
    """Return an inspect-only Bronze coverage census over the current catalog state."""
    report = inspect_catalog(root)
    source_surfaces = [_coverage_census_surface_row(row) for row in report["source_surfaces"]]
    source_families = _coverage_census_source_families(source_surfaces)
    unknown_source_family = next(
        (row for row in source_families if row["source_family"] is None),
        None,
    )
    return {
        "status": report["status"],
        "census_kind": "bronze_catalog_observed_coverage_census",
        "authority": _CATALOG_AUTHORITY,
        "catalog_version": report["catalog_version"],
        "catalog_schema_version": report["catalog_schema_version"],
        "bronze_baseline_status": BRONZE_BASELINE_STATUS,
        "bronze_baseline_semantics": BRONZE_BASELINE_SEMANTICS,
        "coverage_basis": "verified_raw_packet_manifests_compared_to_generated_catalog",
        "semantics": _COVERAGE_CENSUS_SEMANTICS,
        "field_semantics": _COVERAGE_CENSUS_FIELD_SEMANTICS,
        "catalog_status": report["status"],
        "catalog_issue_summary": _coverage_census_issue_summary(report),
        "expected_packet_count": report["expected_packet_count"],
        "indexed_packet_count": report["indexed_packet_count"],
        "attachment_record_count": report["attachment_record_count"],
        "indexed_attachment_record_count": report["indexed_attachment_record_count"],
        "source_family_count": sum(
            1 for row in source_families if row["source_family"] is not None
        ),
        "unknown_source_family_packet_count": (
            unknown_source_family["packet_count"] if unknown_source_family else 0
        ),
        "unknown_source_family_attachment_record_count": (
            unknown_source_family["attachment_record_count"]
            if unknown_source_family
            else 0
        ),
        "source_surface_count": report["source_surface_count"],
        "source_families": source_families,
        "source_surfaces": source_surfaces,
        "stable_query_paths": {
            "all_packets": "all_packets.jsonl",
            "source_surfaces": "source_surfaces.json",
            "attachment_records_root": "attachment_records/",
            "by_packet_root": "by_packet/",
        },
        "catalog_root": report["catalog_root"],
    }


def source_surface_catalog_rows(
    root: DataLakeRoot,
    *,
    source_family: str,
    source_surface: str,
    inspection_report: dict[str, Any] | None = None,
    inspection_cache: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Read generated Bronze packet and AR query rows for one source surface.

    The helper intentionally resolves the generated paths from the catalog's own
    source-surface summary so downstream lanes do not reimplement private safe-name
    rules or guess filesystem layout.
    """
    family = string_or_none(source_family)
    surface = string_or_none(source_surface)
    if family is None or surface is None:
        raise DataLakeRootError("source_family and source_surface must be non-blank strings")
    report = inspection_report
    if report is None and inspection_cache is not None:
        report = inspection_cache.get("bronze_catalog_inspection_report")
    if report is None:
        report = inspect_catalog(root)
        if inspection_cache is not None:
            inspection_cache["bronze_catalog_inspection_report"] = report
    if report["status"] != "ok":
        raise DataLakeRootError(
            "Bronze catalog is not current; run run_data_lake_catalog.py --rebuild "
            "before source-surface downstream consumption"
        )
    surface_row = next(
        (
            row
            for row in report["source_surfaces"]
            if row.get("source_family") == family and row.get("source_surface") == surface
        ),
        None,
    )
    if surface_row is None:
        return {
            "source_family": family,
            "source_surface": surface,
            "catalog_query_paths": {},
            "packet_rows": [],
            "attachment_record_query_rows": [],
            "attachment_record_rows": [],
        }
    packet_rows = [
        row
        for row in _read_catalog_jsonl(root, surface_row.get("by_source_surface_path"))
        if row.get("source_family") == family and row.get("source_surface") == surface
    ]
    attachment_record_query_rows = [
        row
        for row in _read_catalog_jsonl(root, surface_row.get("attachment_records_path"))
        if row.get("source_family") == family and row.get("source_surface") == surface
    ]
    attachment_record_rows = [
        _read_attachment_record_catalog_entry(root, row)
        for row in attachment_record_query_rows
    ]
    return {
        "source_family": family,
        "source_surface": surface,
        "catalog_query_paths": {
            "by_source_surface": surface_row.get("by_source_surface_path"),
            "attachment_records_by_source_surface": surface_row.get("attachment_records_path"),
        },
        "packet_rows": packet_rows,
        "attachment_record_query_rows": attachment_record_query_rows,
        "attachment_record_rows": attachment_record_rows,
    }


def _build_entries(root: DataLakeRoot) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for packet_id in _iter_committed_packet_ids(root):
        loaded = root.load_raw_packet(packet_id)
        manifest = loaded.manifest
        extractor_registered = _extractor_key(manifest) in _EXTRACTORS
        facets = [
            *_universal_facets(manifest),
            *_extractor_facets(manifest, loaded.bodies),
        ]
        container = loaded.container
        manifest_path = container / "manifest.json"
        entry = {
            "catalog_version": BRONZE_CATALOG_VERSION,
            "catalog_schema_version": BRONZE_CATALOG_SCHEMA_VERSION,
            "packet_id": packet_id,
            "raw_path": _rel(root, container),
            "manifest_relpath": _rel(root, manifest_path),
            "manifest_sha256": hash_file(manifest_path),
            "source_family": string_or_none(manifest.get("source_family")),
            "source_surface": string_or_none(manifest.get("source_surface")),
            "source_locator": _visible_fact_value(manifest.get("source_locator")),
            "facet_extractor": "registered" if extractor_registered else "universal_only",
            "session_identity": string_or_none(manifest.get("session_identity")),
            "capture_time": _visible_fact_value(
                (manifest.get("timing") or {}).get("capture_time")
                if isinstance(manifest.get("timing"), dict)
                else None
            ),
            "series_id": string_or_none(manifest.get("series_id")),
            "source_slice_count": _list_len(manifest.get("source_slices")),
            "preserved_file_count": _list_len(manifest.get("preserved_files")),
            "facets": sorted((facet.to_dict() for facet in facets), key=_facet_sort_key),
        }
        packet_attachment_records = _packet_attachment_records(entry, manifest, loaded.bodies)
        entry["attachment_record_count"] = len(packet_attachment_records)
        entry["attachment_record_ids"] = [
            record["attachment_record_id"] for record in packet_attachment_records
        ]
        entry["_attachment_records"] = packet_attachment_records
        entries.append(entry)
    return sorted(entries, key=lambda item: item["packet_id"])


def _coverage_census_surface_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_family": row.get("source_family"),
        "source_surface": row.get("source_surface"),
        "packet_count": row.get("packet_count", 0),
        "attachment_record_count": row.get("attachment_record_count", 0),
        "facet_extractor": row.get("facet_extractor"),
        "facet_namespaces": row.get("facet_namespaces", []),
        "coverage_basis": "verified_raw_packet_manifests",
        "catalog_query_paths": {
            "by_source_surface": row.get("by_source_surface_path"),
            "attachment_records_by_source_surface": row.get("attachment_records_path"),
        },
    }


def _coverage_census_source_families(
    source_surfaces: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    buckets: dict[str | None, dict[str, Any]] = {}
    for row in source_surfaces:
        source_family = string_or_none(row.get("source_family"))
        bucket = buckets.setdefault(
            source_family,
            {
                "source_family": source_family,
                "packet_count": 0,
                "attachment_record_count": 0,
                "source_surface_count": 0,
                "registered_surface_count": 0,
                "universal_only_surface_count": 0,
            },
        )
        bucket["packet_count"] += row.get("packet_count", 0)
        bucket["attachment_record_count"] += row.get("attachment_record_count", 0)
        bucket["source_surface_count"] += 1
        if row.get("facet_extractor") == "registered":
            bucket["registered_surface_count"] += 1
        else:
            bucket["universal_only_surface_count"] += 1
    return [
        bucket
        for _, bucket in sorted(buckets.items(), key=lambda item: item[0] or "")
    ]


def _coverage_census_issue_summary(report: dict[str, Any]) -> dict[str, Any]:
    issue_fields = (
        "missing_packets",
        "orphaned_packets",
        "stale_packets",
        "catalog_read_failures",
        "missing_files",
        "orphaned_files",
        "stale_files",
    )
    issue_counts = {field: len(report[field]) for field in issue_fields}
    issue_samples = {
        field: report[field][:_COVERAGE_CENSUS_ISSUE_SAMPLE_LIMIT]
        for field in issue_fields
        if report[field]
    }
    return {
        "issue_counts": issue_counts,
        "issue_samples": issue_samples,
        "issue_sample_limit": _COVERAGE_CENSUS_ISSUE_SAMPLE_LIMIT,
        "full_issue_report": "run run_data_lake_catalog.py without --census for full issue lists",
    }


def _indexed_attachment_record_count(body: bytes | None) -> int:
    if body is None:
        return 0
    try:
        lines = body.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        return 0
    count = 0
    for line in lines:
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except ValueError:
            continue
        if isinstance(payload, dict) and isinstance(payload.get("attachment_record_id"), str):
            count += 1
    return count


def _read_catalog_jsonl(root: DataLakeRoot, relative_path: object) -> list[dict[str, Any]]:
    if relative_path is None:
        return []
    path = _catalog_generated_path(root, relative_path)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise DataLakeRootError(f"cannot read Bronze catalog query file {path}: {exc}") from exc
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError as exc:
            raise DataLakeRootError(
                f"invalid JSONL row in Bronze catalog query file {path} line {line_number}: {exc}"
            ) from exc
        if not isinstance(row, dict):
            raise DataLakeRootError(
                f"invalid Bronze catalog query row in {path} line {line_number}: expected object"
            )
        rows.append(row)
    return rows


def _read_attachment_record_catalog_entry(
    root: DataLakeRoot, query_row: dict[str, Any]
) -> dict[str, Any]:
    record_id = string_or_none(query_row.get("attachment_record_id"))
    if record_id is None or "/" in record_id or "\\" in record_id:
        raise DataLakeRootError("Bronze attachment query row has unsafe attachment_record_id")
    return _read_catalog_json(
        root,
        f"attachment_records/by_attachment_record/{record_id}.json",
    )


def _read_catalog_json(root: DataLakeRoot, relative_path: object) -> dict[str, Any]:
    path = _catalog_generated_path(root, relative_path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise DataLakeRootError(f"cannot read Bronze catalog JSON file {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise DataLakeRootError(f"invalid Bronze catalog JSON file {path}: expected object")
    return payload


def _catalog_generated_path(root: DataLakeRoot, relative_path: object) -> Path:
    if not isinstance(relative_path, str) or not relative_path:
        raise DataLakeRootError("Bronze catalog query path must be a non-blank string")
    rel = PurePosixPath(relative_path)
    if rel.is_absolute() or any(part in {"", ".", ".."} for part in rel.parts):
        raise DataLakeRootError(f"unsafe Bronze catalog query path: {relative_path!r}")
    catalog_root = _catalog_root(root)
    path = catalog_root.joinpath(*rel.parts)
    try:
        path.resolve().relative_to(catalog_root.resolve())
    except ValueError as exc:
        raise DataLakeRootError(f"Bronze catalog query path escapes catalog root: {relative_path!r}") from exc
    return path


def _iter_committed_packet_ids(root: DataLakeRoot) -> list[str]:
    raw_dir = root.path / "raw"
    if not raw_dir.is_dir():
        return []
    tombstoned = root.tombstoned_packet_ids()
    packet_ids: list[str] = []
    for shard_dir in sorted(raw_dir.iterdir()):
        if not shard_dir.is_dir():
            continue
        for container in sorted(shard_dir.iterdir()):
            if (
                container.is_dir()
                and _PACKET_ID_RE.fullmatch(container.name)
                and shard_dir.name == raw_shard(container.name)
                and (container / "manifest.json").is_file()
                and container.name not in tombstoned
            ):
                packet_ids.append(container.name)
    return packet_ids


def _catalog_snapshot(
    entries: list[dict[str, Any]],
    source_surfaces: list[dict[str, Any]],
    attachment_records: list[dict[str, Any]],
) -> dict[str, bytes]:
    snapshot: dict[str, bytes] = {}
    by_source_family: dict[str, list[dict[str, Any]]] = {}
    by_source_surface: dict[str, list[dict[str, Any]]] = {}
    by_session: dict[str, list[dict[str, Any]]] = {}
    by_locator_sha: dict[str, list[dict[str, Any]]] = {}
    by_series: dict[str, list[dict[str, Any]]] = {}
    by_facet: dict[tuple[str, str, str], list[dict[str, Any]]] = {}

    for entry in entries:
        snapshot[f"by_packet/{entry['packet_id']}.json"] = _json_bytes(
            _packet_index_entry(entry)
        )
        row = _query_row(entry)
        _bucket(by_source_family, entry.get("source_family"), row)
        _bucket(by_source_surface, entry.get("source_surface"), row)
        _bucket(by_session, entry.get("session_identity"), row)
        _bucket(by_series, entry.get("series_id"), row)
        locator = entry.get("source_locator")
        if isinstance(locator, str) and locator:
            _bucket(by_locator_sha, hashlib.sha256(locator.encode("utf-8")).hexdigest(), row)
        for facet in entry["facets"]:
            key = (facet["facet_type"], facet["namespace"], facet["value"])
            by_facet.setdefault(key, []).append(row | {"facet": facet})

    snapshot["all_packets.jsonl"] = _jsonl_bytes(_query_row(entry) for entry in entries)
    snapshot["source_surfaces.json"] = _json_bytes(
        {
            "authority": _CATALOG_AUTHORITY,
            "catalog_version": BRONZE_CATALOG_VERSION,
            "catalog_schema_version": BRONZE_CATALOG_SCHEMA_VERSION,
            "bronze_baseline_status": BRONZE_BASELINE_STATUS,
            "bronze_baseline_semantics": BRONZE_BASELINE_SEMANTICS,
            "completeness": _SOURCE_SURFACE_COMPLETENESS,
            "field_semantics": _SOURCE_SURFACE_FIELD_SEMANTICS,
            "stable_query_paths": {
                "all_packets": "all_packets.jsonl",
                "attachment_records_root": "attachment_records/",
                "by_packet_root": "by_packet/",
                "by_source_surface_path_field": "source_surfaces[].by_source_surface_path",
                "attachment_records_path_field": "source_surfaces[].attachment_records_path",
            },
            "source_surface_count": len(source_surfaces),
            "source_surfaces": source_surfaces,
        }
    )
    snapshot.update(_attachment_record_snapshot(attachment_records))
    snapshot.update(_bucket_jsonl_snapshot("by_source_family", by_source_family))
    snapshot.update(_bucket_jsonl_snapshot("by_source_surface", by_source_surface))
    snapshot.update(_bucket_jsonl_snapshot("by_session_identity", by_session))
    snapshot.update(_bucket_jsonl_snapshot("by_locator_sha256", by_locator_sha))
    snapshot.update(_bucket_jsonl_snapshot("by_series", by_series))
    for (facet_type, namespace, value), rows in sorted(by_facet.items()):
        path = (
            "by_facet/"
            f"{_safe_name(facet_type)}/"
            f"{_safe_name(namespace)}/"
            f"{_safe_name(value)}.jsonl"
        )
        snapshot[path] = _jsonl_bytes(
            sorted(rows, key=lambda item: (item["packet_id"], item["facet"]["role"]))
        )
    snapshot["manifest.json"] = _json_bytes(
        {
            "authority": _CATALOG_AUTHORITY,
            "catalog_version": BRONZE_CATALOG_VERSION,
            "catalog_schema_version": BRONZE_CATALOG_SCHEMA_VERSION,
            "bronze_baseline_status": BRONZE_BASELINE_STATUS,
            "bronze_baseline_semantics": BRONZE_BASELINE_SEMANTICS,
            "packet_count": len(entries),
            "attachment_record_count": len(attachment_records),
        }
    )
    return snapshot


def _source_surface_summary(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[tuple[str | None, str | None], dict[str, Any]] = {}
    for entry in entries:
        key = (entry.get("source_family"), entry.get("source_surface"))
        bucket = buckets.setdefault(
            key,
            {
                "source_family": key[0],
                "source_surface": key[1],
                "by_source_surface_path": _source_surface_bucket_path(key[1]),
                "packet_count": 0,
                "attachment_record_count": 0,
                "facet_extractor": "universal_only",
                "facet_namespaces": set(),
            },
        )
        bucket["packet_count"] += 1
        bucket["attachment_record_count"] += entry.get("attachment_record_count", 0)
        if entry.get("facet_extractor") == "registered":
            bucket["facet_extractor"] = "registered"
        for facet in entry.get("facets", []):
            namespace = facet.get("namespace") if isinstance(facet, dict) else None
            if isinstance(namespace, str) and namespace:
                bucket["facet_namespaces"].add(namespace)
    return [
        {
            "source_family": bucket["source_family"],
            "source_surface": bucket["source_surface"],
            "by_source_surface_path": bucket["by_source_surface_path"],
            "attachment_records_path": _attachment_records_source_surface_path(
                bucket["source_surface"]
            )
            if bucket["attachment_record_count"]
            else None,
            "packet_count": bucket["packet_count"],
            "attachment_record_count": bucket["attachment_record_count"],
            "facet_extractor": bucket["facet_extractor"],
            "facet_namespaces": sorted(bucket["facet_namespaces"]),
        }
        for _, bucket in sorted(
            buckets.items(), key=lambda item: (item[0][0] or "", item[0][1] or "")
        )
    ]


def _source_surface_bucket_path(source_surface: object) -> str | None:
    if isinstance(source_surface, str) and source_surface:
        return f"by_source_surface/{_safe_name(source_surface)}.jsonl"
    return None


def _attachment_records_source_surface_path(source_surface: object) -> str | None:
    if isinstance(source_surface, str) and source_surface:
        return f"attachment_records/by_source_surface/{_safe_name(source_surface)}.jsonl"
    return None


def _attachment_records(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = [
        record
        for entry in entries
        for record in entry.get("_attachment_records", [])
        if isinstance(record, dict)
    ]
    return sorted(records, key=lambda item: item["attachment_record_id"])


def _packet_index_entry(entry: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in entry.items() if not key.startswith("_")}


def _packet_attachment_records(
    entry: dict[str, Any], manifest: dict[str, Any], bodies: dict[str, bytes]
) -> list[dict[str, Any]]:
    """Materialize catalog AR rows: canonical entries from the pinned A2
    serializer plus catalog-only decorations. The canonical part is owned by
    ``data_lake.attachment_record_entry``; this wrapper adds only generated
    read-state fields (authority note, catalog versions, query paths)."""
    canonical_entries = derive_attachment_record_entries(
        packet_id=entry["packet_id"],
        raw_path=entry["raw_path"],
        manifest_relpath=entry["manifest_relpath"],
        manifest_sha256=entry["manifest_sha256"],
        manifest=manifest,
        bodies=bodies,
    )
    records: list[dict[str, Any]] = []
    for canonical in canonical_entries:
        record = dict(canonical)
        record["authority"] = _CATALOG_AUTHORITY
        record["catalog_version"] = BRONZE_CATALOG_VERSION
        record["catalog_schema_version"] = BRONZE_CATALOG_SCHEMA_VERSION
        replay_version_pins = dict(record["replay_version_pins"])
        replay_version_pins["catalog_schema_version"] = BRONZE_CATALOG_SCHEMA_VERSION
        record["replay_version_pins"] = replay_version_pins
        record["stable_query_paths"] = {
            "by_attachment_record": (
                f"attachment_records/by_attachment_record/{record['attachment_record_id']}.json"
            ),
            "by_packet": (
                f"attachment_records/by_packet/{_safe_name(entry['packet_id'])}.jsonl"
            ),
        }
        records.append(record)
    return records


def _require_supported_attachment_record_body_ref_kind(body_ref_kind: str) -> None:
    if body_ref_kind not in _SUPPORTED_ATTACHMENT_RECORD_BODY_REF_KINDS:
        allowed_list = ", ".join(sorted(_SUPPORTED_ATTACHMENT_RECORD_BODY_REF_KINDS))
        raise DataLakeRootError(
            f"unsupported attachment body_ref_kind {body_ref_kind!r}; expected one of "
            f"{{{allowed_list}}}"
        )


# Owned by the pinned A2 serializer; kept under the private catalog names for
# the reader-side checks in load_attachment_record_body and existing importers.
_require_supported_attachment_record_hash_basis = require_supported_hash_basis
_attachment_record_id = attachment_record_id


def _universal_facets(manifest: dict[str, Any]) -> list[CatalogFacet]:
    facets: list[CatalogFacet] = []
    for facet_type, namespace, field in (
        ("source_family", "source_family", "source_family"),
        ("source_surface", "source_surface", "source_surface"),
        ("session_identity", "session_identity", "session_identity"),
        ("series", "series_id", "series_id"),
    ):
        value = string_or_none(manifest.get(field))
        if value:
            facets.append(
                CatalogFacet(
                    facet_type=facet_type,
                    namespace=namespace,
                    value=value,
                    role="packet",
                    source=f"manifest.{field}",
                )
            )
    locator = _visible_fact_value(manifest.get("source_locator"))
    if locator:
        facets.append(
            CatalogFacet(
                facet_type="locator",
                namespace="source_locator_sha256",
                value=hashlib.sha256(locator.encode("utf-8")).hexdigest(),
                role="packet",
                source="manifest.source_locator",
            )
        )
    return facets


def _extractor_facets(manifest: dict[str, Any], bodies: dict[str, bytes]) -> list[CatalogFacet]:
    extractor = _EXTRACTORS.get(_extractor_key(manifest))
    return list(extractor(manifest, bodies)) if extractor is not None else []


def _extractor_key(manifest: dict[str, Any]) -> tuple[str | None, str | None]:
    return (
        string_or_none(manifest.get("source_family")),
        string_or_none(manifest.get("source_surface")),
    )


def _ig_reels_grid_facets(_manifest: dict[str, Any], bodies: dict[str, bytes]) -> list[CatalogFacet]:
    payload = _first_json_body(bodies, "ig_reels_grid_capture.json")
    if not isinstance(payload, dict):
        return []
    facets: list[CatalogFacet] = []
    snapshot = payload.get("creator_profile_snapshot")
    if isinstance(snapshot, dict):
        handle = string_or_none(snapshot.get("source_profile"))
        if handle:
            facets.append(
                CatalogFacet(
                    facet_type="entity",
                    namespace="instagram_creator_handle",
                    value=handle.lower().lstrip("@"),
                    role="publisher",
                    source="ig_reels_grid.creator_profile_snapshot.source_profile",
                    json_pointer="/creator_profile_snapshot/source_profile",
                )
            )
        numeric_id = string_or_none(snapshot.get("numeric_id"))
        if numeric_id:
            facets.append(
                CatalogFacet(
                    facet_type="entity",
                    namespace="instagram_creator_numeric_id",
                    value=numeric_id,
                    role="publisher",
                    source="ig_reels_grid.creator_profile_snapshot.numeric_id",
                    json_pointer="/creator_profile_snapshot/numeric_id",
                )
            )
    joined_rows = payload.get("joined_rows")
    if isinstance(joined_rows, list):
        for index, joined in enumerate(joined_rows):
            if not isinstance(joined, dict):
                continue
            dom_row = joined.get("dom_row")
            if not isinstance(dom_row, dict):
                continue
            shortcode = string_or_none(dom_row.get("shortcode"))
            if shortcode:
                facets.append(
                    CatalogFacet(
                        facet_type="content",
                        namespace="instagram_shortcode",
                        value=shortcode,
                        role=string_or_none(dom_row.get("kind")) or "media",
                        source="ig_reels_grid.joined_rows.dom_row.shortcode",
                        json_pointer=f"/joined_rows/{index}/dom_row/shortcode",
                    )
                )
    return facets


_EXTRACTORS: dict[tuple[str | None, str | None], FacetExtractor] = {
    ("instagram_creator", "ig_reels_grid_dom_passive_json"): _ig_reels_grid_facets,
}


def _first_json_body(bodies: dict[str, bytes], suffix: str) -> object | None:
    for file_id in sorted(bodies):
        try:
            text = bodies[file_id].decode("utf-8")
        except UnicodeDecodeError:
            continue
        try:
            payload = json.loads(text)
        except ValueError:
            continue
        if isinstance(payload, dict) and _payload_looks_like(payload, suffix):
            return payload
    return None


def _payload_looks_like(payload: dict[str, Any], suffix: str) -> bool:
    if suffix == "ig_reels_grid_capture.json":
        return "creator_profile_snapshot" in payload and "joined_rows" in payload
    return False


def _query_row(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "packet_id": entry["packet_id"],
        "raw_path": entry["raw_path"],
        "manifest_relpath": entry["manifest_relpath"],
        "manifest_sha256": entry["manifest_sha256"],
        "source_family": entry.get("source_family"),
        "source_surface": entry.get("source_surface"),
        "session_identity": entry.get("session_identity"),
        "capture_time": entry.get("capture_time"),
        "attachment_record_count": entry.get("attachment_record_count", 0),
    }


def _attachment_record_snapshot(attachment_records: list[dict[str, Any]]) -> dict[str, bytes]:
    snapshot: dict[str, bytes] = {}
    by_packet: dict[str, list[dict[str, Any]]] = {}
    by_source_family: dict[str, list[dict[str, Any]]] = {}
    by_source_surface: dict[str, list[dict[str, Any]]] = {}
    by_payload_kind: dict[str, list[dict[str, Any]]] = {}
    by_body_sha256: dict[str, list[dict[str, Any]]] = {}

    for record in attachment_records:
        record_id = record["attachment_record_id"]
        snapshot[f"attachment_records/by_attachment_record/{record_id}.json"] = _json_bytes(record)
        row = _attachment_query_row(record)
        _bucket(by_packet, record.get("packet_id"), row)
        _bucket(by_source_family, record.get("source_family"), row)
        _bucket(by_source_surface, record.get("source_surface"), row)
        _bucket(by_payload_kind, record.get("payload_kind"), row)
        _bucket(by_body_sha256, record.get("body_sha256"), row)

    snapshot["attachment_records/all_attachment_records.jsonl"] = _jsonl_bytes(attachment_records)
    snapshot["attachment_records/manifest.json"] = _json_bytes(
        {
            "authority": _CATALOG_AUTHORITY,
            "catalog_version": BRONZE_CATALOG_VERSION,
            "catalog_schema_version": BRONZE_CATALOG_SCHEMA_VERSION,
            "bronze_baseline_status": BRONZE_BASELINE_STATUS,
            "bronze_baseline_semantics": BRONZE_BASELINE_SEMANTICS,
            "attachment_record_schema_version": BRONZE_ATTACHMENT_RECORD_SCHEMA_VERSION,
            "attachment_record_physicalization": BRONZE_ATTACHMENT_RECORD_PHYSICALIZATION,
            "attachment_record_count": len(attachment_records),
            "completeness": _ATTACHMENT_RECORD_COMPLETENESS,
            "field_semantics": _ATTACHMENT_RECORD_FIELD_SEMANTICS,
            "stable_query_paths": {
                "all_attachment_records": "attachment_records/all_attachment_records.jsonl",
                "by_attachment_record_root": "attachment_records/by_attachment_record/",
                "by_packet_root": "attachment_records/by_packet/",
                "by_source_family_root": "attachment_records/by_source_family/",
                "by_source_surface_root": "attachment_records/by_source_surface/",
                "by_payload_kind_root": "attachment_records/by_payload_kind/",
                "by_body_sha256_root": "attachment_records/by_body_sha256/",
            },
        }
    )
    snapshot.update(_bucket_jsonl_snapshot("attachment_records/by_packet", by_packet))
    snapshot.update(
        _bucket_jsonl_snapshot("attachment_records/by_source_family", by_source_family)
    )
    snapshot.update(
        _bucket_jsonl_snapshot("attachment_records/by_source_surface", by_source_surface)
    )
    snapshot.update(
        _bucket_jsonl_snapshot("attachment_records/by_payload_kind", by_payload_kind)
    )
    snapshot.update(
        _bucket_jsonl_snapshot("attachment_records/by_body_sha256", by_body_sha256)
    )
    return snapshot


def _attachment_query_row(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "attachment_record_id": record["attachment_record_id"],
        "attachment_record_physicalization": record["attachment_record_physicalization"],
        "packet_id": record["packet_id"],
        "source_family": record.get("source_family"),
        "source_surface": record.get("source_surface"),
        "file_id": record["file_id"],
        "relative_packet_path": record["relative_packet_path"],
        "body_sha256": record["body_sha256"],
        "hash_basis": record["hash_basis"],
        "payload_kind": record["payload_kind"],
        "source_slice_ids": record.get("source_slice_ids", []),
    }


def load_attachment_record_body(
    root: DataLakeRoot,
    attachment_record: dict[str, Any],
    *,
    loaded_packet: Any | None = None,
) -> bytes:
    """Resolve and verify the raw body referenced by a generated Attachment Record."""
    packet_id = required_string(attachment_record.get("packet_id"), "packet_id")
    file_id = required_string(attachment_record.get("file_id"), "file_id")
    relative_packet_path = required_string(
        attachment_record.get("relative_packet_path"), "relative_packet_path"
    )
    expected_sha256 = required_string(attachment_record.get("body_sha256"), "body_sha256")
    expected_hash_basis = required_string(attachment_record.get("hash_basis"), "hash_basis")
    expected_body_ref_kind = required_string(
        attachment_record.get("body_ref_kind"), "body_ref_kind"
    )
    _require_supported_attachment_record_body_ref_kind(expected_body_ref_kind)
    _require_supported_attachment_record_hash_basis(expected_hash_basis, file_id=file_id)
    body_ref = attachment_record.get("body_ref")
    if body_ref is not None:
        if not isinstance(body_ref, dict):
            raise DataLakeRootError("Attachment Record body_ref must be an object when present")
        expected_body_ref = {
            "kind": expected_body_ref_kind,
            "packet_id": packet_id,
            "file_id": file_id,
            "relative_packet_path": relative_packet_path,
            "body_sha256": expected_sha256,
            "hash_basis": expected_hash_basis,
        }
        for key, expected_value in expected_body_ref.items():
            if body_ref.get(key) != expected_value:
                raise DataLakeRootError(
                    f"Attachment Record body_ref mismatch for {file_id!r}: {key}"
                )
    loaded = loaded_packet or root.load_raw_packet(packet_id)
    preserved = _preserved_file_by_id(loaded.manifest, file_id)
    if preserved.get("relative_packet_path") != relative_packet_path:
        raise DataLakeRootError(
            f"Attachment Record path mismatch for {file_id!r}: "
            f"{relative_packet_path!r} != {preserved.get('relative_packet_path')!r}"
        )
    if preserved.get("sha256") != expected_sha256:
        raise DataLakeRootError(
            f"Attachment Record sha256 mismatch for {file_id!r}: "
            f"{expected_sha256!r} != {preserved.get('sha256')!r}"
        )
    body = loaded.bodies.get(file_id)
    if body is None:
        raise DataLakeRootError(f"preserved body {file_id!r} missing after verified load")
    actual_sha256 = hashlib.sha256(body).hexdigest()
    if actual_sha256 != expected_sha256:
        raise DataLakeRootError(
            f"Attachment Record body sha256 mismatch for {file_id!r}: "
            f"{actual_sha256!r} != {expected_sha256!r}"
        )
    return body


def _preserved_file_by_id(manifest: dict[str, Any], file_id: str) -> dict[str, Any]:
    preserved_files = manifest.get("preserved_files")
    if not isinstance(preserved_files, list):
        raise DataLakeRootError("raw manifest preserved_files must be a list")
    for preserved in preserved_files:
        if isinstance(preserved, dict) and preserved.get("file_id") == file_id:
            return preserved
    raise DataLakeRootError(f"raw manifest does not contain preserved file_id {file_id!r}")

def _bucket(target: dict[str, list[dict[str, Any]]], key: object, row: dict[str, Any]) -> None:
    if isinstance(key, str) and key:
        target.setdefault(key, []).append(row)


def _bucket_jsonl_snapshot(
    root: str, buckets: dict[str, list[dict[str, Any]]]
) -> dict[str, bytes]:
    snapshot: dict[str, bytes] = {}
    for key, rows in sorted(buckets.items()):
        snapshot[f"{root}/{_safe_name(key)}.jsonl"] = _jsonl_bytes(
            sorted(rows, key=lambda item: item["packet_id"])
        )
    return snapshot


def _write_snapshot(root: Path, snapshot: dict[str, bytes]) -> None:
    for relpath, body in sorted(snapshot.items()):
        path = root / Path(relpath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)


def _read_snapshot(
    root: DataLakeRoot, catalog_root: Path
) -> tuple[dict[str, bytes], list[dict[str, str]]]:
    if not catalog_root.is_dir():
        return {}, []
    snapshot: dict[str, bytes] = {}
    read_failures: list[dict[str, str]] = []
    for path in sorted(catalog_root.rglob("*")):
        if not path.is_file():
            continue
        relpath = path.relative_to(catalog_root).as_posix()
        try:
            snapshot[relpath] = path.read_bytes()
        except OSError as exc:
            read_failures.append({"path": _rel(root, path), "error": str(exc)})
    return snapshot, read_failures


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _jsonl_bytes(rows: Iterable[dict[str, Any]]) -> bytes:
    return "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows).encode("utf-8")


def _catalog_root(root: DataLakeRoot) -> Path:
    return root._within(*CATALOG_RELATIVE_ROOT)


def _rel(root: DataLakeRoot, path: Path) -> str:
    return path.relative_to(root.path).as_posix()


def _safe_name(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    cleaned = "".join(
        ch.lower() if ch.isascii() and ch.isalnum() else "_" for ch in value.strip()
    )
    cleaned = "_".join(part for part in cleaned.split("_") if part)
    return f"{cleaned[:64] or 'blank'}__{digest}"


# Owned by the pinned A2 serializer (same known-status extraction rule).
_visible_fact_value = visible_fact_value


def _list_len(value: object) -> int:
    return len(value) if isinstance(value, list) else 0


def _facet_sort_key(facet: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        facet.get("facet_type", ""),
        facet.get("namespace", ""),
        facet.get("value", ""),
        facet.get("role", ""),
    )


__all__ = [
    "BRONZE_ATTACHMENT_RECORD_PHYSICALIZATION",
    "BRONZE_ATTACHMENT_RECORD_SCHEMA_VERSION",
    "BRONZE_BASELINE_SEMANTICS",
    "BRONZE_BASELINE_STATUS",
    "BRONZE_CATALOG_SCHEMA_VERSION",
    "BRONZE_CATALOG_VERSION",
    "CATALOG_RELATIVE_ROOT",
    "CatalogFacet",
    "catalog_coverage_census",
    "inspect_catalog",
    "load_attachment_record_body",
    "rebuild_catalog",
    "source_surface_catalog_rows",
]
