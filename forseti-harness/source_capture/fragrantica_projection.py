from __future__ import annotations

import html
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Mapping

from pydantic import Field, field_validator, model_validator

from harness_utils import generate_ulid
from schemas.case_models import StrictModel
from source_capture.models import PreservedFile, SourceCapturePacket, SourceCaptureSlice
from source_capture.projection_shared import (
    dedupe_preserve_order as _dedupe_preserve_order,
    first_match as _first_match,
    is_forbidden_field_pattern_match,
    normalized_html_text as _text,
    read_packet_directory as _read_packet_directory,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


FRAGRANTICA_PROJECTION_METHOD = "fragrantica_current_window_mechanical_projection"
FRAGRANTICA_PROJECTION_VERSION = "v1"
FRAGRANTICA_PROJECTION_CERTIFICATION = (
    "view_only; not_cleaned; not_normalized; not_judgment_ready"
)
PROJECTION_FRAGRANTICA_LANE = "projection_fragrantica"
FRAGRANTICA_DIRECT_HTTP_SOURCE_SURFACE = "fragrantica_product_page_direct_http"
FRAGRANTICA_CLOAKBROWSER_INITIAL_VIEWPORT_SOURCE_SURFACE = (
    "fragrantica_product_page_cloakbrowser_initial_viewport"
)
FRAGRANTICA_CLOAKBROWSER_DEEP_SCROLL_SOURCE_SURFACE = (
    "fragrantica_product_page_cloakbrowser_deep_scroll_current_window"
)
FRAGRANTICA_SOURCE_SURFACES = frozenset(
    {
        FRAGRANTICA_DIRECT_HTTP_SOURCE_SURFACE,
        FRAGRANTICA_CLOAKBROWSER_INITIAL_VIEWPORT_SOURCE_SURFACE,
        FRAGRANTICA_CLOAKBROWSER_DEEP_SCROLL_SOURCE_SURFACE,
    }
)
FRAGRANTICA_CONTENT_RECORD_KIND = "fragrantica_rendered_current_window_content"
FRAGRANTICA_CONTENT_SCHEMA_VERSION = "fragrantica_rendered_current_window_content_v1"
FRAGRANTICA_PARSER_VERSION = "fragrantica_rendered_current_window_parser_v1"

_FRAGRANTICA_SOURCE_FAMILY = "fragrance_native_database"
_FRAGRANTICA_RENDERED_SURFACES = frozenset(
    {
        FRAGRANTICA_CLOAKBROWSER_INITIAL_VIEWPORT_SOURCE_SURFACE,
        FRAGRANTICA_CLOAKBROWSER_DEEP_SCROLL_SOURCE_SURFACE,
    }
)
_FRAGRANTICA_CONTENT_SLICE_ID = "cloakbrowser_snapshot_01"
_FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES = frozenset(
    {
        "action_ceiling",
        "action_supporting",
        "credibility",
        "decision_strength",
        "demand",
        "discount",
        "exclude",
        "excluded",
        "inclusion",
        "integrity",
        "judgment",
        "signal_use",
        "strength",
        "strong",
        "weak",
    }
)


class FragranticaProjectionRawRef(StrictModel):
    packet_id: str
    slice_id: str


class FragranticaProjectionRawAnchor(StrictModel):
    file_id: str
    relative_packet_path: str
    sha256: str
    hash_basis: str
    anchor_kind: Literal["file", "html_selector", "text_pattern", "json_pointer"] = "file"
    anchor_value: str | None = None
    json_pointer: str | None = None

    @model_validator(mode="after")
    def validate_anchor_value(self) -> "FragranticaProjectionRawAnchor":
        if self.anchor_kind == "json_pointer":
            if not (self.json_pointer and self.json_pointer.startswith("/")):
                raise ValueError("json_pointer anchors require an absolute json_pointer")
            if self.anchor_value is not None:
                raise ValueError("json_pointer anchors must not carry anchor_value")
            return self
        if self.json_pointer is not None:
            raise ValueError("non-json-pointer anchors must not carry json_pointer")
        if self.anchor_kind != "file" and not (self.anchor_value and self.anchor_value.strip()):
            raise ValueError(f"{self.anchor_kind} anchors require anchor_value")
        if self.anchor_kind == "file" and self.anchor_value is not None:
            raise ValueError("file anchors must not carry anchor_value")
        return self


class FragranticaProjectionRow(StrictModel):
    row_id: str
    row_kind: Literal[
        "fragrance_product_snapshot",
        "fragrance_review_tab",
        "fragrance_aggregate_rating",
        "fragrance_performance_component",
        "fragrance_review_archive_gate",
        "fragrance_review_card_current_window",
    ]
    raw_ref: FragranticaProjectionRawRef
    raw_anchor: FragranticaProjectionRawAnchor
    source_platform: Literal["fragrantica"] = "fragrantica"
    source_object_type: Literal["fragrance_product"] = "fragrance_product"
    source_object_site_id: str | None = None
    source_object_name: str | None = None
    brand_or_house: str | None = None
    tab_id: str | None = None
    source_order: int | None = Field(default=None, ge=0)
    comment_id: str | None = None
    parent_row_id: str | None = None
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)
    residuals: list[str] = Field(default_factory=list)

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(cls, value: dict[str, Any | None]) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "Fragrantica projection source_visible_fields may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value


class FragranticaProjectionBinding(StrictModel):
    binding_type: Literal["review_votes_to_review_text"] = "review_votes_to_review_text"
    row_id: str
    raw_ref: FragranticaProjectionRawRef
    raw_anchor: FragranticaProjectionRawAnchor


