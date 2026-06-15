"""Operator-triggered demand-durability series runner (capture-spine step 3).

This is the cadence RUNNER that runs a *commissioned* demand-durability proxy series
OVER TIME. It does NOT score, rank, weight, or judge demand (INV-1); it only records
observed facts and their limits. Whether the series shows durable vs hollow demand is
downstream Judgment.

What it is (option A, operator-triggered per slot -- the lowest standing footprint):

- A bounded, Decision-Frame-tied series is declared once (``init``) from a series spec:
  a ``series_id``, a fixed source set (one or more URLs), a declared cadence plan built
  via ``cadence.build_cadence_plan`` (the SAME primitive the step-2 writer uses -- no
  re-invented cadence math), the demand-durability pins/postures, and a Decision-Frame
  reference. The series is bounded to the cadence plan's ``slot_count``.
- Each slot is executed by a SEPARATE operator invocation (``run-slot``), which fetches
  the source(s) NOW by calling the step-2 durability writer
  (``run_source_capture_http_packet``) per URL for that one observation, then records the
  realized ``capture_time`` vs the intended slot time.
- A slot the operator could not (or chose not to) sample is recorded explicitly as
  ``un-observed`` (``mark-gap`` / a failed ``run-slot``). A gap is a visible LIMITATION,
  NEVER "the source did not change" -- absence of an observation is not a no-change fact.

What it is NOT:

- NOT a scheduler/cron/daemon/queue (options B/C were owner-deferred as higher standing
  footprint). The operator triggers each slot; this runner keeps only the minimal on-disk
  series state needed to track slots across those separate invocations.
- NOT an open crawler. The series is tied to a Decision Frame + fixed source set
  (obligation contract Ob.1 commissioning gate) and bounded to ``slot_count``.
- NOT series-diff / change-detection (Element 3, deferred). This runner records the
  observation packets + realized timings + gaps only; comparing extracted values across
  observations is a separate follow-on.

Series state on disk (smallest-complete; no DB):

    <series_dir>/
        series_index.json     # the spec + per-slot records (intended vs realized, status)
        obs_000/, obs_001/...  # one subdir per (slot, url) observation = a SourceCapturePacket

Each slot record is one of:
    {"status": "pending"}                                   # not yet sampled
    {"status": "observed", realized timings + packet paths} # sampled; capture_time recorded
    {"status": "un_observed", "gap_reason": ...}            # gap: visible limitation, not no-change
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.cadence import build_cadence_plan
from runners.run_source_capture_http_packet import main as run_http_packet_main


SERIES_INDEX_FILENAME = "series_index.json"
SERIES_INDEX_VERSION = "demand_durability_series_index_v0"

# Slot status vocabulary. ``un_observed`` is deliberately distinct from any "no change"
# notion: a gap is a visible limitation, never a no-change fact (the load-bearing
# gap != no-change invariant).
SLOT_PENDING = "pending"
SLOT_OBSERVED = "observed"
SLOT_UN_OBSERVED = "un_observed"

SERIES_RUNNER_NON_CLAIMS = [
    "not a scheduler, cron, daemon, or queue (operator triggers each slot)",
    "not an open crawler (commissioned, Decision-Frame-bound, slot-count-bounded series)",
    "not series-diff or change-detection (Element 3 deferred)",
    "not a demand verdict, score, rank, weight, or threshold (INV-1)",
    "not a durable-vs-hollow judgment",
    "a gap is recorded as un-observed, never as no-change",
]


def _utc_now_z() -> str:
    """Current UTC instant in the ISO-8601 ``...Z`` form used across the capture envelope."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_z(timestamp: str) -> datetime:
    """Parse an ISO-8601 ``...Z`` (or offset) timestamp to an aware UTC datetime."""
    parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


@dataclass(frozen=True)
class DurabilityPins:
    """The Element-1 pins + Element-2 series-origin postures held fixed across the series.

    Each is a raw operator string (a known value) or ``None`` (the writer records an honest
    gap). A future caller that needs unknown/not-applicable reasons can extend the spec; the
    runner forwards whatever is present to the step-2 writer's flags verbatim. These are
    observed facts, never weights (INV-1).
    """

    session_visibility_pin: str | None = None
    locale_pin: str | None = None
    currency_pin: str | None = None
    variant_pin: str | None = None
    variant_pin_unknown_reason: str | None = None
    cold_start_at: str | None = None
    pre_coverage_history_posture: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "DurabilityPins":
        known = {field for field in cls.__dataclass_fields__}
        unknown = set(data) - known
        if unknown:
            raise ValueError(f"unknown durability pin keys: {', '.join(sorted(unknown))}")
        return cls(**{key: data[key] for key in data})  # type: ignore[arg-type]

    def to_dict(self) -> dict[str, object]:
        return {key: getattr(self, key) for key in self.__dataclass_fields__ if getattr(self, key) is not None}


