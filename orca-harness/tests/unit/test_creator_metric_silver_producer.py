"""Unit tests for the Silver Vault creator-metric producer.

These build IG reels-grid projection fixtures in a temp dir and a temp lake
(``DataLakeRoot.for_test``) -- no external lake drive is required. They assert
the producer emits Silver Vault-conformant records, reproduces ``content_hash``
independently, obeys posture/value coupling, threads rollup -> observation
lineage, and does NOT drift from the reused seed computation.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from capture_spine.creator_profile_current.silver_metric_producer import (
    METRIC_OBSERVATION_LANE,
    METRIC_OBSERVATION_PAYLOAD_KIND,
    METRIC_ROLLUP_LANE,
    METRIC_ROLLUP_PAYLOAD_KIND,
    derive_creator_metric_silver_records_from_projections,
)
from capture_spine.creator_profile_current.silver_metric_reader import (
    discover_creator_metric_rollup_records,
    read_creator_metric_rollups_from_lake,
)
from capture_spine.creator_profile_current.silver_metric_snapshot import (
    SNAPSHOT_WRAPPER_KEY,
    generate_creator_metric_rollup_snapshot,
    validate_snapshot,
)
from data_lake.catalog import rebuild_catalog
from data_lake.root import DataLakeRoot, DataLakeRootError
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet

PACKET_ID = "packet_fixture"
GENERATED_AT = "2026-06-29T00:02:00Z"


def _content_hash(record: dict) -> str:
    """Independent re-implementation of the canonical content hash (catches a
    producer-side helper mistake instead of trusting it)."""
    canonical = dict(record)
    canonical.pop("content_hash", None)
    payload = json.dumps(
        canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _account_ledger() -> dict:
    return {
        "platform_accounts": [
            {
                "platform_account_id": "acct_ig_fixture_001",
                "platform": "instagram",
                "public_handle": "fixturecreator",
                "public_profile_url": "https://www.instagram.com/fixturecreator/",
                "handle_source_pointer": "fixture#/rows/0",
                "handle_observed_at": "2026-06-29T00:00:00Z",
            }
        ]
    }


def _profile_row(username: str, value: int, capture_time: str) -> dict:
    return {
        "row_id": f"{PACKET_ID}:profile:follower_count",
        "row_kind": "ig_creator_metric",
        "username": username,
        "content_kind": "profile",
        "content_shortcode": None,
        "content_url": None,
        "metric": "follower_count",
        "posture": "observed",
        "value": value,
        "reason": None,
        "capture_time": capture_time,
        "coverage_window": {"start": None, "end": capture_time},
        "raw_ref": {"packet_id": PACKET_ID, "slice_id": "ig_reels_profile_00"},
        "raw_anchor": {
            "file_id": "file_01",
            "relative_packet_path": "raw/01.json",
            "sha256": "a" * 64,
            "hash_basis": "raw_stored_bytes",
        },
        "chosen_source_surface": "web_profile_info_json_metadata",
        "source_surface_count_candidates": [],
        "source_publication_or_event": None,
    }


def _reel_row(username: str, shortcode: str, metric: str, value: int, capture_time: str) -> dict:
    return {
        "row_id": f"{PACKET_ID}:{shortcode}:{metric}",
        "row_kind": "ig_media_metric",
        "username": username,
        "content_kind": "reel",
        "content_shortcode": shortcode,
        "content_url": f"https://www.instagram.com/{username}/reel/{shortcode}/",
        "metric": metric,
        "posture": "observed",
        "value": value,
        "reason": None,
        "capture_time": capture_time,
        "coverage_window": {"start": None, "end": capture_time},
        "raw_ref": {"packet_id": PACKET_ID, "slice_id": "ig_reels_grid_01"},
        "raw_anchor": {
            "file_id": "file_01",
            "relative_packet_path": "raw/01.json",
            "sha256": "a" * 64,
            "hash_basis": "raw_stored_bytes",
        },
        "chosen_source_surface": "clips_user_json_metadata",
        "source_surface_count_candidates": [],
        "source_publication_or_event": capture_time,
    }


def _projection_rows() -> list[dict]:
    rows = [_profile_row("fixturecreator", 1000, "2026-06-29T00:01:00Z")]
    for shortcode, view, like, comment in (("AAA", 100, 10, 5), ("BBB", 300, 30, 15)):
        rows.append(_reel_row("fixturecreator", shortcode, "view_count", view, "2026-06-29T00:01:00Z"))
        rows.append(_reel_row("fixturecreator", shortcode, "like_count", like, "2026-06-29T00:01:00Z"))
        rows.append(_reel_row("fixturecreator", shortcode, "comment_count", comment, "2026-06-29T00:01:00Z"))
    return rows


def _run(tmp_path: Path):
    projection = tmp_path / "projection.json"
    projection.write_text(json.dumps({"packet_id": PACKET_ID, "rows": _projection_rows()}), encoding="utf-8")
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    return derive_creator_metric_silver_records_from_projections(
        data_root=data_root,
        projection_paths=[projection],
        account_ledger=_account_ledger(),
        generated_at_utc=GENERATED_AT,
    )


def _projection_rows_for_anchor(packet_id: str, raw_anchor: dict) -> list[dict]:
    rows = _projection_rows()
    for row in rows:
        row["row_id"] = str(row["row_id"]).replace(PACKET_ID, packet_id)
        row["raw_ref"] = dict(row["raw_ref"], packet_id=packet_id)
        row["raw_anchor"] = dict(raw_anchor)
    return rows


def _commit_bronze_reels_packet(data_root: DataLakeRoot, tmp_path: Path) -> tuple[str, dict]:
    raw = tmp_path / "ig_reels_grid_capture.json"
    raw.write_text(json.dumps({"grid": "fixture"}, sort_keys=True), encoding="utf-8")
    result = write_local_source_capture_packet(
        data_root=data_root,
        input_files=[raw],
        source_family="instagram_creator",
        source_surface="ig_reels_grid_dom_passive_json",
        source_locator=known_fact("https://www.instagram.com/fixturecreator/reels/"),
        decision_question="creator metric AR-backed raw refs",
        capture_context="creator metric Silver AR proof test",
    )
    packet_id = result.packet.packet_id
    preserved = data_root.load_raw_packet(packet_id).manifest["preserved_files"][0]
    raw_anchor = {
        "file_id": preserved["file_id"],
        "relative_packet_path": preserved["relative_packet_path"],
        "sha256": preserved["sha256"],
        "hash_basis": preserved["hash_basis"],
    }
    return packet_id, raw_anchor


def test_producer_emits_conformant_metric_observation_records(tmp_path: Path) -> None:
    result = _run(tmp_path)
    # 1 profile follower + 2 reels x (view, like, comment) = 7 observations.
    assert len(result.observation_records) == 7
    for record in result.observation_records:
        assert record["schema_version"] == "silver_vault_record_v0"
        assert record["record_kind"] == "observation"
        assert record["payload_kind"] == METRIC_OBSERVATION_PAYLOAD_KIND
        assert record["lane_namespace"] == METRIC_OBSERVATION_LANE
        assert record["content_hash_basis"] == "canonical_json_excluding_content_hash"
        assert record["raw_anchor"] == PACKET_ID
        assert record["content_hash"] == f"sha256:{_content_hash(record)}"
        assert record["raw_refs"][0]["packet_id"] == PACKET_ID
        assert record["raw_refs"][0]["sha256"]

        observation = record["payload"]["observation"]
        posture = observation["metric_posture"]
        if posture["kind"] == "observed":
            assert isinstance(observation["metric_value"], (int, float))
            assert not isinstance(observation["metric_value"], bool)
            assert posture["reason_detail"] is None
        else:
            assert observation["metric_value"] is None
            assert posture["reason_detail"]


def test_observation_raw_refs_use_bronze_attachment_records_when_requested(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id, raw_anchor = _commit_bronze_reels_packet(data_root, tmp_path)
    assert rebuild_catalog(data_root)["status"] == "rebuilt"
    projection = tmp_path / "projection.json"
    projection.write_text(
        json.dumps({"packet_id": packet_id, "rows": _projection_rows_for_anchor(packet_id, raw_anchor)}),
        encoding="utf-8",
    )

    result = derive_creator_metric_silver_records_from_projections(
        data_root=data_root,
        projection_paths=[projection],
        account_ledger=_account_ledger(),
        generated_at_utc=GENERATED_AT,
        use_bronze_attachment_records=True,
    )

    assert result.observation_records
    for record in result.observation_records:
        raw_ref = record["raw_refs"][0]
        assert raw_ref["raw_ref_kind"] == "bronze_attachment_record"
        assert raw_ref["attachment_record_id"].startswith("ar_")
        assert raw_ref["attachment_record_schema_version"] == "bronze_attachment_record_v0_schema_2"
        assert raw_ref["attachment_record_physicalization"] == "manifest_equivalent_entry_over_raw_packet_body_v0"
        assert raw_ref["packet_id"] == packet_id
        assert raw_ref["file_id"] == raw_anchor["file_id"]
        assert raw_ref["relative_packet_path"] == raw_anchor["relative_packet_path"]
        assert raw_ref["body_sha256"] == raw_anchor["sha256"]
        assert raw_ref["body_ref"] == {
            "kind": "raw_packet_relative_path",
            "packet_id": packet_id,
            "file_id": raw_anchor["file_id"],
            "relative_packet_path": raw_anchor["relative_packet_path"],
            "body_sha256": raw_anchor["sha256"],
            "hash_basis": "raw_stored_bytes",
        }
        assert raw_ref["source_family"] == "instagram_creator"
        assert raw_ref["source_surface"] == "ig_reels_grid_dom_passive_json"
        assert raw_ref["payload_kind"] == "json_body"
        assert "lineage_limitations" not in record


def test_ar_mode_records_round_trip_through_reader_discovery_and_snapshot(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id, raw_anchor = _commit_bronze_reels_packet(data_root, tmp_path)
    assert rebuild_catalog(data_root)["status"] == "rebuilt"
    projection = tmp_path / "projection.json"
    projection.write_text(
        json.dumps({"packet_id": packet_id, "rows": _projection_rows_for_anchor(packet_id, raw_anchor)}),
        encoding="utf-8",
    )

    result = derive_creator_metric_silver_records_from_projections(
        data_root=data_root,
        projection_paths=[projection],
        account_ledger=_account_ledger(),
        generated_at_utc=GENERATED_AT,
        use_bronze_attachment_records=True,
    )
    seed_rollup = result.seed_document["instagram_reels_creator_metric_seed"]["metric_rollups"][0]

    reconstructed = read_creator_metric_rollups_from_lake(data_root, raw_anchors=[packet_id])
    assert reconstructed == [seed_rollup]

    discovered = discover_creator_metric_rollup_records(data_root, account_ledger=_account_ledger())
    assert sorted(discovered) == ["acct_ig_fixture_001"]
    assert len(discovered["acct_ig_fixture_001"]) == 1

    snapshot = generate_creator_metric_rollup_snapshot(
        data_root,
        account_ledger=_account_ledger(),
        platform="instagram",
        snapshot_generated_at=GENERATED_AT,
    ).snapshot
    assert validate_snapshot(snapshot) == []
    assert snapshot[SNAPSHOT_WRAPPER_KEY]["metric_rollups"] == [seed_rollup]


def test_missing_bronze_attachment_record_stays_visible_when_requested(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    assert rebuild_catalog(data_root)["status"] == "rebuilt"
    projection = tmp_path / "projection.json"
    projection.write_text(json.dumps({"packet_id": PACKET_ID, "rows": _projection_rows()}), encoding="utf-8")

    result = derive_creator_metric_silver_records_from_projections(
        data_root=data_root,
        projection_paths=[projection],
        account_ledger=_account_ledger(),
        generated_at_utc=GENERATED_AT,
        use_bronze_attachment_records=True,
    )

    raw_ref = result.observation_records[0]["raw_refs"][0]
    assert raw_ref["raw_ref_kind"] == "raw_packet_fallback_missing_attachment_record"
    assert raw_ref["typed_attachment_record_status"] == "missing"
    assert raw_ref["attachment_record_residual"] == "typed_attachment_record_missing_for_raw_ref"
    assert result.observation_records[0]["lineage_limitations"] == [
        {"reason": "other", "detail": "typed_attachment_record_missing_for_raw_ref"}
    ]

    on_disk = json.loads(result.observation_paths[0].read_text(encoding="utf-8"))
    assert on_disk["lineage_limitations"] == [
        {"reason": "other", "detail": "typed_attachment_record_missing_for_raw_ref"}
    ]


def test_bronze_attachment_records_require_current_catalog_when_requested(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    projection = tmp_path / "projection.json"
    projection.write_text(json.dumps({"packet_id": PACKET_ID, "rows": _projection_rows()}), encoding="utf-8")

    with pytest.raises(DataLakeRootError, match="Bronze catalog is not current"):
        derive_creator_metric_silver_records_from_projections(
            data_root=data_root,
            projection_paths=[projection],
            account_ledger=_account_ledger(),
            generated_at_utc=GENERATED_AT,
            use_bronze_attachment_records=True,
        )


def test_observation_records_written_and_reload_with_stable_hash(tmp_path: Path) -> None:
    result = _run(tmp_path)
    assert len(result.observation_paths) == len(result.observation_records) == 7
    for record, path in zip(result.observation_records, result.observation_paths, strict=True):
        assert path.exists()
        on_disk = json.loads(path.read_text(encoding="utf-8"))
        assert on_disk["record_id"] == record["record_id"]
        # the on-disk record's hash reproduces from its own content
        assert on_disk["content_hash"] == f"sha256:{_content_hash(on_disk)}"


def test_rollup_record_lineage_and_no_drift(tmp_path: Path) -> None:
    result = _run(tmp_path)
    assert len(result.rollup_records) == 1
    rollup = result.rollup_records[0]
    assert rollup["record_kind"] == "observation"
    assert rollup["payload_kind"] == METRIC_ROLLUP_PAYLOAD_KIND
    assert rollup["lane_namespace"] == METRIC_ROLLUP_LANE
    assert rollup["raw_anchor"] == PACKET_ID
    assert rollup["content_hash"] == f"sha256:{_content_hash(rollup)}"

    seed_rollup = result.seed_document["instagram_reels_creator_metric_seed"]["metric_rollups"][0]
    observations_by_record_id = {record["record_id"]: record for record in result.observation_records}

    # derived_refs point at the emitted observation records, content hash matches.
    assert len(rollup["derived_refs"]) == len(seed_rollup["source_metric_observation_ids"]) == 6
    for edge in rollup["derived_refs"]:
        assert edge["edge_type"] == "derived_from_record"
        assert edge["lane_namespace"] == METRIC_OBSERVATION_LANE
        assert edge["content_hash"] == observations_by_record_id[edge["record_id"]]["content_hash"]

    # no-drift: the rollup record's numbers equal the reused seed computation.
    payload = rollup["payload"]["observation"]
    assert payload["derivation"] == {
        "kind": "computed_metric_rollup",
        "source_record_ref_kind": "derived_refs",
        "metric_posture_semantics": "source_input_support_not_raw_aggregate_visibility",
        "calculation_recipe_version": seed_rollup["calculation_recipe_version"],
    }
    assert payload["observation_count"] == seed_rollup["observation_count"] == 6
    assert payload["view_count_min"] == seed_rollup["view_count_min"] == 100
    assert payload["view_count_max"] == seed_rollup["view_count_max"] == 300
    assert (
        payload["metric_rollups"]["average_views"]["metric_value"]
        == seed_rollup["metric_rollups"]["average_views"]["value_or_none"]
        == 200
    )
    assert (
        payload["metric_rollups"]["engagement_rate"]["metric_value"]
        == seed_rollup["metric_rollups"]["engagement_rate"]["value_or_none"]
        == 0.15
    )
    assert payload["sample_support"] == seed_rollup["sample_support"]
    assert payload["limitations"] == seed_rollup["limitations"]


def test_rollup_metric_posture_value_coupling(tmp_path: Path) -> None:
    result = _run(tmp_path)
    payload = result.rollup_records[0]["payload"]["observation"]
    for metric in payload["metric_rollups"].values():
        posture = metric["metric_posture"]
        if posture["kind"] == "observed":
            assert isinstance(metric["metric_value"], (int, float))
            assert not isinstance(metric["metric_value"], bool)
            assert posture["reason_detail"] is None
        else:
            assert metric["metric_value"] is None
            assert posture["reason_detail"]


def test_content_subject_missing_native_id_fails_closed(tmp_path: Path) -> None:
    rows = _projection_rows()
    rows[1] = dict(rows[1], content_shortcode=None)
    projection = tmp_path / "projection.json"
    projection.write_text(json.dumps({"packet_id": PACKET_ID, "rows": rows}), encoding="utf-8")
    data_root = DataLakeRoot.for_test(tmp_path / "lake")

    with pytest.raises(ValueError, match="content subject requires a non-empty entity_key native_id"):
        derive_creator_metric_silver_records_from_projections(
            data_root=data_root,
            projection_paths=[projection],
            account_ledger=_account_ledger(),
            generated_at_utc=GENERATED_AT,
        )
