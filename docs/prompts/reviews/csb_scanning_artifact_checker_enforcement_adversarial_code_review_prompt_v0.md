# CSB Scanning Artifact Checker Enforcement Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review prompt
scope: >
  Filed route-out prompt for adversarial implementation/code review of the
  CSB-first scanning artifact checker mechanical-enforcement change packet on
  branch codex/csb-scanning-artifact-checker.
use_when:
  - Commissioning an independent review of PR #364 / commit dbd7a67d.
  - Checking whether the checker reduces LLM memory burden without creating
    false passes, over-enforcement, stale vocabulary, or doctrine leakage.
authority_boundary: retrieval_only
branch_or_commit: codex/csb-scanning-artifact-checker @ dbd7a67d48e11e58445d72ffadb87fe525245fdf
```

## Orca Prompt Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_review_packet
  edit_permission: read-only
  target_scope: >
    Review only the CSB-first scanning artifact checker mechanical-enforcement
    change packet. Do not patch source files in this review lane.
  dirty_state_checked: yes
  blocked_if_missing: >
    If the worktree, branch, target implementation commit, or target files
    cannot be confirmed, return SOURCE_CONTEXT_INCOMPLETE instead of reviewing
    a substitute checkout.

prompt_mode:
  output_mode: file-write review prompt; receiver output mode is review-report
  prompt_artifact_path: docs/prompts/reviews/csb_scanning_artifact_checker_enforcement_adversarial_code_review_prompt_v0.md
  report_destination: docs/review-outputs/csb_scanning_artifact_checker_enforcement_adversarial_code_review_v0.md
  template_kind: review
  repo_map_decision: not_needed
  repo_map_reason: target paths and validation commands are named directly

workspace_preflight:
  workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\scanning-broad-scout-recency-default
  expected_branch: codex/csb-scanning-artifact-checker
  expected_target_implementation_commit: dbd7a67d48e11e58445d72ffadb87fe525245fdf
  expected_base_before_enforcement_commit: c6583dcdab18377c4cb1acea2a8fdcb7e88e5a59
  dirty_state_allowance: >
    The prompt file itself and the review report may be present as local
    additions or later prompt-only commits. The target implementation/docs files
    under review must match the expected target implementation commit unless the
    CA explicitly redirects.
  untracked_scope: prompt/report artifacts only

route_from_delegated_review_patch:
  status: routed_to_code_review
  reason: >
    Orca's delegated-review-patch convention is provisional and should not be
    stretched to a multi-file implementation/code diff. This commission therefore
    requests de-correlated adversarial implementation/code review, not patch
    execution.
  de_correlation_who_constraint: >
    The receiving reviewer should be a different vendor/model family than the
    author/home model when the operator can provide that. This is a
    who-constraint, not a runtime model recommendation, ranking, or selection
    rule. If the reviewer is same-vendor or self-family, record the weaker bar
    rather than claiming cross-vendor discovery.
  author_home_model_family: OpenAI/GPT
  authored_by: openai-gpt-5-codex
  reviewed_by: operator_to_fill
  de_correlation_bar: operator_to_fill
```

## Fitness Reference

Goal: reduce LLM memory burden in future CSB-first scanning runs by making the mechanical receipt obligations machine-checkable instead of relying on the reviewer or runner to remember them.

Done looks like: the checker catches missing or contradictory mechanical receipt shape for CSB anchoring, broad scout, exact queries, observations, candidate records, capture requests, count consistency, closeout consistency, and recency/Capture boundary leaks, while still explicitly not grading signal quality, proving demand, validating candidates, authorizing Capture, or binding source routes.

Treat this as an axis to attack, not a pass-if-matches bar.

## Source-Gated Method Contract

1. REFERENCE-LOAD the required method instructions first. Do not APPLY them yet.
2. SOURCE-LOAD the authority and target files below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. Only after source readiness, APPLY `workflow-deep-thinking`, then APPLY `workflow-code-review`.
5. For the docs in the mixed change packet, also apply a bounded artifact/doctrine leakage check. If `workflow-adversarial-artifact-review` is available, REFERENCE-LOAD it before source loading and APPLY it after `SOURCE_CONTEXT_READY`; if unavailable, name that gap and continue the code review without issuing strict artifact-review claims.

If you have repo/filesystem access, open the named sources directly and re-read the load-bearing sections before making strict or actionable claims. If you do not have repo/filesystem access, stop and request a pasted source capsule or no-repo review bundle; do not review from this prompt text alone.

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
- `orca/product/spines/scanning/scan_core/orca_demand_scan_core_spec_v0.md`
- `orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` targeted only for Capture preservation/route-binding vocabulary if the checker or docs appear to overbind Capture.
- Prior review report: `docs/review-outputs/csb_scanning_artifact_checker_adversarial_code_review_v0.md`.

Git context to inspect:

- `git status --short --branch`
- `git rev-parse HEAD`
- `git show --stat --oneline dbd7a67d48e11e58445d72ffadb87fe525245fdf`
- `git diff --stat c6583dcdab18377c4cb1acea2a8fdcb7e88e5a59..dbd7a67d48e11e58445d72ffadb87fe525245fdf`
- `git diff --patch --no-ext-diff --unified=80 c6583dcdab18377c4cb1acea2a8fdcb7e88e5a59..dbd7a67d48e11e58445d72ffadb87fe525245fdf -- .agents/hooks/check_csb_scanning_artifact.py orca-harness/tests/fixtures/csb_scanning_artifacts/valid_csb_first_scan.md orca-harness/tests/unit/test_csb_scanning_artifact_validator.py orca/product/spines/scanning/README.md docs/workflows/orca_repo_map_v0.md`

