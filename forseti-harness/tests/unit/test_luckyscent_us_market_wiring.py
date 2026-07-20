from __future__ import annotations

import json
from typing import Any

import pytest

from runners import run_source_capture_cloakbrowser_packet as cloak_writer
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
from source_capture.adapters.luckyscent_us_market import (
    LuckyscentUSMarketPlugin,
    confirm_luckyscent_us_market,
)


def _loader_dom(context: dict[str, str]) -> str:
    table: list[Any] = [
        {"_1": 2},
        "i18n",
        {"_3": 4, "_5": 6, "_7": 8},
        "country",
        context["country"],
        "market",
        context["market"],
        "currency",
        context["currency"],
    ]
    chunk = f"P0:{json.dumps(table, separators=(',', ':'))}\n"
    return (
        "<html><body><script>"
        "window.__reactRouterContext.streamController.enqueue("
        f"{json.dumps(chunk)}"
        ");</script></body></html>"
    )


_US_DOM = _loader_dom(
    {"country": "US", "market": "market-us", "currency": "USD"}
)


def _fake_capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
    pre_capture = kwargs["pre_capture"]
    assert isinstance(pre_capture, LuckyscentUSMarketPlugin)
    confirmation = pre_capture.confirm(_US_DOM)
    return CloakBrowserSnapshotSuccess(
        requested_url=kwargs["url"],
        final_url=kwargs["url"],
        title="Bread and Roses",
        rendered_dom=_US_DOM,
        visible_text="Pearfat Parfum Bread and Roses $120.00",
        screenshot_png=b"\x89PNG\r\n\x1a\n",
        metadata={
            "capture_timestamp": "2026-07-18T00:00:00Z",
            "requested_url": kwargs["url"],
            **pre_capture.describe(),
            "pin_confirmed": confirmation.confirmed,
        },
        warning_notes=[],
        limitation_notes=[],
    )


def test_confirmation_requires_one_luckyscent_i18n_conjunction() -> None:
    confirmation = confirm_luckyscent_us_market(_US_DOM)

    assert confirmation.confirmed is True
    assert "country=US" in confirmation.detail


@pytest.mark.parametrize(
    "dom",
    [
        "<script>{\"buyerCountry\":\"US\"}</script><span>$120</span>",
        _loader_dom(
            {"country": "US", "market": "market-us", "currency": "SGD"}
        ),
        _loader_dom(
            {"country": "SG", "market": "market-us", "currency": "USD"}
        ),
        (
            _loader_dom(
                {"country": "US", "market": "market-sg", "currency": "SGD"}
            )
            + '<script>{"priceCurrency":"USD","market":"market-us"}</script>'
        ),
        '<script>window.__reactRouterContext.streamController.enqueue("broken");</script>',
    ],
)
def test_confirmation_rejects_weak_split_or_malformed_signals(dom: str) -> None:
    assert confirm_luckyscent_us_market(dom).confirmed is False


def test_plugin_is_assertion_only_and_does_not_touch_page() -> None:
    page = object()

    outcome = LuckyscentUSMarketPlugin().before(page, setup_timeout_ms=1)

    assert outcome.attempted is True
    assert outcome.steps_completed is True
    assert outcome.warning_notes == []
    assert LuckyscentUSMarketPlugin().humanize is False


class _PromotionalCloseControl:
    def __init__(self, modal: "_PromotionalModal") -> None:
        self.modal = modal
        self.click_count = 0

    def count(self) -> int:
        return 1

    def click(self, *, timeout: int) -> None:
        assert timeout > 0
        self.click_count += 1
        self.modal.hidden = True


class _PromotionalModal:
    def __init__(self, *, text: str, count: int = 1) -> None:
        self.text = text
        self.modal_count = count
        self.hidden = False
        self.close_control = _PromotionalCloseControl(self)
        self.close_selectors: list[str] = []

    def count(self) -> int:
        return self.modal_count

    def inner_text(self, *, timeout: int) -> str:
        assert timeout > 0
        return self.text

    def locator(self, selector: str) -> _PromotionalCloseControl:
        self.close_selectors.append(selector)
        return self.close_control

    def wait_for(self, *, state: str, timeout: int) -> None:
        assert state == "hidden"
        assert timeout > 0
        assert self.hidden is True


