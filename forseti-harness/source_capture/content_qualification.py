"""Ephemeral qualification for deterministic capture-time content extraction.

Qualification operates only on operator-supplied scratch inputs.  It never
creates or admits a Source Capture packet.  A match deletes the disposable
scratch inputs and leaves a compact report; drift or failure preserves every
input for diagnosis.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

QUALIFICATION_REPORT_VERSION = "content_extraction_qualification_v1"


class ContentQualificationError(ValueError):
    """Fail-loud qualification error carrying a stable result code."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def qualify_rendered_content(
    *,
    scratch_root: Path,
    rendered_dom_path: Path,
    visible_text_path: Path,
    expected_content_record_path: Path,
    report_path: Path,
    extractor_version: str,
    source_url: str,
    extractor: Callable[[bytes, bytes, str], Mapping[str, Any]],
) -> tuple[int, dict[str, Any]]:
    """Compare current extraction with a retained record, then release scratch.

    The two disposable inputs and the report must live below ``scratch_root``.
    The expected record may be a copied reference outside scratch.  Only the
    two explicitly supplied disposable inputs are ever deleted.
    """
    root = scratch_root.resolve()
    dom_path = _inside(root, rendered_dom_path, "rendered DOM")
    text_path = _inside(root, visible_text_path, "visible text")
    result_path = _inside(root, report_path, "qualification report")
    if dom_path == text_path:
        raise ContentQualificationError(
            "duplicate_input_path", "rendered DOM and visible text paths must differ"
        )
    if result_path in {dom_path, text_path}:
        raise ContentQualificationError(
            "report_overlaps_input", "qualification report may not overwrite an input"
        )
    if not extractor_version.strip():
        raise ContentQualificationError(
            "extractor_version_missing", "extractor_version must be non-empty"
        )
    if not source_url.strip():
        raise ContentQualificationError("source_url_missing", "source_url must be non-empty")

    try:
        rendered_dom = dom_path.read_bytes()
        visible_text = text_path.read_bytes()
        expected_bytes = expected_content_record_path.resolve().read_bytes()
        expected = json.loads(expected_bytes)
        if not isinstance(expected, dict):
            raise ValueError("expected content record must be a JSON object")
        current = dict(extractor(rendered_dom, visible_text, source_url))
    except Exception as exc:
        report = _report(
            status="failure",
            extractor_version=extractor_version,
            source_url=source_url,
            inputs=_available_input_rows(dom_path, text_path),
            failure_code="qualification_input_or_extraction_failure",
            message=f"{type(exc).__name__}: {exc}",
        )
        _write_report(result_path, report)
        return 1, report

    matches = current == expected
    report = _report(
        status="match" if matches else "drift",
        extractor_version=extractor_version,
        source_url=source_url,
        inputs=_input_rows(dom_path, text_path),
        expected_sha256=hashlib.sha256(expected_bytes).hexdigest(),
        current_sha256=hashlib.sha256(_canonical_bytes(current)).hexdigest(),
        changed_top_level_keys=(
            []
            if matches
            else sorted(
                key
                for key in set(expected) | set(current)
                if expected.get(key) != current.get(key)
            )
        ),
    )
    _write_report(result_path, report)
    if matches:
        dom_path.unlink()
        text_path.unlink()
    return (0 if matches else 1), report


def _inside(root: Path, path: Path, label: str) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(root):
        raise ContentQualificationError(
            "scratch_boundary_violation", f"{label} must live below scratch_root"
        )
    return resolved


def _input_rows(dom_path: Path, text_path: Path) -> list[dict[str, Any]]:
    return [_input_row("rendered_dom", dom_path), _input_row("visible_text", text_path)]


def _available_input_rows(dom_path: Path, text_path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for role, path in (("rendered_dom", dom_path), ("visible_text", text_path)):
        if path.is_file():
            rows.append(_input_row(role, path))
        else:
            rows.append({"role": role, "filename": path.name, "status": "missing"})
    return rows


def _input_row(role: str, path: Path) -> dict[str, Any]:
    body = path.read_bytes()
    return {
        "role": role,
        "filename": path.name,
        "sha256": hashlib.sha256(body).hexdigest(),
        "byte_count": len(body),
    }


def _report(
    *,
    status: str,
    extractor_version: str,
    source_url: str,
    inputs: list[dict[str, Any]],
    **extra: Any,
) -> dict[str, Any]:
    return {
        "schema_version": QUALIFICATION_REPORT_VERSION,
        "status": status,
        "extractor_version": extractor_version,
        "source_url": source_url,
        "inputs": inputs,
        **extra,
    }


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _write_report(path: Path, report: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


__all__ = [
    "ContentQualificationError",
    "QUALIFICATION_REPORT_VERSION",
    "qualify_rendered_content",
]
