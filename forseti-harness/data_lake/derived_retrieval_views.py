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
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
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
]
