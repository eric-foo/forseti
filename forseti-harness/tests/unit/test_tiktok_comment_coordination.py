from __future__ import annotations

import json
from pathlib import Path

import pytest

from cleaning.tiktok_silver_analytics import comment_coordination_signals
from data_lake.root import DataLakeRoot, DataLakeRootError
from runners.run_tiktok_comment_coordination import build_creator_coordination_report
from source_capture.models import known_fact
from source_capture.tiktok.batch_packet import TIKTOK_BATCH_CAPTURE_SURFACE
from source_capture.writer import write_local_source_capture_packet


def _comment(
    cid: str,
    *,
    uid: str,
    handle: str,
    text: str,
    created: int,
) -> dict:
    return {
        "cid": cid,
        "text": text,
        "create_time": created,
        "digg_count": 0,
        "reply_comment_total": 0,
        "user": {"uid": uid, "unique_id": handle, "nickname": handle},
    }


def _video(
    video_id: str,
    created: int,
    comments: list[dict],
    *,
    has_more: bool = True,
) -> dict:
    return {
        "video_id": video_id,
        "create_time": created,
        "comments": {
            "envelope": {"has_more": has_more, "total": 100},
            "comments": comments,
        },
    }


def _videos() -> list[dict]:
    repeated = "This fragrance is absolutely amazing"
    return [
        _video(
            "v1",
            1_000,
            [
                _comment(
                    "c1", uid="u1", handle="alice0001", text=repeated, created=1_010
                ),
                _comment(
                    "c2", uid="u2", handle="alice0002", text=repeated, created=1_015
                ),
                _comment(
                    "c3",
                    uid="u3",
                    handle="organicfan",
                    text="I like this too",
                    created=1_020,
                ),
                _comment(
                    "c4",
                    uid="u4",
                    handle="fourthfan",
                    text="A separate reaction",
                    created=1_900,
                ),
                _comment(
                    "c5",
                    uid="u5",
                    handle="fifthfan",
                    text="Another separate reaction",
                    created=2_000,
                ),
            ],
        ),
        _video(
            "v2",
            2_000,
            [
                _comment(
                    "c6", uid="u1", handle="alice0001", text="Back again", created=2_030
                ),
                _comment(
                    "c7", uid="u6", handle="sixthfan", text="Different words", created=3_000
                ),
                _comment(
                    "c8", uid="u7", handle="seventhfan", text="Still different", created=4_000
                ),
                _comment(
                    "c9", uid="u8", handle="eighthfan", text="More words", created=5_000
                ),
                _comment(
                    "c10", uid="u9", handle="ninthfan", text="Final words", created=6_000
                ),
            ],
        ),
    ]


def test_coordination_signals_are_evidence_only_and_include_post_relative_time() -> None:
    report = comment_coordination_signals(_videos())

    assert report["pattern_posture"] == "selected_patterns_observed"
    assert (
        report["paid_or_astroturfed_conclusion"]
        == "not_established_by_comment_telemetry"
    )
    assert report["coverage"]["continuation_video_count"] == 2
    assert report["coverage"]["post_relative_timestamp_comment_count"] == 10
    assert (
        report["signals"]["cross_video_repeated_commenters"][0]["account_id"]
        == "u1"
    )
    assert (
        report["signals"]["exact_text_reuse_across_accounts"][0][
            "distinct_account_count"
        ]
        == 2
    )
    assert (
        report["signals"]["similar_public_handle_pairs"][0]["signal_strength"]
        == "weak_lead_only"
    )
    burst = report["signals"]["post_relative_time_bursts"][0]
    assert burst["distinct_account_count"] == 3
    assert burst["post_relative_window_start_seconds"] == 10
    assert (
        "not proof of payment, astroturfing, common control, or deceptive intent"
        in report["non_claims"]
    )


