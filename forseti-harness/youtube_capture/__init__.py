"""YouTube stealth public-data capture package.

Modules: stealth_client (Chrome TLS/JA3 costume), capture_youtube_v0 (watch/metadata capture),
shorts_scroll_capture_v0, behavioral_projection, enrich_ryd_v0, verify_fingerprint_v0.

An explicit package marker so the built wheel ships this package: `setuptools` `packages.find`
skips a bare namespace directory (no `__init__.py`), which previously dropped `youtube_capture`
from a non-editable `pip install .` and raised ModuleNotFoundError in the runners that import it.
"""
