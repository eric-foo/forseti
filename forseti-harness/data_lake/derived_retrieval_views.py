"""Gate-opened Silver Vault generated-read-model builder.

Builds the three object-level views the 2026-06-25 gate opening named
(``by_creator``, ``by_mention``, ``undone``) as rebuildable JSON query tables
under the Silver Vault contract-owned
``indexes/derived_retrieval/silver_vault/core/`` home, with paired manifest
rows carrying the read-model obligations. Contract:
``core_spine_v0_data_lake_consumption_seam_contract_v0.md`` (Rebuild Command
Binding section); command shape pinned by the derived-layout contract.
``by_creator`` was deferred at gate opening behind the audience-silver lake
wiring; that wiring has since landed (registered creator-metric, grid, and
comment-attention Silver lanes, census-reconciled), so the view is built.
``by_mention`` was owner-widened 2026-07-17 to also carry native
product-page identity (a brand/line entity routes to its own product-page
capture, not only to creator-content mentions).

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
  Cleaning's job, never the lake's. Native product-page identity rows are
  labeled routing (from the view-only mechanical projection), never Silver
  authority.
- ``by_creator`` entries carry the authority status of every routed Silver
  record, computed at build time by the shared
  ``classify_silver_vault_record_sources`` classifier (the census's
  classifier) — never inferred from file presence. Per-platform object-level
  only: no cross-platform identity is unified.
- A key, packet, lane, or metric ABSENT from a view means "not captured or
  not indexed"; it must never be read as an observed zero.
- Generation stamps are injectable so a rebuild under recorded stamps is
  byte-deterministic (``--prove-rebuildability`` regenerates under the stored
  manifest's stamps and byte-compares; it never compares a rebuild against
  itself).

Writes follow the incumbent generated-index pattern (``data_lake.catalog``):
``root._reverify()`` + ``root._within(...)`` + replacement of only the
owned generated views. No behavior is added to ``DataLakeRoot``.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from data_lake.canonical_json import canonical_record_bytes
from data_lake.consumption import iter_all_acks
from data_lake.creator_metric_lineage import build_creator_metric_lineage_index
from data_lake.lane_registry import LANE_ROLES, LaneRole
from data_lake.product_mention_selection import (
    MENTIONS_LANE,
    normalize_product_mention_policy,
    select_product_mention_records,
)
from data_lake.silver_record import (
    PHYSICALLY_SOURCE_BACKED_COMPLETE_STATUS,
    SILVER_VAULT_RECORD_SCHEMA_VERSION,
    classify_silver_vault_record_sources,
)

UNDONE_VIEW_SCHEMA_VERSION = 1
BY_MENTION_VIEW_SCHEMA_VERSION = 3
BY_CREATOR_VIEW_SCHEMA_VERSION = 1
VIEW_SCHEMA_VERSION = BY_MENTION_VIEW_SCHEMA_VERSION
MANIFEST_SCHEMA_VERSION = 1
SILVER_VAULT_CORE_PARTS = ("indexes", "derived_retrieval", "silver_vault", "core")
BUILT_VIEWS = ("by_creator", "by_mention", "undone")

FRAGRANTICA_PROJECTION_LANE = "projection_fragrantica"
FRAGRANTICA_PRODUCT_ROW_KIND = "fragrance_product_snapshot"
_MISSING_EVIDENCE_NOTE = (
    "a key, packet, lane, or metric absent from this view means not captured or "
    "not indexed at build time; it must never be read as an observed zero"
)

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
        "view_schema_version": UNDONE_VIEW_SCHEMA_VERSION,
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


_ACTIVE_SILVER_ENVELOPE_LANES = tuple(
    sorted(
        lane for lane, role in LANE_ROLES.items() if role is LaneRole.SILVER_ENVELOPE
    )
)


def _classified_silver_sweep(root) -> dict[str, Any]:
    """One deterministic classification sweep over every registered active
    ``silver_envelope`` lane: per-anchor/lane/status counts, account-bearing
    subject refs, source refs, and named residuals. Shared by ``by_creator``
    and the ``by_mention`` native-product-page section so one build classifies
    each record exactly once."""
    anchor_lane_status: dict[str, dict[str, Counter]] = defaultdict(
        lambda: defaultdict(Counter)
    )
    accounts: dict[tuple[str, str], dict[str, Any]] = {}
    source_refs: list[str] = []
    residuals: list[dict[str, Any]] = []
    derived = root.path / "derived"
    lineage = build_creator_metric_lineage_index(root)
    for lane in _ACTIVE_SILVER_ENVELOPE_LANES:
        for path in sorted(derived.glob(f"*/*/{lane}/*")):
            if not path.is_file():
                continue
            anchor = path.parents[1].name
            ref_key = f"{anchor}/{lane}/{path.name}"
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                residuals.append(
                    {"status": "unreadable", "raw_anchor": anchor, "lane": lane, "record_id": path.name}
                )
                continue
            if (
                not isinstance(record, dict)
                or record.get("schema_version") != SILVER_VAULT_RECORD_SCHEMA_VERSION
            ):
                residuals.append(
                    {
                        "status": "non_envelope_schema_audit_only",
                        "raw_anchor": anchor,
                        "lane": lane,
                        "record_id": path.name,
                    }
                )
                continue
            source_refs.append(ref_key)
            authority = classify_silver_vault_record_sources(
                root, record, record_path=path, creator_metric_lineage=lineage
            )
            anchor_lane_status[anchor][lane][authority.status] += 1
            ref = {
                "raw_anchor": anchor,
                "lane": lane,
                "record_id": record.get("record_id"),
                "content_hash": record.get("content_hash"),
                "payload_kind": record.get("payload_kind"),
                "observed_at": record.get("observed_at"),
                "authority_status": authority.status,
                "reason_code": authority.reason_code,
            }
            for namespace, native_id, aliases in _account_subject_keys(record):
                entry = accounts.setdefault(
                    (namespace, native_id), {"aliases": {}, "refs_by_anchor": defaultdict(list)}
                )
                for alias_key, alias_value in aliases.items():
                    entry["aliases"].setdefault(alias_key, alias_value)
                entry["refs_by_anchor"][anchor].append(ref)
    return {
        "anchor_lane_status": anchor_lane_status,
        "accounts": accounts,
        "source_refs": sorted(source_refs),
        "residuals": sorted(residuals, key=lambda row: json.dumps(row, sort_keys=True)),
    }


def _account_subject_keys(record: dict) -> list[tuple[str, str, dict[str, Any]]]:
    """Per-platform public-account keys a record's subject asserts: a
    ``platform_public_account`` subject directly, or a ``public_content_object``
    subject that names its publishing account. Exact strings preserved."""
    payload = record.get("payload")
    observation = payload.get("observation") if isinstance(payload, dict) else None
    subject = observation.get("subject") if isinstance(observation, dict) else None
    if not isinstance(subject, dict) or subject.get("ref_type") != "entity_key":
        return []
    ref = subject.get("ref")
    if not isinstance(ref, dict):
        return []
    namespace = str(ref.get("namespace") or "").strip()
    if not namespace:
        return []
    keys: list[tuple[str, str, dict[str, Any]]] = []
    if ref.get("kind") == "platform_public_account":
        native_id = str(ref.get("native_id") or "").strip()
        if native_id:
            aliases = {
                field: ref[field]
                for field in ("orca_platform_account_id", "native_id_kind")
                if ref.get(field)
            }
            keys.append((namespace, native_id, aliases))
    elif ref.get("kind") == "public_content_object":
        publisher = str(ref.get("published_by_account_native_id") or "").strip()
        if publisher:
            aliases = {
                alias_key: ref[source_field]
                for source_field, alias_key in (
                    ("orca_platform_account_id", "orca_platform_account_id"),
                    ("published_by_account_native_id_kind", "native_id_kind"),
                )
                if ref.get(source_field)
            }
            keys.append((namespace, publisher, aliases))
    return keys


def build_by_creator_view(root, *, sweep: dict | None = None) -> tuple[dict, list[str]]:
    """The per-platform by_creator view plus the source refs its manifest cites.

    (platform namespace, observed public account id) -> committed packet +
    Silver-record refs with build-time authority classification. Object-level
    only; no cross-platform identity is unified.
    """
    sweep = sweep or _classified_silver_sweep(root)
    creators: dict[str, dict[str, Any]] = {}
    for (namespace, native_id), entry in sorted(sweep["accounts"].items()):
        packets = {}
        totals: Counter = Counter()
        for anchor in sorted(entry["refs_by_anchor"]):
            lane_status = {
                lane: dict(sorted(statuses.items()))
                for lane, statuses in sorted(sweep["anchor_lane_status"][anchor].items())
            }
            for statuses in lane_status.values():
                totals.update(statuses)
            packets[anchor] = {
                "subject_evidence": sorted(
                    entry["refs_by_anchor"][anchor],
                    key=lambda ref: (ref["lane"], str(ref["record_id"])),
                ),
                "anchor_silver_records_by_lane_status": lane_status,
            }
        creators.setdefault(namespace, {})[native_id] = {
            "aliases": dict(sorted(entry["aliases"].items())),
            "packets": packets,
            "anchor_level_totals_by_status": dict(sorted(totals.items())),
        }
    view = {
        "view": "by_creator",
        "view_schema_version": BY_CREATOR_VIEW_SCHEMA_VERSION,
        "semantics": (
            "(platform namespace, observed public account native id) -> committed "
            "packet + Silver record refs; authority statuses computed at build time "
            "by data_lake.silver_record.classify_silver_vault_record_sources; "
            "per-platform object-level only, no cross-platform identity; exact "
            "observed strings preserved (normalization is the reader's concern)"
        ),
        "zero_rows_meaning": _MISSING_EVIDENCE_NOTE,
        "creators": creators,
        "creator_count": sum(len(ids) for ids in creators.values()),
        "residuals": sweep["residuals"],
        "residual_count": len(sweep["residuals"]),
    }
    return view, list(sweep["source_refs"])


def _native_product_pages(root, sweep: dict) -> tuple[dict, list[str]]:
    """Native product-page identity rows from committed Fragrantica projections
    (view-only mechanical records used as identity ROUTING, never authority),
    each joined to its anchor's classified Silver record counts."""
    pages: dict[str, dict[str, list[dict]]] = {}
    source_refs: list[str] = []
    derived = root.path / "derived"
    for path in sorted(derived.glob(f"*/*/{FRAGRANTICA_PROJECTION_LANE}/*")):
        if not path.is_file():
            continue
        try:
            projection = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        rows = projection.get("rows") if isinstance(projection, dict) else None
        if not isinstance(rows, list):
            continue
        anchor = path.parents[1].name
        for row in rows:
            if not isinstance(row, dict) or row.get("row_kind") != FRAGRANTICA_PRODUCT_ROW_KIND:
                continue
            brand = str(row.get("brand_or_house") or "unknown")
            line = str(row.get("source_object_name") or "")
            if not line:
                continue
            visible = row.get("source_visible_fields")
            entry = {
                "source_site": str(row.get("source_platform") or "fragrantica"),
                "site_native_id": row.get("source_object_site_id"),
                "canonical_url": (
                    visible.get("canonical_url") if isinstance(visible, dict) else None
                ),
                "raw_anchor": anchor,
                "identity_source": (
                    f"{FRAGRANTICA_PROJECTION_LANE} {FRAGRANTICA_PRODUCT_ROW_KIND} row "
                    "(view-only mechanical projection; identity routing, not Silver authority)"
                ),
                "anchor_silver_records_by_lane_status": {
                    lane: dict(sorted(statuses.items()))
                    for lane, statuses in sorted(sweep["anchor_lane_status"][anchor].items())
                },
            }
            entries = pages.setdefault(brand, {}).setdefault(line, [])
            # An anchor may hold several projection records carrying the same
            # snapshot row; one identity entry per (anchor, site id) is enough.
            if entry not in entries:
                entries.append(entry)
            source_refs.append(f"{anchor}/{FRAGRANTICA_PROJECTION_LANE}/{path.name}")
    normalized = {
        brand: {line: sorted(entries, key=lambda e: str(e["raw_anchor"])) for line, entries in sorted(lines.items())}
        for brand, lines in sorted(pages.items())
    }
    return normalized, sorted(set(source_refs))


