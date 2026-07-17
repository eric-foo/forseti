"""Offline tests for the US-storefront pin capability (--delivery-zip via the plugin seam).

Covers:
  - The allowlist entries in the cadence runner so --delivery-zip and its bounded setup-timeout
    flag can be passed via --writer-arg.
  - The CloakBrowser adapter's generic pre_capture plugin seam (de-Amazoned generic adapter).
  - The Amazon delivery-location plugin: honest CONFIRMED vs ATTEMPTED-but-NOT-confirmed notes
    (the honesty keystone), pin_confirmed metadata, and the apply-failed Return-fallback warning.
  - The writer CLI accepting --delivery-zip + --delivery-zip-setup-timeout-seconds and building
    the plugin.
  - End-to-end: runner --writer-arg=--delivery-zip value reaches the writer.
  - The generic adapter contains no Amazon strings.

All tests are offline: no live browser, network, or cloakbrowser runtime is required.
INV-1: observed facts only; a pin is recorded only when CONFIRMED in the rendered DOM.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable
from unittest.mock import MagicMock

import pytest

from runners import run_source_capture_cloakbrowser_packet as cloak_writer
from runners import run_source_capture_durability_series as series_runner
from runners.run_source_capture_durability_series import _WRITER_ARG_KNOB_ALLOWLIST
from source_capture.adapters import amazon_delivery_location as amazon_pin
from source_capture.adapters.amazon_delivery_location import (
    _AMAZON_HOMEPAGE_URL,
    AmazonDeliveryLocationPlugin,
    confirm_us_storefront,
    confirm_us_storefront_with_zip,
)
from source_capture.adapters.cloakbrowser_snapshot import (
    CloakBrowserSnapshotSuccess,
    PinConfirmation,
    PreCaptureOutcome,
    fetch_cloakbrowser_snapshot_capture,
)


_US_DOM = '<html><body><input name="currencyOfPreference" value="USD"></body></html>'
_US_DOM_REORDERED = "<html><body><input value='USD' type='hidden' name='currencyOfPreference'></body></html>"
_US_ZIP_DOM = """
<html><body>
<script>ue_sn = 'www.amazon.com'</script>
<span id="glow-ingress-line2">New York 10001</span>
<input name="currencyOfPreference" value="USD">
</body></html>
"""
_NON_US_DOM = "<html><body><span>S$45.00</span></body></html>"


def _fake_capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
    """Offline substitute for fetch_cloakbrowser_snapshot_capture; honors the pre_capture seam."""
    url = str(kwargs.get("url", "https://example.com/"))
    pre_capture = kwargs.get("pre_capture")
    rendered_dom = _US_ZIP_DOM
    limitation_notes = []
    pin_confirmed = None
    metadata: dict[str, Any] = {
        "capture_timestamp": "2026-06-16T00:00:00Z",
        "requested_url": url,
    }
    if pre_capture is not None:
        outcome = PreCaptureOutcome(attempted=True, steps_completed=True, reason=None)
        confirmation = pre_capture.confirm(rendered_dom)
        pin_confirmed = confirmation.confirmed
        limitation_notes.append(pre_capture.note(outcome, confirmation))
        metadata.update(pre_capture.describe())
        metadata["humanize_mode_active"] = pre_capture.humanize
    metadata["pin_confirmed"] = pin_confirmed
    return CloakBrowserSnapshotSuccess(
        requested_url=url,
        final_url=url,
        title="Product Page",
        rendered_dom=rendered_dom,
        visible_text="USD price",
        screenshot_png=b"\x89PNG\r\n\x1a\n",
        metadata=metadata,
        warning_notes=[],
        limitation_notes=limitation_notes,
    )


# ── Allowlist tests ────────────────────────────────────────────────────────────

def test_delivery_zip_in_runner_allowlist() -> None:
    """--delivery-zip must be in the cadence runner allowlist so the operator can pass it
    per-slot via --writer-arg without triggering the default-deny guard."""
    assert "--delivery-zip" in _WRITER_ARG_KNOB_ALLOWLIST


def test_delivery_zip_setup_timeout_in_runner_allowlist() -> None:
    """FIX #1: the bounded pre-capture setup-timeout flag must also be allowlisted."""
    assert "--delivery-zip-setup-timeout-seconds" in _WRITER_ARG_KNOB_ALLOWLIST


