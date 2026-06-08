from __future__ import annotations

import ast
import importlib
from pathlib import Path


FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "archivebox",
    "bs4",
    "httpx",
    "praw",
    "requests",
    "scrapy",
    "selenium",
    "webbrowser",
}


def test_browser_snapshot_module_imports_without_playwright_installed() -> None:
    module = importlib.import_module("source_capture.adapters.browser_snapshot")

    assert hasattr(module, "fetch_browser_snapshot_capture")


def test_browser_snapshot_adapter_avoids_scraper_api_proxy_and_webbrowser_imports() -> None:
    project_root = Path(__file__).resolve().parents[2]
    target_paths = [
        project_root / "source_capture" / "adapters" / "__init__.py",
        project_root / "source_capture" / "adapters" / "browser_snapshot.py",
        project_root / "runners" / "run_source_capture_browser_packet.py",
        project_root / "runners" / "run_source_capture_authenticated_browser_packet.py",
        project_root / "runners" / "run_source_capture_browser_session_bootstrap.py",
    ]

    for path in target_paths:
        assert path.exists(), f"browser snapshot path missing: {path}"
        assert not _forbidden_import_roots(path), f"Forbidden import in {path}"


def test_only_browser_snapshot_surfaces_name_playwright_dependency() -> None:
    project_root = Path(__file__).resolve().parents[2]
    source_capture_paths = sorted((project_root / "source_capture").rglob("*.py"))
    runner_paths = sorted((project_root / "runners").glob("run_source_capture_*packet.py"))
    allowed = {
        project_root / "source_capture" / "adapters" / "browser_snapshot.py",
        project_root / "source_capture" / "adapters" / "cloakbrowser_snapshot.py",
        project_root / "runners" / "run_source_capture_authenticated_browser_packet.py",
        project_root / "runners" / "run_source_capture_browser_session_bootstrap.py",
    }
    offenders: list[Path] = []
    for path in source_capture_paths + runner_paths:
        if path in allowed:
            continue
        if "playwright" in path.read_text(encoding="utf-8").lower():
            offenders.append(path)

    assert offenders == []


def _forbidden_import_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    forbidden: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            forbidden.update(
                alias.name.split(".")[0]
                for alias in node.names
                if alias.name.split(".")[0] in FORBIDDEN_IMPORT_ROOTS
            )
        if isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".")[0]
            if root in FORBIDDEN_IMPORT_ROOTS:
                forbidden.add(root)
    return forbidden
