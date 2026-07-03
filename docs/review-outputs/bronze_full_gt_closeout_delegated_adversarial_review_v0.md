# Bronze Full-GT Closeout Delegated Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial code review-and-patch report
scope: Bronze full-GT closeout assembled contracts and code at claude/a2-implementation head 1a7600ad, with patch authority limited to the named patchable file set in PR #612 comment 4870056388.
use_when:
  - Adjudicating the delegated adversarial review return for PR #612 Bronze full-GT closeout.
  - Checking whether the A2 attachment-record implementation and proof gates need further patching before owner decision.
authority_boundary: retrieval_only
reviewed_by: OpenAI GPT-5 (Codex)
authored_by: Anthropic Claude (Fable 5)
review_use_boundary: >
  Findings are decision input only. They are not approval, validation,
  readiness, mandatory remediation, or patch authority until separately
  accepted or authorized by the owning Orca lane.
```

## Findings

### F-01 - Minor - [proof-gate] [entry-tests] Projection-only canonical-row proof did not prove the catalog decoration envelope

Status: patched in this return.

Evidence: the catalog wrapper declares that materialized Attachment Record rows are the canonical serializer output plus catalog-only generated read-state fields at `orca-harness/data_lake/catalog.py:782`, then adds `authority`, catalog versions, a catalog replay pin, and stable query paths at `orca-harness/data_lake/catalog.py:796`. The pre-patch equality proof stripped catalog-only fields before comparing, so it proved canonical byte equality but did not independently prove that the materialized row contained exactly the allowed decoration envelope. The patch adds exact envelope assertions in `orca-harness/tests/test_data_lake_attachment_record_entry.py:63` and calls them before the equality proof at `orca-harness/tests/test_data_lake_attachment_record_entry.py:120`; PROOF-07 mirrors that closure at `orca-harness/tests/test_data_lake_physicalization_proof.py:53` and `orca-harness/tests/test_data_lake_physicalization_proof.py:322`.

Impact: this was a proof-gate weakness, not an observed production-code divergence. A future wrapper drift that changed catalog-only keys or added replay pins could have been less visible while canonical projection still passed.

Minimum closure condition: keep the attached test hardening, with the focused A2/proof, catalog, inventory, seam-coverage, producer tests, full `orca-harness` suite, and strict provenance checker passing.

Next authorized action: home-model adjudication may accept or reject this patch. No architecture pass is required unless the home model wants to change the catalog row contract itself.

No critical or major findings were found.

## Unified Uncommitted Diff

```diff
diff --git a/orca-harness/tests/test_data_lake_attachment_record_entry.py b/orca-harness/tests/test_data_lake_attachment_record_entry.py
index dd31ba79..532e841d 100644
--- a/orca-harness/tests/test_data_lake_attachment_record_entry.py
+++ b/orca-harness/tests/test_data_lake_attachment_record_entry.py
@@ -22,12 +22,18 @@ from data_lake.attachment_record_entry import (
     serialize_entries,
     serialize_entry,
 )
-from data_lake.catalog import rebuild_catalog, source_surface_catalog_rows
+from data_lake.catalog import (
+    BRONZE_CATALOG_SCHEMA_VERSION,
+    BRONZE_CATALOG_VERSION,
+    rebuild_catalog,
+    source_surface_catalog_rows,
+)
 from data_lake.root import DataLakeRoot, DataLakeRootError
 from source_capture.models import known_fact
 from source_capture.writer import write_local_source_capture_packet
 
 _CATALOG_ONLY_KEYS = {"authority", "catalog_version", "catalog_schema_version", "stable_query_paths"}
+_CATALOG_REPLAY_PIN_KEYS = {"catalog_schema_version"}
 
 
 def _capture(root: DataLakeRoot, tmp_path: Path, body: str):
@@ -54,6 +60,24 @@ def _canonical_projection(row: dict) -> dict:
     return canonical
 
 
