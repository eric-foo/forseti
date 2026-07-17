from __future__ import annotations

import html
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Mapping, Protocol
from urllib.parse import unquote

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


PARFUMO_PROJECTION_METHOD = "parfumo_current_window_mechanical_projection"
PARFUMO_PROJECTION_VERSION = "v0"
PARFUMO_PROJECTION_CERTIFICATION = "view_only; not_cleaned; not_normalized; not_judgment_ready"
PROJECTION_PARFUMO_LANE = "projection_parfumo"
PARFUMO_TARGETED_CONTENT_RECORD_KIND = "parfumo_targeted_content"
PARFUMO_TARGETED_CONTENT_SCHEMA_VERSION = "parfumo_targeted_content_v1"
PARFUMO_TARGETED_PARSER_VERSION = "parfumo_targeted_parser_v1"

_PARFUMO_SOURCE_FAMILY = "fragrance_native_database"
PARFUMO_DIRECT_HTTP_SOURCE_SURFACE = "parfumo_product_page_direct_http"
PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE = (
    "parfumo_product_page_chrome_extension_targeted_rendered_session"
)
_PARFUMO_SOURCE_SURFACES = (
    PARFUMO_DIRECT_HTTP_SOURCE_SURFACE,
    PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE,
)
_TARGETED_PRODUCT_CONTEXT_SLICE = "parfumo_targeted:product_context"
_TARGETED_REVIEW_LATEST_RECENT_SLICE = "parfumo_targeted:review_latest_recent"
_TARGETED_REVIEW_HIGH_RATING_SLICE = "parfumo_targeted:review_source_visible_high_rating"
_TARGETED_REVIEW_LOW_RATING_SLICE = "parfumo_targeted:review_source_visible_low_rating"
_TARGETED_STATEMENT_LATEST_RECENT_SLICE = "parfumo_targeted:statement_latest_recent"
_TARGETED_SLICE_IDS = (
    _TARGETED_PRODUCT_CONTEXT_SLICE,
    _TARGETED_REVIEW_LATEST_RECENT_SLICE,
    _TARGETED_REVIEW_HIGH_RATING_SLICE,
    _TARGETED_REVIEW_LOW_RATING_SLICE,
    _TARGETED_STATEMENT_LATEST_RECENT_SLICE,
)
_LATEST_REVIEW_TOKENS = ("latest", "recent", "new", "newest")
_HIGH_RATING_BUCKET_TOKENS = ("high", "top", "positive")
_LOW_RATING_BUCKET_TOKENS = ("low", "critical", "negative")
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


class ParfumoProjectionRawRef(StrictModel):
    packet_id: str
    slice_id: str


class ParfumoProjectionRawAnchor(StrictModel):
    file_id: str
    relative_packet_path: str
    sha256: str
    hash_basis: str
    anchor_kind: Literal["file", "html_selector", "json_pointer", "text_pattern"] = "file"
    anchor_value: str | None = None
    json_pointer: str | None = None

    @model_validator(mode="after")
    def validate_anchor_value(self) -> "ParfumoProjectionRawAnchor":
        if self.anchor_kind == "json_pointer":
            if not (self.json_pointer and self.json_pointer.strip()):
                raise ValueError("json_pointer anchors require json_pointer")
            if self.anchor_value is not None:
                raise ValueError("json_pointer anchors must not carry anchor_value")
            return self
        if self.json_pointer is not None:
            raise ValueError(f"{self.anchor_kind} anchors must not carry json_pointer")
        if self.anchor_kind != "file" and not (self.anchor_value and self.anchor_value.strip()):
            raise ValueError(f"{self.anchor_kind} anchors require anchor_value")
        if self.anchor_kind == "file" and self.anchor_value is not None:
            raise ValueError("file anchors must not carry anchor_value")
        return self


class ParfumoProjectionRow(StrictModel):
    row_id: str
    row_kind: Literal[
        "fragrance_product_snapshot",
        "fragrance_review_tab",
        "fragrance_aggregate_rating",
        "fragrance_performance_component",
        "fragrance_review_archive_gate",
        "fragrance_review_card_current_window",
        "fragrance_statement_current_window",
    ]
    raw_ref: ParfumoProjectionRawRef
    raw_anchor: ParfumoProjectionRawAnchor
    source_platform: Literal["parfumo"] = "parfumo"
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
                "Parfumo projection source_visible_fields may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value


class ParfumoProjectionBinding(StrictModel):
    binding_type: Literal[
        "review_metadata_to_review_text",
        "statement_metadata_to_statement_text",
    ]
    row_id: str
    raw_ref: ParfumoProjectionRawRef
    raw_anchor: ParfumoProjectionRawAnchor


class ParfumoProjectionLossLedger(StrictModel):
    preserved_evidence_rows: int = Field(ge=0)
    preserved_review_cards: int = Field(ge=0)
    preserved_statements: int = Field(ge=0)
    preserved_review_tabs: int = Field(ge=0)
    preserved_bindings: int = Field(ge=0)
    text_row_counts_by_tab: dict[str, int] = Field(default_factory=dict)
    timing: Literal["separate_not_collapsed"] = "separate_not_collapsed"
    hierarchy_preserved: bool
    source_order_preserved: bool
    full_review_corpus_captured: Literal[False] = False
    full_statement_corpus_captured: Literal[False] = False
    certification: Literal[
        "mechanical_current_window_projection; does_not_certify_corpus_completeness"
    ] = "mechanical_current_window_projection; does_not_certify_corpus_completeness"


class ParfumoProjectionPacket(StrictModel):
    projection_method: Literal["parfumo_current_window_mechanical_projection"] = (
        PARFUMO_PROJECTION_METHOD
    )
    projection_version: Literal["v0"] = PARFUMO_PROJECTION_VERSION
    certification: Literal["view_only; not_cleaned; not_normalized; not_judgment_ready"] = (
        PARFUMO_PROJECTION_CERTIFICATION
    )
    packet_id: str
    rows: list[ParfumoProjectionRow] = Field(default_factory=list)
    binding_map: list[ParfumoProjectionBinding] = Field(default_factory=list)
    loss_ledger: ParfumoProjectionLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "ParfumoProjectionPacket":
        if self.loss_ledger.preserved_evidence_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_evidence_rows must match rows length")
        if self.loss_ledger.preserved_bindings != len(self.binding_map):
            raise ValueError("loss_ledger.preserved_bindings must match binding_map length")
        review_rows = [
            row for row in self.rows if row.row_kind == "fragrance_review_card_current_window"
        ]
        if self.loss_ledger.preserved_review_cards != len(review_rows):
            raise ValueError("loss_ledger.preserved_review_cards must match review rows length")
        statement_rows = [
            row for row in self.rows if row.row_kind == "fragrance_statement_current_window"
        ]
        if self.loss_ledger.preserved_statements != len(statement_rows):
            raise ValueError("loss_ledger.preserved_statements must match statement rows length")
        tab_rows = [row for row in self.rows if row.row_kind == "fragrance_review_tab"]
        if self.loss_ledger.preserved_review_tabs != len(tab_rows):
            raise ValueError("loss_ledger.preserved_review_tabs must match review-tab rows length")
        return self


