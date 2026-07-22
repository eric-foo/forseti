"""Sephora storefront-country preference and assertion for browser capture.

The public Sephora route accepts ``country_switch=us`` as request intent and
serializes the served country in ``Sephora.renderQueryParams``. Outside the US,
Sephora may place a country-routing dialog over the target. This plugin uses only
the dialog's explicit ``Continue to Sephora.com`` action before the main capture
navigation.

PDP admission remains strict US/USD and requires retailer-bound offer currency.
Brand-grid admission confirms the US country route independently; currency stays
separately observed and is never inferred from a dollar glyph. Delivery location
is deliberately outside both assertions.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Iterator, Literal
from urllib.parse import parse_qs, urlparse

from source_capture.adapters.cloakbrowser_snapshot import (
    PinConfirmation,
    PreCaptureOutcome,
)
from source_capture.sephora_brand_grid import (
    SephoraBrandGridStateError,
    load_sephora_brand_grid_state,
)


_RENDER_QUERY_MARKER = "Sephora.renderQueryParams"
_SEPHORA_HOSTS = frozenset({"sephora.com", "www.sephora.com"})
_COUNTRY_DIALOG_SELECTOR = (
    '[role="dialog"][aria-modal="true"][data-at="modal_dialog"]'
)
_COUNTRY_DIALOG_DIAGNOSTIC_TEXT = "This site does not ship to your country."
_COUNTRY_DIALOG_CONTINUE_TEXT = "Continue to"
_COUNTRY_DIALOG_WAIT_MS = 5_000
_COUNTRY_DIALOG_POST_CLICK_WAIT_MS = 2_000


@dataclass(frozen=True)
class SephoraUSMarketPlugin:
    """Establish and confirm the page-kind-specific Sephora storefront."""

    target_url: str
    country_code: str = "US"
    currency_code: str = "USD"
    page_kind: Literal["pdp", "grid"] = "pdp"

    def __post_init__(self) -> None:
        if self.country_code != "US" or self.currency_code != "USD":
            raise ValueError("Sephora market assertion currently supports only US/USD")
        if self.page_kind not in {"pdp", "grid"}:
            raise ValueError("Sephora market assertion page_kind must be pdp or grid")
        parsed = urlparse(self.target_url)
        country_switch = parse_qs(parsed.query).get("country_switch", [])
        if (
            parsed.scheme != "https"
            or (parsed.hostname or "").lower() not in _SEPHORA_HOSTS
            or not any(value.lower() == "us" for value in country_switch)
        ):
            raise ValueError(
                "Sephora market preference requires an HTTPS sephora.com target "
                "with country_switch=us"
            )

    @property
    def humanize(self) -> bool:
        return True

    def before(self, page: object, *, setup_timeout_ms: float) -> PreCaptureOutcome:
        try:
            page.goto(
                self.target_url,
                wait_until="domcontentloaded",
                timeout=setup_timeout_ms,
            )
            page.wait_for_timeout(min(_COUNTRY_DIALOG_WAIT_MS, setup_timeout_ms))
            dialog = page.locator(_COUNTRY_DIALOG_SELECTOR)
            if dialog.count() == 0 or not dialog.is_visible():
                return _preference_outcome()
            dialog_text = dialog.inner_text(timeout=setup_timeout_ms)
            if _COUNTRY_DIALOG_DIAGNOSTIC_TEXT not in dialog_text:
                return _preference_outcome(
                    reason="Sephora country dialog did not carry the expected diagnostic text"
                )
            continue_button = (
                dialog.locator("p")
                .filter(has_text=_COUNTRY_DIALOG_CONTINUE_TEXT)
                .locator("button")
            )
            if continue_button.count() != 1:
                return _preference_outcome(
                    reason=(
                        "Sephora country dialog did not expose exactly one scoped "
                        "Continue-to-Sephora control"
                    )
                )
            continue_button.click(timeout=setup_timeout_ms)
            page.wait_for_timeout(
                min(_COUNTRY_DIALOG_POST_CLICK_WAIT_MS, setup_timeout_ms)
            )
            if dialog.count() != 0 and dialog.is_visible():
                return _preference_outcome(
                    reason="Sephora country dialog remained visible after explicit continuation"
                )
            if (urlparse(str(page.url)).hostname or "").lower() not in _SEPHORA_HOSTS:
                return _preference_outcome(
                    reason="Sephora country continuation left the sephora.com storefront"
                )
            return _preference_outcome()
        except Exception as exc:
            return _preference_outcome(
                reason=(
                    "Sephora country-continuation preflight failed: "
                    f"{type(exc).__name__}"
                )
            )

    def confirm(self, rendered_dom: str) -> PinConfirmation:
        return confirm_sephora_us_market(rendered_dom, page_kind=self.page_kind)

    def describe(self) -> dict[str, object]:
        return {
            "pre_capture": "sephora_us_country_continuation_and_market_assertion",
            "market_page_kind": self.page_kind,
            "country_code_requested": self.country_code,
            "currency_code_requested": self.currency_code,
            "market_confirmation_scope": (
                "country_and_currency" if self.page_kind == "pdp" else "country_route_only"
            ),
            "market_preference_action": (
                "exact_country_dialog_continue_then_main_target_navigation"
            ),
        }

    def note(self, outcome: PreCaptureOutcome, confirmation: PinConfirmation) -> str:
        reason = confirmation.detail
        if not outcome.steps_completed and outcome.reason is not None:
            reason = f"pre-capture assertion setup failed: {outcome.reason}; {reason}"
        if self.page_kind == "grid":
            if confirmation.confirmed:
                return (
                    "declared_storefront_country: Sephora rendered route CONFIRMED as "
                    f"US ({confirmation.detail}); currency and delivery location remain "
                    "separately typed"
                )
            return (
                "declared_storefront_country: Sephora US country-route assertion NOT "
                f"confirmed ({reason}); treat storefront country, currency, and delivery "
                "location as un-pinned (honest gap)"
            )
        if confirmation.confirmed:
            return (
                "declared_storefront_market: Sephora rendered route CONFIRMED as "
                f"US/USD ({confirmation.detail}); delivery location remains un-pinned"
            )
        return (
            "declared_storefront_market: Sephora US/USD rendered-market assertion NOT "
            f"confirmed ({reason}); treat storefront country and currency as un-pinned "
            "(honest gap)"
        )


def confirm_sephora_us_market(
    rendered_dom: str, *, page_kind: Literal["pdp", "grid"] = "pdp"
) -> PinConfirmation:
    """Confirm the US route; require exact USD independently for PDPs only."""
    dom = rendered_dom or ""
    country_dialog_absent = _COUNTRY_DIALOG_DIAGNOSTIC_TEXT not in dom
    country_values = [
        params["country"]
        for params in _iter_render_query_params(dom)
        if "country" in params
    ]
    if page_kind == "grid":
        # Grid admission carries no second retailer-owned conjunct, so the country
        # evidence must be unanimous: contradictory serialized country values
        # fail closed instead of being outvoted by one US occurrence.
        country_confirmed = bool(country_values) and all(
            value == "US" for value in country_values
        )
        grid_state_error: str | None = None
        try:
            grid_state = load_sephora_brand_grid_state(dom)
        except SephoraBrandGridStateError as exc:
            grid_state = None
            grid_state_error = str(exc)
        currency_codes = (
            grid_state.explicit_currency_codes if grid_state is not None else ()
        )
        # Currency is reported as observed, never as inferred. An unreadable or
        # absent grid state is not evidence that no explicit currency code exists.
        if grid_state_error is not None:
            currency_observation = (
                f"grid currency state was unreadable ({grid_state_error}), so "
                "currency remains un-pinned"
            )
        elif grid_state is None:
            currency_observation = (
                "no retailer-owned grid currency state was present, so currency "
                "remains un-pinned"
            )
        elif currency_codes == ("USD",):
            currency_observation = (
                "explicit grid currency code USD was observed separately"
            )
        elif currency_codes:
            currency_observation = (
                "explicit grid currency code(s) "
                + ", ".join(currency_codes)
                + " were observed separately and were not promoted to USD"
            )
        else:
            currency_observation = (
                "grid state exposed no explicit currency code, so currency "
                "remains un-pinned"
            )
        if country_dialog_absent and country_confirmed:
            return PinConfirmation(
                confirmed=True,
                detail=(
                    "country-routing dialog absent and Sephora.renderQueryParams bound "
                    f"country=US; {currency_observation}; grid admission is country-only"
                ),
            )
        missing: list[str] = []
        if not country_dialog_absent:
            missing.append("country-routing dialog absent")
        if not country_confirmed:
            if country_values:
                missing.append(
                    "unanimous Sephora.renderQueryParams country=US (observed "
                    + ", ".join(repr(value) for value in country_values)
                    + ")"
                )
            else:
                missing.append("Sephora.renderQueryParams country=US")
        return PinConfirmation(
            confirmed=False,
            detail=(
                "required Sephora US country-route conjunction absent: "
                + "; ".join(missing)
                + f"; {currency_observation}"
            ),
        )
    if page_kind != "pdp":
        raise ValueError("Sephora market confirmation page_kind must be pdp or grid")
    # PDP admission keeps its existing country rule because the Sephora-sold USD
    # Offer below is an independent second conjunct.
    country_confirmed = any(value == "US" for value in country_values)
    currency_confirmed = any(
        _is_sephora_usd_offer(candidate) for candidate in _iter_json_ld_objects(dom)
    )
    if country_dialog_absent and country_confirmed and currency_confirmed:
        return PinConfirmation(
            confirmed=True,
            detail=(
                "country-routing dialog absent, Sephora.renderQueryParams bound "
                "country=US, and product JSON-LD contained a Sephora-sold Offer "
                "with priceCurrency=USD"
            ),
        )
    missing: list[str] = []
    if not country_dialog_absent:
        missing.append("country-routing dialog absent")
    if not country_confirmed:
        missing.append("Sephora.renderQueryParams country=US")
    if not currency_confirmed:
        missing.append("Sephora-sold JSON-LD Offer with priceCurrency=USD")
    return PinConfirmation(
        confirmed=False,
        detail="required Sephora US/USD rendered conjunction absent: " + "; ".join(missing),
    )


def _preference_outcome(*, reason: str | None = None) -> PreCaptureOutcome:
    return PreCaptureOutcome(
        attempted=True,
        steps_completed=reason is None,
        reason=reason,
        warning_notes=[],
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