def test_allowlist_still_excludes_proxy_and_identity_flags() -> None:
    """Regression: adding the delivery-zip knobs must not inadvertently add proxy/identity flags."""
    for forbidden in ("--proxy-profile-label", "--url", "--series-id", "--output",
                      "--preflight-only", "--guarded-reddit-launch"):
        assert forbidden not in _WRITER_ARG_KNOB_ALLOWLIST, (
            f"allowlist should not contain {forbidden}"
        )


# ── Generic adapter is de-Amazoned ──────────────────────────────────────────────

def test_generic_adapter_has_no_amazon_strings() -> None:
    """FIX #6: the generic adapter must contain NO Amazon delivery-location widget code.

    Scoped to the delivery-location widget concern (selectors, homepage URL, setter,
    metadata). The block-detector's ``amazon_continue_shopping_interstitial`` signal is a
    separate, already-merged concern (PR #161) and is intentionally NOT covered here.
    """
    adapter_path = (
        Path(__file__).resolve().parents[2]
        / "source_capture"
        / "adapters"
        / "cloakbrowser_snapshot.py"
    )
    source = adapter_path.read_text(encoding="utf-8").lower()
    for forbidden in (
        "glux",
        "glow",
        "nav-global",
        "_set_delivery_location",
        "_amazon_homepage_url",
        "delivery_zip_requested",
    ):
        assert forbidden not in source, f"generic adapter must not contain {forbidden!r}"


# ── confirm_us_storefront (the post-capture source of truth) ────────────────────

def test_confirm_us_storefront_confirms_on_usd_currency_signal() -> None:
    confirmation = confirm_us_storefront(_US_DOM)
    assert confirmation.confirmed is True
    assert "currencyOfPreference" in confirmation.detail


def test_confirm_us_storefront_confirms_on_usd_currency_signal_attribute_order() -> None:
    confirmation = confirm_us_storefront(_US_DOM_REORDERED)
    assert confirmation.confirmed is True
    assert "currencyOfPreference" in confirmation.detail


def test_confirm_us_storefront_not_confirmed_on_singapore_price() -> None:
    confirmation = confirm_us_storefront(_NON_US_DOM)
    assert confirmation.confirmed is False
    assert "currencyOfPreference" in confirmation.detail


def test_confirm_us_storefront_not_confirmed_when_no_signal() -> None:
    confirmation = confirm_us_storefront("<html><body>no prices here</body></html>")
    assert confirmation.confirmed is False
    assert "no US storefront signal" in confirmation.detail


def test_confirm_us_storefront_not_confirmed_on_bare_dollar_from_page_js() -> None:
    """Tightening: a bare '$' from page JS (e.g. jQuery) with no US price PATTERN and no
    currencyOfPreference signal must NOT confirm. The prior '$' in dom heuristic false-positived."""
    dom = "<html><body><script>$(function(){var s='$';});</script>no price shown</body></html>"
    confirmation = confirm_us_storefront(dom)
    assert confirmation.confirmed is False


def test_confirm_us_storefront_not_confirmed_on_us_price_pattern_without_currency_signal() -> None:
    """A dollar-looking price alone is not proof the storefront flipped to US."""
    dom = "<html><body><span class='a-offscreen'>$24.99</span></body></html>"
    confirmation = confirm_us_storefront(dom)
    assert confirmation.confirmed is False
    assert "currencyOfPreference" in confirmation.detail


@pytest.mark.parametrize("price", ["C$24.99", "A$24.99", "HK$24.99", "NZ$24.99"])
def test_confirm_us_storefront_not_confirmed_on_prefixed_currency_without_currency_signal(
    price: str,
) -> None:
    confirmation = confirm_us_storefront(f"<html><body><span>{price}</span></body></html>")
    assert confirmation.confirmed is False
    assert "currencyOfPreference" in confirmation.detail


