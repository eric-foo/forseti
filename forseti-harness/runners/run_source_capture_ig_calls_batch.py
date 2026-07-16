from __future__ import annotations

import argparse
from datetime import UTC, datetime, timedelta
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Sequence
from urllib.parse import urlparse

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runners.run_source_capture_ig_calls_packet import (
    DEFAULT_CAPTURE_RETRY_BACKOFF_SECONDS,
    DEFAULT_IG_PROFILE_VIEWPORT_HEIGHT,
    DEFAULT_IG_PROFILE_VIEWPORT_WIDTH,
    DEFAULT_MAX_ARTIFACT_BYTES,
    DEFAULT_PROFILE_LINK_RETRIES,
    DEFAULT_PROFILE_LINK_RETRY_BACKOFF_SECONDS,
    DEFAULT_PROFILE_SCROLL_PASSES,
    DEFAULT_PROFILE_SETTLE_SECONDS,
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_VIEW_COUNT_MAX_GRAPHQL_PAGES,
    DEFAULT_XHR_REQUEST_GAP_SECONDS,
    IG_CIRCUIT_BREAK_EXIT_CODE,
    run_source_capture_ig_calls_packet,
)
from source_capture.auth_state import AuthenticatedSessionMode
from source_capture.cadence import CadenceMode, build_cadence_plan


DEFAULT_MAX_PROFILES = 10
DEFAULT_MAX_ITEMS_PER_PROFILE = 6
DEFAULT_INTER_PROFILE_DELAY_SECONDS = 60.0
DEFAULT_COOLDOWN_SECONDS = 3600.0
IG_CALLS_BATCH_EXIT_CODE_COOLDOWN_ACTIVE = IG_CIRCUIT_BREAK_EXIT_CODE

_SLOT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
_IG_HANDLE_RE = re.compile(r"^[A-Za-z0-9._]{1,30}$")
_CIRCUIT_BREAK_LIMITATION_PREFIX = "ig_circuit_break_recommended"


@dataclass(frozen=True)
class IgCallsBatchSlot:
    slot_id: str
    profile_url: str
    handle: str


def default_cooldown_ledger_path() -> Path:
    return Path(__file__).resolve().parents[1] / "_test_runs" / "ig_calls_cooldown_ledger.json"


