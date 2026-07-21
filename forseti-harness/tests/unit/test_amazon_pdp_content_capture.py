"""Amazon canonical PDP content: target binding, exact bodies, fail-loud gates.

The fixture mirrors the exact structures the proof packet
``01KY0PHPN10205MKKCK1GB7YH1`` exposes: ``celwidget`` feature modules stamped
with ``data-csa-c-asin``, Amazon's ``a-state`` twister and social-proofing page
state, the duplicated per-row review header markup, and the reviewer's own rich
content block.  Storage impact and raw-to-content reconstruction are measured
against that real packet in the route's proof record, not asserted here.
"""

from __future__ import annotations

import json

import pytest

from runners.run_content_qualification import _ROUTES
from source_capture.retail_pdp_content import load_retail_pdp_content_record  # noqa: F401
from source_capture.retail_pdp_projection import (
    AMAZON_PDP_CONTENT_SCHEMA_VERSION,
    AMAZON_PDP_PARSER_VERSION,
    AmazonPdpAggregateContentRecord,
    build_amazon_pdp_aggregate_content_record,
)

_ASIN = "B07XXPHQZK"
_SOURCE_URL = f"https://www.amazon.com/Laneige-Sleeping-Berry/dp/{_ASIN}"
_SESSION_ID = "133-2733401-9448351"
_CSRF_TOKEN = "hL0v3E/nX/WAkadPRgPEExVyNW9NUoPuOGMOUUXlVG6CAAAAAGpekZplOTU2"


def _celwidget(
    *,
    feature: str,
    body: str,
    asin: str | None = _ASIN,
    slot: str | None = None,
    active: str | None = None,
    element_id: str | None = None,
) -> str:
    attributes = (
        f'id="{element_id or feature + "_feature_div"}" class="celwidget" '
        f'data-feature-name="{feature}" data-csa-c-content-id="{feature}" '
        f'data-csa-c-slot-id="{slot or feature + "_feature_div"}" '
        f'data-csa-c-asin="{"" if asin is None else asin}"'
    )
    if active is not None:
        attributes += f' data-csa-c-is-in-initial-active-row="{active}"'
    return f"<div {attributes}>{body}</div>"


def _price_body(amount: str) -> str:
    return (
        '<span id="apex-pricetopay-accessibility-label" class="aok-offscreen"> '
        f"${amount} </span>"
        '<span class="a-price priceToPay apex-pricetopay-value">'
        f'<span class="a-offscreen">${amount}</span></span>'
    )


_TWISTER_STATE = {
    "sortedVariations": [[1], [2]],
    "sorting_filtering_exp": {"sorting": ["featuredOffer"]},
    "sortedDimValuesForAllDims": {
        "style_name": [
            {
                "indexInDimList": 1,
                "defaultAsin": _ASIN,
                "dimensionValueDisplayText": "Berry",
                "dimensionValueState": "SELECTED",
                "dimensionDisplaySubType": "image",
                "asinHiddenInCollapseView": True,
                "slotsFetched": True,
                "imageAttribute": {
                    "url": "https://m.media-amazon.com/images/I/21qLKDdC+yL.jpg",
                    "width": 500,
                    "height": 500,
                },
                "slots": [{"metaData": {"key": "apexPrice"}, "displayData": {}}],
            },
            {
                "indexInDimList": 2,
                "defaultAsin": "B0BT4FN3X6",
                "dimensionValueDisplayText": "Grapefruit",
                "dimensionValueState": "AVAILABLE",
                "dimensionDisplaySubType": "image",
                "asinHiddenInCollapseView": False,
                "slotsFetched": True,
                "imageAttribute": {
                    "url": "https://m.media-amazon.com/images/I/31nXKFhJf-L.jpg",
                    "width": 500,
                    "height": 500,
                },
                "slots": [],
            },
        ]
    },
}
_SOCIAL_PROOFING_STATE = {"loggedIn": False, "asin": _ASIN, "availableFaceouts": "TK_BOUGHT"}