If later prompt-only commits exist on the branch, do not treat them as part of the implementation target. Review the implementation delta above unless the CA explicitly redirects.

## Review Scope

Findings-first. Prioritize bugs, false passes, false failures, over-enforcement, missing tests, drift from scanning doctrine, route-binding leakage, stale vocabulary, and misleading docs. Do not praise the patch before listing findings.

Review questions:

- Does the checker enforce the mechanical obligations it now claims to enforce, without pretending to validate truth or quality?
- Can an artifact omit broad-scout detail, CSB row IDs, observation records, candidate records, capture request structure, exact-query accounting, venue/hidden-venue accounting, or closeout consistency and still pass?
- Can a null, blank, malformed, nested, or YAML-date value bypass an intended check?
- Are count checks actually tied to unique IDs in the artifact, or can prose/test scaffolding accidentally satisfy them?
- Does the broad-scout ledger check enforce meaningful route-ledger shape without making one brittle paragraph/token the only way to pass?
- Does the observation schema match scanning vocabulary: `signal_stage`, `gate_role`, uncertainty/limits, and URL-backed/date-backed evidence?
- Does `route_binding_state` match the MGT contract: `cited_current`, `unknown`, `blocked_outside_current_binding`, `not_applicable`?
- Do `not_bound` or `capture_owned` fail where they should, without breaking legitimate `unknown` or `not_applicable` cases?
- Are Capture requests framed as preservation/inspection asks, not Capture authorization, route binding, packet commitment, ECR work, Cleaning work, or Judgment work?
- Does recency/currentness remain an attention-priority signal only, with no proof, scoring, verdict, gate-clearance, or numeric-weight leakage?
- Does the closeout logic prevent contradictory artifacts: candidate-ready with no candidate observation, no-candidate with candidate observations, or capture-preservation-only without capture requests?
- Are tests independent enough to catch regressions, or are they coupled to the valid fixture's exact prose and implementation string choices?
- Are there mutation gaps around invalid enums, section removal, YAML parse failure, URL/date validation, duplicate IDs, nested records, and route-binding values?
- Does the scanning README accurately describe the checker as a manual receipt-shape gate rather than validation, readiness, proof, or automatic hook/CI wiring?
- Does the repo map accurately classify the checker without overstating automation, CI wiring, validation, or readiness?
- Does the implementation avoid fragile cwd/path assumptions when run from the repo root and from `orca-harness` test context?

Out of scope:

- No live scanning run.
- No crawler, Capture runtime, outreach, source access, registry, atlas, monitor, or candidate minting.
- No broad rewrite of scanning doctrine.
- No patch execution in this review lane. Recommend concrete fixes, but leave source edits to CA adjudication and a separately authorized patch turn.

## Validation To Run

Run these from the workspace root unless noted. If a command is unavailable, times out, or fails for an environmental reason, record it as not run or blocked with the observed error.

Because this change materially touches a custom checker, first run a 30-second child-scoped smoke probe for the checker selftest before any repeated/raw validation run. If the smoke probe times out, stop and return `VALIDATION_HOOK_TIMEOUT` with command, cwd, touched files, and observed process state.

```powershell
python -B .agents\hooks\check_csb_scanning_artifact.py --selftest
```

```powershell
Push-Location orca-harness
python -B -m pytest -q -p no:cacheprovider tests\unit\test_commission_signal_board_output_validator.py tests\unit\test_csb_scanning_artifact_validator.py
Pop-Location
```

```powershell
git diff --check c6583dcdab18377c4cb1acea2a8fdcb7e88e5a59..dbd7a67d48e11e58445d72ffadb87fe525245fdf
```

```powershell
python .agents\hooks\check_retrieval_header.py --changed
python .agents\hooks\check_repo_map_freshness.py --changed
python .agents\hooks\check_map_links.py --strict
python .agents\hooks\check_placement.py --check
```

Targeted stale/leakage searches:

```powershell
rg -n "attention and relevance weight|route_binding_state: (not_bound|capture_owned)|checker.*(proof|readiness|validates candidates|buyer proof)|candidate.*validated|recency.*(proof|proves|gate|clear|verdict|score|weight)|currentness.*(proof|proves|gate|clear|verdict|score|weight)|capture.*route.*bind|scan.*bind.*capture" .agents/hooks/check_csb_scanning_artifact.py orca-harness/tests/unit/test_csb_scanning_artifact_validator.py orca-harness/tests/fixtures/csb_scanning_artifacts/valid_csb_first_scan.md orca/product/spines/scanning/README.md docs/workflows/orca_repo_map_v0.md
```

## Output Contract

Write the durable report to:

`docs/review-outputs/csb_scanning_artifact_checker_enforcement_adversarial_code_review_v0.md`

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
  report_path: docs/review-outputs/csb_scanning_artifact_checker_enforcement_adversarial_code_review_v0.md
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