from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

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
) -> dict[str, Any]:
    rebuild_count = root.rebuild_availability() if rebuild_availability else None

    raw_candidates, wrong_shard, legacy_flat, malformed, missing_manifest = _raw_candidates(root)
    availability, availability_count, availability_failures = _availability_entries(root)
    valid_packet_ids = {candidate.packet_id for candidate in raw_candidates}

    missing_availability: list[str] = []
    stale_availability: list[dict[str, Any]] = []
    read_failures: list[dict[str, str]] = []
    verified_raw_packet_count = 0

    for candidate in raw_candidates:
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

    orphan_availability = sorted(packet_id for packet_id in availability if packet_id not in valid_packet_ids)
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
        description="Inspect a v4.1 Orca data lake root and optionally rebuild its availability index."
    )
    parser.add_argument(
        "--data-root",
        default=None,
        help="Orca data root to inspect. If omitted, ORCA_DATA_ROOT is used.",
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
    try:
        root = DataLakeRoot.resolve(explicit=args.data_root)
        report = inspect_data_lake(
            root,
            rebuild_availability=args.rebuild_availability,
            packet_id=args.packet_id,
        )
    except Exception as exc:
        parser.exit(status=2, message=f"data lake doctor failed: {exc}\n")

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
