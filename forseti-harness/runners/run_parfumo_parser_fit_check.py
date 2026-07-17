"""Parser-fit drift check for pinned-route Parfumo sample packets.

Sample mode preserves rendered DOM, visible text, and the capture-time content
record in one packet. This checker validates the packet's provenance metadata,
re-runs the current deterministic parser, and compares the complete record.

Exit codes: 0 all samples match; 1 drift or per-packet failure; 2 usage error.
The check is read-only and makes no readiness or corpus-completeness claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.models import SOURCE_CAPTURE_MANIFEST_VERSION
from source_capture.packet_inspection import read_packet_leniently
from source_capture.parfumo_projection import (
    PARFUMO_TARGETED_CONTENT_RECORD_KIND,
    PARFUMO_TARGETED_PARSER_VERSION,
    PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE,
    ParfumoTargetedContentRecord,
    build_parfumo_targeted_content_record,
)
from source_capture.source_quality import resolve_manifest_path

SOURCE_FAMILY = "fragrance_native_database"


class ParserFitCheckError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def check_parfumo_parser_fit(*, packet_or_manifest_path: Path) -> dict[str, Any]:
    manifest_path = resolve_manifest_path(packet_or_manifest_path).resolve()
    try:
        report = read_packet_leniently(manifest_path)
    except Exception as exc:
        raise ParserFitCheckError(
            "manifest_read_failure",
            f"manifest could not be read: {exc}",
        ) from exc
    if not report.conforms_to_current_schema or not report.declares_current_manifest_version:
        raise ParserFitCheckError(
            "manifest_nonconforming",
            f"manifest is not a current {SOURCE_CAPTURE_MANIFEST_VERSION!r} packet",
        )
    packet = report.packet
    if packet is None:
        raise ParserFitCheckError("packet_unavailable", "no validated packet was available")
    if packet.source_family != SOURCE_FAMILY:
        raise ParserFitCheckError(
            "ineligible_source_family",
            f"expected {SOURCE_FAMILY!r}, got {packet.source_family!r}",
        )
    if packet.source_surface != PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE:
        raise ParserFitCheckError(
            "ineligible_source_surface",
            f"expected {PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE!r}, "
            f"got {packet.source_surface!r}",
        )

    packet_dir = manifest_path.parent
    content_path = _verified_preserved_path(
        packet=packet,
        packet_dir=packet_dir,
        file_name="content_record.json",
    )
    metadata_path = _verified_preserved_path(
        packet=packet,
        packet_dir=packet_dir,
        file_name="content_capture_metadata.json",
    )
    metadata = _read_json_object(
        metadata_path,
        code="content_capture_metadata_shape",
        label="content capture metadata",
    )
    if metadata.get("capture_artifact_mode") != "sample":
        raise ParserFitCheckError(
            "ineligible_capture_mode",
            "parser-fit checks require a sample packet",
        )
    if metadata.get("parser_version") != PARFUMO_TARGETED_PARSER_VERSION:
        raise ParserFitCheckError(
            "parser_version_mismatch",
            f"stored parser version {metadata.get('parser_version')!r} does not match "
            f"current {PARFUMO_TARGETED_PARSER_VERSION!r}",
        )
    if metadata.get("projection_status") != "succeeded":
        raise ParserFitCheckError(
            "projection_not_succeeded",
            f"sample projection status is {metadata.get('projection_status')!r}",
        )

    input_rows = metadata.get("inputs")
    if not isinstance(input_rows, list):
        raise ParserFitCheckError(
            "content_capture_metadata_shape",
            "content capture metadata inputs must be a list",
        )
    inputs_by_role: dict[str, dict[str, Any]] = {}
    for item in input_rows:
        if not isinstance(item, dict) or not isinstance(item.get("role"), str):
            raise ParserFitCheckError(
                "content_capture_metadata_shape",
                "content capture metadata input rows must be objects with role",
            )
        inputs_by_role[item["role"]] = item

    raw_inputs: dict[str, bytes] = {}
    for role in ("rendered_dom", "visible_text"):
        item = inputs_by_role.get(role)
        if item is None:
            raise ParserFitCheckError(
                "projector_input_missing",
                f"sample metadata carries no {role!r} input",
            )
        if item.get("preserved") is not True:
            raise ParserFitCheckError(
                "projector_input_not_preserved",
                f"sample input {role!r} is not marked preserved",
            )
        filename = item.get("filename")
        if not isinstance(filename, str) or not filename:
            raise ParserFitCheckError(
                "content_capture_metadata_shape",
                f"sample input {role!r} has no filename",
            )
        path = _verified_preserved_path(
            packet=packet,
            packet_dir=packet_dir,
            file_name=filename,
        )
        body = path.read_bytes()
        if item.get("sha256") != hashlib.sha256(body).hexdigest():
            raise ParserFitCheckError(
                "projector_input_hash_mismatch",
                f"sample input {role!r} sha256 does not match metadata",
            )
        if item.get("byte_count") != len(body):
            raise ParserFitCheckError(
                "projector_input_size_mismatch",
                f"sample input {role!r} byte count does not match metadata",
            )
        raw_inputs[role] = body

    stored_loaded = _read_json_object(
        content_path,
        code="content_record_shape",
        label="stored content record",
    )
    try:
        stored_record = ParfumoTargetedContentRecord.model_validate(stored_loaded)
    except Exception as exc:
        raise ParserFitCheckError(
            "content_record_shape",
            f"stored content record is invalid: {exc}",
        ) from exc
    if stored_record.record_kind != PARFUMO_TARGETED_CONTENT_RECORD_KIND:
        raise ParserFitCheckError(
            "content_record_shape",
            f"stored record kind is {stored_record.record_kind!r}",
        )
    if stored_record.parser_version != PARFUMO_TARGETED_PARSER_VERSION:
        raise ParserFitCheckError(
            "parser_version_mismatch",
            f"stored content parser version {stored_record.parser_version!r} does not match current",
        )
    source_url = packet.source_locator.value
    if not isinstance(source_url, str) or not source_url:
        raise ParserFitCheckError(
            "source_locator_missing",
            "packet source locator is not a known non-empty URL",
        )
    if stored_record.source_url != source_url:
        raise ParserFitCheckError(
            "source_url_mismatch",
            f"stored source_url {stored_record.source_url!r} does not match packet locator",
        )

    current_record = build_parfumo_targeted_content_record(
        rendered_dom=raw_inputs["rendered_dom"],
        visible_text=raw_inputs["visible_text"],
        source_url=source_url,
    )
    stored_dict = stored_record.model_dump(mode="json")
    drift = current_record != stored_dict
    return {
        "manifest_path": str(manifest_path),
        "source_family": packet.source_family,
        "source_surface": packet.source_surface,
        "stored_parser_version": stored_record.parser_version,
        "current_parser_version": PARFUMO_TARGETED_PARSER_VERSION,
        "status": "drift" if drift else "match",
        "diff_summary": _diff_summary(stored_dict, current_record) if drift else None,
    }


def run_parfumo_parser_fit_check(*, packet_paths: Sequence[Path]) -> tuple[int, dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    failures = 0
    for packet_path in packet_paths:
        try:
            row = check_parfumo_parser_fit(packet_or_manifest_path=packet_path)
            if row["status"] != "match":
                failures += 1
        except ParserFitCheckError as exc:
            failures += 1
            row = {
                "manifest_path": str(packet_path),
                "status": "error",
                "error_code": exc.code,
                "error": exc.message,
            }
        rows.append(row)
    return (
        1 if failures else 0,
        {
            "checker": "parfumo_targeted_parser_fit_v1",
            "packet_count": len(rows),
            "failure_count": failures,
            "results": rows,
        },
    )


def _verified_preserved_path(*, packet, packet_dir: Path, file_name: str) -> Path:
    matches = [
        item
        for item in packet.preserved_files
        if item.relative_packet_path.replace("\\", "/").endswith(file_name)
    ]
    if len(matches) != 1:
        raise ParserFitCheckError(
            "preserved_file_missing_or_ambiguous",
            f"expected exactly one preserved file ending in {file_name!r}, got {len(matches)}",
        )
    item = matches[0]
    path = packet_dir / item.relative_packet_path
    if not path.is_file():
        raise ParserFitCheckError(
            "preserved_file_missing",
            f"preserved file is missing: {item.relative_packet_path}",
        )
    body = path.read_bytes()
    if hashlib.sha256(body).hexdigest() != item.sha256:
        raise ParserFitCheckError(
            "preserved_file_hash_mismatch",
            f"preserved file hash does not match manifest: {item.relative_packet_path}",
        )
    return path


def _read_json_object(path: Path, *, code: str, label: str) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ParserFitCheckError(code, f"{label} could not be read: {exc}") from exc
    if not isinstance(loaded, dict):
        raise ParserFitCheckError(code, f"{label} must be a JSON object")
    return loaded


def _diff_summary(stored: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    keys = sorted(set(stored) | set(current))
    changed = [key for key in keys if stored.get(key) != current.get(key)]
    return {"changed_top_level_keys": changed}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check Parfumo sample packet parser fit.")
    parser.add_argument("--packet", type=Path, action="append", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    exit_code, report = run_parfumo_parser_fit_check(packet_paths=args.packet)
    print(json.dumps(report, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
