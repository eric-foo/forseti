from __future__ import annotations

import urllib.error
import urllib.request
from typing import Any, Iterable, Sequence

from source_capture.adapters.browser_snapshot import BrowserPageResponse


def fetch_fragrance_widget_fallback_responses(
    *,
    urls: Sequence[str],
    timeout_seconds: float,
    max_response_bytes: int,
) -> list[BrowserPageResponse]:
    responses: list[BrowserPageResponse] = []
    for url in urls:
        responses.append(
            fetch_fragrance_widget_fallback_response(
                url,
                timeout_seconds=timeout_seconds,
                max_response_bytes=max_response_bytes,
            )
        )
    return responses


def fetch_fragrance_widget_fallback_response(
    url: str,
    *,
    timeout_seconds: float,
    max_response_bytes: int,
) -> BrowserPageResponse:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (compatible; OrcaSourceCapture/0.1)",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            body_text, limitation_notes = _read_response_body_with_cap(
                response,
                max_response_bytes=max_response_bytes,
            )
            status = int(response.getcode())
            return BrowserPageResponse(
                requested_url=url,
                final_url=str(response.geturl()),
                status=status,
                ok=200 <= status < 400,
                body_text=body_text,
                response_headers=_headers_without_cookies(response.headers.items()),
                limitation_notes=limitation_notes,
            )
    except urllib.error.HTTPError as exc:
        body_text, limitation_notes = _read_response_body_with_cap(
            exc,
            max_response_bytes=max_response_bytes,
        )
        return BrowserPageResponse(
            requested_url=url,
            final_url=str(exc.geturl()),
            status=int(exc.code),
            ok=False,
            body_text=body_text,
            response_headers=_headers_without_cookies(exc.headers.items() if exc.headers else ()),
            limitation_notes=limitation_notes,
        )
    except Exception as exc:
        return BrowserPageResponse(
            requested_url=url,
            final_url=url,
            status=0,
            ok=False,
            body_text="",
            response_headers={},
            limitation_notes=[f"bounded_fallback_fetch_failed:{type(exc).__name__}:{exc}"],
        )


def _read_response_body_with_cap(response: Any, *, max_response_bytes: int) -> tuple[str, list[str]]:
    raw = response.read(max_response_bytes + 1)
    if len(raw) > max_response_bytes:
        return "", [f"bounded_fallback_response_body_exceeded_cap:{len(raw)}>{max_response_bytes}"]
    charset = response.headers.get_content_charset() if response.headers else None
    return raw.decode(charset or "utf-8", errors="replace"), []


def _headers_without_cookies(items: Iterable[tuple[str, str]]) -> dict[str, str]:
    return {
        str(key): str(value)
        for key, value in items
        if str(key).lower() not in {"set-cookie", "cookie"}
    }