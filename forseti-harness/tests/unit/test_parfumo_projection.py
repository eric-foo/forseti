from __future__ import annotations

import json
from pathlib import Path

import pytest

from runners.run_parfumo_mgt_capture import (
    TARGETED_RENDERED_SLOT,
    TARGETED_RENDERED_SURFACE,
    run_parfumo_targeted_rendered_capture,
)
from runners.run_parfumo_projection import main as projection_main
from source_capture.models import known_fact
from source_capture.parfumo_projection import (
    PARFUMO_PROJECTION_CERTIFICATION,
    PARFUMO_TARGETED_PARSER_VERSION,
    build_parfumo_projection,
    build_parfumo_projection_from_packet_directory,
    build_parfumo_targeted_content_record,
)
from source_capture.writer import write_local_source_capture_packet


_LOCATOR = "https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum"


def test_builds_parfumo_projection_from_direct_http_packet(tmp_path: Path) -> None:
    result = _write_packet(tmp_path)
    projection = build_parfumo_projection(
        packet=result.packet,
        raw_file_bytes_by_file_id=_raw_file_bytes(result.output_directory),
    )

    assert projection.certification == PARFUMO_PROJECTION_CERTIFICATION
    assert "not_cleaned" in projection.certification
    assert "not_judgment_ready" in projection.certification
    assert projection.loss_ledger.preserved_review_cards == 1
    assert projection.loss_ledger.preserved_statements == 1
    assert projection.loss_ledger.full_review_corpus_captured is False
    assert projection.loss_ledger.full_statement_corpus_captured is False
    assert "full_review_corpus_not_captured_ajax_pagination_present" in projection.residuals
    assert "full_statement_corpus_not_captured_ajax_pagination_present" in projection.residuals

    product = next(row for row in projection.rows if row.row_kind == "fragrance_product_snapshot")
    assert product.source_visible_fields["source_object_site_id"] == "67720"
    assert product.source_visible_fields["source_object_name"] == "Baccarat Rouge 540 Eau de Parfum"
    assert product.source_visible_fields["brand_or_house"] == "Maison Francis Kurkdjian"

    aggregate = next(row for row in projection.rows if row.row_kind == "fragrance_aggregate_rating")
    assert aggregate.source_visible_fields["rating_count"] == 5176
    assert aggregate.source_visible_fields["declared_reviews"] == 369
    assert aggregate.source_visible_fields["declared_statements"] == 1390
    assert aggregate.source_visible_fields["scent_rating"] == 7.7

    review = next(row for row in projection.rows if row.row_kind == "fragrance_review_card_current_window")
    assert review.source_visible_fields["review_text"] == "This perfume died young."
    assert review.source_visible_fields["author_display_name"] == "Rimazy"
    assert review.raw_anchor.anchor_kind == "html_selector"

    statement = next(row for row in projection.rows if row.row_kind == "fragrance_statement_current_window")
    assert statement.source_visible_fields["statement_text"] == "Airy amber trail."


