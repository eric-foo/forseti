from __future__ import annotations

import hashlib
import json
from pathlib import Path

from data_lake.root import DataLakeRoot, raw_shard
from data_lake.silver_census import (
    FRAGRANTICA_REVIEW_VOTE_POLICY_VERSION,
    _observation_window,
    build_silver_observation_census,
)
from data_lake.silver_record import (
    append_raw_packet_tombstone,
    append_silver_record,
    silver_content_hash,
)
from schemas.audience_comment_models import AudienceComment
from source_capture.ig_reels_deep_capture import ReelDeepCaptureResult
from source_capture.ig_reels_deep_capture_lake import (
    AUDIENCE_COMMENTS_LANE,
    DEEP_CAPTURE_SET_LANE,
    REEL_TRANSCRIPT_LANE,
    write_reel_deep_capture_into_lake,
)

PACKET = "01KW2MJM01Y0936VNECWB3MHSD"
PARFUMO_PACKET = "01KW2MJM01Y0936VNECWB3MHSE"
FAILED_DEEP_CAPTURE_PACKET = "01KW2MJM01Y0936VNECWB3MHSF"
FAILED_IG_GRID_PACKET = "01KW2MJM01Y0936VNECWB3MHSG"
OBSERVED_AT = "2026-07-15T00:00:00Z"


def test_census_does_not_substitute_capture_time_for_unknown_observed_at() -> None:
    observation = {
        "effective_interval": {
            "start": None,
            "start_precision": "unknown",
            "unknown_reason": "source exposes no effective timestamp",
        }
    }
    record = {"observed_at": None, "captured_at": OBSERVED_AT}

    assert _observation_window(record, observation) == "unknown"


def _write_deep_capture(root: DataLakeRoot, shortcode: str, comment_id: str, audio: bytes):
    """Write one packet-first deep capture and return its lake write handle."""
    comment = AudienceComment(
        comment_id=comment_id,
        reel_shortcode=shortcode,
        author_username="ana",
        text=f"comment on {shortcode}",
        like_count=2,
        created_at_unix=1784073600,
    )
    substrate = (
        json.dumps(
            {
                "pk": comment_id,
                "user": {"username": "ana"},
                "text": f"comment on {shortcode}",
                "comment_like_count": 2,
                "created_at": 1784073600,
                "__typename": "XIGComment",
            }
        )
        + "\n"
    ).encode()
    return write_reel_deep_capture_into_lake(
        data_root=root,
        result=ReelDeepCaptureResult(
            reel_shortcode=shortcode,
            comments=(comment,),
            transcript_posture="transcribed",
            transcript_cues=({"start_ms": 0, "end_ms": 1000, "text": f"audio {shortcode}"},),
            media_url_used="https://cdn.example/expiring.mp4?token=secret",
            comment_substrate=substrate,
            audio_bytes=audio,
            audio_ext="mp4",
        ),
        generated_at=OBSERVED_AT,
    )


