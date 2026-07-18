"""Amazon-specific delivery-location pre-capture plugin for the CloakBrowser adapter.

This is the ONE place Amazon-specific knowledge lives: the delivery-location widget flow,
the US-storefront confirmation signal, and the operator-facing limitation wording. The
generic ``cloakbrowser_snapshot`` adapter knows none of it -- it only calls this plugin
through the ``PreCapturePlugin`` seam (``before`` / ``confirm`` / ``describe`` / ``note``).

The honesty keystone: setting the ZIP via clicks is an ATTEMPT, never proof. The packet
records the delivery pin as confirmed ONLY when ``confirm`` observes the requested ZIP in
Amazon's rendered location anchor together with an amazon.com US-marketplace marker. USD
alone confirms currency, not the requested delivery ZIP. When the conjunction is absent,
the note says ATTEMPTED-but-NOT-confirmed and the slot is treated as un-pinned -- never a
fake "set" claim that could let a non-US capture count as a US one (INV-1).
"""

from __future__ import annotations

import re
import time

from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import urlparse

from source_capture.adapters.cloakbrowser_snapshot import (
    PinConfirmation,
    PreCaptureOutcome,
)


# Homepage whose delivery-location widget pins the storefront. The main capture URL is a
# separate PDP; this navigation happens BEFORE it, inside the plugin's bounded setup window.
_AMAZON_HOMEPAGE_URL = "https://www.amazon.com/"
_AMAZON_US_HOSTS = frozenset({"amazon.com", "www.amazon.com"})

# Bounded state waits replace fixed sleeps. Amazon's VPN-routed homepage can finish
# DOMContentLoaded before its location anchor hydrates, so the anchor gets one longer,
# combined-selector readiness wait without paying that wait once per fallback selector.
_POST_APPLY_POLL_MS = 100
_WIDGET_PROBE_TIMEOUT_MS = 2500
_WIDGET_READY_TIMEOUT_MS = 5000
_WIDGET_CLICK_TIMEOUT_MS = 5000

# Widget selectors, probed on amazon.com 2026-06-16; subject to Amazon DOM changes.
_WIDGET_OPEN_SELECTORS = (
    "#nav-global-location-popover-link",
    "#glow-ingress-block",
)
_WIDGET_OPEN_SELECTOR = ", ".join(_WIDGET_OPEN_SELECTORS)
_ZIP_INPUT_SELECTORS = ("#GLUXZipUpdateInput", "input[id*='zip' i][type='text']")
_APPLY_SELECTORS = ("#GLUXZipUpdate", "span.a-button-inner > input[type='submit']")

# The US-storefront signal recon proved appears in the rendered DOM once a US ZIP is applied.
_LOCATION_ANCHOR_IDS = frozenset({"glow-ingress-line2", "glow-ingress-block"})
_LOCATION_TEXT_ATTRIBUTES = frozenset({"aria-label", "title"})
_IGNORED_LOCATION_CONTENT_TAGS = frozenset({"script", "style", "template", "noscript"})
_FIVE_DIGIT_ZIP_PATTERN = re.compile(r"(?<!\d)(\d{5})(?!\d)")
_US_MARKETPLACE_MARKERS = (
    "ue_sn = 'www.amazon.com'",
    "retail:prod:www.amazon.com",
    "assoc_handle=usflex",
)


