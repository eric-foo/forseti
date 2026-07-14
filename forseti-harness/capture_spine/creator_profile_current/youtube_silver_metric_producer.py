"""Emit Silver Vault creator-metric records from the committed YouTube Shorts
fragrance creator-metric seed.

This producer makes YouTube creator metrics lake-native. Mirroring the merged
Instagram producer's Silver-envelope discipline
(``silver_metric_producer.py``), it re-emits each committed seed metric
observation and each per-account rollup as a formal Silver Vault derived record
(``record_kind: observation``) conforming to the Silver Vault record contract
(common header, content-hash discipline, posture/value coupling) and to the
sibling ``youtube_creator_metric_silver_record_contract_v0`` doc.

Number source -- resolved in scoping as Option 2 ("wrap the committed seed"):
the producer reads the committed
``youtube_shorts_fragrance_creator_metric_seed_v0.json`` and wraps its
``metric_observations`` + ``metric_rollups`` into Silver envelopes. It does NOT
recompute any metric. No-drift is therefore guaranteed by construction: the
emitted numbers ARE the committed, already-tested seed numbers.

Boundary: this producer does NOT compute metrics, does NOT regenerate the
``creator_profile_current`` read model (that is the separate reader lane), does
NOT introduce cross-platform creator identity, and does NOT write to the real
lake by itself -- callers pass a ``DataLakeRoot`` (tests use
``DataLakeRoot.for_test``); running it against the production lake is an
operational step outside this module.

Scope (v0), mirroring the IG slice:
- emits MetricObservation + MetricRollupObservation observation records only;
- does NOT emit entity or relationship records (the metric subject is carried as
  a self-describing ``entity_key`` reference);
- per-platform account subjects only; no cross-platform creator rollups.

YouTube-specific anchoring (resolved in scoping; an honest divergence from IG):
- Each committed YouTube observation carries its own real raw-packet id in
  ``source_packet_id_or_none`` (a Crockford-26 lake packet handle). Each
  MetricObservation Silver record anchors to that per-Short packet id, exactly
  as IG anchors to its projection packet.
- A per-account rollup's source observations span MULTIPLE distinct per-Short
  packets (28 of 30 accounts), so there is no single source packet to anchor the
  rollup to. The rollup anchors to its ``platform_account_id`` instead -- an
  honest account-scoped raw anchor for a multi-packet aggregate. (IG can share
  one packet across a rollup's observations; YouTube cannot.) Named residual.
- The YouTube seed carries NO IG-style ``raw_anchor`` dict
  (file_id/relative_packet_path/sha256). ``raw_refs`` are rebuilt honestly from
  the YouTube seed's own portable provenance fields (``source_pointer``,
  ``source_field``, ``source_file``, ``source_packet_id_or_none``) plus the
  captured watch/shorts HTML sha256s, which ARE the hash-checkable source
  material per the Silver Vault ``raw_refs`` rule.
- When requested, observation ``raw_refs`` are upgraded through the public Bronze
  source-surface catalog helper for YouTube watch Attachment Records. The join is
  packet id + body hash, because the seed does not carry packet-relative body
  paths; missing or ambiguous AR rows stay visible as lineage limitations.

Accepted residuals (named for review, not hidden):
- Derives from the committed proof seed JSON rather than recomputing from source
  review-inputs -- the doctrinal difference from IG, which reuses a live builder.
  Upgrade trigger: if the YouTube seed needs live recompute, extract a
  ``youtube_metric_seed.py`` builder (handoff Option 1) and have this producer
  reuse it.
- The Silver-envelope helpers (content hash, canonical JSON, posture coupling,
  fail-closed native-id) were previously duplicated from the IG producer; that
  named upgrade trigger has fired and both producers now import the shared
  ``silver_envelope_core`` (an extraction, not a redesign -- record bytes are
  unchanged).
- These records share the platform-agnostic ``creator_metric_silver`` /
  ``creator_metric_rollup_silver`` lanes with the IG producer (records stay
  distinguishable by ``source_family``/``source_surface``/subject namespace).
  Upgrade trigger: the owner/reader prefers per-platform lanes -- a constant
  change while records remain test-only (no real-lake migration).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping

from capture_spine.creator_profile_current.silver_envelope_core import (
    BASE_NON_CLAIMS as _BASE_NON_CLAIMS,
    CONTENT_HASH_BASIS as _CONTENT_HASH_BASIS,
    METRIC_OBSERVATION_LANE,
    METRIC_OBSERVATION_PAYLOAD_KIND,
    METRIC_ROLLUP_LANE,
    METRIC_ROLLUP_PAYLOAD_KIND,
    SILVER_VAULT_RECORD_SCHEMA_VERSION,
    SOURCE_FAMILY as _SOURCE_FAMILY,
    assert_posture_value_coupling as _assert_posture_value_coupling,
    content_hash as _content_hash,
    metric_posture as _metric_posture,
    require_source_packet_id as _require_source_packet_id,
    required_subject_native_id as _required_subject_native_id,
    rollup_metric as _rollup_metric,
)
from capture_spine.creator_profile_current.silver_subject_ref import (
    platform_account_ref_field as _platform_account_ref_field,
)
from harness_utils import generate_ulid
from data_lake.catalog import source_surface_catalog_rows
from data_lake.silver_record import append_silver_record

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


YOUTUBE_SEED_WRAPPER_KEY = "youtube_shorts_fragrance_creator_metric_seed"

# Default committed-seed location (repo-relative), so callers can wrap the real
# committed seed without re-deriving the path. Resolved from this module:
# forseti-harness/capture_spine/creator_profile_current/ -> repo root is parents[3].
DEFAULT_YOUTUBE_SEED_PATH = (
    Path(__file__).resolve().parents[3]
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "youtube"
    / "youtube_shorts_fragrance_creator_metric_seed_v0.json"
)

METRIC_OBSERVATION_PRODUCER_SCHEMA_VERSION = "youtube_creator_metric_silver_metricobservation_v1"
METRIC_ROLLUP_PRODUCER_SCHEMA_VERSION = "youtube_creator_metric_silver_metricrollupobservation_v1"

_OBS_PRODUCER_ID = (
    "forseti-harness.capture_spine.creator_profile_current.youtube_silver_metric_producer"
    ".derive_youtube_creator_metric_silver_records_from_seed#metric_observation"
)
_ROLLUP_PRODUCER_ID = (
    "forseti-harness.capture_spine.creator_profile_current.youtube_silver_metric_producer"
    ".derive_youtube_creator_metric_silver_records_from_seed#metric_rollup"
)
_PLATFORM_NAMESPACE = "youtube"
_SOURCE_SURFACE = "youtube_shorts"
_YOUTUBE_BRONZE_SOURCE_FAMILY = "youtube"
_YOUTUBE_BRONZE_SOURCE_SURFACE = "youtube_watch_metadata_comments"
_BRONZE_AR_RAW_REF_KIND = "bronze_attachment_record"
_RAW_PACKET_FALLBACK_MISSING_AR_REF_KIND = "raw_packet_fallback_missing_attachment_record"
_RAW_PACKET_FALLBACK_AMBIGUOUS_AR_REF_KIND = "raw_packet_fallback_ambiguous_attachment_record"
_MISSING_AR_LIMITATION = "typed_attachment_record_missing_for_raw_ref"
_AMBIGUOUS_AR_LIMITATION = "typed_attachment_record_ambiguous_for_raw_ref"

# The engagement/like/comment non-claim added on top of the shared base
# non-claims is CONDITIONAL: it is load-bearing for view-count-only records (the
# committed genesis seed), but must not attach to a record that actually carries
# an observed engagement-family metric (live watch-packet documents expose
# like/comment inputs) -- a false non-claim is an honesty bug, not caution.
_ENGAGEMENT_NON_CLAIM = "not an engagement-rate, like, or comment metric"
_ENGAGEMENT_OBSERVATION_METRIC_NAMES = frozenset({"like_count", "total_comment_count", "comment_count"})
_ENGAGEMENT_ROLLUP_METRIC_NAMES = frozenset(
    {"engagement_rate", "average_like_count", "average_comment_count"}
)


def _record_non_claims(*, engagement_bearing: bool) -> list[str]:
    claims = set(_BASE_NON_CLAIMS)
    if not engagement_bearing:
        claims.add(_ENGAGEMENT_NON_CLAIM)
    return sorted(claims)


@dataclass(frozen=True)
class YoutubeCreatorMetricSilverResult:
    """Outputs of one YouTube creator-metric Silver derivation."""

    observation_records: list[dict[str, Any]]
    observation_paths: list[Path]
    rollup_records: list[dict[str, Any]]
    rollup_paths: list[Path]
    seed_document: dict[str, Any]


def derive_youtube_creator_metric_silver_records_from_seed(
    *,
    data_root: "DataLakeRoot",
    seed_document: Mapping[str, Any],
    use_bronze_attachment_records: bool = False,
) -> YoutubeCreatorMetricSilverResult:
    """Wrap the committed YouTube creator-metric seed's observations + per-account
    rollups in Silver Vault envelopes and append them through the lake writer.

    Observations are appended first so each rollup can thread its source
    observation records' content hashes into ``derived_refs`` (the canonical
    Silver lineage, mirroring the IG producer)."""
    seed = seed_document[YOUTUBE_SEED_WRAPPER_KEY]
    bronze_attachment_records_by_packet_body_hash = (
        _bronze_attachment_records_by_packet_body_hash(data_root)
        if use_bronze_attachment_records
        else {}
    )

    observation_records: list[dict[str, Any]] = []
    observation_paths: list[Path] = []
    ref_by_seed_observation_id: dict[str, dict[str, str]] = {}
    for seed_observation in seed["metric_observations"]:
        record = build_metric_observation_record(
            seed_observation=seed_observation,
            bronze_attachment_records_by_packet_body_hash=(
                bronze_attachment_records_by_packet_body_hash
            ),
            use_bronze_attachment_records=use_bronze_attachment_records,
        )
        path = append_silver_record(
            data_root,
            raw_anchor=_require_source_packet_id(seed_observation),
            lane=METRIC_OBSERVATION_LANE,
            record_id=record["record_id"],
            record=record,
        )
        observation_records.append(record)
        observation_paths.append(path)
        ref_by_seed_observation_id[seed_observation["metric_observation_id"]] = {
            "raw_anchor": record["raw_anchor"],
            "lane_namespace": METRIC_OBSERVATION_LANE,
            "record_id": record["record_id"],
            "content_hash": record["content_hash"],
        }

    rollup_records: list[dict[str, Any]] = []
    rollup_paths: list[Path] = []
    for seed_rollup in seed["metric_rollups"]:
        rollup_raw_anchor = _rollup_raw_anchor(seed_rollup)
        record = build_metric_rollup_record(
            seed_rollup=seed_rollup,
            ref_by_seed_observation_id=ref_by_seed_observation_id,
            raw_anchor=rollup_raw_anchor,
        )
        path = append_silver_record(
            data_root,
            raw_anchor=rollup_raw_anchor,
            lane=METRIC_ROLLUP_LANE,
            record_id=record["record_id"],
            record=record,
        )
        rollup_records.append(record)
        rollup_paths.append(path)

    return YoutubeCreatorMetricSilverResult(
        observation_records=observation_records,
        observation_paths=observation_paths,
        rollup_records=rollup_records,
        rollup_paths=rollup_paths,
        seed_document=dict(seed_document),
    )


def derive_youtube_creator_metric_silver_records_from_seed_file(
    *,
    data_root: "DataLakeRoot",
    seed_path: str | Path = DEFAULT_YOUTUBE_SEED_PATH,
    use_bronze_attachment_records: bool = False,
) -> YoutubeCreatorMetricSilverResult:
    """Convenience wrapper: read the committed seed JSON from ``seed_path`` (the
    real committed seed by default) and derive Silver records from it. Uses
    ``utf-8-sig`` to tolerate a BOM, matching the seed's own test loader."""
    seed_document = json.loads(Path(seed_path).read_text(encoding="utf-8-sig"))
    return derive_youtube_creator_metric_silver_records_from_seed(
        data_root=data_root,
        seed_document=seed_document,
        use_bronze_attachment_records=use_bronze_attachment_records,
    )


