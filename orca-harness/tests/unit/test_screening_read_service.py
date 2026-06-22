from __future__ import annotations

import ast
from pathlib import Path
from unittest.mock import patch

from source_capture.adapters.anti_blocking_http import AntiBlockingHttpCaptureSuccess
from source_capture.adapters.direct_http import DirectHttpCaptureSuccess
from source_capture.block_shell import CaptureBodyClass
from source_capture.screening_extraction import (
    StructuredListingExtractionSpec,
    extract_old_reddit_thread_candidates,
    extract_structured_listing_candidates,
)
from source_capture.screening_read import (
    RATE_CEILING_NOTE,
    ScreeningReadDispatch,
    ScreeningReadRecord,
    ScreeningReadRefused,
    ScreeningReadRoute,
    close_old_reddit_search_surface_receipt,
    screening_read,
)
from source_capture.screening_reddit_read import RedditScreenLight


_HARNESS_ROOT = Path(__file__).resolve().parents[2]
_SCREENING_MODULES = (
    _HARNESS_ROOT / "source_capture" / "screening_read.py",
    _HARNESS_ROOT / "source_capture" / "screening_browser_read.py",
    _HARNESS_ROOT / "source_capture" / "screening_reddit_read.py",
)
_FORBIDDEN_IMPORT_PARTS = {
    "packet_assembly",
    "stage_and_write_packet",
    "runners",
    "run_source_capture_http_packet",
    "run_source_capture_antiblock_http_packet",
    "run_source_capture_cloakbrowser_packet",
    "ecr",
    "cleaning",
    "evidence_binding",
}


def _dispatch() -> ScreeningReadDispatch:
    return ScreeningReadDispatch(screen_id="screen-1", question="What did this one source say?")


def _direct_success(url: str, body: bytes) -> DirectHttpCaptureSuccess:
    return DirectHttpCaptureSuccess(
        requested_url=url,
        final_url=url,
        status=200,
        reason="OK",
        metadata={
            "byte_count": len(body),
            "capture_timestamp": "2026-06-21T00:00:00Z",
            "content_type": "text/html; charset=utf-8",
        },
        body=body,
        warning_notes=[],
        limitation_notes=[],
    )


def _antiblock_success(url: str, body: bytes, headers: dict[str, str] | None = None) -> AntiBlockingHttpCaptureSuccess:
    return AntiBlockingHttpCaptureSuccess(
        requested_url=url,
        final_url=url,
        status=200,
        reason="OK",
        impersonation_profile="header_complete_stdlib",
        method_category="anti_blocking_http",
        response_headers=dict(headers or {"Content-Type": "text/html"}),
        metadata={
            "byte_count": len(body),
            "capture_timestamp": "2026-06-21T00:00:00Z",
            "content_type": "text/html",
            "method_category": "anti_blocking_http",
            "impersonation_profile": "header_complete_stdlib",
        },
        body=body,
        warning_notes=[],
        limitation_notes=[],
    )


def test_screening_modules_do_not_import_or_call_packet_ecr_paths() -> None:
    for path in _SCREENING_MODULES:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    parts = set(alias.name.split("."))
                    assert not (parts & _FORBIDDEN_IMPORT_PARTS), f"forbidden import in {path}: {alias.name}"
            elif isinstance(node, ast.ImportFrom) and node.module:
                parts = set(node.module.split("."))
                imported_names = {alias.name for alias in node.names}
                forbidden = (parts | imported_names) & _FORBIDDEN_IMPORT_PARTS
                assert not forbidden, f"forbidden import in {path}: {forbidden}"
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    assert node.func.id not in _FORBIDDEN_IMPORT_PARTS
                elif isinstance(node.func, ast.Attribute):
                    assert node.func.attr not in _FORBIDDEN_IMPORT_PARTS


def test_screening_read_refuses_walker_direct_before_fetch() -> None:
    dispatch = ScreeningReadDispatch(
        screen_id="screen-1",
        question="one source",
        invoked_by="walker",  # type: ignore[arg-type]
    )
    with patch("source_capture.screening_read.fetch_direct_http_capture") as mock_fetch:
        result = screening_read(
            url="https://example.com/source",
            route=ScreeningReadRoute.DIRECT_HTTP,
            dispatch=dispatch,
        )

    mock_fetch.assert_not_called()
    assert isinstance(result, ScreeningReadRefused)
    assert result.reason == "not_orchestrator_invoked"


