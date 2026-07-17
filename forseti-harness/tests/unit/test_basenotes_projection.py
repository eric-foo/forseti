from __future__ import annotations

import json
from pathlib import Path

import pytest

from runners.run_basenotes_projection import main as projection_main
from source_capture.models import known_fact
from source_capture.basenotes_projection import (
    BASENOTES_CONTENT_RECORD_KIND,
    BASENOTES_CONTENT_SCHEMA_VERSION,
    BASENOTES_PARSER_VERSION,
    BASENOTES_PROJECTION_CERTIFICATION,
    build_basenotes_content_record,
    build_basenotes_projection,
    build_basenotes_projection_from_packet_directory,
)
from source_capture.writer import write_local_source_capture_packet


_LOCATOR = "https://basenotes.com/fragrances/mojave-ghost-by-byredo.26143979"
_SOURCE_SURFACE = "basenotes_product_page_user_cleared_persistent_chrome_current_window"
_FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "basenotes"
    / "mojave_ghost_product_page.html"
)


def _fixture_html() -> str:
    return _FIXTURE.read_text(encoding="utf-8")


def test_builds_basenotes_projection_from_persistent_chrome_packet(tmp_path: Path) -> None:
    result = _write_packet(tmp_path)
    projection = build_basenotes_projection(
        packet=result.packet,
        raw_file_bytes_by_file_id=_raw_file_bytes(result.output_directory),
    )

    assert projection.certification == BASENOTES_PROJECTION_CERTIFICATION
    assert "not_cleaned" in projection.certification
    assert "not_judgment_ready" in projection.certification
    # The in-page JSON-LD carries the 6-review SUBSET; the declared corpus is 18.
    assert projection.loss_ledger.preserved_review_cards == 6
    assert projection.loss_ledger.preserved_statements == 0
    assert projection.loss_ledger.full_review_corpus_captured is False
    assert "full_review_corpus_not_captured" in projection.residuals

    product = next(row for row in projection.rows if row.row_kind == "fragrance_product_snapshot")
    assert product.source_visible_fields["source_object_site_id"] == "26143979"
    assert product.source_visible_fields["source_object_name"] == "Mojave Ghost"
    assert product.source_visible_fields["brand_or_house"] == "Byredo"
    assert (
        product.source_visible_fields["canonical_url"]
        == "https://basenotes.com/fragrances/mojave-ghost-by-byredo.26143979"
    )
    assert product.source_visible_fields["product_image"] == "https://basenotes.com/img/26143979-602-j"

    review = next(
        row for row in projection.rows if row.row_kind == "fragrance_review_card_current_window"
    )
    assert review.source_visible_fields["author_display_name"] == "Griff"
    assert (
        review.source_visible_fields["review_text"]
        == "Ectoplasmic. A wisp of something and then poof, it's gone. Spooky."
    )
    assert review.source_visible_fields["date_published"] == "2025-11-05T17:09:12+00:00"
    assert review.source_visible_fields["rating"] == 2.0
    assert review.tab_id == "reviews"
    assert review.raw_anchor.anchor_kind == "text_pattern"

    # The br-bearing review body is normalized (entities + <br /> collapsed to spaces).
    mai7 = next(
        row
        for row in projection.rows
        if row.row_kind == "fragrance_review_card_current_window"
        and row.source_visible_fields.get("author_display_name") == "Mai7"
    )
    assert "<br" not in (mai7.source_visible_fields["review_text"] or "")
    assert mai7.source_visible_fields["review_text"].startswith(
        "The thing I like most about Byredo fragrances is their names."
    )


def test_basenotes_projection_prefers_review_bearing_product_jsonld_when_multiple_blocks(
    tmp_path: Path,
) -> None:
    metadata_only_product = (
        '<script type="application/ld+json">'
        '{"@context":"http://schema.org","@type":"Product","name":"Metadata Only",'
        '"brand":{"@type":"Brand","name":"Wrong House"}}'
        '</script>'
    )
    html = _fixture_html().replace(
        '<script type="application/ld+json"> {',
        f'{metadata_only_product}\n<script type="application/ld+json"> {{',
        1,
    )
    result = _write_packet(tmp_path, html=html)

    projection = build_basenotes_projection(
        packet=result.packet,
        raw_file_bytes_by_file_id=_raw_file_bytes(result.output_directory),
    )

    assert projection.loss_ledger.preserved_review_cards == 6
    product = next(row for row in projection.rows if row.row_kind == "fragrance_product_snapshot")
    assert product.source_visible_fields["source_object_name"] == "Mojave Ghost"
    review_texts = {
        row.source_visible_fields["review_text"]
        for row in projection.rows
        if row.row_kind == "fragrance_review_card_current_window"
    }
    assert "Ectoplasmic. A wisp of something and then poof, it's gone. Spooky." in review_texts


