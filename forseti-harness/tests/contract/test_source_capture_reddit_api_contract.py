from __future__ import annotations

import ast
from pathlib import Path


FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "archivebox",
    "bs4",
    "httpx",
    "playwright",
    "praw",
    "requests",
    "scrapy",
    "selenium",
    "webbrowser",
}


def test_reddit_api_adapter_avoids_sdk_browser_and_scraper_imports() -> None:
    project_root = Path(__file__).resolve().parents[2]
    target = project_root / "source_capture" / "adapters" / "reddit_api.py"
    assert target.exists(), f"reddit_api adapter missing: {target}"

    tree = ast.parse(target.read_text(encoding="utf-8"), filename=str(target))
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

    assert not forbidden, f"Forbidden import(s) in reddit_api.py: {sorted(forbidden)}"