class FragranticaProjectionLossLedger(StrictModel):
    preserved_evidence_rows: int = Field(ge=0)
    preserved_review_cards: int = Field(ge=0)
    preserved_review_tabs: int = Field(ge=0)
    preserved_bindings: int = Field(ge=0)
    review_card_counts_by_tab: dict[str, int] = Field(default_factory=dict)
    timing: Literal["separate_not_collapsed"] = "separate_not_collapsed"
    hierarchy_preserved: bool
    source_order_preserved: bool
    full_archive_captured: Literal[False] = False
    certification: Literal[
        "mechanical_current_window_projection; does_not_certify_archive_completeness"
    ] = "mechanical_current_window_projection; does_not_certify_archive_completeness"


class FragranticaProjectionPacket(StrictModel):
    projection_method: Literal["fragrantica_current_window_mechanical_projection"] = (
        FRAGRANTICA_PROJECTION_METHOD
    )
    projection_version: Literal["v1"] = FRAGRANTICA_PROJECTION_VERSION
    certification: Literal["view_only; not_cleaned; not_normalized; not_judgment_ready"] = (
        FRAGRANTICA_PROJECTION_CERTIFICATION
    )
    packet_id: str
    rows: list[FragranticaProjectionRow] = Field(default_factory=list)
    binding_map: list[FragranticaProjectionBinding] = Field(default_factory=list)
    loss_ledger: FragranticaProjectionLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "FragranticaProjectionPacket":
        if self.loss_ledger.preserved_evidence_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_evidence_rows must match rows length")
        if self.loss_ledger.preserved_bindings != len(self.binding_map):
            raise ValueError("loss_ledger.preserved_bindings must match binding_map length")
        review_rows = [
            row for row in self.rows if row.row_kind == "fragrance_review_card_current_window"
        ]
        if self.loss_ledger.preserved_review_cards != len(review_rows):
            raise ValueError("loss_ledger.preserved_review_cards must match review rows length")
        tab_rows = [row for row in self.rows if row.row_kind == "fragrance_review_tab"]
        if self.loss_ledger.preserved_review_tabs != len(tab_rows):
            raise ValueError("loss_ledger.preserved_review_tabs must match review-tab rows length")
        return self


class FragranticaContentRow(StrictModel):
    slice_id: str
    row_id: str
    row_kind: Literal[
        "fragrance_product_snapshot",
        "fragrance_review_tab",
        "fragrance_aggregate_rating",
        "fragrance_performance_component",
        "fragrance_review_archive_gate",
        "fragrance_review_card_current_window",
    ]
    source_platform: Literal["fragrantica"] = "fragrantica"
    source_object_type: Literal["fragrance_product"] = "fragrance_product"
    source_object_site_id: str | None = None
    source_object_name: str | None = None
    brand_or_house: str | None = None
    tab_id: str | None = None
    source_order: int | None = Field(default=None, ge=0)
    comment_id: str | None = None
    parent_row_id: str | None = None
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)
    residuals: list[str] = Field(default_factory=list)
    source_anchor_kind: Literal["file", "html_selector", "text_pattern"]
    source_anchor_value: str | None = None

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(cls, value: dict[str, Any | None]) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "Fragrantica content source_visible_fields may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value

    @model_validator(mode="after")
    def validate_source_anchor(self) -> "FragranticaContentRow":
        if self.source_anchor_kind != "file" and not (
            self.source_anchor_value and self.source_anchor_value.strip()
        ):
            raise ValueError(f"{self.source_anchor_kind} anchors require source_anchor_value")
        if self.source_anchor_kind == "file" and self.source_anchor_value is not None:
            raise ValueError("file anchors must not carry source_anchor_value")
        return self


class FragranticaContentBinding(StrictModel):
    slice_id: str
    binding_type: Literal["review_votes_to_review_text"] = "review_votes_to_review_text"
    row_id: str


class FragranticaContentRecord(StrictModel):
    record_kind: Literal["fragrantica_rendered_current_window_content"] = (
        FRAGRANTICA_CONTENT_RECORD_KIND
    )
    schema_version: Literal["fragrantica_rendered_current_window_content_v1"] = (
        FRAGRANTICA_CONTENT_SCHEMA_VERSION
    )
    parser_version: Literal["fragrantica_rendered_current_window_parser_v1"] = (
        FRAGRANTICA_PARSER_VERSION
    )
    source_surface: Literal[
        "fragrantica_product_page_cloakbrowser_initial_viewport",
        "fragrantica_product_page_cloakbrowser_deep_scroll_current_window",
    ]
    source_url: str
    rows: list[FragranticaContentRow] = Field(default_factory=list)
    binding_map: list[FragranticaContentBinding] = Field(default_factory=list)
    loss_ledger: FragranticaProjectionLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "FragranticaContentRecord":
        if self.loss_ledger.preserved_evidence_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_evidence_rows must match rows length")
        if self.loss_ledger.preserved_bindings != len(self.binding_map):
            raise ValueError("loss_ledger.preserved_bindings must match binding_map length")
        return self


