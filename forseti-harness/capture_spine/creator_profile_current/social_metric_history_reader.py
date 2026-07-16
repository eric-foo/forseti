"""Policy-pinned by-key reader for packet-grain social metric histories.

Availability is discovery only.  Authority remains the deterministic Silver
record under each raw packet anchor; no derived-retrieval view or "latest"
sibling guess participates in selection.
"""
from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Any

from capture_spine.creator_profile_current.silver_envelope_core import content_hash
from data_lake.silver_record import (
    METRIC_OBSERVATION_SET_PAYLOAD_KIND,
    validate_silver_vault_record,
    verify_silver_vault_record_sources,
)

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


@dataclass(frozen=True)
class SocialMetricHistoryPoint:
    raw_anchor: str
    observed_at: str
    platform: str
    account_native_id: str
    content_native_id: str
    source_position: int | None
    metrics: dict[str, dict[str, Any]]


def read_social_metric_history(
    *,
    data_root: "DataLakeRoot",
    lane: str,
    policy_fingerprint: str,
    record_id_for_anchor: Any,
    platform: str,
    account_native_id: str,
    content_native_ids: Iterable[str],
    raw_anchors: Iterable[str] | None = None,
) -> dict[str, list[SocialMetricHistoryPoint]]:
    """Return ordered histories for the requested platform-native content IDs.

    ``policy_fingerprint`` and ``record_id_for_anchor`` are mandatory selection
    inputs.  A record for any other policy lives at a different deterministic
    record id and is simply absent here; a record found at the exact-policy path
    whose embedded record_id or policy fingerprint disagrees is a misfiled or
    tampered record and fails the read loudly, as does any malformed or
    integrity-invalid exact-policy record.
    """
    requested = {str(value).strip() for value in content_native_ids if str(value).strip()}
    histories: dict[str, list[SocialMetricHistoryPoint]] = defaultdict(list)
    anchors = (
        sorted(set(raw_anchors))
        if raw_anchors is not None
        else data_root.list_available(source_family=platform)
    )
    for raw_anchor in anchors:
        record_id = record_id_for_anchor(raw_anchor, policy_fingerprint=policy_fingerprint)
        path = data_root.record_path(
            subtree="derived",
            raw_anchor=raw_anchor,
            lane=lane,
            record_id=record_id,
        )
        if not path.is_file():
            continue
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ValueError(f"unreadable social metric Silver record {path}: {exc}") from exc
        if not isinstance(record, Mapping):
            raise ValueError(f"social metric Silver record is not an object: {path}")
        validate_silver_vault_record(record)
        verify_silver_vault_record_sources(data_root, record, record_path=path)
        expected_hash = f"sha256:{content_hash(dict(record))}"
        if record.get("content_hash") != expected_hash:
            raise ValueError(f"social metric Silver content hash mismatch: {path}")
        if record.get("raw_anchor") != raw_anchor:
            raise ValueError(f"social metric Silver raw_anchor mismatch: {path}")
        if record.get("payload_kind") != METRIC_OBSERVATION_SET_PAYLOAD_KIND:
            raise ValueError(f"unexpected social metric Silver payload kind: {path}")
        if record.get("record_id") != record_id:
            raise ValueError(f"social metric Silver record_id mismatch: {path}")
        observation = record["payload"]["observation"]
        if observation.get("policy_fingerprint_sha256") != policy_fingerprint:
            raise ValueError(
                "social metric Silver record at the exact-policy path carries a "
                f"different policy fingerprint: {path}"
            )
        if observation.get("platform") != platform:
            continue
        account_ref = observation.get("subject", {}).get("ref", {})
        if account_ref.get("native_id") != account_native_id:
            continue
        _validate_source_backed_lineage(record, raw_anchor=raw_anchor)
        observed_at = _required_utc(record.get("observed_at"), path=str(path))
        for row in observation["rows"]:
            native_id = str(row["subject"]["ref"]["native_id"])
            if native_id not in requested:
                continue
            histories[native_id].append(
                SocialMetricHistoryPoint(
                    raw_anchor=raw_anchor,
                    observed_at=observed_at,
                    platform=platform,
                    account_native_id=account_native_id,
                    content_native_id=native_id,
                    source_position=row.get("source_position"),
                    metrics={name: dict(metric) for name, metric in row["metrics"].items()},
                )
            )
    for native_id, points in histories.items():
        points.sort(key=lambda point: (_parse_utc(point.observed_at), point.raw_anchor))
        for prior, current in zip(points, points[1:]):
            if _parse_utc(prior.observed_at) == _parse_utc(current.observed_at):
                raise ValueError(
                    "ambiguous equal-time social metric observations for "
                    f"{platform}/{account_native_id}/{native_id}: "
                    f"{prior.raw_anchor}, {current.raw_anchor}"
                )
    return {native_id: histories.get(native_id, []) for native_id in sorted(requested)}


def _validate_source_backed_lineage(record: Mapping[str, Any], *, raw_anchor: str) -> None:
    raw_refs = record.get("raw_refs")
    if not isinstance(raw_refs, list) or not raw_refs:
        raise ValueError("social metric Silver record requires source-backed raw_refs")
    if not any(
        isinstance(ref, Mapping)
        and ref.get("packet_id") == raw_anchor
        and isinstance(ref.get("file_id"), str)
        and isinstance(ref.get("sha256"), str)
        for ref in raw_refs
    ):
        raise ValueError("social metric Silver lineage does not bind its raw anchor")


def _parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"timestamp must carry a UTC offset: {value!r}")
    return parsed


def _required_utc(value: object, *, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"social metric Silver record lacks observed_at: {path}")
    _parse_utc(value)
    return value


__all__ = ["SocialMetricHistoryPoint", "read_social_metric_history"]
