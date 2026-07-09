"""Reddit API source-capture adapter (application-only, read-only public data).

Follows the adapter convention in ``docs/adapter_author_contract.md``: a free
function ``fetch_reddit_api_capture(...) -> Success | Failure`` over native inputs,
frozen result dataclasses with honest ``warning_notes`` / ``limitation_notes``,
and a Protocol transport seam so unit/contract tests inject a fake and no live
network (or OAuth) runs there. The adapter never imports the writer and never
constructs a packet — the runner translates the result into writer kwargs.

Shape: post = one captured unit (the runner maps each to a ``SourceCaptureSlice``);
comments live in that unit's verbatim ``/comments/{id}`` response. Batch-over-posts
like ``media_asset``: ``post_id`` mode = a batch of one; ``subreddit``+``listing``
mode = fetch the listing, then one ``/comments/{id}`` per post. The default
``/comments`` response is preserved verbatim (post + default-depth comment tree +
Reddit ``more`` stubs); deeper threads are NOT recursively expanded (an honest
limitation, not a relevance judgement).

SECURITY: no secret (``client_secret`` / bearer token / ``Authorization`` header)
ever appears in any result field or metadata. The bearer token lives only inside
the real client's ``get`` and is never returned. OAuth verified against Reddit's
OAuth2 docs; RE-VERIFY against current docs before relying on the real client.
"""

from __future__ import annotations

import base64
import json
import time
from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping, Protocol, Sequence, TypeAlias
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import re

from harness_utils import utc_now_z
from source_capture.reddit_credentials import RedditCredentials


DEFAULT_TIMEOUT_SECONDS = 20.0
DEFAULT_MAX_BYTES = 5_000_000
DEFAULT_LIMIT = 10
MAX_LIMIT = 25
DEFAULT_USER_AGENT = "ForsetiSourceCaptureRedditAPI/0.1 (stdlib OAuth app-only read; no praw/sdk)"
DEFAULT_TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
DEFAULT_API_BASE_URL = "https://oauth.reddit.com"
ALLOWED_LISTINGS = ("hot", "new", "top", "rising")

_SUBREDDIT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_]{0,80}$")
_POST_ID_RE = re.compile(r"^[A-Za-z0-9]{1,16}$")


class RedditApiCaptureFailureKind(StrEnum):
    AUTH_FAILED = "auth_failed"
    NETWORK_ERROR = "network_error"
    TIMEOUT = "timeout"
    ACCESS_FAILED = "access_failed"
    RATE_LIMITED = "rate_limited"
    EMPTY_RESULT = "empty_result"
    MALFORMED_RESPONSE = "malformed_response"
    SIZE_CAP_EXCEEDED = "size_cap_exceeded"


@dataclass(frozen=True)
class RedditApiResponse:
    """A completed HTTP response from the transport seam. Carries no auth material."""

    status: int
    body: bytes


class RedditApiClient(Protocol):
    """Transport seam. The real impl does OAuth + HTTP and hides the bearer token.

    ``get`` returns a ``RedditApiResponse`` for any completed HTTP request
    (including non-2xx, which the adapter maps to a failure). It raises
    ``RedditApiTransportError`` when no HTTP response could be obtained (token
    acquisition failure, network error, timeout, size-cap).
    """

    def get(self, *, path: str, params: Mapping[str, object]) -> RedditApiResponse:
        ...


class RedditApiTransportError(RuntimeError):
    def __init__(self, message: str, *, failure_kind: RedditApiCaptureFailureKind) -> None:
        super().__init__(message)
        self.failure_kind = failure_kind


@dataclass(frozen=True)
class RedditPostCapture:
    post_index: int
    post_id: str
    locator: str
    title: str | None
    created_utc: float | None
    raw_json: bytes
    metadata: dict[str, object]


@dataclass(frozen=True)
class RedditPostFailure:
    post_index: int
    post_id: str | None
    failure_kind: RedditApiCaptureFailureKind
    message: str
    status: int | None = None


@dataclass(frozen=True)
class RedditApiCaptureSuccess:
    request_descriptor: str
    mode: str
    posts: list[RedditPostCapture]
    failures: list[RedditPostFailure]
    metadata: dict[str, object]
    warning_notes: list[str]
    limitation_notes: list[str]


@dataclass(frozen=True)
class RedditApiCaptureFailure:
    request_descriptor: str
    failure_kind: RedditApiCaptureFailureKind
    message: str
    status: int | None = None


