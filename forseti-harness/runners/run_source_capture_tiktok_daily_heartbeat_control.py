"""TikTok bindings for the shared daily heartbeat run-control core."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from harness_utils import utc_now_z
from source_capture import social_heartbeat_run_control as shared_control

RUN_CONTROL_VERSION = "tiktok_daily_heartbeat_run_control_v0"
RUN_CONTROL_NAMESPACE = Path("run_control") / "tiktok_daily_heartbeat"
DEFAULT_BUCKET_COUNT = 4
DEFAULT_SEED_SALT_ID = "daily_bucket_v1"

SHARED_POLICY = shared_control.RunControlPolicy(
    platform="tiktok",
    namespace=RUN_CONTROL_NAMESPACE,
    run_control_version=RUN_CONTROL_VERSION,
    plan_schema_version="tiktok_daily_heartbeat_daily_plan_v0",
    attempt_schema_version="tiktok_daily_heartbeat_attempt_v0",
    session_summary_schema_version="tiktok_daily_heartbeat_session_summary_v0",
    daily_summary_schema_version="tiktok_daily_heartbeat_daily_summary_v0",
    plan_id_prefix="tiktok_daily_heartbeat_plan",
    actor="tiktok_daily_heartbeat_run_control",
)


def plan_day(
    *, active_roster_path: Path, run_control_root: Path, plan_date: str,
    bucket_count: int = DEFAULT_BUCKET_COUNT, seed_salt_id: str = DEFAULT_SEED_SALT_ID,
    overwrite: bool = False, now_func: Callable[[], str] = utc_now_z,
) -> shared_control.PlanDayResult:
    payload = json.loads(active_roster_path.read_text(encoding="utf-8"))
    rows = payload if isinstance(payload, list) else payload.get("creators") if isinstance(payload, dict) else None
    if not isinstance(rows, list):
        raise ValueError("TikTok active roster must be a list or contain creators")
    creators = [_active_creator(row, index) for index, row in enumerate(rows, start=1)]
    source_sha = hashlib.sha256(active_roster_path.read_bytes()).hexdigest()
    return shared_control.freeze_plan(
        policy=SHARED_POLICY,
        creators=creators,
        source_inputs={"active_roster": {"path": str(active_roster_path), "sha256": source_sha}},
        run_control_root=run_control_root,
        plan_date=plan_date,
        bucket_count=bucket_count,
        seed_salt_id=seed_salt_id,
        overwrite=overwrite,
        now_func=now_func,
    )


def run_session(
    *, run_control_root: Path, plan_date: str, bucket: int, lane_id: str, lane_count: int,
    heartbeat_runner: Callable[..., Any], output_root: Path | None = None, data_root: Any | None = None,
    session_id: str | None = None, retry_statuses: Sequence[str] = (), lease_stale_seconds: int = 7200,
    max_creators: int | None = None, time_budget_seconds: float | None = None,
    allow_heavy_assets: bool = False, now_func: Callable[[], str] = utc_now_z,
) -> shared_control.RunSessionResult:
    return shared_control.run_session(
        policy=SHARED_POLICY,
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
        allow_heavy_assets=allow_heavy_assets,
        now_func=now_func,
    )


def summarize_day(
    *, run_control_root: Path, plan_date: str, now_func: Callable[[], str] = utc_now_z,
) -> shared_control.SummarizeDayResult:
    return shared_control.summarize_day(
        policy=SHARED_POLICY,
        run_control_root=run_control_root,
        plan_date=plan_date,
        now_func=now_func,
    )


def day_directory(run_control_root: Path, plan_date: str) -> Path:
    return shared_control.day_directory(run_control_root, SHARED_POLICY, plan_date)


def _active_creator(raw: object, index: int) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise ValueError(f"TikTok active roster row {index} must be an object")
    platform = str(raw.get("platform") or "").strip().lower()
    if platform != "tiktok":
        raise ValueError(f"TikTok active roster row {index} platform must be tiktok")
    if str(raw.get("monitoring_status") or "").strip().lower() != "active":
        raise ValueError(f"TikTok active roster row {index} monitoring_status must be active")
    if str(raw.get("cadence") or "").strip().lower() != "daily":
        raise ValueError(f"TikTok active roster row {index} cadence must be daily")
    account_id = str(raw.get("platform_account_id") or "").strip()
    if not account_id:
        raise ValueError(f"TikTok active roster row {index} is missing platform_account_id")
    handle = str(raw.get("handle") or raw.get("public_handle") or "").strip().lstrip("@").lower()
    if not handle or "/" in handle or "\\" in handle:
        raise ValueError(f"TikTok active roster row {index} has invalid handle")
    return {
        **dict(raw),
        "platform": "tiktok",
        "handle": handle,
        "platform_account_id": account_id,
        "stable_partition_key": f"platform_account_id:{account_id}",
        "partition_key_source": "platform_account_id",
    }


__all__ = [
    "DEFAULT_BUCKET_COUNT", "DEFAULT_SEED_SALT_ID", "SHARED_POLICY", "day_directory",
    "plan_day", "run_session", "summarize_day",
]
