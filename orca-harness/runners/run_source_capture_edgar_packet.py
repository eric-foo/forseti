"""EDGAR packet runner -- translate an EdgarFilingSuccess into a full-filing SourceCapturePacket.

The "last mile" for the EDGAR capture path: take the adapter's ``EdgarFilingSuccess`` (the FULL
primary-document bytes + structured filing metadata) and write a ``SourceCapturePacket`` that
preserves the whole filing and records the EDGAR metadata as capture context. It uses the shared
``stage_and_write_packet`` helper (which owns staging, the ``file_{NN}`` id map, posture-honesty
validation, and cleanup); it does NOT extract the employee count (that is the Layer-2 derivation)
and it does NOT decide entity identity.

``build_edgar_packet`` is pure-ish and offline-testable (a supplied Success in -> a packet on
disk out). ``main`` is the thin CLI: it calls the live adapter (a real SEC User-Agent is
required), then ``build_edgar_packet``; exit codes follow the runner convention (0 = packet
produced; 2 = bad input / ValueError; 3 = adapter or other failure).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from harness_utils import utc_now_z
from source_capture.adapters.edgar_filings import (
    EdgarFilingFailure,
    EdgarFilingSuccess,
    EdgarHttpFetch,
    fetch_edgar_filing,
)
from source_capture.models import (
    CaptureModeCategory,
    PacketTiming,
    PacketWriteResult,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map
from source_capture.adapters.direct_http import fetch_direct_http_capture  # noqa: F401  (default seam re-export for callers)

EDGAR_SOURCE_SURFACE = "www.sec.gov/Archives (SEC EDGAR)"
EDGAR_ACCESS_POSTURE = "public_official_edgar"
EDGAR_PACKET_NON_CLAIMS = [
    "full primary filing captured; NO employee count extracted (that is the Layer-2 derivation)",
    "raw observation; not validated, not ECR-ready until rebound under a Decision Frame",
    "structured filing metadata carried; not a canonical-entity or comparability claim",
    "not Cleaning, ECR, or Judgment design",
]


def build_edgar_packet(
    *,
    success: EdgarFilingSuccess,
    output_directory: Path,
    decision_question: str,
    operator_category: str = "local_cli_operator",
) -> PacketWriteResult:
    """Write a full-filing SourceCapturePacket from a fetched EDGAR filing (offline-testable)."""
    artifact_name = f"{success.accession_number.replace('-', '')}_{success.primary_document}"
    staged: list[tuple[str, bytes]] = [(artifact_name, success.filing_bytes)]
    file_id = staged_file_id_map(staged)[artifact_name]

    capture_context = json.dumps(
        {
            "source": "sec_edgar",
            "cik": success.cik,
            "accession_number": success.accession_number,
            "form_type": success.form_type,
            "period_of_report": success.period_of_report,
            "primary_document": success.primary_document,
            "document_url": success.document_url,
            "final_url": success.final_url,
            "http_status": success.http_metadata.get("status"),
            "content_type": success.http_metadata.get("content_type"),
            "byte_count": success.http_metadata.get("byte_count"),
            "filing_date": "not_carried_by_this_adapter_slice",
        },
        sort_keys=True,
    )

    # period_of_report is the fiscal-period event the headcount is as-of; filing/publication date
    # is not separately carried by this adapter slice (a deferred enrichment), recorded honestly.
    publication = known_fact(success.period_of_report)
    edit_version = not_applicable("EDGAR primary filing carries no separate edit/version timing in this slice")
    cutoff = unknown_with_reason("cutoff posture is decision-frame supplied; standing-corpus capture sets it later")
    recapture = not_applicable("first capture of this filing")
    access = known_fact(EDGAR_ACCESS_POSTURE)
    archive = not_attempted("live EDGAR fetch; archive/history not queried in this slice")
    media = not_applicable("structured text/HTML filing; no additional media capture required")

    edgar_slice = SourceCaptureSlice(
        slice_id="edgar_primary_filing",
        locator=known_fact(success.document_url),
        timing=PacketTiming(
            source_publication_or_event=publication,
            source_edit_or_version=edit_version,
            capture_time=known_fact(utc_now_z()),
            recapture_time=recapture,
            cutoff_posture=cutoff,
        ),
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=recapture,
        limitations=list(success.limitation_notes),
        warning_notes=list(success.warning_notes),
        preserved_file_ids=[file_id],
    )

    return stage_and_write_packet(
        output_directory=output_directory,
        staged_artifacts=staged,
        source_slices=[edgar_slice],
        source_family="sec_edgar",
        source_surface=EDGAR_SOURCE_SURFACE,
        source_locator=known_fact(success.document_url),
        decision_question=decision_question,
        capture_context=capture_context,
        capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
        operator_category=operator_category,
        source_publication_or_event=publication,
        source_edit_or_version=edit_version,
        cutoff_posture=cutoff,
        recapture_time=recapture,
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=recapture,
        warnings=list(success.warning_notes),
        limitations=list(success.limitation_notes),
        receipt_summary=(
            f"EDGAR {success.form_type} full-filing capture for CIK {success.cik} "
            f"(period {success.period_of_report}); {len(success.filing_bytes)} bytes preserved."
        ),
        receipt_non_claims=EDGAR_PACKET_NON_CLAIMS,
    )


def main(argv: Sequence[str] | None = None, *, fetch: EdgarHttpFetch = fetch_direct_http_capture) -> int:
    parser = argparse.ArgumentParser(description="Capture one SEC EDGAR primary filing into a Source Capture Packet.")
    parser.add_argument("--cik", required=True)
    parser.add_argument("--accession-number", required=True)
    parser.add_argument("--primary-document", required=True)
    parser.add_argument("--period-of-report", required=True)
    parser.add_argument("--form-type", default="10-K")
    parser.add_argument("--user-agent", required=True, help="SEC fair-access requires a declared contactable UA")
    parser.add_argument("--output-directory", required=True, type=Path)
    parser.add_argument("--decision-question", required=True)
    args = parser.parse_args(argv)

    try:
        result = fetch_edgar_filing(
            cik=args.cik,
            accession_number=args.accession_number,
            primary_document=args.primary_document,
            period_of_report=args.period_of_report,
            form_type=args.form_type,
            user_agent=args.user_agent,
            fetch=fetch,
        )
    except ValueError as exc:
        parser.error(str(exc))  # exit code 2

    if isinstance(result, EdgarFilingFailure):
        sys.stderr.write(f"EDGAR fetch failed ({result.failure_kind}): {result.message}\n")
        return 3

    try:
        write_result = build_edgar_packet(
            success=result,
            output_directory=args.output_directory,
            decision_question=args.decision_question,
        )
    except (ValueError, FileNotFoundError) as exc:
        sys.stderr.write(f"EDGAR packet write failed: {exc}\n")
        return 3

    sys.stdout.write(f"{write_result.output_directory}\n")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
