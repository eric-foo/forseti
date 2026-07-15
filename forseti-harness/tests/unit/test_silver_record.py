"""Silver Vault envelope validator + validating write front-door.

Proves the no-blur core is enforced by CODE: a blurred Silver record is rejected,
and the front-door refuses to persist one (raises before any bytes are written).
"""
from __future__ import annotations

from pathlib import Path
from copy import deepcopy
import hashlib
import json

import pytest

from data_lake.root import DataLakeRoot, raw_shard
from data_lake.silver_census import build_silver_observation_census
from data_lake.silver_record import (
    CURRENT_SOURCE_BACKED_AUTHORITY,
    INVALID_SILVER_AUTHORITY,
    SilverRecordError,
    append_silver_record,
    append_silver_record_set,
    classify_silver_vault_record_sources,
    silver_content_hash,
    validate_silver_vault_record,
    validate_silver_vault_record_for_write,
)

_PACKET_ID = "01J00000000000000000000001"
_SILVER_LANE = "cleaning_fragrantica_silver"


def _text_record() -> dict:
    record = {
        "record_id": "rec_text.json",
        "raw_anchor": _PACKET_ID,
        "lane_namespace": _SILVER_LANE,
        "producer_id": "test.silver",
        "schema_version": "silver_vault_record_v0",
        "producer_schema_version": "test_v0",
        "record_kind": "observation",
        "payload_kind": "TextObservation",
        "producer_row_kind": "test_text",
        "source_surface": "test_surface",
        "observed_at": "2026-07-14T00:00:00Z",
        "captured_at": "2026-07-14T00:00:00Z",
        "raw_refs": [{"ref_type": "raw_packet", "packet_id": _PACKET_ID}],
        "derived_refs": [],
        "content_hash": "",
        "content_hash_basis": "canonical_json_excluding_content_hash",
        "payload": {
            "observation": {
                "text_artifact_type": "review_body",
                "text_value": "This perfume died young.",
                "text_ref": None,
                "text_hash": "sha256:cf4cba9b20b36e4795eb1e25cb44ec847ba2e8cf862166985fefdfae5d2ef5ee",
                "text_posture": {"kind": "observed", "reason_code": None, "reason_detail": None},
            }
        },
    }
    record["content_hash"] = f"sha256:{silver_content_hash(record)}"
    return record


def _metric_record() -> dict:
    record = {
        "record_id": "rec_metric.json",
        "raw_anchor": _PACKET_ID,
        "lane_namespace": _SILVER_LANE,
        "producer_id": "test.silver",
        "schema_version": "silver_vault_record_v0",
        "producer_schema_version": "test_v0",
        "record_kind": "observation",
        "payload_kind": "MetricObservation",
        "producer_row_kind": "test_metric",
        "source_surface": "test_surface",
        "observed_at": "2026-07-14T00:00:00Z",
        "captured_at": "2026-07-14T00:00:00Z",
        "raw_refs": [{"ref_type": "raw_packet", "packet_id": _PACKET_ID}],
        "derived_refs": [],
        "content_hash": "",
        "content_hash_basis": "canonical_json_excluding_content_hash",
        "payload": {
            "observation": {
                "metric_name": "review_rating",
                "metric_value": 5,
                "metric_posture": {"kind": "observed", "reason_code": None, "reason_detail": None},
            }
        },
    }
    record["content_hash"] = f"sha256:{silver_content_hash(record)}"
    return record


