from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

import pytest

from runners import run_source_capture_proxy_profile_bootstrap as bootstrap_runner
from runners.run_source_capture_proxy_profile_bootstrap import run_proxy_profile_bootstrap
from source_capture.proxy_profiles import (
    ProxyCategory,
    ProxyProfile,
    load_proxy_profile,
    proxy_profile_metadata_path_for_label,
    proxy_profile_path_for_label,
    validate_proxy_profile_file,
    write_proxy_profile_metadata,
)


@pytest.fixture
def scratch_dir() -> Path:
    root = Path(__file__).resolve().parents[2] / "_test_runs"
    path = root / f"source_capture_proxy_profiles_{uuid.uuid4().hex}"
    path.mkdir(parents=True)
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


def _write_profile_file(
    profile_root: Path,
    label: str,
    *,
    server: str = "http://user:SUPER_SECRET_PROXY_VALUE@proxy.example:8080",
) -> Path:
    profile_root.mkdir(parents=True, exist_ok=True)
    path = proxy_profile_path_for_label(label, profile_root=profile_root)
    path.write_text(json.dumps({"server": server}), encoding="utf-8")
    return path


def test_proxy_categories_are_fixed_vocabulary() -> None:
    assert [item.value for item in ProxyCategory] == [
        "residential_static",
        "residential_rotating",
        "mobile_static",
        "mobile_rotating",
        "datacenter_static",
        "datacenter_rotating",
    ]


def test_proxy_profile_label_rejects_path_traversal(scratch_dir: Path) -> None:
    with pytest.raises(ValueError, match="proxy-profile label"):
        proxy_profile_path_for_label("../outside", profile_root=scratch_dir)
    with pytest.raises(ValueError, match="proxy-profile label"):
        proxy_profile_path_for_label("nested/profile", profile_root=scratch_dir)


def test_validate_proxy_profile_file_rejects_missing_and_bad_shape(scratch_dir: Path) -> None:
    with pytest.raises(ValueError, match="does not exist"):
        validate_proxy_profile_file("missing", profile_root=scratch_dir)

    path = proxy_profile_path_for_label("bad", profile_root=scratch_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"not_server": "http://proxy.example:8080"}), encoding="utf-8")
    with pytest.raises(ValueError, match="server"):
        validate_proxy_profile_file("bad", profile_root=scratch_dir)


