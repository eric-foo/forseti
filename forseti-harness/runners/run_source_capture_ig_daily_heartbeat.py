"""IG daily heartbeat controller.

This controller owns batch orchestration for registered IG creator grid
heartbeats. It intentionally delegates page observation to the optimized
``run_source_capture_ig_reels_grid_packet`` primitive and keeps monitoring
logic out of the runner: no pagination, no scoring, no platform writes, and no
deep-capture target invention.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence
from urllib.parse import urlparse

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import generate_ulid, utc_now_z
from runners.run_source_capture_ig_reels_grid_packet import (
    DEFAULT_MAX_ROWS,
    SOURCE_SURFACE,
    run_source_capture_ig_reels_grid_packet,
)
from source_capture.ig_reels_grid_capture import (
    DEFAULT_IG_REELS_MAX_RESPONSE_BYTES,
    DEFAULT_IG_REELS_SETTLE_SECONDS,
    DEFAULT_IG_REELS_TIMEOUT_SECONDS,
    DEFAULT_IG_REELS_VIEWPORT_HEIGHT,
    DEFAULT_IG_REELS_VIEWPORT_WIDTH,
)
from source_capture.social_heartbeat_run_control import (
    assign_lane_id as assign_social_heartbeat_lane_id,
    find_committed_packet_by_session_identity,
)


CONTROLLER_VERSION = "ig_daily_heartbeat_controller_v0"
BEHAVIOR_POLICY_VERSION = "ig_daily_heartbeat_operating_policy_v0"
RECEIPT_SCHEMA_VERSION = "ig_daily_heartbeat_receipt_v0"
PARTITION_ALGORITHM_VERSION = "sha256_stable_key_mod_lane_count_v0"
SOURCE_SURFACE_HEARTBEAT = "ig_daily_heartbeat_first_visible_reels_grid"
GRID_SCOPE = "first_visible_grid_only"

ALLOWED_BREAKOUT_TAGS = frozenset(
    {
        "spike_candidate",
        "fresh_breakout_candidate",
        "active_breakout_candidate",
        "durable_breakout_candidate",
    }
)

GridRunner = Callable[..., tuple[int, str]]
NowFunc = Callable[[], str]
MonotonicFunc = Callable[[], float]


@dataclass(frozen=True)
class HeartbeatRosterEntry:
    handle: str
    platform_account_id: str | None = None
    platform_public_account_id: str | None = None
    creator_record_id: str | None = None
    ig_roster_record_id: str | None = None
    public_profile_url: str | None = None
    roster_status: str = "active"
    stable_partition_key: str = ""
    partition_key_source: str = ""
    attempt_id: str | None = None
    attempt_resume: bool = False
    limitations: tuple[str, ...] = ()

    @property
    def normalized_handle(self) -> str:
        return normalize_handle(self.handle)

    @property
    def reels_url(self) -> str:
        return f"https://www.instagram.com/{self.normalized_handle}/reels/"


@dataclass(frozen=True)
class HeartbeatRosterSnapshot:
    snapshot_id: str
    source_path: Path
    source_sha256: str
    source_kind: str
    entries: tuple[HeartbeatRosterEntry, ...]
    limitations: tuple[str, ...] = ()

    @property
    def active_entries(self) -> tuple[HeartbeatRosterEntry, ...]:
        return tuple(entry for entry in self.entries if _is_active_status(entry.roster_status))


@dataclass(frozen=True)
class BreakoutCandidate:
    handle: str
    tag: str
    platform_item_id: str
    source: str | None = None

    def to_receipt_dict(self) -> dict[str, str]:
        out = {
            "tag": self.tag,
            "platform_item_id": self.platform_item_id,
        }
        if self.source:
            out["source"] = self.source
        return out


@dataclass(frozen=True)
class HeartbeatRunResult:
    run_id: str
    receipt_jsonl: Path
    attempted_count: int
    succeeded_count: int
    access_gap_count: int
    failed_count: int
    selected_count: int
    skipped_by_lane_count: int
    stopped_by_budget: bool = False

    @property
    def exit_code(self) -> int:
        return 0

    def message(self) -> str:
        return str(self.receipt_jsonl)


@dataclass(frozen=True)
class _PacketSummary:
    fields: Mapping[str, Any] = field(default_factory=dict)
    warnings: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()


class HeartbeatRecoveryError(RuntimeError):
    """Raised when an interrupted attempt cannot be resumed without recapture."""


def normalize_handle(value: str) -> str:
    normalized = value.strip().lstrip("@")
    if not normalized or "/" in normalized or "\\" in normalized:
        raise ValueError(f"invalid IG handle: {value!r}")
    return normalized


def load_ig_heartbeat_roster(path: Path) -> HeartbeatRosterSnapshot:
    raw = path.read_bytes()
    try:
        data = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"roster JSON is invalid: {path}: {exc}") from exc

    source_sha256 = hashlib.sha256(raw).hexdigest()
    source_kind, snapshot_id, rows, source_limitations = _extract_roster_rows(data, path=path)
    entries: list[HeartbeatRosterEntry] = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"roster row {index} must be an object")
        entry = _entry_from_row(row, index=index, source_kind=source_kind)
        if entry is not None:
            entries.append(entry)

    return HeartbeatRosterSnapshot(
        snapshot_id=snapshot_id,
        source_path=path,
        source_sha256=source_sha256,
        source_kind=source_kind,
        entries=tuple(entries),
        limitations=tuple(source_limitations),
    )


def assign_lane_id(partition_key: str, lane_count: int) -> str:
    return assign_social_heartbeat_lane_id(partition_key, lane_count)


def load_breakout_candidates(path: Path | None) -> dict[str, tuple[BreakoutCandidate, ...]]:
    if path is None:
        return {}
    records = _load_breakout_records(path)
    by_handle: dict[str, list[BreakoutCandidate]] = {}
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"breakout candidate row {index} must be an object")
        platform = _optional_string(record.get("platform"))
        if platform is not None and platform.lower() != "instagram":
            raise ValueError(f"breakout candidate row {index} is not an instagram candidate")
        raw_tag = _first_string(record, ("tag", "breakout_tag", "candidate_tag"))
        if raw_tag is None or raw_tag not in ALLOWED_BREAKOUT_TAGS:
            allowed = ", ".join(sorted(ALLOWED_BREAKOUT_TAGS))
            raise ValueError(f"breakout candidate row {index} has unsupported tag {raw_tag!r}; allowed: {allowed}")
        raw_handle = _first_string(
            record,
            ("handle", "ig_handle", "platform_handle", "creator_handle", "public_handle"),
        )
        if raw_handle is None:
            raise ValueError(f"breakout candidate row {index} is missing handle")
        platform_item_id = _first_string(
            record,
            ("platform_item_id", "post_shortcode", "shortcode", "reel_shortcode"),
        )
        if platform_item_id is None:
            raise ValueError(f"breakout candidate row {index} is missing platform item id")
        handle = normalize_handle(raw_handle).lower()
        candidate = BreakoutCandidate(
            handle=handle,
            tag=raw_tag,
            platform_item_id=platform_item_id,
            source=_first_string(record, ("source", "source_run_id", "producer")),
        )
        by_handle.setdefault(handle, []).append(candidate)
    return {handle: tuple(items) for handle, items in by_handle.items()}


def run_ig_daily_heartbeat(
    *,
    roster_path: Path,
    receipt_jsonl: Path,
    lane_id: str,
    lane_count: int,
    output_root: Path | None = None,
    data_root: object | None = None,
    breakout_candidates_path: Path | None = None,
    max_creators: int | None = None,
    time_budget_seconds: float | None = None,
    max_rows: int = DEFAULT_MAX_ROWS,
    timeout_seconds: float = DEFAULT_IG_REELS_TIMEOUT_SECONDS,
    settle_seconds: float = DEFAULT_IG_REELS_SETTLE_SECONDS,
    viewport_width: int = DEFAULT_IG_REELS_VIEWPORT_WIDTH,
    viewport_height: int = DEFAULT_IG_REELS_VIEWPORT_HEIGHT,
    max_response_bytes: int = DEFAULT_IG_REELS_MAX_RESPONSE_BYTES,
    block_heavy_assets: bool = True,
    partition_preselected: bool = False,
    grid_runner: GridRunner = run_source_capture_ig_reels_grid_packet,
    now_func: NowFunc = utc_now_z,
    monotonic_func: MonotonicFunc = time.monotonic,
) -> HeartbeatRunResult:
    if (output_root is None) == (data_root is None):
        raise ValueError("exactly one of output_root or data_root is required")
    if max_creators is not None and max_creators < 0:
        raise ValueError("max_creators must be non-negative")
    if time_budget_seconds is not None and time_budget_seconds < 0:
        raise ValueError("time_budget_seconds must be non-negative")
    _validate_lane_id(lane_id=lane_id, lane_count=lane_count)

    roster = load_ig_heartbeat_roster(roster_path)
    breakout_candidates = load_breakout_candidates(breakout_candidates_path)
    run_id = generate_ulid()
    receipt_jsonl.parent.mkdir(parents=True, exist_ok=True)
    receipt_jsonl.touch(exist_ok=True)

    selected = list(roster.active_entries) if partition_preselected else [
        entry
        for entry in roster.active_entries
        if assign_lane_id(entry.stable_partition_key, lane_count) == lane_id
    ]
    skipped_by_lane_count = len(roster.active_entries) - len(selected)
    if max_creators is not None:
        selected = selected[:max_creators]

    attempted = 0
    succeeded = 0
    access_gaps = 0
    failed = 0
    stopped_by_budget = False
    run_started_monotonic = monotonic_func()

    for index, entry in enumerate(selected, start=1):
        if time_budget_seconds is not None and monotonic_func() - run_started_monotonic >= time_budget_seconds:
            stopped_by_budget = True
            break
        receipt = _run_one_creator(
            run_id=run_id,
            sequence=index,
            roster=roster,
            entry=entry,
            attempt_id=entry.attempt_id or generate_ulid(),
            lane_id=lane_id,
            lane_count=lane_count,
            output_root=output_root,
            data_root=data_root,
            breakout_candidates=breakout_candidates.get(entry.normalized_handle.lower(), ()),
            max_rows=max_rows,
            timeout_seconds=timeout_seconds,
            settle_seconds=settle_seconds,
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            max_response_bytes=max_response_bytes,
            block_heavy_assets=block_heavy_assets,
            grid_runner=grid_runner,
            now_func=now_func,
            monotonic_func=monotonic_func,
        )
        attempted += 1
        if receipt["status"] == "succeeded":
            succeeded += 1
        elif receipt["status"] == "access_gap":
            access_gaps += 1
        else:
            failed += 1
        _append_jsonl(receipt_jsonl, receipt)

    return HeartbeatRunResult(
        run_id=run_id,
        receipt_jsonl=receipt_jsonl,
        attempted_count=attempted,
        succeeded_count=succeeded,
        access_gap_count=access_gaps,
        failed_count=failed,
        selected_count=len(selected),
        skipped_by_lane_count=skipped_by_lane_count,
        stopped_by_budget=stopped_by_budget,
    )


def _run_one_creator(
    *,
    run_id: str,
    sequence: int,
    roster: HeartbeatRosterSnapshot,
    entry: HeartbeatRosterEntry,
    attempt_id: str,
    lane_id: str,
    lane_count: int,
    output_root: Path | None,
    data_root: object | None,
    breakout_candidates: Sequence[BreakoutCandidate],
    max_rows: int,
    timeout_seconds: float,
    settle_seconds: float,
    viewport_width: int,
    viewport_height: int,
    max_response_bytes: int,
    block_heavy_assets: bool,
    grid_runner: GridRunner,
    now_func: NowFunc,
    monotonic_func: MonotonicFunc,
) -> dict[str, Any]:
    started_at = now_func()
    started_monotonic = monotonic_func()
    packet_output_directory = _packet_output_directory(
        output_root=output_root,
        run_id=run_id,
        lane_id=lane_id,
        sequence=sequence,
        handle=entry.normalized_handle,
        attempt_id=attempt_id,
    )
    packet_pointer: str | None = None
    packet_summary = _PacketSummary()
    exit_code: int | None = None
    message = ""
    error_class: str | None = None

    reconciled = False
    try:
        if entry.attempt_resume:
            existing = _find_existing_attempt_packet(
                output_directory=packet_output_directory,
                data_root=data_root,
                attempt_id=attempt_id,
            )
            if existing is None:
                raise HeartbeatRecoveryError(
                    "resumed attempt has neither a verified committed packet nor a reusable frozen artifact"
                )
            packet_pointer = str(existing)
            message = packet_pointer
            exit_code = 0
            packet_summary = _read_packet_summary(existing)
            reconciled = True
        else:
            kwargs = {
                "handle": entry.normalized_handle,
                "output_directory": packet_output_directory,
                "data_root": data_root,
                "decision_question": f"IG daily heartbeat grid capture for @{entry.normalized_handle}",
                "max_rows": max_rows,
                "timeout_seconds": timeout_seconds,
                "settle_seconds": settle_seconds,
                "viewport_width": viewport_width,
                "viewport_height": viewport_height,
                "max_response_bytes": max_response_bytes,
                "block_heavy_assets": block_heavy_assets,
                "session_id": attempt_id,
                "warnings": (
                    f"heartbeat_policy_version:{BEHAVIOR_POLICY_VERSION}",
                    f"heartbeat_controller_version:{CONTROLLER_VERSION}",
                ),
                "limitations": tuple(entry.limitations) + tuple(roster.limitations),
            }
            exit_code, message = grid_runner(**kwargs)
            if exit_code == 0:
                packet_pointer = message
                packet_summary = _read_packet_summary(Path(message))
    except Exception as exc:  # noqa: BLE001 - receipt must preserve visible failure
        exit_code = None
        message = str(exc)
        error_class = type(exc).__name__

    finished_at = now_func()
    normal_e2e_ms = int(round((monotonic_func() - started_monotonic) * 1000))
    status = _receipt_status(exit_code=exit_code, message=message, error_class=error_class)
    # access_gap_reason explains an access gap only. On a succeeded or failed run it must
    # stay None; otherwise a trigger substring in the success message (the packet path or
    # handle can contain "blocked"/"login"/etc.) would fabricate a gap signal and corrupt
    # access-gap telemetry.
    access_gap_reason = (
        _access_gap_reason(exit_code=exit_code, message=message, error_class=error_class)
        if status == "access_gap"
        else None
    )
    candidates = [candidate.to_receipt_dict() for candidate in breakout_candidates]

    receipt: dict[str, Any] = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "run_id": run_id,
        "controller_version": CONTROLLER_VERSION,
        "behavior_policy_version": BEHAVIOR_POLICY_VERSION,
        "roster_snapshot_id": roster.snapshot_id,
        "roster_snapshot_sha256": roster.source_sha256,
        "roster_source_kind": roster.source_kind,
        "sequence": sequence,
        "lane_id": lane_id,
        "lane_count": lane_count,
        "partition_algorithm_version": PARTITION_ALGORITHM_VERSION,
        "attempt_id": attempt_id,
        "partition_key": entry.stable_partition_key,
        "partition_key_source": entry.partition_key_source,
        "assigned_lane_id": assign_lane_id(entry.stable_partition_key, lane_count),
        "creator": {
            "platform": "instagram",
            "handle": entry.normalized_handle,
            "ig_roster_record_id": entry.ig_roster_record_id,
            "platform_account_id": entry.platform_account_id,
            "platform_public_account_id": entry.platform_public_account_id,
            "creator_record_id": entry.creator_record_id,
            "roster_status": entry.roster_status,
        },
        "target_url": entry.reels_url,
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "normal_e2e_ms": normal_e2e_ms,
        "owner_attention_wait_ms": 0,
        "status": status,
        "grid_runner_exit_code": exit_code,
        "grid_runner_message": message,
        "packet_pointer": packet_pointer,
        "packet_id": packet_summary.fields.get("packet_id"),
        "reconciled_existing_packet": reconciled,
        "access_gap_reason": access_gap_reason,
        "source_surface": SOURCE_SURFACE,
        "heartbeat_source_surface": SOURCE_SURFACE_HEARTBEAT,
        "grid_scope": GRID_SCOPE,
        "pagination_attempted": False,
        "scroll_expansion_attempted": False,
        "platform_write_actions_attempted": False,
        "asset_policy": _asset_policy(block_heavy_assets),
        "block_heavy_assets": block_heavy_assets,
        "headless": True,
        "browser_backend": "grid_runner_default_playwright",
        "viewport": {"width": viewport_width, "height": viewport_height},
        "deep_capture_selection": "breakout_candidate_selected" if candidates else "no_candidate",
        "deep_capture_candidates": candidates,
    }
    if error_class:
        receipt["error_class"] = error_class
    for key, value in packet_summary.fields.items():
        receipt[key] = value
    limitations = tuple(entry.limitations) + tuple(roster.limitations) + packet_summary.limitations
    if limitations:
        receipt["limitations"] = list(dict.fromkeys(limitations))
    if packet_summary.warnings:
        receipt["warnings"] = list(packet_summary.warnings)
    return receipt


def _extract_roster_rows(data: object, *, path: Path) -> tuple[str, str, Sequence[object], list[str]]:
    if isinstance(data, list):
        return "ig_active_roster_list", path.stem, data, []
    if not isinstance(data, dict):
        raise ValueError("roster JSON must be an object or list")

    if isinstance(data.get("creator_registry_index"), dict):
        index = data["creator_registry_index"]
        rows = index.get("platform_accounts")
        if not isinstance(rows, list):
            raise ValueError("creator_registry_index.platform_accounts must be a list")
        snapshot_id = _optional_string(index.get("index_id")) or path.stem
        return (
            "creator_registry_index_pilot",
            snapshot_id,
            rows,
            ["creator_registry_index_used_as_pilot_roster_no_active_monitoring_state"],
        )

    for key in ("creators", "roster", "records", "platform_accounts"):
        rows = data.get(key)
        if isinstance(rows, list):
            snapshot_id = (
                _optional_string(data.get("roster_snapshot_id"))
                or _optional_string(data.get("snapshot_id"))
                or _optional_string(data.get("index_id"))
                or path.stem
            )
            return "ig_active_roster_snapshot", snapshot_id, rows, []

    raise ValueError("roster JSON must contain creators, roster, records, platform_accounts, or creator_registry_index")


def _entry_from_row(row: Mapping[str, Any], *, index: int, source_kind: str) -> HeartbeatRosterEntry | None:
    platform = _first_string(row, ("platform", "platform_name"))
    if platform is not None and platform.lower() != "instagram":
        return None

    raw_handle = _first_string(
        row,
        ("public_handle", "normalized_public_handle", "handle", "ig_handle", "instagram_handle", "username"),
    )
    public_profile_url = _first_string(row, ("public_profile_url", "profile_url", "url"))
    if raw_handle is None and public_profile_url is not None:
        raw_handle = _handle_from_instagram_url(public_profile_url)
    if raw_handle is None:
        raise ValueError(f"instagram roster row {index} is missing a public handle")

    limitations: list[str] = []
    roster_status = _first_string(
        row,
        ("heartbeat_status", "monitoring_status", "roster_status", "status"),
    )
    if roster_status is None:
        if source_kind == "creator_registry_index_pilot":
            roster_status = "active_pilot_from_registry_known_account"
            limitations.append("no_active_roster_state_on_creator_registry_row")
        else:
            roster_status = "active_status_unspecified"
            limitations.append("no_active_roster_state_on_roster_row")

    platform_account_id = _first_string(row, ("platform_account_id", "ig_platform_account_id"))
    platform_public_account_id = _first_string(
        row,
        ("platform_public_account_id", "platform_public_account_id_or_none", "instagram_user_id", "numeric_id"),
    )
    creator_record_id = _first_string(row, ("creator_record_id", "creator_record_id_or_none"))
    ig_roster_record_id = _first_string(row, ("ig_roster_record_id", "roster_record_id"))
    normalized_handle = normalize_handle(raw_handle)
    stable_partition_key = _first_string(row, ("stable_partition_key",))
    partition_key_source = _first_string(row, ("partition_key_source",))
    if stable_partition_key is None:
        stable_partition_key, partition_key_source = _stable_partition_key(
            ig_roster_record_id=ig_roster_record_id,
            platform_account_id=platform_account_id,
            platform_public_account_id=platform_public_account_id,
            handle=normalized_handle,
            limitations=limitations,
        )
    elif partition_key_source is None:
        raise ValueError(f"instagram roster row {index} has stable_partition_key without partition_key_source")

    return HeartbeatRosterEntry(
        handle=normalized_handle,
        platform_account_id=platform_account_id,
        platform_public_account_id=platform_public_account_id,
        creator_record_id=creator_record_id,
        ig_roster_record_id=ig_roster_record_id,
        public_profile_url=public_profile_url,
        roster_status=roster_status,
        stable_partition_key=stable_partition_key,
        partition_key_source=partition_key_source,
        attempt_id=_first_string(row, ("attempt_id",)),
        attempt_resume=row.get("attempt_resume") is True,
        limitations=tuple(limitations),
    )


def _stable_partition_key(
    *,
    ig_roster_record_id: str | None,
    platform_account_id: str | None,
    platform_public_account_id: str | None,
    handle: str,
    limitations: list[str],
) -> tuple[str, str]:
    if ig_roster_record_id:
        return f"ig_roster_record_id:{ig_roster_record_id}", "ig_roster_record_id"
    if platform_account_id:
        return f"platform_account_id:{platform_account_id}", "platform_account_id"
    if platform_public_account_id:
        return f"platform_public_account_id:{platform_public_account_id}", "platform_public_account_id"
    limitations.append("partition_key_handle_fallback_handle_mutable")
    return f"instagram_handle:{handle.lower()}", "normalized_handle_fallback"


def _is_active_status(status: str) -> bool:
    normalized = status.strip().lower()
    if normalized in {"paused", "parked", "removed", "inactive", "disabled", "blocked"}:
        return False
    return normalized == "active" or normalized.startswith("active_")


def _load_breakout_records(path: Path) -> list[object]:
    text = path.read_text(encoding="utf-8")
    stripped = text.strip()
    if not stripped:
        return []
    if stripped.startswith("[") or stripped.startswith("{"):
        data = json.loads(stripped)
        if isinstance(data, list):
            return list(data)
        if isinstance(data, dict):
            for key in ("breakout_candidates", "candidates", "items", "records"):
                value = data.get(key)
                if isinstance(value, list):
                    return list(value)
        raise ValueError("breakout candidates JSON must be a list or contain a candidate list")
    records: list[object] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"breakout candidates JSONL line {line_no} is invalid: {exc}") from exc
    return records


def _packet_output_directory(
    *,
    output_root: Path | None,
    run_id: str,
    lane_id: str,
    sequence: int,
    handle: str,
    attempt_id: str,
) -> Path | None:
    if output_root is None:
        return None
    return output_root / "heartbeat_attempts" / attempt_id / _safe_path_segment(handle)


def _find_existing_attempt_packet(
    *, output_directory: Path | None, data_root: object | None, attempt_id: str
) -> Path | None:
    if data_root is not None:
        found = find_committed_packet_by_session_identity(
            data_root,
            session_identity=attempt_id,
            source_surface=SOURCE_SURFACE,
        )
        return found[1] if found is not None else None
    if output_directory is None or not (output_directory / "manifest.json").is_file():
        return None
    try:
        manifest = json.loads((output_directory / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(manifest, dict) or manifest.get("session_identity") != attempt_id:
        return None
    return output_directory


def _safe_path_segment(value: str) -> str:
    safe = "".join(char if char.isalnum() or char in {"-", "_", "."} else "_" for char in value)
    return safe.strip("._") or "creator"


def _receipt_status(*, exit_code: int | None, message: str, error_class: str | None) -> str:
    if error_class is not None:
        return "failed"
    if exit_code == 0:
        return "succeeded"
    if _access_gap_reason(exit_code=exit_code, message=message, error_class=error_class) is not None:
        return "access_gap"
    return "failed"


def _access_gap_reason(*, exit_code: int | None, message: str, error_class: str | None) -> str | None:
    if error_class is not None:
        return None
    lowered = message.lower()
    if exit_code == 5:
        return _extract_parenthetical_reason(message) or "profile_access_blocked"
    if any(token in lowered for token in ("login", "challenge", "captcha", "rate_limited", "blocked")):
        return "grid_runner_reported_access_gap"
    return None


def _extract_parenthetical_reason(message: str) -> str | None:
    start = message.find("(")
    end = message.find(")", start + 1)
    if start == -1 or end == -1:
        return None
    reason = message[start + 1 : end].strip()
    return reason or None


def _asset_policy(block_heavy_assets: bool) -> str:
    return "heavy_assets_blocked_bandwidth_mode" if block_heavy_assets else "browser_default_assets"


def _read_packet_summary(packet_dir: Path) -> _PacketSummary:
    manifest_path = packet_dir / "manifest.json"
    if not manifest_path.is_file():
        return _PacketSummary(limitations=("packet_manifest_missing_for_receipt_summary",))
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return _PacketSummary(limitations=(f"packet_manifest_unreadable_for_receipt_summary:{type(exc).__name__}",))
    if not isinstance(manifest, dict):
        return _PacketSummary(limitations=("packet_manifest_not_object_for_receipt_summary",))

    fields: dict[str, Any] = {}
    source_slices = manifest.get("source_slices")
    if isinstance(source_slices, list):
        media_slices = [
            item
            for item in source_slices
            if isinstance(item, dict) and str(item.get("slice_id", "")).startswith("ig_reels_grid_")
        ]
        fields["row_counts"] = {"grid_media_slices": len(media_slices)}
        metric_counts: dict[str, int] = {}
        for source_slice in media_slices:
            observations = source_slice.get("metric_observations")
            if not isinstance(observations, list):
                continue
            for observation in observations:
                if not isinstance(observation, dict):
                    continue
                if observation.get("posture") != "observed" or observation.get("value") is None:
                    continue
                metric = _optional_string(observation.get("metric"))
                if metric is not None:
                    metric_counts[metric] = metric_counts.get(metric, 0) + 1
        if metric_counts:
            fields["metric_observation_counts"] = metric_counts
    packet_id = _optional_string(manifest.get("packet_id"))
    if packet_id is not None:
        fields["packet_id"] = packet_id
    surface = _optional_string(manifest.get("source_surface"))
    if surface is not None:
        fields["packet_source_surface"] = surface

    warnings = _string_list(manifest.get("warnings"))
    limitations = _string_list(manifest.get("limitations"))
    return _PacketSummary(fields=fields, warnings=tuple(warnings), limitations=tuple(limitations))


def _validate_lane_id(*, lane_id: str, lane_count: int) -> None:
    if lane_count < 1:
        raise ValueError("lane_count must be at least 1")
    expected = {f"lane_{index}" for index in range(1, lane_count + 1)}
    if lane_id not in expected:
        raise ValueError(f"lane_id must be one of: {', '.join(sorted(expected))}")


def _handle_from_instagram_url(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.netloc.lower() not in {"instagram.com", "www.instagram.com"}:
        return None
    parts = [part for part in parsed.path.split("/") if part]
    return parts[0] if parts else None


def _append_jsonl(path: Path, payload: Mapping[str, Any]) -> None:
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        handle.write("\n")


def _first_string(row: Mapping[str, Any], keys: Sequence[str]) -> str | None:
    for key in keys:
        value = _optional_string(row.get(key))
        if value is not None:
            return value
    return None


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, int):
        return str(value)
    return None


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in (_optional_string(raw) for raw in value) if item is not None]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run one lane of IG daily heartbeat grid captures over an active roster snapshot."
    )
    parser.add_argument("--roster", type=Path, required=True)
    parser.add_argument("--receipt-jsonl", type=Path, required=True)
    parser.add_argument("--lane-id", required=True, help="One-based lane id, e.g. lane_1.")
    parser.add_argument("--lane-count", type=int, required=True)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--output-root", type=Path, default=None)
    target.add_argument(
        "--data-root",
        default=None,
        help="Commit grid packets into a Forseti data root instead of a local output bundle.",
    )
    parser.add_argument("--breakout-candidates", type=Path, default=None)
    parser.add_argument("--max-creators", type=int, default=None)
    parser.add_argument("--time-budget-seconds", type=float, default=None)
    parser.add_argument("--max-rows", type=int, default=DEFAULT_MAX_ROWS)
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_IG_REELS_TIMEOUT_SECONDS)
    parser.add_argument("--settle-seconds", type=float, default=DEFAULT_IG_REELS_SETTLE_SECONDS)
    parser.add_argument("--viewport-width", type=int, default=DEFAULT_IG_REELS_VIEWPORT_WIDTH)
    parser.add_argument("--viewport-height", type=int, default=DEFAULT_IG_REELS_VIEWPORT_HEIGHT)
    parser.add_argument("--max-response-bytes", type=int, default=DEFAULT_IG_REELS_MAX_RESPONSE_BYTES)
    parser.add_argument(
        "--allow-heavy-assets",
        action="store_true",
        help="Pass browser-default asset loading through to the grid primitive. Default records bandwidth mode.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        data_root = None
        if args.data_root is not None:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)
        result = run_ig_daily_heartbeat(
            roster_path=args.roster,
            receipt_jsonl=args.receipt_jsonl,
            lane_id=args.lane_id,
            lane_count=args.lane_count,
            output_root=args.output_root,
            data_root=data_root,
            breakout_candidates_path=args.breakout_candidates,
            max_creators=args.max_creators,
            time_budget_seconds=args.time_budget_seconds,
            max_rows=args.max_rows,
            timeout_seconds=args.timeout_seconds,
            settle_seconds=args.settle_seconds,
            viewport_width=args.viewport_width,
            viewport_height=args.viewport_height,
            max_response_bytes=args.max_response_bytes,
            block_heavy_assets=not args.allow_heavy_assets,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"ig daily heartbeat failed: {exc}\n")
    except Exception as exc:  # noqa: BLE001 - preserve visible controller failures
        parser.exit(status=3, message=f"ig daily heartbeat failed: {type(exc).__name__}: {exc}\n")

    print(result.message())
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