class ParfumoTargetedContentRow(StrictModel):
    slice_id: str
    row_id: str
    row_kind: Literal[
        "fragrance_product_snapshot",
        "fragrance_review_tab",
        "fragrance_aggregate_rating",
        "fragrance_performance_component",
        "fragrance_review_archive_gate",
        "fragrance_review_card_current_window",
        "fragrance_statement_current_window",
    ]
    source_platform: Literal["parfumo"] = "parfumo"
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

    @model_validator(mode="after")
    def validate_source_anchor(self) -> "ParfumoTargetedContentRow":
        if self.source_anchor_kind != "file" and not (
            self.source_anchor_value and self.source_anchor_value.strip()
        ):
            raise ValueError(f"{self.source_anchor_kind} anchors require source_anchor_value")
        if self.source_anchor_kind == "file" and self.source_anchor_value is not None:
            raise ValueError("file anchors must not carry source_anchor_value")
        return self


class ParfumoTargetedContentBinding(StrictModel):
    slice_id: str
    binding_type: Literal[
        "review_metadata_to_review_text",
        "statement_metadata_to_statement_text",
    ]
    row_id: str


class ParfumoTargetedContentRecord(StrictModel):
    record_kind: Literal["parfumo_targeted_content"] = PARFUMO_TARGETED_CONTENT_RECORD_KIND
    schema_version: Literal["parfumo_targeted_content_v1"] = (
        PARFUMO_TARGETED_CONTENT_SCHEMA_VERSION
    )
    parser_version: Literal["parfumo_targeted_parser_v1"] = PARFUMO_TARGETED_PARSER_VERSION
    source_url: str
    rows: list[ParfumoTargetedContentRow] = Field(default_factory=list)
    binding_map: list[ParfumoTargetedContentBinding] = Field(default_factory=list)
    loss_ledger: ParfumoProjectionLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "ParfumoTargetedContentRecord":
        if self.loss_ledger.preserved_evidence_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_evidence_rows must match rows length")
        if self.loss_ledger.preserved_bindings != len(self.binding_map):
            raise ValueError("loss_ledger.preserved_bindings must match binding_map length")
        return self


def build_parfumo_projection(
    *,
    packet: SourceCapturePacket,
    raw_file_bytes_by_file_id: Mapping[str, bytes],
) -> ParfumoProjectionPacket:
    """Derive a Parfumo current-window row view from preserved packet bytes."""
    if packet.source_family != _PARFUMO_SOURCE_FAMILY:
        raise ValueError(
            "Parfumo projection requires "
            f"source_family={_PARFUMO_SOURCE_FAMILY!r}; got {packet.source_family!r}"
        )
    if packet.source_surface not in _PARFUMO_SOURCE_SURFACES:
        raise ValueError(
            "Parfumo projection requires "
            f"source_surface in {_PARFUMO_SOURCE_SURFACES!r}; got {packet.source_surface!r}"
        )

    preserved_files = {item.file_id: item for item in packet.preserved_files}
    content_files = [
        item
        for item in packet.preserved_files
        if item.relative_packet_path.replace("\\", "/").endswith("content_record.json")
    ]
    if content_files:
        if len(content_files) != 1:
            raise ValueError("Parfumo packet must preserve exactly one content_record.json")
        content_file = content_files[0]
        content_bytes = raw_file_bytes_by_file_id.get(content_file.file_id)
        if content_bytes is None:
            raise ValueError(
                f"content record bytes are required for preserved file id: {content_file.file_id}"
            )
        return _projection_from_targeted_content_record(
            packet=packet,
            content_file=content_file,
            content_bytes=content_bytes,
        )

    for source_slice in packet.source_slices:
        for file_id in source_slice.preserved_file_ids:
            if file_id not in raw_file_bytes_by_file_id:
                raise ValueError(f"raw bytes are required for preserved file id: {file_id}")

    rows: list[ParfumoProjectionRow] = []
    bindings: list[ParfumoProjectionBinding] = []
    residuals: list[str] = []

    for source_slice in packet.source_slices:
        raw_ref = ParfumoProjectionRawRef(
            packet_id=packet.packet_id,
            slice_id=source_slice.slice_id,
        )
        for file_id in source_slice.preserved_file_ids:
            preserved_file = preserved_files[file_id]
            body = raw_file_bytes_by_file_id[file_id]
            if not _looks_like_parfumo_body(
                preserved_file,
                body,
                source_surface=packet.source_surface,
            ):
                continue
            projected = _project_parfumo_html(
                body,
                source_slice=source_slice,
                raw_ref=raw_ref,
                raw_anchor=_raw_anchor(preserved_file),
                source_surface=packet.source_surface,
            )
            rows.extend(projected.rows)
            bindings.extend(projected.bindings)
            residuals.extend(projected.residuals)

    text_counts = Counter(
        row.tab_id or row.row_kind
        for row in rows
        if row.row_kind
        in {"fragrance_review_card_current_window", "fragrance_statement_current_window"}
    )
    if not any(row.row_kind == "fragrance_review_card_current_window" for row in rows):
        residuals.append("parfumo_review_cards_absent")
    if not any(row.row_kind == "fragrance_statement_current_window" for row in rows):
        residuals.append("parfumo_statement_rows_absent")
    if not any(row.row_kind == "fragrance_product_snapshot" for row in rows):
        residuals.append("parfumo_product_snapshot_absent")

    return ParfumoProjectionPacket(
        packet_id=packet.packet_id,
        rows=rows,
        binding_map=bindings,
        loss_ledger=ParfumoProjectionLossLedger(
            preserved_evidence_rows=len(rows),
            preserved_review_cards=sum(
                1 for row in rows if row.row_kind == "fragrance_review_card_current_window"
            ),
            preserved_statements=sum(
                1 for row in rows if row.row_kind == "fragrance_statement_current_window"
            ),
            preserved_review_tabs=sum(1 for row in rows if row.row_kind == "fragrance_review_tab"),
            preserved_bindings=len(bindings),
            text_row_counts_by_tab={str(key): count for key, count in sorted(text_counts.items())},
            hierarchy_preserved=True,
            source_order_preserved=True,
        ),
        residuals=_dedupe_preserve_order(residuals),
    )


