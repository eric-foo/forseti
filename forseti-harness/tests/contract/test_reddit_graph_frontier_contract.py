from __future__ import annotations

import ast
import importlib
from pathlib import Path


FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "bs4",
    "cloakbrowser",
    "ftplib",
    "http",
    "httpx",
    "patchright",
    "playwright",
    "praw",
    "pycurl",
    "requests",
    "scrapy",
    "selenium",
    "socket",
    "source_capture",
    "subprocess",
    "urllib",
    "webbrowser",
    "websocket",
    "websockets",
}


def test_reddit_graph_frontier_imports_without_capture_dependencies() -> None:
    module = importlib.import_module("capture_spine.reddit_graph_frontier")

    assert hasattr(module, "build_graph_frontier_register")
    assert hasattr(module, "prepare_next_bounded_run_envelope")


def test_reddit_graph_frontier_has_no_network_browser_or_armory_imports() -> None:
    project_root = Path(__file__).resolve().parents[2]
    target_paths = sorted((project_root / "capture_spine" / "reddit_graph_frontier").glob("*.py"))

    offenders: dict[str, set[str]] = {}
    for path in target_paths:
        forbidden = _forbidden_import_roots(path)
        if forbidden:
            offenders[str(path)] = forbidden

    assert offenders == {}


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
