"""Operator runner: recompute every creator-metric rollup in the lake from its
source observations (``rollup_formula_revalidation``) and fail loudly on any
formula, lineage, or integrity mismatch.

Read-only: this runner writes nothing. Run it after any producer run (genesis or
live watch-packet), before trusting a snapshot regeneration, or on demand as the
formula-at-scale check across the whole longitudinal rollup history. CI never
resolves the real lake; the pure module is exercised against
``DataLakeRoot.for_test`` and only ``main``/``resolve`` touches the live lake.

Exit codes: 0 = every rollup recomputed clean; 2 = at least one failure (each is
printed per record -- one bad record never hides the rest); 2 with a distinct
message = the lake itself is unavailable.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from capture_spine.creator_profile_current.rollup_formula_revalidation import (
    revalidate_creator_metric_rollups,
)
from data_lake.root import DataLakeRoot, DataLakeRootError


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Recompute every creator-metric rollup Silver record in the data lake from its "
            "source observations and report formula/lineage/integrity mismatches."
        )
    )
    parser.add_argument("--data-root", default=None, help="Lake root; defaults to ORCA_DATA_ROOT.")
    parser.add_argument(
        "--platform",
        default=None,
        help="Optional platform_scope filter (e.g. youtube or instagram). Default: all rollups.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        data_root = DataLakeRoot.resolve(explicit=args.data_root)
    except DataLakeRootError as exc:
        parser.exit(status=2, message=f"data lake unavailable: {exc}\n")

    report = revalidate_creator_metric_rollups(data_root, platform=args.platform)

    for finding in report.findings:
        if finding.ok:
            continue
        print(
            f"FAIL {finding.record_id} account={finding.account_id} "
            f"recipe={finding.recipe_version}"
        )
        for failure in finding.failures:
            print(f"  - {failure}")

    scope = f" platform={args.platform}" if args.platform else ""
    print(
        f"revalidated {report.rollups_checked} rollup record(s){scope}: "
        f"{report.failures_total} failure(s)"
    )
    if not report.ok:
        parser.exit(
            status=2,
            message="creator rollup formula revalidation failed: see per-record failures above\n",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