def test_builds_parfumo_projection_from_targeted_rendered_packet_without_slice_duplication(
    tmp_path: Path,
) -> None:
    packet_dir = _write_targeted_packet(tmp_path, html=_TARGETED_HTML)

    projection = build_parfumo_projection_from_packet_directory(packet_or_manifest_path=packet_dir)

    assert projection.loss_ledger.preserved_review_cards == 3
    assert projection.loss_ledger.preserved_statements == 1
    assert projection.loss_ledger.preserved_review_tabs == 0
    assert {row.raw_ref.slice_id for row in projection.rows} == {
        "parfumo_targeted:product_context",
        "parfumo_targeted:review_latest_recent",
        "parfumo_targeted:review_source_visible_high_rating",
        "parfumo_targeted:review_source_visible_low_rating",
        "parfumo_targeted:statement_latest_recent",
    }

    product_rows = [
        row for row in projection.rows if row.raw_ref.slice_id == "parfumo_targeted:product_context"
    ]
    assert {row.row_kind for row in product_rows} == {
        "fragrance_product_snapshot",
        "fragrance_aggregate_rating",
        "fragrance_performance_component",
        "fragrance_review_archive_gate",
    }
    assert not any(
        row.row_kind == "fragrance_product_snapshot"
        for row in projection.rows
        if row.raw_ref.slice_id != "parfumo_targeted:product_context"
    )

    review_rows_by_slice = {
        row.raw_ref.slice_id: row
        for row in projection.rows
        if row.row_kind == "fragrance_review_card_current_window"
    }
    assert set(review_rows_by_slice) == {
        "parfumo_targeted:review_latest_recent",
        "parfumo_targeted:review_source_visible_high_rating",
        "parfumo_targeted:review_source_visible_low_rating",
    }
    assert review_rows_by_slice[
        "parfumo_targeted:review_latest_recent"
    ].source_visible_fields["review_id"] == "latest-001"
    assert review_rows_by_slice[
        "parfumo_targeted:review_source_visible_high_rating"
    ].source_visible_fields["rating"] == 9.0
    assert review_rows_by_slice[
        "parfumo_targeted:review_source_visible_low_rating"
    ].source_visible_fields["rating"] == 3.0

    statement = next(
        row for row in projection.rows if row.row_kind == "fragrance_statement_current_window"
    )
    assert statement.raw_ref.slice_id == "parfumo_targeted:statement_latest_recent"
    assert statement.source_visible_fields["statement_text"] == "Airy amber trail."
    assert all(row.raw_anchor.anchor_kind == "json_pointer" for row in projection.rows)
    assert all(row.raw_anchor.json_pointer for row in projection.rows)
    assert all(row.raw_anchor.relative_packet_path.endswith("content_record.json") for row in projection.rows)


def test_targeted_content_record_is_deterministic_and_packet_unbound() -> None:
    first = build_parfumo_targeted_content_record(
        rendered_dom=_TARGETED_HTML.encode("utf-8"),
        visible_text=b"Baccarat Rouge 540\nReviews 369\nStatements 1390\n",
        source_url=_LOCATOR,
    )
    second = build_parfumo_targeted_content_record(
        rendered_dom=_TARGETED_HTML.encode("utf-8"),
        visible_text=b"Baccarat Rouge 540\nReviews 369\nStatements 1390\n",
        source_url=_LOCATOR,
    )

    assert first == second
    assert first["parser_version"] == PARFUMO_TARGETED_PARSER_VERSION
    assert first["rows"]
    assert {row["slice_id"] for row in first["rows"]} == {
        "parfumo_targeted:product_context",
        "parfumo_targeted:review_latest_recent",
        "parfumo_targeted:review_source_visible_high_rating",
        "parfumo_targeted:review_source_visible_low_rating",
        "parfumo_targeted:statement_latest_recent",
    }
    assert all("raw_ref" not in row and "raw_anchor" not in row for row in first["rows"])
    assert "packet_id" not in json.dumps(first, sort_keys=True)


def test_targeted_projection_parses_live_rendered_parfumo_cards(tmp_path: Path) -> None:
    packet_dir = _write_targeted_packet(tmp_path, html=_LIVE_RENDERED_HTML)

    projection = build_parfumo_projection_from_packet_directory(packet_or_manifest_path=packet_dir)

    assert projection.loss_ledger.preserved_review_cards == 1
    assert projection.loss_ledger.preserved_statements == 1

    review = next(row for row in projection.rows if row.row_kind == "fragrance_review_card_current_window")
    assert review.raw_ref.slice_id == "parfumo_targeted:review_source_visible_high_rating"
    assert review.source_visible_fields["review_id"] == "258984"
    assert review.source_visible_fields["author_display_name"] == "NoirAlethea"
    assert review.source_visible_fields["date_published"] == "2023-06-26"
    assert review.source_visible_fields["date_display_text"] == "06/26/2023"
    assert review.source_visible_fields["rating"] == 10.0
    assert review.source_visible_fields["tab_label"] == "Positive"
    assert review.source_visible_fields["review_text"] == (
        "Due to the way BR540 makes me feel, I can only imagine black magic."
    )
    assert review.source_visible_fields["source_item_url"].endswith("/reviews/258984")

    statement = next(
        row for row in projection.rows if row.row_kind == "fragrance_statement_current_window"
    )
    assert statement.raw_ref.slice_id == "parfumo_targeted:statement_latest_recent"
    assert statement.source_visible_fields["statement_id"] == "2397523"
    assert statement.source_visible_fields["author_display_name"] == "Ceesie"
    assert statement.source_visible_fields["date_published"] is None
    assert statement.source_visible_fields["date_display_text"] == "6 months ago"
    assert statement.source_visible_fields["rating"] == 4.0
    assert statement.source_visible_fields["statement_text"] == (
        "It just does not add up in my mind. It is a scrubber for me."
    )
    assert statement.source_visible_fields["source_item_url"].endswith("/statements/2397523")


