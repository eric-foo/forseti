"""EDGAR discovery adapter -- which filing to fetch, via the SEC submissions API.

The companion to ``edgar_filings`` (which fetches a *known* filing): given a CIK, this finds
the latest filing of a form (default ``10-K``) by reading the SEC submissions JSON
(``https://data.sec.gov/submissions/CIK##########.json``) and returns the structured target
(accession, primary document, period-of-report, **filing date**) the fetch adapter needs.

It conforms to the same adapter contract: a free ``discover_filing`` function returning frozen
``EdgarDiscoverySuccess`` / ``EdgarDiscoveryFailure`` dataclasses; transport behind an injected
``EdgarHttpFetch`` seam (default ``fetch_direct_http_capture``); SEC fair-access requires a
declared User-Agent, so it is REQUIRED. Bad input (blank / non-numeric CIK) raises ``ValueError``;
an operational failure (network, non-2xx, malformed body, no matching filing) returns a typed
``EdgarDiscoveryFailure``.

``select_latest_filing`` is the PURE, offline-testable core (a parsed submissions dict in -> the
chosen row out). v0 reads ``filings.recent`` only; older filings live in ``filings.files[]``
shards which v0 does not consult (recorded as a limitation -- the latest 10-K is always in
``recent``). It supplies ``filing_date``, closing the gap the capture adapter slice left open.
"""
from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum

from source_capture.adapters.direct_http import (
    DEFAULT_TIMEOUT_SECONDS,
    DirectHttpCaptureFailure,
    fetch_direct_http_capture,
)
from source_capture.adapters.edgar_filings import EdgarHttpFetch

EDGAR_SUBMISSIONS_BASE = "https://data.sec.gov/submissions"
# Submissions JSON for a prolific filer can exceed the 5 MB direct_http default; raise the cap so
# a large-but-valid submissions document is not silently truncated.
EDGAR_SUBMISSIONS_MAX_BYTES = 15_000_000
DEFAULT_DISCOVERY_FORM = "10-K"

_RECENT_LIMITATION = (
    "v0 discovery reads filings.recent only; older filings in filings.files[] shards are not "
    "consulted (the latest 10-K is always in recent)"
)
_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _is_nonblank_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_iso_date(value: object) -> bool:
    return isinstance(value, str) and bool(_ISO_DATE.match(value.strip()))


class EdgarDiscoveryFailureKind(StrEnum):
    SUBMISSIONS_FETCH_FAILED = "submissions_fetch_failed"  # transport-level failure
    NON_2XX_STATUS = "non_2xx_status"                      # fetched, but a non-2xx status
    MALFORMED_SUBMISSIONS = "malformed_submissions"        # body was not a JSON object
    NO_MATCHING_FILING = "no_matching_filing"              # no row of the requested form


@dataclass(frozen=True)
class EdgarDiscoverySuccess:
    """The discovered filing target -- everything the fetch adapter + deriver need."""

    cik: str  # zero-padded 10-digit
    accession_number: str
    primary_document: str
    period_of_report: str
    form_type: str
    filing_date: str
    submissions_url: str
    warning_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class EdgarDiscoveryFailure:
    cik: str
    submissions_url: str
    failure_kind: EdgarDiscoveryFailureKind
    message: str
    status: int | None = None
    warning_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)


EdgarDiscoveryResult = EdgarDiscoverySuccess | EdgarDiscoveryFailure


def select_latest_filing(submissions: Mapping, *, form_type: str = DEFAULT_DISCOVERY_FORM) -> dict | None:
    """Pure: pick the latest ``form_type`` row from a parsed submissions dict (or None).

    'Latest' = max ``filingDate`` (ISO dates sort lexically), tie-broken by accession. Rows
    missing a primary document are skipped (not fetchable)."""
    recent = (((submissions or {}).get("filings") or {}).get("recent")) or {}
    forms = recent.get("form") or []
    accessions = recent.get("accessionNumber") or []
    primaries = recent.get("primaryDocument") or []
    report_dates = recent.get("reportDate") or []
    filing_dates = recent.get("filingDate") or []

    rows: list[dict] = []
    for index, form in enumerate(forms):
        if form != form_type:
            continue
        if index >= len(accessions) or index >= len(primaries) or index >= len(report_dates) or index >= len(filing_dates):
            continue  # malformed / unaligned arrays -> skip this row
        primary = primaries[index]
        accession = accessions[index]
        report_date = report_dates[index]
        filing_date = filing_dates[index]
        # Durable filing facts must be well-formed (F-04): a blank / None / non-date value must NOT
        # be coerced into a stringified "None" that would pass the observation key's non-blank
        # check downstream. A malformed row is skipped, not silently stringified.
        if not _is_nonblank_str(primary) or not _is_nonblank_str(accession):
            continue
        if not _is_iso_date(report_date) or not _is_iso_date(filing_date):
            continue
        rows.append(
            {
                "accession_number": accession,
                "primary_document": primary,
                "period_of_report": report_date,
                "filing_date": filing_date,
                "form_type": form,
            }
        )

    if not rows:
        return None
    return sorted(rows, key=lambda row: (str(row["filing_date"]), str(row["accession_number"])))[-1]


