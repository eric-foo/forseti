from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from runners import run_source_capture_cloakbrowser_packet as cloak_writer
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
from source_capture.adapters.sephora_us_market import (
    SephoraUSMarketPlugin,
    confirm_sephora_us_market,
)


def _sephora_dom(
    *,
    country: str = "US",
    currency: str = "USD",
    seller: str = "Sephora",
    price: object = "16.00",
) -> str:
    render_query = json.dumps(
        {
            "channel": "rwd",
            "country": country,
            "language": "en",
            "urlPath": "/product/tower-28-lipsoftie-P509397",
        },
        separators=(",", ":"),
    )
    product = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": "LipSoftie Hydrating Tinted Lip Treatment Balm",
            "brand": {"@type": "Brand", "name": "Tower 28 Beauty"},
            "offers": {
                "@type": "Offer",
                "price": price,
                "priceCurrency": currency,
                "seller": {"@type": "Organization", "name": seller},
            },
        },
        separators=(",", ":"),
    )
    return (
        "<html><body><script>"
        f"Sephora.renderQueryParams = {render_query};Sephora.isSPA = true;"
        "</script><script type=\"application/ld+json\">"
        f"{product}"
        "</script></body></html>"
    )


_US_DOM = _sephora_dom()
_COUNTRY_DIALOG_TEXT = "This site does not ship to your country."
_SEPHORA_URL = (
    "https://www.sephora.com/product/"
    "tower-28-lipsoftie-hydrating-tinted-lip-treatment-balm-P509397"
    "?country_switch=us&lang=en"
)


