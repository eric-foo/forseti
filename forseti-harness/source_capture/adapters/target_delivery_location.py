"""Target public shipping-ZIP setup and fail-closed rendered confirmation."""

from __future__ import annotations

import html
import json
import re
import time
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Any, Iterator
from urllib.parse import urlparse

from source_capture.adapters.cloakbrowser_snapshot import (
    PinConfirmation,
    PreCaptureOutcome,
)


_TARGET_HOSTS = frozenset({"target.com", "www.target.com"})
_ZIP_CONTROL_SELECTOR = "#zip-code-id-btn"
_ZIP_INPUT_SELECTORS = (
    'input[data-test="@web/ZipCodeInput/Input"]:visible',
    '[role="dialog"] input[id*="zip" i]:visible',
    '[role="dialog"] input[name*="zip" i]:visible',
    '[role="dialog"] input[aria-label*="zip" i]:visible',
    '[role="dialog"] input[placeholder*="zip" i]:visible',
    '[data-test*="ZipCode"] input:visible',
)
_ZIP_APPLY_SELECTORS = (
    'button[data-test="@web/ZipCodeInput/SubmitButton"]:visible',
    '[role="dialog"] button:visible:has-text("Save")',
    '[role="dialog"] button:visible:has-text("Apply")',
    '[data-test*="ZipCode"] button:visible:has-text("Save")',
    '[data-test*="ZipCode"] button:visible:has-text("Apply")',
)
_CONTROL_READINESS_TIMEOUT_MS = 10_000
_CONTROL_POLL_MS = 100
_POST_APPLY_TIMEOUT_MS = 5_000
_FIVE_DIGIT_ZIP = re.compile(r"^\d{5}$")


