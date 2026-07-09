from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

import yaml
from pydantic import ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_capture.source_quality import LIFECYCLE_STATES, build_source_quality_report_skeleton


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a Mini God-Tier source-quality report skeleton from one existing Source Capture Packet manifest."
    )
    parser.add_argument("--packet", type=Path, required=True, help="Packet directory or manifest.json path.")
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-language-anchor", action="append", default=[])
    parser.add_argument("--coverage-or-drift-note")
    parser.add_argument(
        "--lifecycle-state",
        choices=sorted(LIFECYCLE_STATES),
        default="scratch",
    )
    parser.add_argument("--lifecycle-decision-reference")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        skeleton = build_source_quality_report_skeleton(
            packet_or_manifest_path=args.packet,
            source_id=args.source_id,
            source_language_anchors=args.source_language_anchor,
            coverage_or_drift_note=args.coverage_or_drift_note,
            lifecycle_state=args.lifecycle_state,
            lifecycle_decision_reference=args.lifecycle_decision_reference,
        )
        if args.output.exists():
            raise ValueError(f"output already exists: {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(yaml.safe_dump(skeleton, sort_keys=False), encoding="utf-8")
    except ValidationError as exc:
        parser.exit(status=1, message=f"source-quality skeleton manifest validation failed: {exc}\n")
    except Exception as exc:
        parser.exit(status=2, message=f"source-quality skeleton failed: {exc}\n")

    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
