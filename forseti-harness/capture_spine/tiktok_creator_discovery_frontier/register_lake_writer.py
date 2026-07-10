"""Lake persistence for validated TikTok Creator Discovery Frontier registers.

Kept as a sibling of the pure builder so `register_writer` stays network- and
lake-free. The register is appended as a derived record keyed to the raw
parent-grid packet it was built from, per the data-lake derived-layout rule
(derived records are append-only and anchored to committed raw truth).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from capture_spine.tiktok_creator_discovery_frontier.models import (
    TikTokCreatorDiscoveryFrontierError,
)
from capture_spine.tiktok_creator_discovery_frontier.validation import (
    validate_tiktok_creator_discovery_frontier_register,
)

FRONTIER_REGISTER_DERIVED_LANE = "tiktok_creator_discovery_frontier"


def write_tiktok_creator_discovery_frontier_register(
    register: Mapping[str, Any],
    data_root: Any,
    *,
    record_id: str,
) -> Path:
    """Append a validated frontier register to the lake and return its path.

    ``data_root`` is a resolved ``DataLakeRoot``; the raw anchor is the
    register's parent-grid packet id, so a register built without a committed
    parent-grid packet cannot be lake-written (fail-closed -- use an explicit
    local ``--output`` escape instead).
    """
    validate_tiktok_creator_discovery_frontier_register(register)
    wrapper = register["tiktok_creator_discovery_frontier_register"]
    raw_anchor = wrapper["provenance"].get("parent_grid_packet_id_or_none")
    if not raw_anchor:
        raise TikTokCreatorDiscoveryFrontierError(
            "missing_parent_grid_packet_anchor",
            "lake write requires provenance.parent_grid_packet_id_or_none; a "
            "register without a committed parent-grid packet has no raw anchor",
        )
    body = json.dumps(register, indent=2, sort_keys=True) + "\n"
    return data_root.append_record(
        subtree="derived",
        raw_anchor=str(raw_anchor),
        lane=FRONTIER_REGISTER_DERIVED_LANE,
        record_id=record_id,
        data=body.encode("utf-8"),
    )
