from __future__ import annotations

import ast
import importlib
from pathlib import Path


FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "archivebox",
    "cloakbrowser",
    "httpx",
    "patchright",
    "playwright",
    "praw",
    "requests",
    "scrapy",
    "selenium",
    "socket",
    "urllib",
    "webbrowser",
}


def test_reddit_consolidation_package_imports_without_capture_dependencies() -> None:
    module = importlib.import_module("source_capture.reddit_consolidation")

    assert hasattr(module, "consolidate_reddit_packet")


def test_reddit_consolidation_core_has_no_network_browser_or_capture_imports() -> None:
    project_root = Path(__file__).resolve().parents[2]
    target_paths = sorted((project_root / "source_capture" / "reddit_consolidation").glob("*.py"))
    target_paths.append(project_root / "runners" / "run_reddit_consolidation.py")

    offenders: dict[str, set[str]] = {}
    for path in target_paths:
        forbidden = _forbidden_import_roots(path)
        if forbidden:
            offenders[str(path)] = forbidden

    assert offenders == {}


def test_reddit_consolidation_is_not_imported_from_top_level_source_capture_module() -> None:
    project_root = Path(__file__).resolve().parents[2]
    top_level_source_files = [
        path
        for path in (project_root / "source_capture").glob("*.py")
        if path.name != "__init__.py"
    ]

    offenders = [
        path
        for path in top_level_source_files
        if "reddit_consolidation" in path.read_text(encoding="utf-8")
    ]

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
