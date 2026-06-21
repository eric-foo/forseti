from __future__ import annotations

import ast
from pathlib import Path
from unittest.mock import patch

from source_capture.adapters.anti_blocking_http import AntiBlockingHttpCaptureSuccess
from source_capture.adapters.direct_http import DirectHttpCaptureSuccess
from source_capture.screening_browser_read import SCREENING_ORCHESTRATOR_CONTEXT, ScreeningBrowserRead
from source_capture.screening_read import (
    ScreeningReadRecord,
    ScreeningReadRefused,
    ScreeningReadRoute,
    extract_old_reddit_listing_fields,
    screening_read,
)

_HARNESS_ROOT = Path(__file__).resolve().parents[2]
_MODULE_PATH = _HARNESS_ROOT / "source_capture" / "screening_read.py"


def _ast_imported_names(path: Path) -> set[str]:
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
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                names.add(node.func.id)
            elif isinstance(node.func, ast.Attribute):
                names.add(node.func.attr)
    return names


def _direct_success(url: str, body: bytes, status: int = 200) -> DirectHttpCaptureSuccess:
    return DirectHttpCaptureSuccess(
        requested_url=url,
        final_url=url,
        status=status,
        reason="OK" if status == 200 else "Forbidden",
        metadata={"byte_count": len(body), "capture_timestamp": "2026-06-21T00:00:00Z"},
        body=body,
        warning_notes=[],
        limitation_notes=[],
    )


def test_refuses_non_orchestrator_invocation_without_fetch() -> None:
    with patch("source_capture.screening_read.fetch_direct_http_capture") as direct_fetch:
        result = screening_read(
            url="https://example.com/source",
            route=ScreeningReadRoute.DIRECT_HTTP,
            invocation_context="walker",
        )

    direct_fetch.assert_not_called()
    assert isinstance(result, ScreeningReadRefused)
    assert result.reason == "not_orchestrator_invoked"


def test_direct_http_route_classifies_cloudflare_shell() -> None:
    url = "https://www.basenotes.com/fragrances/mojave-ghost-by-byredo.26143979/"
    body = b"<html><title>Just a moment...</title><body>enable JavaScript</body></html>"

    with patch(
        "source_capture.screening_read.fetch_direct_http_capture",
        return_value=_direct_success(url, body, status=403),
    ):
        result = screening_read(
            url=url,
            route=ScreeningReadRoute.DIRECT_HTTP,
            invocation_context=SCREENING_ORCHESTRATOR_CONTEXT,
        )

    assert isinstance(result, ScreeningReadRecord)
    assert result.content_class == "block_shell"
    assert result.content_signal == "cloudflare_interstitial"
    assert any("access_failed" in note for note in result.limitation_notes)
    assert result.metadata["packet_written"] is False
    assert result.metadata["ecr_touched"] is False


def test_anti_blocking_route_classifies_cf_mitigated_header() -> None:
    url = "https://www.basenotes.com/fragrances/mojave-ghost-by-byredo.26143979/"
    body = b"<html><body>challenge body</body></html>"
    anti_result = AntiBlockingHttpCaptureSuccess(
        requested_url=url,
        final_url=url,
        status=403,
        reason="Forbidden",
        impersonation_profile="header_complete_stdlib",
        method_category="anti_blocking_http",
        response_headers={"cf-mitigated": "challenge"},
        metadata={"byte_count": len(body), "capture_timestamp": "2026-06-21T00:00:00Z"},
        body=body,
        warning_notes=[],
        limitation_notes=[],
    )

    with patch(
        "source_capture.screening_read.fetch_anti_blocking_http_capture",
        return_value=anti_result,
    ):
        result = screening_read(
            url=url,
            route=ScreeningReadRoute.ANTI_BLOCKING_HTTP,
            invocation_context=SCREENING_ORCHESTRATOR_CONTEXT,
        )

    assert isinstance(result, ScreeningReadRecord)
    assert result.content_class == "block_shell"
    assert result.content_signal == "cloudflare_mitigated"
    assert result.metadata["method_category"] == "anti_blocking_http"


