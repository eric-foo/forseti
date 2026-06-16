"""archive.today capture adapter -- the second general-archive locate+body rung of slice E.

This is the **archive.today** rung of the cross-archive historical-capture ladder
(`source_capture/historical_capture.py`). It is the sibling of `archive_org.py` (Wayback):
where Wayback exposes a CDX availability API, archive.today exposes a Memento **TimeMap**
(`https://archive.ph/timemap/<url>`) that lists every memento it holds for a URL. This adapter:

- fetches the TimeMap, parses the `application/link-format` body into mementos (each memento URL
  carries a 14-digit `YYYYMMDDhhmmss` timestamp in its path, plus a `datetime=` link param);
- selects the latest memento at or before a cutoff (the per-archive ``<=cutoff`` leak guard,
  mirroring ``archive_org.select_snapshot``);
- fetches that memento's body and verifies the **served** snapshot (slice G): the served URL is
  under an archive.today mirror-family host, its served timestamp is ``<= cutoff``, and it still
  addresses the requested original URL. An off-family host, a served-time leak, an identity
  mismatch, or -- when a cutoff is set -- an unparseable served time is a verification FAILURE,
  never a silent pass.

**No-gate-defeat (hard line, honored here):** archive.today sits behind nginx and throttles with
HTTP 429 (a transient *rate limit*, retried with backoff -- in-posture). That is distinct from a
Cloudflare/anti-bot **challenge** (interstitial / CAPTCHA / "just a moment" / "checking your
browser"). A challenge is the gate-defeat line: this adapter detects it and **STOPS** (records
``gate_defeat_stop``), it never solves it. ``direct_http`` does not surface raw response headers,
so challenge detection inspects the response *body markers* (the same signal a human sees), which
also will not misclassify the plain 429 rate-limit page as a challenge.

All HTTP goes through ``fetch_direct_http_capture`` (no ``urllib.request`` / ``requests`` here, per
the adapter no-forbidden-import contract). The bounded 429/503/504 retry helper below is an
intentional small parallel of ``archive_org._fetch_with_retry`` -- it is **duplicated, not shared**,
to keep each archive's adapter isolated and to avoid refactoring ``archive_org.py``'s existing path
(the foregone DRY is named, not hidden). This adapter never imports the writer and never constructs
a packet; a runner translates the result into writer kwargs.
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import TypeAlias
from urllib.parse import urlparse

from source_capture.adapters.direct_http import (
    DEFAULT_MAX_BYTES,
    DEFAULT_TIMEOUT_SECONDS,
    DirectHttpCaptureFailure,
    DirectHttpCaptureResult,
    DirectHttpCaptureSuccess,
    fetch_direct_http_capture,
)


DEFAULT_TIMEMAP_BASE_URL = "https://archive.ph/timemap"

# archive.today is one service behind many rotating mirror domains. A memento located via one
# mirror (the live TimeMap currently answers from archive.md) may serve its body from any family
# member, so served-time host-anchoring accepts the whole family rather than a single base. This is
# the archive.today analogue of archive_org's single-base anchor; the family is closed + maintained
# (named limitation: a new mirror domain must be added here), never an open "any host" anchor.
_ARCHIVE_TODAY_HOSTS = frozenset(
    {
        "archive.today",
        "archive.ph",
        "archive.is",
        "archive.li",
        "archive.md",
        "archive.vn",
        "archive.fo",
        "archive.ec",
    }
)

# Bounded retry for transient archive.today rate-limiting (HTTP 429/503/504). archive.today throttles
# per-IP under load; a few backed-off retries let a transient rate limit self-heal. Persistent
# throttling still surfaces honestly as access_failed, never a fabricated success. Intentional small
# parallel of archive_org._fetch_with_retry (duplicated to keep adapters isolated; see module docs).
DEFAULT_MAX_ATTEMPTS = 4
DEFAULT_RETRY_BACKOFF_SECONDS = 2.0
_RATE_LIMIT_STATUSES = frozenset({429, 503, 504})

# A memento URL carries the captured time as a 14-digit path segment: <host>/<14>/<original_url>.
# archive.today does not use Wayback's replay modifiers (id_/im_/...), so no modifier tolerance is
# needed here; the original URL is whatever follows the timestamp segment.
_MEMENTO_URL_RE = re.compile(r"^https?://(?P<host>[^/]+)/(?P<ts>\d{14})/(?P<url>.+)$")

# Cloudflare / anti-bot challenge markers (gate-defeat line). These appear in challenge interstitial
# bodies regardless of status code; the plain archive.today 429 rate-limit page carries none of them.
_CHALLENGE_MARKERS = (
    "just a moment",
    "checking your browser",
    "challenge-platform",
    "cf-chl",
    "cf_chl",
    "/cdn-cgi/challenge",
    "hcaptcha",
    "recaptcha",
)
_CAPTCHA_CONTEXT_MARKERS = (
    "complete the captcha",
    "solve the captcha",
    "verify you are human",
    "verify that you are human",
    "security check",
    "access denied",
    "enable cookies",
    "enable javascript",
    "cloudflare",
)


@dataclass(frozen=True)
class ArchiveTodayMemento:
    timestamp: str  # 14-digit YYYYMMDDhhmmss parsed from the memento URL path
    original_url: str
    memento_url: str
    datetime_header: str | None = None  # the TimeMap link `datetime=` value (RFC1123), if present


@dataclass(frozen=True)
class ArchiveTodayBodyVerification:
    # Slice G verdict for a retrieved archive.today body: whether the SERVED memento (parsed from the
    # post-redirect final_url) is on an archive.today family host, holds the no-lookahead line
    # (served_ts <= cutoff), and still addresses the requested original URL.
    ok: bool
    served_timestamp: str | None
    reason: str | None = None


@dataclass(frozen=True)
class ArchiveTodayCaptureSuccess:
    original_url: str
    timemap_url: str
    timemap_result: DirectHttpCaptureSuccess
    mementos: list[ArchiveTodayMemento]
    selected_memento: ArchiveTodayMemento | None
    body_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None = None
    parse_warning: str | None = None
    body_verification: ArchiveTodayBodyVerification | None = None
    # Set when a Cloudflare/anti-bot CHALLENGE was detected on the body fetch (gate-defeat line):
    # the body is NOT preserved and NOT solved; this records the honest STOP. A transient 429 rate
    # limit is NOT a gate defeat -- it is retried, then surfaces as a body access_failed.
    gate_defeat_stop: str | None = None


@dataclass(frozen=True)
class ArchiveTodayCaptureFailure:
    # The TimeMap lookup itself did not yield a usable listing -- no memento could even be located.
    # `timemap_result` may be a transport Failure, or a Success whose status was non-2xx (e.g. a
    # persistent 429 rate-limit page) or a detected challenge body (then `gate_defeat_stop` is set).
    original_url: str
    timemap_url: str
    timemap_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure
    gate_defeat_stop: str | None = None
    limitation_notes: list[str] = field(default_factory=list)


ArchiveTodayCaptureResult: TypeAlias = ArchiveTodayCaptureSuccess | ArchiveTodayCaptureFailure


def fetch_archive_today_capture(
    *,
    original_url: str,
    cutoff_timestamp: str | None = None,
    timemap_base_url: str = DEFAULT_TIMEMAP_BASE_URL,
    archive_today_hosts: frozenset[str] = _ARCHIVE_TODAY_HOSTS,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_BYTES,
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    retry_backoff_seconds: float = DEFAULT_RETRY_BACKOFF_SECONDS,
) -> ArchiveTodayCaptureResult:
    """Latest archive.today memento of ``original_url`` at or before ``cutoff_timestamp``.

    ``cutoff_timestamp`` is the 14-digit Wayback form (the orchestrator converts its canonical
    ISO-8601 cutoff once and hands both general-archive rungs the same 14-digit value). A failed /
    non-2xx / challenged TimeMap -> ``ArchiveTodayCaptureFailure``; no pre-cutoff memento -> success
    with ``selected_memento=None`` (NO-GO); a failed/challenged body fetch -> success with a
    failure/None ``body_result`` (PARTIAL); a clean pre-cutoff body -> success with
    ``body_verification.ok``.
    """
    normalized_original_url = _validate_original_url(original_url)
    if cutoff_timestamp is not None:
        _validate_wayback_timestamp(cutoff_timestamp)

    timemap_url = build_timemap_url(
        original_url=normalized_original_url, timemap_base_url=timemap_base_url
    )
    timemap_result = _fetch_with_retry(
        url=timemap_url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
        max_attempts=max_attempts,
        retry_backoff_seconds=retry_backoff_seconds,
    )

    # Transport failure -> cannot locate.
    if isinstance(timemap_result, DirectHttpCaptureFailure):
        return ArchiveTodayCaptureFailure(
            original_url=normalized_original_url,
            timemap_url=timemap_url,
            timemap_result=timemap_result,
            limitation_notes=[f"access_failed: archive.today TimeMap {timemap_result.failure_kind}"],
        )

    # Gate-defeat line: a challenge body is a hard STOP, never solved.
    gate_defeat = _detect_gate_defeat(timemap_result)
    if gate_defeat is not None:
        return ArchiveTodayCaptureFailure(
            original_url=normalized_original_url,
            timemap_url=timemap_url,
            timemap_result=timemap_result,
            gate_defeat_stop=gate_defeat,
            limitation_notes=[f"gate_defeat_stop: archive.today TimeMap {gate_defeat}"],
        )

    # A non-2xx TimeMap (body preserved by direct_http, e.g. a persistent 429 rate-limit page) is NOT
    # usable listing evidence -- treat it as access_failed, mirroring publisher_history's PH-01.
    if timemap_result.status < 200 or timemap_result.status >= 300:
        return ArchiveTodayCaptureFailure(
            original_url=normalized_original_url,
            timemap_url=timemap_url,
            timemap_result=timemap_result,
            limitation_notes=[
                f"access_failed: archive.today TimeMap returned HTTP {timemap_result.status} "
                f"{timemap_result.reason or 'without reason'}; response body preserved but not parsed"
            ],
        )

    mementos: list[ArchiveTodayMemento]
    parse_warning: str | None = None
    try:
        mementos = parse_timemap_mementos(
            timemap_result.body,
            requested_original_url=normalized_original_url,
            allowed_hosts=archive_today_hosts,
        )
    except (ValueError, UnicodeDecodeError) as exc:
        mementos = []
        parse_warning = f"archive_today TimeMap parse_failed: {exc}"

    selected_memento = select_memento(mementos, cutoff_timestamp=cutoff_timestamp)

    body_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None = None
    body_verification: ArchiveTodayBodyVerification | None = None
    gate_defeat_stop: str | None = None
    if selected_memento is not None:
        raw_body = _fetch_with_retry(
            url=selected_memento.memento_url,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
            max_attempts=max_attempts,
            retry_backoff_seconds=retry_backoff_seconds,
        )
        if isinstance(raw_body, DirectHttpCaptureSuccess):
            body_gate_defeat = _detect_gate_defeat(raw_body)
            if body_gate_defeat is not None:
                # STOP at the gate-defeat boundary: do not preserve or trust a challenge body.
                gate_defeat_stop = body_gate_defeat
            else:
                body_result = raw_body
                body_verification = verify_archive_today_body(
                    body_result=raw_body,
                    requested_original_url=selected_memento.original_url,
                    cutoff_timestamp=cutoff_timestamp,
                    allowed_hosts=archive_today_hosts,
                )
        else:
            body_result = raw_body  # transport failure -> PARTIAL

    return ArchiveTodayCaptureSuccess(
        original_url=normalized_original_url,
        timemap_url=timemap_url,
        timemap_result=timemap_result,
        mementos=mementos,
        selected_memento=selected_memento,
        body_result=body_result,
        parse_warning=parse_warning,
        body_verification=body_verification,
        gate_defeat_stop=gate_defeat_stop,
    )


def build_timemap_url(*, original_url: str, timemap_base_url: str = DEFAULT_TIMEMAP_BASE_URL) -> str:
    """archive.today TimeMap URL: ``<base>/<original_url>`` (the raw URL is appended in the path)."""
    parsed_base = urlparse(timemap_base_url)
    if parsed_base.scheme not in {"http", "https"} or not parsed_base.netloc:
        raise ValueError("archive.today TimeMap base URL requires an absolute http:// or https:// URL")
    return f"{timemap_base_url.rstrip('/')}/{original_url}"


def parse_timemap_mementos(
    body: bytes,
    *,
    requested_original_url: str,
    allowed_hosts: frozenset[str] = _ARCHIVE_TODAY_HOSTS,
) -> list[ArchiveTodayMemento]:
    """Parse an ``application/link-format`` TimeMap body into mementos with served-time proof.

    Link-format entries are ``<uri>; rel="..."; datetime="..."`` separated by commas, but the
    RFC1123 ``datetime`` value itself contains a comma (``"Sat, 31 Dec 1994 ..."``), so we cannot
    naively split on commas. Instead we locate each ``<uri>`` by position and read the parameters
    that follow it up to the next ``<uri>``. Only entries whose ``rel`` contains ``memento`` are
    kept (``original``/``timegate``/``self`` are skipped), and only those whose memento URL exposes a
    parseable 14-digit timestamp on an archive.today family host are admitted -- an entry without a
    parseable served timestamp is not trusted (AR-02: served time is what proves no-lookahead).
    """
    text = body.decode("utf-8", "strict")
    uri_spans = list(re.finditer(r"<([^>]*)>", text))
    mementos: list[ArchiveTodayMemento] = []
    for index, match in enumerate(uri_spans):
        uri = match.group(1).strip()
        params_start = match.end()
        params_end = uri_spans[index + 1].start() if index + 1 < len(uri_spans) else len(text)
        params = text[params_start:params_end]

        rel_match = re.search(r'rel\s*=\s*"([^"]*)"', params)
        if rel_match is None or "memento" not in rel_match.group(1).lower():
            continue

        url_match = _MEMENTO_URL_RE.match(uri)
        if url_match is None:
            continue
        if url_match.group("host").lower() not in allowed_hosts:
            continue

        datetime_match = re.search(r'datetime\s*=\s*"([^"]*)"', params)
        mementos.append(
            ArchiveTodayMemento(
                timestamp=url_match.group("ts"),
                original_url=url_match.group("url"),
                memento_url=uri,
                datetime_header=datetime_match.group(1) if datetime_match else None,
            )
        )
    return mementos


def select_memento(
    mementos: list[ArchiveTodayMemento],
    *,
    cutoff_timestamp: str | None = None,
) -> ArchiveTodayMemento | None:
    """Latest memento at or before the cutoff (the per-archive ``<=cutoff`` leak guard).

    14-digit timestamps are fixed-width, so lexical ordering equals chronological ordering. Mirrors
    ``archive_org.select_snapshot``. With no cutoff, returns the newest memento.
    """
    if not mementos:
        return None
    if cutoff_timestamp is not None:
        eligible = [memento for memento in mementos if memento.timestamp <= cutoff_timestamp]
        if not eligible:
            return None
        return max(eligible, key=lambda memento: memento.timestamp)
    return max(mementos, key=lambda memento: memento.timestamp)


def verify_archive_today_body(
    *,
    body_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None,
    requested_original_url: str,
    cutoff_timestamp: str | None,
    allowed_hosts: frozenset[str] = _ARCHIVE_TODAY_HOSTS,
) -> ArchiveTodayBodyVerification | None:
    """Slice G served-time no-lookahead guard for an archive.today body.

    The select-time ``<=cutoff`` check cannot see that a memento request may resolve (or redirect) to
    a different captured time, so this verifies the SERVED memento (parsed from the post-redirect
    final_url): it must be on an archive.today family host, address the requested original URL, and
    carry a served timestamp ``<= cutoff``. An off-family host, an identity drift, a served-time
    leak, or -- when a cutoff is set -- an unparseable served time is a verification FAILURE, never a
    silent pass. With no cutoff and an unparseable served time, the family-host check alone passes
    (served_timestamp=None), mirroring archive_org's no-cutoff behavior. Content-integrity checks
    (soft-404 / charset) are a separate deferred slice.
    """
    if not isinstance(body_result, DirectHttpCaptureSuccess):
        return None  # no preserved body to verify; body-not-preserved is handled by the caller
    if body_result.status < 200 or body_result.status >= 300:
        return ArchiveTodayBodyVerification(
            ok=False,
            served_timestamp=None,
            reason=(
                f"body_http_status_not_usable: archive.today body returned HTTP {body_result.status} "
                f"{body_result.reason or 'without reason'}; availability is not body honesty"
            ),
        )
    match = _MEMENTO_URL_RE.match(body_result.final_url)
    if match is None or match.group("host").lower() not in allowed_hosts:
        host = urlparse(body_result.final_url).netloc
        if host.lower() not in allowed_hosts:
            return ArchiveTodayBodyVerification(
                ok=False,
                served_timestamp=None,
                reason=(
                    f"served_off_archive_host: final_url {body_result.final_url!r} is not on an "
                    f"archive.today mirror-family host"
                ),
            )
        # On a family host but the path is not the <14>/<url> form (e.g. a short canonical URL):
        # the served time cannot be read from the URL.
        if cutoff_timestamp is None:
            return ArchiveTodayBodyVerification(ok=True, served_timestamp=None)
        return ArchiveTodayBodyVerification(
            ok=False,
            served_timestamp=None,
            reason=(
                "served_time_unverifiable: could not parse a 14-digit served timestamp from "
                f"archive.today URL {body_result.final_url!r}"
            ),
        )
    served_timestamp, served_original_url = match.group("ts"), match.group("url")
    if served_original_url != requested_original_url:
        return ArchiveTodayBodyVerification(
            ok=False,
            served_timestamp=served_timestamp,
            reason=(
                f"served_url_identity_mismatch: served {served_original_url!r} "
                f"!= requested {requested_original_url!r}"
            ),
        )
    if cutoff_timestamp is not None and served_timestamp > cutoff_timestamp:
        return ArchiveTodayBodyVerification(
            ok=False,
            served_timestamp=served_timestamp,
            reason=(
                f"served_time_leak: served memento {served_timestamp} is after cutoff "
                f"{cutoff_timestamp} (no-lookahead violation the select-time <=cutoff guard cannot see)"
            ),
        )
    return ArchiveTodayBodyVerification(ok=True, served_timestamp=served_timestamp)


def _detect_gate_defeat(result: DirectHttpCaptureResult) -> str | None:
    """Return a reason if the response is a Cloudflare/anti-bot CHALLENGE, else None.

    direct_http does not surface raw response headers, so detection inspects the response body for
    challenge markers (the same signal a human sees). A challenge is the gate-defeat line: the caller
    STOPS and never solves it. The plain archive.today 429 rate-limit page carries none of these
    markers, so it is not misclassified as a challenge (it is retried, then surfaces as access_failed).
    """
    if not isinstance(result, DirectHttpCaptureSuccess):
        return None
    text = result.body[:4096].decode("utf-8", "replace").lower()
    for marker in _CHALLENGE_MARKERS:
        if marker in text:
            return (
                f"challenge_detected (HTTP {result.status}); marker {marker!r} present -- "
                "auth/anti-bot challenge is a hard STOP, not solved (no-gate-defeat)"
            )
    if "captcha" in text:
        for marker in _CAPTCHA_CONTEXT_MARKERS:
            if marker in text:
                return (
                    f"challenge_detected (HTTP {result.status}); marker 'captcha' present with "
                    f"context {marker!r} -- auth/anti-bot challenge is a hard STOP, not solved "
                    "(no-gate-defeat)"
                )
    return None


def _is_rate_limited(result: DirectHttpCaptureResult) -> bool:
    # Transient throttling shows up as HTTP 429/503/504 on either the body-preserved success form
    # (status on the success) or the empty-body failure form (status on the failure). Network errors
    # carry no status and are NOT retried here -- they are not a reliable transient rate-limit signal.
    return getattr(result, "status", None) in _RATE_LIMIT_STATUSES


def _fetch_with_retry(
    *,
    url: str,
    timeout_seconds: float,
    max_bytes: int,
    max_attempts: int,
    retry_backoff_seconds: float,
) -> DirectHttpCaptureResult:
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1")
    result = fetch_direct_http_capture(url=url, timeout_seconds=timeout_seconds, max_bytes=max_bytes)
    attempt = 1
    while _is_rate_limited(result) and attempt < max_attempts:
        time.sleep(retry_backoff_seconds * (2 ** (attempt - 1)))
        attempt += 1
        result = fetch_direct_http_capture(url=url, timeout_seconds=timeout_seconds, max_bytes=max_bytes)
    return result


def _validate_original_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("archive.today capture requires an absolute original http:// or https:// URL")
    return parsed.geturl()


def _validate_wayback_timestamp(timestamp: str) -> None:
    if not timestamp.isdigit() or len(timestamp) != 14:
        raise ValueError("archive.today cutoff timestamp must be a 14-digit YYYYMMDDhhmmss value")
