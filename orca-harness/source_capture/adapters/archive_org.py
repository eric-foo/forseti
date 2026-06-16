from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from json import JSONDecodeError
from typing import TypeAlias
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from source_capture.adapters.direct_http import (
    DEFAULT_MAX_BYTES,
    DEFAULT_TIMEOUT_SECONDS,
    DirectHttpCaptureFailure,
    DirectHttpCaptureResult,
    DirectHttpCaptureSuccess,
    fetch_direct_http_capture,
)


DEFAULT_CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"
DEFAULT_SNAPSHOT_BASE_URL = "https://web.archive.org/web"

# Most-recent N rows the CDX availability query returns (negative => newest |N|).
# Bounds the response so long-lived URLs no longer return full history and time
# out. Snapshot selection needs only the single latest pre-cutoff row; -10 keeps
# a small margin for the deferred redirect-resolution case without materially
# growing the response.
DEFAULT_CDX_LIMIT = -10


# Bounded retry for transient Archive.org rate-limiting. CDX availability and
# snapshot-body requests intermittently return HTTP 429/503/504 under load; a few
# backed-off retries let a transient rate-limit self-heal instead of forcing the
# operator to re-run the capture by hand. Persistent failure still surfaces
# honestly (the final access_failed limitation note / non-zero runner exit),
# never a fabricated success.
DEFAULT_MAX_ATTEMPTS = 4
DEFAULT_RETRY_BACKOFF_SECONDS = 2.0
_RATE_LIMIT_STATUSES = frozenset({429, 503, 504})


@dataclass(frozen=True)
class ArchiveOrgSnapshot:
    timestamp: str
    original_url: str
    snapshot_url: str
    status_code: str | None
    mime_type: str | None
    digest: str | None


@dataclass(frozen=True)
class ArchiveBodyVerification:
    # Slice G verdict for a retrieved archive body: whether the SERVED snapshot
    # (parsed from the post-redirect final_url) holds the no-lookahead line.
    ok: bool
    served_timestamp: str | None
    reason: str | None = None


@dataclass(frozen=True)
class ArchiveOrgCaptureSuccess:
    original_url: str
    availability_url: str
    availability_result: DirectHttpCaptureSuccess
    snapshots: list[ArchiveOrgSnapshot]
    selected_snapshot: ArchiveOrgSnapshot | None
    body_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None
    parse_warning: str | None = None
    body_verification: ArchiveBodyVerification | None = None


@dataclass(frozen=True)
class ArchiveOrgCaptureFailure:
    original_url: str
    availability_url: str
    availability_result: DirectHttpCaptureFailure


ArchiveOrgCaptureResult: TypeAlias = ArchiveOrgCaptureSuccess | ArchiveOrgCaptureFailure


def fetch_archive_org_capture(
    *,
    original_url: str,
    cutoff_timestamp: str | None = None,
    cdx_endpoint: str = DEFAULT_CDX_ENDPOINT,
    snapshot_base_url: str = DEFAULT_SNAPSHOT_BASE_URL,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_BYTES,
    limit: int = DEFAULT_CDX_LIMIT,
    max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    retry_backoff_seconds: float = DEFAULT_RETRY_BACKOFF_SECONDS,
) -> ArchiveOrgCaptureResult:
    normalized_original_url = _validate_original_url(original_url)
    if cutoff_timestamp is not None:
        _validate_wayback_timestamp(cutoff_timestamp)

    availability_url = build_cdx_availability_url(
        original_url=normalized_original_url,
        cdx_endpoint=cdx_endpoint,
        cutoff_timestamp=cutoff_timestamp,
        limit=limit,
    )
    availability_result = _fetch_with_retry(
        url=availability_url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
        max_attempts=max_attempts,
        retry_backoff_seconds=retry_backoff_seconds,
    )
    if isinstance(availability_result, DirectHttpCaptureFailure):
        return ArchiveOrgCaptureFailure(
            original_url=normalized_original_url,
            availability_url=availability_url,
            availability_result=availability_result,
        )

    snapshots: list[ArchiveOrgSnapshot]
    parse_warning: str | None = None
    try:
        snapshots = parse_availability_snapshots(
            availability_result.body,
            original_url=normalized_original_url,
            snapshot_base_url=snapshot_base_url,
        )
    except (JSONDecodeError, ValueError) as exc:
        snapshots = []
        parse_warning = f"archive_org availability metadata parse_failed: {exc}"

    selected_snapshot = select_snapshot(snapshots, cutoff_timestamp=cutoff_timestamp)
    body_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None = None
    body_verification: ArchiveBodyVerification | None = None
    if selected_snapshot is not None:
        body_result = _fetch_with_retry(
            url=selected_snapshot.snapshot_url,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
            max_attempts=max_attempts,
            retry_backoff_seconds=retry_backoff_seconds,
        )
        body_verification = verify_archive_body(
            body_result=body_result,
            requested_original_url=selected_snapshot.original_url,
            cutoff_timestamp=cutoff_timestamp,
            snapshot_base_url=snapshot_base_url,
        )

    return ArchiveOrgCaptureSuccess(
        original_url=normalized_original_url,
        availability_url=availability_url,
        availability_result=availability_result,
        snapshots=snapshots,
        selected_snapshot=selected_snapshot,
        body_result=body_result,
        parse_warning=parse_warning,
        body_verification=body_verification,
    )


