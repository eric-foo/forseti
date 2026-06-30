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
from pathlib import Path
from typing import Any, Callable, Iterable

from data_lake.root import DataLakeRoot, raw_shard
from harness_utils import hash_file

BRONZE_CATALOG_VERSION = "bronze_catalog_v0"
BRONZE_CATALOG_SCHEMA_VERSION = "bronze_catalog_v0_schema_1"
CATALOG_RELATIVE_ROOT = ("indexes", "derived_retrieval", "bronze_catalog", "v0")
_PACKET_ID_RE = re.compile(r"[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{26}")
_CATALOG_AUTHORITY = "generated_from_raw_packet_manifests; raw remains authoritative"
_SOURCE_SURFACE_COMPLETENESS = (
    "observed_source_surface_coverage_only; not capture_support, silver_readiness, "
    "projection_coverage, source_family_completeness, or validation"
)
_SOURCE_SURFACE_FIELD_SEMANTICS = {
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
    source_surfaces = _source_surface_summary(entries)
    snapshot = _catalog_snapshot(entries, source_surfaces)
    root._reverify()
    catalog_root = _catalog_root(root)
    if catalog_root.exists():
        shutil.rmtree(catalog_root)
    _write_snapshot(catalog_root, snapshot)
    return {
        "status": "rebuilt",
        "catalog_version": BRONZE_CATALOG_VERSION,
        "catalog_schema_version": BRONZE_CATALOG_SCHEMA_VERSION,
        "packet_count": len(entries),
        "source_surface_count": len(source_surfaces),
        "source_surfaces": source_surfaces,
        "file_count": len(snapshot),
        "catalog_root": _rel(root, catalog_root),
    }


def inspect_catalog(root: DataLakeRoot) -> dict[str, Any]:
    """Compare generated catalog files to the raw-derived expected catalog."""
    expected = _build_entries(root)
    source_surfaces = _source_surface_summary(expected)
    expected_snapshot = _catalog_snapshot(expected, source_surfaces)
    catalog_root = _catalog_root(root)
    actual_snapshot, read_failures = _read_snapshot(root, catalog_root)
    missing_files = sorted(set(expected_snapshot) - set(actual_snapshot))
    orphaned_files = sorted(set(actual_snapshot) - set(expected_snapshot))
    stale_files = sorted(
        path
        for path in set(expected_snapshot) & set(actual_snapshot)
        if actual_snapshot[path] != expected_snapshot[path]
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

    expected_by_packet = {entry["packet_id"]: entry for entry in expected}
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
        "expected_packet_count": len(expected),
        "indexed_packet_count": len(existing),
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
        entries.append(
            {
                "catalog_version": BRONZE_CATALOG_VERSION,
                "catalog_schema_version": BRONZE_CATALOG_SCHEMA_VERSION,
                "packet_id": packet_id,
                "raw_path": _rel(root, container),
                "manifest_relpath": _rel(root, manifest_path),
                "manifest_sha256": hash_file(manifest_path),
                "source_family": _string_or_none(manifest.get("source_family")),
                "source_surface": _string_or_none(manifest.get("source_surface")),
                "source_locator": _visible_fact_value(manifest.get("source_locator")),
                "facet_extractor": "registered" if extractor_registered else "universal_only",
                "session_identity": _string_or_none(manifest.get("session_identity")),
                "capture_time": _visible_fact_value(
                    (manifest.get("timing") or {}).get("capture_time")
                    if isinstance(manifest.get("timing"), dict)
                    else None
                ),
                "series_id": _string_or_none(manifest.get("series_id")),
                "source_slice_count": _list_len(manifest.get("source_slices")),
                "preserved_file_count": _list_len(manifest.get("preserved_files")),
                "facets": sorted((facet.to_dict() for facet in facets), key=_facet_sort_key),
            }
        )
    return sorted(entries, key=lambda item: item["packet_id"])


def _iter_committed_packet_ids(root: DataLakeRoot) -> list[str]:
    raw_dir = root.path / "raw"
    if not raw_dir.is_dir():
        return []
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
            ):
                packet_ids.append(container.name)
    return packet_ids


def _catalog_snapshot(
    entries: list[dict[str, Any]], source_surfaces: list[dict[str, Any]]
) -> dict[str, bytes]:
    snapshot: dict[str, bytes] = {}
    by_source_family: dict[str, list[dict[str, Any]]] = {}
    by_source_surface: dict[str, list[dict[str, Any]]] = {}
    by_session: dict[str, list[dict[str, Any]]] = {}
    by_locator_sha: dict[str, list[dict[str, Any]]] = {}
    by_series: dict[str, list[dict[str, Any]]] = {}
    by_facet: dict[tuple[str, str, str], list[dict[str, Any]]] = {}

    for entry in entries:
        snapshot[f"by_packet/{entry['packet_id']}.json"] = _json_bytes(entry)
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
            "completeness": _SOURCE_SURFACE_COMPLETENESS,
            "field_semantics": _SOURCE_SURFACE_FIELD_SEMANTICS,
            "stable_query_paths": {
                "all_packets": "all_packets.jsonl",
                "by_packet_root": "by_packet/",
                "by_source_surface_path_field": "source_surfaces[].by_source_surface_path",
            },
            "source_surface_count": len(source_surfaces),
            "source_surfaces": source_surfaces,
        }
    )
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
            "packet_count": len(entries),
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
                "facet_extractor": "universal_only",
                "facet_namespaces": set(),
            },
        )
        bucket["packet_count"] += 1
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
            "packet_count": bucket["packet_count"],
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


def _universal_facets(manifest: dict[str, Any]) -> list[CatalogFacet]:
    facets: list[CatalogFacet] = []
    for facet_type, namespace, field in (
        ("source_family", "source_family", "source_family"),
        ("source_surface", "source_surface", "source_surface"),
        ("session_identity", "session_identity", "session_identity"),
        ("series", "series_id", "series_id"),
    ):
        value = _string_or_none(manifest.get(field))
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
        _string_or_none(manifest.get("source_family")),
        _string_or_none(manifest.get("source_surface")),
    )


def _ig_reels_grid_facets(_manifest: dict[str, Any], bodies: dict[str, bytes]) -> list[CatalogFacet]:
    payload = _first_json_body(bodies, "ig_reels_grid_capture.json")
    if not isinstance(payload, dict):
        return []
    facets: list[CatalogFacet] = []
    snapshot = payload.get("creator_profile_snapshot")
    if isinstance(snapshot, dict):
        handle = _string_or_none(snapshot.get("source_profile"))
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
        numeric_id = _string_or_none(snapshot.get("numeric_id"))
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
            shortcode = _string_or_none(dom_row.get("shortcode"))
            if shortcode:
                facets.append(
                    CatalogFacet(
                        facet_type="content",
                        namespace="instagram_shortcode",
                        value=shortcode,
                        role=_string_or_none(dom_row.get("kind")) or "media",
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
    }


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


def _visible_fact_value(value: object) -> str | None:
    if isinstance(value, dict) and value.get("status") == "known":
        return _string_or_none(value.get("value"))
    return None


def _string_or_none(value: object) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return None


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
    "BRONZE_CATALOG_SCHEMA_VERSION",
    "BRONZE_CATALOG_VERSION",
    "CATALOG_RELATIVE_ROOT",
    "CatalogFacet",
    "inspect_catalog",
    "rebuild_catalog",
]
