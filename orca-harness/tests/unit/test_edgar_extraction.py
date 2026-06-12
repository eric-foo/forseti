from __future__ import annotations

import re

from source_capture.company_aggregate.edgar_extraction import (
    EXTRACTOR_BASIS_VALUES,
    EXTRACTOR_QUALITY_VALUES,
    PARSER_METHOD,
    PARSER_VERSION,
    RULESET_SHA256,
    extract_employee_count,
    extraction_to_measure_facts,
)
from source_capture.company_aggregate.observation import (
    MEASUREMENT_BASIS_VALUES,
    VALUE_QUALITY_VALUES,
    EdgarHeadcountObservation,
    EdgarObservationKey,
    ExtractionProvenance,
    ExtractionSpan,
)


# ---- extraction of the dominant form ----

def test_approximate_full_time_equivalent():
    out = extract_employee_count(
        "As of September 30, 2023, we had approximately 161,000 full-time equivalent employees."
    )
    assert out.found is True
    assert out.count_int == 161000
    assert out.quality == "approximate"
    assert out.basis == "full_time_equivalent"
    # the span points back into the text
    assert out.char_start is not None and out.char_end > out.char_start


def test_plain_count_unspecified_basis():
    out = extract_employee_count("We employed 12,500 people worldwide.")
    assert out.found is True
    assert out.count_int == 12500
    assert out.quality == "exact"
    assert out.basis == "unspecified"


def test_total_basis():
    out = extract_employee_count("At fiscal year-end we had 164,000 total employees.")
    assert out.found is True
    assert out.count_int == 164000
    assert out.basis == "total"
    assert out.quality == "exact"


def test_full_time_basis():
    out = extract_employee_count("The Company had 5,200 full-time employees.")
    assert out.found and out.count_int == 5200 and out.basis == "full_time"


# ---- AR-03: multiple bases -> primary headcount + flagged alternates (NOT ambiguous) ----

def test_multi_basis_picks_total_primary_and_flags_alternate():
    out = extract_employee_count(
        "We had approximately 161,000 full-time employees and 200,000 total employees."
    )
    assert out.found is True
    assert out.count_int == 200000  # total is the canonical primary
    assert out.basis == "total"
    assert "161,000" in out.alternates


# ---- genuine ambiguity: tied at the top basis, conflicting values ----

def test_conflicting_unspecified_counts_are_ambiguous():
    out = extract_employee_count(
        "We had 161,000 employees. The filing elsewhere reports we had 200,000 employees."
    )
    assert out.found is False
    assert out.quality == "ambiguous"
    assert out.count_int is None
    assert set(out.alternates) == {"161,000", "200,000"}


# ---- F-01: conservative acceptance -- non-headcount counts are honest misses, never KNOWN ----

def test_event_count_is_an_honest_miss():
    # a hiring-EVENT count is not a workforce total
    out = extract_employee_count("During 2023, we hired 5,000 employees.")
    assert out.found is False
    assert out.count_int != 5000


def test_possession_plus_event_is_still_a_miss():
    # even with a possession verb present, an event verb on the count excludes it
    assert extract_employee_count("As of year-end we had added 5,000 employees.").found is False


def test_regional_segment_count_is_an_honest_miss():
    assert extract_employee_count("We had 12,000 employees in our retail segment.").found is False


def test_bare_uncued_people_count_is_an_honest_miss():
    # no workforce qualifier and no possession/as-of cue -> not a headcount total
    assert extract_employee_count("Roughly 5,000 people visited our stores.").found is False


def test_possession_cue_admits_a_plain_count():
    out = extract_employee_count("As of December 31, 2023, the Company employed 5,200 people.")
    assert out.found is True
    assert out.count_int == 5200


# ---- F-02: basis comes from the matched qualifier, not a pre-count "a total of" ----

