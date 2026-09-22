"""Complete-row reuse of frozen verification; never a new semantic judgment."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from judgment import semantic_evidence_integration as semantic
from provider_attempts import unique_json_object


VERSION = "semantic_verified_row_selection_v1"
MANIFESTS = ("raw_response_manifest", "row_verification_manifest", "row_repair_manifest")


def load_original(path, expected):
    """Hash the very bytes decoded, with no mutable-path or cached-proof fallback."""
    try:
        raw = Path(path).read_bytes()
    except OSError as exc:
        raise semantic.SemanticIntegrationError(f"verified selection original dependency unavailable: {path}") from exc
    if hashlib.sha256(raw).hexdigest() != expected:
        raise semantic.SemanticIntegrationError(f"verified selection original dependency changed: {path}")
    return json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_json_object)


def validate_verified_inputs(source, bundle, verified):
    """Validate exact source ownership and native complete/selected verification."""
    if "verified_row_selection" in verified:
        validate_verified_selection(bundle, verified, source=source)
        return
    semantic._validate_verification_input_compilation(bundle, verified)
    semantic._verify_row_verification_manifest(bundle, verified)
    if not verified.get("row_verification_manifest"):
        raise semantic.SemanticIntegrationError("verified selection requires row verification")
    # Rebuild source-owned content without repacking the entire original corpus.
    # Existing projection validation above owns its frozen work-unit partition.
    rebuilt = semantic.build_bundle(source, max_prompt_bytes=bundle["max_prompt_bytes"],
        max_evidence_per_work_unit=bundle["semantic_work_unit_projection"]["max_evidence_per_work_unit"],
        target_bundle_version=bundle["schema_version"], _pack_batches=False)
    packing = {"bundle_sha256", "batches", "semantic_work_unit_projection"}
    if ({k: v for k, v in rebuilt.items() if k not in packing}
            != {k: v for k, v in bundle.items() if k not in packing}
            or any(rebuilt["semantic_work_unit_projection"].get(k) != bundle["semantic_work_unit_projection"].get(k)
                   for k in ("context_registry", "semantic_execution_identity"))):
        raise semantic.SemanticIntegrationError("verified selection original source does not match original bundle")


def _derive(originals, dependencies, evidence_ids, *, max_prompt_bytes, max_evidence_per_work_unit):
    source, bundle, verified = (originals[k] for k in ("source", "bundle", "verified"))
    if "verified_row_selection" in verified:
        raise semantic.SemanticIntegrationError("verified selection requires original verification, not a nested selection")
    validate_verified_inputs(source, bundle, verified)
    if (not isinstance(evidence_ids, list) or not evidence_ids
            or any(not isinstance(i, str) or not i for i in evidence_ids)
            or len(evidence_ids) != len(set(evidence_ids))):
        raise semantic.SemanticIntegrationError("verified selection requires distinct nonempty complete-row evidence IDs")
    wanted = set(evidence_ids)
    if wanted - {r["evidence_id"] for r in bundle["evidence_units"]}:
        raise semantic.SemanticIntegrationError("verified selection contains foreign or partial-row IDs")
    rows = [r for r in source["captured_items"] if r["evidence_id"] in wanted]
    selected_ids = [r["evidence_id"] for r in rows]
    if len(selected_ids) != len(wanted):
        raise semantic.SemanticIntegrationError("verified selection source IDs are not unique and complete")
    counts = Counter(r["container_id"] for r in rows)
    selected_source = {k: deepcopy(v) for k, v in source.items()
                       if k not in {"source_sha256", "captured_items", "containers"}}
    selected_source["captured_items"] = deepcopy(rows)
    selected_source["containers"] = [dict(deepcopy(r), captured_leaf_count=counts[r["container_id"]])
        for r in source["containers"] if r["container_id"] in counts]
    selected_source["corpus_profile"] = "bounded_regression_slice"
    selected_source["corpus_scope"] = source["corpus_scope"] + " | complete-row selection of previously verified evidence"
    selected_source["source_sha256"] = semantic._sha256(selected_source)
    selected_bundle = semantic.build_bundle(selected_source, max_prompt_bytes=max_prompt_bytes,
        max_evidence_per_work_unit=max_evidence_per_work_unit, target_bundle_version=bundle["schema_version"])
    selected_verified = {k: deepcopy(v) for k, v in verified.items()
                         if k not in {"compilation_sha256", "semantic_units", "evidence_dispositions"}}
    selected_verified["bundle_sha256"] = selected_bundle["bundle_sha256"]
    for field in ("semantic_units", "evidence_dispositions"):
        selected_verified[field] = [deepcopy(r) for r in verified[field] if r["evidence_id"] in wanted]
    excluded = [r["evidence_id"] for r in source["captured_items"] if r["evidence_id"] not in wanted]
    selection = {
        "schema_version": VERSION, "meaning": "derived complete-row reuse; not fresh verification",
        "original_inputs": deepcopy(dependencies), "selected_evidence_ids": selected_ids,
        "selected_source_sha256": selected_source["source_sha256"],
        "original_bundle_sha256": bundle["bundle_sha256"],
        "original_compilation_sha256": verified["compilation_sha256"],
        "original_manifest_sha256": {k: verified[k]["manifest_sha256"] for k in MANIFESTS if k in verified},
        "original_captured_row_count": len(source["captured_items"]),
        "original_verified_row_count": len(verified["evidence_dispositions"]),
        "original_semantic_unit_count": len(verified["semantic_units"]),
        "selected_row_count": len(rows), "selected_semantic_unit_count": len(selected_verified["semantic_units"]),
        "excluded_row_count": len(excluded), "excluded_evidence_ids_sha256": semantic._sha256(excluded),
        "max_prompt_bytes": max_prompt_bytes, "max_evidence_per_work_unit": max_evidence_per_work_unit,
    }
    selection["selection_sha256"] = semantic._sha256(selection)
    selected_verified["verified_row_selection"] = selection
    selected_verified["compilation_sha256"] = semantic._sha256(selected_verified)
    return selected_source, selected_bundle, selected_verified


def derive_verified_selection(dependencies, evidence_ids, *, max_prompt_bytes=80000, max_evidence_per_work_unit=30):
    originals = {k: load_original(v["path"], v["sha256"]) for k, v in dependencies.items()}
    return _derive(originals, dependencies, evidence_ids, max_prompt_bytes=max_prompt_bytes,
                   max_evidence_per_work_unit=max_evidence_per_work_unit)


def validate_verified_selection(bundle, compilation, *, source=None, load=load_original):
    """Reproduce the complete derived objects from required, content-pinned originals.

    Return the original bundle whose work units own the unchanged raw manifests.
    Snapshot readers supply their closed resolver; absent mappings never use live paths.
    """
    selection = compilation.get("verified_row_selection")
    if not isinstance(selection, dict) or selection.get("schema_version") != VERSION:
        raise semantic.SemanticIntegrationError("invalid verified row selection")
    semantic._verify_stored_hash(selection, field="selection_sha256", label="verified row selection")
    dependencies = selection.get("original_inputs")
    if not isinstance(dependencies, dict) or set(dependencies) != {"source", "bundle", "verified"}:
        raise semantic.SemanticIntegrationError("verified selection lacks original dependencies")
    for record in dependencies.values():
        if (not isinstance(record, dict) or set(record) != {"path", "sha256"}
                or not isinstance(record["path"], str) or not Path(record["path"]).is_absolute()
                or not isinstance(record["sha256"], str) or len(record["sha256"]) != 64):
            raise semantic.SemanticIntegrationError("invalid verified selection original dependency")
    originals = {k: load(v["path"], v["sha256"]) for k, v in dependencies.items()}
    expected_source, expected_bundle, expected_verified = _derive(originals, dependencies,
        selection.get("selected_evidence_ids"), max_prompt_bytes=selection.get("max_prompt_bytes"),
        max_evidence_per_work_unit=selection.get("max_evidence_per_work_unit"))
    if bundle != expected_bundle or compilation != expected_verified or (source is not None and source != expected_source):
        raise semantic.SemanticIntegrationError("verified selection differs from complete unchanged original rows or provenance")
    return originals["bundle"]


def provider_verified_evidence(compilation):
    """Keep selected evidence and compact provenance; full original proofs stay local."""
    if "verified_row_selection" not in compilation:
        return compilation
    return {k: v for k, v in compilation.items() if k not in MANIFESTS}
