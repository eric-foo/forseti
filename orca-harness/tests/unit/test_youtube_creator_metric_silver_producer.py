"""Unit tests for the YouTube creator-metric Silver Vault producer.

These run the producer against the REAL committed
``youtube_shorts_fragrance_creator_metric_seed_v0.json`` (Option 2 wraps the
committed seed, so no-drift is the strongest possible: the emitted numbers ARE
the committed, already-tested seed numbers) into a temp lake
(``DataLakeRoot.for_test`` -- no external lake drive). They assert the producer
emits Silver Vault-conformant records, reproduces ``content_hash`` independently,
obeys posture/value coupling, threads rollup -> observation lineage via
``derived_refs``, anchors observations to their per-Short packet and rollups to
their account id, and fails closed on a blank subject native_id.
"""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from capture_spine.creator_profile_current.youtube_silver_metric_producer import (
    DEFAULT_YOUTUBE_SEED_PATH,
    METRIC_OBSERVATION_LANE,
    METRIC_OBSERVATION_PAYLOAD_KIND,
    METRIC_ROLLUP_LANE,
    METRIC_ROLLUP_PAYLOAD_KIND,
    YOUTUBE_SEED_WRAPPER_KEY,
    build_metric_observation_record,
    derive_youtube_creator_metric_silver_records_from_seed,
)
from data_lake.catalog import rebuild_catalog
from data_lake.root import DataLakeRoot
from source_capture.youtube_watch_packet import YoutubeWatchFetch, write_youtube_watch_packet

EXPECTED_OBSERVATIONS = 196
EXPECTED_ROLLUPS = 30
YOUTUBE_AR_PROOF_VIDEO_ID = "as7hye0qgYc"
YOUTUBE_AR_PROOF_WATCH_HTML = b"<html>ytInitialPlayerResponse</html>"
YOUTUBE_AR_PROOF_CAPTURED_AT = "2026-06-21T00:00:00Z"


