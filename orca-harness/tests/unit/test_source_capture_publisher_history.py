from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import pytest

from source_capture.adapters.direct_http import DirectHttpCaptureFailure, DirectHttpCaptureSuccess
from source_capture.adapters.publisher_history import (
    PublisherHistoryCaptureFailure,
    PublisherHistoryCaptureSuccess,
    build_github_history_url,
    build_mediawiki_history_url,
    fetch_github_history_capture,
    fetch_mediawiki_history_capture,
)


# --------------------------------------------------------------------------------------------------
# Loopback fixture (no live network). One server serves both rungs:
#   - MediaWiki listing:  GET /w/api.php?...rvprop=timestamp|ids...   -> revisions list <= cutoff
#   - MediaWiki content:  GET /w/api.php?...rvprop=content|...&rvstartid=<revid> -> revision body
#   - GitHub listing:     GET /repos/<owner>/<repo>/commits?...until=<cutoff>... -> commits list
#   - GitHub raw body:    GET /<owner>/<repo>/<sha>/<path>            -> file bytes at that sha
# Each fixed title/path encodes one scenario (with-body / no-pre-cutoff / body-fails / post-cutoff).
# --------------------------------------------------------------------------------------------------


def _mediawiki_listing(revisions: list[dict]) -> dict:
    return {"query": {"pages": [{"pageid": 1, "title": "T", "revisions": revisions}]}}


_MEDIAWIKI_LISTINGS = {
    # Title -> the revision the API would return as newest <= cutoff (rvlimit=1). The server honors
    # rvstart by filtering, so a post-cutoff revision is dropped server-side too; the adapter's
    # own <=cutoff guard is what the post-cutoff test ultimately proves.
    "With Body": [
        {"revid": 555, "parentid": 554, "timestamp": "2024-05-15T10:00:00Z"},
    ],
    "Body Fails": [
        {"revid": 777, "parentid": 776, "timestamp": "2024-05-15T10:00:00Z"},
    ],
    "No Pre Cutoff": [],  # rvstart=<cutoff>&rvdir=older returned nothing
    "Post Cutoff Only": [
        # Only a post-cutoff revision exists; rvstart should have excluded it, but the server
        # returns it anyway to prove the adapter never selects a post-cutoff version.
        {"revid": 999, "parentid": 998, "timestamp": "2025-01-01T00:00:00Z"},
    ],
    "Multi": [
        # Listing carries several; the API's rvlimit=1 would give the newest <= cutoff, but the
        # server returns all to prove client-side selection picks the latest eligible one.
        {"revid": 300, "parentid": 299, "timestamp": "2025-09-01T00:00:00Z"},  # post-cutoff
        {"revid": 220, "parentid": 219, "timestamp": "2024-05-15T10:00:00Z"},  # latest <= cutoff
        {"revid": 100, "parentid": 99, "timestamp": "2023-01-01T00:00:00Z"},
    ],
}

_MEDIAWIKI_CONTENT = {
    "555": (200, b"<wikitext>with body revision 555</wikitext>"),
    "220": (200, b"<wikitext>multi latest pre-cutoff revision 220</wikitext>"),
    # revid 777 (Body Fails) intentionally absent -> content endpoint returns 204 empty -> PARTIAL.
}


def _github_commit(sha: str, date: str) -> dict:
    return {"sha": sha, "commit": {"committer": {"date": date}, "author": {"date": date}}}


_GITHUB_LISTINGS = {
    # path -> commits list the API returns for &until=<cutoff>&per_page=1
    "docs/with-body.md": [_github_commit("sha-withbody", "2024-05-15T10:00:00Z")],
    "docs/body-fails.md": [_github_commit("sha-bodyfails", "2024-05-15T10:00:00Z")],
    "docs/no-pre-cutoff.md": [],
    "docs/post-cutoff-only.md": [_github_commit("sha-future", "2025-01-01T00:00:00Z")],
    "docs/multi.md": [
        _github_commit("sha-future", "2025-09-01T00:00:00Z"),  # post-cutoff
        _github_commit("sha-latest", "2024-05-15T10:00:00Z"),  # latest <= cutoff
        _github_commit("sha-old", "2023-01-01T00:00:00Z"),
    ],
}

