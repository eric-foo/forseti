# CSB Scanning Artifact Checker Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review prompt
scope: >
  De-correlated adversarial code review prompt for the CSB-first scanning
  artifact checker change packet on branch codex/csb-scanning-artifact-checker.
use_when:
  - Commissioning an independent review of PR #364 / commit b63f7b41.
  - Checking whether the new checker reduces LLM memory burden without creating
    false-pass, overreach, or doctrine-leakage risk.
authority_boundary: retrieval_only
```

## Orca Prompt Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_review_packet
  edit_permission: read-only
  target_scope: >
    Review only the CSB-first scanning artifact checker change packet. Do not
    patch source files in this review lane.
  dirty_state_checked: yes
  blocked_if_missing: >
    If the worktree, branch, target commit, or target files cannot be confirmed,
    return SOURCE_CONTEXT_INCOMPLETE instead of reviewing a substitute checkout.

prompt_mode:
  output_mode: review-report
  prompt_artifact_path: docs/prompts/reviews/csb_scanning_artifact_checker_adversarial_code_review_prompt_v0.md
  report_destination: docs/review-outputs/csb_scanning_artifact_checker_adversarial_code_review_v0.md
  template_kind: review
  repo_map_decision: not_needed
  repo_map_reason: target paths and validation commands are named directly

workspace_preflight:
  workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\scanning-broad-scout-recency-default
  expected_branch: codex/csb-scanning-artifact-checker
  expected_target_head: b63f7b41aa053a8dd09a76adc70f8e6849c11a61
  dirty_state_allowance: >
    The prompt file itself and the review report may be present as local
    additions. The target implementation/docs files under review must match the
    expected target head unless the CA explicitly redirects.
  untracked_scope: prompt/report artifacts only

route_from_delegated_review_patch:
  status: routed_to_code_review
  reason: >
    Orca's delegated-review-patch convention is provisional and does not stretch
    to a multi-file implementation/code diff. This commission therefore requests
    de-correlated adversarial code review, not patch execution.
  de_correlation_who_constraint: >
    The receiving reviewer should be a different vendor/model family than the
    author/home model when the operator can provide that. This is a
    who-constraint, not a runtime model recommendation.
  authored_by: openai-gpt-5-codex
  reviewed_by: operator_to_fill
  de_correlation_bar: operator_to_fill
```

## Fitness Reference

Goal: reduce LLM memory burden in future CSB-first scanning runs by enforcing the receipt shape that operators otherwise have to remember.

Done looks like: the checker catches missing broad-scout, CSB-row, exact-query, cap, closeout, overclaim, and Capture-route-binding mistakes, while explicitly not grading signal quality, proving demand, validating candidates, or binding Capture work.

Treat this as an axis to attack, not a pass-if-matches bar.

## Source-Gated Method Contract

1. REFERENCE-LOAD the required method instructions first. Do not APPLY them yet.
2. SOURCE-LOAD the authority and target files below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. Only after source readiness, APPLY `workflow-deep-thinking`, then APPLY `workflow-code-review`.
5. For the docs in the mixed change packet, also apply a bounded artifact/doctrine leakage check. If `workflow-adversarial-artifact-review` is available, REFERENCE-LOAD it before source loading and APPLY it after `SOURCE_CONTEXT_READY`; if unavailable, name that gap and continue the code review without issuing strict artifact-review claims.

Required method instructions:

- `workflow-deep-thinking`
- `workflow-code-review`
- `workflow-adversarial-artifact-review` for the bounded doc/doctrine leakage check, if available

