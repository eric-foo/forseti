"""IG creator-momentum JSON harvest helpers.

This module is the IG-specific satellite around the generic browser-context
response-body adapter. It parses profile-feed JSON into metric facts without
treating absent fields as observed zeroes.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable
from urllib.parse import quote, urlencode, urlparse

from source_capture.adapters.browser_snapshot import (
    BrowserContextRequest,
    BrowserContextResponsesResult,
    BrowserContextResponsesSuccess,
    BrowserSnapshotFailure,
    fetch_browser_context_responses,
)

IG_WEB_APP_ID = "936619743392459"
IG_GRID_DOC_ID = "7950326061742207"
IG_METRIC_REGISTRY_VERSION = "ig_creator_momentum_metrics_v0"
IG_ID_CONFLICT_POLICY_VERSION = "ig_numeric_id_username_policy_v0"


@dataclass(frozen=True)
class IgMomentumResponseRecord:
    request_id: str
    requested_url: str
    final_url: str | None
    status: int | None
    ok: bool
    body_text: str
    failure_message: str | None = None


@dataclass(frozen=True)
class IgMediaMetricRecord:
    shortcode: str
    is_video: bool | None
    video_view_count: int | None
    like_count: int | None
    comment_count: int | None
    caption: str | None
    taken_at_timestamp: int | None


@dataclass(frozen=True)
class IgProfileMomentumCapture:
    username: str
    numeric_id: str | None
    follower_count: int | None
    media_by_shortcode: dict[str, IgMediaMetricRecord]
    raw_responses: list[IgMomentumResponseRecord]
    warning_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)

    def to_staged_payload(self) -> dict[str, object]:
        return {
            "username": self.username,
            "numeric_id": self.numeric_id,
            "follower_count": self.follower_count,
            "metric_registry_version": IG_METRIC_REGISTRY_VERSION,
            "identity_conflict_policy_version": IG_ID_CONFLICT_POLICY_VERSION,
            "media": {
                shortcode: {
                    "shortcode": item.shortcode,
                    "is_video": item.is_video,
                    "video_view_count": item.video_view_count,
                    "like_count": item.like_count,
                    "comment_count": item.comment_count,
                    "caption": item.caption,
                    "taken_at_timestamp": item.taken_at_timestamp,
                }
                for shortcode, item in sorted(self.media_by_shortcode.items())
            },
            "responses": [
                {
                    "request_id": response.request_id,
                    "requested_url": response.requested_url,
                    "final_url": response.final_url,
                    "status": response.status,
                    "ok": response.ok,
                    "body_text": response.body_text,
                    "failure_message": response.failure_message,
                }
                for response in self.raw_responses
            ],
            "warning_notes": self.warning_notes,
            "limitation_notes": self.limitation_notes,
        }


def extract_ig_username(profile_url: str) -> str | None:
    path_parts = [part for part in urlparse(profile_url).path.split("/") if part]
    return path_parts[0] if path_parts else None


def extract_ig_shortcode(url: str) -> str | None:
    path_parts = [part for part in urlparse(url).path.split("/") if part]
    for index, part in enumerate(path_parts):
        if part in {"p", "reel"} and index + 1 < len(path_parts):
            return path_parts[index + 1]
    return None


def fetch_ig_profile_momentum(
    *,
    profile_url: str,
    max_media: int,
    max_graphql_pages: int = 1,
    request_gap_seconds: float = 3.0,
    timeout_seconds: float = 20.0,
    max_response_bytes: int = 5_000_000,
    storage_state_path: Path | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
    browser_fetcher: Callable[..., BrowserContextResponsesResult] = fetch_browser_context_responses,
) -> IgProfileMomentumCapture:
    if max_media <= 0:
        raise ValueError("max_media must be greater than zero")
    if max_graphql_pages < 0:
        raise ValueError("max_graphql_pages must be zero or greater")
    if request_gap_seconds < 2.5:
        raise ValueError("request_gap_seconds must be at least 2.5 seconds for IG browser-context requests")
    username = extract_ig_username(profile_url)
    if not username:
        raise ValueError("profile_url must contain an IG username path")

    raw_responses: list[IgMomentumResponseRecord] = []
    warnings: list[str] = []
    limitations: list[str] = []
    media_by_shortcode: dict[str, IgMediaMetricRecord] = {}
    numeric_id: str | None = None
    follower_count: int | None = None
    next_cursor: str | None = None

    web_result = browser_fetcher(
        page_url=profile_url,
        requests=[
            BrowserContextRequest(
                request_id="web_profile_info",
                url=_web_profile_info_url(username),
                headers=_ig_json_headers(),
            )
        ],
        timeout_seconds=timeout_seconds,
        wait_until="load",
        max_response_bytes=max_response_bytes,
        storage_state_path=storage_state_path,
    )
    web_records = _records_from_fetch_result(web_result)
    raw_responses.extend(web_records)
    web_response = web_records[0]
    if web_response.status == 200:
        try:
            profile_payload = json.loads(web_response.body_text)
        except json.JSONDecodeError as exc:
            limitations.append(f"web_profile_info_invalid_json: {exc}")
        else:
            profile = _parse_profile_payload(profile_payload)
            numeric_id = profile.numeric_id
            follower_count = profile.follower_count
            media_by_shortcode.update(profile.media_by_shortcode)
            next_cursor = profile.next_cursor
            warnings.extend(profile.warning_notes)
            limitations.extend(profile.limitation_notes)
    else:
        limitations.append(
            f"web_profile_info_unavailable: status={web_response.status} failure={web_response.failure_message}"
        )

    graphql_pages = 0
    while numeric_id and next_cursor and graphql_pages < max_graphql_pages:
        if graphql_pages > 0 or media_by_shortcode:
            sleep_fn(request_gap_seconds)
        request_id = f"graphql_grid_{graphql_pages + 1:02d}"
        graph_result = browser_fetcher(
            page_url=profile_url,
            requests=[
                BrowserContextRequest(
                    request_id=request_id,
                    url=_graphql_grid_url(numeric_id=numeric_id, after=next_cursor, first=max(12, max_media)),
                    headers=_ig_json_headers(),
                )
            ],
            timeout_seconds=timeout_seconds,
            wait_until="load",
            max_response_bytes=max_response_bytes,
            storage_state_path=storage_state_path,
        )
        graph_records = _records_from_fetch_result(graph_result)
        raw_responses.extend(graph_records)
        graph_response = graph_records[0]
        graphql_pages += 1
        if graph_response.status != 200:
            limitations.append(
                f"{request_id}_unavailable: status={graph_response.status} failure={graph_response.failure_message}"
            )
            break
        try:
            graph_payload = json.loads(graph_response.body_text)
        except json.JSONDecodeError as exc:
            limitations.append(f"{request_id}_invalid_json: {exc}")
            break
        parsed = _parse_media_payload(graph_payload)
        media_by_shortcode.update(parsed.media_by_shortcode)
        next_cursor = parsed.next_cursor
        warnings.extend(parsed.warning_notes)
        limitations.extend(parsed.limitation_notes)
        if len(media_by_shortcode) >= max_media and graphql_pages >= 1:
            break

    return IgProfileMomentumCapture(
        username=username,
        numeric_id=numeric_id,
        follower_count=follower_count,
        media_by_shortcode=media_by_shortcode,
        raw_responses=raw_responses,
        warning_notes=warnings,
        limitation_notes=limitations,
    )


@dataclass(frozen=True)
class _ParsedPayload:
    numeric_id: str | None
    follower_count: int | None
    media_by_shortcode: dict[str, IgMediaMetricRecord]
    next_cursor: str | None
    warning_notes: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)


def _records_from_fetch_result(result: BrowserContextResponsesResult) -> list[IgMomentumResponseRecord]:
    if isinstance(result, BrowserSnapshotFailure):
        return [
            IgMomentumResponseRecord(
                request_id="browser_context_failure",
                requested_url=result.requested_url,
                final_url=result.final_url,
                status=None,
                ok=False,
                body_text="",
                failure_message=result.message,
            )
        ]
    if not isinstance(result, BrowserContextResponsesSuccess):
        raise TypeError(f"unexpected browser response result: {type(result)!r}")
    if not result.responses:
        return [
            IgMomentumResponseRecord(
                request_id="browser_context_empty_response",
                requested_url=result.page_url,
                final_url=result.final_page_url,
                status=None,
                ok=False,
                body_text="",
                failure_message="browser context response capture returned no responses",
            )
        ]
    return [
        IgMomentumResponseRecord(
            request_id=response.request_id,
            requested_url=response.requested_url,
            final_url=response.final_url,
            status=response.status,
            ok=response.ok,
            body_text=response.body_text,
        )
        for response in result.responses
    ]


def _parse_profile_payload(payload: object) -> _ParsedPayload:
    data = payload.get("data") if isinstance(payload, dict) else None
    user = data.get("user") if isinstance(data, dict) else None
    if not isinstance(user, dict):
        return _ParsedPayload(
            numeric_id=None,
            follower_count=None,
            media_by_shortcode={},
            next_cursor=None,
            limitation_notes=["web_profile_info_missing_data_user"],
        )
    parsed_media = _parse_media_payload(user)
    return _ParsedPayload(
        numeric_id=_string_or_none(user.get("id")),
        follower_count=_edge_count(user.get("edge_followed_by")),
        media_by_shortcode=parsed_media.media_by_shortcode,
        next_cursor=parsed_media.next_cursor,
        warning_notes=parsed_media.warning_notes,
        limitation_notes=parsed_media.limitation_notes,
    )


def _parse_media_payload(payload: object) -> _ParsedPayload:
    media: dict[str, IgMediaMetricRecord] = {}
    next_cursor: str | None = None
    containers = list(_iter_timeline_containers(payload))
    if not containers:
        return _ParsedPayload(
            numeric_id=None,
            follower_count=None,
            media_by_shortcode={},
            next_cursor=None,
            limitation_notes=["timeline_media_container_not_found"],
        )
    for container in containers:
        for edge in container.get("edges", []):
            node = edge.get("node") if isinstance(edge, dict) else None
            if not isinstance(node, dict):
                continue
            record = _parse_media_node(node)
            if record is not None:
                media[record.shortcode] = record
        page_info = container.get("page_info")
        if isinstance(page_info, dict) and page_info.get("has_next_page"):
            next_cursor = _string_or_none(page_info.get("end_cursor"))
    return _ParsedPayload(
        numeric_id=None,
        follower_count=None,
        media_by_shortcode=media,
        next_cursor=next_cursor,
    )


def _iter_timeline_containers(value: object) -> Iterable[dict[str, object]]:
    if isinstance(value, dict):
        edges = value.get("edges")
        page_info = value.get("page_info")
        if isinstance(edges, list) and isinstance(page_info, dict):
            if any(_edge_has_shortcode(edge) for edge in edges):
                yield value
        for child in value.values():
            yield from _iter_timeline_containers(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_timeline_containers(child)


def _edge_has_shortcode(edge: object) -> bool:
    node = edge.get("node") if isinstance(edge, dict) else None
    return isinstance(node, dict) and _string_or_none(node.get("shortcode")) is not None


def _parse_media_node(node: dict[str, object]) -> IgMediaMetricRecord | None:
    shortcode = _string_or_none(node.get("shortcode"))
    if not shortcode:
        return None
    return IgMediaMetricRecord(
        shortcode=shortcode,
        is_video=node.get("is_video") if isinstance(node.get("is_video"), bool) else None,
        video_view_count=_first_int(node, ("video_view_count", "play_count", "view_count")),
        like_count=_first_edge_count(node, ("edge_liked_by", "edge_media_preview_like")),
        comment_count=_edge_count(node.get("edge_media_to_comment")),
        caption=_caption_text(node.get("edge_media_to_caption")),
        taken_at_timestamp=_int_or_none(node.get("taken_at_timestamp")),
    )


def _web_profile_info_url(username: str) -> str:
    return f"https://www.instagram.com/api/v1/users/web_profile_info/?username={quote(username)}"


def _graphql_grid_url(*, numeric_id: str, after: str, first: int) -> str:
    variables = json.dumps({"id": numeric_id, "first": first, "after": after}, separators=(",", ":"))
    return "https://www.instagram.com/graphql/query/?" + urlencode(
        {"doc_id": IG_GRID_DOC_ID, "variables": variables}
    )


def _ig_json_headers() -> dict[str, str]:
    return {
        "Accept": "application/json",
        "X-IG-App-ID": IG_WEB_APP_ID,
    }


def _edge_count(value: object) -> int | None:
    if isinstance(value, dict):
        return _int_or_none(value.get("count"))
    return None


def _first_edge_count(container: dict[str, object], keys: tuple[str, ...]) -> int | None:
    for key in keys:
        parsed = _edge_count(container.get(key))
        if parsed is not None:
            return parsed
    return None


def _caption_text(value: object) -> str | None:
    if not isinstance(value, dict):
        return None
    edges = value.get("edges")
    if not isinstance(edges, list) or not edges:
        return None
    first = edges[0]
    node = first.get("node") if isinstance(first, dict) else None
    if isinstance(node, dict):
        return _string_or_none(node.get("text"))
    return None


def _first_int(container: dict[str, object], keys: tuple[str, ...]) -> int | None:
    for key in keys:
        if key in container:
            parsed = _int_or_none(container.get(key))
            if parsed is not None:
                return parsed
    return None


def _int_or_none(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        stripped = value.replace(",", "").strip()
        return int(stripped) if stripped.isdigit() else None
    return None


def _string_or_none(value: object) -> str | None:
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    if isinstance(value, int):
        return str(value)
    return None
