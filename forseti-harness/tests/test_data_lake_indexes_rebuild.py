"""Silver Vault derived-retrieval view builder + rebuild runner tests.

Covers the seam contract's Rebuild Command Binding: manifest-backed rebuildable
views, the by_mention read-side lineage gate, the undone view's documented
weaker semantics, and a prove-rebuildability that fails on tampered bytes
(never self-comparing).
"""
from __future__ import annotations

import json
import hashlib
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
    MENTIONS_LANE,
    audit_derived_retrieval_source_integrity,
    build_by_creator_view,
    build_by_mention_view,
    prove_incremental_rebuild_equality,
    prove_derived_retrieval_rebuildability,
    rebuild_creator_vault,
    rebuild_derived_retrieval,
)
from data_lake.root import DataLakeRoot, raw_shard
from data_lake.silver_lineage import (
    SilverAnchor,
    SilverLineage,
    SilverRawRef,
    SilverSourceObject,
)
from data_lake.silver_record import (
    CURRENT_SOURCE_BACKED_AUTHORITY,
    SilverSourceAuthority,
    append_raw_packet_tombstone,
    silver_content_hash,
)
from data_lake.sibling_selection import SiblingSelectionError
from source_capture.models import known_fact
from source_capture.writer import write_local_source_capture_packet

_STAMP = {"generation_id": "0" * 32, "generated_at": "2026-07-02T00:00:00+00:00"}
_NS = "projection_ig"
_POLICY = {"policy_version": "v0", "policy_fingerprint_sha256": "a" * 64}
_POLICY_ARGS = [
    "--product-mention-policy-version", "v0",
    "--product-mention-policy-fingerprint-sha256", "a" * 64,
]


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


