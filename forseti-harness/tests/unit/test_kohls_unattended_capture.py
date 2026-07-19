from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

import runners.run_kohls_unattended_capture as unattended


def test_parse_docker_port_accepts_private_ipv4() -> None:
    assert unattended._parse_docker_port("127.0.0.1:49153\n") == 49153


def test_parse_docker_port_rejects_public_binding() -> None:
    with pytest.raises(unattended.UnattendedCaptureError):
        unattended._parse_docker_port("0.0.0.0:49153\n")


def test_docker_timeout_is_a_typed_visible_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd=args[0], timeout=kwargs["timeout"])

    monkeypatch.setattr(subprocess, "run", timeout)

    with pytest.raises(unattended.UnattendedCaptureError, match="exceeded 2s"):
        unattended._docker(["image", "inspect", "example"], timeout_seconds=2)


def test_capture_kohls_surfaces_forwards_lake_and_unattended_provenance(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[dict] = []

    def fake_capture(**kwargs):
        calls.append(kwargs)
        return 0, f"/packet/{kwargs['source_family']}"

    monkeypatch.setattr(
        unattended,
        "run_source_capture_realchrome_cdp_packet",
        fake_capture,
    )
    lake = object()

    outcomes = unattended.capture_kohls_surfaces(
        data_root=lake,
        cdp_endpoint="http://127.0.0.1:49153",
        chrome_no_sandbox=True,
    )

    assert [outcome.surface for outcome in outcomes] == ["pdp", "policy"]
    assert len(calls) == 2
    assert all(call["data_root"] is lake for call in calls)
    assert all(call["browser_provisioning"] == "unattended_xvfb" for call in calls)
    assert all(call["persistent_profile_loaded"] is True for call in calls)
    assert all(
        any("chrome_inner_sandbox_disabled" in item for item in call["limitations"])
        for call in calls
    )


def test_job_stops_its_container_when_capture_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    stopped: list[str] = []
    monkeypatch.setattr(unattended, "_ensure_image", lambda **kwargs: False)
    monkeypatch.setattr(
        unattended,
        "_start_browser",
        lambda **kwargs: "forseti-kohls-xvfb-test",
    )
    monkeypatch.setattr(
        unattended,
        "_wait_for_cdp",
        lambda **kwargs: "http://127.0.0.1:49153",
    )
    monkeypatch.setattr(
        unattended,
        "capture_kohls_surfaces",
        lambda **kwargs: (_ for _ in ()).throw(RuntimeError("capture failed")),
    )
    monkeypatch.setattr(
        unattended,
        "_stop_browser",
        lambda name: stopped.append(name),
    )

    with pytest.raises(RuntimeError, match="capture failed"):
        unattended.run_unattended_job(data_root=object())

    assert stopped == ["forseti-kohls-xvfb-test"]
