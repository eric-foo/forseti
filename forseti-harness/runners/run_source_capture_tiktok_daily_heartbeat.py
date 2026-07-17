"""Capture grid-only TikTok heartbeat observations for a preselected roster."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.adapters.browser_snapshot import (
    BrowserPageObservationEngine,
    BrowserSnapshotFailure,
    ChromeCdpPageObservationSessionEngine,
)
from source_capture.auth_state import validate_auth_state_provenance_requirement
from source_capture.browser_user_data import browser_user_data_path_for_label
from source_capture.session_profiles import (
    default_session_profile_auth_state_root,
    resolve_session_profile,
)
from source_capture.tiktok.creator_onboarding import (
    DEFAULT_MAX_GRID_SCROLL_PASSES,
    DEFAULT_WINDOW_SIZE,
    build_tiktok_grid_window,
    capture_tiktok_creator_grid,
)
from source_capture.tiktok.grid_packet import (
    TIKTOK_GRID_PACKET_SOURCE_SURFACE,
    write_tiktok_grid_packet,
)
from source_capture.tiktok.live_batch_probe import (
    TIKTOK_ACCOUNT_SAFETY_STOP_MARKERS,
    TIKTOK_BROWSER_BACKEND_CHROME_CDP,
    TIKTOK_CHALLENGE_TEXT_MARKERS,
    TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
)
from source_capture.social_heartbeat_run_control import (
    assign_lane_id,
    find_committed_packet_by_session_identity,
)
from capture_spine.creator_profile_current.silver_envelope_core import (
    METRIC_OBSERVATION_LANE,
)
from capture_spine.creator_profile_current.tiktok_grid_observation_producer import (
    TIKTOK_PROFILE_METRIC_FIELDS,
    profile_metric_record_id,
)
from data_lake.silver_record import (
    validate_silver_vault_record,
    verify_silver_vault_record_sources,
)
from runners.run_tiktok_grid_observation_producer import (
    run_tiktok_grid_observations,
)

RECEIPT_SCHEMA_VERSION = "tiktok_daily_heartbeat_receipt_v1"
CONTROLLER_VERSION = "tiktok_daily_heartbeat_controller_v1"


@dataclass(frozen=True)
class TikTokHeartbeatRunResult:
    exit_code: int
    processed_count: int
    succeeded_count: int
    access_gap_count: int
    failed_count: int
    selected_count: int
    skipped_by_lane_count: int
    stopped_by_budget: bool
    deferred_partition_keys: tuple[str, ...] = ()


def run_tiktok_daily_heartbeat(
    *,
    roster_path: Path,
    receipt_jsonl: Path,
    lane_id: str,
    lane_count: int,
    output_root: Path | None = None,
    data_root: Any | None = None,
    max_creators: int | None = None,
    time_budget_seconds: float | None = None,
    block_heavy_assets: bool = True,
    partition_preselected: bool = False,
    storage_state_path: Path,
    engine: BrowserPageObservationEngine,
    window_size: int = DEFAULT_WINDOW_SIZE,
    minimum_window_size: int = 1,
    max_grid_scroll_passes: int = DEFAULT_MAX_GRID_SCROLL_PASSES,
    timeout_seconds: float = 30.0,
    settle_seconds: float = 2.0,
) -> TikTokHeartbeatRunResult:
    """Run one bounded grid-only session using an already-acquired browser lease."""
    del block_heavy_assets  # CDP session policy is owned by the platform adapter.
    if (output_root is None) == (data_root is None):
        raise ValueError("exactly one of output_root or data_root is required")
    if max_creators is not None and max_creators < 0:
        raise ValueError("max_creators must be non-negative")
    payload = json.loads(roster_path.read_text(encoding="utf-8"))
    rows = payload.get("creators") if isinstance(payload, dict) else None
    if not isinstance(rows, list):
        raise ValueError("TikTok heartbeat roster creators must be a list")
    parsed = [_parse_roster_row(row, index) for index, row in enumerate(rows, start=1)]
    selected = parsed if partition_preselected else [
        row for row in parsed if assign_lane_id(row["stable_partition_key"], lane_count) == lane_id
    ]
    skipped_by_lane = len(parsed) - len(selected)
    if max_creators is not None:
        selected = selected[:max_creators]

    receipt_jsonl.parent.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    counts = {"succeeded": 0, "access_gap": 0, "failed": 0}
    processed = 0
    stopped_by_budget = False
    context_stopped = False
    deferred: list[str] = []
    for row in selected:
        if time_budget_seconds is not None and time.monotonic() - started >= time_budget_seconds:
            stopped_by_budget = True
            break
        if context_stopped:
            deferred.append(row["stable_partition_key"])
            continue
        else:
            receipt, context_stopped = _run_one(
                row=row,
                receipt_jsonl=receipt_jsonl,
                lane_id=lane_id,
                lane_count=lane_count,
                output_root=output_root,
                data_root=data_root,
                storage_state_path=storage_state_path,
                engine=engine,
                window_size=window_size,
                minimum_window_size=minimum_window_size,
                max_grid_scroll_passes=max_grid_scroll_passes,
                timeout_seconds=timeout_seconds,
                settle_seconds=settle_seconds,
            )
        _append_jsonl(receipt_jsonl, receipt)
        processed += 1
        counts[str(receipt["status"])] += 1
    return TikTokHeartbeatRunResult(
        exit_code=0,
        processed_count=processed,
        succeeded_count=counts["succeeded"],
        access_gap_count=counts["access_gap"],
        failed_count=counts["failed"],
        selected_count=len(selected),
        skipped_by_lane_count=skipped_by_lane,
        stopped_by_budget=stopped_by_budget,
        deferred_partition_keys=tuple(deferred),
    )


def _run_one(
    *, row: dict[str, Any], receipt_jsonl: Path, lane_id: str, lane_count: int,
    output_root: Path | None, data_root: Any | None, storage_state_path: Path,
    engine: BrowserPageObservationEngine, window_size: int, minimum_window_size: int,
    max_grid_scroll_passes: int, timeout_seconds: float, settle_seconds: float,
) -> tuple[dict[str, Any], bool]:
    receipt = _base_receipt(row, lane_id=lane_id, lane_count=lane_count)
    attempt_id = row["attempt_id"]
    packet_output = output_root / "heartbeat_attempts" / attempt_id if output_root is not None else None
    try:
        existing = None
        if row["attempt_resume"] and data_root is not None:
            existing = find_committed_packet_by_session_identity(
                data_root,
                session_identity=attempt_id,
                source_surface=TIKTOK_GRID_PACKET_SOURCE_SURFACE,
            )
        elif row["attempt_resume"] and packet_output is not None:
            existing = _existing_local_packet(packet_output, attempt_id)
        if existing is not None:
            packet_id, packet_path = existing
            receipt.update(_success_fields(packet_id, packet_path, reconciled=True))
            receipt.update(
                _profile_metric_silver_fields(data_root=data_root, packet_id=packet_id)
                if data_root is not None
                else _local_profile_metric_silver_fields()
            )
            return receipt, False

        artifact_path = receipt_jsonl.parent / "attempt_artifacts" / attempt_id / "tiktok_grid_window.json"
        if artifact_path.is_file():
            raw_window = artifact_path.read_bytes()
            _verify_frozen_binding(raw_window, row)
        elif row["attempt_resume"]:
            raise RuntimeError(
                "resumed attempt has neither a verified committed packet nor a reusable frozen grid window"
            )
        else:
            capture = capture_tiktok_creator_grid(
                profile_url=f"https://www.tiktok.com/@{row['handle']}",
                creator_handle=row["handle"],
                storage_state_path=storage_state_path,
                window_size=window_size,
                timeout_seconds=timeout_seconds,
                settle_seconds=settle_seconds,
                max_grid_scroll_passes=max_grid_scroll_passes,
                engine=engine,
            )
            if isinstance(capture, BrowserSnapshotFailure):
                raise RuntimeError(f"grid capture failed: {capture.failure_kind.value}: {capture.message}")
            stop_reason = _capture_stop_reason(capture.metadata)
            if stop_reason is not None:
                receipt.update({"status": "access_gap", "access_gap_reason": stop_reason})
                return receipt, True
            window = build_tiktok_grid_window(
                creator_handle=row["handle"],
                capture=capture,
                window_size=window_size,
                minimum_window_size=minimum_window_size,
            )
            window["heartbeat_binding"] = {
                "attempt_id": attempt_id,
                "stable_partition_key": row["stable_partition_key"],
                "platform_account_id": row["platform_account_id"],
            }
            raw_window = (json.dumps(window, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
            _write_bytes_atomic(artifact_path, raw_window)

        code, pointer = write_tiktok_grid_packet(
            grid_window_json=raw_window,
            output_directory=packet_output,
            data_root=data_root,
            session_identity=attempt_id,
        )
        if code != 0:
            raise RuntimeError(f"TikTok grid admission returned exit code {code}")
        packet_path = Path(pointer)
        manifest = json.loads((packet_path / "manifest.json").read_text(encoding="utf-8"))
        packet_id = str(manifest.get("packet_id") or "").strip()
        if not packet_id or manifest.get("session_identity") != attempt_id:
            raise RuntimeError("committed packet does not bind the heartbeat attempt identity")
        receipt.update(_success_fields(packet_id, packet_path, reconciled=row["attempt_resume"]))
        receipt["grid_window_sha256"] = hashlib.sha256(raw_window).hexdigest()
        receipt.update(
            _profile_metric_silver_fields(data_root=data_root, packet_id=packet_id)
            if data_root is not None
            else _local_profile_metric_silver_fields()
        )
        return receipt, False
    except Exception as exc:  # noqa: BLE001 - terminal receipt preserves failure visibility
        receipt.update({
            "status": "failed",
            "error_class": type(exc).__name__,
            "error_message": str(exc),
        })
        return receipt, False


def _parse_roster_row(raw: object, index: int) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise ValueError(f"TikTok heartbeat roster row {index} must be an object")
    platform = str(raw.get("platform") or "").strip().lower()
    if platform != "tiktok":
        raise ValueError(f"TikTok heartbeat roster row {index} has wrong platform")
    required = {}
    for field in ("platform_account_id", "stable_partition_key", "attempt_id"):
        value = raw.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"TikTok heartbeat roster row {index} is missing {field}")
        required[field] = value.strip()
    handle = str(raw.get("handle") or raw.get("public_handle") or "").strip().lstrip("@").lower()
    if not handle or "/" in handle or "\\" in handle:
        raise ValueError(f"TikTok heartbeat roster row {index} has invalid handle")
    return {
        **dict(raw),
        **required,
        "handle": handle,
        "attempt_resume": raw.get("attempt_resume") is True,
    }


def _base_receipt(row: Mapping[str, Any], *, lane_id: str, lane_count: int) -> dict[str, Any]:
    return {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "controller_version": CONTROLLER_VERSION,
        "attempt_id": row["attempt_id"],
        "partition_key": row["stable_partition_key"],
        "assigned_lane_id": assign_lane_id(str(row["stable_partition_key"]), lane_count),
        "lane_id": lane_id,
        "lane_count": lane_count,
        "creator": {
            "platform": "tiktok",
            "handle": row["handle"],
            "platform_account_id": row["platform_account_id"],
        },
        "source_surface": TIKTOK_GRID_PACKET_SOURCE_SURFACE,
        "status": "failed",
        "packet_pointer": None,
    }


def _success_fields(packet_id: str, packet_path: Path, *, reconciled: bool) -> dict[str, Any]:
    return {
        "status": "succeeded",
        "packet_id": packet_id,
        "packet_pointer": str(packet_path),
        "reconciled_existing_packet": reconciled,
    }


def _local_profile_metric_silver_fields() -> dict[str, Any]:
    return {
        "profile_metric_silver_status": "not_applicable_without_data_root",
        "profile_metric_record_ids": [],
    }


def _profile_metric_silver_fields(*, data_root: Any, packet_id: str) -> dict[str, Any]:
    results = run_tiktok_grid_observations(
        data_root=data_root,
        packet_ids=[packet_id],
    )
    packet_results = [
        row for row in results if row.get("packet_id") == packet_id
    ]
    failures = [row for row in packet_results if row.get("status") == "failed"]
    if failures:
        raise RuntimeError(
            f"TikTok profile metric Silver projection failed: {failures[0].get('error')}"
        )
    if not any(
        row.get("status") in {"derived", "already_current"}
        for row in packet_results
    ):
        raise RuntimeError(
            "TikTok profile metric Silver projection did not verify the admitted packet"
        )

    record_ids = [
        profile_metric_record_id(packet_id, metric_name)
        for metric_name, _source_field in TIKTOK_PROFILE_METRIC_FIELDS
    ]
    observed_metric_names: list[str] = []
    for record_id in record_ids:
        path = data_root.record_path(
            subtree="derived",
            raw_anchor=packet_id,
            lane=METRIC_OBSERVATION_LANE,
            record_id=record_id,
        )
        if not path.is_file():
            raise RuntimeError(
                f"TikTok profile metric Silver record is absent after projection: {record_id}"
            )
        record = json.loads(path.read_text(encoding="utf-8"))
        validate_silver_vault_record(record)
        verify_silver_vault_record_sources(data_root, record, record_path=path)
        observation = record["payload"]["observation"]
        observed_metric_names.append(str(observation["metric_name"]))
    expected_metric_names = [name for name, _source_field in TIKTOK_PROFILE_METRIC_FIELDS]
    if observed_metric_names != expected_metric_names:
        raise RuntimeError("TikTok profile metric Silver records have unexpected identities")
    return {
        "profile_metric_silver_status": "verified",
        "profile_metric_record_ids": record_ids,
    }


def _capture_stop_reason(metadata: Mapping[str, object]) -> str | None:
    stops = metadata.get("pre_action_stop_attempts")
    if isinstance(stops, list) and stops:
        return "account_safety_stop"
    handoffs = metadata.get("human_challenge_handoff_attempts")
    if isinstance(handoffs, list) and any(
        isinstance(item, Mapping) and item.get("cleared") is not True for item in handoffs
    ):
        return "human_challenge_unresolved"
    return None


def _verify_frozen_binding(raw: bytes, row: Mapping[str, Any]) -> None:
    payload = json.loads(raw.decode("utf-8"))
    binding = payload.get("heartbeat_binding") if isinstance(payload, dict) else None
    expected = {
        "attempt_id": row["attempt_id"],
        "stable_partition_key": row["stable_partition_key"],
        "platform_account_id": row["platform_account_id"],
    }
    if binding != expected:
        raise ValueError("frozen TikTok grid window heartbeat binding mismatch")


def _existing_local_packet(packet_path: Path, attempt_id: str) -> tuple[str, Path] | None:
    manifest_path = packet_path / "manifest.json"
    if not manifest_path.is_file():
        return None
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("session_identity") != attempt_id:
        raise ValueError("existing local packet does not match the heartbeat attempt identity")
    packet_id = str(manifest.get("packet_id") or "").strip()
    preserved = manifest.get("preserved_files")
    if not packet_id or not isinstance(preserved, list) or not preserved:
        raise ValueError("existing local heartbeat packet manifest is incomplete")
    for item in preserved:
        if not isinstance(item, Mapping):
            raise ValueError("existing local heartbeat packet preserved_files entry is invalid")
        relative = str(item.get("relative_packet_path") or "").strip()
        expected = str(item.get("sha256") or "").strip()
        body = (packet_path / relative).read_bytes()
        if not relative or not expected or hashlib.sha256(body).hexdigest() != expected:
            raise ValueError("existing local heartbeat packet body verification failed")
    return packet_id, packet_path


def _write_bytes_atomic(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(payload)
    os.replace(temporary, path)
    if path.read_bytes() != payload:
        raise OSError("frozen TikTok grid window readback mismatch")


def _append_jsonl(path: Path, payload: Mapping[str, Any]) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(dict(payload), ensure_ascii=False, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


__all__ = ["TikTokHeartbeatRunResult", "run_tiktok_daily_heartbeat"]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--roster", required=True, type=Path)
    parser.add_argument("--receipt-jsonl", required=True, type=Path)
    parser.add_argument("--lane-id", required=True)
    parser.add_argument("--lane-count", required=True, type=int)
    destination = parser.add_mutually_exclusive_group(required=True)
    destination.add_argument("--admit-output", dest="output_root", type=Path)
    destination.add_argument("--data-root")
    parser.add_argument("--session-profile", default="chowdakr_sg_tiktok")
    parser.add_argument("--session-profile-config", type=Path)
    parser.add_argument("--max-creators", type=int)
    parser.add_argument("--time-budget-seconds", type=float)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    engine = None
    try:
        from data_lake.root import DataLakeRoot

        data_root = (
            DataLakeRoot.resolve(explicit=args.data_root)
            if args.data_root is not None
            else None
        )
        profile = resolve_session_profile(args.session_profile, config_path=args.session_profile_config)
        if profile.browser_backend != TIKTOK_BROWSER_BACKEND_CHROME_CDP:
            raise ValueError("TikTok daily heartbeat requires Chrome CDP")
        if profile.browser_user_data_label is None:
            raise ValueError("TikTok daily heartbeat requires a retained browser_user_data_label")
        storage_state_path = validate_auth_state_provenance_requirement(
            profile.state_label,
            session_mode=profile.session_mode,
            required_harness_proxy_profile_posture=profile.required_harness_proxy_profile_posture,
            auth_state_root=default_session_profile_auth_state_root(),
        )
        user_data_dir = browser_user_data_path_for_label(profile.browser_user_data_label)
        if not user_data_dir.is_dir() or not any(user_data_dir.iterdir()):
            raise ValueError("retained browser profile is missing or empty")
        engine = ChromeCdpPageObservationSessionEngine(
            pre_action_stop_markers=TIKTOK_ACCOUNT_SAFETY_STOP_MARKERS,
            human_challenge_handoff_markers=TIKTOK_CHALLENGE_TEXT_MARKERS,
            human_challenge_handoff_timeout_seconds=180.0,
            human_challenge_handoff_prompt=TIKTOK_HUMAN_CHALLENGE_HANDOFF_PROMPT,
        )
        result = run_tiktok_daily_heartbeat(
            roster_path=args.roster,
            receipt_jsonl=args.receipt_jsonl,
            lane_id=args.lane_id,
            lane_count=args.lane_count,
            output_root=args.output_root,
            data_root=data_root,
            max_creators=args.max_creators,
            time_budget_seconds=args.time_budget_seconds,
            storage_state_path=storage_state_path,
            engine=engine,
        )
    except Exception as exc:  # noqa: BLE001 - CLI boundary reports a visible failure
        parser.exit(3, f"TikTok daily heartbeat failed: {type(exc).__name__}: {exc}\n")
    finally:
        if engine is not None:
            engine.close()
    print(args.receipt_jsonl)
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
