from __future__ import annotations

import io
import json
from urllib.error import HTTPError, URLError

import pytest

import source_capture.adapters.reddit_api as reddit_api
from source_capture.adapters.reddit_api import (
    DEFAULT_TOKEN_URL,
    MAX_LIMIT,
    RedditApiCaptureFailure,
    RedditApiCaptureFailureKind,
    RedditApiCaptureSuccess,
    RedditApiResponse,
    RedditApiTransportError,
    build_reddit_oauth_client,
    fetch_reddit_api_capture,
)
from source_capture.reddit_credentials import RedditCredentialMode, RedditCredentials


# --- canned Reddit JSON + a fake transport seam (no network) ---


def _listing_bytes(post_ids: list[str]) -> bytes:
    return json.dumps(
        {"kind": "Listing", "data": {"children": [{"kind": "t3", "data": {"id": pid}} for pid in post_ids]}}
    ).encode("utf-8")


def _comments_bytes(post_id: str, *, subreddit: str = "testsub", title: str = "A title") -> bytes:
    permalink = f"/r/{subreddit}/comments/{post_id}/a_title/"
    post_listing = {
        "kind": "Listing",
        "data": {
            "children": [
                {
                    "kind": "t3",
                    "data": {
                        "id": post_id,
                        "title": title,
                        "permalink": permalink,
                        "created_utc": 1700000000.0,
                        "subreddit": subreddit,
                        "num_comments": 2,
                    },
                }
            ]
        },
    }
    comments_listing = {
        "kind": "Listing",
        "data": {
            "children": [
                {"kind": "t1", "data": {"id": "c1", "body": "first comment"}},
                {"kind": "more", "data": {"count": 5, "children": ["c2", "c3"]}},
            ]
        },
    }
    return json.dumps([post_listing, comments_listing]).encode("utf-8")


class _FakeRedditApiClient:
    def __init__(self, responses: dict[str, RedditApiResponse], *, raise_on: dict[str, Exception] | None = None) -> None:
        self._responses = responses
        self._raise_on = raise_on or {}
        self.calls: list[tuple[str, dict]] = []

    def get(self, *, path: str, params) -> RedditApiResponse:
        self.calls.append((path, dict(params)))
        if path in self._raise_on:
            raise self._raise_on[path]
        return self._responses.get(path, RedditApiResponse(status=404, body=b'{"message": "not found"}'))


def _ok(body: bytes) -> RedditApiResponse:
    return RedditApiResponse(status=200, body=body)


def test_post_id_mode_captures_one_post_with_verbatim_comments() -> None:
    comments = _comments_bytes("abc123")
    client = _FakeRedditApiClient({"/comments/abc123": _ok(comments)})

    result = fetch_reddit_api_capture(client=client, post_id="abc123")

    assert isinstance(result, RedditApiCaptureSuccess)
    assert result.mode == "post"
    assert [p.post_id for p in result.posts] == ["abc123"]
    assert result.failures == []
    post = result.posts[0]
    assert post.raw_json == comments  # verbatim
    assert b"first comment" in post.raw_json and b"more" in post.raw_json  # comments + 'more' stub preserved
    assert post.locator == "https://www.reddit.com/r/testsub/comments/abc123/a_title/"
    assert post.title == "A title"
    assert result.metadata["preserved_post_count"] == 1
    assert client.calls == [("/comments/abc123", {"raw_json": 1})]


def test_listing_mode_captures_each_post_with_comments() -> None:
    client = _FakeRedditApiClient(
        {
            "/r/testsub/hot": _ok(_listing_bytes(["p1", "p2"])),
            "/comments/p1": _ok(_comments_bytes("p1")),
            "/comments/p2": _ok(_comments_bytes("p2")),
        }
    )

    result = fetch_reddit_api_capture(client=client, subreddit="testsub", listing="hot", limit=5)

    assert isinstance(result, RedditApiCaptureSuccess)
    assert result.mode == "listing"
    assert [p.post_id for p in result.posts] == ["p1", "p2"]
    assert result.failures == []
    assert ("/r/testsub/hot", {"limit": 5, "raw_json": 1}) in client.calls
    assert result.metadata["preserved_post_count"] == 2


