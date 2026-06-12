from __future__ import annotations

import json

import pytest

from source_capture.adapters.direct_http import (
    DirectHttpCaptureFailure,
    DirectHttpCaptureFailureKind,
    DirectHttpCaptureSuccess,
)
from source_capture.adapters.edgar_discovery import (
    EdgarDiscoveryFailure,
    EdgarDiscoveryFailureKind,
    EdgarDiscoverySuccess,
    discover_filing,
    select_latest_filing,
)

UA = "Orca research probe (research@orca.local)"


def _recent(forms, accessions, primaries, reports, filings) -> dict:
    return {
        "filings": {
            "recent": {
                "form": forms,
                "accessionNumber": accessions,
                "primaryDocument": primaries,
                "reportDate": reports,
                "filingDate": filings,
            },
            "files": [],
        }
    }


# ---- the pure selection core (offline) ----

def test_select_picks_latest_10k_by_filing_date():
    subs = _recent(
        ["10-K", "10-K", "10-Q"],
        ["a-2021", "a-2023", "q"],
        ["2021.htm", "2023.htm", "q.htm"],
        ["2021-09-25", "2023-09-30", "2023-06-30"],
        ["2021-10-29", "2023-11-03", "2023-07-15"],
    )
    row = select_latest_filing(subs)
    assert row["accession_number"] == "a-2023"
    assert row["period_of_report"] == "2023-09-30"
    assert row["filing_date"] == "2023-11-03"


def test_select_ignores_amendments_when_form_is_10k():
    subs = _recent(
        ["10-K/A", "10-K"],
        ["amd", "orig"],
        ["amd.htm", "orig.htm"],
        ["2023-09-30", "2023-09-30"],
        ["2023-12-01", "2023-11-03"],
    )
    assert select_latest_filing(subs, form_type="10-K")["accession_number"] == "orig"


def test_select_returns_none_when_no_matching_form():
    subs = _recent(["10-Q", "8-K"], ["q", "k"], ["q.htm", "k.htm"], ["2023-06-30", "2023-10-01"], ["2023-07-15", "2023-10-20"])
    assert select_latest_filing(subs) is None


def test_select_skips_row_missing_primary_document():
    # the later (2024) 10-K has no primary document -> not fetchable -> skipped; falls back to 2023
    subs = _recent(
        ["10-K", "10-K"],
        ["no-doc", "good"],
        ["", "good.htm"],
        ["2024-09-30", "2023-09-30"],
        ["2024-11-01", "2023-11-03"],
    )
    assert select_latest_filing(subs)["accession_number"] == "good"


def test_select_tolerates_empty_submissions():
    assert select_latest_filing({}) is None


# ---- F-04: malformed durable filing facts are skipped, never stringified into "None" ----

def test_select_skips_row_with_missing_report_date():
    subs = _recent(["10-K"], ["acc"], ["doc.htm"], [None], ["2023-11-03"])
    assert select_latest_filing(subs) is None


def test_select_skips_row_with_non_iso_date():
    subs = _recent(["10-K"], ["acc"], ["doc.htm"], ["2023/09/30"], ["2023-11-03"])
    assert select_latest_filing(subs) is None


def test_select_skips_malformed_row_but_keeps_a_valid_one():
    # the later (2024) row has a malformed reportDate -> skipped; the valid 2023 row is selected
    subs = _recent(
        ["10-K", "10-K"],
        ["bad", "good"],
        ["bad.htm", "good.htm"],
        [None, "2023-09-30"],
        ["2024-11-01", "2023-11-03"],
    )
    assert select_latest_filing(subs)["accession_number"] == "good"


# ---- discover_filing with a stubbed transport (offline) ----

class _StubFetch:
    def __init__(self, result) -> None:
        self.result = result
        self.url = None

    def __call__(self, *, url, timeout_seconds, max_bytes, user_agent):
        self.url = url
        return self.result


def _ok(url: str, body: bytes) -> DirectHttpCaptureSuccess:
    return DirectHttpCaptureSuccess(
        requested_url=url, final_url=url, status=200, reason="OK",
        metadata={"status": 200, "byte_count": len(body)}, body=body, warning_notes=[], limitation_notes=[],
    )


def test_discover_filing_success_pads_cik_and_builds_url():
    subs = _recent(["10-K"], ["0000320193-23-000106"], ["aapl-20230930.htm"], ["2023-09-30"], ["2023-11-03"])
    stub = _StubFetch(_ok("u", json.dumps(subs).encode("utf-8")))
    out = discover_filing(cik="320193", user_agent=UA, fetch=stub)

    assert isinstance(out, EdgarDiscoverySuccess)
    assert out.cik == "0000320193"  # zero-padded to 10 digits
    assert out.accession_number == "0000320193-23-000106"
    assert out.primary_document == "aapl-20230930.htm"
    assert out.period_of_report == "2023-09-30"
    assert out.filing_date == "2023-11-03"
    assert "CIK0000320193.json" in stub.url
    assert out.limitation_notes  # the recent-only limitation is recorded


def test_discover_filing_no_10k_is_typed_failure():
    subs = _recent(["10-Q"], ["q"], ["q.htm"], ["2023-06-30"], ["2023-07-15"])
    out = discover_filing(cik="320193", user_agent=UA, fetch=_StubFetch(_ok("u", json.dumps(subs).encode("utf-8"))))
    assert isinstance(out, EdgarDiscoveryFailure)
    assert out.failure_kind is EdgarDiscoveryFailureKind.NO_MATCHING_FILING


def test_discover_filing_network_failure_is_typed():
    failure = DirectHttpCaptureFailure(
        requested_url="u", failure_kind=DirectHttpCaptureFailureKind.NETWORK_ERROR, message="boom"
    )
    out = discover_filing(cik="320193", user_agent=UA, fetch=_StubFetch(failure))
    assert isinstance(out, EdgarDiscoveryFailure)
    assert out.failure_kind is EdgarDiscoveryFailureKind.SUBMISSIONS_FETCH_FAILED


def test_discover_filing_malformed_json_is_typed():
    out = discover_filing(cik="320193", user_agent=UA, fetch=_StubFetch(_ok("u", b"not json{")))
    assert isinstance(out, EdgarDiscoveryFailure)
    assert out.failure_kind is EdgarDiscoveryFailureKind.MALFORMED_SUBMISSIONS


def test_discover_filing_non_2xx_is_typed():
    resp = DirectHttpCaptureSuccess(
        requested_url="u", final_url="u", status=404, reason="Not Found",
        metadata={"status": 404}, body=b"", warning_notes=[], limitation_notes=[],
    )
    out = discover_filing(cik="320193", user_agent=UA, fetch=_StubFetch(resp))
    assert isinstance(out, EdgarDiscoveryFailure)
    assert out.failure_kind is EdgarDiscoveryFailureKind.NON_2XX_STATUS


def test_discover_filing_bad_cik_raises():
    with pytest.raises(ValueError, match="cik"):
        discover_filing(cik="not-a-cik", user_agent=UA, fetch=_StubFetch(None))
