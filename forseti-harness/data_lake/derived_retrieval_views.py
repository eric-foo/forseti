"""Gate-opened Silver Vault generated-read-model (lake-map) builder.

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
  ``acknowledgements/`` records. The disposable SQLite source inventory may
  reuse already-read immutable bytes and classification keys, but deleting it
  produces the same cold generation and readers never consult it.
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
- A complete generation is written beside the current one and published only
  by atomically replacing ``core/CURRENT``. Readers resolve that pointer once;
  an interrupted build cannot expose a mixed or partial generation.

Writes stay inside the contract-owned disposable index home. No behavior is
added to ``DataLakeRoot``.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sqlite3
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from data_lake.canonical_json import canonical_record_bytes
from data_lake.consumption import iter_all_acks
from data_lake.creator_metric_lineage import (
    OBSERVATION_LANE,
    ROLLUP_LANE,
    build_creator_metric_lineage_index,
)
from data_lake.derived_retrieval_cache import ClassificationCacheSession
from data_lake.derived_retrieval_state import IncrementalSourceInventory
from data_lake.lane_registry import LANE_ROLES, LaneRole
from data_lake.product_mention_selection import (
    MENTIONS_LANE,
    normalize_product_mention_policy,
    select_product_mention_records,
)
from data_lake.root import DataLakeRootError, _atomic_create, _atomic_replace
from data_lake.silver_record import (
    CURRENT_SOURCE_BACKED_AUTHORITY,
    PHYSICALLY_SOURCE_BACKED_COMPLETE_STATUS,
    SILVER_VAULT_RECORD_SCHEMA_VERSION,
    classify_silver_vault_record_sources,
)

UNDONE_VIEW_SCHEMA_VERSION = 1
BY_MENTION_VIEW_SCHEMA_VERSION = 3
BY_CREATOR_VIEW_SCHEMA_VERSION = 2
VIEW_SCHEMA_VERSION = BY_MENTION_VIEW_SCHEMA_VERSION
MANIFEST_SCHEMA_VERSION = 2
SILVER_VAULT_CORE_PARTS = ("indexes", "derived_retrieval", "silver_vault", "core")
BUILT_VIEWS = ("by_creator", "by_mention", "undone")
CURRENT_POINTER_FILENAME = "CURRENT"
CURRENT_POINTER_SCHEMA_VERSION = 1
GENERATIONS_DIRNAME = "generations"
_GENERATION_ID = re.compile(r"[0-9a-f]{32}")

FRAGRANTICA_PROJECTION_LANE = "projection_fragrantica"
FRAGRANTICA_PRODUCT_ROW_KIND = "fragrance_product_snapshot"

# Closed per-platform namespace vocabulary for account-card filing. An account
# subject naming any other namespace is a named residual, never a new platform
# key (exact lowercase canonical strings; extend deliberately per new platform).
KNOWN_PLATFORM_NAMESPACES = frozenset({"instagram", "tiktok", "youtube"})
# Key label when a record does not assert what kind of identifier its account
# native_id is (e.g. handle vs stable platform id). Distinct identity kinds
# never merge into one card key.
UNSPECIFIED_IDENTITY_KIND = "unspecified"
# Subject kinds known NOT to describe a creator account even though they carry
# a native_id (comments, retail product pages). Kinds outside this set and the
# two account-bearing shapes are named residuals, never guesses.
KNOWN_NON_ACCOUNT_SUBJECT_KINDS = frozenset({"public_comment", "retailer_product"})
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


def _generation_id(value: object) -> str:
    generation_id = str(value or "")
    if _GENERATION_ID.fullmatch(generation_id) is None:
        raise DataLakeRootError(
            f"invalid derived-retrieval generation id: {generation_id!r}"
        )
    return generation_id


def current_generation_root(root) -> tuple[Path, str | None, str]:
    """Resolve the complete current map generation.

    Fixed paths remain a migration fallback until the first
    generation-published rebuild creates ``CURRENT``.
    """
    core = _silver_vault_core_root(root)
    pointer = core / CURRENT_POINTER_FILENAME
    if not pointer.is_file():
        return core, None, "legacy_fixed_paths"
    try:
        payload = json.loads(pointer.read_text(encoding="utf-8"))
        if (
            not isinstance(payload, dict)
            or payload.get("pointer_schema_version")
            != CURRENT_POINTER_SCHEMA_VERSION
        ):
            raise ValueError("unsupported pointer schema")
        generation_id = _generation_id(payload["generation_id"])
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise DataLakeRootError(
            f"derived-retrieval CURRENT pointer is unreadable: {exc}"
        ) from exc
    generation_root = core / GENERATIONS_DIRNAME / generation_id
    if not generation_root.is_dir():
        raise DataLakeRootError(
            "derived-retrieval CURRENT pointer names an absent generation: "
            f"{generation_id}"
        )
    return generation_root, generation_id, "generation_pointer"


def load_derived_retrieval_view(
    root, view_name: str
) -> tuple[dict | None, dict | None, dict[str, Any]]:
    """Load and verify one sanctioned generated view/manifest pair."""
    if view_name not in BUILT_VIEWS:
        raise ValueError(f"unknown derived-retrieval view: {view_name!r}")
    generation_root, pointer_generation, layout = current_generation_root(root)
    view_path = generation_root / "query_tables" / f"{view_name}.json"
    manifest_path = generation_root / "manifests" / f"{view_name}.json"
    view_exists = view_path.is_file()
    manifest_exists = manifest_path.is_file()
    provenance = {
        "layout": layout,
        "pointer_generation_id": pointer_generation,
    }
    if not view_exists and not manifest_exists:
        return None, None, provenance
    if not view_exists or not manifest_exists:
        raise DataLakeRootError(
            f"{view_name} generated view/manifest pair is incomplete"
        )
    try:
        view_bytes = view_path.read_bytes()
        view = json.loads(view_bytes.decode("utf-8"))
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise DataLakeRootError(
            f"{view_name} generated view/manifest pair is unreadable: {exc}"
        ) from exc
    if not isinstance(view, dict) or not isinstance(manifest, dict):
        raise DataLakeRootError(
            f"{view_name} generated view/manifest must both be JSON objects"
        )
    if view.get("view") != view_name or manifest.get("view") != view_name:
        raise DataLakeRootError(
            f"{view_name} generated view/manifest identity mismatch"
        )
    if view.get("view_schema_version") != manifest.get("view_schema_version"):
        raise DataLakeRootError(
            f"{view_name} generated view/manifest schema mismatch"
        )
    if (
        pointer_generation is not None
        and manifest.get("generation_id") != pointer_generation
    ):
        raise DataLakeRootError(
            f"{view_name} manifest generation does not match CURRENT"
        )
    actual_sha256 = hashlib.sha256(view_bytes).hexdigest()
    if manifest.get("view_sha256") != actual_sha256:
        raise DataLakeRootError(
            f"{view_name} view_sha256 mismatch: manifest does not match view bytes"
        )
    return view, manifest, provenance


def build_undone_view(
    root,
    *,
    source_inventory: IncrementalSourceInventory | None = None,
) -> tuple[dict, list[str]]:
    """The undone view body plus the source refs its manifest must cite."""
    committed = sorted(root.list_available())
    acked_by_namespace: dict[str, set[str]] = {}
    ack_refs: list[str] = []
    if source_inventory is None:
        acknowledgements = iter_all_acks(root)
    else:
        acknowledgements = (
            (row.raw_anchor, row.lane, ack)
            for row in source_inventory.records(subtree="acknowledgements")
            for ack in (_acknowledgement_from_bytes(row.body),)
            if ack is not None
        )
    for raw_anchor, namespace, ack in acknowledgements:
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


def _acknowledgement_from_bytes(body: bytes) -> dict | None:
    """Match the consumption seam's safe acknowledgement parsing from bytes."""
    try:
        value = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return None
    if (
        isinstance(value, dict)
        and value.get("record_kind") == "acknowledgement"
        and isinstance(value.get("obligation_fingerprint"), str)
    ):
        return value
    return None


_ACTIVE_SILVER_ENVELOPE_LANES = tuple(
    sorted(
        (lane for lane, role in LANE_ROLES.items() if role is LaneRole.SILVER_ENVELOPE),
        key=lambda lane: (lane != OBSERVATION_LANE, lane),
    )
)
_CREATOR_METRIC_LANES = frozenset({OBSERVATION_LANE, ROLLUP_LANE})


