from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from source_capture.models import known_fact
from source_capture.retail_portfolio_onboarding import (
    RetailPortfolioOnboardingError,
    build_retail_portfolio_onboarding,
    load_portfolio_commission,
    write_retail_portfolio_onboarding,
)
from source_capture.writer import write_local_source_capture_packet


def test_multi_retailer_composition_preserves_identity_and_typed_residuals(
    tmp_path: Path,
) -> None:
    commission_path, target_raw = _fixture(tmp_path)
    commission = load_portfolio_commission(commission_path)

    first = build_retail_portfolio_onboarding(
        commission=commission, base_directory=tmp_path
    )
    second = build_retail_portfolio_onboarding(
        commission=commission, base_directory=tmp_path
    )

    assert first == second
    assert first["owned_parent_count"] == 3
    target = next(
        item for item in first["coverage_by_retailer"] if item["retailer"] == "target"
    )
    assert target["covered_owned_parent_ids"] == ["p1", "p2"]
    assert target["covered_owned_parent_count"] == 2
    assert target["exact_listing_count"] == 2
    ulta = next(
        item for item in first["coverage_by_retailer"] if item["retailer"] == "ulta"
    )
    assert ulta["covered_owned_parent_ids"] == ["p1", "p2"]
    assert ulta["exact_listing_count"] == 2
    duplicate = next(
        item
        for item in first["listing_identities"]
        if item["source_product_id"] == "100"
    )
    assert len(duplicate["occurrence_row_ids"]) == 2
    residuals = first["coverage_residuals"]
    assert "DUPLICATE_LISTING:target:100:occurrences=2" in residuals
    assert any(item.startswith("VARIANT_URL:target:200:") for item in residuals)
    assert any(item.startswith("BUNDLE_SET:target:300:") for item in residuals)
    assert any(item.startswith("AMBIGUOUS_MATCH:target:400:") for item in residuals)
    assert any(item.startswith("UNMATCHED_MATCH:target:500:") for item in residuals)
    assert "MISSING_MATERIAL_VARIANT:target:p1:p1-v2" in residuals
    assert "PARENT_NOT_LISTED:target:p3" in residuals
    assert "RETAILER_OUTCOME:sephora:NOT_LISTED" in residuals
    assert len(first["pdp_baselines"]) == 4
    assert all("hero" not in key.lower() for key in _all_keys(first))
    assert hashlib.sha256(target_raw.read_bytes()).hexdigest() == hashlib.sha256(
        _target_html()
    ).hexdigest()


def test_writer_refuses_rerun_without_touching_raw(tmp_path: Path) -> None:
    commission_path, target_raw = _fixture(tmp_path)
    output = tmp_path / "coverage.json"
    raw_hash = hashlib.sha256(target_raw.read_bytes()).hexdigest()

    write_retail_portfolio_onboarding(
        commission_path=commission_path, output_path=output
    )
    with pytest.raises(RetailPortfolioOnboardingError, match="refusing overwrite"):
        write_retail_portfolio_onboarding(
            commission_path=commission_path, output_path=output
        )

    assert hashlib.sha256(target_raw.read_bytes()).hexdigest() == raw_hash


def test_missing_exact_listing_baseline_fails_closed(tmp_path: Path) -> None:
    commission_path, _ = _fixture(tmp_path)
    payload = json.loads(commission_path.read_text(encoding="utf-8"))
    payload["pdp_baselines"].pop()
    commission_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(
        RetailPortfolioOnboardingError, match="PDP baselines must equal"
    ):
        build_retail_portfolio_onboarding(
            commission=load_portfolio_commission(commission_path),
            base_directory=tmp_path,
        )


def test_baseline_raw_hash_mismatch_fails_closed(tmp_path: Path) -> None:
    commission_path, _ = _fixture(tmp_path)
    payload = json.loads(commission_path.read_text(encoding="utf-8"))
    baseline_dir = Path(payload["pdp_baselines"][0]["packet_directory"])
    raw_path = next((baseline_dir / "raw").iterdir())
    raw_path.write_bytes(b"tampered")

    with pytest.raises(ValueError, match="sha256 mismatch|size mismatch"):
        build_retail_portfolio_onboarding(
            commission=load_portfolio_commission(commission_path),
            base_directory=tmp_path,
        )


def test_acquisition_judgment_key_is_rejected(tmp_path: Path) -> None:
    commission_path, _ = _fixture(tmp_path)
    payload = json.loads(commission_path.read_text(encoding="utf-8"))
    payload["hero_label"] = "p1"
    commission_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(RetailPortfolioOnboardingError, match="forbidden Judgment key"):
        load_portfolio_commission(commission_path)


