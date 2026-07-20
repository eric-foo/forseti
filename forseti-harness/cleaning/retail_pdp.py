"""Retail/PDP content adaptation owned by Cleaning."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from cleaning.content import cleaning_input_handles_from_content_rows
from cleaning.legacy import cleaning_handles_from_legacy_rows, decode_retail_pdp_raw
from cleaning.models import CleaningInputHandle
from source_capture.models import SourceCapturePacket
from source_capture.retail_pdp_content import load_retail_pdp_content_record

RETAIL_PDP_CLEANING_HANDLE_PREFIX = "cleaning:retail_pdp"


@dataclass(frozen=True)
class RetailPdpCleaningInput:
    """Validated rows and source anchors entering Retail Silver."""

    packet_id: str
    rows: list[Any]
    handles: list[CleaningInputHandle]
    residuals: list[str]
    content_schema_version: str | None
    extractor_version: str | None
    legacy_input: bool

    @property
    def handle_by_row_id(self) -> dict[str, CleaningInputHandle]:
        return {
            handle.source_row_id: handle
            for handle in self.handles
            if handle.source_row_id is not None
        }


def build_retail_pdp_cleaning_input(
    *,
    packet: SourceCapturePacket,
    file_bytes_by_file_id: Mapping[str, bytes],
) -> RetailPdpCleaningInput:
    """Prefer canonical content; use the read-only raw decoder for history."""
    loaded = load_retail_pdp_content_record(
        packet=packet, file_bytes_by_file_id=file_bytes_by_file_id
    )
    if loaded is not None:
        content_file, record = loaded
        handles = cleaning_input_handles_from_content_rows(
            packet=packet,
            content_file=content_file,
            source_family=packet.source_family,
            source_surface=packet.source_surface,
            rows=record.rows,
            handle_id_prefix=RETAIL_PDP_CLEANING_HANDLE_PREFIX,
        )
        return RetailPdpCleaningInput(
            packet_id=packet.packet_id,
            rows=list(record.rows),
            handles=handles,
            residuals=list(record.residuals),
            content_schema_version=record.schema_version,
            extractor_version=record.parser_version,
            legacy_input=False,
        )

    legacy = decode_retail_pdp_raw(
        packet=packet, file_bytes_by_file_id=file_bytes_by_file_id
    )
    handles = cleaning_handles_from_legacy_rows(
        source_family=packet.source_family,
        source_surface=packet.source_surface,
        packet_id=packet.packet_id,
        rows=legacy.rows,
        handle_id_prefix=RETAIL_PDP_CLEANING_HANDLE_PREFIX,
    )
    return RetailPdpCleaningInput(
        packet_id=packet.packet_id,
        rows=list(legacy.rows),
        handles=handles,
        residuals=list(legacy.residuals),
        content_schema_version=None,
        extractor_version=None,
        legacy_input=True,
    )


__all__ = [
    "RETAIL_PDP_CLEANING_HANDLE_PREFIX",
    "RetailPdpCleaningInput",
    "build_retail_pdp_cleaning_input",
]
