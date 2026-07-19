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
from data_lake.lane_registry import LANE_ROLES, LaneRole
from data_lake.root import _atomic_replace
from data_lake.product_mention_selection import (
    MENTIONS_LANE,
    normalize_product_mention_policy,
    select_product_mention_records,
)
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
MANIFEST_SCHEMA_VERSION = 1
SILVER_VAULT_ROOT_PARTS = ("indexes", "derived_retrieval", "silver_vault")
SILVER_VAULT_CORE_PARTS = (*SILVER_VAULT_ROOT_PARTS, "core")
SILVER_VAULT_CREATOR_PARTS = (*SILVER_VAULT_ROOT_PARTS, "creator_vault")
BUILT_VIEWS = ("by_creator", "by_mention", "undone")
CREATOR_VAULT_ACCOUNT_ENVELOPE_SCHEMA_VERSION = 1
CREATOR_VAULT_ACCOUNT_SELECTION_POLICY_VERSION = "creator_vault_account_latest_profile_metric_v0"
_TIKTOK_PROFILE_METRIC_PRODUCER_ROW_KIND = "tiktok_creator_profile_metric"
_PLATFORM_ACCOUNT_ID_ALIAS_FIELDS = (
    "platform_account_id",
    "forseti_platform_account_id",
    "orca_platform_account_id",
)
_SAFE_READ_MODEL_KEY = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")

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
        (lane for lane, role in LANE_ROLES.items() if role is LaneRole.SILVER_ENVELOPE),
        key=lambda lane: (lane != OBSERVATION_LANE, lane),
    )
)
_CREATOR_METRIC_LANES = frozenset({OBSERVATION_LANE, ROLLUP_LANE})


