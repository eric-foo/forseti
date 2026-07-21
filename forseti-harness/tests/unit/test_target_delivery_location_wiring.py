from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from data_lake.root import DataLakeRoot
from runners import run_source_capture_cloakbrowser_packet as cloak_writer
from source_capture.adapters import target_delivery_location as target_location
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
from source_capture.adapters.target_delivery_location import (
    TargetDeliveryLocationPlugin,
    TargetGridPlugin,
    TargetSearchGridPlugin,
    confirm_target_us_delivery_zip,
)
from source_capture.retail_capture_profiles import (
    get_retail_capture_profile,
    target_bestseller_grid_url,
)


_TARGET_URL = "https://www.target.com/b/naturium/-/N-q643le8pm3h"


def _target_dom(
    *,
    shipping_zip: str = "10001",
    country: str = "US",
    server_zip: str = "52404",
    store_zip: str = "52404",
) -> str:
    server_location = json.dumps(
        {
            "zipCode": server_zip,
            "primaryStore": {
                "id": "1771",
                "storeName": "Cedar Rapids South",
                "zipCode": store_zip,
            },
            "location": {
                "zipCode": server_zip,
                "state": "IA",
                "country": country,
            },
        },
        separators=(",", ":"),
    )
    return f"""
<html><body>
<script>window.__TGT__ = {{"serverLocationVariables":{server_location}}};</script>
<button id="zip-code-id-btn" aria-label="Ship to location: {shipping_zip}">
  <span data-test="@web/ZipCodeButton/ZipCodeNumber">Ship to {shipping_zip}</span>
</button>
<h1>Naturium products at Target</h1><span>$14.69</span>
</body></html>
"""


class _Locator:
    def __init__(
        self,
        *,
        visible: bool = True,
        label: str | None = None,
        text: str = "",
        fail_click: bool = False,
    ) -> None:
        self.visible = visible
        self.label = label
        self.text = text
        self.fail_click = fail_click
        self.filled: str | None = None
        self.pressed: str | None = None
        self.clicked = False
        self.first = self
        self.child: _Locator | None = None

    def wait_for(self, **_kwargs: Any) -> None:
        if not self.visible:
            raise TimeoutError("not visible")

    def click(self, **_kwargs: Any) -> None:
        if self.fail_click:
            raise RuntimeError("click intercepted")
        self.clicked = True

    def fill(self, value: str, **_kwargs: Any) -> None:
        self.filled = value

    def press(self, key: str, **_kwargs: Any) -> None:
        self.pressed = key

    def get_attribute(self, name: str, **_kwargs: Any) -> str | None:
        return self.label if name == "aria-label" else None

    def inner_text(self, **_kwargs: Any) -> str:
        return self.text

    def locator(self, _selector: str) -> "_Locator":
        assert self.child is not None
        return self.child


class _Page:
    def __init__(
        self,
        *,
        control_visible: bool = True,
        control_click_fails: bool = False,
        apply_visible: bool = True,
    ) -> None:
        self.control = _Locator(
            visible=control_visible,
            label="Ship to location: 10001",
            fail_click=control_click_fails,
        )
        self.control.child = _Locator(text="Ship to 10001")
        self.zip_input = _Locator()
        self.apply = _Locator(visible=apply_visible)
        self.goto_calls: list[dict[str, object]] = []

    def goto(self, url: str, **kwargs: Any) -> None:
        self.goto_calls.append({"url": url, **kwargs})

    def locator(self, selector: str) -> _Locator:
        if selector == "#zip-code-id-btn":
            return self.control
        if selector in {
            'input[data-test="@web/LocationFlyout/FormInput"]:visible',
            'input[data-test="@web/ZipCodeInput/Input"]:visible',
        }:
            return self.zip_input
        if selector in {
            'button[data-test="@web/LocationFlyout/UpdateLocationButton"]:visible',
            'button[data-test="@web/ZipCodeInput/SubmitButton"]:visible',
        }:
            return self.apply
        return _Locator(visible=False)

    def wait_for_timeout(self, _milliseconds: float) -> None:
        return None


