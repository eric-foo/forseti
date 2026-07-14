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
from data_lake.silver_record import (
    SILVER_VAULT_RECORD_SCHEMA_VERSION,
    validate_silver_vault_record,
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
    "content_observations",
    "directly_observed_atomic_metric_values",
    "current_policy_qualified_direct_metric_values",
    "text_observations",
    "derived_analytical_values",
    "unavailable_with_reason_states",
    "not_attempted_states",
    "excluded_invalid_observed_metric_values",
    "historical_unqualified_metric_values",
    "unclassified_silver_records",
    "duplicate_observation_units_suppressed",
    "conflicting_observation_units",
)

# Mechanical applicability selectors used only when a registered current lane
# is empty.  A selector is (source_family, source_surface prefix or None).
# Populated lanes and retired lanes never depend on this table for their state.
_LANE_APPLICABILITY: dict[str, tuple[tuple[str, str | None], ...]] = {
    "cleaning_basenotes_silver": (("fragrance_native_database", "basenotes_"),),
    "cleaning_fragrantica_silver": (("fragrance_native_database", "fragrantica_"),),
    "cleaning_parfumo_silver": (("fragrance_native_database", "parfumo_"),),
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
    "tiktok_audience_evidence_silver": (
        ("tiktok", "tiktok_creator_batch_comment_subtitle_admission"),
    ),
    "retail_pdp_silver": (("fragrance_purchase_review_pdp", None),),
    "silver__capture__audience_comments": (("instagram_creator", None),),
    "silver__capture__reel_transcript": (("instagram_creator", None),),
    "silver__capture__reel_deep_capture__set": (("instagram_creator", None),),
}
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
    point = record.get("observed_at") or record.get("captured_at")
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
    lane_counts: Mapping[str, int], manifests: list[dict[str, Any]]
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
    lane_counts: Counter[str] = Counter()
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
                if record.get("schema_version") != SILVER_VAULT_RECORD_SCHEMA_VERSION:
                    accumulator.increment("unclassified_silver_records", context)
                    continue
                try:
                    validate_silver_vault_record(record)
                except (TypeError, ValueError) as exc:
                    accumulator.increment("unclassified_silver_records", context)
                    errors.append(
                        {"kind": "silver_record_invalid", "path": relative, "error": f"{type(exc).__name__}: {exc}"}
                    )
                    continue
                _classify_record(
                    accumulator,
                    record,
                    lane=lane,
                    manifest_by_packet=manifest_by_packet,
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
        "lane_states": _lane_states(lane_counts, manifests),
        "reconciliation": reconciliation,
        "errors": sorted(accumulator.errors, key=lambda item: _canonical(item)),
    }


__all__ = [
    "CENSUS_SCHEMA_VERSION",
    "FRAGRANTICA_REVIEW_VOTE_POLICY_VERSION",
    "build_silver_observation_census",
]
