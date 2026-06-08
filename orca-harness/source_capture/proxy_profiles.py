"""Local, ignored proxy profile store for CloakBrowser source capture.

Proxy endpoints and credentials are secrets. This module keeps them behind a
label-indirected local store and returns them only as in-memory values for the
CloakBrowser launch call. Packets may record the non-secret method category and
geoip setting, never the endpoint, credentials, exit IP, store root, or file path.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from source_capture.local_secret_store import (
    DEFAULT_MAX_SECRET_STORE_BYTES,
    ensure_store_directory,
    read_sidecar,
    read_store_payload,
    sidecar_path_for,
    store_path_for_label,
    write_sidecar,
)


PROXY_PROFILE_DIRNAME = "_proxy_profiles"
PROXY_PROFILE_METADATA_SUFFIX = ".meta.json"
MAX_PROXY_PROFILE_BYTES = DEFAULT_MAX_SECRET_STORE_BYTES
_PROXY_PROFILE_KIND = "proxy-profile"
_REQUIRED_PROFILE_KEYS = ("server",)


class ProxyCategory(StrEnum):
    RESIDENTIAL_STATIC = "residential_static"
    RESIDENTIAL_ROTATING = "residential_rotating"
    MOBILE_STATIC = "mobile_static"
    MOBILE_ROTATING = "mobile_rotating"
    DATACENTER_STATIC = "datacenter_static"
    DATACENTER_ROTATING = "datacenter_rotating"


@dataclass(frozen=True, repr=False)
class ProxyProfile:
    """In-memory proxy profile. Holds the secret endpoint; never serialize."""

    proxy_endpoint: str
    proxy_category: ProxyCategory
    geoip_enabled: bool

    def __repr__(self) -> str:
        return (
            "ProxyProfile(proxy_endpoint='<redacted>', "
            f"proxy_category={self.proxy_category.value!r}, geoip_enabled={self.geoip_enabled!r})"
        )


def default_proxy_profile_root() -> Path:
    return Path(__file__).resolve().parents[1] / PROXY_PROFILE_DIRNAME


def proxy_profile_path_for_label(label: str, *, profile_root: Path | None = None) -> Path:
    root = profile_root or default_proxy_profile_root()
    return store_path_for_label(label, root=root, kind=_PROXY_PROFILE_KIND)


def proxy_profile_metadata_path_for_label(
    label: str, *, profile_root: Path | None = None
) -> Path:
    root = profile_root or default_proxy_profile_root()
    profile_path = proxy_profile_path_for_label(label, profile_root=root)
    return sidecar_path_for(
        profile_path,
        root=root,
        sidecar_suffix=PROXY_PROFILE_METADATA_SUFFIX,
        kind=_PROXY_PROFILE_KIND,
    )


def ensure_proxy_profile_directory(*, profile_root: Path | None = None) -> Path:
    root = profile_root or default_proxy_profile_root()
    return ensure_store_directory(root)


def validate_proxy_profile_file(label: str, *, profile_root: Path | None = None) -> Path:
    root = profile_root or default_proxy_profile_root()
    path = proxy_profile_path_for_label(label, profile_root=root)
    payload = read_store_payload(
        path, max_bytes=MAX_PROXY_PROFILE_BYTES, kind=_PROXY_PROFILE_KIND, label=label
    )
    _validate_profile_shape(payload, label=label)
    return path


def write_proxy_profile_metadata(
    label: str,
    *,
    proxy_category: ProxyCategory,
    geoip_enabled: bool,
    profile_root: Path | None = None,
) -> Path:
    root = profile_root or default_proxy_profile_root()
    profile_path = validate_proxy_profile_file(label, profile_root=root)
    metadata_path = proxy_profile_metadata_path_for_label(label, profile_root=root)
    write_sidecar(
        metadata_path,
        payload={
            "profile_file": profile_path.name,
            "proxy_category": proxy_category.value,
            "geoip_enabled": geoip_enabled,
        },
        kind=_PROXY_PROFILE_KIND,
        label=label,
    )
    return metadata_path


def load_proxy_profile(
    label: str,
    *,
    proxy_category: ProxyCategory,
    profile_root: Path | None = None,
) -> ProxyProfile:
    root = profile_root or default_proxy_profile_root()
    profile_path = proxy_profile_path_for_label(label, profile_root=root)
    payload = read_store_payload(
        profile_path, max_bytes=MAX_PROXY_PROFILE_BYTES, kind=_PROXY_PROFILE_KIND, label=label
    )
    _validate_profile_shape(payload, label=label)

    metadata_path = proxy_profile_metadata_path_for_label(label, profile_root=root)
    if not metadata_path.exists():
        raise ValueError(
            "proxy-profile metadata sidecar does not exist for label: "
            f"{label}; register the profile with an explicit proxy category"
        )
    sidecar = read_sidecar(metadata_path, kind=_PROXY_PROFILE_KIND, label=label)
    if sidecar.get("profile_file") != profile_path.name:
        raise ValueError(f"proxy-profile metadata file binding mismatch for label: {label}")
    registered_category = sidecar.get("proxy_category")
    if registered_category != proxy_category.value:
        raise ValueError(
            "proxy-profile category mismatch for label: "
            f"{label}; registered as {registered_category!r} but capture declared {proxy_category.value!r}"
        )
    geoip_enabled = sidecar.get("geoip_enabled")
    if not isinstance(geoip_enabled, bool):
        raise ValueError(f"proxy-profile metadata geoip_enabled must be boolean for label: {label}")

    return ProxyProfile(
        proxy_endpoint=payload["server"],
        proxy_category=proxy_category,
        geoip_enabled=geoip_enabled,
    )


def _validate_profile_shape(payload: dict, *, label: str) -> None:
    for key in _REQUIRED_PROFILE_KEYS:
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"proxy-profile file must contain a non-empty string {key!r} for label: {label}"
            )
    unexpected = sorted(set(payload) - set(_REQUIRED_PROFILE_KEYS))
    if unexpected:
        raise ValueError(
            f"proxy-profile file has unexpected key(s) {unexpected} for label: {label}; "
            "the supported CloakBrowser proxy profile accepts exactly server"
        )


__all__ = [
    "ProxyCategory",
    "ProxyProfile",
    "default_proxy_profile_root",
    "ensure_proxy_profile_directory",
    "load_proxy_profile",
    "proxy_profile_metadata_path_for_label",
    "proxy_profile_path_for_label",
    "validate_proxy_profile_file",
    "write_proxy_profile_metadata",
]
