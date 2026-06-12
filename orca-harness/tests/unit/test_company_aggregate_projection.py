from __future__ import annotations

import pytest

from source_capture.company_aggregate.entity_resolution_port import (
    DEFAULT_RESOLUTION_MAP,
    PassthroughNullResolutionMap,
    ResolutionMap,
    ResolutionOutcome,
)
from source_capture.company_aggregate.observation import (
    EdgarHeadcountObservation,
    EdgarObservationKey,
    ExtractionProvenance,
    ExtractionSpan,
    HeadcountSupersession,
    ObservationRef,
)
from source_capture.company_aggregate.projection import (
    CompanyHeadcountProjection,
    HeadcountPoint,
    project_company_headcount,
)
from source_capture.models import (
    VisibleFactStatus,
    known_fact,
    not_applicable,
    unknown_with_reason,
)

APPLE_CIK = "0000320193"


def _obs(
    *,
    cik: str = APPLE_CIK,
    period: str,
    accession: str,
    count_int: int | None,
    basis: str = "full_time",
    quality: str = "approximate",
    filing_date: str = "2023-11-03",
    run_id: str = "01HRUN0000000000000000000",
    supersedes: HeadcountSupersession | None = None,
) -> EdgarHeadcountObservation:
    if count_int is None:
        employee_count = unknown_with_reason("no count extracted")
        value_quality = not_applicable("no value extracted")
        measurement_basis = not_applicable("no value extracted")
        char_end = 0
        matched = "(none)"
    else:
        employee_count = known_fact(f"{count_int:,}")
        value_quality = known_fact(quality)
        measurement_basis = known_fact(basis)
        char_end = 10
        matched = "matched"
    return EdgarHeadcountObservation(
        key=EdgarObservationKey(source="sec_edgar", cik=cik, accession_number=accession, period_of_report=period),
        form_type="10-K",
        filing_date=filing_date,
        employee_count=employee_count,
        employee_count_int=count_int,
        value_quality=value_quality,
        measurement_basis=measurement_basis,
        extraction_span=ExtractionSpan(
            preserved_file_id="file_01",
            relative_packet_path="raw/10k.htm",
            source_sha256="a" * 64,
            locator_kind="char_offset_range",
            char_start=0,
            char_end=char_end,
            excerpt_sha256="b" * 64,
            matched_text=matched,
        ),
        extraction=ExtractionProvenance(
            parser_method="edgar_item1_employee_regex",
            parser_version="v0",
            ruleset_sha256="c" * 64,
            run_id=run_id,
            derived_at="2026-06-12T00:00:00Z",
        ),
        supersedes=supersedes,
        packet_id=f"pkt-{accession}",
        evidence_slice_id="edgar_primary_filing",
        manifest_sha256="d" * 64,
    )


# ---- the v0 default: a filer-level UNRESOLVED trend (AR-04/05) ----

def test_passthrough_null_is_an_unresolved_filer_level_series():
    observations = [
        _obs(period="2021-09-25", accession="acc-2021", count_int=154000),
        _obs(period="2023-09-30", accession="acc-2023", count_int=161000),
        _obs(period="2022-09-24", accession="acc-2022", count_int=164000),
    ]
    projections = project_company_headcount(observations)
    assert len(projections) == 1
    projection = projections[0]

    # identity honesty: provisional filer key, never a canonical entity_key
    assert projection.resolution_state == "unresolved"
    assert projection.entity_key is None
    assert projection.provisional_filer_key == f"sec_edgar:CIK{APPLE_CIK}"
    assert projection.source == "sec_edgar"

    # version binding is pinned (AR-06)
    assert projection.map_version == "passthrough_null_v0"
    assert projection.resolver_version == "v0"
    assert projection.event_ordering == "period_of_report_asc"
    assert projection.conflict_rule == "surface_both"

    # ordered ascending by period_of_report
    assert [p.period_of_report for p in projection.points] == ["2021-09-25", "2022-09-24", "2023-09-30"]
    assert [p.employee_count_int for p in projection.points] == [154000, 164000, 161000]
    assert all(p.point_state == "single" for p in projection.points)

    # each point traces back to its observation (the ECR binding handle is preserved)
    first = projection.points[0]
    assert first.observation_refs[0].packet_id == "pkt-acc-2021"
    assert first.observation_refs[0].evidence_slice_id == "edgar_primary_filing"

    assert CompanyHeadcountProjection.model_validate(projection.model_dump(mode="json")) == projection


def test_descending_order_is_honored():
    observations = [
        _obs(period="2021-09-25", accession="a1", count_int=154000),
        _obs(period="2023-09-30", accession="a3", count_int=161000),
    ]
    projection = project_company_headcount(observations, event_ordering="period_of_report_desc")[0]
    assert [p.period_of_report for p in projection.points] == ["2023-09-30", "2021-09-25"]


def test_default_map_is_the_passthrough_null():
    assert isinstance(DEFAULT_RESOLUTION_MAP, PassthroughNullResolutionMap)
    assert isinstance(DEFAULT_RESOLUTION_MAP, ResolutionMap)  # satisfies the port


def test_empty_log_projects_to_nothing():
    assert project_company_headcount([]) == []


# ---- absence is a visible gap in the trend, never a silent zero ----

def test_absent_count_is_an_honest_gap_point():
    observations = [_obs(period="2023-09-30", accession="acc", count_int=None)]
    point = project_company_headcount(observations)[0].points[0]
    assert point.point_state == "single"
    assert point.employee_count_int is None
    assert point.employee_count.status is VisibleFactStatus.UNKNOWN_WITH_REASON


# ---- conflict vs identical-collapse at the same period ----