def test_partial_failure_surfaces_failed_post_without_aborting() -> None:
    client = _FakeRedditApiClient(
        {
            "/r/testsub/hot": _ok(_listing_bytes(["p1", "p2"])),
            "/comments/p1": _ok(_comments_bytes("p1")),
            "/comments/p2": RedditApiResponse(status=404, body=b'{"message": "not found"}'),
        }
    )

    result = fetch_reddit_api_capture(client=client, subreddit="testsub", listing="hot")

    assert isinstance(result, RedditApiCaptureSuccess)
    assert [p.post_id for p in result.posts] == ["p1"]
    assert len(result.failures) == 1
    failure = result.failures[0]
    assert failure.post_id == "p2"
    assert failure.failure_kind == RedditApiCaptureFailureKind.ACCESS_FAILED
    assert failure.status == 404
    assert any("post_02_not_preserved" in note and "p2" in note for note in result.limitation_notes)


def test_listing_fetch_failure_returns_top_level_failure() -> None:
    client = _FakeRedditApiClient({"/r/private/hot": RedditApiResponse(status=403, body=b"forbidden")})
    result = fetch_reddit_api_capture(client=client, subreddit="private", listing="hot")
    assert isinstance(result, RedditApiCaptureFailure)
    assert result.failure_kind == RedditApiCaptureFailureKind.ACCESS_FAILED
    assert result.status == 403


def test_rate_limited_listing_returns_failure() -> None:
    client = _FakeRedditApiClient({"/r/testsub/hot": RedditApiResponse(status=429, body=b"")})
    result = fetch_reddit_api_capture(client=client, subreddit="testsub", listing="hot")
    assert isinstance(result, RedditApiCaptureFailure)
    assert result.failure_kind == RedditApiCaptureFailureKind.RATE_LIMITED


def test_empty_listing_returns_failure() -> None:
    client = _FakeRedditApiClient({"/r/testsub/hot": _ok(_listing_bytes([]))})
    result = fetch_reddit_api_capture(client=client, subreddit="testsub", listing="hot")
    assert isinstance(result, RedditApiCaptureFailure)
    assert result.failure_kind == RedditApiCaptureFailureKind.EMPTY_RESULT


def test_transport_error_on_listing_maps_to_failure_kind() -> None:
    client = _FakeRedditApiClient(
        {},
        raise_on={
            "/r/testsub/hot": RedditApiTransportError(
                "network down", failure_kind=RedditApiCaptureFailureKind.NETWORK_ERROR
            )
        },
    )
    result = fetch_reddit_api_capture(client=client, subreddit="testsub", listing="hot")
    assert isinstance(result, RedditApiCaptureFailure)
    assert result.failure_kind == RedditApiCaptureFailureKind.NETWORK_ERROR


def test_malformed_comments_response_is_a_post_failure() -> None:
    client = _FakeRedditApiClient(
        {
            "/r/testsub/hot": _ok(_listing_bytes(["p1"])),
            "/comments/p1": _ok(b'{"not": "the expected shape"}'),
        }
    )
    result = fetch_reddit_api_capture(client=client, subreddit="testsub", listing="hot")
    assert isinstance(result, RedditApiCaptureSuccess)
    assert result.posts == []
    assert result.failures[0].failure_kind == RedditApiCaptureFailureKind.MALFORMED_RESPONSE


@pytest.mark.parametrize("bad_id", [{"not": "a string"}, "different"])
def test_comments_response_must_identify_requested_post(bad_id) -> None:  # noqa: ANN001
    post_listing = {"kind": "Listing", "data": {"children": [{"kind": "t3", "data": {"id": bad_id}}]}}
    client = _FakeRedditApiClient({"/comments/abc123": _ok(json.dumps([post_listing]).encode("utf-8"))})

    result = fetch_reddit_api_capture(client=client, post_id="abc123")

    assert isinstance(result, RedditApiCaptureSuccess)
    assert result.posts == []
    assert result.failures[0].failure_kind == RedditApiCaptureFailureKind.MALFORMED_RESPONSE


