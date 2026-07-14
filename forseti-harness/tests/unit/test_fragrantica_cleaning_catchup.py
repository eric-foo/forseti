"""Offline behavioral tests for the Fragrantica Cleaning catch-up runner.

No network, no credentials. Commits real packets into a temp lake and asserts the
handoff's S-signals: the runner finds its own backlog (S1), does nothing twice with a
byte-unchanged lake tree (S2), re-surfaces on a cleaning-policy bump (S3 — the raw
packet is immutable and the derivation consumes no committed derived records, so the
policy tokens are the lane's ONLY growable input class), fails loud without acking on
a damaged packet (S4), isolates per-packet failure (S5), and honors the seam
boundaries (S6: registered ack namespace, committed anchors only, non-raising
obligation) — plus the shared-family surface gate: known basenotes/parfumo-surface
packets are acknowledged with explicit out-of-scope evidence, never derived and never
left re-surfacing forever, while unknown future surfaces stay unacknowledged.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from cleaning.fragrantica_lake import (
    FRAGRANTICA_CLEANING_AUDIT_LANE,
    FRAGRANTICA_CLEANING_SILVER_LANE,
)
from data_lake.consumption import find_acks
from data_lake.root import DataLakeRoot, DataLakeRootError
from runners import run_fragrantica_cleaning_catchup as frag_runner
from runners.run_fragrantica_cleaning_catchup import main, pending_packets, run_catchup
from source_capture.models import (
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
    unknown_with_reason,
)
from source_capture.writer import write_local_source_capture_packet

_CAPTURE_TIME = "2026-06-28T18:57:58Z"
_BASENOTES_SURFACE = "basenotes_product_page_cloakbrowser_deep_scroll_current_window"
_PARFUMO_DIRECT_SURFACE = "parfumo_product_page_direct_http"
_PARFUMO_RENDERED_SURFACE = "parfumo_product_page_chrome_extension_targeted_rendered_session"


def _fragrantica_html() -> str:
    return """
    <html><head>
      <link rel="canonical" href="https://www.fragrantica.com/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html"/>
      <title>Baccarat Rouge 540 Maison Francis Kurkdjian perfume</title>
    </head><body>
      <div id="perfume-description-content" itemprop="description">
        <p><b>Baccarat Rouge 540</b> by <b>Maison Francis Kurkdjian</b> is a fragrance. Baccarat Rouge 540 was launched in 2015.</p>
      </div>
      <p itemprop="aggregateRating"><span itemprop="ratingValue">3.76</span><span itemprop="bestRating">5</span><span itemprop="ratingCount" content="28808">28,808</span></p>
      <span>Reviews (<span>3.9K</span>)</span>
      <button data-tab="all-reviews" data-active="true">All reviews by date</button>
      <div class="review-tab-panel" id="all-reviews">
        <div id="parent3090334" class="cell tw-review-card tw-gradient-rose" itemprop="review" itemscope>
          <user-perfume-votes-new :perfume-votes="{&quot;rating&quot;:5,&quot;winter&quot;:0,&quot;spring&quot;:0,&quot;summer&quot;:0,&quot;autumn&quot;:0,&quot;day&quot;:0,&quot;night&quot;:0,&quot;longevity&quot;:3,&quot;sillage&quot;:2,&quot;gender&quot;:&quot;female_unisex&quot;,&quot;relation&quot;:&quot;have&quot;}"></user-perfume-votes-new>
          <meta itemprop="name" content="Rimazy"/>
          <span itemprop="datePublished" content="2026-06-25">06\\25\\26 18:41</span>
          <div id="review_3090334"><p>This perfume died young.</p></div>
          <vote-buttons-new initial-status="neutral" item-id="33519" comment-id="3090334" vote-for="perfumeReview"></vote-buttons-new>
          <share-new path="/perfume/Maison-Francis-Kurkdjian/Baccarat-Rouge-540-33519.html?ccid=3090334#focus-zone"></share-new>
        </div>
        <reviews-infinity-new :perfume-id="33519" sentiment="all" :is-logged="false" login-url="/board/login.php"
          :lang-strings="{&quot;loginPromptMessage&quot;:&quot;Sign in to access the full review archive&quot;}">
        </reviews-infinity-new>
      </div>
    </body></html>
    """


def _commit_family_packet(
    data_root,
    tmp_path: Path,
    *,
    name: str = "frag",
    source_surface: str = "fragrantica_product_page_direct_http",
    body_text: str | None = None,
) -> str:
    body_path = tmp_path / f"{name}_body.bin"
    body_path.write_text(
        body_text if body_text is not None else _fragrantica_html(), encoding="utf-8"
    )
    metadata_path = tmp_path / f"{name}_metadata.json"
    metadata_path.write_text('{"status": 200}\n', encoding="utf-8")
    timing = PacketTiming(
        source_publication_or_event=unknown_with_reason("fixture does not supply source event timing"),
        source_edit_or_version=unknown_with_reason("fixture does not supply edit timing"),
        capture_time=known_fact(_CAPTURE_TIME),
        recapture_time=not_applicable("first capture"),
        cutoff_posture=unknown_with_reason("test fixture has no decision cutoff"),
    )
    source_slice = SourceCaptureSlice(
        slice_id="slice_01",
        locator=known_fact(f"https://example.test/{name}"),
        timing=timing,
        access_posture=known_fact("direct HTTP fixture supplied"),
        archive_history_posture=not_attempted("archive not queried"),
        media_modality_posture=not_attempted("linked media not fetched"),
        re_capture_relationship=not_applicable("first capture"),
        limitations=[],
        warning_notes=[],
        preserved_file_ids=["file_01", "file_02"],
    )
    return write_local_source_capture_packet(
        data_root=data_root,
        input_files=[body_path, metadata_path],
        source_family="fragrance_native_database",
        source_surface=source_surface,
        source_locator=known_fact(f"https://example.test/{name}"),
        decision_question="q",
        capture_context="fragrantica cleaning catchup test",
        source_slices=[source_slice],
    ).packet.packet_id


def _lake_tree_state(data_root) -> dict[str, str]:
    """Every file under the lake root -> sha256, for byte-unchanged idempotence asserts."""
    return {
        str(p.relative_to(data_root.path)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(data_root.path.rglob("*"))
        if p.is_file()
    }


def _tamper_packet(data_root, packet_id: str) -> None:
    """Corrupt a committed packet's preserved bytes so the verified read fails closed."""
    preserved = next((data_root.path / "raw").glob(f"*/{packet_id}/raw/*"))
    preserved.write_bytes(b"tampered bytes\n")


