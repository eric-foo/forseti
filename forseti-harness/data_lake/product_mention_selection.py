"""Exact-policy selection for current transcript-product-mention Silver records."""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Any, Mapping

from data_lake.sibling_selection import SiblingCandidate, select_current_record_per_subject
from data_lake.silver_record import (
    CURRENT_SOURCE_BACKED_AUTHORITY,
    SilverSourceAuthority,
    SilverRecordError,
    validate_silver_vault_record,
    verify_silver_vault_record_sources,
)

MENTIONS_LANE = "transcript_product_mentions_silver"


class ProductMentionPolicyError(ValueError):
    """The caller did not provide an exact product-mention policy identity."""


@dataclass(frozen=True)
class SelectedProductMentionRecord:
    raw_anchor: str
    record_id: str
    sha256: str
    subject_key: str
    record: dict[str, Any]

    @property
    def record_ref(self) -> str:
        return f"{self.raw_anchor}/{MENTIONS_LANE}/{self.record_id}"


@dataclass(frozen=True)
class ProductMentionSelectionResult:
    policy: dict[str, str]
    selected: tuple[SelectedProductMentionRecord, ...]
    residuals: tuple[dict[str, Any], ...]
    source_refs: tuple[str, ...]


def normalize_product_mention_policy(value: object) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise ProductMentionPolicyError("product-mention policy must be an object")
    version = value.get("policy_version")
    fingerprint = value.get("policy_fingerprint_sha256")
    if not isinstance(version, str) or not version.strip():
        raise ProductMentionPolicyError("policy_version must be a non-empty string")
    if not isinstance(fingerprint, str) or re.fullmatch(r"[0-9a-f]{64}", fingerprint) is None:
        raise ProductMentionPolicyError(
            "policy_fingerprint_sha256 must be lowercase 64-hex"
        )
    return {
        "policy_version": version.strip(),
        "policy_fingerprint_sha256": fingerprint,
    }


def _observation(record: Mapping[str, Any]) -> Mapping[str, Any] | None:
    payload = record.get("payload")
    observation = payload.get("observation") if isinstance(payload, Mapping) else None
    return observation if isinstance(observation, Mapping) else None


def _subject_key(raw_anchor: str, record: Mapping[str, Any]) -> str | None:
    observation = _observation(record)
    subject = observation.get("subject") if observation is not None else None
    ref = subject.get("ref") if isinstance(subject, Mapping) else None
    if not isinstance(ref, Mapping):
        return None
    identity = [
        raw_anchor,
        str(ref.get("namespace") or ""),
        str(ref.get("kind") or ""),
        str(ref.get("native_id") or ""),
    ]
    if any(not part for part in identity):
        return None
    provenance = record.get("provenance")
    provenance = provenance if isinstance(provenance, Mapping) else {}
    identity.extend(
        str(provenance.get(field) or "")
        for field in (
            "transcript_source_key",
            "source_route",
            "asr_record_id",
            "transcript_source",
        )
    )
    return json.dumps(identity, ensure_ascii=False, separators=(",", ":"))


def _residual(raw_anchor: str, record_id: str, status: str, **detail: Any) -> dict[str, Any]:
    return {
        "raw_anchor": raw_anchor,
        "record_id": record_id,
        "status": status,
        **detail,
    }


