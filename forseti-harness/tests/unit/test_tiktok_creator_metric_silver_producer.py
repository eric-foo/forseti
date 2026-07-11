"""Unit tests for the TikTok creator-metric Silver producer and the TikTok
recipe branch of the rollup formula revalidator.

End-to-end against ``DataLakeRoot.for_test`` with real-shape batch packets
(fixture helper shared with the seed builder tests): records appended through
the sanctioned Silver writer, engagement math pinned with hand-computed values,
posture/value coupling preserved for gap observations, derived_refs lineage
intact, and the independent revalidation recompute both passing clean and
catching a tampered stored value. The content hash is re-implemented locally
(not imported from the producer) so a producer-side hash bug cannot validate
itself.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from capture_spine.creator_profile_current.rollup_formula_revalidation import (
    revalidate_creator_metric_rollups,
)
from capture_spine.creator_profile_current.silver_subject_ref import (
    FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY,
    LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY,
)
from capture_spine.creator_profile_current.tiktok_metric_seed import (
    build_tiktok_batch_creator_metric_seed_document,
)
from capture_spine.creator_profile_current.tiktok_silver_metric_producer import (
    METRIC_OBSERVATION_LANE,
    METRIC_OBSERVATION_PAYLOAD_KIND,
    METRIC_ROLLUP_LANE,
    METRIC_ROLLUP_PAYLOAD_KIND,
    TiktokCreatorMetricSilverResult,
    build_metric_rollup_record,
    derive_tiktok_creator_metric_silver_records_from_seed,
)
from data_lake.canonical_json import canonical_record_bytes
from data_lake.root import DataLakeRoot
from test_tiktok_creator_metric_seed import (
    ACCOUNT_MAP,
    CAPTURE_T1,
    GENERATED_AT,
    _commit_batch_packet,
    _stats,
    _video,
)


def _content_hash(record: dict) -> str:
    canonical = dict(record)
    canonical.pop("content_hash", None)
    return hashlib.sha256(
        json.dumps(
            canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    ).hexdigest()


def _produced_lake(tmp_path: Path) -> tuple[DataLakeRoot, str, TiktokCreatorMetricSilverResult]:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _commit_batch_packet(
        data_root,
        videos=[
            _video("7655162561783975199", stats=_stats(10800, 1625, 96, share=29, collect=163)),
            _video("7655162561783975200", stats=_stats(43000, 5936, 228, share=175, collect=1492)),
        ],
    )
    document = build_tiktok_batch_creator_metric_seed_document(
        data_root, account_id_by_handle=ACCOUNT_MAP, generated_at_utc=GENERATED_AT
    )
    result = derive_tiktok_creator_metric_silver_records_from_seed(
        data_root=data_root, seed_document=document
    )
    return data_root, packet_id, result


def test_derive_appends_observation_and_rollup_silver_records(tmp_path: Path) -> None:
    data_root, packet_id, result = _produced_lake(tmp_path)

    assert len(result.observation_records) == 10  # 2 videos x 5 named metrics
    assert len(result.rollup_records) == 1
    for record, path in zip(result.observation_records, result.observation_paths, strict=True):
        assert record["lane_namespace"] == METRIC_OBSERVATION_LANE
        assert record["payload_kind"] == METRIC_OBSERVATION_PAYLOAD_KIND
        assert record["raw_anchor"] == packet_id
        assert record["source_family"] == "social_media"
        assert record["source_surface"] == "tiktok_creator_batch_comment_subtitle_admission"
        assert record["content_hash"] == f"sha256:{_content_hash(record)}"
        on_disk = json.loads(path.read_text(encoding="utf-8"))
        assert on_disk == record
        assert METRIC_OBSERVATION_LANE in str(path)

    rollup = result.rollup_records[0]
    assert rollup["lane_namespace"] == METRIC_ROLLUP_LANE
    assert rollup["payload_kind"] == METRIC_ROLLUP_PAYLOAD_KIND
    assert rollup["raw_anchor"] == packet_id  # single-batch-packet anchor, the IG shape
    assert rollup["content_hash"] == f"sha256:{_content_hash(rollup)}"

    # Subject shapes: per-video content objects published by the handle account.
    view = next(
        record
        for record in result.observation_records
        if record["payload"]["observation"]["metric_name"] == "view_count"
    )
    ref = view["payload"]["observation"]["subject"]["ref"]
    assert ref["namespace"] == "tiktok"
    assert ref["kind"] == "public_content_object"
    assert ref["native_id_kind"] == "tiktok_video_id"
    assert ref["published_by_account_native_id"] == "funmimonet"
    assert ref[FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY] == "acct_tt_funmimonet"
    assert LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY not in ref
    raw_ref = view["raw_refs"][0]
    assert raw_ref["packet_id"] == packet_id
    assert raw_ref["json_pointer"].endswith("/stats/playCount")
    assert raw_ref["sha256"]

    rollup_ref = rollup["payload"]["observation"]["subject"]["ref"]
    assert rollup_ref["kind"] == "platform_public_account"
    assert rollup_ref["native_id"] == "funmimonet"
    assert rollup_ref[FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY] == "acct_tt_funmimonet"
    assert LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY not in rollup_ref


def test_rollup_engagement_math_and_derived_refs_lineage(tmp_path: Path) -> None:
    _data_root, _packet_id, result = _produced_lake(tmp_path)
    rollup = result.rollup_records[0]
    observation = rollup["payload"]["observation"]
    metrics = observation["metric_rollups"]

    # Hand-computed: (1625 + 5936 + 96 + 228) / (10800 + 43000) = 7885 / 53800.
    assert metrics["engagement_rate"]["metric_value"] == 0.146561
    assert metrics["engagement_rate"]["metric_posture"]["kind"] == "observed"
    assert metrics["average_views"]["metric_value"] == 26900.0
    assert metrics["average_like_count"]["metric_value"] == 3780.5
    assert metrics["average_comment_count"]["metric_value"] == 162.0
    assert observation["view_count_min"] == 10800
    assert observation["view_count_max"] == 43000
    assert observation["computed_at"] == GENERATED_AT
    assert observation["calculation_recipe_version"] == (
        "creator_metric_rollup_tiktok_profile_grid_engagement_v0"
    )

    # derived_refs resolve to the appended observation records by id AND hash.
    observation_by_record_id = {
        record["record_id"]: record for record in result.observation_records
    }
    assert len(rollup["derived_refs"]) == observation["observation_count"] == 6
    for edge in rollup["derived_refs"]:
        source = observation_by_record_id[edge["record_id"]]
        assert edge["content_hash"] == source["content_hash"]
        assert edge["lane_namespace"] == METRIC_OBSERVATION_LANE
        # Only the engagement trio feeds the rollup lineage.
        assert source["payload"]["observation"]["metric_name"] in {
            "view_count",
            "like_count",
            "total_comment_count",
        }
    assert "not buyer proof" in rollup["non_claims"]


def test_gap_observation_keeps_posture_value_coupling(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    gap_stats = _stats(5000, 250, 50)
    del gap_stats["diggCount"]
    _commit_batch_packet(
        data_root,
        videos=[
            _video("7655162561783975199", stats=_stats(10800, 1625, 96)),
            _video("7655162561783975201", stats=gap_stats),
        ],
    )
    document = build_tiktok_batch_creator_metric_seed_document(
        data_root, account_id_by_handle=ACCOUNT_MAP, generated_at_utc=GENERATED_AT
    )
    result = derive_tiktok_creator_metric_silver_records_from_seed(
        data_root=data_root, seed_document=document
    )
    gap_records = [
        record
        for record in result.observation_records
        if record["payload"]["observation"]["metric_posture"]["kind"] == "unavailable_with_reason"
    ]
    assert len(gap_records) == 1
    gap = gap_records[0]["payload"]["observation"]
    assert gap["metric_name"] == "like_count"
    assert gap["metric_value"] is None
    assert "never zero-filled" in gap["metric_posture"]["reason_detail"]
    observed = [
        record
        for record in result.observation_records
        if record["payload"]["observation"]["metric_posture"]["kind"] == "observed"
    ]
    assert all(
        isinstance(record["payload"]["observation"]["metric_value"], int) for record in observed
    )


def test_rollup_referencing_unknown_observation_fails_closed() -> None:
    seed_rollup = {
        "metric_rollup_id": "tiktok_batch_account_engagement_rollup_v0_001",
        "source_metric_observation_ids": ["tiktok_batch_metric_obs_v0_999"],
    }
    with pytest.raises(ValueError, match="unknown source observation id"):
        build_metric_rollup_record(
            seed_rollup=seed_rollup, ref_by_seed_observation_id={}, raw_anchor="01FAKEANCHOR"
        )


def test_revalidation_recomputes_tiktok_recipe_clean(tmp_path: Path) -> None:
    data_root, _packet_id, _result = _produced_lake(tmp_path)
    report = revalidate_creator_metric_rollups(data_root, platform="tiktok")
    assert report.rollups_checked == 1
    assert report.ok, [finding.failures for finding in report.findings]


def test_revalidation_detects_tampered_engagement_rate(tmp_path: Path) -> None:
    data_root, _packet_id, result = _produced_lake(tmp_path)
    rollup_path = result.rollup_paths[0]
    record = json.loads(rollup_path.read_text(encoding="utf-8"))
    record["payload"]["observation"]["metric_rollups"]["engagement_rate"]["metric_value"] = 0.5
    # Restamp the content hash so only the FORMULA check can catch the change.
    canonical = dict(record)
    canonical.pop("content_hash", None)
    record["content_hash"] = "sha256:" + hashlib.sha256(
        json.dumps(
            canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    ).hexdigest()
    rollup_path.write_bytes(canonical_record_bytes(record))

    report = revalidate_creator_metric_rollups(data_root, platform="tiktok")
    assert not report.ok
    assert any(
        "engagement_rate" in failure and "recomputed" in failure
        for finding in report.findings
        for failure in finding.failures
    )


def test_revalidation_detects_tampered_observation_integrity(tmp_path: Path) -> None:
    data_root, _packet_id, result = _produced_lake(tmp_path)
    observation_path = result.observation_paths[0]
    record = json.loads(observation_path.read_text(encoding="utf-8"))
    record["payload"]["observation"]["metric_value"] = 999999  # no hash restamp
    observation_path.write_bytes(canonical_record_bytes(record))
    report = revalidate_creator_metric_rollups(data_root, platform="tiktok")
    assert not report.ok
    assert any(
        "content_hash does not reproduce" in failure
        for finding in report.findings
        for failure in finding.failures
    )