def _corrupt_manifest(data_root, packet_id: str) -> None:
    container = data_root.find_packet(packet_id)
    assert container is not None
    (container / "manifest.json").write_text("{not-json\n", encoding="utf-8")


def test_catchup_finds_backlog_derives_and_acks(tmp_path) -> None:
    # S1: a committed packet nobody pointed a per-packet command at is discovered
    # and derived by ONE catch-up run, with the derivation as ack evidence.
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
        (data_root.path / "derived").glob(f"*/{pid}/{FRAGRANTICA_CLEANING_AUDIT_LANE}/*")
    )
    assert audit_path.name == audit_record_id
    silver_paths = list(
        (data_root.path / "derived").glob(f"*/{pid}/{FRAGRANTICA_CLEANING_SILVER_LANE}/*")
    )
    assert len(silver_paths) == results[0]["silver_count"]

    acks = find_acks(data_root, raw_anchor=pid, ack_namespace=FRAGRANTICA_CLEANING_AUDIT_LANE)
    assert len(acks) == 1
    obligation = acks[0]["obligation"]
    assert obligation["consumer"] == "fragrantica_cleaning_catchup"
    assert obligation["cleaning_core_version"] == frag_runner.CLEANING_CORE_VERSION
    assert obligation["projection_version"] == frag_runner.FRAGRANTICA_PROJECTION_VERSION
    evidence_by_kind = {entry["kind"]: entry for entry in acks[0]["evidence"]}
    assert evidence_by_kind["derived_record"]["record_id"] == audit_record_id
    assert evidence_by_kind["derived_record"]["lane"] == FRAGRANTICA_CLEANING_AUDIT_LANE
    assert evidence_by_kind["silver_records"]["count"] == results[0]["silver_count"]
    assert pending_packets(data_root=data_root) == []


