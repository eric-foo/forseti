"""Read-only creator-level TikTok comment coordination signal report.

The runner selects verified admitted batch packets, deduplicates recaptured
videos, and emits inspectable patterns. It never writes to the lake and never
claims that payment, astroturfing, common control, or deceptive intent occurred.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cleaning.tiktok_silver_analytics import comment_coordination_signals
from data_lake.root import DataLakeRoot
from harness_utils import hash_file
from source_capture.tiktok.batch_packet import TIKTOK_BATCH_CAPTURE_SURFACE


_BY_CREATOR_TABLE = Path(
    "indexes/derived_retrieval/silver_vault/core/query_tables/by_creator.json"
)
_BY_CREATOR_MANIFEST = Path(
    "indexes/derived_retrieval/silver_vault/core/manifests/by_creator.json"
)
_BATCH_FILENAME = "tiktok_batch_capture.json"


def _load_json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _normalized_creator(value: str) -> str:
    creator = value.strip().lstrip("@").lower()
    if not creator:
        raise ValueError("creator handle must be non-empty")
    return creator


def _map_packet_ids(
    root: DataLakeRoot, creator: str
) -> tuple[list[str], dict[str, Any]]:
    table_path = root.path / _BY_CREATOR_TABLE
    manifest_path = root.path / _BY_CREATOR_MANIFEST
    table = _load_json_object(table_path)
    creators = table.get("creators")
    if not isinstance(creators, Mapping):
        raise ValueError("by_creator query table lacks creators")
    tiktok = creators.get("tiktok")
    unspecified = tiktok.get("unspecified") if isinstance(tiktok, Mapping) else None
    if not isinstance(unspecified, Mapping):
        raise ValueError("by_creator query table lacks TikTok creator rows")
    matched = next(
        (value for key, value in unspecified.items() if str(key).lower() == creator),
        None,
    )
    if not isinstance(matched, Mapping):
        raise ValueError(
            f"creator @{creator} is absent from the current by_creator map; "
            "refresh the lake map or pass --packet-id"
        )
    packets = matched.get("packets")
    if not isinstance(packets, Mapping) or not packets:
        raise ValueError(f"creator @{creator} has no mapped packets")
    manifest = _load_json_object(manifest_path)
    return sorted(str(packet_id) for packet_id in packets), manifest


def _map_freshness(
    root: DataLakeRoot, manifest: Mapping[str, Any] | None
) -> dict[str, Any]:
    if not manifest:
        return {"posture": "unavailable", "reason": "by_creator manifest not loaded"}
    generated_at = str(manifest.get("generated_at") or "").strip()
    generated_timestamp: float | None = None
    try:
        generated_timestamp = datetime.fromisoformat(
            generated_at.replace("Z", "+00:00")
        ).astimezone(timezone.utc).timestamp()
    except (TypeError, ValueError):
        pass
    latest_availability_timestamp: float | None = None
    availability_dir = root.path / "indexes" / "availability"
    if availability_dir.is_dir():
        for path in availability_dir.glob("*.json"):
            try:
                modified = path.stat().st_mtime
            except OSError:
                continue
            latest_availability_timestamp = max(
                latest_availability_timestamp or modified,
                modified,
            )
    stale = (
        generated_timestamp is not None
        and latest_availability_timestamp is not None
        and latest_availability_timestamp > generated_timestamp
    )
    return {
        "posture": (
            "stale_by_newer_availability_entry" if stale else "not_proven_current"
        ),
        "generated_at": generated_at or None,
        "source_high_watermark": manifest.get("source_high_watermark"),
        "stale_if": manifest.get("stale_if"),
        "latest_availability_mtime_utc": (
            datetime.fromtimestamp(latest_availability_timestamp, timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
            if latest_availability_timestamp is not None
            else None
        ),
    }


def _load_batch_packet(
    root: DataLakeRoot,
    *,
    packet_id: str,
    creator: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    loaded = root.load_raw_packet(packet_id)
    if loaded.manifest.get("source_surface") != TIKTOK_BATCH_CAPTURE_SURFACE:
        raise ValueError(
            f"packet {packet_id} is not a TikTok creator batch packet: "
            f"{loaded.manifest.get('source_surface')!r}"
        )
    preserved = loaded.manifest.get("preserved_files")
    candidates = (
        [
            row
            for row in preserved
            if isinstance(row, Mapping)
            and str(row.get("relative_packet_path") or "").endswith(_BATCH_FILENAME)
        ]
        if isinstance(preserved, list)
        else []
    )
    if len(candidates) != 1:
        raise ValueError(
            f"packet {packet_id} must contain exactly one {_BATCH_FILENAME}; "
            f"found {len(candidates)}"
        )
    relative_path = str(candidates[0]["relative_packet_path"])
    payload = _load_json_object(loaded.container / relative_path)
    payload_creator = _normalized_creator(str(payload.get("creator_handle") or ""))
    if payload_creator != creator:
        raise ValueError(f"packet {packet_id} belongs to @{payload_creator}, not @{creator}")
    if (
        payload.get("platform") != "tiktok"
        or payload.get("source_surface") != TIKTOK_BATCH_CAPTURE_SURFACE
    ):
        raise ValueError(
            f"packet {packet_id} batch payload has the wrong platform or source surface"
        )
    return payload, {
        "packet_id": packet_id,
        "capture_timestamp": payload.get("capture_timestamp"),
        "video_count": len(payload.get("videos") or []),
        "relative_packet_path": relative_path,
        "manifest_sha256": hash_file(loaded.container / "manifest.json"),
        "payload_sha256": candidates[0].get("sha256"),
    }


def build_creator_coordination_report(
    root: DataLakeRoot,
    *,
    creator_handle: str,
    packet_ids: Sequence[str] | None = None,
) -> dict[str, Any]:
    creator = _normalized_creator(creator_handle)
    map_manifest: dict[str, Any] | None = None
    if packet_ids:
        selected_packet_ids = sorted(set(packet_ids))
        manifest_path = root.path / _BY_CREATOR_MANIFEST
        if manifest_path.is_file():
            map_manifest = _load_json_object(manifest_path)
        selection_source = "explicit_packet_ids"
    else:
        selected_packet_ids, map_manifest = _map_packet_ids(root, creator)
        selection_source = "by_creator_map"

    payloads: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for packet_id in selected_packet_ids:
        payloads.append(_load_batch_packet(root, packet_id=packet_id, creator=creator))
    analysis_videos: list[dict[str, Any]] = []
    packet_comment_count = 0
    for payload, receipt in payloads:
        videos = payload.get("videos")
        if not isinstance(videos, list):
            raise ValueError(f"packet {receipt['packet_id']} batch payload lacks videos")
        for video in videos:
            if not isinstance(video, Mapping):
                raise ValueError(
                    f"packet {receipt['packet_id']} contains a non-object video row"
                )
            video_id = str(video.get("video_id") or video.get("id") or "").strip()
            if not video_id:
                raise ValueError(
                    f"packet {receipt['packet_id']} contains a video without video_id"
                )
            comments = (
                video.get("comments")
                if isinstance(video.get("comments"), Mapping)
                else {}
            )
            packet_comment_count += len(comments.get("comments") or [])
            selected = dict(video)
            selected["_source_packet_id"] = receipt["packet_id"]
            analysis_videos.append(selected)

    analysis = comment_coordination_signals(analysis_videos)
    unique_video_count = len(
        {str(video.get("video_id") or video.get("id")) for video in analysis_videos}
    )
    return {
        "report_kind": "tiktok_creator_comment_coordination_signals",
        "creator_handle": creator,
        "platform": "tiktok",
        "selection": {
            "source": selection_source,
            "packet_ids": selected_packet_ids,
            "packet_count": len(selected_packet_ids),
            "packet_comment_row_count_before_video_deduplication": packet_comment_count,
            "analyzed_unique_video_count": unique_video_count,
            "map_freshness": _map_freshness(root, map_manifest),
        },
        "source_packets": [receipt for _payload, receipt in payloads],
        "analysis": analysis,
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Analyze source-backed TikTok creator comment coordination signals "
            "without making paid/astroturf verdicts."
        )
    )
    parser.add_argument(
        "--creator", required=True, help="TikTok creator handle, with or without @."
    )
    parser.add_argument(
        "--data-root",
        default=None,
        help="Forseti data lake root; defaults to FORSETI_DATA_ROOT.",
    )
    parser.add_argument(
        "--packet-id",
        action="append",
        default=[],
        help=(
            "Analyze an exact admitted packet; repeat for multiple packets. "
            "Otherwise uses by_creator."
        ),
    )
    parser.add_argument(
        "--output", type=Path, default=None, help="Optional local JSON report path."
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        root = DataLakeRoot.resolve(explicit=args.data_root)
        report = build_creator_coordination_report(
            root,
            creator_handle=args.creator,
            packet_ids=args.packet_id or None,
        )
        text = f"{json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True)}\n"
        if args.output is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8", newline="\n")
        print(text, end="")
    except Exception as exc:
        parser.exit(
            status=2,
            message=f"TikTok comment coordination analysis failed: {exc}\n",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
