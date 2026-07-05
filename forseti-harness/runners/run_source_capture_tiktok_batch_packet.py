"""CLI: admit a sanitized TikTok creator batch from parsed staging results."""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.tiktok import COMPLETE_LANE_NOTE, write_tiktok_batch_packet


def run_source_capture_tiktok_batch_packet(
    *,
    creator_handle: str,
    creator_profile_url: str,
    grid_result_json_path: Path,
    cadence_result_json_paths: Sequence[Path],
    output_directory: Path | None = None,
    data_root=None,
    decision_question: str,
    batch_label: str = "tiktok_creator_batch",
) -> tuple[int, str]:
    if (output_directory is None) == (data_root is None):
        raise ValueError("exactly one of output_directory or data_root is required")
    if not cadence_result_json_paths:
        raise ValueError("at least one --cadence-result-json path is required")

    grid_bytes = grid_result_json_path.read_bytes()
    cadence_bytes = [path.read_bytes() for path in cadence_result_json_paths]
    receipts = [_source_receipt(grid_result_json_path, grid_bytes, "grid_result_json")]
    receipts.extend(
        _source_receipt(path, raw, f"cadence_result_json_{index + 1}")
        for index, (path, raw) in enumerate(zip(cadence_result_json_paths, cadence_bytes, strict=True))
    )

    return write_tiktok_batch_packet(
        creator_handle=creator_handle,
        creator_profile_url=creator_profile_url,
        grid_result_json=grid_bytes,
        cadence_result_jsons=cadence_bytes,
        output_directory=output_directory,
        data_root=data_root,
        decision_question=decision_question,
        batch_label=batch_label,
        source_file_receipts=receipts,
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Admit sanitized parsed TikTok creator-batch staging results into a SourceCapturePacket.",
        epilog=f"Complete-lane note: {COMPLETE_LANE_NOTE}",
    )
    parser.add_argument("--creator-handle", required=True, help="TikTok handle, with or without leading @.")
    parser.add_argument("--creator-profile-url", required=True, help="Canonical TikTok profile URL without query string.")
    parser.add_argument("--grid-result-json", required=True, type=Path)
    parser.add_argument(
        "--cadence-result-json",
        required=True,
        action="append",
        type=Path,
        help="Parsed cadence result JSON. Repeat for split runs such as N5 and N25.",
    )
    target = parser.add_mutually_exclusive_group(required=False)
    target.add_argument("--output", type=Path, default=None)
    target.add_argument(
        "--data-root",
        default=None,
        help="Commit into the Forseti data lake at this root; FORSETI_DATA_ROOT is used only when --output is omitted; legacy ORCA_DATA_ROOT is also accepted.",
    )
    parser.add_argument("--batch-label", default="tiktok_creator_batch")
    parser.add_argument(
        "--decision-question",
        default="Admit TikTok creator-batch comment, subtitle, source-text, and typed extraction seed signals.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        data_root = None
        data_root_requested = args.data_root is not None or (args.output is None and (os.environ.get("FORSETI_DATA_ROOT") or os.environ.get("ORCA_DATA_ROOT")))
        if args.output is not None and args.data_root is not None:
            parser.exit(status=2, message="source capture tiktok batch failed: supply only one of --output or --data-root\n")
        if args.output is None and not data_root_requested:
            parser.exit(
                status=2,
                message="source capture tiktok batch failed: exactly one of --output or --data-root/FORSETI_DATA_ROOT/ORCA_DATA_ROOT is required\n",
            )
        if data_root_requested:
            from data_lake.root import DataLakeRoot

            data_root = DataLakeRoot.resolve(explicit=args.data_root)
        exit_code, message = run_source_capture_tiktok_batch_packet(
            creator_handle=args.creator_handle,
            creator_profile_url=args.creator_profile_url,
            grid_result_json_path=args.grid_result_json,
            cadence_result_json_paths=args.cadence_result_json,
            output_directory=args.output if data_root is None else None,
            data_root=data_root,
            decision_question=args.decision_question,
            batch_label=args.batch_label,
        )
    except ValueError as exc:
        parser.exit(status=2, message=f"source capture tiktok batch failed: {exc}\n")
    except Exception as exc:  # noqa: BLE001 - surface capture/lake failures visibly
        parser.exit(status=3, message=f"source capture tiktok batch failed: {type(exc).__name__}: {exc}\n")

    if exit_code == 0:
        print(COMPLETE_LANE_NOTE)
        print(message)
        return 0
    parser.exit(status=exit_code, message=f"source capture tiktok batch failed: {message}\n")
    return exit_code


def _source_receipt(path: Path, raw: bytes, role: str) -> dict[str, object]:
    resolved = str(path.resolve())
    return {
        "role": role,
        "file_name": path.name,
        "sha256": hashlib.sha256(raw).hexdigest(),
        "size_bytes": len(raw),
        "source_path_sha256": hashlib.sha256(resolved.encode("utf-8")).hexdigest(),
    }


if __name__ == "__main__":
    raise SystemExit(main())
