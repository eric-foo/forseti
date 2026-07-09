from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

import pytest

from runners import run_source_capture_reddit_credential_bootstrap as bootstrap_runner
from runners.run_source_capture_reddit_credential_bootstrap import run_reddit_credential_bootstrap
from source_capture import RedditCredentialMode
from source_capture.reddit_credentials import (
    RedditCredentials,
    load_reddit_credentials,
    reddit_credential_metadata_path_for_label,
    reddit_credential_path_for_label,
    validate_reddit_credential_file,
    write_reddit_credential_metadata,
)


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"source_capture_reddit_credentials_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _write_credential_file(
    cred_root: Path,
    label: str,
    *,
    client_id: str = "public-app-id",
    client_secret: str = "SUPER_SECRET_VALUE",
) -> Path:
    cred_root.mkdir(parents=True, exist_ok=True)
    path = reddit_credential_path_for_label(label, credential_root=cred_root)
    path.write_text(
        json.dumps({"client_id": client_id, "client_secret": client_secret}),
        encoding="utf-8",
    )
    return path


def test_reddit_credential_modes_are_fixed_vocabulary() -> None:
    assert [item.value for item in RedditCredentialMode] == ["owner_registered_script_app"]


def test_reddit_credential_label_rejects_path_traversal(scratch_dir: Path) -> None:
    with pytest.raises(ValueError, match="reddit-credential label"):
        reddit_credential_path_for_label("../outside", credential_root=scratch_dir)
    with pytest.raises(ValueError, match="reddit-credential label"):
        reddit_credential_path_for_label("nested/cred", credential_root=scratch_dir)


def test_validate_reddit_credential_file_rejects_missing_and_bad_shape(scratch_dir: Path) -> None:
    with pytest.raises(ValueError, match="does not exist"):
        validate_reddit_credential_file("missing", credential_root=scratch_dir)

    path = reddit_credential_path_for_label("bad", credential_root=scratch_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"client_id": "only-id"}), encoding="utf-8")
    with pytest.raises(ValueError, match="client_secret"):
        validate_reddit_credential_file("bad", credential_root=scratch_dir)


