from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot
from source_capture.amazon_review_onboarding_capture import (
    AMAZON_REVIEW_ONBOARDING_PARSER_VERSION,
    AmazonReviewOnboardingCaptureError,
    capture_amazon_review_onboarding_packet,
)
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet

URL = "https://www.amazon.com/Laneige-Sleeping-Berry/dp/B07XXPHQZK"


def _parent(root: DataLakeRoot, tmp_path: Path, pin: bool = True, html: str | None = None) -> str:
    html = html if html is not None else """<input name="currencyOfPreference" value="USD"><a href="?filterByStar=five_star">5 star 80%</a><div id="localTopReviews"><h3>Top reviews from the United States</h3><div data-hook="review" id="R123456789"><span data-hook="review-by-line">Alice</span><i data-hook="review-star-rating">5.0 out of 5 stars</i><a data-hook="reviewTitle">Excellent</a><span data-hook="review-date">Reviewed in the United States on July 1, 2026</span><span data-hook="avp-badge">Verified Purchase</span><span data-hook="reviewText">The exact first review body.</span><span data-hook="helpful-vote-statement">2 people found this helpful</span><div data-hook="review-image-tile"><img src="https://images.example/review.jpg"/></div></div></div><div id="internationalTopReviews"><h3>Top reviews from other countries</h3><div data-hook="review" id="RABCDEFGHI"><span data-hook="review-by-line">Bob</span><i data-hook="review-star-rating">4.0 out of 5 stars</i><a data-hook="reviewTitle">Good</a><span data-hook="review-date">Reviewed in Canada on June 2, 2026</span><span data-hook="reviewText">The exact second review body.</span></div></div><div class="aplus-question">Brand FAQ?</div>"""
    metadata = {"final_url": URL + "?th=1", "access_blocked": False, "pin_confirmed": pin, "retail_capture_profile": {"name": "amazon_pdp_aggregate"}}
    sources = {"cloakbrowser_rendered_dom.html": html, "cloakbrowser_visible_text.txt": "4.6 out of 5 stars 12,345 global ratings", "cloakbrowser_snapshot_metadata.json": json.dumps(metadata)}
    paths = []
    for name, body in sources.items():
        path = tmp_path / name
        path.write_text(body, encoding="utf-8")
        paths.append(path)
    return write_local_source_capture_packet(data_root=root, input_files=paths, source_family="retail_pdp", source_surface="cloakbrowser_snapshot", source_locator=known_fact(URL), decision_question="test", capture_context="US fixture").packet.packet_id

def _summary(root: DataLakeRoot, packet_id: str) -> bytes:
    packet = root.load_raw_packet(packet_id)
    file_id = next(row["file_id"] for row in packet.manifest["preserved_files"] if row["relative_packet_path"].endswith("amazon_review_onboarding_summary.json"))
    return packet.bodies[file_id]

