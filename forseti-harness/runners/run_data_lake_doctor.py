from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.root import (  # noqa: E402
    EPOCH_MARKER_FILENAME,
    LAKE_EPOCH,
    LAKE_SUBDIRECTORIES,
    ROOT_MARKER_CONTRACT_VERSION,
    ROOT_MARKER_FILENAME,
    DataLakeRoot,
    DataLakeRootError,
    raw_shard,
)
from harness_utils import hash_file  # noqa: E402

_PACKET_ID = re.compile(r"[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{26}")
_AVAILABILITY_FIELDS = (
    "packet_id",
    "source_family",
    "source_surface",
    "raw_path",
    "manifest_relpath",
    "manifest_sha256",
)
_ALLOWED_ROOT_DIRS = {Path(subdir).parts[0] for subdir in LAKE_SUBDIRECTORIES}


@dataclass(frozen=True)
class _RawCandidate:
    packet_id: str
    container: Path
    manifest: Path


ProgressCallback = Callable[[dict[str, Any]], None]


def _notify_progress(
    progress: ProgressCallback | None,
    *,
    phase: str,
    status: str,
    started_at: float | None = None,
    **fields: Any,
) -> None:
    if progress is None:
        return
    event: dict[str, Any] = {"phase": phase, "status": status, **fields}
    if started_at is not None:
        event["elapsed_seconds"] = round(max(0.0, perf_counter() - started_at), 3)
    progress(event)


def _rel(root: DataLakeRoot, path: Path) -> str:
    return path.relative_to(root.path).as_posix()


def _read_json_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object at {path}")
    return data


def _expected_availability(root: DataLakeRoot, candidate: _RawCandidate) -> dict[str, Any]:
    manifest = _read_json_object(candidate.manifest)
    shard = raw_shard(candidate.packet_id)
    return {
        "packet_id": candidate.packet_id,
        "source_family": manifest.get("source_family"),
        "source_surface": manifest.get("source_surface"),
        "raw_path": f"raw/{shard}/{candidate.packet_id}",
        "manifest_relpath": f"raw/{shard}/{candidate.packet_id}/manifest.json",
        "manifest_sha256": hash_file(candidate.manifest),
    }


def _raw_candidates(
    root: DataLakeRoot,
) -> tuple[list[_RawCandidate], list[str], list[str], list[str], list[str]]:
    valid: list[_RawCandidate] = []
    wrong_shard: list[str] = []
    legacy_flat: list[str] = []
    malformed: list[str] = []
    missing_manifest: list[str] = []
    raw_dir = root.path / "raw"
    if not raw_dir.is_dir():
        return valid, wrong_shard, legacy_flat, malformed, missing_manifest

    for first in sorted(raw_dir.iterdir()):
        if not first.is_dir():
            continue

        flat_manifest = first / "manifest.json"
        if flat_manifest.is_file():
            if _PACKET_ID.fullmatch(first.name):
                legacy_flat.append(_rel(root, first))
            else:
                malformed.append(_rel(root, first))
            continue
        if _PACKET_ID.fullmatch(first.name):
            missing_manifest.append(_rel(root, first))
            continue

        for container in sorted(first.iterdir()):
            if not container.is_dir():
                continue
            if not _PACKET_ID.fullmatch(container.name):
                # Any non-packet-id directory under a shard dir is a
                # non-conforming raw container; surface it instead of skipping
                # (previously a manifest-less stray here vanished from the report).
                malformed.append(_rel(root, container))
                continue
            manifest = container / "manifest.json"
            if not manifest.is_file():
                # A packet-id-named container with no manifest is a partial or
                # corrupted committed packet (aborted allocate, half publish, or
                # a deleted manifest). It must stay visible: skipping it silently
                # lets a corrupt packet read as a clean lake, and rebuild_availability
                # also skips it, so absence here would hide it entirely.
                missing_manifest.append(_rel(root, container))
                continue
            if first.name != raw_shard(container.name):
                wrong_shard.append(_rel(root, container))
                continue
            valid.append(
                _RawCandidate(
                    packet_id=container.name,
                    container=container,
                    manifest=manifest,
                )
            )
    return valid, wrong_shard, legacy_flat, malformed, missing_manifest


def _availability_entries(root: DataLakeRoot) -> tuple[dict[str, dict[str, Any]], int, list[dict[str, str]]]:
    entries: dict[str, dict[str, Any]] = {}
    failures: list[dict[str, str]] = []
    count = 0
    availability_dir = root.path / "indexes" / "availability"
    if not availability_dir.is_dir():
        return entries, count, failures

    for entry_file in sorted(availability_dir.glob("*.json")):
        count += 1
        packet_id = entry_file.stem
        if not _PACKET_ID.fullmatch(packet_id):
            failures.append({"path": _rel(root, entry_file), "error": "invalid packet_id filename"})
            continue
        try:
            entry = _read_json_object(entry_file)
        except (OSError, ValueError) as exc:
            failures.append({"path": _rel(root, entry_file), "error": str(exc)})
            continue
        entries[packet_id] = entry
    return entries, count, failures


