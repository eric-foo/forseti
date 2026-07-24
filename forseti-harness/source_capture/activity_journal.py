"""Append-only, sanitized activity timing journal for source-capture runs."""

from __future__ import annotations

import json
import os
import re
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable, Mapping, Sequence
from uuid import uuid4


SOURCE_CAPTURE_ACTIVITY_SCHEMA_VERSION = "source_capture_activity_v1"
SOURCE_CAPTURE_ACTIVITY_JSONL_NAME = "source_capture_activity.jsonl"

MonotonicFn = Callable[[], float]
UtcNowFn = Callable[[], datetime]

_COMMON_KEYS = frozenset(
    {
        "schema_version",
        "run_id",
        "sequence",
        "observed_at_utc",
        "elapsed_seconds",
        "event_type",
    }
)
_EVENT_KEYS = {
    "run_started": frozenset({"run_kind", "platform"}),
    "phase": frozenset({"phase_name", "details"}),
    "browser_capture_started": frozenset(
        {"capture_index", "action_names", "settle_seconds", "reload_requested"}
    ),
    "browser_capture_finished": frozenset(
        {
            "capture_index",
            "outcome",
            "capture_elapsed_seconds",
            "action_names",
            "context_observations",
            "pointer_outcomes",
            "wheel_outcome_or_none",
            "error_type_or_none",
        }
    ),
    "cadence_wait_started": frozenset(
        {"wait_kind", "policy", "planned_seconds", "plan"}
    ),
    "cadence_wait_finished": frozenset(
        {"wait_kind", "planned_seconds", "actual_seconds"}
    ),
    "terminal": frozenset({"status", "terminal_phase", "error_type_or_none"}),
}
_FORBIDDEN_KEY_PARTS = (
    "url",
    "body",
    "cookie",
    "token",
    "storage",
    "text",
    "html",
    "dom",
)


