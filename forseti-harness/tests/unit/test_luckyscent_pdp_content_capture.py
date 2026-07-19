from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Callable

import pytest

from runners import run_source_capture_cloakbrowser_packet as runner
from runners.run_luckyscent_pdp_parser_fit_check import (
    ParserFitCheckError,
    check_luckyscent_pdp_parser_fit,
    run_luckyscent_pdp_parser_fit_check,
)
from source_capture import CaptureModeCategory
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
from source_capture.content_capture import RenderedContentCaptureSpec
from source_capture.models import SourceCapturePacket
from source_capture.retail_capture_profiles import get_retail_capture_profile
from source_capture.retail_pdp_projection import (
    LUCKYSCENT_PDP_CONTENT_RECORD_KIND,
    LUCKYSCENT_PDP_PARSER_VERSION,
    build_luckyscent_pdp_aggregate_content_record,
    build_retail_pdp_projection_from_packet_directory,
)
from source_capture.retail_pdp_silver import build_retail_pdp_silver_records


_URL = "https://www.luckyscent.com/products/bread-and-roses-by-pearfat-parfum"
_VARIANTS = [
    {
        "@type": "Product",
        "name": "Bread and Roses - 50ml",
        "size": "50ml",
        "sku": "1016005",
        "url": f"{_URL}?variant=1",
        "offers": {
            "@type": "Offer",
            "price": "120.0",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "seller": {"@type": "Organization", "name": "Luckyscent"},
        },
    },
    {
        "@type": "Product",
        "name": "Bread and Roses - 15ml",
        "size": "15ml",
        "sku": "1016005_R",
        "url": f"{_URL}?variant=2",
        "offers": {
            "@type": "Offer",
            "price": "45.0",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "seller": {"@type": "Organization", "name": "Luckyscent"},
        },
    },
    {
        "@type": "Product",
        "name": "Bread and Roses - 1ml spray",
        "size": "1ml spray",
        "sku": "1016005_S",
        "url": f"{_URL}?variant=3",
        "offers": {
            "@type": "Offer",
            "price": "5.0",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "seller": {"@type": "Organization", "name": "Luckyscent"},
        },
    },
]
_PRODUCT_GROUP = {
    "@context": "https://schema.org",
    "@type": "ProductGroup",
    "productGroupID": "shopify_ZZ_9980138127681",
    "name": "Bread and Roses",
    "description": (
        "Fresh baguette warmth and red rose petals meet sweet orange, cocoa and "
        "nutmeg over resinous labdanum in a cozy gourmand floral."
    ),
    "url": _URL,
    "brand": {"@type": "Brand", "name": "Pearfat Parfum"},
    "hasVariant": _VARIANTS,
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": 3.75,
        "reviewCount": 8,
    },
}
_PRODUCT_RATING = {
    "@context": "http://schema.org",
    "@type": "Product",
    "@id": f"{_URL}#product",
    "name": "Bread and Roses",
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": 3.75,
        "reviewCount": 8,
    },
}
_RECOMMENDATION = {
    "@context": "https://schema.org",
    "@type": "Product",
    "@id": "https://www.luckyscent.com/products/unrelated#product",
    "name": "Unrelated Footer Recommendation",
    "offers": {
        "@type": "Offer",
        "price": "999",
        "priceCurrency": "USD",
        "seller": {"name": "Wrong Seller"},
    },
}