def test_catchup_second_run_is_byte_unchanged_noop(tmp_path) -> None:
    # S2: an immediate second run over the unchanged lake emits ZERO status entries
    # and performs ZERO lake writes (byte-unchanged tree, not merely no failures).
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_family_packet(data_root, tmp_path)
    assert [r["status"] for r in run_catchup(data_root=data_root)] == ["derived"]

    before = _lake_tree_state(data_root)
    assert run_catchup(data_root=data_root) == []
    assert _lake_tree_state(data_root) == before


def test_output_shaping_policy_tokens_are_in_obligation() -> None:
    obligation = frag_runner._packet_obligation()

    assert obligation["projection_method"] == frag_runner.FRAGRANTICA_PROJECTION_METHOD
    assert obligation["projection_version"] == frag_runner.FRAGRANTICA_PROJECTION_VERSION
    assert obligation["projection_certification"] == frag_runner.FRAGRANTICA_PROJECTION_CERTIFICATION
    assert obligation["cleaning_audit_pack_schema_version"] == (
        frag_runner.CLEANING_AUDIT_PACK_SCHEMA_VERSION
    )
    assert obligation["silver_vault_record_schema_version"] == (
        frag_runner.SILVER_VAULT_RECORD_SCHEMA_VERSION
    )
    assert obligation["cleaning_method_id"] == frag_runner.FRAGRANTICA_CLEANING_METHOD_ID
    assert obligation["review_text_normalization_rule"] == (
        frag_runner.REVIEW_TEXT_NORMALIZATION_RULE
    )
    assert obligation["review_vote_carry_rule"] == frag_runner.REVIEW_VOTE_CARRY_RULE
    assert obligation["review_vote_policy_version"] == (
        frag_runner.FRAGRANTICA_REVIEW_VOTE_POLICY_VERSION
    )
    assert obligation["review_vote_metric_specs"] == [
        list(spec) for spec in frag_runner._REVIEW_VOTE_METRIC_SPECS
    ]


def test_policy_bump_resurfaces_and_rederives(tmp_path, monkeypatch) -> None:
    # S3: the policy tokens are the lane's only re-trigger inputs (immutable raw,
    # no derived-record inputs). Bumping one re-surfaces the SAME anchor, derives
    # a FRESH audit sibling under the new policy, and re-acks under the new
    # fingerprint; the run after that is silent again.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(data_root, tmp_path)
    original_version = frag_runner.CLEANING_CORE_VERSION

    first = run_catchup(data_root=data_root)
    assert [r["status"] for r in first] == ["derived"]
    assert run_catchup(data_root=data_root) == []

    monkeypatch.setattr(frag_runner, "CLEANING_CORE_VERSION", "test-cleaning-vnext")
    third = run_catchup(data_root=data_root)
    assert [r["status"] for r in third] == ["derived"]
    assert third[0]["audit_record_id"] != first[0]["audit_record_id"]  # fresh sibling

    acks = find_acks(data_root, raw_anchor=pid, ack_namespace=FRAGRANTICA_CLEANING_AUDIT_LANE)
    assert len(acks) == 2
    assert {ack["obligation"]["cleaning_core_version"] for ack in acks} == {
        original_version,
        "test-cleaning-vnext",
    }
    assert run_catchup(data_root=data_root) == []


