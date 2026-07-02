"""End-to-end lake-free proof of the LIVE capture->registry recapture loop.

The load-bearing claim of the live path is not one module -- it is the cycle:
watch packets -> live metric document -> Silver producer -> committed snapshot
(run-order chain advance) -> freshness gate, with the longitudinal rollup
history accruing append-only in the lake. This test runs TWO full recapture
cycles against ``DataLakeRoot.for_test`` (CI never resolves the real lake) and
asserts every seam:

1. cycle 1 populates the lake and mints snapshot run 1 (genesis manifest);
2. the freshness gate proves the committed snapshot fresh;
3. cycle 2 (new packets, fresh computed_at) appends -- history now has two
   rollup records per account -- and the gate reports ``snapshot_behind_lake``;
4. snapshot run 2 advances the selection chain onto the new rollups;
5. the regenerated snapshot materializes into a VALID creator_profile_current
   view (the view validator accepts engagement-bearing YouTube rollups);
6. the formula revalidator recomputes the ENTIRE history (both cycles) clean.
"""
from __future__ import annotations

import json
from pathlib import Path

from capture_spine.creator_profile_current.live_lake_freshness_gate import (
    check_live_lake_freshness,
)
from capture_spine.creator_profile_current.materialize import (
    build_creator_profile_current_view_from_files,
)
from capture_spine.creator_profile_current.rollup_formula_revalidation import (
    revalidate_creator_metric_rollups,
)
from capture_spine.creator_profile_current.silver_metric_snapshot import SNAPSHOT_WRAPPER_KEY
from data_lake.root import DataLakeRoot
from runners.run_creator_metric_rollup_snapshot import run_snapshot
from runners.run_youtube_watch_packet_metric_rollup_producer import run_watch_packet_producer
from source_capture.youtube_watch_packet import YoutubeWatchFetch, write_youtube_watch_packet

ALPHA_CHANNEL = "UCalphaAlphaAlphaAlpha01"
BRAVO_CHANNEL = "UCbravoBravoBravoBravo01"
CAPTURE_T1 = "2026-07-01T10:00:00Z"
CAPTURE_T2 = "2026-07-02T09:00:00Z"
RUN_T1 = "2026-07-01T11:00:00Z"
RUN_T2 = "2026-07-02T10:00:00Z"


