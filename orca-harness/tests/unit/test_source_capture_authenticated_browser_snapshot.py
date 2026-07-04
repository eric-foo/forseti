from __future__ import annotations

import builtins
import hashlib
import json
import shutil
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path

import pytest

from runners import run_source_capture_authenticated_browser_packet as auth_runner
from runners import run_source_capture_browser_session_bootstrap as bootstrap_runner
from runners import run_source_capture_browser_user_data_export as export_runner
from runners import run_source_capture_cloakbrowser_profile_warmup as warmup_runner
from runners.run_source_capture_browser_session_bootstrap import run_browser_session_bootstrap
from runners.run_source_capture_browser_user_data_export import run_browser_user_data_export
from runners.run_source_capture_cloakbrowser_profile_warmup import run_cloakbrowser_profile_warmup
from source_capture import AuthenticatedSessionMode, CaptureModeCategory
from source_capture.adapters.browser_snapshot import BrowserSnapshotSuccess
from source_capture.auth_state import auth_state_path_for_label, validate_auth_state_file, write_auth_state_metadata
from source_capture.browser_user_data import (
    browser_user_data_path_for_label,
    browser_user_data_provenance_path_for_label,
)
from source_capture.proxy_profiles import ProxyProfile
from source_capture.source_access_provenance import build_browser_user_data_source_access_provenance


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
        "--user-data-dir",
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
    assert "--browser-backend" in options
    assert "--cloakbrowser-humanize" in options
    assert "--cloakbrowser-user-data-label" in options


def test_browser_user_data_export_cli_exposes_no_secret_or_path_flags() -> None:
    forbidden_destinations = {"password", "username", "token", "cookie", "profile", "user_data_dir"}
    forbidden_options = {
        "--password",
        "--username",
        "--token",
        "--cookie",
        "--profile",
        "--profile-path",
        "--storage-state-path",
        "--user-data-dir",
        "--login-url",
    }
    parser = export_runner._build_parser()
    destinations = {action.dest for action in parser._actions}
    options = {option for action in parser._actions for option in action.option_strings}

    assert destinations.isdisjoint(forbidden_destinations)
    assert options.isdisjoint(forbidden_options)
    assert "--user-data-label" in options
    assert "--state-label" in options
    assert "--session-mode" in options


def test_cloakbrowser_profile_warmup_cli_exposes_no_secret_or_path_flags() -> None:
    forbidden_destinations = {"password", "username", "token", "cookie", "profile", "user_data_dir"}
    forbidden_options = {
        "--password",
        "--username",
        "--token",
        "--cookie",
        "--profile",
        "--profile-path",
        "--storage-state-path",
        "--user-data-dir",
    }
    parser = warmup_runner._build_parser()
    destinations = {action.dest for action in parser._actions}
    options = {option for action in parser._actions for option in action.option_strings}

    assert destinations.isdisjoint(forbidden_destinations)
    assert options.isdisjoint(forbidden_options)
    assert "--user-data-label" in options
    assert "--proxy-profile-label" in options
    assert "--proxy-profile-root" in options


def test_auth_state_label_rejects_path_traversal(scratch_dir: Path) -> None:
    with pytest.raises(ValueError, match="auth-state label"):
        auth_state_path_for_label("../outside", auth_state_root=scratch_dir)
    with pytest.raises(ValueError, match="auth-state label"):
        auth_state_path_for_label("nested/state", auth_state_root=scratch_dir)


def test_browser_user_data_label_rejects_path_traversal(scratch_dir: Path) -> None:
    with pytest.raises(ValueError, match="browser user-data label"):
        browser_user_data_path_for_label("../outside", user_data_root=scratch_dir)
    with pytest.raises(ValueError, match="browser user-data label"):
        browser_user_data_path_for_label("nested/state", user_data_root=scratch_dir)


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


