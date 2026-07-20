"""Physical temp-lake source fixtures for creator-metric Silver tests."""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from data_lake.root import DataLakeRoot, raw_shard


YOUTUBE_FIXTURE_PACKET_ID = "01J00000000000000000000001"


def seed_preexisting_legacy_silver_record(
    data_root: DataLakeRoot,
    record: Mapping[str, Any],
) -> Path:
    """TEST-ONLY: materialize synthetic historical bytes for read-side proof.

    This deliberately bypasses the authoritative Silver append API: the record
    models bytes that already existed before the physical-authority contract.
    It proves only legacy read-side classification in a temporary lake, never
    writer acceptance, private-lake provenance, or a production ingest route.
    """
    path = data_root.record_path(
        subtree="derived",
        raw_anchor=str(record["raw_anchor"]),
        lane=str(record["lane_namespace"]),
        record_id=str(record["record_id"]),
    )
    if path.exists():
        raise AssertionError(f"historical fixture record already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(dict(record), ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def seed_preexisting_youtube_creator_metric_records(
    data_root: DataLakeRoot,
    seed_document: Mapping[str, Any],
    *,
    wrapper_key: str,
    limit_to_platform_account_ids: frozenset[str] | set[str] | None = None,
):
    """Build and seed synthetic pre-contract YouTube Silver record bytes.

    The production builders preserve the historical envelope shape; this
    helper writes their output directly under the derived-record grammar. It
    is strictly a read-side classification fixture and must not be used as
    evidence that the authoritative append route accepts the records.

    ``limit_to_platform_account_ids``, when given, restricts materialization to
    the named accounts only, so callers that assert on a handful of accounts
    are not charged for building and writing every committed-seed record.
    Default ``None`` keeps the full seed and byte-identical behavior.
    """
    from capture_spine.creator_profile_current.youtube_silver_metric_producer import (
        YoutubeCreatorMetricSilverResult,
        build_metric_observation_record,
        build_metric_rollup_record,
    )

    copied = deepcopy(seed_document)
    seed = copied[wrapper_key]
    if limit_to_platform_account_ids is not None:
        seed["metric_observations"] = [
            seed_observation
            for seed_observation in seed["metric_observations"]
            if seed_observation["platform_account_id"] in limit_to_platform_account_ids
        ]
        if not seed["metric_observations"]:
            raise AssertionError(
                "limit_to_platform_account_ids matched zero metric_observations "
                f"(check for typos): {sorted(limit_to_platform_account_ids)}"
            )
        seed["metric_rollups"] = [
            seed_rollup
            for seed_rollup in seed["metric_rollups"]
            if seed_rollup["platform_account_ids"][0] in limit_to_platform_account_ids
        ]
    observation_records: list[dict[str, Any]] = []
    observation_paths: list[Path] = []
    refs_by_seed_id: dict[str, dict[str, str]] = {}
    for seed_observation in seed["metric_observations"]:
        record = build_metric_observation_record(seed_observation=seed_observation)
        path = seed_preexisting_legacy_silver_record(data_root, record)
        observation_records.append(record)
        observation_paths.append(path)
        refs_by_seed_id[seed_observation["metric_observation_id"]] = {
            "raw_anchor": record["raw_anchor"],
            "lane_namespace": record["lane_namespace"],
            "record_id": record["record_id"],
            "content_hash": record["content_hash"],
        }

    rollup_records: list[dict[str, Any]] = []
    rollup_paths: list[Path] = []
    for seed_rollup in seed["metric_rollups"]:
        account_ids = seed_rollup["platform_account_ids"]
        if not isinstance(account_ids, list) or len(account_ids) != 1:
            raise AssertionError("historical YouTube rollup fixture requires one account id")
        record = build_metric_rollup_record(
            seed_rollup=seed_rollup,
            ref_by_seed_observation_id=refs_by_seed_id,
            raw_anchor=account_ids[0],
        )
        path = seed_preexisting_legacy_silver_record(data_root, record)
        rollup_records.append(record)
        rollup_paths.append(path)

    return YoutubeCreatorMetricSilverResult(
        observation_records=observation_records,
        observation_paths=observation_paths,
        rollup_records=rollup_records,
        rollup_paths=rollup_paths,
        seed_document=copied,
    )


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
    """Copy a seed and bind every observation to one synthetic temp-lake packet.

    Metric facts and observation identities stay unchanged. Only provenance that
    points at the unavailable private historical lake is rebound. This is
    structural verifier proof only; it does not prove that private-lake seed
    sources resolve.
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