def _classified_silver_sweep(
    root,
    *,
    cache_session: ClassificationCacheSession | None = None,
    source_inventory: IncrementalSourceInventory | None = None,
) -> dict[str, Any]:
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
    authority_by_ref: dict[str, Any] = {}
    verification_cache: dict[str, Any] = {}
    derived = root.path / "derived"
    lineage = None
    if source_inventory is None:
        source_rows = (
            (
                path,
                path.parents[1].name,
                lane,
                path.name,
                path.read_bytes(),
                None,
            )
            for lane in _ACTIVE_SILVER_ENVELOPE_LANES
            for path in sorted(derived.glob(f"*/*/{lane}/*"))
            if path.is_file()
        )
    else:
        source_rows = (
            (
                root.path / row.relative_path,
                row.raw_anchor,
                row.lane,
                row.record_id,
                row.body,
                row,
            )
            for row in source_inventory.records(
                subtree="derived", lanes=_ACTIVE_SILVER_ENVELOPE_LANES
            )
        )
    previous_classifier_version = (
        source_inventory.metadata("classifier_version")
        if source_inventory is not None
        else None
    )
    previous_lineage_fingerprint = (
        source_inventory.metadata("creator_lineage_state_fingerprint")
        if source_inventory is not None
        else None
    )
    previous_catalog_fingerprint = (
        source_inventory.metadata("bronze_catalog_fingerprint")
        if source_inventory is not None
        else None
    )
    current_catalog_fingerprint: str | None = None
    for path, anchor, lane, record_id, body, stored_row in source_rows:
            ref_key = f"{anchor}/{lane}/{record_id}"
            try:
                record = json.loads(body.decode("utf-8"))
            except (UnicodeDecodeError, ValueError):
                residuals.append(
                    {
                        "status": "unreadable",
                        "raw_anchor": anchor,
                        "lane": lane,
                        "record_id": record_id,
                    }
                )
                continue
            if (
                cache_session is not None
                and lane == OBSERVATION_LANE
                and isinstance(record, dict)
            ):
                cache_session.register_creator_metric_observation(
                    record, record_path=path
                )
            if (
                not isinstance(record, dict)
                or record.get("schema_version") != SILVER_VAULT_RECORD_SCHEMA_VERSION
            ):
                residuals.append(
                    {
                        "status": "non_envelope_schema_audit_only",
                        "raw_anchor": anchor,
                        "lane": lane,
                        "record_id": record_id,
                    }
                )
                continue
            source_refs.append(ref_key)
            cache_key = (
                stored_row.classification_cache_key
                if stored_row is not None
                else None
            )
            authority = None
            attachment_backed = any(
                isinstance(ref, dict)
                and ref.get("ref_type") == "bronze_attachment_record"
                for ref in record.get("raw_refs", [])
            )
            creator_metric = record.get("lane_namespace") in _CREATOR_METRIC_LANES
            if cache_session is not None:
                global_key_state_matches = (
                    previous_classifier_version == cache_session.classifier_version
                )
                if creator_metric:
                    global_key_state_matches = (
                        global_key_state_matches
                        and previous_lineage_fingerprint
                        == cache_session.lineage_fingerprint
                    )
                if attachment_backed:
                    if current_catalog_fingerprint is None:
                        current_catalog_fingerprint = (
                            cache_session.catalog_fingerprint()
                        )
                    global_key_state_matches = (
                        global_key_state_matches
                        and previous_catalog_fingerprint
                        == current_catalog_fingerprint
                    )
                if cache_key is not None and global_key_state_matches:
                    authority = cache_session.lookup_cached_key(cache_key)
                if authority is None:
                    cache_key, authority = cache_session.lookup(
                        record, record_path=path
                    )
            if authority is None:
                if (
                    record.get("lane_namespace") in _CREATOR_METRIC_LANES
                    and lineage is None
                ):
                    lineage = build_creator_metric_lineage_index(root)
                authority = classify_silver_vault_record_sources(
                    root,
                    record,
                    record_path=path,
                    creator_metric_lineage=lineage,
                    verification_cache=verification_cache,
                )
                if cache_session is not None:
                    cache_session.remember(cache_key, authority)
            if source_inventory is not None and stored_row is not None:
                source_inventory.remember_classification_cache_key(
                    stored_row.relative_path, cache_key
                )
            authority_by_ref[ref_key] = authority
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
            account_keys, account_problems = _account_subject_keys(record)
            for problem in account_problems:
                residuals.append(
                    {
                        **problem,
                        "raw_anchor": anchor,
                        "lane": lane,
                        "record_id": record_id,
                    }
                )
            for namespace, identity_kind, native_id, aliases in account_keys:
                entry = accounts.setdefault(
                    (namespace, identity_kind, native_id),
                    {
                        "aliases": {},
                        "alias_values": defaultdict(set),
                        "refs_by_anchor": defaultdict(list),
                    },
                )
                for alias_key, alias_value in aliases.items():
                    # Cold is shard-ordered while the inventory is anchor-ordered.
                    # Pick a stable minimum so modeled alias conflicts cannot make
                    # published bytes depend on the builder path.
                    current = entry["aliases"].get(alias_key)
                    if current is None or str(alias_value) < str(current):
                        entry["aliases"][alias_key] = alias_value
                    entry["alias_values"][alias_key].add(str(alias_value))
                entry["refs_by_anchor"][anchor].append(ref)
    if source_inventory is not None and cache_session is not None:
        source_inventory.remember_metadata(
            "classifier_version", cache_session.classifier_version
        )
        source_inventory.remember_metadata(
            "creator_lineage_state_fingerprint",
            cache_session.lineage_fingerprint,
        )
        if current_catalog_fingerprint is not None:
            source_inventory.remember_metadata(
                "bronze_catalog_fingerprint", current_catalog_fingerprint
            )
    for (namespace, identity_kind, native_id), entry in sorted(accounts.items()):
        for alias_key, alias_values in sorted(entry["alias_values"].items()):
            if len(alias_values) > 1:
                residuals.append(
                    {
                        "status": "account_alias_conflict",
                        "namespace": namespace,
                        "identity_kind": identity_kind,
                        "native_id": native_id,
                        "alias_key": alias_key,
                        "alias_values": sorted(alias_values),
                    }
                )
    return {
        "anchor_lane_status": anchor_lane_status,
        "accounts": accounts,
        "source_refs": sorted(source_refs),
        "authority_by_ref": authority_by_ref,
        "residuals": sorted(residuals, key=lambda row: json.dumps(row, sort_keys=True)),
    }


def _account_subject_keys(
    record: dict,
) -> tuple[list[tuple[str, str, str, dict[str, Any]]], list[dict[str, Any]]]:
    """Per-platform public-account keys a record's subject asserts, plus the
    named problems for account-describing shapes the view cannot file.

    Keys are ``(namespace, identity_kind, native_id)``: the identity kind the
    record asserts for its account identifier (e.g. ``youtube_channel_id``) or
    ``unspecified`` when unasserted. Distinct identity kinds never merge into
    one key. A ``platform_public_account`` subject files directly; a
    ``public_content_object`` subject files via its publishing account. Exact
    strings preserved. Account-describing shapes that cannot be filed (missing
    identifiers, unknown platform namespace, unknown subject kind carrying
    account-identifier fields) return problems so absence stays labeled, never
    silent."""
    payload = record.get("payload")
    observation = payload.get("observation") if isinstance(payload, dict) else None
    subject = observation.get("subject") if isinstance(observation, dict) else None
    if not isinstance(subject, dict) or subject.get("ref_type") != "entity_key":
        return [], []
    ref = subject.get("ref")
    if not isinstance(ref, dict):
        return [], []
    kind = str(ref.get("kind") or "").strip()
    namespace = str(ref.get("namespace") or "").strip()
    keys: list[tuple[str, str, str, dict[str, Any]]] = []
    problems: list[dict[str, Any]] = []

    def _file_account(native_id: str, identity_kind: str, aliases: dict[str, Any]) -> None:
        missing = [
            field
            for field, value in (("namespace", namespace), ("native_id", native_id))
            if not value
        ]
        if missing:
            problems.append(
                {
                    "status": "unrecognized_account_subject_shape",
                    "subject_ref_kind": kind,
                    "missing_fields": missing,
                }
            )
        elif namespace not in KNOWN_PLATFORM_NAMESPACES:
            problems.append(
                {
                    "status": "unrecognized_platform_namespace",
                    "subject_ref_kind": kind,
                    "namespace": namespace,
                }
            )
        else:
            keys.append((namespace, identity_kind, native_id, aliases))

    if kind == "platform_public_account":
        identity_kind = str(ref.get("native_id_kind") or "").strip() or UNSPECIFIED_IDENTITY_KIND
        aliases = {
            field: ref[field] for field in ("orca_platform_account_id",) if ref.get(field)
        }
        _file_account(str(ref.get("native_id") or "").strip(), identity_kind, aliases)
    elif kind == "public_content_object":
        if ref.get("published_by_account_native_id") is not None:
            identity_kind = (
                str(ref.get("published_by_account_native_id_kind") or "").strip()
                or UNSPECIFIED_IDENTITY_KIND
            )
            aliases = {
                field: ref[field] for field in ("orca_platform_account_id",) if ref.get(field)
            }
            _file_account(
                str(ref.get("published_by_account_native_id") or "").strip(),
                identity_kind,
                aliases,
            )
        # A content object without a publisher assertion is not account-describing.
    elif any(
        ref.get(field)
        for field in ("native_id", "published_by_account_native_id", "orca_platform_account_id")
    ) and kind not in KNOWN_NON_ACCOUNT_SUBJECT_KINDS:
        # Unknown subject kind carrying account-identifier fields: the map does
        # not guess; it names the shape so a wiring gap never reads as
        # "not captured".
        problems.append(
            {
                "status": "unrecognized_account_subject_shape",
                "subject_ref_kind": kind or None,
                "missing_fields": [],
            }
        )
    return keys, problems


