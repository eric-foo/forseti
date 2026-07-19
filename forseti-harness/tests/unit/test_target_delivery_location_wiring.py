from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from runners import run_source_capture_cloakbrowser_packet as cloak_writer
from source_capture.adapters import target_delivery_location as target_location
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
from source_capture.adapters.target_delivery_location import (
    TargetDeliveryLocationPlugin,
    confirm_target_us_delivery_zip,
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
        if selector == 'input[data-test="@web/ZipCodeInput/Input"]:visible':
            return self.zip_input
        if selector == 'button[data-test="@web/ZipCodeInput/SubmitButton"]:visible':
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


def test_writer_rejects_target_plus_other_site_preference(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="only one site-specific pre-capture"):
        _run_writer(tmp_path, sephora_market="US")


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
