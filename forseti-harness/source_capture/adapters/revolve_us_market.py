"""REVOLVE US/USD storefront preference and fail-closed assertion."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Iterator, Literal
from urllib.parse import urlparse

from source_capture.adapters.cloakbrowser_snapshot import (
    PinConfirmation,
    PreCaptureOutcome,
)


_REVOLVE_HOSTS = frozenset({"revolve.com", "www.revolve.com"})
_PREFERENCE_TRIGGER = 'button[data-url="/r/ajax/CountryPreferences.jsp"]'
_COUNTRY_SELECT = "#preferences-shipTo"
_CURRENCY_SELECT = "#preferences-currency"
_UPDATE_CONTROL = 'button:has-text("Update Preferences")'
_PREFERENCE_DIALOG = (
    '[role="dialog"][aria-label="Please Choose Your Country/Region Preferences"],'
    '[role="dialog"]:has-text("Please Choose Your Country/Region Preferences")'
)
_PREFERENCE_MARKER = "Country Preference: US"
_PREFERENCE_CURRENCY_MARKER = "$USD"
_PREFERENCE_WAIT_MS = 10_000
_STYLE_ID_RE = re.compile(r"^[A-Z0-9]{2,12}-[A-Z]{1,4}\d+$", re.IGNORECASE)


@dataclass(frozen=True)
class RevolveUSMarketPlugin:
    """Set REVOLVE's public country/currency controls and confirm their result."""

    target_url: str
    style_id: str | None = None
    country_code: str = "US"
    currency_code: str = "USD"
    page_kind: Literal["pdp", "grid"] = "pdp"

    def __post_init__(self) -> None:
        parsed = urlparse(self.target_url)
        if self.country_code != "US" or self.currency_code != "USD":
            raise ValueError("REVOLVE market preference currently supports only US/USD")
        if parsed.scheme != "https" or (parsed.hostname or "").lower() not in _REVOLVE_HOSTS:
            raise ValueError("REVOLVE market preference requires an HTTPS revolve.com URL")
        if self.page_kind == "grid":
            if not re.fullmatch(
                r"/[a-z0-9][a-z0-9-]*/br/[a-f0-9]{6}",
                parsed.path.rstrip("/"),
                flags=re.IGNORECASE,
            ):
                raise ValueError(
                    "REVOLVE grid market preference requires /<brand>/br/<brand-id>"
                )
            return
        if (
            self.style_id is None
            or not _STYLE_ID_RE.fullmatch(self.style_id)
            or f"/DP/{self.style_id.upper()}" not in parsed.path.upper()
        ):
            raise ValueError(
                "REVOLVE PDP market preference requires a REVOLVE style id "
                "matching the requested URL"
            )

    @property
    def humanize(self) -> bool:
        return True

    def before(self, page: object, *, setup_timeout_ms: float) -> PreCaptureOutcome:
        timeout_ms = max(1, min(int(setup_timeout_ms), _PREFERENCE_WAIT_MS))
        last_reason = "REVOLVE country/currency preference did not run"
        for attempt in (1, 2):
            stage = "navigate_target"
            try:
                page.goto(  # type: ignore[union-attr]
                    self.target_url,
                    wait_until="domcontentloaded",
                    timeout=setup_timeout_ms,
                )
                page.wait_for_timeout(min(1_000, timeout_ms))  # type: ignore[union-attr]
                html = page.content()  # type: ignore[union-attr]
                if _rendered_preference_is_usd(html):
                    return _outcome()

                stage = "wait_preference_trigger"
                page.wait_for_selector(_PREFERENCE_TRIGGER, timeout=timeout_ms)  # type: ignore[union-attr]
                trigger = page.locator(_PREFERENCE_TRIGGER)  # type: ignore[union-attr]
                if trigger.count() != 1:
                    last_reason = (
                        "REVOLVE country-preference trigger was absent or ambiguous "
                        f"on attempt {attempt}"
                    )
                    continue
                stage = "click_preference_trigger"
                trigger.click(timeout=timeout_ms)
                stage = "wait_country_control"
                page.wait_for_selector(_COUNTRY_SELECT, timeout=timeout_ms)  # type: ignore[union-attr]
                stage = "wait_currency_control"
                page.wait_for_selector(_CURRENCY_SELECT, timeout=timeout_ms)  # type: ignore[union-attr]
                stage = "wait_update_control"
                page.wait_for_selector(_UPDATE_CONTROL, timeout=timeout_ms)  # type: ignore[union-attr]
                country = page.locator(_COUNTRY_SELECT)  # type: ignore[union-attr]
                currency = page.locator(_CURRENCY_SELECT)  # type: ignore[union-attr]
                update = page.locator(_UPDATE_CONTROL)  # type: ignore[union-attr]
                counts = (country.count(), currency.count(), update.count())
                if counts != (1, 1, 1):
                    last_reason = (
                        "REVOLVE preference controls were absent or ambiguous "
                        f"on attempt {attempt}: country={counts[0]}, "
                        f"currency={counts[1]}, update={counts[2]}"
                    )
                    continue
                stage = "select_country_US"
                country.select_option(value="US", timeout=timeout_ms)
                stage = "select_currency_USD"
                currency.select_option(value="USD", timeout=timeout_ms)
                stage = "click_update_preferences"
                update.click(timeout=timeout_ms, no_wait_after=True)
                stage = "settle_preference_update"
                page.wait_for_timeout(min(3_000, timeout_ms))  # type: ignore[union-attr]
                if (urlparse(str(page.url)).hostname or "").lower() not in _REVOLVE_HOSTS:  # type: ignore[union-attr]
                    last_reason = (
                        "REVOLVE preference update left the revolve.com storefront "
                        f"on attempt {attempt}"
                    )
                    continue
                return _outcome()
            except Exception as exc:
                last_reason = (
                    "REVOLVE country/currency preference failed on attempt "
                    f"{attempt} at {stage}: {type(exc).__name__}"
                )
        return _outcome(reason=last_reason)

    def confirm(self, rendered_dom: str) -> PinConfirmation:
        return confirm_revolve_us_market(
            rendered_dom,
            expected_style_id=self.style_id,
            page_kind=self.page_kind,
        )

    def describe(self) -> dict[str, object]:
        return {
            "pre_capture": "revolve_us_country_currency_preference",
            "country_code_requested": self.country_code,
            "currency_code_requested": self.currency_code,
            "page_kind": self.page_kind,
            "style_id_requested": self.style_id,
            "market_preference_action": (
                "public_country_preferences_select_US_and_USD"
            ),
        }

    def note(self, outcome: PreCaptureOutcome, confirmation: PinConfirmation) -> str:
        detail = confirmation.detail
        if not outcome.steps_completed and outcome.reason:
            detail = f"pre-capture preference failed: {outcome.reason}; {detail}"
        if confirmation.confirmed:
            return (
                "declared_storefront_market: REVOLVE rendered storefront CONFIRMED "
                f"as US/USD ({detail}); shopper origin and delivery address remain un-pinned"
            )
        return (
            "declared_storefront_market: REVOLVE US/USD assertion NOT confirmed "
            f"({detail}); packet is diagnostic only"
        )


