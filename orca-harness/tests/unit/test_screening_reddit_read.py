from __future__ import annotations

# Tests for source_capture/screening_reddit_read.py
# Gate coverage (§7 commission):
#   (a) screen-light: no packet, no staging, no stage_and_write_packet touch
#   (b) logged-out + bounded: max_bytes/timeout passed through; no proxy/auth
#   (c) read path: returned fields match the adapter response
#   (d) entitlement gate: auth-gated / non-reddit URLs refused pre-fetch

import ast
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from source_capture.screening_reddit_read import (
    RATE_CEILING_NOTE,
    RedditScreeningReadRefused,
    RedditScreenLight,
    reddit_screening_read,
)
from source_capture.adapters.direct_http import (
    DirectHttpCaptureFailure,
    DirectHttpCaptureFailureKind,
    DirectHttpCaptureSuccess,
)

_HARNESS_ROOT = Path(__file__).resolve().parents[2]
_MODULE_PATH = _HARNESS_ROOT / "source_capture" / "screening_reddit_read.py"


# ---------------------------------------------------------------------------
# (a) Screen-light boundary: no stage_and_write_packet anywhere in the module
# ---------------------------------------------------------------------------

def _ast_imported_names(path: Path) -> set[str]:
    """Return all names imported (from X import Y → Y; import X → X) in the module."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
            for alias in node.names:
                names.add(alias.name)
    return names


def _ast_called_names(path: Path) -> set[str]:
    """Return all simple function-call names (flat calls like foo()) in the module."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                names.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                names.add(node.func.attr)
    return names


def test_screening_module_does_not_import_stage_and_write_packet() -> None:
    """AST: stage_and_write_packet must not be imported or called in the screening module."""
    imported = _ast_imported_names(_MODULE_PATH)
    called = _ast_called_names(_MODULE_PATH)
    assert "stage_and_write_packet" not in imported, (
        "screening_reddit_read imports stage_and_write_packet — "
        "that path writes a SourceCapturePacket into ECR (screen-light violation)."
    )
    assert "stage_and_write_packet" not in called, (
        "screening_reddit_read calls stage_and_write_packet — "
        "that path writes a SourceCapturePacket into ECR (screen-light violation)."
    )


def test_screening_module_does_not_import_packet_runner() -> None:
    """AST: run_source_capture_http_packet must not be imported or called by the screening module."""
    imported = _ast_imported_names(_MODULE_PATH)
    called = _ast_called_names(_MODULE_PATH)
    assert "run_source_capture_http_packet" not in imported, (
        "screening_reddit_read imports run_source_capture_http_packet — forbidden."
    )
    assert "run_source_capture_http_packet" not in called, (
        "screening_reddit_read calls run_source_capture_http_packet — forbidden."
    )


def test_screening_module_does_not_import_packet_assembly() -> None:
    """AST: packet_assembly (the ECR write path) must not be imported."""
    imported = _ast_imported_names(_MODULE_PATH)
    assert not any("packet_assembly" in name for name in imported), (
        "screening_reddit_read imports something from packet_assembly — "
        "that is the ECR write path."
    )


def test_screening_module_ast_imports_only_adapter_not_packet_runner() -> None:
    """AST-level check: only the direct_http adapter is imported, not the packet runner."""
    tree = ast.parse(_MODULE_PATH.read_text(encoding="utf-8"), filename=str(_MODULE_PATH))
    forbidden_roots = {"packet_assembly", "run_source_capture_http_packet"}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".")[0]
            if root in forbidden_roots:
                pytest.fail(f"Forbidden import root {root!r} found in screening module.")
            for part in node.module.split("."):
                if part in forbidden_roots:
                    pytest.fail(f"Forbidden module part {part!r} found in screening module.")


def test_screen_light_result_has_no_packet_fields() -> None:
    """RedditScreenLight must not carry any packet/staging/ECR fields."""
    fields = {f.name for f in RedditScreenLight.__dataclass_fields__.values()}
    packet_fields = {
        "packet_path", "output_directory", "staged_artifacts", "source_slices",
        "manifest", "ecr", "packet", "staging",
    }
    overlap = fields & packet_fields
    assert not overlap, f"RedditScreenLight carries packet/ECR field(s): {overlap}"


# ---------------------------------------------------------------------------
# (b) Logged-out + bounded: max_bytes/timeout honored, no proxy/auth headers
# ---------------------------------------------------------------------------

def _make_success_result(url: str, body: bytes = b"thread /comments/abc 123") -> DirectHttpCaptureSuccess:
    return DirectHttpCaptureSuccess(
        requested_url=url,
        final_url=url,
        status=200,
        reason="OK",
        metadata={"byte_count": len(body), "capture_timestamp": "2026-06-12T00:00:00Z"},
        body=body,
        warning_notes=[],
        limitation_notes=[],
    )


