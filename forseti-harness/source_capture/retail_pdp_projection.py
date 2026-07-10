from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Mapping, Sequence

from pydantic import Field, field_validator, model_validator

from harness_utils import generate_ulid
from schemas.case_models import StrictModel
from source_capture.models import PreservedFile, SourceCapturePacket, SourceCaptureSlice, VisibleFactStatus

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


RETAIL_PDP_PROJECTION_METHOD = "retail_pdp_mechanical_projection"
RETAIL_PDP_PROJECTION_VERSION = "v0"
RETAIL_PDP_PROJECTION_CERTIFICATION = "view_only; not_cleaned; not_normalized; not_judgment_ready"

# Append-only derived lane namespace for the Retail/PDP projection's Silver record.
PROJECTION_RETAIL_PDP_LANE = "projection_retail_pdp"

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

_REQUIRED_RETAIL_STRUCTURE_BINDINGS = frozenset(
    {
        "sku_variant_price",
        "variant_availability",
        "review_substrate_for_product",
        "series_locale_currency",
    }
)


class RetailProjectionRawRef(StrictModel):
    packet_id: str
    slice_id: str


class RetailProjectionRawAnchor(StrictModel):
    file_id: str
    relative_packet_path: str
    sha256: str
    hash_basis: str
    anchor_kind: Literal["file", "html_selector", "script_index", "text_pattern", "json_pointer"]
    anchor_value: str | None = None


class RetailPdpProjectionRow(StrictModel):
    row_id: str
    row_kind: Literal[
        "retail_pdp_product",
        "retail_variant_offer",
        "retail_review_substrate",
        "retail_embedded_structured_json",
        "retail_carried_module",
    ]
    retailer: Literal["amazon", "sephora", "ulta", "unknown"]
    raw_ref: RetailProjectionRawRef
    raw_anchor: RetailProjectionRawAnchor
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)
    residuals: list[str] = Field(default_factory=list)

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(cls, value: dict[str, Any | None]) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "retail PDP projection source_visible_fields may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value


class RetailPdpProjectionBinding(StrictModel):
    binding_type: Literal[
        "sku_variant_price",
        "variant_availability",
        "review_substrate_for_product",
        "series_locale_currency",
        "structured_json_for_product",
        "module_carried",
    ]
    row_id: str
    raw_ref: RetailProjectionRawRef
    raw_anchor: RetailProjectionRawAnchor
    source_visible_fields: dict[str, Any | None] = Field(default_factory=dict)

    @field_validator("source_visible_fields")
    @classmethod
    def reject_judgment_field_names(cls, value: dict[str, Any | None]) -> dict[str, Any | None]:
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "retail PDP projection bindings may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value


class RetailPdpProjectionLossEntry(StrictModel):
    category: Literal["RETAIL_HERO_IMAGERY_COLLAPSED", "RETAIL_CART_NOTIFY_STATE_COLLAPSED"]
    count: int = Field(ge=0)
    raw_anchor: RetailProjectionRawAnchor
    reason: str


class RetailPdpProjectionLossLedger(StrictModel):
    collapsed: list[RetailPdpProjectionLossEntry] = Field(default_factory=list)
    preserved_evidence_rows: int = Field(ge=0)
    preserved_bindings: int = Field(ge=0)
    timing: Literal["separate_not_collapsed"] = "separate_not_collapsed"
    hierarchy_preserved: bool
    structure_preserved: bool
    certification: Literal["collapses_only_logged_frame_conditional_pdp_envelope; does_not_certify_cleaning"] = (
        "collapses_only_logged_frame_conditional_pdp_envelope; does_not_certify_cleaning"
    )


class RetailPdpProjectionPacket(StrictModel):
    projection_method: Literal["retail_pdp_mechanical_projection"] = RETAIL_PDP_PROJECTION_METHOD
    projection_version: Literal["v0"] = RETAIL_PDP_PROJECTION_VERSION
    certification: Literal["view_only; not_cleaned; not_normalized; not_judgment_ready"] = (
        RETAIL_PDP_PROJECTION_CERTIFICATION
    )
    packet_id: str
    rows: list[RetailPdpProjectionRow] = Field(default_factory=list)
    binding_map: list[RetailPdpProjectionBinding] = Field(default_factory=list)
    loss_ledger: RetailPdpProjectionLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "RetailPdpProjectionPacket":
        if self.loss_ledger.preserved_evidence_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_evidence_rows must match rows length")
        if self.loss_ledger.preserved_bindings != len(self.binding_map):
            raise ValueError("loss_ledger.preserved_bindings must match binding_map length")
        return self


def _retail_structure_preserved(bindings: Sequence[RetailPdpProjectionBinding]) -> bool:
    binding_types = {binding.binding_type for binding in bindings}
    return _REQUIRED_RETAIL_STRUCTURE_BINDINGS.issubset(binding_types)


class RetailPdpProjectionInputError(ValueError):
    """A packet directory cannot be projected without losing raw-file integrity."""


def build_retail_pdp_projection_from_packet_directory(*, packet_directory: Path) -> RetailPdpProjectionPacket:
    """Build a Retail/PDP projection from an existing local Source Capture Packet directory."""
    packet, raw_file_bytes_by_file_id = _load_packet_directory_projection_inputs(packet_directory)
    return build_retail_pdp_projection(packet=packet, raw_file_bytes_by_file_id=raw_file_bytes_by_file_id)


def write_retail_pdp_projection(*, packet_directory: Path, output_path: Path) -> RetailPdpProjectionPacket:
    """Write a projection JSON sidecar from an existing packet directory.

    This is a local view writer only: it reads ``manifest.json`` plus hash-verified
    preserved files, then writes the mechanical projection. It performs no capture,
    fetch, Cleaning, ECR, or Judgment work.
    """
    projection = build_retail_pdp_projection_from_packet_directory(packet_directory=packet_directory)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        f"{json.dumps(projection.model_dump(mode='json'), indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    return projection


