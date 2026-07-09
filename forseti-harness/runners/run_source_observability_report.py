from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

import yaml
from pydantic import ValidationError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from source_observability.checker import run_source_observability_checks
from source_observability.models import SourceObservabilityRecord


NON_CLAIMS = [
    "not capture validation",
    "not capture readiness",
    "not categorical ECR receipt",
    "not Cleaning output",
    "not Judgment output",
    "not source acquisition",
    "not source-access handling",
    "not archive retrieval",
    "not media capture",
    "not browser automation",
    "not source-quality scoring",
]


def load_operator_records(path: Path) -> list[SourceObservabilityRecord]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    raw_records = _extract_records(payload)
    return [SourceObservabilityRecord.model_validate(record) for record in raw_records]


def build_source_observability_report(
    records: Sequence[SourceObservabilityRecord],
) -> dict[str, Any]:
    result = run_source_observability_checks(list(records))
    return {
        "report_type": "source_observability_limitations_report",
        "record_count": result.record_count,
        "limitation_count": len(result.limitations),
        "has_visible_limitations": result.has_visible_limitations,
        "record_summaries": [_record_summary(record) for record in records],
        "limitations": [
            limitation.model_dump(mode="json") for limitation in result.limitations
        ],
        "non_claims": NON_CLAIMS,
    }


def write_source_observability_report(input_path: Path, output_path: Path | None) -> dict[str, Any]:
    records = load_operator_records(input_path)
    report = build_source_observability_report(records)
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if output_path is None:
        print(rendered)
    else:
        output_path.write_text(f"{rendered}\n", encoding="utf-8")
    return report


def _extract_records(payload: object) -> list[object]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return payload["records"]
    raise ValueError("input must be a YAML/JSON list or a mapping with a records list")


def _record_summary(record: SourceObservabilityRecord) -> dict[str, Any]:
    return record.model_dump(mode="json")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build a local source-observability limitations report from operator-authored records."
    )
    parser.add_argument("input_path", type=Path, help="Local YAML/JSON file containing records.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional local JSON report path. Defaults to stdout.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        write_source_observability_report(args.input_path, args.output)
    except (OSError, ValueError, ValidationError) as exc:
        parser.exit(2, f"source observability report failed: {exc}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
