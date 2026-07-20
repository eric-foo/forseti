from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot
from source_capture.amazon_review_onboarding_capture import (
    AmazonReviewOnboardingCaptureError,
    capture_amazon_review_onboarding_packet,
)
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet

URL = "https://www.amazon.com/Laneige-Sleeping-Berry/dp/B07XXPHQZK"


def _parent(root: DataLakeRoot, tmp_path: Path, pin: bool = True) -> str:
    html = """<input name="currencyOfPreference" value="USD"><a href="?filterByStar=five_star">5 star 80%</a><div id="localTopReviews"><h3>Top reviews from the United States</h3><div data-hook="review" id="R123456789"><span data-hook="review-by-line">Alice</span><i data-hook="review-star-rating">5.0 out of 5 stars</i><a data-hook="reviewTitle">Excellent</a><span data-hook="review-date">Reviewed in the United States on July 1, 2026</span><span data-hook="avp-badge">Verified Purchase</span><span data-hook="reviewText">The exact first review body.</span><span data-hook="helpful-vote-statement">2 people found this helpful</span><div data-hook="review-image-tile"><img src="https://images.example/review.jpg"/></div></div></div><div id="internationalTopReviews"><h3>Top reviews from other countries</h3><div data-hook="review" id="RABCDEFGHI"><span data-hook="review-by-line">Bob</span><i data-hook="review-star-rating">4.0 out of 5 stars</i><a data-hook="reviewTitle">Good</a><span data-hook="review-date">Reviewed in Canada on June 2, 2026</span><span data-hook="reviewText">The exact second review body.</span></div></div><div class="aplus-question">Brand FAQ?</div>"""
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