def project_retail_pdp_into_lake(
    *,
    data_root: "DataLakeRoot",
    packet_id: str,
    record_id: str | None = None,
) -> tuple[RetailPdpProjectionPacket, Path]:
    """Project a committed raw packet -- read by key from the lake and
    hash-verified -- into a Retail/PDP projection, and append it as a derived
    record at ``derived/<packet_id>/projection_retail_pdp/<record_id>.json``
    (append-only; re-derive = new sibling).

    The verified read is the lake loader (``DataLakeRoot.load_raw_packet``); the
    extraction is byte-identical to the legacy directory path
    (``build_retail_pdp_projection_from_packet_directory``). This adds no capture,
    fetch, Cleaning, ECR, or Judgment. Returns the projection and the derived
    record path.
    """
    loaded = data_root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    projection = build_retail_pdp_projection(
        packet=packet,
        raw_file_bytes_by_file_id=loaded.bodies,
    )
    record = record_id if record_id is not None else generate_ulid()
    data = (
        f"{json.dumps(projection.model_dump(mode='json'), indent=2, sort_keys=True)}\n"
    ).encode("utf-8")
    derived_path = data_root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=PROJECTION_RETAIL_PDP_LANE,
        record_id=f"{record}.json",
        data=data,
    )
    return projection, derived_path


def build_retail_pdp_projection(
    *,
    packet: SourceCapturePacket,
    raw_file_bytes_by_file_id: Mapping[str, bytes],
) -> RetailPdpProjectionPacket:
    """Derive a traceable, mechanical Retail/PDP row view from preserved packet bytes.

    This is not a parser authority, Cleaning transform, ECR schema, or Judgment
    read. It only projects rendered PDP capture bytes into inspectable rows that
    carry packet/slice/file/hash anchors and preserves embedded structured JSON
    verbatim when present.
    """
    preserved_files = {item.file_id: item for item in packet.preserved_files}
    rows: list[RetailPdpProjectionRow] = []
    bindings: list[RetailPdpProjectionBinding] = []
    collapsed: list[RetailPdpProjectionLossEntry] = []
    residuals: list[str] = []
    retailer = _detect_retailer(packet)

    for source_slice in packet.source_slices:
        raw_ref = RetailProjectionRawRef(packet_id=packet.packet_id, slice_id=source_slice.slice_id)
        slice_files: list[tuple[PreservedFile, bytes]] = []
        for file_id in source_slice.preserved_file_ids:
            preserved_file = preserved_files[file_id]
            body = raw_file_bytes_by_file_id.get(file_id)
            if body is None:
                raise ValueError(f"raw bytes are required for preserved file id: {file_id}")
            slice_files.append((preserved_file, body))

        html_files = [
            (preserved_file, body)
            for preserved_file, body in slice_files
            if preserved_file.relative_packet_path.lower().endswith((".html", ".htm"))
        ]
        visible_text_files = [
            (preserved_file, _decode_text(body))
            for preserved_file, body in slice_files
            if preserved_file.relative_packet_path.lower().endswith(".txt")
        ]
        visible_text = "\n".join(text for _preserved_file, text in visible_text_files)

        if not html_files:
            residuals.append(f"{source_slice.slice_id}:retail_pdp_rendered_dom_absent")
            continue

        for preserved_file, body in html_files:
            html = _decode_text(body)
            projected = _project_retail_html(
                html,
                visible_text=visible_text,
                packet=packet,
                source_slice=source_slice,
                raw_ref=raw_ref,
                visible_text_files=visible_text_files,
                raw_anchor=_raw_anchor(preserved_file),
                retailer=retailer,
            )
            rows.extend(projected.rows)
            bindings.extend(projected.bindings)
            collapsed.extend(projected.collapsed)
            residuals.extend(projected.residuals)

    return RetailPdpProjectionPacket(
        packet_id=packet.packet_id,
        rows=rows,
        binding_map=bindings,
        loss_ledger=RetailPdpProjectionLossLedger(
            collapsed=collapsed,
            preserved_evidence_rows=len(rows),
            preserved_bindings=len(bindings),
            # Retail PDPs have no parent->reply thread hierarchy; retail structure is attested
            # through the binding map instead.
            hierarchy_preserved=True,
            structure_preserved=_retail_structure_preserved(bindings),
        ),
        residuals=residuals,
    )


class _ProjectedRetailHtml(StrictModel):
    rows: list[RetailPdpProjectionRow] = Field(default_factory=list)
    bindings: list[RetailPdpProjectionBinding] = Field(default_factory=list)
    collapsed: list[RetailPdpProjectionLossEntry] = Field(default_factory=list)
    residuals: list[str] = Field(default_factory=list)


class _StructuredJsonEntry(StrictModel):
    kind: Literal["ld_json", "apollo_state"]
    index: int
    raw_text: str
    parsed: object | None
    raw_anchor: RetailProjectionRawAnchor


