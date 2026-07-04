from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.registry_match_preflight import (
    build_creator_registry_match_preflight_receipt_from_files,
    dump_creator_registry_match_preflight_receipt,
    has_blocking_preflight_results,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = (
    ROOT
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "creator_registry"
    / "creator_profile_current_view_v0.json"
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Preflight candidate creator/account identities against the current "
            "Creator Registry before starting new capture."
        )
    )
    parser.add_argument("--candidates", type=Path, required=True, help="Candidate batch JSON.")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY, help="creator_profile_current view JSON.")
    parser.add_argument("--output", type=Path, help="Write receipt JSON. Defaults to stdout.")
    parser.add_argument("--generated-at-utc", help="Receipt timestamp. Defaults to now.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    generated_at = args.generated_at_utc or _now_utc()
    try:
        receipt = build_creator_registry_match_preflight_receipt_from_files(
            candidate_path=args.candidates,
            registry_path=args.registry,
            generated_at_utc=generated_at,
        )
        rendered = dump_creator_registry_match_preflight_receipt(receipt)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8", newline="\n")
            print(args.output)
        else:
            print(rendered, end="")
        return 2 if has_blocking_preflight_results(receipt) else 0
    except Exception as exc:
        parser.exit(status=2, message=f"creator registry match preflight failed: {exc}\n")


def _now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