def test_confirm_us_storefront_with_zip_confirms_grid_surface() -> None:
    dom = """
<html lang="en-us"><body>
<script>ue_sn = 'www.amazon.com'</script>
<span id="glow-ingress-line2">New York 10001</span>
</body></html>
"""
    confirmation = confirm_us_storefront_with_zip(dom, delivery_zip="10001")

    assert confirmation.confirmed is True
    assert "delivery ZIP '10001'" in confirmation.detail


def test_confirm_us_storefront_with_zip_rejects_currency_only() -> None:
    confirmation = confirm_us_storefront_with_zip(_US_DOM, delivery_zip="10001")

    assert confirmation.confirmed is False
    assert "requested delivery ZIP '10001'" in confirmation.detail


def test_confirm_us_storefront_with_zip_rejects_zip_outside_location_anchor() -> None:
    dom = """
<html><body>
<script>ue_sn = 'www.amazon.com'; var unrelated = '10001';</script>
<span id="glow-ingress-line2">Singapore</span>
</body></html>
"""
    confirmation = confirm_us_storefront_with_zip(dom, delivery_zip="10001")

    assert confirmation.confirmed is False


def test_confirm_us_storefront_with_zip_rejects_non_us_marketplace() -> None:
    dom = """
<html><body>
<script>ue_sn = 'www.amazon.sg'</script>
<span id="glow-ingress-line2">New York 10001</span>
</body></html>
"""
    confirmation = confirm_us_storefront_with_zip(dom, delivery_zip="10001")

    assert confirmation.confirmed is False


# ── The honesty keystone: note(...) ─────────────────────────────────────────────

def test_plugin_note_confirmed_says_set_and_confirmed() -> None:
    """When confirm() is True the note may assert the storefront was set AND confirmed."""
    plugin = AmazonDeliveryLocationPlugin(delivery_zip="10001")
    outcome = PreCaptureOutcome(attempted=True, steps_completed=True, reason=None)
    note = plugin.note(outcome, PinConfirmation(confirmed=True, detail="USD observed"))
    assert "set to '10001'" in note
    assert "CONFIRMED" in note
    assert "USD observed" in note


def test_plugin_note_not_confirmed_never_claims_set() -> None:
    """KEYSTONE: when confirm() is False the note must say ATTEMPTED ... NOT confirmed and
    must NEVER assert the storefront was 'set' or 'pinned'."""
    plugin = AmazonDeliveryLocationPlugin(delivery_zip="10001")
    outcome = PreCaptureOutcome(attempted=True, steps_completed=True, reason=None)
    note = plugin.note(
        outcome,
        PinConfirmation(confirmed=False, detail="no US storefront signal in rendered DOM"),
    )
    assert "ATTEMPTED" in note
    assert "NOT confirmed" in note
    assert "treat as un-pinned" in note
    # Must not falsely assert success.
    assert "set to" not in note
    assert "and CONFIRMED" not in note


def test_plugin_note_failed_step_surfaces_reason() -> None:
    """When a widget step failed, the un-confirmed note surfaces the first failed step."""
    plugin = AmazonDeliveryLocationPlugin(delivery_zip="10001")
    outcome = PreCaptureOutcome(attempted=True, steps_completed=False, reason="apply")
    note = plugin.note(
        outcome,
        PinConfirmation(confirmed=False, detail="no US storefront signal"),
    )
    assert "ATTEMPTED" in note
    assert "widget step failed: apply" in note
    assert "set to" not in note


# ── before(): widget flow outcome (FIX #3 + #4) ─────────────────────────────────