def test_plugin_waits_for_visible_control_and_applies_public_zip_flow() -> None:
    plugin = TargetDeliveryLocationPlugin(
        target_url=_TARGET_URL,
        delivery_zip="10001",
    )
    page = _Page()

    outcome = plugin.before(page, setup_timeout_ms=30_000)
    confirmation = plugin.confirm(_target_dom())

    assert outcome.steps_completed is True
    assert page.control.clicked is True
    assert page.zip_input.filled == "10001"
    assert page.apply.clicked is True
    assert confirmation.confirmed is True
    assert plugin.humanize is True
    assert plugin.setup_timeout_ms == 30_000


def test_plugin_types_readiness_and_click_failures_separately() -> None:
    readiness = TargetDeliveryLocationPlugin(_TARGET_URL, "10001").before(
        _Page(control_visible=False), setup_timeout_ms=30_000
    )
    click = TargetDeliveryLocationPlugin(_TARGET_URL, "10001").before(
        _Page(control_click_fails=True), setup_timeout_ms=30_000
    )

    assert readiness.reason == "wait_for_zip_control"
    assert click.reason == "open_zip_control"
    assert all(outcome.steps_completed is False for outcome in (readiness, click))


def test_plugin_fails_before_readiness_when_setup_budget_is_exhausted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monotonic_values = iter([100.0, 100.0, 100.001])
    monkeypatch.setattr(
        target_location.time,
        "monotonic",
        lambda: next(monotonic_values),
    )
    page = _Page()

    outcome = TargetDeliveryLocationPlugin(_TARGET_URL, "10001").before(
        page,
        setup_timeout_ms=1,
    )

    assert outcome.reason == "wait_for_zip_control"
    assert page.control.clicked is False
    assert float(page.goto_calls[0]["timeout"]) > 0


