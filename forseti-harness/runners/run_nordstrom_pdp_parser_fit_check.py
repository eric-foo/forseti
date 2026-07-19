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
    NORDSTROM_PDP_CONTENT_PROFILE,
    NORDSTROM_PDP_PARSER_VERSION,
    NordstromPdpAggregateContentRecord,
    build_nordstrom_pdp_aggregate_content_record,
)


class ParserFitCheckError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def check_nordstrom_pdp_parser_fit(
    *,
    packet_or_manifest_path: Path,
) -> dict[str, Any]:
    packet_directory = (
        packet_or_manifest_path.parent
        if packet_or_manifest_path.name == "manifest.json"
        else packet_or_manifest_path
    )
    manifest_path = packet_directory / "manifest.json"
    try:
        manifest_payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        packet = SourceCapturePacket.model_validate(manifest_payload)
    except Exception as exc:
        raise ParserFitCheckError(
            "manifest_invalid", f"invalid packet manifest: {exc}"
        ) from exc

    bodies: dict[str, bytes] = {}
    files_by_name = {}
    root = packet_directory.resolve()
    for preserved in packet.preserved_files:
        candidate = (root / preserved.relative_packet_path).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise ParserFitCheckError(
                "preserved_path_invalid",
                f"preserved file escapes packet directory: {preserved.file_id}",
            ) from exc
        try:
            body = candidate.read_bytes()
        except OSError as exc:
            raise ParserFitCheckError(
                "preserved_file_missing",
                f"preserved file is unreadable: {preserved.file_id}: {exc}",
            ) from exc
        if len(body) != preserved.size_bytes or hashlib.sha256(body).hexdigest() != preserved.sha256:
            raise ParserFitCheckError(
                "preserved_file_mismatch",
                f"preserved file size/hash mismatch: {preserved.file_id}",
            )
        logical_name = Path(
            preserved.relative_packet_path.replace("\\", "/")
        ).name
        if len(logical_name) > 3 and logical_name[:2].isdigit() and logical_name[2] == "_":
            logical_name = logical_name[3:]
        if logical_name in files_by_name:
            raise ParserFitCheckError(
                "preserved_file_ambiguous",
                f"multiple preserved files map to {logical_name}",
            )
        files_by_name[logical_name] = preserved
        bodies[logical_name] = body

    required = {
        "cloakbrowser_rendered_dom.html",
        "cloakbrowser_visible_text.txt",
        "cloakbrowser_snapshot_metadata.json",
        "content_record.json",
        "content_capture_metadata.json",
    }
    missing = sorted(required - bodies.keys())
    if missing:
        raise ParserFitCheckError(
            "sample_required",
            "Nordstrom parser-fit requires a sample packet with: "
            + ", ".join(missing),
        )

    capture_metadata = _json_object(
        bodies["content_capture_metadata.json"],
        code="content_metadata_shape",
        label="content_capture_metadata.json",
    )
    if capture_metadata.get("capture_artifact_mode") != "sample":
        raise ParserFitCheckError(
            "sample_required", "Nordstrom parser-fit accepts sample packets only"
        )
    if capture_metadata.get("parser_version") != NORDSTROM_PDP_PARSER_VERSION:
        raise ParserFitCheckError(
            "parser_version_mismatch",
            "stored Nordstrom parser version does not match current",
        )
    if capture_metadata.get("projection_status") != "succeeded":
        raise ParserFitCheckError(
            "projection_status",
            "stored Nordstrom projection status is not succeeded",
        )
    _validate_input_receipts(capture_metadata, bodies)

    browser_metadata = _json_object(
        bodies["cloakbrowser_snapshot_metadata.json"],
        code="browser_metadata_shape",
        label="cloakbrowser_snapshot_metadata.json",
    )
    profile = browser_metadata.get("retail_capture_profile")
    if (
        not isinstance(profile, dict)
        or profile.get("name") != NORDSTROM_PDP_CONTENT_PROFILE
    ):
        raise ParserFitCheckError(
            "profile_mismatch", "packet does not use the Nordstrom aggregate profile"
        )
    if browser_metadata.get("pin_confirmed") is not True:
        raise ParserFitCheckError(
            "market_pin_mismatch",
            "packet does not carry a confirmed Nordstrom US/USD storefront pin",
        )

    try:
        stored_record = NordstromPdpAggregateContentRecord.model_validate_json(
            bodies["content_record.json"]
        )
    except Exception as exc:
        raise ParserFitCheckError(
            "content_record_shape", f"invalid Nordstrom content record: {exc}"
        ) from exc
    source_urls = {
        source_slice.locator.value
        for source_slice in packet.source_slices
        if source_slice.locator.status == VisibleFactStatus.KNOWN
    }
    if stored_record.source_url not in source_urls:
        raise ParserFitCheckError(
            "source_mismatch",
            "content record source_url does not match a packet slice locator",
        )

    current_payload = build_nordstrom_pdp_aggregate_content_record(
        rendered_dom=bodies["cloakbrowser_rendered_dom.html"],
        visible_text=bodies["cloakbrowser_visible_text.txt"],
        source_url=stored_record.source_url,
    )
    stored_payload = stored_record.model_dump(mode="json")
    stored_sha256 = _canonical_sha256(stored_payload)
    current_sha256 = _canonical_sha256(current_payload)
    if stored_payload != current_payload:
        return {
            "status": "drift",
            "packet_id": packet.packet_id,
            "stored_parser_version": stored_record.parser_version,
            "current_parser_version": NORDSTROM_PDP_PARSER_VERSION,
            "difference": {
                "path": _first_difference_path(stored_payload, current_payload),
                "stored_sha256": stored_sha256,
                "current_sha256": current_sha256,
            },
        }
    return {
        "status": "match",
        "packet_id": packet.packet_id,
        "stored_parser_version": stored_record.parser_version,
        "current_parser_version": NORDSTROM_PDP_PARSER_VERSION,
        "content_sha256": current_sha256,
    }


