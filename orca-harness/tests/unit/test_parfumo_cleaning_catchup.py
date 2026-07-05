"""Offline behavioral tests for the Parfumo Cleaning catch-up runner.

Mirror of the adjudicated Fragrantica catch-up suite (F-FRAG-001/002 conventions
inherited): S1 finds-own-backlog, S2 byte-unchanged rerun, output-shaping policy
tokens all in the obligation, S3 policy-bump re-derive, allowlist surface gate over
Parfumo's TWO in-scope surfaces (known other-lane surfaces acked out-of-scope;
unknown surfaces visible and unacknowledged), S4 damage fails loud without ack,
S5 per-packet isolation, F-ECR-001 reconcile visibility, and the CLI.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from cleaning.parfumo_lake import (
    PARFUMO_CLEANING_AUDIT_LANE,
    PARFUMO_CLEANING_SILVER_LANE,
)
from data_lake.consumption import find_acks
from data_lake.root import DataLakeRoot, DataLakeRootError
from runners import run_parfumo_cleaning_catchup as pf_runner
from runners.run_parfumo_cleaning_catchup import main, pending_packets, run_catchup
from source_capture.models import VisibleFact, known_fact
from source_capture.parfumo_projection import (
    PARFUMO_DIRECT_HTTP_SOURCE_SURFACE,
    PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE,
)
from source_capture.writer import write_local_source_capture_packet

_BASENOTES_SURFACE = "basenotes_product_page_cloakbrowser_deep_scroll_current_window"
_LOCATOR = "https://www.parfumo.com/Perfumes/Maison_Francis_Kurkdjian/Baccarat_Rouge_540_Eau_de_Parfum"
_REVIEW_TEXT = "This perfume died young."
_STATEMENT_TEXT = "Airy amber trail."

_HTML = f"""
<html><head>
  <link rel="canonical" href="{_LOCATOR}"/>
  <meta name="description" content="Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian"/>
  <title>Baccarat Rouge 540 Eau de Parfum by Maison Francis Kurkdjian (Eau de Parfum) &amp; Perfume Facts</title>
</head><body>
  <main data-perfume-id="67720" data-rating-count="5176" data-review-count="369"
        data-statement-count="1390" data-scent-rating="7.7" data-longevity-rating="8.7"
        data-sillage-rating="8.5">
    <button data-tab="reviews" data-active="true">Reviews <span>369</span></button>
    <button data-tab="statements">Statements <span>1390</span></button>
    <input type="hidden" name="h" value="7536fa6f9c01a6637a935e7717b53101">
    <script>const routes = {{reviews: "/action/perfume/get_reviews.php", statements: "/action/perfume/get_statements.php", p_id: 67720}};</script>
    <article data-review-id="900001" data-author="Rimazy" data-rating="8.0">
      <time datetime="2026-06-25">06/25/26</time>
      <p data-role="review-text">{_REVIEW_TEXT}</p>
      <a href="/Users/rimazy">Read review</a>
    </article>
    <article data-statement-id="st7001" data-author="Lyra">
      <time datetime="2026-06-24">06/24/26</time>
      <p data-role="statement-text">{_STATEMENT_TEXT}</p>
    </article>
  </main>
