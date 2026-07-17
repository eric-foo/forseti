from __future__ import annotations

import hashlib
import html as html_module
import json
import re
from pathlib import Path
from typing import Any, Literal, Mapping
from urllib.parse import urljoin

from pydantic import Field, field_validator, model_validator

from schemas.case_models import StrictModel
from source_capture.models import PreservedFile, SourceCapturePacket, SourceCaptureSlice, VisibleFactStatus
from source_capture.projection_shared import is_forbidden_field_token_match
from source_capture.retail_pdp_projection import RetailProjectionRawAnchor, RetailProjectionRawRef


RETAIL_GRID_PROJECTION_METHOD = "retail_grid_mechanical_projection"
RETAIL_GRID_PROJECTION_VERSION = "v0"
RETAIL_GRID_PROJECTION_CERTIFICATION = "view_only; not_cleaned; not_normalized; not_judgment_ready"

RetailGridRetailer = Literal["walmart", "target"]

_FORBIDDEN_FIELD_TOKENS = frozenset(
    {
        "action_ceiling",
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
_NEXT_DATA_RE = re.compile(
    r"<script[^>]+id=[\"']__NEXT_DATA__[\"'][^>]*>(?P<json>.*?)</script>",
    flags=re.IGNORECASE | re.DOTALL,
)
_TARGET_CARD_RE = re.compile(
    r"<div[^>]*\bdata-focusid=[\"'](?P<product_id>\d+)_product_card[\"'][^>]*>",
    flags=re.IGNORECASE,
)


class RetailGridProjectionInputError(ValueError):
    """A packet cannot be projected without verified raw files and grid identity."""


class RetailGridProjectionRow(StrictModel):
    row_id: str
    row_kind: Literal["retail_grid_product"] = "retail_grid_product"
    retailer: RetailGridRetailer
    raw_ref: RetailProjectionRawRef
    raw_anchor: RetailProjectionRawAnchor
    source_visible_fields: dict[str, Any | None]
    residuals: list[str] = Field(default_factory=list)

    @field_validator("source_visible_fields")
    @classmethod
    def require_identity_and_reject_judgment(
        cls, value: dict[str, Any | None]
    ) -> dict[str, Any | None]:
        missing = [
            field
            for field in ("source_product_id", "product_url", "name")
            if not isinstance(value.get(field), str) or not str(value[field]).strip()
        ]
        if missing:
            raise ValueError(
                "retail grid product rows require non-empty source identity fields: "
                + ", ".join(missing)
            )
        forbidden = sorted(key for key in value if _is_forbidden_field_name(key))
        if forbidden:
            raise ValueError(
                "retail grid projection may carry source-visible facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value


class RetailGridProjectionLossLedger(StrictModel):
    preserved_evidence_rows: int = Field(ge=0)
    timing: Literal["separate_not_collapsed"] = "separate_not_collapsed"
    hierarchy_preserved: bool = True
    structure_preserved: bool
    certification: Literal[
        "source_visible_product_tiles_preserved; does_not_certify_cleaning"
    ] = "source_visible_product_tiles_preserved; does_not_certify_cleaning"


class RetailGridProjectionPacket(StrictModel):
    projection_method: Literal["retail_grid_mechanical_projection"] = RETAIL_GRID_PROJECTION_METHOD
    projection_version: Literal["v0"] = RETAIL_GRID_PROJECTION_VERSION
    certification: Literal[
        "view_only; not_cleaned; not_normalized; not_judgment_ready"
    ] = RETAIL_GRID_PROJECTION_CERTIFICATION
    packet_id: str
    rows: list[RetailGridProjectionRow] = Field(default_factory=list)
    loss_ledger: RetailGridProjectionLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "RetailGridProjectionPacket":
        if self.loss_ledger.preserved_evidence_rows != len(self.rows):
            raise ValueError("loss_ledger.preserved_evidence_rows must match rows length")
        if self.loss_ledger.structure_preserved != bool(self.rows):
            raise ValueError("grid structure_preserved must be true exactly when product rows exist")
        return self


def build_retail_grid_projection_from_packet_directory(
    *, packet_directory: Path
) -> RetailGridProjectionPacket:
    packet, raw_file_bytes_by_file_id = _load_packet_directory_projection_inputs(packet_directory)
    return build_retail_grid_projection(
        packet=packet, raw_file_bytes_by_file_id=raw_file_bytes_by_file_id
    )


def write_retail_grid_projection(
    *, packet_directory: Path, output_path: Path
) -> RetailGridProjectionPacket:
    projection = build_retail_grid_projection_from_packet_directory(
        packet_directory=packet_directory
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        f"{json.dumps(projection.model_dump(mode='json'), indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    return projection


def build_retail_grid_projection(
    *, packet: SourceCapturePacket, raw_file_bytes_by_file_id: Mapping[str, bytes]
) -> RetailGridProjectionPacket:
    retailer = _detect_retailer(packet)
    preserved_files = {item.file_id: item for item in packet.preserved_files}
    rows: list[RetailGridProjectionRow] = []
    residuals: list[str] = []

    for source_slice in packet.source_slices:
        raw_ref = RetailProjectionRawRef(
            packet_id=packet.packet_id, slice_id=source_slice.slice_id
        )
        slice_row_count = 0
        for file_id in source_slice.preserved_file_ids:
            preserved_file = preserved_files[file_id]
            body = raw_file_bytes_by_file_id.get(file_id)
            if body is None:
                raise ValueError(f"raw bytes are required for preserved file id: {file_id}")
            raw_anchor = _raw_anchor(preserved_file)
            text = body.decode("utf-8", errors="replace")
            if retailer == "walmart":
                projected, file_residuals = _project_walmart_next_data(
                    text,
                    packet=packet,
                    source_slice=source_slice,
                    raw_ref=raw_ref,
                    raw_anchor=raw_anchor,
                )
            else:
                projected, file_residuals = _project_target_cards(
                    text,
                    packet=packet,
                    source_slice=source_slice,
                    raw_ref=raw_ref,
                    raw_anchor=raw_anchor,
                )
            rows.extend(projected)
            residuals.extend(file_residuals)
            slice_row_count += len(projected)
        if slice_row_count == 0:
            residuals.append(f"{source_slice.slice_id}:{retailer}:grid_product_tiles_absent")

    return RetailGridProjectionPacket(
        packet_id=packet.packet_id,
        rows=rows,
        loss_ledger=RetailGridProjectionLossLedger(
            preserved_evidence_rows=len(rows), structure_preserved=bool(rows)
        ),
        residuals=_dedupe(residuals),
    )


def _project_walmart_next_data(
    text: str,
    *,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    raw_ref: RetailProjectionRawRef,
    raw_anchor: RetailProjectionRawAnchor,
) -> tuple[list[RetailGridProjectionRow], list[str]]:
    match = _NEXT_DATA_RE.search(text)
    if match is None:
        return [], []
    try:
        payload = json.loads(match.group("json"))
    except json.JSONDecodeError as exc:
        raise RetailGridProjectionInputError("Walmart __NEXT_DATA__ is malformed") from exc

    stacks = _nested_value(
        payload, "props", "pageProps", "initialData", "searchResult", "itemStacks"
    )
    if not isinstance(stacks, list):
        return [], []

    rows: list[RetailGridProjectionRow] = []
    residuals: list[str] = []
    for stack_index, stack in enumerate(stacks):
        items = stack.get("items") if isinstance(stack, dict) else None
        if not isinstance(items, list):
            continue
        for item_index, item in enumerate(items):
            if not isinstance(item, dict) or item.get("__typename") != "Product":
                continue
            product_id = _text(item.get("usItemId"))
            product_url = _absolute_url("https://www.walmart.com", _text(item.get("canonicalUrl")))
            name = _text(item.get("name"))
            if product_id is None or product_url is None or name is None:
                residuals.append(
                    f"{source_slice.slice_id}:walmart:grid_tile_identity_incomplete:"
                    f"{stack_index}:{item_index}"
                )
                continue
            pointer = (
                f"/props/pageProps/initialData/searchResult/itemStacks/{stack_index}"
                f"/items/{item_index}"
            )
            fields = _base_fields(packet=packet, source_slice=source_slice, retailer="walmart")
            fields.update(
                {
                    "source_product_id": product_id,
                    "product_url": product_url,
                    "name": name,
                    "selected_variant": _walmart_selected_variant(item, product_id),
                    "price": _walmart_price(item),
                    "price_currency": _fact_value(source_slice.currency_pin),
                    "currency_symbol": "$" if _walmart_price_text(item).startswith("$") else None,
                    "average_rating": _first_present(item.get("averageRating"), _nested_value(item, "rating", "averageRating")),
                    "rating_count": _first_present(item.get("numberOfReviews"), _nested_value(item, "rating", "numberOfReviews")),
                    "written_review_count": None,
                    "availability_summary": _first_present(
                        _nested_value(item, "availabilityStatusV2", "display"),
                        item.get("availabilityStatusDisplayValue"),
                    ),
                    "shipping_availability": _walmart_fulfilment_badge(item, "FF_SHIPPING"),
                    "pickup_availability": _walmart_fulfilment_badge(item, "FF_PICKUP"),
                    "delivery_availability": _walmart_fulfilment_badge(item, "FF_DELIVERY"),
                    "location_ids": _walmart_location_ids(item),
                    "seller": _text(item.get("sellerName")),
                }
            )
            row_residuals = _row_residuals(
                retailer="walmart",
                selected_variant=fields["selected_variant"],
                location_observed=bool(fields["location_ids"]),
            )
            rows.append(
                RetailGridProjectionRow(
                    row_id=(
                        f"{source_slice.slice_id}:grid:walmart:{stack_index}:{item_index}:"
                        f"{product_id or 'missing'}"
                    ),
                    retailer="walmart",
                    raw_ref=raw_ref,
                    raw_anchor=_with_anchor(raw_anchor, "json_pointer", pointer),
                    source_visible_fields=fields,
                    residuals=row_residuals,
                )
            )
    return rows, residuals


def _project_target_cards(
    text: str,
    *,
    packet: SourceCapturePacket,
    source_slice: SourceCaptureSlice,
    raw_ref: RetailProjectionRawRef,
    raw_anchor: RetailProjectionRawAnchor,
) -> tuple[list[RetailGridProjectionRow], list[str]]:
    matches = list(_TARGET_CARD_RE.finditer(text))
    rows: list[RetailGridProjectionRow] = []
    residuals: list[str] = []
    occurrences_by_product_id: dict[str, int] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        card = text[match.start() : end]
        product_id = match.group("product_id")
        occurrence = occurrences_by_product_id.get(product_id, 0) + 1
        occurrences_by_product_id[product_id] = occurrence
        product_url = _absolute_url(
            "https://www.target.com",
            _first_regex(
                card,
                (
                    r"href=[\"']([^\"']*/p/[^\"']+)[\"']",
                ),
            ),
        )
        name = _first_regex(
            card,
            (
                r"<a[^>]+aria-label=[\"']([^\"']+)[\"'][^>]+data-test=[\"']@web/ProductCard/title[\"']",
                r"data-test=[\"']@web/ProductCard/title[\"'][^>]+aria-label=[\"']([^\"']+)[\"']",
            ),
        )
        if product_url is None or name is None:
            residuals.append(
                f"{source_slice.slice_id}:target:grid_card_identity_incomplete:{product_id}"
            )
            continue
        rating_match = re.search(
            r"aria-label=[\"']([0-9.]+)\s+stars?\s+with\s+([0-9,]+)\s+ratings?[\"']",
            card,
            flags=re.IGNORECASE,
        )
        price_text = _first_regex(
            card,
            (r"data-test=[\"']current-price[\"'][^>]*>\s*<span>\s*([^<]+)",),
        )
        pickup = _target_channel_text(card, "Pickup")
        delivery = _target_channel_text(card, "Delivery")
        shipping = _target_channel_text(card, "Shipping")
        overall_availability = _first_regex(
            card,
            (r"data-test=[\"']lowStockMessaging[\"'][^>]*>.*?<span[^>]*>([^<]+)</span>",),
        )
        fields = _base_fields(packet=packet, source_slice=source_slice, retailer="target")
        fields.update(
            {
                "source_product_id": product_id,
                "product_url": product_url,
                "name": html_module.unescape(name) if name else None,
                "selected_variant": None,
                "price": price_text.lstrip("$").strip() if price_text else None,
                "price_currency": _fact_value(source_slice.currency_pin),
                "currency_symbol": "$" if price_text and price_text.startswith("$") else None,
                "average_rating": rating_match.group(1) if rating_match else None,
                "rating_count": rating_match.group(2).replace(",", "") if rating_match else None,
                "written_review_count": None,
                "availability_summary": html_module.unescape(overall_availability) if overall_availability else None,
                "shipping_availability": shipping,
                "pickup_availability": pickup,
                "delivery_availability": delivery,
                "location_ids": [],
                "seller": None,
            }
        )
        rows.append(
            RetailGridProjectionRow(
                row_id=f"{source_slice.slice_id}:grid:target:{index}:{product_id}",
                retailer="target",
                raw_ref=raw_ref,
                raw_anchor=_with_anchor(
                    raw_anchor,
                    "html_selector",
                    f':nth-match([data-focusid="{product_id}_product_card"], {occurrence})',
                ),
                source_visible_fields=fields,
                residuals=_row_residuals(
                    retailer="target", selected_variant=None, location_observed=False
                ),
            )
        )
    return rows, residuals


def _base_fields(
    *, packet: SourceCapturePacket, source_slice: SourceCaptureSlice, retailer: RetailGridRetailer
) -> dict[str, Any | None]:
    return {
        "retailer": retailer,
        "page_kind": "grid",
        "capture_time": _fact_value(source_slice.timing.capture_time),
        "locale_pin": _fact_value(source_slice.locale_pin),
        "location_pin": None,
        "series_id": packet.series_id,
        "exact_inventory_quantity": None,
        "exact_inventory_quantity_posture": "not_observed",
        "sold_units": None,
        "sold_units_posture": "not_observed",
    }


def _row_residuals(
    *, retailer: RetailGridRetailer, selected_variant: object, location_observed: bool
) -> list[str]:
    residuals = [
        f"{retailer}_grid_written_review_count_not_observed",
        f"{retailer}_grid_exact_inventory_quantity_not_observed",
        f"{retailer}_grid_sold_units_not_observed",
    ]
    if selected_variant is None:
        residuals.append(f"{retailer}_grid_selected_variant_not_observed")
    if not location_observed:
        residuals.append(f"{retailer}_grid_location_pin_not_observed")
    return residuals


def _walmart_selected_variant(item: dict[str, Any], product_id: str | None) -> str | None:
    variants = item.get("variantList")
    if not isinstance(variants, list) or product_id is None:
        return None
    for variant in variants:
        if isinstance(variant, dict) and _text(variant.get("usItemId")) == product_id:
            return _first_text(variant.get("displayName"), variant.get("name"))
    return None


def _walmart_price(item: dict[str, Any]) -> str | None:
    value = item.get("price")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    text = _walmart_price_text(item)
    return text.lstrip("$").strip() or None


def _walmart_price_text(item: dict[str, Any]) -> str:
    return _first_text(
        _nested_value(item, "priceInfo", "linePriceDisplay"),
        _nested_value(item, "priceInfo", "linePrice"),
    ) or ""


def _walmart_fulfilment_badge(item: dict[str, Any], key: str) -> str | None:
    badges = item.get("fulfillmentBadgeGroups")
    if not isinstance(badges, list):
        return None
    for badge in badges:
        if isinstance(badge, dict) and badge.get("key") == key:
            parts = [_text(badge.get("text")), _text(badge.get("slaText"))]
            return " ".join(part for part in parts if part).strip() or None
    return None


def _walmart_location_ids(item: dict[str, Any]) -> list[str]:
    summaries = item.get("fulfillmentSummary")
    if not isinstance(summaries, list):
        return []
    return _dedupe(
        _text(summary.get("storeId"))
        for summary in summaries
        if isinstance(summary, dict) and _text(summary.get("storeId"))
    )


def _target_channel_text(card: str, label: str) -> str | None:
    value = _first_regex(
        card,
        (
            rf"<span[^>]*>\s*{re.escape(label)}\s*</span>\s*<span[^>]*>([^<]+)</span>",
        ),
    )
    return html_module.unescape(value) if value else None


def _detect_retailer(packet: SourceCapturePacket) -> RetailGridRetailer:
    locators = [_fact_value(packet.source_locator)] + [
        _fact_value(source_slice.locator) for source_slice in packet.source_slices
    ]
    joined = " ".join(value.lower() for value in locators if value)
    if "walmart." in joined:
        return "walmart"
    if "target." in joined:
        return "target"
    raise RetailGridProjectionInputError(
        "retail grid projection supports only source-visible Walmart or Target locators"
    )


def _load_packet_directory_projection_inputs(
    packet_directory: Path,
) -> tuple[SourceCapturePacket, dict[str, bytes]]:
    manifest_path = packet_directory / "manifest.json"
    if not manifest_path.is_file():
        raise RetailGridProjectionInputError(f"packet manifest not found: {manifest_path}")
    raw_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(raw_manifest, dict):
        raise RetailGridProjectionInputError(f"manifest is not a JSON object: {manifest_path}")
    packet = SourceCapturePacket.model_validate(raw_manifest)
    bodies: dict[str, bytes] = {}
    packet_root = packet_directory.resolve()
    for preserved_file in packet.preserved_files:
        relative = Path(preserved_file.relative_packet_path)
        if relative.is_absolute():
            raise RetailGridProjectionInputError(
                f"preserved path for {preserved_file.file_id!r} is absolute; block-don't-repair"
            )
        resolved = (packet_root / relative).resolve()
        try:
            resolved.relative_to(packet_root)
        except ValueError as exc:
            raise RetailGridProjectionInputError(
                f"preserved path for {preserved_file.file_id!r} resolves outside the packet dir; block-don't-repair"
            ) from exc
        if not resolved.is_file():
            raise RetailGridProjectionInputError(
                f"preserved file for {preserved_file.file_id!r} not found; block-don't-repair"
            )
        body = resolved.read_bytes()
        if len(body) != preserved_file.size_bytes:
            raise RetailGridProjectionInputError(
                f"preserved file size mismatch for {preserved_file.file_id!r}; block-don't-repair"
            )
        if hashlib.sha256(body).hexdigest() != preserved_file.sha256:
            raise RetailGridProjectionInputError(
                f"preserved file sha256 mismatch for {preserved_file.file_id!r}; block-don't-repair"
            )
        bodies[preserved_file.file_id] = body
    return packet, bodies


def _raw_anchor(preserved_file: PreservedFile) -> RetailProjectionRawAnchor:
    return RetailProjectionRawAnchor(
        file_id=preserved_file.file_id,
        relative_packet_path=preserved_file.relative_packet_path,
        sha256=preserved_file.sha256,
        hash_basis=preserved_file.hash_basis,
        anchor_kind="file",
    )


def _with_anchor(
    raw_anchor: RetailProjectionRawAnchor,
    anchor_kind: Literal["json_pointer", "text_pattern"],
    anchor_value: str,
) -> RetailProjectionRawAnchor:
    return raw_anchor.model_copy(
        update={"anchor_kind": anchor_kind, "anchor_value": anchor_value}
    )


def _nested_value(value: object, *keys: str) -> object | None:
    current = value
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def _fact_value(fact: object | None) -> str | None:
    if fact is not None and getattr(fact, "status", None) == VisibleFactStatus.KNOWN:
        return getattr(fact, "value", None)
    return None


def _absolute_url(base: str, value: str | None) -> str | None:
    return urljoin(base, html_module.unescape(value)) if value else None


def _first_regex(text: str, patterns: tuple[str, ...]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return " ".join(match.group(1).split())
    return None


def _first_present(*values: object) -> object | None:
    return next((value for value in values if value is not None and value != ""), None)


def _first_text(*values: object) -> str | None:
    return next((text for value in values if (text := _text(value))), None)


def _text(value: object) -> str | None:
    if isinstance(value, (str, int, float)) and not isinstance(value, bool):
        text = str(value).strip()
        return text or None
    return None


def _dedupe(values: Any) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))


def _is_forbidden_field_name(key: str) -> bool:
    return is_forbidden_field_token_match(key, _FORBIDDEN_FIELD_TOKENS)


__all__ = [
    "RETAIL_GRID_PROJECTION_CERTIFICATION",
    "RETAIL_GRID_PROJECTION_METHOD",
    "RETAIL_GRID_PROJECTION_VERSION",
    "RetailGridProjectionInputError",
    "RetailGridProjectionLossLedger",
    "RetailGridProjectionPacket",
    "RetailGridProjectionRow",
    "build_retail_grid_projection",
    "build_retail_grid_projection_from_packet_directory",
    "write_retail_grid_projection",
]