def _a_state(key: str, payload: dict) -> str:
    meta = json.dumps({"key": key}).replace('"', "&quot;")
    return f'<script type="a-state" data-a-state="{meta}">{json.dumps(payload)}</script>'


def _review_header(*, title: str, stars: str, date_text: str, author: str) -> str:
    """Amazon renders this block twice inside one review row; so does the fixture."""
    return (
        f'<i data-hook="review-star-rating"><span class="a-icon-alt">{stars} out of 5 '
        "stars</span></i>"
        f'<div data-hook="genome-widget"><span class="a-profile-name">{author}</span></div>'
        f'<h5 data-hook="reviewTitle">{title}</h5>'
        f'<div data-hook="review-by-line"><span data-hook="review-date">{date_text}'
        "</span></div>"
        '<div data-hook="product-variation-attributes"><span>Style: Berry</span>'
        '<div data-hook="review-badges"><span data-hook="avp-badge">Verified Purchase'
        "</span></div></div>"
    )


def _review(
    *,
    review_id: str,
    title: str = "Great mask",
    stars: str = "5",
    date_text: str = "Reviewed in the United States on July 4, 2026",
    author: str = "HonesTee",
    body: str = "Thick, nourishing, and it lasts a long time.",
    rich: bool = True,
    helpful: str | None = "7 people found this helpful",
) -> str:
    header = _review_header(title=title, stars=stars, date_text=date_text, author=author)
    inner = (
        f'<div data-hook="reviewRichContentContainer"><p><span>{body}</span></p></div>'
        if rich
        else f"<span>{body}</span>"
    )
    helpful_block = (
        f'<span data-hook="helpful-vote-statement">{helpful}</span>' if helpful else ""
    )
    return (
        f'<div id="{review_id}" data-hook="review">'
        f"{header}{header}"
        '<div data-hook="reviewText">'
        "<div>Brief content visible, double tap to read full content.</div>"
        f"{inner}"
        "<span>Read more</span><span>Read less</span>"
        "</div>"
        f"{helpful_block}"
        "</div>"
    )


_US_REVIEWS = "".join(
    _review(review_id=f"R1S7HOZY4X45Z{suffix}") for suffix in ("I", "J")
)
_INTERNATIONAL_REVIEW = _review(
    review_id="R2S7HOZY4X45ZK",
    date_text="Reviewed in Australia on February 26, 2026",
    author="Oliver G",
    body="Great product and feels good.",
    helpful=None,
)

_VISIBLE_TEXT = """Deliver to
New York 10001
4.6 out of 5 stars
(37,045)
70K+ bought in past month
$24.00
In Stock
37,045 global ratings
"""


def _histogram(asin: str = _ASIN) -> str:
    rows = "".join(
        f'<a aria-label="{percent} percent of reviews have {word} stars" '
        f'href="/portal/customer-reviews/{asin}/ref=acr_dp_hist?filterByStar='
        f'{word}_star"><span>{percent}%</span></a>'
        for word, percent in (
            ("five", 81),
            ("four", 11),
            ("three", 5),
            ("two", 1),
            ("one", 2),
        )
    )
    return f'<ul id="histogramTable">{rows}</ul>'


