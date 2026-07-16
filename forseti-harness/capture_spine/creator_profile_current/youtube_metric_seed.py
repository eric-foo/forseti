"""Build the YouTube Shorts fragrance creator metric seed from source files."""

from __future__ import annotations

import hashlib
import json
import statistics
from pathlib import Path, PureWindowsPath
from typing import Any, Iterable, Mapping


YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_WRAPPER = "youtube_shorts_fragrance_creator_metric_seed"
YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_SCHEMA_VERSION = "youtube_shorts_fragrance_creator_metric_seed_v0"
YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_ID = "youtube_shorts_fragrance_creator_metric_seed_v0"
YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_RECIPE_VERSION = "creator_metric_rollup_admitted_youtube_shorts_average_v0"
YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_REGISTRY_VERSION = "creator_metric_seed_youtube_view_count_v0"

_PLATFORM = "youtube"
_REPO_ROOT = Path(__file__).resolve().parents[3]

_CREATOR_OBSERVATION_LEDGER_POINTER = (
    "forseti/product/spines/capture/core/source_families/social_media/youtube/"
    "youtube_shorts_fragrance_creator_observation_ledger_v0.json"
)
_ACCOUNT_LEDGER_POINTER = (
    "forseti/product/spines/capture/core/source_families/social_media/creator_registry/"
    "creator_public_handle_linkage_ledger_v0.json"
)
_REVIEW_INPUT_POINTERS = (
    "docs/review-inputs/youtube_shorts_fragrance_retained_recapture_v0.json",
    "docs/review-inputs/youtube_shorts_fragrance_replacement_capture_v0.json",
    "docs/review-inputs/youtube_shorts_fragrance_tone_expansion30_capture_v0.json",
    "docs/review-inputs/youtube_shorts_fragrance_tone_expansion100_capture_v0.json",
    "docs/review-inputs/youtube_shorts_fragrance_tone_expansion200_capture_v0.json",
)
_LIVE_PROBE_POINTER = "docs/review-inputs/creator_metric_source_live_probe_youtube_v0.json"
_SOURCE_INPUT_ORDER = (
    _CREATOR_OBSERVATION_LEDGER_POINTER,
    _ACCOUNT_LEDGER_POINTER,
    *_REVIEW_INPUT_POINTERS,
    _LIVE_PROBE_POINTER,
)
_SOURCE_INPUT_ROLES = {
    _CREATOR_OBSERVATION_LEDGER_POINTER: (
        "maps admitted video ids to source-backed YouTube creator/channel observations and brand exclusion posture"
    ),
    _ACCOUNT_LEDGER_POINTER: (
        "maps YouTube channel ids to platform_account ids for account-scoped profile subjects"
    ),
    _LIVE_PROBE_POINTER: (
        "bounded live route receipt confirming direct-HTTP watch HTML can expose YouTube view_count for some Shorts; "
        "not used as the 200-row seed source"
    ),
    **{
        pointer: "source-visible YouTube view_count rows for admitted fragrance Shorts"
        for pointer in _REVIEW_INPUT_POINTERS
    },
}


