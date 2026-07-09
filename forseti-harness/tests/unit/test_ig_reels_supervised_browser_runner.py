from __future__ import annotations

from pathlib import Path

import pytest

import runners.run_source_capture_ig_reels_supervised_browser as supervised_runner
from runners.run_source_capture_ig_reels_supervised_browser import (
    main as supervised_main,
)
from runners.run_source_capture_ig_reels_supervised_browser import (
    run_ig_reels_supervised_browser,
)


class _FakeProcess:
    def __init__(self) -> None:
        self.polls_before_exit: list[int | None] = [None, 0]

    def poll(self) -> int | None:
        if self.polls_before_exit:
            return self.polls_before_exit.pop(0)
        return 0


class _FakeCloakBrowser:
    def __init__(self) -> None:
        self.ensure_binary_calls = 0
        self.build_args_calls: list[dict[str, object]] = []

    def ensure_binary(self) -> str:
        self.ensure_binary_calls += 1
        return "C:/cloak/chrome.exe"

    def build_args(
        self,
        stealth_args: bool,
        extra_args: list[str] | None,
        *,
        headless: bool,
    ) -> list[str]:
        self.build_args_calls.append(
            {
                "stealth_args": stealth_args,
                "extra_args": list(extra_args or []),
                "headless": headless,
            }
        )
        return ["--built-by-cloakbrowser", *(extra_args or [])]


def test_supervised_browser_uses_direct_headed_cloakbrowser_profile(tmp_path: Path) -> None:
    fake = _FakeCloakBrowser()
    launched: list[list[str]] = []

    def fake_process_factory(args: object) -> _FakeProcess:
        launched.append(list(args))
        return _FakeProcess()

    exit_code, message = run_ig_reels_supervised_browser(
        handles=("@milanscents",),
        profile_urls=("https://www.instagram.com/jeremyfragrance/reels/",),
        browser_user_data_label="aphrodite-ig-us-fragrance",
        browser_user_data_root=tmp_path / "user-data",
        viewport_width=1440,
        viewport_height=2200,
        zoom=0.67,
        wait_for_operator=False,
        cloakbrowser_module=fake,
        process_factory=fake_process_factory,
    )

    assert exit_code == 0
    assert "2 url(s)" in message
    assert fake.ensure_binary_calls == 1
    assert fake.build_args_calls == [
        {
            "stealth_args": False,
            "extra_args": [
                "--disable-popup-blocking",
                "--no-first-run",
                "--no-default-browser-check",
                f"--user-data-dir={tmp_path / 'user-data' / 'aphrodite-ig-us-fragrance'}",
                "--window-size=1440,2200",
                "--force-device-scale-factor=0.67",
            ],
            "headless": False,
        }
    ]
    assert launched == [
        [
            "C:/cloak/chrome.exe",
            "--built-by-cloakbrowser",
            "--disable-popup-blocking",
            "--no-first-run",
            "--no-default-browser-check",
            f"--user-data-dir={tmp_path / 'user-data' / 'aphrodite-ig-us-fragrance'}",
            "--window-size=1440,2200",
            "--force-device-scale-factor=0.67",
            "https://www.instagram.com/milanscents/reels/",
            "https://www.instagram.com/jeremyfragrance/reels/",
        ]
    ]


def test_supervised_browser_waits_for_operator_without_closing_browser(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake = _FakeCloakBrowser()
    prompts: list[str] = []

    def fake_input() -> str:
        prompts.append("waited")
        return ""

    monkeypatch.setattr("builtins.input", fake_input)

    exit_code, _message = run_ig_reels_supervised_browser(
        handles=("milanscents",),
        browser_user_data_label="aphrodite-ig-supervised",
        browser_user_data_root=tmp_path / "user-data",
        wait_for_operator=True,
        cloakbrowser_module=fake,
        process_factory=lambda _args: _FakeProcess(),
    )

    assert exit_code == 0
    assert prompts == ["waited"]


def test_supervised_browser_hold_open_until_browser_exits(tmp_path: Path) -> None:
    fake = _FakeCloakBrowser()
    process = _FakeProcess()

    exit_code, _message = run_ig_reels_supervised_browser(
        handles=("milanscents",),
        browser_user_data_label="aphrodite-ig-supervised",
        browser_user_data_root=tmp_path / "user-data",
        wait_for_operator=False,
        hold_open_until_killed=True,
        cloakbrowser_module=fake,
        process_factory=lambda _args: process,
    )

    assert exit_code == 0
    assert process.polls_before_exit == []


def test_supervised_browser_hold_open_preserves_interrupt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fake = _FakeCloakBrowser()
    process = _FakeProcess()
    process.polls_before_exit = [None]

    def fake_sleep(_seconds: float) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr(supervised_runner.time, "sleep", fake_sleep)

    with pytest.raises(KeyboardInterrupt):
        run_ig_reels_supervised_browser(
            handles=("milanscents",),
            browser_user_data_label="aphrodite-ig-supervised",
            browser_user_data_root=tmp_path / "user-data",
            wait_for_operator=False,
            hold_open_until_killed=True,
            cloakbrowser_module=fake,
            process_factory=lambda _args: process,
        )


def test_supervised_browser_rejects_missing_locator(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="supply at least one"):
        run_ig_reels_supervised_browser(
            browser_user_data_label="aphrodite-ig-supervised",
            browser_user_data_root=tmp_path / "user-data",
            wait_for_operator=False,
            cloakbrowser_module=_FakeCloakBrowser(),
            process_factory=lambda _args: _FakeProcess(),
        )


def test_supervised_browser_cli_threads_options(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    def fake_run(**kwargs: object) -> tuple[int, str]:
        captured.update(kwargs)
        return 0, "opened"

    monkeypatch.setattr(
        "runners.run_source_capture_ig_reels_supervised_browser.run_ig_reels_supervised_browser",
        fake_run,
    )

    assert supervised_main(
        [
            "--handle",
            "milanscents",
            "--browser-user-data-label",
            "aphrodite-ig-supervised",
            "--viewport-width",
            "1200",
            "--viewport-height",
            "1800",
            "--zoom",
            "0.5",
            "--no-wait",
        ]
    ) == 0

    assert captured["handles"] == ["milanscents"]
    assert captured["profile_urls"] == []
    assert captured["browser_user_data_label"] == "aphrodite-ig-supervised"
    assert captured["viewport_width"] == 1200
    assert captured["viewport_height"] == 1800
    assert captured["zoom"] == 0.5
    assert captured["wait_for_operator"] is False
    assert captured["hold_open_until_killed"] is False
