"""Compact, replayable REVOLVE PDP content extraction."""

from __future__ import annotations

import hashlib
import json
import re
from html.parser import HTMLParser
from typing import Any, Iterator, Literal
from urllib.parse import urlparse

from pydantic import Field, model_validator

from schemas.case_models import StrictModel


REVOLVE_PDP_CONTENT_PROFILE = "revolve_pdp_aggregate"
REVOLVE_PDP_CONTENT_RECORD_KIND = "retail_pdp_revolve_aggregate_content"
REVOLVE_PDP_CONTENT_SCHEMA_VERSION = "retail_pdp_revolve_aggregate_content_v1"
REVOLVE_PDP_PARSER_VERSION = "retail_pdp_revolve_aggregate_parser_v1"
_REVOLVE_HOSTS = frozenset({"revolve.com", "www.revolve.com"})
_STYLE_PATH_RE = re.compile(
    r"/dp/(?P<style_id>[A-Z0-9]{2,12}-[A-Z]{1,4}\d+)/?$",
    re.IGNORECASE,
)
_YOTPO_STORE_RE = re.compile(
    r"cdn-widgetsrepository\.yotpo\.com/v1/loader/"
    r"(?P<store_id>[A-Za-z0-9_-]{20,80})",
    re.IGNORECASE,
)
_MANUFACTURER_STYLE_RE = re.compile(
    r"Manufacturer Style No\.\s+(?P<value>[A-Za-z0-9._/-]+)",
    re.IGNORECASE,
)
_SIZE_RE = re.compile(
    r"(?<![A-Za-z0-9])\d+(?:\.\d+)?\s*(?:fl\.?\s*oz|oz|ml|g)(?![A-Za-z0-9])",
    re.IGNORECASE,
)


class RevolvePdpAggregateContentRecord(StrictModel):
    record_kind: Literal["retail_pdp_revolve_aggregate_content"] = (
        REVOLVE_PDP_CONTENT_RECORD_KIND
    )
    schema_version: Literal["retail_pdp_revolve_aggregate_content_v1"] = (
        REVOLVE_PDP_CONTENT_SCHEMA_VERSION
    )
    parser_version: Literal["retail_pdp_revolve_aggregate_parser_v1"] = (
        REVOLVE_PDP_PARSER_VERSION
    )
    capture_profile: Literal["revolve_pdp_aggregate"] = REVOLVE_PDP_CONTENT_PROFILE
    source_url: str
    style_id: str
    product: dict[str, Any]
    offer: dict[str, Any]
    variants: list[dict[str, Any]] = Field(default_factory=list)
    media_urls: list[str] = Field(default_factory=list)
    product_details: dict[str, Any | None] = Field(default_factory=dict)
    review_substrate: dict[str, Any | None] = Field(default_factory=dict)
    input_hashes: dict[str, str]
    residuals: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_identity_and_market(self) -> "RevolvePdpAggregateContentRecord":
        if str(self.product.get("sku", "")).upper() != self.style_id:
            raise ValueError("REVOLVE product SKU does not match source URL style id")
        if self.offer.get("priceCurrency") != "USD":
            raise ValueError("REVOLVE PDP offer must bind exact USD")
        if not str(self.offer.get("price", "")).strip():
            raise ValueError("REVOLVE PDP offer must retain a nonempty price")
        if self.review_substrate.get("provider") != "yotpo":
            raise ValueError("REVOLVE PDP must retain its observed Yotpo substrate")
        if self.review_substrate.get("product_id") != self.style_id:
            raise ValueError("REVOLVE Yotpo product id does not match source URL")
        return self


