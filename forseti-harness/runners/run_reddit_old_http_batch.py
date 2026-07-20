from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Sequence
from urllib.parse import urlparse

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot

from harness_utils import utc_now_z_microseconds
from runners.run_source_capture_http_packet import run_source_capture_http_packet
from source_capture import CaptureModeCategory
from source_capture.cadence import CadenceMode, build_cadence_plan
from source_capture.content_extraction import (
    CAPTURE_RETENTION_MODES,
    CONTENT_EXTRACTION_FAILED_EXIT_CODE,
    CONTENT_RECORD_FILENAME,
    ContentExtractionSpec,
)
from source_capture.reddit_consolidation import (
    OLD_REDDIT_THREAD_PARSER_VERSION,
    build_thread_content_record,
)


DEFAULT_DELAY_SECONDS = 30.0
DEFAULT_MAX_URLS = 10
DEFAULT_TIMEOUT_SECONDS = 20.0
DEFAULT_MAX_BYTES = 5_000_000
# Content retention is the standard fleet posture: the thread record is
# extracted in flight and preserved in the packet; raw is hashed then
# discarded. Raw remains the explicit operator-selected evidence posture.
DEFAULT_RETENTION_MODE = "content"


@dataclass(frozen=True)
class BatchSlot:
    slot_id: str
    url: str