def build_by_creator_view(root, *, sweep: dict | None = None) -> tuple[dict, list[str]]:
    """The per-platform by_creator view plus the source refs its manifest cites.

    (platform namespace, observed public account id) -> committed packet +
    Silver-record refs with build-time authority classification. Object-level
    only; no cross-platform identity is unified.
    """
    sweep = sweep or _classified_silver_sweep(root)
    creators: dict[str, dict[str, Any]] = {}
    for (namespace, identity_kind, native_id), entry in sorted(sweep["accounts"].items()):
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
        creators.setdefault(namespace, {}).setdefault(identity_kind, {})[native_id] = {
            "aliases": dict(sorted(entry["aliases"].items())),
            "packets": packets,
            "anchor_level_totals_by_status": dict(sorted(totals.items())),
        }
    view = {
        "view": "by_creator",
        "view_schema_version": BY_CREATOR_VIEW_SCHEMA_VERSION,
        "semantics": (
            "(platform namespace, asserted identity kind, observed public account "
            "native id) -> committed packet + Silver record refs; identity kind is "
            "the record-asserted kind of the account identifier (or 'unspecified'); "
            "distinct identity kinds never merge into one key; platform namespaces "
            "come from a closed vocabulary and unknown namespaces or unfileable "
            "account shapes are named residuals, never silent drops; authority "
            "statuses computed at build time by "
            "data_lake.silver_record.classify_silver_vault_record_sources; "
            "per-platform object-level only, no cross-platform identity; exact "
            "observed strings preserved (normalization is the reader's concern)"
        ),
        "zero_rows_meaning": _MISSING_EVIDENCE_NOTE,
        "creators": creators,
        "creator_count": sum(
            len(ids) for kinds in creators.values() for ids in kinds.values()
        ),
        "residuals": sweep["residuals"],
        "residual_count": len(sweep["residuals"]),
    }
    return view, list(sweep["source_refs"])


def _fragrantica_native_product_identity(row: dict) -> dict[str, str]:
    """Fragrantica projection row -> the source-neutral identity fields the
    shared native-product-page loop consumes."""
    visible = row.get("source_visible_fields")
    return {
        "brand": str(row.get("brand_or_house") or "").strip(),
        "line": str(row.get("source_object_name") or "").strip(),
        "source_site": str(row.get("source_platform") or "fragrantica").strip(),
        "site_native_id": str(row.get("source_object_site_id") or "").strip(),
        "canonical_url": (
            str(visible.get("canonical_url") or "").strip()
            if isinstance(visible, dict)
            else ""
        ),
    }


# Closed registry of the projection sources that may establish native
# product-page identity. Adding a product-identity source (e.g. a future
# non-Fragrantica domain) is a deliberate registry entry with its own
# extractor, never a rewrite of the shared loop.
NATIVE_PRODUCT_PAGE_SOURCES: tuple[tuple[str, str, Any], ...] = (
    (
        FRAGRANTICA_PROJECTION_LANE,
        FRAGRANTICA_PRODUCT_ROW_KIND,
        _fragrantica_native_product_identity,
    ),
)


def _incremental_source_lanes() -> tuple[str, ...]:
    return tuple(
        sorted(
            set(_ACTIVE_SILVER_ENVELOPE_LANES)
            | {lane for lane, _row_kind, _extractor in NATIVE_PRODUCT_PAGE_SOURCES}
        )
    )


def _cold_source_inventory(root) -> dict[str, object]:
    rows = []
    derived = root.path / "derived"
    for lane in _incremental_source_lanes():
        for path in sorted(derived.glob(f"*/*/{lane}/*")):
            if path.is_file():
                rows.append(
                    {
                        "relative_path": path.relative_to(root.path).as_posix(),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    }
                )
    acknowledgements = root.path / "acknowledgements"
    if acknowledgements.is_dir():
        for path in sorted(acknowledgements.glob("*/*/*/*")):
            if path.is_file():
                rows.append(
                    {
                        "relative_path": path.relative_to(root.path).as_posix(),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    }
                )
    rows.sort(key=lambda row: str(row["relative_path"]))
    return {
        "source_count": len(rows),
        "source_inventory_sha256": hashlib.sha256(
            canonical_record_bytes(rows)
        ).hexdigest(),
    }


def _input_fingerprint(
    root,
    *,
    source_inventory: IncrementalSourceInventory,
    cache_session: ClassificationCacheSession,
    product_mention_policy: dict[str, str],
) -> str:
    _undone, undone_source_refs = build_undone_view(
        root, source_inventory=source_inventory
    )
    payload = {
        "derived_source_inventory": source_inventory.inventory(),
        "undone_source_refs": undone_source_refs,
        "product_mention_policy": normalize_product_mention_policy(
            product_mention_policy
        ),
        "classifier_version": cache_session.classifier_version,
        "creator_lineage_state_fingerprint": cache_session.lineage_fingerprint,
        "bronze_catalog_fingerprint": cache_session.catalog_fingerprint(),
    }
    return hashlib.sha256(canonical_record_bytes(payload)).hexdigest()


def _native_product_pages(
    root,
    sweep: dict,
    *,
    source_inventory: IncrementalSourceInventory | None = None,
) -> tuple[dict, list[str], list[dict]]:
    """Native product-page identity rows from the registered projection
    sources (view-only mechanical records used as identity ROUTING, never
    authority), each joined to its anchor's classified Silver record counts."""
    pages: dict[str, dict[str, dict[tuple[str, str, str], dict]]] = {}
    identity_bindings: dict[tuple[str, str, str], tuple[str, str, dict]] = {}
    source_refs: set[str] = set()
    residuals: list[dict[str, Any]] = []
    derived = root.path / "derived"
    for source_lane, source_row_kind, extract_identity in NATIVE_PRODUCT_PAGE_SOURCES:
        if source_inventory is None:
            source_rows = (
                (
                    path.parents[1].name,
                    path.name,
                    path.read_bytes(),
                )
                for path in sorted(derived.glob(f"*/*/{source_lane}/*"))
                if path.is_file()
            )
        else:
            source_rows = (
                (row.raw_anchor, row.record_id, row.body)
                for row in source_inventory.records(
                    subtree="derived", lanes=(source_lane,)
                )
            )
        for anchor, record_id, body in source_rows:
            try:
                projection = json.loads(body.decode("utf-8"))
            except (UnicodeDecodeError, ValueError):
                continue
            rows = projection.get("rows") if isinstance(projection, dict) else None
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict) or row.get("row_kind") != source_row_kind:
                    continue
                source_ref = f"{anchor}/{source_lane}/{record_id}"
                source_refs.add(source_ref)
                identity = extract_identity(row)
                brand = identity["brand"]
                line = identity["line"]
                missing_fields = [
                    field
                    for field, value in (("brand", brand), ("line", line))
                    if not value
                ]
                if missing_fields:
                    residuals.append(
                        {
                            "status": "native_product_page_identity_incomplete",
                            "raw_anchor": anchor,
                            "lane": source_lane,
                            "record_id": record_id,
                            "row_id": row.get("row_id"),
                            "missing_fields": missing_fields,
                        }
                    )
                    continue
                canonical_url = identity["canonical_url"]
                site_native_id = identity["site_native_id"]
                source_site = identity["source_site"]
                entry = {
                    "source_site": source_site,
                    "site_native_id": site_native_id or None,
                    "canonical_url": canonical_url or None,
                    "raw_anchor": anchor,
                    "identity_source": (
                        f"{source_lane} {source_row_kind} row "
                        "(view-only mechanical projection; identity routing, not Silver authority)"
                    ),
                    "anchor_silver_records_by_lane_status": {
                        lane: dict(sorted(statuses.items()))
                        for lane, statuses in sorted(sweep["anchor_lane_status"][anchor].items())
                    },
                }
                identity_key = (anchor, source_site, site_native_id or canonical_url)
                existing = identity_bindings.get(identity_key)
                if existing is None:
                    identity_bindings[identity_key] = (brand, line, entry)
                    pages.setdefault(brand, {}).setdefault(line, {})[identity_key] = entry
                elif existing != (brand, line, entry):
                    kept_brand, kept_line, kept_entry = existing
                    residuals.append(
                        {
                            "status": "native_product_page_identity_conflict",
                            "raw_anchor": anchor,
                            "lane": source_lane,
                            "record_id": record_id,
                            "row_id": row.get("row_id"),
                            "brand": brand,
                            "line": line,
                            "source_site": source_site,
                            "site_native_id": site_native_id or None,
                            "kept_brand": kept_brand,
                            "kept_line": kept_line,
                            "kept_canonical_url": kept_entry.get("canonical_url"),
                            "conflicting_canonical_url": canonical_url or None,
                        }
                    )
    normalized = {
        brand: {
            line: sorted(
                entries.values(),
                key=lambda entry: (
                    str(entry["raw_anchor"]),
                    str(entry["source_site"]),
                    str(entry["site_native_id"]),
                    str(entry["canonical_url"]),
                ),
            )
            for line, entries in sorted(lines.items())
        }
        for brand, lines in sorted(pages.items())
    }
    return (
        normalized,
        sorted(source_refs),
        sorted(residuals, key=lambda row: json.dumps(row, sort_keys=True)),
    )


