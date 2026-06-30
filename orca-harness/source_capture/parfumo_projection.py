from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Mapping

from pydantic import Field, field_validator, model_validator

from harness_utils import generate_ulid
from schemas.case_models import StrictModel
from source_capture.models import PreservedFile, SourceCapturePacket, SourceCaptureSlice

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


PARFUMO_PROJECTION_METHOD = "parfumo_current_window_mechanical_projection"
PARFUMO_PROJECTION_VERSION = "v0"
PARFUMO_PROJECTION_CERTIFICATION = "view_only; not_cleaned; not_normalized; not_judgment_ready"
PROJECTION_PARFUMO_LANE = "projection_parfumo"

_PARFUMO_SOURCE_FAMILY = "fragrance_native_database"
_PARFUMO_SOURCE_SURFACE = "parfumo_product_page_direct_http"
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
    anchor_kind: Literal["file", "html_selector", "text_pattern"] = "file"
    anchor_value: str | None = None

    @model_validator(mode="after")
    def validate_anchor_value(self) -> "ParfumoProjectionRawAnchor":
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
    if packet.source_surface != _PARFUMO_SOURCE_SURFACE:
        raise ValueError(
            "Parfumo projection requires "
            f"source_surface={_PARFUMO_SOURCE_SURFACE!r}; got {packet.source_surface!r}"
        )

    preserved_files = {item.file_id: item for item in packet.preserved_files}
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
            if not _looks_like_parfumo_body(preserved_file, body):
                continue
            projected = _project_parfumo_html(
                body,
                source_slice=source_slice,
                raw_ref=raw_ref,
                raw_anchor=_raw_anchor(preserved_file),
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


def _project_parfumo_html(
    body: bytes,
    *,
    source_slice: SourceCaptureSlice,
    raw_ref: ParfumoProjectionRawRef,
    raw_anchor: ParfumoProjectionRawAnchor,
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

    residuals.extend(
        [
            "linked_media_assets_not_preserved_by_direct_http_packet",
            "review_attached_photo_proof_not_present",
        ]
    )
    residuals.extend(_non_text_fragrance_scope_residuals(text))

    return _ProjectedParfumoHtml(
        rows=rows,
        bindings=bindings,
        residuals=_dedupe_preserve_order(residuals),
    )


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
    pattern = re.compile(
        r'<(?:button|a)[^>]+data-tab=["\']([^"\']+)["\'][^>]*>(.*?)</(?:button|a)>',
        flags=re.IGNORECASE | re.DOTALL,
    )
    for index, match in enumerate(pattern.finditer(text), start=1):
        tab_id = match.group(1)
        tab_body = match.group(0)
        rows.append(
            ParfumoProjectionRow(
                row_id=f"{source_slice.slice_id}:parfumo:review_tab:{tab_id}",
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
                    "tab_label": _text(match.group(2)),
                    "active": _attr_present(tab_body, "data-active", "true")
                    or _attr_present(tab_body, "aria-selected", "true"),
                    "displayed_count": _parse_count(_first_match(match.group(2), r"([\d,.]+)")),
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
    attr = f"data-{kind}-id"
    pattern = re.compile(
        rf'<(?P<tag>article|div|li)[^>]*\b{attr}=["\'](?P<id>[^"\']+)["\'][^>]*>',
        flags=re.IGNORECASE,
    )
    starts = list(pattern.finditer(text))
    rows: list[ParfumoProjectionRow] = []
    bindings: list[ParfumoProjectionBinding] = []
    source_order_by_tab: Counter[str] = Counter()
    for index, match in enumerate(starts):
        item_id = html.unescape(match.group("id")).strip()
        segment_end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        segment = _bounded_segment(text, match.start(), segment_end, match.group("tag"))
        tab_id = _text_card_tab_id(kind=kind, segment=segment, position=match.start(), text=text)
        source_order_by_tab[str(tab_id)] += 1
        row_kind = (
            "fragrance_review_card_current_window"
            if kind == "review"
            else "fragrance_statement_current_window"
        )
        row_id = f"{source_slice.slice_id}:parfumo:{kind}:{tab_id or 'unknown'}:{item_id}"
        row_anchor = _with_anchor(raw_anchor, "html_selector", f'[{attr}="{item_id}"]')
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
        "date_published": _first_match(
            segment,
            r'<time[^>]+datetime=["\']([^"\']+)["\']',
            flags=re.IGNORECASE,
        ),
        "date_display_text": _text(_first_match(segment, r"<time[^>]*>(.*?)</time>", flags=re.DOTALL)),
        text_field: text_value,
        f"{kind}_text_length_chars": len(text_value) if text_value is not None else None,
        "rating": _to_float(_attr_value(segment, "data-rating")),
        "helpful_count": _parse_count(_attr_value(segment, "data-helpful-count")),
        "source_item_url": _first_match(
            segment,
            r'<a[^>]+href=["\']([^"\']*(?:review|statement)[^"\']+)["\']',
            flags=re.IGNORECASE,
        ),
    }


def _text_row_residuals(segment: str, *, kind: Literal["review", "statement"]) -> list[str]:
    residuals = []
    if _author_name(segment) is None:
        residuals.append("author_display_name_absent")
    if re.search(r"<time\b", segment, flags=re.IGNORECASE) is None:
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


def _looks_like_parfumo_body(preserved_file: PreservedFile, body: bytes) -> bool:
    path = preserved_file.relative_packet_path.lower()
    if "http_response_metadata" in path:
        return False
    sample = body[:200_000].decode("utf-8", errors="ignore").lower()
    return (
        "parfumo.com/perfumes/" in sample
        or "/action/perfume/get_reviews.php" in sample
        or "perfume facts" in sample
    )


def _read_packet_directory(packet_or_manifest_path: Path) -> tuple[SourceCapturePacket, dict[str, bytes]]:
    manifest_path = (
        packet_or_manifest_path / "manifest.json"
        if packet_or_manifest_path.is_dir()
        else packet_or_manifest_path
    )
    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest not found: {manifest_path}")
    packet_dir = manifest_path.parent
    packet = SourceCapturePacket.model_validate(json.loads(manifest_path.read_text(encoding="utf-8")))
    raw_file_bytes_by_file_id: dict[str, bytes] = {}
    for preserved_file in packet.preserved_files:
        raw_path = packet_dir / preserved_file.relative_packet_path
        if not raw_path.exists():
            raise FileNotFoundError(f"preserved file {preserved_file.file_id} not found at {raw_path}")
        raw_file_bytes_by_file_id[preserved_file.file_id] = raw_path.read_bytes()
    return packet, raw_file_bytes_by_file_id


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
    close = re.search(rf"</{re.escape(tag)}>", text[start:max_end], flags=re.IGNORECASE)
    if close is not None:
        return text[start : start + close.end()]
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
    panels = [
        (match.start(), match.group(1))
        for match in re.finditer(
            r'<[^>]+(?:id|data-tab-panel)=["\']([^"\']+)["\'][^>]*>',
            text,
            flags=re.IGNORECASE,
        )
    ]
    active = None
    for panel_start, tab_id in panels:
        if panel_start <= position:
            active = tab_id
        else:
            break
    return active or "reviews"


def _source_text(segment: str, *, kind: Literal["review", "statement"]) -> str | None:
    for pattern in (
        rf'<[^>]+data-role=["\']{kind}-text["\'][^>]*>(.*?)</[^>]+>',
        r'<p[^>]+class=["\'][^"\']*(?:review|statement)[_-]?text[^"\']*["\'][^>]*>(.*?)</p>',
        r"<p[^>]*>(.*?)</p>",
    ):
        value = _text(_first_match(segment, pattern, flags=re.IGNORECASE | re.DOTALL))
        if value:
            return value
    return None


def _author_name(segment: str) -> str | None:
    return (
        _attr_value(segment, "data-author")
        or _first_match(
            segment,
            r'<[^>]+class=["\'][^"\']*author[^"\']*["\'][^>]*>(.*?)</[^>]+>',
            flags=re.DOTALL,
        )
        or _first_match(segment, r'<meta[^>]+itemprop=["\']author["\'][^>]+content=["\']([^"\']+)["\']')
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


def _first_match(text: str, pattern: str, *, flags: int = 0) -> str | None:
    match = re.search(pattern, text, flags)
    return html.unescape(match.group(1)).strip() if match else None


def _text(value: str | None) -> str | None:
    if value is None:
        return None
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.IGNORECASE)
    value = re.sub(r"</p\s*>", "\n", value, flags=re.IGNORECASE)
    value = re.sub(r"<[^>]+>", " ", value)
    normalized = re.sub(r"\s+", " ", html.unescape(value)).strip()
    return normalized


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


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _is_forbidden_field_name(key: str) -> bool:
    normalized = re.sub(r"[^a-z0-9]+", "_", key.lower()).strip("_")
    padded = f"_{normalized}_"
    return any(f"_{token}_" in padded for token in _FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES)


def _projection_json_text(projection: ParfumoProjectionPacket) -> str:
    return f"{json.dumps(projection.model_dump(mode='json'), indent=2, sort_keys=True)}\n"


__all__ = [
    "PARFUMO_PROJECTION_CERTIFICATION",
    "PARFUMO_PROJECTION_METHOD",
    "PARFUMO_PROJECTION_VERSION",
    "PROJECTION_PARFUMO_LANE",
    "ParfumoProjectionBinding",
    "ParfumoProjectionLossLedger",
    "ParfumoProjectionPacket",
    "ParfumoProjectionRawAnchor",
    "ParfumoProjectionRawRef",
    "ParfumoProjectionRow",
    "build_parfumo_projection",
    "build_parfumo_projection_from_packet_directory",
    "project_parfumo_into_lake",
    "write_parfumo_projection",
]