def build_by_mention_view(
    root,
    *,
    product_mention_policy: dict[str, str],
    sweep: dict | None = None,
) -> tuple[dict, list[str]]:
    """The exact-policy by_mention view plus every non-evidence residual."""
    selection = select_product_mention_records(root, policy=product_mention_policy)
    mentions: dict[str, dict[str, list[dict]]] = {}
    for selected in selection.selected:
        ref = {
            "raw_anchor": selected.raw_anchor,
            "lane": MENTIONS_LANE,
            "record_id": selected.record_id,
            "sha256": selected.sha256,
        }
        payload = selected.record.get("payload")
        observation = payload.get("observation") if isinstance(payload, dict) else None
        rows = observation.get("rows") if isinstance(observation, dict) else []
        for row in rows or []:
            mention = row.get("mention") if isinstance(row, dict) else None
            if not isinstance(mention, dict):
                continue
            brand = str(mention.get("brand") or "unknown")
            line = str(mention.get("line") or "")
            refs = mentions.setdefault(brand, {}).setdefault(line, [])
            if ref not in refs:
                refs.append(ref)
    native_pages, native_refs = _native_product_pages(
        root, sweep or _classified_silver_sweep(root)
    )
    view = {
        "view": "by_mention",
        "view_schema_version": BY_MENTION_VIEW_SCHEMA_VERSION,
        "selection_policy": selection.policy,
        "semantics": (
            "exact (brand, line) strings from exact-policy, source-backed-complete "
            f"{MENTIONS_LANE} records -> committed record refs; native_product_pages "
            "additionally routes a brand/line entity to its own committed product-page "
            "capture anchor with classified Silver record counts (identity from the "
            "view-only projection, owner-widened 2026-07-17); residuals are non-evidence"
        ),
        "zero_rows_meaning": _MISSING_EVIDENCE_NOTE,
        "mentions": {
            brand: {line: refs for line, refs in sorted(lines.items())}
            for brand, lines in sorted(mentions.items())
        },
        "native_product_pages": native_pages,
        "selected_record_count": len(selection.selected),
        "residuals": list(selection.residuals),
        "residual_count": len(selection.residuals),
    }
    return view, sorted(set(selection.source_refs) | set(native_refs))