def build_by_mention_view(
    root,
    *,
    product_mention_policy: dict[str, str],
    sweep: dict | None = None,
    source_inventory: IncrementalSourceInventory | None = None,
) -> tuple[dict, list[str]]:
    """The exact-policy by_mention view plus every non-evidence residual."""
    sweep = sweep or _classified_silver_sweep(
        root, source_inventory=source_inventory
    )
    selection = select_product_mention_records(
        root,
        policy=product_mention_policy,
        preclassified_authority=sweep["authority_by_ref"],
        source_records=(
            source_inventory.records(
                subtree="derived", lanes=(MENTIONS_LANE,)
            )
            if source_inventory is not None
            else None
        ),
    )
    mentions: dict[str, dict[str, list[dict]]] = {}
    mention_ref_keys: dict[tuple[str, str], set[tuple[str, str, str]]] = defaultdict(set)
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
            ref_key = (selected.raw_anchor, MENTIONS_LANE, selected.record_id)
            if ref_key not in mention_ref_keys[(brand, line)]:
                mention_ref_keys[(brand, line)].add(ref_key)
                refs.append(ref)
    native_pages, native_refs, native_residuals = _native_product_pages(
        root, sweep, source_inventory=source_inventory
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
        "residuals": list(selection.residuals) + native_residuals,
        "residual_count": len(selection.residuals) + len(native_residuals),
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
    source_inventory: dict[str, object],
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
        "freshness": {
            "posture": "current_as_of_generation",
            "reconciled_at": stamp["generated_at"],
            "derived_source_inventory": source_inventory,
        },
        "stale_if": (
            "any committed availability/derived/acknowledgement change after "
            "this generation; refresh before same-day analysis or verify with "
            "--prove-rebuildability"
        ),
    }


def _generate(
    root,
    stamp: dict,
    *,
    product_mention_policy: dict[str, str] | None,
    views: tuple[str, ...] = BUILT_VIEWS,
    cache_session: ClassificationCacheSession | None = None,
    source_inventory: IncrementalSourceInventory | None = None,
) -> dict[str, bytes]:
    """All owned view files as relpath -> bytes, regenerated purely from
    committed material under the given stamp."""
    normalized_policy = (
        normalize_product_mention_policy(product_mention_policy)
        if "by_mention" in views else None
    )
    inventory_state = (
        source_inventory.inventory()
        if source_inventory is not None
        else _cold_source_inventory(root)
    )
    sweep = (
        _classified_silver_sweep(
            root,
            cache_session=cache_session,
            source_inventory=source_inventory,
        )
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
                source_inventory=source_inventory,
            )
        else:
            view, source_refs = build_undone_view(
                root, source_inventory=source_inventory
            )
        view_bytes = canonical_record_bytes(view)
        manifest_bytes = canonical_record_bytes(
            _manifest(
                view_name,
                view_bytes,
                source_refs,
                stamp,
                normalized_policy,
                inventory_state,
            )
        )
        files[f"query_tables/{view_name}.json"] = view_bytes
        files[f"manifests/{view_name}.json"] = manifest_bytes
    return files


def _silver_vault_core_root(root) -> Path:
    return root._within(*SILVER_VAULT_CORE_PARTS)


def _publish_generation(root, files: dict[str, bytes], stamp: dict) -> Path:
    """Publish one complete immutable map generation, then switch CURRENT."""
    generation_id = _generation_id(stamp.get("generation_id"))
    core = _silver_vault_core_root(root)
    generations = core / GENERATIONS_DIRNAME
    generations.mkdir(parents=True, exist_ok=True)
    target = generations / generation_id
    staging = generations / f".building-{generation_id}-{uuid.uuid4().hex}"
    staging.mkdir(parents=False, exist_ok=False)
    try:
        for relpath, data in sorted(files.items()):
            destination = staging / relpath
            destination.parent.mkdir(parents=True, exist_ok=True)
            _atomic_create(destination, data)
        if target.exists():
            mismatches = [
                relpath
                for relpath, data in sorted(files.items())
                if not (target / relpath).is_file()
                or (target / relpath).read_bytes() != data
            ]
            if mismatches:
                raise DataLakeRootError(
                    "derived-retrieval generation id collision with different "
                    f"bytes: {generation_id}: {mismatches}"
                )
        else:
            os.replace(staging, target)
        pointer_bytes = canonical_record_bytes(
            {
                "pointer_schema_version": CURRENT_POINTER_SCHEMA_VERSION,
                "generation_id": generation_id,
            }
        )
        _atomic_replace(core / CURRENT_POINTER_FILENAME, pointer_bytes)
        return target
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def rebuild_derived_retrieval(
    root,
    *,
    product_mention_policy: dict[str, str],
    stamp: dict | None = None,
    full_rebuild: bool = False,
) -> dict:
    """Replace the owned views and remove their contradictory legacy home."""
    root._reverify()
    allow_noop = stamp is None
    stamp = stamp or generation_stamp()
    cache_session = ClassificationCacheSession(
        root, use_existing=not full_rebuild
    )
    with IncrementalSourceInventory(root, reset=full_rebuild) as source_inventory:
        source_inventory.refresh(
            derived_lanes=_incremental_source_lanes(),
            include_acknowledgements=True,
        )
        sql_catalogue = refresh_sql_catalogue(
            root, source_inventory, full_rebuild=full_rebuild
        )
        input_fingerprint = _input_fingerprint(
            root,
            source_inventory=source_inventory,
            cache_session=cache_session,
            product_mention_policy=product_mention_policy,
        )
        _current_root, current_generation_id, current_layout = (
            current_generation_root(root)
        )
        if (
            allow_noop
            and not full_rebuild
            and current_generation_id is not None
            and source_inventory.metadata("last_input_fingerprint")
            == input_fingerprint
        ):
            return {
                "status": "current",
                "views": list(BUILT_VIEWS),
                "deferred_views": [],
                "generation_id": current_generation_id,
                "file_count": len(BUILT_VIEWS) * 2,
                "classification_cache": cache_session.report(),
                "source_inventory": source_inventory.report(),
                "generation_root": str(_current_root),
                "layout": current_layout,
                "full_rebuild": False,
                "sql_catalogue": sql_catalogue,
            }
        files = _generate(
            root,
            stamp,
            product_mention_policy=product_mention_policy,
            cache_session=cache_session,
            source_inventory=source_inventory,
        )
        legacy_root = root._within("indexes", "derived_retrieval", "object_level")
        if legacy_root.exists():
            shutil.rmtree(legacy_root)
        cache_session.save()
        generation_root = _publish_generation(root, files, stamp)
        source_inventory.remember_metadata(
            "last_input_fingerprint", input_fingerprint
        )
        source_inventory.remember_metadata(
            "last_generation_id", stamp["generation_id"]
        )
        source_inventory_report = source_inventory.report()
    return {
        "status": "rebuilt",
        "views": list(BUILT_VIEWS),
        "deferred_views": [],
        "generation_id": stamp["generation_id"],
        "file_count": len(files),
        "classification_cache": cache_session.report(),
        "source_inventory": source_inventory_report,
        "generation_root": str(generation_root),
        "full_rebuild": full_rebuild,
        "sql_catalogue": sql_catalogue,
    }


def prove_incremental_rebuild_equality(
    root,
    *,
    product_mention_policy: dict[str, str],
) -> dict:
    """Byte-compare incremental generation with a full cold generation."""
    root._reverify()
    stamp = generation_stamp()
    incremental_cache = ClassificationCacheSession(root, use_existing=True)
    with IncrementalSourceInventory(
        root, persistent=False
    ) as source_inventory:
        source_inventory.refresh(
            derived_lanes=_incremental_source_lanes(),
            include_acknowledgements=True,
        )
        incremental = _generate(
            root,
            stamp,
            product_mention_policy=product_mention_policy,
            cache_session=incremental_cache,
            source_inventory=source_inventory,
        )
        source_inventory_report = source_inventory.report()
    cold_cache = ClassificationCacheSession(root, use_existing=False)
    cold = _generate(
        root,
        stamp,
        product_mention_policy=product_mention_policy,
        cache_session=cold_cache,
    )
    mismatches = sorted(
        relpath
        for relpath in set(incremental) | set(cold)
        if incremental.get(relpath) != cold.get(relpath)
    )
    return {
        "status": "proven" if not mismatches else "failed",
        "mismatched_files": mismatches,
        "file_count": len(cold),
        "incremental_classification_cache": incremental_cache.report(),
        "incremental_source_inventory": source_inventory_report,
        "cold_classification_cache": cold_cache.report(),
    }


def audit_derived_retrieval_source_integrity(root) -> dict:
    """Cold, read-only re-hash and byte proof against the stored lake map."""
    report = prove_derived_retrieval_rebuildability(root)
    return {
        **report,
        "mode": "source_integrity_audit",
        "semantics": (
            "full cold source verification and byte comparison against stored views; "
            "no classification-cache verdict is trusted"
        ),
    }


