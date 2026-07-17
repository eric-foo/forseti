"""Nordstrom-specific US/USD preference pin for CloakBrowser capture.

The interaction is only an attempt. A packet records the pin as confirmed only when the
main URL's rendered DOM contains mutually reinforcing Nordstrom storefront-state signals.
Dollar-looking prices and Nordstrom's ``nordcountrycode`` cookie are deliberately excluded:
both appeared in an international capture and therefore cannot prove a US storefront.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass

from source_capture.adapters.cloakbrowser_snapshot import (
    PinConfirmation,
    PreCaptureOutcome,
)


_NORDSTROM_HOMEPAGE_URL = "https://www.nordstrom.com/"
_CONTROL_PROBE_TIMEOUT_MS = 2500
_POST_SELECTION_POLL_MS = 100
_HOMEPAGE_RENDER_SETTLE_MS = 5000

# The first two selectors cover the semantic control observed in earlier recon. The flag
# selectors cover the current rendered control, whose markup has no stable name/aria-label.
_COUNTRY_CONTROL_SELECTORS = (
    "button:has(img[src*='/alias/SG.gif'])",
    "button:has(img[src*='/alias/'][src$='.gif'])",
    "button[name='changeCountry']",
    "button[aria-label*='Choose your shipping country' i]",
    "footer button:has-text('Singapore')",
    "button:has-text('Singapore')",
)
_COUNTRY_SELECT_SELECTORS = (
    "[role='dialog'] select[name*='country' i]",
    "[role='dialog'] select",
    "select[name*='country' i]",
)
_COUNTRY_OPTION_SELECTORS = (
    "[role='dialog'] [role='option']:has-text('United States')",
    "[role='dialog'] button:has-text('United States')",
    "[role='dialog'] label:has-text('United States')",
    "[role='dialog'] text='United States'",
    "[role='option']:has-text('United States')",
    "button:has-text('United States')",
    "label:has-text('United States')",
)
_APPLY_SELECTORS = (
    "[role='dialog'] button:has-text('Save')",
    "[role='dialog'] button:has-text('Start Shopping')",
    "[role='dialog'] button:has-text('Continue')",
    "[role='dialog'] button:has-text('Apply')",
)


@dataclass(frozen=True)
class NordstromCountryPreferencePlugin:
    """Attempt Nordstrom's own country UI, then confirm US/USD on the main capture."""

    country_code: str = "US"
    currency_code: str = "USD"
    setup_timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        if self.country_code != "US" or self.currency_code != "USD":
            raise ValueError("Nordstrom country preference currently supports only US/USD")
        if self.setup_timeout_seconds <= 0:
            raise ValueError(
                "nordstrom_country_setup_timeout_seconds must be greater than zero"
            )

    @property
    def humanize(self) -> bool:
        return True

    @property
    def setup_timeout_ms(self) -> float:
        return self.setup_timeout_seconds * 1000

    def before(self, page: object, *, setup_timeout_ms: float) -> PreCaptureOutcome:
        warning_notes: list[str] = []
        deadline = time.monotonic() + (setup_timeout_ms / 1000)

        try:
            page.goto(  # type: ignore[union-attr]
                _NORDSTROM_HOMEPAGE_URL,
                wait_until="domcontentloaded",
                timeout=setup_timeout_ms,
            )
        except Exception as exc:
            return _failed_outcome(
                "homepage_navigation",
                f"homepage navigation failed ({exc})",
            )

        # Nordstrom's international-shipping banner is client-rendered after
        # ``domcontentloaded``. A measured five-second allowance made the visible header flag
        # control stable in the no-proxy capture environment.
        render_settle_ms = min(_HOMEPAGE_RENDER_SETTLE_MS, _remaining_ms(deadline))
        if render_settle_ms > 0:
            page.wait_for_timeout(render_settle_ms)  # type: ignore[union-attr]

        if not _click_first(page, _COUNTRY_CONTROL_SELECTORS, deadline):
            return _failed_outcome(
                "open_country_control",
                "could not open Nordstrom country preference control",
            )

        if not (
            _select_country(page, deadline)
            or _click_first(page, _COUNTRY_OPTION_SELECTORS, deadline)
        ):
            return _failed_outcome(
                "select_country",
                "could not select United States in Nordstrom country preference UI",
            )

        # Some Nordstrom variants apply immediately; others expose a final action. A missing
        # final-action button is therefore not called a setup failure. The post-main-navigation
        # rendered-state confirmation is authoritative in either case.
        apply_clicked = _click_first(page, _APPLY_SELECTORS, deadline)
        if not apply_clicked:
            warning_notes.append(
                "nordstrom_country_setup: no final apply control was clicked; the selected "
                "country may have applied immediately, and post-capture confirmation remains "
                "authoritative"
            )
        else:
            # Save can trigger a homepage navigation. Let it start, then place a bounded barrier
            # before the generic adapter navigates to the main PDP; without this, the two
            # navigations race and Playwright reports net::ERR_ABORTED for the main URL.
            settle_ms = min(1000, _remaining_ms(deadline))
            if settle_ms > 0:
                page.wait_for_timeout(settle_ms)  # type: ignore[union-attr]
            try:
                page.wait_for_load_state(  # type: ignore[union-attr]
                    "domcontentloaded",
                    timeout=_remaining_ms(deadline),
                )
            except Exception as exc:
                warning_notes.append(
                    "nordstrom_country_setup: post-Save navigation did not reach "
                    f"domcontentloaded within the setup bound ({exc}); post-capture "
                    "confirmation remains authoritative"
                )

        if not _wait_for_visible_us_control(page, deadline):
            warning_notes.append(
                "nordstrom_country_setup: United States was not observed on the homepage "
                "country control before main navigation; post-capture confirmation remains "
                "authoritative"
            )

        return PreCaptureOutcome(
            attempted=True,
            steps_completed=True,
            reason=None,
            warning_notes=warning_notes,
        )

    def confirm(self, rendered_dom: str) -> PinConfirmation:
        return confirm_nordstrom_us_storefront(rendered_dom)

    def describe(self) -> dict[str, object]:
        return {
            "pre_capture": "nordstrom_country_preference",
            "country_code_requested": self.country_code,
            "currency_code_requested": self.currency_code,
        }

    def note(self, outcome: PreCaptureOutcome, confirmation: PinConfirmation) -> str:
        if confirmation.confirmed:
            return (
                "declared_country_preference: Nordstrom country preference set to US/USD "
                f"and CONFIRMED ({confirmation.detail})"
            )
        if not outcome.steps_completed and outcome.reason is not None:
            reason = f"preference step failed: {outcome.reason}; {confirmation.detail}"
        else:
            reason = confirmation.detail
        return (
            "declared_country_preference: Nordstrom US/USD preference ATTEMPTED but NOT "
            f"confirmed ({reason}); storefront may remain the origin-IP locale -- treat as "
            "un-pinned (honest gap)"
        )