def build_metric_observation_record(
    *,
    seed_observation: Mapping[str, Any],
    bronze_attachment_records_by_packet_body_hash: Mapping[
        tuple[str, str], list[Mapping[str, Any]]
    ] | None = None,
    use_bronze_attachment_records: bool = False,
) -> dict[str, Any]:
    """Wrap one committed seed metric observation in a Silver Vault
    MetricObservation record."""
    posture = seed_observation["metric_posture"]
    value = seed_observation.get("metric_value_or_none")
    reason = seed_observation.get("posture_reason_or_none")
    _assert_posture_value_coupling(
        posture=posture,
        value=value,
        reason=reason,
        what=f"observation {seed_observation.get('metric_observation_id')!r}",
    )
    observed_at = seed_observation["observed_at"]
    raw_ref = _raw_ref(
        seed_observation,
        bronze_attachment_records_by_packet_body_hash=(
            bronze_attachment_records_by_packet_body_hash or {}
        ),
        use_bronze_attachment_records=use_bronze_attachment_records,
    )
    lineage_limitations = _raw_ref_lineage_limitations(raw_ref)
    record: dict[str, Any] = {
        "record_id": f"{generate_ulid()}.json",
        "raw_anchor": _require_source_packet_id(seed_observation),
        "lane_namespace": METRIC_OBSERVATION_LANE,
        "producer_id": _OBS_PRODUCER_ID,
        "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "producer_schema_version": METRIC_OBSERVATION_PRODUCER_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": _CONTENT_HASH_BASIS,
        "record_kind": "observation",
        "payload_kind": METRIC_OBSERVATION_PAYLOAD_KIND,
        "producer_row_kind": "yt_media_metric",
        "source_family": _SOURCE_FAMILY,
        "source_surface": _SOURCE_SURFACE,
        "observed_at": observed_at,
        "captured_at": observed_at,
        "raw_refs": [raw_ref],
        "derived_refs": [],
        "payload": {
            "observation": {
                "subject": _observation_subject(seed_observation),
                "metric_name": seed_observation["metric_name"],
                "metric_value": value,
                "metric_posture": _metric_posture(posture, reason),
                "coverage_window": {
                    "start": seed_observation.get("capture_window_start_or_none"),
                    "end": seed_observation.get("capture_window_end_or_none"),
                },
                "source_surface": _SOURCE_SURFACE,
                "source_publication_or_event": seed_observation.get(
                    "content_publication_or_event_time_or_none"
                ),
                "unit": seed_observation["metric_unit"],
                "content_url": seed_observation.get("content_url_or_none"),
                "watch_url": seed_observation.get("watch_url_or_none"),
            }
        },
        "provenance": {
            "seed_metric_observation_id": seed_observation["metric_observation_id"],
            "metric_registry_version": seed_observation.get("metric_registry_version"),
            "youtube_creator_observation_id": seed_observation.get("youtube_creator_observation_id"),
            "source_pool_row_id": seed_observation.get("source_pool_row_id"),
            "source_pointer": seed_observation.get("source_pointer"),
            "source_field": seed_observation.get("source_field"),
            "creator_handle_query": seed_observation.get("creator_handle_query"),
            "observed_at_source": seed_observation.get("observed_at_source"),
        },
        "non_claims": _record_non_claims(
            engagement_bearing=(
                posture == "observed"
                and seed_observation["metric_name"] in _ENGAGEMENT_OBSERVATION_METRIC_NAMES
            )
        ),
    }
    if lineage_limitations:
        record["lineage_limitations"] = lineage_limitations
    record["content_hash"] = f"sha256:{_content_hash(record)}"
    return record


