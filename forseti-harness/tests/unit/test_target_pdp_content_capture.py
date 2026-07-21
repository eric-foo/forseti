"""Target canonical PDP content: reconstruction, loss honesty, and fail-loud gates.

The fixture mirrors the structure of the proven parent packet
(``01KXR823YS3V5M9E01QXP71ETC``, TCIN ``80184023``): Target-owned
``__NEXT_DATA__`` CDUI page state whose core product datasource is hydrated
server-side while the price, offer, fulfillment, variation, and store
datasources are declared but null, plus the rendered text that carries the
client-hydrated price, fulfillment, and review widget.
"""

from __future__ import annotations

import json

import pytest

from runners.run_content_qualification import _ROUTES
from source_capture.retail_pdp_content import load_retail_pdp_content_record  # noqa: F401
from source_capture.retail_pdp_projection import (
    TARGET_PDP_CONTENT_PROFILE,
    TARGET_PDP_CONTENT_RECORD_KIND,
    TARGET_PDP_CONTENT_SCHEMA_VERSION,
    TARGET_PDP_PARSER_VERSION,
    TargetPdpAggregateContentRecord,
    build_target_pdp_aggregate_content_record,
)

_TCIN = "80184023"
_SOURCE_URL = f"https://www.target.com/p/-/A-{_TCIN}"
_ACCESS_TOKEN = "eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.FIXTURE_ACCESS_TOKEN_VALUE"
_REFRESH_TOKEN = "LmIhyZRAvwRBn07mvFfdd30virR1QTz3TWnQF3s04s4v80sDO7FIXTURE"


def _product(tcin: str = _TCIN) -> dict:
    return {
        "__typename": "Product",
        "tcin": tcin,
        "category": {
            "parent_category_id": "5xtzf",
            "name": "Face Serums",
            "breadcrumbs": [{"name": "target"}, {"name": "Beauty"}],
        },
        "ratings_and_reviews": {
            "has_verified": True,
            "statistics": {
                "rating": {
                    "average": 4.45,
                    "count": 1771,
                    "distribution": {
                        "rating1": 112,
                        "rating2": 51,
                        "rating3": 94,
                        "rating4": 195,
                        "rating5": 1319,
                    },
                    "secondary_averages": [
                        {"label": "Brightening", "value": 3.95},
                        {"label": "Soothing", "value": 3.82},
                    ],
                },
                "review_count": 758,
                "question_count": 34,
                "recommended_count": 163,
                "not_recommended_count": 80,
                "recommended_percentage": 67,
            },
            "most_recent": [
                {
                    "id": "2e6c916e-2add-4efb-b36c-3cdac72a276b",
                    "text": "staple in my skincare routine, only four stars because of the finish",
                    "author": {"external_id": "3528344578"},
                    "rating": {"value": 4, "submitted_at": "2026-06-11T00:38:16.725Z"},
                },
                {
                    "id": "a12b7409-15ef-4224-863a-a752187b1558",
                    "text": "This is a great product, I can see the difference love it",
                    "author": {"external_id": "3527911204"},
                    "rating": {"value": 5, "submitted_at": "2026-06-10T19:33:30.000Z"},
                },
            ],
            "photos": ["https://target.scene7.com/is/image/Target/GUEST_a", ""],
        },
        "desirability_cues": [{"code": "highly_rated"}],
        "item": {
            "dpci": "037-14-0466",
            "primary_barcode": "850010792071",
            "relationship_type_code": "SA",
            "cart_add_on_threshold": 35,
            "return_method": "Mail in or Store",
            "formatted_return_method": "This item can be returned to any Target store.",
            "return_policies_guest_message": "Return within 90 days.",
            "disclaimer": {"type": "Healthcare Disclaimer", "description": "Reference only."},
            "eligibility_rules": {
                "hold": {"is_active": True},
                "scheduled_delivery": {"is_active": True},
                "ship_to_guest": {"is_active": False},
            },
            "environmental_segmentation": {"is_hazardous_material": False},
            "fulfillment": {"is_gift_wrap_eligible": True, "purchase_limit": 10},
            "handling": {"import_designation_description": "Made in the USA"},
            "merchandise_classification": {
                "class_id": 14,
                "department_id": 37,
                "department_name": "SKIN/BATH CARE",
            },
            "package_dimensions": {
                "depth": 1.41,
                "width": 1.54,
                "height": 5.37,
                "weight": 0.27,
                "dimension_unit_of_measure": "INCH",
                "weight_unit_of_measure": "POUND",
            },
            "primary_brand": {
                "name": "Naturium",
                "canonical_url": "/b/naturium/-/N-q643le8pm3h",
                "linking_id": "q643le8pm3h",
            },
            "product_classification": {
                "item_type": {"name": "Facial Treatments", "type": 250648},
                "product_type_name": "HEALTH AND BEAUTY",
                "purchase_behavior": "Frequency",
            },
            "product_description": {
                "title": "Naturium Vitamin C Complex Serum- 1 fl oz",
                "downstream_description": "Our potent vitamin C serum is formulated with a gold complex.",
                "bullet_descriptions": ["<B>Scent:</B> Unscented", "<B>Health Facts:</B> Vegan"],
                "soft_bullets": {
                    "title": "highlights",
                    "bullets": ["Helps improve appearance of fine lines", "Helps skin look brighter"],
                },
            },
            "wellness_merchandise_attributes": [
                {
                    "value_name": "Clean",
                    "value_id": "836281",
                    "parent_id": "304049",
                    "wellness_description": "Formulated without selected chemicals.",
                }
            ],
            "enrichment": {
                "buy_url": f"https://www.target.com/p/naturium/-/A-{tcin}",
                "image_info": {
                    "base_url": "//target.scene7.com/is/image/Target/",
                    "primary_image": {"url": "GUEST_primary"},
                    "alternate_images": [{"url": "GUEST_alt_1"}, {"url": "GUEST_alt_2"}],
                    "content_labels": [{"a": 1}],
                },
                "nutrition_facts": {
                    "ingredients": "Water (Aqua), Glycerin, Sodium Ascorbyl Phosphate",
                    "nutrition_label_type_code": "LEGACY_FORMAT",
                    "warning": "CAUTION: For external use only.",
                },
                "videos": [
                    {
                        "video_title": "NATR_Vitamin-C-Complex-Serum-Video-1",
                        "video_length_seconds": 22,
                        "video_poster_image": "https://target.scene7.com/is/image/Target/GUEST_poster",
                        "video_files": [{"url": "a.mp4"}],
                        "video_captions": [{"url": "a.vtt"}],
                    }
                ],
                "return_policies": [{"user_type": "best_guest", "day_count": 120}],
            },
        },
    }


