"""derived_retrieval object-level view builder + rebuild runner tests.

Covers the seam contract's Rebuild Command Binding: manifest-backed rebuildable
views, the by_mention read-side lineage gate, the undone view's documented
weaker semantics, and a prove-rebuildability that fails on tampered bytes
(never self-comparing).
"""
from __future__ import annotations

import json
import hashlib
from pathlib import Path

from data_lake.canonical_json import canonical_record_bytes
from data_lake.consumption import append_ack
from data_lake.derived_retrieval_views import (
    MENTIONS_LANE,
    build_by_mention_view,
    prove_derived_retrieval_rebuildability,
    rebuild_derived_retrieval,
)
from data_lake.root import DataLakeRoot
from data_lake.silver_lineage import (
    SilverAnchor,
    SilverLineage,
    SilverRawRef,
    SilverSourceObject,
)
from data_lake.silver_record import silver_content_hash
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet

_STAMP = {"generation_id": "0" * 32, "generated_at": "2026-07-02T00:00:00+00:00"}
_NS = "projection_ig"


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


def _complete_lineage_fields(packet_id: str) -> dict:
    lineage = SilverLineage(
        producer_id="test.producer",
        producer_schema_version="v0",
        source_surface="youtube_captions",
        source_object=SilverSourceObject(namespace="youtube", kind="transcript", native_id="vid1"),
        raw_refs=[
            SilverRawRef(
                packet_id=packet_id,
                file_id="f1",
                relative_packet_path="preserved/f1.json",
                sha256="a" * 64,
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
                "policy_version": "v0",
                "policy_fingerprint_sha256": "a" * 64,
                "row_count": len(rows),
                "rows": rows,
            }
        },
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
            **_complete_lineage_fields(first),
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


def test_rebuild_builds_views_and_manifests(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first, second = _seeded_root(root, tmp_path)

    report = rebuild_derived_retrieval(root, stamp=_STAMP)
    assert report["status"] == "rebuilt"
    assert report["views"] == ["by_mention", "undone"]
    assert report["deferred_views"] == ["by_creator"]

    object_level = root.path / "indexes" / "derived_retrieval" / "object_level"
    by_mention = json.loads((object_level / "by_mention" / "view.json").read_text("utf-8"))
    undone = json.loads((object_level / "undone" / "view.json").read_text("utf-8"))

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

    for view_name in ("by_mention", "undone"):
        manifest = json.loads(
            (object_level / view_name / "manifest.json").read_text("utf-8")
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
    view, _refs = build_by_mention_view(root)
    assert view["mentions"] == {}
    assert view["residuals"][0]["status"] == "unreadable"


def test_prove_rebuildability_green_then_tamper_fails(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    _seeded_root(root, tmp_path)
    rebuild_derived_retrieval(root, stamp=_STAMP)

    proof = prove_derived_retrieval_rebuildability(root)
    assert proof["status"] == "proven"
    assert proof["results"] == {"by_mention": "rebuildable", "undone": "rebuildable"}

    view_path = (
        root.path / "indexes" / "derived_retrieval" / "object_level" / "undone" / "view.json"
    )
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
    rebuild_derived_retrieval(root, stamp=_STAMP)
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
        "by_mention": "absent_nothing_to_prove",
        "undone": "absent_nothing_to_prove",
    }


def test_runner_cli_fails_closed_on_in_repo_root(tmp_path: Path, capsys) -> None:
    # tmp_path lives inside the repo working tree; production resolution must
    # refuse it (write-boundary fail-closed rule), exit 2, and write nothing.
    from runners.run_data_lake_indexes_rebuild import main

    assert main(["--root", str(tmp_path / "lake"), "--target", "all"]) == 2
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "error"


def test_runner_cli_rebuild_then_prove(tmp_path: Path, capsys, monkeypatch) -> None:
    from runners.run_data_lake_indexes_rebuild import main

    root = DataLakeRoot.for_test(tmp_path / "lake")
    _seeded_root(root, tmp_path)
    # resolve() correctly refuses in-repo test roots (covered above); inject the
    # verified test root to exercise the runner's rebuild/prove flow itself.
    monkeypatch.setattr(DataLakeRoot, "resolve", staticmethod(lambda **_kwargs: root))

    assert main(["--root", str(root.path), "--target", "all"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "ok"
    assert report["availability"]["status"] == "rebuilt"
    assert report["derived_retrieval"]["status"] == "rebuilt"

    assert main(["--root", str(root.path), "--target", "all", "--prove-rebuildability"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["availability"]["status"] == "proven"
    assert report["derived_retrieval"]["status"] == "proven"

    view_path = (
        root.path / "indexes" / "derived_retrieval" / "object_level" / "by_mention" / "view.json"
    )
    view_path.write_bytes(view_path.read_bytes() + b" ")
    assert main(["--root", str(root.path), "--target", "derived_retrieval", "--prove-rebuildability"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "failed"
    assert report["derived_retrieval"]["failures"] == ["by_mention"]