def build_metric_rollup_record(
    *,
    seed_rollup: Mapping[str, Any],
    ref_by_seed_observation_id: Mapping[str, Mapping[str, str]],
    raw_anchor: str,
) -> dict[str, Any]:
    """Wrap one committed per-account rollup in a Silver Vault
    MetricRollupObservation record whose ``derived_refs`` point at its source
    observation records.

    ``raw_anchor`` is the rollup's ``platform_account_id`` (resolved by the
    orchestrator and reused for the append path, so the in-record anchor and the
    on-disk location agree). Unlike IG, a YouTube rollup spans multiple per-Short
    packets, so an account-scoped anchor is the honest choice."""
    derived_refs: list[dict[str, Any]] = []
    for source_id in seed_rollup["source_metric_observation_ids"]:
        ref = ref_by_seed_observation_id.get(source_id)
        if ref is None:
            raise ValueError(
                f"rollup {seed_rollup.get('metric_rollup_id')!r} references unknown "
                f"source observation id: {source_id!r}"
            )
        derived_refs.append(
            {
                "edge_type": "derived_from_record",
                "raw_anchor": ref["raw_anchor"],
                "lane_namespace": ref["lane_namespace"],
                "record_id": ref["record_id"],
                "content_hash": ref["content_hash"],
                "content_hash_basis": _CONTENT_HASH_BASIS,
            }
        )

    computed_at = seed_rollup["computed_at"]
    record: dict[str, Any] = {
        "record_id": f"{generate_ulid()}.json",
        "raw_anchor": raw_anchor,
        "lane_namespace": METRIC_ROLLUP_LANE,
        "producer_id": _ROLLUP_PRODUCER_ID,
        "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "producer_schema_version": METRIC_ROLLUP_PRODUCER_SCHEMA_VERSION,
        "content_hash": "",
        "content_hash_basis": _CONTENT_HASH_BASIS,
        "record_kind": "observation",
        "payload_kind": METRIC_ROLLUP_PAYLOAD_KIND,
        "producer_row_kind": "creator_account_metric_rollup",
        "source_family": _SOURCE_FAMILY,
        "source_surface": _SOURCE_SURFACE,
        "observed_at": computed_at,
        "captured_at": computed_at,
        "raw_refs": [],
        "derived_refs": derived_refs,
        "payload": {
            "observation": {
                "subject": _rollup_subject(seed_rollup),
                "rollup_kind": "creator_account_metric_rollup",
                "platform_scope": seed_rollup["platform_scope"],
                "platform_account_ids": list(seed_rollup["platform_account_ids"]),
                "rollup_window": seed_rollup["rollup_window"],
                "rollup_window_description": seed_rollup["rollup_window_description"],
                "content_kind_inclusion_rule": seed_rollup["content_kind_inclusion_rule"],
                "derivation": {
                    "kind": "computed_metric_rollup",
                    "source_record_ref_kind": "derived_refs",
                    "metric_posture_semantics": "source_input_support_not_raw_aggregate_visibility",
                    "calculation_recipe_version": seed_rollup["calculation_recipe_version"],
                },
                "metric_rollups": {
                    name: _rollup_metric(
                        metric, what=f"rollup {seed_rollup.get('metric_rollup_id')!r} metric {name!r}"
                    )
                    for name, metric in seed_rollup["metric_rollups"].items()
                },
                "observation_count": seed_rollup["observation_count"],
                "view_count_min": seed_rollup["view_count_min"],
                "view_count_max": seed_rollup["view_count_max"],
                "calculation_recipe_version": seed_rollup["calculation_recipe_version"],
                "computed_at": computed_at,
                "freshness_state": seed_rollup["freshness_state"],
                "sample_support": seed_rollup["sample_support"],
                "limitations": list(seed_rollup["limitations"]),
                "source_metric_observation_ids": list(seed_rollup["source_metric_observation_ids"]),
            }
        },
        "provenance": {
            "seed_metric_rollup_id": seed_rollup["metric_rollup_id"],
            "public_handle": seed_rollup.get("public_handle"),
        },
        "non_claims": _record_non_claims(
            engagement_bearing=any(
                seed_rollup["metric_rollups"][name]["posture"] == "observed"
                for name in _ENGAGEMENT_ROLLUP_METRIC_NAMES
                if name in seed_rollup["metric_rollups"]
            )
        ),
    }
    record["content_hash"] = f"sha256:{_content_hash(record)}"
    return record


