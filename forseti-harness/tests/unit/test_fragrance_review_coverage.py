from __future__ import annotations

import json
from datetime import date

import pytest
from pydantic import ValidationError

from runners import run_fragrance_review_coverage as coverage_runner
from source_capture.fragrance_review_coverage import (
    FRAGRANCE_REVIEW_COVERAGE_CERTIFICATION,
    FragranceReviewCoverageInputError,
    FragranceReviewCoverageRow,
    build_fragrance_review_coverage,
)


PRODUCT_URL = "https://www.luckyscent.com/products/example-fragrance"


def _words(prefix: str, count: int) -> str:
    return " ".join(f"{prefix}{i}" for i in range(count))


def _review(
    review_id: str,
    *,
    rating: int,
    timestamp: str,
    body: str,
    verified: bool = False,
    media: bool = False,
    title: str | None = None,
) -> str:
    title_html = f'<div class="jdgm-rev__title">{title}</div>' if title else ""
    media_html = (
        '<div class="jdgm-rev__pics"><a class="jdgm-rev__pic-link">'
        '<img src="https://cdn.example/review-photo.jpg" alt="review photo"></a></div>'
        if media
        else '<img class="jdgm-rev__avatar" src="https://cdn.example/avatar.jpg" alt="avatar">'
    )
    return f"""
    <div class="jdgm-rev" data-review-id="{review_id}" data-verified-buyer="{str(verified).lower()}"
      data-product-title="Example Fragrance" data-product-url="{PRODUCT_URL}"
      data-thumb-up-count="2" data-thumb-down-count="0">
      <div class="jdgm-rev__rating" data-score="{rating}"></div>
      <span class="jdgm-rev__timestamp" data-content="{timestamp}">date label</span>
      <span class="jdgm-rev__author">Reviewer {review_id}</span>
      {title_html}
      <div class="jdgm-rev__body"><p>{body}</p></div>
      <span class="jdgm-rev__source-badge" data-badge-type="review_collected_via_store_invitation"></span>
      {media_html}
    </div>
    """


def _widget_response() -> str:
    html = "\n".join(
        [
            _review("recent-low", rating=2, timestamp="2026-04-23 19:42:02 UTC", body="short disappointment", verified=True),
            _review("core-four", rating=4, timestamp="2025-12-12 12:00:00 UTC", body=_words("balanced", 42), verified=True),
            _review("long-five", rating=5, timestamp="2025-04-01 00:00:00 UTC", body=_words("positive", 80)),
            _review("long-three", rating=3, timestamp="2024-07-01 00:00:00 UTC", body=_words("mixed", 76)),
            _review("media-three", rating=3, timestamp="2021-01-01 00:00:00 UTC", body=_words("photo", 24), media=True),
            _review("old-short-three", rating=3, timestamp="2021-02-01 00:00:00 UTC", body=_words("shortmixed", 24)),
            _review("old-short-five", rating=5, timestamp="2021-03-01 00:00:00 UTC", body=_words("shortpositive", 24)),
            _review(
                "old-mid-five",
                rating=5,
                timestamp="2021-04-01 00:00:00 UTC",
                body=_words("midpositive", 50),
                title="Old positive title",
            ),
        ]
    )
    return json.dumps({"page": 1, "total_count": 8, "html": html})


def _pdp_html() -> str:
    aggregate = {
        "@context": "https://schema.org",
        "@type": "ProductGroup",
        "name": "Example Fragrance",
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": 3.71,
            "reviewCount": 8,
            "bestRating": 5,
            "worstRating": 1,
        },
    }
    return f'<html><head><script type="application/ld+json">{json.dumps(aggregate)}</script></head></html>'


def _receipt():
    return build_fragrance_review_coverage(
        widget_responses=[_widget_response()],
        pdp_html=_pdp_html(),
        source_id="fragrance_retail_luckyscent",
        source_site="Luckyscent / Scent Bar",
        product_url=PRODUCT_URL,
        widget_route={"shop_domain": "lucky-scent-site.myshopify.com", "product_id": "8675663642945"},
        as_of_date=date(2026, 6, 29),
        source_media_filter_count=0,
    )