def build_fragrantica_projection(
    *,
    packet: SourceCapturePacket,
    raw_file_bytes_by_file_id: Mapping[str, bytes],
) -> FragranticaProjectionPacket:
    """Derive a Fragrantica current-window row view from preserved packet bytes.

    This is not a crawler, archive completion pass, Cleaning transform, ECR schema,
    Judgment read, or demand proof. It only carries source-visible product,
    aggregate, review-tab, review-card, and archive-gate facts with raw anchors.
    """
    if packet.source_family != _FRAGRANTICA_SOURCE_FAMILY:
        raise ValueError(
            "Fragrantica projection requires "
            f"source_family={_FRAGRANTICA_SOURCE_FAMILY!r}; got {packet.source_family!r}"
        )
    if packet.source_surface not in FRAGRANTICA_SOURCE_SURFACES:
        raise ValueError(
            "Fragrantica projection requires "
            f"source_surface in {sorted(FRAGRANTICA_SOURCE_SURFACES)!r}; "
            f"got {packet.source_surface!r}"
        )

    preserved_files = {item.file_id: item for item in packet.preserved_files}
    content_files = [
        item
        for item in packet.preserved_files
        if item.relative_packet_path.replace("\\", "/").endswith("content_record.json")
    ]
    if content_files:
        if len(content_files) != 1:
            raise ValueError("Fragrantica packet must preserve exactly one content_record.json")
        content_file = content_files[0]
        content_bytes = raw_file_bytes_by_file_id.get(content_file.file_id)
        if content_bytes is None:
            raise ValueError(
                f"content record bytes are required for preserved file id: {content_file.file_id}"
            )
        return _projection_from_content_record(
            packet=packet,
            content_file=content_file,
            content_bytes=content_bytes,
        )
    for source_slice in packet.source_slices:
        for file_id in source_slice.preserved_file_ids:
            if file_id not in raw_file_bytes_by_file_id:
                raise ValueError(f"raw bytes are required for preserved file id: {file_id}")

    rows: list[FragranticaProjectionRow] = []
    bindings: list[FragranticaProjectionBinding] = []
    residuals: list[str] = []

    for source_slice in packet.source_slices:
        raw_ref = FragranticaProjectionRawRef(
            packet_id=packet.packet_id,
            slice_id=source_slice.slice_id,
        )
        for file_id in source_slice.preserved_file_ids:
            preserved_file = preserved_files[file_id]
            if not _looks_like_fragrantica_body(preserved_file, raw_file_bytes_by_file_id[file_id]):
                continue
            projected = _project_fragrantica_html(
                raw_file_bytes_by_file_id[file_id],
                source_slice=source_slice,
                raw_ref=raw_ref,
                raw_anchor=_raw_anchor(preserved_file),
            )
            rows.extend(projected.rows)
            bindings.extend(projected.bindings)
            residuals.extend(projected.residuals)

    review_counts = Counter(
        row.tab_id for row in rows if row.row_kind == "fragrance_review_card_current_window"
    )
    if not review_counts:
        residuals.append("fragrantica_review_cards_absent")
    if not any(row.row_kind == "fragrance_product_snapshot" for row in rows):
        residuals.append("fragrantica_product_snapshot_absent")

    return FragranticaProjectionPacket(
        packet_id=packet.packet_id,
        rows=rows,
        binding_map=bindings,
        loss_ledger=FragranticaProjectionLossLedger(
            preserved_evidence_rows=len(rows),
            preserved_review_cards=sum(review_counts.values()),
            preserved_review_tabs=sum(1 for row in rows if row.row_kind == "fragrance_review_tab"),
            preserved_bindings=len(bindings),
            review_card_counts_by_tab={str(key): count for key, count in sorted(review_counts.items())},
            hierarchy_preserved=True,
            source_order_preserved=True,
        ),
        residuals=_dedupe_preserve_order(residuals),
    )


def build_fragrantica_content_record(
    *,
    rendered_dom: bytes,
    visible_text: bytes,
    source_url: str,
    source_surface: str,
) -> dict[str, Any]:
    """Parse one rendered Fragrantica slice without fabricating packet identity."""
    if source_surface not in _FRAGRANTICA_RENDERED_SURFACES:
        raise ValueError(
            "Fragrantica content records require a rendered source surface; "
            f"got {source_surface!r}"
        )
    if not source_url.strip():
        raise ValueError("source_url must be non-empty")
    if not isinstance(rendered_dom, bytes) or not isinstance(visible_text, bytes):
        raise TypeError("rendered_dom and visible_text must be bytes")

    source_slice = _ContentSlice(slice_id=_FRAGRANTICA_CONTENT_SLICE_ID)
    raw_ref = FragranticaProjectionRawRef(
        packet_id="content_record_unbound",
        slice_id=_FRAGRANTICA_CONTENT_SLICE_ID,
    )
    raw_anchor = FragranticaProjectionRawAnchor(
        file_id="content_input_rendered_dom",
        relative_packet_path="cloakbrowser_rendered_dom.html",
        sha256=hashlib.sha256(rendered_dom).hexdigest(),
        hash_basis="raw_stored_bytes",
    )
    projected = _project_fragrantica_html(
        rendered_dom,
        source_slice=source_slice,
        raw_ref=raw_ref,
        raw_anchor=raw_anchor,
    )
    rows = [_content_row(row) for row in projected.rows]
    bindings = [_content_binding(binding) for binding in projected.bindings]
    review_counts = Counter(
        row.tab_id for row in rows if row.row_kind == "fragrance_review_card_current_window"
    )
    residuals = list(projected.residuals)
    if not review_counts:
        residuals.append("fragrantica_review_cards_absent")
    if not any(row.row_kind == "fragrance_product_snapshot" for row in rows):
        residuals.append("fragrantica_product_snapshot_absent")

    record = FragranticaContentRecord(
        source_surface=source_surface,
        source_url=source_url,
        rows=rows,
        binding_map=bindings,
        loss_ledger=FragranticaProjectionLossLedger(
            preserved_evidence_rows=len(rows),
            preserved_review_cards=sum(review_counts.values()),
            preserved_review_tabs=sum(
                1 for row in rows if row.row_kind == "fragrance_review_tab"
            ),
            preserved_bindings=len(bindings),
            review_card_counts_by_tab={
                str(key): count for key, count in sorted(review_counts.items())
            },
            hierarchy_preserved=True,
            source_order_preserved=True,
        ),
        residuals=_dedupe_preserve_order(residuals),
    )
    return record.model_dump(mode="json")


