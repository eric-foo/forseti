"""Company Surface producer-owned Silver mapping and deterministic read models.

The generic Silver envelope stays unchanged.  This module owns only the four
Company Surface payloads, their append-only correction edges, and rebuildable
views.  It is intentionally not a matcher, registry, canonical identity owner,
source adapter, or second store.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from datetime import datetime, timezone
import calendar
import hashlib
import json
from pathlib import Path
import re
import shutil
from typing import Any
import uuid

from capture_spine.company_aggregate_forward_signal.validation import (
    validate_company_aggregate_observation,
)
from data_lake.canonical_json import canonical_record_bytes
from data_lake.silver_record import (
    CONTENT_HASH_BASIS,
    SILVER_VAULT_RECORD_SCHEMA_VERSION,
    append_silver_record,
    silver_content_hash,
    validate_silver_vault_record,
)


COMPANY_SURFACE_LANE = "company_surface_silver"
COMPANY_SURFACE_PRODUCER_ID = "company_surface.silver_mapper"
COMPANY_SURFACE_PRODUCER_SCHEMA_VERSION = "company_surface_silver_mapping_v0"
COMPANY_SURFACE_VIEW_SCHEMA_VERSION = 1
COMPANY_SURFACE_MANIFEST_SCHEMA_VERSION = 1
COMPANY_SURFACE_SELECTION_POLICY_VERSION = "company_surface_temporal_selection_v1"
COMPANY_SURFACE_INDEX_PARTS = (
    "indexes",
    "derived_retrieval",
    "silver_vault",
    "company_surface",
)

RECORD_FAMILIES = (
    "subject_assertion",
    "relationship_assertion",
    "company_activity_link",
    "coverage_failure_marker",
)
ASSERTION_STATES = ("resolved", "provisional", "ambiguous", "unresolved")
VIEW_MODES = ("current", "historical_restated", "historical_as_known")

_FAMILY_MAPPING = {
    "subject_assertion": ("observation", "CompanySubjectAssertion", "observation"),
    "relationship_assertion": (
        "relationship",
        "CompanyRelationshipAssertion",
        "relationship",
    ),
    "company_activity_link": ("relationship", "CompanyActivityLink", "relationship"),
    "coverage_failure_marker": (
        "observation",
        "CompanyCoverageMarker",
        "observation",
    ),
}
_EDGE_FIELDS = {
    "corrects": "corrects_record",
    "supersedes": "supersedes_record",
    "conflicts_with": "conflicts_with_record",
}
_COMMON_LOGICAL_KEYS = frozenset(
    {
        "record_ref",
        "record_family",
        "raw_anchor",
        "subject_anchors",
        "evidence_refs",
        "assertion_state",
        "effective_interval",
        "captured_at",
        "recorded_at",
        "limitations",
        "alternatives",
        "corrects",
        "supersedes",
        "conflicts_with",
        "source_surface",
        "producer_row_kind",
        "family_payload",
    }
)
_INTERVAL_KEYS = frozenset(
    {
        "start",
        "start_precision",
        "end",
        "end_precision",
        "end_state",
        "unknown_reason",
    }
)
_PRECISIONS = frozenset({"exact", "day", "month", "year", "unknown"})
_FORBIDDEN_DECISION_KEYS = frozenset(
    {
        "pain_score",
        "pain_hypothesis",
        "recommended_action",
        "recommendation",
        "preferred_intervention",
        "pitch",
        "contact",
        "contact_email",
        "outreach",
    }
)
_SHA256 = re.compile(r"^(?:sha256:)?[0-9a-f]{64}$")


class CompanySurfaceError(ValueError):
    """A logical record, mapping, or view violates the Company Surface contract."""


def validate_company_surface_logical_record(record: Mapping[str, Any]) -> None:
    if not isinstance(record, Mapping):
        raise CompanySurfaceError("Company Surface logical record must be a mapping.")
    _reject_unknown(record, _COMMON_LOGICAL_KEYS, "logical record")
    _reject_decision_fields(record)
    for field in (
        "record_ref",
        "record_family",
        "raw_anchor",
        "captured_at",
        "recorded_at",
        "source_surface",
        "producer_row_kind",
    ):
        _require_string(record.get(field), field)
    family = record.get("record_family")
    if family not in RECORD_FAMILIES:
        raise CompanySurfaceError(f"record_family must be one of {RECORD_FAMILIES}.")
    anchors = _require_string_list(record.get("subject_anchors"), "subject_anchors", non_empty=True)
    for anchor in anchors:
        if not anchor.startswith(("brand:", "org:")):
            raise CompanySurfaceError("subject anchors must use brand:<slug> or org:<slug>.")
    _validate_evidence_refs(record.get("evidence_refs"))
    _validate_interval(record.get("effective_interval"))
    _require_string_list(record.get("limitations"), "limitations")
    _require_string_list(record.get("alternatives"), "alternatives")
    for edge_field in _EDGE_FIELDS:
        _require_string_list(record.get(edge_field), edge_field)

    assertion_state = record.get("assertion_state")
    if family in {"subject_assertion", "relationship_assertion"}:
        if assertion_state not in ASSERTION_STATES:
            raise CompanySurfaceError(
                f"{family} assertion_state must be one of {ASSERTION_STATES}."
            )
    elif assertion_state != "not_applicable":
        raise CompanySurfaceError(f"{family} assertion_state must be 'not_applicable'.")

    payload = record.get("family_payload")
    if not isinstance(payload, Mapping):
        raise CompanySurfaceError("family_payload must be a mapping.")
    _validate_family_payload(family, payload, anchors)


def _validate_family_payload(family: str, payload: Mapping[str, Any], anchors: list[str]) -> None:
    if family == "subject_assertion":
        allowed = frozenset(
            {"raw_identifier", "asserted_subject", "asserted_subject_kind", "competing_candidates"}
        )
        _reject_unknown(payload, allowed, family)
        _require_string(payload.get("raw_identifier"), "raw_identifier")
        subject = _require_string(payload.get("asserted_subject"), "asserted_subject")
        kind = payload.get("asserted_subject_kind")
        if kind not in {"Brand", "Org"}:
            raise CompanySurfaceError("asserted_subject_kind must be Brand or Org.")
        if subject not in anchors:
            raise CompanySurfaceError("asserted_subject must be one of subject_anchors.")
        if (kind == "Brand") != subject.startswith("brand:"):
            raise CompanySurfaceError("asserted subject kind must match its namespace.")
        _require_string_list(payload.get("competing_candidates"), "competing_candidates")
    elif family == "relationship_assertion":
        allowed = frozenset({"subject", "relationship_kind", "object", "source_qualifiers"})
        _reject_unknown(payload, allowed, family)
        subject = _require_string(payload.get("subject"), "relationship subject")
        obj = _require_string(payload.get("object"), "relationship object")
        relation = payload.get("relationship_kind")
        if relation not in {"owned_by", "subsidiary_of"}:
            raise CompanySurfaceError("relationship_kind must be owned_by or subsidiary_of.")
        if relation == "owned_by" and not (subject.startswith("brand:") and obj.startswith("org:")):
            raise CompanySurfaceError("owned_by must connect Brand to Org.")
        if relation == "subsidiary_of" and not (
            subject.startswith("org:") and obj.startswith("org:")
        ):
            raise CompanySurfaceError("subsidiary_of must connect Org to Org.")
        if subject not in anchors or obj not in anchors:
            raise CompanySurfaceError("relationship endpoints must be subject_anchors.")
        _require_string_list(payload.get("source_qualifiers"), "source_qualifiers")
    elif family == "company_activity_link":
        allowed = frozenset(
            {
                "observation_ref",
                "receipt_ref",
                "subject_assertion_ref",
                "activity_kind",
                "capture_posture",
                "source_schema_version",
                "reobserves_observation_id",
            }
        )
        _reject_unknown(payload, allowed, family)
        for field in (
            "observation_ref",
            "receipt_ref",
            "subject_assertion_ref",
            "activity_kind",
            "capture_posture",
            "source_schema_version",
        ):
            _require_string(payload.get(field), field)
        if payload.get("reobserves_observation_id") is not None:
            _require_string(payload["reobserves_observation_id"], "reobserves_observation_id")
    else:
        allowed = frozenset(
            {"surface", "coverage_state", "capture_posture", "receipt_ref", "missing_boundary"}
        )
        _reject_unknown(payload, allowed, family)
        for field in ("surface", "capture_posture", "receipt_ref"):
            _require_string(payload.get(field), field)
        state = payload.get("coverage_state")
        if state not in {"available", "partial", "failed", "excluded", "not_covered"}:
            raise CompanySurfaceError("invalid coverage_state.")
        missing = payload.get("missing_boundary")
        if state == "available" and missing is not None:
            raise CompanySurfaceError("available coverage must not carry missing_boundary.")
        if state != "available":
            _require_string(missing, "missing_boundary")


def map_company_surface_record(
    record: Mapping[str, Any],
    *,
    target_raw_anchors: Mapping[str, str] | None = None,
) -> tuple[dict[str, Any], ...]:
    """Map one logical record plus any correction/conflict edges to Silver records."""
    validate_company_surface_logical_record(record)
    logical = deepcopy(dict(record))
    record_id = company_surface_record_id(logical["record_ref"])
    record_kind, payload_kind, payload_slot = _FAMILY_MAPPING[logical["record_family"]]
    common_payload = {
        "logical_record_ref": logical["record_ref"],
        "record_family": logical["record_family"],
        "subject_anchors": logical["subject_anchors"],
        "assertion_state": logical["assertion_state"],
        "effective_interval": logical["effective_interval"],
        "recorded_at": logical["recorded_at"],
        "evidence_refs": logical["evidence_refs"],
        "limitations": logical["limitations"],
        "alternatives": logical["alternatives"],
        "family_payload": logical["family_payload"],
    }
    primary = _silver_record(
        record_id=record_id,
        raw_anchor=logical["raw_anchor"],
        record_kind=record_kind,
        payload_kind=payload_kind,
        producer_row_kind=logical["producer_row_kind"],
        source_surface=logical["source_surface"],
        observed_at=logical["effective_interval"].get("start"),
        captured_at=logical["captured_at"],
        raw_refs=_silver_raw_refs(logical["evidence_refs"]),
        derived_refs=[],
        payload={payload_slot: common_payload},
    )
    mapped = [primary]
    target_raw_anchors = target_raw_anchors or {}
    for field, edge_type in _EDGE_FIELDS.items():
        for target_ref in logical[field]:
            target_raw_anchor = target_raw_anchors.get(target_ref)
            if target_raw_anchor is None:
                raise CompanySurfaceError(
                    f"{field} target {target_ref!r} requires its persisted raw_anchor."
                )
            target_id = company_surface_record_id(target_ref)
            edge_id = company_surface_edge_record_id(logical["record_ref"], edge_type, target_ref)
            mapped.append(
                _silver_record(
                    record_id=edge_id,
                    raw_anchor=logical["raw_anchor"],
                    record_kind="relationship",
                    payload_kind="RelationshipEdge",
                    producer_row_kind=f"company_surface_{edge_type}",
                    source_surface=logical["source_surface"],
                    observed_at=logical["effective_interval"].get("start"),
                    captured_at=logical["captured_at"],
                    raw_refs=_silver_raw_refs(logical["evidence_refs"]),
                    derived_refs=[
                        {
                            "raw_anchor": logical["raw_anchor"],
                            "lane_namespace": COMPANY_SURFACE_LANE,
                            "record_id": record_id,
                        },
                        {
                            "raw_anchor": target_raw_anchor,
                            "lane_namespace": COMPANY_SURFACE_LANE,
                            "record_id": target_id,
                        },
                    ],
                    payload={
                        "relationship": {
                            "edge_type": edge_type,
                            "from": {"ref_type": "record_id", "ref": record_id},
                            "to": {"ref_type": "record_id", "ref": target_id},
                            "source_logical_record_ref": logical["record_ref"],
                            "target_logical_record_ref": target_ref,
                            "recorded_at": logical["recorded_at"],
                        }
                    },
                )
            )
    return tuple(mapped)


def company_activity_logical_record_from_observation(
    observation: Mapping[str, Any],
    *,
    subject_assertion_ref: str,
    recorded_at: str,
    record_ref: str | None = None,
) -> dict[str, Any]:
    """Translate a validated Capture observation into a Company-activity link.

    The observation payload remains upstream.  The logical record stores only
    references and the semantics required to attach it to a company subject.
    """
    validate_company_aggregate_observation(observation)
    source_time = next(
        time_value
        for time_value in (
            observation["source_effective_time"],
            observation["as_of_time"],
            observation["filing_time"],
        )
        if time_value["value"] is not None
    )
    provenance = observation["provenance"]
    result = {
        "record_ref": record_ref or f"company.activity.{observation['observation_id']}",
        "record_family": "company_activity_link",
        "raw_anchor": provenance[0]["packet_id"],
        "subject_anchors": [observation["entity_key"]],
        "evidence_refs": [dict(ref) for ref in provenance],
        "assertion_state": "not_applicable",
        "effective_interval": {
            "start": source_time["value"],
            "start_precision": source_time["precision"],
            "end": source_time["value"],
            "end_precision": source_time["precision"],
            "end_state": "bounded",
            "unknown_reason": None,
        },
        "captured_at": observation["captured_at"],
        "recorded_at": recorded_at,
        "limitations": list(observation["limitations"]),
        "alternatives": [],
        "corrects": [],
        "supersedes": [],
        "conflicts_with": [],
        "source_surface": observation["source_tag"],
        "producer_row_kind": f"company_activity_link_{observation['signal_kind']}",
        "family_payload": {
            "observation_ref": observation["observation_id"],
            "receipt_ref": provenance[0]["packet_id"],
            "subject_assertion_ref": subject_assertion_ref,
            "activity_kind": observation["signal_kind"],
            "capture_posture": observation["capture_posture"],
            "source_schema_version": observation["schema_version"],
            "reobserves_observation_id": observation.get("reobserves_observation_id"),
        },
    }
    validate_company_surface_logical_record(result)
    return result


def append_company_surface_logical_record(data_root, record: Mapping[str, Any]) -> tuple[Path, ...]:
    target_raw_anchors = {
        _company_payload(existing)["logical_record_ref"]: existing["raw_anchor"]
        for existing in load_company_surface_records(data_root)
        if existing["payload_kind"] != "RelationshipEdge"
    }
    paths = []
    for mapped in map_company_surface_record(
        record,
        target_raw_anchors=target_raw_anchors,
    ):
        paths.append(
            append_silver_record(
                data_root,
                raw_anchor=mapped["raw_anchor"],
                lane=COMPANY_SURFACE_LANE,
                record_id=mapped["record_id"],
                record=mapped,
            )
        )
    return tuple(paths)


def append_company_surface_logical_records(
    data_root, records: Sequence[Mapping[str, Any]]
) -> tuple[Path, ...]:
    paths: list[Path] = []
    for record in records:
        paths.extend(append_company_surface_logical_record(data_root, record))
    return tuple(paths)


def load_company_surface_records(data_root) -> list[dict[str, Any]]:
    data_root._reverify()
    derived = data_root._within("derived")
    if not derived.exists():
        return []
    records = []
    for path in sorted(derived.glob(f"*/*/{COMPANY_SURFACE_LANE}/*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        validate_silver_vault_record(record)
        records.append(record)
    return records


def build_company_surface_view(
    records: Sequence[Mapping[str, Any]], query: Mapping[str, Any]
) -> dict[str, Any]:
    query = _validate_query(query)
    cutoff = _parse_datetime(query["knowledge_cutoff"])
    primaries: list[Mapping[str, Any]] = []
    edges: list[Mapping[str, Any]] = []
    all_records: dict[str, Mapping[str, Any]] = {}
    for record in records:
        validate_silver_vault_record(record)
        if record["lane_namespace"] != COMPANY_SURFACE_LANE:
            raise CompanySurfaceError("view input contains a non-Company-Surface lane record.")
        all_records[record["record_id"]] = record
        if record["payload_kind"] == "RelationshipEdge":
            edges.append(record)
        elif record["payload_kind"] in {mapping[1] for mapping in _FAMILY_MAPPING.values()}:
            primaries.append(record)

    eligible_edges = [edge for edge in edges if _recorded_at(edge) <= cutoff]
    replaced: dict[str, list[dict[str, str]]] = {}
    conflicts: list[dict[str, str]] = []
    for edge in eligible_edges:
        body = edge["payload"]["relationship"]
        entry = {
            "edge_record_id": edge["record_id"],
            "edge_type": body["edge_type"],
            "from_record_id": body["from"]["ref"],
            "to_record_id": body["to"]["ref"],
        }
        if body["edge_type"] in {"corrects_record", "supersedes_record"}:
            replaced.setdefault(body["to"]["ref"], []).append(entry)
        else:
            conflicts.append(entry)

    eligible_primary_by_ref: dict[str, Mapping[str, Any]] = {}
    for record in primaries:
        if _recorded_at(record) <= cutoff and record["record_id"] not in replaced:
            common = _company_payload(record)
            eligible_primary_by_ref[common["logical_record_ref"]] = record

    resolved: list[dict[str, Any]] = []
    residuals: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []
    exclusions: list[dict[str, Any]] = []
    for record in sorted(primaries, key=lambda item: item["record_id"]):
        common = _company_payload(record)
        if _recorded_at(record) > cutoff:
            exclusions.append({"record_id": record["record_id"], "reason": "after_knowledge_cutoff"})
            continue
        if record["record_id"] in replaced:
            exclusions.append(
                {
                    "record_id": record["record_id"],
                    "reason": "corrected_or_superseded",
                    "edges": replaced[record["record_id"]],
                }
            )
            continue
        if query["anchor_subject"] not in common["subject_anchors"]:
            exclusions.append({"record_id": record["record_id"], "reason": "different_anchor"})
            continue
        interval_state = _interval_selection_state(
            common["effective_interval"], query["effective_boundary"]
        )
        entry = _view_record_entry(record, common)
        if interval_state == "excluded":
            exclusions.append({"record_id": record["record_id"], "reason": "outside_effective_boundary"})
            continue
        if common["record_family"] == "coverage_failure_marker":
            coverage.append(entry)
            continue
        if interval_state == "indeterminate":
            residuals.append({"reason": "temporally_indeterminate", **entry})
            continue
        if common["assertion_state"] in {"provisional", "ambiguous", "unresolved"}:
            residuals.append({"reason": f"assertion_{common['assertion_state']}", **entry})
            continue
        if common["record_family"] == "company_activity_link":
            assertion_ref = common["family_payload"]["subject_assertion_ref"]
            assertion_record = eligible_primary_by_ref.get(assertion_ref)
            if assertion_record is None or _company_payload(assertion_record)["assertion_state"] != "resolved":
                residuals.append({"reason": "subject_assertion_not_resolved", **entry})
                continue
            # Activity may attach only through an assertion that is itself
            # determinate and applicable at the requested boundary; a resolved
            # state alone does not license the roll-up.
            if (
                _interval_selection_state(
                    _company_payload(assertion_record)["effective_interval"],
                    query["effective_boundary"],
                )
                != "applicable"
            ):
                residuals.append(
                    {"reason": "subject_assertion_not_applicable_at_boundary", **entry}
                )
                continue
        resolved.append(entry)

    visible_ids = {entry["record_id"] for entry in resolved + coverage}
    visible_ids.update(entry["record_id"] for entry in residuals)
    visible_conflicts = [
        edge
        for edge in conflicts
        if edge["from_record_id"] in visible_ids or edge["to_record_id"] in visible_ids
    ]
    return {
        "view_schema_version": COMPANY_SURFACE_VIEW_SCHEMA_VERSION,
        "view_mode": query["mode"],
        "query_boundaries": query,
        "selection_policy_version": COMPANY_SURFACE_SELECTION_POLICY_VERSION,
        "resolved_records": resolved,
        "coverage_and_failure_markers": coverage,
        "visible_residuals": residuals,
        "conflicts": visible_conflicts,
        "exclusions": exclusions,
        "non_authoritative": True,
    }


def company_surface_generation_stamp() -> dict[str, str]:
    return {
        "generation_id": uuid.uuid4().hex,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def generate_company_surface_view_files(
    records: Sequence[Mapping[str, Any]],
    queries: Sequence[Mapping[str, Any]],
    *,
    stamp: Mapping[str, str],
) -> dict[str, bytes]:
    generation_id = _require_string(stamp.get("generation_id"), "generation_id")
    generated_at = _require_string(stamp.get("generated_at"), "generated_at")
    source_ids = sorted(str(record["record_id"]) for record in records)
    source_set_hash = hashlib.sha256(canonical_record_bytes(source_ids)).hexdigest()
    recorded_times = [_recorded_at(record) for record in records if record["payload_kind"] in ({"RelationshipEdge"} | {mapping[1] for mapping in _FAMILY_MAPPING.values()})]
    high_watermark = max(recorded_times).isoformat() if recorded_times else None
    files: dict[str, bytes] = {}
    seen_modes: set[str] = set()
    for raw_query in queries:
        query = _validate_query(raw_query)
        mode = query["mode"]
        if mode in seen_modes:
            raise CompanySurfaceError(f"duplicate view mode in one generation: {mode}")
        seen_modes.add(mode)
        view = build_company_surface_view(records, query)
        view_bytes = canonical_record_bytes(view)
        manifest = {
            "manifest_schema_version": COMPANY_SURFACE_MANIFEST_SCHEMA_VERSION,
            "view_mode": mode,
            "generation_id": generation_id,
            "generated_at": generated_at,
            "source_record_ids": source_ids,
            "source_high_watermark": {
                "recorded_at": high_watermark,
                "record_set_sha256": source_set_hash,
            },
            "selection_policy_versions": {
                "company_surface": COMPANY_SURFACE_SELECTION_POLICY_VERSION,
                "view_schema": COMPANY_SURFACE_VIEW_SCHEMA_VERSION,
            },
            "query": query,
            "view_sha256": hashlib.sha256(view_bytes).hexdigest(),
            "stale_if": "committed company_surface_silver record set or selection policy changes",
        }
        files[f"views/{mode}.json"] = view_bytes
        files[f"manifests/{mode}.json"] = canonical_record_bytes(manifest)
    return files


def rebuild_company_surface_views(
    data_root,
    queries: Sequence[Mapping[str, Any]],
    *,
    stamp: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    data_root._reverify()
    stamp = stamp or company_surface_generation_stamp()
    records = load_company_surface_records(data_root)
    files = generate_company_surface_view_files(records, queries, stamp=stamp)
    target_root = data_root._within(*COMPANY_SURFACE_INDEX_PARTS)
    if target_root.exists():
        shutil.rmtree(target_root)
    for relpath, content in files.items():
        target = target_root / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    return {
        "status": "rebuilt",
        "view_modes": sorted(path.split("/")[1].split(".")[0] for path in files if path.startswith("views/")),
        "generation_id": stamp["generation_id"],
        "file_count": len(files),
    }


def prove_company_surface_views_rebuildable(data_root) -> dict[str, Any]:
    data_root._reverify()
    target_root = data_root._within(*COMPANY_SURFACE_INDEX_PARTS)
    manifest_dir = target_root / "manifests"
    if not manifest_dir.exists():
        return {"status": "no_views_generated", "results": {}, "failures": []}
    manifest_paths = sorted(manifest_dir.glob("*.json"))
    if not manifest_paths:
        return {"status": "no_views_generated", "results": {}, "failures": []}
    records = load_company_surface_records(data_root)
    results: dict[str, str] = {}
    failures: list[str] = []
    for manifest_path in manifest_paths:
        mode = manifest_path.stem
        view_path = target_root / "views" / f"{mode}.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            regenerated = generate_company_surface_view_files(
                records,
                [manifest["query"]],
                stamp={
                    "generation_id": manifest["generation_id"],
                    "generated_at": manifest["generated_at"],
                },
            )
        except (ValueError, KeyError, json.JSONDecodeError, CompanySurfaceError):
            results[mode] = "failed_unreadable_manifest"
            failures.append(mode)
            continue
        if (
            view_path.is_file()
            and regenerated[f"views/{mode}.json"] == view_path.read_bytes()
            and regenerated[f"manifests/{mode}.json"] == manifest_path.read_bytes()
        ):
            results[mode] = "rebuildable"
        else:
            results[mode] = "failed_drift_or_non_regenerable"
            failures.append(mode)
    return {"status": "proven" if not failures else "failed", "results": results, "failures": failures}


def company_surface_record_id(logical_record_ref: str) -> str:
    digest = hashlib.sha256(logical_record_ref.encode("utf-8")).hexdigest()[:24]
    return f"company_{digest}.json"


def company_surface_edge_record_id(source_ref: str, edge_type: str, target_ref: str) -> str:
    digest = hashlib.sha256(f"{source_ref}|{edge_type}|{target_ref}".encode("utf-8")).hexdigest()[:24]
    return f"company_edge_{digest}.json"


def _silver_record(
    *,
    record_id: str,
    raw_anchor: str,
    record_kind: str,
    payload_kind: str,
    producer_row_kind: str,
    source_surface: str,
    observed_at: str | None,
    captured_at: str,
    raw_refs: list[dict[str, Any]],
    derived_refs: list[dict[str, Any]],
    payload: dict[str, Any],
) -> dict[str, Any]:
    record = {
        "record_id": record_id,
        "raw_anchor": raw_anchor,
        "lane_namespace": COMPANY_SURFACE_LANE,
        "producer_id": COMPANY_SURFACE_PRODUCER_ID,
        "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "producer_schema_version": COMPANY_SURFACE_PRODUCER_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": CONTENT_HASH_BASIS,
        "record_kind": record_kind,
        "payload_kind": payload_kind,
        "producer_row_kind": producer_row_kind,
        "source_surface": source_surface,
        "observed_at": observed_at,
        "captured_at": captured_at,
        "raw_refs": raw_refs,
        "derived_refs": derived_refs,
        "payload": payload,
    }
    record["content_hash"] = f"sha256:{silver_content_hash(record)}"
    validate_silver_vault_record(record)
    return record


def _silver_raw_refs(evidence_refs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    refs = []
    for ref in evidence_refs:
        physical_ref = {
            "ref_type": "raw_packet",
            "packet_id": ref["packet_id"],
        }
        if ref["hash_basis"] == "raw_stored_bytes":
            physical_ref.update(
                {
                    "sha256": ref["sha256"],
                    "hash_basis": "raw_stored_bytes",
                }
            )
        refs.append(physical_ref)
    return refs


def _validate_evidence_refs(value: Any) -> None:
    if not _is_list(value) or not value:
        raise CompanySurfaceError("evidence_refs must be a non-empty list.")
    allowed = frozenset({"packet_id", "source_locator", "sha256", "hash_basis", "source_span"})
    for index, ref in enumerate(value):
        if not isinstance(ref, Mapping):
            raise CompanySurfaceError(f"evidence_refs[{index}] must be a mapping.")
        _reject_unknown(ref, allowed, f"evidence_refs[{index}]")
        for field in ("packet_id", "source_locator", "sha256", "hash_basis"):
            _require_string(ref.get(field), f"evidence_refs[{index}].{field}")
        if _SHA256.fullmatch(str(ref["sha256"])) is None:
            raise CompanySurfaceError("evidence sha256 must be lowercase sha256.")
        if ref.get("source_span") is not None:
            _require_string(ref["source_span"], f"evidence_refs[{index}].source_span")


def _validate_interval(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise CompanySurfaceError("effective_interval must be a mapping.")
    _reject_unknown(value, _INTERVAL_KEYS, "effective_interval")
    start_precision = value.get("start_precision")
    end_precision = value.get("end_precision")
    if start_precision not in _PRECISIONS or end_precision not in _PRECISIONS:
        raise CompanySurfaceError("effective interval precision is invalid.")
    start = value.get("start")
    unknown_reason = value.get("unknown_reason")
    if start_precision == "unknown":
        if start is not None:
            raise CompanySurfaceError("unknown interval start must not carry a value.")
        _require_string(unknown_reason, "effective_interval.unknown_reason")
    else:
        _require_string(start, "effective_interval.start")
    end_state = value.get("end_state")
    if end_state not in {"bounded", "open", "unknown"}:
        raise CompanySurfaceError("end_state must be bounded, open, or unknown.")
    if end_state == "bounded":
        _require_string(value.get("end"), "effective_interval.end")
        if end_precision == "unknown":
            raise CompanySurfaceError("bounded interval end cannot have unknown precision.")
    elif value.get("end") is not None:
        raise CompanySurfaceError("open or unknown interval end must not carry a value.")
    if end_state == "unknown":
        _require_string(unknown_reason, "effective_interval.unknown_reason")


def _validate_query(value: Mapping[str, Any]) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise CompanySurfaceError("view query must be a mapping.")
    allowed = frozenset({"mode", "anchor_subject", "effective_boundary", "knowledge_cutoff"})
    _reject_unknown(value, allowed, "view query")
    query = {key: _require_string(value.get(key), f"query.{key}") for key in allowed}
    if query["mode"] not in VIEW_MODES:
        raise CompanySurfaceError(f"view mode must be one of {VIEW_MODES}.")
    if not query["anchor_subject"].startswith(("brand:", "org:")):
        raise CompanySurfaceError("view anchor_subject must be Brand or Org.")
    _parse_datetime(query["knowledge_cutoff"])
    _parse_datetime(query["effective_boundary"])
    return query


def _recorded_at(record: Mapping[str, Any]) -> datetime:
    body = record["payload"]["relationship"] if record["payload_kind"] == "RelationshipEdge" else _company_payload(record)
    return _parse_datetime(body["recorded_at"])


def _company_payload(record: Mapping[str, Any]) -> Mapping[str, Any]:
    slot = "observation" if record["record_kind"] == "observation" else "relationship"
    return record["payload"][slot]


def _view_record_entry(record: Mapping[str, Any], common: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "record_id": record["record_id"],
        "content_hash": record["content_hash"],
        "payload_kind": record["payload_kind"],
        "source_surface": record["source_surface"],
        "observed_at": record["observed_at"],
        "captured_at": record["captured_at"],
        "raw_refs": deepcopy(list(record["raw_refs"])),
        "record": deepcopy(dict(common)),
    }


def _interval_selection_state(interval: Mapping[str, Any], boundary: str) -> str:
    point = _parse_datetime(boundary)
    if interval["start_precision"] == "unknown":
        return "indeterminate"
    start_low, start_high = _precision_bounds(interval["start"], interval["start_precision"])
    if point < start_low:
        return "excluded"
    if start_low != start_high and point <= start_high:
        return "indeterminate"
    if interval["end_state"] == "open":
        return "applicable"
    if interval["end_state"] == "unknown":
        return "indeterminate"
    end_low, end_high = _precision_bounds(interval["end"], interval["end_precision"])
    if point > end_high:
        return "excluded"
    if end_low != end_high and point >= end_low:
        return "indeterminate"
    return "applicable"


def _precision_bounds(value: str, precision: str) -> tuple[datetime, datetime]:
    if precision in {"exact", "day"}:
        point = _parse_datetime(value)
        if precision == "day" and "T" not in value:
            return point, point.replace(hour=23, minute=59, second=59, microsecond=999999)
        return point, point
    if precision == "month":
        year, month = (int(part) for part in value.split("-")[:2])
        last = calendar.monthrange(year, month)[1]
        return (
            datetime(year, month, 1, tzinfo=timezone.utc),
            datetime(year, month, last, 23, 59, 59, 999999, tzinfo=timezone.utc),
        )
    if precision == "year":
        year = int(value[:4])
        return (
            datetime(year, 1, 1, tzinfo=timezone.utc),
            datetime(year, 12, 31, 23, 59, 59, 999999, tzinfo=timezone.utc),
        )
    raise CompanySurfaceError(f"unsupported precision: {precision}")


def _parse_datetime(value: str) -> datetime:
    try:
        if re.fullmatch(r"\d{4}", value):
            return datetime(int(value), 1, 1, tzinfo=timezone.utc)
        if re.fullmatch(r"\d{4}-\d{2}", value):
            return datetime.fromisoformat(value + "-01").replace(tzinfo=timezone.utc)
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CompanySurfaceError(f"invalid ISO time: {value!r}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _reject_decision_fields(value: Any, path: str = "record") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).lower() in _FORBIDDEN_DECISION_KEYS:
                raise CompanySurfaceError(f"decision/GTM field is forbidden at {path}.{key}")
            _reject_decision_fields(child, f"{path}.{key}")
    elif _is_list(value):
        for index, child in enumerate(value):
            _reject_decision_fields(child, f"{path}[{index}]")


def _reject_unknown(value: Mapping[str, Any], allowed: frozenset[str], label: str) -> None:
    unknown = sorted(str(key) for key in value if str(key) not in allowed)
    if unknown:
        raise CompanySurfaceError(f"{label} contains unknown field(s): {unknown}")


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CompanySurfaceError(f"{label} must be a non-empty string.")
    return value


def _require_string_list(value: Any, label: str, *, non_empty: bool = False) -> list[str]:
    if not _is_list(value) or (non_empty and not value):
        raise CompanySurfaceError(f"{label} must be {'a non-empty ' if non_empty else 'an explicit '}list.")
    result = []
    for item in value:
        result.append(_require_string(item, label))
    return result


def _is_list(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


__all__ = [
    "ASSERTION_STATES",
    "COMPANY_SURFACE_INDEX_PARTS",
    "COMPANY_SURFACE_LANE",
    "COMPANY_SURFACE_MANIFEST_SCHEMA_VERSION",
    "COMPANY_SURFACE_SELECTION_POLICY_VERSION",
    "COMPANY_SURFACE_VIEW_SCHEMA_VERSION",
    "CompanySurfaceError",
    "RECORD_FAMILIES",
    "VIEW_MODES",
    "append_company_surface_logical_record",
    "append_company_surface_logical_records",
    "build_company_surface_view",
    "company_activity_logical_record_from_observation",
    "company_surface_edge_record_id",
    "company_surface_generation_stamp",
    "company_surface_record_id",
    "generate_company_surface_view_files",
    "load_company_surface_records",
    "map_company_surface_record",
    "prove_company_surface_views_rebuildable",
    "rebuild_company_surface_views",
    "validate_company_surface_logical_record",
]
