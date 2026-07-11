"""Amazon-specific delivery-location pre-capture plugin for the CloakBrowser adapter.

This is the ONE place Amazon-specific knowledge lives: the delivery-location widget flow,
the US-storefront confirmation signal, and the operator-facing limitation wording. The
generic ``cloakbrowser_snapshot`` adapter knows none of it -- it only calls this plugin
through the ``PreCapturePlugin`` seam (``before`` / ``confirm`` / ``describe`` / ``note``).

The honesty keystone: setting the ZIP via clicks is an ATTEMPT, never proof. The packet
records the storefront as pinned ONLY when ``confirm`` observes a US signal in the rendered
DOM (recon proved ``currencyOfPreference="USD"`` appears after a US ZIP is applied). When the
signal is absent, the note says ATTEMPTED-but-NOT-confirmed and the slot is treated as
un-pinned -- never a fake "set" claim that could let a non-US capture count as a US one (INV-1).
"""

from __future__ import annotations

import re
import time

from dataclasses import dataclass

from source_capture.adapters.cloakbrowser_snapshot import (
    PinConfirmation,
    PreCaptureOutcome,
)


# Homepage whose delivery-location widget pins the storefront. The main capture URL is a
# separate PDP; this navigation happens BEFORE it, inside the plugin's bounded setup window.
_AMAZON_HOMEPAGE_URL = "https://www.amazon.com/"

# Short bounded probes replace fixed sleeps: browser actions already wait for their target,
# while the post-apply poll returns as soon as Amazon renders the requested ZIP.
_POST_APPLY_POLL_MS = 100
_WIDGET_PROBE_TIMEOUT_MS = 2500

# Widget selectors, probed on amazon.com 2026-06-16; subject to Amazon DOM changes.
_WIDGET_OPEN_SELECTORS = (
    "#nav-global-location-popover-link",
    "#glow-ingress-block",
)
_ZIP_INPUT_SELECTORS = ("#GLUXZipUpdateInput", "input[id*='zip' i][type='text']")
_APPLY_SELECTORS = ("#GLUXZipUpdate", "span.a-button-inner > input[type='submit']")

# The US-storefront signal recon proved appears in the rendered DOM once a US ZIP is applied.
_INPUT_TAG_PATTERN = re.compile(r"<input\b[^>]*>", re.IGNORECASE)
_ATTR_PATTERN = re.compile(r"""([^\s=/>]+)\s*=\s*(['"])(.*?)\2""", re.IGNORECASE)


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

        # Step 2: open the delivery-location widget. FIX #4: a short probe click, no is_visible.
        widget_clicked = False
        for selector in _WIDGET_OPEN_SELECTORS:
            probe_ms = _remaining_probe_timeout_ms(setup_deadline)
            if probe_ms <= 0:
                break
            try:
                page.locator(selector).first.click(timeout=probe_ms)  # type: ignore[union-attr]
                widget_clicked = True
                break
            except Exception:
                continue
        if not widget_clicked:
            warning_notes.append(
                "delivery_zip_setup: could not click delivery location widget; "
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


def confirm_us_storefront(rendered_dom: str) -> PinConfirmation:
    """Confirm the rendered DOM shows a US storefront after the delivery-location pin attempt.

    Confirmed iff the recon-proven ``currencyOfPreference="USD"`` signal is present as an input
    value. Dollar-looking prices are deliberately not a confirmation signal: they can appear in
    scripts, cached data, alternate-market markup, or non-storefront page fragments. Otherwise
    NOT confirmed, with a detail naming what was missing. This is the post-capture source of
    truth for the packet's pin_confirmed flag and the honesty of the note -- clicks alone never
    confirm.
    """
    dom = rendered_dom or ""
    if _has_us_currency_dom_signal(dom):
        return PinConfirmation(
            confirmed=True,
            detail='currencyOfPreference="USD" observed in rendered DOM',
        )
    return PinConfirmation(
        confirmed=False,
        detail=(
            'no US storefront signal (currencyOfPreference="USD" absent as a rendered input '
            "value) in rendered DOM"
        ),
    )


def confirm_us_storefront_with_zip(
    rendered_dom: str, *, delivery_zip: str
) -> PinConfirmation:
    """Confirm a US target surface using currency or a ZIP-bound marketplace anchor."""
    currency_confirmation = confirm_us_storefront(rendered_dom)
    if currency_confirmation.confirmed:
        return currency_confirmation
    if _has_us_delivery_zip_dom_signal(rendered_dom or "", delivery_zip):
        return PinConfirmation(
            confirmed=True,
            detail=(
                f"delivery ZIP {delivery_zip!r} and amazon.com US-marketplace markers "
                "observed in rendered DOM"
            ),
        )
    return PinConfirmation(
        confirmed=False,
        detail=(
            'no US storefront signal (currencyOfPreference="USD" or delivery ZIP '
            f"{delivery_zip!r} absent from recognized rendered-DOM anchors)"
        ),
    )


def _has_us_currency_dom_signal(dom: str) -> bool:
    """Return True only for a rendered input carrying currencyOfPreference=USD."""
    for input_tag in _INPUT_TAG_PATTERN.findall(dom):
        attrs = {
            match.group(1).lower(): match.group(3)
            for match in _ATTR_PATTERN.finditer(input_tag)
        }
        if (
            attrs.get("name") == "currencyOfPreference"
            and attrs.get("value", "").upper() == "USD"
        ):
            return True
    return False


def _has_us_delivery_zip_dom_signal(dom: str, delivery_zip: str) -> bool:
    location_anchor = re.search(
        (
            r'id=["\'](?:glow-ingress-line2|glow-ingress-block)["\'][^>]*>'
            rf'.{{0,1000}}?{re.escape(delivery_zip)}'
        ),
        dom,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if location_anchor is None:
        return False
    normalized = dom.lower()
    return any(
        marker in normalized
        for marker in (
            "ue_sn = 'www.amazon.com'",
            "retail:prod:www.amazon.com",
            "assoc_handle=usflex",
        )
    )


def _remaining_ms(deadline: float) -> float:
    return max(0.0, (deadline - time.monotonic()) * 1000)


def _remaining_probe_timeout_ms(deadline: float) -> float:
    return min(_WIDGET_PROBE_TIMEOUT_MS, _remaining_ms(deadline))


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
