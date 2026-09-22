"""Derived reuse must preserve whole rows and original proof at every consumer."""
from copy import deepcopy
import json
from pathlib import Path

import pytest

from harness_utils import hash_file
from judgment import semantic_evidence_integration as semantic
from judgment import verified_evidence_selection as selection
from judgment.review_evidence import render_evidence
from reports import finite_closeout
from reports.finite_failure_evidence import SavedEvidence
from runners import run_finite_semantic_consolidation as finite
from runners import run_semantic_evidence_integration as native
from test_semantic_evidence_integration import (
    _source_v7, _v5_responses, _row_verification_responses, _finite_decision_response,
)


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def rehash(value, field):
    value.pop(field, None)
    value[field] = semantic._sha256(value)


def test_normal_advance_reuses_selected_verification_and_rejects_changed_originals(originals, tmp_path):
    dependencies, ids, _ = originals
    selected = selection.derive_verified_selection(dependencies, ids)
    paths = {name: tmp_path / "selected" / (name + ".json") for name in ("source", "bundle", "verified")}
    for (name, path), value in zip(paths.items(), selected):
        write(path, value)
    kwargs = dict(source_path=paths["source"], bundle_path=paths["bundle"], verified_path=paths["verified"], run_dir=tmp_path / "run")
    first = native.advance_semantic_run(**kwargs)
    assert first["status"] == "SEMANTIC_JUDGMENT_REQUIRED" and first["phase"] == "reconciliation", first.get("error")
    assert all(r["phase"] == "reconciliation" for r in first["judgment_requests"])
    assert not (tmp_path / "run/extraction").exists()
    proof = Path(dependencies["verified"]["path"])
    original = json.loads(proof.read_text())
    original["evidence_dispositions"][0]["disposition_reason"] += " Coherently changed."
    rehash(original, "compilation_sha256")
    write(proof, original)
    failed = native.advance_semantic_run(**kwargs)
    assert failed["status"] == "SEMANTIC_ADVANCE_BLOCKED" and not failed["judgment_requests"]
    assert "dependency changed" in failed["error"]
    proof.unlink()
    failed = native.advance_semantic_run(**kwargs)
    assert "dependency unavailable" in failed["error"] and not failed["judgment_requests"]


def test_normal_advance_rejects_paired_wrong_source_before_new_judgments(originals, tmp_path):
    dependencies, ids, _ = originals
    source, bundle, verified = selection.derive_verified_selection(dependencies, ids)
    source["captured_items"][0]["text"] += " Altered source meaning."
    rehash(source, "source_sha256")
    paths = {name: tmp_path / (name + ".json") for name in ("source", "bundle", "verified")}
    for (name, path), value in zip(paths.items(), (source, bundle, verified)):
        write(path, value)
    failed = native.advance_semantic_run(source_path=paths["source"], bundle_path=paths["bundle"], verified_path=paths["verified"], run_dir=tmp_path / "run")
    assert failed["status"] == "SEMANTIC_ADVANCE_BLOCKED" and not failed["judgment_requests"]
    assert "differs" in failed["error"] and not (tmp_path / "run").exists()


@pytest.fixture
def originals(tmp_path):
    source = _source_v7(count=6)
    bundle = semantic.build_bundle(source, max_prompt_bytes=80000, max_evidence_per_work_unit=30)
    responses = _v5_responses(bundle, detailed_per_batch=2)
    units = responses[0]["evidence"][0]["semantic_units"]
    units.append({**deepcopy(units[0]), "semantic_unit_key": "second"})
    compiled = semantic.validate_batch_responses(bundle, responses)
    stage, _ = semantic.prepare_row_verification(bundle, compiled)
    verified = semantic.apply_row_verification(bundle, compiled, stage, _row_verification_responses(stage))
    dependencies = {}
    for name, value in (("source", source), ("bundle", bundle), ("verified", verified)):
        path = tmp_path / "original" / (name + ".json")
        write(path, value)
        dependencies[name] = {"path": str(path.resolve()), "sha256": hash_file(path)}
    ids = [r["evidence_id"] for r in bundle["evidence_units"]]
    return dependencies, [ids[0], ids[1], ids[-1]], (source, bundle, verified)


