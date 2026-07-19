"""Walmart US/USD storefront assertion for anonymous Direct HTTP capture.

The assertion performs no preference or delivery-location mutation. It admits
only one Walmart-owned ``__NEXT_DATA__`` product state that binds the requested
item, USD offer currency, internally consistent origin-derived postal context,
and an immediate US module-targeting signal.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urlparse


_WALMART_HOST = "www.walmart.com"
_WALMART_ITEM_PATH = re.compile(r"^/ip/(?:[^/]+/)?(?P<item_id>[0-9]+)/?$")


@dataclass(frozen=True)
class WalmartUSMarketConfirmation:
    confirmed: bool
    detail: str
    requested_item_id: str | None
    product_item_id: str | None
    observed_currency_code: str | None
    observed_postal_code: str | None
    country_signal_shape: str | None

    def metadata(self) -> dict[str, object]:
        return {
            "market_assertion": "walmart_us_market",
            "market_assertion_detail": self.detail,
            "requested_item_id": self.requested_item_id,
            "product_item_id": self.product_item_id,
            "bound_item_id": (
                self.requested_item_id
                if self.requested_item_id == self.product_item_id
                else None
            ),
            "country_code_confirmed": "US" if self.confirmed else None,
            "currency_code_confirmed": "USD" if self.confirmed else None,
            "observed_currency_code": self.observed_currency_code,
            "observed_location_postal_code": self.observed_postal_code,
            "observed_location_posture": (
                "origin_derived_unpinned"
                if self.observed_postal_code is not None
                else None
            ),
            "country_code_signal_shape": self.country_signal_shape,
            "pin_confirmed": self.confirmed,
        }


def validate_walmart_us_market_url(url: str) -> str:
    parsed = urlparse(url)
    match = _WALMART_ITEM_PATH.fullmatch(parsed.path)
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower() != _WALMART_HOST
        or match is None
    ):
        raise ValueError(
            "--walmart-market US requires an HTTPS www.walmart.com /ip/.../<item-id> PDP URL"
        )
    return match.group("item_id")


def confirm_walmart_us_market(
    html: str,
    *,
    requested_url: str,
    final_url: str,
) -> WalmartUSMarketConfirmation:
    """Require one bound Walmart item/currency/location/country conjunction."""
    try:
        requested_item_id = validate_walmart_us_market_url(requested_url)
    except ValueError as exc:
        return _failure(str(exc))

    try:
        final_item_id = validate_walmart_us_market_url(final_url)
    except ValueError:
        return _failure(
            "required Walmart US/USD conjunction absent: final route was not the "
            "commissioned www.walmart.com PDP",
            requested_item_id=requested_item_id,
        )

    if final_item_id != requested_item_id:
        return _failure(
            "required Walmart US/USD conjunction absent: final Walmart item ID "
            "did not match the commissioned item",
            requested_item_id=requested_item_id,
        )

    parser = _NextDataParser()
    try:
        parser.feed(html or "")
        parser.close()
    except Exception:
        return _failure(
            "required Walmart US/USD conjunction absent: malformed HTML",
            requested_item_id=requested_item_id,
        )
    if len(parser.documents) != 1:
        return _failure(
            "required Walmart US/USD conjunction absent: expected exactly one "
            "Walmart __NEXT_DATA__ document",
            requested_item_id=requested_item_id,
        )

    try:
        root = json.loads(parser.documents[0])
    except (json.JSONDecodeError, TypeError):
        return _failure(
            "required Walmart US/USD conjunction absent: malformed __NEXT_DATA__ JSON",
            requested_item_id=requested_item_id,
        )

    data = _nested_mapping(root, "props", "pageProps", "initialData", "data")
    product = _mapping(data.get("product")) if data is not None else None
    content_layout = _mapping(data.get("contentLayout")) if data is not None else None
    product_item_id = _scalar_text(product.get("usItemId")) if product is not None else None

    price_info = _mapping(product.get("priceInfo")) if product is not None else None
    current_price = _mapping(price_info.get("currentPrice")) if price_info is not None else None
    currency_code = (
        _scalar_text(current_price.get("currencyUnit"))
        if current_price is not None
        else None
    )

    product_location = _mapping(product.get("location")) if product is not None else None
    page_metadata = (
        _mapping(content_layout.get("pageMetadata"))
        if content_layout is not None
        else None
    )
    page_location = (
        _mapping(page_metadata.get("location"))
        if page_metadata is not None
        else None
    )
    product_postal = (
        _scalar_text(product_location.get("postalCode"))
        if product_location is not None
        else None
    )
    page_postal = (
        _scalar_text(page_location.get("postalCode"))
        if page_location is not None
        else None
    )
    observed_postal = (
        product_postal
        if product_postal is not None and product_postal == page_postal
        else None
    )

    country_signal_shape = _admitted_country_signal_shape(content_layout)
    item_bound = product_item_id == requested_item_id
    usd_bound = currency_code == "USD"
    postal_bound = observed_postal is not None
    country_bound = country_signal_shape is not None

    if item_bound and usd_bound and postal_bound and country_bound:
        return WalmartUSMarketConfirmation(
            confirmed=True,
            detail=(
                f"Walmart __NEXT_DATA__ bound item {requested_item_id}, current-price "
                f"currency USD, equal page/product origin postal {observed_postal}, "
                f"and immediate module countryCode US ({country_signal_shape})"
            ),
            requested_item_id=requested_item_id,
            product_item_id=product_item_id,
            observed_currency_code=currency_code,
            observed_postal_code=observed_postal,
            country_signal_shape=country_signal_shape,
        )

    missing: list[str] = []
    if not item_bound:
        missing.append(f"product.usItemId={requested_item_id}")
    if not usd_bound:
        missing.append("product current-price currencyUnit=USD")
    if not postal_bound:
        missing.append("equal nonempty page/product postal context")
    if not country_bound:
        missing.append(
            "immediate module targeting countryCode as scalar US or exact [US]"
        )
    return WalmartUSMarketConfirmation(
        confirmed=False,
        detail="required Walmart US/USD conjunction absent: " + "; ".join(missing),
        requested_item_id=requested_item_id,
        product_item_id=product_item_id,
        observed_currency_code=currency_code,
        observed_postal_code=observed_postal,
        country_signal_shape=country_signal_shape,
    )


class _NextDataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.documents: list[str] = []
        self._capturing = False
        self._parts: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        attributes = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "script" and attributes.get("id") == "__NEXT_DATA__":
            self._capturing = True
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._capturing:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._capturing:
            self.documents.append("".join(self._parts))
            self._parts = []
            self._capturing = False


def _admitted_country_signal_shape(
    content_layout: dict[str, Any] | None,
) -> str | None:
    if content_layout is None:
        return None
    module_groups = (
        content_layout.get("modules"),
        content_layout.get("lazyModules"),
    )
    for modules in module_groups:
        if not isinstance(modules, list):
            continue
        for module in modules:
            module_mapping = _mapping(module)
            targeting = (
                _mapping(module_mapping.get("targeting"))
                if module_mapping is not None
                else None
            )
            if targeting is None:
                continue
            country_code = targeting.get("countryCode")
            if country_code == "US":
                return "scalar"
            if country_code == ["US"]:
                return "single_item_list"
    return None


def _nested_mapping(value: Any, *keys: str) -> dict[str, Any] | None:
    current = value
    for key in keys:
        mapping = _mapping(current)
        if mapping is None:
            return None
        current = mapping.get(key)
    return _mapping(current)


def _mapping(value: Any) -> dict[str, Any] | None:
    return value if isinstance(value, dict) else None


def _scalar_text(value: Any) -> str | None:
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        return None
    text = str(value).strip()
    return text or None


def _failure(
    detail: str,
    *,
    requested_item_id: str | None = None,
) -> WalmartUSMarketConfirmation:
    return WalmartUSMarketConfirmation(
        confirmed=False,
        detail=detail,
        requested_item_id=requested_item_id,
        product_item_id=None,
        observed_currency_code=None,
        observed_postal_code=None,
        country_signal_shape=None,
    )


__all__ = [
    "WalmartUSMarketConfirmation",
    "confirm_walmart_us_market",
    "validate_walmart_us_market_url",
]
