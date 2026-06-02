from __future__ import annotations

import json
from dataclasses import dataclass
from json import JSONDecodeError
from typing import TypeAlias
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from source_capture.adapters.direct_http import (
    DEFAULT_MAX_BYTES,
    DEFAULT_TIMEOUT_SECONDS,
    DirectHttpCaptureFailure,
    DirectHttpCaptureSuccess,
    fetch_direct_http_capture,
)


DEFAULT_CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"
DEFAULT_SNAPSHOT_BASE_URL = "https://web.archive.org/web"


@dataclass(frozen=True)
class ArchiveOrgSnapshot:
    timestamp: str
    original_url: str
    snapshot_url: str
    status_code: str | None
    mime_type: str | None
    digest: str | None


@dataclass(frozen=True)
class ArchiveOrgCaptureSuccess:
    original_url: str
    availability_url: str
    availability_result: DirectHttpCaptureSuccess
    snapshots: list[ArchiveOrgSnapshot]
    selected_snapshot: ArchiveOrgSnapshot | None
    body_result: DirectHttpCaptureSuccess | DirectHttpCaptureFailure | None
    parse_warning: str | None = None


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
) -> ArchiveOrgCaptureResult:
    normalized_original_url = _validate_original_url(original_url)
    if cutoff_timestamp is not None:
        _validate_wayback_timestamp(cutoff_timestamp)

    availability_url = build_cdx_availability_url(
        original_url=normalized_original_url,
        cdx_endpoint=cdx_endpoint,
    )
    availability_result = fetch_direct_http_capture(
        url=availability_url,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
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
    if selected_snapshot is not None:
        body_result = fetch_direct_http_capture(
            url=selected_snapshot.snapshot_url,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
        )

    return ArchiveOrgCaptureSuccess(
        original_url=normalized_original_url,
        availability_url=availability_url,
        availability_result=availability_result,
        snapshots=snapshots,
        selected_snapshot=selected_snapshot,
        body_result=body_result,
        parse_warning=parse_warning,
    )


def build_cdx_availability_url(*, original_url: str, cdx_endpoint: str = DEFAULT_CDX_ENDPOINT) -> str:
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
