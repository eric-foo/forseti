from __future__ import annotations

import json
from pathlib import Path

import pytest

import runners.run_source_capture_cloakbrowser_packet as cloakbrowser_runner
from cleaning.retail_pdp import build_retail_pdp_cleaning_input
from runners.run_source_capture_cloakbrowser_packet import (
    CONTENT_EXTRACTION_FAILED_EXIT_CODE,
    run_source_capture_cloakbrowser_packet,
)
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
from source_capture.content_extraction import RenderedContentExtractionSpec
from source_capture.content_qualification import qualify_rendered_content
from source_capture.models import CaptureModeCategory
from source_capture.models import SourceCapturePacket
from source_capture.retail_pdp_projection import (
    NORDSTROM_PDP_PARSER_VERSION,
    build_nordstrom_pdp_aggregate_content_record,
)

_SOURCE_URL = "https://www.nordstrom.com/s/test-product/8260802"


def _product_state() -> dict:
    available = {
        "asOf": "2026-07-20T00:00:00Z",
        "salability": {"status": "SELLABLE"},
        "availability": {
            "isAvailable": True,
            "isShipAvailable": True,
            "isMarketPickAvailable": True,
            "isPickAvailable": True,
            "shipQuantity": 7,
            "marketPickQuantity": 8,
            "pickQuantity": 9,
        },
        "pricings": [{"sellingRetail": {"priceType": "REGULAR", "price": "28.00"}}],
        "isFinalSale": False,
    }
    sold_out = {
        "asOf": "2026-07-20T00:00:00Z",
        "salability": {"status": "SOLD_OUT"},
        "availability": {
            "isAvailable": False,
            "isShipAvailable": False,
            "isMarketPickAvailable": False,
            "isPickAvailable": False,
            "shipQuantity": 0,
            "marketPickQuantity": 0,
            "pickQuantity": 0,
        },
        "pricings": [{"sellingRetail": {"priceType": "REGULAR", "price": "28.00"}}],
        "isFinalSale": False,
    }
    product = {
        "id": "8260802",
        "sellingBrand": "NORDSTROM",
        "legacyStyleGroupId": "10743748",
        "webPathAlias": "test-product",
        "copyProductTitle": "Test Product",
        "copyDescription": "<b>What it is:</b> Test description.",
        "copyFeatures": ["Cruelty-free", "B Corp certified"],
        "copyFitInfo": [],
        "copyFitInfoDetails": [],
        "copyIngredientsDetail": "Water, Shea Butter",
        "labelId": "brand-1",
        "labelDisplayName": "Test Brand",
        "brandLink": "/brands/test-brand",
        "addToBagCta": "addToBag",
        "partnerRelationships": [],
        "reviews": {
            "numberOfReviews": 1,
            "averageRating": 5.0,
            "maximumRating": 5,
            "secondaryRatings": [],
        },
        "propositions": [
            {
                "availability": {
                    "shipQuantity": 7,
                    "marketPickQuantity": 8,
                    "pickQuantity": 9,
                },
                "coreChoiceSelections": [
                    {
                        "coreChoiceId": "choice-1",
                        "sellableItems": ["item-1"],
                        "sellableSkus": ["sku-1"],
                        "previewableItems": [],
                        "previewableSkus": [],
                        "soldOutItems": ["item-2"],
                        "soldOutSkus": ["sku-2"],
                    }
                ],
            }
        ],
        "coreProducts": [
            {
                "coreProductId": "core-1",
                "editorialShots": [],
                "featuredIngredients": ["Shea Butter"],
                "nptHierarchy": ["Beauty", "Lip Care"],
                "coreChoices": [
                    {
                        "coreChoiceId": "choice-1",
                        "displayColorDescription": "NO COLOR",
                        "colorFamily": {"code": "NON", "label": "None"},
                        "orderedShots": [
                            {
                                "shotName": "front:product",
                                "fileFormat": "JPEG",
                                "imageUrl": "https://n.nordstrommedia.com/it/front.jpeg",
                                "croppedImageAspectRatio": "1:1",
                                "metadata": {"carouselOnlinePhotographyGuideOrder": "0"},
                            },
                            {
                                "shotName": "side:product",
                                "fileFormat": "JPEG",
                                "imageUrl": "https://n.nordstrommedia.com/it/side.jpeg",
                                "croppedImageAspectRatio": "1:1",
                                "metadata": {"carouselOnlinePhotographyGuideOrder": "1"},
                            },
                        ],
                        "items": [
                            {
                                "npin": "item-1",
                                "productSetIds": ["set-1"],
                                "age": {"code": "ADT", "label": "Adult"},
                                "upcs": [{"upc": "111", "isPrimary": "TRUE"}],
                                "sizeDimension1": {"code": "OS", "label": "One Size"},
                                "concatenatedDisplaySize": "One Size",
                                "skinTypes": [{"code": "NRML", "label": "Normal Skin"}],
                                "sku": {"skuId": "sku-1", "propositions": [available]},
                            },
                            {
                                "npin": "item-2",
                                "productSetIds": [],
                                "age": {"code": "ADT", "label": "Adult"},
                                "upcs": [{"upc": "222", "isPrimary": "TRUE"}],
                                "sizeDimension1": {"code": "OS2", "label": "Travel"},
                                "concatenatedDisplaySize": "Travel",
                                "skinTypes": [],
                                "sku": {"skuId": "sku-2", "propositions": [sold_out]},
                            },
                        ],
                    }
                ],
            }
        ],
    }
    return {
        "productDisplay": {
            "productDisplaysById": {"entities": {"8260802": product}},
            "interactions": {
                "product-page::8260802": {
                    "selections": {
                        "coreChoice": "choice-1",
                        "sizeType": None,
                        "size": "One Size",
                        "width": None,
                    }
                }
            },
        },
        "shopper": {"secret_that_must_not_be_retained": "do-not-copy"},
    }


