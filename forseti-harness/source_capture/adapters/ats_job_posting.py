"""ATS job-posting source-capture adapters (public, unauthenticated job boards).

Capture-only (Forseti Capture spine, source family ``ats_job_posting``). These
adapters FETCH verbatim public ATS board responses and normalize each posting to
a common :class:`AtsPosting` shape. They never rank, filter by relevance,
classify roles, or infer pains — a captured posting is preserved exactly as the
board returned it; the only "geography" a posting carries is the vendor's
**verbatim** location string plus, where the vendor exposes one, its **verbatim
structured** country field. No relevance/US-market classification lives here
(that stays a downstream lens).

Provenance: the endpoint shapes were ported as new Python from a read-only study
of the jb ``curated-jobs-v2`` lane (reference only, never Forseti authority) and,
for Ashby, a Phase-0 access-posture scan. See
``docs/workflows/forseti_capture_ats_job_posting_port_plan_v0.md``.

Follows ``docs/adapter_author_contract.md``: free ``fetch_*`` functions over
native (per-vendor) inputs returning frozen ``Success | Failure`` dataclasses
with honest ``warning_notes`` / ``limitation_notes``; a ``Protocol`` transport
seam so unit/contract tests inject a fake and no live network runs there; the
adapter never imports the writer and never constructs a packet. The per-vendor
``parse_*`` functions are pure and are shared with the projection so raw is
parsed by exactly one code path.

Uniformity thesis (adapter contract): uniformity lives in the OUTPUT
(:class:`AtsPosting` + the preserved verbatim raw document), not in the adapter
inputs — Greenhouse takes a board token, Workday takes tenant+site, etc.

SECURITY: no secret appears in any result field. All four endpoints are public
and unauthenticated. Workday's ``X-Calypso-Csrf-Token`` is a public per-session
token sent only as a REQUEST header; it is never a response-body value and is
never carried in an adapter result or preserved artifact.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Callable, Mapping, Protocol, Sequence, TypeAlias
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request, build_opener


DEFAULT_TIMEOUT_SECONDS = 25.0
# ATS boards can be large (a live Ashby scan returned ~2.2 MB / 126 jobs), so the
# default cap is generous vs. direct_http's 5 MB; overflow is an honest
# size_cap_exceeded failure, never a silent truncation.
DEFAULT_MAX_BYTES = 25_000_000
# Polite, sequential per-request pacing. jb only *recommended* 1.5-2s (its shipped
# code ran concurrent with no delay); Forseti implements the polite posture.
DEFAULT_DELAY_SECONDS = 1.75
DEFAULT_USER_AGENT = (
    "ForsetiSourceCaptureAtsJobPosting/0.1 "
    "(stdlib honest fetch; public unauthenticated job boards; no browser/sdk/proxy)"
)
DEFAULT_WORKDAY_PAGE_SIZE = 20
DEFAULT_WORKDAY_MAX_PAGES = 25

_NO_PROXY_OPENER = build_opener(ProxyHandler({}))


class AtsVendor(StrEnum):
    GREENHOUSE = "greenhouse"
    LEVER = "lever"
    WORKDAY = "workday"
    ASHBY = "ashby"


class AtsCaptureFailureKind(StrEnum):
    NETWORK_ERROR = "network_error"
    TIMEOUT = "timeout"
    ACCESS_FAILED = "access_failed"
    RATE_LIMITED = "rate_limited"
    MALFORMED_RESPONSE = "malformed_response"
    SIZE_CAP_EXCEEDED = "size_cap_exceeded"


@dataclass(frozen=True)
class AtsHttpResponse:
    """A completed HTTP response from the transport seam. Carries no request auth."""

    status: int
    body: bytes
    final_url: str
    headers: Mapping[str, str] = field(default_factory=dict)


class AtsTransportError(RuntimeError):
    """Raised by a transport when NO HTTP response could be obtained (network,
    timeout, size cap). A completed non-2xx response is returned, not raised."""

    def __init__(self, message: str, *, failure_kind: AtsCaptureFailureKind) -> None:
        super().__init__(message)
        self.failure_kind = failure_kind


class AtsHttpTransport(Protocol):
    """Transport seam. Real impl does stdlib HTTP; tests inject a fake."""

    def get(self, *, url: str, headers: Mapping[str, str]) -> AtsHttpResponse:
        ...

    def post(self, *, url: str, headers: Mapping[str, str], body: bytes) -> AtsHttpResponse:
        ...


@dataclass(frozen=True)
class AtsPosting:
    """One captured job posting, normalized across vendors. Every field is a
    verbatim (or verbatim-then-HTML-stripped, for ``description``) source value —
    never a ranking, score, or relevance judgment."""

    ats_job_id: str
    title: str | None
    description: str | None
    posted_date: str | None
    source_url: str | None
    location_raw: str | None
    location_country: str | None
    is_listed: bool | None = None


@dataclass(frozen=True)
class AtsBoardCaptureSuccess:
    vendor: AtsVendor
    board_locator: str
    company: str
    http_status: int
    raw_board_document: bytes
    postings: tuple[AtsPosting, ...]
    warning_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AtsBoardCaptureFailure:
    vendor: AtsVendor
    board_locator: str
    company: str
    failure_kind: AtsCaptureFailureKind
    message: str
    http_status: int | None = None


AtsBoardCaptureResult: TypeAlias = AtsBoardCaptureSuccess | AtsBoardCaptureFailure

SleepFn: TypeAlias = Callable[[float], None]


# --------------------------------------------------------------------------- #
# Stdlib transport
# --------------------------------------------------------------------------- #


class StdlibAtsHttpTransport:
    """Honest stdlib GET/POST transport with no ambient proxy (direct provenance),
    an explicit timeout, and a byte cap. Non-2xx responses are RETURNED (the body
    is preserved as evidence); only a genuine no-response condition raises
    ``AtsTransportError``."""

    def __init__(
        self,
        *,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
        max_bytes: int = DEFAULT_MAX_BYTES,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")
        if max_bytes <= 0:
            raise ValueError("max_bytes must be greater than zero")
        self._timeout_seconds = timeout_seconds
        self._max_bytes = max_bytes
        self._user_agent = user_agent

    def get(self, *, url: str, headers: Mapping[str, str]) -> AtsHttpResponse:
        return self._request(method="GET", url=url, headers=headers, body=None)

    def post(self, *, url: str, headers: Mapping[str, str], body: bytes) -> AtsHttpResponse:
        return self._request(method="POST", url=url, headers=headers, body=body)

    def _request(
        self,
        *,
        method: str,
        url: str,
        headers: Mapping[str, str],
        body: bytes | None,
    ) -> AtsHttpResponse:
        merged = {"User-Agent": self._user_agent, "Accept": "application/json", **dict(headers)}
        request = Request(url, data=body, headers=merged, method=method)
        try:
            with _NO_PROXY_OPENER.open(request, timeout=self._timeout_seconds) as response:
                return self._read(response, url)
        except HTTPError as exc:  # completed non-2xx response; preserve its body
            return self._read(exc, url)
        except URLError as exc:
            reason = str(getattr(exc, "reason", exc)).lower()
            kind = (
                AtsCaptureFailureKind.TIMEOUT
                if "timed out" in reason or "timeout" in reason
                else AtsCaptureFailureKind.NETWORK_ERROR
            )
            raise AtsTransportError(f"{method} {url} failed: {exc.reason}", failure_kind=kind) from exc
        except TimeoutError as exc:
            raise AtsTransportError(
                f"{method} {url} timed out during response read: {exc}",
                failure_kind=AtsCaptureFailureKind.TIMEOUT,
            ) from exc
        except OSError as exc:
            raise AtsTransportError(
                f"{method} {url} response read failed: {exc}",
                failure_kind=AtsCaptureFailureKind.NETWORK_ERROR,
            ) from exc

    def _read(self, response: object, requested_url: str) -> AtsHttpResponse:
        status = int(response.getcode())  # type: ignore[attr-defined]
        final_url = response.geturl()  # type: ignore[attr-defined]
        response_headers = {key: value for key, value in response.headers.items()}  # type: ignore[attr-defined]
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = response.read(min(65536, self._max_bytes - total + 1))  # type: ignore[attr-defined]
            if not chunk:
                break
            total += len(chunk)
            if total > self._max_bytes:
                raise AtsTransportError(
                    f"{requested_url} exceeded max-bytes cap during read: "
                    f"{total} > {self._max_bytes}",
                    failure_kind=AtsCaptureFailureKind.SIZE_CAP_EXCEEDED,
                )
            chunks.append(chunk)
        return AtsHttpResponse(
            status=status, body=b"".join(chunks), final_url=final_url, headers=response_headers
        )


# --------------------------------------------------------------------------- #
# Shared helpers
# --------------------------------------------------------------------------- #


def _html_to_text(value: object) -> str | None:
    """Real HTML fragment -> whitespace-normalized text ('' / non-str -> None).

    Tags are stripped BEFORE the single entity unescape, so a literal ``&lt;`` in
    the body text survives as ``<`` instead of being decoded into a fake tag and
    dropped. Used for Ashby ``descriptionHtml`` and Workday ``jobDescription``
    (real HTML). Greenhouse's entity-encoded ``content`` uses
    ``_entity_encoded_html_to_text`` instead. Locally owned (name distinct from
    projection_shared.normalized_html_text); raw preservation keeps the
    un-stripped bytes regardless."""
    if not isinstance(value, str) or not value.strip():
        return None
    import html as _html

    text = re.sub(r"<br\s*/?>", "\n", value, flags=re.IGNORECASE)
    text = re.sub(r"</p\s*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    normalized = re.sub(r"\s+", " ", _html.unescape(text)).strip()
    return normalized or None


def _entity_encoded_html_to_text(value: object) -> str | None:
    """Entity-encoded HTML (Greenhouse ``content``: ``&lt;h3&gt;...``) -> text.

    One unescape turns the entity-encoded markup back into real HTML, then
    ``_html_to_text`` strips the now-real tags and resolves the remaining
    text-level entities. Without the first unescape a naive tag-strip leaves the
    literal ``<h3>`` markup in the output (observed live on real boards)."""
    if not isinstance(value, str) or not value.strip():
        return None
    import html as _html

    return _html_to_text(_html.unescape(value))


def _plain(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    stripped = value.strip()
    return stripped or None


def _decode_json(raw: bytes, *, vendor: AtsVendor) -> object:
    try:
        return json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise _MalformedBoard(f"{vendor.value} board response was not valid JSON: {exc}") from exc


class _MalformedBoard(ValueError):
    pass


def _status_failure(
    *, vendor: AtsVendor, board_locator: str, company: str, status: int, reason: str
) -> AtsBoardCaptureFailure:
    kind = (
        AtsCaptureFailureKind.RATE_LIMITED
        if status == 429
        else AtsCaptureFailureKind.ACCESS_FAILED
    )
    return AtsBoardCaptureFailure(
        vendor=vendor,
        board_locator=board_locator,
        company=company,
        failure_kind=kind,
        message=f"{vendor.value} board {board_locator} returned HTTP {status} {reason}".strip(),
        http_status=status,
    )


def _ok(status: int) -> bool:
    return 200 <= status < 300


# --------------------------------------------------------------------------- #
# Greenhouse: GET boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true
# --------------------------------------------------------------------------- #


def greenhouse_board_url(board_token: str) -> str:
    return f"https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true"


def parse_greenhouse_postings(raw_board_document: bytes) -> list[AtsPosting]:
    payload = _decode_json(raw_board_document, vendor=AtsVendor.GREENHOUSE)
    if not isinstance(payload, dict):
        raise _MalformedBoard("greenhouse board document is not a JSON object")
    jobs = payload.get("jobs")
    if not isinstance(jobs, list):
        raise _MalformedBoard("greenhouse board document missing a 'jobs' array")
    postings: list[AtsPosting] = []
    for index, job in enumerate(jobs):
        if not isinstance(job, dict) or job.get("id") is None:
            raise _MalformedBoard(
                f"greenhouse jobs[{index}] is not an object with a non-null 'id'"
            )
        location = job.get("location")
        location_raw = location.get("name") if isinstance(location, dict) else None
        postings.append(
            AtsPosting(
                ats_job_id=str(job.get("id")),
                title=_plain(job.get("title")),
                description=_entity_encoded_html_to_text(job.get("content")),
                posted_date=_plain(job.get("first_published")) or _plain(job.get("updated_at")),
                source_url=_plain(job.get("absolute_url")),
                location_raw=_plain(location_raw),
                # Greenhouse exposes no reliable structured country on the list; None is honest.
                location_country=None,
            )
        )
    return postings


def fetch_greenhouse_board(
    *,
    company: str,
    board_token: str,
    transport: AtsHttpTransport,
) -> AtsBoardCaptureResult:
    url = greenhouse_board_url(board_token)
    try:
        response = transport.get(url=url, headers={})
    except AtsTransportError as exc:
        return AtsBoardCaptureFailure(
            vendor=AtsVendor.GREENHOUSE,
            board_locator=url,
            company=company,
            failure_kind=exc.failure_kind,
            message=str(exc),
        )
    if not _ok(response.status):
        return _status_failure(
            vendor=AtsVendor.GREENHOUSE,
            board_locator=url,
            company=company,
            status=response.status,
            reason="",
        )
    return _finish_get_board(
        vendor=AtsVendor.GREENHOUSE,
        company=company,
        board_locator=url,
        response=response,
        parser=parse_greenhouse_postings,
    )


# --------------------------------------------------------------------------- #
# Lever: GET api.lever.co/v0/postings/{company}?mode=json
# --------------------------------------------------------------------------- #


def lever_board_url(board_token: str) -> str:
    return f"https://api.lever.co/v0/postings/{board_token}?mode=json"


def _epoch_ms_to_iso(value: object) -> str | None:
    if not isinstance(value, (int, float)):
        return None
    try:
        from datetime import datetime, timezone

        return (
            datetime.fromtimestamp(value / 1000.0, tz=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        )
    except (ValueError, OverflowError, OSError):
        return None


def parse_lever_postings(raw_board_document: bytes) -> list[AtsPosting]:
    payload = _decode_json(raw_board_document, vendor=AtsVendor.LEVER)
    if not isinstance(payload, list):
        raise _MalformedBoard("lever board document is not a JSON array of postings")
    postings: list[AtsPosting] = []
    for index, job in enumerate(payload):
        if not isinstance(job, dict) or job.get("id") is None:
            raise _MalformedBoard(
                f"lever posting[{index}] is not an object with a non-null 'id'"
            )
        categories = job.get("categories")
        location_raw = categories.get("location") if isinstance(categories, dict) else None
        postings.append(
            AtsPosting(
                ats_job_id=str(job.get("id")),
                title=_plain(job.get("text")),
                description=_plain(job.get("descriptionPlain")) or _html_to_text(job.get("description")),
                posted_date=_epoch_ms_to_iso(job.get("createdAt")),
                source_url=_plain(job.get("hostedUrl")) or _plain(job.get("applyUrl")),
                location_raw=_plain(location_raw),
                # Lever's posting schema exposes this top-level structured country.
                location_country=_plain(job.get("country")),
            )
        )
    return postings


def fetch_lever_board(
    *,
    company: str,
    board_token: str,
    transport: AtsHttpTransport,
) -> AtsBoardCaptureResult:
    url = lever_board_url(board_token)
    try:
        response = transport.get(url=url, headers={})
    except AtsTransportError as exc:
        return AtsBoardCaptureFailure(
            vendor=AtsVendor.LEVER,
            board_locator=url,
            company=company,
            failure_kind=exc.failure_kind,
            message=str(exc),
        )
    if not _ok(response.status):
        return _status_failure(
            vendor=AtsVendor.LEVER, board_locator=url, company=company, status=response.status, reason=""
        )
    return _finish_get_board(
        vendor=AtsVendor.LEVER,
        company=company,
        board_locator=url,
        response=response,
        parser=parse_lever_postings,
    )


# --------------------------------------------------------------------------- #
# Ashby: GET api.ashbyhq.com/posting-api/job-board/{name}?includeCompensation=true
# --------------------------------------------------------------------------- #


def ashby_board_url(job_board_name: str) -> str:
    return (
        f"https://api.ashbyhq.com/posting-api/job-board/{job_board_name}"
        "?includeCompensation=true"
    )


def parse_ashby_postings(raw_board_document: bytes) -> list[AtsPosting]:
    payload = _decode_json(raw_board_document, vendor=AtsVendor.ASHBY)
    if not isinstance(payload, dict):
        raise _MalformedBoard("ashby board document is not a JSON object")
    jobs = payload.get("jobs")
    if not isinstance(jobs, list):
        raise _MalformedBoard("ashby board document missing a 'jobs' array")
    postings: list[AtsPosting] = []
    for index, job in enumerate(jobs):
        if not isinstance(job, dict) or job.get("id") is None:
            raise _MalformedBoard(
                f"ashby jobs[{index}] is not an object with a non-null 'id'"
            )
        country = None
        address = job.get("address")
        if isinstance(address, dict):
            postal = address.get("postalAddress")
            if isinstance(postal, dict):
                country = postal.get("addressCountry")
        is_listed = job.get("isListed")
        postings.append(
            AtsPosting(
                ats_job_id=str(job.get("id")),
                title=_plain(job.get("title")),
                description=_plain(job.get("descriptionPlain")) or _html_to_text(job.get("descriptionHtml")),
                posted_date=_plain(job.get("publishedAt")),
                source_url=_plain(job.get("jobUrl")) or _plain(job.get("applyUrl")),
                location_raw=_plain(job.get("location")),
                location_country=_plain(country),
                is_listed=is_listed if isinstance(is_listed, bool) else None,
            )
        )
    return postings


def fetch_ashby_board(
    *,
    company: str,
    job_board_name: str,
    transport: AtsHttpTransport,
) -> AtsBoardCaptureResult:
    url = ashby_board_url(job_board_name)
    try:
        response = transport.get(url=url, headers={})
    except AtsTransportError as exc:
        return AtsBoardCaptureFailure(
            vendor=AtsVendor.ASHBY,
            board_locator=url,
            company=company,
            failure_kind=exc.failure_kind,
            message=str(exc),
        )
    if not _ok(response.status):
        return _status_failure(
            vendor=AtsVendor.ASHBY, board_locator=url, company=company, status=response.status, reason=""
        )
    return _finish_get_board(
        vendor=AtsVendor.ASHBY,
        company=company,
        board_locator=url,
        response=response,
        parser=parse_ashby_postings,
    )


def _finish_get_board(
    *,
    vendor: AtsVendor,
    company: str,
    board_locator: str,
    response: AtsHttpResponse,
    parser: Callable[[bytes], list[AtsPosting]],
) -> AtsBoardCaptureResult:
    try:
        postings = parser(response.body)
    except _MalformedBoard as exc:
        return AtsBoardCaptureFailure(
            vendor=vendor,
            board_locator=board_locator,
            company=company,
            failure_kind=AtsCaptureFailureKind.MALFORMED_RESPONSE,
            message=str(exc),
            http_status=response.status,
        )
    limitation_notes: list[str] = []
    if not postings:
        limitation_notes.append(
            f"{vendor.value} board returned zero postings (an empty board is a valid dated snapshot)"
        )
    return AtsBoardCaptureSuccess(
        vendor=vendor,
        board_locator=board_locator,
        company=company,
        http_status=response.status,
        raw_board_document=response.body,
        postings=tuple(postings),
        limitation_notes=limitation_notes,
    )


# --------------------------------------------------------------------------- #
# Workday: POST /wday/cxs/{tenant}/{site}/jobs (offset paging) + per-job detail
# --------------------------------------------------------------------------- #
#
# Workday needs several calls: an offset-paginated POST list, then one GET per
# job for its description. The successful response bodies are retained as exact
# UTF-8 strings inside one lossless JSON envelope so the projection parses raw
# through one path. CSRF is optional: the list POST is attempted
# without a token; on HTTP 403 a token is read from the careers-page Set-Cookie
# and the POST retried. The token is a request header only and is never stored.


def workday_host(tenant: str, wd_server: str) -> str:
    return f"https://{tenant}.{wd_server}.myworkdayjobs.com"


def workday_jobs_url(tenant: str, wd_server: str, site: str) -> str:
    return f"{workday_host(tenant, wd_server)}/wday/cxs/{tenant}/{site}/jobs"


def _workday_detail_url(tenant: str, wd_server: str, site: str, external_path: str) -> str:
    path = external_path if external_path.startswith("/") else f"/{external_path}"
    return f"{workday_host(tenant, wd_server)}/wday/cxs/{tenant}/{site}{path}"


def _extract_calypso_token(headers: Mapping[str, str]) -> str | None:
    cookie = headers.get("Set-Cookie") or headers.get("set-cookie")
    if not cookie:
        return None
    match = re.search(r"CALYPSO_CSRF_TOKEN=([^;]+)", cookie)
    return match.group(1) if match else None


def parse_workday_postings(raw_board_document: bytes) -> list[AtsPosting]:
    """Parse the lossless Workday response-body envelope.

    Detail responses are an ORDERED list of slots (one per list posting, in the
    same flattened order), never a path-keyed map — so duplicate externalPaths
    keep distinct bodies and gaps stay explicit (F8). A slot is paired to its
    posting by position; the slot's external_path must match its posting's."""
    payload = _decode_json(raw_board_document, vendor=AtsVendor.WORKDAY)
    if not isinstance(payload, dict):
        raise _MalformedBoard("workday envelope is not a JSON object")
    list_page_documents = payload.get("list_page_documents")
    job_detail_documents = payload.get("job_detail_documents")
    if not isinstance(list_page_documents, list) or not isinstance(job_detail_documents, list):
        raise _MalformedBoard(
            "workday envelope missing 'list_page_documents' array or "
            "'job_detail_documents' array"
        )

    list_pages = [
        _decode_workday_embedded_json(document, label=f"list_page_documents[{index}]")
        for index, document in enumerate(list_page_documents)
    ]

    # Flatten list postings in order; this order defines detail-slot pairing.
    flat_postings: list[dict[str, object]] = []
    for page_index, page in enumerate(list_pages):
        if not isinstance(page, dict):
            raise _MalformedBoard(f"workday list page {page_index} is not a JSON object")
        page_postings = page.get("jobPostings")
        if not isinstance(page_postings, list):
            raise _MalformedBoard(
                f"workday list page {page_index} missing a 'jobPostings' array"
            )
        for posting_index, posting in enumerate(page_postings):
            if not isinstance(posting, dict) or _plain(posting.get("externalPath")) is None:
                raise _MalformedBoard(
                    f"workday list page {page_index} posting {posting_index} "
                    "is not an object with a non-empty 'externalPath'"
                )
            flat_postings.append(posting)

    if job_detail_documents and len(job_detail_documents) != len(flat_postings):
        raise _MalformedBoard(
            f"workday envelope has {len(job_detail_documents)} detail slot(s) for "
            f"{len(flat_postings)} posting(s); expected one ordered slot per posting"
        )

    base_url = payload.get("board_base_url")
    postings: list[AtsPosting] = []
    for index, posting in enumerate(flat_postings):
        external_path = _plain(posting.get("externalPath"))
        detail_info = _workday_detail_info(
            job_detail_documents[index] if job_detail_documents else None,
            index=index,
            external_path=external_path,
        )
        description = None
        posted_date = None
        source_url = None
        location_country = None
        if detail_info:
            description = (
                _html_to_text(detail_info.get("jobDescription"))
                or _plain(detail_info.get("jobDescription"))
            )
            posted_date = _plain(detail_info.get("startDate")) or _plain(detail_info.get("postedOn"))
            source_url = _plain(detail_info.get("externalUrl"))
            location_country = _workday_structured_country(detail_info)
        if source_url is None and external_path and isinstance(base_url, str):
            source_url = f"{base_url.rstrip('/')}{external_path}"
        postings.append(
            AtsPosting(
                ats_job_id=external_path,
                title=_plain(posting.get("title")),
                description=description,
                posted_date=posted_date or _plain(posting.get("postedOn")),
                source_url=source_url,
                location_raw=_plain(posting.get("locationsText")),
                location_country=location_country,
            )
        )
    return postings


def _workday_detail_info(
    slot: object, *, index: int, external_path: str | None
) -> dict[str, object]:
    """Resolve one ordered detail slot to its ``jobPostingInfo``, or ``{}`` for a
    gap slot (a failed/non-2xx/unparseable/shape-invalid detail). A slot whose
    ``external_path`` disagrees with its positionally-paired posting is malformed."""
    if slot is None:
        return {}
    if not isinstance(slot, dict):
        raise _MalformedBoard(f"workday detail slot {index} is not an object")
    slot_path = _plain(slot.get("external_path"))
    if slot_path is not None and external_path is not None and slot_path != external_path:
        raise _MalformedBoard(
            f"workday detail slot {index} external_path {slot_path!r} does not match "
            f"posting external_path {external_path!r}"
        )
    body = slot.get("response_body")
    if body is None:
        return {}  # explicit gap slot
    detail = _decode_workday_embedded_json(body, label=f"job_detail_documents[{index}]")
    if not isinstance(detail, dict) or not isinstance(detail.get("jobPostingInfo"), dict):
        raise _MalformedBoard(
            f"workday detail slot {index} missing a 'jobPostingInfo' object"
        )
    return detail["jobPostingInfo"]


def _decode_workday_embedded_json(document: object, *, label: str) -> object:
    if not isinstance(document, str):
        raise _MalformedBoard(f"workday {label} is not a UTF-8 response-body string")
    try:
        return json.loads(document)
    except json.JSONDecodeError as exc:
        raise _MalformedBoard(f"workday {label} was not valid JSON: {exc}") from exc


def _workday_structured_country(detail_info: Mapping[str, object]) -> str | None:
    """Return only a Workday-provided structured country value; never parse location text."""

    candidates: list[object] = [detail_info.get("country")]
    requisition_location = detail_info.get("jobRequisitionLocation")
    if isinstance(requisition_location, dict):
        candidates.append(requisition_location.get("country"))
    for candidate in candidates:
        if isinstance(candidate, dict):
            value = _plain(candidate.get("descriptor")) or _plain(candidate.get("alpha2Code"))
        else:
            value = _plain(candidate)
        if value is not None:
            return value
    return None


def fetch_workday_board(
    *,
    company: str,
    tenant: str,
    wd_server: str,
    site: str,
    transport: AtsHttpTransport,
    sleep: SleepFn | None = None,
    delay_seconds: float = DEFAULT_DELAY_SECONDS,
    page_size: int = DEFAULT_WORKDAY_PAGE_SIZE,
    max_pages: int = DEFAULT_WORKDAY_MAX_PAGES,
    fetch_details: bool = True,
) -> AtsBoardCaptureResult:
    if delay_seconds < 0:
        raise ValueError("delay_seconds must be non-negative")
    if page_size <= 0:
        raise ValueError("page_size must be greater than zero")
    if max_pages <= 0:
        raise ValueError("max_pages must be greater than zero")

    sleep = sleep or _default_sleep
    jobs_url = workday_jobs_url(tenant, wd_server, site)
    board_base_url = f"{workday_host(tenant, wd_server)}/{site}"
    headers = {"Content-Type": "application/json"}
    list_page_documents: list[str] = []
    warning_notes: list[str] = []
    limitation_notes: list[str] = []

    csrf_token: str | None = None
    offset = 0
    total: int | None = None
    for page_index in range(max_pages):
        body = json.dumps(
            {"appliedFacets": {}, "limit": page_size, "offset": offset, "searchText": ""}
        ).encode("utf-8")
        request_headers = dict(headers)
        if csrf_token is not None:
            request_headers["X-Calypso-Csrf-Token"] = csrf_token
        try:
            response = transport.post(url=jobs_url, headers=request_headers, body=body)
        except AtsTransportError as exc:
            return AtsBoardCaptureFailure(
                vendor=AtsVendor.WORKDAY,
                board_locator=jobs_url,
                company=company,
                failure_kind=exc.failure_kind,
                message=str(exc),
            )
        if response.status == 403 and csrf_token is None:
            csrf_token = _fetch_workday_csrf(transport, board_base_url)
            if csrf_token is not None:
                warning_notes.append("workday list POST retried with a CSRF token after HTTP 403")
                request_headers["X-Calypso-Csrf-Token"] = csrf_token
                try:
                    response = transport.post(
                        url=jobs_url, headers=request_headers, body=body
                    )
                except AtsTransportError as exc:
                    return AtsBoardCaptureFailure(
                        vendor=AtsVendor.WORKDAY,
                        board_locator=jobs_url,
                        company=company,
                        failure_kind=exc.failure_kind,
                        message=str(exc),
                    )
        if not _ok(response.status):
            return _status_failure(
                vendor=AtsVendor.WORKDAY,
                board_locator=jobs_url,
                company=company,
                status=response.status,
                reason="",
            )
        try:
            page_document = response.body.decode("utf-8")
            page = json.loads(page_document)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            return AtsBoardCaptureFailure(
                vendor=AtsVendor.WORKDAY,
                board_locator=jobs_url,
                company=company,
                failure_kind=AtsCaptureFailureKind.MALFORMED_RESPONSE,
                message=f"workday list page was not valid JSON: {exc}",
                http_status=response.status,
            )
        if not isinstance(page, dict) or not isinstance(page.get("jobPostings"), list):
            return AtsBoardCaptureFailure(
                vendor=AtsVendor.WORKDAY,
                board_locator=jobs_url,
                company=company,
                failure_kind=AtsCaptureFailureKind.MALFORMED_RESPONSE,
                message="workday list page missing a 'jobPostings' array",
                http_status=response.status,
            )
        for posting_index, posting in enumerate(page["jobPostings"]):
            if not isinstance(posting, dict) or _plain(posting.get("externalPath")) is None:
                return AtsBoardCaptureFailure(
                    vendor=AtsVendor.WORKDAY,
                    board_locator=jobs_url,
                    company=company,
                    failure_kind=AtsCaptureFailureKind.MALFORMED_RESPONSE,
                    message=(
                        f"workday list posting {posting_index} is not an object with "
                        "a non-empty 'externalPath'"
                    ),
                    http_status=response.status,
                )
        list_page_documents.append(page_document)
        page_postings = page.get("jobPostings") if isinstance(page, dict) else None
        if total is None and isinstance(page, dict):
            total = page.get("total") if isinstance(page.get("total"), int) else None
        count = len(page_postings) if isinstance(page_postings, list) else 0
        offset += count
        if count == 0 or (total is not None and offset >= total):
            break
        if page_index + 1 < max_pages:
            sleep(delay_seconds)
    else:
        limitation_notes.append(
            f"workday paging stopped at max_pages={max_pages}; the board may have more postings"
        )

    external_paths: list[str] = []
    for page_document in list_page_documents:
        page = json.loads(page_document)
        for posting in page["jobPostings"]:
            external_paths.append(posting["externalPath"])

    # One ORDERED detail slot per list posting, positionally aligned to the
    # flattened posting order — never a path-keyed map. Two postings that share an
    # externalPath therefore keep DISTINCT detail bodies (no dedupe/overwrite), and
    # a failed, non-2xx, unparseable, or shape-invalid detail is an EXPLICIT gap
    # slot, never a silent drop (F8). Each slot carries its external_path for a
    # positional-integrity check at parse time.
    job_detail_documents: list[dict[str, str]] = []
    if fetch_details:
        for external_path in external_paths:
            sleep(delay_seconds)
            detail_url = _workday_detail_url(tenant, wd_server, site, external_path)
            slot: dict[str, str] = {"external_path": external_path}
            try:
                detail_response = transport.get(url=detail_url, headers={})
            except AtsTransportError as exc:
                slot["gap_reason"] = f"detail fetch failed: {exc}"
                limitation_notes.append(
                    f"workday job detail fetch failed for {external_path}: {exc}"
                )
                job_detail_documents.append(slot)
                continue
            if not _ok(detail_response.status):
                slot["gap_reason"] = f"detail returned HTTP {detail_response.status}"
                limitation_notes.append(
                    f"workday job detail returned HTTP {detail_response.status} for {external_path}"
                )
                job_detail_documents.append(slot)
                continue
            try:
                detail_document = detail_response.body.decode("utf-8")
                detail = json.loads(detail_document)
            except (json.JSONDecodeError, UnicodeDecodeError):
                slot["gap_reason"] = "detail body was not valid JSON"
                limitation_notes.append(
                    f"workday job detail was not valid JSON for {external_path}"
                )
                job_detail_documents.append(slot)
                continue
            if not isinstance(detail, dict) or not isinstance(
                detail.get("jobPostingInfo"), dict
            ):
                slot["gap_reason"] = "detail missing jobPostingInfo object"
                limitation_notes.append(
                    f"workday job detail missing jobPostingInfo object for {external_path}"
                )
                job_detail_documents.append(slot)
                continue
            slot["response_body"] = detail_document
            job_detail_documents.append(slot)
    else:
        limitation_notes.append("workday job descriptions not fetched (fetch_details=False)")

    envelope = {
        "board_base_url": board_base_url,
        "list_page_documents": list_page_documents,
        "job_detail_documents": job_detail_documents,
    }
    raw_board_document = (json.dumps(envelope, sort_keys=True) + "\n").encode("utf-8")
    try:
        postings = parse_workday_postings(raw_board_document)
    except _MalformedBoard as exc:
        return AtsBoardCaptureFailure(
            vendor=AtsVendor.WORKDAY,
            board_locator=jobs_url,
            company=company,
            failure_kind=AtsCaptureFailureKind.MALFORMED_RESPONSE,
            message=str(exc),
        )
    if not postings:
        limitation_notes.append(
            "workday board returned zero postings (an empty board is a valid dated snapshot)"
        )
    return AtsBoardCaptureSuccess(
        vendor=AtsVendor.WORKDAY,
        board_locator=jobs_url,
        company=company,
        http_status=200,
        raw_board_document=raw_board_document,
        postings=tuple(postings),
        warning_notes=warning_notes,
        limitation_notes=limitation_notes,
    )


def _fetch_workday_csrf(transport: AtsHttpTransport, board_base_url: str) -> str | None:
    try:
        response = transport.get(url=board_base_url, headers={"Accept": "text/html"})
    except AtsTransportError:
        return None
    return _extract_calypso_token(response.headers)


def _default_sleep(seconds: float) -> None:
    import time

    time.sleep(seconds)


# --------------------------------------------------------------------------- #
# Projection-facing dispatch (parse verbatim raw by exactly one path)
# --------------------------------------------------------------------------- #

_PARSERS: dict[AtsVendor, Callable[[bytes], list[AtsPosting]]] = {
    AtsVendor.GREENHOUSE: parse_greenhouse_postings,
    AtsVendor.LEVER: parse_lever_postings,
    AtsVendor.ASHBY: parse_ashby_postings,
    AtsVendor.WORKDAY: parse_workday_postings,
}


def parse_board_postings(vendor: AtsVendor, raw_board_document: bytes) -> list[AtsPosting]:
    """Parse a preserved verbatim raw board document into postings (projection path)."""
    parser = _PARSERS.get(AtsVendor(vendor))
    if parser is None:
        raise ValueError(f"no parser for ATS vendor {vendor!r}")
    return parser(raw_board_document)


__all__ = [
    "AtsBoardCaptureFailure",
    "AtsBoardCaptureResult",
    "AtsBoardCaptureSuccess",
    "AtsCaptureFailureKind",
    "AtsHttpResponse",
    "AtsHttpTransport",
    "AtsPosting",
    "AtsTransportError",
    "AtsVendor",
    "StdlibAtsHttpTransport",
    "ashby_board_url",
    "fetch_ashby_board",
    "fetch_greenhouse_board",
    "fetch_lever_board",
    "fetch_workday_board",
    "greenhouse_board_url",
    "lever_board_url",
    "parse_ashby_postings",
    "parse_board_postings",
    "parse_greenhouse_postings",
    "parse_lever_postings",
    "parse_workday_postings",
    "workday_jobs_url",
]
