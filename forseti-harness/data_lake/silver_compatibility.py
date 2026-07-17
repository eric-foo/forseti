"""Closed Silver Vault compatibility registry for immutable persisted records.

Strict new writes and compatible historical reads are separate obligations
(``docs/decisions/silver_vault_legacy_record_convergence_v0.md``). This module
owns the read-side half: one closed, code-owned registry keyed by

    (producer_id, producer_schema_version, lane_namespace)

that names every persisted producer tuple whose immutable records may be read
under a declared compatibility profile instead of the current semantic grammar.
Each entry explicitly owns its stable profile identifier, its persisted
semantic validator, its reference-resolution strategy, whether a physically
verified record may classify current or historical-compatible, its reason
codes, and the checked-in byte-faithful fixture that pins the persisted shape
(``tests/unit/test_silver_compatibility_registry.py`` enforces the one-to-one
registry/fixture equality gate).

Boundaries, deliberately:

- The registry is CLOSED. No plugin hooks, policy DSL, dynamic discovery, or
  raw-path guessing; adding a tuple is a reviewed edit here plus a fixture.
- A profile is read-only. ``validate_silver_vault_record_for_write`` rejects
  every registry tuple, so a compatibility profile can never become writable.
- Current producer versions must not appear here: a record that is not a
  registry tuple is validated under the full current semantic grammar.
- Unknown, contradictory, incomplete, or ambiguous legacy-looking records fail
  closed: a registry tuple is validated ONLY against its own persisted
  profile, never against a union of grammars.

``data_lake.silver_record`` imports this registry at module load; the shared
semantic primitives (posture coupling, strict lineage grammar, the
observed-at contract) are imported lazily at call time so the import-time
dependency stays one-way and the profile validators still reuse the exact
code the current grammar runs -- the fixture equality gate turns any future
tightening of a shared primitive that would break an immutable profile into a
loud test failure instead of a silent unreadable record.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

ProducerTuple = tuple[str, str, str]

# Reference-resolution strategies. classify_silver_vault_record_sources
# dispatches physical source verification on these closed values.
FRAGRANTICA_INFERRED_REFS = "fragrantica_inferred_raw_and_audit_refs"
CREATOR_METRIC_LINEAGE_INDEX = "creator_metric_lineage_index"
STRICT_CANONICAL_REFS = "strict_canonical_refs"

_FRAGRANTICA_PRODUCER_ID = (
    "orca-harness.cleaning.fragrantica_lake.derive_fragrantica_cleaning_into_lake#silver"
)
_YOUTUBE_OBSERVATION_PRODUCER_ID = (
    "orca-harness.capture_spine.creator_profile_current.youtube_silver_metric_producer"
    ".derive_youtube_creator_metric_silver_records_from_seed#metric_observation"
)
_PROJECTION_OBSERVATION_PRODUCER_ID = (
    "orca-harness.capture_spine.creator_profile_current.silver_metric_producer"
    ".derive_creator_metric_silver_records_from_projections#metric_observation"
)
_YOUTUBE_ROLLUP_PRODUCER_ID = (
    "orca-harness.capture_spine.creator_profile_current.youtube_silver_metric_producer"
    ".derive_youtube_creator_metric_silver_records_from_seed#metric_rollup"
)
_PROJECTION_ROLLUP_PRODUCER_ID = (
    "orca-harness.capture_spine.creator_profile_current.silver_metric_producer"
    ".derive_creator_metric_silver_records_from_projections#metric_rollup"
)
_TIKTOK_V1_PRODUCER_ID = (
    "forseti-harness.capture_spine.creator_profile_current.tiktok_comment_attention_producer"
)

# The exact persisted observation key set of every TikTok comment-attention v1
# record (verified uniform across all 174 stored v1 records, null-time and
# known-time, at live fingerprint 07f5e0ca... on 2026-07-16). The null-time
# compatibility branch closes over this set so a mutated or partially rebuilt
# record cannot pass as the immutable historical shape.
_TIKTOK_V1_OBSERVATION_KEYS = frozenset(
    {
        "coverage_window",
        "denominator",
        "engagement_context",
        "metric_name",
        "metric_posture",
        "metric_value",
        "numerator",
        "source_publication_or_event",
        "source_surface",
        "subject",
        "temporal_pairing",
        "unit",
    }
)


@dataclass(frozen=True)
class SilverCompatibilityProfile:
    """One declared immutable persisted form and everything a reader needs.

    ``current_reason_code`` / ``historical_reason_code`` are the classification
    reason codes emitted after physical verification. For the
    ``creator_metric_lineage_index`` strategy both are ``None``: status and
    reason pass through the cross-epoch lineage classification unchanged
    (``data_lake.creator_metric_lineage``), which existing census and reader
    consumers already depend on.
    """

    profile_id: str
    producer_id: str
    producer_schema_version: str
    lane_namespace: str
    payload_kind: str
    validate_persisted: Callable[[Mapping[str, Any]], None]
    reference_strategy: str
    may_classify_current: bool
    may_classify_historical: bool
    current_reason_code: str | None
    historical_reason_code: str | None
    # Harness-root-relative path of the checked-in byte-faithful fixture.
    fixture_path: str

    @property
    def key(self) -> ProducerTuple:
        return (self.producer_id, self.producer_schema_version, self.lane_namespace)


def _silver_record():
    # Lazy import: silver_record imports this registry at module load; the
    # profile validators reuse its semantic primitives at call time only.
    from data_lake import silver_record

    return silver_record


def _require_payload_shape(
    record: Mapping[str, Any], *, profile_id: str, payload_kind: str
) -> Mapping[str, Any]:
    sr = _silver_record()
    if record.get("record_kind") != "observation":
        raise sr.SilverRecordError(f"{profile_id} requires record_kind 'observation'.")
    if record.get("payload_kind") != payload_kind:
        raise sr.SilverRecordError(
            f"{profile_id} requires payload_kind {payload_kind!r}; "
            f"got {record.get('payload_kind')!r}."
        )
    observation = record["payload"].get("observation")
    if not isinstance(observation, Mapping):
        raise sr.SilverRecordError(f"{profile_id} requires payload.observation.")
    return observation


def _require_known_time(record: Mapping[str, Any], *, profile_id: str) -> None:
    sr = _silver_record()
    if record.get("observed_at") is None:
        raise sr.SilverRecordError(
            f"{profile_id} records carry a known observed_at; a null-time form "
            "is not part of this declared persisted profile."
        )
    sr._validate_observed_at_contract(
        record_kind="observation",
        observed_at=record.get("observed_at"),
        captured_at=record.get("captured_at"),
        payload=record["payload"],
    )


def _validate_fragrantica_v0_refs(record: Mapping[str, Any]) -> None:
    sr = _silver_record()
    raw_refs = record["raw_refs"]
    derived_refs = record["derived_refs"]
    if not raw_refs:
        raise sr.SilverRecordError("fragrantica_v0 requires raw_refs.")
    for index, ref in enumerate(raw_refs):
        if not isinstance(ref, Mapping) or ref.get("ref_type") is not None:
            raise sr.SilverRecordError(
                f"Legacy raw_refs[{index}] must use the declared pre-ref_type grammar."
            )
        for field in ("packet_id", "sha256", "hash_basis"):
            sr._require_non_empty_string(ref.get(field), f"Legacy raw_refs[{index}].{field}")
        if ref.get("hash_basis") != sr.RAW_STORED_BYTES_HASH_BASIS:
            raise sr.SilverRecordError(
                f"Legacy raw_refs[{index}] has an unsupported hash basis."
            )
        sr._require_non_empty_string(ref.get("file_id"), f"Legacy raw_refs[{index}].file_id")
    if not derived_refs:
        raise sr.SilverRecordError("fragrantica_v0 requires derived_refs.")
    _validate_legacy_derived_refs(record, expected_lane="cleaning_fragrantica_audit")


def _validate_legacy_derived_refs(record: Mapping[str, Any], *, expected_lane: str) -> None:
    sr = _silver_record()
    for index, ref in enumerate(record["derived_refs"]):
        if not isinstance(ref, Mapping) or ref.get("raw_anchor") is not None:
            raise sr.SilverRecordError(
                f"Legacy derived_refs[{index}] must use the declared address grammar."
            )
        lane = ref.get("lane_namespace", ref.get("lane"))
        if lane != expected_lane:
            raise sr.SilverRecordError(
                f"Legacy derived_refs[{index}] has an unexpected lane."
            )
        sr._require_non_empty_string(
            ref.get("record_id"), f"Legacy derived_refs[{index}].record_id"
        )
        sr._require_non_empty_string(
            ref.get("content_hash"), f"Legacy derived_refs[{index}].content_hash"
        )
        if ref.get("content_hash_basis") != sr.CONTENT_HASH_BASIS:
            raise sr.SilverRecordError(
                f"Legacy derived_refs[{index}].content_hash_basis must be "
                f"{sr.CONTENT_HASH_BASIS!r}."
            )


def _validate_fragrantica_text_v0(record: Mapping[str, Any]) -> None:
    sr = _silver_record()
    observation = _require_payload_shape(
        record, profile_id="fragrantica_text_v0", payload_kind="TextObservation"
    )
    sr._validate_text_observation(observation)
    _require_known_time(record, profile_id="fragrantica_text_v0")
    _validate_fragrantica_v0_refs(record)


def _validate_fragrantica_metric_v0(record: Mapping[str, Any]) -> None:
    sr = _silver_record()
    observation = _require_payload_shape(
        record, profile_id="fragrantica_metric_v0", payload_kind="MetricObservation"
    )
    sr._validate_metric_posture(observation)
    _require_known_time(record, profile_id="fragrantica_metric_v0")
    _validate_fragrantica_v0_refs(record)


def _validate_creator_metric_observation_v0(record: Mapping[str, Any]) -> None:
    sr = _silver_record()
    observation = _require_payload_shape(
        record,
        profile_id="creator_metric_observation_v0",
        payload_kind="MetricObservation",
    )
    sr._validate_metric_posture(observation)
    _require_known_time(record, profile_id="creator_metric_observation_v0")
    raw_refs = record["raw_refs"]
    if not raw_refs:
        raise sr.SilverRecordError("creator_metric_observation_v0 requires raw_refs.")
    for index, ref in enumerate(raw_refs):
        if not isinstance(ref, Mapping) or ref.get("ref_type") is not None:
            raise sr.SilverRecordError(
                f"Legacy raw_refs[{index}] must use the declared pre-ref_type grammar."
            )
        for field in ("packet_id", "sha256", "hash_basis"):
            sr._require_non_empty_string(ref.get(field), f"Legacy raw_refs[{index}].{field}")
        if ref.get("hash_basis") not in (
            sr.RAW_STORED_BYTES_HASH_BASIS,
            "source_captured_watch_html_sha256",
        ):
            raise sr.SilverRecordError(
                f"Legacy raw_refs[{index}] has an unsupported hash basis."
            )
    if record["derived_refs"]:
        raise sr.SilverRecordError(
            "creator_metric_observation_v0 must not carry derived_refs."
        )


def _validate_creator_metric_rollup_v0(record: Mapping[str, Any]) -> None:
    sr = _silver_record()
    _require_payload_shape(
        record,
        profile_id="creator_metric_rollup_v0",
        payload_kind="MetricRollupObservation",
    )
    _require_known_time(record, profile_id="creator_metric_rollup_v0")
    if record["raw_refs"] or not record["derived_refs"]:
        raise sr.SilverRecordError("creator_metric_rollup_v0 requires only derived_refs.")
    _validate_legacy_derived_refs(record, expected_lane="creator_metric_silver")


def _validate_tiktok_comment_attention_v1(record: Mapping[str, Any]) -> None:
    sr = _silver_record()
    observation = _require_payload_shape(
        record,
        profile_id="tiktok_comment_attention_v1",
        payload_kind="MetricObservation",
    )
    if record.get("producer_row_kind") != "tiktok_comment_attention_metric":
        raise sr.SilverRecordError(
            "Legacy TikTok comment-attention v1 producer_row_kind is invalid."
        )
    if record.get("source_surface") != "tiktok_creator_batch_comment_subtitle_admission":
        raise sr.SilverRecordError(
            "Legacy TikTok comment-attention v1 source_surface is invalid."
        )
    sr._require_non_empty_string(
        record.get("captured_at"), "Legacy TikTok comment-attention v1 captured_at"
    )
    if record["derived_refs"]:
        raise sr.SilverRecordError(
            "Legacy TikTok comment-attention v1 must not carry derived_refs."
        )
    sr._validate_strict_lineage_refs(record)
    _validate_tiktok_v1_observation_keys(observation)
    sr._validate_metric_posture(observation)
    if record.get("observed_at") is None:
        _validate_tiktok_v1_null_time_shape(observation)
    else:
        sr._validate_observed_at_contract(
            record_kind="observation",
            observed_at=record.get("observed_at"),
            captured_at=record.get("captured_at"),
            payload=record["payload"],
        )


def _validate_tiktok_v1_observation_keys(observation: Mapping[str, Any]) -> None:
    """Require the closed persisted observation shape for every v1 record."""
    sr = _silver_record()
    observed_keys = frozenset(observation)
    if observed_keys != _TIKTOK_V1_OBSERVATION_KEYS:
        missing = sorted(_TIKTOK_V1_OBSERVATION_KEYS - observed_keys)
        extra = sorted(observed_keys - _TIKTOK_V1_OBSERVATION_KEYS)
        raise sr.SilverRecordError(
            "Legacy TikTok comment-attention v1 observation key set "
            f"does not match the persisted shape (missing={missing!r}, extra={extra!r})."
        )


def _validate_tiktok_v1_null_time_shape(observation: Mapping[str, Any]) -> None:
    """Accept only the exact immutable v1 null-time posture as historical."""
    sr = _silver_record()
    if observation.get("metric_name") != "comment_like_to_video_like_ratio":
        raise sr.SilverRecordError(
            "Legacy TikTok comment-attention v1 metric_name is invalid."
        )
    if observation.get("metric_value") is not None:
        raise sr.SilverRecordError(
            "Legacy TikTok comment-attention v1 null-time metric_value must be null."
        )
    posture = observation.get("metric_posture")
    if not isinstance(posture, Mapping) or (
        posture.get("kind") != "unavailable_with_reason"
        or posture.get("reason_code") != "temporal_alignment_unproven"
    ):
        raise sr.SilverRecordError(
            "Legacy TikTok comment-attention v1 requires temporal_alignment_unproven posture."
        )
    pairing = observation.get("temporal_pairing")
    if not isinstance(pairing, Mapping) or (
        pairing.get("alignment") != "unproven"
        or pairing.get("comment_observed_at") is not None
        or not isinstance(pairing.get("video_stats_observed_at"), str)
        or not pairing["video_stats_observed_at"].strip()
    ):
        raise sr.SilverRecordError(
            "Legacy TikTok comment-attention v1 temporal_pairing is contradictory."
        )
    if observation.get("source_publication_or_event") is not None:
        raise sr.SilverRecordError(
            "Legacy TikTok comment-attention v1 source_publication_or_event must be null."
        )


_FIXTURE_DIR = "tests/fixtures/silver_compatibility"

SILVER_COMPATIBILITY_PROFILES: tuple[SilverCompatibilityProfile, ...] = (
    SilverCompatibilityProfile(
        profile_id="fragrantica_text_v0",
        producer_id=_FRAGRANTICA_PRODUCER_ID,
        producer_schema_version="fragrantica_cleaning_silver_textobservation_v0",
        lane_namespace="cleaning_fragrantica_silver",
        payload_kind="TextObservation",
        validate_persisted=_validate_fragrantica_text_v0,
        reference_strategy=FRAGRANTICA_INFERRED_REFS,
        may_classify_current=True,
        may_classify_historical=False,
        current_reason_code="legacy_bytes_verified",
        historical_reason_code=None,
        fixture_path=f"{_FIXTURE_DIR}/fragrantica_text_v0.json",
    ),
    SilverCompatibilityProfile(
        profile_id="fragrantica_metric_v0",
        producer_id=_FRAGRANTICA_PRODUCER_ID,
        producer_schema_version="fragrantica_cleaning_silver_metricobservation_v0",
        lane_namespace="cleaning_fragrantica_silver",
        payload_kind="MetricObservation",
        validate_persisted=_validate_fragrantica_metric_v0,
        reference_strategy=FRAGRANTICA_INFERRED_REFS,
        may_classify_current=True,
        may_classify_historical=False,
        current_reason_code="legacy_bytes_verified",
        historical_reason_code=None,
        fixture_path=f"{_FIXTURE_DIR}/fragrantica_metric_v0.json",
    ),
    SilverCompatibilityProfile(
        profile_id="creator_metric_observation_youtube_v0",
        producer_id=_YOUTUBE_OBSERVATION_PRODUCER_ID,
        producer_schema_version="youtube_creator_metric_silver_metricobservation_v0",
        lane_namespace="creator_metric_silver",
        payload_kind="MetricObservation",
        validate_persisted=_validate_creator_metric_observation_v0,
        reference_strategy=CREATOR_METRIC_LINEAGE_INDEX,
        may_classify_current=True,
        may_classify_historical=True,
        current_reason_code=None,
        historical_reason_code=None,
        fixture_path=f"{_FIXTURE_DIR}/creator_metric_observation_youtube_v0.json",
    ),
    SilverCompatibilityProfile(
        profile_id="creator_metric_observation_projection_v0",
        producer_id=_PROJECTION_OBSERVATION_PRODUCER_ID,
        producer_schema_version="creator_metric_silver_metricobservation_v0",
        lane_namespace="creator_metric_silver",
        payload_kind="MetricObservation",
        validate_persisted=_validate_creator_metric_observation_v0,
        reference_strategy=CREATOR_METRIC_LINEAGE_INDEX,
        may_classify_current=True,
        may_classify_historical=True,
        current_reason_code=None,
        historical_reason_code=None,
        fixture_path=f"{_FIXTURE_DIR}/creator_metric_observation_projection_v0.json",
    ),
    SilverCompatibilityProfile(
        profile_id="creator_metric_rollup_youtube_v0",
        producer_id=_YOUTUBE_ROLLUP_PRODUCER_ID,
        producer_schema_version="youtube_creator_metric_silver_metricrollupobservation_v0",
        lane_namespace="creator_metric_rollup_silver",
        payload_kind="MetricRollupObservation",
        validate_persisted=_validate_creator_metric_rollup_v0,
        reference_strategy=CREATOR_METRIC_LINEAGE_INDEX,
        may_classify_current=True,
        may_classify_historical=True,
        current_reason_code=None,
        historical_reason_code=None,
        fixture_path=f"{_FIXTURE_DIR}/creator_metric_rollup_youtube_v0.json",
    ),
    SilverCompatibilityProfile(
        profile_id="creator_metric_rollup_projection_v0",
        producer_id=_PROJECTION_ROLLUP_PRODUCER_ID,
        producer_schema_version="creator_metric_silver_metricrollupobservation_v0",
        lane_namespace="creator_metric_rollup_silver",
        payload_kind="MetricRollupObservation",
        validate_persisted=_validate_creator_metric_rollup_v0,
        reference_strategy=CREATOR_METRIC_LINEAGE_INDEX,
        may_classify_current=True,
        may_classify_historical=True,
        current_reason_code=None,
        historical_reason_code=None,
        fixture_path=f"{_FIXTURE_DIR}/creator_metric_rollup_projection_v0.json",
    ),
    SilverCompatibilityProfile(
        profile_id="tiktok_comment_attention_v1",
        producer_id=_TIKTOK_V1_PRODUCER_ID,
        producer_schema_version="tiktok_comment_attention_metric_observation_v1",
        lane_namespace="tiktok_comment_attention_silver",
        payload_kind="MetricObservation",
        validate_persisted=_validate_tiktok_comment_attention_v1,
        reference_strategy=STRICT_CANONICAL_REFS,
        may_classify_current=True,
        may_classify_historical=True,
        current_reason_code="legacy_bytes_verified",
        historical_reason_code="legacy_tiktok_comment_attention_v1_bytes_verified",
        fixture_path=f"{_FIXTURE_DIR}/tiktok_comment_attention_v1.json",
    ),
)

_PROFILES_BY_KEY: dict[ProducerTuple, SilverCompatibilityProfile] = {
    profile.key: profile for profile in SILVER_COMPATIBILITY_PROFILES
}
if len(_PROFILES_BY_KEY) != len(SILVER_COMPATIBILITY_PROFILES):
    raise RuntimeError("Silver compatibility registry declares a duplicate producer tuple.")


def compatibility_profile_for(
    record: Mapping[str, Any],
) -> SilverCompatibilityProfile | None:
    """Return the declared profile for a record's exact producer tuple, else None."""
    return _PROFILES_BY_KEY.get(
        (
            record.get("producer_id"),
            record.get("producer_schema_version"),
            record.get("lane_namespace"),
        )
    )


__all__ = [
    "CREATOR_METRIC_LINEAGE_INDEX",
    "FRAGRANTICA_INFERRED_REFS",
    "STRICT_CANONICAL_REFS",
    "SILVER_COMPATIBILITY_PROFILES",
    "SilverCompatibilityProfile",
    "compatibility_profile_for",
]
