from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.reddit_agent_view import RedditAgentViewFailure, build_reddit_agent_views


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Create full and stripped agent-consumption views from an existing Reddit JSON artifact."
        )
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help=(
            "Existing reddit_thread_consolidation.json, reddit_candidate_url_intake.json, "
            "or reddit_graph_frontier_register.json."
        ),
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--full-name", default="reddit_agent_view_full.json")
    parser.add_argument("--stripped-name", default="reddit_agent_view_stripped.json")
    parser.add_argument("--receipt-name", default="reddit_agent_view_receipt.md")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        result = build_reddit_agent_views(
            input_json_path=args.input,
            output_directory=args.output_dir,
            full_name=args.full_name,
            stripped_name=args.stripped_name,
            receipt_name=args.receipt_name,
        )
    except RedditAgentViewFailure as exc:
        parser.exit(status=3, message=f"reddit agent view refused ({exc.code}): {exc.message}\n")
    except Exception as exc:
        parser.exit(status=2, message=f"reddit agent view failed: {exc}\n")

    print(result["full_json_path"])
    print(result["stripped_json_path"])
    print(result["receipt_path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
