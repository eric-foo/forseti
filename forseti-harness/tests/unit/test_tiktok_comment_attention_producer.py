from __future__ import annotations

import json
import hashlib
from types import SimpleNamespace

import pytest

from capture_spine.creator_profile_current.tiktok_comment_attention_producer import (
    COMMENT_ATTENTION_LANE,
    COMMENT_ATTENTION_METRIC,
    COMMENT_ATTENTION_POLICY_FINGERPRINT,
    build_comment_attention_records,
)
from data_lake.consumption import find_acks
from data_lake.root import DataLakeRoot
from data_lake.silver_lineage import SOURCE_BACKED_COMPLETE_STATUS, silver_record_source_backed_status
from runners import run_tiktok_comment_attention_producer as runner
from runners.run_tiktok_comment_attention_producer import run_comment_attention
from tiktok_batch_test_support import CAPTURE_T1, _commit_batch_packet, _stats, _video
from test_tiktok_grid_observation_producer import _admit_grid


def _comment_video(*, video_likes: int = 1000) -> dict:
    video = _video("7655162561783975199", stats=_stats(10000, video_likes, 100))
    video["stats_observed_utc"] = CAPTURE_T1
    video["comments"] = {
        "posture": "captured_page_owned_response",
        "observed_utc": CAPTURE_T1,
        "captured_comment_count": 2,
        "comments": [
            {
                "source_order": 0,
                "cid": "comment-1",
                "text": "this one wins",
                "create_time_utc": "2026-06-30T16:00:00Z",
                "digg_count": 50,
                "reply_comment_total": 2,
            },
            {
                "source_order": 1,
                "cid": "comment-2",
                "text": "not for me",
                "create_time_utc": "2026-06-30T16:01:00Z",
                "digg_count": 10,
                "reply_comment_total": 0,
            },
        ],
    }
    return video


