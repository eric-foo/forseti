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


BASENOTES_PROJECTION_METHOD = "basenotes_current_window_mechanical_projection"
BASENOTES_PROJECTION_VERSION = "v0"
BASENOTES_PROJECTION_CERTIFICATION = "view_only; not_cleaned; not_normalized; not_judgment_ready"
PROJECTION_BASENOTES_LANE = "projection_basenotes"

_BASENOTES_SOURCE_FAMILY = "fragrance_native_database"
_BASENOTES_SOURCE_SURFACE = "basenotes_product_page_cloakbrowser_deep_scroll_current_window"
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

# Basenotes' reviews live in the page's schema.org JSON-LD as Product.review[], NOT in
# data-review-id HTML attributes (Parfumo's shape). Each review is an in-page SUBSET of the
# declared "N Reviews" corpus; the sentiment sub-URLs below are the archive gate, not AJAX.
_SENTIMENT_TABS = ("positive", "neutral", "negative")


class BasenotesProjectionRawRef(StrictModel):
    packet_id: str
    slice_id: str


class BasenotesProjectionRawAnchor(StrictModel):
    file_id: str
    relative_packet_path: str
    sha256: str
    hash_basis: str
    anchor_kind: Literal["file", "html_selector", "text_pattern"] = "file"
    anchor_value: str | None = None

    @model_validator(mode="after")
    def validate_anchor_value(self) -> "BasenotesProjectionRawAnchor":
        if self.anchor_kind != "file" and not (self.anchor_value and self.anchor_value.strip()):
            raise ValueError(f"{self.anchor_kind} anchors require anchor_value")
        if self.anchor_kind == "file" and self.anchor_value is not None:
            raise ValueError("file anchors must not carry anchor_value")
        return self


class BasenotesProjectionRow(StrictModel):
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
    raw_ref: BasenotesProjectionRawRef
    raw_anchor: BasenotesProjectionRawAnchor
    source_platform: Literal["basenotes"] = "basenotes"
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
                "Basenotes projection source_visible_fields may carry raw facts only; "
                f"forbidden Judgment field(s): {', '.join(forbidden)}"
            )
        return value


class BasenotesProjectionBinding(StrictModel):
    binding_type: Literal[
        "review_metadata_to_review_text",
        "statement_metadata_to_statement_text",
    ]
    row_id: str
    raw_ref: BasenotesProjectionRawRef
    raw_anchor: BasenotesProjectionRawAnchor


class BasenotesProjectionLossLedger(StrictModel):
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


class BasenotesProjectionPacket(StrictModel):
    projection_method: Literal["basenotes_current_window_mechanical_projection"] = (
        BASENOTES_PROJECTION_METHOD
    )
    projection_version: Literal["v0"] = BASENOTES_PROJECTION_VERSION
    certification: Literal["view_only; not_cleaned; not_normalized; not_judgment_ready"] = (
        BASENOTES_PROJECTION_CERTIFICATION
    )
    packet_id: str
    rows: list[BasenotesProjectionRow] = Field(default_factory=list)
    binding_map: list[BasenotesProjectionBinding] = Field(default_factory=list)
    loss_ledger: BasenotesProjectionLossLedger
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_counts(self) -> "BasenotesProjectionPacket":
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


