from __future__ import annotations

import json
from pathlib import Path

import pytest

from harness_utils import sha256_text
from runners.run_source_capture_edgar_packet import build_edgar_packet
from source_capture.adapters.edgar_filings import EdgarFilingSuccess
from source_capture.company_aggregate.edgar_derivation import (
    EdgarDerivationFailure,
    derive_edgar_headcount_observation,
)
from source_capture.company_aggregate.observation import EdgarHeadcountObservation
from source_capture.models import VisibleFactStatus

CIK = "0000320193"
ACCESSION = "0000320193-23-000106"
PERIOD = "2023-09-30"
PRIMARY = "aapl-20230930.htm"
DOC_URL = f"https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/{PRIMARY}"
FOUND_BODY = b"<html>... As of fiscal year-end we had approximately 161,000 full-time employees ...</html>"

RUN_ID = "01HRUN0000000000000000000"
DERIVED_AT = "2026-06-12T00:00:00Z"
FILING_DATE = "2023-11-03"


def _success(body: bytes) -> EdgarFilingSuccess:
    return EdgarFilingSuccess(
        cik=CIK,
        accession_number=ACCESSION,
        period_of_report=PERIOD,
        form_type="10-K",
        primary_document=PRIMARY,
        document_url=DOC_URL,
        final_url=DOC_URL,
        filing_bytes=body,
        http_metadata={"status": 200, "content_type": "text/html", "byte_count": len(body)},
        warning_notes=[],
        limitation_notes=[],
    )


def _build_packet(tmp_path: Path, body: bytes):
    return build_edgar_packet(
        success=_success(body),
        output_directory=tmp_path / "packet",
        decision_question="beauty net-adds backtest",
    )


def _derive(tmp_path: Path):
    return derive_edgar_headcount_observation(
        packet_or_manifest_path=Path(tmp_path / "packet"),
        filing_date=FILING_DATE,
        run_id=RUN_ID,
        derived_at=DERIVED_AT,
    )


# ---- the happy path: a found count -> a complete, valid observation ----

def test_derive_from_found_packet_builds_observation(tmp_path):
    result = _build_packet(tmp_path, FOUND_BODY)
    obs = _derive(tmp_path)

    assert isinstance(obs, EdgarHeadcountObservation)
    # durable filing-fact key, read from the packet capture context
    assert obs.key.source == "sec_edgar"
    assert obs.key.cik == CIK
    assert obs.key.accession_number == ACCESSION
    assert obs.key.period_of_report == PERIOD
    assert obs.form_type == "10-K"
    assert obs.filing_date == FILING_DATE

    # the measure
    assert obs.employee_count_int == 161000
    assert obs.employee_count.status is VisibleFactStatus.KNOWN
    assert obs.value_quality.value == "approximate"
    assert obs.measurement_basis.value == "full_time"

    # packet provenance binds the observation back to the capture
    assert obs.packet_id == result.packet.packet_id
    assert obs.evidence_slice_id == "edgar_primary_filing"
    manifest_path = Path(result.output_directory) / "manifest.json"
    assert obs.manifest_sha256 == sha256_text(manifest_path.read_text(encoding="utf-8"))

    # a valid, round-trippable observation
    assert EdgarHeadcountObservation.model_validate(obs.model_dump(mode="json")) == obs


def test_span_binds_verified_source_and_points_into_decoded_text(tmp_path):
    result = _build_packet(tmp_path, FOUND_BODY)
    obs = _derive(tmp_path)
    span = obs.extraction_span

    preserved = result.packet.preserved_files[0]
    raw_path = Path(result.output_directory) / preserved.relative_packet_path
    # the span's source hash is the RE-VERIFIED preserved-bytes hash
    assert span.source_sha256 == preserved.sha256
    assert span.preserved_file_id == preserved.file_id

    # the char offsets actually point at the matched text inside the decoded filing
    text = raw_path.read_text(encoding="utf-8", errors="replace")
    assert text[span.char_start : span.char_end] == span.matched_text
    assert "161,000" in span.matched_text
    assert span.excerpt_sha256 == sha256_text(span.matched_text)