def test_cleaning_method_policy_bump_resurfaces_and_rederives(tmp_path, monkeypatch) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(data_root, tmp_path)
    original_method = frag_runner.FRAGRANTICA_CLEANING_METHOD_ID

    first = run_catchup(data_root=data_root)
    assert [r["status"] for r in first] == ["derived"]
    assert run_catchup(data_root=data_root) == []

    monkeypatch.setattr(frag_runner, "FRAGRANTICA_CLEANING_METHOD_ID", "method-vnext")
    third = run_catchup(data_root=data_root)
    assert [r["status"] for r in third] == ["derived"]
    assert third[0]["audit_record_id"] != first[0]["audit_record_id"]

    acks = find_acks(data_root, raw_anchor=pid, ack_namespace=FRAGRANTICA_CLEANING_AUDIT_LANE)
    assert {ack["obligation"]["cleaning_method_id"] for ack in acks} == {
        original_method,
        "method-vnext",
    }


def test_review_vote_policy_bump_resurfaces_and_rederives(tmp_path, monkeypatch) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(data_root, tmp_path)
    original_policy = frag_runner.FRAGRANTICA_REVIEW_VOTE_POLICY_VERSION

    first = run_catchup(data_root=data_root)
    assert [r["status"] for r in first] == ["derived"]
    assert run_catchup(data_root=data_root) == []

    monkeypatch.setattr(
        frag_runner,
        "FRAGRANTICA_REVIEW_VOTE_POLICY_VERSION",
        "fragrantica_review_vote_valid_ordinal_vnext",
    )
    third = run_catchup(data_root=data_root)
    assert [r["status"] for r in third] == ["derived"]
    assert third[0]["audit_record_id"] != first[0]["audit_record_id"]

    acks = find_acks(data_root, raw_anchor=pid, ack_namespace=FRAGRANTICA_CLEANING_AUDIT_LANE)
    assert {ack["obligation"]["review_vote_policy_version"] for ack in acks} == {
        original_policy,
        "fragrantica_review_vote_valid_ordinal_vnext",
    }


@pytest.mark.parametrize(
    ("surface", "name"),
    [
        (_BASENOTES_SURFACE, "basenotes"),
        (_PARFUMO_DIRECT_SURFACE, "parfumo_direct"),
        (_PARFUMO_RENDERED_SURFACE, "parfumo_rendered"),
    ],
)
def test_shared_family_known_other_surface_acked_out_of_scope_never_derived(
    tmp_path, surface: str, name: str
) -> None:
    # Surface gate: a known non-Fragrantica packet in the SAME family is acknowledged
    # with explicit out-of-scope evidence — never handed to the Fragrantica
    # deriver, never left re-surfacing forever — and stays fully available to its
    # own lane's namespace (zero cleaning records written under it).
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    other = _commit_family_packet(
        data_root,
        tmp_path,
        name=name,
        source_surface=surface,
        body_text=f"<html><body>a {name} page</body></html>",
    )
    frag = _commit_family_packet(data_root, tmp_path)

    results = run_catchup(data_root=data_root)
    by_packet = {r["packet_id"]: r for r in results}
    assert by_packet[frag]["status"] == "derived"
    assert by_packet[other]["status"] == "acked_no_cleanable_content"
    assert by_packet[other]["source_surface"] == surface

    # no cleaning records under the out-of-scope packet, but its ack exists with
    # the explicit out-of-scope evidence
    assert list((data_root.path / "derived").glob(f"*/{other}/*")) == []
    acks = find_acks(data_root, raw_anchor=other, ack_namespace=FRAGRANTICA_CLEANING_AUDIT_LANE)
    assert len(acks) == 1
    assert acks[0]["evidence"] == [
        {
            "kind": "no_cleanable_content_for_surface",
            "raw_anchor": other,
            "source_surface": surface,
            "basis": "known_non_fragrantica_source_surface",
        }
    ]

    assert run_catchup(data_root=data_root) == []


