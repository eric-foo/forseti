from __future__ import annotations

import re
from datetime import date
from typing import Any

import pytest

from runners import run_source_capture_cloakbrowser_packet as cloak_writer
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
from source_capture.adapters.nordstrom_country_preference import (
    NordstromCountryPreferencePlugin,
    confirm_nordstrom_review_posture,
    confirm_nordstrom_us_storefront,
    observe_nordstrom_review_window,
)


_US_DOM = """
<html><body>
<button name="changeCountry" aria-label="United States. Choose your shipping country">
  <img src="https://n.nordstrommedia.com/alias/US.gif"><span>United States</span>
</button>
<script>
window.__STATE__ = {
  "internationalShipping": {"selectedCountryCode":"US","selectedCurrencyCode":"USD"},
  "shopper": {"Context":{"CountryCode":"US","CurrencyCode":"USD","IsInternationalShopping":false}}
};
</script>
</body></html>
"""


def _review_dom(
    *,
    sort: str = "Most Recent",
    review_count: int = 6,
    dense: bool = False,
) -> str:
    low_density_dates = [
        "June 13, 2026",
        "Apr 27, 2026",
        "Apr 20, 2026",
        "Mar 31, 2026",
        "Mar 23, 2026",
        "Mar 21, 2026",
    ]
    dense_dates = [
        "July 18, 2026",
        "July 17, 2026",
        "July 16, 2026",
        "July 15, 2026",
        "July 14, 2026",
        "July 13, 2026",
        "July 12, 2026",
        "July 11, 2026",
        "July 10, 2026",
        "July 9, 2026",
        "July 8, 2026",
        "July 7, 2026",
        "June 1, 2026",
    ]
    dates = dense_dates if dense else low_density_dates
    reviews = "".join(
        f'<div id="review-{index}">{dates[min(index - 1, len(dates) - 1)]}'
        f" review {index}</div>"
        for index in range(1, review_count + 1)
    )
    return f"""
<div id="product-page-reviews">
  <div>Most helpful positive review
    <span id="review-stars-positive" aria-label="Rated 5 out of 5 stars."></span>
  </div>
  <div>Most helpful critical review
    <span id="review-stars-critical" aria-label="Rated 1 out of 5 stars."></span>
  </div>
  <div id="sort-by-filter-8260802-anchor">Sort by <strong>{sort}</strong></div>
  {reviews}
  <a href="?page=2">Load 6 more reviews</a>
</div>
"""


class _FakeLocator:
    def __init__(self, page: "_FakePage", selector: str) -> None:
        self.page = page
        self.selector = selector

    @property
    def last(self) -> "_FakeLocator":
        return self

    @property
    def first(self) -> "_FakeLocator":
        return self

    def click(self, *, timeout: float) -> None:
        self.page.actions.append(("click", self.selector, timeout))
        if self.selector not in self.page.clickable:
            raise RuntimeError("not clickable")
        if self.selector == "role=option:Most Recent":
            if self.page.option_click_failures > 0:
                self.page.option_click_failures -= 1
                raise RuntimeError("element position is still changing")
            self.page.review_sort = "Most Recent"
        if self.selector == (
            "#product-page-reviews a:has-text('Load 6 more reviews')"
        ):
            self.page.review_count += 6

    def select_option(self, *, timeout: float, **option: str) -> None:
        self.page.actions.append(("select_option", self.selector, option, timeout))
        if self.selector not in self.page.selectable:
            raise RuntimeError("not selectable")

    def scroll_into_view_if_needed(self, *, timeout: float) -> None:
        self.page.actions.append(("scroll_into_view", self.selector, timeout))

    def inner_text(self, *, timeout: float) -> str:
        if self.selector == "#sort-by-filter-8260802-anchor":
            return f"Sort by {self.page.review_sort}"
        return self.page.body_text

    def count(self) -> int:
        return int(
            self.selector in self.page.clickable
            or self.selector in self.page.selectable
        )