def test_native_selection_preparation_finite_consumers_and_no_unit_rows(originals, tmp_path):
    dependencies, ids, (original_source, original_bundle, original_verified) = originals
    ids_path = tmp_path / "ids.json"
    write(ids_path, ids)
    out = tmp_path / "selected"
    assert native.main(["select-verified-rows", *[arg for k, v in dependencies.items() for arg in ("--" + k, v["path"])],
                        "--evidence-ids", str(ids_path), "--output-dir", str(out)]) == 0
    source, bundle, verified = [json.loads((out / (name + ".json")).read_text(encoding="utf-8"))
                                for name in ("source", "bundle", "verified")]
    assert (source, bundle, verified) == selection.derive_verified_selection(dependencies, list(reversed(ids)))
    assert source["captured_items"] == [r for r in original_source["captured_items"] if r["evidence_id"] in ids]
    assert len(verified["semantic_units"]) == 3
    assert len(verified["evidence_dispositions"]) == 3
    assert all(verified[k] == original_verified[k] for k in selection.MANIFESTS if k in original_verified)
    stage_path, prompts = tmp_path / "stage.json", tmp_path / "prompts"
    result = native.prepare_reconciliation_level(bundle_path=out / "bundle.json", compilation_path=out / "verified.json",
        stage_out=stage_path, prompt_dir=prompts, reconciliation_policy_version=semantic.RECONCILIATION_POLICY_VERSION_V2,
        completion_strategy=semantic.FINITE_COMPLETION_STRATEGY)
    assert result["model_api_calls"] == 0 and result["candidate_count"] == 3
    assert list(prompts.glob("*.md")) and list(prompts.glob("*.schema.json"))
    formation = json.loads(stage_path.read_text(encoding="utf-8"))
    groups = [[(ref, "support")] for ref in formation["batches"][0]["candidate_refs"]]
    formed = semantic.validate_reconciliation_stage(bundle, formation,
        [_finite_decision_response(formation, groups, terminal=False)])
    finish, _ = semantic.prepare_reconciliation_stage(bundle, formed,
        completion_strategy=semantic.FINITE_COMPLETION_STRATEGY, packing_strategy="group_aware_v1")
    finished = semantic.validate_reconciliation_stage(bundle, finish,
        [_finite_decision_response(finish, [[(r, "support") for r in finish["batches"][0]["candidate_refs"]]], terminal=True)])
    view = semantic.finalize_v3_view(bundle, verified, finished)
    packet = semantic.project_evidence_packet(view, bundle, verified, finished,
        proposition_ids=[p["proposition_id"] for p in view["propositions"]])
    assert finite.coverage(bundle, verified, view, packet)["source_rows"] == 3
    assert semantic.finalize_v3_view(bundle, verified, finished) == view  # Frozen finite replay closure.
    questions = {"assessment_only": {"checks": [{"id": "all", "source_rows": ids}]}}
    closeout = finite_closeout.evidence_view(source, verified, view, questions)
    assert {r["evidence_id"] for r in closeout["source_rows"]} == set(ids)
    assert len(closeout["evidence_dispositions"]) == 3
    model_view = selection.provider_verified_evidence(verified)
    assert not set(selection.MANIFESTS) & model_view.keys()
    assert model_view["semantic_units"] == verified["semantic_units"]
    rendered = render_evidence(model_view)
    excluded = set(r["evidence_id"] for r in original_bundle["evidence_units"]) - set(ids)
    assert not any(i in rendered for i in excluded)
    for record in dependencies.values():
        assert hash_file(Path(record["path"])) == record["sha256"]