@dataclass(frozen=True)
class AmazonDeliveryLocationPlugin:
    """Pin amazon.com to a US ZIP before the main capture, then CONFIRM the storefront flipped.

    ``delivery_zip`` is the US ZIP to set. ``setup_timeout_seconds`` bounds the pre-capture
    widget flow separately from the main capture timeout (FIX #1); it is converted to ms and
    used for the homepage nav and as the basis for the widget-step probe timeouts.
    """

    delivery_zip: str
    setup_timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        if self.setup_timeout_seconds <= 0:
            raise ValueError("delivery_zip_setup_timeout_seconds must be greater than zero")

    @property
    def humanize(self) -> bool:
        # The widget interaction needs the humanized launch profile.
        return True

    @property
    def setup_timeout_ms(self) -> float:
        """Bounded pre-capture timeout in ms (FIX #1); the engine passes this into ``before``."""
        return self.setup_timeout_seconds * 1000

    def before(self, page: object, *, setup_timeout_ms: float) -> PreCaptureOutcome:
        """Run the delivery-location widget flow. Records an ATTEMPT outcome, never a claim.

        ``steps_completed`` is True only when every step (homepage -> open widget -> fill ZIP
        -> apply) succeeded; ``reason`` names the FIRST failed step. Failures are recorded as
        warning notes (the main capture still proceeds, just un-pinned). The post-capture
        ``confirm`` is the source of truth for whether the storefront actually flipped.
        """
        warning_notes: list[str] = []
        setup_deadline = time.monotonic() + (setup_timeout_ms / 1000)

        # Step 1: homepage navigation (bounded by the setup timeout, not the main timeout).
        try:
            page.goto(
                _AMAZON_HOMEPAGE_URL,
                wait_until="domcontentloaded",
                timeout=setup_timeout_ms,
            )  # type: ignore[union-attr]
        except Exception as exc:
            warning_notes.append(
                f"delivery_zip_setup: homepage navigation failed ({exc}); "
                "main URL capture proceeds without delivery location pin"
            )
            return PreCaptureOutcome(
                attempted=True,
                steps_completed=False,
                reason="homepage_navigation",
                warning_notes=warning_notes,
            )

        homepage_hostname = _page_hostname(page)
        if homepage_hostname not in _AMAZON_US_HOSTS:
            observed = homepage_hostname or "unknown"
            warning_notes.append(
                "delivery_zip_setup: amazon.com homepage navigation landed on non-US "
                f"marketplace host {observed!r}; main URL capture proceeds without delivery "
                "location pin"
            )
            return PreCaptureOutcome(
                attempted=True,
                steps_completed=False,
                reason="homepage_marketplace_redirect",
                warning_notes=warning_notes,
            )

        # Step 2: open the delivery-location widget. The VPN-routed homepage can report
        # DOMContentLoaded before this anchor hydrates. Wait for either known selector in one
        # locator, then click it; this stays inside the shared setup budget and avoids paying a
        # full missing-selector timeout twice.
        widget_clicked = False
        widget_error: Exception | None = None
        widget = page.locator(_WIDGET_OPEN_SELECTOR).first  # type: ignore[union-attr]
        ready_ms = _remaining_timeout_ms(
            setup_deadline, cap_ms=_WIDGET_READY_TIMEOUT_MS
        )
        if ready_ms > 0:
            try:
                widget.wait_for(state="visible", timeout=ready_ms)
                click_ms = _remaining_timeout_ms(
                    setup_deadline, cap_ms=_WIDGET_CLICK_TIMEOUT_MS
                )
                if click_ms <= 0:
                    raise TimeoutError("shared setup window exhausted before widget click")
                widget.click(timeout=click_ms)
                widget_clicked = True
            except Exception as exc:
                widget_error = exc
        if not widget_clicked:
            failure_type = (
                type(widget_error).__name__ if widget_error is not None else "TimeoutError"
            )
            warning_notes.append(
                "delivery_zip_setup: delivery location widget did not become visible and "
                f"clickable within its bounded readiness step ({failure_type}); "
                "main URL capture proceeds without delivery location pin"
            )
            return PreCaptureOutcome(
                attempted=True,
                steps_completed=False,
                reason="open_widget",
                warning_notes=warning_notes,
            )

        # Step 3: fill the ZIP input.
        zip_filled = False
        for selector in _ZIP_INPUT_SELECTORS:
            probe_ms = _remaining_probe_timeout_ms(setup_deadline)
            if probe_ms <= 0:
                break
            try:
                page.locator(selector).first.fill(self.delivery_zip, timeout=probe_ms)  # type: ignore[union-attr]
                zip_filled = True
                break
            except Exception:
                continue
        if not zip_filled:
            warning_notes.append(
                "delivery_zip_setup: could not fill ZIP input; "
                "main URL capture proceeds without delivery location pin"
            )
            return PreCaptureOutcome(
                attempted=True,
                steps_completed=False,
                reason="fill_zip",
                warning_notes=warning_notes,
            )

        # Step 4: apply. FIX #3: if the Apply-button click loop fails and we fall back to
        # pressing Return, the apply step is still recorded as FAILED -- a Return that did not
        # throw is NOT proof the submit landed. steps_completed stays False and the post-capture
        # confirm() is the only thing that can mark the storefront pinned.
        apply_clicked = False
        for selector in _APPLY_SELECTORS:
            probe_ms = _remaining_probe_timeout_ms(setup_deadline)
            if probe_ms <= 0:
                break
            try:
                page.locator(selector).first.click(timeout=probe_ms)  # type: ignore[union-attr]
                apply_clicked = True
                break
            except Exception:
                continue
        if not apply_clicked:
            return_pressed = False
            try:
                page.keyboard.press("Return")  # type: ignore[union-attr]
                return_pressed = True
            except Exception as exc:
                warning_notes.append(
                    f"delivery_zip_setup: could not click Apply or press Return ({exc}); "
                    "main URL capture proceeds without delivery location pin"
                )
            if return_pressed:
                warning_notes.append(
                    "delivery_zip_setup: Apply-button click failed; fell back to pressing Return "
                    "(did not throw), but the apply submit is UNCONFIRMED from the click flow"
                )
            return PreCaptureOutcome(
                attempted=True,
                steps_completed=False,
                reason="apply",
                warning_notes=warning_notes,
            )

        if not _wait_for_delivery_zip(page, self.delivery_zip, setup_deadline):
            warning_notes.append(
                "delivery_zip_setup: Apply click completed but requested ZIP was not observed "
                "before main navigation; post-capture storefront confirmation remains authoritative"
            )

        return PreCaptureOutcome(
            attempted=True,
            steps_completed=True,
            reason=None,
            warning_notes=warning_notes,
        )

    def confirm(self, rendered_dom: str) -> PinConfirmation:
        return confirm_us_storefront_with_zip(rendered_dom, delivery_zip=self.delivery_zip)

    def describe(self) -> dict[str, object]:
        return {
            "pre_capture": "amazon_delivery_location",
            "delivery_zip_requested": self.delivery_zip,
        }

    def note(self, outcome: PreCaptureOutcome, confirmation: PinConfirmation) -> str:
        """The honesty keystone. NEVER asserts 'set'/'pinned' unless confirmation is True.

        Confirmed: the rendered DOM showed the US signal -> the storefront is genuinely pinned.
        Not confirmed: clicks happened but the storefront did not demonstrably flip -> the note
        says ATTEMPTED-but-NOT-confirmed and tells the reader to treat the slot as un-pinned. The
        before()-step ``reason`` (or the missing-signal detail) is surfaced so the gap is visible.
        """
        if confirmation.confirmed:
            return (
                f"declared_delivery_zip: Amazon US delivery location set to "
                f"{self.delivery_zip!r} and CONFIRMED "
                f"({confirmation.detail})"
            )
        if not outcome.steps_completed and outcome.reason is not None:
            reason = f"widget step failed: {outcome.reason}; {confirmation.detail}"
        else:
            reason = confirmation.detail
        return (
            f"declared_delivery_zip: Amazon delivery-location pin ATTEMPTED for "
            f"{self.delivery_zip!r} but NOT confirmed ({reason}); storefront may be the "
            "origin-IP locale -- treat as un-pinned (honest gap)"
        )