_VIEW_SCHEMA_VERSIONS = {
    "by_creator": BY_CREATOR_VIEW_SCHEMA_VERSION,
    "by_mention": BY_MENTION_VIEW_SCHEMA_VERSION,
    "undone": UNDONE_VIEW_SCHEMA_VERSION,
}


def _manifest(
    view_name: str,
    view_bytes: bytes,
    source_refs: list[str],
    stamp: dict,
    product_mention_policy: dict[str, str] | None,
) -> dict:
    selection_policy_versions: dict[str, Any] = {
        "view_schema": _VIEW_SCHEMA_VERSIONS[view_name],
    }
    if view_name == "by_mention":
        selection_policy_versions.update(
            {
                "silver_lineage_gate": PHYSICALLY_SOURCE_BACKED_COMPLETE_STATUS,
                "product_mention_policy": product_mention_policy,
                "native_product_page_identity": (
                    f"{FRAGRANTICA_PROJECTION_LANE}/{FRAGRANTICA_PRODUCT_ROW_KIND}"
                ),
            }
        )
    if view_name == "by_creator":
        selection_policy_versions["silver_authority_classifier"] = (
            "data_lake.silver_record.classify_silver_vault_record_sources"
        )
    return {
        "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
        "view": view_name,
        "view_schema_version": _VIEW_SCHEMA_VERSIONS[view_name],
        "generation_id": stamp["generation_id"],
        "generated_at": stamp["generated_at"],
        "source_record_ids": source_refs,
        "source_high_watermark": hashlib.sha256(
            canonical_record_bytes(source_refs)
        ).hexdigest(),
        "selection_policy_versions": selection_policy_versions,
        "view_sha256": hashlib.sha256(view_bytes).hexdigest(),
        "stale_if": (
            "any committed availability/derived/acknowledgement change after "
            "source_high_watermark; verify with --prove-rebuildability"
        ),
    }