class _FakeWarmupEngine:
    def __init__(self) -> None:
        self.user_data_dirs: list[Path] = []
        self.proxy_profiles: list[ProxyProfile | None] = []

    def warm_profile(
        self, *, login_url: str, user_data_dir: Path, proxy_profile: ProxyProfile | None
    ) -> str:
        self.user_data_dirs.append(user_data_dir)
        self.proxy_profiles.append(proxy_profile)
        return login_url


def test_cloakbrowser_profile_warmup_uses_label_indirected_user_data_without_auth_state(
    scratch_dir: Path,
) -> None:
    user_data_root = scratch_dir / "_browser_user_data"
    engine = _FakeWarmupEngine()

    exit_code, message = run_cloakbrowser_profile_warmup(
        login_url="https://example.com/login",
        user_data_label="google-login",
        user_data_root=user_data_root,
        engine=engine,
    )

    assert exit_code == 0
    assert engine.user_data_dirs == [user_data_root / "google-login"]
    assert (user_data_root / "google-login").is_dir()
    assert "google-login" in message
    assert str(user_data_root) not in message
    assert engine.proxy_profiles == [None]
    assert not (scratch_dir / "_auth_state").exists()


def test_cloakbrowser_profile_warmup_uses_proxy_profile_label_without_secret_output(
    scratch_dir: Path,
) -> None:
    user_data_root = scratch_dir / "_browser_user_data"
    profile_root = scratch_dir / "_proxy_profiles"
    profile_root.mkdir(parents=True)
    (profile_root / "reddit-res.json").write_text(
        json.dumps({"server": "http://user:SUPER_SECRET_PROXY_VALUE@proxy.example:8080"}),
        encoding="utf-8",
    )
    (profile_root / "reddit-res.meta.json").write_text(
        json.dumps(
            {
                "profile_file": "reddit-res.json",
                "proxy_category": "residential_rotating",
                "geoip_enabled": False,
                "timezone": "America/New_York",
                "locale": "en-US",
            }
        ),
        encoding="utf-8",
    )
    engine = _FakeWarmupEngine()

    exit_code, message = run_cloakbrowser_profile_warmup(
        login_url="https://example.com/login",
        user_data_label="google-login",
        user_data_root=user_data_root,
        proxy_profile_label="reddit-res",
        proxy_profile_root=profile_root,
        engine=engine,
    )

    assert exit_code == 0
    assert engine.user_data_dirs == [user_data_root / "google-login"]
    assert engine.proxy_profiles[0] is not None
    assert engine.proxy_profiles[0].proxy_category.value == "residential_rotating"
    assert "reddit-res" in message
    assert "residential_rotating" in message
    assert "SUPER_SECRET_PROXY_VALUE" not in message
    assert "proxy.example" not in message
    assert str(profile_root) not in message
    assert not (scratch_dir / "_auth_state").exists()




def test_cloakbrowser_profile_warmup_writes_no_proxy_profile_provenance_sidecar(
    scratch_dir: Path,
) -> None:
    user_data_root = scratch_dir / "_browser_user_data"
    engine = _FakeWarmupEngine()

    run_cloakbrowser_profile_warmup(
        login_url="https://example.com/login",
        user_data_label="google-login",
        user_data_root=user_data_root,
        engine=engine,
    )

    provenance_path = browser_user_data_provenance_path_for_label(
        "google-login",
        user_data_root=user_data_root,
    )
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    assert provenance["schema_version"] == 1
    assert provenance["browser_backend"] == "cloakbrowser"
    assert provenance["harness_proxy_profile_posture"] == "no_proxy_profile_loaded"
    assert provenance["proxy_category"] == "none"
    assert len(provenance["browser_user_data_label_sha256"]) == 64
    assert "google-login" not in json.dumps(provenance)


