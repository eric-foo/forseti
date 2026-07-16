"""Fail-closed validation for one commissioned scan-to-Capture lifecycle."""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
import re
from typing import Any

from pydantic import ValidationError

from data_lake.root import DataLakeRoot, DataLakeRootError
from harness_utils import hash_file
from source_capture.models import SourceCapturePacket


CAPTURE_REQUEST_LIFECYCLE_SCHEMA_VERSION = "capture_request_lifecycle_v0"
_TERMINAL_STATES = frozenset({"handoff_ready", "declined"})
_TRANSITIONS = {
    None: frozenset({"requested"}),
    "requested": frozenset({"route_bound", "declined"}),
    "route_bound": frozenset({"captured", "declined"}),
    "captured": frozenset({"handoff_ready", "declined"}),
    "handoff_ready": frozenset(),
    "declined": frozenset(),
}
_TOKEN = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_LEDGER_KEYS = frozenset(
    {"schema_version", "commission_id", "subject", "source_scan", "requests", "events", "cost_yield"}
)
_REQUEST_KEYS = frozenset(
    {"request_id", "source_family", "venue", "urls", "demand_origin_eligible"}
)
_EVENT_KEYS = frozenset(
    {
        "event_id",
        "request_id",
        "state",
        "observed_at",
        "evidence_refs",
        "reason_or_none",
        "mode_ladder_receipt_or_none",
        "packet_id_or_none",
        "manifest_sha256_or_none",
    }
)
_COST_KEYS = frozenset(
    {
        "stage_id",
        "stage_type",
        "request_id_or_none",
        "source_family_or_none",
        "wall_clock_seconds",
        "token_cost_posture",
        "token_count_or_none",
        "token_unknown_reason_or_none",
        "venues_touched",
        "requests_emitted",
        "requests_fulfilled",
        "requests_declined",
        "packets_handoff_ready",
    }
)
_COUNT_FIELDS = (
    "venues_touched",
    "requests_emitted",
    "requests_fulfilled",
    "requests_declined",
    "packets_handoff_ready",
)


