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

from dataclasses import dataclass, field
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlparse

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

_AMAZON_GRID_NEXT_SELECTOR = "a.s-pagination-next"
_AMAZON_GRID_PAGE_CHANGE_POLL_MS = 150
_AMAZON_GRID_PAGE_CHANGE_TIMEOUT_MS = 10_000
_AMAZON_GRID_PAGE_POPULATION_POLL_MS = 250
_AMAZON_GRID_PAGE_POPULATION_TIMEOUT_MS = 10_000
_AMAZON_GRID_STABLE_POPULATION_POLLS = 3
_AMAZON_GRID_CARD_OPEN_RE = re.compile(
    r"<div\b(?=[^>]*\bdata-component-type=[\"']s-search-result[\"'])"
    r"(?P<attrs>[^>]*)>",
    flags=re.IGNORECASE,
)
_AMAZON_GRID_TERMINAL_RE = re.compile(
    r"<(?:span|a)\b(?=[^>]*\bs-pagination-next\b)"
    r"(?=[^>]*\bs-pagination-disabled\b)[^>]*>",
    flags=re.IGNORECASE,
)
_AMAZON_GRID_RANGE_RE = re.compile(
    r"(?<!\d)(?P<start>\d[\d,]*)\s*[-\u2013]\s*(?P<end>\d[\d,]*)"
    r"\s+of\s+(?:over\s+)?(?P<total>\d[\d,]*)\s+results?\s+for\b",
    flags=re.IGNORECASE,
)
_AMAZON_GRID_SCRIPT_OR_STYLE_RE = re.compile(
    r"<(?P<tag>script|style)\b[^>]*>.*?</(?P=tag)\s*>",
    flags=re.IGNORECASE | re.DOTALL,
)
_AMAZON_GRID_PAGINATION_RE = re.compile(
    r"<(?:span|a)\b[^>]*\bclass=[\"'][^\"']*\bs-pagination-next\b[^\"']*[\"']",
    flags=re.IGNORECASE,
)


@dataclass(frozen=True)
class _AmazonGridPopulation:
    rendered_dom: str
    card_count: int
    page_asins: list[str]
    result_range: dict[str, int] | None
    stable: bool
    stable_polls: int
    pagination_control_reached: bool
    observed_card_counts: list[int]
    observed_valid_asin_counts: list[int]


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


