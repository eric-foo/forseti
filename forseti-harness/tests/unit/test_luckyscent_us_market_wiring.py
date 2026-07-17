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


def test_writer_rejects_luckyscent_plus_other_site_preference(tmp_path) -> None:
    with pytest.raises(ValueError, match="only one site-specific pre-capture"):
        cloak_writer.run_source_capture_cloakbrowser_packet(
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
            nordstrom_country="US",
            luckyscent_market="US",
        )