def load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(_resolve_path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON document must be an object: {path}")
    return value


def build_youtube_shorts_fragrance_creator_metric_seed_from_files(
    *,
    source_files: Iterable[str | Path],
    account_ledger: Mapping[str, Any],
    generated_at_utc: str,
) -> dict[str, Any]:
    source_documents = [_source_document(path) for path in source_files]
    if not source_documents:
        raise ValueError("at least one YouTube metric source file is required")

    source_by_pointer = {document["source_pointer"]: document for document in source_documents}
    _add_canonical_context_source_if_present(source_by_pointer, _ACCOUNT_LEDGER_POINTER)
    if _review_inputs_supplied(source_by_pointer):
        _add_canonical_context_source_if_present(source_by_pointer, _LIVE_PROBE_POINTER)

    creator_ledger_document = source_by_pointer.get(_CREATOR_OBSERVATION_LEDGER_POINTER)
    if creator_ledger_document is None:
        raise ValueError("YouTube creator observation ledger source file is required")

    source_rows = _source_metric_rows(source_by_pointer)
    ledger_video_rows = _ledger_video_rows(_unwrap_creator_ledger(creator_ledger_document["document"]))
    if {row["video_id"] for row in source_rows} != set(ledger_video_rows):
        raise ValueError("YouTube source metric rows and creator ledger video ids do not match")

    accounts_by_channel = _youtube_accounts_by_channel(account_ledger)
    observations: list[dict[str, Any]] = []
    exclusions: list[dict[str, Any]] = []
    by_account: dict[str, list[dict[str, Any]]] = {}

    for row in source_rows:
        ledger_video_row = ledger_video_rows[row["video_id"]]
        creator = ledger_video_row["creator"]
        classification = _required_str(creator, "creator_classification")
        if classification == "brand_or_platform_account_observed":
            exclusions.append(_brand_or_platform_exclusion(row=row, ledger_video_row=ledger_video_row))
            continue

        account = accounts_by_channel.get(row["channel_id"])
        if account is None:
            raise ValueError(f"YouTube source channel has no platform account row: {row['channel_id']}")
        observation = _metric_observation(
            row=row,
            account=account,
            ledger_video_row=ledger_video_row,
            sequence=len(observations) + 1,
        )
        observations.append(observation)
        by_account.setdefault(observation["platform_account_id"], []).append(observation)

    rollups = [
        _rollup(
            account=account,
            observations=sorted(by_account[account["platform_account_id"]], key=lambda item: _pool_index(item["source_pool_row_id"])),
            generated_at_utc=generated_at_utc,
            rollup_index=index,
        )
        for index, account in enumerate(
            sorted(
                (account for account in accounts_by_channel.values() if account["platform_account_id"] in by_account),
                key=lambda item: item["platform_account_id"],
            ),
            start=1,
        )
    ]

    seed = {
        "schema_version": YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_SCHEMA_VERSION,
        "seed_id": YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_ID,
        "seed_mode": "source_backed_static_metric_observation_and_rollup_seed",
        "generated_at_utc": generated_at_utc,
        "source_policy_posture": (
            "Static seed generated from checked-in YouTube Shorts fragrance capture artifacts. Rows are "
            "account-scoped view_count observations for admitted Shorts, not channel-wide creator averages, not "
            "engagement-rate support, not cross-platform linkage, not SQLite/runtime storage, and not live dashboard "
            "readiness."
        ),
        "authority_pointers": [
            "forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md",
            "forseti/product/spines/capture/core/source_families/social_media/youtube/youtube_creator_observation_ledger_spec_v0.md",
            "forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_public_handle_linkage_ledger_spec_v0.md",
            "forseti/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md",
        ],
        "source_inputs": _source_inputs(source_by_pointer),
        "source_capture_playbook_posture": {
            "access_classification": "publicly-viewable-but-ToS-restricted",
            "route": (
                "direct-HTTP served YouTube watch/shorts HTML captured in checked-in source artifacts; live "
                "3-video probe recorded separately"
            ),
            "source_native_field_family": "YouTube served HTML / ytInitialPlayerResponse-derived view_count fields preserved by capture artifacts",
            "verdict": "GO for source-visible YouTube view_count observations in the admitted source pool only",
            "partial_or_blocked_fields": [
                "like_count unavailable in the 200-row source artifacts",
                "comment_count unavailable as total platform comments in the 200-row source artifacts",
                "subscriber_count unavailable in the 200-row source artifacts",
                "engagement_rate unavailable because numerator inputs are absent",
            ],
        },
        "selection_policy": {
            "included": (
                "creator_or_channel_observed rows from the YouTube Shorts fragrance creator observation ledger with "
                "source-visible view_count in the checked-in capture artifacts"
            ),
            "excluded": (
                "brand_or_platform_account_observed rows, currently Scentbird, are preserved only as exclusions and "
                "do not enter creator rollups"
            ),
            "rollup_scope": "platform_account only; no creator_record or cross-platform rollups",
            "metric_value_rule": "only observed source-visible numeric view_count values are stored; absent metrics are not zero-filled",
            "representativeness_rule": (
                "Average and median view rollups are directional admitted-pool statistics only. They must carry "
                "sample_support and must not be presented as representative creator or channel averages."
            ),
        },
        "counts": _counts(source_rows=source_rows, observations=observations, rollups=rollups, exclusions=exclusions),
        "metric_observations": observations,
        "metric_rollups": rollups,
        "brand_or_platform_exclusions": exclusions,
        "accepted_residuals": [
            "The rollups are admitted-pool averages, not full-channel creator averages.",
            "View counts can drift after capture; the live probe observed drift and one missing current view field on a three-video sample.",
            "No like_count, total comment_count, subscriber_count, average_like_count, average_comment_count, or engagement_rate is supported by the 200-row checked-in source artifacts.",
            "The current local/external lake does not contain typed metric_observations for these rows; this seed is a static product artifact over checked-in capture records.",
            "Cross-platform rollups remain blocked until public-handle linkage is promoted beyond candidate/rejected states.",
            "Per-account average_views and median_views may be based on as few as one admitted Short; sample_support names thin rows and the values must be treated as directional, not representative creator averages.",
            "The admitted pool is fragrance and transcript-bearing Shorts, so admission-filter selection can bias view averages relative to the creator's full Shorts or channel output.",
            "source_packet_pointer_or_none values are local-only capture-environment drill-back paths; portable provenance comes from source_pointer/source_field/source_file and source_packet_id_or_none.",
        ],
        "non_claims": [
            "not channel-wide creator average",
            "not engagement rate",
            "not subscriber count",
            "not cross-platform identity linkage",
            "not creator_record rollup",
            "not buyer proof",
            "not validation or readiness",
            "not SQLite migration",
            "not data-lake job implementation",
            "not dashboard implementation",
            "not live capture authorization",
            "not contact or outreach authorization",
        ],
        "source_packet_pointer_posture": {
            "source_packet_pointer_or_none": "optional local-only drill-back pointer copied from the capture environment; not portable provenance",
            "portable_provenance_fields": [
                "source_pointer",
                "source_field",
                "source_file",
                "source_packet_id_or_none",
            ],
            "non_claim": "absolute local lake paths are not required to resolve outside the capture host",
        },
    }
    return {YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_SEED_WRAPPER: seed}


def _source_document(path: str | Path) -> dict[str, Any]:
    resolved = _resolve_path(path)
    source_pointer = _source_pointer(resolved)
    return {
        "path": resolved,
        "source_pointer": source_pointer,
        "document": load_json(resolved),
        "sha256": _sha256(resolved),
    }


def _resolve_path(path: str | Path) -> Path:
    value = Path(path)
    if value.is_file():
        return value
    repo_relative = _REPO_ROOT / value
    if repo_relative.is_file():
        return repo_relative
    return value


def _source_pointer(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(_REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _review_inputs_supplied(source_by_pointer: Mapping[str, Mapping[str, Any]]) -> bool:
    return set(_REVIEW_INPUT_POINTERS).issubset(source_by_pointer)


def _add_canonical_context_source_if_present(source_by_pointer: dict[str, dict[str, Any]], pointer: str) -> None:
    if pointer in source_by_pointer:
        return
    path = _REPO_ROOT / pointer
    if path.is_file():
        source_by_pointer[pointer] = _source_document(path)


def _source_inputs(source_by_pointer: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    inputs: list[dict[str, Any]] = []
    for pointer in _SOURCE_INPUT_ORDER:
        source = source_by_pointer.get(pointer)
        if source is None:
            continue
        inputs.append({"source_pointer": pointer, "sha256": source["sha256"], "role": _SOURCE_INPUT_ROLES[pointer]})
    return inputs


def _source_metric_rows(source_by_pointer: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pointer in _REVIEW_INPUT_POINTERS:
        source = source_by_pointer.get(pointer)
        if source is None:
            raise ValueError(f"missing YouTube review-input source file: {pointer}")
        rows.extend(_source_rows_for_document(source))
    return rows


def _source_rows_for_document(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    document = source["document"]
    pointer = source["source_pointer"]
    if "recaptured_rows" in document:
        return [
            _retained_recapture_row(source_pointer=pointer, document=document, row=row, row_index=index)
            for index, row in enumerate(document["recaptured_rows"])
        ]
    if "selected_replacements" in document:
        return [
            _selected_replacement_row(source_pointer=pointer, row=row, row_index=index)
            for index, row in enumerate(document["selected_replacements"])
        ]
    if "attempts" in document:
        return [
            _admitted_attempt_row(source_pointer=pointer, row=row, row_index=index)
            for index, row in enumerate(document["attempts"])
            if row.get("admission_status") == "admitted"
        ]
    raise ValueError(f"unrecognized YouTube metric source file: {pointer}")


def _retained_recapture_row(
    *,
    source_pointer: str,
    document: Mapping[str, Any],
    row: Mapping[str, Any],
    row_index: int,
) -> dict[str, Any]:
    metadata = _required_mapping(row, "metadata")
    packet_id = row.get("caption_packet_id") or row.get("asr_source_packet_id")
    packet_pointer = row.get("caption_packet_path") or row.get("asr_raw_audio_packet_path")
    if row.get("caption_capture_time_utc"):
        observed_at = row.get("caption_capture_time_utc")
        observed_at_source = "caption_capture_time_utc"
    else:
        observed_at = document.get("generated_at_utc")
        observed_at_source = "source_artifact_generated_at_utc"
    return _source_row(
        source_pointer=source_pointer,
        source_field=f"/recaptured_rows/{row_index}/metadata/view_count",
        source_fragment=f"#/recaptured_rows/{row_index}",
        source_row_id=f"source_index:{row['source_index']}",
        video_id=row["video_id"],
        creator_handle_query=row["creator_handle_query"],
        shorts_url=row["shorts_url"],
        watch_url=row["watch_url"],
        metadata=metadata,
        packet_id=packet_id,
        packet_pointer=packet_pointer,
        transcript_route=row.get("transcript_route"),
        observed_at=observed_at,
        observed_at_source=observed_at_source,
    )


def _selected_replacement_row(*, source_pointer: str, row: Mapping[str, Any], row_index: int) -> dict[str, Any]:
    metadata = _required_mapping(row, "metadata")
    return _source_row(
        source_pointer=source_pointer,
        source_field=f"/selected_replacements/{row_index}/metadata/view_count",
        source_fragment=f"#/selected_replacements/{row_index}",
        source_row_id=f"selected_replacement:{row_index}",
        video_id=row["video_id"],
        creator_handle_query=row["creator_handle_query"],
        shorts_url=row["shorts_url"],
        watch_url=row["watch_url"],
        metadata=metadata,
        packet_id=row.get("caption_packet_id"),
        packet_pointer=row.get("caption_packet_path"),
        transcript_route=None,
        observed_at=row.get("caption_capture_time_utc"),
        observed_at_source="caption_capture_time_utc",
    )


def _admitted_attempt_row(*, source_pointer: str, row: Mapping[str, Any], row_index: int) -> dict[str, Any]:
    packet_pointer = _required_mapping(row, "caption_packet_write").get("message")
    packet_id = PureWindowsPath(str(packet_pointer)).name if packet_pointer else None
    metadata = {
        "channel_id": row.get("channel_id"),
        "title": row.get("title"),
        "publish_date": row.get("publish_date"),
        "view_count": row.get("view_count"),
        "watch_html_sha256": row.get("watch_html_sha256"),
        "shorts_html_sha256": row.get("shorts_html_sha256"),
        "watch_byte_size": row.get("watch_byte_size"),
        "shorts_byte_size": row.get("shorts_byte_size"),
    }
    return _source_row(
        source_pointer=source_pointer,
        source_field=f"/attempts/{row_index}/view_count",
        source_fragment=f"#/attempts/{row_index}",
        source_row_id=row["expansion_id"],
        video_id=row["video_id"],
        creator_handle_query=row["handle_query"],
        shorts_url=row["shorts_url"],
        watch_url=row["watch_url"],
        metadata=metadata,
        packet_id=packet_id,
        packet_pointer=packet_pointer,
        transcript_route="youtube_caption_packet" if _required_mapping(row, "caption_fetch").get("found") else None,
        observed_at=row.get("attempted_at_utc"),
        observed_at_source="attempted_at_utc",
    )


def _source_row(
    *,
    source_pointer: str,
    source_field: str,
    source_fragment: str,
    source_row_id: str,
    video_id: str,
    creator_handle_query: str,
    shorts_url: str,
    watch_url: str,
    metadata: Mapping[str, Any],
    packet_id: Any,
    packet_pointer: Any,
    transcript_route: Any,
    observed_at: Any,
    observed_at_source: str,
) -> dict[str, Any]:
    return {
        "video_id": _required_non_empty(video_id, "video_id"),
        "creator_handle_query": _required_non_empty(creator_handle_query, "creator_handle_query"),
        "channel_id": _required_str(metadata, "channel_id"),
        "shorts_url": _required_non_empty(shorts_url, "shorts_url"),
        "watch_url": _required_non_empty(watch_url, "watch_url"),
        "title": metadata.get("title"),
        "publish_date": metadata.get("publish_date"),
        "view_count": _required_int(metadata, "view_count"),
        "source_pointer": f"{source_pointer}{source_fragment}",
        "source_field": source_field,
        "source_file": source_pointer,
        "source_row_id": source_row_id,
        "watch_html_sha256": metadata.get("watch_html_sha256"),
        "shorts_html_sha256": metadata.get("shorts_html_sha256"),
        "watch_byte_size": metadata.get("watch_byte_size"),
        "shorts_byte_size": metadata.get("shorts_byte_size"),
        "packet_id": packet_id,
        "packet_pointer": packet_pointer,
        "transcript_route": transcript_route,
        "observed_at": observed_at,
        "observed_at_source": observed_at_source,
    }


def _unwrap_creator_ledger(document: Mapping[str, Any]) -> Mapping[str, Any]:
    value = document.get("youtube_creator_observation_ledger", document)
    if not isinstance(value, Mapping):
        raise ValueError("YouTube creator observation ledger must be an object")
    return value


def _unwrap_account_ledger(document: Mapping[str, Any]) -> Mapping[str, Any]:
    value = document.get("creator_public_handle_linkage_ledger", document)
    if not isinstance(value, Mapping):
        raise ValueError("account ledger must be an object")
    return value


def _ledger_video_rows(creator_ledger: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    rows = creator_ledger.get("creator_observations")
    if not isinstance(rows, list):
        raise ValueError("YouTube creator observation ledger creator_observations must be a list")
    videos: dict[str, dict[str, Any]] = {}
    for creator in rows:
        if not isinstance(creator, Mapping):
            raise ValueError("YouTube creator observation rows must be objects")
        for pool_id, video_id in zip(creator["pool_ids"], creator["video_ids"], strict=True):
            videos[video_id] = {"pool_id": pool_id, "creator": creator}
    return videos


def ledger_video_retirements(creator_ledger: Mapping[str, Any]) -> dict[str, str]:
    """Operator-attested dead-video retirements from the observation ledger's
    optional ``operator_video_retirements`` block, as a video_id -> reason map.
    Retired videos stay in the compiled pool (the ledger is a compiled fixture;
    removal would desync its reconciled counts and packet refs) -- producers
    exclude them loudly and the batch capture runner skips recapturing them.
    Fails closed on malformed entries or retirements naming videos outside the
    admitted pool, mirroring the builder's unknown-exclusion rule."""
    ledger = _unwrap_creator_ledger(creator_ledger)
    block = ledger.get("operator_video_retirements")
    if block is None:
        return {}
    if not isinstance(block, list):
        raise ValueError("operator_video_retirements must be a list")
    pool = set(_ledger_video_rows(ledger))
    retirements: dict[str, str] = {}
    for entry in block:
        if not isinstance(entry, Mapping):
            raise ValueError("operator_video_retirements entries must be objects")
        video_id = entry.get("video_id")
        reason = entry.get("reason")
        if not isinstance(video_id, str) or not video_id.strip():
            raise ValueError("operator_video_retirements entry lacks a video_id")
        if video_id in retirements:
            raise ValueError(f"duplicate operator_video_retirements entry: {video_id}")
        if video_id not in pool:
            raise ValueError(
                f"operator_video_retirements names a video outside the admitted pool: {video_id}"
            )
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"operator_video_retirements entry for {video_id} lacks a reason")
        retirements[video_id] = reason.strip()
    return retirements


def _youtube_accounts_by_channel(account_ledger: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    ledger = _unwrap_account_ledger(account_ledger)
    accounts = ledger.get("platform_accounts")
    if not isinstance(accounts, list):
        raise ValueError("account ledger platform_accounts must be a list")
    result: dict[str, Mapping[str, Any]] = {}
    for account in accounts:
        if not isinstance(account, Mapping) or account.get("platform") != _PLATFORM:
            continue
        channel_id = account.get("platform_public_account_id_or_none")
        if not isinstance(channel_id, str) or not channel_id.strip():
            raise ValueError("YouTube platform account must carry platform_public_account_id_or_none")
        result[channel_id] = account
    return result


def _metric_observation(
    *,
    row: Mapping[str, Any],
    account: Mapping[str, Any],
    ledger_video_row: Mapping[str, Any],
    sequence: int,
) -> dict[str, Any]:
    creator = ledger_video_row["creator"]
    observed_at_source = row["observed_at_source"]
    return {
        "metric_observation_id": f"yt_fragrance_short_view_obs_v0_{sequence:03d}",
        "platform_account_id": account["platform_account_id"],
        "profile_subject_kind": "platform_account",
        "profile_subject_id": account["platform_account_id"],
        "creator_record_id_or_none": None,
        "youtube_creator_observation_id": creator["creator_observation_id"],
        "platform": _PLATFORM,
        "platform_subject_key_type": "youtube_channel_id",
        "platform_subject_key": creator["platform_subject_key"],
        "creator_handle_query": creator["creator_handle_query"],
        "source_pool_row_id": ledger_video_row["pool_id"],
        "content_id_or_none": row["video_id"],
        "content_url_or_none": row["shorts_url"],
        "watch_url_or_none": row["watch_url"],
        "content_kind": "short",
        "content_title_or_none": row["title"],
        "content_publication_or_event_time_or_none": row["publish_date"],
        "metric_name": "view_count",
        "metric_value_or_none": row["view_count"],
        "metric_unit": "count",
        "metric_posture": "observed",
        "posture_reason_or_none": None,
        "source_pointer": row["source_pointer"],
        "source_field": row["source_field"],
        "source_file": row["source_file"],
        "source_row_id_or_none": row["source_row_id"],
        "source_watch_html_sha256_or_none": row["watch_html_sha256"],
        "source_shorts_html_sha256_or_none": row["shorts_html_sha256"],
        "source_watch_byte_size_or_none": row["watch_byte_size"],
        "source_shorts_byte_size_or_none": row["shorts_byte_size"],
        "source_packet_id_or_none": row["packet_id"],
        "source_packet_pointer_or_none": row["packet_pointer"],
        "transcript_route_or_none": row["transcript_route"],
        "observed_at": row["observed_at"],
        "observed_at_source": observed_at_source,
        "capture_window_start_or_none": None,
        "capture_window_end_or_none": None,
        "metric_registry_version": YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_REGISTRY_VERSION,
        "limitation_notes": _observation_limitations(observed_at_source=observed_at_source),
    }


def _brand_or_platform_exclusion(
    *,
    row: Mapping[str, Any],
    ledger_video_row: Mapping[str, Any],
) -> dict[str, Any]:
    creator = ledger_video_row["creator"]
    return {
        "video_id": row["video_id"],
        "creator_handle_query": creator["creator_handle_query"],
        "platform_subject_key": creator["platform_subject_key"],
        "source_pool_row_id": ledger_video_row["pool_id"],
        "view_count_at_capture": row["view_count"],
        "exclusion_reason": "brand_or_platform_account_observed; not included in creator account metric rollups",
        "source_pointer": row["source_pointer"],
        "source_field": row["source_field"],
    }


def _rollup(
    *,
    account: Mapping[str, Any],
    observations: list[dict[str, Any]],
    generated_at_utc: str,
    rollup_index: int,
) -> dict[str, Any]:
    if not observations:
        raise ValueError(f"no YouTube observations for {account['platform_account_id']}")
    values = [observation["metric_value_or_none"] for observation in observations]
    observation_count = len(observations)
    sample_adequacy = _sample_support_label(observation_count)
    return {
        "metric_rollup_id": f"yt_fragrance_account_view_rollup_v0_{rollup_index:03d}",
        "profile_subject_kind": "platform_account",
        "profile_subject_id": account["platform_account_id"],
        "creator_record_id_or_none": None,
        "platform_scope": _PLATFORM,
        "platform_account_ids": [account["platform_account_id"]],
        "platform_subject_key_type": "youtube_channel_id",
        "platform_subject_key": account["platform_public_account_id_or_none"],
        "public_handle": account["public_handle"],
        "rollup_window": "custom",
        "rollup_window_description": "admitted_fragrance_shorts_pool200_v0; not a full creator-channel window",
        "content_kind_inclusion_rule": "youtube Shorts admitted into the fragrance transcript-bearing source pool only",
        "metric_rollups": {
            "average_views": _observed_metric(round(statistics.mean(values), 2), "count"),
            "median_views": _observed_metric(round(statistics.median(values), 2), "count"),
            "engagement_rate": _unavailable_metric(
                "source rows contain view_count but no like_count/comment_count denominator-compatible engagement inputs",
                "rate",
            ),
            "average_like_count": _unavailable_metric("source rows do not contain source-visible like_count", "count"),
            "average_comment_count": _unavailable_metric(
                "source rows do not contain source-visible total comment_count",
                "count",
            ),
            "posting_cadence": _not_attempted_metric("cadence recipe is out of scope for this metric seed", "rate"),
            "recent_velocity": _not_attempted_metric("velocity recipe is out of scope for this metric seed", "rate"),
        },
        "source_metric_observation_ids": [observation["metric_observation_id"] for observation in observations],
        "observation_count": observation_count,
        "view_count_min": min(values),
        "view_count_max": max(values),
        "calculation_recipe_version": YOUTUBE_SHORTS_FRAGRANCE_CREATOR_METRIC_RECIPE_VERSION,
        "computed_at": generated_at_utc,
        "freshness_state": "partial",
        "limitations": [
            "Rollup covers the admitted fragrance Shorts pool only; it is not a channel-wide average.",
            "View counts are capture-time observations and may have changed since capture.",
            "Engagement rate is unavailable because like/comment/subscriber inputs are absent.",
            "Cross-platform rollups are not authorized without promoted public-handle linkage evidence.",
            (
                f"Average/median views are computed over {observation_count} admitted Shorts; sample adequacy is "
                f"{sample_adequacy} and the value is not a representative creator average."
            ),
            (
                "The admitted pool is fragrance and transcript-bearing, so selection can bias view averages relative "
                "to the creator's full Shorts or channel output."
            ),
        ],
        "sample_support": {
            "observation_count": observation_count,
            "sample_adequacy": sample_adequacy,
            "representativeness_posture": "admitted_pool_only_not_representative_creator_average",
            "surface_handling": _surface_handling(observation_count),
        },
    }


def _counts(
    *,
    source_rows: list[dict[str, Any]],
    observations: list[dict[str, Any]],
    rollups: list[dict[str, Any]],
    exclusions: list[dict[str, Any]],
) -> dict[str, int]:
    return {
        "source_metric_rows_total": len(source_rows),
        "metric_observations_total": len(observations),
        "brand_or_platform_excluded_rows": len(exclusions),
        "unique_video_ids_source": len({row["video_id"] for row in source_rows}),
        "unique_video_ids_observed_creator_rows": len({item["content_id_or_none"] for item in observations}),
        "unique_platform_accounts_with_observations": len({item["platform_account_id"] for item in observations}),
        "metric_rollups_total": len(rollups),
        "engagement_rate_rollups_observed": sum(
            1 for rollup in rollups if rollup["metric_rollups"]["engagement_rate"]["posture"] == "observed"
        ),
    }


def _observation_limitations(*, observed_at_source: str) -> list[str]:
    limitations = [
        "View count is source-visible at capture time and may change after capture.",
        "Observation belongs to the admitted fragrance Shorts pool, not a full channel crawl.",
        "No like_count, comment_count, subscriber_count, or engagement_rate was available from this source row.",
    ]
    if observed_at_source == "source_artifact_generated_at_utc":
        limitations.append(
            "Exact per-row metric observation timestamp was absent; source artifact generated_at_utc is used as fallback observed_at."
        )
    return limitations


def _observed_metric(value: int | float | None, unit: str) -> dict[str, Any]:
    if value is None:
        raise ValueError("observed metric value must not be None")
    return {"value_or_none": value, "posture": "observed", "metric_unit": unit}


def _unavailable_metric(reason: str, unit: str) -> dict[str, Any]:
    return {
        "value_or_none": None,
        "posture": "unavailable_with_reason",
        "posture_reason_or_none": reason,
        "metric_unit": unit,
    }


def _not_attempted_metric(reason: str, unit: str) -> dict[str, Any]:
    return {
        "value_or_none": None,
        "posture": "not_attempted",
        "posture_reason_or_none": reason,
        "metric_unit": unit,
    }


def _sample_support_label(observation_count: int) -> str:
    if observation_count <= 3:
        return "thin_n_1_to_3"
    if observation_count <= 7:
        return "limited_n_4_to_7"
    return "stronger_admitted_pool_n_8_plus"


def _surface_handling(observation_count: int) -> str:
    if observation_count <= 3:
        return "downgrade_or_withhold_summary_claim"
    return "show_only_with_visible_admitted_pool_limitation"


def _pool_index(pool_id: str) -> int:
    return int(pool_id.rsplit("-", 1)[-1])


def _required_mapping(value: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    item = value.get(key)
    if not isinstance(item, Mapping):
        raise ValueError(f"required object missing: {key}")
    return item


def _required_str(value: Mapping[str, Any], key: str) -> str:
    item = value.get(key)
    if not isinstance(item, str) or not item.strip():
        raise ValueError(f"required string missing: {key}")
    return item


def _required_non_empty(value: Any, key: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"required string missing: {key}")
    return value


def _required_int(value: Mapping[str, Any], key: str) -> int:
    item = value.get(key)
    if isinstance(item, bool) or not isinstance(item, int):
        raise ValueError(f"required integer missing: {key}")
    return item