def test_input_validation() -> None:
    client = _FakeRedditApiClient({})
    with pytest.raises(ValueError, match="exactly one"):
        fetch_reddit_api_capture(client=client, post_id="abc", subreddit="x")
    with pytest.raises(ValueError, match="exactly one"):
        fetch_reddit_api_capture(client=client)
    with pytest.raises(ValueError, match="positive integer"):
        fetch_reddit_api_capture(client=client, subreddit="x", limit=0)
    with pytest.raises(ValueError, match=f"<= {MAX_LIMIT}"):
        fetch_reddit_api_capture(client=client, subreddit="x", limit=MAX_LIMIT + 1)
    with pytest.raises(ValueError, match="subreddit must be"):
        fetch_reddit_api_capture(client=client, subreddit="bad/sub")
    with pytest.raises(ValueError, match="post_id must be"):
        fetch_reddit_api_capture(client=client, post_id="bad/id")
    with pytest.raises(ValueError, match="listing must be"):
        fetch_reddit_api_capture(client=client, subreddit="x", listing="worst")


def test_no_auth_material_in_adapter_controlled_fields() -> None:
    client = _FakeRedditApiClient({"/comments/abc123": _ok(_comments_bytes("abc123"))})
    result = fetch_reddit_api_capture(client=client, post_id="abc123")
    assert isinstance(result, RedditApiCaptureSuccess)
    # Scan only adapter-CONTROLLED text (not the verbatim raw_json, which is public content).
    controlled = json.dumps(result.metadata) + result.request_descriptor + "".join(
        result.warning_notes + result.limitation_notes
    )
    for post in result.posts:
        controlled += json.dumps(post.metadata) + post.locator
    lowered = controlled.lower()
    for forbidden in ("authorization", "bearer", "client_secret", "access_token"):
        assert forbidden not in lowered


# --- real OAuth client wiring, proven offline with a fake urlopen ---


class _FakeHttpResponse:
    def __init__(self, status: int, body: bytes) -> None:
        self._status = status
        self._body = body
        self._served = False

    def __enter__(self) -> "_FakeHttpResponse":
        return self

    def __exit__(self, *exc: object) -> bool:
        return False

    def getcode(self) -> int:
        return self._status

    def read(self, _n: int = -1) -> bytes:
        if self._served:
            return b""
        self._served = True
        return self._body


def test_real_oauth_client_sends_basic_then_bearer_and_returns_only_status_body(monkeypatch) -> None:
    recorded: list[object] = []

    def fake_urlopen(request, timeout=None):  # noqa: ANN001
        recorded.append(request)
        if request.full_url == DEFAULT_TOKEN_URL:
            return _FakeHttpResponse(200, json.dumps({"access_token": "TESTTOKEN", "expires_in": 3600}).encode("utf-8"))
        return _FakeHttpResponse(200, _listing_bytes(["p1"]))

    monkeypatch.setattr(reddit_api, "urlopen", fake_urlopen)

    client = build_reddit_oauth_client(
        credentials=RedditCredentials(
            client_id="public-app-id",
            client_secret="SUPER_SECRET_VALUE",
            credential_mode=RedditCredentialMode.OWNER_REGISTERED_SCRIPT_APP,
        )
    )
    response = client.get(path="/r/x/hot", params={"limit": 5})

    # token request: Basic auth + client_credentials grant at the token endpoint
    token_request = recorded[0]
    assert token_request.full_url == DEFAULT_TOKEN_URL
    assert token_request.get_method() == "POST"
    assert (token_request.get_header("Authorization") or "").startswith("Basic ")
    assert token_request.data == b"grant_type=client_credentials"

    # api request: bearer token to oauth.reddit.com with a descriptive UA
    api_request = recorded[1]
    assert api_request.full_url.startswith("https://oauth.reddit.com/r/x/hot")
    assert api_request.get_header("Authorization") == "bearer TESTTOKEN"
    assert "Orca" in (api_request.get_header("User-agent") or "")

    # the seam returns ONLY status + body — no token/secret leaks back to the adapter
    assert isinstance(response, RedditApiResponse)
    assert response.status == 200 and response.body == _listing_bytes(["p1"])
    assert "SUPER_SECRET_VALUE" not in repr(response)
    assert "TESTTOKEN" not in repr(response)


