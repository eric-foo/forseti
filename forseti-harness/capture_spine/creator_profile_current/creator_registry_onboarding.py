"""Derive Creator Registry onboarding state from public committed Bronze packets.

Onboarding is account-scoped: a registry account is onboarded after at least one
complete, verified, publicly available packet from a qualifying content-capture
surface can be attributed exactly to that account. Discovery packets, RSS
heartbeats, scratch directories, staging output, and public-consumption
tombstones never qualify.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard


ONBOARDING_POLICY_VERSION = "creator_registry_onboarding_v0"
QUALIFYING_SURFACES: tuple[tuple[str, str], ...] = (
    ("instagram_creator", "ig_reels_grid_dom_passive_json"),
    ("tiktok", "tiktok_creator_batch_comment_subtitle_admission"),
    ("tiktok", "tiktok_creator_grid_window"),
    ("tiktok", "tiktok_video_comment_subtitle_admission"),
    ("youtube", "youtube_watch_metadata_comments"),
)
EXCLUDED_SURFACES = (
    "youtube_channel_rss_feed",
    "tiktok_logged_out_profile_browser_snapshot",
    "tiktok_profile_suggested_accounts_admission",
)
_YOUTUBE_CAPTURE_SCHEMAS = frozenset(
    {
        "youtube_watch_metadata_comments_capture_v0",
        "youtube_watch_metadata_comments_capture_v1",
    }
)
_TIKTOK_HANDLE_FROM_VIDEO_URL = re.compile(r"^https://www\.tiktok\.com/@([^/]+)/video/\d+")


class CreatorRegistryOnboardingError(ValueError):
    """Fail-closed onboarding derivation or registry refresh error."""


@dataclass(frozen=True)
class OnboardingEvidence:
    platform_account_id: str
    packet_id: str
    source_family: str
    source_surface: str
    captured_at: str

    def sort_key(self) -> tuple[str, str]:
        return self.captured_at, self.packet_id


def derive_onboarding_by_account(
    *, data_root: DataLakeRoot, platform_accounts: Sequence[Mapping[str, Any]]
) -> dict[str, dict[str, Any]]:
    """Return one deterministic onboarding block for every registry account."""
    return derive_onboarding_snapshot(
        data_root=data_root,
        platform_accounts=platform_accounts,
    )["accounts"]


def derive_onboarding_snapshot(
    *, data_root: DataLakeRoot, platform_accounts: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    """Return account states plus visible packet-attribution diagnostics."""
    accounts = [_account_mapping(account) for account in platform_accounts]
    accounts_by_id = {str(account["platform_account_id"]): account for account in accounts}
    if len(accounts_by_id) != len(accounts):
        raise CreatorRegistryOnboardingError("duplicate platform_account_id in Creator Registry")
    by_native_id, by_handle = _identity_indexes(accounts)
    earliest: dict[str, OnboardingEvidence] = {}
    qualifying_packet_count = 0
    attributable_packet_count = 0
    unmatched_packet_count = 0
    unattributable_legacy_packet_ids: list[str] = []
    data_root._reverify()

    for packet_id, manifest in _iter_committed_manifests(data_root):
        family = _optional_text(manifest.get("source_family"))
        surface = _optional_text(manifest.get("source_surface"))
        if (family, surface) not in QUALIFYING_SURFACES:
            continue
        qualifying_packet_count += 1
        identity = _packet_identity(
            data_root=data_root,
            packet_id=packet_id,
            source_family=family,
            source_surface=surface,
            manifest=manifest,
        )
        if identity is None:
            unattributable_legacy_packet_ids.append(packet_id)
            continue
        account_id = _match_account(
            identity=identity,
            by_native_id=by_native_id,
            by_handle=by_handle,
        )
        if account_id is None:
            unmatched_packet_count += 1
            continue
        attributable_packet_count += 1
        evidence = OnboardingEvidence(
            platform_account_id=account_id,
            packet_id=packet_id,
            source_family=family,
            source_surface=surface,
            captured_at=_capture_time(manifest, packet_id=packet_id),
        )
        previous = earliest.get(account_id)
        if previous is None or evidence.sort_key() < previous.sort_key():
            earliest[account_id] = evidence

    return {
        "policy_version": ONBOARDING_POLICY_VERSION,
        "accounts": {
            account_id: _onboarding_block(earliest.get(account_id))
            for account_id in sorted(accounts_by_id)
        },
        "diagnostics": {
            "qualifying_packet_count": qualifying_packet_count,
            "attributable_registry_packet_count": attributable_packet_count,
            "unmatched_registry_packet_count": unmatched_packet_count,
            "unattributable_legacy_packet_count": len(unattributable_legacy_packet_ids),
            "unattributable_legacy_packet_ids": sorted(unattributable_legacy_packet_ids),
        },
    }


def refresh_creator_registry_index_document(
    *,
    current_document: Mapping[str, Any],
    account_ledger: Mapping[str, Any],
    onboarding_by_account: Mapping[str, Mapping[str, Any]],
    generated_at_utc: str,
    data_root_uuid: str,
    account_ledger_sha256: str,
    derivation_diagnostics: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Refresh identity mirrors and onboarding state without rewriting identity truth."""
    wrapper = _mapping(current_document.get("creator_registry_index"), "creator_registry_index")
    ledger_accounts = list(_mapping(account_ledger, "account_ledger").get("platform_accounts", []))
    current_rows = list(wrapper.get("platform_accounts", []))
    current_by_id = {
        str(_mapping(row, "registry account").get("platform_account_id")): deepcopy(row)
        for row in current_rows
    }
    creator_by_account = _creator_record_links(account_ledger)
    refreshed_rows: list[dict[str, Any]] = []

    for index, raw_account in enumerate(ledger_accounts):
        account = _account_mapping(raw_account)
        account_id = str(account["platform_account_id"])
        onboarding = onboarding_by_account.get(account_id)
        if onboarding is None:
            raise CreatorRegistryOnboardingError(
                f"onboarding derivation omitted registry account {account_id!r}"
            )
        row = current_by_id.get(account_id)
        if row is None:
            row = _new_registry_row(
                account=account,
                account_index=index,
                creator_record_id=creator_by_account.get(account_id),
            )
        _refresh_identity_fields(
            row=row,
            account=account,
            account_index=index,
            creator_record_id=creator_by_account.get(account_id),
        )
        row["onboarding"] = deepcopy(dict(onboarding))
        if onboarding.get("onboarding_state") == "onboarded":
            if row.get("capture_state") == "never_captured":
                row["capture_state"] = "identity_observed_content_packet_available"
            row["freshness"]["last_capture_observed_at_or_none"] = _latest_timestamp(
                row["freshness"].get("last_capture_observed_at_or_none"),
                onboarding.get("onboarded_at_or_none"),
            )
        refreshed_rows.append(row)

    document = deepcopy(dict(current_document))
    refreshed = document["creator_registry_index"]
    refreshed["index_mode"] = "materialized_known_public_account_dedupe_and_onboarding_index"
    refreshed["generated_at_utc"] = generated_at_utc
    refreshed["source_policy_posture"] = (
        "Creator Registry lookup and routing projection generated from the public-handle "
        "linkage ledger, with account onboarding derived from verified committed Bronze "
        "content-capture packets under an exact-identity policy. It is not metric authority, "
        "raw capture storage, freshness SLA, or final cross-platform identity proof."
    )
    refreshed["source_inputs"] = [
        {
            "source_pointer": (
                "forseti/product/spines/capture/core/source_families/social_media/"
                "creator_registry/creator_public_handle_linkage_ledger_v0.json"
            ),
            "sha256": account_ledger_sha256,
            "role": "source-backed known public platform accounts and linkage state",
        }
    ]
    refreshed["onboarding_policy"] = {
        "policy_version": ONBOARDING_POLICY_VERSION,
        "data_root_uuid": data_root_uuid,
        "qualifying_source_surfaces": [
            {"source_family": family, "source_surface": surface}
            for family, surface in QUALIFYING_SURFACES
        ],
        "explicitly_non_qualifying_surfaces": list(EXCLUDED_SURFACES),
        "state_semantics": (
            "not_onboarded means no exactly attributable, publicly available qualifying "
            "committed Bronze packet was found; onboarded means at least one such packet "
            "was verified"
        ),
        "monotonicity": (
            "onboarded is monotonic over publicly available immutable Bronze history; "
            "owner-directed public-consumption tombstones remove packets from eligibility"
        ),
        "derivation_diagnostics": deepcopy(dict(derivation_diagnostics or {})),
    }
    refreshed["platform_accounts"] = refreshed_rows
    refreshed["counts"] = _registry_counts(refreshed_rows, refreshed.get("creator_records", []))
    refreshed["accepted_residuals"] = [
        "Onboarding proves one publicly available qualifying committed capture for one platform account; it does not prove capture freshness, completeness across all content, or recurring monitoring.",
        "Accounts without a qualifying packet remain not_onboarded even when discovery, RSS, challenge-limited profile, or scratch/staging evidence exists.",
        "TikTok and Instagram handle-only attribution remains exact same-platform handle matching until a platform-native public account id is available; ambiguous registry keys fail the refresh.",
        "The checked-in registry remains a generated static projection refreshed by an operator runner, not a runtime database.",
    ]
    _validate_refreshed_registry(refreshed, ledger_accounts)
    return document


