"""Read-only adaptation for historical raw and Projection-era packets.

No current producer writes a Projection record. This module exists only so
historical packet bytes remain consumable while families migrate through the
same Cleaning outputs.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Literal, Mapping

from cleaning.models import CleaningInputHandle, CleaningSourceAnchor
from source_capture.models import SourceCapturePacket

_ANCHOR_KINDS = frozenset(
    {"file", "json_pointer", "html_selector", "script_index", "text_pattern"}
)


@dataclass(frozen=True)
class LegacyDecodedContent:
    """Family-neutral rows recovered from one historical raw packet."""

    packet_id: str
    rows: list[Any]
    residuals: list[str]


def decode_basenotes_raw(
    *, packet: SourceCapturePacket, file_bytes_by_file_id: Mapping[str, bytes]
) -> LegacyDecodedContent:
    from source_capture.basenotes_projection import build_basenotes_projection

    decoded = build_basenotes_projection(
        packet=packet, raw_file_bytes_by_file_id=file_bytes_by_file_id
    )
    return _decoded_content(decoded)


def decode_fragrantica_raw(
    *, packet: SourceCapturePacket, file_bytes_by_file_id: Mapping[str, bytes]
) -> LegacyDecodedContent:
    from source_capture.fragrantica_projection import build_fragrantica_projection

    decoded = build_fragrantica_projection(
        packet=packet, raw_file_bytes_by_file_id=file_bytes_by_file_id
    )
    return _decoded_content(decoded)


def decode_parfumo_raw(
    *, packet: SourceCapturePacket, file_bytes_by_file_id: Mapping[str, bytes]
) -> LegacyDecodedContent:
    from source_capture.parfumo_projection import build_parfumo_projection

    decoded = build_parfumo_projection(
        packet=packet, raw_file_bytes_by_file_id=file_bytes_by_file_id
    )
    return _decoded_content(decoded)


def decode_retail_pdp_raw(
    *, packet: SourceCapturePacket, file_bytes_by_file_id: Mapping[str, bytes]
) -> LegacyDecodedContent:
    from source_capture.retail_pdp_projection import build_retail_pdp_projection

    decoded = build_retail_pdp_projection(
        packet=packet, raw_file_bytes_by_file_id=file_bytes_by_file_id
    )
    return _decoded_content(decoded)


def _decoded_content(value: Any) -> LegacyDecodedContent:
    return LegacyDecodedContent(
        packet_id=_required_str(value, "packet_id", owner="historical decoder"),
        rows=list(getattr(value, "rows", [])),
        residuals=list(getattr(value, "residuals", [])),
    )


def cleaning_handles_from_legacy_rows(
    *,
    source_family: str,
    source_surface: str,
    packet_id: str,
    rows: Iterable[Any],
    handle_id_prefix: str,
) -> list[CleaningInputHandle]:
    """Adapt historical mechanical rows without carrying a Projection reference."""
    handles: list[CleaningInputHandle] = []
    for row in rows:
        raw_ref = _required_object(row, "raw_ref", owner="legacy row")
        anchor = _required_object(row, "raw_anchor", owner="legacy row")
        row_packet_id = _required_str(raw_ref, "packet_id", owner="legacy row raw_ref")
        if row_packet_id != packet_id:
            raise ValueError("legacy row packet id does not match requested packet")
        row_id = _required_str(row, "row_id", owner="legacy row")
        row_kind = _required_str(row, "row_kind", owner="legacy row")
        handles.append(
            CleaningInputHandle(
                handle_id=f"{handle_id_prefix}:{row_id}",
                source_family=source_family,
                source_surface=source_surface,
                source_anchor=_source_anchor(
                    packet_id=packet_id,
                    slice_id=_required_str(
                        raw_ref, "slice_id", owner="legacy row raw_ref"
                    ),
                    legacy_anchor=anchor,
                ),
                source_row_id=row_id,
                source_row_kind=row_kind,
                residuals=sorted(set(getattr(row, "residuals", []) or [])),
            )
        )
    return handles


def _source_anchor(
    *, packet_id: str, slice_id: str, legacy_anchor: Any
) -> CleaningSourceAnchor:
    anchor_kind = _anchor_kind(legacy_anchor)
    base = {
        "packet_id": packet_id,
        "slice_id": slice_id,
        "file_id": _required_str(legacy_anchor, "file_id", owner="legacy anchor"),
        "relative_packet_path": _required_str(
            legacy_anchor, "relative_packet_path", owner="legacy anchor"
        ),
        "sha256": _required_str(legacy_anchor, "sha256", owner="legacy anchor"),
        "hash_basis": _required_str(
            legacy_anchor, "hash_basis", owner="legacy anchor"
        ),
    }
    if anchor_kind == "json_pointer":
        pointer = getattr(legacy_anchor, "json_pointer", None) or getattr(
            legacy_anchor, "anchor_value", None
        )
        return CleaningSourceAnchor(
            **base,
            anchor_kind="json_pointer",
            json_pointer=_non_empty(pointer, "legacy anchor.json_pointer"),
        )
    if anchor_kind == "file":
        return CleaningSourceAnchor(**base)
    return CleaningSourceAnchor(
        **base,
        anchor_kind=anchor_kind,
        anchor_value=_non_empty(
            getattr(legacy_anchor, "anchor_value", None),
            "legacy anchor.anchor_value",
        ),
    )


def _anchor_kind(
    anchor: Any,
) -> Literal["file", "json_pointer", "html_selector", "script_index", "text_pattern"]:
    value = getattr(anchor, "anchor_kind", None)
    if value is None:
        return "json_pointer" if getattr(anchor, "json_pointer", None) else "file"
    if value not in _ANCHOR_KINDS:
        raise ValueError(f"unsupported historical anchor kind: {value!r}")
    return value


def _required_object(value: Any, field: str, *, owner: str) -> Any:
    item = getattr(value, field, None)
    if item is None:
        raise ValueError(f"{owner}.{field} is required")
    return item


def _required_str(value: Any, field: str, *, owner: str) -> str:
    return _non_empty(getattr(value, field, None), f"{owner}.{field}")


def _non_empty(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value


__all__ = [
    "LegacyDecodedContent",
    "cleaning_handles_from_legacy_rows",
    "decode_basenotes_raw",
    "decode_fragrantica_raw",
    "decode_parfumo_raw",
    "decode_retail_pdp_raw",
]
