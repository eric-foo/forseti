"""Historical raw-packet compatibility at the Cleaning boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from cleaning.basenotes import build_basenotes_cleaning_packet_from_source
from cleaning.fragrantica import build_fragrantica_cleaning_packet_from_source
from cleaning.parfumo import build_parfumo_cleaning_packet_from_source
from cleaning.retail_pdp import build_retail_pdp_cleaning_input
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


_BASENOTES_FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "basenotes"
    / "mojave_ghost_product_page.html"
)

_FRAGRANTICA_HTML = """
<html><head>
  <link rel="canonical" href="https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html"/>
</head><body>
  <div id="perfume-description-content" itemprop="description">
    <p><b>Baccarat Rouge 540</b> by <b>Maison Francis Kurkdjian</b> is a fragrance.</p>
  </div>
  <button data-tab="all-reviews" data-active="true">All reviews by date</button>
  <div class="review-tab-panel" id="all-reviews">
    <div id="parent3090334" class="cell tw-review-card" itemprop="review" itemscope>
      <user-perfume-votes-new :perfume-votes="{&quot;rating&quot;:5,&quot;longevity&quot;:3,&quot;sillage&quot;:2,&quot;gender&quot;:&quot;female_unisex&quot;,&quot;relation&quot;:&quot;have&quot;}"></user-perfume-votes-new>
      <meta itemprop="name" content="Rimazy"/>
      <span itemprop="datePublished" content="2026-06-25">06/25/26</span>
      <div id="review_3090334"><p>This perfume died young.</p></div>
    </div>
  </div>
</body></html>
"""

_PARFUMO_HTML = """
<html><head>
  <link rel="canonical" href="https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum"/>
  <title>Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian</title>
</head><body>
  <main data-perfume-id="67720" data-rating-count="5176" data-review-count="369" data-statement-count="1390">
    <script>const routes = {reviews: "/action/perfume/get_reviews.php", statements: "/action/perfume/get_statements.php", p_id: 67720};</script>
    <article data-review-id="900001" data-author="Rimazy" data-rating="8.0">
      <time datetime="2026-06-25">06/25/26</time>
      <p data-role="review-text">This perfume died young.</p>
    </article>
    <article data-statement-id="st7001" data-author="Lyra">
      <time datetime="2026-06-24">06/24/26</time>
      <p data-role="statement-text">Airy amber trail.</p>
    </article>
  </main>
