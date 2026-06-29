"""Build an Instagram creator metric seed from IG reels-grid projections."""

from __future__ import annotations

import hashlib
import json
import statistics
from pathlib import Path
from typing import Any, Iterable, Mapping


INSTAGRAM_REELS_CREATOR_METRIC_SEED_WRAPPER = "instagram_reels_creator_metric_seed"
INSTAGRAM_REELS_CREATOR_METRIC_SEED_SCHEMA_VERSION = "instagram_reels_creator_metric_seed_v0"
INSTAGRAM_REELS_CREATOR_METRIC_SEED_ID = "instagram_reels_creator_metric_seed_v0"
INSTAGRAM_REELS_CREATOR_METRIC_RECIPE_VERSION = "creator_metric_rollup_instagram_reels_grid_engagement_v0"
INSTAGRAM_REELS_CREATOR_METRIC_REGISTRY_VERSION = "creator_metric_seed_instagram_reels_grid_v0"

_PLATFORM = "instagram"
_METRIC_ORDER = ("view_count", "like_count", "comment_count")


def load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON document must be an object: {path}")
    return value


def build_instagram_reels_creator_metric_seed_from_files(
    *,
    projection_paths: Iterable[str | Path],
    account_ledger: Mapping[str, Any],
    generated_at_utc: str,
) -> dict[str, Any]:
    projections = [_projection_summary(Path(path)) for path in projection_paths]
    if not projections:
        raise ValueError("at least one IG reels projection file is required")

    selected = _select_projection_per_username(projections)
    accounts_by_handle = _instagram_accounts_by_handle(account_ledger)

    observations: list[dict[str, Any]] = []
    rollups: list[dict[str, Any]] = []
    source_inputs: list[dict[str, Any]] = []
    sequence = 1

    for selected_projection in sorted(selected, key=lambda item: item["username"]):
        username = selected_projection["username"]
        account = accounts_by_handle.get(username.casefold())
        if account is None:
            raise ValueError(f"IG projection username has no platform account row: {username}")

        source_pointer = str(selected_projection["path"])
        source_inputs.append(
            {
                "source_pointer": source_pointer,
                "sha256": selected_projection["sha256"],
                "role": f"source-surface-preserving IG reels-grid projection for @{username}",
            }
        )

        observation_start = len(observations)
        for row_index, row in enumerate(selected_projection["rows"]):
            observation = _metric_observation(
                account=account,
                row=row,
                row_index=row_index,
                source_pointer=source_pointer,
                source_packet_pointer=_source_packet_pointer(selected_projection["path"], selected_projection["packet_id"]),
                sequence=sequence,
            )
            observations.append(observation)
            sequence += 1

        account_observations = observations[observation_start:]
        rollups.append(
            _rollup(
                account=account,
                observations=account_observations,
                selected_projection=selected_projection,
                generated_at_utc=generated_at_utc,
                rollup_index=len(rollups) + 1,
            )
        )

    seed = {
        "schema_version": INSTAGRAM_REELS_CREATOR_METRIC_SEED_SCHEMA_VERSION,
        "seed_id": INSTAGRAM_REELS_CREATOR_METRIC_SEED_ID,
        "seed_mode": "source_backed_static_metric_observation_and_rollup_seed",
        "generated_at_utc": generated_at_utc,
        "source_policy_posture": (
            "Static seed generated from IG reels-grid projection artifacts. Rows are "
            "account-scoped public Instagram metric observations for selected grid "
            "reels/profile facts, not full-account history, not cross-platform linkage, "
            "not SQLite/runtime storage, and not dashboard readiness."
        ),
        "authority_pointers": [
            "orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_spec_v0.md",
            "orca/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md",
            "orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_spec_v0.md",
            "orca/product/spines/creator_signal/creator_intelligence_profile_surface_v0.md",
        ],
        "source_inputs": source_inputs,
        "source_capture_playbook_posture": {
            "access_classification": "publicly-viewable-but-platform-restricted",
            "route": "IG reels-grid Source Capture Packet projected into source-surface-preserving metric rows",
            "source_native_field_family": "IG web profile and clips/user passive JSON plus DOM grid engagement text",
            "verdict": "GO for source-visible Instagram reels-grid metric observations in admitted projection files only",
            "partial_or_blocked_fields": [
                "Only visible grid reels from selected projections enter rollups.",
                "Follower count is preserved as a profile metric observation but is not surfaced as a profile-current rollup metric.",
                "No cross-platform identity linkage is inferred from matching handles.",
            ],
        },
        "selection_policy": {
            "included": "latest usable IG reels-grid projection per username from the supplied projection files",
            "projection_dedupe_rule": (
                "group by projection username; choose the projection with the most observed metric rows, "
                "then the latest capture_time, then lexical path as deterministic tie-break"
            ),
            "rollup_scope": "platform_account only; no creator_record or cross-platform rollups",
            "metric_value_rule": "only observed source-visible numeric values enter numeric aggregations; absent metrics are not zero-filled",
            "engagement_rate_recipe": "(sum(like_count) + sum(comment_count)) / sum(view_count) over complete reel rows",
            "representativeness_rule": (
                "Average and median view rollups are directional selected-grid statistics only. "
                "They must carry sample_support and must not be presented as representative creator or account averages."
            ),
        },
        "counts": _counts(observations, rollups, selected, projections),
        "metric_observations": observations,
        "metric_rollups": rollups,
        "source_packet_pointer_posture": {
            "source_packet_pointer_or_none": "optional local-only drill-back pointer copied from the capture environment; not portable provenance",
            "portable_provenance_fields": [
                "source_pointer",
                "source_field",
                "source_file",
                "source_packet_id_or_none",
                "raw_anchor",
            ],
            "non_claim": "absolute local lake paths are not required to resolve outside the capture host",
        },
        "accepted_residuals": [
            "The seed uses selected IG reels-grid projections, not a full account crawl.",
            "Projection-file paths are local lake drill-back pointers and may not resolve outside the capture host.",
            "Follower_count is preserved as a source-backed observation but is not yet a profile-current rollup metric.",
            "Matching public handles across platforms remain unlinked until public-handle linkage evidence is human reviewed.",
        ],
        "non_claims": [
            "not full-account creator average",
            "not cross-platform identity linkage",
            "not public person-level identity",
            "not buyer proof",
            "not contact or outreach authorization",
            "not follower or audience graph",
            "not SQLite migration",
            "not dashboard readiness",
        ],
    }
    return {INSTAGRAM_REELS_CREATOR_METRIC_SEED_WRAPPER: seed}


