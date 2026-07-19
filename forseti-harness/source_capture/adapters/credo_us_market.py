"""Credo US/USD storefront assertion for anonymous Direct HTTP capture.

The assertion performs no preference, cookie, or delivery-location mutation.
It admits only one Credo-owned product state that binds the requested PDP and
canonical URL, Shopify country/currency globals, and a Product JSON-LD offer.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Mapping
from urllib.parse import urlparse


_CREDO_HOST = "credobeauty.com"
_CREDO_PRODUCT_PATH = re.compile(r"^/products/(?P<handle>[a-z0-9][a-z0-9-]*)/?$")


@dataclass(frozen=True)
class CredoUSMarketConfirmation:
    confirmed: bool
    detail: str
    requested_product_handle: str | None
    product_name: str | None
    brand_name: str | None
    product_sku: str | None
    observed_country_code: str | None
    observed_currency_code: str | None
    observed_offer_currencies: tuple[str, ...]
    canonical_url: str | None

    def metadata(self) -> dict[str, object]:
        return {
            "market_assertion": "credo_us_market",
            "market_assertion_detail": self.detail,
            "requested_product_handle": self.requested_product_handle,
            "bound_product_handle": (
                self.requested_product_handle if self.confirmed else None
            ),
            "product_name": self.product_name,
            "brand_name": self.brand_name,
            "product_sku": self.product_sku,
            "country_code_confirmed": "US" if self.confirmed else None,
            "currency_code_confirmed": "USD" if self.confirmed else None,
            "observed_country_code": self.observed_country_code,
            "observed_currency_code": self.observed_currency_code,
            "observed_offer_currencies": list(self.observed_offer_currencies),
            "canonical_url": self.canonical_url,
            "delivery_location_posture": "unpinned",
            "pin_confirmed": self.confirmed,
        }


def validate_credo_us_market_url(url: str) -> str:
    parsed = urlparse(url)
    match = _CREDO_PRODUCT_PATH.fullmatch(parsed.path)
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower() != _CREDO_HOST
        or match is None
    ):
        raise ValueError(
            "--credo-market US requires an HTTPS credobeauty.com /products/<handle> PDP URL"
        )
    return match.group("handle")


def confirm_credo_us_market(
    html: str,
    *,
    requested_url: str,
    final_url: str,
) -> CredoUSMarketConfirmation:
    """Require one bound Credo PDP/country/currency/offer conjunction."""
    try:
        requested_handle = validate_credo_us_market_url(requested_url)
    except ValueError as exc:
        return _failure(str(exc))

    try:
        final_handle = validate_credo_us_market_url(final_url)
    except ValueError:
        return _failure(
            "required Credo US/USD conjunction absent: final route was not the "
            "commissioned credobeauty.com PDP",
            requested_product_handle=requested_handle,
        )
    if final_handle != requested_handle:
        return _failure(
            "required Credo US/USD conjunction absent: final product handle did "
            "not match the commissioned product",
            requested_product_handle=requested_handle,
        )

    parser = _CredoDocumentParser()
    try:
        parser.feed(html or "")
        parser.close()
    except Exception:
        return _failure(
            "required Credo US/USD conjunction absent: malformed HTML",
            requested_product_handle=requested_handle,
        )

    canonical_urls = tuple(dict.fromkeys(parser.canonical_urls))
    canonical_url = canonical_urls[0] if len(canonical_urls) == 1 else None
    canonical_bound = (
        canonical_url is not None
        and _same_credo_product_route(canonical_url, final_url)
    )

    countries = _shopify_country_codes(html)
    currencies = _shopify_active_currencies(html)
    observed_country = next(iter(countries)) if len(countries) == 1 else None
    observed_currency = next(iter(currencies)) if len(currencies) == 1 else None

    products = _bound_products(parser.json_ld_documents, final_url=final_url)
    product = products[0] if len(products) == 1 else None
    product_name = _text(product.get("name")) if product is not None else None
    product_sku = _text(product.get("sku")) if product is not None else None
    brand_name = _brand_name(product.get("brand")) if product is not None else None
    offers = _product_offers(product)
    offer_currencies = tuple(
        sorted(
            {
                currency
                for offer in offers
                if (currency := _text(offer.get("priceCurrency"))) is not None
            }
        )
    )
    priced_offers = [
        offer
        for offer in offers
        if _nonempty_price(offer.get("price"))
        and _text(offer.get("priceCurrency")) == "USD"
    ]

    country_bound = countries == {"US"}
    currency_bound = currencies == {"USD"}
    product_bound = (
        product is not None
        and product_name is not None
        and brand_name is not None
        and offer_currencies == ("USD",)
        and bool(priced_offers)
    )
    if canonical_bound and country_bound and currency_bound and product_bound:
        return CredoUSMarketConfirmation(
            confirmed=True,
            detail=(
                f"Credo canonical PDP {requested_handle} bound Shopify country US, "
                f"active currency USD, and {len(priced_offers)} priced USD Product "
                f"offer(s) for {brand_name} / {product_name}"
            ),
            requested_product_handle=requested_handle,
            product_name=product_name,
            brand_name=brand_name,
            product_sku=product_sku,
            observed_country_code=observed_country,
            observed_currency_code=observed_currency,
            observed_offer_currencies=offer_currencies,
            canonical_url=canonical_url,
        )

    missing: list[str] = []
    if not canonical_bound:
        missing.append("one canonical URL matching the final Credo PDP")
    if not country_bound:
        missing.append("only Shopify.country=US")
    if not currency_bound:
        missing.append("only Shopify.currency.active=USD")
    if product is None:
        missing.append("exactly one Product JSON-LD object bound to the final PDP")
    else:
        if product_name is None:
            missing.append("bound Product name")
        if brand_name is None:
            missing.append("bound Product brand")
        if offer_currencies != ("USD",):
            missing.append("only USD Product offer currencies")
        if not priced_offers:
            missing.append("a nonempty priced USD Product offer")
    return CredoUSMarketConfirmation(
        confirmed=False,
        detail="required Credo US/USD conjunction absent: " + "; ".join(missing),
        requested_product_handle=requested_handle,
        product_name=product_name,
        brand_name=brand_name,
        product_sku=product_sku,
        observed_country_code=observed_country,
        observed_currency_code=observed_currency,
        observed_offer_currencies=offer_currencies,
        canonical_url=canonical_url,
    )


class _CredoDocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.canonical_urls: list[str] = []
        self.json_ld_documents: list[object] = []
        self._json_ld_parts: list[str] | None = None

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        attributes = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "link" and attributes.get("rel", "").lower() == "canonical":
            href = attributes.get("href", "").strip()
            if href:
                self.canonical_urls.append(href)
        if (
            tag.lower() == "script"
            and attributes.get("type", "").lower() == "application/ld+json"
        ):
            self._json_ld_parts = []

    def handle_data(self, data: str) -> None:
        if self._json_ld_parts is not None:
            self._json_ld_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "script" or self._json_ld_parts is None:
            return
        raw = "".join(self._json_ld_parts).strip()
        self._json_ld_parts = None
        if not raw:
            return
        try:
            self.json_ld_documents.append(json.loads(raw))
        except json.JSONDecodeError:
            self.json_ld_documents.append(None)


def _shopify_country_codes(html: str) -> set[str]:
    values: set[str] = set()
    for raw in re.findall(
        r"\bShopify\.country\s*=\s*(\"(?:\\.|[^\"\\])*\")\s*;",
        html or "",
    ):
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(value, str) and value.strip():
            values.add(value.strip())
    return values


def _shopify_active_currencies(html: str) -> set[str]:
    values: set[str] = set()
    marker = re.compile(r"\bShopify\.currency\s*=\s*")
    decoder = json.JSONDecoder()
    for match in marker.finditer(html or ""):
        try:
            value, _end = decoder.raw_decode((html or "")[match.end() :])
        except (json.JSONDecodeError, TypeError):
            continue
        if isinstance(value, dict):
            active = _text(value.get("active"))
            if active is not None:
                values.add(active)
    return values


def _bound_products(documents: list[object], *, final_url: str) -> list[Mapping[str, Any]]:
    products: list[Mapping[str, Any]] = []
    for document in documents:
        for value in _walk_mappings(document):
            product_types = value.get("@type")
            types = (
                {str(item) for item in product_types}
                if isinstance(product_types, list)
                else {str(product_types)}
                if product_types is not None
                else set()
            )
            if "Product" not in types:
                continue
            product_url = _text(value.get("url"))
            if product_url is not None and _same_credo_product_route(
                product_url, final_url
            ):
                products.append(value)
    return products


def _walk_mappings(value: object):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_mappings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_mappings(child)


def _product_offers(product: Mapping[str, Any] | None) -> list[Mapping[str, Any]]:
    if product is None:
        return []
    offers = product.get("offers")
    if isinstance(offers, dict):
        return [offers]
    if isinstance(offers, list):
        return [item for item in offers if isinstance(item, dict)]
    return []


def _brand_name(value: object) -> str | None:
    if isinstance(value, dict):
        return _text(value.get("name"))
    return _text(value)


def _same_credo_product_route(left: str, right: str) -> bool:
    try:
        left_handle = validate_credo_us_market_url(left)
        right_handle = validate_credo_us_market_url(right)
    except ValueError:
        return False
    return left_handle == right_handle


def _nonempty_price(value: object) -> bool:
    if isinstance(value, bool) or value is None:
        return False
    if isinstance(value, (int, float)):
        return value >= 0
    return isinstance(value, str) and bool(value.strip())


def _text(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    return text or None


def _failure(
    detail: str,
    *,
    requested_product_handle: str | None = None,
) -> CredoUSMarketConfirmation:
    return CredoUSMarketConfirmation(
        confirmed=False,
        detail=detail,
        requested_product_handle=requested_product_handle,
        product_name=None,
        brand_name=None,
        product_sku=None,
        observed_country_code=None,
        observed_currency_code=None,
        observed_offer_currencies=(),
        canonical_url=None,
    )


__all__ = [
    "CredoUSMarketConfirmation",
    "confirm_credo_us_market",
    "validate_credo_us_market_url",
]