def test_validate_proxy_profile_rejects_unexpected_keys(scratch_dir: Path) -> None:
    profile_root = scratch_dir / "_proxy_profiles"
    profile_root.mkdir(parents=True, exist_ok=True)
    path = proxy_profile_path_for_label("reddit-res", profile_root=profile_root)
    path.write_text(
        json.dumps(
            {
                "server": "http://user:SUPER_SECRET_PROXY_VALUE@proxy.example:8080",
                "exit_ip": "203.0.113.10",
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="unexpected key"):
        validate_proxy_profile_file("reddit-res", profile_root=profile_root)


def test_write_metadata_then_load_returns_secret_endpoint(scratch_dir: Path) -> None:
    profile_root = scratch_dir / "_proxy_profiles"
    _write_profile_file(profile_root, "reddit-res")

    metadata_path = write_proxy_profile_metadata(
        "reddit-res",
        proxy_category=ProxyCategory.RESIDENTIAL_STATIC,
        geoip_enabled=True,
        profile_root=profile_root,
    )
    assert json.loads(metadata_path.read_text(encoding="utf-8")) == {
        "profile_file": "reddit-res.json",
        "proxy_category": "residential_static",
        "geoip_enabled": True,
    }

    profile = load_proxy_profile(
        "reddit-res",
        proxy_category=ProxyCategory.RESIDENTIAL_STATIC,
        profile_root=profile_root,
    )
    assert profile.proxy_endpoint == "http://user:SUPER_SECRET_PROXY_VALUE@proxy.example:8080"
    assert profile.proxy_category is ProxyCategory.RESIDENTIAL_STATIC
    assert profile.geoip_enabled is True


def test_write_metadata_then_load_round_trips_declared_geo(scratch_dir: Path) -> None:
    profile_root = scratch_dir / "_proxy_profiles"
    _write_profile_file(profile_root, "reddit-res")

    metadata_path = write_proxy_profile_metadata(
        "reddit-res",
        proxy_category=ProxyCategory.RESIDENTIAL_STATIC,
        geoip_enabled=True,
        timezone="America/New_York",
        locale="en-US",
        profile_root=profile_root,
    )
    assert json.loads(metadata_path.read_text(encoding="utf-8")) == {
        "profile_file": "reddit-res.json",
        "proxy_category": "residential_static",
        "geoip_enabled": True,
        "timezone": "America/New_York",
        "locale": "en-US",
    }

    profile = load_proxy_profile(
        "reddit-res",
        proxy_category=ProxyCategory.RESIDENTIAL_STATIC,
        profile_root=profile_root,
    )
    assert profile.timezone == "America/New_York"
    assert profile.locale == "en-US"


def test_load_proxy_profile_without_declared_geo_defaults_to_none(scratch_dir: Path) -> None:
    profile_root = scratch_dir / "_proxy_profiles"
    _write_profile_file(profile_root, "reddit-res")
    write_proxy_profile_metadata(
        "reddit-res",
        proxy_category=ProxyCategory.RESIDENTIAL_STATIC,
        geoip_enabled=True,
        profile_root=profile_root,
    )

    profile = load_proxy_profile(
        "reddit-res",
        proxy_category=ProxyCategory.RESIDENTIAL_STATIC,
        profile_root=profile_root,
    )
    assert profile.timezone is None
    assert profile.locale is None


def test_load_proxy_profile_rejects_blank_declared_geo(scratch_dir: Path) -> None:
    profile_root = scratch_dir / "_proxy_profiles"
    _write_profile_file(profile_root, "reddit-res")
    metadata_path = proxy_profile_metadata_path_for_label("reddit-res", profile_root=profile_root)
    metadata_path.write_text(
        json.dumps(
            {
                "profile_file": "reddit-res.json",
                "proxy_category": "residential_static",
                "geoip_enabled": True,
                "timezone": "   ",
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="timezone"):
        load_proxy_profile(
            "reddit-res",
            proxy_category=ProxyCategory.RESIDENTIAL_STATIC,
            profile_root=profile_root,
        )


def test_bootstrap_writes_declared_geo_into_sidecar(scratch_dir: Path) -> None:
    profile_root = scratch_dir / "_proxy_profiles"
    _write_profile_file(profile_root, "reddit-res")

    exit_code, message = run_proxy_profile_bootstrap(
        profile_label="reddit-res",
        proxy_category=ProxyCategory.RESIDENTIAL_STATIC,
        geoip_enabled=True,
        timezone="America/New_York",
        locale="en-US",
        profile_root=profile_root,
    )

    assert exit_code == 0
    assert "America/New_York" in message
    assert "SUPER_SECRET_PROXY_VALUE" not in message
    sidecar = json.loads((profile_root / "reddit-res.meta.json").read_text(encoding="utf-8"))
    assert sidecar["timezone"] == "America/New_York"
    assert sidecar["locale"] == "en-US"


def test_load_rejects_category_mismatch(scratch_dir: Path) -> None:
    profile_root = scratch_dir / "_proxy_profiles"
    _write_profile_file(profile_root, "reddit-res")
    metadata_path = proxy_profile_metadata_path_for_label("reddit-res", profile_root=profile_root)
    metadata_path.write_text(
        json.dumps(
            {
                "profile_file": "reddit-res.json",
                "proxy_category": "mobile_static",
                "geoip_enabled": True,
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="category mismatch"):
        load_proxy_profile(
            "reddit-res",
            proxy_category=ProxyCategory.RESIDENTIAL_STATIC,
            profile_root=profile_root,
        )


def test_proxy_profile_repr_redacts_endpoint() -> None:
    profile = ProxyProfile(
        proxy_endpoint="http://user:SUPER_SECRET_PROXY_VALUE@proxy.example:8080",
        proxy_category=ProxyCategory.RESIDENTIAL_STATIC,
        geoip_enabled=True,
    )
    for rendered in (repr(profile), str(profile), f"{profile}"):
        assert "SUPER_SECRET_PROXY_VALUE" not in rendered
        assert "proxy.example" not in rendered
        assert "redacted" in rendered


def test_bootstrap_writes_sidecar_for_placed_file_without_packet(scratch_dir: Path) -> None:
    profile_root = scratch_dir / "_proxy_profiles"
    _write_profile_file(profile_root, "reddit-res")

    exit_code, message = run_proxy_profile_bootstrap(
        profile_label="reddit-res",
        proxy_category=ProxyCategory.RESIDENTIAL_STATIC,
        geoip_enabled=True,
        profile_root=profile_root,
    )

    assert exit_code == 0
    assert "residential_static" in message
    assert "SUPER_SECRET_PROXY_VALUE" not in message
    sidecar = profile_root / "reddit-res.meta.json"
    assert sidecar.exists()
    assert json.loads(sidecar.read_text(encoding="utf-8")) == {
        "profile_file": "reddit-res.json",
        "proxy_category": "residential_static",
        "geoip_enabled": True,
    }
    assert not (scratch_dir / "manifest.json").exists()


def test_bootstrap_cli_exposes_no_secret_flags() -> None:
    forbidden_destinations = {
        "password",
        "username",
        "token",
        "cookie",
        "client_id",
        "client_secret",
        "secret",
        "server",
        "proxy_endpoint",
    }
    forbidden_options = {
        "--password",
        "--username",
        "--token",
        "--cookie",
        "--client-id",
        "--client-secret",
        "--secret",
        "--server",
        "--proxy",
    }
    parser = bootstrap_runner._build_parser()
    destinations = {action.dest for action in parser._actions}
    options = {option for action in parser._actions for option in action.option_strings}
    assert destinations.isdisjoint(forbidden_destinations)
    assert options.isdisjoint(forbidden_options)