def prove_derived_retrieval_rebuildability(root) -> dict:
    """Read-only verification: regenerate every stored view under the stamps its
    stored manifest recorded and byte-compare. Never compares a rebuild against
    itself; never writes."""
    root._reverify()
    target_root, _generation_id_value, _layout = current_generation_root(root)
    view_paths = {
        view_name: target_root / "query_tables" / f"{view_name}.json"
        for view_name in BUILT_VIEWS
    }
    manifest_paths = {
        view_name: target_root / "manifests" / f"{view_name}.json"
        for view_name in BUILT_VIEWS
    }
    if all(
        view_paths[name].is_file() and manifest_paths[name].is_file()
        for name in BUILT_VIEWS
    ):
        try:
            stored_manifests = {
                name: json.loads(manifest_paths[name].read_text(encoding="utf-8"))
                for name in BUILT_VIEWS
            }
            stamps = {
                (
                    manifest["generation_id"],
                    manifest["generated_at"],
                )
                for manifest in stored_manifests.values()
            }
            if len(stamps) != 1:
                raise ValueError("stored view manifests do not share one generation")
            generation_id, generated_at = next(iter(stamps))
            product_mention_policy = normalize_product_mention_policy(
                stored_manifests["by_mention"]["selection_policy_versions"][
                    "product_mention_policy"
                ]
            )
        except (ValueError, KeyError, TypeError):
            pass
        else:
            regenerated = _generate(
                root,
                {
                    "generation_id": generation_id,
                    "generated_at": generated_at,
                },
                product_mention_policy=product_mention_policy,
            )
            results = {}
            failures = []
            for view_name in BUILT_VIEWS:
                matches = (
                    regenerated[f"query_tables/{view_name}.json"]
                    == view_paths[view_name].read_bytes()
                    and regenerated[f"manifests/{view_name}.json"]
                    == manifest_paths[view_name].read_bytes()
                )
                results[view_name] = (
                    "rebuildable"
                    if matches
                    else "failed_drift_or_non_regenerable"
                )
                if not matches:
                    failures.append(view_name)
            return {
                "status": "proven" if not failures else "failed",
                "results": results,
                "failures": failures,
            }
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


# Disposable SQL reader catalogue. The lake remains authority; actor identifiers
# are hydrated from cited evidence for one query and never stored in SQL.
SQL_CATALOGUE_SCHEMA_VERSION = 1
SQL_EXTRACTOR_PROFILE = "derived_retrieval_evidence_v1"
SQL_EVENT_LANES = frozenset({
    "cleaning_basenotes_silver", "cleaning_fragrantica_silver",
    "cleaning_parfumo_silver", "retail_pdp_silver",
    "silver__capture__audience_comments",
})
SQL_RAW_SURFACES = frozenset({
    "tiktok_creator_batch_comment_subtitle_admission",
    "youtube_watch_metadata_comments",
})
# Bound on the candidate window an exact-actor rehydration may scan. Reaching it
# means the window was truncated, which is a loud failure, never a short answer.
SQL_ACTOR_CANDIDATE_LIMIT = 10000
SQL_QUERY_CONTRACT_VERSION = 1
SQL_QUERY_AUDIT_SCHEMA_VERSION = 2
SQL_DECISION_QUESTION_ID_MAX_LENGTH = 128
SQL_SOURCE_LOOKUP_CHUNK = 500
SQL_DECISION_QUESTIONS = frozenset({
    "creator_comment_coordination", "content_comment_coordination",
    "bounded_public_actor_context",
})


def sql_catalogue_path(root) -> Path:
    configured = os.environ.get("FORSETI_DERIVED_RETRIEVAL_SQL_ROOT")
    if configured:
        base = Path(configured).expanduser()
        if not base.is_absolute():
            raise DataLakeRootError("FORSETI_DERIVED_RETRIEVAL_SQL_ROOT must be absolute")
        if os.name == "nt" and str(base).startswith(("\\", "//")):
            raise DataLakeRootError("SQLite catalogue root must be local, not a network share")
        lake_key = hashlib.sha256(str(root.path.resolve()).encode()).hexdigest()[:16]
        return base / lake_key / "catalogue.sqlite3"
    return root._within(*SILVER_VAULT_CORE_PARTS, "sql", "catalogue.sqlite3")


def _dr_connect(path: Path, *, read_only: bool = False):
    if read_only:
        connection = sqlite3.connect("file:%s?mode=ro" % path, uri=True, timeout=5)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(str(path), timeout=0, isolation_level=None)
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA synchronous=FULL")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys=ON")
    return connection


# Issued one statement at a time inside the caller's IMMEDIATE transaction:
# executescript() COMMITs any pending transaction first, which would let a
# --full-rebuild that dies mid-extraction leave the catalogue dropped instead
# of untouched.
_DR_RESET_STATEMENTS = (
    "DROP TRIGGER IF EXISTS dr_ai",
    "DROP TRIGGER IF EXISTS dr_ad",
    "DROP TABLE IF EXISTS evidence_fts",
    "DROP TABLE IF EXISTS evidence_events",
    "DROP TABLE IF EXISTS evidence_sources",
    "DROP TABLE IF EXISTS evidence_metadata",
)
_DR_SCHEMA_STATEMENTS = (
    """CREATE TABLE IF NOT EXISTS evidence_metadata(
      key TEXT PRIMARY KEY, value TEXT NOT NULL) STRICT""",
    """CREATE TABLE IF NOT EXISTS evidence_sources(
      source_ref TEXT PRIMARY KEY, source_kind TEXT NOT NULL,
      raw_anchor TEXT NOT NULL, source_sha256 TEXT NOT NULL,
      extractor_profile TEXT NOT NULL, event_count INTEGER NOT NULL,
      residuals_json TEXT NOT NULL) STRICT""",
    """CREATE TABLE IF NOT EXISTS evidence_events(
      row_id INTEGER PRIMARY KEY, event_id TEXT NOT NULL UNIQUE,
      source_ref TEXT NOT NULL REFERENCES evidence_sources(source_ref) ON DELETE CASCADE,
      source_kind TEXT NOT NULL, event_locator TEXT NOT NULL,
      event_kind TEXT NOT NULL CHECK(event_kind IN ('comment','review')),
      raw_anchor TEXT NOT NULL, source_family TEXT, source_surface TEXT,
      platform TEXT, vendor TEXT, creator_namespace TEXT,
      creator_native_id TEXT, creator_observed_handle TEXT,
      content_native_id TEXT, product_namespace TEXT, product_native_id TEXT,
      event_time_utc TEXT, event_time_precision TEXT, event_time_source_text TEXT,
      post_time_utc TEXT, capture_time_utc TEXT, body_text TEXT NOT NULL,
      body_sha256 TEXT NOT NULL, authority_status TEXT NOT NULL,
      limitations_json TEXT NOT NULL) STRICT""",
    """CREATE INDEX IF NOT EXISTS dr_creator_time ON evidence_events(
      creator_namespace,creator_native_id,event_time_utc)""",
    """CREATE INDEX IF NOT EXISTS dr_content_time ON evidence_events(
      platform,content_native_id,event_time_utc)""",
    """CREATE INDEX IF NOT EXISTS dr_product_time ON evidence_events(
      product_namespace,product_native_id,event_time_utc)""",
    """CREATE INDEX IF NOT EXISTS dr_surface_time ON evidence_events(
      source_surface,event_time_utc)""",
    "CREATE INDEX IF NOT EXISTS dr_body_hash ON evidence_events(body_sha256)",
    """CREATE VIRTUAL TABLE IF NOT EXISTS evidence_fts USING fts5(
      body_text,content='evidence_events',content_rowid='row_id',tokenize='unicode61')""",
    """CREATE TRIGGER IF NOT EXISTS dr_ai AFTER INSERT ON evidence_events BEGIN
      INSERT INTO evidence_fts(rowid,body_text) VALUES(new.row_id,new.body_text);
    END""",
    """CREATE TRIGGER IF NOT EXISTS dr_ad AFTER DELETE ON evidence_events BEGIN
      INSERT INTO evidence_fts(evidence_fts,rowid,body_text)
      VALUES('delete',old.row_id,old.body_text);
    END""",
)


def _dr_schema(connection, *, reset: bool) -> None:
    if reset:
        for statement in _DR_RESET_STATEMENTS:
            connection.execute(statement)
    for statement in _DR_SCHEMA_STATEMENTS:
        connection.execute(statement)
    row = connection.execute(
        "SELECT value FROM evidence_metadata WHERE key='schema_version'"
    ).fetchone()
    if row is None:
        connection.execute(
            "INSERT INTO evidence_metadata VALUES('schema_version',?)",
            (str(SQL_CATALOGUE_SCHEMA_VERSION),),
        )
    elif row[0] != str(SQL_CATALOGUE_SCHEMA_VERSION):
        raise DataLakeRootError("SQL catalogue schema changed; run --full-rebuild")


def _dr_text(value):
    return value.strip() if isinstance(value, str) and value.strip() else None


def _dr_map(value):
    return value if isinstance(value, dict) else {}


def _dr_list(value):
    return value if isinstance(value, list) else []


def _dr_time(value):
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return datetime.fromtimestamp(value, timezone.utc).isoformat(), "second", None
    text = _dr_text(value)
    if text is None:
        return None, None, None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None, None, text
    if parsed.tzinfo is None:
        if len(text) != 10:
            return None, None, text
        parsed = parsed.replace(tzinfo=timezone.utc)
        precision = "day"
    else:
        precision = "second"
    return parsed.astimezone(timezone.utc).isoformat(), precision, text


