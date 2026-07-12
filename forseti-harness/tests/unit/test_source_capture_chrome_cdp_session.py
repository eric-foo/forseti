from __future__ import annotations

import json
from pathlib import Path

from runners import run_source_capture_chrome_cdp_session as runner
from source_capture.auth_state import (
    AuthenticatedSessionMode,
    validate_auth_state_provenance_requirement,
)
from source_capture.source_access_provenance import HarnessProxyProfilePosture


def test_chrome_cdp_session_bootstrap_exports_no_proxy_state_and_leaves_browser(
    tmp_path: Path,
    monkeypatch,
) -> None:
    chrome = tmp_path / "chrome.exe"
    chrome.write_bytes(b"test")
    launched: list[list[str]] = []
    events: list[str] = []

    class FakeProcess:
        pass

    def fake_popen(args: list[str]) -> FakeProcess:
        launched.append(list(args))
        return FakeProcess()

    class FakeContext:
        def storage_state(self, *, path: str) -> None:
            Path(path).write_text(
                json.dumps({"cookies": [], "origins": []}), encoding="utf-8"
            )

    class FakeBrowser:
        contexts = [FakeContext()]

        def close(self) -> None:
            events.append("browser_disconnect")

    class FakeChromium:
        def connect_over_cdp(self, endpoint: str) -> FakeBrowser:
            events.append(f"attach:{endpoint}")
            return FakeBrowser()

    class FakeOwner:
        chromium = FakeChromium()

        def stop(self) -> None:
            events.append("playwright_stop")

    class FakeStarter:
        @staticmethod
        def start() -> FakeOwner:
            return FakeOwner()

    class FakeSyncApi:
        @staticmethod
        def sync_playwright() -> FakeStarter:
            return FakeStarter()

    monkeypatch.setattr(runner.subprocess, "Popen", fake_popen)
    monkeypatch.setattr(runner, "input", lambda: "", raising=False)
    monkeypatch.setattr(
        runner,
        "import_module",
        lambda name: FakeSyncApi() if name == "playwright.sync_api" else None,
    )
    auth_root = tmp_path / "auth"
    profile_root = tmp_path / "profiles"

    code, _ = runner.launch_and_export_chrome_cdp_session(
        user_data_label="chowdakr_sg_tiktok_chrome_v1",
        state_label="chowdakr_sg_tiktok_chrome_v1",
        session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
        auth_state_root=auth_root,
        browser_user_data_root=profile_root,
        chrome_executable=chrome,
    )

    assert code == 0
    assert launched and "--remote-debugging-address=127.0.0.1" in launched[0]
    assert not any("extension" in arg.lower() for arg in launched[0])
    assert events == [
        "attach:http://127.0.0.1:9222",
        "browser_disconnect",
        "playwright_stop",
    ]
    state_path = validate_auth_state_provenance_requirement(
        "chowdakr_sg_tiktok_chrome_v1",
        session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
        required_harness_proxy_profile_posture=(
            HarnessProxyProfilePosture.NO_PROXY_PROFILE_LOADED
        ),
        auth_state_root=auth_root,
    )
    assert state_path.is_file()
