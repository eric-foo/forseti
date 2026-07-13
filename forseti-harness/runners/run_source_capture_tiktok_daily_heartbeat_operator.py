"""Operator wrapper for one TikTok daily heartbeat bucket/lane session."""
from __future__ import annotations

import argparse
import functools
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.root import DataLakeRoot
from harness_utils import utc_now_z
from runners import run_source_capture_tiktok_daily_heartbeat_control as control
from runners.run_source_capture_tiktok_daily_heartbeat import run_tiktok_daily_heartbeat
from source_capture.adapters.browser_snapshot import ChromeCdpPageObservationSessionEngine
from source_capture.auth_state import validate_auth_state_provenance_requirement
from source_capture.browser_user_data import browser_user_data_path_for_label
from source_capture.session_profiles import (
    default_session_profile_auth_state_root,
    resolve_session_profile,
)
from source_capture.tiktok.live_batch_probe import (
    TIKTOK_ACCOUNT_SAFETY_STOP_MARKERS,
    TIKTOK_BROWSER_BACKEND_CHROME_CDP,
    TIKTOK_CHALLENGE_TEXT_MARKERS,
    TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
)


@dataclass(frozen=True)
class OperatorSessionResult:
    plan_path: Path
    session_summary_path: Path
    daily_summary_path: Path
    planned_count: int
    selected_count: int
    effective_exit_code: int

    @property
    def exit_code(self) -> int:
        return self.effective_exit_code


def run_operator_session(
    *, active_roster_path: Path, run_control_root: Path, plan_date: str,
    bucket: int, lane_id: str, lane_count: int, output_root: Path | None = None,
    data_root: Any | None = None, session_profile_alias: str = "chowdakr_sg_tiktok",
    session_profile_config: Path | None = None, auth_state_root: Path | None = None,
    browser_user_data_root: Path | None = None, plan_if_missing: bool = True,
    heartbeat_runner: Callable[..., Any] | None = None,
    session_id: str | None = None, retry_statuses: Sequence[str] = (),
    lease_stale_seconds: int = 7200, max_creators: int | None = None,
    time_budget_seconds: float | None = None, now_func: Callable[[], str] = utc_now_z,
) -> OperatorSessionResult:
    if (output_root is None) == (data_root is None):
        raise ValueError("exactly one of output_root or data_root is required")
    day_dir = control.day_directory(run_control_root, plan_date)
    plan_path = day_dir / "daily_plan.json"
    if not plan_path.exists():
        if not plan_if_missing:
            raise ValueError(f"daily plan missing and plan_if_missing is false: {plan_path}")
        try:
            plan = control.plan_day(
                active_roster_path=active_roster_path,
                run_control_root=run_control_root,
                plan_date=plan_date,
                now_func=now_func,
            )
        except ValueError:
            # A concurrent operator may win the exclusive plan write. Reuse
            # that immutable winner; unrelated planning errors still fail.
            if not plan_path.exists():
                raise
        else:
            plan_path = plan.plan_path
    planned_count = len(json.loads(plan_path.read_text(encoding="utf-8"))["creators"])

    owned_engine = None
    if heartbeat_runner is None:
        profile = resolve_session_profile(session_profile_alias, config_path=session_profile_config)
        if profile.browser_backend != TIKTOK_BROWSER_BACKEND_CHROME_CDP:
            raise ValueError("TikTok daily heartbeat requires Chrome CDP")
        if profile.browser_user_data_label is None:
            raise ValueError("TikTok daily heartbeat requires a retained browser_user_data_label")
        resolved_auth_root = auth_state_root or default_session_profile_auth_state_root()
        storage_state_path = validate_auth_state_provenance_requirement(
            profile.state_label,
            session_mode=profile.session_mode,
            required_harness_proxy_profile_posture=profile.required_harness_proxy_profile_posture,
            auth_state_root=resolved_auth_root,
        )
        user_data_dir = browser_user_data_path_for_label(
            profile.browser_user_data_label, user_data_root=browser_user_data_root
        )
        if not user_data_dir.is_dir() or not any(user_data_dir.iterdir()):
            raise ValueError("retained browser profile is missing or empty")
        owned_engine = ChromeCdpPageObservationSessionEngine(
            pre_action_stop_markers=TIKTOK_ACCOUNT_SAFETY_STOP_MARKERS,
            human_challenge_handoff_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
            human_challenge_handoff_timeout_seconds=180.0,
            human_challenge_handoff_prompt=TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
        )
        heartbeat_runner = functools.partial(
            run_tiktok_daily_heartbeat,
            storage_state_path=storage_state_path,
            engine=owned_engine,
        )
    try:
        session = control.run_session(
            run_control_root=run_control_root,
            plan_date=plan_date,
            bucket=bucket,
            lane_id=lane_id,
            lane_count=lane_count,
            heartbeat_runner=heartbeat_runner,
            output_root=output_root,
            data_root=data_root,
            session_id=session_id,
            retry_statuses=retry_statuses,
            lease_stale_seconds=lease_stale_seconds,
            max_creators=max_creators,
            time_budget_seconds=time_budget_seconds,
            now_func=now_func,
        )
    finally:
        if owned_engine is not None:
            owned_engine.close()
    daily = control.summarize_day(
        run_control_root=run_control_root, plan_date=plan_date, now_func=now_func
    )
    return OperatorSessionResult(
        plan_path=plan_path,
        session_summary_path=session.session_summary_path,
        daily_summary_path=daily.summary_path,
        planned_count=planned_count,
        selected_count=session.selected_count,
        effective_exit_code=session.effective_exit_code,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--active-roster", required=True, type=Path)
    parser.add_argument("--run-control-root", required=True, type=Path)
    parser.add_argument("--plan-date", required=True)
    parser.add_argument("--bucket", required=True, type=int)
    parser.add_argument("--lane-id", required=True)
    parser.add_argument("--lane-count", required=True, type=int)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--output-root", type=Path)
    target.add_argument("--data-root")
    parser.add_argument("--session-profile", default="chowdakr_sg_tiktok")
    parser.add_argument("--session-profile-config", type=Path)
    parser.add_argument("--retry-status", action="append", default=[])
    parser.add_argument("--max-creators", type=int)
    parser.add_argument("--time-budget-seconds", type=float)
    parser.add_argument("--no-plan-if-missing", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root) if args.data_root else None
        result = run_operator_session(
            active_roster_path=args.active_roster,
            run_control_root=args.run_control_root,
            plan_date=args.plan_date,
            bucket=args.bucket,
            lane_id=args.lane_id,
            lane_count=args.lane_count,
            output_root=args.output_root,
            data_root=data_root,
            session_profile_alias=args.session_profile,
            session_profile_config=args.session_profile_config,
            plan_if_missing=not args.no_plan_if_missing,
            retry_statuses=args.retry_status,
            max_creators=args.max_creators,
            time_budget_seconds=args.time_budget_seconds,
        )
    except Exception as exc:  # noqa: BLE001 - operator boundary reports visible failure
        parser.exit(3, f"TikTok heartbeat operator failed: {type(exc).__name__}: {exc}\n")
    print(result.daily_summary_path)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
