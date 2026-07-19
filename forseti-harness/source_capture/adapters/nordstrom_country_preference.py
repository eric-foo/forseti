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
from datetime import date, datetime, timedelta, timezone
from typing import Literal
from urllib.parse import urlparse

from source_capture.adapters.cloakbrowser_snapshot import (
    PinConfirmation,
    PreCaptureOutcome,
)
from source_capture.projection_shared import first_match


_NORDSTROM_HOMEPAGE_URL = "https://www.nordstrom.com/"
_CONTROL_PROBE_TIMEOUT_MS = 2500
_POST_SELECTION_POLL_MS = 100
_HOMEPAGE_RENDER_SETTLE_MS = 5000
_REVIEW_POSTURE_POLL_MS = 100
_REVIEW_POSTURE_TIMEOUT_MS = 20000
NORDSTROM_REVIEW_WINDOW_DAYS = 30
NORDSTROM_REVIEW_MINIMUM = 6
NORDSTROM_REVIEW_MAXIMUM = 30
NORDSTROM_REVIEW_POSTURES = ("recent_window_30d",)
NordstromReviewPosture = Literal["recent_window_30d"]

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
    setup_timeout_seconds: float = 45.0
    target_url: str | None = None
    review_posture: NordstromReviewPosture | None = None
    review_window_reference_date: date | None = None

    def __post_init__(self) -> None:
        if self.country_code != "US" or self.currency_code != "USD":
            raise ValueError("Nordstrom country preference currently supports only US/USD")
        if self.setup_timeout_seconds <= 0:
            raise ValueError(
                "nordstrom_country_setup_timeout_seconds must be greater than zero"
            )
        if self.target_url is not None:
            hostname = (urlparse(self.target_url).hostname or "").lower()
            if hostname not in {"nordstrom.com", "www.nordstrom.com"}:
                raise ValueError(
                    "Nordstrom country preference target_url must use nordstrom.com"
                )
        if (
            self.review_posture is not None
            and self.review_posture not in NORDSTROM_REVIEW_POSTURES
        ):
            raise ValueError(
                "Nordstrom review posture currently supports only recent_window_30d"
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
            if self.target_url is None:
                return _failed_outcome(
                    "open_country_control",
                    "could not open Nordstrom country preference control",
                )
            try:
                page.goto(  # type: ignore[union-attr]
                    self.target_url,
                    wait_until="domcontentloaded",
                    timeout=_remaining_ms(deadline),
                )
            except Exception as exc:
                return _failed_outcome(
                    "target_navigation",
                    f"target-page country-control fallback navigation failed ({exc})",
                )
            render_settle_ms = min(
                _HOMEPAGE_RENDER_SETTLE_MS, _remaining_ms(deadline)
            )
            if render_settle_ms > 0:
                page.wait_for_timeout(render_settle_ms)  # type: ignore[union-attr]
            if not _click_first(page, _COUNTRY_CONTROL_SELECTORS, deadline):
                return _failed_outcome(
                    "open_country_control",
                    "country control was absent on both homepage and commissioned target",
                )
            warning_notes.append(
                "nordstrom_country_setup: homepage country control was unavailable; "
                "the same retailer-owned control on the commissioned target was used"
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
            # navigations race and the browser runtime reports net::ERR_ABORTED for the main URL.
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

    def before_snapshot(
        self, page: object, *, setup_timeout_ms: float
    ) -> PreCaptureOutcome:
        """Select Most Recent and bound a 30-day window with a 6-row floor/30-row cap."""
        if self.review_posture is None:
            return PreCaptureOutcome(attempted=False, steps_completed=True)
        product_id = _product_id_from_url(self.target_url)
        if product_id is None:
            return _failed_review_outcome(
                "target_product_id",
                "commissioned target URL did not expose a numeric product id",
            )
        deadline = time.monotonic() + (
            min(setup_timeout_ms, _REVIEW_POSTURE_TIMEOUT_MS) / 1000
        )
        warning_notes: list[str] = []
        selector = f"#sort-by-filter-{product_id}-anchor"
        try:
            sort_control = page.locator(selector)  # type: ignore[union-attr]
            if sort_control.count() != 1:
                return _failed_review_outcome(
                    "sort_control",
                    f"{selector} did not resolve to exactly one element",
                )
            if sort_control.inner_text(timeout=_remaining_probe_timeout_ms(deadline)).strip() != (
                "Sort by Most Recent"
            ):
                sort_control.scroll_into_view_if_needed(
                    timeout=_remaining_probe_timeout_ms(deadline)
                )
                page.wait_for_timeout(500)  # type: ignore[union-attr]
                try:
                    sort_control.click(
                        timeout=_remaining_probe_timeout_ms(deadline)
                    )
                except Exception as first_click_error:
                    page.wait_for_timeout(1000)  # type: ignore[union-attr]
                    sort_control.click(
                        timeout=_remaining_probe_timeout_ms(deadline)
                    )
                    warning_notes.append(
                        "nordstrom_review_posture: sort control required one "
                        f"bounded stability retry ({first_click_error})"
                    )
                option = page.get_by_role(  # type: ignore[union-attr]
                    "option", name="Most Recent", exact=True
                )
                if option.count() != 1:
                    return _failed_review_outcome(
                        "most_recent_option",
                        "Most Recent did not resolve to exactly one open-menu option",
                    )
                try:
                    option.click(timeout=_remaining_probe_timeout_ms(deadline))
                except Exception as first_option_click_error:
                    page.wait_for_timeout(1000)  # type: ignore[union-attr]
                    option = page.get_by_role(  # type: ignore[union-attr]
                        "option", name="Most Recent", exact=True
                    )
                    if option.count() != 1:
                        return _failed_review_outcome(
                            "most_recent_option",
                            "Most Recent disappeared during its bounded stability retry",
                        )
                    option.click(timeout=_remaining_probe_timeout_ms(deadline))
                    warning_notes.append(
                        "nordstrom_review_posture: Most Recent option required one "
                        f"bounded stability retry ({first_option_click_error})"
                    )
        except Exception as exc:
            return _failed_review_outcome(
                "select_most_recent",
                f"Most Recent selection failed ({exc})",
            )

        reference_date = self.review_window_reference_date or datetime.now(
            timezone.utc
        ).date()
        while time.monotonic() < deadline:
            try:
                observation = observe_nordstrom_review_window(
                    page.content(),  # type: ignore[union-attr]
                    reference_date=reference_date,
                )
                if observation["admitted"]:
                    return PreCaptureOutcome(
                        attempted=True,
                        steps_completed=True,
                        warning_notes=warning_notes,
                    )
                if observation["status"] == "needs_more":
                    continuation = page.locator(  # type: ignore[union-attr]
                        "#product-page-reviews a:has-text('Load 6 more reviews')"
                    )
                    if continuation.count() != 1:
                        return _failed_review_outcome(
                            "review_continuation",
                            "the 30-day window needs another batch but the target "
                            "continuation did not resolve exactly once",
                        )
                    continuation.click(
                        timeout=_remaining_probe_timeout_ms(deadline)
                    )
                    page.wait_for_timeout(1500)  # type: ignore[union-attr]
            except Exception:
                pass
            pause_ms = min(_REVIEW_POSTURE_POLL_MS, _remaining_ms(deadline))
            if pause_ms > 0:
                page.wait_for_timeout(pause_ms)  # type: ignore[union-attr]
        return _failed_review_outcome(
            "review_postconditions",
            "Most Recent, the highlighted pair, and the bounded 30-day review "
            "window were not jointly observed",
        )

    def describe(self) -> dict[str, object]:
        return {
            "pre_capture": "nordstrom_country_preference",
            "country_code_requested": self.country_code,
            "currency_code_requested": self.currency_code,
            "nordstrom_review_posture_requested": self.review_posture,
            "nordstrom_review_window_days": (
                NORDSTROM_REVIEW_WINDOW_DAYS
                if self.review_posture is not None
                else None
            ),
            "nordstrom_review_minimum": (
                NORDSTROM_REVIEW_MINIMUM
                if self.review_posture is not None
                else None
            ),
            "nordstrom_review_maximum": (
                NORDSTROM_REVIEW_MAXIMUM
                if self.review_posture is not None
                else None
            ),
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


def observe_nordstrom_review_window(
    rendered_dom: str,
    *,
    reference_date: date,
) -> dict[str, object]:
    """Observe the bounded recent-review window without trusting click intent."""
    dom = rendered_dom or ""
    product_id_match = re.search(
        r'id=["\']sort-by-filter-(\d+)-anchor["\'][^>]*>'
        r"[\s\S]{0,500}?Sort by\s*<strong>\s*Most Recent\s*</strong>",
        dom,
        flags=re.IGNORECASE,
    )
    review_start = dom.find('id="product-page-reviews"')
    review_html = dom[review_start:] if review_start >= 0 else ""
    review_dates = _main_review_dates(review_html)
    review_ids = [review_id for review_id, _review_date in review_dates]
    highlighted_pair = all(
        marker in review_html
        for marker in (
            "Most helpful positive review",
            "Most helpful critical review",
            'id="review-stars-positive"',
            'id="review-stars-critical"',
        )
    )
    continuation = (
        re.search(
            r'<a\b[^>]*href=["\']\?page=\d+["\'][^>]*>\s*'
            r"Load\s+6\s+more reviews\s*</a>",
            review_html,
            flags=re.IGNORECASE,
        )
        is not None
    )
    count = len(review_ids)
    consecutive = review_ids == list(range(1, count + 1))
    descending = all(
        review_dates[index][1] >= review_dates[index + 1][1]
        for index in range(max(0, count - 1))
    )
    cutoff = reference_date - timedelta(days=NORDSTROM_REVIEW_WINDOW_DAYS)
    in_window_count = sum(
        review_date >= cutoff for _review_id, review_date in review_dates
    )
    oldest = review_dates[-1][1] if review_dates else None
    base_valid = (
        product_id_match is not None
        and highlighted_pair
        and consecutive
        and descending
        and count >= NORDSTROM_REVIEW_MINIMUM
        and count <= NORDSTROM_REVIEW_MAXIMUM
        and count % NORDSTROM_REVIEW_MINIMUM == 0
    )
    if not base_valid:
        status = "invalid"
    elif oldest is not None and oldest <= cutoff:
        status = "low_density_context" if in_window_count == 0 else "window_complete"
    elif count >= NORDSTROM_REVIEW_MAXIMUM:
        status = "window_truncated"
    elif continuation:
        status = "needs_more"
    else:
        status = "invalid"
    admitted = status in {
        "window_complete",
        "low_density_context",
        "window_truncated",
    }
    return {
        "admitted": admitted,
        "status": status,
        "reference_date": reference_date.isoformat(),
        "window_days": NORDSTROM_REVIEW_WINDOW_DAYS,
        "cutoff_date": cutoff.isoformat(),
        "captured_review_count": count,
        "in_window_review_count": in_window_count,
        "newest_review_date": (
            review_dates[0][1].isoformat() if review_dates else None
        ),
        "oldest_review_date": oldest.isoformat() if oldest is not None else None,
        "continuation_available": continuation,
        "continuation_activations": max(
            0, (count - NORDSTROM_REVIEW_MINIMUM) // NORDSTROM_REVIEW_MINIMUM
        ),
        "highlighted_pair_present": highlighted_pair,
        "sort_most_recent": product_id_match is not None,
        "review_ids": review_ids,
    }


def confirm_nordstrom_review_posture(
    rendered_dom: str,
    *,
    reference_date: date | None = None,
) -> PinConfirmation:
    """Confirm the bounded review-window posture from captured source state."""
    observation = observe_nordstrom_review_window(
        rendered_dom,
        reference_date=reference_date or datetime.now(timezone.utc).date(),
    )
    if observation["admitted"]:
        return PinConfirmation(
            confirmed=True,
            detail=(
                "target review section shows Sort by Most Recent, the most-helpful "
                "positive/critical pair, and bounded recent-review status "
                f"{observation['status']} with "
                f"{observation['captured_review_count']} main-list rows"
            ),
        )
    return PinConfirmation(
        confirmed=False,
        detail=(
            "required Nordstrom onboarding review conjunction absent "
            f"(status={observation['status']}, "
            f"most_recent={observation['sort_most_recent']}, "
            f"review_ids={observation['review_ids']}, "
            f"highlighted_pair={observation['highlighted_pair_present']}, "
            f"continuation={observation['continuation_available']})"
        ),
    )


def _main_review_dates(review_html: str) -> list[tuple[int, date]]:
    starts = list(
        re.finditer(
            r'<div\b[^>]*\bid=["\']review-(\d+)["\'][^>]*>',
            review_html,
            flags=re.IGNORECASE,
        )
    )
    result: list[tuple[int, date]] = []
    for index, start in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(review_html)
        card = review_html[start.start() : end]
        raw_date = None
        for pattern in (
            r'itemprop=["\']datePublished["\'][^>]*content=["\']'
            r"(\d{4}-\d{2}-\d{2})",
            r"\b("
            r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|"
            r"May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|"
            r"Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
            r"\s+\d{1,2},\s+\d{4})\b",
        ):
            raw_date = first_match(
                card,
                pattern,
                flags=re.IGNORECASE | re.DOTALL,
            )
            if raw_date is not None:
                break
        parsed = _parse_review_date(raw_date)
        if parsed is not None:
            result.append((int(start.group(1)), parsed))
    return result


def _parse_review_date(value: str | None) -> date | None:
    if value is None:
        return None
    value = re.sub(r"^Sept\s+", "Sep ", value, flags=re.IGNORECASE)
    for format_string in ("%Y-%m-%d", "%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(value, format_string).date()
        except ValueError:
            continue
    return None


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


def _failed_review_outcome(reason: str, detail: str) -> PreCaptureOutcome:
    return PreCaptureOutcome(
        attempted=True,
        steps_completed=False,
        reason=reason,
        warning_notes=[
            "nordstrom_review_posture: "
            f"{detail}; artifacts will be captured and fail closed at admission"
        ],
    )


def _product_id_from_url(url: str | None) -> str | None:
    if url is None:
        return None
    match = re.search(r"/s/[^/?#]+/(\d+)(?:[/?#]|$)", urlparse(url).path)
    return match.group(1) if match else None


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