def build_basenotes_projection(
    *,
    packet: SourceCapturePacket,
    raw_file_bytes_by_file_id: Mapping[str, bytes],
) -> BasenotesProjectionPacket:
    """Derive a Basenotes current-window row view from preserved packet bytes."""
    if packet.source_family != _BASENOTES_SOURCE_FAMILY:
        raise ValueError(
            "Basenotes projection requires "
            f"source_family={_BASENOTES_SOURCE_FAMILY!r}; got {packet.source_family!r}"
        )
    if packet.source_surface != _BASENOTES_SOURCE_SURFACE:
        raise ValueError(
            "Basenotes projection requires "
            f"source_surface={_BASENOTES_SOURCE_SURFACE!r}; got {packet.source_surface!r}"
        )

    preserved_files = {item.file_id: item for item in packet.preserved_files}
    for source_slice in packet.source_slices:
        for file_id in source_slice.preserved_file_ids:
            if file_id not in raw_file_bytes_by_file_id:
                raise ValueError(f"raw bytes are required for preserved file id: {file_id}")

    rows: list[BasenotesProjectionRow] = []
    bindings: list[BasenotesProjectionBinding] = []
    residuals: list[str] = []

    for source_slice in packet.source_slices:
        raw_ref = BasenotesProjectionRawRef(
            packet_id=packet.packet_id,
            slice_id=source_slice.slice_id,
        )
        for file_id in source_slice.preserved_file_ids:
            preserved_file = preserved_files[file_id]
            body = raw_file_bytes_by_file_id[file_id]
            if not _looks_like_basenotes_body(preserved_file, body):
                continue
            projected = _project_basenotes_html(
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
        residuals.append("basenotes_review_cards_absent")
    if not any(row.row_kind == "fragrance_statement_current_window" for row in rows):
        residuals.append("basenotes_statement_rows_absent")
    if not any(row.row_kind == "fragrance_product_snapshot" for row in rows):
        residuals.append("basenotes_product_snapshot_absent")

    return BasenotesProjectionPacket(
        packet_id=packet.packet_id,
        rows=rows,
        binding_map=bindings,
        loss_ledger=BasenotesProjectionLossLedger(
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


def build_basenotes_projection_from_packet_directory(
    *,
    packet_or_manifest_path: Path,
) -> BasenotesProjectionPacket:
    packet, raw_file_bytes_by_file_id = _read_packet_directory(packet_or_manifest_path)
    return build_basenotes_projection(
        packet=packet,
        raw_file_bytes_by_file_id=raw_file_bytes_by_file_id,
    )


def write_basenotes_projection(
    *,
    packet_or_manifest_path: Path,
    output_path: Path,
    overwrite: bool = False,
) -> BasenotesProjectionPacket:
    projection = build_basenotes_projection_from_packet_directory(
        packet_or_manifest_path=packet_or_manifest_path,
    )
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"output already exists: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_projection_json_text(projection), encoding="utf-8")
    return projection


def project_basenotes_into_lake(
    *,
    data_root: "DataLakeRoot",
    packet_id: str,
    record_id: str | None = None,
) -> tuple[BasenotesProjectionPacket, Path]:
    """Project a committed Basenotes raw packet into an append-only derived record."""
    loaded = data_root.load_raw_packet(packet_id)
    packet = SourceCapturePacket.model_validate(loaded.manifest)
    projection = build_basenotes_projection(
        packet=packet,
        raw_file_bytes_by_file_id=loaded.bodies,
    )
    record = record_id if record_id is not None else generate_ulid()
    derived_path = data_root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=PROJECTION_BASENOTES_LANE,
        record_id=f"{record}.json",
        data=_projection_json_text(projection).encode("utf-8"),
    )
    return projection, derived_path


class _ProjectedBasenotesHtml(StrictModel):
    rows: list[BasenotesProjectionRow] = Field(default_factory=list)
    bindings: list[BasenotesProjectionBinding] = Field(default_factory=list)
    residuals: list[str] = Field(default_factory=list)


def _project_basenotes_html(
    body: bytes,
    *,
    source_slice: SourceCaptureSlice,
    raw_ref: BasenotesProjectionRawRef,
    raw_anchor: BasenotesProjectionRawAnchor,
) -> _ProjectedBasenotesHtml:
    text = body.decode("utf-8", errors="replace")
    product_jsonld = _product_jsonld(text)
    product = _product_context(text, product_jsonld)
    rows: list[BasenotesProjectionRow] = []
    bindings: list[BasenotesProjectionBinding] = []
    residuals: list[str] = []
    source_object_site_id = product.get("source_object_site_id")
    source_object_name = product.get("source_object_name")
    brand_or_house = product.get("brand_or_house")
    product_slug = product.get("product_slug")

    rows.append(
        BasenotesProjectionRow(
            row_id=f"{source_slice.slice_id}:basenotes:product_snapshot",
            row_kind="fragrance_product_snapshot",
            raw_ref=raw_ref,
            raw_anchor=_with_anchor(raw_anchor, "text_pattern", "canonical|application/ld+json|title"),
            source_object_site_id=source_object_site_id,
            source_object_name=source_object_name,
            brand_or_house=brand_or_house,
            source_visible_fields=product,
            residuals=_product_residuals(product),
        )
    )

    review_rows, review_bindings = _jsonld_review_card_rows(
        product_jsonld,
        raw_ref=raw_ref,
        raw_anchor=raw_anchor,
        source_slice=source_slice,
        source_object_site_id=source_object_site_id,
        source_object_name=source_object_name,
        brand_or_house=brand_or_house,
    )
    rows.extend(review_rows)
    bindings.extend(review_bindings)

    aggregate_row = _aggregate_rating_row(
        text,
        product_jsonld=product_jsonld,
        captured_review_count=len(review_rows),
        raw_ref=raw_ref,
        raw_anchor=raw_anchor,
        source_slice=source_slice,
        source_object_site_id=source_object_site_id,
        source_object_name=source_object_name,
        brand_or_house=brand_or_house,
    )
    if aggregate_row is None:
        residuals.append("basenotes_aggregate_rating_absent")
    else:
        rows.append(aggregate_row)

    archive_gate_rows = _archive_gate_rows(
        text,
        product_jsonld=product_jsonld,
        product_slug=product_slug,
        captured_review_count=len(review_rows),
        raw_ref=raw_ref,
        raw_anchor=raw_anchor,
        source_slice=source_slice,
        source_object_site_id=source_object_site_id,
        source_object_name=source_object_name,
        brand_or_house=brand_or_house,
    )
    rows.extend(archive_gate_rows)
    if any(row.source_visible_fields.get("corpus_kind") == "reviews" for row in archive_gate_rows):
        residuals.append("full_review_corpus_not_captured")

    residuals.extend(
        [
            "linked_media_assets_not_preserved_by_cloakbrowser_snapshot",
            "review_attached_photo_proof_not_present",
        ]
    )
    residuals.extend(_non_text_fragrance_scope_residuals(text))

    return _ProjectedBasenotesHtml(
        rows=rows,
        bindings=bindings,
        residuals=_dedupe_preserve_order(residuals),
    )


def _product_jsonld(text: str) -> dict[str, Any]:
    """Parse the schema.org Product JSON-LD block (the one carrying the review array).

    Basenotes embeds the product + its in-page review subset as a single
    ``<script type="application/ld+json">`` Product object. Returns ``{}`` when no
    parseable Product block is present (caller treats that as reviews absent)."""
    first_product: dict[str, Any] | None = None
    for block in re.finditer(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        text,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        raw = block.group(1).strip()
        try:
            parsed = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            continue
        for candidate in _iter_jsonld_objects(parsed):
            if not _jsonld_type_includes(candidate.get("@type"), "Product"):
                continue
            if first_product is None:
                first_product = candidate
            if _has_jsonld_reviews(candidate.get("review")):
                return candidate
    return first_product or {}


def _iter_jsonld_objects(parsed: Any):
    if isinstance(parsed, dict):
        graph = parsed.get("@graph")
        if isinstance(graph, list):
            for item in graph:
                if isinstance(item, dict):
                    yield item
        yield parsed
    elif isinstance(parsed, list):
        for item in parsed:
            if isinstance(item, dict):
                yield item


def _jsonld_type_includes(value: Any, expected: str) -> bool:
    if isinstance(value, str):
        return value == expected
    if isinstance(value, list):
        return any(item == expected for item in value)
    return False


def _has_jsonld_reviews(value: Any) -> bool:
    if not isinstance(value, list):
        return False
    return any(
        isinstance(item, dict) and _jsonld_type_includes(item.get("@type"), "Review")
        for item in value
    )


def _product_context(text: str, product_jsonld: Mapping[str, Any]) -> dict[str, Any | None]:
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

    product_name = _jsonld_str(product_jsonld.get("name"))
    brand_or_house = _jsonld_str(_brand_name(product_jsonld.get("brand")))
    image = _jsonld_str(product_jsonld.get("image"))

    slug = _product_slug(canonical_url) or _product_slug(
        _first_match(
            text,
            r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']',
            flags=re.IGNORECASE,
        )
    )
    site_id = _site_id_from_slug(slug)

    if product_name is None and title:
        match = re.search(r"(.+?)\s+by\s+(.+?)(?:\s*[-–—]|$)", title, flags=re.IGNORECASE)
        if match:
            product_name = _text(match.group(1))
            if brand_or_house is None:
                brand_or_house = _text(match.group(2))

    return {
        "source_platform": "basenotes",
        "source_object_type": "fragrance_product",
        "source_object_site_id": site_id,
        "source_object_name": product_name,
        "brand_or_house": brand_or_house,
        "canonical_url": canonical_url,
        "product_slug": slug,
        "product_image": image,
        "page_title": title,
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
    if re.search(r"\bphotos?\b", text, flags=re.IGNORECASE):
        residuals.append("fragrance_photo_surface_present_but_not_projected")
    return residuals


def _jsonld_review_card_rows(
    product_jsonld: Mapping[str, Any],
    *,
    raw_ref: BasenotesProjectionRawRef,
    raw_anchor: BasenotesProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
    source_object_site_id: str | None,
    source_object_name: str | None,
    brand_or_house: str | None,
) -> tuple[list[BasenotesProjectionRow], list[BasenotesProjectionBinding]]:
    reviews = product_jsonld.get("review")
    if not isinstance(reviews, list):
        return [], []
    rows: list[BasenotesProjectionRow] = []
    bindings: list[BasenotesProjectionBinding] = []
    tab_id = "reviews"
    for index, review in enumerate(reviews, start=1):
        if not isinstance(review, dict) or review.get("@type") != "Review":
            continue
        item_id = f"jsonld_review_{index:03d}"
        row_id = f"{source_slice.slice_id}:basenotes:review:{tab_id}:{item_id}"
        # JSON-LD reviews are addressed by their position in the in-page Product.review[]
        # array (no per-card DOM id is exposed), so the anchor names the ld+json array slot.
        row_anchor = _with_anchor(
            raw_anchor,
            "text_pattern",
            f'application/ld+json::Product.review[{index - 1}]',
        )
        row = BasenotesProjectionRow(
            row_id=row_id,
            row_kind="fragrance_review_card_current_window",
            raw_ref=raw_ref,
            raw_anchor=row_anchor,
            source_object_site_id=source_object_site_id,
            source_object_name=source_object_name,
            brand_or_house=brand_or_house,
            tab_id=tab_id,
            source_order=index,
            comment_id=item_id,
            source_visible_fields=_review_row_fields(review, item_id=item_id, tab_id=tab_id),
            residuals=_review_row_residuals(review),
        )
        rows.append(row)
        bindings.append(
            BasenotesProjectionBinding(
                binding_type="review_metadata_to_review_text",
                row_id=row_id,
                raw_ref=raw_ref,
                raw_anchor=row_anchor,
            )
        )
    return rows, bindings


def _review_row_fields(
    review: Mapping[str, Any],
    *,
    item_id: str,
    tab_id: str,
) -> dict[str, Any | None]:
    text_value = _text(_jsonld_str(review.get("reviewBody")))
    rating = _review_rating_value(review.get("reviewRating"))
    return {
        "review_id": item_id,
        "tab_id": tab_id,
        "tab_label": "Reviews",
        "author_display_name": _text(_jsonld_str(review.get("author")))
        or _text(_jsonld_str(_author_name(review.get("author")))),
        "author_profile_url": None,
        "date_published": _jsonld_str(review.get("datePublished")),
        "date_display_text": None,
        "review_text": text_value,
        "review_text_length_chars": len(text_value) if text_value is not None else None,
        "rating": rating,
        "helpful_count": None,
        "source_item_url": None,
    }


def _review_row_residuals(review: Mapping[str, Any]) -> list[str]:
    residuals = []
    if _text(_jsonld_str(review.get("author"))) is None and _author_name(review.get("author")) is None:
        residuals.append("author_display_name_absent")
    if review.get("datePublished") in {None, ""}:
        residuals.append("date_published_absent")
    if _text(_jsonld_str(review.get("reviewBody"))) is None:
        residuals.append("review_text_absent")
    return residuals


def _aggregate_rating_row(
    text: str,
    *,
    product_jsonld: Mapping[str, Any],
    captured_review_count: int,
    raw_ref: BasenotesProjectionRawRef,
    raw_anchor: BasenotesProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
    source_object_site_id: str | None,
    source_object_name: str | None,
    brand_or_house: str | None,
) -> BasenotesProjectionRow | None:
    declared_reviews = _declared_review_count(text)
    aggregate = product_jsonld.get("aggregateRating")
    rating_value = None
    rating_count = None
    if isinstance(aggregate, dict):
        rating_value = _to_float(_jsonld_str(aggregate.get("ratingValue")))
        rating_count = _parse_count(_jsonld_str(aggregate.get("reviewCount"))) or _parse_count(
            _jsonld_str(aggregate.get("ratingCount"))
        )
    sentiment_counts = _sentiment_counts(text)
    fields = {
        "rating_value": rating_value,
        "rating_count": rating_count,
        "declared_reviews": declared_reviews,
        "declared_statements": None,
        "captured_review_cards": captured_review_count,
        "positive_review_count": sentiment_counts.get("positive"),
        "neutral_review_count": sentiment_counts.get("neutral"),
        "negative_review_count": sentiment_counts.get("negative"),
    }
    if all(value is None for value in fields.values()):
        return None
    return BasenotesProjectionRow(
        row_id=f"{source_slice.slice_id}:basenotes:aggregate_rating",
        row_kind="fragrance_aggregate_rating",
        raw_ref=raw_ref,
        raw_anchor=_with_anchor(raw_anchor, "text_pattern", "Reviews|Positive|Neutral|Negative"),
        source_object_site_id=source_object_site_id,
        source_object_name=source_object_name,
        brand_or_house=brand_or_house,
        source_visible_fields=fields,
    )


def _archive_gate_rows(
    text: str,
    *,
    product_jsonld: Mapping[str, Any],
    product_slug: str | None,
    captured_review_count: int,
    raw_ref: BasenotesProjectionRawRef,
    raw_anchor: BasenotesProjectionRawAnchor,
    source_slice: SourceCaptureSlice,
    source_object_site_id: str | None,
    source_object_name: str | None,
    brand_or_house: str | None,
) -> list[BasenotesProjectionRow]:
    declared_reviews = _declared_review_count(text)
    reviews = product_jsonld.get("review")
    has_review_array = isinstance(reviews, list) and any(
        isinstance(item, dict) and item.get("@type") == "Review" for item in reviews
    )
    # The in-page JSON-LD carries only a SUBSET of the declared "N Reviews". Emit the gate
    # whenever the page declares a review corpus or exposes the reviews sub-URL, so the
    # full-corpus residual is honestly recorded. Basenotes has NO AJAX endpoint -- the
    # corpus continuation is the /reviews/ sub-URL plus its sentiment tabs.
    reviews_subpath = f"/fragrances/{product_slug}/reviews/" if product_slug else None
    show_all_link = _first_match(
        text,
        r'<a[^>]+class=["\'][^"\']*showall[^"\']*["\'][^>]+href=["\']([^"\']*/reviews/)["\']',
        flags=re.IGNORECASE,
    )
    if reviews_subpath is None and show_all_link is None and declared_reviews is None and not has_review_array:
        return []
    endpoint = reviews_subpath or show_all_link or "/reviews/"
    sentiment_endpoints = (
        {tab: f"{reviews_subpath}{tab}/" for tab in _SENTIMENT_TABS}
        if reviews_subpath is not None
        else {tab: f"{endpoint.rstrip('/')}/{tab}/" for tab in _SENTIMENT_TABS}
    )
    return [
        BasenotesProjectionRow(
            row_id=f"{source_slice.slice_id}:basenotes:archive_gate:reviews",
            row_kind="fragrance_review_archive_gate",
            raw_ref=raw_ref,
            raw_anchor=_with_anchor(raw_anchor, "text_pattern", endpoint),
            source_object_site_id=source_object_site_id,
            source_object_name=source_object_name,
            brand_or_house=brand_or_house,
            source_visible_fields={
                "corpus_kind": "reviews",
                "endpoint_path": endpoint,
                "sentiment_tab_endpoints": sentiment_endpoints,
                "product_slug": product_slug,
                "declared_review_count": declared_reviews,
                "captured_review_subset": captured_review_count,
                "pagination_posture": "review_suburl_observed_but_not_followed_by_projection",
            },
            residuals=["full_review_corpus_not_captured"],
        )
    ]


def _looks_like_basenotes_body(preserved_file: PreservedFile, body: bytes) -> bool:
    path = preserved_file.relative_packet_path.lower()
    if "snapshot_metadata" in path or "visible_text" in path or "screenshot" in path:
        return False
    sample = body[:300_000].decode("utf-8", errors="ignore").lower()
    return (
        "basenotes.com/fragrances/" in sample
        or 'application/ld+json' in sample
        and '"@type": "product"' in sample
        or "fragreview" in sample
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


def _raw_anchor(preserved_file: PreservedFile) -> BasenotesProjectionRawAnchor:
    return BasenotesProjectionRawAnchor(
        file_id=preserved_file.file_id,
        relative_packet_path=preserved_file.relative_packet_path,
        sha256=preserved_file.sha256,
        hash_basis=preserved_file.hash_basis,
    )


def _with_anchor(
    raw_anchor: BasenotesProjectionRawAnchor,
    anchor_kind: Literal["html_selector", "text_pattern"],
    anchor_value: str,
) -> BasenotesProjectionRawAnchor:
    return BasenotesProjectionRawAnchor(
        file_id=raw_anchor.file_id,
        relative_packet_path=raw_anchor.relative_packet_path,
        sha256=raw_anchor.sha256,
        hash_basis=raw_anchor.hash_basis,
        anchor_kind=anchor_kind,
        anchor_value=anchor_value,
    )


def _brand_name(brand: Any) -> Any:
    if isinstance(brand, dict):
        return brand.get("name")
    return brand


def _author_name(author: Any) -> Any:
    if isinstance(author, dict):
        return author.get("name")
    return author


def _review_rating_value(rating: Any) -> float | None:
    if isinstance(rating, dict):
        return _to_float(_jsonld_str(rating.get("ratingValue")))
    return _to_float(_jsonld_str(rating))


def _declared_review_count(text: str) -> int | None:
    # The page renders the declared corpus size as "N Reviews" (e.g. the "Show all 18
    # Reviews" link and the sentiment summary header), distinct from the in-page subset.
    return _parse_count(
        _first_match(text, r"Show all\s+([\d,]+)\s+Reviews?", flags=re.IGNORECASE)
    ) or _parse_count(_first_match(text, r"([\d,]+)\s+Reviews?\b", flags=re.IGNORECASE))


def _sentiment_counts(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for tab in _SENTIMENT_TABS:
        value = _first_match(
            text,
            rf"([\d,]+)\s+{tab}\s*\(",
            flags=re.IGNORECASE,
        )
        parsed = _parse_count(value)
        if parsed is not None:
            counts[tab] = parsed
    return counts


def _product_slug(url: str | None) -> str | None:
    if not url:
        return None
    match = re.search(r"/fragrances/([^/?#]+)", url, flags=re.IGNORECASE)
    if match is None:
        return None
    return html.unescape(match.group(1)).strip() or None


def _site_id_from_slug(slug: str | None) -> str | None:
    if not slug:
        return None
    match = re.search(r"\.(\d+)$", slug)
    return match.group(1) if match else None


def _jsonld_str(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, (int, float)):
        return str(value)
    return None


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
    return normalized or None


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
    try:
        return int(float(normalized) * multiplier)
    except ValueError:
        return None


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


def _projection_json_text(projection: BasenotesProjectionPacket) -> str:
    return f"{json.dumps(projection.model_dump(mode='json'), indent=2, sort_keys=True)}\n"


__all__ = [
    "BASENOTES_PROJECTION_CERTIFICATION",
    "BASENOTES_PROJECTION_METHOD",
    "BASENOTES_PROJECTION_VERSION",
    "PROJECTION_BASENOTES_LANE",
    "BasenotesProjectionBinding",
    "BasenotesProjectionLossLedger",
    "BasenotesProjectionPacket",
    "BasenotesProjectionRawAnchor",
    "BasenotesProjectionRawRef",
    "BasenotesProjectionRow",
    "build_basenotes_projection",
    "build_basenotes_projection_from_packet_directory",
    "project_basenotes_into_lake",
    "write_basenotes_projection",
]
