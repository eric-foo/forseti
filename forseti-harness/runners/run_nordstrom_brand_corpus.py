"""Capture one complete public Nordstrom US brand corpus and deep-review PDP."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Sequence

from pydantic import Field

from runners.run_source_capture_cloakbrowser_packet import (
    main as run_cloakbrowser_capture,
)
from schemas.case_models import StrictModel
from source_capture.adapters.cloakbrowser_snapshot import (
    CloakBrowserSnapshotEngine,
    ReusableCloakBrowserSnapshotEngine,
)
from source_capture.nordstrom_brand_corpus import (
    NORDSTROM_GRID_PARSER_VERSION,
    NordstromDeepPdpReceipt,
    NordstromPdpEvidence,
    build_nordstrom_pdp_evidence,
    build_nordstrom_review_order_receipt,
    load_nordstrom_grid_packet,
    verify_nordstrom_corpus,
)


RUN_SCHEMA_VERSION = "nordstrom_brand_corpus_run_v1"
CaptureMain = Callable[[Sequence[str] | None], int]


class NordstromBrandCorpusRunReceipt(StrictModel):
    schema_version: str = RUN_SCHEMA_VERSION
    brand_url: str
    authorization_url: str
    authorization_statement: str
    grid_packet_directory: str
    grid_projection_path: str
    grid_input_mode: str
    grid_parser_version: str = NORDSTROM_GRID_PARSER_VERSION
    requested_pdp_count: int = 0
    captured_pdp_count: int = 0
    resumed_pdp_count: int = 0
    pdp_packet_directories: dict[str, str] = Field(default_factory=dict)
    pdp_evidence_paths: dict[str, str] = Field(default_factory=dict)
    deep_receipt_path: str | None = None
    corpus_receipt_path: str | None = None
    status: str
    failure: str | None = None


def run_nordstrom_brand_corpus(
    *,
    brand_url: str,
    authorization_url: str,
    authorization_statement: str,
    output_root: Path,
    review_limit: int = 100,
    resume_grid_packet: Path | None = None,
    resume_from: Sequence[Path] | Path | None = None,
    capture_main: CaptureMain = run_cloakbrowser_capture,
    capture_engine: CloakBrowserSnapshotEngine | None = None,
) -> tuple[int, NordstromBrandCorpusRunReceipt]:
    if output_root.exists():
        raise ValueError(f"output root already exists; refusing overwrite: {output_root}")
    if not 1 <= review_limit <= 100:
        raise ValueError("review_limit must be between 1 and 100")
    output_root.mkdir(parents=True)
    grid_packet = (
        resume_grid_packet.resolve()
        if resume_grid_packet is not None
        else output_root / "grid-packet"
    )
    grid_projection_path = output_root / "grid-projection.json"
    pdp_root = output_root / "pdp"
    pdp_evidence_root = output_root / "pdp-evidence"
    deep_root = output_root / "deep"
    deep_receipt_path = output_root / "deep-pdp.json"
    corpus_receipt_path = output_root / "corpus-receipt.json"
    run_receipt_path = output_root / "run-receipt.json"
    pdp_directories: dict[str, str] = {}
    pdp_evidence_paths: dict[str, str] = {}
    pdps: list[NordstromPdpEvidence] = []
    resumed_pdp_count = 0
    resume_roots = (
        [resume_from]
        if isinstance(resume_from, Path)
        else list(resume_from or ())
    )

    if resume_grid_packet is None:
        grid_exit = _invoke_capture(
            capture_main,
            _capture_args(url=brand_url, output=grid_packet, grid=True),
            capture_engine=capture_engine,
        )
        if grid_exit != 0:
            return _finish(
                run_receipt_path,
                _receipt(
                    brand_url,
                    authorization_url,
                    authorization_statement,
                    grid_packet,
                    grid_projection_path,
                    "live_capture",
                    status="partial",
                    failure=f"nordstrom_grid_capture_failed:exit={grid_exit}",
                ),
                grid_exit,
            )
    try:
        grid = load_nordstrom_grid_packet(
            packet_directory=grid_packet, requested_url=brand_url
        )
        _write_new_json(grid_projection_path, grid.model_dump(mode="json"))
    except Exception as exc:
        return _finish(
            run_receipt_path,
            _receipt(
                brand_url,
                authorization_url,
                authorization_statement,
                grid_packet,
                grid_projection_path,
                "verified_raw_replay" if resume_grid_packet else "live_capture",
                status="partial",
                failure=f"nordstrom_grid_projection_failed:{type(exc).__name__}:{exc}",
            ),
            3,
        )

    for card in sorted(grid.cards, key=lambda item: item.position):
        resume_candidates = [
            root / "pdp" / card.product_id
            for root in resume_roots
            if (root / "pdp" / card.product_id).is_dir()
        ]
        if len(resume_candidates) > 1:
            raise ValueError(
                f"multiple resume packets found for product {card.product_id}"
            )
        resumed_packet = resume_candidates[0] if resume_candidates else None
        packet_dir = (
            resumed_packet
            if resumed_packet is not None and resumed_packet.is_dir()
            else pdp_root / card.product_id
        )
        if packet_dir == pdp_root / card.product_id:
            pdp_exit = _invoke_capture(
                capture_main,
                _capture_args(
                    url=card.product_url,
                    output=packet_dir,
                    profile="nordstrom_pdp_aggregate",
                ),
                capture_engine=capture_engine,
            )
            if pdp_exit != 0:
                return _finish(
                    run_receipt_path,
                    _receipt(
                        brand_url,
                        authorization_url,
                        authorization_statement,
                        grid_packet,
                        grid_projection_path,
                        "verified_raw_replay" if resume_grid_packet else "live_capture",
                        requested=len(grid.cards),
                        captured=len(pdps),
                        resumed=resumed_pdp_count,
                        pdp_directories=pdp_directories,
                        status="partial",
                        failure=(
                            f"nordstrom_pdp_capture_failed:{card.product_id}:exit={pdp_exit}"
                        ),
                    ),
                    pdp_exit,
                )
        try:
            pdp = build_nordstrom_pdp_evidence(
                packet_directory=packet_dir,
                expected_product_id=card.product_id,
                expected_brand=grid.brand_name,
            )
        except Exception as exc:
            return _finish(
                run_receipt_path,
                _receipt(
                    brand_url,
                    authorization_url,
                    authorization_statement,
                    grid_packet,
                    grid_projection_path,
                    "verified_raw_replay" if resume_grid_packet else "live_capture",
                    requested=len(grid.cards),
                    captured=len(pdps),
                    resumed=resumed_pdp_count,
                    pdp_directories=pdp_directories,
                    status="partial",
                    failure=(
                        f"nordstrom_pdp_verification_failed:{card.product_id}:"
                        f"{type(exc).__name__}:{exc}"
                    ),
                ),
                3,
            )
        pdps.append(pdp)
        pdp_directories[card.product_id] = str(packet_dir.resolve())
        evidence_path = pdp_evidence_root / f"{card.product_id}.json"
        _write_new_json(evidence_path, pdp.model_dump(mode="json"))
        pdp_evidence_paths[card.product_id] = str(evidence_path.resolve())
        if resumed_packet is not None and packet_dir == resumed_packet:
            resumed_pdp_count += 1

    try:
        candidate = min(
            grid.cards,
            key=lambda item: (-item.review_count, item.position, item.product_id),
        )
    except Exception as exc:
        return _finish(
            run_receipt_path,
            _receipt(
                brand_url,
                authorization_url,
                authorization_statement,
                grid_packet,
                grid_projection_path,
                "verified_raw_replay" if resume_grid_packet else "live_capture",
                requested=len(grid.cards),
                captured=len(pdps),
                resumed=resumed_pdp_count,
                pdp_directories=pdp_directories,
                pdp_evidence_paths=pdp_evidence_paths,
                status="partial",
                failure=(
                    "nordstrom_deep_candidate_selection_failed:"
                    f"{type(exc).__name__}:{exc}"
                ),
            ),
            3,
        )
    order_receipts = {}
    for slug, requested_sort in (
        ("most-helpful", "Most Helpful"),
        ("most-recent", "Most Recent"),
    ):
        packet_dir = deep_root / slug
        posture = slug.replace("-", "_") + "_100"
        deep_exit = _invoke_capture(
            capture_main,
            _capture_args(
                url=candidate.product_url,
                output=packet_dir,
                profile="nordstrom_pdp_aggregate",
                review_posture=posture,
            ),
            capture_engine=capture_engine,
        )
        if deep_exit != 0:
            return _finish(
                run_receipt_path,
                _receipt(
                    brand_url,
                    authorization_url,
                    authorization_statement,
                    grid_packet,
                    grid_projection_path,
                    "verified_raw_replay" if resume_grid_packet else "live_capture",
                    requested=len(grid.cards),
                    captured=len(pdps),
                    resumed=resumed_pdp_count,
                    pdp_directories=pdp_directories,
                    status="partial",
                    failure=f"nordstrom_deep_capture_failed:{slug}:exit={deep_exit}",
                ),
                deep_exit,
            )
        try:
            order_receipts[slug] = build_nordstrom_review_order_receipt(
                packet_directory=packet_dir,
                requested_sort=requested_sort,
                limit=review_limit,
            )
        except Exception as exc:
            return _finish(
                run_receipt_path,
                _receipt(
                    brand_url,
                    authorization_url,
                    authorization_statement,
                    grid_packet,
                    grid_projection_path,
                    "verified_raw_replay" if resume_grid_packet else "live_capture",
                    requested=len(grid.cards),
                    captured=len(pdps),
                    resumed=resumed_pdp_count,
                    pdp_directories=pdp_directories,
                    pdp_evidence_paths=pdp_evidence_paths,
                    status="partial",
                    failure=(
                        f"nordstrom_deep_review_failed:{slug}:"
                        f"{type(exc).__name__}:{exc}"
                    ),
                ),
                3,
            )
    deep = NordstromDeepPdpReceipt(
        product_id=candidate.product_id,
        source_url=candidate.product_url,
        selection_basis=(
            "highest live grid review_count; tie-break grid position then product id"
        ),
        most_helpful=order_receipts["most-helpful"],
        most_recent=order_receipts["most-recent"],
        status="complete",
    )
    _write_new_json(deep_receipt_path, deep.model_dump(mode="json"))
    try:
        corpus = verify_nordstrom_corpus(grid=grid, pdps=pdps, deep=deep)
        _write_new_json(corpus_receipt_path, corpus.model_dump(mode="json"))
    except Exception as exc:
        return _finish(
            run_receipt_path,
            _receipt(
                brand_url,
                authorization_url,
                authorization_statement,
                grid_packet,
                grid_projection_path,
                "verified_raw_replay" if resume_grid_packet else "live_capture",
                requested=len(grid.cards),
                captured=len(pdps),
                resumed=resumed_pdp_count,
                pdp_directories=pdp_directories,
                pdp_evidence_paths=pdp_evidence_paths,
                deep_receipt_path=deep_receipt_path,
                status="partial",
                failure=(
                    "nordstrom_corpus_verification_failed:"
                    f"{type(exc).__name__}:{exc}"
                ),
            ),
            3,
        )
    receipt = _receipt(
        brand_url,
        authorization_url,
        authorization_statement,
        grid_packet,
        grid_projection_path,
        "verified_raw_replay" if resume_grid_packet else "live_capture",
        requested=len(grid.cards),
        captured=len(pdps),
        resumed=resumed_pdp_count,
        pdp_directories=pdp_directories,
        pdp_evidence_paths=pdp_evidence_paths,
        deep_receipt_path=deep_receipt_path,
        corpus_receipt_path=corpus_receipt_path,
        status=corpus.status,
        failure=None if corpus.status == "complete" else ";".join(corpus.residuals),
    )
    return _finish(run_receipt_path, receipt, 0 if corpus.status == "complete" else 4)


def _capture_args(
    *,
    url: str,
    output: Path,
    grid: bool = False,
    profile: str | None = None,
    review_posture: str | None = None,
) -> list[str]:
    args = [
        "--url",
        url,
        "--source-family",
        "retail_pdp",
        "--source-surface",
        "cloakbrowser_snapshot",
        "--decision-question",
        "What complete public Nordstrom US brand/PDP evidence is visible now?",
        "--output",
        str(output),
        "--capture-context",
        (
            "public logged-out Nordstrom US/USD capture; no VPN, proxy, stored "
            "browser profile, login, or retailer account"
        ),
        "--operator-category",
        "nordstrom_brand_corpus_cli_operator",
        "--nordstrom-country",
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
        "no earlier Nordstrom packet is being replaced",
        "--require-not-access-blocked",
    ]
    if grid:
        args.extend(["--settle-seconds", "8", "--scroll-passes", "2"])
    if profile is not None:
        args.extend(["--retail-capture-profile", profile, "--retention-mode", "raw"])
    if review_posture is not None:
        args.extend(
            [
                "--nordstrom-review-posture",
                review_posture,
                "--nordstrom-country-setup-timeout-seconds",
                "120",
                "--timeout-seconds",
                "180",
            ]
        )
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
            raise ValueError("capture_engine is supported only by the default runner")
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 3
    return int(result)


def _receipt(
    brand_url: str,
    authorization_url: str,
    authorization_statement: str,
    grid_packet: Path,
    projection_path: Path,
    input_mode: str,
    *,
    requested: int = 0,
    captured: int = 0,
    resumed: int = 0,
    pdp_directories: dict[str, str] | None = None,
    pdp_evidence_paths: dict[str, str] | None = None,
    deep_receipt_path: Path | None = None,
    corpus_receipt_path: Path | None = None,
    status: str,
    failure: str | None,
) -> NordstromBrandCorpusRunReceipt:
    return NordstromBrandCorpusRunReceipt(
        brand_url=brand_url,
        authorization_url=authorization_url,
        authorization_statement=authorization_statement,
        grid_packet_directory=str(grid_packet.resolve()),
        grid_projection_path=str(projection_path.resolve()),
        grid_input_mode=input_mode,
        requested_pdp_count=requested,
        captured_pdp_count=captured,
        resumed_pdp_count=resumed,
        pdp_packet_directories=pdp_directories or {},
        pdp_evidence_paths=pdp_evidence_paths or {},
        deep_receipt_path=str(deep_receipt_path.resolve()) if deep_receipt_path else None,
        corpus_receipt_path=(
            str(corpus_receipt_path.resolve()) if corpus_receipt_path else None
        ),
        status=status,
        failure=failure,
    )


def _finish(
    path: Path, receipt: NordstromBrandCorpusRunReceipt, exit_code: int
) -> tuple[int, NordstromBrandCorpusRunReceipt]:
    _write_new_json(path, receipt.model_dump(mode="json"))
    return exit_code, receipt


def _write_new_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brand-url", required=True)
    parser.add_argument("--authorization-url", required=True)
    parser.add_argument("--authorization-statement", required=True)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--review-limit", default=100, type=int)
    parser.add_argument("--resume-grid-packet", default=None, type=Path)
    parser.add_argument(
        "--resume-from",
        default=None,
        type=Path,
        action="append",
        help=(
            "Reuse only hash-verified, identity/seller/US/USD-valid PDP packets from "
            "an interrupted prior run; stale or incompatible packets fail closed."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    with ReusableCloakBrowserSnapshotEngine() as engine:
        exit_code, receipt = run_nordstrom_brand_corpus(
            brand_url=args.brand_url,
            authorization_url=args.authorization_url,
            authorization_statement=args.authorization_statement,
            output_root=args.output_root,
            review_limit=args.review_limit,
            resume_grid_packet=args.resume_grid_packet,
            resume_from=args.resume_from,
            capture_engine=engine,
        )
    print(json.dumps(receipt.model_dump(mode="json"), sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
