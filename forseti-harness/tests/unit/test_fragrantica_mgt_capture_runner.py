from __future__ import annotations

import inspect
import json
from pathlib import Path
from typing import Callable

import pytest

from runners import run_fragrantica_mgt_capture as runner
from runners.run_source_capture_cloakbrowser_packet import run_source_capture_cloakbrowser_packet
from runners.run_source_capture_http_packet import run_source_capture_http_packet


_URL = "https://www.fragrantica.com/perfume/Chanel/Chanel-No-5-33519.html"


def _fact(value: str) -> dict[str, object]:
    return {"reason": None, "status": "known", "value": value}


def _not_attempted(reason: str) -> dict[str, object]:
    return {"reason": reason, "status": "not_attempted", "value": None}


def _write_manifest(
    packet_dir: Path,
    *,
    packet_id: str,
    source_surface: str,
    access_value: str = "anonymous capture succeeded",
) -> None:
    archive_posture = _not_attempted("test packet does not query archive or history services")
    packet_dir.mkdir(parents=True, exist_ok=True)
    (packet_dir / "manifest.json").write_text(
        json.dumps(
            {
                "packet_id": packet_id,
                "source_family": runner.SOURCE_FAMILY,
                "source_surface": source_surface,
                "access_posture": _fact(access_value),
                "archive_history_posture": archive_posture,
                "source_slices": [
                    {
                        "slice_id": "slice_01",
                        "access_posture": _fact(access_value),
                        "archive_history_posture": archive_posture,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def _assert_kwargs_match_signature(call: dict[str, object], target: Callable[..., object]) -> None:
    signature = inspect.signature(target)
    accepted = {
        name
        for name, parameter in signature.parameters.items()
        if parameter.kind in {inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD}
    }
    required = {
        name
        for name, parameter in signature.parameters.items()
        if parameter.default is inspect.Parameter.empty
        and parameter.kind in {inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD}
    }

    assert set(call) <= accepted
    assert required <= set(call)


def test_fragrantica_mgt_capture_composes_three_packets_and_summary(tmp_path: Path) -> None:
    calls: list[dict[str, object]] = []

    def fake_http_runner(**kwargs: object) -> tuple[int, str]:
        calls.append(dict(kwargs))
        packet_dir = Path(kwargs["output_directory"])
        _write_manifest(
            packet_dir,
            packet_id="01KW0000000000000000000001",
            source_surface=str(kwargs["source_surface"]),
            access_value="direct HTTP succeeded",
        )
        return 0, str(packet_dir)

    def fake_cloakbrowser_runner(**kwargs: object) -> tuple[int, str]:
        calls.append(dict(kwargs))
        packet_dir = Path(kwargs["output_directory"])
        packet_id = (
            "01KW0000000000000000000002"
            if kwargs["source_surface"] == runner.INITIAL_VIEWPORT_SURFACE
            else "01KW0000000000000000000003"
        )
        _write_manifest(
            packet_dir,
            packet_id=packet_id,
            source_surface=str(kwargs["source_surface"]),
            access_value=f"{kwargs['source_surface']} succeeded",
        )
        return 0, str(packet_dir)

    output_root = tmp_path / "fragrantica_mgt_bundle"

    exit_code, message = runner.run_fragrantica_mgt_capture(
        url=_URL,
        output_root=output_root,
        http_runner=fake_http_runner,
        cloakbrowser_runner=fake_cloakbrowser_runner,
    )

    assert exit_code == 0
    summary_path = Path(message)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["capture_profile"] == runner.CAPTURE_PROFILE
    assert summary["tier"] == "mini_god_tier"
    assert summary["source_family"] == runner.SOURCE_FAMILY
    assert summary["fragrantica_product_id"] == "33519"
    assert summary["packet_publication_mode"] == "local_output_bundle"
    assert summary["projection_status"] == (
        "capture_time_for_rendered_packets; direct_http_remains_raw_canary"
    )
    assert summary["capture_parameters"]["rendered_capture_artifact_mode"] == "content"
    assert summary["capture_parameters"]["direct_http_capture_artifact_mode"] == "raw"
    assert summary["packet_roles"][runner.DIRECT_HTTP_SLOT]["packet_id"] == "01KW0000000000000000000001"
    assert summary["packet_roles"][runner.INITIAL_VIEWPORT_SLOT]["packet_id"] == "01KW0000000000000000000002"
    assert summary["packet_roles"][runner.DEEP_SCROLL_SLOT]["packet_id"] == "01KW0000000000000000000003"
    assert summary["packet_roles"][runner.DIRECT_HTTP_SLOT]["access_posture"]["value"] == "direct HTTP succeeded"
    assert summary["packet_roles"][runner.DIRECT_HTTP_SLOT]["slice_postures"][0]["slice_id"] == "slice_01"
    assert any("login-gated full review archive" in item for item in summary["accepted_residuals"])

    assert len(calls) == 3
    _assert_kwargs_match_signature(calls[0], run_source_capture_http_packet)
    _assert_kwargs_match_signature(calls[1], run_source_capture_cloakbrowser_packet)
    _assert_kwargs_match_signature(calls[2], run_source_capture_cloakbrowser_packet)
    assert calls[0]["source_surface"] == runner.DIRECT_HTTP_SURFACE
    assert calls[0]["capture_mode"] == runner.CaptureModeCategory.STRUCTURED_ACCESS
    assert calls[0]["data_root"] is None
    assert "content_capture" not in calls[0]
    assert calls[1]["source_surface"] == runner.INITIAL_VIEWPORT_SURFACE
    assert calls[1]["settle_seconds"] == runner.DEFAULT_INITIAL_SETTLE_SECONDS
    assert calls[1]["scroll_passes"] == 0
    assert calls[1]["scroll_step_px"] == 0
    assert calls[1]["content_capture"].capture_artifact_mode == "content"
    assert calls[2]["source_surface"] == runner.DEEP_SCROLL_SURFACE
    assert calls[2]["settle_seconds"] == runner.DEFAULT_DEEP_SETTLE_SECONDS
    assert calls[2]["scroll_passes"] == runner.DEFAULT_DEEP_SCROLL_PASSES
    assert calls[2]["scroll_step_px"] == runner.DEFAULT_DEEP_SCROLL_STEP_PX
    assert calls[2]["block_heavy_assets"] is False
    assert calls[2]["content_capture"].capture_artifact_mode == "content"


class _FakeDataRoot:
    def __init__(self, path: Path) -> None:
        self.path = path


def test_fragrantica_mgt_capture_data_root_mode_writes_local_summary(tmp_path: Path) -> None:
    # The fleet lake-seam scanner owns direct packet writers; this test owns this transitive wrapper's lake branch.
    calls: list[dict[str, object]] = []
    data_root = _FakeDataRoot(tmp_path / "lake")
    lake_packets_root = tmp_path / "lake_packets"

    def fake_http_runner(**kwargs: object) -> tuple[int, str]:
        calls.append(dict(kwargs))
        packet_dir = lake_packets_root / str(kwargs["source_surface"])
        _write_manifest(
            packet_dir,
            packet_id="01KW0000000000000000000004",
            source_surface=str(kwargs["source_surface"]),
            access_value="lake direct HTTP succeeded",
        )
        return 0, str(packet_dir)

    def fake_cloakbrowser_runner(**kwargs: object) -> tuple[int, str]:
        calls.append(dict(kwargs))
        packet_dir = lake_packets_root / str(kwargs["source_surface"])
        packet_id = (
            "01KW0000000000000000000005"
            if kwargs["source_surface"] == runner.INITIAL_VIEWPORT_SURFACE
            else "01KW0000000000000000000006"
        )
        _write_manifest(
            packet_dir,
            packet_id=packet_id,
            source_surface=str(kwargs["source_surface"]),
            access_value=f"lake {kwargs['source_surface']} succeeded",
        )
        return 0, str(packet_dir)

    output_root = tmp_path / "bundle_summary"

    exit_code, message = runner.run_fragrantica_mgt_capture(
        url=_URL,
        output_root=output_root,
        data_root=data_root,  # type: ignore[arg-type]
        http_runner=fake_http_runner,
        cloakbrowser_runner=fake_cloakbrowser_runner,
    )

    assert exit_code == 0
    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    assert summary["packet_publication_mode"] == "data_lake_raw_packets_with_local_summary"
    assert summary["data_root"] == str(data_root.path)
    assert summary["packet_roles"][runner.DIRECT_HTTP_SLOT]["packet_path"] == str(
        lake_packets_root / runner.DIRECT_HTTP_SURFACE
    )
    assert summary["packet_roles"][runner.DEEP_SCROLL_SLOT]["access_posture"]["value"] == (
        f"lake {runner.DEEP_SCROLL_SURFACE} succeeded"
    )
    assert all(call["data_root"] is data_root for call in calls)
    assert all(call["output_directory"] is None for call in calls)


def test_preflight_does_not_create_output_root(tmp_path: Path, capsys) -> None:
    output_root = tmp_path / "preflight_bundle"

    exit_code = runner.main(
        [
            "--url",
            _URL,
            "--output-root",
            str(output_root),
            "--preflight-only",
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "no network capture attempted" in captured.out
    assert "product_id=33519" in captured.out
    assert not output_root.exists()


def test_preflight_rejects_lookalike_fragrantica_hosts(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="absolute fragrantica.com URL"):
        runner.preflight_fragrantica_mgt_capture(
            url="https://notfragrantica.com/perfume/Fake/Fake-1.html",
            output_root=tmp_path / "blocked",
        )

    message = runner.preflight_fragrantica_mgt_capture(
        url="https://www.fragrantica.com/perfume/Fake/Fake-1.html",
        output_root=tmp_path / "allowed",
    )
    assert "preflight passed" in message


def test_nonempty_output_root_fails_before_capture(tmp_path: Path) -> None:
    output_root = tmp_path / "bundle"
    output_root.mkdir()
    (output_root / "existing.txt").write_text("do not overwrite", encoding="utf-8")

    with pytest.raises(ValueError, match="output root must be absent or empty"):
        runner.run_fragrantica_mgt_capture(
            url=_URL,
            output_root=output_root,
            http_runner=lambda **_kwargs: (0, "should-not-run"),
            cloakbrowser_runner=lambda **_kwargs: (0, "should-not-run"),
        )


def test_missing_packet_manifest_fails_visibly(tmp_path: Path) -> None:
    def fake_http_runner(**_kwargs: object) -> tuple[int, str]:
        packet_dir = tmp_path / "packet_without_manifest"
        packet_dir.mkdir()
        return 0, str(packet_dir)

    with pytest.raises(ValueError, match="packet manifest not found"):
        runner.run_fragrantica_mgt_capture(
            url=_URL,
            output_root=tmp_path / "bundle",
            http_runner=fake_http_runner,
            cloakbrowser_runner=lambda **_kwargs: pytest.fail("cloakbrowser should not run"),
        )


def test_sub_runner_failure_returns_slot_message_without_summary(tmp_path: Path) -> None:
    output_root = tmp_path / "bundle"

    exit_code, message = runner.run_fragrantica_mgt_capture(
        url=_URL,
        output_root=output_root,
        http_runner=lambda **_kwargs: (12, "network stopped"),
        cloakbrowser_runner=lambda **_kwargs: pytest.fail("cloakbrowser should not run"),
    )

    assert exit_code == 12
    assert message == f"{runner.DIRECT_HTTP_SLOT} failed: network stopped"
    assert not (output_root / runner.SUMMARY_FILENAME).exists()