def _semantic_folder_violations(root: DataLakeRoot) -> list[str]:
    if not root.path.is_dir():
        return []
    return sorted(
        child.name
        for child in root.path.iterdir()
        if child.is_dir() and child.name not in _ALLOWED_ROOT_DIRS
    )


def _packet_report(root: DataLakeRoot, packet_id: str) -> dict[str, Any]:
    try:
        loaded = root.load_raw_packet(packet_id)
    except DataLakeRootError as exc:
        return {"packet_id": packet_id, "error": str(exc)}
    preserved = loaded.manifest.get("preserved_files")
    file_ids = [
        item.get("file_id")
        for item in preserved
        if isinstance(item, dict) and isinstance(item.get("file_id"), str)
    ] if isinstance(preserved, list) else []
    return {
        "packet_id": packet_id,
        "container": _rel(root, loaded.container),
        "manifest_relpath": f"{_rel(root, loaded.container)}/manifest.json",
        "source_family": loaded.manifest.get("source_family"),
        "source_surface": loaded.manifest.get("source_surface"),
        "preserved_file_count": len(loaded.bodies),
        "file_ids": sorted(file_ids),
    }


def inspect_data_lake(
    root: DataLakeRoot,
    *,
    rebuild_availability: bool = False,
    packet_id: str | None = None,
    progress: ProgressCallback | None = None,
) -> dict[str, Any]:
    rebuild_count = None
    if rebuild_availability:
        phase_started = perf_counter()
        _notify_progress(
            progress, phase="rebuild_availability", status="phase_started"
        )
        rebuild_count = root.rebuild_availability()
        _notify_progress(
            progress,
            phase="rebuild_availability",
            status="phase_completed",
            started_at=phase_started,
            packet_count=rebuild_count,
        )

    phase_started = perf_counter()
    _notify_progress(progress, phase="discover_raw_packets", status="phase_started")
    raw_candidates, wrong_shard, legacy_flat, malformed, missing_manifest = _raw_candidates(root)
    _notify_progress(
        progress,
        phase="discover_raw_packets",
        status="phase_completed",
        started_at=phase_started,
        raw_packet_count=len(raw_candidates),
    )

    phase_started = perf_counter()
    _notify_progress(progress, phase="read_availability_index", status="phase_started")
    availability, availability_count, availability_failures = _availability_entries(root)
    _notify_progress(
        progress,
        phase="read_availability_index",
        status="phase_completed",
        started_at=phase_started,
        availability_count=availability_count,
        read_failure_count=len(availability_failures),
    )
    valid_packet_ids = {candidate.packet_id for candidate in raw_candidates}
    phase_started = perf_counter()
    _notify_progress(progress, phase="resolve_raw_tombstones", status="phase_started")
    tombstoned_packet_ids = root.tombstoned_packet_ids()
    _notify_progress(
        progress,
        phase="resolve_raw_tombstones",
        status="phase_completed",
        started_at=phase_started,
        tombstoned_packet_count=len(tombstoned_packet_ids),
    )
    public_packet_ids = valid_packet_ids - tombstoned_packet_ids

    missing_availability: list[str] = []
    stale_availability: list[dict[str, Any]] = []
    read_failures: list[dict[str, str]] = []
    verified_raw_packet_count = 0

    phase_started = perf_counter()
    _notify_progress(
        progress,
        phase="verify_raw_packets",
        status="phase_started",
        packet_count=len(raw_candidates),
    )
    for candidate_index, candidate in enumerate(raw_candidates, start=1):
        try:
            expected = _expected_availability(root, candidate)
        except (OSError, ValueError, DataLakeRootError) as exc:
            read_failures.append(
                {
                    "packet_id": candidate.packet_id,
                    "container": _rel(root, candidate.container),
                    "error": str(exc),
                }
            )
            continue

        entry = availability.get(candidate.packet_id)
        if candidate.packet_id not in tombstoned_packet_ids:
            if entry is None:
                missing_availability.append(candidate.packet_id)
            else:
                mismatched = [
                    field
                    for field in _AVAILABILITY_FIELDS
                    if entry.get(field) != expected.get(field)
                ]
                if mismatched:
                    stale_availability.append(
                        {"packet_id": candidate.packet_id, "fields": mismatched}
                    )

        try:
            root.load_raw_packet(candidate.packet_id)
        except DataLakeRootError as exc:
            read_failures.append(
                {
                    "packet_id": candidate.packet_id,
                    "container": _rel(root, candidate.container),
                    "error": str(exc),
                }
            )
        else:
            verified_raw_packet_count += 1

        if candidate_index % 100 == 0 or candidate_index == len(raw_candidates):
            _notify_progress(
                progress,
                phase="verify_raw_packets",
                status="phase_progress",
                started_at=phase_started,
                processed_packet_count=candidate_index,
                packet_count=len(raw_candidates),
                read_failure_count=len(read_failures),
            )

    _notify_progress(
        progress,
        phase="verify_raw_packets",
        status="phase_completed",
        started_at=phase_started,
        processed_packet_count=len(raw_candidates),
        verified_packet_count=verified_raw_packet_count,
        read_failure_count=len(read_failures),
    )
    orphan_availability = sorted(
        packet_id for packet_id in availability if packet_id not in public_packet_ids
    )
    packet = _packet_report(root, packet_id) if packet_id is not None else None

    report: dict[str, Any] = {
        "root": {
            "path": str(root.path),
            "root_uuid": root.root_uuid,
            "root_marker": ROOT_MARKER_FILENAME,
            "root_contract_version": ROOT_MARKER_CONTRACT_VERSION,
            "epoch_marker": EPOCH_MARKER_FILENAME,
            "lake_epoch": LAKE_EPOCH,
        },
        "rebuild_availability_count": rebuild_count,
        "raw_packet_count": len(raw_candidates),
        "verified_raw_packet_count": verified_raw_packet_count,
        "public_raw_packet_count": len(public_packet_ids),
        "tombstoned_raw_packets": sorted(valid_packet_ids & tombstoned_packet_ids),
        "availability_count": availability_count,
        "missing_availability": sorted(missing_availability),
        "stale_availability": sorted(stale_availability, key=lambda item: item["packet_id"]),
        "orphan_availability": orphan_availability,
        "wrong_shard_packets": wrong_shard,
        "legacy_flat_packets": legacy_flat,
        "malformed_raw_containers": malformed,
        "missing_manifest_raw_containers": missing_manifest,
        "availability_read_failures": availability_failures,
        "read_failures": read_failures,
        "semantic_folder_violations": _semantic_folder_violations(root),
    }
    if packet is not None:
        report["packet"] = packet

    issue_keys = (
        "missing_availability",
        "stale_availability",
        "orphan_availability",
        "wrong_shard_packets",
        "legacy_flat_packets",
        "malformed_raw_containers",
        "missing_manifest_raw_containers",
        "availability_read_failures",
        "read_failures",
        "semantic_folder_violations",
    )
    has_issue = any(report[key] for key in issue_keys) or bool(
        isinstance(packet, dict) and packet.get("error")
    )
    report["status"] = "issues_found" if has_issue else "ok"
    return report


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect a v4.1 Forseti data lake root and optionally rebuild its availability index."
    )
    parser.add_argument(
        "--data-root",
        default=None,
        help="Forseti data root to inspect. If omitted, FORSETI_DATA_ROOT is used; legacy ORCA_DATA_ROOT is also accepted.",
    )
    parser.add_argument(
        "--rebuild-availability",
        action="store_true",
        help="Rewrite indexes/availability from committed raw packets before reporting.",
    )
    parser.add_argument(
        "--packet-id",
        default=None,
        help="Inspect one raw packet by key and include its verified read summary.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    command_started = perf_counter()

    def emit_progress(event: dict[str, Any]) -> None:
        print(json.dumps(event, sort_keys=True), file=sys.stderr, flush=True)

    emit_progress({"phase": "data_lake_doctor", "status": "phase_started"})
    try:
        root = DataLakeRoot.resolve(explicit=args.data_root)
        report = inspect_data_lake(
            root,
            rebuild_availability=args.rebuild_availability,
            packet_id=args.packet_id,
            progress=emit_progress,
        )
    except Exception as exc:
        emit_progress(
            {
                "phase": "data_lake_doctor",
                "status": "phase_failed",
                "elapsed_seconds": round(
                    max(0.0, perf_counter() - command_started), 3
                ),
                "error_type": type(exc).__name__,
            }
        )
        parser.exit(status=2, message=f"data lake doctor failed: {exc}\n")

    emit_progress(
        {
            "phase": "data_lake_doctor",
            "status": "phase_completed",
            "elapsed_seconds": round(max(0.0, perf_counter() - command_started), 3),
            "result_status": report["status"],
        }
    )
    print(json.dumps(report, indent=2, sort_keys=True), flush=True)
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