def _review(index: int) -> str:
    rating = (5, 4, 2, 5, 5, 5, 2, 2)[index]
    variant = ("1ml spray", None, "1ml spray", None, "15ml", "1ml spray", "1ml spray", None)[
        index
    ]
    variant_html = (
        '<div class="jdgm-rev__prod-variant-wrapper">'
        '<span class="jdgm-rev__variant-label"></span>'
        f"<span>{variant}</span></div>"
        if variant
        else ""
    )
    return (
        '<div class="jdgm-rev jdgm-divider-top jdgm--done-setup" '
        f'data-verified-buyer="{"true" if index != 1 else "false"}" '
        f'data-review-id="review-{index + 1}" '
        'data-product-title="Bread and Roses" '
        'data-product-url="/products/bread-and-roses-by-pearfat-parfum">'
        f'<span class="jdgm-rev__rating" data-score="{rating}"></span>'
        f'<span class="jdgm-rev__timestamp" data-content="2026-0{index + 1}-01 00:00:00 UTC">'
        f"0{index + 1}/01/2026</span>"
        f'<span class="jdgm-rev__author">Reviewer {index + 1}</span>'
        '<span class="jdgm-rev__location">United States</span>'
        f'<div class="jdgm-rev__body"><p>Target review body {index + 1}.</p></div>'
        f"{variant_html}"
        '<div class="jdgm-rev__transparency-badge" '
        'data-badge-type="review_collected_via_store_invitation">'
        "Review collected via store invitation</div></div>"
    )


_HISTOGRAM = "".join(
    '<div class="jdgm-histogram__row" '
    f'data-rating="{stars}" data-frequency="{count}" data-percentage="{percent}"></div>'
    for stars, count, percent in ((5, 4, 50), (4, 1, 13), (3, 0, 0), (2, 3, 38), (1, 0, 0))
)
_DOM = (
    "<html><head>"
    f'<script type="application/ld+json">{json.dumps(_PRODUCT_GROUP, separators=(",", ":"))}</script>'
    f'<script type="application/ld+json">{json.dumps(_PRODUCT_RATING, separators=(",", ":"))}</script>'
    f'<script type="application/ld+json">{json.dumps(_RECOMMENDATION, separators=(",", ":"))}</script>'
    "</head><body><main class=\"ProductHero\">"
    + _HISTOGRAM
    + "".join(_review(index) for index in range(8))
    + '<div class="jdgm-paginate"></div></main></body></html>'
)
_VISIBLE_TEXT = """
Bread and Roses
Pearfat Parfum
3.8
(8)
$120
Size: 50ml
50ml
15ml
1ml Spray Sample
Add to Cart
Gender
Unisex
Concentration
Eau de Parfum
Main Note
Rose
Country
United States
Released
2024
Fragrance Notes
Fresh Baguette, Sweet Orange, Familiar Warmth, Red Rose Petals, Cocoa, Nutmeg, Labdanum
Fragrance Style
Floral, Floral - Spicy, Gourmand, Resinous / Balsamic, Spicy
The Scoop
Bread, roses, and warm spice meet in the source-visible product description.
You May Also Like
Customer Reviews
3.75 out of 5
"""


def _logical_name(relative_packet_path: str) -> str:
    return re.sub(r"^\d+_", "", Path(relative_packet_path).name)


def _success(
    *,
    pin_confirmed: bool = True,
    rendered_dom: str = _DOM,
    visible_text: str = _VISIBLE_TEXT,
) -> CloakBrowserSnapshotSuccess:
    return CloakBrowserSnapshotSuccess(
        requested_url=_URL,
        final_url=_URL,
        title="Bread and Roses by Pearfat Parfum | Luckyscent",
        rendered_dom=rendered_dom,
        visible_text=visible_text,
        screenshot_png=b"\x89PNG\r\n\x1a\nluckyscent-active-capture",
        metadata={
            "capture_timestamp": "2026-07-19T00:00:00Z",
            "requested_url": _URL,
            "final_url": _URL,
            "pin_confirmed": pin_confirmed,
        },
        warning_notes=[],
        limitation_notes=[],
    )