RedditApiCaptureResult: TypeAlias = RedditApiCaptureSuccess | RedditApiCaptureFailure


def fetch_reddit_api_capture(
    *,
    client: RedditApiClient,
    subreddit: str | None = None,
    listing: str | None = None,
    post_id: str | None = None,
    limit: int = DEFAULT_LIMIT,
) -> RedditApiCaptureResult:
    """Capture Reddit posts (each with its verbatim /comments response) via the seam.

    ``client`` is REQUIRED and creds-agnostic from the adapter's view: tests inject
    a fake; the runner injects the real OAuth client built from STEP-03 credentials.
    """
    mode, listing_norm = _validate_inputs(subreddit=subreddit, listing=listing, post_id=post_id, limit=limit)

    if mode == "post":
        request_descriptor = f"/comments/{post_id}"
        post_ids: list[str] = [post_id]  # type: ignore[list-item]
        listing_warnings: list[str] = []
    else:
        request_descriptor = f"/r/{subreddit}/{listing_norm}?limit={limit}"
        listing_outcome = _fetch_listing_post_ids(
            client, subreddit=subreddit, listing=listing_norm, limit=limit, request_descriptor=request_descriptor
        )
        if isinstance(listing_outcome, RedditApiCaptureFailure):
            return listing_outcome
        post_ids, listing_warnings = listing_outcome

    if not post_ids:
        return RedditApiCaptureFailure(
            request_descriptor=request_descriptor,
            failure_kind=RedditApiCaptureFailureKind.EMPTY_RESULT,
            message="reddit listing returned no usable posts to capture",
        )

    posts: list[RedditPostCapture] = []
    failures: list[RedditPostFailure] = []
    for index, pid in enumerate(post_ids, start=1):
        outcome = _fetch_post_comments(client, post_id=pid, post_index=index)
        if isinstance(outcome, RedditPostFailure):
            failures.append(outcome)
        else:
            posts.append(outcome)

    warning_notes = list(listing_warnings)
    limitation_notes: list[str] = [
        f"post_{failure.post_index:02d}_not_preserved: {failure.post_id or '?'} "
        f"{failure.failure_kind.value}: {failure.message}"
        for failure in failures
    ]
    if posts:
        limitation_notes.append(
            "reddit_api preserved each post's default /comments response (post + default-depth "
            "comment tree); deeper or collapsed comments remain as Reddit 'more' stubs and were "
            "not expanded"
        )

    metadata = {
        "mode": mode,
        "request_descriptor": request_descriptor,
        "subreddit": subreddit,
        "listing": listing_norm,
        "post_id": post_id,
        "requested_post_count": len(post_ids),
        "preserved_post_count": len(posts),
        "failed_post_count": len(failures),
        "capture_timestamp": utc_now_z(),
    }

    return RedditApiCaptureSuccess(
        request_descriptor=request_descriptor,
        mode=mode,
        posts=posts,
        failures=failures,
        metadata=metadata,
        warning_notes=warning_notes,
        limitation_notes=limitation_notes,
    )


def _validate_inputs(
    *, subreddit: str | None, listing: str | None, post_id: str | None, limit: int
) -> tuple[str, str | None]:
    if post_id is not None and subreddit is not None:
        raise ValueError("provide exactly one of post_id OR subreddit, not both")
    if post_id is None and subreddit is None:
        raise ValueError("provide exactly one of post_id OR subreddit")
    if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
        raise ValueError("limit must be a positive integer")
    if limit > MAX_LIMIT:
        raise ValueError(f"limit must be <= {MAX_LIMIT} to respect the Reddit rate budget")

    if post_id is not None:
        if not _POST_ID_RE.fullmatch(post_id):
            raise ValueError("post_id must be 1-16 letters/numbers (Reddit base-36 id)")
        return "post", None

    if not _SUBREDDIT_RE.fullmatch(subreddit):  # type: ignore[arg-type]
        raise ValueError(
            "subreddit must be 1-81 characters: letters, numbers, underscore; starting with a letter or number"
        )
    listing_norm = (listing or "hot").lower()
    if listing_norm not in ALLOWED_LISTINGS:
        raise ValueError(f"listing must be one of: {', '.join(ALLOWED_LISTINGS)}")
    return "listing", listing_norm


