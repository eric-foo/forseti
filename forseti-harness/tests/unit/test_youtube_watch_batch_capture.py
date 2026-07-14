"""Unit tests for the ledger-driven YouTube watch batch-capture wrapper.

Everything runs lake-free: capture is an injected callable (writing REAL
packets into a ``DataLakeRoot.for_test`` lake for success paths, or failing on
command), pacing is an injected ``sleep_fn``, and the clock is an injected
``now_fn``. The red paths are the point: consecutive-failure break,
consecutive-non-playable break, cooldown refusal, and the
visibly-incomplete-sweep exit — a wrapper whose guards cannot fire would be
ceremony around a blocking hazard."""
from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot
from runners.run_source_capture_youtube_watch_batch import (
    YOUTUBE_WATCH_BATCH_EXIT_CODE_BREAK,
    admitted_pool_video_ids,
    run_youtube_watch_batch,
)
from source_capture.youtube_watch_packet import YoutubeWatchFetch, write_youtube_watch_packet

ALPHA_CHANNEL = "UCalphaAlphaAlphaAlpha01"
POOL = ("vidAlpha001", "vidAlpha002", "vidAlpha003")


def _creator_ledger(*, include_brand_row: bool = False, retire: tuple[str, ...] = ()) -> dict:
    video_ids = list(POOL)
    pool_ids = [f"yt-frag-pool200-{index:03d}" for index in range(1, len(video_ids) + 1)]
    observations = [
        {
            "creator_observation_id": "yt_creator_obs_alpha",
            "platform_subject_key": ALPHA_CHANNEL,
            "creator_handle_query": "@alphafrag",
            "creator_classification": "creator_or_channel_observed",
            "pool_ids": pool_ids,
            "video_ids": video_ids,
        }
    ]
    if include_brand_row:
        observations.append(
            {
                "creator_observation_id": "yt_creator_obs_brand",
                "platform_subject_key": "UCbrandBrandBrandBrand01",
                "creator_handle_query": "@somebrand",
                "creator_classification": "brand_or_platform_account_observed",
                "pool_ids": ["yt-frag-pool200-099"],
                "video_ids": ["vidBrand0001"],
            }
        )
    wrapper: dict = {"creator_observations": observations}
    if retire:
        wrapper["operator_video_retirements"] = [
            {
                "video_id": video_id,
                "reason": "video unavailable (fixture retirement)",
                "retired_at_utc": "2026-07-03T00:00:00Z",
                "evidence_packet_ids": ["01KWH1TR2QY5VRNYTPNNJY18QV"],
            }
            for video_id in retire
        ]
    return {"youtube_creator_observation_ledger": wrapper}


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


def _write_real_packet(
    data_root: DataLakeRoot, *, video_id: str, video_state: str, captured_at: str
) -> tuple[int, str]:
    playable = video_state == "playable"
    packet = {
        "video_id": video_id,
        "surface_type": "watch",
        "watch_url": f"https://www.youtube.com/watch?v={video_id}",
        "canonical_url": f"https://www.youtube.com/watch?v={video_id}",
        "channel": {"channel_id": ALPHA_CHANNEL, "author": "fixture"},
        "metadata": {"title": f"fixture {video_id}", "publish_date": "2026-06-20"},
        "engagement": {"view_count": 100} if playable else {},
        "availability": {"video_state": video_state, "comments_state": "comments_not_exposed"},
        "metric_receipts": {
            "view_count": (
                _observed_receipt(100) if playable else _unavailable_receipt("video unavailable")
            ),
            "like_count": _unavailable_receipt("not exposed in fixture"),
            "total_comment_count": _unavailable_receipt("not exposed in fixture"),
            "comment_sample_count": _unavailable_receipt("not exposed in fixture"),
        },
        "comments_posture": "comments_not_exposed",
        "comments": [],
        "comment_capture_coverage": {
            "requested_page_limit": 1,
            "pages_fetched": 0,
            "selected_comment_count": 0,
            "continuation_remaining_after_stop": False,
            "ordering_posture": "source_default_order_as_served",
        },
        "receipts": {"http_status": 200, "retrieval_time_utc": captured_at},
    }
    return write_youtube_watch_packet(
        YoutubeWatchFetch(
            video_id=video_id,
            raw_watch_html=f"<html>{video_id}@{captured_at}</html>".encode(),
            packet=packet,
        ),
        data_root=data_root,
        decision_question="batch wrapper test",
        now_iso=captured_at,
    )


class _Clock:
    def __init__(self) -> None:
        self._now = datetime(2026, 7, 2, 12, 0, 0, tzinfo=UTC)

    def __call__(self) -> datetime:
        self._now += timedelta(seconds=1)
        return self._now


