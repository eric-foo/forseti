from __future__ import annotations

import re
import unicodedata
from typing import Any, Mapping
from urllib.parse import urlparse, urlunparse

from source_capture.models import SourceCapturePacket, VisibleFactStatus
from source_capture.revolve_brand_grid import (
    REVOLVE_GRID_CONTENT_RECORD_VERSION,
    RevolveBrandGridState,
    RevolveBrandGridStateError,
    load_revolve_brand_grid_state,
)


_PRICE_RE = re.compile(
    r"^\s*\$(?P<price>\d+(?:\.\d+)?)(?:\s*\(\$(?P<value>\d+(?:\.\d+)?)\s+Value\))?\s*$",
    re.IGNORECASE,
)
_SALE_RE = re.compile(
    r"Sale price:\s*\$(?P<sale>\d+(?:\.\d+)?)\s*"
    r"Previous price:\s*\$(?P<list>\d+(?:\.\d+)?)",
    re.IGNORECASE,
)


def build_revolve_grid_projection(
    *, packet: SourceCapturePacket, raw_file_bytes_by_file_id: Mapping[str, bytes]
):
    from source_capture.retail_grid_projection import (
        RetailGridCompletenessReconciliation,
        RetailGridProjectionInputError,
        RetailGridProjectionLossLedger,
        RetailGridProjectionPacket,
        RetailGridProjectionPlacement,
        RetailGridProjectionRow,
    )
    from source_capture.retail_pdp_projection import (
        RetailProjectionRawAnchor,
        RetailProjectionRawRef,
    )

    preserved_files = {item.file_id: item for item in packet.preserved_files}
    rows: list[RetailGridProjectionRow] = []
    residuals: list[str] = []
    states: list[RevolveBrandGridState] = []
    for source_slice in packet.source_slices:
        raw_ref = RetailProjectionRawRef(
            packet_id=packet.packet_id, slice_id=source_slice.slice_id
        )
        slice_count = 0
        for file_id in source_slice.preserved_file_ids:
            body = raw_file_bytes_by_file_id.get(file_id)
            if body is None:
                raise ValueError(f"raw bytes are required for preserved file id: {file_id}")
            try:
                state = load_revolve_brand_grid_state(
                    body.decode("utf-8", errors="replace")
                )
            except RevolveBrandGridStateError as exc:
                raise RetailGridProjectionInputError(str(exc)) from exc
            if state is None:
                continue
            states.append(state)
            preserved = preserved_files[file_id]
            file_anchor = RetailProjectionRawAnchor(
                file_id=preserved.file_id,
                relative_packet_path=preserved.relative_packet_path,
                sha256=preserved.sha256,
                hash_basis=preserved.hash_basis,
                anchor_kind="file",
            )
            for card in state.cards:
                if card.product_url is None or card.name is None or card.brand_name is None:
                    residuals.append(
                        f"{source_slice.slice_id}:revolve:grid_tile_identity_incomplete:{card.grid_position}"
                    )
                    continue
                if state.content_record_version == REVOLVE_GRID_CONTENT_RECORD_VERSION:
                    anchor = file_anchor.model_copy(
                        update={
                            "anchor_kind": "json_pointer",
                            "anchor_value": f"/cards/{card.grid_position - 1}",
                        }
                    )
                else:
                    anchor = file_anchor.model_copy(
                        update={
                            "anchor_kind": "html_selector",
                            "anchor_value": f"li.plp__product#{card.style_id}",
                        }
                    )
                price, list_price = _prices(card.price_display)
                row_residuals = [
                    "revolve_grid_exact_inventory_quantity_not_observed",
                    "revolve_grid_sold_units_not_observed",
                    "revolve_grid_delivery_location_not_observed",
                    "revolve_grid_category_not_observed",
                ]
                if card.average_rating is None and card.review_count == 0:
                    row_residuals.append("revolve_grid_zero_or_absent_review_aggregate")
                if card.out_of_stock is None:
                    row_residuals.append("revolve_grid_availability_not_observed")
                if price is None:
                    row_residuals.append("revolve_grid_price_not_mechanically_parsed")
                fields: dict[str, Any | None] = {
                    "retailer": "revolve",
                    "page_kind": "grid",
                    "capture_time": _fact_value(source_slice.timing.capture_time),
                    "locale_pin": _fact_value(source_slice.locale_pin),
                    "location_pin": None,
                    "series_id": packet.series_id,
                    "source_product_id": card.style_id,
                    "style_id": card.style_id,
                    "product_url": card.product_url,
                    "canonical_product_url": _canonical(card.product_url),
                    "name": card.name,
                    "brand": card.brand_name,
                    "grid_position": card.grid_position,
                    "selected_variant": card.selected_color,
                    "visible_variant_count": len(card.color_names),
                    "visible_variant_names": list(card.color_names),
                    "price": price,
                    "list_price": list_price,
                    "price_display": card.price_display,
                    "price_currency": state.currency_code,
                    "currency_symbol": "$" if card.price_display else None,
                    "average_rating": card.average_rating,
                    "rating_count": card.review_count,
                    "review_count": card.review_count,
                    "badges": list(card.badges),
                    "availability_summary": (
                        "out_of_stock"
                        if card.out_of_stock is True
                        else "available"
                        if card.out_of_stock is False
                        else None
                    ),
                    "image_urls": list(card.image_urls),
                    "seller": "REVOLVE",
                    "country_code": state.country_code,
                }
                rows.append(
                    RetailGridProjectionRow(
                        row_id=(
                            f"{source_slice.slice_id}:grid:revolve:{card.style_id}"
                        ),
                        retailer="revolve",
                        raw_ref=raw_ref,
                        raw_anchor=anchor,
                        placements=[
                            RetailGridProjectionPlacement(
                                grid_position=card.grid_position, raw_anchor=anchor
                            )
                        ],
                        source_visible_fields=fields,
                        residuals=row_residuals,
                    )
                )
                slice_count += 1
        if slice_count == 0:
            residuals.append(f"{source_slice.slice_id}:revolve:grid_product_tiles_absent")

    rows, merge_residuals = _merge(rows)
    residuals.extend(merge_residuals)
    placement_count = sum(len(row.placements) for row in rows)
    state = states[0] if len(states) == 1 else None
    completeness_residuals: list[str] = []
    if not states:
        completeness_residuals.append("revolve_grid_state_absent")
    elif len(states) != 1:
        completeness_residuals.append(f"revolve_grid_state_count:{len(states)}")
    requested_slug, requested_brand_id = _requested_subject(packet)
    observed_slug = _slugify(state.brand_name) if state and state.brand_name else None
    subject_confirmed = bool(
        state
        and requested_slug
        and requested_brand_id
        and state.brand_slug == requested_slug
        and state.brand_id == requested_brand_id
        and observed_slug == requested_slug
    )
    if not subject_confirmed:
        completeness_residuals.append("revolve_grid_subject_binding_unconfirmed")
    declared = state.declared_count if state else None
    if declared is None:
        completeness_residuals.append("revolve_grid_declared_count_absent")
    elif declared != placement_count:
        completeness_residuals.append(
            "revolve_grid_declared_placement_count_mismatch:"
            f"declared={declared}:anchored={placement_count}"
        )
    if state and len(state.cards) != placement_count:
        completeness_residuals.append(
            "revolve_grid_serialized_placement_count_mismatch:"
            f"serialized={len(state.cards)}:anchored={placement_count}"
        )
    if state and state.continuation_control_present:
        completeness_residuals.append("revolve_grid_continuation_control_present")
    if state and (
        state.view_limit is None
        or state.declared_count is None
        or state.view_limit < state.declared_count
    ):
        completeness_residuals.append("revolve_grid_view_limit_does_not_cover_declared_count")
    if state and (state.country_code != "US" or state.currency_code != "USD"):
        completeness_residuals.append("revolve_grid_usd_market_unconfirmed")
    if any("identity_incomplete" in item for item in residuals):
        completeness_residuals.append("revolve_grid_incomplete_product_identity_present")
    complete = not completeness_residuals
    completeness = RetailGridCompletenessReconciliation(
        status="complete" if complete else "incomplete",
        page_declared_result_count=declared,
        extracted_unique_parent_count=len(rows),
        extracted_placement_count=placement_count,
        duplicate_placement_count=placement_count - len(rows),
        subject_binding_confirmed=subject_confirmed,
        termination=(
            "retailer_visible_count_reconciled" if complete else "unproven"
        ),
        residuals=completeness_residuals,
    )
    return RetailGridProjectionPacket(
        packet_id=packet.packet_id,
        rows=rows,
        source_visible_grid_facts={
            "retailer": "revolve",
            "page_kind": "brand_grid",
            "brand_name": state.brand_name if state else None,
            "requested_brand_slug": requested_slug,
            "requested_brand_id": requested_brand_id,
            "observed_brand_slug": state.brand_slug if state else None,
            "observed_brand_id": state.brand_id if state else None,
            "subject_binding_confirmed": subject_confirmed,
            "page_declared_result_count": declared,
            "view_limit": state.view_limit if state else None,
            "country_code": state.country_code if state else None,
            "currency_code": state.currency_code if state else None,
        },
        completeness=completeness,
        loss_ledger=RetailGridProjectionLossLedger(
            preserved_evidence_rows=len(rows), structure_preserved=bool(rows)
        ),
        residuals=list(dict.fromkeys(residuals)),
    )