class _FakePage:
    def __init__(
        self,
        *,
        clickable: set[str] | None = None,
        selectable: set[str] | None = None,
        body_text: str = "United States",
        goto_error: Exception | None = None,
        target_control_url: str | None = None,
        review_sort: str = "Most Helpful",
        review_count: int = 6,
        dense_reviews: bool = False,
        option_click_failures: int = 0,
    ) -> None:
        self.clickable = clickable or set()
        self.selectable = selectable or set()
        self.body_text = body_text
        self.goto_error = goto_error
        self.target_control_url = target_control_url
        self.actions: list[tuple[Any, ...]] = []
        self.review_sort = review_sort
        self.review_count = review_count
        self.dense_reviews = dense_reviews
        self.option_click_failures = option_click_failures

    def goto(self, url: str, *, wait_until: str, timeout: float) -> None:
        self.actions.append(("goto", url, wait_until, timeout))
        if self.goto_error is not None:
            raise self.goto_error
        if url == self.target_control_url:
            self.clickable.update(
                {
                    "button[name='changeCountry']",
                    "[role='dialog'] button:has-text('United States')",
                    "[role='dialog'] button:has-text('Save')",
                }
            )

    def locator(self, selector: str) -> _FakeLocator:
        return _FakeLocator(self, selector)

    def get_by_role(
        self, role: str, *, name: str, exact: bool
    ) -> _FakeLocator:
        assert (role, name, exact) == ("option", "Most Recent", True)
        return _FakeLocator(self, "role=option:Most Recent")

    def content(self) -> str:
        return _review_dom(
            sort=self.review_sort,
            review_count=self.review_count,
            dense=self.dense_reviews,
        )

    def wait_for_timeout(self, timeout: float) -> None:
        self.actions.append(("wait", timeout))

    def wait_for_load_state(self, state: str, *, timeout: float) -> None:
        self.actions.append(("wait_for_load_state", state, timeout))


def _fake_capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
    pre_capture = kwargs["pre_capture"]
    assert isinstance(pre_capture, NordstromCountryPreferencePlugin)
    confirmation = pre_capture.confirm(_US_DOM)
    return CloakBrowserSnapshotSuccess(
        requested_url=kwargs["url"],
        final_url=kwargs["url"],
        title="The Lip Balm",
        rendered_dom=_US_DOM,
        visible_text="Nécessaire The Lip Balm $28.00",
        screenshot_png=b"\x89PNG\r\n\x1a\n",
        metadata={
            "capture_timestamp": "2026-07-17T00:00:00Z",
            "requested_url": kwargs["url"],
            **pre_capture.describe(),
            "pin_confirmed": confirmation.confirmed,
        },
        warning_notes=[],
        limitation_notes=[],
    )


def test_confirmation_requires_nordstrom_us_state_conjunction() -> None:
    confirmation = confirm_nordstrom_us_storefront(_US_DOM)

    assert confirmation.confirmed is True
    assert "US shopper context" in confirmation.detail


@pytest.mark.parametrize(
    "dom",
    [
        '<script>{"nordcountrycode":"US"}</script><span>$28.00</span>',
        '<script>{"selectedCountryCode":"US","selectedCurrencyCode":"USD"}</script>',
        (
            '<script>{"CountryCode":"SG","CurrencyCode":"SGD",'
            '"IsInternationalShopping":true}</script><span>S$37.19</span>'
        ),
        (
            '<script>{"CountryCode":"US","CurrencyCode":"USD",'
            '"IsInternationalShopping":false}</script><span>$28.00</span>'
        ),
        (
            '<script>{"Context":{"CountryCode":"US"},'
            '"other":{"CurrencyCode":"USD","IsInternationalShopping":false},'
            '"selectedCountryCode":"US","selectedCurrencyCode":"USD"}</script>'
        ),
    ],
)
def test_confirmation_rejects_weak_or_incomplete_signals(dom: str) -> None:
    assert confirm_nordstrom_us_storefront(dom).confirmed is False


def test_before_uses_observed_flag_control_and_country_option() -> None:
    page = _FakePage(
        clickable={
            "button:has(img[src*='/alias/SG.gif'])",
            "[role='dialog'] button:has-text('United States')",
            "[role='dialog'] button:has-text('Save')",
        }
    )

    outcome = NordstromCountryPreferencePlugin().before(page, setup_timeout_ms=20_000)

    assert outcome.steps_completed is True
    assert outcome.reason is None
    assert any(action[1] == "button:has(img[src*='/alias/SG.gif'])" for action in page.actions)
    assert any(action[0] == "wait_for_load_state" for action in page.actions)


def test_before_reports_missing_country_control() -> None:
    outcome = NordstromCountryPreferencePlugin().before(
        _FakePage(), setup_timeout_ms=20_000
    )

    assert outcome.steps_completed is False
    assert outcome.reason == "open_country_control"
    assert "without a confirmed country preference" in outcome.warning_notes[0]


