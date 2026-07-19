from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from runners import run_source_capture_http_packet as http_writer
from source_capture.adapters.credo_us_market import (
    confirm_credo_us_market,
    validate_credo_us_market_url,
)
from source_capture.adapters.direct_http import DirectHttpCaptureSuccess
from source_capture.retail_pdp_projection import (
    build_retail_pdp_projection_from_packet_directory,
)


_HANDLE = "sos-save-our-skin-daily-rescue-facial-spray"
_URL = f"https://credobeauty.com/products/{_HANDLE}"


def _body(
    *,
    country: str = "US",
    currency: str = "USD",
    offer_currency: str = "USD",
    canonical_url: str = _URL,
    product_url: str = _URL,
    product_name: str = "SOS Daily Rescue Facial Spray",
    brand_name: str = "Tower 28",
) -> str:
    product = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product_name,
        "url": product_url,
        "sku": "210000007835",
        "brand": {"@type": "Brand", "name": brand_name},
        "offers": [
            {
                "@type": "Offer",
                "sku": "210000007834",
                "price": 28.0,
                "priceCurrency": offer_currency,
            },
            {
                "@type": "Offer",
                "sku": "210000007835",
                "price": 12.0,
                "priceCurrency": offer_currency,
                "availability": "https://schema.org/InStock",
            },
        ],
    }
    return (
        "<html><head>"
        f'<link rel="canonical" href="{canonical_url}">'
        f"<script>Shopify.currency = {json.dumps({'active': currency, 'rate': '1.0'})};"
        f"Shopify.country = {json.dumps(country)};</script>"
        '<script type="application/ld+json">'
        f"{json.dumps(product)}"
        "</script></head><body>Tower 28 SOS Daily Rescue Facial Spray $12</body></html>"
    )


def _fake_capture(*, body: str, final_url: str = _URL):
    def capture(**kwargs: Any) -> DirectHttpCaptureSuccess:
        return DirectHttpCaptureSuccess(
            requested_url=kwargs["url"],
            final_url=final_url,
            status=200,
            reason="OK",
            metadata={
                "requested_url": kwargs["url"],
                "final_url": final_url,
                "capture_timestamp": "2026-07-19T00:00:00Z",
            },
            body=body.encode("utf-8"),
            warning_notes=[],
            limitation_notes=[],
        )

    return capture


def _run_kwargs(output: Path) -> dict[str, Any]:
    return {
        "url": _URL,
        "source_family": "retail_pdp",
        "source_surface": "direct_http",
        "decision_question": "Does the bound Credo PDP confirm US/USD?",
        "output_directory": output,
        "capture_context": "offline test",
        "operator_category": "test",
        "capture_mode": http_writer.CaptureModeCategory.STRUCTURED_ACCESS,
        "session_id": None,
        "actor_audience_context": None,
        "visible_mode_changes": [],
        "source_publication_or_event": None,
        "source_edit_or_version": None,
        "cutoff_posture": None,
        "recapture_time": None,
        "re_capture_relationship": None,
        "warnings": [],
        "limitations": [],
        "retail_capture_profile": None,
        "timeout_seconds": 20,
        "max_bytes": 2_000_000,
        "credo_market": "US",
    }


def test_confirmation_accepts_bound_credo_country_currency_and_product() -> None:
    confirmation = confirm_credo_us_market(
        _body(),
        requested_url=_URL,
        final_url=_URL,
    )

    assert confirmation.confirmed is True
    assert confirmation.requested_product_handle == _HANDLE
    assert confirmation.observed_country_code == "US"
    assert confirmation.observed_currency_code == "USD"
    assert confirmation.observed_offer_currencies == ("USD",)
    assert confirmation.product_name == "SOS Daily Rescue Facial Spray"
    assert confirmation.brand_name == "Tower 28"
    assert confirmation.product_sku == "210000007835"


@pytest.mark.parametrize(
    "body",
    [
        "<html><body>credobeauty.com Tower 28 SOS $12 US USD</body></html>",
        _body(country="SG"),
        _body(currency="SGD"),
        _body(offer_currency="SGD"),
        _body(canonical_url="https://credobeauty.com/products/other-product"),
        _body(product_url="https://credobeauty.com/products/other-product"),
        _body(product_name=""),
        _body(brand_name=""),
        _body().replace(
            "Shopify.country = \"US\";",
            'Shopify.country = "US";Shopify.country = "SG";',
        ),
    ],
)
def test_confirmation_rejects_loose_split_malformed_or_conflicting_signals(
    body: str,
) -> None:
    assert (
        confirm_credo_us_market(
            body,
            requested_url=_URL,
            final_url=_URL,
        ).confirmed
        is False
    )