def _merge(rows):
    merged = {}
    residuals: list[str] = []
    for row in rows:
        product_id = str(row.source_visible_fields["source_product_id"])
        existing = merged.get(product_id)
        if existing is None:
            merged[product_id] = row
            continue
        placements = [*existing.placements, *row.placements]
        marker = f"revolve_grid_duplicate_style_placement:{product_id}:{len(placements)}"
        merged[product_id] = existing.model_copy(
            update={
                "placements": placements,
                "residuals": list(dict.fromkeys([*existing.residuals, marker])),
            }
        )
        residuals.append(marker)
    return list(merged.values()), residuals


def _requested_subject(packet: SourceCapturePacket) -> tuple[str | None, str | None]:
    locators = [_fact_value(packet.source_locator)] + [
        _fact_value(source_slice.locator) for source_slice in packet.source_slices
    ]
    for locator in locators:
        if not locator:
            continue
        match = re.fullmatch(
            r"/(?P<slug>[a-z0-9][a-z0-9-]*)/br/(?P<brand_id>[a-f0-9]{6})",
            urlparse(locator).path.rstrip("/"),
            flags=re.IGNORECASE,
        )
        if match:
            return match.group("slug").lower(), match.group("brand_id").lower()
    return None, None


def _prices(value: str | None) -> tuple[str | None, str | None]:
    if value is None:
        return None, None
    sale = _SALE_RE.search(value)
    if sale:
        return sale.group("sale"), sale.group("list")
    regular = _PRICE_RE.fullmatch(value)
    return (regular.group("price"), None) if regular else (None, None)


def _canonical(value: str) -> str:
    parsed = urlparse(value)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))


def _fact_value(fact: object | None) -> str | None:
    if fact is not None and getattr(fact, "status", None) == VisibleFactStatus.KNOWN:
        return getattr(fact, "value", None)
    return None


def _slugify(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.lower())
    folded = "".join(
        character
        for character in decomposed
        if not unicodedata.combining(character) and character not in "'’"
    )
    return re.sub(r"[^a-z0-9]+", "-", folded).strip("-")


__all__ = ["build_revolve_grid_projection"]