def test_targeted_projection_residualizes_rating_buckets_without_source_visible_rating(
    tmp_path: Path,
) -> None:
    packet_dir = _write_targeted_packet(tmp_path, html=_TARGETED_HTML_WITHOUT_RATING_BUCKETS)

    projection = build_parfumo_projection_from_packet_directory(packet_or_manifest_path=packet_dir)

    assert "parfumo_high_rating_review_bucket_absent_or_unexposed" in projection.residuals
    assert "parfumo_low_rating_review_bucket_absent_or_unexposed" in projection.residuals
    assert any(
        row.raw_ref.slice_id == "parfumo_targeted:review_latest_recent"
        and row.row_kind == "fragrance_review_card_current_window"
        for row in projection.rows
    )


def test_targeted_projection_partitions_overlapping_review_views_without_loss(
    tmp_path: Path,
) -> None:
    packet_dir = _write_targeted_packet(tmp_path, html=_TARGETED_HTML_OVERLAP_AND_MID_BUCKET)

    projection = build_parfumo_projection_from_packet_directory(packet_or_manifest_path=packet_dir)

    review_ids_by_slice: dict[str, list[str]] = {}
    for row in projection.rows:
        if row.row_kind != "fragrance_review_card_current_window":
            continue
        review_ids_by_slice.setdefault(row.raw_ref.slice_id, []).append(
            row.source_visible_fields["review_id"]
        )

    assert projection.loss_ledger.preserved_review_cards == 3
    assert review_ids_by_slice == {
        "parfumo_targeted:review_latest_recent": ["dup-001"],
        "parfumo_targeted:review_source_visible_high_rating": ["loss-001"],
        "parfumo_targeted:review_source_visible_low_rating": ["low-001"],
    }
    review_ids = [item for values in review_ids_by_slice.values() for item in values]
    assert len(review_ids) == len(set(review_ids))
    assert "parfumo_high_rating_review_bucket_absent_or_unexposed" not in projection.residuals
    assert "parfumo_low_rating_review_bucket_absent_or_unexposed" not in projection.residuals


def test_targeted_projection_bucket_token_matching_is_segment_bounded(tmp_path: Path) -> None:
    packet_dir = _write_targeted_packet(tmp_path, html=_TARGETED_HTML_SEGMENT_BOUNDARY)

    projection = build_parfumo_projection_from_packet_directory(packet_or_manifest_path=packet_dir)

    review_rows = [
        row for row in projection.rows if row.row_kind == "fragrance_review_card_current_window"
    ]
    assert [(row.raw_ref.slice_id, row.source_visible_fields["review_id"]) for row in review_rows] == [
        ("parfumo_targeted:review_latest_recent", "flower-001")
    ]
    assert "parfumo_low_rating_review_bucket_absent_or_unexposed" in projection.residuals


def test_parfumo_projection_ignores_unrelated_ids_when_attributing_review_tab(tmp_path: Path) -> None:
    html = _HTML.replace(
        '    <article data-review-id="900001"',
        '    <aside id="sidebar">not a review tab panel</aside>\n    <article data-review-id="900001"',
    )
    result = _write_packet(tmp_path, html=html)
    projection = build_parfumo_projection(
        packet=result.packet,
        raw_file_bytes_by_file_id=_raw_file_bytes(result.output_directory),
    )

    review = next(row for row in projection.rows if row.row_kind == "fragrance_review_card_current_window")
    assert review.tab_id == "reviews"
    assert review.source_visible_fields["tab_id"] == "reviews"


