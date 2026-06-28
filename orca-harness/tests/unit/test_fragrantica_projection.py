from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from runners import run_fragrantica_projection
from source_capture.fragrantica_projection import (
    FRAGRANTICA_PROJECTION_CERTIFICATION,
    FRAGRANTICA_PROJECTION_METHOD,
    build_fragrantica_projection,
    build_fragrantica_projection_from_packet_directory,
)
from source_capture.models import (
    CaptureModeCategory,
    PacketTiming,
    PreservedFile,
    ReceiptMetadata,
    SourceCapturePacket,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)


def test_fragrantica_projection_preserves_current_window_reviews_and_residuals() -> None:
    packet, raw = _packet()

    projection = build_fragrantica_projection(packet=packet, raw_file_bytes_by_file_id=raw)

    assert projection.packet_id == "pkt-fragrantica"
    assert projection.projection_method == FRAGRANTICA_PROJECTION_METHOD
    assert projection.loss_ledger.preserved_review_cards == 3
    assert projection.loss_ledger.preserved_review_tabs == 4
    assert projection.loss_ledger.review_card_counts_by_tab == {
        "all-reviews": 2,
        "popular-positive-reviews": 1,
    }
    assert projection.loss_ledger.full_archive_captured is False
    assert "full_review_archive_not_captured_login_prompt_present" in projection.residuals
    assert "search_review_rows_not_embedded_in_direct_http_body" in projection.residuals

    product = _single_row(projection.rows, "fragrance_product_snapshot")
    assert product.source_object_site_id == "33519"
    assert product.source_object_name == "Baccarat Rouge 540"
    assert product.brand_or_house == "Maison Francis Kurkdjian"
    assert product.source_visible_fields["launched_year"] == 2015

    aggregate = _single_row(projection.rows, "fragrance_aggregate_rating")
    assert aggregate.source_visible_fields["rating_value"] == 3.76
    assert aggregate.source_visible_fields["rating_count"] == 28808
    assert aggregate.source_visible_fields["displayed_review_count"] == "3.9K"
    assert aggregate.source_visible_fields["displayed_review_count_approx_value"] == 3900

    review = next(row for row in projection.rows if row.comment_id == "3090334")
    assert review.row_kind == "fragrance_review_card_current_window"
    assert review.tab_id == "all-reviews"
    assert review.raw_anchor.anchor_kind == "html_selector"
    assert review.raw_anchor.anchor_value == "#parent3090334"
    assert review.source_visible_fields["author_display_name"] == "Rimazy"
    assert review.source_visible_fields["date_published"] == "2026-06-25"
    assert review.source_visible_fields["review_text"] == "This perfume died young."
    assert review.source_visible_fields["rating"] == 5
    assert review.source_visible_fields["relation"] == "have"
    assert review.source_visible_fields["share_path"].endswith("?ccid=3090334#focus-zone")

    assert len(projection.binding_map) == 3
    assert projection.binding_map[0].binding_type == "review_votes_to_review_text"


def test_fragrantica_projection_rejects_wrong_source_family() -> None:
    packet, raw = _packet(source_family="web_page")

    with pytest.raises(ValueError, match="source_family='fragrance_native_database'"):
        build_fragrantica_projection(packet=packet, raw_file_bytes_by_file_id=raw)


def test_fragrantica_projection_requires_raw_bytes() -> None:
    packet, raw = _packet()
    raw.pop("file_01")

    with pytest.raises(ValueError, match="file_01"):
        build_fragrantica_projection(packet=packet, raw_file_bytes_by_file_id=raw)


def test_fragrantica_projection_builds_from_existing_packet_directory(tmp_path: Path) -> None:
    packet, raw = _packet()
    packet_dir = _write_packet_dir(tmp_path, packet=packet, raw=raw)

    projection = build_fragrantica_projection_from_packet_directory(
        packet_or_manifest_path=packet_dir,
    )

    assert projection.packet_id == "pkt-fragrantica"
    assert projection.loss_ledger.preserved_review_cards == 3


def test_fragrantica_projection_runner_writes_existing_packet_projection(tmp_path: Path, capsys) -> None:
    packet, raw = _packet()
    packet_dir = _write_packet_dir(tmp_path, packet=packet, raw=raw)
    output_path = tmp_path / "projection" / "fragrantica_projection.json"

    result = run_fragrantica_projection.main(
        ["--packet", str(packet_dir / "manifest.json"), "--output", str(output_path)]
    )

    assert result == 0
    assert capsys.readouterr().out.strip() == str(output_path)
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["projection_method"] == FRAGRANTICA_PROJECTION_METHOD
    assert payload["certification"] == FRAGRANTICA_PROJECTION_CERTIFICATION
    assert payload["loss_ledger"]["preserved_review_cards"] == 3


