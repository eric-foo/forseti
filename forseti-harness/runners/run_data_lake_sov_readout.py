"""Share-of-voice readout command (on-demand-first metric-family surface).

Computes a ``source_backed_brand_line_share_of_voice`` readout from committed
lake records per the field contract
(``core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md``)
and the seam contract's on-demand-first metrics policy.

Modes:

- **default (on demand)**: ``--spec <spec.json>`` — compute the readout and
  print it to stdout; nothing is written into the lake.
- **--materialize**: additionally persist the readout as a rebuildable,
  manifest-backed, non-authoritative cache under
  ``indexes/derived_retrieval/metric_family/<family>/<readout_id>/``.
- **--prove-rebuildability**: verification only (no ``--spec``): every
  materialized readout is regenerated under its stored manifest's recorded
  spec + stamp and byte-compared (never self-comparing).

Spec file shape (JSON object):

    {
      "platform": "youtube",
      "cohort": {
        "cohort_id": "...", "definition": "...",
        "member_refs": [{"namespace": "youtube", "kind": "transcript", "native_id": "..."}]
      },
      "coverage_window": {"start": "...", "end": "...",
                          "window_basis": "capture_time" | "source_publication_time"},
      "cohort_selection": "<version or manifest identity>",
      "comparison_set": {  # optional; required for zero rows to exist at all
        "brand_line_keys": [["Brand", "Line"], ...],
        "basis": "...", "comparison_set_ref": "...", "version": "..."
      }
    }
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.root import DataLakeRoot, DataLakeRootError
from data_lake.sov_readout import (
    compute_sov_readout,
    materialize_sov_readout,
    prove_sov_rebuildability,
)


def _load_spec(path: str) -> dict:
    try:
        spec = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise DataLakeRootError(f"unreadable sov spec file {path}: {exc}") from exc
    if not isinstance(spec, dict):
        raise DataLakeRootError(f"sov spec file must contain a JSON object: {path}")
    return spec


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Compute a source-backed brand/line share-of-voice readout from committed "
            "lake records (on demand by default; optionally materialized as a "
            "rebuildable manifest-backed cache)."
        )
    )
    parser.add_argument(
        "--root",
        "--data-root",
        dest="data_root",
        help="Explicit Forseti data root path (falls back to FORSETI_DATA_ROOT (legacy ORCA_DATA_ROOT)).",
    )
    parser.add_argument(
        "--spec",
        help="Path to the readout spec JSON (required unless --prove-rebuildability).",
    )
    parser.add_argument(
        "--materialize",
        action="store_true",
        help="Persist the readout as a rebuildable cache under indexes/derived_retrieval/.",
    )
    parser.add_argument(
        "--prove-rebuildability",
        action="store_true",
        help=(
            "Verify every materialized share-of-voice readout regenerates "
            "byte-identically under its stored manifest (no --spec needed)."
        ),
    )
    args = parser.parse_args(argv)

    report: dict = {
        "metric_family": "source_backed_brand_line_share_of_voice",
        "prove": args.prove_rebuildability,
        "materialize": args.materialize,
    }
    if args.prove_rebuildability and (args.spec or args.materialize):
        parser.error("--prove-rebuildability takes no --spec/--materialize")
    if not args.prove_rebuildability and not args.spec:
        parser.error("--spec is required unless --prove-rebuildability is given")

    try:
        root = DataLakeRoot.resolve(explicit=args.data_root)
        if args.prove_rebuildability:
            proof = prove_sov_rebuildability(root)
            report.update(proof)
        elif args.materialize:
            report.update(materialize_sov_readout(root, _load_spec(args.spec)))
        else:
            view, _source_refs = compute_sov_readout(root, _load_spec(args.spec))
            report["status"] = "computed"
            report["readout"] = view
    except DataLakeRootError as exc:
        report["status"] = "error"
        report["error"] = str(exc)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 2

    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] in {"computed", "materialized", "proven"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