def _capture_recorder(data_root: DataLakeRoot, *, outcomes: dict[str, str]):
    """outcomes[video_id]: 'playable' | 'nonplayable' | 'fail' | 'raise'."""
    calls: list[str] = []

    def capture_fn(*, video_id: str, data_root: DataLakeRoot, decision_question: str, comment_pages: int):
        calls.append(video_id)
        outcome = outcomes.get(video_id, "playable")
        if outcome == "raise":
            raise ConnectionError(f"transport down for {video_id}")
        if outcome == "fail":
            return 3, f"simulated capture failure for {video_id}"
        state = "playable" if outcome == "playable" else "removed_or_unavailable"
        return _write_real_packet(
            data_root, video_id=video_id, video_state=state, captured_at=f"2026-07-02T09:00:0{len(calls)}Z"
        )

    return capture_fn, calls


def _run(data_root: DataLakeRoot, tmp_path: Path, *, outcomes: dict[str, str], **kwargs):
    capture_fn, calls = _capture_recorder(data_root, outcomes=outcomes)
    sleeps: list[float] = []
    defaults = dict(
        creator_ledger=_creator_ledger(),
        pace_seconds=7.5,
        output_root=tmp_path / "batch_out",
        cooldown_ledger_path=tmp_path / "cooldown.json",
        capture_fn=capture_fn,
        sleep_fn=sleeps.append,
        now_fn=_Clock(),
    )
    defaults.update(kwargs)
    exit_code, summary_path = run_youtube_watch_batch(data_root, **defaults)
    summary = json.loads(Path(summary_path).read_text(encoding="utf-8"))
    return exit_code, summary, calls, sleeps


