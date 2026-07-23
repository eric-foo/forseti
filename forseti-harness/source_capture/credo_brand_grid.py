"""Exact Credo collection-grid parsing for a single public Shopify response."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import urlparse


CREDO_GRID_PARSER_VERSION = "credo_brand_grid_v1"
_PRODUCT_PATH = re.compile(r"^/products/(?P<handle>[a-z0-9][a-z0-9-]*)/?$")
_VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


@dataclass(frozen=True)
class CredoBrandGridCard:
    grid_position: int
    product_id: str
    handle: str
    product_url: str
    vendor: str


@dataclass(frozen=True)
class CredoBrandGridState:
    source_url: str
    collection_id: str
    collection_title: str
    country_code: str
    currency_code: str
    cards: tuple[CredoBrandGridCard, ...]
    pagination_next_url: str | None
    parser_version: str = CREDO_GRID_PARSER_VERSION


def canonical_credo_collection_url(value: str) -> str | None:
    parsed = urlparse(value)
    match = re.fullmatch(r"/collections/([a-z0-9][a-z0-9-]*)/?", parsed.path)
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower() != "credobeauty.com"
        or match is None
        or parsed.query
        or parsed.fragment
    ):
        return None
    return f"https://credobeauty.com/collections/{match.group(1)}"


def load_credo_brand_grid_state(
    html: str,
    *,
    requested_url: str,
) -> CredoBrandGridState:
    """Reconcile Credo's visible grid with its first-party Shopify page state."""
    source_url = canonical_credo_collection_url(requested_url)
    if source_url is None:
        raise ValueError("Credo grid requires an exact HTTPS /collections/<slug> URL")
    init_data = _shopify_init_data(html)
    shop = init_data.get("shop")
    page = init_data.get("page")
    if not isinstance(page, dict):
        page = _shopify_page_state(html)
    products = init_data.get("products")
    if not isinstance(shop, dict) or not isinstance(page, dict) or not isinstance(products, list):
        raise ValueError("Credo grid lacks one Shopify shop/page/products conjunction")
    if (
        shop.get("countryCode") != "US"
        or shop.get("paymentSettings", {}).get("currencyCode") != "USD"
        or shop.get("storefrontUrl") != "https://credobeauty.com"
    ):
        raise ValueError("Credo grid Shopify state is not exact US/USD storefront state")
    if page.get("pageType") != "collection" or page.get(
        "resourceType", "collection"
    ) != "collection":
        raise ValueError("Credo grid Shopify page state is not a collection")
    collection_id = str(page.get("resourceId") or "")
    if not collection_id:
        raise ValueError("Credo grid Shopify page state lacks collection identity")

    state_products: list[tuple[str, str]] = []
    for index, product in enumerate(products):
        if not isinstance(product, dict):
            raise ValueError(f"Credo grid Shopify product {index} is not an object")
        product_id = str(product.get("id") or "")
        handle = str(product.get("handle") or "")
        if not product_id or _PRODUCT_PATH.fullmatch(f"/products/{handle}") is None:
            raise ValueError(f"Credo grid Shopify product {index} lacks exact identity")
        state_products.append((product_id, handle))
    if not state_products or len({handle for _product_id, handle in state_products}) != len(
        state_products
    ):
        raise ValueError("Credo grid Shopify product set is empty or duplicated")

    parser = _CredoGridParser()
    parser.feed(html)
    parser.close()
    dom_handles = tuple(dict.fromkeys(parser.product_handles))
    state_handles = tuple(handle for _product_id, handle in state_products)
    if dom_handles != state_handles:
        raise ValueError(
            "Credo grid DOM and Shopify product identities do not reconcile exactly"
        )
    if len(parser.vendors) != len(state_products) or any(
        vendor.casefold() != "tower 28" for vendor in parser.vendors
    ):
        raise ValueError("Credo grid does not bind every product card to Tower 28")
    if parser.next_urls:
        raise ValueError("Credo grid exposes a next-page route; single-response completeness is false")

    title = _collection_title(html)
    if title.casefold() != "tower 28 beauty":
        raise ValueError("Credo collection title does not bind Tower 28 Beauty")
    cards = tuple(
        CredoBrandGridCard(
            grid_position=index,
            product_id=product_id,
            handle=handle,
            product_url=f"https://credobeauty.com/products/{handle}",
            vendor=parser.vendors[index - 1],
        )
        for index, (product_id, handle) in enumerate(state_products, start=1)
    )
    return CredoBrandGridState(
        source_url=source_url,
        collection_id=collection_id,
        collection_title=title,
        country_code="US",
        currency_code="USD",
        cards=cards,
        pagination_next_url=None,
    )