+def _assert_row_is_canonical_plus_catalog_decorations(row: dict, canonical: dict) -> None:
+    assert set(row) == set(canonical) | _CATALOG_ONLY_KEYS
+    assert row["catalog_version"] == BRONZE_CATALOG_VERSION
+    assert row["catalog_schema_version"] == BRONZE_CATALOG_SCHEMA_VERSION
+    assert isinstance(row["authority"], str) and row["authority"]
+    stable_query_paths = row["stable_query_paths"]
+    assert set(stable_query_paths) == {"by_attachment_record", "by_packet"}
+    assert stable_query_paths["by_attachment_record"] == (
+        f"attachment_records/by_attachment_record/{row['attachment_record_id']}.json"
+    )
+    assert stable_query_paths["by_packet"].startswith("attachment_records/by_packet/")
+    assert stable_query_paths["by_packet"].endswith(".jsonl")
+    row_pins = row["replay_version_pins"]
+    canonical_pins = canonical["replay_version_pins"]
+    assert set(row_pins) == set(canonical_pins) | _CATALOG_REPLAY_PIN_KEYS
+    assert row_pins["catalog_schema_version"] == BRONZE_CATALOG_SCHEMA_VERSION
+
+
 def test_every_entry_carries_the_ratified_version_pins(tmp_path: Path) -> None:
     root = DataLakeRoot.for_test(tmp_path / "orca-data")
     packet_id = _capture(root, tmp_path, "alpha").packet.packet_id
@@ -93,11 +117,19 @@ def test_by_key_derivation_equals_canonical_part_of_catalog_rows(tmp_path: Path)
     rows = source_surface_catalog_rows(
         root, source_family="reddit", source_surface="r/EntrySerializer"
     )["attachment_record_rows"]
+    derived_entries = derive_entries_by_key(root, packet_id)
+    derived_by_id = {entry["attachment_record_id"]: entry for entry in derived_entries}
+    rows_by_id = {
+        row["attachment_record_id"]: row for row in rows if row["packet_id"] == packet_id
+    }
+    assert set(rows_by_id) == set(derived_by_id)
+    for record_id, row in rows_by_id.items():
+        _assert_row_is_canonical_plus_catalog_decorations(row, derived_by_id[record_id])
     materialized_canonical = serialize_entries(
-        [_canonical_projection(row) for row in rows if row["packet_id"] == packet_id]
+        [_canonical_projection(rows_by_id[record_id]) for record_id in sorted(rows_by_id)]
     )
 