def _dom(
    *,
    extra_head: str = "",
    price_modules: str | None = None,
    social_proofing: str | None = None,
    ship_sold: str | None = None,
    twister: str | None = None,
    reviews: str | None = None,
    histogram_asin: str = _ASIN,
    asin_input: str = _ASIN,
    currency: str = "USD",
    detail_bullet_asin: str = _ASIN,
) -> bytes:
    price = (
        price_modules
        if price_modules is not None
        else (
            _celwidget(
                feature="newAccordionCaption",
                body="One-time purchase",
                slot="newAccordionRow_0",
                active="true",
            )
            + _celwidget(
                feature="corePrice",
                body=_price_body("24.00"),
                slot="newAccordionRow_0",
                active="true",
                element_id="corePrice_feature_div",
            )
            + _celwidget(
                feature="corePrice",
                body=_price_body("22.80"),
                slot="snsAccordionRowMiddle",
                active="false",
                element_id="corePrice_feature_div",
            )
            + _celwidget(
                feature="corePriceDisplay_desktop", body=_price_body("24.00")
            )
        )
    )
    faceout = (
        social_proofing
        if social_proofing is not None
        else _celwidget(
            feature="socialProofingAsinFaceout",
            body=(
                '<span class="a-text-bold">70K+ bought</span><span> in past month</span>'
                + _a_state("social-proofing-page-state", _SOCIAL_PROOFING_STATE)
            ),
        )
    )
    seller = (
        ship_sold
        if ship_sold is not None
        else _celwidget(
            feature="shipFromSoldByAbbreviatedODF",
            body=(
                "<span>Ships from: </span><span>Amazon.com</span>"
                "<span>Sold by: </span><span>Amazon.com</span>"
            ),
            slot="newAccordionRow_0",
            active="true",
        )
    )
    twister_module = (
        twister
        if twister is not None
        else _celwidget(
            feature="twister",
            body=_a_state("desktop-twister-sort-filter-data", _TWISTER_STATE),
        )
    )
    review_rows = reviews if reviews is not None else _US_REVIEWS + _INTERNATIONAL_REVIEW
    body = f"""<html><head><title>Amazon.com: LANEIGE Lip Sleeping Mask</title></head><body>
{extra_head}
<input type="hidden" id="ASIN" name="ASIN" value="{asin_input}">
<input type="hidden" name="currencyOfPreference" value="{currency}">
<input type="hidden" id="session-id" name="session-id" value="{_SESSION_ID}">
<input type="hidden" name="anti-csrftoken-a2z" value="{_CSRF_TOKEN}">
<span class="nav-line-2" id="glow-ingress-line2">New York 10001</span>
<span id="productTitle">LANEIGE Lip Sleeping Mask: Berry</span>
<a id="visitStoreLink" href="/stores/node/23666223011?ref_=dp&amp;x=1">Visit the LANEIGE Store</a>
<img id="logoByLine" title="LANEIGE">
<a class="a-link-normal" href="/Lip-Care-Products/b/ref=dp_bc_3?ie=UTF8&amp;node=3761351">Lip Care</a>
{price}
{faceout}
{seller}
{twister_module}
{_celwidget(feature="acBadge", body='<span class="mvt-ac-badge-rectangle">Amazon&#39;s Choice</span>')}
{_celwidget(feature="availabilityInsideBuyBox", body='<div id="availability"><span class="a-color-success primary-availability-message"> In Stock </span></div>', slot="newAccordionRow_0", active="true")}
{_celwidget(feature="deliveryBlock", body='<span data-csa-c-content-id="DEXUnifiedCXPDM" data-csa-c-delivery-price="FREE" data-csa-c-delivery-type="delivery" data-csa-c-delivery-time="Saturday, July 25" data-csa-c-delivery-condition="on orders shipped by Amazon over $35" data-csa-c-mir-type="DELIVERY" data-csa-c-mir-sub-type="CONDITIONALLY_FREE"> FREE delivery </span>', slot="newAccordionRow_0", active="true")}
{_celwidget(feature="mediaBlock", body='<img id="landingImage" data-a-dynamic-image="{&quot;https://m.media-amazon.com/images/I/51VfrPOslWL._SX342_.jpg&quot;:[342,342]}"><li data-csa-c-media-type="IMAGE" data-csa-c-content-id="51VfrPOslWL" data-csa-c-media-block-entity="primaryView" data-csa-c-posx="0"></li>')}
{_celwidget(feature="voyagerAccordian", body='<div id="feature-bullets"><ul><li><span class="a-list-item">A leave-on lip mask.</span></li><li><span class="a-list-item">Skin Type: Normal, Dry.</span></li></ul></div>')}
{_celwidget(feature="productSupportInsideAccordionHeaderODF", body="", slot="newAccordionRow_0", active="true")}
{_celwidget(feature="ask", body="", asin=None)}
{_celwidget(feature="aplus", body='<div id="aplus_feature_div">brand story</div>', asin=None)}
<div id="detailBullets_feature_div"><ul>
<li><span class="a-list-item"><span class="a-text-bold">Manufacturer &#8207; : &#8206; </span><span>LANEIGE</span></span></li>
<li><span class="a-list-item"><span class="a-text-bold">ASIN &#8207; : &#8206; </span><span>{detail_bullet_asin}</span></span></li>
<li><span class="a-list-item"><span class="a-text-bold"> Best Sellers Rank: </span> #319 in Beauty &amp; Personal Care</span></li>
</ul></div>
{_histogram(histogram_asin)}
{_celwidget(feature="averageCustomerReviews", body='<span id="acrPopover" title="4.6 out of 5 stars"></span><span id="acrCustomerReviewText">37,045 ratings</span>')}
<div id="customerReviews">
<div id="localTopReviewsList"><h2>Top reviews from the United States</h2>{review_rows if reviews is not None else _US_REVIEWS}</div>
<div id="internationalTopReviews"><h2>Top reviews from other countries</h2>{_INTERNATIONAL_REVIEW if reviews is None else ""}</div>
</div>
</body></html>"""
    return body.encode("utf-8")