def test_before_falls_back_to_same_control_on_commissioned_target() -> None:
    target_url = "https://www.nordstrom.com/s/the-lip-balm/8260802"
    page = _FakePage(target_control_url=target_url)

    outcome = NordstromCountryPreferencePlugin(target_url=target_url).before(
        page, setup_timeout_ms=45_000
    )

    assert outcome.steps_completed is True
    assert outcome.reason is None
    assert any(action[:2] == ("goto", target_url) for action in page.actions)
    assert any(
        "commissioned target was used" in warning
        for warning in outcome.warning_notes
    )


def test_before_snapshot_expands_sparse_window_to_thirty_recent_rows() -> None:
    continuation_selector = (
        "#product-page-reviews a:has-text('Load 6 more reviews')"
    )
    page = _FakePage(
        clickable={
            "#sort-by-filter-8260802-anchor",
            "role=option:Most Recent",
            continuation_selector,
        },
    )
    plugin = NordstromCountryPreferencePlugin(
        target_url="https://www.nordstrom.com/s/the-lip-balm/8260802",
        review_posture="recent_window_30d",
        review_window_reference_date=date(2026, 7, 19),
    )

    outcome = plugin.before_snapshot(page, setup_timeout_ms=20_000)

    assert outcome.steps_completed is True
    assert page.review_sort == "Most Recent"
    assert confirm_nordstrom_review_posture(
        page.content(), reference_date=date(2026, 7, 19)
    ).confirmed is True
    observation = observe_nordstrom_review_window(
        page.content(), reference_date=date(2026, 7, 19)
    )
    assert page.review_count == 30
    assert observation["status"] == "historical_context_complete"
    assert observation["continuation_activations"] == 4
    assert observation["in_window_review_count"] == 0


def test_before_snapshot_retries_one_moving_most_recent_option() -> None:
    continuation_selector = (
        "#product-page-reviews a:has-text('Load 6 more reviews')"
    )
    page = _FakePage(
        clickable={
            "#sort-by-filter-8260802-anchor",
            "role=option:Most Recent",
            continuation_selector,
        },
        option_click_failures=1,
    )
    plugin = NordstromCountryPreferencePlugin(
        target_url="https://www.nordstrom.com/s/the-lip-balm/8260802",
        review_posture="recent_window_30d",
        review_window_reference_date=date(2026, 7, 19),
    )

    outcome = plugin.before_snapshot(page, setup_timeout_ms=20_000)

    assert outcome.steps_completed is True
    assert page.review_sort == "Most Recent"
    assert any("bounded stability retry" in note for note in outcome.warning_notes)
    assert sum(
        action[:2] == ("click", "role=option:Most Recent")
        for action in page.actions
    ) == 2


def test_review_posture_confirmation_rejects_stale_sort_or_seventh_review() -> None:
    assert confirm_nordstrom_review_posture(
        _review_dom(sort="Most Helpful"),
        reference_date=date(2026, 7, 19),
    ).confirmed is False
    assert confirm_nordstrom_review_posture(
        _review_dom(review_count=7),
        reference_date=date(2026, 7, 19),
    ).confirmed is False


def test_before_snapshot_loads_two_six_row_batches_to_close_dense_window() -> None:
    continuation_selector = (
        "#product-page-reviews a:has-text('Load 6 more reviews')"
    )
    page = _FakePage(
        clickable={
            "#sort-by-filter-8260802-anchor",
            "role=option:Most Recent",
            continuation_selector,
        },
        dense_reviews=True,
    )
    plugin = NordstromCountryPreferencePlugin(
        target_url="https://www.nordstrom.com/s/the-lip-balm/8260802",
        review_posture="recent_window_30d",
        review_window_reference_date=date(2026, 7, 19),
    )

    outcome = plugin.before_snapshot(page, setup_timeout_ms=20_000)
    observation = observe_nordstrom_review_window(
        page.content(), reference_date=date(2026, 7, 19)
    )

    assert outcome.steps_completed is True
    assert page.review_count == 18
    assert observation["status"] == "recent_window_complete"
    assert observation["in_window_review_count"] == 12
    assert observation["continuation_activations"] == 2


