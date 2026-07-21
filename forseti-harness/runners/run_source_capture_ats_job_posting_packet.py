"""Runner: capture one public ATS job board as a dated Source Capture Packet.

Commission-bounded, capture-only, point-in-time: one invocation captures one
board's current postings as one packet (postings become slices), preserving the
verbatim ATS response in ``raw/``. No scheduler, no standing crawler — re-capture
is a new invocation. The board to capture comes from the manual registry
(company + vendor + token/tenant); this runner takes the resolved coordinates as
flags.

The last mile (stage -> write -> clean up) is owned by
``packet_assembly.stage_and_write_packet``; exit codes follow the adapter runner
convention: 0 = packet produced, 2 = bad input, 3 = adapter/other failure.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness_utils import utc_now_z
from source_capture import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.adapters.ats_job_posting import (
    AtsBoardCaptureFailure,
    AtsBoardCaptureSuccess,
    AtsHttpTransport,
    AtsVendor,
    StdlibAtsHttpTransport,
    fetch_ashby_board,
    fetch_greenhouse_board,
    fetch_lever_board,
    fetch_workday_board,
)
from source_capture.ats_job_posting_projection import (
    ATS_JOB_POSTING_SOURCE_FAMILY,
    CAPTURE_METADATA_BASENAME,
    RAW_BOARD_DOCUMENT_BASENAME,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


ATS_JOB_POSTING_NON_CLAIMS = [
    "not ranking, relevance filtering, or role classification",
    "not US-market or geographic gating (verbatim location only)",
    "not pain inference",
    "not a standing crawler or scheduler",
    "not ECR design",
    "not Cleaning implementation",
    "not Judgment scoring",
    "not buyer proof",
    "not commercial-readiness logic",
]


def _fetch_board(
    *, vendor: AtsVendor, company: str, args: argparse.Namespace, transport: StdlibAtsHttpTransport
):
    if vendor is AtsVendor.GREENHOUSE:
        _require(args, "board_token", vendor)
        return fetch_greenhouse_board(company=company, board_token=args.board_token, transport=transport)
    if vendor is AtsVendor.LEVER:
        _require(args, "board_token", vendor)
        return fetch_lever_board(company=company, board_token=args.board_token, transport=transport)
    if vendor is AtsVendor.ASHBY:
        _require(args, "job_board_name", vendor)
        return fetch_ashby_board(
            company=company, job_board_name=args.job_board_name, transport=transport
        )
    if vendor is AtsVendor.WORKDAY:
        for name in ("tenant", "wd_server", "site"):
            _require(args, name, vendor)
        return fetch_workday_board(
            company=company,
            tenant=args.tenant,
            wd_server=args.wd_server,
            site=args.site,
            transport=transport,
            delay_seconds=args.delay_seconds,
        )
    raise ValueError(f"unsupported ATS vendor: {vendor}")


def _require(args: argparse.Namespace, attr: str, vendor: AtsVendor) -> None:
    if getattr(args, attr, None) in (None, ""):
        raise ValueError(f"--{attr.replace('_', '-')} is required for vendor {vendor.value}")


def run_source_capture_ats_job_posting_packet(
    *,
    vendor: AtsVendor,
    company: str,
    decision_question: str,
    args: argparse.Namespace,
    output_directory: Path | None = None,
    data_root: "DataLakeRoot | None" = None,
    transport: AtsHttpTransport | None = None,
) -> tuple[int, str]:
    transport = transport or StdlibAtsHttpTransport(
        timeout_seconds=args.timeout_seconds, max_bytes=args.max_bytes
    )
    result = _fetch_board(vendor=vendor, company=company, args=args, transport=transport)
    if isinstance(result, AtsBoardCaptureFailure):
        return 3, f"{result.failure_kind.value}: {result.message}"
    assert isinstance(result, AtsBoardCaptureSuccess)

    captured_at = utc_now_z()
    metadata = {
        "ats_vendor": result.vendor.value,
        "company": result.company,
        "board_locator": result.board_locator,
        "captured_at": captured_at,
        "http_status": result.http_status,
        "posting_count": len(result.postings),
        "warning_notes": list(result.warning_notes),
        "limitation_notes": list(result.limitation_notes),
    }
    artifacts: list[tuple[str, bytes]] = [
        (RAW_BOARD_DOCUMENT_BASENAME, result.raw_board_document),
        (
            CAPTURE_METADATA_BASENAME,
            (json.dumps(metadata, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        ),
    ]
    file_ids = staged_file_id_map(artifacts)
    raw_file_id = file_ids[RAW_BOARD_DOCUMENT_BASENAME]
    metadata_file_id = file_ids[CAPTURE_METADATA_BASENAME]

    access_posture = known_fact(
        f"ats {vendor.value} public board fetch succeeded with HTTP {result.http_status}"
    )
    archive_posture = not_attempted("ATS adapter does not query archive or history services")
    media_posture = not_attempted("ATS adapter preserves the JSON board response only")
    recapture_posture = not_applicable(
        "no prior capture packet was supplied for this dated ATS snapshot"
    )

    def _timing(posted_date: str | None = None) -> PacketTiming:
        return PacketTiming(
            source_publication_or_event=(
                known_fact(posted_date)
                if posted_date
                else unknown_with_reason(
                    "ATS posting did not expose publication or event timing"
                )
            ),
            source_edit_or_version=unknown_with_reason("ATS board response carries no envelope version"),
            capture_time=known_fact(captured_at),
            recapture_time=not_applicable("dated point-in-time board snapshot; re-capture is a new commission"),
            cutoff_posture=unknown_with_reason("ATS runner did not receive cutoff posture metadata"),
        )

    slices: list[SourceCaptureSlice] = []
    if result.postings:
        for index, posting in enumerate(result.postings, start=1):
            locator = (
                known_fact(posting.source_url)
                if posting.source_url
                else known_fact(f"{vendor.value}:{posting.ats_job_id}")
            )
            # Every posting-slice's evidence lives in the one verbatim board document
            # (file_01); slice_01 additionally anchors the capture metadata (file_02).
            preserved_ids = [raw_file_id]
            if index == 1:
                preserved_ids.append(metadata_file_id)
            slices.append(
                SourceCaptureSlice(
                    slice_id=f"slice_{index:04d}",
                    locator=locator,
                    timing=_timing(posting.posted_date),
                    access_posture=access_posture,
                    archive_history_posture=archive_posture,
                    media_modality_posture=media_posture,
                    re_capture_relationship=recapture_posture,
                    preserved_file_ids=preserved_ids,
                )
            )
    else:
        slices.append(
            SourceCaptureSlice(
                slice_id="slice_0001",
                locator=known_fact(result.board_locator),
                timing=_timing(),
                access_posture=access_posture,
                archive_history_posture=archive_posture,
                media_modality_posture=media_posture,
                re_capture_relationship=recapture_posture,
                preserved_file_ids=[raw_file_id, metadata_file_id],
            )
        )

    capture_limitations = list(result.limitation_notes)
    write_result = stage_and_write_packet(
        output_directory=output_directory,
        data_root=data_root,
        staged_artifacts=artifacts,
        source_slices=slices,
        source_family=ATS_JOB_POSTING_SOURCE_FAMILY,
        source_surface=f"ats_{vendor.value}",
        source_locator=known_fact(result.board_locator),
        decision_question=decision_question,
        capture_context=(
            f"public {vendor.value} ATS board snapshot for {company}; "
            f"{len(result.postings)} posting(s) captured verbatim, capture-only"
        ),
        capture_mode=CaptureModeCategory.STRUCTURED_ACCESS,
        operator_category="ats_job_posting_cli_operator",
        session_identity=args.session_id,
        access_posture=access_posture,
        archive_history_posture=archive_posture,
        media_modality_posture=media_posture,
        re_capture_relationship=recapture_posture,
        warnings=list(result.warning_notes),
        limitations=capture_limitations,
        receipt_summary=(
            f"ATS {vendor.value} board packet for {company}: {len(result.postings)} posting(s) "
            f"preserved verbatim (HTTP {result.http_status})."
        ),
        receipt_non_claims=ATS_JOB_POSTING_NON_CLAIMS,
    )
    return 0, write_result.output_directory


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Capture one public ATS job board (Greenhouse/Lever/Workday/Ashby) as a dated "
            "Source Capture Packet. Capture-only: no ranking, filtering, or classification."
        )
    )
    parser.add_argument("--vendor", required=True, choices=[item.value for item in AtsVendor])
    parser.add_argument("--company", required=True, help="Registry company name for the board.")
    parser.add_argument(
        "--decision-question",
        required=True,
        help="The commission's decision question this capture serves.",
    )
    parser.add_argument("--board-token", default=None, help="Greenhouse/Lever board token or slug.")
    parser.add_argument("--job-board-name", default=None, help="Ashby jobBoardName.")
    parser.add_argument("--tenant", default=None, help="Workday tenant.")
    parser.add_argument("--wd-server", default=None, help="Workday server segment, e.g. wd1/wd5.")
    parser.add_argument("--site", default=None, help="Workday career site id.")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--data-root",
        default=None,
        help=(
            "Commit into the Forseti data lake at this root; mutually exclusive with --output. "
            "FORSETI_DATA_ROOT is used only when --output is omitted; legacy ORCA_DATA_ROOT accepted."
        ),
    )
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--timeout-seconds", type=float, default=25.0)
    parser.add_argument("--max-bytes", type=int, default=25_000_000)
    parser.add_argument(
        "--delay-seconds",
        type=float,
        default=1.75,
        help="Polite inter-request delay for multi-request vendors (Workday).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    import os

    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        vendor = AtsVendor(args.vendor)
        data_root = None
        output_directory = args.output
        if output_directory is not None and args.data_root is not None:
            parser.exit(
                status=2,
                message="exactly one of --output or --data-root/FORSETI_DATA_ROOT/ORCA_DATA_ROOT is required\n",
            )
        data_root_requested = args.data_root is not None or (
            output_directory is None and (os.environ.get("FORSETI_DATA_ROOT") or os.environ.get("ORCA_DATA_ROOT"))
        )
        if data_root_requested:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)
            output_directory = None
        if (output_directory is None) == (data_root is None):
            parser.exit(
                status=2,
                message="exactly one of --output or --data-root/FORSETI_DATA_ROOT/ORCA_DATA_ROOT is required\n",
            )
        exit_code, message = run_source_capture_ats_job_posting_packet(
            vendor=vendor,
            company=args.company,
            decision_question=args.decision_question,
            args=args,
            output_directory=output_directory,
            data_root=data_root,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"ats job-posting capture failed: {exc}\n")
    except Exception as exc:  # noqa: BLE001 - map any uncaught failure to exit 3
        parser.exit(status=3, message=f"ats job-posting capture failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0
    parser.exit(status=exit_code, message=f"ats job-posting capture failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
