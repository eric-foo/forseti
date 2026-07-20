"""Retail/PDP capture-time content extraction and validation.

Retailer schemas and extractors remain family-owned.  The historical
``retail_pdp_projection`` module still houses the DOM parsers so old raw
packets remain readable; current capture and Cleaning import this content
boundary and never persist or require a Projection record.
"""

from __future__ import annotations

import json
from typing import Any, Mapping

from source_capture.models import PreservedFile, SourceCapturePacket
from source_capture.retail_pdp_projection import (
    LUCKYSCENT_PDP_CONTENT_PROFILE,
    LUCKYSCENT_PDP_CONTENT_RECORD_KIND,
    LUCKYSCENT_PDP_PARSER_VERSION,
    NORDSTROM_PDP_CONTENT_PROFILE,
    NORDSTROM_PDP_CONTENT_RECORD_KIND,
    NORDSTROM_PDP_PARSER_VERSION,
    SEPHORA_PDP_CONTENT_PROFILE,
    SEPHORA_PDP_CONTENT_RECORD_KIND,
    SEPHORA_PDP_PARSER_VERSION,
    ULTA_PDP_CONTENT_PROFILE,
    ULTA_PDP_CONTENT_RECORD_KIND,
    ULTA_PDP_PARSER_VERSION,
    LuckyscentPdpAggregateContentRecord,
    NordstromPdpAggregateContentRecord,
    SephoraPdpAggregateContentRecord,
    UltaPdpAggregateContentRecord,
    build_luckyscent_pdp_aggregate_content_record,
    build_nordstrom_pdp_aggregate_content_record,
    build_sephora_pdp_aggregate_content_record,
    build_ulta_pdp_aggregate_content_record,
)

_RECORD_MODEL_BY_KIND = {
    SEPHORA_PDP_CONTENT_RECORD_KIND: SephoraPdpAggregateContentRecord,
    LUCKYSCENT_PDP_CONTENT_RECORD_KIND: LuckyscentPdpAggregateContentRecord,
    NORDSTROM_PDP_CONTENT_RECORD_KIND: NordstromPdpAggregateContentRecord,
    ULTA_PDP_CONTENT_RECORD_KIND: UltaPdpAggregateContentRecord,
}
_EXPECTED_VERSION_BY_PROFILE = {
    SEPHORA_PDP_CONTENT_PROFILE: SEPHORA_PDP_PARSER_VERSION,
    LUCKYSCENT_PDP_CONTENT_PROFILE: LUCKYSCENT_PDP_PARSER_VERSION,
    NORDSTROM_PDP_CONTENT_PROFILE: NORDSTROM_PDP_PARSER_VERSION,
    ULTA_PDP_CONTENT_PROFILE: ULTA_PDP_PARSER_VERSION,
}


def load_retail_pdp_content_record(
    *,
    packet: SourceCapturePacket,
    file_bytes_by_file_id: Mapping[str, bytes],
) -> tuple[PreservedFile, Any] | None:
    """Validate and load one current or historical retained content record."""
    content_matches = _matches(packet, "content_record.json")
    if not content_matches:
        return None
    if len(content_matches) != 1:
        raise ValueError(
            "Retail/PDP packet must preserve exactly one content_record.json"
        )
    content_file = content_matches[0]
    payload = _json_object(
        file_bytes_by_file_id, content_file, "content_record.json"
    )
    record_kind = payload.get("record_kind")
    model = _RECORD_MODEL_BY_KIND.get(record_kind)
    if model is None:
        raise ValueError(f"unsupported Retail/PDP content record kind: {record_kind!r}")
    record = model.model_validate(payload)
    if packet.source_locator.value != record.source_url:
        raise ValueError("Retail/PDP content record source_url does not match packet")

    profile = record.capture_profile
    expected_version = _EXPECTED_VERSION_BY_PROFILE[profile]
    current_metadata = _matches(packet, "content_extraction_metadata.json")
    if current_metadata:
        if len(current_metadata) != 1:
            raise ValueError(
                "Retail/PDP packet must preserve exactly one content_extraction_metadata.json"
            )
        metadata = _json_object(
            file_bytes_by_file_id,
            current_metadata[0],
            "content_extraction_metadata.json",
        )
        if metadata.get("extractor_version") != expected_version:
            raise ValueError("Retail/PDP extractor version does not match content record")
        if metadata.get("extraction_status") != "succeeded":
            raise ValueError("Retail/PDP content extraction did not succeed")
        if metadata.get("retention_outcome") != "content":
            raise ValueError("Retail/PDP content packet did not retain canonical content")
    else:
        legacy = _one(packet, "content_capture_metadata.json")
        metadata = _json_object(
            file_bytes_by_file_id, legacy, "content_capture_metadata.json"
        )
        if metadata.get("parser_version") != record.parser_version:
            raise ValueError("legacy Retail/PDP parser version does not match record")
        if metadata.get("projection_status") != "succeeded":
            raise ValueError("legacy Retail/PDP content projection did not succeed")
        if metadata.get("capture_artifact_mode") not in {"content", "sample"}:
            raise ValueError("legacy Retail/PDP content packet mode is invalid")

    browser_metadata_file = _one(packet, "cloakbrowser_snapshot_metadata.json")
    browser_metadata = _json_object(
        file_bytes_by_file_id,
        browser_metadata_file,
        "cloakbrowser_snapshot_metadata.json",
    )
    captured_profile = browser_metadata.get("retail_capture_profile")
    if (
        not isinstance(captured_profile, dict)
        or captured_profile.get("name") != profile
    ):
        raise ValueError("Retail/PDP capture profile does not match content record")
    if browser_metadata.get("pin_confirmed") is not True:
        raise ValueError("Retail/PDP content packet has no confirmed storefront pin")
    return content_file, record


def _matches(packet: SourceCapturePacket, filename: str) -> list[PreservedFile]:
    return [
        item
        for item in packet.preserved_files
        if item.relative_packet_path.replace("\\", "/").endswith(filename)
    ]


def _one(packet: SourceCapturePacket, filename: str) -> PreservedFile:
    matches = _matches(packet, filename)
    if len(matches) != 1:
        raise ValueError(f"Retail/PDP packet must preserve exactly one {filename}")
    return matches[0]


def _json_object(
    bodies: Mapping[str, bytes], preserved_file: PreservedFile, filename: str
) -> dict[str, Any]:
    body = bodies.get(preserved_file.file_id)
    if body is None:
        raise ValueError(f"preserved bytes are required for {filename}")
    try:
        value = json.loads(body)
    except Exception as exc:
        raise ValueError(f"invalid {filename}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{filename} must contain a JSON object")
    return value


__all__ = [
    "LUCKYSCENT_PDP_CONTENT_PROFILE",
    "LUCKYSCENT_PDP_PARSER_VERSION",
    "NORDSTROM_PDP_CONTENT_PROFILE",
    "NORDSTROM_PDP_PARSER_VERSION",
    "SEPHORA_PDP_CONTENT_PROFILE",
    "SEPHORA_PDP_PARSER_VERSION",
    "ULTA_PDP_CONTENT_PROFILE",
    "ULTA_PDP_PARSER_VERSION",
    "build_luckyscent_pdp_aggregate_content_record",
    "build_nordstrom_pdp_aggregate_content_record",
    "build_sephora_pdp_aggregate_content_record",
    "build_ulta_pdp_aggregate_content_record",
    "load_retail_pdp_content_record",
]
