"""Advisory selection helpers for TikTok creator discovery frontier registers.

These helpers are intentionally pure: they read already-built register mappings
and return ranking/overlap views. They do not launch TikTok, write packets,
mutate registers, authorize next runs, or infer creator quality.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


_WRAPPER_KEY = "tiktok_creator_discovery_frontier_register"
_CANDIDATE_NODE_TYPE = "tiktok_creator_candidate"
_SUGGESTED_EDGE_TYPE = "platform_suggested_account_relation"
_EXPANDED_SECTION_MARKERS = ("view_all", "expanded")
_FRAGRANCE_TOKENS = (
    "frag",
    "fragrance",
    "scent",
    "cologne",
    "parfum",
    "perfume",
    "smell",
    "sniff",
    "nose",
    "oud",
)


def rank_tiktok_creator_discovery_targets(
    registers: Sequence[Mapping[str, Any]],
    *,
    already_scanned_handles: Sequence[str] = (),
    exclude_root_seed_handles: bool = True,
) -> list[dict[str, Any]]:
    """Return an advisory next-target ranking from existing frontier registers.

    The rank is built from weak suggested-account edges only. It intentionally
    favors once-only, expanded-surface, fragrance-like candidates and
    deprioritizes repeated hubs. It is not a capture authorization, registry
    decision, metric, or creator-quality score.
    """
    records, root_handle_keys = _collect_candidate_records(registers)
    excluded = {_handle_key(handle) for handle in already_scanned_handles}
    excluded.discard(None)
    if exclude_root_seed_handles:
        excluded.update(root_handle_keys)

    ranked: list[dict[str, Any]] = []
    for handle_key, record in records.items():
        if handle_key in excluded:
            continue
        frequency = len(record["observed_from_root_keys"])
        expanded = _has_expanded_section(record["observed_sections"])
        fragrance_like = _is_fragrance_like(record["handle"], record["display_name_or_none"])
        tier = _recommendation_tier(frequency, expanded, fragrance_like)
        score = _score_candidate(frequency, expanded, fragrance_like)
        ranked.append(
            {
                "handle": record["handle"],
                "display_name_or_none": record["display_name_or_none"],
                "source_url_or_locator": record["source_url_or_locator"],
                "prior_suggested_frequency": frequency,
                "observed_from_roots": sorted(record["observed_from_roots"]),
                "observed_sections": sorted(record["observed_sections"]),
                "is_once_only": frequency == 1,
                "is_expanded_tail_observed": expanded,
                "fragrance_handle_or_name_match": fragrance_like,
                "score": score,
                "recommendation_tier": tier,
                "selection_rationale": _selection_rationale(
                    frequency=frequency,
                    expanded=expanded,
                    fragrance_like=fragrance_like,
                ),
            }
        )

    ranked.sort(
        key=lambda item: (
            _tier_sort_key(str(item["recommendation_tier"])),
            -int(item["score"]),
            int(item["prior_suggested_frequency"]),
            str(item["handle"]).lower(),
        )
    )
    return ranked


def summarize_tiktok_creator_discovery_overlap(
    *,
    prior_registers: Sequence[Mapping[str, Any]],
    current_register: Mapping[str, Any],
) -> dict[str, Any]:
    """Summarize how a new register overlaps with prior frontier registers."""
    prior_records, _ = _collect_candidate_records(prior_registers)
    current_records, _ = _collect_candidate_records((current_register,))

    repeated_prior_2plus: list[str] = []
    prior_once_now_repeated: list[str] = []
    brand_new_tail: list[str] = []
    seen_before = 0

    for handle_key, record in current_records.items():
        prior = prior_records.get(handle_key)
        handle = record["handle"]
        if prior is None:
            brand_new_tail.append(handle)
            continue
        seen_before += 1
        prior_frequency = len(prior["observed_from_root_keys"])
        if prior_frequency >= 2:
            repeated_prior_2plus.append(handle)
        elif prior_frequency == 1:
            prior_once_now_repeated.append(handle)

    current_count = len(current_records)
    return {
        "current_root_handle": _current_root_handle(current_register),
        "current_candidate_count": current_count,
        "seen_before_count": seen_before,
        "not_seen_before_count": current_count - seen_before,
        "repeated_prior_2plus": sorted(repeated_prior_2plus, key=str.lower),
        "prior_once_now_repeated": sorted(prior_once_now_repeated, key=str.lower),
        "brand_new_tail": sorted(brand_new_tail, key=str.lower),
        "non_claims": [
            "overlap summary is not creator quality",
            "overlap summary is not capture authorization",
            "overlap summary is not registry identity proof",
        ],
    }


def _collect_candidate_records(
    registers: Sequence[Mapping[str, Any]]
) -> tuple[dict[str, dict[str, Any]], set[str]]:
    records: dict[str, dict[str, Any]] = {}
    root_handle_keys: set[str] = set()

    for register in registers:
        wrapper = _register_wrapper(register)
        root_handle = _clean_handle(_mapping_value(wrapper, "root_seed").get("handle"))
        root_handle_key = _handle_key(root_handle)
        if root_handle_key:
            root_handle_keys.add(root_handle_key)

        nodes = _sequence_value(wrapper, "nodes")
        edges = _sequence_value(wrapper, "edges")
        node_by_id = {
            str(node["node_id"]): node
            for node in nodes
            if isinstance(node, Mapping) and isinstance(node.get("node_id"), str)
        }
        candidates_by_id = {
            node_id: node
            for node_id, node in node_by_id.items()
            if node.get("node_type") == _CANDIDATE_NODE_TYPE
            and _handle_key(node.get("handle_or_none"))
        }
        observed_via_suggested_edge: set[str] = set()

        for edge in edges:
            if not isinstance(edge, Mapping) or edge.get("edge_type") != _SUGGESTED_EDGE_TYPE:
                continue
            candidate = candidates_by_id.get(str(edge.get("to_node_id")))
            if candidate is None:
                continue
            from_node = node_by_id.get(str(edge.get("from_node_id")), {})
            observed_root = _clean_handle(from_node.get("handle_or_none")) or root_handle
            sections = _string_values(edge.get("observed_sections"))
            handle_key = _upsert_candidate_record(records, candidate, observed_root, sections)
            if handle_key:
                observed_via_suggested_edge.add(handle_key)

        for candidate in candidates_by_id.values():
            handle_key = _handle_key(candidate.get("handle_or_none"))
            if handle_key and handle_key not in observed_via_suggested_edge:
                _upsert_candidate_record(records, candidate, root_handle, ())

    return records, root_handle_keys


def _upsert_candidate_record(
    records: dict[str, dict[str, Any]],
    candidate: Mapping[str, Any],
    observed_root: str | None,
    sections: Sequence[str],
) -> str | None:
    handle = _clean_handle(candidate.get("handle_or_none"))
    handle_key = _handle_key(handle)
    if not handle or not handle_key:
        return None

    record = records.setdefault(
        handle_key,
        {
            "handle": handle,
            "display_name_or_none": _optional_text(candidate.get("display_name_or_none")),
            "source_url_or_locator": _optional_text(candidate.get("source_url_or_locator")),
            "observed_from_roots": set(),
            "observed_from_root_keys": set(),
            "observed_sections": set(),
        },
    )
    if record["display_name_or_none"] is None:
        record["display_name_or_none"] = _optional_text(candidate.get("display_name_or_none"))
    if record["source_url_or_locator"] is None:
        record["source_url_or_locator"] = _optional_text(candidate.get("source_url_or_locator"))

    root_key = _handle_key(observed_root)
    if observed_root and root_key:
        record["observed_from_roots"].add(observed_root)
        record["observed_from_root_keys"].add(root_key)
    record["observed_sections"].update(sections)
    return handle_key


def _register_wrapper(register: Mapping[str, Any]) -> Mapping[str, Any]:
    wrapper = register.get(_WRAPPER_KEY)
    if isinstance(wrapper, Mapping):
        return wrapper
    if isinstance(register.get("nodes"), Sequence) and isinstance(register.get("edges"), Sequence):
        return register
    raise ValueError(f"{_WRAPPER_KEY} wrapper is required")


def _mapping_value(value: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    item = value.get(key)
    if not isinstance(item, Mapping):
        raise ValueError(f"{key} must be a mapping")
    return item


def _sequence_value(value: Mapping[str, Any], key: str) -> Sequence[Any]:
    item = value.get(key)
    if not isinstance(item, Sequence) or isinstance(item, (str, bytes, bytearray)):
        raise ValueError(f"{key} must be a sequence")
    return item


def _current_root_handle(register: Mapping[str, Any]) -> str | None:
    wrapper = _register_wrapper(register)
    return _clean_handle(_mapping_value(wrapper, "root_seed").get("handle"))


def _has_expanded_section(sections: set[str]) -> bool:
    lowered = [section.lower() for section in sections]
    return any(marker in section for marker in _EXPANDED_SECTION_MARKERS for section in lowered)


def _is_fragrance_like(handle: str, display_name: str | None) -> bool:
    haystack = f"{handle} {display_name or ''}".lower()
    return any(token in haystack for token in _FRAGRANCE_TOKENS)


def _recommendation_tier(frequency: int, expanded: bool, fragrance_like: bool) -> str:
    if frequency >= 3:
        return "deprioritize_repeated_hub"
    if frequency == 1 and (expanded or fragrance_like):
        return "prioritize"
    return "consider"


def _score_candidate(frequency: int, expanded: bool, fragrance_like: bool) -> int:
    if frequency <= 0:
        score = 0
    elif frequency == 1:
        score = 40
    elif frequency == 2:
        score = 15
    else:
        score = -25 - ((frequency - 3) * 5)
    if expanded:
        score += 20
    if fragrance_like:
        score += 15
    return score


def _selection_rationale(*, frequency: int, expanded: bool, fragrance_like: bool) -> str:
    reasons: list[str] = []
    if frequency == 1:
        reasons.append("seen from one scanned root, reducing duplicate graphing")
    elif frequency >= 3:
        reasons.append(f"seen from {frequency} scanned roots, so it may be a repeated hub")
    else:
        reasons.append(f"seen from {frequency} scanned roots")
    if expanded:
        reasons.append("observed on an expanded suggested surface")
    if fragrance_like:
        reasons.append("handle or display name contains a fragrance token")
    return "; ".join(reasons)


def _tier_sort_key(tier: str) -> int:
    order = {
        "prioritize": 0,
        "consider": 1,
        "deprioritize_repeated_hub": 2,
    }
    return order.get(tier, 3)


def _clean_handle(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    handle = value.strip().lstrip("@").strip()
    return handle or None


def _handle_key(value: Any) -> str | None:
    handle = _clean_handle(value)
    return handle.lower() if handle else None


def _optional_text(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    text = value.strip()
    return text or None


def _string_values(value: Any) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        return ()
    return tuple(str(item) for item in value if str(item).strip())
