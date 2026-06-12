from __future__ import annotations

from source_capture.company_aggregate.observation import (
    EdgarHeadcountObservation,
    EdgarObservationKey,
    ExtractionProvenance,
    ExtractionSpan,
)
from source_capture.company_aggregate.observation_log import append_observation, read_observation_log
from source_capture.models import known_fact


def _obs(*, accession: str, period: str = "2023-09-30", count_int: int = 161000) -> EdgarHeadcountObservation:
    return EdgarHeadcountObservation(
        key=EdgarObservationKey(source="sec_edgar", cik="0000320193", accession_number=accession, period_of_report=period),
        form_type="10-K",
        filing_date="2023-11-03",
        employee_count=known_fact(f"{count_int:,}"),
        employee_count_int=count_int,
        value_quality=known_fact("approximate"),
        measurement_basis=known_fact("full_time"),
        extraction_span=ExtractionSpan(
            preserved_file_id="file_01", relative_packet_path="raw/10k.htm", source_sha256="a" * 64,
            locator_kind="char_offset_range", char_start=0, char_end=10, excerpt_sha256="b" * 64, matched_text="m",
        ),
        extraction=ExtractionProvenance(
            parser_method="edgar_item1_employee_regex", parser_version="v0", ruleset_sha256="c" * 64,
            run_id="01HRUN0000000000000000000", derived_at="2026-06-12T00:00:00Z",
        ),
        packet_id=f"pkt-{accession}",
        evidence_slice_id="edgar_primary_filing",
        manifest_sha256="d" * 64,
    )


def test_read_missing_log_is_empty(tmp_path):
    assert read_observation_log(tmp_path / "absent.yaml") == []


def test_append_then_read_round_trips(tmp_path):
    log = tmp_path / "obs_log.yaml"
    first = _obs(accession="acc-2022", period="2022-09-24", count_int=164000)
    second = _obs(accession="acc-2023", period="2023-09-30", count_int=161000)
    append_observation(first, log_path=log)
    append_observation(second, log_path=log)

    back = read_observation_log(log)
    assert len(back) == 2
    assert back[0] == first  # full model equality survives the YAML round-trip
    assert back[1] == second


def test_append_is_additive_never_overwrites(tmp_path):
    log = tmp_path / "obs_log.yaml"
    for accession in ("a1", "a2", "a3"):
        append_observation(_obs(accession=accession), log_path=log)
    assert [o.key.accession_number for o in read_observation_log(log)] == ["a1", "a2", "a3"]
