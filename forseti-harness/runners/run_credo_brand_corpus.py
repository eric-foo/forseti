"""Capture one complete public Credo brand grid, every PDP, and one deep PDP."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Sequence

from pydantic import Field

from runners import run_source_capture_http_packet as http_writer
from schemas.case_models import StrictModel
from source_capture.credo_brand_grid import (
    CREDO_GRID_PARSER_VERSION,
    CredoBrandGridState,
    canonical_credo_collection_url,
    load_credo_brand_grid_state,
)
from source_capture.credo_yotpo_deep_capture import (
    CredoYotpoBinding,
    CredoYotpoDeepCaptureReceipt,
    capture_credo_yotpo_deep,
    parse_credo_yotpo_binding,
)
from source_capture.models import VisibleFactStatus
from source_capture.retail_grid_projection import (
    load_verified_source_capture_packet_directory,
)


RUN_SCHEMA_VERSION = "credo_brand_corpus_run_v1"
CORPUS_SCHEMA_VERSION = "credo_corpus_verification_v1"


class CredoPdpReceipt(StrictModel):
    handle: str
    product_url: str
    canonical_url: str
    product_name: str
    brand_name: str
    product_sku: str | None
    packet_directory: str
    response_sha256: str
    review_count: int
    review_store_id: str | None
    review_product_id: str | None


class CredoCorpusReceipt(StrictModel):
    schema_version: str = CORPUS_SCHEMA_VERSION
    brand_url: str
    grid_product_count: int
    pdp_count: int
    grid_handles: list[str]
    pdp_handles: list[str]
    selected_deep_handle: str
    deep_declared_review_count: int
    deep_most_relevant_count: int
    deep_most_recent_count: int
    transport_posture: str
    status: str
    residuals: list[str] = Field(default_factory=list)


class CredoBrandCorpusRunReceipt(StrictModel):
    schema_version: str = RUN_SCHEMA_VERSION
    brand_url: str
    authorization_url: str
    authorization_evidence: str
    authorization_observed_date: str
    grid_packet_directory: str
    grid_receipt_path: str
    grid_input_mode: str
    grid_parser_version: str = CREDO_GRID_PARSER_VERSION
    requested_pdp_count: int = 0
    captured_pdp_count: int = 0
    pdp_packet_directories: dict[str, str] = Field(default_factory=dict)
    deep_receipt_path: str | None = None
    corpus_receipt_path: str | None = None
    proxy_used: bool = False
    persisted_profile_used: bool = False
    status: str
    failure: str | None = None


def run_credo_brand_corpus(
    *,
    brand_url: str,
    output_root: Path,
    authorization_url: str,
    authorization_evidence: str,
    authorization_observed_date: str,
    review_limit: int = 100,
    resume_grid_packet: Path | None = None,
) -> tuple[int, CredoBrandCorpusRunReceipt]:
    if output_root.exists():
        raise ValueError(f"output root already exists; refusing overwrite: {output_root}")
    canonical_brand_url = canonical_credo_collection_url(brand_url)
    if canonical_brand_url is None:
        raise ValueError("brand_url must be an exact Credo collection URL")
    if authorization_url != "https://www.tower28beauty.com/pages/stores":
        raise ValueError("Tower 28 corpus requires the current brand-owned stores source")
    if "CredoBeauty.com" not in authorization_evidence:
        raise ValueError("authorization evidence must explicitly name CredoBeauty.com")
    if not 1 <= review_limit <= 100:
        raise ValueError("review_limit must be between 1 and 100")
    output_root.mkdir(parents=True)
    grid_packet = (
        resume_grid_packet.resolve()
        if resume_grid_packet is not None
        else output_root / "grid-packet"
    )
    grid_receipt_path = output_root / "grid-receipt.json"
    corpus_receipt_path = output_root / "corpus-receipt.json"
    deep_receipt_path = output_root / "deep-pdp.json"
    run_receipt_path = output_root / "run-receipt.json"
    pdp_root = output_root / "pdp"

    try:
        if resume_grid_packet is None:
            exit_code, message = _capture_packet(
                url=canonical_brand_url,
                output=grid_packet,
                credo_market=None,
            )
            if exit_code:
                raise _CaptureFailure(f"grid_capture_failed:exit={exit_code}:{message}", exit_code)
        grid_state = _load_grid_packet(grid_packet, canonical_brand_url)
        _write_new_json(grid_receipt_path, _grid_json(grid_state))
    except Exception as exc:
        exit_code = exc.exit_code if isinstance(exc, _CaptureFailure) else 3
        receipt = _run_receipt(
            brand_url=canonical_brand_url,
            authorization_url=authorization_url,
            authorization_evidence=authorization_evidence,
            authorization_observed_date=authorization_observed_date,
            grid_packet=grid_packet,
            grid_receipt_path=grid_receipt_path,
            resumed=resume_grid_packet is not None,
            status="partial",
            failure=f"credo_grid_failed:{type(exc).__name__}:{exc}",
        )
        _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
        return exit_code, receipt

    pdps: list[CredoPdpReceipt] = []
    bindings: list[CredoYotpoBinding] = []
    packet_directories: dict[str, str] = {}
    for card in grid_state.cards:
        packet_directory = pdp_root / card.handle
        exit_code, message = _capture_packet(
            url=card.product_url,
            output=packet_directory,
            credo_market="US",
        )
        if exit_code:
            receipt = _run_receipt(
                brand_url=canonical_brand_url,
                authorization_url=authorization_url,
                authorization_evidence=authorization_evidence,
                authorization_observed_date=authorization_observed_date,
                grid_packet=grid_packet,
                grid_receipt_path=grid_receipt_path,
                resumed=resume_grid_packet is not None,
                requested_pdp_count=len(grid_state.cards),
                captured_pdp_count=len(pdps),
                pdp_packet_directories=packet_directories,
                status="partial",
                failure=f"credo_pdp_capture_failed:{card.handle}:exit={exit_code}:{message}",
            )
            _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
            return exit_code, receipt
        pdp, binding = _load_pdp_packet(packet_directory, expected_handle=card.handle)
        pdps.append(pdp)
        packet_directories[card.handle] = str(packet_directory.resolve())
        if binding is not None:
            bindings.append(binding)

    try:
        candidate = min(
            bindings,
            key=lambda item: (
                -item.declared_review_count,
                next(card.grid_position for card in grid_state.cards if card.handle == item.handle),
                item.handle,
            ),
        )
        deep = capture_credo_yotpo_deep(binding=candidate, review_limit=review_limit)
        _write_new_json(deep_receipt_path, deep.model_dump(mode="json"))
        corpus = _verify_corpus(grid_state=grid_state, pdps=pdps, deep=deep)
        _write_new_json(corpus_receipt_path, corpus.model_dump(mode="json"))
    except Exception as exc:
        receipt = _run_receipt(
            brand_url=canonical_brand_url,
            authorization_url=authorization_url,
            authorization_evidence=authorization_evidence,
            authorization_observed_date=authorization_observed_date,
            grid_packet=grid_packet,
            grid_receipt_path=grid_receipt_path,
            resumed=resume_grid_packet is not None,
            requested_pdp_count=len(grid_state.cards),
            captured_pdp_count=len(pdps),
            pdp_packet_directories=packet_directories,
            deep_receipt_path=deep_receipt_path if deep_receipt_path.exists() else None,
            status="partial",
            failure=f"credo_deep_or_corpus_failed:{type(exc).__name__}:{exc}",
        )
        _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
        return 3, receipt

    status = "complete" if corpus.status == "complete" else "partial"
    receipt = _run_receipt(
        brand_url=canonical_brand_url,
        authorization_url=authorization_url,
        authorization_evidence=authorization_evidence,
        authorization_observed_date=authorization_observed_date,
        grid_packet=grid_packet,
        grid_receipt_path=grid_receipt_path,
        resumed=resume_grid_packet is not None,
        requested_pdp_count=len(grid_state.cards),
        captured_pdp_count=len(pdps),
        pdp_packet_directories=packet_directories,
        deep_receipt_path=deep_receipt_path,
        corpus_receipt_path=corpus_receipt_path,
        status=status,
        failure=None if status == "complete" else ";".join(corpus.residuals),
    )
    _write_new_json(run_receipt_path, receipt.model_dump(mode="json"))
    return (0 if status == "complete" else 4), receipt


def _capture_packet(*, url: str, output: Path, credo_market: str | None) -> tuple[int, str]:
    return http_writer.run_source_capture_http_packet(
        url=url,
        source_family="retail_grid" if credo_market is None else "retail_pdp",
        source_surface="direct_http",
        decision_question=(
            "Capture the exact complete Credo brand grid."
            if credo_market is None
            else "Capture one exact Credo US/USD PDP for corpus reconciliation."
        ),
        output_directory=output,
        capture_context="Credo Tower 28 authorized-brand corpus dogfood",
        operator_category="implementation_dogfood",
        capture_mode=http_writer.CaptureModeCategory.STRUCTURED_ACCESS,
        session_id=None,
        actor_audience_context=None,
        visible_mode_changes=[],
        source_publication_or_event=None,
        source_edit_or_version=None,
        cutoff_posture=None,
        recapture_time=None,
        re_capture_relationship=None,
        warnings=[],
        limitations=["One-brand proof; not broad Credo reliability or production readiness."],
        timeout_seconds=30,
        max_bytes=5_000_000,
        credo_market=credo_market,
    )


def _load_grid_packet(packet_directory: Path, brand_url: str) -> CredoBrandGridState:
    packet, bodies = load_verified_source_capture_packet_directory(packet_directory)
    if (
        packet.source_locator.status != VisibleFactStatus.KNOWN
        or packet.source_locator.value != brand_url
    ):
        raise ValueError("grid packet does not bind the requested Credo collection")
    body = _single_body(packet, bodies)
    return load_credo_brand_grid_state(body.decode("utf-8", errors="replace"), requested_url=brand_url)


def _load_pdp_packet(
    packet_directory: Path,
    *,
    expected_handle: str,
) -> tuple[CredoPdpReceipt, CredoYotpoBinding | None]:
    packet, bodies = load_verified_source_capture_packet_directory(packet_directory)
    body_bytes = _single_body(packet, bodies)
    metadata_files = [
        item
        for item in packet.preserved_files
        if item.relative_packet_path.replace("\\", "/").endswith("http_response_metadata.json")
    ]
    if len(metadata_files) != 1:
        raise ValueError("Credo PDP packet requires one HTTP metadata file")
    metadata = json.loads(bodies[metadata_files[0].file_id])
    if (
        metadata.get("pin_confirmed") is not True
        or metadata.get("bound_product_handle") != expected_handle
        or metadata.get("country_code_confirmed") != "US"
        or metadata.get("currency_code_confirmed") != "USD"
        or str(metadata.get("brand_name", "")).casefold() != "tower 28"
    ):
        raise ValueError(f"Credo PDP packet fails exact market/brand identity: {expected_handle}")
    product_url = f"https://credobeauty.com/products/{expected_handle}"
    if metadata.get("canonical_url") != product_url:
        raise ValueError(f"Credo PDP canonical URL mismatch: {expected_handle}")
    binding = parse_credo_yotpo_binding(
        body_bytes.decode("utf-8", errors="replace"),
        source_url=product_url,
    )
    return (
        CredoPdpReceipt(
            handle=expected_handle,
            product_url=product_url,
            canonical_url=product_url,
            product_name=str(metadata["product_name"]),
            brand_name=str(metadata["brand_name"]),
            product_sku=(
                str(metadata["product_sku"]) if metadata.get("product_sku") is not None else None
            ),
            packet_directory=str(packet_directory.resolve()),
            response_sha256=hashlib.sha256(body_bytes).hexdigest(),
            review_count=binding.declared_review_count if binding is not None else 0,
            review_store_id=binding.store_id if binding is not None else None,
            review_product_id=binding.product_id if binding is not None else None,
        ),
        binding,
    )


def _single_body(packet, bodies: dict[str, bytes]) -> bytes:
    body_files = [
        item
        for item in packet.preserved_files
        if item.relative_packet_path.replace("\\", "/").endswith("http_response_body.bin")
    ]
    if len(body_files) != 1:
        raise ValueError("packet requires exactly one HTTP response body")
    return bodies[body_files[0].file_id]


def _verify_corpus(
    *,
    grid_state: CredoBrandGridState,
    pdps: list[CredoPdpReceipt],
    deep: CredoYotpoDeepCaptureReceipt,
) -> CredoCorpusReceipt:
    grid_handles = [card.handle for card in grid_state.cards]
    pdp_handles = [pdp.handle for pdp in pdps]
    residuals: list[str] = []
    if grid_handles != pdp_handles:
        residuals.append("grid_to_pdp_order_or_identity_mismatch")
    if len(set(pdp_handles)) != len(pdp_handles):
        residuals.append("duplicate_pdp_identity")
    if deep.handle not in grid_handles:
        residuals.append("deep_pdp_not_in_grid")
    highest = max((pdp.review_count for pdp in pdps), default=-1)
    selected = next((pdp for pdp in pdps if pdp.handle == deep.handle), None)
    if selected is None or selected.review_count != highest:
        residuals.append("deep_pdp_is_not_highest_review_candidate")
    if deep.status != "complete":
        residuals.extend(deep.residuals or ["deep_receipt_partial"])
    return CredoCorpusReceipt(
        brand_url=grid_state.source_url,
        grid_product_count=len(grid_handles),
        pdp_count=len(pdp_handles),
        grid_handles=grid_handles,
        pdp_handles=pdp_handles,
        selected_deep_handle=deep.handle,
        deep_declared_review_count=deep.declared_review_count,
        deep_most_relevant_count=len(deep.most_relevant_review_ids),
        deep_most_recent_count=len(deep.most_recent_review_ids),
        transport_posture=deep.transport_posture,
        status="complete" if not residuals else "partial",
        residuals=residuals,
    )


def _grid_json(state: CredoBrandGridState) -> dict[str, object]:
    return {
        "schema_version": CREDO_GRID_PARSER_VERSION,
        "source_url": state.source_url,
        "collection_id": state.collection_id,
        "collection_title": state.collection_title,
        "country_code": state.country_code,
        "currency_code": state.currency_code,
        "declared_shopify_product_count": len(state.cards),
        "observed_dom_product_count": len(state.cards),
        "pagination_next_url": state.pagination_next_url,
        "status": "complete",
        "cards": [
            {
                "grid_position": card.grid_position,
                "product_id": card.product_id,
                "handle": card.handle,
                "product_url": card.product_url,
                "vendor": card.vendor,
            }
            for card in state.cards
        ],
        "residuals": [],
    }


def _run_receipt(
    *,
    brand_url: str,
    authorization_url: str,
    authorization_evidence: str,
    authorization_observed_date: str,
    grid_packet: Path,
    grid_receipt_path: Path,
    resumed: bool,
    requested_pdp_count: int = 0,
    captured_pdp_count: int = 0,
    pdp_packet_directories: dict[str, str] | None = None,
    deep_receipt_path: Path | None = None,
    corpus_receipt_path: Path | None = None,
    status: str,
    failure: str | None,
) -> CredoBrandCorpusRunReceipt:
    return CredoBrandCorpusRunReceipt(
        brand_url=brand_url,
        authorization_url=authorization_url,
        authorization_evidence=authorization_evidence,
        authorization_observed_date=authorization_observed_date,
        grid_packet_directory=str(grid_packet.resolve()),
        grid_receipt_path=str(grid_receipt_path.resolve()),
        grid_input_mode="verified_raw_replay" if resumed else "live_capture",
        requested_pdp_count=requested_pdp_count,
        captured_pdp_count=captured_pdp_count,
        pdp_packet_directories=pdp_packet_directories or {},
        deep_receipt_path=(
            str(deep_receipt_path.resolve()) if deep_receipt_path is not None else None
        ),
        corpus_receipt_path=(
            str(corpus_receipt_path.resolve()) if corpus_receipt_path is not None else None
        ),
        status=status,
        failure=failure,
    )


def _write_new_json(path: Path, value: object) -> None:
    if path.exists():
        raise ValueError(f"refusing to overwrite existing receipt: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class _CaptureFailure(ValueError):
    def __init__(self, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brand-url", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--authorization-url", required=True)
    parser.add_argument("--authorization-evidence", required=True)
    parser.add_argument("--authorization-observed-date", required=True)
    parser.add_argument("--review-limit", type=int, default=100)
    parser.add_argument("--resume-grid-packet", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    exit_code, receipt = run_credo_brand_corpus(
        brand_url=args.brand_url,
        output_root=args.output,
        authorization_url=args.authorization_url,
        authorization_evidence=args.authorization_evidence,
        authorization_observed_date=args.authorization_observed_date,
        review_limit=args.review_limit,
        resume_grid_packet=args.resume_grid_packet,
    )
    print(receipt.model_dump_json(indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
