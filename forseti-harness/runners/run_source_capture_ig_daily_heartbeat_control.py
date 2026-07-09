"""Run-control utilities for IG daily heartbeat.

This layer owns operational provenance around the heartbeat runner: daily plan
freezing, deterministic session buckets, duplicate-attempt prevention, and
operator summaries. It intentionally does not parse IG, score momentum, select
deep captures, or mutate Creator Registry rows.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import generate_ulid, utc_now_z
from runners.run_source_capture_ig_daily_heartbeat import (
    assign_lane_id as assign_heartbeat_lane_id,
    run_ig_daily_heartbeat,
)


RUN_CONTROL_VERSION = "ig_daily_heartbeat_run_control_v0"
PLAN_SCHEMA_VERSION = "ig_daily_heartbeat_daily_plan_v0"
ATTEMPT_SCHEMA_VERSION = "ig_daily_heartbeat_attempt_v0"
SESSION_SUMMARY_SCHEMA_VERSION = "ig_daily_heartbeat_session_summary_v0"
DAILY_SUMMARY_SCHEMA_VERSION = "ig_daily_heartbeat_daily_summary_v0"
RUN_CONTROL_NAMESPACE = Path("run_control") / "ig_daily_heartbeat"
DEFAULT_BUCKET_COUNT = 4
DEFAULT_SEED_VERSION = "daily_bucket_sha256_v0"
DEFAULT_SEED_SALT_ID = "daily_bucket_v1"
TERMINAL_ATTEMPT_STATUSES = frozenset({"succeeded", "access_gap", "failed", "skipped"})

HeartbeatRunner = Callable[..., Any]
NowFunc = Callable[[], str]


@dataclass(frozen=True)
class PlanDayResult:
    plan_path: Path
    attempts_path: Path
    planned_count: int

    @property
    def exit_code(self) -> int:
        return 0

    def message(self) -> str:
        return str(self.plan_path)


@dataclass(frozen=True)
class RunSessionResult:
    session_roster_path: Path
    receipt_jsonl: Path
    attempts_path: Path
    session_summary_path: Path
    selected_count: int
    duplicate_prevented_count: int
    skipped_by_lane_in_bucket_count: int
    heartbeat_exit_code: int

    @property
    def exit_code(self) -> int:
        return self.heartbeat_exit_code

    def message(self) -> str:
        return str(self.session_summary_path)


@dataclass(frozen=True)
class SummarizeDayResult:
    summary_path: Path

    @property
    def exit_code(self) -> int:
        return 0

    def message(self) -> str:
        return str(self.summary_path)


class _DayLock:
    def __init__(self, path: Path, *, session_id: str, stale_seconds: int, now_func: NowFunc) -> None:
        self.path = path
        self.session_id = session_id
        self.stale_seconds = stale_seconds
        self.now_func = now_func
        self.acquired = False

    def __enter__(self) -> "_DayLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            age_seconds = _file_age_seconds(self.path)
            if age_seconds <= self.stale_seconds:
                raise ValueError(f"session lock already exists: {self.path}")
            self.path.unlink()
        payload = {
            "schema_version": "ig_daily_heartbeat_session_lock_v0",
            "session_id": self.session_id,
            "created_at_utc": self.now_func(),
        }
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        fd = os.open(self.path, flags)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(f"{json.dumps(payload, sort_keys=True)}\n")
        except Exception:
            os.close(fd)
            raise
        self.acquired = True
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self.acquired and self.path.exists():
            self.path.unlink()


def plan_day(
    *,
    registry_index_path: Path,
    monitoring_sidecar_path: Path,
    run_control_root: Path,
    plan_date: str,
    bucket_count: int = DEFAULT_BUCKET_COUNT,
    seed_salt_id: str = DEFAULT_SEED_SALT_ID,
    overwrite: bool = False,
    now_func: NowFunc = utc_now_z,
) -> PlanDayResult:
    _validate_plan_date(plan_date)
    _validate_bucket_count(bucket_count)
    day_dir = day_directory(run_control_root, plan_date)
    day_dir.mkdir(parents=True, exist_ok=True)
    plan_path = day_dir / "daily_plan.json"
    attempts_path = day_dir / "attempts.jsonl"
    if plan_path.exists() and not overwrite:
        raise ValueError(f"daily plan already exists: {plan_path}")

    registry = _load_json_object(registry_index_path)
    sidecar = _load_json_object(monitoring_sidecar_path)
    registry_rows = _registry_rows(registry)
    sidecar_rows = _sidecar_rows(sidecar)
    sidecar_by_account = _sidecar_by_platform_account_id(sidecar_rows)

    creators: list[dict[str, Any]] = []
    for row in registry_rows:
        platform = _optional_string(row.get("platform"))
        if platform is None or platform.lower() != "instagram":
            continue
        platform_account_id = _optional_string(row.get("platform_account_id"))
        if platform_account_id is None:
            raise ValueError("instagram registry row is missing platform_account_id")
        sidecar_row = sidecar_by_account.get(platform_account_id)
        if sidecar_row is None:
            continue
        status = _required_string(sidecar_row, ("monitoring_status", "heartbeat_status", "status"))
        cadence = _required_string(sidecar_row, ("cadence", "monitoring_cadence", "heartbeat_cadence"))
        if status != "active" or cadence != "daily":
            continue
        handle = _first_string(row, ("normalized_public_handle", "public_handle"))
        if handle is None:
            raise ValueError(f"registry row {platform_account_id} is missing a public handle")
        stable_key = f"platform_account_id:{platform_account_id}"
        creators.append(
            {
                "creator_record_id": _optional_string(row.get("creator_record_id_or_none")),
                "platform": "instagram",
                "platform_account_id": platform_account_id,
                "platform_public_account_id": _optional_string(row.get("platform_public_account_id_or_none")),
                "handle": handle,
                "public_profile_url": _optional_string(row.get("public_profile_url")),
                "monitoring_status_at_plan": status,
                "cadence_at_plan": cadence,
                "stable_partition_key": stable_key,
                "partition_key_source": "platform_account_id",
                "bucket": assign_daily_bucket(
                    stable_key,
                    plan_date=plan_date,
                    bucket_count=bucket_count,
                    seed_salt_id=seed_salt_id,
                ),
            }
        )

    registry_sha256 = _sha256_file(registry_index_path)
    sidecar_sha256 = _sha256_file(monitoring_sidecar_path)
    plan_hash = _short_hash_values(plan_date, str(bucket_count), seed_salt_id, registry_sha256, sidecar_sha256)

    plan = {
        "schema_version": PLAN_SCHEMA_VERSION,
        "run_control_version": RUN_CONTROL_VERSION,
        "plan_id": f"ig_daily_heartbeat_plan_{plan_date}_{plan_hash}",
        "plan_date": plan_date,
        "created_at_utc": now_func(),
        "source_registry": {
            "path": str(registry_index_path),
            "sha256": registry_sha256,
        },
        "monitoring_sidecar": {
            "path": str(monitoring_sidecar_path),
            "sha256": sidecar_sha256,
        },
        "bucket_count": bucket_count,
        "seed_version": DEFAULT_SEED_VERSION,
        "seed_salt_id": seed_salt_id,
        "storage_namespace": (RUN_CONTROL_NAMESPACE / plan_date).as_posix(),
        "non_claims": [
            "not Silver",
            "not Gold",
            "not creator intelligence",
            "not live capture authorization",
            "not account-safety proof",
        ],
        "creators": sorted(creators, key=lambda item: (item["bucket"], item["stable_partition_key"])),
    }
    _write_json(plan_path, plan)
    if overwrite:
        attempts_path.write_text("", encoding="utf-8", newline="\n")
    else:
        attempts_path.touch(exist_ok=True)
    return PlanDayResult(plan_path=plan_path, attempts_path=attempts_path, planned_count=len(creators))


def run_session(
    *,
    run_control_root: Path,
    plan_date: str,
    bucket: int,
    lane_id: str,
    lane_count: int,
    output_root: Path | None = None,
    data_root: Any | None = None,
    heartbeat_runner: HeartbeatRunner = run_ig_daily_heartbeat,
    session_id: str | None = None,
    retry_statuses: Sequence[str] = (),
    lease_stale_seconds: int = 7200,
    max_creators: int | None = None,
    time_budget_seconds: float | None = None,
    allow_heavy_assets: bool = False,
    now_func: NowFunc = utc_now_z,
) -> RunSessionResult:
    _validate_plan_date(plan_date)
    _validate_lane_id(lane_id=lane_id, lane_count=lane_count)
    day_dir = day_directory(run_control_root, plan_date)
    plan = _load_daily_plan(day_dir / "daily_plan.json")
    if plan.get("plan_date") != plan_date:
        raise ValueError("daily plan date does not match requested plan_date")
    bucket_count = _int_field(plan, "bucket_count")
    if bucket < 1 or bucket > bucket_count:
        raise ValueError(f"bucket must be between 1 and {bucket_count}")
    if (output_root is None) == (data_root is None):
        raise ValueError("exactly one of output_root or data_root is required")

    attempts_path = day_dir / "attempts.jsonl"
    attempts_path.touch(exist_ok=True)
    session_id = session_id or f"session_{plan_date}_bucket_{bucket}_{generate_ulid()}"
    lock_path = day_dir / f"session_{bucket}.lock"
    retry = set(retry_statuses)
    invalid_retry = retry - TERMINAL_ATTEMPT_STATUSES
    if invalid_retry:
        raise ValueError(f"unsupported retry statuses: {', '.join(sorted(invalid_retry))}")

    with _DayLock(lock_path, session_id=session_id, stale_seconds=lease_stale_seconds, now_func=now_func):
        attempts = read_jsonl(attempts_path)
        terminal_by_key = _terminal_attempts_by_key(attempts)
        bucket_rows = [row for row in plan["creators"] if row.get("bucket") == bucket]
        lane_rows = [
            row
            for row in bucket_rows
            if assign_heartbeat_lane_id(str(row["stable_partition_key"]), lane_count) == lane_id
        ]
        skipped_by_lane_in_bucket = len(bucket_rows) - len(lane_rows)
        selected_rows: list[dict[str, Any]] = []
        duplicate_prevented = 0
        for row in lane_rows:
            key = str(row["stable_partition_key"])
            existing = terminal_by_key.get(key)
            if existing is not None and existing.get("attempt_status") not in retry:
                duplicate_prevented += 1
                continue
            selected_rows.append(row)
        if max_creators is not None:
            selected_rows = selected_rows[:max_creators]

        # Per-(bucket, lane) session artifacts so two lanes in the same bucket cannot clobber each
        # other's roster/receipts/summary (APH-IMPL-1: these were keyed by bucket only). The
        # bucket-scoped session lock above -- i.e. whether lanes in a bucket may run concurrently --
        # stays the deferred F2 concurrency decision, unchanged here.
        session_roster_path = day_dir / f"session_{bucket}_{lane_id}_roster.json"
        receipt_jsonl = day_dir / f"heartbeat_receipts_session_{bucket}_{lane_id}.jsonl"
        summary_path = day_dir / f"session_{bucket}_{lane_id}_summary.json"
        _write_session_roster(session_roster_path, plan=plan, bucket=bucket, rows=selected_rows)
        for row in selected_rows:
            append_attempt(
                attempts_path,
                _attempt_row(
                    plan=plan,
                    row=row,
                    session_id=session_id,
                    bucket=bucket,
                    status="leased",
                    now_func=now_func,
                ),
            )
        for row in selected_rows:
            append_attempt(
                attempts_path,
                _attempt_row(
                    plan=plan,
                    row=row,
                    session_id=session_id,
                    bucket=bucket,
                    status="started",
                    now_func=now_func,
                ),
            )

        result = heartbeat_runner(
            roster_path=session_roster_path,
            receipt_jsonl=receipt_jsonl,
            lane_id=lane_id,
            lane_count=lane_count,
            output_root=output_root,
            data_root=data_root,
            max_creators=None,
            time_budget_seconds=time_budget_seconds,
            block_heavy_assets=not allow_heavy_assets,
        )
        receipts = read_jsonl(receipt_jsonl)
        plan_by_key = {str(row["stable_partition_key"]): row for row in selected_rows}
        plan_by_handle = {str(row["handle"]).lower(): row for row in selected_rows}
        for receipt in receipts:
            # Prefer the immutable stable partition key the receipt carries. Handles are
            # mutable and may be normalized/cased differently than the plan row, which
            # would drop or misattribute a terminal receipt and leave a captured creator
            # counted as missed.
            partition_key = _optional_string(receipt.get("partition_key"))
            if partition_key is not None:
                row = plan_by_key.get(partition_key)
            else:
                creator = receipt.get("creator")
                handle = _optional_string(creator.get("handle") if isinstance(creator, dict) else None)
                row = plan_by_handle.get(handle.lower()) if handle is not None else None
            if row is None:
                continue
            append_attempt(
                attempts_path,
                _attempt_row_from_receipt(
                    plan=plan,
                    row=row,
                    receipt=receipt,
                    receipt_jsonl=receipt_jsonl,
                    session_id=session_id,
                    bucket=bucket,
                    now_func=now_func,
                ),
            )

        summary = _session_summary(
            plan=plan,
            bucket=bucket,
            session_id=session_id,
            selected_count=len(selected_rows),
            duplicate_prevented_count=duplicate_prevented,
            skipped_by_lane_in_bucket_count=skipped_by_lane_in_bucket,
            heartbeat_exit_code=int(getattr(result, "exit_code", 0)),
            receipt_jsonl=receipt_jsonl,
            receipts=receipts,
            now_func=now_func,
        )
        _write_json(summary_path, summary)
        return RunSessionResult(
            session_roster_path=session_roster_path,
            receipt_jsonl=receipt_jsonl,
            attempts_path=attempts_path,
            session_summary_path=summary_path,
            selected_count=len(selected_rows),
            duplicate_prevented_count=duplicate_prevented,
            skipped_by_lane_in_bucket_count=skipped_by_lane_in_bucket,
            heartbeat_exit_code=int(getattr(result, "exit_code", 0)),
        )


def summarize_day(*, run_control_root: Path, plan_date: str, now_func: NowFunc = utc_now_z) -> SummarizeDayResult:
    _validate_plan_date(plan_date)
    day_dir = day_directory(run_control_root, plan_date)
    plan = _load_daily_plan(day_dir / "daily_plan.json")
    if plan.get("plan_date") != plan_date:
        raise ValueError("daily plan date does not match requested plan_date")
    attempts = read_jsonl(day_dir / "attempts.jsonl")
    terminal = _terminal_attempts_by_key(attempts)
    counts = {"succeeded": 0, "access_gap": 0, "failed": 0, "skipped": 0}
    for attempt in terminal.values():
        status = _optional_string(attempt.get("attempt_status"))
        if status in counts:
            counts[status] += 1
    planned = len(plan["creators"])
    attempted = sum(counts.values())
    summary = {
        "schema_version": DAILY_SUMMARY_SCHEMA_VERSION,
        "run_control_version": RUN_CONTROL_VERSION,
        "plan_id": plan["plan_id"],
        "plan_date": plan_date,
        "generated_at_utc": now_func(),
        "planned_count": planned,
        "attempted_count": attempted,
        "succeeded_count": counts["succeeded"],
        "access_gap_count": counts["access_gap"],
        "failed_count": counts["failed"],
        "skipped_count": counts["skipped"],
        "missed_count": max(planned - attempted, 0),
        "attempts_path": str(day_dir / "attempts.jsonl"),
        "non_claims": ["operational coverage summary only", "not Silver", "not Gold"],
    }
    summary_path = day_dir / "daily_summary.json"
    _write_json(summary_path, summary)
    return SummarizeDayResult(summary_path=summary_path)


def day_directory(run_control_root: Path, plan_date: str) -> Path:
    return run_control_root / RUN_CONTROL_NAMESPACE / plan_date


def assign_daily_bucket(
    stable_key: str,
    *,
    plan_date: str,
    bucket_count: int = DEFAULT_BUCKET_COUNT,
    seed_salt_id: str = DEFAULT_SEED_SALT_ID,
) -> int:
    _validate_bucket_count(bucket_count)
    material = f"{stable_key}|{plan_date}|{DEFAULT_SEED_VERSION}|{seed_salt_id}"
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return int(digest, 16) % bucket_count + 1


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        parsed = json.loads(line)
        if not isinstance(parsed, dict):
            raise ValueError(f"JSONL row must be an object: {path}")
        rows.append(parsed)
    return rows


def append_attempt(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True))
        handle.write("\n")


def _attempt_row(
    *,
    plan: Mapping[str, Any],
    row: Mapping[str, Any],
    session_id: str,
    bucket: int,
    status: str,
    now_func: NowFunc,
) -> dict[str, Any]:
    return {
        "schema_version": ATTEMPT_SCHEMA_VERSION,
        "plan_id": plan["plan_id"],
        "plan_date": plan["plan_date"],
        "timestamp_utc": now_func(),
        "session_id": session_id,
        "bucket": bucket,
        "stable_partition_key": row["stable_partition_key"],
        "platform_account_id": row.get("platform_account_id"),
        "creator_record_id": row.get("creator_record_id"),
        "handle_at_plan": row["handle"],
        "attempt_status": status,
        "actor": "ig_daily_heartbeat_run_control",
    }


def _attempt_row_from_receipt(
    *,
    plan: Mapping[str, Any],
    row: Mapping[str, Any],
    receipt: Mapping[str, Any],
    receipt_jsonl: Path,
    session_id: str,
    bucket: int,
    now_func: NowFunc,
) -> dict[str, Any]:
    attempt = _attempt_row(plan=plan, row=row, session_id=session_id, bucket=bucket, status=str(receipt["status"]), now_func=now_func)
    attempt["run_id"] = receipt.get("run_id")
    attempt["receipt_status"] = receipt.get("status")
    # Point at the session's receipt file (the receipt dict carries no self-pointer; the run_id
    # above locates the line). Previously read receipt.get("receipt_pointer") -- a key the receipt
    # never carries -- so this field was always null (APH-IMPL-3).
    attempt["receipt_pointer"] = str(receipt_jsonl)
    attempt["packet_pointer"] = receipt.get("packet_pointer")
    if receipt.get("access_gap_reason") is not None:
        attempt["access_gap_reason"] = receipt.get("access_gap_reason")
    if receipt.get("error_class") is not None:
        attempt["error_class"] = receipt.get("error_class")
    return attempt


def _session_summary(
    *,
    plan: Mapping[str, Any],
    bucket: int,
    session_id: str,
    selected_count: int,
    duplicate_prevented_count: int,
    skipped_by_lane_in_bucket_count: int,
    heartbeat_exit_code: int,
    receipt_jsonl: Path,
    receipts: Sequence[Mapping[str, Any]],
    now_func: NowFunc,
) -> dict[str, Any]:
    counts = {"succeeded": 0, "access_gap": 0, "failed": 0}
    for receipt in receipts:
        status = _optional_string(receipt.get("status"))
        if status in counts:
            counts[status] += 1
    return {
        "schema_version": SESSION_SUMMARY_SCHEMA_VERSION,
        "run_control_version": RUN_CONTROL_VERSION,
        "plan_id": plan["plan_id"],
        "plan_date": plan["plan_date"],
        "session_id": session_id,
        "bucket": bucket,
        "generated_at_utc": now_func(),
        "selected_count": selected_count,
        "duplicate_prevented_count": duplicate_prevented_count,
        "skipped_by_lane_in_bucket_count": skipped_by_lane_in_bucket_count,
        "heartbeat_exit_code": heartbeat_exit_code,
        "attempted_count": len(receipts),
        "succeeded_count": counts["succeeded"],
        "access_gap_count": counts["access_gap"],
        "failed_count": counts["failed"],
        "receipt_jsonl": str(receipt_jsonl),
        "non_claims": ["operational session summary only", "not Silver", "not Gold"],
    }


def _write_session_roster(path: Path, *, plan: Mapping[str, Any], bucket: int, rows: Sequence[Mapping[str, Any]]) -> None:
    roster_rows = []
    for row in rows:
        roster_rows.append(
            {
                "platform": "instagram",
                "handle": row["handle"],
                "platform_account_id": row.get("platform_account_id"),
                "platform_public_account_id": row.get("platform_public_account_id"),
                "creator_record_id": row.get("creator_record_id"),
                "public_profile_url": row.get("public_profile_url"),
                "status": "active",
            }
        )
    _write_json(
        path,
        {
            "roster_snapshot_id": f"{plan['plan_id']}_bucket_{bucket}",
            "plan_id": plan["plan_id"],
            "plan_date": plan["plan_date"],
            "bucket": bucket,
            "creators": roster_rows,
        },
    )


def _load_daily_plan(path: Path) -> dict[str, Any]:
    plan = _load_json_object(path)
    if plan.get("schema_version") != PLAN_SCHEMA_VERSION:
        raise ValueError(f"daily plan has unsupported schema_version: {plan.get('schema_version')!r}")
    creators = plan.get("creators")
    if not isinstance(creators, list):
        raise ValueError("daily plan creators must be a list")
    return plan


def _terminal_attempts_by_key(attempts: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    terminal: dict[str, Mapping[str, Any]] = {}
    for attempt in attempts:
        status = _optional_string(attempt.get("attempt_status"))
        key = _optional_string(attempt.get("stable_partition_key"))
        if key is not None and status in TERMINAL_ATTEMPT_STATUSES:
            terminal[key] = attempt
    return terminal


def _registry_rows(data: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]:
    root = data.get("creator_registry_index")
    if isinstance(root, dict):
        rows = root.get("platform_accounts")
    else:
        rows = data.get("platform_accounts")
    if not isinstance(rows, list):
        raise ValueError("registry index must contain platform_accounts")
    out: list[Mapping[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"registry row {index} must be an object")
        out.append(row)
    return out


def _sidecar_rows(data: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]:
    root = data.get("ig_daily_monitoring_sidecar")
    if isinstance(root, dict):
        data = root
    rows = None
    for key in ("accounts", "records", "creators", "monitoring_accounts"):
        if isinstance(data.get(key), list):
            rows = data[key]
            break
    if rows is None:
        raise ValueError("monitoring sidecar must contain accounts, records, creators, or monitoring_accounts")
    out: list[Mapping[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"monitoring sidecar row {index} must be an object")
        out.append(row)
    return out


def _sidecar_by_platform_account_id(rows: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    out: dict[str, Mapping[str, Any]] = {}
    for index, row in enumerate(rows, start=1):
        account_id = _optional_string(row.get("platform_account_id"))
        if account_id is None:
            raise ValueError(f"monitoring sidecar row {index} is missing platform_account_id")
        if account_id in out:
            raise ValueError(f"duplicate monitoring sidecar platform_account_id: {account_id}")
        out[account_id] = row
    return out


def _load_json_object(path: Path) -> dict[str, Any]:
    parsed = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError(f"JSON file must contain an object: {path}")
    return parsed


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True)}\n", encoding="utf-8", newline="\n")


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _short_hash_values(*values: str) -> str:
    h = hashlib.sha256()
    for value in values:
        h.update(value.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:12]


def _first_string(row: Mapping[str, Any], keys: Sequence[str]) -> str | None:
    for key in keys:
        value = _optional_string(row.get(key))
        if value is not None:
            return value
    return None


def _required_string(row: Mapping[str, Any], keys: Sequence[str]) -> str:
    value = _first_string(row, keys)
    if value is None:
        raise ValueError(f"row is missing one of: {', '.join(keys)}")
    return value.strip().lower()


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, int):
        return str(value)
    return None


def _int_field(row: Mapping[str, Any], key: str) -> int:
    value = row.get(key)
    if isinstance(value, int):
        return value
    raise ValueError(f"{key} must be an integer")


def _validate_plan_date(value: str) -> None:
    parts = value.split("-")
    if len(parts) != 3 or any(not part.isdigit() for part in parts):
        raise ValueError("plan_date must use YYYY-MM-DD")
    year, month, day = (int(part) for part in parts)
    if year < 2000 or not (1 <= month <= 12) or not (1 <= day <= 31):
        raise ValueError("plan_date must use YYYY-MM-DD")


def _validate_bucket_count(value: int) -> None:
    if value < 1:
        raise ValueError("bucket_count must be at least 1")


def _validate_lane_id(*, lane_id: str, lane_count: int) -> None:
    if lane_count < 1:
        raise ValueError("lane_count must be at least 1")
    expected = {f"lane_{index}" for index in range(1, lane_count + 1)}
    if lane_id not in expected:
        allowed = ", ".join(sorted(expected))
        raise ValueError(f"lane_id must be one of: {allowed}")


def _file_age_seconds(path: Path) -> float:
    return max(0.0, time.time() - os.path.getmtime(path))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plan and run IG daily heartbeat run-control sessions.")
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan-day", help="Freeze today's active IG daily plan from registry + sidecar.")
    plan.add_argument("--registry-index", type=Path, required=True)
    plan.add_argument("--monitoring-sidecar", type=Path, required=True)
    plan.add_argument("--run-control-root", type=Path, required=True)
    plan.add_argument("--plan-date", required=True)
    plan.add_argument("--bucket-count", type=int, default=DEFAULT_BUCKET_COUNT)
    plan.add_argument("--seed-salt-id", default=DEFAULT_SEED_SALT_ID)
    plan.add_argument("--overwrite", action="store_true")

    run = sub.add_parser("run-session", help="Run one planned heartbeat bucket.")
    run.add_argument("--run-control-root", type=Path, required=True)
    run.add_argument("--plan-date", required=True)
    run.add_argument("--bucket", type=int, required=True)
    run.add_argument("--lane-id", required=True)
    run.add_argument("--lane-count", type=int, required=True)
    target = run.add_mutually_exclusive_group(required=True)
    target.add_argument("--output-root", type=Path, default=None)
    target.add_argument("--data-root", default=None)
    run.add_argument("--session-id", default=None)
    run.add_argument("--retry-status", action="append", default=[])
    run.add_argument("--lease-stale-seconds", type=int, default=7200)
    run.add_argument("--max-creators", type=int, default=None)
    run.add_argument("--time-budget-seconds", type=float, default=None)
    run.add_argument("--allow-heavy-assets", action="store_true")

    summary = sub.add_parser("summarize-day", help="Write an operational daily summary.")
    summary.add_argument("--run-control-root", type=Path, required=True)
    summary.add_argument("--plan-date", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "plan-day":
            result = plan_day(
                registry_index_path=args.registry_index,
                monitoring_sidecar_path=args.monitoring_sidecar,
                run_control_root=args.run_control_root,
                plan_date=args.plan_date,
                bucket_count=args.bucket_count,
                seed_salt_id=args.seed_salt_id,
                overwrite=args.overwrite,
            )
        elif args.command == "run-session":
            data_root = None
            if args.data_root is not None:
                from data_lake.root import DataLakeRoot

                data_root = DataLakeRoot.resolve(explicit=args.data_root)
            result = run_session(
                run_control_root=args.run_control_root,
                plan_date=args.plan_date,
                bucket=args.bucket,
                lane_id=args.lane_id,
                lane_count=args.lane_count,
                output_root=args.output_root,
                data_root=data_root,
                session_id=args.session_id,
                retry_statuses=args.retry_status,
                lease_stale_seconds=args.lease_stale_seconds,
                max_creators=args.max_creators,
                time_budget_seconds=args.time_budget_seconds,
                allow_heavy_assets=args.allow_heavy_assets,
            )
        else:
            result = summarize_day(run_control_root=args.run_control_root, plan_date=args.plan_date)
    except ValueError as exc:
        parser.exit(status=2, message=f"ig heartbeat run-control failed: {exc}\n")
    except Exception as exc:  # noqa: BLE001 - preserve visible run-control failures
        parser.exit(status=3, message=f"ig heartbeat run-control failed: {type(exc).__name__}: {exc}\n")

    print(result.message())
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