# ---------------------------------------------------------------------------
# Subject / posture / ref helpers
# ---------------------------------------------------------------------------

def _observation_subject(seed_observation: Mapping[str, Any]) -> dict[str, Any]:
    """Every committed YouTube creator-metric observation is a per-Short
    view_count fact (``content_kind == "short"``): the subject is the public
    content object, published by the YouTube channel account. Stable identifiers
    only (video id + channel id) -- the mutable handle is not part of the
    entity_key."""
    ref: dict[str, Any] = {
        "namespace": _PLATFORM_NAMESPACE,
        "kind": "public_content_object",
        "native_id": _required_subject_native_id(
            seed_observation.get("content_id_or_none"),
            what=f"observation {seed_observation.get('metric_observation_id')!r} content subject",
        ),
        "native_id_kind": "youtube_video_id",
        "published_by_account_native_id": _required_subject_native_id(
            seed_observation.get("platform_subject_key"),
            what=f"observation {seed_observation.get('metric_observation_id')!r} publisher subject",
        ),
        "published_by_account_native_id_kind": seed_observation.get("platform_subject_key_type"),
        **_platform_account_ref_field(
            seed_observation["platform_account_id"],
            what=f"observation {seed_observation.get('metric_observation_id')!r} platform account id",
        ),
    }
    return {"ref_type": "entity_key", "ref": ref}