def _fake_capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
    pre_capture = kwargs["pre_capture"]
    assert isinstance(pre_capture, SephoraUSMarketPlugin)
    assert pre_capture.target_url == kwargs["url"]
    confirmation = pre_capture.confirm(_US_DOM)
    return CloakBrowserSnapshotSuccess(
        requested_url=kwargs["url"],
        final_url=kwargs["url"],
        title="LipSoftie - Tower 28 Beauty | Sephora",
        rendered_dom=_US_DOM,
        visible_text=(
            "Tower 28 Beauty LipSoftie Hydrating Tinted Lip Treatment Balm "
            "$16.00 Ratings & Reviews"
        ),
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


def _run_writer(tmp_path: Path, **overrides: Any) -> tuple[int, str]:
    kwargs: dict[str, Any] = {
        "url": _SEPHORA_URL,
        "source_family": "retail_pdp",
        "source_surface": "cloakbrowser_snapshot",
        "decision_question": "Does the bound Sephora US/USD PDP render?",
        "output_directory": tmp_path / "packet",
        "capture_context": "offline test",
        "operator_category": "test",
        "capture_mode": cloak_writer.CaptureModeCategory.MULTIMODAL,
        "session_id": None,
        "proxy_profile": None,
        "actor_audience_context": cloak_writer.unknown_with_reason("not needed"),
        "visible_mode_changes": [],
        "source_publication_or_event": cloak_writer.unknown_with_reason("not needed"),
        "source_edit_or_version": cloak_writer.unknown_with_reason("not needed"),
        "cutoff_posture": cloak_writer.unknown_with_reason("not needed"),
        "recapture_time": cloak_writer.not_applicable("not needed"),
        "re_capture_relationship": cloak_writer.not_applicable("not needed"),
        "warnings": [],
        "limitations": [],
        "timeout_seconds": 30,
        "wait_until": "load",
        "viewport_width": 1920,
        "viewport_height": 1080,
        "max_artifact_bytes": 5_000_000,
        "block_heavy_assets": False,
        "sephora_market": "US",
    }
    kwargs.update(overrides)
    return cloak_writer.run_source_capture_cloakbrowser_packet(**kwargs)


def test_confirmation_requires_served_country_and_sephora_usd_offer() -> None:
    confirmation = confirm_sephora_us_market(_US_DOM)

    assert confirmation.confirmed is True
    assert "country=US" in confirmation.detail
    assert "priceCurrency=USD" in confirmation.detail


def test_confirmation_rejects_country_dialog_over_valid_usd_page() -> None:
    confirmation = confirm_sephora_us_market(
        _US_DOM + f"<div>{_COUNTRY_DIALOG_TEXT}</div>"
    )

    assert confirmation.confirmed is False
    assert "country-routing dialog absent" in confirmation.detail


@pytest.mark.parametrize(
    "dom",
    [
        '<script>Sephora.renderQueryParams={"country":"US"}</script>',
        (
            '<script type="application/ld+json">'
            '{"@type":"Offer","price":"16","priceCurrency":"USD",'
            '"seller":{"@type":"Organization","name":"Sephora"}}'
            "</script>"
        ),
        _sephora_dom(country="CA"),
        _sephora_dom(currency="CAD"),
        _sephora_dom(seller="Marketplace Seller"),
        _sephora_dom(price=""),
        (
            '<script>Sephora.renderQueryParams={"country":"US"};</script>'
            '<script>{"@type":"Offer","price":"16","priceCurrency":"USD",'
            '"seller":{"@type":"Organization","name":"Sephora"}}</script>'
        ),
        (
            "<script>Sephora.renderQueryParams = {broken};</script>"
            '<script type="application/ld+json">{broken}</script>'
        ),
        (
            "<p>Sephora.renderQueryParams is documented here</p>"
            '<script>{"country":"US"}</script>'
            '<script type="application/ld+json">'
            '{"@type":"Offer","price":"16","priceCurrency":"USD",'
            '"seller":{"@type":"Organization","name":"Sephora"}}'
            "</script>"
        ),
    ],
)
def test_confirmation_rejects_weak_split_or_malformed_signals(dom: str) -> None:
    assert confirm_sephora_us_market(dom).confirmed is False


def test_plugin_preflight_noops_after_target_navigation_when_dialog_absent() -> None:
    page = MagicMock()
    dialog = page.locator.return_value
    dialog.count.return_value = 0

    outcome = SephoraUSMarketPlugin(target_url=_SEPHORA_URL).before(
        page, setup_timeout_ms=10_000
    )

    assert outcome.attempted is True
    assert outcome.steps_completed is True
    assert outcome.warning_notes == []
    page.goto.assert_called_once_with(
        _SEPHORA_URL,
        wait_until="load",
        timeout=10_000,
    )
    assert SephoraUSMarketPlugin(target_url=_SEPHORA_URL).humanize is False


def test_plugin_uses_exact_country_dialog_continuation() -> None:
    page = MagicMock()
    page.url = "https://www.sephora.com/"
    dialog = page.locator.return_value
    dialog.count.side_effect = [1, 0]
    dialog.is_visible.return_value = True
    dialog.inner_text.return_value = (
        "Looks like you are trying to access Sephora.com from another country. "
        f"{_COUNTRY_DIALOG_TEXT} Continue to Sephora.com."
    )
    paragraph = dialog.locator.return_value
    filtered = paragraph.filter.return_value
    button = filtered.locator.return_value
    button.count.return_value = 1

    outcome = SephoraUSMarketPlugin(target_url=_SEPHORA_URL).before(
        page, setup_timeout_ms=10_000
    )

    assert outcome.steps_completed is True
    paragraph.filter.assert_called_once_with(has_text="Continue to")
    button.locator.assert_not_called()
    button.click.assert_called_once_with(timeout=10_000)


def test_plugin_fails_closed_on_ambiguous_country_dialog() -> None:
    page = MagicMock()
    dialog = page.locator.return_value
    dialog.count.return_value = 1
    dialog.is_visible.return_value = True
    dialog.inner_text.return_value = (
        f"{_COUNTRY_DIALOG_TEXT} Continue to Sephora.com."
    )
    dialog.locator.return_value.filter.return_value.locator.return_value.count.return_value = 2

    outcome = SephoraUSMarketPlugin(target_url=_SEPHORA_URL).before(
        page, setup_timeout_ms=10_000
    )

    assert outcome.steps_completed is False
    assert outcome.reason is not None
    assert "exactly one" in outcome.reason


def test_plugin_rejects_non_us_market() -> None:
    with pytest.raises(ValueError, match="only US/USD"):
        SephoraUSMarketPlugin(
            target_url=_SEPHORA_URL,
            country_code="CA",
            currency_code="CAD",
        )


def test_plugin_rejects_non_us_target_route() -> None:
    with pytest.raises(ValueError, match="country_switch=us"):
        SephoraUSMarketPlugin(
            target_url="https://www.sephora.com/product/example"
        )


def test_writer_builds_sephora_market_plugin(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_capture)

    exit_code, output = _run_writer(tmp_path)

    assert exit_code == 0
    assert output == str(tmp_path / "packet")


def test_writer_requires_sephora_us_request_route(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="country_switch=us"):
        _run_writer(
            tmp_path,
            url="https://www.sephora.com/product/tower-28-lipsoftie-P509397",
        )

    with pytest.raises(ValueError, match="country_switch=us"):
        _run_writer(
            tmp_path,
            url="https://www.ulta.com/product/example?country_switch=us",
        )


def test_cli_preflight_validates_sephora_request_before_capture(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    common = [
        "--source-family",
        "retail_pdp",
        "--source-surface",
        "cloakbrowser_snapshot",
        "--decision-question",
        "Does the bound Sephora US/USD PDP render?",
        "--output",
        str(tmp_path / "packet"),
        "--sephora-market",
        "US",
        "--preflight-only",
    ]

    with pytest.raises(SystemExit) as exc_info:
        cloak_writer.main(
            [
                "--url",
                "https://www.sephora.com/product/tower-28-lipsoftie-P509397",
                *common,
            ]
        )

    assert exc_info.value.code == 2
    assert "country_switch=us" in capsys.readouterr().err
    assert cloak_writer.main(["--url", _SEPHORA_URL, *common]) == 0
    assert "no network capture attempted" in capsys.readouterr().out


def test_writer_preserves_but_rejects_unconfirmed_sephora_market(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def _unconfirmed_capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
        result = _fake_capture(**kwargs)
        result.metadata["pin_confirmed"] = False
        return CloakBrowserSnapshotSuccess(
            requested_url=result.requested_url,
            final_url="https://www.sephora.ca/product/tower-28-lipsoftie-P509397",
            title=result.title,
            rendered_dom=_sephora_dom(country="CA", currency="CAD"),
            visible_text="Tower 28 Beauty LipSoftie $22.00 CAD",
            screenshot_png=result.screenshot_png,
            metadata=result.metadata,
            warning_notes=result.warning_notes,
            limitation_notes=result.limitation_notes,
        )

    monkeypatch.setattr(
        cloak_writer, "fetch_cloakbrowser_snapshot_capture", _unconfirmed_capture
    )

    exit_code, message = _run_writer(tmp_path)

    assert exit_code == cloak_writer.SOURCE_DETAIL_SUFFICIENCY_EXIT_CODE
    assert cloak_writer.SEPHORA_MARKET_PIN_FAILURE_MODE_CHANGE in message
    manifest = json.loads(
        (tmp_path / "packet" / "manifest.json").read_text(encoding="utf-8")
    )
    assert cloak_writer.SEPHORA_MARKET_PIN_FAILURE_MODE_CHANGE in manifest[
        "visible_mode_changes"
    ]
    assert any(
        "MUST NOT be admitted as Sephora US/USD storefront evidence" in limitation
        for limitation in manifest["limitations"]
    )


def test_sephora_pin_enforcement_requires_true_boolean_and_sephora_host() -> None:
    assert (
        cloak_writer._sephora_market_pin_failure(
            sephora_market="US",
            final_url=_SEPHORA_URL,
            pin_confirmed=True,
        )
        is None
    )
    assert "not sephora.com" in (
        cloak_writer._sephora_market_pin_failure(
            sephora_market="US",
            final_url="https://www.sephora.ca/product/example",
            pin_confirmed=True,
        )
        or ""
    )
    assert "not confirmed" in (
        cloak_writer._sephora_market_pin_failure(
            sephora_market="US",
            final_url=_SEPHORA_URL,
            pin_confirmed=1,
        )
        or ""
    )