def test_focused_review_coverage_extracts_source_visible_receipt() -> None:
    receipt = _receipt()

    assert receipt.certification == FRAGRANCE_REVIEW_COVERAGE_CERTIFICATION
    assert receipt.aggregate_companion.rating_value == 3.71
    assert receipt.aggregate_companion.review_count == 8
    assert receipt.coverage_summary.total_rows == 8
    assert receipt.coverage_summary.widget_total_count == 8
    assert receipt.coverage_summary.native_review_id_count == 8
    assert receipt.coverage_summary.verified_true_count == 2
    assert receipt.coverage_summary.media_true_count == 1
    assert receipt.coverage_summary.selected_count == 5
    assert receipt.coverage_summary.skipped_count == 3
    assert receipt.coverage_summary.rating_counts == {"2": 1, "3": 3, "4": 1, "5": 3}
    assert receipt.coverage_summary.length_counts == {"20_39": 3, "40_74": 2, "75_plus": 2, "lt20": 1}
    assert set(receipt.selected_row_ids) == {"recent-low", "core-four", "long-five", "long-three", "media-three"}
    assert set(receipt.skipped_row_ids) == {"old-short-three", "old-short-five", "old-mid-five"}

    rows = {row.row_id: row for row in receipt.rows}
    assert "recent_low_rating_without_1_star" in rows["recent-low"].selection_reasons
    assert "core_rating_4" in rows["core-four"].selection_reasons
    assert "length_75_plus" in rows["long-five"].selection_reasons
    assert "review_media_attached" in rows["media-three"].selection_reasons
    assert rows["recent-low"].media_attached_flag is False
    assert rows["media-three"].media_attached_flag is True
    assert rows["core-four"].review_body_verbatim is not None
    assert rows["old-short-three"].review_body_verbatim is None
    assert rows["old-short-three"].review_body_sha256 is not None
    assert rows["old-short-three"].skip_reasons == ["below_focused_policy_threshold"]
    assert rows["old-mid-five"].review_body_verbatim is None
    assert rows["old-mid-five"].review_title_verbatim is None
    assert rows["old-mid-five"].review_length_bucket == "40_74"


def test_adaptive_cap_preserves_skipped_receipt() -> None:
    receipt = build_fragrance_review_coverage(
        widget_responses=[_widget_response()],
        pdp_html=_pdp_html(),
        source_id="fragrance_retail_luckyscent",
        source_site="Luckyscent / Scent Bar",
        product_url=PRODUCT_URL,
        as_of_date=date(2026, 6, 29),
        max_selected_rows=3,
    )

    assert receipt.coverage_summary.selected_count == 3
    assert receipt.coverage_summary.skipped_count == 5
    assert any(row.skip_reasons == ["adaptive_cap_excluded"] for row in receipt.rows)
    assert all(row.review_body_verbatim is None for row in receipt.rows if not row.selected_for_reader)
    assert all(row.review_title_verbatim is None for row in receipt.rows if not row.selected_for_reader)


def test_coverage_row_rejects_interpretation_fields() -> None:
    with pytest.raises(ValidationError, match="forbidden interpretation field"):
        FragranceReviewCoverageRow(
            row_id="bad",
            row_ordinal=1,
            row_source="judgeme_widget_html",
            candidate_review_key="key",
            review_key_status="candidate_key_only",
            review_body_word_count=0,
            review_length_bucket="lt20",
            source_visible_fields={"integrity_label": "high"},
        )

    row = FragranceReviewCoverageRow(
        row_id="allowed",
        row_ordinal=1,
        row_source="judgeme_widget_html",
        candidate_review_key="key",
        review_key_status="candidate_key_only",
        review_body_word_count=0,
        review_length_bucket="lt20",
        source_visible_fields={"scent_strength": "moderate"},
    )
    assert row.source_visible_fields == {"scent_strength": "moderate"}


def test_malformed_widget_json_preserves_failure_visibility() -> None:
    with pytest.raises(FragranceReviewCoverageInputError, match="widget response 1 is not parseable JSON"):
        build_fragrance_review_coverage(
            widget_responses=["{not json"],
            source_id="fragrance_retail_luckyscent",
            source_site="Luckyscent / Scent Bar",
            product_url=PRODUCT_URL,
            as_of_date=date(2026, 6, 29),
        )