def _all_keys(value: object) -> list[str]:
    if isinstance(value, dict):
        return [str(key) for key in value] + [
            key for child in value.values() for key in _all_keys(child)
        ]
    if isinstance(value, list):
        return [key for child in value for key in _all_keys(child)]
    return []


def _fixture(tmp_path: Path) -> tuple[Path, Path]:
    grid_dir, target_raw = _packet(
        tmp_path,
        name="target-grid",
        body=_target_html(),
        source_family="retail_grid",
        source_surface="cloakbrowser_snapshot",
        locator="https://www.target.com/s?searchTerm=example",
    )
    ulta_grid_dir, _ = _packet(
        tmp_path,
        name="ulta-grid",
        body=_ulta_grid_html(),
        source_family="retail_grid",
        source_surface="cloakbrowser_snapshot",
        locator="https://www.ulta.com/brand/example",
    )
    p1_url = "https://www.target.com/p/one/-/A-100"
    p2_url = "https://www.target.com/p/two/-/A-200?preselect=p2-v1"
    p1_dir, _ = _packet(
        tmp_path,
        name="target-pdp-100",
        body=b"full raw PDP 100",
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        locator=p1_url,
    )
    p2_dir, _ = _packet(
        tmp_path,
        name="target-pdp-200",
        body=b"full raw PDP 200",
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        locator=p2_url,
    )
    ulta_p1_url = (
        "https://www.ulta.com/p/moisture-surge-pimprod2056072?sku=2639131"
    )
    ulta_p2_url = "https://www.ulta.com/p/almost-lipstick-VP11111?sku=2253011"
    ulta_p1_dir, _ = _packet(
        tmp_path,
        name="ulta-pdp-2639131",
        body=b"full raw Ulta PDP 2639131",
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        locator=ulta_p1_url,
    )
    ulta_p2_dir, _ = _packet(
        tmp_path,
        name="ulta-pdp-2253011",
        body=b"full raw Ulta PDP 2253011",
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        locator=ulta_p2_url,
    )
    reconciliations = [
        _reconciliation(0, "100", p1_url, "PARENT", "EXACT", ["p1"], ["p1-v1"]),
        _reconciliation(1, "100", p1_url, "PARENT", "EXACT", ["p1"], ["p1-v1"]),
        _reconciliation(2, "200", p2_url, "VARIANT_URL", "EXACT", ["p2"], ["p2-v1"]),
        _reconciliation(3, "300", "https://www.target.com/p/set/-/A-300",
            "BUNDLE_SET", "EXACT", ["p1", "p2"], []),
        _reconciliation(4, "400", "https://www.target.com/p/ambiguous/-/A-400",
            "PARENT", "AMBIGUOUS", ["p2", "p3"], []),
        _reconciliation(5, "500", "https://www.target.com/p/unmatched/-/A-500",
            "PARENT", "UNMATCHED", [], []),
        {
            "retailer": "ulta",
            "grid_row_id": "slice_01:grid:ulta:pimprod2056072",
            "source_product_id": "pimprod2056072",
            "listing_url": ulta_p1_url,
            "listing_kind": "PARENT",
            "match_status": "EXACT",
            "owned_parent_ids": ["p1"],
            "material_variant_ids": [],
        },
        {
            "retailer": "ulta",
            "grid_row_id": "slice_01:grid:ulta:VP11111",
            "source_product_id": "VP11111",
            "listing_url": ulta_p2_url,
            "listing_kind": "PARENT",
            "match_status": "EXACT",
            "owned_parent_ids": ["p2"],
            "material_variant_ids": [],
        },
    ]
    payload = {
        "company_id": "example-company",
        "owned_census": {
            "source_packet_id": "owned-census-packet",
            "parents": [
                {"owned_parent_id": "p1", "name": "One",
                    "owned_url": "https://example.test/one",
                    "material_variant_ids": ["p1-v1", "p1-v2"]},
                {"owned_parent_id": "p2", "name": "Two",
                    "owned_url": "https://example.test/two",
                    "material_variant_ids": ["p2-v1"]},
                {"owned_parent_id": "p3", "name": "Three",
                    "owned_url": "https://example.test/three",
                    "material_variant_ids": []},
            ],
        },
        "retailer_outcomes": [
            {"retailer": "sephora", "status": "NOT_LISTED",
                "evidence_refs": ["receipt:sephora:not-listed"]},
            {"retailer": "ulta", "status": "GRID_CAPTURED_COMPLETE",
                "evidence_refs": ["packet:ulta-grid"],
                "grid_packet_directory": str(ulta_grid_dir)},
            {"retailer": "target", "status": "GRID_CAPTURED_INCOMPLETE",
                "evidence_refs": ["packet:target-grid"],
                "grid_packet_directory": str(grid_dir)},
            {"retailer": "amazon", "status": "MARKET_UNPINNED",
                "evidence_refs": ["receipt:amazon:unpinned"]},
        ],
        "listing_reconciliations": reconciliations,
        "pdp_baselines": [
            {"retailer": "target", "source_product_id": "100",
                "packet_directory": str(p1_dir)},
            {"retailer": "target", "source_product_id": "200",
                "packet_directory": str(p2_dir)},
            {"retailer": "ulta", "source_product_id": "pimprod2056072",
                "packet_directory": str(ulta_p1_dir)},
            {"retailer": "ulta", "source_product_id": "VP11111",
                "packet_directory": str(ulta_p2_dir)},
        ],
    }
    commission_path = tmp_path / "commission.json"
    commission_path.write_text(
        f"{json.dumps(payload, indent=2, sort_keys=True)}\n", encoding="utf-8"
    )
    return commission_path, target_raw