def dump_instagram_reels_creator_metric_seed(document: Mapping[str, Any]) -> str:
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"


def _projection_summary(path: Path) -> dict[str, Any]:
    document = load_json(path)
    rows = document.get("rows")
    if not isinstance(rows, list):
        raise ValueError(f"IG projection rows must be a list: {path}")
    username = next((row.get("username") for row in rows if isinstance(row, Mapping) and row.get("username")), None)
    if not isinstance(username, str) or not username.strip():
        raise ValueError(f"IG projection has no username: {path}")
    packet_id = document.get("packet_id")
    if not isinstance(packet_id, str) or not packet_id.strip():
        raise ValueError(f"IG projection has no packet_id: {path}")
    capture_times = [row.get("capture_time") for row in rows if isinstance(row, Mapping) and row.get("capture_time")]
    observed_count = sum(1 for row in rows if isinstance(row, Mapping) and row.get("posture") == "observed")
    return {
        "path": path,
        "document": document,
        "rows": rows,
        "username": username.strip(),
        "packet_id": packet_id,
        "capture_time": max(str(value) for value in capture_times) if capture_times else "",
        "observed_count": observed_count,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def _select_projection_per_username(projections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_username: dict[str, list[dict[str, Any]]] = {}
    for projection in projections:
        by_username.setdefault(str(projection["username"]).casefold(), []).append(projection)

    selected: list[dict[str, Any]] = []
    for candidates in by_username.values():
        selected.append(
            max(
                candidates,
                key=lambda item: (
                    int(item["observed_count"]),
                    str(item["capture_time"]),
                    str(item["path"]),
                ),
            )
        )
    return selected


def _instagram_accounts_by_handle(account_ledger: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    accounts = account_ledger.get("platform_accounts")
    if not isinstance(accounts, list):
        raise ValueError("account ledger platform_accounts must be a list")
    result: dict[str, Mapping[str, Any]] = {}
    for account in accounts:
        if not isinstance(account, Mapping) or account.get("platform") != _PLATFORM:
            continue
        handle = account.get("public_handle")
        if not isinstance(handle, str) or not handle.strip():
            raise ValueError("Instagram platform account must carry public_handle")
        result[handle.casefold()] = account
    return result


def _metric_observation(
    *,
    account: Mapping[str, Any],
    row: Mapping[str, Any],
    row_index: int,
    source_pointer: str,
    source_packet_pointer: str | None,
    sequence: int,
) -> dict[str, Any]:
    metric = _required_str(row, "metric")
    posture = _required_str(row, "posture")
    observed = posture == "observed"
    value = row.get("value")
    if observed and (isinstance(value, bool) or not isinstance(value, int)):
        raise ValueError(f"observed IG projection metric requires int value at rows/{row_index}")
    content_kind = _required_str(row, "content_kind")
    row_id = _required_str(row, "row_id")
    raw_ref = row.get("raw_ref") if isinstance(row.get("raw_ref"), Mapping) else {}
    raw_anchor = row.get("raw_anchor") if isinstance(row.get("raw_anchor"), Mapping) else {}
    coverage_window = row.get("coverage_window") if isinstance(row.get("coverage_window"), Mapping) else {}
    source_field = f"/rows/{row_index}/value" if observed else f"/rows/{row_index}/reason"

    return {
        "metric_observation_id": f"ig_reels_metric_obs_v0_{sequence:03d}",
        "platform_account_id": account["platform_account_id"],
        "profile_subject_kind": "platform_account",
        "profile_subject_id": account["platform_account_id"],
        "creator_record_id_or_none": None,
        "platform": _PLATFORM,
        "platform_subject_key_type": "instagram_public_handle",
        "platform_subject_key": account["public_handle"],
        "creator_handle_query": account["public_handle"],
        "source_projection_row_id": row_id,
        "content_id_or_none": row.get("content_shortcode"),
        "content_url_or_none": row.get("content_url"),
        "content_kind": content_kind,
        "metric_name": metric,
        "metric_value_or_none": value if observed else None,
        "metric_unit": "count",
        "metric_posture": posture,
        "posture_reason_or_none": None if observed else row.get("reason"),
        "source_pointer": f"{source_pointer}#/rows/{row_index}",
        "source_field": source_field,
        "source_file": source_pointer,
        "source_row_id_or_none": row_id,
        "source_packet_id_or_none": raw_ref.get("packet_id"),
        "source_packet_pointer_or_none": source_packet_pointer,
        "raw_anchor": raw_anchor,
        "chosen_source_surface_or_none": row.get("chosen_source_surface"),
        "source_surface_count_candidates": row.get("source_surface_count_candidates", []),
        "observed_at": row.get("capture_time"),
        "observed_at_source": "ig_reels_grid_projection.row.capture_time",
        "capture_window_start_or_none": coverage_window.get("start"),
        "capture_window_end_or_none": coverage_window.get("end"),
        "source_publication_or_event_time_or_none": row.get("source_publication_or_event"),
        "metric_registry_version": INSTAGRAM_REELS_CREATOR_METRIC_REGISTRY_VERSION,
        "limitation_notes": _observation_limitations(metric=metric, content_kind=content_kind),
    }


def _rollup(
    *,
    account: Mapping[str, Any],
    observations: list[dict[str, Any]],
    selected_projection: Mapping[str, Any],
    generated_at_utc: str,
    rollup_index: int,
) -> dict[str, Any]:
    complete_reels = _complete_reel_metrics(observations)
    if not complete_reels:
        raise ValueError(f"no complete IG reel metric rows for {account['platform_account_id']}")

    views = [item["view_count"]["metric_value_or_none"] for item in complete_reels]
    likes = [item["like_count"]["metric_value_or_none"] for item in complete_reels]
    comments = [item["comment_count"]["metric_value_or_none"] for item in complete_reels]
    denominator = sum(views)
    engagement_rate = round((sum(likes) + sum(comments)) / denominator, 6) if denominator > 0 else None
    source_ids = [
        item[metric]["metric_observation_id"]
        for item in complete_reels
        for metric in _METRIC_ORDER
    ]
    observation_count = len(source_ids)

    return {
        "metric_rollup_id": f"ig_reels_account_engagement_rollup_v0_{rollup_index:03d}",
        "profile_subject_kind": "platform_account",
        "profile_subject_id": account["platform_account_id"],
        "creator_record_id_or_none": None,
        "platform_scope": _PLATFORM,
        "platform_account_ids": [account["platform_account_id"]],
        "rollup_window": "custom",
        "rollup_window_description": "selected_latest_ig_reels_grid_projection_v0; not a full-account history window",
        "content_kind_inclusion_rule": "Instagram Reels from the selected /reels/ grid projection only; static posts and profile follower_count are excluded from rollup math",
        "metric_rollups": {
            "average_views": _observed_metric(round(statistics.mean(views), 2), "count"),
            "median_views": _observed_metric(round(statistics.median(views), 2), "count"),
            "engagement_rate": (
                _observed_metric(engagement_rate, "rate")
                if engagement_rate is not None
                else _unavailable_metric("view_count denominator was zero or unavailable", "rate")
            ),
            "average_like_count": _observed_metric(round(statistics.mean(likes), 2), "count"),
            "average_comment_count": _observed_metric(round(statistics.mean(comments), 2), "count"),
            "posting_cadence": _not_attempted_metric("cadence recipe is out of scope for this IG metric seed", "rate"),
            "recent_velocity": _not_attempted_metric("velocity recipe is out of scope for this IG metric seed", "rate"),
        },
        "source_metric_observation_ids": source_ids,
        "observation_count": observation_count,
        "view_count_min": min(views),
        "view_count_max": max(views),
        "calculation_recipe_version": INSTAGRAM_REELS_CREATOR_METRIC_RECIPE_VERSION,
        "computed_at": generated_at_utc,
        "freshness_state": "partial",
        "limitations": _rollup_limitations(
            reel_count=len(complete_reels),
            observation_count=observation_count,
            username=str(selected_projection["username"]),
        ),
        "sample_support": {
            "observation_count": observation_count,
            "sample_adequacy": _sample_support_label(observation_count),
            "representativeness_posture": "admitted_pool_only_not_representative_creator_average",
            "surface_handling": _surface_handling(observation_count),
        },
    }


def _complete_reel_metrics(observations: list[dict[str, Any]]) -> list[dict[str, dict[str, Any]]]:
    by_content: dict[str, dict[str, dict[str, Any]]] = {}
    order: list[str] = []
    for observation in observations:
        if observation["content_kind"] != "reel" or observation["metric_name"] not in _METRIC_ORDER:
            continue
        if observation["metric_posture"] != "observed":
            continue
        content_id = observation.get("content_id_or_none")
        if not isinstance(content_id, str) or not content_id.strip():
            continue
        if content_id not in by_content:
            by_content[content_id] = {}
            order.append(content_id)
        by_content[content_id][observation["metric_name"]] = observation
    return [
        by_content[content_id]
        for content_id in order
        if all(metric in by_content[content_id] for metric in _METRIC_ORDER)
    ]


def _counts(
    observations: list[dict[str, Any]],
    rollups: list[dict[str, Any]],
    selected: list[dict[str, Any]],
    projections: list[dict[str, Any]],
) -> dict[str, int]:
    content_ids = {
        observation["content_id_or_none"]
        for observation in observations
        if observation.get("content_id_or_none")
    }
    return {
        "source_projection_files_supplied": len(projections),
        "source_projection_files_selected": len(selected),
        "metric_observations_total": len(observations),
        "content_metric_observations_total": sum(1 for item in observations if item["content_kind"] == "reel"),
        "profile_metric_observations_total": sum(1 for item in observations if item["content_kind"] == "profile"),
        "unique_content_items_observed": len(content_ids),
        "unique_platform_accounts_with_observations": len({item["platform_account_id"] for item in observations}),
        "metric_rollups_total": len(rollups),
        "engagement_rate_rollups_observed": sum(
            1 for rollup in rollups if rollup["metric_rollups"]["engagement_rate"]["posture"] == "observed"
        ),
    }


def _source_packet_pointer(path: Path, packet_id: str) -> str | None:
    parts = path.parts
    if "derived" not in parts:
        return None
    derived_index = parts.index("derived")
    root = Path(*parts[:derived_index])
    return str(root / "raw" / packet_id)


def _observation_limitations(*, metric: str, content_kind: str) -> list[str]:
    limitations = [
        "Metric is source-visible at capture time and may change after capture.",
        "Observation belongs to a selected IG reels-grid projection, not a full account crawl.",
    ]
    if metric == "follower_count":
        limitations.append("Follower_count is preserved as a profile metric observation but is not a follower graph or audience estimate.")
    if content_kind == "reel":
        limitations.append("Grid selection can bias averages relative to the creator's full Instagram output.")
    return limitations


def _rollup_limitations(*, reel_count: int, observation_count: int, username: str) -> list[str]:
    adequacy = _sample_support_label(observation_count)
    return [
        "Rollup covers selected Instagram Reels grid rows only; it is not a full-account average.",
        "View, like, and comment counts are capture-time observations and may have changed since capture.",
        "Cross-platform rollups are not authorized without promoted public-handle linkage evidence.",
        (
            f"Average/median views are computed over {reel_count} selected reels and "
            f"{observation_count} metric observations for @{username}; sample adequacy is {adequacy} "
            "and the value is not a representative creator average."
        ),
        "The selected IG reels grid selection can bias view averages relative to the creator's full Instagram output.",
        "Engagement rate is computed only from source-backed selected-grid view, like, and comment counts.",
        "Profile follower_count is not included in rollup math.",
    ]


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


def _required_str(value: Mapping[str, Any], key: str) -> str:
    item = value.get(key)
    if not isinstance(item, str) or not item.strip():
        raise ValueError(f"required string missing: {key}")
    return item