def _dr_window_bound(value, label):
    """Stored event/capture times are canonical UTC ``+00:00`` isoformat and the
    window filter compares them as TEXT. A caller bound must be normalized the
    same way first, or a ``Z``-suffixed or non-UTC-offset bound silently selects
    a lexicographically shifted window instead of the requested instants."""
    normalized, _precision, _source_text = _dr_time(value)
    if normalized is None:
        raise ValueError("%s must be an ISO-8601 timestamp: %r" % (label, value))
    return normalized


def _dr_event(source_ref, source_kind, locator, kind, raw_anchor, body, *,
              family=None, surface=None, platform=None, vendor=None,
              creator_namespace=None, creator_id=None, creator_handle=None,
              content_id=None, product_namespace=None, product_id=None,
              event_time=None, post_time=None, capture_time=None,
              authority="verified", limitations=(), actor=None):
    event_utc, precision, source_text = _dr_time(event_time)
    body = body.strip()
    body_hash = hashlib.sha256(body.encode()).hexdigest()
    event_id = hashlib.sha256(canonical_record_bytes({
        "source_ref": source_ref, "locator": locator, "body_sha256": body_hash
    })).hexdigest()
    limits = sorted({str(item) for item in limitations if item})
    if event_utc is None:
        limits.append("exact_event_time_unavailable")
    return {
        "event_id": event_id, "source_ref": source_ref,
        "source_kind": source_kind, "event_locator": locator,
        "event_kind": kind, "raw_anchor": raw_anchor,
        "source_family": family, "source_surface": surface,
        "platform": platform, "vendor": vendor,
        "creator_namespace": creator_namespace, "creator_native_id": creator_id,
        "creator_observed_handle": creator_handle,
        "content_native_id": content_id,
        "product_namespace": product_namespace, "product_native_id": product_id,
        "event_time_utc": event_utc, "event_time_precision": precision,
        "event_time_source_text": source_text,
        "post_time_utc": _dr_time(post_time)[0],
        "capture_time_utc": _dr_time(capture_time)[0], "body_text": body,
        "body_sha256": body_hash, "authority_status": authority,
        "limitations_json": json.dumps(limits, sort_keys=True),
        "_actor": _dr_text(actor),
    }


def _dr_silver_events(record, source_ref):
    observation = _dr_map(_dr_map(record.get("payload")).get("observation"))
    subject = _dr_map(_dr_map(observation.get("subject")).get("ref"))
    kind = _dr_text(record.get("producer_row_kind"))
    common = {
        "family": _dr_text(record.get("source_family")),
        "surface": _dr_text(record.get("source_surface")),
        "capture_time": record.get("captured_at"),
        "authority": CURRENT_SOURCE_BACKED_AUTHORITY,
        "limitations": _dr_list(record.get("non_claims")) + _dr_list(record.get("residuals")),
    }
    anchor = _dr_text(record.get("raw_anchor")) or "unknown"
    events = []
    if kind in {
        "basenotes_review_body_text", "fragrantica_review_body_text",
        "parfumo_review_body_text",
    }:
        body = _dr_text(observation.get("text_value"))
        if body:
            events.append(_dr_event(
                source_ref, "silver_record", "payload/observation/text_value",
                "review", anchor, body, vendor=kind.split("_", 1)[0],
                event_time=record.get("observed_at"), **common))
    elif kind == "instagram_audience_comment":
        content_id = _dr_text(subject.get("native_id"))
        for index, row in enumerate(_dr_list(observation.get("rows"))):
            row = _dr_map(row); comment = _dr_map(row.get("comment"))
            body = _dr_text(row.get("text_value"))
            if body:
                events.append(_dr_event(
                    source_ref, "silver_record",
                    "payload/observation/rows/%d" % index, "comment", anchor, body,
                    platform="instagram", content_id=content_id,
                    event_time=comment.get("created_at_unix"),
                    actor=comment.get("author_username"), **common))
    elif observation.get("observation_kind") == "retail_review_aggregate":
        fields = _dr_map(observation.get("source_visible_fields"))
        namespace = _dr_text(subject.get("namespace"))
        product_id = _dr_text(subject.get("native_id"))
        vendor = namespace.split(":", 1)[1] if namespace and ":" in namespace else None
        for list_name in ("displayed_reviews", "displayed_review_rows", "reviews"):
            for index, row in enumerate(_dr_list(fields.get(list_name))):
                row = _dr_map(row)
                body = next((_dr_text(row.get(key)) for key in
                    ("body","review_body","reviewBody","text","text_value")
                    if _dr_text(row.get(key))), None)
                if not body:
                    continue
                event_time = next((row.get(key) for key in
                    ("date_published","datePublished","created_at","submitted_at")
                    if row.get(key) is not None), None)
                actor = next((_dr_text(row.get(key)) for key in
                    ("author","username","nickname","user_nickname")
                    if _dr_text(row.get(key))), None)
                events.append(_dr_event(
                    source_ref, "silver_record",
                    "payload/observation/source_visible_fields/%s/%d" % (list_name,index),
                    "review", anchor, body, vendor=vendor,
                    product_namespace=namespace, product_id=product_id,
                    event_time=event_time, actor=actor, **common))
    return events


def _dr_packet_payload(loaded, suffix):
    rows = [row for row in _dr_list(loaded.manifest.get("preserved_files"))
            if isinstance(row, dict)
            and (_dr_text(row.get("relative_packet_path")) or "").endswith(suffix)]
    if len(rows) != 1 or rows[0].get("file_id") not in loaded.bodies:
        raise DataLakeRootError("packet must contain exactly one %s" % suffix)
    value = json.loads(loaded.bodies[rows[0]["file_id"]].decode())
    if not isinstance(value, dict):
        raise DataLakeRootError("packet payload is not an object: %s" % suffix)
    return value


def _dr_raw_events(loaded, source_ref):
    surface = loaded.manifest.get("source_surface")
    packet_id = loaded.manifest.get("packet_id")
    family = loaded.manifest.get("source_family")
    events = []
    if surface == "tiktok_creator_batch_comment_subtitle_admission":
        payload = _dr_packet_payload(loaded, "tiktok_batch_capture.json")
        creator = _dr_text(payload.get("creator_handle"))
        for vi, video in enumerate(_dr_list(payload.get("videos"))):
            video = _dr_map(video); content_id = _dr_text(video.get("video_id") or video.get("id"))
            comments = _dr_map(video.get("comments"))
            for ci, comment in enumerate(_dr_list(comments.get("comments"))):
                comment = _dr_map(comment); user = _dr_map(comment.get("user"))
                body = _dr_text(comment.get("text"))
                if body:
                    actor = _dr_text(user.get("uid")) or _dr_text(user.get("unique_id"))
                    events.append(_dr_event(
                        source_ref, "raw_packet", "videos/%d/comments/%d" % (vi,ci),
                        "comment", packet_id, body, family=family, surface=surface,
                        platform="tiktok", creator_namespace="tiktok",
                        creator_id=creator, creator_handle=creator, content_id=content_id,
                        event_time=comment.get("create_time"), post_time=video.get("create_time"),
                        capture_time=payload.get("capture_timestamp"), actor=actor,
                        limitations=("not_full_comment_census",)))
    elif surface == "youtube_watch_metadata_comments":
        payload = _dr_packet_payload(loaded, "youtube_watch_capture.json")
        packet = _dr_map(payload.get("packet")); channel = _dr_map(packet.get("channel"))
        metadata = _dr_map(packet.get("metadata"))
        content_id = _dr_text(payload.get("platform_video_id") or packet.get("video_id"))
        for ci, comment in enumerate(_dr_list(packet.get("comments"))):
            comment = _dr_map(comment); body = _dr_text(comment.get("text"))
            if body:
                events.append(_dr_event(
                    source_ref, "raw_packet", "packet/comments/%d" % ci,
                    "comment", packet_id, body, family=family, surface=surface,
                    platform="youtube", creator_namespace="youtube",
                    creator_id=_dr_text(channel.get("channel_id")),
                    creator_handle=_dr_text(channel.get("author")), content_id=content_id,
                    event_time=comment.get("published_time"),
                    post_time=metadata.get("publish_date"),
                    capture_time=payload.get("capture_timestamp"),
                    actor=comment.get("author"),
                    limitations=("not_full_comment_graph",)))
    return events



def _dr_insert_events(connection, events):
    columns = (
        "event_id","source_ref","source_kind","event_locator","event_kind",
        "raw_anchor","source_family","source_surface","platform","vendor",
        "creator_namespace","creator_native_id","creator_observed_handle",
        "content_native_id","product_namespace","product_native_id",
        "event_time_utc","event_time_precision","event_time_source_text",
        "post_time_utc","capture_time_utc","body_text","body_sha256",
        "authority_status","limitations_json",
    )
    connection.executemany(
        "INSERT INTO evidence_events(%s) VALUES(%s)" %
        (",".join(columns), ",".join("?" for _ in columns)),
        [tuple(event.get(column) for column in columns) for event in events],
    )