def build_revolve_pdp_aggregate_content_record(
    *,
    rendered_dom: bytes,
    visible_text: bytes,
    source_url: str,
) -> RevolvePdpAggregateContentRecord:
    if not isinstance(rendered_dom, bytes) or not isinstance(visible_text, bytes):
        raise TypeError("rendered_dom and visible_text must be bytes")
    style_id = extract_revolve_style_id_from_url(source_url)
    if style_id is None:
        raise ValueError(
            "REVOLVE aggregate content requires an exact revolve.com /dp/<style-id> URL"
        )
    dom = rendered_dom.decode("utf-8", errors="replace")
    text = " ".join(visible_text.decode("utf-8", errors="replace").split())
    products = [
        value
        for value in _iter_json_ld_objects(dom)
        if value.get("@type") == "Product"
        and str(value.get("sku", "")).upper() == style_id
    ]
    if len(products) != 1:
        raise ValueError(
            "REVOLVE aggregate content requires exactly one target-bound Product JSON-LD"
        )
    product = products[0]
    offers = product.get("offers")
    offer_values = offers if isinstance(offers, list) else [offers]
    usd_offers = [
        value
        for value in offer_values
        if isinstance(value, dict)
        and value.get("@type") == "Offer"
        and value.get("priceCurrency") == "USD"
        and str(value.get("price", "")).strip()
    ]
    if len(usd_offers) != 1:
        raise ValueError(
            "REVOLVE aggregate content requires exactly one target-bound USD Offer"
        )
    parser = _RevolvePdpParser(style_id=style_id)
    try:
        parser.feed(dom)
        parser.close()
    except Exception as exc:
        raise ValueError(
            f"REVOLVE PDP rendered DOM is malformed: {type(exc).__name__}"
        ) from exc
    store_ids = list(
        dict.fromkeys(match.group("store_id") for match in _YOTPO_STORE_RE.finditer(dom))
    )
    product_ids = list(dict.fromkeys(parser.yotpo_product_ids))
    currencies = list(dict.fromkeys(parser.yotpo_currencies))
    if len(store_ids) != 1 or product_ids != [style_id] or currencies != ["USD"]:
        raise ValueError(
            "REVOLVE Yotpo route is ambiguous or not bound to the requested style/USD"
        )
    aggregate = product.get("aggregateRating")
    if not isinstance(aggregate, dict):
        aggregate = {}
    review_count = _int_or_none(aggregate.get("reviewCount"))
    rating_value = _string_or_none(aggregate.get("ratingValue"))
    residuals: list[str] = []
    if review_count is None:
        residuals.append("revolve_pdp_review_count_not_observed")
    if rating_value is None:
        residuals.append("revolve_pdp_rating_value_not_observed")
    if not parser.variant_names:
        residuals.append("revolve_pdp_variants_not_exposed")
    if not parser.media_urls:
        residuals.append("revolve_pdp_media_not_observed")
    manufacturer = _MANUFACTURER_STYLE_RE.search(text)
    sizes = list(dict.fromkeys(match.group(0) for match in _SIZE_RE.finditer(text)))
    return RevolvePdpAggregateContentRecord(
        source_url=source_url,
        style_id=style_id,
        product=_json_safe_copy(product),
        offer=_json_safe_copy(usd_offers[0]),
        variants=[
            {"name": name, "selected": name == parser.selected_variant}
            for name in parser.variant_names
        ],
        media_urls=parser.media_urls,
        product_details={
            "brand": _brand_name(product.get("brand")),
            "name": _string_or_none(product.get("name")),
            "description": parser.yotpo_description
            or _string_or_none(product.get("description")),
            "manufacturer_style_no": (
                manufacturer.group("value") if manufacturer else None
            ),
            "size_mentions": sizes,
        },
        review_substrate={
            "provider": "yotpo",
            "store_id": store_ids[0],
            "product_id": style_id,
            "instance_ids": parser.yotpo_instance_ids,
            "rating_value": rating_value,
            "review_count": review_count,
            "available_sort_labels": parser.sort_labels,
            "source_native_depth_orders": [
                label
                for label in ("Most relevant", "Most recent")
                if label in parser.sort_labels
            ],
            "qna_exposed": parser.qna_exposed,
        },
        input_hashes={
            "rendered_dom_sha256": hashlib.sha256(rendered_dom).hexdigest(),
            "visible_text_sha256": hashlib.sha256(visible_text).hexdigest(),
        },
        residuals=residuals,
    )