def test_real_oauth_client_does_not_return_authenticated_http_error_body(monkeypatch) -> None:
    def fake_urlopen(request, timeout=None):  # noqa: ANN001
        if request.full_url == DEFAULT_TOKEN_URL:
            return _FakeHttpResponse(200, json.dumps({"access_token": "TESTTOKEN", "expires_in": 3600}).encode("utf-8"))
        raise HTTPError(
            request.full_url,
            500,
            "server error",
            hdrs={},
            fp=io.BytesIO(b"Authorization: bearer TESTTOKEN; client_secret=SUPER_SECRET_VALUE"),
        )

    monkeypatch.setattr(reddit_api, "urlopen", fake_urlopen)

    client = build_reddit_oauth_client(
        credentials=RedditCredentials(
            client_id="public-app-id",
            client_secret="SUPER_SECRET_VALUE",
            credential_mode=RedditCredentialMode.OWNER_REGISTERED_SCRIPT_APP,
        )
    )

    response = client.get(path="/r/x/hot", params={"limit": 5})

    assert response.status == 500
    assert response.body == b""
    assert "TESTTOKEN" not in repr(response)
    assert "SUPER_SECRET_VALUE" not in repr(response)


def test_real_oauth_client_redacts_api_transport_error_reason(monkeypatch) -> None:
    def fake_urlopen(request, timeout=None):  # noqa: ANN001
        if request.full_url == DEFAULT_TOKEN_URL:
            return _FakeHttpResponse(200, json.dumps({"access_token": "TESTTOKEN", "expires_in": 3600}).encode("utf-8"))
        raise URLError("transport failed with bearer TESTTOKEN and SUPER_SECRET_VALUE")

    monkeypatch.setattr(reddit_api, "urlopen", fake_urlopen)

    client = build_reddit_oauth_client(
        credentials=RedditCredentials(
            client_id="public-app-id",
            client_secret="SUPER_SECRET_VALUE",
            credential_mode=RedditCredentialMode.OWNER_REGISTERED_SCRIPT_APP,
        )
    )

    result = fetch_reddit_api_capture(client=client, subreddit="x")

    assert isinstance(result, RedditApiCaptureFailure)
    assert result.failure_kind == RedditApiCaptureFailureKind.NETWORK_ERROR
    assert "TESTTOKEN" not in result.message
    assert "SUPER_SECRET_VALUE" not in result.message


def test_malformed_token_json_maps_to_auth_failure(monkeypatch) -> None:
    def fake_urlopen(request, timeout=None):  # noqa: ANN001
        return _FakeHttpResponse(200, b"not-json")

    monkeypatch.setattr(reddit_api, "urlopen", fake_urlopen)

    client = build_reddit_oauth_client(
        credentials=RedditCredentials(
            client_id="public-app-id",
            client_secret="SUPER_SECRET_VALUE",
            credential_mode=RedditCredentialMode.OWNER_REGISTERED_SCRIPT_APP,
        )
    )

    with pytest.raises(RedditApiTransportError) as excinfo:
        client.get(path="/r/x/hot", params={"limit": 5})

    assert excinfo.value.failure_kind == RedditApiCaptureFailureKind.AUTH_FAILED
    assert str(excinfo.value) == "reddit token response was not valid JSON"
    assert "SUPER_SECRET_VALUE" not in str(excinfo.value)