def _rollup_subject(seed_rollup: Mapping[str, Any]) -> dict[str, Any]:
    """The rollup subject is the platform account, keyed by the stable
    youtube_channel_id (not the mutable public handle)."""
    ref: dict[str, Any] = {
        "namespace": _PLATFORM_NAMESPACE,
        "kind": "platform_public_account",
        "native_id": _required_subject_native_id(
            seed_rollup.get("platform_subject_key"),
            what=f"rollup {seed_rollup.get('metric_rollup_id')!r} account subject",
        ),
        "native_id_kind": seed_rollup.get("platform_subject_key_type"),
        **_platform_account_ref_field(
            seed_rollup["profile_subject_id"],
            what=f"rollup {seed_rollup.get('metric_rollup_id')!r} platform account id",
        ),
    }
    return {"ref_type": "entity_key", "ref": ref}


def _raw_ref(
    seed_observation: Mapping[str, Any],
    *,
    bronze_attachment_records_by_packet_body_hash: Mapping[
        tuple[str, str], list[Mapping[str, Any]]
    ],
    use_bronze_attachment_records: bool,
) -> dict[str, Any]:
    """Build an honest portable provenance ref from the fields the YouTube seed
    actually declares as portable (the YouTube seed carries NO IG-style
    raw_anchor dict). Historical v0 seeds use the preserved watch HTML; selective
    v1 seeds use the preserved compact capture payload that contains the exact
    source-visible metric values and comment rows."""
    evidence_hash = seed_observation.get("source_evidence_sha256")
    evidence_hash_basis = seed_observation.get("source_evidence_hash_basis")
    if evidence_hash is None and evidence_hash_basis is None:
        evidence_hash = seed_observation.get("source_watch_html_sha256_or_none")
        evidence_hash_basis = "source_captured_watch_html_sha256"
    if evidence_hash_basis not in {
        "source_captured_watch_html_sha256",
        "source_captured_selective_payload_sha256",
    }:
        raise ValueError(
            f"metric observation {seed_observation.get('metric_observation_id')!r} raw_ref "
            f"has unsupported source_evidence_hash_basis {evidence_hash_basis!r}"
        )
    evidence_hash = _required_hash_value(
        evidence_hash,
        what=f"metric observation {seed_observation.get('metric_observation_id')!r} raw_ref",
    )
    raw_ref: dict[str, Any] = {
        "ref_type": "raw_packet",
        "packet_id": seed_observation.get("source_packet_id_or_none"),
        "source_pointer": seed_observation.get("source_pointer"),
        "source_field": seed_observation.get("source_field"),
        "source_file": seed_observation.get("source_file"),
        "source_row_id": seed_observation.get("source_row_id_or_none"),
        "sha256": evidence_hash,
        "hash_basis": evidence_hash_basis,
        "evidence_sha256": evidence_hash,
        "shorts_html_sha256": seed_observation.get("source_shorts_html_sha256_or_none"),
    }
    if evidence_hash_basis == "source_captured_watch_html_sha256":
        raw_ref["watch_html_sha256"] = evidence_hash
    if not use_bronze_attachment_records:
        return raw_ref

    key = _raw_ref_packet_body_key(raw_ref)
    candidates = (
        bronze_attachment_records_by_packet_body_hash.get(key, [])
        if key is not None
        else []
    )
    if len(candidates) != 1:
        raw_ref.update(
            _fallback_raw_ref_fields(
                residual=(
                    _AMBIGUOUS_AR_LIMITATION
                    if len(candidates) > 1
                    else _MISSING_AR_LIMITATION
                )
            )
        )
        return raw_ref

    attachment_record = candidates[0]
    body_sha256 = attachment_record.get("body_sha256") or evidence_hash
    raw_ref.update(
        {
            "ref_type": _BRONZE_AR_RAW_REF_KIND,
            "attachment_record_id": attachment_record.get("attachment_record_id"),
            "attachment_record_schema_version": attachment_record.get(
                "attachment_record_schema_version"
            ),
            "attachment_record_physicalization": attachment_record.get(
                "attachment_record_physicalization"
            ),
            "file_id": attachment_record.get("file_id"),
            "relative_packet_path": attachment_record.get("relative_packet_path"),
            "body_ref_kind": attachment_record.get("body_ref_kind"),
            "body_ref": attachment_record.get("body_ref"),
            "body_sha256": body_sha256,
            "sha256": body_sha256,
            "hash_basis": attachment_record.get("hash_basis"),
            "source_family": attachment_record.get("source_family"),
            "source_surface": attachment_record.get("source_surface"),
            "source_slice_ids": attachment_record.get("source_slice_ids", []),
            "payload_kind": attachment_record.get("payload_kind"),
            "payload_schema_version": attachment_record.get("payload_schema_version"),
            "replay_version_pins": attachment_record.get("replay_version_pins"),
        }
    )
    return raw_ref