def refresh_sql_catalogue(root, source_inventory, *, full_rebuild=False, path=None):
    path = path or sql_catalogue_path(root)
    connection = _dr_connect(path)
    changed = 0; seen = set(); verification_cache = {}
    try:
        connection.execute("BEGIN IMMEDIATE")
        _dr_schema(connection, reset=full_rebuild)
        candidates = []
        for stored in source_inventory.records(subtree="derived", lanes=SQL_EVENT_LANES):
            candidates.append((stored.relative_path, "silver_record", stored.raw_anchor,
                               stored.sha256, stored))
        for entry in root.snapshot_public_availability():
            if entry.get("source_surface") in SQL_RAW_SURFACES:
                candidates.append(("raw_packet:%s" % entry["packet_id"], "raw_packet",
                    entry["packet_id"], entry["manifest_sha256"], entry))
        for source_ref, source_kind, anchor, source_sha, source in candidates:
            seen.add(source_ref)
            old = connection.execute(
                "SELECT source_sha256,extractor_profile FROM evidence_sources WHERE source_ref=?",
                (source_ref,)).fetchone()
            if old:
                if old[0] != source_sha:
                    raise DataLakeRootError("catalogued write-once source changed: %s" % source_ref)
                if old[1] != SQL_EXTRACTOR_PROFILE:
                    raise DataLakeRootError("SQL extractor changed; run --full-rebuild")
                continue
            residuals = []
            if source_kind == "raw_packet":
                events = _dr_raw_events(root.load_raw_packet(anchor), source_ref)
            else:
                try:
                    record = json.loads(source.body.decode())
                    authority = classify_silver_vault_record_sources(
                        root, record, record_path=root.path / source.relative_path,
                        verification_cache=verification_cache)
                except (OSError, TypeError, ValueError, DataLakeRootError) as exc:
                    events = []; residuals = ["silver_source_error:%s" % type(exc).__name__]
                else:
                    if authority.status == CURRENT_SOURCE_BACKED_AUTHORITY:
                        events = _dr_silver_events(record, source_ref)
                    else:
                        events = []; residuals = [
                            "silver_authority:%s:%s" % (authority.status,authority.reason_code)]
            connection.execute("INSERT INTO evidence_sources VALUES(?,?,?,?,?,?,?)",
                (source_ref,source_kind,anchor,source_sha,SQL_EXTRACTOR_PROFILE,
                 len(events),json.dumps(residuals,sort_keys=True)))
            _dr_insert_events(connection, events); changed += 1
        missing = sorted({row[0] for row in connection.execute(
            "SELECT source_ref FROM evidence_sources")} - seen)
        if missing:
            raise DataLakeRootError("catalogued evidence source disappeared: %s" % missing[:3])
        source_rows = [dict(row) for row in connection.execute(
            "SELECT source_ref,source_sha256,extractor_profile FROM evidence_sources ORDER BY source_ref")]
        source_digest = hashlib.sha256(canonical_record_bytes(source_rows)).hexdigest()
        event_count = connection.execute("SELECT count(*) FROM evidence_events").fetchone()[0]
        prior_digest = connection.execute(
            "SELECT value FROM evidence_metadata WHERE key='logical_digest'").fetchone()
        if changed or full_rebuild or not prior_digest:
            logical_rows = [dict(row) for row in connection.execute(
                "SELECT * FROM evidence_events ORDER BY event_id")]
            for row in logical_rows: row.pop("row_id", None)
            logical_digest = hashlib.sha256(canonical_record_bytes(logical_rows)).hexdigest()
        else:
            logical_digest = prior_digest[0]
        refreshed = datetime.now(timezone.utc).isoformat()
        connection.executemany(
            "INSERT INTO evidence_metadata(key,value) VALUES(?,?) "
            "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (("extractor_profile",SQL_EXTRACTOR_PROFILE),
             ("source_inventory_sha256",source_digest),
             ("logical_digest",logical_digest),
             ("last_successful_refresh_at",refreshed)))
        connection.execute("COMMIT")
        check = connection.execute("PRAGMA quick_check").fetchone()[0]
        if check != "ok": raise DataLakeRootError("SQL quick_check failed: %s" % check)
        return {"status":"rebuilt" if changed or full_rebuild else "current",
            "path":str(path),"changed_sources":changed,
            "source_count":len(source_rows),"event_count":event_count,
            "source_inventory_sha256":source_digest,"logical_digest":logical_digest,
            "last_successful_refresh_at":refreshed,"quick_check":check}
    except Exception:
        if connection.in_transaction: connection.execute("ROLLBACK")
        raise
    finally:
        connection.close()


def _dr_catalogue_status(connection, path):
    meta = {row[0]:row[1] for row in connection.execute(
        "SELECT key,value FROM evidence_metadata")}
    check = connection.execute("PRAGMA quick_check").fetchone()[0]
    return {"status":"ok" if check=="ok" else "failed","path":str(path),
        "schema_version":int(meta.get("schema_version","0")),
        "extractor_profile":meta.get("extractor_profile"),
        "source_inventory_sha256":meta.get("source_inventory_sha256"),
        "logical_digest":meta.get("logical_digest"),
        "last_successful_refresh_at":meta.get("last_successful_refresh_at"),
        "source_count":connection.execute("SELECT count(*) FROM evidence_sources").fetchone()[0],
        "event_count":connection.execute("SELECT count(*) FROM evidence_events").fetchone()[0],
        "quick_check":check}


def sql_catalogue_status(root, *, path=None):
    path = path or sql_catalogue_path(root)
    if not path.is_file(): raise DataLakeRootError("SQL catalogue has not been built: %s" % path)
    connection = _dr_connect(path, read_only=True)
    try:
        connection.execute("BEGIN")
        return _dr_catalogue_status(connection,path)
    finally: connection.close()


def query_sql_catalogue(root, *, body_query=None, platform=None, vendor=None,
                        surface=None, creator_id=None, content_id=None, product_id=None,
                        from_utc=None, to_utc=None, limit=1000):
    if limit < 1 or limit > 10000: raise ValueError("limit must be 1..10000")
    path = sql_catalogue_path(root)
    connection = _dr_connect(path,read_only=True)
    try:
        connection.execute("BEGIN")
        join = ""; clauses = []; values = []
        normalized_from = _dr_window_bound(from_utc,"from_utc") if from_utc else None
        normalized_to = _dr_window_bound(to_utc,"to_utc") if to_utc else None
        if body_query:
            join = " JOIN evidence_fts ON evidence_fts.rowid=e.row_id"
            clauses.append("evidence_fts MATCH ?"); values.append(body_query)
        for column,value in (("platform",platform),("vendor",vendor),
            ("source_surface",surface),("creator_native_id",creator_id),
            ("content_native_id",content_id),("product_native_id",product_id)):
            if value is not None: clauses.append("e.%s=?" % column); values.append(value)
        if normalized_from:
            clauses.append("coalesce(e.event_time_utc,e.capture_time_utc)>=?")
            values.append(normalized_from)
        if normalized_to:
            clauses.append("coalesce(e.event_time_utc,e.capture_time_utc)<=?")
            values.append(normalized_to)
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        fetched = [dict(row) for row in connection.execute(
            "SELECT e.* FROM evidence_events e" + join + where +
            " ORDER BY coalesce(e.event_time_utc,e.capture_time_utc),e.event_id LIMIT ?",
            (*values,limit+1))]
        truncated = len(fetched) > limit
        rows = fetched[:limit]
        for row in rows:
            row.pop("row_id",None); row["limitations"]=json.loads(row.pop("limitations_json"))
        normalized_query = {"body_query":body_query if body_query else None,
            "platform":platform,"vendor":vendor,"surface":surface,
            "creator_id":creator_id,"content_id":content_id,"product_id":product_id,
            "from_utc":normalized_from,"to_utc":normalized_to,"limit":limit}
        return {"query_profile":"evidence_search",
            "query_contract_version":SQL_QUERY_CONTRACT_VERSION,
            "normalized_query":normalized_query,
            "catalogue":_dr_catalogue_status(connection,path),
            "row_count":len(rows),"result_set_complete":not truncated,
            "truncated":truncated,"rows":rows,
            "non_claims":["captured evidence only","not a complete platform census",
             "not cross-platform identity","not a paid/bot/fake/astroturf conclusion"]}
    finally: connection.close()


def _dr_catalogued_sources(root, source_refs):
    refs = sorted(set(source_refs))
    if not refs: return {}
    connection = _dr_connect(sql_catalogue_path(root),read_only=True)
    try:
        connection.execute("BEGIN")
        sources = {}
        for start in range(0,len(refs),SQL_SOURCE_LOOKUP_CHUNK):
            chunk = refs[start:start+SQL_SOURCE_LOOKUP_CHUNK]
            placeholders = ",".join("?" for _ in chunk)
            for row in connection.execute(
                    "SELECT * FROM evidence_sources WHERE source_ref IN (%s)" % placeholders,
                    chunk):
                sources[row["source_ref"]] = dict(row)
    finally: connection.close()
    missing = sorted(set(refs)-set(sources))
    if missing:
        raise DataLakeRootError("query citation source absent from catalogue: %s" % missing[:3])
    return sources


