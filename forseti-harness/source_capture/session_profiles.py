from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

from source_capture.auth_state import (
    AuthenticatedSessionMode,
    validate_auth_state_provenance_requirement,
)
from source_capture.local_secret_store import label_to_filename
from source_capture.source_access_provenance import HarnessProxyProfilePosture


SESSION_PROFILE_CONFIG_SCHEMA_VERSION = "source_capture_session_profiles_v0"
FORSETI_AUTH_STATE_ROOT_ENV = "FORSETI_AUTH_STATE_ROOT"
FORSETI_SESSION_PROFILE_CONFIG_ENV = "FORSETI_SESSION_PROFILE_CONFIG"
MAX_SESSION_PROFILE_CONFIG_BYTES = 64_000
OWNER_HANDOFF_BEFORE_ACTION = "owner_handoff_before_action"
_SESSION_PROFILE_KIND = "session-profile"
_ALLOWED_PROFILE_FIELDS = {
    "platform",
    "state_label",
    "session_mode",
    "required_harness_proxy_profile_posture",
    "browser_backend",
    "challenge_policy",
    "browser_user_data_label",
}


@dataclass(frozen=True)
class SourceCaptureSessionProfile:
    alias: str
    platform: str
    state_label: str
    session_mode: AuthenticatedSessionMode
    required_harness_proxy_profile_posture: HarnessProxyProfilePosture
    browser_backend: str
    challenge_policy: str
    browser_user_data_label: str | None = None


def default_session_profile_config_path() -> Path:
    configured_path = os.environ.get(FORSETI_SESSION_PROFILE_CONFIG_ENV)
    if configured_path:
        return Path(configured_path).expanduser()
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "Forseti" / "source_capture_session_profiles.json"
    return Path.home() / ".forseti" / "source_capture_session_profiles.json"


def default_session_profile_auth_state_root() -> Path:
    configured_root = os.environ.get(FORSETI_AUTH_STATE_ROOT_ENV)
    if configured_root:
        return Path(configured_root).expanduser()
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "Forseti" / "auth_state"
    return Path.home() / ".forseti" / "auth_state"


def resolve_session_profile(
    alias: str,
    *,
    config_path: Path | None = None,
) -> SourceCaptureSessionProfile:
    label_to_filename(alias, kind=_SESSION_PROFILE_KIND)
    path = config_path or default_session_profile_config_path()
    try:
        if not path.is_file():
            raise ValueError(
                f"session-profile config is unavailable for alias: {alias}"
            )
        if path.stat().st_size > MAX_SESSION_PROFILE_CONFIG_BYTES:
            raise ValueError(
                f"session-profile config exceeds {MAX_SESSION_PROFILE_CONFIG_BYTES} byte cap"
            )
        raw_payload = path.read_text(encoding="utf-8")
    except OSError:
        raise ValueError("session-profile config is unreadable") from None
    try:
        payload = json.loads(raw_payload)
    except json.JSONDecodeError:
        raise ValueError("session-profile config is not valid JSON") from None
    if not isinstance(payload, dict):
        raise ValueError("session-profile config must be a JSON object")
    if payload.get("schema_version") != SESSION_PROFILE_CONFIG_SCHEMA_VERSION:
        raise ValueError("session-profile config schema version is unsupported")
    profiles = payload.get("profiles")
    if not isinstance(profiles, dict):
        raise ValueError("session-profile config must contain a profiles object")
    profile_payload = profiles.get(alias)
    if not isinstance(profile_payload, dict):
        raise ValueError(f"session-profile alias is unavailable: {alias}")
    unknown_fields = sorted(set(profile_payload) - _ALLOWED_PROFILE_FIELDS)
    if unknown_fields:
        raise ValueError(
            "session-profile contains unsupported fields: " + ", ".join(unknown_fields)
        )

    platform = _required_string(profile_payload, "platform")
    if platform != "tiktok":
        raise ValueError("session-profile platform must be tiktok")
    state_label = _required_string(profile_payload, "state_label")
    label_to_filename(state_label, kind="auth-state")
    try:
        session_mode = AuthenticatedSessionMode(
            _required_string(profile_payload, "session_mode")
        )
    except ValueError:
        raise ValueError("session-profile session_mode is unsupported") from None
    try:
        proxy_posture = HarnessProxyProfilePosture(
            _required_string(
                profile_payload, "required_harness_proxy_profile_posture"
            )
        )
    except ValueError:
        raise ValueError(
            "session-profile required_harness_proxy_profile_posture is unsupported"
        ) from None
    browser_backend = _required_string(profile_payload, "browser_backend")
    if browser_backend not in {"cloakbrowser", "chrome_cdp"}:
        raise ValueError(
            "TikTok session-profile browser_backend must be cloakbrowser or chrome_cdp"
        )
    challenge_policy = _required_string(profile_payload, "challenge_policy")
    if challenge_policy != OWNER_HANDOFF_BEFORE_ACTION:
        raise ValueError(
            "TikTok session-profile challenge_policy must be owner_handoff_before_action"
        )
    browser_user_data_label = profile_payload.get("browser_user_data_label")
    if browser_user_data_label is not None:
        if (
            not isinstance(browser_user_data_label, str)
            or not browser_user_data_label.strip()
        ):
            raise ValueError(
                "session-profile browser_user_data_label must be a non-empty string"
            )
        browser_user_data_label = browser_user_data_label.strip()
        label_to_filename(
            browser_user_data_label, kind="browser user-data", suffix=""
        )
    return SourceCaptureSessionProfile(
        alias=alias,
        platform=platform,
        state_label=state_label,
        session_mode=session_mode,
        required_harness_proxy_profile_posture=proxy_posture,
        browser_backend=browser_backend,
        challenge_policy=challenge_policy,
        browser_user_data_label=browser_user_data_label,
    )