def _run(
    *,
    output: Path,
    monkeypatch: pytest.MonkeyPatch,
    mode: str | None,
    capture_factory: Callable[[], CloakBrowserSnapshotSuccess] = _success,
    projector=None,
) -> tuple[int, str]:
    monkeypatch.setattr(
        runner,
        "fetch_cloakbrowser_snapshot_capture",
        lambda **_kwargs: capture_factory(),
    )
    content_capture = (
        None
        if mode is None
        else RenderedContentCaptureSpec(
            capture_artifact_mode=mode,
            parser_version=LUCKYSCENT_PDP_PARSER_VERSION,
            projector=projector
            or (
                lambda rendered_dom, visible_text, final_url: (
                    build_luckyscent_pdp_aggregate_content_record(
                        rendered_dom=rendered_dom,
                        visible_text=visible_text,
                        source_url=final_url,
                    )
                )
            ),
        )
    )
    return runner.run_source_capture_cloakbrowser_packet(
        url=_URL,
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        decision_question="What source-visible offer and review facts are present?",
        output_directory=output,
        capture_context="Luckyscent content-mode unit proof",
        operator_category="unit_test",
        capture_mode=CaptureModeCategory.MULTIMODAL,
        session_id=None,
        proxy_profile=None,
        actor_audience_context=runner.unknown_with_reason("not supplied"),
        visible_mode_changes=[],
        source_publication_or_event=runner.unknown_with_reason("not supplied"),
        source_edit_or_version=runner.unknown_with_reason("not supplied"),
        cutoff_posture=runner.unknown_with_reason("not supplied"),
        recapture_time=runner.not_applicable("first capture"),
        re_capture_relationship=runner.not_applicable("first capture"),
        warnings=[],
        limitations=[],
        retail_capture_profile=get_retail_capture_profile(
            "luckyscent_pdp_aggregate"
        ),
        timeout_seconds=30,
        wait_until="domcontentloaded",
        viewport_width=1280,
        viewport_height=720,
        max_artifact_bytes=10_000_000,
        block_heavy_assets=False,
        settle_seconds=5,
        scroll_passes=4,
        scroll_step_px=500,
        luckyscent_market="US",
        series_id="luckyscent_bread_and_roses_us_v0",
        locale_pin=runner.known_fact("default storefront country=US"),
        currency_pin=runner.known_fact("USD"),
        content_capture=content_capture,
    )


def _manifest(packet_dir: Path) -> dict[str, Any]:
    return json.loads((packet_dir / "manifest.json").read_text(encoding="utf-8"))


def _artifact_path(packet_dir: Path, filename: str) -> Path:
    return next(
        packet_dir / item["relative_packet_path"]
        for item in _manifest(packet_dir)["preserved_files"]
        if _logical_name(item["relative_packet_path"]) == filename
    )


def _packet(packet_dir: Path) -> SourceCapturePacket:
    return SourceCapturePacket.model_validate(_manifest(packet_dir))


