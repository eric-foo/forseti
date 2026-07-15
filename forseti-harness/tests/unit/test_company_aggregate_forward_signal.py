from __future__ import annotations

import copy

import pytest

from capture_spine.company_aggregate_forward_signal import (
    CompanyAggregateObservationError,
    validate_company_aggregate_observation,
)


def _observation() -> dict:
    return {
        "schema_version": "company_aggregate_observation_v0",
        "observation_id": "org-motion-2021-03-03",
        "entity_key": "org:topicals",
        "raw_entity_name": "Topicals",
        "source_tag": "first_party_archive",
        "capture_posture": "first_party_archive_holdout",
        "signal_kind": "hiring_intent",
        "source_effective_time": {
            "value": "2021-03-03",
            "precision": "day",
            "unknown_reason": None,
        },
        "filing_time": {
            "value": None,
            "precision": "unknown",
            "unknown_reason": "not a filing source",
        },
        "as_of_time": {
            "value": "2021-03-03",
            "precision": "day",
            "unknown_reason": None,
        },
        "captured_at": "2026-06-14T00:00:00Z",
        "provenance": [
            {
                "packet_id": "01KV2M7XPZENAJJ74H1QVWCW6E",
                "source_locator": "https://web.archive.org/web/20210303084505/https://mytopicals.com/pages/careers",
                "sha256": "db147fc02195e872957d588be376a935aee0fda584960dbd10d063912a0d981b",
                "hash_basis": "raw_snapshot_body_bytes",
                "source_span": "one Supply Chain Manager role",
            }
        ],
        "limitations": ["single role and single snapshot; not net headcount adds"],
        "headcount": None,
        "size_band": None,
        "follower_count": None,
        "open_role_count": {
            "posture": "observed",
            "value": 1,
            "unit": "open_roles",
            "source_field": "careers_page_open_role",
            "reason": None,
            "zero_basis": None,
        },
        "signal_details": ["Supply Chain Manager (Full Time)"],
        "reobserves_observation_id": None,
    }


def test_company_aggregate_schema_accepts_inspectable_observation() -> None:
    validate_company_aggregate_observation(_observation())


@pytest.mark.parametrize(
    ("mutation", "match"),
    [
        (lambda row: row.pop("provenance"), "provenance"),
        (lambda row: row.pop("capture_posture"), "capture_posture"),
        (lambda row: row.pop("source_effective_time"), "source_effective_time"),
    ],
)
def test_company_aggregate_schema_fails_closed_on_missing_provenance_time_or_posture(
    mutation, match: str
) -> None:
    row = _observation()
    mutation(row)
    with pytest.raises(CompanyAggregateObservationError, match=match):
        validate_company_aggregate_observation(row)


def test_company_aggregate_schema_rejects_absence_encoded_as_zero() -> None:
    row = _observation()
    row["headcount"] = {
        "posture": "unavailable_with_reason",
        "value": 0,
        "unit": "employees",
        "source_field": "not_rendered",
        "reason": "source did not report headcount",
        "zero_basis": None,
    }
    with pytest.raises(CompanyAggregateObservationError, match="absence must never be zero"):
        validate_company_aggregate_observation(row)


def test_company_aggregate_schema_requires_basis_for_genuine_observed_zero() -> None:
    row = _observation()
    row["open_role_count"]["value"] = 0
    with pytest.raises(CompanyAggregateObservationError, match="zero_basis"):
        validate_company_aggregate_observation(row)
    row["open_role_count"]["zero_basis"] = "source explicitly displayed zero open roles"
    validate_company_aggregate_observation(row)


def test_reobservation_is_new_append_only_row() -> None:
    first = _observation()
    later = copy.deepcopy(first)
    later["observation_id"] = "org-motion-2021-04-01"
    later["source_effective_time"]["value"] = "2021-04-01"
    later["as_of_time"]["value"] = "2021-04-01"
    later["reobserves_observation_id"] = first["observation_id"]
    validate_company_aggregate_observation(first)
    validate_company_aggregate_observation(later)
    assert later["observation_id"] != later["reobserves_observation_id"]
