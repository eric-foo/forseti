"""Physical temp-lake source fixtures for creator-metric Silver tests."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

from data_lake.root import DataLakeRoot, raw_shard


YOUTUBE_FIXTURE_PACKET_ID = "01J00000000000000000000001"


def commit_raw_packet(
    data_root: DataLakeRoot,
    *,
    packet_id: str,
    body: bytes,
    file_id: str = "file_01",
    relative_packet_path: str = "raw/01.json",
) -> dict[str, str]:
    """Materialize one loader-verifiable raw packet and return its exact anchor."""
    digest = hashlib.sha256(body).hexdigest()
    container = data_root.path / "raw" / raw_shard(packet_id) / packet_id
    preserved = container / relative_packet_path
    manifest_path = container / "manifest.json"
    if manifest_path.exists():
        loaded = data_root.load_raw_packet(packet_id)
        entry = next(
            item for item in loaded.manifest["preserved_files"] if item["file_id"] == file_id
        )
        return {
            "file_id": entry["file_id"],
            "relative_packet_path": entry["relative_packet_path"],
            "sha256": entry["sha256"],
            "hash_basis": entry.get("hash_basis", "raw_stored_bytes"),
        }

    preserved.parent.mkdir(parents=True)
    preserved.write_bytes(body)
    manifest_path.write_text(
        json.dumps(
            {
                "packet_id": packet_id,
                "preserved_files": [
                    {
                        "file_id": file_id,
                        "relative_packet_path": relative_packet_path,
                        "size_bytes": len(body),
                        "sha256": digest,
                        "hash_basis": "raw_stored_bytes",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    data_root.load_raw_packet(packet_id)
    return {
        "file_id": file_id,
        "relative_packet_path": relative_packet_path,
        "sha256": digest,
        "hash_basis": "raw_stored_bytes",
    }


def materialize_youtube_seed_sources(
    data_root: DataLakeRoot,
    seed_document: Mapping[str, Any],
    *,
    wrapper_key: str,
) -> dict[str, Any]:
    """Copy a seed and bind every observation to one real temp-lake packet.

    Metric facts and observation identities stay unchanged. Only provenance that
    points at the unavailable private historical lake is rebound for unit tests.
    """
    copied = deepcopy(seed_document)
    body = b'{"fixture":"youtube creator metric source"}'
    anchor = commit_raw_packet(
        data_root,
        packet_id=YOUTUBE_FIXTURE_PACKET_ID,
        body=body,
        file_id="source",
        relative_packet_path="preserved/source.json",
    )
    for observation in copied[wrapper_key]["metric_observations"]:
        observation["source_packet_id_or_none"] = YOUTUBE_FIXTURE_PACKET_ID
        observation["source_packet_pointer_or_none"] = None
        observation["source_evidence_sha256"] = anchor["sha256"]
        observation["source_evidence_hash_basis"] = (
            "source_captured_selective_payload_sha256"
        )
        observation["source_watch_html_sha256_or_none"] = None
        observation["source_shorts_html_sha256_or_none"] = None
        observation["source_file"] = anchor["relative_packet_path"]
    return copied