@pytest.mark.parametrize("change", ["text", "context", "catalog", "method", "unit", "drop_unit", "disposition", "drop_disposition", "proof"])
def test_rehashed_selected_tampering_rejected(originals, change):
    dependencies, ids, _ = originals
    source, bundle, verified = selection.derive_verified_selection(dependencies, ids)
    if change in {"text", "context", "catalog", "method"}:
        if change == "text":
            source["captured_items"][0]["text"] += " Changed meaning."
        elif change == "context":
            source["captured_items"][0]["parent_context"] = [{"text": "changed parent context"}]
        elif change == "catalog":
            source["product_identity_catalog"] = {"catalog_id": "changed"}
        else:
            source["semantic_method_version"] = semantic.METHOD_VERSION_V8
        rehash(source, "source_sha256")
        # A source edit must fail even if a caller preserves the old bundle.
        with pytest.raises(semantic.SemanticIntegrationError, match="differs"):
            selection.validate_verified_selection(bundle, verified, source=source)
        return
    if change == "unit":
        verified["semantic_units"][0]["conditions"] = ["fabricated condition"]
    elif change == "drop_unit":
        verified["semantic_units"].pop()
    elif change == "disposition":
        verified["evidence_dispositions"][-1]["disposition_reason"] = "changed"
    elif change == "drop_disposition":
        verified["evidence_dispositions"].pop()
    else:
        verified["row_verification_manifest"]["decision_counts"]["accept"] += 1
        rehash(verified["row_verification_manifest"], "manifest_sha256")
    rehash(verified, "compilation_sha256")
    with pytest.raises(semantic.SemanticIntegrationError, match="differs"):
        semantic.prepare_reconciliation_stage(bundle, verified)


@pytest.mark.parametrize("bad_ids", [[], ["foreign"], ["row::partial"], ["duplicate", "duplicate"]])
def test_foreign_duplicate_partial_or_empty_selection_rejected(originals, bad_ids):
    with pytest.raises(semantic.SemanticIntegrationError, match="IDs"):
        selection.derive_verified_selection(originals[0], bad_ids)


@pytest.mark.parametrize("name", ["source", "bundle", "verified"])
def test_missing_or_changed_original_dependency_rejected(originals, name):
    dependencies, ids, _ = originals
    source, bundle, verified = selection.derive_verified_selection(dependencies, ids)
    path = Path(dependencies[name]["path"])
    raw = path.read_bytes()
    path.write_bytes(raw + b" ")
    with pytest.raises(semantic.SemanticIntegrationError, match="dependency changed"):
        semantic.prepare_reconciliation_stage(bundle, verified)
    path.unlink()
    with pytest.raises(semantic.SemanticIntegrationError, match="dependency unavailable"):
        selection.validate_verified_selection(bundle, verified, source=source)


def test_frozen_snapshot_uses_original_proof_copies_and_refuses_live_fallback(originals, tmp_path):
    dependencies, ids, _ = originals
    source, bundle, verified = selection.derive_verified_selection(dependencies, ids)
    base = tmp_path / "snapshot"
    files = {}
    for name, record in dependencies.items():
        path = base / (name + ".json")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(Path(record["path"]).read_bytes())
        files[path.name] = {"original": record["path"], "sha256": record["sha256"]}
    manifest = base / "manifest.json"
    write(manifest, {"files": files})
    frozen = SavedEvidence(manifest)
    Path(dependencies["verified"]["path"]).write_text("changed live original", encoding="utf-8")
    selection.validate_verified_selection(bundle, verified, source=source, load=frozen.load)
    assert len(frozen.hashes) == 4
    # An incomplete snapshot cannot use an existing original dependency.
    files.pop("source.json")
    (base / "source.json").unlink()
    write(manifest, {"files": files})
    incomplete = SavedEvidence(manifest)
    with pytest.raises((ValueError, FileNotFoundError)):
        selection.validate_verified_selection(bundle, verified, source=source, load=incomplete.load)


