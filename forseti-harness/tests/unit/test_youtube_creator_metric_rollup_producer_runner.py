"""Unit tests for the YouTube creator-metric rollup PRODUCER runner -- the
capture-fed lake-population step (YouTube fold-in / s8 / AR-06) that deposits the
records the snapshot runner's account-anchored discovery consumes.

The core (``run_youtube_producer``) runs against a temp lake from the REAL
committed review-input captures (they are checked into the repo, so CI can drive
the whole capture-fed chain lake-free). There is no real-lake ``main`` test: the
producer is append-only, so running it against the live lake would deposit
durable records -- not something a test may do. ``main``'s only extra surface
over the tested core is ``DataLakeRoot.resolve`` (covered by the lake's own
tests) and ledger loading (covered here).
"""
from __future__ import annotations

import json
from pathlib import Path

from capture_spine.creator_profile_current.silver_metric_reader import (
    discover_creator_metric_rollup_records,
)
from capture_spine.creator_profile_current.silver_subject_ref import (
    platform_account_id_from_subject_ref,
)
from data_lake.root import DataLakeRoot
from runners.run_youtube_creator_metric_rollup_producer import (
    DEFAULT_ACCOUNT_LEDGER,
    _load_account_ledger,
    default_generated_at_utc,
    default_source_files,
    run_youtube_producer,
)


def _account_of(record: dict) -> str:
    return platform_account_id_from_subject_ref(
        record["payload"]["observation"]["subject"]["ref"], what="rollup subject ref"
    )


def _yt_discovery_ledger(*account_ids: str) -> dict:
    return {
        "platform_accounts": [
            {"platform_account_id": a, "platform": "youtube", "public_handle": a}
            for a in account_ids
        ]
    }


def test_run_youtube_producer_appends_discoverable_rollups(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")

    result = run_youtube_producer(
        data_root,
        source_files=default_source_files(),
        account_ledger=_load_account_ledger(DEFAULT_ACCOUNT_LEDGER),
        generated_at_utc=default_generated_at_utc(),
    )

    accounts = sorted({_account_of(r) for r in result.rollup_records})
    assert accounts, "expected at least one covered YouTube account"
    assert len(result.rollup_records) == len(accounts)  # one rollup per account
    assert all(path.is_file() for path in result.rollup_paths)

    # the deposited rollups are exactly what the snapshot runner's account-anchored
    # discovery finds -- one latest rollup per expected account, no availability index.
    found = discover_creator_metric_rollup_records(
        data_root, account_ledger=_yt_discovery_ledger(*accounts)
    )
    assert set(found) == set(accounts)
    assert all(len(records) == 1 for records in found.values())


def test_load_account_ledger_unwraps_committed_shape(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.json"
    ledger.write_text(
        json.dumps(
            {
                "creator_public_handle_linkage_ledger": {
                    "platform_accounts": [{"platform_account_id": "x"}]
                }
            }
        ),
        encoding="utf-8",
    )
    assert _load_account_ledger(ledger) == {"platform_accounts": [{"platform_account_id": "x"}]}
