"""Select account-scoped social creator onboarding candidates from registry truth."""

from __future__ import annotations

from typing import Any, Mapping


SOCIAL_CREATOR_ONBOARDING_PLATFORMS = frozenset(
    {"instagram", "tiktok", "youtube"}
)
SELECTION_POLICY = "sole_not_onboarded_platform_account"


class CreatorOnboardingSelectionError(ValueError):
    """Raised when the internal registry cannot supply an eligible candidate."""


def eligible_creator_onboarding_candidates(
    registry_document: Mapping[str, Any],
    *,
    platform: str,
) -> list[dict[str, str]]:
    """Return deterministic account-scoped candidates not yet onboarded."""

    normalized_platform = platform.strip().lower()
    if normalized_platform not in SOCIAL_CREATOR_ONBOARDING_PLATFORMS:
        raise CreatorOnboardingSelectionError(
            f"unsupported social creator onboarding platform {platform!r}"
        )
    wrapper = registry_document.get("creator_profile_current_view")
    if not isinstance(wrapper, Mapping):
        raise CreatorOnboardingSelectionError(
            "Creator Registry has no creator_profile_current_view object"
        )
    profiles = wrapper.get("profiles")
    if not isinstance(profiles, list):
        raise CreatorOnboardingSelectionError(
            "Creator Registry has no profiles list"
        )

    candidates: list[dict[str, str]] = []
    for profile in profiles:
        if not isinstance(profile, Mapping):
            continue
        if profile.get("profile_subject_kind") != "platform_account":
            continue
        onboarding = profile.get("onboarding")
        if (
            not isinstance(onboarding, Mapping)
            or onboarding.get("onboarding_state") != "not_onboarded"
        ):
            continue
        accounts = profile.get("platform_accounts")
        if not isinstance(accounts, list) or len(accounts) != 1:
            continue
        account = accounts[0]
        if (
            not isinstance(account, Mapping)
            or str(account.get("platform") or "").strip().lower()
            != normalized_platform
        ):
            continue
        candidate = {
            "platform": normalized_platform,
            "platform_account_id": _required_text(
                account.get("platform_account_id"), "platform_account_id"
            ),
            "public_handle": _required_text(
                account.get("public_handle"), "public_handle"
            ),
            "public_profile_url": _required_text(
                account.get("public_profile_url"), "public_profile_url"
            ),
        }
        candidates.append(candidate)
    return candidates


def select_creator_onboarding_candidate(
    registry_document: Mapping[str, Any],
    *,
    platform: str,
    platform_account_id: str | None = None,
) -> dict[str, str]:
    """Resolve an exact eligible account, or auto-select an eligible singleton."""

    candidates = eligible_creator_onboarding_candidates(
        registry_document,
        platform=platform,
    )
    if platform_account_id is not None:
        normalized_account_id = platform_account_id.strip()
        exact = [
            candidate
            for candidate in candidates
            if candidate["platform_account_id"] == normalized_account_id
        ]
        if len(exact) != 1:
            raise CreatorOnboardingSelectionError(
                f"Creator Registry account {platform_account_id!r} is not an eligible "
                f"not_onboarded {platform.strip().lower()} account"
            )
        return {**exact[0], "selection_policy": "exact_platform_account_id"}
    if not candidates:
        raise CreatorOnboardingSelectionError(
            f"Creator Registry has no not_onboarded {platform.strip().lower()} account"
        )
    if len(candidates) != 1:
        candidate_ids = [
            candidate["platform_account_id"] for candidate in candidates
        ]
        raise CreatorOnboardingSelectionError(
            f"Creator Registry has {len(candidates)} not_onboarded "
            f"{platform.strip().lower()} accounts; select one exact platform_account_id "
            f"from {candidate_ids}"
        )
    return {**candidates[0], "selection_policy": SELECTION_POLICY}


def _required_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CreatorOnboardingSelectionError(
            f"eligible Creator Registry account has no {field_name}"
        )
    return value.strip()
