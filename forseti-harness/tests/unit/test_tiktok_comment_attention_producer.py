from __future__ import annotations

import json
import hashlib

from capture_spine.creator_profile_current.tiktok_comment_attention_producer import (
    COMMENT_ATTENTION_LANE,
    COMMENT_ATTENTION_METRIC,
    COMMENT_ATTENTION_POLICY_FINGERPRINT,
    build_comment_attention_records,
)
from data_lake.root import DataLakeRoot
from data_lake.silver_lineage import SOURCE_BACKED_COMPLETE_STATUS, silver_record_source_backed_status
from runners.run_tiktok_comment_attention_producer import run_comment_attention
from test_tiktok_creator_metric_seed import CAPTURE_T1, _commit_batch_packet, _stats, _video


def _comment_video(*, video_likes: int = 1000) -> dict:
    video = _video("7655162561783975199", stats=_stats(10000, video_likes, 100))
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