def test_widget_json_route_covers_candidate_key_native_dedup_and_media() -> None:
    widget = json.dumps(
        {
            "total_count": 4,
            "reviews": [
                {
                    "id": "json-one",
                    "rating": 1,
                    "created_at": "2026-06-10 00:00:00 UTC",
                    "body": _words("bad", 25),
                    "verified_buyer": True,
                    "pictures": ["https://cdn.example/review-photo.jpg"],
                },
                {
                    "rating": 4,
                    "date": "2026-05-01",
                    "content": _words("balancedjson", 42),
                    "user_name": "No Id Reviewer",
                },
                {"id": "dupe-five", "rating": 5, "created_at": "2025-06-01", "body": _words("longjson", 80)},
                {"id": "dupe-five", "rating": 5, "created_at": "2025-06-01", "body": _words("longjson", 80)},
            ],
        }
    )

    receipt = build_fragrance_review_coverage(
        widget_responses=[widget],
        pdp_html=None,
        source_id="fragrance_retail_twisted_lily",
        source_site="Twisted Lily",
        product_url=PRODUCT_URL,
        as_of_date=date(2026, 6, 29),
        source_media_filter_count=1,
    )

    assert receipt.coverage_summary.total_rows == 3
    assert receipt.coverage_summary.widget_total_count == 4
    assert receipt.coverage_summary.native_review_id_count == 2
    assert receipt.coverage_summary.media_true_count == 1
    assert "widget_total_count_deduped_row_count_mismatch" in receipt.residuals
    assert "aggregate_companion_absent" in receipt.residuals

    one_star = next(row for row in receipt.rows if row.source_native_review_id == "json-one")
    assert one_star.row_source == "widget_json_review"
    assert one_star.media_attached_flag is True
    assert "core_rating_1" in one_star.selection_reasons
    assert len([row for row in receipt.rows if row.source_native_review_id == "dupe-five"]) == 1

    candidate_rows = [row for row in receipt.rows if row.review_key_status == "candidate_key_only"]
    assert len(candidate_rows) == 1
    candidate = candidate_rows[0]
    assert candidate.source_visible_fields["candidate_key_basis"]["row_ordinal"] == 2
    assert "candidate_key_only_weaker_than_native_id" in candidate.residuals


def test_judgeme_json_list_preserves_body_uuid_verified_media_and_widget_aggregate() -> None:
    widget = json.dumps(
        {
            "number_of_reviews": 2,
            "average_rating": "4.50",
            "reviews": [
                {
                    "uuid": "59a40313-8002-52bd-9f67-ce9907d0d6a8",
                    "title": "Special, every one",
                    "rating": 5,
                    "body_html": "<p>Great scents with enough detail to parse.</p>",
                    "verified_buyer": True,
                    "created_at": "2026-06-23T13:49:27.000Z",
                    "reviewer_name": "Allen",
                    "pictures_urls": ["https://cdn.example/review.jpg"],
                    "thumb_up": 2,
                    "thumb_down": 1,
                    "transparency_badges": ["review_written_in_shop_app"],
                    "product_title": "Essential Parfums Discovery Set",
                    "product_url": "/products/essential-parfums-discovery-set-1",
                },
                {
                    "uuid": "second-review",
                    "rating": 4,
                    "body_html": "<p>Balanced.</p>",
                    "verified_buyer": False,
                    "created_at": "2026-04-01T00:00:00.000Z",
                },
            ],
        }
    )

    receipt = build_fragrance_review_coverage(
        widget_responses=[widget],
        pdp_html=None,
        source_id="fragrance_retail_twisted_lily",
        source_site="Twisted Lily",
        product_url=PRODUCT_URL,
        as_of_date=date(2026, 6, 29),
    )

    assert receipt.aggregate_companion.source == "widget_json"
    assert receipt.aggregate_companion.rating_value == 4.5
    assert receipt.aggregate_companion.review_count == 2
    assert receipt.coverage_summary.total_rows == 2
    assert receipt.coverage_summary.widget_total_count == 2
    assert receipt.coverage_summary.native_review_id_count == 2
    assert receipt.coverage_summary.media_true_count == 1

    row = next(row for row in receipt.rows if row.source_native_review_id == "59a40313-8002-52bd-9f67-ce9907d0d6a8")
    assert row.row_source == "widget_json_review"
    assert row.review_body_verbatim == "Great scents with enough detail to parse."
    assert row.review_body_word_count == 7
    assert row.media_attached_flag is True
    assert row.verified_purchase_flag is True
    assert row.helpful_positive_count == 2
    assert row.helpful_negative_count == 1
    assert row.source_visible_fields["source_widget"] == "judge_me"
    assert row.transparency_badge_type == "review_written_in_shop_app"