def _single_row(rows, row_kind: str):
    matches = [row for row in rows if row.row_kind == row_kind]
    assert len(matches) == 1
    return matches[0]


def _packet(
    *,
    source_family: str = "fragrance_native_database",
    source_surface: str = "fragrantica_product_page_direct_http",
) -> tuple[SourceCapturePacket, dict[str, bytes]]:
    raw = {
        "file_01": _html().encode("utf-8"),
        "file_02": b'{"status": 200}',
    }
    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason("fixture does not supply source event timing"),
        source_edit_or_version=unknown_with_reason("fixture does not supply edit timing"),
        capture_time=known_fact("2026-06-28T18:57:58Z"),
        recapture_time=not_applicable("first capture"),
        cutoff_posture=unknown_with_reason("test fixture has no decision cutoff"),
    )
    packet = SourceCapturePacket(
        packet_id="pkt-fragrantica",
        manifest_version="source_capture_packet_manifest_v1",
        obligation_contract_version="core_spine_v0_data_capture_spine_obligation_contract_v0",
        source_family=source_family,
        source_surface=source_surface,
        source_locator=known_fact(
            "https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html"
        ),
        requested_decision_context=known_fact("test Fragrantica projection"),
        capture_context=known_fact("unit test packet"),
        actor_audience_context=unknown_with_reason("not supplied by fixture"),
        capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
        operator_category="unit_test",
        session_identity="",
        timing=timing,
        access_posture=known_fact("direct HTTP fixture supplied"),
        archive_history_posture=not_attempted("archive not queried"),
        media_modality_posture=not_attempted("linked media not fetched"),
        re_capture_relationship=not_applicable("first capture"),
        source_slices=[
            SourceCaptureSlice(
                slice_id="slice_01",
                locator=known_fact(
                    "https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html"
                ),
                timing=timing,
                access_posture=known_fact("direct HTTP fixture supplied"),
                archive_history_posture=not_attempted("archive not queried"),
                media_modality_posture=not_attempted("linked media not fetched"),
                re_capture_relationship=not_applicable("first capture"),
                limitations=[],
                warning_notes=[],
                preserved_file_ids=["file_01", "file_02"],
            )
        ],
        preserved_files=[
            _preserved_file("file_01", "raw/01_http_response_body.bin", raw["file_01"]),
            _preserved_file("file_02", "raw/02_http_response_metadata.json", raw["file_02"]),
        ],
        receipt_metadata=ReceiptMetadata(
            title="Source Capture Packet Receipt",
            generated_at="2026-06-28T18:57:59Z",
            summary="unit test packet",
            non_claims=["not Cleaning", "not Judgment"],
        ),
    )
    return packet, raw


def _preserved_file(file_id: str, relative_path: str, body: bytes) -> PreservedFile:
    return PreservedFile(
        file_id=file_id,
        original_path=relative_path.rsplit("/", 1)[-1],
        relative_packet_path=relative_path,
        sha256=hashlib.sha256(body).hexdigest(),
        hash_basis="raw_stored_bytes",
        size_bytes=len(body),
    )