def confirm_revolve_us_market(
    rendered_dom: str,
    *,
    expected_style_id: str | None,
    page_kind: Literal["pdp", "grid"] = "pdp",
) -> PinConfirmation:
    dom = rendered_dom or ""
    preference = _rendered_preference_is_usd(dom)
    country_links = re.findall(r"countryCode=([A-Za-z]{2})", dom, flags=re.IGNORECASE)
    country_bound = bool(country_links) and all(
        value.upper() == "US" for value in country_links
    )
    body_us = bool(
        re.search(r"<body\b[^>]*\bclass=[\"'][^\"']*\bUS\b", dom, re.IGNORECASE)
    )
    conflicts = _explicit_currency_conflicts(dom)
    if page_kind == "grid":
        usd_prices = bool(
            re.search(
                r"class=[\"'][^\"']*\b(?:plp_price|js-plp-prices-div)\b"
                r"[^\"']*[\"'][^>]*>\s*\$",
                dom,
                flags=re.IGNORECASE,
            )
        )
        if preference and country_bound and body_us and usd_prices and not conflicts:
            return PinConfirmation(
                confirmed=True,
                detail=(
                    "public preference rendered US and $USD, shipping links unanimously "
                    "bound countryCode=US, body storefront class bound US, and grid "
                    "prices carried no contradictory explicit currency"
                ),
            )
        missing = []
        if not preference:
            missing.append("Country Preference: US | EN | $USD")
        if not country_bound:
            missing.append("unanimous retailer shipping countryCode=US")
        if not body_us:
            missing.append("body storefront class US")
        if not usd_prices:
            missing.append("REVOLVE grid USD price nodes")
        if conflicts:
            missing.append("no contradictory explicit currency")
        return PinConfirmation(
            confirmed=False,
            detail="required REVOLVE US/USD grid conjunction absent: " + "; ".join(missing),
        )

    if expected_style_id is None:
        return PinConfirmation(
            confirmed=False,
            detail="required REVOLVE US/USD PDP conjunction absent: expected style id",
        )
    product = next(
        (
            value
            for value in _iter_json_ld_objects(dom)
            if value.get("@type") == "Product"
            and str(value.get("sku", "")).upper() == expected_style_id.upper()
        ),
        None,
    )
    offer_usd = False
    if product is not None:
        offers = product.get("offers")
        values = offers if isinstance(offers, list) else [offers]
        offer_usd = any(
            isinstance(value, dict)
            and value.get("priceCurrency") == "USD"
            and str(value.get("price", "")).strip()
            for value in values
        )
    yotpo_bound = bool(
        re.search(
            rf'data-yotpo-product-id=[\"\']{re.escape(expected_style_id)}[\"\']',
            dom,
            flags=re.IGNORECASE,
        )
        and re.search(r'data-yotpo-currency=[\"\']USD[\"\']', dom, re.IGNORECASE)
    )
    if (
        preference
        and country_bound
        and body_us
        and offer_usd
        and yotpo_bound
        and not conflicts
    ):
        return PinConfirmation(
            confirmed=True,
            detail=(
                "public preference rendered US and $USD, shipping links unanimously "
                f"bound countryCode=US, Product JSON-LD and Yotpo bound "
                f"{expected_style_id} to USD"
            ),
        )
    missing = []
    if not preference:
        missing.append("Country Preference: US | EN | $USD")
    if not country_bound:
        missing.append("unanimous retailer shipping countryCode=US")
    if not body_us:
        missing.append("body storefront class US")
    if not offer_usd:
        missing.append(f"Product JSON-LD SKU {expected_style_id} with USD offer")
    if not yotpo_bound:
        missing.append(f"Yotpo product {expected_style_id} with currency USD")
    if conflicts:
        missing.append("no contradictory explicit currency")
    return PinConfirmation(
        confirmed=False,
        detail="required REVOLVE US/USD PDP conjunction absent: " + "; ".join(missing),
    )


def _rendered_preference_is_usd(dom: str) -> bool:
    return _PREFERENCE_MARKER in dom and _PREFERENCE_CURRENCY_MARKER in dom


def _explicit_currency_conflicts(dom: str) -> list[str]:
    values = {
        match.upper()
        for match in re.findall(
            r'(?:data-yotpo-currency|priceCurrency)\\?["\']?\s*[:=]\s*\\?["\']([A-Z]{3})',
            dom,
            flags=re.IGNORECASE,
        )
    }
    return sorted(value for value in values if value != "USD")


def _outcome(*, reason: str | None = None) -> PreCaptureOutcome:
    return PreCaptureOutcome(
        attempted=True,
        steps_completed=reason is None,
        reason=reason,
        warning_notes=[],
    )


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


__all__ = ["RevolveUSMarketPlugin", "confirm_revolve_us_market"]