def test_parfumo_projection_rejects_wrong_surface(tmp_path: Path) -> None:
    result = _write_packet(tmp_path, source_surface="fragrantica_product_page_direct_http")
    with pytest.raises(ValueError, match="source_surface"):
        build_parfumo_projection(
            packet=result.packet,
            raw_file_bytes_by_file_id=_raw_file_bytes(result.output_directory),
        )


def test_parfumo_projection_requires_preserved_file_bytes(tmp_path: Path) -> None:
    result = _write_packet(tmp_path)
    with pytest.raises(ValueError, match="raw bytes are required"):
        build_parfumo_projection(packet=result.packet, raw_file_bytes_by_file_id={})


def test_parfumo_projection_runner_writes_output(tmp_path: Path) -> None:
    result = _write_packet(tmp_path)
    output_path = tmp_path / "projection.json"

    exit_code = projection_main(["--packet", result.output_directory, "--output", str(output_path)])

    assert exit_code == 0
    written = json.loads(output_path.read_text(encoding="utf-8"))
    assert written["projection_method"] == "parfumo_current_window_mechanical_projection"
    assert written["loss_ledger"]["preserved_review_cards"] == 1


def test_builds_parfumo_projection_from_packet_directory(tmp_path: Path) -> None:
    result = _write_packet(tmp_path)

    projection = build_parfumo_projection_from_packet_directory(
        packet_or_manifest_path=Path(result.output_directory)
    )

    assert projection.packet_id == result.packet.packet_id
    assert projection.loss_ledger.preserved_statements == 1