Required authority reads:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/delegated-review-patch.md`

Required target reads:

- `.agents/hooks/check_csb_scanning_artifact.py`
- `orca-harness/tests/unit/test_csb_scanning_artifact_validator.py`
- `orca-harness/tests/fixtures/csb_scanning_artifacts/valid_csb_first_scan.md`
- `orca-harness/tests/fixtures/csb_scanning_artifacts/bad_missing_broad_scout.md`
- `orca/product/spines/scanning/README.md`
- `docs/workflows/orca_repo_map_v0.md`

Adjacent comparison reads:

- `.agents/hooks/check_commission_signal_board_output.py`
- `orca-harness/tests/unit/test_commission_signal_board_output_validator.py`
- `orca/product/spines/scanning/scan_core/orca_scanning_intelligent_walk_mgt_operating_model_v0.md`

Git context to inspect:

- `git status --short --branch`
- `git rev-parse HEAD`
- `git show --stat --oneline b63f7b41aa053a8dd09a76adc70f8e6849c11a61`
- `git show --patch --no-ext-diff --unified=80 b63f7b41aa053a8dd09a76adc70f8e6849c11a61`

## Review Scope

Findings-first. Prioritize bugs, false passes, overbroad failures, missing tests, drift from scanning doctrine, and misleading docs. Do not praise the patch before listing findings.

Review questions:

- Does the checker enforce the minimum CSB-first scanning receipt shape it claims to enforce?
- Can an artifact omit broad scout accounting, CSB row consumption, exact-query discovery, venue evaluation, hidden venue pointers, observations, negatives/access notes, capture requests, candidate decision, or closeout and still pass?
- Are run caps mandatory and actually compared against `screening_moves_used` and `exact_queries_used`?
- Are closeout states restricted to the intended set: `candidate_ready_for_next_lane`, `capture_preservation_only`, and `no_candidate_after_discovery`?
- Does the checker detect obvious recency/currentness proof leakage and Capture route-binding leakage without flagging allowed non-proof boundary language?
- Does the checker stay receipt-shape-only, avoiding candidate validation, demand-proof grading, Capture authorization, crawler/runtime behavior, or source-class ratification?
- Are fixtures realistic enough to catch regressions, or are tests only confirming the implementation's current string choices?
- Are there mutation gaps around YAML parsing, missing fenced YAML, malformed caps, section aliases, invalid overclaim fields, and route-binding values?
- Does the scanning README describe the checker as a manual receipt-shape gate rather than validation, readiness, proof, or automatic hook wiring?
- Does the repo map accurately classify the checker without overstating automation or CI wiring?
- Does the implementation avoid fragile path/cwd assumptions when run from the repo root?

Out of scope:

- No live scanning run.
- No crawler, Capture runtime, outreach, source access, registry, atlas, monitor, or candidate minting.
- No broad rewrite of scanning doctrine.
- No patches in this review lane. Recommend concrete fixes, but leave source edits to CA adjudication and a separate patch turn.

## Validation To Run

Run these from the workspace root unless noted. If a command is unavailable, times out, or fails for an environmental reason, record it as not run or blocked with the observed error.

```powershell
python -B .agents\hooks\check_csb_scanning_artifact.py --selftest
```

```powershell
Push-Location orca-harness
python -B -m pytest -q -p no:cacheprovider tests\unit\test_commission_signal_board_output_validator.py tests\unit\test_csb_scanning_artifact_validator.py
Pop-Location
```

```powershell
git diff --check HEAD~1..HEAD
```

```powershell
python .agents\hooks\check_retrieval_header.py --changed
python .agents\hooks\check_repo_map_freshness.py --changed
python .agents\hooks\check_map_links.py --strict
python .agents\hooks\check_placement.py --check
```

Targeted stale/leakage searches:

```powershell
rg -n "recency.*(proof|proves|gate|clear|verdict|score|weight)|currentness.*(proof|proves|gate|clear|verdict|score|weight)|capture.*route.*bind|scan.*bind.*capture|candidate.*validated|checker.*(proof|readiness|validation)" .agents/hooks/check_csb_scanning_artifact.py orca-harness/tests/unit/test_csb_scanning_artifact_validator.py orca/product/spines/scanning/README.md docs/workflows/orca_repo_map_v0.md
```

## Output Contract

Write the durable report to:

`docs/review-outputs/csb_scanning_artifact_checker_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by` and `authored_by` provenance fields. Use `unrecorded` only when the operator/tooling did not provide the value; do not fabricate.
- `de_correlation_bar`: `cross_vendor_discovery`, `same_vendor_sanity`, or `self_fallback`.
- `same_vendor_rationale` when `de_correlation_bar` is `same_vendor_sanity`.
- `source_context_status`: `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
- Findings ordered by severity, with file/line citations.
- For each actionable finding: `minimum_closure_condition` and `next_authorized_action`.
- Validation commands run, exit status, and material output.
- Residual risks and not-assessed gaps.

Return this courier YAML in chat after the report is written:

```yaml
review_summary:
  status: completed | blocked | failed
  report_path: docs/review-outputs/csb_scanning_artifact_checker_adversarial_code_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: operator_to_fill
  authored_by: openai-gpt-5-codex
  de_correlation_bar: operator_to_fill
  summary: "One sentence."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step."
```

Review findings are decision input only. They are not approval, validation, readiness, mandatory remediation, or patch authority until the CA adjudicates them.