@dataclass
class TargetDeliveryLocationPlugin:
    """Attempt Target's public shipping-ZIP flow, then verify retailer-owned state."""

    target_url: str
    delivery_zip: str
    setup_timeout_seconds: float = 30.0
    _setup_completed: bool = field(default=False, init=False, repr=False)
    _observed_context: dict[str, object] = field(
        default_factory=dict, init=False, repr=False
    )

    def __post_init__(self) -> None:
        parsed = urlparse(self.target_url)
        if (
            parsed.scheme != "https"
            or (parsed.hostname or "").lower() not in _TARGET_HOSTS
        ):
            raise ValueError(
                "Target delivery preference requires an HTTPS target.com URL"
            )
        if _FIVE_DIGIT_ZIP.fullmatch(self.delivery_zip) is None:
            raise ValueError("Target delivery ZIP must contain exactly five digits")
        if self.setup_timeout_seconds <= 0:
            raise ValueError("Target setup timeout must be greater than zero")

    @property
    def humanize(self) -> bool:
        return True

    @property
    def setup_timeout_ms(self) -> float:
        return self.setup_timeout_seconds * 1000

    def before(self, page: object, *, setup_timeout_ms: float) -> PreCaptureOutcome:
        deadline = time.monotonic() + setup_timeout_ms / 1000
        try:
            page.goto(  # type: ignore[union-attr]
                self.target_url,
                wait_until="domcontentloaded",
                timeout=_required_remaining_ms(deadline),
            )
        except Exception as exc:
            return _failed_outcome(
                "navigate_setup_surface",
                f"Target setup surface did not reach domcontentloaded ({type(exc).__name__})",
            )

        control = page.locator(_ZIP_CONTROL_SELECTOR)  # type: ignore[union-attr]
        try:
            readiness_timeout_ms = min(
                _CONTROL_READINESS_TIMEOUT_MS,
                _required_remaining_ms(deadline),
            )
            control.wait_for(state="visible", timeout=readiness_timeout_ms)
        except Exception:
            return _failed_outcome(
                "wait_for_zip_control",
                "Target public ZIP control did not become visible within the bounded readiness wait",
            )
        try:
            control.click(timeout=_required_remaining_ms(deadline))
        except Exception:
            return _failed_outcome(
                "open_zip_control",
                "Target public ZIP control became visible but could not be opened",
            )

        zip_input = _first_visible_locator(page, _ZIP_INPUT_SELECTORS, deadline)
        if zip_input is None:
            return _failed_outcome(
                "find_zip_input",
                "Target ZIP dialog did not expose a recognized visible ZIP input",
            )
        try:
            zip_input.fill(
                self.delivery_zip,
                timeout=_required_remaining_ms(deadline),
            )
        except Exception:
            return _failed_outcome(
                "fill_zip_input",
                "Target ZIP input could not be filled through the public retailer UI",
            )

        apply_button = _first_visible_locator(page, _ZIP_APPLY_SELECTORS, deadline)
        warning_notes: list[str] = []
        if apply_button is None:
            try:
                zip_input.press(
                    "Enter",
                    timeout=_required_remaining_ms(deadline),
                )
                warning_notes.append(
                    "target_zip_setup: no recognized visible Save or Apply control was "
                    "present; submitted the already-scoped public ZIP input with Enter, "
                    "and final Target header confirmation remains authoritative"
                )
            except Exception:
                return _failed_outcome(
                    "apply_zip",
                    "Target ZIP dialog exposed no recognized action and the scoped input "
                    "could not be submitted with Enter",
                )
        else:
            try:
                apply_button.click(timeout=_required_remaining_ms(deadline))
            except Exception:
                return _failed_outcome(
                    "apply_zip",
                    "Target ZIP dialog action could not be applied",
                )

        expected_label = f"Ship to location: {self.delivery_zip}"
        expected_text = f"Ship to {self.delivery_zip}"
        poll_deadline = min(
            deadline, time.monotonic() + _POST_APPLY_TIMEOUT_MS / 1000
        )
        while time.monotonic() < poll_deadline:
            try:
                label = control.get_attribute(
                    "aria-label",
                    timeout=min(500, _required_remaining_ms(poll_deadline)),
                )
                child_text = control.locator(
                    '[data-test="@web/ZipCodeButton/ZipCodeNumber"]'
                ).inner_text(
                    timeout=min(500, _required_remaining_ms(poll_deadline))
                )
                if label == expected_label and child_text.strip() == expected_text:
                    self._setup_completed = True
                    return PreCaptureOutcome(
                        attempted=True,
                        steps_completed=True,
                        warning_notes=warning_notes,
                    )
            except Exception:
                pass
            pause_ms = min(_CONTROL_POLL_MS, _remaining_ms(poll_deadline))
            if pause_ms > 0:
                page.wait_for_timeout(pause_ms)  # type: ignore[union-attr]
        return _failed_outcome(
            "confirm_applied_header",
            "Target shipping header did not bind the requested ZIP after the public UI action",
        )

    def confirm(self, rendered_dom: str) -> PinConfirmation:
        confirmation, context = confirm_target_us_delivery_zip(
            rendered_dom,
            delivery_zip=self.delivery_zip,
            setup_completed=self._setup_completed,
        )
        self._observed_context = context
        return confirmation

    def describe(self) -> dict[str, object]:
        return {
            "pre_capture": "target_delivery_location",
            "delivery_zip_requested": self.delivery_zip,
            "target_zip_setup_url": self.target_url,
            "target_store_context_posture": (
                "retailer_store_or_pickup_context_not_delivery_zip"
            ),
            **self._observed_context,
        }

    def note(self, outcome: PreCaptureOutcome, confirmation: PinConfirmation) -> str:
        store_zip = self._observed_context.get("target_primary_store_zip")
        server_zip = self._observed_context.get("target_server_location_zip")
        store_context = (
            f"; server/store ZIP context remained {server_zip!r}/{store_zip!r}"
            if server_zip is not None or store_zip is not None
            else ""
        )
        if confirmation.confirmed:
            return (
                "declared_delivery_zip: Target shipping ZIP "
                f"{self.delivery_zip!r} CONFIRMED ({confirmation.detail})"
                f"{store_context}; store/pickup ZIP is an independent context"
            )
        reason = confirmation.detail
        if not outcome.steps_completed and outcome.reason is not None:
            reason = f"retailer UI step failed: {outcome.reason}; {reason}"
        return (
            "declared_delivery_zip: Target shipping ZIP "
            f"{self.delivery_zip!r} ATTEMPTED but NOT confirmed ({reason})"
            f"{store_context}; treat delivery location as un-pinned"
        )


def confirm_target_us_delivery_zip(
    rendered_dom: str,
    *,
    delivery_zip: str,
    setup_completed: bool,
) -> tuple[PinConfirmation, dict[str, object]]:
    """Require completed UI setup, exact shipping labels, and Target-owned US state."""
    parser = _TargetZipHeaderParser()
    try:
        parser.feed(rendered_dom or "")
        parser.close()
    except Exception:
        parser = _TargetZipHeaderParser()

    expected_pair = (
        f"Ship to location: {delivery_zip}",
        f"Ship to {delivery_zip}",
    )
    header_confirmed = bool(parser.pairs) and set(parser.pairs) == {expected_pair}

    location_objects = list(_iter_server_location_variables(rendered_dom or ""))
    countries = {
        location.get("country")
        for item in location_objects
        if isinstance((location := item.get("location")), dict)
        and isinstance(location.get("country"), str)
    }
    country_confirmed = bool(countries) and countries == {"US"}

    context = _observed_target_context(location_objects)
    if setup_completed and header_confirmed and country_confirmed:
        return (
            PinConfirmation(
                confirmed=True,
                detail=(
                    f"public Target ZIP UI completed, exact shipping header bound "
                    f"{delivery_zip}, and serverLocationVariables.location.country=US"
                ),
            ),
            context,
        )

    missing: list[str] = []
    if not setup_completed:
        missing.append("public Target ZIP UI setup did not complete")
    if not header_confirmed:
        missing.append(
            f"header aria-label and ZIP child were not the exact requested {delivery_zip} pair"
        )
    if not country_confirmed:
        missing.append(
            "one consistent serverLocationVariables.location.country=US signal"
        )
    return (
        PinConfirmation(
            confirmed=False,
            detail="required Target shipping/US conjunction absent: " + "; ".join(missing),
        ),
        context,
    )


