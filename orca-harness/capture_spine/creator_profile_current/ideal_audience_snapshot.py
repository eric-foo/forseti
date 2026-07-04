"""Build and validate creator ideal-audience profile snapshots.

The snapshot is the registry-facing envelope around the existing Tier-1
``IdealAudienceProfile`` model. It adds subject/join metadata and keeps the
profile body intact so multi-pillar results are not flattened into a single
claim.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from copy import deepcopy
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from schemas.audience_inference_models import EvidenceRecord, IdealAudienceProfile, OutputField
from scoring.audience_fusion import FUSION_CONFIG_VERSION, fuse_profile

SNAPSHOT_SCHEMA_VERSION = "creator_ideal_audience_profile_snapshot_v0"
SNAPSHOT_WRAPPER_KEY = "creator_ideal_audience_profile_snapshot"

_ALLOWED_DOCUMENT_KEYS = frozenset({SNAPSHOT_WRAPPER_KEY})
_ALLOWED_WRAPPER_KEYS = frozenset({"schema_version", "generated_at_utc", "profiles"})
_ALLOWED_SNAPSHOT_KEYS = frozenset(
    {
        "schema_version",
        "audience_profile_snapshot_id",
        "profile_subject_kind",
        "profile_subject_id",
        "platform_account_ids",
        "creator_record_id_or_none",
        "platform_scope",
        "observation_window_start",
        "observation_window_end",
        "actual_audience",
        "tier_1_profile",
        "tier_2a_profile_or_none",
        "evidence_ids",
        "fusion_config_version",
        "computed_at",
        "limitations",
        "ideal_audience_profile",
    }
)
_ALLOWED_SUBJECT_KINDS = frozenset({"platform_account", "creator_record"})
_ALLOWED_PLATFORM_SCOPES = frozenset({"instagram", "tiktok", "youtube", "cross_platform"})


def load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON document must be an object: {path}")
    return value


def dump_creator_ideal_audience_snapshot_document(document: Mapping[str, Any]) -> str:
    return json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def load_evidence_records(path: str | Path) -> list[EvidenceRecord]:
    value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if isinstance(value, Mapping):
        records = value.get("evidence_records")
    else:
        records = value
    if not _is_list(records) or not records:
        raise ValueError("evidence input must be a non-empty list or an object with evidence_records")
    try:
        return [EvidenceRecord.model_validate(record) for record in records]
    except ValidationError as exc:
        raise ValueError(f"invalid evidence record input: {exc}") from exc


def build_creator_ideal_audience_profile_snapshot_from_evidence(
    evidence: Sequence[EvidenceRecord],
    *,
    profile_subject_kind: str,
    profile_subject_id: str,
    platform_account_ids: Sequence[str] | None = None,
    creator_record_id_or_none: str | None = None,
    platform_scope: str | None = None,
    observation_window_start: str,
    observation_window_end: str,
    computed_at: str | None = None,
    snapshot_id: str | None = None,
    fusion_config_version: str = FUSION_CONFIG_VERSION,
    limitations: Sequence[str] | None = None,
) -> dict[str, Any]:
    records = list(evidence)
    if not records:
        raise ValueError("at least one evidence record is required")
    profile = fuse_profile(records, fusion_config_version=fusion_config_version, generated_at=computed_at)
    return build_creator_ideal_audience_profile_snapshot_from_profile(
        profile,
        profile_subject_kind=profile_subject_kind,
        profile_subject_id=profile_subject_id,
        platform_account_ids=platform_account_ids,
        creator_record_id_or_none=creator_record_id_or_none,
        platform_scope=platform_scope,
        observation_window_start=observation_window_start,
        observation_window_end=observation_window_end,
        evidence_ids=sorted({record.evidence_id for record in records}),
        snapshot_id=snapshot_id,
        limitations=limitations,
    )


def build_creator_ideal_audience_profile_snapshot_from_profile(
    profile: IdealAudienceProfile,
    *,
    profile_subject_kind: str,
    profile_subject_id: str,
    platform_account_ids: Sequence[str] | None,
    creator_record_id_or_none: str | None,
    platform_scope: str | None,
    observation_window_start: str,
    observation_window_end: str,
    evidence_ids: Sequence[str],
    snapshot_id: str | None = None,
    limitations: Sequence[str] | None = None,
) -> dict[str, Any]:
    subject_kind = _require_allowed(profile_subject_kind, _ALLOWED_SUBJECT_KINDS, "profile_subject_kind")
    subject_id = _non_empty_str(profile_subject_id, "profile_subject_id")
    if profile.creator_id != subject_id:
        raise ValueError("ideal-audience profile creator_id must match profile_subject_id")
    account_ids = [_non_empty_str(value, "platform_account_ids") for value in (platform_account_ids or [subject_id])]
    if len(account_ids) != len(set(account_ids)):
        raise ValueError("platform_account_ids must be unique")
    if subject_kind == "platform_account":
        if account_ids != [subject_id]:
            raise ValueError("platform_account snapshots must list only their own platform account")
        if creator_record_id_or_none is not None:
            raise ValueError("platform_account snapshots must not carry creator_record_id_or_none")
    else:
        if creator_record_id_or_none != subject_id:
            raise ValueError("creator_record snapshots must carry matching creator_record_id_or_none")
    scope = _require_allowed(platform_scope or _single_platform_scope(profile), _ALLOWED_PLATFORM_SCOPES, "platform_scope")
    evidence = [_non_empty_str(value, "evidence_ids") for value in evidence_ids]
    if not evidence:
        raise ValueError("evidence_ids must be non-empty")
    if len(evidence) != len(set(evidence)):
        raise ValueError("evidence_ids must be unique")

    profile_body = profile.model_dump(mode="json")
    snapshot = {
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
        "audience_profile_snapshot_id": snapshot_id
        or _snapshot_id(subject_id=subject_id, evidence_ids=evidence, profile_body=profile_body),
        "profile_subject_kind": subject_kind,
        "profile_subject_id": subject_id,
        "platform_account_ids": account_ids,
        "creator_record_id_or_none": creator_record_id_or_none,
        "platform_scope": scope,
        "observation_window_start": _non_empty_str(observation_window_start, "observation_window_start"),
        "observation_window_end": _non_empty_str(observation_window_end, "observation_window_end"),
        "actual_audience": profile.actual_audience,
        "tier_1_profile": _tier_1_profile(profile),
        "tier_2a_profile_or_none": None,
        "evidence_ids": evidence,
        "fusion_config_version": profile.fusion_config_version,
        "computed_at": profile.generated_at,
        "limitations": list(limitations or _default_limitations()),
        "ideal_audience_profile": profile_body,
    }
    validate_creator_ideal_audience_profile_snapshot(snapshot)
    return snapshot


def build_creator_ideal_audience_snapshot_document(
    profiles: Sequence[Mapping[str, Any]],
    *,
    generated_at_utc: str,
) -> dict[str, Any]:
    snapshots = [validate_creator_ideal_audience_profile_snapshot(profile) for profile in profiles]
    if not snapshots:
        raise ValueError("snapshot document requires at least one profile")
    return {
        SNAPSHOT_WRAPPER_KEY: {
            "schema_version": SNAPSHOT_SCHEMA_VERSION,
            "generated_at_utc": _non_empty_str(generated_at_utc, "generated_at_utc"),
            "profiles": snapshots,
        }
    }


def load_creator_ideal_audience_snapshot_document(path: str | Path) -> list[dict[str, Any]]:
    return validate_creator_ideal_audience_snapshot_document(load_json(path))


def validate_creator_ideal_audience_snapshot_document(document: Mapping[str, Any]) -> list[dict[str, Any]]:
    if SNAPSHOT_WRAPPER_KEY in document:
        _reject_unknown_keys(document, _ALLOWED_DOCUMENT_KEYS, "snapshot document")
        wrapper = document[SNAPSHOT_WRAPPER_KEY]
        if not isinstance(wrapper, Mapping):
            raise ValueError(f"{SNAPSHOT_WRAPPER_KEY} wrapper must be an object")
        _reject_unknown_keys(wrapper, _ALLOWED_WRAPPER_KEYS, SNAPSHOT_WRAPPER_KEY)
        _require(wrapper, ("schema_version", "generated_at_utc", "profiles"), SNAPSHOT_WRAPPER_KEY)
        if wrapper["schema_version"] != SNAPSHOT_SCHEMA_VERSION:
            raise ValueError("unexpected creator ideal-audience snapshot schema_version")
        _non_empty_str(wrapper["generated_at_utc"], "generated_at_utc")
        profiles = wrapper["profiles"]
    else:
        profiles = [document]
    if not _is_list(profiles) or not profiles:
        raise ValueError("snapshot document profiles must be a non-empty list")
    snapshots = [validate_creator_ideal_audience_profile_snapshot(profile) for profile in profiles]
    subject_ids = [snapshot["profile_subject_id"] for snapshot in snapshots]
    duplicates = sorted({subject_id for subject_id in subject_ids if subject_ids.count(subject_id) > 1})
    if duplicates:
        raise ValueError(f"duplicate ideal-audience snapshots for subject(s): {duplicates!r}")
    return snapshots


def validate_creator_ideal_audience_profile_snapshot(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(snapshot, Mapping):
        raise ValueError("ideal-audience profile snapshot must be an object")
    _reject_unknown_keys(snapshot, _ALLOWED_SNAPSHOT_KEYS, "ideal-audience profile snapshot")
    _require(snapshot, tuple(_ALLOWED_SNAPSHOT_KEYS), "ideal-audience profile snapshot")
    if snapshot["schema_version"] != SNAPSHOT_SCHEMA_VERSION:
        raise ValueError("unexpected ideal-audience profile snapshot schema_version")

    subject_kind = _require_allowed(snapshot["profile_subject_kind"], _ALLOWED_SUBJECT_KINDS, "profile_subject_kind")
    subject_id = _non_empty_str(snapshot["profile_subject_id"], "profile_subject_id")
    account_ids = _str_list(snapshot["platform_account_ids"], "platform_account_ids", allow_empty=False)
    creator_record_id = snapshot["creator_record_id_or_none"]
    if creator_record_id is not None:
        creator_record_id = _non_empty_str(creator_record_id, "creator_record_id_or_none")
    if subject_kind == "platform_account":
        if account_ids != [subject_id]:
            raise ValueError("platform_account snapshot subject must match its single platform_account_id")
        if creator_record_id is not None:
            raise ValueError("platform_account snapshot must not carry creator_record_id_or_none")
    else:
        if creator_record_id != subject_id:
            raise ValueError("creator_record snapshot subject must match creator_record_id_or_none")

    _non_empty_str(snapshot["audience_profile_snapshot_id"], "audience_profile_snapshot_id")
    _require_allowed(snapshot["platform_scope"], _ALLOWED_PLATFORM_SCOPES, "platform_scope")
    _non_empty_str(snapshot["observation_window_start"], "observation_window_start")
    _non_empty_str(snapshot["observation_window_end"], "observation_window_end")
    if snapshot["actual_audience"] != "not_estimated":
        raise ValueError("actual_audience must be not_estimated")
    if snapshot["tier_2a_profile_or_none"] is not None:
        raise ValueError("tier_2a_profile_or_none must stay null in v0")
    evidence_ids = _str_list(snapshot["evidence_ids"], "evidence_ids", allow_empty=False)
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError("evidence_ids must be unique")
    _non_empty_str(snapshot["fusion_config_version"], "fusion_config_version")
    _non_empty_str(snapshot["computed_at"], "computed_at")
    _str_list(snapshot["limitations"], "limitations", allow_empty=False)
    try:
        profile = IdealAudienceProfile.model_validate(snapshot["ideal_audience_profile"])
    except ValidationError as exc:
        raise ValueError(f"invalid ideal_audience_profile body: {exc}") from exc
    if profile.creator_id != subject_id:
        raise ValueError("ideal_audience_profile.creator_id must match profile_subject_id")
    if profile.actual_audience != snapshot["actual_audience"]:
        raise ValueError("snapshot actual_audience must match ideal_audience_profile.actual_audience")
    if profile.fusion_config_version != snapshot["fusion_config_version"]:
        raise ValueError("snapshot fusion_config_version must match ideal_audience_profile")
    if profile.generated_at != snapshot["computed_at"]:
        raise ValueError("snapshot computed_at must match ideal_audience_profile.generated_at")
    if _tier_1_profile(profile) != snapshot["tier_1_profile"]:
        raise ValueError("tier_1_profile does not match ideal_audience_profile")
    nested_ids = _nested_profile_evidence_ids(profile)
    missing_ids = sorted(nested_ids - set(evidence_ids))
    if missing_ids:
        raise ValueError(f"nested profile evidence ids missing from snapshot evidence_ids: {missing_ids!r}")
    return deepcopy(dict(snapshot))


def _tier_1_profile(profile: IdealAudienceProfile) -> dict[str, Any]:
    field_names = [field.value for field in OutputField]
    pillar_profiles: list[dict[str, Any]] = []
    for pillar in profile.ideal_audience_profiles:
        results = {field_name: None for field_name in field_names}
        for result in pillar.field_results:
            results[result.field.value] = {
                "label_or_none": None if result.label == "unknown" else result.label,
                "support_band": result.support_band.value,
                "uncalibrated_support_score": result.uncalibrated_support_score,
                "evidence_ids": list(result.evidence_ids),
                "counterevidence_ids": list(result.counterevidence_ids),
            }
        pillar_profiles.append(
            {
                "pillar_id": pillar.pillar_id,
                "pillar_label": pillar.pillar_label,
                "positioning_share": pillar.positioning_share,
                "field_results": results,
            }
        )
    return {"pillar_profiles": pillar_profiles}


def _nested_profile_evidence_ids(profile: IdealAudienceProfile) -> set[str]:
    ids: set[str] = set()
    for pillar in profile.ideal_audience_profiles:
        for result in pillar.field_results:
            ids.update(result.evidence_ids)
            ids.update(result.counterevidence_ids)
    return ids


def _single_platform_scope(profile: IdealAudienceProfile) -> str:
    platforms = {
        part
        for pillar in profile.ideal_audience_profiles
        for part in [pillar.pillar_label.split(":", 1)[0]]
        if part
    }
    if len(platforms) == 1:
        return next(iter(platforms))
    return "cross_platform"


def _snapshot_id(*, subject_id: str, evidence_ids: Sequence[str], profile_body: Mapping[str, Any]) -> str:
    basis = {
        "profile_subject_id": subject_id,
        "evidence_ids": list(evidence_ids),
        "profile_body": profile_body,
    }
    digest = hashlib.sha256(json.dumps(basis, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    return f"creator_ideal_audience_profile_snapshot:{subject_id}:{digest[:16]}"


def _default_limitations() -> list[str]:
    return [
        "Ideal-audience profile is a content-positioning best-fit read, not actual follower or buyer demographics.",
        "actual_audience is not_estimated; no actual-audience claim is made.",
        "Support scores are uncalibrated evidence strength, not measured accuracy.",
        "Tier-2A aggregate-audience demographics are omitted in this v0 snapshot.",
    ]


def _reject_unknown_keys(value: Mapping[str, Any], allowed: frozenset[str], context: str) -> None:
    unknown = sorted(set(str(key) for key in value) - allowed)
    if unknown:
        raise ValueError(f"unknown field(s) in {context}: {', '.join(unknown)}")


def _require(value: Mapping[str, Any], keys: Sequence[str], context: str) -> None:
    for key in keys:
        if key not in value:
            raise ValueError(f"{context} missing required field: {key}")


def _require_allowed(value: Any, allowed: frozenset[str], context: str) -> str:
    text = _non_empty_str(value, context)
    if text not in allowed:
        raise ValueError(f"{context} must be one of {sorted(allowed)!r}")
    return text


def _non_empty_str(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context} must be a non-empty string")
    return value


def _str_list(value: Any, context: str, *, allow_empty: bool) -> list[str]:
    if not _is_list(value) or (not allow_empty and not value):
        raise ValueError(f"{context} must be a list")
    result: list[str] = []
    for item in value:
        result.append(_non_empty_str(item, context))
    return result


def _is_list(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))
