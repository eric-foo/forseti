"""The contract-pinned lake indexes rebuild command (runner packaging).

Shape pinned by the derived-layout contract:
``lake indexes rebuild --root <FORSETI_DATA_ROOT> --target
availability|derived_retrieval|all --prove-rebuildability`` — the semantics
are the contract; the argparse runner is the incumbent CLI packaging
(consumption seam contract, Rebuild Command Binding).

Modes:

- **rebuild** (default): regenerate the requested index tier(s) from committed
  material. ``availability`` delegates to ``DataLakeRoot.rebuild_availability``;
  ``derived_retrieval`` reuses unchanged inventoried source bytes, writes a
  complete immutable generation, then atomically publishes ``CURRENT``. An
  unchanged refresh exits successfully as ``current`` without publishing.
- **--prove-rebuildability**: verification. ``derived_retrieval`` is proven
  read-only — every stored view is regenerated under the stamps its stored
  manifest recorded and byte-compared (a rebuild is never compared against
  itself). ``availability`` is proven by before/after byte comparison around
  an in-place rebuild (mutation-to-truth): any drift means the stored index
  was smuggling non-regenerable or stale state and is reported as a failure.
- **--prove-incremental-equality**: read-only Stage 1 gate. Generate the lake
  map once through the disposable source inventory/classification cache and
  once through a full cold sweep under one stamp, then byte-compare every view
  and manifest.
- **--audit-source-integrity**: read-only cold source re-hash and byte proof,
  intended for the owner-operated periodic integrity schedule.

Fresh-root one-time bootstrap (binds and reports this checkout's exact active
policy, and refuses an existing ``by_mention`` manifest):

``python runners/run_data_lake_indexes_rebuild.py --root F:\\forseti-data-lake --target derived_retrieval --bootstrap-active-product-mention-policy``

Owner-operated one-shot daily fallback (policy pins are read from the stored
generated-view manifest, never hardcoded):

``python runners/run_data_lake_indexes_rebuild.py --root F:\\forseti-data-lake --target derived_retrieval --use-stored-product-mention-policy``

Periodic integrity command (scheduling remains owner-operated):

``python runners/run_data_lake_indexes_rebuild.py --root F:\\forseti-data-lake --target derived_retrieval --audit-source-integrity``
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cleaning.transcript_product_extractor import EXTRACTOR_RUBRIC_VERSION
from cleaning.transcript_product_lake import product_mentions_policy_fingerprint
from data_lake.derived_retrieval_views import (
    audit_derived_retrieval_source_integrity,
    current_generation_root,
    normalize_decision_question_id,
    prove_incremental_rebuild_equality,
    prove_derived_retrieval_rebuildability,
    prove_sql_catalogue_rebuildability,
    query_exact_actor_context,
    query_sql_catalogue,
    rebuild_derived_retrieval,
    sql_catalogue_status,
    verify_sql_query_sources,
    write_actor_query_audit,
    write_evidence_query_audit,
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


def _by_mention_manifest_path(root: DataLakeRoot) -> Path:
    generation_root, _generation_id, _layout = current_generation_root(root)
    return generation_root / "manifests" / "by_mention.json"


def _stored_product_mention_policy(root: DataLakeRoot) -> dict[str, str]:
    try:
        manifest = json.loads(
            _by_mention_manifest_path(root).read_text(encoding="utf-8")
        )
        policy = manifest["selection_policy_versions"]["product_mention_policy"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise ValueError(
            f"stored by_mention manifest does not provide product-mention policy pins: {exc}"
        ) from exc
    return normalize_product_mention_policy(policy)


def _active_product_mention_policy_for_bootstrap(
    root: DataLakeRoot,
) -> dict[str, str]:
    manifest_path = _by_mention_manifest_path(root)
    if manifest_path.exists():
        raise ValueError(
            "active product-mention policy bootstrap is fresh-root only; "
            "by_mention manifest already exists, so use stored policy pins"
        )
    return normalize_product_mention_policy(
        {
            "policy_version": EXTRACTOR_RUBRIC_VERSION,
            "policy_fingerprint_sha256": product_mentions_policy_fingerprint(
                EXTRACTOR_RUBRIC_VERSION
            ),
        }
    )


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
        choices=("availability", "derived_retrieval", "all"),
        default="all",
        help="Which index tier to rebuild or prove (default: all).",
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
        help=(
            "Recreate the disposable source inventory and ignore the persisted "
            "classification cache for this rebuild."
        ),
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
    parser.add_argument(
        "--bootstrap-active-product-mention-policy",
        action="store_true",
        help=(
            "One-time fresh-root rebuild: bind the exact active product-mention "
            "policy from this checkout and refuse an existing by_mention manifest."
        ),
    )

    parser.add_argument("--sql-status", action="store_true", help="Report SQL catalogue health and freshness.")
    parser.add_argument("--sql-query", action="store_true", help="Run a bounded evidence search.")
    parser.add_argument("--sql-exact-actor", help="Hydrate one exact public actor identifier for one bounded query.")
    parser.add_argument("--sql-body-query")
    parser.add_argument("--sql-platform")
    parser.add_argument("--sql-vendor")
    parser.add_argument("--sql-surface")
    parser.add_argument("--sql-creator-id")
    parser.add_argument("--sql-content-id")
    parser.add_argument("--sql-product-id")
    parser.add_argument("--sql-from-utc")
    parser.add_argument("--sql-to-utc")
    parser.add_argument("--sql-limit", type=int, default=1000)
    parser.add_argument("--decision-question-id")
    args = parser.parse_args(argv)

    sql_modes = sum(bool(value) for value in (args.sql_status,args.sql_query,args.sql_exact_actor))
    if sql_modes > 1:
        parser.error("choose only one SQL status/query mode")
    # Absence routes to exploratory; anything SUPPLIED -- including "" -- is a
    # decision request and is validated before the query runs.
    if args.decision_question_id is not None and not (
            args.sql_query or args.sql_exact_actor):
        parser.error("--decision-question-id requires --sql-query or --sql-exact-actor")
    if sql_modes:
        try:
            decision_question_id = (
                normalize_decision_question_id(args.decision_question_id)
                if args.decision_question_id is not None else None)
            root = DataLakeRoot.resolve(explicit=args.data_root)
            if args.sql_status:
                report = sql_catalogue_status(root)
            elif args.sql_query:
                report = query_sql_catalogue(
                    root,body_query=args.sql_body_query,platform=args.sql_platform,
                    vendor=args.sql_vendor,surface=args.sql_surface,
                    creator_id=args.sql_creator_id,
                    content_id=args.sql_content_id,product_id=args.sql_product_id,
                    from_utc=args.sql_from_utc,to_utc=args.sql_to_utc,limit=args.sql_limit)
                if decision_question_id is not None:
                    if not report["result_set_complete"]:
                        raise ValueError(
                            "decision query result set is truncated; narrow the query")
                    report["source_verification"] = verify_sql_query_sources(root,report)
                    report["audit_path"] = write_evidence_query_audit(
                        report,decision_question_id=decision_question_id)
            else:
                if not (args.sql_platform and args.sql_from_utc and args.sql_to_utc
                        and decision_question_id is not None):
                    parser.error("--sql-exact-actor requires platform, from/to UTC, and decision-question-id")
                report = query_exact_actor_context(
                    root,platform=args.sql_platform,actor=args.sql_exact_actor,
                    from_utc=args.sql_from_utc,to_utc=args.sql_to_utc,
                    creator_id=args.sql_creator_id,content_id=args.sql_content_id)
                report["audit_path"] = write_actor_query_audit(
                    report,decision_question_id=decision_question_id)
        except (OSError,DataLakeRootError,ValueError,sqlite3.DatabaseError) as exc:
            print(json.dumps({"status":"error","error":str(exc)},indent=2,sort_keys=True))
            return 2
        print(json.dumps(report,indent=2,sort_keys=True,ensure_ascii=True))
        return 0
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
    explicit_product_policy_requested = bool(
        args.product_mention_policy_version
        or args.product_mention_policy_fingerprint_sha256
    )
    product_policy_sources = sum(
        (
            bool(args.use_stored_product_mention_policy),
            bool(args.bootstrap_active_product_mention_policy),
            explicit_product_policy_requested,
        )
    )
    if product_policy_sources > 1:
        parser.error(
            "choose exactly one product-mention policy source: stored manifest, "
            "fresh-root active-policy bootstrap, or explicit pins"
        )
    if args.bootstrap_active_product_mention_policy and (
        verification_modes or args.target not in ("derived_retrieval", "all")
    ):
        parser.error(
            "--bootstrap-active-product-mention-policy applies only to a "
            "derived_retrieval or all rebuild"
        )
    needs_product_policy = (
        args.target in ("derived_retrieval", "all")
        and not args.prove_rebuildability
        and not args.audit_source_integrity
    )
    if needs_product_policy and (
        not args.use_stored_product_mention_policy
        and not args.bootstrap_active_product_mention_policy
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
        if needs_product_policy and explicit_product_policy_requested
        else None
    )
    product_mention_policy_source = (
        "stored_manifest"
        if args.use_stored_product_mention_policy
        else "active_checkout_bootstrap"
        if args.bootstrap_active_product_mention_policy
        else "explicit_pins"
        if explicit_product_policy_requested
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
            else _active_product_mention_policy_for_bootstrap(root)
            if needs_product_policy and args.bootstrap_active_product_mention_policy
            else explicit_product_mention_policy
        )
        if needs_product_policy:
            report["product_mention_policy_source"] = product_mention_policy_source
            report["product_mention_policy"] = product_mention_policy
        statuses: list[str] = []
        if args.target in ("availability", "all"):
            availability = _rebuild_availability(root, prove=args.prove_rebuildability)
            report["availability"] = availability
            statuses.append(availability["status"])
        if args.target in ("derived_retrieval", "all"):
            if args.prove_rebuildability:
                derived = prove_derived_retrieval_rebuildability(root)
                sql_proof = prove_sql_catalogue_rebuildability(root)
                derived["sql_catalogue"] = sql_proof
                if sql_proof["status"] != "proven":
                    derived["status"] = "failed"
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

    report["status"] = (
        "ok"
        if all(s in {"current", "rebuilt", "proven"} for s in statuses)
        else "failed"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
