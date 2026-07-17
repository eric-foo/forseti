"""Read-only, deterministic Silver Vault observation census.

The counting unit is a unique ``subject + observation type/metric + observed
time + policy + lineage anchor``.  Stored files are counted separately from
commercial observations.  Duplicate units are suppressed, conflicting units
are surfaced, unavailable/not-attempted cells never become numeric zero, and
derived values never double-count their inputs.

This module scans RAW manifests and registered Silver lanes directly.  It does
not consult or write a maintained total, availability index, database, or live
status file, so the output is rebuildable from authority on every invocation.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from data_lake.lane_registry import LaneRole, SILVER_LANES, role_of
from data_lake.root import EPOCH_MARKER_FILENAME, LEGACY_EPOCH_MARKER_FILENAME
from data_lake.creator_metric_lineage import (
    EXCLUDED as CREATOR_METRIC_EXCLUDED,
    HISTORICAL_COMPATIBLE as CREATOR_METRIC_HISTORICAL_COMPATIBLE,
    OBSERVATION_LANE as CREATOR_METRIC_OBSERVATION_LANE,
    ROLLUP_LANE as CREATOR_METRIC_ROLLUP_LANE,
    SOURCE_BACKED_COMPLETE as CREATOR_METRIC_SOURCE_BACKED_COMPLETE,
    build_creator_metric_lineage_index,
)
from data_lake.silver_record import (
    CURRENT_SOURCE_BACKED_AUTHORITY,
    HISTORICAL_COMPATIBLE_AUTHORITY,
    INVALID_SILVER_AUTHORITY,
    SILVER_VAULT_RECORD_SCHEMA_VERSION,
    classify_silver_vault_record_sources,
    silver_raw_refs_bound_to_own_anchor,
    validate_silver_vault_record,
    verify_silver_vault_record_sources,
)

CENSUS_SCHEMA_VERSION = "silver_observation_census_v0"

# This is a read-side adapter for the corrected producer policy.  It deliberately
# names the current public policy token and the three source ordinal domains so
# historical v0 zero sentinels cannot enter the meaningful-observation headline.
FRAGRANTICA_REVIEW_VOTE_POLICY_VERSION = "fragrantica_review_vote_valid_ordinal_v1"
_FRAGRANTICA_REVIEW_VOTE_VALUES: dict[str, frozenset[int]] = {
    "review_rating": frozenset(range(1, 6)),
    "review_longevity_vote": frozenset(range(1, 6)),
    "review_sillage_vote": frozenset(range(1, 5)),
}

_ADDITIVE_FIELDS = (
    "silver_records",
    "current_source_backed_silver_records",
    "historical_compatible_silver_records",
    "retired_audit_only_silver_records",
    "identity_entity_records",
    "relationship_edge_records",
    "content_observations",
    "directly_observed_atomic_metric_values",
    "current_policy_qualified_direct_metric_values",
    "text_observations",
    "derived_analytical_values",
    "unavailable_with_reason_states",
    "not_attempted_states",
    "excluded_invalid_observed_metric_values",
    "historical_unqualified_metric_values",
    "creator_metric_source_backed_complete_records",
    "creator_metric_historical_compatible_records",
    "creator_metric_excluded_records",
    "current_source_backed_creator_metric_records",
    "deep_capture_current_source_backed_records",
    "deep_capture_historical_audit_only_records",
    "deep_capture_current_completion_markers",
    "deep_capture_historical_audit_only_completion_markers",
    "unclassified_silver_records",
    "duplicate_observation_units_suppressed",
    "conflicting_observation_units",
)

# Mechanical applicability selectors used only when a registered current lane
# is empty.  A selector is (source_family, source_surface prefix or None).
# Populated lanes and retired lanes never depend on this table for their state.
_DEEP_CAPTURE_APPLICABILITY = (("instagram_creator", "ig_reels_deep_capture"),)
_LANE_APPLICABILITY: dict[str, tuple[tuple[str, str | None], ...]] = {
    "cleaning_basenotes_silver": (("fragrance_native_database", "basenotes_"),),
    "cleaning_fragrantica_silver": (("fragrance_native_database", "fragrantica_"),),
    "cleaning_parfumo_silver": (("fragrance_native_database", "parfumo_"),),
    # The vertical slice has no authorized source-access route.  Populated
    # records are counted normally; an empty lane is intentionally inactive
    # rather than inferred applicable from unrelated raw packets.
    "company_surface_silver": (),
    "creator_metric_silver": (
        ("youtube", None),
        ("instagram_creator", None),
        ("social_media", None),
    ),
    "creator_metric_rollup_silver": (
        ("youtube", None),
        ("instagram_creator", None),
        ("social_media", None),
    ),
    "social_metric_observation_set_silver": (
        ("tiktok", "tiktok_creator_grid_window"),
        ("instagram_creator", "ig_reels_grid"),
    ),
    "tiktok_comment_attention_silver": (
        ("tiktok", "tiktok_creator_batch_comment_subtitle_admission"),
    ),
    "transcript_product_mentions_silver": (
        ("youtube", None),
        ("tiktok", "tiktok_creator_batch_comment_subtitle_admission"),
        ("instagram_creator", None),
    ),
    "raw_packet_tombstone_silver": (),
    "retail_pdp_silver": (
        ("fragrance_purchase_review_pdp", None),
        ("retail_pdp", None),
    ),
    "silver__capture__audience_comments": _DEEP_CAPTURE_APPLICABILITY,
    "silver__capture__reel_transcript": _DEEP_CAPTURE_APPLICABILITY,
}
_DEEP_CAPTURE_SILVER_LANES = frozenset(
    {"silver__capture__audience_comments", "silver__capture__reel_transcript"}
)
_DEEP_CAPTURE_SET_LANE = "silver__capture__reel_deep_capture__set"
_ACTIVE_SILVER_LANES = {
    lane for lane in SILVER_LANES if role_of(lane) is not LaneRole.RETIRED_SILVER_LINEAGE
}
if set(_LANE_APPLICABILITY) != _ACTIVE_SILVER_LANES:
    raise RuntimeError(
        "Silver census applicability must cover every current registered Silver lane "
        f"(missing={sorted(_ACTIVE_SILVER_LANES - set(_LANE_APPLICABILITY))!r}, "
        f"extra={sorted(set(_LANE_APPLICABILITY) - _ACTIVE_SILVER_LANES)!r})"
    )



def _empty_counts() -> Counter[str]:
    return Counter({field: 0 for field in _ADDITIVE_FIELDS})


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    try:
        parsed = datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith("Z") else text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _timestamp_z(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _known_time_values(value: Any, *, key: str | None = None) -> list[datetime]:
    found: list[datetime] = []
    if isinstance(value, Mapping):
        for child_key, child in value.items():
            found.extend(_known_time_values(child, key=str(child_key)))
    elif isinstance(value, list):
        for child in value:
            found.extend(_known_time_values(child, key=key))
    elif key in {
        "observed_at",
        "captured_at",
        "created_at",
        "capture_time",
        "source_publication_or_event",
        "computed_at",
        "start",
        "end",
        "value",
    }:
        parsed = _timestamp(value)
        if parsed is not None:
            found.append(parsed)
    return found


def _epoch(root: Path) -> dict[str, Any]:
    primary = root / EPOCH_MARKER_FILENAME
    legacy = root / LEGACY_EPOCH_MARKER_FILENAME
    path = primary if primary.is_file() else legacy
    if not path.is_file():
        raise ValueError(f"Silver census requires a lake epoch marker under {root}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"lake epoch marker must be a JSON object: {path}")
    return value


def _manifest_failed(manifest: Mapping[str, Any]) -> bool:
    posture = manifest.get("access_posture")
    if not isinstance(posture, Mapping):
        return False
    status = str(posture.get("status") or "").casefold()
    detail = " ".join(str(posture.get(key) or "") for key in ("value", "reason")).casefold()
    return status in {"failed", "unavailable", "unknown_with_reason"} or "failed" in detail


def _scan_manifests(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[datetime], list[str]]:
    manifests: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    times: list[datetime] = []
    fingerprint_parts: list[str] = []
    raw = root / "raw"
    if not raw.is_dir():
        return manifests, errors, times, fingerprint_parts
    for path in sorted(raw.glob("*/*/manifest.json")):
        relative = path.relative_to(root).as_posix()
        stat = path.stat()
        fingerprint_parts.append(f"{relative}\0{stat.st_size}\0{stat.st_mtime_ns}")
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(value, dict):
                raise ValueError("manifest is not a JSON object")
            manifests.append(value)
            times.extend(_known_time_values(value))
        except (OSError, ValueError, TypeError) as exc:
            errors.append(
                {"kind": "raw_manifest_unreadable", "path": relative, "error": f"{type(exc).__name__}: {exc}"}
            )
            times.append(datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc))
    return manifests, errors, times, fingerprint_parts


def _policy_identity(record: Mapping[str, Any], observation: Mapping[str, Any]) -> str:
    tokens: list[str] = []
    for owner in (record, observation, record.get("provenance")):
        if not isinstance(owner, Mapping):
            continue
        for key, value in sorted(owner.items()):
            if (
                key == "policy_version"
                or key.endswith("_policy_version")
                or key == "rubric_version"
            ) and isinstance(value, str) and value.strip():
                tokens.append(f"{key}={value.strip()}")
    if tokens:
        return "|".join(sorted(set(tokens)))
    producer = str(record.get("producer_schema_version") or "unknown")
    return f"missing_explicit_policy:producer_schema_version={producer}"


def _observation_window(record: Mapping[str, Any], observation: Mapping[str, Any]) -> str:
    coverage = observation.get("coverage_window")
    if isinstance(coverage, Mapping) and (coverage.get("start") or coverage.get("end")):
        return f"coverage:{coverage.get('start') or '<open>'}/{coverage.get('end') or '<open>'}"
    if observation.get("rollup_window"):
        return f"rollup:{observation.get('rollup_window')}"
    point = record.get("observed_at")
    return f"point:{point}" if point else "unknown"


def _subject_key(subject: Any) -> str:
    if isinstance(subject, Mapping):
        return _canonical(subject)
    if subject is None:
        return "<missing-subject>"
    return _canonical(subject)


def _subject_kind(subject: Any) -> str:
    if not isinstance(subject, Mapping):
        return ""
    ref = subject.get("ref")
    if isinstance(ref, Mapping):
        return str(ref.get("kind") or "").casefold()
    return str(subject.get("kind") or "").casefold()


class _Accumulator:
    def __init__(self) -> None:
        self.totals = _empty_counts()
        self.groups: dict[str, dict[str, Counter[str]]] = {
            "lane": defaultdict(_empty_counts),
            "source_family": defaultdict(_empty_counts),
            "policy_version": defaultdict(_empty_counts),
            "observation_window": defaultdict(_empty_counts),
        }
        self.units: dict[str, str] = {}
        self.subjects: set[str] = set()
        self.content_objects: set[str] = set()
        self.accounts: set[str] = set()
        self.products: set[str] = set()
        self.errors: list[dict[str, Any]] = []

    def increment(self, field: str, context: Mapping[str, str]) -> None:
        self.totals[field] += 1
        for dimension in self.groups:
            self.groups[dimension][context[dimension]][field] += 1

    def remember_subject(self, subject: Any) -> None:
        key = _subject_key(subject)
        if key == "<missing-subject>":
            return
        self.subjects.add(key)
        kind = _subject_kind(subject)
        if "account" in kind:
            self.accounts.add(key)
        if "content" in kind or kind in {"public_comment", "transcript"}:
            self.content_objects.add(key)
        if "product" in kind:
            self.products.add(key)

    def add_unit(
        self,
        *,
        field: str,
        subject: Any,
        observation_type: str,
        record: Mapping[str, Any],
        policy: str,
        context: Mapping[str, str],
    ) -> bool:
        unit = _canonical(
            {
                "subject": subject,
                "observation_type": observation_type,
                "observed_at": record.get("observed_at"),
                "policy": policy,
                "lineage_anchor": record.get("raw_anchor"),
            }
        )
        prior = self.units.get(unit)
        if prior == field:
            self.increment("duplicate_observation_units_suppressed", context)
            return False
        if prior is not None:
            self.increment("conflicting_observation_units", context)
            self.errors.append(
                {"kind": "conflicting_observation_unit", "unit": json.loads(unit), "first": prior, "second": field}
            )
            return False
        self.units[unit] = field
        self.increment(field, context)
        self.remember_subject(subject)
        return True


def _context(
    record: Mapping[str, Any],
    observation: Mapping[str, Any],
    *,
    lane: str,
    manifest_by_packet: Mapping[str, Mapping[str, Any]],
) -> dict[str, str]:
    source_family = str(record.get("source_family") or "").strip()
    if not source_family:
        manifest = manifest_by_packet.get(str(record.get("raw_anchor") or ""), {})
        source_family = str(manifest.get("source_family") or "missing_explicit_source_family")
    return {
        "lane": lane,
        "source_family": source_family,
        "policy_version": _policy_identity(record, observation),
        "observation_window": _observation_window(record, observation),
    }


def _metric_is_derived(record: Mapping[str, Any], observation: Mapping[str, Any]) -> bool:
    provenance = record.get("provenance")
    return bool(
        observation.get("derivation")
        or observation.get("numerator")
        or observation.get("denominator")
        or observation.get("calculation_recipe_version")
        or (isinstance(provenance, Mapping) and provenance.get("calculation_recipe_version"))
    )


def _fragrantica_vote_status(
    record: Mapping[str, Any], observation: Mapping[str, Any]
) -> tuple[bool, bool, bool]:
    """Return meaningful, current-policy-qualified, historical-unqualified."""
    metric_name = str(observation.get("metric_name") or "")
    allowed = _FRAGRANTICA_REVIEW_VOTE_VALUES.get(metric_name)
    if record.get("lane_namespace") != "cleaning_fragrantica_silver" or allowed is None:
        return True, True, False
    value = observation.get("metric_value")
    meaningful = type(value) is int and value in allowed
    provenance = record.get("provenance")
    current = (
        isinstance(provenance, Mapping)
        and provenance.get("review_vote_policy_version") == FRAGRANTICA_REVIEW_VOTE_POLICY_VERSION
    )
    return meaningful, current and meaningful, not current


def _add_metric(
    accumulator: _Accumulator,
    *,
    record: Mapping[str, Any],
    observation: Mapping[str, Any],
    subject: Any,
    metric_name: str,
    posture: Mapping[str, Any],
    policy: str,
    context: Mapping[str, str],
    derived: bool,
) -> None:
    kind = posture.get("kind")
    observation_type = f"metric:{metric_name}"
    if kind == "unavailable_with_reason":
        accumulator.add_unit(
            field="unavailable_with_reason_states",
            subject=subject,
            observation_type=observation_type,
            record=record,
            policy=policy,
            context=context,
        )
        return
    if kind == "not_attempted":
        accumulator.add_unit(
            field="not_attempted_states",
            subject=subject,
            observation_type=observation_type,
            record=record,
            policy=policy,
            context=context,
        )
        return
    if kind != "observed":
        return
    if derived:
        accumulator.add_unit(
            field="derived_analytical_values",
            subject=subject,
            observation_type=observation_type,
            record=record,
            policy=policy,
            context=context,
        )
        return
    meaningful, current, historical = _fragrantica_vote_status(record, observation)
    if not meaningful:
        added = accumulator.add_unit(
            field="excluded_invalid_observed_metric_values",
            subject=subject,
            observation_type=observation_type,
            record=record,
            policy=policy,
            context=context,
        )
        if added and historical:
            accumulator.increment("historical_unqualified_metric_values", context)
        return
    added = accumulator.add_unit(
        field="directly_observed_atomic_metric_values",
        subject=subject,
        observation_type=observation_type,
        record=record,
        policy=policy,
        context=context,
    )
    if added and current:
        accumulator.increment("current_policy_qualified_direct_metric_values", context)
    if added and historical:
        accumulator.increment("historical_unqualified_metric_values", context)


def _classify_record(
    accumulator: _Accumulator,
    record: Mapping[str, Any],
    *,
    lane: str,
    manifest_by_packet: Mapping[str, Mapping[str, Any]],
) -> None:
    payload = record.get("payload")
    if not isinstance(payload, Mapping):
        context = _context(record, {}, lane=lane, manifest_by_packet=manifest_by_packet)
        accumulator.increment("unclassified_silver_records", context)
        return
    if record.get("record_kind") == "entity":
        entity = payload.get("entity")
        if not isinstance(entity, Mapping):
            context = _context(record, {}, lane=lane, manifest_by_packet=manifest_by_packet)
            accumulator.increment("unclassified_silver_records", context)
            return
        context = _context(record, entity, lane=lane, manifest_by_packet=manifest_by_packet)
        accumulator.increment("identity_entity_records", context)
        accumulator.remember_subject(
            {"ref_type": "entity_key", "ref": entity.get("entity_key")}
        )
        return
    if record.get("record_kind") == "relationship":
        # Relationship records (corrections, supersessions, tombstones) carry a
        # payload.relationship edge, not an observation; they are counted as
        # edges, never as unclassified observation units.
        relationship = payload.get("relationship")
        context = _context(
            record,
            relationship if isinstance(relationship, Mapping) else {},
            lane=lane,
            manifest_by_packet=manifest_by_packet,
        )
        accumulator.increment("relationship_edge_records", context)
        return
    observation = payload.get("observation") if isinstance(payload, Mapping) else None
    if not isinstance(observation, Mapping):
        context = _context(record, {}, lane=lane, manifest_by_packet=manifest_by_packet)
        accumulator.increment("unclassified_silver_records", context)
        return
    context = _context(record, observation, lane=lane, manifest_by_packet=manifest_by_packet)
    policy = context["policy_version"]
    accumulator.remember_subject(observation.get("subject"))
    payload_kind = record.get("payload_kind")
    if payload_kind == "MetricObservation":
        posture = observation.get("metric_posture")
        if isinstance(posture, Mapping):
            _add_metric(
                accumulator,
                record=record,
                observation=observation,
                subject=observation.get("subject"),
                metric_name=str(observation.get("metric_name") or "<missing>"),
                posture=posture,
                policy=policy,
                context=context,
                derived=_metric_is_derived(record, observation),
            )
        return
    if payload_kind == "MetricObservationSet":
        for row in observation.get("rows", []):
            if not isinstance(row, Mapping):
                continue
            subject = row.get("subject")
            accumulator.add_unit(
                field="content_observations",
                subject=subject,
                observation_type=f"content:{observation.get('observation_set_kind') or 'set_row'}",
                record=record,
                policy=policy,
                context=context,
            )
            metrics = row.get("metrics")
            if not isinstance(metrics, Mapping):
                continue
            for metric_name, cell in sorted(metrics.items()):
                if not isinstance(cell, Mapping) or not isinstance(cell.get("metric_posture"), Mapping):
                    continue
                _add_metric(
                    accumulator,
                    record=record,
                    observation=cell,
                    subject=subject,
                    metric_name=str(metric_name),
                    posture=cell["metric_posture"],
                    policy=policy,
                    context=context,
                    derived=False,
                )
        return
    if payload_kind == "TextObservation":
        accumulator.add_unit(
            field="text_observations",
            subject=observation.get("subject"),
            observation_type=f"text:{observation.get('text_artifact_type') or 'text'}",
            record=record,
            policy=policy,
            context=context,
        )
        return
    if payload_kind == "TextObservationSet":
        parent = observation.get("subject")
        for row in observation.get("rows", []):
            if not isinstance(row, Mapping):
                continue
            subject = row.get("subject") or {"parent": parent, "row_id": row.get("row_id")}
            accumulator.add_unit(
                field="text_observations",
                subject=subject,
                observation_type=f"text:{row.get('text_artifact_type') or 'text'}",
                record=record,
                policy=policy,
                context=context,
            )
        return
    if payload_kind == "MetricRollupObservation":
        subject = observation.get("subject")
        metric_rollups = observation.get("metric_rollups")
        if isinstance(metric_rollups, Mapping):
            for metric_name, cell in sorted(metric_rollups.items()):
                if not isinstance(cell, Mapping) or not isinstance(cell.get("metric_posture"), Mapping):
                    continue
                _add_metric(
                    accumulator,
                    record=record,
                    observation=cell,
                    subject=subject,
                    metric_name=str(metric_name),
                    posture=cell["metric_posture"],
                    policy=policy,
                    context=context,
                    derived=True,
                )


def _eligible(manifest: Mapping[str, Any], selectors: tuple[tuple[str, str | None], ...]) -> bool:
    family = str(manifest.get("source_family") or "")
    surface = str(manifest.get("source_surface") or "")
    return any(family == wanted and (prefix is None or surface.startswith(prefix)) for wanted, prefix in selectors)


def _lane_states(
    lane_counts: Mapping[str, int], manifests: list[dict[str, Any]], marker_counts: Mapping[str, int]
) -> list[dict[str, Any]]:
    states: list[dict[str, Any]] = []
    for lane in sorted(SILVER_LANES):
        role = role_of(lane)
        record_count = lane_counts.get(lane, 0)
        selectors = _LANE_APPLICABILITY.get(lane, ())
        candidates = [manifest for manifest in manifests if _eligible(manifest, selectors)]
        failed = sum(1 for manifest in candidates if _manifest_failed(manifest))
        if role is LaneRole.RETIRED_SILVER_LINEAGE:
            state = "retired"
        elif record_count:
            state = "populated"
        elif not selectors:
            state = "intentionally_inactive"
        elif not candidates:
            state = "no_applicable_source"
        elif failed == len(candidates):
            state = "failed"
        else:
            state = "pending_backlog"
        states.append(
            {
                "lane": lane,
                "role": role.value if role is not None else "unknown",
                "state": state,
                "record_count": record_count,
                "eligible_capture_packets": len(candidates),
                "failed_eligible_capture_packets": failed,
                "derivation": "registry_role_plus_stored_records_plus_raw_manifest_applicability_v0",
            }
        )
    marker_candidates = [manifest for manifest in manifests if _eligible(manifest, _DEEP_CAPTURE_APPLICABILITY)]
    states.append(
        {
            "lane": _DEEP_CAPTURE_SET_LANE,
            "role": LaneRole.COMPLETION_MARKER.value,
            "state": "populated" if sum(marker_counts.values()) else "no_applicable_source",
            "record_count": sum(marker_counts.values()),
            "current_source_backed_record_count": marker_counts.get("current", 0),
            "historical_audit_only_record_count": marker_counts.get("audit_only", 0),
            "invalid_current_record_count": marker_counts.get("invalid_current", 0),
            "eligible_capture_packets": len(marker_candidates),
            "failed_eligible_capture_packets": sum(
                1 for manifest in marker_candidates if _manifest_failed(manifest)
            ),
            "derivation": "completion_marker_member_envelope_and_exact_raw_ref_resolution_v0",
        }
    )
    return states


def _group_output(groups: Mapping[str, Counter[str]]) -> list[dict[str, Any]]:
    return [{"key": key, **{field: counts[field] for field in _ADDITIVE_FIELDS}} for key, counts in sorted(groups.items())]


def _reconciles(total: Counter[str], groups: Mapping[str, Counter[str]]) -> bool:
    return all(sum(counts[field] for counts in groups.values()) == total[field] for field in _ADDITIVE_FIELDS)


def build_silver_observation_census(data_root: Any) -> dict[str, Any]:
    """Build one census from a verified ``DataLakeRoot`` without writing."""
    root = Path(data_root.path)
    epoch = _epoch(root)
    manifests, errors, times, fingerprint_parts = _scan_manifests(root)
    manifest_by_packet = {
        str(manifest.get("packet_id")): manifest
        for manifest in manifests
        if isinstance(manifest.get("packet_id"), str)
    }
    accumulator = _Accumulator()
    creator_metric_lineage = build_creator_metric_lineage_index(data_root)
    creator_metric_lanes = {
        CREATOR_METRIC_OBSERVATION_LANE,
        CREATOR_METRIC_ROLLUP_LANE,
    }
    creator_metric_status_fields = {
        CREATOR_METRIC_SOURCE_BACKED_COMPLETE: "creator_metric_source_backed_complete_records",
        CREATOR_METRIC_HISTORICAL_COMPATIBLE: "creator_metric_historical_compatible_records",
        CREATOR_METRIC_EXCLUDED: "creator_metric_excluded_records",
    }
    lane_counts: Counter[str] = Counter()
    marker_counts: Counter[str] = Counter()
    audit_only_residuals: list[dict[str, Any]] = []
    derived = root / "derived"
    if derived.is_dir():
        for lane in sorted(SILVER_LANES):
            for path in sorted(derived.glob(f"*/*/{lane}/*")):
                if not path.is_file():
                    continue
                relative = path.relative_to(root).as_posix()
                stat = path.stat()
                fingerprint_parts.append(f"{relative}\0{stat.st_size}\0{stat.st_mtime_ns}")
                lane_counts[lane] += 1
                try:
                    record = json.loads(path.read_text(encoding="utf-8"))
                    if not isinstance(record, dict):
                        raise ValueError("Silver record is not a JSON object")
                except (OSError, ValueError, TypeError) as exc:
                    context = {
                        "lane": lane,
                        "source_family": "unreadable",
                        "policy_version": "unreadable",
                        "observation_window": "unreadable",
                    }
                    accumulator.increment("silver_records", context)
                    accumulator.increment("unclassified_silver_records", context)
                    errors.append(
                        {"kind": "silver_record_unreadable", "path": relative, "error": f"{type(exc).__name__}: {exc}"}
                    )
                    times.append(datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc))
                    continue
                times.extend(_known_time_values(record))
                observation = (
                    record.get("payload", {}).get("observation", {})
                    if isinstance(record.get("payload"), Mapping)
                    else {}
                )
                context = _context(record, observation, lane=lane, manifest_by_packet=manifest_by_packet)
                accumulator.increment("silver_records", context)
                if role_of(lane) is LaneRole.RETIRED_SILVER_LINEAGE:
                    accumulator.increment("retired_audit_only_silver_records", context)
                    audit_only_residuals.append(
                        {
                            "kind": "retired_audit_only",
                            "lane": lane,
                            "path": relative,
                            "reason": "registered retired_silver_lineage bytes are audit-only",
                        }
                    )
                    continue
                if record.get("schema_version") != SILVER_VAULT_RECORD_SCHEMA_VERSION:
                    if lane in _DEEP_CAPTURE_SILVER_LANES:
                        accumulator.increment("deep_capture_historical_audit_only_records", context)
                        audit_only_residuals.append(
                            {
                                "kind": "historical_audit_only",
                                "lane": lane,
                                "path": relative,
                                "reason": "legacy deep-capture record lacks silver_vault_record_v0 envelope and exact raw refs",
                            }
                        )
                        continue
                    accumulator.increment("unclassified_silver_records", context)
                    continue
                authority = classify_silver_vault_record_sources(
                    data_root,
                    record,
                    record_path=path,
                    creator_metric_lineage=creator_metric_lineage,
                )
                if authority.status in {INVALID_SILVER_AUTHORITY, "unresolved"}:
                    accumulator.increment("unclassified_silver_records", context)
                    errors.append(
                        {
                            "kind": (
                                "silver_record_invalid"
                                if authority.status == INVALID_SILVER_AUTHORITY
                                else "silver_record_source_unresolved"
                            ),
                            "path": relative,
                            "reason_code": authority.reason_code,
                            "error": authority.error or authority.reason_code,
                        }
                    )
                    continue
                if authority.status == HISTORICAL_COMPATIBLE_AUTHORITY:
                    accumulator.increment("historical_compatible_silver_records", context)
                    if lane in creator_metric_lanes:
                        lineage = creator_metric_lineage.classification_for_path(path)
                        accumulator.increment(
                            creator_metric_status_fields[lineage.status], context
                        )
                    continue
                if authority.status != CURRENT_SOURCE_BACKED_AUTHORITY:
                    raise AssertionError(f"unknown Silver authority status: {authority}")
                accumulator.increment("current_source_backed_silver_records", context)
                if lane in _DEEP_CAPTURE_SILVER_LANES:
                    if not silver_raw_refs_bound_to_own_anchor(record):
                        accumulator.increment("unclassified_silver_records", context)
                        errors.append(
                            {
                                "kind": "deep_capture_source_ref_unresolved",
                                "path": relative,
                                "error": "Silver raw_refs cite a packet other than the record's own raw_anchor",
                            }
                        )
                        continue
                    accumulator.increment("deep_capture_current_source_backed_records", context)
                if lane in creator_metric_lanes:
                    lineage = creator_metric_lineage.classification_for_path(path)
                    accumulator.increment(creator_metric_status_fields[lineage.status], context)
                    if lineage.current_source_backed_eligible:
                        accumulator.increment("current_source_backed_creator_metric_records", context)
                    else:
                        # The record remains in the stored-record and lineage
                        # classification totals, but its observation values are
                        # not current source-backed census evidence.
                        continue
                _classify_record(
                    accumulator,
                    record,
                    lane=lane,
                    manifest_by_packet=manifest_by_packet,
                )

        for marker_path in sorted(derived.glob(f"*/*/{_DEEP_CAPTURE_SET_LANE}/*")):
            if not marker_path.is_file():
                continue
            relative = marker_path.relative_to(root).as_posix()
            marker_stat = marker_path.stat()
            fingerprint_parts.append(
                f"{relative}\0{marker_stat.st_size}\0{marker_stat.st_mtime_ns}"
            )
            times.append(datetime.fromtimestamp(marker_stat.st_mtime, tz=timezone.utc))
            raw_anchor = marker_path.parents[1].name
            try:
                marker = json.loads(marker_path.read_text(encoding="utf-8"))
            except (OSError, ValueError, TypeError):
                marker = {}
            current_member = False
            envelope_member_present = False
            try:
                marker_complete = data_root.is_record_set_complete(
                    subtree="derived",
                    raw_anchor=raw_anchor,
                    record_id=marker_path.name,
                    completion_lane=_DEEP_CAPTURE_SET_LANE,
                )
            except Exception:  # noqa: BLE001 - classified below as invalid current state
                marker_complete = False
            for lane in marker.get("member_lanes", []) if isinstance(marker, Mapping) else []:
                if lane not in _DEEP_CAPTURE_SILVER_LANES:
                    continue
                member_path = marker_path.parents[1] / lane / marker_path.name
                try:
                    member = json.loads(member_path.read_text(encoding="utf-8"))
                except (OSError, ValueError, TypeError):
                    continue
                if not isinstance(member, Mapping):
                    continue
                if member.get("schema_version") == SILVER_VAULT_RECORD_SCHEMA_VERSION:
                    envelope_member_present = True
                try:
                    validate_silver_vault_record(member)
                except (TypeError, ValueError):
                    continue
                try:
                    verify_silver_vault_record_sources(data_root, member)
                except (TypeError, ValueError):
                    continue
                if (
                    marker_complete
                    and member.get("raw_anchor") == raw_anchor
                    and member.get("record_id") == marker_path.name
                    and member.get("lane_namespace") == lane
                    and silver_raw_refs_bound_to_own_anchor(member)
                ):
                    current_member = True
                    break
            if current_member:
                marker_counts["current"] += 1
                accumulator.increment(
                    "deep_capture_current_completion_markers",
                    {"lane": _DEEP_CAPTURE_SET_LANE, "source_family": "instagram_creator", "policy_version": "current_source_backed", "observation_window": "unknown"},
                )
            elif not envelope_member_present:
                marker_counts["audit_only"] += 1
                accumulator.increment(
                    "deep_capture_historical_audit_only_completion_markers",
                    {"lane": _DEEP_CAPTURE_SET_LANE, "source_family": "instagram_creator", "policy_version": "historical_audit_only", "observation_window": "unknown"},
                )
                audit_only_residuals.append(
                    {
                        "kind": "historical_audit_only",
                        "lane": _DEEP_CAPTURE_SET_LANE,
                        "path": relative,
                        "reason": "completion marker points only to legacy unsupported deep-capture members",
                    }
                )
            else:
                marker_counts["invalid_current"] += 1
                errors.append(
                    {
                        "kind": "deep_capture_completion_marker_invalid_current",
                        "path": relative,
                        "error": "official envelope member or completion proof failed exact source-backed validation",
                    }
                )

    accumulator.errors.extend(errors)
    times.extend(_known_time_values(epoch))
    if not times:
        raise ValueError(f"Silver census could not derive an as-of time from {root}")
    snapshot_fingerprint = hashlib.sha256("\n".join(sorted(fingerprint_parts)).encode("utf-8")).hexdigest()
    totals = {field: accumulator.totals[field] for field in _ADDITIVE_FIELDS}
    totals.update(
        {
            "capture_packets": len(manifests) + sum(1 for error in errors if error["kind"] == "raw_manifest_unreadable"),
            "unique_subjects": len(accumulator.subjects),
            "unique_content_objects": len(accumulator.content_objects),
            "unique_accounts": len(accumulator.accounts),
            "unique_products": len(accumulator.products),
        }
    )
    capture_by_family = Counter(str(manifest.get("source_family") or "missing") for manifest in manifests)
    capture_by_family["unreadable"] += sum(1 for error in errors if error["kind"] == "raw_manifest_unreadable")
    reconciliation = {
        f"additive_totals_equal_{dimension}_breakdown": _reconciles(accumulator.totals, groups)
        for dimension, groups in accumulator.groups.items()
    }
    if not all(reconciliation.values()):
        raise AssertionError(f"Silver census reconciliation failed: {reconciliation}")
    lineage_reconciliation = creator_metric_lineage.reconciliation()
    if not lineage_reconciliation["exact_reconciliation"]:
        raise AssertionError(
            f"creator-metric lineage reconciliation failed: {lineage_reconciliation}"
        )
    return {
        "schema_version": CENSUS_SCHEMA_VERSION,
        "counting_unit": "unique subject + observation type/metric + observed time + policy + lineage anchor",
        "lake": {
            "root_uuid": data_root.root_uuid,
            "lake_epoch": epoch.get("lake_epoch"),
            "epoch_policy": epoch.get("epoch_policy"),
            "as_of": _timestamp_z(max(times)),
            "snapshot_fingerprint_sha256": snapshot_fingerprint,
        },
        "totals": totals,
        "capture_packets_by_source_family": [
            {"source_family": family, "capture_packets": count}
            for family, count in sorted(capture_by_family.items())
            if count
        ],
        "breakdowns": {
            f"by_{dimension}": _group_output(groups)
            for dimension, groups in accumulator.groups.items()
        },
        "lane_states": _lane_states(lane_counts, manifests, marker_counts),
        "creator_metric_lineage": lineage_reconciliation,
        "reconciliation": reconciliation,
        "errors": sorted(accumulator.errors, key=lambda item: _canonical(item)),
        "audit_only_residuals": sorted(audit_only_residuals, key=lambda item: _canonical(item)),
    }


__all__ = [
    "CENSUS_SCHEMA_VERSION",
    "FRAGRANTICA_REVIEW_VOTE_POLICY_VERSION",
    "build_silver_observation_census",
]
