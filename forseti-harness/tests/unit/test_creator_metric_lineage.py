from __future__ import annotations

import hashlib
import json
from pathlib import Path

from data_lake.creator_metric_lineage import (
    EXCLUDED,
    HISTORICAL_COMPATIBLE,
    SOURCE_BACKED_COMPLETE,
    build_creator_metric_lineage_index,
)
from data_lake.root import DataLakeRoot, EPOCH_MARKER_FILENAME, raw_shard
from data_lake.silver_census import build_silver_observation_census
from data_lake.silver_record import silver_content_hash
from tests.unit._creator_metric_silver_fixtures import seed_preexisting_legacy_silver_record


PACKET_CURRENT = "01KW2MJM01Y0936VNECWB3MHSD"
PACKET_ARCHIVE = "01KW2MJM01Y0936VNECWB3MHSE"
PACKET_ABSENT = "01KW2MJM01Y0936VNECWB3MHSF"
PACKET_AMBIGUOUS = "01KW2MJM01Y0936VNECWB3MHSG"


def _write_packet(
    root: Path,
    packet_id: str,
    *,
    body: bytes,
    file_id: str = "file_01",
    relative: str = "raw/evidence.bin",
) -> None:
    packet = root / "raw" / raw_shard(packet_id) / packet_id
    file_path = packet.joinpath(*relative.split("/"))
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(body)
    manifest = {
        "packet_id": packet_id,
        "source_family": "youtube",
        "source_surface": "fixture",
        "preserved_files": [
            {
                "file_id": file_id,
                "relative_packet_path": relative,
                "size_bytes": len(body),
                "sha256": hashlib.sha256(body).hexdigest(),
                "hash_basis": "raw_stored_bytes",
            }
        ],
    }
    (packet / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _archive_root(path: Path) -> Path:
    path.mkdir(parents=True)
    (path / ".orca-data-root").write_text(
        json.dumps(
            {
                "root_uuid": "01KWLEGACYROOTIDENTITY0001",
                "label": "legacy-fixture",
                "contract_version": "v0",
            }
        ),
        encoding="utf-8",
    )
    return path


def _declare_archives(data_root: DataLakeRoot, *archives: Path) -> None:
    marker_path = data_root.path / EPOCH_MARKER_FILENAME
    marker = json.loads(marker_path.read_text(encoding="utf-8"))
    marker["legacy_roots"] = [str(path) for path in archives]
    marker_path.write_text(json.dumps(marker, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _record(
    packet_id: str,
    *,
    expected_sha256: str,
    record_id: str,
    direct: bool = False,
) -> dict:
    raw_ref = {
        "ref_type": "raw_packet",
        "packet_id": packet_id,
        "sha256": expected_sha256,
        "hash_basis": "raw_stored_bytes",
    }
    if direct:
        raw_ref.update(file_id="file_01", relative_packet_path="raw/evidence.bin")
    record = {
        "record_id": record_id,
        "raw_anchor": packet_id,
        "lane_namespace": "creator_metric_silver",
        "producer_id": "test.creator_metric_lineage",
        "schema_version": "silver_vault_record_v0",
        "producer_schema_version": "creator_metric_lineage_fixture_v0",
        "content_hash": "",
        "content_hash_basis": "canonical_json_excluding_content_hash",
        "record_kind": "observation",
        "payload_kind": "MetricObservation",
        "producer_row_kind": "yt_media_metric",
        "source_family": "social_media",
        "source_surface": "youtube_shorts",
        "observed_at": "2026-07-15T00:00:00Z",
        "captured_at": "2026-07-15T00:00:00Z",
        "raw_refs": [raw_ref],
        "derived_refs": [],
        "payload": {
            "observation": {
                "subject": {
                    "ref_type": "entity_key",
                    "ref": {
                        "namespace": "youtube",
                        "kind": "public_content_object",
                        "native_id": record_id,
                    },
                },
                "metric_name": "view_count",
                "metric_value": 1,
                "metric_posture": {
                    "kind": "observed",
                    "reason_code": None,
                    "reason_detail": None,
                },
                "coverage_window": {"start": None, "end": None},
                "source_surface": "youtube_shorts",
                "source_publication_or_event": None,
                "unit": "count",
            }
        },
    }
    record["content_hash"] = f"sha256:{silver_content_hash(record)}"
    return record


def _append(data_root: DataLakeRoot, record: dict) -> Path:
    return seed_preexisting_legacy_silver_record(data_root, record)


def test_current_root_bytes_are_recomputed_and_admitted(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    body = b"current evidence"
    _write_packet(root.path, PACKET_CURRENT, body=body)
    path = _append(
        root,
        _record(
            PACKET_CURRENT,
            expected_sha256=hashlib.sha256(body).hexdigest(),
            record_id="01KWLINEAGECURRENT00000001.json",
            direct=True,
        ),
    )

    result = build_creator_metric_lineage_index(root).classification_for_path(path)

    assert result.status == SOURCE_BACKED_COMPLETE
    assert result.current_source_backed_eligible is True
    assert result.expected_sha256 == result.recomputed_sha256
    assert result.evidence_roots[0].role == "current_root"


def test_declared_archive_bytes_can_verify_without_becoming_current(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    archive = _archive_root(tmp_path / "archive")
    _declare_archives(root, archive)
    body = b"archived evidence"
    _write_packet(archive, PACKET_ARCHIVE, body=body)
    path = _append(
        root,
        _record(
            PACKET_ARCHIVE,
            expected_sha256=hashlib.sha256(body).hexdigest(),
            record_id="01KWLINEAGEARCHIVE00000001.json",
            direct=True,
        ),
    )

    result = build_creator_metric_lineage_index(root).classification_for_path(path)

    assert result.status == SOURCE_BACKED_COMPLETE
    assert result.reason_code == "declared_archive_bytes_verified"
    assert result.current_source_backed_eligible is False
    assert result.evidence_roots[0].root_uuid == "01KWLEGACYROOTIDENTITY0001"


def test_archive_packet_without_cited_bytes_is_historical_compatible(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    archive = _archive_root(tmp_path / "archive")
    _declare_archives(root, archive)
    _write_packet(archive, PACKET_ARCHIVE, body=b"caption json, not watch html")
    path = _append(
        root,
        _record(
            PACKET_ARCHIVE,
            expected_sha256=hashlib.sha256(b"missing watch html").hexdigest(),
            record_id="01KWLINEAGEHISTORICAL0001.json",
        ),
    )

    result = build_creator_metric_lineage_index(root).classification_for_path(path)

    assert result.status == HISTORICAL_COMPATIBLE
    assert result.reason_code == "archive_packet_present_cited_bytes_absent"
    assert result.impact and "excluded from current" in result.impact
    assert result.owner == "creator_metric_silver owner"
    assert result.upgrade_trigger and "re-capture" in result.upgrade_trigger


def test_direct_hash_mismatch_is_excluded(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    _write_packet(root.path, PACKET_CURRENT, body=b"actual")
    path = _append(
        root,
        _record(
            PACKET_CURRENT,
            expected_sha256=hashlib.sha256(b"expected").hexdigest(),
            record_id="01KWLINEAGEMISMATCH0000001.json",
            direct=True,
        ),
    )

    result = build_creator_metric_lineage_index(root).classification_for_path(path)

    assert result.status == EXCLUDED
    assert result.reason_code == "hash_mismatch"


def test_unmounted_declared_archive_is_excluded_visibly(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    _declare_archives(root, tmp_path / "not-mounted")
    path = _append(
        root,
        _record(
            PACKET_ABSENT,
            expected_sha256="a" * 64,
            record_id="01KWLINEAGEUNMOUNTED00001.json",
        ),
    )

    result = build_creator_metric_lineage_index(root).classification_for_path(path)

    assert result.status == EXCLUDED
    assert result.reason_code == "declared_archive_unmounted_or_invalid"
    assert result.evidence_roots[0].mounted is False


def test_duplicate_packet_resolution_across_epochs_is_excluded(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    archive = _archive_root(tmp_path / "archive")
    _declare_archives(root, archive)
    body = b"duplicated"
    _write_packet(root.path, PACKET_AMBIGUOUS, body=body)
    _write_packet(archive, PACKET_AMBIGUOUS, body=body)
    path = _append(
        root,
        _record(
            PACKET_AMBIGUOUS,
            expected_sha256=hashlib.sha256(body).hexdigest(),
            record_id="01KWLINEAGEAMBIGUOUS00001.json",
            direct=True,
        ),
    )

    result = build_creator_metric_lineage_index(root).classification_for_path(path)

    assert result.status == EXCLUDED
    assert result.reason_code == "ambiguous_duplicate_resolution"


def test_census_keeps_unresolved_historical_bytes_visible_as_non_authority(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    archive = _archive_root(tmp_path / "archive")
    _declare_archives(root, archive)
    current_body = b"current"
    _write_packet(root.path, PACKET_CURRENT, body=current_body)
    _write_packet(archive, PACKET_ARCHIVE, body=b"caption only")
    _append(
        root,
        _record(
            PACKET_CURRENT,
            expected_sha256=hashlib.sha256(current_body).hexdigest(),
            record_id="01KWLINEAGECENSUSCURRENT1.json",
            direct=True,
        ),
    )
    _append(
        root,
        _record(
            PACKET_ARCHIVE,
            expected_sha256=hashlib.sha256(b"absent watch html").hexdigest(),
            record_id="01KWLINEAGECENSUSHISTORY1.json",
        ),
    )

    census = build_silver_observation_census(root)

    assert census["totals"]["silver_records"] == 2
    assert census["totals"]["directly_observed_atomic_metric_values"] == 1
    assert census["totals"]["creator_metric_source_backed_complete_records"] == 1
    assert census["totals"]["creator_metric_historical_compatible_records"] == 0
    assert census["totals"]["creator_metric_excluded_records"] == 0
    assert census["totals"]["unclassified_silver_records"] == 1
    assert census["errors"][0]["kind"] == "silver_record_source_unresolved"
