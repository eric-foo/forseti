"""Reuse complete saved extraction batches in an explicitly smaller, unverified run.

Original bytes remain untouched. Derived response envelopes are deterministic
rebindings, never claimed as new model answers or independent verification.
"""
from collections import Counter
from copy import deepcopy
from pathlib import Path

from harness_utils import hash_file
from judgment import semantic_evidence_integration as semantic
from judgment.verified_evidence_selection import load_original, validate_source_bundle


VERSION = "semantic_extracted_batch_selection_v1"


def derive(dependencies):
    if set(dependencies) != {"source", "bundle", "responses"} or not dependencies["responses"]:
        raise ValueError("extracted selection requires source, bundle and explicit completed responses")
    source, bundle = (load_original(**dependencies[k]) for k in ("source", "bundle"))
    responses = [load_original(**record) for record in dependencies["responses"]]
    validate_source_bundle(source, bundle)
    semantic.validate_batch_responses(bundle, responses, require_all=False)
    def rows_by_id(owner, answers):
        batches = {b["batch_id"]: b["evidence_ids"] for b in owner["batches"]}
        rows = {}
        for response in answers:
            expanded = semantic._response_rows_by_id(response, batch_id=response["batch_id"],
                expected_ids=batches[response["batch_id"]], new_generation=True,
                response_version=semantic._expected_response_version(owner))
            rows.update({eid: {k: deepcopy(v) for k, v in row.items() if k != "terminal_group"}
                         for eid, row in expanded.items()})
        return rows
    proposed = rows_by_id(bundle, responses)
    wanted = set(proposed)
    if not wanted:
        raise ValueError("extracted selection contains no complete evidence rows")
    rows = [r for r in source["captured_items"] if r["evidence_id"] in wanted]
    if len(rows) != len(wanted):
        raise ValueError("extracted selection source ownership differs")
    counts = Counter(r["container_id"] for r in rows)
    selected = {k: deepcopy(v) for k, v in source.items()
                if k not in {"source_sha256", "captured_items", "containers"}}
    selected["captured_items"] = deepcopy(rows)
    selected["containers"] = [dict(deepcopy(r), captured_leaf_count=counts[r["container_id"]])
        for r in source["containers"] if r["container_id"] in counts]
    selected["corpus_profile"] = "bounded_regression_slice"
    selected["corpus_scope"] = source["corpus_scope"] + " | completed extraction batch selection; independent verification pending"
    selected["source_sha256"] = semantic._sha256(selected)
    selected_bundle = semantic.build_bundle(selected, max_prompt_bytes=bundle["max_prompt_bytes"],
        max_evidence_per_work_unit=bundle["semantic_work_unit_projection"]["max_evidence_per_work_unit"],
        target_bundle_version=bundle["schema_version"])
    rebound = [semantic._batch_response_from_rows(selected_bundle, batch["batch_id"],
        [proposed[eid] for eid in batch["evidence_ids"]]) for batch in selected_bundle["batches"]]
    check = semantic.validate_batch_responses(selected_bundle, rebound)
    if rows_by_id(selected_bundle, rebound) != proposed:
        raise ValueError("extracted selection changed a saved judgment")
    original_batches = {eid: r["batch_id"] for r in bundle["batches"] for eid in r["evidence_ids"] if eid in wanted}
    record = {"schema_version": VERSION, "meaning": "unchanged extraction reuse; independent verification pending",
        "original_inputs": deepcopy(dependencies), "original_batch_by_evidence_id": original_batches,
        "selected_evidence_ids": [r["evidence_id"] for r in rows],
        "selected_row_count": len(rows), "excluded_row_count": len(source["captured_items"]) - len(rows),
        "selected_semantic_unit_count": len(check["semantic_units"]),
        "source_sha256": selected["source_sha256"], "bundle_sha256": selected_bundle["bundle_sha256"],
        "derived_response_sha256": {r["batch_id"]: semantic._sha256(r) for r in rebound}}
    record["selection_sha256"] = semantic._sha256(record)
    return selected, selected_bundle, rebound, record


def prepare(*, source_path, bundle_path, response_paths, output_dir):
    from runners.run_semantic_evidence_integration import _write_json
    output_dir = Path(output_dir)
    if output_dir.exists():
        raise ValueError("refusing to replace an extracted selection directory")
    if not response_paths or len({Path(p).resolve() for p in response_paths}) != len(response_paths):
        raise ValueError("select distinct completed response files explicitly")
    def bind(path):
        path = Path(path).resolve(strict=True)
        return {"path": str(path), "expected": hash_file(path)}
    dependencies = {"source": bind(source_path), "bundle": bind(bundle_path),
                    "responses": [bind(p) for p in response_paths]}
    source, bundle, responses, record = derive(dependencies)
    for name, value in (("source", source), ("bundle", bundle), ("selection", record)):
        _write_json(output_dir / (name + ".json"), value)
    for response in responses:
        _write_json(output_dir / "responses" / (response["batch_id"] + ".json"), response)
    validate(output_dir / "selection.json", source, bundle)
    return {"status": "EXTRACTED_SELECTION_REQUIRES_VERIFICATION", "model_api_calls": 0,
        "output_dir": str(output_dir.resolve()), "selection_sha256": record["selection_sha256"],
        **{k: record[k] for k in ("selected_row_count", "excluded_row_count", "selected_semantic_unit_count")}}


def validate(selection_path, source, bundle):
    from runners.run_semantic_evidence_integration import _load_object
    selection_path = Path(selection_path)
    saved = _load_object(selection_path)
    if saved.get("schema_version") != VERSION:
        raise ValueError("unsupported extracted selection")
    semantic._verify_stored_hash(saved, field="selection_sha256", label="extracted selection")
    expected_source, expected_bundle, responses, expected = derive(saved["original_inputs"])
    if source != expected_source or bundle != expected_bundle or saved != expected:
        raise ValueError("extracted selection differs from its unchanged original judgments or source")
    response_dir = selection_path.parent / "responses"
    expected_paths = {response_dir / (r["batch_id"] + ".json") for r in responses}
    if set(response_dir.iterdir()) != expected_paths:
        raise ValueError("extracted selection has missing, unexpected or staged responses")
    for response in responses:
        if _load_object(response_dir / (response["batch_id"] + ".json")) != response:
            raise ValueError("extracted selection response differs from its original judgment")
    return responses
