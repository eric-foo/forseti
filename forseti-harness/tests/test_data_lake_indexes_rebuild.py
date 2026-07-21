"""Silver Vault derived-retrieval view builder + rebuild runner tests.

Covers the seam contract's Rebuild Command Binding: manifest-backed rebuildable
views, the by_mention read-side lineage gate, the undone view's documented
weaker semantics, and a prove-rebuildability that fails on tampered bytes
(never self-comparing).
"""
from __future__ import annotations

import io
import json
import hashlib
import sqlite3
import sys
from pathlib import Path

from cleaning.transcript_product_extractor import EXTRACTOR_RUBRIC_VERSION
from cleaning.transcript_product_lake import product_mentions_policy_fingerprint
from data_lake.canonical_json import canonical_record_bytes
import pytest
from data_lake.consumption import append_ack
from data_lake.derived_retrieval_cache import (
    CACHE_PARTS,
    ClassificationCacheSession,
    _CLASSIFIER_SOURCE_NAMES,
)
from data_lake.derived_retrieval_views import (
    CURRENT_POINTER_FILENAME,
    MENTIONS_LANE,
    audit_derived_retrieval_source_integrity,
    build_by_creator_view,
    build_by_mention_view,
    current_generation_root,
    prove_incremental_rebuild_equality,
    prove_derived_retrieval_rebuildability,
    rebuild_derived_retrieval,
)
from data_lake.derived_retrieval_state import (
    IncrementalSourceInventory,
    STATE_PARTS,
)
from data_lake.root import DataLakeRoot, DataLakeRootError, raw_shard
from data_lake.silver_lineage import (
    SilverAnchor,
    SilverLineage,
    SilverRawRef,
    SilverSourceObject,
)
from data_lake.silver_record import (
    CURRENT_SOURCE_BACKED_AUTHORITY,
    SilverSourceAuthority,
    silver_content_hash,
)
from data_lake.sibling_selection import SiblingSelectionError
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet
from tests.unit._creator_metric_silver_fixtures import commit_raw_packet

_STAMP = {"generation_id": "0" * 32, "generated_at": "2026-07-02T00:00:00+00:00"}
_NS = "projection_ig"
_POLICY = {"policy_version": "v0", "policy_fingerprint_sha256": "a" * 64}
_POLICY_ARGS = [
    "--product-mention-policy-version", "v0",
    "--product-mention-policy-fingerprint-sha256", "a" * 64,
]


def _current_core(root: DataLakeRoot) -> Path:
    return current_generation_root(root)[0]


def _commit_packet(root: DataLakeRoot, tmp_path: Path, body: str) -> str:
    src = tmp_path / f"{body}.json"
    src.write_text(f'{{"b": "{body}"}}', encoding="utf-8")
    receipt = write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family="reddit",
        source_surface="s",
        source_locator=known_fact(f"https://www.reddit.com/r/test/{body}/"),
        decision_question="q",
        capture_context="indexes rebuild test",
    )
    return receipt.packet.packet_id


def _complete_lineage_fields(root: DataLakeRoot, packet_id: str) -> dict:
    preserved = root.load_raw_packet(packet_id).manifest["preserved_files"][0]
    lineage = SilverLineage(
        producer_id="test.producer",
        producer_schema_version="v0",
        source_surface="youtube_captions",
        source_object=SilverSourceObject(namespace="youtube", kind="transcript", native_id="vid1"),
        observed_at="2026-07-15T00:00:00Z",
        captured_at="2026-07-15T00:00:00Z",
        raw_refs=[
            SilverRawRef(
                packet_id=packet_id,
                file_id=preserved["file_id"],
                relative_packet_path=preserved["relative_packet_path"],
                sha256=preserved["sha256"],
                hash_basis="raw_stored_bytes",
                anchor=SilverAnchor(kind="file"),
                relation="consumed",
            )
        ],
    )
    return lineage.to_record_fields()


def _write_mentions_record(
    root: DataLakeRoot, raw_anchor: str, record_id: str, record: dict
) -> None:
    mentions = record.pop("mentions", [])
    rows = []
    for index, mention in enumerate(mentions):
        quote = f"quote {index}"
        rows.append(
            {
                "row_id": f"mention-{index}",
                "text_artifact_type": "transcript_quote",
                "text_value": quote,
                "text_ref": None,
                "text_hash": "sha256:" + hashlib.sha256(quote.encode()).hexdigest(),
                "text_posture": {"kind": "observed", "reason_code": None, "reason_detail": None},
                "mention": mention,
            }
        )
    record = {
        "record_id": record_id,
        "raw_anchor": raw_anchor,
        "lane_namespace": MENTIONS_LANE,
        "producer_id": record.get("producer_id", "test.producer"),
        "schema_version": "silver_vault_record_v0",
        "producer_schema_version": record.get("producer_schema_version", "v0"),
        "content_hash": "",
        "content_hash_basis": "canonical_json_excluding_content_hash",
        "record_kind": "observation",
        "payload_kind": "TextObservationSet",
        "producer_row_kind": "transcript_product_mentions",
        "source_surface": record.get("source_surface", "youtube_captions"),
        "observed_at": record.get("observed_at"),
        "captured_at": record.get("captured_at"),
        "raw_refs": record.get("raw_refs", []),
        "derived_refs": record.get("derived_refs", []),
        **{key: value for key, value in record.items() if key not in {"producer_id", "producer_schema_version", "source_surface", "observed_at", "captured_at", "raw_refs", "derived_refs"}},
        "payload": {
            "observation": {
                "subject": {"ref_type": "entity_key", "ref": {"namespace": "youtube", "kind": "public_content_object", "native_id": "vid1"}},
                "observation_set_kind": "transcript_product_mentions",
                "policy_version": record.get("policy_version", "v0"),
                "policy_fingerprint_sha256": record.get("policy_fingerprint_sha256", "a" * 64),
                "row_count": len(rows),
                "rows": rows,
            }
        },
        "provenance": {"transcript_source_key": record.get("transcript_source_key", record_id)},
    }
    record["content_hash"] = "sha256:" + silver_content_hash(record)
    root.append_record(
        subtree="derived",
        raw_anchor=raw_anchor,
        lane=MENTIONS_LANE,
        record_id=record_id,
        data=canonical_record_bytes(record),
    )


def _seeded_root(root: DataLakeRoot, tmp_path: Path) -> tuple[str, str]:
    """Two committed packets: one with a gated-in mentions record + an ack, one
    with a lineage-missing mentions record and no ack."""
    first = _commit_packet(root, tmp_path, "alpha")
    second = _commit_packet(root, tmp_path, "beta")
    _write_mentions_record(
        root,
        first,
        "m_complete.json",
        {
            "mentions": [
                {"brand": "Dior", "line": "Sauvage Elixir"},
                {"brand": "Dior", "line": "Homme Intense"},
            ],
            **_complete_lineage_fields(root, first),
        },
    )
    _write_mentions_record(
        root,
        second,
        "m_no_lineage.json",
        {"mentions": [{"brand": "Ghost", "line": "Should Not Index"}]},
    )
    append_ack(
        root,
        raw_anchor=first,
        ack_namespace=_NS,
        obligation={"obligation_schema": 1, "consumer": "indexes_rebuild_test", "inputs": []},
        evidence=[{"kind": "test_marker", "ref": "r1"}],
    )
    return first, second




