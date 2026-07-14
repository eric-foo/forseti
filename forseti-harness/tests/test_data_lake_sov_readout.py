"""Share-of-voice readout conformance tests (metric-family field contract).

Pins the SoV field contract's load-bearing clauses against
``data_lake.sov_readout``: mention-LEVEL refs with ``mention_count ==
len(mention_refs)``, the read-side Silver lineage gate as counted exclusions,
declared-cohort scoping and reconciliation, window-basis inclusion rules
(capture_time fallback to the packet manifest; publication-time missing-basis
counting), observed-zero-only zero semantics behind a declared comparison_set,
the empty-scope posture (never a table of zeros), and materialization with a
prove-rebuildability that fails on tampered bytes or post-generation source
change (never self-comparing).
"""
from __future__ import annotations

import json
import hashlib
from pathlib import Path

import pytest

from data_lake.canonical_json import canonical_record_bytes
from data_lake.derived_retrieval_views import MENTIONS_LANE
from data_lake.root import DataLakeRoot
from data_lake.silver_lineage import (
    SilverAnchor,
    SilverLineage,
    SilverRawRef,
    SilverSourceObject,
)
from data_lake.silver_record import silver_content_hash
from data_lake.sov_readout import (
    METRIC_FAMILY,
    SovSpecError,
    compute_sov_readout,
    materialize_sov_readout,
    prove_sov_rebuildability,
    sov_readout_id,
)
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet

_STAMP = {"generation_id": "0" * 32, "generated_at": "2026-07-03T00:00:00+00:00"}

_POLICY = {"policy_version": "rubric_v0", "policy_fingerprint_sha256": "a" * 64}

def _commit_packet(root: DataLakeRoot, tmp_path: Path, body: str) -> str:
    src = tmp_path / f"{body}.json"
    src.write_text(f'{{"b": "{body}"}}', encoding="utf-8")
    receipt = write_local_source_capture_packet(
        data_root=root,
        input_files=[src],
        source_family="youtube",
        source_surface="youtube_captions",
        source_locator=known_fact(f"https://www.youtube.com/watch?v={body}"),
        decision_question="q",
        capture_context="sov readout test",
    )
    return receipt.packet.packet_id