def _classified_silver_sweep(
    root,
    *,
    cache_session: ClassificationCacheSession | None = None,
) -> dict[str, Any]:
    """Classify each active Silver record once for every generated read model."""
    anchor_lane_status: dict[str, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
    accounts: dict[tuple[str, str, str], dict[str, Any]] = {}
    source_refs: list[str] = []
    residuals: list[dict[str, Any]] = []
    authority_by_ref: dict[str, Any] = {}
    records_by_ref: dict[str, dict[str, Any]] = {}
    verification_cache: dict[str, Any] = {}
    derived = root.path / "derived"
    lineage = None
    tombstoned_packet_ids = root.tombstoned_packet_ids()
    for lane in _ACTIVE_SILVER_ENVELOPE_LANES:
        for path in sorted(derived.glob(f"*/*/{lane}/*")):
            if not path.is_file():
                continue
            anchor = path.parents[1].name
            if anchor in tombstoned_packet_ids:
                continue
            ref_key = f"{anchor}/{lane}/{path.name}"
            try:
                record = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                residuals.append({"status": "unreadable", "raw_anchor": anchor, "lane": lane, "record_id": path.name})
                continue
            if cache_session is not None and lane == OBSERVATION_LANE and isinstance(record, dict):
                cache_session.register_creator_metric_observation(record, record_path=path)
            if not isinstance(record, dict) or record.get("schema_version") != SILVER_VAULT_RECORD_SCHEMA_VERSION:
                residuals.append({"status": "non_envelope_schema_audit_only", "raw_anchor": anchor, "lane": lane, "record_id": path.name})
                continue
            source_refs.append(ref_key)
            records_by_ref[ref_key] = record
            cache_key = None
            authority = None
            if cache_session is not None:
                cache_key, authority = cache_session.lookup(record, record_path=path)
            if authority is None:
                if record.get("lane_namespace") in _CREATOR_METRIC_LANES and lineage is None:
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
                residuals.append({**problem, "raw_anchor": anchor, "lane": lane, "record_id": path.name})
            for namespace, identity_kind, native_id, aliases in account_keys:
                entry = accounts.setdefault(
                    (namespace, identity_kind, native_id),
                    {"aliases": {}, "alias_values": defaultdict(set), "refs_by_anchor": defaultdict(list)},
                )
                for alias_key, alias_value in aliases.items():
                    entry["aliases"].setdefault(alias_key, alias_value)
                    entry["alias_values"][alias_key].add(str(alias_value))
                entry["refs_by_anchor"][anchor].append(ref)
    for (namespace, identity_kind, native_id), entry in sorted(accounts.items()):
        for alias_key, alias_values in sorted(entry["alias_values"].items()):
            if len(alias_values) > 1:
                residuals.append({
                    "status": "account_alias_conflict",
                    "namespace": namespace,
                    "identity_kind": identity_kind,
                    "native_id": native_id,
                    "alias_key": alias_key,
                    "alias_values": sorted(alias_values),
                })
        account_ids = {
            str(entry["aliases"][field])
            for field in _PLATFORM_ACCOUNT_ID_ALIAS_FIELDS
            if entry["aliases"].get(field)
        }
        if len(account_ids) > 1:
            residuals.append({
                "status": "platform_account_id_alias_conflict",
                "namespace": namespace,
                "identity_kind": identity_kind,
                "native_id": native_id,
                "account_ids": sorted(account_ids),
            })
    return {
        "anchor_lane_status": anchor_lane_status,
        "accounts": accounts,
        "source_refs": sorted(source_refs),
        "authority_by_ref": authority_by_ref,
        "records_by_ref": records_by_ref,
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
            field: ref[field] for field in _PLATFORM_ACCOUNT_ID_ALIAS_FIELDS if ref.get(field)
        }
        _file_account(str(ref.get("native_id") or "").strip(), identity_kind, aliases)
    elif kind == "public_content_object":
        if ref.get("published_by_account_native_id") is not None:
            identity_kind = (
                str(ref.get("published_by_account_native_id_kind") or "").strip()
                or UNSPECIFIED_IDENTITY_KIND
            )
            aliases = {
                field: ref[field] for field in _PLATFORM_ACCOUNT_ID_ALIAS_FIELDS if ref.get(field)
            }
            _file_account(
                str(ref.get("published_by_account_native_id") or "").strip(),
                identity_kind,
                aliases,
            )
        # A content object without a publisher assertion is not account-describing.
    elif any(
        ref.get(field)
        for field in (
            "native_id",
            "published_by_account_native_id",
            *_PLATFORM_ACCOUNT_ID_ALIAS_FIELDS,
        )
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


def _platform_account_id(entry: dict[str, Any]) -> str | None:
    values = {
        str(entry["aliases"][field])
        for field in _PLATFORM_ACCOUNT_ID_ALIAS_FIELDS
        if entry.get("aliases", {}).get(field)
    }
    return next(iter(values)) if len(values) == 1 else None


def _observed_time(value: Any) -> datetime:
    text = str(value or "").strip()
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        raise ValueError("Creator Vault metric observed_at must be timezone-aware")
    return parsed.astimezone(timezone.utc)


def _candidate_from_record(ref_key: str, record: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    payload = record.get("payload")
    observation = payload.get("observation") if isinstance(payload, dict) else None
    posture = observation.get("metric_posture") if isinstance(observation, dict) else None
    metric_name = str(observation.get("metric_name") or "").strip() if isinstance(observation, dict) else ""
    if not metric_name or not isinstance(posture, dict):
        raise ValueError(f"Creator Vault metric record {ref_key} has invalid observation shape")
    observed_at = str(record.get("observed_at") or "").strip()
    source = {
        "record_id": record.get("record_id"),
        "packet_id": record.get("raw_anchor"),
        "lane": record.get("lane_namespace"),
        "content_hash": record.get("content_hash"),
        "observed_at": observed_at,
    }
    candidate = {
        **source,
        "metric_value_or_none": observation.get("metric_value"),
        "metric_posture": str(posture.get("kind") or "").strip(),
        "reason_code_or_none": posture.get("reason_code"),
        "reason_detail_or_none": posture.get("reason_detail"),
        "_ref_key": ref_key,
        "_timestamp": _observed_time(observed_at),
        "_record": record,
    }
    candidate["_signature"] = json.dumps(
        {
            "metric_value_or_none": candidate["metric_value_or_none"],
            "metric_posture": candidate["metric_posture"],
            "reason_code_or_none": candidate["reason_code_or_none"],
            "reason_detail_or_none": candidate["reason_detail_or_none"],
        }, sort_keys=True, separators=(",", ":")
    )
    return metric_name, candidate


def _public_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in candidate.items() if not key.startswith("_")}


def _select_metric_state(metric_name: str, candidates: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    ordered = sorted(candidates, key=lambda row: (row["_timestamp"], str(row["record_id"])))
    groups: dict[datetime, list[dict[str, Any]]] = defaultdict(list)
    for candidate in ordered:
        groups[candidate["_timestamp"]].append(candidate)
    latest_time = max(groups)
    latest_group = groups[latest_time]
    latest_conflicted = len({row["_signature"] for row in latest_group}) > 1
    conflicts = [
        {
            "metric_name": metric_name,
            "observed_at": max(row["observed_at"] for row in group),
            "candidates": [_public_candidate(row) for row in group],
        }
        for _time, group in sorted(groups.items())
        if len({row["_signature"] for row in group}) > 1
    ]
    latest_attempt = None if latest_conflicted else _public_candidate(
        max(latest_group, key=lambda row: str(row["record_id"]))
    )
    last_observed = None
    for observed_at in sorted(groups, reverse=True):
        if latest_conflicted and observed_at == latest_time:
            continue
        observed = [row for row in groups[observed_at] if row["metric_posture"] == "observed"]
        values = {json.dumps(row["metric_value_or_none"], sort_keys=True) for row in observed}
        if observed and len(values) == 1:
            last_observed = _public_candidate(max(observed, key=lambda row: str(row["record_id"])))
            break
    if latest_conflicted:
        display_state = "conflicted_latest_attempt"
    elif latest_attempt["metric_posture"] == "observed":
        display_state = "current_observed"
        last_observed = latest_attempt
    elif last_observed is not None:
        display_state = "last_observed_retained_after_unavailable_attempt"
    else:
        display_state = "unavailable_no_observed_value"
    state = {"display_state": display_state, "last_observed": last_observed, "latest_attempt": latest_attempt}
    selected_ids = {
        row["record_id"] for row in (last_observed, latest_attempt) if isinstance(row, dict)
    }
    return state, conflicts, [row for row in ordered if row["record_id"] in selected_ids]


def _dedupe_json_rows(rows: list[Any]) -> list[Any]:
    by_key = {
        json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False): row
        for row in rows
    }
    return [by_key[key] for key in sorted(by_key)]


def build_creator_vault_account_files(sweep: dict[str, Any], stamp: dict[str, str]) -> dict[str, bytes]:
    """Generate TikTok account envelopes from the same classified Silver sweep."""
    grouped: dict[tuple[str, str], dict[str, Any]] = {}
    for (namespace, _identity_kind, native_id), entry in sorted(sweep["accounts"].items()):
        if namespace != "tiktok":
            continue
        account_id = _platform_account_id(entry)
        if account_id is None or _SAFE_READ_MODEL_KEY.fullmatch(account_id) is None:
            continue
        account = grouped.setdefault((namespace, account_id), {"native_ids": set(), "candidates": defaultdict(list)})
        account["native_ids"].add(native_id)
        for anchor, refs in entry["refs_by_anchor"].items():
            for ref in refs:
                if ref.get("lane") != OBSERVATION_LANE or ref.get("authority_status") != CURRENT_SOURCE_BACKED_AUTHORITY:
                    continue
                ref_key = f"{anchor}/{ref['lane']}/{ref['record_id']}"
                record = sweep["records_by_ref"].get(ref_key)
                if not isinstance(record, dict) or record.get("producer_row_kind") != _TIKTOK_PROFILE_METRIC_PRODUCER_ROW_KIND or record.get("payload_kind") != "MetricObservation":
                    continue
                metric_name, candidate = _candidate_from_record(ref_key, record)
                account["candidates"][metric_name].append(candidate)

    files: dict[str, bytes] = {}
    for (platform, account_id), account in sorted(grouped.items()):
        metrics: dict[str, Any] = {}
        postures: dict[str, str] = {}
        windows: dict[str, dict[str, str]] = {}
        conflicts: list[dict[str, Any]] = []
        selected: list[dict[str, Any]] = []
        all_candidates: list[dict[str, Any]] = []
        for metric_name, candidates in sorted(account["candidates"].items()):
            state, metric_conflicts, metric_selected = _select_metric_state(metric_name, candidates)
            metrics[metric_name] = state
            postures[metric_name] = "conflicted" if state["display_state"] == "conflicted_latest_attempt" else state["latest_attempt"]["metric_posture"]
            windows[metric_name] = {
                "start": min(row["observed_at"] for row in candidates),
                "end": max(row["observed_at"] for row in candidates),
            }
            conflicts.extend(metric_conflicts)
            selected.extend(metric_selected)
            all_candidates.extend(candidates)
        if not metrics:
            continue
        selected_records = [row["_record"] for row in selected]
        source_record_ids = sorted({row["_ref_key"] for row in all_candidates})
        source_high_watermark = hashlib.sha256(canonical_record_bytes(source_record_ids)).hexdigest()
        manifest_id = f"creator_vault_account:{platform}:{account_id}:{stamp['generation_id']}"
        envelope = {
            "envelope_type": "creator_vault_account_v0",
            "envelope_schema_version": CREATOR_VAULT_ACCOUNT_ENVELOPE_SCHEMA_VERSION,
            "platform": platform,
            "account_key": {"platform_account_id": account_id, "observed_native_ids": sorted(account["native_ids"])},
            "latest_metric_snapshot": metrics,
            "coverage_summary": {
                "metric_count": len(metrics),
                "source_record_count": len(source_record_ids),
                "first_attempt_at": min(row["observed_at"] for row in all_candidates),
                "latest_attempt_at": max(row["observed_at"] for row in all_candidates),
            },
            "metric_postures": postures,
            "coverage_windows": windows,
            "source_conflicts": conflicts,
            "raw_refs": _dedupe_json_rows([raw_ref for record in selected_records for raw_ref in record.get("raw_refs", [])]),
            "derived_refs": _dedupe_json_rows([
                {"record_id": row["record_id"], "packet_id": row["packet_id"], "lane": row["lane"], "content_hash": row["content_hash"]}
                for row in selected
            ]),
            "query_table_pointers": ["indexes/derived_retrieval/silver_vault/core/query_tables/by_creator.json"],
            "read_model_manifest_id": manifest_id,
            "selection_policy_version": CREATOR_VAULT_ACCOUNT_SELECTION_POLICY_VERSION,
            "judgment_boundary": "exact public profile metric observations only; no rollup, growth, audience, credibility, or commercial judgment",
            "per_platform_identity_only": True,
            "cross_platform_identity_assumed": False,
        }
        envelope_bytes = canonical_record_bytes(envelope)
        manifest = {
            "manifest_schema_version": MANIFEST_SCHEMA_VERSION,
            "read_model_manifest_id": manifest_id,
            "envelope_type": envelope["envelope_type"],
            "envelope_schema_version": envelope["envelope_schema_version"],
            "platform": platform,
            "platform_account_id": account_id,
            "generation_id": stamp["generation_id"],
            "generated_at": stamp["generated_at"],
            "source_record_ids": source_record_ids,
            "source_high_watermark": source_high_watermark,
            "selection_policy_versions": {
                "account_envelope": CREATOR_VAULT_ACCOUNT_SELECTION_POLICY_VERSION,
                "silver_authority_gate": CURRENT_SOURCE_BACKED_AUTHORITY,
                "source_lane": OBSERVATION_LANE,
            },
            "envelope_sha256": hashlib.sha256(envelope_bytes).hexdigest(),
            "stale_if": "a committed creator-profile MetricObservation or raw-packet tombstone changes the account selection after this source_high_watermark",
        }
        files[f"accounts/{platform}/{account_id}/envelope.json"] = envelope_bytes
        files[f"manifests/accounts/{platform}/{account_id}.json"] = canonical_record_bytes(manifest)
    return files

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


def _native_product_pages(root, sweep: dict) -> tuple[dict, list[str], list[dict]]:
    """Native product-page identity rows from the registered projection
    sources (view-only mechanical records used as identity ROUTING, never
    authority), each joined to its anchor's classified Silver record counts."""
    pages: dict[str, dict[str, dict[tuple[str, str, str], dict]]] = {}
    identity_bindings: dict[tuple[str, str, str], tuple[str, str, dict]] = {}
    source_refs: set[str] = set()
    residuals: list[dict[str, Any]] = []
    derived = root.path / "derived"
    for source_lane, source_row_kind, extract_identity in NATIVE_PRODUCT_PAGE_SOURCES:
        for path in sorted(derived.glob(f"*/*/{source_lane}/*")):
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
                if not isinstance(row, dict) or row.get("row_kind") != source_row_kind:
                    continue
                source_ref = f"{anchor}/{source_lane}/{path.name}"
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
                            "record_id": path.name,
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
                            "record_id": path.name,
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
) -> tuple[dict, list[str]]:
    """The exact-policy by_mention view plus every non-evidence residual."""
    sweep = sweep or _classified_silver_sweep(root)
    selection = select_product_mention_records(
        root,
        policy=product_mention_policy,
        preclassified_authority=sweep["authority_by_ref"],
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
        root, sweep
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
    cache_session: ClassificationCacheSession | None = None,
    sweep: dict[str, Any] | None = None,
) -> dict[str, bytes]:
    """Generate the core view files from one optional shared Silver sweep."""
    normalized_policy = normalize_product_mention_policy(product_mention_policy) if "by_mention" in views else None
    if sweep is None and any(name in views for name in ("by_creator", "by_mention")):
        sweep = _classified_silver_sweep(root, cache_session=cache_session)
    files: dict[str, bytes] = {}
    for view_name in views:
        if view_name == "by_creator":
            view, source_refs = build_by_creator_view(root, sweep=sweep)
        elif view_name == "by_mention":
            view, source_refs = build_by_mention_view(root, product_mention_policy=normalized_policy, sweep=sweep)
        else:
            view, source_refs = build_undone_view(root)
        view_bytes = canonical_record_bytes(view)
        manifest_bytes = canonical_record_bytes(_manifest(view_name, view_bytes, source_refs, stamp, normalized_policy))
        files[f"query_tables/{view_name}.json"] = view_bytes
        files[f"manifests/{view_name}.json"] = manifest_bytes
    return files


def _generate_all(
    root,
    stamp: dict[str, str],
    *,
    product_mention_policy: dict[str, str],
    cache_session: ClassificationCacheSession | None = None,
) -> dict[str, bytes]:
    sweep = _classified_silver_sweep(root, cache_session=cache_session)
    core = _generate(
        root,
        stamp,
        product_mention_policy=product_mention_policy,
        cache_session=cache_session,
        sweep=sweep,
    )
    creator_vault = build_creator_vault_account_files(sweep, stamp)
    return {
        **{f"core/{path}": data for path, data in core.items()},
        **{f"creator_vault/{path}": data for path, data in creator_vault.items()},
    }


def _silver_vault_root(root) -> Path:
    return root._within(*SILVER_VAULT_ROOT_PARTS)


def _silver_vault_core_root(root) -> Path:
    return root._within(*SILVER_VAULT_CORE_PARTS)


def _owned_generated_paths(root) -> set[Path]:
    core_root = _silver_vault_core_root(root)
    owned = {
        target
        for view_name in BUILT_VIEWS
        for target in (
            core_root / "query_tables" / f"{view_name}.json",
            core_root / "manifests" / f"{view_name}.json",
        )
        if target.is_file()
    }
    creator_root = root._within(*SILVER_VAULT_CREATOR_PARTS)
    for pattern in ("accounts/tiktok/*/envelope.json", "manifests/accounts/tiktok/*.json"):
        owned.update(path for path in creator_root.glob(pattern) if path.is_file())
    return owned


def _publish_generated_files(root, files: dict[str, bytes]) -> None:
    """Atomically replace owned files and roll back the package on failure."""
    root._reverify()
    target_root = _silver_vault_root(root)
    desired = {target_root / relpath: data for relpath, data in files.items()}
    existing = _owned_generated_paths(root)
    affected = set(desired) | existing
    previous = {path: path.read_bytes() if path.is_file() else None for path in affected}
    changed: list[Path] = []
    try:
        for target, data in sorted(desired.items(), key=lambda item: str(item[0])):
            _atomic_replace(target, data)
            changed.append(target)
        for target in sorted(existing - set(desired), key=str):
            target.unlink()
            changed.append(target)
    except Exception as publish_error:
        rollback_errors: list[str] = []
        for target in reversed(changed):
            try:
                old_bytes = previous[target]
                if old_bytes is None:
                    target.unlink(missing_ok=True)
                else:
                    _atomic_replace(target, old_bytes)
            except Exception as rollback_error:  # pragma: no cover - storage-loss boundary
                rollback_errors.append(f"{target}: {rollback_error}")
        if rollback_errors:
            raise RuntimeError(
                "derived-retrieval publication failed and rollback was incomplete: "
                + "; ".join(rollback_errors)
            ) from publish_error
        raise


def rebuild_derived_retrieval(
    root,
    *,
    product_mention_policy: dict[str, str],
    stamp: dict | None = None,
    full_rebuild: bool = False,
) -> dict:
    """Replace core views and daily Creator Vault account summaries."""
    root._reverify()
    stamp = stamp or generation_stamp()
    cache_session = ClassificationCacheSession(root, use_existing=not full_rebuild)
    files = _generate_all(
        root,
        stamp,
        product_mention_policy=product_mention_policy,
        cache_session=cache_session,
    )
    cache_session.save()
    legacy_root = root._within("indexes", "derived_retrieval", "object_level")
    if legacy_root.exists():
        shutil.rmtree(legacy_root)
    _publish_generated_files(root, files)
    account_envelope_count = sum(
        path.startswith("creator_vault/accounts/") and path.endswith("/envelope.json")
        for path in files
    )
    return {
        "status": "rebuilt",
        "views": list(BUILT_VIEWS),
        "creator_vault_account_envelope_count": account_envelope_count,
        "deferred_views": [],
        "generation_id": stamp["generation_id"],
        "file_count": len(files),
        "classification_cache": cache_session.report(),
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
    incremental = _generate_all(
        root,
        stamp,
        product_mention_policy=product_mention_policy,
        cache_session=incremental_cache,
    )
    cold_cache = ClassificationCacheSession(root, use_existing=False)
    cold = _generate_all(
        root,
        stamp,
        product_mention_policy=product_mention_policy,
        cache_session=cold_cache,
    )
    mismatches = sorted(
        relpath for relpath in set(incremental) | set(cold)
        if incremental.get(relpath) != cold.get(relpath)
    )
    return {
        "status": "proven" if not mismatches else "failed",
        "mismatched_files": mismatches,
        "file_count": len(cold),
        "incremental_classification_cache": incremental_cache.report(),
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


def _stored_creator_vault_account_files(root) -> dict[str, bytes]:
    creator_root = root._within(*SILVER_VAULT_CREATOR_PARTS)
    files: dict[str, bytes] = {}
    for pattern in ("accounts/tiktok/*/envelope.json", "manifests/accounts/tiktok/*.json"):
        for path in sorted(creator_root.glob(pattern)):
            if path.is_file():
                files[path.relative_to(creator_root).as_posix()] = path.read_bytes()
    return files


def _prove_stored_creator_vault_accounts(root) -> str:
    stored = _stored_creator_vault_account_files(root)
    if not stored:
        return "absent_nothing_to_prove"
    try:
        manifests = [json.loads(data.decode("utf-8")) for path, data in stored.items() if path.startswith("manifests/")]
        stamps = {(row["generation_id"], row["generated_at"]) for row in manifests}
        if not manifests or len(stamps) != 1:
            raise ValueError("Creator Vault manifests do not share one generation")
        generation_id, generated_at = next(iter(stamps))
    except (UnicodeDecodeError, ValueError, KeyError, TypeError):
        return "failed_unreadable_manifest"
    regenerated = build_creator_vault_account_files(
        _classified_silver_sweep(root),
        {"generation_id": generation_id, "generated_at": generated_at},
    )
    return "rebuildable" if regenerated == stored else "failed_drift_or_non_regenerable"


def prove_derived_retrieval_rebuildability(root) -> dict:
    """Regenerate stored core views and Creator Vault envelopes without writing."""
    root._reverify()
    target_root = _silver_vault_core_root(root)
    view_paths = {name: target_root / "query_tables" / f"{name}.json" for name in BUILT_VIEWS}
    manifest_paths = {name: target_root / "manifests" / f"{name}.json" for name in BUILT_VIEWS}
    if all(view_paths[name].is_file() and manifest_paths[name].is_file() for name in BUILT_VIEWS):
        try:
            stored_manifests = {name: json.loads(manifest_paths[name].read_text(encoding="utf-8")) for name in BUILT_VIEWS}
            stamps = {(manifest["generation_id"], manifest["generated_at"]) for manifest in stored_manifests.values()}
            if len(stamps) != 1:
                raise ValueError("stored view manifests do not share one generation")
            generation_id, generated_at = next(iter(stamps))
            product_mention_policy = normalize_product_mention_policy(
                stored_manifests["by_mention"]["selection_policy_versions"]["product_mention_policy"]
            )
        except (ValueError, KeyError, TypeError):
            pass
        else:
            stamp = {"generation_id": generation_id, "generated_at": generated_at}
            sweep = _classified_silver_sweep(root)
            regenerated = _generate(root, stamp, product_mention_policy=product_mention_policy, sweep=sweep)
            results = {}
            failures = []
            for view_name in BUILT_VIEWS:
                matches = (
                    regenerated[f"query_tables/{view_name}.json"] == view_paths[view_name].read_bytes()
                    and regenerated[f"manifests/{view_name}.json"] == manifest_paths[view_name].read_bytes()
                )
                results[view_name] = "rebuildable" if matches else "failed_drift_or_non_regenerable"
                if not matches:
                    failures.append(view_name)
            creator_vault_matches = build_creator_vault_account_files(sweep, stamp) == _stored_creator_vault_account_files(root)
            results["creator_vault_accounts"] = "rebuildable" if creator_vault_matches else "failed_drift_or_non_regenerable"
            if not creator_vault_matches:
                failures.append("creator_vault_accounts")
            return {"status": "proven" if not failures else "failed", "results": results, "failures": failures}
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
            stamp = {"generation_id": stored_manifest["generation_id"], "generated_at": stored_manifest["generated_at"]}
            product_mention_policy = normalize_product_mention_policy(stored_manifest["selection_policy_versions"]["product_mention_policy"]) if view_name == "by_mention" else None
        except (ValueError, KeyError):
            results[view_name] = "failed_unreadable_manifest"
            failures.append(view_name)
            continue
        regenerated = _generate(root, stamp, product_mention_policy=product_mention_policy, views=(view_name,))
        if regenerated[f"query_tables/{view_name}.json"] == view_path.read_bytes() and regenerated[f"manifests/{view_name}.json"] == manifest_path.read_bytes():
            results[view_name] = "rebuildable"
        else:
            results[view_name] = "failed_drift_or_non_regenerable"
            failures.append(view_name)
    creator_vault_result = _prove_stored_creator_vault_accounts(root)
    results["creator_vault_accounts"] = creator_vault_result
    if creator_vault_result.startswith("failed_"):
        failures.append("creator_vault_accounts")
    return {"status": "proven" if not failures else "failed", "results": results, "failures": failures}

__all__ = [
    "BUILT_VIEWS",
    "BY_CREATOR_VIEW_SCHEMA_VERSION",
    "MANIFEST_SCHEMA_VERSION",
    "MENTIONS_LANE",
    "SILVER_VAULT_CORE_PARTS",
    "SILVER_VAULT_CREATOR_PARTS",
    "VIEW_SCHEMA_VERSION",
    "build_by_creator_view",
    "build_by_mention_view",
    "build_undone_view",
    "audit_derived_retrieval_source_integrity",
    "generation_stamp",
    "prove_incremental_rebuild_equality",
    "prove_derived_retrieval_rebuildability",
    "rebuild_derived_retrieval",
]