def discover_filing(
    *,
    cik: str,
    user_agent: str,
    form_type: str = DEFAULT_DISCOVERY_FORM,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = EDGAR_SUBMISSIONS_MAX_BYTES,
    fetch: EdgarHttpFetch = fetch_direct_http_capture,
) -> EdgarDiscoveryResult:
    """Find the latest ``form_type`` filing for ``cik`` via the SEC submissions API."""
    cik_padded = _normalize_cik(cik)
    agent = _require_nonblank("user_agent", user_agent)
    form = _require_nonblank("form_type", form_type)
    url = f"{EDGAR_SUBMISSIONS_BASE}/CIK{cik_padded}.json"

    result = fetch(url=url, timeout_seconds=timeout_seconds, max_bytes=max_bytes, user_agent=agent)

    if isinstance(result, DirectHttpCaptureFailure):
        return EdgarDiscoveryFailure(
            cik=cik_padded,
            submissions_url=url,
            failure_kind=EdgarDiscoveryFailureKind.SUBMISSIONS_FETCH_FAILED,
            message=f"submissions fetch failed ({result.failure_kind}): {result.message}",
            status=result.status,
            limitation_notes=[f"access_failed: direct_http {result.failure_kind}"],
        )

    if not 200 <= result.status < 300:
        return EdgarDiscoveryFailure(
            cik=cik_padded,
            submissions_url=url,
            failure_kind=EdgarDiscoveryFailureKind.NON_2XX_STATUS,
            message=f"submissions fetch returned HTTP {result.status} {result.reason or ''}".strip(),
            status=result.status,
            warning_notes=list(result.warning_notes),
            limitation_notes=list(result.limitation_notes),
        )

    try:
        submissions = json.loads(result.body)
    except ValueError as exc:
        return EdgarDiscoveryFailure(
            cik=cik_padded,
            submissions_url=url,
            failure_kind=EdgarDiscoveryFailureKind.MALFORMED_SUBMISSIONS,
            message=f"submissions body is not valid JSON: {exc}",
        )
    if not isinstance(submissions, dict):
        return EdgarDiscoveryFailure(
            cik=cik_padded,
            submissions_url=url,
            failure_kind=EdgarDiscoveryFailureKind.MALFORMED_SUBMISSIONS,
            message="submissions body did not decode to a JSON object",
        )

    row = select_latest_filing(submissions, form_type=form)
    if row is None:
        return EdgarDiscoveryFailure(
            cik=cik_padded,
            submissions_url=url,
            failure_kind=EdgarDiscoveryFailureKind.NO_MATCHING_FILING,
            message=f"no {form!r} filing found in filings.recent for CIK {cik_padded}",
            limitation_notes=[_RECENT_LIMITATION],
        )

    return EdgarDiscoverySuccess(
        cik=cik_padded,
        accession_number=str(row["accession_number"]),
        primary_document=str(row["primary_document"]),
        period_of_report=str(row["period_of_report"]),
        form_type=str(row["form_type"]),
        filing_date=str(row["filing_date"]),
        submissions_url=url,
        limitation_notes=[_RECENT_LIMITATION],
    )


def _normalize_cik(cik: str) -> str:
    if not isinstance(cik, str) or not cik.strip():
        raise ValueError("cik must be a non-empty string")
    digits = "".join(ch for ch in cik if ch.isdigit())
    if not digits:
        raise ValueError(f"cik must contain digits; got {cik!r}")
    if len(digits) > 10:
        raise ValueError(f"cik has more than 10 digits; got {cik!r}")
    return digits.zfill(10)


def _require_nonblank(field_name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()
