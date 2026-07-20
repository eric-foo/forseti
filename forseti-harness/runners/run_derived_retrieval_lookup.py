"""Scoped, read-only lookup over the generated derived_retrieval views.

The agent-facing retrieval entry point: resolve a creator (per-platform
public account) or a brand/line product entity to its committed packet and
Silver-record refs, with the build-time authority classification the views
carry, in one call — instead of a whole-lake scan.

Reads ONLY the complete generation named by
``indexes/derived_retrieval/silver_vault/core/CURRENT`` (or the fixed-path
migration fallback before the first pointer publication). The views are
rebuildable, non-authoritative routing caches:
by-key discovery over ``derived/`` stays the retrieval authority, and every
result carries the generation provenance so a consumer can detect staleness
and rebuild (``run_data_lake_indexes_rebuild.py --target derived_retrieval``).
A key absent from a view means "not captured or not indexed" — never zero.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.derived_retrieval_views import load_derived_retrieval_view
from data_lake.root import DataLakeRoot, DataLakeRootError


def _normalized(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip().casefold())


def _provenance(
    manifest: dict | None, reader_provenance: dict[str, Any]
) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        return {"manifest": "absent", **reader_provenance}
    return {
        "generation_id": manifest.get("generation_id"),
        "generated_at": manifest.get("generated_at"),
        "freshness": manifest.get("freshness"),
        "stale_if": manifest.get("stale_if"),
        **reader_provenance,
    }


def lookup_creator(root: DataLakeRoot, query: str) -> dict[str, Any]:
    view, manifest, reader_provenance = load_derived_retrieval_view(
        root, "by_creator"
    )
    if view is None:
        return {
            "status": "view_not_built",
            "hint": "run runners/run_data_lake_indexes_rebuild.py --target derived_retrieval",
        }
    wanted = _normalized(query)
    namespace_filter = None
    if ":" in query:
        prefix, _, rest = query.partition(":")
        namespace_filter = _normalized(prefix)
        wanted = _normalized(rest)
    if not wanted:
        raise ValueError("creator query must contain a non-empty account id or alias")
    matches = []
    for namespace, kinds in view.get("creators", {}).items():
        if namespace_filter and _normalized(namespace) != namespace_filter:
            continue
        for identity_kind, ids in kinds.items():
            for native_id, entry in ids.items():
                candidates = {_normalized(native_id)} | {
                    _normalized(alias) for alias in entry.get("aliases", {}).values()
                }
                if wanted in candidates:
                    matches.append(
                        {
                            "namespace": namespace,
                            "identity_kind": identity_kind,
                            "native_id": native_id,
                            **entry,
                        }
                    )
    return {
        "status": "found" if matches else "not_found",
        "query": query,
        "matches": matches,
        "zero_rows_meaning": view.get("zero_rows_meaning"),
        "authority_note": view.get("semantics"),
        "view_provenance": _provenance(manifest, reader_provenance),
    }


def lookup_mention(root: DataLakeRoot, query: str) -> dict[str, Any]:
    view, manifest, reader_provenance = load_derived_retrieval_view(
        root, "by_mention"
    )
    if view is None:
        return {
            "status": "view_not_built",
            "hint": "run runners/run_data_lake_indexes_rebuild.py --target derived_retrieval",
        }
    wanted = _normalized(query)
    if not wanted:
        raise ValueError("mention query must contain a non-empty brand or line identity")
    matches: list[dict[str, Any]] = []
    for section in ("mentions", "native_product_pages"):
        for brand, lines in view.get(section, {}).items():
            for line, refs in lines.items():
                tokens = {
                    _normalized(brand),
                    _normalized(line),
                    _normalized(f"{brand} {line}"),
                }
                if wanted in tokens:
                    matches.append(
                        {"source_class": section, "brand": brand, "line": line, "refs": refs}
                    )
    return {
        "status": "found" if matches else "not_found",
        "query": query,
        "matches": matches,
        "zero_rows_meaning": view.get("zero_rows_meaning"),
        "authority_note": view.get("semantics"),
        "view_provenance": _provenance(manifest, reader_provenance),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        "--data-root",
        dest="data_root",
        help="Explicit Forseti data root path (falls back to FORSETI_DATA_ROOT).",
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument(
        "--creator",
        help="Creator query: bare handle/account id, or namespace:native_id.",
    )
    target.add_argument(
        "--mention",
        help="Brand/line product entity query (normalized exact brand, line, or combined identity).",
    )
    args = parser.parse_args(argv)
    try:
        root = DataLakeRoot.resolve_readonly(explicit=args.data_root)
        result = (
            lookup_creator(root, args.creator)
            if args.creator is not None
            else lookup_mention(root, args.mention)
        )
    except (DataLakeRootError, OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if result["status"] == "found":
        return 0
    if result["status"] == "not_found":
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
