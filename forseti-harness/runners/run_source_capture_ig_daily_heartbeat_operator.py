"""Operator-facing wrapper for IG daily heartbeat run-control sessions.

This module deliberately wraps the existing run-control layer instead of creating a
second heartbeat runner. One operator invocation can ensure a daily plan exists,
run exactly one bucket/lane session, and refresh the daily operational summary.
It does not register schedules, select egress, solve challenges, or add Silver /
Gold monitoring logic.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import utc_now_z
from runners import run_source_capture_ig_daily_heartbeat_control as control
from runners.run_source_capture_ig_daily_heartbeat import run_ig_daily_heartbeat


HeartbeatRunner = Callable[..., Any]
NowFunc = Callable[[], str]


@dataclass(frozen=True)
class OperatorSessionResult:
    plan_path: Path
    attempts_path: Path
    session_summary_path: Path
    daily_summary_path: Path
    planned_count: int
    selected_count: int
    heartbeat_exit_code: int
    effective_exit_code: int
    plan_created: bool

    @property
    def exit_code(self) -> int:
        return self.effective_exit_code

    def message(self) -> str:
        return str(self.daily_summary_path)


def run_operator_session(
    *,
    registry_index_path: Path,
    monitoring_sidecar_path: Path,
    run_control_root: Path,
    plan_date: str,
    bucket: int,
    lane_id: str,
    lane_count: int,
    output_root: Path | None = None,
    data_root: Any | None = None,
    plan_if_missing: bool = True,
    bucket_count: int = control.DEFAULT_BUCKET_COUNT,
    seed_salt_id: str = control.DEFAULT_SEED_SALT_ID,
    session_id: str | None = None,
    retry_statuses: Sequence[str] = (),
    lease_stale_seconds: int = 7200,
    max_creators: int | None = None,
    time_budget_seconds: float | None = None,
    allow_heavy_assets: bool = False,
    heartbeat_runner: HeartbeatRunner = run_ig_daily_heartbeat,
    now_func: NowFunc = utc_now_z,
) -> OperatorSessionResult:
    """Run one supervised daily-heartbeat operator session.

    If the daily plan is missing, this creates it from Creator Registry plus the
    monitoring sidecar. The session still runs exactly one bucket/lane; operators
    schedule multiple invocations rather than a standing crawler loop.
    """
    if (output_root is None) == (data_root is None):
        raise ValueError("exactly one of output_root or data_root is required")

    day_dir = control.day_directory(run_control_root, plan_date)
    plan_path = day_dir / "daily_plan.json"
    attempts_path = day_dir / "attempts.jsonl"
    plan_created = False

    if plan_path.exists():
        planned_count = _planned_count(plan_path)
    else:
        if not plan_if_missing:
            raise ValueError(f"daily plan missing and plan_if_missing is false: {plan_path}")
        try:
            plan_result = control.plan_day(
                registry_index_path=registry_index_path,
                monitoring_sidecar_path=monitoring_sidecar_path,
                run_control_root=run_control_root,
                plan_date=plan_date,
                bucket_count=bucket_count,
                seed_salt_id=seed_salt_id,
                overwrite=False,
                now_func=now_func,
            )
        except ValueError:
            # Another operator session can create the plan between our existence
            # check and plan_day's exclusive write. Reuse that winner; planning
            # errors that leave no plan still fail visibly.
            if not plan_path.exists():
                raise
            planned_count = _planned_count(plan_path)
        else:
            plan_created = True
            planned_count = plan_result.planned_count
            plan_path = plan_result.plan_path
            attempts_path = plan_result.attempts_path

    session_result = control.run_session(
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
    daily_result = control.summarize_day(
        run_control_root=run_control_root,
        plan_date=plan_date,
        now_func=now_func,
    )
    return OperatorSessionResult(
        plan_path=plan_path,
        attempts_path=attempts_path,
        session_summary_path=session_result.session_summary_path,
        daily_summary_path=daily_result.summary_path,
        planned_count=planned_count,
        selected_count=session_result.selected_count,
        heartbeat_exit_code=session_result.heartbeat_exit_code,
        effective_exit_code=session_result.effective_exit_code,
        plan_created=plan_created,
    )


def _planned_count(plan_path: Path) -> int:
    parsed = json.loads(plan_path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict) or not isinstance(parsed.get("creators"), list):
        raise ValueError(f"daily plan creators must be a list: {plan_path}")
    return len(parsed["creators"])


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one supervised IG daily heartbeat operator session."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser(
        "run-session",
        help="Ensure the daily plan exists, run one bucket/lane, then summarize the day.",
    )
    run.add_argument("--registry-index", type=Path, required=True)
    run.add_argument("--monitoring-sidecar", type=Path, required=True)
    run.add_argument("--run-control-root", type=Path, required=True)
    run.add_argument("--plan-date", required=True)
    run.add_argument("--bucket", type=int, required=True)
    run.add_argument("--lane-id", required=True)
    run.add_argument("--lane-count", type=int, required=True)
    target = run.add_mutually_exclusive_group(required=True)
    target.add_argument("--output-root", type=Path, default=None)
    target.add_argument("--data-root", default=None)
    run.add_argument("--no-plan-if-missing", action="store_true")
    run.add_argument("--bucket-count", type=int, default=control.DEFAULT_BUCKET_COUNT)
    run.add_argument("--seed-salt-id", default=control.DEFAULT_SEED_SALT_ID)
    run.add_argument("--session-id", default=None)
    run.add_argument("--retry-status", action="append", default=[])
    run.add_argument("--lease-stale-seconds", type=int, default=7200)
    run.add_argument("--max-creators", type=int, default=None)
    run.add_argument("--time-budget-seconds", type=float, default=None)
    run.add_argument("--allow-heavy-assets", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command != "run-session":
            parser.exit(status=2, message=f"unsupported command: {args.command}\n")
        data_root = None
        if args.data_root is not None:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)
        result = run_operator_session(
            registry_index_path=args.registry_index,
            monitoring_sidecar_path=args.monitoring_sidecar,
            run_control_root=args.run_control_root,
            plan_date=args.plan_date,
            bucket=args.bucket,
            lane_id=args.lane_id,
            lane_count=args.lane_count,
            output_root=args.output_root,
            data_root=data_root,
            plan_if_missing=not args.no_plan_if_missing,
            bucket_count=args.bucket_count,
            seed_salt_id=args.seed_salt_id,
            session_id=args.session_id,
            retry_statuses=args.retry_status,
            lease_stale_seconds=args.lease_stale_seconds,
            max_creators=args.max_creators,
            time_budget_seconds=args.time_budget_seconds,
            allow_heavy_assets=args.allow_heavy_assets,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"ig heartbeat operator session failed: {exc}\n")
    except Exception as exc:  # noqa: BLE001 - preserve visible operator failures
        parser.exit(status=3, message=f"ig heartbeat operator session failed: {type(exc).__name__}: {exc}\n")

    print(result.message())
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
