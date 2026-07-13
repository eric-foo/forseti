from __future__ import annotations

import json
from pathlib import Path

import pytest

from runners import run_source_capture_tiktok_daily_heartbeat as heartbeat
from runners import run_source_capture_tiktok_daily_heartbeat_control as control
from source_capture.adapters.browser_snapshot import BrowserPageObservationSuccess


def _active_creator(*, account_id: str = "acct-001", handle: str = "@Creator") -> dict[str, str]:
    return {
        "platform": "tiktok",
        "platform_account_id": account_id,
        "handle": handle,
        "monitoring_status": "active",
        "cadence": "daily",
    }


def _session_roster(*, attempt_resume: bool = False) -> dict[str, object]:
    return {
        "creators": [
            {
                "platform": "tiktok",
                "platform_account_id": "acct-001",
                "stable_partition_key": "platform_account_id:acct-001",
                "handle": "creator",
                "attempt_id": "01TESTATTEMPT",
                "attempt_resume": attempt_resume,
            }
        ]
    }


def _capture() -> BrowserPageObservationSuccess:
    return BrowserPageObservationSuccess(
        requested_url="https://www.tiktok.com/@creator",
        final_url="https://www.tiktok.com/@creator",
        title="creator",
        visible_text="",
        dom_observation={"ordered_videos": []},
        responses=[],
        metadata={
            "pre_action_stop_attempts": [],
            "human_challenge_handoff_attempts": [],
        },
        warning_notes=[],
        limitation_notes=[],
    )


def _grid_window() -> dict[str, object]:
    return {
        "creator_handle": "creator",
        "window_size": 1,
        "complete": True,
        "items": [
            {
                "video_id": "101",
                "video_url": "https://www.tiktok.com/@creator/video/101",
                "stats": {"playCount": 100, "diggCount": 10},
            }
        ],
        "collection_receipt": {"capture_timestamp": "2026-07-14T01:02:03Z"},
    }


def test_plan_day_uses_platform_account_identity_and_normalizes_handle(tmp_path: Path) -> None:
    roster = tmp_path / "active.json"
    roster.write_text(json.dumps({"creators": [_active_creator()]}), encoding="utf-8")

    result = control.plan_day(
        active_roster_path=roster,
        run_control_root=tmp_path / "control",
        plan_date="2026-07-14",
        bucket_count=1,
        now_func=lambda: "2026-07-14T00:00:00Z",
    )

    payload = json.loads(result.plan_path.read_text(encoding="utf-8"))
    creator = payload["creators"][0]
    assert creator["platform_account_id"] == "acct-001"
    assert creator["stable_partition_key"] == "platform_account_id:acct-001"
    assert creator["partition_key_source"] == "platform_account_id"
    assert creator["handle"] == "creator"


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("monitoring_status", "paused", "monitoring_status must be active"),
        ("cadence", "weekly", "cadence must be daily"),
    ],
)
def test_plan_day_rejects_non_active_daily_rows(
    tmp_path: Path, field: str, value: str, message: str
) -> None:
    row = _active_creator()
    row[field] = value
    roster = tmp_path / f"{field}.json"
    roster.write_text(json.dumps([row]), encoding="utf-8")

    with pytest.raises(ValueError, match=message):
        control.plan_day(
            active_roster_path=roster,
            run_control_root=tmp_path / "control",
            plan_date="2026-07-14",
        )


def test_grid_only_runner_binds_success_to_attempt_and_preserves_frozen_artifact(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    roster = tmp_path / "session_roster.json"
    roster.write_text(json.dumps(_session_roster()), encoding="utf-8")
    receipt_path = tmp_path / "session" / "receipts.jsonl"
    capture_calls: list[dict[str, object]] = []
    admission_calls: list[dict[str, object]] = []

    def fake_capture(**kwargs: object) -> BrowserPageObservationSuccess:
        capture_calls.append(dict(kwargs))
        return _capture()

    def fake_admit(**kwargs: object) -> tuple[int, str]:
        admission_calls.append(dict(kwargs))
        packet = Path(str(kwargs["output_directory"]))
        packet.mkdir(parents=True)
        (packet / "manifest.json").write_text(
            json.dumps(
                {
                    "packet_id": "01TESTPACKET",
                    "session_identity": kwargs["session_identity"],
                }
            ),
            encoding="utf-8",
        )
        return 0, str(packet)

    monkeypatch.setattr(heartbeat, "capture_tiktok_creator_grid", fake_capture)
    monkeypatch.setattr(heartbeat, "build_tiktok_grid_window", lambda **_kwargs: _grid_window())
    monkeypatch.setattr(heartbeat, "write_tiktok_grid_packet", fake_admit)

    result = heartbeat.run_tiktok_daily_heartbeat(
        roster_path=roster,
        receipt_jsonl=receipt_path,
        lane_id="0",
        lane_count=1,
        output_root=tmp_path / "packets",
        storage_state_path=tmp_path / "state",
        engine=object(),
        partition_preselected=True,
    )

    assert result.succeeded_count == 1
    assert len(capture_calls) == 1
    assert admission_calls[0]["session_identity"] == "01TESTATTEMPT"
    frozen = receipt_path.parent / "attempt_artifacts/01TESTATTEMPT/tiktok_grid_window.json"
    binding = json.loads(frozen.read_text(encoding="utf-8"))["heartbeat_binding"]
    assert binding == {
        "attempt_id": "01TESTATTEMPT",
        "stable_partition_key": "platform_account_id:acct-001",
        "platform_account_id": "acct-001",
    }
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["status"] == "succeeded"
    assert receipt["attempt_id"] == "01TESTATTEMPT"
    assert receipt["packet_id"] == "01TESTPACKET"


def test_resumed_attempt_reuses_bound_frozen_window_without_browser_recapture(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    roster = tmp_path / "session_roster.json"
    roster.write_text(json.dumps(_session_roster(attempt_resume=True)), encoding="utf-8")
    receipt_path = tmp_path / "session" / "receipts.jsonl"
    frozen = receipt_path.parent / "attempt_artifacts/01TESTATTEMPT/tiktok_grid_window.json"
    frozen.parent.mkdir(parents=True)
    window = _grid_window()
    window["heartbeat_binding"] = {
        "attempt_id": "01TESTATTEMPT",
        "stable_partition_key": "platform_account_id:acct-001",
        "platform_account_id": "acct-001",
    }
    frozen.write_text(json.dumps(window), encoding="utf-8")

    monkeypatch.setattr(
        heartbeat,
        "capture_tiktok_creator_grid",
        lambda **_kwargs: pytest.fail("resume with a frozen artifact must not recapture"),
    )

    def fake_admit(**kwargs: object) -> tuple[int, str]:
        packet = Path(str(kwargs["output_directory"]))
        packet.mkdir(parents=True)
        (packet / "manifest.json").write_text(
            json.dumps(
                {
                    "packet_id": "01RESUMEDPACKET",
                    "session_identity": kwargs["session_identity"],
                }
            ),
            encoding="utf-8",
        )
        return 0, str(packet)

    monkeypatch.setattr(heartbeat, "write_tiktok_grid_packet", fake_admit)

    result = heartbeat.run_tiktok_daily_heartbeat(
        roster_path=roster,
        receipt_jsonl=receipt_path,
        lane_id="0",
        lane_count=1,
        output_root=tmp_path / "packets",
        storage_state_path=tmp_path / "state",
        engine=object(),
        partition_preselected=True,
    )

    assert result.succeeded_count == 1
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["reconciled_existing_packet"] is True
    assert receipt["packet_id"] == "01RESUMEDPACKET"
