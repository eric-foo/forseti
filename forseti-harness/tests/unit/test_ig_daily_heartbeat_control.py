from __future__ import annotations

import json
from pathlib import Path

import pytest

from runners import run_source_capture_ig_daily_heartbeat_control as control
from runners import run_source_capture_ig_daily_heartbeat_operator as operator_runner


def _write_json(path: Path, payload: object) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _planned_row_for_lane(target_lane: str, handle: str) -> dict[str, object]:
    for index in range(1000):
        account_id = f"acct_{handle}_{index}"
        stable_key = f"platform_account_id:{account_id}"
        if control.assign_heartbeat_lane_id(stable_key, 2) == target_lane:
            return {
                "platform": "instagram",
                "platform_account_id": account_id,
                "creator_record_id": f"creator_{handle}",
                "handle": handle,
                "monitoring_status_at_plan": "active",
                "cadence_at_plan": "daily",
                "stable_partition_key": stable_key,
                "partition_key_source": "platform_account_id",
                "bucket": 1,
            }
    raise AssertionError(f"could not find a key for {target_lane}")


class _FakeHeartbeatResult:
    exit_code = 0

    def message(self) -> str:
        return "fake heartbeat complete"


def test_plan_day_uses_registry_sidecar_and_writes_navigable_control_folder(tmp_path: Path) -> None:
    registry = _write_json(
        tmp_path / "registry.json",
        {
            "creator_registry_index": {
                "platform_accounts": [
                    {
                        "platform": "instagram",
                        "platform_account_id": "acct_ig_one",
                        "platform_public_account_id_or_none": "111",
                        "normalized_public_handle": "one",
                        "public_profile_url": "https://www.instagram.com/one/",
                        "creator_record_id_or_none": "creator_one",
                    },
                    {
                        "platform": "instagram",
                        "platform_account_id": "acct_ig_two",
                        "normalized_public_handle": "two",
                    },
                    {
                        "platform": "youtube",
                        "platform_account_id": "acct_yt",
                        "normalized_public_handle": "yt",
                    },
                ]
            }
        },
    )
    sidecar = _write_json(
        tmp_path / "sidecar.json",
        {
            "ig_daily_monitoring_sidecar": {
                "accounts": [
                    {"platform_account_id": "acct_ig_one", "monitoring_status": "active", "cadence": "daily"},
                    {"platform_account_id": "acct_ig_two", "monitoring_status": "paused", "cadence": "daily"},
                ]
            }
        },
    )

    result = control.plan_day(
        registry_index_path=registry,
        monitoring_sidecar_path=sidecar,
        run_control_root=tmp_path / "lake",
        plan_date="2026-07-09",
        now_func=lambda: "2026-07-09T00:00:00Z",
    )

    assert result.planned_count == 1
    expected_dir = tmp_path / "lake" / "run_control" / "ig_daily_heartbeat" / "2026-07-09"
    assert result.plan_path == expected_dir / "daily_plan.json"
    assert result.attempts_path == expected_dir / "attempts.jsonl"
    plan = _read_json(result.plan_path)
    creators = plan["creators"]
    assert len(creators) == 1
    assert creators[0]["platform_account_id"] == "acct_ig_one"
    assert creators[0]["bucket"] in {1, 2, 3, 4}
    assert plan["storage_namespace"] == "run_control/ig_daily_heartbeat/2026-07-09"
    assert "not Silver" in plan["non_claims"]


def test_daily_bucket_assignment_is_reproducible_and_date_seeded() -> None:
    keys = [f"platform_account_id:acct_{index}" for index in range(20)]
    day_one = [control.assign_daily_bucket(key, plan_date="2026-07-09") for key in keys]
    day_one_repeat = [control.assign_daily_bucket(key, plan_date="2026-07-09") for key in keys]
    day_two = [control.assign_daily_bucket(key, plan_date="2026-07-10") for key in keys]

    assert day_one == day_one_repeat
    assert set(day_one) <= {1, 2, 3, 4}
    assert day_one != day_two