def run_source_capture_ig_calls_batch(
    *,
    slots: Sequence[IgCallsBatchSlot],
    output_root: Path,
    decision_question: str,
    max_profiles: int = DEFAULT_MAX_PROFILES,
    max_items_per_profile: int = DEFAULT_MAX_ITEMS_PER_PROFILE,
    profile_scroll_passes: int = DEFAULT_PROFILE_SCROLL_PASSES,
    inter_profile_delay_seconds: float = DEFAULT_INTER_PROFILE_DELAY_SECONDS,
    cadence_mode: CadenceMode = "fixed",
    cadence_window_seconds: float | None = None,
    cadence_min_gap_seconds: float | None = None,
    cadence_max_gap_seconds: float | None = None,
    cadence_random_seed: int | None = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_artifact_bytes: int = DEFAULT_MAX_ARTIFACT_BYTES,
    capture_view_counts: bool = True,
    view_count_max_graphql_pages: int = DEFAULT_VIEW_COUNT_MAX_GRAPHQL_PAGES,
    xhr_request_gap_seconds: float = DEFAULT_XHR_REQUEST_GAP_SECONDS,
    capture_retries: int = 0,
    capture_retry_backoff_seconds: float = DEFAULT_CAPTURE_RETRY_BACKOFF_SECONDS,
    profile_settle_seconds: float = DEFAULT_PROFILE_SETTLE_SECONDS,
    profile_link_retries: int = DEFAULT_PROFILE_LINK_RETRIES,
    profile_link_retry_backoff_seconds: float = DEFAULT_PROFILE_LINK_RETRY_BACKOFF_SECONDS,
    auth_state_label: str | None = None,
    auth_session_mode: AuthenticatedSessionMode | None = None,
    auth_state_root: Path | None = None,
    cooldown_ledger_path: Path | None = None,
    cooldown_seconds: float = DEFAULT_COOLDOWN_SECONDS,
    ignore_cooldown: bool = False,
    smoke_mode: bool = False,
    now_fn: Callable[[], datetime] | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> tuple[int, str]:
    if smoke_mode:
        _validate_smoke_mode_inputs(
            slots=slots,
            output_root=output_root,
            max_profiles=max_profiles,
            max_items_per_profile=max_items_per_profile,
            inter_profile_delay_seconds=inter_profile_delay_seconds,
            cadence_mode=cadence_mode,
            ignore_cooldown=ignore_cooldown,
        )
    _validate_batch_inputs(
        slots=slots,
        output_root=output_root,
        max_profiles=max_profiles,
        max_items_per_profile=max_items_per_profile,
        inter_profile_delay_seconds=inter_profile_delay_seconds,
        cooldown_seconds=cooldown_seconds,
    )
    now_fn = now_fn or (lambda: datetime.now(UTC))
    cooldown_ledger_path = cooldown_ledger_path or default_cooldown_ledger_path()
    cadence = build_cadence_plan(
        slot_count=len(slots),
        mode=cadence_mode,
        delay_seconds=inter_profile_delay_seconds,
        window_seconds=cadence_window_seconds,
        min_gap_seconds=cadence_min_gap_seconds,
        max_gap_seconds=cadence_max_gap_seconds,
        random_seed=cadence_random_seed,
    )

    output_root.mkdir(parents=True, exist_ok=True)
    summary_path = output_root / "ig_calls_batch_summary.json"
    if summary_path.exists():
        raise ValueError(f"IG calls batch summary already exists: {summary_path}")

    cooldown_active = _active_cooldown(cooldown_ledger_path=cooldown_ledger_path, now=now_fn())
    if cooldown_active is not None and not ignore_cooldown:
        summary = _build_summary(
            status="cooldown_active",
            slots=slots,
            max_profiles=max_profiles,
            max_items_per_profile=max_items_per_profile,
            capture_view_counts=capture_view_counts,
            cadence=cadence.to_dict(),
            auth_state_label=auth_state_label,
            auth_session_mode=auth_session_mode,
            cooldown_policy=_cooldown_policy(cooldown_seconds=cooldown_seconds, ledger_enabled=True),
            cooldown=cooldown_active,
            results=[],
            smoke_mode=smoke_mode,
        )
        _write_json(summary_path, summary)
        return IG_CALLS_BATCH_EXIT_CODE_COOLDOWN_ACTIVE, str(summary_path)

    results: list[dict[str, Any]] = []
    batch_status = "completed"
    cooldown_record: dict[str, Any] | None = None
    for index, slot in enumerate(slots):
        packet_dir = output_root / slot.slot_id
        per_profile_seed = None if cadence_random_seed is None else cadence_random_seed + index
        row: dict[str, Any] = {
            "slot_id": slot.slot_id,
            "handle": slot.handle,
            "profile_url": slot.profile_url,
            "packet_dir": str(packet_dir),
            "capture_exit": None,
            "capture_message": None,
            "packet_written": False,
            "circuit_break_detected": False,
            "circuit_break_reason": None,
            "planned_start_offset_seconds": cadence.planned_offsets_seconds[index],
            "planned_wait_after_seconds": (
                cadence.planned_waits_seconds[index]
                if index < len(cadence.planned_waits_seconds)
                else None
            ),
            "capture_started_at": None,
            "capture_finished_at": None,
        }

        run_limitations = [
            "batch_runner=ig_calls_batch",
            f"batch_slot_id={slot.slot_id}",
            "batch_inputs_locked_before_run",
            "batch_runner_no_discovery",
        ]
        if smoke_mode:
            run_limitations.append("batch_smoke_mode=max_profiles_1_max_items_1_cooldown_respected")

        try:
            row["capture_started_at"] = _utc_now(now_fn)
            capture_exit, capture_message = run_source_capture_ig_calls_packet(
                profile_url=slot.profile_url,
                output_directory=packet_dir,
                decision_question=decision_question,
                max_items=max_items_per_profile,
                profile_scroll_passes=profile_scroll_passes,
                cadence_random_seed=per_profile_seed,
                timeout_seconds=timeout_seconds,
                max_artifact_bytes=max_artifact_bytes,
                capture_view_counts=capture_view_counts,
                view_count_max_graphql_pages=view_count_max_graphql_pages,
                xhr_request_gap_seconds=xhr_request_gap_seconds,
                capture_retries=capture_retries,
                capture_retry_backoff_seconds=capture_retry_backoff_seconds,
                profile_settle_seconds=profile_settle_seconds,
                profile_link_retries=profile_link_retries,
                profile_link_retry_backoff_seconds=profile_link_retry_backoff_seconds,
                auth_state_label=auth_state_label,
                auth_session_mode=auth_session_mode,
                auth_state_root=auth_state_root,
                limitations=run_limitations,
                sleep_fn=sleep_fn,
            )
            row["capture_exit"] = capture_exit
            row["capture_message"] = capture_message
        except Exception as exc:  # noqa: BLE001 - keep per-slot failures visible in summary
            row["capture_exit"] = 2
            row["capture_message"] = f"{type(exc).__name__}: {exc}"
        finally:
            row["capture_finished_at"] = _utc_now(now_fn)

        if row["capture_exit"] == 0:
            row["packet_written"] = True
            manifest_break = _manifest_circuit_break_reason(packet_dir / "manifest.json")
            if manifest_break is not None:
                row["circuit_break_detected"] = True
                row["circuit_break_reason"] = manifest_break
        elif row["capture_exit"] == IG_CIRCUIT_BREAK_EXIT_CODE:
            row["circuit_break_detected"] = True
            row["circuit_break_reason"] = str(row["capture_message"])

        results.append(row)
        if row["circuit_break_detected"]:
            batch_status = "stopped_circuit_break"
            cooldown_record = _write_cooldown_record(
                cooldown_ledger_path=cooldown_ledger_path,
                cooldown_seconds=cooldown_seconds,
                now=now_fn(),
                trigger_row=row,
                output_root=output_root,
            )
            break

        if index < len(cadence.planned_waits_seconds):
            wait_seconds = cadence.planned_waits_seconds[index]
            if wait_seconds > 0:
                sleep_fn(wait_seconds)

    summary = _build_summary(
        status=batch_status,
        slots=slots,
        max_profiles=max_profiles,
        max_items_per_profile=max_items_per_profile,
        capture_view_counts=capture_view_counts,
        cadence=cadence.to_dict(),
        auth_state_label=auth_state_label,
        auth_session_mode=auth_session_mode,
        cooldown_policy=_cooldown_policy(cooldown_seconds=cooldown_seconds, ledger_enabled=True),
        cooldown=cooldown_record,
        results=results,
        smoke_mode=smoke_mode,
    )
    _write_json(summary_path, summary)
    return (IG_CIRCUIT_BREAK_EXIT_CODE if batch_status == "stopped_circuit_break" else 0), str(summary_path)


def load_slots(path: Path) -> list[IgCallsBatchSlot]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("IG profile list must be a JSON array")
    slots: list[IgCallsBatchSlot] = []
    for index, item in enumerate(payload, start=1):
        if isinstance(item, str):
            slot_id = f"slot_{index:03d}"
            profile_url, handle = _canonical_profile_url_and_handle(item)
        elif isinstance(item, dict):
            raw_slot_id = item.get("slot_id") or item.get("id")
            if not isinstance(raw_slot_id, str) or not raw_slot_id.strip():
                raise ValueError(f"IG profile list item {index} must include a non-empty slot_id")
            raw_profile = item.get("profile_url")
            raw_handle = item.get("handle")
            if isinstance(raw_profile, str) and isinstance(raw_handle, str):
                raise ValueError(f"IG profile list item {index} must include handle or profile_url, not both")
            raw_target = raw_profile if isinstance(raw_profile, str) else raw_handle
            if not isinstance(raw_target, str) or not raw_target.strip():
                raise ValueError(f"IG profile list item {index} must include handle or profile_url")
            slot_id = raw_slot_id.strip()
            profile_url, handle = _canonical_profile_url_and_handle(raw_target)
        else:
            raise ValueError(f"IG profile list item {index} must be a string or object")
        slots.append(
            IgCallsBatchSlot(
                slot_id=_validate_slot_id(slot_id),
                profile_url=profile_url,
                handle=handle,
            )
        )
    return slots


def slots_from_handles(handles: Sequence[str]) -> list[IgCallsBatchSlot]:
    slots: list[IgCallsBatchSlot] = []
    for index, handle in enumerate(handles, start=1):
        profile_url, normalized = _canonical_profile_url_and_handle(handle)
        slots.append(
            IgCallsBatchSlot(
                slot_id=_validate_slot_id(normalized.replace(".", "_")),
                profile_url=profile_url,
                handle=normalized,
            )
        )
    return slots


def _validate_batch_inputs(
    *,
    slots: Sequence[IgCallsBatchSlot],
    output_root: Path,
    max_profiles: int,
    max_items_per_profile: int,
    inter_profile_delay_seconds: float,
    cooldown_seconds: float,
) -> None:
    if not slots:
        raise ValueError("IG calls batch requires at least one profile")
    if max_profiles <= 0:
        raise ValueError("max_profiles must be greater than zero")
    if len(slots) > max_profiles:
        raise ValueError(f"IG calls batch received {len(slots)} profile(s), above max_profiles={max_profiles}")
    if max_items_per_profile <= 0:
        raise ValueError("max_items_per_profile must be greater than zero")
    if inter_profile_delay_seconds < 0:
        raise ValueError("inter_profile_delay_seconds must be zero or greater")
    if cooldown_seconds < 0:
        raise ValueError("cooldown_seconds must be zero or greater")
    slot_ids = [slot.slot_id for slot in slots]
    duplicates = sorted({slot_id for slot_id in slot_ids if slot_ids.count(slot_id) > 1})
    if duplicates:
        raise ValueError(f"duplicate slot_id value(s): {duplicates}")
    for slot in slots:
        _validate_slot_id(slot.slot_id)
        _canonical_profile_url_and_handle(slot.profile_url)
    if output_root.exists() and not output_root.is_dir():
        raise ValueError(f"output_root is not a directory: {output_root}")


def _validate_smoke_mode_inputs(
    *,
    slots: Sequence[IgCallsBatchSlot],
    output_root: Path,
    max_profiles: int,
    max_items_per_profile: int,
    inter_profile_delay_seconds: float,
    cadence_mode: CadenceMode,
    ignore_cooldown: bool,
) -> None:
    if len(slots) != 1:
        raise ValueError("IG smoke mode requires exactly one profile")
    if max_profiles != 1:
        raise ValueError("IG smoke mode requires max_profiles=1")
    if max_items_per_profile != 1:
        raise ValueError("IG smoke mode requires max_items_per_profile=1")
    if inter_profile_delay_seconds != 0:
        raise ValueError("IG smoke mode requires inter_profile_delay_seconds=0")
    if cadence_mode != "fixed":
        raise ValueError("IG smoke mode requires fixed cadence")
    if ignore_cooldown:
        raise ValueError("IG smoke mode respects cooldown and cannot be combined with --ignore-cooldown")
    if output_root.exists():
        raise ValueError("IG smoke mode requires a new output_root")


def _canonical_profile_url_and_handle(raw: str) -> tuple[str, str]:
    target = raw.strip()
    if not target:
        raise ValueError("IG handle/profile URL must be non-empty")
    if target.startswith("@"):
        target = target[1:]
    if target.lower().startswith(("http://", "https://")):
        parsed = urlparse(target)
        if parsed.scheme != "https" or parsed.netloc.lower() not in {"www.instagram.com", "instagram.com"}:
            raise ValueError("IG profile URL must be an https://www.instagram.com/<handle>/ URL")
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) != 1:
            raise ValueError("IG profile URL must point to exactly one public profile handle")
        handle = parts[0]
    else:
        handle = target
    if handle.lower() in {"p", "reel", "stories", "explore", "accounts", "api", "graphql"}:
        raise ValueError("IG calls batch accepts profile handles only, not item or system paths")
    if not _IG_HANDLE_RE.fullmatch(handle):
        raise ValueError("IG handle must be 1-30 characters using letters, numbers, dot, or underscore")
    return f"https://www.instagram.com/{handle}/", handle