_GITHUB_RAW = {
    "sha-withbody": (200, b"# with body file content"),
    "sha-latest": (200, b"# multi latest pre-cutoff file content"),
    # sha-bodyfails intentionally absent -> raw endpoint returns 204 empty -> PARTIAL.
}


@pytest.fixture
def publisher_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)

            if parsed.path == "/w/api.php":
                self._handle_mediawiki(query)
                return
            if parsed.path.startswith("/repos/") and parsed.path.endswith("/commits"):
                self._handle_github_listing(query)
                return
            if parsed.path.startswith("/raw/"):
                self._handle_github_raw(parsed.path)
                return

            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"unexpected path")

        def _handle_mediawiki(self, query: dict) -> None:
            title = query.get("titles", [""])[0]
            rvprop = query.get("rvprop", [""])[0]
            if "content" in rvprop:
                revid = query.get("rvstartid", [""])[0]
                response = _MEDIAWIKI_CONTENT.get(revid)
                if response is None:
                    self._send(204, b"")
                    return
                status, body = response
                payload = _mediawiki_listing(
                    [{"revid": int(revid), "timestamp": "2024-05-15T10:00:00Z", "content": body.decode()}]
                )
                self._send_json(status, payload)
                return
            if title == "Listing Transport Fails":
                # Empty body -> direct_http maps this to a NO_BODY DirectHttpCaptureFailure, i.e. a
                # genuine transport-level listing-lookup failure (distinct from NO-GO/PARTIAL).
                self._send(204, b"")
                return
            revisions = _MEDIAWIKI_LISTINGS.get(title)
            if revisions is None:
                self._send(500, b"unexpected wiki title")
                return
            self._send_json(200, _mediawiki_listing(revisions))

        def _handle_github_listing(self, query: dict) -> None:
            path = query.get("path", [""])[0]
            commits = _GITHUB_LISTINGS.get(path)
            if commits is None:
                self._send(500, b"unexpected github path")
                return
            self._send_json(200, commits)

        def _handle_github_raw(self, path: str) -> None:
            # /raw/<owner>/<repo>/<sha>/<path...>
            parts = path.split("/")
            if len(parts) < 5:
                self._send(500, b"unexpected raw path")
                return
            sha = parts[4]
            response = _GITHUB_RAW.get(sha)
            if response is None:
                self._send(204, b"")
                return
            status, body = response
            self._send(status, body)

        def _send_json(self, status: int, payload: object) -> None:
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)

        def _send(self, status: int, body: bytes) -> None:
            self.send_response(status)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            if body:
                self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base = f"http://127.0.0.1:{server.server_address[1]}"
        yield {
            "wiki_api_base": base,
            "github_api_base": base,
            "github_raw_base": f"{base}/raw",
        }
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


CUTOFF = "2024-06-01T00:00:00Z"


# --------------------------------------------------------------------------------------------------
# MediaWiki rung
# --------------------------------------------------------------------------------------------------


def test_mediawiki_selects_latest_pre_cutoff_with_served_identity_and_timestamp(
    publisher_server: dict[str, str],
) -> None:
    result = fetch_mediawiki_history_capture(
        wiki_api_base=publisher_server["wiki_api_base"],
        title="Multi",
        cutoff_timestamp=CUTOFF,
        timeout_seconds=5,
        max_bytes=4096,
    )

    assert isinstance(result, PublisherHistoryCaptureSuccess)
    assert result.selected_revision is not None
    # Served identity (revid) + served timestamp are non-opaque proof (AR-02), and the chosen
    # revision is the latest one <= cutoff (220), never the post-cutoff 300.
    assert result.selected_revision.identity == "220"
    assert result.selected_revision.served_timestamp == "2024-05-15T10:00:00Z"
    assert result.selected_revision.served_timestamp <= CUTOFF


def test_mediawiki_fetches_content_for_selected_revision(
    publisher_server: dict[str, str],
) -> None:
    result = fetch_mediawiki_history_capture(
        wiki_api_base=publisher_server["wiki_api_base"],
        title="With Body",
        cutoff_timestamp=CUTOFF,
        timeout_seconds=5,
        max_bytes=4096,
    )

    assert isinstance(result, PublisherHistoryCaptureSuccess)
    assert result.selected_revision is not None
    assert result.selected_revision.identity == "555"
    assert isinstance(result.body_result, DirectHttpCaptureSuccess)
    assert b"with body revision 555" in result.body_result.body


