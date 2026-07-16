"""Companion temp-lake materializer for the Silver compatibility fixtures.

The checked-in fixtures under ``tests/fixtures/silver_compatibility/`` pin the
byte-faithful persisted shape of every declared compatibility tuple. This
helper owns the deterministic synthetic companion facts those fixtures cite --
raw packet bodies and the Fragrantica cleaning-audit sibling -- and
materializes them plus the fixture records themselves into a temporary
``DataLakeRoot`` so the equality gate can prove each profile's reference
resolver behaves exactly as its registry entry declares.

TEST-ONLY: fixture records are written through the raw derived-record path on
purpose (they model immutable pre-existing bytes); this never demonstrates
writer acceptance -- the strict front door must keep rejecting every one.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from data_lake.canonical_json import canonical_record_bytes
from data_lake.root import DataLakeRoot, raw_shard
from data_lake.silver_compatibility import (
    SILVER_COMPATIBILITY_PROFILES,
    SilverCompatibilityProfile,
)
from data_lake.silver_record import silver_content_hash

HARNESS_ROOT = Path(__file__).resolve().parents[2]

FRAGRANTICA_PACKET_ID = "01J000000000000000000000F1"
YOUTUBE_OBS_PACKET_ID = "01J000000000000000000000Y1"
PROJECTION_OBS_PACKET_ID = "01J000000000000000000000P1"
TIKTOK_V1_PACKET_ID = "01J000000000000000000000T1"

FRAGRANTICA_RAW_BODY = b"silver compatibility fixture raw body: fragrantica_v0\n"
YOUTUBE_OBS_RAW_BODY = b"silver compatibility fixture raw body: creator_metric_observation_youtube_v0\n"
PROJECTION_OBS_RAW_BODY = b"silver compatibility fixture raw body: creator_metric_observation_projection_v0\n"
TIKTOK_V1_RAW_BODY = b"silver compatibility fixture raw body: tiktok_comment_attention_v1\n"

# One raw packet per fixture family: packet id -> (body, relative path).
FIXTURE_PACKETS: dict[str, tuple[bytes, str]] = {
    FRAGRANTICA_PACKET_ID: (FRAGRANTICA_RAW_BODY, "raw/01_http_response_body.bin"),
    YOUTUBE_OBS_PACKET_ID: (YOUTUBE_OBS_RAW_BODY, "preserved/watch.html"),
    PROJECTION_OBS_PACKET_ID: (PROJECTION_OBS_RAW_BODY, "raw/01_ig_reels_grid_capture.json"),
    TIKTOK_V1_PACKET_ID: (TIKTOK_V1_RAW_BODY, "raw/01_tiktok_batch_capture.json"),
}


def fragrantica_audit_record() -> dict[str, Any]:
    """The deterministic cleaning-audit sibling both Fragrantica fixtures cite."""
    record = {
        "record_id": "01J00000000000000000000FA1.json",
        "raw_anchor": FRAGRANTICA_PACKET_ID,
        "lane_namespace": "cleaning_fragrantica_audit",
        "content_hash": "",
        "payload": {"audit": "silver compatibility fixture cleaning audit"},
    }
    record["content_hash"] = f"sha256:{silver_content_hash(record)}"
    return record


def load_fixture_record(profile: SilverCompatibilityProfile) -> dict[str, Any]:
    path = HARNESS_ROOT / profile.fixture_path
    record = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(record, dict):
        raise AssertionError(f"compatibility fixture must be a JSON object: {path}")
    return record


def _commit_packet(data_root: DataLakeRoot, packet_id: str) -> None:
    body, relative = FIXTURE_PACKETS[packet_id]
    container = data_root.path / "raw" / raw_shard(packet_id) / packet_id
    if (container / "manifest.json").exists():
        return
    preserved = container / Path(relative)
    preserved.parent.mkdir(parents=True, exist_ok=True)
    preserved.write_bytes(body)
    (container / "manifest.json").write_text(
        json.dumps(
            {
                "packet_id": packet_id,
                "preserved_files": [
                    {
                        "file_id": "file_01",
                        "relative_packet_path": relative,
                        "size_bytes": len(body),
                        "sha256": hashlib.sha256(body).hexdigest(),
                        "hash_basis": "raw_stored_bytes",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def _seed_record(data_root: DataLakeRoot, record: Mapping[str, Any]) -> Path:
    path = data_root.record_path(
        subtree="derived",
        raw_anchor=str(record["raw_anchor"]),
        lane=str(record["lane_namespace"]),
        record_id=str(record["record_id"]),
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_record_bytes(dict(record)))
    return path


def materialize_fixture_lake(
    data_root: DataLakeRoot,
) -> dict[str, tuple[dict[str, Any], Path]]:
    """Seed every fixture record plus its cited synthetic sources.

    Returns ``{profile_id: (fixture_record, persisted_path)}``.
    """
    for packet_id in FIXTURE_PACKETS:
        _commit_packet(data_root, packet_id)
    _seed_record(data_root, fragrantica_audit_record())
    seeded: dict[str, tuple[dict[str, Any], Path]] = {}
    for profile in SILVER_COMPATIBILITY_PROFILES:
        record = load_fixture_record(profile)
        seeded[profile.profile_id] = (record, _seed_record(data_root, record))
    return seeded


__all__ = [
    "FIXTURE_PACKETS",
    "FRAGRANTICA_PACKET_ID",
    "FRAGRANTICA_RAW_BODY",
    "HARNESS_ROOT",
    "PROJECTION_OBS_PACKET_ID",
    "PROJECTION_OBS_RAW_BODY",
    "TIKTOK_V1_PACKET_ID",
    "TIKTOK_V1_RAW_BODY",
    "YOUTUBE_OBS_PACKET_ID",
    "YOUTUBE_OBS_RAW_BODY",
    "fragrantica_audit_record",
    "load_fixture_record",
    "materialize_fixture_lake",
]
