from __future__ import annotations

import ast
from pathlib import Path


# Mirrors the archive_org contract test: the publisher-history rungs must fetch ONLY through the
# shared direct_http adapter, never an HTTP/browser/api-client/scraper/archive package. urllib is
# also forbidden directly -- HTTP belongs behind fetch_direct_http_capture.
FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "archivebox",
    "bs4",
    "httpx",
    "internetarchive",
    "playwright",
    "praw",
    "pygithub",
    "github",
    "requests",
    "scrapy",
    "selenium",
    "urllib3",
    "waybackpy",
    "webbrowser",
}

# urllib.request is the transport stdlib the adapter must NOT reach for; selection-only urllib.parse
# helpers (urlencode/quote/urlparse) stay allowed.
FORBIDDEN_IMPORT_MODULES = {"urllib.request"}


def test_publisher_history_adapter_avoids_transport_browser_api_and_scraper_imports() -> None:
    project_root = Path(__file__).resolve().parents[2]
    target_paths = [
        project_root / "source_capture" / "adapters" / "__init__.py",
        project_root / "source_capture" / "adapters" / "publisher_history.py",
    ]

    for path in target_paths:
        assert path.exists(), f"publisher history path missing: {path}"
        assert not _forbidden_import_roots(path), f"Forbidden import root in {path}"
        assert not _forbidden_import_modules(path), f"Forbidden import module in {path}"


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


def _forbidden_import_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    forbidden: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            forbidden.update(
                alias.name for alias in node.names if alias.name in FORBIDDEN_IMPORT_MODULES
            )
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module in FORBIDDEN_IMPORT_MODULES:
                forbidden.add(node.module)
    return forbidden
