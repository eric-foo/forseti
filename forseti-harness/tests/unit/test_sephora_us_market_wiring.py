from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from data_lake.root import DataLakeRoot
from runners import run_source_capture_cloakbrowser_packet as cloak_writer
from source_capture.adapters.cloakbrowser_snapshot import (
    CloakBrowserSnapshotSuccess,
    PreCaptureOutcome,
)
from source_capture.adapters.sephora_us_market import (
    SephoraUSMarketPlugin,
    confirm_sephora_us_market,
)
from source_capture.retail_capture_profiles import get_retail_capture_profile


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


def _sephora_grid_dom(
    *, country: str = "US", currency_code: str | None = "USD"
) -> str:
    render_query = json.dumps(
        {
            "channel": "rwd",
            "country": country,
            "language": "en",
            "urlPath": "/brand/summer-fridays",
        },
        separators=(",", ":"),
    )
    nth_brand: dict[str, object] = {
        "brandId": "6247",
        "displayName": "Summer Fridays",
        "shortName": "Summer Fridays",
        "resultId": "test-result",
        "targetUrl": "/brand/summer-fridays",
        "seoCanonicalUrl": "/brand/summer-fridays",
        "pageSize": 60,
        "totalProducts": 2,
        "products": [
            {
                "brandName": "Summer Fridays",
                "currentSku": {
                    "isNew": True,
                    "listPrice": "$24.00",
                    "skuId": "2968907",
                },
                "displayName": "Lip Butter Balm",
                "moreColors": 11,
                "pickupEligible": False,
                "productId": "P455936",
                "rating": 4.29,
                "reviews": 17635,
                "sameDayEligible": False,
                "targetUrl": "/product/lip-butter-balm-P455936?skuId=2968907",
            },
            {
                "brandName": "Summer Fridays",
                "currentSku": {
                    "listPrice": "$49.00",
                    "skuId": "2473361",
                },
                "displayName": "Jet Lag Mask",
                "moreColors": 0,
                "pickupEligible": False,
                "productId": "P429952",
                "rating": 4.2,
                "reviews": 6700,
                "sameDayEligible": False,
                "targetUrl": "/product/jet-lag-mask-P429952?skuId=2473361",
            },
        ],
    }
    if currency_code is not None:
        nth_brand["currencyCode"] = currency_code
    page_json = json.dumps(
        {"page": {"nthBrand": nth_brand}}, separators=(",", ":")
    )
    return (
        "<html><body><script>"
        f"Sephora.renderQueryParams = {render_query};Sephora.isSPA = true;"
        '</script><script id="linkStore" type="text/json">'
        f"{page_json}</script></body></html>"
    )


