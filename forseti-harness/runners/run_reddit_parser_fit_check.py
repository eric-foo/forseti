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
from urllib.parse import urlparse

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import hash_file
from capture_spine.reddit_subreddit_grid.grid_projection import (
    GRID_PROJECTION_PARSER_VERSION,
    RedditGridProjectionError,
    build_grid_content_record,
    grid_view_from_record,
)
from source_capture.models import SOURCE_CAPTURE_MANIFEST_VERSION
from source_capture.packet_inspection import read_packet_leniently
from source_capture.reddit_consolidation import (
    OLD_REDDIT_THREAD_PARSER_VERSION,
    THREAD_CONTENT_RECORD_KIND,
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
    metadata_path = _verified_preserved_path(
        packet=packet, packet_dir=packet_dir, file_name="http_response_metadata.json"
    )

    stored_record = _read_json_object(
        content_path,
        error_code="content_record_shape",
        label="stored content record",
    )
    metadata = _read_json_object(
        metadata_path,
        error_code="http_metadata_shape",
        label="stored HTTP metadata",
    )
    _verify_sample_metadata(
        metadata=metadata,
        stored_record=stored_record,
        raw_path=raw_path,
    )
    current_parser_version = (
        GRID_PROJECTION_PARSER_VERSION
        if packet.source_family == GRID_SOURCE_FAMILY
        else OLD_REDDIT_THREAD_PARSER_VERSION
    )
    stored_parser_version = stored_record.get("parser_version")
    if stored_parser_version != current_parser_version:
        raise ParserFitCheckError(
            "parser_version_mismatch",
            f"stored parser_version {stored_parser_version!r} does not match "
            f"current parser_version {current_parser_version!r}; compare samples only "
            "within one parser version",
        )
    html = raw_path.read_text(encoding="utf-8", errors="replace")

    if packet.source_family == GRID_SOURCE_FAMILY:
        try:
            grid_view = grid_view_from_record(stored_record)
        except RedditGridProjectionError as exc:
            raise ParserFitCheckError(
                "content_record_shape",
                f"stored grid content record is invalid: {exc}",
            ) from exc
        if not isinstance(grid_view.subreddit, str) or not isinstance(
            grid_view.listing_url, str
        ):
            raise ParserFitCheckError(
                "content_record_shape",
                "stored grid content record subreddit and listing_url must be strings",
            )
        locator = packet.source_locator.value
        expected_subreddit = _grid_subreddit_from_url(locator)
        if expected_subreddit is None:
            raise ParserFitCheckError(
                "grid_locator_invalid",
                f"packet source locator is not an old-Reddit grid URL: {locator!r}",
            )
        if grid_view.subreddit.lower() != expected_subreddit:
            raise ParserFitCheckError(
                "grid_subreddit_mismatch",
                f"stored grid record names subreddit {grid_view.subreddit!r}, "
                f"packet locator names {expected_subreddit!r}",
            )
        if grid_view.listing_url != locator:
            raise ParserFitCheckError(
                "grid_listing_url_mismatch",
                f"stored grid record listing_url {grid_view.listing_url!r} "
                f"does not match packet locator {locator!r}",
            )
        final_url = metadata["final_url"]
        if _grid_subreddit_from_url(final_url) != expected_subreddit:
            raise ParserFitCheckError(
                "grid_final_url_mismatch",
                f"HTTP final URL does not match packet subreddit {expected_subreddit!r}: "
                f"{final_url!r}",
            )
        reprojected = build_grid_content_record(
            html_text=html,
            subreddit=expected_subreddit,
            listing_url=locator,
        )
    else:
        if stored_record.get("record_kind") != THREAD_CONTENT_RECORD_KIND:
            raise ParserFitCheckError(
                "content_record_shape",
                f"thread record_kind is {stored_record.get('record_kind')!r}, "
                f"expected {THREAD_CONTENT_RECORD_KIND!r}",
            )
        source_url = stored_record.get("source_url")
        if not isinstance(source_url, str) or not source_url:
            raise ParserFitCheckError("content_record_shape", "thread record carries no source_url")
        final_url = metadata["final_url"]
        if source_url != final_url or not _is_old_reddit_thread_url(final_url):
            raise ParserFitCheckError(
                "thread_source_url_mismatch",
                f"thread record source_url {source_url!r} is not the packet's "
                f"old-Reddit final URL {final_url!r}",
            )
        reprojected = build_thread_content_record(html_text=html, source_url=final_url)

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
    if not candidate.is_file():
        raise ParserFitCheckError(
            "preserved_file_missing",
            f"preserved file is missing: {preserved.relative_packet_path!r}",
        )
    actual_hash = hash_file(candidate)
    if actual_hash != preserved.sha256:
        raise ParserFitCheckError(
            "preserved_file_hash_mismatch",
            f"stored bytes hash mismatch for {file_name}: manifest={preserved.sha256} actual={actual_hash}",
        )
    return candidate


def _read_json_object(path: Path, *, error_code: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ParserFitCheckError(error_code, f"{label} could not be read: {exc}") from exc
    if not isinstance(value, dict):
        raise ParserFitCheckError(error_code, f"{label} is not a JSON object")
    return value


def _verify_sample_metadata(
    *,
    metadata: dict[str, Any],
    stored_record: dict[str, Any],
    raw_path: Path,
) -> None:
    content_capture = metadata.get("content_capture")
    if not isinstance(content_capture, dict):
        raise ParserFitCheckError(
            "content_capture_metadata_missing",
            "sample packet HTTP metadata carries no content_capture object",
        )
    if content_capture.get("capture_artifact_mode") != "sample":
        raise ParserFitCheckError(
            "not_sample_packet",
            "parser-fit check requires capture_artifact_mode='sample'",
        )
    if (
        content_capture.get("projection_status") != "succeeded"
        or content_capture.get("raw_preserved") is not True
    ):
        raise ParserFitCheckError(
            "sample_projection_incomplete",
            "sample packet must preserve raw bytes and a successfully projected record",
        )
    if content_capture.get("parser_version") != stored_record.get("parser_version"):
        raise ParserFitCheckError(
            "content_capture_parser_version_mismatch",
            "HTTP metadata parser_version does not match the stored content record",
        )
    status = metadata.get("status")
    if not isinstance(status, int) or not 200 <= status < 300:
        raise ParserFitCheckError(
            "sample_http_unsuccessful",
            f"sample packet HTTP status is not successful: {status!r}",
        )
    final_url = metadata.get("final_url")
    if not isinstance(final_url, str) or not final_url:
        raise ParserFitCheckError(
            "sample_final_url_missing",
            "sample packet HTTP metadata carries no final_url",
        )
    raw_hash = hash_file(raw_path)
    if content_capture.get("raw_sha256") != raw_hash:
        raise ParserFitCheckError(
            "raw_provenance_hash_mismatch",
            "HTTP metadata raw_sha256 does not match the preserved sample raw bytes",
        )
    if content_capture.get("raw_byte_count") != raw_path.stat().st_size:
        raise ParserFitCheckError(
            "raw_provenance_size_mismatch",
            "HTTP metadata raw_byte_count does not match the preserved sample raw bytes",
        )


def _grid_subreddit_from_url(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    parsed = urlparse(value)
    parts = [part for part in parsed.path.split("/") if part]
    if (
        parsed.scheme == "https"
        and parsed.netloc.lower() == "old.reddit.com"
        and len(parts) >= 3
        and parts[0] == "r"
        and parts[1].isascii()
        and parts[1].replace("_", "").isalnum()
        and parts[2] in {"hot", "new", "top", "rising"}
    ):
        return parts[1].lower()
    return None


def _is_old_reddit_thread_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return (
        parsed.scheme == "https"
        and parsed.netloc.lower() == "old.reddit.com"
        and "/comments/" in parsed.path
    )


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