def test_basenotes_projection_archive_gate_carries_review_suburl_and_sentiment_tabs(
    tmp_path: Path,
) -> None:
    result = _write_packet(tmp_path)
    projection = build_basenotes_projection(
        packet=result.packet,
        raw_file_bytes_by_file_id=_raw_file_bytes(result.output_directory),
    )

    gate = next(row for row in projection.rows if row.row_kind == "fragrance_review_archive_gate")
    fields = gate.source_visible_fields
    assert fields["corpus_kind"] == "reviews"
    assert fields["endpoint_path"] == "/fragrances/mojave-ghost-by-byredo.26143979/reviews/"
    assert fields["declared_review_count"] == 18
    assert fields["captured_review_subset"] == 6
    assert fields["sentiment_tab_endpoints"] == {
        "positive": "/fragrances/mojave-ghost-by-byredo.26143979/reviews/positive/",
        "neutral": "/fragrances/mojave-ghost-by-byredo.26143979/reviews/neutral/",
        "negative": "/fragrances/mojave-ghost-by-byredo.26143979/reviews/negative/",
    }
    assert "full_review_corpus_not_captured" in gate.residuals


def test_basenotes_projection_aggregate_rating_carries_declared_and_sentiment_counts(
    tmp_path: Path,
) -> None:
    result = _write_packet(tmp_path)
    projection = build_basenotes_projection(
        packet=result.packet,
        raw_file_bytes_by_file_id=_raw_file_bytes(result.output_directory),
    )

    aggregate = next(
        row for row in projection.rows if row.row_kind == "fragrance_aggregate_rating"
    )
    fields = aggregate.source_visible_fields
    assert fields["declared_reviews"] == 18
    assert fields["captured_review_cards"] == 6
    assert fields["positive_review_count"] == 4
    assert fields["neutral_review_count"] == 8
    assert fields["negative_review_count"] == 6


def test_basenotes_projection_rejects_wrong_surface(tmp_path: Path) -> None:
    result = _write_packet(tmp_path, source_surface="parfumo_product_page_direct_http")
    with pytest.raises(ValueError, match="source_surface"):
        build_basenotes_projection(
            packet=result.packet,
            raw_file_bytes_by_file_id=_raw_file_bytes(result.output_directory),
        )


def test_basenotes_projection_requires_preserved_file_bytes(tmp_path: Path) -> None:
    result = _write_packet(tmp_path)
    with pytest.raises(ValueError, match="raw bytes are required"):
        build_basenotes_projection(packet=result.packet, raw_file_bytes_by_file_id={})


def test_basenotes_projection_runner_writes_output(tmp_path: Path) -> None:
    result = _write_packet(tmp_path)
    output_path = tmp_path / "projection.json"

    exit_code = projection_main(["--packet", result.output_directory, "--output", str(output_path)])

    assert exit_code == 0
    written = json.loads(output_path.read_text(encoding="utf-8"))
    assert written["projection_method"] == "basenotes_current_window_mechanical_projection"
    assert written["loss_ledger"]["preserved_review_cards"] == 6


def test_builds_basenotes_projection_from_packet_directory(tmp_path: Path) -> None:
    result = _write_packet(tmp_path)

    projection = build_basenotes_projection_from_packet_directory(
        packet_or_manifest_path=Path(result.output_directory)
    )

    assert projection.packet_id == result.packet.packet_id
    assert projection.loss_ledger.preserved_review_cards == 6


def test_basenotes_content_record_is_deterministic_and_packet_unbound() -> None:
    kwargs = {
        "rendered_dom": _fixture_html().encode("utf-8"),
        "visible_text": b"Mojave Ghost by Byredo\n",
        "source_url": _LOCATOR,
    }

    first = build_basenotes_content_record(**kwargs)
    second = build_basenotes_content_record(**kwargs)

    assert first == second
    assert first["record_kind"] == BASENOTES_CONTENT_RECORD_KIND
    assert first["schema_version"] == BASENOTES_CONTENT_SCHEMA_VERSION
    assert first["parser_version"] == BASENOTES_PARSER_VERSION
    serialized = json.dumps(first, sort_keys=True)
    assert "packet_id" not in serialized
    assert "file_id" not in serialized
    assert "relative_packet_path" not in serialized
    assert "raw_ref" not in serialized


def _write_packet(
    tmp_path: Path,
    *,
    source_surface: str = _SOURCE_SURFACE,
    html: str | None = None,
):
    body_path = tmp_path / "browser_rendered_dom.html"
    body_path.write_text(_fixture_html() if html is None else html, encoding="utf-8")
    metadata_path = tmp_path / "browser_snapshot_metadata.json"
    metadata_path.write_text('{"capture_timestamp": "2026-06-30T00:00:00Z"}\n', encoding="utf-8")
    return write_local_source_capture_packet(
        output_directory=tmp_path / "packet",
        input_files=[body_path, metadata_path],
        source_family="fragrance_native_database",
        source_surface=source_surface,
        source_locator=known_fact(_LOCATOR),
        decision_question="test Basenotes projection",
        capture_context="basenotes projection unit fixture",
    )


def _raw_file_bytes(packet_dir: str) -> dict[str, bytes]:
    manifest = json.loads((Path(packet_dir) / "manifest.json").read_text(encoding="utf-8"))
    return {
        item["file_id"]: (Path(packet_dir) / item["relative_packet_path"]).read_bytes()
        for item in manifest["preserved_files"]
    }