def test_review_window_marks_thirty_in_window_rows_truncated() -> None:
    dom = _review_dom(review_count=30, dense=True)
    dom = re.sub(
        r"(?:June|May)\s+\d{1,2},\s+2026",
        "July 1, 2026",
        dom,
    )

    observation = observe_nordstrom_review_window(
        dom, reference_date=date(2026, 7, 19)
    )

    assert observation["status"] == "recent_window_truncated"
    assert observation["captured_review_count"] == 30
    assert observation["continuation_activations"] == 4


def test_review_window_admits_proven_source_exhaustion_below_thirty() -> None:
    dom = _review_dom().replace(
        '  <a href="?page=2">Load 6 more reviews</a>',
        (
            '<script type="application/ld+json">'
            '{"@type":"Product","url":"https://www.nordstrom.com/s/item/8260802",'
            '"aggregateRating":{"reviewCount":6}}</script>'
        ),
    )

    observation = observe_nordstrom_review_window(
        dom, reference_date=date(2026, 7, 19)
    )

    assert observation["status"] == "source_exhausted"
    assert observation["source_total_count"] == 6
    assert observation["captured_review_count"] == 6
    assert observation["admitted"] is True


def test_plugin_rejects_non_us_and_non_positive_timeout() -> None:
    with pytest.raises(ValueError, match="only US/USD"):
        NordstromCountryPreferencePlugin(country_code="SG", currency_code="SGD")
    with pytest.raises(ValueError, match="greater than zero"):
        NordstromCountryPreferencePlugin(setup_timeout_seconds=0)
    with pytest.raises(ValueError, match="must use nordstrom.com"):
        NordstromCountryPreferencePlugin(target_url="https://example.com/product")


def test_writer_builds_nordstrom_plugin(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setattr(cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_capture)

    exit_code, output = cloak_writer.run_source_capture_cloakbrowser_packet(
        url="https://www.nordstrom.com/s/the-lip-balm/8260802",
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        decision_question="Does the bound US PDP render?",
        output_directory=tmp_path / "packet",
        capture_context="offline test",
        operator_category="test",
        capture_mode=cloak_writer.CaptureModeCategory.MULTIMODAL,
        session_id=None,
        proxy_profile=None,
        actor_audience_context=cloak_writer.unknown_with_reason("not needed"),
        visible_mode_changes=[],
        source_publication_or_event=cloak_writer.unknown_with_reason("not needed"),
        source_edit_or_version=cloak_writer.unknown_with_reason("not needed"),
        cutoff_posture=cloak_writer.unknown_with_reason("not needed"),
        recapture_time=cloak_writer.not_applicable("not needed"),
        re_capture_relationship=cloak_writer.not_applicable("not needed"),
        warnings=[],
        limitations=[],
        timeout_seconds=30,
        wait_until="load",
        viewport_width=1920,
        viewport_height=1080,
        max_artifact_bytes=5_000_000,
        block_heavy_assets=False,
        nordstrom_country="US",
    )

    assert exit_code == 0
    assert output == str(tmp_path / "packet")


def test_writer_rejects_two_site_specific_pre_capture_plugins(tmp_path) -> None:
    with pytest.raises(ValueError, match="only one site-specific pre-capture"):
        cloak_writer.run_source_capture_cloakbrowser_packet(
            url="https://www.nordstrom.com/s/the-lip-balm/8260802",
            source_family="retail_pdp",
            source_surface="cloakbrowser_snapshot",
            decision_question="Does the bound US PDP render?",
            output_directory=tmp_path / "packet",
            capture_context="offline test",
            operator_category="test",
            capture_mode=cloak_writer.CaptureModeCategory.MULTIMODAL,
            session_id=None,
            proxy_profile=None,
            actor_audience_context=cloak_writer.unknown_with_reason("not needed"),
            visible_mode_changes=[],
            source_publication_or_event=cloak_writer.unknown_with_reason("not needed"),
            source_edit_or_version=cloak_writer.unknown_with_reason("not needed"),
            cutoff_posture=cloak_writer.unknown_with_reason("not needed"),
            recapture_time=cloak_writer.not_applicable("not needed"),
            re_capture_relationship=cloak_writer.not_applicable("not needed"),
            warnings=[],
            limitations=[],
            timeout_seconds=30,
            wait_until="load",
            viewport_width=1920,
            viewport_height=1080,
            max_artifact_bytes=5_000_000,
            block_heavy_assets=False,
            delivery_zip="10001",
            nordstrom_country="US",
        )