def test_census_separates_current_source_backed_deep_capture_from_historical_audit_only(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    comment = AudienceComment(
        comment_id="c1",
        reel_shortcode="ReelCurrent",
        author_username="ana",
        text="exact comment",
        like_count=2,
        created_at_unix=1784073600,
    )
    substrate = (
        json.dumps(
            {
                "pk": "c1",
                "user": {"username": "ana"},
                "text": "exact comment",
                "comment_like_count": 2,
                "created_at": 1784073600,
                "__typename": "XIGComment",
            }
        )
        + "\n"
    ).encode()
    write_reel_deep_capture_into_lake(
        data_root=root,
        result=ReelDeepCaptureResult(
            reel_shortcode="ReelCurrent",
            comments=(comment,),
            transcript_posture="transcribed",
            transcript_cues=({"start_ms": 0, "end_ms": 1000, "text": "exact audio"},),
            media_url_used="https://cdn.example/expiring.mp4?token=secret",
            comment_substrate=substrate,
            audio_bytes=b"exact-audio-bytes",
            audio_ext="mp4",
        ),
        generated_at=OBSERVED_AT,
    )
    _manifest(
        root,
        FAILED_DEEP_CAPTURE_PACKET,
        "instagram_creator",
        "ig_reels_deep_capture",
        failed=True,
    )
    _manifest(
        root,
        FAILED_IG_GRID_PACKET,
        "instagram_creator",
        "ig_reels_grid_dom_passive_json",
        failed=True,
    )
    root.append_record_set(
        subtree="derived",
        raw_anchor="ReelLegacy",
        record_id="legacy.json",
        members={
            AUDIENCE_COMMENTS_LANE: b'{"reel_shortcode":"ReelLegacy","comments":[]}\n',
            REEL_TRANSCRIPT_LANE: b'{"reel_shortcode":"ReelLegacy","cues":[]}\n',
        },
        completion_lane=DEEP_CAPTURE_SET_LANE,
    )

    census = build_silver_observation_census(root)

    assert census["totals"]["deep_capture_current_source_backed_records"] == 2
    assert census["totals"]["deep_capture_historical_audit_only_records"] == 2
    assert census["totals"]["deep_capture_current_completion_markers"] == 1
    assert census["totals"]["deep_capture_historical_audit_only_completion_markers"] == 1
    assert len(census["audit_only_residuals"]) == 3
    marker_state = next(
        state for state in census["lane_states"] if state["lane"] == DEEP_CAPTURE_SET_LANE
    )
    for lane in (AUDIENCE_COMMENTS_LANE, REEL_TRANSCRIPT_LANE, DEEP_CAPTURE_SET_LANE):
        state = next(entry for entry in census["lane_states"] if entry["lane"] == lane)
        assert state["eligible_capture_packets"] == 2
        assert state["failed_eligible_capture_packets"] == 1
    assert marker_state["current_source_backed_record_count"] == 1
    assert marker_state["historical_audit_only_record_count"] == 1


def _manifest(
    root: DataLakeRoot,
    packet_id: str,
    family: str,
    surface: str,
    *,
    failed: bool = False,
) -> None:
    container = root.path / "raw" / raw_shard(packet_id) / packet_id
    container.mkdir(parents=True)
    body = (f"census fixture {packet_id}").encode()
    evidence = container / "raw" / "evidence.json"
    evidence.parent.mkdir()
    evidence.write_bytes(body)
    (container / "manifest.json").write_text(
        json.dumps(
            {
                "packet_id": packet_id,
                "source_family": family,
                "source_surface": surface,
                "access_posture": {
                    "status": "known",
                    "value": "access_failed with HTTP 403" if failed else "capture succeeded",
                    "reason": None,
                },
                "timing": {"capture_time": {"status": "known", "value": OBSERVED_AT}},
                "preserved_files": [
                    {
                        "file_id": "file_01",
                        "relative_packet_path": "raw/evidence.json",
                        "size_bytes": len(body),
                        "sha256": hashlib.sha256(body).hexdigest(),
                        "hash_basis": "raw_stored_bytes",
                    }
                ],
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )


def _entity(kind: str, native_id: str) -> dict:
    return {
        "ref_type": "entity_key",
        "ref": {"namespace": "tiktok", "kind": kind, "native_id": native_id},
    }


def _record(
    record_id: str,
    lane: str,
    payload_kind: str,
    observation: dict,
    *,
    producer_schema: str = "test_v0",
    provenance: dict | None = None,
) -> dict:
    record = {
        "record_id": record_id,
        "raw_anchor": PACKET,
        "lane_namespace": lane,
        "producer_id": "test.silver_census",
        "schema_version": "silver_vault_record_v0",
        "producer_schema_version": producer_schema,
        "record_kind": "observation",
        "payload_kind": payload_kind,
        "producer_row_kind": "test_row",
        "source_family": "tiktok" if "tiktok" in lane or "social_metric" in lane else "fragrance_native_database",
        "source_surface": "test_surface",
        "observed_at": OBSERVED_AT,
        "captured_at": OBSERVED_AT,
        "raw_refs": [
            {
                "ref_type": "raw_packet",
                "packet_id": PACKET,
                "file_id": "file_01",
                "relative_packet_path": "raw/evidence.json",
                "sha256": hashlib.sha256(f"census fixture {PACKET}".encode()).hexdigest(),
                "hash_basis": "raw_stored_bytes",
            }
        ],
        "derived_refs": [],
        "content_hash": "",
        "content_hash_basis": "canonical_json_excluding_content_hash",
        "payload": {"observation": observation},
    }
    if provenance is not None:
        record["provenance"] = provenance
    record["content_hash"] = f"sha256:{silver_content_hash(record)}"
    return record


def _append(root: DataLakeRoot, record: dict) -> None:
    append_silver_record(
        root,
        raw_anchor=record["raw_anchor"],
        lane=record["lane_namespace"],
        record_id=record["record_id"],
        record=record,
    )


def _cell(kind: str, value: int | None = None) -> dict:
    return {
        "metric_value": value,
        "metric_posture": {
            "kind": kind,
            "reason_code": None if kind == "observed" else f"test_{kind}",
            "reason_detail": None,
        },
        "unit": "count",
        "source_field": "fixture",
    }


def _grid() -> dict:
    rows = []
    for index in range(30):
        metrics = {f"metric_{number}": _cell("observed", number) for number in range(5)}
        metrics["missing"] = _cell("unavailable_with_reason")
        metrics["skipped"] = _cell("not_attempted")
        rows.append({"subject": _entity("public_content_object", f"video-{index}"), "metrics": metrics})
    return {
        "subject": _entity("platform_public_account", "creator"),
        "observation_set_kind": "social_content_metric_grid",
        "platform": "tiktok",
        "policy_version": "grid_policy_v1",
        "policy_fingerprint_sha256": "a" * 64,
        "row_count": len(rows),
        "coverage_window": {"start": OBSERVED_AT, "end": OBSERVED_AT},
        "rows": rows,
    }


def _vote(metric: str, value: int) -> dict:
    return {
        "subject": {"review_handle_id": f"review-{metric}-{value}"},
        "metric_name": metric,
        "metric_value": value,
        "metric_posture": {"kind": "observed", "reason_code": None, "reason_detail": None},
    }


def test_census_is_deterministic_reconciled_and_counts_observation_units(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test((tmp_path / "lake").resolve())
    _manifest(root, PACKET, "tiktok", "tiktok_creator_batch_comment_subtitle_admission")
    _manifest(
        root,
        PARFUMO_PACKET,
        "fragrance_native_database",
        "parfumo_product_page_direct_http",
        failed=True,
    )
    _append(root, _record("grid.json", "social_metric_observation_set_silver", "MetricObservationSet", _grid()))
    for record_id, metric, value, current in (
        ("old-zero.json", "review_sillage_vote", 0, False),
        ("old-valid.json", "review_sillage_vote", 4, False),
        ("current-valid.json", "review_rating", 5, True),
    ):
        _append(
            root,
            _record(
                record_id,
                "cleaning_fragrantica_silver",
                "MetricObservation",
                _vote(metric, value),
                producer_schema="fragrantica_cleaning_silver_metricobservation_v3" if current else "fragrantica_cleaning_silver_metricobservation_v0",
                provenance={"review_vote_policy_version": FRAGRANTICA_REVIEW_VOTE_POLICY_VERSION} if current else {},
            ),
        )
    _append(
        root,
        _record(
            "ratio.json",
            "tiktok_comment_attention_silver",
            "MetricObservation",
            {
                "subject": _entity("public_comment", "comment-1"),
                "metric_name": "comment_like_to_video_like_ratio",
                "metric_value": 0.25,
                "metric_posture": {"kind": "observed", "reason_code": None, "reason_detail": None},
                "numerator": {"metric_value": 1},
                "denominator": {"metric_value": 4},
            },
            provenance={"calculation_recipe_version": "ratio_v1"},
        ),
    )
    _append(
        root,
        _record(
            "rollup.json",
            "creator_metric_rollup_silver",
            "MetricRollupObservation",
            {
                "subject": _entity("platform_public_account", "creator"),
                "rollup_window": "custom",
                "metric_rollups": {
                    "average": _cell("observed", 10),
                    "median": _cell("observed", 8),
                    "missing": _cell("unavailable_with_reason"),
                    "skipped": _cell("not_attempted"),
                },
            },
        ),
    )
    text = "one review"
    _append(
        root,
        _record(
            "text.json",
            "cleaning_fragrantica_silver",
            "TextObservation",
            {
                "subject": {"review_handle_id": "review-text"},
                "text_artifact_type": "review_body",
                "text_value": text,
                "text_ref": None,
                "text_hash": f"sha256:{hashlib.sha256(text.encode()).hexdigest()}",
                "text_posture": {"kind": "observed", "reason_code": None, "reason_detail": None},
            },
        ),
    )

    first = build_silver_observation_census(root)
    assert first == build_silver_observation_census(root)
    totals = first["totals"]
    assert totals["capture_packets"] == 2
    assert totals["silver_records"] == 7
    assert totals["content_observations"] == 30
    assert totals["directly_observed_atomic_metric_values"] == 152
    assert totals["current_policy_qualified_direct_metric_values"] == 151
    assert totals["text_observations"] == 1
    assert totals["derived_analytical_values"] == 3
    assert totals["unavailable_with_reason_states"] == 31
    assert totals["not_attempted_states"] == 31
    assert totals["excluded_invalid_observed_metric_values"] == 1
    assert totals["historical_unqualified_metric_values"] == 2
    assert all(first["reconciliation"].values())
    states = {entry["lane"]: entry["state"] for entry in first["lane_states"]}
    assert states["cleaning_fragrantica_silver"] == "populated"
    assert states["cleaning_basenotes_silver"] == "no_applicable_source"
    assert states["cleaning_parfumo_silver"] == "failed"
    assert states["transcript_product_mentions_silver"] == "pending_backlog"
    assert states["tiktok_audience_evidence_silver"] == "retired"
    assert states["silver__cleaning__product_mentions"] == "retired"


def test_relationship_records_count_as_edges_not_unclassified(tmp_path: Path) -> None:
    """A valid relationship-kind Silver record (the raw-packet tombstone shape)
    is counted as a relationship edge, never as an unclassified observation."""
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    retained = "01KW2MJM01Y0936VNECWB3MHSH"
    tombstoned = "01KW2MJM01Y0936VNECWB3MHSJ"
    _manifest(root, retained, "tiktok", "tiktok_creator_batch_comment_subtitle_admission")
    _manifest(root, tombstoned, "tiktok", "tiktok_creator_batch_comment_subtitle_admission")

    append_raw_packet_tombstone(
        root,
        retained_packet_id=retained,
        tombstoned_packet_id=tombstoned,
        captured_at=OBSERVED_AT,
        reason="census relationship-arm fixture",
    )
    census = build_silver_observation_census(root)

    assert census["totals"]["silver_records"] == 1
    assert census["totals"]["relationship_edge_records"] == 1
    assert census["totals"]["unclassified_silver_records"] == 0
    assert census["totals"]["current_source_backed_silver_records"] == 1
    assert census["errors"] == []


def test_duplicate_unit_is_suppressed_but_both_files_remain_stored(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test((tmp_path / "lake").resolve())
    _manifest(root, PACKET, "tiktok", "tiktok_creator_grid_window")
    observation = {
        "subject": _entity("public_content_object", "video-1"),
        "metric_name": "view_count",
        "metric_value": 10,
        "metric_posture": {"kind": "observed", "reason_code": None, "reason_detail": None},
    }
    for record_id in ("first.json", "duplicate.json"):
        _append(root, _record(record_id, "creator_metric_silver", "MetricObservation", observation))
    totals = build_silver_observation_census(root)["totals"]
    assert totals["silver_records"] == 2
    assert totals["directly_observed_atomic_metric_values"] == 1
    assert totals["duplicate_observation_units_suppressed"] == 1


def test_deep_capture_record_citing_another_packet_cannot_inflate_current_totals(
    tmp_path: Path,
) -> None:
    """Cross-anchor refs resolve and hash-verify, but they are another packet's.

    The census headline says these records are *current source-backed* for their
    own anchor, so physical resolution alone is not enough to be counted.
    """
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first = _write_deep_capture(root, "ReelOne", "c1", b"audio-one")
    second = _write_deep_capture(root, "ReelTwo", "c2", b"audio-two")
    assert first.packet_id != second.packet_id

    donor = json.loads(second[AUDIENCE_COMMENTS_LANE].read_text(encoding="utf-8"))
    victim_path = first[AUDIENCE_COMMENTS_LANE]
    record = json.loads(victim_path.read_text(encoding="utf-8"))
    record["raw_refs"] = donor["raw_refs"]
    record["content_hash"] = f"sha256:{silver_content_hash(record)}"
    victim_path.write_text(json.dumps(record), encoding="utf-8")

    census = build_silver_observation_census(root)

    # The transcript sibling of packet one plus both of packet two stay current;
    # only the cross-anchor comments record is demoted.
    assert census["totals"]["deep_capture_current_source_backed_records"] == 3
    assert any(
        error["kind"] == "deep_capture_source_ref_unresolved" for error in census["errors"]
    )


def test_unresolved_record_is_named_and_cannot_inflate_observation_totals(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test((tmp_path / "lake").resolve())
    _manifest(root, PACKET, "tiktok", "tiktok_creator_grid_window")
    record = _record(
        "unresolved.json",
        "creator_metric_silver",
        "MetricObservation",
        {
            "subject": _entity("public_content_object", "video-1"),
            "metric_name": "view_count",
            "metric_value": 10,
            "metric_posture": {
                "kind": "observed",
                "reason_code": None,
                "reason_detail": None,
            },
        },
    )
    record["raw_refs"][0]["packet_id"] = "01J00000000000000000000004"
    record["content_hash"] = f"sha256:{silver_content_hash(record)}"
    path = root.record_path(
        subtree="derived",
        raw_anchor=PACKET,
        lane=record["lane_namespace"],
        record_id=record["record_id"],
    )
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(record), encoding="utf-8")

    census = build_silver_observation_census(root)

    assert census["totals"]["silver_records"] == 1
    assert census["totals"]["directly_observed_atomic_metric_values"] == 0
    assert census["totals"]["unclassified_silver_records"] == 1
    assert census["errors"][0]["kind"] == "silver_record_source_unresolved"
