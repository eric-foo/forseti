from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from capture_spine.creator_profile_current.silver_envelope_core import content_hash
from capture_spine.creator_profile_current.social_metric_history_reader import (
    read_social_metric_history,
)
from capture_spine.creator_profile_current.tiktok_grid_observation_producer import (
    SOCIAL_METRIC_OBSERVATION_SET_LANE,
    TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT,
    observation_set_record_id,
)
from data_lake.consumption import find_acks
from data_lake.root import DataLakeRoot
from runners import run_tiktok_grid_observation_producer as runner
from source_capture.tiktok.grid_packet import write_tiktok_grid_packet
from test_tiktok_creator_metric_seed import _commit_batch_packet, _stats, _video


def _grid_bytes(
    *,
    observed_at: str,
    play_count: int,
    like_count: int,
    comment_count: int | None,
) -> bytes:
    stats = {
        "playCount": play_count,
        "diggCount": like_count,
        "shareCount": 3,
        "collectCount": 4,
    }
    if comment_count is not None:
        stats["commentCount"] = comment_count
    payload = {
        "creator_handle": "creator",
        "window_size": 2,
        "complete": True,
        "items": [
            {
                "video_id": "101",
                "video_url": "https://www.tiktok.com/@creator/video/101",
                "stats": stats,
            },
            {
                "video_id": "102",
                "video_url": "https://www.tiktok.com/@creator/video/102",
                "stats": {
                    "playCount": play_count + 10,
                    "diggCount": like_count + 1,
                    "commentCount": 1,
                },
            },
        ],
        "collection_receipt": {"capture_timestamp": observed_at},
    }
    return json.dumps(payload, separators=(",", ":")).encode("utf-8")


def _admit_grid(
    data_root: DataLakeRoot,
    *,
    observed_at: str,
    play_count: int,
    like_count: int,
    comment_count: int | None,
) -> str:
    code, packet_dir = write_tiktok_grid_packet(
        grid_window_json=_grid_bytes(
            observed_at=observed_at,
            play_count=play_count,
            like_count=like_count,
            comment_count=comment_count,
        ),
        data_root=data_root,
    )
    assert code == 0
    return Path(packet_dir).name


def test_runner_materializes_two_capture_history_with_missing_distinct_from_zero(
    tmp_path: Path,
) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    first_packet = _admit_grid(
        data_root,
        observed_at="2026-07-12T00:00:00Z",
        play_count=100,
        like_count=10,
        comment_count=0,
    )
    second_packet = _admit_grid(
        data_root,
        observed_at="2026-07-13T00:00:00Z",
        play_count=150,
        like_count=15,
        comment_count=None,
    )

    results = runner.run_catchup(data_root=data_root)

    assert {row["packet_id"] for row in results} == {first_packet, second_packet}
    assert all(row["status"] == "derived" for row in results)
    assert all(row["row_count"] == 2 for row in results)
    history = read_social_metric_history(
        data_root=data_root,
        lane=SOCIAL_METRIC_OBSERVATION_SET_LANE,
        policy_fingerprint=TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT,
        record_id_for_anchor=observation_set_record_id,
        platform="tiktok",
        account_native_id="creator",
        content_native_ids=["101"],
    )["101"]
    assert [point.observed_at for point in history] == [
        "2026-07-12T00:00:00Z",
        "2026-07-13T00:00:00Z",
    ]
    assert history[0].metrics["comment_count"]["metric_value"] == 0
    assert history[0].metrics["comment_count"]["metric_posture"]["kind"] == "observed"
    assert history[1].metrics["comment_count"]["metric_value"] is None
    assert history[1].metrics["comment_count"]["metric_posture"] == {
        "kind": "unavailable_with_reason",
        "reason_code": "source_field_absent",
        "reason_detail": (
            "TikTok grid row did not expose commentCount; value was never zero-filled"
        ),
    }

    assert runner.pending_packets(data_root=data_root) == []
    assert runner.run_catchup(data_root=data_root) == []
    for packet_id in (first_packet, second_packet):
        lane = data_root.lane_dir(
            subtree="derived",
            raw_anchor=packet_id,
            lane=SOCIAL_METRIC_OBSERVATION_SET_LANE,
        )
        assert [path.name for path in lane.iterdir()] == [
            observation_set_record_id(packet_id)
        ]