def run_reddit_old_http_batch(
    *,
    slots: Sequence[BatchSlot],
    output_root: Path,
    decision_question: str,
    data_root: "DataLakeRoot | None" = None,
    delay_seconds: float = DEFAULT_DELAY_SECONDS,
    max_urls: int = DEFAULT_MAX_URLS,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_BYTES,
    cadence_mode: CadenceMode = "fixed",
    cadence_window_seconds: float | None = None,
    cadence_min_gap_seconds: float | None = None,
    cadence_max_gap_seconds: float | None = None,
    cadence_random_seed: int | None = None,
    requested_retention_mode: str = DEFAULT_RETENTION_MODE,
) -> tuple[int, str]:
    if requested_retention_mode not in CAPTURE_RETENTION_MODES:
        raise ValueError(
            f"requested_retention_mode must be one of {CAPTURE_RETENTION_MODES}, "
            f"got {requested_retention_mode!r}"
        )
    _validate_batch_inputs(
        slots=slots,
        output_root=output_root,
        delay_seconds=delay_seconds,
        max_urls=max_urls,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
    )
    cadence_plan = build_cadence_plan(
        slot_count=len(slots),
        mode=cadence_mode,
        delay_seconds=delay_seconds,
        window_seconds=cadence_window_seconds,
        min_gap_seconds=cadence_min_gap_seconds,
        max_gap_seconds=cadence_max_gap_seconds,
        random_seed=cadence_random_seed,
    )
    output_root.mkdir(parents=True, exist_ok=True)
    summary_path = output_root / "batch_summary.json"
    if summary_path.exists():
        raise ValueError(f"batch summary already exists: {summary_path}")

    results: list[dict[str, Any]] = []
    for index, slot in enumerate(slots):
        packet_dir = None if data_root is not None else output_root / f"{slot.slot_id}_packet"
        row: dict[str, Any] = {
            "slot_id": slot.slot_id,
            "url": slot.url,
            "capture_exit": None,
            "capture_message": None,
            "packet_dir": str(packet_dir) if packet_dir is not None else None,
            "lake_committed": data_root is not None,
            "retry_count": 0,
            "planned_start_offset_seconds": cadence_plan.planned_offsets_seconds[index],
            "planned_wait_after_seconds": (
                cadence_plan.planned_waits_seconds[index]
                if index < len(cadence_plan.planned_waits_seconds)
                else None
            ),
            "capture_started_at": None,
            "capture_finished_at": None,
            "content_extraction_failed": False,
            "content_record_preserved": False,
        }

        extraction_spec = ContentExtractionSpec(
            requested_retention_mode=requested_retention_mode,
            extractor_version=OLD_REDDIT_THREAD_PARSER_VERSION,
            extractor=lambda html_text, final_url: build_thread_content_record(
                html_text=html_text,
                source_url=final_url,
            ),
        )
        try:
            row["capture_started_at"] = utc_now_z_microseconds()
            capture_exit, capture_message = run_source_capture_http_packet(
                url=slot.url,
                source_family="reddit_thread",
                source_surface="old_reddit_direct_http",
                decision_question=decision_question,
                output_directory=packet_dir,
                data_root=data_root,
                capture_context=(
                    "bounded old Reddit direct HTTP calibration batch; exact supplied URL only; "
                    "no proxy, browser, crawler, retry, or link following"
                ),
                operator_category="reddit_old_http_batch_operator",
                capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
                session_id=None,
                actor_audience_context=None,
                visible_mode_changes=[],
                source_publication_or_event=None,
                source_edit_or_version=None,
                cutoff_posture=None,
                recapture_time=None,
                re_capture_relationship=None,
                warnings=[],
                limitations=[
                    "batch runner accepts exact old.reddit.com URLs only",
                    f"batch runner cadence_mode={cadence_plan.mode}",
                    f"batch runner planned_start_offset_seconds={cadence_plan.planned_offsets_seconds[index]}",
                    "batch runner retry_count=0",
                ],
                timeout_seconds=timeout_seconds,
                max_bytes=max_bytes,
                content_extraction=extraction_spec,
            )
            row["capture_exit"] = capture_exit
            row["capture_message"] = capture_message
            if capture_exit == CONTENT_EXTRACTION_FAILED_EXIT_CODE:
                row["content_extraction_failed"] = True
            if capture_exit in (0, CONTENT_EXTRACTION_FAILED_EXIT_CODE) and packet_dir is None:
                # Lake commit: the runner returns the committed packet directory.
                packet_dir = Path(capture_message)
                row["packet_dir"] = str(packet_dir)
            if packet_dir is not None:
                row["content_record_preserved"] = _packet_preserves_content_record(packet_dir)
        except Exception as exc:
            row["capture_exit"] = 2
            row["capture_message"] = f"{type(exc).__name__}: {exc}"
        finally:
            row["capture_finished_at"] = utc_now_z_microseconds()

        results.append(row)
        if index < len(cadence_plan.planned_waits_seconds):
            wait_seconds = cadence_plan.planned_waits_seconds[index]
            if wait_seconds > 0:
                time.sleep(wait_seconds)

    summary = {
        "runner": "reddit_old_http_batch",
        "method": "old_reddit_direct_http",
        "requested_retention_mode": requested_retention_mode,
        "content_extraction_failure_count": sum(
            1 for row in results if row["content_extraction_failed"]
        ),
        "lake_committed": data_root is not None,
        "non_claims": [
            "not crawler",
            "not source discovery",
            "not monitoring",
            "not proxy use",
            "not browser automation",
            "not retry escalation",
            "not broad Reddit crawl",
        ],
        "delay_seconds": cadence_plan.delay_seconds,
        "cadence": cadence_plan.to_dict(),
        "max_urls": max_urls,
        "url_count": len(slots),
        "capture_success_count": sum(1 for row in results if row["capture_exit"] == 0),
        "results": results,
    }
    summary_path.write_text(
        f"{json.dumps(summary, indent=2, sort_keys=True)}\n",
        encoding="utf-8",
        newline="\n",
    )
    return 0, str(summary_path)


def _packet_preserves_content_record(packet_dir: Path) -> bool:
    return (
        sum(
            1
            for path in packet_dir.rglob(CONTENT_RECORD_FILENAME)
            if path.is_file() and path.name == CONTENT_RECORD_FILENAME
        )
        == 1
    )


def load_slots(path: Path) -> list[BatchSlot]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("URL list must be a JSON array")

    slots: list[BatchSlot] = []
    for index, item in enumerate(payload, start=1):
        if isinstance(item, str):
            slot_id = f"slot_{index:03d}"
            url = item
        elif isinstance(item, dict):
            raw_slot_id = item.get("slot_id") or item.get("id")
            raw_url = item.get("url")
            if not isinstance(raw_slot_id, str) or not raw_slot_id.strip():
                raise ValueError(f"URL list item {index} must include a non-empty slot_id")
            if not isinstance(raw_url, str) or not raw_url.strip():
                raise ValueError(f"URL list item {index} must include a non-empty url")
            slot_id = raw_slot_id.strip()
            url = raw_url.strip()
        else:
            raise ValueError(f"URL list item {index} must be a string or object")
        slots.append(BatchSlot(slot_id=_validate_slot_id(slot_id), url=_validate_old_reddit_url(url)))
    return slots


