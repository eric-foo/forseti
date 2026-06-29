"""Read-only lake adapter for IG Reels behavioral projection.

This module discovers already-persisted IG grid, deep-capture, standalone audio
ASR, and product-extraction records and feeds them into
``project_ig_reels_behavioral_item``. It does not acquire, render, transcribe,
extract, or write unless the caller explicitly opts into rebuilding the
availability index.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from cleaning.transcript_product_lake import (
    PRODUCT_MENTIONS_LANE,
    PRODUCT_MENTIONS_SET_LANE,
)
from source_capture.ig_reels_behavioral_projection import project_ig_reels_behavioral_item
from source_capture.ig_reels_deep_capture_lake import (
    AUDIENCE_COMMENTS_LANE,
    DEEP_CAPTURE_SET_LANE,
    REEL_TRANSCRIPT_LANE,
)
from source_capture.ig_reels_grid_projection import build_ig_reels_grid_projection
from source_capture.models import SourceCapturePacket

IG_REELS_BEHAVIORAL_LAKE_ADAPTER_METHOD = "ig_reels_behavioral_lake_adapter"
IG_REELS_BEHAVIORAL_LAKE_ADAPTER_VERSION = "v0"

_IG_SOURCE_FAMILY = "instagram_creator"
_IG_AUDIO_SURFACE = "ig_reels_audio"
_IG_GRID_SURFACE = "ig_reels_grid_dom_passive_json"
_ASR_LANE = "transcript_asr"
_PRODUCT_MENTIONS_LANE = PRODUCT_MENTIONS_LANE
_PRODUCT_MENTIONS_SET_LANE = PRODUCT_MENTIONS_SET_LANE


@dataclass
class _BehavioralInputs:
    grid_rows: list[dict[str, Any]] = field(default_factory=list)
    comment_sets: list[dict[str, Any]] = field(default_factory=list)
    standalone_audio_transcript_records: list[dict[str, Any]] = field(default_factory=list)
    deep_capture_transcript_records: list[dict[str, Any]] = field(default_factory=list)
    extraction_results: list[dict[str, Any]] = field(default_factory=list)
    adapter_residuals: list[str] = field(default_factory=list)


def project_ig_reels_behavioral_item_from_lake(
    *,
    data_root: Any,
    platform_item_id: str,
    rebuild_availability: bool = False,
) -> dict[str, Any]:
    """Project one IG Reel behavioral item from already-persisted lake records."""
    index = _collect_ig_reels_behavioral_inputs(
        data_root=data_root,
        target_shortcodes=(platform_item_id,),
        rebuild_availability=rebuild_availability,
    )
    return _project_from_inputs(
        platform_item_id,
        index.get(platform_item_id, _BehavioralInputs()),
        rebuild_availability=rebuild_availability,
    )


def project_ig_reels_behavioral_index_from_lake(
    *,
    data_root: Any,
    platform_item_ids: Sequence[str] | None = None,
    rebuild_availability: bool = False,
) -> dict[str, dict[str, Any]]:
    """Project every discovered or requested IG Reel into a shortcode-keyed index."""
    targets = tuple(platform_item_ids or ())
    index = _collect_ig_reels_behavioral_inputs(
        data_root=data_root,
        target_shortcodes=targets,
        rebuild_availability=rebuild_availability,
    )
    shortcodes = sorted(set(targets) if targets else index)
    return {
        shortcode: _project_from_inputs(
            shortcode,
            index.get(shortcode, _BehavioralInputs()),
            rebuild_availability=rebuild_availability,
        )
        for shortcode in shortcodes
    }


def _collect_ig_reels_behavioral_inputs(
    *,
    data_root: Any,
    target_shortcodes: Sequence[str],
    rebuild_availability: bool,
) -> dict[str, _BehavioralInputs]:
    if rebuild_availability:
        data_root.rebuild_availability()

    index: dict[str, _BehavioralInputs] = {}
    global_residuals: list[str] = []
    _collect_packet_backed_inputs(data_root, index, global_residuals)
    _collect_deep_capture_inputs(data_root, index)
    _collect_product_extraction_results(data_root, index, global_residuals)

    for shortcode in target_shortcodes:
        index.setdefault(shortcode, _BehavioralInputs())
    _append_global_residuals_to_index(index, target_shortcodes, global_residuals)
    return index


def _collect_packet_backed_inputs(
    data_root: Any,
    index: dict[str, _BehavioralInputs],
    global_residuals: list[str],
) -> None:
    for packet_id in data_root.list_available(source_family=_IG_SOURCE_FAMILY):
        try:
            loaded = data_root.load_raw_packet(packet_id)
        except Exception:  # noqa: BLE001 - preserve target-visible discovery failure below
            _append_once(global_residuals, f"ig_lake_raw_packet_discovery_failed:{packet_id}")
            continue
        manifest = loaded.manifest
        surface = manifest.get("source_surface")
        if surface == _IG_AUDIO_SURFACE:
            _collect_audio_packet_inputs(data_root, packet_id, loaded, index, global_residuals)
        elif surface == _IG_GRID_SURFACE:
            _collect_grid_packet_inputs(packet_id, loaded, index, global_residuals)


def _collect_audio_packet_inputs(
    data_root: Any,
    packet_id: str,
    loaded: Any,
    index: dict[str, _BehavioralInputs],
    global_residuals: list[str],
) -> None:
    meta = _capture_metadata(loaded)
    meta_shortcode = _string_or_none(meta.get("platform_shortcode"))
    for record_id, record in _json_records_in_lane(data_root, raw_anchor=packet_id, lane=_ASR_LANE):
        if record is None:
            residual = f"ig_lake_asr_record_unreadable:{packet_id}:{record_id}"
            if meta_shortcode is None:
                _append_once(global_residuals, residual)
            else:
                _append_adapter_residual(index, meta_shortcode, residual)
            continue
        record.setdefault("record_id", record_id)
        record.setdefault("transcript_anchor", packet_id)
        if meta_shortcode is not None:
            record.setdefault("shortcode", meta_shortcode)
            record.setdefault("video_id", meta_shortcode)
        provenance = _mapping_or_empty(record.get("provenance"))
        provenance.setdefault("source_packet_id", packet_id)
        record["provenance"] = provenance
        shortcode = _string_or_none(record.get("shortcode")) or _string_or_none(record.get("video_id"))
        if shortcode is None:
            _append_once(global_residuals, f"ig_lake_asr_record_shortcode_absent:{packet_id}:{record_id}")
            continue
        index.setdefault(shortcode, _BehavioralInputs()).standalone_audio_transcript_records.append(record)


def _collect_grid_packet_inputs(
    packet_id: str,
    loaded: Any,
    index: dict[str, _BehavioralInputs],
    global_residuals: list[str],
) -> None:
    try:
        packet = SourceCapturePacket.model_validate(loaded.manifest)
        projection = build_ig_reels_grid_projection(
            packet=packet,
            raw_file_bytes_by_file_id=loaded.bodies,
        )
    except Exception:  # noqa: BLE001 - preserve target-visible grid projection failure below
        _append_once(global_residuals, f"ig_lake_grid_projection_failed:{packet_id}")
        return
    for row in projection.rows:
        row_data = _model_dump(row)
        shortcode = _string_or_none(row_data.get("content_shortcode"))
        if shortcode is None:
            continue
        index.setdefault(shortcode, _BehavioralInputs()).grid_rows.append(row_data)


def _collect_deep_capture_inputs(data_root: Any, index: dict[str, _BehavioralInputs]) -> None:
    for shortcode, record_id, _marker in _iter_derived_lane_records(data_root, DEEP_CAPTURE_SET_LANE):
        bucket = index.setdefault(shortcode, _BehavioralInputs())
        try:
            complete = data_root.is_record_set_complete(
                subtree="derived",
                raw_anchor=shortcode,
                record_id=record_id,
                completion_lane=DEEP_CAPTURE_SET_LANE,
            )
        except Exception:  # noqa: BLE001 - preserve target-visible failure without aborting index
            complete = False
        if not complete:
            _append_once(bucket.adapter_residuals, f"ig_deep_capture_record_set_incomplete:{shortcode}:{record_id}")
            continue

        comment_record = _read_derived_json_record(
            data_root,
            raw_anchor=shortcode,
            lane=AUDIENCE_COMMENTS_LANE,
            record_id=record_id,
        )
        transcript_record = _read_derived_json_record(
            data_root,
            raw_anchor=shortcode,
            lane=REEL_TRANSCRIPT_LANE,
            record_id=record_id,
        )
        if comment_record is None:
            _append_once(bucket.adapter_residuals, f"ig_deep_capture_comment_record_unreadable:{shortcode}:{record_id}")
        else:
            comment_record.setdefault("record_id", record_id)
            bucket.comment_sets.append(comment_record)
        if transcript_record is None:
            _append_once(bucket.adapter_residuals, f"ig_deep_capture_transcript_record_unreadable:{shortcode}:{record_id}")
        else:
            transcript_record.setdefault("record_id", record_id)
            bucket.deep_capture_transcript_records.append(transcript_record)


def _collect_product_extraction_results(
    data_root: Any,
    index: dict[str, _BehavioralInputs],
    global_residuals: list[str],
) -> None:
    for anchor, record_id, record_path in _iter_derived_lane_records(data_root, _PRODUCT_MENTIONS_LANE):
        body = _read_json_file(record_path)
        if not isinstance(body, dict):
            _append_once(global_residuals, f"ig_lake_product_mentions_record_unreadable:{anchor}:{record_id}")
            continue
        shortcode = _string_or_none(body.get("video_id")) or _string_or_none(body.get("shortcode"))
        if shortcode is None:
            _append_once(global_residuals, f"ig_lake_product_mentions_record_video_id_absent:{anchor}:{record_id}")
            continue
        try:
            complete = data_root.is_record_set_complete(
                subtree="derived",
                raw_anchor=anchor,
                record_id=record_id,
                completion_lane=_PRODUCT_MENTIONS_SET_LANE,
            )
        except Exception:  # noqa: BLE001
            complete = False
        status = "extracted" if complete else "partial_needs_cleanup"
        index.setdefault(shortcode, _BehavioralInputs()).extraction_results.append(
            {
                "anchor": anchor,
                "video_id": shortcode,
                "status": status,
                "path": str(record_path),
                "transcript_source_key": _string_or_none(body.get("transcript_source_key")),
                "source_key": _string_or_none(body.get("source_key")),
                "source_route": _string_or_none(body.get("source_route")),
                "asr_record_id": _string_or_none(body.get("asr_record_id")),
            }
        )


def _project_from_inputs(
    shortcode: str,
    inputs: _BehavioralInputs,
    *,
    rebuild_availability: bool,
) -> dict[str, Any]:
    projection = project_ig_reels_behavioral_item(
        platform_item_id=shortcode,
        grid_rows=inputs.grid_rows,
        comment_sets=inputs.comment_sets,
        standalone_audio_transcript_records=inputs.standalone_audio_transcript_records,
        deep_capture_transcript_records=inputs.deep_capture_transcript_records,
        extraction_results=inputs.extraction_results,
    )
    if inputs.adapter_residuals:
        residuals = projection["behavioral_completeness"]["residuals"]
        for residual in inputs.adapter_residuals:
            _append_once(residuals, residual)
        if projection["behavioral_completeness"]["status"] == "complete":
            projection["behavioral_completeness"]["status"] = "complete_with_residuals"
            projection["behavioral_completeness"]["complete"] = False
            projection["transcript"]["extraction_rollup"]["status"] = "complete_with_residuals"
            projection["extraction"]["rollup"]["status"] = "complete_with_residuals"
    projection["lake_adapter"] = {
        "adapter_method": IG_REELS_BEHAVIORAL_LAKE_ADAPTER_METHOD,
        "adapter_version": IG_REELS_BEHAVIORAL_LAKE_ADAPTER_VERSION,
        "rebuild_availability": rebuild_availability,
    }
    return projection


def _append_adapter_residual(index: dict[str, _BehavioralInputs], shortcode: str, residual: str) -> None:
    _append_once(index.setdefault(shortcode, _BehavioralInputs()).adapter_residuals, residual)


def _append_global_residuals_to_index(
    index: dict[str, _BehavioralInputs],
    target_shortcodes: Sequence[str],
    residuals: Sequence[str],
) -> None:
    if not residuals:
        return
    shortcodes = tuple(target_shortcodes) or tuple(index)
    for shortcode in shortcodes:
        bucket = index.setdefault(shortcode, _BehavioralInputs())
        for residual in residuals:
            _append_once(bucket.adapter_residuals, residual)


def _capture_metadata(loaded: Any) -> dict[str, Any]:
    files = _file_paths(loaded.manifest)
    body = _body_ending_with(loaded, files, "capture_metadata.json")
    if body is None:
        return {}
    parsed = _loads_json_bytes(body)
    return parsed if isinstance(parsed, dict) else {}


def _json_records_in_lane(data_root: Any, *, raw_anchor: str, lane: str) -> list[tuple[str, dict[str, Any] | None]]:
    lane_dir = data_root.lane_dir(subtree="derived", raw_anchor=raw_anchor, lane=lane)
    if not lane_dir.is_dir():
        return []
    out: list[tuple[str, dict[str, Any] | None]] = []
    for record_file in sorted(lane_dir.iterdir()):
        if not record_file.is_file():
            continue
        body = _read_json_file(record_file)
        out.append((record_file.name, dict(body) if isinstance(body, dict) else None))
    return out


def _read_derived_json_record(
    data_root: Any,
    *,
    raw_anchor: str,
    lane: str,
    record_id: str,
) -> dict[str, Any] | None:
    path = data_root.record_path(
        subtree="derived",
        raw_anchor=raw_anchor,
        lane=lane,
        record_id=record_id,
    )
    body = _read_json_file(path)
    return dict(body) if isinstance(body, dict) else None


def _iter_derived_lane_records(data_root: Any, lane: str) -> Iterable[tuple[str, str, Path]]:
    derived = data_root.path / "derived"
    if not derived.is_dir():
        return
    for shard_dir in sorted(derived.iterdir()):
        if not shard_dir.is_dir():
            continue
        for anchor_dir in sorted(shard_dir.iterdir()):
            if not anchor_dir.is_dir():
                continue
            lane_dir = anchor_dir / lane
            if not lane_dir.is_dir():
                continue
            for record_file in sorted(lane_dir.iterdir()):
                if record_file.is_file():
                    yield anchor_dir.name, record_file.name, record_file


def _file_paths(manifest: Mapping[str, Any]) -> dict[str, str]:
    return {
        item.get("file_id", ""): item.get("relative_packet_path", "")
        for item in _list(manifest.get("preserved_files"))
        if isinstance(item, dict)
    }


def _body_ending_with(loaded: Any, files: Mapping[str, str], suffix: str) -> bytes | None:
    for file_id, path in files.items():
        if path.endswith(suffix):
            return loaded.bodies.get(file_id)
    return None


def _read_json_file(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _loads_json_bytes(body: bytes) -> Any:
    try:
        return json.loads(body.decode("utf-8"))
    except ValueError:
        return None


def _model_dump(value: Any) -> dict[str, Any]:
    dump = getattr(value, "model_dump", None)
    if dump is not None:
        return dump(mode="json")
    return dict(value)


def _mapping_or_empty(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _string_or_none(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _append_once(items: list[str], item: str) -> None:
    if item not in items:
        items.append(item)


__all__ = [
    "IG_REELS_BEHAVIORAL_LAKE_ADAPTER_METHOD",
    "IG_REELS_BEHAVIORAL_LAKE_ADAPTER_VERSION",
    "project_ig_reels_behavioral_index_from_lake",
    "project_ig_reels_behavioral_item_from_lake",
]