def _fallback_raw_ref_fields(*, residual: str) -> dict[str, str]:
    if residual == _AMBIGUOUS_AR_LIMITATION:
        return {
            "ref_type": "raw_packet",
            "typed_attachment_record_status": "ambiguous",
            "attachment_record_residual": residual,
        }
    return {
        "ref_type": "raw_packet",
        "typed_attachment_record_status": "missing",
        "attachment_record_residual": _MISSING_AR_LIMITATION,
    }


def _bronze_attachment_records_by_packet_body_hash(
    data_root: "DataLakeRoot",
) -> dict[tuple[str, str], list[Mapping[str, Any]]]:
    rows = source_surface_catalog_rows(
        data_root,
        source_family=_YOUTUBE_BRONZE_SOURCE_FAMILY,
        source_surface=_YOUTUBE_BRONZE_SOURCE_SURFACE,
    )
    by_key: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for row in rows["attachment_record_rows"]:
        key = _packet_body_hash_key(row)
        if key is not None:
            by_key.setdefault(key, []).append(row)
    return by_key


def _packet_body_hash_key(record: Mapping[str, Any]) -> tuple[str, str] | None:
    packet_id = record.get("packet_id")
    body_sha256 = record.get("body_sha256")
    if not all(isinstance(value, str) and value.strip() for value in (packet_id, body_sha256)):
        return None
    return (packet_id, body_sha256)