def test_screening_read_refuses_non_public_url_before_fetch() -> None:
    with patch("source_capture.screening_read.fetch_direct_http_capture") as mock_fetch:
        result = screening_read(
            url="http://127.0.0.1/private",
            route=ScreeningReadRoute.DIRECT_HTTP,
            dispatch=_dispatch(),
        )

    mock_fetch.assert_not_called()
    assert isinstance(result, ScreeningReadRefused)
    assert result.reason == "entitlement_gated"


def test_direct_http_route_returns_screen_light_record_with_class_and_extraction() -> None:
    url = "https://old.reddit.com/r/b2bmarketing/search?q=meetings&restrict_sr=on&sort=new"
    body = b"""
    <html><body>
      <div class="search-result">
        <a class="search-title may-blank" href="https://old.reddit.com/r/b2bmarketing/comments/abc123/a_meeting_funnel/">
          A meeting funnel
        </a>
        <time class="live-timestamp" datetime="2026-06-20T12:00:00+00:00">1 day ago</time>
      </div>
    </body></html>
    """
    with patch(
        "source_capture.screening_read.fetch_direct_http_capture",
        return_value=_direct_success(url, body),
    ) as mock_fetch:
        result = screening_read(
            url=url,
            route=ScreeningReadRoute.DIRECT_HTTP,
            dispatch=_dispatch(),
            timeout_seconds=7,
            max_bytes=9000,
            old_reddit_submission_min_datetime="2026-01-01T00:00:00Z",
            old_reddit_submission_max_datetime="2026-06-21T23:59:59Z",
        )

    mock_fetch.assert_called_once_with(url=url, timeout_seconds=7, max_bytes=9000)
    assert isinstance(result, ScreeningReadRecord)
    assert result.status == 200
    assert result.byte_count == len(body)
    assert result.content_class == CaptureBodyClass.CONTENT_UNVERIFIED.value
    assert result.extracted_fields["old_reddit_thread_candidate_count"] == 1
    row = result.extracted_fields["old_reddit_thread_candidates"][0]
    assert row["thread_url"] == "https://old.reddit.com/r/b2bmarketing/comments/abc123/a_meeting_funnel/"
    assert row["submission_datetime"] == "2026-06-20T12:00:00Z"
    assert row["submission_datetime_state"] == "known"


def test_antiblocking_route_classifies_block_shell() -> None:
    url = "https://example.com/source"
    body = b"<html><title>Just a moment...</title><body>Checking your browser.</body></html>"
    with patch(
        "source_capture.screening_read.fetch_anti_blocking_http_capture",
        return_value=_antiblock_success(url, body),
    ):
        result = screening_read(
            url=url,
            route=ScreeningReadRoute.ANTI_BLOCKING_HTTP,
            dispatch=_dispatch(),
        )

    assert isinstance(result, ScreeningReadRecord)
    assert result.content_class == CaptureBodyClass.BLOCK_SHELL.value
    assert result.content_signal == "cloudflare_interstitial"


def test_first_act_old_reddit_receipt_helper_uses_bounded_search_surface() -> None:
    screen_light = RedditScreenLight(
        final_url="https://old.reddit.com/r/beauty/search?q=skincare+moisturizer&restrict_sr=on&sort=new",
        status=200,
        byte_count=1234,
        comments_marker_count=2,
        content_class=CaptureBodyClass.CONTENT_UNVERIFIED.value,
        content_signal=None,
        content_class_detail="ok",
        extracted_fields={"comments_marker_count": 2},
    )
    with patch("source_capture.screening_read.reddit_screening_read", return_value=screen_light) as mock_read:
        result = close_old_reddit_search_surface_receipt(dispatch=_dispatch())

    mock_read.assert_called_once()
    _, kwargs = mock_read.call_args
    assert kwargs["url"] == "https://old.reddit.com/r/beauty/search?q=skincare+moisturizer&restrict_sr=on&sort=new"
    assert kwargs["timeout_seconds"] == 20.0
    assert kwargs["max_bytes"] == 500_000
    assert isinstance(result, ScreeningReadRecord)
    assert result.extracted_fields["rate_ceiling_note"] == RATE_CEILING_NOTE