def test_bounded_params_are_passed_to_adapter() -> None:
    """max_bytes and timeout_seconds are forwarded to fetch_direct_http_capture."""
    url = "https://old.reddit.com/r/beauty/search?q=test&restrict_sr=on&sort=new"
    mock_result = _make_success_result(url)

    with patch(
        "source_capture.screening_reddit_read.fetch_direct_http_capture",
        return_value=mock_result,
    ) as mock_fetch:
        reddit_screening_read(url=url, timeout_seconds=15.0, max_bytes=500_000)

    mock_fetch.assert_called_once_with(
        url=url,
        timeout_seconds=15.0,
        max_bytes=500_000,
    )


def test_default_bounds_are_sane() -> None:
    """Default timeout and max_bytes are forwarded when not overridden."""
    url = "https://old.reddit.com/r/beauty/search?q=test&restrict_sr=on&sort=new"
    mock_result = _make_success_result(url)

    with patch(
        "source_capture.screening_reddit_read.fetch_direct_http_capture",
        return_value=mock_result,
    ) as mock_fetch:
        reddit_screening_read(url=url)

    _, kwargs = mock_fetch.call_args
    assert kwargs["timeout_seconds"] > 0
    assert kwargs["max_bytes"] > 0


def test_adapter_uses_no_proxy_opener() -> None:
    """The direct_http adapter itself uses ProxyHandler({}) — confirm we call the adapter, not raw urllib."""
    # We confirm we call fetch_direct_http_capture (the no-proxy adapter), not urllib directly.
    # The no-proxy guarantee is in the adapter; this test ensures we use the adapter path.
    source = _MODULE_PATH.read_text(encoding="utf-8")
    assert "fetch_direct_http_capture" in source
    # We must NOT call urlopen or build_opener directly in the screening module.
    assert "urlopen" not in source
    assert "build_opener" not in source


# ---------------------------------------------------------------------------
# (c) Read path: returned fields match the adapter response
# ---------------------------------------------------------------------------

def test_screen_light_fields_populated_from_adapter() -> None:
    """RedditScreenLight carries the correct fields from the adapter response."""
    url = "https://old.reddit.com/r/beauty/search?q=moisturizer&restrict_sr=on&sort=new"
    body = b"some text /comments/abc123 and /comments/def456 end"
    mock_result = _make_success_result(url, body=body)

    with patch(
        "source_capture.screening_reddit_read.fetch_direct_http_capture",
        return_value=mock_result,
    ):
        result = reddit_screening_read(url=url)

    assert isinstance(result, RedditScreenLight)
    assert result.final_url == url
    assert result.status == 200
    assert result.byte_count == len(body)
    assert result.comments_marker_count == 2
    assert result.rate_ceiling_note == RATE_CEILING_NOTE


def test_comments_marker_count_is_zero_when_no_markers() -> None:
    url = "https://old.reddit.com/r/beauty/search?q=test&restrict_sr=on&sort=new"
    mock_result = _make_success_result(url, body=b"no markers here")

    with patch(
        "source_capture.screening_reddit_read.fetch_direct_http_capture",
        return_value=mock_result,
    ):
        result = reddit_screening_read(url=url)

    assert isinstance(result, RedditScreenLight)
    assert result.comments_marker_count == 0


def test_fetch_failure_returns_refused_not_exception() -> None:
    """A fetch failure returns RedditScreeningReadRefused, not an exception."""
    url = "https://old.reddit.com/r/beauty/search?q=test&restrict_sr=on&sort=new"
    failure = DirectHttpCaptureFailure(
        requested_url=url,
        failure_kind=DirectHttpCaptureFailureKind.NETWORK_ERROR,
        message="name resolution failed",
    )

    with patch(
        "source_capture.screening_reddit_read.fetch_direct_http_capture",
        return_value=failure,
    ):
        result = reddit_screening_read(url=url)

    assert isinstance(result, RedditScreeningReadRefused)
    assert result.reason == "fetch_failed"
    assert "name resolution failed" in result.message


def test_login_redirect_is_refused_post_fetch() -> None:
    """If Reddit redirects to a login page, the result is refused (not returned as screen-light)."""
    requested_url = "https://old.reddit.com/r/beauty/search?q=test&restrict_sr=on&sort=new"
    login_url = "https://www.reddit.com/login?dest=..."
    mock_result = DirectHttpCaptureSuccess(
        requested_url=requested_url,
        final_url=login_url,
        status=200,
        reason="OK",
        metadata={"byte_count": 100, "capture_timestamp": "2026-06-12T00:00:00Z"},
        body=b"please log in",
        warning_notes=[f"direct_http followed redirect from {requested_url} to {login_url}"],
        limitation_notes=[],
    )

    with patch(
        "source_capture.screening_reddit_read.fetch_direct_http_capture",
        return_value=mock_result,
    ):
        result = reddit_screening_read(url=requested_url)

    assert isinstance(result, RedditScreeningReadRefused)
    assert result.reason == "login_redirect"