def _metric_set_record() -> dict:
    record = {
        "record_id": "rec_metric_set.json",
        "raw_anchor": _PACKET_ID,
        "lane_namespace": _SILVER_LANE,
        "producer_id": "test.silver",
        "schema_version": "silver_vault_record_v0",
        "producer_schema_version": "test_v0",
        "record_kind": "observation",
        "payload_kind": "MetricObservationSet",
        "producer_row_kind": "test_metric_set",
        "source_surface": "test_surface",
        "observed_at": "2026-07-14T00:00:00Z",
        "captured_at": "2026-07-14T00:00:00Z",
        "raw_refs": [{"ref_type": "raw_packet", "packet_id": _PACKET_ID}],
        "derived_refs": [],
        "content_hash": "",
        "content_hash_basis": "canonical_json_excluding_content_hash",
        "payload": {
            "observation": {
                "subject": {
                    "ref_type": "entity_key",
                    "ref": {
                        "namespace": "tiktok",
                        "kind": "platform_public_account",
                        "native_id": "creator",
                    },
                },
                "observation_set_kind": "social_content_metric_grid",
                "platform": "tiktok",
                "policy_version": "policy_v0",
                "policy_fingerprint_sha256": "a" * 64,
                "row_count": 1,
                "rows": [
                    {
                        "subject": {
                            "ref_type": "entity_key",
                            "ref": {
                                "namespace": "tiktok",
                                "kind": "public_content_object",
                                "native_id": "123",
                            },
                        },
                        "metrics": {
                            "view_count": {
                                "metric_value": 0,
                                "metric_posture": {
                                    "kind": "observed",
                                    "reason_code": None,
                                    "reason_detail": None,
                                },
                                "unit": "count",
                                "source_field": "playCount",
                            }
                        },
                    }
                ],
            }
        },
    }
    record["content_hash"] = f"sha256:{silver_content_hash(record)}"
    return record


def _rehash(record: dict) -> None:
    record["content_hash"] = f"sha256:{silver_content_hash(record)}"


def _explicit_unknown_time_observation() -> dict:
    record = _metric_record()
    record["payload_kind"] = "UnknownSourceTimeObservation"
    record["observed_at"] = None
    record["payload"] = {
        "observation": {
            "effective_interval": {
                "start": None,
                "start_precision": "unknown",
                "end": None,
                "end_precision": "unknown",
                "end_state": "unknown",
                "unknown_reason": "the source exposes no effective timestamp",
            },
            "recorded_at": "2026-07-14T01:00:00Z",
            "evidence_refs": [{"packet_id": _PACKET_ID}],
            "limitations": ["Source-effective time is absent from the cited material."],
        }
    }
    _rehash(record)
    return record