def _build(**kwargs):
    return build_amazon_pdp_aggregate_content_record(
        rendered_dom=kwargs.pop("rendered_dom", None) or _dom(),
        visible_text=kwargs.pop("visible_text", None) or _VISIBLE_TEXT.encode("utf-8"),
        source_url=kwargs.pop("source_url", _SOURCE_URL),
    )


def _rows(record: dict, kind: str) -> list[dict]:
    return [row for row in record["rows"] if row["row_kind"] == kind]


def _fields(record: dict, kind: str) -> dict:
    matches = _rows(record, kind)
    assert len(matches) == 1, f"expected exactly one {kind} row, found {len(matches)}"
    return matches[0]["source_visible_fields"]


def test_record_identity_and_versions_are_amazon_local() -> None:
    record = _build()

    assert record["record_kind"] == "retail_pdp_amazon_aggregate_content"
    assert record["schema_version"] == AMAZON_PDP_CONTENT_SCHEMA_VERSION
    assert record["parser_version"] == AMAZON_PDP_PARSER_VERSION
    assert record["capture_profile"] == "amazon_pdp_aggregate"
    assert record["asin"] == _ASIN
    assert record["review_provider"] == "amazon_native_rendered_pdp"


def test_exact_review_bodies_are_retained_here_because_no_companion_owns_them() -> None:
    """The inversion from Target: Amazon's companion is body-free, so this record keeps bodies."""
    record = _build()
    rows = _rows(record, "retail_review_row")

    assert record["review_body_retention"] == "exact_bodies_retained_in_this_record"
    assert len(rows) == 3
    bodies = [row["source_visible_fields"]["body"] for row in rows]
    assert bodies[0] == "Thick, nourishing, and it lasts a long time."
    assert bodies[-1] == "Great product and feels good."
    for row in rows:
        fields = row["source_visible_fields"]
        assert fields["body_retained_here"] is True
        assert fields["body_source"] == "amazon_review_rich_content_container"
        # The exact body carries no a11y teaser or Read more/less page chrome.
        assert "double tap to read" not in fields["body"]
        assert "Read more" not in fields["body"]
        assert "double tap to read" in fields["review_text_hook_with_page_chrome"]


def test_review_rows_undouble_amazons_repeated_header_markup() -> None:
    record = _build()
    fields = _rows(record, "retail_review_row")[0]["source_visible_fields"]

    assert fields["title"] == "Great mask"
    assert fields["rating_text"] == "5 out of 5 stars"
    assert fields["source_date_text"] == "Reviewed in the United States on July 4, 2026"
    assert fields["source_date"] == "2026-07-04"
    assert fields["review_location"] == "the United States"
    assert fields["author"] == "HonesTee"
    assert fields["verified_purchase"] is True
    assert fields["badge_labels"] == ["Verified Purchase"]
    assert fields["helpful_count"] == 7


