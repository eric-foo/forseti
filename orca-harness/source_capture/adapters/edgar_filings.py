"""EDGAR filing fetch adapter -- capture only, FULL filing, no extraction.

A per-source fetch adapter for SEC EDGAR primary filing documents, conforming to the
source-capture adapter author contract: a free ``fetch_edgar_filing`` function returning
frozen ``EdgarFilingSuccess`` / ``EdgarFilingFailure`` dataclasses (each carrying
``warning_notes`` + ``limitation_notes``); transport behind an injected callable seam
(default ``fetch_direct_http_capture``); it NEVER imports the packet writer and never builds
a packet.

It captures the FULL raw primary-document bytes (AR-04 -- no hand-selected excerpt) and
carries the structured filing metadata its caller's discovery step supplies (CIK, accession,
form, period-of-report, primary document). It does NOT extract the employee count -- that
narrative extraction is the Layer-2 derivation (a later slice); ``EdgarFilingSuccess`` has no
count field.

SEC fair-access requires a declared, contactable User-Agent, so ``user_agent`` is a REQUIRED
argument (no hidden default that would hide identity and earn a 403). The byte cap defaults
above the 5 MB ``direct_http`` default because 10-K primary documents can be larger (OQ-3);
an oversized filing fails visibly as a typed failure rather than being silently truncated.
Discovery (finding which 10-K to fetch via the submissions API) is a separate concern, not
this adapter.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol, TypeAlias

from source_capture.adapters.direct_http import (
    DEFAULT_TIMEOUT_SECONDS,
    DirectHttpCaptureFailure,
    DirectHttpCaptureResult,
    DirectHttpCaptureSuccess,
    fetch_direct_http_capture,
)

EDGAR_ARCHIVES_BASE = "https://www.sec.gov/Archives/edgar/data"
# 10-K primary documents routinely exceed the 5 MB direct_http default (OQ-3); raise the cap
# for full-filing capture. Oversized filings still fail visibly (direct_http SIZE_CAP_EXCEEDED).
EDGAR_DEFAULT_MAX_BYTES = 25_000_000


class EdgarFilingFailureKind(StrEnum):
    HTTP_FETCH_FAILED = "http_fetch_failed"  # transport-level failure (network / timeout / no_body / size cap)
    NON_2XX_STATUS = "non_2xx_status"        # fetched, but the document endpoint returned a non-2xx status


class EdgarHttpFetch(Protocol):
    """The injected transport seam (default ``fetch_direct_http_capture``)."""

    def __call__(
        self, *, url: str, timeout_seconds: float, max_bytes: int, user_agent: str
    ) -> DirectHttpCaptureResult: ...


@dataclass(frozen=True)
class EdgarFilingSuccess:
    cik: str
    accession_number: str
    period_of_report: str
    form_type: str
    primary_document: str
    document_url: str
    final_url: str
    filing_bytes: bytes
    http_metadata: dict[str, object]
    warning_notes: list[str]
    limitation_notes: list[str]


@dataclass(frozen=True)
class EdgarFilingFailure:
    cik: str
    accession_number: str
    document_url: str
    failure_kind: EdgarFilingFailureKind
    message: str
    status: int | None = None
    warning_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)


EdgarFilingResult: TypeAlias = EdgarFilingSuccess | EdgarFilingFailure


def fetch_edgar_filing(
    *,
    cik: str,
    accession_number: str,
    primary_document: str,
    period_of_report: str,
    form_type: str,
    user_agent: str,
    max_bytes: int = EDGAR_DEFAULT_MAX_BYTES,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    fetch: EdgarHttpFetch = fetch_direct_http_capture,
) -> EdgarFilingResult:
    """Fetch one EDGAR primary filing document (full bytes) for a known filing.

    Bad input (blank/non-numeric identity, bad max_bytes) raises ``ValueError`` (the
    bad-input convention). An operational fetch failure (transport error or non-2xx) returns
    a typed ``EdgarFilingFailure``.
    """
    cik_clean = _require_nonblank("cik", cik)
    cik_digits = _cik_digits(cik_clean)
    accession = _require_nonblank("accession_number", accession_number)
    primary = _validate_primary_document(primary_document)
    period = _require_nonblank("period_of_report", period_of_report)
    form = _require_nonblank("form_type", form_type)
    agent = _require_nonblank("user_agent", user_agent)
    if max_bytes <= 0:
        raise ValueError("max_bytes must be greater than zero")

    document_url = f"{EDGAR_ARCHIVES_BASE}/{cik_digits}/{accession.replace('-', '')}/{primary}"

    result = fetch(
        url=document_url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
        user_agent=agent,
    )

    if isinstance(result, DirectHttpCaptureFailure):
        return EdgarFilingFailure(
            cik=cik_clean,
            accession_number=accession,
            document_url=document_url,
            failure_kind=EdgarFilingFailureKind.HTTP_FETCH_FAILED,
            message=f"EDGAR document fetch failed ({result.failure_kind}): {result.message}",
            status=result.status,
            limitation_notes=[f"access_failed: direct_http {result.failure_kind}"],
        )

    if not _is_2xx(result.status):
        return EdgarFilingFailure(
            cik=cik_clean,
            accession_number=accession,
            document_url=document_url,
            failure_kind=EdgarFilingFailureKind.NON_2XX_STATUS,
            message=f"EDGAR document fetch returned HTTP {result.status} {result.reason or ''}".strip(),
            status=result.status,
            warning_notes=list(result.warning_notes),
            limitation_notes=[
                f"access_failed: EDGAR returned HTTP {result.status}; not a clean filing fetch",
                *result.limitation_notes,
            ],
        )

    return EdgarFilingSuccess(
        cik=cik_clean,
        accession_number=accession,
        period_of_report=period,
        form_type=form,
        primary_document=primary,
        document_url=document_url,
        final_url=result.final_url,
        filing_bytes=result.body,
        http_metadata=dict(result.metadata),
        warning_notes=list(result.warning_notes),
        limitation_notes=list(result.limitation_notes),
    )


def _is_2xx(status: int) -> bool:
    return 200 <= status < 300


def _require_nonblank(field_name: str, value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _cik_digits(cik: str) -> str:
    try:
        return str(int(cik))  # strip leading zeros for the Archives path segment
    except ValueError as exc:
        raise ValueError(f"cik must be numeric; got {cik!r}") from exc


def _validate_primary_document(primary_document: str) -> str:
    text = _require_nonblank("primary_document", primary_document)
    if ".." in text or text.startswith("/") or "://" in text:
        raise ValueError(
            f"primary_document must be a plain filename, not a path or URL; got {primary_document!r}"
        )
    return text
