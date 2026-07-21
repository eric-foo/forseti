"""Strict parsing of Sephora's retailer-owned brand-grid PageJSON."""

from __future__ import annotations

import json
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any


class SephoraBrandGridStateError(ValueError):
    """The preserved Sephora brand-grid PageJSON is present but malformed."""


@dataclass(frozen=True)
class SephoraBrandGridState:
    brand_id: str | None
    brand_name: str | None
    short_name: str | None
    result_id: str | None
    target_url: str | None
    canonical_url: str | None
    page_size: int | None
    total_products: int | None
    products: tuple[dict[str, Any], ...]
    explicit_currency_codes: tuple[str, ...]
    currency_evidence_paths: tuple[str, ...]


def load_sephora_brand_grid_state(rendered_dom: str) -> SephoraBrandGridState | None:
    parser = _LinkStoreParser()
    try:
        parser.feed(rendered_dom or "")
        parser.close()
    except Exception as exc:
        raise SephoraBrandGridStateError(
            f"Sephora linkStore script parsing failed: {type(exc).__name__}"
        ) from exc
    if not parser.documents:
        return None
    if len(parser.documents) != 1:
        raise SephoraBrandGridStateError(
            f"expected exactly one Sephora linkStore script; found {len(parser.documents)}"
        )
    try:
        payload = json.loads(parser.documents[0])
    except (json.JSONDecodeError, TypeError) as exc:
        raise SephoraBrandGridStateError("Sephora linkStore PageJSON is malformed") from exc
    if not isinstance(payload, dict):
        raise SephoraBrandGridStateError("Sephora linkStore PageJSON is not an object")
    page = payload.get("page")
    nth_brand = page.get("nthBrand") if isinstance(page, dict) else None
    if not isinstance(nth_brand, dict):
        return None
    raw_products = nth_brand.get("products")
    if not isinstance(raw_products, list):
        raise SephoraBrandGridStateError(
            "Sephora linkStore page.nthBrand.products is not an array"
        )
    products: list[dict[str, Any]] = []
    for product in raw_products:
        if not isinstance(product, dict):
            raise SephoraBrandGridStateError(
                "Sephora linkStore page.nthBrand.products contains a non-object row"
            )
        products.append(product)
    currency_codes, currency_paths = _explicit_currency_evidence(
        nth_brand=nth_brand, products=products
    )
    return SephoraBrandGridState(
        brand_id=_text(nth_brand.get("brandId")),
        brand_name=_text(nth_brand.get("displayName")),
        short_name=_text(nth_brand.get("shortName")),
        result_id=_text(nth_brand.get("resultId")),
        target_url=_text(nth_brand.get("targetUrl")),
        canonical_url=_text(nth_brand.get("seoCanonicalUrl")),
        page_size=_integer(nth_brand.get("pageSize")),
        total_products=_integer(nth_brand.get("totalProducts")),
        products=tuple(products),
        explicit_currency_codes=tuple(currency_codes),
        currency_evidence_paths=tuple(currency_paths),
    )


class _LinkStoreParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self._in_link_store = False
        self._parts: list[str] = []
        self.documents: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag.lower() != "script":
            return
        attributes = {key.lower(): value or "" for key, value in attrs}
        if attributes.get("id") == "linkStore":
            self._in_link_store = True
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._in_link_store:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._in_link_store:
            self.documents.append("".join(self._parts))
            self._parts = []
            self._in_link_store = False


def _explicit_currency_evidence(
    *, nth_brand: dict[str, Any], products: list[dict[str, Any]]
) -> tuple[list[str], list[str]]:
    codes: list[str] = []
    paths: list[str] = []
    for key in ("currency", "currencyCode", "priceCurrency"):
        value = _currency_code(nth_brand.get(key))
        if value is not None:
            codes.append(value)
            paths.append(f"/page/nthBrand/{key}")
    for index, product in enumerate(products):
        current_sku = product.get("currentSku")
        if not isinstance(current_sku, dict):
            continue
        for key in ("currency", "currencyCode", "priceCurrency"):
            value = _currency_code(current_sku.get(key))
            if value is not None:
                codes.append(value)
                paths.append(f"/page/nthBrand/products/{index}/currentSku/{key}")
    return list(dict.fromkeys(codes)), list(dict.fromkeys(paths))


def _currency_code(value: object) -> str | None:
    text = _text(value)
    if text is None:
        return None
    normalized = text.upper()
    return normalized if len(normalized) == 3 and normalized.isalpha() else None


def _integer(value: object) -> int | None:
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return value
    return None


def _text(value: object) -> str | None:
    if isinstance(value, (str, int, float)) and not isinstance(value, bool):
        text = str(value).strip()
        return text or None
    return None


__all__ = [
    "SephoraBrandGridState",
    "SephoraBrandGridStateError",
    "load_sephora_brand_grid_state",
]