@dataclass
class AmazonSearchGridPlugin:
    """Capture a caller-sized consecutive Amazon search-result window in one tab."""

    target_url: str
    page_count: int = 2
    delivery_zip: str | None = None
    setup_timeout_seconds: float = 30.0
    traversal_timeout_seconds: float = 60.0
    _grid_page_doms: list[str] = field(default_factory=list, init=False, repr=False)
    _grid_page_urls: list[str] = field(default_factory=list, init=False, repr=False)
    _grid_population_observations: list[dict[str, object]] = field(
        default_factory=list, init=False, repr=False
    )
    _grid_observation: dict[str, object] = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.page_count <= 0:
            raise ValueError("amazon_grid_page_count must be greater than zero")
        if self.setup_timeout_seconds <= 0:
            raise ValueError("delivery_zip_setup_timeout_seconds must be greater than zero")
        if self.traversal_timeout_seconds <= 0:
            raise ValueError("Amazon grid traversal timeout must be greater than zero")
        requested_query = _amazon_grid_query(self.target_url)
        if requested_query is None:
            raise ValueError("Amazon search-grid capture requires a non-empty /s?k= query")

    @property
    def humanize(self) -> bool:
        return True

    @property
    def setup_timeout_ms(self) -> float:
        return self.setup_timeout_seconds * 1000

    @property
    def grid_page_doms(self) -> tuple[str, ...]:
        return tuple(self._grid_page_doms)

    @property
    def grid_page_urls(self) -> tuple[str, ...]:
        return tuple(self._grid_page_urls)

    @property
    def grid_observation(self) -> dict[str, object]:
        return dict(self._grid_observation)

    def _delivery_plugin(self) -> AmazonDeliveryLocationPlugin | None:
        if self.delivery_zip is None:
            return None
        return AmazonDeliveryLocationPlugin(
            delivery_zip=self.delivery_zip,
            setup_timeout_seconds=self.setup_timeout_seconds,
        )

    def before(self, page: object, *, setup_timeout_ms: float) -> PreCaptureOutcome:
        delivery_plugin = self._delivery_plugin()
        if delivery_plugin is None:
            return PreCaptureOutcome(attempted=False, steps_completed=True)
        return delivery_plugin.before(page, setup_timeout_ms=setup_timeout_ms)

    def confirm(self, rendered_dom: str) -> PinConfirmation:
        delivery_plugin = self._delivery_plugin()
        if delivery_plugin is not None:
            return delivery_plugin.confirm(rendered_dom)
        confirmed = _amazon_us_marketplace_observed(rendered_dom)
        return PinConfirmation(
            confirmed=confirmed,
            detail=(
                "amazon.com US-marketplace marker observed; no delivery ZIP was requested"
                if confirmed
                else "amazon.com US-marketplace marker was not observed"
            ),
        )

    def note(self, outcome: PreCaptureOutcome, confirmation: PinConfirmation) -> str:
        delivery_plugin = self._delivery_plugin()
        if delivery_plugin is not None:
            return delivery_plugin.note(outcome, confirmation)
        return (
            "amazon_grid_location_binding: US marketplace observed; delivery ZIP NOT REQUESTED; "
            "price and fulfilment remain bound only to the preserved page state"
            if confirmation.confirmed
            else "amazon_grid_location_binding: US marketplace NOT CONFIRMED; delivery ZIP NOT REQUESTED"
        )

    def describe(self) -> dict[str, object]:
        delivery_plugin = self._delivery_plugin()
        location = (
            delivery_plugin.describe()
            if delivery_plugin is not None
            else {
                "pre_capture": "amazon_search_grid",
                "delivery_zip_requested": None,
                "amazon_grid_location_binding": "us_marketplace_only",
            }
        )
        return {
            **location,
            "amazon_grid_requested_page_count": self.page_count,
            **self._grid_observation,
        }

    def before_snapshot(
        self, page: object, *, setup_timeout_ms: float
    ) -> PreCaptureOutcome:
        del setup_timeout_ms
        deadline = time.monotonic() + self.traversal_timeout_seconds
        requested_query = _amazon_grid_query(self.target_url)
        assert requested_query is not None
        seen_asins: set[str] = set()
        placement_count = 0
        range_observations: list[dict[str, int]] = []
        termination = "unproven"

        try:
            for expected_page in range(1, self.page_count + 1):
                rendered_dom = page.content()  # type: ignore[union-attr]
                page_url = str(page.url)  # type: ignore[union-attr]
                if _amazon_error_shell_observed(rendered_dom):
                    return self._grid_failed(
                        reason="amazon_error_shell",
                        detail=(
                            f"Amazon grid page {expected_page} returned the retailer's "
                            "Sorry/500/503 error shell"
                        ),
                        placement_count=placement_count,
                        unique_count=len(seen_asins),
                        range_observations=range_observations,
                    )
                hostname = (urlparse(page_url).hostname or "").lower()
                if hostname not in _AMAZON_US_HOSTS:
                    return self._grid_failed(
                        reason="wrong_marketplace_host",
                        detail=f"Amazon grid page {expected_page} landed on {hostname or 'unknown'!r}",
                        placement_count=placement_count,
                        unique_count=len(seen_asins),
                        range_observations=range_observations,
                    )
                if not _amazon_us_marketplace_observed(rendered_dom):
                    return self._grid_failed(
                        reason="us_marketplace_unconfirmed",
                        detail=f"Amazon grid page {expected_page} exposed no US-marketplace marker",
                        placement_count=placement_count,
                        unique_count=len(seen_asins),
                        range_observations=range_observations,
                    )
                observed_query = _amazon_grid_query(page_url)
                if _normalize_query(observed_query) != _normalize_query(requested_query):
                    return self._grid_failed(
                        reason="query_binding_mismatch",
                        detail=(
                            f"Amazon grid page {expected_page} query {observed_query!r} did not "
                            f"match requested query {requested_query!r}"
                        ),
                        placement_count=placement_count,
                        unique_count=len(seen_asins),
                        range_observations=range_observations,
                    )
                observed_page = _amazon_grid_page_number(page_url)
                if observed_page != expected_page:
                    return self._grid_failed(
                        reason="page_discontinuity",
                        detail=(
                            f"Amazon grid expected page {expected_page} but URL encoded "
                            f"page {observed_page}"
                        ),
                        placement_count=placement_count,
                        unique_count=len(seen_asins),
                        range_observations=range_observations,
                    )

                population = _wait_for_amazon_grid_page_population(
                    page,
                    initial_dom=rendered_dom,
                    traversal_deadline=deadline,
                )
                rendered_dom = population.rendered_dom
                card_count = population.card_count
                page_asins = population.page_asins
                page_range = population.result_range
                settled_page_url = str(page.url)  # type: ignore[union-attr]
                settled_hostname = (urlparse(settled_page_url).hostname or "").lower()
                if (
                    settled_hostname not in _AMAZON_US_HOSTS
                    or _normalize_query(_amazon_grid_query(settled_page_url))
                    != _normalize_query(requested_query)
                    or _amazon_grid_page_number(settled_page_url) != expected_page
                ):
                    return self._grid_failed(
                        reason="page_binding_changed_during_population_wait",
                        detail=(
                            f"Amazon grid page {expected_page} changed host, query, or page "
                            "binding while its displayed result range populated"
                        ),
                        placement_count=placement_count,
                        unique_count=len(seen_asins),
                        range_observations=range_observations,
                    )
                page_url = settled_page_url
                if not page_asins or len(page_asins) != card_count:
                    return self._grid_failed(
                        reason="product_identity_absent",
                        detail=(
                            f"Amazon grid page {expected_page} exposed {card_count} ranked cards "
                            f"but {len(page_asins)} valid ASIN identities"
                        ),
                        placement_count=placement_count,
                        unique_count=len(seen_asins),
                        range_observations=range_observations,
                    )
                if page_range is None:
                    return self._grid_failed(
                        reason="result_range_absent",
                        detail=f"Amazon grid page {expected_page} exposed no ranked result range",
                        placement_count=placement_count,
                        unique_count=len(seen_asins),
                        range_observations=range_observations,
                    )
                displayed_slot_count = page_range["end"] - page_range["start"] + 1
                self._grid_population_observations.append(
                    {
                        "page": expected_page,
                        "source_visible_placement_count": card_count,
                        "displayed_result_range_slot_count": displayed_slot_count,
                        "stable_population_polls": population.stable_polls,
                        "population_stable": population.stable,
                        "pagination_control_reached": population.pagination_control_reached,
                        "observed_card_counts": population.observed_card_counts,
                        "observed_valid_asin_counts": (
                            population.observed_valid_asin_counts
                        ),
                    }
                )
                if not population.stable:
                    population_gap = (
                        "did not expose a stable valid-card population after reaching the "
                        "pagination region"
                        if population.pagination_control_reached
                        else "did not expose a reachable pagination region"
                    )
                    return self._grid_failed(
                        reason="page_population_unproven",
                        detail=f"Amazon grid page {expected_page} {population_gap}",
                        placement_count=placement_count,
                        unique_count=len(seen_asins),
                        range_observations=range_observations,
                    )
                if range_observations and (
                    page_range["start"] <= range_observations[-1]["start"]
                    or page_range["end"] <= range_observations[-1]["end"]
                ):
                    return self._grid_failed(
                        reason="result_range_discontinuity",
                        detail=(
                            f"Amazon grid page {expected_page} range did not advance: "
                            f"previous={range_observations[-1]}, current={page_range}"
                        ),
                        placement_count=placement_count,
                        unique_count=len(seen_asins),
                        range_observations=range_observations,
                    )

                self._grid_page_doms.append(rendered_dom)
                self._grid_page_urls.append(page_url)
                range_observations.append(page_range)
                placement_count += len(page_asins)
                seen_asins.update(page_asins)
                if expected_page == self.page_count:
                    termination = "requested_page_window_reconciled"
                    break

                next_link = page.locator(_AMAZON_GRID_NEXT_SELECTOR).first  # type: ignore[union-attr]
                try:
                    next_link.wait_for(
                        state="visible",
                        timeout=min(5_000, _grid_required_remaining_ms(deadline)),
                    )
                except Exception:
                    if _AMAZON_GRID_TERMINAL_RE.search(rendered_dom):
                        termination = "retailer_terminal_reconciled"
                        break
                    return self._grid_failed(
                        reason="next_page_control_unavailable",
                        detail=(
                            f"Amazon grid page {expected_page} ended before the requested "
                            f"{self.page_count}-page window and exposed no terminal control"
                        ),
                        placement_count=placement_count,
                        unique_count=len(seen_asins),
                        range_observations=range_observations,
                    )
                previous_asins = tuple(page_asins)
                next_link.scroll_into_view_if_needed(
                    timeout=min(5_000, _grid_required_remaining_ms(deadline))
                )
                next_link.click(timeout=min(5_000, _grid_required_remaining_ms(deadline)))
                change_deadline = min(
                    deadline,
                    time.monotonic() + _AMAZON_GRID_PAGE_CHANGE_TIMEOUT_MS / 1000,
                )
                while time.monotonic() < change_deadline:
                    page.wait_for_timeout(  # type: ignore[union-attr]
                        min(_AMAZON_GRID_PAGE_CHANGE_POLL_MS, _grid_remaining_ms(change_deadline))
                    )
                    current_url = str(page.url)  # type: ignore[union-attr]
                    _, current_asins = _amazon_grid_card_asins(
                        page.content()  # type: ignore[union-attr]
                    )
                    if (
                        _amazon_grid_page_number(current_url) == expected_page + 1
                        and current_asins
                        and tuple(current_asins) != previous_asins
                    ):
                        break
                else:
                    return self._grid_failed(
                        reason="next_page_did_not_advance",
                        detail=f"Amazon grid did not advance after page {expected_page}",
                        placement_count=placement_count,
                        unique_count=len(seen_asins),
                        range_observations=range_observations,
                    )
        except Exception as exc:
            return self._grid_failed(
                reason="grid_traversal_failed",
                detail=f"Amazon grid traversal failed ({type(exc).__name__}: {exc})",
                placement_count=placement_count,
                unique_count=len(seen_asins),
                range_observations=range_observations,
            )

        self._grid_observation = {
            "amazon_grid_requested_page_count": self.page_count,
            "amazon_grid_captured_page_count": len(self._grid_page_doms),
            "amazon_grid_extracted_unique_parent_count": len(seen_asins),
            "amazon_grid_extracted_placement_count": placement_count,
            "amazon_grid_duplicate_placement_count": placement_count - len(seen_asins),
            "amazon_grid_result_range_observations": range_observations,
            "amazon_grid_population_observations": list(
                self._grid_population_observations
            ),
            "amazon_grid_termination": termination,
            "amazon_grid_requested_query": requested_query,
        }
        return PreCaptureOutcome(attempted=True, steps_completed=True)

    def _grid_failed(
        self,
        *,
        reason: str,
        detail: str,
        placement_count: int,
        unique_count: int,
        range_observations: list[dict[str, int]],
    ) -> PreCaptureOutcome:
        self._grid_observation = {
            "amazon_grid_requested_page_count": self.page_count,
            "amazon_grid_captured_page_count": len(self._grid_page_doms),
            "amazon_grid_extracted_unique_parent_count": unique_count,
            "amazon_grid_extracted_placement_count": placement_count,
            "amazon_grid_duplicate_placement_count": placement_count - unique_count,
            "amazon_grid_result_range_observations": list(range_observations),
            "amazon_grid_population_observations": list(
                self._grid_population_observations
            ),
            "amazon_grid_termination": "unproven",
            "amazon_grid_failure": detail,
        }
        return PreCaptureOutcome(
            attempted=True,
            steps_completed=False,
            reason=reason,
            warning_notes=[f"amazon_grid_traversal: {detail}"],
        )


