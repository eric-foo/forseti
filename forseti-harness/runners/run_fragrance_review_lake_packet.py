"""Tee preserved fragrance review widget-response bytes into a Source Capture Packet.

Reads an existing rendered-widget companion receipt JSON (already captured; no
network here), extracts its review-bearing widget responses, and preserves their
EXACT raw bytes into the Data Lake (``--data-root`` / ``ORCA_DATA_ROOT``) or a
local output directory (``--output``). The two output modes are mutually
exclusive, mirroring ``run_source_capture_http_packet.py`` so the lake seam is
uniform across packet-producing runners.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.fragrance_rendered_widget_companion import FragranceRenderedWidgetCompanionReceipt
from source_capture.fragrance_review_lake import (
    FragranceReviewLakeInputError,
    write_fragrance_review_capture_packet,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


def run_fragrance_review_lake_packet(
    *,
    companion_receipt_path: Path,
    decision_question: str,
    capture_context: str,
    product_url: str | None = None,
    output_directory: Path | None = None,
    data_root: "DataLakeRoot | None" = None,
    session_id: str | None = None,
    warnings: Sequence[str] = (),
    limitations: Sequence[str] = (),
) -> tuple[int, str]:
    raw = json.loads(Path(companion_receipt_path).read_text(encoding="utf-8"))
    receipt = FragranceRenderedWidgetCompanionReceipt.model_validate(raw)
    effective_product_url = product_url or receipt.product_url

    try:
        result = write_fragrance_review_capture_packet(
            output_directory=output_directory,
            data_root=data_root,
            widget_responses=receipt.widget_responses,
            product_url=effective_product_url,
            decision_question=decision_question,
            capture_context=capture_context,
            session_id=session_id,
            warnings=list(warnings),
            limitations=list(limitations),
        )
    except FragranceReviewLakeInputError as exc:
        return 3, str(exc)
    return 0, result.output_directory


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Preserve the raw review widget-response bytes from a fragrance rendered-widget "
            "companion receipt into a Source Capture Packet (Data Lake or local output)."
        )
    )
    parser.add_argument("--companion-receipt", required=True, type=Path)
    parser.add_argument("--product-url", default=None)
    parser.add_argument("--decision-question", default="fragrance review demand evidence")
    parser.add_argument(
        "--capture-context",
        default="fragrance rendered-widget review-response bytes preserved into the lake",
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--data-root",
        default=None,
        help=(
            "Commit into the Orca data lake at this root; explicit --data-root is mutually "
            "exclusive with --output. ORCA_DATA_ROOT is used only when --output is omitted."
        ),
    )
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--warning", action="append", default=[])
    parser.add_argument("--limitation", action="append", default=[])
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        data_root = None
        output_directory = args.output
        if output_directory is not None and args.data_root is not None:
            parser.exit(
                status=2,
                message="exactly one of --output or --data-root/ORCA_DATA_ROOT is required\n",
            )
        data_root_requested = args.data_root is not None or (
            output_directory is None and os.environ.get("ORCA_DATA_ROOT")
        )
        if data_root_requested:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)
            output_directory = None
        if (output_directory is None) == (data_root is None):
            parser.exit(
                status=2,
                message="exactly one of --output or --data-root/ORCA_DATA_ROOT is required\n",
            )
        exit_code, message = run_fragrance_review_lake_packet(
            companion_receipt_path=args.companion_receipt,
            decision_question=args.decision_question,
            capture_context=args.capture_context,
            product_url=args.product_url,
            output_directory=output_directory,
            data_root=data_root,
            session_id=args.session_id,
            warnings=args.warning,
            limitations=args.limitation,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"fragrance review lake tee failed: {exc}\n")
    except Exception as exc:  # noqa: BLE001 - surface any runner failure as a non-zero exit
        parser.exit(status=3, message=f"fragrance review lake tee failed: {exc}\n")

    if exit_code == 0:
        print(message)
        return 0

    parser.exit(status=exit_code, message=f"fragrance review lake tee failed: {message}\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