def _next_data(
    *,
    product: dict | None = None,
    hydrate_variations: bool = False,
    include_session_secrets: bool = True,
) -> dict:
    core_module = {
        "module_type": "ProductDetailWebDatasourceCore",
        "module_placement_id": "ProductDetailWebDatasourceCore",
        "module_data": {"data": {"product": product if product is not None else _product()}},
    }
    variation_module = {
        "module_type": "ProductDetailWebDatasourceFulfillmentAndVariations",
        "module_placement_id": "ProductDetailWebDatasourceFulfillmentAndVariations",
        "module_data": ({"data": {"variations": []}} if hydrate_variations else None),
    }
    queries = [
        {
            "queryKey": ["platform/domain-cdui-orchestrations/fetch-cdui-layout-v1", {}],
            "state": {
                "status": "success",
                "data": {
                    "data": {
                        "page_type": "pdp",
                        "layout": {
                            "id": "web_pdp_default",
                            "zones": [
                                {
                                    "module_groups": [
                                        {
                                            "modules": [
                                                {"module_type": "ProductDetailTitle"},
                                                {"module_type": "ProductDetailPrice"},
                                                {"module_type": "ProductDetailVariationSelector"},
                                            ]
                                        }
                                    ]
                                }
                            ],
                        },
                        "data_source_modules": [
                            {
                                "module_type": "ProductDetailWebDatasourceCircleOffers",
                                "module_data": None,
                            },
                            core_module,
                            variation_module,
                        ],
                    }
                },
            },
        }
    ]
    if include_session_secrets:
        queries.append(
            {
                "queryKey": ["site-top-of-funnel/get-cookies", {}],
                "state": {
                    "status": "success",
                    "data": {
                        "accessToken": _ACCESS_TOKEN,
                        "refreshToken": _REFRESH_TOKEN,
                        "visitorId": "019F7080D22202008A5F8C019597ECEA",
                    },
                },
            }
        )
    return {"props": {"dehydratedState": {"mutations": [], "queries": queries}}}


_VISIBLE_TEXT = """Ship to 52404
Cedar Rapids South
Naturium Vitamin C Complex Serum- 1 fl oz
4.45 out of 5 stars with 1771 reviews
1771
34 Questions
$14.69 was $17.89
When purchased online
Pickup
Ready within 2 hours
Delivery
Check availability
Shipping
Arrives by Tue, Jul 21
Guest ratings & reviews
5 stars
74%
4 stars
11%
3 stars
5%
2 stars
3%
1 star
6%
67% would recommend
We found 757 matching reviews
"""


