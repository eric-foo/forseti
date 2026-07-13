from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from threading import Event, Thread
from types import SimpleNamespace
from typing import Any, Callable

import pytest

from source_capture import social_heartbeat_run_control as control


POLICY = control.RunControlPolicy(
    platform="test_social",
    namespace=Path("run_control") / "test_social_daily_heartbeat",
    run_control_version="test_social_daily_heartbeat_control_v0",
    plan_schema_version="test_social_daily_heartbeat_plan_v0",
    attempt_schema_version="test_social_daily_heartbeat_attempt_v0",
    session_summary_schema_version="test_social_daily_heartbeat_session_summary_v0",
    daily_summary_schema_version="test_social_daily_heartbeat_daily_summary_v0",
    plan_id_prefix="plan_test_social_daily_heartbeat",
    actor="pytest",
)
PLAN_DATE = "2026-07-14"
STABLE_KEY = "platform_account_id:acct_test_one"


def _creator(*, stable_key: str = STABLE_KEY, handle: str = "test_one") -> dict[str, object]:
    return {
        "platform": POLICY.platform,
        "platform_account_id": stable_key.removeprefix("platform_account_id:"),
        "handle": handle,
        "stable_partition_key": stable_key,
    }


def _freeze_one(run_control_root: Path) -> control.PlanDayResult:
    return control.freeze_plan(
        policy=POLICY,
        creators=[_creator()],
        source_inputs={"active_roster": {"path": "fixture.json", "sha256": "a" * 64}},
        run_control_root=run_control_root,
        plan_date=PLAN_DATE,
        bucket_count=1,
        now_func=lambda: "2026-07-14T00:00:00Z",
    )


def _read_json(path: Path) -> dict[str, Any]:
    parsed = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(parsed, dict)
    return parsed


def _roster_row(kwargs: dict[str, object]) -> dict[str, Any]:
    roster = _read_json(Path(kwargs["roster_path"]))
    assert roster["partition_preselected"] is True
    rows = roster["creators"]
    assert isinstance(rows, list) and len(rows) == 1
    assert isinstance(rows[0], dict)
    return rows[0]


def _write_receipts(path: object, receipts: list[dict[str, object]]) -> None:
    Path(path).write_text(
        "".join(f"{json.dumps(receipt, sort_keys=True)}\n" for receipt in receipts),
        encoding="utf-8",
    )


def _failed_receipt(row: dict[str, Any], **overrides: object) -> dict[str, object]:
    receipt: dict[str, object] = {
        "partition_key": row["stable_partition_key"],
        "attempt_id": row["attempt_id"],
        "status": "failed",
        "error_class": "FixtureFailure",
    }
    receipt.update(overrides)
    return receipt