def select_product_mention_records(
    root,
    *,
    policy: Mapping[str, Any],
    preclassified_authority: Mapping[str, SilverSourceAuthority] | None = None,
) -> ProductMentionSelectionResult:
    """Select one exact-policy record per transcript evidence subject.

    Every file is selected or reported as a residual. Distinct same-policy
    siblings retain the shared selector's fail-closed error; path and model
    identity never silently order the choice.
    """
    normalized = normalize_product_mention_policy(policy)
    residuals: list[dict[str, Any]] = []
    source_refs: list[str] = []
    candidates: list[SiblingCandidate] = []

    for raw_anchor in sorted(root.list_available()):
        lane_dir = root.lane_dir(
            subtree="derived", raw_anchor=raw_anchor, lane=MENTIONS_LANE
        )
        if not lane_dir.is_dir():
            continue
        for record_file in sorted(path for path in lane_dir.iterdir() if path.is_file()):
            body = record_file.read_bytes()
            source_refs.append(f"{raw_anchor}/{MENTIONS_LANE}/{record_file.name}")
            try:
                record = json.loads(body.decode("utf-8"))
            except ValueError:
                record = None
            if not isinstance(record, dict):
                residuals.append(_residual(raw_anchor, record_file.name, "unreadable"))
                continue

            observation = _observation(record)
            actual_version = observation.get("policy_version") if observation else None
            actual_fingerprint = (
                observation.get("policy_fingerprint_sha256") if observation else None
            )
            if (
                not isinstance(actual_version, str)
                or not actual_version.strip()
                or not isinstance(actual_fingerprint, str)
                or re.fullmatch(r"[0-9a-f]{64}", actual_fingerprint) is None
            ):
                residuals.append(
                    _residual(
                        raw_anchor,
                        record_file.name,
                        "missing_or_invalid_policy_identity",
                    )
                )
                continue
            try:
                validate_silver_vault_record(record)
            except SilverRecordError:
                residuals.append(
                    _residual(raw_anchor, record_file.name, "invalid_silver_envelope")
                )
                continue
            record_ref = f"{raw_anchor}/{MENTIONS_LANE}/{record_file.name}"
            authority = (
                preclassified_authority.get(record_ref)
                if preclassified_authority is not None
                else None
            )
            try:
                if authority is None:
                    verify_silver_vault_record_sources(root, record)
                elif authority.status != CURRENT_SOURCE_BACKED_AUTHORITY:
                    detail = f": {authority.error}" if authority.error else ""
                    raise SilverRecordError(
                        "Silver source authority is "
                        f"{authority.status} ({authority.reason_code}){detail}"
                    )
            except SilverRecordError as exc:
                residuals.append(
                    _residual(
                        raw_anchor,
                        record_file.name,
                        "source_ref_unresolved",
                        error=str(exc),
                    )
                )
                continue
            if observation.get("observation_set_kind") != "transcript_product_mentions":
                residuals.append(
                    _residual(raw_anchor, record_file.name, "wrong_observation_set_kind")
                )
                continue
            if (
                actual_version != normalized["policy_version"]
                or actual_fingerprint != normalized["policy_fingerprint_sha256"]
            ):
                residuals.append(
                    _residual(
                        raw_anchor,
                        record_file.name,
                        "policy_mismatch",
                        actual_policy_version=actual_version,
                        actual_policy_fingerprint_sha256=actual_fingerprint,
                    )
                )
                continue
            subject_key = _subject_key(raw_anchor, record)
            if subject_key is None:
                residuals.append(
                    _residual(raw_anchor, record_file.name, "missing_selection_subject")
                )
                continue
            selected_record = SelectedProductMentionRecord(
                raw_anchor=raw_anchor,
                record_id=record_file.name,
                sha256=hashlib.sha256(body).hexdigest(),
                subject_key=subject_key,
                record=record,
            )
            candidates.append(
                SiblingCandidate(
                    subject_key=subject_key,
                    raw_anchor=raw_anchor,
                    record_ref=selected_record.record_ref,
                    content_hash=str(record["content_hash"]),
                    derivation_rank=0,
                    payload=selected_record,
                )
            )

    selected: list[SelectedProductMentionRecord] = []
    for _subject_key_value, result in sorted(
        select_current_record_per_subject(candidates).items()
    ):
        selected.append(result.selected.payload)
        residuals.extend(
            _residual(
                candidate.raw_anchor,
                candidate.payload.record_id,
                "same_policy_bypassed",
                selected_record_id=result.selected.payload.record_id,
            )
            for candidate in result.bypassed
        )
    return ProductMentionSelectionResult(
        policy=normalized,
        selected=tuple(selected),
        residuals=tuple(
            sorted(
                residuals,
                key=lambda row: (row["raw_anchor"], row["record_id"], row["status"]),
            )
        ),
        source_refs=tuple(sorted(source_refs)),
    )


__all__ = [
    "MENTIONS_LANE",
    "ProductMentionPolicyError",
    "ProductMentionSelectionResult",
    "SelectedProductMentionRecord",
    "normalize_product_mention_policy",
    "select_product_mention_records",
]
