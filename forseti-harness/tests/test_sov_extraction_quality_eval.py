"""SoV extraction-quality eval runner tests (measurement honesty).

Pins the eval's counted-never-dropped dispositions: leak vs present
classification (casefold substring over resolved caption transcript),
unknown-brand mentions never scanned, gate-failing and unreadable records
counted but never scanned, unresolvable transcript refs counted with named
mentions going to unscannable, and the runner's read-only fail-closed CLI.
"""
from __future__ import annotations

import json
import hashlib
from pathlib import Path

from data_lake.canonical_json import canonical_record_bytes
from data_lake.derived_retrieval_views import MENTIONS_LANE
from data_lake.root import DataLakeRoot
from data_lake.silver_record import (
    CONTENT_HASH_BASIS,
    SILVER_VAULT_RECORD_SCHEMA_VERSION,
    TEXT_OBSERVATION_SET_PAYLOAD_KIND,
    silver_content_hash,
)
from data_lake.silver_lineage import (
    SilverAnchor,
    SilverDerivedRef,
    SilverLineage,
    SilverRawRef,
    SilverSourceObject,
)
from runners.run_sov_extraction_quality_eval import main, run_eval
from source_capture.models import known_fact
_POLICY = {"policy_version": "test_policy_v1", "policy_fingerprint_sha256": "1" * 64}
_POLICY_ARGS = [
    "--product-mention-policy-version", "test_policy_v1",
    "--product-mention-policy-fingerprint-sha256", "1" * 64,
]
from source_capture.writer import write_local_source_capture_packet


def _json3(text: str) -> str:
    return json.dumps(
        {"events": [{"tStartMs": 0, "dDurationMs": 1000, "segs": [{"utf8": text}]}]}
    )


def _commit_caption_packet(
    root: DataLakeRoot, tmp_path: Path, name: str, transcript_text: str
) -> tuple[str, dict]:
    """Commit a packet whose preserved file is a real caption json3; returns
    (packet_id, json3 preserved-file manifest entry)."""
    src = tmp_path / f"{name}.json3"
    src.write_text(_json3(transcript_text), encoding="utf-8")
    receipt = write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family="youtube",
        source_surface="youtube_captions",
        source_locator=known_fact(f"https://www.youtube.com/watch?v={name}"),
        decision_question="q",
        capture_context="sov eval test",
    )
    packet_id = receipt.packet.packet_id
    manifest = json.loads(
        (root.find_packet(packet_id) / "manifest.json").read_text(encoding="utf-8")
    )
    json3_entry = next(
        pf
        for pf in manifest["preserved_files"]
        if str(pf.get("relative_packet_path", "")).endswith(".json3")
    )
    return packet_id, json3_entry


def _lineage_fields(packet_id: str, json3_entry: dict | None, native_id: str) -> dict:
    """Gate-complete lineage fields: a raw json3 ref when an entry is given,
    else a derived (ASR) ref only — gate-complete but with NO transcript raw ref."""
    if json3_entry is not None:
        raw_refs = [
            SilverRawRef(
                packet_id=packet_id,
                file_id=json3_entry["file_id"],
                relative_packet_path=json3_entry["relative_packet_path"],
                sha256=json3_entry["sha256"],
                hash_basis="raw_stored_bytes",
                anchor=SilverAnchor(kind="file"),
                relation="consumed",
            )
        ]
        derived_refs = []
    else:
        raw_refs = []
        derived_refs = [
            SilverDerivedRef(
                raw_anchor=packet_id,
                lane="transcript_asr",
                record_id="asr_x",
                relation="consumed",
            )
        ]
    lineage = SilverLineage(
        producer_id="test.producer",
        producer_schema_version="v0",
        source_surface="youtube_captions",
        source_object=SilverSourceObject(
            namespace="youtube", kind="transcript", native_id=native_id
        ),
        raw_refs=raw_refs,
        derived_refs=derived_refs,
    )
    return lineage.to_record_fields()


def _mention(mention_id: str, brand: str, line: str) -> dict:
    return {
        "mention_id": mention_id,
        "brand": brand,
        "line": line,
        "source_pointer": f"quote {mention_id}",
        "start_ms": 0,
        "end_ms": 100,
    }


def _write_record(root: DataLakeRoot, raw_anchor: str, record_id: str, record: dict) -> None:
    mentions = record.get("mentions")
    if isinstance(mentions, list):
        record = _official_record(
            raw_anchor=raw_anchor,
            record_id=record_id,
            mentions=mentions,
            lineage_fields={key: value for key, value in record.items() if key != "mentions"},
        )
    root.append_record(
        subtree="derived",
        raw_anchor=raw_anchor,
        lane=MENTIONS_LANE,
        record_id=record_id,
        data=canonical_record_bytes(record),
    )


