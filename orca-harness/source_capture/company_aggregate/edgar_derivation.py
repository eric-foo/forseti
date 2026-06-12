"""Layer-2 derivation: a verified EDGAR capture packet -> one EdgarHeadcountObservation (slice 04b).

The "wire-up" between the captured filing (Layer 1) and the immutable observation shape
(Layer 2a, ``observation.py``). It reads a *current-schema, conformance-checked*
``SourceCapturePacket``, RE-VERIFIES the preserved primary-filing bytes against the manifest
``sha256`` before trusting them, runs the deterministic employee-count extractor over the decoded
filing text, and assembles an ``EdgarHeadcountObservation``.

It copies the safety contract of ``reddit_consolidation.consolidator`` exactly:
resolve manifest -> conformance gate -> current-manifest-version gate -> path-escape guard ->
``hash_file`` re-verify -> derive OUTSIDE the immutable packet. "Outside" is automatic here: the
observation is returned in-memory and this module NEVER writes into, or mutates, the packet
directory (persistence, the append-only series, and the entity projection are later slices).

It carries NO entity identity. The observation key is filing-fact-only (``source, cik,
accession_number, period_of_report``); resolving a CIK/filer to a canonical company is the unbuilt
entity spine's job (the #1 ownership boundary), and even the later projection emits only a
``provisional_filer_key`` + ``resolution_state``, never a canonical ``entity_key``.

``filing_date`` is NOT yet carried by the capture adapter slice (a deferred enrichment; the packet
records it as a sentinel), so the caller supplies it (the discovery layer / operator). Everything
else -- ``cik`` / ``accession_number`` / ``period_of_report`` / ``form_type`` -- is read from the
packet ``capture_context``.
"""
from __future__ import annotations

import json
from pathlib import Path

from harness_utils import generate_ulid, sha256_bytes, sha256_text, utc_now_z
from source_capture.company_aggregate.edgar_extraction import (
    PARSER_METHOD,
    PARSER_VERSION,
    RULESET_SHA256,
    extract_employee_count,
    extraction_to_measure_facts,
)
from source_capture.company_aggregate.observation import (
    EDGAR_SOURCE,
    EdgarHeadcountObservation,
    EdgarObservationKey,
    ExtractionProvenance,
    ExtractionSpan,
)
from source_capture.models import SOURCE_CAPTURE_MANIFEST_VERSION, PreservedFile, SourceCapturePacket
from source_capture.packet_inspection import PacketConformanceReport, read_packet_leniently
from source_capture.source_quality import resolve_manifest_path

# Span sentinel: when no single trustworthy count is read (not-found or ambiguous), there is no
# read location, but the model requires a span. We record a degenerate 0..0 span that still binds
# the source file (source_sha256) and carries a deterministic marker, so the absence is auditable
# and re-derivable -- never a fabricated location.
_NO_SPAN_MARKER = "(no single extracted span; see employee_count reason)"

OBSERVATION_NON_CLAIMS = [
    "narrative-extracted employee count from one 10-K Item-1 text; EDGAR exposes no structured count",
    "raw observation; not validated, not ECR-ready until rebound under a Decision Frame",
    "no entity identity; a filer-keyed source fact, not a canonical-company or cross-company claim",
    "cross-year / cross-company comparability NOT established",
    "not Cleaning, ECR, or Judgment design",
]