def _amazon_us_marketplace_observed(rendered_dom: str) -> bool:
    return any(marker in rendered_dom for marker in _US_MARKETPLACE_MARKERS)


def _amazon_error_shell_observed(rendered_dom: str) -> bool:
    folded = rendered_dom.casefold()
    return (
        "sorry! something went wrong!" in folded
        and ("cs_503" in folded or "500_503.png" in folded)
    )


def _amazon_grid_query(url: str) -> str | None:
    values = parse_qs(urlparse(url).query).get("k", [])
    value = values[0].strip() if values else ""
    return value or None


def _normalize_query(value: str | None) -> str:
    return " ".join((value or "").casefold().split())


def _amazon_grid_page_number(url: str) -> int | None:
    values = parse_qs(urlparse(url).query).get("page", [])
    if not values:
        return 1
    try:
        page = int(values[0])
    except (TypeError, ValueError):
        return None
    return page if page > 0 else None


def _amazon_grid_card_asins(rendered_dom: str) -> tuple[int, list[str]]:
    matches = list(_AMAZON_GRID_CARD_OPEN_RE.finditer(rendered_dom))
    asins: list[str] = []
    for match in matches:
        asin = re.search(
            r"\bdata-asin=[\"']([A-Z0-9]{10})[\"']",
            match.group("attrs"),
        )
        if asin is not None:
            asins.append(asin.group(1).upper())
    return len(matches), asins


