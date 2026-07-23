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


def test_direct_http_adapter_avoids_browser_api_and_scraper_imports() -> None:
    project_root = Path(__file__).resolve().parents[2]
    target_paths = [
        project_root / "source_capture" / "adapters" / "__init__.py",
        project_root / "source_capture" / "adapters" / "direct_http.py",
        project_root / "source_capture" / "access_gate.py",
        project_root / "runners" / "run_source_capture_http_packet.py",
    ]

    for path in target_paths:
        assert path.exists(), f"direct HTTP path missing: {path}"
        assert not _forbidden_import_roots(path), f"Forbidden import in {path}"


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