class _FakePage:
    """A scriptable fake Playwright page. ``fail_steps`` names steps that should error."""

    def __init__(
        self,
        fail_steps: set[str] | None = None,
        apply_button_missing: bool = False,
        apply_confirmation_missing: bool = False,
        clock_advance: Callable[[float], None] | None = None,
        action_advance_ms: float = 0,
        homepage_url: str = _AMAZON_HOMEPAGE_URL,
    ):
        self.fail_steps = fail_steps or set()
        self.apply_button_missing = apply_button_missing
        self.apply_confirmation_missing = apply_confirmation_missing
        self._clock_advance = clock_advance
        self._action_advance_ms = action_advance_ms
        self.calls: list[str] = []
        self.click_timeouts: list[float] = []
        self.return_pressed = False
        self.filled_zip: str | None = None
        self.applied = False
        self.goto_wait_until: str | None = None
        self.url = homepage_url

    def goto(self, url: str, **kwargs: Any) -> None:
        self.calls.append(f"goto:{url}")
        self.goto_wait_until = kwargs.get("wait_until")
        self._advance_action()
        if "homepage" in self.fail_steps:
            raise RuntimeError("nav failed")

    def _advance_action(self) -> None:
        if self._clock_advance is not None and self._action_advance_ms > 0:
            self._clock_advance(self._action_advance_ms)

    def wait_for_timeout(self, ms: float) -> None:
        self.calls.append("wait")
        if self._clock_advance is not None:
            self._clock_advance(ms)

    def locator(self, selector: str) -> "_FakeLocator":
        return _FakeLocator(self, selector)

    @property
    def keyboard(self) -> "_FakeKeyboard":
        return _FakeKeyboard(self)


class _FakeLocator:
    def __init__(self, page: _FakePage, selector: str):
        self._page = page
        self._selector = selector

    @property
    def first(self) -> "_FakeLocator":
        return self

    def click(self, *, timeout: float) -> None:
        self._page.click_timeouts.append(timeout)
        self._page._advance_action()
        # Widget-open selectors
        if self._selector in ("#nav-global-location-popover-link", "#glow-ingress-block"):
            if "open_widget" in self._page.fail_steps:
                raise RuntimeError("widget not clickable")
            self._page.calls.append("open_widget")
            return
        # Apply selectors
        if self._page.apply_button_missing or "apply" in self._page.fail_steps:
            raise RuntimeError("apply button not present")
        self._page.calls.append("apply")
        self._page.applied = True

    def fill(self, value: str, *, timeout: float) -> None:
        self._page.click_timeouts.append(timeout)
        self._page._advance_action()
        if "fill_zip" in self._page.fail_steps:
            raise RuntimeError("zip input not present")
        self._page.filled_zip = value
        self._page.calls.append(f"fill:{value}")

    def inner_text(self, *, timeout: float) -> str:
        if (
            self._selector == "body"
            and self._page.applied
            and not self._page.apply_confirmation_missing
        ):
            return f"Deliver to New York {self._page.filled_zip}"
        return ""


class _FakeKeyboard:
    def __init__(self, page: _FakePage):
        self._page = page

    def press(self, key: str) -> None:
        self._page.return_pressed = True
        self._page.calls.append(f"press:{key}")


def test_plugin_before_all_steps_succeed() -> None:
    plugin = AmazonDeliveryLocationPlugin(delivery_zip="10001")
    page = _FakePage()
    outcome = plugin.before(page, setup_timeout_ms=30_000)
    assert outcome.attempted is True
    assert outcome.steps_completed is True
    assert outcome.reason is None
    assert f"goto:{_AMAZON_HOMEPAGE_URL}" in page.calls
    assert "open_widget" in page.calls
    assert "fill:10001" in page.calls
    assert "apply" in page.calls
    assert page.goto_wait_until == "domcontentloaded"
    assert "wait" not in page.calls


