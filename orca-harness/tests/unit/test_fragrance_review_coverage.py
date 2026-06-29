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
