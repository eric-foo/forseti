"""Unit tests for Silver subject-ref account-id helpers."""
from __future__ import annotations

import pytest

from capture_spine.creator_profile_current.silver_subject_ref import (
    FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY,
    LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY,
    platform_account_id_from_subject_ref,
    platform_account_ref_field,
)


def test_platform_account_ref_field_writes_forseti_key_only() -> None:
    ref = platform_account_ref_field("acct_123", what="account id")

    assert ref == {FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY: "acct_123"}
    assert LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY not in ref


def test_platform_account_id_from_subject_ref_reads_legacy_key() -> None:
    assert (
        platform_account_id_from_subject_ref(
            {LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY: "acct_legacy"},
            what="rollup subject ref",
        )
        == "acct_legacy"
    )


def test_platform_account_id_from_subject_ref_rejects_conflicting_keys() -> None:
    with pytest.raises(ValueError, match="conflicting account ids"):
        platform_account_id_from_subject_ref(
            {
                FORSETI_PLATFORM_ACCOUNT_ID_REF_KEY: "acct_new",
                LEGACY_ORCA_PLATFORM_ACCOUNT_ID_REF_KEY: "acct_old",
            },
            what="rollup subject ref",
        )