def _dr_verified_query_sources(root, rows):
    refs = sorted({row["source_ref"] for row in rows})
    sources = _dr_catalogued_sources(root,refs)
    verified = {}
    for ref in refs:
        source = sources[ref]
        if source["source_kind"] == "raw_packet":
            loaded = root.load_raw_packet(source["raw_anchor"])
            manifest_path = loaded.container / "manifest.json"
            try:
                manifest_bytes = manifest_path.read_bytes()
            except OSError as exc:
                raise DataLakeRootError(
                    "unreadable query citation manifest: %s: %s" % (ref,exc)) from exc
            if hashlib.sha256(manifest_bytes).hexdigest() != source["source_sha256"]:
                raise DataLakeRootError("query citation manifest hash mismatch: %s" % ref)
            payload = loaded
        elif source["source_kind"] == "silver_record":
            path = root.path / ref
            try:
                payload = path.read_bytes()
            except OSError as exc:
                raise DataLakeRootError(
                    "unreadable query citation Silver record: %s: %s" % (ref,exc)) from exc
            if hashlib.sha256(payload).hexdigest() != source["source_sha256"]:
                raise DataLakeRootError("query citation Silver hash mismatch: %s" % ref)
        else:
            raise DataLakeRootError(
                "unsupported query citation source kind: %s: %s" %
                (ref,source["source_kind"]))
        verified[ref] = (source,payload)
    return verified


def verify_sql_query_sources(root, report):
    if report.get("query_profile") != "evidence_search":
        raise ValueError("source verification requires an evidence_search report")
    verified = _dr_verified_query_sources(root,report["rows"])
    return {"status":"passed","verified_source_count":len(verified)}


def query_exact_actor_context(root, *, platform, actor, from_utc, to_utc,
                              creator_id=None, content_id=None):
    if platform not in {"instagram","tiktok","youtube"}:
        raise ValueError("one admitted platform namespace is required")
    start = datetime.fromisoformat(from_utc.replace("Z","+00:00"))
    end = datetime.fromisoformat(to_utc.replace("Z","+00:00"))
    if start.tzinfo is None or end.tzinfo is None:
        raise ValueError("actor window timestamps must include UTC offsets")
    if end <= start or end-start > timedelta(days=90):
        raise ValueError("actor window must be greater than zero and at most 90 days")
    if not actor.strip():
        raise ValueError("actor identifier must not be empty")
    from_utc = start.astimezone(timezone.utc).isoformat()
    to_utc = end.astimezone(timezone.utc).isoformat()
    report = query_sql_catalogue(root,platform=platform,creator_id=creator_id,
        content_id=content_id,from_utc=from_utc,to_utc=to_utc,
        limit=SQL_ACTOR_CANDIDATE_LIMIT)
    if report["truncated"]:
        raise ValueError(
            "actor candidate set exceeds the bounded result limit; narrow the "
            "time window or add a creator/content anchor")
    verified = _dr_verified_query_sources(root,report["rows"])
    hydrated = {}
    for ref,(source,payload) in verified.items():
        if source["source_kind"] == "raw_packet":
            events = _dr_raw_events(payload,ref)
        else:
            events = _dr_silver_events(json.loads(payload.decode()),ref)
        hydrated.update({event["event_id"]:event for event in events})
    needle = actor.strip().lstrip("@").casefold(); rows = []
    for row in report["rows"]:
        event = hydrated.get(row["event_id"])
        observed = _dr_text(event.get("_actor")) if event else None
        if observed and observed.strip().lstrip("@").casefold() == needle:
            row["actor_public_identifier"] = observed; rows.append(row)
    return {"query_profile":"exact_actor_context",
        "query_contract_version":report["query_contract_version"],
        "normalized_query":report["normalized_query"],"catalogue":report["catalogue"],
        "platform_namespace":platform,"identifier_scope":actor,
        "time_window":{"from_utc":from_utc,"to_utc":to_utc},
        "candidate_event_count":report["row_count"],"row_count":len(rows),
        "result_set_complete":True,"truncated":False,"rows":rows,
        "source_verification":{"status":"passed",
                               "verified_source_count":len(verified)},
        "non_claims":["no durable actor index","no cross-platform identity merge",
                      "not a paid/bot/fake/astroturf conclusion"]}


def _dr_decision_question_id(value):
    text = _dr_text(value)
    if text is None or len(text) > SQL_DECISION_QUESTION_ID_MAX_LENGTH:
        raise ValueError(
            "decision_question_id must be nonblank and at most %d characters" %
            SQL_DECISION_QUESTION_ID_MAX_LENGTH)
    return text


def _dr_query_citations(report):
    return [{"event_id":row["event_id"],"source_ref":row["source_ref"],
             "body_sha256":row["body_sha256"]} for row in report["rows"]]


def _dr_write_query_audit(report, *, decision_question_id, caller, audit_root,
                          profile_fields=None):
    if report.get("result_set_complete") is not True or report.get("truncated"):
        raise ValueError("decision query result set is truncated; narrow the query")
    verification = report.get("source_verification")
    if not isinstance(verification,dict) or verification.get("status") != "passed":
        raise ValueError("decision query sources must be verified before audit")
    catalogue = report.get("catalogue")
    if not isinstance(catalogue,dict):
        raise ValueError("decision query catalogue snapshot is missing")
    citations = _dr_query_citations(report)
    payload = {"audit_schema_version":SQL_QUERY_AUDIT_SCHEMA_VERSION,
        "created_at":datetime.now(timezone.utc).isoformat(),
        "caller":caller or os.environ.get("USERNAME") or "unknown",
        "decision_question_id":decision_question_id,
        "profile":report["query_profile"],
        "query_contract_version":report["query_contract_version"],
        "normalized_query":report["normalized_query"],
        "catalogue_snapshot":{
            key:catalogue.get(key) for key in (
                "schema_version","extractor_profile","source_inventory_sha256",
                "logical_digest","last_successful_refresh_at")},
        "row_count":report["row_count"],"result_set_complete":True,
        "source_verification":verification,"citations":citations,
        "citation_manifest_sha256":hashlib.sha256(
            canonical_record_bytes(citations)).hexdigest(),
        "non_claims":report["non_claims"],"cache_hit":False,
        "elevated_volume":report["row_count"]>=1000}
    if profile_fields: payload.update(profile_fields)
    root = Path(audit_root or os.environ.get("LOCALAPPDATA") or Path.home()) / "Forseti" / "audit" / "derived-retrieval"
    root.mkdir(parents=True,exist_ok=True)
    cutoff = datetime.now(timezone.utc).timestamp() - 365*24*60*60
    for path in root.glob("*.json"):
        if path.stat().st_mtime < cutoff: path.unlink()
    target = root / ("%s.json" % uuid.uuid4().hex)
    _atomic_create(target,canonical_record_bytes(payload))
    return str(target)


def write_evidence_query_audit(report, *, decision_question_id, caller=None,
                               audit_root=None):
    if report.get("query_profile") != "evidence_search":
        raise ValueError("ordinary evidence audit requires an evidence_search report")
    return _dr_write_query_audit(
        report,decision_question_id=_dr_decision_question_id(decision_question_id),
        caller=caller,audit_root=audit_root)


def write_actor_query_audit(report, *, decision_question_id, caller=None, audit_root=None):
    if decision_question_id not in SQL_DECISION_QUESTIONS:
        raise ValueError("unregistered actor decision question")
    if report.get("query_profile") != "exact_actor_context":
        raise ValueError("actor audit requires an exact_actor_context report")
    return _dr_write_query_audit(
        report,decision_question_id=decision_question_id,caller=caller,
        audit_root=audit_root,profile_fields={
            "identifier_scope":report["identifier_scope"],
            "platform_namespace":report["platform_namespace"],
            "time_window":report["time_window"],
            "candidate_event_count":report["candidate_event_count"]})


def prove_sql_catalogue_rebuildability(root):
    import tempfile
    live = sql_catalogue_status(root)
    with tempfile.TemporaryDirectory(prefix="forseti-sql-proof-") as temp:
        with IncrementalSourceInventory(root,persistent=False) as inventory:
            inventory.refresh(derived_lanes=_incremental_source_lanes(),include_acknowledgements=True)
            cold = refresh_sql_catalogue(root,inventory,full_rebuild=True,
                                         path=Path(temp)/"catalogue.sqlite3")
    matched = (live["logical_digest"]==cold["logical_digest"] and
               live["source_inventory_sha256"]==cold["source_inventory_sha256"])
    return {"status":"proven" if matched else "failed",
            "live_logical_digest":live["logical_digest"],
            "cold_logical_digest":cold["logical_digest"],
            "source_inventory_matches":live["source_inventory_sha256"]==cold["source_inventory_sha256"]}


__all__ = [
    "BUILT_VIEWS",
    "BY_CREATOR_VIEW_SCHEMA_VERSION",
    "CURRENT_POINTER_FILENAME",
    "GENERATIONS_DIRNAME",
    "MANIFEST_SCHEMA_VERSION",
    "MENTIONS_LANE",
    "SILVER_VAULT_CORE_PARTS",
    "VIEW_SCHEMA_VERSION",
    "build_by_creator_view",
    "build_by_mention_view",
    "build_undone_view",
    "audit_derived_retrieval_source_integrity",
    "current_generation_root",
    "generation_stamp",
    "load_derived_retrieval_view",
    "prove_incremental_rebuild_equality",
    "prove_derived_retrieval_rebuildability",
    "rebuild_derived_retrieval",
    "prove_sql_catalogue_rebuildability",
    "query_exact_actor_context",
    "query_sql_catalogue",
    "refresh_sql_catalogue",
    "sql_catalogue_status",
    "verify_sql_query_sources",
    "write_actor_query_audit",
    "write_evidence_query_audit",
]
