from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.registry_match_preflight import (
    build_creator_registry_match_preflight_receipt,
    build_creator_registry_match_preflight_receipt_from_files,
    dump_creator_registry_match_preflight_receipt,
    has_blocking_preflight_results,
    load_creator_registry_match_candidates,
)
from data_lake.canonical_json import canonical_record_bytes
from data_lake.creator_registry import load_current_registry_preflight_view
from data_lake.root import DataLakeRoot
from harness_utils import utc_now_z


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Preflight candidate creator/account identities against the current "
            "Creator Registry before starting new capture."
        )
    )
    parser.add_argument("--candidates", type=Path, required=True, help="Candidate batch JSON.")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--data-root", help="Forseti data root; defaults to configured root.")
    source.add_argument(
        "--registry",
        type=Path,
        help="Test-only creator_profile_current JSON override.",
    )
    parser.add_argument("--output", type=Path, help="Write receipt JSON. Defaults to stdout.")
    parser.add_argument("--generated-at-utc", help="Receipt timestamp. Defaults to now.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    generated_at = args.generated_at_utc or utc_now_z()
    try:
        if args.registry is not None:
            receipt = build_creator_registry_match_preflight_receipt_from_files(
                candidate_path=args.candidates,
                registry_path=args.registry,
                generated_at_utc=generated_at,
            )
        else:
            registry = load_current_registry_preflight_view(
                DataLakeRoot.resolve(explicit=args.data_root)
            )
            receipt = build_creator_registry_match_preflight_receipt(
                candidates=load_creator_registry_match_candidates(args.candidates),
                registry_document=registry,
                registry_source_pointer=(
                    "indexes/derived_retrieval/creator_registry/CURRENT"
                ),
                registry_sha256=hashlib.sha256(
                    canonical_record_bytes(registry)
                ).hexdigest(),
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


if __name__ == "__main__":
    raise SystemExit(main())