def test_history_reader_requires_the_exact_policy_fingerprint(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _admit_grid(
        data_root,
        observed_at="2026-07-12T00:00:00Z",
        play_count=100,
        like_count=10,
        comment_count=2,
    )
    assert all(row["status"] == "derived" for row in runner.run_catchup(data_root=data_root))

    history = read_social_metric_history(
        data_root=data_root,
        lane=SOCIAL_METRIC_OBSERVATION_SET_LANE,
        policy_fingerprint="f" * 64,
        record_id_for_anchor=observation_set_record_id,
        platform="tiktok",
        account_native_id="creator",
        content_native_ids=["101"],
    )

    assert history == {"101": []}


def test_history_reader_rejects_tampered_exact_policy_record(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _admit_grid(
        data_root,
        observed_at="2026-07-12T00:00:00Z",
        play_count=100,
        like_count=10,
        comment_count=2,
    )
    assert all(row["status"] == "derived" for row in runner.run_catchup(data_root=data_root))
    path = data_root.record_path(
        subtree="derived",
        raw_anchor=packet_id,
        lane=SOCIAL_METRIC_OBSERVATION_SET_LANE,
        record_id=observation_set_record_id(packet_id),
    )
    record = json.loads(path.read_text(encoding="utf-8"))
    record["payload"]["observation"]["rows"][0]["metrics"]["view_count"][
        "metric_value"
    ] = 999
    path.write_text(json.dumps(record), encoding="utf-8")

    with pytest.raises(ValueError, match="content hash mismatch"):
        read_social_metric_history(
            data_root=data_root,
            lane=SOCIAL_METRIC_OBSERVATION_SET_LANE,
            policy_fingerprint=TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT,
            record_id_for_anchor=observation_set_record_id,
            platform="tiktok",
            account_native_id="creator",
            content_native_ids=["101"],
        )


def test_history_reader_fails_loud_on_wrong_policy_record_at_exact_policy_path(
    tmp_path: Path,
) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _admit_grid(
        data_root,
        observed_at="2026-07-12T00:00:00Z",
        play_count=100,
        like_count=10,
        comment_count=2,
    )
    assert all(row["status"] == "derived" for row in runner.run_catchup(data_root=data_root))
    path = data_root.record_path(
        subtree="derived",
        raw_anchor=packet_id,
        lane=SOCIAL_METRIC_OBSERVATION_SET_LANE,
        record_id=observation_set_record_id(packet_id),
    )
    record = json.loads(path.read_text(encoding="utf-8"))
    record["payload"]["observation"]["policy_fingerprint_sha256"] = "f" * 64
    record["content_hash"] = f"sha256:{content_hash(record)}"
    path.write_text(json.dumps(record), encoding="utf-8")

    with pytest.raises(ValueError, match="different policy fingerprint"):
        read_social_metric_history(
            data_root=data_root,
            lane=SOCIAL_METRIC_OBSERVATION_SET_LANE,
            policy_fingerprint=TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT,
            record_id_for_anchor=observation_set_record_id,
            platform="tiktok",
            account_native_id="creator",
            content_native_ids=["101"],
        )


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


def test_history_reader_rejects_equal_time_siblings(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    for play_count in (100, 150):
        _admit_grid(
            data_root,
            observed_at="2026-07-12T00:00:00Z",
            play_count=play_count,
            like_count=10,
            comment_count=2,
        )
    assert all(row["status"] == "derived" for row in runner.run_catchup(data_root=data_root))

    with pytest.raises(ValueError, match="ambiguous equal-time"):
        read_social_metric_history(
            data_root=data_root,
            lane=SOCIAL_METRIC_OBSERVATION_SET_LANE,
            policy_fingerprint=TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT,
            record_id_for_anchor=observation_set_record_id,
            platform="tiktok",
            account_native_id="creator",
            content_native_ids=["101"],
        )


def test_runner_acknowledges_non_grid_tiktok_packet_as_not_applicable(
    tmp_path: Path,
) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _commit_batch_packet(
        data_root,
        videos=[_video("7655162561783975199", stats=_stats(100, 10, 2))],
    )

    assert runner.run_catchup(data_root=data_root) == [
        {"packet_id": packet_id, "status": "not_applicable"}
    ]
    acks = find_acks(
        data_root,
        raw_anchor=packet_id,
        ack_namespace=SOCIAL_METRIC_OBSERVATION_SET_LANE,
    )
    assert len(acks) == 1
    assert acks[0]["evidence"][0]["kind"] == "not_applicable_no_tiktok_grid_window"
    assert runner.pending_packets(data_root=data_root) == []


def test_runner_does_not_ack_when_silver_persistence_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    packet_id = _admit_grid(
        data_root,
        observed_at="2026-07-12T00:00:00Z",
        play_count=100,
        like_count=10,
        comment_count=2,
    )
    monkeypatch.setattr(
        runner,
        "derive_tiktok_grid_observation_set",
        lambda **_kwargs: (_ for _ in ()).throw(OSError("simulated persistence failure")),
    )

    result = runner.run_catchup(data_root=data_root)

    assert result[0]["packet_id"] == packet_id
    assert result[0]["status"] == "failed"
    assert "simulated persistence failure" in result[0]["error"]
    assert find_acks(
        data_root,
        raw_anchor=packet_id,
        ack_namespace=SOCIAL_METRIC_OBSERVATION_SET_LANE,
    ) == []
    assert runner.pending_packets(data_root=data_root) == [packet_id]
