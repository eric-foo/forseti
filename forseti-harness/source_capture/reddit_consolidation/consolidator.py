from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from harness_utils import hash_file, sha256_text, utc_now_z
from source_capture.models import SOURCE_CAPTURE_MANIFEST_VERSION, PreservedFile, SourceCapturePacket
from source_capture.packet_inspection import PacketConformanceReport, read_packet_leniently
from source_capture.reddit_consolidation.parser import (
    OLD_REDDIT_THREAD_PARSER_VERSION,
    ParsedComment,
    RedditParseFailure,
    parse_old_reddit_html,
)
from source_capture.source_quality import resolve_manifest_path


REDDIT_THREAD_CONSOLIDATION_SCHEMA_VERSION = "reddit_thread_consolidation_v0"
THREAD_CONTENT_RECORD_KIND = "reddit_thread_content_v0"

NON_CLAIMS = [
    "not validation",
    "not readiness",
    "not Reddit source completeness proof",
    "not live Reddit capture",
    "not Reddit monitoring",
    "not source discovery",
    "not broad crawling",
    "not storage, database, queue, scheduler, dashboard, or export corpus",
    "not commercial API behavior",
    "not source-quality scoring",
    "not fixture admission",
    "not canonical source body",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring or judgment-quality evidence",
]

SECRET_OR_SESSION_MARKERS = {
    "authorization:",
    "bearer ",
    "cookie:",
    "cookie=",
    "password=",
    "storage_state",
    "session cookie",
}