</body></html>
"""


def _timing() -> PacketTiming:
    return PacketTiming(
        source_publication_or_event=unknown_with_reason(
            "fixture does not supply source event timing"
        ),
        source_edit_or_version=unknown_with_reason(
            "fixture does not supply edit timing"
        ),
        capture_time=known_fact("2026-07-01T00:00:00Z"),
        recapture_time=not_applicable("first capture"),
        cutoff_posture=unknown_with_reason("test fixture has no cutoff"),
    )


def _raw_packet(
    *,
    packet_id: str,
    source_family: str,
    source_surface: str,
    source_url: str,
    files: dict[str, tuple[str, bytes]],
) -> tuple[SourceCapturePacket, dict[str, bytes]]:
    timing = _timing()
    preserved = []
    file_bytes = {}
    file_ids = []
    for index, (name, body) in enumerate(files.values(), 1):
        file_id = f"file_{index:02d}"
        file_ids.append(file_id)
        file_bytes[file_id] = body
        preserved.append(
            PreservedFile(
                file_id=file_id,
                original_path=name,
                relative_packet_path=f"raw/{index:02d}_{name}",
                sha256=hashlib.sha256(body).hexdigest(),
                hash_basis="raw_stored_bytes",
                size_bytes=len(body),
            )
        )
    packet = SourceCapturePacket(
        packet_id=packet_id,
        manifest_version="source_capture_packet_manifest_v1",
        obligation_contract_version=(
            "core_spine_v0_data_capture_spine_obligation_contract_v0"
        ),
        source_family=source_family,
        source_surface=source_surface,
        source_locator=known_fact(source_url),
        requested_decision_context=known_fact("legacy raw compatibility test"),
        capture_context=known_fact("unit test historical raw packet"),
        actor_audience_context=unknown_with_reason("not supplied"),
        capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
        operator_category="unit_test",
        session_identity="",
        timing=timing,
        access_posture=known_fact("raw fixture supplied"),
        archive_history_posture=not_attempted("archive not queried"),
        media_modality_posture=not_attempted("media not supplied"),
        re_capture_relationship=not_applicable("first capture"),
        source_slices=[
            SourceCaptureSlice(
                slice_id="slice_01",
                locator=known_fact(source_url),
                timing=timing,
                access_posture=known_fact("raw fixture supplied"),
                archive_history_posture=not_attempted("archive not queried"),
                media_modality_posture=not_attempted("media not supplied"),
                re_capture_relationship=not_applicable("first capture"),
                limitations=[],
                warning_notes=[],
                preserved_file_ids=file_ids,
            )
        ],
        preserved_files=preserved,
        receipt_metadata=ReceiptMetadata(
            title="Source Capture Packet Receipt",
            generated_at="2026-07-01T00:00:01Z",
            summary="historical raw compatibility fixture",
            non_claims=["not live capture"],
        ),
    )
    return packet, file_bytes


def _assert_legacy_handles(packet, *, expected_prefix: str) -> None:
    assert packet.handles
    assert all(handle.source_row_id for handle in packet.handles)
    assert all(
        handle.handle_id.startswith(expected_prefix) for handle in packet.handles
    )
    assert all(
        handle.source_anchor is not None
        and handle.source_anchor.anchor_kind != "json_pointer"
        for handle in packet.handles
    )


def test_basenotes_raw_packet_uses_legacy_decoder_under_cleaning() -> None:
    url = "https://basenotes.com/fragrances/mojave-ghost-by-byredo.26143979"
    packet, bodies = _raw_packet(
        packet_id="01LEGACYBASENOTES",
        source_family="fragrance_native_database",
        source_surface=(
            "basenotes_product_page_user_cleared_persistent_chrome_current_window"
        ),
        source_url=url,
        files={
            "dom": (
                "browser_rendered_dom.html",
                _BASENOTES_FIXTURE.read_bytes(),
            ),
            "text": ("browser_visible_text.txt", b"Mojave Ghost visible text"),
        },
    )
    result = build_basenotes_cleaning_packet_from_source(
        packet=packet, file_bytes_by_file_id=bodies
    )
    _assert_legacy_handles(result, expected_prefix="cleaning:basenotes:")


def test_fragrantica_raw_packet_uses_legacy_decoder_under_cleaning() -> None:
    url = (
        "https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/"
        "Baccarat-Rouge-540-33519.html"
    )
    packet, bodies = _raw_packet(
        packet_id="01LEGACYFRAGRANTICA",
        source_family="fragrance_native_database",
        source_surface="fragrantica_product_page_direct_http",
        source_url=url,
        files={
            "body": ("http_response_body.bin", _FRAGRANTICA_HTML.encode()),
            "metadata": ("http_response_metadata.json", b'{"status": 200}'),
        },
    )
    result = build_fragrantica_cleaning_packet_from_source(
        packet=packet, file_bytes_by_file_id=bodies
    )
    _assert_legacy_handles(result, expected_prefix="cleaning:fragrantica:")


def test_parfumo_raw_packet_uses_legacy_decoder_under_cleaning() -> None:
    url = (
        "https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/"
        "Baccarat_Rouge_540_Eau_de_Parfum"
    )
    packet, bodies = _raw_packet(
        packet_id="01LEGACYPARFUMO",
        source_family="fragrance_native_database",
        source_surface="parfumo_product_page_direct_http",
        source_url=url,
        files={
            "body": ("http_response_body.bin", _PARFUMO_HTML.encode()),
            "metadata": ("http_response_metadata.json", b'{"status": 200}'),
        },
    )
    result = build_parfumo_cleaning_packet_from_source(
        packet=packet, file_bytes_by_file_id=bodies
    )
    _assert_legacy_handles(result, expected_prefix="cleaning:parfumo:")


def test_retail_raw_packet_uses_legacy_decoder_under_cleaning() -> None:
    url = "https://www.sephora.com/product/lip-sleeping-mask-in-berry-2-5g-P446304"
    product = {
        "@context": "https://schema.org",
        "@type": "ProductGroup",
        "productGroupID": "P446304",
        "name": "Lip Sleeping Mask",
        "hasVariant": [
            {
                "@type": "Product",
                "sku": "2240844",
                "name": "Lip Sleeping Mask in Berry",
                "offers": {
                    "@type": "Offer",
                    "price": "25.00",
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock",
                },
            }
        ],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.3",
            "reviewCount": "22000",
        },
    }
    html = (
        '<html><head><script type="application/ld+json">'
        + json.dumps(product)
        + "</script></head><body>IN STOCK</body></html>"
    ).encode()
    packet, bodies = _raw_packet(
        packet_id="01LEGACYRETAILPDP",
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        source_url=url,
        files={
            "dom": ("cloakbrowser_rendered_dom.html", html),
            "text": (
                "cloakbrowser_visible_text.txt",
                b"IN STOCK\nRatings & Reviews\n4.3\n22000 Reviews",
            ),
        },
    )
    result = build_retail_pdp_cleaning_input(
        packet=packet, file_bytes_by_file_id=bodies
    )
    assert result.legacy_input is True
    assert result.content_schema_version is None
    assert result.extractor_version is None
    _assert_legacy_handles(result, expected_prefix="cleaning:retail_pdp:")
