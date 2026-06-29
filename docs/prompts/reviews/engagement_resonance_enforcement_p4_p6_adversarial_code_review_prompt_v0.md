# Engagement Resonance Enforcement P4-P6 Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review prompt
scope: >
  Filed route-out prompt for adversarial implementation/code review of the
  Priority 4 through Priority 6 engagement-resonance enforcement checker batch
  on branch codex/search-surface-mgt-p0-captures-ws.
use_when:
  - Commissioning an independent review of the P4-P6 checker batch after commits 4d62a7b2, 801a07fc, and 64a13b7a.
  - Checking whether the CSB output, scanning artifact, and review-output provenance checkers reduce mechanical LLM burden without creating proof, validation, route-binding, model-ranking, or review-quality claims.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/hygiene/engagement_resonance_enforcement_goal_handoff_v0.md
branch_or_commit: codex/search-surface-mgt-p0-captures-ws @ 64a13b7af04e98e9e3877339bffc7856693211e2
implementation_under_review: eee9aa7b3f42a5baf4e5dfe99495f07ad09a15d5..64a13b7af04e98e9e3877339bffc7856693211e2
prompt_carrier_note: >
  This prompt may be committed after the implementation commits. The implementation
  target under review ends at 64a13b7af04e98e9e3877339bffc7856693211e2; prompt-only
  carrier commits do not change the implementation target unless they modify the
  named target files.
```

## Orca Prompt Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_review_packet
  edit_permission: read-only
  target_scope: >
    Review only the P4-P6 engagement-resonance enforcement checker batch:
    diff range eee9aa7b3f42a5baf4e5dfe99495f07ad09a15d5..64a13b7af04e98e9e3877339bffc7856693211e2
    over the named hook, fixture, test, playbook, and README files. Do not patch
    source files in this review lane.
  dirty_state_checked: yes
  blocked_if_missing: >
    If the worktree, branch, target commits, or target files cannot be confirmed,
    return SOURCE_CONTEXT_INCOMPLETE instead of reviewing a substitute checkout,
    summary, recreated source pack, or broad branch diff.

prompt_mode:
  output_mode: file-write review prompt; receiver output mode is review-report
  prompt_artifact_path: docs/prompts/reviews/engagement_resonance_enforcement_p4_p6_adversarial_code_review_prompt_v0.md
  report_destination: docs/review-outputs/engagement_resonance_enforcement_p4_p6_adversarial_code_review_v0.md
  template_kind: review
  template_source: generic prompt-orchestrator review frame plus Orca overlay bindings; repo-code-review template kind is unbound
  repo_map_decision: not_needed
  repo_map_reason: target commits, files, validation commands, and report destination are named directly

workspace_preflight:
  workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\search-surface-mgt-p0-captures
  expected_branch: codex/search-surface-mgt-p0-captures-ws
  expected_target_head: 64a13b7af04e98e9e3877339bffc7856693211e2
  expected_base_before_batch: eee9aa7b3f42a5baf4e5dfe99495f07ad09a15d5
  target_commit_range: eee9aa7b3f42a5baf4e5dfe99495f07ad09a15d5..64a13b7af04e98e9e3877339bffc7856693211e2
  dirty_state_allowance: >
    The prompt file itself and the review report may be present as local additions
    or later prompt-only commits. The implementation files under review must match
    the expected target head unless the CA explicitly redirects. The pre-existing
    untracked docs/prompts/hygiene-queue/ is not part of the review target.
  untracked_scope: prompt/report artifacts plus pre-existing docs/prompts/hygiene-queue/ only

route_from_delegated_review_patch:
  status: routed_to_code_review
  reason: >
    workflow-delegated-review-patch was invoked, but Orca's delegated-review-patch
    overlay says a multi-file implementation/code diff must not be stretched into
    the single-artifact delegated review-and-patch convention unless separate patch
    execution is explicitly bound. This prompt therefore routes to de-correlated
    adversarial implementation/code review, not patch execution.
  de_correlation_who_constraint: >
    The receiving reviewer should be a different vendor/model family than the
    author/home model when the operator can provide that. This is a who-constraint,
    not a runtime model recommendation, ranking, or selection rule. If the reviewer
    is same-vendor or self-family, record the weaker bar rather than claiming
    cross-vendor discovery.
  author_home_model_family: OpenAI/GPT
  authored_by: openai-gpt-5-codex
  reviewed_by: operator_to_fill
  de_correlation_bar: operator_to_fill
```

## Fitness Reference

