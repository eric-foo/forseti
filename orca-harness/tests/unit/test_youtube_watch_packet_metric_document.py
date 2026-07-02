"""Unit tests for the LIVE watch-packet metric document builder.

The builder is the live half of the YouTube capture->registry loop: it reads
committed ``youtube_watch_metadata_comments`` packets from a (test) lake and
produces the seed-shaped document the Silver producer consumes. These tests
prove: engagement recipe math (IG-mirroring semantics), per-metric observed
subsets, latest-packet-per-video selection, and every fail-closed path
(missing packet, timestamp tie, channel mismatch, zero observed views,
non-integer receipt value)."""
from __future__ import annotations

from pathlib import Path

import pytest

from capture_spine.creator_profile_current.youtube_metric_seed import (
    YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_WRAPPER,
)
from capture_spine.creator_profile_current.youtube_watch_packet_metric_document import (
    YOUTUBE_WATCH_PACKET_METRIC_RECIPE_VERSION,
    YOUTUBE_WATCH_PACKET_METRIC_REGISTRY_VERSION,
    WatchPacketMetricDocumentError,
    build_youtube_watch_packet_metric_document,
    discover_latest_watch_captures,
)
from data_lake.root import DataLakeRoot
from source_capture.youtube_watch_packet import YoutubeWatchFetch, write_youtube_watch_packet

ALPHA_CHANNEL = "UCalphaAlphaAlphaAlpha01"
BRAVO_CHANNEL = "UCbravoBravoBravoBravo01"
T1 = "2026-07-01T10:00:00Z"
T2 = "2026-07-02T09:00:00Z"
GENERATED_AT = "2026-07-02T12:00:00Z"


def _account_ledger() -> dict:
    return {
        "platform_accounts": [
            {
                "platform_account_id": "acct_yt_alpha",
                "platform": "youtube",
                "platform_public_account_id_or_none": ALPHA_CHANNEL,
                "public_handle": "@alphafrag",
            },
            {
                "platform_account_id": "acct_yt_bravo",
                "platform": "youtube",
                "platform_public_account_id_or_none": BRAVO_CHANNEL,
                "public_handle": "@bravofrag",
            },
        ]
    }


def _creator_ledger(*, include_brand_row: bool = False) -> dict:
    observations = [
        {
            "creator_observation_id": "yt_creator_obs_alpha",
            "platform_subject_key": ALPHA_CHANNEL,
            "creator_handle_query": "@alphafrag",
            "creator_classification": "creator_or_channel_observed",
            "pool_ids": ["yt-frag-pool200-001", "yt-frag-pool200-002"],
            "video_ids": ["vidAlpha001", "vidAlpha002"],
        },
        {
            "creator_observation_id": "yt_creator_obs_bravo",
            "platform_subject_key": BRAVO_CHANNEL,
            "creator_handle_query": "@bravofrag",
            "creator_classification": "creator_or_channel_observed",
            "pool_ids": ["yt-frag-pool200-003"],
            "video_ids": ["vidBravo001"],
        },
    ]
    if include_brand_row:
        observations.append(
            {
                "creator_observation_id": "yt_creator_obs_brand",
                "platform_subject_key": "UCbrandBrandBrandBrand01",
                "creator_handle_query": "@somebrand",
                "creator_classification": "brand_or_platform_account_observed",
                "pool_ids": ["yt-frag-pool200-004"],
                "video_ids": ["vidBrand0001"],
            }
        )
    return {"youtube_creator_observation_ledger": {"creator_observations": observations}}


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