# Wayback replay form after the archive base: <14-digit ts>[<2-3 char modifier>_]/<original_url>.
# The optional modifier (id_, if_, im_, cs_, js_, ...) must be tolerated or a clean modifier
# replay false-fails (G-001); anchoring to the archive base (below) stops an off-archive
# redirect that merely mimics the /web/<ts>/<url> shape from false-passing (G-001).
_SERVED_SNAPSHOT_RE = re.compile(r"^(\d{14})(?:[a-z]{2,3}_)?/(.+)$")


def verify_archive_body(
    *,
    body_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None,
    requested_original_url: str,
    cutoff_timestamp: str | None,
    snapshot_base_url: str = DEFAULT_SNAPSHOT_BASE_URL,
) -> ArchiveBodyVerification | None:
    # Slice G -- served-time no-lookahead guard. select_snapshot's selection-time
    # <=cutoff check cannot see that Wayback may 302 a pre-cutoff request to a
    # POST-cutoff capture; this verifies the SERVED snapshot (parsed from the
    # post-redirect final_url) came from the expected archive host, is <=cutoff,
    # and still addresses the requested original URL. An off-archive host, a
    # served-time violation, an identity drift, or -- when a cutoff is set -- an
    # unparseable served time is a verification FAILURE, never a silent pass.
    # Content-integrity checks (soft-404 / charset) are a separate deferred slice.
    if not isinstance(body_result, DirectHttpCaptureSuccess):
        return None  # no preserved body to verify; body-not-preserved is handled elsewhere
    if body_result.status < 200 or body_result.status >= 300:
        # A non-2xx served status is a verification failure: direct_http preserves a non-2xx
        # response as a DirectHttpCaptureSuccess (body kept + access_failed limitation), but
        # availability is not body honesty -- a soft-404 / 403 / 429-with-body served from the
        # archive host at a valid <=cutoff replay URL must not pass as a clean archived body
        # (matches the archive_today/publisher-history rungs). Content-integrity checks
        # (soft-404 with HTTP 200 / charset) remain the separate deferred slice noted above.
        return ArchiveBodyVerification(
            ok=False,
            served_timestamp=None,
            reason=(
                f"body_http_status_not_usable: archive snapshot body returned HTTP {body_result.status} "
                f"{body_result.reason or 'without reason'}; availability is not body honesty"
            ),
        )
    base_prefix = snapshot_base_url.rstrip("/") + "/"
    if not body_result.final_url.startswith(base_prefix):
        return ArchiveBodyVerification(
            ok=False,
            served_timestamp=None,
            reason=(
                f"served_off_archive_host: final_url {body_result.final_url!r} is not under the "
                f"expected archive base {base_prefix!r}"
            ),
        )
    match = _SERVED_SNAPSHOT_RE.match(body_result.final_url[len(base_prefix):])
    if match is None:
        if cutoff_timestamp is None:
            return ArchiveBodyVerification(ok=True, served_timestamp=None)
        return ArchiveBodyVerification(
            ok=False,
            served_timestamp=None,
            reason=(
                "served_time_unverifiable: could not parse a 14-digit served snapshot "
                f"timestamp from archive replay URL {body_result.final_url!r}"
            ),
        )
    served_timestamp, served_original_url = match.group(1), match.group(2)
    if served_original_url != requested_original_url:
        return ArchiveBodyVerification(
            ok=False,
            served_timestamp=served_timestamp,
            reason=(
                f"served_url_identity_mismatch: served {served_original_url!r} "
                f"!= requested {requested_original_url!r}"
            ),
        )
    if cutoff_timestamp is not None and served_timestamp > cutoff_timestamp:
        return ArchiveBodyVerification(
            ok=False,
            served_timestamp=served_timestamp,
            reason=(
                f"served_time_leak: served snapshot {served_timestamp} is after cutoff "
                f"{cutoff_timestamp} (no-lookahead violation the select-time <=cutoff guard cannot see)"
            ),
        )
    return ArchiveBodyVerification(ok=True, served_timestamp=served_timestamp)


def _is_rate_limited(result: DirectHttpCaptureResult) -> bool:
    # Transient Archive.org throttling shows up as HTTP 429/503/504 in either the
    # body-preserved success form (status on the success) or the empty-body failure
    # form (status on the failure). Network errors carry no status and are NOT
    # retried here -- they are not a reliable transient rate-limit signal.
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