def _project_retail_html(
    html: str,
    *,
    visible_text_files: Sequence[tuple[PreservedFile, str]],
    visible_text: str,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    raw_ref: RetailProjectionRawRef,
    raw_anchor: RetailProjectionRawAnchor,
    retailer: Literal["amazon", "sephora", "ulta", "unknown"],
) -> _ProjectedRetailHtml:
    rows: list[RetailPdpProjectionRow] = []
    bindings: list[RetailPdpProjectionBinding] = []
    residuals: list[str] = []
    collapsed: list[RetailPdpProjectionLossEntry] = []

    structured_entries = _extract_structured_json_entries(html, raw_anchor=raw_anchor)
    product_row_id = f"{source_slice.slice_id}:{retailer}:pdp"
    product_fields = _product_context_fields(packet, source_slice, retailer)
    rows.append(
        RetailPdpProjectionRow(
            row_id=product_row_id,
            row_kind="retail_pdp_product",
            retailer=retailer,
            raw_ref=raw_ref,
            raw_anchor=raw_anchor,
            source_visible_fields=product_fields,
        )
    )

    for entry in structured_entries:
        row_id = f"{source_slice.slice_id}:{retailer}:structured:{entry.kind}:{entry.index}"
        rows.append(
            RetailPdpProjectionRow(
                row_id=row_id,
                row_kind="retail_embedded_structured_json",
                retailer=retailer,
                raw_ref=raw_ref,
                raw_anchor=entry.raw_anchor,
                source_visible_fields={
                    "structured_json_kind": entry.kind,
                    "script_index": entry.index,
                    "raw_json_text": entry.raw_text,
                    "parse_status": "parsed" if entry.parsed is not None else "malformed_json",
                    "parsed_type": _json_type(entry.parsed),
                },
                residuals=[] if entry.parsed is not None else [f"{entry.kind}_{entry.index}_malformed_json"],
            )
        )
        bindings.append(
            RetailPdpProjectionBinding(
                binding_type="structured_json_for_product",
                row_id=row_id,
                raw_ref=raw_ref,
                raw_anchor=entry.raw_anchor,
                source_visible_fields={"product_row_id": product_row_id, "structured_json_kind": entry.kind},
            )
        )

    variant_fields, variant_anchor, variant_residuals = _variant_offer_fields(
        retailer=retailer,
        html=html,
        visible_text=visible_text,
        packet=packet,
        source_slice=source_slice,
        structured_entries=structured_entries,
        fallback_anchor=raw_anchor,
    )
    residuals.extend(variant_residuals)
    if variant_fields:
        sku = _string_or_none(variant_fields.get("sku")) or _string_or_none(variant_fields.get("product_id")) or "unknown"
        variant_row_id = f"{source_slice.slice_id}:{retailer}:variant:{_row_token(sku)}"
        rows.append(
            RetailPdpProjectionRow(
                row_id=variant_row_id,
                row_kind="retail_variant_offer",
                retailer=retailer,
                raw_ref=raw_ref,
                raw_anchor=variant_anchor,
                source_visible_fields=variant_fields,
            )
        )
        bindings.extend(
            [
                RetailPdpProjectionBinding(
                    binding_type="sku_variant_price",
                    row_id=variant_row_id,
                    raw_ref=raw_ref,
                    raw_anchor=variant_anchor,
                    source_visible_fields={
                        "sku": variant_fields.get("sku"),
                        "variant_name": variant_fields.get("variant_name"),
                        "price": variant_fields.get("price"),
                        "price_currency": variant_fields.get("price_currency"),
                    },
                ),
                RetailPdpProjectionBinding(
                    binding_type="variant_availability",
                    row_id=variant_row_id,
                    raw_ref=raw_ref,
                    raw_anchor=variant_anchor,
                    source_visible_fields={
                        "sku": variant_fields.get("sku"),
                        "variant_name": variant_fields.get("variant_name"),
                        "availability": variant_fields.get("availability"),
                    },
                ),
                RetailPdpProjectionBinding(
                    binding_type="series_locale_currency",
                    row_id=variant_row_id,
                    raw_ref=raw_ref,
                    raw_anchor=raw_anchor,
                    source_visible_fields={
                        "series_id": packet.series_id,
                        "locale_pin": _fact_value(source_slice.locale_pin),
                        "currency_pin": _fact_value(source_slice.currency_pin),
                        "variant_pin": _fact_value(source_slice.variant_pin),
                    },
                ),
            ]
        )
    else:
        residuals.append(f"{source_slice.slice_id}:{retailer}:variant_offer_absent")

    review_fields, review_anchor, review_residuals = _review_substrate_fields(
        retailer=retailer,
        html=html,
        visible_text=visible_text,
        structured_entries=structured_entries,
        fallback_anchor=raw_anchor,
    )
    residuals.extend(review_residuals)
    if review_fields:
        review_row_id = f"{source_slice.slice_id}:{retailer}:review_substrate"
        rows.append(
            RetailPdpProjectionRow(
                row_id=review_row_id,
                row_kind="retail_review_substrate",
                retailer=retailer,
                raw_ref=raw_ref,
                raw_anchor=review_anchor,
                source_visible_fields=review_fields,
                residuals=review_residuals,
            )
        )
        bindings.append(
            RetailPdpProjectionBinding(
                binding_type="review_substrate_for_product",
                row_id=review_row_id,
                raw_ref=raw_ref,
                raw_anchor=review_anchor,
                source_visible_fields={
                    "product_row_id": product_row_id,
                    "review_substrate_source": review_fields.get("review_substrate_source"),
                    "review_count": review_fields.get("review_count"),
                    "rating": review_fields.get("rating"),
                },
            )
        )
    else:
        residuals.append(f"{source_slice.slice_id}:{retailer}:review_substrate_absent")

    for module in _carried_module_fields(
        retailer=retailer,
        html=html,
        visible_text_files=visible_text_files,
        raw_anchor=raw_anchor,
    ):
        module_row_id = f"{source_slice.slice_id}:{retailer}:module:{module['module_type']}"
        rows.append(
            RetailPdpProjectionRow(
                row_id=module_row_id,
                row_kind="retail_carried_module",
                retailer=retailer,
                raw_ref=raw_ref,
                raw_anchor=module["raw_anchor"],
                source_visible_fields={key: value for key, value in module.items() if key != "raw_anchor"},
            )
        )
        bindings.append(
            RetailPdpProjectionBinding(
                binding_type="module_carried",
                row_id=module_row_id,
                raw_ref=raw_ref,
                raw_anchor=module["raw_anchor"],
                source_visible_fields={"module_type": module["module_type"]},
            )
        )

    collapsed.extend(_collapse_entries(html=html, visible_text=visible_text, raw_anchor=raw_anchor))
    return _ProjectedRetailHtml(rows=rows, bindings=bindings, collapsed=collapsed, residuals=residuals)


def _extract_structured_json_entries(html: str, *, raw_anchor: RetailProjectionRawAnchor) -> list[_StructuredJsonEntry]:
    entries: list[_StructuredJsonEntry] = []
    for index, raw_text in enumerate(_extract_ld_json_texts(html)):
        stripped = raw_text.strip()
        entries.append(
            _StructuredJsonEntry(
                kind="ld_json",
                index=index,
                raw_text=stripped,
                parsed=_safe_json_loads(stripped),
                raw_anchor=_with_anchor(raw_anchor, "script_index", f"ld_json[{index}]"),
            )
        )

    apollo_text = _extract_apollo_state_text(html)
    if apollo_text is not None:
        entries.append(
            _StructuredJsonEntry(
                kind="apollo_state",
                index=0,
                raw_text=apollo_text,
                parsed=_safe_json_loads(apollo_text),
                raw_anchor=_with_anchor(raw_anchor, "script_index", "window.__APOLLO_STATE__"),
            )
        )
    return entries


