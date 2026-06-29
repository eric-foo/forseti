from __future__ import annotations

import json
from pathlib import Path

import pytest

from data_lake.catalog import CATALOG_RELATIVE_ROOT, inspect_catalog, rebuild_catalog
from data_lake.root import DataLakeRoot, raw_shard
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


def _write_ig_reels_grid_packet(root: DataLakeRoot, tmp_path: Path):
    payload = {
        "creator_profile_snapshot": {
            "source_profile": "hyram",
            "numeric_id": "5802114508",
            "profile_grid_url": "https://www.instagram.com/hyram/reels/",
        },
        "joined_rows": [
            {
                "dom_row": {
                    "shortcode": "REEL123",
                    "kind": "reel",
                    "permalink_url": "https://www.instagram.com/reel/REEL123/",
                }
            }
        ],
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
        session_identity="ig-session",
    )


def _facet_rows(root: DataLakeRoot) -> list[dict]:
    rows: list[dict] = []
    for path in sorted((_catalog_root(root) / "by_facet").rglob("*.jsonl")):
        rows.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines())
    return rows


def test_rebuild_catalog_indexes_universal_and_ig_facets(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "orca-data")
    reddit = _write_reddit_packet(root, tmp_path, series_id="b2b-series")
    ig = _write_ig_reels_grid_packet(root, tmp_path)

    report = rebuild_catalog(root)

    assert report["status"] == "rebuilt"
    assert report["packet_count"] == 2
    assert inspect_catalog(root)["status"] == "ok"

    ig_pid = ig.packet.packet_id
    ig_entry = json.loads(
        (_catalog_root(root) / "by_packet" / f"{ig_pid}.json").read_text(encoding="utf-8")
    )
    assert ig_entry["raw_path"] == f"raw/{raw_shard(ig_pid)}/{ig_pid}"
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