def confirm_nordstrom_us_storefront(rendered_dom: str) -> PinConfirmation:
    """Require two Nordstrom-owned US/USD state surfaces; never infer from price glyphs."""
    dom = rendered_dom or ""
    selected_pair = _has_json_value(dom, "selectedCountryCode", "US") and _has_json_value(
        dom, "selectedCurrencyCode", "USD"
    )
    shopper_context = _has_us_shopper_context(dom)
    visible_us_control = _has_visible_us_country_control(dom)

    if shopper_context and (selected_pair or visible_us_control):
        observed = (
            "selected country/currency state plus US shopper context"
            if selected_pair
            else "visible United States country control plus US shopper context"
        )
        return PinConfirmation(
            confirmed=True,
            detail=f"Nordstrom {observed} observed in rendered DOM",
        )
    return PinConfirmation(
        confirmed=False,
        detail=(
            "required Nordstrom US/USD conjunction absent from rendered DOM "
            "(US shopper context with either selected US/USD state or a visible "
            "United States country control)"
        ),
    )


def _failed_outcome(reason: str, detail: str) -> PreCaptureOutcome:
    return PreCaptureOutcome(
        attempted=True,
        steps_completed=False,
        reason=reason,
        warning_notes=[
            f"nordstrom_country_setup: {detail}; main URL capture proceeds without a "
            "confirmed country preference"
        ],
    )