def _dom(next_data: dict | None = None, *, include_next_data: bool = True) -> bytes:
    payload = json.dumps(next_data if next_data is not None else _next_data())
    script = (
        f'<script id="__NEXT_DATA__" type="application/json">{payload}</script>'
        if include_next_data
        else ""
    )
    return (
        "<html><head><title>Naturium Vitamin C Complex Serum : Target</title>"
        '<meta property="og:title" content="Naturium Vitamin C Complex Serum- 1 fl oz">'
        "</head><body>"
        '<div data-test="current-price"><span>$14.69</span></div>'
        f"{script}</body></html>"
    ).encode("utf-8")


def _build(**kwargs):
    return build_target_pdp_aggregate_content_record(
        rendered_dom=kwargs.pop("rendered_dom", _dom()),
        visible_text=kwargs.pop("visible_text", _VISIBLE_TEXT.encode("utf-8")),
        source_url=kwargs.pop("source_url", _SOURCE_URL),
    )


def _rows(record: dict, kind: str) -> list[dict]:
    return [row for row in record["rows"] if row["row_kind"] == kind]


def _fields(record: dict, kind: str) -> dict:
    matches = _rows(record, kind)
    assert len(matches) == 1, f"expected exactly one {kind} row, got {len(matches)}"
    return matches[0]["source_visible_fields"]


def test_record_identity_and_versions_are_target_local() -> None:
    record = _build()

    assert record["record_kind"] == TARGET_PDP_CONTENT_RECORD_KIND
    assert record["schema_version"] == TARGET_PDP_CONTENT_SCHEMA_VERSION
    assert record["parser_version"] == TARGET_PDP_PARSER_VERSION
    assert record["capture_profile"] == TARGET_PDP_CONTENT_PROFILE
    assert record["tcin"] == _TCIN
    assert record["retailer"] if "retailer" in record else True
    assert all(row["retailer"] == "target" for row in record["rows"])


def test_reconstructs_product_identity_copy_and_ingredients() -> None:
    product = _fields(_build(), "retail_pdp_product")

    assert product["tcin"] == _TCIN
    assert product["dpci"] == "037-14-0466"
    assert product["primary_barcode"] == "850010792071"
    assert product["brand_name"] == "Naturium"
    assert product["brand_linking_id"] == "q643le8pm3h"
    assert product["category_name"] == "Face Serums"
    assert product["category_breadcrumbs"] == ["target", "Beauty"]
    assert product["department_name"] == "SKIN/BATH CARE"
    assert product["bullet_descriptions"][0] == "<B>Scent:</B> Unscented"
    assert product["soft_bullets"] == [
        "Helps improve appearance of fine lines",
        "Helps skin look brighter",
    ]

    subtree = _fields(_build(), "retail_product_module_subtree")
    assert subtree["ingredients"].startswith("Water (Aqua), Glycerin")
    assert subtree["nutrition_warning"].startswith("CAUTION")
    assert subtree["alternate_image_count"] == 2
    assert subtree["videos"][0]["video_length_seconds"] == 22
    assert subtree["wellness_merchandise_attributes"][0]["value_name"] == "Clean"
    assert subtree["package_dimensions"]["weight_unit_of_measure"] == "POUND"
    assert subtree["eligibility_rules"] == ["hold", "scheduled_delivery"]
    assert subtree["import_designation_description"] == "Made in the USA"


def test_offer_comes_from_rendered_dom_because_ssr_leaves_it_unhydrated() -> None:
    record = _build()
    offer = _fields(record, "retail_variant_offer")

    assert record["offer_module_state"] == "hydrated_in_rendered_dom"
    assert offer["price"] == "14.69"
    assert offer["price_currency"] == "USD"
    assert "pickup=Ready within 2 hours" in offer["availability"]
    assert "shipping=Arrives by Tue, Jul 21" in offer["availability"]
    assert (
        "target_price_offer_fulfillment_variation_datasources_declared_unhydrated_in_ssr"
        in record["residuals"]
    )


def test_price_absence_is_reported_not_invented() -> None:
    record = _build(
        rendered_dom=_dom().replace(b'<div data-test="current-price"><span>$14.69</span></div>', b""),
        visible_text=_VISIBLE_TEXT.replace("$14.69 was $17.89", "").encode("utf-8"),
    )

    assert record["offer_module_state"] == "declared_unhydrated"
    assert "target_price_absent_from_rendered_dom_and_page_state" in record["residuals"]
    assert _fields(record, "retail_variant_offer")["price"] is None


