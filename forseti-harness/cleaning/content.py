"""Internal adaptation from canonical content records into Cleaning handles."""

from __future__ import annotations

from collections.abc import Iterable
import json
from typing import Any, Mapping, TypeVar

from cleaning.models import CleaningInputHandle, CleaningSourceAnchor
from source_capture.models import PreservedFile, SourceCapturePacket

_RecordT = TypeVar("_RecordT")


def load_validated_content_record(
    *,
    packet: SourceCapturePacket,
    file_bytes_by_file_id: Mapping[str, bytes],
    record_model: type[_RecordT],
    family_label: str,
) -> tuple[PreservedFile, _RecordT] | None:
    """Load the one canonical content record, or return ``None`` for legacy raw."""
    matches = [
        item
        for item in packet.preserved_files
        if item.relative_packet_path.replace("\\", "/").endswith(
            "content_record.json"
        )
    ]
    if not matches:
        return None
    if len(matches) != 1:
        raise ValueError(
            f"{family_label} packet must preserve exactly one content_record.json"
        )
    content_file = matches[0]
    body = file_bytes_by_file_id.get(content_file.file_id)
    if body is None:
        raise ValueError(
            f"content record bytes are required for preserved file id: "
            f"{content_file.file_id}"
        )
    try:
        loaded = json.loads(body.decode("utf-8"))
        record = record_model.model_validate(loaded)  # type: ignore[attr-defined]
    except Exception as exc:
        raise ValueError(f"invalid {family_label} content record: {exc}") from exc
    source_url = getattr(record, "source_url", None)
    if packet.source_locator.value != source_url:
        raise ValueError(
            f"{family_label} content record source_url {source_url!r} does not match "
            f"packet source locator {packet.source_locator.value!r}"
        )
    return content_file, record


def cleaning_input_handles_from_content_rows(
    *,
    packet: SourceCapturePacket,
    content_file: PreservedFile,
    source_family: str,
    source_surface: str,
    rows: Iterable[Any],
    handle_id_prefix: str,
) -> list[CleaningInputHandle]:
    """Bind canonical content rows to their packet-local JSON pointers."""
    slice_by_id = {item.slice_id: item for item in packet.source_slices}
    handles: list[CleaningInputHandle] = []
    for index, row in enumerate(rows):
        slice_id = _required_str(row, "slice_id", owner="content row")
        source_slice = slice_by_id.get(slice_id)
        if source_slice is None:
            raise ValueError(f"content row references unknown source slice: {slice_id}")
        if content_file.file_id not in source_slice.preserved_file_ids:
            raise ValueError(
                f"content row slice {slice_id!r} does not reference content_record.json"
            )
        row_id = _required_str(row, "row_id", owner="content row")
        row_kind = _required_str(row, "row_kind", owner="content row")
        handles.append(
            CleaningInputHandle(
                handle_id=f"{handle_id_prefix}:{row_id}",
                source_family=source_family,
                source_surface=source_surface,
                source_anchor=CleaningSourceAnchor(
                    packet_id=packet.packet_id,
                    slice_id=slice_id,
                    file_id=content_file.file_id,
                    relative_packet_path=content_file.relative_packet_path,
                    sha256=content_file.sha256,
                    hash_basis=content_file.hash_basis,
                    anchor_kind="json_pointer",
                    json_pointer=f"/rows/{index}",
                ),
                source_row_id=row_id,
                source_row_kind=row_kind,
                residuals=sorted(set(getattr(row, "residuals", []) or [])),
            )
        )
    return handles


def _required_str(value: Any, field: str, *, owner: str) -> str:
    item = getattr(value, field, None)
    if not isinstance(item, str) or not item.strip():
        raise ValueError(f"{owner}.{field} must be a non-empty string")
    return item


__all__ = [
    "cleaning_input_handles_from_content_rows",
    "load_validated_content_record",
]