def confirm_us_storefront_with_zip(
    rendered_dom: str, *, delivery_zip: str
) -> PinConfirmation:
    """Confirm the requested ZIP remains bound to Amazon's US marketplace.

    A USD currency input is useful storefront evidence but cannot prove which delivery ZIP
    Amazon applied. Delivery-pin confirmation therefore requires the requested five-digit ZIP
    as an exact token in recognized location-anchor text, no conflicting ZIP in those anchors,
    and an amazon.com marketplace marker in the same rendered DOM.
    """
    if _has_us_delivery_zip_dom_signal(rendered_dom or "", delivery_zip):
        return PinConfirmation(
            confirmed=True,
            detail=(
                f"delivery ZIP {delivery_zip!r} was the only ZIP in recognized Amazon "
                "location-anchor text and amazon.com US-marketplace markers were observed"
            ),
        )
    return PinConfirmation(
        confirmed=False,
        detail=(
            f"requested delivery ZIP {delivery_zip!r} was not the sole exact five-digit ZIP "
            "bound to recognized Amazon location-anchor text together with an amazon.com "
            "US-marketplace marker in rendered DOM"
        ),
    )


def _has_us_delivery_zip_dom_signal(dom: str, delivery_zip: str) -> bool:
    if re.fullmatch(r"\d{5}", delivery_zip) is None:
        return False
    parser = _AmazonLocationAnchorParser()
    try:
        parser.feed(dom)
        parser.close()
    except Exception:
        return False
    location_zips = {
        match.group(1)
        for fragment in parser.location_fragments
        for match in _FIVE_DIGIT_ZIP_PATTERN.finditer(fragment)
    }
    normalized = dom.lower()
    marketplace_confirmed = any(
        marker in normalized for marker in _US_MARKETPLACE_MARKERS
    )
    return location_zips == {delivery_zip} and marketplace_confirmed