def test_preserves_three_way_review_count_disagreement() -> None:
    review = _fields(_build(), "retail_review_substrate")

    # The page states three different totals; none is reconciled away.
    assert review["rating_count"] == "1771"  # rendered widget star ratings
    assert review["structured_review_count"] == "758"  # CDUI page state
    assert review["filtered_review_count"] == "757"  # rendered filter result
    assert review["structured_rating_average"] == "4.45"
    assert review["structured_question_count"] == "34"
    assert review["structured_recommended_count"] == "163"
    assert review["structured_not_recommended_count"] == "80"
    assert review["structured_rating_distribution"]["rating5"] == 1319
    assert review["structured_secondary_averages"][0]["label"] == "Brightening"


def test_review_identity_is_retained_without_duplicating_companion_bodies() -> None:
    record = _build()
    identity = _rows(record, "retail_review_identity")

    assert len(identity) == 2
    first = identity[0]["source_visible_fields"]
    assert first["target_native_review_id"] == "2e6c916e-2add-4efb-b36c-3cdac72a276b"
    assert first["review_id_family"] == "target_native_uuid"
    assert first["rating_value"] == 4
    assert first["submitted_at"] == "2026-06-11T00:38:16.725Z"
    assert first["body_present"] is True
    assert first["body_retained_here"] is False
    assert first["body_char_count"] == 68

    # No review body text may appear anywhere in the serialized record.
    blob = json.dumps(record)
    assert "staple in my skincare routine" not in blob
    assert "I can see the difference" not in blob
    assert "target_review_bodies_not_retained_companion_owns_them" in record["residuals"]
    assert (
        "target_native_review_ids_do_not_join_bazaarvoice_review_ids"
        in record["residuals"]
    )


def test_refuses_to_emit_guest_session_secret_material() -> None:
    record = _build()
    blob = json.dumps(record)

    assert _ACCESS_TOKEN not in blob
    assert _REFRESH_TOKEN not in blob
    assert "accessToken" not in blob
    assert (
        "target_guest_session_secret_query_present_not_retained" in record["residuals"]
    )


def test_variant_state_is_not_exposed_when_variation_datasource_is_null() -> None:
    record = _build()

    assert record["variant_module_state"] == "not_exposed"
    assert (
        "target_variation_datasource_not_hydrated_no_variants_retained"
        in record["residuals"]
    )


def test_variant_state_is_observed_when_variation_datasource_hydrates() -> None:
    record = _build(rendered_dom=_dom(_next_data(hydrate_variations=True)))

    assert record["variant_module_state"] == "observed"


def test_declared_cdui_modules_are_inventoried_with_hydration_state() -> None:
    modules = [
        row["source_visible_fields"] for row in _rows(_build(), "retail_carried_module")
    ]
    by_type = {row["module_type"]: row for row in modules}

    assert by_type["ProductDetailWebDatasourceCore"]["server_side_hydration"] == "hydrated"
    assert (
        by_type["ProductDetailWebDatasourceCircleOffers"]["server_side_hydration"]
        == "declared_unhydrated"
    )
    assert (
        by_type["ProductDetailWebDatasourceFulfillmentAndVariations"][
            "server_side_hydration"
        ]
        == "declared_unhydrated"
    )
    layout = by_type["cdui_layout_declared_modules"]
    assert layout["layout_id"] == "web_pdp_default"
    assert "ProductDetailPrice" in layout["declared_module_types"]


@pytest.mark.parametrize(
    "bad_url",
    [
        "https://www.target.com/p/-/A-80184023/-/A-99999999",
        "https://www.walmart.com/p/-/A-80184023",
        "https://www.target.com/p/naturium",
    ],
)
def test_rejects_urls_that_do_not_bind_exactly_one_tcin(bad_url: str) -> None:
    with pytest.raises(ValueError, match="exactly one /A-<tcin>"):
        _build(source_url=bad_url)


def test_fails_loud_when_page_state_tcin_disagrees_with_requested_tcin() -> None:
    with pytest.raises(ValueError, match="does not match requested"):
        _build(rendered_dom=_dom(_next_data(product=_product("99999999"))))


def test_fails_loud_when_next_data_is_absent() -> None:
    with pytest.raises(ValueError, match="exactly one __NEXT_DATA__"):
        _build(rendered_dom=_dom(include_next_data=False))


def test_fails_loud_when_core_datasource_is_not_hydrated() -> None:
    payload = _next_data()
    modules = payload["props"]["dehydratedState"]["queries"][0]["state"]["data"]["data"][
        "data_source_modules"
    ]
    for module in modules:
        if module["module_type"] == "ProductDetailWebDatasourceCore":
            module["module_data"] = None

    with pytest.raises(ValueError, match="does not hydrate"):
        _build(rendered_dom=_dom(payload))