def _commit_source(root: DataLakeRoot, *, body: bytes = b"source") -> Path:
    container = root.path / "raw" / raw_shard(_PACKET_ID) / _PACKET_ID
    preserved = container / "preserved" / "source.bin"
    preserved.parent.mkdir(parents=True)
    preserved.write_bytes(body)
    (container / "manifest.json").write_text(
        json.dumps(
            {
                "packet_id": _PACKET_ID,
                "preserved_files": [
                    {
                        "file_id": "source",
                        "relative_packet_path": "preserved/source.bin",
                        "size_bytes": len(body),
                        "sha256": hashlib.sha256(body).hexdigest(),
                        "hash_basis": "raw_stored_bytes",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return preserved


def test_validate_accepts_well_formed_text_and_metric_observations() -> None:
    validate_silver_vault_record(_text_record())
    validate_silver_vault_record(_metric_record())
    validate_silver_vault_record(_metric_set_record())


def test_validate_accepts_explicit_unknown_time_observation() -> None:
    validate_silver_vault_record(_explicit_unknown_time_observation())


def test_validate_rejects_ordinary_observation_without_observed_at() -> None:
    record = _metric_record()
    record["observed_at"] = None
    _rehash(record)
    with pytest.raises(SilverRecordError, match="requires payload.observation.effective_interval"):
        validate_silver_vault_record(record)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (
            lambda observation: observation["effective_interval"].pop("start_precision"),
            "start_precision='unknown'",
        ),
        (
            lambda observation: observation["effective_interval"].update(unknown_reason=""),
            "unknown_reason",
        ),
        (lambda observation: observation.update(evidence_refs=[]), "evidence_refs"),
        (lambda observation: observation.update(limitations=[]), "limitations"),
        (lambda observation: observation.pop("recorded_at"), "recorded_at"),
    ],
)
def test_validate_rejects_partial_unknown_time_observation(mutation, message: str) -> None:
    record = _explicit_unknown_time_observation()
    mutation(record["payload"]["observation"])
    _rehash(record)
    with pytest.raises(SilverRecordError, match=message):
        validate_silver_vault_record(record)


def test_validate_rejects_capture_or_record_time_substituted_for_unknown_observed_at() -> None:
    record = _explicit_unknown_time_observation()
    record["observed_at"] = record["captured_at"]
    _rehash(record)
    with pytest.raises(SilverRecordError, match="must not substitute"):
        validate_silver_vault_record(record)


def test_validate_preserves_nullable_relationship_observed_at() -> None:
    record = _metric_record()
    record["record_kind"] = "relationship"
    record["payload_kind"] = "RelationshipEdge"
    record["observed_at"] = None
    record["payload"] = {
        "relationship": {
            "edge_type": "derived_from_record",
            "from": {"ref_type": "record_id", "ref": "source"},
            "to": {"ref_type": "record_id", "ref": "target"},
        }
    }
    _rehash(record)
    validate_silver_vault_record(record)


def test_validate_requires_non_null_captured_at() -> None:
    record = _explicit_unknown_time_observation()
    record["captured_at"] = None
    _rehash(record)
    with pytest.raises(SilverRecordError, match="captured_at"):
        validate_silver_vault_record(record)


def test_validate_metric_set_rejects_row_count_drift() -> None:
    record = _metric_set_record()
    record["payload"]["observation"]["row_count"] = 2
    with pytest.raises(SilverRecordError, match="row_count"):
        validate_silver_vault_record(record)


def test_validate_metric_set_rejects_cross_platform_row_namespace() -> None:
    record = _metric_set_record()
    record["payload"]["observation"]["rows"][0]["subject"]["ref"]["namespace"] = "instagram"
    with pytest.raises(SilverRecordError, match="must equal platform"):
        validate_silver_vault_record(record)


def test_validate_metric_set_rejects_missing_source_field() -> None:
    record = _metric_set_record()
    del record["payload"]["observation"]["rows"][0]["metrics"]["view_count"][
        "source_field"
    ]
    with pytest.raises(SilverRecordError, match="source_field"):
        validate_silver_vault_record(record)


def test_validate_rejects_open_record_kind() -> None:
    record = _text_record()
    record["record_kind"] = "banana"
    with pytest.raises(SilverRecordError, match="record_kind"):
        validate_silver_vault_record(record)


def test_validate_rejects_wrong_schema_version() -> None:
    record = _text_record()
    record["schema_version"] = "cleaning_audit_pack_v0"
    with pytest.raises(SilverRecordError, match="schema_version"):
        validate_silver_vault_record(record)


def test_validate_rejects_missing_common_header_field() -> None:
    record = _text_record()
    del record["producer_id"]
    with pytest.raises(SilverRecordError, match="producer_id"):
        validate_silver_vault_record(record)


def test_validate_rejects_content_hash_mismatch() -> None:
    record = _text_record()
    record["payload"]["observation"]["text_value"] = "changed after hashing"
    record["payload"]["observation"]["text_hash"] = (
        "sha256:831963f00e4e78b71be17b656210f4375b11e23063b44e150f6eee7684cc5c06"
    )
    with pytest.raises(SilverRecordError, match="content hash mismatch"):
        validate_silver_vault_record(record)


def test_validate_rejects_record_without_source_lineage() -> None:
    record = _text_record()
    record["raw_refs"] = []
    with pytest.raises(SilverRecordError, match="at least one resolvable"):
        validate_silver_vault_record(record)


def test_validate_rejects_raw_ref_without_explicit_source_posture() -> None:
    record = _text_record()
    record["raw_refs"][0].pop("ref_type")
    _rehash(record)

    with pytest.raises(SilverRecordError, match="ref_type"):
        validate_silver_vault_record(record)


def test_validate_rejects_raw_ref_with_non_raw_bytes_basis() -> None:
    record = _text_record()
    record["raw_refs"] = [
        {
            "ref_type": "raw_packet",
            "packet_id": _PACKET_ID,
            "sha256": "a" * 64,
            "hash_basis": "source_captured_watch_html_sha256",
        }
    ]
    _rehash(record)

    with pytest.raises(SilverRecordError, match="raw_stored_bytes"):
        validate_silver_vault_record(record)


def test_validate_bronze_ref_requires_raw_bytes_basis_and_matching_body_hash() -> None:
    record = _text_record()
    ref = {
        "ref_type": "bronze_attachment_record",
        "packet_id": _PACKET_ID,
        "attachment_record_id": "ar_test",
        "source_family": "youtube",
        "source_surface": "youtube_watch_metadata_comments",
        "sha256": "a" * 64,
        "body_sha256": "a" * 64,
        "hash_basis": "raw_stored_bytes",
    }
    record["raw_refs"] = [ref]
    _rehash(record)
    validate_silver_vault_record(record)

    hashless = deepcopy(record)
    for field in ("sha256", "hash_basis", "body_sha256"):
        hashless["raw_refs"][0].pop(field)
    _rehash(hashless)
    with pytest.raises(SilverRecordError, match="sha256 must be a non-empty string"):
        validate_silver_vault_record(hashless)

    missing_body_hash = deepcopy(record)
    missing_body_hash["raw_refs"][0].pop("body_sha256")
    _rehash(missing_body_hash)
    with pytest.raises(SilverRecordError, match="body_sha256 must be a non-empty string"):
        validate_silver_vault_record(missing_body_hash)

    wrong_basis = deepcopy(record)
    wrong_basis["raw_refs"][0]["hash_basis"] = "derived_record_bytes"
    _rehash(wrong_basis)
    with pytest.raises(SilverRecordError, match="raw_stored_bytes"):
        validate_silver_vault_record(wrong_basis)

    wrong_body_hash = deepcopy(record)
    wrong_body_hash["raw_refs"][0]["body_sha256"] = "b" * 64
    _rehash(wrong_body_hash)
    with pytest.raises(SilverRecordError, match="body_sha256 must equal sha256"):
        validate_silver_vault_record(wrong_body_hash)


def test_validate_derived_hash_pairs_are_independent_and_closed() -> None:
    address = {
        "raw_anchor": _PACKET_ID,
        "lane_namespace": _SILVER_LANE,
        "record_id": "source.json",
    }
    sha_pair = {
        **address,
        "sha256": "a" * 64,
        "hash_basis": "derived_record_bytes",
    }
    content_pair = {
        **address,
        "content_hash": f"sha256:{'b' * 64}",
        "content_hash_basis": "canonical_json_excluding_content_hash",
    }
    for ref in (sha_pair, content_pair, {**sha_pair, **content_pair}):
        record = _metric_record()
        record["raw_refs"] = []
        record["derived_refs"] = [ref]
        _rehash(record)
        validate_silver_vault_record(record)

    wrong_sha_basis = {**sha_pair, "hash_basis": "raw_stored_bytes"}
    record = _metric_record()
    record["raw_refs"] = []
    record["derived_refs"] = [wrong_sha_basis]
    _rehash(record)
    with pytest.raises(SilverRecordError, match="derived_record_bytes"):
        validate_silver_vault_record(record)

    wrong_content_basis = {
        **content_pair,
        "content_hash_basis": "derived_record_bytes",
    }
    record["derived_refs"] = [wrong_content_basis]
    _rehash(record)
    with pytest.raises(SilverRecordError, match="canonical_json_excluding_content_hash"):
        validate_silver_vault_record(record)


def test_validate_rejects_transform_ledger_in_a_fact() -> None:
    record = _text_record()
    record["payload"]["cleaning_packet"] = {"handles": []}
    with pytest.raises(SilverRecordError, match="transform ledger"):
        validate_silver_vault_record(record)


def test_validate_rejects_ledger_hidden_inside_observation() -> None:
    record = _metric_record()
    record["payload"]["observation"]["transform_ledger"] = [{"x": 1}]
    with pytest.raises(SilverRecordError, match="transform ledger"):
        validate_silver_vault_record(record)


def test_validate_rejects_observation_without_observation_object() -> None:
    record = _text_record()
    record["payload"] = {"not_an_observation": True}
    with pytest.raises(SilverRecordError, match=r"payload.observation"):
        validate_silver_vault_record(record)


def test_validate_rejects_observed_metric_with_null_value() -> None:
    record = _metric_record()
    record["payload"]["observation"]["metric_value"] = None
    with pytest.raises(SilverRecordError, match="observed metric requires"):
        validate_silver_vault_record(record)


def test_validate_rejects_non_observed_metric_with_value() -> None:
    record = _metric_record()
    record["payload"]["observation"]["metric_posture"]["kind"] = "unavailable_with_reason"
    with pytest.raises(SilverRecordError, match="must not carry a metric_value"):
        validate_silver_vault_record(record)


def test_validate_rejects_non_observed_metric_without_reason() -> None:
    record = _metric_record()
    observation = record["payload"]["observation"]
    observation["metric_posture"]["kind"] = "unavailable_with_reason"
    observation["metric_value"] = None
    with pytest.raises(SilverRecordError, match="requires a posture reason"):
        validate_silver_vault_record(record)


@pytest.mark.parametrize("kind", ["unavailable_with_reason", "not_attempted"])
def test_validate_accepts_non_observed_metric_with_reason_detail(kind: str) -> None:
    # The contract requires "a reason is present", not specifically reason_code; the
    # controlled signal is the posture kind. Both valid non-observed kinds whose reason is
    # in reason_detail (the creator_metric shape) must pass the front-door.
    record = _metric_record()
    observation = record["payload"]["observation"]
    observation["metric_posture"] = {
        "kind": kind,
        "reason_code": None,
        "reason_detail": "metric not rendered in the captured surface",
    }
    observation["metric_value"] = None
    _rehash(record)
    validate_silver_vault_record(record)


def test_validate_rejects_unknown_metric_posture_kind() -> None:
    # The posture kind must map to the closed source-capture vocabulary
    # (METRIC_POSTURE_KINDS); a free-text kind must not enter through the front-door.
    record = _metric_record()
    observation = record["payload"]["observation"]
    observation["metric_posture"] = {
        "kind": "banana",
        "reason_code": None,
        "reason_detail": "synthetic reason",
    }
    observation["metric_value"] = None
    with pytest.raises(SilverRecordError, match="metric_posture.kind must be one of"):
        validate_silver_vault_record(record)


def test_validate_rejects_observed_metric_with_reason_detail() -> None:
    # observed => both reason fields null (contract: "reason fields are absent/null").
    record = _metric_record()
    record["payload"]["observation"]["metric_posture"]["reason_detail"] = "should not be here"
    with pytest.raises(SilverRecordError, match="must not carry a posture reason"):
        validate_silver_vault_record(record)


def test_append_silver_record_writes_a_valid_record(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _commit_source(root)
    record = _text_record()
    path = append_silver_record(
        root,
        raw_anchor=_PACKET_ID,
        lane=_SILVER_LANE,
        record_id=record["record_id"],
        record=record,
    )
    assert path.is_file()
    assert path.parent == (
        root.path / "derived" / raw_shard(_PACKET_ID) / _PACKET_ID / _SILVER_LANE
    )


def test_append_silver_record_refuses_to_persist_a_blurred_record(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    record = _text_record()
    record["payload"]["cleaning_packet"] = {"handles": []}  # a ledger inside a fact
    with pytest.raises(SilverRecordError):
        append_silver_record(
            root,
            raw_anchor=_PACKET_ID,
            lane=_SILVER_LANE,
            record_id=record["record_id"],
            record=record,
        )
    # The blurred record never reached disk (validation raised before the write).
    lane_dir = root.path / "derived" / raw_shard(_PACKET_ID) / _PACKET_ID / _SILVER_LANE
    assert not lane_dir.exists() or not list(lane_dir.glob("*.json"))


def test_append_silver_record_rejects_header_target_mismatch(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    record = _text_record()
    with pytest.raises(SilverRecordError, match="write binding mismatch"):
        append_silver_record(
            root,
            raw_anchor=_PACKET_ID,
            lane="some_other_silver",
            record_id=record["record_id"],
            record=record,
        )


def test_append_silver_record_set_validates_all_members_before_write(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _commit_source(root)
    valid = _text_record()
    invalid = _text_record()
    invalid["record_id"] = valid["record_id"]
    invalid["lane_namespace"] = "second_silver"
    invalid["raw_refs"] = []
    _rehash(invalid)
    with pytest.raises(SilverRecordError, match="at least one resolvable"):
        append_silver_record_set(
            root,
            raw_anchor=_PACKET_ID,
            record_id=valid["record_id"],
            records={_SILVER_LANE: valid, "second_silver": invalid},
            completion_lane="silver_test_completion",
        )
    assert not root.lane_dir(
        subtree="derived", raw_anchor=_PACKET_ID, lane=_SILVER_LANE
    ).exists()


def test_append_silver_record_rejects_unresolved_source_before_write(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    record = _text_record()
    with pytest.raises(SilverRecordError, match="physically unresolved"):
        append_silver_record(
            root,
            raw_anchor=_PACKET_ID,
            lane=_SILVER_LANE,
            record_id=record["record_id"],
            record=record,
        )
    assert not root.lane_dir(
        subtree="derived", raw_anchor=_PACKET_ID, lane=_SILVER_LANE
    ).exists()


def test_append_silver_record_rejects_tampered_source_before_write(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    preserved = _commit_source(root)
    preserved.write_bytes(b"tampered")
    record = _text_record()
    with pytest.raises(SilverRecordError, match="tampered"):
        append_silver_record(
            root,
            raw_anchor=_PACKET_ID,
            lane=_SILVER_LANE,
            record_id=record["record_id"],
            record=record,
        )
    assert not root.lane_dir(
        subtree="derived", raw_anchor=_PACKET_ID, lane=_SILVER_LANE
    ).exists()


def test_append_silver_record_verifies_exact_derived_ref_and_hash(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _commit_source(root)
    source = _text_record()
    source_path = append_silver_record(
        root,
        raw_anchor=_PACKET_ID,
        lane=_SILVER_LANE,
        record_id=source["record_id"],
        record=source,
    )
    dependent = _metric_record()
    dependent["lane_namespace"] = "derived_metric_silver"
    dependent["raw_refs"] = []
    dependent["derived_refs"] = [
        {
            "raw_anchor": _PACKET_ID,
            "lane_namespace": _SILVER_LANE,
            "record_id": source["record_id"],
            "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
            "hash_basis": "derived_record_bytes",
            "content_hash": source["content_hash"],
            "content_hash_basis": source["content_hash_basis"],
        }
    ]
    _rehash(dependent)

    path = append_silver_record(
        root,
        raw_anchor=_PACKET_ID,
        lane=dependent["lane_namespace"],
        record_id=dependent["record_id"],
        record=dependent,
    )
    assert path.is_file()


@pytest.mark.parametrize("claim", ["sha256", "content_hash"])
def test_append_silver_record_rejects_wrong_derived_hash_before_write(
    tmp_path: Path, claim: str
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _commit_source(root)
    source = _text_record()
    source_path = append_silver_record(
        root,
        raw_anchor=_PACKET_ID,
        lane=_SILVER_LANE,
        record_id=source["record_id"],
        record=source,
    )
    dependent = _metric_record()
    dependent["lane_namespace"] = "derived_metric_silver"
    dependent["raw_refs"] = []
    ref = {
        "raw_anchor": _PACKET_ID,
        "lane_namespace": _SILVER_LANE,
        "record_id": source["record_id"],
        "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "hash_basis": "derived_record_bytes",
        "content_hash": source["content_hash"],
        "content_hash_basis": "canonical_json_excluding_content_hash",
    }
    ref[claim] = f"sha256:{'f' * 64}" if claim == "content_hash" else "f" * 64
    dependent["derived_refs"] = [ref]
    _rehash(dependent)

    with pytest.raises(SilverRecordError, match="tampered"):
        append_silver_record(
            root,
            raw_anchor=_PACKET_ID,
            lane=dependent["lane_namespace"],
            record_id=dependent["record_id"],
            record=dependent,
        )
    assert not root.record_path(
        subtree="derived",
        raw_anchor=_PACKET_ID,
        lane=dependent["lane_namespace"],
        record_id=dependent["record_id"],
    ).exists()


def test_append_silver_record_set_rejects_unresolved_member_before_any_write(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _commit_source(root)
    first = _text_record()
    second = _metric_record()
    second["record_id"] = first["record_id"]
    second["lane_namespace"] = "second_silver"
    second["raw_refs"] = [
        {"ref_type": "raw_packet", "packet_id": "01J00000000000000000000002"}
    ]
    _rehash(second)

    with pytest.raises(SilverRecordError, match="physically unresolved"):
        append_silver_record_set(
            root,
            raw_anchor=_PACKET_ID,
            record_id=first["record_id"],
            records={_SILVER_LANE: first, "second_silver": second},
            completion_lane="silver_test_completion",
        )
    assert not root.lane_dir(
        subtree="derived", raw_anchor=_PACKET_ID, lane=_SILVER_LANE
    ).exists()


def _legacy_fragrantica_record(root: DataLakeRoot) -> dict:
    source_body = b"legacy Fragrantica source"
    _commit_source(root, body=source_body)
    audit = {
        "record_id": "legacy_audit.json",
        "raw_anchor": _PACKET_ID,
        "lane_namespace": "cleaning_fragrantica_audit",
        "content_hash": "",
        "payload": {"audit": "legacy fixture"},
    }
    audit["content_hash"] = f"sha256:{silver_content_hash(audit)}"
    root.append_record(
        subtree="derived",
        raw_anchor=_PACKET_ID,
        lane=audit["lane_namespace"],
        record_id=audit["record_id"],
        data=(json.dumps(audit, sort_keys=True) + "\n").encode("utf-8"),
    )
    record = _text_record()
    record["producer_id"] = (
        "orca-harness.cleaning.fragrantica_lake."
        "derive_fragrantica_cleaning_into_lake#silver"
    )
    record["producer_schema_version"] = (
        "fragrantica_cleaning_silver_textobservation_v0"
    )
    record["raw_refs"] = [
        {
            "packet_id": _PACKET_ID,
            "file_id": "source",
            "relative_packet_path": "preserved/source.bin",
            "sha256": hashlib.sha256(source_body).hexdigest(),
            "hash_basis": "raw_stored_bytes",
        }
    ]
    record["derived_refs"] = [
        {
            "lane_namespace": audit["lane_namespace"],
            "record_id": audit["record_id"],
            "content_hash": audit["content_hash"],
            "content_hash_basis": "canonical_json_excluding_content_hash",
        }
    ]
    _rehash(record)
    return record


def test_legacy_fragrantica_refs_resolve_without_rewriting_immutable_record(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    record = _legacy_fragrantica_record(root)
    original = deepcopy(record)

    validate_silver_vault_record(record)
    authority = classify_silver_vault_record_sources(root, record)
    root.append_record(
        subtree="derived",
        raw_anchor=record["raw_anchor"],
        lane=record["lane_namespace"],
        record_id=record["record_id"],
        data=(json.dumps(record, sort_keys=True) + "\n").encode("utf-8"),
    )
    census = build_silver_observation_census(root)

    assert record == original
    assert "lineage_schema_version" not in record
    assert authority.status == CURRENT_SOURCE_BACKED_AUTHORITY
    assert authority.reason_code == "legacy_bytes_verified"
    assert census["totals"]["current_source_backed_silver_records"] == 1
    assert census["errors"] == []


def test_legacy_fragrantica_profile_is_read_only_at_strict_write_boundary(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    record = _legacy_fragrantica_record(root)

    with pytest.raises(SilverRecordError, match="read-only compatibility"):
        validate_silver_vault_record_for_write(record)
    with pytest.raises(SilverRecordError, match="read-only compatibility"):
        append_silver_record(
            root,
            raw_anchor=record["raw_anchor"],
            lane=record["lane_namespace"],
            record_id=record["record_id"],
            record=record,
        )


def test_unknown_producer_cannot_claim_legacy_missing_ref_fields(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    record = _legacy_fragrantica_record(root)
    record["producer_id"] = "unknown.producer"
    _rehash(record)

    authority = classify_silver_vault_record_sources(root, record)
    assert authority.status == INVALID_SILVER_AUTHORITY
    assert authority.reason_code == "invalid_silver_envelope"
