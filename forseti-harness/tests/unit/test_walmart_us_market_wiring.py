from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from runners import run_source_capture_http_packet as http_writer
from source_capture.adapters.direct_http import DirectHttpCaptureSuccess
from source_capture.adapters.walmart_us_market import (
    confirm_walmart_us_market,
    validate_walmart_us_market_url,
)
from source_capture.retail_capture_profiles import get_retail_capture_profile
from source_capture.retail_pdp_projection import (
    build_retail_pdp_projection_from_packet_directory,
)


_ITEM_ID = "2150828728"
_URL = (
    "https://www.walmart.com/ip/Vitamasques-Cherry-Vegan-Collagen-Lip-Mask-"
    f"Moisturise-Plump-One-Patch/{_ITEM_ID}"
)


def _body(
    *,
    item_id: str = _ITEM_ID,
    currency: str = "USD",
    page_postal: str = "95829",
    product_postal: str = "95829",
    country_code: Any = None,
    use_lazy_modules: bool = False,
) -> str:
    if country_code is None:
        country_code = ["US"]
    country_module = {"targeting": {"countryCode": country_code}}
    content_layout: dict[str, Any] = {
        "pageMetadata": {"location": {"postalCode": page_postal}},
        "modules": [] if use_lazy_modules else [country_module],
    }
    if use_lazy_modules:
        content_layout["lazyModules"] = [country_module]
    next_data = {
        "props": {
            "pageProps": {
                "initialData": {
                    "data": {
                        "product": {
                            "usItemId": item_id,
                            "name": "Vitamasques Cherry Vegan Collagen Lip Mask",
                            "priceInfo": {
                                "currentPrice": {
                                    "price": 2.97,
                                    "currencyUnit": currency,
                                }
                            },
                            "location": {"postalCode": product_postal},
                            "averageRating": 4.4,
                            "numberOfReviews": 41,
                        },
                        "contentLayout": content_layout,
                    }
                }
            }
        }
    }
    return (
        "<html><head><script id=\"__NEXT_DATA__\" type=\"application/json\">"
        f"{json.dumps(next_data)}"
        "</script></head><body>"
        "Vitamasques Cherry Vegan Collagen Lip Mask"
        "</body></html>"
    )


def _fake_capture(
    *,
    body: str,
    final_url: str = _URL,
):
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
        "decision_question": "Does the bound Walmart PDP confirm US/USD?",
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
        "retail_capture_profile": get_retail_capture_profile(
            "walmart_pdp_aggregate"
        ),
        "timeout_seconds": 20,
        "max_bytes": 1_000_000,
        "walmart_market": "US",
    }


@pytest.mark.parametrize(
    ("country_code", "expected_shape"),
    [
        ("US", "scalar"),
        (["US"], "single_item_list"),
    ],
)
def test_confirmation_accepts_only_bound_walmart_country_serializations(
    country_code: Any,
    expected_shape: str,
) -> None:
    confirmation = confirm_walmart_us_market(
        _body(country_code=country_code),
        requested_url=_URL,
        final_url=_URL,
    )

    assert confirmation.confirmed is True
    assert confirmation.requested_item_id == _ITEM_ID
    assert confirmation.product_item_id == _ITEM_ID
    assert confirmation.observed_currency_code == "USD"
    assert confirmation.observed_postal_code == "95829"
    assert confirmation.country_signal_shape == expected_shape


def test_confirmation_accepts_immediate_content_layout_lazy_module() -> None:
    confirmation = confirm_walmart_us_market(
        _body(use_lazy_modules=True),
        requested_url=_URL,
        final_url=_URL,
    )

    assert confirmation.confirmed is True
    assert confirmation.country_signal_shape == "single_item_list"


@pytest.mark.parametrize(
    "body",
    [
        "<html><body>www.walmart.com US USD $2.97 2150828728</body></html>",
        "<script id=\"__NEXT_DATA__\">{broken}</script>",
        _body(item_id="9999999"),
        _body(currency="SGD"),
        _body(page_postal="10001", product_postal="95829"),
        _body(country_code="SG"),
        _body(country_code=["US", "CA"]),
        _body(country_code=[]),
        _body(country_code={"country": "US"}),
    ],
)
def test_confirmation_rejects_loose_malformed_split_or_conflicting_signals(
    body: str,
) -> None:
    assert (
        confirm_walmart_us_market(
            body,
            requested_url=_URL,
            final_url=_URL,
        ).confirmed
        is False
    )