def _generate(
    root,
    stamp: dict,
    *,
    product_mention_policy: dict[str, str] | None,
    views: tuple[str, ...] = BUILT_VIEWS,
) -> dict[str, bytes]:
    """All owned view files as relpath -> bytes, regenerated purely from
    committed material under the given stamp."""
    normalized_policy = (
        normalize_product_mention_policy(product_mention_policy)
        if "by_mention" in views else None
    )
    sweep = (
        _classified_silver_sweep(root)
        if any(name in views for name in ("by_creator", "by_mention"))
        else None
    )
    files: dict[str, bytes] = {}
    for view_name in views:
        if view_name == "by_creator":
            view, source_refs = build_by_creator_view(root, sweep=sweep)
        elif view_name == "by_mention":
            view, source_refs = build_by_mention_view(
                root,
                product_mention_policy=normalized_policy,
                sweep=sweep,
            )
        else:
            view, source_refs = build_undone_view(root)
        view_bytes = canonical_record_bytes(view)
        manifest_bytes = canonical_record_bytes(
            _manifest(
                view_name,
                view_bytes,
                source_refs,
                stamp,
                normalized_policy,
            )
        )
        files[f"query_tables/{view_name}.json"] = view_bytes
        files[f"manifests/{view_name}.json"] = manifest_bytes
    return files