def _validate_slot_id(slot_id: str) -> str:
    if not _SLOT_ID_RE.fullmatch(slot_id):
        raise ValueError("slot_id must be 1-64 characters using letters, numbers, dot, underscore, or hyphen")
    if "/" in slot_id or "\\" in slot_id or Path(slot_id).name != slot_id:
        raise ValueError("slot_id must not contain path separators")
    return slot_id


def _manifest_circuit_break_reason(manifest_path: Path) -> str | None:
    if not manifest_path.is_file():
        return None
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    limitations = manifest.get("limitations", [])
    if not isinstance(limitations, list):
        return None
    for item in limitations:
        if isinstance(item, str) and _CIRCUIT_BREAK_LIMITATION_PREFIX in item:
            return item
    return None


def _active_cooldown(*, cooldown_ledger_path: Path, now: datetime) -> dict[str, Any] | None:
    if not cooldown_ledger_path.is_file():
        return None
    payload = json.loads(cooldown_ledger_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("IG cooldown ledger must be a JSON object")
    raw_until = payload.get("cooldown_until")
    if not isinstance(raw_until, str):
        raise ValueError("IG cooldown ledger missing cooldown_until")
    cooldown_until = _parse_utc(raw_until)
    if cooldown_until <= now:
        return None
    out = dict(payload)
    out["cooldown_active"] = True
    return out


def _write_cooldown_record(
    *,
    cooldown_ledger_path: Path,
    cooldown_seconds: float,
    now: datetime,
    trigger_row: dict[str, Any],
    output_root: Path,
) -> dict[str, Any]:
    cooldown_until = now + timedelta(seconds=cooldown_seconds)
    record = {
        "runner": "ig_calls_batch",
        "cooldown_started_at": _format_utc(now),
        "cooldown_until": _format_utc(cooldown_until),
        "cooldown_seconds": cooldown_seconds,
        "trigger_slot_id": trigger_row.get("slot_id"),
        "trigger_handle": trigger_row.get("handle"),
        "trigger_profile_url": trigger_row.get("profile_url"),
        "trigger_exit": trigger_row.get("capture_exit"),
        "trigger_reason": trigger_row.get("circuit_break_reason"),
        "batch_output_root": str(output_root),
        "non_claims": [
            "not proof of exact IG cooldown decay",
            "not validation",
            "not session effectiveness proof",
        ],
    }
    cooldown_ledger_path.parent.mkdir(parents=True, exist_ok=True)
    _write_json(cooldown_ledger_path, record)
    return record


def _build_summary(
    *,
    status: str,
    slots: Sequence[IgCallsBatchSlot],
    max_profiles: int,
    max_items_per_profile: int,
    capture_view_counts: bool,
    cadence: dict[str, object],
    auth_state_label: str | None,
    auth_session_mode: AuthenticatedSessionMode | None,
    cooldown_policy: dict[str, object],
    cooldown: dict[str, Any] | None,
    results: Sequence[dict[str, Any]],
    smoke_mode: bool,
) -> dict[str, Any]:
    return {
        "runner": "ig_calls_batch",
        "method": "wrap_existing_ig_calls_packet_runner",
        "smoke_mode": smoke_mode,
        "status": status,
        "non_claims": [
            "not crawler",
            "not source discovery",
            "not passive monitoring",
            "not comment body or timestamp capture",
            "not media byte capture",
            "not live validation",
            "not cooldown-duration proof",
        ],
        "profile_count": len(slots),
        "max_profiles": max_profiles,
        "max_items_per_profile": max_items_per_profile,
        "capture_view_counts": capture_view_counts,
        "auth_state_loaded": auth_session_mode is not None,
        "auth_session_mode": auth_session_mode.value if auth_session_mode is not None else None,
        "auth_state_label": auth_state_label,
        "auth_state_path_recorded": False,
        "cadence": cadence,
        "cooldown_policy": cooldown_policy,
        "cooldown": cooldown,
        "slots": [slot.__dict__ for slot in slots],
        "results": list(results),
        "attempted_count": len(results),
        "packet_success_count": sum(1 for row in results if row.get("capture_exit") == 0),
        "circuit_break_count": sum(1 for row in results if row.get("circuit_break_detected") is True),
    }


def _cooldown_policy(*, cooldown_seconds: float, ledger_enabled: bool) -> dict[str, object]:
    return {
        "ledger_enabled": ledger_enabled,
        "cooldown_seconds": cooldown_seconds,
        "quiet_window_source": "IG calibration note minimum quiet cooldown",
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(f"{json.dumps(payload, indent=2, sort_keys=True)}\n", encoding="utf-8", newline="\n")


def _utc_now(now_fn: Callable[[], datetime]) -> str:
    # Diverges from harness_utils.utc_now_z: injected clock and keeps microsecond precision.
    return _format_utc(now_fn())


def _format_utc(value: datetime) -> str:
    value = value.astimezone(UTC) if value.tzinfo is not None else value.replace(tzinfo=UTC)
    return value.isoformat().replace("+00:00", "Z")


def _parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a bounded locked-list IG calls batch using the existing per-profile packet runner."
    )
    parser.add_argument("--profile-list", type=Path, help="JSON array of IG handles or profile URL objects.")
    parser.add_argument("--handle", action="append", default=[], help="Locked IG handle to include in the batch.")
    parser.add_argument("--decision-question", required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--max-profiles", type=int, default=DEFAULT_MAX_PROFILES)
    parser.add_argument("--max-items-per-profile", type=int, default=DEFAULT_MAX_ITEMS_PER_PROFILE)
    parser.add_argument("--profile-scroll-passes", type=int, default=DEFAULT_PROFILE_SCROLL_PASSES)
    parser.add_argument("--inter-profile-delay-seconds", type=float, default=DEFAULT_INTER_PROFILE_DELAY_SECONDS)
    parser.add_argument("--cadence-mode", choices=["fixed", "bounded_jitter"], default="fixed")
    parser.add_argument("--cadence-window-seconds", type=float, default=None)
    parser.add_argument("--cadence-min-gap-seconds", type=float, default=None)
    parser.add_argument("--cadence-max-gap-seconds", type=float, default=None)
    parser.add_argument("--cadence-random-seed", type=int, default=None)
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--max-artifact-bytes", type=int, default=DEFAULT_MAX_ARTIFACT_BYTES)
    parser.add_argument("--skip-view-counts", action="store_true")
    parser.add_argument("--view-count-max-graphql-pages", type=int, default=DEFAULT_VIEW_COUNT_MAX_GRAPHQL_PAGES)
    parser.add_argument("--xhr-request-gap-seconds", type=float, default=DEFAULT_XHR_REQUEST_GAP_SECONDS)
    parser.add_argument("--capture-retries", type=int, default=0)
    parser.add_argument("--capture-retry-backoff-seconds", type=float, default=DEFAULT_CAPTURE_RETRY_BACKOFF_SECONDS)
    parser.add_argument("--profile-settle-seconds", type=float, default=DEFAULT_PROFILE_SETTLE_SECONDS)
    parser.add_argument("--profile-link-retries", type=int, default=DEFAULT_PROFILE_LINK_RETRIES)
    parser.add_argument("--profile-link-retry-backoff-seconds", type=float, default=DEFAULT_PROFILE_LINK_RETRY_BACKOFF_SECONDS)
    auth_group = parser.add_argument_group(
        "auth state",
        "Optional ignored Playwright storage-state label. No cookies, paths, or credentials are accepted.",
    )
    auth_group.add_argument("--auth-state-label", default=None)
    auth_group.add_argument("--session-mode", choices=[item.value for item in AuthenticatedSessionMode], default=None)
    auth_group.add_argument("--auth-state-root", type=Path, default=None)
    parser.add_argument("--cooldown-ledger", type=Path, default=None)
    parser.add_argument("--cooldown-seconds", type=float, default=DEFAULT_COOLDOWN_SECONDS)
    parser.add_argument("--ignore-cooldown", action="store_true")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Force the safest live smoke envelope: one locked profile, one item, fixed zero inter-profile delay, cooldown respected, and a fresh output root.",
    )
    return parser


def _slots_from_args(args: argparse.Namespace) -> list[IgCallsBatchSlot]:
    slots: list[IgCallsBatchSlot] = []
    if args.profile_list is not None:
        slots.extend(load_slots(args.profile_list))
    if args.handle:
        slots.extend(slots_from_handles(args.handle))
    if not slots:
        raise ValueError("supply --profile-list or at least one --handle")
    seen: set[str] = set()
    for slot in slots:
        if slot.slot_id in seen:
            raise ValueError(f"duplicate slot_id in IG calls batch: {slot.slot_id}")
        seen.add(slot.slot_id)
    return slots


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        slots = _slots_from_args(args)
        max_profiles = 1 if args.smoke else args.max_profiles
        max_items_per_profile = 1 if args.smoke else args.max_items_per_profile
        inter_profile_delay_seconds = 0.0 if args.smoke else args.inter_profile_delay_seconds
        cadence_mode = "fixed" if args.smoke else args.cadence_mode
        cadence_window_seconds = None if args.smoke else args.cadence_window_seconds
        cadence_min_gap_seconds = None if args.smoke else args.cadence_min_gap_seconds
        cadence_max_gap_seconds = None if args.smoke else args.cadence_max_gap_seconds
        exit_code, message = run_source_capture_ig_calls_batch(
            slots=slots,
            output_root=args.output_root,
            decision_question=args.decision_question,
            max_profiles=max_profiles,
            max_items_per_profile=max_items_per_profile,
            profile_scroll_passes=args.profile_scroll_passes,
            inter_profile_delay_seconds=inter_profile_delay_seconds,
            cadence_mode=cadence_mode,
            cadence_window_seconds=cadence_window_seconds,
            cadence_min_gap_seconds=cadence_min_gap_seconds,
            cadence_max_gap_seconds=cadence_max_gap_seconds,
            cadence_random_seed=args.cadence_random_seed,
            timeout_seconds=args.timeout_seconds,
            max_artifact_bytes=args.max_artifact_bytes,
            capture_view_counts=not args.skip_view_counts,
            view_count_max_graphql_pages=args.view_count_max_graphql_pages,
            xhr_request_gap_seconds=args.xhr_request_gap_seconds,
            capture_retries=args.capture_retries,
            capture_retry_backoff_seconds=args.capture_retry_backoff_seconds,
            profile_settle_seconds=args.profile_settle_seconds,
            profile_link_retries=args.profile_link_retries,
            profile_link_retry_backoff_seconds=args.profile_link_retry_backoff_seconds,
            auth_state_label=args.auth_state_label,
            auth_session_mode=AuthenticatedSessionMode(args.session_mode) if args.session_mode else None,
            auth_state_root=args.auth_state_root,
            cooldown_ledger_path=args.cooldown_ledger,
            cooldown_seconds=args.cooldown_seconds,
            ignore_cooldown=args.ignore_cooldown,
            smoke_mode=args.smoke,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"source capture ig calls batch failed: {exc}\n")
    except Exception as exc:  # noqa: BLE001 - surface unexpected runner failures visibly
        parser.exit(status=3, message=f"source capture ig calls batch failed: {exc}\n")
    if exit_code == 0:
        print(message)
        return 0
    parser.exit(status=exit_code, message=f"source capture ig calls batch failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
