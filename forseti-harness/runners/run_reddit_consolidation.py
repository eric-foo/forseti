from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.reddit_consolidation import RedditConsolidationFailure, consolidate_reddit_packet


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Consolidate one existing Reddit Source Capture Packet into derived JSON and a receipt."
    )
    parser.add_argument("--packet", type=Path, required=True, help="Packet directory or manifest.json path.")
    parser.add_argument("--output-dir", type=Path, required=True, help="Separate directory for derived outputs.")
    parser.add_argument("--json-name", default="reddit_thread_consolidation.json")
    parser.add_argument("--receipt-name", default="reddit_thread_consolidation_receipt.md")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        result = consolidate_reddit_packet(
            packet_or_manifest_path=args.packet,
            output_directory=args.output_dir,
            json_name=args.json_name,
            receipt_name=args.receipt_name,
        )
    except RedditConsolidationFailure as exc:
        parser.exit(status=3, message=f"reddit consolidation refused ({exc.code}): {exc.message}\n")
    except Exception as exc:
        parser.exit(status=2, message=f"reddit consolidation failed: {exc}\n")

    print(result["json_path"])
    print(result["receipt_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