</body></html>
"""


_BLOCKED_CAPTURE_BODY = "<html><body>blocked</body></html>"
_BLOCKED_CAPTURE_ACCESS_POSTURE = known_fact(
    "direct_http access_failed with HTTP 403 Forbidden; response body preserved"
)


def _commit_family_packet(
    data_root,
    tmp_path: Path,
    *,
    name: str = "pf",
    source_surface: str = PARFUMO_DIRECT_HTTP_SOURCE_SURFACE,
    body_text: str | None = None,
    access_posture: VisibleFact | None = None,
) -> str:
    body_path = tmp_path / f"{name}_body.bin"
    body_path.write_text(body_text if body_text is not None else _HTML, encoding="utf-8")
    metadata_path = tmp_path / f"{name}_metadata.json"
    metadata_path.write_text('{"status": 200}\n', encoding="utf-8")
    return write_local_source_capture_packet(
        data_root=data_root,
        input_files=[body_path, metadata_path],
        source_family="fragrance_native_database",
        source_surface=source_surface,
        source_locator=known_fact(_LOCATOR),
        decision_question="q",
        capture_context="parfumo cleaning catchup test",
        access_posture=access_posture,
    ).packet.packet_id


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
        (data_root.path / "derived").glob(f"*/{pid}/{PARFUMO_CLEANING_AUDIT_LANE}/*")
    )
    assert audit_path.name == audit_record_id
    silver_paths = list(
        (data_root.path / "derived").glob(f"*/{pid}/{PARFUMO_CLEANING_SILVER_LANE}/*")
    )
    assert len(silver_paths) == results[0]["silver_count"]

    acks = find_acks(data_root, raw_anchor=pid, ack_namespace=PARFUMO_CLEANING_AUDIT_LANE)
    assert len(acks) == 1
    obligation = acks[0]["obligation"]
    assert obligation["consumer"] == "parfumo_cleaning_catchup"
    evidence_by_kind = {entry["kind"]: entry for entry in acks[0]["evidence"]}
    assert evidence_by_kind["derived_record"]["record_id"] == audit_record_id
    assert evidence_by_kind["silver_records"]["count"] == results[0]["silver_count"]
    assert pending_packets(data_root=data_root) == []


def test_targeted_rendered_surface_is_in_scope_and_derives(tmp_path) -> None:
    # Parfumo owns TWO surfaces; the rendered-session surface must derive, not be
    # gated out (the lake adapter passes the packet's surface through). The
    # rendered surface expects the targeted-capture packet shape, so commit it
    # through the capture runner exactly as production does.
    from runners.run_parfumo_mgt_capture import (
        TARGETED_RENDERED_SLOT,
        run_parfumo_targeted_rendered_capture,
    )

    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    artifact_dir = tmp_path / "targeted_artifacts"
    artifact_dir.mkdir(parents=True)
    rendered_dom = artifact_dir / "rendered_dom.html"
    visible_text = artifact_dir / "visible_text.txt"
    route_receipt = artifact_dir / "route_receipt.json"
    screenshot = artifact_dir / "viewport.png"
    rendered_dom.write_text(_HTML, encoding="utf-8")
    visible_text.write_text("Baccarat Rouge 540 Eau de Parfum\nReviews 369\n", encoding="utf-8")
    route_receipt.write_text(
        json.dumps(
            {
                "route": "chrome_extension_user_visible_rendered_session",
                "source_surface": PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE,
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    screenshot.write_bytes(b"png fixture bytes")
    exit_code, message = run_parfumo_targeted_rendered_capture(
        url=_LOCATOR,
        output_root=tmp_path / "targeted_out",
        rendered_dom_path=rendered_dom,
        visible_text_path=visible_text,
        route_receipt_path=route_receipt,
        screenshot_path=screenshot,
        data_root=data_root,
    )
    assert exit_code == 0
    summary = json.loads(Path(message).read_text(encoding="utf-8"))
    pid = summary["packet_roles"][TARGETED_RENDERED_SLOT]["packet_id"]

    results = run_catchup(data_root=data_root)
    assert [(r["packet_id"], r["status"]) for r in results] == [(pid, "derived")]
    assert len(find_acks(data_root, raw_anchor=pid, ack_namespace=PARFUMO_CLEANING_AUDIT_LANE)) == 1


def test_output_shaping_policy_tokens_are_in_obligation() -> None:
    # F-FRAG-001 convention: every output-shaping pre-existing constant is in the
    # envelope, so a change to any of them re-fingerprints and re-surfaces work.
    obligation = pf_runner._packet_obligation()
    assert obligation["cleaning_core_version"] == pf_runner.CLEANING_CORE_VERSION
    assert obligation["projection_method"] == pf_runner.PARFUMO_PROJECTION_METHOD
    assert obligation["projection_version"] == pf_runner.PARFUMO_PROJECTION_VERSION
    assert obligation["projection_certification"] == pf_runner.PARFUMO_PROJECTION_CERTIFICATION
    assert obligation["cleaning_audit_pack_schema_version"] == pf_runner.CLEANING_AUDIT_PACK_SCHEMA_VERSION
    assert obligation["audit_pack_schema_version"] == pf_runner.PARFUMO_AUDIT_PACK_PRODUCER_SCHEMA_VERSION
    assert obligation["silver_vault_record_schema_version"] == pf_runner.SILVER_VAULT_RECORD_SCHEMA_VERSION
    assert obligation["silver_schema_version"] == pf_runner.PARFUMO_SILVER_PRODUCER_SCHEMA_VERSION
    assert obligation["silver_metric_schema_version"] == pf_runner.PARFUMO_SILVER_METRIC_PRODUCER_SCHEMA_VERSION
    assert obligation["cleaning_method_id"] == pf_runner.PARFUMO_CLEANING_METHOD_ID
    assert obligation["text_normalization_rule"] == pf_runner.TEXT_NORMALIZATION_RULE
    assert obligation["rating_carry_rule"] == pf_runner.PARFUMO_RATING_CARRY_RULE
    assert obligation["rating_metric_absent_residual"] == pf_runner.PARFUMO_RATING_METRIC_ABSENT_RESIDUAL
    assert obligation["review_rating_metric_specs"] == [
        list(spec) for spec in pf_runner._REVIEW_RATING_METRIC_SPECS
    ]


def test_catchup_second_run_is_byte_unchanged_noop(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_family_packet(data_root, tmp_path)
    assert [r["status"] for r in run_catchup(data_root=data_root)] == ["derived"]

    before = _lake_tree_state(data_root)
    assert run_catchup(data_root=data_root) == []
    assert _lake_tree_state(data_root) == before


def test_out_of_scope_policy_change_re_surfaces_previous_ack(tmp_path, monkeypatch) -> None:
    # F-IGRC-002 convention: the surface gate is fingerprinted policy — removing a
    # surface from the known-out-of-scope set must re-surface its packets as
    # visible unsupported_surface instead of leaving the old ack trusted.
    from cleaning.parfumo_lake import PARFUMO_CLEANING_AUDIT_LANE as _audit_lane
    from data_lake.consumption import find_acks as _find_acks

    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(
        data_root,
        tmp_path,
        name="bn",
        source_surface=_BASENOTES_SURFACE,
        body_text="<html><body>a basenotes page</body></html>",
    )
    assert [r["status"] for r in run_catchup(data_root=data_root)] == [
        "acked_no_cleanable_content"
    ]

    monkeypatch.setattr(pf_runner, "_KNOWN_OUT_OF_SCOPE_SURFACES", frozenset())
    second = run_catchup(data_root=data_root)

    assert [r["status"] for r in second] == ["unsupported_surface"]
    assert second[0]["source_surface"] == _BASENOTES_SURFACE
    assert len(_find_acks(data_root, raw_anchor=pid, ack_namespace=_audit_lane)) == 1


def test_policy_bump_resurfaces_and_rederives(tmp_path, monkeypatch) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(data_root, tmp_path)
    original_version = pf_runner.CLEANING_CORE_VERSION

    first = run_catchup(data_root=data_root)
    assert [r["status"] for r in first] == ["derived"]
    assert run_catchup(data_root=data_root) == []

    monkeypatch.setattr(pf_runner, "CLEANING_CORE_VERSION", "test-cleaning-vnext")
    third = run_catchup(data_root=data_root)
    assert [r["status"] for r in third] == ["derived"]
    assert third[0]["audit_record_id"] != first[0]["audit_record_id"]

    acks = find_acks(data_root, raw_anchor=pid, ack_namespace=PARFUMO_CLEANING_AUDIT_LANE)
    assert len(acks) == 2
    assert {ack["obligation"]["cleaning_core_version"] for ack in acks} == {
        original_version,
        "test-cleaning-vnext",
    }
    assert run_catchup(data_root=data_root) == []


def test_shared_family_known_other_surface_acked_out_of_scope_never_derived(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    other = _commit_family_packet(
        data_root,
        tmp_path,
        name="bn",
        source_surface=_BASENOTES_SURFACE,
        body_text="<html><body>a basenotes page</body></html>",
    )
    pf = _commit_family_packet(data_root, tmp_path)

    results = run_catchup(data_root=data_root)
    by_packet = {r["packet_id"]: r for r in results}
    assert by_packet[pf]["status"] == "derived"
    assert by_packet[other]["status"] == "acked_no_cleanable_content"

    assert list((data_root.path / "derived").glob(f"*/{other}/*")) == []
    acks = find_acks(data_root, raw_anchor=other, ack_namespace=PARFUMO_CLEANING_AUDIT_LANE)
    assert len(acks) == 1
    assert acks[0]["evidence"] == [
        {
            "kind": "no_cleanable_content_for_surface",
            "raw_anchor": other,
            "source_surface": _BASENOTES_SURFACE,
            "basis": "known_non_parfumo_source_surface",
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
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=PARFUMO_CLEANING_AUDIT_LANE) == []

    second = run_catchup(data_root=data_root)
    assert [r["status"] for r in second] == ["unsupported_surface"]
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=PARFUMO_CLEANING_AUDIT_LANE) == []


def test_damaged_packet_fails_loud_without_ack_and_resurfaces(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(data_root, tmp_path)
    _tamper_packet(data_root, pid)

    results = run_catchup(data_root=data_root)
    assert [r["status"] for r in results] == ["derive_failed"]
    assert results[0]["error"]
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=PARFUMO_CLEANING_AUDIT_LANE) == []
    assert list((data_root.path / "derived").glob(f"*/{pid}/*")) == []

    second = run_catchup(data_root=data_root)
    assert [r["status"] for r in second] == ["derive_failed"]
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=PARFUMO_CLEANING_AUDIT_LANE) == []


def test_blocked_capture_zero_handles_acks_only_direct_http_surface(tmp_path) -> None:
    # A recorded source-side access failure (e.g. Cloudflare/anti-bot 403 block) on
    # the in-scope direct-HTTP surface yields zero projection rows/handles -- an
    # honest non-cleanable outcome, not a parser bug, so it must ack rather than
    # raise derive_failed (F-CAD-002-class parfumo empty-handles fix).
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(
        data_root,
        tmp_path,
        name="blocked",
        body_text=_BLOCKED_CAPTURE_BODY,
        access_posture=_BLOCKED_CAPTURE_ACCESS_POSTURE,
    )

    results = run_catchup(data_root=data_root)
    assert [r["status"] for r in results] == ["acked_no_cleanable_content"]
    assert results[0]["source_surface"] == PARFUMO_DIRECT_HTTP_SOURCE_SURFACE

    acks = find_acks(data_root, raw_anchor=pid, ack_namespace=PARFUMO_CLEANING_AUDIT_LANE)
    assert len(acks) == 1
    assert acks[0]["evidence"] == [
        {
            "kind": "no_cleanable_content_for_blocked_capture",
            "raw_anchor": pid,
            "source_surface": PARFUMO_DIRECT_HTTP_SOURCE_SURFACE,
            "basis": _BLOCKED_CAPTURE_ACCESS_POSTURE.value,
        }
    ]
    assert list((data_root.path / "derived").glob(f"*/{pid}/*")) == []
    assert pending_packets(data_root=data_root) == []

    targeted_root = DataLakeRoot.for_test(tmp_path / "targeted_lake")
    targeted = _commit_family_packet(
        targeted_root,
        tmp_path,
        name="targetedblocked",
        source_surface=PARFUMO_TARGETED_RENDERED_SOURCE_SURFACE,
        body_text=_BLOCKED_CAPTURE_BODY,
        access_posture=_BLOCKED_CAPTURE_ACCESS_POSTURE,
    )

    targeted_results = run_catchup(data_root=targeted_root)
    assert [r["status"] for r in targeted_results] == ["derive_failed"]
    assert "too_short" in targeted_results[0]["error"]
    assert (
        find_acks(
            targeted_root,
            raw_anchor=targeted,
            ack_namespace=PARFUMO_CLEANING_AUDIT_LANE,
        )
        == []
    )


def test_zero_handles_without_blocked_signal_still_fails_loud(tmp_path) -> None:
    # Same zero-row body, but WITHOUT a recorded access-failure signal (default
    # access_posture): the fork between "parser found nothing on a blocked capture"
    # and "parser found nothing on what looks like a real page" must stay
    # distinguishable -- this must still surface loudly and never ack.
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_family_packet(
        data_root,
        tmp_path,
        name="emptynotblocked",
        body_text=_BLOCKED_CAPTURE_BODY,
    )

    results = run_catchup(data_root=data_root)
    assert [r["status"] for r in results] == ["derive_failed"]
    assert "too_short" in results[0]["error"]
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=PARFUMO_CLEANING_AUDIT_LANE) == []

    second = run_catchup(data_root=data_root)
    assert [r["status"] for r in second] == ["derive_failed"]
    assert find_acks(data_root, raw_anchor=pid, ack_namespace=PARFUMO_CLEANING_AUDIT_LANE) == []


def test_per_packet_failure_is_isolated(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    good = _commit_family_packet(data_root, tmp_path, name="good")
    bad = _commit_family_packet(data_root, tmp_path, name="bad")
    _tamper_packet(data_root, bad)

    results = run_catchup(data_root=data_root)
    by_packet = {r["packet_id"]: r["status"] for r in results}
    assert by_packet == {good: "derived", bad: "derive_failed"}
    assert len(find_acks(data_root, raw_anchor=good, ack_namespace=PARFUMO_CLEANING_AUDIT_LANE)) == 1
    assert find_acks(data_root, raw_anchor=bad, ack_namespace=PARFUMO_CLEANING_AUDIT_LANE) == []


def test_corrupt_manifest_reconcile_failure_still_processes_healthy_packet(tmp_path) -> None:
    data_root = DataLakeRoot.for_test(tmp_path / "lake")
    bad = _commit_family_packet(data_root, tmp_path, name="bad")
    good = _commit_family_packet(data_root, tmp_path, name="good")
    _corrupt_manifest(data_root, bad)

    results = run_catchup(data_root=data_root)
    by_packet = {r["packet_id"]: r for r in results}
    assert by_packet[bad]["status"] == "availability_reconcile_failed"
    assert by_packet[good]["status"] == "derived"
    assert find_acks(data_root, raw_anchor=bad, ack_namespace=PARFUMO_CLEANING_AUDIT_LANE) == []


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
