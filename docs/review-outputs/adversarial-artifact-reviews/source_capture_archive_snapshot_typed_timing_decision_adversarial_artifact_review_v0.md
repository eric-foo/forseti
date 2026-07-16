```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Adversarial artifact review of the source-capture archive-snapshot typed-timing decision.
use_when:
  - Inspecting findings or the bounded patch for the typed-timing decision.
  - Tracing later timing-decision changes to this review.
authority_boundary: retrieval_only
```

review_summary:
  status: completed_with_bounded_patch
  reviewed_by: gpt-5
  authored_by: anthropic_claude_opus_class_commission_stated
  de_correlation_bar: cross_vendor_discovery
  target: docs/decisions/source_capture_archive_snapshot_typed_timing_decision_v0.md
  counts:
    critical: 0
    major: 2
    minor: 1
  verdict: sound_after_patch
  residual_risk: >
    The producer contract is coherent after patch. Residual risk is old-reader
    forward skew: a prior strict PacketTiming model will reject new manifests
    carrying archive_snapshot_time, including serialized null on non-archive
    packets. That limitation is now recorded; it is not removed by the no-bump
    decision.

# Adversarial Delegated Review-And-Patch Report

## Scope And Preflight

orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom delegated review pack
  edit_permission: patch-only for the target decision record; read-only for code/tests and all other sources
  target_scope: docs/decisions/source_capture_archive_snapshot_typed_timing_decision_v0.md
  dirty_state_checked: yes
  blocked_if_missing: none

De-correlation receipt: author recorded by commission as Anthropic / Claude Opus-class; reviewer/controller is OpenAI / GPT-family. Cross-vendor discovery bar satisfied.

Workspace preflight observed:
- Worktree: `C:\Users\vmon7\Desktop\projects\orca-archive-timing-wt`.
- Branch: `capture-archive-snapshot-timing`.
- Base/main: `f15de9457bb88015d65ea99af8e4312610f98955`.
- Dirty state: five modified code/test files plus one untracked target decision record, matching the commissioned in-scope state before this report was written.
- Target hash before patch: `63B97FB75E6B95DE4FEBC45C828C27769A507045E3D652A8CA8E42619EF138F4`, 262 lines.
- Commission handoff hash: `69E370A3C39D5206030DFBA3E16F06D037C2467F5129608CBA2C9F6936C2EC04`.

SOURCE_CONTEXT_READY. Sources read: target decision record; commissioned handoff; `orca-harness/source_capture/models.py`; `orca-harness/source_capture/writer.py`; `orca-harness/runners/run_source_capture_archive_packet.py`; `orca-harness/tests/unit/test_source_capture_archive_org.py`; `orca-harness/tests/unit/test_source_capture_packet.py`; `docs/product/source_capture_packet_schema_evolution_architecture_v0.md`; Orca overlay authority files named in the commission.

Deep-thinking failure modes framed before findings:
- No-bump rationale could be true for backward read while hiding old-reader forward skew under `extra="forbid"`.
- The record could collapse three timing surfaces by using "packet capture_time" imprecisely after the writer rebuilds packet timing.
- "Archive-mode only / live untouched" could be semantically true while still producing a serialized `null` field on non-archive packets because `PacketTiming` is shared.
- Validation could be overclaimed if the reproduced test set does not match the stated blast radius.

## Findings

### AR-01 - major - No-bump rationale hid old-reader forward skew

Phase: correctness.

Target and purpose: `docs/decisions/source_capture_archive_snapshot_typed_timing_decision_v0.md`, schema-version/no-bump decision for the typed archive snapshot-time producer seam.

Evidence:
- The target originally described the field as additive optional and non-breaking, citing existing-manifest backward read under `StrictModel(extra="forbid")` at target lines 84-105 before patch.
- `PacketTiming` is a strict model with `archive_snapshot_time: VisibleFact | None = None` added at `orca-harness/source_capture/models.py:82-96`.
- The schema-evolution architecture attacks every-read strict failures under `extra="forbid"` and keeps strict validation at write plus lenient inspection read (`docs/product/source_capture_packet_schema_evolution_architecture_v0.md:174-200`).

Strongest defense: The target's no-bump decision is sound under the adopted backward-read/current-reader rule: existing manifests omit the key and still validate, and a version bump would mislabel an optional add as a second breaking v1->v2 bump.

Why the defense was incomplete: With `extra="forbid"`, an old reader whose model predates `archive_snapshot_time` will reject a new manifest that carries the extra key. This is especially visible because non-archive packets may serialize the new key as `null`. The no-bump decision can still stand, but only if the record stops calling the change "non-breaking" without the forward-skew boundary.

Patch applied: Added an explicit forward-skew limitation to the no-bump section and adjusted the direction-change receipt to say backward-read/current-reader compatible, not universally non-breaking.

Minimum closure condition: The record must distinguish backward-read/current-reader compatibility from old-reader forward compatibility and preserve the no-bump justification without claiming old strict readers can read new manifests.

