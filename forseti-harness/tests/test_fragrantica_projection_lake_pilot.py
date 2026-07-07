from __future__ import annotations

from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard
from source_capture.fragrantica_projection import (
    PROJECTION_FRAGRANTICA_LANE,
    project_fragrantica_into_lake,
)
from source_capture.models import (
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.writer import write_local_source_capture_packet


_CAPTURE_TIME = "2026-06-28T18:57:58Z"


def test_projects_committed_fragrantica_raw_into_derived_record(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id = _commit_fragrantica_packet(root, tmp_path)

    projection, derived_path = project_fragrantica_into_lake(data_root=root, packet_id=packet_id)

    assert derived_path.parent == root.path / "derived" / raw_shard(packet_id) / packet_id / PROJECTION_FRAGRANTICA_LANE
    assert derived_path.suffix == ".json"
    assert derived_path.is_file()
    assert projection.packet_id == packet_id
    assert projection.loss_ledger.preserved_review_cards == 1
    assert "full_review_archive_not_captured_login_prompt_present" in projection.residuals

    assert root.load_raw_packet(packet_id).manifest["packet_id"] == packet_id


def test_fragrantica_projection_re_derive_appends_sibling_not_overwrite(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id = _commit_fragrantica_packet(root, tmp_path)

    _, first = project_fragrantica_into_lake(data_root=root, packet_id=packet_id)
    _, second = project_fragrantica_into_lake(data_root=root, packet_id=packet_id)

    lane_dir = root.path / "derived" / raw_shard(packet_id) / packet_id / PROJECTION_FRAGRANTICA_LANE
    assert first != second
    assert len(list(lane_dir.glob("*.json"))) == 2


def test_fragrantica_projection_explicit_record_id_is_create_only(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id = _commit_fragrantica_packet(root, tmp_path)

    project_fragrantica_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")
    with pytest.raises(DataLakeRootError):
        project_fragrantica_into_lake(data_root=root, packet_id=packet_id, record_id="rec1")


def _commit_fragrantica_packet(root: DataLakeRoot, tmp_path: Path) -> str:
    body_path = tmp_path / "http_response_body.bin"
    body_path.write_text(_html(), encoding="utf-8")
    metadata_path = tmp_path / "http_response_metadata.json"
    metadata_path.write_text('{"status": 200}\n', encoding="utf-8")

    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason("fixture does not supply source event timing"),
        source_edit_or_version=unknown_with_reason("fixture does not supply edit timing"),
        capture_time=known_fact(_CAPTURE_TIME),
        recapture_time=not_applicable("first capture"),
        cutoff_posture=unknown_with_reason("test fixture has no decision cutoff"),
    )
    source_slice = SourceCaptureSlice(
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
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[body_path, metadata_path],
        source_family="fragrance_native_database",
        source_surface="fragrantica_product_page_direct_http",
        source_locator=known_fact(
            "https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html"
        ),
        decision_question="test Fragrantica projection into lake",
        capture_context="fragrantica projection lake pilot",
        source_slices=[source_slice],
    )
    return result.packet.packet_id


def _html() -> str:
    return """
    <html><head>
      <link rel="canonical" href="https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html"/>
      <title>Baccarat Rouge 540 Maison Francis Kurkdjian perfume</title>
    </head><body>
      <div id="perfume-description-content" itemprop="description">
        <p><b>Baccarat Rouge 540</b> by <b>Maison Francis Kurkdjian</b> is a fragrance. Baccarat Rouge 540 was launched in 2015.</p>
      </div>
      <p itemprop="aggregateRating"><span itemprop="ratingValue">3.76</span><span itemprop="bestRating">5</span><span itemprop="ratingCount" content="28808">28,808</span></p>
      <span>Reviews (<span>3.9K</span>)</span>
      <button data-tab="all-reviews" data-active="true">All reviews by date</button>
      <div class="review-tab-panel" id="all-reviews">
        <div id="parent3090334" class="cell tw-review-card tw-gradient-rose" itemprop="review" itemscope>
          <user-perfume-votes-new :perfume-votes="{&quot;rating&quot;:5,&quot;winter&quot;:0,&quot;spring&quot;:0,&quot;summer&quot;:0,&quot;autumn&quot;:0,&quot;day&quot;:0,&quot;night&quot;:0,&quot;longevity&quot;:3,&quot;sillage&quot;:2,&quot;gender&quot;:&quot;female_unisex&quot;,&quot;relation&quot;:&quot;have&quot;}"></user-perfume-votes-new>
          <meta itemprop="name" content="Rimazy"/>
          <span itemprop="datePublished" content="2026-06-25">06/25/26 18:41</span>
          <div id="review_3090334"><p>This perfume died young.</p></div>
          <vote-buttons-new initial-status="neutral" item-id="33519" comment-id="3090334" vote-for="perfumeReview"></vote-buttons-new>
          <share-new path="/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html?ccid=3090334#focus-zone"></share-new>
        </div>
        <reviews-infinity-new :perfume-id="33519" sentiment="all" :is-logged="false" login-url="/board/login.php"
          :lang-strings="{&quot;loginPromptMessage&quot;:&quot;Sign in to access the full review archive&quot;}">
        </reviews-infinity-new>
      </div>
    </body></html>
    """
