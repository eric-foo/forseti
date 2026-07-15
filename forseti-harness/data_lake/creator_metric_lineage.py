"""Read-only creator-metric Silver evidence verification across lake epochs.

Normal lake readers remain single-root and v4.1-forward.  This module is the
bounded compatibility path for creator-metric lineage: it reads the current
root plus only the legacy roots explicitly declared by that root's epoch marker,
locates the bytes cited by each raw ref, re-hashes them, and classifies records
without writing a status file or mutating either lake.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any, Literal, Mapping

from data_lake.root import (
    EPOCH_MARKER_FILENAME,
    LEGACY_EPOCH_MARKER_FILENAME,
    LEGACY_ROOT_MARKER_FILENAME,
    ROOT_MARKER_FILENAME,
    raw_shard,
)


SOURCE_BACKED_COMPLETE = "source_backed_complete"
HISTORICAL_COMPATIBLE = "historical_compatible"
EXCLUDED = "excluded"
CURRENT_SOURCE_BACKED = "current_source_backed"
AUDIT_COMPATIBLE = "audit_compatible"

CreatorMetricLineageStatus = Literal[
    "source_backed_complete", "historical_compatible", "excluded"
]
CreatorMetricReadMode = Literal["current_source_backed", "audit_compatible"]

OBSERVATION_LANE = "creator_metric_silver"
ROLLUP_LANE = "creator_metric_rollup_silver"
LINEAGE_RECONCILIATION_SCHEMA_VERSION = "creator_metric_lineage_reconciliation_v0"

_HISTORICAL_IMPACT = (
    "audit-readable only; excluded from current source-backed creator-metric "
    "retrieval and census observation totals"
)
_EXCLUDED_IMPACT = (
    "not admissible as creator-metric evidence; excluded from current "
    "source-backed retrieval and census observation totals"
)
_OWNER = "creator_metric_silver owner"
_UPGRADE_TRIGGER = (
    "re-capture and re-derive from genuinely preserved evidence, or a later "
    "explicit owner decision changing epoch doctrine"
)
_PACKET_ID = re.compile(r"[0-9A-HJKMNP-TV-Z]{26}")


class CreatorMetricLineageError(ValueError):
    """A creator-metric record cannot be safely classified or admitted."""

    def __init__(self, reason_code: str, detail: str) -> None:
        self.reason_code = reason_code
        super().__init__(f"{reason_code}: {detail}")


@dataclass(frozen=True)
class EvidenceRoot:
    role: Literal["current_root", "declared_archive"]
    path: Path
    mounted: bool
    root_uuid: str | None
    label: str | None
    contract_version: str | None
    lake_epoch: str | None
    epoch_policy: str | None
    marker_error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "path": str(self.path),
            "mounted": self.mounted,
            "root_uuid": self.root_uuid,
            "label": self.label,
            "contract_version": self.contract_version,
            "lake_epoch": self.lake_epoch,
            "epoch_policy": self.epoch_policy,
            "marker_error": self.marker_error,
        }


@dataclass(frozen=True)
class CreatorMetricLineageClassification:
    status: CreatorMetricLineageStatus
    reason_code: str
    current_source_backed_eligible: bool
    evidence_roots: tuple[EvidenceRoot, ...] = ()
    evidence_locations: tuple[str, ...] = ()
    expected_sha256: str | None = None
    recomputed_sha256: str | None = None
    impact: str | None = None
    owner: str | None = None
    upgrade_trigger: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "reason_code": self.reason_code,
            "current_source_backed_eligible": self.current_source_backed_eligible,
            "evidence_roots": [root.as_dict() for root in self.evidence_roots],
            "evidence_locations": list(self.evidence_locations),
            "expected_sha256": self.expected_sha256,
            "recomputed_sha256": self.recomputed_sha256,
            "impact": self.impact,
            "owner": self.owner,
            "upgrade_trigger": self.upgrade_trigger,
        }


@dataclass(frozen=True)
class _IndexedObservation:
    path: Path
    record: Mapping[str, Any]
    classification: CreatorMetricLineageClassification


class CreatorMetricLineageIndex:
    """One rebuildable, read-only classification of creator-metric records."""

    def __init__(
        self,
        *,
        current_root: EvidenceRoot,
        declared_archives: tuple[EvidenceRoot, ...],
        observations_by_path: Mapping[Path, _IndexedObservation],
        observations_by_id: Mapping[str, tuple[_IndexedObservation, ...]],
        rollups_by_path: Mapping[Path, CreatorMetricLineageClassification],
    ) -> None:
        self.current_root = current_root
        self.declared_archives = declared_archives
        self._observations_by_path = dict(observations_by_path)
        self._observations_by_id = dict(observations_by_id)
        self._rollups_by_path = dict(rollups_by_path)

    def classification_for_path(self, path: Path) -> CreatorMetricLineageClassification:
        resolved = path.resolve()
        observation = self._observations_by_path.get(resolved)
        if observation is not None:
            return observation.classification
        rollup = self._rollups_by_path.get(resolved)
        if rollup is not None:
            return rollup
        raise CreatorMetricLineageError("record_not_indexed", str(path))

    def admits(self, path: Path, *, mode: CreatorMetricReadMode) -> bool:
        classification = self.classification_for_path(path)
        if classification.status == EXCLUDED:
            raise CreatorMetricLineageError(
                classification.reason_code,
                f"excluded creator-metric record at {path}",
            )
        if mode == CURRENT_SOURCE_BACKED:
            return classification.current_source_backed_eligible
        if mode == AUDIT_COMPATIBLE:
            return classification.status in {SOURCE_BACKED_COMPLETE, HISTORICAL_COMPATIBLE}
        raise CreatorMetricLineageError("unsupported_read_mode", repr(mode))

    def reconciliation(self) -> dict[str, Any]:
        lane_rows: dict[str, list[CreatorMetricLineageClassification]] = {
            OBSERVATION_LANE: [item.classification for item in self._observations_by_path.values()],
            ROLLUP_LANE: list(self._rollups_by_path.values()),
        }
        by_lane: dict[str, Any] = {}
        all_rows: list[tuple[str, CreatorMetricLineageClassification]] = []
        for lane, rows in lane_rows.items():
            counts = Counter(row.status for row in rows)
            by_lane[lane] = {
                "record_count": len(rows),
                "classification_counts": {
                    SOURCE_BACKED_COMPLETE: counts[SOURCE_BACKED_COMPLETE],
                    HISTORICAL_COMPATIBLE: counts[HISTORICAL_COMPATIBLE],
                    EXCLUDED: counts[EXCLUDED],
                },
                "current_source_backed_eligible_records": sum(
                    row.current_source_backed_eligible for row in rows
                ),
                "exact_reconciliation": sum(counts.values()) == len(rows),
            }
            all_rows.extend((lane, row) for row in rows)

        counts = Counter(row.status for _, row in all_rows)
        residual_groups: dict[tuple[str, str, str], list[CreatorMetricLineageClassification]] = defaultdict(list)
        for lane, row in all_rows:
            if not row.current_source_backed_eligible:
                residual_groups[(lane, row.status, row.reason_code)].append(row)
        residuals = []
        for (lane, status, reason), rows in sorted(residual_groups.items()):
            roots = {
                json.dumps(root.as_dict(), sort_keys=True): root.as_dict()
                for row in rows
                for root in row.evidence_roots
            }
            residuals.append(
                {
                    "lane": lane,
                    "status": status,
                    "reason_code": reason,
                    "count": len(rows),
                    "evidence_roots": [roots[key] for key in sorted(roots)],
                    "impact": rows[0].impact,
                    "owner": rows[0].owner,
                    "upgrade_trigger": rows[0].upgrade_trigger,
                }
            )
        total = len(all_rows)
        return {
            "schema_version": LINEAGE_RECONCILIATION_SCHEMA_VERSION,
            "current_root": self.current_root.as_dict(),
            "declared_archives": [root.as_dict() for root in self.declared_archives],
            "record_count": total,
            "classification_counts": {
                SOURCE_BACKED_COMPLETE: counts[SOURCE_BACKED_COMPLETE],
                HISTORICAL_COMPATIBLE: counts[HISTORICAL_COMPATIBLE],
                EXCLUDED: counts[EXCLUDED],
            },
            "current_source_backed_eligible_records": sum(
                row.current_source_backed_eligible for _, row in all_rows
            ),
            "by_lane": by_lane,
            "exact_reconciliation": sum(counts.values()) == total
            and all(item["exact_reconciliation"] for item in by_lane.values()),
            "residuals": residuals,
        }


def build_creator_metric_lineage_index(data_root: Any) -> CreatorMetricLineageIndex:
    """Recompute creator-metric evidence status from the current root and its
    explicitly declared archives.  No archive is searched unless named by the
    current epoch marker; archive matches never become current-root eligibility."""
    current_root, archives = _evidence_roots(data_root)
    by_path: dict[Path, _IndexedObservation] = {}
    by_id_lists: dict[str, list[_IndexedObservation]] = defaultdict(list)
    derived = current_root.path / "derived"
    for path in sorted(derived.glob(f"*/*/{OBSERVATION_LANE}/*.json")):
        resolved = path.resolve()
        try:
            record = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError, TypeError) as exc:
            classification = _excluded("record_unreadable")
            record = {}
        else:
            if not isinstance(record, Mapping):
                classification = _excluded("record_not_json_object")
                record = {}
            else:
                classification = classify_creator_metric_observation(
                    record, current_root=current_root, declared_archives=archives
                )
        item = _IndexedObservation(resolved, record, classification)
        by_path[resolved] = item
        record_id = record.get("record_id")
        if isinstance(record_id, str) and record_id:
            by_id_lists[record_id].append(item)

    by_id = {key: tuple(values) for key, values in by_id_lists.items()}
    rollups: dict[Path, CreatorMetricLineageClassification] = {}
    for path in sorted(derived.glob(f"*/*/{ROLLUP_LANE}/*.json")):
        resolved = path.resolve()
        try:
            record = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError, TypeError):
            rollups[resolved] = _excluded("record_unreadable")
            continue
        if not isinstance(record, Mapping):
            rollups[resolved] = _excluded("record_not_json_object")
            continue
        if record.get("derived_refs"):
            rollups[resolved] = classify_creator_metric_rollup(
                record, observations_by_id=by_id
            )
        else:
            # The live producers use exact derived refs, but the Silver envelope
            # contract also permits a directly raw-backed rollup. Verify that
            # direct evidence by the same byte rule rather than inventing a
            # derived-ref requirement the owning contract does not contain.
            rollups[resolved] = classify_creator_metric_observation(
                record, current_root=current_root, declared_archives=archives
            )

    return CreatorMetricLineageIndex(
        current_root=current_root,
        declared_archives=archives,
        observations_by_path=by_path,
        observations_by_id=by_id,
        rollups_by_path=rollups,
    )


def classify_creator_metric_observation(
    record: Mapping[str, Any],
    *,
    current_root: EvidenceRoot,
    declared_archives: tuple[EvidenceRoot, ...],
) -> CreatorMetricLineageClassification:
    refs = record.get("raw_refs")
    if not isinstance(refs, list) or not refs:
        return _excluded("raw_refs_missing")
    results = [
        _classify_raw_ref(
            ref,
            raw_anchor=record.get("raw_anchor"),
            current_root=current_root,
            declared_archives=declared_archives,
        )
        if isinstance(ref, Mapping)
        else _excluded("raw_ref_malformed")
        for ref in refs
    ]
    excluded = next((result for result in results if result.status == EXCLUDED), None)
    if excluded is not None:
        return excluded
    if all(result.current_source_backed_eligible for result in results):
        return _combine(results, SOURCE_BACKED_COMPLETE, "current_root_bytes_verified", True)
    if all(result.status == SOURCE_BACKED_COMPLETE for result in results):
        return _combine(results, SOURCE_BACKED_COMPLETE, "declared_archive_bytes_verified", False)
    return _combine(
        results,
        HISTORICAL_COMPATIBLE,
        "archive_packet_present_cited_bytes_absent",
        False,
        impact=_HISTORICAL_IMPACT,
    )


def classify_creator_metric_rollup(
    record: Mapping[str, Any],
    *,
    observations_by_id: Mapping[str, tuple[_IndexedObservation, ...]],
) -> CreatorMetricLineageClassification:
    refs = record.get("derived_refs")
    if not isinstance(refs, list) or not refs:
        return _excluded("derived_refs_missing")
    sources: list[CreatorMetricLineageClassification] = []
    for ref in refs:
        if not isinstance(ref, Mapping):
            return _excluded("derived_ref_malformed")
        if ref.get("lane_namespace", ref.get("lane")) != OBSERVATION_LANE:
            return _excluded("derived_ref_wrong_lane")
        record_id = ref.get("record_id")
        if not isinstance(record_id, str) or not record_id:
            return _excluded("derived_ref_record_id_missing")
        candidates = observations_by_id.get(record_id, ())
        if not candidates:
            return _excluded("derived_observation_missing")
        if len(candidates) != 1:
            return _excluded("ambiguous_duplicate_observation_record_id")
        source = candidates[0]
        expected_hash = ref.get("content_hash", ref.get("sha256"))
        if expected_hash != source.record.get("content_hash"):
            return _excluded("derived_observation_content_hash_mismatch")
        if source.classification.status == EXCLUDED:
            return _excluded("depends_on_excluded_observation")
        sources.append(source.classification)
    if all(source.current_source_backed_eligible for source in sources):
        return _combine(sources, SOURCE_BACKED_COMPLETE, "all_inputs_current_root_byte_verified", True)
    return _combine(
        sources,
        HISTORICAL_COMPATIBLE,
        "depends_on_noncurrent_source_evidence",
        False,
        impact=_HISTORICAL_IMPACT,
    )


def _evidence_roots(data_root: Any) -> tuple[EvidenceRoot, tuple[EvidenceRoot, ...]]:
    current_path = Path(data_root.path).resolve()
    current = _read_root_identity(current_path, role="current_root")
    if current.marker_error is not None or current.root_uuid != data_root.root_uuid:
        raise CreatorMetricLineageError(
            "current_root_identity_invalid",
            current.marker_error or f"expected {data_root.root_uuid}, found {current.root_uuid}",
        )
    epoch_path = _existing_marker(current_path, EPOCH_MARKER_FILENAME, LEGACY_EPOCH_MARKER_FILENAME)
    if epoch_path is None:
        raise CreatorMetricLineageError("current_epoch_marker_missing", str(current_path))
    try:
        epoch = json.loads(epoch_path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError, TypeError) as exc:
        raise CreatorMetricLineageError("current_epoch_marker_unreadable", str(exc)) from exc
    legacy_roots = epoch.get("legacy_roots") if isinstance(epoch, Mapping) else None
    if not isinstance(legacy_roots, list):
        raise CreatorMetricLineageError("declared_archives_invalid", "legacy_roots must be a list")
    archives: list[EvidenceRoot] = []
    seen: set[Path] = set()
    for value in legacy_roots:
        if not isinstance(value, str) or not value.strip() or not Path(value).is_absolute():
            raise CreatorMetricLineageError("declared_archive_path_invalid", repr(value))
        path = Path(value).resolve()
        if path == current_path or path in seen:
            raise CreatorMetricLineageError("declared_archive_path_ambiguous", str(path))
        seen.add(path)
        archives.append(_read_root_identity(path, role="declared_archive"))
    return current, tuple(archives)


def _read_root_identity(path: Path, *, role: Literal["current_root", "declared_archive"]) -> EvidenceRoot:
    mounted = path.is_dir()
    if not mounted:
        return EvidenceRoot(role, path, False, None, None, None, None, None)
    marker_path = _existing_marker(path, ROOT_MARKER_FILENAME, LEGACY_ROOT_MARKER_FILENAME)
    if marker_path is None:
        return EvidenceRoot(role, path, True, None, None, None, None, None, "root_marker_missing")
    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError, TypeError) as exc:
        return EvidenceRoot(role, path, True, None, None, None, None, None, f"root_marker_unreadable:{exc}")
    if (
        not isinstance(marker, Mapping)
        or not isinstance(marker.get("root_uuid"), str)
        or not marker.get("root_uuid")
        or not isinstance(marker.get("contract_version"), str)
        or not marker.get("contract_version")
    ):
        return EvidenceRoot(role, path, True, None, None, None, None, None, "root_marker_malformed")
    epoch_path = _existing_marker(path, EPOCH_MARKER_FILENAME, LEGACY_EPOCH_MARKER_FILENAME)
    epoch: Mapping[str, Any] = {}
    if epoch_path is not None:
        try:
            value = json.loads(epoch_path.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError, TypeError) as exc:
            return EvidenceRoot(
                role, path, True, marker.get("root_uuid"), marker.get("label"),
                marker.get("contract_version"), None, None, f"epoch_marker_unreadable:{exc}"
            )
        if isinstance(value, Mapping):
            epoch = value
    return EvidenceRoot(
        role=role,
        path=path,
        mounted=True,
        root_uuid=marker.get("root_uuid") if isinstance(marker, Mapping) else None,
        label=marker.get("label") if isinstance(marker, Mapping) else None,
        contract_version=marker.get("contract_version") if isinstance(marker, Mapping) else None,
        lake_epoch=epoch.get("lake_epoch"),
        epoch_policy=epoch.get("epoch_policy"),
    )


def _existing_marker(root: Path, primary: str, legacy: str) -> Path | None:
    for name in (primary, legacy):
        path = root / name
        if path.is_file():
            return path
    return None


def _classify_raw_ref(
    ref: Mapping[str, Any],
    *,
    raw_anchor: Any,
    current_root: EvidenceRoot,
    declared_archives: tuple[EvidenceRoot, ...],
) -> CreatorMetricLineageClassification:
    packet_id = ref.get("packet_id")
    expected = ref.get("sha256")
    basis = ref.get("hash_basis")
    if not all(isinstance(value, str) and value.strip() for value in (packet_id, expected, basis)):
        return _excluded("raw_ref_hash_identity_missing")
    if packet_id != raw_anchor:
        return _excluded("raw_anchor_packet_id_contradiction")
    if _PACKET_ID.fullmatch(packet_id) is None:
        return _excluded("packet_id_invalid")
    try:
        shard = raw_shard(packet_id)
    except (AttributeError, TypeError, UnicodeEncodeError, ValueError):
        return _excluded("packet_id_invalid")
    roots = (current_root, *declared_archives)
    candidates: list[tuple[EvidenceRoot, Path]] = []
    for root in roots:
        if not root.mounted or root.marker_error is not None:
            continue
        for path in (root.path / "raw" / shard / packet_id, root.path / "raw" / packet_id):
            if path.is_dir():
                candidates.append((root, path.resolve()))
    unique = {(root.path, path): (root, path) for root, path in candidates}
    candidates = list(unique.values())
    if len(candidates) > 1:
        return _excluded("ambiguous_duplicate_resolution", roots=tuple(root for root, _ in candidates))
    if not candidates:
        bad_archives = [root for root in declared_archives if not root.mounted or root.marker_error]
        if bad_archives:
            return _excluded("declared_archive_unmounted_or_invalid", roots=tuple(bad_archives))
        return _excluded("packet_missing_from_current_and_declared_archives")
    root, packet = candidates[0]
    verification = _verify_packet_ref(packet, ref)
    if verification["status"] == "verified":
        return CreatorMetricLineageClassification(
            status=SOURCE_BACKED_COMPLETE,
            reason_code="current_root_bytes_verified" if root.role == "current_root" else "declared_archive_bytes_verified",
            current_source_backed_eligible=root.role == "current_root",
            evidence_roots=(root,),
            evidence_locations=(verification["path"],),
            expected_sha256=expected,
            recomputed_sha256=verification["actual_sha256"],
            impact=None if root.role == "current_root" else _HISTORICAL_IMPACT,
            owner=None if root.role == "current_root" else _OWNER,
            upgrade_trigger=None if root.role == "current_root" else _UPGRADE_TRIGGER,
        )
    if verification["status"] == "cited_bytes_absent" and root.role == "declared_archive":
        return CreatorMetricLineageClassification(
            status=HISTORICAL_COMPATIBLE,
            reason_code="archive_packet_present_cited_bytes_absent",
            current_source_backed_eligible=False,
            evidence_roots=(root,),
            expected_sha256=expected,
            impact=_HISTORICAL_IMPACT,
            owner=_OWNER,
            upgrade_trigger=_UPGRADE_TRIGGER,
        )
    return _excluded(
        verification["status"],
        roots=(root,),
        expected_sha256=expected,
        recomputed_sha256=verification.get("actual_sha256"),
    )


def _verify_packet_ref(packet: Path, ref: Mapping[str, Any]) -> dict[str, Any]:
    manifest_path = packet / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError, TypeError):
        return {"status": "manifest_unreadable"}
    preserved = manifest.get("preserved_files") if isinstance(manifest, Mapping) else None
    if not isinstance(preserved, list) or not preserved:
        return {"status": "manifest_preserved_files_invalid"}
    files: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    packet_root = packet.resolve()
    for item in preserved:
        if not isinstance(item, Mapping):
            return {"status": "manifest_preserved_files_invalid"}
        file_id = item.get("file_id")
        relative = item.get("relative_packet_path")
        if not isinstance(file_id, str) or not file_id or not isinstance(relative, str) or not relative:
            return {"status": "manifest_preserved_files_invalid"}
        normalized = relative.replace("\\", "/")
        parts = PurePosixPath(normalized).parts
        if PurePosixPath(normalized).is_absolute() or not parts or any(part in {"", ".", ".."} for part in parts):
            return {"status": "preserved_path_invalid"}
        if file_id in seen_ids or normalized in seen_paths:
            return {"status": "manifest_preserved_file_ambiguous"}
        seen_ids.add(file_id)
        seen_paths.add(normalized)
        path = packet.joinpath(*parts).resolve()
        try:
            path.relative_to(packet_root)
        except ValueError:
            return {"status": "preserved_path_escapes_packet"}
        try:
            body = path.read_bytes()
        except OSError:
            return {"status": "preserved_file_missing_or_unreadable"}
        actual = hashlib.sha256(body).hexdigest()
        if item.get("sha256") != actual or item.get("size_bytes") != len(body):
            return {"status": "packet_manifest_hash_mismatch", "actual_sha256": actual}
        files.append({"file_id": file_id, "relative": normalized, "path": str(path), "sha256": actual})

    direct_path = ref.get("relative_packet_path")
    direct_id = ref.get("file_id")
    direct = files
    if direct_path is not None:
        if not isinstance(direct_path, str) or not direct_path:
            return {"status": "raw_ref_file_identity_invalid"}
        wanted = direct_path.replace("\\", "/")
        direct = [item for item in direct if item["relative"] == wanted]
    if direct_id is not None:
        if not isinstance(direct_id, str) or not direct_id:
            return {"status": "raw_ref_file_identity_invalid"}
        direct = [item for item in direct if item["file_id"] == direct_id]
    if direct_path is not None or direct_id is not None:
        if len(direct) > 1:
            return {"status": "ambiguous_multiple_byte_matches"}
        if not direct:
            return {"status": "cited_bytes_absent"}
        candidate = direct[0]
        if candidate["sha256"] != ref.get("sha256"):
            return {"status": "hash_mismatch", "actual_sha256": candidate["sha256"]}
        return {"status": "verified", "path": candidate["path"], "actual_sha256": candidate["sha256"]}

    matches = [item for item in files if item["sha256"] == ref.get("sha256")]
    if len(matches) > 1:
        return {"status": "ambiguous_multiple_byte_matches"}
    if not matches:
        return {"status": "cited_bytes_absent"}
    return {"status": "verified", "path": matches[0]["path"], "actual_sha256": matches[0]["sha256"]}


def _combine(
    rows: list[CreatorMetricLineageClassification],
    status: CreatorMetricLineageStatus,
    reason: str,
    eligible: bool,
    *,
    impact: str | None = None,
) -> CreatorMetricLineageClassification:
    roots = {root.path: root for row in rows for root in row.evidence_roots}
    locations = sorted({path for row in rows for path in row.evidence_locations})
    return CreatorMetricLineageClassification(
        status=status,
        reason_code=reason,
        current_source_backed_eligible=eligible,
        evidence_roots=tuple(roots[path] for path in sorted(roots, key=str)),
        evidence_locations=tuple(locations),
        impact=impact,
        owner=_OWNER if impact else None,
        upgrade_trigger=_UPGRADE_TRIGGER if impact else None,
    )


def _excluded(
    reason: str,
    *,
    roots: tuple[EvidenceRoot, ...] = (),
    expected_sha256: str | None = None,
    recomputed_sha256: str | None = None,
) -> CreatorMetricLineageClassification:
    return CreatorMetricLineageClassification(
        status=EXCLUDED,
        reason_code=reason,
        current_source_backed_eligible=False,
        evidence_roots=roots,
        expected_sha256=expected_sha256,
        recomputed_sha256=recomputed_sha256,
        impact=_EXCLUDED_IMPACT,
        owner=_OWNER,
        upgrade_trigger=_UPGRADE_TRIGGER,
    )


__all__ = [
    "AUDIT_COMPATIBLE",
    "CURRENT_SOURCE_BACKED",
    "EXCLUDED",
    "HISTORICAL_COMPATIBLE",
    "OBSERVATION_LANE",
    "ROLLUP_LANE",
    "SOURCE_BACKED_COMPLETE",
    "CreatorMetricLineageClassification",
    "CreatorMetricLineageError",
    "CreatorMetricLineageIndex",
    "CreatorMetricReadMode",
    "EvidenceRoot",
    "build_creator_metric_lineage_index",
    "classify_creator_metric_observation",
    "classify_creator_metric_rollup",
]
