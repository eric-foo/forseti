# Bronze Physicalization Proof Scope Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Delegated adversarial code review-and-patch of the Bronze physicalization
  proof-scope diff (PR #589, A1 inventory gate + PROOF-01..06) by a
  cross-vendor controller, with the delegate's uncommitted working-tree patch
  adjudicated by the commissioning Chief Architect.
use_when:
  - Consuming the delegated review findings for the physicalization proof scope.
  - Checking which fake-pass/tautology/silent-exclusion classes were found, patched, and adjudicated.
authority_boundary: retrieval_only
reviewed_by: OpenAI GPT-5 Codex
authored_by: Anthropic Claude (Fable 5)
de_correlation_bar: cross_vendor_discovery
commission_source: https://github.com/eric-foo/orca/pull/589#issuecomment-4866180797
access_mode: repo
mode: delegated_code_review_and_patch
output_mode: review-report
report_path: docs/review-outputs/bronze_physicalization_proof_scope_delegated_adversarial_code_review_v0.md
patch_status: adjudicated_by_commissioning_ca_2026_07_02
stale_if:
  - The adjudicated patch is reverted or superseded on the lane branch.
  - A later review round over the same scope replaces this report.
```

Use boundary: all findings, diffs, citations, and verdicts in this report are
decision input only — not approval, not validation, not readiness, not
mandatory remediation, and not patch authority. What is kept is decided solely
by the commissioning Chief Architect's adjudication under
`.agents/workflow-overlay/review-lanes.md`.

## CA Adjudication (2026-07-02, commissioning Chief Architect)

- `[ADV-01]` ACCEPTED unmodified: detector gap verified against the pre-patch
  code (Name-only base); dotted-name fix is fail-safe-directional; seeded
  tests pin both import shapes.
- `[ADV-02]` ACCEPTED unmodified: size-vs-sha masking verified (loader
  fail-closes on size before sha); size-preserving tamper isolates the
  hash_basis invariant; wrong-cause `match=` tightening accepted for
  PROOF-02/03/05/06.
- `[ADV-03]` ACCEPTED unmodified: exclusions-family diff gap and
  thin-resolved-unknown self-certification residue verified; class-specific
  violations plus seeded tests accepted.
- Kept: the full delegate diff, unmodified. Independent re-validation by the
  adjudicator: 36 targeted tests green; `check_dcp_receipt.py --strict` OK;
  `header_index.py --strict` OK; inventory JSON byte-unchanged.

## Commission

Review PR #589 at `claude/bronze-proof-scope-impl` head `223f460e` against base `origin/main` `1dfbb2d0`. Attack the claim that the Bronze lake proof layer cannot pass vacuously: every gate/proof must fail on its seeded violation, inventory entries must not be silently excluded, and artifact text must not claim beyond fixture-lake-tier proof.

## Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom delegated code-review-and-patch pack
  edit_permission: patch-only inside commissioned file set; report write authorized at docs/review-outputs/...
  target_scope: PR #589 A1 inventory gate plus PROOF-01..06 proof gate; read-only flag for closeout/MGT/ADRs/contracts
  dirty_state_checked: yes (target worktree clean before delegate patch)
  blocked_if_missing: none
```

Preflight observed before patching:

- Branch: `claude/bronze-proof-scope-impl`.
- Head: `223f460e`.
- Base: `origin/main` `1dfbb2d0`.
- Clean target worktree before delegate edits.
- No `NEEDS_ARCHITECTURE_PASS`: all material issues found were patch-level inside the named file set.

## Source-Read Ledger

- `AGENTS.md` and `.agents/workflow-overlay/README.md`: project entry and overlay binding.
- `.agents/workflow-overlay/delegated-review-patch.md`: repo-mode delegated code-review-and-patch contract.
- `.agents/workflow-overlay/safety-rules.md`: patch boundary and protected-path rules.
- `.agents/workflow-overlay/prompt-orchestration.md` targeted sections: Source-Gated Method Contract, Review Prompt Defaults, review-report output mode.
- `.agents/workflow-overlay/review-lanes.md`, `.agents/workflow-overlay/validation-gates.md`, `.agents/workflow-overlay/communication-style.md`: review doctrine, gate semantics, report closeout and adjudicator tail.
- `workflow-deep-thinking` and `workflow-code-review` skill instructions: reference-loaded before source application.
- PR diff `1dfbb2d0..223f460e`, all five patchable files in full, closeout record, MGT baseline declaration, both ratified gate ADRs, folded AR implementation contract, and the scoping route.
- Targeted behavior reads: `orca-harness/data_lake/root.py` and `orca-harness/data_lake/catalog.py` for the public error paths asserted by PROOF-02..06.

SOURCE_CONTEXT_READY was declared before applying the review methods.

## Findings

### [ADV-01] major - writer discovery missed unaliased module-import writer calls

- Label: `[inventory-module]` / `[seam-test]`.
- Location: `orca-harness/data_lake/inventory.py:189`, `orca-harness/data_lake/inventory.py:283`, `orca-harness/data_lake/inventory.py:303`; seeded tests at `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py:157` and `:175`.
- Evidence: before the patch, `is_imported_module_writer_call()` only accepted an `ast.Name` module base. A runner using `import source_capture.youtube_watch_packet` and then calling `source_capture.youtube_watch_packet.write_youtube_watch_packet(..., data_root=root)` has an `ast.Attribute` base, so it was not detected as a packet writer. `from source_capture import youtube_watch_packet` was also not added to `module_aliases` when the imported name was a module rather than a writer function.
- Impact: a future raw-packet writer could be added behind a common import form without tripping the seam/inventory discovery gate, undercutting the no-silent-writer-exclusion claim.
- Patch: added `dotted_name()` and module-alias handling for unaliased full imports and `from source_capture import module` forms; added seeded seam tests for both shapes.
- minimum_closure_condition: fresh discovery detects aliased, unaliased dotted, and from-imported `source_capture` module writer calls, with seeded tests that fail against the old detector shape.
- next_authorized_action: commissioning CA adjudicates the diff; if accepted, keep the patch and land through the PR lane.

### [ADV-02] major - PROOF-04 could fail on size mismatch before proving SHA verification

- Label: `[proof-gate]`.
- Location: `orca-harness/tests/test_data_lake_physicalization_proof.py:57`, `:192`, `:235`.
- Evidence: the original `_corrupt_preserved_body()` replaced `{"b": "alpha"}` with `{"b": "tampered"}`. That changes stored-byte length, so `DataLakeRoot.load_raw_packet()` can fail at `size_bytes` mismatch before reaching the `sha256` check. The closeout and Gate 1 authority specifically claim `hash_basis: raw_stored_bytes` verification.
- Impact: the seeded violation did not isolate the invariant it claimed to prove. A broken hash check could be masked by an earlier size guard.
- Patch: tamper now preserves serialized byte length and the PROOF-04/05 violation halves assert `preserved file sha256 mismatch` specifically.
- minimum_closure_condition: corrupt-body violations keep size constant and fail on the SHA verification path through public reads.
- next_authorized_action: commissioning CA adjudicates the diff; if accepted, keep the patch and land through the PR lane.

### [ADV-03] major - exclusion and resolved-unknown checks lacked class-specific fail-capability

- Label: `[inventory-module]` / `[inventory-gate]`.
- Location: `orca-harness/data_lake/inventory.py:476`, `orca-harness/data_lake/inventory.py:499`, `orca-harness/tests/contract/test_data_lake_inventory_gate.py:99`, `:132`.
- Evidence: before the patch, `inventory_violations()` compared raw writer and non-raw touchpoint families, but did not compare `exclusions` against the freshly generated inventory. A reasoned but non-generated exclusion could avoid a class-specific violation in `inventory_violations()`. Also, a resolved unknown needed only `owner_disposition.status == "resolved"`; it did not require a concrete disposition or owner-attribution evidence.
- Impact: the inventory proof claimed reasoned exclusions and owner-dispositioned unknowns, but the seeded proof did not cover plausible silent-exclusion and thin-disposition shapes.
- Patch: `inventory_violations()` now diffs `exclusions` and requires resolved unknowns to carry target, question, concrete disposition, and owner-attribution evidence; seeded tests cover reasoned exclusion drift and a thin resolved unknown.
- minimum_closure_condition: plausible reasoned exclusions and thin resolved unknowns produce explicit violations, not only generic drift or self-certifying status fields.
- next_authorized_action: commissioning CA adjudicates the diff; if accepted, keep the patch and land through the PR lane.

## Non-Findings

- Seam-test assertion baselines remain present after delegation: current Bronze writer runner set, non-raw touchpoint counter, exclusive output modes, unsynced reasons, data_root forwarding, orchestrator forwarding, and direct raw-publication bans are still asserted.
- The checked-in inventory record remains generated and byte-identical to `build_inventory()` after the patch; no inventory JSON change was needed.
- Closeout and MGT text stay inside fixture-lake-tier, non-production, non-full-GT claim boundaries. The hash-proof wording became defensible after the PROOF-04 patch.
- No backend, A2 serialization, second body home, erasure, production-lake validation, full-GT, or readiness claim was introduced.

## Validation Evidence

Targeted command, from `orca-harness/`, with `ORCA_DATA_ROOT` unset:

```text
python -m pytest -q tests\contract\test_capture_runner_lake_seam_coverage.py tests\contract\test_data_lake_inventory_gate.py tests\test_data_lake_physicalization_proof.py
....................................                                     [100%]
```

Full-suite command, from `orca-harness/`, with `ORCA_DATA_ROOT` unset:

```text
python -m pytest
2395 passed, 7 skipped, 1 warning in 224.42s (0:03:44)
```

Failure visibility note: an earlier full-suite run printed the same completed test summary but the tool wrapper returned exit 124 at timeout. It was rerun with a larger timeout and exited 0.

## Overall Verdict

Material issues were found and patched inside the commissioned file set. After the delegate patch, I found no remaining blocker in the reviewed scope. This verdict is decision input only for the commissioning Chief Architect; it is not approval, validation, readiness, a PASS claim, or a full-GT claim.

## Per-File Sub-Verdicts

- `orca-harness/data_lake/inventory.py`: patched for `[ADV-01]` and `[ADV-03]`; no remaining reviewed-scope blocker found.
- `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py`: patched seeded coverage for `[ADV-01]`; pre-existing assertion baselines retained.
- `orca-harness/tests/contract/test_data_lake_inventory_gate.py`: patched seeded coverage for `[ADV-03]`; current inventory still clears the gate.
- `orca-harness/tests/test_data_lake_physicalization_proof.py`: patched `[ADV-02]` and tightened wrong-cause exception checks for PROOF-02/03/06.
- `orca-harness/data_lake/lake_touchpoint_inventory_v0.json`: no change required.

## Residual Risk

The review attacked import-shape discovery, exclusion/unknown proof classes, wrong-cause seeded failures, and seam-test delegation. It did not attempt all possible AST import/call patterns, production-lake validation, backend behavior, A2 serialization consequences, or real-lane fixture breadth; those remain outside this commissioned scope or already named residuals.

## Unified Working-Tree Diff

Hunk label map:

- `[ADV-01]`: `inventory.py` `dotted_name` / module alias detection; seam tests for unaliased and from-imported module calls.
- `[ADV-02]`: proof tamper helper preserving byte length; proof exception `match=` assertions for hash and wrong-cause guards.
- `[ADV-03]`: exclusion drift comparison; resolved-unknown detail requirements; seeded inventory-gate tests.

```diff
diff --git a/orca-harness/data_lake/inventory.py b/orca-harness/data_lake/inventory.py
index 3f797733..52d7fd7b 100644
--- a/orca-harness/data_lake/inventory.py
+++ b/orca-harness/data_lake/inventory.py
@@ -186,6 +186,17 @@ def call_name(node: ast.Call) -> str | None:
     return None
 
 
+def dotted_name(node: ast.AST) -> str | None:
+    if isinstance(node, ast.Name):
+        return node.id
+    if isinstance(node, ast.Attribute):
+        parent = dotted_name(node.value)
+        if parent is None:
+            return None
+        return f"{parent}.{node.attr}"
+    return None
+
+
 def called_names(node: ast.AST) -> set[str]:
     return {
         name
@@ -280,10 +291,12 @@ def source_capture_imports(tree: ast.AST) -> tuple[set[str], set[str]]:
             for alias in node.names:
                 if is_packet_writer_name(alias.name, packet_writer_names):
                     writer_names.add(alias.asname or alias.name)
+                else:
+                    module_aliases.add(alias.asname or alias.name)
         elif isinstance(node, ast.Import):
             for alias in node.names:
                 if alias.name.startswith("source_capture."):
-                    module_aliases.add(alias.asname or alias.name.split(".")[-1])
+                    module_aliases.add(alias.asname or alias.name)
     return writer_names, module_aliases
 
 
@@ -292,7 +305,8 @@ def is_imported_module_writer_call(node: ast.Call, module_aliases: set[str]) ->
         return False
     if not is_packet_writer_name(node.func.attr, source_capture_packet_writer_names()):
         return False
-    return isinstance(node.func.value, ast.Name) and node.func.value.id in module_aliases
+    base_name = dotted_name(node.func.value)
+    return base_name in module_aliases
 
 
 def producer_calls(
@@ -459,6 +473,7 @@ def inventory_violations(declared: dict, discovered: dict) -> list[str]:
         ("raw_packet_writers", "runner_seams"),
         ("raw_packet_writers", "writer_functions"),
         ("non_raw_touchpoints", None),
+        ("exclusions", None),
     ):
         label = f"{family}.{subfamily}" if subfamily else family
         declared_set = _entry_set(declared, family, subfamily)
@@ -479,5 +494,18 @@ def inventory_violations(declared: dict, discovered: dict) -> list[str]:
                 "unknown without a resolved owner disposition (owner-attributable via the "
                 f"human-gated PR merge; pending fails the gate): {unknown.get('target')!r}"
             )
+            continue
+        if not str(unknown.get("target", "")).strip():
+            violations.append("resolved unknown without a target")
+        if not str(unknown.get("question", "")).strip():
+            violations.append(f"resolved unknown without a question: {unknown.get('target')!r}")
+        if not str(disposition.get("disposition", "")).strip():
+            violations.append(
+                f"resolved unknown without a concrete disposition: {unknown.get('target')!r}"
+            )
+        if not str(disposition.get("recorded_by", "")).strip():
+            violations.append(
+                f"resolved unknown without owner-attribution evidence: {unknown.get('target')!r}"
+            )
 
     return violations
diff --git a/orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py b/orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
index 14724917..675f732c 100644
--- a/orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
+++ b/orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py
@@ -154,6 +154,42 @@ def main(root):
     assert calls[0].forwards_data_root is True
 
 
+def test_detector_follows_unaliased_source_capture_module_import_packet_writer() -> None:
+    tree = ast.parse(
+        """
+import source_capture.youtube_watch_packet
+
+def main(root):
+    return source_capture.youtube_watch_packet.write_youtube_watch_packet(fetch, data_root=root)
+"""
+    )
+
+    writer_names, module_aliases = _source_capture_imports(tree)
+    calls = _producer_calls(tree, writer_names, module_aliases)
+
+    assert len(calls) == 1
+    assert calls[0].name == "write_youtube_watch_packet"
+    assert calls[0].forwards_data_root is True
+
+
+def test_detector_follows_from_imported_source_capture_module_packet_writer() -> None:
+    tree = ast.parse(
+        """
+from source_capture import youtube_watch_packet
+
+def main(root):
+    return youtube_watch_packet.write_youtube_watch_packet(fetch, data_root=root)
+"""
+    )
+
+    writer_names, module_aliases = _source_capture_imports(tree)
+    calls = _producer_calls(tree, writer_names, module_aliases)
+
+    assert len(calls) == 1
+    assert calls[0].name == "write_youtube_watch_packet"
+    assert calls[0].forwards_data_root is True
+
+
 def test_detector_discovers_indirect_source_capture_packet_writers() -> None:
     writers = _source_capture_packet_writer_names()
 
@@ -180,6 +216,7 @@ def test_non_raw_lake_touchpoint_inventory_is_explicit() -> None:
         f"removed={dict(sorted(removed.items()))}"
     )
 
+
 def test_non_raw_lake_touchpoint_inventory_reads_tracked_source_only() -> None:
     relative_paths = {
         path.relative_to(_HARNESS_ROOT).as_posix() for path in _tracked_harness_python_files()
@@ -189,6 +226,7 @@ def test_non_raw_lake_touchpoint_inventory_reads_tracked_source_only() -> None:
     assert not any(path.startswith("tests/") for path in relative_paths)
     assert not any(path.startswith("_test_runs/") for path in relative_paths)
 
+
 def test_detector_distinguishes_packet_output_from_summary_output_root() -> None:
     tree = ast.parse(
         """
diff --git a/orca-harness/tests/contract/test_data_lake_inventory_gate.py b/orca-harness/tests/contract/test_data_lake_inventory_gate.py
index 9ac13013..0cdc60eb 100644
--- a/orca-harness/tests/contract/test_data_lake_inventory_gate.py
+++ b/orca-harness/tests/contract/test_data_lake_inventory_gate.py
@@ -96,6 +96,21 @@ def test_gate_fails_on_seeded_reasonless_exclusion() -> None:
     ), violations
 
 
+def test_gate_fails_on_seeded_reasoned_exclusion_drift() -> None:
+    declared = copy.deepcopy(load_declared_inventory())
+    declared["exclusions"].append(
+        {"target": "seeded/reasoned_but_not_generated", "reason": "plausible but stale"}
+    )
+
+    violations = inventory_violations(declared, build_inventory())
+
+    assert any(
+        "stale exclusions entry" in violation
+        and "seeded/reasoned_but_not_generated" in violation
+        for violation in violations
+    ), violations
+
+
 def test_gate_fails_on_seeded_undispositioned_unknown() -> None:
     declared = copy.deepcopy(load_declared_inventory())
     declared["unknowns"].append(
@@ -115,6 +130,30 @@ def test_gate_fails_on_seeded_undispositioned_unknown() -> None:
     ), violations
 
 
+def test_gate_fails_on_seeded_resolved_unknown_missing_disposition_detail() -> None:
+    declared = copy.deepcopy(load_declared_inventory())
+    declared["unknowns"].append(
+        {
+            "target": "seeded/thin_resolved_unknown",
+            "question": "is this a lake touchpoint?",
+            "owner_disposition": {"status": "resolved"},
+        }
+    )
+
+    violations = inventory_violations(declared, build_inventory())
+
+    assert any(
+        "resolved unknown without a concrete disposition" in violation
+        and "seeded/thin_resolved_unknown" in violation
+        for violation in violations
+    ), violations
+    assert any(
+        "resolved unknown without owner-attribution evidence" in violation
+        and "seeded/thin_resolved_unknown" in violation
+        for violation in violations
+    ), violations
+
+
 def test_resolved_unknown_clears_without_weakening_other_checks() -> None:
     declared = copy.deepcopy(load_declared_inventory())
     declared["unknowns"].append(
diff --git a/orca-harness/tests/test_data_lake_physicalization_proof.py b/orca-harness/tests/test_data_lake_physicalization_proof.py
index c9cf8305..118fa6e6 100644
--- a/orca-harness/tests/test_data_lake_physicalization_proof.py
+++ b/orca-harness/tests/test_data_lake_physicalization_proof.py
@@ -57,10 +57,16 @@ def _packet_container(root: DataLakeRoot, packet_id: str) -> Path:
 
 def _corrupt_preserved_body(root: DataLakeRoot, packet_id: str, body: str) -> Path:
     """Overwrite the preserved body file's stored bytes (tamper simulation)."""
+    assert body, "tamper helper requires a non-empty body"
     original = json.dumps({"b": body}, sort_keys=True).encode("utf-8")
+    replacement_body = "z" * len(body)
+    if replacement_body == body:
+        replacement_body = "y" * len(body)
+    tampered = json.dumps({"b": replacement_body}, sort_keys=True).encode("utf-8")
+    assert len(tampered) == len(original), "tamper must preserve size to prove SHA checking"
     for path in sorted(_packet_container(root, packet_id).rglob("*")):
         if path.is_file() and path.read_bytes() == original:
-            path.write_bytes(json.dumps({"b": "tampered"}, sort_keys=True).encode("utf-8"))
+            path.write_bytes(tampered)
             return path
     raise AssertionError("preserved body file not found in packet container")
 
@@ -132,7 +138,7 @@ def test_proof_02_violation_rewriting_an_existing_record_is_refused(tmp_path: Pa
             record_id="record_01.json",
             data=b'{"ok": true}',
         )
-        with pytest.raises(DataLakeRootError):
+        with pytest.raises(DataLakeRootError, match="refusing to overwrite existing record"):
             root.append_record(
                 subtree=subtree,
                 raw_anchor=packet_id,
@@ -159,7 +165,7 @@ def test_proof_03_violation_missing_packet_fails_closed(tmp_path: Path) -> None:
     root = DataLakeRoot.for_test(tmp_path / "orca-data")
     _capture(root, tmp_path, "alpha")
 
-    with pytest.raises(DataLakeRootError):
+    with pytest.raises(DataLakeRootError, match="raw packet not committed"):
         root.load_raw_packet("0" * 26)
 
 
@@ -183,7 +189,7 @@ def test_proof_04_violation_tampered_body_fails_verified_read(tmp_path: Path) ->
 
     _corrupt_preserved_body(root, packet_id, body)
 
-    with pytest.raises(DataLakeRootError):
+    with pytest.raises(DataLakeRootError, match="preserved file sha256 mismatch"):
         root.load_raw_packet(packet_id)
 
 
@@ -226,7 +232,7 @@ def test_proof_05_violation_tampered_body_fails_public_ar_resolution(tmp_path: P
 
     _corrupt_preserved_body(root, packet_id, body)
 
-    with pytest.raises(DataLakeRootError):
+    with pytest.raises(DataLakeRootError, match="preserved file sha256 mismatch"):
         load_attachment_record_body(root, record)
 
 
@@ -266,7 +272,7 @@ def test_proof_06_violation_reads_survive_index_loss_so_indexes_carry_no_authori
     assert loaded.manifest["packet_id"] == packet_id
     # The generated catalog is gone and must fail loudly (stale reads refused),
     # while raw truth stays readable by key: indexes are caches, never authority.
-    with pytest.raises(DataLakeRootError):
+    with pytest.raises(DataLakeRootError, match="Bronze catalog is not current"):
         source_surface_catalog_rows(
             root, source_family=_SOURCE_FAMILY, source_surface=_SOURCE_SURFACE
         )
```

## Adjudicator Tail

Commissioning Chief Architect should adjudicate this return under `.agents/workflow-overlay/communication-style.md` -> Review Adjudication Next Step and `docs/prompts/templates/review/delegated_review_return_adjudication_v0.md`: first adjudicate findings, diff, verdict, and residuals as claims; close self-closable material issues same-turn; use one batched land step for admin once clean; then deep-think the 1-5 material next moves that genuinely require judgment.