def _variant_offer_fields(
    *,
    retailer: Literal["amazon", "sephora", "ulta", "unknown"],
    html: str,
    visible_text: str,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    structured_entries: list[_StructuredJsonEntry],
    fallback_anchor: RetailProjectionRawAnchor,
) -> tuple[dict[str, Any | None], RetailProjectionRawAnchor, list[str]]:
    residuals: list[str] = []
    if retailer == "amazon":
        fields = _amazon_variant_offer_fields(html=html, visible_text=visible_text, packet=packet, source_slice=source_slice)
        amazon_residuals = (
            ["amazon_price_from_unanchored_visible_text_fallback"]
            if fields.get("price_isolation") == "unanchored_visible_text_fallback"
            else []
        )
        return fields, _with_anchor(fallback_anchor, "html_selector", "#ASIN/#corePrice_feature_div/#availability"), amazon_residuals

    sephora_dom_fields = _sephora_dom_offer_fields(html) if retailer == "sephora" else {}
    selected_sku = _string_or_none(sephora_dom_fields.get("dom_sku"))
    structured_fields, structured_anchor = _structured_variant_offer_fields(
        structured_entries,
        preferred_sku=selected_sku,
    )
    apollo_fields, apollo_anchor = _ulta_apollo_offer_fields(structured_entries) if retailer == "ulta" else ({}, None)
    if retailer == "ulta" and not apollo_fields and _ulta_apollo_offer_substrate_present(structured_entries):
        residuals.append(f"{source_slice.slice_id}:ulta:variant_offer_substrate_present_but_unextracted")
    if sephora_dom_fields:
        structured_fields = {
            **structured_fields,
            "product_id": _string_or_none(sephora_dom_fields.get("dom_product_id"))
            or structured_fields.get("product_id"),
            "sku": selected_sku or structured_fields.get("sku"),
            **sephora_dom_fields,
            "selected_sku": selected_sku,
            "selection_binding_source": "sephora_dom_product_page",
        }
    if retailer == "sephora" and structured_fields:
        structured_fields = {
            **structured_fields,
            "exact_stock_quantity": "not_observed",
            "sold_units": "not_observed",
        }
        if selected_sku and not _string_or_none(structured_fields.get("availability")):
            residuals.append("sephora_selected_variant_availability_absent")
    residuals.extend(_structured_price_residuals(retailer=retailer, structured_fields=structured_fields))
    if retailer == "ulta" and structured_fields and apollo_fields:
        for key in ("sku", "product_id", "price", "availability"):
            left = _string_or_none(structured_fields.get(key))
            right = _string_or_none(apollo_fields.get(key))
            if left and right and not _equivalent_offer_value(key, left, right):
                residuals.append(f"ulta_ld_json_apollo_{key}_mismatch")
        apollo_prefixed = {
            key if key.startswith("apollo_") else f"apollo_{key}": value for key, value in apollo_fields.items()
        }
        merged = {**structured_fields, **apollo_prefixed}
        _residualize_ulta_requested_sku_mismatch(merged, residuals, source_slice=source_slice)
        return merged, structured_anchor or apollo_anchor or fallback_anchor, residuals
    if structured_fields:
        if retailer == "ulta":
            _residualize_ulta_requested_sku_mismatch(structured_fields, residuals, source_slice=source_slice)
        return structured_fields, structured_anchor or fallback_anchor, residuals
    if apollo_fields:
        _residualize_ulta_requested_sku_mismatch(apollo_fields, residuals, source_slice=source_slice)
        return apollo_fields, apollo_anchor or fallback_anchor, residuals
    return {}, fallback_anchor, residuals


def _review_substrate_fields(
    *,
    retailer: Literal["amazon", "sephora", "ulta", "unknown"],
    html: str,
    visible_text: str,
    structured_entries: list[_StructuredJsonEntry],
    fallback_anchor: RetailProjectionRawAnchor,
) -> tuple[dict[str, Any | None], RetailProjectionRawAnchor, list[str]]:
    if retailer == "amazon":
        return _amazon_review_fields(html=html, visible_text=visible_text), _with_anchor(
            fallback_anchor, "html_selector", "#averageCustomerReviews/#acrCustomerReviewText"
        ), []
    if retailer == "sephora":
        fields = _sephora_review_fields(html=html, visible_text=visible_text, structured_entries=structured_entries)
        residuals = []
        if fields.get("review_count_isolation") == "unanchored_fallback":
            residuals.append("sephora_review_count_from_unanchored_fallback")
        if not fields.get("target_widget_review_count"):
            residuals.append("sephora_target_widget_exact_review_count_absent")
        if not fields.get("rating_distribution_histogram"):
            residuals.append("sephora_target_widget_rating_distribution_absent")
        structured_count = _string_or_none(fields.get("structured_review_count"))
        target_dom_count = _string_or_none(fields.get("target_widget_review_count")) or _string_or_none(
            fields.get("displayed_review_count_text")
        )
        if (
            structured_count
            and target_dom_count
            and not _equivalent_review_count(structured_count, target_dom_count)
        ):
            residuals.append("sephora_ld_json_review_count_differs_from_target_dom")
        section_anchor = _sephora_review_section_anchor(html)
        anchor = (
            _with_anchor(fallback_anchor, "html_selector", section_anchor)
            if section_anchor
            else _with_anchor(fallback_anchor, "text_pattern", "Ratings & Reviews")
        )
        return fields, anchor, residuals
    if retailer == "ulta":
        fields, residuals = _ulta_review_fields(structured_entries)
        return fields, _with_anchor(fallback_anchor, "script_index", "ld_json/apollo_state review modules"), residuals
    return {}, fallback_anchor, []


def _amazon_variant_offer_fields(
    *,
    html: str,
    visible_text: str,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
) -> dict[str, Any | None]:
    asin = _first_regex(
        html,
        (
            r"<input[^>]+(?:id|name)=[\"']ASIN[\"'][^>]+value=[\"']([^\"']+)[\"']",
            r"<input[^>]+value=[\"']([^\"']+)[\"'][^>]+(?:id|name)=[\"']ASIN[\"']",
            r"/dp/([A-Z0-9]{10})",
        ),
    )
    if asin is None:
        return {}
    price = _first_regex(
        html,
        (
            r"name=[\"']items\[0\.base\]\[customerVisiblePrice\]\[amount\][\"'][^>]+value=[\"']([^\"']+)[\"']",
            r"value=[\"']([^\"']+)[\"'][^>]+name=[\"']items\[0\.base\]\[customerVisiblePrice\]\[amount\][\"']",
        ),
    )
    # The DOM price input is target-anchored; the visible-text "$N" fallback is
    # position-dependent, so fallback-only price reads are carried but residualized.
    price_isolation = "amazon_dom_target_input"
    if price is None:
        price = _first_regex(visible_text, (r"\$(\d+(?:\.\d{2})?)",))
        price_isolation = "unanchored_visible_text_fallback" if price is not None else "absent"
    availability = _first_literal(visible_text, ("In Stock", "Currently unavailable", "Out of Stock"))
    variant_name = _first_regex(visible_text, (r"Style:\s*([^\n]+)",))
    return {
        "product_id": asin,
        "sku": asin,
        "variant_name": variant_name or _fact_value(source_slice.variant_pin),
        "price": price,
        "price_isolation": price_isolation,
        "price_currency": _fact_value(source_slice.currency_pin) or "USD",
        "availability": availability,
        "series_id": packet.series_id,
        "locale_pin": _fact_value(source_slice.locale_pin),
        "currency_pin": _fact_value(source_slice.currency_pin),
        "variant_pin": _fact_value(source_slice.variant_pin),
        "variant_binding_source": "amazon_dom_js",
    }