def _packet(
    tmp_path: Path,
    *,
    name: str,
    body: bytes,
    source_family: str,
    source_surface: str,
    locator: str,
) -> tuple[Path, Path]:
    source = tmp_path / f"{name}.bin"
    source.write_bytes(body)
    packet_dir = tmp_path / f"{name}-packet"
    write_local_source_capture_packet(
        output_directory=packet_dir,
        input_files=[source],
        source_family=source_family,
        source_surface=source_surface,
        source_locator=known_fact(locator),
        decision_question="unit test portfolio onboarding",
        capture_context="unit test",
    )
    raw_path = next((packet_dir / "raw").iterdir())
    return packet_dir, raw_path


def _reconciliation(
    index: int,
    product_id: str,
    url: str,
    listing_kind: str,
    match_status: str,
    parents: list[str],
    variants: list[str],
) -> dict[str, object]:
    return {
        "retailer": "target",
        "grid_row_id": f"slice_01:grid:target:{index}:{product_id}",
        "source_product_id": product_id,
        "listing_url": url,
        "listing_kind": listing_kind,
        "match_status": match_status,
        "owned_parent_ids": parents,
        "material_variant_ids": variants,
    }


def _ulta_grid_html() -> bytes:
    def card(sku: str, href: str, name: str) -> str:
        return (
            f'<li data-test="products-list-item" data-sku-id="{sku}">'
            f'<a href="{href}">'
            '<span class="pal-c-ProductCardBody--brandName">Example</span>'
            f'<span class="pal-c-ProductCardBody--title">{name}</span></a>'
            '<span class="pal-c-ProductCardBody--price">$25.00</span>'
            '<span class="pal-c-Ratings"><span class="sr-only">'
            '4.5 out of 5 stars ; 100 reviews</span></span>'
            '<span class="pal-c-ProductCardHeader__variant">2 sizes</span>'
            "<button>Add to bag</button></li>"
        )

    cards = [
        card(
            "2639131",
            "/p/moisture-surge-pimprod2056072?sku=2639131",
            "Moisture Surge",
        ),
        card(
            "2253011",
            "https://www.ulta.com/p/almost-lipstick-VP11111?sku=2253011",
            "Almost Lipstick",
        ),
        card(
            "2639131",
            "/p/moisture-surge-pimprod2056072?sku=2639131",
            "Moisture Surge",
        ),
    ]
    return (
        '<html lang="en-US"><head><script>window.__APP_LOCALE__="en-US";'
        'fetch("/graphql?ultasite=en-us")</script></head><body>'
        '<h1>Example</h1><ul data-test="products-list">'
        + "".join(cards)
        + "</ul><p>You have viewed 3 of 3</p></body></html>"
    ).encode("utf-8")


def _target_html() -> bytes:
    cards = [
        ("100", "/p/one/-/A-100", "One"),
        ("100", "/p/one/-/A-100", "One duplicate"),
        ("200", "/p/two/-/A-200?preselect=p2-v1", "Two variant"),
        ("300", "/p/set/-/A-300", "Set"),
        ("400", "/p/ambiguous/-/A-400", "Ambiguous"),
        ("500", "/p/unmatched/-/A-500", "Unmatched"),
    ]
    return "".join(
        f'<div data-focusid="{product_id}_product_card">'
        f'<a href="{url}" aria-label="{name}" '
        'data-test="@web/ProductCard/title"></a></div>'
        for product_id, url, name in cards
    ).encode("utf-8")
