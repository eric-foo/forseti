"""Unit tests for the lake-wide rollup formula revalidator.

Green: live watch-packet rollups, a genesis view-count-only rollup (cut from the
real committed seed), and an IG-recipe-shaped rollup all recompute clean.
Red: a tampered rollup value (hash fixed) fails the FORMULA check; a tampered
observation (hash not fixed) fails the INTEGRITY check; a deleted observation
fails lineage resolution; an unknown recipe version is a failure, not a skip.
The red cases are the point -- a validator that cannot fail is ceremony.
"""
from __future__ import annotations

import hashlib
import json
import statistics
from copy import deepcopy
from pathlib import Path

from capture_spine.creator_profile_current.rollup_formula_revalidation import (
    _recompute_ig,
    _recompute_tiktok,
    _SourceRow,
    revalidate_creator_metric_rollups,
)
from capture_spine.creator_profile_current.youtube_silver_metric_producer import (
    DEFAULT_YOUTUBE_SEED_PATH,
    YOUTUBE_SEED_WRAPPER_KEY,
    derive_youtube_creator_metric_silver_records_from_seed,
)
from capture_spine.creator_profile_current.youtube_watch_packet_metric_document import (
    build_youtube_watch_packet_metric_document,
)
from data_lake.canonical_json import canonical_record_bytes
from data_lake.root import DataLakeRoot
from source_capture.youtube_watch_packet import YoutubeWatchFetch, write_youtube_watch_packet

ALPHA_CHANNEL = "UCalphaAlphaAlphaAlpha01"
CAPTURE_T1 = "2026-07-01T10:00:00Z"
RUN_T1 = "2026-07-01T11:00:00Z"
IG_RECIPE = "creator_metric_rollup_instagram_reels_grid_engagement_v0"


def _account_ledger() -> dict:
    return {
        "platform_accounts": [
            {
                "platform_account_id": "acct_yt_alpha",
                "platform": "youtube",
                "platform_public_account_id_or_none": ALPHA_CHANNEL,
                "public_handle": "@alphafrag",
            }
        ]
    }


def _creator_ledger() -> dict:
    return {
        "youtube_creator_observation_ledger": {
            "creator_observations": [
                {
                    "creator_observation_id": "yt_creator_obs_alpha",
                    "platform_subject_key": ALPHA_CHANNEL,
                    "creator_handle_query": "@alphafrag",
                    "creator_classification": "creator_or_channel_observed",
                    "pool_ids": ["yt-frag-pool200-001", "yt-frag-pool200-002"],
                    "video_ids": ["vidAlpha001", "vidAlpha002"],
                }
            ]
        }
    }


def _observed_receipt(value: int) -> dict:
    return {
        "posture": "observed",
        "value": value,
        "source_route": "ytInitialPlayerResponse",
        "source_path": "ytInitialPlayerResponse.videoDetails",
        "artifact": "raw_watch.html",
    }


def _unavailable_receipt(reason: str) -> dict:
    return {
        "posture": "unavailable_with_reason",
        "reason": reason,
        "routes_checked": ["youtube_watch_metadata_comments"],
    }


def _commit_packet(
    data_root: DataLakeRoot, *, video_id: str, view_count: int, like_count: int, comments: int
) -> None:
    packet = {
        "video_id": video_id,
        "surface_type": "watch",
        "watch_url": f"https://www.youtube.com/watch?v={video_id}",
        "canonical_url": f"https://www.youtube.com/watch?v={video_id}",
        "channel": {"channel_id": ALPHA_CHANNEL, "author": "fixture"},
        "metadata": {"title": f"fixture {video_id}", "publish_date": "2026-06-20"},
        "engagement": {
            "view_count": view_count,
            "like_count": like_count,
            "total_comment_count": comments,
        },
        "availability": {"video_state": "playable", "comments_state": "comments_not_exposed"},
        "metric_receipts": {
            "view_count": _observed_receipt(view_count),
            "like_count": _observed_receipt(like_count),
            "total_comment_count": _observed_receipt(comments),
            "comment_sample_count": _unavailable_receipt("comments not sampled in fixture"),
        },
        "comments_posture": "comments_not_exposed",
        "receipts": {"http_status": 200, "retrieval_time_utc": CAPTURE_T1},
    }
    code, _output = write_youtube_watch_packet(
        YoutubeWatchFetch(
            video_id=video_id,
            raw_watch_html=f"<html>{video_id}</html>".encode(),
            packet=packet,
        ),
        data_root=data_root,
        decision_question="rollup formula revalidation test",
        now_iso=CAPTURE_T1,
    )
    assert code == 0