class CaptureRequestLifecycleError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def validate_capture_request_lifecycle(
    ledger: Mapping[str, Any],
    *,
    require_terminal: bool = True,
    require_p0: bool = False,
    data_root: DataLakeRoot | None = None,
    require_packet_verification: bool = False,
) -> None:
    """Validate structure, transitions, closeout truth, cost rows, and optional packet evidence."""
    if not isinstance(ledger, Mapping):
        _fail("invalid_ledger", "lifecycle ledger must be a mapping")
    _reject_unknown(ledger, _LEDGER_KEYS, "ledger")
    _require_keys(ledger, _LEDGER_KEYS, "ledger")
    if ledger.get("schema_version") != CAPTURE_REQUEST_LIFECYCLE_SCHEMA_VERSION:
        _fail("invalid_schema_version", "unexpected lifecycle schema_version")
    for name in ("commission_id", "subject", "source_scan"):
        _require_string(ledger.get(name), name)

    requests = _as_list(ledger.get("requests"), "requests", nonempty=True)
    request_by_id: dict[str, Mapping[str, Any]] = {}
    for index, request in enumerate(requests):
        label = f"requests[{index}]"
        if not isinstance(request, Mapping):
            _fail("invalid_request", f"{label} must be a mapping")
        _reject_unknown(request, _REQUEST_KEYS, label)
        _require_keys(request, _REQUEST_KEYS, label)
        request_id = _require_token(request.get("request_id"), f"{label}.request_id")
        if request_id in request_by_id:
            _fail("duplicate_request_id", f"duplicate request_id: {request_id}")
        _require_token(request.get("source_family"), f"{label}.source_family")
        _require_string(request.get("venue"), f"{label}.venue")
        urls = _as_list(request.get("urls"), f"{label}.urls", nonempty=True)
        if any(not isinstance(url, str) or not re.match(r"^https?://", url) for url in urls):
            _fail("invalid_request_url", f"{label}.urls must contain public http(s) URLs")
        if type(request.get("demand_origin_eligible")) is not bool:
            _fail("invalid_demand_origin_eligibility", f"{label}.demand_origin_eligible must be boolean")
        request_by_id[request_id] = request

    events = _as_list(ledger.get("events"), "events", nonempty=True)
    current: dict[str, str] = {}
    captured_packet: dict[str, str] = {}
    handoff_event: dict[str, Mapping[str, Any]] = {}
    event_ids: set[str] = set()
    last_observed_at: datetime | None = None
    for index, event in enumerate(events):
        label = f"events[{index}]"
        if not isinstance(event, Mapping):
            _fail("invalid_event", f"{label} must be a mapping")
        _reject_unknown(event, _EVENT_KEYS, label)
        _require_keys(event, _EVENT_KEYS, label)
        event_id = _require_token(event.get("event_id"), f"{label}.event_id")
        if event_id in event_ids:
            _fail("duplicate_event_id", f"duplicate event_id: {event_id}")
        event_ids.add(event_id)
        request_id = _require_token(event.get("request_id"), f"{label}.request_id")
        if request_id not in request_by_id:
            _fail("unknown_request_id", f"{label} references unknown request_id: {request_id}")
        state = _require_token(event.get("state"), f"{label}.state")
        previous = current.get(request_id)
        if state not in _TRANSITIONS.get(previous, frozenset()):
            _fail("invalid_transition", f"{request_id} cannot transition from {previous!r} to {state!r}")
        observed_at = _require_aware_timestamp(event.get("observed_at"), f"{label}.observed_at")
        if last_observed_at is not None and observed_at < last_observed_at:
            _fail("event_order_regression", "events must be appended in non-decreasing observed_at order")
        last_observed_at = observed_at
        _string_list(event.get("evidence_refs"), f"{label}.evidence_refs", nonempty=True)
        _validate_event_payload(event, state, label)
        packet_id = event.get("packet_id_or_none")
        if state == "captured":
            captured_packet[request_id] = _require_string(packet_id, f"{label}.packet_id_or_none")
        elif state == "handoff_ready":
            packet_id = _require_string(packet_id, f"{label}.packet_id_or_none")
            if captured_packet.get(request_id) != packet_id:
                _fail("handoff_packet_mismatch", f"{request_id} handoff packet differs from captured packet")
            handoff_event[request_id] = event
        current[request_id] = state

    missing_events = sorted(set(request_by_id) - set(current))
    if missing_events:
        _fail("request_without_event", f"requests have no lifecycle events: {missing_events}")
    if require_terminal:
        open_requests = sorted(request_id for request_id, state in current.items() if state not in _TERMINAL_STATES)
        if open_requests:
            _fail("nonterminal_requests", f"requests remain nonterminal: {open_requests}")

    _validate_cost_yield(ledger.get("cost_yield"), request_by_id, current)

    if require_p0:
        families = {
            str(request_by_id[request_id]["source_family"])
            for request_id, state in current.items()
            if state == "handoff_ready" and request_by_id[request_id]["demand_origin_eligible"] is True
        }
        if len(families) < 2:
            _fail("insufficient_independent_origin_families", "P0 requires handoff-ready packets from at least two eligible source families")

    if require_packet_verification and data_root is None:
        _fail("packet_verification_unavailable", "packet verification requires a resolved DataLakeRoot")
    if data_root is not None:
        for request_id, event in handoff_event.items():
            _verify_handoff_packet(data_root, request_id, request_by_id[request_id], event)


def _validate_event_payload(event: Mapping[str, Any], state: str, label: str) -> None:
    reason = event.get("reason_or_none")
    mode_receipt = event.get("mode_ladder_receipt_or_none")
    packet_id = event.get("packet_id_or_none")
    manifest_sha = event.get("manifest_sha256_or_none")
    if state == "declined":
        _require_string(reason, f"{label}.reason_or_none")
        _require_string(mode_receipt, f"{label}.mode_ladder_receipt_or_none")
        if packet_id is not None or manifest_sha is not None:
            _fail("decline_has_packet", f"{label} declined event must not claim packet evidence")
        return
    if reason is not None or mode_receipt is not None:
        _fail("non_decline_has_reason", f"{label} non-declined event must use null decline fields")
    if state in {"requested", "route_bound"}:
        if packet_id is not None or manifest_sha is not None:
            _fail("premature_packet_claim", f"{label} cannot claim a packet before capture")
    elif state == "captured":
        _require_string(packet_id, f"{label}.packet_id_or_none")
        if manifest_sha is not None:
            _fail("premature_handoff_claim", f"{label} captured event must not claim verified manifest hash")
    elif state == "handoff_ready":
        _require_string(packet_id, f"{label}.packet_id_or_none")
        if not isinstance(manifest_sha, str) or _SHA256.fullmatch(manifest_sha) is None:
            _fail("invalid_manifest_sha256", f"{label}.manifest_sha256_or_none must be lowercase sha256")


