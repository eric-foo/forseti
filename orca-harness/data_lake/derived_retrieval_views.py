"""Gate-opened ``indexes/derived_retrieval`` object-level view builder.

Builds the two currently-buildable views the 2026-06-25 gate opening named
(``undone``, ``by_mention``; ``by_creator`` stays deferred behind the
audience-silver lake wiring), as rebuildable JSON caches under
``indexes/derived_retrieval/object_level/<view>/`` with a per-view manifest
carrying the Silver Vault read-model obligations. Contract:
``core_spine_v0_data_lake_consumption_seam_contract_v0.md`` (Rebuild Command
Binding section); command shape pinned by the derived-layout contract.

Invariants enforced here:

- Views are regenerated ONLY from committed availability + ``derived/`` +
  ``acknowledgements/`` records — never from another index, so
  prove-rebuildability is meaningful.
- Views are caches: nothing in the seam helper (``data_lake.consumption``)
  reads them, and the ``undone`` view's weaker no-ack semantics are stated in
  the view body itself.
- ``by_mention`` admits only records passing the read-side Silver lineage
  gate; everything else is a named residual, never evidence. Exact
  ``(brand, line)`` strings are preserved — grouping normalization is
  Cleaning's job, never the lake's.
- Generation stamps are injectable so a rebuild under recorded stamps is
  byte-deterministic (``--prove-rebuildability`` regenerates under the stored
  manifest's stamps and byte-compares; it never compares a rebuild against
  itself).

Writes follow the incumbent generated-index pattern (``data_lake.catalog``):
``root._reverify()`` + ``root._within(...)`` + wipe-and-rewrite of the
rebuildable tier. No behavior is added to ``DataLakeRoot``.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from data_lake.canonical_json import canonical_record_bytes
from data_lake.consumption import iter_all_acks
from data_lake.lane_registry import LANE_ROLES
from data_lake.silver_lineage import (
    SOURCE_BACKED_COMPLETE_STATUS,
    silver_record_source_backed_status,
)

VIEW_SCHEMA_VERSION = 1
MANIFEST_SCHEMA_VERSION = 1
OBJECT_LEVEL_PARTS = ("indexes", "derived_retrieval", "object_level")
BUILT_VIEWS = ("by_mention", "undone")

# The mentions lane the by_mention view indexes. String mirrored from the
# CI-guarded lane registry (asserted below) rather than imported from
# cleaning/, which would invert the base-layer boundary.
MENTIONS_LANE = "silver__cleaning__product_mentions"
assert MENTIONS_LANE in LANE_ROLES, "by_mention source lane must stay registered"

_UNDONE_SEMANTICS = (
    "per adopted ack namespace (>=1 ack record), the committed anchors having zero "
    "ack records; lane-side obligation growth is NOT reflected; rebuildable cache "
    "for inspection only, never pickup authority"
)


def generation_stamp() -> dict[str, str]:
    """A fresh build stamp. Injectable into the builders so verification can
    regenerate under a RECORDED stamp deterministically."""
    return {
        "generation_id": uuid.uuid4().hex,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def build_undone_view(root) -> tuple[dict, list[str]]:
    """The undone view body plus the source refs its manifest must cite."""
    committed = sorted(root.list_available())
    acked_by_namespace: dict[str, set[str]] = {}
    ack_refs: list[str] = []
    for raw_anchor, namespace, ack in iter_all_acks(root):
        acked_by_namespace.setdefault(namespace, set()).add(raw_anchor)
        ack_refs.append(f"{raw_anchor}/{namespace}/{ack.get('obligation_fingerprint', '')}")
    view = {
        "view": "undone",
        "view_schema_version": VIEW_SCHEMA_VERSION,
        "semantics": _UNDONE_SEMANTICS,
        "zero_rows_meaning": (
            "zero ack records for the namespace — NOT current-obligation satisfied; "
            "stale-ack/grown-obligation backlog is visible only to lane-side pickup"
        ),
        "adopted_namespaces": sorted(acked_by_namespace),
        "anchors_with_acks": {
            namespace: len(anchors)
            for namespace, anchors in sorted(acked_by_namespace.items())
        },
        "undone": {
            namespace: sorted(set(committed) - anchors)
            for namespace, anchors in sorted(acked_by_namespace.items())
        },
    }
    source_refs = sorted(f"availability/{packet_id}" for packet_id in committed) + sorted(ack_refs)
    return view, source_refs


def build_by_mention_view(root) -> tuple[dict, list[str]]:
    """The by_mention view body plus the source refs its manifest must cite."""
    mentions: dict[str, dict[str, list[dict]]] = {}
    residuals: list[dict] = []
    source_refs: list[str] = []
    for raw_anchor in sorted(root.list_available()):
        lane_dir = root.lane_dir(subtree="derived", raw_anchor=raw_anchor, lane=MENTIONS_LANE)
        if not lane_dir.is_dir():
            continue
        for record_file in sorted(p for p in lane_dir.iterdir() if p.is_file()):
            body = record_file.read_bytes()
            source_refs.append(f"{raw_anchor}/{MENTIONS_LANE}/{record_file.name}")
            try:
                record = json.loads(body.decode("utf-8"))
            except ValueError:
                record = None
            if not isinstance(record, dict):
                residuals.append(
                    {"raw_anchor": raw_anchor, "record_id": record_file.name, "status": "unreadable"}
                )
                continue
            status = silver_record_source_backed_status(record)
            if status != SOURCE_BACKED_COMPLETE_STATUS:
                # Read-side Silver lineage gate: named residual, never evidence.
                residuals.append(
                    {"raw_anchor": raw_anchor, "record_id": record_file.name, "status": status}
                )
                continue
            sha256 = hashlib.sha256(body).hexdigest()
            ref = {
                "raw_anchor": raw_anchor,
                "lane": MENTIONS_LANE,
                "record_id": record_file.name,
                "sha256": sha256,
            }
            for mention in record.get("mentions") or []:
                if not isinstance(mention, dict):
                    continue
                brand = str(mention.get("brand") or "unknown")
                line = str(mention.get("line") or "")
                refs = mentions.setdefault(brand, {}).setdefault(line, [])
                if ref not in refs:
                    refs.append(ref)
    view = {
        "view": "by_mention",
        "view_schema_version": VIEW_SCHEMA_VERSION,
        "semantics": (
            "exact (brand, line) strings from source-backed-complete "
            f"{MENTIONS_LANE} records -> committed record refs; residuals are "
            "records failing the read-side Silver lineage gate and are not evidence"
        ),
        "mentions": {
            brand: {line: refs for line, refs in sorted(lines.items())}
            for brand, lines in sorted(mentions.items())
        },
        "residuals": sorted(
            residuals, key=lambda r: (r["raw_anchor"], r["record_id"])
        ),
        "residual_count": len(residuals),
    }
    return view, sorted(source_refs)


_BUILDERS = {
    "by_mention": build_by_mention_view,
    "undone": build_undone_view,
}


def _manifest(view_name: str, view_bytes: bytes, source_refs: list[str], stamp: dict) -> dict:
    return {
        "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
        "view": view_name,
        "view_schema_version": VIEW_SCHEMA_VERSION,
        "generation_id": stamp["generation_id"],
        "generated_at": stamp["generated_at"],
        "source_record_ids": source_refs,
        "source_high_watermark": hashlib.sha256(
            canonical_record_bytes(source_refs)
        ).hexdigest(),
        "selection_policy_versions": {
            "view_schema": VIEW_SCHEMA_VERSION,
            "silver_lineage_gate": SOURCE_BACKED_COMPLETE_STATUS,
        },
        "view_sha256": hashlib.sha256(view_bytes).hexdigest(),
        "stale_if": (
            "any committed availability/derived/acknowledgement change after "
            "source_high_watermark; verify with --prove-rebuildability"
        ),
    }


def _generate(root, stamp: dict) -> dict[str, bytes]:
    """All object-level view files as relpath -> bytes, regenerated purely from
    committed material under the given stamp."""
    files: dict[str, bytes] = {}
    for view_name in BUILT_VIEWS:
        view, source_refs = _BUILDERS[view_name](root)
        view_bytes = canonical_record_bytes(view)
        manifest_bytes = canonical_record_bytes(
            _manifest(view_name, view_bytes, source_refs, stamp)
        )
        files[f"{view_name}/view.json"] = view_bytes
        files[f"{view_name}/manifest.json"] = manifest_bytes
    return files


def _object_level_root(root) -> Path:
    return root._within(*OBJECT_LEVEL_PARTS)


def rebuild_derived_retrieval(root, *, stamp: dict | None = None) -> dict:
    """Wipe and rewrite the object-level views (rebuildable tier, catalog pattern)."""
    root._reverify()
    stamp = stamp or generation_stamp()
    files = _generate(root, stamp)
    target_root = _object_level_root(root)
    if target_root.exists():
        shutil.rmtree(target_root)
    for relpath, data in files.items():
        target = target_root / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return {
        "status": "rebuilt",
        "views": list(BUILT_VIEWS),
        "deferred_views": ["by_creator"],
        "generation_id": stamp["generation_id"],
        "file_count": len(files),
    }


def prove_derived_retrieval_rebuildability(root) -> dict:
    """Read-only verification: regenerate every stored view under the stamps its
    stored manifest recorded and byte-compare. Never compares a rebuild against
    itself; never writes."""
    root._reverify()
    target_root = _object_level_root(root)
    results: dict[str, str] = {}
    failures: list[str] = []
    for view_name in BUILT_VIEWS:
        view_path = target_root / view_name / "view.json"
        manifest_path = target_root / view_name / "manifest.json"
        if not view_path.is_file() and not manifest_path.is_file():
            results[view_name] = "absent_nothing_to_prove"
            continue
        if not view_path.is_file() or not manifest_path.is_file():
            results[view_name] = "failed_partial_files"
            failures.append(view_name)
            continue
        try:
            stored_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            stamp = {
                "generation_id": stored_manifest["generation_id"],
                "generated_at": stored_manifest["generated_at"],
            }
        except (ValueError, KeyError):
            results[view_name] = "failed_unreadable_manifest"
            failures.append(view_name)
            continue
        regenerated = _generate(root, stamp)
        if (
            regenerated[f"{view_name}/view.json"] == view_path.read_bytes()
            and regenerated[f"{view_name}/manifest.json"] == manifest_path.read_bytes()
        ):
            results[view_name] = "rebuildable"
        else:
            results[view_name] = "failed_drift_or_non_regenerable"
            failures.append(view_name)
    return {
        "status": "proven" if not failures else "failed",
        "results": results,
        "failures": failures,
    }


__all__ = [
    "BUILT_VIEWS",
    "MANIFEST_SCHEMA_VERSION",
    "MENTIONS_LANE",
    "OBJECT_LEVEL_PARTS",
    "VIEW_SCHEMA_VERSION",
    "build_by_mention_view",
    "build_undone_view",
    "generation_stamp",
    "prove_derived_retrieval_rebuildability",
    "rebuild_derived_retrieval",
]
