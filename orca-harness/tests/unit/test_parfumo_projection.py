from __future__ import annotations

import json
from pathlib import Path

import pytest

from runners.run_parfumo_projection import main as projection_main
from source_capture.models import known_fact
from source_capture.parfumo_projection import (
    PARFUMO_PROJECTION_CERTIFICATION,
    build_parfumo_projection,
    build_parfumo_projection_from_packet_directory,
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


def _write_packet(tmp_path: Path, *, source_surface: str = "parfumo_product_page_direct_http"):
    body_path = tmp_path / "http_response_body.bin"
    body_path.write_text(_HTML, encoding="utf-8")
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