def _fixture_dom(
    *,
    ai_summary: bool = False,
    unsupported_review_field: str | None = None,
) -> bytes:
    product = {
        "@context": "https://schema.org/",
        "@type": "Product",
        "name": "Test Product",
        "brand": {"@type": "Brand", "name": "Test Brand"},
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": 5,
            "reviewCount": 1,
        },
        "offers": {
            "@type": "Offer",
            "price": "28.00",
            "availability": "http://schema.org/InStock",
            "priceCurrency": "USD",
            "url": _SOURCE_URL,
        },
        "description": "Test description",
        "image": ["https://n.nordstrommedia.com/it/front.jpeg"],
    }
    breadcrumbs = {
        "@context": "https://schema.org/",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 0, "name": "Home", "item": "/"},
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Beauty",
                "item": "/browse/beauty",
            },
        ],
    }
    review_summary = (
        "<p>AI-generated review summary</p>" if ai_summary else ""
    )
    unsupported_review_markup = (
        f"<dl><dt>{unsupported_review_field}</dt><dd>Source value</dd></dl>"
        if unsupported_review_field
        else ""
    )
    html = f"""
    <html><head>
      <script type="application/ld+json">{json.dumps(product)}</script>
      <script type="application/ld+json">{json.dumps(breadcrumbs)}</script>
      <script>window.__INITIAL_CONFIG__ = {json.dumps(_product_state())};</script>
    </head><body>
      <main>Main content Test Brand Test Product Current Price $28.00 One Size
      Sold by Nordstrom Add to Bag Shipping to 10001 You Might Also Like</main>
      <section>Highlights Cruelty-free Details & care Test description
      Item #10743748 Core Product ID core-1 Ingredients Water, Shea Butter
      Shipping & returns Free shipping Gift options Reviews</section>
      <div id="product-page-reviews"><div id="reviews">
        <span itemprop="review" itemtype="https://schema.org/Review">
          <span itemprop="name" content="Useful review"></span>
          <span itemprop="author" content="Reviewer"></span>
          <meta itemprop="datePublished" content="2026-07-19T00:00:00+00:00">
          <span itemprop="ratingValue" content="5"></span>
          <span itemprop="reviewBody" content="Review body"></span>
        </span>
        {review_summary}
        <div id="sort-by-filter-8260802-anchor">Sort by <strong>Most Recent</strong></div>
        <div id="reviews-container">
          <div id="review-1"><div>Reviewer Reposted from Test Brand</div>
            <div>Verified purchase</div><div><strong>4</strong> found this helpful</div>
            <div><strong>Size purchased: </strong>One Size</div>
            <div><strong>Color: </strong>Clear</div>
            {unsupported_review_markup}
            <div>Useful review Review body</div>
          </div>
        </div>
        <a href="?page=2">Load 6 more reviews</a>
      </div></div>
    </body></html>
    """
    return html.encode()


def _fixture_text() -> bytes:
    return b"""
    Main content
    Test Brand
    Test Product
    Current Price $28.00
    One Size
    Sold by Nordstrom
    Add to Bag
    Shipping to 10001
    You Might Also Like
    Highlights
    Cruelty-free
    Details & care
    Test description
    Item #10743748
    Core Product ID core-1
    Ingredients
    Water, Shea Butter
    Shipping & returns
    Free shipping
    Gift options
    Reviews
    Reviews (1)
    5.0 out of 5
    5 stars 100%
    4 stars 0%
    3 stars 0%
    2 stars 0%
    1 star 0%
    Recommended for You
    """


