# Creator Registry Scan Handoff Enforcement Delegated Adversarial Code Review Patch v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: >
  Delegated adversarial code review and bounded patch return for PR #660's
  Creator Registry scan/capture handoff enforcement work unit
  (`.agents/hooks/check_csb_scanning_artifact.py` and its named docs/tests).
use_when:
  - Adjudicating whether PR #660's Creator Registry preflight receipt
    enforcement is ready to land.
  - Checking what was patched in the bounded target set and what residual
    risk remains after this pass.
authority_boundary: retrieval_only
```

Commissioning prompt: `docs/prompts/reviews/creator_registry_scan_handoff_enforcement_delegated_adversarial_code_review_patch_prompt_v0.md`.

## Start State

- Target workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-registry-receipt-handoffs`.
- Branch at review start: `codex/creator-registry-receipt-handoffs`.
- HEAD SHA at review start: `351cb258b9f42a81a9cae74570c285b6b1fcc43f`.
- Dirty state at review start: clean (`git status --porcelain=v1 --branch` returned only the branch line).
- Diff target used: `origin/main...HEAD`, scoped to the named target-set files plus `.github/workflows/ci.yml` and the read-only baseline sources for adjudication context.
- All 22 named required sources exist (verified by per-file existence check before reading; zero misses).
- `SOURCE_CONTEXT_READY` was declared before findings, recommendations, or patches were produced, per `.agents/workflow-overlay/prompt-orchestration.md` Source-Gated Method Contract. `workflow-deep-thinking` was applied first to frame the failure-mode boundary (self-asserted receipt fields vs. mechanically verifiable shape; runbook-vs-checker contract drift; escape-hatch completeness), then `workflow-code-review` was applied to the diff under `.agents/workflow-overlay/delegated-review-patch.md`'s `delegated_code_review_and_patch` sibling mode.

## Source-Read Ledger

