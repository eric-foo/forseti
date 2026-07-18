"""Sephora US/USD storefront-market assertion for CloakBrowser capture.

The public Sephora route accepts ``country_switch=us`` as request intent and
serializes the served country in ``Sephora.renderQueryParams``. Product JSON-LD
then exposes retailer-bound offer currency. This plugin performs no preference
mutation: it confirms the final rendered page only when those independent,
retailer-owned signals agree on US/USD.

Delivery location is deliberately outside this assertion.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Iterator

from source_capture.adapters.cloakbrowser_snapshot import (
    PinConfirmation,
    PreCaptureOutcome,
)


_RENDER_QUERY_MARKER = "Sephora.renderQueryParams"


@dataclass(frozen=True)
class SephoraUSMarketPlugin:
    """Confirm the rendered Sephora page is serving its US/USD storefront."""

    country_code: str = "US"
    currency_code: str = "USD"

    def __post_init__(self) -> None:
        if self.country_code != "US" or self.currency_code != "USD":
            raise ValueError("Sephora market assertion currently supports only US/USD")

    @property
    def humanize(self) -> bool:
        return False

    def before(self, page: object, *, setup_timeout_ms: float) -> PreCaptureOutcome:
        del page, setup_timeout_ms
        return PreCaptureOutcome(
            attempted=True,
            steps_completed=True,
            reason=None,
            warning_notes=[],
        )

    def confirm(self, rendered_dom: str) -> PinConfirmation:
        return confirm_sephora_us_market(rendered_dom)

    def describe(self) -> dict[str, object]:
        return {
            "pre_capture": "sephora_us_market_assertion",
            "country_code_requested": self.country_code,
            "currency_code_requested": self.currency_code,
            "market_preference_action": "none_rendered_market_assertion",
        }

    def note(self, outcome: PreCaptureOutcome, confirmation: PinConfirmation) -> str:
        if confirmation.confirmed:
            return (
                "declared_storefront_market: Sephora rendered route CONFIRMED as "
                f"US/USD ({confirmation.detail}); delivery location remains un-pinned"
            )
        reason = confirmation.detail
        if not outcome.steps_completed and outcome.reason is not None:
            reason = f"pre-capture assertion setup failed: {outcome.reason}; {reason}"
        return (
            "declared_storefront_market: Sephora US/USD rendered-market assertion NOT "
            f"confirmed ({reason}); treat storefront country and currency as un-pinned "
            "(honest gap)"
        )


def confirm_sephora_us_market(rendered_dom: str) -> PinConfirmation:
    """Require Sephora's served-country state and a Sephora-sold USD offer."""
    dom = rendered_dom or ""
    country_confirmed = any(
        params.get("country") == "US" for params in _iter_render_query_params(dom)
    )
    usd_offer_confirmed = any(
        _is_sephora_usd_offer(candidate) for candidate in _iter_json_ld_objects(dom)
    )
    if country_confirmed and usd_offer_confirmed:
        return PinConfirmation(
            confirmed=True,
            detail=(
                "Sephora.renderQueryParams bound country=US and product JSON-LD "
                "contained a Sephora-sold Offer with priceCurrency=USD"
            ),
        )
    missing: list[str] = []
    if not country_confirmed:
        missing.append("Sephora.renderQueryParams country=US")
    if not usd_offer_confirmed:
        missing.append("Sephora-sold JSON-LD Offer with priceCurrency=USD")
    return PinConfirmation(
        confirmed=False,
        detail="required Sephora US/USD rendered conjunction absent: " + "; ".join(missing),
    )


def _iter_render_query_params(rendered_dom: str) -> Iterator[dict[str, Any]]:
    decoder = json.JSONDecoder()
    search_from = 0
    while True:
        marker_index = rendered_dom.find(_RENDER_QUERY_MARKER, search_from)
        if marker_index < 0:
            return
        marker_end = marker_index + len(_RENDER_QUERY_MARKER)
        object_start = rendered_dom.find("{", marker_end)
        if object_start < 0:
            return
        if rendered_dom[marker_end:object_start].strip() != "=":
            search_from = marker_end
            continue
        try:
            value, consumed = decoder.raw_decode(rendered_dom[object_start:])
        except json.JSONDecodeError:
            search_from = marker_end
            continue
        search_from = object_start + consumed
        if isinstance(value, dict):
            yield value


class _JsonLdScriptParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self._in_json_ld = False
        self._parts: list[str] = []
        self.documents: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag.lower() != "script":
            return
        attributes = {
            key.lower(): (value or "").lower()
            for key, value in attrs
        }
        if attributes.get("type") == "application/ld+json":
            self._in_json_ld = True
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._in_json_ld:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script" and self._in_json_ld:
            self.documents.append("".join(self._parts))
            self._parts = []
            self._in_json_ld = False


def _iter_json_ld_objects(rendered_dom: str) -> Iterator[dict[str, Any]]:
    parser = _JsonLdScriptParser()
    try:
        parser.feed(rendered_dom)
        parser.close()
    except Exception:
        return
    for document in parser.documents:
        try:
            value = json.loads(document)
        except (json.JSONDecodeError, TypeError):
            continue
        yield from _walk_json_objects(value)


def _walk_json_objects(value: Any) -> Iterator[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk_json_objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_json_objects(child)


def _is_sephora_usd_offer(candidate: dict[str, Any]) -> bool:
    if candidate.get("@type") != "Offer":
        return False
    if candidate.get("priceCurrency") != "USD":
        return False
    price = candidate.get("price")
    if isinstance(price, bool) or not isinstance(price, (str, int, float)):
        return False
    if isinstance(price, str) and not price.strip():
        return False
    seller = candidate.get("seller")
    return (
        isinstance(seller, dict)
        and seller.get("@type") == "Organization"
        and seller.get("name") == "Sephora"
    )
