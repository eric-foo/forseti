# Lake Enforcement Substrates Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Orca delegated review-and-patch output (decision input only)
scope: >
  Cross-vendor delegated adversarial code review-and-patch of the
  lake-enforcement-substrates lane: no-new-core-field gate plus full-GT claim
  tripwire.
authority_boundary: retrieval_only
reviewed_by: OpenAI GPT-5 (Codex)
authored_by: Anthropic Claude (Fable 5)
review_use_boundary: >
  Findings are decision input for Chief Architect adjudication and are not
  approval, validation, readiness, mandatory remediation, executor-ready mandate,
  or patch authority.
commission_prompt: docs/prompts/reviews/lake_enforcement_substrates_delegated_adversarial_code_review_patch_commission_prompt_v0.md
branch: claude/lake-enforcement-substrates
base_commit: 2e542c8c
reviewed_head: 19423cc9
status: completed
recommendation: ca_adjudicate_patch_before_keep
```

## Findings

### F-01 - major [claim-checker] Clause-external ballast could silence a real unbounded claim

Evidence: the original classifier accepted `BALLAST_RE.search(line)` at line scope; the patch diff below shows that deleted line and replaces it with a per-claim-segment helper. Without that change, a sentence like `This is not about production. Bronze is full God Tier.` could pass because `not` appeared elsewhere on the same line. Current closure code splits claim-bearing clauses at `.agents/hooks/check_full_gt_claims.py:56` and requires every claim-bearing segment to carry ballast at `.agents/hooks/check_full_gt_claims.py:91`-`.agents/hooks/check_full_gt_claims.py:111`; regression selftests pin the bypass at `.agents/hooks/check_full_gt_claims.py:237`-`.agents/hooks/check_full_gt_claims.py:247`.

minimum_closure_condition: The CA accepts or modifies the [claim-checker] hunk so unrelated ballast no longer clears an unbounded claim, and the selftest plus red probe remain observed.

next_authorized_action: CA adjudication of the supplied hunk; delegate does not commit or widen scope.

### F-02 - major [core-field-gate] The schema gate did not pin nested lake-core shapes

Evidence: the write-boundary authority says deterministic schema/tool enforcement rejects new direct source-family payload fields on `SourceCapturePacket`, `SourceCaptureSlice`, or lake-core manifest/index structures (`orca/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md:115`-`orca/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md:117`). The original test pinned the top-level packet/slice/preserved-file fields, manifest top-level keys, preserved-file entry keys, and top-level Attachment Record entry keys, but not nested direct surfaces such as `VisibleFact`, `PacketTiming`, `MetricObservation`, manifest `source_slices`, Attachment Record `body_ref`, `posture_summary`, or `replay_version_pins`. Current closure pins those constants at `orca-harness/tests/contract/test_data_lake_core_field_gate.py:106`-`orca-harness/tests/contract/test_data_lake_core_field_gate.py:164`, live nested model fields at `orca-harness/tests/contract/test_data_lake_core_field_gate.py:233`-`orca-harness/tests/contract/test_data_lake_core_field_gate.py:243`, manifest nested structures at `orca-harness/tests/contract/test_data_lake_core_field_gate.py:253`-`orca-harness/tests/contract/test_data_lake_core_field_gate.py:300`, and Attachment Record nested structures at `orca-harness/tests/contract/test_data_lake_core_field_gate.py:319`-`orca-harness/tests/contract/test_data_lake_core_field_gate.py:333`.

minimum_closure_condition: The CA accepts or modifies the [core-field-gate] hunk so nested source-capture and Attachment Record schema drift fails the deterministic contract test.

next_authorized_action: CA adjudication of the supplied hunk; delegate does not patch read-only data_lake/source_capture modules.

## Verdicts

Overall verdict: bounded patch supplied for CA adjudication; no `NEEDS_ARCHITECTURE_PASS` was triggered. The original substrates were directionally right but under-enforced two material bypass classes.

Per-surface sub-verdicts:

| Surface | Verdict |
| --- | --- |
| [claim-checker] `.agents/hooks/check_full_gt_claims.py` | Major finding patched in scope. |
| [core-field-gate] `orca-harness/tests/contract/test_data_lake_core_field_gate.py` | Major finding patched in scope. |
| [ci-wiring] `.github/workflows/ci.yml` | No finding. The new step runs at repo root after checkout with `fetch-depth: 0`; `GITHUB_BASE_REF=main` resolves to `origin/main`, matching the checker default. |
| [map-note] `docs/workflows/orca_repo_map_v0.md` | No patch. The Active Hooks note is broad but correctly reports shape-only semantics and owner-gated hook registration. |

## Explicit Non-Findings

- Diff plumbing: no finding on `origin/main...HEAD`, `--diff-filter=ACMR`, `--find-renames`, `--unified=0`, or line-number computation after review. The parser increments only added-line numbers under zero-context hunks, which matches the checker's added-line scope.
- Untracked files: no finding at the CI boundary. `--changed` does not scan untracked files, but PR CI only evaluates committed changes; whole-file and hook modes remain available locally.
- Fail-open branch: no finding for CI as wired. `fetch-depth: 0` plus the checked `origin/main` base avoids the expected infra gap for PR runs; the fail-open path remains loud and is an infra-gap posture, not a silent clean claim.
- Allowlisted prompt/review-output families: no finding. The broad allowlist is a policy choice for claim-owning/record surfaces; the material defect was unrelated ballast outside the claim segment.
- Hook registration: no finding. `.claude/settings.json` does not register `check_full_gt_claims.py --hook`, matching the commission's owner-gated absence.
- Running marker lane interaction: no collision observed. This diff does not touch `orca-harness/data_lake/catalog.py`; the current marker strings remain at `orca-harness/data_lake/catalog.py:37`-`orca-harness/data_lake/catalog.py:41`, and the full-GT tripwire is `.md`-scoped.

## Residual Risks

- forward-only scope: Both substrates are forward-looking gates and do not backfill historical documents or historical sealed packet shapes.
- no retroactive validation: Passing tests/checks does not prove old lake material, old claims, or old review outputs are correct.
- shape-not-truth boundary: The schema gate and claim tripwire enforce deterministic shape and placement, not factual truth of any Bronze claim or packet payload.
- hook registration owner-gated: Local PostToolUse registration for the full-GT hook remains absent by design; CI wiring covers committed PR changes.

## Validation Evidence

- Preflight: `git fetch origin main claude/lake-enforcement-substrates` completed; `HEAD` and `origin/claude/lake-enforcement-substrates` both resolved to `19423cc9`; `origin/main` resolved to `2e542c8c`; initial worktree status was clean.
- Focused core-field gate: `$env:ORCA_DATA_ROOT=$null; python -m pytest -q tests/contract/test_data_lake_core_field_gate.py` completed with `.......... [100%]` after sandbox temp-directory failures required escalation.
- Full harness test: from `orca-harness/` with `ORCA_DATA_ROOT` unset, `python -m pytest` completed with `2553 passed, 7 skipped, 42 warnings in 194.74s (0:03:14)`.
- Full-GT selftest: `python .agents/hooks/check_full_gt_claims.py --selftest` printed `check_full_gt_claims --selftest: OK (11 cases)`.
- Full-GT changed-file gate: `python .agents/hooks/check_full_gt_claims.py --changed --strict` printed `check_full_gt_claims: OK -- no unballasted full-GT claim language in scope`.
- Red probe: a temporary `docs/decisions/full_gt_claim_tripwire_probe_tmp.md` containing `Bronze is full God Tier.` failed strict whole-file mode with `FAIL docs/decisions/full_gt_claim_tripwire_probe_tmp.md:3: unballasted full-GT claim language outside the claim-owning surfaces...`; the probe was deleted and `Test-Path` returned `False`.
- Report provenance: `python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/lake_enforcement_substrates_delegated_adversarial_code_review_v0.md` exited 0 with no output.

## Unified Uncommitted Diff

```diff
diff --git a/.agents/hooks/check_full_gt_claims.py b/.agents/hooks/check_full_gt_claims.py
index be1b5eed..b15f9239 100644
--- a/.agents/hooks/check_full_gt_claims.py
+++ b/.agents/hooks/check_full_gt_claims.py
@@ -10,8 +10,9 @@ WHAT THIS DOES
 
   A flagged line is allowed when ANY of these hold:
     - the file is in the allowlisted claim-owning/record path families below;