def test_mediawiki_no_pre_cutoff_revision_is_no_go(
    publisher_server: dict[str, str],
) -> None:
    result = fetch_mediawiki_history_capture(
        wiki_api_base=publisher_server["wiki_api_base"],
        title="No Pre Cutoff",
        cutoff_timestamp=CUTOFF,
        timeout_seconds=5,
        max_bytes=4096,
    )

    assert isinstance(result, PublisherHistoryCaptureSuccess)
    assert result.selected_revision is None  # NO-GO
    assert result.body_result is None
    assert result.selection_warning is not None


def test_mediawiki_content_fetch_failure_is_partial(
    publisher_server: dict[str, str],
) -> None:
    result = fetch_mediawiki_history_capture(
        wiki_api_base=publisher_server["wiki_api_base"],
        title="Body Fails",
        cutoff_timestamp=CUTOFF,
        timeout_seconds=5,
        max_bytes=4096,
    )

    assert isinstance(result, PublisherHistoryCaptureSuccess)
    # Version selected (availability) but body not retrieved (PARTIAL); the two are separated.
    assert result.selected_revision is not None
    assert result.selected_revision.identity == "777"
    assert isinstance(result.body_result, DirectHttpCaptureFailure)


def test_mediawiki_never_selects_post_cutoff_revision(
    publisher_server: dict[str, str],
) -> None:
    result = fetch_mediawiki_history_capture(
        wiki_api_base=publisher_server["wiki_api_base"],
        title="Post Cutoff Only",
        cutoff_timestamp=CUTOFF,
        timeout_seconds=5,
        max_bytes=4096,
    )

    # The server returned a post-cutoff revision (999 @ 2025); the adapter's <=cutoff guard must
    # refuse to select it -> NO-GO, no body fetch, no post-cutoff leak.
    assert isinstance(result, PublisherHistoryCaptureSuccess)
    assert result.selected_revision is None
    assert result.body_result is None


# --------------------------------------------------------------------------------------------------
# GitHub rung
# --------------------------------------------------------------------------------------------------


def test_github_selects_latest_pre_cutoff_with_served_identity_and_timestamp(
    publisher_server: dict[str, str],
) -> None:
    result = fetch_github_history_capture(
        owner="acme",
        repo="docs",
        path="docs/multi.md",
        cutoff_timestamp=CUTOFF,
        api_base=publisher_server["github_api_base"],
        raw_base=publisher_server["github_raw_base"],
        timeout_seconds=5,
        max_bytes=4096,
    )

    assert isinstance(result, PublisherHistoryCaptureSuccess)
    assert result.selected_revision is not None
    assert result.selected_revision.identity == "sha-latest"
    assert result.selected_revision.served_timestamp == "2024-05-15T10:00:00Z"
    assert result.selected_revision.served_timestamp <= CUTOFF


def test_github_fetches_content_for_selected_commit(
    publisher_server: dict[str, str],
) -> None:
    result = fetch_github_history_capture(
        owner="acme",
        repo="docs",
        path="docs/with-body.md",
        cutoff_timestamp=CUTOFF,
        api_base=publisher_server["github_api_base"],
        raw_base=publisher_server["github_raw_base"],
        timeout_seconds=5,
        max_bytes=4096,
    )

    assert isinstance(result, PublisherHistoryCaptureSuccess)
    assert result.selected_revision is not None
    assert result.selected_revision.identity == "sha-withbody"
    assert isinstance(result.body_result, DirectHttpCaptureSuccess)
    assert b"with body file content" in result.body_result.body


def test_github_no_pre_cutoff_commit_is_no_go(
    publisher_server: dict[str, str],
) -> None:
    result = fetch_github_history_capture(
        owner="acme",
        repo="docs",
        path="docs/no-pre-cutoff.md",
        cutoff_timestamp=CUTOFF,
        api_base=publisher_server["github_api_base"],
        raw_base=publisher_server["github_raw_base"],
        timeout_seconds=5,
        max_bytes=4096,
    )

    assert isinstance(result, PublisherHistoryCaptureSuccess)
    assert result.selected_revision is None  # NO-GO
    assert result.body_result is None
    assert result.selection_warning is not None


