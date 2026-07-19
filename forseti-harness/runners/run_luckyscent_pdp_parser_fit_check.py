"""Parser-fit drift check for pinned Luckyscent aggregate PDP sample packets.

Exit codes: 0 all samples match; 1 drift or per-packet failure; 2 usage error.
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

from source_capture.models import SourceCapturePacket, VisibleFactStatus
from source_capture.retail_pdp_projection import (
    LUCKYSCENT_PDP_CONTENT_PROFILE,
    LUCKYSCENT_PDP_CONTENT_RECORD_KIND,
    LUCKYSCENT_PDP_PARSER_VERSION,
    LuckyscentPdpAggregateContentRecord,
    build_luckyscent_pdp_aggregate_content_record,
)


SOURCE_FAMILY = "retail_pdp"
SOURCE_SURFACE = "cloakbrowser_snapshot"


class ParserFitCheckError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def check_luckyscent_pdp_parser_fit(
    *,
    packet_or_manifest_path: Path,
) -> dict[str, Any]:
    manifest_path = (
        packet_or_manifest_path / "manifest.json"
        if packet_or_manifest_path.is_dir()
        else packet_or_manifest_path
    )
    packet_dir = manifest_path.parent
    try:
        packet = SourceCapturePacket.model_validate_json(manifest_path.read_bytes())
    except Exception as exc:
        raise ParserFitCheckError(
            "packet_shape", f"invalid packet manifest: {exc}"
        ) from exc
    if packet.source_family != SOURCE_FAMILY or packet.source_surface != SOURCE_SURFACE:
        raise ParserFitCheckError(
            "source_mismatch",
            f"unsupported source route {packet.source_family!r}/{packet.source_surface!r}",
        )

    content_path = _verified_preserved_path(
        packet=packet,
        packet_dir=packet_dir,
        filename="content_record.json",
    )
    capture_metadata_path = _verified_preserved_path(
        packet=packet,
        packet_dir=packet_dir,
        filename="content_capture_metadata.json",
    )
    browser_metadata_path = _verified_preserved_path(
        packet=packet,
        packet_dir=packet_dir,
        filename="cloakbrowser_snapshot_metadata.json",
    )
    capture_metadata = _read_object(
        capture_metadata_path, "content_capture_metadata_shape"
    )
    if capture_metadata.get("capture_artifact_mode") != "sample":
        raise ParserFitCheckError(
            "sample_required", "parser-fit checks require a sample packet"
        )
    if capture_metadata.get("parser_version") != LUCKYSCENT_PDP_PARSER_VERSION:
        raise ParserFitCheckError(
            "parser_version_mismatch",
            f"stored parser version {capture_metadata.get('parser_version')!r} "
            "does not match current",
        )
    if capture_metadata.get("projection_status") != "succeeded":
        raise ParserFitCheckError(
            "projection_not_succeeded",
            f"sample projection status is {capture_metadata.get('projection_status')!r}",
        )

    browser_metadata = _read_object(
        browser_metadata_path, "browser_metadata_shape"
    )
    profile = browser_metadata.get("retail_capture_profile")
    if (
        not isinstance(profile, dict)
        or profile.get("name") != LUCKYSCENT_PDP_CONTENT_PROFILE
    ):
        raise ParserFitCheckError(
            "profile_mismatch",
            "browser metadata does not bind luckyscent_pdp_aggregate",
        )
    if browser_metadata.get("pin_confirmed") is not True:
        raise ParserFitCheckError(
            "source_mismatch",
            "browser metadata does not confirm the Luckyscent US/USD market pin",
        )

    inputs = capture_metadata.get("inputs")
    if not isinstance(inputs, list):
        raise ParserFitCheckError(
            "content_capture_metadata_shape", "metadata inputs must be a list"
        )
    input_by_role = {
        item.get("role"): item for item in inputs if isinstance(item, dict)
    }
    raw_inputs: dict[str, bytes] = {}
    for role in ("rendered_dom", "visible_text"):
        item = input_by_role.get(role)
        if not isinstance(item, dict) or item.get("preserved") is not True:
            raise ParserFitCheckError(
                "sample_input_missing", f"sample input {role!r} is not preserved"
            )
        filename = item.get("filename")
        if not isinstance(filename, str) or not filename:
            raise ParserFitCheckError(
                "content_capture_metadata_shape",
                f"sample input {role!r} has no filename",
            )
        body = _verified_preserved_path(
            packet=packet,
            packet_dir=packet_dir,
            filename=filename,
        ).read_bytes()
        if hashlib.sha256(body).hexdigest() != item.get("sha256"):
            raise ParserFitCheckError(
                "input_hash_mismatch",
                f"sample input {role!r} hash does not match metadata",
            )
        if len(body) != item.get("byte_count"):
            raise ParserFitCheckError(
                "input_size_mismatch",
                f"sample input {role!r} byte count does not match metadata",
            )
        raw_inputs[role] = body

    stored_payload = _read_object(content_path, "content_record_shape")
    try:
        stored_record = LuckyscentPdpAggregateContentRecord.model_validate(
            stored_payload
        )
    except Exception as exc:
        raise ParserFitCheckError(
            "content_record_shape", f"stored content record is invalid: {exc}"
        ) from exc
    if stored_record.record_kind != LUCKYSCENT_PDP_CONTENT_RECORD_KIND:
        raise ParserFitCheckError(
            "content_record_shape",
            "stored content record kind is not Luckyscent aggregate PDP content",
        )
    if stored_record.parser_version != LUCKYSCENT_PDP_PARSER_VERSION:
        raise ParserFitCheckError(
            "parser_version_mismatch",
            "stored content record parser version does not match current",
        )
    if stored_record.capture_profile != LUCKYSCENT_PDP_CONTENT_PROFILE:
        raise ParserFitCheckError(
            "profile_mismatch", "stored content record profile does not match current"
        )
    slice_urls = {
        source_slice.locator.value
        for source_slice in packet.source_slices
        if source_slice.locator.status == VisibleFactStatus.KNOWN
    }
    if stored_record.source_url not in slice_urls:
        raise ParserFitCheckError(
            "source_mismatch",
            "stored content record source URL does not match a packet slice",
        )

    current = build_luckyscent_pdp_aggregate_content_record(
        rendered_dom=raw_inputs["rendered_dom"],
        visible_text=raw_inputs["visible_text"],
        source_url=stored_record.source_url,
    )
    match = current == stored_payload
    return {
        "packet_id": packet.packet_id,
        "source_surface": packet.source_surface,
        "capture_profile": stored_record.capture_profile,
        "status": "match" if match else "drift",
        "stored_parser_version": stored_record.parser_version,
        "current_parser_version": LUCKYSCENT_PDP_PARSER_VERSION,
        "difference": None if match else _diff_summary(stored_payload, current),
    }


def run_luckyscent_pdp_parser_fit_check(
    *,
    packet_paths: Sequence[Path],
) -> tuple[int, dict[str, Any]]:
    results: list[dict[str, Any]] = []
    failed = False
    for packet_path in packet_paths:
        try:
            result = check_luckyscent_pdp_parser_fit(
                packet_or_manifest_path=packet_path
            )
            failed = failed or result["status"] != "match"
            results.append(result)
        except ParserFitCheckError as exc:
            failed = True
            results.append(
                {
                    "packet": str(packet_path),
                    "status": "failure",
                    "failure_code": exc.code,
                    "message": str(exc),
                }
            )
        except Exception as exc:
            failed = True
            results.append(
                {
                    "packet": str(packet_path),
                    "status": "failure",
                    "failure_code": "unexpected_error",
                    "message": f"{type(exc).__name__}: {exc}",
                }
            )
    return (
        1 if failed else 0,
        {
            "checker": "retail_pdp_luckyscent_aggregate_parser_fit_v1",
            "parser_version": LUCKYSCENT_PDP_PARSER_VERSION,
            "results": results,
        },
    )


def _verified_preserved_path(
    *,
    packet: SourceCapturePacket,
    packet_dir: Path,
    filename: str,
) -> Path:
    matches = [
        item
        for item in packet.preserved_files
        if Path(item.relative_packet_path).name.endswith(filename)
    ]
    if len(matches) != 1:
        raise ParserFitCheckError(
            "preserved_file_mismatch",
            f"packet must preserve exactly one {filename}; found {len(matches)}",
        )
    preserved_file = matches[0]
    path = packet_dir / preserved_file.relative_packet_path
    try:
        body = path.read_bytes()
    except OSError as exc:
        raise ParserFitCheckError(
            "preserved_file_missing", f"cannot read preserved {filename}: {exc}"
        ) from exc
    if hashlib.sha256(body).hexdigest() != preserved_file.sha256:
        raise ParserFitCheckError(
            "preserved_file_hash_mismatch", f"preserved {filename} hash mismatch"
        )
    return path


def _read_object(path: Path, code: str) -> dict[str, Any]:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ParserFitCheckError(code, f"invalid JSON in {path.name}: {exc}") from exc
    if not isinstance(loaded, dict):
        raise ParserFitCheckError(code, f"{path.name} must contain a JSON object")
    return loaded


def _diff_summary(
    stored: dict[str, Any],
    current: dict[str, Any],
) -> dict[str, Any]:
    return {
        "stored_sha256": hashlib.sha256(
            json.dumps(stored, sort_keys=True).encode("utf-8")
        ).hexdigest(),
        "current_sha256": hashlib.sha256(
            json.dumps(current, sort_keys=True).encode("utf-8")
        ).hexdigest(),
        "stored_row_count": len(stored.get("rows", [])),
        "current_row_count": len(current.get("rows", [])),
    }


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check pinned Luckyscent aggregate PDP sample packet parser fit."
    )
    parser.add_argument("--packet", type=Path, action="append", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    exit_code, report = run_luckyscent_pdp_parser_fit_check(
        packet_paths=args.packet
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