def test_builds_source_backed_ratio_observations_with_policy_fingerprint() -> None:
    records = build_comment_attention_records(
        raw_anchor="01TESTPACKET",
        batch_payload={"capture_timestamp": CAPTURE_T1, "videos": [_comment_video()]},
        raw_file_ref={
            "file_id": "file-1",
            "relative_packet_path": "raw/01_tiktok_batch_capture.json",
            "sha256": "a" * 64,
            "hash_basis": "raw_stored_bytes",
        },
    )
    assert len(records) == 2
    observation = records[0]["payload"]["observation"]
    assert records[0]["lane_namespace"] == COMMENT_ATTENTION_LANE
    assert observation["metric_name"] == COMMENT_ATTENTION_METRIC
    assert observation["metric_value"] == 0.05
    assert observation["numerator"]["metric_value"] == 50
    assert observation["denominator"]["metric_value"] == 1000
    assert observation["temporal_pairing"]["alignment"] == "same_capture_observation"
    assert observation["engagement_context"]["comment_like_to_video_comment_count_ratio"] == 0.5
    assert observation["engagement_context"]["comment_like_rank_within_captured"] == 1
    assert observation["engagement_context"]["comment_like_percentile_within_captured"] == 1.0
    assert records[0]["provenance"]["policy_fingerprint_sha256"] == COMMENT_ATTENTION_POLICY_FINGERPRINT
    assert silver_record_source_backed_status(records[0]) == SOURCE_BACKED_COMPLETE_STATUS
    canonical = dict(records[0])
    canonical.pop("content_hash")
    expected_hash = hashlib.sha256(
        json.dumps(
            canonical,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()
    assert records[0]["content_hash"] == f"sha256:{expected_hash}"


def test_zero_video_likes_is_unavailable_not_zero() -> None:
    record = build_comment_attention_records(
        raw_anchor="01TESTPACKET",
        batch_payload={"capture_timestamp": CAPTURE_T1, "videos": [_comment_video(video_likes=0)]},
        raw_file_ref={
            "file_id": "file-1",
            "relative_packet_path": "raw/01_tiktok_batch_capture.json",
            "sha256": "a" * 64,
        },
    )[0]
    observation = record["payload"]["observation"]
    assert observation["metric_value"] is None
    assert observation["metric_posture"]["kind"] == "unavailable_with_reason"
    assert observation["metric_posture"]["reason_code"] == "video_like_count_zero_denominator"


def test_unaligned_video_stats_are_retained_but_not_used() -> None:
    video = _comment_video()
    video["stats_observed_utc"] = "2026-07-01T00:00:00Z"
    observation = build_comment_attention_records(
        raw_anchor="01TESTPACKET",
        batch_payload={"capture_timestamp": CAPTURE_T1, "videos": [video]},
        raw_file_ref={"file_id": "file-1", "relative_packet_path": "raw/x.json", "sha256": "a" * 64},
    )[0]["payload"]["observation"]
    assert observation["metric_value"] is None
    assert observation["metric_posture"]["reason_code"] == "temporal_alignment_unproven"
    assert observation["numerator"]["metric_value"] == 50
    assert observation["denominator"]["metric_value"] == 1000


def test_comment_without_native_cid_uses_dom_fallback_without_crash() -> None:
    # DOM-captured top-level comments can lack a native cid; the record falls back
    # to a dom:{video}:{source_order} id. The mechanics lookup must still resolve
    # such comments instead of KeyError-ing.
    video = _comment_video()
    del video["comments"]["comments"][0]["cid"]
    records = build_comment_attention_records(
        raw_anchor="01TESTPACKET",
        batch_payload={"capture_timestamp": CAPTURE_T1, "videos": [video]},
        raw_file_ref={"file_id": "file-1", "relative_packet_path": "raw/x.json", "sha256": "a" * 64},
    )
    fallback = records[0]
    assert fallback["source_object"]["native_id"] == f"dom:{fallback['provenance']['video_id']}:0"
    assert fallback["provenance"]["comment_id"] is None
    observation = fallback["payload"]["observation"]
    assert observation["metric_value"] == 0.05
    assert observation["metric_posture"]["kind"] == "observed"
    assert observation["engagement_context"]["comment_like_rank_within_captured"] == 1


def test_runner_appends_once_and_ack_skips_unchanged_packet(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _commit_batch_packet(data_root, videos=[_comment_video()])

    first = run_comment_attention(data_root=data_root)
    assert first == [
        {
            "packet_id": packet_id,
            "status": "derived",
            "record_count": 2,
            "written_count": 2,
            "skipped_existing_count": 0,
        }
    ]
    lane = data_root.lane_dir(
        subtree="derived", raw_anchor=packet_id, lane=COMMENT_ATTENTION_LANE
    )
    stored = [json.loads(path.read_text(encoding="utf-8")) for path in lane.iterdir()]
    assert sorted(row["payload"]["observation"]["metric_value"] for row in stored) == [0.01, 0.05]

    assert run_comment_attention(data_root=data_root) == []
    assert len(list(lane.iterdir())) == 2


def test_runner_packet_selector_does_not_drain_unrelated_pending_packet(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    selected = _commit_batch_packet(data_root, videos=[_comment_video()])
    unrelated = _commit_batch_packet(data_root, videos=[_comment_video()])

    result = run_comment_attention(data_root=data_root, packet_ids=[selected])

    assert [row["packet_id"] for row in result if row["status"] == "derived"] == [selected]
    unrelated_lane = data_root.lane_dir(
        subtree="derived", raw_anchor=unrelated, lane=COMMENT_ATTENTION_LANE
    )
    assert not unrelated_lane.exists()


def test_runner_acknowledges_grid_packet_as_not_applicable(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _admit_grid(
        data_root,
        observed_at="2026-07-12T00:00:00Z",
        play_count=100,
        like_count=10,
        comment_count=2,
    )

    assert runner.run_catchup(data_root=data_root) == [
        {"packet_id": packet_id, "status": "not_applicable"}
    ]
    acks = find_acks(
        data_root,
        raw_anchor=packet_id,
        ack_namespace=COMMENT_ATTENTION_LANE,
    )
    assert len(acks) == 1
    assert acks[0]["evidence"][0]["kind"] == "not_applicable_non_batch_tiktok_packet"
    assert runner.pending_packets(data_root=data_root) == []


def test_main_exit_code_fails_on_availability_reconcile_failure(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        runner,
        "DataLakeRoot",
        SimpleNamespace(resolve=lambda **_kwargs: object()),
    )
    monkeypatch.setattr(
        runner,
        "run_catchup",
        lambda **_kwargs: [
            {
                "packet_id": "01PACKET",
                "status": "availability_reconcile_failed",
                "error": "OSError: simulated locked availability entry",
            }
        ],
    )

    assert runner.main(["--data-root", "ignored"]) == 1
    assert "availability_reconcile_failed" in capsys.readouterr().out