def test_github_content_fetch_failure_is_partial(
    publisher_server: dict[str, str],
) -> None:
    result = fetch_github_history_capture(
        owner="acme",
        repo="docs",
        path="docs/body-fails.md",
        cutoff_timestamp=CUTOFF,
        api_base=publisher_server["github_api_base"],
        raw_base=publisher_server["github_raw_base"],
        timeout_seconds=5,
        max_bytes=4096,
    )

    assert isinstance(result, PublisherHistoryCaptureSuccess)
    assert result.selected_revision is not None
    assert result.selected_revision.identity == "sha-bodyfails"
    assert isinstance(result.body_result, DirectHttpCaptureFailure)


def test_github_never_selects_post_cutoff_commit(
    publisher_server: dict[str, str],
) -> None:
    result = fetch_github_history_capture(
        owner="acme",
        repo="docs",
        path="docs/post-cutoff-only.md",
        cutoff_timestamp=CUTOFF,
        api_base=publisher_server["github_api_base"],
        raw_base=publisher_server["github_raw_base"],
        timeout_seconds=5,
        max_bytes=4096,
    )

    assert isinstance(result, PublisherHistoryCaptureSuccess)
    assert result.selected_revision is None
    assert result.body_result is None


# --------------------------------------------------------------------------------------------------
# Listing-lookup failure (distinct from NO-GO/PARTIAL) + input validation + URL shape
# --------------------------------------------------------------------------------------------------


def test_mediawiki_listing_transport_failure_returns_failure(
    publisher_server: dict[str, str],
) -> None:
    # A transport-level listing failure (empty body -> direct_http NO_BODY) is a
    # PublisherHistoryCaptureFailure, NOT a NO-GO success: no version could even be located.
    result = fetch_mediawiki_history_capture(
        wiki_api_base=publisher_server["wiki_api_base"],
        title="Listing Transport Fails",
        cutoff_timestamp=CUTOFF,
        timeout_seconds=5,
        max_bytes=4096,
    )
    assert isinstance(result, PublisherHistoryCaptureFailure)
    assert isinstance(result.listing_result, DirectHttpCaptureFailure)


def test_mediawiki_unparseable_listing_with_body_is_no_go_not_failure(
    publisher_server: dict[str, str],
) -> None:
    # A non-2xx listing that still returns a body is a DirectHttpCaptureSuccess (body preserved),
    # so the listing leg "succeeded"; the body just is not parseable revision JSON -> NO-GO with a
    # parse_warning, never an opaque pass. This documents the availability/body boundary.
    result = fetch_mediawiki_history_capture(
        wiki_api_base=publisher_server["wiki_api_base"],
        title="Unknown Title",  # fake server answers HTTP 500 with a non-JSON body
        cutoff_timestamp=CUTOFF,
        timeout_seconds=5,
        max_bytes=4096,
    )
    assert isinstance(result, PublisherHistoryCaptureSuccess)
    assert result.selected_revision is None
    assert result.parse_warning is not None


def test_invalid_cutoff_raises_value_error(publisher_server: dict[str, str]) -> None:
    with pytest.raises(ValueError):
        fetch_github_history_capture(
            owner="acme",
            repo="docs",
            path="docs/multi.md",
            cutoff_timestamp="not-a-timestamp",
            api_base=publisher_server["github_api_base"],
            raw_base=publisher_server["github_raw_base"],
        )


def test_build_mediawiki_history_url_carries_cutoff_and_older_direction() -> None:
    url = build_mediawiki_history_url(
        wiki_api_base="https://en.wikipedia.org",
        title="Some Page",
        cutoff_timestamp="2024-06-01T00:00:00Z",
    )
    query = parse_qs(urlparse(url).query)
    assert query["rvstart"] == ["2024-06-01T00:00:00Z"]
    assert query["rvdir"] == ["older"]
    assert query["rvlimit"] == ["1"]
    assert query["prop"] == ["revisions"]


def test_build_github_history_url_carries_until_and_path() -> None:
    url = build_github_history_url(
        owner="acme",
        repo="docs",
        path="docs/multi.md",
        cutoff_timestamp="2024-06-01T00:00:00Z",
    )
    query = parse_qs(urlparse(url).query)
    assert query["until"] == ["2024-06-01T00:00:00Z"]
    assert query["path"] == ["docs/multi.md"]
    assert query["per_page"] == ["1"]