def _account_ledger() -> dict:
    return {
        "platform_accounts": [
            {
                "platform_account_id": "acct_yt_alpha",
                "platform": "youtube",
                "platform_public_account_id_or_none": ALPHA_CHANNEL,
                "public_handle": "@alphafrag",
                "public_profile_url": "https://www.youtube.com/@alphafrag",
                "handle_source_pointer": "docs/review-inputs/fixture_alpha.json#/handle",
                "handle_observed_at": "2026-06-20T00:00:00Z",
            },
            {
                "platform_account_id": "acct_yt_bravo",
                "platform": "youtube",
                "platform_public_account_id_or_none": BRAVO_CHANNEL,
                "public_handle": "@bravofrag",
                "public_profile_url": "https://www.youtube.com/@bravofrag",
                "handle_source_pointer": "docs/review-inputs/fixture_bravo.json#/handle",
                "handle_observed_at": "2026-06-20T00:00:00Z",
            },
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
    data_root: DataLakeRoot,
    *,
    captured_at: str,
    video_id: str,
    channel_id: str,
    view_count: int,
    like_count: int,
    total_comment_count: int,
) -> None:
    packet = {
        "video_id": video_id,
        "surface_type": "watch",
        "watch_url": f"https://www.youtube.com/watch?v={video_id}",
        "channel": {"channel_id": channel_id, "author": "fixture"},
        "metadata": {"title": f"fixture {video_id}", "publish_date": "2026-06-20"},
        "engagement": {
            "view_count": view_count,
            "like_count": like_count,
            "total_comment_count": total_comment_count,
        },
        "availability": {"video_state": "playable", "comments_state": "comments_not_exposed"},
        "metric_receipts": {
            "view_count": _observed_receipt(view_count),
            "like_count": _observed_receipt(like_count),
            "total_comment_count": _observed_receipt(total_comment_count),
            "comment_sample_count": _unavailable_receipt("comments not sampled in fixture"),
        },
        "comments_posture": "comments_not_exposed",
        "receipts": {"http_status": 200, "retrieval_time_utc": captured_at},
    }
    code, _output = write_youtube_watch_packet(
        YoutubeWatchFetch(
            video_id=video_id,
            raw_watch_html=f"<html>{video_id}@{captured_at}</html>".encode(),
            packet=packet,
        ),
        data_root=data_root,
        decision_question="live recapture loop test",
        now_iso=captured_at,
    )
    assert code == 0


def _commit_capture_cycle(data_root: DataLakeRoot, *, captured_at: str, base_views: int) -> None:
    _commit_packet(
        data_root,
        captured_at=captured_at,
        video_id="vidAlpha001",
        channel_id=ALPHA_CHANNEL,
        view_count=base_views,
        like_count=10,
        total_comment_count=5,
    )
    _commit_packet(
        data_root,
        captured_at=captured_at,
        video_id="vidAlpha002",
        channel_id=ALPHA_CHANNEL,
        view_count=base_views * 2,
        like_count=20,
        total_comment_count=8,
    )
    _commit_packet(
        data_root,
        captured_at=captured_at,
        video_id="vidBravo001",
        channel_id=BRAVO_CHANNEL,
        view_count=base_views // 2,
        like_count=5,
        total_comment_count=2,
    )
    data_root.rebuild_availability()


def test_live_recapture_loop_snapshot_freshness_view_and_revalidation(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    account_ledger = _account_ledger()
    creator_ledger = _creator_ledger()
    snapshot_dir = tmp_path / "committed"
    snapshot_path = snapshot_dir / "youtube_shorts_fragrance_creator_metric_rollup_snapshot_v0.json"
    manifest_path = snapshot_dir / "youtube_shorts_fragrance_creator_metric_rollup_selection_manifest_v0.json"
    receipt_path = snapshot_dir / "youtube_shorts_fragrance_creator_metric_rollup_freshness_receipt_v0.json"

    # -- cycle 1: capture, produce, mint snapshot run 1 -----------------------
    _commit_capture_cycle(data_root, captured_at=CAPTURE_T1, base_views=100)
    result_1 = run_watch_packet_producer(
        data_root,
        creator_ledger=creator_ledger,
        account_ledger=account_ledger,
        generated_at_utc=RUN_T1,
    )
    assert len(result_1.rollup_records) == 2
    assert len(result_1.observation_records) == 9  # 3 metrics x 3 videos

    summary_1 = run_snapshot(
        data_root,
        account_ledger=account_ledger,
        platform="youtube",
        snapshot_generated_at=RUN_T1,
        reconciled_at=RUN_T1,
        snapshot_path=snapshot_path,
        manifest_path=manifest_path,
        receipt_path=receipt_path,
        write=True,
    )
    assert summary_1["selection_run_id"] == 1
    assert summary_1["accounts"] == 2

    committed_snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    committed_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    fresh_1 = check_live_lake_freshness(
        data_root,
        account_ledger=account_ledger,
        platform="youtube",
        committed_snapshot=committed_snapshot,
        committed_manifest=committed_manifest,
    )
    assert fresh_1.is_fresh

    # -- cycle 2: recapture with moved numbers, produce with a fresh computed_at
    _commit_capture_cycle(data_root, captured_at=CAPTURE_T2, base_views=150)
    result_2 = run_watch_packet_producer(
        data_root,
        creator_ledger=creator_ledger,
        account_ledger=account_ledger,
        generated_at_utc=RUN_T2,
    )
    assert len(result_2.rollup_records) == 2

    stale = check_live_lake_freshness(
        data_root,
        account_ledger=account_ledger,
        platform="youtube",
        committed_snapshot=committed_snapshot,
        committed_manifest=committed_manifest,
    )
    assert not stale.is_fresh
    assert stale.reason == "snapshot_behind_lake"
    assert set(stale.drifted_accounts) == {"acct_yt_alpha", "acct_yt_bravo"}

    summary_2 = run_snapshot(
        data_root,
        account_ledger=account_ledger,
        platform="youtube",
        snapshot_generated_at=RUN_T2,
        reconciled_at=RUN_T2,
        snapshot_path=snapshot_path,
        manifest_path=manifest_path,
        receipt_path=receipt_path,
        write=True,
    )
    assert summary_2["selection_run_id"] == 2

    snapshot_2 = json.loads(snapshot_path.read_text(encoding="utf-8"))
    rollups_2 = {
        rollup["profile_subject_id"]: rollup
        for rollup in snapshot_2[SNAPSHOT_WRAPPER_KEY]["metric_rollups"]
    }
    alpha_2 = rollups_2["acct_yt_alpha"]
    assert alpha_2["computed_at"] == RUN_T2
    assert alpha_2["metric_rollups"]["average_views"]["value_or_none"] == 225.0  # (150+300)/2
    assert alpha_2["metric_rollups"]["engagement_rate"]["posture"] == "observed"

    fresh_2 = check_live_lake_freshness(
        data_root,
        account_ledger=account_ledger,
        platform="youtube",
        committed_snapshot=snapshot_2,
        committed_manifest=json.loads(manifest_path.read_text(encoding="utf-8")),
    )
    assert fresh_2.is_fresh

    # -- the regenerated snapshot materializes into a VALID committed view ----
    ledger_path = tmp_path / "creator_public_handle_linkage_ledger_v0.json"
    ledger_path.write_text(
        json.dumps({"creator_public_handle_linkage_ledger": account_ledger}, indent=2) + "\n",
        encoding="utf-8",
    )
    view = build_creator_profile_current_view_from_files(
        account_ledger_path=ledger_path,
        metric_seed_paths=[snapshot_path],
        generated_at_utc=RUN_T2,
    )  # validates internally; raising == the live rollup shape broke the view contract
    wrapper = view["creator_profile_current_view"]
    assert wrapper["counts"]["profiles_total"] == 2
    assert wrapper["counts"]["engagement_rate_observed_profiles"] == 2

    # -- the formula revalidator recomputes the WHOLE history (both cycles) ---
    report = revalidate_creator_metric_rollups(data_root)
    assert report.rollups_checked == 4  # 2 accounts x 2 recapture cycles
    assert report.failures_total == 0, [f.failures for f in report.findings if not f.ok]


def test_live_rollup_records_drop_the_engagement_non_claim(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_capture_cycle(data_root, captured_at=CAPTURE_T1, base_views=100)
    result = run_watch_packet_producer(
        data_root,
        creator_ledger=_creator_ledger(),
        account_ledger=_account_ledger(),
        generated_at_utc=RUN_T1,
    )
    engagement_non_claim = "not an engagement-rate, like, or comment metric"
    for record in result.rollup_records:
        # Live rollups carry OBSERVED engagement metrics; the non-claim would be false.
        assert engagement_non_claim not in record["non_claims"]
        assert "not buyer proof" in record["non_claims"]
    for record in result.observation_records:
        metric_name = record["payload"]["observation"]["metric_name"]
        if metric_name in {"like_count", "total_comment_count"}:
            assert engagement_non_claim not in record["non_claims"]
        else:
            assert engagement_non_claim in record["non_claims"]