def test_sql_catalogue_incremental_search_actor_audit_and_cold_rebuild(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import data_lake.derived_retrieval_views as retrieval_views
    from data_lake.derived_retrieval_views import (
        query_exact_actor_context, query_sql_catalogue, sql_catalogue_path,
        sql_catalogue_status, verify_sql_query_sources, write_actor_query_audit,
        write_evidence_query_audit,
    )
    payload = {
        "platform": "tiktok",
        "source_surface": "tiktok_creator_batch_comment_subtitle_admission",
        "creator_handle": "creator",
        "capture_timestamp": "2026-07-20T00:00:00Z",
        "videos": [{
            "video_id": "7000000000000000001", "create_time": 1784500000,
            "comments": {"posture": "captured_page_owned_response", "comments": [{
                "cid": "c1", "text": "wear test coordination",
                "create_time": 1784500060,
                "user": {"uid": "actor-1", "unique_id": "same_name"}
            }]}
        }]
    }
    source = tmp_path / "tiktok_batch_capture.json"
    source.write_text(json.dumps(payload),encoding="utf-8")
    root = DataLakeRoot.for_test(tmp_path / "lake")
    receipt = write_local_source_capture_packet(
        data_root=root,input_files=[source],source_family="tiktok",
        source_surface="tiktok_creator_batch_comment_subtitle_admission",
        source_locator=known_fact("https://www.tiktok.com/@creator"),
        decision_question="test SQL retrieval",capture_context="fixture")
    silver = json.loads((Path(__file__).parent / "fixtures" / "silver_compatibility" /
                         "fragrantica_text_v0.json").read_text(encoding="utf-8"))
    root.append_record(
        subtree="derived",raw_anchor=receipt.packet.packet_id,
        lane="cleaning_fragrantica_silver",record_id=silver["record_id"],
        data=canonical_record_bytes(silver))
    monkeypatch.setattr(
        retrieval_views,"classify_silver_vault_record_sources",
        lambda *_args,**_kwargs: SilverSourceAuthority(
            CURRENT_SOURCE_BACKED_AUTHORITY,"test_current"))
    first = rebuild_derived_retrieval(root,product_mention_policy=_POLICY)
    assert first["sql_catalogue"]["event_count"] == 2
    second = rebuild_derived_retrieval(root,product_mention_policy=_POLICY)
    assert second["sql_catalogue"]["status"] == "current"
    found = query_sql_catalogue(root,body_query='"wear test"',platform="tiktok")
    assert found["row_count"] == 1
    assert found["query_contract_version"] == 1
    assert found["result_set_complete"] is True
    assert found["truncated"] is False
    assert found["normalized_query"]["platform"] == "tiktok"
    assert "actor-1" not in json.dumps(found)
    assert query_sql_catalogue(
        root,surface="tiktok_creator_batch_comment_subtitle_admission"
    )["row_count"] == 1
    assert query_sql_catalogue(root,surface="not_this_surface")["row_count"] == 0
    silver_found = query_sql_catalogue(
        root,body_query='"Synthetic fixture"',vendor="fragrantica")
    assert silver_found["row_count"] == 1
    decision = query_sql_catalogue(root,limit=10)
    decision["source_verification"] = verify_sql_query_sources(root,decision)
    assert decision["source_verification"] == {
        "status":"passed","verified_source_count":2}
    decision_audit = write_evidence_query_audit(
        decision,decision_question_id="creator_comment_coordination",
        audit_root=tmp_path / "general-audit")
    decision_receipt = json.loads(Path(decision_audit).read_text(encoding="utf-8"))
    assert decision_receipt["audit_schema_version"] == 2
    assert decision_receipt["result_set_complete"] is True
    assert len(decision_receipt["citations"]) == 2
    assert decision_receipt["catalogue_snapshot"]["logical_digest"]
    assert decision_receipt["citation_manifest_sha256"]
    assert "body_text" not in json.dumps(decision_receipt)
    with pytest.raises(ValueError,match="nonblank"):
        write_evidence_query_audit(decision,decision_question_id="")
    with pytest.raises(ValueError,match="at most 128"):
        write_evidence_query_audit(decision,decision_question_id="x" * 129)

    raw_manifest = root.find_packet(receipt.packet.packet_id) / "manifest.json"
    raw_manifest_bytes = raw_manifest.read_bytes()
    try:
        raw_manifest.write_bytes(raw_manifest_bytes + b" ")
        with pytest.raises(DataLakeRootError, match="manifest hash mismatch"):
            verify_sql_query_sources(root,found)
    finally:
        raw_manifest.write_bytes(raw_manifest_bytes)
    silver_path = root.path / silver_found["rows"][0]["source_ref"]
    silver_bytes = silver_path.read_bytes()
    try:
        silver_path.write_bytes(silver_bytes + b" ")
        with pytest.raises(DataLakeRootError, match="Silver hash mismatch"):
            verify_sql_query_sources(root,silver_found)
    finally:
        silver_path.write_bytes(silver_bytes)

    actor = query_exact_actor_context(
        root,platform="tiktok",actor="actor-1",
        from_utc="2026-07-01T00:00:00Z",to_utc="2026-07-31T00:00:00Z",
        creator_id="creator")
    assert actor["row_count"] == 1
    with pytest.raises(ValueError, match="at most 90 days"):
        query_exact_actor_context(
            root,platform="tiktok",actor="actor-1",
            from_utc="2026-07-01T00:00:00Z",to_utc="2026-10-01T00:00:01Z")
    monkeypatch.setenv("FORSETI_DERIVED_RETRIEVAL_SQL_ROOT","relative")
    with pytest.raises(DataLakeRootError, match="must be absolute"):
        sql_catalogue_path(root)
    monkeypatch.delenv("FORSETI_DERIVED_RETRIEVAL_SQL_ROOT")
    monkeypatch.setenv("LOCALAPPDATA",str(tmp_path / "local"))
    audit = write_actor_query_audit(
        actor,decision_question_id="bounded_public_actor_context")
    assert Path(audit).is_file()
    actor_receipt = json.loads(Path(audit).read_text(encoding="utf-8"))
    assert actor_receipt["audit_schema_version"] == 2
    assert actor_receipt["decision_question_id"] == "bounded_public_actor_context"
    assert actor_receipt["source_verification"]["status"] == "passed"
    assert len(actor_receipt["citations"]) == 1
    assert "body_text" not in json.dumps(actor_receipt)
    before = sql_catalogue_status(root)["logical_digest"]
    rebuilt = rebuild_derived_retrieval(
        root,product_mention_policy=_POLICY,full_rebuild=True)
    assert rebuilt["sql_catalogue"]["logical_digest"] == before


def test_runner_sql_query_is_safe_on_cp1252_console(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import runners.run_data_lake_indexes_rebuild as runner

    root = DataLakeRoot.for_test(tmp_path / "lake")
    monkeypatch.setattr(DataLakeRoot,"resolve",staticmethod(lambda **_kwargs: root))
    query_kwargs = {}

    def _query(*_args, **kwargs):
        query_kwargs.update(kwargs)
        return {"status":"ok","rows":[{"body_text":"broken heart 💔"}]}

    monkeypatch.setattr(runner,"query_sql_catalogue",_query)
    monkeypatch.setattr(
        runner,"verify_sql_query_sources",
        lambda *_args,**_kwargs: pytest.fail("exploratory query verified sources"))
    monkeypatch.setattr(
        runner,"write_evidence_query_audit",
        lambda *_args,**_kwargs: pytest.fail("exploratory query wrote receipt"))
    raw = io.BytesIO()
    console = io.TextIOWrapper(raw,encoding="cp1252")
    monkeypatch.setattr(sys,"stdout",console)

    assert runner.main([
        "--root",str(root.path),"--sql-query",
        "--sql-surface","tiktok_creator_batch_comment_subtitle_admission",
    ]) == 0
    assert query_kwargs["surface"] == "tiktok_creator_batch_comment_subtitle_admission"
    console.flush()
    rendered = raw.getvalue().decode("cp1252")
    assert "broken heart" in rendered
    assert r"\ud83d\udc94" in rendered


def test_runner_decision_query_verifies_and_audits_before_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import runners.run_data_lake_indexes_rebuild as runner

    root = DataLakeRoot.for_test(tmp_path / "lake")
    monkeypatch.setattr(DataLakeRoot,"resolve",staticmethod(lambda **_kwargs: root))
    report = {"query_profile":"evidence_search","query_contract_version":1,
        "normalized_query":{},"catalogue":{},"row_count":0,
        "result_set_complete":True,"truncated":False,"rows":[],"non_claims":[]}
    order = []
    monkeypatch.setattr(runner,"query_sql_catalogue",lambda *_args,**_kwargs: dict(report))
    monkeypatch.setattr(
        runner,"verify_sql_query_sources",
        lambda *_args,**_kwargs: order.append("verified") or {
            "status":"passed","verified_source_count":0})
    monkeypatch.setattr(
        runner,"write_evidence_query_audit",
        lambda *_args,**_kwargs: order.append("audited") or "receipt.json")
    output = io.StringIO()
    monkeypatch.setattr(sys,"stdout",output)
    assert runner.main([
        "--root",str(root.path),"--sql-query",
        "--decision-question-id","creator_comment_coordination",
    ]) == 0
    assert order == ["verified","audited"]
    assert json.loads(output.getvalue())["audit_path"] == "receipt.json"

    truncated = dict(report,result_set_complete=False,truncated=True)
    monkeypatch.setattr(runner,"query_sql_catalogue",lambda *_args,**_kwargs: truncated)
    monkeypatch.setattr(
        runner,"verify_sql_query_sources",
        lambda *_args,**_kwargs: pytest.fail("truncated query verified sources"))
    output = io.StringIO()
    monkeypatch.setattr(sys,"stdout",output)
    assert runner.main([
        "--root",str(root.path),"--sql-query",
        "--decision-question-id","creator_comment_coordination",
    ]) == 2
    assert "truncated" in json.loads(output.getvalue())["error"]


def _sql_catalogue_root(
    tmp_path: Path, *, create_time: int, comment_count: int = 1
) -> DataLakeRoot:
    tmp_path.mkdir(parents=True, exist_ok=True)
    """One committed TikTok comment packet catalogued through the real raw path."""
    payload = {
        "platform": "tiktok",
        "source_surface": "tiktok_creator_batch_comment_subtitle_admission",
        "creator_handle": "creator",
        "capture_timestamp": "2026-07-20T00:00:00Z",
        "videos": [{
            "video_id": "7000000000000000001", "create_time": create_time,
            "comments": {"posture": "captured_page_owned_response", "comments": [{
                "cid": "c%d" % index, "text": "boundary window probe",
                "create_time": create_time,
                "user": {"uid": "actor-1", "unique_id": "same_name"}
            } for index in range(comment_count)]}
        }]
    }
    source = tmp_path / "tiktok_batch_capture.json"
    source.write_text(json.dumps(payload), encoding="utf-8")
    root = DataLakeRoot.for_test(tmp_path / "lake")
    write_local_source_capture_packet(
        data_root=root, input_files=[source], source_family="tiktok",
        source_surface="tiktok_creator_batch_comment_subtitle_admission",
        source_locator=known_fact("https://www.tiktok.com/@creator"),
        decision_question="test SQL retrieval", capture_context="fixture")
    rebuild_derived_retrieval(root, product_mention_policy=_POLICY)
    return root


def test_sql_time_window_bounds_are_normalized_before_filtering(
    tmp_path: Path,
) -> None:
    """Stored event times are canonical ``+00:00`` UTC. A caller bound written
    as ``Z`` or in a non-UTC offset must select the SAME instants, not a
    lexicographically shifted window."""
    from data_lake.derived_retrieval_views import (
        query_exact_actor_context, query_sql_catalogue,
    )

    root = _sql_catalogue_root(tmp_path, create_time=1784505600)
    boundary = query_sql_catalogue(
        root, platform="tiktok",
        from_utc="2026-07-20T00:00:00Z", to_utc="2026-07-20T00:00:00Z")
    assert boundary["row_count"] == 1
    assert boundary["normalized_query"]["from_utc"] == "2026-07-20T00:00:00+00:00"
    assert boundary["normalized_query"]["to_utc"] == "2026-07-20T00:00:00+00:00"
    offset_window = query_exact_actor_context(
        root, platform="tiktok", actor="actor-1",
        from_utc="2026-07-20T09:00:00+09:00", to_utc="2026-07-21T09:00:00+09:00",
        creator_id="creator")
    assert offset_window["row_count"] == 1
    assert offset_window["time_window"] == {
        "from_utc": "2026-07-20T00:00:00+00:00",
        "to_utc": "2026-07-21T00:00:00+00:00",
    }
    outside = query_sql_catalogue(
        root, platform="tiktok",
        from_utc="2026-07-20T00:00:01Z", to_utc="2026-07-21T00:00:00Z")
    assert outside["row_count"] == 0
    with pytest.raises(ValueError, match="from_utc"):
        query_sql_catalogue(root, from_utc="not-a-timestamp")


def test_sql_query_reports_true_result_set_truncation(tmp_path: Path) -> None:
    from data_lake.derived_retrieval_views import query_sql_catalogue

    root = _sql_catalogue_root(
        tmp_path,create_time=1784505600,comment_count=2)
    complete = query_sql_catalogue(root,platform="tiktok",limit=2)
    assert complete["row_count"] == 2
    assert complete["result_set_complete"] is True
    assert complete["truncated"] is False
    truncated = query_sql_catalogue(root,platform="tiktok",limit=1)
    assert truncated["row_count"] == 1
    assert truncated["result_set_complete"] is False
    assert truncated["truncated"] is True
    assert truncated["normalized_query"]["limit"] == 1


def test_failed_full_rebuild_leaves_the_previous_sql_catalogue_intact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A --full-rebuild that dies mid-extraction (the external-volume failure
    mode) must not leave an emptied catalogue reporting a healthy zero."""
    import data_lake.derived_retrieval_views as retrieval_views
    from data_lake.derived_retrieval_views import sql_catalogue_status

    root = _sql_catalogue_root(tmp_path, create_time=1784505600)
    before = sql_catalogue_status(root)
    assert before["event_count"] == 1

    def _device_loss(*_args, **_kwargs):
        raise OSError("simulated external volume loss")

    monkeypatch.setattr(retrieval_views, "_dr_insert_events", _device_loss)
    with pytest.raises(OSError):
        rebuild_derived_retrieval(
            root, product_mention_policy=_POLICY, full_rebuild=True)
    monkeypatch.undo()

    after = sql_catalogue_status(root)
    assert after["event_count"] == before["event_count"]
    assert after["source_count"] == before["source_count"]
    assert after["logical_digest"] == before["logical_digest"]
    assert after["last_successful_refresh_at"] == before["last_successful_refresh_at"]


def test_exact_actor_saturated_candidate_set_fails_loud(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A saturated candidate window is silently truncated evidence; an anchored
    query must fail loud rather than return a short audited answer."""
    import data_lake.derived_retrieval_views as retrieval_views
    from data_lake.derived_retrieval_views import query_exact_actor_context

    root = _sql_catalogue_root(
        tmp_path,create_time=1784505600,comment_count=2)
    monkeypatch.setattr(retrieval_views,"SQL_ACTOR_CANDIDATE_LIMIT",2)
    complete = query_exact_actor_context(
        root,platform="tiktok",actor="actor-1",
        from_utc="2026-07-19T00:00:00Z",to_utc="2026-07-21T00:00:00Z",
        creator_id="creator")
    assert complete["row_count"] == 2
    monkeypatch.setattr(retrieval_views,"SQL_ACTOR_CANDIDATE_LIMIT",1)
    with pytest.raises(ValueError,match="exceeds"):
        query_exact_actor_context(
            root,platform="tiktok",actor="actor-1",
            from_utc="2026-07-19T00:00:00Z",to_utc="2026-07-21T00:00:00Z",
            creator_id="creator")


def test_rebuild_builds_views_and_manifests(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first, second = _seeded_root(root, tmp_path)

    legacy_root = root.path / "indexes" / "derived_retrieval" / "object_level"
    legacy_root.mkdir(parents=True)
    (legacy_root / "by_mention.json").write_text("legacy", encoding="utf-8")
    report = rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
    assert report["status"] == "rebuilt"
    assert report["views"] == ["by_creator", "by_mention", "undone"]
    assert report["deferred_views"] == []

    assert not legacy_root.exists()
    silver_core = _current_core(root)
    by_creator = json.loads((silver_core / "query_tables" / "by_creator.json").read_text("utf-8"))
    by_mention = json.loads((silver_core / "query_tables" / "by_mention.json").read_text("utf-8"))
    undone = json.loads((silver_core / "query_tables" / "undone.json").read_text("utf-8"))
    assert by_creator["view_schema_version"] == 2
    assert "no cross-platform identity" in by_creator["semantics"]
    assert "identity kinds never merge" in by_creator["semantics"]

    # lineage gate: the complete record is evidence; the lineage-missing one is a residual.
    refs = by_mention["mentions"]["Dior"]["Sauvage Elixir"]
    assert [r["raw_anchor"] for r in refs] == [first]
    assert "Homme Intense" in by_mention["mentions"]["Dior"]
    assert "Ghost" not in by_mention["mentions"]
    assert by_mention["residual_count"] == 1
    assert by_mention["residuals"][0]["status"] == "invalid_silver_envelope"
    assert by_mention["residuals"][0]["raw_anchor"] == second

    # undone view: adopted-namespace backlog only, weaker semantics stated in-body,
    # zero-rows disclosure fields pinned (seam contract disclosure obligation).
    assert undone["adopted_namespaces"] == [_NS]
    assert undone["undone"][_NS] == sorted([second])
    assert "never pickup authority" in undone["semantics"]
    assert "NOT current-obligation satisfied" in undone["zero_rows_meaning"]
    assert undone["anchors_with_acks"] == {_NS: 1}

    for view_name in ("by_creator", "by_mention", "undone"):
        manifest = json.loads(
            (silver_core / "manifests" / f"{view_name}.json").read_text("utf-8")
        )
        assert manifest["generation_id"] == _STAMP["generation_id"]
        assert manifest["generated_at"] == _STAMP["generated_at"]
        assert manifest["source_record_ids"]
        assert manifest["source_high_watermark"]
        assert manifest["selection_policy_versions"]
        assert manifest["view_sha256"]
        assert manifest["stale_if"]


def test_by_mention_gates_unreadable_records(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(root, tmp_path, "alpha")
    root.append_record(
        subtree="derived",
        raw_anchor=pid,
        lane=MENTIONS_LANE,
        record_id="m_corrupt.json",
        data=b"{not json",
    )
    view, _refs = build_by_mention_view(root, product_mention_policy=_POLICY)
    assert view["mentions"] == {}
    assert view["residuals"][0]["status"] == "unreadable"


def test_by_mention_selects_only_the_requested_policy(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(root, tmp_path, "alpha")
    _write_mentions_record(
        root,
        pid,
        "old.json",
        {
            "mentions": [{"brand": "Old", "line": "Excluded"}],
            "policy_version": "old",
            "policy_fingerprint_sha256": "b" * 64,
            "transcript_source_key": "same-source",
            **_complete_lineage_fields(root, pid),
        },
    )
    _write_mentions_record(
        root,
        pid,
        "current.json",
        {
            "mentions": [{"brand": "Current", "line": "Included"}],
            "transcript_source_key": "same-source",
            **_complete_lineage_fields(root, pid),
        },
    )

    view, _refs = build_by_mention_view(root, product_mention_policy=_POLICY)

    assert set(view["mentions"]) == {"Current"}
    assert view["selection_policy"] == _POLICY
    assert [residual["status"] for residual in view["residuals"]] == ["policy_mismatch"]


def test_by_mention_distinct_same_policy_siblings_fail_closed(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(root, tmp_path, "alpha")
    for record_id, brand in (("a.json", "A"), ("b.json", "B")):
        _write_mentions_record(
            root,
            pid,
            record_id,
            {
                "mentions": [{"brand": brand, "line": "line"}],
                "transcript_source_key": "same-source",
                **_complete_lineage_fields(root, pid),
            },
        )

    with pytest.raises(SiblingSelectionError, match="ambiguous_sibling_derivation"):
        build_by_mention_view(root, product_mention_policy=_POLICY)


def test_by_mention_requires_exact_policy_identity(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    with pytest.raises(ValueError, match="policy_version"):
        build_by_mention_view(
            root,
            product_mention_policy={
                "policy_fingerprint_sha256": "a" * 64,
            },
        )

def test_prove_rebuildability_green_then_tamper_fails(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    _seeded_root(root, tmp_path)
    rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)

    proof = prove_derived_retrieval_rebuildability(root)
    assert proof["status"] == "proven"
    assert proof["results"] == {
        "by_creator": "rebuildable",
        "by_mention": "rebuildable",
        "undone": "rebuildable",
    }

    view_path = _current_core(root) / "query_tables" / "undone.json"
    view_path.write_bytes(view_path.read_bytes() + b" ")  # smuggled state
    proof = prove_derived_retrieval_rebuildability(root)
    assert proof["status"] == "failed"
    assert proof["results"]["undone"] == "failed_drift_or_non_regenerable"
    assert proof["failures"] == ["undone"]


def test_prove_detects_source_change_since_generation(tmp_path: Path) -> None:
    # A new committed packet after generation changes the undone view's inputs:
    # the stored view no longer matches a regeneration -> drift is reported.
    root = DataLakeRoot.for_test(tmp_path / "lake")
    _seeded_root(root, tmp_path)
    rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
    assert prove_derived_retrieval_rebuildability(root)["status"] == "proven"

    _commit_packet(root, tmp_path, "gamma")
    proof = prove_derived_retrieval_rebuildability(root)
    assert proof["status"] == "failed"
    assert proof["results"]["undone"] == "failed_drift_or_non_regenerable"


def test_prove_on_empty_store_is_absent_not_failure(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    proof = prove_derived_retrieval_rebuildability(root)
    assert proof["status"] == "proven"
    assert proof["results"] == {
        "by_creator": "absent_nothing_to_prove",
        "by_mention": "absent_nothing_to_prove",
        "undone": "absent_nothing_to_prove",
    }


def test_incremental_cache_is_disposable_and_byte_identical(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    _seeded_root(root, tmp_path)

    cold = rebuild_derived_retrieval(
        root,
        product_mention_policy=_POLICY,
        stamp=_STAMP,
        full_rebuild=True,
    )
    target_root = _current_core(root)
    cold_files = {
        path.relative_to(target_root).as_posix(): path.read_bytes()
        for path in sorted(target_root.rglob("*.json"))
        if "cache" not in path.parts
    }
    assert cold["classification_cache"]["hits"] == 0
    cache_path = root._within(*CACHE_PARTS)
    assert cache_path.is_file()

    incremental = rebuild_derived_retrieval(
        root,
        product_mention_policy=_POLICY,
        stamp=_STAMP,
    )
    incremental_files = {
        path.relative_to(target_root).as_posix(): path.read_bytes()
        for path in sorted(target_root.rglob("*.json"))
        if "cache" not in path.parts
    }
    assert incremental["classification_cache"]["hits"] > 0
    assert incremental_files == cold_files

    cache_path.unlink()
    rebuilt_without_cache = rebuild_derived_retrieval(
        root,
        product_mention_policy=_POLICY,
        stamp=_STAMP,
    )
    rebuilt_files = {
        path.relative_to(target_root).as_posix(): path.read_bytes()
        for path in sorted(target_root.rglob("*.json"))
        if "cache" not in path.parts
    }
    assert rebuilt_without_cache["classification_cache"]["hits"] == 0
    assert rebuilt_files == cold_files


def test_repeat_refresh_is_noop_and_new_source_publishes_incrementally(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    _seeded_root(root, tmp_path)

    first = rebuild_derived_retrieval(
        root, product_mention_policy=_POLICY
    )
    repeated = rebuild_derived_retrieval(
        root, product_mention_policy=_POLICY
    )

    assert repeated["status"] == "current"
    assert repeated["generation_id"] == first["generation_id"]
    assert repeated["source_inventory"]["source_body_reads"] == 0

    packet_id = _commit_packet(root, tmp_path, "incremental-new-source")
    _write_fragrantica_projection(root, packet_id)
    advanced = rebuild_derived_retrieval(
        root, product_mention_policy=_POLICY
    )

    assert advanced["status"] == "rebuilt"
    assert advanced["generation_id"] != first["generation_id"]
    assert advanced["source_inventory"]["new_sources"] == 1
    assert advanced["source_inventory"]["source_body_reads"] == 1
    by_mention = json.loads(
        (_current_core(root) / "query_tables" / "by_mention.json").read_text(
            encoding="utf-8"
        )
    )
    assert "Ariana Grande" in by_mention["native_product_pages"]


def test_incremental_refresh_rejects_changed_or_disappeared_source(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    _seeded_root(root, tmp_path)
    rebuild_derived_retrieval(root, product_mention_policy=_POLICY)
    source = next(
        path for path in (root.path / "derived").glob("*/*/*/*") if path.is_file()
    )
    original = source.read_bytes()

    source.write_bytes(original + b" ")
    with pytest.raises(DataLakeRootError, match="changed after it was inventoried"):
        rebuild_derived_retrieval(root, product_mention_policy=_POLICY)

    source.write_bytes(original)
    source.unlink()
    with pytest.raises(DataLakeRootError, match="disappeared after it was inventoried"):
        rebuild_derived_retrieval(root, product_mention_policy=_POLICY)


def test_failed_pointer_switch_keeps_previous_complete_generation(
    tmp_path: Path, monkeypatch
) -> None:
    import data_lake.derived_retrieval_views as views

    root = DataLakeRoot.for_test(tmp_path / "lake")
    _seeded_root(root, tmp_path)
    first = rebuild_derived_retrieval(
        root, product_mention_policy=_POLICY
    )
    pointer = _current_core(root).parent.parent / CURRENT_POINTER_FILENAME
    pointer_before = pointer.read_bytes()
    packet_id = _commit_packet(root, tmp_path, "pointer-failure")
    _write_fragrantica_projection(root, packet_id)
    real_atomic_replace = views._atomic_replace

    def fail_pointer(target: Path, data: bytes) -> None:
        if target.name == CURRENT_POINTER_FILENAME:
            raise OSError("seeded pointer failure")
        real_atomic_replace(target, data)

    monkeypatch.setattr(views, "_atomic_replace", fail_pointer)
    with pytest.raises(OSError, match="seeded pointer failure"):
        rebuild_derived_retrieval(root, product_mention_policy=_POLICY)

    assert pointer.read_bytes() == pointer_before
    assert current_generation_root(root)[1] == first["generation_id"]


def test_concurrent_updater_fails_loud_and_disposable_state_rebuilds(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    _seeded_root(root, tmp_path)
    first = rebuild_derived_retrieval(
        root, product_mention_policy=_POLICY, stamp=_STAMP
    )
    first_files = {
        path.relative_to(_current_core(root)).as_posix(): path.read_bytes()
        for path in sorted(_current_core(root).rglob("*.json"))
    }

    with IncrementalSourceInventory(root):
        with pytest.raises(DataLakeRootError, match="another updater is active"):
            rebuild_derived_retrieval(root, product_mention_policy=_POLICY)

    root._within(*STATE_PARTS).unlink()
    rebuilt = rebuild_derived_retrieval(
        root, product_mention_policy=_POLICY, stamp=_STAMP
    )
    rebuilt_files = {
        path.relative_to(_current_core(root)).as_posix(): path.read_bytes()
        for path in sorted(_current_core(root).rglob("*.json"))
    }
    assert rebuilt["status"] == "rebuilt"
    assert rebuilt["generation_id"] == first["generation_id"]
    assert rebuilt_files == first_files


def test_unsupported_inventory_schema_releases_writer_before_recovery(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    _seeded_root(root, tmp_path)
    rebuild_derived_retrieval(root, product_mention_policy=_POLICY)
    inventory_path = root._within(*STATE_PARTS)
    connection = sqlite3.connect(inventory_path)
    try:
        connection.execute(
            "UPDATE metadata SET value = 'unsupported' "
            "WHERE key = 'state_schema_version'"
        )
        connection.commit()
    finally:
        connection.close()

    with pytest.raises(DataLakeRootError, match="unsupported lake-map"):
        rebuild_derived_retrieval(root, product_mention_policy=_POLICY)

    inventory_path.unlink()
    recovered = rebuild_derived_retrieval(
        root, product_mention_policy=_POLICY, full_rebuild=True
    )
    assert recovered["status"] == "rebuilt"


def test_classifier_version_covers_local_authority_implementation_modules() -> None:
    assert {
        "derived_retrieval_cache.py",
        "silver_record.py",
        "silver_compatibility.py",
        "creator_metric_lineage.py",
        "catalog.py",
        "attachment_record_entry.py",
        "canonical_json.py",
        "root.py",
        "../harness_utils.py",
    } <= set(_CLASSIFIER_SOURCE_NAMES)


def test_cache_rejects_unknown_authority_status(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    record = {"content_hash": "sha256:record", "raw_refs": [], "derived_refs": []}
    cache = ClassificationCacheSession(root, use_existing=False)
    key, authority = cache.lookup(record)
    assert key is not None
    assert authority is None
    cache.remember(
        key,
        SilverSourceAuthority(CURRENT_SOURCE_BACKED_AUTHORITY, "test_current"),
    )
    cache.save()

    payload = json.loads(root._within(*CACHE_PARTS).read_text(encoding="utf-8"))
    payload["classifier_version"] = "sha256:stale"
    root._within(*CACHE_PARTS).write_bytes(canonical_record_bytes(payload))
    assert ClassificationCacheSession(root).lookup(record)[1] is None

    payload["classifier_version"] = cache.classifier_version
    payload["verdicts"][key]["status"] = "corrupted_status"
    root._within(*CACHE_PARTS).write_bytes(canonical_record_bytes(payload))

    reloaded = ClassificationCacheSession(root)
    reloaded_key, reloaded_authority = reloaded.lookup(record)
    assert reloaded_key == key
    assert reloaded_authority is None
    assert reloaded.report()["misses"] == 1

    payload["verdicts"][key] = {
        "status": CURRENT_SOURCE_BACKED_AUTHORITY,
        "reason_code": 7,
        "error": None,
    }
    root._within(*CACHE_PARTS).write_bytes(canonical_record_bytes(payload))
    assert ClassificationCacheSession(root).lookup(record)[1] is None


def test_rollup_cache_tracks_observation_keys_and_duplicate_candidates(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first_packet = _commit_packet(root, tmp_path, "rollup-first")
    observation_id = "shared-observation.json"
    observation = {
        "record_id": observation_id,
        "content_hash": "sha256:observation",
        "lane_namespace": "creator_metric_silver",
        "raw_refs": [{"packet_id": first_packet}],
        "derived_refs": [],
    }
    observation_path = root.append_record(
        subtree="derived",
        raw_anchor=first_packet,
        lane="creator_metric_silver",
        record_id=observation_id,
        data=canonical_record_bytes(observation),
    )
    rollup = {
        "content_hash": "sha256:rollup",
        "lane_namespace": "creator_metric_rollup_silver",
        "raw_refs": [],
        "derived_refs": [
            {
                "raw_anchor": first_packet,
                "lane_namespace": "creator_metric_silver",
                "record_id": observation_id,
                "content_hash": observation["content_hash"],
            }
        ],
    }
    cache = ClassificationCacheSession(root, use_existing=False)
    cache.lookup(observation, record_path=observation_path)
    key, authority = cache.lookup(rollup)
    assert key is not None
    assert authority is None
    cache.remember(
        key,
        SilverSourceAuthority(CURRENT_SOURCE_BACKED_AUTHORITY, "test_current"),
    )
    cache.save()
    reloaded = ClassificationCacheSession(root)
    reloaded.lookup(observation, record_path=observation_path)
    assert reloaded.lookup(rollup)[1] is not None

    loaded_packet = root.load_raw_packet(first_packet)
    preserved = loaded_packet.manifest["preserved_files"][0]
    body_path = root._within("raw", raw_shard(first_packet), first_packet).joinpath(
        *preserved["relative_packet_path"].replace("\\", "/").split("/")
    )
    original_body = body_path.read_bytes()
    body_path.unlink()
    changed = ClassificationCacheSession(root)
    changed.lookup(observation, record_path=observation_path)
    assert changed.lookup(rollup)[1] is None

    body_path.write_bytes(original_body)
    restored_cache = ClassificationCacheSession(root)
    restored_cache.lookup(observation, record_path=observation_path)
    restored_key, restored_authority = restored_cache.lookup(rollup)
    assert restored_key is not None
    assert restored_authority is None
    restored_cache.remember(
        restored_key,
        SilverSourceAuthority(CURRENT_SOURCE_BACKED_AUTHORITY, "test_current"),
    )
    restored_cache.save()

    second_packet = _commit_packet(root, tmp_path, "rollup-second")
    duplicate = {
        **observation,
        "raw_refs": [{"packet_id": second_packet}],
    }
    duplicate_path = root.append_record(
        subtree="derived",
        raw_anchor=second_packet,
        lane="creator_metric_silver",
        record_id=observation_id,
        data=canonical_record_bytes(duplicate),
    )
    duplicated = ClassificationCacheSession(root)
    duplicated.lookup(observation, record_path=observation_path)
    duplicated.lookup(duplicate, record_path=duplicate_path)
    assert duplicated.lookup(rollup)[1] is None


def test_incremental_equality_and_integrity_audit_are_read_only_gates(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    _seeded_root(root, tmp_path)
    rebuild_derived_retrieval(
        root, product_mention_policy=_POLICY, stamp=_STAMP
    )
    target_root = _current_core(root)
    before = {
        path.relative_to(target_root).as_posix(): path.read_bytes()
        for path in sorted(target_root.rglob("*.json"))
    }

    equality = prove_incremental_rebuild_equality(
        root, product_mention_policy=_POLICY
    )
    assert equality["status"] == "proven"
    assert equality["mismatched_files"] == []
    assert equality["incremental_classification_cache"]["hits"] > 0

    audit = audit_derived_retrieval_source_integrity(root)
    assert audit["status"] == "proven"
    assert audit["mode"] == "source_integrity_audit"
    after = {
        path.relative_to(target_root).as_posix(): path.read_bytes()
        for path in sorted(target_root.rglob("*.json"))
    }
    assert after == before


def _write_creator_metric_record(
    root: DataLakeRoot,
    raw_anchor: str,
    record_id: str,
    *,
    subject_ref: dict,
) -> None:
    """One strict-current MetricObservation with an account-bearing subject."""
    record = {
        "record_id": record_id,
        "raw_anchor": raw_anchor,
        "lane_namespace": "creator_metric_silver",
        "producer_id": "test.creator_metric_producer",
        "schema_version": "silver_vault_record_v0",
        "producer_schema_version": "test_creator_metric_v1",
        "content_hash": "",
        "content_hash_basis": "canonical_json_excluding_content_hash",
        "record_kind": "observation",
        "payload_kind": "MetricObservation",
        "producer_row_kind": "test_creator_metric",
        "source_surface": "test_surface",
        "observed_at": "2026-07-15T00:00:00Z",
        "captured_at": "2026-07-15T00:00:00Z",
        **{
            key: value
            for key, value in _complete_lineage_fields(root, raw_anchor).items()
            if key in ("raw_refs", "derived_refs")
        },
        "payload": {
            "observation": {
                "subject": {"ref_type": "entity_key", "ref": subject_ref},
                "metric_name": "follower_count",
                "metric_value": 1000,
                "metric_posture": {"kind": "observed", "reason_code": None, "reason_detail": None},
            }
        },
    }
    record["content_hash"] = "sha256:" + silver_content_hash(record)
    root.append_record(
        subtree="derived",
        raw_anchor=raw_anchor,
        lane="creator_metric_silver",
        record_id=record_id,
        data=canonical_record_bytes(record),
    )


def _write_fragrantica_projection(
    root: DataLakeRoot,
    raw_anchor: str,
    *,
    record_id: str = "projection.json",
    rows: list[dict] | None = None,
) -> None:
    projection = {
        "packet_id": raw_anchor,
        "certification": "view_only; not_cleaned; not_normalized; not_judgment_ready",
        "rows": rows or [
            {
                "row_id": "slice_01:fragrantica:product_snapshot",
                "row_kind": "fragrance_product_snapshot",
                "brand_or_house": "Ariana Grande",
                "source_object_name": "Cloud",
                "source_object_site_id": "50384",
                "source_platform": "fragrantica",
                "source_visible_fields": {
                    "canonical_url": "https://www.fragrantica.com/perfume/Ariana-Grande/Cloud-50384.html"
                },
            }
        ],
    }
    root.append_record(
        subtree="derived",
        raw_anchor=raw_anchor,
        lane="projection_fragrantica",
        record_id=record_id,
        data=canonical_record_bytes(projection),
    )


def test_by_creator_indexes_account_subjects_with_classified_authority(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(root, tmp_path, "creator")
    _write_creator_metric_record(
        root,
        pid,
        "account_metric.json",
        subject_ref={
            "namespace": "instagram",
            "kind": "platform_public_account",
            "native_id": "fixture_creator",
            "orca_platform_account_id": "acct_ig_fixture_001",
        },
    )
    _write_creator_metric_record(
        root,
        pid,
        "content_metric.json",
        subject_ref={
            "namespace": "youtube",
            "kind": "public_content_object",
            "native_id": "vid123",
            "published_by_account_native_id": "UCfixturechannel",
        },
    )

    view, source_refs = build_by_creator_view(root)

    assert view["creator_count"] == 2
    ig_entry = view["creators"]["instagram"]["unspecified"]["fixture_creator"]
    assert ig_entry["aliases"]["orca_platform_account_id"] == "acct_ig_fixture_001"
    evidence = ig_entry["packets"][pid]["subject_evidence"]
    assert [ref["record_id"] for ref in evidence] == ["account_metric.json"]
    assert evidence[0]["authority_status"] == "current_source_backed"
    lane_status = ig_entry["packets"][pid]["anchor_silver_records_by_lane_status"]
    assert lane_status["creator_metric_silver"] == {"current_source_backed": 2}
    # content-object subject keys under its publishing account
    assert "UCfixturechannel" in view["creators"]["youtube"]["unspecified"]
    assert f"{pid}/creator_metric_silver/account_metric.json" in source_refs


def test_by_creator_distinct_identity_kinds_never_merge(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(root, tmp_path, "creator-kind-split")
    _write_creator_metric_record(
        root,
        pid,
        "id_keyed.json",
        subject_ref={
            "namespace": "youtube",
            "kind": "platform_public_account",
            "native_id": "same_string",
            "native_id_kind": "youtube_channel_id",
        },
    )
    _write_creator_metric_record(
        root,
        pid,
        "handle_keyed.json",
        subject_ref={
            "namespace": "youtube",
            "kind": "platform_public_account",
            "native_id": "same_string",
        },
    )

    view, _source_refs = build_by_creator_view(root)

    kinds = view["creators"]["youtube"]
    assert "same_string" in kinds["youtube_channel_id"]
    assert "same_string" in kinds["unspecified"]
    assert view["creator_count"] == 2


def test_by_creator_unfileable_account_shapes_are_named_residuals(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(root, tmp_path, "creator-unfiled")
    # Unknown platform namespace: never a new platform key, always a residual.
    _write_creator_metric_record(
        root,
        pid,
        "unknown_namespace.json",
        subject_ref={
            "namespace": "myspace",
            "kind": "platform_public_account",
            "native_id": "fixture_creator",
        },
    )
    # Account subject missing its identifier: residual, not a silent drop.
    _write_creator_metric_record(
        root,
        pid,
        "missing_native_id.json",
        subject_ref={
            "namespace": "instagram",
            "kind": "platform_public_account",
            "native_id": "",
        },
    )
    # Unknown subject kind carrying an account-identifier field: residual.
    _write_creator_metric_record(
        root,
        pid,
        "unknown_kind.json",
        subject_ref={
            "namespace": "instagram",
            "kind": "reddit_author_profile",
            "native_id": "some_author",
        },
    )
    # Known non-account subject kind: neither a card nor a residual.
    _write_creator_metric_record(
        root,
        pid,
        "retail_product.json",
        subject_ref={
            "namespace": "sephora",
            "kind": "retailer_product",
            "native_id": "P12345",
        },
    )

    view, _source_refs = build_by_creator_view(root)

    assert view["creators"] == {}
    statuses = sorted(
        (residual["status"], residual["record_id"])
        for residual in view["residuals"]
        if residual["status"].startswith("unrecognized_")
    )
    assert statuses == [
        ("unrecognized_account_subject_shape", "missing_native_id.json"),
        ("unrecognized_account_subject_shape", "unknown_kind.json"),
        ("unrecognized_platform_namespace", "unknown_namespace.json"),
    ]


def test_by_creator_surfaces_conflicting_account_aliases(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(root, tmp_path, "creator-alias-conflict")
    for record_id, account_id in (
        ("first.json", "acct_ig_fixture_001"),
        ("second.json", "acct_ig_fixture_002"),
    ):
        _write_creator_metric_record(
            root,
            pid,
            record_id,
            subject_ref={
                "namespace": "instagram",
                "kind": "platform_public_account",
                "native_id": "fixture_creator",
                "orca_platform_account_id": account_id,
            },
        )

    view, _source_refs = build_by_creator_view(root)

    assert view["creators"]["instagram"]["unspecified"]["fixture_creator"]["aliases"] == {
        "orca_platform_account_id": "acct_ig_fixture_001"
    }
    assert any(
        residual["status"] == "account_alias_conflict"
        and residual["namespace"] == "instagram"
        and residual["identity_kind"] == "unspecified"
        and residual["native_id"] == "fixture_creator"
        and residual["alias_values"]
        == ["acct_ig_fixture_001", "acct_ig_fixture_002"]
        for residual in view["residuals"]
    )


def test_incremental_and_cold_alias_conflicts_are_byte_identical(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first = "01J00000000000000000000003"
    second = "01J00000000000000000000004"
    assert first < second
    assert raw_shard(first) > raw_shard(second)

    for packet_id, account_id in (
        (first, "acct_ig_fixture_002"),
        (second, "acct_ig_fixture_001"),
    ):
        commit_raw_packet(
            root,
            packet_id=packet_id,
            body=f'{{"packet_id": "{packet_id}"}}'.encode(),
        )
        root.record_availability(packet_id)
        _write_creator_metric_record(
            root,
            packet_id,
            "account_metric.json",
            subject_ref={
                "namespace": "instagram",
                "kind": "platform_public_account",
                "native_id": "fixture_creator",
                "orca_platform_account_id": account_id,
            },
        )

    report = prove_incremental_rebuild_equality(
        root, product_mention_policy=_POLICY
    )

    assert report["status"] == "proven"
    assert report["mismatched_files"] == []


def test_by_mention_carries_native_product_page_identity(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(root, tmp_path, "product")
    _write_fragrantica_projection(root, pid)

    view, source_refs = build_by_mention_view(root, product_mention_policy=_POLICY)

    entry = view["native_product_pages"]["Ariana Grande"]["Cloud"]
    assert len(entry) == 1
    assert entry[0]["raw_anchor"] == pid
    assert entry[0]["site_native_id"] == "50384"
    assert entry[0]["canonical_url"].endswith("Cloud-50384.html")
    assert "not Silver authority" in entry[0]["identity_source"]
    assert f"{pid}/projection_fragrantica/projection.json" in source_refs
    assert "never be read as an observed zero" in view["zero_rows_meaning"]


def test_by_mention_rejects_partial_and_conflicting_native_product_identity(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(root, tmp_path, "product-identity")
    base_row = {
        "row_kind": "fragrance_product_snapshot",
        "brand_or_house": "Ariana Grande",
        "source_object_name": "Cloud",
        "source_object_site_id": "50384",
        "source_platform": "fragrantica",
    }
    _write_fragrantica_projection(
        root,
        pid,
        record_id="first.json",
        rows=[
            {
                **base_row,
                "row_id": "first",
                "source_visible_fields": {
                    "canonical_url": "https://www.fragrantica.com/perfume/Ariana-Grande/Cloud-50384.html"
                },
            },
            {
                **base_row,
                "row_id": "missing-brand",
                "brand_or_house": None,
                "source_object_name": "Cloud Pink",
                "source_object_site_id": "81442",
                "source_visible_fields": {
                    "canonical_url": "https://www.fragrantica.com/perfume/Ariana-Grande/Cloud-Pink-81442.html"
                },
            },
        ],
    )
    _write_fragrantica_projection(
        root,
        pid,
        record_id="second.json",
        rows=[
            {
                **base_row,
                "row_id": "second",
                "brand_or_house": "Impostor Brand",
                "source_visible_fields": {
                    "canonical_url": "https://www.fragrantica.com/perfume/Ariana-Grande/Cloud-50384.html?duplicate=1"
                },
            }
        ],
    )

    view, source_refs = build_by_mention_view(root, product_mention_policy=_POLICY)

    assert "unknown" not in view["native_product_pages"]
    assert "Impostor Brand" not in view["native_product_pages"]
    assert len(view["native_product_pages"]["Ariana Grande"]["Cloud"]) == 1
    statuses = [residual["status"] for residual in view["residuals"]]
    assert "native_product_page_identity_incomplete" in statuses
    assert "native_product_page_identity_conflict" in statuses
    assert f"{pid}/projection_fragrantica/first.json" in source_refs
    assert f"{pid}/projection_fragrantica/second.json" in source_refs


def test_lookup_runner_resolves_creator_and_mention(tmp_path: Path, capsys, monkeypatch) -> None:
    from runners.run_derived_retrieval_lookup import main as lookup_main

    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid = _commit_packet(root, tmp_path, "creator")
    _write_creator_metric_record(
        root,
        pid,
        "account_metric.json",
        subject_ref={
            "namespace": "instagram",
            "kind": "platform_public_account",
            "native_id": "fixture_creator",
            "orca_platform_account_id": "acct_ig_fixture_001",
        },
    )
    _write_fragrantica_projection(root, pid)
    rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
    monkeypatch.setattr(DataLakeRoot, "resolve_readonly", staticmethod(lambda **_kwargs: root))

    assert lookup_main(["--creator", "fixture_creator"]) == 0
    found = json.loads(capsys.readouterr().out)
    assert found["status"] == "found"
    assert found["matches"][0]["namespace"] == "instagram"
    assert found["matches"][0]["identity_kind"] == "unspecified"
    assert found["view_provenance"]["generation_id"] == _STAMP["generation_id"]

    assert lookup_main(["--creator", "acct_ig_fixture_001"]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "found"

    assert lookup_main(["--mention", "cloud"]) == 0
    mention = json.loads(capsys.readouterr().out)
    assert mention["matches"][0]["source_class"] == "native_product_pages"
    assert mention["matches"][0]["brand"] == "Ariana Grande"

    assert lookup_main(["--mention", "grand"]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "not_found"

    assert lookup_main(["--creator", "nobody_here"]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "not_found"


def test_lookup_runner_fails_closed_on_absent_or_tampered_view_pair(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    from runners.run_derived_retrieval_lookup import main as lookup_main

    root = DataLakeRoot.for_test(tmp_path / "lake")
    monkeypatch.setattr(DataLakeRoot, "resolve_readonly", staticmethod(lambda **_kwargs: root))

    assert lookup_main(["--creator", "fixture_creator"]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "view_not_built"

    pid = _commit_packet(root, tmp_path, "tampered-view")
    _write_fragrantica_projection(root, pid)
    rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
    view_path = _current_core(root) / "query_tables" / "by_mention.json"
    tampered = json.loads(view_path.read_text(encoding="utf-8"))
    tampered["native_product_pages"]["Ariana Grande"]["Cloud"][0][
        "canonical_url"
    ] = "https://example.test/tampered"
    view_path.write_bytes(canonical_record_bytes(tampered))

    assert lookup_main(["--mention", "cloud"]) == 2
    error = json.loads(capsys.readouterr().out)
    assert error["status"] == "error"
    assert "view_sha256" in error["error"]


def test_runner_cli_fails_closed_on_in_repo_root(tmp_path: Path, capsys) -> None:
    # tmp_path lives inside the repo working tree; production resolution must
    # refuse it (write-boundary fail-closed rule), exit 2, and write nothing.
    from runners.run_data_lake_indexes_rebuild import main

    assert main(["--root", str(tmp_path / "lake"), "--target", "all", *_POLICY_ARGS]) == 2
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "error"


def test_runner_cli_bootstraps_active_policy_once(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    from runners.run_data_lake_indexes_rebuild import main

    root = DataLakeRoot.for_test(tmp_path / "lake")
    monkeypatch.setattr(DataLakeRoot, "resolve", staticmethod(lambda **_kwargs: root))
    expected_policy = {
        "policy_version": EXTRACTOR_RUBRIC_VERSION,
        "policy_fingerprint_sha256": product_mentions_policy_fingerprint(
            EXTRACTOR_RUBRIC_VERSION
        ),
    }

    assert main(
        [
            "--root",
            str(root.path),
            "--target",
            "derived_retrieval",
            "--bootstrap-active-product-mention-policy",
        ]
    ) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "ok"
    assert report["product_mention_policy_source"] == "active_checkout_bootstrap"
    assert report["product_mention_policy"] == expected_policy
    manifest = json.loads(
        (_current_core(root) / "manifests" / "by_mention.json").read_text(
            encoding="utf-8"
        )
    )
    assert (
        manifest["selection_policy_versions"]["product_mention_policy"]
        == expected_policy
    )

    assert main(
        [
            "--root",
            str(root.path),
            "--target",
            "derived_retrieval",
            "--bootstrap-active-product-mention-policy",
        ]
    ) == 2
    report = json.loads(capsys.readouterr().out)
    assert "fresh-root only" in report["error"]

    assert main(
        [
            "--root",
            str(root.path),
            "--target",
            "derived_retrieval",
            "--use-stored-product-mention-policy",
        ]
    ) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["product_mention_policy_source"] == "stored_manifest"
    assert report["product_mention_policy"] == expected_policy


def test_runner_cli_rebuild_then_prove(tmp_path: Path, capsys, monkeypatch) -> None:
    from runners.run_data_lake_indexes_rebuild import main

    root = DataLakeRoot.for_test(tmp_path / "lake")
    _seeded_root(root, tmp_path)
    # resolve() correctly refuses in-repo test roots (covered above); inject the
    # verified test root to exercise the runner's rebuild/prove flow itself.
    monkeypatch.setattr(DataLakeRoot, "resolve", staticmethod(lambda **_kwargs: root))

    assert main(["--root", str(root.path), "--target", "all", *_POLICY_ARGS]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "ok"
    assert report["availability"]["status"] == "rebuilt"
    assert report["derived_retrieval"]["status"] == "rebuilt"

    assert main(["--root", str(root.path), "--target", "all", "--prove-rebuildability"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["availability"]["status"] == "proven"
    assert report["derived_retrieval"]["status"] == "proven"

    assert main(
        [
            "--root",
            str(root.path),
            "--target",
            "derived_retrieval",
            "--use-stored-product-mention-policy",
        ]
    ) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["mode"] == "incremental_rebuild"
    assert report["derived_retrieval"]["status"] == "current"
    assert report["derived_retrieval"]["source_inventory"]["source_body_reads"] == 0

    assert main(
        [
            "--root",
            str(root.path),
            "--target",
            "derived_retrieval",
            "--use-stored-product-mention-policy",
            "--prove-incremental-equality",
        ]
    ) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["mode"] == "prove_incremental_equality"
    assert report["derived_retrieval"]["status"] == "proven"

    assert main(
        [
            "--root",
            str(root.path),
            "--target",
            "derived_retrieval",
            "--audit-source-integrity",
        ]
    ) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["mode"] == "audit_source_integrity"
    assert report["derived_retrieval"]["status"] == "proven"

    view_path = _current_core(root) / "query_tables" / "by_mention.json"
    view_path.write_bytes(view_path.read_bytes() + b" ")
    assert main(["--root", str(root.path), "--target", "derived_retrieval", "--prove-rebuildability"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "failed"
    assert report["derived_retrieval"]["failures"] == ["by_mention"]
