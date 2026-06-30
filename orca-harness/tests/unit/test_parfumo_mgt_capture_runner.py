from __future__ import annotations

import json
from pathlib import Path

import pytest

from runners.run_parfumo_mgt_capture import (
    DIRECT_HTTP_SLOT,
    DIRECT_HTTP_SURFACE,
    extract_parfumo_product_slug,
    preflight_parfumo_mgt_capture,
    run_parfumo_mgt_capture,
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


def test_extract_parfumo_product_slug() -> None:
    assert (
        extract_parfumo_product_slug(_LOCATOR)
        == "Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum"
    )