def test_fails_loud_when_rating_average_is_missing() -> None:
    product = _product()
    product["ratings_and_reviews"]["statistics"]["rating"].pop("average")

    with pytest.raises(ValueError, match="structured rating average"):
        _build(rendered_dom=_dom(_next_data(product=product)))


def test_record_model_requires_the_four_singleton_rows() -> None:
    record = _build()
    trimmed = [
        row for row in record["rows"] if row["row_kind"] != "retail_product_module_subtree"
    ]

    with pytest.raises(ValueError, match="exactly one product, offer"):
        TargetPdpAggregateContentRecord.model_validate({**record, "rows": trimmed})


def test_qualification_route_uses_the_family_owned_parser() -> None:
    parser_version, _extractor = _ROUTES["target"]

    assert parser_version == TARGET_PDP_PARSER_VERSION


def test_content_record_does_not_smuggle_the_disposable_inputs() -> None:
    """Content retention must extract, never embed, the DOM it discards.

    Storage impact is measured against a real packet in the route's dogfood
    record; a synthetic fixture cannot honestly assert a compaction ratio.
    """
    dom = _dom()
    record = _build(rendered_dom=dom)
    blob = json.dumps(record)

    # Source anchors legitimately name __NEXT_DATA__; the raw markup, the
    # loader envelope, and the disposable text must not survive.
    assert "<html" not in blob and "<script" not in blob
    assert "dehydratedState" not in blob
    assert "queryKey" not in blob
    assert _VISIBLE_TEXT not in blob


def test_extraction_failure_preserves_the_raw_packet_and_exits_nonzero(
    tmp_path,
    monkeypatch,
) -> None:
    """A drifted PDP must fall back to raw, not emit a thin content record."""
    import runners.run_source_capture_cloakbrowser_packet as cloakbrowser_runner
    from runners.run_source_capture_cloakbrowser_packet import (
        CONTENT_EXTRACTION_FAILED_EXIT_CODE,
        run_source_capture_cloakbrowser_packet,
    )
    from source_capture.adapters.cloakbrowser_snapshot import (
        CloakBrowserSnapshotSuccess,
    )
    from source_capture.content_extraction import RenderedContentExtractionSpec
    from source_capture.models import CaptureModeCategory

    output = tmp_path / "content-packet"

    def fake_capture(**kwargs):
        return CloakBrowserSnapshotSuccess(
            requested_url=_SOURCE_URL,
            final_url=_SOURCE_URL,
            title="Target",
            rendered_dom="<html><body>parser drift, no __NEXT_DATA__</body></html>",
            visible_text="parser drift",
            screenshot_png=b"\x89PNG\r\n\x1a\ntarget",
            metadata={
                "requested_url": _SOURCE_URL,
                "final_url": _SOURCE_URL,
                "title": "Target",
                "capture_timestamp": "2026-07-21T00:00:00Z",
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
                "rendered_dom_byte_count": 52,
                "visible_text_byte_count": 12,
                "screenshot_byte_count": 16,
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
        decision_question="Does Target retain the canonical product evidence?",
        output_directory=output,
        capture_context="Target raw fallback unit proof",
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
            extractor_version=TARGET_PDP_PARSER_VERSION,
            extractor=lambda _dom, _text, _url: build_target_pdp_aggregate_content_record(
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
    # Every acquired raw input survives the failure.
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


def test_unpainted_review_widget_is_recorded_not_inferred() -> None:
    """Live captures can miss the lazy below-fold widget; page state still holds.

    Observed on dogfood packets 01KY2E0Q5C2V598GSEGG6ABZRM and
    01KY2E4GG7J3CN93S6ZA4CRQT2: the rendered filtered-match count and percent
    distribution were absent while the CDUI per-star counts were present.
    """
    # The whole below-fold widget region is simply absent from the rendered text.
    widgetless = _VISIBLE_TEXT.split("Guest ratings & reviews")[0]
    record = _build(visible_text=widgetless.encode("utf-8"))
    review = _fields(record, "retail_review_substrate")

    assert review["filtered_review_count"] is None
    assert not review["rating_distribution_buckets"]
    assert "target_rendered_filtered_review_count_not_observed" in record["residuals"]
    assert (
        "target_rendered_percent_distribution_not_observed_structured_counts_retained"
        in record["residuals"]
    )
    # The structured aggregates are unaffected and remain exact per-star counts.
    assert review["structured_review_count"] == "758"
    assert review["structured_rating_distribution"]["rating5"] == 1319