def test_plugin_before_warns_when_apply_confirmation_does_not_arrive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = {"now": 0.0}

    def _now() -> float:
        return clock["now"]

    def _advance(ms: float) -> None:
        clock["now"] += ms / 1000

    monkeypatch.setattr(amazon_pin.time, "monotonic", _now)
    plugin = AmazonDeliveryLocationPlugin(delivery_zip="10001")
    page = _FakePage(
        apply_confirmation_missing=True,
        clock_advance=_advance,
    )

    outcome = plugin.before(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is True
    assert "wait" in page.calls
    assert any(
        "requested ZIP was not observed" in warning for warning in outcome.warning_notes
    )


def test_plugin_before_uses_short_probe_timeout_not_8000ms() -> None:
    """FIX #4: widget probes use the SHORT 2.5s probe timeout, never the old 8000ms."""
    plugin = AmazonDeliveryLocationPlugin(delivery_zip="10001")
    page = _FakePage()
    plugin.before(page, setup_timeout_ms=30_000)
    assert page.click_timeouts, "widget steps should have probed with a timeout"
    assert all(t == 2500 for t in page.click_timeouts), page.click_timeouts
    assert 8000 not in page.click_timeouts


def test_plugin_before_uses_setup_timeout_as_shared_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    """FIX #1: setup timeout is a shared pre-capture budget, not reset per widget step."""
    clock = {"now": 0.0}

    def _now() -> float:
        return clock["now"]

    def _advance(ms: float) -> None:
        clock["now"] += ms / 1000

    monkeypatch.setattr(amazon_pin.time, "monotonic", _now)
    plugin = AmazonDeliveryLocationPlugin(delivery_zip="10001")
    page = _FakePage(clock_advance=_advance, action_advance_ms=1_500)

    outcome = plugin.before(page, setup_timeout_ms=2_000)

    assert outcome.steps_completed is False
    assert outcome.reason == "fill_zip"
    assert page.click_timeouts == [500]


def test_plugin_rejects_non_positive_setup_timeout() -> None:
    with pytest.raises(ValueError, match="delivery_zip_setup_timeout_seconds"):
        AmazonDeliveryLocationPlugin(delivery_zip="10001", setup_timeout_seconds=0)


def test_plugin_before_homepage_failure_is_first_failed_step() -> None:
    plugin = AmazonDeliveryLocationPlugin(delivery_zip="10001")
    page = _FakePage(fail_steps={"homepage"})
    outcome = plugin.before(page, setup_timeout_ms=30_000)
    assert outcome.steps_completed is False
    assert outcome.reason == "homepage_navigation"
    assert any("homepage navigation failed" in w for w in outcome.warning_notes)


def test_plugin_before_rejects_homepage_marketplace_redirect() -> None:
    plugin = AmazonDeliveryLocationPlugin(delivery_zip="10001")
    page = _FakePage(homepage_url="https://www.amazon.sg/?ref_=mr_direct_us_sg_sg")

    outcome = plugin.before(page, setup_timeout_ms=30_000)

    assert outcome.steps_completed is False
    assert outcome.reason == "homepage_marketplace_redirect"
    assert "open_widget" not in page.calls
    assert any("'www.amazon.sg'" in warning for warning in outcome.warning_notes)


def test_plugin_before_apply_failure_falls_back_to_return_and_warns() -> None:
    """FIX #3: when the Apply click loop fails and we fall back to Return (which doesn't throw),
    a warning records the apply click failed and the submit is unconfirmed; steps_completed False."""
    plugin = AmazonDeliveryLocationPlugin(delivery_zip="10001")
    page = _FakePage(apply_button_missing=True)
    outcome = plugin.before(page, setup_timeout_ms=30_000)
    assert outcome.steps_completed is False
    assert outcome.reason == "apply"
    assert page.return_pressed is True
    assert any(
        "Apply-button click failed" in w and "UNCONFIRMED" in w for w in outcome.warning_notes
    ), outcome.warning_notes


# ── Adapter end-to-end through the seam: keystone confirmed vs not ──────────────

class _PluginEngine:
    """A fake engine that runs the plugin's before() against a fake page and returns a DOM."""

    def __init__(self, rendered_dom: str, before_outcome: PreCaptureOutcome):
        self._dom = rendered_dom
        self._before_outcome = before_outcome

    def capture(self, **kwargs: Any) -> Any:
        return MagicMock(
            final_url=str(kwargs["url"]),
            title="PDP",
            rendered_dom=self._dom,
            visible_text="text",
            screenshot_png=b"\x89PNG\r\n\x1a\n",
            warning_notes=[],
            pre_capture_outcome=self._before_outcome,
        )


def test_adapter_confirmed_pin_records_confirmed_note_and_true_flag() -> None:
    """Requested ZIP plus US marketplace DOM -> CONFIRMED and pin_confirmed True."""
    plugin = AmazonDeliveryLocationPlugin(delivery_zip="10001")
    engine = _PluginEngine(
        rendered_dom=_US_ZIP_DOM,
        before_outcome=PreCaptureOutcome(attempted=True, steps_completed=True, reason=None),
    )
    result = fetch_cloakbrowser_snapshot_capture(
        url="https://www.amazon.com/dp/B07XXPHQZK",
        pre_capture=plugin,
        engine=engine,  # type: ignore[arg-type]
    )
    assert isinstance(result, CloakBrowserSnapshotSuccess)
    assert result.metadata["pin_confirmed"] is True
    assert result.metadata["humanize_mode_active"] is True
    assert result.metadata["pre_capture"] == "amazon_delivery_location"
    assert result.metadata["delivery_zip_requested"] == "10001"
    note = next(n for n in result.limitation_notes if "declared_delivery_zip" in n)
    assert "CONFIRMED" in note
    assert "set to '10001'" in note


def test_adapter_unconfirmed_pin_records_attempted_note_and_false_flag() -> None:
    """KEYSTONE through the adapter: confirm() False (non-US DOM) -> note says ATTEMPTED ...
    NOT confirmed (never 'set to'), pin_confirmed False."""
    plugin = AmazonDeliveryLocationPlugin(delivery_zip="10001")
    engine = _PluginEngine(
        rendered_dom=_NON_US_DOM,
        before_outcome=PreCaptureOutcome(attempted=True, steps_completed=True, reason=None),
    )
    result = fetch_cloakbrowser_snapshot_capture(
        url="https://www.amazon.com/dp/B07XXPHQZK",
        pre_capture=plugin,
        engine=engine,  # type: ignore[arg-type]
    )
    assert isinstance(result, CloakBrowserSnapshotSuccess)
    assert result.metadata["pin_confirmed"] is False
    note = next(n for n in result.limitation_notes if "declared_delivery_zip" in n)
    assert "ATTEMPTED" in note
    assert "NOT confirmed" in note
    assert "set to" not in note


def test_adapter_no_pre_capture_leaves_pin_confirmed_none() -> None:
    """Without a plugin, pin_confirmed is None and humanize_mode_active is False; no note."""

    class _PlainEngine:
        def capture(self, **kwargs: Any) -> Any:
            return MagicMock(
                final_url=str(kwargs["url"]),
                title="page",
                rendered_dom="<html><body>content</body></html>",
                visible_text="content",
                screenshot_png=b"\x89PNG\r\n\x1a\n",
                warning_notes=[],
                pre_capture_outcome=None,
            )

    result = fetch_cloakbrowser_snapshot_capture(
        url="https://www.ulta.com/p/example",
        engine=_PlainEngine(),  # type: ignore[arg-type]
    )
    assert isinstance(result, CloakBrowserSnapshotSuccess)
    assert result.metadata["pin_confirmed"] is None
    assert result.metadata["humanize_mode_active"] is False
    assert not any("declared_delivery_zip" in n for n in result.limitation_notes)


# ── Writer CLI tests ───────────────────────────────────────────────────────────

def test_writer_cli_accepts_delivery_zip_flag_and_builds_plugin(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """--delivery-zip is accepted by the writer CLI and forwarded as a pre_capture plugin."""
    calls: list[dict[str, Any]] = []

    def _recording_capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
        calls.append(dict(kwargs))
        return _fake_capture(**kwargs)

    monkeypatch.setattr(cloak_writer, "fetch_cloakbrowser_snapshot_capture", _recording_capture)

    rc = cloak_writer.main(
        [
            "--url", "https://www.amazon.com/dp/B07XXPHQZK",
            "--decision-question", "Does USD price appear after delivery location pin?",
            "--output", str(tmp_path / "obs_000_00"),
            "--delivery-zip", "10001",
            "--delivery-zip-setup-timeout-seconds", "45",
            "--series-id", "amazon-laneige-us-v0",
            "--intended-cadence-mode", "fixed",
            "--intended-cadence-slot-count", "4",
            "--locale-pin", "en-US",
            "--currency-pin", "USD",
        ]
    )

    assert rc == 0, "writer should exit 0"
    assert len(calls) == 1, "adapter should be called exactly once"
    plugin = calls[0]["pre_capture"]
    assert isinstance(plugin, AmazonDeliveryLocationPlugin)
    assert plugin.delivery_zip == "10001"
    assert plugin.setup_timeout_seconds == 45.0


def test_writer_cli_delivery_zip_absent_passes_no_plugin(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without --delivery-zip the adapter receives pre_capture=None (no pin)."""
    calls: list[dict[str, Any]] = []

    def _recording_capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
        calls.append(dict(kwargs))
        return _fake_capture(**kwargs)

    monkeypatch.setattr(cloak_writer, "fetch_cloakbrowser_snapshot_capture", _recording_capture)

    rc = cloak_writer.main(
        [
            "--url", "https://www.ulta.com/p/example",
            "--decision-question", "no pin capture",
            "--output", str(tmp_path / "obs_no_pin"),
        ]
    )

    assert rc == 0
    assert calls[0].get("pre_capture") is None


def test_writer_cli_delivery_zip_metadata_field(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When delivery_zip is supplied, the packet manifest carries the declared_delivery_zip
    limitation note (verifiable without live capture)."""
    monkeypatch.setattr(cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_capture)
    output_dir = tmp_path / "obs_zip"

    rc = cloak_writer.main(
        [
            "--url", "https://www.amazon.com/dp/B07XXPHQZK",
            "--decision-question", "US storefront pin test",
            "--output", str(output_dir),
            "--delivery-zip", "10001",
            "--series-id", "amazon-us-v0",
            "--intended-cadence-mode", "fixed",
            "--intended-cadence-slot-count", "2",
        ]
    )

    assert rc == 0
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    all_limitations = manifest.get("limitations", [])
    assert any("declared_delivery_zip" in lim for lim in all_limitations), (
        "packet limitations should record the delivery zip pin"
    )


def test_writer_rejects_delivery_zip_for_non_amazon_url(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="requires an amazon.com capture URL"):
        cloak_writer.run_source_capture_cloakbrowser_packet(
            url="https://www.ulta.com/p/example",
            source_family="retail_pdp",
            source_surface="cloakbrowser_snapshot",
            decision_question="invalid Amazon pin route",
            output_directory=tmp_path / "packet",
            capture_context="test",
            operator_category="authorized_subject_probe",
            capture_mode=cloak_writer.CaptureModeCategory.AGENT_ASSISTED,
            session_id=None,
            proxy_profile=None,
            actor_audience_context=None,
            visible_mode_changes=[],
            source_publication_or_event=None,
            source_edit_or_version=None,
            cutoff_posture=None,
            recapture_time=None,
            re_capture_relationship=None,
            warnings=[],
            limitations=[],
            timeout_seconds=20,
            wait_until="load",
            viewport_width=1280,
            viewport_height=720,
            max_artifact_bytes=50_000,
            block_heavy_assets=False,
            delivery_zip="10001",
        )


def test_amazon_pin_enforcement_rejects_redirect_even_if_confirmation_is_true() -> None:
    failure = cloak_writer._amazon_delivery_pin_failure(
        delivery_zip="10001",
        final_url="https://www.amazon.sg/dp/B07XXPHQZK",
        pin_confirmed=True,
    )

    assert failure is not None
    assert "not amazon.com" in failure


def test_amazon_pin_enforcement_accepts_confirmed_amazon_com_page() -> None:
    assert (
        cloak_writer._amazon_delivery_pin_failure(
            delivery_zip="10001",
            final_url="https://www.amazon.com/dp/B07XXPHQZK?th=1",
            pin_confirmed=True,
        )
        is None
    )


def test_writer_preserves_but_rejects_unconfirmed_amazon_pin(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output_dir = tmp_path / "unconfirmed"

    def _unconfirmed_capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
        result = _fake_capture(**kwargs)
        result.metadata["pin_confirmed"] = False
        return CloakBrowserSnapshotSuccess(
            requested_url=result.requested_url,
            final_url="https://www.amazon.sg/dp/B07XXPHQZK",
            title=result.title,
            rendered_dom=_NON_US_DOM,
            visible_text="S$45.00",
            screenshot_png=result.screenshot_png,
            metadata=result.metadata,
            warning_notes=result.warning_notes,
            limitation_notes=result.limitation_notes,
        )

    monkeypatch.setattr(
        cloak_writer, "fetch_cloakbrowser_snapshot_capture", _unconfirmed_capture
    )

    exit_code, message = cloak_writer.run_source_capture_cloakbrowser_packet(
        url="https://www.amazon.com/dp/B07XXPHQZK",
        source_family="retail_pdp",
        source_surface="cloakbrowser_snapshot",
        decision_question="US pin must remain applied",
        output_directory=output_dir,
        capture_context="test",
        operator_category="authorized_subject_probe",
        capture_mode=cloak_writer.CaptureModeCategory.AGENT_ASSISTED,
        session_id=None,
        proxy_profile=None,
        actor_audience_context=None,
        visible_mode_changes=[],
        source_publication_or_event=None,
        source_edit_or_version=None,
        cutoff_posture=None,
        recapture_time=None,
        re_capture_relationship=None,
        warnings=[],
        limitations=[],
        timeout_seconds=20,
        wait_until="load",
        viewport_width=1280,
        viewport_height=720,
        max_artifact_bytes=50_000,
        block_heavy_assets=False,
        delivery_zip="10001",
    )

    assert exit_code == cloak_writer.SOURCE_DETAIL_SUFFICIENCY_EXIT_CODE
    assert cloak_writer.AMAZON_DELIVERY_PIN_FAILURE_MODE_CHANGE in message
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert cloak_writer.AMAZON_DELIVERY_PIN_FAILURE_MODE_CHANGE in manifest[
        "visible_mode_changes"
    ]
    assert any(
        "MUST NOT be admitted as Amazon US delivery-pinned evidence" in limitation
        for limitation in manifest["limitations"]
    )


# ── Runner end-to-end: --writer-arg=--delivery-zip wires through ──────────────

def test_runner_delivery_zip_writer_arg_passes_validation(tmp_path: Path) -> None:
    """The cadence runner accepts --writer-arg=--delivery-zip value without raising (allowlist OK).
    Actual capture is not invoked: we use a fake writer_main that records argv and exits 0."""
    received_argv: list[list[str]] = []

    def _fake_writer_main(argv: list[str]) -> int:
        received_argv.append(list(argv))
        # Write a minimal packet to satisfy the runner's 'observed' check.
        import argparse
        p = argparse.ArgumentParser()
        p.add_argument("--output")
        ns, _ = p.parse_known_args(argv)
        if ns.output:
            out = Path(ns.output)
            out.mkdir(parents=True, exist_ok=True)
            manifest = {
                "SOURCE_CAPTURE_MANIFEST_VERSION": "source_capture_packet_v0",
                "timing": {
                    "capture_time": {"status": "known", "value": "2026-06-16T00:00:00Z"},
                },
                "access_posture": {"status": "known", "value": "cloakbrowser_snapshot clean capture"},
            }
            (out / "manifest.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
        return 0

    series_dir = tmp_path / "amazon_us_v0"
    series_dir.mkdir()
    index = series_runner.build_series_index(
        series_id="amazon-laneige-us-v0",
        urls=["https://www.amazon.com/dp/B07XXPHQZK"],
        decision_frame_ref="amazon-us-demand-frame-v0",
        decision_question="Does USD demand persist?",
        cadence_mode="fixed",
        slot_count=4,
    )
    (series_dir / "series_index.json").write_text(
        json.dumps(index), encoding="utf-8"
    )

    status, _ = series_runner.run_slot(
        series_dir=series_dir,
        slot_index=0,
        writer_main=_fake_writer_main,
        writer_extra_argv=["--delivery-zip", "10001", "--delivery-zip-setup-timeout-seconds", "45"],
    )

    assert status == series_runner.SLOT_OBSERVED
    assert len(received_argv) == 1
    writer_call = received_argv[0]
    assert "--delivery-zip" in writer_call
    zip_index = writer_call.index("--delivery-zip")
    assert writer_call[zip_index + 1] == "10001"
    assert "--delivery-zip-setup-timeout-seconds" in writer_call