def _write_packet_dir(tmp_path: Path, *, packet: SourceCapturePacket, raw: dict[str, bytes]) -> Path:
    packet_dir = tmp_path / "packet"
    for preserved_file in packet.preserved_files:
        raw_path = packet_dir / preserved_file.relative_packet_path
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_bytes(raw[preserved_file.file_id])
    (packet_dir / "manifest.json").write_text(
        f"{json.dumps(packet.model_dump(mode='json'), indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    return packet_dir


def _review_card(comment_id: str, *, author: str, date: str, text: str, rating: int, tab: str) -> str:
    votes = (
        '{"rating":'
        f"{rating},"
        '"winter":0,"spring":0,"summer":0,"autumn":0,"day":0,"night":0,'
        '"longevity":3,"sillage":2,"gender":"female_unisex","relation":"have"}'
    )
    escaped_votes = (
        votes.replace('"', "&quot;")
    )
    return f"""
    <div id="parent{comment_id}" class="cell tw-review-card tw-gradient-rose" itemprop="review" itemscope>
      <user-perfume-votes-new :perfume-votes="{escaped_votes}"></user-perfume-votes-new>
      <div itemprop="author" itemscope>
        <meta itemprop="name" content="{author}"/>
        <span title="https://www.fragrantica.com/@{author.lower()}">
          <img itemprop="image" src="https://fimgs.net/mdimg/avatari/{comment_id}.jpg" alt="{author}">
        </span>
      </div>
      <span itemprop="datePublished" content="{date}">{date}</span>
      <div itemprop="reviewBody">
        <review-read-more-new :text-length="{len(text)}">
          <div id="review_{comment_id}"><p>{text}</p></div>
        </review-read-more-new>
      </div>
      <vote-buttons-new initial-status="neutral" item-id="33519" comment-id="{comment_id}" vote-for="perfumeReview"></vote-buttons-new>
      <share-new path="/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html?ccid={comment_id}#focus-zone"></share-new>
      <span class="fixture-tab">{tab}</span>
    </div>
    """


def _html() -> str:
    return f"""
    <html>
      <head>
        <link rel="canonical" href="https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html"/>
        <meta name="description" content="Baccarat Rouge 540 by Maison Francis Kurkdjian is a Oriental Floral fragrance for women and men."/>
        <meta name="keywords" content="Baccarat Rouge 540, Maison Francis Kurkdjian, perfume review"/>
        <title>Baccarat Rouge 540 Maison Francis Kurkdjian perfume - a fragrance for women and men 2015</title>
      </head>
      <body>
        <div id="perfume-description-content" itemprop="description">
          <p><b>Baccarat Rouge 540</b> by <b>Maison Francis Kurkdjian</b> is a fragrance. Baccarat Rouge 540 was launched in 2015.</p>
        </div>
        <p itemprop="aggregateRating" itemscope>
          Perfume rating <span itemprop="ratingValue">3.76</span> out of <span itemprop="bestRating">5</span>
          with <span itemprop="ratingCount" content="28808">28,808</span> votes
        </p>
        <span>Reviews (<span>3.9K</span>)</span>
        <longevity-rating-new :perfume_id="33519"></longevity-rating-new>
        <sillage-rating-new :perfume_id="33519"></sillage-rating-new>
        <seasons-rating-new :perfume_id="33519"></seasons-rating-new>
        <nav aria-label="Reviews tabs">
          <button data-tab="all-reviews" data-active="true"><span>All reviews by date</span></button>
          <button data-tab="popular-positive-reviews"><span>Positive Reviews</span></button>
          <button data-tab="popular-negative-reviews"><span>Negative Reviews</span></button>
          <button data-tab="search-reviews"><span>Search</span></button>
        </nav>
        <div class="review-tab-panel" id="all-reviews" data-active="true">
          {_review_card("3090334", author="Rimazy", date="2026-06-25", text="This perfume died young.", rating=5, tab="all")}
          {_review_card("3086504", author="Linlin", date="2026-06-22", text="Second current-window review.", rating=1, tab="all")}
          <reviews-infinity-new :perfume-id="33519" sentiment="all" :is-logged="false" login-url="/board/login.php"
            :lang-strings="{{&quot;loginPromptTitle&quot;:&quot;Want to see more reviews?&quot;,&quot;loginPromptMessage&quot;:&quot;Sign in to access the full review archive&quot;,&quot;loginButtonText&quot;:&quot;Log in&quot;}}">
          </reviews-infinity-new>
        </div>
        <div class="review-tab-panel hidden" id="popular-positive-reviews">
          {_review_card("1993513", author="Positive", date="2025-01-01", text="Popular positive review.", rating=5, tab="positive")}
          <reviews-infinity-new :perfume-id="33519" sentiment="positive" :is-logged="false" login-url="/board/login.php"
            :lang-strings="{{&quot;loginPromptMessage&quot;:&quot;Sign in to access the full review archive&quot;}}">
          </reviews-infinity-new>
        </div>
        <div class="review-tab-panel hidden" id="popular-negative-reviews">
          <reviews-infinity-new :perfume-id="33519" sentiment="negative" :is-logged="false" login-url="/board/login.php"
            :lang-strings="{{&quot;loginPromptMessage&quot;:&quot;Sign in to access the full review archive&quot;}}">
          </reviews-infinity-new>
        </div>
        <div class="review-tab-panel hidden" id="search-reviews">
          <search-perfume-reviews-new :perfume_id="33519"></search-perfume-reviews-new>
        </div>
      </body>
    </html>
    """
