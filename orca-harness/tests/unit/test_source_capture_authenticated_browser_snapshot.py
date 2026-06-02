from __future__ import annotations

import json
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path

import pytest

from runners import run_source_capture_authenticated_browser_packet as auth_runner
from runners import run_source_capture_browser_session_bootstrap as bootstrap_runner
from runners.run_source_capture_browser_session_bootstrap import run_browser_session_bootstrap
from source_capture import AuthenticatedSessionMode, CaptureModeCategory
from source_capture.adapters.browser_snapshot import BrowserSnapshotSuccess
from source_capture.auth_state import auth_state_path_for_label, validate_auth_state_file, write_auth_state_metadata


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"source_capture_authenticated_browser_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def test_session_modes_are_fixed_vocabulary() -> None:
    assert [item.value for item in AuthenticatedSessionMode] == [
        "free_account_created_session",
        "paid_entitled_session",
        "client_provided_session",
        "consenting_coworker_session",
    ]


def test_authenticated_browser_clis_expose_no_secret_or_password_flags() -> None:
    forbidden_destinations = {"password", "username", "token", "cookie", "profile"}
    forbidden_options = {
        "--password",
        "--username",
        "--token",
        "--cookie",
        "--profile",
        "--profile-path",
        "--storage-state-path",
    }
    parsers = [
        auth_runner._build_parser(),
        bootstrap_runner._build_parser(),
    ]
    for parser in parsers:
        destinations = {action.dest for action in parser._actions}
        options = {
            option
            for action in parser._actions
            for option in action.option_strings
        }
        assert destinations.isdisjoint(forbidden_destinations)
        assert options.isdisjoint(forbidden_options)


def test_auth_state_label_rejects_path_traversal(scratch_dir: Path) -> None:
    with pytest.raises(ValueError, match="auth-state label"):
        auth_state_path_for_label("../outside", auth_state_root=scratch_dir)
    with pytest.raises(ValueError, match="auth-state label"):
        auth_state_path_for_label("nested/state", auth_state_root=scratch_dir)