class SourceCaptureActivityJournal:
    """Write one durable JSON object per diagnostic event.

    The journal is diagnostic only. It deliberately contains no checkpoint or
    resume state, and creating it refuses to append to an existing run.
    """

    def __init__(
        self,
        path: str | Path,
        *,
        run_kind: str,
        platform: str,
        monotonic_fn: MonotonicFn = time.monotonic,
        utc_now_fn: UtcNowFn = lambda: datetime.now(UTC),
    ) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._stream = self.path.open("xb")
        self._monotonic_fn = monotonic_fn
        self._utc_now_fn = utc_now_fn
        self._started_monotonic = monotonic_fn()
        self._run_id = uuid4().hex
        self._sequence = 0
        self._closed = False
        self.record("run_started", run_kind=run_kind, platform=platform)

    def record(self, event_type: str, **fields: object) -> None:
        if self._closed:
            raise RuntimeError("source-capture activity journal is already closed")
        row = {
            "schema_version": SOURCE_CAPTURE_ACTIVITY_SCHEMA_VERSION,
            "run_id": self._run_id,
            "sequence": self._sequence,
            "observed_at_utc": _utc_iso(self._utc_now_fn()),
            "elapsed_seconds": round(
                max(0.0, self._monotonic_fn() - self._started_monotonic), 6
            ),
            "event_type": event_type,
            **fields,
        }
        _validate_activity_row(row)
        encoded = (
            json.dumps(
                row,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
            + b"\n"
        )
        self._stream.write(encoded)
        self._stream.flush()
        os.fsync(self._stream.fileno())
        self._sequence += 1

    def close(
        self,
        *,
        status: str,
        terminal_phase: str,
        error_type_or_none: str | None,
    ) -> None:
        if self._closed:
            return
        try:
            self.record(
                "terminal",
                status=status,
                terminal_phase=terminal_phase,
                error_type_or_none=error_type_or_none,
            )
        finally:
            self._stream.close()
            self._closed = True


def validate_source_capture_activity_jsonl(raw: bytes) -> list[dict[str, object]]:
    """Validate exact journal bytes before durable packet attachment."""

    if not raw:
        raise ValueError("source-capture activity journal must not be empty")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("source-capture activity journal must be UTF-8") from exc
    if not text.endswith("\n"):
        raise ValueError("source-capture activity journal must end with a newline")
    rows: list[dict[str, object]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"source-capture activity journal line {line_number} is invalid JSON"
            ) from exc
        if not isinstance(row, dict):
            raise ValueError(
                f"source-capture activity journal line {line_number} must be an object"
            )
        _validate_activity_row(row)
        rows.append(row)
    if not rows or rows[0]["event_type"] != "run_started":
        raise ValueError("source-capture activity journal must start with run_started")
    if rows[-1]["event_type"] != "terminal":
        raise ValueError("source-capture activity journal must end with terminal")
    run_ids = {row["run_id"] for row in rows}
    if len(run_ids) != 1:
        raise ValueError("source-capture activity journal must contain one run_id")
    if [row["sequence"] for row in rows] != list(range(len(rows))):
        raise ValueError(
            "source-capture activity journal sequence must be contiguous from zero"
        )
    return rows


def _validate_activity_row(row: Mapping[str, object]) -> None:
    event_type = row.get("event_type")
    if not isinstance(event_type, str) or event_type not in _EVENT_KEYS:
        raise ValueError("source-capture activity event_type is invalid")
    allowed = _COMMON_KEYS | _EVENT_KEYS[event_type]
    unexpected = sorted(set(row) - allowed)
    if unexpected:
        raise ValueError(
            "source-capture activity event contains unsupported fields: "
            + ", ".join(unexpected)
        )
    missing = sorted((_COMMON_KEYS | _EVENT_KEYS[event_type]) - set(row))
    if missing:
        raise ValueError(
            "source-capture activity event is missing required fields: "
            + ", ".join(missing)
        )
    if row.get("schema_version") != SOURCE_CAPTURE_ACTIVITY_SCHEMA_VERSION:
        raise ValueError("source-capture activity schema_version is invalid")
    if not isinstance(row.get("run_id"), str) or not row["run_id"]:
        raise ValueError("source-capture activity run_id is required")
    sequence = row.get("sequence")
    if isinstance(sequence, bool) or not isinstance(sequence, int) or sequence < 0:
        raise ValueError("source-capture activity sequence must be non-negative")
    observed_at_utc = row.get("observed_at_utc")
    if not isinstance(observed_at_utc, str):
        raise ValueError("source-capture activity observed_at_utc is required")
    try:
        observed_at = datetime.fromisoformat(
            observed_at_utc.replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise ValueError(
            "source-capture activity observed_at_utc must be ISO-8601"
        ) from exc
    if observed_at.tzinfo is None:
        raise ValueError(
            "source-capture activity observed_at_utc must be timezone-aware"
        )
    elapsed = row.get("elapsed_seconds")
    if isinstance(elapsed, bool) or not isinstance(elapsed, (int, float)) or elapsed < 0:
        raise ValueError("source-capture activity elapsed_seconds must be non-negative")
    _validate_event_fields(event_type, row)
    _reject_forbidden_material(row)
    json.dumps(row, ensure_ascii=False, allow_nan=False)


def _validate_event_fields(
    event_type: str, row: Mapping[str, object]
) -> None:
    if event_type == "run_started":
        _require_strings(row, "run_kind", "platform")
    elif event_type == "phase":
        _require_strings(row, "phase_name")
        if not isinstance(row.get("details"), Mapping):
            raise ValueError("source-capture activity phase details must be an object")
    elif event_type == "browser_capture_started":
        _require_non_negative_int(row, "capture_index")
        _require_string_list(row, "action_names")
        _require_non_negative_number(row, "settle_seconds")
        if not isinstance(row.get("reload_requested"), bool):
            raise ValueError(
                "source-capture activity reload_requested must be boolean"
            )
    elif event_type == "browser_capture_finished":
        _require_non_negative_int(row, "capture_index")
        _require_strings(row, "outcome")
        _require_non_negative_number(row, "capture_elapsed_seconds")
        _require_string_list(row, "action_names")
        for field in ("context_observations", "pointer_outcomes"):
            value = row.get(field)
            if not isinstance(value, list) or not all(
                isinstance(item, Mapping) for item in value
            ):
                raise ValueError(
                    f"source-capture activity {field} must be a list of objects"
                )
        wheel = row.get("wheel_outcome_or_none")
        if wheel is not None and not isinstance(wheel, Mapping):
            raise ValueError(
                "source-capture activity wheel_outcome_or_none must be an object or null"
            )
        error_type = row.get("error_type_or_none")
        if error_type is not None and not isinstance(error_type, str):
            raise ValueError(
                "source-capture activity error_type_or_none must be a string or null"
            )
    elif event_type == "cadence_wait_started":
        _require_strings(row, "wait_kind", "policy")
        _require_non_negative_number(row, "planned_seconds")
        if not isinstance(row.get("plan"), Mapping):
            raise ValueError("source-capture activity cadence plan must be an object")
    elif event_type == "cadence_wait_finished":
        _require_strings(row, "wait_kind")
        _require_non_negative_number(row, "planned_seconds")
        _require_non_negative_number(row, "actual_seconds")
    elif event_type == "terminal":
        _require_strings(row, "status", "terminal_phase")
        error_type = row.get("error_type_or_none")
        if error_type is not None and not isinstance(error_type, str):
            raise ValueError(
                "source-capture activity error_type_or_none must be a string or null"
            )


def _require_strings(row: Mapping[str, object], *fields: str) -> None:
    for field in fields:
        if not isinstance(row.get(field), str) or not row[field]:
            raise ValueError(
                f"source-capture activity {field} must be a non-empty string"
            )


def _require_string_list(row: Mapping[str, object], field: str) -> None:
    value = row.get(field)
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise ValueError(
            f"source-capture activity {field} must be a list of non-empty strings"
        )


def _require_non_negative_int(
    row: Mapping[str, object], field: str
) -> None:
    value = row.get(field)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(
            f"source-capture activity {field} must be a non-negative integer"
        )


def _require_non_negative_number(
    row: Mapping[str, object], field: str
) -> None:
    value = row.get(field)
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or value < 0
    ):
        raise ValueError(
            f"source-capture activity {field} must be non-negative"
        )


def _reject_forbidden_material(value: object, *, key: str | None = None) -> None:
    if key is not None:
        tokens = {
            token
            for token in re.split(r"[^a-z0-9]+", key.lower())
            if token
        }
        if tokens.intersection(_FORBIDDEN_KEY_PARTS):
            raise ValueError(
                f"source-capture activity field is forbidden: {key}"
            )
    if isinstance(value, Mapping):
        for child_key, child_value in value.items():
            if not isinstance(child_key, str):
                raise ValueError("source-capture activity keys must be strings")
            _reject_forbidden_material(child_value, key=child_key)
        return
    if isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    ):
        for child in value:
            _reject_forbidden_material(child)
        return
    if isinstance(value, str):
        lowered = value.lower()
        if "://" in lowered or "<html" in lowered or "document.cookie" in lowered:
            raise ValueError("source-capture activity value contains forbidden material")


def _utc_iso(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")