Next authorized action: CA adjudication of the bounded wording patch.

### AR-02 - major - Evidence chain conflated runner/slice timing with final packet timing

Phase: correctness.

Target and purpose: `docs/decisions/source_capture_archive_snapshot_typed_timing_decision_v0.md`, evidence chain supporting the two-date timing contract.

Evidence:
- The target already states that final packet-level `capture_time` is packet write time while slice-level `capture_time` is archive fetch time (`docs/decisions/source_capture_archive_snapshot_typed_timing_decision_v0.md:72-75` before patch).
- The runner creates intermediate `packet_timing.capture_time` from availability metadata and threads `archive_snapshot_time` through to the writer (`orca-harness/runners/run_source_capture_archive_packet.py:116-127`, `:199-207`).
- The writer rebuilds packet-level timing from `captured_at`, including `capture_time=known_fact(captured_at)` (`orca-harness/source_capture/writer.py:91-102`, `:134-149`).
- Archive body and availability slice timing use the archive fetch metadata (`orca-harness/runners/run_source_capture_archive_packet.py:346-370`).

Strongest defense: The record's main semantics section was correct and the implementation keeps `archive_snapshot_time` distinct from both packet write time and archive fetch time.

Why the defense failed: The evidence section's phrase "packet `capture_time = known_fact(str(metadata[...]))`" was false for the final packet manifest and contradicted the record's own earlier statement. It could mislead a consumer into thinking packet-level `capture_time` was still the availability fetch timestamp.

Patch applied: Rewrote the evidence bullets to distinguish runner intermediate timing, archive slice `capture_time`, final packet-level writer timing, and fetch wall-clock metadata.

Minimum closure condition: The record's evidence chain must match the actual writer thread-through: final packet-level timing is writer-owned; archive slice timing is runner/fetch-owned.

Next authorized action: CA adjudication of the bounded wording patch.

### AR-03 - minor - "Other runners untouched" under-described the serialized null footprint

Phase: correctness.

Target and purpose: `docs/decisions/source_capture_archive_snapshot_typed_timing_decision_v0.md`, constraint and residual-risk clarity for non-archive packets.

Evidence:
- `archive_snapshot_time` lives on shared `PacketTiming`, not on an archive-only subtype (`orca-harness/source_capture/models.py:82-96`).
- `write_local_source_capture_packet` always constructs `PacketTiming` and passes the optional field through, defaulting to `None` when not supplied (`orca-harness/source_capture/writer.py:91-102`).
- The target already acknowledged that non-archive manifests gain `"archive_snapshot_time": null`, but still described other runners as "untouched" (`docs/decisions/source_capture_archive_snapshot_typed_timing_decision_v0.md:177-182` before patch).

Strongest defense: Semantically, non-archive timing is untouched; their `capture_time` remains the observation/fetch time and the new field is `None`.

Why the defense needed wording: A serialized `null` key is still a manifest shape footprint. The record should not rely on "untouched" without naming the shape effect.

Patch applied: Reworded the constraint to say archive/history producers populate a `VisibleFact`, non-archive runners leave `None`, and the serialized null is a deliberate shape footprint rather than a timing-semantics change.

Minimum closure condition: The record must state both the semantic boundary and the manifest-shape footprint.

Next authorized action: CA adjudication of the bounded wording patch.

## Unified Diff - Decision Record Only