def _fetch_packet(
    *,
    video_id: str,
    channel_id: str,
    view_count: int | None,
    like_count: int | None = None,
    total_comment_count: int | None = None,
) -> dict:
    engagement: dict = {}
    receipts: dict = {}
    for metric, value in (
        ("view_count", view_count),
        ("like_count", like_count),
        ("total_comment_count", total_comment_count),
    ):
        if value is None:
            receipts[metric] = _unavailable_receipt(f"{metric} not exposed in fixture")
        else:
            engagement[metric] = value
            receipts[metric] = _observed_receipt(value)
    receipts["comment_sample_count"] = _unavailable_receipt("comments not sampled in fixture")
    return {
        "video_id": video_id,
        "surface_type": "watch",
        "watch_url": f"https://www.youtube.com/watch?v={video_id}",
        "channel": {"channel_id": channel_id, "author": "fixture"},
        "metadata": {"title": f"fixture {video_id}", "publish_date": "2026-06-20"},
        "engagement": engagement,
        "availability": {"video_state": "playable", "comments_state": "comments_not_exposed"},
        "metric_receipts": receipts,
        "comments_posture": "comments_not_exposed",
        "receipts": {"http_status": 200, "retrieval_time_utc": T1},
    }


def _commit_packet(data_root: DataLakeRoot, *, captured_at: str, **packet_kwargs) -> str:
    code, output_dir = write_youtube_watch_packet(
        YoutubeWatchFetch(
            video_id=packet_kwargs["video_id"],
            raw_watch_html=f"<html>{packet_kwargs['video_id']}@{captured_at}</html>".encode(),
            packet=_fetch_packet(**packet_kwargs),
        ),
        data_root=data_root,
        decision_question="live watch-packet metric document test",
        now_iso=captured_at,
    )
    assert code == 0
    return Path(output_dir).name


def _lake_with_default_captures(tmp_path: Path) -> DataLakeRoot:
    """Alpha: vidAlpha001 fully engaged, vidAlpha002 view-only. Bravo: one fully
    engaged video."""
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_packet(
        data_root,
        captured_at=T1,
        video_id="vidAlpha001",
        channel_id=ALPHA_CHANNEL,
        view_count=100,
        like_count=10,
        total_comment_count=5,
    )
    _commit_packet(
        data_root,
        captured_at=T1,
        video_id="vidAlpha002",
        channel_id=ALPHA_CHANNEL,
        view_count=200,
    )
    _commit_packet(
        data_root,
        captured_at=T1,
        video_id="vidBravo001",
        channel_id=BRAVO_CHANNEL,
        view_count=50,
        like_count=5,
        total_comment_count=2,
    )
    data_root.rebuild_availability()
    return data_root


def _build(data_root: DataLakeRoot, **overrides) -> dict:
    kwargs = {
        "creator_ledger": _creator_ledger(),
        "account_ledger": _account_ledger(),
        "generated_at_utc": GENERATED_AT,
    }
    kwargs.update(overrides)
    return build_youtube_watch_packet_metric_document(data_root, **kwargs)


def test_builds_engagement_bearing_document_from_live_packets(tmp_path: Path) -> None:
    data_root = _lake_with_default_captures(tmp_path)
    document = _build(data_root)
    seed = document[YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_WRAPPER]

    assert seed["generated_at_utc"] == GENERATED_AT
    assert seed["counts"]["metric_rollups_total"] == 2
    assert seed["counts"]["engagement_rate_rollups_observed"] == 2
    # Alpha: view(100), like(10), comment(5), view(200) = 4; Bravo: 3.
    assert seed["counts"]["metric_observations_total"] == 7

    rollups = {rollup["profile_subject_id"]: rollup for rollup in seed["metric_rollups"]}
    alpha = rollups["acct_yt_alpha"]
    assert alpha["calculation_recipe_version"] == YOUTUBE_WATCH_PACKET_METRIC_RECIPE_VERSION
    assert alpha["computed_at"] == GENERATED_AT
    metrics = alpha["metric_rollups"]
    assert metrics["average_views"]["value_or_none"] == 150.0
    assert metrics["median_views"]["value_or_none"] == 150.0
    assert alpha["view_count_min"] == 100
    assert alpha["view_count_max"] == 200
    # Engagement covers ONLY the complete-input video (vidAlpha001).
    assert metrics["engagement_rate"]["posture"] == "observed"
    assert metrics["engagement_rate"]["value_or_none"] == round((10 + 5) / 100, 6)
    assert metrics["average_like_count"]["value_or_none"] == 10.0
    assert metrics["average_comment_count"]["value_or_none"] == 5.0
    assert metrics["posting_cadence"]["posture"] == "not_attempted"
    # 4 observations -> limited adequacy band, IG-style multi-metric counting.
    assert alpha["observation_count"] == 4 == len(alpha["source_metric_observation_ids"])
    assert alpha["sample_support"]["sample_adequacy"] == "limited_n_4_to_7"
    assert alpha["sample_support"]["surface_handling"] == "show_only_with_visible_admitted_pool_limitation"
    joined_limitations = " ".join(alpha["limitations"])
    assert "not a representative creator average" in joined_limitations
    assert "selection can bias view averages" in joined_limitations
    assert "1 of 2 admitted Shorts" in joined_limitations

    bravo = rollups["acct_yt_bravo"]
    assert bravo["metric_rollups"]["engagement_rate"]["value_or_none"] == round((5 + 2) / 50, 6)
    assert bravo["observation_count"] == 3
    assert bravo["sample_support"]["sample_adequacy"] == "thin_n_1_to_3"
    assert bravo["sample_support"]["surface_handling"] == "downgrade_or_withhold_summary_claim"


