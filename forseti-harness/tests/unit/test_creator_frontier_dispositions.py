from __future__ import annotations

import hashlib
import json

import pytest

from capture_spine.tiktok_creator_discovery_frontier.models import (
    TikTokCreatorDiscoveryFrontierError,
)
from capture_spine.tiktok_creator_discovery_frontier.register_lake_writer import (
    FRONTIER_DISPOSITION_DERIVED_LANE,
    FRONTIER_DISPOSITION_SCHEMA,
    _normalize_disposition_action,
    _validate_disposition_entry,
    _write_frontier_action_packet,
    load_creator_frontier_dispositions,
    write_creator_frontier_dispositions,
)
from data_lake.canonical_json import canonical_record_bytes
from data_lake.root import DataLakeRoot
from runners.run_creator_registry_lake import main as registry_main


def _eligible(handle: str = "scent.creator") -> dict[str, object]:
    return {
        "platform": "tiktok",
        "handle": handle,
        "status": "eligible",
        "priority": "high",
        "reason_code": "owner_choice",
    }


def test_disposition_replay_is_idempotent_and_change_supersedes_current(tmp_path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first = write_creator_frontier_dispositions(
        data_root=root,
        actions=[_eligible()],
        recorded_at="2026-07-22T01:00:00Z",
    )
    replay = write_creator_frontier_dispositions(
        data_root=root,
        actions=[_eligible()],
        recorded_at="2026-07-22T02:00:00+00:00",
    )
    changed = write_creator_frontier_dispositions(
        data_root=root,
        actions=[
            {
                "platform": "tiktok",
                "handle": "scent.creator",
                "status": "deferred",
                "reason_code": "owner_choice",
                "reconsideration": "new_signal",
            }
        ],
        recorded_at="2026-07-22T03:00:00Z",
    )

    first_row = first["current"]["creator_frontier_disposition_current"]["dispositions"][0]
    current = changed["current"]["creator_frontier_disposition_current"]
    assert replay["status"] == "already_current"
    assert replay["written"] == 0
    assert current["counts"] == {"current": 1, "eligible": 0, "deferred": 1, "rejected": 0}
    assert current["dispositions"][0]["supersedes_record_ids"] == [
        first_row["disposition_id"]
    ]
    assert len(current["history"]) == 2


def test_invalid_batch_fails_before_any_packet_write(tmp_path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")

    with pytest.raises(TikTokCreatorDiscoveryFrontierError, match="priority"):
        write_creator_frontier_dispositions(
            data_root=root,
            actions=[_eligible("valid.first"), {**_eligible("bad.second"), "priority": None}],
            recorded_at="2026-07-22T01:00:00Z",
        )

    assert root.list_committed_packet_ids() == []


def test_multiple_unsuperseded_heads_fail_closed(tmp_path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    write_creator_frontier_dispositions(
        data_root=root,
        actions=[_eligible()],
        recorded_at="2026-07-22T01:00:00Z",
    )
    action = _normalize_disposition_action(
        {**_eligible(), "priority": "super"},
        recorded_at="2026-07-22T02:00:00Z",
    )
    action["supersedes_record_ids"] = []
    action["disposition_id"] = "cfd_" + hashlib.sha256(
        canonical_record_bytes(action)
    ).hexdigest()[:24]
    action = _validate_disposition_entry(action)
    packet_id = _write_frontier_action_packet(
        data_root=root,
        actions=[action],
        recorded_at=action["recorded_at"],
    )
    payload = {
        "schema_version": FRONTIER_DISPOSITION_SCHEMA,
        "raw_anchor": packet_id,
        "recorded_at": action["recorded_at"],
        "dispositions": [action],
    }
    record_id = "cfdb_" + hashlib.sha256(canonical_record_bytes(payload)).hexdigest()[:24]
    root.append_record(
        subtree="derived",
        raw_anchor=packet_id,
        lane=FRONTIER_DISPOSITION_DERIVED_LANE,
        record_id=record_id,
        data=canonical_record_bytes({"record_id": record_id, **payload}),
    )

    with pytest.raises(TikTokCreatorDiscoveryFrontierError, match="multiple unsuperseded"):
        load_creator_frontier_dispositions(root)


def test_registry_cli_writes_and_shows_frontier_state(tmp_path, capsys) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    assert registry_main(
        [
            "frontier-disposition",
            "--data-root",
            str(root.path),
            "--handle",
            "Scent.Creator",
            "--status",
            "eligible",
            "--priority",
            "normal",
            "--reason-code",
            "owner_choice",
            "--recorded-at",
            "2026-07-22T01:00:00Z",
        ]
    ) == 0
    capsys.readouterr()

    assert registry_main(["frontier-show", "--data-root", str(root.path)]) == 0
    shown = json.loads(capsys.readouterr().out)
    row = shown["creator_frontier_disposition_current"]["dispositions"][0]
    assert row["candidate_key"] == "tiktok:@scent.creator"
    assert row["status"] == "eligible"