def test_international_rows_are_preserved_outside_the_us_analysis_window() -> None:
    record = _build()
    review = _fields(record, "retail_review_substrate")
    sections = [
        row["source_visible_fields"]["section"]
        for row in _rows(record, "retail_review_row")
    ]

    assert review["united_states_rows"] == 2
    assert review["other_countries_rows"] == 1
    assert review["default_us_market_analysis_window"] == "top_reviews_united_states"
    assert sections.count("top_reviews_other_countries") == 1
    assert (
        "amazon_international_review_rows_preserved_but_excluded_from_us_analysis_window"
        in record["residuals"]
    )


def test_body_source_falls_back_and_is_labelled_when_rich_content_is_absent() -> None:
    record = _build(
        rendered_dom=_dom(reviews=_review(review_id="R3S7HOZY4X45ZL", rich=False))
    )
    fields = _rows(record, "retail_review_row")[0]["source_visible_fields"]

    assert (
        fields["body_source"]
        == "amazon_reviewText_hook_without_rich_content_container"
    )
    assert "Thick, nourishing" in fields["body"]


def test_buybox_retains_every_target_bound_buying_option() -> None:
    record = _build()
    offer = _fields(record, "retail_variant_offer")

    assert offer["price"] == "24.00"
    assert offer["price_isolation"] == "amazon_target_bound_active_buying_option"
    assert offer["buying_option_count"] == 2
    assert [option["price"] for option in offer["buying_options"]] == ["24.00", "22.80"]
    assert offer["buying_options"][0]["buying_option_caption"] == "One-time purchase"
    assert offer["buying_options"][0]["is_initial_active_row"] is True
    assert offer["buying_options"][1]["buying_option_slot_id"] == "snsAccordionRowMiddle"
    assert record["offer_module_state"] == "hydrated_in_rendered_dom"


def test_offer_does_not_bind_an_unrelated_products_price_module() -> None:
    rail_price = _celwidget(
        feature="corePrice",
        body=_price_body("9.99"),
        asin="B000RECOMMEND",
        slot="newAccordionRow_0",
        active="true",
    )
    with pytest.raises(ValueError, match="refusing to bind an unrelated-product"):
        _build(rendered_dom=_dom(price_modules=rail_price))


def test_apex_display_price_that_no_buying_option_carries_fails_loud() -> None:
    modules = (
        _celwidget(
            feature="corePrice",
            body=_price_body("24.00"),
            slot="newAccordionRow_0",
            active="true",
        )
        + _celwidget(feature="corePriceDisplay_desktop", body=_price_body("19.99"))
    )
    with pytest.raises(ValueError, match="no target-bound buying option carries"):
        _build(rendered_dom=_dom(price_modules=modules))


def test_bought_in_past_month_must_be_target_asin_bound() -> None:
    """Two independent lanes found this defect class; it stays a gate, not a nicety."""
    rail = _celwidget(
        feature="socialProofingAsinFaceout",
        body='<span class="a-text-bold">9K+ bought</span><span> in past month</span>',
        asin="B000RECOMMEND",
    )
    with pytest.raises(ValueError, match="refusing to bind an unrelated-product"):
        _build(rendered_dom=_dom(social_proofing=rail))


def test_page_global_bought_in_past_month_without_a_bound_module_fails_loud() -> None:
    with pytest.raises(ValueError, match="refusing to bind a page-global"):
        _build(rendered_dom=_dom(social_proofing=""))


def test_social_proofing_state_naming_another_asin_fails_loud() -> None:
    mismatched = _celwidget(
        feature="socialProofingAsinFaceout",
        body=(
            '<span class="a-text-bold">70K+ bought</span><span> in past month</span>'
            + _a_state(
                "social-proofing-page-state", {**_SOCIAL_PROOFING_STATE, "asin": "B000OTHER1"}
            )
        ),
    )
    with pytest.raises(ValueError, match="social-proofing page state names ASIN"):
        _build(rendered_dom=_dom(social_proofing=mismatched))