def _row(record: dict, kind: str) -> dict:
    return next(
        row["source_visible_fields"]
        for row in record["rows"]
        if row["row_kind"] == kind
    )


def test_nordstrom_v5_retains_target_product_state_variants_reviews_and_loss() -> None:
    record = build_nordstrom_pdp_aggregate_content_record(
        rendered_dom=_fixture_dom(),
        visible_text=_fixture_text(),
        source_url=_SOURCE_URL,
    )

    assert record["schema_version"] == "retail_pdp_nordstrom_aggregate_content_v2"
    assert record["parser_version"] == NORDSTROM_PDP_PARSER_VERSION
    state_row = next(
        row
        for row in record["rows"]
        if row["source_visible_fields"].get("structured_json_kind")
        == "nordstrom_initial_product_state"
    )
    assert "secret_that_must_not_be_retained" not in state_row["source_visible_fields"][
        "raw_json_text"
    ]

    offer = _row(record, "retail_variant_offer")
    assert offer["sku"] == "sku-1"
    assert offer["variant_count"] == 2
    assert offer["out_of_stock_variant_count"] == 1
    assert [row["out_of_stock"] for row in offer["variants"]] == [False, True]
    assert [row["selected"] for row in offer["variants"]] == [True, False]
    assert offer["exact_inventory_quantity"] == {
        "shipQuantity": 7,
        "marketPickQuantity": 8,
        "pickQuantity": 9,
    }
    assert offer["media_reference_count"] == 2
    assert offer["product_features"] == ["Cruelty-free", "B Corp certified"]
    assert "product_display.coreProducts[]" in offer[
        "product_state_raw_field_inventory"
    ]

    reviews = _row(record, "retail_review_substrate")
    assert reviews["rendered_review_count"] == 1
    assert reviews["rendered_reviews"][0] == {
        "title": "Useful review",
        "author": "Reviewer",
        "date": "2026-07-19T00:00:00+00:00",
        "rating": "5",
        "body": "Review body",
        "source_card_id": "review-1",
        "source_display_position": 1,
        "helpful_count": "4",
        "verified_purchase": True,
        "reposted_from": "Test Brand",
        "reviewed_variant": {
            "color": "Clear",
            "size_purchased": "One Size",
        },
        "media_urls": [],
        "raw_field_names": [
            "found_this_helpful.count",
            "itemprop.author.content",
            "itemprop.datePublished.content",
            "itemprop.name.content",
            "itemprop.ratingValue.content",
            "itemprop.reviewBody.content",
            "reposted_from.label",
            "reviewed_variant.color",
            "reviewed_variant.size_purchased",
            "verified_purchase.badge",
        ],
    }
    assert reviews["review_field_exposure"]["variant"] == "retained"
    assert record["information_extraction_coverage"]["questions_and_answers"][
        "status"
    ] == "not_exposed_on_target_pdp"
    assert record["information_extraction_coverage"]["ai_review_sentiment"][
        "status"
    ] == "not_exposed_on_target_pdp"
    omission_categories = {
        row["category"]
        for row in record["loss_ledger"]["omitted_or_not_exposed"]
    }
    assert {
        "RETAIL_REVIEW_INCENTIVE_FILTER_NOT_EXPOSED",
        "RETAIL_REVIEW_DEMOGRAPHICS_NOT_EXPOSED",
        "RETAIL_AI_SENTIMENT_NOT_EXPOSED",
        "RETAIL_QA_NOT_EXPOSED",
        "RETAIL_VARIANT_MERCHANDISING_FLAGS_NOT_EXPOSED",
        "RETAIL_MEDIA_BINARY_NOT_PRESERVED",
    }.issubset(omission_categories)


def test_nordstrom_v5_fails_closed_when_new_ai_sentiment_appears() -> None:
    with pytest.raises(ValueError, match="AI review sentiment became source-visible"):
        build_nordstrom_pdp_aggregate_content_record(
            rendered_dom=_fixture_dom(ai_summary=True),
            visible_text=_fixture_text(),
            source_url=_SOURCE_URL,
        )


@pytest.mark.parametrize(
    "field_label",
    [
        "Would Recommend",
        "Not Helpful",
        "Reviewed Variant",
        "Age Range",
        "Pros",
    ],
)
def test_nordstrom_v5_fails_closed_when_new_review_card_field_appears(
    field_label: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="review-card fields became source-visible",
    ):
        build_nordstrom_pdp_aggregate_content_record(
            rendered_dom=_fixture_dom(unsupported_review_field=field_label),
            visible_text=_fixture_text(),
            source_url=_SOURCE_URL,
        )