def _validate_cost_yield(value: Any, requests: Mapping[str, Mapping[str, Any]], states: Mapping[str, str]) -> None:
    rows = _as_list(value, "cost_yield", nonempty=True)
    scan_rows: list[Mapping[str, Any]] = []
    capture_rows: dict[str, Mapping[str, Any]] = {}
    stage_ids: set[str] = set()
    for index, row in enumerate(rows):
        label = f"cost_yield[{index}]"
        if not isinstance(row, Mapping):
            _fail("invalid_cost_yield_row", f"{label} must be a mapping")
        _reject_unknown(row, _COST_KEYS, label)
        _require_keys(row, _COST_KEYS, label)
        stage_id = _require_token(row.get("stage_id"), f"{label}.stage_id")
        if stage_id in stage_ids:
            _fail("duplicate_cost_stage", f"duplicate cost stage_id: {stage_id}")
        stage_ids.add(stage_id)
        stage_type = row.get("stage_type")
        if stage_type not in {"scan", "capture"}:
            _fail("invalid_cost_stage_type", f"{label}.stage_type must be scan or capture")
        elapsed = row.get("wall_clock_seconds")
        if isinstance(elapsed, bool) or not isinstance(elapsed, (int, float)) or elapsed < 0:
            _fail("invalid_wall_clock", f"{label}.wall_clock_seconds must be non-negative")
        for field in _COUNT_FIELDS:
            _nonnegative_int(row.get(field), f"{label}.{field}")
        _validate_token_cost(row, label)
        request_id = row.get("request_id_or_none")
        source_family = row.get("source_family_or_none")
        if stage_type == "scan":
            if request_id is not None or source_family is not None:
                _fail("scan_cost_has_request", f"{label} scan row must use null request/source family")
            scan_rows.append(row)
        else:
            request_id = _require_string(request_id, f"{label}.request_id_or_none")
            if request_id not in requests:
                _fail("unknown_cost_request", f"{label} references unknown request_id: {request_id}")
            if request_id in capture_rows:
                _fail("duplicate_capture_cost", f"multiple capture cost rows for {request_id}")
            if source_family != requests[request_id]["source_family"]:
                _fail("cost_source_family_mismatch", f"{label} source family differs from request")
            capture_rows[request_id] = row
    if len(scan_rows) != 1:
        _fail("scan_cost_row_count", "lifecycle requires exactly one scan cost/yield row")
    missing_capture_rows = sorted(set(requests) - set(capture_rows))
    if missing_capture_rows:
        _fail("missing_capture_cost_rows", f"requests missing capture cost/yield rows: {missing_capture_rows}")
    fulfilled = sum(state == "handoff_ready" for state in states.values())
    declined = sum(state == "declined" for state in states.values())
    scan = scan_rows[0]
    expected_scan = {
        "requests_emitted": len(requests),
        "requests_fulfilled": fulfilled,
        "requests_declined": declined,
        "packets_handoff_ready": fulfilled,
    }
    for field, expected in expected_scan.items():
        if scan[field] != expected:
            _fail("scan_cost_yield_mismatch", f"scan {field} must be {expected}, got {scan[field]}")
    for request_id, row in capture_rows.items():
        terminal = states.get(request_id)
        expected_fulfilled = 1 if terminal == "handoff_ready" else 0
        expected_declined = 1 if terminal == "declined" else 0
        if row["requests_emitted"] != 0 or row["requests_fulfilled"] != expected_fulfilled or row["requests_declined"] != expected_declined or row["packets_handoff_ready"] != expected_fulfilled:
            _fail("capture_cost_yield_mismatch", f"capture cost/yield row does not match terminal state for {request_id}")