def build_parfumo_targeted_content_record(
    *,
    rendered_dom: bytes,
    visible_text: bytes,
    source_url: str,
) -> dict[str, Any]:
    """Parse the pinned rendered route without embedding future packet identity."""
    if not source_url.strip():
        raise ValueError("source_url must be non-empty")

    rows: list[ParfumoTargetedContentRow] = []
    bindings: list[ParfumoTargetedContentBinding] = []
    residuals: list[str] = []
    inputs = (
        ("rendered_dom", "rendered_dom.html", rendered_dom),
        ("visible_text", "visible_text.txt", visible_text),
    )
    for slice_id in _TARGETED_SLICE_IDS:
        source_slice = _ContentSlice(slice_id=slice_id)
        for role, relative_path, body in inputs:
            if not _looks_like_parfumo_content_body(
                relative_path=relative_path,
                body=body,
                source_surface=PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE,
            ):
                continue
            raw_ref = ParfumoProjectionRawRef(
                packet_id="content_record_unbound",
                slice_id=slice_id,
            )
            raw_anchor = ParfumoProjectionRawAnchor(
                file_id=f"content_input_{role}",
                relative_packet_path=relative_path,
                sha256=hashlib.sha256(body).hexdigest(),
                hash_basis="raw_bytes",
            )
            projected = _project_parfumo_html(
                body,
                source_slice=source_slice,
                raw_ref=raw_ref,
                raw_anchor=raw_anchor,
                source_surface=PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE,
            )
            rows.extend(_content_row(row) for row in projected.rows)
            bindings.extend(_content_binding(binding) for binding in projected.bindings)
            residuals.extend(projected.residuals)

    text_counts = Counter(
        row.tab_id or row.row_kind
        for row in rows
        if row.row_kind
        in {"fragrance_review_card_current_window", "fragrance_statement_current_window"}
    )
    if not any(row.row_kind == "fragrance_review_card_current_window" for row in rows):
        residuals.append("parfumo_review_cards_absent")
    if not any(row.row_kind == "fragrance_statement_current_window" for row in rows):
        residuals.append("parfumo_statement_rows_absent")
    if not any(row.row_kind == "fragrance_product_snapshot" for row in rows):
        residuals.append("parfumo_product_snapshot_absent")

    record = ParfumoTargetedContentRecord(
        source_url=source_url,
        rows=rows,
        binding_map=bindings,
        loss_ledger=ParfumoProjectionLossLedger(
            preserved_evidence_rows=len(rows),
            preserved_review_cards=sum(
                1 for row in rows if row.row_kind == "fragrance_review_card_current_window"
            ),
            preserved_statements=sum(
                1 for row in rows if row.row_kind == "fragrance_statement_current_window"
            ),
            preserved_review_tabs=sum(
                1 for row in rows if row.row_kind == "fragrance_review_tab"
            ),
            preserved_bindings=len(bindings),
            text_row_counts_by_tab={str(key): count for key, count in sorted(text_counts.items())},
            hierarchy_preserved=True,
            source_order_preserved=True,
        ),
        residuals=_dedupe_preserve_order(residuals),
    )
    return record.model_dump(mode="json")


def _projection_from_targeted_content_record(
    *,
    packet: SourceCapturePacket,
    content_file: PreservedFile,
    content_bytes: bytes,
) -> ParfumoProjectionPacket:
    if packet.source_surface != PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE:
        raise ValueError("Parfumo content records are valid only for the targeted rendered surface")
    try:
        loaded = json.loads(content_bytes.decode("utf-8"))
        record = ParfumoTargetedContentRecord.model_validate(loaded)
    except Exception as exc:
        raise ValueError(f"invalid Parfumo content record: {exc}") from exc
    if packet.source_locator.value != record.source_url:
        raise ValueError(
            f"Parfumo content record source_url {record.source_url!r} does not match "
            f"packet source locator {packet.source_locator.value!r}"
        )

    slice_by_id = {source_slice.slice_id: source_slice for source_slice in packet.source_slices}
    projection_rows: list[ParfumoProjectionRow] = []
    for index, content_row in enumerate(record.rows):
        source_slice = slice_by_id.get(content_row.slice_id)
        if source_slice is None:
            raise ValueError(
                f"Parfumo content row references unknown source slice: {content_row.slice_id}"
            )
        if content_file.file_id not in source_slice.preserved_file_ids:
            raise ValueError(
                f"Parfumo content row slice {content_row.slice_id!r} does not reference "
                "content_record.json"
            )
        row_data = content_row.model_dump(
            mode="json",
            exclude={"slice_id", "source_anchor_kind", "source_anchor_value"},
        )
        projection_rows.append(
            ParfumoProjectionRow(
                **row_data,
                raw_ref=ParfumoProjectionRawRef(
                    packet_id=packet.packet_id,
                    slice_id=content_row.slice_id,
                ),
                raw_anchor=_content_record_anchor(content_file, f"/rows/{index}"),
            )
        )

    projection_bindings: list[ParfumoProjectionBinding] = []
    for index, content_binding in enumerate(record.binding_map):
        source_slice = slice_by_id.get(content_binding.slice_id)
        if source_slice is None or content_file.file_id not in source_slice.preserved_file_ids:
            raise ValueError(
                f"Parfumo content binding references invalid source slice: "
                f"{content_binding.slice_id}"
            )
        projection_bindings.append(
            ParfumoProjectionBinding(
                binding_type=content_binding.binding_type,
                row_id=content_binding.row_id,
                raw_ref=ParfumoProjectionRawRef(
                    packet_id=packet.packet_id,
                    slice_id=content_binding.slice_id,
                ),
                raw_anchor=_content_record_anchor(content_file, f"/binding_map/{index}"),
            )
        )

    return ParfumoProjectionPacket(
        packet_id=packet.packet_id,
        rows=projection_rows,
        binding_map=projection_bindings,
        loss_ledger=record.loss_ledger,
        residuals=record.residuals,
    )


def _content_row(row: ParfumoProjectionRow) -> ParfumoTargetedContentRow:
    row_data = row.model_dump(mode="json", exclude={"raw_ref", "raw_anchor"})
    return ParfumoTargetedContentRow(
        **row_data,
        slice_id=row.raw_ref.slice_id,
        source_anchor_kind=row.raw_anchor.anchor_kind,
        source_anchor_value=row.raw_anchor.anchor_value,
    )


def _content_binding(binding: ParfumoProjectionBinding) -> ParfumoTargetedContentBinding:
    return ParfumoTargetedContentBinding(
        slice_id=binding.raw_ref.slice_id,
        binding_type=binding.binding_type,
        row_id=binding.row_id,
    )


def _content_record_anchor(
    content_file: PreservedFile,
    json_pointer: str,
) -> ParfumoProjectionRawAnchor:
    return ParfumoProjectionRawAnchor(
        file_id=content_file.file_id,
        relative_packet_path=content_file.relative_packet_path,
        sha256=content_file.sha256,
        hash_basis=content_file.hash_basis,
        anchor_kind="json_pointer",
        json_pointer=json_pointer,
    )


def build_parfumo_projection_from_packet_directory(
    *,
    packet_or_manifest_path: Path,
) -> ParfumoProjectionPacket:
    packet, raw_file_bytes_by_file_id = _read_packet_directory(packet_or_manifest_path)
    return build_parfumo_projection(
        packet=packet,
        raw_file_bytes_by_file_id=raw_file_bytes_by_file_id,
    )


def write_parfumo_projection(
    *,
    packet_or_manifest_path: Path,
    output_path: Path,
    overwrite: bool = False,
) -> ParfumoProjectionPacket:
    projection = build_parfumo_projection_from_packet_directory(
        packet_or_manifest_path=packet_or_manifest_path,
    )
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_projection_json_text(projection), encoding="utf-8")
    return projection


def project_parfumo_into_lake(
    *,
    data_root: "DataLakeRoot",
    packet_id: str,
    record_id: str | None = None,
) -> tuple[ParfumoProjectionPacket, Path]:
    """Project a committed Parfumo raw packet into an append-only derived record."""
    loaded = data_root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    projection = build_parfumo_projection(
        packet=packet,
        raw_file_bytes_by_file_id=loaded.bodies,
    )
    record = record_id if record_id is not None else generate_ulid()
    derived_path = data_root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=PROJECTION_PARFUMO_LANE,
        record_id=f"{record}.json",
        data=_projection_json_text(projection).encode("utf-8"),
    )
    return projection, derived_path