def test_plugin_never_turns_expired_budget_into_unbounded_click(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(target_location.time, "monotonic", lambda: clock[0])
    page = _Page()

    def exhaust_budget_after_readiness(**_kwargs: Any) -> None:
        clock[0] = 100.001

    page.control.wait_for = exhaust_budget_after_readiness  # type: ignore[method-assign]

    outcome = TargetDeliveryLocationPlugin(_TARGET_URL, "10001").before(
        page,
        setup_timeout_ms=1,
    )

    assert outcome.reason == "open_zip_control"
    assert page.control.clicked is False


def test_plugin_submits_scoped_zip_input_with_enter_when_action_label_drifts() -> None:
    plugin = TargetDeliveryLocationPlugin(_TARGET_URL, "10001")
    page = _Page(apply_visible=False)

    outcome = plugin.before(page, setup_timeout_ms=30_000)
    confirmation = plugin.confirm(_target_dom())

    assert outcome.steps_completed is True
    assert page.zip_input.pressed == "Enter"
    assert any("submitted" in warning for warning in outcome.warning_notes)
    assert confirmation.confirmed is True


def test_confirmation_allows_shipping_and_store_zip_separation() -> None:
    confirmation, context = confirm_target_us_delivery_zip(
        _target_dom(shipping_zip="10001", server_zip="52404", store_zip="52404"),
        delivery_zip="10001",
        setup_completed=True,
    )

    assert confirmation.confirmed is True
    assert context["target_server_location_zip"] == "52404"
    assert context["target_primary_store_zip"] == "52404"
    assert context["target_nested_location_country"] == "US"


class _GridLocator:
    def __init__(self, page: "_GridPage", kind: str) -> None:
        self.page = page
        self.kind = kind

    def inner_text(self, **_kwargs: Any) -> str:
        assert self.kind == "body"
        return f"{self.page.declared_count} results"

    def count(self) -> int:
        if self.kind == "pager":
            return 1
        assert self.kind == "next"
        return int(self.page.index + 1 < len(self.page.pages))

    def wait_for(self, **_kwargs: Any) -> None:
        if self.kind == "next" and self.count() == 0:
            raise TimeoutError("next page is not available")

    def scroll_into_view_if_needed(self, **_kwargs: Any) -> None:
        return None

    def click(self, **_kwargs: Any) -> None:
        assert self.count() == 1
        self.page.index += 1


class _GridMouse:
    def __init__(self, page: "_GridPage") -> None:
        self.page = page

    def wheel(self, delta_x: int, delta_y: int) -> None:
        assert delta_x == 0
        assert delta_y > 0
        self.page.scroll_steps.append(delta_y)


class _GridPage:
    def __init__(
        self, pages: list[list[str]], *, declared_count: int | list[int]
    ) -> None:
        self.pages = pages
        self.declared_counts = (
            [declared_count] * len(pages)
            if isinstance(declared_count, int)
            else declared_count
        )
        assert len(self.declared_counts) == len(pages)
        self.index = 0
        self.locator_selectors: list[str] = []
        self.scroll_steps: list[int] = []
        self.mouse = _GridMouse(self)

    @property
    def declared_count(self) -> int:
        return self.declared_counts[self.index]

    @property
    def url(self) -> str:
        return (
            "https://www.target.com/s?searchTerm=lip+mask&sortBy=bestselling"
            f"&moveTo=product-list-grid&Nao={self.index * 24}"
        )

    def content(self) -> str:
        cards = "".join(
            f'<div data-focusid="{product_id}_product_card"></div>'
            for product_id in self.pages[self.index]
        )
        return f"<html><body>{cards}</body></html>"

    def locator(self, selector: str) -> _GridLocator:
        self.locator_selectors.append(selector)
        if selector == "body":
            kind = "body"
        elif selector == '[data-test="listing-page-pagination"]':
            kind = "pager"
        else:
            kind = "next"
        return _GridLocator(self, kind)

    def wait_for_timeout(self, _milliseconds: float) -> None:
        return None


def test_target_search_grid_traverses_main_pager_and_reconciles_declared_count() -> None:
    plugin = TargetSearchGridPlugin(
        "https://www.target.com/s?searchTerm=lip%20mask",
        "10001",
    )
    page = _GridPage(
        [["10000001", "10000002"], ["10000002", "10000003"]],
        declared_count=4,
    )

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is True
    assert len(plugin.grid_page_doms) == 2
    assert page.scroll_steps == []
    assert '[data-test="listing-page-pagination"]' in page.locator_selectors
    assert any('aria-label="next page"' in value for value in page.locator_selectors)
    assert plugin.grid_observation == {
        "target_grid_page_load_count": 2,
        "target_grid_declared_result_count": 4,
        "target_grid_declared_result_count_observations": [4, 4],
        "target_grid_extracted_unique_parent_count": 3,
        "target_grid_extracted_placement_count": 4,
        "target_grid_duplicate_placement_count": 1,
        "target_grid_termination": "retailer_declared_count_reconciled",
        "target_grid_subject_kind": "search_query",
        "target_grid_subject": "lip mask",
        "target_grid_sort_order": "bestselling",
    }


def test_target_grid_uses_current_declared_count_and_preserves_count_drift() -> None:
    plugin = TargetSearchGridPlugin(
        "https://www.target.com/s?searchTerm=lip%20mask",
        "10001",
    )
    page = _GridPage(
        [["10000001", "10000002"], ["10000003"]],
        declared_count=[4, 3],
    )

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is True
    assert plugin.grid_observation["target_grid_declared_result_count"] == 3
    assert plugin.grid_observation[
        "target_grid_declared_result_count_observations"
    ] == [4, 3]
    assert plugin.grid_observation["target_grid_extracted_placement_count"] == 3


def test_target_brand_grid_defaults_to_bestseller_and_accepts_next_page_route() -> None:
    plugin = TargetGridPlugin(
        "https://www.target.com/b/e-l-f/-/N-5oajg?count=96&sortBy=newest",
        "10001",
    )

    assert plugin.target_url == (
        "https://www.target.com/b/e-l-f/-/N-5oajg?"
        "sortBy=bestselling&moveTo=product-list-grid"
    )
    assert target_bestseller_grid_url(plugin.target_url) == plugin.target_url


def test_target_catalog_grid_without_requested_zip_preserves_observed_context() -> None:
    plugin = TargetGridPlugin(
        "https://www.target.com/b/e-l-f/-/N-5oajg",
        require_delivery_pin=False,
    )

    confirmation = plugin.confirm(_target_dom())
    description = plugin.describe()

    assert confirmation.confirmed is False
    assert "no delivery ZIP was requested" in confirmation.detail
    assert description["delivery_zip_requested"] is None
    assert description["target_grid_location_binding"] == "unrequested"
    assert description["target_server_location_zip"] == "52404"


def test_target_search_grid_fails_when_pager_ends_before_declared_count() -> None:
    plugin = TargetSearchGridPlugin(
        "https://www.target.com/s?searchTerm=lip%20mask",
        "10001",
    )
    page = _GridPage([["10000001", "10000002"]], declared_count=3)

    outcome = plugin.before_snapshot(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is False
    assert outcome.reason == "next_page_control_unavailable"
    assert plugin.grid_observation["target_grid_termination"] == "unproven"


@pytest.mark.parametrize(
    ("dom", "setup_completed"),
    [
        (_target_dom(shipping_zip="10002"), True),
        (_target_dom(country="CA"), True),
        (_target_dom(), False),
        (
            _target_dom()
            + _target_dom(shipping_zip="10002", server_zip="10002", store_zip="10002"),
            True,
        ),
        ("<html><body>target.com $14.69 United States 10001</body></html>", True),
        (
            '<button id="zip-code-id-btn" aria-label="Ship to location: 10001">'
            '<span data-test="@web/ZipCodeButton/ZipCodeNumber">Ship to 10001</span>'
            '</button><script>{"serverLocationVariables":{broken}}</script>',
            True,
        ),
    ],
)
def test_confirmation_rejects_split_loose_or_malformed_signals(
    dom: str, setup_completed: bool
) -> None:
    confirmation, _context = confirm_target_us_delivery_zip(
        dom,
        delivery_zip="10001",
        setup_completed=setup_completed,
    )

    assert confirmation.confirmed is False


def test_confirmation_parses_target_escaped_bootstrap_state() -> None:
    bootstrap = json.dumps(
        {
            "serverLocationVariables": {
                "zipCode": "52404",
                "primaryStore": {
                    "storeName": "Cedar Rapids South",
                    "zipCode": "52404",
                },
                "location": {"zipCode": "52404", "country": "US"},
            }
        },
        separators=(",", ":"),
    )
    escaped = json.dumps(bootstrap)
    dom = (
        f"<script>deepFreeze(JSON.parse({escaped}))</script>"
        '<button id="zip-code-id-btn" aria-label="Ship to location: 10001">'
        '<span data-test="@web/ZipCodeButton/ZipCodeNumber">Ship to 10001</span>'
        "</button>"
    )

    confirmation, context = confirm_target_us_delivery_zip(
        dom,
        delivery_zip="10001",
        setup_completed=True,
    )

    assert confirmation.confirmed is True
    assert context["target_nested_location_country"] == "US"


def _fake_capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
    plugin = kwargs["pre_capture"]
    assert isinstance(plugin, TargetDeliveryLocationPlugin)
    plugin._setup_completed = True
    dom = _target_dom()
    confirmation = plugin.confirm(dom)
    return CloakBrowserSnapshotSuccess(
        requested_url=kwargs["url"],
        final_url=kwargs["url"],
        title="Naturium products at Target",
        rendered_dom=dom,
        visible_text="Naturium products at Target $14.69",
        screenshot_png=b"\x89PNG\r\n\x1a\n",
        metadata={
            "capture_timestamp": "2026-07-19T00:00:00Z",
            "pin_confirmed": confirmation.confirmed,
            **plugin.describe(),
        },
        warning_notes=[],
        limitation_notes=[],
    )


def _run_writer(tmp_path: Path, **overrides: Any) -> tuple[int, str]:
    kwargs: dict[str, Any] = {
        "url": _TARGET_URL,
        "source_family": "retail_pdp",
        "source_surface": "cloakbrowser_snapshot",
        "decision_question": "Does the bound Target page retain ZIP 10001?",
        "output_directory": tmp_path / "packet",
        "capture_context": "offline test",
        "operator_category": "test",
        "capture_mode": cloak_writer.CaptureModeCategory.MULTIMODAL,
        "session_id": None,
        "proxy_profile": None,
        "actor_audience_context": cloak_writer.unknown_with_reason("not needed"),
        "visible_mode_changes": [],
        "source_publication_or_event": cloak_writer.unknown_with_reason("not needed"),
        "source_edit_or_version": cloak_writer.unknown_with_reason("not needed"),
        "cutoff_posture": cloak_writer.unknown_with_reason("not needed"),
        "recapture_time": cloak_writer.not_applicable("not needed"),
        "re_capture_relationship": cloak_writer.not_applicable("not needed"),
        "warnings": [],
        "limitations": [],
        "timeout_seconds": 30,
        "wait_until": "domcontentloaded",
        "viewport_width": 1280,
        "viewport_height": 720,
        "max_artifact_bytes": 5_000_000,
        "block_heavy_assets": False,
        "target_zip": "10001",
    }
    kwargs.update(overrides)
    return cloak_writer.run_source_capture_cloakbrowser_packet(**kwargs)


def _target_grid_dom(
    products: list[tuple[str, str]], *, declared_count: int = 4
) -> str:
    cards = "".join(
        f"""
        <div data-focusid="{product_id}_product_card">
          <a data-test="content" href="/p/product-{product_id}/-/A-{product_id}">
            <span>$10.99</span><h3>{name}</h3>
            <div data-test="rating-stars"
                 aria-label="Average customer rating is 4.6 out of 5 stars with 145 reviews.">
            </div>
            <span>Shipping dates may vary</span>
          </a>
        </div>
        """
        for product_id, name in products
    )
    location = json.dumps(
        {
            "serverLocationVariables": {
                "zipCode": "52404",
                "primaryStore": {"storeName": "Cedar Rapids South", "zipCode": "52404"},
                "location": {"zipCode": "52404", "country": "US"},
            }
        },
        separators=(",", ":"),
    )
    return f"""
    <html><head><title>"lip mask" : Target</title></head><body>
      <script>window.__TGT__ = {location}; window.guest = {{"accessToken":"secret"}};</script>
      <button id="zip-code-id-btn" aria-label="Ship to location: 10001">
        <span data-test="@web/ZipCodeButton/ZipCodeNumber">Ship to 10001</span>
      </button>
      <div>{declared_count} results</div>{cards}
    </body></html>
    """


def _fake_target_grid_capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
    plugin = kwargs["pre_capture"]
    assert isinstance(plugin, TargetSearchGridPlugin)
    pages = [
        _target_grid_dom([("10000001", "First"), ("10000002", "Second")]),
        _target_grid_dom([("10000002", "Second"), ("10000003", "Third")]),
    ]
    plugin._setup_completed = True
    plugin._grid_page_doms = pages
    plugin._grid_page_urls = [
        "https://www.target.com/s?searchTerm=lip+mask&sortBy=bestselling"
        "&moveTo=product-list-grid",
        "https://www.target.com/s?searchTerm=lip+mask&sortBy=bestselling"
        "&moveTo=product-list-grid&Nao=24",
    ]
    plugin._grid_observation = {
        "target_grid_page_load_count": 2,
        "target_grid_declared_result_count": 4,
        "target_grid_extracted_unique_parent_count": 3,
        "target_grid_extracted_placement_count": 4,
        "target_grid_duplicate_placement_count": 1,
        "target_grid_termination": "retailer_declared_count_reconciled",
        "target_grid_subject_kind": "search_query",
        "target_grid_subject": "lip mask",
        "target_grid_sort_order": "bestselling",
    }
    confirmation = plugin.confirm(pages[-1])
    return CloakBrowserSnapshotSuccess(
        requested_url=kwargs["url"],
        final_url=plugin._grid_page_urls[-1],
        title='"lip mask" : Target',
        rendered_dom=pages[-1],
        visible_text="lip mask 3 results $10.99",
        screenshot_png=b"\x89PNG\r\n\x1a\n",
        metadata={
            "capture_timestamp": "2026-07-22T00:00:00Z",
            "pin_confirmed": confirmation.confirmed,
            "before_snapshot_attempted": True,
            "before_snapshot_steps_completed": True,
            "before_snapshot_reason": None,
            **plugin.describe(),
        },
        warning_notes=[],
        limitation_notes=[],
    )


def test_target_grid_runner_writes_sanitized_content_and_local_projection(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_target_grid_capture
    )
    projection_path = tmp_path / "target-grid.json"

    exit_code, message = _run_writer(
        tmp_path,
        url="https://www.target.com/s?searchTerm=lip%20mask",
        retail_capture_profile=get_retail_capture_profile("target_grid_aggregate"),
        retail_grid_projection_output=projection_path,
    )

    assert exit_code == 0
    packet_path = Path(
        message.split(";", 1)[0].removeprefix("raw packet preserved at ")
    )
    manifest = json.loads((packet_path / "manifest.json").read_text())
    stored_text = "\n".join(
        path.read_text(errors="ignore")
        for path in (packet_path / "raw").iterdir()
        if path.suffix != ".png"
    )
    assert "accessToken" not in stored_text
    assert all(
        item["relative_packet_path"] != "raw/01_cloakbrowser_rendered_dom.html"
        for item in manifest["preserved_files"]
    )
    projection = json.loads(projection_path.read_text())
    assert projection["completeness"] == {
        "duplicate_placement_count": 1,
        "extracted_placement_count": 4,
        "extracted_unique_parent_count": 3,
        "page_declared_result_count": 4,
        "residuals": [],
        "status": "complete",
        "subject_binding_confirmed": True,
        "termination": "retailer_visible_count_reconciled",
    }


def test_target_grid_runner_files_projection_into_test_lake(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(
        cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_target_grid_capture
    )
    root = DataLakeRoot.for_test(tmp_path / "lake")

    exit_code, message = _run_writer(
        tmp_path,
        url="https://www.target.com/s?searchTerm=lip%20mask",
        output_directory=None,
        data_root=root,
        retail_capture_profile=get_retail_capture_profile("target_grid_aggregate"),
        retail_grid_projection_output=None,
        target_zip=None,
    )

    assert exit_code == 0
    packet_path = Path(
        message.split(";", 1)[0].removeprefix("raw packet preserved at ")
    )
    packet_id = json.loads((packet_path / "manifest.json").read_text())["packet_id"]
    loaded = root.load_raw_packet(packet_id)
    assert loaded.manifest["packet_id"] == packet_id
    projection_paths = list(root.path.rglob("projection_retail_grid/*.json"))
    assert len(projection_paths) == 1
    assert json.loads(projection_paths[0].read_text())["completeness"]["status"] == (
        "complete"
    )


def test_writer_builds_target_plugin_and_accepts_exact_target_host(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_capture)

    exit_code, output = _run_writer(tmp_path)

    assert exit_code == 0
    assert output == str(tmp_path / "packet")


def test_writer_rejects_target_flag_for_non_target_url(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="requires a target.com"):
        _run_writer(tmp_path, url="https://www.target.sg/example")


def test_target_pin_enforcement_requires_true_boolean_and_target_host() -> None:
    assert (
        cloak_writer._target_delivery_pin_failure(
            target_zip="10001",
            final_url=_TARGET_URL,
            pin_confirmed=True,
        )
        is None
    )
    assert "not target.com" in (
        cloak_writer._target_delivery_pin_failure(
            target_zip="10001",
            final_url="https://www.target.sg/example",
            pin_confirmed=True,
        )
        or ""
    )
    assert "not confirmed" in (
        cloak_writer._target_delivery_pin_failure(
            target_zip="10001",
            final_url=_TARGET_URL,
            pin_confirmed=1,
        )
        or ""
    )


def test_writer_preserves_but_rejects_unconfirmed_target_pin(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def _unconfirmed_capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
        result = _fake_capture(**kwargs)
        result.metadata["pin_confirmed"] = False
        return result

    monkeypatch.setattr(
        cloak_writer, "fetch_cloakbrowser_snapshot_capture", _unconfirmed_capture
    )

    exit_code, message = _run_writer(tmp_path)

    assert exit_code == cloak_writer.SOURCE_DETAIL_SUFFICIENCY_EXIT_CODE
    assert cloak_writer.TARGET_DELIVERY_PIN_FAILURE_MODE_CHANGE in message
    manifest = json.loads(
        (tmp_path / "packet" / "manifest.json").read_text(encoding="utf-8")
    )
    assert cloak_writer.TARGET_DELIVERY_PIN_FAILURE_MODE_CHANGE in manifest[
        "visible_mode_changes"
    ]
    assert any(
        "MUST NOT be admitted as Target US delivery-pinned evidence" in limitation
        for limitation in manifest["limitations"]
    )