def _write_targeted_packet(tmp_path: Path, *, html: str) -> Path:
    artifact_dir = tmp_path / "targeted_artifacts"
    artifact_dir.mkdir(parents=True)
    rendered_dom = artifact_dir / "rendered_dom.html"
    visible_text = artifact_dir / "visible_text.txt"
    route_receipt = artifact_dir / "route_receipt.json"
    screenshot = artifact_dir / "viewport.png"
    rendered_dom.write_text(html, encoding="utf-8")
    visible_text.write_text(
        "Baccarat Rouge 540 Eau de Parfum\nReviews 369\nStatements 1390\n",
        encoding="utf-8",
    )
    route_receipt.write_text(
        json.dumps(
            {
                "route": "chrome_extension_user_visible_rendered_session",
                "source_surface": TARGETED_RENDERED_SURFACE,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    screenshot.write_bytes(b"png fixture bytes")

    exit_code, message = run_parfumo_targeted_rendered_capture(
        url=_LOCATOR,
        output_root=tmp_path / "targeted_out",
        rendered_dom_path=rendered_dom,
        visible_text_path=visible_text,
        route_receipt_path=route_receipt,
        screenshot_path=screenshot,
    )
    assert exit_code == 0
    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    assert summary["packet_roles"][TARGETED_RENDERED_SLOT]["source_surface"] == (
        TARGETED_RENDERED_SURFACE
    )
    return Path(summary["packet_roles"][TARGETED_RENDERED_SLOT]["packet_path"])


def _write_packet(
    tmp_path: Path,
    *,
    source_surface: str = "parfumo_product_page_direct_http",
    html: str | None = None,
):
    body_path = tmp_path / "http_response_body.bin"
    body_path.write_text(_HTML if html is None else html, encoding="utf-8")
    metadata_path = tmp_path / "http_response_metadata.json"
    metadata_path.write_text('{"status": 200}\n', encoding="utf-8")
    return write_local_source_capture_packet(
        output_directory=tmp_path / "packet",
        input_files=[body_path, metadata_path],
        source_family="fragrance_native_database",
        source_surface=source_surface,
        source_locator=known_fact(_LOCATOR),
        decision_question="test Parfumo projection",
        capture_context="parfumo projection unit fixture",
    )


def _raw_file_bytes(packet_dir: str) -> dict[str, bytes]:
    manifest = json.loads((Path(packet_dir) / "manifest.json").read_text(encoding="utf-8"))
    return {
        item["file_id"]: (Path(packet_dir) / item["relative_packet_path"]).read_bytes()
        for item in manifest["preserved_files"]
    }


_HTML = """
<html><head>
  <link rel="canonical" href="https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum"/>
  <meta name="description" content="Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian"/>
  <title>Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian (Eau de Parfum) & Perfume Facts</title>
</head><body>
  <main data-perfume-id="67720" data-rating-count="5176" data-review-count="369"
        data-statement-count="1390" data-scent-rating="7.7" data-longevity-rating="8.7"
        data-sillage-rating="8.5">
    <button data-tab="reviews" data-active="true">Reviews <span>369</span></button>
    <button data-tab="statements">Statements <span>1390</span></button>
    <input type="hidden" name="h" value="7536fa6f9c01a6637a935e7717b53101">
    <script>
      const routes = {
        reviews: "/action/perfume/get_reviews.php",
        statements: "/action/perfume/get_statements.php",
        p_id: 67720,
        h: "7536fa6f9c01a6637a935e7717b53101"
      };
    </script>
    <article data-review-id="900001" data-author="Rimazy" data-rating="8.0">
      <time datetime="2026-06-25">06/25/26</time>
      <p data-role="review-text">This perfume died young.</p>
      <a href="/Users/rimazy">Read review</a>
    </article>
    <article data-statement-id="st7001" data-author="Lyra">
      <time datetime="2026-06-24">06/24/26</time>
      <p data-role="statement-text">Airy amber trail.</p>
    </article>
  </main>
</body></html>
"""


_TARGETED_HTML = f"""
<html><head>
  <link rel="canonical" href="{_LOCATOR}"/>
  <meta name="description" content="Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian"/>
  <title>Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian (Eau de Parfum) & Perfume Facts</title>
</head><body>
  <main data-perfume-id="67720" data-rating-count="5176" data-review-count="369"
        data-statement-count="1390" data-scent-rating="7.7" data-longevity-rating="8.7"
        data-sillage-rating="8.5">
    <script>const routes = {{reviews: "/action/perfume/get_reviews.php", statements: "/action/perfume/get_statements.php", p_id: 67720}};</script>
    <article data-review-id="latest-001" data-author="Rimazy" data-rating="7.0" data-tab="latest">
      <time datetime="2026-06-25">06/25/26</time>
      <p data-role="review-text">This perfume died young.</p>
    </article>
    <article data-review-id="high-001" data-author="Sol" data-rating="9.0" data-tab="high_rating">
      <time datetime="2026-06-23">06/23/26</time>
      <p data-role="review-text">Glowing amber for hours.</p>
    </article>
    <article data-review-id="low-001" data-author="Noir" data-rating="3.0" data-tab="low_rating">
      <time datetime="2026-06-20">06/20/26</time>
      <p data-role="review-text">Too sharp on my skin.</p>
    </article>
    <article data-statement-id="st7001" data-author="Lyra" data-tab="statements">
      <time datetime="2026-06-24">06/24/26</time>
      <p data-role="statement-text">Airy amber trail.</p>
    </article>
  </main>
</body></html>
"""

_LIVE_RENDERED_HTML = f"""
<html><head>
  <link rel="canonical" href="{_LOCATOR}"/>
  <title>Baccarat Rouge 540 by Maison Francis Kurkdjian (Eau de Parfum) & Perfume Facts</title>
</head><body>
  <main data-perfume-id="67720" data-rating-count="5179" data-review-count="369"
        data-statement-count="1390">
    <div id="reviews_holder">
      <nav class="flex ptabs">
        <div class="action_reviews_order" data-o="order_date_desc"><span>Latest</span></div>
        <div class="active action_reviews_order" data-o="order_scent_desc"><span>Positive</span></div>
        <div class="action_reviews_order" data-o="order_scent_asc"><span>Negative</span></div>
      </nav>
      <article class="review review_article_258984 rounded" itemprop="review" itemscope="" itemtype="https://schema.org/Review">
        <div class="review_header flex" id="review_258984">
          <div class="text-sm lightgrey grey" itemprop="datePublished" content="2023-06-26">06/26/2023</div>
          <a href="https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum/reviews/258984">
            <span itemprop="reviewRating" itemscope="" itemtype="https://schema.org/Rating">
              <meta itemprop="ratingValue" content="10">
              <span class="nr blue">10</span>Scent
            </span>
          </a>
        </div>
        <span itemprop="author" itemscope="" itemtype="https://schema.org/Person"><span itemprop="name">NoirAlethea</span></span>
        <div itemprop="reviewBody">
          <div class="leading-7" id="r_text_258984">Due to the way BR540 makes me feel, I can only imagine black magic.</div>
        </div>
      </article>
    </div>
    <div id="statements_holder">
      <div class="statement-bubble">
        <div class="statement-top-left">
          <div class="nowrap"><a href="https://www.parfumo.com/Users/Ceesie/statements">Ceesie</a></div>
          <div class="text-xs lightblue2">6 months ago</div>
        </div>
        <a href="https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum/statements/2397523">
          <span class="nr blue">4</span>Scent
          <span class="nr red">9</span>Longevity
          <span class="nr purple">6</span>Sillage
        </a>
        <div id="s_text_content_2397523">It just does not add up in my mind. It is a scrubber for me.</div>
      </div>
    </div>
  </main>
</body></html>
"""

_TARGETED_HTML_OVERLAP_AND_MID_BUCKET = f"""
<html><head>
  <link rel="canonical" href="{_LOCATOR}"/>
  <title>Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian (Eau de Parfum) & Perfume Facts</title>
</head><body>
  <main data-perfume-id="67720" data-review-count="369" data-statement-count="1390">
    <article data-review-id="dup-001" data-author="Rimazy" data-rating="9.0">
      <time datetime="2026-06-25">06/25/26</time>
      <p data-role="review-text">High rating but latest source view.</p>
    </article>
    <article data-review-id="loss-001" data-author="Sol" data-rating="7.5" data-tab="high_rating">
      <time datetime="2026-06-23">06/23/26</time>
      <p data-role="review-text">Source-visible high bucket but mid numeric rating.</p>
    </article>
    <article data-review-id="low-001" data-author="Noir" data-rating="3.0" data-tab="low_rating">
      <time datetime="2026-06-20">06/20/26</time>
      <p data-role="review-text">Low source-visible bucket.</p>
    </article>
    <article data-statement-id="st7001" data-author="Lyra" data-tab="statements">
      <time datetime="2026-06-24">06/24/26</time>
      <p data-role="statement-text">Airy amber trail.</p>
    </article>
  </main>
</body></html>
"""


_TARGETED_HTML_SEGMENT_BOUNDARY = f"""
<html><head>
  <link rel="canonical" href="{_LOCATOR}"/>
  <title>Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian (Eau de Parfum) & Perfume Facts</title>
</head><body>
  <main data-perfume-id="67720" data-review-count="369" data-statement-count="1390">
    <article data-review-id="flower-001" data-author="Iris" data-rating="7.5" data-tab="flower">
      <time datetime="2026-06-25">06/25/26</time>
      <p data-role="review-text">The word flower contains low as a substring.</p>
    </article>
  </main>
</body></html>
"""


_TARGETED_HTML_WITHOUT_RATING_BUCKETS = f"""
<html><head>
  <link rel="canonical" href="{_LOCATOR}"/>
  <title>Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian (Eau de Parfum) & Perfume Facts</title>
</head><body>
  <main data-perfume-id="67720" data-review-count="369" data-statement-count="1390">
    <article data-review-id="latest-001" data-author="Rimazy" data-tab="latest">
      <time datetime="2026-06-25">06/25/26</time>
      <p data-role="review-text">This perfume died young.</p>
    </article>
    <article data-statement-id="st7001" data-author="Lyra" data-tab="statements">
      <time datetime="2026-06-24">06/24/26</time>
      <p data-role="statement-text">Airy amber trail.</p>
    </article>
  </main>
</body></html>
"""
