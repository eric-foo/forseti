from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.reddit_agent_view_ab_probe import (
    DEFAULT_FULL_NAME,
    DEFAULT_MANIFEST_NAME,
    DEFAULT_RECEIPT_NAME,
    DEFAULT_STRIPPED_NAME,
    RedditAgentViewABProbeFailure,
    build_reddit_agent_view_ab_probe,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Create local A/B probe prompts for comparing full vs stripped Reddit agent views."
        )
    )
    parser.add_argument(
        "--view-dir",
        type=Path,
        action="append",
        required=True,
        help=(
            "Directory containing reddit_agent_view_full.json and "
            "reddit_agent_view_stripped.json. Repeat for multiple cases."
        ),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--full-name", default=DEFAULT_FULL_NAME)
    parser.add_argument("--stripped-name", default=DEFAULT_STRIPPED_NAME)
    parser.add_argument("--manifest-name", default=DEFAULT_MANIFEST_NAME)
    parser.add_argument("--receipt-name", default=DEFAULT_RECEIPT_NAME)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        result = build_reddit_agent_view_ab_probe(
            view_directories=args.view_dir,
            output_directory=args.output_dir,
            full_name=args.full_name,
            stripped_name=args.stripped_name,
            manifest_name=args.manifest_name,
            receipt_name=args.receipt_name,
        )
    except RedditAgentViewABProbeFailure as exc:
        parser.exit(status=3, message=f"reddit agent view A/B probe refused ({exc.code}): {exc.message}\n")
    except Exception as exc:
        parser.exit(status=2, message=f"reddit agent view A/B probe failed: {exc}\n")

    print(result["manifest_path"])
    print(result["receipt_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