def _rewrite_artifact_and_manifest(
    packet_dir: Path,
    filename: str,
    body: bytes,
) -> None:
    manifest = _manifest(packet_dir)
    match = next(
        item
        for item in manifest["preserved_files"]
        if _logical_name(item["relative_packet_path"]) == filename
    )
    (packet_dir / match["relative_packet_path"]).write_bytes(body)
    match["sha256"] = hashlib.sha256(body).hexdigest()
    match["size_bytes"] = len(body)
    (packet_dir / "manifest.json").write_text(
        f"{json.dumps(manifest, indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )


def _mutate_json_artifact(
    packet_dir: Path,
    filename: str,
    mutate: Callable[[dict[str, Any]], None],
) -> None:
    payload = json.loads(_artifact_path(packet_dir, filename).read_text(encoding="utf-8"))
    mutate(payload)
    _rewrite_artifact_and_manifest(
        packet_dir,
        filename,
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode(),
    )


def _names(packet_dir: Path) -> set[str]:
    return {
        _logical_name(item["relative_packet_path"])
        for item in _manifest(packet_dir)["preserved_files"]
    }


def test_luckyscent_profile_has_measured_route_posture() -> None:
    profile = get_retail_capture_profile("luckyscent_pdp_aggregate")
    assert profile.retailer == "luckyscent"
    assert profile.wait_until == "domcontentloaded"
    assert profile.settle_seconds == 5
    assert profile.scroll_passes == 4
    assert profile.scroll_step_px == 500


@pytest.mark.parametrize(
    ("mode", "raw_preserved", "record_preserved"),
    [("content", False, True), ("sample", True, True), ("raw", True, False)],
)
def test_capture_artifact_modes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mode: str,
    raw_preserved: bool,
    record_preserved: bool,
) -> None:
    packet_dir = tmp_path / mode
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode=mode)[0] == 0
    names = _names(packet_dir)
    assert ("cloakbrowser_rendered_dom.html" in names) is raw_preserved
    assert ("cloakbrowser_visible_text.txt" in names) is raw_preserved
    assert ("content_record.json" in names) is record_preserved
    assert "content_capture_metadata.json" in names
    assert "cloakbrowser_viewport_screenshot.png" in names
    assert "cloakbrowser_snapshot_metadata.json" in names
    metadata = json.loads(
        _artifact_path(packet_dir, "content_capture_metadata.json").read_text()
    )
    assert metadata["capture_artifact_mode"] == mode
    by_role = {item["role"]: item for item in metadata["inputs"]}
    assert by_role["rendered_dom"]["preserved"] is raw_preserved
    assert by_role["visible_text"]["preserved"] is raw_preserved
    assert by_role["screenshot"]["preserved"] is True
    assert by_role["browser_metadata"]["preserved"] is True


def test_profile_defaults_to_content_mode(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet_dir = tmp_path / "default"
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode=None)[0] == 0
    assert "content_record.json" in _names(packet_dir)
    assert "cloakbrowser_rendered_dom.html" not in _names(packet_dir)


def test_content_record_is_deterministic_target_scoped_and_complete() -> None:
    first = build_luckyscent_pdp_aggregate_content_record(
        rendered_dom=_DOM.encode(),
        visible_text=_VISIBLE_TEXT.encode(),
        source_url=_URL,
    )
    second = build_luckyscent_pdp_aggregate_content_record(
        rendered_dom=_DOM.encode(),
        visible_text=_VISIBLE_TEXT.encode(),
        source_url=_URL,
    )
    assert first == second
    assert first["record_kind"] == LUCKYSCENT_PDP_CONTENT_RECORD_KIND
    structured = [
        row
        for row in first["rows"]
        if row["row_kind"] == "retail_embedded_structured_json"
    ]
    assert len(structured) == 2
    offer = next(
        row for row in first["rows"] if row["row_kind"] == "retail_variant_offer"
    )["source_visible_fields"]
    assert [variant["price"] for variant in offer["variants"]] == [
        "120.0",
        "45.0",
        "5.0",
    ]
    assert offer["seller"] == "Luckyscent"
    assert offer["fragrance_notes"].startswith("Fresh Baguette")
    assert offer["fragrance_style"].startswith("Floral")
    review = next(
        row
        for row in first["rows"]
        if row["row_kind"] == "retail_review_substrate"
    )["source_visible_fields"]
    assert review["displayed_rating"] == "3.8"
    assert review["structured_rating"] == "3.75"
    assert len(review["reviews"]) == 8
    serialized = json.dumps(first, sort_keys=True)
    assert "Wrong Seller" not in serialized
    assert "Unrelated Footer Recommendation" not in serialized
    assert "content_record_unbound" not in serialized
    assert "content_input_rendered_dom" not in serialized
    assert "cloakbrowser_rendered_dom.html" not in serialized


def test_content_builder_rejects_wrong_product_or_incomplete_reviews() -> None:
    wrong_product = _DOM.replace(
        '"url":"' + _URL + '"',
        '"url":"https://www.luckyscent.com/products/other"',
        1,
    )
    with pytest.raises(ValueError, match="aggregate offer row"):
        build_luckyscent_pdp_aggregate_content_record(
            rendered_dom=wrong_product.encode(),
            visible_text=_VISIBLE_TEXT.encode(),
            source_url=_URL,
        )
    incomplete = _DOM.replace(_review(7), "")
    with pytest.raises(ValueError, match="review rows"):
        build_luckyscent_pdp_aggregate_content_record(
            rendered_dom=incomplete.encode(),
            visible_text=_VISIBLE_TEXT.encode(),
            source_url=_URL,
        )