def test_selected_run_reaches_complete_finite_closeout_and_resume(tmp_path):
    from test_finite_closeout import saved_correction_run
    run, result = saved_correction_run(tmp_path, "mixed", selected=True)
    view = finite_closeout.collect(run.root)
    assert view["saved_result"] == result
    originals = run.verified["verified_row_selection"]["original_inputs"]
    assert all(record["path"] in view["read_artifact_hashes"] for record in originals.values())
    assert result["coverage"]["verified_selection"]["selected_row_count"] == 3
    assessment = finite.read(run.root / "assessment/input.json")["complete_frozen_verified_evidence"]
    assert not set(selection.MANIFESTS) & assessment.keys()
    assert assessment["semantic_units"] == run.verified["semantic_units"]
    assert run.run() == result
    assert finite_closeout.collect(run.root) == view
    Path(originals["verified"]["path"]).write_text("tampered proof", encoding="utf-8")
    with pytest.raises(ValueError, match="saved binding changed"):
        finite_closeout.collect(run.root)


def test_actual_frozen_failure_closeout_does_not_follow_live_originals(originals, tmp_path):
    from test_finite_failure_evidence import failed_run, snapshot
    live = tmp_path / "live"
    dependencies = {}
    for name, value in zip(("source", "bundle", "verified"), originals[2]):
        path = live / "original-proof" / (name + ".json")
        write(path, value)
        dependencies[name] = {"path": str(path.resolve()), "sha256": hash_file(path)}
    selected = selection.derive_verified_selection(dependencies, originals[1])
    root, failure, paths = failed_run(live)
    binding = finite.read(root / "binding.json")
    for name, value in zip(("source", "bundle", "verified"), selected):
        write(paths[name], value)
        binding["inputs"][name]["sha256"] = hash_file(paths[name])
    binding["verified_selection_original_inputs"] = dependencies
    write(root / "binding.json", binding)
    record = finite.read(failure)
    record["evidence_files"] = {str(p): hash_file(p) for p in root.rglob("*") if p.is_file() and p != failure}
    write(failure, record)
    frozen = tmp_path / "frozen"
    manifest = snapshot(live, frozen)
    Path(dependencies["verified"]["path"]).write_text("changed live original", encoding="utf-8")
    result = finite_closeout.collect(frozen / "run", failure_record=frozen / "run/failure-001.json",
                                    snapshot_manifest=manifest)
    assert result["schema_version"] == "finite_failure_closeout_v1"
    assert str(frozen / "original-proof/verified.json") in result["read_artifact_hashes"]
    assert not any(path.startswith(str(live)) for path in result["read_artifact_hashes"])


@pytest.mark.parametrize("field", ["method_version", "product_identity_catalog", "evidence_units"])
def test_rehashed_selected_bundle_cannot_change_original_semantics(originals, field):
    dependencies, ids, _ = originals
    _, bundle, verified = selection.derive_verified_selection(dependencies, ids)
    if field == "method_version":
        bundle[field] = semantic.METHOD_VERSION_V8
    elif field == "product_identity_catalog":
        bundle[field] = {"catalog_id": "different"}
    else:
        bundle[field][0]["text"] += " changed source"
    rehash(bundle, "bundle_sha256")
    verified["bundle_sha256"] = bundle["bundle_sha256"]
    rehash(verified, "compilation_sha256")
    with pytest.raises(semantic.SemanticIntegrationError):
        semantic.prepare_reconciliation_stage(bundle, verified)


def test_rehashed_changed_original_proof_still_requires_original_active_content(originals):
    dependencies, ids, (_, _, verified) = originals
    verified["semantic_units"][0]["conditions"] = ["not verified"]
    rehash(verified, "compilation_sha256")
    path = Path(dependencies["verified"]["path"])
    write(path, verified)
    dependencies["verified"]["sha256"] = hash_file(path)
    with pytest.raises(semantic.SemanticIntegrationError, match="active row content"):
        selection.derive_verified_selection(dependencies, ids)