-    derived = serialize_entries(derive_entries_by_key(root, packet_id))
+    derived = serialize_entries([derived_by_id[record_id] for record_id in sorted(derived_by_id)])
 
     assert derived == materialized_canonical, (
         "the materialized catalog row must be exactly the canonical entry plus "
diff --git a/orca-harness/tests/test_data_lake_physicalization_proof.py b/orca-harness/tests/test_data_lake_physicalization_proof.py
index 8d591bac..c168d770 100644
--- a/orca-harness/tests/test_data_lake_physicalization_proof.py
+++ b/orca-harness/tests/test_data_lake_physicalization_proof.py
@@ -26,6 +26,8 @@ import pytest
 
 from data_lake.attachment_record_entry import derive_entries_by_key, serialize_entries
 from data_lake.catalog import (
+    BRONZE_CATALOG_SCHEMA_VERSION,
+    BRONZE_CATALOG_VERSION,
     load_attachment_record_body,
     rebuild_catalog,
     source_surface_catalog_rows,
@@ -36,6 +38,34 @@ from source_capture.writer import write_local_source_capture_packet
 
 _SOURCE_FAMILY = "reddit"
 _SOURCE_SURFACE = "r/PhysicalizationProof"
+_CATALOG_ONLY_KEYS = {"authority", "catalog_version", "catalog_schema_version", "stable_query_paths"}
+_CATALOG_REPLAY_PIN_KEYS = {"catalog_schema_version"}
+
+
+def _canonical_projection(row: dict) -> dict:
+    canonical = {key: value for key, value in row.items() if key not in _CATALOG_ONLY_KEYS}
+    pins = dict(canonical["replay_version_pins"])
+    pins.pop("catalog_schema_version", None)
+    canonical["replay_version_pins"] = pins
+    return canonical
+
+
+def _assert_row_is_canonical_plus_catalog_decorations(row: dict, canonical: dict) -> None:
+    assert set(row) == set(canonical) | _CATALOG_ONLY_KEYS
+    assert row["catalog_version"] == BRONZE_CATALOG_VERSION
+    assert row["catalog_schema_version"] == BRONZE_CATALOG_SCHEMA_VERSION
+    assert isinstance(row["authority"], str) and row["authority"]
+    stable_query_paths = row["stable_query_paths"]
+    assert set(stable_query_paths) == {"by_attachment_record", "by_packet"}
+    assert stable_query_paths["by_attachment_record"] == (
+        f"attachment_records/by_attachment_record/{row['attachment_record_id']}.json"
+    )
+    assert stable_query_paths["by_packet"].startswith("attachment_records/by_packet/")
+    assert stable_query_paths["by_packet"].endswith(".jsonl")
+    row_pins = row["replay_version_pins"]
+    canonical_pins = canonical["replay_version_pins"]
+    assert set(row_pins) == set(canonical_pins) | _CATALOG_REPLAY_PIN_KEYS
+    assert row_pins["catalog_schema_version"] == BRONZE_CATALOG_SCHEMA_VERSION
 
 
 def _capture(root: DataLakeRoot, tmp_path: Path, body: str):
@@ -289,14 +319,19 @@ def test_proof_07_canonical_entries_derive_by_key_with_zero_indexes(tmp_path: Pa
     rows = source_surface_catalog_rows(
         root, source_family=_SOURCE_FAMILY, source_surface=_SOURCE_SURFACE
     )["attachment_record_rows"]
-    catalog_only = {"authority", "catalog_version", "catalog_schema_version", "stable_query_paths"}
-    materialized_canonical = []
-    for row in rows:
-        canonical = {key: value for key, value in row.items() if key not in catalog_only}
-        pins = dict(canonical["replay_version_pins"])
-        pins.pop("catalog_schema_version", None)
-        canonical["replay_version_pins"] = pins
-        materialized_canonical.append(canonical)
+    derived_before_index_loss = derive_entries_by_key(root, packet_id)
+    derived_by_id = {
+        entry["attachment_record_id"]: entry for entry in derived_before_index_loss
+    }
+    rows_by_id = {
+        row["attachment_record_id"]: row for row in rows if row["packet_id"] == packet_id
+    }
+    assert set(rows_by_id) == set(derived_by_id)
+    for record_id, row in rows_by_id.items():
+        _assert_row_is_canonical_plus_catalog_decorations(row, derived_by_id[record_id])
+    materialized_canonical = [
+        _canonical_projection(rows_by_id[record_id]) for record_id in sorted(rows_by_id)
+    ]
 
     shutil.rmtree(root.path / "indexes")
```

## Verdict

Verdict: accept-with-minor-test-hardening, decision-input only. The assembled state does not show a critical or major blocker against the A2 closeout claim ceiling after F-01 is retained. This is not approval, readiness, production validation, or a full-GT declaration.

## Per-Surface Sub-Verdicts

- Contract-to-code seams: no blocker. The serializer centralizes version pins and derivation-rule ownership at `orca-harness/data_lake/attachment_record_entry.py:42`, dispatches raw manifest versions fail-closed at `orca-harness/data_lake/attachment_record_entry.py:121`, and derives by key through verified raw packet load without indexes at `orca-harness/data_lake/attachment_record_entry.py:303`.
- Catalog wrapper: no production-code patch. The wrapper copies the canonical entry and adds generated catalog fields at `orca-harness/data_lake/catalog.py:795`; F-01 hardens tests around that boundary.
- Proof-gate fail capability: acceptable with patch. PROOF-07 now checks exact row decoration shape before deleting indexes and deriving by key at `orca-harness/tests/test_data_lake_physicalization_proof.py:322`.
- Version-pin integrity: no issue found. The schema, physicalization, serialization, and derivation-rule pins are centralized in `attachment_record_entry.py`; producer tests import the schema constant instead of hardcoding it at `orca-harness/tests/unit/test_creator_metric_silver_producer.py:33` and `orca-harness/tests/unit/test_youtube_creator_metric_silver_producer.py:33`.
- Claim inflation: no issue found in the reviewed surfaces. The baseline declaration says it is not validation/readiness/full GT at `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md:40`; the A2 closeout states fixture-lake tier and not full GT at `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_a2_implementation_closeout_v0.md:29`; catalog semantics repeat the no-readiness/no-validation boundary at `orca-harness/data_lake/catalog.py:39`.
- Cross-lane merge seams: no issue found. The RSS monitor is included in the expected Bronze writer set at `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py:73`, declares a bound identity mechanism at `orca-harness/data_lake/inventory.py:292`, and the seam test requires every Bronze writer to declare valid identity binding at `orca-harness/tests/contract/test_capture_runner_lake_seam_coverage.py:296`.

## Residual Risk Note

Residual risks accepted here are the same claim-ceiling risks named by the source records: fixture-lake coverage is not production-lake validation, all-source coverage, storage-engine selection, replay tooling, real-lane fixture breadth, erasure capability, or full-GT approval. Gate 2 deletion posture remains deferred; final full-GT declaration remains owner/adjudicator work, not a property of this review.

## Explicit Non-Findings

- No `NEEDS_ARCHITECTURE_PASS` trigger was found.
- No runtime-model recommendation is made.
- No patch outside the authorized test/proof surfaces was needed.
- No generated inventory rewrite was needed.
- No GitHub comment was resolved or posted by this return.

## Validation Evidence

- Focused A2/proof tests: `python -m pytest tests/test_data_lake_attachment_record_entry.py tests/test_data_lake_physicalization_proof.py -q` from `orca-harness/` with `ORCA_DATA_ROOT` unset returned exit 0 and `27 passed`.
- Broader focused commission set: `python -m pytest tests/test_data_lake_attachment_record_entry.py tests/test_data_lake_physicalization_proof.py tests/test_data_lake_catalog.py tests/contract/test_data_lake_inventory_gate.py tests/contract/test_capture_runner_lake_seam_coverage.py tests/unit/test_creator_metric_silver_producer.py tests/unit/test_youtube_creator_metric_silver_producer.py -q` from `orca-harness/` with `ORCA_DATA_ROOT` unset returned exit 0, with one expected skip.
- Full suite: `python -m pytest` from `orca-harness/` with `ORCA_DATA_ROOT` unset returned exit 0: `2529 passed, 7 skipped, 1 warning in 208.57s (0:03:28)`.
- Strict provenance: `python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/bronze_full_gt_closeout_delegated_adversarial_review_v0.md` returned exit 0 with no findings.

## DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Return type: delegated adversarial review-and-patch.

Review result: one minor proof-gate hardening finding, patched in the uncommitted diff above; no critical or major findings.

Home-model adjudication request: decide whether to retain F-01's test hardening. If retained and validation remains green, this review supports moving to the next owner/adjudicator decision step within the existing claim ceiling.

## Review Adjudication Next Step

The commissioning CA should adjudicate F-01 and the attached uncommitted diff as decision input. If accepted, the next material move is to keep the patch and report on the A2 lane, then proceed through the lane's normal commit, push, and PR/update flow without treating this review as approval, readiness, validation, or a full-GT declaration.

## CA Adjudication (2026-07-03)

- Adjudicator: commissioning Chief Architect (Anthropic Claude, Fable 5 — the artifact author; de-correlation held at review time, reviewed_by above).
- F-01: **ACCEPTED unmodified.** The pre-patch projection proof caught foreign row keys but not a dropped decoration or decoration-value drift (strip of an absent key is a no-op); the exact-envelope assertions close that class. Patch stays inside the commissioned patchable set (test files only; no production code).
- Independent verification (not inherited from the delegate): `BRONZE_CATALOG_VERSION` / `BRONZE_CATALOG_SCHEMA_VERSION` confirmed at `orca-harness/data_lake/catalog.py:31`; derive output confirmed already id-sorted at `orca-harness/data_lake/attachment_record_entry.py:288`, so the test-side re-sort masks no ordering regression; focused commission test set re-run exit 0 (one expected skip) with `ORCA_DATA_ROOT` unset; strict provenance checker re-run exit 0 on this report.
- Verdict, per-surface sub-verdicts, residual-risk note, and non-findings adjudicated as claims and kept: consistent with the commission's claim ceiling; no reopened ratified decision found in the report.
- This adjudication is a keep-decision on the delegated return only — not approval, validation, readiness, or a full-GT declaration.