def test_capture_is_truthful_and_body_free(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent = _parent(root, tmp_path)
    code, result = capture_amazon_review_onboarding_packet(data_root=root, parent_packet_id=parent)
    raw = _summary(root, result["packet_id"])
    summary = json.loads(raw)
    rows = summary["reviews"]["review_inventory"]
    assert code == 0 and summary["provider"] == "amazon_native_rendered_pdp"
    assert summary["route_classification"]["bazaarvoice_marker_count"] == 0
    assert summary["review_aggregate"]["rating_distribution_percent"] == {"5": 80}
    assert [row["review_id"] for row in rows] == ["R123456789", "RABCDEFGHI"]
    assert rows[0]["helpful_count"] == 2 and rows[0]["verified_purchase"] is True
    assert rows[0]["raw_anchor"]["parent_packet_id"] == parent
    assert summary["questions"]["excluded_brand_authored_aplus_faq_questions"] == 1
    assert summary["extraction_target_matrix"]["most_recent"] == "not_exposed_in_parent"
    assert b"The exact first review body." not in raw


def test_capture_rejects_unconfirmed_us_pin(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    with pytest.raises(AmazonReviewOnboardingCaptureError, match="US delivery pin"):
        capture_amazon_review_onboarding_packet(data_root=root, parent_packet_id=_parent(root, tmp_path, False))


# --- v2 precise-field regressions -------------------------------------------
# The fixture above is idealized: one header copy, a name inside
# `review-by-line`, and a bare `reviewText` body. Real Amazon rows repeat the
# whole header inside one `data-hook="review"`, put only the date in
# `review-by-line`, carry the reviewer's name in the profile widget, and wrap
# the body in a11y teaser text plus a Read more/less footer. Measured on parent
# packet 01KY0PHPN10205MKKCK1GB7YH1; see
# docs/research/forseti_amazon_canonical_content_capture_proof_v0.md section 5.

_REAL_SHAPE_DOM = (
    '<input name="currencyOfPreference" value="USD">'
    '<a href="?filterByStar=five_star">5 star 80%</a>'
    '<div id="localTopReviews"><h3>Top reviews from the United States</h3>'
    '<div data-hook="review" id="R1S7HOZY4X45ZI">'
    # header rendered twice, exactly as Amazon emits it
    '<div class="a-profile-content"><span class="a-profile-name">HonesTee</span></div>'
    '<i data-hook="review-star-rating">5.0 out of 5 stars</i>'
    '<a data-hook="reviewTitle">Hydrating Lip Mask</a>'
    '<span data-hook="review-by-line">'
    '<span data-hook="review-date">Reviewed in the United States on July 4, 2026</span>'
    "</span>"
    '<span data-hook="avp-badge">Verified Purchase</span>'
    '<span data-hook="product-variation-attributes">Style: Berry</span>'
    '<div class="a-profile-content"><span class="a-profile-name">HonesTee</span></div>'
    '<i data-hook="review-star-rating">5.0 out of 5 stars</i>'
    '<a data-hook="reviewTitle">Hydrating Lip Mask</a>'
    '<span data-hook="review-by-line">'
    '<span data-hook="review-date">Reviewed in the United States on July 4, 2026</span>'
    "</span>"
    '<span data-hook="avp-badge">Verified Purchase</span>'
    '<span data-hook="product-variation-attributes">Style: Berry</span>'
    # body: a11y teaser + exact rich container + Read more/less footer
    '<span data-hook="reviewText">The media could not be loaded. '
    '<span data-hook="reviewRichContentContainer">The exact body only.</span>'
    " Read more Read less</span>"
    "</div></div>"
)


def _summary_for(tmp_path: Path, html: str) -> dict:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    parent = _parent(root, tmp_path, html=html)
    _code, result = capture_amazon_review_onboarding_packet(
        data_root=root, parent_packet_id=parent
    )
    return json.loads(_summary(root, result["packet_id"]))


def _only_row(summary: dict) -> dict:
    rows = summary["reviews"]["review_inventory"]
    assert len(rows) == 1
    return rows[0]


def test_author_is_the_reviewer_not_the_review_date(tmp_path: Path) -> None:
    row = _only_row(_summary_for(tmp_path, _REAL_SHAPE_DOM))

    assert row["author"] == "HonesTee"
    assert "Reviewed in" not in (row["author"] or "")


def test_multiple_profile_names_remain_unresolved_not_synthetically_joined(
    tmp_path: Path,
) -> None:
    html = _REAL_SHAPE_DOM.replace(
        '<span class="a-profile-name">HonesTee</span></div>'
        '<i data-hook="review-star-rating">5.0 out of 5 stars</i>',
        '<span class="a-profile-name">Second Profile</span></div>'
        '<i data-hook="review-star-rating">5.0 out of 5 stars</i>',
        1,
    )
    summary = _summary_for(tmp_path, html)
    row = _only_row(summary)

    assert row["author"] is None
    assert row["author_profile_names"] == ["HonesTee", "Second Profile"]
    assert row["author_resolution"] == "multiple_profile_names_unresolved"
    assert summary["reviews"]["ambiguous_author_rows"] == ["R1S7HOZY4X45ZI"]
    assert any(
        item["category"] == "author_identity" for item in summary["loss_ledger"]
    )


def test_doubled_header_text_is_collapsed_to_one_copy(tmp_path: Path) -> None:
    row = _only_row(_summary_for(tmp_path, _REAL_SHAPE_DOM))

    assert row["title"] == "Hydrating Lip Mask"
    assert row["rating_text"] == "5.0 out of 5 stars"
    assert row["source_date_text"] == "Reviewed in the United States on July 4, 2026"
    assert row["variant_text"] == "Style: Berry"
    assert row["badge_labels"] == ["Verified Purchase"]
    # _DATE_RE's non-greedy group runs across both copies on a doubled row.
    assert row["review_location"] == "the United States"


def test_body_hash_describes_the_exact_body_not_page_chrome(tmp_path: Path) -> None:
    row = _only_row(_summary_for(tmp_path, _REAL_SHAPE_DOM))
    exact = "The exact body only."

    assert row["body_character_count"] == len(exact)
    assert row["body_sha256"] == hashlib.sha256(exact.encode("utf-8")).hexdigest()
    assert row["body_hash_basis"] == "review_rich_content_container"
    assert row["body_present"] is True


def test_verified_purchase_survives_a_doubled_badge(tmp_path: Path) -> None:
    """The v1 rollup tested the raw badge for equality, so a doubled
    'Verified Purchase Verified Purchase' silently undercounted it."""
    summary = _summary_for(tmp_path, _REAL_SHAPE_DOM)

    assert _only_row(summary)["verified_purchase"] is True
    assert summary["reviews"]["verified_purchase_rows"] == 1
    assert summary["reviews"]["captured_review_rows"] == 1


def test_summary_declares_the_v2_record_kind_and_parser(tmp_path: Path) -> None:
    summary = _summary_for(tmp_path, _REAL_SHAPE_DOM)

    assert summary["record_kind"] == "amazon_review_onboarding_summary_v2"
    assert summary["parser_version"] == "amazon_pdp_review_onboarding_v2"
    assert AMAZON_REVIEW_ONBOARDING_PARSER_VERSION == "amazon_pdp_review_onboarding_v2"


def test_summary_still_never_carries_review_bodies(tmp_path: Path) -> None:
    summary = _summary_for(tmp_path, _REAL_SHAPE_DOM)

    assert "The exact body only." not in json.dumps(summary)
    assert summary["content_qualification"]["summary_duplicates_review_bodies"] is False