def test_observations_carry_lake_packet_provenance(tmp_path: Path) -> None:
    data_root = _lake_with_default_captures(tmp_path)
    seed = _build(data_root)[YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_WRAPPER]
    observations = seed["metric_observations"]
    assert len({obs["metric_observation_id"] for obs in observations}) == len(observations)
    for observation in observations:
        packet_id = observation["source_packet_id_or_none"]
        assert packet_id
        assert observation["metric_registry_version"] == YOUTUBE_WATCH_PACKET_METRIC_REGISTRY_VERSION
        assert observation["metric_posture"] == "observed"
        assert observation["observed_at"] == T1
        assert observation["observed_at_source"] == "watch_packet_capture_timestamp"
        assert observation["source_file"].startswith("raw/")
        assert f"/{packet_id}/" in observation["source_file"]
        assert observation["source_file"].endswith("youtube_watch_capture.json")
        metric = observation["metric_name"]
        assert observation["source_pointer"] == f"{observation['source_file']}#/metric_receipts/{metric}"
        # The provenance hash is the preserved watch HTML's manifest sha256.
        loaded = data_root.load_raw_packet(packet_id)
        watch_entry = next(
            entry
            for entry in loaded.manifest["preserved_files"]
            if str(entry["relative_packet_path"]).endswith("raw_watch.html")
        )
        assert observation["source_watch_html_sha256_or_none"] == watch_entry["sha256"]