class EdgarDerivationFailure(ValueError):
    """A typed, operationally-honest derivation failure (mirrors RedditConsolidationFailure)."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def derive_edgar_headcount_observation(
    *,
    packet_or_manifest_path: Path,
    filing_date: str,
    run_id: str | None = None,
    derived_at: str | None = None,
) -> EdgarHeadcountObservation:
    """Derive one immutable headcount observation from a verified EDGAR capture packet.

    ``filing_date`` is caller-supplied (the capture adapter slice does not yet carry it). ``run_id``
    / ``derived_at`` are audit metadata only -- never identity, never inputs to the value -- and
    default to a fresh ULID / current UTC; pass them for deterministic derivation.
    """
    if not filing_date.strip():
        raise EdgarDerivationFailure("filing_date_required", "filing_date must be a non-empty string")

    manifest_path = resolve_manifest_path(packet_or_manifest_path)
    packet_dir = manifest_path.parent

    report = _read_conforming_current_packet(manifest_path)
    packet = report.packet
    if packet is None:  # defensive: a conforming report always carries a packet
        raise EdgarDerivationFailure("packet_unavailable", "no validated packet was available")
    if packet.source_family != EDGAR_SOURCE:
        raise EdgarDerivationFailure(
            "ineligible_source_surface",
            f"packet source_family is {packet.source_family!r}, not {EDGAR_SOURCE!r}",
        )

    metadata = _read_edgar_metadata(packet)
    preserved_file, raw_path, evidence_slice_id = _resolve_primary_filing(
        packet_dir=packet_dir, packet=packet, primary_document=metadata["primary_document"]
    )

    # Read the preserved bytes ONCE, then hash AND decode those same bytes (F-05): verification
    # and extraction must bind to identical bytes -- a second read could see a mutated file
    # (TOCTOU) and parse bytes that were never the verified bytes.
    raw_bytes = raw_path.read_bytes()
    actual_hash = sha256_bytes(raw_bytes)
    if actual_hash != preserved_file.sha256:
        raise EdgarDerivationFailure(
            "source_file_hash_mismatch",
            f"stored-bytes hash mismatch for {preserved_file.file_id}: "
            f"manifest={preserved_file.sha256} actual={actual_hash}",
        )

    text = raw_bytes.decode("utf-8", errors="replace")
    extraction = extract_employee_count(text)
    employee_count, count_int, value_quality, measurement_basis = extraction_to_measure_facts(extraction)

    span = _build_span(extraction=extraction, preserved_file=preserved_file, source_sha256=actual_hash)
    provenance = ExtractionProvenance(
        parser_method=PARSER_METHOD,
        parser_version=PARSER_VERSION,
        ruleset_sha256=RULESET_SHA256,
        run_id=run_id or generate_ulid(),
        derived_at=derived_at or utc_now_z(),
    )

    limitations = [
        "filing_date supplied by caller; the capture adapter slice does not yet carry it (deferred enrichment)",
        "extraction runs over the decoded filing text (utf-8, errors='replace'); v0 does not normalize HTML structure",
    ]
    if extraction.quality == "ambiguous":
        limitations.append(f"ambiguous extraction; no single trustworthy count: {extraction.reason}")
    elif not extraction.found:
        limitations.append(f"no employee count extracted: {extraction.reason}")

    return EdgarHeadcountObservation(
        key=EdgarObservationKey(
            source=EDGAR_SOURCE,
            cik=metadata["cik"],
            accession_number=metadata["accession_number"],
            period_of_report=metadata["period_of_report"],
        ),
        form_type=metadata["form_type"],
        filing_date=filing_date,
        employee_count=employee_count,
        employee_count_int=count_int,
        value_quality=value_quality,
        measurement_basis=measurement_basis,
        extraction_span=span,
        extraction=provenance,
        supersedes=None,
        packet_id=packet.packet_id,
        evidence_slice_id=evidence_slice_id,
        manifest_sha256=sha256_text(manifest_path.read_text(encoding="utf-8")),
        alternates=list(extraction.alternates),
        limitations=limitations,
        non_claims=list(OBSERVATION_NON_CLAIMS),
    )


def _read_conforming_current_packet(manifest_path: Path) -> PacketConformanceReport:
    try:
        report = read_packet_leniently(manifest_path)
    except Exception as exc:
        raise EdgarDerivationFailure("manifest_read_failure", f"manifest could not be read: {exc}") from exc
    if not report.conforms_to_current_schema:
        raise EdgarDerivationFailure(
            "manifest_nonconforming",
            f"manifest does not conform to the current Source Capture schema: "
            f"{len(report.current_schema_errors)} error(s)",
        )
    if not report.declares_current_manifest_version:
        raise EdgarDerivationFailure(
            "manifest_non_current_version",
            f"manifest declares {report.declared_manifest_version!r}, not {SOURCE_CAPTURE_MANIFEST_VERSION!r}",
        )
    return report


def _read_edgar_metadata(packet: SourceCapturePacket) -> dict[str, str]:
    try:
        raw = json.loads(packet.capture_context.value or "")
    except (TypeError, ValueError) as exc:
        raise EdgarDerivationFailure("capture_context_unreadable", f"capture_context is not JSON: {exc}") from exc
    if not isinstance(raw, dict):
        raise EdgarDerivationFailure("capture_context_unreadable", "capture_context did not decode to an object")

    metadata: dict[str, str] = {}
    for field in ("cik", "accession_number", "period_of_report", "form_type", "primary_document"):
        value = raw.get(field)
        if not isinstance(value, str) or not value.strip():
            raise EdgarDerivationFailure(
                "capture_context_unreadable",
                f"capture_context is missing a non-empty {field!r}",
            )
        metadata[field] = value
    return metadata


def _resolve_primary_filing(
    *, packet_dir: Path, packet: SourceCapturePacket, primary_document: str
) -> tuple[PreservedFile, Path, str]:
    preserved_by_id = {item.file_id: item for item in packet.preserved_files}
    candidates: list[tuple[PreservedFile, str]] = []
    for source_slice in packet.source_slices:
        for file_id in source_slice.preserved_file_ids:
            preserved_file = preserved_by_id.get(file_id)
            if preserved_file is not None:
                candidates.append((preserved_file, source_slice.slice_id))

    # Prefer the preserved file whose path carries the primary document name; for an EDGAR packet
    # (exactly one preserved primary filing) fall back to the lone candidate.
    chosen = next(
        (pair for pair in candidates if pair[0].relative_packet_path.endswith(primary_document)),
        candidates[0] if len(candidates) == 1 else None,
    )
    if chosen is None:
        raise EdgarDerivationFailure(
            "primary_filing_unresolved",
            f"could not resolve the preserved primary filing {primary_document!r} among "
            f"{len(candidates)} referenced preserved file(s)",
        )

    preserved_file, slice_id = chosen
    raw_path = _resolve_preserved_path(packet_dir=packet_dir, preserved_file=preserved_file)
    if not raw_path.exists():
        raise EdgarDerivationFailure(
            "preserved_file_path_missing",
            f"preserved file path is missing for {preserved_file.file_id}: {preserved_file.relative_packet_path}",
        )
    return preserved_file, raw_path, slice_id


def _resolve_preserved_path(*, packet_dir: Path, preserved_file: PreservedFile) -> Path:
    resolved = (packet_dir / preserved_file.relative_packet_path).resolve()
    if not _is_relative_to(resolved, packet_dir.resolve()):
        raise EdgarDerivationFailure(
            "preserved_file_path_escape",
            f"preserved file escapes the packet directory: {preserved_file.file_id}",
        )
    return resolved


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _build_span(
    *, extraction, preserved_file: PreservedFile, source_sha256: str
) -> ExtractionSpan:
    if extraction.found and extraction.char_start is not None and extraction.char_end is not None:
        matched = extraction.matched_text or ""
        return ExtractionSpan(
            preserved_file_id=preserved_file.file_id,
            relative_packet_path=preserved_file.relative_packet_path,
            source_sha256=source_sha256,
            locator_kind="char_offset_range",
            char_start=extraction.char_start,
            char_end=extraction.char_end,
            excerpt_sha256=sha256_text(matched),
            matched_text=matched,
        )
    # No single trustworthy span: degenerate 0..0 span that still binds the source file.
    return ExtractionSpan(
        preserved_file_id=preserved_file.file_id,
        relative_packet_path=preserved_file.relative_packet_path,
        source_sha256=source_sha256,
        locator_kind="char_offset_range",
        char_start=0,
        char_end=0,
        excerpt_sha256=sha256_text(_NO_SPAN_MARKER),
        matched_text=_NO_SPAN_MARKER,
    )