def _projection_from_content_record(
    *,
    packet: SourceCapturePacket,
    content_file: PreservedFile,
    content_bytes: bytes,
) -> FragranticaProjectionPacket:
    try:
        record = FragranticaContentRecord.model_validate_json(content_bytes)
    except Exception as exc:
        raise ValueError(f"invalid Fragrantica content record: {exc}") from exc
    if packet.source_surface != record.source_surface:
        raise ValueError(
            f"Fragrantica content record source_surface {record.source_surface!r} does not "
            f"match packet source surface {packet.source_surface!r}"
        )
    if packet.source_locator.value != record.source_url:
        raise ValueError(
            f"Fragrantica content record source_url {record.source_url!r} does not match "
            f"packet source locator {packet.source_locator.value!r}"
        )

    slice_by_id = {source_slice.slice_id: source_slice for source_slice in packet.source_slices}
    rows: list[FragranticaProjectionRow] = []
    for index, content_row in enumerate(record.rows):
        source_slice = slice_by_id.get(content_row.slice_id)
        if source_slice is None or content_file.file_id not in source_slice.preserved_file_ids:
            raise ValueError(
                f"Fragrantica content row references invalid source slice: {content_row.slice_id}"
            )
        row_data = content_row.model_dump(
            mode="json",
            exclude={"slice_id", "source_anchor_kind", "source_anchor_value"},
        )
        rows.append(
            FragranticaProjectionRow(
                **row_data,
                raw_ref=FragranticaProjectionRawRef(
                    packet_id=packet.packet_id,
                    slice_id=content_row.slice_id,
                ),
                raw_anchor=_content_record_anchor(content_file, f"/rows/{index}"),
            )
        )

    bindings: list[FragranticaProjectionBinding] = []
    for index, content_binding in enumerate(record.binding_map):
        source_slice = slice_by_id.get(content_binding.slice_id)
        if source_slice is None or content_file.file_id not in source_slice.preserved_file_ids:
            raise ValueError(
                "Fragrantica content binding references invalid source slice: "
                f"{content_binding.slice_id}"
            )
        bindings.append(
            FragranticaProjectionBinding(
                binding_type=content_binding.binding_type,
                row_id=content_binding.row_id,
                raw_ref=FragranticaProjectionRawRef(
                    packet_id=packet.packet_id,
                    slice_id=content_binding.slice_id,
                ),
                raw_anchor=_content_record_anchor(content_file, f"/binding_map/{index}"),
            )
        )
    return FragranticaProjectionPacket(
        packet_id=packet.packet_id,
        rows=rows,
        binding_map=bindings,
        loss_ledger=record.loss_ledger,
        residuals=record.residuals,
    )


def _content_row(row: FragranticaProjectionRow) -> FragranticaContentRow:
    row_data = row.model_dump(mode="json", exclude={"raw_ref", "raw_anchor"})
    return FragranticaContentRow(
        **row_data,
        slice_id=row.raw_ref.slice_id,
        source_anchor_kind=row.raw_anchor.anchor_kind,
        source_anchor_value=row.raw_anchor.anchor_value,
    )


def _content_binding(binding: FragranticaProjectionBinding) -> FragranticaContentBinding:
    return FragranticaContentBinding(
        slice_id=binding.raw_ref.slice_id,
        binding_type=binding.binding_type,
        row_id=binding.row_id,
    )


def _content_record_anchor(
    content_file: PreservedFile,
    json_pointer: str,
) -> FragranticaProjectionRawAnchor:
    return FragranticaProjectionRawAnchor(
        file_id=content_file.file_id,
        relative_packet_path=content_file.relative_packet_path,
        sha256=content_file.sha256,
        hash_basis=content_file.hash_basis,
        anchor_kind="json_pointer",
        json_pointer=json_pointer,
    )


def build_fragrantica_projection_from_packet_directory(
    *,
    packet_or_manifest_path: Path,
) -> FragranticaProjectionPacket:
    packet, raw_file_bytes_by_file_id = _read_packet_directory(packet_or_manifest_path)
    return build_fragrantica_projection(
        packet=packet,
        raw_file_bytes_by_file_id=raw_file_bytes_by_file_id,
    )


class _ProjectedFragranticaHtml(StrictModel):
    rows: list[FragranticaProjectionRow] = Field(default_factory=list)
    bindings: list[FragranticaProjectionBinding] = Field(default_factory=list)
    residuals: list[str] = Field(default_factory=list)


class _ContentSlice(StrictModel):
    slice_id: str