def build_series_index(
    *,
    series_id: str,
    urls: Sequence[str],
    decision_frame_ref: str,
    decision_question: str,
    cadence_mode: str,
    slot_count: int,
    delay_seconds: float | None = None,
    window_seconds: float | None = None,
    min_gap_seconds: float | None = None,
    max_gap_seconds: float | None = None,
    random_seed: int | None = None,
    pins: DurabilityPins | None = None,
    anchor_time: str | None = None,
) -> dict[str, object]:
    """Build the series index (spec + empty per-slot records) for a new commissioned series.

    The cadence plan is built with ``cadence.build_cadence_plan`` (the reused primitive); its
    ``planned_offsets_seconds`` define the intended slot times relative to ``anchor_time`` (the
    declared series start; defaults to now). ``slot_count`` bounds the series -- the runner
    refuses to run a slot beyond it (Ob.1: bounded commissioned unit, not an open crawler).
    """
    if not urls:
        raise ValueError("a demand-durability series requires at least one source URL")

    # Ob.1 commissioning gate: a series is a Decision-Frame-bound commissioned unit, so the
    # Decision Frame reference and the decision question must be real (non-empty after strip),
    # never blank/whitespace. This single builder-level check covers both the direct-builder and
    # the CLI `init` path (which constructs the index here). Input validation only (INV-1).
    if not str(decision_frame_ref).strip() or not str(decision_question).strip():
        raise ValueError(
            "a demand-durability series requires a non-empty Decision Frame reference and "
            "decision question (Ob.1)"
        )

    plan = build_cadence_plan(
        slot_count=slot_count,
        mode=cadence_mode,
        delay_seconds=delay_seconds if delay_seconds is not None else 0.0,
        window_seconds=window_seconds,
        min_gap_seconds=min_gap_seconds,
        max_gap_seconds=max_gap_seconds,
        random_seed=random_seed,
    )
    anchor = anchor_time or _utc_now_z()
    anchor_dt = _parse_z(anchor)
    pins = pins or DurabilityPins()

    slots: list[dict[str, object]] = []
    for slot_index, offset in enumerate(plan.planned_offsets_seconds):
        intended_dt = datetime.fromtimestamp(anchor_dt.timestamp() + offset, tz=timezone.utc)
        slots.append(
            {
                "slot_index": slot_index,
                "intended_offset_seconds": offset,
                "intended_slot_time": intended_dt.isoformat(timespec="seconds").replace("+00:00", "Z"),
                "status": SLOT_PENDING,
                "observations": [],
            }
        )

    return {
        "series_index_version": SERIES_INDEX_VERSION,
        "series_id": series_id,
        "decision_frame_ref": decision_frame_ref,
        "decision_question": decision_question,
        "urls": list(urls),
        "anchor_time": anchor,
        "slot_count": slot_count,
        "intended_cadence": plan.to_dict(),
        "durability_pins": pins.to_dict(),
        "slots": slots,
        "non_claims": list(SERIES_RUNNER_NON_CLAIMS),
    }


def _read_index(series_dir: Path) -> dict[str, object]:
    index_path = series_dir / SERIES_INDEX_FILENAME
    if not index_path.exists():
        raise ValueError(f"no series index at {index_path}; run `init` first")
    return json.loads(index_path.read_text(encoding="utf-8"))