class _ProjectedParfumoHtml(StrictModel):
    rows: list[ParfumoProjectionRow] = Field(default_factory=list)
    bindings: list[ParfumoProjectionBinding] = Field(default_factory=list)
    residuals: list[str] = Field(default_factory=list)


class _SliceIdentity(Protocol):
    slice_id: str


@dataclass(frozen=True)
class _ContentSlice:
    slice_id: str


@dataclass(frozen=True)
class _TextCardStart:
    start: int
    tag: str
    explicit_id: str | None = None


def _project_parfumo_html(
    body: bytes,
    *,
    source_slice: _SliceIdentity,
    raw_ref: ParfumoProjectionRawRef,
    raw_anchor: ParfumoProjectionRawAnchor,
    source_surface: str,
) -> _ProjectedParfumoHtml:
    text = body.decode("utf-8", errors="replace")
    product = _product_context(text)
    rows: list[ParfumoProjectionRow] = []
    bindings: list[ParfumoProjectionBinding] = []
    residuals: list[str] = []
    source_object_site_id = product.get("source_object_site_id")
    source_object_name = product.get("source_object_name")
    brand_or_house = product.get("brand_or_house")

    rows.append(
        ParfumoProjectionRow(
            row_id=f"{source_slice.slice_id}:parfumo:product_snapshot",
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

    review_rows, review_bindings = _text_card_rows(
        text,
        kind="review",
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

    statement_rows, statement_bindings = _text_card_rows(
        text,
        kind="statement",
        raw_ref=raw_ref,
        raw_anchor=raw_anchor,
        source_slice=source_slice,
        source_object_site_id=source_object_site_id,
        source_object_name=source_object_name,
        brand_or_house=brand_or_house,
        tab_labels=tab_labels,
    )
    rows.extend(statement_rows)
    bindings.extend(statement_bindings)

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
        residuals.append("parfumo_aggregate_rating_absent")
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
    if any(row.source_visible_fields.get("corpus_kind") == "reviews" for row in archive_gate_rows):
        residuals.append("full_review_corpus_not_captured_ajax_pagination_present")
    if any(row.source_visible_fields.get("corpus_kind") == "statements" for row in archive_gate_rows):
        residuals.append("full_statement_corpus_not_captured_ajax_pagination_present")

    if source_surface == PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE:
        residuals.append("linked_media_assets_not_preserved_by_targeted_rendered_packet")
    else:
        residuals.append("linked_media_assets_not_preserved_by_direct_http_packet")
    residuals.append("review_attached_photo_proof_not_present")
    residuals.extend(_non_text_fragrance_scope_residuals(text))

    projected = _ProjectedParfumoHtml(
        rows=rows,
        bindings=bindings,
        residuals=_dedupe_preserve_order(residuals),
    )
    if source_surface == PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE:
        return _filter_targeted_projection(projected, source_slice=source_slice)
    return projected


def _filter_targeted_projection(
    projected: _ProjectedParfumoHtml,
    *,
    source_slice: _SliceIdentity,
) -> _ProjectedParfumoHtml:
    slice_id = source_slice.slice_id
    kept_rows: list[ParfumoProjectionRow]
    residuals: list[str] = []

    if slice_id == _TARGETED_PRODUCT_CONTEXT_SLICE:
        kept_rows = [
            row
            for row in projected.rows
            if row.row_kind
            in {
                "fragrance_product_snapshot",
                "fragrance_aggregate_rating",
                "fragrance_performance_component",
                "fragrance_review_archive_gate",
            }
        ]
        residuals.extend(projected.residuals)
    elif slice_id == _TARGETED_REVIEW_LATEST_RECENT_SLICE:
        kept_rows = [
            row
            for row in projected.rows
            if row.row_kind == "fragrance_review_card_current_window"
            and _targeted_review_slice_id(row) == slice_id
        ]
        if not kept_rows:
            residuals.append("parfumo_latest_recent_review_bucket_absent_or_unexposed")
    elif slice_id == _TARGETED_REVIEW_HIGH_RATING_SLICE:
        kept_rows = [
            row
            for row in projected.rows
            if row.row_kind == "fragrance_review_card_current_window"
            and _targeted_review_slice_id(row) == slice_id
        ]
        if not kept_rows:
            residuals.append("parfumo_high_rating_review_bucket_absent_or_unexposed")
    elif slice_id == _TARGETED_REVIEW_LOW_RATING_SLICE:
        kept_rows = [
            row
            for row in projected.rows
            if row.row_kind == "fragrance_review_card_current_window"
            and _targeted_review_slice_id(row) == slice_id
        ]
        if not kept_rows:
            residuals.append("parfumo_low_rating_review_bucket_absent_or_unexposed")
    elif slice_id == _TARGETED_STATEMENT_LATEST_RECENT_SLICE:
        kept_rows = [
            row
            for row in projected.rows
            if row.row_kind == "fragrance_statement_current_window"
            and _is_latest_or_recent_statement(row)
        ]
        if not kept_rows:
            residuals.append("parfumo_latest_recent_statement_bucket_absent_or_unexposed")
    else:
        kept_rows = []
        residuals.append("parfumo_targeted_slice_id_unrecognized")

    kept_row_ids = {row.row_id for row in kept_rows}
    kept_bindings = [binding for binding in projected.bindings if binding.row_id in kept_row_ids]
    return _ProjectedParfumoHtml(
        rows=kept_rows,
        bindings=kept_bindings,
        residuals=_dedupe_preserve_order(residuals),
    )


def _targeted_review_slice_id(row: ParfumoProjectionRow) -> str:
    """Return the one targeted review slice this source-visible review belongs to."""
    tab_id = row.source_visible_fields.get("tab_id")
    if tab_id == "order_scent_desc":
        return _TARGETED_REVIEW_HIGH_RATING_SLICE
    if tab_id == "order_scent_asc":
        return _TARGETED_REVIEW_LOW_RATING_SLICE
    if _has_high_rating_bucket_cue(row):
        return _TARGETED_REVIEW_HIGH_RATING_SLICE
    if _has_low_rating_bucket_cue(row):
        return _TARGETED_REVIEW_LOW_RATING_SLICE
    return _TARGETED_REVIEW_LATEST_RECENT_SLICE



def _is_latest_or_recent_statement(row: ParfumoProjectionRow) -> bool:
    fields = row.source_visible_fields
    return _field_mentions_any(
        fields,
        "tab_id",
        "tab_label",
        tokens=(*_LATEST_REVIEW_TOKENS, "statement"),
    ) or row.tab_id in {None, "statements"}



def _has_high_rating_bucket_cue(row: ParfumoProjectionRow) -> bool:
    fields = row.source_visible_fields
    return _field_mentions_any(
        fields,
        "tab_id",
        "tab_label",
        tokens=_HIGH_RATING_BUCKET_TOKENS,
    )


def _has_low_rating_bucket_cue(row: ParfumoProjectionRow) -> bool:
    fields = row.source_visible_fields
    return _field_mentions_any(
        fields,
        "tab_id",
        "tab_label",
        tokens=_LOW_RATING_BUCKET_TOKENS,
    )


def _field_mentions_any(
    fields: Mapping[str, Any | None],
    *names: str,
    tokens: tuple[str, ...],
) -> bool:
    values = []
    for name in names:
        value = fields.get(name)
        if isinstance(value, str):
            values.append(value.lower())
    if not values:
        return False
    text = " ".join(values)
    field_tokens = {token for token in re.split(r"[^a-z0-9]+", text) if token}
    return any(token in field_tokens for token in tokens)


def _numeric_field(value: Any | None) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _product_context(text: str) -> dict[str, Any | None]:
    canonical_url = _first_match(
        text,
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
        flags=re.IGNORECASE,
    )
    if canonical_url is None:
        canonical_url = _first_match(
            text,
            r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']',
            flags=re.IGNORECASE,
        )
    title = _text(_first_match(text, r"<title>(.*?)</title>", flags=re.IGNORECASE | re.DOTALL))
    meta_description = _first_match(
        text,
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)["\']',
        flags=re.IGNORECASE,
    )
    site_id = _first_match(
        text,
        r'(?:data-perfume-id|data-pid|name=["\']p_id["\'][^>]*value)=["\']?(\d+)',
        flags=re.IGNORECASE,
    )
    if site_id is None:
        site_id = _first_match(
            text,
            r'(?:"p_id"|p_id|perfume_id)\s*[:=]\s*["\']?(\d+)',
            flags=re.IGNORECASE,
        )
    product_name = None
    brand_or_house = None
    if title:
        match = re.search(r"(.+?)\s+by\s+(.+?)(?:\s+\(|\s*&|\s+-|$)", title, flags=re.IGNORECASE)
        if match:
            product_name = _text(match.group(1))
            brand_or_house = _text(match.group(2))
    if product_name is None and canonical_url:
        product_name = _name_from_parfumo_url(canonical_url)
    if brand_or_house is None and canonical_url:
        brand_or_house = _brand_from_parfumo_url(canonical_url)

    return {
        "source_platform": "parfumo",
        "source_object_type": "fragrance_product",
        "source_object_site_id": site_id,
        "source_object_name": product_name,
        "brand_or_house": brand_or_house,
        "canonical_url": canonical_url,
        "page_title": title,
        "meta_description": html.unescape(meta_description) if meta_description else None,
        "ajax_hash": _ajax_hash(text),
    }


def _product_residuals(product: Mapping[str, Any | None]) -> list[str]:
    residuals = []
    for field in ("source_object_site_id", "source_object_name", "brand_or_house", "canonical_url"):
        if product.get(field) in {None, ""}:
            residuals.append(f"{field}_absent")
    return residuals


def _non_text_fragrance_scope_residuals(text: str) -> list[str]:
    residuals = []
    if re.search(r"\bnotes?\b", text, flags=re.IGNORECASE):
        residuals.append("fragrance_notes_surface_present_but_not_projected")
    if re.search(r"\b(?:scent|longevity|sillage)\b", text, flags=re.IGNORECASE):
        residuals.append("fragrance_performance_surface_partially_projected")
    if re.search(r"\bphotos?\b", text, flags=re.IGNORECASE):
        residuals.append("fragrance_photo_surface_present_but_not_projected")
    return residuals


def _review_tab_rows(
    text: str,
    *,
    raw_ref: ParfumoProjectionRawRef,
    raw_anchor: ParfumoProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
    source_object_site_id: str | None,
    source_object_name: str | None,
    brand_or_house: str | None,
) -> list[ParfumoProjectionRow]:
    rows = []
    tab_matches: list[tuple[str, str, str, str | None, bool]] = []
    pattern = re.compile(
        r'<(?:button|a)[^>]+data-tab=["\']([^"\']+)["\'][^>]*>(.*?)</(?:button|a)>',
        flags=re.IGNORECASE | re.DOTALL,
    )
    for match in pattern.finditer(text):
        tab_id = match.group(1)
        tab_body = match.group(0)
        tab_matches.append(
            (
                tab_id,
                match.group(2),
                f'[data-tab="{tab_id}"]',
                _first_match(match.group(2), r"([\d,.]+)"),
                _attr_present(tab_body, "data-active", "true")
                or _attr_present(tab_body, "aria-selected", "true"),
            )
        )

    order_pattern = re.compile(
        r'<div[^>]+class=["\'][^"\']*\baction_reviews_order\b[^"\']*["\'][^>]+data-o=["\']([^"\']+)["\'][^>]*>(.*?)</div>',
        flags=re.IGNORECASE | re.DOTALL,
    )
    for match in order_pattern.finditer(text):
        tab_id = match.group(1)
        tab_body = match.group(0)
        tab_matches.append(
            (
                tab_id,
                match.group(2),
                f'[data-o="{tab_id}"]',
                None,
                "active" in ((_attr_value(tab_body, "class") or "").split()),
            )
        )

    for index, (tab_id, label_html, anchor_value, displayed_count, active) in enumerate(
        tab_matches, start=1
    ):
        rows.append(
            ParfumoProjectionRow(
                row_id=f"{source_slice.slice_id}:parfumo:review_tab:{tab_id}",
                row_kind="fragrance_review_tab",
                raw_ref=raw_ref,
                raw_anchor=_with_anchor(raw_anchor, "html_selector", anchor_value),
                source_object_site_id=source_object_site_id,
                source_object_name=source_object_name,
                brand_or_house=brand_or_house,
                tab_id=tab_id,
                source_order=index,
                source_visible_fields={
                    "tab_id": tab_id,
                    "tab_label": _text(label_html),
                    "active": active,
                    "displayed_count": _parse_count(displayed_count),
                },
            )
        )
    return rows


def _text_card_rows(
    text: str,
    *,
    kind: Literal["review", "statement"],
    raw_ref: ParfumoProjectionRawRef,
    raw_anchor: ParfumoProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
    source_object_site_id: str | None,
    source_object_name: str | None,
    brand_or_house: str | None,
    tab_labels: Mapping[str | None, Any | None],
) -> tuple[list[ParfumoProjectionRow], list[ParfumoProjectionBinding]]:
    starts = _text_card_starts(text, kind=kind)
    rows: list[ParfumoProjectionRow] = []
    bindings: list[ParfumoProjectionBinding] = []
    source_order_by_tab: Counter[str] = Counter()
    seen: set[tuple[str, str]] = set()
    for index, start in enumerate(starts):
        segment_end = starts[index + 1].start if index + 1 < len(starts) else len(text)
        segment = _bounded_segment(text, start.start, segment_end, start.tag)
        item_id = _text_card_item_id(segment, kind=kind, explicit_id=start.explicit_id)
        if item_id is None:
            continue
        seen_key = (kind, item_id)
        if seen_key in seen:
            continue
        seen.add(seen_key)
        tab_id = _text_card_tab_id(kind=kind, segment=segment, position=start.start, text=text)
        source_order_by_tab[str(tab_id)] += 1
        row_kind = (
            "fragrance_review_card_current_window"
            if kind == "review"
            else "fragrance_statement_current_window"
        )
        row_id = f"{source_slice.slice_id}:parfumo:{kind}:{tab_id or 'unknown'}:{item_id}"
        row_anchor = _with_anchor(raw_anchor, "html_selector", _text_card_anchor(kind, item_id))
        row = ParfumoProjectionRow(
            row_id=row_id,
            row_kind=row_kind,
            raw_ref=raw_ref,
            raw_anchor=row_anchor,
            source_object_site_id=source_object_site_id,
            source_object_name=source_object_name,
            brand_or_house=brand_or_house,
            tab_id=tab_id,
            source_order=source_order_by_tab[str(tab_id)],
            comment_id=item_id,
            source_visible_fields=_text_row_fields(
                segment,
                item_id=item_id,
                kind=kind,
                tab_id=tab_id,
                tab_label=tab_labels.get(tab_id),
            ),
            residuals=_text_row_residuals(segment, kind=kind),
        )
        rows.append(row)
        bindings.append(
            ParfumoProjectionBinding(
                binding_type=(
                    "review_metadata_to_review_text"
                    if kind == "review"
                    else "statement_metadata_to_statement_text"
                ),
                row_id=row_id,
                raw_ref=raw_ref,
                raw_anchor=row_anchor,
            )
        )
    return rows, bindings


def _text_card_starts(text: str, *, kind: Literal["review", "statement"]) -> list[_TextCardStart]:
    attr = f"data-{kind}-id"
    starts: list[_TextCardStart] = []
    data_attr_pattern = re.compile(
        rf'<(?P<tag>article|div|li)[^>]*\b{attr}=["\'](?P<id>[^"\']+)["\'][^>]*>',
        flags=re.IGNORECASE,
    )
    for match in data_attr_pattern.finditer(text):
        starts.append(
            _TextCardStart(
                start=match.start(),
                tag=match.group("tag"),
                explicit_id=html.unescape(match.group("id")).strip(),
            )
        )

    if kind == "review":
        live_review_pattern = re.compile(
            r'<(?P<tag>article)\b(?=[^>]*(?:itemprop=["\']review["\']|class=["\'][^"\']*\breview(?:[\s_-]|["\'])))[^>]*>',
            flags=re.IGNORECASE,
        )
        starts.extend(
            _TextCardStart(start=match.start(), tag=match.group("tag"))
            for match in live_review_pattern.finditer(text)
        )
    else:
        live_statement_pattern = re.compile(
            r'<(?P<tag>div)\b(?=[^>]*class=["\'][^"\']*\bstatement-bubble\b)[^>]*>',
            flags=re.IGNORECASE,
        )
        starts.extend(
            _TextCardStart(start=match.start(), tag=match.group("tag"))
            for match in live_statement_pattern.finditer(text)
        )

    return sorted(starts, key=lambda item: item.start)


def _text_card_item_id(
    segment: str,
    *,
    kind: Literal["review", "statement"],
    explicit_id: str | None,
) -> str | None:
    if explicit_id:
        return explicit_id
    if kind == "review":
        return (
            _first_match(segment, r"\breview_article_([A-Za-z0-9_-]+)", flags=re.IGNORECASE)
            or _first_match(segment, r'\bid=["\']review_([^"\']+)["\']', flags=re.IGNORECASE)
            or _first_match(segment, r'/reviews/([^"\'/?#\s]+)', flags=re.IGNORECASE)
        )
    return (
        _first_match(segment, r'/statements/([^"\'/?#\s]+)', flags=re.IGNORECASE)
        or _first_match(segment, r'\bid=["\']s_text(?:_content)?_([^"\']+)["\']', flags=re.IGNORECASE)
    )


def _text_card_anchor(kind: Literal["review", "statement"], item_id: str) -> str:
    if kind == "review":
        return f'[data-review-id="{item_id}"], article.review_article_{item_id}, a[href*="/reviews/{item_id}"]'
    return f'[data-statement-id="{item_id}"], a[href*="/statements/{item_id}"], #s_text_content_{item_id}'


def _text_row_fields(
    segment: str,
    *,
    item_id: str,
    kind: Literal["review", "statement"],
    tab_id: str | None,
    tab_label: Any | None,
) -> dict[str, Any | None]:
    text_field = "review_text" if kind == "review" else "statement_text"
    text_value = _source_text(segment, kind=kind)
    return {
        f"{kind}_id": item_id,
        "tab_id": tab_id,
        "tab_label": tab_label,
        "author_display_name": _author_name(segment),
        "author_profile_url": _first_match(
            segment,
            r'<a[^>]+href=["\']([^"\']*(?:/Users/|/User/)[^"\']+)["\']',
            flags=re.IGNORECASE,
        ),
        "date_published": _date_published(segment),
        "date_display_text": _date_display_text(segment),
        text_field: text_value,
        f"{kind}_text_length_chars": len(text_value) if text_value is not None else None,
        "rating": _text_row_rating(segment),
        "helpful_count": _parse_count(_attr_value(segment, "data-helpful-count")),
        "source_item_url": _source_item_url(segment, kind=kind, item_id=item_id),
    }


def _source_item_url(
    segment: str,
    *,
    kind: Literal["review", "statement"],
    item_id: str,
) -> str | None:
    path = "reviews" if kind == "review" else "statements"
    escaped_id = re.escape(item_id)
    return (
        _first_match(
            segment,
            rf'<a[^>]+href=["\']([^"\']*/Perfumes/[^"\']*/{path}/{escaped_id}[^"\']*)["\']',
            flags=re.IGNORECASE,
        )
        or _first_match(
            segment,
            rf'<a[^>]+href=["\']([^"\']*/{path}/{escaped_id}[^"\']*)["\']',
            flags=re.IGNORECASE,
        )
    )


def _text_row_residuals(segment: str, *, kind: Literal["review", "statement"]) -> list[str]:
    residuals = []
    if _author_name(segment) is None:
        residuals.append("author_display_name_absent")
    if _date_published(segment) is None:
        residuals.append("date_published_absent")
    if _source_text(segment, kind=kind) is None:
        residuals.append(f"{kind}_text_absent")
    return residuals


def _aggregate_rating_row(
    text: str,
    *,
    raw_ref: ParfumoProjectionRawRef,
    raw_anchor: ParfumoProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
    source_object_site_id: str | None,
    source_object_name: str | None,
    brand_or_house: str | None,
) -> ParfumoProjectionRow | None:
    fields = {
        "rating_value": _to_float(_attr_value(text, "data-rating-value"))
        or _to_float(_first_match(text, r'itemprop=["\']ratingValue["\'][^>]*>([^<]+)<')),
        "rating_count": _parse_count(_attr_value(text, "data-rating-count"))
        or _parse_count(_first_match(text, r"([\d,.]+)\s+Ratings?", flags=re.IGNORECASE)),
        "declared_reviews": _parse_count(_attr_value(text, "data-review-count"))
        or _parse_count(_first_match(text, r"([\d,.]+)\s+Reviews?", flags=re.IGNORECASE)),
        "declared_statements": _parse_count(_attr_value(text, "data-statement-count"))
        or _parse_count(_first_match(text, r"([\d,.]+)\s+Statements?", flags=re.IGNORECASE)),
        "scent_rating": _to_float(_attr_value(text, "data-scent-rating")),
        "longevity_rating": _to_float(_attr_value(text, "data-longevity-rating")),
        "sillage_rating": _to_float(_attr_value(text, "data-sillage-rating")),
    }
    if all(value is None for value in fields.values()):
        return None
    return ParfumoProjectionRow(
        row_id=f"{source_slice.slice_id}:parfumo:aggregate_rating",
        row_kind="fragrance_aggregate_rating",
        raw_ref=raw_ref,
        raw_anchor=_with_anchor(raw_anchor, "text_pattern", "Ratings|Reviews|Statements"),
        source_object_site_id=source_object_site_id,
        source_object_name=source_object_name,
        brand_or_house=brand_or_house,
        source_visible_fields=fields,
    )


def _performance_component_rows(
    text: str,
    *,
    raw_ref: ParfumoProjectionRawRef,
    raw_anchor: ParfumoProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
    source_object_site_id: str | None,
    source_object_name: str | None,
    brand_or_house: str | None,
) -> list[ParfumoProjectionRow]:
    rows = []
    for component, attr_name in (
        ("scent", "data-scent-rating"),
        ("longevity", "data-longevity-rating"),
        ("sillage", "data-sillage-rating"),
    ):
        value = _to_float(_attr_value(text, attr_name))
        if value is None:
            value = _to_float(
                _first_match(
                    text,
                    rf"\b{component}\b\s*[: ]\s*([0-9]+(?:[.,][0-9]+)?)",
                    flags=re.IGNORECASE,
                )
            )
        if value is None:
            continue
        rows.append(
            ParfumoProjectionRow(
                row_id=f"{source_slice.slice_id}:parfumo:performance_component:{component}",
                row_kind="fragrance_performance_component",
                raw_ref=raw_ref,
                raw_anchor=_with_anchor(raw_anchor, "text_pattern", component),
                source_object_site_id=source_object_site_id,
                source_object_name=source_object_name,
                brand_or_house=brand_or_house,
                source_visible_fields={"component": component, "component_value": value},
            )
        )
    return rows


def _archive_gate_rows(
    text: str,
    *,
    raw_ref: ParfumoProjectionRawRef,
    raw_anchor: ParfumoProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
    source_object_site_id: str | None,
    source_object_name: str | None,
    brand_or_house: str | None,
) -> list[ParfumoProjectionRow]:
    rows = []
    endpoints = (
        ("reviews", "/action/perfume/get_reviews.php"),
        ("statements", "/action/perfume/get_statements.php"),
    )
    for corpus_kind, endpoint in endpoints:
        if endpoint not in text:
            continue
        rows.append(
            ParfumoProjectionRow(
                row_id=f"{source_slice.slice_id}:parfumo:archive_gate:{corpus_kind}",
                row_kind="fragrance_review_archive_gate",
                raw_ref=raw_ref,
                raw_anchor=_with_anchor(raw_anchor, "text_pattern", endpoint),
                source_object_site_id=source_object_site_id,
                source_object_name=source_object_name,
                brand_or_house=brand_or_house,
                source_visible_fields={
                    "corpus_kind": corpus_kind,
                    "endpoint_path": endpoint,
                    "perfume_id": source_object_site_id,
                    "ajax_hash": _ajax_hash(text),
                    "pagination_posture": "ajax_endpoint_observed_but_not_invoked_by_projection",
                },
                residuals=[
                    f"full_{corpus_kind[:-1] if corpus_kind.endswith('s') else corpus_kind}_corpus_not_captured"
                ],
            )
        )
    return rows


def _looks_like_parfumo_body(
    preserved_file: PreservedFile,
    body: bytes,
    *,
    source_surface: str,
) -> bool:
    path = preserved_file.relative_packet_path.lower()
    return _looks_like_parfumo_content_body(
        relative_path=path,
        body=body,
        source_surface=source_surface,
    )


def _looks_like_parfumo_content_body(
    *,
    relative_path: str,
    body: bytes,
    source_surface: str,
) -> bool:
    path = relative_path.lower()
    if "http_response_metadata" in path:
        return False
    sample = body[:200_000].decode("utf-8", errors="ignore").lower()
    if source_surface == PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE:
        if path.endswith((".json", ".png", ".jpg", ".jpeg", ".webp")):
            return False
        return (
            "<html" in sample
            or "data-perfume-id" in sample
            or "data-review-id" in sample
            or "data-statement-id" in sample
            or 'itemprop="review"' in sample
            or "statement-bubble" in sample
        )
    return (
        "parfumo.com/perfumes/" in sample
        or "/action/perfume/get_reviews.php" in sample
        or "perfume facts" in sample
    )


def _raw_anchor(preserved_file: PreservedFile) -> ParfumoProjectionRawAnchor:
    return ParfumoProjectionRawAnchor(
        file_id=preserved_file.file_id,
        relative_packet_path=preserved_file.relative_packet_path,
        sha256=preserved_file.sha256,
        hash_basis=preserved_file.hash_basis,
    )


def _with_anchor(
    raw_anchor: ParfumoProjectionRawAnchor,
    anchor_kind: Literal["html_selector", "text_pattern"],
    anchor_value: str,
) -> ParfumoProjectionRawAnchor:
    return ParfumoProjectionRawAnchor(
        file_id=raw_anchor.file_id,
        relative_packet_path=raw_anchor.relative_packet_path,
        sha256=raw_anchor.sha256,
        hash_basis=raw_anchor.hash_basis,
        anchor_kind=anchor_kind,
        anchor_value=anchor_value,
    )


def _bounded_segment(text: str, start: int, max_end: int, tag: str) -> str:
    depth = 0
    tag_pattern = re.compile(rf"</?{re.escape(tag)}\b[^>]*>", flags=re.IGNORECASE)
    for match in tag_pattern.finditer(text[start:max_end]):
        token = match.group(0)
        if token.startswith("</"):
            depth -= 1
            if depth == 0:
                return text[start : start + match.end()]
        elif not token.endswith("/>"):
            depth += 1
    return text[start:max_end]


def _text_card_tab_id(
    *,
    kind: Literal["review", "statement"],
    segment: str,
    position: int,
    text: str,
) -> str | None:
    explicit = _attr_value(segment, "data-tab") or _attr_value(segment, "data-section")
    if explicit:
        return explicit
    if kind == "statement":
        return "statements"
    active_order = _active_review_order_tab_before(text, position)
    if active_order is not None:
        return active_order
    panels: list[tuple[int, str]] = []
    for match in re.finditer(r"<[^>]+>", text, flags=re.IGNORECASE):
        tag = match.group(0)
        tab_id = _attr_value(tag, "data-tab-panel")
        if tab_id is None and (_attr_value(tag, "role") or "").lower() == "tabpanel":
            tab_id = _attr_value(tag, "id")
        if tab_id:
            panels.append((match.start(), tab_id))
    active = None
    for panel_start, tab_id in panels:
        if panel_start <= position:
            active = tab_id
        else:
            break
    return active or "reviews"


def _active_review_order_tab_before(text: str, position: int) -> str | None:
    active = None
    pattern = re.compile(r"<[^>]+>", flags=re.IGNORECASE)
    for match in pattern.finditer(text[:position]):
        tag = match.group(0)
        if _attr_value(tag, "data-o") is None:
            continue
        class_value = _attr_value(tag, "class") or ""
        if "action_reviews_order" not in class_value.split():
            continue
        if "active" in class_value.split():
            active = _attr_value(tag, "data-o")
    return active


def _source_text(segment: str, *, kind: Literal["review", "statement"]) -> str | None:
    id_prefix = "r" if kind == "review" else "s"
    for pattern in (
        rf'<[^>]+id=["\']{id_prefix}_text_content_[^"\']+["\'][^>]*>(.*?)</[^>]+>',
        rf'<[^>]+id=["\']{id_prefix}_text_[^"\']+["\'][^>]*>(.*?)</[^>]+>',
        r'<[^>]+itemprop=["\']reviewBody["\'][^>]*>\s*<[^>]+id=["\']r_text_[^"\']+["\'][^>]*>(.*?)</[^>]+>',
        rf'<[^>]+data-role=["\']{kind}-text["\'][^>]*>(.*?)</[^>]+>',
        r'<p[^>]+class=["\'][^"\']*(?:review|statement)[_-]?text[^"\']*["\'][^>]*>(.*?)</p>',
        r"<p[^>]*>(.*?)</p>",
    ):
        value = _text(_first_match(segment, pattern, flags=re.IGNORECASE | re.DOTALL))
        if value:
            return value
    return None


def _author_name(segment: str) -> str | None:
    value = (
        _attr_value(segment, "data-author")
        or _first_match(
            segment,
            r'itemprop=["\']author["\'][^>]*>.*?itemprop=["\']name["\'][^>]*>(.*?)</[^>]+>',
            flags=re.IGNORECASE | re.DOTALL,
        )
        or _first_match(
            segment,
            r'<[^>]+class=["\'][^"\']*author[^"\']*["\'][^>]*>(.*?)</[^>]+>',
            flags=re.IGNORECASE | re.DOTALL,
        )
        or _first_match(segment, r'<meta[^>]+itemprop=["\']author["\'][^>]+content=["\']([^"\']+)["\']')
        or _first_match(segment, r'/Users/([^"\'/?#\s]+)', flags=re.IGNORECASE)
    )
    return _clean_author_name(value)


def _clean_author_name(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = _text(unquote(value))
    return cleaned or None


def _date_published(segment: str) -> str | None:
    return (
        _first_match(segment, r'<time[^>]+datetime=["\']([^"\']+)["\']', flags=re.IGNORECASE)
        or _first_match(
            segment,
            r'itemprop=["\']datePublished["\'][^>]+content=["\']([^"\']+)["\']',
            flags=re.IGNORECASE,
        )
        or _first_match(
            segment,
            r'<meta[^>]+itemprop=["\']datePublished["\'][^>]+content=["\']([^"\']+)["\']',
            flags=re.IGNORECASE,
        )
    )


def _date_display_text(segment: str) -> str | None:
    return (
        _text(_first_match(segment, r"<time[^>]*>(.*?)</time>", flags=re.IGNORECASE | re.DOTALL))
        or _text(
            _first_match(
                segment,
                r'itemprop=["\']datePublished["\'][^>]*>(.*?)</[^>]+>',
                flags=re.IGNORECASE | re.DOTALL,
            )
        )
        or _text(
            _first_match(
                segment,
                r'<[^>]+class=["\'][^"\']*\b(?:lightblue2|date|time)[^"\']*["\'][^>]*>(.*?)</[^>]+>',
                flags=re.IGNORECASE | re.DOTALL,
            )
        )
    )


def _text_row_rating(segment: str) -> float | None:
    return (
        _to_float(_attr_value(segment, "data-rating"))
        or _to_float(
            _first_match(
                segment,
                r'itemprop=["\']ratingValue["\'][^>]+content=["\']([^"\']+)["\']',
                flags=re.IGNORECASE,
            )
        )
        or _to_float(
            _first_match(
                segment,
                r'<[^>]+itemprop=["\']ratingValue["\'][^>]*>([^<]+)</[^>]+>',
                flags=re.IGNORECASE,
            )
        )
        or _to_float(
            _first_match(
                segment,
                r'<span[^>]+class=["\'][^"\']*\bnr\b[^"\']*\bblue\b[^"\']*["\'][^>]*>\s*([0-9]+(?:[.,][0-9]+)?)\s*</span>\s*Scent',
                flags=re.IGNORECASE,
            )
        )
    )


def _ajax_hash(text: str) -> str | None:
    return (
        _first_match(text, r'name=["\']h["\'][^>]+value=["\']([^"\']+)["\']', flags=re.IGNORECASE)
        or _first_match(text, r'["\']h["\']\s*[:=]\s*["\']([^"\']+)["\']', flags=re.IGNORECASE)
    )


def _attr_value(segment: str, name: str) -> str | None:
    return _first_match(
        segment,
        rf'\b{re.escape(name)}\s*=\s*["\']([^"\']+)["\']',
        flags=re.IGNORECASE,
    )


def _attr_present(segment: str, name: str, value: str) -> bool:
    return bool(re.search(rf'\b{re.escape(name)}\s*=\s*["\']{re.escape(value)}["\']', segment))


def _to_float(value: str | None) -> float | None:
    if value is None:
        return None
    try:
        return float(value.replace(",", ".").strip())
    except ValueError:
        return None


def _parse_count(value: str | None) -> int | None:
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
    elif "." in normalized:
        normalized = normalized.replace(".", "")
    try:
        return int(float(normalized) * multiplier)
    except ValueError:
        return None


def _name_from_parfumo_url(url: str) -> str | None:
    match = re.search(r"/Perfumes/[^/]+/([^/?#]+)", url, flags=re.IGNORECASE)
    if match is None:
        return None
    return html.unescape(match.group(1).replace("_", " ").replace("-", " "))


def _brand_from_parfumo_url(url: str) -> str | None:
    match = re.search(r"/Perfumes/([^/]+)/", url, flags=re.IGNORECASE)
    if match is None:
        return None
    return html.unescape(match.group(1).replace("_", " ").replace("-", " "))


def _is_forbidden_field_name(key: str) -> bool:
    return is_forbidden_field_pattern_match(key, _FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES)


def _projection_json_text(projection: ParfumoProjectionPacket) -> str:
    return f"{json.dumps(projection.model_dump(mode='json'), indent=2, sort_keys=True)}\n"


__all__ = [
    "PARFUMO_DIRECT_HTTP_SOURCE_SURFACE",
    "PARFUMO_PROJECTION_CERTIFICATION",
    "PARFUMO_PROJECTION_METHOD",
    "PARFUMO_PROJECTION_VERSION",
    "PARFUMO_TARGETED_CONTENT_RECORD_KIND",
    "PARFUMO_TARGETED_CONTENT_SCHEMA_VERSION",
    "PARFUMO_TARGETED_PARSER_VERSION",
    "PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE",
    "PROJECTION_PARFUMO_LANE",
    "ParfumoProjectionBinding",
    "ParfumoProjectionLossLedger",
    "ParfumoProjectionPacket",
    "ParfumoProjectionRawAnchor",
    "ParfumoProjectionRawRef",
    "ParfumoProjectionRow",
    "ParfumoTargetedContentRecord",
    "build_parfumo_projection",
    "build_parfumo_projection_from_packet_directory",
    "build_parfumo_targeted_content_record",
    "project_parfumo_into_lake",
    "write_parfumo_projection",
]