Goal: finish the first six engagement-resonance enforcement surfaces so future agents can rely on narrow deterministic checks instead of repeatedly policing the same mechanical public-engagement overclaim, provenance, and hygiene failures by hand.

Done looks like: the P4-P6 checkers catch mechanical CSB output overclaims, scanning artifact overclaims, and review-output provenance/boundary omissions while preserving their limits: no checker decides signal quality, demand, credibility, buyer proof, Capture route choice, final resonance weight, review quality, de-correlation truth, validation, readiness, approval, or acceptance.

Treat this as an axis to attack, not a pass-if-matches bar.

## Source-Gated Method Contract

1. REFERENCE-LOAD the required method instructions first. Do not APPLY them yet.
2. SOURCE-LOAD the authority and target files below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. Only after source readiness, APPLY `workflow-deep-thinking`, then APPLY `workflow-code-review`.
5. For the README/playbook documentation parts of the mixed change packet, also apply a bounded artifact/doctrine leakage check. If `workflow-adversarial-artifact-review` is available, REFERENCE-LOAD it before source loading and APPLY it after `SOURCE_CONTEXT_READY`; if unavailable, name that gap and continue the code review without issuing strict artifact-review claims.

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
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `docs/hygiene/engagement_resonance_enforcement_goal_handoff_v0.md`
- `orca/product/shared/engagement_registry/engagement_logic_registry_v0.md`
- `orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_structure_rules_v0.md`
- `orca/product/spines/scanning/README.md`

Required target reads:

- `.agents/hooks/check_commission_signal_board_output.py`
- `.agents/hooks/check_csb_scanning_artifact.py`
- `.agents/hooks/check_review_output_provenance.py`
- `.agents/hooks/README.md`
- `orca-harness/tests/unit/test_commission_signal_board_output_validator.py`
- `orca-harness/tests/unit/test_csb_scanning_artifact_validator.py`
- `orca-harness/tests/unit/test_review_output_provenance_checker.py`
- `orca-harness/tests/fixtures/commission_signal_board_outputs/bad_engagement_overclaim_output.txt`
- `orca-harness/tests/fixtures/csb_scanning_artifacts/bad_engagement_overclaim.md`
- `orca-harness/tests/fixtures/review_outputs/valid_review_output.md`
- `orca-harness/tests/fixtures/review_outputs/bad_missing_boundary.md`
- `orca-harness/tests/fixtures/review_outputs/bad_missing_header.md`
- `orca-harness/tests/fixtures/review_outputs/bad_missing_provenance.md`
- `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`
- `orca/product/spines/scanning/README.md`

Adjacent comparison reads:

- `.agents/hooks/check_dcp_receipt_hygiene.py`
- `.agents/hooks/check_registry_list_sync.py`
- `.agents/hooks/check_engagement_stale_phrases.py`
- `.agents/hooks/check_retrieval_header.py`
- `docs/prompts/reviews/engagement_resonance_enforcement_p1_p3_adversarial_code_review_prompt_v0.md` for local review-prompt precedent only.

Git context to inspect:

```powershell
git status --short --branch
git rev-parse HEAD
git log --oneline --reverse eee9aa7b3f42a5baf4e5dfe99495f07ad09a15d5..64a13b7af04e98e9e3877339bffc7856693211e2
git diff --stat eee9aa7b3f42a5baf4e5dfe99495f07ad09a15d5..64a13b7af04e98e9e3877339bffc7856693211e2
git diff --name-status eee9aa7b3f42a5baf4e5dfe99495f07ad09a15d5..64a13b7af04e98e9e3877339bffc7856693211e2
```

Review the implementation diff with enough context:

```powershell
git diff --patch --no-ext-diff --unified=80 eee9aa7b3f42a5baf4e5dfe99495f07ad09a15d5..64a13b7af04e98e9e3877339bffc7856693211e2 -- .agents/hooks/check_commission_signal_board_output.py .agents/hooks/check_csb_scanning_artifact.py .agents/hooks/check_review_output_provenance.py .agents/hooks/README.md orca-harness/tests/unit/test_commission_signal_board_output_validator.py orca-harness/tests/unit/test_csb_scanning_artifact_validator.py orca-harness/tests/unit/test_review_output_provenance_checker.py orca-harness/tests/fixtures/commission_signal_board_outputs/bad_engagement_overclaim_output.txt orca-harness/tests/fixtures/csb_scanning_artifacts/bad_engagement_overclaim.md orca-harness/tests/fixtures/review_outputs/valid_review_output.md orca-harness/tests/fixtures/review_outputs/bad_missing_boundary.md orca-harness/tests/fixtures/review_outputs/bad_missing_header.md orca-harness/tests/fixtures/review_outputs/bad_missing_provenance.md orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md orca/product/spines/scanning/README.md
```