def _structured_variant_offer_fields(
    structured_entries: list[_StructuredJsonEntry],
    *,
    preferred_sku: str | None = None,
) -> tuple[dict[str, Any | None], RetailProjectionRawAnchor | None]:
    for entry in structured_entries:
        for product in _walk_dicts(entry.parsed):
            product_type = product.get("@type")
            if isinstance(product_type, list):
                product_type_values = set(str(item) for item in product_type)
            else:
                product_type_values = {str(product_type)} if product_type is not None else set()
            if "ProductGroup" in product_type_values:
                variants = product.get("hasVariant")
                if isinstance(variants, list) and variants:
                    candidates = [item for item in variants if isinstance(item, dict)]
                    variant = (
                        next(
                            (
                                item
                                for item in candidates
                                if _string_or_none(item.get("sku")) == preferred_sku
                            ),
                            None,
                        )
                        if preferred_sku
                        else next(iter(candidates), None)
                    )
                    if variant is not None:
                        offer = variant.get("offers") if isinstance(variant.get("offers"), dict) else {}
                        return _offer_fields_from_product(product, variant, offer, entry.kind), entry.raw_anchor
            if "Product" in product_type_values:
                if preferred_sku and _string_or_none(product.get("sku")) != preferred_sku:
                    continue
                offer = product.get("offers") if isinstance(product.get("offers"), dict) else {}
                return _offer_fields_from_product(product, product, offer, entry.kind), entry.raw_anchor
    return {}, None


def _offer_fields_from_product(
    group_or_product: Mapping[str, object],
    variant: Mapping[str, object],
    offer: Mapping[str, object],
    source: str,
) -> dict[str, Any | None]:
    return {
        "product_id": _string_or_none(group_or_product.get("productGroupID"))
        or _string_or_none(group_or_product.get("productID"))
        or _string_or_none(variant.get("productID")),
        "sku": _string_or_none(variant.get("sku")),
        "variant_name": _string_or_none(variant.get("color")) or _string_or_none(variant.get("scent")) or _string_or_none(variant.get("name")),
        "price": _string_or_none(offer.get("price")),
        "price_isolation": "structured_json_offer" if _string_or_none(offer.get("price")) else "absent",
        "price_currency": _string_or_none(offer.get("priceCurrency")),
        "availability": _string_or_none(offer.get("availability")),
        "price_binding_source": source,
        "variant_binding_source": source,
    }


def _ulta_apollo_offer_fields(
    structured_entries: list[_StructuredJsonEntry],
) -> tuple[dict[str, Any | None], RetailProjectionRawAnchor | None]:
    for entry in structured_entries:
        if entry.kind != "apollo_state":
            continue
        requested_sku = _first_regex(entry.raw_text, (r'\\"sku\\":\\"([^\\"]+)\\"', r'"sku":"([^"]+)"'))
        best: dict[str, object] | None = None
        for item in _walk_dicts(entry.parsed):
            if item.get("skuId") and item.get("productName") and (item.get("listPrice") or item.get("salePrice")):
                best = item
                break
        if best is None:
            return {}, entry.raw_anchor
        price = _string_or_none(best.get("salePrice")) or _string_or_none(best.get("listPrice"))
        return {
            "product_id": _string_or_none(best.get("productId")),
            "sku": _string_or_none(best.get("skuId")),
            "variant_name": _string_or_none(best.get("productName")),
            "price": price[1:] if isinstance(price, str) and price.startswith("$") else price,
            "price_currency": "USD" if price else None,
            "availability": _first_literal(json.dumps(entry.parsed), ("InStock", "OutOfStock")),
            "apollo_requested_sku": requested_sku,
            "variant_binding_source": "apollo_state",
        }, entry.raw_anchor
    return {}, None


def _ulta_apollo_offer_substrate_present(structured_entries: list[_StructuredJsonEntry]) -> bool:
    for entry in structured_entries:
        if entry.kind != "apollo_state":
            continue
        for item in _walk_dicts(entry.parsed):
            if item.get("skuId") and (item.get("listPrice") or item.get("salePrice")):
                return True
    return False


def _sephora_dom_offer_fields(html: str) -> dict[str, Any | None]:
    for match in re.finditer(r"<[^>]*data-comp=\"ProductPage[^\"]*\"[^>]*>", html, flags=re.IGNORECASE):
        tag = match.group(0)
        price = _html_attr_value(tag, "data-cnstrc-item-price")
        if price is None:
            continue
        return {
            "dom_product_id": _html_attr_value(tag, "data-cnstrc-item-id"),
            "dom_sku": _html_attr_value(tag, "data-cnstrc-item-variation-id"),
            "dom_price": price.lstrip("$"),
            "price": price.lstrip("$"),
            "price_isolation": "sephora_dom_product_page",
            "price_binding_source": "rendered_dom_product_page",
        }
    return {}


def _structured_price_residuals(
    *,
    retailer: Literal["amazon", "sephora", "ulta", "unknown"],
    structured_fields: Mapping[str, object],
) -> list[str]:
    if (
        retailer == "sephora"
        and _string_or_none(structured_fields.get("price"))
        and structured_fields.get("price_isolation") == "structured_json_offer"
    ):
        return ["sephora_price_from_structured_json_without_target_dom_price"]
    return []


def _sku_from_variant_pin(variant_pin: str | None) -> str | None:
    if variant_pin is None:
        return None
    return _first_regex(variant_pin, (r"\bsku=([A-Za-z0-9_-]+)", r"\bsku:\s*([A-Za-z0-9_-]+)"))


def _amazon_review_fields(*, html: str, visible_text: str) -> dict[str, Any | None]:
    rating = _first_regex(visible_text, (r"Customer reviews\s+(\d+(?:\.\d+)?) out of 5", r"(\d+(?:\.\d+)?) out of 5 stars"))
    count = _first_regex(visible_text, (r"([\d,]+) global ratings", r"([\d,]+) ratings"))
    best_sellers_rank = _first_regex(visible_text, (r"(Best Sellers Rank:[^\n]+(?:\n#[^\n]+)*)",))
    ld_json_present = bool(_extract_ld_json_texts(html))
    average_customer_reviews_node_present = "averageCustomerReviews" in html
    acr_customer_review_text_node_present = "acrCustomerReviewText" in html
    if not any(
        (
            rating,
            count,
            best_sellers_rank,
            ld_json_present,
            average_customer_reviews_node_present,
            acr_customer_review_text_node_present,
        )
    ):
        return {}
    return {
        "review_substrate_source": "amazon_dom_js",
        "ld_json_present": ld_json_present,
        "average_customer_reviews_node_present": average_customer_reviews_node_present,
        "acr_customer_review_text_node_present": acr_customer_review_text_node_present,
        "rating": rating,
        "review_count": count,
        "best_sellers_rank_text": best_sellers_rank,
    }


