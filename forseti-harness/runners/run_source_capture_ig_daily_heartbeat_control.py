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
import sys
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import utc_now_z
from runners.run_source_capture_ig_daily_heartbeat import run_ig_daily_heartbeat
from source_capture import social_heartbeat_run_control as shared_control


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

SHARED_POLICY = shared_control.RunControlPolicy(
    platform="instagram",
    namespace=RUN_CONTROL_NAMESPACE,
    run_control_version=RUN_CONTROL_VERSION,
    plan_schema_version=PLAN_SCHEMA_VERSION,
    attempt_schema_version=ATTEMPT_SCHEMA_VERSION,
    session_summary_schema_version=SESSION_SUMMARY_SCHEMA_VERSION,
    daily_summary_schema_version=DAILY_SUMMARY_SCHEMA_VERSION,
    plan_id_prefix="ig_daily_heartbeat_plan",
    actor="ig_daily_heartbeat_run_control",
)

HeartbeatRunner = Callable[..., Any]
NowFunc = Callable[[], str]


PlanDayResult = shared_control.PlanDayResult
RunSessionResult = shared_control.RunSessionResult
SummarizeDayResult = shared_control.SummarizeDayResult


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
            }
        )

    registry_sha256 = _sha256_file(registry_index_path)
    sidecar_sha256 = _sha256_file(monitoring_sidecar_path)
    return shared_control.freeze_plan(
        policy=SHARED_POLICY,
        creators=creators,
        source_inputs={
            "source_registry": {"path": str(registry_index_path), "sha256": registry_sha256},
            "monitoring_sidecar": {"path": str(monitoring_sidecar_path), "sha256": sidecar_sha256},
        },
        plan_metadata={
            "source_registry": {"path": str(registry_index_path), "sha256": registry_sha256},
            "monitoring_sidecar": {"path": str(monitoring_sidecar_path), "sha256": sidecar_sha256},
        },
        run_control_root=run_control_root,
        plan_date=plan_date,
        bucket_count=bucket_count,
        seed_salt_id=seed_salt_id,
        overwrite=overwrite,
        now_func=now_func,
    )


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
    return shared_control.run_session(
        policy=SHARED_POLICY,
        run_control_root=run_control_root,
        plan_date=plan_date,
        bucket=bucket,
        lane_id=lane_id,
        lane_count=lane_count,
        output_root=output_root,
        data_root=data_root,
        heartbeat_runner=heartbeat_runner,
        session_id=session_id,
        retry_statuses=retry_statuses,
        lease_stale_seconds=lease_stale_seconds,
        max_creators=max_creators,
        time_budget_seconds=time_budget_seconds,
        allow_heavy_assets=allow_heavy_assets,
        now_func=now_func,
    )


def summarize_day(*, run_control_root: Path, plan_date: str, now_func: NowFunc = utc_now_z) -> SummarizeDayResult:
    return shared_control.summarize_day(
        policy=SHARED_POLICY,
        run_control_root=run_control_root,
        plan_date=plan_date,
        now_func=now_func,
    )


def day_directory(run_control_root: Path, plan_date: str) -> Path:
    return shared_control.day_directory(run_control_root, SHARED_POLICY, plan_date)


def assign_daily_bucket(
    stable_key: str,
    *,
    plan_date: str,
    bucket_count: int = DEFAULT_BUCKET_COUNT,
    seed_salt_id: str = DEFAULT_SEED_SALT_ID,
) -> int:
    return shared_control.assign_daily_bucket(
        stable_key,
        plan_date=plan_date,
        bucket_count=bucket_count,
        seed_salt_id=seed_salt_id,
    )


def assign_heartbeat_lane_id(stable_partition_key: str, lane_count: int) -> str:
    """Compatibility name for the now-shared canonical lane assignment."""
    return shared_control.assign_lane_id(stable_partition_key, lane_count)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return shared_control.read_jsonl(path)


def append_attempt(path: Path, payload: Mapping[str, Any]) -> None:
    shared_control.append_attempt(path, payload)


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


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
