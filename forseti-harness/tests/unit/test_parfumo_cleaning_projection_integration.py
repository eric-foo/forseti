from __future__ import annotations

import json
from pathlib import Path

from cleaning.parfumo import PARFUMO_RATING_CARRY_RULE, build_parfumo_cleaning_packet
from runners.run_parfumo_mgt_capture import (
    TARGETED_RENDERED_SLOT,
    TARGETED_RENDERED_SURFACE,
    run_parfumo_targeted_rendered_capture,
)
from source_capture.models import known_fact
from source_capture.parfumo_projection import (
    build_parfumo_projection,
    build_parfumo_projection_from_packet_directory,
)
from source_capture.writer import write_local_source_capture_packet


_LOCATOR = "https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum"
_HTML = """
<html><head>
  <link rel="canonical" href="https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum"/>
  <title>Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian (Eau de Parfum) & Perfume Facts</title>
</head><body>
  <main data-perfume-id="67720" data-rating-count="5176" data-review-count="369" data-statement-count="1390">
    <script>const routes = {reviews: "/action/perfume/get_reviews.php", statements: "/action/perfume/get_statements.php", p_id: 67720};</script>
    <article data-review-id="900001" data-author="  Rimazy  " data-rating="8.0">
      <time datetime="2026-06-25">06/25/26</time>
      <p data-role="review-text">This   perfume
      died young.</p>
    </article>
    <article data-statement-id="st7001" data-author="Lyra">
      <time datetime="2026-06-24">06/24/26</time>
      <p data-role="statement-text">Airy   amber trail.</p>
    </article>
  </main>
</body></html>
"""


def test_parfumo_projection_builds_cleaning_packet_with_text_transforms(tmp_path: Path) -> None:
    projection = _projection(tmp_path)

    cleaning_packet = build_parfumo_cleaning_packet(projection)

    assert len(cleaning_packet.handles) == len(projection.rows)
    assert all(handle.ecr_ref is not None for handle in cleaning_packet.handles)
    assert {
        "inspect_raw_before_review_corpus_completeness_claim",
        "inspect_raw_before_statement_corpus_completeness_claim",
    }.issubset(
        {
            trigger
            for handle in cleaning_packet.handles
            for trigger in handle.raw_pull_triggers
        }
    )

    rules = [entry.transform.method_or_rule for entry in cleaning_packet.transform_ledger]
    assert rules.count("parfumo_text_whitespace_normalization") == 2
    assert "parfumo_author_display_name_whitespace_normalization" in rules
    assert "parfumo_text_length_bin" in rules
    assert PARFUMO_RATING_CARRY_RULE in rules

    rating_entries = [
        entry
        for entry in cleaning_packet.transform_ledger
        if entry.transform.method_or_rule == PARFUMO_RATING_CARRY_RULE
    ]
    assert len(rating_entries) == 1
    assert json.loads(rating_entries[0].transform.transformed_value) == {"rating": 8.0}

    text_values = {
        entry.transform.transformed_value
        for entry in cleaning_packet.transform_ledger
        if entry.transform.method_or_rule == "parfumo_text_whitespace_normalization"
    }
    assert text_values == {"This perfume died young.", "Airy amber trail."}


def test_targeted_content_and_raw_packets_produce_equivalent_cleaning_transforms(
    tmp_path: Path,
) -> None:
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()
    rendered_dom = artifacts / "rendered_dom.html"
    visible_text = artifacts / "visible_text.txt"
    route_receipt = artifacts / "route_receipt.json"
    screenshot = artifacts / "viewport.png"
    rendered_dom.write_text(_HTML, encoding="utf-8")
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

    packet_dirs: dict[str, Path] = {}
    for mode in ("raw", "content"):
        exit_code, message = run_parfumo_targeted_rendered_capture(
            url=_LOCATOR,
            output_root=tmp_path / mode,
            rendered_dom_path=rendered_dom,
            visible_text_path=visible_text,
            route_receipt_path=route_receipt,
            screenshot_path=screenshot,
            capture_artifact_mode=mode,
        )
        assert exit_code == 0
        summary = json.loads(Path(message).read_text(encoding="utf-8"))
        packet_dirs[mode] = Path(
            summary["packet_roles"][TARGETED_RENDERED_SLOT]["packet_path"]
        )

    projections = {
        mode: build_parfumo_projection_from_packet_directory(
            packet_or_manifest_path=packet_dir
        )
        for mode, packet_dir in packet_dirs.items()
    }
    semantic_rows = {
        mode: [
            row.model_dump(mode="json", exclude={"raw_ref", "raw_anchor"})
            for row in projection.rows
        ]
        for mode, projection in projections.items()
    }
    assert semantic_rows["content"] == semantic_rows["raw"]

    cleaning_packets = {
        mode: build_parfumo_cleaning_packet(
            projection,
            source_surface=TARGETED_RENDERED_SURFACE,
        )
        for mode, projection in projections.items()
    }
    assert (
        cleaning_packets["content"].transform_ledger
        == cleaning_packets["raw"].transform_ledger
    )


def _projection(tmp_path: Path):
    body_path = tmp_path / "http_response_body.bin"
    body_path.write_text(_HTML, encoding="utf-8")
    metadata_path = tmp_path / "http_response_metadata.json"
    metadata_path.write_text('{"status": 200}\n', encoding="utf-8")
    result = write_local_source_capture_packet(
        output_directory=tmp_path / "packet",
        input_files=[body_path, metadata_path],
        source_family="fragrance_native_database",
        source_surface="parfumo_product_page_direct_http",
        source_locator=known_fact(_LOCATOR),
        decision_question="test Parfumo Cleaning projection integration",
        capture_context="parfumo cleaning projection unit fixture",
    )
    manifest = json.loads((Path(result.output_directory) / "manifest.json").read_text(encoding="utf-8"))
    bodies = {
        item["file_id"]: (Path(result.output_directory) / item["relative_packet_path"]).read_bytes()
        for item in manifest["preserved_files"]
    }
    return build_parfumo_projection(packet=result.packet, raw_file_bytes_by_file_id=bodies)
