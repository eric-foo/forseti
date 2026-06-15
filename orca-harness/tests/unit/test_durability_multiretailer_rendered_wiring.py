"""Offline tests for the multi-retailer rendered-capture wiring.

These cover the SETTLE deliverable for the demand-durability series: the rendered (CloakBrowser)
writer exposing the SAME demand-durability flag surface as the direct_http writer, populating the
Ob.17 durability fields into the packet, and the cadence runner selecting the rendered writer per
slot (with a knob passthrough) through its existing injectable ``writer_main`` seam.

All tests are offline: the CloakBrowser adapter is monkeypatched with a fake capture, so no live
browser, network, or cloakbrowser runtime is required. INV-1: these assert that observed facts and
limits are recorded -- never a demand verdict, score, weight, or durable-vs-hollow judgment.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from runners import run_source_capture_cloakbrowser_packet as cloak_writer
from runners import run_source_capture_durability_series as series_runner
from runners import run_source_capture_http_packet as http_writer
from source_capture import cli_support
from source_capture.adapters.cloakbrowser_snapshot import CloakBrowserSnapshotSuccess


def _all_option_strings(build_parser) -> set[str]:
    parser = build_parser()
    opts: set[str] = set()
    for action in parser._actions:
        opts.update(action.option_strings)
    return opts


def _canonical_durability_option_strings() -> set[str]:
    """The EXACT durability flag surface, defined once in cli_support.add_durability_arguments."""
    parser = argparse.ArgumentParser()
    cli_support.add_durability_arguments(parser)
    opts = _all_option_strings(lambda: parser)
    opts.discard("-h")
    opts.discard("--help")
    return opts


def test_rendered_and_direct_writers_expose_identical_durability_flags() -> None:
    """Drift guard (EXACT, not a substring proxy). The cadence runner forwards ONE fixed durability
    argv to whichever writer --writer selects, so each writer must expose EXACTLY the shared
    durability surface from cli_support.add_durability_arguments -- a single missing or renamed flag
    would abort the rendered writer on a forwarded arg. Compared against the canonical set so a
    future durability flag added outside the old substring tokens can no longer slip past."""
    canonical = _canonical_durability_option_strings()
    assert canonical  # the shared contract is non-empty
    direct = _all_option_strings(http_writer._build_parser)
    rendered = _all_option_strings(cloak_writer._build_parser)
    # each writer exposes the FULL canonical durability surface...
    assert canonical <= direct, f"direct_http missing: {canonical - direct}"
    assert canonical <= rendered, f"rendered writer missing: {canonical - rendered}"
    # ...and the two writers' durability surfaces are identical (no divergence within the surface).
    assert (direct & canonical) == (rendered & canonical) == canonical


def _fake_rendered_capture(**kwargs: object) -> CloakBrowserSnapshotSuccess:
    """A successful rendered capture (e.g. a Ulta PDP whose __APOLLO_STATE__ is in the rendered DOM)
    without launching a browser. Mirrors the adapter's success envelope."""
    url = str(kwargs["url"])
    return CloakBrowserSnapshotSuccess(
        requested_url=url,
        final_url=url,
        title="Rendered PDP",
        rendered_dom="<html><body><script>window.__APOLLO_STATE__={};</script></body></html>",
        visible_text="price and availability",
        screenshot_png=b"\x89PNG\r\n\x1a\nrendered",
        metadata={"capture_timestamp": "2026-06-15T00:00:01Z", "requested_url": url},
        warning_notes=[],
        limitation_notes=[],
    )