def _validate_batch_inputs(
    *,
    slots: Sequence[BatchSlot],
    output_root: Path,
    delay_seconds: float,
    max_urls: int,
    timeout_seconds: float,
    max_bytes: int,
) -> None:
    if not slots:
        raise ValueError("batch requires at least one URL")
    if max_urls <= 0:
        raise ValueError("max_urls must be greater than zero")
    if len(slots) > max_urls:
        raise ValueError(f"batch received {len(slots)} URL(s), above max_urls={max_urls}")
    if delay_seconds < 0:
        raise ValueError("delay_seconds must be zero or greater")
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")
    if max_bytes <= 0:
        raise ValueError("max_bytes must be greater than zero")
    if output_root.exists() and not output_root.is_dir():
        raise ValueError(f"output_root exists and is not a directory: {output_root}")
    slot_ids = [slot.slot_id for slot in slots]
    duplicates = sorted({slot_id for slot_id in slot_ids if slot_ids.count(slot_id) > 1})
    if duplicates:
        raise ValueError(f"duplicate slot_id value(s): {duplicates}")
    # Enforce the exact-URL/old.reddit.com-only and safe-slot-id bounds at the
    # execution boundary, not only in load_slots. run_reddit_old_http_batch and
    # BatchSlot are an importable API: a caller that builds slots directly must
    # not be able to bypass the host bound or smuggle a path-traversal slot_id
    # into the per-slot packet/derived directory names.
    for slot in slots:
        _validate_slot_id(slot.slot_id)
        _validate_old_reddit_url(slot.url)


def _validate_slot_id(slot_id: str) -> str:
    if not slot_id.replace("_", "").replace("-", "").isalnum():
        raise ValueError("slot_id may contain only letters, numbers, underscore, and hyphen")
    return slot_id


def _validate_old_reddit_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname != "old.reddit.com":
        raise ValueError("batch accepts only absolute old.reddit.com URLs")
    if "/comments/" not in parsed.path:
        raise ValueError("batch accepts only old Reddit thread URLs containing /comments/")
    return parsed.geturl()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run a polite bounded old Reddit direct-HTTP content-extraction batch for "
            "an explicit JSON list of exact thread URLs."
        )
    )
    parser.add_argument("--url-list", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument(
        "--data-root",
        default=None,
        help=(
            "Commit packets into the Forseti data lake at this root instead of per-slot "
            "local packet directories; the batch summary stays "
            "under --output-root."
        ),
    )
    parser.add_argument("--decision-question", required=True)
    parser.add_argument("--delay-seconds", type=float, default=DEFAULT_DELAY_SECONDS)
    parser.add_argument("--max-urls", type=int, default=DEFAULT_MAX_URLS)
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    parser.add_argument("--cadence-mode", choices=["fixed", "bounded_jitter"], default="fixed")
    parser.add_argument("--cadence-window-seconds", type=float, default=None)
    parser.add_argument("--cadence-min-gap-seconds", type=float, default=None)
    parser.add_argument("--cadence-max-gap-seconds", type=float, default=None)
    parser.add_argument("--cadence-random-seed", type=int, default=None)
    parser.add_argument(
        "--retention-mode",
        choices=list(CAPTURE_RETENTION_MODES),
        default=DEFAULT_RETENTION_MODE,
        help=(
            "content (default): extract the thread in flight, preserve the content record, "
            "and discard raw after hashing; raw: preserve the response."
        ),
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
        exit_code, message = run_reddit_old_http_batch(
            slots=load_slots(args.url_list),
            output_root=args.output_root,
            decision_question=args.decision_question,
            data_root=data_root,
            delay_seconds=args.delay_seconds,
            max_urls=args.max_urls,
            timeout_seconds=args.timeout_seconds,
            max_bytes=args.max_bytes,
            cadence_mode=args.cadence_mode,
            cadence_window_seconds=args.cadence_window_seconds,
            cadence_min_gap_seconds=args.cadence_min_gap_seconds,
            cadence_max_gap_seconds=args.cadence_max_gap_seconds,
            cadence_random_seed=args.cadence_random_seed,
            requested_retention_mode=args.retention_mode,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"reddit old HTTP batch failed: {exc}\n")
    except Exception as exc:
        parser.exit(status=3, message=f"reddit old HTTP batch failed: {exc}\n")

    print(message)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