def test_seller_and_shipper_must_be_target_asin_bound() -> None:
    record = _build()
    offer = _fields(record, "retail_variant_offer")

    assert offer["seller"] == "Amazon.com"
    assert offer["shipper"] == "Amazon.com"
    assert (
        offer["seller_binding_source"]
        == "amazon_target_bound_shipFromSoldByAbbreviatedODF_module"
    )

    rail = _celwidget(
        feature="shipFromSoldByAbbreviatedODF",
        body="<span>Ships from: </span><span>Other</span><span>Sold by: </span><span>Other</span>",
        asin="B000RECOMMEND",
    )
    with pytest.raises(ValueError, match="refusing to bind an unrelated-product"):
        _build(rendered_dom=_dom(ship_sold=rail))


def test_quick_view_social_proof_disagreement_is_preserved_not_resolved() -> None:
    """The harvested #pqv anchor carries a past-week window on the proof packet."""
    record = _build(
        rendered_dom=_dom(
            extra_head='<p id="pqv-bought-in-last-month">1K+ bought in past week</p>'
        )
    )
    offer = _fields(record, "retail_variant_offer")

    assert offer["bought_in_past_month"] == "70K+ bought in past month"
    assert offer["quick_view_social_proof_text"] == "1K+ bought in past week"
    assert (
        "amazon_quick_view_social_proof_disagrees_with_faceout_badge_both_preserved"
        in record["residuals"]
    )


def test_variants_come_from_amazons_own_twister_dimension_state() -> None:
    record = _build()
    variants = [row["source_visible_fields"] for row in _rows(record, "retail_variant_state")]

    assert record["variant_module_state"] == "observed"
    assert len(variants) == 2
    assert variants[0]["variant_asin"] == _ASIN
    assert variants[0]["is_selected"] is True
    assert variants[0]["is_requested_target"] is True
    assert variants[1]["variant_display_text"] == "Grapefruit"
    assert variants[1]["variant_state"] == "AVAILABLE"
    assert variants[1]["variant_price_posture"] == "not_exposed_in_twister_state"
    assert "amazon_twister_variant_prices_not_exposed_in_page_state" in record["residuals"]


def test_hydrated_twister_without_parsable_state_fails_loud() -> None:
    """A newly exposed variant surface with no lossless parse forces raw fallback."""
    with pytest.raises(ValueError, match="refusing to report variants as observed"):
        _build(
            rendered_dom=_dom(
                twister=_celwidget(feature="twister", body="<div>rendered swatches</div>")
            )
        )


def test_twister_state_that_does_not_select_the_requested_asin_fails_loud() -> None:
    state = json.loads(json.dumps(_TWISTER_STATE))
    state["sortedDimValuesForAllDims"]["style_name"][0]["defaultAsin"] = "B000OTHER1"
    module = _celwidget(
        feature="twister", body=_a_state("desktop-twister-sort-filter-data", state)
    )
    with pytest.raises(ValueError, match="does not select exactly the requested ASIN"):
        _build(rendered_dom=_dom(twister=module))


def test_absent_twister_module_reports_not_exposed_without_variant_rows() -> None:
    record = _build(rendered_dom=_dom(twister=""))

    assert record["variant_module_state"] == "not_exposed"
    assert not _rows(record, "retail_variant_state")


def test_declared_modules_are_inventoried_with_render_and_binding_state() -> None:
    record = _build()
    inventory = _fields(record, "retail_carried_module")
    by_name = {
        row["feature_name"]: row for row in inventory["declared_modules"]
    }

    assert inventory["module_role"] == "detail_page_module_inventory"
    assert inventory["declared_module_count"] == len(inventory["declared_modules"])
    assert by_name["corePriceDisplay_desktop"]["server_side_render"] == "hydrated"
    assert by_name["corePriceDisplay_desktop"]["target_asin_bound"] is True
    # Declared-but-unhydrated modules are inventoried, never omitted.
    assert (
        by_name["productSupportInsideAccordionHeaderODF"]["server_side_render"]
        == "declared_unhydrated"
    )
    assert by_name["ask"]["server_side_render"] == "declared_unhydrated"
    assert by_name["aplus"]["target_asin_bound"] is False
    assert inventory["declared_unhydrated_module_count"] >= 2
    assert (
        "amazon_declared_unhydrated_detail_page_modules_inventoried_not_retained"
        in record["residuals"]
    )


