from __future__ import annotations

from dataclasses import fields

import pytest

from source_capture.adapters.direct_http import (
    DEFAULT_MAX_BYTES,
    DirectHttpCaptureFailure,
    DirectHttpCaptureFailureKind,
    DirectHttpCaptureSuccess,
)
from source_capture.adapters.edgar_filings import (
    EDGAR_DEFAULT_MAX_BYTES,
    EdgarFilingFailure,
    EdgarFilingFailureKind,
    EdgarFilingSuccess,
    fetch_edgar_filing,
)

UA = "Orca research probe (research@orca.local)"
EXPECTED_URL = "https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm"


def _http_success(*, status: int = 200, body: bytes = b"<html>... approximately 161,000 ...</html>") -> DirectHttpCaptureSuccess:
    return DirectHttpCaptureSuccess(
        requested_url=EXPECTED_URL,
        final_url=EXPECTED_URL,
        status=status,
        reason="OK" if status == 200 else "Not Found",
        metadata={"status": status, "byte_count": len(body), "content_type": "text/html"},
        body=body,
        warning_notes=[],
        limitation_notes=[],
    )


def _http_failure(kind: DirectHttpCaptureFailureKind = DirectHttpCaptureFailureKind.NETWORK_ERROR) -> DirectHttpCaptureFailure:
    return DirectHttpCaptureFailure(requested_url=EXPECTED_URL, failure_kind=kind, message="boom")


class _StubFetch:
    def __init__(self, result) -> None:
        self.result = result
        self.calls: list[dict] = []

    def __call__(self, *, url, timeout_seconds, max_bytes, user_agent):
        self.calls.append(
            {"url": url, "timeout_seconds": timeout_seconds, "max_bytes": max_bytes, "user_agent": user_agent}
        )
        return self.result


def _args(**overrides) -> dict:
    base = dict(
        cik="0000320193",
        accession_number="0000320193-23-000106",
        primary_document="aapl-20230930.htm",
        period_of_report="2023-09-30",
        form_type="10-K",
        user_agent=UA,
    )
    base.update(overrides)
    return base


# ---- happy path ----

def test_successful_fetch_returns_full_bytes_and_metadata():
    body = b"<html>... approximately 161,000 full-time employees ...</html>"
    stub = _StubFetch(_http_success(body=body))
    result = fetch_edgar_filing(**_args(), fetch=stub)

    assert isinstance(result, EdgarFilingSuccess)
    assert result.filing_bytes == body  # FULL bytes, not an excerpt
    assert result.document_url == EXPECTED_URL  # leading zeros stripped, dashes removed
    assert result.period_of_report == "2023-09-30"
    assert result.form_type == "10-K"
    # the SEC-compliant UA and the raised cap are passed through to the transport
    assert stub.calls[0]["user_agent"] == UA
    assert stub.calls[0]["max_bytes"] == EDGAR_DEFAULT_MAX_BYTES


def test_document_url_strips_leading_zeros_and_dashes():
    stub = _StubFetch(_http_success())
    result = fetch_edgar_filing(**_args(), fetch=stub)
    assert stub.calls[0]["url"] == EXPECTED_URL
    assert isinstance(result, EdgarFilingSuccess)


def test_max_bytes_override_passed_to_transport():
    stub = _StubFetch(_http_success())
    fetch_edgar_filing(**_args(), max_bytes=9_000_000, fetch=stub)
    assert stub.calls[0]["max_bytes"] == 9_000_000


# ---- operational failures (typed, not exceptions) ----

def test_transport_failure_returns_typed_failure():
    stub = _StubFetch(_http_failure(DirectHttpCaptureFailureKind.TIMEOUT))
    result = fetch_edgar_filing(**_args(), fetch=stub)
    assert isinstance(result, EdgarFilingFailure)
    assert result.failure_kind is EdgarFilingFailureKind.HTTP_FETCH_FAILED
    assert result.limitation_notes  # honest visible limitation


def test_non_2xx_returns_typed_failure():
    stub = _StubFetch(_http_success(status=404))
    result = fetch_edgar_filing(**_args(), fetch=stub)
    assert isinstance(result, EdgarFilingFailure)
    assert result.failure_kind is EdgarFilingFailureKind.NON_2XX_STATUS
    assert result.status == 404


# ---- bad input -> ValueError (the bad-input convention) ----

@pytest.mark.parametrize(
    "field_name",
    ["cik", "accession_number", "primary_document", "period_of_report", "form_type", "user_agent"],
)
def test_blank_inputs_raise(field_name):
    stub = _StubFetch(_http_success())
    with pytest.raises(ValueError, match=field_name):
        fetch_edgar_filing(**_args(**{field_name: "   "}), fetch=stub)


def test_non_numeric_cik_raises():
    stub = _StubFetch(_http_success())
    with pytest.raises(ValueError, match="cik must be numeric"):
        fetch_edgar_filing(**_args(cik="apple"), fetch=stub)


def test_primary_document_rejects_path_or_url():
    stub = _StubFetch(_http_success())
    with pytest.raises(ValueError, match="plain filename"):
        fetch_edgar_filing(**_args(primary_document="../secrets.txt"), fetch=stub)
    with pytest.raises(ValueError, match="plain filename"):
        fetch_edgar_filing(**_args(primary_document="https://evil.example/x.htm"), fetch=stub)


# ---- capture-only invariant: the adapter never carries an extracted count ----

def test_adapter_success_carries_no_employee_count():
    names = {f.name for f in fields(EdgarFilingSuccess)}
    assert not any("employee" in name or "count" in name for name in names), sorted(names)


def test_default_cap_exceeds_direct_http_default():
    # OQ-3: full-filing capture needs headroom over the 5 MB direct_http default.
    assert EDGAR_DEFAULT_MAX_BYTES > DEFAULT_MAX_BYTES