def extract_revolve_style_id_from_url(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or (parsed.hostname or "").lower() not in _REVOLVE_HOSTS:
        return None
    match = _STYLE_PATH_RE.search(parsed.path)
    return match.group("style_id").upper() if match else None


class _RevolvePdpParser(HTMLParser):
    def __init__(self, *, style_id: str) -> None:
        super().__init__(convert_charrefs=True)
        self.style_id = style_id
        self.yotpo_product_ids: list[str] = []
        self.yotpo_currencies: list[str] = []
        self.yotpo_instance_ids: list[str] = []
        self.yotpo_description: str | None = None
        self.variant_names: list[str] = []
        self.selected_variant: str | None = None
        self.media_urls: list[str] = []
        self.sort_labels: list[str] = []
        self.qna_exposed = False

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = {key.lower(): value or "" for key, value in attrs}
        product_id = attributes.get("data-yotpo-product-id", "").upper()
        if product_id:
            self.yotpo_product_ids.append(product_id)
            currency = attributes.get("data-yotpo-currency", "").upper()
            if currency:
                self.yotpo_currencies.append(currency)
            instance = attributes.get("data-yotpo-instance-id", "")
            if instance:
                self.yotpo_instance_ids.append(instance)
            description = attributes.get("data-yotpo-description", "").strip()
            if description:
                self.yotpo_description = description
        if tag.lower() == "input" and attributes.get("type") == "radio":
            label = attributes.get("aria-label", "").removeprefix("color:").strip()
            if label:
                self.variant_names.append(label)
                if "checked" in attributes:
                    self.selected_variant = label
        if tag.lower() == "img":
            for key in ("src", "data-src", "data-lazy-src"):
                value = attributes.get(key, "")
                if (
                    value
                    and "revolveassets.com" in value
                    and self.style_id.lower() in value.lower()
                ):
                    self.media_urls.append(value)
        aria = attributes.get("aria-label", "")
        if aria in {
            "Most relevant",
            "Most recent",
            "Highest rating",
            "Lowest rating",
        }:
            self.sort_labels.append(aria)
        if "Questions & Answers" in aria:
            self.qna_exposed = True

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if text in {
            "Most relevant",
            "Most recent",
            "Highest rating",
            "Lowest rating",
        }:
            self.sort_labels.append(text)
        if "Questions & Answers" in text:
            self.qna_exposed = True

    def close(self) -> None:
        super().close()
        self.yotpo_product_ids = list(dict.fromkeys(self.yotpo_product_ids))
        self.yotpo_currencies = list(dict.fromkeys(self.yotpo_currencies))
        self.yotpo_instance_ids = list(dict.fromkeys(self.yotpo_instance_ids))
        self.variant_names = list(dict.fromkeys(self.variant_names))
        self.media_urls = list(dict.fromkeys(self.media_urls))
        self.sort_labels = list(dict.fromkeys(self.sort_labels))


class _JsonLdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.documents: list[str] = []
        self._active = False
        self._parts: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        attributes = {key.lower(): (value or "").lower() for key, value in attrs}
        if tag.lower() == "script" and attributes.get("type") == "application/ld+json":
            self._active = True
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._active:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._active:
            self.documents.append("".join(self._parts))
            self._active = False
            self._parts = []


def _iter_json_ld_objects(dom: str) -> Iterator[dict[str, Any]]:
    parser = _JsonLdParser()
    try:
        parser.feed(dom)
        parser.close()
    except Exception:
        return
    for document in parser.documents:
        try:
            value = json.loads(document)
        except (json.JSONDecodeError, TypeError):
            continue
        yield from _walk(value)


def _walk(value: Any) -> Iterator[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def _brand_name(value: object) -> str | None:
    if isinstance(value, dict):
        return _string_or_none(value.get("name"))
    return _string_or_none(value)


# helper-delta: unlike harness_utils.string_or_none, retain numeric JSON-LD ratings.
def _string_or_none(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


# helper-delta: unlike harness_utils.int_or_none, reject negative and float counts.
def _int_or_none(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        parsed = int(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return None
    return parsed if parsed >= 0 else None


def _json_safe_copy(value: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(value, ensure_ascii=False))


__all__ = [
    "REVOLVE_PDP_CONTENT_PROFILE",
    "REVOLVE_PDP_CONTENT_RECORD_KIND",
    "REVOLVE_PDP_CONTENT_SCHEMA_VERSION",
    "REVOLVE_PDP_PARSER_VERSION",
    "RevolvePdpAggregateContentRecord",
    "build_revolve_pdp_aggregate_content_record",
    "extract_revolve_style_id_from_url",
]