def build_cdx_availability_url(
    *,
    original_url: str,
    cdx_endpoint: str = DEFAULT_CDX_ENDPOINT,
    cutoff_timestamp: str | None = None,
    limit: int | None = None,
) -> str:
    parsed_endpoint = urlparse(cdx_endpoint)
    if parsed_endpoint.scheme not in {"http", "https"} or not parsed_endpoint.netloc:
        raise ValueError("Archive.org CDX endpoint requires an absolute http:// or https:// URL")

    query = dict(parse_qsl(parsed_endpoint.query, keep_blank_values=True))
    query.update(
        {
            "url": original_url,
            "output": "json",
            "fl": "timestamp,original,statuscode,mimetype,digest",
            "collapse": "digest",
        }
    )
    # Server-side bound so long-lived URLs return a small window instead of full
    # history; client-side select_snapshot stays authoritative over the result.
    if cutoff_timestamp is not None:
        query["to"] = cutoff_timestamp
    if limit is not None:
        query["limit"] = str(limit)
    return urlunparse(parsed_endpoint._replace(query=urlencode(query)))


def parse_availability_snapshots(
    body: bytes,
    *,
    original_url: str,
    snapshot_base_url: str = DEFAULT_SNAPSHOT_BASE_URL,
) -> list[ArchiveOrgSnapshot]:
    payload = json.loads(body.decode("utf-8"))
    if isinstance(payload, list):
        return _parse_cdx_list_payload(
            payload,
            original_url=original_url,
            snapshot_base_url=snapshot_base_url,
        )
    if isinstance(payload, dict):
        return _parse_availability_dict_payload(payload, original_url=original_url)
    raise ValueError("availability metadata JSON must be a list or object")


def select_snapshot(
    snapshots: list[ArchiveOrgSnapshot],
    *,
    cutoff_timestamp: str | None = None,
) -> ArchiveOrgSnapshot | None:
    if not snapshots:
        return None
    if cutoff_timestamp is not None:
        eligible = [snapshot for snapshot in snapshots if snapshot.timestamp <= cutoff_timestamp]
        if not eligible:
            return None
        return max(eligible, key=lambda snapshot: snapshot.timestamp)
    return max(snapshots, key=lambda snapshot: snapshot.timestamp)


def _parse_cdx_list_payload(
    payload: list[object],
    *,
    original_url: str,
    snapshot_base_url: str,
) -> list[ArchiveOrgSnapshot]:
    if not payload:
        return []
    header_row = payload[0]
    if not isinstance(header_row, list):
        raise ValueError("CDX JSON first row must be a header list")
    header = [str(item) for item in header_row]
    snapshots: list[ArchiveOrgSnapshot] = []
    for row in payload[1:]:
        if not isinstance(row, list):
            raise ValueError("CDX JSON data rows must be lists")
        values = {header[index]: str(value) for index, value in enumerate(row) if index < len(header)}
        timestamp = values.get("timestamp")
        row_original_url = values.get("original") or original_url
        if not timestamp:
            continue
        _validate_wayback_timestamp(timestamp)
        snapshots.append(
            ArchiveOrgSnapshot(
                timestamp=timestamp,
                original_url=row_original_url,
                snapshot_url=_build_snapshot_url(
                    timestamp=timestamp,
                    original_url=row_original_url,
                    snapshot_base_url=snapshot_base_url,
                ),
                status_code=values.get("statuscode"),
                mime_type=values.get("mimetype"),
                digest=values.get("digest"),
            )
        )
    return snapshots


def _parse_availability_dict_payload(
    payload: dict[str, object],
    *,
    original_url: str,
) -> list[ArchiveOrgSnapshot]:
    archived_snapshots = payload.get("archived_snapshots")
    if not isinstance(archived_snapshots, dict):
        return []
    closest = archived_snapshots.get("closest")
    if not isinstance(closest, dict) or closest.get("available") is not True:
        return []
    timestamp = closest.get("timestamp")
    snapshot_url = closest.get("url")
    if not isinstance(timestamp, str) or not isinstance(snapshot_url, str):
        return []
    _validate_wayback_timestamp(timestamp)
    status = closest.get("status")
    return [
        ArchiveOrgSnapshot(
            timestamp=timestamp,
            original_url=str(payload.get("url") or original_url),
            snapshot_url=snapshot_url,
            status_code=str(status) if status is not None else None,
            mime_type=None,
            digest=None,
        )
    ]


def _validate_original_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Archive.org capture requires an absolute original http:// or https:// URL")
    return parsed.geturl()


def _validate_wayback_timestamp(timestamp: str) -> None:
    if not timestamp.isdigit() or len(timestamp) != 14:
        raise ValueError("Wayback timestamp must be a 14-digit YYYYMMDDhhmmss value")


def _build_snapshot_url(*, timestamp: str, original_url: str, snapshot_base_url: str) -> str:
    parsed_base = urlparse(snapshot_base_url)
    if parsed_base.scheme not in {"http", "https"} or not parsed_base.netloc:
        raise ValueError("Archive.org snapshot base URL requires an absolute http:// or https:// URL")
    return f"{snapshot_base_url.rstrip('/')}/{timestamp}/{original_url}"