def test_rendered_writer_cli_populates_ob17_durability_fields(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The rendered writer's CLI -- the exact entrypoint the cadence runner invokes as writer_main
    -- accepts the forwarded durability argv and populates the Ob.17 fields: the four Element-1 pins
    ride on the slice; series_id + the Element-2 origin postures + the Element-4 declared cadence
    ride on the packet. An unsupplied pin is recorded as an honest gap, never fabricated (INV-1)."""
    monkeypatch.setattr(cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_rendered_capture)
    output_dir = tmp_path / "obs_000_00"

    rc = cloak_writer.main(
        [
            "--url", "https://www.ulta.com/p/example",
            "--decision-question", "Does demand persist across the cadence?",
            "--output", str(output_dir),
            "--series-id", "ulta-demand-001",
            "--intended-cadence-mode", "fixed",
            "--intended-cadence-slot-count", "3",
            "--session-visibility-pin", "logged_out_public",
            "--locale-pin", "en-US",
            "--currency-pin", "USD",
            # forwarded by the cadence runner only when variant_pin is absent -> honest gap
            "--variant-pin-unknown-reason", "variant not surfaced on PDP",
            "--cold-start-at", "2026-06-15T00:00:00Z",
            "--pre-coverage-history-posture", "no pre-coverage history captured",
        ]
    )

    assert rc == 0
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))

    # Element 2 + Element 4 ride on the packet.
    assert manifest["series_id"] == "ulta-demand-001"
    assert manifest["cold_start_at"] == {
        "status": "known",
        "value": "2026-06-15T00:00:00Z",
        "reason": None,
    }
    assert manifest["pre_coverage_history_posture"]["status"] == "known"
    assert manifest["pre_coverage_history_posture"]["value"] == "no pre-coverage history captured"
    assert manifest["intended_cadence"]["mode"] == "fixed"
    assert manifest["intended_cadence"]["slot_count"] == 3

    # Element 1 pins ride on the slice; the unsupplied variant pin is an honest gap.
    observed_slice = manifest["source_slices"][0]
    assert observed_slice["session_visibility_pin"] == {
        "status": "known",
        "value": "logged_out_public",
        "reason": None,
    }
    assert observed_slice["locale_pin"]["value"] == "en-US"
    assert observed_slice["currency_pin"]["value"] == "USD"
    assert observed_slice["variant_pin"]["status"] == "unknown_with_reason"


def test_rendered_writer_non_durability_capture_leaves_fields_unset(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Back-compat: with no durability flags the rendered writer still writes a valid packet and the
    durability fields stay None (no manifest bump, no fabricated series)."""
    monkeypatch.setattr(cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_rendered_capture)
    output_dir = tmp_path / "obs_plain"

    rc = cloak_writer.main(
        [
            "--url", "https://www.ulta.com/p/example",
            "--decision-question", "One-off rendered capture",
            "--output", str(output_dir),
        ]
    )

    assert rc == 0
    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["series_id"] is None
    assert manifest["cold_start_at"] is None
    assert manifest["pre_coverage_history_posture"] is None
    assert manifest["intended_cadence"] is None
    observed_slice = manifest["source_slices"][0]
    assert observed_slice["session_visibility_pin"] is None
    assert observed_slice["locale_pin"] is None
    assert observed_slice["currency_pin"] is None
    assert observed_slice["variant_pin"] is None


def test_rendered_writer_rejects_durability_field_without_series_id(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A demand-durability fact supplied without a --series-id has no series identity to ride on:
    the rendered writer fails visibly (exit 2), same as direct_http, rather than writing an
    orphaned packet."""
    monkeypatch.setattr(cloak_writer, "fetch_cloakbrowser_snapshot_capture", _fake_rendered_capture)

    with pytest.raises(SystemExit) as excinfo:
        cloak_writer.main(
            [
                "--url", "https://www.ulta.com/p/example",
                "--decision-question", "missing series id",
                "--output", str(tmp_path / "orphan"),
                "--locale-pin", "en-US",  # durability fact, but no --series-id
            ]
        )
    assert excinfo.value.code == 2


def test_series_runner_writer_registry_exposes_both_writers() -> None:
    """The cadence runner can invoke either writer through its injectable seam; the default stays
    direct_http (back-compat) and 'cloakbrowser' maps to the rendered writer's CLI main."""
    assert series_runner.DEFAULT_WRITER == "direct_http"
    assert set(series_runner.WRITER_MAINS) == {"direct_http", "cloakbrowser"}
    assert series_runner.WRITER_MAINS["cloakbrowser"] is cloak_writer.main
    assert series_runner.WRITER_MAINS["direct_http"] is http_writer.main


def _init_series(series_dir: Path) -> None:
    rc = series_runner.main(
        [
            "init",
            "--series-dir", str(series_dir),
            "--series-id", "sephora-demand-001",
            "--decision-frame-ref", "DF-multiretailer-001",
            "--decision-question", "Does demand persist across the cadence?",
            "--url", "https://www.sephora.com/product/example",
            "--cadence-mode", "fixed",
            "--slot-count", "2",
            "--locale-pin", "en-US",
            "--currency-pin", "USD",
        ]
    )
    assert rc == 0


def test_run_slot_routes_to_selected_writer_and_appends_writer_arg(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """run-slot --writer cloakbrowser invokes the rendered writer, and --writer-arg knobs (e.g.
    Sephora's progressive --scroll-step-px) are appended verbatim to the forwarded argv -- on top of
    the series/cadence/pin flags the runner already forwards. The knobs are NOT persisted in the
    series state (no state-model change); each packet self-records its capture config in metadata."""
    series_dir = tmp_path / "series"
    _init_series(series_dir)

    captured: dict[str, list[str]] = {}

    def fake_rendered_main(argv) -> int:
        captured["argv"] = list(argv)
        output_dir = Path(argv[argv.index("--output") + 1])
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "manifest.json").write_text(
            json.dumps({"timing": {"capture_time": {"value": "2026-06-15T00:00:05Z"}}}),
            encoding="utf-8",
        )
        return 0

    monkeypatch.setitem(series_runner.WRITER_MAINS, "cloakbrowser", fake_rendered_main)

    rc = series_runner.main(
        [
            "run-slot",
            "--series-dir", str(series_dir),
            "--slot", "0",
            "--writer", "cloakbrowser",
            "--writer-arg=--scroll-step-px=350",
            "--writer-arg=--settle-seconds=2.0",
        ]
    )

    assert rc == 0  # observed
    argv = captured["argv"]
    # series/cadence/pin flags the runner forwards regardless of writer:
    assert "--series-id" in argv and "sephora-demand-001" in argv
    assert "--locale-pin" in argv and "--currency-pin" in argv
    assert "--intended-cadence-mode" in argv
    # rendered-only knobs appended verbatim via --writer-arg passthrough:
    assert "--scroll-step-px=350" in argv
    assert "--settle-seconds=2.0" in argv


def test_run_slot_default_writer_is_direct_http(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Back-compat: with no --writer flag, run-slot still uses the direct_http writer."""
    series_dir = tmp_path / "series"
    _init_series(series_dir)

    used: dict[str, bool] = {}

    def fake_direct_main(argv) -> int:
        used["direct_http"] = True
        output_dir = Path(argv[argv.index("--output") + 1])
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "manifest.json").write_text(
            json.dumps({"timing": {"capture_time": {"value": "2026-06-15T00:00:05Z"}}}),
            encoding="utf-8",
        )
        return 0

    monkeypatch.setitem(series_runner.WRITER_MAINS, "direct_http", fake_direct_main)

    rc = series_runner.main(
        ["run-slot", "--series-dir", str(series_dir), "--slot", "0"]
    )
    assert rc == 0
    assert used.get("direct_http") is True


# --- Hardening guards (closes the delegated cross-vendor review findings) -------------------


def test_run_slot_rejects_writer_arg_overriding_runner_owned_arg(tmp_path: Path) -> None:
    """A --writer-arg that re-specifies a runner-owned arg (here --url) is rejected (exit 2), so a
    passthrough cannot override the slot's identity/source/output via argparse last-value-wins."""
    series_dir = tmp_path / "series"
    _init_series(series_dir)
    with pytest.raises(SystemExit) as excinfo:
        series_runner.main(
            [
                "run-slot", "--series-dir", str(series_dir), "--slot", "0",
                "--writer", "cloakbrowser",
                "--writer-arg=--url=https://evil.example/x",
            ]
        )
    assert excinfo.value.code == 2


def test_run_slot_rejects_writer_arg_capture_skipping_mode(tmp_path: Path) -> None:
    """A --writer-arg selecting a capture-skipping mode (--preflight-only) is rejected (exit 2), so
    it cannot be used to mark a slot observed without a real capture."""
    series_dir = tmp_path / "series"
    _init_series(series_dir)
    with pytest.raises(SystemExit) as excinfo:
        series_runner.main(
            [
                "run-slot", "--series-dir", str(series_dir), "--slot", "0",
                "--writer", "cloakbrowser",
                "--writer-arg=--preflight-only",
            ]
        )
    assert excinfo.value.code == 2


def test_run_slot_allows_capture_knob_writer_arg(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A legitimate rendered-capture knob (--scroll-step-px) passes the allowlist, routes to the
    rendered writer, and is appended to the forwarded argv (the intended Sephora-scroll path)."""
    series_dir = tmp_path / "series"
    _init_series(series_dir)
    captured: dict[str, list[str]] = {}

    def fake(argv) -> int:
        captured["argv"] = list(argv)
        out = Path(argv[argv.index("--output") + 1])
        out.mkdir(parents=True, exist_ok=True)
        (out / "manifest.json").write_text(
            json.dumps({"timing": {"capture_time": {"value": "2026-06-15T00:00:05Z"}}}),
            encoding="utf-8",
        )
        return 0

    monkeypatch.setitem(series_runner.WRITER_MAINS, "cloakbrowser", fake)
    rc = series_runner.main(
        [
            "run-slot", "--series-dir", str(series_dir), "--slot", "0",
            "--writer", "cloakbrowser",
            "--writer-arg=--scroll-step-px=350",
        ]
    )
    assert rc == 0  # observed
    assert "--scroll-step-px=350" in captured["argv"]


def test_run_slot_writer_exit0_without_packet_is_un_observed_gap(tmp_path: Path) -> None:
    """Exit 0 alone is NOT an observation: a writer that returns 0 but writes no source-capture
    packet is recorded as an un-observed GAP, never observed (no fake success / gap != no-change)."""
    series_dir = tmp_path / "series"
    _init_series(series_dir)
    status, slot = series_runner.run_slot(
        series_dir=series_dir, slot_index=0, writer_main=lambda argv: 0, now_z="2026-06-15T00:00:00Z"
    )
    assert status == series_runner.SLOT_UN_OBSERVED
    assert slot["gap_kind"] == "fetch_failed"
    assert "no source-capture packet" in slot["gap_reason"]
    assert "no_change" not in json.dumps(slot).lower()
    assert "no change" not in json.dumps(slot).lower()


def test_run_slot_access_failed_packet_is_un_observed_gap(tmp_path: Path) -> None:
    """A packet whose access_posture is access_failed (a non-2xx body or a rendered anti-bot /
    interstitial block page) is an un-observed GAP, never an observed durability slot (commission
    no-gate-defeat: STOP at a challenge, record the limitation)."""
    series_dir = tmp_path / "series"
    _init_series(series_dir)

    def access_blocked_writer(argv) -> int:
        out = Path(argv[argv.index("--output") + 1])
        out.mkdir(parents=True, exist_ok=True)
        (out / "manifest.json").write_text(
            json.dumps(
                {
                    "timing": {"capture_time": {"value": "2026-06-15T00:00:05Z"}},
                    "access_posture": {
                        "status": "known",
                        "value": (
                            "cloakbrowser_snapshot access_failed with access block "
                            "reddit_network_security_block; rendered block artifacts preserved"
                        ),
                        "reason": None,
                    },
                }
            ),
            encoding="utf-8",
        )
        return 0

    status, slot = series_runner.run_slot(
        series_dir=series_dir, slot_index=0, writer_main=access_blocked_writer, now_z="2026-06-15T00:00:00Z"
    )
    assert status == series_runner.SLOT_UN_OBSERVED
    assert "access_failed" in slot["gap_reason"]
    assert "no_change" not in json.dumps(slot).lower()