def test_rebuild_builds_views_and_manifests(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    first, second = _seeded_root(root, tmp_path)

    legacy_root = root.path / "indexes" / "derived_retrieval" / "object_level"
    legacy_root.mkdir(parents=True)
    (legacy_root / "by_mention.json").write_text("legacy", encoding="utf-8")
    silver_core = root.path / "indexes" / "derived_retrieval" / "silver_vault" / "core"

    report = rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
    assert report["status"] == "rebuilt"
    assert report["views"] == ["by_creator", "by_mention", "undone"]
    assert report["deferred_views"] == []

    assert not legacy_root.exists()
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
        "creator_vault_accounts": "rebuildable",
    }

    view_path = (
        root.path / "indexes" / "derived_retrieval" / "silver_vault" / "core"
        / "query_tables" / "undone.json"
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
        "creator_vault_accounts": "absent_nothing_to_prove",
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
    target_root = root._within(
        "indexes", "derived_retrieval", "silver_vault", "core"
    )
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
    target_root = root._within(
        "indexes", "derived_retrieval", "silver_vault", "core"
    )
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
    metric_name: str = "follower_count",
    metric_value: int | None = 1000,
    posture_kind: str = "observed",
    reason_code: str | None = None,
    observed_at: str = "2026-07-15T00:00:00Z",
    producer_row_kind: str = "test_creator_metric",
) -> None:
    """One strict-current MetricObservation with an account-bearing subject."""
    if posture_kind != "observed" and reason_code is None:
        reason_code = "source_unavailable"
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
        "producer_row_kind": producer_row_kind,
        "source_surface": "test_surface",
        "observed_at": observed_at,
        "captured_at": observed_at,
        **{
            key: value
            for key, value in _complete_lineage_fields(root, raw_anchor).items()
            if key in ("raw_refs", "derived_refs")
        },
        "payload": {
            "observation": {
                "subject": {"ref_type": "entity_key", "ref": subject_ref},
                "metric_name": metric_name,
                "metric_value": metric_value,
                "metric_posture": {
                    "kind": posture_kind,
                    "reason_code": reason_code,
                    "reason_detail": None if posture_kind == "observed" else "fixture source unavailable",
                },
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


def _tiktok_profile_subject(account_id: str, handle: str = "fixture_creator") -> dict:
    return {
        "namespace": "tiktok",
        "kind": "platform_public_account",
        "native_id": handle,
        "platform_account_id": account_id,
    }


def _creator_vault_account_paths(root: DataLakeRoot, account_id: str) -> tuple[Path, Path]:
    creator_root = root.path / "indexes" / "derived_retrieval" / "silver_vault" / "creator_vault"
    return (
        creator_root / "accounts" / "tiktok" / account_id / "envelope.json",
        creator_root / "manifests" / "accounts" / "tiktok" / f"{account_id}.json",
    )


def test_creator_vault_retains_last_observed_after_unavailable_and_combines_registry(
    tmp_path: Path,
) -> None:
    from runners.run_derived_retrieval_lookup import lookup_creator

    root = DataLakeRoot.for_test(tmp_path / "lake")
    account_id = "acct_tt_fixture_001"
    subject = _tiktok_profile_subject(account_id)
    first = _commit_packet(root, tmp_path, "profile-first")
    second = _commit_packet(root, tmp_path, "profile-second")
    _write_creator_metric_record(
        root, first, "followers-first.json",
        subject_ref=subject,
        metric_value=1000,
        observed_at="2026-07-15T00:00:00Z",
        producer_row_kind="tiktok_creator_profile_metric",
    )
    _write_creator_metric_record(
        root, first, "likes-first.json",
        subject_ref=subject,
        metric_name="profile_total_like_count",
        metric_value=5000,
        observed_at="2026-07-15T00:00:00Z",
        producer_row_kind="tiktok_creator_profile_metric",
    )
    _write_creator_metric_record(
        root, second, "followers-gap.json",
        subject_ref=subject,
        metric_value=None,
        posture_kind="unavailable_with_reason",
        observed_at="2026-07-16T00:00:00Z",
        producer_row_kind="tiktok_creator_profile_metric",
    )
    _write_creator_metric_record(
        root, second, "likes-second.json",
        subject_ref=subject,
        metric_name="profile_total_like_count",
        metric_value=6000,
        observed_at="2026-07-16T00:00:00Z",
        producer_row_kind="tiktok_creator_profile_metric",
    )

    report = rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
    assert report["creator_vault_account_envelope_count"] == 1
    envelope_path, manifest_path = _creator_vault_account_paths(root, account_id)
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    follower = envelope["latest_metric_snapshot"]["follower_count"]
    assert follower["display_state"] == "last_observed_retained_after_unavailable_attempt"
    assert follower["last_observed"]["metric_value_or_none"] == 1000
    assert follower["latest_attempt"]["metric_posture"] == "unavailable_with_reason"
    likes = envelope["latest_metric_snapshot"]["profile_total_like_count"]
    assert likes["display_state"] == "current_observed"
    assert likes["last_observed"]["metric_value_or_none"] == 6000
    assert manifest["envelope_sha256"] == hashlib.sha256(envelope_path.read_bytes()).hexdigest()
    assert manifest["generated_at"] == _STAMP["generated_at"]
    assert manifest["source_ref_set_fingerprint_sha256"]

    creator_root = envelope_path.parents[3]
    before = {path.relative_to(creator_root): path.read_bytes() for path in creator_root.rglob("*.json")}
    rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
    after = {path.relative_to(creator_root): path.read_bytes() for path in creator_root.rglob("*.json")}
    assert after == before

    stable_profile = {
        "profile_subject_id": account_id,
        "platform_accounts": [{
            "platform": "tiktok",
            "platform_account_id": account_id,
            "public_handle": "fixture_creator",
        }],
        "identity_state": "single_platform_observed",
    }
    result = lookup_creator(
        root,
        "tiktok:fixture_creator",
        profile_view={"creator_profile_current_view": {"profiles": [stable_profile]}},
    )
    match = result["matches"][0]
    assert match["registry_profile_or_none"] == stable_profile
    assert match["creator_vault_account_or_none"] == envelope
    assert match["current_profile_metrics_status"] == "generated"
    assert match["creator_vault_provenance"]["generated_at"] == _STAMP["generated_at"]
    assert prove_derived_retrieval_rebuildability(root)["status"] == "proven"

    third = _commit_packet(root, tmp_path, "profile-third")
    _write_creator_metric_record(
        root, third, "followers-third.json",
        subject_ref=subject,
        metric_value=2000,
        observed_at="2026-07-17T00:00:00Z",
        producer_row_kind="tiktok_creator_profile_metric",
    )
    stale = prove_derived_retrieval_rebuildability(root)
    assert stale["status"] == "failed"
    assert stale["results"]["creator_vault_accounts"] == "failed_drift_or_non_regenerable"


def test_creator_vault_publication_failure_restores_previous_generated_package(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import data_lake.derived_retrieval_views as views

    root = DataLakeRoot.for_test(tmp_path / "lake")
    account_id = "acct_tt_publish_failure"
    subject = _tiktok_profile_subject(account_id, "publish_failure_creator")
    first = _commit_packet(root, tmp_path, "publish-first")
    _write_creator_metric_record(
        root, first, "followers-first.json",
        subject_ref=subject,
        metric_value=1000,
        observed_at="2026-07-15T00:00:00Z",
        producer_row_kind="tiktok_creator_profile_metric",
    )
    views.rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
    package_root = root.path / "indexes" / "derived_retrieval" / "silver_vault"

    def package_bytes() -> dict[Path, bytes]:
        return {
            path.relative_to(package_root): path.read_bytes()
            for subtree in (package_root / "core", package_root / "creator_vault")
            for path in subtree.rglob("*.json")
            if "cache" not in path.parts
        }

    previous = package_bytes()
    second = _commit_packet(root, tmp_path, "publish-second")
    _write_creator_metric_record(
        root, second, "followers-second.json",
        subject_ref=subject,
        metric_value=2000,
        observed_at="2026-07-16T00:00:00Z",
        producer_row_kind="tiktok_creator_profile_metric",
    )
    real_atomic_replace = views._atomic_replace
    calls = 0

    def fail_once(target: Path, data: bytes) -> None:
        nonlocal calls
        calls += 1
        if calls == 3:
            raise OSError("simulated generated-package publication failure")
        real_atomic_replace(target, data)

    monkeypatch.setattr(views, "_atomic_replace", fail_once)
    with pytest.raises(OSError, match="simulated generated-package publication failure"):
        views.rebuild_derived_retrieval(
            root,
            product_mention_policy=_POLICY,
            stamp={"generation_id": "1" * 32, "generated_at": "2026-07-16T00:00:00+00:00"},
        )
    assert calls > 3  # publication began, then rollback used the same atomic primitive
    assert package_bytes() == previous


def test_creator_vault_surfaces_missing_history_and_latest_conflict(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    conflict_id = "acct_tt_conflict"
    conflict_subject = _tiktok_profile_subject(conflict_id, "conflicted_creator")
    old = _commit_packet(root, tmp_path, "conflict-old")
    left = _commit_packet(root, tmp_path, "conflict-left")
    right = _commit_packet(root, tmp_path, "conflict-right")
    _write_creator_metric_record(
        root, old, "old.json", subject_ref=conflict_subject, metric_value=1000,
        observed_at="2026-07-15T00:00:00Z", producer_row_kind="tiktok_creator_profile_metric",
    )
    for packet_id, record_id, value in ((left, "left.json", 2000), (right, "right.json", 3000)):
        _write_creator_metric_record(
            root, packet_id, record_id, subject_ref=conflict_subject, metric_value=value,
            observed_at="2026-07-16T00:00:00Z", producer_row_kind="tiktok_creator_profile_metric",
        )
    missing_id = "acct_tt_missing"
    missing_packet = _commit_packet(root, tmp_path, "missing")
    _write_creator_metric_record(
        root, missing_packet, "missing.json",
        subject_ref=_tiktok_profile_subject(missing_id, "missing_creator"),
        metric_value=None,
        posture_kind="unavailable_with_reason",
        observed_at="2026-07-16T00:00:00Z",
        producer_row_kind="tiktok_creator_profile_metric",
    )

    rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
    conflict_path, _ = _creator_vault_account_paths(root, conflict_id)
    conflict = json.loads(conflict_path.read_text(encoding="utf-8"))
    metric = conflict["latest_metric_snapshot"]["follower_count"]
    assert metric["display_state"] == "conflicted_latest_attempt"
    assert metric["latest_attempt"] is None
    assert metric["last_observed"]["metric_value_or_none"] == 1000
    assert conflict["metric_postures"]["follower_count"] == "conflicted"
    assert len(conflict["source_conflicts"]) == 1

    missing_path, _ = _creator_vault_account_paths(root, missing_id)
    missing = json.loads(missing_path.read_text(encoding="utf-8"))
    metric = missing["latest_metric_snapshot"]["follower_count"]
    assert metric["display_state"] == "unavailable_no_observed_value"
    assert metric["last_observed"] is None
    assert metric["latest_attempt"]["metric_posture"] == "unavailable_with_reason"


def test_creator_vault_excludes_tombstoned_latest_packet(tmp_path: Path) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    account_id = "acct_tt_tombstone"
    subject = _tiktok_profile_subject(account_id, "tombstone_creator")
    retained = _commit_packet(root, tmp_path, "retained")
    retired = _commit_packet(root, tmp_path, "retired")
    _write_creator_metric_record(
        root, retained, "retained.json", subject_ref=subject, metric_value=1000,
        observed_at="2026-07-15T00:00:00Z", producer_row_kind="tiktok_creator_profile_metric",
    )
    _write_creator_metric_record(
        root, retired, "retired.json", subject_ref=subject, metric_value=2000,
        observed_at="2026-07-16T00:00:00Z", producer_row_kind="tiktok_creator_profile_metric",
    )
    append_raw_packet_tombstone(
        root,
        retained_packet_id=retained,
        tombstoned_packet_id=retired,
        captured_at="2026-07-17T00:00:00Z",
        reason="Creator Vault tombstone fixture",
    )

    rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
    envelope_path, manifest_path = _creator_vault_account_paths(root, account_id)
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    assert envelope["latest_metric_snapshot"]["follower_count"]["last_observed"]["metric_value_or_none"] == 1000
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert all(retired not in source_ref for source_ref in manifest["source_record_ids"])


def test_creator_lookup_rejects_tampered_creator_vault_envelope(tmp_path: Path) -> None:
    from runners.run_derived_retrieval_lookup import lookup_creator

    root = DataLakeRoot.for_test(tmp_path / "lake")
    account_id = "acct_tt_tamper"
    packet_id = _commit_packet(root, tmp_path, "tamper")
    _write_creator_metric_record(
        root, packet_id, "metric.json",
        subject_ref=_tiktok_profile_subject(account_id, "tamper_creator"),
        producer_row_kind="tiktok_creator_profile_metric",
    )
    rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
    envelope_path, _ = _creator_vault_account_paths(root, account_id)
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    envelope["coverage_summary"]["metric_count"] = 99
    envelope_path.write_bytes(canonical_record_bytes(envelope))

    stable_profile = {
        "profile_subject_id": account_id,
        "platform_accounts": [{
            "platform": "tiktok",
            "platform_account_id": account_id,
            "public_handle": "tamper_creator",
        }],
    }
    with pytest.raises(ValueError, match="envelope_sha256"):
        lookup_creator(
            root,
            "tiktok:tamper_creator",
            profile_view={"creator_profile_current_view": {"profiles": [stable_profile]}},
        )

def test_creator_vault_scoped_rebuild_is_byte_equal_and_leaves_core_unchanged(
    tmp_path: Path,
) -> None:
    from runners.run_derived_retrieval_lookup import lookup_creator

    root = DataLakeRoot.for_test(tmp_path / "lake")
    account_id = "acct_tt_scoped"
    packet_id = _commit_packet(root, tmp_path, "scoped")
    _write_creator_metric_record(
        root,
        packet_id,
        "metric.json",
        subject_ref=_tiktok_profile_subject(account_id, "scoped_creator"),
        producer_row_kind="tiktok_creator_profile_metric",
    )
    rebuild_derived_retrieval(
        root,
        product_mention_policy=_POLICY,
        stamp=_STAMP,
    )
    silver_root = (
        root.path / "indexes" / "derived_retrieval" / "silver_vault"
    )
    core_before = {
        path.relative_to(silver_root): path.read_bytes()
        for path in (silver_root / "core").rglob("*.json")
    }
    creator_before = {
        path.relative_to(silver_root): path.read_bytes()
        for path in (silver_root / "creator_vault").rglob("*.json")
    }

    report = rebuild_creator_vault(root, stamp=_STAMP)
    assert report["silver_lanes_scanned"] == ["creator_metric_silver"]
    assert report["producer_row_kind"] == "tiktok_creator_profile_metric"
    core_after = {
        path.relative_to(silver_root): path.read_bytes()
        for path in (silver_root / "core").rglob("*.json")
    }
    creator_after = {
        path.relative_to(silver_root): path.read_bytes()
        for path in (silver_root / "creator_vault").rglob("*.json")
    }
    assert core_after == core_before
    assert creator_after == creator_before

    stable_profile = {
        "profile_subject_id": "profile_scoped_creator",
        "platform_accounts": [{
            "platform": "tiktok",
            "platform_account_id": account_id,
            "public_handle": "scoped_creator",
        }],
    }
    lookup = lookup_creator(
        root,
        "tiktok:scoped_creator",
        profile_view={"creator_profile_current_view": {"profiles": [stable_profile]}},
    )
    assert lookup["status"] == "found"
    assert lookup["matches"][0]["current_profile_metrics_status"] == "generated"
    assert lookup["matches"][0]["registry_profile_or_none"] == stable_profile


def test_creator_vault_names_unfileable_captured_accounts_for_lookup(
    tmp_path: Path,
) -> None:
    from runners.run_derived_retrieval_lookup import lookup_creator

    root = DataLakeRoot.for_test(tmp_path / "lake")
    fixtures = [
        (
            "missing-alias",
            {
                "namespace": "tiktok",
                "kind": "platform_public_account",
                "native_id": "missing_alias_creator",
            },
            "acct_tt_missing_alias",
            "missing_platform_account_id",
        ),
        (
            "conflicting-alias",
            {
                "namespace": "tiktok",
                "kind": "platform_public_account",
                "native_id": "conflicting_alias_creator",
                "platform_account_id": "acct_tt_conflict_a",
                "orca_platform_account_id": "acct_tt_conflict_b",
            },
            "acct_tt_conflict_a",
            "conflicting_platform_account_id_aliases",
        ),
        (
            "unsafe-alias",
            {
                "namespace": "tiktok",
                "kind": "platform_public_account",
                "native_id": "unsafe_alias_creator",
                "platform_account_id": "unsafe/account",
            },
            "unsafe/account",
            "unsafe_platform_account_id_path_key",
        ),
    ]
    for label, subject, _registry_id, _status in fixtures:
        packet_id = _commit_packet(root, tmp_path, label)
        _write_creator_metric_record(
            root,
            packet_id,
            "metric.json",
            subject_ref=subject,
            producer_row_kind="tiktok_creator_profile_metric",
        )

    rebuild_creator_vault(root, stamp=_STAMP)
    residual_path = (
        root.path
        / "indexes"
        / "derived_retrieval"
        / "silver_vault"
        / "creator_vault"
        / "unfiled_accounts.json"
    )
    residual_view = json.loads(residual_path.read_text(encoding="utf-8"))
    assert {row["status"] for row in residual_view["residuals"]} == {
        "missing_platform_account_id",
        "conflicting_platform_account_id_aliases",
        "unsafe_platform_account_id_path_key",
    }

    for _label, subject, registry_id, residual_status in fixtures:
        handle = subject["native_id"]
        stable_profile = {
            "profile_subject_id": f"profile_{handle}",
            "platform_accounts": [{
                "platform": "tiktok",
                "platform_account_id": registry_id,
                "public_handle": handle,
            }],
        }
        result = lookup_creator(
            root,
            f"tiktok:{handle}",
            profile_view={
                "creator_profile_current_view": {"profiles": [stable_profile]}
            },
        )
        match = result["matches"][0]
        assert match["current_profile_metrics_status"] == "captured_but_unfileable"
        assert [row["status"] for row in match["creator_vault_residuals"]] == [
            residual_status
        ]


def test_creator_vault_selection_uses_full_ref_key_across_packets(
    tmp_path: Path,
) -> None:
    root = DataLakeRoot.for_test(tmp_path / "lake")
    account_id = "acct_tt_ref_collision"
    subject = _tiktok_profile_subject(account_id, "ref_collision_creator")
    older = _commit_packet(root, tmp_path, "ref-collision-older")
    latest = _commit_packet(root, tmp_path, "ref-collision-latest")
    _write_creator_metric_record(
        root,
        older,
        "metric.json",
        subject_ref=subject,
        metric_value=1000,
        observed_at="2026-07-15T00:00:00Z",
        producer_row_kind="tiktok_creator_profile_metric",
    )
    _write_creator_metric_record(
        root,
        latest,
        "metric.json",
        subject_ref=subject,
        metric_value=2000,
        observed_at="2026-07-16T00:00:00Z",
        producer_row_kind="tiktok_creator_profile_metric",
    )

    rebuild_creator_vault(root, stamp=_STAMP)
    envelope_path, _ = _creator_vault_account_paths(root, account_id)
    envelope = json.loads(envelope_path.read_text(encoding="utf-8"))
    assert envelope["latest_metric_snapshot"]["follower_count"]["last_observed"][
        "metric_value_or_none"
    ] == 2000
    assert envelope["derived_refs"] == [{
        "content_hash": envelope["derived_refs"][0]["content_hash"],
        "lane": "creator_metric_silver",
        "packet_id": latest,
        "record_id": "metric.json",
        "source_record_ref": f"{latest}/creator_metric_silver/metric.json",
    }]


def test_creator_lookup_reports_registry_conflict_without_loading_generic_map(
    tmp_path: Path,
) -> None:
    from runners.run_derived_retrieval_lookup import lookup_creator

    root = DataLakeRoot.for_test(tmp_path / "lake")
    profiles = [
        {
            "profile_subject_id": f"profile_{suffix}",
            "platform_accounts": [{
                "platform": "tiktok",
                "platform_account_id": f"acct_tt_{suffix}",
                "public_handle": "same_handle",
            }],
        }
        for suffix in ("left", "right")
    ]
    result = lookup_creator(
        root,
        "tiktok:same_handle",
        profile_view={"creator_profile_current_view": {"profiles": profiles}},
    )
    assert result["status"] == "conflicted"
    assert len(result["registry_candidates"]) == 2

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
    from runners import run_derived_retrieval_lookup as lookup_runner

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
    monkeypatch.setattr(
        DataLakeRoot,
        "resolve_readonly",
        staticmethod(lambda **_kwargs: root),
    )
    stable_profile = {
        "profile_subject_id": "profile_fixture_creator",
        "platform_accounts": [{
            "platform": "instagram",
            "platform_account_id": "acct_ig_fixture_001",
            "public_handle": "fixture_creator",
        }],
    }
    monkeypatch.setattr(
        lookup_runner,
        "load_creator_profile_current_view",
        lambda _path: {"creator_profile_current_view": {"profiles": [stable_profile]}},
    )

    assert lookup_runner.main(["--creator", "fixture_creator"]) == 0
    found = json.loads(capsys.readouterr().out)
    assert found["status"] == "found"
    assert found["matches"][0]["namespace"] == "instagram"
    assert found["matches"][0]["identity_kind"] == "stable_registry_platform_account"
    assert found["matches"][0]["registry_profile_or_none"] == stable_profile
    assert found["matches"][0]["current_profile_metrics_status"] == "not_captured_or_not_processed"

    assert lookup_runner.main(["--creator", "acct_ig_fixture_001"]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "found"

    assert lookup_runner.main(["--mention", "cloud"]) == 0
    mention = json.loads(capsys.readouterr().out)
    assert mention["matches"][0]["source_class"] == "native_product_pages"
    assert mention["matches"][0]["brand"] == "Ariana Grande"

    assert lookup_runner.main(["--mention", "grand"]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "not_found"

    assert lookup_runner.main(["--creator", "nobody_here"]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "unknown_to_registry"

def test_lookup_runner_fails_closed_on_absent_or_tampered_view_pair(
    tmp_path: Path, capsys, monkeypatch
) -> None:
    from runners import run_derived_retrieval_lookup as lookup_runner

    root = DataLakeRoot.for_test(tmp_path / "lake")
    monkeypatch.setattr(
        DataLakeRoot,
        "resolve_readonly",
        staticmethod(lambda **_kwargs: root),
    )
    monkeypatch.setattr(
        lookup_runner,
        "load_creator_profile_current_view",
        lambda _path: {"creator_profile_current_view": {"profiles": []}},
    )

    assert lookup_runner.main(["--creator", "fixture_creator"]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "unknown_to_registry"

    pid = _commit_packet(root, tmp_path, "tampered-view")
    _write_fragrantica_projection(root, pid)
    rebuild_derived_retrieval(root, product_mention_policy=_POLICY, stamp=_STAMP)
    view_path = (
        root.path
        / "indexes"
        / "derived_retrieval"
        / "silver_vault"
        / "core"
        / "query_tables"
        / "by_mention.json"
    )
    tampered = json.loads(view_path.read_text(encoding="utf-8"))
    tampered["native_product_pages"]["Ariana Grande"]["Cloud"][0][
        "canonical_url"
    ] = "https://example.test/tampered"
    view_path.write_bytes(canonical_record_bytes(tampered))

    assert lookup_runner.main(["--mention", "cloud"]) == 2
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
        (
            root.path
            / "indexes"
            / "derived_retrieval"
            / "silver_vault"
            / "core"
            / "manifests"
            / "by_mention.json"
        ).read_text(encoding="utf-8")
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
        ["--root", str(root.path), "--target", "creator_vault"]
    ) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["creator_vault"]["status"] == "rebuilt"
    assert report["creator_vault"]["silver_lanes_scanned"] == [
        "creator_metric_silver"
    ]
    assert main(
        [
            "--root",
            str(root.path),
            "--target",
            "creator_vault",
            "--prove-rebuildability",
        ]
    ) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["creator_vault"]["status"] == "proven"

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
    assert report["derived_retrieval"]["classification_cache"]["hits"] > 0

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

    view_path = (
        root.path / "indexes" / "derived_retrieval" / "silver_vault" / "core"
        / "query_tables" / "by_mention.json"
    )
    view_path.write_bytes(view_path.read_bytes() + b" ")
    assert main(["--root", str(root.path), "--target", "derived_retrieval", "--prove-rebuildability"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "failed"
    assert report["derived_retrieval"]["failures"] == ["by_mention"]
