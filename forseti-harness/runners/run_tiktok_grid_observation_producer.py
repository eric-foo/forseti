"""Derive packet-grain TikTok grid metric observations into Silver.

Every committed TikTok packet is acknowledged for the current policy. Packets
without a preserved grid window receive an explicit not-applicable ack; target
packets are acknowledged only after the deterministic Silver record has passed
byte readback and schema/integrity validation in the producer.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.tiktok_grid_observation_producer import (
    SOCIAL_METRIC_OBSERVATION_SET_LANE,
    TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT,
    TIKTOK_GRID_OBSERVATION_SOURCE_SURFACE,
    derive_tiktok_grid_observation_set,
    derive_tiktok_profile_metric_observations,
)
from data_lake.consumption import append_ack, is_acknowledged, pickup, reconcile_availability_per_packet
from data_lake.root import DataLakeRoot, DataLakeRootError
from source_capture.tiktok.batch_packet import (
    TIKTOK_BATCH_CAPTURE_SURFACE,
    TIKTOK_BATCH_GRID_WINDOW_JSON_NAME,
)
from source_capture.tiktok.grid_packet import TIKTOK_GRID_WINDOW_JSON_NAME

_ACK_NAMESPACE = SOCIAL_METRIC_OBSERVATION_SET_LANE
_SOURCE_FAMILY = "tiktok"


def _obligation(data_root: DataLakeRoot, packet_id: str) -> dict[str, Any]:
    availability = data_root.read_availability(packet_id) or {}
    return {
        "obligation_schema": 1,
        "consumer": "tiktok_grid_observation_producer",
        "policy_fingerprint_sha256": TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT,
        "manifest_sha256": str(availability.get("manifest_sha256") or "missing"),
    }


def _grid_input(
    data_root: DataLakeRoot, packet_id: str
) -> tuple[dict[str, Any], dict[str, Any], str, str] | None:
    loaded = data_root.load_raw_packet(packet_id)
    source_surface = str(loaded.manifest.get("source_surface") or "")
    if source_surface not in {
        TIKTOK_GRID_OBSERVATION_SOURCE_SURFACE,
        TIKTOK_BATCH_CAPTURE_SURFACE,
    }:
        return None
    expected_name = (
        TIKTOK_BATCH_GRID_WINDOW_JSON_NAME
        if source_surface == TIKTOK_BATCH_CAPTURE_SURFACE
        else TIKTOK_GRID_WINDOW_JSON_NAME
    )
    matches = [
        item
        for item in loaded.manifest.get("preserved_files", [])
        if isinstance(item, Mapping)
        and _staged_artifact_name(item) == expected_name
    ]
    if not matches and source_surface == TIKTOK_BATCH_CAPTURE_SURFACE:
        return None
    if len(matches) != 1:
        raise ValueError(
            f"packet {packet_id} requires exactly one {expected_name}"
        )
    preserved = dict(matches[0])
    file_id = str(preserved.get("file_id") or "")
    body = loaded.bodies.get(file_id)
    if body is None:
        raise ValueError(f"packet {packet_id} TikTok grid body is absent")
    try:
        payload = json.loads(body.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"packet {packet_id} TikTok grid is invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"packet {packet_id} TikTok grid must be a JSON object")
    observed_at = _observed_at(payload, loaded.manifest)
    return (
        payload,
        {
            "file_id": file_id,
            "relative_packet_path": preserved.get("relative_packet_path"),
            "sha256": preserved.get("sha256"),
            "hash_basis": "raw_stored_bytes",
        },
        observed_at,
        source_surface,
    )


def _staged_artifact_name(preserved: Mapping[str, Any]) -> str:
    """Recover the canonical staged name from ``raw/NN_<name>`` storage."""
    stored_name = Path(str(preserved.get("relative_packet_path") or "")).name
    ordinal, separator, staged_name = stored_name.partition("_")
    if separator and len(ordinal) == 2 and ordinal.isdigit():
        return staged_name
    return stored_name


def _observed_at(payload: Mapping[str, Any], manifest: Mapping[str, Any]) -> str:
    receipt = payload.get("collection_receipt")
    if isinstance(receipt, Mapping):
        capture_timestamp = receipt.get("capture_timestamp")
        if isinstance(capture_timestamp, str) and capture_timestamp.strip():
            return capture_timestamp
    for source_slice in manifest.get("source_slices", []):
        if not isinstance(source_slice, Mapping):
            continue
        timing = source_slice.get("timing")
        capture_time = timing.get("capture_time") if isinstance(timing, Mapping) else None
        if not isinstance(capture_time, Mapping) or capture_time.get("status") != "known":
            continue
        value = capture_time.get("value")
        if isinstance(value, str) and value.strip():
            return value
    raise ValueError("TikTok grid packet lacks a source-backed capture timestamp")


def run_tiktok_grid_observations(
    *, data_root: DataLakeRoot, packet_ids: Sequence[str] | None = None
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    results.extend(reconcile_availability_per_packet(data_root))
    requested = set(packet_ids or ())
    items = list(pickup(
        data_root,
        ack_namespace=_ACK_NAMESPACE,
        obligation_fn=lambda packet_id: _obligation(data_root, packet_id),
        source_family=_SOURCE_FAMILY,
        reconcile=False,
    ))
    if requested:
        items = [item for item in items if item.raw_anchor in requested]
        selected = {item.raw_anchor for item in items}
        for packet_id in sorted(requested - selected):
            obligation = _obligation(data_root, packet_id)
            if is_acknowledged(
                data_root,
                raw_anchor=packet_id,
                ack_namespace=_ACK_NAMESPACE,
                obligation=obligation,
            ):
                results.append({"packet_id": packet_id, "status": "already_current"})
            else:
                results.append({"packet_id": packet_id, "status": "not_pending_or_unavailable"})
    for item in items:
        packet_id = item.raw_anchor
        try:
            grid_input = _grid_input(data_root, packet_id)
            if grid_input is None:
                evidence = [
                    {
                        "kind": "not_applicable_non_grid_source_surface",
                        "manifest_sha256": item.obligation["manifest_sha256"],
                        "policy_fingerprint_sha256": (
                            TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT
                        ),
                    }
                ]
                append_ack(
                    data_root,
                    raw_anchor=packet_id,
                    ack_namespace=_ACK_NAMESPACE,
                    obligation=item.obligation,
                    evidence=evidence,
                )
                results.append({"packet_id": packet_id, "status": "not_applicable"})
                continue
            payload, raw_file_ref, observed_at, source_packet_surface = grid_input
            derived = derive_tiktok_grid_observation_set(
                data_root=data_root,
                raw_anchor=packet_id,
                grid_payload=payload,
                raw_file_ref=raw_file_ref,
                observed_at=observed_at,
                source_packet_surface=source_packet_surface,
            )
            profile_derived = derive_tiktok_profile_metric_observations(
                data_root=data_root,
                raw_anchor=packet_id,
                grid_payload=payload,
                raw_file_ref=raw_file_ref,
                observed_at=observed_at,
                source_packet_surface=source_packet_surface,
            )
            if payload.get("profile_metric_capture_policy_version") is not None and len(
                profile_derived
            ) != 2:
                raise ValueError(
                    "current TikTok grid profile policy requires exactly two Silver metrics"
                )
            observation = derived.record["payload"]["observation"]
            evidence = [
                {
                    "kind": "silver_observation_set_verified",
                    "lane": SOCIAL_METRIC_OBSERVATION_SET_LANE,
                    "record_id": derived.record["record_id"],
                    "content_hash": derived.record["content_hash"],
                    "row_count": observation["row_count"],
                    "policy_fingerprint_sha256": (
                        TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT
                    ),
                }
            ]
            evidence.extend(
                {
                    "kind": "silver_profile_metric_verified",
                    "lane": result.record["lane_namespace"],
                    "record_id": result.record["record_id"],
                    "content_hash": result.record["content_hash"],
                    "metric_name": result.record["payload"]["observation"]["metric_name"],
                }
                for result in profile_derived
            )
            append_ack(
                data_root,
                raw_anchor=packet_id,
                ack_namespace=_ACK_NAMESPACE,
                obligation=item.obligation,
                evidence=evidence,
            )
            results.append(
                {
                    "packet_id": packet_id,
                    "status": "derived",
                    "record_id": derived.record["record_id"],
                    "row_count": observation["row_count"],
                    "written": derived.written,
                    "profile_metric_record_ids": [
                        result.record["record_id"] for result in profile_derived
                    ],
                    "profile_metric_written_count": sum(
                        1 for result in profile_derived if result.written
                    ),
                }
            )
        except Exception as exc:  # noqa: BLE001 - one corrupt packet must not hide peers
            results.append(
                {
                    "packet_id": packet_id,
                    "status": "failed",
                    "error": f"{type(exc).__name__}: {exc}"[:300],
                }
            )
    return results


def pending_packets(*, data_root: DataLakeRoot) -> list[str]:
    failures = reconcile_availability_per_packet(data_root)
    if failures:
        first = failures[0]
        raise DataLakeRootError(
            "availability reconcile failed before pending check: "
            f"{first['packet_id']}: {first['error']}"
        )
    return [
        item.raw_anchor
        for item in pickup(
            data_root,
            ack_namespace=_ACK_NAMESPACE,
            obligation_fn=lambda packet_id: _obligation(data_root, packet_id),
            source_family=_SOURCE_FAMILY,
            reconcile=False,
        )
    ]


def run_catchup(
    *, data_root: DataLakeRoot, packet_ids: Sequence[str] | None = None
) -> list[dict[str, Any]]:
    return run_tiktok_grid_observations(data_root=data_root, packet_ids=packet_ids)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", default=None)
    parser.add_argument("--packet-id", action="append", dest="packet_ids")
    args = parser.parse_args(argv)
    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
        results = run_catchup(data_root=data_root, packet_ids=args.packet_ids)
    except DataLakeRootError as exc:
        parser.exit(status=2, message=f"data lake unavailable: {exc}\n")
    print(json.dumps(results, indent=2, sort_keys=True))
    # Allowlist exit semantics (matching the catch-up siblings): any unexpected
    # status -- including availability_reconcile_failed -- fails the exit code.
    return 0 if all(row.get("status") in {"derived", "not_applicable", "already_current"} for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