def test_cloakbrowser_profile_warmup_writes_proxy_profile_provenance_without_secret_material(
    scratch_dir: Path,
) -> None:
    user_data_root = scratch_dir / "_browser_user_data"
    profile_root = scratch_dir / "_proxy_profiles"
    profile_root.mkdir(parents=True)
    (profile_root / "reddit-res.json").write_text(
        json.dumps({"server": "http://user:SUPER_SECRET_PROXY_VALUE@proxy.example:8080"}),
        encoding="utf-8",
    )
    (profile_root / "reddit-res.meta.json").write_text(
        json.dumps(
            {
                "profile_file": "reddit-res.json",
                "proxy_category": "residential_rotating",
                "geoip_enabled": False,
            }
        ),
        encoding="utf-8",
    )

    run_cloakbrowser_profile_warmup(
        login_url="https://example.com/login",
        user_data_label="google-login",
        user_data_root=user_data_root,
        proxy_profile_label="reddit-res",
        proxy_profile_root=profile_root,
        engine=_FakeWarmupEngine(),
    )

    provenance = json.loads(
        browser_user_data_provenance_path_for_label(
            "google-login",
            user_data_root=user_data_root,
        ).read_text(encoding="utf-8")
    )
    serialized = json.dumps(provenance)
    assert provenance["harness_proxy_profile_posture"] == "proxy_profile_loaded"
    assert provenance["proxy_category"] == "residential_rotating"
    assert "SUPER_SECRET_PROXY_VALUE" not in serialized
    assert "proxy.example" not in serialized
    assert str(profile_root) not in serialized


class _FakeDirectWarmupProcess:
    def __init__(self, *, poll_result: int | None) -> None:
        self.poll_result = poll_result
        self.wait_called = False

    def wait(self) -> int:
        self.wait_called = True
        self.poll_result = 0
        return 0

    def poll(self) -> int | None:
        return self.poll_result


def test_direct_warmup_waits_for_browser_exit_when_stdin_is_unavailable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    process = _FakeDirectWarmupProcess(poll_result=None)

    def raise_eof() -> None:
        raise EOFError

    monkeypatch.setattr(builtins, "input", raise_eof)
    ticks = iter([10.0, 14.0])
    monkeypatch.setattr(warmup_runner.time, "monotonic", lambda: next(ticks))
    warmup_runner._wait_for_direct_warmup_completion(process)

    assert process.wait_called



