"""Lenient, honest read-back for inspecting Source Capture packet manifests.

Phase-1 of the packet schema-evolution architecture (the lenient-read slice).

The strict ``SourceCapturePacket`` model is the single source of truth for "what
conforms to the current schema." This module reuses it as a *probe*: it runs
``model_validate`` inside ``try/except ValidationError`` and reports the verdict
instead of crashing on it. It NEVER hand-rebuilds the schema (no second source of
truth to drift), and it NEVER returns a ``SourceCapturePacket`` for a
non-conforming manifest — it returns a distinct ``PacketConformanceReport`` so no
caller can mistake an inspection note for a validated packet.

It is version-*aware* (it reads and reports ``manifest_version``) but does NOT
dispatch to per-version schemas: with no frozen historical model, it can only
report current-schema conformance + declared-version facts, never whether a
packet matches its own declared (non-current) shape. See
``docs/product/source_capture_packet_schema_evolution_architecture_v0.md``
(AR-01 binding amendment).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from schemas.case_models import StrictModel
from source_capture.models import SOURCE_CAPTURE_MANIFEST_VERSION, SourceCapturePacket


# Sentinel for the declared-version shape check that Phase-1 cannot perform: with no
# frozen per-version model, a packet that declares a non-current version cannot be
# validated against the shape it claims (AR-01). Only current-schema conformance is
# knowable here.
NOT_AVAILABLE_WITHOUT_PER_VERSION_SCHEMA = "not_available_without_per_version_schema"


class ConformanceError(StrictModel):
    """One current-schema conformance failure, projected from a pydantic error.

    Carries only location/type/message — pydantic's ``input`` (raw value) and
    ``url`` are dropped so the report never leaks packet content or volatile data.
    """

    loc: str
    type: str
    msg: str


class PacketConformanceReport(StrictModel):
    """Distinct inspection result — never a validated packet.

    ``packet`` is populated ONLY when ``conforms_to_current_schema`` is True; a
    caller that wants a validated packet must branch on conformance and cannot be
    handed a half-built one.
    """

    declared_manifest_version: str | None
    declares_current_manifest_version: bool
    conforms_to_current_schema: bool
    current_schema_errors: list[ConformanceError]
    declared_version_shape_validation: str | None
    packet: SourceCapturePacket | None = None


def _project_errors(error: ValidationError) -> list[ConformanceError]:
    projected: list[ConformanceError] = []
    for item in error.errors():
        loc = ".".join(str(part) for part in item.get("loc", ()))
        projected.append(
            ConformanceError(
                loc=loc,
                type=str(item.get("type", "")),
                msg=str(item.get("msg", "")),
            )
        )
    return projected


def inspect_packet_manifest(raw_manifest: dict[str, Any]) -> PacketConformanceReport:
    """Inspect an already-parsed manifest dict; report conformance, never raise on schema skew.

    Reuses ``SourceCapturePacket.model_validate`` as the conformance probe. Only
    ``ValidationError`` is caught — any other exception (a real bug in the model or
    this reader) propagates rather than being laundered into a false "non-conforming".
    """
    declared = raw_manifest.get("manifest_version")
    declared_version = declared if isinstance(declared, str) else None
    declares_current = declared_version == SOURCE_CAPTURE_MANIFEST_VERSION
    # Function of the declared version only: if it does not declare the current
    # version, we cannot validate the shape it claims (no per-version model), even
    # if it happens to satisfy the current schema.
    declared_version_shape_validation = (
        None if declares_current else NOT_AVAILABLE_WITHOUT_PER_VERSION_SCHEMA
    )

    try:
        packet = SourceCapturePacket.model_validate(raw_manifest)
    except ValidationError as exc:
        return PacketConformanceReport(
            declared_manifest_version=declared_version,
            declares_current_manifest_version=declares_current,
            conforms_to_current_schema=False,
            current_schema_errors=_project_errors(exc),
            declared_version_shape_validation=declared_version_shape_validation,
            packet=None,
        )

    return PacketConformanceReport(
        declared_manifest_version=declared_version,
        declares_current_manifest_version=declares_current,
        conforms_to_current_schema=True,
        current_schema_errors=[],
        declared_version_shape_validation=declared_version_shape_validation,
        packet=packet,
    )


def read_packet_leniently(manifest_path: Path) -> PacketConformanceReport:
    """Read + inspect a manifest file.

    Raises for a genuinely unreadable manifest (missing file, invalid JSON, or a
    non-object JSON document) so the caller can keep treating those as
    missing/uninspectable. Returns a report for any manifest that parses to a JSON
    object — including one that does not conform to the current schema.
    """
    raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"manifest is not a JSON object: {manifest_path}")
    return inspect_packet_manifest(raw)