def _raw_ref_packet_body_key(record: Mapping[str, Any]) -> tuple[str, str] | None:
    packet_id = record.get("packet_id")
    sha256 = record.get("sha256")
    if not all(isinstance(value, str) and value.strip() for value in (packet_id, sha256)):
        return None
    return (packet_id, sha256)


def _raw_ref_lineage_limitations(raw_ref: Mapping[str, Any]) -> list[dict[str, str]]:
    status = raw_ref.get("typed_attachment_record_status")
    if status not in {"missing", "ambiguous"}:
        return []
    residual = raw_ref.get("attachment_record_residual")
    detail = residual if isinstance(residual, str) else _MISSING_AR_LIMITATION
    return [{"reason": "other", "detail": detail}]


def _required_hash_value(value: object, *, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{what} requires a non-empty source evidence sha256")
    return value


def _rollup_raw_anchor(seed_rollup: Mapping[str, Any]) -> str:
    """A per-account rollup aggregates observations spanning multiple distinct
    per-Short raw packets, so (unlike IG) there is no single source packet to
    anchor it to. Anchor to the rollup's declared single ``platform_account_ids``
    entry, fail closed if absent, blank, or divergent from ``profile_subject_id``.
    The lake writer additionally validates the segment is path-safe."""
    account_ids = seed_rollup.get("platform_account_ids")
    if not isinstance(account_ids, list) or len(account_ids) != 1:
        raise ValueError(
            f"rollup {seed_rollup.get('metric_rollup_id')!r} requires exactly one "
            "platform_account_id raw anchor"
        )
    account_id = account_ids[0]
    if not isinstance(account_id, str) or not account_id.strip():
        raise ValueError(
            f"rollup {seed_rollup.get('metric_rollup_id')!r} lacks a platform_account_id raw anchor"
        )
    profile_subject_id = seed_rollup.get("profile_subject_id")
    if profile_subject_id is not None and profile_subject_id != account_id:
        raise ValueError(
            f"rollup {seed_rollup.get('metric_rollup_id')!r} platform_account_id raw anchor "
            f"{account_id!r} does not match profile_subject_id {profile_subject_id!r}"
        )
    return account_id


__all__ = [
    "YoutubeCreatorMetricSilverResult",
    "METRIC_OBSERVATION_LANE",
    "METRIC_OBSERVATION_PAYLOAD_KIND",
    "METRIC_ROLLUP_LANE",
    "METRIC_ROLLUP_PAYLOAD_KIND",
    "DEFAULT_YOUTUBE_SEED_PATH",
    "build_metric_observation_record",
    "build_metric_rollup_record",
    "derive_youtube_creator_metric_silver_records_from_seed",
    "derive_youtube_creator_metric_silver_records_from_seed_file",
]