def _live_lake(tmp_path: Path):
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_packet(data_root, video_id="vidAlpha001", view_count=100, like_count=10, comments=5)
    _commit_packet(data_root, video_id="vidAlpha002", view_count=200, like_count=30, comments=15)
    data_root.rebuild_availability()
    document = build_youtube_watch_packet_metric_document(
        data_root,
        creator_ledger=_creator_ledger(),
        account_ledger=_account_ledger(),
        generated_at_utc=RUN_T1,
    )
    result = derive_youtube_creator_metric_silver_records_from_seed(
        data_root=data_root, seed_document=document
    )
    return data_root, result


def _rewrite_record(path: Path, mutate) -> None:
    """Load a lake record, apply ``mutate``, restamp its content_hash so only the
    FORMULA (not integrity) check can catch the change, and write it back."""
    record = json.loads(path.read_text(encoding="utf-8"))
    mutate(record)
    canonical = dict(record)
    canonical.pop("content_hash", None)
    digest = hashlib.sha256(
        json.dumps(
            canonical, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("utf-8")
    ).hexdigest()
    record["content_hash"] = f"sha256:{digest}"
    path.write_bytes(canonical_record_bytes(record))


def test_live_watch_packet_rollups_recompute_clean(tmp_path: Path) -> None:
    data_root, _result = _live_lake(tmp_path)
    report = revalidate_creator_metric_rollups(data_root)
    assert report.rollups_checked == 1
    assert report.ok, [f.failures for f in report.findings]


def test_genesis_seed_rollup_recomputes_clean(tmp_path: Path) -> None:
    seed_document = json.loads(DEFAULT_YOUTUBE_SEED_PATH.read_text(encoding="utf-8-sig"))
    seed = seed_document[YOUTUBE_SEED_WRAPPER_KEY]
    rollup = deepcopy(seed["metric_rollups"][0])
    source_ids = set(rollup["source_metric_observation_ids"])
    seed["metric_rollups"] = [rollup]
    seed["metric_observations"] = [
        deepcopy(obs)
        for obs in seed["metric_observations"]
        if obs["metric_observation_id"] in source_ids
    ]
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    derive_youtube_creator_metric_silver_records_from_seed(
        data_root=data_root, seed_document=seed_document
    )
    report = revalidate_creator_metric_rollups(data_root)
    assert report.rollups_checked == 1
    assert report.ok, [f.failures for f in report.findings]
    assert report.findings[0].recipe_version == (
        "creator_metric_rollup_admitted_youtube_shorts_average_v0"
    )


def test_ig_recipe_branch_recomputes_clean_and_catches_bad_engagement(tmp_path: Path) -> None:
    # Craft an IG-recipe rollup through the Silver envelope path: two complete
    # trios (view/like/comment per content id) -- exercises the IG recompute math.
    views, likes, comments = [100, 300], [10, 20], [4, 6]
    observations = []
    for index, (view, like, comment) in enumerate(zip(views, likes, comments, strict=True)):
        for metric, value in (("view_count", view), ("like_count", like), ("comment_count", comment)):
            observations.append(
                {
                    "metric_observation_id": f"ig_fixture_obs_{index}_{metric}",
                    "platform_account_id": "acct_ig_fixture",
                    "platform_subject_key": "ig_user_fixture",
                    "platform_subject_key_type": "instagram_username",
                    "content_id_or_none": f"reel_{index}",
                    "content_url_or_none": f"https://www.instagram.com/reel/reel_{index}/",
                    "watch_url_or_none": None,
                    "content_kind": "reel",
                    "content_title_or_none": None,
                    "content_publication_or_event_time_or_none": None,
                    "metric_name": metric,
                    "metric_value_or_none": value,
                    "metric_unit": "count",
                    "metric_posture": "observed",
                    "posture_reason_or_none": None,
                    "source_pointer": f"fixture#/rows/{index}/{metric}",
                    "source_field": f"/rows/{index}/{metric}",
                    "source_file": "fixture",
                    "source_row_id_or_none": f"fixture:{index}:{metric}",
                    "source_watch_html_sha256_or_none": "f" * 64,
                    "source_shorts_html_sha256_or_none": None,
                    "source_watch_byte_size_or_none": 10,
                    "source_shorts_byte_size_or_none": None,
                    "source_packet_id_or_none": "01IGFIXTUREPACKET00000001",
                    "source_packet_pointer_or_none": None,
                    "transcript_route_or_none": None,
                    "observed_at": CAPTURE_T1,
                    "observed_at_source": "fixture",
                    "metric_registry_version": "fixture_v0",
                    "limitation_notes": ["fixture"],
                }
            )
    engagement = round((sum(likes) + sum(comments)) / sum(views), 6)
    rollup = {
        "metric_rollup_id": "ig_fixture_rollup_001",
        "profile_subject_kind": "platform_account",
        "profile_subject_id": "acct_ig_fixture",
        "creator_record_id_or_none": None,
        "platform_scope": "instagram",
        "platform_account_ids": ["acct_ig_fixture"],
        "platform_subject_key_type": "instagram_username",
        "platform_subject_key": "ig_user_fixture",
        "public_handle": "@igfixture",
        "rollup_window": "custom",
        "rollup_window_description": "fixture window",
        "content_kind_inclusion_rule": "fixture reels only",
        "metric_rollups": {
            "average_views": {"value_or_none": round(statistics.mean(views), 2), "posture": "observed", "metric_unit": "count"},
            "median_views": {"value_or_none": round(statistics.median(views), 2), "posture": "observed", "metric_unit": "count"},
            "engagement_rate": {"value_or_none": engagement, "posture": "observed", "metric_unit": "rate"},
            "average_like_count": {"value_or_none": round(statistics.mean(likes), 2), "posture": "observed", "metric_unit": "count"},
            "average_comment_count": {"value_or_none": round(statistics.mean(comments), 2), "posture": "observed", "metric_unit": "count"},
            "posting_cadence": {"value_or_none": None, "posture": "not_attempted", "posture_reason_or_none": "fixture", "metric_unit": "rate"},
            "recent_velocity": {"value_or_none": None, "posture": "not_attempted", "posture_reason_or_none": "fixture", "metric_unit": "rate"},
        },
        "source_metric_observation_ids": [obs["metric_observation_id"] for obs in observations],
        "observation_count": len(observations),
        "view_count_min": min(views),
        "view_count_max": max(views),
        "calculation_recipe_version": IG_RECIPE,
        "computed_at": RUN_T1,
        "freshness_state": "partial",
        "limitations": ["fixture"],
        "sample_support": {
            "observation_count": len(observations),
            "sample_adequacy": "limited_n_4_to_7",
            "representativeness_posture": "admitted_pool_only_not_representative_creator_average",
            "surface_handling": "show_only_with_visible_admitted_pool_limitation",
        },
    }
    seed_document = {
        YOUTUBE_SEED_WRAPPER_KEY: {
            "metric_observations": observations,
            "metric_rollups": [rollup],
        }
    }
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    result = derive_youtube_creator_metric_silver_records_from_seed(
        data_root=data_root, seed_document=seed_document
    )
    report = revalidate_creator_metric_rollups(data_root)
    assert report.rollups_checked == 1
    assert report.ok, [f.failures for f in report.findings]

    def _corrupt_engagement(record: dict) -> None:
        record["payload"]["observation"]["metric_rollups"]["engagement_rate"]["metric_value"] = 0.5

    _rewrite_record(result.rollup_paths[0], _corrupt_engagement)
    report = revalidate_creator_metric_rollups(data_root)
    assert not report.ok
    assert any("engagement_rate" in failure for failure in report.findings[0].failures)


def test_tampered_rollup_value_fails_formula_check(tmp_path: Path) -> None:
    data_root, result = _live_lake(tmp_path)

    def _bump_average_views(record: dict) -> None:
        metric = record["payload"]["observation"]["metric_rollups"]["average_views"]
        metric["metric_value"] = metric["metric_value"] + 1

    _rewrite_record(result.rollup_paths[0], _bump_average_views)
    report = revalidate_creator_metric_rollups(data_root)
    assert report.rollups_checked == 1
    finding = report.findings[0]
    assert not finding.ok
    assert any("average_views" in failure and "recomputed" in failure for failure in finding.failures)


def test_malformed_rollup_subject_ref_is_record_failure_not_walk_crash(tmp_path: Path) -> None:
    data_root, result = _live_lake(tmp_path)

    def _remove_account_ref(record: dict) -> None:
        record["payload"]["observation"]["subject"]["ref"] = {}

    _rewrite_record(result.rollup_paths[0], _remove_account_ref)
    report = revalidate_creator_metric_rollups(data_root)

    assert report.rollups_checked == 1
    finding = report.findings[0]
    assert finding.account_id == ""
    assert not finding.ok
    assert any("account id unresolved" in failure for failure in finding.failures)


def test_tampered_observation_fails_integrity_check(tmp_path: Path) -> None:
    data_root, result = _live_lake(tmp_path)
    observation_path = result.observation_paths[0]
    record = json.loads(observation_path.read_text(encoding="utf-8"))
    record["payload"]["observation"]["metric_value"] = 999999  # no hash restamp
    observation_path.write_bytes(canonical_record_bytes(record))
    report = revalidate_creator_metric_rollups(data_root)
    assert not report.ok
    assert any(
        "content_hash does not reproduce" in failure
        for finding in report.findings
        for failure in finding.failures
    )


def test_deleted_observation_fails_lineage_resolution(tmp_path: Path) -> None:
    data_root, result = _live_lake(tmp_path)
    result.observation_paths[0].unlink()
    report = revalidate_creator_metric_rollups(data_root)
    assert not report.ok
    assert any(
        "does not resolve" in failure
        for finding in report.findings
        for failure in finding.failures
    )


def test_unknown_recipe_version_is_a_failure_not_a_skip(tmp_path: Path) -> None:
    data_root, result = _live_lake(tmp_path)

    def _unknown_recipe(record: dict) -> None:
        record["payload"]["observation"]["calculation_recipe_version"] = "mystery_recipe_v9"

    _rewrite_record(result.rollup_paths[0], _unknown_recipe)
    report = revalidate_creator_metric_rollups(data_root)
    assert not report.ok
    assert any(
        "unknown calculation_recipe_version" in failure
        for failure in report.findings[0].failures
    )


# -- IG recompute: engagement inputs must be grouped by content_id -----------

def test_recompute_ig_rejects_mixed_subset_engagement_inputs() -> None:
    # The exact tamper a restamped rollup could carry: view from reel A, like
    # from reel B, comment from reel A. Counts are equal (1/1/1) so a
    # count-only check would pass, but NO single reel has all three -- there is
    # no complete reel trio, so the grouped recompute must fail.
    rows = [
        _SourceRow(metric_name="view_count", value=1000, content_id="reelA"),
        _SourceRow(metric_name="like_count", value=50, content_id="reelB"),
        _SourceRow(metric_name="comment_count", value=9, content_id="reelA"),
    ]
    failures = _recompute_ig(observation={}, metrics={}, rows=rows)
    assert failures
    assert any("complete reel trio" in f for f in failures)


# -- TikTok recompute: engagement inputs must be grouped by content_id ---------

def test_recompute_tiktok_rejects_mixed_subset_engagement_inputs() -> None:
    # The exact tamper the delegated review probed: view from video A, like from
    # video B, comment from video A. Counts are equal (1/1/1) so a count-only
    # check would pass, but NO single content has all three -- there is no
    # complete video trio, so the grouped recompute must fail.
    rows = [
        _SourceRow(metric_name="view_count", value=1000, content_id="videoA"),
        _SourceRow(metric_name="like_count", value=50, content_id="videoB"),
        _SourceRow(metric_name="total_comment_count", value=9, content_id="videoA"),
    ]
    failures = _recompute_tiktok(observation={}, metrics={}, rows=rows)
    assert failures
    assert any("complete video trio" in f for f in failures)


def test_recompute_tiktok_uses_only_complete_content_groups() -> None:
    # videoA is a complete trio; videoB has only a like (its view/comment are
    # gaps). The producer computes over complete videos only, so the recompute
    # must ignore videoB entirely and require metrics computed from videoA alone.
    rows = [
        _SourceRow(metric_name="view_count", value=1000, content_id="videoA"),
        _SourceRow(metric_name="like_count", value=50, content_id="videoA"),
        _SourceRow(metric_name="total_comment_count", value=9, content_id="videoA"),
        _SourceRow(metric_name="like_count", value=99999, content_id="videoB"),
    ]
    # engagement over the complete group only: (50 + 9) / 1000 = 0.059
    metrics = {
        "average_views": {"metric_posture": {"kind": "observed"}, "metric_value": 1000.0},
        "view_count_min": {"metric_posture": {"kind": "observed"}, "metric_value": 1000},
        "view_count_max": {"metric_posture": {"kind": "observed"}, "metric_value": 1000},
        "median_views": {"metric_posture": {"kind": "observed"}, "metric_value": 1000.0},
        "average_like_count": {"metric_posture": {"kind": "observed"}, "metric_value": 50.0},
        "average_comment_count": {"metric_posture": {"kind": "observed"}, "metric_value": 9.0},
        "engagement_rate": {"metric_posture": {"kind": "observed"}, "metric_value": 0.059},
        "posting_cadence": {"metric_posture": {"kind": "not_attempted"}},
        "recent_velocity": {"metric_posture": {"kind": "not_attempted"}},
    }
    # videoB's stray like (99999) must NOT contaminate the average_like_count of 50
    observation = {"view_count_min": 1000, "view_count_max": 1000}
    failures = _recompute_tiktok(observation=observation, metrics=metrics, rows=rows)
    assert failures == []
