"""Parser-fit drift check over Reddit sample packets (raw + derived preserved).

Storage-and-retention doctrine (reddit_radar_grid_capture_maintenance_design_v0.md,
2026-07-17): the fleet captures content packets (raw discarded after hashing),
and a small rotating daily sample preserves BOTH the raw HTML and the
capture-time derived record in one packet. This runner is the drift alarm:
it re-projects each sample's raw bytes through the CURRENT parser and diffs
the result against the packet's own stored derived record. A mismatch means
Reddit changed markup (or the parser changed behavior without a version bump)
and the fleet's content packets may be silently degrading.

Exit codes: 0 all samples match; 1 at least one drift or per-packet failure;
2 usage error. The check is read-only and makes no registry, lake, or
readiness claim.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import hash_file
from capture_spine.reddit_subreddit_grid.grid_projection import (
    GRID_PROJECTION_PARSER_VERSION,
    build_grid_content_record,
)
from source_capture.models import SOURCE_CAPTURE_MANIFEST_VERSION
from source_capture.packet_inspection import read_packet_leniently
from source_capture.reddit_consolidation import (
    OLD_REDDIT_THREAD_PARSER_VERSION,
    build_thread_content_record,
)
from source_capture.source_quality import resolve_manifest_path

GRID_SOURCE_FAMILY = "reddit_subreddit_grid"
THREAD_SOURCE_FAMILY = "reddit_thread"


class ParserFitCheckError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def check_packet_parser_fit(*, packet_or_manifest_path: Path) -> dict[str, Any]:
    """Check one sample packet; returns a report row (raises only on unusable input)."""
    manifest_path = resolve_manifest_path(packet_or_manifest_path).resolve()
    try:
        report = read_packet_leniently(manifest_path)
    except Exception as exc:
        raise ParserFitCheckError("manifest_read_failure", f"manifest could not be read: {exc}") from exc
    if not report.conforms_to_current_schema or not report.declares_current_manifest_version:
        raise ParserFitCheckError(
            "manifest_nonconforming",
            f"manifest is not a current {SOURCE_CAPTURE_MANIFEST_VERSION!r} packet: {manifest_path}",
        )
    packet = report.packet
    if packet is None:
        raise ParserFitCheckError("packet_unavailable", "no validated packet was available")
    if packet.source_family not in (GRID_SOURCE_FAMILY, THREAD_SOURCE_FAMILY):
        raise ParserFitCheckError(
            "ineligible_source_family",
            f"parser-fit check covers {GRID_SOURCE_FAMILY!r} and {THREAD_SOURCE_FAMILY!r}, "
            f"got {packet.source_family!r}",
        )

    packet_dir = manifest_path.parent
    raw_path = _verified_preserved_path(
        packet=packet, packet_dir=packet_dir, file_name="http_response_body.bin"
    )
    content_path = _verified_preserved_path(
        packet=packet, packet_dir=packet_dir, file_name="content_record.json"
    )

    stored_record = json.loads(content_path.read_text(encoding="utf-8"))
    if not isinstance(stored_record, dict):
        raise ParserFitCheckError("content_record_shape", "stored content record is not a JSON object")
    html = raw_path.read_text(encoding="utf-8", errors="replace")

    if packet.source_family == GRID_SOURCE_FAMILY:
        current_parser_version = GRID_PROJECTION_PARSER_VERSION
        grid_view = stored_record.get("grid_view")
        if not isinstance(grid_view, dict):
            raise ParserFitCheckError("content_record_shape", "grid record carries no grid_view object")
        reprojected = build_grid_content_record(
            html_text=html,
            subreddit=str(grid_view.get("subreddit", "")),
            listing_url=str(grid_view.get("listing_url", "")),
        )
    else:
        current_parser_version = OLD_REDDIT_THREAD_PARSER_VERSION
        source_url = stored_record.get("source_url")
        if not isinstance(source_url, str) or not source_url:
            raise ParserFitCheckError("content_record_shape", "thread record carries no source_url")
        reprojected = build_thread_content_record(html_text=html, source_url=source_url)

    drift = reprojected != stored_record
    return {
        "manifest_path": str(manifest_path),
        "source_family": packet.source_family,
        "stored_parser_version": stored_record.get("parser_version"),
        "current_parser_version": current_parser_version,
        "status": "drift" if drift else "match",
        "diff_summary": _diff_summary(stored_record, reprojected) if drift else None,
    }


def _verified_preserved_path(*, packet, packet_dir: Path, file_name: str) -> Path:
    matches = [
        item
        for item in packet.preserved_files
        if item.relative_packet_path.replace("\\", "/").endswith(file_name)
    ]
    if len(matches) != 1:
        raise ParserFitCheckError(
            "preserved_file_unresolved",
            f"a sample packet must preserve exactly one {file_name} "
            f"(raw AND derived are required for a drift check), found {len(matches)}",
        )
    preserved = matches[0]
    packet_root = packet_dir.resolve()
    candidate = (packet_root / preserved.relative_packet_path).resolve()
    if not candidate.is_relative_to(packet_root):
        raise ParserFitCheckError(
            "preserved_file_escape",
            f"preserved file path escapes packet directory: {preserved.relative_packet_path!r}",
        )
    actual_hash = hash_file(candidate)
    if actual_hash != preserved.sha256:
        raise ParserFitCheckError(
            "preserved_file_hash_mismatch",
            f"stored bytes hash mismatch for {file_name}: manifest={preserved.sha256} actual={actual_hash}",
        )
    return candidate


def _diff_summary(stored: dict[str, Any], reprojected: dict[str, Any]) -> dict[str, Any]:
    differing_keys = sorted(
        key
        for key in set(stored) | set(reprojected)
        if stored.get(key) != reprojected.get(key)
    )
    summary: dict[str, Any] = {"differing_top_level_keys": differing_keys}
    for list_key in ("comments",):
        if list_key in differing_keys:
            summary[f"{list_key}_count_stored"] = len(stored.get(list_key) or [])
            summary[f"{list_key}_count_reprojected"] = len(reprojected.get(list_key) or [])
    if "grid_view" in differing_keys:
        stored_rows = (stored.get("grid_view") or {}).get("thread_rows") or []
        reprojected_rows = (reprojected.get("grid_view") or {}).get("thread_rows") or []
        summary["thread_rows_count_stored"] = len(stored_rows)
        summary["thread_rows_count_reprojected"] = len(reprojected_rows)
    return summary


def run_reddit_parser_fit_check(
    *,
    packet_paths: Sequence[Path],
    report_path: Path | None = None,
) -> tuple[int, dict[str, Any]]:
    if not packet_paths:
        raise ParserFitCheckError("no_packets", "at least one sample packet path is required")
    rows: list[dict[str, Any]] = []
    for path in packet_paths:
        try:
            rows.append(check_packet_parser_fit(packet_or_manifest_path=path))
        except ParserFitCheckError as exc:
            rows.append(
                {
                    "manifest_path": str(path),
                    "status": "check_failed",
                    "failure_code": exc.code,
                    "failure_message": exc.message,
                }
            )
    drift_count = sum(1 for row in rows if row["status"] == "drift")
    failure_count = sum(1 for row in rows if row["status"] == "check_failed")
    report = {
        "runner": "reddit_parser_fit_check",
        "packet_count": len(rows),
        "match_count": sum(1 for row in rows if row["status"] == "match"),
        "drift_count": drift_count,
        "check_failure_count": failure_count,
        "results": rows,
        "non_claims": [
            "not validation or readiness",
            "not source completeness proof",
            "not registry or lake mutation",
        ],
    }
    if report_path is not None:
        if report_path.exists():
            raise ParserFitCheckError("report_exists", f"report already exists: {report_path}")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            f"{json.dumps(report, indent=2, sort_keys=True)}\n",
            encoding="utf-8",
            newline="\n",
        )
    exit_code = 0 if drift_count == 0 and failure_count == 0 else 1
    return exit_code, report


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Re-project Reddit sample packets (raw + derived preserved) through the current "
            "parser and diff against the stored derived record; nonzero exit on any drift."
        )
    )
    parser.add_argument(
        "--packet",
        action="append",
        required=True,
        type=Path,
        dest="packets",
        help="Sample packet directory or manifest path; repeatable.",
    )
    parser.add_argument("--report", type=Path, default=None, help="Optional JSON report output path.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        exit_code, report = run_reddit_parser_fit_check(
            packet_paths=args.packets,
            report_path=args.report,
        )
    except ParserFitCheckError as exc:
        parser.exit(status=2, message=f"reddit parser-fit check failed: {exc.message}\n")
    except Exception as exc:
        parser.exit(status=2, message=f"reddit parser-fit check failed: {exc}\n")

    print(json.dumps(report, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