def _sephora_review_fields(
    *,
    html: str,
    visible_text: str,
    structured_entries: list[_StructuredJsonEntry],
) -> dict[str, Any | None]:
    # The target header's abbreviated count, the exact ReviewsStats count, and JSON-LD
    # are separate source observations. Preserve all three rather than normalizing them.
    review_section_html = _sephora_review_section_html(html)
    html_displayed_count = _first_regex(
        review_section_html,
        (r"Ratings\s*&(?:amp;)?\s*Reviews\s*\(([^)]+)\)",),
    )
    visible_displayed_count = _first_regex(
        visible_text,
        (r"Ratings & Reviews\s*\(([^)]+)\)",),
    )
    anchored_count = html_displayed_count or visible_displayed_count
    fallback_count = _first_regex(visible_text, (r"([^\s]+)\s+Reviews\*?",))
    displayed_count = anchored_count or fallback_count
    review_count_isolation = (
        "target_anchored" if anchored_count else ("unanchored_fallback" if fallback_count else "absent")
    )

    target_widget_review_count = _first_regex(
        review_section_html,
        (r">\s*([\d,]+)\s+Reviews\*\s*<",),
    )
    if target_widget_review_count is None and anchored_count:
        visible_target_start = re.search(
            r"Ratings & Reviews\s*\([^)]+\)",
            visible_text,
            flags=re.IGNORECASE,
        )
        if visible_target_start:
            target_widget_review_count = _first_regex(
                visible_text[visible_target_start.end() : visible_target_start.end() + 3000],
                (r"([\d,]+)\s+Reviews\*",),
            )

    rating = _first_regex(visible_text, (r"Summary\s+5\s+4\s+3\s+2\s+1\s+(\d+(?:\.\d+)?)",))
    ld_count = None
    ld_rating = None
    for entry in structured_entries:
        if entry.kind != "ld_json":
            continue
        for item in _walk_dicts(entry.parsed):
            aggregate = item.get("aggregateRating")
            if isinstance(aggregate, dict):
                ld_count = _string_or_none(aggregate.get("reviewCount")) or ld_count
                ld_rating = _string_or_none(aggregate.get("ratingValue")) or ld_rating
    recommendation_counts = re.findall(
        r'data-cnstrc-item=["\']recommendation["\'][\s\S]{0,1400}?aria-label=["\']([^"\']+ reviews)["\']',
        html,
        flags=re.IGNORECASE,
    )
    return {
        "review_substrate_source": "sephora_target_dom",
        "bazaarvoice_api_config_present": "api.bazaarvoice.com" in html.lower(),
        "rating": rating or ld_rating,
        "review_count": displayed_count,
        "displayed_review_count_text": displayed_count,
        "target_widget_review_count": target_widget_review_count,
        "structured_review_count": ld_count,
        "review_count_isolation": review_count_isolation,
        "ld_json_review_count": ld_count,
        "ld_json_rating": ld_rating,
        "rating_distribution_histogram": _sephora_rating_distribution(review_section_html),
        "recommendation_review_count_examples": recommendation_counts[:5],
        "recommendation_counts_are_not_target_substrate": bool(recommendation_counts),
    }


def _sephora_review_section_anchor(html: str) -> str | None:
    match = re.search(
        r'data-at=["\']ratings_reviews_section["\']',
        html,
        flags=re.IGNORECASE,
    )
    return match.group(0) if match else None


def _sephora_review_section_html(html: str) -> str:
    anchor = re.search(
        r'data-at=["\']ratings_reviews_section["\']',
        html,
        flags=re.IGNORECASE,
    )
    if anchor is None:
        return ""
    return html[anchor.start() : anchor.start() + 6000]


def _sephora_rating_distribution(review_section_html: str) -> dict[str, Any] | None:
    matches = re.findall(
        r'Histogram-label[^>]*>\s*([1-5])\s*</span>[\s\S]{0,800}?style=["\'][^"\']*width:\s*([0-9]+(?:\.[0-9]+)?)%;',
        review_section_html,
        flags=re.IGNORECASE,
    )
    percentages: dict[int, str] = {}
    for raw_rating, raw_value in matches:
        percentages.setdefault(int(raw_rating), raw_value)
    if set(percentages) != {1, 2, 3, 4, 5}:
        return None
    return {
        "basis": "percent",
        "order": "5_to_1",
        "buckets": [
            {"rating": rating, "value": percentages[rating]}
            for rating in (5, 4, 3, 2, 1)
        ],
    }


def _equivalent_review_count(left: str, right: str) -> bool:
    return left.replace(",", "").strip() == right.replace(",", "").strip()


def _ulta_review_fields(structured_entries: list[_StructuredJsonEntry]) -> tuple[dict[str, Any | None], list[str]]:
    residuals: list[str] = []
    ld_count = None
    ld_rating = None
    apollo_count = None
    apollo_rating = None
    for entry in structured_entries:
        for item in _walk_dicts(entry.parsed):
            aggregate = item.get("aggregateRating") if isinstance(item, dict) else None
            if entry.kind == "ld_json" and isinstance(aggregate, dict):
                ld_count = _string_or_none(aggregate.get("reviewCount")) or ld_count
                ld_rating = _string_or_none(aggregate.get("ratingValue")) or ld_rating
            if entry.kind == "apollo_state" and item.get("reviewCount") and item.get("rating"):
                apollo_count = _string_or_none(item.get("reviewCount")) or apollo_count
                apollo_rating = _string_or_none(item.get("rating")) or apollo_rating
    if ld_count and apollo_count and ld_count != apollo_count:
        residuals.append("ulta_ld_json_apollo_review_count_mismatch")
    if ld_rating and apollo_rating and ld_rating != apollo_rating:
        residuals.append("ulta_ld_json_apollo_rating_mismatch")
    return {
        "review_substrate_source": "ulta_ld_json_and_apollo_state",
        "review_count": apollo_count or ld_count,
        "rating": apollo_rating or ld_rating,
        "ld_json_review_count": ld_count,
        "ld_json_rating": ld_rating,
        "apollo_review_count": apollo_count,
        "apollo_rating": apollo_rating,
    }, residuals