def _fetch_listing_post_ids(
    client: RedditApiClient,
    *,
    subreddit: str,
    listing: str,
    limit: int,
    request_descriptor: str,
) -> tuple[list[str], list[str]] | RedditApiCaptureFailure:
    try:
        response = client.get(path=f"/r/{subreddit}/{listing}", params={"limit": limit, "raw_json": 1})
    except RedditApiTransportError as exc:
        return RedditApiCaptureFailure(
            request_descriptor=request_descriptor, failure_kind=exc.failure_kind, message=str(exc)
        )

    failure = _http_status_failure(response.status, request_descriptor=request_descriptor, what="reddit listing fetch")
    if failure is not None:
        return failure

    try:
        payload = json.loads(response.body)
        children = payload["data"]["children"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return RedditApiCaptureFailure(
            request_descriptor=request_descriptor,
            failure_kind=RedditApiCaptureFailureKind.MALFORMED_RESPONSE,
            message="reddit listing response was not the expected Listing JSON shape",
        )
    if not isinstance(children, list):
        return RedditApiCaptureFailure(
            request_descriptor=request_descriptor,
            failure_kind=RedditApiCaptureFailureKind.MALFORMED_RESPONSE,
            message="reddit listing 'children' was not a list",
        )

    post_ids: list[str] = []
    warnings: list[str] = []
    for child in children:
        pid = None
        if isinstance(child, dict) and child.get("kind") == "t3":
            data = child.get("data")
            if isinstance(data, dict):
                pid = data.get("id")
        if isinstance(pid, str) and _POST_ID_RE.fullmatch(pid):
            post_ids.append(pid)
        else:
            warnings.append("reddit listing returned a child without a usable t3 post id; skipped")
    return post_ids, warnings


def _fetch_post_comments(
    client: RedditApiClient, *, post_id: str, post_index: int
) -> RedditPostCapture | RedditPostFailure:
    try:
        response = client.get(path=f"/comments/{post_id}", params={"raw_json": 1})
    except RedditApiTransportError as exc:
        return RedditPostFailure(
            post_index=post_index, post_id=post_id, failure_kind=exc.failure_kind, message=str(exc)
        )

    if response.status == 429:
        return RedditPostFailure(
            post_index=post_index,
            post_id=post_id,
            failure_kind=RedditApiCaptureFailureKind.RATE_LIMITED,
            message="reddit comments fetch was rate-limited (HTTP 429)",
            status=429,
        )
    if not 200 <= response.status < 300:
        return RedditPostFailure(
            post_index=post_index,
            post_id=post_id,
            failure_kind=RedditApiCaptureFailureKind.ACCESS_FAILED,
            message=f"reddit comments fetch returned HTTP {response.status}",
            status=response.status,
        )
    if not response.body:
        return RedditPostFailure(
            post_index=post_index,
            post_id=post_id,
            failure_kind=RedditApiCaptureFailureKind.MALFORMED_RESPONSE,
            message="reddit comments response had an empty body",
            status=response.status,
        )

    try:
        payload = json.loads(response.body)
        if not isinstance(payload, list) or len(payload) < 2:
            raise ValueError("comments response was not a 2-element [post, comments] listing")
        post_data = payload[0]["data"]["children"][0]["data"]
        resolved_id = post_data["id"]
        comments_listing = payload[1]
        if not isinstance(comments_listing, dict) or not isinstance(comments_listing.get("data"), dict):
            raise ValueError("comments response was missing the comments listing")
    except (json.JSONDecodeError, KeyError, IndexError, TypeError, ValueError):
        return RedditPostFailure(
            post_index=post_index,
            post_id=post_id,
            failure_kind=RedditApiCaptureFailureKind.MALFORMED_RESPONSE,
            message="reddit comments response was not the expected [post, comments] JSON shape",
            status=response.status,
        )
    if not isinstance(resolved_id, str) or not _POST_ID_RE.fullmatch(resolved_id) or resolved_id != post_id:
        return RedditPostFailure(
            post_index=post_index,
            post_id=post_id,
            failure_kind=RedditApiCaptureFailureKind.MALFORMED_RESPONSE,
            message="reddit comments response did not identify the requested post",
            status=response.status,
        )

    permalink = post_data.get("permalink")
    locator = (
        f"https://www.reddit.com{permalink}"
        if isinstance(permalink, str) and permalink.startswith("/")
        else f"https://www.reddit.com/comments/{resolved_id}"
    )
    metadata = {
        "post_id": resolved_id,
        "permalink": permalink if isinstance(permalink, str) else None,
        "title": post_data.get("title"),
        "created_utc": post_data.get("created_utc"),
        "subreddit": post_data.get("subreddit"),
        "num_comments": post_data.get("num_comments"),
        "comments_response_byte_count": len(response.body),
        "capture_timestamp": utc_now_z(),
    }
    return RedditPostCapture(
        post_index=post_index,
        post_id=str(resolved_id),
        locator=locator,
        title=post_data.get("title"),
        created_utc=post_data.get("created_utc"),
        raw_json=response.body,
        metadata=metadata,
    )


def _http_status_failure(
    status: int, *, request_descriptor: str, what: str
) -> RedditApiCaptureFailure | None:
    if status == 429:
        return RedditApiCaptureFailure(
            request_descriptor=request_descriptor,
            failure_kind=RedditApiCaptureFailureKind.RATE_LIMITED,
            message=f"{what} was rate-limited (HTTP 429)",
            status=429,
        )
    if not 200 <= status < 300:
        return RedditApiCaptureFailure(
            request_descriptor=request_descriptor,
            failure_kind=RedditApiCaptureFailureKind.ACCESS_FAILED,
            message=f"{what} returned HTTP {status}",
            status=status,
        )
    return None


# --- real transport (OAuth + HTTP); never exercised by unit/contract tests ---


def build_reddit_oauth_client(
    *,
    credentials: RedditCredentials,
    user_agent: str = DEFAULT_USER_AGENT,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_BYTES,
    token_url: str = DEFAULT_TOKEN_URL,
    api_base_url: str = DEFAULT_API_BASE_URL,
) -> RedditApiClient:
    """Build the real application-only OAuth client (used by the runner, not tests)."""
    return _RedditOAuthClient(
        credentials=credentials,
        user_agent=user_agent,
        timeout_seconds=timeout_seconds,
        max_bytes=max_bytes,
        token_url=token_url,
        api_base_url=api_base_url,
    )


class _RedditOAuthClient:
    """Application-only (client_credentials) OAuth client over stdlib urllib.

    Obtains and caches a 1-hour bearer token (HTTP Basic with client_id:secret at
    the token endpoint) and issues authenticated GETs to oauth.reddit.com. The
    token and credentials never leave this object.
    """

    def __init__(
        self,
        *,
        credentials: RedditCredentials,
        user_agent: str,
        timeout_seconds: float,
        max_bytes: int,
        token_url: str,
        api_base_url: str,
    ) -> None:
        self._credentials = credentials
        self._user_agent = user_agent
        self._timeout = timeout_seconds
        self._max_bytes = max_bytes
        self._token_url = token_url
        self._api_base_url = api_base_url
        self._token: str | None = None
        self._token_expiry_monotonic = 0.0

    def get(self, *, path: str, params: Mapping[str, object]) -> RedditApiResponse:
        token = self._ensure_token()
        query = urlencode({key: value for key, value in params.items()})
        url = f"{self._api_base_url}{path}"
        if query:
            url = f"{url}?{query}"
        request = Request(
            url,
            method="GET",
            headers={"Authorization": f"bearer {token}", "User-Agent": self._user_agent},
        )
        try:
            with urlopen(request, timeout=self._timeout) as response:
                return RedditApiResponse(status=int(response.getcode()), body=_read_with_cap(response, self._max_bytes))
        except HTTPError as exc:
            # Authenticated error bodies are not a safe seam surface: a server or
            # proxy could echo request headers. Preserve status only.
            return RedditApiResponse(status=int(exc.code), body=b"")
        except _BodyTooLargeError as exc:
            raise RedditApiTransportError(
                f"reddit api response exceeded the {self._max_bytes}-byte cap",
                failure_kind=RedditApiCaptureFailureKind.SIZE_CAP_EXCEEDED,
            ) from exc
        except URLError as exc:
            raise RedditApiTransportError(
                "reddit api request failed before an HTTP response was available",
                failure_kind=_transport_failure_kind(exc),
            ) from None
        except TimeoutError:
            # Read-phase timeout during _read_with_cap()/response.read() after urlopen returned:
            # not a URLError, previously uncaught -> escaped get() and violated the transport
            # contract (get must raise RedditApiTransportError, never a raw socket error).
            raise RedditApiTransportError(
                "reddit api response read timed out before completion",
                failure_kind=RedditApiCaptureFailureKind.TIMEOUT,
            ) from None
        except OSError:
            # Other read-phase socket errors (connection reset, etc.) likewise fire after urlopen
            # and are not URLError; surface as the transport error callers rely on, not a crash.
            raise RedditApiTransportError(
                "reddit api response read failed before completion",
                failure_kind=RedditApiCaptureFailureKind.NETWORK_ERROR,
            ) from None

    def _ensure_token(self) -> str:
        now = time.monotonic()
        if self._token is not None and now < self._token_expiry_monotonic:
            return self._token

        basic = base64.b64encode(
            f"{self._credentials.client_id}:{self._credentials.client_secret}".encode("utf-8")
        ).decode("ascii")
        body = urlencode({"grant_type": "client_credentials"}).encode("utf-8")
        request = Request(
            self._token_url,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Basic {basic}",
                "User-Agent": self._user_agent,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        try:
            with urlopen(request, timeout=self._timeout) as response:
                payload = json.loads(_read_with_cap(response, self._max_bytes))
        except (json.JSONDecodeError, TypeError, UnicodeDecodeError):
            raise RedditApiTransportError(
                "reddit token response was not valid JSON",
                failure_kind=RedditApiCaptureFailureKind.AUTH_FAILED,
            ) from None
        except HTTPError as exc:
            # Sever the cause chain (finding #1): the raw HTTPError can hold an
            # echoed Basic header / client_secret in its body; do not retain it on
            # the raised transport error. Matches the from None used by the sibling
            # handlers in this method. Only the non-secret status escapes.
            raise RedditApiTransportError(
                f"reddit token request failed: HTTP {exc.code}",
                failure_kind=RedditApiCaptureFailureKind.AUTH_FAILED,
            ) from None
        except _BodyTooLargeError as exc:
            raise RedditApiTransportError(
                "reddit token response exceeded the size cap",
                failure_kind=RedditApiCaptureFailureKind.AUTH_FAILED,
            ) from exc
        except URLError as exc:
            raise RedditApiTransportError(
                "reddit token request failed before a token response was available",
                failure_kind=_transport_failure_kind(exc),
            ) from None
        except TimeoutError:
            raise RedditApiTransportError(
                "reddit token response read timed out before completion",
                failure_kind=RedditApiCaptureFailureKind.TIMEOUT,
            ) from None
        except OSError:
            raise RedditApiTransportError(
                "reddit token response read failed before completion",
                failure_kind=RedditApiCaptureFailureKind.NETWORK_ERROR,
            ) from None

        access_token = payload.get("access_token") if isinstance(payload, dict) else None
        if not isinstance(access_token, str) or not access_token:
            raise RedditApiTransportError(
                "reddit token response did not contain an access_token",
                failure_kind=RedditApiCaptureFailureKind.AUTH_FAILED,
            )
        expires_in = payload.get("expires_in", 3600)
        try:
            ttl = float(expires_in)
        except (TypeError, ValueError):
            ttl = 3600.0
        self._token = access_token
        self._token_expiry_monotonic = now + max(0.0, ttl - 60.0)
        return access_token


def _transport_failure_kind(error: URLError) -> RedditApiCaptureFailureKind:
    reason = str(error.reason).lower()
    if "timed out" in reason or "timeout" in reason:
        return RedditApiCaptureFailureKind.TIMEOUT
    return RedditApiCaptureFailureKind.NETWORK_ERROR


def _read_with_cap(response: object, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(65536, max_bytes - total + 1))  # type: ignore[attr-defined]
        if not chunk:
            return b"".join(chunks)
        total += len(chunk)
        if total > max_bytes:
            raise _BodyTooLargeError(f"response exceeded the {max_bytes}-byte cap during read")
        chunks.append(chunk)


class _BodyTooLargeError(ValueError):
    pass


__all__ = [
    "ALLOWED_LISTINGS",
    "DEFAULT_LIMIT",
    "DEFAULT_USER_AGENT",
    "MAX_LIMIT",
    "RedditApiCaptureFailure",
    "RedditApiCaptureFailureKind",
    "RedditApiCaptureResult",
    "RedditApiCaptureSuccess",
    "RedditApiClient",
    "RedditApiResponse",
    "RedditApiTransportError",
    "RedditPostCapture",
    "RedditPostFailure",
    "build_reddit_oauth_client",
    "fetch_reddit_api_capture",
]