def _content_hash(record: dict) -> str:
    """Independent re-implementation of the canonical content hash (catches a
    producer-side helper mistake instead of trusting it)."""
    canonical = dict(record)
    canonical.pop("content_hash", None)
    payload = json.dumps(
        canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _committed_seed_document() -> dict:
    return json.loads(DEFAULT_YOUTUBE_SEED_PATH.read_text(encoding="utf-8-sig"))


def _metric_observed(value: int, path: str, artifact: str) -> dict:
    return {
        "posture": "observed",
        "value": value,
        "source_route": path.rsplit(".", 1)[0],
        "source_path": path,
        "artifact": artifact,
    }


def _metric_unavailable(reason: str) -> dict:
    return {
        "posture": "unavailable_with_reason",
        "reason": reason,
        "routes_checked": ["youtube_watch_metadata_comments"],
    }


def _youtube_watch_packet(*, view_count: int) -> dict:
    return {
        "video_id": YOUTUBE_AR_PROOF_VIDEO_ID,
        "surface_type": "watch",
        "watch_url": f"https://www.youtube.com/watch?v={YOUTUBE_AR_PROOF_VIDEO_ID}",
        "channel": {"channel_id": "UCzKrJ5NSA9o7RHYRG12kHZw", "author": "JeremyFragrance"},
        "metadata": {
            "title": "UNIQUE BLUE, By SUPERZ",
            "length_seconds": 42,
            "publish_date": "2026-06-20",
        },
        "engagement": {
            "view_count": view_count,
            "view_count_source_path": "player.microformat",
            "like_count": 34,
        },
        "availability": {"video_state": "playable", "comments_state": "comments_not_exposed"},
        "metric_receipts": {
            "view_count": _metric_observed(
                view_count, "ytInitialPlayerResponse.videoDetails.viewCount", "raw_watch.html"
            ),
            "like_count": _metric_observed(
                34,
                "ytInitialPlayerResponse.microformat.playerMicroformatRenderer.likeCount",
                "raw_watch.html",
            ),
            "comment_sample_count": _metric_unavailable("comments not exposed in AR proof fixture"),
            "total_comment_count": _metric_unavailable("comments not exposed in AR proof fixture"),
        },
        "comments_posture": "comments_not_exposed",
        "comments": [],
        "receipts": {"http_status": 200, "retrieval_time_utc": YOUTUBE_AR_PROOF_CAPTURED_AT},
    }


def _commit_youtube_watch_packet(data_root: DataLakeRoot, *, view_count: int) -> tuple[str, dict]:
    code, output_dir = write_youtube_watch_packet(
        YoutubeWatchFetch(
            video_id=YOUTUBE_AR_PROOF_VIDEO_ID,
            raw_watch_html=YOUTUBE_AR_PROOF_WATCH_HTML,
            packet=_youtube_watch_packet(view_count=view_count),
        ),
        data_root=data_root,
        decision_question="creator metric YT AR-backed raw refs",
        now_iso=YOUTUBE_AR_PROOF_CAPTURED_AT,
    )
    assert code == 0
    packet_id = Path(output_dir).name
    preserved = data_root.load_raw_packet(packet_id).manifest["preserved_files"][0]
    assert preserved["relative_packet_path"].endswith("raw_watch.html")
    return packet_id, preserved


def _single_observation_seed_document(*, packet_id: str, watch_hash: str, view_count: int) -> dict:
    seed_document = _committed_seed_document()
    seed = deepcopy(seed_document[YOUTUBE_SEED_WRAPPER_KEY])
    seed_observation = deepcopy(seed["metric_observations"][0])
    seed_observation.update(
        {
            "source_packet_id_or_none": packet_id,
            "source_packet_pointer_or_none": None,
            "source_watch_html_sha256_or_none": watch_hash,
            "source_watch_byte_size_or_none": len(YOUTUBE_AR_PROOF_WATCH_HTML),
            "source_pointer": "youtube_watch_packet_fixture#/metric_receipts/view_count",
            "source_field": "/metric_receipts/view_count/value",
            "source_file": "youtube_watch_packet_fixture",
            "source_row_id_or_none": "fixture:youtube_watch_packet:view_count",
            "metric_value_or_none": view_count,
            "observed_at": YOUTUBE_AR_PROOF_CAPTURED_AT,
        }
    )
    rollup = deepcopy(
        next(
            item
            for item in seed["metric_rollups"]
            if seed_observation["metric_observation_id"] in item["source_metric_observation_ids"]
        )
    )
    rollup.update(
        {
            "profile_subject_id": seed_observation["platform_account_id"],
            "platform_account_ids": [seed_observation["platform_account_id"]],
            "platform_subject_key": seed_observation["platform_subject_key"],
            "platform_subject_key_type": seed_observation["platform_subject_key_type"],
            "source_metric_observation_ids": [seed_observation["metric_observation_id"]],
            "observation_count": 1,
            "view_count_min": view_count,
            "view_count_max": view_count,
            "computed_at": YOUTUBE_AR_PROOF_CAPTURED_AT,
        }
    )
    rollup["metric_rollups"]["average_views"]["value_or_none"] = float(view_count)
    rollup["metric_rollups"]["median_views"]["value_or_none"] = float(view_count)
    rollup["sample_support"] = {
        "observation_count": 1,
        "sample_adequacy": "thin_n_1_to_3",
        "representativeness_posture": "admitted_pool_only_not_representative_creator_average",
        "surface_handling": "downgrade_or_withhold_summary_claim",
    }
    seed["metric_observations"] = [seed_observation]
    seed["metric_rollups"] = [rollup]
    seed_document[YOUTUBE_SEED_WRAPPER_KEY] = seed
    return seed_document


def _run(tmp_path: Path):
    seed_document = _committed_seed_document()
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    result = derive_youtube_creator_metric_silver_records_from_seed(
        data_root=data_root, seed_document=seed_document
    )
    return result, seed_document[YOUTUBE_SEED_WRAPPER_KEY]


def test_producer_emits_conformant_metric_observation_records(tmp_path: Path) -> None:
    result, seed = _run(tmp_path)
    assert len(result.observation_records) == EXPECTED_OBSERVATIONS == len(seed["metric_observations"])

    seed_by_id = {o["metric_observation_id"]: o for o in seed["metric_observations"]}
    emitted_seed_ids = [r["provenance"]["seed_metric_observation_id"] for r in result.observation_records]
    assert set(emitted_seed_ids) == set(seed_by_id)
    assert len(emitted_seed_ids) == len(set(emitted_seed_ids)) == EXPECTED_OBSERVATIONS
    for record in result.observation_records:
        assert record["schema_version"] == "silver_vault_record_v0"
        assert record["record_kind"] == "observation"
        assert record["payload_kind"] == METRIC_OBSERVATION_PAYLOAD_KIND
        assert record["lane_namespace"] == METRIC_OBSERVATION_LANE
        assert record["content_hash_basis"] == "canonical_json_excluding_content_hash"
        assert record["source_family"] == "social_media"
        assert record["source_surface"] == "youtube_shorts"
        # content_hash reproduces independently from the record's own content.
        assert record["content_hash"] == f"sha256:{_content_hash(record)}"

        seed_obs = seed_by_id[record["provenance"]["seed_metric_observation_id"]]
        # Observation anchors to its own per-Short raw packet id (mirrors IG).
        assert record["raw_anchor"] == seed_obs["source_packet_id_or_none"]

        # raw_refs are honest YouTube provenance (no IG-style raw_anchor dict),
        # carrying sha256 + hash_basis per the Silver Vault raw_refs rule.
        raw_ref = record["raw_refs"][0]
        assert raw_ref["packet_id"] == seed_obs["source_packet_id_or_none"]
        assert raw_ref["source_pointer"] == seed_obs["source_pointer"]
        assert raw_ref["source_field"] == seed_obs["source_field"]
        assert raw_ref["sha256"] == seed_obs["source_watch_html_sha256_or_none"]
        assert raw_ref["sha256"]
        assert raw_ref["hash_basis"] == "source_captured_watch_html_sha256"

        observation = record["payload"]["observation"]
        # Subject is the public content object keyed by stable ids only.
        subject_ref = observation["subject"]["ref"]
        assert observation["subject"]["ref_type"] == "entity_key"
        assert subject_ref["namespace"] == "youtube"
        assert subject_ref["kind"] == "public_content_object"
        assert subject_ref["native_id"] == seed_obs["content_id_or_none"]
        assert subject_ref["published_by_account_native_id"] == seed_obs["platform_subject_key"]
        assert subject_ref["orca_platform_account_id"] == seed_obs["platform_account_id"]

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
    view_count = 479
    packet_id, preserved = _commit_youtube_watch_packet(data_root, view_count=view_count)
    assert rebuild_catalog(data_root)["status"] == "rebuilt"
    seed_document = _single_observation_seed_document(
        packet_id=packet_id, watch_hash=preserved["sha256"], view_count=view_count
    )

    result = derive_youtube_creator_metric_silver_records_from_seed(
        data_root=data_root,
        seed_document=seed_document,
        use_bronze_attachment_records=True,
    )

    assert len(result.observation_records) == 1
    record = result.observation_records[0]
    raw_ref = record["raw_refs"][0]
    assert raw_ref["raw_ref_kind"] == "bronze_attachment_record"
    assert raw_ref["attachment_record_id"].startswith("ar_")
    assert raw_ref["attachment_record_schema_version"] == "bronze_attachment_record_v0_schema_2"
    assert raw_ref["attachment_record_physicalization"] == "manifest_equivalent_entry_over_raw_packet_body_v0"
    assert raw_ref["packet_id"] == packet_id
    assert raw_ref["file_id"] == preserved["file_id"]
    assert raw_ref["relative_packet_path"] == preserved["relative_packet_path"]
    assert raw_ref["body_sha256"] == preserved["sha256"]
    assert raw_ref["sha256"] == preserved["sha256"]
    assert raw_ref["hash_basis"] == "raw_stored_bytes"
    assert raw_ref["body_ref"] == {
        "kind": "raw_packet_relative_path",
        "packet_id": packet_id,
        "file_id": preserved["file_id"],
        "relative_packet_path": preserved["relative_packet_path"],
        "body_sha256": preserved["sha256"],
        "hash_basis": "raw_stored_bytes",
    }
    assert raw_ref["source_family"] == "youtube"
    assert raw_ref["source_surface"] == "youtube_watch_metadata_comments"
    assert raw_ref["payload_kind"] == "html_body"
    assert "lineage_limitations" not in record


def test_missing_bronze_attachment_record_stays_visible_when_requested(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    assert rebuild_catalog(data_root)["status"] == "rebuilt"
    seed_document = _single_observation_seed_document(
        packet_id="01KWYTARPROOFFALLBACK0001", watch_hash="f" * 64, view_count=479
    )

    result = derive_youtube_creator_metric_silver_records_from_seed(
        data_root=data_root,
        seed_document=seed_document,
        use_bronze_attachment_records=True,
    )

    raw_ref = result.observation_records[0]["raw_refs"][0]
    assert raw_ref["raw_ref_kind"] == "raw_packet_fallback_missing_attachment_record"
    assert raw_ref["typed_attachment_record_status"] == "missing"
    assert raw_ref["attachment_record_residual"] == "typed_attachment_record_missing_for_raw_ref"
    assert result.observation_records[0]["lineage_limitations"] == [
        {"reason": "other", "detail": "typed_attachment_record_missing_for_raw_ref"}
    ]


def test_ambiguous_bronze_attachment_record_stays_visible_when_requested(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    view_count = 479
    packet_id, preserved = _commit_youtube_watch_packet(data_root, view_count=view_count)
    seed_document = _single_observation_seed_document(
        packet_id=packet_id, watch_hash=preserved["sha256"], view_count=view_count
    )
    seed_observation = seed_document[YOUTUBE_SEED_WRAPPER_KEY]["metric_observations"][0]
    ambiguous_candidates = [
        {"attachment_record_id": "ar_candidate_1"},
        {"attachment_record_id": "ar_candidate_2"},
    ]

    record = build_metric_observation_record(
        seed_observation=seed_observation,
        bronze_attachment_records_by_packet_body_hash={
            (packet_id, preserved["sha256"]): ambiguous_candidates
        },
        use_bronze_attachment_records=True,
    )

    raw_ref = record["raw_refs"][0]
    assert raw_ref["raw_ref_kind"] == "raw_packet_fallback_ambiguous_attachment_record"
    assert raw_ref["typed_attachment_record_status"] == "ambiguous"
    assert raw_ref["attachment_record_residual"] == "typed_attachment_record_ambiguous_for_raw_ref"
    assert raw_ref["packet_id"] == packet_id
    assert raw_ref["sha256"] == preserved["sha256"]
    assert record["lineage_limitations"] == [
        {"reason": "other", "detail": "typed_attachment_record_ambiguous_for_raw_ref"}
    ]

def test_observation_no_drift_against_committed_seed(tmp_path: Path) -> None:
    result, seed = _run(tmp_path)
    seed_by_id = {o["metric_observation_id"]: o for o in seed["metric_observations"]}
    for record in result.observation_records:
        seed_obs = seed_by_id[record["provenance"]["seed_metric_observation_id"]]
        observation = record["payload"]["observation"]
        # No-drift: the emitted number equals the committed seed observation.
        assert observation["metric_value"] == seed_obs["metric_value_or_none"]
        assert observation["metric_name"] == seed_obs["metric_name"]
        assert observation["unit"] == seed_obs["metric_unit"]
        # No-drift on posture too (decision-bearing: observed vs unavailable vs not_attempted).
        assert observation["metric_posture"]["kind"] == seed_obs["metric_posture"]
        assert observation["metric_posture"]["reason_detail"] == seed_obs["posture_reason_or_none"]


def test_observation_records_written_and_reload_with_stable_hash(tmp_path: Path) -> None:
    result, _ = _run(tmp_path)
    assert len(result.observation_paths) == len(result.observation_records) == EXPECTED_OBSERVATIONS
    # Spot-check the first/last 5 reload with a self-reproducing hash (full set is
    # already covered by the conformance test; this proves the bytes-on-disk path).
    sample = result.observation_records[:5] + result.observation_records[-5:]
    sample_paths = result.observation_paths[:5] + result.observation_paths[-5:]
    for record, path in zip(sample, sample_paths, strict=True):
        assert path.exists()
        on_disk = json.loads(path.read_text(encoding="utf-8"))
        assert on_disk["record_id"] == record["record_id"]
        assert on_disk["content_hash"] == f"sha256:{_content_hash(on_disk)}"


def test_rollup_records_lineage_and_no_drift(tmp_path: Path) -> None:
    result, seed = _run(tmp_path)
    assert len(result.rollup_records) == EXPECTED_ROLLUPS == len(seed["metric_rollups"])

    seed_by_id = {r["metric_rollup_id"]: r for r in seed["metric_rollups"]}
    observations_by_record_id = {r["record_id"]: r for r in result.observation_records}
    record_id_by_seed_obs_id = {
        r["provenance"]["seed_metric_observation_id"]: r["record_id"]
        for r in result.observation_records
    }
    emitted_rollup_ids = [r["provenance"]["seed_metric_rollup_id"] for r in result.rollup_records]
    assert set(emitted_rollup_ids) == set(seed_by_id)
    assert len(emitted_rollup_ids) == len(set(emitted_rollup_ids)) == EXPECTED_ROLLUPS

    for rollup in result.rollup_records:
        assert rollup["record_kind"] == "observation"
        assert rollup["payload_kind"] == METRIC_ROLLUP_PAYLOAD_KIND
        assert rollup["lane_namespace"] == METRIC_ROLLUP_LANE
        assert rollup["content_hash"] == f"sha256:{_content_hash(rollup)}"

        seed_rollup = seed_by_id[rollup["provenance"]["seed_metric_rollup_id"]]
        # Rollup anchors to its declared platform account id (not a single packet).
        assert rollup["raw_anchor"] == seed_rollup["platform_account_ids"][0]

        payload = rollup["payload"]["observation"]
        # derived_refs point at the emitted observation records; hash matches.
        assert len(rollup["derived_refs"]) == len(seed_rollup["source_metric_observation_ids"])
        assert Counter(edge["record_id"] for edge in rollup["derived_refs"]) == Counter(
            record_id_by_seed_obs_id[source_id]
            for source_id in seed_rollup["source_metric_observation_ids"]
        )
        for edge in rollup["derived_refs"]:
            assert edge["edge_type"] == "derived_from_record"
            assert edge["lane_namespace"] == METRIC_OBSERVATION_LANE
            assert edge["content_hash"] == observations_by_record_id[edge["record_id"]]["content_hash"]

        # Mandatory derivation marker (not optional prose).
        assert payload["derivation"] == {
            "kind": "computed_metric_rollup",
            "source_record_ref_kind": "derived_refs",
            "metric_posture_semantics": "source_input_support_not_raw_aggregate_visibility",
            "calculation_recipe_version": seed_rollup["calculation_recipe_version"],
        }

        # No-drift: every rollup number equals the committed seed computation.
        assert payload["observation_count"] == seed_rollup["observation_count"]
        assert payload["view_count_min"] == seed_rollup["view_count_min"]
        assert payload["view_count_max"] == seed_rollup["view_count_max"]
        assert payload["sample_support"] == seed_rollup["sample_support"]
        assert payload["limitations"] == seed_rollup["limitations"]
        for name, seed_metric in seed_rollup["metric_rollups"].items():
            rollup_metric = payload["metric_rollups"][name]
            assert rollup_metric["metric_value"] == seed_metric["value_or_none"]
            assert rollup_metric["unit"] == seed_metric["metric_unit"]
            # No-drift on posture too.
            assert rollup_metric["metric_posture"]["kind"] == seed_metric["posture"]
            assert rollup_metric["metric_posture"]["reason_detail"] == seed_metric.get("posture_reason_or_none")


def test_rollup_metric_posture_value_coupling(tmp_path: Path) -> None:
    result, _ = _run(tmp_path)
    saw_observed = False
    saw_non_observed = False
    for rollup in result.rollup_records:
        for metric in rollup["payload"]["observation"]["metric_rollups"].values():
            posture = metric["metric_posture"]
            if posture["kind"] == "observed":
                saw_observed = True
                assert isinstance(metric["metric_value"], (int, float))
                assert not isinstance(metric["metric_value"], bool)
                assert posture["reason_detail"] is None
            else:
                saw_non_observed = True
                assert metric["metric_value"] is None
                assert posture["reason_detail"]
    # The YouTube seed has both observed (average/median views) and non-observed
    # (engagement_rate/like/comment/cadence/velocity) rollup metrics.
    assert saw_observed and saw_non_observed


def test_observations_anchor_to_distinct_packets_rollups_to_accounts(tmp_path: Path) -> None:
    result, seed = _run(tmp_path)
    # Each observation anchors to its own distinct per-Short packet.
    obs_anchors = [r["raw_anchor"] for r in result.observation_records]
    assert len(set(obs_anchors)) == EXPECTED_OBSERVATIONS
    # Rollups anchor to the 30 distinct account ids (the declared single platform_account_ids entry).
    rollup_anchors = {r["raw_anchor"] for r in result.rollup_records}
    assert all(len(r["platform_account_ids"]) == 1 for r in seed["metric_rollups"])
    assert rollup_anchors == {r["platform_account_ids"][0] for r in seed["metric_rollups"]}
    assert len(rollup_anchors) == EXPECTED_ROLLUPS


def test_content_subject_missing_native_id_fails_closed() -> None:
    seed_document = _committed_seed_document()
    seed_obs = dict(seed_document[YOUTUBE_SEED_WRAPPER_KEY]["metric_observations"][0])
    seed_obs["content_id_or_none"] = None  # blank the content subject native_id
    with pytest.raises(ValueError, match="content subject requires a non-empty entity_key native_id"):
        build_metric_observation_record(seed_observation=seed_obs)


def test_observation_missing_source_packet_fails_closed() -> None:
    seed_document = _committed_seed_document()
    seed_obs = dict(seed_document[YOUTUBE_SEED_WRAPPER_KEY]["metric_observations"][0])
    seed_obs["source_packet_id_or_none"] = None  # remove the source anchor
    with pytest.raises(ValueError, match="lacks a source packet id"):
        build_metric_observation_record(seed_observation=seed_obs)


def test_observation_missing_source_hash_fails_closed() -> None:
    seed_document = _committed_seed_document()
    seed_obs = dict(seed_document[YOUTUBE_SEED_WRAPPER_KEY]["metric_observations"][0])
    seed_obs["source_watch_html_sha256_or_none"] = None
    with pytest.raises(ValueError, match="source_watch_html_sha256_or_none"):
        build_metric_observation_record(seed_observation=seed_obs)


def test_rollup_platform_account_mismatch_fails_closed(tmp_path: Path) -> None:
    # AR-2 hardening: the rollup raw_anchor is the declared single platform_account_ids
    # entry and must equal profile_subject_id; a divergence fails closed.
    seed_document = _committed_seed_document()
    seed_document[YOUTUBE_SEED_WRAPPER_KEY]["metric_rollups"][0]["platform_account_ids"] = ["acct_mismatch"]
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    with pytest.raises(ValueError, match="does not match profile_subject_id"):
        derive_youtube_creator_metric_silver_records_from_seed(
            data_root=data_root, seed_document=seed_document
        )