def test_nordstrom_v5_content_qualification_matches_and_releases_scratch(
    tmp_path: Path,
) -> None:
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    dom_path = scratch / "dom.html"
    text_path = scratch / "visible.txt"
    expected_path = tmp_path / "expected.json"
    report_path = scratch / "report.json"
    dom_path.write_bytes(_fixture_dom())
    text_path.write_bytes(_fixture_text())
    expected_path.write_text(
        json.dumps(
            build_nordstrom_pdp_aggregate_content_record(
                rendered_dom=_fixture_dom(),
                visible_text=_fixture_text(),
                source_url=_SOURCE_URL,
            )
        ),
        encoding="utf-8",
    )

    exit_code, report = qualify_rendered_content(
        scratch_root=scratch,
        rendered_dom_path=dom_path,
        visible_text_path=text_path,
        expected_content_record_path=expected_path,
        report_path=report_path,
        extractor_version=NORDSTROM_PDP_PARSER_VERSION,
        source_url=_SOURCE_URL,
        extractor=lambda dom, text, url: build_nordstrom_pdp_aggregate_content_record(
            rendered_dom=dom,
            visible_text=text,
            source_url=url,
        ),
    )

    assert exit_code == 0
    assert report["status"] == "match"
    assert report["changed_top_level_keys"] == []
    assert not dom_path.exists()
    assert not text_path.exists()
    assert report_path.is_file()