def _silver_vault_core_root(root) -> Path:
    return root._within(*SILVER_VAULT_CORE_PARTS)


def rebuild_derived_retrieval(
    root,
    *,
    product_mention_policy: dict[str, str],
    stamp: dict | None = None,
) -> dict:
    """Replace the owned views and remove their contradictory legacy home."""
    root._reverify()
    stamp = stamp or generation_stamp()
    files = _generate(root, stamp, product_mention_policy=product_mention_policy)
    target_root = _silver_vault_core_root(root)
    legacy_root = root._within("indexes", "derived_retrieval", "object_level")
    if legacy_root.exists():
        shutil.rmtree(legacy_root)
    for view_name in BUILT_VIEWS:
        for target in (
            target_root / "query_tables" / f"{view_name}.json",
            target_root / "manifests" / f"{view_name}.json",
        ):
            if target.exists():
                target.unlink()
    for relpath, data in files.items():
        target = target_root / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return {
        "status": "rebuilt",
        "views": list(BUILT_VIEWS),
        "deferred_views": [],
        "generation_id": stamp["generation_id"],
        "file_count": len(files),
    }


def prove_derived_retrieval_rebuildability(root) -> dict:
    """Read-only verification: regenerate every stored view under the stamps its
    stored manifest recorded and byte-compare. Never compares a rebuild against
    itself; never writes."""
    root._reverify()
    target_root = _silver_vault_core_root(root)
    results: dict[str, str] = {}
    failures: list[str] = []
    for view_name in BUILT_VIEWS:
        view_path = target_root / "query_tables" / f"{view_name}.json"
        manifest_path = target_root / "manifests" / f"{view_name}.json"
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
            product_mention_policy = (
                normalize_product_mention_policy(
                    stored_manifest["selection_policy_versions"]["product_mention_policy"]
                )
                if view_name == "by_mention"
                else None
            )
        except (ValueError, KeyError):
            results[view_name] = "failed_unreadable_manifest"
            failures.append(view_name)
            continue
        regenerated = _generate(
            root,
            stamp,
            product_mention_policy=product_mention_policy,
            views=(view_name,),
        )
        if (
            regenerated[f"query_tables/{view_name}.json"] == view_path.read_bytes()
            and regenerated[f"manifests/{view_name}.json"] == manifest_path.read_bytes()
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
    "BY_CREATOR_VIEW_SCHEMA_VERSION",
    "MANIFEST_SCHEMA_VERSION",
    "MENTIONS_LANE",
    "SILVER_VAULT_CORE_PARTS",
    "VIEW_SCHEMA_VERSION",
    "build_by_creator_view",
    "build_by_mention_view",
    "build_undone_view",
    "generation_stamp",
    "prove_derived_retrieval_rebuildability",
    "rebuild_derived_retrieval",
]