def test_review_aggregate_and_histogram_bind_to_the_target_asin() -> None:
    record = _build()
    review = _fields(record, "retail_review_substrate")

    assert review["rating"] == "4.6"
    assert review["rating_count"] == "37,045"
    assert review["rating_distribution_percent"] == {"5": 81, "4": 11, "3": 5, "2": 1, "1": 2}
    assert review["rating_histogram_binding_source"].endswith(_ASIN)
    assert review["bazaarvoice_marker_count"] == 0
    assert review["review_provider"] == "amazon_native_rendered_pdp"


def test_histogram_links_for_another_asin_fail_loud() -> None:
    with pytest.raises(ValueError, match="histogram links reference non-target"):
        _build(rendered_dom=_dom(histogram_asin="B000OTHER1"))


def test_product_details_must_declare_the_requested_asin() -> None:
    record = _build()
    subtree = _fields(record, "retail_product_module_subtree")

    assert subtree["product_details_declared_asin"] == _ASIN
    assert {"label": "Manufacturer", "value": "LANEIGE"} in subtree["product_details"]
    assert subtree["best_sellers_rank_text"].startswith("#319 in Beauty")
    assert subtree["feature_bullet_count"] == 2
    assert subtree["media_bytes_fetched"] is False
    assert subtree["image_reference_count"] == 1

    with pytest.raises(ValueError, match="bullet list declares ASIN"):
        _build(rendered_dom=_dom(detail_bullet_asin="B000OTHER1"))


@pytest.mark.parametrize(
    "marker",
    ['<div id="cr-summarization-attributes-list">Customers say</div>', '<a id="askATFLink">Q</a>'],
)
def test_newly_exposed_unparsable_surface_forces_raw_fallback(marker: str) -> None:
    """retailer_information_extraction_standard_v0.md:210,216 requires this."""
    with pytest.raises(ValueError, match="cannot retain losslessly"):
        _build(rendered_dom=_dom(extra_head=marker))


def test_absent_ai_summary_and_qa_are_recorded_as_not_exposed() -> None:
    record = _build()

    assert record["ai_review_summary_state"] == "not_exposed_on_target_pdp"
    assert record["customer_q_and_a_state"] == "not_exposed_on_target_pdp"
    review = _fields(record, "retail_review_substrate")
    assert review["customer_q_and_a_status"] == "not_exposed_on_target_pdp"
    assert (
        "amazon_no_customer_product_qa_is_exposed_aplus_faq_is_brand_authored"
        in record["residuals"]
    )


def test_refuses_to_emit_guest_session_or_csrf_material() -> None:
    leaking = _dom(
        extra_head=f'<span id="productTitle">Mask {_SESSION_ID}</span>'
    )
    # The session id is echoed into a retained product field.
    with pytest.raises(ValueError, match="refusing"):
        _build(rendered_dom=leaking)


def test_short_product_copy_is_not_mistaken_for_a_secret() -> None:
    """Length alone never decides: only secret-bearing keys contribute values."""
    record = _build(
        rendered_dom=_dom(
            extra_head='<input type="hidden" id="marketplaceID" value="ATVPDKIKX0DER">'
        )
    )
    subtree = _fields(record, "retail_product_module_subtree")

    assert subtree["product_details_declared_asin"] == _ASIN
    assert (
        "amazon_guest_session_and_csrf_material_present_not_retained"
        in record["residuals"]
    )


@pytest.mark.parametrize(
    "bad_url",
    [
        "https://www.amazon.com/Laneige-Sleeping-Berry",
        "https://www.amazon.sg/dp/B07XXPHQZK",
        "https://example.com/dp/B07XXPHQZK",
        "https://www.amazon.com/dp/B07XXPHQZK/dp/B000OTHER1",
    ],
)
def test_rejects_urls_that_do_not_bind_exactly_one_amazon_asin(bad_url: str) -> None:
    with pytest.raises(ValueError, match="exactly one /dp/"):
        _build(source_url=bad_url)


