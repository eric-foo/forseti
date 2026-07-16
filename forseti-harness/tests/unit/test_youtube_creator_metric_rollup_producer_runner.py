"""YouTube creator-metric runner support and historical read-side fixtures.

The historical test writes explicitly synthetic pre-contract record bytes
directly into a temp lake. It proves audit classification only; it does not
exercise or bypass the authoritative production append route.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from capture_spine.creator_profile_current.youtube_silver_metric_producer import (
    DEFAULT_YOUTUBE_SEED_PATH,
    YOUTUBE_SEED_WRAPPER_KEY,
)
from capture_spine.creator_profile_current.silver_metric_reader import (
    CreatorRollupDiscoveryError,
    discover_creator_metric_rollup_records,
)
from capture_spine.creator_profile_current.silver_subject_ref import (
    platform_account_id_from_subject_ref,
)
from data_lake.creator_metric_lineage import (
    AUDIT_COMPATIBLE,
)
from data_lake.root import EPOCH_MARKER_FILENAME, DataLakeRoot, raw_shard
from runners.run_youtube_creator_metric_rollup_producer import (
    DEFAULT_ACCOUNT_LEDGER,
    _load_account_ledger,
    default_generated_at_utc,
    default_source_files,
)
from tests.unit._creator_metric_silver_fixtures import (
    seed_preexisting_youtube_creator_metric_records,
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


def _declare_seed_archive(
    data_root: DataLakeRoot, tmp_path: Path, observation_records: tuple[dict, ...]
) -> None:
    archive = tmp_path / "youtube_seed_archive"
    archive.mkdir()
    (archive / ".orca-data-root").write_text(
        json.dumps(
            {
                "root_uuid": "01KWYTSEEDARCHIVEROOT00002",
                "label": "youtube-seed-producer-test-archive",
                "contract_version": "v0",
            }
        ),
        encoding="utf-8",
    )
    for record in observation_records:
        packet_id = record["raw_anchor"]
        packet = archive / "raw" / raw_shard(packet_id) / packet_id
        body = packet / "raw" / "caption.json"
        body.parent.mkdir(parents=True, exist_ok=True)
        body.write_bytes(b"caption fixture; cited watch HTML intentionally absent")
        digest = hashlib.sha256(body.read_bytes()).hexdigest()
        (packet / "manifest.json").write_text(
            json.dumps(
                {
                    "packet_id": packet_id,
                    "preserved_files": [
                        {
                            "file_id": "file_01",
                            "relative_packet_path": "raw/caption.json",
                            "size_bytes": body.stat().st_size,
                            "sha256": digest,
                            "hash_basis": "raw_stored_bytes",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
    epoch_path = data_root.path / EPOCH_MARKER_FILENAME
    epoch = json.loads(epoch_path.read_text(encoding="utf-8"))
    epoch["legacy_roots"] = [str(archive)]
    epoch_path.write_text(json.dumps(epoch), encoding="utf-8")


def test_preexisting_youtube_rollups_are_audit_discoverable(tmp_path: Path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")

    result = seed_preexisting_youtube_creator_metric_records(
        data_root,
        json.loads(DEFAULT_YOUTUBE_SEED_PATH.read_text(encoding="utf-8-sig")),
        wrapper_key=YOUTUBE_SEED_WRAPPER_KEY,
    )

    accounts = sorted({_account_of(r) for r in result.rollup_records})
    assert accounts, "expected at least one covered YouTube account"
    assert len(result.rollup_records) == len(accounts)  # one rollup per account
    assert all(path.is_file() for path in result.rollup_paths)

    _declare_seed_archive(data_root, tmp_path, result.observation_records)

    # The checked-in review inputs assert watch-HTML hashes but do not preserve those
    # bytes. Their rollups stay discoverable only through the explicit audit mode.
    with pytest.raises(CreatorRollupDiscoveryError, match="missing_account_rollup"):
        discover_creator_metric_rollup_records(
            data_root, account_ledger=_yt_discovery_ledger(*accounts)
        )
    found = discover_creator_metric_rollup_records(
        data_root,
        account_ledger=_yt_discovery_ledger(*accounts),
        lineage_mode=AUDIT_COMPATIBLE,
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
