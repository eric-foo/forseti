from __future__ import annotations

import hashlib
import re
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping

from source_capture.proxy_profiles import ProxyCategory


SOURCE_ACCESS_PROVENANCE_SCHEMA_VERSION = 1
SOURCE_ACCESS_PROVENANCE_KEY = "source_access_provenance"
BROWSER_USER_DATA_LABEL_SHA256_KEY = "browser_user_data_label_sha256"
WARMUP_USER_DATA_LABEL_SHA256_KEY = "warmup_user_data_label_sha256"
STATE_CONTENT_SHA256_KEY = "state_content_sha256"

SOURCE_ACCESS_POSTURE_PUBLIC_LOGGED_OUT = "public_logged_out"
SOURCE_ACCESS_POSTURES = {
    SOURCE_ACCESS_POSTURE_PUBLIC_LOGGED_OUT,
    "free_account_created_session",
    "paid_entitled_session",
    "client_provided_session",
    "consenting_coworker_session",
}

BROWSER_BACKENDS = {"cloakbrowser", "playwright"}
PROXY_CATEGORY_NONE = "none"
NO_SECRET_SCAN_PASSED = "passed"

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_HOST_PORT_RE = re.compile(r"\b[A-Za-z0-9.-]+\.[A-Za-z]{2,}:\d{2,5}\b")
_URL_SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*://")
_WINDOWS_ABSOLUTE_PATH_RE = re.compile(r"^[A-Za-z]:[\\/]")

_FORBIDDEN_KEY_FRAGMENTS = (
    "cookie",
    "credential",
    "device_id",
    "exit_ip",
    "host_port",
    "ms_token",
    "mstoken",
    "password",
    "profile_path",
    "proxy_endpoint",
    "proxy_host",
    "proxy_password",
    "proxy_port",
    "proxy_server",
    "proxy_username",
    "signature",
    "storage_state",
    "token",
    "user_data_dir",
    "user_data_path",
)


class HarnessProxyProfilePosture(StrEnum):
    NO_PROXY_PROFILE_LOADED = "no_proxy_profile_loaded"
    PROXY_PROFILE_LOADED = "proxy_profile_loaded"
    UNKNOWN = "unknown"