class RedditConsolidationFailure(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def consolidate_reddit_packet(
    *,
    packet_or_manifest_path: Path,
    output_directory: Path,
    json_name: str = "reddit_thread_consolidation.json",
    receipt_name: str = "reddit_thread_consolidation_receipt.md",
) -> dict[str, str]:
    manifest_path = resolve_manifest_path(packet_or_manifest_path)
    packet_dir = manifest_path.parent
    _require_separate_output(packet_dir=packet_dir, output_directory=output_directory)

    report = _read_conforming_current_packet(manifest_path)
    packet = report.packet
    if packet is None:
        raise RedditConsolidationFailure("packet_unavailable", "no validated packet was available")
    if not _is_reddit_like_packet(packet):
        raise RedditConsolidationFailure(
            "ineligible_source_surface",
            "packet is not Reddit-like or old-Reddit/browser-visible HTML-like",
        )
    if _appears_contaminated(packet):
        raise RedditConsolidationFailure(
            "packet_contamination_suspected",
            "packet metadata appears to carry credential/session/profile material",
        )

    raw_file, raw_path = _resolve_raw_html_file(packet_dir=packet_dir, packet=packet)
    raw_hash = hash_file(raw_path)
    if raw_hash != raw_file.sha256:
        raise RedditConsolidationFailure(
            "raw_file_hash_mismatch",
            f"stored bytes hash mismatch for {raw_file.file_id}: manifest={raw_file.sha256} actual={raw_hash}",
        )

    html = raw_path.read_text(encoding="utf-8", errors="replace")
    try:
        parsed = parse_old_reddit_html(html)
    except RedditParseFailure as exc:
        raise RedditConsolidationFailure(exc.code, exc.message) from exc

    output_directory.mkdir(parents=True, exist_ok=True)
    json_path = output_directory / json_name
    receipt_path = output_directory / receipt_name
    for path in (json_path, receipt_path):
        if path.exists():
            raise RedditConsolidationFailure("output_exists", f"output already exists: {path}")

    artifact = _build_artifact(
        packet=packet,
        packet_dir=packet_dir,
        manifest_path=manifest_path,
        raw_file=raw_file,
        raw_hash=raw_hash,
        parsed=parsed,
    )
    json_path.write_text(json.dumps(artifact, indent=2, sort_keys=True), encoding="utf-8", newline="\n")
    receipt_path.write_text(_render_receipt(artifact), encoding="utf-8", newline="\n")
    return {
        "json_path": str(json_path),
        "receipt_path": str(receipt_path),
        "comment_count": str(len(parsed.comments)),
        "observable_comment_node_count": str(parsed.observable_comment_node_count),
    }


def build_thread_content_record(*, html_text: str, source_url: str) -> dict[str, Any]:
    """Project one old Reddit thread page into the deterministic content-packet record.

    Parse-in-flight counterpart of ``consolidate_reddit_packet``: same parser,
    but a pure function of ``(html_text, source_url)`` — no timestamps, no
    packet references, no environment reads — so ephemeral qualification can
    re-project sampled raw bytes and compare byte-for-byte against the stored
    record. Provenance lives at the packet level (the record is preserved
    inside the packet it describes); parse failures raise and are handled by
    the capture seam's raw-fallback path.
    """
    parsed = parse_old_reddit_html(html_text)
    posture_counts = Counter(comment.comment_posture for comment in parsed.comments)
    return {
        "record_kind": THREAD_CONTENT_RECORD_KIND,
        "parser_version": OLD_REDDIT_THREAD_PARSER_VERSION,
        "source_url": source_url,
        "thread": {
            "thread_id": parsed.thread_id,
            "subreddit": parsed.subreddit,
            "title": parsed.title,
            "permalink": parsed.permalink,
        },
        "post": {
            "author_state": parsed.author_state,
            "timestamp_state": parsed.timestamp_state,
            "score_state": parsed.score_state,
            "body_text": parsed.post_body_text,
        },
        "comments": [
            {
                "row_id": comment.row_id,
                "comment_id": comment.comment_id,
                "parent_id": comment.parent_id,
                "depth": comment.depth,
                "author_state": comment.author_state,
                "timestamp_state": comment.timestamp_state,
                "score_state": comment.score_state,
                "body_text": comment.body_text,
                "comment_posture": comment.comment_posture,
                "parser_warnings": comment.parser_warnings,
            }
            for comment in parsed.comments
        ],
        "counts": {
            "observable_comment_nodes": parsed.observable_comment_node_count,
            "comments_parsed": len(parsed.comments),
            "comment_postures": dict(sorted(posture_counts.items())),
        },
        "warnings": parsed.warnings,
        "limitations": parsed.limitations,
        "non_claims": NON_CLAIMS,
    }


def _read_conforming_current_packet(manifest_path: Path) -> PacketConformanceReport:
    try:
        report = read_packet_leniently(manifest_path)
    except Exception as exc:
        raise RedditConsolidationFailure("manifest_read_failure", f"manifest could not be read: {exc}") from exc
    if not report.conforms_to_current_schema:
        raise RedditConsolidationFailure(
            "manifest_nonconforming",
            f"manifest does not conform to current Source Capture schema: {len(report.current_schema_errors)} error(s)",
        )
    if not report.declares_current_manifest_version:
        raise RedditConsolidationFailure(
            "manifest_non_current_version",
            (
                f"manifest declares {report.declared_manifest_version!r}, not "
                f"{SOURCE_CAPTURE_MANIFEST_VERSION!r}"
            ),
        )
    return report


def _require_separate_output(*, packet_dir: Path, output_directory: Path) -> None:
    resolved_packet_dir = packet_dir.resolve()
    resolved_output = output_directory.resolve()
    if resolved_output == resolved_packet_dir or _is_relative_to(resolved_output, resolved_packet_dir):
        raise RedditConsolidationFailure(
            "output_inside_packet_directory",
            "derived outputs must be written outside the read-only source packet directory",
        )


def _is_reddit_like_packet(packet: SourceCapturePacket) -> bool:
    facts = [
        packet.source_family,
        packet.source_surface,
        packet.source_locator.value or "",
    ]
    return any("reddit" in item.lower() for item in facts)


def _appears_contaminated(packet: SourceCapturePacket) -> bool:
    text_parts = [
        packet.capture_context.value or "",
        packet.session_identity,
        *packet.visible_mode_changes,
        *packet.warnings,
        *packet.limitations,
    ]
    haystack = "\n".join(text_parts).lower()
    return any(marker in haystack for marker in SECRET_OR_SESSION_MARKERS)


def _resolve_raw_html_file(*, packet_dir: Path, packet: SourceCapturePacket) -> tuple[PreservedFile, Path]:
    referenced_ids = [file_id for source_slice in packet.source_slices for file_id in source_slice.preserved_file_ids]
    preserved_by_id = {item.file_id: item for item in packet.preserved_files}
    candidates = [preserved_by_id[file_id] for file_id in referenced_ids if file_id in preserved_by_id]
    for preserved_file in candidates:
        path = _resolve_preserved_path(packet_dir=packet_dir, preserved_file=preserved_file)
        if not path.exists():
            raise RedditConsolidationFailure(
                "preserved_file_path_missing",
                f"preserved file path is missing for {preserved_file.file_id}: {preserved_file.relative_packet_path}",
            )
        if _is_metadata_path(preserved_file.relative_packet_path):
            continue
        if _looks_like_html_path(preserved_file.relative_packet_path) or _sniffs_as_html(path):
            return preserved_file, path
    raise RedditConsolidationFailure("raw_html_missing", "no preserved raw HTML file could be resolved")


def _resolve_preserved_path(*, packet_dir: Path, preserved_file: PreservedFile) -> Path:
    resolved = (packet_dir / preserved_file.relative_packet_path).resolve()
    if not _is_relative_to(resolved, packet_dir.resolve()):
        raise RedditConsolidationFailure(
            "preserved_file_path_escape",
            f"preserved file escapes packet directory: {preserved_file.file_id}",
        )
    return resolved


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _is_metadata_path(relative_path: str) -> bool:
    lowered = relative_path.lower()
    return lowered.endswith("_metadata.json") or lowered.endswith("metadata.json")


def _looks_like_html_path(relative_path: str) -> bool:
    return relative_path.lower().endswith((".html", ".htm"))


def _sniffs_as_html(path: Path) -> bool:
    sample = path.read_bytes()[:512].lower()
    return b"<html" in sample or b"old reddit" in sample or b"class=\"thing" in sample


def _build_artifact(
    *,
    packet: SourceCapturePacket,
    packet_dir: Path,
    manifest_path: Path,
    raw_file: PreservedFile,
    raw_hash: str,
    parsed: Any,
) -> dict[str, Any]:
    manifest_hash = sha256_text(manifest_path.read_text(encoding="utf-8"))
    posture_counts = Counter(comment.comment_posture for comment in parsed.comments)
    return {
        "reddit_thread_consolidation": {
            "schema_version": REDDIT_THREAD_CONSOLIDATION_SCHEMA_VERSION,
            "generated_at": utc_now_z(),
            "source_packet": {
                "operator_supplied_packet_path": str(packet_dir),
                "manifest_path": str(manifest_path),
                "packet_id": packet.packet_id,
                "manifest_hash": manifest_hash,
                "raw_html_file_id": raw_file.file_id,
                "raw_html_relative_packet_path": raw_file.relative_packet_path,
                "raw_html_sha256": raw_hash,
                "source_family": packet.source_family,
                "source_surface": packet.source_surface,
                "capture_mode": packet.capture_mode.value,
                "operator_category": packet.operator_category,
                "session_identity": packet.session_identity,
            },
            "thread": {
                "thread_id": parsed.thread_id,
                "subreddit": parsed.subreddit,
                "title": parsed.title,
                "permalink": parsed.permalink,
            },
            "post": {
                "author_state": parsed.author_state,
                "timestamp_state": parsed.timestamp_state,
                "score_state": parsed.score_state,
                "body_text": parsed.post_body_text,
                "provenance": _provenance_pointer(packet_dir=packet_dir, raw_file=raw_file),
            },
            "comments": [
                _comment_to_json(comment, packet_dir=packet_dir, raw_file=raw_file)
                for comment in parsed.comments
            ],
            "counts": {
                "observable_comment_nodes": parsed.observable_comment_node_count,
                "comments_parsed": len(parsed.comments),
                "comment_postures": dict(sorted(posture_counts.items())),
            },
            "warnings": parsed.warnings,
            "limitations": parsed.limitations,
            "non_claims": NON_CLAIMS,
        }
    }


def _comment_to_json(comment: ParsedComment, *, packet_dir: Path, raw_file: PreservedFile) -> dict[str, Any]:
    return {
        "row_id": comment.row_id,
        "comment_id": comment.comment_id,
        "parent_id": comment.parent_id,
        "depth": comment.depth,
        "author_state": comment.author_state,
        "timestamp_state": comment.timestamp_state,
        "score_state": comment.score_state,
        "body_text": comment.body_text,
        "comment_posture": comment.comment_posture,
        "provenance": _provenance_pointer(packet_dir=packet_dir, raw_file=raw_file),
        "parser_warnings": comment.parser_warnings,
    }


def _provenance_pointer(*, packet_dir: Path, raw_file: PreservedFile) -> dict[str, str]:
    return {
        "packet_path": str(packet_dir),
        "raw_html_file_id": raw_file.file_id,
        "raw_html_relative_packet_path": raw_file.relative_packet_path,
    }


def _render_receipt(artifact: dict[str, Any]) -> str:
    data = artifact["reddit_thread_consolidation"]
    source = data["source_packet"]
    counts = data["counts"]
    postures = counts["comment_postures"]
    lines = [
        "# Reddit Thread Consolidation Receipt",
        "",
        f"- Packet path: `{source['operator_supplied_packet_path']}`",
        f"- Manifest path: `{source['manifest_path']}`",
        (
            f"- Raw HTML: `{source['raw_html_file_id']}` -> "
            f"`{source['raw_html_relative_packet_path']}` ({source['raw_html_sha256']})"
        ),
        f"- Thread title: {data['thread']['title'] or 'unknown_with_reason: title not visible'}",
        f"- Comments parsed: {counts['comments_parsed']}",
        f"- Observable comment nodes: {counts['observable_comment_nodes']}",
        "- Comment postures:",
    ]
    if postures:
        lines.extend(f"  - {key}: {value}" for key, value in postures.items())
    else:
        lines.append("  - none")
    lines.extend(["", "## Warnings"])
    lines.extend(_bullet_list(data["warnings"]))
    lines.extend(["", "## Limitations"])
    lines.extend(_bullet_list(data["limitations"]))
    lines.extend(["", "## Non-Claims"])
    lines.extend(_bullet_list(data["non_claims"]))
    return "\n".join(lines) + "\n"


def _bullet_list(items: list[str]) -> list[str]:
    if not items:
        return ["- none"]
    return [f"- {item}" for item in items]