def _official_record(
    *, raw_anchor: str, record_id: str, mentions: list[dict], lineage_fields: dict
) -> dict:
    rows = []
    for mention in mentions:
        quote = mention["source_pointer"]
        rows.append(
            {
                "row_id": mention["mention_id"],
                "text_artifact_type": "transcript_quote",
                "text_value": quote,
                "text_ref": None,
                "text_hash": f"sha256:{hashlib.sha256(quote.encode('utf-8')).hexdigest()}",
                "text_posture": {"kind": "observed", "reason_code": None, "reason_detail": None},
                "coverage_window": {"start": None, "end": None},
                "source_span": {"start_ms": mention["start_ms"], "end_ms": mention["end_ms"]},
                "mention": mention,
            }
        )
    body = {
        "record_id": record_id,
        "raw_anchor": raw_anchor,
        "lane_namespace": MENTIONS_LANE,
        "producer_id": "test.producer",
        "schema_version": SILVER_VAULT_RECORD_SCHEMA_VERSION,
        "producer_schema_version": "transcript_product_mentions_record_v1",
        "content_hash": "",
        "content_hash_basis": CONTENT_HASH_BASIS,
        "record_kind": "observation",
        "payload_kind": TEXT_OBSERVATION_SET_PAYLOAD_KIND,
        "producer_row_kind": "transcript_product_mentions",
        "record_schema_version": "transcript_product_mentions_record_v1",
        "source_family": "social_media",
        **lineage_fields,
        "provenance": {"transcript_source_key": record_id},
        "payload": {
            "observation": {
                "subject": {
                    "ref_type": "entity_key",
                    "ref": {"namespace": "youtube", "kind": "public_content_object", "native_id": (lineage_fields.get("source_object") or {}).get("native_id", "unknown")},
                },
                "observation_set_kind": "transcript_product_mentions",
                "policy_version": "test_policy_v1",
                "policy_fingerprint_sha256": "1" * 64,
                "row_count": len(rows),
                "rows": rows,
            }
        },
    }
    body["content_hash"] = f"sha256:{silver_content_hash(body)}"
    return body


