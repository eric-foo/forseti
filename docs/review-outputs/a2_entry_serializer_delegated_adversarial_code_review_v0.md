# A2 Entry Serializer Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Delegated adversarial code review-and-patch of the A2 pinned entry
  serializer diff (PR #612, fused Lane A) by a cross-vendor controller, with
  the delegate's uncommitted working-tree patch adjudicated by the
  commissioning Chief Architect.
use_when:
  - Consuming the delegated review findings for the A2 serializer implementation.
  - Checking which dispatch/extraction defect classes were found, patched, and adjudicated.
authority_boundary: retrieval_only
reviewed_by: OpenAI GPT-5 (Codex)
authored_by: Anthropic Claude (Fable 5)
de_correlation_bar: cross_vendor_discovery
commission: https://github.com/eric-foo/orca/pull/612#issuecomment-4869201064
review_target: PR 612, branch claude/a2-implementation, head 7d1b8e9759291b743a7caf7eb000661a01326fa3
mode: delegated_code_review_and_patch
access: repo
source_context_ready: true
report_written: docs/review-outputs/a2_entry_serializer_delegated_adversarial_code_review_v0.md
patch_status: adjudicated_by_commissioning_ca_2026_07_03
stale_if:
  - The adjudicated patch is reverted or superseded on the lane branch.
  - A later review round over the same scope replaces this report.
non_claims:
  - not validation
  - not readiness
  - not acceptance
  - not a Bronze full-GT claim
  - not runtime model routing
```

Use boundary: all findings, diffs, citations, and verdicts in this report are
decision input only — not approval, not validation, not readiness, not
mandatory remediation, and not patch authority. What is kept is decided solely
by the commissioning Chief Architect's adjudication under
`.agents/workflow-overlay/review-lanes.md`.

## CA Adjudication (2026-07-03, commissioning Chief Architect)

- `F-01` ACCEPTED unmodified: fail-open verified against the pre-patch code
  (malformed present `manifest_version` values coerced to legacy dispatch via
  the string helper); the absent/null-vs-malformed split is the correct
  fail-closed boundary; parametrized red probes proved the gap pre-fix.
- `F-02` ACCEPTED unmodified: independently verified against
  `git show 2ed2059c:orca-harness/data_lake/catalog.py` that the old catalog
  helper stripped whitespace (`value.strip() or None`); the extraction had
  silently dropped the trim; restoring it re-aligns AR-row fields with the
  catalog's packet-entry fields for padded inputs.
- Kept: the full delegate diff, unmodified. Independent re-validation by the
  adjudicator: 54 targeted tests green (entry serializer + proof gate +
  catalog); delegate's pre-fix red probes (`FFFFF`) and full-suite exit 0
  accepted as claims consistent with the re-run evidence.

## Findings

### F-01 - major - [entry-serializer] Malformed `manifest_version` values were coerced to legacy dispatch

Original evidence: at commissioned head `7d1b8e97`, `orca-harness/data_lake/attachment_record_entry.py` used `string_or_none(manifest.get("manifest_version"))` inside `_require_supported_manifest_version`; because that helper returned `None` for non-strings and `""`, the dispatch gate only rejected unsupported non-empty strings. `derive_attachment_record_entries` calls that gate before inspecting `preserved_files`, so a packet manifest carrying `manifest_version: ""`, a number, an array, or an object could pass as the legacy/no-version case.

Authority basis: A2 ADR Required Outputs 4 and 7 require centralized dispatch and refusal of packets that cannot be safely mapped. The closeout also claims unknown sealed-packet formats are refused, never coerced.

Impact: the claimed fail-closed dispatch was incomplete. A malformed present version is not the same as an absent legacy version; treating it as legacy hides the format boundary the serializer is supposed to enforce.

Patch: `_require_supported_manifest_version` now allows only absent or `null` `manifest_version` as legacy, and rejects present malformed values or unsupported strings through the same fail-closed error path.

minimum_closure_condition: malformed present values (`""`, number, list, object, and by branch implication bool/unsupported string) raise `DataLakeRootError` before derivation; absent and `null` legacy manifests still dispatch as `None`.

next_authorized_action: Chief Architect adjudicates the finding and the `[entry-serializer]` / `[entry-tests]` hunks; if accepted, keep the patch and its regression tests.

### F-02 - major - [entry-serializer] Moved string extraction stopped preserving catalog trim semantics

Original evidence: old-base `catalog.py` normalized optional strings through `_string_or_none`, which stripped whitespace before returning a value. The new serializer's `string_or_none` returned any non-empty string unchanged. After catalog delegation, `_build_entries` still used the catalog trim helper for packet/source-surface summary fields, while `_packet_attachment_records` delegated Attachment Record row fields to the serializer. A whitespace-padded `source_family` or `source_surface` could therefore make catalog summary paths and AR row buckets disagree.

Authority basis: the commission explicitly called for comparison of moved helpers against `git show 2ed2059c:orca-harness/data_lake/catalog.py`, including `visible_fact_value` and posture-summary behavior. The PR claim is catalog rows equal canonical entry plus decorations, not canonical entry plus silent extraction drift.

Impact: this is a public-surface divergence risk, not style. A source-surface helper can resolve a stripped path from the summary while the generated AR rows were bucketed under unstripped values, hiding rows or changing downstream `raw_refs` behavior for otherwise valid manifest strings.

Patch: serializer `string_or_none` now strips whitespace and returns `None` for blank strings, matching the previous catalog helper behavior for source family, source surface, locator values, slice IDs, original path, payload schema version, and posture-summary strings. Manifest-version dispatch no longer uses that helper for the version gate, so strict version matching is preserved.

minimum_closure_condition: moved optional-string fields keep the old trim semantics while manifest-version dispatch still refuses malformed present values.

next_authorized_action: Chief Architect adjudicates the finding and the `[entry-serializer]` / `[entry-tests]` hunks; if accepted, keep the patch and regression test.

## Patch Summary

- `[entry-serializer][F-01]` Strictly separates legacy absent/null `manifest_version` from malformed present values.
- `[entry-serializer][F-02]` Restores the old catalog trim semantics in the moved shared string helper.
- `[entry-tests][F-01]` Adds fail-capable malformed-version cases and keeps absent/null legacy coverage.
- `[entry-tests][F-02]` Adds a direct derivation test for trim-preserving moved fields.

No patch was made to `[catalog]`, `[proof-gate]`, `[catalog-tests]`, or `[producer-tests]`; they were exercised by validation.

## Unified Uncommitted Diff

Hunk labels: `[entry-serializer][F-01,F-02]`; `[entry-tests][F-01,F-02]`.

```diff
diff --git a/orca-harness/data_lake/attachment_record_entry.py b/orca-harness/data_lake/attachment_record_entry.py
index 5a7819cb..9c40127c 100644
--- a/orca-harness/data_lake/attachment_record_entry.py
+++ b/orca-harness/data_lake/attachment_record_entry.py
@@ -49,16 +49,17 @@ SUPPORTED_ATTACHMENT_RECORD_BODY_REF_KINDS = frozenset({RAW_PACKET_BODY_REF_KIND
 SUPPORTED_ATTACHMENT_RECORD_HASH_BASIS = frozenset({"raw_stored_bytes"})
 
 # Central dispatch registry: raw manifest versions this derivation rule
-# version knows how to derive from. Legacy packets without a manifest_version
-# string dispatch through the same v1 rule (incumbent-compatible). Adding a
-# version here is a deliberate, reviewed act paired with a DERIVATION_RULE_VERSION
-# decision, never a consumer-side fork.
+# version knows how to derive from. Legacy packets with an absent/null
+# manifest_version dispatch through the same v1 rule (incumbent-compatible).
+# Adding a version here is a deliberate, reviewed act paired with a
+# DERIVATION_RULE_VERSION decision, never a consumer-side fork.
 SUPPORTED_RAW_PACKET_MANIFEST_VERSIONS = frozenset({"source_capture_packet_manifest_v1"})
 
 
 def string_or_none(value: object) -> str | None:
-    if isinstance(value, str) and value:
-        return value
+    if isinstance(value, str):
+        stripped = value.strip()
+        return stripped or None
     return None
 
 
@@ -121,14 +122,20 @@ def _require_supported_manifest_version(manifest: dict[str, Any]) -> str | None:
     """Centralized version dispatch (ADR Required Output 4). Fails closed on
     an unknown manifest version: sealed packets are never coerced through a
     rule that does not know their format."""
-    manifest_version = string_or_none(manifest.get("manifest_version"))
-    if manifest_version is not None and manifest_version not in SUPPORTED_RAW_PACKET_MANIFEST_VERSIONS:
+    if "manifest_version" not in manifest or manifest.get("manifest_version") is None:
+        return None
+    manifest_version = manifest["manifest_version"]
+    if (
+        not isinstance(manifest_version, str)
+        or not manifest_version
+        or manifest_version not in SUPPORTED_RAW_PACKET_MANIFEST_VERSIONS
+    ):
         allowed_list = ", ".join(sorted(SUPPORTED_RAW_PACKET_MANIFEST_VERSIONS))
         raise DataLakeRootError(
             f"unsupported raw packet manifest_version {manifest_version!r} for "
             f"Attachment Record entry derivation under {DERIVATION_RULE_VERSION}; "
-            f"supported: {{{allowed_list}}} (plus legacy packets without a version "
-            "string). Add a new derivation rule version deliberately in "
+            f"supported: {{{allowed_list}}} (plus legacy packets with absent/null "
+            "manifest_version). Add a new derivation rule version deliberately in "
             "data_lake.attachment_record_entry; do not fork per-version logic in a "
             "consumer, and never rewrite the sealed packet."
         )
diff --git a/orca-harness/tests/test_data_lake_attachment_record_entry.py b/orca-harness/tests/test_data_lake_attachment_record_entry.py
index b4b96814..dd31ba79 100644
--- a/orca-harness/tests/test_data_lake_attachment_record_entry.py
+++ b/orca-harness/tests/test_data_lake_attachment_record_entry.py
@@ -123,9 +123,42 @@ def test_dispatch_fails_closed_on_unknown_manifest_version() -> None:
         )
 
 
-def test_legacy_manifest_without_version_string_dispatches(tmp_path: Path) -> None:
-    manifest = {"preserved_files": []}
+@pytest.mark.parametrize(
+    "malformed_manifest_version",
+    [
+        "",
+        12,
+        ["source_capture_packet_manifest_v1"],
+        {"version": "source_capture_packet_manifest_v1"},
+    ],
+)
+def test_dispatch_fails_closed_on_malformed_manifest_version(
+    malformed_manifest_version: object,
+) -> None:
+    manifest = {
+        "manifest_version": malformed_manifest_version,
+        "preserved_files": [],
+    }
+
+    with pytest.raises(DataLakeRootError, match="unsupported raw packet manifest_version"):
+        derive_attachment_record_entries(
+            packet_id="0" * 26,
+            raw_path="raw/000/" + "0" * 26,
+            manifest_relpath="raw/000/" + "0" * 26 + "/manifest.json",
+            manifest_sha256="0" * 64,
+            manifest=manifest,
+            bodies={},
+        )
 
+
+@pytest.mark.parametrize(
+    "manifest",
+    [
+        {"preserved_files": []},
+        {"manifest_version": None, "preserved_files": []},
+    ],
+)
+def test_legacy_manifest_without_version_string_dispatches(manifest: dict) -> None:
     entries = derive_attachment_record_entries(
         packet_id="0" * 26,
         raw_path="raw/000/" + "0" * 26,
@@ -138,6 +171,59 @@ def test_legacy_manifest_without_version_string_dispatches(tmp_path: Path) -> No
     assert entries == []
 
 
+def test_moved_string_fields_preserve_catalog_trim_semantics() -> None:
+    body = b"{}"
+    manifest = {
+        "manifest_version": "source_capture_packet_manifest_v1",
+        "source_family": " reddit ",
+        "source_surface": " r/EntrySerializer ",
+        "source_locator": {
+            "status": "known",
+            "value": " https://example.invalid/item ",
+        },
+        "source_slices": [{"slice_id": " slice_01 ", "preserved_file_ids": ["file_01"]}],
+        "preserved_files": [
+            {
+                "file_id": "file_01",
+                "relative_packet_path": "raw/body.json",
+                "sha256": "0" * 64,
+                "hash_basis": "raw_stored_bytes",
+                "size_bytes": len(body),
+                "original_path": " body.json ",
+                "payload_schema_version": " schema-v1 ",
+            }
+        ],
+        "access_posture": {
+            "status": "known",
+            "value": " local_file_only ",
+            "reason": " fixture ",
+        },
+    }
+
+    entries = derive_attachment_record_entries(
+        packet_id="0" * 26,
+        raw_path="raw/000/" + "0" * 26,
+        manifest_relpath="raw/000/" + "0" * 26 + "/manifest.json",
+        manifest_sha256="0" * 64,
+        manifest=manifest,
+        bodies={"file_01": body},
+    )
+
+    assert len(entries) == 1
+    entry = entries[0]
+    assert entry["source_family"] == "reddit"
+    assert entry["source_surface"] == "r/EntrySerializer"
+    assert entry["source_locator"] == "https://example.invalid/item"
+    assert entry["source_slice_ids"] == ["slice_01"]
+    assert entry["original_path"] == "body.json"
+    assert entry["payload_schema_version"] == "schema-v1"
+    assert entry["posture_summary"]["access_posture"] == {
+        "status": "known",
+        "value": "local_file_only",
+        "reason": "fixture",
+    }
+
+
 def test_missing_required_preserved_field_is_refused(tmp_path: Path) -> None:
     manifest = {
         "manifest_version": "source_capture_packet_manifest_v1",
```

## Validation

Pre-fix red probes, after adding only the new tests and before changing implementation:

```text
$env:ORCA_DATA_ROOT=$null; $env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider -q tests/test_data_lake_attachment_record_entry.py -k "malformed_manifest_version or moved_string_fields"
exit 1
FFFFF [100%]
Failures: four malformed manifest_version cases DID NOT RAISE; trim-semantic probe saw ' reddit ' != 'reddit'.
```

Post-fix entry serializer tests:

```text
$env:ORCA_DATA_ROOT=$null; $env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider -q tests/test_data_lake_attachment_record_entry.py
exit 0
............. [100%]
```

Commissioned targeted test files:

```text
$env:ORCA_DATA_ROOT=$null; $env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider -q tests/test_data_lake_attachment_record_entry.py tests/test_data_lake_physicalization_proof.py tests/test_data_lake_catalog.py tests/unit/test_creator_metric_silver_producer.py tests/unit/test_youtube_creator_metric_silver_producer.py
exit 0
.......................................s................................ [ 94%]
.... [100%]
```

Full suite from `orca-harness/` with `ORCA_DATA_ROOT` unset:

```text
$env:ORCA_DATA_ROOT=$null; $env:PYTHONDONTWRITEBYTECODE=1; python -m pytest -p no:cacheprovider -q
exit 0
... [100%]
warning: PytestUnknownMarkWarning for tests\integration\test_reddit_screening_read_live.py:17 unknown pytest.mark.integration
```

`git diff --check`:

```text
exit 0
warning: LF will be replaced by CRLF the next time Git touches the two edited Python files
```

## Verdict

Overall verdict: two material patchable defects were found in the commissioned A2 serializer diff and patched in the uncommitted working tree. No `NEEDS_ARCHITECTURE_PASS`; no out-of-scope patching.

Per-file sub-verdicts:

- `[entry-serializer]` `orca-harness/data_lake/attachment_record_entry.py`: patch returned for CA adjudication on F-01 and F-02.
- `[entry-tests]` `orca-harness/tests/test_data_lake_attachment_record_entry.py`: regression tests returned for CA adjudication on F-01 and F-02.
- `[catalog]` `orca-harness/data_lake/catalog.py`: no patch; reviewed for delegation boundary and moved-helper drift.
- `[proof-gate]` `orca-harness/tests/test_data_lake_physicalization_proof.py`: no patch; targeted validation passed.
- `[catalog-tests]` `orca-harness/tests/test_data_lake_catalog.py`: no patch; targeted validation passed.
- `[producer-tests]` Silver producer tests: no patch; targeted validation passed.
- Read-and-flag-only contracts and closeout: no stronger-than-fixture-lake claim flagged.

## Explicit Non-Findings

- The canonical-vs-materialized equality proof is not merely tautological on the inspected code path: it strips only the catalog-only keys plus the catalog schema pin; added, dropped, or changed canonical fields still affect the serialized comparison.
- Unsupported string versions, including casing changes, already fail through the unsupported-string path; the patched gap was malformed present non-string/empty values.
- `PurePosixPath` use in payload classification does not create a Windows path traversal issue on by-key reads because `DataLakeRoot.load_raw_packet` verifies preserved paths before bodies reach the serializer.
- Catalog compatibility aliases preserve the existing import names `_attachment_record_id` and `_require_supported_attachment_record_hash_basis`; no production consumer literal for schema `_2` was found in the commissioned review scope.
- No review evidence supports a full Bronze-GT, readiness, backend, retention, Manifest v2, or production-lake validation claim.

## Residual Risk

- The patch proves representative malformed JSON value classes for `manifest_version` (empty string, number, array, object) plus absent/null legacy behavior. It does not claim production-lake validation.
- The review used the explicit commissioned diff range `2ed2059c..7d1b8e97`. Local `origin/main` had advanced to `c2f5449`, but the branch merge-base remained `2ed2059c`; this was recorded as a preflight caveat, not used to widen the review.
- The full test suite passed at fixture/CI-equivalent tier with `ORCA_DATA_ROOT` unset; external live-lake behavior remains outside this commission.

## Delegated Return Courier

DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

Include:
- original commission or review target: PR 612 issue comment 4869201064, A2 Pinned Entry Serializer Lane A
- implementation context, diff, and reviewed files: `2ed2059c..7d1b8e97`; patchable file set honored; uncommitted diff included above
- findings and implementation evidence: F-01 malformed `manifest_version` coercion; F-02 moved string trim drift
- proposed patch, diff, or exact requested edits: included above, uncommitted
- citations: original serializer dispatch/string helper behavior; old-base catalog trim helper behavior; A2 ADR Required Outputs 4 and 7
- reviewer verdict: two major patchable defects found and patched; no architecture-pass stop
- validation evidence and not-run checks: red probes failed before implementation fix; entry, targeted, and full suites exit 0 after patch; no production-lake validation run
- residual risk: fixture/CI-equivalent tier only; CA must adjudicate before keeping hunks
- blockers, off-scope flags, and not-proven boundaries: no blockers; no out-of-scope patch; not validation/readiness/full-GT

Review Adjudication Next Step for the commissioning Chief Architect: first adjudicate F-01, F-02, the diff hunks, this verdict, and the residuals as claims. If accepted or modified, self-close any material issue that remains inside the commissioned patch scope in the same turn and re-check. Once no unresolved material issue remains, batch admin/lifecycle into one land step for the PR branch, then deep-think only the next 1-5 material moves that need judgment. If a non-self-closable material issue remains, route only the smallest complete closure step for that issue before downstream material planning.