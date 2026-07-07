from __future__ import annotations

import json
from pathlib import Path

from cleaning.basenotes_lake import derive_basenotes_cleaning_into_lake
from data_lake.lane_registry import LaneRole, role_of
from data_lake.non_silver_record import validate_non_silver_record
from data_lake.root import DataLakeRoot
from source_capture.models import SourceCapturePacket, known_fact
from source_capture.basenotes_projection import PROJECTION_BASENOTES_LANE, build_basenotes_projection
from source_capture.writer import write_local_source_capture_packet


_LOCATOR = "https://basenotes.com/fragrances/mojave-ghost-by-byredo.26143979"
_SOURCE_SURFACE = "basenotes_product_page_cloakbrowser_deep_scroll_current_window"
_FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "basenotes"
    / "mojave_ghost_product_page.html"
)


def _fixture_html() -> str:
    return _FIXTURE.read_text(encoding="utf-8")


def test_basenotes_registry_roles_match_validator_expectations() -> None:
    assert role_of("cleaning_basenotes_audit") is LaneRole.CLEANING_AUDIT
    assert role_of(PROJECTION_BASENOTES_LANE) is LaneRole.PROJECTION
    assert role_of("cleaning_basenotes_silver") is LaneRole.SILVER_ENVELOPE


def test_real_basenotes_cleaning_audit_and_projection_pass_non_silver_validator(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id = _commit_packet(root, tmp_path)

    result = derive_basenotes_cleaning_into_lake(data_root=root, packet_id=packet_id)
    audit = json.loads(result.audit_path.read_text(encoding="utf-8"))
    validate_non_silver_record(LaneRole.CLEANING_AUDIT, audit)
    assert audit["record_family"] == "processing_audit"
    assert "not_judgment" in audit["non_claims"]
    assert "transform_ledger" in audit["payload"]["cleaning_packet"]

    loaded = root.load_raw_packet(packet_id)
    projection = build_basenotes_projection(
        packet=SourceCapturePacket.model_validate(loaded.manifest),
        raw_file_bytes_by_file_id=loaded.bodies,
    ).model_dump(mode="json")
    validate_non_silver_record(LaneRole.PROJECTION, projection)


def _commit_packet(root: DataLakeRoot, tmp_path: Path) -> str:
    body_path = tmp_path / "cloakbrowser_rendered_dom.html"
    body_path.write_text(_fixture_html(), encoding="utf-8")
    metadata_path = tmp_path / "cloakbrowser_snapshot_metadata.json"
    metadata_path.write_text('{"capture_timestamp": "2026-06-30T00:00:00Z"}\n', encoding="utf-8")
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[body_path, metadata_path],
        source_family="fragrance_native_database",
        source_surface=_SOURCE_SURFACE,
        source_locator=known_fact(_LOCATOR),
        decision_question="test Basenotes non-silver conformance",
        capture_context="basenotes non-silver conformance fixture",
    )
    return result.packet.packet_id