def test_json_review_body_absence_html_sanitizing_and_product_mismatch_are_visible() -> None:
    widget = json.dumps(
        {
            "total_count": 3,
            "reviews": [
                {
                    "id": "plain-body-fallback",
                    "rating": 4,
                    "created_at": "2026-06-01",
                    "body": "Plain fallback body survives empty html.",
                    "body_html": "",
                },
                {
                    "id": "script-style-html",
                    "rating": 4,
                    "created_at": "2026-06-02",
                    "body_html": "<p>Readable text.</p><script>bad()</script><style>.x{color:red}</style>",
                },
                {
                    "id": "rating-only-other-product",
                    "rating": 4,
                    "created_at": "2026-06-03",
                    "product_url": "/products/other-fragrance",
                },
            ],
        }
    )

    receipt = build_fragrance_review_coverage(
        widget_responses=[widget],
        pdp_html=None,
        source_id="fragrance_retail_example",
        source_site="Example",
        product_url=PRODUCT_URL,
        as_of_date=date(2026, 6, 29),
    )

    summary = receipt.coverage_summary
    assert summary.total_rows == 3
    assert summary.review_body_captured_count == 2
    assert summary.review_body_absent_count == 1
    assert summary.selected_review_body_absent_count == 1
    assert "review_body_absent_rows_present" in receipt.residuals
    assert "selected_review_body_absent_rows_present" in receipt.residuals
    assert "review_product_url_mismatch" in receipt.residuals

    rows = {row.source_native_review_id: row for row in receipt.rows}
    assert rows["plain-body-fallback"].review_body_verbatim == "Plain fallback body survives empty html."
    assert rows["script-style-html"].review_body_verbatim == "Readable text."
    assert "bad" not in rows["script-style-html"].review_body_verbatim
    assert rows["rating-only-other-product"].review_body_verbatim is None
    assert "review_body_absent" in rows["rating-only-other-product"].residuals

def test_yotpo_v3_reviews_parse_rows_and_widget_bottomline() -> None:
    widget = json.dumps(
        {
            "pagination": {"page": 1, "perPage": 5, "total": 1},
            "bottomline": {
                "totalReview": 1,
                "averageScore": 5.0,
                "starDistribution": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 1},
            },
            "reviews": [
                {
                    "id": 833318480,
                    "score": 5,
                    "votesUp": 0,
                    "votesDown": 0,
                    "content": _words("concrete", 96),
                    "title": None,
                    "createdAt": "2026-04-24T03:03:33",
                    "verifiedBuyer": True,
                    "isIncentivized": True,
                    "incentiveType": "yotpo_loyalty_points",
                    "customFields": {
                        "22681": {
                            "title": "Age Range",
                            "fieldType": "SingleChoice",
                            "value": "25 to 34",
                        }
                    },
                    "imagesData": [],
                    "user": {"displayName": "Helen"},
                }
            ],
        }
    )

    receipt = build_fragrance_review_coverage(
        widget_responses=[widget],
        pdp_html=None,
        source_id="fragrance_retail_zgo",
        source_site="ZGO Perfumery",
        product_url=PRODUCT_URL,
        as_of_date=date(2026, 6, 29),
    )

    assert receipt.aggregate_companion.source == "widget_json"
    assert receipt.aggregate_companion.rating_value == 5.0
    assert receipt.aggregate_companion.review_count == 1
    assert receipt.coverage_summary.total_rows == 1
    assert receipt.coverage_summary.widget_total_count == 1
    assert receipt.coverage_summary.selected_count == 1

    row = receipt.rows[0]
    assert row.row_source == "yotpo_v3_review"
    assert row.source_native_review_id == "833318480"
    assert row.review_body_word_count == 96
    assert row.review_length_bucket == "75_plus"
    assert row.review_month == "2026-04"
    assert row.verified_purchase_flag is True
    assert row.reviewer_display_label == "Helen"
    assert row.helpful_positive_count == 0
    assert row.helpful_negative_count == 0
    assert row.source_visible_fields["source_widget"] == "yotpo"
    assert row.source_visible_fields["is_incentivized"] is True
    assert row.source_visible_fields["incentive_type"] == "yotpo_loyalty_points"
    assert row.source_visible_fields["reviewer_declared_age_range"] == "25 to 34"