def test_old_reddit_post_date_uses_targeted_locator_not_sidebar_min_datetime() -> None:
    html = """
    <html><body>
      <div class="side"><time datetime="2011-03-01T00:00:00Z">subreddit created</time></div>
      <div class="search-result">
        <a class="search-title may-blank" href="https://old.reddit.com/r/b2bmarketing/comments/new123/newer_thread/">Newer thread</a>
        <time class="live-timestamp" datetime="2026-06-20T12:00:00Z">1 day ago</time>
      </div>
    </body></html>
    """

    rows = extract_old_reddit_thread_candidates(
        body_text=html,
        submission_min_datetime="2025-01-01T00:00:00Z",
        submission_max_datetime="2026-06-21T23:59:59Z",
    )

    assert len(rows) == 1
    assert rows[0].submission_datetime == "2026-06-20T12:00:00Z"
    assert rows[0].submission_datetime_state == "known"


def test_old_reddit_post_date_range_sanity_marks_candidate_out_of_range() -> None:
    html = """
    <html><body>
      <div class="search-result">
        <a class="search-title may-blank" href="https://old.reddit.com/r/b2bmarketing/comments/old123/old_thread/">Old thread</a>
        <time class="live-timestamp" datetime="2011-03-01T00:00:00Z">old</time>
      </div>
    </body></html>
    """

    rows = extract_old_reddit_thread_candidates(
        body_text=html,
        submission_min_datetime="2025-01-01T00:00:00Z",
        submission_max_datetime="2026-06-21T23:59:59Z",
    )

    assert len(rows) == 1
    assert rows[0].submission_datetime == "2011-03-01T00:00:00Z"
    assert rows[0].submission_datetime_state == "out_of_range"
    assert "before range minimum" in (rows[0].submission_datetime_detail or "")


def test_structured_listing_extractor_generalizes_row_scoped_dates() -> None:
    html = """
    <html><body>
      <aside><time datetime="2011-03-01T00:00:00Z">site launched</time></aside>
      <article class="listing-card">
        <a class="listing-title" href="https://example.com/forums/topic-123?ref=listing">Topic 123</a>
        <time class="published-at" datetime="2026-06-20T12:00:00Z">Jun 20</time>
      </article>
    </body></html>
    """

    rows = extract_structured_listing_candidates(
        body_text=html,
        spec=StructuredListingExtractionSpec(
            container_classes=("listing-card",),
            anchor_classes=("listing-title",),
            href_must_contain=("/forums/",),
            datetime_classes=("published-at",),
            datetime_label="published datetime",
        ),
        item_min_datetime="2025-01-01T00:00:00Z",
        item_max_datetime="2026-06-21T23:59:59Z",
    )

    assert len(rows) == 1
    assert rows[0].item_url == "https://example.com/forums/topic-123?ref=listing"
    assert rows[0].title == "Topic 123"
    assert rows[0].source_container_class == "listing-card"
    assert rows[0].item_datetime == "2026-06-20T12:00:00Z"
    assert rows[0].item_datetime_state == "known"


def test_structured_listing_extractor_marks_row_datetime_out_of_range() -> None:
    html = """
    <html><body>
      <article class="listing-card">
        <a class="listing-title" href="https://example.com/forums/topic-201">Topic 201</a>
        <time class="published-at" datetime="2011-03-01T00:00:00Z">old</time>
      </article>
    </body></html>
    """

    rows = extract_structured_listing_candidates(
        body_text=html,
        spec=StructuredListingExtractionSpec(
            container_classes=("listing-card",),
            anchor_classes=("listing-title",),
            href_must_contain=("/forums/",),
            datetime_classes=("published-at",),
            datetime_label="published datetime",
        ),
        item_min_datetime="2025-01-01T00:00:00Z",
        item_max_datetime="2026-06-21T23:59:59Z",
    )

    assert len(rows) == 1
    assert rows[0].item_datetime == "2011-03-01T00:00:00Z"
    assert rows[0].item_datetime_state == "out_of_range"
    assert "published datetime is before range minimum" in (rows[0].item_datetime_detail or "")

def test_screen_light_record_has_no_packet_or_ecr_fields() -> None:
    fields = {field.name for field in ScreeningReadRecord.__dataclass_fields__.values()}
    forbidden = {"packet", "packet_path", "manifest", "manifest_path", "staged_artifacts", "ecr"}
    assert not (fields & forbidden)