def _validate_token_cost(row: Mapping[str, Any], label: str) -> None:
    posture = row.get("token_cost_posture")
    count = row.get("token_count_or_none")
    reason = row.get("token_unknown_reason_or_none")
    if posture == "observed":
        _nonnegative_int(count, f"{label}.token_count_or_none")
        if reason is not None:
            _fail("observed_token_cost_has_reason", f"{label} observed token cost must use null reason")
    elif posture == "unknown_with_reason":
        if count is not None:
            _fail("unknown_token_cost_has_count", f"{label} unknown token cost must use null count")
        _require_string(reason, f"{label}.token_unknown_reason_or_none")
    else:
        _fail("invalid_token_cost_posture", f"{label}.token_cost_posture is invalid")


def _verify_handoff_packet(
    data_root: DataLakeRoot,
    request_id: str,
    request: Mapping[str, Any],
    event: Mapping[str, Any],
) -> None:
    packet_id = str(event["packet_id_or_none"])
    try:
        loaded = data_root.load_raw_packet(packet_id)
        packet = SourceCapturePacket.model_validate(loaded.manifest)
    except (DataLakeRootError, ValidationError, OSError, ValueError) as exc:
        _fail("handoff_packet_invalid", f"{request_id} packet failed schema/hash verification: {exc}")
    if packet.packet_id != packet_id:
        _fail("handoff_packet_id_mismatch", f"{request_id} manifest packet_id does not match lifecycle event")
    if packet.source_family != request["source_family"]:
        _fail("handoff_source_family_mismatch", f"{request_id} packet source_family differs from request")
    locator = packet.source_locator.value
    if locator not in request["urls"]:
        _fail(
            "handoff_source_locator_mismatch",
            f"{request_id} packet source_locator {locator!r} is not a URL this request asked for",
        )
    actual_manifest_sha = hash_file(loaded.container / "manifest.json")
    if actual_manifest_sha != event["manifest_sha256_or_none"]:
        _fail("handoff_manifest_hash_mismatch", f"{request_id} manifest sha256 does not match lifecycle event")


def _require_aware_timestamp(value: Any, label: str) -> datetime:
    text = _require_string(value, label)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        _fail("invalid_timestamp", f"{label} must be ISO-8601: {exc}")
    if parsed.tzinfo is None:
        _fail("naive_timestamp", f"{label} must include a timezone")
    return parsed


def _reject_unknown(value: Mapping[str, Any], allowed: frozenset[str], label: str) -> None:
    unknown = sorted(str(key) for key in value if str(key) not in allowed)
    if unknown:
        _fail("unknown_field", f"{label} contains unknown field(s): {unknown}")


def _require_keys(value: Mapping[str, Any], required: frozenset[str], label: str) -> None:
    missing = sorted(required - set(value))
    if missing:
        _fail("missing_field", f"{label} is missing field(s): {missing}")


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail("invalid_string", f"{label} must be a non-empty string")
    return value


def _require_token(value: Any, label: str) -> str:
    text = _require_string(value, label)
    if _TOKEN.fullmatch(text) is None:
        _fail("invalid_token", f"{label} must be a lowercase stable token")
    return text


def _as_list(value: Any, label: str, *, nonempty: bool) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        _fail("invalid_list", f"{label} must be a list")
    if nonempty and not value:
        _fail("empty_list", f"{label} must not be empty")
    return value


def _string_list(value: Any, label: str, *, nonempty: bool) -> None:
    items = _as_list(value, label, nonempty=nonempty)
    for item in items:
        _require_string(item, label)


def _nonnegative_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        _fail("invalid_count", f"{label} must be a non-negative integer")
    return value


def _fail(code: str, message: str) -> None:
    raise CaptureRequestLifecycleError(code, message)


__all__ = [
    "CAPTURE_REQUEST_LIFECYCLE_SCHEMA_VERSION",
    "CaptureRequestLifecycleError",
    "validate_capture_request_lifecycle",
]
