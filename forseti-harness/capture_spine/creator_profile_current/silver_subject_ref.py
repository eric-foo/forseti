"""Shared subject-ref helpers for creator-metric Silver records."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from capture_spine.creator_profile_current.silver_envelope_core import (
    required_subject_native_id,
)

FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY = "forseti_platform_account_id"
LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY = "orca_platform_account_id"


def platform_account_ref_field(platform_account_id: Any, *, what: str) -> dict[str, str]:
    """Build the Forseti-native account-id field for a Silver subject ref."""
    return {
        FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY: required_subject_native_id(
            platform_account_id, what=what
        )
    }


def platform_account_id_from_subject_ref(
    subject_ref: Mapping[str, Any], *, what: str = "Silver subject ref"
) -> str:
    """Read the Forseti account-id key, falling back to legacy Orca records."""
    if not isinstance(subject_ref, Mapping):
        raise TypeError(f"{what} must be a mapping")
    value = subject_ref.get(FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY)
    legacy_value = subject_ref.get(LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY)
    if value is not None and legacy_value is not None:
        account_id = required_subject_native_id(value, what=what)
        legacy_account_id = required_subject_native_id(legacy_value, what=f"legacy {what}")
        if account_id != legacy_account_id:
            raise ValueError(
                f"{what} has conflicting account ids for "
                f"{FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY!r} and "
                f"{LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY!r}"
            )
        return account_id
    if value is None:
        value = legacy_value
    if value is None:
        raise KeyError(
            f"{what} lacks {FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY!r} "
            f"(legacy {LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY!r})"
        )
    return required_subject_native_id(value, what=what)


__all__ = [
    "FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY",
    "LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY",
    "platform_account_id_from_subject_ref",
    "platform_account_ref_field",
]