def test_complete_sweep_exits_zero_and_paces_between_attempts(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    exit_code, summary, calls, sleeps = _run(data_root, tmp_path, outcomes={})
    assert exit_code == 0
    assert summary["status"] == "completed"
    assert calls == list(POOL)
    # Pacing fires exactly between attempts: attempts-1 sleeps of the pace value.
    assert sleeps == [7.5, 7.5]
    assert summary["counts"] == {
        "pool_total": 3,
        "attempted": 3,
        "captured": 3,
        "skipped_resume": 0,
        "skipped_ledger_retired": 0,
        "capture_failed": 0,
        "not_attempted": 0,
    }
    for row in summary["results"]:
        assert row["status"] == "captured"
        assert row["video_state_or_none"] == "playable"
        # packet_ref is the committed packet id, readable from the lake.
        assert data_root.find_packet(row["packet_ref_or_error"]) is not None
    assert not (tmp_path / "cooldown.json").exists()


def test_ledger_retired_videos_are_never_recaptured(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    exit_code, summary, calls, sleeps = _run(
        data_root,
        tmp_path,
        outcomes={},
        creator_ledger=_creator_ledger(retire=("vidAlpha002",)),
    )
    assert exit_code == 0
    assert summary["status"] == "completed"
    # the retired video is skipped before any capture attempt or pacing
    assert calls == ["vidAlpha001", "vidAlpha003"]
    assert sleeps == [7.5]
    assert summary["counts"]["skipped_ledger_retired"] == 1
    assert summary["counts"]["captured"] == 2
    assert summary["ledger_retired_video_ids"] == ["vidAlpha002"]
    retired_row = next(r for r in summary["results"] if r["video_id"] == "vidAlpha002")
    assert retired_row["status"] == "skipped_ledger_retired"
    assert retired_row["attempted_at"] is None


def test_all_videos_retired_refuses_noop_sweep(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    with pytest.raises(ValueError, match="retires every admitted video"):
        _run(
            data_root,
            tmp_path,
            outcomes={},
            creator_ledger=_creator_ledger(retire=POOL),
        )


def test_retirement_outside_pool_fails_closed(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    with pytest.raises(ValueError, match="outside the admitted pool"):
        _run(
            data_root,
            tmp_path,
            outcomes={},
            creator_ledger=_creator_ledger(retire=("vidUnknown99",)),
        )


def test_isolated_failure_continues_but_sweep_is_visibly_incomplete(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    exit_code, summary, calls, _sleeps = _run(
        data_root, tmp_path, outcomes={"vidAlpha002": "fail"}
    )
    assert exit_code == 2  # never a quiet success: producer needs 100% coverage
    assert summary["status"] == "completed_with_failures"
    assert calls == list(POOL)  # the sweep continued past the failure
    assert summary["failed_video_ids"] == ["vidAlpha002"]
    assert not (tmp_path / "cooldown.json").exists()


def test_consecutive_failures_trip_break_and_write_cooldown(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    exit_code, summary, calls, _sleeps = _run(
        data_root,
        tmp_path,
        outcomes={"vidAlpha001": "raise", "vidAlpha002": "fail"},
        break_after_failures=2,
    )
    assert exit_code == YOUTUBE_WATCH_BATCH_EXIT_CODE_BREAK
    assert summary["status"] == "stopped_circuit_break"
    assert "consecutive capture failures" in summary["break_reason_or_none"]
    assert calls == ["vidAlpha001", "vidAlpha002"]  # vidAlpha003 never attempted
    assert summary["counts"]["not_attempted"] == 1
    cooldown = json.loads((tmp_path / "cooldown.json").read_text(encoding="utf-8"))
    assert cooldown["trigger_video_id"] == "vidAlpha002"
    assert cooldown["cooldown_seconds"] == 3600.0


def test_success_resets_failure_streak(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    exit_code, summary, calls, _sleeps = _run(
        data_root,
        tmp_path,
        outcomes={"vidAlpha001": "fail", "vidAlpha003": "fail"},
        break_after_failures=2,
    )
    # fail, success, fail: never two consecutive -> no break, incomplete sweep.
    assert exit_code == 2
    assert summary["status"] == "completed_with_failures"
    assert calls == list(POOL)
    assert summary["failed_video_ids"] == ["vidAlpha001", "vidAlpha003"]


def test_consecutive_nonplayable_packets_trip_soft_block_break(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    exit_code, summary, calls, _sleeps = _run(
        data_root,
        tmp_path,
        outcomes={"vidAlpha001": "nonplayable", "vidAlpha002": "nonplayable"},
        break_after_nonplayable=2,
    )
    assert exit_code == YOUTUBE_WATCH_BATCH_EXIT_CODE_BREAK
    assert summary["status"] == "stopped_circuit_break"
    assert "non-playable" in summary["break_reason_or_none"]
    assert calls == ["vidAlpha001", "vidAlpha002"]
    # The packets ARE committed (unavailability is data); the break is about the streak.
    committed = [row for row in summary["results"] if row["status"] == "captured"]
    assert len(committed) == 2
    assert all(row["video_state_or_none"] == "removed_or_unavailable" for row in committed)


def test_playable_resets_nonplayable_streak(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    exit_code, summary, _calls, _sleeps = _run(
        data_root,
        tmp_path,
        outcomes={"vidAlpha001": "nonplayable", "vidAlpha003": "nonplayable"},
        break_after_nonplayable=2,
    )
    assert exit_code == 0  # all packets committed; no streak reached the threshold
    assert summary["status"] == "completed"


def test_active_cooldown_refuses_and_ignore_flag_overrides(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    cooldown_path = tmp_path / "cooldown.json"
    cooldown_path.write_text(
        json.dumps(
            {
                "runner": "youtube_watch_batch",
                "cooldown_until": "2026-07-02T13:00:00Z",  # after the injected clock start
            }
        ),
        encoding="utf-8",
    )
    exit_code, summary, calls, _sleeps = _run(data_root, tmp_path, outcomes={})
    assert exit_code == YOUTUBE_WATCH_BATCH_EXIT_CODE_BREAK
    assert summary["status"] == "cooldown_active"
    assert calls == []  # nothing attempted under active cooldown

    exit_code, summary, calls, _sleeps = _run(
        data_root, tmp_path, outcomes={}, ignore_cooldown=True
    )
    assert exit_code == 0
    assert summary["status"] == "completed"
    assert calls == list(POOL)


def test_resume_skips_previously_captured_videos(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    # First run: vidAlpha002 fails -> incomplete sweep.
    exit_code, first_summary, _calls, _sleeps = _run(
        data_root, tmp_path, outcomes={"vidAlpha002": "fail"}
    )
    assert exit_code == 2
    first_summary_path = sorted((tmp_path / "batch_out").glob("*.json"))[0]

    # Resume: only the failed video is re-attempted; no pacing needed for one attempt.
    capture_fn, calls = _capture_recorder(data_root, outcomes={})
    sleeps: list[float] = []
    exit_code, summary_path = run_youtube_watch_batch(
        data_root,
        creator_ledger=_creator_ledger(),
        pace_seconds=7.5,
        resume_from=first_summary_path,
        output_root=tmp_path / "batch_out_resume",
        cooldown_ledger_path=tmp_path / "cooldown.json",
        capture_fn=capture_fn,
        sleep_fn=sleeps.append,
        now_fn=_Clock(),
    )
    summary = json.loads(Path(summary_path).read_text(encoding="utf-8"))
    assert exit_code == 0
    assert summary["status"] == "completed"
    assert calls == ["vidAlpha002"]
    assert sleeps == []
    assert summary["counts"]["skipped_resume"] == 2
    assert summary["counts"]["captured"] == 1


def test_pool_extraction_excludes_brand_rows_and_keeps_pool_order(tmp_path: Path) -> None:
    pool = admitted_pool_video_ids(_creator_ledger(include_brand_row=True))
    assert pool == list(POOL)


def test_invalid_thresholds_fail_closed(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    with pytest.raises(ValueError, match="break_after_failures"):
        run_youtube_watch_batch(
            data_root,
            creator_ledger=_creator_ledger(),
            break_after_failures=0,
            capture_fn=lambda **_: (0, "unused"),
            sleep_fn=lambda _s: None,
            now_fn=_Clock(),
            output_root=tmp_path / "out",
            cooldown_ledger_path=tmp_path / "cooldown.json",
        )