def _project_fragrantica_html(
    body: bytes,
    *,
    source_slice: SourceCaptureSlice | _ContentSlice,
    raw_ref: FragranticaProjectionRawRef,
    raw_anchor: FragranticaProjectionRawAnchor,
) -> _ProjectedFragranticaHtml:
    text = body.decode("utf-8", errors="replace")
    product = _product_context(text)
    rows: list[FragranticaProjectionRow] = []
    bindings: list[FragranticaProjectionBinding] = []
    residuals: list[str] = []
    source_object_site_id = product.get("source_object_site_id")
    source_object_name = product.get("source_object_name")
    brand_or_house = product.get("brand_or_house")

    rows.append(
        FragranticaProjectionRow(
            row_id=f"{source_slice.slice_id}:fragrantica:product_snapshot",
            row_kind="fragrance_product_snapshot",
            raw_ref=raw_ref,
            raw_anchor=_with_anchor(raw_anchor, "text_pattern", "canonical|description|title"),
            source_object_site_id=source_object_site_id,
            source_object_name=source_object_name,
            brand_or_house=brand_or_house,
            source_visible_fields=product,
            residuals=_product_residuals(product),
        )
    )

    tab_rows = _review_tab_rows(
        text,
        raw_ref=raw_ref,
        raw_anchor=raw_anchor,
        source_slice=source_slice,
        source_object_site_id=source_object_site_id,
        source_object_name=source_object_name,
        brand_or_house=brand_or_house,
    )
    rows.extend(tab_rows)
    tab_labels = {row.tab_id: row.source_visible_fields.get("tab_label") for row in tab_rows}

    review_rows, review_bindings = _review_card_rows(
        text,
        raw_ref=raw_ref,
        raw_anchor=raw_anchor,
        source_slice=source_slice,
        source_object_site_id=source_object_site_id,
        source_object_name=source_object_name,
        brand_or_house=brand_or_house,
        tab_labels=tab_labels,
    )
    rows.extend(review_rows)
    bindings.extend(review_bindings)

    aggregate_row = _aggregate_rating_row(
        text,
        raw_ref=raw_ref,
        raw_anchor=raw_anchor,
        source_slice=source_slice,
        source_object_site_id=source_object_site_id,
        source_object_name=source_object_name,
        brand_or_house=brand_or_house,
    )
    if aggregate_row is None:
        residuals.append("fragrantica_aggregate_rating_absent")
    else:
        rows.append(aggregate_row)

    performance_rows = _performance_component_rows(
        text,
        raw_ref=raw_ref,
        raw_anchor=raw_anchor,
        source_slice=source_slice,
        source_object_site_id=source_object_site_id,
        source_object_name=source_object_name,
        brand_or_house=brand_or_house,
    )
    rows.extend(performance_rows)
    if performance_rows:
        residuals.append("performance_component_values_not_observed_in_preserved_body")

    archive_gate_rows = _archive_gate_rows(
        text,
        raw_ref=raw_ref,
        raw_anchor=raw_anchor,
        source_slice=source_slice,
        source_object_site_id=source_object_site_id,
        source_object_name=source_object_name,
        brand_or_house=brand_or_house,
    )
    rows.extend(archive_gate_rows)
    if archive_gate_rows:
        residuals.append("full_review_archive_not_captured_login_prompt_present")
    residuals.extend(
        [
            "linked_media_assets_not_preserved_by_current_window_packet",
            "review_attached_photo_proof_not_present",
        ]
    )
    if any(row.tab_id == "search-reviews" for row in tab_rows) and not any(
        row.tab_id == "search-reviews" for row in review_rows
    ):
        residuals.append("search_review_rows_not_embedded_in_preserved_body")
    residuals.extend(_non_review_fragrance_scope_residuals(text))

    return _ProjectedFragranticaHtml(
        rows=rows,
        bindings=bindings,
        residuals=_dedupe_preserve_order(residuals),
    )