def test_yotpo_v3_preserves_explicit_non_incentivized_state_and_missing_age() -> None:
    widget = json.dumps(
        {
            "pagination": {"page": 1, "perPage": 1, "total": 1},
            "bottomline": {"totalReview": 1, "averageScore": 4.0},
            "reviews": [
                {
                    "id": 833318481,
                    "score": 4,
                    "content": "A source-visible review body.",
                    "createdAt": "2026-04-25T03:03:33",
                    "verifiedBuyer": False,
                    "isIncentivized": False,
                    "incentiveType": None,
                    "customFields": {},
                    "user": {"displayName": "Reader"},
                }
            ],
        }
    )

    receipt = build_fragrance_review_coverage(
        widget_responses=[widget],
        pdp_html=None,
        source_id="fragrance_retail_zgo",
        source_site="ZGO Perfumery",
        product_url=PRODUCT_URL,
        as_of_date=date(2026, 6, 29),
    )

    row = receipt.rows[0]
    assert row.source_visible_fields["is_incentivized"] is False
    assert "incentive_type" not in row.source_visible_fields
    assert "reviewer_declared_age_range" not in row.source_visible_fields


def test_residuals_cover_media_and_aggregate_disagreements() -> None:
    widget = json.dumps(
        {
            "total_count": 1,
            "reviews": [
                {"id": "no-media-four", "rating": 4, "created_at": "2026-05-01", "body": _words("plain", 42)}
            ],
        }
    )
    aggregate = {
        "@context": "https://schema.org",
        "@type": "Product",
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": 4.2, "reviewCount": 2},
    }
    pdp_html = (
        '<script type="application/ld+json">{bad json</script>'
        f'<script type="application/ld+json">{json.dumps(aggregate)}</script>'
    )

    receipt = build_fragrance_review_coverage(
        widget_responses=[widget],
        pdp_html=pdp_html,
        source_id="fragrance_retail_luckyscent",
        source_site="Luckyscent / Scent Bar",
        product_url=PRODUCT_URL,
        as_of_date=date(2026, 6, 29),
        source_media_filter_count=1,
    )

    assert "media_filter_row_scan_mismatch" in receipt.residuals
    assert "aggregate_review_count_widget_total_count_mismatch" in receipt.residuals
    assert "json_ld_parse_error" in receipt.aggregate_companion.residuals


def test_fragrance_review_coverage_runner_writes_json(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    widget_path = tmp_path / "widget.json"
    pdp_path = tmp_path / "pdp.html"
    output_path = tmp_path / "coverage.json"
    widget_path.write_text(_widget_response(), encoding="utf-8")
    pdp_path.write_text(_pdp_html(), encoding="utf-8")

    assert (
        coverage_runner.main(
            [
                "--widget-response",
                str(widget_path),
                "--pdp-html",
                str(pdp_path),
                "--product-url",
                PRODUCT_URL,
                "--output",
                str(output_path),
                "--as-of-date",
                "2026-06-29",
                "--source-media-filter-count",
                "0",
                "--widget-route-param",
                "shop_domain=lucky-scent-site.myshopify.com",
            ]
        )
        == 0
    )

    assert capsys.readouterr().out.strip() == str(output_path)
    written = json.loads(output_path.read_text(encoding="utf-8"))
    assert written["coverage_method"] == "fragrance_review_focused_coverage"
    assert written["coverage_summary"]["selected_count"] == 5
    assert written["aggregate_companion"]["rating_value"] == 3.71
    assert written["aggregate_companion"]["review_count"] == 8
    assert written["widget_route"]["shop_domain"] == "lucky-scent-site.myshopify.com"