def test_coordination_signals_unions_recaptures_and_deduplicates_only_same_comment() -> None:
    first = _video(
        "v1",
        1_000,
        [_comment("c1", uid="u1", handle="oneuser", text="first", created=1_010)],
    )
    second = _video(
        "v1",
        1_000,
        [
            _comment("c1", uid="u1", handle="oneuser", text="first", created=1_010),
            _comment("c2", uid="u2", handle="twouser", text="second", created=1_020),
        ],
    )

    report = comment_coordination_signals([first, second])

    assert report["coverage"]["video_count"] == 1
    assert report["coverage"]["captured_comment_count"] == 2
    assert report["coverage"]["deduplicated_recapture_comment_count"] == 1


def test_coordination_signals_fail_loud_on_insufficient_coverage() -> None:
    report = comment_coordination_signals(
        [
            _video(
                "v1",
                1_000,
                [
                    _comment(
                        "c1", uid="u1", handle="oneuser", text="x", created=1_010
                    )
                ],
            )
        ]
    )

    assert report["pattern_posture"] == "insufficient_coverage"
    assert report["signal_family_counts"] == {
        "cross_video_repeated_commenters": 0,
        "exact_text_reuse_across_accounts": 0,
        "similar_public_handle_pairs": 0,
        "post_relative_time_bursts": 0,
    }


def _write_batch_packet(
    root: DataLakeRoot, tmp_path: Path, *, creator: str = "creator"
) -> str:
    payload = {
        "platform": "tiktok",
        "source_surface": TIKTOK_BATCH_CAPTURE_SURFACE,
        "creator_handle": creator,
        "capture_timestamp": "2026-07-19T00:00:00Z",
        "videos": _videos(),
    }
    source = tmp_path / "tiktok_batch_capture.json"
    source.write_text(json.dumps(payload), encoding="utf-8")
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[source],
        source_family="tiktok",
        source_surface=TIKTOK_BATCH_CAPTURE_SURFACE,
        source_locator=known_fact(f"https://www.tiktok.com/@{creator}"),
        decision_question="Test creator comment coordination signals.",
        capture_context="unit test admitted TikTok batch packet",
    )
    return result.packet.packet_id


def _write_creator_map(root: DataLakeRoot, *, creator: str, packet_id: str) -> None:
    table_path = (
        root.path
        / "indexes"
        / "derived_retrieval"
        / "silver_vault"
        / "core"
        / "query_tables"
        / "by_creator.json"
    )
    manifest_path = table_path.parent.parent / "manifests" / "by_creator.json"
    table_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    table_path.write_text(
        json.dumps(
            {
                "creators": {
                    "tiktok": {
                        "unspecified": {creator: {"packets": {packet_id: {}}}}
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    manifest_path.write_text(
        json.dumps(
            {
                "generated_at": "2000-01-01T00:00:00Z",
                "source_high_watermark": "test-watermark",
                "stale_if": "newer availability exists",
            }
        ),
        encoding="utf-8",
    )


def test_lake_runner_resolves_creator_verifies_packet_and_discloses_stale_map(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _write_batch_packet(root, tmp_path)
    _write_creator_map(root, creator="creator", packet_id=packet_id)

    report = build_creator_coordination_report(root, creator_handle="@Creator")

    assert report["selection"]["source"] == "by_creator_map"
    assert report["selection"]["packet_ids"] == [packet_id]
    assert (
        report["selection"]["map_freshness"]["posture"]
        == "stale_by_newer_availability_entry"
    )
    assert report["source_packets"][0]["payload_sha256"]
    assert report["analysis"]["coverage"]["captured_comment_count"] == 10


def test_lake_runner_rejects_changed_raw_payload(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _write_batch_packet(root, tmp_path)
    loaded = root.load_raw_packet(packet_id)
    payload_path = loaded.container / "raw" / "01_tiktok_batch_capture.json"
    original = payload_path.read_text(encoding="utf-8")
    payload_path.write_text(" " + original[1:], encoding="utf-8")

    with pytest.raises(DataLakeRootError, match="sha256 mismatch"):
        build_creator_coordination_report(
            root,
            creator_handle="creator",
            packet_ids=[packet_id],
        )