def test_grammatical_total_of_is_full_time_not_total_basis():
    out = extract_employee_count("We had a total of 5,200 full-time employees.")
    assert out.found is True
    assert out.count_int == 5200
    assert out.basis == "full_time"  # the qualifier on the noun, NOT the grammatical "a total of"


# ---- honest not-found ----

def test_no_match_is_not_found():
    out = extract_employee_count("This section discusses our business strategy and risk factors.")
    assert out.found is False
    assert out.quality is None
    assert out.count_int is None
    assert out.reason


def test_empty_text_is_not_found():
    assert extract_employee_count("   ").found is False


def test_average_number_form_is_an_honest_miss_not_a_wrong_value():
    # v0 does not handle "average number of employees was N" (number after the noun).
    # It must MISS honestly, never emit a wrong value.
    out = extract_employee_count("The average number of employees during 2023 was 5,200.")
    assert out.count_int != 5200  # not silently captured
    assert out.found is False


# ---- determinism + provenance binding ----

def test_extraction_is_deterministic():
    text = "We had approximately 161,000 full-time equivalent employees."
    assert extract_employee_count(text) == extract_employee_count(text)


def test_ruleset_hash_is_stable_hex():
    assert re.fullmatch(r"[0-9a-f]{64}", RULESET_SHA256)
    assert PARSER_METHOD and PARSER_VERSION


# ---- the extractor's vocabularies are subsets of the observation closed sets ----

def test_extractor_vocabularies_are_subsets():
    assert EXTRACTOR_BASIS_VALUES <= MEASUREMENT_BASIS_VALUES
    assert EXTRACTOR_QUALITY_VALUES <= VALUE_QUALITY_VALUES


# ---- the bridge: mapped measure-facts build a VALID observation (honesty end-to-end) ----

def _observation_from_measure(measure) -> EdgarHeadcountObservation:
    employee_count, count_int, value_quality, measurement_basis = measure
    return EdgarHeadcountObservation(
        key=EdgarObservationKey(
            source="sec_edgar",
            cik="0000320193",
            accession_number="0000320193-23-000106",
            period_of_report="2023-09-30",
        ),
        form_type="10-K",
        filing_date="2023-11-03",
        employee_count=employee_count,
        employee_count_int=count_int,
        value_quality=value_quality,
        measurement_basis=measurement_basis,
        extraction_span=ExtractionSpan(
            preserved_file_id="file_01",
            relative_packet_path="raw/01_10k.htm",
            source_sha256="a" * 64,
            locator_kind="char_offset_range",
            char_start=0,
            char_end=48,
            excerpt_sha256="b" * 64,
            matched_text="approximately 161,000 full-time equivalent",
        ),
        extraction=ExtractionProvenance(
            parser_method=PARSER_METHOD,
            parser_version=PARSER_VERSION,
            ruleset_sha256=RULESET_SHA256,
            run_id="01HRUN0000000000000000000",
            derived_at="2026-06-12T00:00:00Z",
        ),
        packet_id="pkt-1",
        evidence_slice_id="s_filing",
        manifest_sha256="c" * 64,
    )


def test_found_extraction_builds_valid_observation():
    measure = extraction_to_measure_facts(
        extract_employee_count("approximately 161,000 full-time equivalent employees")
    )
    obs = _observation_from_measure(measure)
    assert obs.employee_count_int == 161000
    assert obs.value_quality.value == "approximate"
    assert obs.measurement_basis.value == "full_time_equivalent"


def test_ambiguous_extraction_builds_valid_observation():
    measure = extraction_to_measure_facts(
        extract_employee_count("We had 161,000 employees. The filing elsewhere reports we had 200,000 employees.")
    )
    obs = _observation_from_measure(measure)
    assert obs.employee_count_int is None
    assert obs.value_quality.value == "ambiguous"


def test_not_found_extraction_builds_valid_observation():
    measure = extraction_to_measure_facts(extract_employee_count("no count here"))
    obs = _observation_from_measure(measure)
    assert obs.employee_count_int is None
    assert obs.employee_count.status.value == "unknown_with_reason"
