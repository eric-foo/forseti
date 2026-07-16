"""Closed Silver compatibility registry + byte-faithful fixture equality gate.

Two-way, deterministic: every registry tuple has exactly one checked-in
fixture that reproduces the persisted shape; every fixture belongs to exactly
one registry tuple; each fixture's content hash verifies before compatibility
inference, its persisted semantic validator passes, its reference resolver
behaves exactly as its entry declares, mutation of a discriminating field
fails closed, and no fixture can pass the strict new-write boundary.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from data_lake.root import DataLakeRoot
from data_lake.silver_census import build_silver_observation_census
from data_lake.silver_compatibility import (
    CREATOR_METRIC_LINEAGE_INDEX,
    FRAGRANTICA_INFERRED_REFS,
    SILVER_COMPATIBILITY_PROFILES,
    STRICT_CANONICAL_REFS,
    compatibility_profile_for,
)
from data_lake.silver_record import (
    CURRENT_SOURCE_BACKED_AUTHORITY,
    HISTORICAL_COMPATIBLE_AUTHORITY,
    INVALID_SILVER_AUTHORITY,
    SilverRecordError,
    append_silver_record,
    classify_silver_vault_record_sources,
    silver_content_hash,
    validate_silver_vault_record,
    validate_silver_vault_record_for_write,
    validate_silver_vault_record_stable,
)

from _silver_compatibility_fixture_lake import (
    HARNESS_ROOT,
    load_fixture_record,
    materialize_fixture_lake,
)

# The complete closed set of persisted compatibility tuples. Adding or removing
# a tuple is a deliberate reviewed edit here AND in the registry AND a fixture.
DECLARED_TUPLES = {
    (
        "orca-harness.cleaning.fragrantica_lake.derive_fragrantica_cleaning_into_lake#silver",
        "fragrantica_cleaning_silver_textobservation_v0",
        "cleaning_fragrantica_silver",
    ),
    (
        "orca-harness.cleaning.fragrantica_lake.derive_fragrantica_cleaning_into_lake#silver",
        "fragrantica_cleaning_silver_metricobservation_v0",
        "cleaning_fragrantica_silver",
    ),
    (
        "orca-harness.capture_spine.creator_profile_current.youtube_silver_metric_producer.derive_youtube_creator_metric_silver_records_from_seed#metric_observation",
        "youtube_creator_metric_silver_metricobservation_v0",
        "creator_metric_silver",
    ),
    (
        "orca-harness.capture_spine.creator_profile_current.silver_metric_producer.derive_creator_metric_silver_records_from_projections#metric_observation",
        "creator_metric_silver_metricobservation_v0",
        "creator_metric_silver",
    ),
    (
        "orca-harness.capture_spine.creator_profile_current.youtube_silver_metric_producer.derive_youtube_creator_metric_silver_records_from_seed#metric_rollup",
        "youtube_creator_metric_silver_metricrollupobservation_v0",
        "creator_metric_rollup_silver",
    ),
    (
        "orca-harness.capture_spine.creator_profile_current.silver_metric_producer.derive_creator_metric_silver_records_from_projections#metric_rollup",
        "creator_metric_silver_metricrollupobservation_v0",
        "creator_metric_rollup_silver",
    ),
    (
        "forseti-harness.capture_spine.creator_profile_current.tiktok_comment_attention_producer",
        "tiktok_comment_attention_metric_observation_v1",
        "tiktok_comment_attention_silver",
    ),
}

_PROFILES_BY_ID = {profile.profile_id: profile for profile in SILVER_COMPATIBILITY_PROFILES}

# Declared classification of each physically verified fixture:
# (status, reason_code or None for lineage pass-through).
DECLARED_FIXTURE_CLASSIFICATION = {
    "fragrantica_text_v0": (CURRENT_SOURCE_BACKED_AUTHORITY, "legacy_bytes_verified"),
    "fragrantica_metric_v0": (CURRENT_SOURCE_BACKED_AUTHORITY, "legacy_bytes_verified"),
    "creator_metric_observation_youtube_v0": (
        CURRENT_SOURCE_BACKED_AUTHORITY,
        "current_root_bytes_verified",
    ),
    "creator_metric_observation_projection_v0": (
        CURRENT_SOURCE_BACKED_AUTHORITY,
        "current_root_bytes_verified",
    ),
    "creator_metric_rollup_youtube_v0": (
        CURRENT_SOURCE_BACKED_AUTHORITY,
        "all_inputs_current_root_byte_verified",
    ),
    "creator_metric_rollup_projection_v0": (
        CURRENT_SOURCE_BACKED_AUTHORITY,
        "all_inputs_current_root_byte_verified",
    ),
    "tiktok_comment_attention_v1": (
        HISTORICAL_COMPATIBLE_AUTHORITY,
        "legacy_tiktok_comment_attention_v1_bytes_verified",
    ),
}


def _rehash(record: dict[str, Any]) -> dict[str, Any]:
    record["content_hash"] = f"sha256:{silver_content_hash(record)}"
    return record


def test_registry_covers_exactly_the_declared_tuples() -> None:
    assert {profile.key for profile in SILVER_COMPATIBILITY_PROFILES} == DECLARED_TUPLES
    assert len(SILVER_COMPATIBILITY_PROFILES) == len(DECLARED_TUPLES)
    assert len(_PROFILES_BY_ID) == len(SILVER_COMPATIBILITY_PROFILES)


def test_registry_excludes_current_producer_versions() -> None:
    from capture_spine.creator_profile_current.silver_metric_producer import (
        METRIC_OBSERVATION_PRODUCER_SCHEMA_VERSION as IG_OBS_CURRENT,
        METRIC_ROLLUP_PRODUCER_SCHEMA_VERSION as IG_ROLLUP_CURRENT,
    )
    from capture_spine.creator_profile_current.tiktok_comment_attention_producer import (
        COMMENT_ATTENTION_PRODUCER_SCHEMA_VERSION as TIKTOK_CURRENT,
    )
    from capture_spine.creator_profile_current.youtube_silver_metric_producer import (
        METRIC_OBSERVATION_PRODUCER_SCHEMA_VERSION as YT_OBS_CURRENT,
        METRIC_ROLLUP_PRODUCER_SCHEMA_VERSION as YT_ROLLUP_CURRENT,
    )

    registered_schema_versions = {
        profile.producer_schema_version for profile in SILVER_COMPATIBILITY_PROFILES
    }
    for current in (
        IG_OBS_CURRENT,
        IG_ROLLUP_CURRENT,
        TIKTOK_CURRENT,
        YT_OBS_CURRENT,
        YT_ROLLUP_CURRENT,
    ):
        assert current not in registered_schema_versions


def test_registry_and_fixture_corpus_are_one_to_one() -> None:
    fixture_dir = HARNESS_ROOT / "tests" / "fixtures" / "silver_compatibility"
    declared = {HARNESS_ROOT / profile.fixture_path for profile in SILVER_COMPATIBILITY_PROFILES}
    on_disk = set(fixture_dir.glob("*.json"))
    assert declared == on_disk
    assert len(declared) == len(SILVER_COMPATIBILITY_PROFILES)


@pytest.mark.parametrize("profile", SILVER_COMPATIBILITY_PROFILES, ids=lambda p: p.profile_id)
def test_fixture_matches_its_registry_key_and_hash_verifies(profile) -> None:
    record = load_fixture_record(profile)
    assert record["producer_id"] == profile.producer_id
    assert record["producer_schema_version"] == profile.producer_schema_version
    assert record["lane_namespace"] == profile.lane_namespace
    assert record["payload_kind"] == profile.payload_kind
    # The original content hash verifies before any compatibility inference.
    assert record["content_hash"] == f"sha256:{silver_content_hash(record)}"
    validate_silver_vault_record_stable(record)
    assert compatibility_profile_for(record) is profile
    # The declared persisted semantic validator passes on the exact stored shape.
    profile.validate_persisted(record)
    validate_silver_vault_record(record)


@pytest.mark.parametrize("profile", SILVER_COMPATIBILITY_PROFILES, ids=lambda p: p.profile_id)
def test_fixture_cannot_pass_the_strict_new_write_boundary(profile) -> None:
    record = load_fixture_record(profile)
    with pytest.raises(SilverRecordError, match="read-only compatibility"):
        validate_silver_vault_record_for_write(record)


def test_fixture_append_is_refused_before_any_write(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    for profile in SILVER_COMPATIBILITY_PROFILES:
        record = load_fixture_record(profile)
        with pytest.raises(SilverRecordError, match="read-only compatibility"):
            append_silver_record(
                root,
                raw_anchor=record["raw_anchor"],
                lane=record["lane_namespace"],
                record_id=record["record_id"],
                record=record,
            )
        assert not root.lane_dir(
            subtree="derived",
            raw_anchor=record["raw_anchor"],
            lane=record["lane_namespace"],
        ).exists()


def test_fixture_reference_resolution_behaves_as_declared(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    seeded = materialize_fixture_lake(root)
    for profile in SILVER_COMPATIBILITY_PROFILES:
        record, path = seeded[profile.profile_id]
        authority = classify_silver_vault_record_sources(root, record, record_path=path)
        expected_status, expected_reason = DECLARED_FIXTURE_CLASSIFICATION[profile.profile_id]
        assert (authority.status, authority.reason_code) == (
            expected_status,
            expected_reason,
        ), profile.profile_id
        may_current = authority.status == CURRENT_SOURCE_BACKED_AUTHORITY
        may_historical = authority.status == HISTORICAL_COMPATIBLE_AUTHORITY
        assert not may_current or profile.may_classify_current
        assert not may_historical or profile.may_classify_historical
        assert profile.reference_strategy in {
            FRAGRANTICA_INFERRED_REFS,
            CREATOR_METRIC_LINEAGE_INDEX,
            STRICT_CANONICAL_REFS,
        }


def test_census_and_authority_readers_agree_on_the_fixture_lake(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    materialize_fixture_lake(root)
    census = build_silver_observation_census(root)
    totals = census["totals"]
    assert totals["silver_records"] == 7
    assert totals["current_source_backed_silver_records"] == 6
    assert totals["historical_compatible_silver_records"] == 1
    assert totals["unclassified_silver_records"] == 0
    assert census["errors"] == []


def _tamper(record: dict[str, Any], dotted: str, value: Any, *, delete: bool = False) -> None:
    parts = dotted.split(".")
    container: Any = record
    for part in parts[:-1]:
        container = container[part]
    if delete:
        del container[parts[-1]]
    else:
        container[parts[-1]] = value


# Discriminating-field mutations. Every entry must classify INVALID (fail
# closed) after the record is re-hashed, proving the mutated shape can claim
# neither its compatibility profile nor the current strict grammar.
_MUTATIONS = [
    ("fragrantica_text_v0", "producer_schema_version", "fragrantica_cleaning_silver_textobservation_v999", False),
    ("fragrantica_text_v0", "raw_refs", [], False),
    ("fragrantica_text_v0", "derived_refs", [], False),
    ("fragrantica_metric_v0", "payload_kind", "TextObservation", False),
    ("fragrantica_metric_v0", "derived_refs", [], False),
    ("creator_metric_observation_youtube_v0", "producer_id", "unknown.producer", False),
    ("creator_metric_observation_youtube_v0", "raw_refs", [], False),
    ("creator_metric_observation_projection_v0", "observed_at", None, False),
    ("creator_metric_rollup_youtube_v0", "derived_refs", [], False),
    ("creator_metric_rollup_projection_v0", "payload_kind", "MetricObservation", False),
    ("tiktok_comment_attention_v1", "producer_schema_version", "tiktok_comment_attention_metric_observation_v999", False),
    ("tiktok_comment_attention_v1", "payload.observation.metric_value", 0.5, False),
    ("tiktok_comment_attention_v1", "payload.observation.metric_posture.reason_code", "some_other_reason", False),
    ("tiktok_comment_attention_v1", "payload.observation.temporal_pairing.alignment", "same_capture_observation", False),
    ("tiktok_comment_attention_v1", "payload.observation.source_publication_or_event", "2026-01-01T00:00:00Z", False),
    ("tiktok_comment_attention_v1", "captured_at", None, False),
    ("tiktok_comment_attention_v1", "derived_refs", [{"raw_anchor": "x", "lane_namespace": "y", "record_id": "z"}], False),
    # PR #1006 review gap (F-1): the persisted observation key set is closed.
    # Omitting a real persisted field or adding a foreign one fails closed.
    ("tiktok_comment_attention_v1", "payload.observation.engagement_context", None, True),
    ("tiktok_comment_attention_v1", "payload.observation.effective_interval", {"start": None, "start_precision": "unknown"}, False),
]


@pytest.mark.parametrize(
    ("profile_id", "dotted", "value", "delete"),
    _MUTATIONS,
    ids=[f"{row[0]}::{row[1]}" for row in _MUTATIONS],
)
def test_mutating_a_discriminating_field_fails_closed(
    tmp_path: Path, profile_id: str, dotted: str, value: Any, delete: bool
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    seeded = materialize_fixture_lake(root)
    record, path = seeded[profile_id]
    mutated = deepcopy(record)
    _tamper(mutated, dotted, value, delete=delete)
    _rehash(mutated)
    authority = classify_silver_vault_record_sources(root, mutated, record_path=path)
    assert authority.status == INVALID_SILVER_AUTHORITY, (profile_id, dotted, authority)


def test_tampered_content_hash_fails_before_compatibility_inference(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    seeded = materialize_fixture_lake(root)
    record, path = seeded["tiktok_comment_attention_v1"]
    tampered = deepcopy(record)
    tampered["captured_at"] = "2027-01-01T00:00:00Z"  # deliberately NOT re-hashed
    authority = classify_silver_vault_record_sources(root, tampered, record_path=path)
    assert authority.status == INVALID_SILVER_AUTHORITY
    assert authority.reason_code == "invalid_silver_envelope"
    assert "content hash mismatch" in (authority.error or "")


def test_fixture_records_are_never_mutated_by_classification(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    seeded = materialize_fixture_lake(root)
    for profile in SILVER_COMPATIBILITY_PROFILES:
        record, path = seeded[profile.profile_id]
        original = deepcopy(record)
        classify_silver_vault_record_sources(root, record, record_path=path)
        assert record == original, profile.profile_id