def _amazon_grid_range(rendered_dom: str) -> dict[str, int] | None:
    # Script and style bodies survive tag stripping as ordinary text. The projection
    # reads the displayed range from script-free text, so stripping them here keeps
    # the traversal gate and the admitted record reading the same retailer fact
    # instead of letting serialized page state decide when the window is filled.
    visible_text = re.sub(
        r"<[^>]+>", " ", _AMAZON_GRID_SCRIPT_OR_STYLE_RE.sub(" ", rendered_dom)
    )
    match = _AMAZON_GRID_RANGE_RE.search(visible_text)
    if match is None:
        return None
    return {
        key: int(match.group(key).replace(",", ""))
        for key in ("start", "end", "total")
    }


def _wait_for_amazon_grid_page_population(
    page: object,
    *,
    initial_dom: str,
    traversal_deadline: float,
) -> _AmazonGridPopulation:
    """Reach the page footer, then require a stable valid-card population."""

    population_deadline = min(
        traversal_deadline,
        time.monotonic() + _AMAZON_GRID_PAGE_POPULATION_TIMEOUT_MS / 1000,
    )
    rendered_dom = initial_dom
    pagination_control_reached = False
    stable_population_polls = 0
    previous_population: tuple[int, int] | None = None
    observed_card_counts: list[int] = []
    observed_valid_asin_counts: list[int] = []
    while True:
        if not pagination_control_reached:
            try:
                page.evaluate(  # type: ignore[union-attr]
                    "window.scrollTo(0, document.body.scrollHeight)"
                )
                rendered_dom = page.content()  # type: ignore[union-attr]
                pagination_control_reached = bool(
                    _AMAZON_GRID_PAGINATION_RE.search(rendered_dom)
                )
            except Exception:
                # Retry while the page hydrates. Absence is adjudicated after
                # population: disabled proves terminal; missing continuation fails.
                pass
        card_count, page_asins = _amazon_grid_card_asins(rendered_dom)
        observed_card_counts.append(card_count)
        observed_valid_asin_counts.append(len(page_asins))
        page_range = _amazon_grid_range(rendered_dom)
        population_observed = (
            pagination_control_reached
            and page_range is not None
            and card_count > 0
            and len(page_asins) == card_count
        )
        current_population = (card_count, len(page_asins))
        if population_observed and current_population == previous_population:
            stable_population_polls += 1
        elif population_observed:
            stable_population_polls = 1
        else:
            stable_population_polls = 0
        if stable_population_polls >= _AMAZON_GRID_STABLE_POPULATION_POLLS:
            return _AmazonGridPopulation(
                rendered_dom=rendered_dom,
                card_count=card_count,
                page_asins=page_asins,
                result_range=page_range,
                stable=True,
                stable_polls=stable_population_polls,
                pagination_control_reached=pagination_control_reached,
                observed_card_counts=observed_card_counts,
                observed_valid_asin_counts=observed_valid_asin_counts,
            )
        if time.monotonic() >= population_deadline:
            return _AmazonGridPopulation(
                rendered_dom=rendered_dom,
                card_count=card_count,
                page_asins=page_asins,
                result_range=page_range,
                stable=False,
                stable_polls=stable_population_polls,
                pagination_control_reached=pagination_control_reached,
                observed_card_counts=observed_card_counts,
                observed_valid_asin_counts=observed_valid_asin_counts,
            )
        previous_population = current_population
        page.wait_for_timeout(  # type: ignore[union-attr]
            min(
                _AMAZON_GRID_PAGE_POPULATION_POLL_MS,
                _grid_remaining_ms(population_deadline),
            )
        )
        rendered_dom = page.content()  # type: ignore[union-attr]


def _grid_remaining_ms(deadline: float) -> int:
    return max(0, int((deadline - time.monotonic()) * 1000))


def _grid_required_remaining_ms(deadline: float) -> int:
    remaining = _grid_remaining_ms(deadline)
    if remaining <= 0:
        raise TimeoutError("Amazon grid traversal window exhausted")
    return remaining


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