| Source | Read as | Status |
| --- | --- | --- |
| `AGENTS.md` | full | clean |
| `.agents/workflow-overlay/README.md` | full | clean |
| `.agents/workflow-overlay/source-loading.md` | full | clean |
| `.agents/workflow-overlay/review-lanes.md` | full | clean |
| `.agents/workflow-overlay/delegated-review-patch.md` | full | clean |
| `.agents/workflow-overlay/prompt-orchestration.md` | full | clean |
| `.agents/workflow-overlay/validation-gates.md` | full | clean |
| `docs/workflows/creator_registry_record_contract_handoff_v0.md` | full (lane-boundary check only) | clean |
| `orca/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md` | diff + full context | clean |
| `orca-harness/docs/source_capture_agent_runbook.md` | targeted section (report-skeleton block) | clean, then patched |
| `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md` | diff | clean |
| `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md` | diff | clean |
| `.agents/hooks/check_csb_scanning_artifact.py` | full | clean, then patched |
| `.agents/hooks/README.md` | diff | clean |
| `docs/workflows/orca_repo_map_v0.md` | diff | clean |
| `orca-harness/tests/unit/test_csb_scanning_artifact_validator.py` | full | clean, then patched |
| `orca-harness/tests/fixtures/csb_scanning_artifacts/valid_csb_first_scan.md` | diff | clean |
| `orca-harness/tests/fixtures/csb_scanning_artifacts/bad_engagement_overclaim.md` | diff | clean |
| `.github/workflows/ci.yml` | targeted grep (`check_csb_scanning_artifact` wiring) | clean |
| `orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py` | full | clean (read-only baseline) |
| `orca-harness/runners/run_creator_registry_match_preflight.py` | full | clean (read-only baseline) |
| `orca-harness/tests/unit/test_creator_registry_match_preflight.py` | full | clean (read-only baseline) |
| `.agents/hooks/check_review_output_provenance.py` (not in required list; read to shape this report's output correctly) | full | clean |

No source gaps. No modified/untracked controlling source at review start.

## review_summary

```yaml
review_summary:
  status: findings_confirmed_patches_applied_pending_ca_adjudication
  report_path: docs/review-outputs/adversarial-artifact-reviews/creator_registry_scan_handoff_enforcement_delegated_adversarial_code_review_patch_v0.md
  recommendation: ca_adjudicate_then_land
  reviewed_by: claude-sonnet-5
  authored_by: unrecorded
  de_correlation_bar: self_fallback
  same_vendor_rationale: >
    Recorded self_fallback rather than same_vendor_sanity or
    cross_vendor_discovery because the commission did not supply PR #660's
    authoring model/vendor identity (authored_by is unrecorded); neither
    de-correlation bar could be verified. Treat this pass as advisory review
    quality, not a verified no-new-seam discovery pass.
  findings_count: 4
  blocking_findings: 0
  advisory_findings: 1
  next_action: >
    Commissioning Chief Architect adjudicates the three patched findings and
    the one advisory (out-of-scope) finding below, then batches
    commit/push/PR into one land step if the patches are accepted.
```

## Findings

### Finding 1 (major, patched) — runbook told agents to omit the block the checker now requires

- File: `orca-harness/docs/source_capture_agent_runbook.md`.
- Summary: the capture-report template's `required_when` line read `<new social creator/account capture; otherwise omit>`, directly contradicting the commission's own stated rule ("non-social capture requests must carry the explicit `not_applicable` boundary rather than omit the seam") and the checker's actual enforcement, since `creator_registry_match_preflight` is unconditionally in `REQUIRED_CAPTURE_REQUEST_FIELDS`.
- Failure scenario: an agent authoring a non-social capture request follows the runbook's literal instruction and omits the block entirely. The checker then fails the artifact with `missing_capture_request_fields`, or worse, an agent who only skims the runbook never learns the block must carry an explicit `not_applicable` value at all. This is adversarial focus item 7 (docs/checker contract mismatch).
- `minimum_closure_condition`: the runbook's `required_when` line states the block is always required and must read `not_applicable` for non-applicable captures, never omitted.
- `next_authorized_action`: patched in this pass (see Patch Summary); CA adjudicates.

### Finding 2 (major, patched) — `not_applicable` escape hatch only checked 2 of 5 preflight fields

- File: `.agents/hooks/check_csb_scanning_artifact.py`.
- Summary: `_validate_creator_registry_match_preflight`'s `not_applicable` branch only inspected `intended_action` (must not equal `new_capture`) and `can_start_new_capture` (must not be boolean `True`). It never inspected `row_decision`, `action_status`, or `receipt_path`.
- Failure scenario: a scan artifact could declare `required_when: not_applicable` (the mechanically "safe" value) while also carrying `row_decision: new_candidate`, `action_status: allowed`, and a real-looking `receipt_path` in the same block — a block that visually mimics a cleared new-capture receipt except for the top-level `required_when` — and the checker passed it with zero findings. This is exactly adversarial focus item 4 ("`required_when: not_applicable` can be used as an escape hatch while still carrying ... metadata"), just wider than the two fields the prior code checked.
- `minimum_closure_condition`: a `not_applicable` block carrying any of `receipt_path` / `intended_action` / `row_decision` / `action_status` / `can_start_new_capture` set to anything other than empty / `not_applicable` / `false` (for `can_start_new_capture`) is flagged `contradictory_creator_registry_match_preflight_not_applicable`.
- `next_authorized_action`: patched in this pass; CA adjudicates.

### Finding 3 (minor, patched) — untested escape-hatch and boolean-parsing branches

- File: `orca-harness/tests/unit/test_csb_scanning_artifact_validator.py`.
- Summary: the only `not_applicable` contradiction test exercised the compound case (`intended_action: new_capture` **and** `can_start_new_capture: true` together). The isolated `can_start_new_capture`-alone path, the `row_decision`/`action_status` escape-hatch path, and a malformed-but-truthy `can_start_new_capture` value (e.g. `1`, which `_as_bool` does not recognize as `True`) were untested. This is adversarial focus item 8 ("tests prove only happy paths and miss the dangerous bypasses").
- Failure scenario: a future edit to the `not_applicable` branch could silently regress any of these three paths with no test failing to catch it.
- `minimum_closure_condition`: dedicated unit tests cover the isolated `can_start_new_capture` path, the `row_decision`/`action_status` escape-hatch path, and a malformed-truthy `can_start_new_capture` value.
- `next_authorized_action`: patched in this pass (3 new tests added); CA adjudicates.

### Finding 4 (advisory, out of scope, not patched) — `row_decision` vs. the runner's actual `decision` field name

- Files: `orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py` (read-only baseline; the actual preflight receipt result key is `decision`, per `_build_candidate_result`) and `orca-harness/docs/source_capture_agent_runbook.md` / `.agents/hooks/check_csb_scanning_artifact.py` (which both use `row_decision`).
- Summary: the scan-handoff vocabulary (`row_decision`) does not match the field name the real preflight runner emits (`decision`). This mismatch predates PR #660 — the `row_decision` line in the runbook diff is unchanged context, not a new addition — and PR #660 neither introduced nor touched it.
- Failure scenario: an agent transcribing a real preflight receipt into the scan handoff must remember to rename the receipt's `decision` key to `row_decision`; this is a documentation-consistency risk, not a checker defect, since the checker only validates the scan handoff's own declared vocabulary and has no visibility into the receipt JSON's key names.
- `minimum_closure_condition`: `row_decision` and `decision` are reconciled to one name across the runner, runbook, and checker, or the naming difference is explicitly documented as intentional.
- `next_authorized_action`: CA decision or separate lane. Renaming touches `registry_match_preflight.py` and `run_creator_registry_match_preflight.py`, both outside this commission's Bounded Patch Scope; touching them here would silently widen the named target set, which the sibling-mode convention forbids without a re-commission.

## Patch Summary

Three files patched, all inside the commissioned Bounded Patch Scope:

- `.agents/hooks/check_csb_scanning_artifact.py` — widened the `not_applicable` escape-hatch check (Finding 2).
- `orca-harness/docs/source_capture_agent_runbook.md` — corrected the stale "otherwise omit" template line (Finding 1).
- `orca-harness/tests/unit/test_csb_scanning_artifact_validator.py` — added 3 tests closing the coverage gap (Finding 3).

Unified diff (`git diff` against the pre-patch tree):

```diff
diff --git a/.agents/hooks/check_csb_scanning_artifact.py b/.agents/hooks/check_csb_scanning_artifact.py
index 540b6028..67867d4f 100644
--- a/.agents/hooks/check_csb_scanning_artifact.py
+++ b/.agents/hooks/check_csb_scanning_artifact.py
@@ -127,6 +127,7 @@ REQUIRED_CREATOR_REGISTRY_PREFLIGHT_FIELDS = {
     "can_start_new_capture",
 }
 VALID_CREATOR_REGISTRY_REQUIRED_WHEN = {"new_social_creator_account_capture", "not_applicable"}
+NOT_APPLICABLE_ALLOWED_PREFLIGHT_VOCAB = {"", "not_applicable"}
 VALID_CREATOR_REGISTRY_INTENDED_ACTIONS = {"new_capture", "classify", "update_existing", "not_applicable"}
 VALID_CREATOR_REGISTRY_ROW_DECISIONS = {"existing_match", "new_candidate", "ambiguous_match", "invalid_candidate", "not_applicable"}
 VALID_CREATOR_REGISTRY_ACTION_STATUSES = {"allowed", "blocked", "not_applicable"}
@@ -604,13 +605,25 @@ def _validate_creator_registry_match_preflight(request_id: Any, request: dict[st
         return findings

     if required_when == "not_applicable":
-        if _normalize_vocab(preflight.get("intended_action")) == "new_capture" or _as_bool(
-            preflight.get("can_start_new_capture")
-        ) is True:
+        disallowed = [
+            field
+            for field in ("intended_action", "row_decision", "action_status")
+            if _normalize_vocab(preflight.get(field)) not in NOT_APPLICABLE_ALLOWED_PREFLIGHT_VOCAB
+        ]
+        if "receipt_path" in preflight and _normalize_vocab(
+            preflight.get("receipt_path")
+        ) not in PLACEHOLDER_PREFLIGHT_RECEIPT_VALUES:
+            disallowed.append("receipt_path")
+        can_start = preflight.get("can_start_new_capture")
+        if _as_bool(can_start) is True or _normalize_vocab(can_start) not in (
+            NOT_APPLICABLE_ALLOWED_PREFLIGHT_VOCAB | {"false"}
+        ):
+            disallowed.append("can_start_new_capture")
+        if disallowed:
             findings.append(
                 Finding(
                     "contradictory_creator_registry_match_preflight_not_applicable",
-                    f"Capture request {request_id} creator_registry_match_preflight cannot be not_applicable while carrying new_capture clearance.",
+                    f"Capture request {request_id} creator_registry_match_preflight is not_applicable but also carries: {', '.join(disallowed)}.",
                 )
             )
         return findings
diff --git a/orca-harness/docs/source_capture_agent_runbook.md b/orca-harness/docs/source_capture_agent_runbook.md
index 288c8977..d35adb6f 100644
--- a/orca-harness/docs/source_capture_agent_runbook.md
+++ b/orca-harness/docs/source_capture_agent_runbook.md
@@ -683,7 +683,7 @@ source_capture_agent_report:
   authenticated_browser_caveat: <if authenticated browser packet, session mode/state label reported but no state contents or login-wall absence proof; otherwise none>
   visible_stop_if_any: <missing input, access failure, browser-needed, no packet, or none>
   creator_registry_match_preflight:
-    required_when: <new social creator/account capture; otherwise omit>
+    required_when: <new_social_creator_account_capture if this capture request is a new social creator/account capture, otherwise not_applicable; never omit this block>
     receipt_path: <path to preflight receipt JSON>
     intended_action: <new_capture|classify|update_existing>
     row_decision: <existing_match|new_candidate|ambiguous_match|invalid_candidate>
diff --git a/orca-harness/tests/unit/test_csb_scanning_artifact_validator.py b/orca-harness/tests/unit/test_csb_scanning_artifact_validator.py
index ca4b4d62..b152c222 100644
--- a/orca-harness/tests/unit/test_csb_scanning_artifact_validator.py
+++ b/orca-harness/tests/unit/test_csb_scanning_artifact_validator.py
@@ -407,6 +407,41 @@ def test_not_applicable_creator_registry_preflight_rejects_new_capture_clearance
     assert "contradictory_creator_registry_match_preflight_not_applicable" in _codes(text)


+def test_not_applicable_creator_registry_preflight_rejects_can_start_alone() -> None:
+    text = _replace_creator_registry_preflight(
+        _valid_text(),
+        "creator_registry_match_preflight:\n"
+        "  required_when: not_applicable\n"
+        "  intended_action: classify\n"
+        "  can_start_new_capture: true\n",
+    )
+
+    assert "contradictory_creator_registry_match_preflight_not_applicable" in _codes(text)
+
+
+def test_not_applicable_creator_registry_preflight_rejects_clearance_shaped_row_fields() -> None:
+    text = _replace_creator_registry_preflight(
+        _valid_text(),
+        "creator_registry_match_preflight:\n"
+        "  required_when: not_applicable\n"
+        "  row_decision: new_candidate\n"
+        "  action_status: allowed\n",
+    )
+
+    assert "contradictory_creator_registry_match_preflight_not_applicable" in _codes(text)
+
+
+def test_not_applicable_creator_registry_preflight_rejects_malformed_truthy_can_start() -> None:
+    text = _replace_creator_registry_preflight(
+        _valid_text(),
+        "creator_registry_match_preflight:\n"
+        "  required_when: not_applicable\n"
+        "  can_start_new_capture: 1\n",
+    )
+
+    assert "contradictory_creator_registry_match_preflight_not_applicable" in _codes(text)
+
+
 def test_new_social_creator_capture_preflight_can_clear_capture_request() -> None:
     text = _replace_creator_registry_preflight(
         _valid_text(),
```

## Validation Evidence

All commands run from `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-registry-receipt-handoffs` after the patches above were applied. All observed results below are actual command output, not projected or future-tense.

| Command | Observed result |
| --- | --- |
| `python -m py_compile .agents\hooks\check_csb_scanning_artifact.py` | PASS — exit 0, no output (run under a 30s smoke-timeout first per the validation-probe rule, then unbounded). |
| `python -m pytest -q orca-harness\tests\unit\test_csb_scanning_artifact_validator.py` | PASS — 88 passed (75 pre-existing + 13 creator-registry-preflight tests, of which 3 are new in this pass). |
| `python .agents\hooks\check_csb_scanning_artifact.py --selftest` | PASS — `SELFTEST OK` (3 fixtures: `bad_engagement_overclaim.md` expected-fail confirmed, `bad_missing_broad_scout.md` expected-fail confirmed, `valid_csb_first_scan.md` expected-pass confirmed). |
| `python .agents\hooks\check_csb_scanning_artifact.py --diff origin/main --strict` | PASS — `no changed CSB-first scan artifacts detected` (exit 0; correct, since no `docs/research/` scan artifact changed in this diff — only the checker/docs/tests/fixtures under `orca-harness/`/`.agents/hooks/`). |
| `python .agents\hooks\check_retrieval_header.py --changed --strict` | PASS — exit 0, no findings. |
| `python .agents\hooks\header_index.py --strict --base origin/main` | PASS — "2 changed durable .md file(s) all have headers and are map-reachable". |
| `python .agents\hooks\check_handoff_pointers.py --strict --base origin/main` | PASS — "0 findings in 9 changed file(s) vs origin/main". |
| `python .agents\hooks\check_dcp_receipt.py --strict --base origin/main` | PASS — "every real receipt in the changed .md files is shape-valid". |
| `python .agents\hooks\check_review_routing.py --strict --base origin/main` | PASS — disposition satisfied by this review artifact itself, filed under `docs/prompts/reviews/` in the same change. |
| `python .agents\hooks\check_map_links.py --strict` | PASS — "0 findings" (33 pre-existing annotated-nonresolving entries are backlog debt, not failures). |
| `python .agents\hooks\check_full_gt_claims.py --changed --strict` | PASS — "no unballasted full-GT claim language in scope". |
| `git diff --check` | PASS — exit 0, no whitespace/conflict-marker issues. |

None of the twelve required gates were skipped or returned `not_run`.

## Residual Risks And Non-Claims

- This review confirms **shape/receipt-field enforcement only**. It does not, and structurally cannot, verify that a cited `receipt_path` corresponds to a real, on-disk preflight receipt, or that the receipt's actual content matches the scan handoff's declared `intended_action` / `row_decision` / `action_status` / `can_start_new_capture` values. `git ls-files | grep -i creator_registry_match_preflight_receipt` returned no results anywhere in the repository, confirming these receipts are ephemeral, agent-local, uncommitted artifacts by design; a mechanical existence/content check inside the checker would produce false-positive CI failures against the intended workflow. This residual matches the checker's own declared non-claim ("never scan quality, buyer proof, registry truth, or Capture route authorization") — it is a permanent, named boundary, not a defect this pass closes.
- Finding 4 (`row_decision` vs. the runner's `decision` field name) is unresolved and named, not silently dropped; closing it requires touching files outside this commission's Bounded Patch Scope.
- `de_correlation_bar: self_fallback` — the commission did not supply PR #660's authoring vendor/model identity, so this pass cannot claim the cross-vendor no-new-seam discovery bar or the same-vendor sanity tier; treat it as advisory review quality only.
- No capture, registry-identity-ledger, or external-data-lake actions were taken. All applied changes are documentation, checker, and test edits inside the named Bounded Patch Scope.
- `NEEDS_ARCHITECTURE_PASS` was **not** returned: none of the findings required a capture-runner schema change, identity-resolver redesign, fuzzy matching, route-binding authority, registry schema change, external data-lake work, live capture, or CI architecture change outside the named target set.

review_use_boundary: The findings, diff, and verdict in this report are decision input only. They are not approval, not validation, not mandatory remediation, and not executor-ready patch authority until the commissioning Chief Architect adjudicates and separately authorizes them.

## CA Adjudication Addendum

```yaml
adjudication_closeout:
  status: clean
  accepted_findings:
    - finding_1_runbook_omit_instruction
    - finding_2_not_applicable_escape_hatch
    - finding_3_escape_hatch_test_coverage
  modified_findings:
    - finding_4_row_decision_vs_decision_field_name
  rejected_findings: []
  accepted_patch_summary:
    - Kept the delegate's runbook fix that makes the preflight block never-omit and explicit `not_applicable` for non-applicable captures.
    - Kept the delegate's stricter `not_applicable` contradiction check and added tests.
    - Modified Finding 4 from advisory/defer to same-PR CA patch: aligned the scan handoff/checker/test vocabulary to the runner's real receipt field name `decision`, without changing the runner.
  vetoed_patch_summary: []
  residuals:
    - The checker still verifies only scan-handoff shape and self-consistency; it does not verify ephemeral receipt file existence or receipt contents.
    - The delegated pass recorded `de_correlation_bar: self_fallback`; this remains advisory review quality, not a cross-vendor no-new-seam claim.
  review_output_integrity_check: "python .agents\\hooks\\check_review_output_provenance.py --strict docs\\review-outputs\\adversarial-artifact-reviews\\creator_registry_scan_handoff_enforcement_delegated_adversarial_code_review_patch_v0.md - PASS, exit 0"
  admin_land_step: "Commit and push the accepted delegate patches, CA field-name patch, and review report to PR #660."
  next_material_steps:
    - step: "Run the delegated prompt if another reviewer is desired after the CA patch."
      why_it_compounds: "The prompt now exists in PR #660 and targets this exact enforcement surface."
      main_risk: "A second pass may produce small wording churn rather than material defects."
  next_action: "land accepted same-PR patch after validation"
  non_claims:
    - not validation
    - not readiness
    - not runtime model routing
```

CA validation after the final CA patch:

| Command | Observed result |
| --- | --- |
| `python -m py_compile .agents\hooks\check_csb_scanning_artifact.py` | PASS - exit 0, no output. |
| `python -m pytest -q orca-harness\tests\unit\test_csb_scanning_artifact_validator.py` | PASS - exit 0, progress reached 100%. |
| `python .agents\hooks\check_csb_scanning_artifact.py --selftest` | PASS - `SELFTEST OK`. |
| `git diff --check` | PASS - exit 0, no output. |
| `rg -n "row_decision" .agents\hooks\check_csb_scanning_artifact.py orca-harness\docs\source_capture_agent_runbook.md orca\product\spines\scanning\scan_core\orca_scanning_intelligent_walk_mgt_operating_model_v0.md orca-harness\tests\unit\test_csb_scanning_artifact_validator.py orca\product\spines\capture\core\source_families\social_media\creator_registry\creator_registry_match_preflight_usage_v0.md` | PASS - no matches in the checked live handoff/checker/test/usage surfaces. |

CA review-use boundary: this addendum records adjudication and accepted patches for PR #660 only. It is not approval, not validation beyond the observed commands above, not product readiness, and not runtime model routing.