def _carried_module_fields(
    *,
    retailer: Literal["amazon", "sephora", "ulta", "unknown"],
    html: str,
    visible_text_files: Sequence[tuple[PreservedFile, str]],
    raw_anchor: RetailProjectionRawAnchor,
) -> list[dict[str, Any]]:
    modules: list[dict[str, Any]] = []
    module_specs = [
        ("shipping", ("FREE delivery", "standard shipping", "same day delivery", "deliveryBlock")),
        ("loyalty", ("Beauty Insider", "points", "Store Card", "Rewards")),
        ("recommendations", ("data-cnstrc-item=\"recommendation\"", "customers bought together", "Make it a routine")),
    ]
    anchorable_texts = [
        ("rendered_dom", html, raw_anchor),
        *[
            ("visible_text", text, _raw_anchor(preserved_file))
            for preserved_file, text in visible_text_files
        ],
    ]
    for module_type, patterns in module_specs:
        match = _first_module_anchor_match(anchorable_texts, patterns)
        if match is None:
            continue
        source_label, matched, anchor_fragment, excerpt, match_anchor = match
        modules.append(
            {
                "module_type": module_type,
                "retailer": retailer,
                "anchor_pattern": matched,
                "anchor_source": source_label,
                "text_excerpt": excerpt,
                "raw_anchor": _with_anchor(match_anchor, "text_pattern", anchor_fragment),
            }
        )
    return modules


def _collapse_entries(
    *,
    html: str,
    visible_text: str,
    raw_anchor: RetailProjectionRawAnchor,
) -> list[RetailPdpProjectionLossEntry]:
    entries: list[RetailPdpProjectionLossEntry] = []
    hero_count = len(re.findall(r"hero|ProductHero|imageBlock|main-hero", html, flags=re.IGNORECASE))
    if hero_count:
        entries.append(
            RetailPdpProjectionLossEntry(
                category="RETAIL_HERO_IMAGERY_COLLAPSED",
                count=hero_count,
                raw_anchor=_with_anchor(raw_anchor, "text_pattern", "hero|ProductHero|imageBlock|main-hero"),
                reason="hero imagery presence collapsed to raw-anchored ledger entry; raw bytes remain canonical",
            )
        )
    cart_count = len(re.findall(r"add to cart|add to bag|add for ship|out of stock|notify me", visible_text, flags=re.IGNORECASE))
    if cart_count:
        entries.append(
            RetailPdpProjectionLossEntry(
                category="RETAIL_CART_NOTIFY_STATE_COLLAPSED",
                count=cart_count,
                raw_anchor=_with_anchor(raw_anchor, "text_pattern", "add to cart|add to bag|add for ship|out of stock|notify me"),
                reason="cart/notify button chrome collapsed while variant availability binding is carried",
            )
        )
    return entries


def _product_context_fields(
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    retailer: str,
) -> dict[str, Any | None]:
    return {
        "retailer": retailer,
        "source_family": packet.source_family,
        "source_surface": packet.source_surface,
        "source_locator": _fact_value(packet.source_locator),
        "slice_locator": _fact_value(source_slice.locator),
        "series_id": packet.series_id,
        "locale_pin": _fact_value(source_slice.locale_pin),
        "currency_pin": _fact_value(source_slice.currency_pin),
        "variant_pin": _fact_value(source_slice.variant_pin),
        "location_pin": None,
        "capture_time": _fact_value(source_slice.timing.capture_time),
        "cutoff_posture": _fact_value(source_slice.timing.cutoff_posture),
        "archive_history_posture": _fact_value(source_slice.archive_history_posture),
    }


def _detect_retailer(packet: SourceCapturePacket) -> Literal["amazon", "sephora", "ulta", "unknown"]:
    haystack = " ".join(
        item
        for item in [
            packet.series_id or "",
            _fact_value(packet.source_locator) or "",
            packet.requested_decision_context.value if packet.requested_decision_context.status == VisibleFactStatus.KNOWN else "",
        ]
        if item
    ).lower()
    if "amazon." in haystack or "amazon_" in haystack or "amazon " in haystack:
        return "amazon"
    if "sephora." in haystack or "sephora_" in haystack or "sephora " in haystack:
        return "sephora"
    if "ulta." in haystack or "ulta_" in haystack or "ulta " in haystack:
        return "ulta"
    return "unknown"