def test_nordstrom_extraction_failure_preserves_raw_packet(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = tmp_path / "packet"

    def fake_capture(**kwargs: object) -> CloakBrowserSnapshotSuccess:
        return CloakBrowserSnapshotSuccess(
            requested_url=_SOURCE_URL,
            final_url=_SOURCE_URL,
            title="Nordstrom",
            rendered_dom="<html><body>parser drift</body></html>",
            visible_text="parser drift",
            screenshot_png=b"\x89PNG\r\n\x1a\nnordstrom",
            metadata={
                "requested_url": _SOURCE_URL,
                "final_url": _SOURCE_URL,
                "title": "Nordstrom",
                "capture_timestamp": "2026-07-20T00:00:00Z",
                "timeout_seconds": kwargs["timeout_seconds"],
                "wait_until": kwargs["wait_until"],
                "viewport_width": kwargs["viewport_width"],
                "viewport_height": kwargs["viewport_height"],
                "screenshot_mode": "viewport",
                "method_category": "anti_blocking_browser",
                "browser_engine": "cloakbrowser",
                "cloakbrowser_backend": "playwright",
                "profile_persistence": "none",
                "storage_state_loaded": False,
                "proxy_used": False,
                "geoip_used": False,
                "extension_paths_loaded": False,
                "rendered_dom_byte_count": 38,
                "visible_text_byte_count": 12,
                "screenshot_byte_count": 17,
            },
            warning_notes=[],
            limitation_notes=[],
        )

    monkeypatch.setattr(
        cloakbrowser_runner, "fetch_cloakbrowser_snapshot_capture", fake_capture
    )
    exit_code, _message = run_source_capture_cloakbrowser_packet(
        url=_SOURCE_URL,
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        decision_question="Does Nordstrom retain the standard product evidence?",
        output_directory=output,
        capture_context="Nordstrom raw fallback unit proof",
        operator_category="cloakbrowser_snapshot_cli_operator",
        capture_mode=CaptureModeCategory.MULTIMODAL,
        session_id=None,
        proxy_profile=None,
        actor_audience_context=None,
        visible_mode_changes=[],
        source_publication_or_event=None,
        source_edit_or_version=None,
        cutoff_posture=None,
        recapture_time=None,
        re_capture_relationship=None,
        warnings=[],
        limitations=[],
        timeout_seconds=20,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        max_artifact_bytes=50_000,
        block_heavy_assets=False,
        content_extraction=RenderedContentExtractionSpec(
            requested_retention_mode="content",
            extractor_version=NORDSTROM_PDP_PARSER_VERSION,
            extractor=lambda _dom, _text, _url: build_nordstrom_pdp_aggregate_content_record(
                rendered_dom=_dom,
                visible_text=_text,
                source_url=_url,
            ),
        ),
    )

    assert exit_code == CONTENT_EXTRACTION_FAILED_EXIT_CODE
    paths = {
        row["relative_packet_path"]
        for row in json.loads((output / "manifest.json").read_text())[
            "preserved_files"
        ]
    }
    assert {
        "raw/01_cloakbrowser_rendered_dom.html",
        "raw/02_cloakbrowser_visible_text.txt",
        "raw/03_cloakbrowser_viewport_screenshot.png",
        "raw/04_cloakbrowser_snapshot_metadata.json",
        "raw/05_content_extraction_metadata.json",
    }.issubset(paths)
    assert not any(path.endswith("content_record.json") for path in paths)
    metadata = json.loads(
        (output / "raw" / "05_content_extraction_metadata.json").read_text()
    )
    assert metadata["retention_outcome"] == "raw_failure"
    assert metadata["extraction_status"].startswith("failed:")


def test_nordstrom_current_content_has_exact_cleaning_row_equivalence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = tmp_path / "content-packet"

    def fake_capture(**kwargs: object) -> CloakBrowserSnapshotSuccess:
        return CloakBrowserSnapshotSuccess(
            requested_url=_SOURCE_URL,
            final_url=_SOURCE_URL,
            title="Nordstrom",
            rendered_dom=_fixture_dom().decode(),
            visible_text=_fixture_text().decode(),
            screenshot_png=b"\x89PNG\r\n\x1a\nnordstrom",
            metadata={
                "requested_url": _SOURCE_URL,
                "final_url": _SOURCE_URL,
                "title": "Nordstrom",
                "capture_timestamp": "2026-07-20T00:00:00Z",
                "timeout_seconds": kwargs["timeout_seconds"],
                "wait_until": kwargs["wait_until"],
                "viewport_width": kwargs["viewport_width"],
                "viewport_height": kwargs["viewport_height"],
                "screenshot_mode": "viewport",
                "method_category": "anti_blocking_browser",
                "browser_engine": "cloakbrowser",
                "cloakbrowser_backend": "playwright",
                "profile_persistence": "none",
                "storage_state_loaded": False,
                "proxy_used": False,
                "geoip_used": False,
                "extension_paths_loaded": False,
                "retail_capture_profile": {"name": "nordstrom_pdp_aggregate"},
                "pin_confirmed": True,
                "rendered_dom_byte_count": len(_fixture_dom()),
                "visible_text_byte_count": len(_fixture_text()),
                "screenshot_byte_count": 17,
            },
            warning_notes=[],
            limitation_notes=[],
        )

    monkeypatch.setattr(
        cloakbrowser_runner, "fetch_cloakbrowser_snapshot_capture", fake_capture
    )
    exit_code, _message = run_source_capture_cloakbrowser_packet(
        url=_SOURCE_URL,
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        decision_question="Does Nordstrom retain the standard product evidence?",
        output_directory=output,
        capture_context="Nordstrom content-to-Cleaning equivalence proof",
        operator_category="cloakbrowser_snapshot_cli_operator",
        capture_mode=CaptureModeCategory.MULTIMODAL,
        session_id=None,
        proxy_profile=None,
        actor_audience_context=None,
        visible_mode_changes=[],
        source_publication_or_event=None,
        source_edit_or_version=None,
        cutoff_posture=None,
        recapture_time=None,
        re_capture_relationship=None,
        warnings=[],
        limitations=[],
        timeout_seconds=20,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        max_artifact_bytes=50_000,
        block_heavy_assets=False,
        content_extraction=RenderedContentExtractionSpec(
            requested_retention_mode="content",
            extractor_version=NORDSTROM_PDP_PARSER_VERSION,
            extractor=lambda dom, text, url: build_nordstrom_pdp_aggregate_content_record(
                rendered_dom=dom,
                visible_text=text,
                source_url=url,
            ),
        ),
    )
    assert exit_code == 0
    manifest = json.loads((output / "manifest.json").read_text())
    packet = SourceCapturePacket.model_validate(manifest)
    file_bytes = {
        row["file_id"]: (output / row["relative_packet_path"]).read_bytes()
        for row in manifest["preserved_files"]
    }
    retained = json.loads(
        next(
            body
            for file_id, body in file_bytes.items()
            if next(
                row
                for row in manifest["preserved_files"]
                if row["file_id"] == file_id
            )["relative_packet_path"].endswith("content_record.json")
        )
    )

    cleaning = build_retail_pdp_cleaning_input(
        packet=packet,
        file_bytes_by_file_id=file_bytes,
    )

    assert cleaning.legacy_input is False
    assert cleaning.extractor_version == NORDSTROM_PDP_PARSER_VERSION
    assert [row.row_id for row in cleaning.rows] == [
        row["row_id"] for row in retained["rows"]
    ]
    assert len(cleaning.handles) == len(retained["rows"])