```diff
--- a/docs/decisions/source_capture_archive_snapshot_typed_timing_decision_v0.md
+++ b/docs/decisions/source_capture_archive_snapshot_typed_timing_decision_v0.md
@@
 - **The consumer keys on field presence, not version** (handoff §3 #7: "prefer
   typed → else blessed legacy derivation → else typed dating-gap").
 - Bumping would **mislabel** a non-breaking change as a version break, flip all
   existing v1 packets to `declares_current_manifest_version = False`
   (`packet_inspection.py:91`), and trip that architecture doc's own
   `stale_if` ("a second breaking bump v1 → v2").
+- **Forward-skew limit acknowledged:** an older reader whose `PacketTiming`
+  model predates this field and still uses `extra="forbid"` will reject a new
+  manifest carrying `archive_snapshot_time` (including a serialized `null` on a
+  non-archive packet). The no-bump decision is therefore a backward-read /
+  current-reader compatibility decision, not a guarantee that old code can read
+  new manifests. A version bump would not make that older strict reader accept
+  the extra key; it would only label this additive field as a breaking v2
+  contrary to the adopted bump-on-breaking-change rule.
@@
-- packet `capture_time = known_fact(str(metadata["capture_timestamp"]))` — runner `:114-124`; `_body_timing` `:310-321`.
-- `capture_timestamp = utc_now_z()` (fetch wall-clock) — `direct_http.py:164`, `anti_blocking_http.py:216`.
+- archive runner intermediate timing and archive slice `capture_time` use
+  `known_fact(str(metadata["capture_timestamp"]))` — runner `:116-127`;
+  `_body_timing` `:346-358`; `_availability_timing` `:361-370`.
+- final packet-level `capture_time` is rebuilt by `writer.py` from
+  `captured_at` (`writer.py:91-102`, `:134-149`), so it is packet write/access
+  timing rather than archive snapshot timing.
+- `capture_timestamp = utc_now_z()` (fetch wall-clock) — `direct_http.py:164`, `anti_blocking_http.py:216`.
@@
-- Archive/history mode only; other runners untouched (field defaults `None`, so their manifests gain only `"archive_snapshot_time": null` — semantically correct, `capture_time` intact).
+- Archive/history producers populate the field as a `VisibleFact`; non-archive
+  runners leave it `None`. Because the field lives on shared `PacketTiming`, new
+  non-archive manifests may serialize `"archive_snapshot_time": null`; that is a
+  deliberate shape footprint, not a timing-semantics change (`capture_time`
+  remains intact).
@@
-    optional with no manifest_version bump (non-breaking under the adopted
-    bump-on-breaking-change rule). It is the published seam downstream archive
+    optional with no manifest_version bump (backward-read/current-reader
+    compatible under the adopted bump-on-breaking-change rule; old strict-reader
+    forward skew remains a recorded limitation). It is the published seam downstream archive
@@
-      reason: additive optional field is non-breaking; bump-on-breaking-change rule => no bump (owner-confirmed).
+      reason: additive optional field is backward-read/current-reader compatible; bump-on-breaking-change rule => no bump (owner-confirmed), with old strict-reader forward skew recorded as a limitation.
```

## Validation

Primary reproduced regression set:

```text
C:\Users\vmon7\Desktop\projects\orca\orca-harness\.venv\Scripts\python.exe -m pytest
  tests\unit\test_source_capture_archive_org.py
  tests\unit\test_source_capture_packet.py
  tests\unit\test_packet_assembly.py
  tests\unit\test_packet_inspection.py
  tests\unit\test_source_capture_direct_http.py
  tests\unit\test_anti_blocking_http_adapter.py
  tests\unit\test_source_capture_browser_snapshot.py
  tests\unit\test_source_capture_authenticated_browser_snapshot.py
  tests\unit\test_source_capture_media_asset.py
  tests\unit\test_source_capture_reddit_api.py
  tests\unit\test_source_capture_reddit_credentials.py
  tests\unit\test_source_quality_state_assembler.py
  tests\contract\test_source_capture_archive_org_contract.py
  tests\contract\test_source_capture_browser_snapshot_contract.py
  tests\contract\test_source_capture_direct_http_contract.py
  tests\contract\test_source_capture_media_asset_contract.py
  tests\contract\test_source_capture_reddit_api_contract.py
  tests\contract\test_source_capture_packet_no_runtime_imports.py
  tests\contract\test_source_quality_report_skeleton_contract.py
  -q
```

Observed result: passed. Follow-up `--collect-only -q` listed per-file counts summing to 150.

Additional context: a broader 164-test run also passed when including `tests\unit\test_source_quality_report_skeleton.py`. The first non-escalated pytest attempt failed only because the sandbox denied creation of `_test_runs` and `.pytest_cache` inside the sibling worktree; the escalated reruns passed.

## CODE-FLAGS

None.

Read-only checks supporting no code flags:
- `capture_time` is not repurposed: final packet-level `capture_time` comes from writer `captured_at`, while archive slice timing uses fetch metadata and `archive_snapshot_time` is separate (`orca-harness/source_capture/writer.py:91-102`; `orca-harness/runners/run_source_capture_archive_packet.py:116-127`, `:346-370`).
- The optional field is present on shared `PacketTiming` and defaults to `None` (`orca-harness/source_capture/models.py:82-96`).
- Archive runner emits known / absent / unparseable cases and tests cover present, absent, unparseable, and legacy omit-read (`orca-harness/tests/unit/test_source_capture_archive_org.py:224-300`; `orca-harness/tests/unit/test_source_capture_packet.py:158-185`).
- `source_observability` does not import or consume `PacketTiming`; the observed direct packet reader is `source_capture/source_quality.py` (`orca-harness/source_observability/checker.py:3-25`; `orca-harness/source_capture/source_quality.py:121`).

## Verdict

`sound_after_patch`. The implementation and tests support the producer seam. The decision record needed wording hardening on compatibility and timing evidence, and the bounded patch corrects those claims without changing the design.

## Residual Risk

Old strict readers that predate `archive_snapshot_time` will reject new manifests carrying the field. This is now a recorded compatibility limitation, not a hidden contradiction in the no-bump decision. The CA should adjudicate whether that limitation is acceptable before keeping the patch.

Review-use boundary: this report, findings, diff, verdict, residual risk, and code-flag absence are decision input only. They are not approval, validation, readiness, mandatory remediation, merge authorization, or executor-ready authority until separately accepted by the commissioning CA.
