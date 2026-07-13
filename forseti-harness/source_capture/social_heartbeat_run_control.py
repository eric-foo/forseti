"""Platform-neutral run control for daily social account heartbeats.

Platform modules own roster policy and capture.  This module owns the frozen
plan, deterministic partitioning, leases, attempt identity, strict receipt
cardinality, verified Bronze completion, and operational summaries.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from harness_utils import generate_ulid, utc_now_z


DEFAULT_BUCKET_COUNT = 4
DEFAULT_SEED_VERSION = "daily_bucket_sha256_v0"
DEFAULT_SEED_SALT_ID = "daily_bucket_v1"
TERMINAL_ATTEMPT_STATUSES = frozenset({"succeeded", "access_gap", "failed", "skipped"})
RETRYABLE_ATTEMPT_STATUSES = frozenset({"access_gap", "failed", "skipped"})
RECEIPT_STATUSES = frozenset({"succeeded", "access_gap", "failed"})
RECEIPT_CONTRACT_EXIT_CODE = 4

HeartbeatRunner = Callable[..., Any]
NowFunc = Callable[[], str]


@dataclass(frozen=True)
class RunControlPolicy:
    platform: str
    namespace: Path
    run_control_version: str
    plan_schema_version: str
    attempt_schema_version: str
    session_summary_schema_version: str
    daily_summary_schema_version: str
    plan_id_prefix: str
    actor: str


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
    receipt_contract_error_count: int
    effective_exit_code: int

    @property
    def exit_code(self) -> int:
        return self.effective_exit_code

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


class DayLock:
    def __init__(self, path: Path, *, session_id: str, stale_seconds: int, now_func: NowFunc) -> None:
        self.path = path
        self.session_id = session_id
        self.stale_seconds = stale_seconds
        self.now_func = now_func
        self.acquired = False

    def __enter__(self) -> "DayLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            age_seconds = max(0.0, time.time() - os.path.getmtime(self.path))
            if age_seconds <= self.stale_seconds:
                raise ValueError(f"session lock already exists: {self.path}")
            self.path.unlink()
        payload = {
            "schema_version": "social_daily_heartbeat_session_lock_v0",
            "session_id": self.session_id,
            "created_at_utc": self.now_func(),
        }
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        fd = os.open(self.path, flags)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(f"{json.dumps(payload, sort_keys=True)}\n")
            handle.flush()
            os.fsync(handle.fileno())
        self.acquired = True
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        if not self.acquired or not self.path.exists():
            return
        try:
            current = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        if isinstance(current, dict) and current.get("session_id") == self.session_id:
            self.path.unlink()


def day_directory(run_control_root: Path, policy: RunControlPolicy, plan_date: str) -> Path:
    return run_control_root / policy.namespace / plan_date


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


def assign_lane_id(partition_key: str, lane_count: int) -> str:
    if lane_count < 1:
        raise ValueError("lane_count must be at least 1")
    digest = hashlib.sha256(partition_key.encode("utf-8")).hexdigest()
    return f"lane_{int(digest, 16) % lane_count + 1}"


def freeze_plan(
    *,
    policy: RunControlPolicy,
    creators: Sequence[Mapping[str, Any]],
    source_inputs: Mapping[str, Mapping[str, str]],
    plan_metadata: Mapping[str, Any] | None = None,
    run_control_root: Path,
    plan_date: str,
    bucket_count: int = DEFAULT_BUCKET_COUNT,
    seed_salt_id: str = DEFAULT_SEED_SALT_ID,
    overwrite: bool = False,
    now_func: NowFunc = utc_now_z,
) -> PlanDayResult:
    _validate_plan_date(plan_date)
    _validate_bucket_count(bucket_count)
    day_dir = day_directory(run_control_root, policy, plan_date)
    day_dir.mkdir(parents=True, exist_ok=True)
    plan_path = day_dir / "daily_plan.json"
    attempts_path = day_dir / "attempts.jsonl"
    normalized = _normalize_creators(
        creators,
        platform=policy.platform,
        plan_date=plan_date,
        bucket_count=bucket_count,
        seed_salt_id=seed_salt_id,
    )
    input_hashes = [value.get("sha256", "") for _key, value in sorted(source_inputs.items())]
    plan_hash = _short_hash_values(plan_date, str(bucket_count), seed_salt_id, *input_hashes)
    plan = {
        "schema_version": policy.plan_schema_version,
        "run_control_version": policy.run_control_version,
        "plan_id": f"{policy.plan_id_prefix}_{plan_date}_{plan_hash}",
        "plan_date": plan_date,
        "platform": policy.platform,
        "created_at_utc": now_func(),
        "source_inputs": dict(source_inputs),
        "bucket_count": bucket_count,
        "seed_version": DEFAULT_SEED_VERSION,
        "seed_salt_id": seed_salt_id,
        "storage_namespace": (policy.namespace / plan_date).as_posix(),
        "non_claims": ["not Silver", "not Gold", "not live capture authorization"],
        "creators": normalized,
    }
    if plan_metadata:
        overlap = set(plan) & set(plan_metadata)
        if overlap:
            raise ValueError(f"plan_metadata cannot replace core fields: {', '.join(sorted(overlap))}")
        plan.update(dict(plan_metadata))
    if overwrite:
        _write_json(plan_path, plan)
        attempts_path.write_text("", encoding="utf-8", newline="\n")
    else:
        _write_json_exclusive(plan_path, plan)
        attempts_path.touch(exist_ok=True)
    return PlanDayResult(plan_path=plan_path, attempts_path=attempts_path, planned_count=len(normalized))


def run_session(
    *,
    policy: RunControlPolicy,
    run_control_root: Path,
    plan_date: str,
    bucket: int,
    lane_id: str,
    lane_count: int,
    heartbeat_runner: HeartbeatRunner,
    output_root: Path | None = None,
    data_root: Any | None = None,
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
    if max_creators is not None and max_creators < 0:
        raise ValueError("max_creators must be non-negative")
    if time_budget_seconds is not None and time_budget_seconds < 0:
        raise ValueError("time_budget_seconds must be non-negative")
    if (output_root is None) == (data_root is None):
        raise ValueError("exactly one of output_root or data_root is required")
    retry = set(retry_statuses)
    invalid_retry = retry - RETRYABLE_ATTEMPT_STATUSES
    if invalid_retry:
        raise ValueError(f"unsupported retry statuses: {', '.join(sorted(invalid_retry))}")

    day_dir = day_directory(run_control_root, policy, plan_date)
    plan = _load_daily_plan(day_dir / "daily_plan.json", policy=policy)
    if plan.get("plan_date") != plan_date or plan.get("platform") not in {None, policy.platform}:
        raise ValueError("daily plan identity does not match the requested platform/date")
    bucket_count = _int_field(plan, "bucket_count")
    if bucket < 1 or bucket > bucket_count:
        raise ValueError(f"bucket must be between 1 and {bucket_count}")

    attempts_path = day_dir / "attempts.jsonl"
    attempts_path.touch(exist_ok=True)
    session_id = session_id or f"session_{plan_date}_bucket_{bucket}_{generate_ulid()}"
    lock_path = day_dir / f"session_{bucket}.lock"
    with DayLock(lock_path, session_id=session_id, stale_seconds=lease_stale_seconds, now_func=now_func):
        attempts = read_jsonl(attempts_path)
        terminal = _terminal_attempts_by_key(attempts)
        active = _active_attempts_by_key(attempts)
        bucket_rows = [row for row in plan["creators"] if row.get("bucket") == bucket]
        lane_rows = [
            row for row in bucket_rows
            if assign_lane_id(str(row["stable_partition_key"]), lane_count) == lane_id
        ]
        skipped_by_lane = len(bucket_rows) - len(lane_rows)
        selected: list[dict[str, Any]] = []
        duplicate_prevented = 0
        for raw_row in lane_rows:
            row = dict(raw_row)
            key = str(row["stable_partition_key"])
            existing_terminal = terminal.get(key)
            if existing_terminal is not None and existing_terminal.get("attempt_status") not in retry:
                duplicate_prevented += 1
                continue
            active_attempt = active.get(key) if existing_terminal is None else None
            attempt_id = _optional_string(active_attempt.get("attempt_id")) if active_attempt else None
            row["attempt_id"] = attempt_id or generate_ulid()
            row["attempt_resume"] = active_attempt is not None
            selected.append(row)
        if max_creators is not None:
            selected = selected[:max_creators]

        safe_session = _safe_segment(session_id)
        roster_path = day_dir / f"session_{bucket}_{lane_id}_{safe_session}_roster.json"
        receipt_path = day_dir / f"heartbeat_receipts_{bucket}_{lane_id}_{safe_session}.jsonl"
        summary_path = day_dir / f"session_{bucket}_{lane_id}_{safe_session}_summary.json"
        _write_session_roster(roster_path, plan=plan, bucket=bucket, lane_id=lane_id, rows=selected)
        receipt_path.write_text("", encoding="utf-8", newline="\n")
        for row in selected:
            append_attempt(
                attempts_path,
                _attempt_row(policy, plan, row, session_id, bucket, "leased", now_func),
            )

        runner_error: Exception | None = None
        result: Any | None = None
        try:
            result = heartbeat_runner(
                roster_path=roster_path,
                receipt_jsonl=receipt_path,
                lane_id=lane_id,
                lane_count=lane_count,
                output_root=output_root,
                data_root=data_root,
                max_creators=None,
                time_budget_seconds=time_budget_seconds,
                block_heavy_assets=not allow_heavy_assets,
                partition_preselected=True,
            )
        except Exception as exc:  # noqa: BLE001 - convert runner crash into visible control failure
            runner_error = exc

        raw_receipts = read_jsonl(receipt_path)
        valid_receipts, errors = _validate_receipts(
            raw_receipts,
            selected=selected,
            data_root=data_root,
        )
        if runner_error is not None:
            errors.append(f"heartbeat runner raised {type(runner_error).__name__}: {runner_error}")
        heartbeat_exit_code = _runner_exit_code(result, errors)
        stopped_by_budget = bool(getattr(result, "stopped_by_budget", False)) if result is not None else False
        deferred_keys = set(getattr(result, "deferred_partition_keys", ())) if result is not None else set()
        selected_keys = {str(row["stable_partition_key"]) for row in selected}
        unknown_deferred = deferred_keys - selected_keys
        if unknown_deferred:
            errors.append(
                "runner deferred unknown partition keys: " + ", ".join(sorted(unknown_deferred))
            )
        received_keys = {str(receipt["partition_key"]) for receipt in valid_receipts}
        overlap = received_keys & deferred_keys
        if overlap:
            errors.append(
                "runner both receipted and deferred partition keys: " + ", ".join(sorted(overlap))
            )
        for receipt in valid_receipts:
            row = next(item for item in selected if item["stable_partition_key"] == receipt["partition_key"])
            append_attempt(
                attempts_path,
                _attempt_row(policy, plan, row, session_id, bucket, "started", now_func),
            )
            append_attempt(
                attempts_path,
                _attempt_row_from_receipt(policy, plan, row, receipt, receipt_path, session_id, bucket, now_func),
            )
        for row in selected:
            if str(row["stable_partition_key"]) in received_keys:
                continue
            if str(row["stable_partition_key"]) in deferred_keys:
                attempt = _attempt_row(policy, plan, row, session_id, bucket, "skipped", now_func)
                attempt["skip_reason"] = "platform_context_stopped_before_attempt"
            elif stopped_by_budget:
                attempt = _attempt_row(policy, plan, row, session_id, bucket, "skipped", now_func)
                attempt["skip_reason"] = "time_budget_exhausted_before_attempt"
            else:
                errors.append(f"missing receipt for partition_key {row['stable_partition_key']}")
                attempt = _attempt_row(policy, plan, row, session_id, bucket, "failed", now_func)
                attempt["error_class"] = "ReceiptContractError"
                attempt["error_message"] = "selected creator produced no valid terminal receipt"
            append_attempt(attempts_path, attempt)

        effective_exit_code = heartbeat_exit_code
        if errors and effective_exit_code == 0:
            effective_exit_code = RECEIPT_CONTRACT_EXIT_CODE
        summary = _session_summary(
            policy=policy,
            plan=plan,
            bucket=bucket,
            session_id=session_id,
            selected_count=len(selected),
            duplicate_prevented_count=duplicate_prevented,
            skipped_by_lane_in_bucket_count=skipped_by_lane,
            heartbeat_exit_code=heartbeat_exit_code,
            effective_exit_code=effective_exit_code,
            receipt_jsonl=receipt_path,
            receipts=valid_receipts,
            contract_errors=errors,
            now_func=now_func,
        )
        _write_json(summary_path, summary)
        return RunSessionResult(
            session_roster_path=roster_path,
            receipt_jsonl=receipt_path,
            attempts_path=attempts_path,
            session_summary_path=summary_path,
            selected_count=len(selected),
            duplicate_prevented_count=duplicate_prevented,
            skipped_by_lane_in_bucket_count=skipped_by_lane,
            heartbeat_exit_code=heartbeat_exit_code,
            receipt_contract_error_count=len(errors),
            effective_exit_code=effective_exit_code,
        )


def summarize_day(
    *, policy: RunControlPolicy, run_control_root: Path, plan_date: str, now_func: NowFunc = utc_now_z
) -> SummarizeDayResult:
    _validate_plan_date(plan_date)
    day_dir = day_directory(run_control_root, policy, plan_date)
    plan = _load_daily_plan(day_dir / "daily_plan.json", policy=policy)
    attempts = read_jsonl(day_dir / "attempts.jsonl")
    terminal = _terminal_attempts_by_key(attempts)
    counts = {status: 0 for status in TERMINAL_ATTEMPT_STATUSES}
    for attempt in terminal.values():
        status = _optional_string(attempt.get("attempt_status"))
        if status in counts:
            counts[status] += 1
    planned = len(plan["creators"])
    attempted = sum(counts.values())
    summary = {
        "schema_version": policy.daily_summary_schema_version,
        "run_control_version": policy.run_control_version,
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
        handle.flush()
        os.fsync(handle.fileno())


def find_committed_packet_by_session_identity(
    data_root: Any, *, session_identity: str, source_surface: str
) -> tuple[str, Path] | None:
    raw_root = Path(data_root.path) / "raw"
    if not raw_root.is_dir():
        return None
    matches: list[tuple[str, Path]] = []
    for manifest_path in raw_root.glob("*/*/manifest.json"):
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(manifest, dict):
            continue
        if manifest.get("session_identity") != session_identity or manifest.get("source_surface") != source_surface:
            continue
        packet_id = _optional_string(manifest.get("packet_id"))
        if packet_id is None:
            continue
        data_root.load_raw_packet(packet_id)
        if data_root.read_availability(packet_id) is None:
            data_root.record_availability(packet_id)
        matches.append((packet_id, manifest_path.parent))
    if len(matches) > 1:
        raise ValueError(f"multiple committed packets share heartbeat session_identity {session_identity}")
    return matches[0] if matches else None


def _normalize_creators(
    creators: Sequence[Mapping[str, Any]], *, platform: str, plan_date: str, bucket_count: int, seed_salt_id: str
) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(creators, start=1):
        row = dict(raw)
        row_platform = _required_string(row.get("platform"), f"creator row {index} platform").lower()
        if row_platform != platform:
            raise ValueError(f"creator row {index} platform must be {platform}")
        stable_key = _required_string(row.get("stable_partition_key"), f"creator row {index} stable_partition_key")
        if stable_key in seen:
            raise ValueError(f"duplicate stable_partition_key in daily plan: {stable_key}")
        seen.add(stable_key)
        _required_string(row.get("handle"), f"creator row {index} handle")
        row["platform"] = platform
        row["stable_partition_key"] = stable_key
        row["bucket"] = assign_daily_bucket(
            stable_key, plan_date=plan_date, bucket_count=bucket_count, seed_salt_id=seed_salt_id
        )
        normalized.append(row)
    return sorted(normalized, key=lambda item: (item["bucket"], item["stable_partition_key"]))


def _validate_receipts(
    receipts: Sequence[Mapping[str, Any]], *, selected: Sequence[Mapping[str, Any]], data_root: Any | None
) -> tuple[list[dict[str, Any]], list[str]]:
    selected_by_key = {str(row["stable_partition_key"]): row for row in selected}
    accepted: list[dict[str, Any]] = []
    errors: list[str] = []
    seen: set[str] = set()
    for index, raw in enumerate(receipts, start=1):
        receipt = dict(raw)
        key = _optional_string(receipt.get("partition_key"))
        if key is None or key not in selected_by_key:
            errors.append(f"receipt {index} has missing or unmatched partition_key")
            continue
        if key in seen:
            errors.append(f"duplicate receipt for partition_key {key}")
            continue
        seen.add(key)
        row = selected_by_key[key]
        if receipt.get("attempt_id") != row.get("attempt_id"):
            errors.append(f"receipt for {key} does not match attempt_id")
            continue
        status = _optional_string(receipt.get("status"))
        if status not in RECEIPT_STATUSES:
            errors.append(f"receipt for {key} has unsupported status {status!r}")
            continue
        if status == "succeeded":
            try:
                _verify_success_packet(receipt, attempt_id=str(row["attempt_id"]), data_root=data_root)
            except (OSError, ValueError) as exc:
                errors.append(f"receipt for {key} failed packet verification: {exc}")
                continue
        accepted.append(receipt)
    return accepted, errors


def _verify_success_packet(receipt: Mapping[str, Any], *, attempt_id: str, data_root: Any | None) -> None:
    pointer = _required_string(receipt.get("packet_pointer"), "succeeded receipt packet_pointer")
    packet_dir = Path(pointer)
    manifest_path = packet_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("packet manifest must be an object")
    if manifest.get("session_identity") != attempt_id:
        raise ValueError("packet manifest session_identity does not match attempt_id")
    packet_id = _required_string(manifest.get("packet_id"), "packet manifest packet_id")
    if receipt.get("packet_id") not in {None, packet_id}:
        raise ValueError("receipt packet_id does not match packet manifest")
    if data_root is not None:
        loaded = data_root.load_raw_packet(packet_id)
        if Path(loaded.container).resolve() != packet_dir.resolve():
            raise ValueError("packet pointer does not match committed data-lake packet")
        return
    preserved = manifest.get("preserved_files")
    if not isinstance(preserved, list) or not preserved:
        raise ValueError("packet manifest preserved_files must be non-empty")
    for item in preserved:
        if not isinstance(item, dict):
            raise ValueError("packet manifest preserved_files entry must be an object")
        rel = _required_string(item.get("relative_packet_path"), "relative_packet_path")
        expected = _required_string(item.get("sha256"), "preserved file sha256")
        body = (packet_dir / Path(rel)).read_bytes()
        if hashlib.sha256(body).hexdigest() != expected:
            raise ValueError(f"preserved file hash mismatch: {rel}")


def _runner_exit_code(result: Any | None, errors: list[str]) -> int:
    if result is None:
        return 3
    value = getattr(result, "exit_code", None)
    if not isinstance(value, int):
        errors.append("heartbeat runner result is missing an integer exit_code")
        return RECEIPT_CONTRACT_EXIT_CODE
    return value


def _attempt_row(
    policy: RunControlPolicy,
    plan: Mapping[str, Any],
    row: Mapping[str, Any],
    session_id: str,
    bucket: int,
    status: str,
    now_func: NowFunc,
) -> dict[str, Any]:
    return {
        "schema_version": policy.attempt_schema_version,
        "plan_id": plan["plan_id"],
        "plan_date": plan["plan_date"],
        "timestamp_utc": now_func(),
        "session_id": session_id,
        "attempt_id": row["attempt_id"],
        "attempt_resume": bool(row.get("attempt_resume")),
        "bucket": bucket,
        "stable_partition_key": row["stable_partition_key"],
        "platform_account_id": row.get("platform_account_id"),
        "creator_record_id": row.get("creator_record_id"),
        "handle_at_plan": row["handle"],
        "attempt_status": status,
        "actor": policy.actor,
    }


def _attempt_row_from_receipt(
    policy: RunControlPolicy,
    plan: Mapping[str, Any],
    row: Mapping[str, Any],
    receipt: Mapping[str, Any],
    receipt_jsonl: Path,
    session_id: str,
    bucket: int,
    now_func: NowFunc,
) -> dict[str, Any]:
    attempt = _attempt_row(policy, plan, row, session_id, bucket, str(receipt["status"]), now_func)
    attempt["run_id"] = receipt.get("run_id")
    attempt["receipt_status"] = receipt.get("status")
    attempt["receipt_pointer"] = str(receipt_jsonl)
    attempt["packet_pointer"] = receipt.get("packet_pointer")
    attempt["packet_id"] = receipt.get("packet_id")
    for key in ("access_gap_reason", "error_class", "error_message"):
        if receipt.get(key) is not None:
            attempt[key] = receipt[key]
    return attempt


def _session_summary(
    *,
    policy: RunControlPolicy,
    plan: Mapping[str, Any],
    bucket: int,
    session_id: str,
    selected_count: int,
    duplicate_prevented_count: int,
    skipped_by_lane_in_bucket_count: int,
    heartbeat_exit_code: int,
    effective_exit_code: int,
    receipt_jsonl: Path,
    receipts: Sequence[Mapping[str, Any]],
    contract_errors: Sequence[str],
    now_func: NowFunc,
) -> dict[str, Any]:
    counts = {status: 0 for status in RECEIPT_STATUSES}
    for receipt in receipts:
        counts[str(receipt["status"])] += 1
    return {
        "schema_version": policy.session_summary_schema_version,
        "run_control_version": policy.run_control_version,
        "plan_id": plan["plan_id"],
        "plan_date": plan["plan_date"],
        "session_id": session_id,
        "bucket": bucket,
        "generated_at_utc": now_func(),
        "selected_count": selected_count,
        "duplicate_prevented_count": duplicate_prevented_count,
        "skipped_by_lane_in_bucket_count": skipped_by_lane_in_bucket_count,
        "heartbeat_exit_code": heartbeat_exit_code,
        "effective_exit_code": effective_exit_code,
        "attempted_count": len(receipts),
        "succeeded_count": counts["succeeded"],
        "access_gap_count": counts["access_gap"],
        "failed_count": counts["failed"],
        "receipt_contract_error_count": len(contract_errors),
        "receipt_contract_errors": list(contract_errors),
        "receipt_jsonl": str(receipt_jsonl),
        "non_claims": ["operational session summary only", "not Silver", "not Gold"],
    }


def _write_session_roster(
    path: Path, *, plan: Mapping[str, Any], bucket: int, lane_id: str, rows: Sequence[Mapping[str, Any]]
) -> None:
    roster_rows = []
    for row in rows:
        out = dict(row)
        out["status"] = "active"
        roster_rows.append(out)
    _write_json(
        path,
        {
            "roster_snapshot_id": f"{plan['plan_id']}_bucket_{bucket}_{lane_id}",
            "plan_id": plan["plan_id"],
            "plan_date": plan["plan_date"],
            "platform": plan.get("platform"),
            "partition_preselected": True,
            "bucket": bucket,
            "creators": roster_rows,
        },
    )


def _load_daily_plan(path: Path, *, policy: RunControlPolicy) -> dict[str, Any]:
    plan = _load_json_object(path)
    if plan.get("schema_version") != policy.plan_schema_version:
        raise ValueError(f"daily plan has unsupported schema_version: {plan.get('schema_version')!r}")
    if not isinstance(plan.get("creators"), list):
        raise ValueError("daily plan creators must be a list")
    return plan


def _terminal_attempts_by_key(attempts: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    out: dict[str, Mapping[str, Any]] = {}
    for attempt in attempts:
        key = _optional_string(attempt.get("stable_partition_key"))
        if key is not None and attempt.get("attempt_status") in TERMINAL_ATTEMPT_STATUSES:
            out[key] = attempt
    return out


def _active_attempts_by_key(attempts: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    terminal = _terminal_attempts_by_key(attempts)
    out: dict[str, Mapping[str, Any]] = {}
    for attempt in attempts:
        key = _optional_string(attempt.get("stable_partition_key"))
        if key is not None and key not in terminal and attempt.get("attempt_status") in {"leased", "started"}:
            out[key] = attempt
    return out


def _load_json_object(path: Path) -> dict[str, Any]:
    parsed = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError(f"JSON file must contain an object: {path}")
    return parsed


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True)}\n", encoding="utf-8", newline="\n")


def _write_json_exclusive(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    try:
        fd = os.open(path, flags)
    except FileExistsError as exc:
        raise ValueError(f"daily plan already exists: {path}") from exc
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(f"{json.dumps(dict(payload), ensure_ascii=False, indent=2, sort_keys=True)}\n")
        handle.flush()
        os.fsync(handle.fileno())


def _required_string(value: object, field: str) -> str:
    text = _optional_string(value)
    if text is None:
        raise ValueError(f"{field} is missing or blank")
    return text


def _optional_string(value: object) -> str | None:
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    return None


def _int_field(row: Mapping[str, Any], key: str) -> int:
    value = row.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{key} must be an integer")
    return value


def _short_hash_values(*values: str) -> str:
    h = hashlib.sha256()
    for value in values:
        h.update(value.encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()[:12]


def _safe_segment(value: str) -> str:
    return "".join(char if char.isalnum() or char in {"-", "_", "."} else "_" for char in value)


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
        raise ValueError(f"lane_id must be one of: {', '.join(sorted(expected))}")


__all__ = [
    "DEFAULT_BUCKET_COUNT",
    "DEFAULT_SEED_SALT_ID",
    "DEFAULT_SEED_VERSION",
    "PlanDayResult",
    "RunControlPolicy",
    "RunSessionResult",
    "SummarizeDayResult",
    "append_attempt",
    "assign_daily_bucket",
    "assign_lane_id",
    "day_directory",
    "find_committed_packet_by_session_identity",
    "freeze_plan",
    "read_jsonl",
    "run_session",
    "summarize_day",
]