def test_confirmation_rejects_final_route_drift() -> None:
    confirmation = confirm_walmart_us_market(
        _body(),
        requested_url=_URL,
        final_url=_URL.replace(_ITEM_ID, "9999999"),
    )

    assert confirmation.confirmed is False
    assert "final Walmart item ID" in confirmation.detail


def test_url_validation_requires_exact_https_walmart_pdp() -> None:
    assert validate_walmart_us_market_url(_URL) == _ITEM_ID
    for invalid in (
        "http://www.walmart.com/ip/example/2150828728",
        "https://www.walmart.ca/ip/example/2150828728",
        "https://www.walmart.com/search?q=2150828728",
    ):
        with pytest.raises(ValueError, match="www.walmart.com"):
            validate_walmart_us_market_url(invalid)


def test_writer_accepts_asserted_packet_and_derives_country_currency_pins(
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
            tmp_path
            / "packet"
            / "raw"
            / "02_http_response_metadata.json"
        ).read_text(encoding="utf-8")
    )
    assert metadata["pin_confirmed"] is True
    assert metadata["bound_item_id"] == _ITEM_ID
    assert metadata["country_code_confirmed"] == "US"
    assert metadata["currency_code_confirmed"] == "USD"
    assert metadata["country_code_signal_shape"] == "single_item_list"
    assert metadata["observed_location_posture"] == "origin_derived_unpinned"

    manifest = json.loads(
        (tmp_path / "packet" / "manifest.json").read_text(encoding="utf-8")
    )
    source_slice = manifest["source_slices"][0]
    assert source_slice["locale_pin"]["status"] == "known"
    assert source_slice["locale_pin"]["value"] == "US"
    assert source_slice["currency_pin"]["status"] == "known"
    assert source_slice["currency_pin"]["value"] == "USD"
    assert any(
        "origin-derived page context" in limitation
        for limitation in manifest["limitations"]
    )
    projection = build_retail_pdp_projection_from_packet_directory(
        packet_directory=tmp_path / "packet"
    )
    offers = [row for row in projection.rows if row.row_kind == "retail_variant_offer"]
    assert len(offers) == 1
    assert offers[0].source_visible_fields["product_id"] == _ITEM_ID
    assert offers[0].source_visible_fields["price_currency"] == "USD"


def test_writer_preserves_typed_packet_and_exits_nonzero_when_pin_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        http_writer,
        "fetch_direct_http_capture",
        _fake_capture(body=_body(country_code=["US", "CA"])),
    )

    exit_code, message = http_writer.run_source_capture_http_packet(
        **_run_kwargs(tmp_path / "failed")
    )

    assert exit_code == http_writer.SOURCE_DETAIL_SUFFICIENCY_EXIT_CODE
    assert message.startswith("walmart_market_pin_failed: packet preserved")
    metadata = json.loads(
        (
            tmp_path
            / "failed"
            / "raw"
            / "02_http_response_metadata.json"
        ).read_text(encoding="utf-8")
    )
    assert metadata["pin_confirmed"] is False
    manifest = json.loads(
        (tmp_path / "failed" / "manifest.json").read_text(encoding="utf-8")
    )
    assert "walmart_market_pin_failed" in manifest["visible_mode_changes"]
    assert any(
        "MUST NOT be admitted as Walmart US/USD storefront evidence"
        in limitation
        for limitation in manifest["limitations"]
    )


def test_writer_rejects_wrong_profile_and_manual_pin_declarations(
    tmp_path: Path,
) -> None:
    kwargs = _run_kwargs(tmp_path / "wrong_profile")
    kwargs["retail_capture_profile"] = None
    with pytest.raises(ValueError, match="walmart_pdp_aggregate"):
        http_writer.run_source_capture_http_packet(**kwargs)

    kwargs = _run_kwargs(tmp_path / "manual_pin")
    kwargs["currency_pin"] = http_writer.known_fact("manual USD declaration")
    with pytest.raises(ValueError, match="must not be combined"):
        http_writer.run_source_capture_http_packet(**kwargs)


def test_cli_exposes_only_us_walmart_market_choice() -> None:
    parser = http_writer._build_parser()
    args = parser.parse_args(
        [
            "--url",
            _URL,
            "--decision-question",
            "Walmart US/USD?",
            "--output",
            "packet",
            "--retail-capture-profile",
            "walmart_pdp_aggregate",
            "--walmart-market",
            "US",
        ]
    )

    assert args.walmart_market == "US"
