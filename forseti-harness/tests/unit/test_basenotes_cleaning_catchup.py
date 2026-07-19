"""Offline behavioral tests for the Basenotes Cleaning catch-up runner.

Mirror of the adjudicated Fragrantica catch-up suite (F-FRAG-001/002 conventions
inherited): S1 finds-own-backlog, S2 byte-unchanged rerun, output-shaping policy
tokens all in the obligation, S3 policy-bump re-derive, allowlist surface gate
(known other-lane surfaces acked out-of-scope; unknown surfaces visible and
unacknowledged), S4 damage fails loud without ack, S5 per-packet isolation,
F-ECR-001 reconcile visibility, and the CLI.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from cleaning.basenotes_lake import (
    BASENOTES_CLEANING_AUDIT_LANE,
    BASENOTES_CLEANING_SILVER_LANE,
)
from data_lake.consumption import find_acks
from data_lake.root import DataLakeRoot, DataLakeRootError
from runners import run_basenotes_cleaning_catchup as bn_runner
from runners.run_basenotes_mgt_capture import (
    PERSISTENT_CHROME_SLOT,
    run_basenotes_mgt_capture,
)
from runners.run_basenotes_cleaning_catchup import main, pending_packets, run_catchup
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet

_BASENOTES_SURFACE = "basenotes_product_page_user_cleared_persistent_chrome_current_window"
_FRAGRANTICA_SURFACE = "fragrantica_product_page_direct_http"
_FRAGRANTICA_INITIAL_VIEWPORT_SURFACE = "fragrantica_product_page_cloakbrowser_initial_viewport"
_FRAGRANTICA_DEEP_SCROLL_SURFACE = "fragrantica_product_page_cloakbrowser_deep_scroll_current_window"
_PARFUMO_DIRECT_SURFACE = "parfumo_product_page_direct_http"
_PARFUMO_RENDERED_SURFACE = "parfumo_product_page_chrome_extension_targeted_rendered_session"
_FIXTURE = (
    Path(__file__).resolve().parents[1]
    / "fixtures"
    / "basenotes"
    / "mojave_ghost_product_page.html"
)


def _commit_family_packet(
    data_root,
    tmp_path: Path,
    *,
    name: str = "bn",
    source_surface: str = _BASENOTES_SURFACE,
    body_text: str | None = None,
) -> str:
    body_path = tmp_path / f"{name}_body.html"
    body_path.write_text(
        body_text if body_text is not None else _FIXTURE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    metadata_path = tmp_path / f"{name}_metadata.json"
    metadata_path.write_text('{"capture_timestamp": "2026-06-30T00:00:00Z"}\n', encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=data_root,
        input_files=[body_path, metadata_path],
        source_family="fragrance_native_database",
        source_surface=source_surface,
        source_locator=known_fact(f"https://example.test/{name}"),
        decision_question="q",
        capture_context="basenotes cleaning catchup test",
    ).packet.packet_id


def _commit_content_packet(data_root, tmp_path: Path, *, name: str = "content") -> str:
    bundle = tmp_path / f"{name}_bundle"
    bundle.mkdir()
    (bundle / "browser_rendered_dom.html").write_text(
        _FIXTURE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (bundle / "browser_visible_text.txt").write_text(
        "Mojave Ghost by Byredo public product page with source-visible reviews. " * 12,
        encoding="utf-8",
    )
    source_url = "https://basenotes.com/fragrances/mojave-ghost-by-byredo.26143979"
    (bundle / "browser_snapshot_metadata.json").write_text(
        json.dumps(
            {
                "capture_timestamp": "2026-07-15T17:50:00Z",
                "requested_url": source_url,
                "final_url": source_url,
                "title": "Mojave Ghost by Byredo– Basenotes",
                "browser_channel": "user_chrome_extension",
                "headless": False,
                "persistent_user_session": True,
                "human_cleared_access_gate": True,
                "cookies_exported": False,
                "credentials_exported": False,
                "proxy_used": False,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    exit_code, summary_path = run_basenotes_mgt_capture(
        url=source_url,
        bundle_directory=bundle,
        output_root=tmp_path / f"{name}_output",
        data_root=data_root,
        capture_artifact_mode="content",
    )
    assert exit_code == 0
    summary = json.loads(Path(summary_path).read_text(encoding="utf-8"))
    return summary["packet_roles"][PERSISTENT_CHROME_SLOT]["packet_id"]


def _lake_tree_state(data_root) -> dict[str, str]:
    return {
        str(p.relative_to(data_root.path)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(data_root.path.rglob("*"))
        if p.is_file()
    }


def _tamper_packet(data_root, packet_id: str) -> None:
    preserved = next((data_root.path / "raw").glob(f"*/{packet_id}/raw/*"))
    preserved.write_bytes(b"tampered bytes\n")


def _corrupt_manifest(data_root, packet_id: str) -> None:
    container = data_root.find_packet(packet_id)
    assert container is not None
    (container / "manifest.json").write_text("{not-json\n", encoding="utf-8")


def test_catchup_finds_backlog_derives_and_acks(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(data_root, tmp_path)
    assert pending_packets(data_root=data_root) == [pid]

    results = run_catchup(data_root=data_root)
    assert len(results) == 1
    assert results[0]["packet_id"] == pid
    assert results[0]["status"] == "derived"
    audit_record_id = results[0]["audit_record_id"]
    assert results[0]["silver_count"] >= 1

    audit_path = next(
        (data_root.path / "derived").glob(f"*/{pid}/{BASENOTES_CLEANING_AUDIT_LANE}/*")
    )
    assert audit_path.name == audit_record_id
    silver_paths = list(
        (data_root.path / "derived").glob(f"*/{pid}/{BASENOTES_CLEANING_SILVER_LANE}/*")
    )
    assert len(silver_paths) == results[0]["silver_count"]

    acks = find_acks(data_root, raw_anchor=pid, ack_namespace=BASENOTES_CLEANING_AUDIT_LANE)
    assert len(acks) == 1
    obligation = acks[0]["obligation"]
    assert obligation["consumer"] == "basenotes_cleaning_catchup"
    evidence_by_kind = {entry["kind"]: entry for entry in acks[0]["evidence"]}
    assert evidence_by_kind["derived_record"]["record_id"] == audit_record_id
    assert evidence_by_kind["silver_records"]["count"] == results[0]["silver_count"]
    assert pending_packets(data_root=data_root) == []


def test_output_shaping_policy_tokens_are_in_obligation() -> None:
    # F-FRAG-001 convention: every output-shaping pre-existing constant is in the
    # envelope, so a change to any of them re-fingerprints and re-surfaces work.
    obligation = bn_runner._packet_obligation()
    assert obligation["cleaning_core_version"] == bn_runner.CLEANING_CORE_VERSION
    assert obligation["projection_method"] == bn_runner.BASENOTES_PROJECTION_METHOD
    assert obligation["projection_version"] == bn_runner.BASENOTES_PROJECTION_VERSION
    assert obligation["projection_certification"] == bn_runner.BASENOTES_PROJECTION_CERTIFICATION
    assert obligation["content_parser_version"] == bn_runner.BASENOTES_PARSER_VERSION
    assert obligation["cleaning_audit_pack_schema_version"] == bn_runner.CLEANING_AUDIT_PACK_SCHEMA_VERSION
    assert obligation["audit_pack_schema_version"] == bn_runner.BASENOTES_AUDIT_PACK_PRODUCER_SCHEMA_VERSION
    assert obligation["silver_vault_record_schema_version"] == bn_runner.SILVER_VAULT_RECORD_SCHEMA_VERSION
    assert obligation["silver_schema_version"] == bn_runner.BASENOTES_SILVER_PRODUCER_SCHEMA_VERSION
    assert obligation["cleaning_method_id"] == bn_runner.BASENOTES_CLEANING_METHOD_ID
    assert obligation["text_normalization_rule"] == bn_runner.TEXT_NORMALIZATION_RULE
    assert obligation["rating_metric_residual"] == bn_runner.BASENOTES_RATING_METRIC_RESIDUAL


def test_catchup_second_run_is_byte_unchanged_noop(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_family_packet(data_root, tmp_path)
    assert [r["status"] for r in run_catchup(data_root=data_root)] == ["derived"]

    before = _lake_tree_state(data_root)
    assert run_catchup(data_root=data_root) == []
    assert _lake_tree_state(data_root) == before


def test_content_packet_catchup_derives_without_dom_and_is_idempotent(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_content_packet(data_root, tmp_path)
    packet = data_root.load_raw_packet(pid)
    names = {
        Path(item["relative_packet_path"]).name
        for item in packet.manifest["preserved_files"]
    }
    assert not any(name.endswith("_browser_rendered_dom.html") for name in names)
    assert not any(name.endswith("_browser_visible_text.txt") for name in names)

    assert [row["status"] for row in run_catchup(data_root=data_root)] == ["derived"]
    before = _lake_tree_state(data_root)
    assert run_catchup(data_root=data_root) == []
    assert _lake_tree_state(data_root) == before


def test_damaged_content_record_fails_without_ack(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_content_packet(data_root, tmp_path)
    packet = data_root.load_raw_packet(pid)
    content_item = next(
        item
        for item in packet.manifest["preserved_files"]
        if item["relative_packet_path"].replace("\\", "/").endswith(
            "content_record.json"
        )
    )
    (packet.container / content_item["relative_packet_path"]).write_bytes(
        b"tampered content record\n"
    )

    results = run_catchup(data_root=data_root)
    assert [row["status"] for row in results] == ["derive_failed"]
    assert find_acks(
        data_root,
        raw_anchor=pid,
        ack_namespace=BASENOTES_CLEANING_AUDIT_LANE,
    ) == []


def test_out_of_scope_policy_change_re_surfaces_previous_ack(tmp_path, monkeypatch) -> None:
    # F-IGRC-002 convention: the surface gate is fingerprinted policy — removing a
    # surface from the known-out-of-scope set must re-surface its packets as
    # visible unsupported_surface instead of leaving the old ack trusted.
    from cleaning.basenotes_lake import BASENOTES_CLEANING_AUDIT_LANE as _audit_lane
    from data_lake.consumption import find_acks as _find_acks

    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(
        data_root,
        tmp_path,
        name="frag",
        source_surface=_FRAGRANTICA_SURFACE,
        body_text="<html><body>a fragrantica page</body></html>",
    )
    assert [r["status"] for r in run_catchup(data_root=data_root)] == [
        "acked_no_cleanable_content"
    ]

    monkeypatch.setattr(bn_runner, "_KNOWN_OUT_OF_SCOPE_SURFACES", frozenset())
    second = run_catchup(data_root=data_root)

    assert [r["status"] for r in second] == ["unsupported_surface"]
    assert second[0]["source_surface"] == _FRAGRANTICA_SURFACE
    assert len(_find_acks(data_root, raw_anchor=pid, ack_namespace=_audit_lane)) == 1


def test_policy_bump_resurfaces_and_rederives(tmp_path, monkeypatch) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(data_root, tmp_path)
    original_version = bn_runner.CLEANING_CORE_VERSION

    first = run_catchup(data_root=data_root)
    assert [r["status"] for r in first] == ["derived"]
    assert run_catchup(data_root=data_root) == []

    monkeypatch.setattr(bn_runner, "CLEANING_CORE_VERSION", "test-cleaning-vnext")
    third = run_catchup(data_root=data_root)
    assert [r["status"] for r in third] == ["derived"]
    assert third[0]["audit_record_id"] != first[0]["audit_record_id"]

    acks = find_acks(data_root, raw_anchor=pid, ack_namespace=BASENOTES_CLEANING_AUDIT_LANE)
    assert len(acks) == 2
    assert {ack["obligation"]["cleaning_core_version"] for ack in acks} == {
        original_version,
        "test-cleaning-vnext",
    }
    assert run_catchup(data_root=data_root) == []


@pytest.mark.parametrize(
    ("surface", "name"),
    [
        (_FRAGRANTICA_SURFACE, "fragrantica_direct"),
        (_FRAGRANTICA_INITIAL_VIEWPORT_SURFACE, "fragrantica_initial_viewport"),
        (_FRAGRANTICA_DEEP_SCROLL_SURFACE, "fragrantica_deep_scroll"),
        (_PARFUMO_DIRECT_SURFACE, "parfumo_direct"),
        (_PARFUMO_RENDERED_SURFACE, "parfumo_rendered"),
    ],
)
def test_shared_family_known_other_surface_acked_out_of_scope_never_derived(
    tmp_path, surface: str, name: str
) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    other = _commit_family_packet(
        data_root,
        tmp_path,
        name=name,
        source_surface=surface,
        body_text=f"<html><body>a {name} page</body></html>",
    )
    bn = _commit_family_packet(data_root, tmp_path)

    results = run_catchup(data_root=data_root)
    by_packet = {r["packet_id"]: r for r in results}
    assert by_packet[bn]["status"] == "derived"
    assert by_packet[other]["status"] == "acked_no_cleanable_content"
    assert by_packet[other]["source_surface"] == surface

    assert list((data_root.path / "derived").glob(f"*/{other}/*")) == []
    acks = find_acks(data_root, raw_anchor=other, ack_namespace=BASENOTES_CLEANING_AUDIT_LANE)
    assert len(acks) == 1
    assert acks[0]["evidence"] == [
        {
            "kind": "no_cleanable_content_for_surface",
            "raw_anchor": other,
            "source_surface": surface,
            "basis": "known_non_basenotes_source_surface",
        }
    ]
    assert run_catchup(data_root=data_root) == []


def test_unknown_family_surface_fails_loud_without_ack(tmp_path) -> None:
    # F-FRAG-002 convention: an unknown surface is a visible, unacknowledged
    # backlog item, never an open-world ack that could pre-close a future lane.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(
        data_root,
        tmp_path,
        name="future",
        source_surface="future_fragrance_surface_v1",
        body_text="<html><body>future surface</body></html>",
    )

    results = run_catchup(data_root=data_root)
    assert len(results) == 1
    assert results[0]["packet_id"] == pid
    assert results[0]["status"] == "unsupported_surface"
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=BASENOTES_CLEANING_AUDIT_LANE) == []

    second = run_catchup(data_root=data_root)
    assert [r["status"] for r in second] == ["unsupported_surface"]
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=BASENOTES_CLEANING_AUDIT_LANE) == []


def test_damaged_packet_fails_loud_without_ack_and_resurfaces(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(data_root, tmp_path)
    _tamper_packet(data_root, pid)

    results = run_catchup(data_root=data_root)
    assert [r["status"] for r in results] == ["derive_failed"]
    assert results[0]["error"]
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=BASENOTES_CLEANING_AUDIT_LANE) == []
    assert list((data_root.path / "derived").glob(f"*/{pid}/*")) == []

    second = run_catchup(data_root=data_root)
    assert [r["status"] for r in second] == ["derive_failed"]
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=BASENOTES_CLEANING_AUDIT_LANE) == []


def test_per_packet_failure_is_isolated(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    good = _commit_family_packet(data_root, tmp_path, name="good")
    bad = _commit_family_packet(data_root, tmp_path, name="bad")
    _tamper_packet(data_root, bad)

    results = run_catchup(data_root=data_root)
    by_packet = {r["packet_id"]: r["status"] for r in results}
    assert by_packet == {good: "derived", bad: "derive_failed"}
    assert len(find_acks(data_root, raw_anchor=good, ack_namespace=BASENOTES_CLEANING_AUDIT_LANE)) == 1
    assert find_acks(data_root, raw_anchor=bad, ack_namespace=BASENOTES_CLEANING_AUDIT_LANE) == []


def test_corrupt_manifest_reconcile_failure_still_processes_healthy_packet(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    bad = _commit_family_packet(data_root, tmp_path, name="bad")
    good = _commit_family_packet(data_root, tmp_path, name="good")
    _corrupt_manifest(data_root, bad)

    results = run_catchup(data_root=data_root)
    by_packet = {r["packet_id"]: r for r in results}
    assert by_packet[bad]["status"] == "availability_reconcile_failed"
    assert by_packet[good]["status"] == "derived"
    assert find_acks(data_root, raw_anchor=bad, ack_namespace=BASENOTES_CLEANING_AUDIT_LANE) == []


def test_pending_packets_blocks_on_corrupt_manifest_reconcile_failure(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(data_root, tmp_path)
    _corrupt_manifest(data_root, pid)

    with pytest.raises(
        DataLakeRootError, match="availability reconcile failed before pending check"
    ):
        pending_packets(data_root=data_root)


def test_check_cli_prints_pending_count(tmp_path, monkeypatch, capsys) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_family_packet(data_root, tmp_path)

    def fake_resolve(cls, *, explicit=None, **_kwargs):  # noqa: ANN001
        assert explicit is None
        return data_root

    monkeypatch.setattr(DataLakeRoot, "resolve", classmethod(fake_resolve))
    assert main(["--check"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "1\n"

    assert main(["--run"]) == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out.strip())["status"] == "derived"

    assert main(["--check"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "0\n"