class _PromotionalPage:
    def __init__(self, modal: _PromotionalModal) -> None:
        self.modal = modal
        self.selectors: list[str] = []

    def locator(self, selector: str) -> _PromotionalModal:
        self.selectors.append(selector)
        return self.modal


def test_plugin_dismisses_only_the_exact_luckyscent_promotional_modal() -> None:
    modal = _PromotionalModal(
        text=(
            "Lucky You!\n10% off Your First Order.\n"
            "A code will be emailed to you.\nClaim My 10% Off"
        )
    )
    page = _PromotionalPage(modal)

    outcome = LuckyscentUSMarketPlugin().before_snapshot(
        page, setup_timeout_ms=30_000
    )

    assert outcome.attempted is True
    assert outcome.steps_completed is True
    assert outcome.reason is None
    assert modal.close_control.click_count == 1
    assert modal.hidden is True
    assert page.selectors == [
        '[role="dialog"][aria-modal="true"][aria-label="POPUP Form"]'
        '[data-kl-scroll-locking-modal="true"]'
    ]
    assert modal.close_selectors == [
        'button.klaviyo-close-form[aria-label="Close dialog"]'
    ]


def test_plugin_leaves_absent_or_changed_promotional_modal_untouched() -> None:
    absent = _PromotionalModal(text="", count=0)
    absent_outcome = LuckyscentUSMarketPlugin().before_snapshot(
        _PromotionalPage(absent), setup_timeout_ms=30_000
    )
    assert absent_outcome.attempted is False
    assert absent_outcome.steps_completed is True
    assert absent.close_control.click_count == 0

    changed = _PromotionalModal(text="An unrelated account dialog")
    changed_outcome = LuckyscentUSMarketPlugin().before_snapshot(
        _PromotionalPage(changed), setup_timeout_ms=30_000
    )
    assert changed_outcome.attempted is True
    assert changed_outcome.steps_completed is False
    assert "markers changed" in (changed_outcome.reason or "")
    assert changed.close_control.click_count == 0


def test_plugin_records_the_named_overlay_action_without_secret_state() -> None:
    metadata = LuckyscentUSMarketPlugin().describe()

    assert metadata["overlay_action_classification"] == "benign_dismissible_overlay"
    assert metadata["overlay_action_name"] == "luckyscent_first_order_promo_dismiss_v1"
    assert metadata["overlay_action_allowed_control"] == "Close dialog"
    serialized = json.dumps(metadata, sort_keys=True)
    assert "Claim My 10% Off" in serialized
    assert "cookie" in serialized
    assert "storage" not in serialized
    assert "credential" not in serialized


def test_unresolved_luckyscent_overlay_fails_content_admission_explicitly() -> None:
    assert cloak_writer._luckyscent_overlay_dismissal_failure(
        luckyscent_market="US",
        before_snapshot_steps_completed=False,
        before_snapshot_reason="modal markers changed",
    ) == "modal markers changed"
    assert (
        cloak_writer._luckyscent_overlay_dismissal_failure(
            luckyscent_market="US",
            before_snapshot_steps_completed=True,
            before_snapshot_reason=None,
        )
        is None
    )
    assert (
        cloak_writer._luckyscent_overlay_dismissal_failure(
            luckyscent_market=None,
            before_snapshot_steps_completed=False,
            before_snapshot_reason="unrelated route",
        )
        is None
    )


def test_plugin_rejects_non_us_market() -> None:
    with pytest.raises(ValueError, match="only US/USD"):
        LuckyscentUSMarketPlugin(country_code="SG", currency_code="SGD")


def test_writer_builds_luckyscent_market_plugin(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    monkeypatch.setattr(cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_capture)

    exit_code, output = cloak_writer.run_source_capture_cloakbrowser_packet(
        url="https://www.luckyscent.com/products/bread-and-roses-by-pearfat-parfum",
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        decision_question="Does the bound US-market PDP render?",
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
        luckyscent_market="US",
    )

    assert exit_code == 0
    assert output == str(tmp_path / "packet")
