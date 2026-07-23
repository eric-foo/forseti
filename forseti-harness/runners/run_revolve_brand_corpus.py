"""Capture one complete public REVOLVE brand grid, every PDP, and one deep PDP."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Sequence
from urllib.parse import urlparse

from pydantic import Field

from runners.run_source_capture_cloakbrowser_packet import (
    main as run_cloakbrowser_capture,
)
from schemas.case_models import StrictModel
from source_capture.adapters.cloakbrowser_snapshot import (
    CloakBrowserSnapshotEngine,
    ReusableCloakBrowserSnapshotEngine,
)
from source_capture.adapters.revolve_us_market import confirm_revolve_us_market
from source_capture.models import VisibleFactStatus
from source_capture.retail_grid_projection import (
    RetailGridProjectionPacket,
    build_retail_grid_projection,
    load_verified_source_capture_packet_directory,
)
from source_capture.retail_capture_profiles import extract_revolve_grid_subject_from_url
from source_capture.retail_pdp_content import load_retail_pdp_content_record
from source_capture.revolve_brand_grid import REVOLVE_GRID_PARSER_VERSION
from source_capture.revolve_corpus import (
    RevolveCorpusVerificationReceipt,
    verify_revolve_corpus,
)
from source_capture.revolve_pdp_content import RevolvePdpAggregateContentRecord
from source_capture.revolve_yotpo_deep_capture import (
    RevolveYotpoDeepCaptureReceipt,
    capture_revolve_yotpo_deep_from_content,
)

RUN_SCHEMA_VERSION = "revolve_brand_corpus_run_v2"
CaptureMain = Callable[[Sequence[str] | None], int]
DeepCapture = Callable[..., RevolveYotpoDeepCaptureReceipt]


class RevolveBrandCorpusRunReceipt(StrictModel):
    schema_version: str = RUN_SCHEMA_VERSION
    brand_url: str
    grid_packet_directory: str
    grid_projection_path: str
    grid_input_mode: str
    grid_parser_version: str = REVOLVE_GRID_PARSER_VERSION
    requested_pdp_count: int = 0
    captured_pdp_count: int = 0
    pdp_packet_directories: dict[str, str] = Field(default_factory=dict)
    deep_receipt_path: str | None = None
    corpus_receipt_path: str | None = None
    status: str
    failure: str | None = None


def run_revolve_brand_corpus(
    *,
    brand_url: str,
    output_root: Path,
    review_limit: int = 100,
    resume_grid_packet: Path | None = None,
    capture_main: CaptureMain = run_cloakbrowser_capture,
    deep_capture: DeepCapture = capture_revolve_yotpo_deep_from_content,
    capture_engine: CloakBrowserSnapshotEngine | None = None,
) -> tuple[int, RevolveBrandCorpusRunReceipt]:
    """Run a fresh, no-proxy, no-stored-profile REVOLVE corpus capture."""
    if output_root.exists():
        raise ValueError(f"output root already exists; refusing overwrite: {output_root}")
    if not 1 <= review_limit <= 100:
        raise ValueError("review_limit must be between 1 and 100")
    output_root.mkdir(parents=True)
    grid_packet_directory = (
        resume_grid_packet.resolve()
        if resume_grid_packet is not None
        else output_root / "grid-packet"
    )
    grid_projection_path = output_root / "grid-projection.json"
    pdp_root = output_root / "pdp"
    deep_receipt_path = output_root / "deep-pdp.json"
    corpus_receipt_path = output_root / "corpus-receipt.json"
    run_receipt_path = output_root / "run-receipt.json"

    if resume_grid_packet is not None:
        try:
            projection = _replay_verified_grid_packet(
                packet_directory=grid_packet_directory,
                brand_url=brand_url,
                projection_path=grid_projection_path,
            )
        except Exception as exc:
            receipt = _run_receipt(
                brand_url=brand_url,
                grid_packet_directory=grid_packet_directory,
                grid_projection_path=grid_projection_path,
                status="partial",
                failure=(
                    "revolve_grid_replay_failed:"
                    f"{type(exc).__name__}:{exc}"
                ),
            )
            _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
            return 3, receipt
    else:
        grid_exit = _invoke_capture(
            capture_main,
            _capture_args(
                url=brand_url,
                source_family="retail_pdp",
                profile="revolve_grid_aggregate",
                output=grid_packet_directory,
                grid_projection=grid_projection_path,
            ),
            capture_engine=capture_engine,
        )
        if grid_exit != 0:
            receipt = _run_receipt(
                brand_url=brand_url,
                grid_packet_directory=grid_packet_directory,
                grid_projection_path=grid_projection_path,
                status="partial",
                failure=f"revolve_grid_capture_failed:exit={grid_exit}",
            )
            _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
            return grid_exit, receipt

        try:
            projection = RetailGridProjectionPacket.model_validate_json(
                grid_projection_path.read_text(encoding="utf-8")
            )
        except Exception as exc:
            receipt = _run_receipt(
                brand_url=brand_url,
                grid_packet_directory=grid_packet_directory,
                grid_projection_path=grid_projection_path,
                status="partial",
                failure=(
                    "revolve_grid_projection_load_failed:"
                    f"{type(exc).__name__}:{exc}"
                ),
            )
            _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
            return 3, receipt
    if projection.completeness.status != "complete":
        receipt = _run_receipt(
            brand_url=brand_url,
            grid_packet_directory=grid_packet_directory,
            grid_projection_path=grid_projection_path,
            requested_pdp_count=len(projection.rows),
            status="partial",
            failure=(
                "revolve_grid_projection_incomplete:"
                + ";".join(projection.completeness.residuals)
            ),
        )
        _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
        return 4, receipt

    pdp_records: list[RevolvePdpAggregateContentRecord] = []
    pdp_packet_directories: dict[str, str] = {}
    ordered_rows = sorted(
        projection.rows,
        key=lambda row: (
            min(item.grid_position for item in row.placements),
            str(row.source_visible_fields.get("style_id") or ""),
        ),
    )
    for row in ordered_rows:
        style_id = str(row.source_visible_fields.get("style_id") or "")
        product_url = str(
            row.source_visible_fields.get("canonical_product_url")
            or row.source_visible_fields.get("product_url")
            or ""
        )
        if not style_id or not product_url:
            receipt = _run_receipt(
                brand_url=brand_url,
                grid_packet_directory=grid_packet_directory,
                grid_projection_path=grid_projection_path,
                requested_pdp_count=len(ordered_rows),
                captured_pdp_count=len(pdp_records),
                pdp_packet_directories=pdp_packet_directories,
                status="partial",
                failure=f"revolve_grid_row_identity_incomplete:{row.row_id}",
            )
            _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
            return 4, receipt
        packet_directory = pdp_root / style_id
        pdp_exit = _invoke_capture(
            capture_main,
            _capture_args(
                url=product_url,
                source_family="retail_pdp",
                profile="revolve_pdp_aggregate",
                output=packet_directory,
            ),
            capture_engine=capture_engine,
        )
        if pdp_exit != 0:
            receipt = _run_receipt(
                brand_url=brand_url,
                grid_packet_directory=grid_packet_directory,
                grid_projection_path=grid_projection_path,
                requested_pdp_count=len(ordered_rows),
                captured_pdp_count=len(pdp_records),
                pdp_packet_directories=pdp_packet_directories,
                status="partial",
                failure=f"revolve_pdp_capture_failed:{style_id}:exit={pdp_exit}",
            )
            _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
            return pdp_exit, receipt
        try:
            record = _load_revolve_pdp_record(packet_directory)
        except Exception as exc:
            receipt = _run_receipt(
                brand_url=brand_url,
                grid_packet_directory=grid_packet_directory,
                grid_projection_path=grid_projection_path,
                requested_pdp_count=len(ordered_rows),
                captured_pdp_count=len(pdp_records),
                pdp_packet_directories=pdp_packet_directories,
                status="partial",
                failure=(
                    f"revolve_pdp_record_load_failed:{style_id}:"
                    f"{type(exc).__name__}:{exc}"
                ),
            )
            _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
            return 3, receipt
        pdp_records.append(record)
        pdp_packet_directories[style_id] = str(packet_directory.resolve())

    try:
        candidate_style_id = _deep_candidate_style_id(projection)
        candidate_record = next(
            record for record in pdp_records if record.style_id == candidate_style_id
        )
    except Exception as exc:
        receipt = _run_receipt(
            brand_url=brand_url,
            grid_packet_directory=grid_packet_directory,
            grid_projection_path=grid_projection_path,
            requested_pdp_count=len(ordered_rows),
            captured_pdp_count=len(pdp_records),
            pdp_packet_directories=pdp_packet_directories,
            status="partial",
            failure=(
                "revolve_deep_candidate_selection_failed:"
                f"{type(exc).__name__}:{exc}"
            ),
        )
        _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
        return 3, receipt
    try:
        deep_receipt = deep_capture(
            content_record=candidate_record,
            review_limit=review_limit,
        )
        _write_new_json(
            deep_receipt_path,
            deep_receipt.model_dump(mode="json"),
        )
    except Exception as exc:
        receipt = _run_receipt(
            brand_url=brand_url,
            grid_packet_directory=grid_packet_directory,
            grid_projection_path=grid_projection_path,
            requested_pdp_count=len(ordered_rows),
            captured_pdp_count=len(pdp_records),
            pdp_packet_directories=pdp_packet_directories,
            status="partial",
            failure=f"revolve_deep_capture_failed:{type(exc).__name__}:{exc}",
        )
        _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
        return 3, receipt
    try:
        corpus_receipt: RevolveCorpusVerificationReceipt = verify_revolve_corpus(
            grid_projection=projection,
            pdp_records=pdp_records,
            deep_receipt=deep_receipt,
        )
        _write_new_json(
            corpus_receipt_path,
            corpus_receipt.model_dump(mode="json"),
        )
    except Exception as exc:
        receipt = _run_receipt(
            brand_url=brand_url,
            grid_packet_directory=grid_packet_directory,
            grid_projection_path=grid_projection_path,
            requested_pdp_count=len(ordered_rows),
            captured_pdp_count=len(pdp_records),
            pdp_packet_directories=pdp_packet_directories,
            deep_receipt_path=deep_receipt_path,
            status="partial",
            failure=(
                "revolve_corpus_verification_failed:"
                f"{type(exc).__name__}:{exc}"
            ),
        )
        _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
        return 3, receipt
    status = "complete" if corpus_receipt.status == "complete" else "partial"
    receipt = _run_receipt(
        brand_url=brand_url,
        grid_packet_directory=grid_packet_directory,
        grid_projection_path=grid_projection_path,
        requested_pdp_count=len(ordered_rows),
        captured_pdp_count=len(pdp_records),
        pdp_packet_directories=pdp_packet_directories,
        deep_receipt_path=deep_receipt_path,
        corpus_receipt_path=corpus_receipt_path,
        status=status,
        failure=(
            None
            if status == "complete"
            else "revolve_corpus_verification_partial:"
            + ";".join(corpus_receipt.residuals)
        ),
    )
    _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
    return (0 if status == "complete" else 4), receipt


def _capture_args(
    *,
    url: str,
    source_family: str,
    profile: str,
    output: Path,
    grid_projection: Path | None = None,
) -> list[str]:
    args = [
        "--url",
        url,
        "--source-family",
        source_family,
        "--source-surface",
        "cloakbrowser_snapshot",
        "--decision-question",
        "What complete public REVOLVE brand/PDP evidence is visible now?",
        "--output",
        str(output),
        "--capture-context",
        (
            "public logged-out REVOLVE US/USD capture; no VPN, proxy, "
            "stored browser profile, login, or retailer account"
        ),
        "--operator-category",
        "revolve_brand_corpus_cli_operator",
        "--retail-capture-profile",
        profile,
        "--revolve-market",
        "US",
        "--actor-audience-context",
        "public logged-out shopper surface",
        "--source-publication-or-event-unknown-reason",
        "retailer page publication time is not exposed",
        "--source-edit-or-version-unknown-reason",
        "retailer page edit version is not exposed",
        "--cutoff-posture-unknown-reason",
        "the retailer page exposes current state but no bounded publication cutoff",
        "--recapture-time-not-applicable-reason",
        "fresh one-off pre-project proof capture",
        "--recapture-relationship-not-applicable-reason",
        "no earlier REVOLVE packet is being replaced",
    ]
    if grid_projection is not None:
        args.extend(["--retail-grid-projection-output", str(grid_projection)])
    return args


def _invoke_capture(
    capture_main: CaptureMain,
    args: Sequence[str],
    *,
    capture_engine: CloakBrowserSnapshotEngine | None,
) -> int:
    try:
        if capture_engine is None:
            result = capture_main(args)
        elif capture_main is run_cloakbrowser_capture:
            result = capture_main(args, capture_engine=capture_engine)  # type: ignore[call-arg]
        else:
            raise ValueError(
                "capture_engine is supported only by the default CloakBrowser runner"
            )
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 3
    return int(result)


def _canonical_revolve_brand_url(value: str) -> str | None:
    parsed = urlparse(value)
    if (
        parsed.scheme != "https"
        or (parsed.hostname or "").lower()
        not in {"revolve.com", "www.revolve.com"}
    ):
        return None
    subject = extract_revolve_grid_subject_from_url(value)
    if subject is None:
        return None
    slug, brand_id = subject
    return f"https://www.revolve.com/{slug}/br/{brand_id}"


def _replay_verified_grid_packet(
    *, packet_directory: Path, brand_url: str, projection_path: Path
) -> RetailGridProjectionPacket:
    packet, bodies = load_verified_source_capture_packet_directory(packet_directory)
    if packet.source_family != "retail_pdp":
        raise ValueError("resume grid packet is not a retail capture packet")
    if (
        packet.source_locator.status != VisibleFactStatus.KNOWN
        or packet.source_locator.value is None
        or _canonical_revolve_brand_url(packet.source_locator.value)
        != _canonical_revolve_brand_url(brand_url)
    ):
        raise ValueError("resume grid packet does not bind the requested REVOLVE brand URL")
    rendered_files = [
        item
        for item in packet.preserved_files
        if item.relative_packet_path.replace("\\", "/").endswith(
            "cloakbrowser_rendered_dom.html"
        )
    ]
    if len(rendered_files) != 1:
        raise ValueError(
            "resume grid packet must preserve exactly one rendered REVOLVE DOM"
        )
    rendered_body = bodies.get(rendered_files[0].file_id)
    if rendered_body is None:
        raise ValueError("resume grid packet rendered DOM bytes are unavailable")
    rendered_dom = rendered_body.decode("utf-8", errors="replace")
    confirmation = confirm_revolve_us_market(
        rendered_dom,
        expected_style_id=None,
        page_kind="grid",
    )
    if not confirmation.confirmed:
        raise ValueError(
            "resume grid packet fails current REVOLVE US/USD confirmation: "
            f"{confirmation.detail}"
        )
    projection = build_retail_grid_projection(
        packet=packet,
        raw_file_bytes_by_file_id=bodies,
    )
    if projection.completeness.status != "complete":
        raise ValueError(
            "resume grid packet fails current completeness reconciliation: "
            + ";".join(projection.completeness.residuals)
        )
    _write_new_json(projection_path, projection.model_dump(mode="json"))
    return projection
def _load_revolve_pdp_record(
    packet_directory: Path,
) -> RevolvePdpAggregateContentRecord:
    packet, bodies = load_verified_source_capture_packet_directory(packet_directory)
    loaded = load_retail_pdp_content_record(
        packet=packet,
        file_bytes_by_file_id=bodies,
    )
    if loaded is None or not isinstance(loaded[1], RevolvePdpAggregateContentRecord):
        raise ValueError(
            f"packet did not retain a REVOLVE PDP content record: {packet_directory}"
        )
    return loaded[1]


def _deep_candidate_style_id(projection: RetailGridProjectionPacket) -> str:
    candidate = min(
        projection.rows,
        key=lambda row: (
            -int(row.source_visible_fields.get("review_count") or 0),
            min(item.grid_position for item in row.placements),
            str(row.source_visible_fields.get("style_id") or ""),
        ),
    )
    return str(candidate.source_visible_fields["style_id"])


def _run_receipt(
    *,
    brand_url: str,
    grid_packet_directory: Path,
    grid_projection_path: Path,
    requested_pdp_count: int = 0,
    captured_pdp_count: int = 0,
    pdp_packet_directories: dict[str, str] | None = None,
    deep_receipt_path: Path | None = None,
    corpus_receipt_path: Path | None = None,
    status: str,
    failure: str | None,
) -> RevolveBrandCorpusRunReceipt:
    return RevolveBrandCorpusRunReceipt(
        brand_url=brand_url,
        grid_packet_directory=str(grid_packet_directory.resolve()),
        grid_projection_path=str(grid_projection_path.resolve()),
        grid_input_mode=(
            "live_capture"
            if grid_packet_directory.resolve()
            == (grid_projection_path.parent / "grid-packet").resolve()
            else "verified_raw_replay"
        ),
        requested_pdp_count=requested_pdp_count,
        captured_pdp_count=captured_pdp_count,
        pdp_packet_directories=pdp_packet_directories or {},
        deep_receipt_path=(
            str(deep_receipt_path.resolve()) if deep_receipt_path is not None else None
        ),
        corpus_receipt_path=(
            str(corpus_receipt_path.resolve())
            if corpus_receipt_path is not None
            else None
        ),
        status=status,
        failure=failure,
    )


def _write_new_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Capture one complete public REVOLVE brand grid, every unique PDP, "
            "and bounded Most Relevant/Most Recent reviews for the deepest PDP."
        )
    )
    parser.add_argument("--brand-url", required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--review-limit", type=int, default=100)
    parser.add_argument(
        "--resume-grid-packet",
        type=Path,
        default=None,
        help=(
            "Reuse one hash-verified raw REVOLVE grid packet after current-parser "
            "brand and US/USD revalidation, then continue directly to PDP capture."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        with ReusableCloakBrowserSnapshotEngine() as capture_engine:
            exit_code, receipt = run_revolve_brand_corpus(
                brand_url=args.brand_url,
                output_root=args.output_root,
                review_limit=args.review_limit,
                resume_grid_packet=args.resume_grid_packet,
                capture_engine=capture_engine,
            )
    except ValueError as exc:
        raise SystemExit(f"REVOLVE brand corpus capture failed: {exc}") from exc
    print(json.dumps(receipt.model_dump(mode="json"), sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
