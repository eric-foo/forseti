"""Focused acceptance tests for the Company Surface physical vertical slice.

The nine owner-signed success signals are deliberately named in the tests so
the implementation remains bound to the purpose contract rather than to a
larger source corpus.  The final test is the offline Topicals holdout and uses
only facts already frozen in the product-learning case.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from capture_spine.company_aggregate_forward_signal.models import (
    COMPANY_AGGREGATE_OBSERVATION_SCHEMA_VERSION,
)
from data_lake.company_surface import (
    COMPANY_SURFACE_INDEX_PARTS,
    CompanySurfaceError,
    append_company_surface_logical_record,
    append_company_surface_logical_records,
    build_company_surface_view,
    company_activity_logical_record_from_observation,
    generate_company_surface_view_files,
    load_company_surface_records,
    map_company_surface_record,
    prove_company_surface_views_rebuildable,
    rebuild_company_surface_views,
)
from data_lake.root import DataLakeRoot
from data_lake.silver_census import build_silver_observation_census


PACKET_ID = "packet_company_fixture"
SOURCE_SHA = "a" * 64
TOPICALS_PACKET_ID = "01KV2M7XPZENAJJ74H1QVWCW6E"
TOPICALS_SOURCE_SHA = "db147fc02195e872957d588be376a935aee0fda584960dbd10d063912a0d981b"
TOPICALS_LOCATOR = (
    "https://web.archive.org/web/20210303084505/"
    "https://mytopicals.com/pages/careers"
)
FIXED_STAMP = {
    "generation_id": "company-surface-test-generation",
    "generated_at": "2026-07-15T00:00:00+00:00",
}


def _evidence(
    *,
    packet_id: str = PACKET_ID,
    sha256: str = SOURCE_SHA,
    locator: str = "https://example.test/company",
    span: str = "fixture#/company",
) -> dict:
    return {
        "packet_id": packet_id,
        "source_locator": locator,
        "sha256": sha256,
        "hash_basis": "raw_snapshot_body_bytes",
        "source_span": span,
    }


def _interval(
    start: str = "2025-01-01",
    *,
    precision: str = "day",
    end: str | None = None,
    end_state: str = "bounded",
    unknown_reason: str | None = None,
) -> dict:
    return {
        "start": start if precision != "unknown" else None,
        "start_precision": precision,
        "end": (end or start) if end_state == "bounded" else None,
        "end_precision": precision,
        "end_state": end_state,
        "unknown_reason": unknown_reason,
    }


def _logical(
    family: str,
    ref: str,
    payload: dict,
    *,
    anchors: list[str] | None = None,
    assertion_state: str | None = None,
    interval: dict | None = None,
    recorded_at: str = "2025-01-02T00:00:00Z",
    limitations: list[str] | None = None,
    alternatives: list[str] | None = None,
    corrects: list[str] | None = None,
    conflicts_with: list[str] | None = None,
    evidence: dict | None = None,
) -> dict:
    return {
        "record_ref": ref,
        "record_family": family,
        "raw_anchor": (evidence or _evidence())["packet_id"],
        "subject_anchors": anchors or ["org:acme"],
        "evidence_refs": [evidence or _evidence()],
        "assertion_state": assertion_state
        or ("resolved" if family in {"subject_assertion", "relationship_assertion"} else "not_applicable"),
        "effective_interval": interval or _interval(),
        "captured_at": "2025-01-01T12:00:00Z",
        "recorded_at": recorded_at,
        "limitations": limitations or [],
        "alternatives": alternatives or [],
        "corrects": corrects or [],
        "supersedes": [],
        "conflicts_with": conflicts_with or [],
        "source_surface": "company_fixture",
        "producer_row_kind": f"company_{family}",
        "family_payload": payload,
    }


def _subject(
    ref: str = "subject.acme",
    *,
    subject: str = "org:acme",
    state: str = "resolved",
    recorded_at: str = "2025-01-02T00:00:00Z",
    corrects: list[str] | None = None,
    interval: dict | None = None,
    evidence: dict | None = None,
) -> dict:
    return _logical(
        "subject_assertion",
        ref,
        {
            "raw_identifier": subject.removeprefix("org:").removeprefix("brand:"),
            "asserted_subject": subject,
            "asserted_subject_kind": "Brand" if subject.startswith("brand:") else "Org",
            "competing_candidates": [],
        },
        anchors=[subject],
        assertion_state=state,
        interval=interval,
        recorded_at=recorded_at,
        corrects=corrects,
        evidence=evidence,
    )


def _activity(
    ref: str = "activity.acme",
    *,
    subject: str = "org:acme",
    subject_assertion_ref: str = "subject.acme",
    interval: dict | None = None,
    evidence: dict | None = None,
) -> dict:
    return _logical(
        "company_activity_link",
        ref,
        {
            "observation_ref": f"observation.{ref}",
            "receipt_ref": (evidence or _evidence())["packet_id"],
            "subject_assertion_ref": subject_assertion_ref,
            "activity_kind": "org_motion",
            "capture_posture": "offline_fixture",
            "source_schema_version": COMPANY_AGGREGATE_OBSERVATION_SCHEMA_VERSION,
            "reobserves_observation_id": None,
        },
        anchors=[subject],
        interval=interval,
        evidence=evidence,
    )


def _query(
    mode: str,
    *,
    subject: str = "org:acme",
    effective: str = "2025-01-01T12:00:00Z",
    cutoff: str = "2025-12-31T23:59:59Z",
) -> dict:
    return {
        "mode": mode,
        "anchor_subject": subject,
        "effective_boundary": effective,
        "knowledge_cutoff": cutoff,
    }


def test_signal_1_company_reality_is_reconstructable_through_silver_front_door(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    paths = append_company_surface_logical_records(root, [_subject(), _activity()])
    assert len(paths) == 2
    records = load_company_surface_records(root)
    view = build_company_surface_view(records, _query("current"))
    assert {item["record"]["record_family"] for item in view["resolved_records"]} == {
        "company_activity_link",
        "subject_assertion",
    }
    assert view["non_authoritative"] is True


def test_signal_2_history_is_preserved_and_restated_differs_from_as_known() -> None:
    original = _subject(ref="subject.acme.old", subject="org:acme", state="resolved")
    corrected = _subject(
        ref="subject.acme.corrected",
        subject="org:acme",
        state="unresolved",
        recorded_at="2025-06-01T00:00:00Z",
        corrects=["subject.acme.old"],
    )
    records = [*map_company_surface_record(original), *map_company_surface_record(corrected)]

    as_known = build_company_surface_view(
        records,
        _query("historical_as_known", cutoff="2025-05-31T23:59:59Z"),
    )
    restated = build_company_surface_view(
        records,
        _query("historical_restated", cutoff="2025-12-31T23:59:59Z"),
    )

    assert len(as_known["resolved_records"]) == 1
    assert as_known["visible_residuals"] == []
    assert restated["resolved_records"] == []
    assert restated["visible_residuals"][0]["reason"] == "assertion_unresolved"
    assert any(item["reason"] == "corrected_or_superseded" for item in restated["exclusions"])


def test_signal_3_every_material_statement_is_inspectable_and_coarse_time_survives() -> None:
    mapped = map_company_surface_record(
        _activity(
            interval=_interval("2025-01", precision="month"),
            evidence=_evidence(span="snapshot#/roles/0"),
        )
    )[0]
    common = mapped["payload"]["relationship"]
    assert mapped["raw_refs"][0]["source_span"] == "snapshot#/roles/0"
    assert common["effective_interval"]["start_precision"] == "month"
    assert common["subject_anchors"] == ["org:acme"]
    assert "limitations" in common and "alternatives" in common


def test_signal_4_evidence_is_reusable_in_all_three_query_modes() -> None:
    records = [*map_company_surface_record(_subject()), *map_company_surface_record(_activity())]
    outputs = [build_company_surface_view(records, _query(mode)) for mode in (
        "current",
        "historical_restated",
        "historical_as_known",
    )]
    assert {item["view_mode"] for item in outputs} == {
        "current",
        "historical_restated",
        "historical_as_known",
    }
    assert len({item["resolved_records"][0]["content_hash"] for item in outputs}) == 1


def test_signal_5_center_rejects_decision_gtm_and_contact_fields() -> None:
    for forbidden in ("pain_score", "recommended_action", "pitch", "contact"):
        record = _subject()
        record["family_payload"][forbidden] = "must remain downstream"
        with pytest.raises(CompanySurfaceError, match="decision/GTM field is forbidden"):
            map_company_surface_record(record)


def test_signal_6_contradictions_are_visible_without_resolving_them() -> None:
    first = _subject(ref="subject.acme.first")
    second = _subject(ref="subject.acme.second", state="ambiguous")
    second["conflicts_with"] = ["subject.acme.first"]
    records = [*map_company_surface_record(first), *map_company_surface_record(second)]
    view = build_company_surface_view(records, _query("current"))
    assert view["conflicts"][0]["edge_type"] == "conflicts_with_record"
    assert view["visible_residuals"][0]["reason"] == "assertion_ambiguous"


def test_signal_7_unknowns_and_failures_remain_visible_not_false_zero() -> None:
    failure = _logical(
        "coverage_failure_marker",
        "coverage.acme.linkedin",
        {
            "surface": "linkedin_company_page",
            "coverage_state": "failed",
            "capture_posture": "not_attempted",
            "receipt_ref": PACKET_ID,
            "missing_boundary": "no authorized source adapter",
        },
        limitations=["No headcount claim is available."],
    )
    view = build_company_surface_view(map_company_surface_record(failure), _query("current"))
    marker = view["coverage_and_failure_markers"][0]["record"]
    assert marker["family_payload"]["coverage_state"] == "failed"
    assert "value" not in marker["family_payload"]
    assert marker["limitations"] == ["No headcount claim is available."]


def test_signal_8_four_families_extend_one_closed_silver_foundation() -> None:
    records = [
        _subject(),
        _logical(
            "relationship_assertion",
            "relationship.acme-brand",
            {
                "subject": "brand:acme",
                "relationship_kind": "owned_by",
                "object": "org:acme",
                "source_qualifiers": [],
            },
            anchors=["brand:acme", "org:acme"],
        ),
        _activity(),
        _logical(
            "coverage_failure_marker",
            "coverage.acme",
            {
                "surface": "company_site",
                "coverage_state": "available",
                "capture_posture": "offline_fixture",
                "receipt_ref": PACKET_ID,
                "missing_boundary": None,
            },
        ),
    ]
    mapped = [map_company_surface_record(record)[0] for record in records]
    assert {item["record_kind"] for item in mapped} == {"observation", "relationship"}
    assert {item["payload_kind"] for item in mapped} == {
        "CompanySubjectAssertion",
        "CompanyRelationshipAssertion",
        "CompanyActivityLink",
        "CompanyCoverageMarker",
    }


def test_signal_9_current_traceable_observations_do_not_embed_gtm_conclusions() -> None:
    output = json.dumps(map_company_surface_record(_activity()), sort_keys=True).lower()
    assert "company_fixture" in output and SOURCE_SHA in output
    for forbidden in ("pain_score", "recommended_action", "preferred_intervention", "outreach"):
        assert forbidden not in output


def test_deterministic_rebuild_reproduces_view_and_manifest_bytes(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    append_company_surface_logical_records(root, [_subject(), _activity()])
    queries = [_query(mode) for mode in (
        "current",
        "historical_restated",
        "historical_as_known",
    )]
    records = load_company_surface_records(root)
    first = generate_company_surface_view_files(records, queries, stamp=FIXED_STAMP)
    second = generate_company_surface_view_files(records, queries, stamp=FIXED_STAMP)
    assert first == second

    result = rebuild_company_surface_views(root, queries, stamp=FIXED_STAMP)
    assert result == {
        "status": "rebuilt",
        "view_modes": ["current", "historical_as_known", "historical_restated"],
        "generation_id": FIXED_STAMP["generation_id"],
        "file_count": 6,
    }
    assert prove_company_surface_views_rebuildable(root)["status"] == "proven"
    target = root._within(*COMPANY_SURFACE_INDEX_PARTS)
    assert (target / "views" / "current.json").read_bytes() == first["views/current.json"]
    assert (target / "manifests" / "current.json").read_bytes() == first[
        "manifests/current.json"
    ]


def test_company_surface_census_lane_is_honestly_inactive_without_source_access(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    census = build_silver_observation_census(root)
    state = next(
        item for item in census["lane_states"] if item["lane"] == "company_surface_silver"
    )
    assert state["state"] == "intentionally_inactive"
    assert state["eligible_capture_packets"] == 0


def test_topicals_offline_product_learning_holdout_uses_same_public_path(tmp_path: Path) -> None:
    """No buyer/readiness claim: one frozen snapshot and one hiring-intent row only."""
    root = DataLakeRoot.for_test(tmp_path / "lake")
    evidence = _evidence(
        packet_id=TOPICALS_PACKET_ID,
        sha256=TOPICALS_SOURCE_SHA,
        locator=TOPICALS_LOCATOR,
        span="careers snapshot: Supply Chain Manager (Full Time)",
    )
    org_assertion = _subject(
        ref="subject.topicals.org",
        subject="org:topicals",
        state="provisional",
        interval=_interval("2021-03-03", precision="day"),
        recorded_at="2021-03-04T00:00:00Z",
        evidence=evidence,
    )
    brand_assertion = _subject(
        ref="subject.topicals.brand",
        subject="brand:topicals",
        state="resolved",
        interval=_interval("2021-03-03", precision="day"),
        recorded_at="2021-03-04T00:00:00Z",
        evidence=evidence,
    )
    observation = {
        "observation_id": "topicals.org_motion.2021-03-03.supply_chain_manager",
        "entity_key": "org:topicals",
        "raw_entity_name": "Topicals",
        "source_tag": "archived_company_careers_page",
        "capture_posture": "offline_frozen_packet",
        "signal_kind": "open_role",
        "source_effective_time": {
            "value": "2021-03-03T08:45:05Z",
            "precision": "exact",
            "unknown_reason": None,
        },
        "filing_time": {
            "value": None,
            "precision": "unknown",
            "unknown_reason": "careers page is not a filing",
        },
        "as_of_time": {
            "value": "2021-03-03",
            "precision": "day",
            "unknown_reason": None,
        },
        "captured_at": "2026-07-01T00:00:00Z",
        "provenance": [evidence],
        "limitations": [
            "Single frozen careers-page snapshot; no earlier baseline.",
            "One advertised role is hiring intent, not proof of a net headcount addition.",
            "The evidence does not resolve the operating or legal Org behind the Topicals Brand.",
        ],
        "schema_version": COMPANY_AGGREGATE_OBSERVATION_SCHEMA_VERSION,
        "headcount": None,
        "size_band": None,
        "follower_count": None,
        "open_role_count": {
            "posture": "observed",
            "value": 1,
            "unit": "role",
            "source_field": "Supply Chain Manager (Full Time)",
            "reason": None,
            "zero_basis": None,
        },
        "signal_details": ["Supply Chain Manager (Full Time)"],
        "reobserves_observation_id": None,
    }
    activity = company_activity_logical_record_from_observation(
        observation,
        subject_assertion_ref="subject.topicals.org",
        recorded_at="2026-07-01T00:00:00Z",
    )
    append_company_surface_logical_records(root, [brand_assertion, org_assertion, activity])
    records = load_company_surface_records(root)
    queries = [
        _query(
            mode,
            subject="org:topicals",
            effective="2021-03-03T08:45:05Z",
            cutoff="2026-07-01T00:00:00Z",
        )
        for mode in ("current", "historical_restated", "historical_as_known")
    ]
    outputs = [build_company_surface_view(records, query) for query in queries]

    assert all(output["resolved_records"] == [] for output in outputs)
    assert all(
        {item["reason"] for item in output["visible_residuals"]}
        == {"assertion_provisional", "subject_assertion_not_resolved"}
        for output in outputs
    )
    brand_view = build_company_surface_view(
        records,
        _query(
            "current",
            subject="brand:topicals",
            effective="2021-03-03T08:45:05Z",
            cutoff="2026-07-01T00:00:00Z",
        ),
    )
    assert len(brand_view["resolved_records"]) == 1
    assert not any(
        item["record"]["record_family"] == "relationship_assertion"
        for output in [*outputs, brand_view]
        for item in output["resolved_records"]
    )
    serialized = json.dumps(outputs, sort_keys=True)
    assert TOPICALS_SOURCE_SHA in serialized and TOPICALS_LOCATOR in serialized
    assert "hiring intent, not proof" in serialized
    assert "willingness_to_pay" not in serialized and "buyer_proof" not in serialized
