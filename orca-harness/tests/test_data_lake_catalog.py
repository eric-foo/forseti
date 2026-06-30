from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from data_lake.catalog import (
    BRONZE_CATALOG_SCHEMA_VERSION,
    CATALOG_RELATIVE_ROOT,
    inspect_catalog,
    rebuild_catalog,
)
from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard
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


def _source_surface_rows(root: DataLakeRoot) -> list[dict]:
    return _source_surface_payload(root)["source_surfaces"]


def test_rebuild_catalog_indexes_universal_and_ig_facets(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    reddit = _write_reddit_packet(root, tmp_path, series_id="b2b-series")
    ig = _write_ig_reels_grid_packet(root, tmp_path)

    report = rebuild_catalog(root)

    assert report["status"] == "rebuilt"
    assert report["catalog_schema_version"] == BRONZE_CATALOG_SCHEMA_VERSION
    assert report["packet_count"] == 2
    assert report["source_surface_count"] == 2
    assert inspect_catalog(root)["status"] == "ok"

    ig_pid = ig.packet.packet_id
    ig_entry = json.loads(
        (_catalog_root(root) / "by_packet" / f"{ig_pid}.json").read_text(encoding="utf-8")
    )
    assert ig_entry["raw_path"] == f"raw/{raw_shard(ig_pid)}/{ig_pid}"
    assert ig_entry["catalog_schema_version"] == BRONZE_CATALOG_SCHEMA_VERSION
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
    assert "not capture_support" in surface_payload["completeness"]
    assert "neither value claims" in surface_payload["field_semantics"]["facet_extractor"]
    assert "union" in surface_payload["field_semantics"]["facet_namespaces"]
    assert surface_payload["stable_query_paths"]["all_packets"] == "all_packets.jsonl"
    generated_surface_rows = {
        (row["source_family"], row["source_surface"]): row
        for row in surface_payload["source_surfaces"]
    }
    assert generated_surface_rows == report_surface_rows
    reddit_surface_path = report_surface_rows[("reddit", "r/B2BMarketing")][
        "by_source_surface_path"
    ]
    assert reddit_surface_path.startswith("by_source_surface/")
    assert (_catalog_root(root) / reddit_surface_path).is_file()
    assert report_surface_rows[("reddit", "r/B2BMarketing")]["packet_count"] == 1
    assert (
        report_surface_rows[("reddit", "r/B2BMarketing")]["facet_extractor"]
        == "universal_only"
    )
    ig_surface = report_surface_rows[("instagram_creator", "ig_reels_grid_dom_passive_json")]
    assert ig_surface["by_source_surface_path"].startswith("by_source_surface/")
    assert (_catalog_root(root) / ig_surface["by_source_surface_path"]).is_file()
    assert ig_surface["packet_count"] == 1
    assert ig_surface["facet_extractor"] == "registered"
    assert {
        "instagram_creator_handle",
        "instagram_creator_numeric_id",
        "instagram_shortcode",
    } <= set(ig_surface["facet_namespaces"])


def test_rebuild_catalog_marks_unknown_future_surface_universal_only(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
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
    assert future_row["packet_count"] == 1
    assert future_row["facet_extractor"] == "universal_only"
    assert {
        "source_family",
        "source_surface",
        "session_identity",
        "source_locator_sha256",
    } <= set(future_row["facet_namespaces"])


def test_inspect_catalog_reports_missing_and_stale_generated_index(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
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
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
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
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
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
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
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
    assert row["packet_count"] == 1
    assert row["facet_extractor"] == "universal_only"
    assert set(row["facet_namespaces"]) == {"session_identity", "source_locator_sha256"}
    assert inspect_catalog(root)["status"] == "ok"


def test_rebuild_catalog_replaces_orphaned_generated_files_byte_identically(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
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
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
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
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
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
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
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
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
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