def test_engagement_unavailable_when_no_video_exposes_inputs(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    for video_id, pool_channel in (("vidAlpha001", ALPHA_CHANNEL), ("vidAlpha002", ALPHA_CHANNEL)):
        _commit_packet(
            data_root, captured_at=T1, video_id=video_id, channel_id=pool_channel, view_count=100
        )
    _commit_packet(
        data_root, captured_at=T1, video_id="vidBravo001", channel_id=BRAVO_CHANNEL, view_count=50
    )
    data_root.rebuild_availability()
    seed = _build(data_root)[YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_WRAPPER]
    assert seed["counts"]["engagement_rate_rollups_observed"] == 0
    for rollup in seed["metric_rollups"]:
        for name in ("engagement_rate", "average_like_count", "average_comment_count"):
            metric = rollup["metric_rollups"][name]
            assert metric["posture"] == "unavailable_with_reason"
            assert metric["value_or_none"] is None
            assert metric["posture_reason_or_none"]


def test_latest_packet_per_video_wins(tmp_path: Path) -> None:
    data_root = _lake_with_default_captures(tmp_path)
    _commit_packet(
        data_root,
        captured_at=T2,
        video_id="vidBravo001",
        channel_id=BRAVO_CHANNEL,
        view_count=80,
        like_count=8,
        total_comment_count=4,
    )
    data_root.rebuild_availability()
    seed = _build(data_root)[YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_WRAPPER]
    bravo = next(r for r in seed["metric_rollups"] if r["profile_subject_id"] == "acct_yt_bravo")
    assert bravo["metric_rollups"]["average_views"]["value_or_none"] == 80.0
    bravo_observations = [
        obs for obs in seed["metric_observations"] if obs["platform_account_id"] == "acct_yt_bravo"
    ]
    assert {obs["observed_at"] for obs in bravo_observations} == {T2}


def test_distinct_packets_tying_on_timestamp_fail_closed(tmp_path: Path) -> None:
    data_root = _lake_with_default_captures(tmp_path)
    _commit_packet(
        data_root, captured_at=T1, video_id="vidBravo001", channel_id=BRAVO_CHANNEL, view_count=999
    )
    data_root.rebuild_availability()
    with pytest.raises(WatchPacketMetricDocumentError) as excinfo:
        _build(data_root)
    assert excinfo.value.reason == "ambiguous_video_packet"
    assert excinfo.value.subject == "vidBravo001"


def test_missing_watch_packet_fails_closed_and_names_videos(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_packet(
        data_root,
        captured_at=T1,
        video_id="vidAlpha001",
        channel_id=ALPHA_CHANNEL,
        view_count=100,
    )
    data_root.rebuild_availability()
    with pytest.raises(WatchPacketMetricDocumentError) as excinfo:
        _build(data_root)
    assert excinfo.value.reason == "missing_video_packet"
    assert "vidAlpha002" in str(excinfo.value)
    assert "vidBravo001" in str(excinfo.value)


def test_brand_ledger_rows_need_no_packet_and_enter_no_rollup(tmp_path: Path) -> None:
    data_root = _lake_with_default_captures(tmp_path)
    seed = _build(data_root, creator_ledger=_creator_ledger(include_brand_row=True))[
        YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_WRAPPER
    ]
    assert seed["counts"]["brand_or_platform_excluded_ledger_rows"] == 1
    assert seed["counts"]["metric_rollups_total"] == 2
    assert all(
        obs["content_id_or_none"] != "vidBrand0001" for obs in seed["metric_observations"]
    )


def test_channel_mismatch_fails_closed(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_packet(
        data_root,
        captured_at=T1,
        video_id="vidAlpha001",
        channel_id=BRAVO_CHANNEL,  # captured under the WRONG channel
        view_count=100,
    )
    _commit_packet(
        data_root, captured_at=T1, video_id="vidAlpha002", channel_id=ALPHA_CHANNEL, view_count=200
    )
    _commit_packet(
        data_root, captured_at=T1, video_id="vidBravo001", channel_id=BRAVO_CHANNEL, view_count=50
    )
    data_root.rebuild_availability()
    with pytest.raises(WatchPacketMetricDocumentError) as excinfo:
        _build(data_root)
    assert excinfo.value.reason == "channel_mismatch"
    assert excinfo.value.subject == "vidAlpha001"


def test_account_with_no_observed_views_fails_closed(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_packet(
        data_root, captured_at=T1, video_id="vidAlpha001", channel_id=ALPHA_CHANNEL, view_count=100
    )
    _commit_packet(
        data_root, captured_at=T1, video_id="vidAlpha002", channel_id=ALPHA_CHANNEL, view_count=200
    )
    # Bravo's only video exposes NO view_count (e.g. the video became unavailable).
    _commit_packet(
        data_root,
        captured_at=T1,
        video_id="vidBravo001",
        channel_id=BRAVO_CHANNEL,
        view_count=None,
        like_count=5,
    )
    data_root.rebuild_availability()
    with pytest.raises(WatchPacketMetricDocumentError) as excinfo:
        _build(data_root)
    assert excinfo.value.reason == "no_observed_views_for_account"
    assert excinfo.value.subject == "acct_yt_bravo"


def test_discovery_ignores_unexpected_videos(tmp_path: Path) -> None:
    data_root = _lake_with_default_captures(tmp_path)
    _commit_packet(
        data_root,
        captured_at=T1,
        video_id="vidOther001",
        channel_id="UCotherOtherOtherOther01",
        view_count=7,
    )
    data_root.rebuild_availability()
    captures = discover_latest_watch_captures(
        data_root, expected_video_ids=["vidAlpha001", "vidAlpha002", "vidBravo001"]
    )
    assert set(captures) == {"vidAlpha001", "vidAlpha002", "vidBravo001"}