def _product_context(text: str) -> dict[str, Any | None]:
    canonical_url = _first_match(text, r'<link\s+rel="canonical"\s+href="([^"]+)"')
    title = _text(_first_match(text, r"<title>(.*?)</title>", flags=re.IGNORECASE | re.DOTALL))
    meta_description = _first_match(
        text,
        r'<meta\s+name="description"\s+content="([^"]*)"',
        flags=re.IGNORECASE,
    )
    meta_keywords = _first_match(
        text,
        r'<meta\s+name="keywords"\s+content="([^"]*)"',
        flags=re.IGNORECASE,
    )
    description_html = _first_match(
        text,
        r'<div id="perfume-description-content".*?itemprop="description">(.*?)</div>',
        flags=re.IGNORECASE | re.DOTALL,
    )
    product_name = None
    brand_or_house = None
    if description_html:
        match = re.search(
            r"<b>(.*?)</b>\s+by\s+<b>(.*?)</b>",
            description_html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if match:
            product_name = _text(match.group(1))
            brand_or_house = _text(match.group(2))
    if product_name is None and canonical_url:
        product_name = _name_from_fragrantica_url(canonical_url)
    if brand_or_house is None and canonical_url:
        brand_or_house = _brand_from_fragrantica_url(canonical_url)

    site_id = _first_match(canonical_url or "", r"-(\d+)\.html$")
    if site_id is None:
        site_id = _first_match(text, r':perfume[_-]id="(\d+)"')
    launched_year = _first_match(
        _text(description_html or meta_description or ""),
        r"was launched in (\d{4})",
        flags=re.IGNORECASE,
    )
    return {
        "source_platform": "fragrantica",
        "source_object_type": "fragrance_product",
        "source_object_site_id": site_id,
        "source_object_name": product_name,
        "brand_or_house": brand_or_house,
        "canonical_url": canonical_url,
        "page_title": title,
        "meta_description": html.unescape(meta_description) if meta_description else None,
        "meta_keywords": html.unescape(meta_keywords) if meta_keywords else None,
        "launched_year": int(launched_year) if launched_year else None,
    }


def _product_residuals(product: Mapping[str, Any | None]) -> list[str]:
    residuals = []
    for field in ("source_object_site_id", "source_object_name", "brand_or_house", "canonical_url"):
        if product.get(field) in {None, ""}:
            residuals.append(f"{field}_absent")
    return residuals


def _non_review_fragrance_scope_residuals(text: str) -> list[str]:
    residuals = []
    if re.search(r"\bmain\s+accords?\b", text, flags=re.IGNORECASE):
        residuals.append("fragrance_accords_present_but_not_projected")
    if re.search(r"\b(?:top|middle|base)\s+notes?\b", text, flags=re.IGNORECASE):
        residuals.append("fragrance_notes_pyramid_present_but_not_projected")
    if re.search(r"\breminds\s+me\s+of\b", text, flags=re.IGNORECASE):
        residuals.append("fragrance_similarity_surface_present_but_not_projected")
    return residuals


def _review_tab_rows(
    text: str,
    *,
    raw_ref: FragranticaProjectionRawRef,
    raw_anchor: FragranticaProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
    source_object_site_id: str | None,
    source_object_name: str | None,
    brand_or_house: str | None,
) -> list[FragranticaProjectionRow]:
    rows = []
    for index, match in enumerate(
        re.finditer(r'<button[^>]+data-tab="([^"]+)"([^>]*)>(.*?)</button>', text, re.DOTALL),
        start=1,
    ):
        tab_id = match.group(1)
        tab_body = match.group(0)
        rows.append(
            FragranticaProjectionRow(
                row_id=f"{source_slice.slice_id}:fragrantica:review_tab:{tab_id}",
                row_kind="fragrance_review_tab",
                raw_ref=raw_ref,
                raw_anchor=_with_anchor(raw_anchor, "html_selector", f'[data-tab="{tab_id}"]'),
                source_object_site_id=source_object_site_id,
                source_object_name=source_object_name,
                brand_or_house=brand_or_house,
                tab_id=tab_id,
                source_order=index,
                source_visible_fields={
                    "tab_id": tab_id,
                    "tab_label": _text(match.group(3)),
                    "active": 'data-active="true"' in tab_body,
                },
            )
        )
    return rows


def _review_card_rows(
    text: str,
    *,
    raw_ref: FragranticaProjectionRawRef,
    raw_anchor: FragranticaProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
    source_object_site_id: str | None,
    source_object_name: str | None,
    brand_or_house: str | None,
    tab_labels: Mapping[str | None, Any | None],
) -> tuple[list[FragranticaProjectionRow], list[FragranticaProjectionBinding]]:
    panels = [
        (match.start(), match.group(1))
        for match in re.finditer(
            r'<div class="review-tab-panel[^>]*" id="([^"]+)"',
            text,
            flags=re.IGNORECASE,
        )
    ]
    starts = list(
        re.finditer(
            r'<div id="parent(\d+)"\s+class="([^"]*tw-review-card[^"]*)"',
            text,
            flags=re.IGNORECASE,
        )
    )
    rows: list[FragranticaProjectionRow] = []
    bindings: list[FragranticaProjectionBinding] = []
    source_order_by_tab: Counter[str] = Counter()
    for index, match in enumerate(starts):
        comment_id = match.group(1)
        tab_id = _panel_for_position(match.start(), panels)
        source_order_by_tab[str(tab_id)] += 1
        segment_end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        segment = text[match.start() : segment_end]
        row_id = (
            f"{source_slice.slice_id}:fragrantica:review_card:{tab_id or 'unknown'}:{comment_id}"
        )
        row_anchor = _with_anchor(raw_anchor, "html_selector", f"#parent{comment_id}")
        row = FragranticaProjectionRow(
            row_id=row_id,
            row_kind="fragrance_review_card_current_window",
            raw_ref=raw_ref,
            raw_anchor=row_anchor,
            source_object_site_id=source_object_site_id,
            source_object_name=source_object_name,
            brand_or_house=brand_or_house,
            tab_id=tab_id,
            source_order=source_order_by_tab[str(tab_id)],
            comment_id=comment_id,
            source_visible_fields=_review_card_fields(
                segment,
                comment_id=comment_id,
                tab_id=tab_id,
                tab_label=tab_labels.get(tab_id),
            ),
            residuals=_review_card_residuals(segment, comment_id),
        )
        rows.append(row)
        bindings.append(FragranticaProjectionBinding(row_id=row_id, raw_ref=raw_ref, raw_anchor=row_anchor))
    return rows, bindings


def _review_card_fields(
    segment: str,
    *,
    comment_id: str,
    tab_id: str | None,
    tab_label: Any | None,
) -> dict[str, Any | None]:
    votes = _json_attr(segment, r'<user-perfume-votes-new[^>]+:perfume-votes="([^"]+)"')
    author_name = _first_match(segment, r'<meta\s+itemprop="name"\s+content="([^"]*)"')
    author_profile_url = _first_match(segment, r'title="(https://www\.fragrantica\.com/@[^"]+)"')
    avatar_url = _first_match(segment, r'<img[^>]+itemprop="image"[^>]+src="([^"]+)"', flags=re.DOTALL)
    date_match = re.search(
        r'itemprop="datePublished"\s+content="([^"]+)"[^>]*>(.*?)</span>',
        segment,
        flags=re.DOTALL,
    )
    review_html = _first_match(
        segment,
        rf'<div id="review_{re.escape(comment_id)}">(.*?)</div>',
        flags=re.DOTALL,
    )
    review_text = _text(review_html)
    source_text_length = _first_match(segment, r':text-length="(\d+)"')
    return {
        "comment_id": comment_id,
        "tab_id": tab_id,
        "tab_label": tab_label,
        "card_gradient_class": _first_match(segment, r'tw-review-card\s+(tw-gradient-[a-z]+)'),
        "author_display_name": html.unescape(author_name) if author_name else None,
        "author_profile_url": author_profile_url,
        "author_avatar_url": avatar_url,
        "date_published": date_match.group(1) if date_match else None,
        "date_display_text": _text(date_match.group(2)) if date_match else None,
        "review_text": review_text,
        "review_text_length_chars": len(review_text) if review_text is not None else None,
        "source_text_length": int(source_text_length) if source_text_length else None,
        "perfume_votes": votes,
        "rating": votes.get("rating") if isinstance(votes, dict) else None,
        "longevity": votes.get("longevity") if isinstance(votes, dict) else None,
        "sillage": votes.get("sillage") if isinstance(votes, dict) else None,
        "gender": votes.get("gender") if isinstance(votes, dict) else None,
        "relation": votes.get("relation") if isinstance(votes, dict) else None,
        "season_winter": votes.get("winter") if isinstance(votes, dict) else None,
        "season_spring": votes.get("spring") if isinstance(votes, dict) else None,
        "season_summer": votes.get("summer") if isinstance(votes, dict) else None,
        "season_autumn": votes.get("autumn") if isinstance(votes, dict) else None,
        "day": votes.get("day") if isinstance(votes, dict) else None,
        "night": votes.get("night") if isinstance(votes, dict) else None,
        "vote_initial_status": _first_match(segment, r'<vote-buttons-new[^>]+initial-status="([^"]+)"'),
        "vote_item_id": _first_match(segment, r'<vote-buttons-new[^>]+item-id="([^"]+)"', flags=re.DOTALL),
        "vote_comment_id": _first_match(
            segment,
            r'<vote-buttons-new[^>]+comment-id="([^"]+)"',
            flags=re.DOTALL,
        ),
        "share_path": _first_match(segment, r'<share-new\s+path="([^"]+)"'),
    }


def _review_card_residuals(segment: str, comment_id: str) -> list[str]:
    residuals = []
    checks = {
        "author_display_name_absent": r'<meta\s+itemprop="name"\s+content="([^"]*)"',
        "date_published_absent": r'itemprop="datePublished"\s+content="([^"]+)"',
        "review_text_absent": rf'<div id="review_{re.escape(comment_id)}">(.*?)</div>',
        "perfume_votes_absent": r'<user-perfume-votes-new[^>]+:perfume-votes="([^"]+)"',
        "share_path_absent": r'<share-new\s+path="([^"]+)"',
    }
    for residual, pattern in checks.items():
        if re.search(pattern, segment, flags=re.DOTALL) is None:
            residuals.append(residual)
    return residuals


def _aggregate_rating_row(
    text: str,
    *,
    raw_ref: FragranticaProjectionRawRef,
    raw_anchor: FragranticaProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
    source_object_site_id: str | None,
    source_object_name: str | None,
    brand_or_house: str | None,
) -> FragranticaProjectionRow | None:
    rating_value = _first_match(text, r'itemprop="ratingValue"[^>]*>([^<]+)</span>')
    rating_count = _first_match(text, r'itemprop="ratingCount"\s+content="([^"]+)"')
    rating_count_display = _first_match(
        text,
        r'itemprop="ratingCount"\s+content="[^"]+"[^>]*>([^<]+)</span>',
    )
    displayed_review_count = _first_match(
        text,
        r'Reviews\s*\(<span[^>]*>([^<]+)</span>\)',
        flags=re.IGNORECASE,
    )
    if rating_value is None and rating_count is None and displayed_review_count is None:
        return None
    return FragranticaProjectionRow(
        row_id=f"{source_slice.slice_id}:fragrantica:aggregate_rating",
        row_kind="fragrance_aggregate_rating",
        raw_ref=raw_ref,
        raw_anchor=_with_anchor(raw_anchor, "text_pattern", "Perfume rating|Reviews"),
        source_object_site_id=source_object_site_id,
        source_object_name=source_object_name,
        brand_or_house=brand_or_house,
        source_visible_fields={
            "rating_value": _to_float(rating_value),
            "best_rating": _to_float(_first_match(text, r'itemprop="bestRating"[^>]*>([^<]+)</span>')),
            "rating_count": _to_int(rating_count),
            "rating_count_display": rating_count_display,
            "displayed_review_count": displayed_review_count,
            "displayed_review_count_approx_value": _parse_abbrev_count(displayed_review_count),
        },
    )


def _performance_component_rows(
    text: str,
    *,
    raw_ref: FragranticaProjectionRawRef,
    raw_anchor: FragranticaProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
    source_object_site_id: str | None,
    source_object_name: str | None,
    brand_or_house: str | None,
) -> list[FragranticaProjectionRow]:
    component_patterns = (
        ("longevity", r"<longevity-rating-new\b[^>]*>"),
        ("sillage", r"<sillage-rating-new\b[^>]*>"),
        ("seasons", r"<seasons-rating-new\b[^>]*>"),
    )
    rows = []
    for component, pattern in component_patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match is None:
            continue
        rows.append(
            FragranticaProjectionRow(
                row_id=f"{source_slice.slice_id}:fragrantica:performance_component:{component}",
                row_kind="fragrance_performance_component",
                raw_ref=raw_ref,
                raw_anchor=_with_anchor(raw_anchor, "html_selector", f"{component}-rating-new"),
                source_object_site_id=source_object_site_id,
                source_object_name=source_object_name,
                brand_or_house=brand_or_house,
                source_visible_fields={
                    "component": component,
                    "component_present": True,
                    "value_posture": "component_placeholder_present_value_not_observed_in_preserved_body",
                    "perfume_id": _first_match(match.group(0), r':perfume_id="(\d+)"'),
                },
                residuals=["component_value_not_observed_in_preserved_body"],
            )
        )
    return rows


def _archive_gate_rows(
    text: str,
    *,
    raw_ref: FragranticaProjectionRawRef,
    raw_anchor: FragranticaProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
    source_object_site_id: str | None,
    source_object_name: str | None,
    brand_or_house: str | None,
) -> list[FragranticaProjectionRow]:
    rows = []
    for match in re.finditer(r"<reviews-infinity-new\b[^>]*>", text, flags=re.IGNORECASE):
        tag = match.group(0)
        sentiment = _first_match(tag, r'sentiment="([^"]+)"') or "unknown"
        lang_strings = _json_attr(tag, r':lang-strings="([^"]+)"')
        rows.append(
            FragranticaProjectionRow(
                row_id=f"{source_slice.slice_id}:fragrantica:review_archive_gate:{sentiment}",
                row_kind="fragrance_review_archive_gate",
                raw_ref=raw_ref,
                raw_anchor=_with_anchor(
                    raw_anchor,
                    "html_selector",
                    f'reviews-infinity-new[sentiment="{sentiment}"]',
                ),
                source_object_site_id=source_object_site_id,
                source_object_name=source_object_name,
                brand_or_house=brand_or_house,
                source_visible_fields={
                    "sentiment": sentiment,
                    "perfume_id": _first_match(tag, r':perfume-id="(\d+)"'),
                    "is_logged": _to_bool(_first_match(tag, r':is-logged="([^"]+)"')),
                    "login_url": _first_match(tag, r'login-url="([^"]+)"'),
                    "login_prompt_title": (
                        lang_strings.get("loginPromptTitle") if isinstance(lang_strings, dict) else None
                    ),
                    "login_prompt_message": (
                        lang_strings.get("loginPromptMessage") if isinstance(lang_strings, dict) else None
                    ),
                    "login_button_text": (
                        lang_strings.get("loginButtonText") if isinstance(lang_strings, dict) else None
                    ),
                },
                residuals=["full_archive_requires_login_in_observed_preserved_body"],
            )
        )
    return rows


def _looks_like_fragrantica_body(preserved_file: PreservedFile, body: bytes) -> bool:
    path = preserved_file.relative_packet_path.lower()
    non_body_artifacts = (
        "http_response_metadata",
        "snapshot_metadata",
        "visible_text",
        "screenshot",
    )
    if any(marker in path for marker in non_body_artifacts):
        return False
    sample = body[:200_000].decode("utf-8", errors="ignore").lower()
    return "fragrantica.com/perfume/" in sample or "user-perfume-votes-new" in sample


def _raw_anchor(preserved_file: PreservedFile) -> FragranticaProjectionRawAnchor:
    return FragranticaProjectionRawAnchor(
        file_id=preserved_file.file_id,
        relative_packet_path=preserved_file.relative_packet_path,
        sha256=preserved_file.sha256,
        hash_basis=preserved_file.hash_basis,
    )


def _with_anchor(
    raw_anchor: FragranticaProjectionRawAnchor,
    anchor_kind: Literal["html_selector", "text_pattern"],
    anchor_value: str,
) -> FragranticaProjectionRawAnchor:
    return FragranticaProjectionRawAnchor(
        file_id=raw_anchor.file_id,
        relative_packet_path=raw_anchor.relative_packet_path,
        sha256=raw_anchor.sha256,
        hash_basis=raw_anchor.hash_basis,
        anchor_kind=anchor_kind,
        anchor_value=anchor_value,
    )


def _panel_for_position(position: int, panels: list[tuple[int, str]]) -> str | None:
    active = None
    for panel_start, tab_id in panels:
        if panel_start <= position:
            active = tab_id
        else:
            break
    return active


def _json_attr(segment: str, pattern: str) -> Any | None:
    value = _first_match(segment, pattern, flags=re.DOTALL)
    if value is None:
        return None
    try:
        return json.loads(html.unescape(value))
    except json.JSONDecodeError:
        return None


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value.replace(",", "").strip())
    except ValueError:
        return None