def _click_first(page: object, selectors: tuple[str, ...], deadline: float) -> bool:
    for selector in selectors:
        timeout_ms = _remaining_probe_timeout_ms(deadline)
        if timeout_ms <= 0:
            break
        try:
            # The header and footer can both match the flag selectors. The header is first in
            # document order and is the measured interactive control; the footer copy was the
            # source of a setup-timeout failure when ``last`` was used.
            page.locator(selector).first.click(timeout=timeout_ms)  # type: ignore[union-attr]
            return True
        except Exception:
            continue
    return False


def _select_country(page: object, deadline: float) -> bool:
    for selector in _COUNTRY_SELECT_SELECTORS:
        timeout_ms = _remaining_probe_timeout_ms(deadline)
        if timeout_ms <= 0:
            break
        # The dialog exposes country first and currency second; country-specific selectors
        # precede the generic dialog-select fallback, and ``first`` preserves that ordering.
        locator = page.locator(selector).first  # type: ignore[union-attr]
        for option in ({"value": "US"}, {"label": "United States"}):
            try:
                locator.select_option(timeout=timeout_ms, **option)
                return True
            except Exception:
                continue
    return False


def _wait_for_visible_us_control(page: object, deadline: float) -> bool:
    poll_deadline = min(
        deadline,
        time.monotonic() + (_CONTROL_PROBE_TIMEOUT_MS / 1000),
    )
    while time.monotonic() < poll_deadline:
        remaining_ms = max(0.0, (poll_deadline - time.monotonic()) * 1000)
        try:
            body_text = page.locator("body").inner_text(  # type: ignore[union-attr]
                timeout=min(500, remaining_ms)
            )
            if "United States" in body_text:
                return True
        except Exception:
            pass
        pause_ms = min(_POST_SELECTION_POLL_MS, remaining_ms)
        if pause_ms > 0:
            page.wait_for_timeout(pause_ms)  # type: ignore[union-attr]
    return False


def _has_json_value(dom: str, key: str, value: str) -> bool:
    return (
        re.search(
            rf'["\']{re.escape(key)}["\']\s*:\s*["\']{re.escape(value)}["\']',
            dom,
            flags=re.IGNORECASE,
        )
        is not None
    )


def _has_json_boolean(dom: str, key: str, value: bool) -> bool:
    literal = "true" if value else "false"
    return (
        re.search(
            rf'["\']{re.escape(key)}["\']\s*:\s*{literal}\b',
            dom,
            flags=re.IGNORECASE,
        )
        is not None
    )


def _has_us_shopper_context(dom: str) -> bool:
    """Keep the three shopper signals in one Nordstrom Context object."""
    for match in re.finditer(
        r'["\']Context["\']\s*:\s*\{(?P<body>[^{}]{0,2000})\}',
        dom,
        flags=re.IGNORECASE,
    ):
        body = match.group("body")
        if (
            _has_json_value(body, "CountryCode", "US")
            and _has_json_value(body, "CurrencyCode", "USD")
            and _has_json_boolean(body, "IsInternationalShopping", False)
        ):
            return True
    return False


def _has_visible_us_country_control(dom: str) -> bool:
    for button in re.findall(r"<button\b[^>]*>.*?</button>", dom, flags=re.I | re.S):
        normalized = re.sub(r"<[^>]+>", " ", button)
        if "United States" not in normalized:
            continue
        if (
            re.search(r"name=[\"']changeCountry[\"']", button, flags=re.I)
            or re.search(r"shipping country", button, flags=re.I)
            or re.search(r"/alias/US\.gif", button, flags=re.I)
        ):
            return True
    return False


def _remaining_ms(deadline: float) -> float:
    return max(0.0, (deadline - time.monotonic()) * 1000)


def _remaining_probe_timeout_ms(deadline: float) -> float:
    return min(_CONTROL_PROBE_TIMEOUT_MS, _remaining_ms(deadline))