def validate_session_profile_auth_state(
    profile: SourceCaptureSessionProfile,
    *,
    auth_state_root: Path | None = None,
) -> None:
    resolved_auth_state_root = auth_state_root or default_session_profile_auth_state_root()
    try:
        validate_auth_state_provenance_requirement(
            profile.state_label,
            session_mode=profile.session_mode,
            required_harness_proxy_profile_posture=(
                profile.required_harness_proxy_profile_posture
            ),
            auth_state_root=resolved_auth_state_root,
        )
    except (OSError, ValueError) as exc:
        raise ValueError(
            "session-profile auth state blocked: "
            + _profile_auth_state_blocker_code(str(exc))
        ) from None


def _profile_auth_state_blocker_code(detail: str) -> str:
    normalized = detail.lower()
    if "file does not exist" in normalized:
        return "auth_state_missing"
    if "metadata sidecar does not exist" in normalized:
        return "auth_state_metadata_missing"
    if "permission denied" in normalized or "access is denied" in normalized:
        return "auth_state_unreadable"
    if "missing or legacy-only" in normalized or "provenance is missing" in normalized:
        return "auth_state_provenance_missing"
    if "mismatch" in normalized:
        return "auth_state_provenance_mismatch"
    return "auth_state_invalid"


def sanitized_session_profile_preflight(
    profile: SourceCaptureSessionProfile,
) -> dict[str, object]:
    return {
        "status": "available",
        "session_profile": profile.alias,
        "platform": profile.platform,
        "session_mode": profile.session_mode.value,
        "required_harness_proxy_profile_posture": (
            profile.required_harness_proxy_profile_posture.value
        ),
        "browser_backend": profile.browser_backend,
        "challenge_policy": profile.challenge_policy,
        "persistent_browser_profile_configured": (
            profile.browser_user_data_label is not None
        ),
        "auth_state_validated": True,
        "secret_values_exposed": False,
    }


def _required_string(payload: dict[str, object], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"session-profile field must be a non-empty string: {field}")
    return value.strip()


__all__ = [
    "FORSETI_SESSION_PROFILE_CONFIG_ENV",
    "FORSETI_AUTH_STATE_ROOT_ENV",
    "MAX_SESSION_PROFILE_CONFIG_BYTES",
    "OWNER_HANDOFF_BEFORE_ACTION",
    "SESSION_PROFILE_CONFIG_SCHEMA_VERSION",
    "SourceCaptureSessionProfile",
    "default_session_profile_config_path",
    "default_session_profile_auth_state_root",
    "resolve_session_profile",
    "sanitized_session_profile_preflight",
    "validate_session_profile_auth_state",
]