_US_DOM = _sephora_dom()
_COUNTRY_DIALOG_TEXT = "This site does not ship to your country."
_SEPHORA_URL = (
    "https://www.sephora.com/product/"
    "tower-28-lipsoftie-hydrating-tinted-lip-treatment-balm-P509397"
    "?country_switch=us&lang=en"
)
_SEPHORA_GRID_URL = (
    "https://www.sephora.com/brand/summer-fridays?country_switch=us"
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


def _fake_grid_capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
    pre_capture = kwargs["pre_capture"]
    assert isinstance(pre_capture, SephoraUSMarketPlugin)
    assert pre_capture.page_kind == "grid"
    dom = _sephora_grid_dom(currency_code=None)
    confirmation = pre_capture.confirm(dom)
    return CloakBrowserSnapshotSuccess(
        requested_url=kwargs["url"],
        final_url=kwargs["url"],
        title="Summer Fridays | Sephora",
        rendered_dom=dom,
        visible_text=(
            "Summer Fridays 2 Results Quicklook Lip Butter Balm $24.00 "
            "Quicklook Jet Lag Mask $49.00 1-2 of 2 Results"
        ),
        screenshot_png=b"\x89PNG\r\n\x1a\n",
        metadata={
            "capture_timestamp": "2026-07-21T00:00:00Z",
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


def test_grid_confirmation_admits_us_country_independently_of_currency() -> None:
    no_currency = confirm_sephora_us_market(
        _sephora_grid_dom(currency_code=None), page_kind="grid"
    )
    usd = confirm_sephora_us_market(_sephora_grid_dom(), page_kind="grid")
    cad = confirm_sephora_us_market(
        _sephora_grid_dom(currency_code="CAD"), page_kind="grid"
    )

    assert no_currency.confirmed is True
    assert "country=US" in no_currency.detail
    assert "currency remains un-pinned" in no_currency.detail
    assert usd.confirmed is True
    assert "currency code USD was observed separately" in usd.detail
    assert cad.confirmed is True
    assert "currency code(s) CAD" in cad.detail
    assert "not promoted to USD" in cad.detail
    assert (
        confirm_sephora_us_market(
            _sephora_grid_dom(country="CA"), page_kind="grid"
        ).confirmed
        is False
    )
    assert (
        confirm_sephora_us_market(
            _sephora_grid_dom() + f"<div>{_COUNTRY_DIALOG_TEXT}</div>",
            page_kind="grid",
        ).confirmed
        is False
    )


def test_grid_confirmation_fails_closed_on_contradictory_country_state() -> None:
    contradictory = _sephora_grid_dom() + (
        '<script>Sephora.renderQueryParams = {"country":"CA"};</script>'
    )

    grid = confirm_sephora_us_market(contradictory, page_kind="grid")

    assert grid.confirmed is False
    assert "unanimous Sephora.renderQueryParams country=US" in grid.detail
    assert "'US', 'CA'" in grid.detail
    # PDP admission is deliberately unchanged: its Sephora-sold USD Offer is an
    # independent second conjunct, so it is not narrowed by the grid-only rule.
    assert (
        confirm_sephora_us_market(
            _sephora_dom()
            + '<script>Sephora.renderQueryParams = {"country":"CA"};</script>'
        ).confirmed
        is True
    )


def test_grid_currency_absence_is_not_asserted_when_grid_state_is_unreadable() -> None:
    unreadable = _sephora_grid_dom(currency_code=None) + (
        '<script id="linkStore" type="text/json">{}</script>'
    )

    confirmation = confirm_sephora_us_market(unreadable, page_kind="grid")

    # The country route is still confirmable; currency is a separate typed fact
    # and an unreadable state must not be reported as an observed absent code.
    assert confirmation.confirmed is True
    assert "grid currency state was unreadable" in confirmation.detail
    assert "exposed no explicit currency code" not in confirmation.detail


def test_grid_note_reports_country_only_admission() -> None:
    plugin = SephoraUSMarketPlugin(target_url=_SEPHORA_GRID_URL, page_kind="grid")
    outcome = PreCaptureOutcome(attempted=True, steps_completed=True, reason=None)
    grid_dom = _sephora_grid_dom(currency_code=None)

    confirmed_note = plugin.note(outcome, plugin.confirm(grid_dom))
    rejected_note = plugin.note(
        outcome,
        plugin.confirm(grid_dom + f"<div>{_COUNTRY_DIALOG_TEXT}</div>"),
    )

    assert confirmed_note.startswith("declared_storefront_country:")
    assert "CONFIRMED as US" in confirmed_note
    assert "currency remains un-pinned" in confirmed_note
    assert "US/USD" not in confirmed_note
    assert "NOT confirmed" in rejected_note
    assert (
        "treat storefront country, currency, and delivery location as un-pinned"
        in rejected_note
    )


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
    assert SephoraUSMarketPlugin(target_url=_SEPHORA_URL).humanize is True


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


def test_writer_requires_and_emits_sephora_grid_projection_sidecar(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_grid_capture
    )
    profile = get_retail_capture_profile("sephora_grid_aggregate")

    with pytest.raises(ValueError, match="retail-grid-projection-output"):
        _run_writer(
            tmp_path,
            url=_SEPHORA_GRID_URL,
            decision_question="What is the Summer Fridays grid?",
            retail_capture_profile=profile,
        )

    projection_path = tmp_path / "projection" / "retail_grid_projection.json"
    exit_code, output = _run_writer(
        tmp_path,
        url=_SEPHORA_GRID_URL,
        decision_question="What is the Summer Fridays grid?",
        retail_capture_profile=profile,
        retail_grid_projection_output=projection_path,
    )

    assert exit_code == 0
    assert output == (
        f"raw packet preserved at {tmp_path / 'packet'}; "
        f"projection preserved at {projection_path}"
    )
    projection = json.loads(projection_path.read_text(encoding="utf-8"))
    manifest = json.loads((tmp_path / "packet" / "manifest.json").read_text())
    preserved_paths = [item["relative_packet_path"] for item in manifest["preserved_files"]]
    assert any(path.endswith("content_record.json") for path in preserved_paths)
    assert not any(path.endswith("rendered_dom.html") for path in preserved_paths)
    assert not any(path.endswith("visible_text.txt") for path in preserved_paths)
    content_path = next(
        tmp_path / "packet" / path
        for path in preserved_paths
        if path.endswith("content_record.json")
    )
    content_body = content_path.read_bytes()
    content_record = json.loads(content_body)
    assert content_record["content_record_version"] == "sephora_grid_content_v1"
    assert projection["completeness"]["status"] == "complete"
    assert projection["completeness"]["page_declared_result_count"] == 2
    assert projection["completeness"]["extracted_unique_parent_count"] == 2
    assert projection["source_visible_grid_facts"]["subject_binding_confirmed"] is True
    assert projection["rows"][0]["raw_anchor"]["sha256"] == hashlib.sha256(
        content_body
    ).hexdigest()


def test_writer_automatically_files_grid_projection_in_data_root(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_grid_capture
    )
    root = DataLakeRoot.for_test(tmp_path / "lake")
    profile = get_retail_capture_profile("sephora_grid_aggregate")

    exit_code, output = _run_writer(
        tmp_path,
        url=_SEPHORA_GRID_URL,
        decision_question="What is the Summer Fridays grid?",
        output_directory=None,
        data_root=root,
        retail_capture_profile=profile,
    )

    assert exit_code == 0
    projection_path = Path(
        output.removeprefix(
            "raw sample not retained; derived observation preserved at "
        )
    )
    projection = json.loads(projection_path.read_text(encoding="utf-8"))
    assert root.list_committed_packet_ids() == []
    assert projection["projection_version"] == "v1"
    assert projection["packet_id"] is None
    assert projection["capture_event"]["raw_sample_packet_id"] is None
    assert projection["completeness"]["status"] == "complete"
    assert projection_path.parent.name == "projection_retail_grid"


def test_sephora_grid_explicit_raw_sample_projects_the_grid_exactly_once(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_grid_capture
    )
    root = DataLakeRoot.for_test(tmp_path / "lake")

    exit_code, output = _run_writer(
        tmp_path,
        url=_SEPHORA_GRID_URL,
        decision_question="What is the Summer Fridays grid?",
        output_directory=None,
        data_root=root,
        retail_capture_profile=get_retail_capture_profile("sephora_grid_aggregate"),
        retain_retail_grid_raw_sample=True,
    )

    assert exit_code == 0
    raw_text, projection_text = output.split("; derived observation preserved at ", 1)
    raw_path = Path(raw_text.removeprefix("raw sample preserved at "))
    projection = json.loads(Path(projection_text).read_text(encoding="utf-8"))
    loaded = root.load_raw_packet(raw_path.name)
    assert any(
        item["relative_packet_path"].endswith("cloakbrowser_rendered_dom.html")
        for item in loaded.manifest["preserved_files"]
    )
    assert projection["capture_event"]["raw_sample_packet_id"] == raw_path.name
    assert projection["completeness"]["status"] == "complete"
    assert projection["completeness"]["extracted_unique_parent_count"] == 2
    assert projection["completeness"]["extracted_placement_count"] == 2
    assert projection["completeness"]["duplicate_placement_count"] == 0
    assert all(
        row["raw_ref"]["packet_id"] == raw_path.name for row in projection["rows"]
    )


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
        "MUST NOT be admitted as the asserted Sephora storefront evidence"
        in limitation
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
