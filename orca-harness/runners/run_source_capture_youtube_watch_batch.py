"""Ledger-driven batch capture of the admitted YouTube Shorts pool -- the
one-command sweep that makes a live recapture cycle practical.

The live producer (``run_youtube_watch_packet_metric_rollup_producer``) fails
closed unless EVERY ledger-admitted creator video has a committed watch packet,
and the per-video capture runner (``run_source_capture_youtube_watch_packet``)
handles exactly one video. This wrapper closes that gap: it reads the admitted
pool from the YouTube creator observation ledger (creator-classified rows only;
brand rows are never captured), loops the per-video capture core with pacing,
records every per-video outcome, and stops early on block-shaped trouble --
mirroring the IG calls batch runner's circuit-break/cooldown discipline.

Break semantics (the spec's dual trigger):

- a committed packet is capture SUCCESS even when the video is unavailable --
  unavailability is honest data, and ``detect_video_state`` classifies it;
- N consecutive capture-attempt FAILURES (an exception or a nonzero per-video
  exit) trip the break -- transport-level trouble;
- K consecutive committed packets whose ``video_state != "playable"`` also trip
  the break -- the suspected consent-wall/soft-block case, where captures
  "succeed" but every page classifies unplayable (a sweep of garbage must not
  count as success);
- a break writes a cooldown record; a rerun during active cooldown refuses
  (exit 4) unless ``--ignore-cooldown``.

A finished sweep with ANY per-video failures exits nonzero and names them: the
downstream producer needs 100% pool coverage, so a partial sweep is visibly
incomplete, never a quiet success. ``--resume-from <summary>`` skips the videos
a prior run already captured and re-attempts the rest.

The summary is a DISPOSABLE run report (timestamped, under ``_test_runs/`` by
default), not a durable schema. This wrapper makes no ToS-safety or
blocking-avoidance claim; pacing and the break triggers reduce risk, they do
not prove it away. CI never resolves the real lake or network: the testable
core takes injected ``capture_fn`` / ``sleep_fn`` / ``now_fn`` and runs against
``DataLakeRoot.for_test``; ``main``/``resolve`` is the only live-bound path.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.youtube_metric_seed import (
    _ledger_video_rows,
    _pool_index,
    _unwrap_creator_ledger,
)
from data_lake.root import DataLakeRoot, DataLakeRootError
from runners.run_source_capture_youtube_watch_packet import (
    run_source_capture_youtube_watch_packet,
)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CREATOR_LEDGER = (
    ROOT
    / "orca"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "youtube"
    / "youtube_shorts_fragrance_creator_observation_ledger_v0.json"
)

DEFAULT_PACE_SECONDS = 10.0
DEFAULT_BREAK_AFTER_FAILURES = 3
DEFAULT_BREAK_AFTER_NONPLAYABLE = 5
DEFAULT_COOLDOWN_SECONDS = 3600.0
# Mirrors the IG batch convention (IG_CIRCUIT_BREAK_EXIT_CODE = 4); the YT
# per-video runner uses 2/3/5, so 4 is free for the batch break/cooldown signal.
YOUTUBE_WATCH_BATCH_EXIT_CODE_BREAK = 4
DEFAULT_DECISION_QUESTION = (
    "Recapture the ledger-admitted fragrance Shorts pool for the creator "
    "registry's live metric refresh."
)

_CREATOR_CLASSIFICATION_INCLUDED = "creator_or_channel_observed"


def default_output_root() -> Path:
    return Path(__file__).resolve().parents[1] / "_test_runs" / "youtube_watch_batch"


def default_cooldown_ledger_path() -> Path:
    return Path(__file__).resolve().parents[1] / "_test_runs" / "youtube_watch_cooldown_ledger.json"


def admitted_pool_video_ids(creator_ledger: Mapping[str, Any]) -> list[str]:
    """The creator-classified admitted video ids in pool order -- exactly the
    set the live metric-document builder will demand packets for. (The ledger
    reader keys by video id, so the ids are unique by construction.)"""
    ledger_rows = _ledger_video_rows(_unwrap_creator_ledger(dict(creator_ledger)))
    ordered = sorted(
        (
            (_pool_index(row["pool_id"]), video_id)
            for video_id, row in ledger_rows.items()
            if row["creator"].get("creator_classification") == _CREATOR_CLASSIFICATION_INCLUDED
        )
    )
    return [video_id for _index, video_id in ordered]


def _default_capture_fn(
    *, video_id: str, data_root: DataLakeRoot, decision_question: str, comment_pages: int
) -> tuple[int, str]:
    return run_source_capture_youtube_watch_packet(
        video_id=video_id,
        data_root=data_root,
        decision_question=decision_question,
        comment_pages=comment_pages,
    )


def run_youtube_watch_batch(
    data_root: DataLakeRoot,
    *,
    creator_ledger: Mapping[str, Any],
    decision_question: str = DEFAULT_DECISION_QUESTION,
    comment_pages: int = 2,
    pace_seconds: float = DEFAULT_PACE_SECONDS,
    break_after_failures: int = DEFAULT_BREAK_AFTER_FAILURES,
    break_after_nonplayable: int = DEFAULT_BREAK_AFTER_NONPLAYABLE,
    cooldown_seconds: float = DEFAULT_COOLDOWN_SECONDS,
    ignore_cooldown: bool = False,
    resume_from: Path | None = None,
    output_root: Path | None = None,
    cooldown_ledger_path: Path | None = None,
    capture_fn: Callable[..., tuple[int, str]] = _default_capture_fn,
    sleep_fn: Callable[[float], None] | None = None,
    now_fn: Callable[[], datetime] | None = None,
) -> tuple[int, str]:
    """Sweep the admitted pool through the per-video capture core. Returns
    ``(exit_code, summary_path)``: 0 = complete sweep, all committed;
    4 = circuit break or active cooldown; 2 = sweep finished but incomplete
    (per-video failures named in the summary)."""
    _validate_inputs(
        pace_seconds=pace_seconds,
        break_after_failures=break_after_failures,
        break_after_nonplayable=break_after_nonplayable,
        cooldown_seconds=cooldown_seconds,
    )
    if sleep_fn is None:
        import time

        sleep_fn = time.sleep
    now_fn = now_fn or (lambda: datetime.now(UTC))
    output_root = output_root or default_output_root()
    cooldown_ledger_path = cooldown_ledger_path or default_cooldown_ledger_path()

    pool = admitted_pool_video_ids(creator_ledger)
    if not pool:
        raise ValueError("YouTube creator observation ledger has no creator-classified videos")
    already_captured = _resume_captured_video_ids(resume_from)

    output_root.mkdir(parents=True, exist_ok=True)
    started_at = now_fn()
    summary_path = output_root / f"youtube_watch_batch_summary_{_file_stamp(started_at)}.json"

    cooldown = _active_cooldown(cooldown_ledger_path=cooldown_ledger_path, now=started_at)
    if cooldown is not None and not ignore_cooldown:
        summary = _build_summary(
            status="cooldown_active",
            pool=pool,
            rows=[],
            break_reason=None,
            cooldown=cooldown,
            cooldown_seconds=cooldown_seconds,
            started_at=started_at,
            finished_at=now_fn(),
            resume_from=resume_from,
        )
        _write_json(summary_path, summary)
        return YOUTUBE_WATCH_BATCH_EXIT_CODE_BREAK, str(summary_path)

    rows: list[dict[str, Any]] = []
    failure_streak = 0
    nonplayable_streak = 0
    break_reason: str | None = None
    cooldown_record: dict[str, Any] | None = None
    attempted_any = False

    for video_id in pool:
        if video_id in already_captured:
            rows.append(
                {
                    "video_id": video_id,
                    "status": "skipped_resume",
                    "packet_ref_or_error": None,
                    "video_state_or_none": None,
                    "attempted_at": None,
                }
            )
            continue

        if attempted_any and pace_seconds > 0:
            sleep_fn(pace_seconds)
        attempted_any = True

        row: dict[str, Any] = {
            "video_id": video_id,
            "status": "capture_failed",
            "packet_ref_or_error": None,
            "video_state_or_none": None,
            "attempted_at": _format_utc(now_fn()),
        }
        try:
            capture_exit, capture_message = capture_fn(
                video_id=video_id,
                data_root=data_root,
                decision_question=decision_question,
                comment_pages=comment_pages,
            )
        except Exception as exc:  # noqa: BLE001 - per-video failures stay visible in the summary
            capture_exit, capture_message = 2, f"{type(exc).__name__}: {exc}"

        if capture_exit == 0:
            packet_id = Path(str(capture_message)).name
            row["status"] = "captured"
            row["packet_ref_or_error"] = packet_id
            row["video_state_or_none"] = _committed_video_state(data_root, packet_id)
            failure_streak = 0
            if row["video_state_or_none"] == "playable":
                nonplayable_streak = 0
            else:
                nonplayable_streak += 1
        else:
            row["packet_ref_or_error"] = f"exit={capture_exit}: {capture_message}"
            failure_streak += 1
            nonplayable_streak = 0
        rows.append(row)

        if failure_streak >= break_after_failures:
            break_reason = (
                f"{failure_streak} consecutive capture failures (threshold "
                f"{break_after_failures}); suspected transport-level blocking"
            )
        elif nonplayable_streak >= break_after_nonplayable:
            break_reason = (
                f"{nonplayable_streak} consecutive non-playable committed packets (threshold "
                f"{break_after_nonplayable}); suspected consent wall or soft block"
            )
        if break_reason is not None:
            cooldown_record = _write_cooldown_record(
                cooldown_ledger_path=cooldown_ledger_path,
                cooldown_seconds=cooldown_seconds,
                now=now_fn(),
                trigger_video_id=video_id,
                break_reason=break_reason,
                output_root=output_root,
            )
            break

    status = (
        "stopped_circuit_break"
        if break_reason is not None
        else (
            "completed"
            if all(r["status"] in {"captured", "skipped_resume"} for r in rows)
            and len(rows) == len(pool)
            else "completed_with_failures"
        )
    )
    summary = _build_summary(
        status=status,
        pool=pool,
        rows=rows,
        break_reason=break_reason,
        cooldown=cooldown_record,
        cooldown_seconds=cooldown_seconds,
        started_at=started_at,
        finished_at=now_fn(),
        resume_from=resume_from,
    )
    _write_json(summary_path, summary)

    if status == "stopped_circuit_break":
        return YOUTUBE_WATCH_BATCH_EXIT_CODE_BREAK, str(summary_path)
    if status == "completed":
        return 0, str(summary_path)
    return 2, str(summary_path)


# -- helpers -------------------------------------------------------------------

def _validate_inputs(
    *,
    pace_seconds: float,
    break_after_failures: int,
    break_after_nonplayable: int,
    cooldown_seconds: float,
) -> None:
    if pace_seconds < 0:
        raise ValueError("pace_seconds must be zero or greater")
    if break_after_failures <= 0:
        raise ValueError("break_after_failures must be greater than zero")
    if break_after_nonplayable <= 0:
        raise ValueError("break_after_nonplayable must be greater than zero")
    if cooldown_seconds < 0:
        raise ValueError("cooldown_seconds must be zero or greater")


def _resume_captured_video_ids(resume_from: Path | None) -> set[str]:
    if resume_from is None:
        return set()
    payload = json.loads(Path(resume_from).read_text(encoding="utf-8"))
    results = payload.get("results")
    if not isinstance(results, list):
        raise ValueError(f"resume summary has no results list: {resume_from}")
    return {
        str(row.get("video_id"))
        for row in results
        if isinstance(row, dict) and row.get("status") in {"captured", "skipped_resume"}
    }


def _committed_video_state(data_root: DataLakeRoot, packet_id: str) -> str | None:
    """Read the just-committed packet's capture payload for its availability
    state (verified by-key read). A readback problem is reported as an unknown
    state, never a capture failure -- the packet is already committed."""
    try:
        loaded = data_root.load_raw_packet(packet_id)
        for entry in loaded.manifest.get("preserved_files", []):
            basename = str(entry.get("relative_packet_path", "")).rsplit("/", 1)[-1]
            original = basename.split("_", 1)[1] if "_" in basename else basename
            if original == "youtube_watch_capture.json":
                payload = json.loads(loaded.bodies[entry["file_id"]].decode("utf-8"))
                availability = payload.get("availability")
                if isinstance(availability, Mapping):
                    state = availability.get("video_state")
                    return state if isinstance(state, str) else None
                return None
    except Exception:  # noqa: BLE001 - readback is diagnostic; the commit already happened
        return None
    return None


def _active_cooldown(*, cooldown_ledger_path: Path, now: datetime) -> dict[str, Any] | None:
    if not cooldown_ledger_path.is_file():
        return None
    payload = json.loads(cooldown_ledger_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("YouTube watch cooldown ledger must be a JSON object")
    raw_until = payload.get("cooldown_until")
    if not isinstance(raw_until, str):
        raise ValueError("YouTube watch cooldown ledger missing cooldown_until")
    if _parse_utc(raw_until) <= now:
        return None
    out = dict(payload)
    out["cooldown_active"] = True
    return out


def _write_cooldown_record(
    *,
    cooldown_ledger_path: Path,
    cooldown_seconds: float,
    now: datetime,
    trigger_video_id: str,
    break_reason: str,
    output_root: Path,
) -> dict[str, Any]:
    record = {
        "runner": "youtube_watch_batch",
        "cooldown_started_at": _format_utc(now),
        "cooldown_until": _format_utc(now + timedelta(seconds=cooldown_seconds)),
        "cooldown_seconds": cooldown_seconds,
        "trigger_video_id": trigger_video_id,
        "trigger_reason": break_reason,
        "batch_output_root": str(output_root),
        "non_claims": [
            "not proof of an actual platform block",
            "not a ToS-safety or blocking-avoidance guarantee",
            "not validation",
        ],
    }
    cooldown_ledger_path.parent.mkdir(parents=True, exist_ok=True)
    _write_json(cooldown_ledger_path, record)
    return record


def _build_summary(
    *,
    status: str,
    pool: Sequence[str],
    rows: list[dict[str, Any]],
    break_reason: str | None,
    cooldown: dict[str, Any] | None,
    cooldown_seconds: float,
    started_at: datetime,
    finished_at: datetime,
    resume_from: Path | None,
) -> dict[str, Any]:
    captured = sum(1 for row in rows if row["status"] == "captured")
    skipped = sum(1 for row in rows if row["status"] == "skipped_resume")
    failed = sum(1 for row in rows if row["status"] == "capture_failed")
    return {
        "runner": "youtube_watch_batch",
        "status": status,
        "started_at": _format_utc(started_at),
        "finished_at": _format_utc(finished_at),
        "resume_from": str(resume_from) if resume_from is not None else None,
        "break_reason_or_none": break_reason,
        "cooldown_or_none": cooldown,
        "cooldown_policy": {"ledger_enabled": True, "cooldown_seconds": cooldown_seconds},
        "counts": {
            "pool_total": len(pool),
            "attempted": captured + failed,
            "captured": captured,
            "skipped_resume": skipped,
            "capture_failed": failed,
            "not_attempted": len(pool) - len(rows),
        },
        "failed_video_ids": [row["video_id"] for row in rows if row["status"] == "capture_failed"],
        "results": rows,
        "non_claims": [
            "disposable run report, not a durable schema",
            "not producer/snapshot/materialize execution",
            "not a ToS-safety or blocking-avoidance guarantee",
        ],
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(f"{json.dumps(payload, indent=2, sort_keys=True)}\n", encoding="utf-8", newline="\n")


def _file_stamp(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")


def _format_utc(value: datetime) -> str:
    value = value.astimezone(UTC) if value.tzinfo is not None else value.replace(tzinfo=UTC)
    return value.isoformat().replace("+00:00", "Z")


def _parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Capture the ledger-admitted YouTube Shorts pool into the data lake, one watch "
            "packet per video, with pacing, circuit-break, cooldown, and a disposable summary."
        )
    )
    parser.add_argument("--creator-ledger", type=Path, default=DEFAULT_CREATOR_LEDGER)
    parser.add_argument("--data-root", default=None, help="Lake root; defaults to ORCA_DATA_ROOT.")
    parser.add_argument("--decision-question", default=DEFAULT_DECISION_QUESTION)
    parser.add_argument("--comment-pages", type=int, default=2)
    parser.add_argument("--pace-seconds", type=float, default=DEFAULT_PACE_SECONDS)
    parser.add_argument("--break-after-failures", type=int, default=DEFAULT_BREAK_AFTER_FAILURES)
    parser.add_argument(
        "--break-after-nonplayable", type=int, default=DEFAULT_BREAK_AFTER_NONPLAYABLE
    )
    parser.add_argument("--cooldown-seconds", type=float, default=DEFAULT_COOLDOWN_SECONDS)
    parser.add_argument("--ignore-cooldown", action="store_true")
    parser.add_argument(
        "--resume-from",
        type=Path,
        default=None,
        help="Prior run summary; videos it marks captured/skipped are not re-attempted.",
    )
    parser.add_argument("--output-root", type=Path, default=None)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
    except DataLakeRootError as exc:
        parser.exit(status=2, message=f"data lake unavailable: {exc}\n")

    creator_ledger = json.loads(Path(args.creator_ledger).read_text(encoding="utf-8-sig"))

    try:
        exit_code, summary_path = run_youtube_watch_batch(
            data_root,
            creator_ledger=creator_ledger,
            decision_question=args.decision_question,
            comment_pages=args.comment_pages,
            pace_seconds=args.pace_seconds,
            break_after_failures=args.break_after_failures,
            break_after_nonplayable=args.break_after_nonplayable,
            cooldown_seconds=args.cooldown_seconds,
            ignore_cooldown=args.ignore_cooldown,
            resume_from=args.resume_from,
            output_root=args.output_root,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"youtube watch batch failed: {exc}\n")

    summary = json.loads(Path(summary_path).read_text(encoding="utf-8"))
    counts = summary["counts"]
    print(
        f"{summary['status']}: captured={counts['captured']} failed={counts['capture_failed']} "
        f"skipped={counts['skipped_resume']} not_attempted={counts['not_attempted']} "
        f"of pool={counts['pool_total']}"
    )
    if summary["break_reason_or_none"]:
        print(f"  break: {summary['break_reason_or_none']}")
    if summary["failed_video_ids"]:
        print(f"  failed videos: {', '.join(summary['failed_video_ids'])}")
    print(f"  summary: {summary_path}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