def test_browser_route_delegates_bounded_params_to_screening_browser_read() -> None:
    browser_result = ScreeningBrowserRead(
        requested_url="https://www.basenotes.com/fragrances/mojave-ghost-by-byredo.26143979/",
        final_url="https://www.basenotes.com/fragrances/mojave-ghost-by-byredo.26143979/",
        title="Mojave Ghost by Byredo",
        visible_text="Mojave Ghost by Byredo\nBasenotes review text",
        byte_count=43,
        content_class="content_unverified",
        content_signal=None,
        content_detail="no known block/challenge signature detected",
        metadata={"packet_written": False, "ecr_touched": False},
    )

    with patch(
        "source_capture.screening_read.screening_browser_read",
        return_value=browser_result,
    ) as browser_read:
        result = screening_read(
            url=browser_result.requested_url,
            route=ScreeningReadRoute.BROWSER,
            invocation_context=SCREENING_ORCHESTRATOR_CONTEXT,
            timeout_seconds=9.0,
            max_bytes=123_456,
            browser_settle_seconds=1.5,
            browser_scroll_passes=2,
            browser_scroll_step_px=600,
        )

    assert isinstance(result, ScreeningReadRecord)
    browser_read.assert_called_once_with(
        url=browser_result.requested_url,
        invocation_context=SCREENING_ORCHESTRATOR_CONTEXT,
        timeout_seconds=9.0,
        max_artifact_bytes=123_456,
        settle_seconds=1.5,
        scroll_passes=2,
        scroll_step_px=600,
    )


def test_reddit_old_search_route_records_first_act_receipt_and_row_local_date() -> None:
    url = "https://old.reddit.com/r/fragrance/search?q=byredo&restrict_sr=on&sort=new"
    html = """
    <html>
      <body>
        <aside class="side">
          <time datetime="2011-01-01T00:00:00+00:00">subreddit created</time>
        </aside>
        <div class="thing">
          <a class="search-title may-blank"
             href="https://old.reddit.com/r/fragrance/comments/abc123/byredo_mojave_ghost/">
             Byredo Mojave Ghost
          </a>
          <time datetime="2026-06-01T00:00:00+00:00">submitted</time>
        </div>
      </body>
    </html>
    """.encode("utf-8")

    with patch(
        "source_capture.screening_read.fetch_direct_http_capture",
        return_value=_direct_success(url, html),
    ):
        result = screening_read(
            url=url,
            route=ScreeningReadRoute.REDDIT_OLD_SEARCH,
            invocation_context=SCREENING_ORCHESTRATOR_CONTEXT,
        )

    assert isinstance(result, ScreeningReadRecord)
    assert result.metadata["first_act_old_reddit_receipt"] is True
    assert result.extracted_fields["comments_marker_count"] == 1
    rows = result.extracted_fields["candidate_rows"]
    assert isinstance(rows, list)
    assert rows[0]["post_date"] == "2026-06-01T00:00:00+00:00"
    assert rows[0]["post_date_status"] == "range_sane"
    assert "2011-01-01" not in str(rows)


def test_old_reddit_post_date_range_sanity_rejects_out_of_range_row_date() -> None:
    fields = extract_old_reddit_listing_fields(
        base_url="https://old.reddit.com/r/fragrance/search?q=byredo",
        html="""
        <html>
          <body>
            <div class="thing">
              <a class="search-title may-blank" href="/r/fragrance/comments/abc/title/">Title</a>
              <time datetime="1999-01-01T00:00:00+00:00">bad date</time>
            </div>
          </body>
        </html>
        """,
    )

    rows = fields["candidate_rows"]
    assert isinstance(rows, list)
    assert rows[0]["post_date"] is None
    assert rows[0]["post_date_status"] == "out_of_range"
    assert fields["range_sanity_guard"] == "reddit_launch_to_now_plus_one_day"


def test_screening_read_module_does_not_import_or_call_packet_write_paths() -> None:
    imported = _ast_imported_names(_MODULE_PATH)
    called = _ast_called_names(_MODULE_PATH)
    forbidden = {
        "packet_assembly",
        "run_source_capture_http_packet",
        "run_source_capture_cloakbrowser_packet",
        "stage_and_write_packet",
        "write_local_source_capture_packet",
        "Path",
        "open",
        "write_text",
        "write_bytes",
    }

    assert not (imported & forbidden)
    assert not (called & forbidden)