def test_extraction_provenance_is_pinned_and_deterministic(tmp_path):
    _build_packet(tmp_path, FOUND_BODY)
    obs = _derive(tmp_path)
    assert obs.extraction.parser_method == "edgar_item1_employee_regex"
    assert obs.extraction.parser_version == "v0"
    assert obs.extraction.run_id == RUN_ID
    assert obs.extraction.derived_at == DERIVED_AT
    assert obs.extraction.ruleset_sha256  # bound to the actual ruleset


# ---- honesty: no count, and ambiguous -> never a fabricated value ----

def test_not_found_packet_is_honest(tmp_path):
    body = b"<html>This section discusses our business strategy and risk factors.</html>"
    _build_packet(tmp_path, body)
    obs = _derive(tmp_path)

    assert obs.employee_count_int is None
    assert obs.employee_count.status is VisibleFactStatus.UNKNOWN_WITH_REASON
    assert obs.value_quality.status is not VisibleFactStatus.KNOWN
    # degenerate span still binds the source file, never a fabricated location
    assert obs.extraction_span.char_start == 0 and obs.extraction_span.char_end == 0
    assert "no single extracted span" in obs.extraction_span.matched_text
    assert any("no employee count extracted" in note for note in obs.limitations)
    assert EdgarHeadcountObservation.model_validate(obs.model_dump(mode="json")) == obs


def test_ambiguous_packet_is_honest(tmp_path):
    body = b"<html>We had 161,000 employees. The filing elsewhere reports we had 200,000 employees.</html>"
    _build_packet(tmp_path, body)
    obs = _derive(tmp_path)

    assert obs.employee_count_int is None
    assert obs.value_quality.value == "ambiguous"
    assert set(obs.alternates) == {"161,000", "200,000"}
    assert any("ambiguous extraction" in note for note in obs.limitations)
    assert EdgarHeadcountObservation.model_validate(obs.model_dump(mode="json")) == obs


# ---- the safety contract copied from the consolidator ----

def test_hash_mismatch_is_rejected(tmp_path):
    result = _build_packet(tmp_path, FOUND_BODY)
    preserved = result.packet.preserved_files[0]
    raw_path = Path(result.output_directory) / preserved.relative_packet_path
    raw_path.write_bytes(b"<html>tampered: now 999,999 full-time employees</html>")

    with pytest.raises(EdgarDerivationFailure) as excinfo:
        _derive(tmp_path)
    assert excinfo.value.code == "source_file_hash_mismatch"


def test_nonconforming_manifest_is_rejected(tmp_path):
    result = _build_packet(tmp_path, FOUND_BODY)
    manifest_path = Path(result.output_directory) / "manifest.json"
    raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    del raw["packet_id"]  # break the current schema
    manifest_path.write_text(json.dumps(raw), encoding="utf-8")

    with pytest.raises(EdgarDerivationFailure) as excinfo:
        _derive(tmp_path)
    assert excinfo.value.code == "manifest_nonconforming"


def test_ineligible_source_family_is_rejected(tmp_path):
    result = _build_packet(tmp_path, FOUND_BODY)
    manifest_path = Path(result.output_directory) / "manifest.json"
    raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    raw["source_family"] = "reddit"  # schema-valid, but not an EDGAR packet
    manifest_path.write_text(json.dumps(raw), encoding="utf-8")

    with pytest.raises(EdgarDerivationFailure) as excinfo:
        _derive(tmp_path)
    assert excinfo.value.code == "ineligible_source_surface"


def test_blank_filing_date_is_rejected(tmp_path):
    _build_packet(tmp_path, FOUND_BODY)
    with pytest.raises(EdgarDerivationFailure) as excinfo:
        derive_edgar_headcount_observation(
            packet_or_manifest_path=Path(tmp_path / "packet"),
            filing_date="   ",
            run_id=RUN_ID,
            derived_at=DERIVED_AT,
        )
    assert excinfo.value.code == "filing_date_required"