def test_run_session_writes_roster_skips_terminal_attempts_and_appends_outcomes(tmp_path: Path) -> None:
    day_dir = control.day_directory(tmp_path / "lake", "2026-07-09")
    plan_path = _write_json(
        day_dir / "daily_plan.json",
        {
            "schema_version": control.PLAN_SCHEMA_VERSION,
            "run_control_version": control.RUN_CONTROL_VERSION,
            "plan_id": "plan_test",
            "plan_date": "2026-07-09",
            "bucket_count": 4,
            "creators": [
                {
                    "platform": "instagram",
                    "platform_account_id": "acct_one",
                    "creator_record_id": "creator_one",
                    "handle": "one",
                    "monitoring_status_at_plan": "active",
                    "cadence_at_plan": "daily",
                    "stable_partition_key": "platform_account_id:acct_one",
                    "partition_key_source": "platform_account_id",
                    "bucket": 2,
                },
                {
                    "platform": "instagram",
                    "platform_account_id": "acct_two",
                    "creator_record_id": "creator_two",
                    "handle": "two",
                    "monitoring_status_at_plan": "active",
                    "cadence_at_plan": "daily",
                    "stable_partition_key": "platform_account_id:acct_two",
                    "partition_key_source": "platform_account_id",
                    "bucket": 2,
                },
            ],
        },
    )
    assert plan_path.exists()
    control.append_attempt(
        day_dir / "attempts.jsonl",
        {
            "schema_version": control.ATTEMPT_SCHEMA_VERSION,
            "plan_id": "plan_test",
            "plan_date": "2026-07-09",
            "timestamp_utc": "2026-07-09T01:00:00Z",
            "session_id": "prior",
            "bucket": 2,
            "stable_partition_key": "platform_account_id:acct_one",
            "platform_account_id": "acct_one",
            "handle_at_plan": "one",
            "attempt_status": "succeeded",
            "actor": "test",
        },
    )

    def fake_heartbeat_runner(**kwargs: object) -> _FakeHeartbeatResult:
        roster = _read_json(Path(kwargs["roster_path"]))
        assert [row["handle"] for row in roster["creators"]] == ["two"]
        receipt_path = Path(kwargs["receipt_jsonl"])
        receipt_path.write_text(
            json.dumps(
                {
                    "run_id": "run_001",
                    "status": "succeeded",
                    "creator": {"handle": "two"},
                    "packet_pointer": "packet_two",
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        return _FakeHeartbeatResult()

    result = control.run_session(
        run_control_root=tmp_path / "lake",
        plan_date="2026-07-09",
        bucket=2,
        lane_id="lane_1",
        lane_count=1,
        output_root=tmp_path / "packets",
        heartbeat_runner=fake_heartbeat_runner,
        session_id="session_two",
        now_func=lambda: "2026-07-09T02:00:00Z",
    )

    assert result.selected_count == 1
    assert result.duplicate_prevented_count == 1
    roster = _read_json(result.session_roster_path)
    assert [row["platform_account_id"] for row in roster["creators"]] == ["acct_two"]
    attempts = _read_jsonl(result.attempts_path)
    assert [row["attempt_status"] for row in attempts] == ["succeeded", "leased", "started", "succeeded"]
    summary = _read_json(result.session_summary_path)
    assert summary["selected_count"] == 1
    assert summary["duplicate_prevented_count"] == 1
    assert summary["succeeded_count"] == 1


def test_run_session_matches_receipt_by_partition_key_when_handle_differs(tmp_path: Path) -> None:
    day_dir = control.day_directory(tmp_path / "lake", "2026-07-09")
    _write_json(
        day_dir / "daily_plan.json",
        {
            "schema_version": control.PLAN_SCHEMA_VERSION,
            "run_control_version": control.RUN_CONTROL_VERSION,
            "plan_id": "plan_key_match",
            "plan_date": "2026-07-09",
            "bucket_count": 4,
            "creators": [
                {
                    "platform": "instagram",
                    "platform_account_id": "acct_one",
                    "creator_record_id": "creator_one",
                    "handle": "one",
                    "monitoring_status_at_plan": "active",
                    "cadence_at_plan": "daily",
                    "stable_partition_key": "platform_account_id:acct_one",
                    "partition_key_source": "platform_account_id",
                    "bucket": 1,
                }
            ],
        },
    )

    def fake_heartbeat_runner(**kwargs: object) -> _FakeHeartbeatResult:
        receipt_path = Path(kwargs["receipt_jsonl"])
        receipt_path.write_text(
            json.dumps(
                {
                    "run_id": "run_key",
                    "status": "succeeded",
                    "partition_key": "platform_account_id:acct_one",
                    "creator": {"handle": "@ONE"},
                    "packet_pointer": "packet_one",
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        return _FakeHeartbeatResult()

    result = control.run_session(
        run_control_root=tmp_path / "lake",
        plan_date="2026-07-09",
        bucket=1,
        lane_id="lane_1",
        lane_count=1,
        output_root=tmp_path / "packets",
        heartbeat_runner=fake_heartbeat_runner,
        session_id="session_key",
        now_func=lambda: "2026-07-09T02:00:00Z",
    )

    attempts = _read_jsonl(result.attempts_path)
    assert [row["attempt_status"] for row in attempts] == ["leased", "started", "succeeded"]
    assert attempts[-1]["stable_partition_key"] == "platform_account_id:acct_one"
    summary = _read_json(result.session_summary_path)
    assert summary["succeeded_count"] == 1

def test_run_session_leases_only_requested_lane_within_bucket(tmp_path: Path) -> None:
    lane_one = _planned_row_for_lane("lane_1", "lane_one")
    lane_two = _planned_row_for_lane("lane_2", "lane_two")
    day_dir = control.day_directory(tmp_path / "lake", "2026-07-09")
    _write_json(
        day_dir / "daily_plan.json",
        {
            "schema_version": control.PLAN_SCHEMA_VERSION,
            "run_control_version": control.RUN_CONTROL_VERSION,
            "plan_id": "plan_lanes",
            "plan_date": "2026-07-09",
            "bucket_count": 4,
            "creators": [lane_one, lane_two],
        },
    )

    def fake_heartbeat_runner(**kwargs: object) -> _FakeHeartbeatResult:
        roster = _read_json(Path(kwargs["roster_path"]))
        assert [row["handle"] for row in roster["creators"]] == ["lane_one"]
        receipt_path = Path(kwargs["receipt_jsonl"])
        receipt_path.write_text(
            json.dumps(
                {
                    "run_id": "run_lane",
                    "status": "succeeded",
                    "creator": {"handle": "lane_one"},
                    "packet_pointer": "packet_lane_one",
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        return _FakeHeartbeatResult()

    result = control.run_session(
        run_control_root=tmp_path / "lake",
        plan_date="2026-07-09",
        bucket=1,
        lane_id="lane_1",
        lane_count=2,
        output_root=tmp_path / "packets",
        heartbeat_runner=fake_heartbeat_runner,
        session_id="session_lane_one",
        now_func=lambda: "2026-07-09T02:00:00Z",
    )

    assert result.selected_count == 1
    assert result.skipped_by_lane_in_bucket_count == 1
    attempts = _read_jsonl(result.attempts_path)
    assert [row["handle_at_plan"] for row in attempts] == ["lane_one", "lane_one", "lane_one"]
    assert [row["attempt_status"] for row in attempts] == ["leased", "started", "succeeded"]
    summary = _read_json(result.session_summary_path)
    assert summary["skipped_by_lane_in_bucket_count"] == 1


def test_run_session_isolates_session_artifacts_per_lane_within_bucket(tmp_path: Path) -> None:
    # Two lanes in the same bucket run sequentially (bucket-scoped lock) but must NOT clobber each
    # other's session roster/receipts/summary. Regression for APH-IMPL-1 (files were keyed by bucket
    # only) + APH-IMPL-3 (receipt_pointer was always null).
    lane_one = _planned_row_for_lane("lane_1", "lane_one")
    lane_two = _planned_row_for_lane("lane_2", "lane_two")
    day_dir = control.day_directory(tmp_path / "lake", "2026-07-09")
    _write_json(
        day_dir / "daily_plan.json",
        {
            "schema_version": control.PLAN_SCHEMA_VERSION,
            "run_control_version": control.RUN_CONTROL_VERSION,
            "plan_id": "plan_lanes",
            "plan_date": "2026-07-09",
            "bucket_count": 4,
            "creators": [lane_one, lane_two],
        },
    )

    def make_fake(handle: str):
        def fake_heartbeat_runner(**kwargs: object) -> _FakeHeartbeatResult:
            Path(kwargs["receipt_jsonl"]).write_text(
                json.dumps(
                    {
                        "run_id": f"run_{handle}",
                        "status": "succeeded",
                        "creator": {"handle": handle},
                        "packet_pointer": f"packet_{handle}",
                    },
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
            return _FakeHeartbeatResult()

        return fake_heartbeat_runner

    common = dict(
        run_control_root=tmp_path / "lake",
        plan_date="2026-07-09",
        bucket=1,
        lane_count=2,
        output_root=tmp_path / "packets",
        now_func=lambda: "2026-07-09T02:00:00Z",
    )
    result_one = control.run_session(
        lane_id="lane_1", heartbeat_runner=make_fake("lane_one"), session_id="session_lane_one", **common
    )
    result_two = control.run_session(
        lane_id="lane_2", heartbeat_runner=make_fake("lane_two"), session_id="session_lane_two", **common
    )

    # Distinct per-lane files -- lane_2 did not overwrite lane_1's session artifacts.
    assert result_one.session_roster_path != result_two.session_roster_path
    assert result_one.session_summary_path != result_two.session_summary_path
    assert result_one.receipt_jsonl != result_two.receipt_jsonl
    assert "lane_1" in result_one.session_summary_path.name
    assert "lane_2" in result_two.session_summary_path.name
    assert result_one.session_roster_path.exists()
    assert result_two.session_roster_path.exists()

    # Each lane's roster survived intact (no clobber).
    assert [row["handle"] for row in _read_json(result_one.session_roster_path)["creators"]] == ["lane_one"]
    assert [row["handle"] for row in _read_json(result_two.session_roster_path)["creators"]] == ["lane_two"]

    # receipt_pointer is populated (APH-IMPL-3): points at a lane's receipt file, never null.
    succeeded_pointers = [
        row.get("receipt_pointer")
        for row in _read_jsonl(result_two.attempts_path)
        if row["attempt_status"] == "succeeded"
    ]
    assert succeeded_pointers, "expected at least one succeeded attempt row"
    assert all(pointer is not None for pointer in succeeded_pointers)
    assert str(result_two.receipt_jsonl) in succeeded_pointers


def test_run_session_refuses_unexpired_bucket_lock(tmp_path: Path) -> None:
    day_dir = control.day_directory(tmp_path / "lake", "2026-07-09")
    _write_json(
        day_dir / "daily_plan.json",
        {
            "schema_version": control.PLAN_SCHEMA_VERSION,
            "plan_id": "plan_test",
            "plan_date": "2026-07-09",
            "bucket_count": 4,
            "creators": [],
        },
    )
    (day_dir / "attempts.jsonl").write_text("", encoding="utf-8")
    (day_dir / "session_1.lock").write_text("locked", encoding="utf-8")

    with pytest.raises(ValueError, match="session lock already exists"):
        control.run_session(
            run_control_root=tmp_path / "lake",
            plan_date="2026-07-09",
            bucket=1,
            lane_id="lane_1",
            lane_count=1,
            output_root=tmp_path / "packets",
            heartbeat_runner=lambda **_: _FakeHeartbeatResult(),
            lease_stale_seconds=999999,
        )


def test_summarize_day_counts_terminal_attempts(tmp_path: Path) -> None:
    day_dir = control.day_directory(tmp_path / "lake", "2026-07-09")
    _write_json(
        day_dir / "daily_plan.json",
        {
            "schema_version": control.PLAN_SCHEMA_VERSION,
            "plan_id": "plan_test",
            "plan_date": "2026-07-09",
            "bucket_count": 4,
            "creators": [
                {"stable_partition_key": "one"},
                {"stable_partition_key": "two"},
                {"stable_partition_key": "three"},
            ],
        },
    )
    attempts = day_dir / "attempts.jsonl"
    control.append_attempt(attempts, {"stable_partition_key": "one", "attempt_status": "leased"})
    control.append_attempt(attempts, {"stable_partition_key": "one", "attempt_status": "succeeded"})
    control.append_attempt(attempts, {"stable_partition_key": "two", "attempt_status": "access_gap"})

    result = control.summarize_day(
        run_control_root=tmp_path / "lake",
        plan_date="2026-07-09",
        now_func=lambda: "2026-07-09T23:59:00Z",
    )

    summary = _read_json(result.summary_path)
    assert summary["planned_count"] == 3
    assert summary["attempted_count"] == 2
    assert summary["succeeded_count"] == 1
    assert summary["access_gap_count"] == 1
    assert summary["missed_count"] == 1
    assert summary["non_claims"] == ["operational coverage summary only", "not Silver", "not Gold"]

def test_operator_session_plans_runs_one_bucket_and_summarizes(tmp_path: Path) -> None:
    registry = _write_json(
        tmp_path / "registry.json",
        {
            "creator_registry_index": {
                "platform_accounts": [
                    {
                        "platform": "instagram",
                        "platform_account_id": "acct_operator_one",
                        "normalized_public_handle": "operator_one",
                        "creator_record_id_or_none": "creator_operator_one",
                    }
                ]
            }
        },
    )
    sidecar = _write_json(
        tmp_path / "sidecar.json",
        {
            "ig_daily_monitoring_sidecar": {
                "accounts": [
                    {
                        "platform_account_id": "acct_operator_one",
                        "monitoring_status": "active",
                        "cadence": "daily",
                    }
                ]
            }
        },
    )

    def fake_heartbeat_runner(**kwargs: object) -> _FakeHeartbeatResult:
        assert Path(kwargs["output_root"]) == tmp_path / "packets"
        assert kwargs["data_root"] is None
        receipt_path = Path(kwargs["receipt_jsonl"])
        receipt_path.write_text(
            json.dumps(
                {
                    "run_id": "run_operator",
                    "status": "succeeded",
                    "partition_key": "platform_account_id:acct_operator_one",
                    "creator": {"handle": "operator_one"},
                    "packet_pointer": "packet_operator_one",
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        return _FakeHeartbeatResult()

    result = operator_runner.run_operator_session(
        registry_index_path=registry,
        monitoring_sidecar_path=sidecar,
        run_control_root=tmp_path / "lake",
        plan_date="2026-07-09",
        bucket=1,
        lane_id="lane_1",
        lane_count=1,
        output_root=tmp_path / "packets",
        plan_if_missing=True,
        bucket_count=1,
        heartbeat_runner=fake_heartbeat_runner,
        session_id="session_operator",
        now_func=lambda: "2026-07-09T02:00:00Z",
    )

    assert result.plan_created is True
    assert result.planned_count == 1
    assert result.selected_count == 1
    assert result.heartbeat_exit_code == 0
    assert result.message() == str(result.daily_summary_path)
    assert result.plan_path.name == "daily_plan.json"
    attempts = _read_jsonl(result.attempts_path)
    assert [row["attempt_status"] for row in attempts] == ["leased", "started", "succeeded"]
    daily_summary = _read_json(result.daily_summary_path)
    assert daily_summary["planned_count"] == 1
    assert daily_summary["succeeded_count"] == 1
    assert daily_summary["missed_count"] == 0


def test_operator_session_reuses_existing_plan_without_replanning(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run_control_root = tmp_path / "lake"
    day_dir = control.day_directory(run_control_root, "2026-07-09")
    stable_key = "platform_account_id:acct_operator_existing"
    _write_json(
        day_dir / "daily_plan.json",
        {
            "schema_version": control.PLAN_SCHEMA_VERSION,
            "plan_id": "plan_existing",
            "plan_date": "2026-07-09",
            "bucket_count": 1,
            "creators": [
                {
                    "platform": "instagram",
                    "platform_account_id": "acct_operator_existing",
                    "creator_record_id": "creator_operator_existing",
                    "handle": "operator_existing",
                    "monitoring_status_at_plan": "active",
                    "cadence_at_plan": "daily",
                    "stable_partition_key": stable_key,
                    "partition_key_source": "platform_account_id",
                    "bucket": 1,
                }
            ],
        },
    )
    attempts_path = day_dir / "attempts.jsonl"
    control.append_attempt(
        attempts_path,
        {
            "stable_partition_key": stable_key,
            "attempt_status": "succeeded",
        },
    )

    def fail_plan_day(**_: object) -> object:
        raise AssertionError("existing plans must be reused without replanning")

    def fake_heartbeat_runner(**kwargs: object) -> _FakeHeartbeatResult:
        roster = _read_json(Path(kwargs["roster_path"]))
        assert roster["creators"] == []
        return _FakeHeartbeatResult()

    monkeypatch.setattr(operator_runner.control, "plan_day", fail_plan_day)

    result = operator_runner.run_operator_session(
        registry_index_path=tmp_path / "unused_registry.json",
        monitoring_sidecar_path=tmp_path / "unused_sidecar.json",
        run_control_root=run_control_root,
        plan_date="2026-07-09",
        bucket=1,
        lane_id="lane_1",
        lane_count=1,
        output_root=tmp_path / "packets",
        heartbeat_runner=fake_heartbeat_runner,
        session_id="session_existing",
        now_func=lambda: "2026-07-09T03:00:00Z",
    )

    assert result.plan_created is False
    assert result.planned_count == 1
    assert result.selected_count == 0
    assert [row["attempt_status"] for row in _read_jsonl(attempts_path)] == ["succeeded"]
    daily_summary = _read_json(result.daily_summary_path)
    assert daily_summary["planned_count"] == 1
    assert daily_summary["succeeded_count"] == 1
    assert daily_summary["missed_count"] == 0


def test_operator_session_reuses_plan_created_concurrently(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run_control_root = tmp_path / "lake"
    day_dir = control.day_directory(run_control_root, "2026-07-09")
    stable_key = "platform_account_id:acct_operator_race"

    def racing_plan_day(**_: object) -> object:
        _write_json(
            day_dir / "daily_plan.json",
            {
                "schema_version": control.PLAN_SCHEMA_VERSION,
                "plan_id": "plan_race_winner",
                "plan_date": "2026-07-09",
                "bucket_count": 1,
                "creators": [
                    {
                        "platform": "instagram",
                        "platform_account_id": "acct_operator_race",
                        "creator_record_id": "creator_operator_race",
                        "handle": "operator_race",
                        "monitoring_status_at_plan": "active",
                        "cadence_at_plan": "daily",
                        "stable_partition_key": stable_key,
                        "partition_key_source": "platform_account_id",
                        "bucket": 1,
                    }
                ],
            },
        )
        raise ValueError("daily plan already exists")

    def fake_heartbeat_runner(**kwargs: object) -> _FakeHeartbeatResult:
        receipt_path = Path(kwargs["receipt_jsonl"])
        receipt_path.write_text(
            json.dumps(
                {
                    "run_id": "run_operator_race",
                    "status": "succeeded",
                    "partition_key": stable_key,
                    "creator": {"handle": "operator_race"},
                    "packet_pointer": "packet_operator_race",
                },
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        return _FakeHeartbeatResult()

    monkeypatch.setattr(operator_runner.control, "plan_day", racing_plan_day)

    result = operator_runner.run_operator_session(
        registry_index_path=tmp_path / "registry.json",
        monitoring_sidecar_path=tmp_path / "sidecar.json",
        run_control_root=run_control_root,
        plan_date="2026-07-09",
        bucket=1,
        lane_id="lane_1",
        lane_count=1,
        output_root=tmp_path / "packets",
        plan_if_missing=True,
        heartbeat_runner=fake_heartbeat_runner,
        session_id="session_race",
        now_func=lambda: "2026-07-09T03:30:00Z",
    )

    assert result.plan_created is False
    assert result.planned_count == 1
    assert result.selected_count == 1
    attempts = _read_jsonl(result.attempts_path)
    assert [row["attempt_status"] for row in attempts] == ["leased", "started", "succeeded"]
    daily_summary = _read_json(result.daily_summary_path)
    assert daily_summary["planned_count"] == 1
    assert daily_summary["succeeded_count"] == 1
    assert daily_summary["missed_count"] == 0


def test_operator_session_requires_existing_plan_when_plan_if_missing_disabled(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="daily plan missing"):
        operator_runner.run_operator_session(
            registry_index_path=tmp_path / "missing_registry.json",
            monitoring_sidecar_path=tmp_path / "missing_sidecar.json",
            run_control_root=tmp_path / "lake",
            plan_date="2026-07-09",
            bucket=1,
            lane_id="lane_1",
            lane_count=1,
            output_root=tmp_path / "packets",
            plan_if_missing=False,
            heartbeat_runner=lambda **_: _FakeHeartbeatResult(),
        )