If later prompt-only commits exist on the branch, do not treat them as part of the implementation target. Review the checker batch diff above unless the CA explicitly redirects.

## Review Scope

Findings-first. Prioritize bugs, false passes, false failures, brittle regex/parsing, missing selftests, over-enforcement, stale or misleading docs, path/cwd failures, and any wording that turns checker passing into proof, validation, readiness, approval, or acceptance. Do not praise the patch before listing findings.

Review questions:

- Does `check_commission_signal_board_output.py` flag the intended mechanical CSB overclaim classes: engagement as demand proof, graph weight shortcut, Commit/Scale or buyer-proof shortcut, credibility/independence shortcut, Action Ceiling shortcut, and final resonance weight?
- Can the CSB overclaim checker miss a later actual overclaim because an earlier negated sentence overlaps the regex match, or because the nonclaim window is too broad?
- Does the CSB checker avoid false positives on explicit nonclaim boundary text such as `engagement does not prove demand`?
- Does the CSB checker remain row-shape/handoff-shape enforcement only, without adding schema columns, graph scoring, Judgment behavior, or product-proof decisions?
- Does `check_csb_scanning_artifact.py` flag scanning artifacts that treat engagement/resonance as proof, gate clearance, Capture route binding, graph weight, credibility, amplification, Action Ceiling, or final resonance weight?
- Does the scanning checker's negation and overlapping-match handling correctly distinguish a nonclaim sentence from a later overclaim?
- Does the scanning checker preserve the existing broad-scout, exact-query, venue, hidden-venue, observation, negative/access-note, capture-request, closeout, and recency-overclaim validations?
- Does the scanning README change accurately describe the checker as receipt-shape and mechanical overclaim enforcement only, with no venue priority, candidate quality, Capture route, demand, or validation judgment?
- Does `check_review_output_provenance.py` correctly enforce only changed or explicit `docs/review-outputs/**.md` review outputs?
- Does the review-output checker require retrieval-header shape by reusing the retrieval-header predicate, and does it avoid broad header restatement drift?
- Does it require present, nonblank `reviewed_by` and `authored_by` fields while accepting `unrecorded` as a visible provenance gap rather than fabricated identity?
- Does it correctly detect review-use boundaries using both `decision input` language and non-approval/non-validation/non-patch-authority language, including `not` and `no` forms?
- Can the review-output checker falsely pass thin or unrelated nonclaim text, or falsely fail common current review-output boundary wording?
- Does it avoid verifying reviewer identity, deciding de-correlation truth, ranking models, grading review quality, or backfilling historical review outputs?
- Are fixtures and tests strong enough to catch the likely false-pass and false-positive classes, or are they only repeating implementation strings?
- Do all three checkers preserve advisory/default behavior where applicable and strict-mode nonzero behavior for actual findings?
- Are path filters and Git selection modes robust for staged, changed, untracked, explicit, out-of-scope, absolute path, and Git-unavailable cases?
- Does the README/playbook documentation stay discoverable without implying CI promotion, validation, readiness, acceptance, or proof?
- Does the P4-P6 batch avoid runtime/schema infrastructure, crawlers, dashboards, scoring engines, Capture route binding, product-proof gates, or review-lane model routing?

Out of scope:

- No implementation of new P7+ enforcement surfaces.
- No product-doctrine rewrite or engagement/resonance scoring design.
- No CI wiring or mandatory repo-wide gate promotion.
- No runtime implementation, crawler, dashboard, schema migration, or resonance-weight calculation.
- No patch execution in this review lane. Recommend concrete fixes, but leave source edits to CA adjudication and a separate patch turn.

## Validation To Run

Run these from the workspace root unless noted. If a command is unavailable, times out, or fails for an environmental reason, record it as not run or blocked with the observed error.

Because this batch introduces or materially changes custom checkers, first run a 30-second child-scoped smoke probe for each changed checker selftest before any repeated/raw validation run. If a smoke probe times out, stop and return `VALIDATION_HOOK_TIMEOUT` with command, cwd, touched files, and observed process state.

```powershell
python -B .agents\hooks\check_commission_signal_board_output.py --selftest
python -B .agents\hooks\check_csb_scanning_artifact.py --selftest
python -B .agents\hooks\check_review_output_provenance.py --selftest
```

