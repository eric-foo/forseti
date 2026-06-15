"""Offline tests for the US-storefront pin capability (--delivery-zip).

Covers:
  - The allowlist entry in the cadence runner so --delivery-zip can be passed via --writer-arg.
  - The CloakBrowser adapter accepting delivery_zip and writing it to metadata.
  - The writer CLI accepting --delivery-zip and forwarding it to the adapter.
  - End-to-end: runner --writer-arg=--delivery-zip value reaches the adapter.

All tests are offline: fetch_cloakbrowser_snapshot_capture is monkeypatched so no live
browser, network, or cloakbrowser runtime is required. INV-1: observed facts only.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from runners import run_source_capture_cloakbrowser_packet as cloak_writer
from runners import run_source_capture_durability_series as series_runner
from runners.run_source_capture_durability_series import _WRITER_ARG_KNOB_ALLOWLIST
from source_capture.adapters.cloakbrowser_snapshot import (
    CloakBrowserSnapshotSuccess,
    _AMAZON_HOMEPAGE_URL,
    fetch_cloakbrowser_snapshot_capture,
)


def _fake_capture(**kwargs: Any) -> CloakBrowserSnapshotSuccess:
    """Offline substitute for fetch_cloakbrowser_snapshot_capture; records delivery_zip."""
    url = str(kwargs.get("url", "https://example.com/"))
    delivery_zip = kwargs.get("delivery_zip")
    limitation_notes = []
    if delivery_zip is not None:
        limitation_notes.append(
            f"declared_delivery_zip: Amazon delivery location set to {delivery_zip!r}"
        )
    return CloakBrowserSnapshotSuccess(
        requested_url=url,
        final_url=url,
        title="Product Page",
        rendered_dom='<html><body><input name="currencyOfPreference" value="USD"></body></html>',
        visible_text="USD price",
        screenshot_png=b"\x89PNG\r\n\x1a\n",
        metadata={
            "capture_timestamp": "2026-06-16T00:00:00Z",
            "requested_url": url,
            "delivery_zip_requested": delivery_zip,
        },
        warning_notes=[],
        limitation_notes=limitation_notes,
    )


# ── Allowlist tests ────────────────────────────────────────────────────────────

def test_delivery_zip_in_runner_allowlist() -> None:
    """--delivery-zip must be in the cadence runner allowlist so the operator can pass it
    per-slot via --writer-arg without triggering the default-deny guard."""
    assert "--delivery-zip" in _WRITER_ARG_KNOB_ALLOWLIST


def test_allowlist_still_excludes_proxy_and_identity_flags() -> None:
    """Regression: adding --delivery-zip must not inadvertently add proxy or identity flags."""
    for forbidden in ("--proxy-profile-label", "--url", "--series-id", "--output",
                      "--preflight-only", "--guarded-reddit-launch"):
        assert forbidden not in _WRITER_ARG_KNOB_ALLOWLIST, (
            f"allowlist should not contain {forbidden}"
        )


# ── Writer CLI tests ───────────────────────────────────────────────────────────

def test_writer_cli_accepts_delivery_zip_flag(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """--delivery-zip is accepted by the writer CLI and forwarded to the adapter."""
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
            "--series-id", "amazon-laneige-us-v0",
            "--intended-cadence-mode", "fixed",
            "--intended-cadence-slot-count", "4",
            "--locale-pin", "en-US",
            "--currency-pin", "USD",
        ]
    )

    assert rc == 0, "writer should exit 0"
    assert len(calls) == 1, "adapter should be called exactly once"
    assert calls[0]["delivery_zip"] == "10001"


def test_writer_cli_delivery_zip_absent_passes_none(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Without --delivery-zip the adapter receives delivery_zip=None (no pin)."""
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
    assert calls[0].get("delivery_zip") is None


def test_writer_cli_delivery_zip_metadata_field(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When delivery_zip is supplied, the packet manifest carries the limitation note and the
    adapter metadata contains delivery_zip_requested (verifiable without live capture)."""
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


# ── Adapter unit tests ────────────────────────────────────────────────────────

def test_adapter_delivery_zip_recorded_in_metadata() -> None:
    """fetch_cloakbrowser_snapshot_capture with delivery_zip records delivery_zip_requested in
    metadata and adds the declared_delivery_zip limitation note. Uses a fake engine so no
    live browser is launched."""

    class _FakeEngine:
        def capture(self, **kwargs: Any) -> Any:
            url = kwargs["url"]
            return MagicMock(
                final_url=url,
                title="USD PDP",
                rendered_dom="<html><body>USD content</body></html>",
                visible_text="USD content",
                screenshot_png=b"\x89PNG\r\n\x1a\n",
                warning_notes=[],
            )

    result = fetch_cloakbrowser_snapshot_capture(
        url="https://www.amazon.com/dp/B07XXPHQZK",
        delivery_zip="10001",
        engine=_FakeEngine(),  # type: ignore[arg-type]
    )

    assert not isinstance(result, type(None))
    from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
    assert isinstance(result, CloakBrowserSnapshotSuccess)
    assert result.metadata.get("delivery_zip_requested") == "10001"
    assert any("declared_delivery_zip" in note for note in result.limitation_notes)


def test_adapter_no_delivery_zip_metadata_none() -> None:
    """Without delivery_zip, metadata[delivery_zip_requested] is None and no delivery_zip
    limitation note is added."""

    class _FakeEngine:
        def capture(self, **kwargs: Any) -> Any:
            url = kwargs["url"]
            return MagicMock(
                final_url=url,
                title="page",
                rendered_dom="<html><body>content</body></html>",
                visible_text="content",
                screenshot_png=b"\x89PNG\r\n\x1a\n",
                warning_notes=[],
            )

    result = fetch_cloakbrowser_snapshot_capture(
        url="https://www.ulta.com/p/example",
        engine=_FakeEngine(),  # type: ignore[arg-type]
    )

    from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess
    assert isinstance(result, CloakBrowserSnapshotSuccess)
    assert result.metadata.get("delivery_zip_requested") is None
    assert not any("declared_delivery_zip" in note for note in result.limitation_notes)


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
            # Minimal manifest matching what _read_capture_time and _read_access_posture expect:
            # timing.capture_time.value  and  access_posture.value (no "access_failed" token).
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
        writer_extra_argv=["--delivery-zip", "10001"],
    )

    assert status == series_runner.SLOT_OBSERVED
    assert len(received_argv) == 1
    writer_call = received_argv[0]
    assert "--delivery-zip" in writer_call
    zip_index = writer_call.index("--delivery-zip")
    assert writer_call[zip_index + 1] == "10001"
