"""The contract-pinned lake indexes rebuild command (runner packaging).

Shape pinned by the derived-layout contract:
``lake indexes rebuild --root <FORSETI_DATA_ROOT> --target
availability|creator_vault|derived_retrieval|all --prove-rebuildability`` — the semantics
are the contract; the argparse runner is the incumbent CLI packaging
(consumption seam contract, Rebuild Command Binding).

Modes:

- **rebuild** (default): regenerate the requested index tier(s) from committed
  material. ``availability`` delegates to ``DataLakeRoot.rebuild_availability``;
  ``creator_vault`` refreshes only the per-account metric package from the
  creator-metric observation lane; ``derived_retrieval`` rewrites the full
  generated lake map and Creator Vault package under one generation stamp.
- **--prove-rebuildability**: verification. ``derived_retrieval`` is proven
  read-only — every stored view is regenerated under the stamps its stored
  manifest recorded and byte-compared (a rebuild is never compared against
  itself). ``availability`` is proven by before/after byte comparison around
  an in-place rebuild (mutation-to-truth): any drift means the stored index
  was smuggling non-regenerable or stale state and is reported as a failure.
- **--prove-incremental-equality**: read-only Stage 1 gate. Generate the lake
  map once through the incremental classification cache and once through a
  full cold classification sweep under one stamp, then byte-compare every
  view and manifest.
- **--audit-source-integrity**: read-only cold source re-hash and byte proof,
  intended for the owner-operated periodic integrity schedule.

Owner-operated one-shot daily Creator Vault fallback:

``python runners/run_data_lake_indexes_rebuild.py --root F:\\forseti-data-lake --target creator_vault``

The generic lake-map views remain explicitly rebuildable with stored policy
pins when their freshness is required:

``python runners/run_data_lake_indexes_rebuild.py --root F:\\forseti-data-lake --target derived_retrieval --use-stored-product-mention-policy``

Periodic integrity command (scheduling remains owner-operated):

``python runners/run_data_lake_indexes_rebuild.py --root F:\\forseti-data-lake --target derived_retrieval --audit-source-integrity``
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.derived_retrieval_views import (
    audit_derived_retrieval_source_integrity,
    prove_creator_vault_rebuildability,
    prove_incremental_rebuild_equality,
    prove_derived_retrieval_rebuildability,
    rebuild_creator_vault,
    rebuild_derived_retrieval,
)
from data_lake.product_mention_selection import normalize_product_mention_policy
from data_lake.root import DataLakeRoot, DataLakeRootError


def _availability_snapshot(root: DataLakeRoot) -> dict[str, bytes]:
    availability_dir = root.path / "indexes" / "availability"
    if not availability_dir.is_dir():
        return {}
    return {
        entry.name: entry.read_bytes()
        for entry in sorted(availability_dir.iterdir())
        if entry.is_file()
    }


def _rebuild_availability(root: DataLakeRoot, *, prove: bool) -> dict:
    if not prove:
        return {"status": "rebuilt", "entry_count": root.rebuild_availability()}
    before = _availability_snapshot(root)
    entry_count = root.rebuild_availability()
    after = _availability_snapshot(root)
    drifted = sorted(
        name
        for name in set(before) | set(after)
        if before.get(name) != after.get(name)
    )
    return {
        "status": "proven" if not drifted else "failed",
        "entry_count": entry_count,
        "drifted_entries": drifted,
    }


def _stored_product_mention_policy(root: DataLakeRoot) -> dict[str, str]:
    manifest_path = root._within(
        "indexes",
        "derived_retrieval",
        "silver_vault",
        "core",
        "manifests",
        "by_mention.json",
    )
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        policy = manifest["selection_policy_versions"]["product_mention_policy"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise ValueError(
            f"stored by_mention manifest does not provide product-mention policy pins: {exc}"
        ) from exc
    return normalize_product_mention_policy(policy)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Rebuild or prove the rebuildability of the Data Lake index tiers "
            "(availability, derived_retrieval object-level views)."
        )
    )
    parser.add_argument(
        "--root",
        "--data-root",
        dest="data_root",
        help="Explicit Forseti data root path (falls back to FORSETI_DATA_ROOT (legacy ORCA_DATA_ROOT)).",
    )
    parser.add_argument(
        "--target",
        choices=("availability", "creator_vault", "derived_retrieval", "all"),
        default="all",
        help="Which generated family to rebuild or prove (default: all).",
    )
    parser.add_argument(
        "--prove-rebuildability",
        action="store_true",
        help=(
            "Verify instead of build: fail when any stored index entry cannot be "
            "regenerated byte-identically from committed material."
        ),
    )
    parser.add_argument(
        "--prove-incremental-equality",
        action="store_true",
        help=(
            "Generate derived_retrieval through incremental and full-cold paths "
            "and byte-compare every output file without writing views."
        ),
    )
    parser.add_argument(
        "--audit-source-integrity",
        action="store_true",
        help=(
            "Cold re-hash all derived_retrieval sources and byte-compare against "
            "stored views without rebuilding."
        ),
    )
    parser.add_argument(
        "--full-rebuild",
        action="store_true",
        help="Ignore the persisted classification cache for this rebuild.",
    )
    parser.add_argument(
        "--product-mention-policy-version",
        help="Exact transcript-product-mention policy version for a rebuild.",
    )
    parser.add_argument(
        "--product-mention-policy-fingerprint-sha256",
        help="Exact lowercase 64-hex transcript-product-mention policy fingerprint.",
    )
    parser.add_argument(
        "--use-stored-product-mention-policy",
        action="store_true",
        help=(
            "Read exact product-mention policy pins from the stored by_mention "
            "manifest (for cadence-tail and owner-scheduled rebuilds)."
        ),
    )
    args = parser.parse_args(argv)
    verification_modes = sum(
        bool(value)
        for value in (
            args.prove_rebuildability,
            args.prove_incremental_equality,
            args.audit_source_integrity,
        )
    )
    if verification_modes > 1:
        parser.error(
            "choose at most one of --prove-rebuildability, "
            "--prove-incremental-equality, and --audit-source-integrity"
        )
    if (args.prove_incremental_equality or args.audit_source_integrity) and (
        args.target != "derived_retrieval"
    ):
        parser.error(
            "--prove-incremental-equality and --audit-source-integrity require "
            "--target derived_retrieval"
        )
    if args.full_rebuild and verification_modes:
        parser.error("--full-rebuild applies only to rebuild mode")
    if args.use_stored_product_mention_policy and (
        args.product_mention_policy_version
        or args.product_mention_policy_fingerprint_sha256
    ):
        parser.error(
            "--use-stored-product-mention-policy cannot be combined with explicit "
            "product-mention policy pins"
        )
    needs_product_policy = (
        args.target in ("derived_retrieval", "all")
        and not args.prove_rebuildability
        and not args.audit_source_integrity
    )
    if needs_product_policy and (
        not args.use_stored_product_mention_policy
        and (
            not args.product_mention_policy_version
            or not args.product_mention_policy_fingerprint_sha256
        )
    ):
        parser.error(
            "derived_retrieval rebuild requires --product-mention-policy-version "
            "and --product-mention-policy-fingerprint-sha256"
        )
    explicit_product_mention_policy = (
        {
            "policy_version": args.product_mention_policy_version,
            "policy_fingerprint_sha256": args.product_mention_policy_fingerprint_sha256,
        }
        if needs_product_policy
        else None
    )

    report: dict = {
        "target": args.target,
        "prove": bool(verification_modes),
        "mode": (
            "prove_rebuildability"
            if args.prove_rebuildability
            else "prove_incremental_equality"
            if args.prove_incremental_equality
            else "audit_source_integrity"
            if args.audit_source_integrity
            else "full_rebuild"
            if args.full_rebuild
            else "incremental_rebuild"
        ),
    }
    try:
        root = DataLakeRoot.resolve(explicit=args.data_root)
        product_mention_policy = (
            _stored_product_mention_policy(root)
            if needs_product_policy and args.use_stored_product_mention_policy
            else explicit_product_mention_policy
        )
        statuses: list[str] = []
        if args.target in ("availability", "all"):
            availability = _rebuild_availability(root, prove=args.prove_rebuildability)
            report["availability"] = availability
            statuses.append(availability["status"])
        if args.target == "creator_vault":
            if args.prove_rebuildability:
                creator_vault = prove_creator_vault_rebuildability(root)
            else:
                creator_vault = rebuild_creator_vault(
                    root,
                    full_rebuild=args.full_rebuild,
                )
            report["creator_vault"] = creator_vault
            statuses.append(creator_vault["status"])
        if args.target in ("derived_retrieval", "all"):
            if args.prove_rebuildability:
                derived = prove_derived_retrieval_rebuildability(root)
            elif args.prove_incremental_equality:
                derived = prove_incremental_rebuild_equality(
                    root,
                    product_mention_policy=product_mention_policy,
                )
            elif args.audit_source_integrity:
                derived = audit_derived_retrieval_source_integrity(root)
            else:
                derived = rebuild_derived_retrieval(
                    root,
                    product_mention_policy=product_mention_policy,
                    full_rebuild=args.full_rebuild,
                )
            report["derived_retrieval"] = derived
            statuses.append(derived["status"])
    except (DataLakeRootError, ValueError) as exc:
        report["status"] = "error"
        report["error"] = str(exc)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 2

    report["status"] = "ok" if all(s in {"rebuilt", "proven"} for s in statuses) else "failed"
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
