from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from unittest.mock import patch

from source_capture.screening_browser_read import (
    SCREENING_ORCHESTRATOR_CONTEXT,
    ScreeningBrowserRead,
    ScreeningBrowserReadRefused,
    screening_browser_read,
)

_HARNESS_ROOT = Path(__file__).resolve().parents[2]
_MODULE_PATH = _HARNESS_ROOT / "source_capture" / "screening_browser_read.py"


@dataclass
class _FakeEngineResult:
    final_url: str
    title: str | None
    rendered_dom: str
    visible_text: str
    screenshot_png: bytes = b"\x89PNG\r\n"
    warning_notes: list[str] = field(default_factory=list)
    pre_capture_outcome: object | None = None


class _FakeEngine:
    def __init__(self, result: _FakeEngineResult) -> None:
        self.result = result
        self.calls: list[dict[str, object]] = []

    def capture(self, **kwargs: object) -> _FakeEngineResult:
        self.calls.append(kwargs)
        return self.result


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


def test_refuses_non_orchestrator_invocation_without_fetch() -> None:
    with patch("source_capture.screening_browser_read.fetch_cloakbrowser_snapshot_capture") as fetch:
        result = screening_browser_read(
            url="https://www.basenotes.com/fragrances/mojave-ghost-by-byredo.26143979/",
            invocation_context="walker",
        )

    fetch.assert_not_called()
    assert isinstance(result, ScreeningBrowserReadRefused)
    assert result.reason == "not_orchestrator_invoked"


def test_refuses_credential_url_without_fetch() -> None:
    with patch("source_capture.screening_browser_read.fetch_cloakbrowser_snapshot_capture") as fetch:
        result = screening_browser_read(
            url="https://user:secret@example.com/private",
            invocation_context=SCREENING_ORCHESTRATOR_CONTEXT,
        )

    fetch.assert_not_called()
    assert isinstance(result, ScreeningBrowserReadRefused)
    assert result.reason == "entitlement_gated"


def test_classifies_visible_text_not_full_dom_cloudflare_residue() -> None:
    engine = _FakeEngine(
        _FakeEngineResult(
            final_url="https://www.basenotes.com/fragrances/mojave-ghost-by-byredo.26143979/",
            title="Mojave Ghost by Byredo",
            rendered_dom=(
                "<html><head><script src='/cdn-cgi/challenge-platform/h/b/orchestrate/jsch/v1'></script>"
                "</head><body><h1>Mojave Ghost by Byredo</h1></body></html>"
            ),
            visible_text=(
                "Mojave Ghost by Byredo\n"
                "Basenotes fragrance reviews\n"
                "Review: airy musk and ambrette, posted Jun 1, 2026"
            ),
        )
    )

    result = screening_browser_read(
        url="https://www.basenotes.com/fragrances/mojave-ghost-by-byredo.26143979/",
        invocation_context=SCREENING_ORCHESTRATOR_CONTEXT,
        engine=engine,
    )

    assert isinstance(result, ScreeningBrowserRead)
    assert result.content_class == "content_unverified"
    assert result.content_signal is None
    assert result.metadata["block_shell_input"] == "visible_text"
    assert "cdn-cgi/challenge-platform" not in result.visible_text


def test_visible_text_block_shell_is_reported_as_access_failed() -> None:
    engine = _FakeEngine(
        _FakeEngineResult(
            final_url="https://example.com/walled",
            title="Just a moment...",
            rendered_dom="<html><body>Just a moment...</body></html>",
            visible_text="Just a moment... Checking your browser before accessing the site.",
        )
    )

    result = screening_browser_read(
        url="https://example.com/walled",
        invocation_context=SCREENING_ORCHESTRATOR_CONTEXT,
        engine=engine,
    )

    assert isinstance(result, ScreeningBrowserRead)
    assert result.content_class == "block_shell"
    assert result.content_signal == "cloudflare_interstitial"
    assert any("access_failed" in note for note in result.limitation_notes)


def test_screening_browser_result_has_no_packet_or_artifact_fields() -> None:
    fields = {f.name for f in ScreeningBrowserRead.__dataclass_fields__.values()}

    assert "rendered_dom" not in fields
    assert "screenshot_png" not in fields
    assert "packet_path" not in fields
    assert "manifest" not in fields
    assert "ecr" not in fields


def test_screening_browser_module_does_not_import_or_call_packet_write_paths() -> None:
    imported = _ast_imported_names(_MODULE_PATH)
    called = _ast_called_names(_MODULE_PATH)
    forbidden = {
        "packet_assembly",
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