def _write_verified_packet(packet_dir: Path, *, attempt_id: str) -> str:
    packet_dir.mkdir(parents=True)
    packet_id = f"packet_{attempt_id}"
    body = b"verified heartbeat packet"
    (packet_dir / "body.bin").write_bytes(body)
    (packet_dir / "manifest.json").write_text(
        json.dumps(
            {
                "packet_id": packet_id,
                "session_identity": attempt_id,
                "preserved_files": [
                    {
                        "relative_packet_path": "body.bin",
                        "sha256": hashlib.sha256(body).hexdigest(),
                    }
                ],
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return packet_id


class _FakeDataRoot:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._packets: dict[str, Path] = {}
        self._availability: set[str] = set()

    def add_packet(
        self, *, packet_id: str, attempt_id: str, source_surface: str
    ) -> Path:
        packet_dir = self.path / "raw" / packet_id[:3] / packet_id
        packet_dir.mkdir(parents=True)
        (packet_dir / "manifest.json").write_text(
            json.dumps(
                {
                    "packet_id": packet_id,
                    "session_identity": attempt_id,
                    "source_surface": source_surface,
                }
            ),
            encoding="utf-8",
        )
        self._packets[packet_id] = packet_dir
        return packet_dir

    def load_raw_packet(self, packet_id: str) -> object:
        return SimpleNamespace(container=self._packets[packet_id])

    def read_availability(self, packet_id: str) -> object | None:
        return {} if packet_id in self._availability else None

    def record_availability(self, packet_id: str) -> None:
        self._availability.add(packet_id)


def _run(
    tmp_path: Path,
    runner: Callable[..., object],
    *,
    run_control_root: Path | None = None,
) -> control.RunSessionResult:
    root = run_control_root or tmp_path / "control"
    if not (control.day_directory(root, POLICY, PLAN_DATE) / "daily_plan.json").exists():
        _freeze_one(root)
    return control.run_session(
        policy=POLICY,
        run_control_root=root,
        plan_date=PLAN_DATE,
        bucket=1,
        lane_id="lane_1",
        lane_count=1,
        heartbeat_runner=runner,
        output_root=tmp_path / "packets",
        session_id="session_fixture",
        now_func=lambda: "2026-07-14T01:00:00Z",
    )


@pytest.mark.parametrize(
    ("case", "expected_error"),
    [
        ("missing", "missing receipt for partition_key"),
        ("unmatched", "missing or unmatched partition_key"),
        ("duplicate", "duplicate receipt for partition_key"),
        ("unknown_status", "unsupported status"),
    ],
)
def test_run_session_fails_loud_on_strict_receipt_contract_errors(
    tmp_path: Path, case: str, expected_error: str
) -> None:
    def runner(**kwargs: object) -> object:
        row = _roster_row(kwargs)
        if case == "missing":
            receipts: list[dict[str, object]] = []
        elif case == "unmatched":
            receipts = [_failed_receipt(row, partition_key="platform_account_id:not_selected")]
        elif case == "duplicate":
            receipts = [_failed_receipt(row), _failed_receipt(row)]
        else:
            receipts = [_failed_receipt(row, status="invented_status")]
        _write_receipts(kwargs["receipt_jsonl"], receipts)
        return SimpleNamespace(exit_code=0, stopped_by_budget=False)

    result = _run(tmp_path, runner)

    assert result.effective_exit_code == control.RECEIPT_CONTRACT_EXIT_CODE
    assert result.receipt_contract_error_count >= 1
    summary = _read_json(result.session_summary_path)
    assert any(expected_error in error for error in summary["receipt_contract_errors"])


@pytest.mark.parametrize("defect", ["receipt_attempt", "manifest_attempt"])
def test_succeeded_receipt_requires_matching_attempt_and_verified_packet(
    tmp_path: Path, defect: str
) -> None:
    def runner(**kwargs: object) -> object:
        row = _roster_row(kwargs)
        attempt_id = str(row["attempt_id"])
        manifest_attempt = "different_attempt" if defect == "manifest_attempt" else attempt_id
        packet_dir = tmp_path / "packets" / defect
        packet_id = _write_verified_packet(packet_dir, attempt_id=manifest_attempt)
        receipt_attempt = "different_attempt" if defect == "receipt_attempt" else attempt_id
        _write_receipts(
            kwargs["receipt_jsonl"],
            [
                {
                    "partition_key": row["stable_partition_key"],
                    "attempt_id": receipt_attempt,
                    "status": "succeeded",
                    "packet_id": packet_id,
                    "packet_pointer": str(packet_dir),
                }
            ],
        )
        return SimpleNamespace(exit_code=0, stopped_by_budget=False)

    result = _run(tmp_path, runner)

    assert result.effective_exit_code == control.RECEIPT_CONTRACT_EXIT_CODE
    summary = _read_json(result.session_summary_path)
    expected = "does not match attempt_id"
    assert any(expected in error for error in summary["receipt_contract_errors"])
    assert summary["succeeded_count"] == 0


def test_succeeded_receipt_with_verified_matching_packet_is_accepted(tmp_path: Path) -> None:
    def runner(**kwargs: object) -> object:
        row = _roster_row(kwargs)
        attempt_id = str(row["attempt_id"])
        packet_dir = tmp_path / "packets" / attempt_id
        packet_id = _write_verified_packet(packet_dir, attempt_id=attempt_id)
        _write_receipts(
            kwargs["receipt_jsonl"],
            [
                {
                    "partition_key": row["stable_partition_key"],
                    "attempt_id": attempt_id,
                    "status": "succeeded",
                    "packet_id": packet_id,
                    "packet_pointer": str(packet_dir),
                }
            ],
        )
        return SimpleNamespace(exit_code=0, stopped_by_budget=False)

    result = _run(tmp_path, runner)

    assert result.effective_exit_code == 0
    assert result.receipt_contract_error_count == 0
    summary = _read_json(result.session_summary_path)
    assert summary["succeeded_count"] == 1


def test_run_session_reuses_active_attempt_identity_on_resume(tmp_path: Path) -> None:
    root = tmp_path / "control"
    plan = _freeze_one(root)
    attempt_id = "attempt_started_before_crash"
    control.append_attempt(
        plan.attempts_path,
        {
            "stable_partition_key": STABLE_KEY,
            "attempt_id": attempt_id,
            "attempt_status": "started",
        },
    )

    def runner(**kwargs: object) -> object:
        row = _roster_row(kwargs)
        assert row["attempt_id"] == attempt_id
        assert row["attempt_resume"] is True
        _write_receipts(kwargs["receipt_jsonl"], [_failed_receipt(row)])
        return SimpleNamespace(exit_code=0, stopped_by_budget=False)

    result = _run(tmp_path, runner, run_control_root=root)

    assert result.effective_exit_code == 0
    attempts = control.read_jsonl(result.attempts_path)
    resumed = [row for row in attempts if row.get("session_id") == "session_fixture"]
    assert [row["attempt_id"] for row in resumed] == [attempt_id, attempt_id, attempt_id]
    assert [row["attempt_status"] for row in resumed] == ["leased", "started", "failed"]


def test_succeeded_attempt_status_cannot_be_retried(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unsupported retry statuses: succeeded"):
        control.run_session(
            policy=POLICY,
            run_control_root=tmp_path / "control",
            plan_date=PLAN_DATE,
            bucket=1,
            lane_id="lane_1",
            lane_count=1,
            heartbeat_runner=lambda **_: SimpleNamespace(exit_code=0),
            output_root=tmp_path / "packets",
            retry_statuses=["succeeded"],
        )


def test_freeze_plan_is_exclusive_and_rejects_duplicate_stable_keys(tmp_path: Path) -> None:
    root = tmp_path / "control"
    _freeze_one(root)

    with pytest.raises(ValueError, match="daily plan already exists"):
        _freeze_one(root)

    duplicate_root = tmp_path / "duplicate_control"
    with pytest.raises(ValueError, match="duplicate stable_partition_key"):
        control.freeze_plan(
            policy=POLICY,
            creators=[_creator(handle="one"), _creator(handle="renamed")],
            source_inputs={"active_roster": {"path": "fixture.json", "sha256": "a" * 64}},
            run_control_root=duplicate_root,
            plan_date=PLAN_DATE,
            bucket_count=1,
        )


def test_attempt_log_append_waits_for_shared_log_lock(tmp_path: Path) -> None:
    attempts_path = tmp_path / "attempts.jsonl"
    attempts_path.touch()
    completed = Event()

    def append_in_thread() -> None:
        control.append_attempt(attempts_path, {"attempt_id": "parallel_bucket"})
        completed.set()

    with control._FileMutex(control._attempt_log_lock_path(attempts_path)):
        thread = Thread(target=append_in_thread, daemon=True)
        thread.start()
        assert completed.wait(0.05) is False

    thread.join(timeout=2)
    assert completed.is_set()
    assert control.read_attempt_log(attempts_path) == [{"attempt_id": "parallel_bucket"}]


def test_day_lock_stale_takeover_race_is_visible_lock_contention(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    lock_path = tmp_path / "session_1.lock"
    lock_path.write_text("stale", encoding="utf-8")
    os.utime(lock_path, (0, 0))
    real_open = control.os.open

    def race_open(path: object, flags: int, *args: object) -> int:
        if Path(path) == lock_path:
            raise FileExistsError(str(path))
        return real_open(path, flags, *args)

    monkeypatch.setattr(control.os, "open", race_open)

    with pytest.raises(ValueError, match="session lock already exists"):
        with control.DayLock(
            lock_path,
            session_id="losing_stale_taker",
            stale_seconds=1,
            now_func=lambda: "2026-07-14T00:00:00Z",
        ):
            pytest.fail("losing stale taker must not acquire the lease")


def test_data_root_success_and_crash_reconciliation_bind_attempt_identity(tmp_path: Path) -> None:
    root = _FakeDataRoot(tmp_path / "lake")
    packet_dir = root.add_packet(
        packet_id="01DATAROOTPACKET00000000000",
        attempt_id="attempt_data_root",
        source_surface="test/grid",
    )
    receipt = {
        "packet_pointer": str(packet_dir),
        "packet_id": "01DATAROOTPACKET00000000000",
    }

    control._verify_success_packet(receipt, attempt_id="attempt_data_root", data_root=root)
    assert control.find_committed_packet_by_session_identity(
        root,
        session_identity="attempt_data_root",
        source_surface="test/grid",
    ) == ("01DATAROOTPACKET00000000000", packet_dir)
    assert root.read_availability("01DATAROOTPACKET00000000000") == {}

    with pytest.raises(ValueError, match="session_identity does not match"):
        control._verify_success_packet(receipt, attempt_id="wrong_attempt", data_root=root)

    root.add_packet(
        packet_id="01DATAROOTDUPLICATE000000000",
        attempt_id="attempt_data_root",
        source_surface="test/grid",
    )
    with pytest.raises(ValueError, match="multiple committed packets"):
        control.find_committed_packet_by_session_identity(
            root,
            session_identity="attempt_data_root",
            source_surface="test/grid",
        )