def test_fails_loud_when_the_rendered_asin_input_disagrees_with_the_url() -> None:
    with pytest.raises(ValueError, match="do not match the requested ASIN"):
        _build(rendered_dom=_dom(asin_input="B000OTHER1"))


def test_fails_loud_without_exact_us_currency_evidence() -> None:
    with pytest.raises(ValueError, match="currencyOfPreference=USD"):
        _build(rendered_dom=_dom(currency="SGD"))


def test_record_model_requires_the_singleton_rows_and_review_rows() -> None:
    record = _build()

    trimmed = [row for row in record["rows"] if row["row_kind"] != "retail_pdp_product"]
    with pytest.raises(ValueError, match="exactly one product, offer"):
        AmazonPdpAggregateContentRecord.model_validate({**record, "rows": trimmed})

    bodyless = [row for row in record["rows"] if row["row_kind"] != "retail_review_row"]
    with pytest.raises(ValueError, match="must retain the exposed review rows"):
        AmazonPdpAggregateContentRecord.model_validate({**record, "rows": bodyless})


def test_qualification_route_uses_the_family_owned_parser() -> None:
    parser_version, _extractor = _ROUTES["amazon"]

    assert parser_version == AMAZON_PDP_PARSER_VERSION


def test_content_record_does_not_smuggle_the_disposable_inputs() -> None:
    """Content retention must extract, never embed, the DOM it discards.

    Storage impact is measured against the real proof packet in this route's
    proof record; a synthetic fixture cannot honestly assert a compaction ratio.
    """
    record = _build()
    blob = json.dumps(record)

    # Source anchors legitimately name Amazon's selectors; the raw markup, the
    # embedded page state, and the disposable text must not survive.
    assert "<html" not in blob and "<script" not in blob and "<div " not in blob
    assert "data-csa-c-id" not in blob
    assert "a-offscreen" not in blob
    assert "sortedDimValuesForAllDims" not in blob
    assert _SESSION_ID not in blob
    assert _CSRF_TOKEN not in blob


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
            title="Amazon.com",
            rendered_dom="<html><body>parser drift, no review sections</body></html>",
            visible_text="parser drift",
            screenshot_png=b"\x89PNG\r\n\x1a\namazon",
            metadata={
                "requested_url": _SOURCE_URL,
                "final_url": _SOURCE_URL,
                "title": "Amazon.com",
                "capture_timestamp": "2026-07-22T00:00:00Z",
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
                "rendered_dom_byte_count": 55,
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
        decision_question="Does Amazon retain the canonical product and review evidence?",
        output_directory=output,
        capture_context="Amazon raw fallback unit proof",
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
            extractor_version=AMAZON_PDP_PARSER_VERSION,
            extractor=lambda _dom, _text, _url: build_amazon_pdp_aggregate_content_record(
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


def test_content_capture_requires_the_admitted_us_delivery_pin(capsys) -> None:
    """The pre-v3 envelope admits exactly one anonymous US destination."""
    from runners.run_source_capture_cloakbrowser_packet import main

    with pytest.raises(SystemExit) as excinfo:
        main(
            [
                "--url",
                _SOURCE_URL,
                "--source-family",
                "retail_pdp",
                "--source-surface",
                "cloakbrowser_snapshot",
                "--decision-question",
                "envelope gate",
                "--output",
                "unused",
                "--capture-context",
                "envelope gate",
                "--operator-category",
                "cloakbrowser_snapshot_cli_operator",
                "--capture-mode",
                "multimodal",
                "--retail-capture-profile",
                "amazon_pdp_aggregate",
                "--delivery-zip",
                "94105",
            ]
        )

    assert excinfo.value.code == 2
    assert (
        "amazon_pdp_aggregate content capture requires --delivery-zip 10001"
        in capsys.readouterr().err
    )