def run_nordstrom_pdp_parser_fit_check(
    *,
    packet_paths: Sequence[Path],
) -> tuple[int, dict[str, Any]]:
    results: list[dict[str, Any]] = []
    failed = False
    for path in packet_paths:
        try:
            result = check_nordstrom_pdp_parser_fit(
                packet_or_manifest_path=path
            )
            if result["status"] != "match":
                failed = True
        except ParserFitCheckError as exc:
            failed = True
            result = {
                "status": "failure",
                "error_code": exc.code,
                "message": str(exc),
            }
        results.append({"path": str(path), **result})
    return (1 if failed else 0), {"results": results}


def _validate_input_receipts(
    metadata: dict[str, Any],
    bodies: dict[str, bytes],
) -> None:
    inputs = metadata.get("inputs")
    if not isinstance(inputs, list):
        raise ParserFitCheckError(
            "content_metadata_shape", "content metadata inputs must be a list"
        )
    by_role = {
        item.get("role"): item for item in inputs if isinstance(item, dict)
    }
    for role, filename in (
        ("rendered_dom", "cloakbrowser_rendered_dom.html"),
        ("visible_text", "cloakbrowser_visible_text.txt"),
    ):
        receipt = by_role.get(role)
        body = bodies[filename]
        if (
            not isinstance(receipt, dict)
            or receipt.get("filename") != filename
            or receipt.get("preserved") is not True
            or receipt.get("byte_count") != len(body)
            or receipt.get("sha256") != hashlib.sha256(body).hexdigest()
        ):
            raise ParserFitCheckError(
                "input_hash_mismatch",
                f"content metadata does not match preserved {role} bytes",
            )


def _json_object(body: bytes, *, code: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(body)
    except Exception as exc:
        raise ParserFitCheckError(code, f"invalid {label}: {exc}") from exc
    if not isinstance(value, dict):
        raise ParserFitCheckError(code, f"{label} must contain a JSON object")
    return value


def _canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _first_difference_path(left: object, right: object, path: str = "") -> str:
    if type(left) is not type(right):
        return path or "/"
    if isinstance(left, dict):
        keys = sorted(set(left) | set(right))
        for key in keys:
            child = f"{path}/{_json_pointer_token(str(key))}"
            if key not in left or key not in right:
                return child
            difference = _first_difference_path(left[key], right[key], child)
            if difference:
                return difference
        return ""
    if isinstance(left, list):
        for index in range(max(len(left), len(right))):
            child = f"{path}/{index}"
            if index >= len(left) or index >= len(right):
                return child
            difference = _first_difference_path(left[index], right[index], child)
            if difference:
                return difference
        return ""
    return "" if left == right else (path or "/")


def _json_pointer_token(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check Nordstrom aggregate sample packets for parser drift."
    )
    parser.add_argument("packet", nargs="+", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    exit_code, report = run_nordstrom_pdp_parser_fit_check(
        packet_paths=args.packet
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "ParserFitCheckError",
    "check_nordstrom_pdp_parser_fit",
    "run_nordstrom_pdp_parser_fit_check",
]
