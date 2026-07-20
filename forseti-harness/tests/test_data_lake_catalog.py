from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from data_lake.attachment_record_entry import (
    DERIVATION_RULE_VERSION,
    ENTRY_SERIALIZATION_VERSION,
)
from data_lake.catalog import (
    BRONZE_ATTACHMENT_RECORD_PHYSICALIZATION,
    BRONZE_ATTACHMENT_RECORD_SCHEMA_VERSION,
    BRONZE_BASELINE_STATUS,
    BRONZE_CATALOG_SCHEMA_VERSION,
    CATALOG_RELATIVE_ROOT,
    _attachment_record_id,
    catalog_coverage_census,
    inspect_catalog,
    load_attachment_record_body,
    rebuild_catalog,
    source_surface_catalog_rows,
)
from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard
from data_lake.silver_record import append_raw_packet_tombstone
import runners.run_data_lake_catalog as catalog_runner
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet


def _catalog_root(root: DataLakeRoot) -> Path:
    return root.path.joinpath(*CATALOG_RELATIVE_ROOT)


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _write_reddit_packet(
    root: DataLakeRoot,
    tmp_path: Path,
    *,
    body: str = "thread body",
    session_identity: str = "reddit-session",
    series_id: str | None = None,
):
    src = tmp_path / f"reddit_{body.replace(' ', '_')}.json"
    src.write_text(json.dumps({"body": body}, sort_keys=True), encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family="reddit",
        source_surface="r/B2BMarketing",
        source_locator=known_fact("https://www.reddit.com/r/B2BMarketing/comments/x/"),
        decision_question="is this B2B tool getting unusual attention?",
        capture_context="catalog fixture",
        session_identity=session_identity,
        series_id=series_id,
    )


def test_rebuild_catalog_excludes_tombstoned_packet_but_keeps_raw_auditable(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    old = _write_reddit_packet(root, tmp_path, body="old testing history")
    retained = _write_reddit_packet(root, tmp_path, body="latest retained history")
    old_id = old.packet.packet_id
    retained_id = retained.packet.packet_id
    append_raw_packet_tombstone(
        root,
        retained_packet_id=retained_id,
        tombstoned_packet_id=old_id,
        captured_at="2026-07-16T15:00:00Z",
        reason="owner-directed cleanup of superseded testing history",
    )

    report = rebuild_catalog(root)

    assert report["status"] == "rebuilt"
    assert report["packet_count"] == 1
    assert not (_catalog_root(root) / "by_packet" / f"{old_id}.json").exists()
    assert (_catalog_root(root) / "by_packet" / f"{retained_id}.json").is_file()
    assert root.find_packet(old_id) is not None
    assert root.load_raw_packet(old_id).bodies


def _write_ig_reels_grid_packet(
    root: DataLakeRoot,
    tmp_path: Path,
    *,
    shortcode: str | None = "REEL123",
    session_identity: str = "ig-session",
):
    joined_rows = []
    if shortcode is not None:
        joined_rows.append(
            {
                "dom_row": {
                    "shortcode": shortcode,
                    "kind": "reel",
                    "permalink_url": f"https://www.instagram.com/reel/{shortcode}/",
                }
            }
        )
    payload = {
        "creator_profile_snapshot": {
            "source_profile": "hyram",
            "numeric_id": "5802114508",
            "profile_grid_url": "https://www.instagram.com/hyram/reels/",
        },
        "joined_rows": joined_rows,
    }
    src = tmp_path / "ig_reels_grid_capture.json"
    src.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family="instagram_creator",
        source_surface="ig_reels_grid_dom_passive_json",
        source_locator=known_fact("https://www.instagram.com/hyram/reels/"),
        decision_question="is this creator gaining momentum?",
        capture_context="catalog fixture",
        session_identity=session_identity,
    )


def _facet_rows(root: DataLakeRoot) -> list[dict]:
    rows: list[dict] = []
    for path in sorted((_catalog_root(root) / "by_facet").rglob("*.jsonl")):
        rows.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines())
    return rows


def _source_surface_payload(root: DataLakeRoot) -> dict:
    return json.loads(
        (_catalog_root(root) / "source_surfaces.json").read_text(encoding="utf-8")
    )


def _catalog_manifest(root: DataLakeRoot) -> dict:
    return json.loads((_catalog_root(root) / "manifest.json").read_text(encoding="utf-8"))


def _source_surface_rows(root: DataLakeRoot) -> list[dict]:
    return _source_surface_payload(root)["source_surfaces"]


def _attachment_record_root(root: DataLakeRoot) -> Path:
    return _catalog_root(root) / "attachment_records"


def _attachment_record_manifest(root: DataLakeRoot) -> dict:
    return json.loads(
        (_attachment_record_root(root) / "manifest.json").read_text(encoding="utf-8")
    )


