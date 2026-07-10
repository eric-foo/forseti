from __future__ import annotations

from source_capture.adapters.cloakbrowser_snapshot import (
    ScrollStopCondition,
    _CloakBrowserSnapshotEngine,
)


class _TickClock:
    def __init__(self) -> None:
        self.value = 0

    def __call__(self) -> int:
        self.value += 1_000_000
        return self.value


def test_live_engine_emits_versioned_monotonic_phase_and_action_timings(monkeypatch) -> None:
    class BodyLocator:
        def inner_text(self, *, timeout: float) -> str:
            return "product reviews"

    class LoadMoreLocator:
        @property
        def first(self):
            return self

        def count(self) -> int:
            return 1

        def click(self, *, timeout: float) -> None:
            return None

    class Page:
        url = "https://example.com/product"

        def goto(self, url: str, **kwargs: object) -> None:
            return None

        def wait_for_timeout(self, ms: float) -> None:
            return None

        def evaluate(self, script: str, value: int | None = None):
            if "scrollHeight" in script and "scrollTo" not in script:
                return 100
            return None

        def content(self) -> str:
            return "<html><body>product reviews</body></html>"

        def locator(self, selector: str):
            return BodyLocator() if selector == "body" else LoadMoreLocator()

        def screenshot(self, **kwargs: object) -> bytes:
            return b"\x89PNG\r\n\x1a\n"

        def title(self) -> str:
            return "Product"

    class Context:
        def new_page(self) -> Page:
            return Page()

        def close(self) -> None:
            return None

    class Browser:
        def new_context(self, **kwargs: object) -> Context:
            return Context()

        def close(self) -> None:
            return None

    class CloakBrowser:
        def launch(self, **kwargs: object) -> Browser:
            return Browser()

    monkeypatch.setattr(
        "source_capture.adapters.cloakbrowser_snapshot.import_module",
        lambda name: CloakBrowser(),
    )

    result = _CloakBrowserSnapshotEngine(clock_ns=_TickClock()).capture(
        url="https://example.com/product",
        timeout_seconds=5,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        proxy_profile=None,
        block_heavy_assets=False,
        settle_seconds=1,
        scroll_step_px=100,
        scroll_passes=1,
        load_more_selector="text=Show more",
        load_more_clicks=1,
    )

    timing = result.capture_phase_timing
    assert timing["schema_version"] == 1
    assert timing["measurement_status"] == "measured"
    assert timing["clock"] == "monotonic"
    assert timing["unit"] == "milliseconds"
    assert timing["total_capture_wall_ms"] > 0
    assert set(timing["phases_ms"]) == {
        "dependency_import_browser_launch",
        "context_creation",
        "page_creation",
        "asset_route_setup",
        "pre_capture_plugin",
        "navigation_wait_until",
        "configured_settle",
        "dom_serialization",
        "visible_text_extraction",
        "screenshot",
        "context_browser_close",
    }
    assert timing["progressive_scroll_steps"] == [
        {"index": 1, "action_ms": 1.0, "post_action_settle_ms": 1.0}
    ]
    assert timing["scroll_passes"] == [
        {"index": 1, "action_ms": 1.0, "post_action_settle_ms": 1.0}
    ]
    assert timing["load_more_actions"] == [
        {"index": 1, "action_ms": 1.0, "post_action_settle_ms": 1.0}
    ]


def test_live_engine_stops_remaining_scrolls_only_after_generic_condition_is_reached(
    monkeypatch,
) -> None:
    state = {"scrolls": 0}

    class Locator:
        def inner_text(self, *, timeout: float) -> str:
            if state["scrolls"] >= 2:
                return "Product Ratings & Reviews (10) Color: Red $12.00"
            return "Product Color: Red $12.00"

    class Page:
        url = "https://example.com/product"

        def goto(self, url: str, **kwargs: object) -> None:
            return None

        def wait_for_timeout(self, ms: float) -> None:
            return None

        def evaluate(self, script: str, value: int | None = None):
            if "scrollHeight" in script and "scrollTo" not in script:
                return 10_000
            if "scrollTo" in script:
                state["scrolls"] += 1
            return None

        def content(self) -> str:
            return "<html><body>Product Ratings & Reviews (10)</body></html>"

        def locator(self, selector: str) -> Locator:
            return Locator()

        def screenshot(self, **kwargs: object) -> bytes:
            return b"\x89PNG\r\n\x1a\n"

        def title(self) -> str:
            return "Product"

    class Context:
        def new_page(self) -> Page:
            return Page()

        def close(self) -> None:
            return None

    class Browser:
        def new_context(self, **kwargs: object) -> Context:
            return Context()

        def close(self) -> None:
            return None

    class CloakBrowser:
        def launch(self, **kwargs: object) -> Browser:
            return Browser()

    monkeypatch.setattr(
        "source_capture.adapters.cloakbrowser_snapshot.import_module",
        lambda name: CloakBrowser(),
    )

    result = _CloakBrowserSnapshotEngine(clock_ns=_TickClock()).capture(
        url="https://example.com/product",
        timeout_seconds=5,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        proxy_profile=None,
        block_heavy_assets=False,
        scroll_step_px=350,
        scroll_passes=1,
        scroll_stop_condition=ScrollStopCondition(
            visible_text_contains=("Ratings & Reviews", "Color:"),
            visible_text_regexes=(r"Ratings & Reviews \([^)]+\)", r"\$\d+\.\d{2}"),
        ),
    )

    timing = result.capture_phase_timing
    assert state["scrolls"] == 2
    assert len(timing["progressive_scroll_steps"]) == 2
    assert timing["scroll_passes"] == []
    assert timing["scroll_stop_condition"]["reached"] is True
    assert timing["scroll_stop_condition"]["reached_stage"] == "progressive_scroll"
    assert timing["scroll_stop_condition"]["checks"][-1]["reached"] is True