def _lineage_fields(
    root: DataLakeRoot,
    packet_id: str,
    native_id: str,
    *,
    captured_at: str | None = None,
    observed_at: str | None = None,
) -> dict:
    manifest = json.loads(
        (root.find_packet(packet_id) / "manifest.json").read_text(encoding="utf-8")
    )
    preserved = manifest["preserved_files"][0]
    lineage = SilverLineage(
        producer_id="test.producer",
        producer_schema_version="v0",
        source_surface="youtube_captions",
        source_object=SilverSourceObject(
            namespace="youtube", kind="transcript", native_id=native_id
        ),
        captured_at=captured_at,
        observed_at=observed_at,
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


def _mention(mention_id: str, brand: str, line: str, start_ms: int = 0) -> dict:
    return {
        "mention_id": mention_id,
        "brand": brand,
        "line": line,
        "source_pointer": f"quote for {mention_id}",
        "start_ms": start_ms,
        "end_ms": start_ms + 100,
    }


def _write_record(root: DataLakeRoot, raw_anchor: str, record_id: str, record: dict) -> None:
    mentions = record.pop("mentions", [])
    source_object = record.get("source_object") if isinstance(record.get("source_object"), dict) else {}
    native_id = str(source_object.get("native_id") or "unknown")
    rows = []
    for index, mention in enumerate(mentions):
        quote = str(mention.get("source_pointer") or f"malformed quote {index}") if isinstance(mention, dict) else f"malformed quote {index}"
        rows.append(
            {
                "row_id": f"row-{index}",
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
                "subject": {"ref_type": "entity_key", "ref": {"namespace": "youtube", "kind": "public_content_object", "native_id": native_id}},
                "observation_set_kind": "transcript_product_mentions",
                "policy_version": "rubric_v0",
                "policy_fingerprint_sha256": "a" * 64,
                "row_count": len(rows),
                "rows": rows,
            }
        },
        "provenance": {
            "rubric_version": record.get("rubric_version", "rubric_v0"),
            "transcript_source_key": record.get("transcript_source_key", record_id),
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


def _member(native_id: str) -> dict:
    return {"namespace": "youtube", "kind": "transcript", "native_id": native_id}


def _spec(
    members: tuple[str, ...] = ("vid1", "vid2"),
    *,
    start: str = "2025-01-01T00:00:00Z",
    end: str = "2027-01-01T00:00:00Z",
    basis: str = "capture_time",
    comparison_set: dict | None = None,
) -> dict:
    spec = {
        "platform": "youtube",
        "cohort": {
            "cohort_id": "test_cohort",
            "definition": "declared captured test cohort",
            "member_refs": [_member(m) for m in members],
        },
        "coverage_window": {"start": start, "end": end, "window_basis": basis},
        "cohort_selection": "declared_member_refs_v0",
        "product_mention_policy": _POLICY,
    }
    if comparison_set is not None:
        spec["comparison_set"] = comparison_set
    return spec


_IN_WINDOW = "2026-01-01T00:00:00Z"


def test_observed_readout_mention_level_refs_and_shares(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first = _commit_packet(root, tmp_path, "alpha")
    second = _commit_packet(root, tmp_path, "beta")
    # One record carrying TWO matching mentions of the same (brand, line):
    # mention-level refs must yield count 2 from a single record (F1).
    _write_record(
        root,
        first,
        "m1.json",
        {
            "rubric_version": "rubric_v0",
            "mentions": [
                _mention("m-1", "Dior", "Sauvage", 100),
                _mention("m-2", "Dior", "Sauvage", 900),
                _mention("m-3", "Chanel", "Bleu", 500),
            ],
            **_lineage_fields(root, first, "vid1", captured_at=_IN_WINDOW),
        },
    )
    _write_record(
        root,
        second,
        "m2.json",
        {
            "rubric_version": "rubric_v0",
            "mentions": [_mention("m-4", "unknown", "mystery scent")],
            **_lineage_fields(root, second, "vid2", captured_at=_IN_WINDOW),
        },
    )

    view, source_refs = compute_sov_readout(root, _spec())

    assert view["metric_family"] == METRIC_FAMILY
    assert view["product_mention_policy"] == _POLICY
    assert view["family_schema_version"] == 2
    assert view["platform"] == "youtube"
    assert view["readout_posture"] == "observed"
    assert view["denominator"] == 4
    assert view["denominator_basis"] == "captured_source_backed_mentions_only"
    assert view["grouping_basis"] == "exact_string_v0"
    assert view["fragmentation_note"].strip()

    rows = {(r["brand"], r["line"]): r for r in view["rows"]}
    dior = rows[("Dior", "Sauvage")]
    assert dior["mention_count"] == 2 == len(dior["mention_refs"])
    for ref in dior["mention_refs"]:
        assert ref["raw_anchor"] == first
        assert ref["lane"] == MENTIONS_LANE
        assert ref["record_id"] == "m1.json"
        assert len(ref["sha256"]) == 64
        assert ref["mention_id"] and ref["source_pointer"]
        assert isinstance(ref["start_ms"], int) and isinstance(ref["end_ms"], int)
    assert dior["share"] == 2 / 4
    # The extractor's literal "unknown" brand is its own row, never merged or dropped.
    assert rows[("unknown", "mystery scent")]["mention_count"] == 1
    assert sum(r["mention_count"] for r in view["rows"]) == view["denominator"]

    policies = view["selection_policy_versions"]
    assert policies["silver_lineage_gate"] == "source_backed_complete"
    assert policies["brand_grouping"] == "exact_string_v0"
    assert policies["cohort_selection"] == "declared_member_refs_v0"
    assert policies["family_schema_version"] == 2
    assert policies["product_mention_policy"] == _POLICY

    cohort = view["cohort"]
    assert cohort["member_basis"] == "captured_set"
    assert cohort["member_count"] == 2 == len(cohort["member_refs"])
    assert view["coverage"]["source_objects_in_scope"] == 2
    assert view["coverage"]["source_objects_with_transcripts"] == 2
    assert view["coverage"]["packets_in_scope"] == 2

    # Schema pin: exactly the contract fields, nothing forbidden can hide here.
    assert set(view) == {
        "product_mention_policy",
        "metric_family",
        "family_schema_version",
        "platform",
        "cohort",
        "coverage_window",
        "selection_policy_versions",
        "grouping_basis",
        "fragmentation_note",
        "coverage",
        "readout_posture",
        "rows",
        "denominator",
        "denominator_basis",
    }
    assert f"{first}/{MENTIONS_LANE}/m1.json" in source_refs


def test_lineage_gate_excludes_and_counts(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first = _commit_packet(root, tmp_path, "alpha")
    _write_record(
        root,
        first,
        "m_ok.json",
        {
            "mentions": [_mention("m-1", "Dior", "Sauvage")],
            **_lineage_fields(root, first, "vid1", captured_at=_IN_WINDOW),
        },
    )
    # Gate-failing record: carries a cohort identity but no lineage fields.
    _write_record(
        root,
        first,
        "m_no_lineage.json",
        {
            "source_object": _member("vid1"),
            "mentions": [_mention("m-2", "Ghost", "Should Not Count")],
        },
    )

    view, _refs = compute_sov_readout(root, _spec(members=("vid1",)))

    assert view["readout_posture"] == "observed"
    assert view["denominator"] == 1
    assert ("Ghost", "Should Not Count") not in {(r["brand"], r["line"]) for r in view["rows"]}
    assert view["coverage"]["mention_records_in_scope"] == 1
    assert view["coverage"]["selection_residual_count_lake_wide"] == 1
    assert view["coverage"]["selection_residuals_by_status"] == {"invalid_silver_envelope": 1}


def test_cohort_scoping_and_residuals(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first = _commit_packet(root, tmp_path, "alpha")
    _write_record(
        root,
        first,
        "m_member.json",
        {
            "mentions": [_mention("m-1", "Dior", "Sauvage")],
            **_lineage_fields(root, first, "vid1", captured_at=_IN_WINDOW),
        },
    )
    # A committed record from a NON-member source object: out of scope entirely.
    _write_record(
        root,
        first,
        "m_other.json",
        {
            "mentions": [_mention("m-2", "Chanel", "Bleu")],
            **_lineage_fields(root, first, "vid_other", captured_at=_IN_WINDOW),
        },
    )

    view, _refs = compute_sov_readout(root, _spec(members=("vid1", "vid_absent")))

    assert view["denominator"] == 1
    assert {(r["brand"], r["line"]) for r in view["rows"]} == {("Dior", "Sauvage")}
    assert view["coverage"]["mention_records_in_scope"] == 1
    assert view["coverage"]["source_objects_in_scope"] == 2
    assert view["coverage"]["cohort_selection_residuals"] == {
        "members_without_committed_records": 1
    }


def test_capture_time_window_excludes_out_of_window(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first = _commit_packet(root, tmp_path, "alpha")
    _write_record(
        root,
        first,
        "m_in.json",
        {
            "mentions": [_mention("m-1", "Dior", "Sauvage")],
            **_lineage_fields(root, first, "vid1", captured_at=_IN_WINDOW),
        },
    )
    _write_record(
        root,
        first,
        "m_out.json",
        {
            "mentions": [_mention("m-2", "Chanel", "Bleu")],
            **_lineage_fields(root, first, "vid1", captured_at="2020-06-01T00:00:00Z"),
        },
    )

    view, _refs = compute_sov_readout(root, _spec(members=("vid1",)))

    assert view["denominator"] == 1
    assert {(r["brand"], r["line"]) for r in view["rows"]} == {("Dior", "Sauvage")}
    # Out-of-window under a carried basis is window exclusion, not missing basis.
    assert view["coverage"]["window_basis_missing"] == 0


def test_capture_time_falls_back_to_packet_manifest(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first = _commit_packet(root, tmp_path, "alpha")
    # No record-level captured_at: the packet manifest's known timing.capture_time
    # (stamped at commit time, i.e. "now") must carry the capture_time basis.
    _write_record(
        root,
        first,
        "m_fallback.json",
        {
            "mentions": [_mention("m-1", "Dior", "Sauvage")],
            **_lineage_fields(root, first, "vid1"),
        },
    )

    view, _refs = compute_sov_readout(
        root,
        _spec(members=("vid1",), start="2000-01-01T00:00:00Z", end="2100-01-01T00:00:00Z"),
    )

    assert view["readout_posture"] == "observed"
    assert view["denominator"] == 1
    assert view["coverage"]["window_basis_missing"] == 0


def test_publication_basis_missing_is_counted_and_can_empty_the_scope(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first = _commit_packet(root, tmp_path, "alpha")
    # No observed_at and the local-files packet has no known publication fact:
    # the record lacks the selected basis entirely (F2).
    _write_record(
        root,
        first,
        "m_no_basis.json",
        {
            "mentions": [_mention("m-1", "Dior", "Sauvage")],
            **_lineage_fields(root, first, "vid1", captured_at=_IN_WINDOW),
        },
    )

    spec = _spec(
        members=("vid1",),
        basis="source_publication_time",
        start="2000-01-01T00:00:00Z",
        end="2100-01-01T00:00:00Z",
    )
    view, _refs = compute_sov_readout(root, spec)

    assert view["readout_posture"] == "unavailable_with_reason"
    assert view["readout_reason"] == "window_basis_missing_for_all_exact_policy_records_in_scope"
    assert view["rows"] == []
    assert "denominator" not in view
    assert view["coverage"]["window_basis_missing"] == 1

    # A record that DOES carry observed_at is evaluated; the basis-lacking one
    # stays excluded from numerator AND denominator but visibly counted.
    _write_record(
        root,
        first,
        "m_observed.json",
        {
            "mentions": [_mention("m-2", "Chanel", "Bleu")],
            **_lineage_fields(root, first, "vid1", observed_at="2026-02-01T00:00:00Z"),
        },
    )
    view, _refs = compute_sov_readout(root, spec)
    assert view["readout_posture"] == "observed"
    assert view["denominator"] == 1
    assert {(r["brand"], r["line"]) for r in view["rows"]} == {("Chanel", "Bleu")}
    assert view["coverage"]["window_basis_missing"] == 1


def test_zero_rows_exist_only_under_declared_comparison_set(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first = _commit_packet(root, tmp_path, "alpha")
    _write_record(
        root,
        first,
        "m1.json",
        {
            "mentions": [_mention("m-1", "Dior", "Sauvage")],
            **_lineage_fields(root, first, "vid1", captured_at=_IN_WINDOW),
        },
    )

    # Without a comparison_set the absence of a row is NOT a zero.
    view, _refs = compute_sov_readout(root, _spec(members=("vid1",)))
    assert {(r["brand"], r["line"]) for r in view["rows"]} == {("Dior", "Sauvage")}

    comparison = {
        "brand_line_keys": [["Dior", "Sauvage"], ["Creed", "Aventus"]],
        "basis": "test competitor set",
        "comparison_set_ref": "docs/test/comparison_manifest_v0.json",
        "version": "comparison_v0",
    }
    view, _refs = compute_sov_readout(root, _spec(members=("vid1",), comparison_set=comparison))
    rows = {(r["brand"], r["line"]): r for r in view["rows"]}
    zero = rows[("Creed", "Aventus")]
    assert zero["mention_count"] == 0
    assert zero["mention_refs"] == []
    assert zero["share"] == 0.0
    assert view["comparison_set"]["comparison_set_ref"]
    assert view["selection_policy_versions"]["comparison_set"] == "comparison_v0"
    assert rows[("Dior", "Sauvage")]["mention_count"] == 1


def test_empty_scope_is_posture_never_a_zero_table(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    _commit_packet(root, tmp_path, "alpha")  # committed material, no mention records
    comparison = {
        "brand_line_keys": [["Dior", "Sauvage"]],
        "basis": "test competitor set",
        "comparison_set_ref": "docs/test/comparison_manifest_v0.json",
        "version": "comparison_v0",
    }
    view, _refs = compute_sov_readout(root, _spec(members=("vid1",), comparison_set=comparison))

    assert view["readout_posture"] == "unavailable_with_reason"
    assert view["readout_reason"] == "no_exact_policy_mention_records_in_scope"
    assert view["rows"] == []
    assert "denominator" not in view and "denominator_basis" not in view
    assert view["coverage"]["cohort_selection_residuals"] == {
        "members_without_committed_records": 1
    }


def test_zero_mention_and_malformed_and_unreadable_are_disclosed(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first = _commit_packet(root, tmp_path, "alpha")
    _write_record(
        root,
        first,
        "m_counts.json",
        {
            "mentions": [
                _mention("m-1", "Dior", "Sauvage"),
                {"brand": "Broken", "line": "No Ref Fields"},  # malformed: no ref fields
                {**_mention("m-2", "", "Blank Brand")},
                {**_mention("m-3", "Broken", "")},
                {**_mention("m-4", "Broken", "Bad Span", 200), "end_ms": 100},
            ],
            **_lineage_fields(root, first, "vid1", captured_at=_IN_WINDOW),
        },
    )
    _write_record(
        root,
        first,
        "m_zero.json",
        {
            "mentions": [],
            **_lineage_fields(root, first, "vid1", captured_at=_IN_WINDOW),
        },
    )
    root.append_record(
        subtree="derived",
        raw_anchor=first,
        lane=MENTIONS_LANE,
        record_id="m_corrupt.json",
        data=b"{not json",
    )

    view, _refs = compute_sov_readout(root, _spec(members=("vid1",)))

    assert view["denominator"] == 1
    coverage = view["coverage"]
    assert coverage["source_backed_records_with_zero_mentions"] == 1
    assert coverage["malformed_mention_entries"] == 4
    assert coverage["selection_residuals_by_status"] == {"unreadable": 1}
    assert {(row["brand"], row["line"]) for row in view["rows"]} == {("Dior", "Sauvage")}


def test_spec_validation_fails_closed(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")

    cross_platform = _spec()
    cross_platform["cohort"]["member_refs"][0]["namespace"] = "instagram"
    with pytest.raises(SovSpecError):
        compute_sov_readout(root, cross_platform)

    duplicated = _spec(members=("vid1", "vid1"))
    with pytest.raises(SovSpecError):
        compute_sov_readout(root, duplicated)

    bad_basis = _spec(basis="upload_time")
    with pytest.raises(SovSpecError):
        compute_sov_readout(root, bad_basis)

    bad_comparison = _spec(
        comparison_set={"brand_line_keys": [["Dior", "Sauvage"]], "version": "v0"}
    )
    with pytest.raises(SovSpecError):
        compute_sov_readout(root, bad_comparison)

    inverted_window = _spec(start="2027-01-01T00:00:00Z", end="2025-01-01T00:00:00Z")
    with pytest.raises(SovSpecError):
        compute_sov_readout(root, inverted_window)


def test_materialize_and_prove_rebuildability(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first = _commit_packet(root, tmp_path, "alpha")
    _write_record(
        root,
        first,
        "m1.json",
        {
            "mentions": [_mention("m-1", "Dior", "Sauvage")],
            **_lineage_fields(root, first, "vid1", captured_at=_IN_WINDOW),
        },
    )
    spec = _spec(members=("vid1",))

    report = materialize_sov_readout(root, spec, stamp=_STAMP)
    assert report["status"] == "materialized"
    readout_id = report["readout_id"]
    assert readout_id == sov_readout_id(
        json.loads(
            (
                root.path
                / "indexes"
                / "derived_retrieval"
                / "metric_family"
                / METRIC_FAMILY
                / readout_id
                / "manifest.json"
            ).read_text("utf-8")
        )["spec"]
    )
    readout_dir = (
        root.path / "indexes" / "derived_retrieval" / "metric_family" / METRIC_FAMILY / readout_id
    )
    manifest = json.loads((readout_dir / "manifest.json").read_text("utf-8"))
    assert manifest["generation_id"] == _STAMP["generation_id"]
    assert manifest["source_record_ids"]
    assert manifest["source_high_watermark"]
    assert manifest["view_sha256"]
    assert manifest["stale_if"]

    proof = prove_sov_rebuildability(root)
    assert proof["status"] == "proven"
    assert proof["results"] == {readout_id: "rebuildable"}

    view_path = readout_dir / "view.json"
    original = view_path.read_bytes()
    view_path.write_bytes(original + b" ")  # smuggled state
    proof = prove_sov_rebuildability(root)
    assert proof["status"] == "failed"
    assert proof["results"][readout_id] == "failed_drift_or_non_regenerable"
    view_path.write_bytes(original)
    assert prove_sov_rebuildability(root)["status"] == "proven"

    # A post-generation committed source change drifts the stored readout.
    _write_record(
        root,
        first,
        "m2.json",
        {
            "mentions": [_mention("m-2", "Chanel", "Bleu")],
            **_lineage_fields(root, first, "vid1", captured_at=_IN_WINDOW),
        },
    )
    proof = prove_sov_rebuildability(root)
    assert proof["status"] == "failed"
    assert proof["failures"] == [readout_id]


def test_prove_on_empty_store_is_proven_nothing(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    proof = prove_sov_rebuildability(root)
    assert proof["status"] == "proven"
    assert proof["results"] == {}


def test_runner_cli_fails_closed_on_in_repo_root(tmp_path: Path, capsys) -> None:
    from runners.run_data_lake_sov_readout import main

    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(_spec()), encoding="utf-8")
    assert main(["--root", str(tmp_path / "lake"), "--spec", str(spec_path)]) == 2
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "error"


def test_runner_cli_compute_materialize_prove(tmp_path: Path, capsys, monkeypatch) -> None:
    from runners.run_data_lake_sov_readout import main

    root = DataLakeRoot.for_test(tmp_path / "lake")
    first = _commit_packet(root, tmp_path, "alpha")
    _write_record(
        root,
        first,
        "m1.json",
        {
            "mentions": [_mention("m-1", "Dior", "Sauvage")],
            **_lineage_fields(root, first, "vid1", captured_at=_IN_WINDOW),
        },
    )
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(_spec(members=("vid1",))), encoding="utf-8")
    monkeypatch.setattr(DataLakeRoot, "resolve", staticmethod(lambda **_kwargs: root))

    # On demand: computed to stdout, nothing written into the lake.
    assert main(["--root", str(root.path), "--spec", str(spec_path)]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "computed"
    assert report["readout"]["readout_posture"] == "observed"
    family_dir = root.path / "indexes" / "derived_retrieval" / "metric_family" / METRIC_FAMILY
    assert not family_dir.exists() or not any(family_dir.iterdir())

    assert main(["--root", str(root.path), "--spec", str(spec_path), "--materialize"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "materialized"

    assert main(["--root", str(root.path), "--prove-rebuildability"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "proven"

    view_path = family_dir / report_readout_id(report) / "view.json"
    view_path.write_bytes(view_path.read_bytes() + b" ")
    assert main(["--root", str(root.path), "--prove-rebuildability"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "failed"


def report_readout_id(prove_report: dict) -> str:
    (readout_id,) = prove_report["results"].keys()
    return readout_id
