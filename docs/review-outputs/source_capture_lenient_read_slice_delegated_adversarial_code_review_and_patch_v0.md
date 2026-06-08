# Source Capture Lenient-Read Slice - Delegated Adversarial Code Review-and-Patch v0

```yaml
status: completed
review_location: docs/review-outputs/source_capture_lenient_read_slice_delegated_adversarial_code_review_and_patch_v0.md
recommendation: patch_proposed
authority_boundary: decision_input_only
patch_application: not_applied
commit_status: not_committed
```

## Preflight

- `AGENTS.md`: read.
- `.agents/workflow-overlay/README.md`: read.
- Required overlay reads: `review-lanes.md`, `delegated-review-patch.md`, `prompt-orchestration.md`, `safety-rules.md`.
- `workflow-deep-thinking`: REFERENCE-LOAD completed before source loading; APPLY completed after source readiness.
- `workflow-code-review`: REFERENCE-LOAD completed before source loading; APPLY completed after source readiness.
- Target scope: four commissioned slice files only.
- Dirty state: checked. Worktree is broadly dirty; the slice files and controlling sources are uncommitted/untracked. This report is advisory decision input only and makes no strict PASS/readiness/settled claim.

## Source Context

`SOURCE_CONTEXT_READY`

Source-loaded evidence:

- `git diff -- orca-harness/source_capture/source_quality.py orca-harness/tests/unit/test_source_quality_state_assembler.py`: read.
- `orca-harness/source_capture/packet_inspection.py`: read in full.
- `orca-harness/tests/unit/test_packet_inspection.py`: read in full.
- `orca-harness/source_capture/source_quality.py`: read with line numbers.
- `orca-harness/tests/unit/test_source_quality_state_assembler.py`: read with line numbers.
- Frozen-contract anchor `docs/product/source_capture_packet_schema_evolution_architecture_v0.md`: read for target-architecture and Adjudication & Amendment anchors.
- Repo search over target surface and relevant call sites: `read_packet_leniently`, `inspect_packet_manifest`, `packet_conformance`, `manifest_nonconforming`, `manifest_uninspectable`, `preserved_by_id`, `SourceCapturePacket.model_validate`, and relevant exception handlers.

Hash anchors confirmed:

| Path | Expected 12-char prefix | Observed prefix | Status |
| --- | --- | --- | --- |
| `orca-harness/source_capture/packet_inspection.py` | `E031FF2DF768` | `E031FF2DF768` | match |
| `orca-harness/source_capture/source_quality.py` | `7B244BAE24DB` | `7B244BAE24DB` | match |
| `orca-harness/tests/unit/test_packet_inspection.py` | `3615168E8128` | `3615168E8128` | match |
| `orca-harness/tests/unit/test_source_quality_state_assembler.py` | `23B323A08852` | `23B323A08852` | match |

Validation run for current worktree, not for the proposed unapplied diff:

```text
python -m pytest -q orca-harness\tests\unit\test_packet_inspection.py orca-harness\tests\unit\test_source_quality_state_assembler.py
.................                                                        [100%]
PytestCacheWarning: could not create cache path ... orca-harness\.pytest_cache\...\nodeids: [WinError 5] Access is denied
```

## Findings

### DRP-01

```yaml
id: DRP-01
severity: major
seam: Census vocabulary / AR-01 honesty
file_line_citation: orca-harness/source_capture/source_quality.py:88
minimum_closure_condition: >
  A parseable manifest that lacks a string manifest_version must not be described
  as declaring a non-current schema version or as off-version evidence. The
  visible stop must preserve the distinction between "declares non-current" and
  "does not validly declare a version", and the unit test must pin that branch.
```

Citation evidence:

- `orca-harness/source_capture/source_quality.py:80-92` builds the census visible stop. The current branch treats every non-current report the same, including `declared_manifest_version is None`, and emits "declares a non-current schema version" plus "off-version evidence, not corruption".
- `orca-harness/source_capture/packet_inspection.py:89-91` sets `declared_manifest_version` to `None` when the manifest_version value is missing or non-string. That is not an actual non-current declaration.
- `orca-harness/tests/unit/test_source_quality_state_assembler.py:86-113` creates `{"not": "a packet"}`, then currently asserts that the row's visible stop includes "non-current schema version". The test therefore pins the false statement rather than the AR-01 distinction.
- `docs/product/source_capture_packet_schema_evolution_architecture_v0.md:529-540` binds AR-01: the lenient read may report the declared version as a fact and current-schema conformance; it must not overpromise beyond knowable version facts.

Impact:

This does not hand a `SourceCapturePacket` to callers and does not make the row conforming. It is still material because the user-visible census language launders a malformed/unknown-version manifest into "off-version evidence, not corruption." That weakens the fake-success guard the slice is supposed to provide.

## Proposed Patch

Not applied in repo. This is a bounded unified diff proposal over accepted finding DRP-01 only.

```diff
diff --git a/orca-harness/source_capture/source_quality.py b/orca-harness/source_capture/source_quality.py
--- a/orca-harness/source_capture/source_quality.py
+++ b/orca-harness/source_capture/source_quality.py
@@ -85,6 +85,13 @@ def _nonconformance_stop(report: PacketConformanceReport) -> str:
             f"({report.declared_manifest_version!r}) but does not conform to it: "
             f"{error_count} schema error(s) — possible corruption of a current-version packet"
         )
+    if report.declared_manifest_version is None:
+        return (
+            "manifest does not declare a string manifest_version; "
+            f"inspected leniently against the current schema and found {error_count} "
+            "non-conformance(s) — malformed or unknown-version packet, not off-version evidence"
+        )
     return (
         f"manifest declares a non-current schema version "
         f"({report.declared_manifest_version!r}); inspected leniently against the current "
diff --git a/orca-harness/tests/unit/test_source_quality_state_assembler.py b/orca-harness/tests/unit/test_source_quality_state_assembler.py
--- a/orca-harness/tests/unit/test_source_quality_state_assembler.py
+++ b/orca-harness/tests/unit/test_source_quality_state_assembler.py
@@ -109,7 +109,7 @@ def test_invalid_manifest_is_row_failure_not_batch_verdict(scratch_dir: Path) ->
     assert row["helper_state"] == "not_invoked"
     assert row["packet_conformance"]["conforms_to_current_schema"] is False
     assert row["packet_conformance"]["declared_manifest_version"] is None
-    assert any("non-current schema version" in item for item in row["visible_stops"])
+    assert any("does not declare a string manifest_version" in item for item in row["visible_stops"])
     assert census["census"]["packet_state_counts"]["manifest_nonconforming"] == 1
 
 
```

## Non-Findings Checked

- Distinct-type guard: nonconforming `inspect_packet_manifest` returns `PacketConformanceReport` with `packet=None` at `packet_inspection.py:101-109`; tests pin that at `test_packet_inspection.py:109-117`.
- Catch scope in reader: `inspect_packet_manifest` catches only `ValidationError` at `packet_inspection.py:99-101`; `test_packet_inspection.py:136-148` pins non-`ValidationError` propagation for the reader.
- Write-once/read-only guard: `read_packet_leniently` reads JSON and returns an inspection report at `packet_inspection.py:121-132`; `test_packet_inspection.py:159-173` snapshots all packet files before/after and confirms no mutation.
- Census nonconforming vs uninspectable split: `source_quality.py:529-549` uses `read_packet_leniently` before strict skeleton build and assigns parseable schema failures to `manifest_nonconforming`; invalid JSON is still `manifest_uninspectable` via `source_quality.py:531-538` and `test_source_quality_state_assembler.py:116-137`.
- Direct skeleton remains strict: `build_source_quality_report_skeleton` still calls `SourceCapturePacket.model_validate(...)` directly at `source_quality.py:115`; leniency is introduced only in the census pre-check at `source_quality.py:529-549`.
- Double-validate: conforming census rows run the lenient probe first, then the existing strict skeleton at `source_quality.py:551-559`. No correctness issue found in the commissioned slice; cost is a known small duplicate validation for conforming rows.

## Verdict

```yaml
recommendation: patch_proposed
strict_pass_claim: not_made
readiness_claim: not_made
settled_claim: not_made
```

## Residual Risk

- The proposed diff is not applied and not test-run in patched state because the commission requires a proposed diff only.
- The current tests pass, but DRP-01 shows one current assertion pins misleading wording; the proposed test edit would make that branch fail on the current implementation and pass after the proposed source edit.
- Broader worktree dirtiness and untracked controlling artifacts remain outside this review and block strict PASS/readiness/settled claims.
- Direct skeleton/CLI strictness remains a named deferred boundary, not changed by this proposed patch.

## De-correlation Disclosure

```yaml
author_model_family: Claude
delegate_model_family: OpenAI GPT-5 / Codex
cross_family_bar: met
```

## Review-Use Boundary

This report and proposed diff are decision input for the commissioning home model only. They are not approval, validation, acceptance, ratification, readiness, formal verdict authority, mandatory remediation, or settled status. The home model adjudicates what, if anything, is kept.
