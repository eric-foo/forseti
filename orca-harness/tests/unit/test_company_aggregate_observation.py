from __future__ import annotations

import pytest
from pydantic import ValidationError

from source_capture.company_aggregate import (
    EDGAR_HEADCOUNT_OBSERVATION_SCHEMA_VERSION,
    EdgarHeadcountObservation,
    EdgarObservationKey,
    ExtractionProvenance,
    ExtractionSpan,
    HeadcountSupersession,
    ObservationRef,
)
from source_capture.models import (
    VisibleFact,
    VisibleFactStatus,
    known_fact,
    not_applicable,
    unknown_with_reason,
)


def _key(**overrides) -> EdgarObservationKey:
    kwargs = dict(
        source="sec_edgar",
        cik="0000320193",
        accession_number="0000320193-23-000106",
        period_of_report="2023-09-30",
    )
    kwargs.update(overrides)
    return EdgarObservationKey(**kwargs)


def _span(**overrides) -> ExtractionSpan:
    kwargs = dict(
        preserved_file_id="file_01",
        relative_packet_path="raw/01_10k.htm",
        source_sha256="a" * 64,
        locator_kind="char_offset_range",
        char_start=1000,
        char_end=1080,
        excerpt_sha256="b" * 64,
        matched_text="approximately 161,000 full-time employees",
    )
    kwargs.update(overrides)
    return ExtractionSpan(**kwargs)


def _prov(**overrides) -> ExtractionProvenance:
    kwargs = dict(
        parser_method="edgar_item1_employee_regex",
        parser_version="v0",
        ruleset_sha256="c" * 64,
        run_id="01HRUN0000000000000000000",
        derived_at="2026-06-12T00:00:00Z",
    )
    kwargs.update(overrides)
    return ExtractionProvenance(**kwargs)


def _obs(**overrides) -> EdgarHeadcountObservation:
    kwargs = dict(
        key=_key(),
        form_type="10-K",
        filing_date="2023-11-03",
        employee_count=known_fact("161,000"),
        employee_count_int=161000,
        value_quality=known_fact("approximate"),
        measurement_basis=known_fact("full_time"),
        extraction_span=_span(),
        extraction=_prov(),
        packet_id="pkt-1",
        evidence_slice_id="s_filing",
        manifest_sha256="d" * 64,
    )
    kwargs.update(overrides)
    return EdgarHeadcountObservation(**kwargs)


# ---- happy paths ----

def test_valid_known_observation_constructs():
    obs = _obs()
    assert obs.schema_version == EDGAR_HEADCOUNT_OBSERVATION_SCHEMA_VERSION
    assert obs.employee_count_int == 161000
    assert obs.key.canonical_key() == "sec_edgar|0000320193|0000320193-23-000106|2023-09-30"


def test_not_extracted_observation_constructs():
    # An honest not-found reading: a named absence, never a silent null int.
    obs = _obs(
        employee_count=unknown_with_reason("no employee-count phrase matched in Item 1"),
        employee_count_int=None,
        value_quality=not_applicable("no value extracted"),
        measurement_basis=not_applicable("no value extracted"),
    )
    assert obs.employee_count.status is VisibleFactStatus.UNKNOWN_WITH_REASON
    assert obs.employee_count_int is None


def test_valid_supersession_constructs():
    prior = ObservationRef(key=_key(), parser_version="v0", run_id="01HOLDRUN0000000000000000")
    obs = _obs(
        extraction=_prov(parser_version="v1"),
        supersedes=HeadcountSupersession(
            relationship="supersede", prior=prior, reason="re-extracted with parser v1"
        ),
    )
    assert obs.supersedes is not None
    assert obs.supersedes.relationship == "supersede"


# ---- honesty invariant: no silent int, no fake value ----

def test_known_count_requires_parsed_int():
    with pytest.raises(ValidationError, match="must carry a parsed employee_count_int"):
        _obs(employee_count_int=None)


def test_absent_count_forbids_int():
    with pytest.raises(ValidationError, match="only when employee_count.status is KNOWN"):
        _obs(
            employee_count=unknown_with_reason("not found"),
            employee_count_int=161000,
            value_quality=not_applicable("no value"),
            measurement_basis=not_applicable("no value"),
        )


def test_quality_exact_or_approximate_requires_known_count():
    with pytest.raises(ValidationError, match="requires a KNOWN employee_count"):
        _obs(
            employee_count=unknown_with_reason("not found"),
            employee_count_int=None,
            value_quality=known_fact("approximate"),
            measurement_basis=not_applicable("no value"),
        )


def test_ambiguous_quality_forbids_known_count():
    with pytest.raises(ValidationError, match="ambiguous"):
        _obs(value_quality=known_fact("ambiguous"))


def test_ambiguous_quality_pairs_with_unknown_count():
    obs = _obs(
        employee_count=unknown_with_reason("two competing figures in Item 1"),
        employee_count_int=None,
        value_quality=known_fact("ambiguous"),
        measurement_basis=not_applicable("unresolved"),
    )
    assert obs.value_quality.value == "ambiguous"


# ---- closed vocabularies ----

def test_value_quality_closed():
    with pytest.raises(ValidationError, match="value_quality known value must be one of"):
        _obs(value_quality=known_fact("pretty_sure"))


def test_measurement_basis_closed():
    with pytest.raises(ValidationError, match="measurement_basis known value must be one of"):
        _obs(measurement_basis=known_fact("headcount-ish"))


def test_measurement_basis_unspecified_is_allowed():
    obs = _obs(measurement_basis=known_fact("unspecified"))
    assert obs.measurement_basis.value == "unspecified"


# ---- durable key guards ----

def test_key_rejects_blank_fields():
    with pytest.raises(ValidationError):
        _key(cik="   ")
    with pytest.raises(ValidationError):
        _key(accession_number="")
    with pytest.raises(ValidationError):
        _key(period_of_report=" ")


def test_source_must_be_edgar():
    with pytest.raises(ValidationError, match="source must be 'sec_edgar'"):
        _key(source="companies_house")


# ---- schema version is pinned ----

def test_schema_version_is_pinned():
    with pytest.raises(ValidationError, match="schema_version must be"):
        _obs(schema_version="edgar_headcount_observation_v999")


# ---- extraction span ----

def test_span_end_before_start_rejected():
    with pytest.raises(ValidationError, match="must be >= char_start"):
        _span(char_start=2000, char_end=1000)


def test_span_locator_kind_closed():
    with pytest.raises(ValidationError, match="locator_kind must be one of"):
        _span(locator_kind="xbrl_fact_pointer")


# ---- supersession vocabulary ----

def test_supersession_relationship_closed():
    prior = ObservationRef(key=_key(), parser_version="v0", run_id="01HOLDRUN0000000000000000")
    with pytest.raises(ValidationError, match="reused Ob.15 vocabulary"):
        HeadcountSupersession(relationship="replaces", prior=prior, reason="x")


# ---- the architecture invariant, enforced in code (AR-01/02/06) ----

def test_immutable_observation_carries_no_entity_identity():
    # The durable observation must NEVER carry canonical/provisional entity identity --
    # that lives only in the derived Layer-2b projection. This guards the identity split.
    fields = set(EdgarHeadcountObservation.model_fields)
    assert not any(
        token in name
        for name in fields
        for token in ("entity_key", "entity_id", "provisional_filer", "resolution")
    ), f"immutable observation leaked an entity-identity field: {sorted(fields)}"


# ---- round-trip ----

def test_round_trip():
    obs = _obs()
    assert EdgarHeadcountObservation.model_validate(obs.model_dump()) == obs