def test_login_page_body_without_redirect_is_refused_post_fetch() -> None:
    """If Reddit serves a login page at the requested URL, the screen-light result is refused."""
    requested_url = "https://old.reddit.com/r/beauty/search?q=test&restrict_sr=on&sort=new"
    mock_result = DirectHttpCaptureSuccess(
        requested_url=requested_url,
        final_url=requested_url,
        status=200,
        reason="OK",
        metadata={"byte_count": 100, "capture_timestamp": "2026-06-12T00:00:00Z"},
        body=b'<html><form action="/login" method="post">Log in to Reddit</form></html>',
        warning_notes=[],
        limitation_notes=[],
    )

    with patch(
        "source_capture.screening_reddit_read.fetch_direct_http_capture",
        return_value=mock_result,
    ):
        result = reddit_screening_read(url=requested_url)

    assert isinstance(result, RedditScreeningReadRefused)
    assert result.reason == "login_redirect"


# ---------------------------------------------------------------------------
# (d) Entitlement gate: auth-gated / non-reddit URLs refused pre-fetch
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "gated_url,expected_substring",
    [
        # Non-reddit host
        (
            "https://www.example.com/r/beauty/search?q=test",
            "example.com",
        ),
        # Reddit API / OAuth host — not old.reddit or www.reddit
        (
            "https://oauth.reddit.com/r/beauty/search?q=test",
            "oauth.reddit.com",
        ),
        # reddit.com without subdomain (not in allowed set)
        (
            "https://reddit.com/r/beauty/search?q=test",
            "reddit.com",
        ),
        # Non-HTTPS and non-absolute URLs are refused before the adapter.
        (
            "http://old.reddit.com/r/beauty/search?q=test",
            "scheme",
        ),
        (
            "//old.reddit.com/r/beauty/search?q=test",
            "scheme",
        ),
        # Path does not start with /r/
        (
            "https://old.reddit.com/login?dest=/r/beauty",
            "/login",
        ),
        # Settings page
        (
            "https://old.reddit.com/prefs",
            "/prefs",
        ),
        # Dot-segment traversal must not pass the /r/ prefix gate.
        (
            "https://old.reddit.com/r/../login",
            "dot-segment",
        ),
        (
            "https://old.reddit.com/r/%2e%2e/login",
            "dot-segment",
        ),
    ],
)
def test_entitlement_gate_refuses_non_public_urls_without_fetch(
    gated_url: str, expected_substring: str
) -> None:
    """Auth-gated / non-public URLs are refused pre-fetch (no network call made)."""
    with patch(
        "source_capture.screening_reddit_read.fetch_direct_http_capture"
    ) as mock_fetch:
        result = reddit_screening_read(url=gated_url)

    mock_fetch.assert_not_called()
    assert isinstance(result, RedditScreeningReadRefused)
    assert result.reason == "entitlement_gated"
    assert expected_substring in result.message


def test_entitlement_gate_allows_old_reddit_search() -> None:
    """A well-formed old.reddit.com /r/<sub>/search URL passes the gate."""
    url = "https://old.reddit.com/r/beauty/search?q=skincare&restrict_sr=on&sort=new"
    mock_result = _make_success_result(url)

    with patch(
        "source_capture.screening_reddit_read.fetch_direct_http_capture",
        return_value=mock_result,
    ) as mock_fetch:
        result = reddit_screening_read(url=url)

    mock_fetch.assert_called_once()
    assert isinstance(result, RedditScreenLight)


def test_entitlement_gate_allows_www_reddit_subreddit() -> None:
    """A well-formed www.reddit.com /r/<sub>/... URL passes the gate."""
    url = "https://www.reddit.com/r/beauty/new/"
    mock_result = _make_success_result(url)

    with patch(
        "source_capture.screening_reddit_read.fetch_direct_http_capture",
        return_value=mock_result,
    ) as mock_fetch:
        result = reddit_screening_read(url=url)

    mock_fetch.assert_called_once()
    assert isinstance(result, RedditScreenLight)


def test_refusal_carries_requested_url() -> None:
    """RedditScreeningReadRefused always carries the originally-requested URL."""
    gated_url = "https://api.reddit.com/r/beauty/search"
    result = reddit_screening_read(url=gated_url)

    assert isinstance(result, RedditScreeningReadRefused)
    assert result.url == gated_url