def test_confirmation_rejects_final_route_drift() -> None:
    confirmation = confirm_credo_us_market(
        _body(),
        requested_url=_URL,
        final_url="https://credobeauty.com/products/other-product",
    )

    assert confirmation.confirmed is False
    assert "final product handle" in confirmation.detail


def test_url_validation_requires_exact_https_credo_pdp() -> None:
    assert validate_credo_us_market_url(_URL) == _HANDLE
    for invalid in (
        f"http://credobeauty.com/products/{_HANDLE}",
        f"https://www.credobeauty.com/products/{_HANDLE}",
        "https://credobeauty.com/collections/tower-28",
        f"https://credobeauty.sg/products/{_HANDLE}",
    ):
        with pytest.raises(ValueError, match="credobeauty.com"):
            validate_credo_us_market_url(invalid)


def test_writer_accepts_packet_derives_pins_and_projects_bound_usd_offer(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        http_writer,
        "fetch_direct_http_capture",
        _fake_capture(body=_body()),
    )

    exit_code, output = http_writer.run_source_capture_http_packet(
        **_run_kwargs(tmp_path / "packet")
    )

    assert exit_code == 0
    assert output == str(tmp_path / "packet")
    metadata = json.loads(
        (
            tmp_path / "packet" / "raw" / "02_http_response_metadata.json"
        ).read_text(encoding="utf-8")
    )
    assert metadata["pin_confirmed"] is True
    assert metadata["bound_product_handle"] == _HANDLE
    assert metadata["country_code_confirmed"] == "US"
    assert metadata["currency_code_confirmed"] == "USD"
    assert metadata["delivery_location_posture"] == "unpinned"

    manifest = json.loads(
        (tmp_path / "packet" / "manifest.json").read_text(encoding="utf-8")
    )
    source_slice = manifest["source_slices"][0]
    assert source_slice["locale_pin"]["value"] == "US"
    assert source_slice["currency_pin"]["value"] == "USD"

    projection = build_retail_pdp_projection_from_packet_directory(
        packet_directory=tmp_path / "packet"
    )
    products = [
        row for row in projection.rows if row.row_kind == "retail_pdp_product"
    ]
    offers = [
        row for row in projection.rows if row.row_kind == "retail_variant_offer"
    ]
    assert len(products) == 1
    assert len(offers) == 1
    assert offers[0].source_visible_fields["sku"] == "210000007835"
    assert offers[0].source_visible_fields["price"] == "12.0"
    assert offers[0].source_visible_fields["price_currency"] == "USD"


def test_writer_preserves_typed_packet_and_exits_nonzero_when_pin_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        http_writer,
        "fetch_direct_http_capture",
        _fake_capture(body=_body(country="SG")),
    )

    exit_code, message = http_writer.run_source_capture_http_packet(
        **_run_kwargs(tmp_path / "failed")
    )

    assert exit_code == http_writer.SOURCE_DETAIL_SUFFICIENCY_EXIT_CODE
    assert message.startswith("credo_market_pin_failed: packet preserved")
    metadata = json.loads(
        (
            tmp_path / "failed" / "raw" / "02_http_response_metadata.json"
        ).read_text(encoding="utf-8")
    )
    assert metadata["pin_confirmed"] is False
    manifest = json.loads(
        (tmp_path / "failed" / "manifest.json").read_text(encoding="utf-8")
    )
    assert "credo_market_pin_failed" in manifest["visible_mode_changes"]
    assert any(
        "MUST NOT be admitted as Credo US/USD storefront evidence"
        in limitation
        for limitation in manifest["limitations"]
    )


def test_writer_rejects_manual_pins_and_cross_retailer_flag(
    tmp_path: Path,
) -> None:
    kwargs = _run_kwargs(tmp_path / "manual_pin")
    kwargs["currency_pin"] = http_writer.known_fact("manual USD declaration")
    with pytest.raises(ValueError, match="must not be combined"):
        http_writer.run_source_capture_http_packet(**kwargs)

    kwargs = _run_kwargs(tmp_path / "cross_retailer")
    kwargs["walmart_market"] = "US"
    with pytest.raises(ValueError, match="mutually exclusive"):
        http_writer.run_source_capture_http_packet(**kwargs)


def test_cli_exposes_only_us_credo_market_choice() -> None:
    parser = http_writer._build_parser()
    args = parser.parse_args(
        [
            "--url",
            _URL,
            "--source-family",
            "retail_pdp",
            "--decision-question",
            "Credo US/USD?",
            "--output",
            "packet",
            "--credo-market",
            "US",
        ]
    )

    assert args.credo_market == "US"
