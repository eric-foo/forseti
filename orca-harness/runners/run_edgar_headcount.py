"""End-to-end EDGAR headcount entrypoint -- discover -> fetch -> packet -> derive -> append -> project.

The trigger-agnostic top of the company-aggregate EDGAR slice. ``run_edgar_headcount_capture`` is a
pure orchestration of the already-built units: discover the latest 10-K (submissions API) -> fetch
the full filing (capture adapter) -> write a SourceCapturePacket -> derive the immutable
observation -> append it to the observation log -> fold the log into a version-pinned projection.
It is "trigger-agnostic": a manual ``main`` CLI drives it now (attended-fallback posture); a
scheduler could call the same function later with no change.

Discovery supplies the real ``filing_date``, so the end-to-end observation carries an actual filing
date (not the capture-adapter sentinel). The network lives entirely behind the injected ``fetch``
seam, so the whole pipeline is offline-testable with a stub transport; no live SEC call runs in
unit tests. The projection stays a filer-level UNRESOLVED trend under the default passthrough-null
map (the #1 ownership boundary): this entrypoint authors no entity identity.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

from runners.run_source_capture_edgar_packet import build_edgar_packet
from source_capture.adapters.direct_http import fetch_direct_http_capture
from source_capture.adapters.edgar_discovery import (
    DEFAULT_DISCOVERY_FORM,
    EdgarDiscoveryFailure,
    EdgarDiscoverySuccess,
    discover_filing,
)
from source_capture.adapters.edgar_filings import EdgarFilingFailure, EdgarHttpFetch, fetch_edgar_filing
from source_capture.company_aggregate.edgar_derivation import (
    EdgarDerivationFailure,
    derive_edgar_headcount_observation,
)
from source_capture.company_aggregate.entity_resolution_port import DEFAULT_RESOLUTION_MAP, ResolutionMap
from source_capture.company_aggregate.observation import EdgarHeadcountObservation
from source_capture.company_aggregate.observation_log import append_observation, read_observation_log
from source_capture.company_aggregate.projection import CompanyHeadcountProjection, project_company_headcount


class EdgarHeadcountRunFailure(ValueError):
    """A typed operational failure in the end-to-end run (discovery / filing fetch)."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True)
class EdgarHeadcountRunResult:
    discovery: EdgarDiscoverySuccess
    packet_output_directory: str
    observation: EdgarHeadcountObservation
    projections: list[CompanyHeadcountProjection] = field(default_factory=list)


def run_edgar_headcount_capture(
    *,
    cik: str,
    user_agent: str,
    packet_output_directory: Path,
    observation_log_path: Path,
    decision_question: str,
    form_type: str = DEFAULT_DISCOVERY_FORM,
    resolution_map: ResolutionMap = DEFAULT_RESOLUTION_MAP,
    fetch: EdgarHttpFetch = fetch_direct_http_capture,
) -> EdgarHeadcountRunResult:
    """Run the full capture->derive->append->project pipeline for one CIK's latest filing."""
    discovery = discover_filing(cik=cik, user_agent=user_agent, form_type=form_type, fetch=fetch)
    if isinstance(discovery, EdgarDiscoveryFailure):
        raise EdgarHeadcountRunFailure(
            "discovery_failed", f"{discovery.failure_kind}: {discovery.message}"
        )

    filing = fetch_edgar_filing(
        cik=discovery.cik,
        accession_number=discovery.accession_number,
        primary_document=discovery.primary_document,
        period_of_report=discovery.period_of_report,
        form_type=discovery.form_type,
        user_agent=user_agent,
        fetch=fetch,
    )
    if isinstance(filing, EdgarFilingFailure):
        raise EdgarHeadcountRunFailure(
            "filing_fetch_failed", f"{filing.failure_kind}: {filing.message}"
        )

    write_result = build_edgar_packet(
        success=filing,
        output_directory=packet_output_directory,
        decision_question=decision_question,
    )
    observation = derive_edgar_headcount_observation(
        packet_or_manifest_path=Path(write_result.output_directory),
        filing_date=discovery.filing_date,
    )
    append_observation(observation, log_path=observation_log_path)
    projections = project_company_headcount(
        read_observation_log(observation_log_path), resolution_map=resolution_map
    )
    return EdgarHeadcountRunResult(
        discovery=discovery,
        packet_output_directory=str(write_result.output_directory),
        observation=observation,
        projections=projections,
    )


def main(argv: Sequence[str] | None = None, *, fetch: EdgarHttpFetch = fetch_direct_http_capture) -> int:
    parser = argparse.ArgumentParser(
        description="Discover, capture, derive, and project one CIK's latest EDGAR headcount filing."
    )
    parser.add_argument("--cik", required=True)
    parser.add_argument("--user-agent", required=True, help="SEC fair-access requires a declared contactable UA")
    parser.add_argument("--packet-output-directory", required=True, type=Path)
    parser.add_argument("--observation-log", required=True, type=Path)
    parser.add_argument("--decision-question", required=True)
    parser.add_argument("--form-type", default=DEFAULT_DISCOVERY_FORM)
    args = parser.parse_args(argv)

    try:
        result = run_edgar_headcount_capture(
            cik=args.cik,
            user_agent=args.user_agent,
            packet_output_directory=args.packet_output_directory,
            observation_log_path=args.observation_log,
            decision_question=args.decision_question,
            form_type=args.form_type,
            fetch=fetch,
        )
    except (EdgarHeadcountRunFailure, EdgarDerivationFailure) as exc:
        sys.stderr.write(f"EDGAR headcount run failed: {exc}\n")
        return 3
    except (ValueError, FileNotFoundError) as exc:
        parser.error(str(exc))  # exit code 2 (bad input / usage)

    sys.stdout.write(f"{result.packet_output_directory}\n")
    for projection in result.projections:
        sys.stdout.write(
            f"{projection.provisional_filer_key} [{projection.resolution_state}] "
            f"{len(projection.points)} point(s)\n"
        )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