def _to_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value.replace(",", "").strip())
    except ValueError:
        return None


def _to_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    return None


def _parse_abbrev_count(value: str | None) -> int | None:
    if value is None:
        return None
    normalized = value.strip().upper().replace(",", "")
    multiplier = 1
    if normalized.endswith("K"):
        multiplier = 1_000
        normalized = normalized[:-1]
    elif normalized.endswith("M"):
        multiplier = 1_000_000
        normalized = normalized[:-1]
    try:
        return int(float(normalized) * multiplier)
    except ValueError:
        return None


def _name_from_fragrantica_url(url: str) -> str | None:
    match = re.search(r"/perfume/[^/]+/([^/]+)-\d+\.html", url)
    if match is None:
        return None
    return html.unescape(match.group(1).replace("-", " "))


def _brand_from_fragrantica_url(url: str) -> str | None:
    match = re.search(r"/perfume/([^/]+)/", url)
    if match is None:
        return None
    return html.unescape(match.group(1).replace("-", " "))


def _is_forbidden_field_name(key: str) -> bool:
    return is_forbidden_field_pattern_match(key, _FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES)


def _projection_json_text(projection: FragranticaProjectionPacket) -> str:
    return f"{json.dumps(projection.model_dump(mode='json'), indent=2, sort_keys=True)}\n"


__all__ = [
    "FRAGRANTICA_CONTENT_RECORD_KIND",
    "FRAGRANTICA_CONTENT_SCHEMA_VERSION",
    "FRAGRANTICA_PARSER_VERSION",
    "FRAGRANTICA_PROJECTION_CERTIFICATION",
    "FRAGRANTICA_PROJECTION_METHOD",
    "FRAGRANTICA_PROJECTION_VERSION",
    "PROJECTION_FRAGRANTICA_LANE",
    "FragranticaContentRecord",
    "FragranticaProjectionBinding",
    "FragranticaProjectionLossLedger",
    "FragranticaProjectionPacket",
    "FragranticaProjectionRawAnchor",
    "FragranticaProjectionRawRef",
    "FragranticaProjectionRow",
    "build_fragrantica_projection",
    "build_fragrantica_content_record",
    "build_fragrantica_projection_from_packet_directory",
]