def test_leak_scan_classifies_present_leaked_unknown(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid, json3_entry = _commit_caption_packet(
        root, tmp_path, "alpha", "today I review Dior Sauvage and love it"
    )
    _write_record(
        root,
        pid,
        "m1.json",
        {
            "mentions": [
                _mention("m-1", "Dior", "Sauvage"),  # present (casefold substring)
                _mention("m-2", "Creed", "Aventus"),  # leaked: never spoken
                _mention("m-3", "unknown", "mystery"),  # unknown: never scanned
            ],
            **_lineage_fields(pid, json3_entry, "vid1"),
        },
    )

    report = run_eval(root, product_mention_policy=_POLICY)

    scan = report["knowledge_leak_scan"]
    assert scan["named_mentions_scanned"] == 2
    assert scan["brand_present_in_transcript"] == 1
    assert scan["brand_absent_from_transcript_leaked"] == 1
    assert scan["leak_rate"] == 0.5
    assert scan["per_brand"]["Dior"] == {
        "mentions": 1,
        "scanned": 1,
        "leaked": 0,
        "unscannable": 0,
    }
    assert scan["per_brand"]["Creed"] == {
        "mentions": 1,
        "scanned": 1,
        "leaked": 1,
        "unscannable": 0,
    }
    assert scan["leaked_samples"][0]["brand"] == "Creed"
    assert scan["leaked_samples"][0]["raw_anchor"] == pid

    substrate = report["substrate"]
    assert substrate["mentions_named_brand"] == 2
    assert substrate["mentions_unknown_or_blank_brand"] == 1
    assert substrate["mention_records_by_selection_status"] == {"selected_exact_policy": 1}
    assert (
        report["transcript_resolution"]["records_by_disposition"]["resolved_caption_json3"] == 1
    )
    assert report["non_claims"]


def test_unresolvable_and_gate_failing_records_are_counted_never_scanned(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid, json3_entry = _commit_caption_packet(root, tmp_path, "alpha", "talking about Dior")
    # Structurally complete record whose derived source does not exist: the
    # physical authority gate excludes it before transcript scanning.
    _write_record(
        root,
        pid,
        "m_noref.json",
        {
            "mentions": [_mention("m-1", "Dior", "Sauvage")],
            **_lineage_fields(pid, None, "vid1"),
        },
    )
    # Gate-FAILING record (no lineage at all): counted by status, never scanned.
    _write_record(
        root,
        pid,
        "m_nolineage.json",
        {"mentions": [_mention("m-2", "Chanel", "Bleu")]},
    )
    # Unreadable record file: counted, never scanned.
    root.append_record(
        subtree="derived",
        raw_anchor=pid,
        lane=MENTIONS_LANE,
        record_id="m_corrupt.json",
        data=b"{not json",
    )

    report = run_eval(root, product_mention_policy=_POLICY)

    assert report["substrate"]["mention_records_total"] == 3
    assert report["substrate"]["mention_records_by_selection_status"] == {
        "invalid_silver_envelope": 1,
        "selected_exact_policy": 0,
        "source_ref_unresolved": 1,
        "unreadable": 1,
    }
    assert report["transcript_resolution"]["records_by_disposition"] == {}
    assert report["transcript_resolution"]["named_mentions_unscannable"] == 0
    assert report["knowledge_leak_scan"]["named_mentions_scanned"] == 0
    assert report["knowledge_leak_scan"]["leak_rate"] is None


def test_raw_ref_mismatches_are_non_authority_not_fallback_scanned(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid, json3_entry = _commit_caption_packet(root, tmp_path, "alpha", "Dior is spoken")

    missing_file_ref = _lineage_fields(pid, json3_entry, "vid1")
    missing_file_ref["raw_refs"][0]["file_id"] = "missing-json3-file"
    _write_record(
        root,
        pid,
        "m_missing_file.json",
        {
            "mentions": [_mention("m-1", "Dior", "Sauvage")],
            **missing_file_ref,
        },
    )

    bad_hash_ref = _lineage_fields(pid, json3_entry, "vid2")
    bad_hash_ref["raw_refs"][0]["sha256"] = "0" * 64
    _write_record(
        root,
        pid,
        "m_bad_hash.json",
        {
            "mentions": [_mention("m-2", "Dior", "Sauvage")],
            **bad_hash_ref,
        },
    )

    report = run_eval(root, product_mention_policy=_POLICY)

    # Neither record may be scanned against a substitute transcript: the wrong
    # file_id and the wrong hash fail the shared physical authority gate.
    assert report["knowledge_leak_scan"]["named_mentions_scanned"] == 0
    assert report["substrate"]["mention_records_by_selection_status"] == {
        "selected_exact_policy": 0,
        "source_ref_unresolved": 2,
    }
    assert report["transcript_resolution"]["named_mentions_unscannable"] == 0
    assert report["transcript_resolution"]["records_by_disposition"] == {}
    assert report["knowledge_leak_scan"]["per_brand"] == {}


def test_records_without_named_mentions_get_not_attempted_disposition(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid, json3_entry = _commit_caption_packet(root, tmp_path, "alpha", "unknown sample")
    _write_record(
        root,
        pid,
        "m_unknown_only.json",
        {
            "mentions": [_mention("m-1", "unknown", "mystery")],
            **_lineage_fields(pid, json3_entry, "vid1"),
        },
    )

    report = run_eval(root, product_mention_policy=_POLICY)

    assert report["substrate"]["mentions_unknown_or_blank_brand"] == 1
    assert report["transcript_resolution"]["records_by_disposition"] == {
        "not_attempted_no_named_mentions": 1
    }
    assert report["knowledge_leak_scan"]["named_mentions_scanned"] == 0


def test_runner_cli_fails_closed_on_in_repo_root(tmp_path: Path, capsys) -> None:
    assert main(["--root", str(tmp_path / "lake"), *_POLICY_ARGS]) == 2
    out = json.loads(capsys.readouterr().out)
    assert out["status"] == "error"


def test_runner_cli_reports_and_refuses_out_inside_lake(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    pid, json3_entry = _commit_caption_packet(root, tmp_path, "alpha", "I love Dior Sauvage")
    _write_record(
        root,
        pid,
        "m1.json",
        {
            "mentions": [_mention("m-1", "Dior", "Sauvage")],
            **_lineage_fields(pid, json3_entry, "vid1"),
        },
    )
    monkeypatch.setattr(DataLakeRoot, "resolve", staticmethod(lambda **_kwargs: root))

    out_file = tmp_path / "report.json"
    assert main(["--root", str(root.path), "--out", str(out_file), *_POLICY_ARGS]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["knowledge_leak_scan"]["leak_rate"] == 0.0
    assert json.loads(out_file.read_text(encoding="utf-8")) == printed

    # --out inside the data root is refused (read-only eval never writes into the lake).
    assert main(["--root", str(root.path), "--out", str(root.path / "indexes" / "x.json"), *_POLICY_ARGS]) == 2
    refused = json.loads(capsys.readouterr().out)
    assert refused["status"] == "error"
    assert not (root.path / "indexes" / "x.json").exists()