def _extract_ld_json_texts(html: str) -> list[str]:
    return [
        match.group("body")
        for match in re.finditer(
            r"<script\b(?P<attrs>[^>]*)>(?P<body>.*?)</script>",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if re.search(r"type\s*=\s*['\"]application/ld\+json['\"]", match.group("attrs"), flags=re.IGNORECASE)
    ]


def _extract_apollo_state_text(html: str) -> str | None:
    marker = "window.__APOLLO_STATE__"
    marker_index = html.find(marker)
    if marker_index < 0:
        return None
    start = html.find("{", marker_index)
    if start < 0:
        return None
    return _balanced_json_object(html, start)


def _balanced_json_object(text: str, start: int) -> str | None:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    return None


def _safe_json_loads(raw_text: str | None) -> object | None:
    if raw_text is None:
        return None
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return None


def _walk_dicts(value: object) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    if isinstance(value, dict):
        found.append(value)
        for child in value.values():
            found.extend(_walk_dicts(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_walk_dicts(child))
    return found


def _raw_anchor(preserved_file: PreservedFile) -> RetailProjectionRawAnchor:
    return RetailProjectionRawAnchor(
        file_id=preserved_file.file_id,
        relative_packet_path=preserved_file.relative_packet_path,
        sha256=preserved_file.sha256,
        hash_basis=preserved_file.hash_basis,
        anchor_kind="file",
    )


def _with_anchor(raw_anchor: RetailProjectionRawAnchor, anchor_kind: str, anchor_value: str) -> RetailProjectionRawAnchor:
    return RetailProjectionRawAnchor(
        file_id=raw_anchor.file_id,
        relative_packet_path=raw_anchor.relative_packet_path,
        sha256=raw_anchor.sha256,
        hash_basis=raw_anchor.hash_basis,
        anchor_kind=anchor_kind,
        anchor_value=anchor_value,
    )


def _load_packet_directory_projection_inputs(packet_directory: Path) -> tuple[SourceCapturePacket, dict[str, bytes]]:
    manifest_path = packet_directory / "manifest.json"
    raw_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(raw_manifest, dict):
        raise RetailPdpProjectionInputError(f"manifest is not a JSON object: {manifest_path}")

    packet = SourceCapturePacket.model_validate(raw_manifest)
    raw_file_bytes_by_file_id: dict[str, bytes] = {}
    for preserved_file in packet.preserved_files:
        file_path = _resolve_packet_relative_path(
            packet_directory=packet_directory,
            relative_packet_path=preserved_file.relative_packet_path,
            file_id=preserved_file.file_id,
        )
        if not file_path.is_file():
            raise RetailPdpProjectionInputError(
                f"preserved file for {preserved_file.file_id!r} not found at "
                f"{preserved_file.relative_packet_path!r} under the packet dir; block-don't-repair."
            )
        body = file_path.read_bytes()
        if len(body) != preserved_file.size_bytes:
            raise RetailPdpProjectionInputError(
                f"preserved file size mismatch for {preserved_file.file_id!r} "
                f"(read {len(body)}, manifest {preserved_file.size_bytes}); block-don't-repair."
            )
        recomputed_sha256 = hashlib.sha256(body).hexdigest()
        if recomputed_sha256 != preserved_file.sha256:
            raise RetailPdpProjectionInputError(
                f"preserved file sha256 mismatch for {preserved_file.file_id!r} "
                f"(recomputed {recomputed_sha256}, manifest {preserved_file.sha256}); block-don't-repair."
            )
        raw_file_bytes_by_file_id[preserved_file.file_id] = body
    return packet, raw_file_bytes_by_file_id


def _resolve_packet_relative_path(*, packet_directory: Path, relative_packet_path: str, file_id: str) -> Path:
    candidate = Path(relative_packet_path)
    if candidate.is_absolute():
        raise RetailPdpProjectionInputError(
            f"preserved path {relative_packet_path!r} for {file_id!r} is absolute; block-don't-repair."
        )
    packet_root = packet_directory.resolve()
    resolved = (packet_root / candidate).resolve()
    try:
        resolved.relative_to(packet_root)
    except ValueError as exc:
        raise RetailPdpProjectionInputError(
            f"preserved path {relative_packet_path!r} for {file_id!r} resolves outside the packet dir; "
            f"block-don't-repair."
        ) from exc
    return resolved


def _decode_text(body: bytes) -> str:
    return body.decode("utf-8", errors="replace")


def _fact_value(fact: object | None) -> str | None:
    if fact is None:
        return None
    if getattr(fact, "status", None) == VisibleFactStatus.KNOWN:
        return getattr(fact, "value", None)
    return None


def _json_type(value: object | None) -> str | None:
    if isinstance(value, dict):
        at_type = value.get("@type")
        return str(at_type) if at_type is not None else "object"
    if isinstance(value, list):
        return "list"
    return None


def _first_regex(text: str, patterns: tuple[str, ...]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return " ".join(match.group(1).split())
    return None


def _first_literal(text: str, literals: tuple[str, ...]) -> str | None:
    lower = text.lower()
    for literal in literals:
        if literal.lower() in lower:
            return literal
    return None


def _html_attr_value(tag: str, attr_name: str) -> str | None:
    return _first_regex(tag, (rf"\b{re.escape(attr_name)}=[\"']([^\"']+)[\"']",))


def _string_or_none(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, (str, int, float)):
        text = str(value)
        return text if text else None
    return None


def _equivalent_offer_value(key: str, left: str, right: str) -> bool:
    if left == right:
        return True
    if key == "availability":
        return left.rstrip("/").endswith(right.rstrip("/")) or right.rstrip("/").endswith(left.rstrip("/"))
    return False


def _residualize_ulta_requested_sku_mismatch(
    fields: Mapping[str, Any | None],
    residuals: list[str],
    *,
    source_slice: SourceCaptureSlice | None = None,
) -> None:
    requested_sku = _string_or_none(fields.get("apollo_requested_sku"))
    if requested_sku is None and source_slice is not None:
        requested_sku = _sku_from_variant_pin(_fact_value(source_slice.variant_pin))
    rendered_sku = _string_or_none(fields.get("sku")) or _string_or_none(fields.get("apollo_sku"))
    residual = "ulta_requested_sku_rendered_sku_mismatch"
    if requested_sku and rendered_sku and requested_sku != rendered_sku and residual not in residuals:
        residuals.append(residual)


def _row_token(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.:-]+", "_", value) or "unknown"


def _excerpt(text: str, pattern: str, *, radius: int = 140) -> str:
    index = text.lower().find(pattern.lower())
    if index < 0:
        return ""
    return _compact_excerpt(text[max(0, index - radius) : index + len(pattern) + radius])


def _first_module_anchor_match(
    anchorable_texts: Sequence[tuple[str, str, RetailProjectionRawAnchor]],
    patterns: Sequence[str],
) -> tuple[str, str, str, str, RetailProjectionRawAnchor] | None:
    for pattern in patterns:
        for source_label, text, raw_anchor in anchorable_texts:
            index = _case_preferred_index(text, pattern)
            if index < 0:
                continue
            anchor_fragment = _raw_excerpt_fragment(text, index, len(pattern))
            return source_label, pattern, anchor_fragment, _compact_excerpt(anchor_fragment), raw_anchor
    return None


def _case_preferred_index(text: str, pattern: str) -> int:
    exact_index = text.find(pattern)
    if exact_index >= 0:
        return exact_index
    return text.lower().find(pattern.lower())


def _raw_excerpt_fragment(text: str, index: int, pattern_length: int, *, leading_radius: int = 40, trailing_radius: int = 180) -> str:
    return text[max(0, index - leading_radius) : index + pattern_length + trailing_radius].strip()


def _compact_excerpt(text: str) -> str:
    return " ".join(text.split())


def _is_forbidden_field_name(key: str) -> bool:
    normalized = key.lower().replace("-", "_")
    parts = normalized.split("_")
    return any(
        token == normalized or token in parts or token in normalized
        for token in _FORBIDDEN_SOURCE_VISIBLE_FIELD_NAMES
    )


__all__ = [
    "RETAIL_PDP_PROJECTION_CERTIFICATION",
    "RETAIL_PDP_PROJECTION_METHOD",
    "RETAIL_PDP_PROJECTION_VERSION",
    "PROJECTION_RETAIL_PDP_LANE",
    "RetailPdpProjectionInputError",
    "RetailPdpProjectionBinding",
    "RetailPdpProjectionLossEntry",
    "RetailPdpProjectionLossLedger",
    "RetailPdpProjectionPacket",
    "RetailPdpProjectionRow",
    "RetailProjectionRawAnchor",
    "RetailProjectionRawRef",
    "build_retail_pdp_projection",
    "build_retail_pdp_projection_from_packet_directory",
    "project_retail_pdp_into_lake",
    "write_retail_pdp_projection",
]
