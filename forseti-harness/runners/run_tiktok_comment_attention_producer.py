"""Append TikTok comment-like/video-like ratio observations to Silver.

The runner consumes committed TikTok batch-admission packets through the lake
consumption seam.  It is idempotent under a policy-fingerprinted deterministic
record id and makes no relevance, credibility, or prioritization judgment.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.tiktok_comment_attention_producer import (
    COMMENT_ATTENTION_LANE,
    COMMENT_ATTENTION_POLICY_FINGERPRINT,
    derive_comment_attention_silver_records,
)
from data_lake.consumption import append_ack, is_acknowledged, pickup, reconcile_availability_per_packet
from data_lake.root import DataLakeRoot, DataLakeRootError
from source_capture.tiktok.batch_packet import (
    TIKTOK_BATCH_CAPTURE_JSON_NAME,
    TIKTOK_BATCH_CAPTURE_SURFACE,
)

_ACK_NAMESPACE = COMMENT_ATTENTION_LANE
_SOURCE_FAMILY = "tiktok"


def _obligation(data_root: DataLakeRoot, packet_id: str) -> dict[str, Any]:
    availability = data_root.read_availability(packet_id) or {}
    return {
        "obligation_schema": 1,
        "consumer": "tiktok_comment_attention_producer",
        "policy_fingerprint_sha256": COMMENT_ATTENTION_POLICY_FINGERPRINT,
        "manifest_sha256": str(availability.get("manifest_sha256") or "missing"),
    }


def _batch_payload(
    data_root: DataLakeRoot, packet_id: str
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    loaded = data_root.load_raw_packet(packet_id)
    manifest = loaded.manifest
    if manifest.get("source_surface") != TIKTOK_BATCH_CAPTURE_SURFACE:
        return None
    matches = [
        item
        for item in manifest.get("preserved_files", [])
        if isinstance(item, Mapping)
        and str(item.get("relative_packet_path") or "").endswith(TIKTOK_BATCH_CAPTURE_JSON_NAME)
    ]
    if len(matches) != 1:
        raise ValueError(f"packet {packet_id} requires exactly one preserved TikTok batch JSON")
    preserved = dict(matches[0])
    file_id = str(preserved.get("file_id") or "")
    body = loaded.bodies.get(file_id)
    if body is None:
        raise ValueError(f"packet {packet_id} TikTok batch body is absent")
    payload = json.loads(body.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"packet {packet_id} TikTok batch body must be a JSON object")
    return payload, {
        "file_id": file_id,
        "relative_packet_path": preserved.get("relative_packet_path"),
        "sha256": preserved.get("sha256"),
        "hash_basis": "raw_stored_bytes",
    }


def run_comment_attention(
    *,
    data_root: DataLakeRoot,
    packet_ids: Sequence[str] | None = None,
    scope_packet_ids: Sequence[str] | None = None,
    reconcile_availability: bool = True,
) -> list[dict[str, Any]]:
    if packet_ids is not None and scope_packet_ids is not None:
        raise ValueError("packet_ids and scope_packet_ids cannot be combined")
    results: list[dict[str, Any]] = []
    if reconcile_availability:
        results.extend(
            reconcile_availability_per_packet(
                data_root,
                scope_packet_ids=(
                    scope_packet_ids if scope_packet_ids is not None else packet_ids
                ),
            )
        )
    requested = set(packet_ids or ())
    items = list(pickup(
        data_root,
        ack_namespace=_ACK_NAMESPACE,
        obligation_fn=lambda packet_id: _obligation(data_root, packet_id),
        source_family=_SOURCE_FAMILY,
        reconcile=False,
        scope_packet_ids=scope_packet_ids,
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
            batch_input = _batch_payload(data_root, packet_id)
            if batch_input is None:
                append_ack(
                    data_root,
                    raw_anchor=packet_id,
                    ack_namespace=_ACK_NAMESPACE,
                    obligation=item.obligation,
                    evidence=[
                        {
                            "kind": "not_applicable_non_batch_tiktok_packet",
                            "manifest_sha256": item.obligation["manifest_sha256"],
                            "policy_fingerprint_sha256": COMMENT_ATTENTION_POLICY_FINGERPRINT,
                        }
                    ],
                )
                results.append({"packet_id": packet_id, "status": "not_applicable"})
                continue
            payload, raw_file_ref = batch_input
            derived = derive_comment_attention_silver_records(
                data_root=data_root,
                raw_anchor=packet_id,
                batch_payload=payload,
                raw_file_ref=raw_file_ref,
            )
            evidence = [
                {
                    "kind": "silver_records_derived",
                    "lane": COMMENT_ATTENTION_LANE,
                    "record_count": len(derived.records),
                    "written_count": len(derived.paths),
                    "skipped_existing_count": len(derived.skipped_record_ids),
                    "policy_fingerprint_sha256": COMMENT_ATTENTION_POLICY_FINGERPRINT,
                }
            ]
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
                    "record_count": len(derived.records),
                    "written_count": len(derived.paths),
                    "skipped_existing_count": len(derived.skipped_record_ids),
                }
            )
        except Exception as exc:  # noqa: BLE001 - isolate one corrupt packet
            results.append(
                {
                    "packet_id": packet_id,
                    "status": "failed",
                    "error": f"{type(exc).__name__}: {exc}"[:300],
                }
            )
    return results


def pending_packets(
    *,
    data_root: DataLakeRoot,
    scope_packet_ids: Sequence[str] | None = None,
    reconcile_availability: bool = True,
) -> list[str]:
    """Compute-free pending surface for the seam cadence."""
    if reconcile_availability:
        failures = reconcile_availability_per_packet(
            data_root, scope_packet_ids=scope_packet_ids
        )
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
            scope_packet_ids=scope_packet_ids,
        )
    ]


def run_catchup(
    *,
    data_root: DataLakeRoot,
    packet_ids: Sequence[str] | None = None,
    scope_packet_ids: Sequence[str] | None = None,
    reconcile_availability: bool = True,
) -> list[dict[str, Any]]:
    return run_comment_attention(
        data_root=data_root,
        packet_ids=packet_ids,
        scope_packet_ids=scope_packet_ids,
        reconcile_availability=reconcile_availability,
    )


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
    return 0 if all(row.get("status") in {"derived", "not_applicable", "already_current"} for row in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