def test_conflicting_observations_same_period_surface_both():
    observations = [
        _obs(period="2023-09-30", accession="acc-A", count_int=161000),
        _obs(period="2023-09-30", accession="acc-B", count_int=200000),
    ]
    point = project_company_headcount(observations)[0].points[0]
    assert point.point_state == "conflict"
    assert point.employee_count_int is None
    assert point.value_quality.value == "ambiguous"
    assert {ref.employee_count_int for ref in point.observation_refs} == {161000, 200000}


def test_identical_re_derivations_collapse_to_a_single_point():
    observations = [
        _obs(period="2023-09-30", accession="acc-A", count_int=161000),
        _obs(period="2023-09-30", accession="acc-B", count_int=161000),
    ]
    point = project_company_headcount(observations)[0].points[0]
    assert point.point_state == "single"
    assert point.employee_count_int == 161000
    assert len(point.observation_refs) == 2  # both contributors recorded


def test_collapsed_point_takes_conservative_deterministic_quality():
    # same value, disagreeing quality -> point is approximate (never overstates precision),
    # and is order-independent (F-03)
    observations = [
        _obs(period="2023-09-30", accession="acc-A", count_int=161000, quality="exact"),
        _obs(period="2023-09-30", accession="acc-B", count_int=161000, quality="approximate"),
    ]
    point = project_company_headcount(observations)[0].points[0]
    assert point.point_state == "single"
    assert point.employee_count_int == 161000
    assert point.value_quality.value == "approximate"
    # reversing the input does not change the collapsed quality
    reversed_point = project_company_headcount(list(reversed(observations)))[0].points[0]
    assert reversed_point.value_quality.value == "approximate"


# ---- supersession collapses to the active reading, keeps the prior off the point ----

def test_supersedes_collapses_to_the_active_reading():
    prior = _obs(period="2023-09-30", accession="acc-orig", count_int=161000)
    superseding = _obs(
        period="2023-09-30",
        accession="acc-amend",
        count_int=162500,
        supersedes=HeadcountSupersession(
            relationship="supersede",
            prior=ObservationRef(key=prior.key, parser_version="v0", run_id=prior.extraction.run_id),
            reason="10-K/A restated the human-capital count",
        ),
    )
    point = project_company_headcount([prior, superseding])[0].points[0]
    assert point.point_state == "single"
    assert point.employee_count_int == 162500  # the superseding reading wins
    assert [ref.accession_number for ref in point.superseded_refs] == ["acc-orig"]


# ---- an injected (spine stand-in) resolved map flows entity_key + groups by it ----

class _StubResolvedMap:
    """A spine stand-in injected for the test -- the lane only APPLIES it, never authors it."""

    map_version = "stub_resolved_v1"
    resolver_version = "v1"

    def __init__(self, mapping: dict[str, str]) -> None:
        self._mapping = mapping

    def resolve(self, *, source: str, cik: str) -> ResolutionOutcome:
        entity_key = self._mapping.get(cik)
        if entity_key:
            return ResolutionOutcome(
                provisional_filer_key=f"{source}:CIK{cik}",
                entity_key=entity_key,
                resolution_state="resolved",
                note="stub",
            )
        return ResolutionOutcome(provisional_filer_key=f"{source}:CIK{cik}", entity_key=None, resolution_state="unresolved")


def test_resolved_map_populates_entity_key_and_pins_its_versions():
    observations = [_obs(period="2023-09-30", accession="acc", count_int=161000)]
    resolved = _StubResolvedMap({APPLE_CIK: "entity:apple_inc"})
    projection = project_company_headcount(observations, resolution_map=resolved)[0]
    assert projection.resolution_state == "resolved"
    assert projection.entity_key == "entity:apple_inc"
    assert projection.map_version == "stub_resolved_v1"
    assert projection.resolver_version == "v1"


def test_resolved_map_merges_two_filers_into_one_entity_lane():
    observations = [
        _obs(cik="0000320193", period="2022-09-24", accession="a1", count_int=164000),
        _obs(cik="0000999999", period="2023-09-30", accession="a2", count_int=170000),
    ]
    resolved = _StubResolvedMap({"0000320193": "entity:acme", "0000999999": "entity:acme"})
    projections = project_company_headcount(observations, resolution_map=resolved)
    assert len(projections) == 1  # both filers fold into the one resolved entity lane
    assert projections[0].entity_key == "entity:acme"
    assert [p.period_of_report for p in projections[0].points] == ["2022-09-24", "2023-09-30"]


# ---- the AR-05 identity-leak guard is enforced in code ----

def test_unresolved_outcome_may_not_carry_entity_key():
    with pytest.raises(ValueError, match="canonical entity_key"):
        ResolutionOutcome(provisional_filer_key="sec_edgar:CIK1", entity_key="entity:x", resolution_state="unresolved")


def test_resolved_outcome_requires_entity_key():
    with pytest.raises(ValueError, match="must carry a non-empty entity_key"):
        ResolutionOutcome(provisional_filer_key="sec_edgar:CIK1", resolution_state="resolved")


def test_unresolved_projection_may_not_carry_entity_key():
    with pytest.raises(ValueError, match="canonical entity_key"):
        CompanyHeadcountProjection(
            provisional_filer_key="sec_edgar:CIK1",
            entity_key="entity:x",
            resolution_state="unresolved",
            source="sec_edgar",
            map_version="passthrough_null_v0",
            resolver_version="v0",
            event_ordering="period_of_report_asc",
            conflict_rule="surface_both",
        )


# ---- bad fold parameters are rejected ----

def test_unknown_event_ordering_is_rejected():
    with pytest.raises(ValueError, match="event_ordering"):
        project_company_headcount([], event_ordering="random")


def test_unknown_conflict_rule_is_rejected():
    with pytest.raises(ValueError, match="conflict_rule"):
        project_company_headcount([], conflict_rule="pick_latest")