def test_validate_auth_state_file_rejects_missing_and_bad_shape(scratch_dir: Path) -> None:
    with pytest.raises(ValueError, match="does not exist"):
        validate_auth_state_file("missing", auth_state_root=scratch_dir)

    path = auth_state_path_for_label("bad", auth_state_root=scratch_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('{"cookies": {}}', encoding="utf-8")
    with pytest.raises(ValueError, match="cookies/origins"):
        validate_auth_state_file("bad", auth_state_root=scratch_dir)


@dataclass(frozen=True)
class _FakeBootstrapEngine:
    payload: str = '{"cookies": [], "origins": []}'

    def save_storage_state(
        self,
        *,
        login_url: str,
        timeout_seconds: float,
        state_path: Path,
    ) -> str:
        state_path.write_text(self.payload, encoding="utf-8")
        return login_url


def _write_auth_state_pair(
    auth_root: Path,
    state_label: str,
    session_mode: AuthenticatedSessionMode,
    payload: str = '{"cookies": [], "origins": []}',
) -> Path:
    auth_root.mkdir(parents=True, exist_ok=True)
    state_path = auth_state_path_for_label(state_label, auth_state_root=auth_root)
    state_path.write_text(payload, encoding="utf-8")
    write_auth_state_metadata(
        state_label,
        session_mode=session_mode,
        auth_state_root=auth_root,
    )
    return state_path


def test_session_bootstrap_writes_auth_state_and_sidecar_without_packet(scratch_dir: Path) -> None:
    auth_root = scratch_dir / "_auth_state"

    exit_code, message = run_browser_session_bootstrap(
        login_url="https://example.com/login",
        state_label="free-example",
        session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
        timeout_seconds=5,
        auth_state_root=auth_root,
        engine=_FakeBootstrapEngine(),
    )

    state_path = auth_root / "free-example.json"
    metadata_path = auth_root / "free-example.meta.json"
    assert exit_code == 0
    assert "free_account_created_session" in message
    assert str(state_path) not in message
    assert state_path.exists()
    assert metadata_path.exists()
    assert json.loads(metadata_path.read_text(encoding="utf-8")) == {
        "auth_state_file": "free-example.json",
        "session_mode": "free_account_created_session",
    }
    assert not (scratch_dir / "manifest.json").exists()
    assert not (scratch_dir / "receipt.md").exists()


def test_authenticated_browser_runner_writes_packet_without_state_leakage(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    auth_root = scratch_dir / "_auth_state"
    state_path = _write_auth_state_pair(
        auth_root,
        "client-example",
        AuthenticatedSessionMode.CLIENT_PROVIDED,
        payload='{"cookies": [{"name": "sessionid", "value": "SECRET_COOKIE_VALUE"}], "origins": []}',
    )
    output_dir = scratch_dir / "packet"
    captured_storage_paths: list[Path] = []

    def fake_capture(**kwargs: object) -> BrowserSnapshotSuccess:
        captured_storage_paths.append(kwargs["storage_state_path"])
        return BrowserSnapshotSuccess(
            requested_url="https://example.com/entitled",
            final_url="https://example.com/entitled",
            title="Entitled Source",
            rendered_dom="<html><body><main>Unlocked source language</main></body></html>",
            visible_text="Unlocked source language",
            screenshot_png=b"\x89PNG\r\n\x1a\nauth-browser",
            metadata={
                "requested_url": "https://example.com/entitled",
                "final_url": "https://example.com/entitled",
                "title": "Entitled Source",
                "capture_timestamp": "2026-06-03T01:02:03Z",
                "timeout_seconds": kwargs["timeout_seconds"],
                "wait_until": kwargs["wait_until"],
                "viewport_width": kwargs["viewport_width"],
                "viewport_height": kwargs["viewport_height"],
                "screenshot_mode": "viewport",
                "storage_state_loaded": True,
                "rendered_dom_byte_count": 66,
                "visible_text_byte_count": 24,
                "screenshot_byte_count": 18,
            },
            warning_notes=[],
            limitation_notes=[],
        )

    monkeypatch.setattr(auth_runner, "fetch_browser_snapshot_capture", fake_capture)

    exit_code, message = auth_runner.run_source_capture_authenticated_browser_packet(
        url="https://example.com/entitled",
        state_label="client-example",
        session_mode=AuthenticatedSessionMode.CLIENT_PROVIDED,
        source_family="authenticated_web_page",
        source_surface="authenticated_browser_snapshot",
        decision_question="What authenticated source was visible before cutoff?",
        output_directory=output_dir,
        capture_context="test authenticated browser snapshot",
        operator_category="authenticated_browser_snapshot_cli_operator",
        capture_mode=CaptureModeCategory.MULTIMODAL,
        session_id=None,
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
        max_artifact_bytes=5_000,
        auth_state_root=auth_root,
    )

    assert exit_code == 0
    assert message == str(output_dir.resolve())
    assert captured_storage_paths == [state_path]
    manifest_text = (output_dir / "manifest.json").read_text(encoding="utf-8")
    receipt_text = (output_dir / "receipt.md").read_text(encoding="utf-8")
    raw_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in (output_dir / "raw").iterdir()
        if path.suffix != ".png"
    )
    combined_text = f"{manifest_text}\n{receipt_text}\n{raw_text}"
    assert "SECRET_COOKIE_VALUE" not in combined_text
    assert str(state_path) not in combined_text

    manifest = json.loads(manifest_text)
    assert manifest["source_surface"] == "authenticated_browser_snapshot"
    assert manifest["source_slices"][0]["slice_id"] == "authenticated_browser_snapshot_01"
    assert manifest["preserved_files"][0]["relative_packet_path"] == (
        "raw/01_authenticated_browser_rendered_dom.html"
    )
    assert "client_provided_session" in manifest["access_posture"]["value"]
    assert "authenticated_browser_storage_state_loaded:client_provided_session:client-example" in (
        manifest["visible_mode_changes"]
    )
    assert manifest["receipt_metadata"]["non_claims"] == (
        auth_runner.AUTHENTICATED_BROWSER_SNAPSHOT_NON_CLAIMS
    )


def test_authenticated_browser_runner_rejects_session_mode_mismatch(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    auth_root = scratch_dir / "_auth_state"
    _write_auth_state_pair(
        auth_root,
        "coworker-example",
        AuthenticatedSessionMode.CONSENTING_COWORKER,
    )

    def fake_capture(**kwargs: object) -> BrowserSnapshotSuccess:
        raise AssertionError("capture must not run when session mode metadata mismatches")

    monkeypatch.setattr(auth_runner, "fetch_browser_snapshot_capture", fake_capture)

    with pytest.raises(ValueError, match="session mode mismatch"):
        auth_runner.run_source_capture_authenticated_browser_packet(
            url="https://example.com/entitled",
            state_label="coworker-example",
            session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
            source_family="authenticated_web_page",
            source_surface="authenticated_browser_snapshot",
            decision_question="What authenticated source was visible before cutoff?",
            output_directory=scratch_dir / "packet",
            capture_context="test authenticated browser snapshot",
            operator_category="authenticated_browser_snapshot_cli_operator",
            capture_mode=CaptureModeCategory.MULTIMODAL,
            session_id=None,
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
            max_artifact_bytes=5_000,
            auth_state_root=auth_root,
        )

    assert not (scratch_dir / "packet").exists()


def test_authenticated_browser_runner_adds_possible_login_wall_limitation(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    auth_root = scratch_dir / "_auth_state"
    _write_auth_state_pair(
        auth_root,
        "free-example",
        AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
    )

    def fake_capture(**kwargs: object) -> BrowserSnapshotSuccess:
        return BrowserSnapshotSuccess(
            requested_url="https://example.com/login",
            final_url="https://example.com/login",
            title="Sign in",
            rendered_dom="<html><body>Password</body></html>",
            visible_text="Sign in with password",
            screenshot_png=b"\x89PNG\r\n\x1a\nauth-browser",
            metadata={
                "requested_url": "https://example.com/login",
                "final_url": "https://example.com/login",
                "title": "Sign in",
                "capture_timestamp": "2026-06-03T01:02:03Z",
                "timeout_seconds": kwargs["timeout_seconds"],
                "wait_until": kwargs["wait_until"],
                "viewport_width": kwargs["viewport_width"],
                "viewport_height": kwargs["viewport_height"],
                "screenshot_mode": "viewport",
                "storage_state_loaded": True,
                "rendered_dom_byte_count": 34,
                "visible_text_byte_count": 21,
                "screenshot_byte_count": 18,
            },
            warning_notes=[],
            limitation_notes=[],
        )

    monkeypatch.setattr(auth_runner, "fetch_browser_snapshot_capture", fake_capture)

    exit_code, _ = auth_runner.run_source_capture_authenticated_browser_packet(
        url="https://example.com/login",
        state_label="free-example",
        session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
        source_family="authenticated_web_page",
        source_surface="authenticated_browser_snapshot",
        decision_question="What authenticated source was visible before cutoff?",
        output_directory=scratch_dir / "packet",
        capture_context="test authenticated browser snapshot",
        operator_category="authenticated_browser_snapshot_cli_operator",
        capture_mode=CaptureModeCategory.MULTIMODAL,
        session_id=None,
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
        max_artifact_bytes=5_000,
        auth_state_root=auth_root,
    )

    assert exit_code == 0
    manifest = json.loads((scratch_dir / "packet" / "manifest.json").read_text(encoding="utf-8"))
    assert any("possible_login_wall_or_auth_challenge_visible" in item for item in manifest["limitations"])


def test_authenticated_browser_runner_cleans_staged_files_when_packet_write_fails(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    auth_root = scratch_dir / "_auth_state"
    _write_auth_state_pair(
        auth_root,
        "client-example",
        AuthenticatedSessionMode.CLIENT_PROVIDED,
    )
    output_dir = scratch_dir / "packet"

    def fake_capture(**kwargs: object) -> BrowserSnapshotSuccess:
        return BrowserSnapshotSuccess(
            requested_url="https://example.com/entitled",
            final_url="https://example.com/entitled",
            title="Entitled Source",
            rendered_dom="<html><body>Unlocked source language</body></html>",
            visible_text="Unlocked source language",
            screenshot_png=b"\x89PNG\r\n\x1a\nauth-browser",
            metadata={
                "requested_url": "https://example.com/entitled",
                "final_url": "https://example.com/entitled",
                "title": "Entitled Source",
                "capture_timestamp": "2026-06-03T01:02:03Z",
                "timeout_seconds": kwargs["timeout_seconds"],
                "wait_until": kwargs["wait_until"],
                "viewport_width": kwargs["viewport_width"],
                "viewport_height": kwargs["viewport_height"],
                "screenshot_mode": "viewport",
                "storage_state_loaded": True,
                "rendered_dom_byte_count": 51,
                "visible_text_byte_count": 24,
                "screenshot_byte_count": 18,
            },
            warning_notes=[],
            limitation_notes=[],
        )

    def fake_packet_writer(**kwargs: object) -> object:
        raise RuntimeError("packet writer failed")

    monkeypatch.setattr(auth_runner, "fetch_browser_snapshot_capture", fake_capture)
    monkeypatch.setattr(auth_runner, "write_local_source_capture_packet", fake_packet_writer)

    with pytest.raises(RuntimeError, match="packet writer failed"):
        auth_runner.run_source_capture_authenticated_browser_packet(
            url="https://example.com/entitled",
            state_label="client-example",
            session_mode=AuthenticatedSessionMode.CLIENT_PROVIDED,
            source_family="authenticated_web_page",
            source_surface="authenticated_browser_snapshot",
            decision_question="What authenticated source was visible before cutoff?",
            output_directory=output_dir,
            capture_context="test authenticated browser snapshot",
            operator_category="authenticated_browser_snapshot_cli_operator",
            capture_mode=CaptureModeCategory.MULTIMODAL,
            session_id=None,
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
            max_artifact_bytes=5_000,
            auth_state_root=auth_root,
        )

    assert not output_dir.exists()
    assert not (output_dir.parent / "authenticated_browser_rendered_dom.html").exists()
    assert not (output_dir.parent / "authenticated_browser_visible_text.txt").exists()
    assert not (output_dir.parent / "authenticated_browser_viewport_screenshot.png").exists()
    assert not (output_dir.parent / "authenticated_browser_snapshot_metadata.json").exists()
