from __future__ import annotations

import json
from pathlib import Path

import pytest

from harness_utils import hash_file
from runners.run_source_capture_edgar_packet import build_edgar_packet, main
from source_capture.adapters.direct_http import (
    DirectHttpCaptureFailure,
    DirectHttpCaptureFailureKind,
    DirectHttpCaptureSuccess,
)
from source_capture.adapters.edgar_filings import EdgarFilingSuccess
from source_capture.models import CaptureModeCategory, SourceCapturePacket

UA = "Orca research probe (research@orca.local)"
DOC_URL = "https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm"


def _success(*, body: bytes = b"<html>... approximately 161,000 full-time employees ...</html>") -> EdgarFilingSuccess:
    return EdgarFilingSuccess(
        cik="0000320193",
        accession_number="0000320193-23-000106",
        period_of_report="2023-09-30",
        form_type="10-K",
        primary_document="aapl-20230930.htm",
        document_url=DOC_URL,
        final_url=DOC_URL,
        filing_bytes=body,
        http_metadata={"status": 200, "content_type": "text/html", "byte_count": len(body)},
        warning_notes=[],
        limitation_notes=[],
    )


class _StubFetch:
    def __init__(self, result) -> None:
        self.result = result

    def __call__(self, *, url, timeout_seconds, max_bytes, user_agent):
        return self.result


def _http_success(body: bytes) -> DirectHttpCaptureSuccess:
    return DirectHttpCaptureSuccess(
        requested_url=DOC_URL,
        final_url=DOC_URL,
        status=200,
        reason="OK",
        metadata={"status": 200, "byte_count": len(body), "content_type": "text/html"},
        body=body,
        warning_notes=[],
        limitation_notes=[],
    )


# ---- the translate core ----

def test_build_edgar_packet_preserves_full_filing(tmp_path):
    body = b"<html>... approximately 161,000 full-time employees ...</html>"
    result = build_edgar_packet(
        success=_success(body=body),
        output_directory=tmp_path / "packet",
        decision_question="beauty net-adds backtest",
    )
    packet = result.packet

    assert packet.source_family == "sec_edgar"
    assert packet.capture_mode is CaptureModeCategory.STRUCTURED_ACCESS
    assert packet.source_locator.value == DOC_URL

    # FULL filing preserved and re-verifiable on disk
    assert len(packet.preserved_files) == 1
    preserved = packet.preserved_files[0]
    raw_path = Path(result.output_directory) / preserved.relative_packet_path
    assert raw_path.read_bytes() == body
    assert hash_file(raw_path) == preserved.sha256
    assert preserved.size_bytes == len(body)
    assert preserved.hash_basis == "raw_stored_bytes"

    # structured EDGAR metadata carried as capture context
    ctx = json.loads(packet.capture_context.value)
    assert ctx["cik"] == "0000320193"
    assert ctx["accession_number"] == "0000320193-23-000106"
    assert ctx["period_of_report"] == "2023-09-30"
    assert ctx["document_url"] == DOC_URL

    # period-of-report carried as the source event timing
    assert packet.timing.source_publication_or_event.value == "2023-09-30"

    # capture-only: the packet asserts no employee count was extracted
    assert any("NO employee count" in claim for claim in packet.receipt_metadata.non_claims)

    # a valid, round-trippable packet
    assert SourceCapturePacket.model_validate(packet.model_dump(mode="json")) == packet


def test_build_edgar_packet_refuses_nonempty_output(tmp_path):
    out = tmp_path / "packet"
    out.mkdir()
    (out / "stray.txt").write_text("x", encoding="utf-8")
    with pytest.raises(ValueError, match="refusing to overwrite non-empty"):
        build_edgar_packet(success=_success(), output_directory=out, decision_question="x")


# ---- the CLI exit-code convention (offline, stubbed transport) ----

def _argv(tmp_path: Path) -> list[str]:
    return [
        "--cik", "0000320193",
        "--accession-number", "0000320193-23-000106",
        "--primary-document", "aapl-20230930.htm",
        "--period-of-report", "2023-09-30",
        "--user-agent", UA,
        "--output-directory", str(tmp_path / "pkt"),
        "--decision-question", "beauty net-adds backtest",
    ]


def test_main_exit_0_on_success(tmp_path):
    stub = _StubFetch(_http_success(b"<html>... 161,000 ...</html>"))
    code = main(_argv(tmp_path), fetch=stub)
    assert code == 0
    assert (tmp_path / "pkt" / "manifest.json").exists()
    assert (tmp_path / "pkt" / "receipt.md").exists()


def test_main_exit_3_on_fetch_failure(tmp_path):
    stub = _StubFetch(
        DirectHttpCaptureFailure(requested_url=DOC_URL, failure_kind=DirectHttpCaptureFailureKind.NETWORK_ERROR, message="boom")
    )
    code = main(_argv(tmp_path), fetch=stub)
    assert code == 3
    assert not (tmp_path / "pkt").exists()


def test_main_exit_2_on_bad_input(tmp_path):
    stub = _StubFetch(_http_success(b"<html>x</html>"))
    argv = _argv(tmp_path)
    argv[argv.index("--cik") + 1] = "not-a-number"
    with pytest.raises(SystemExit) as excinfo:
        main(argv, fetch=stub)
    assert excinfo.value.code == 2