def _write_index(series_dir: Path, index: dict[str, object]) -> None:
    (series_dir / SERIES_INDEX_FILENAME).write_text(
        json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _slot_record(index: dict[str, object], slot_index: int) -> dict[str, object]:
    slots = index["slots"]
    if slot_index < 0 or slot_index >= len(slots):
        raise ValueError(
            f"slot {slot_index} is out of bounds for a bounded series with slot_count "
            f"{index['slot_count']} (valid slots: 0..{len(slots) - 1})"
        )
    return slots[slot_index]


def _writer_argv_for_observation(
    *,
    index: dict[str, object],
    url: str,
    output_dir: Path,
    cold_start: bool,
) -> list[str]:
    """Build the step-2 writer's argv for one observation.

    The intended_cadence, pins, and series identity are forwarded to the step-2 writer's
    OWN flags so the writer (not this runner) populates the packet's durability fields --
    no re-implementation of pin/cadence math here. ``cold_start`` gates the Element-2
    series-origin postures onto the first observed slot only.
    """
    cadence = index["intended_cadence"]
    pins = index["durability_pins"]
    argv = [
        "--url",
        url,
        "--decision-question",
        str(index["decision_question"]),
        "--output",
        str(output_dir),
        "--series-id",
        str(index["series_id"]),
        "--intended-cadence-mode",
        str(cadence["mode"]),
        "--intended-cadence-slot-count",
        str(cadence["slot_count"]),
    ]
    if cadence.get("delay_seconds") is not None:
        argv += ["--intended-cadence-delay-seconds", str(cadence["delay_seconds"])]
    if cadence.get("window_seconds") is not None:
        argv += ["--intended-cadence-window-seconds", str(cadence["window_seconds"])]
    if cadence.get("min_gap_seconds") is not None:
        argv += ["--intended-cadence-min-gap-seconds", str(cadence["min_gap_seconds"])]
    if cadence.get("max_gap_seconds") is not None:
        argv += ["--intended-cadence-max-gap-seconds", str(cadence["max_gap_seconds"])]
    if cadence.get("random_seed") is not None:
        argv += ["--intended-cadence-random-seed", str(cadence["random_seed"])]

    if pins.get("session_visibility_pin") is not None:
        argv += ["--session-visibility-pin", str(pins["session_visibility_pin"])]
    if pins.get("locale_pin") is not None:
        argv += ["--locale-pin", str(pins["locale_pin"])]
    if pins.get("currency_pin") is not None:
        argv += ["--currency-pin", str(pins["currency_pin"])]
    if pins.get("variant_pin") is not None:
        argv += ["--variant-pin", str(pins["variant_pin"])]
    elif pins.get("variant_pin_unknown_reason") is not None:
        argv += ["--variant-pin-unknown-reason", str(pins["variant_pin_unknown_reason"])]

    # Element-2 series-origin postures mark the FIRST observed slot only (the cold start).
    if cold_start:
        if pins.get("cold_start_at") is not None:
            argv += ["--cold-start-at", str(pins["cold_start_at"])]
        if pins.get("pre_coverage_history_posture") is not None:
            argv += ["--pre-coverage-history-posture", str(pins["pre_coverage_history_posture"])]
    return argv


def _read_capture_time(packet_dir: Path) -> str | None:
    """Read the realized ``capture_time`` from a written packet's manifest, if present."""
    manifest_path = packet_dir / "manifest.json"
    if not manifest_path.exists():
        return None
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    timing = manifest.get("timing", {})
    capture_time = timing.get("capture_time", {})
    return capture_time.get("value")


def _any_slot_observed(index: dict[str, object]) -> bool:
    return any(slot["status"] == SLOT_OBSERVED for slot in index["slots"])


def run_slot(
    *,
    series_dir: Path,
    slot_index: int,
    writer_main=run_http_packet_main,
    now_z: str | None = None,
) -> tuple[str, dict[str, object]]:
    """Execute one slot NOW: fetch each series URL via the step-2 writer, record realized timings.

    Returns ``(status, slot_record)`` where status is ``observed`` (every URL captured) or
    ``un_observed`` (the slot is recorded as a gap because a fetch failed). A failed fetch is
    NEVER recorded as a no-change fact -- it is an honest un-observed gap (limitation).
    """
    index = _read_index(series_dir)
    slot = _slot_record(index, slot_index)
    # A recorded slot is immutable: only a still-pending slot may be run. Refusing to
    # overwrite an already observed/un_observed slot keeps the durable series record honest
    # (a re-run must not silently clobber a prior observation or gap). State guard only (INV-1).
    if slot["status"] != SLOT_PENDING:
        raise ValueError(
            f"slot {slot_index} is already {slot['status']}; "
            "refusing to overwrite (a recorded slot is immutable)"
        )
    cold_start = not _any_slot_observed(index)
    realized_now = now_z or _utc_now_z()

    observations: list[dict[str, object]] = []
    failures: list[str] = []
    for url_index, url in enumerate(index["urls"]):
        output_dir = series_dir / f"obs_{slot_index:03d}_{url_index:02d}"
        argv = _writer_argv_for_observation(
            index=index, url=url, output_dir=output_dir, cold_start=cold_start
        )
        # The step-2 writer surfaces a fetch/validation failure either as a non-zero return
        # OR as ``SystemExit`` (its CLI ``main`` calls ``parser.exit``). Treat BOTH as a failed
        # observation so the slot is recorded as an un-observed GAP, never silently as no-change.
        try:
            exit_code = writer_main(argv)
        except SystemExit as exc:
            code = exc.code if isinstance(exc.code, int) else 1
            failures.append(f"url[{url_index}] {url}: writer exit {code}")
            continue
        if exit_code != 0:
            failures.append(f"url[{url_index}] {url}: writer exit {exit_code}")
            continue
        capture_time = _read_capture_time(output_dir)
        observation: dict[str, object] = {
            "url": url,
            "packet_dir": output_dir.name,
            "realized_capture_time": capture_time,
        }
        if capture_time is not None:
            observation["lateness_seconds"] = round(
                _parse_z(capture_time).timestamp() - _parse_z(slot["intended_slot_time"]).timestamp(),
                3,
            )
        observations.append(observation)

    if failures:
        # A slot whose fetch(es) failed is an un-observed GAP -- a visible limitation, never a
        # no-change fact. Any partial observations are still recorded, but the slot status is
        # un_observed so downstream readers never mistake an incomplete slot for "no change".
        slot["status"] = SLOT_UN_OBSERVED
        slot["gap_reason"] = "; ".join(failures)
        slot["gap_kind"] = "fetch_failed"
        slot["recorded_at"] = realized_now
        slot["observations"] = observations
        _write_index(series_dir, index)
        return SLOT_UN_OBSERVED, slot

    slot["status"] = SLOT_OBSERVED
    slot["was_cold_start"] = cold_start
    slot["recorded_at"] = realized_now
    slot["observations"] = observations
    _write_index(series_dir, index)
    return SLOT_OBSERVED, slot


def mark_gap(*, series_dir: Path, slot_index: int, reason: str, now_z: str | None = None) -> dict[str, object]:
    """Record a slot the operator did NOT sample as an un-observed gap (a visible limitation).

    This is the explicit "I skipped/could not run this slot" path. The slot is ``un_observed``
    with ``gap_kind=skipped``; it is NEVER "no change."
    """
    index = _read_index(series_dir)
    slot = _slot_record(index, slot_index)
    # A recorded slot is immutable: only a still-pending slot may be marked as a gap. Refusing
    # to overwrite an already observed/un_observed slot keeps the durable series record honest.
    # State guard only (INV-1).
    if slot["status"] != SLOT_PENDING:
        raise ValueError(
            f"slot {slot_index} is already {slot['status']}; "
            "refusing to overwrite (a recorded slot is immutable)"
        )
    slot["status"] = SLOT_UN_OBSERVED
    slot["gap_reason"] = reason
    slot["gap_kind"] = "skipped"
    slot["recorded_at"] = now_z or _utc_now_z()
    _write_index(series_dir, index)
    return slot


def series_status(series_dir: Path) -> dict[str, object]:
    """Summarize the series: counts of pending / observed / un-observed slots (facts only)."""
    index = _read_index(series_dir)
    slots = index["slots"]
    counts = {SLOT_PENDING: 0, SLOT_OBSERVED: 0, SLOT_UN_OBSERVED: 0}
    for slot in slots:
        counts[slot["status"]] = counts.get(slot["status"], 0) + 1
    return {
        "series_id": index["series_id"],
        "decision_frame_ref": index["decision_frame_ref"],
        "slot_count": index["slot_count"],
        "observed": counts[SLOT_OBSERVED],
        "un_observed": counts[SLOT_UN_OBSERVED],
        "pending": counts[SLOT_PENDING],
        "complete": counts[SLOT_PENDING] == 0,
    }


def _cmd_init(args: argparse.Namespace) -> int:
    pins = DurabilityPins(
        session_visibility_pin=args.session_visibility_pin,
        locale_pin=args.locale_pin,
        currency_pin=args.currency_pin,
        variant_pin=args.variant_pin,
        variant_pin_unknown_reason=args.variant_pin_unknown_reason,
        cold_start_at=args.cold_start_at,
        pre_coverage_history_posture=args.pre_coverage_history_posture,
    )
    index = build_series_index(
        series_id=args.series_id,
        urls=args.url,
        decision_frame_ref=args.decision_frame_ref,
        decision_question=args.decision_question,
        cadence_mode=args.cadence_mode,
        slot_count=args.slot_count,
        delay_seconds=args.cadence_delay_seconds,
        window_seconds=args.cadence_window_seconds,
        min_gap_seconds=args.cadence_min_gap_seconds,
        max_gap_seconds=args.cadence_max_gap_seconds,
        random_seed=args.cadence_random_seed,
        pins=pins,
        anchor_time=args.anchor_time,
    )
    series_dir = args.series_dir
    if (series_dir / SERIES_INDEX_FILENAME).exists():
        raise ValueError(f"series already initialized at {series_dir}; refusing to overwrite")
    series_dir.mkdir(parents=True, exist_ok=True)
    _write_index(series_dir, index)
    print(str(series_dir / SERIES_INDEX_FILENAME))
    return 0


def _cmd_run_slot(args: argparse.Namespace) -> int:
    status, _slot = run_slot(series_dir=args.series_dir, slot_index=args.slot)
    print(f"slot {args.slot}: {status}")
    return 0 if status == SLOT_OBSERVED else 4


def _cmd_mark_gap(args: argparse.Namespace) -> int:
    mark_gap(series_dir=args.series_dir, slot_index=args.slot, reason=args.reason)
    print(f"slot {args.slot}: un_observed (skipped)")
    return 0


def _cmd_status(args: argparse.Namespace) -> int:
    print(json.dumps(series_status(args.series_dir), indent=2, sort_keys=True))
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Operator-triggered demand-durability series runner: run a commissioned, "
            "Decision-Frame-bound series over time by invoking the step-2 durability writer "
            "per slot. Records realized timings + gaps. INV-1: facts only, no demand verdict."
        )
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="declare a new commissioned series from a spec")
    init.add_argument("--series-dir", type=Path, required=True)
    init.add_argument("--series-id", required=True)
    init.add_argument("--decision-frame-ref", required=True, help="reference to the commissioning Decision Frame (Ob.1)")
    init.add_argument("--decision-question", required=True)
    init.add_argument("--url", action="append", required=True, help="a source URL (repeatable for a fixed source set)")
    init.add_argument("--anchor-time", default=None, help="declared series start (ISO-8601 ...Z); defaults to now")
    init.add_argument("--cadence-mode", choices=["fixed", "bounded_jitter"], required=True)
    init.add_argument("--slot-count", type=int, required=True)
    init.add_argument("--cadence-delay-seconds", type=float, default=None)
    init.add_argument("--cadence-window-seconds", type=float, default=None)
    init.add_argument("--cadence-min-gap-seconds", type=float, default=None)
    init.add_argument("--cadence-max-gap-seconds", type=float, default=None)
    init.add_argument("--cadence-random-seed", type=int, default=None)
    init.add_argument("--session-visibility-pin", default=None)
    init.add_argument("--locale-pin", default=None)
    init.add_argument("--currency-pin", default=None)
    init.add_argument("--variant-pin", default=None)
    init.add_argument("--variant-pin-unknown-reason", default=None)
    init.add_argument("--cold-start-at", default=None)
    init.add_argument("--pre-coverage-history-posture", default=None)
    init.set_defaults(func=_cmd_init)

    run = sub.add_parser("run-slot", help="execute one slot NOW (fetch + record); operator-triggered")
    run.add_argument("--series-dir", type=Path, required=True)
    run.add_argument("--slot", type=int, required=True)
    run.set_defaults(func=_cmd_run_slot)

    gap = sub.add_parser("mark-gap", help="record a slot as an un-observed gap (skipped); never no-change")
    gap.add_argument("--series-dir", type=Path, required=True)
    gap.add_argument("--slot", type=int, required=True)
    gap.add_argument("--reason", required=True)
    gap.set_defaults(func=_cmd_mark_gap)

    status = sub.add_parser("status", help="summarize observed / un-observed / pending slots (facts only)")
    status.add_argument("--series-dir", type=Path, required=True)
    status.set_defaults(func=_cmd_status)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ValueError as exc:
        parser.exit(status=2, message=f"demand-durability series runner failed: {exc}\n")
    except Exception as exc:  # surface, do not swallow
        parser.exit(status=3, message=f"demand-durability series runner failed: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