def test_out_of_scope_policy_change_re_surfaces_previous_ack(tmp_path, monkeypatch) -> None:
    # F-IGRC-002 convention: the surface gate is fingerprinted policy — removing a
    # surface from the known-out-of-scope set must re-surface its packets as
    # visible unsupported_surface instead of leaving the old ack trusted.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(
        data_root,
        tmp_path,
        name="parfumo",
        source_surface="parfumo_product_page_direct_http",
        body_text="<html><body>a parfumo page</body></html>",
    )
    assert [r["status"] for r in run_catchup(data_root=data_root)] == [
        "acked_no_cleanable_content"
    ]

    monkeypatch.setattr(frag_runner, "_KNOWN_OUT_OF_SCOPE_SURFACES", frozenset())
    second = run_catchup(data_root=data_root)

    assert [r["status"] for r in second] == ["unsupported_surface"]
    assert second[0]["source_surface"] == "parfumo_product_page_direct_http"
    assert (
        len(find_acks(data_root, raw_anchor=pid, ack_namespace=FRAGRANTICA_CLEANING_AUDIT_LANE))
        == 1
    )


def test_unknown_family_surface_fails_loud_without_ack(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(
        data_root,
        tmp_path,
        name="future",
        source_surface="future_fragrance_surface",
        body_text="<html><body>a future family surface</body></html>",
    )

    results = run_catchup(data_root=data_root)
    assert results == [
        {
            "packet_id": pid,
            "status": "unsupported_surface",
            "source_surface": "future_fragrance_surface",
            "error": "unrecognized fragrance_native_database surface for Fragrantica Cleaning",
        }
    ]
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=FRAGRANTICA_CLEANING_AUDIT_LANE) == []
    assert pending_packets(data_root=data_root) == [pid]


def test_damaged_packet_fails_loud_without_ack_and_resurfaces(tmp_path) -> None:
    # S4: a damaged packet (verified read fails closed) is a typed failure with NO
    # ack, re-surfacing every run — never a silent skip or a fake completion fact.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(data_root, tmp_path)
    _tamper_packet(data_root, pid)

    results = run_catchup(data_root=data_root)
    assert len(results) == 1
    assert results[0]["packet_id"] == pid
    assert results[0]["status"] == "derive_failed"
    assert results[0]["error"]
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=FRAGRANTICA_CLEANING_AUDIT_LANE) == []
    assert list((data_root.path / "derived").glob(f"*/{pid}/*")) == []

    second = run_catchup(data_root=data_root)
    assert [r["status"] for r in second] == ["derive_failed"]
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=FRAGRANTICA_CLEANING_AUDIT_LANE) == []


def test_per_packet_failure_is_isolated(tmp_path) -> None:
    # S5: one damaged packet leaves its anchor unacknowledged while the batch
    # continues and the healthy packet completes and acks.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    good = _commit_family_packet(data_root, tmp_path, name="good")
    bad = _commit_family_packet(data_root, tmp_path, name="bad")
    _tamper_packet(data_root, bad)

    results = run_catchup(data_root=data_root)
    by_packet = {r["packet_id"]: r["status"] for r in results}
    assert by_packet == {good: "derived", bad: "derive_failed"}
    assert len(find_acks(data_root, raw_anchor=good, ack_namespace=FRAGRANTICA_CLEANING_AUDIT_LANE)) == 1
    assert find_acks(data_root, raw_anchor=bad, ack_namespace=FRAGRANTICA_CLEANING_AUDIT_LANE) == []


def test_corrupt_manifest_reconcile_failure_still_processes_healthy_packet(tmp_path) -> None:
    # F-ECR-001 class: a corrupt manifest is a visible reconcile failure, never a
    # silent omission that hides healthy packets from pickup.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    bad = _commit_family_packet(data_root, tmp_path, name="bad")
    good = _commit_family_packet(data_root, tmp_path, name="good")
    _corrupt_manifest(data_root, bad)

    results = run_catchup(data_root=data_root)
    by_packet = {r["packet_id"]: r for r in results}
    assert by_packet[bad]["status"] == "availability_reconcile_failed"
    assert by_packet[good]["status"] == "derived"
    assert find_acks(data_root, raw_anchor=bad, ack_namespace=FRAGRANTICA_CLEANING_AUDIT_LANE) == []


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
    assert len(captured.out.strip().splitlines()) == 1
    assert json.loads(captured.out.strip())["status"] == "derived"

    assert main(["--check"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "0\n"