```powershell
python -B -m pytest -q -p no:cacheprovider orca-harness\tests\unit\test_commission_signal_board_output_validator.py orca-harness\tests\unit\test_csb_scanning_artifact_validator.py orca-harness\tests\unit\test_review_output_provenance_checker.py
python -B -m py_compile .agents\hooks\check_commission_signal_board_output.py .agents\hooks\check_csb_scanning_artifact.py .agents\hooks\check_review_output_provenance.py
```

```powershell
python -B .agents\hooks\check_review_output_provenance.py --changed --strict
python -B .agents\hooks\check_review_output_provenance.py --strict docs\review-outputs\adversarial-artifact-reviews\sp5_finalization_producer_delegated_adversarial_code_review_patch_v0.md
python -B .agents\hooks\check_retrieval_header.py --staged --strict
python -B .agents\hooks\check_dcp_receipt_hygiene.py --staged --strict
python -B .agents\hooks\check_engagement_stale_phrases.py --staged --strict
git diff --check eee9aa7b3f42a5baf4e5dfe99495f07ad09a15d5..64a13b7af04e98e9e3877339bffc7856693211e2
```

Known local dirty-state caveat from the authoring lane: `python -B .agents\hooks\check_retrieval_header.py --changed --strict` failed because of the pre-existing unrelated untracked `docs/prompts/hygiene-queue/precompact_search_surface_trends_next.md` missing a retrieval header. Do not treat that hygiene-queue file as part of the P4-P6 target unless the CA explicitly redirects.

Author-observed validation summary before this prompt was filed:

- P4-P6 changed checker selftests: `SELFTEST OK`.
- P1-P6 checker selftests: `SELFTEST OK` for DCP receipt hygiene, registry/list sync, stale phrases, CSB output, CSB scanning artifact, and review-output provenance.
- Relevant pytest files: passed at `100%`.
- `py_compile` for all six enforcement checkers: exited 0.
- P6 staged strict gates for review-output provenance, retrieval header, DCP receipt hygiene, engagement stale phrases, and `git diff --cached --check`: exited 0.
- `git diff --check` for the worktree: exited 0 during P5/P6 validation, with CRLF warnings only when Git reported them.

Targeted leakage searches:

```powershell
rg -n "validation|readiness|proof|acceptance|buyer proof|score|scoring|resonance weight|demand proof|route binding|model recommendation|runtime model|auto-promot|ontology|schema|CI|runtime" .agents/hooks/check_commission_signal_board_output.py .agents/hooks/check_csb_scanning_artifact.py .agents/hooks/check_review_output_provenance.py .agents/hooks/README.md orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md orca/product/spines/scanning/README.md
```

```powershell
rg -n "engagement_as_proof|engagement_gate_clearance|engagement_route_binding|engagement_graph_weight|engagement_commit_scale|engagement_credibility|engagement_amplification|engagement_action_ceiling|final resonance weight|reviewed_by|authored_by|review_use_boundary|decision input" .agents/hooks/check_commission_signal_board_output.py .agents/hooks/check_csb_scanning_artifact.py .agents/hooks/check_review_output_provenance.py orca-harness/tests/unit/test_commission_signal_board_output_validator.py orca-harness/tests/unit/test_csb_scanning_artifact_validator.py orca-harness/tests/unit/test_review_output_provenance_checker.py
```

## Output Contract

Write the durable report to:

`docs/review-outputs/engagement_resonance_enforcement_p4_p6_adversarial_code_review_v0.md`

The report must include:

- `reviewed_by` and `authored_by` provenance fields. Use `unrecorded` only when the operator/tooling did not provide the value; do not fabricate.
- `de_correlation_bar`: `cross_vendor_discovery`, `same_vendor_sanity`, or `self_fallback`.
- `same_vendor_rationale` when `de_correlation_bar` is `same_vendor_sanity`.
- `source_context_status`: `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
- Findings ordered by severity, with file/line citations.
- For each actionable finding: `minimum_closure_condition` and `next_authorized_action`.
- Validation commands run, exit status, and material output.
- Residual risks and not-assessed gaps.
- Explicit review-use boundary: findings are decision input only, not approval, validation, readiness, mandatory remediation, or patch authority.

Return this courier YAML in chat after the report is written:

```yaml
review_summary:
  status: completed | blocked | failed
  report_path: docs/review-outputs/engagement_resonance_enforcement_p4_p6_adversarial_code_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  reviewed_by: operator_to_fill
  authored_by: openai-gpt-5-codex
  de_correlation_bar: operator_to_fill
  summary: "One sentence."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  next_action: "One concrete next step."
```

Review findings are decision input only. They are not approval, validation, readiness, mandatory remediation, or patch authority until the CA adjudicates them.