def load_credo_shopify_init_data(html: str) -> dict[str, object]:
    return _shopify_init_data(html)


def _shopify_init_data(html: str) -> dict[str, object]:
    decoder = json.JSONDecoder()
    candidates: list[dict[str, object]] = []
    for match in re.finditer(r"\binitData\s*:\s*", html):
        try:
            value, _end = decoder.raw_decode(html[match.end() :])
        except json.JSONDecodeError:
            continue
        if (
            isinstance(value, dict)
            and isinstance(value.get("shop"), dict)
            and isinstance(value.get("products"), list)
        ):
            candidates.append(value)
    if len(candidates) != 1:
        raise ValueError(
            f"Credo page requires exactly one Shopify initData object; observed {len(candidates)}"
        )
    return candidates[0]


def _shopify_page_state(html: str) -> dict[str, object]:
    page_types = tuple(
        dict.fromkeys(re.findall(r'"pageType"\s*:\s*"([^"]+)"', html))
    )
    resource_ids = tuple(
        dict.fromkeys(re.findall(r'"resourceId"\s*:\s*"?([0-9]+)"?', html))
    )
    if len(page_types) != 1 or len(resource_ids) != 1:
        raise ValueError("Credo page lacks one Shopify pageType/resourceId binding")
    return {"pageType": page_types[0], "resourceId": resource_ids[0]}


def _collection_title(html: str) -> str:
    matches = re.findall(r"\bcollection\.title\s*=\s*(\"(?:\\.|[^\"\\])*\")", html)
    values: list[str] = []
    for raw in matches:
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(value, str) and value.strip():
            values.append(value.strip())
    unique = tuple(dict.fromkeys(values))
    if len(unique) != 1:
        raise ValueError("Credo grid requires one collection.title value")
    return unique[0]


class _CredoGridParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.product_handles: list[str] = []
        self.vendors: list[str] = []
        self.next_urls: list[str] = []
        self._in_grid = False
        self._vendor_div_depth = 0
        self._vendor_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key.lower(): value or "" for key, value in attrs}
        lowered = tag.lower()
        rel = {item.casefold() for item in attributes.get("rel", "").split()}
        if lowered in {"a", "link"} and "next" in rel and attributes.get("href"):
            self.next_urls.append(attributes["href"].strip())
        if lowered == "ul" and attributes.get("id") == "product-grid":
            if self._in_grid:
                raise ValueError("Credo grid contains nested product-grid roots")
            self._in_grid = True
            return
        if not self._in_grid:
            return
        if lowered == "a":
            match = _PRODUCT_PATH.fullmatch(urlparse(attributes.get("href", "")).path)
            if match is not None:
                self.product_handles.append(match.group("handle"))
        if lowered == "div" and self._vendor_div_depth:
            self._vendor_div_depth += 1
        if lowered == "div" and "newvendor" in {
            value.casefold() for value in attributes.get("class", "").split()
        }:
            self._vendor_div_depth = 1
            self._vendor_parts = []

    def handle_data(self, data: str) -> None:
        if self._vendor_div_depth:
            self._vendor_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if not self._in_grid:
            return
        lowered = tag.lower()
        if lowered == "div" and self._vendor_div_depth:
            self._vendor_div_depth -= 1
            if not self._vendor_div_depth:
                vendor = " ".join("".join(self._vendor_parts).split())
                if vendor:
                    self.vendors.append(vendor)
                self._vendor_parts = []


__all__ = [
    "CREDO_GRID_PARSER_VERSION",
    "CredoBrandGridCard",
    "CredoBrandGridState",
    "canonical_credo_collection_url",
    "load_credo_brand_grid_state",
    "load_credo_shopify_init_data",
]
