"""Silver Vault envelope validator + validating write front-door.

Proves the no-blur core is enforced by CODE: a blurred Silver record is rejected,
and the front-door refuses to persist one (raises before any bytes are written).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from data_lake.root import DataLakeRoot, raw_shard
from data_lake.silver_record import (
    SilverRecordError,
    append_silver_record,
    validate_silver_vault_record,
)

_PACKET_ID = "01TESTSILVERENVELOPE"
_SILVER_LANE = "cleaning_fragrantica_silver"


def _text_record() -> dict:
    return {
        "record_id": "rec_text.json",
        "raw_anchor": _PACKET_ID,
        "schema_version": "silver_vault_record_v0",
        "record_kind": "observation",
        "payload_kind": "TextObservation",
        "content_hash": "sha256:deadbeef",
        "payload": {
            "observation": {
                "text_artifact_type": "review_body",
                "text_value": "This perfume died young.",
            }
        },
    }


def _metric_record() -> dict:
    return {
        "record_id": "rec_metric.json",
        "raw_anchor": _PACKET_ID,
        "schema_version": "silver_vault_record_v0",
        "record_kind": "observation",
        "payload_kind": "MetricObservation",
        "content_hash": "sha256:deadbeef",
        "payload": {
            "observation": {
                "metric_name": "review_rating",
                "metric_value": 5,
                "metric_posture": {"kind": "observed", "reason_code": None, "reason_detail": None},
            }
        },
    }


def _metric_set_record() -> dict:
    return {
        "record_id": "rec_metric_set.json",
        "raw_anchor": _PACKET_ID,
        "schema_version": "silver_vault_record_v0",
        "record_kind": "observation",
        "payload_kind": "MetricObservationSet",
        "content_hash": "sha256:deadbeef",
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


def test_validate_accepts_well_formed_text_and_metric_observations() -> None:
    validate_silver_vault_record(_text_record())
    validate_silver_vault_record(_metric_record())
    validate_silver_vault_record(_metric_set_record())


def test_validate_metric_set_rejects_row_count_drift() -> None:
    record = _metric_set_record()
    record["payload"]["observation"]["row_count"] = 2
    with pytest.raises(SilverRecordError, match="row_count"):
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