class _TargetZipHeaderParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.pairs: list[tuple[str, str]] = []
        self._button_depth = 0
        self._button_label: str | None = None
        self._child_depth = 0
        self._child_parts: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        normalized = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "button" and normalized.get("id") == "zip-code-id-btn":
            self._button_depth = 1
            self._button_label = normalized.get("aria-label")
            return
        if self._button_depth:
            self._button_depth += 1
            if (
                normalized.get("data-test")
                == "@web/ZipCodeButton/ZipCodeNumber"
            ):
                self._child_depth = self._button_depth
                self._child_parts = []

    def handle_data(self, data: str) -> None:
        if self._child_depth:
            self._child_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if not self._button_depth:
            return
        if self._child_depth == self._button_depth:
            self._child_depth = 0
        self._button_depth -= 1
        if self._button_depth == 0:
            child_text = " ".join("".join(self._child_parts).split())
            self.pairs.append((self._button_label or "", child_text))
            self._button_label = None
            self._child_parts = []


def _iter_server_location_variables(rendered_dom: str) -> Iterator[dict[str, Any]]:
    decoder = json.JSONDecoder()
    candidates = (
        html.unescape(rendered_dom),
        html.unescape(rendered_dom).replace('\\"', '"'),
    )
    seen: set[str] = set()
    marker = '"serverLocationVariables"'
    for candidate in candidates:
        search_from = 0
        while True:
            marker_index = candidate.find(marker, search_from)
            if marker_index < 0:
                break
            object_start = candidate.find("{", marker_index + len(marker))
            if object_start < 0:
                break
            try:
                value, consumed = decoder.raw_decode(candidate[object_start:])
            except json.JSONDecodeError:
                search_from = marker_index + len(marker)
                continue
            search_from = object_start + consumed
            if not isinstance(value, dict):
                continue
            fingerprint = json.dumps(value, sort_keys=True, default=str)
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            yield value


def _observed_target_context(
    location_objects: list[dict[str, Any]],
) -> dict[str, object]:
    context: dict[str, object] = {}
    if not location_objects:
        return context
    first = location_objects[0]
    server_zip = first.get("zipCode")
    if isinstance(server_zip, str):
        context["target_server_location_zip"] = server_zip
    location = first.get("location")
    if isinstance(location, dict):
        nested_zip = location.get("zipCode")
        if isinstance(nested_zip, str):
            context["target_nested_location_zip"] = nested_zip
        country = location.get("country")
        if isinstance(country, str):
            context["target_nested_location_country"] = country
    primary_store = first.get("primaryStore")
    if isinstance(primary_store, dict):
        store_name = primary_store.get("storeName")
        store_zip = primary_store.get("zipCode")
        if isinstance(store_name, str):
            context["target_primary_store_name"] = store_name
        if isinstance(store_zip, str):
            context["target_primary_store_zip"] = store_zip
    return context


def _first_visible_locator(
    page: object, selectors: tuple[str, ...], deadline: float
) -> object | None:
    for selector in selectors:
        timeout_ms = min(1_000, _remaining_ms(deadline))
        if timeout_ms <= 0:
            return None
        locator = page.locator(selector).first  # type: ignore[union-attr]
        try:
            locator.wait_for(state="visible", timeout=timeout_ms)
            return locator
        except Exception:
            continue
    return None


def _failed_outcome(reason: str, detail: str) -> PreCaptureOutcome:
    return PreCaptureOutcome(
        attempted=True,
        steps_completed=False,
        reason=reason,
        warning_notes=[
            f"target_zip_setup: {detail}; main capture proceeds without a confirmed Target delivery pin"
        ],
    )


def _remaining_ms(deadline: float) -> float:
    return max(0.0, (deadline - time.monotonic()) * 1000)


def _required_remaining_ms(deadline: float) -> float:
    remaining_ms = _remaining_ms(deadline)
    if remaining_ms <= 0:
        raise TimeoutError("Target ZIP setup budget exhausted")
    return remaining_ms
