from __future__ import annotations

import json
from pathlib import Path

import pytest

import runners.run_parfumo_mgt_capture as runner_module

from runners.run_parfumo_mgt_capture import (
    DIRECT_HTTP_SLOT,
    DIRECT_HTTP_SURFACE,
    TARGETED_RENDERED_CAPTURE_PROFILE,
    TARGETED_RENDERED_SLOT,
    TARGETED_RENDERED_SURFACE,
    extract_parfumo_product_slug,
    preflight_parfumo_mgt_capture,
    run_parfumo_mgt_capture,
    run_parfumo_targeted_rendered_capture,
)


_LOCATOR = "https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum"


def test_parfumo_capture_preflight_does_not_capture_network(tmp_path: Path) -> None:
    message = preflight_parfumo_mgt_capture(url=_LOCATOR, output_root=tmp_path / "out")

    assert "no network capture attempted" in message
    assert "Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum" in message
    assert not (tmp_path / "out").exists()


def test_parfumo_capture_rejects_non_product_url(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="/Perfumes/ product URL"):
        preflight_parfumo_mgt_capture(url="https://www.parfumo.com/Users/rimazy", output_root=tmp_path / "out")


def test_parfumo_capture_runner_uses_injected_http_runner_without_network(tmp_path: Path) -> None:
    calls: list[dict[str, object]] = []

    def fake_http_runner(**kwargs):
        calls.append(kwargs)
        output_directory = Path(kwargs["output_directory"])
        output_directory.mkdir(parents=True)
        (output_directory / "manifest.json").write_text(
            json.dumps(
                {
                    "packet_id": "01PARFUMOTEST",
                    "source_family": kwargs["source_family"],
                    "source_surface": kwargs["source_surface"],
                    "access_posture": {"status": "known", "value": "fake direct HTTP"},
                    "archive_history_posture": {"status": "not_attempted", "reason": "test"},
                    "source_slices": [],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        return 0, str(output_directory)

    exit_code, message = run_parfumo_mgt_capture(
        url=_LOCATOR,
        output_root=tmp_path / "out",
        http_runner=fake_http_runner,
    )

    assert exit_code == 0
    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    assert summary["packet_roles"][DIRECT_HTTP_SLOT]["source_surface"] == DIRECT_HTTP_SURFACE
    assert "not anti-bot evasion" in summary["non_claims"]
    assert calls and calls[0]["source_surface"] == DIRECT_HTTP_SURFACE


def test_parfumo_cli_uses_orca_data_root_env_without_losing_output_root(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from data_lake.root import DataLakeRoot

    sentinel_data_root = object()
    resolve_calls: list[Path | None] = []
    run_calls: list[dict[str, object]] = []

    def fake_resolve(*, explicit=None, **kwargs):
        resolve_calls.append(explicit)
        return sentinel_data_root

    def fake_run_parfumo_mgt_capture(**kwargs):
        run_calls.append(kwargs)
        return 0, str(tmp_path / "summary.json")

    monkeypatch.setenv("ORCA_DATA_ROOT", str(tmp_path / "lake-root"))
    monkeypatch.setattr(DataLakeRoot, "resolve", staticmethod(fake_resolve))
    monkeypatch.setattr(runner_module, "run_parfumo_mgt_capture", fake_run_parfumo_mgt_capture)

    output_root = tmp_path / "out"
    exit_code = runner_module.main(["--url", _LOCATOR, "--output-root", str(output_root)])

    assert exit_code == 0
    assert resolve_calls == [None]
    assert run_calls
    assert run_calls[0]["data_root"] is sentinel_data_root
    assert run_calls[0]["output_root"] == output_root


def test_parfumo_targeted_rendered_runner_packages_local_artifacts_without_network(
    tmp_path: Path,
) -> None:
    artifacts = _write_targeted_artifacts(tmp_path / "artifacts")

    exit_code, message = run_parfumo_targeted_rendered_capture(
        url=_LOCATOR,
        output_root=tmp_path / "out",
        rendered_dom_path=artifacts["rendered_dom"],
        visible_text_path=artifacts["visible_text"],
        route_receipt_path=artifacts["route_receipt"],
        screenshot_path=artifacts["screenshot"],
    )

    assert exit_code == 0
    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    assert summary["capture_profile"] == TARGETED_RENDERED_CAPTURE_PROFILE
    assert summary["packet_roles"][TARGETED_RENDERED_SLOT]["source_surface"] == TARGETED_RENDERED_SURFACE
    assert "not full Parfumo corpus capture" in summary["non_claims"]
    assert "not live network capture by this local packet writer" in summary["non_claims"]

    packet_path = Path(summary["packet_roles"][TARGETED_RENDERED_SLOT]["packet_path"])
    manifest = json.loads((packet_path / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["source_family"] == "fragrance_native_database"
    assert manifest["source_surface"] == TARGETED_RENDERED_SURFACE
    assert manifest["capture_mode"] == "human-led"
    assert manifest["receipt_metadata"]["non_claims"] == summary["non_claims"]
    assert [source_slice["slice_id"] for source_slice in manifest["source_slices"]] == [
        "parfumo_targeted:product_context",
        "parfumo_targeted:review_latest_recent",
        "parfumo_targeted:review_source_visible_high_rating",
        "parfumo_targeted:review_source_visible_low_rating",
        "parfumo_targeted:statement_latest_recent",
    ]
    assert {preserved_file["file_id"] for preserved_file in manifest["preserved_files"]} == {
        "file_01",
        "file_02",
        "file_03",
        "file_04",
        "file_05",
    }
    preserved_paths = {
        preserved_file["relative_packet_path"] for preserved_file in manifest["preserved_files"]
    }
    assert any(path.endswith("/05_parfumo_targeted_capture_plan.json") for path in preserved_paths)
    assert all(
        source_slice["preserved_file_ids"] == ["file_01", "file_02", "file_03", "file_04", "file_05"]
        for source_slice in manifest["source_slices"]
    )


def test_parfumo_targeted_rendered_runner_rejects_browser_secret_material(tmp_path: Path) -> None:
    artifacts = _write_targeted_artifacts(tmp_path / "artifacts", secret="cf_clearance=abc123")

    with pytest.raises(ValueError, match="browser-secret material"):
        run_parfumo_targeted_rendered_capture(
            url=_LOCATOR,
            output_root=tmp_path / "out",
            rendered_dom_path=artifacts["rendered_dom"],
            visible_text_path=artifacts["visible_text"],
            route_receipt_path=artifacts["route_receipt"],
            screenshot_path=artifacts["screenshot"],
        )


def test_extract_parfumo_product_slug() -> None:
    assert (
        extract_parfumo_product_slug(_LOCATOR)
        == "Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum"
    )


def _write_targeted_artifacts(base_dir: Path, *, secret: str | None = None) -> dict[str, Path]:
    base_dir.mkdir(parents=True)
    rendered_dom = base_dir / "rendered_dom.html"
    visible_text = base_dir / "visible_text.txt"
    route_receipt = base_dir / "route_receipt.json"
    screenshot = base_dir / "viewport_screenshot.png"

    rendered_dom.write_text(
        """
        <html>
          <body>
            <main data-perfume-id="67720">
              <h1>Baccarat Rouge 540 Eau de Parfum</h1>
              <section data-review-id="latest">Recent source-visible review text.</section>
              <section data-statement-id="latest">Recent source-visible statement text.</section>
            </main>
          </body>
        </html>
        """,
        encoding="utf-8",
    )
    visible_text.write_text(
        "Baccarat Rouge 540 Eau de Parfum\nReviews 369\nStatements 1390\n",
        encoding="utf-8",
    )
    route_receipt.write_text(
        json.dumps(
            {
                "route": "chrome_extension_user_visible_rendered_session",
                "source_surface": TARGETED_RENDERED_SURFACE,
                "network": "not captured by this fixture",
                "secret_probe": secret,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    screenshot.write_bytes(b"png fixture bytes")
    return {
        "rendered_dom": rendered_dom,
        "visible_text": visible_text,
        "route_receipt": route_receipt,
        "screenshot": screenshot,
    }