def test_direct_warmup_rejects_immediate_browser_exit_without_stdin(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    process = _FakeDirectWarmupProcess(poll_result=None)

    def raise_eof() -> None:
        raise EOFError

    monkeypatch.setattr(builtins, "input", raise_eof)
    ticks = iter([10.0, 10.2])
    monkeypatch.setattr(warmup_runner.time, "monotonic", lambda: next(ticks))

    with pytest.raises(RuntimeError, match="exited before the operator could inspect"):
        warmup_runner._wait_for_direct_warmup_completion(process)

    assert process.wait_called

def test_direct_warmup_rejects_enter_before_browser_close(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    process = _FakeDirectWarmupProcess(poll_result=None)
    monkeypatch.setattr(builtins, "input", lambda: "")

    with pytest.raises(RuntimeError, match="browser is still running"):
        warmup_runner._wait_for_direct_warmup_completion(process)

    assert not process.wait_called


class _FakeExportEngine:
    payload: str = '{"cookies": [], "origins": []}'

    def __init__(self) -> None:
        self.user_data_dirs: list[Path] = []

    def export_storage_state(self, *, user_data_dir: Path, state_path: Path) -> None:
        self.user_data_dirs.append(user_data_dir)
        state_path.write_text(self.payload, encoding="utf-8")


def test_browser_user_data_export_writes_auth_state_without_packet(scratch_dir: Path) -> None:
    auth_root = scratch_dir / "_auth_state"
    user_data_root = scratch_dir / "_browser_user_data"
    user_data_dir = user_data_root / "tiktok-alt"
    user_data_dir.mkdir(parents=True)
    engine = _FakeExportEngine()

    exit_code, message = run_browser_user_data_export(
        user_data_label="tiktok-alt",
        state_label="tiktok-alt-session",
        session_mode=AuthenticatedSessionMode.CLIENT_PROVIDED,
        auth_state_root=auth_root,
        browser_user_data_root=user_data_root,
        engine=engine,
    )

    state_path = auth_root / "tiktok-alt-session.json"
    metadata_path = auth_root / "tiktok-alt-session.meta.json"
    assert exit_code == 0
    assert engine.user_data_dirs == [user_data_dir]
    assert "client_provided_session" in message
    assert "tiktok-alt-session" in message
    assert "tiktok-alt" in message
    assert str(auth_root) not in message
    assert str(user_data_root) not in message
    assert "about:blank" not in message
    assert "https://" not in message
    assert state_path.exists()
    assert metadata_path.exists()
    assert json.loads(metadata_path.read_text(encoding="utf-8")) == {
        "auth_state_file": "tiktok-alt-session.json",
        "session_mode": "client_provided_session",
    }
    assert not (scratch_dir / "manifest.json").exists()
    assert not (scratch_dir / "receipt.md").exists()



def test_browser_user_data_export_merges_user_data_provenance_into_auth_state(
    scratch_dir: Path,
) -> None:
    auth_root = scratch_dir / "_auth_state"
    user_data_root = scratch_dir / "_browser_user_data"
    user_data_dir = user_data_root / "tiktok-alt"
    user_data_dir.mkdir(parents=True)
    provenance = build_browser_user_data_source_access_provenance(
        user_data_label="tiktok-alt",
        browser_backend="cloakbrowser",
        proxy_category=None,
    )
    browser_user_data_provenance_path_for_label(
        "tiktok-alt",
        user_data_root=user_data_root,
    ).write_text(json.dumps(provenance), encoding="utf-8")

    run_browser_user_data_export(
        user_data_label="tiktok-alt",
        state_label="tiktok-alt-session",
        session_mode=AuthenticatedSessionMode.CLIENT_PROVIDED,
        auth_state_root=auth_root,
        browser_user_data_root=user_data_root,
        engine=_FakeExportEngine(),
    )

    state_path = auth_root / "tiktok-alt-session.json"
    metadata = json.loads((auth_root / "tiktok-alt-session.meta.json").read_text(encoding="utf-8"))
    source_access = metadata["source_access_provenance"]
    assert metadata["schema_version"] == 1
    assert source_access["source_access_posture"] == "client_provided_session"
    assert source_access["browser_backend"] == "cloakbrowser"
    assert source_access["harness_proxy_profile_posture"] == "no_proxy_profile_loaded"
    assert source_access["proxy_category"] == "none"
    assert source_access["warmup_user_data_label_sha256"] == provenance["browser_user_data_label_sha256"]
    assert source_access["state_content_sha256"] == hashlib.sha256(state_path.read_bytes()).hexdigest()


def test_browser_user_data_export_rejects_forbidden_user_data_provenance_and_discards_state(
    scratch_dir: Path,
) -> None:
    auth_root = scratch_dir / "_auth_state"
    user_data_root = scratch_dir / "_browser_user_data"
    user_data_dir = user_data_root / "tiktok-alt"
    user_data_dir.mkdir(parents=True)
    provenance = build_browser_user_data_source_access_provenance(
        user_data_label="tiktok-alt",
        browser_backend="cloakbrowser",
        proxy_category=None,
    )
    provenance["proxy_endpoint"] = "http://proxy.example:8080"
    browser_user_data_provenance_path_for_label(
        "tiktok-alt",
        user_data_root=user_data_root,
    ).write_text(json.dumps(provenance), encoding="utf-8")

    with pytest.raises(ValueError, match="forbidden field"):
        run_browser_user_data_export(
            user_data_label="tiktok-alt",
            state_label="tiktok-alt-session",
            session_mode=AuthenticatedSessionMode.CLIENT_PROVIDED,
            auth_state_root=auth_root,
            browser_user_data_root=user_data_root,
            engine=_FakeExportEngine(),
        )

    assert not (auth_root / "tiktok-alt-session.json").exists()
    assert not (auth_root / "tiktok-alt-session.meta.json").exists()


def test_browser_user_data_export_rejects_missing_user_data_before_state_write(
    scratch_dir: Path,
) -> None:
    auth_root = scratch_dir / "_auth_state"
    user_data_root = scratch_dir / "_browser_user_data"
    engine = _FakeExportEngine()

    with pytest.raises(ValueError, match="browser user-data directory does not exist"):
        run_browser_user_data_export(
            user_data_label="missing",
            state_label="missing-session",
            session_mode=AuthenticatedSessionMode.CLIENT_PROVIDED,
            auth_state_root=auth_root,
            browser_user_data_root=user_data_root,
            engine=engine,
        )

    assert engine.user_data_dirs == []
    assert not (auth_root / "missing-session.json").exists()
    assert not (auth_root / "missing-session.meta.json").exists()


def test_browser_user_data_export_discards_state_when_validation_fails(
    scratch_dir: Path,
) -> None:
    auth_root = scratch_dir / "_auth_state"
    user_data_root = scratch_dir / "_browser_user_data"
    user_data_dir = user_data_root / "tiktok-alt"
    user_data_dir.mkdir(parents=True)

    class _BadShapeExportEngine:
        def export_storage_state(self, *, user_data_dir: Path, state_path: Path) -> None:
            state_path.write_text('{"cookies": {}}', encoding="utf-8")

    with pytest.raises(ValueError, match="cookies/origins"):
        run_browser_user_data_export(
            user_data_label="tiktok-alt",
            state_label="tiktok-alt-session",
            session_mode=AuthenticatedSessionMode.CLIENT_PROVIDED,
            auth_state_root=auth_root,
            browser_user_data_root=user_data_root,
            engine=_BadShapeExportEngine(),
        )

    state_path = auth_root / "tiktok-alt-session.json"
    metadata_path = auth_root / "tiktok-alt-session.meta.json"
    assert not state_path.exists()
    assert not metadata_path.exists()


def test_cloakbrowser_user_data_export_retries_visible_after_headless_failure(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user_data_dir = scratch_dir / "user-data"
    user_data_dir.mkdir()
    state_path = scratch_dir / "state.json"
    attempts: list[tuple[Path, bool, bool]] = []

    class FakeContext:
        def storage_state(self, *, path: str) -> None:
            Path(path).write_text('{"cookies": [], "origins": []}', encoding="utf-8")

        def close(self) -> None:
            return

    class FakeCloakBrowser:
        def launch_persistent_context(
            self,
            user_data_dir_arg: Path,
            *,
            headless: bool,
            stealth_args: bool,
        ) -> FakeContext:
            attempts.append((user_data_dir_arg, headless, stealth_args))
            if headless:
                raise RuntimeError("raw launch diagnostics with local path")
            return FakeContext()

    monkeypatch.setitem(sys.modules, "cloakbrowser", FakeCloakBrowser())

    export_runner._CloakBrowserUserDataExportEngine().export_storage_state(
        user_data_dir=user_data_dir,
        state_path=state_path,
    )

    assert attempts == [(user_data_dir, True, True), (user_data_dir, False, True)]
    assert json.loads(state_path.read_text(encoding="utf-8")) == {"cookies": [], "origins": []}


def test_cloakbrowser_user_data_export_sanitizes_launch_failure(
    scratch_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    user_data_dir = scratch_dir / "user-data"
    user_data_dir.mkdir()
    state_path = scratch_dir / "state.json"
    attempts: list[bool] = []

    class FakeCloakBrowser:
        def launch_persistent_context(
            self,
            user_data_dir_arg: Path,
            *,
            headless: bool,
            stealth_args: bool,
        ) -> object:
            attempts.append(headless)
            raise RuntimeError(f"raw launch diagnostics for {user_data_dir_arg}")

    monkeypatch.setitem(sys.modules, "cloakbrowser", FakeCloakBrowser())

    with pytest.raises(RuntimeError) as exc_info:
        export_runner._CloakBrowserUserDataExportEngine().export_storage_state(
            user_data_dir=user_data_dir,
            state_path=state_path,
        )

    message = str(exc_info.value)
    assert attempts == [True, False]
    assert "raw launch diagnostics" not in message
    assert str(user_data_dir) not in message
    assert "Close any browser window using that user-data label" in message
    assert not state_path.exists()


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


def test_session_bootstrap_rejects_invalid_browser_backend(scratch_dir: Path) -> None:
    with pytest.raises(ValueError, match="browser_backend must be one of"):
        run_browser_session_bootstrap(
            login_url="https://example.com/login",
            state_label="free-example",
            session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
            timeout_seconds=5,
            auth_state_root=scratch_dir / "_auth_state",
            browser_backend="unknown",
            engine=_FakeBootstrapEngine(),
        )


def test_session_bootstrap_rejects_cloakbrowser_humanize_without_cloakbrowser(
    scratch_dir: Path,
) -> None:
    with pytest.raises(ValueError, match="cloakbrowser_humanize requires"):
        run_browser_session_bootstrap(
            login_url="https://example.com/login",
            state_label="free-example",
            session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
            timeout_seconds=5,
            auth_state_root=scratch_dir / "_auth_state",
            browser_backend="playwright",
            cloakbrowser_humanize=True,
            engine=_FakeBootstrapEngine(),
        )


def test_session_bootstrap_rejects_cloakbrowser_user_data_without_cloakbrowser(
    scratch_dir: Path,
) -> None:
    with pytest.raises(ValueError, match="cloakbrowser_user_data_label requires"):
        run_browser_session_bootstrap(
            login_url="https://example.com/login",
            state_label="free-example",
            session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
            timeout_seconds=5,
            auth_state_root=scratch_dir / "_auth_state",
            browser_user_data_root=scratch_dir / "_browser_user_data",
            browser_backend="playwright",
            cloakbrowser_user_data_label="google-login",
            engine=_FakeBootstrapEngine(),
        )


def test_session_bootstrap_checks_existing_state_before_creating_user_data_directory(
    scratch_dir: Path,
) -> None:
    auth_root = scratch_dir / "_auth_state"
    user_data_root = scratch_dir / "_browser_user_data"
    auth_root.mkdir(parents=True)
    state_path = auth_state_path_for_label("free-example", auth_state_root=auth_root)
    state_path.write_text('{"cookies": [], "origins": []}', encoding="utf-8")

    with pytest.raises(ValueError, match="auth-state file already exists"):
        run_browser_session_bootstrap(
            login_url="https://example.com/login",
            state_label="free-example",
            session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
            timeout_seconds=5,
            auth_state_root=auth_root,
            browser_user_data_root=user_data_root,
            browser_backend="cloakbrowser",
            cloakbrowser_user_data_label="google-login",
            engine=_FakeBootstrapEngine(),
        )

    assert not (user_data_root / "google-login").exists()


def test_session_bootstrap_creates_cloakbrowser_user_data_directory(
    scratch_dir: Path,
) -> None:
    auth_root = scratch_dir / "_auth_state"
    user_data_root = scratch_dir / "_browser_user_data"

    exit_code, _ = run_browser_session_bootstrap(
        login_url="https://example.com/login",
        state_label="free-example",
        session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
        timeout_seconds=5,
        auth_state_root=auth_root,
        browser_user_data_root=user_data_root,
        browser_backend="cloakbrowser",
        cloakbrowser_user_data_label="google-login",
        engine=_FakeBootstrapEngine(),
    )

    assert exit_code == 0
    assert (user_data_root / "google-login").is_dir()


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