def test_validate_rejects_unexpected_keys(scratch_dir: Path) -> None:
    cred_root = scratch_dir / "_reddit_credentials"
    cred_root.mkdir(parents=True, exist_ok=True)
    path = reddit_credential_path_for_label("script-app", credential_root=cred_root)
    path.write_text(
        json.dumps({"client_id": "id", "client_secret": "sec", "refresh_token": "LEAK_VALUE"}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="unexpected key"):
        validate_reddit_credential_file("script-app", credential_root=cred_root)


def test_write_metadata_then_load_returns_secrets(scratch_dir: Path) -> None:
    cred_root = scratch_dir / "_reddit_credentials"
    _write_credential_file(cred_root, "script-app", client_id="public-app-id", client_secret="SUPER_SECRET_VALUE")

    metadata_path = write_reddit_credential_metadata(
        "script-app",
        credential_mode=RedditCredentialMode.OWNER_REGISTERED_SCRIPT_APP,
        credential_root=cred_root,
    )
    assert json.loads(metadata_path.read_text(encoding="utf-8")) == {
        "credential_file": "script-app.json",
        "credential_mode": "owner_registered_script_app",
    }

    creds = load_reddit_credentials(
        "script-app",
        credential_mode=RedditCredentialMode.OWNER_REGISTERED_SCRIPT_APP,
        credential_root=cred_root,
    )
    assert creds.client_id == "public-app-id"
    assert creds.client_secret == "SUPER_SECRET_VALUE"
    assert creds.credential_mode is RedditCredentialMode.OWNER_REGISTERED_SCRIPT_APP


def test_load_rejects_mode_mismatch(scratch_dir: Path) -> None:
    cred_root = scratch_dir / "_reddit_credentials"
    _write_credential_file(cred_root, "script-app")
    # Simulate a sidecar registered under a different (e.g. future/stale) mode.
    metadata_path = reddit_credential_metadata_path_for_label("script-app", credential_root=cred_root)
    metadata_path.write_text(
        json.dumps({"credential_file": "script-app.json", "credential_mode": "some_other_mode"}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="credential mode mismatch"):
        load_reddit_credentials(
            "script-app",
            credential_mode=RedditCredentialMode.OWNER_REGISTERED_SCRIPT_APP,
            credential_root=cred_root,
        )


def test_load_rejects_file_binding_mismatch(scratch_dir: Path) -> None:
    cred_root = scratch_dir / "_reddit_credentials"
    _write_credential_file(cred_root, "script-app")
    # Sidecar declares the correct mode but is bound to a different credential file.
    metadata_path = reddit_credential_metadata_path_for_label("script-app", credential_root=cred_root)
    metadata_path.write_text(
        json.dumps(
            {"credential_file": "other-app.json", "credential_mode": "owner_registered_script_app"}
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="file binding mismatch"):
        load_reddit_credentials(
            "script-app",
            credential_mode=RedditCredentialMode.OWNER_REGISTERED_SCRIPT_APP,
            credential_root=cred_root,
        )


def test_load_rejects_missing_sidecar(scratch_dir: Path) -> None:
    cred_root = scratch_dir / "_reddit_credentials"
    _write_credential_file(cred_root, "script-app")
    with pytest.raises(ValueError, match="metadata sidecar does not exist"):
        load_reddit_credentials(
            "script-app",
            credential_mode=RedditCredentialMode.OWNER_REGISTERED_SCRIPT_APP,
            credential_root=cred_root,
        )


def test_reddit_credentials_repr_redacts_both_values() -> None:
    creds = RedditCredentials(
        client_id="PUBLIC_APP_ID_VALUE",
        client_secret="SUPER_SECRET_VALUE",
        credential_mode=RedditCredentialMode.OWNER_REGISTERED_SCRIPT_APP,
    )
    for rendered in (repr(creds), str(creds), f"{creds}"):
        assert "SUPER_SECRET_VALUE" not in rendered
        assert "PUBLIC_APP_ID_VALUE" not in rendered
        assert "redacted" in rendered


def test_bootstrap_writes_sidecar_for_placed_file_without_packet(scratch_dir: Path) -> None:
    cred_root = scratch_dir / "_reddit_credentials"
    _write_credential_file(cred_root, "script-app")

    exit_code, message = run_reddit_credential_bootstrap(
        credential_label="script-app",
        credential_mode=RedditCredentialMode.OWNER_REGISTERED_SCRIPT_APP,
        credential_root=cred_root,
    )

    assert exit_code == 0
    assert "owner_registered_script_app" in message
    assert "SUPER_SECRET_VALUE" not in message
    sidecar = cred_root / "script-app.meta.json"
    assert sidecar.exists()
    assert json.loads(sidecar.read_text(encoding="utf-8")) == {
        "credential_file": "script-app.json",
        "credential_mode": "owner_registered_script_app",
    }
    assert not (scratch_dir / "manifest.json").exists()


def test_bootstrap_rejects_missing_credential_file(scratch_dir: Path) -> None:
    cred_root = scratch_dir / "_reddit_credentials"
    cred_root.mkdir(parents=True, exist_ok=True)
    with pytest.raises(ValueError, match="does not exist"):
        run_reddit_credential_bootstrap(
            credential_label="script-app",
            credential_mode=RedditCredentialMode.OWNER_REGISTERED_SCRIPT_APP,
            credential_root=cred_root,
        )


def test_bootstrap_cli_exposes_no_secret_flags() -> None:
    forbidden_destinations = {"password", "username", "token", "cookie", "profile", "client_id", "client_secret", "secret"}
    forbidden_options = {
        "--password",
        "--username",
        "--token",
        "--cookie",
        "--client-id",
        "--client-secret",
        "--secret",
        "--refresh-token",
    }
    parser = bootstrap_runner._build_parser()
    destinations = {action.dest for action in parser._actions}
    options = {option for action in parser._actions for option in action.option_strings}
    assert destinations.isdisjoint(forbidden_destinations)
    assert options.isdisjoint(forbidden_options)
