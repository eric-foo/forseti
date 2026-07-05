from __future__ import annotations

import json
from pathlib import Path

from cleaning.parfumo_lake import derive_parfumo_cleaning_into_lake
from data_lake.lane_registry import LaneRole, role_of
from data_lake.non_silver_record import validate_non_silver_record
from data_lake.root import DataLakeRoot
from source_capture.models import SourceCapturePacket, known_fact
from source_capture.parfumo_projection import PROJECTION_PARFUMO_LANE, build_parfumo_projection
from source_capture.writer import write_local_source_capture_packet


_LOCATOR = "https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum"
_HTML = """
<html><head>
  <link rel="canonical" href="https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum"/>
  <title>Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian (Eau de Parfum) & Perfume Facts</title>
</head><body>
  <main data-perfume-id="67720" data-rating-count="5176" data-review-count="369" data-statement-count="1390">
    <script>const routes = {reviews: "/action/perfume/get_reviews.php", statements: "/action/perfume/get_statements.php", p_id: 67720};</script>
    <article data-review-id="900001" data-author="Rimazy"><p data-role="review-text">This perfume died young.</p></article>
    <article data-statement-id="st7001" data-author="Lyra"><p data-role="statement-text">Airy amber trail.</p></article>
  </main>
</body></html>
"""


def test_parfumo_registry_roles_match_validator_expectations() -> None:
    assert role_of("cleaning_parfumo_audit") is LaneRole.CLEANING_AUDIT
    assert role_of(PROJECTION_PARFUMO_LANE) is LaneRole.PROJECTION
    assert role_of("cleaning_parfumo_silver") is LaneRole.SILVER_ENVELOPE


def test_real_parfumo_cleaning_audit_and_projection_pass_non_silver_validator(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    packet_id = _commit_packet(root, tmp_path)

    result = derive_parfumo_cleaning_into_lake(data_root=root, packet_id=packet_id)
    audit = json.loads(result.audit_path.read_text(encoding="utf-8"))
    validate_non_silver_record(LaneRole.CLEANING_AUDIT, audit)

    loaded = root.load_raw_packet(packet_id)
    projection = build_parfumo_projection(
        packet=SourceCapturePacket.model_validate(loaded.manifest),
        raw_file_bytes_by_file_id=loaded.bodies,
    ).model_dump(mode="json")
    validate_non_silver_record(LaneRole.PROJECTION, projection)


def _commit_packet(root: DataLakeRoot, tmp_path: Path) -> str:
    body_path = tmp_path / "http_response_body.bin"
    body_path.write_text(_HTML, encoding="utf-8")
    metadata_path = tmp_path / "http_response_metadata.json"
    metadata_path.write_text('{"status": 200}\n', encoding="utf-8")
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[body_path, metadata_path],
        source_family="fragrance_native_database",
        source_surface="parfumo_product_page_direct_http",
        source_locator=known_fact(_LOCATOR),
        decision_question="test Parfumo non-silver conformance",
        capture_context="parfumo non-silver conformance fixture",
    )
    return result.packet.packet_id
