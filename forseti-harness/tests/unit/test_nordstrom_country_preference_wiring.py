from __future__ import annotations

from typing import Any

import pytest

from runners import run_source_capture_cloakbrowser_packet as cloak_writer
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
from source_capture.adapters.nordstrom_country_preference import (
    NordstromCountryPreferencePlugin,
    confirm_nordstrom_us_storefront,
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

    def select_option(self, *, timeout: float, **option: str) -> None:
        self.page.actions.append(("select_option", self.selector, option, timeout))
        if self.selector not in self.page.selectable:
            raise RuntimeError("not selectable")

    def inner_text(self, *, timeout: float) -> str:
        return self.page.body_text


class _FakePage:
    def __init__(
        self,
        *,
        clickable: set[str] | None = None,
        selectable: set[str] | None = None,
        body_text: str = "United States",
        goto_error: Exception | None = None,
        target_control_url: str | None = None,
    ) -> None:
        self.clickable = clickable or set()
        self.selectable = selectable or set()
        self.body_text = body_text
        self.goto_error = goto_error
        self.target_control_url = target_control_url
        self.actions: list[tuple[Any, ...]] = []

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