class _AmazonLocationAnchorParser(HTMLParser):
    """Collect text owned by Amazon's rendered delivery-location anchors."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.location_fragments: list[str] = []
        self._stack: list[tuple[str, bool, bool]] = []
        self._active_anchor_count = 0
        self._ignored_content_count = 0

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        normalized_tag = tag.lower()
        normalized_attrs = {
            name.lower(): value for name, value in attrs if value is not None
        }
        starts_anchor = normalized_attrs.get("id", "").lower() in _LOCATION_ANCHOR_IDS
        ignores_content = normalized_tag in _IGNORED_LOCATION_CONTENT_TAGS
        if starts_anchor:
            self._active_anchor_count += 1
        if ignores_content:
            self._ignored_content_count += 1
        self._stack.append((normalized_tag, starts_anchor, ignores_content))
        if self._active_anchor_count and not self._ignored_content_count:
            self.location_fragments.extend(
                value
                for name, value in normalized_attrs.items()
                if name in _LOCATION_TEXT_ATTRIBUTES
            )

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        normalized_tag = tag.lower()
        while self._stack:
            stack_tag, starts_anchor, ignores_content = self._stack.pop()
            if starts_anchor:
                self._active_anchor_count -= 1
            if ignores_content:
                self._ignored_content_count -= 1
            if stack_tag == normalized_tag:
                break

    def handle_data(self, data: str) -> None:
        if self._active_anchor_count and not self._ignored_content_count:
            self.location_fragments.append(data)


def _page_hostname(page: object) -> str | None:
    """Return only the post-navigation hostname; never retain query or credential material."""
    try:
        page_url = page.url  # type: ignore[union-attr]
    except Exception:
        return None
    if not isinstance(page_url, str):
        return None
    try:
        return (urlparse(page_url).hostname or "").lower() or None
    except ValueError:
        return None


def _remaining_ms(deadline: float) -> float:
    return max(0.0, (deadline - time.monotonic()) * 1000)


def _remaining_probe_timeout_ms(deadline: float) -> float:
    return min(_WIDGET_PROBE_TIMEOUT_MS, _remaining_ms(deadline))


def _remaining_timeout_ms(deadline: float, *, cap_ms: float) -> float:
    return min(cap_ms, _remaining_ms(deadline))


def _wait_for_delivery_zip(page: object, delivery_zip: str, deadline: float) -> bool:
    poll_deadline = min(
        deadline,
        time.monotonic() + (_WIDGET_PROBE_TIMEOUT_MS / 1000),
    )
    while time.monotonic() < poll_deadline:
        remaining_ms = max(0.0, (poll_deadline - time.monotonic()) * 1000)
        try:
            visible_text = page.locator("body").inner_text(
                timeout=min(500, remaining_ms)
            )
            if delivery_zip in visible_text:
                return True
        except Exception:
            pass
        pause_ms = min(_POST_APPLY_POLL_MS, max(0.0, remaining_ms))
        if pause_ms > 0:
            page.wait_for_timeout(pause_ms)  # type: ignore[union-attr]
    return False
