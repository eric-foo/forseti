"""Disposable incremental authority-verdict cache for the Silver lake map.

The cache changes only how ``derived_retrieval_views`` obtains a Silver source
authority verdict.  View bodies and manifests remain generated from committed
lake material and are byte-identical to a cold classification sweep.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from data_lake.canonical_json import canonical_record_bytes
from data_lake.creator_metric_lineage import OBSERVATION_LANE, ROLLUP_LANE
from data_lake.root import (
    EPOCH_MARKER_FILENAME,
    LEGACY_EPOCH_MARKER_FILENAME,
    LEGACY_ROOT_MARKER_FILENAME,
    ROOT_MARKER_FILENAME,
    raw_shard,
)
from data_lake.silver_record import SilverSourceAuthority
from harness_utils import sha256_bytes

CACHE_SCHEMA_VERSION = "derived_retrieval_classification_cache_v1"
CACHE_PARTS = (
    "indexes",
    "derived_retrieval",
    "silver_vault",
    "core",
    "cache",
    "classification_cache.json",
)
_CLASSIFIER_SOURCE_NAMES = (
    "silver_record.py",
    "silver_compatibility.py",
    "creator_metric_lineage.py",
)
_CREATOR_METRIC_LANES = frozenset({OBSERVATION_LANE, ROLLUP_LANE})


def _file_state(path: Path) -> dict[str, Any]:
    try:
        body = path.read_bytes()
    except OSError:
        return {"path": str(path), "status": "absent_or_unreadable"}
    return {
        "path": str(path),
        "status": "present",
        "sha256": sha256_bytes(body),
    }


def _path_stat_state(path: Path) -> dict[str, Any]:
    try:
        stat = path.stat()
    except OSError:
        return {"path": str(path), "status": "absent_or_unreadable"}
    return {
        "path": str(path),
        "status": "present",
        "size_bytes": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
    }


def classifier_version() -> str:
    module_dir = Path(__file__).resolve().parent
    rows = [
        {
            "name": name,
            "sha256": sha256_bytes((module_dir / name).read_bytes()),
        }
        for name in _CLASSIFIER_SOURCE_NAMES
    ]
    return f"sha256:{sha256_bytes(canonical_record_bytes(rows))}"


def _epoch_payload(root_path: Path) -> Mapping[str, Any]:
    for name in (EPOCH_MARKER_FILENAME, LEGACY_EPOCH_MARKER_FILENAME):
        path = root_path / name
        try:
            value = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError, TypeError):
            continue
        if isinstance(value, Mapping):
            return value
    return {}


def _declared_evidence_roots(root) -> tuple[Path, ...]:
    current = Path(root.path).resolve()
    legacy = _epoch_payload(current).get("legacy_roots")
    paths = [current]
    if isinstance(legacy, list):
        paths.extend(
            Path(value).resolve()
            for value in legacy
            if isinstance(value, str) and value.strip() and Path(value).is_absolute()
        )
    return tuple(paths)


def _lineage_state_fingerprint(root) -> str:
    rows: list[dict[str, Any]] = []
    for evidence_root in _declared_evidence_roots(root):
        try:
            root_stat = evidence_root.stat()
            directory_state: dict[str, Any] = {
                "status": "mounted",
                "mtime_ns": root_stat.st_mtime_ns,
            }
        except OSError:
            directory_state = {"status": "unmounted"}
        rows.append(
            {
                "root": str(evidence_root),
                "directory_state": directory_state,
                "root_markers": [
                    _file_state(evidence_root / ROOT_MARKER_FILENAME),
                    _file_state(evidence_root / LEGACY_ROOT_MARKER_FILENAME),
                ],
                "epoch_markers": [
                    _file_state(evidence_root / EPOCH_MARKER_FILENAME),
                    _file_state(evidence_root / LEGACY_EPOCH_MARKER_FILENAME),
                ],
            }
        )
    return sha256_bytes(canonical_record_bytes(rows))


def _packet_manifest_states(root, packet_id: Any, *, creator_metric: bool) -> list[dict[str, Any]]:
    if not isinstance(packet_id, str):
        return [{"packet_id": packet_id, "status": "invalid"}]
    try:
        shard = raw_shard(packet_id)
    except (AttributeError, TypeError, UnicodeEncodeError, ValueError):
        return [{"packet_id": packet_id, "status": "invalid"}]
    evidence_roots = (
        _declared_evidence_roots(root)
        if creator_metric
        else (Path(root.path).resolve(),)
    )
    rows: list[dict[str, Any]] = []
    for evidence_root in evidence_roots:
        containers = [evidence_root / "raw" / shard / packet_id]
        if creator_metric:
            containers.append(evidence_root / "raw" / packet_id)
        for container in containers:
            manifest_path = container / "manifest.json"
            manifest_state = _file_state(manifest_path)
            preserved_states: list[dict[str, Any]] = []
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
            except (OSError, ValueError, TypeError):
                manifest = {}
            preserved = (
                manifest.get("preserved_files")
                if isinstance(manifest, Mapping)
                else None
            )
            if isinstance(preserved, list):
                for item in preserved:
                    if not isinstance(item, Mapping):
                        continue
                    relative = item.get("relative_packet_path")
                    if isinstance(relative, str) and relative:
                        preserved_states.append(
                            {
                                "file_id": item.get("file_id"),
                                "declared_sha256": item.get("sha256"),
                                "state": _path_stat_state(
                                    container.joinpath(*relative.replace("\\", "/").split("/"))
                                ),
                            }
                        )
            rows.append(
                {
                    "root": str(evidence_root),
                    "container": str(container),
                    "manifest": manifest_state,
                    "preserved_file_states": preserved_states,
                }
            )
    return rows


def _catalog_fingerprint(root) -> str:
    catalog_root = Path(root.path) / "indexes" / "derived_retrieval" / "bronze_catalog" / "v0"
    rows = [
        _file_state(catalog_root / "source_surfaces.json"),
        _file_state(catalog_root / "attachment_records" / "all_attachment_records.jsonl"),
    ]
    return sha256_bytes(canonical_record_bytes(rows))


def _reference_fingerprint(
    root,
    record: Mapping[str, Any],
    *,
    packet_state_cache: dict[tuple[str, bool], list[dict[str, Any]]],
    catalog_fingerprint: str | None,
) -> tuple[str, bool]:
    lane = record.get("lane_namespace")
    creator_metric = lane in _CREATOR_METRIC_LANES
    rows: list[dict[str, Any]] = []
    attachment_backed = False
    for ref in record.get("raw_refs", []):
        if not isinstance(ref, Mapping):
            rows.append({"kind": "raw", "ref": ref})
            continue
        attachment_backed = attachment_backed or ref.get("ref_type") == "bronze_attachment_record"
        packet_id = ref.get("packet_id")
        packet_key = (str(packet_id), creator_metric)
        if packet_key not in packet_state_cache:
            packet_state_cache[packet_key] = _packet_manifest_states(
                root, packet_id, creator_metric=creator_metric
            )
        rows.append(
            {
                "kind": "raw",
                "ref": dict(ref),
                "packet_manifests": packet_state_cache[packet_key],
            }
        )
    for ref in record.get("derived_refs", []):
        row: dict[str, Any] = {"kind": "derived", "ref": ref}
        if isinstance(ref, Mapping):
            try:
                path = root.record_path(
                    subtree="derived",
                    raw_anchor=str(ref["raw_anchor"]),
                    lane=str(ref.get("lane_namespace", ref.get("lane"))),
                    record_id=str(ref["record_id"]),
                )
            except (KeyError, TypeError, ValueError):
                row["state"] = "invalid_address"
            else:
                row["state"] = _path_stat_state(path)
                if (
                    path.is_file()
                    and ref.get("sha256") is None
                    and ref.get("content_hash") is None
                ):
                    row["unclaimed_bytes"] = _file_state(path)
        rows.append(row)
    if attachment_backed:
        rows.append({"kind": "bronze_catalog", "fingerprint": catalog_fingerprint})
    return sha256_bytes(canonical_record_bytes(rows)), creator_metric


class ClassificationCacheSession:
    """One rebuild's cache state and hit/miss accounting."""

    def __init__(self, root, *, use_existing: bool = True) -> None:
        self.root = root
        self.classifier_version = classifier_version()
        self.lineage_fingerprint = _lineage_state_fingerprint(root)
        self.verdicts: dict[str, dict[str, Any]] = {}
        self.hits = 0
        self.misses = 0
        self.uncacheable = 0
        self._packet_state_cache: dict[
            tuple[str, bool], list[dict[str, Any]]
        ] = {}
        self._catalog_fingerprint: str | None = None
        if use_existing:
            self._load()

    @property
    def path(self) -> Path:
        return self.root._within(*CACHE_PARTS)

    def _load(self) -> None:
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            return
        if (
            not isinstance(payload, dict)
            or payload.get("cache_schema_version") != CACHE_SCHEMA_VERSION
            or not isinstance(payload.get("verdicts"), dict)
        ):
            return
        self.verdicts = dict(payload["verdicts"])

    def _key(self, record: Mapping[str, Any]) -> str | None:
        content_hash = record.get("content_hash")
        if not isinstance(content_hash, str) or not content_hash:
            return None
        attachment_backed = any(
            isinstance(ref, Mapping)
            and ref.get("ref_type") == "bronze_attachment_record"
            for ref in record.get("raw_refs", [])
        )
        if attachment_backed and self._catalog_fingerprint is None:
            self._catalog_fingerprint = _catalog_fingerprint(self.root)
        referenced_bytes_fingerprint, creator_metric = _reference_fingerprint(
            self.root,
            record,
            packet_state_cache=self._packet_state_cache,
            catalog_fingerprint=self._catalog_fingerprint,
        )
        key_parts = {
            "content_hash": content_hash,
            "classifier_version": self.classifier_version,
            "referenced_bytes_fingerprint": referenced_bytes_fingerprint,
            "creator_lineage_state_fingerprint": (
                self.lineage_fingerprint if creator_metric else None
            ),
        }
        return sha256_bytes(canonical_record_bytes(key_parts))

    def lookup(self, record: Mapping[str, Any]) -> tuple[str | None, SilverSourceAuthority | None]:
        key = self._key(record)
        if key is None:
            self.uncacheable += 1
            return None, None
        cached = self.verdicts.get(key)
        if not isinstance(cached, dict):
            self.misses += 1
            return key, None
        try:
            verdict = SilverSourceAuthority(
                status=cached["status"],
                reason_code=cached["reason_code"],
                error=cached.get("error"),
            )
        except (KeyError, TypeError, ValueError):
            self.misses += 1
            return key, None
        self.hits += 1
        return key, verdict

    def remember(self, key: str | None, verdict: SilverSourceAuthority) -> None:
        if key is None:
            return
        self.verdicts[key] = {
            "status": verdict.status,
            "reason_code": verdict.reason_code,
            "error": verdict.error,
        }

    def save(self) -> None:
        payload = {
            "cache_schema_version": CACHE_SCHEMA_VERSION,
            "classifier_version": self.classifier_version,
            "verdicts": dict(sorted(self.verdicts.items())),
        }
        target = self.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(canonical_record_bytes(payload))

    def report(self) -> dict[str, Any]:
        return {
            "cache_schema_version": CACHE_SCHEMA_VERSION,
            "classifier_version": self.classifier_version,
            "hits": self.hits,
            "misses": self.misses,
            "uncacheable": self.uncacheable,
            "verdict_count": len(self.verdicts),
        }


__all__ = [
    "CACHE_PARTS",
    "CACHE_SCHEMA_VERSION",
    "ClassificationCacheSession",
    "classifier_version",
]