def _attachment_record_rows(root: DataLakeRoot) -> list[dict]:
    return [
        json.loads(line)
        for line in (_attachment_record_root(root) / "all_attachment_records.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]


def test_rebuild_catalog_indexes_universal_and_ig_facets(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    reddit = _write_reddit_packet(root, tmp_path, series_id="b2b-series")
    ig = _write_ig_reels_grid_packet(root, tmp_path)

    report = rebuild_catalog(root)

    assert report["status"] == "rebuilt"
    assert report["catalog_schema_version"] == BRONZE_CATALOG_SCHEMA_VERSION
    assert report["bronze_baseline_status"] == BRONZE_BASELINE_STATUS
    assert report["packet_count"] == 2
    assert report["attachment_record_count"] == 2
    assert report["source_surface_count"] == 2
    assert inspect_catalog(root)["status"] == "ok"

    classifications = {
        (row["source_family"], row["source_surface"]): row["source_classification"]
        for row in _source_surface_rows(root)
    }
    assert classifications[
        ("instagram_creator", "ig_reels_grid_dom_passive_json")
    ]["mapping_status"] == "classified"
    assert classifications[
        ("instagram_creator", "ig_reels_grid_dom_passive_json")
    ]["operator_identity"] == "instagram"
    assert classifications[("reddit", "r/B2BMarketing")]["mapping_status"] == "unknown"
    assert classifications[("reddit", "r/B2BMarketing")]["residuals"] == [
        "unmapped_legacy_source_pair"
    ]

    ig_pid = ig.packet.packet_id
    ig_entry = json.loads(
        (_catalog_root(root) / "by_packet" / f"{ig_pid}.json").read_text(encoding="utf-8")
    )
    assert ig_entry["raw_path"] == f"raw/{raw_shard(ig_pid)}/{ig_pid}"
    assert ig_entry["catalog_schema_version"] == BRONZE_CATALOG_SCHEMA_VERSION
    assert ig_entry["attachment_record_count"] == 1
    assert len(ig_entry["attachment_record_ids"]) == 1
    assert ig_entry["source_family"] == "instagram_creator"
    facets_by_namespace = {facet["namespace"]: facet["value"] for facet in ig_entry["facets"]}
    expected_facets = {
        "instagram_creator_handle": "hyram",
        "instagram_creator_numeric_id": "5802114508",
        "instagram_shortcode": "REEL123",
        "source_family": "instagram_creator",
        "source_surface": "ig_reels_grid_dom_passive_json",
        "session_identity": "ig-session",
    }
    assert expected_facets.items() <= facets_by_namespace.items()

    reddit_pid = reddit.packet.packet_id
    series_rows = [
        json.loads(line)
        for path in sorted((_catalog_root(root) / "by_series").glob("*.jsonl"))
        for line in path.read_text(encoding="utf-8").splitlines()
    ]
    assert any(row["packet_id"] == reddit_pid for row in series_rows)
    assert any(
        row["packet_id"] == ig_pid
        and row["facet"]["namespace"] == "instagram_creator_handle"
        and row["facet"]["value"] == "hyram"
        for row in _facet_rows(root)
    )

    report_surface_rows = {
        (row["source_family"], row["source_surface"]): row
        for row in report["source_surfaces"]
    }
    surface_payload = _source_surface_payload(root)
    assert (
        surface_payload["authority"]
        == "generated_from_raw_packet_manifests; raw remains authoritative"
    )
    assert surface_payload["catalog_schema_version"] == BRONZE_CATALOG_SCHEMA_VERSION
    assert surface_payload["bronze_baseline_status"] == BRONZE_BASELINE_STATUS
    assert "not capture_support" in surface_payload["completeness"]
    assert "neither value claims" in surface_payload["field_semantics"]["facet_extractor"]
    assert "union" in surface_payload["field_semantics"]["facet_namespaces"]
    assert surface_payload["stable_query_paths"]["all_packets"] == "all_packets.jsonl"
    assert surface_payload["stable_query_paths"]["attachment_records_root"] == "attachment_records/"
    generated_surface_rows = {
        (row["source_family"], row["source_surface"]): row
        for row in surface_payload["source_surfaces"]
    }
    assert generated_surface_rows == report_surface_rows
    reddit_surface_path = report_surface_rows[("reddit", "r/B2BMarketing")][
        "by_source_surface_path"
    ]
    reddit_surface = report_surface_rows[("reddit", "r/B2BMarketing")]
    assert reddit_surface_path.startswith("by_source_surface/")
    assert (_catalog_root(root) / reddit_surface_path).is_file()
    assert reddit_surface["attachment_record_count"] == 1
    assert reddit_surface["attachment_records_path"].startswith(
        "attachment_records/by_source_surface/"
    )
    assert (_catalog_root(root) / reddit_surface["attachment_records_path"]).is_file()
    assert report_surface_rows[("reddit", "r/B2BMarketing")]["packet_count"] == 1
    assert (
        report_surface_rows[("reddit", "r/B2BMarketing")]["facet_extractor"]
        == "universal_only"
    )
    ig_surface = report_surface_rows[("instagram_creator", "ig_reels_grid_dom_passive_json")]
    assert ig_surface["by_source_surface_path"].startswith("by_source_surface/")
    assert (_catalog_root(root) / ig_surface["by_source_surface_path"]).is_file()
    assert ig_surface["attachment_record_count"] == 1
    assert ig_surface["attachment_records_path"].startswith(
        "attachment_records/by_source_surface/"
    )
    assert ig_surface["packet_count"] == 1
    assert ig_surface["facet_extractor"] == "registered"
    assert {
        "instagram_creator_handle",
        "instagram_creator_numeric_id",
        "instagram_shortcode",
    } <= set(ig_surface["facet_namespaces"])


def test_rebuild_catalog_marks_unknown_future_surface_universal_only(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    src = tmp_path / "future_lane_payload.json"
    src.write_text(json.dumps({"creator": "future"}, sort_keys=True), encoding="utf-8")
    write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family="future_creator_network",
        source_surface="future_creator_feed_v1",
        source_locator=known_fact("https://example.invalid/future/creator"),
        decision_question="does a future lane appear in Bronze coverage?",
        capture_context="catalog fixture",
        session_identity="future-session",
    )

    report = rebuild_catalog(root)

    rows = {
        (row["source_family"], row["source_surface"]): row
        for row in report["source_surfaces"]
    }
    future_row = rows[("future_creator_network", "future_creator_feed_v1")]
    assert future_row["by_source_surface_path"].startswith("by_source_surface/")
    assert future_row["attachment_records_path"].startswith(
        "attachment_records/by_source_surface/"
    )
    assert future_row["attachment_record_count"] == 1
    assert future_row["packet_count"] == 1
    assert future_row["facet_extractor"] == "universal_only"
    assert {
        "source_family",
        "source_surface",
        "session_identity",
        "source_locator_sha256",
    } <= set(future_row["facet_namespaces"])


def test_source_surface_attachment_path_is_surface_bucket_not_family_bucket(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    for source_family in ("future_creator_network", "synthetic_creator_network"):
        src = tmp_path / f"{source_family}.json"
        src.write_text(json.dumps({"source_family": source_family}), encoding="utf-8")
        write_local_source_capture_packet(
            data_root=root,
            input_files=[src],
            source_family=source_family,
            source_surface="shared_creator_feed_v1",
            source_locator=known_fact(f"https://example.invalid/{source_family}"),
            decision_question="does a shared surface stay filterable by family?",
            capture_context="catalog fixture",
            session_identity=f"{source_family}-session",
        )

    report = rebuild_catalog(root)

    rows = {
        (row["source_family"], row["source_surface"]): row
        for row in report["source_surfaces"]
    }
    first = rows[("future_creator_network", "shared_creator_feed_v1")]
    second = rows[("synthetic_creator_network", "shared_creator_feed_v1")]
    assert first["attachment_record_count"] == 1
    assert second["attachment_record_count"] == 1
    assert first["attachment_records_path"] == second["attachment_records_path"]
    bucket_rows = [
        json.loads(line)
        for line in (_catalog_root(root) / first["attachment_records_path"])
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert {row["source_family"] for row in bucket_rows} == {
        "future_creator_network",
        "synthetic_creator_network",
    }


def test_attachment_record_ids_use_structured_material_not_delimiter_join() -> None:
    packet_id = "01KWBMNTESWZVSVD3YASDAXK0A"
    body_sha256 = "a" * 64

    first = _attachment_record_id(
        packet_id=packet_id,
        file_id="a|b",
        relative_packet_path="c",
        body_sha256=body_sha256,
    )
    second = _attachment_record_id(
        packet_id=packet_id,
        file_id="a",
        relative_packet_path="b|c",
        body_sha256=body_sha256,
    )

    assert first != second


def test_attachment_records_index_preserved_bodies_and_resolve_bytes(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    reddit = _write_reddit_packet(root, tmp_path, series_id="b2b-series")
    ig = _write_ig_reels_grid_packet(root, tmp_path)

    report = rebuild_catalog(root)

    assert report["attachment_record_count"] == 2
    manifest = _attachment_record_manifest(root)
    assert manifest["authority"] == "generated_from_raw_packet_manifests; raw remains authoritative"
    assert manifest["attachment_record_schema_version"] == BRONZE_ATTACHMENT_RECORD_SCHEMA_VERSION
    assert manifest["attachment_record_physicalization"] == BRONZE_ATTACHMENT_RECORD_PHYSICALIZATION
    assert "physicalized_manifest_equivalent_attachment_records" in manifest["completeness"]
    assert "not the positional file_id" in manifest["field_semantics"]["attachment_record_id"]
    assert manifest["stable_query_paths"]["by_packet_root"] == "attachment_records/by_packet/"

    rows = _attachment_record_rows(root)
    assert len(rows) == 2
    by_packet = {row["packet_id"]: row for row in rows}
    reddit_record = by_packet[reddit.packet.packet_id]
    assert reddit_record["attachment_record_id"].startswith("ar_")
    assert reddit_record["attachment_record_physicalization"] == BRONZE_ATTACHMENT_RECORD_PHYSICALIZATION
    assert reddit_record["attachment_record_id"] != reddit_record["file_id"]
    assert reddit_record["body_ref_kind"] == "raw_packet_relative_path"
    assert reddit_record["body_ref"] == {
        "kind": "raw_packet_relative_path",
        "packet_id": reddit.packet.packet_id,
        "file_id": reddit_record["file_id"],
        "relative_packet_path": reddit_record["relative_packet_path"],
        "body_sha256": reddit_record["body_sha256"],
        "hash_basis": "raw_stored_bytes",
    }
    assert reddit_record["hash_basis"] == "raw_stored_bytes"
    assert reddit_record["payload_kind"] == "json_body"
    assert reddit_record["payload_kind_basis"] == "generic_body_classification"
    assert reddit_record["payload_schema_version"] is None
    assert reddit_record["raw_packet_manifest_version"] == "source_capture_packet_manifest_v1"
    assert reddit_record["replay_version_pins"] == {
        "raw_packet_manifest_version": "source_capture_packet_manifest_v1",
        "source_capture_obligation_contract_version": "core_spine_v0_data_capture_spine_obligation_contract_v0",
        "catalog_schema_version": BRONZE_CATALOG_SCHEMA_VERSION,
        "attachment_record_schema_version": BRONZE_ATTACHMENT_RECORD_SCHEMA_VERSION,
        "entry_serialization_version": ENTRY_SERIALIZATION_VERSION,
        "derivation_rule_version": DERIVATION_RULE_VERSION,
    }
    assert reddit_record["source_slice_ids"] == ["slice_01"]
    assert reddit_record["posture_summary"]["access_posture"]["value"] == "local_file_only"
    assert load_attachment_record_body(root, reddit_record) == json.dumps(
        {"body": "thread body"}, sort_keys=True
    ).encode("utf-8")

    record_path = _catalog_root(root) / reddit_record["stable_query_paths"]["by_attachment_record"]
    assert json.loads(record_path.read_text(encoding="utf-8")) == reddit_record
    packet_path = _catalog_root(root) / reddit_record["stable_query_paths"]["by_packet"]
    assert packet_path.is_file()
    packet_rows = [
        json.loads(line)
        for line in packet_path.read_text(encoding="utf-8").splitlines()
    ]
    assert packet_rows[0]["attachment_record_id"] == reddit_record["attachment_record_id"]
    wrong_ref_kind = dict(reddit_record)
    wrong_ref_kind["body_ref_kind"] = "sidecar_body"
    with pytest.raises(DataLakeRootError, match="body_ref_kind"):
        load_attachment_record_body(root, wrong_ref_kind)
    wrong_body_ref = dict(reddit_record)
    wrong_body_ref["body_ref"] = dict(reddit_record["body_ref"])
    wrong_body_ref["body_ref"]["file_id"] = "not_the_file"
    with pytest.raises(DataLakeRootError, match="body_ref mismatch"):
        load_attachment_record_body(root, wrong_body_ref)
    wrong_hash_basis = dict(reddit_record)
    wrong_hash_basis["hash_basis"] = "derived_record_bytes"
    with pytest.raises(DataLakeRootError, match="hash_basis"):
        load_attachment_record_body(root, wrong_hash_basis)
    wrong_path = dict(reddit_record)
    wrong_path["body_ref"] = dict(reddit_record["body_ref"])
    wrong_path["relative_packet_path"] = "raw/not_the_body.json"
    wrong_path["body_ref"]["relative_packet_path"] = wrong_path["relative_packet_path"]
    with pytest.raises(DataLakeRootError, match="path mismatch"):
        load_attachment_record_body(root, wrong_path)
    wrong_sha = dict(reddit_record)
    wrong_sha["body_ref"] = dict(reddit_record["body_ref"])
    wrong_sha["body_sha256"] = "0" * 64
    wrong_sha["body_ref"]["body_sha256"] = wrong_sha["body_sha256"]
    with pytest.raises(DataLakeRootError, match="sha256 mismatch"):
        load_attachment_record_body(root, wrong_sha)
    assert any(
        path.name.startswith("json_body__")
        for path in (_attachment_record_root(root) / "by_payload_kind").glob("*.jsonl")
    )
    assert any(
        path.name.startswith(f"{reddit_record['body_sha256']}__")
        for path in (_attachment_record_root(root) / "by_body_sha256").glob("*.jsonl")
    )
    assert by_packet[ig.packet.packet_id]["source_family"] == "instagram_creator"


def test_bronze_catalog_surfaces_full_gt_ratified_baseline(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _write_reddit_packet(root, tmp_path)

    rebuild = rebuild_catalog(root)
    inspect = inspect_catalog(root)
    catalog_manifest = _catalog_manifest(root)
    source_surfaces = _source_surface_payload(root)
    attachment_manifest = _attachment_record_manifest(root)
    census = catalog_coverage_census(root)

    for payload in (
        rebuild,
        inspect,
        catalog_manifest,
        source_surfaces,
        attachment_manifest,
        census,
    ):
        assert payload["bronze_baseline_status"] == BRONZE_BASELINE_STATUS
        assert "full_god_tier" in payload["bronze_baseline_semantics"]
        assert "no production-lake validation" in payload["bronze_baseline_semantics"]
        assert "no backend/engine selection" in payload["bronze_baseline_semantics"]
        assert "no erasure capability" in payload["bronze_baseline_semantics"]


def test_inspect_catalog_reports_missing_and_stale_generated_index(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    packet_id = _write_reddit_packet(root, tmp_path).packet.packet_id

    missing = inspect_catalog(root)
    assert missing["status"] == "issues_found"
    assert missing["missing_packets"] == [packet_id]

    assert rebuild_catalog(root)["status"] == "rebuilt"
    assert inspect_catalog(root)["status"] == "ok"

    entry_path = _catalog_root(root) / "by_packet" / f"{packet_id}.json"
    entry = json.loads(entry_path.read_text(encoding="utf-8"))
    entry["source_family"] = "stale"
    entry_path.write_text(json.dumps(entry, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    stale = inspect_catalog(root)
    assert stale["status"] == "issues_found"
    assert stale["stale_packets"] == [packet_id]
    assert f"by_packet/{packet_id}.json" in stale["stale_files"]


def test_inspect_catalog_reports_missing_and_stale_source_surfaces_file(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _write_reddit_packet(root, tmp_path)

    assert rebuild_catalog(root)["status"] == "rebuilt"
    source_surfaces = _catalog_root(root) / "source_surfaces.json"
    source_surfaces.unlink()

    missing = inspect_catalog(root)
    assert missing["status"] == "issues_found"
    assert "source_surfaces.json" in missing["missing_files"]

    assert rebuild_catalog(root)["status"] == "rebuilt"
    payload = _source_surface_payload(root)
    payload["source_surface_count"] = 999
    source_surfaces.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    stale = inspect_catalog(root)
    assert stale["status"] == "issues_found"
    assert "source_surfaces.json" in stale["stale_files"]


def test_source_surface_summary_counts_multiple_packets_and_documents_union(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _write_ig_reels_grid_packet(root, tmp_path, shortcode="REEL123", session_identity="ig-a")
    _write_ig_reels_grid_packet(root, tmp_path, shortcode=None, session_identity="ig-b")

    report = rebuild_catalog(root)

    row = {
        (item["source_family"], item["source_surface"]): item
        for item in report["source_surfaces"]
    }[("instagram_creator", "ig_reels_grid_dom_passive_json")]
    assert row["packet_count"] == 2
    assert row["facet_extractor"] == "registered"
    assert "instagram_shortcode" in row["facet_namespaces"]
    assert "session_identity" in row["facet_namespaces"]
    bucket_rows = [
        json.loads(line)
        for line in (_catalog_root(root) / row["by_source_surface_path"])
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert len(bucket_rows) == 2


def test_source_surface_summary_handles_empty_family_and_surface(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    src = tmp_path / "empty_surface_payload.json"
    src.write_text(json.dumps({"body": "empty surface"}, sort_keys=True), encoding="utf-8")
    write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family=" ",
        source_surface=" ",
        source_locator=known_fact("https://example.invalid/empty-surface"),
        decision_question="does an empty source surface remain inspectable?",
        capture_context="catalog fixture",
        session_identity="empty-session",
    )

    report = rebuild_catalog(root)

    row = report["source_surfaces"][0]
    assert row["source_family"] is None
    assert row["source_surface"] is None
    assert row["by_source_surface_path"] is None
    assert row["attachment_records_path"] is None
    assert row["packet_count"] == 1
    assert row["attachment_record_count"] == 1
    assert row["facet_extractor"] == "universal_only"
    assert set(row["facet_namespaces"]) == {"session_identity", "source_locator_sha256"}
    assert inspect_catalog(root)["status"] == "ok"


def test_inspect_catalog_reports_missing_and_stale_attachment_record_files(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _write_reddit_packet(root, tmp_path)

    assert rebuild_catalog(root)["status"] == "rebuilt"
    all_records = _attachment_record_root(root) / "all_attachment_records.jsonl"
    all_records.unlink()

    missing = inspect_catalog(root)
    assert missing["status"] == "issues_found"
    assert "attachment_records/all_attachment_records.jsonl" in missing["missing_files"]

    assert rebuild_catalog(root)["status"] == "rebuilt"
    record = _attachment_record_rows(root)[0]
    record_path = _attachment_record_root(root) / "by_attachment_record" / (
        f"{record['attachment_record_id']}.json"
    )
    payload = json.loads(record_path.read_text(encoding="utf-8"))
    payload["payload_kind"] = "stale"
    record_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    stale = inspect_catalog(root)
    assert stale["status"] == "issues_found"
    assert (
        f"attachment_records/by_attachment_record/{record['attachment_record_id']}.json"
        in stale["stale_files"]
    )

def test_rebuild_catalog_replaces_orphaned_generated_files_byte_identically(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _write_reddit_packet(root, tmp_path, body="alpha")
    _write_reddit_packet(root, tmp_path, body="beta")

    assert rebuild_catalog(root)["status"] == "rebuilt"
    catalog_root = _catalog_root(root)
    before = _snapshot(catalog_root)
    orphan = catalog_root / "junk" / "orphan.json"
    orphan.parent.mkdir(parents=True)
    orphan.write_text("{}", encoding="utf-8")

    dirty = inspect_catalog(root)
    assert dirty["status"] == "issues_found"
    assert "junk/orphan.json" in dirty["orphaned_files"]

    assert rebuild_catalog(root)["status"] == "rebuilt"
    assert not orphan.exists()
    assert _snapshot(catalog_root) == before


def test_rebuild_catalog_rejects_symlinked_catalog_component(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _write_reddit_packet(root, tmp_path)

    bronze_root = root.path / "indexes" / "derived_retrieval" / "bronze_catalog"
    if bronze_root.exists():
        shutil.rmtree(bronze_root)
    outside = tmp_path / "outside-catalog"
    outside.mkdir()
    try:
        bronze_root.symlink_to(outside, target_is_directory=True)
    except (NotImplementedError, OSError) as exc:
        pytest.skip(f"directory symlink unavailable on this platform: {exc}")

    with pytest.raises(DataLakeRootError, match="symlinked component"):
        rebuild_catalog(root)


def test_inspect_catalog_reports_generated_file_read_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _write_reddit_packet(root, tmp_path)
    assert rebuild_catalog(root)["status"] == "rebuilt"

    unreadable = _catalog_root(root) / "all_packets.jsonl"
    original_read_bytes = Path.read_bytes

    def fake_read_bytes(path: Path) -> bytes:
        if path == unreadable:
            raise OSError("simulated permission denied")
        return original_read_bytes(path)

    monkeypatch.setattr(Path, "read_bytes", fake_read_bytes)

    report = inspect_catalog(root)

    assert report["status"] == "issues_found"
    assert "all_packets.jsonl" in report["missing_files"]
    assert any(
        failure["path"].endswith("all_packets.jsonl")
        and "simulated permission denied" in failure["error"]
        for failure in report["catalog_read_failures"]
    )


def test_attachment_records_cover_multi_file_packet_without_file_id_as_record_id(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    json_src = tmp_path / "multi_payload.json"
    bin_src = tmp_path / "multi_payload.bin"
    json_src.write_text(json.dumps({"kind": "json"}, sort_keys=True), encoding="utf-8")
    bin_src.write_bytes(b"\xff\x00\xfe")
    result = write_local_source_capture_packet(
        data_root=root,
        input_files=[json_src, bin_src],
        source_family="future_creator_network",
        source_surface="future_binary_feed_v1",
        source_locator=known_fact("https://example.invalid/future/binary"),
        decision_question="can generic AR entries cover multiple body files?",
        capture_context="catalog fixture",
        session_identity="multi-file-session",
    )

    report = rebuild_catalog(root)

    assert report["attachment_record_count"] == 2
    rows = [
        row
        for row in _attachment_record_rows(root)
        if row["packet_id"] == result.packet.packet_id
    ]
    assert len(rows) == 2
    assert {row["file_id"] for row in rows} == {"file_01", "file_02"}
    assert {row["payload_kind"] for row in rows} == {"json_body", "binary_body"}
    assert all(row["attachment_record_id"] not in {"file_01", "file_02"} for row in rows)
    assert all(row["source_slice_ids"] == ["slice_01"] for row in rows)
    assert sorted(load_attachment_record_body(root, row) for row in rows) == sorted(
        [json.dumps({"kind": "json"}, sort_keys=True).encode("utf-8"), b"\xff\x00\xfe"]
    )

def test_catalog_coverage_census_is_observed_only_and_read_only(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _write_reddit_packet(root, tmp_path)
    _write_ig_reels_grid_packet(root, tmp_path)

    missing = catalog_coverage_census(root)

    assert missing["status"] == "issues_found"
    assert missing["catalog_status"] == "issues_found"
    assert missing["expected_packet_count"] == 2
    assert missing["indexed_packet_count"] == 0
    assert missing["attachment_record_count"] == 2
    assert missing["indexed_attachment_record_count"] == 0
    assert missing["source_surface_count"] == 2
    field_semantics = missing["field_semantics"]
    assert "raw-derived expected committed packet total" in field_semantics["expected_packet_count"]
    assert "readable generated by_packet" in field_semantics["indexed_packet_count"]
    assert "hash-checked raw packet member" in field_semantics["attachment_record_count"]
    assert "all_attachment_records.jsonl" in field_semantics["indexed_attachment_record_count"]
    assert "not a capture-lane registry" in missing["semantics"]
    assert "not generated-catalog currentness unless catalog_status is ok" in missing["semantics"]
    assert missing["catalog_issue_summary"]["issue_counts"]["missing_files"] > 0
    assert missing["catalog_issue_summary"]["issue_sample_limit"] == 25
    assert "missing_files" in missing["catalog_issue_summary"]["issue_samples"]
    assert "missing_files" not in set(missing["catalog_issue_summary"])
    assert not _catalog_root(root).exists()

    assert rebuild_catalog(root)["status"] == "rebuilt"
    catalog_root = _catalog_root(root)
    before = _snapshot(catalog_root)

    census = catalog_coverage_census(root)

    assert census["status"] == "ok"
    assert census["catalog_status"] == "ok"
    assert _snapshot(catalog_root) == before
    assert census["indexed_attachment_record_count"] == 2
    assert census["source_family_count"] == 2
    families = {row["source_family"]: row for row in census["source_families"]}
    assert families["instagram_creator"]["registered_surface_count"] == 1
    assert families["reddit"]["universal_only_surface_count"] == 1
    surfaces = {
        (row["source_family"], row["source_surface"]): row
        for row in census["source_surfaces"]
    }
    ig_surface = surfaces[("instagram_creator", "ig_reels_grid_dom_passive_json")]
    assert ig_surface["coverage_basis"] == "verified_raw_packet_manifests"
    assert ig_surface["catalog_query_paths"]["by_source_surface"].startswith(
        "by_source_surface/"
    )
    assert ig_surface["catalog_query_paths"][
        "attachment_records_by_source_surface"
    ].startswith("attachment_records/by_source_surface/")


def test_source_surface_catalog_rows_expose_packet_and_ar_query_rows(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _write_reddit_packet(root, tmp_path)
    ig = _write_ig_reels_grid_packet(root, tmp_path)

    assert rebuild_catalog(root)["status"] == "rebuilt"

    rows = source_surface_catalog_rows(
        root,
        source_family="instagram_creator",
        source_surface="ig_reels_grid_dom_passive_json",
    )

    assert rows["catalog_query_paths"]["by_source_surface"].startswith("by_source_surface/")
    assert rows["catalog_query_paths"]["attachment_records_by_source_surface"].startswith(
        "attachment_records/by_source_surface/"
    )
    assert [row["packet_id"] for row in rows["packet_rows"]] == [ig.packet.packet_id]
    assert [row["packet_id"] for row in rows["attachment_record_rows"]] == [
        ig.packet.packet_id
    ]
    assert rows["attachment_record_rows"][0]["source_family"] == "instagram_creator"
    assert load_attachment_record_body(root, rows["attachment_record_rows"][0])


def test_source_surface_catalog_rows_require_current_generated_catalog(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _write_ig_reels_grid_packet(root, tmp_path)

    with pytest.raises(DataLakeRootError, match="Bronze catalog is not current"):
        source_surface_catalog_rows(
            root,
            source_family="instagram_creator",
            source_surface="ig_reels_grid_dom_passive_json",
        )


def test_source_surface_catalog_rows_absent_surface_returns_consistent_shape(
    tmp_path: Path,
) -> None:
    # A current catalog with no matching (family, surface) bucket must return the SAME
    # key set as a populated result, so a downstream consumer that iterates
    # attachment_record_query_rows does not KeyError on the no-match path.
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _write_reddit_packet(root, tmp_path)
    assert rebuild_catalog(root)["status"] == "rebuilt"

    rows = source_surface_catalog_rows(
        root,
        source_family="instagram_creator",
        source_surface="surface_not_present_v0",
    )

    assert rows["catalog_query_paths"] == {}
    assert rows["packet_rows"] == []
    assert rows["attachment_record_query_rows"] == []
    assert rows["attachment_record_rows"] == []


def test_source_surface_catalog_rows_share_one_inspection_across_surfaces(
    tmp_path: Path, monkeypatch
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    calls = 0

    def fake_inspect(_root):  # noqa: ANN001
        nonlocal calls
        calls += 1
        return {"status": "ok", "source_surfaces": []}

    monkeypatch.setattr("data_lake.catalog.inspect_catalog", fake_inspect)
    inspection_cache: dict = {}

    source_surface_catalog_rows(
        root,
        source_family="family-a",
        source_surface="surface-a",
        inspection_cache=inspection_cache,
    )
    source_surface_catalog_rows(
        root,
        source_family="family-b",
        source_surface="surface-b",
        inspection_cache=inspection_cache,
    )

    assert calls == 1


def test_catalog_coverage_census_caps_issue_samples(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    for index in range(30):
        _write_reddit_packet(
            root,
            tmp_path,
            body=f"thread body {index}",
            session_identity=f"reddit-session-{index}",
            series_id=f"series-{index}",
        )

    census = catalog_coverage_census(root)
    summary = census["catalog_issue_summary"]

    assert census["status"] == "issues_found"
    assert summary["issue_counts"]["missing_files"] > summary["issue_sample_limit"]
    assert len(summary["issue_samples"]["missing_files"]) == summary["issue_sample_limit"]


def test_catalog_coverage_census_summarizes_stale_generated_files(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _write_reddit_packet(root, tmp_path)
    assert rebuild_catalog(root)["status"] == "rebuilt"

    source_surfaces = _catalog_root(root) / "source_surfaces.json"
    payload = _source_surface_payload(root)
    payload["source_surface_count"] = 999
    source_surfaces.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    census = catalog_coverage_census(root)
    summary = census["catalog_issue_summary"]

    assert census["status"] == "issues_found"
    assert summary["issue_counts"]["stale_files"] == 1
    assert summary["issue_samples"]["stale_files"] == ["source_surfaces.json"]


def test_catalog_coverage_census_separates_unknown_source_family_count(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    src = tmp_path / "unknown_family_payload.json"
    src.write_text(json.dumps({"body": "unknown family"}, sort_keys=True), encoding="utf-8")
    write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family=" ",
        source_surface=" ",
        source_locator=known_fact("https://example.invalid/unknown-family"),
        decision_question="does unknown family coverage remain explicit?",
        capture_context="catalog fixture",
        session_identity="unknown-family-session",
    )
    assert rebuild_catalog(root)["status"] == "rebuilt"

    census = catalog_coverage_census(root)

    assert census["source_family_count"] == 0
    assert census["unknown_source_family_packet_count"] == 1
    assert census["unknown_source_family_attachment_record_count"] == 1
    assert "non-null" in census["field_semantics"]["source_family_count"]
    assert "without a non-blank source_family" in census["field_semantics"][
        "unknown_source_family_packet_count"
    ]
    assert census["source_families"][0]["source_family"] is None
    assert census["source_families"][0]["packet_count"] == 1


def test_catalog_runner_rejects_census_rebuild_combination_without_writing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")

    with pytest.raises(SystemExit) as exc:
        catalog_runner.main(["--data-root", str(root.path), "--census", "--rebuild"])

    assert exc.value.code == 2
    assert "--census cannot be combined with --rebuild" in capsys.readouterr().err
    assert not _catalog_root(root).exists()


def test_catalog_runner_reports_root_resolution_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fake_resolve(*, explicit=None, **_kwargs):
        assert explicit == str(tmp_path / "missing")
        raise DataLakeRootError("missing root")

    monkeypatch.setattr(catalog_runner.DataLakeRoot, "resolve", staticmethod(fake_resolve))

    assert catalog_runner.main(["--data-root", str(tmp_path / "missing")]) == 2
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "error"
    assert "missing root" in report["error"]


def test_catalog_runner_reports_corrupt_raw_verified_read_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    result = _write_reddit_packet(root, tmp_path)
    packet_dir = Path(result.output_directory)
    manifest = json.loads((packet_dir / "manifest.json").read_text(encoding="utf-8"))
    preserved_path = packet_dir / manifest["preserved_files"][0]["relative_packet_path"]
    body = preserved_path.read_bytes()
    first_byte = b"0" if body[:1] != b"0" else b"1"
    preserved_path.write_bytes(first_byte + body[1:])

    def fake_resolve(*, explicit=None, **_kwargs):
        assert explicit == str(root.path)
        return root

    monkeypatch.setattr(catalog_runner.DataLakeRoot, "resolve", staticmethod(fake_resolve))

    assert catalog_runner.main(["--data-root", str(root.path), "--rebuild"]) == 2
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "error"
    assert "sha256 mismatch" in report["error"]


def test_catalog_runner_inspects_and_rebuilds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _write_reddit_packet(root, tmp_path)

    def fake_resolve(*, explicit=None, **_kwargs):
        assert explicit == str(root.path)
        return root

    monkeypatch.setattr(catalog_runner.DataLakeRoot, "resolve", staticmethod(fake_resolve))

    assert catalog_runner.main(["--data-root", str(root.path)]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "issues_found"

    assert catalog_runner.main(["--data-root", str(root.path), "--rebuild"]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "rebuilt"

    assert catalog_runner.main(["--data-root", str(root.path)]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "ok"


def test_catalog_runner_emits_read_only_coverage_census(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "forseti-data")
    _write_reddit_packet(root, tmp_path)

    def fake_resolve(*, explicit=None, **_kwargs):
        assert explicit == str(root.path)
        return root

    monkeypatch.setattr(catalog_runner.DataLakeRoot, "resolve", staticmethod(fake_resolve))

    assert catalog_runner.main(["--data-root", str(root.path), "--census"]) == 1
    missing = json.loads(capsys.readouterr().out)
    assert missing["census_kind"] == "bronze_catalog_observed_coverage_census"
    assert missing["catalog_status"] == "issues_found"
    assert not _catalog_root(root).exists()

    assert catalog_runner.main(["--data-root", str(root.path), "--rebuild"]) == 0
    capsys.readouterr()
    before = _snapshot(_catalog_root(root))

    assert catalog_runner.main(["--data-root", str(root.path), "--census"]) == 0
    census = json.loads(capsys.readouterr().out)
    assert census["catalog_status"] == "ok"
    assert census["source_surfaces"][0]["source_family"] == "reddit"
    assert _snapshot(_catalog_root(root)) == before