def test_projection_failure_and_market_failure_preserve_raw(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail(*_args):
        raise RuntimeError("fixture drift")

    projection_dir = tmp_path / "projection"
    assert (
        _run(
            output=projection_dir,
            monkeypatch=monkeypatch,
            mode="content",
            projector=fail,
        )[0]
        == runner.CONTENT_PROJECTION_FAILED_EXIT_CODE
    )
    assert {
        "cloakbrowser_rendered_dom.html",
        "cloakbrowser_visible_text.txt",
        "cloakbrowser_viewport_screenshot.png",
        "cloakbrowser_snapshot_metadata.json",
    }.issubset(_names(projection_dir))
    assert "content_record.json" not in _names(projection_dir)

    market_dir = tmp_path / "market"
    exit_code, message = _run(
        output=market_dir,
        monkeypatch=monkeypatch,
        mode="content",
        capture_factory=lambda: _success(pin_confirmed=False),
    )
    assert exit_code == runner.SOURCE_DETAIL_SUFFICIENCY_EXIT_CODE
    assert runner.LUCKYSCENT_MARKET_PIN_FAILURE_MODE_CHANGE in message
    assert "content_record.json" in _names(market_dir)
    assert "cloakbrowser_rendered_dom.html" in _names(market_dir)
    assert "cloakbrowser_visible_text.txt" in _names(market_dir)


def test_browser_secret_rejection_writes_no_packet(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    with pytest.raises(ValueError, match="browser-secret"):
        _run(
            output=tmp_path / "secret",
            monkeypatch=monkeypatch,
            mode="content",
            capture_factory=lambda: _success(
                rendered_dom=_DOM + "<script>cf_clearance=secret</script>"
            ),
        )
    assert not (tmp_path / "secret" / "manifest.json").exists()


def _semantic_projection(projection) -> dict[str, Any]:
    payload = projection.model_dump(mode="json")
    payload.pop("packet_id")
    for row in payload["rows"]:
        row.pop("raw_ref")
        row.pop("raw_anchor")
    for binding in payload["binding_map"]:
        binding.pop("raw_ref")
        binding.pop("raw_anchor")
    for entry in payload["loss_ledger"]["collapsed"]:
        entry.pop("raw_anchor")
    return payload


def _without_lineage_refs(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_lineage_refs(item)
            for key, item in value.items()
            if key not in {"raw_refs", "derived_refs"}
        }
    if isinstance(value, list):
        return [_without_lineage_refs(item) for item in value]
    return value


def test_content_projection_and_silver_match_raw_semantics(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    raw_dir = tmp_path / "raw"
    content_dir = tmp_path / "content"
    assert _run(output=raw_dir, monkeypatch=monkeypatch, mode="raw")[0] == 0
    assert _run(output=content_dir, monkeypatch=monkeypatch, mode="content")[0] == 0
    raw_projection = build_retail_pdp_projection_from_packet_directory(
        packet_directory=raw_dir
    )
    content_projection = build_retail_pdp_projection_from_packet_directory(
        packet_directory=content_dir
    )
    assert _semantic_projection(raw_projection) == _semantic_projection(
        content_projection
    )
    assert all(
        row.raw_ref.packet_id == _packet(content_dir).packet_id
        for row in content_projection.rows
    )
    assert all(
        row.raw_anchor.anchor_kind == "json_pointer"
        and row.raw_anchor.anchor_value.startswith("/rows/")
        for row in content_projection.rows
    )
    raw_silver = build_retail_pdp_silver_records(
        packet=_packet(raw_dir),
        projection=raw_projection,
        projection_record_id="projection.json",
        projection_sha256="raw-projection-sha",
    )
    content_silver = build_retail_pdp_silver_records(
        packet=_packet(content_dir),
        projection=content_projection,
        projection_record_id="projection.json",
        projection_sha256="content-projection-sha",
    )
    assert [_without_lineage_refs(record["payload"]) for record in raw_silver] == [
        _without_lineage_refs(record["payload"]) for record in content_silver
    ]
    assert [record.get("residuals") for record in raw_silver] == [
        record.get("residuals") for record in content_silver
    ]


def test_parser_fit_match_and_target_fact_drift(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    packet_dir = tmp_path / "sample"
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode="sample")[0] == 0
    assert check_luckyscent_pdp_parser_fit(
        packet_or_manifest_path=packet_dir
    )["status"] == "match"
    exit_code, report = run_luckyscent_pdp_parser_fit_check(
        packet_paths=[packet_dir]
    )
    assert exit_code == 0
    assert report["results"][0]["status"] == "match"

    dom_path = _artifact_path(packet_dir, "cloakbrowser_rendered_dom.html")
    changed_dom = dom_path.read_bytes().replace(b'"price":"120.0"', b'"price":"121.0"')
    _rewrite_artifact_and_manifest(
        packet_dir, "cloakbrowser_rendered_dom.html", changed_dom
    )

    def update_input_hash(payload: dict[str, Any]) -> None:
        item = next(
            entry for entry in payload["inputs"] if entry["role"] == "rendered_dom"
        )
        item["sha256"] = hashlib.sha256(changed_dom).hexdigest()
        item["byte_count"] = len(changed_dom)

    _mutate_json_artifact(
        packet_dir, "content_capture_metadata.json", update_input_hash
    )
    drift = check_luckyscent_pdp_parser_fit(packet_or_manifest_path=packet_dir)
    assert drift["status"] == "drift"
    assert drift["difference"]["stored_sha256"] != drift["difference"]["current_sha256"]


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("parser_version", "parser_version_mismatch"),
        ("source_url", "source_mismatch"),
        ("malformed", "content_record_shape"),
        ("input_hash", "input_hash_mismatch"),
    ],
)
def test_parser_fit_failure_classes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutation: str,
    expected_code: str,
) -> None:
    packet_dir = tmp_path / mutation
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode="sample")[0] == 0
    if mutation == "parser_version":
        _mutate_json_artifact(
            packet_dir,
            "content_capture_metadata.json",
            lambda payload: payload.update({"parser_version": "old_parser"}),
        )
    elif mutation == "source_url":
        _mutate_json_artifact(
            packet_dir,
            "content_record.json",
            lambda payload: payload.update(
                {"source_url": "https://www.luckyscent.com/products/other"}
            ),
        )
    elif mutation == "malformed":
        _rewrite_artifact_and_manifest(packet_dir, "content_record.json", b"[]\n")
    else:
        body = _artifact_path(packet_dir, "cloakbrowser_rendered_dom.html").read_bytes()
        _rewrite_artifact_and_manifest(
            packet_dir,
            "cloakbrowser_rendered_dom.html",
            body + b"<!-- drift -->",
        )
    with pytest.raises(ParserFitCheckError) as exc:
        check_luckyscent_pdp_parser_fit(packet_or_manifest_path=packet_dir)
    assert exc.value.code == expected_code


@pytest.mark.parametrize("mode", ["content", "raw"])
def test_parser_fit_rejects_non_sample_packets(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mode: str,
) -> None:
    packet_dir = tmp_path / mode
    assert _run(output=packet_dir, monkeypatch=monkeypatch, mode=mode)[0] == 0
    with pytest.raises(ParserFitCheckError) as exc:
        check_luckyscent_pdp_parser_fit(packet_or_manifest_path=packet_dir)
    assert exc.value.code in {"sample_required", "preserved_file_mismatch"}
