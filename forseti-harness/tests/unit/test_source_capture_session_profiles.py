from __future__ import annotations

import hashlib
import json
from pathlib import Path

from runners import check_source_capture_session_profile as preflight_runner
from runners import run_source_capture_tiktok_live_batch_probe as live_runner
from source_capture.auth_state import (
    AuthenticatedSessionMode,
    auth_state_path_for_label,
    write_auth_state_metadata,
)
from source_capture.browser_user_data import default_browser_user_data_root
from source_capture.session_profiles import (
    SESSION_PROFILE_CONFIG_SCHEMA_VERSION,
    resolve_session_profile,
    default_session_profile_auth_state_root,
    sanitized_session_profile_preflight,
    validate_session_profile_auth_state,
)


ALIAS = "chowdakr_sg_tiktok"
STATE_LABEL = "test-chowdakr-state"


def test_default_auth_state_root_is_stable_across_worktrees(
    tmp_path: Path,
    monkeypatch,
) -> None:
    local_app_data = tmp_path / "local"
    monkeypatch.delenv("FORSETI_AUTH_STATE_ROOT", raising=False)
    monkeypatch.setenv("LOCALAPPDATA", str(local_app_data))

    assert default_session_profile_auth_state_root() == local_app_data / "Forseti" / "auth_state"


def test_auth_state_root_environment_override_wins(
    tmp_path: Path,
    monkeypatch,
) -> None:
    explicit = tmp_path / "explicit-auth"
    monkeypatch.setenv("FORSETI_AUTH_STATE_ROOT", str(explicit))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "local"))

    assert default_session_profile_auth_state_root() == explicit


def test_default_browser_user_data_root_is_stable_across_worktrees(
    tmp_path: Path,
    monkeypatch,
) -> None:
    local_app_data = tmp_path / "local"
    monkeypatch.delenv("FORSETI_BROWSER_USER_DATA_ROOT", raising=False)
    monkeypatch.setenv("LOCALAPPDATA", str(local_app_data))

    assert default_browser_user_data_root() == (
        local_app_data / "Forseti" / "_browser_user_data"
    )


def test_browser_user_data_root_environment_override_wins(
    tmp_path: Path,
    monkeypatch,
) -> None:
    explicit = tmp_path / "explicit-browser-profile"
    monkeypatch.setenv("FORSETI_BROWSER_USER_DATA_ROOT", str(explicit))

    assert default_browser_user_data_root() == explicit


def test_profile_resolves_and_preflights_without_secret_path_or_state_label(
    tmp_path: Path,
) -> None:
    auth_root = _write_auth_state(tmp_path)
    config_path = _write_profile_config(tmp_path)

    profile = resolve_session_profile(ALIAS, config_path=config_path)
    validate_session_profile_auth_state(profile, auth_state_root=auth_root)
    receipt = sanitized_session_profile_preflight(profile)
    serialized = json.dumps(receipt, sort_keys=True)

    assert receipt["status"] == "available"
    assert receipt["session_profile"] == ALIAS
    assert receipt["persistent_browser_profile_configured"] is True
    assert receipt["challenge_policy"] == "owner_handoff_before_action"
    assert receipt["auth_state_validated"] is True
    assert STATE_LABEL not in serialized
    assert str(auth_root) not in serialized


def test_profile_preflight_runner_fails_closed_before_browser_launch(
    tmp_path: Path,
    capsys,
) -> None:
    code = preflight_runner.main(
        [
            "--session-profile",
            ALIAS,
            "--session-profile-config",
            str(tmp_path / "missing.json"),
            "--auth-state-root",
            str(tmp_path / "auth"),
        ]
    )

    assert code == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["blocker"] == "BLOCKED_SESSION_PROFILE_UNAVAILABLE"
    assert payload["secret_values_exposed"] is False
    assert "auth_state_root" not in payload
    assert str(tmp_path) not in json.dumps(payload)


def test_live_runner_binds_profile_without_manual_session_flags(
    tmp_path: Path,
    monkeypatch,
) -> None:
    auth_root = _write_auth_state(tmp_path)
    config_path = _write_profile_config(tmp_path)
    captured_kwargs: dict[str, object] = {}

    class _StopAfterBinding(RuntimeError):
        pass

    def fake_write(**kwargs: object) -> None:
        captured_kwargs.update(kwargs)
        raise _StopAfterBinding

    monkeypatch.setattr(
        live_runner,
        "write_tiktok_live_batch_probe_outputs",
        fake_write,
    )

    try:
        live_runner.main(
            [
                "--creator-handle",
                "creator",
                "--creator-profile-url",
                "https://www.tiktok.com/@creator",
                "--video-url",
                "https://www.tiktok.com/@creator/video/7390000000000000001",
                "--session-profile",
                ALIAS,
                "--session-profile-config",
                str(config_path),
                "--auth-state-root",
                str(auth_root),
                "--output-dir",
                str(tmp_path / "out"),
            ]
        )
    except _StopAfterBinding:
        pass
    else:
        raise AssertionError("runner did not reach the bound capture call")

    assert captured_kwargs["state_label"] == STATE_LABEL
    assert captured_kwargs["session_mode"] == AuthenticatedSessionMode.FREE_ACCOUNT_CREATED
    assert captured_kwargs["browser_backend"] == "cloakbrowser"
    assert captured_kwargs["human_challenge_handoff"] is True
    assert captured_kwargs["allow_challenge_close_followthrough"] is False
    assert captured_kwargs["logged_out"] is False


def test_profile_auth_failure_does_not_expose_state_label_or_path(
    tmp_path: Path,
    capsys,
) -> None:
    config_path = _write_profile_config(tmp_path)

    code = preflight_runner.main(
        [
            "--session-profile",
            ALIAS,
            "--session-profile-config",
            str(config_path),
            "--auth-state-root",
            str(tmp_path / "missing-auth"),
        ]
    )

    assert code == 2
    payload = json.loads(capsys.readouterr().out)
    serialized = json.dumps(payload, sort_keys=True)
    assert payload["detail"] == "session-profile auth state blocked: auth_state_missing"
    assert STATE_LABEL not in serialized
    assert str(tmp_path) not in serialized



def _write_profile_config(tmp_path: Path) -> Path:
    path = tmp_path / "profiles.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": SESSION_PROFILE_CONFIG_SCHEMA_VERSION,
                "profiles": {
                    ALIAS: {
                        "platform": "tiktok",
                        "state_label": STATE_LABEL,
                        "browser_user_data_label": ALIAS,
                        "session_mode": "free_account_created_session",
                        "required_harness_proxy_profile_posture": (
                            "proxy_profile_loaded"
                        ),
                        "browser_backend": "cloakbrowser",
                        "challenge_policy": "owner_handoff_before_action",
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    return path


def _write_auth_state(tmp_path: Path) -> Path:
    auth_root = tmp_path / "auth"
    path = auth_state_path_for_label(STATE_LABEL, auth_state_root=auth_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"cookies": [], "origins": []}), encoding="utf-8")
    write_auth_state_metadata(
        STATE_LABEL,
        session_mode=AuthenticatedSessionMode.FREE_ACCOUNT_CREATED,
        auth_state_root=auth_root,
        source_access_provenance={
            "source_access_posture": "free_account_created_session",
            "browser_backend": "cloakbrowser",
            "harness_proxy_profile_posture": "proxy_profile_loaded",
            "proxy_category": "residential_static",
            "warmup_user_data_label_sha256": "a" * 64,
            "state_content_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "no_secret_scan": "passed",
        },
    )
    return auth_root