def dump_creator_registry_index(document: Mapping[str, Any]) -> str:
    return json.dumps(document, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def sha256_repo_text(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _iter_committed_manifests(data_root: DataLakeRoot):
    raw_root = data_root.path / "raw"
    if not raw_root.is_dir():
        return
    tombstoned_packet_ids = data_root.tombstoned_packet_ids()
    for shard in sorted(raw_root.iterdir()):
        if not shard.is_dir():
            continue
        for container in sorted(shard.iterdir()):
            if not container.is_dir():
                continue
            packet_id = container.name
            if packet_id in tombstoned_packet_ids:
                continue
            manifest_path = container / "manifest.json"
            if not manifest_path.is_file():
                raise DataLakeRootError(
                    f"committed raw packet directory missing manifest.json: {container}"
                )
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                raise DataLakeRootError(f"unreadable raw manifest at {manifest_path}: {exc}") from exc
            if not isinstance(manifest, dict) or manifest.get("packet_id") != packet_id:
                raise DataLakeRootError(
                    f"raw manifest packet_id mismatch at {manifest_path}: {manifest.get('packet_id')!r}"
                )
            yield packet_id, manifest


def _identity_indexes(accounts: Sequence[Mapping[str, Any]]):
    by_native: dict[tuple[str, str], str] = {}
    by_handle: dict[tuple[str, str], str] = {}
    for account in accounts:
        account_id = str(account["platform_account_id"])
        platform = _required_text(account.get("platform"), "platform").lower()
        native_id = _optional_text(account.get("platform_public_account_id_or_none"))
        if native_id:
            _insert_unique(by_native, (platform, native_id), account_id, "platform public account id")
        handle = _normalize_handle(account.get("public_handle"))
        _insert_unique(by_handle, (platform, handle), account_id, "same-platform public handle")
    return by_native, by_handle


def _insert_unique(index: dict, key: tuple[str, str], account_id: str, role: str) -> None:
    previous = index.get(key)
    if previous is not None and previous != account_id:
        raise CreatorRegistryOnboardingError(
            f"ambiguous {role} {key!r}: matches {previous!r} and {account_id!r}"
        )
    index[key] = account_id


def _packet_identity(
    *,
    data_root: DataLakeRoot,
    packet_id: str,
    source_family: str,
    source_surface: str,
    manifest: Mapping[str, Any],
) -> dict[str, str] | None:
    if source_surface == "youtube_watch_metadata_comments":
        payload = _json_body(data_root, packet_id, manifest, "youtube_watch_capture.json")
        schema = _required_text(payload.get("capture_schema_version"), "YouTube capture schema")
        if schema not in _YOUTUBE_CAPTURE_SCHEMAS:
            raise CreatorRegistryOnboardingError(f"unsupported YouTube capture schema: {schema!r}")
        packet = _mapping(payload.get("packet"), "YouTube capture packet")
        channel = _mapping(packet.get("channel"), "YouTube capture channel")
        channel_id = _optional_text(channel.get("channel_id"))
        if channel_id is None and schema == "youtube_watch_metadata_comments_capture_v0":
            return None
        return {
            "platform": "youtube",
            "native_id": _required_text(channel_id, "YouTube channel_id"),
        }
    if source_surface == "ig_reels_grid_dom_passive_json":
        payload = _json_body(data_root, packet_id, manifest, "ig_reels_grid_capture.json")
        snapshot = _mapping(payload.get("creator_profile_snapshot"), "Instagram creator snapshot")
        identity = {
            "platform": "instagram",
            "handle": _normalize_handle(snapshot.get("source_profile")),
        }
        numeric_id = _optional_text(snapshot.get("numeric_id"))
        if numeric_id:
            identity["native_id"] = numeric_id
        return identity
    if source_surface == "tiktok_creator_grid_window":
        payload = _json_body(data_root, packet_id, manifest, "tiktok_grid_window.json")
        return {"platform": "tiktok", "handle": _normalize_handle(payload.get("creator_handle"))}
    if source_surface == "tiktok_creator_batch_comment_subtitle_admission":
        payload = _json_body(data_root, packet_id, manifest, "tiktok_batch_capture.json")
        return {"platform": "tiktok", "handle": _normalize_handle(payload.get("creator_handle"))}
    if source_surface == "tiktok_video_comment_subtitle_admission":
        payload = _json_body(data_root, packet_id, manifest, "tiktok_video_capture.json")
        url = _required_text(payload.get("video_url"), "TikTok video_url")
        match = _TIKTOK_HANDLE_FROM_VIDEO_URL.match(url)
        if match is None:
            raise CreatorRegistryOnboardingError(
                f"TikTok video packet has non-canonical creator URL: {url!r}"
            )
        return {"platform": "tiktok", "handle": _normalize_handle(match.group(1))}
    raise CreatorRegistryOnboardingError(
        f"no onboarding identity extractor for {source_family}/{source_surface}"
    )


def _json_body(
    data_root: DataLakeRoot,
    packet_id: str,
    manifest: Mapping[str, Any],
    suffix: str,
) -> dict[str, Any]:
    matches: list[Mapping[str, Any]] = []
    for preserved in manifest.get("preserved_files", []):
        if not isinstance(preserved, Mapping):
            continue
        relative = _optional_text(preserved.get("relative_packet_path"))
        file_id = _optional_text(preserved.get("file_id"))
        if relative and file_id and relative.replace("\\", "/").endswith(suffix):
            matches.append(preserved)
    if len(matches) != 1:
        raise CreatorRegistryOnboardingError(
            f"qualifying packet must preserve exactly one {suffix}; found {len(matches)}"
        )
    preserved = matches[0]
    relative = _required_text(preserved.get("relative_packet_path"), "relative_packet_path")
    if "\\" in relative or relative in {"", "."}:
        raise CreatorRegistryOnboardingError(
            f"packet member path must be packet-relative POSIX: {relative!r}"
        )
    parts = tuple(relative.split("/"))
    if not parts or any(part in {"", ".", ".."} for part in parts):
        raise CreatorRegistryOnboardingError(f"unsafe packet member path: {relative!r}")
    path = data_root._within("raw", raw_shard(packet_id), packet_id, *parts)
    if not path.is_file():
        raise CreatorRegistryOnboardingError(
            f"qualifying packet member is missing: {packet_id}/{relative}"
        )
    body = path.read_bytes()
    expected_size = preserved.get("size_bytes")
    if type(expected_size) is not int or len(body) != expected_size:
        raise CreatorRegistryOnboardingError(
            f"qualifying packet member size mismatch: {packet_id}/{relative}"
        )
    expected_sha = _required_text(preserved.get("sha256"), "preserved member sha256")
    if hashlib.sha256(body).hexdigest() != expected_sha:
        raise CreatorRegistryOnboardingError(
            f"qualifying packet member sha256 mismatch: {packet_id}/{relative}"
        )
    try:
        payload = json.loads(body.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CreatorRegistryOnboardingError(f"invalid JSON body {suffix}: {exc}") from exc
    return dict(_mapping(payload, suffix))


def _match_account(
    *,
    identity: Mapping[str, str],
    by_native_id: Mapping[tuple[str, str], str],
    by_handle: Mapping[tuple[str, str], str],
) -> str | None:
    platform = identity["platform"]
    native_id = identity.get("native_id")
    handle = identity.get("handle")
    native_match = by_native_id.get((platform, native_id)) if native_id else None
    handle_match = by_handle.get((platform, handle)) if handle else None
    if native_match and handle_match and native_match != handle_match:
        raise CreatorRegistryOnboardingError(
            f"qualifying packet identity conflicts: native id maps to {native_match!r}, "
            f"handle maps to {handle_match!r}"
        )
    return native_match or handle_match


def _capture_time(manifest: Mapping[str, Any], *, packet_id: str) -> str:
    timing = _mapping(manifest.get("timing"), f"packet {packet_id} timing")
    fact = _mapping(timing.get("capture_time"), f"packet {packet_id} capture_time")
    if fact.get("status") != "known":
        raise CreatorRegistryOnboardingError(
            f"qualifying packet {packet_id} capture_time must be known"
        )
    return _required_text(fact.get("value"), f"packet {packet_id} capture_time.value")


def _onboarding_block(evidence: OnboardingEvidence | None) -> dict[str, Any]:
    if evidence is None:
        return {
            "onboarding_state": "not_onboarded",
            "onboarded_at_or_none": None,
            "evidence_packet_id_or_none": None,
            "evidence_source_family_or_none": None,
            "evidence_source_surface_or_none": None,
            "policy_version": ONBOARDING_POLICY_VERSION,
        }
    return {
        "onboarding_state": "onboarded",
        "onboarded_at_or_none": evidence.captured_at,
        "evidence_packet_id_or_none": evidence.packet_id,
        "evidence_source_family_or_none": evidence.source_family,
        "evidence_source_surface_or_none": evidence.source_surface,
        "policy_version": ONBOARDING_POLICY_VERSION,
    }


def _creator_record_links(account_ledger: Mapping[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for record in account_ledger.get("creator_records", []):
        if not isinstance(record, Mapping):
            continue
        creator_id = _required_text(record.get("creator_record_id"), "creator_record_id")
        for account_id in record.get("platform_account_ids", []):
            account_id = _required_text(account_id, "creator_record platform_account_id")
            if account_id in result and result[account_id] != creator_id:
                raise CreatorRegistryOnboardingError(
                    f"platform account {account_id!r} belongs to multiple creator records"
                )
            result[account_id] = creator_id
    return result


def _new_registry_row(
    *, account: Mapping[str, Any], account_index: int, creator_record_id: str | None
) -> dict[str, Any]:
    return {
        "platform_account_id": account["platform_account_id"],
        "platform": account["platform"],
        "platform_public_account_id_or_none": account.get("platform_public_account_id_or_none"),
        "public_handle": account["public_handle"],
        "normalized_public_handle": _normalize_handle(account["public_handle"]),
        "public_profile_url": account["public_profile_url"],
        "creator_record_id_or_none": creator_record_id,
        "identity_state": "candidate_public_account_link" if creator_record_id else "single_platform_observed",
        "discovery_state": "known_account",
        "capture_state": "never_captured",
        "linkage_state": "candidate_needs_review" if creator_record_id else "single_platform_observed",
        "routing_decision": (
            "dedupe_exact_platform_account_then_route_linkage_review_before_cross_platform_use"
            if creator_record_id
            else "dedupe_exact_platform_account_then_attach_new_discovery_evidence"
        ),
        "freshness": {
            "identity_observed_at": account["handle_observed_at"],
            "last_discovery_observed_at_or_none": account["handle_observed_at"],
            "last_capture_observed_at_or_none": None,
            "metrics_freshness_state_or_none": None,
        },
        "lookup_keys": [],
        "source_pointers": [],
        "non_claims": [
            "not current handle guarantee",
            "not final cross-platform identity",
            "not metric authority",
            "not audience authority",
            "not contact or outreach authorization",
        ],
    }


def _refresh_identity_fields(
    *,
    row: dict[str, Any],
    account: Mapping[str, Any],
    account_index: int,
    creator_record_id: str | None,
) -> None:
    account_id = str(account["platform_account_id"])
    platform = str(account["platform"])
    normalized_handle = _normalize_handle(account["public_handle"])
    row.update(
        {
            "platform_account_id": account_id,
            "platform": platform,
            "platform_public_account_id_or_none": account.get("platform_public_account_id_or_none"),
            "public_handle": account["public_handle"],
            "normalized_public_handle": normalized_handle,
            "public_profile_url": account["public_profile_url"],
            "creator_record_id_or_none": creator_record_id,
            "identity_state": "candidate_public_account_link" if creator_record_id else "single_platform_observed",
            "discovery_state": "known_account",
            "linkage_state": "candidate_needs_review" if creator_record_id else "single_platform_observed",
            "routing_decision": (
                "dedupe_exact_platform_account_then_route_linkage_review_before_cross_platform_use"
                if creator_record_id
                else "dedupe_exact_platform_account_then_attach_new_discovery_evidence"
            ),
        }
    )
    row.setdefault("freshness", {})["identity_observed_at"] = account["handle_observed_at"]
    row["lookup_keys"] = _lookup_keys(account)
    identity_pointer = (
        "forseti/product/spines/capture/core/source_families/social_media/creator_registry/"
        "creator_public_handle_linkage_ledger_v0.json#/creator_public_handle_linkage_ledger/"
        f"platform_accounts/{account_index}"
    )
    preserved_sources = [
        pointer
        for pointer in row.get("source_pointers", [])
        if isinstance(pointer, str) and "creator_public_handle_linkage_ledger_v0.json#" not in pointer
    ]
    row["source_pointers"] = [identity_pointer, *preserved_sources]


def _lookup_keys(account: Mapping[str, Any]) -> list[str]:
    platform = str(account["platform"])
    account_id = str(account["platform_account_id"])
    handle = _normalize_handle(account["public_handle"])
    keys = [
        f"platform_account_id:{account_id}",
        f"platform:{platform}:handle:{handle}",
        f"platform:{platform}:url:{str(account['public_profile_url']).lower()}",
    ]
    native_id = _optional_text(account.get("platform_public_account_id_or_none"))
    if native_id:
        keys.insert(1, f"platform:{platform}:public_account_id:{native_id}")
    return keys


def _registry_counts(rows: Sequence[Mapping[str, Any]], creator_records: Sequence[Any]) -> dict[str, Any]:
    by_platform: dict[str, int] = {}
    onboarding_counts = {"not_onboarded": 0, "onboarded": 0}
    for row in rows:
        platform = str(row["platform"])
        by_platform[platform] = by_platform.get(platform, 0) + 1
        state = str(_mapping(row.get("onboarding"), "onboarding").get("onboarding_state"))
        onboarding_counts[state] = onboarding_counts.get(state, 0) + 1
    return {
        "platform_accounts_total": len(rows),
        "creator_records_total": len(creator_records),
        "known_account_rows_total": len(rows),
        "platform_accounts_by_platform": dict(sorted(by_platform.items())),
        "platform_accounts_by_onboarding_state": onboarding_counts,
    }


def _validate_refreshed_registry(
    wrapper: Mapping[str, Any], ledger_accounts: Sequence[Mapping[str, Any]]
) -> None:
    rows = wrapper.get("platform_accounts")
    if not isinstance(rows, list):
        raise CreatorRegistryOnboardingError("registry platform_accounts must be a list")
    row_ids = [str(_mapping(row, "registry row").get("platform_account_id")) for row in rows]
    ledger_ids = [str(_account_mapping(account)["platform_account_id"]) for account in ledger_accounts]
    if row_ids != ledger_ids:
        raise CreatorRegistryOnboardingError(
            "registry platform account order/identity must exactly mirror the linkage ledger"
        )
    for row in rows:
        onboarding = _mapping(row.get("onboarding"), "onboarding")
        state = onboarding.get("onboarding_state")
        evidence_values = (
            onboarding.get("onboarded_at_or_none"),
            onboarding.get("evidence_packet_id_or_none"),
            onboarding.get("evidence_source_family_or_none"),
            onboarding.get("evidence_source_surface_or_none"),
        )
        if state == "onboarded" and not all(isinstance(value, str) and value for value in evidence_values):
            raise CreatorRegistryOnboardingError("onboarded rows require complete evidence fields")
        if state == "not_onboarded" and any(value is not None for value in evidence_values):
            raise CreatorRegistryOnboardingError("not_onboarded rows must not carry evidence fields")
        if state not in {"not_onboarded", "onboarded"}:
            raise CreatorRegistryOnboardingError(f"unsupported onboarding state: {state!r}")


def _account_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    account = _mapping(value, "platform account")
    for field in ("platform_account_id", "platform", "public_handle", "public_profile_url", "handle_observed_at"):
        _required_text(account.get(field), field)
    return account


def _mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise CreatorRegistryOnboardingError(f"{field} must be an object")
    return value


def _required_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CreatorRegistryOnboardingError(f"{field} must be a non-empty string")
    return value.strip()


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise CreatorRegistryOnboardingError("optional text value must be a string or null")
    return value.strip() or None


def _normalize_handle(value: Any) -> str:
    return _required_text(value, "public handle").lstrip("@").lower()


def _latest_timestamp(left: Any, right: Any) -> str | None:
    values = [value for value in (left, right) if isinstance(value, str) and value]
    return max(values) if values else None


__all__ = [
    "CreatorRegistryOnboardingError",
    "EXCLUDED_SURFACES",
    "ONBOARDING_POLICY_VERSION",
    "QUALIFYING_SURFACES",
    "derive_onboarding_by_account",
    "derive_onboarding_snapshot",
    "dump_creator_registry_index",
    "refresh_creator_registry_index_document",
    "sha256_repo_text",
]