-    - the line carries bounding ballast (negation / boundary vocabulary such
-      as "not", "pending", "excluded", "ceiling", "fixture", "claim tier");
+    - every claim-bearing sentence/clause carries bounding ballast (negation /
+      boundary vocabulary such as "not", "pending", "excluded", "ceiling",
+      "fixture", "claim tier");
     - the line carries the deliberate, review-visible ack token
       `full-gt-claim-ack`.
 
@@ -52,6 +53,7 @@ RULE_AUTHORITY = (
 ACK_TOKEN = "full-gt-claim-ack"
 
 CLAIM_RE = re.compile(r"full[\s_-]*god[\s_-]*tier|\bfull[\s_-]*gt\b", re.IGNORECASE)
+CLAUSE_SPLIT_RE = re.compile(r"[.;:!?]")
 BALLAST_RE = re.compile(
     r"\b(?:not|never|no|pending|proposed|excluded|exclusion|exclusions|ceiling|"
     r"fixture|fixtures|residual|residuals|historical|superseded|toward|towards|"
@@ -86,6 +88,15 @@ def is_allowlisted(relposix: str) -> bool:
     return relposix.startswith(ALLOWLIST_PREFIXES)
 
 
+def has_bounding_ballast(line: str) -> bool:
+    if ACK_TOKEN in line:
+        return True
+    claim_segments = [
+        segment for segment in CLAUSE_SPLIT_RE.split(line) if CLAIM_RE.search(segment)
+    ]
+    return bool(claim_segments) and all(BALLAST_RE.search(segment) for segment in claim_segments)
+
+
 def classify_added_line(relposix: str, line: str) -> str | None:
     """Return a finding message for an added line, or None when the line is clean.
 
@@ -97,7 +108,7 @@ def classify_added_line(relposix: str, line: str) -> str | None:
         return None
     if is_allowlisted(relposix):
         return None
-    if BALLAST_RE.search(line):
+    if has_bounding_ballast(line):
         return None
     return (
         "unballasted full-GT claim language outside the claim-owning surfaces. "
@@ -223,6 +234,17 @@ def selftest() -> int:
     check("ballasted line is clean",
           classify_added_line("docs/decisions/some_new_note_v0.md",
                               "Bronze is not full God Tier for production surfaces."), None)
+    check("unrelated ballast sentence still fires",
+          classify_added_line("docs/decisions/some_new_note_v0.md",
+                              "This is not about production. Bronze is full God Tier.") is not None,
+          True)
+    check("one unballasted claim among clauses fires",
+          classify_added_line("docs/decisions/some_new_note_v0.md",
+                              "Bronze is not full God Tier; Silver is full God Tier.") is not None,
+          True)
+    check("same-clause pending ballast is clean",
+          classify_added_line("docs/decisions/some_new_note_v0.md",
+                              "Bronze full GT is pending an owner decision."), None)
     check("claim-tier ballast is clean",
           classify_added_line("docs/decisions/some_new_note_v0.md",
                               "Bronze's full-GT claim tier is owned by the declaration."), None)
@@ -245,7 +267,7 @@ def selftest() -> int:
         for failure in failures:
             print(f"SELFTEST FAIL {failure}")
         return 1
-    print("check_full_gt_claims --selftest: OK (8 cases)")
+    print("check_full_gt_claims --selftest: OK (11 cases)")
     return 0
 
 
diff --git a/orca-harness/tests/contract/test_data_lake_core_field_gate.py b/orca-harness/tests/contract/test_data_lake_core_field_gate.py
index 7bc6e721..237dc2f4 100644
--- a/orca-harness/tests/contract/test_data_lake_core_field_gate.py
+++ b/orca-harness/tests/contract/test_data_lake_core_field_gate.py
@@ -26,9 +26,14 @@ import pytest
 from data_lake.attachment_record_entry import derive_entries_by_key
 from data_lake.root import DataLakeRoot
 from source_capture.models import (
+    CoverageWindow,
+    MetricObservation,
+    PacketTiming,
     PreservedFile,
+    ReceiptMetadata,
     SourceCapturePacket,
     SourceCaptureSlice,
+    VisibleFact,
     known_fact,
 )
 from source_capture.writer import write_local_source_capture_packet
@@ -98,6 +103,65 @@ _PRESERVED_FILE_FIELDS = [
     "size_bytes",
 ]
 
+_VISIBLE_FACT_FIELDS = [
+    "reason",
+    "status",
+    "value",
+]
+
+_PACKET_TIMING_FIELDS = [
+    "archive_snapshot_time",
+    "capture_time",
+    "cutoff_posture",
+    "recapture_time",
+    "source_edit_or_version",
+    "source_publication_or_event",
+]
+
+_METRIC_OBSERVATION_FIELDS = [
+    "coverage_window",
+    "metric",
+    "posture",
+    "reason",
+    "value",
+]
+
+_COVERAGE_WINDOW_FIELDS = [
+    "end",
+    "start",
+]
+
+_RECEIPT_METADATA_FIELDS = [
+    "generated_at",
+    "non_claims",
+    "summary",
+    "title",
+]
+
+_ATTACHMENT_RECORD_BODY_REF_KEYS = [
+    "body_sha256",
+    "file_id",
+    "hash_basis",
+    "kind",
+    "packet_id",
+    "relative_packet_path",
+]
+
+_ATTACHMENT_RECORD_POSTURE_SUMMARY_KEYS = [
+    "access_posture",
+    "archive_history_posture",
+    "media_modality_posture",
+    "re_capture_relationship",
+]
+
+_ATTACHMENT_RECORD_REPLAY_VERSION_PINS_KEYS = [
+    "attachment_record_schema_version",
+    "derivation_rule_version",
+    "entry_serialization_version",
+    "raw_packet_manifest_version",
+    "source_capture_obligation_contract_version",
+]
+
 _ATTACHMENT_RECORD_ENTRY_KEYS = [
     "attachment_record_id",
     "attachment_record_id_basis",
@@ -166,12 +230,76 @@ def test_preserved_file_field_set_is_pinned() -> None:
     )
 
 
+def test_nested_source_capture_model_field_sets_are_pinned() -> None:
+    assert sorted(VisibleFact.model_fields) == _VISIBLE_FACT_FIELDS, _PROMOTION_RULE_MESSAGE
+    assert sorted(PacketTiming.model_fields) == _PACKET_TIMING_FIELDS, _PROMOTION_RULE_MESSAGE
+    assert sorted(MetricObservation.model_fields) == _METRIC_OBSERVATION_FIELDS, (
+        _PROMOTION_RULE_MESSAGE
+    )
+    assert sorted(CoverageWindow.model_fields) == _COVERAGE_WINDOW_FIELDS, (
+        _PROMOTION_RULE_MESSAGE
+    )
+    assert sorted(ReceiptMetadata.model_fields) == _RECEIPT_METADATA_FIELDS, (
+        _PROMOTION_RULE_MESSAGE
+    )
+
+
 def test_manifest_top_level_key_set_is_pinned(fixture_packet) -> None:
     _, result = fixture_packet
     manifest = json.loads(Path(result.manifest_path).read_text(encoding="utf-8"))
     assert sorted(manifest) == _SOURCE_CAPTURE_PACKET_FIELDS, _PROMOTION_RULE_MESSAGE
 
 
+def test_manifest_source_slice_and_receipt_key_sets_are_pinned(fixture_packet) -> None:
+    _, result = fixture_packet
+    manifest = json.loads(Path(result.manifest_path).read_text(encoding="utf-8"))
+    assert sorted(manifest["timing"]) == _PACKET_TIMING_FIELDS, _PROMOTION_RULE_MESSAGE
+    assert sorted(manifest["receipt_metadata"]) == _RECEIPT_METADATA_FIELDS, (
+        _PROMOTION_RULE_MESSAGE
+    )
+    assert manifest["source_slices"], "fixture produced no source slices; pin would be vacuous"
+    for entry in manifest["source_slices"]:
+        assert sorted(entry) == _SOURCE_CAPTURE_SLICE_FIELDS, _PROMOTION_RULE_MESSAGE
+        assert sorted(entry["timing"]) == _PACKET_TIMING_FIELDS, _PROMOTION_RULE_MESSAGE
+
+
+def test_manifest_visible_fact_key_sets_are_pinned(fixture_packet) -> None:
+    _, result = fixture_packet
+    manifest = json.loads(Path(result.manifest_path).read_text(encoding="utf-8"))
+    visible_facts = [
+        manifest["source_locator"],
+        manifest["requested_decision_context"],
+        manifest["capture_context"],
+        manifest["actor_audience_context"],
+        manifest["access_posture"],
+        manifest["archive_history_posture"],
+        manifest["media_modality_posture"],
+        manifest["re_capture_relationship"],
+        manifest["timing"]["source_publication_or_event"],
+        manifest["timing"]["source_edit_or_version"],
+        manifest["timing"]["capture_time"],
+        manifest["timing"]["recapture_time"],
+        manifest["timing"]["cutoff_posture"],
+    ]
+    for entry in manifest["source_slices"]:
+        visible_facts.extend(
+            [
+                entry["locator"],
+                entry["access_posture"],
+                entry["archive_history_posture"],
+                entry["media_modality_posture"],
+                entry["re_capture_relationship"],
+                entry["timing"]["source_publication_or_event"],
+                entry["timing"]["source_edit_or_version"],
+                entry["timing"]["capture_time"],
+                entry["timing"]["recapture_time"],
+                entry["timing"]["cutoff_posture"],
+            ]
+        )
+    for fact in visible_facts:
+        assert sorted(fact) == _VISIBLE_FACT_FIELDS, _PROMOTION_RULE_MESSAGE
+
+
 def test_preserved_files_entry_key_set_is_pinned(fixture_packet) -> None:
     _, result = fixture_packet
     manifest = json.loads(Path(result.manifest_path).read_text(encoding="utf-8"))
@@ -186,3 +314,21 @@ def test_attachment_record_entry_key_set_is_pinned(fixture_packet) -> None:
     assert entries, "fixture packet produced no entries; pin would be vacuous"
     for entry in entries:
         assert sorted(entry) == _ATTACHMENT_RECORD_ENTRY_KEYS, _PROMOTION_RULE_MESSAGE
+
+
+def test_attachment_record_entry_nested_key_sets_are_pinned(fixture_packet) -> None:
+    root, result = fixture_packet
+    entries = derive_entries_by_key(root, result.packet.packet_id)
+    assert entries, "fixture packet produced no entries; pin would be vacuous"
+    for entry in entries:
+        assert sorted(entry["body_ref"]) == _ATTACHMENT_RECORD_BODY_REF_KEYS, (
+            _PROMOTION_RULE_MESSAGE
+        )
+        assert sorted(entry["posture_summary"]) == _ATTACHMENT_RECORD_POSTURE_SUMMARY_KEYS, (
+            _PROMOTION_RULE_MESSAGE
+        )
+        assert sorted(entry["replay_version_pins"]) == _ATTACHMENT_RECORD_REPLAY_VERSION_PINS_KEYS, (
+            _PROMOTION_RULE_MESSAGE
+        )
+        for summary in entry["posture_summary"].values():
+            assert sorted(summary) == _VISIBLE_FACT_FIELDS, _PROMOTION_RULE_MESSAGE
```

## Delegated Return Courier

DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

Include:
- original commission or review target: `docs/prompts/reviews/lake_enforcement_substrates_delegated_adversarial_code_review_patch_commission_prompt_v0.md`
- implementation context, diff, and reviewed files: lane `claude/lake-enforcement-substrates`, base `origin/main` at `2e542c8c`, reviewed head `19423cc9`, patched files listed in the unified diff above
- findings and implementation evidence: F-01 [claim-checker], F-02 [core-field-gate]
- proposed patch, diff, or exact requested edits, if authorized: two uncommitted hunks inside the commissioned patchable set
- citations: embedded in each finding
- reviewer verdict: bounded patch supplied for CA adjudication; no architecture pass triggered
- validation evidence and not-run checks: validation evidence listed above, including report provenance exit 0 with no output after durable write
- residual risk: forward-only scope, no retroactive validation, shape-not-truth boundary, hook registration owner-gated
- blockers, off-scope flags, and not-proven boundaries: no blocker; no patch outside named set; no approval/readiness/validation claim

## Adjudicator Tail

The commissioning Chief Architect should first adjudicate this report's findings, diff, verdict, and residuals as claims. If a remaining material issue is self-closable inside the commissioned scope, close it in the same turn and re-check the state. If a non-self-closable issue remains, route the smallest complete closure step. Once clean enough to move on, collapse admin/lifecycle work into one land step, then name the next 1-5 material moves that need judgment, or state `none` with a one-line reason.

## CA Adjudication (2026-07-03)

- Adjudicator: commissioning Chief Architect (Anthropic Claude, Fable 5 — the substrate author; de-correlation held at review time, reviewed_by above).
- F-01: **ACCEPTED unmodified.** The original line-scope ballast was fail-open exactly as the commission's emphasis 2(a) hypothesized ("This is not about production. Bronze is full God Tier." passed on unrelated "not"). The clause-split closure requires every claim-bearing segment to carry its own ballast; the ack token correctly stays line-scoped per the spec; the three new selftest cases pin the bypass and both boundary directions.
- F-02: **ACCEPTED unmodified.** Nested lake-core shapes were unpinned; the contract's "manifest/index structures" includes them. Verified the nested model pins against the live source read (PacketTiming 6 fields incl. archive_snapshot_time; VisibleFact 3; MetricObservation 5; CoverageWindow 2) and that the replay_version_pins pin correctly binds the CANONICAL entry set (no catalog decoration pin — the A2 decoration-envelope test governs that seam separately).
- Independent verification (not inherited): core-field gate 10 tests exit 0; `--selftest` 11 cases OK; `--changed --strict` clean on the lane's own diff; report provenance `--strict` exit 0; reviewed_head `19423cc9` matches the pushed head. Delegate's full-suite run (2553 passed, 7 skipped) accepted as evidence; CI re-runs it on push.
- Verdict, sub-verdicts, non-findings (incl. the untracked-files CI-boundary posture and fail-open-as-infra-gap posture), and residuals adjudicated as claims and kept: consistent with the commission's claim ceiling.
- This adjudication is a keep-decision on the delegated return only — not approval, validation, readiness, or coverage-completeness.