def sha256_label(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_browser_user_data_source_access_provenance(
    *,
    user_data_label: str,
    browser_backend: str,
    proxy_category: str | None,
) -> dict[str, object]:
    normalized_backend = _validate_browser_backend(browser_backend)
    if proxy_category is None:
        harness_proxy_profile_posture = HarnessProxyProfilePosture.NO_PROXY_PROFILE_LOADED.value
        normalized_proxy_category = PROXY_CATEGORY_NONE
    else:
        harness_proxy_profile_posture = HarnessProxyProfilePosture.PROXY_PROFILE_LOADED.value
        normalized_proxy_category = _validate_proxy_category(proxy_category)
    payload: dict[str, object] = {
        "schema_version": SOURCE_ACCESS_PROVENANCE_SCHEMA_VERSION,
        BROWSER_USER_DATA_LABEL_SHA256_KEY: sha256_label(user_data_label),
        "browser_backend": normalized_backend,
        "harness_proxy_profile_posture": harness_proxy_profile_posture,
        "proxy_category": normalized_proxy_category,
        "no_secret_scan": NO_SECRET_SCAN_PASSED,
    }
    assert_no_forbidden_source_access_material(payload)
    return payload


def build_auth_state_source_access_provenance(
    *,
    user_data_label: str,
    session_mode_value: str,
    state_path: Path,
    browser_user_data_provenance: Mapping[str, Any],
) -> dict[str, object]:
    warmup = validate_browser_user_data_source_access_provenance(
        browser_user_data_provenance,
        user_data_label=user_data_label,
    )
    source_access_posture = _validate_source_access_posture(session_mode_value)
    payload: dict[str, object] = {
        "source_access_posture": source_access_posture,
        "browser_backend": warmup["browser_backend"],
        "harness_proxy_profile_posture": warmup["harness_proxy_profile_posture"],
        "proxy_category": warmup["proxy_category"],
        WARMUP_USER_DATA_LABEL_SHA256_KEY: warmup[BROWSER_USER_DATA_LABEL_SHA256_KEY],
        STATE_CONTENT_SHA256_KEY: sha256_file(state_path),
        "no_secret_scan": NO_SECRET_SCAN_PASSED,
    }
    assert_no_forbidden_source_access_material(payload)
    return payload


def validate_browser_user_data_source_access_provenance(
    payload: Mapping[str, Any],
    *,
    user_data_label: str,
) -> dict[str, object]:
    _assert_mapping(payload, "browser user-data source-access provenance")
    assert_no_forbidden_source_access_material(payload)
    _validate_schema_version(payload)
    label_hash = _validate_sha256(
        payload.get(BROWSER_USER_DATA_LABEL_SHA256_KEY),
        field=BROWSER_USER_DATA_LABEL_SHA256_KEY,
    )
    expected_hash = sha256_label(user_data_label)
    if label_hash != expected_hash:
        raise ValueError("browser user-data provenance label binding mismatch")
    result: dict[str, object] = {
        "schema_version": SOURCE_ACCESS_PROVENANCE_SCHEMA_VERSION,
        BROWSER_USER_DATA_LABEL_SHA256_KEY: label_hash,
        "browser_backend": _validate_browser_backend(payload.get("browser_backend")),
        "harness_proxy_profile_posture": _validate_harness_proxy_profile_posture(
            payload.get("harness_proxy_profile_posture")
        ),
        "proxy_category": _validate_proxy_category(payload.get("proxy_category")),
        "no_secret_scan": _validate_no_secret_scan(payload.get("no_secret_scan")),
    }
    _validate_proxy_category_matches_posture(result)
    assert_no_forbidden_source_access_material(result)
    return result


def validate_auth_state_source_access_provenance(
    payload: Mapping[str, Any],
    *,
    state_path: Path,
    expected_source_access_posture: str,
    required_harness_proxy_profile_posture: str | HarnessProxyProfilePosture | None = None,
) -> dict[str, object]:
    _assert_mapping(payload, "auth-state source-access provenance")
    assert_no_forbidden_source_access_material(payload)
    source_access_posture = _validate_source_access_posture(payload.get("source_access_posture"))
    expected_posture = _validate_source_access_posture(expected_source_access_posture)
    if source_access_posture != expected_posture:
        raise ValueError(
            "auth-state source-access posture mismatch: "
            f"metadata has {source_access_posture!r} but capture declared {expected_posture!r}"
        )
    state_hash = _validate_sha256(payload.get(STATE_CONTENT_SHA256_KEY), field=STATE_CONTENT_SHA256_KEY)
    if state_hash != sha256_file(state_path):
        raise ValueError("auth-state source-access provenance state-content binding mismatch")
    harness_proxy_profile_posture = _validate_harness_proxy_profile_posture(
        payload.get("harness_proxy_profile_posture")
    )
    if required_harness_proxy_profile_posture is not None:
        required = _validate_harness_proxy_profile_posture(required_harness_proxy_profile_posture)
        if required == HarnessProxyProfilePosture.UNKNOWN.value:
            raise ValueError("cannot require unknown harness proxy-profile posture")
        if harness_proxy_profile_posture != required:
            raise ValueError(
                "auth-state harness proxy-profile posture mismatch: "
                f"metadata has {harness_proxy_profile_posture!r} but capture required {required!r}"
            )
    result: dict[str, object] = {
        "source_access_posture": source_access_posture,
        "browser_backend": _validate_browser_backend(payload.get("browser_backend")),
        "harness_proxy_profile_posture": harness_proxy_profile_posture,
        "proxy_category": _validate_proxy_category(payload.get("proxy_category")),
        WARMUP_USER_DATA_LABEL_SHA256_KEY: _validate_sha256(
            payload.get(WARMUP_USER_DATA_LABEL_SHA256_KEY),
            field=WARMUP_USER_DATA_LABEL_SHA256_KEY,
        ),
        STATE_CONTENT_SHA256_KEY: state_hash,
        "no_secret_scan": _validate_no_secret_scan(payload.get("no_secret_scan")),
    }
    _validate_proxy_category_matches_posture(result)
    assert_no_forbidden_source_access_material(result)
    return result


def assert_no_forbidden_source_access_material(payload: Mapping[str, Any]) -> None:
    _scan_forbidden_material(payload, path=())


def _scan_forbidden_material(value: Any, *, path: tuple[str, ...]) -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("source-access provenance keys must be strings")
            normalized_key = key.lower().replace("-", "_")
            if any(fragment in normalized_key for fragment in _FORBIDDEN_KEY_FRAGMENTS):
                raise ValueError(f"source-access provenance contains forbidden field: {'.'.join((*path, key))}")
            _scan_forbidden_material(item, path=(*path, key))
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _scan_forbidden_material(item, path=(*path, str(index)))
        return
    if isinstance(value, str):
        stripped = value.strip()
        if (
            _URL_SCHEME_RE.search(stripped)
            or _IPV4_RE.search(stripped)
            or _HOST_PORT_RE.search(stripped)
            or stripped.startswith(("/", "\\"))
            or _WINDOWS_ABSOLUTE_PATH_RE.search(stripped)
        ):
            location = ".".join(path) if path else "<root>"
            raise ValueError(f"source-access provenance contains forbidden value pattern at {location}")


def _assert_mapping(payload: Mapping[str, Any], label: str) -> None:
    if not isinstance(payload, Mapping):
        raise ValueError(f"{label} must be a JSON object")


def _validate_schema_version(payload: Mapping[str, Any]) -> None:
    if payload.get("schema_version") != SOURCE_ACCESS_PROVENANCE_SCHEMA_VERSION:
        raise ValueError(
            "source-access provenance schema_version must be "
            f"{SOURCE_ACCESS_PROVENANCE_SCHEMA_VERSION}"
        )


def _validate_browser_backend(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("source-access provenance browser_backend must be a string")
    normalized = value.strip().lower()
    if normalized not in BROWSER_BACKENDS:
        raise ValueError(f"source-access provenance browser_backend must be one of {sorted(BROWSER_BACKENDS)}")
    return normalized


def _validate_source_access_posture(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("source_access_posture must be a string")
    normalized = value.strip()
    if normalized not in SOURCE_ACCESS_POSTURES:
        raise ValueError(f"source_access_posture must be one of {sorted(SOURCE_ACCESS_POSTURES)}")
    return normalized


def _validate_harness_proxy_profile_posture(value: object) -> str:
    if isinstance(value, HarnessProxyProfilePosture):
        return value.value
    if not isinstance(value, str):
        raise ValueError("harness_proxy_profile_posture must be a string")
    try:
        return HarnessProxyProfilePosture(value.strip()).value
    except ValueError as exc:
        allowed = [item.value for item in HarnessProxyProfilePosture]
        raise ValueError(f"harness_proxy_profile_posture must be one of {allowed}") from exc


def _validate_proxy_category(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("proxy_category must be a non-empty string")
    normalized = value.strip()
    allowed = {PROXY_CATEGORY_NONE, *(item.value for item in ProxyCategory)}
    if normalized not in allowed:
        raise ValueError(f"proxy_category must be one of {sorted(allowed)}")
    return normalized


def _validate_no_secret_scan(value: object) -> str:
    if value != NO_SECRET_SCAN_PASSED:
        raise ValueError("source-access provenance no_secret_scan must be 'passed'")
    return NO_SECRET_SCAN_PASSED


def _validate_sha256(value: object, *, field: str) -> str:
    if not isinstance(value, str) or _SHA256_RE.fullmatch(value) is None:
        raise ValueError(f"{field} must be a lowercase sha256 hex digest")
    return value


def _validate_proxy_category_matches_posture(payload: Mapping[str, object]) -> None:
    posture = payload.get("harness_proxy_profile_posture")
    category = payload.get("proxy_category")
    if posture == HarnessProxyProfilePosture.NO_PROXY_PROFILE_LOADED.value and category != PROXY_CATEGORY_NONE:
        raise ValueError("proxy_category must be 'none' when no proxy profile was loaded")
    if posture == HarnessProxyProfilePosture.PROXY_PROFILE_LOADED.value and category == PROXY_CATEGORY_NONE:
        raise ValueError("proxy_category must name the proxy category when a proxy profile was loaded")
