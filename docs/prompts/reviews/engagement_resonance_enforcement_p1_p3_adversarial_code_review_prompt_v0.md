# Engagement Resonance Enforcement P1-P3 Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review prompt
scope: >
  Filed route-out prompt for adversarial implementation/code review of the
  first three engagement-resonance enforcement checkers on branch
  codex/search-surface-mgt-p0-captures-ws.
use_when:
  - Commissioning an independent review of the P1-P3 checker batch after commits e88ed222, 51f839e5, and 6fffd769.
  - Checking whether the DCP receipt hygiene, registry/list sync, and stale-phrase sweep checkers reduce LLM burden without creating false passes, false failures, overclaiming, or broad grep noise.
authority_boundary: retrieval_only
branch_or_commit: codex/search-surface-mgt-p0-captures-ws @ 6fffd769822a6f6d381717100323720da024d7b1
```

## Orca Prompt Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_review_packet
  edit_permission: read-only
  target_scope: >
    Review only the P1-P3 engagement-resonance enforcement checker batch:
    diff range 182ee24c..6fffd769 over the named hook files and README entry.
    Do not patch source files in this review lane.
  dirty_state_checked: yes
  blocked_if_missing: >
    If the worktree, branch, target commits, or target files cannot be
    confirmed, return SOURCE_CONTEXT_INCOMPLETE instead of reviewing a
    substitute checkout or broad branch diff.

prompt_mode:
  output_mode: file-write review prompt; receiver output mode is review-report
  prompt_artifact_path: docs/prompts/reviews/engagement_resonance_enforcement_p1_p3_adversarial_code_review_prompt_v0.md
  report_destination: docs/review-outputs/engagement_resonance_enforcement_p1_p3_adversarial_code_review_v0.md
  template_kind: review
  repo_map_decision: not_needed
  repo_map_reason: target commits, files, and validation commands are named directly

workspace_preflight:
  workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\search-surface-mgt-p0-captures
  expected_branch: codex/search-surface-mgt-p0-captures-ws
  expected_target_head: 6fffd769822a6f6d381717100323720da024d7b1
  expected_base_before_checker_batch: 182ee24c
  target_commit_range: 182ee24c..6fffd769
  dirty_state_allowance: >
    The prompt file itself and the review report may be present as local
    additions or later prompt-only commits. The implementation files under
    review must match the expected target head unless the CA explicitly
    redirects. The pre-existing untracked docs/prompts/hygiene-queue/ is not
    part of the review target.
  untracked_scope: prompt/report artifacts plus pre-existing docs/prompts/hygiene-queue/ only

route_from_delegated_review_patch:
  status: routed_to_code_review
  reason: >
    Orca's delegated-review-patch convention is provisional and should not be
    stretched to a multi-file implementation/code diff. This commission
    therefore requests de-correlated adversarial implementation/code review,
    not patch execution.
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

Goal: reduce recurring LLM review burden around public-engagement resonance handling by making three mechanical failure classes visible at the tool boundary.

Done looks like: future agents can run narrow checkers for DCP receipt storage shape, Signal Use vocabulary drift, and stale engagement-doctrine phrase leakage instead of manually re-reading broad doctrine, while every checker stays shape/leakage-only and makes no proof, validation, readiness, acceptance, buyer-proof, or resonance-judgment claim.

Treat this as an axis to attack, not a pass-if-matches bar.

## Source-Gated Method Contract

1. REFERENCE-LOAD the required method instructions first. Do not APPLY them yet.
2. SOURCE-LOAD the authority and target files below.
3. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
4. Only after source readiness, APPLY `workflow-deep-thinking`, then APPLY `workflow-code-review`.
5. For the handoff/README/documentation parts of the mixed change packet, also apply a bounded artifact/doctrine leakage check. If `workflow-adversarial-artifact-review` is available, REFERENCE-LOAD it before source loading and APPLY it after `SOURCE_CONTEXT_READY`; if unavailable, name that gap and continue the code review without issuing strict artifact-review claims.

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
- `orca/product/spines/foundation/product_contract/core_spine_v0_information_production_foundation_v0.md`

Required target reads:

- `.agents/hooks/check_dcp_receipt_hygiene.py`
- `.agents/hooks/check_registry_list_sync.py`
- `.agents/hooks/check_engagement_stale_phrases.py`
- `.agents/hooks/README.md`

Adjacent comparison reads:

- `.agents/hooks/check_doc_terms.py`
- `.agents/hooks/check_commission_signal_board_output.py`
- `.agents/hooks/check_csb_scanning_artifact.py`
- `docs/decisions/dcp_receipts_archive_v0.md` targeted only for DCP archive-pointer behavior if the DCP checker appears to mishandle archive rules.

Git context to inspect:

- `git status --short --branch`
- `git rev-parse HEAD`
- `git log --oneline 182ee24c..6fffd769`
- `git diff --stat 182ee24c..6fffd769`
- `git diff --patch --no-ext-diff --unified=80 182ee24c..6fffd769 -- .agents/hooks/check_dcp_receipt_hygiene.py .agents/hooks/check_registry_list_sync.py .agents/hooks/check_engagement_stale_phrases.py .agents/hooks/README.md`

If later prompt-only commits exist on the branch, do not treat them as part of the implementation target. Review the checker batch diff above unless the CA explicitly redirects.

## Review Scope

Findings-first. Prioritize bugs, false passes, false failures, brittle parsing, missing selftests, over-enforcement, historical/noise leakage, stale vocabulary, path/cwd failures, and misleading docs. Do not praise the patch before listing findings.

Review questions:

- Does `check_dcp_receipt_hygiene.py` enforce exactly the DCP storage shape it claims: at most two inline receipts, required archive pointer after inline receipts, and no unauthorized standalone DCP receipt markdown files?
- Can the DCP checker miss active receipts because of heading-region logic, fenced YAML shape, archive-pointer wording, or filename matching?
- Can the DCP checker falsely flag schema examples, the authorized archive, non-markdown checker filenames, or historical prompt/review records?
- Does `check_registry_list_sync.py` correctly enforce only the one accepted binding: Foundation Allowed Signal Uses must be contained by Engagement Registry Signal Use Classification?
- Does the registry/list checker avoid bidirectional enforcement, auto-promotion, category correctness decisions, or ontology/schema expansion?
- Does the registry/list checker make the known live drift visible (`actor-strategy evidence` missing from the registry) without treating checker passing as product correctness?
- Does `check_engagement_stale_phrases.py` flag curated old attention-only, engagement-only cap, score-boost shorthand, and `engagement-proof` wording when they appear in live doctrine?
- Does the stale-phrase checker default to live doctrine paths only and exclude historical prompts, review outputs, hygiene notes, migrations, DCP archives, and DCP self-reference query text?
- Does the stale-phrase checker avoid false positives on current non-claim wording such as `numeric score boost`, `not proof`, or boundaries that say agents must not interpret whether engagement proves demand?
- Do all three checkers preserve advisory default and strict mode behavior, with no fake fail-open success where a strict finding should exit nonzero?
- Are `--changed`, `--staged`, explicit path, and `--live` modes scoped correctly and robust when Git is unavailable, paths are absolute, paths are directories, or selected files are unrelated?
- Are selftests independent enough to catch regressions, or are they mostly confirming current implementation strings?
- Does the README describe these as checker substrates, not validation, readiness, proof, acceptance, or CI promotion?
- Does the batch avoid runtime/schema infrastructure, broad grep gates, scoring engines, crawlers, dashboards, or doctrine rewrites outside the accepted priority units?

Out of scope:

- No implementation of Priority 4, Priority 5, or Priority 6.
- No product-doctrine adjudication or vocabulary auto-fix for the `actor-strategy evidence` live drift.
- No CI wiring or mandatory repo-wide gate promotion.
- No runtime implementation, crawler, dashboard, schema migration, scoring engine, or resonance-weight calculation.
- No patch execution in this review lane. Recommend concrete fixes, but leave source edits to CA adjudication and a separate patch turn.

## Validation To Run

Run these from the workspace root unless noted. If a command is unavailable, times out, or fails for an environmental reason, record it as not run or blocked with the observed error.

Because this change introduces or materially changes custom checkers, first run a 30-second child-scoped smoke probe for each checker selftest before any repeated/raw validation run. If a smoke probe times out, stop and return `VALIDATION_HOOK_TIMEOUT` with command, cwd, touched files, and observed process state.

```powershell
python -B .agents\hooks\check_dcp_receipt_hygiene.py --selftest
python -B .agents\hooks\check_registry_list_sync.py --selftest
python -B .agents\hooks\check_engagement_stale_phrases.py --selftest
```

```powershell
python -B .agents\hooks\check_dcp_receipt_hygiene.py --changed --strict
python -B .agents\hooks\check_registry_list_sync.py --changed --strict
python -B .agents\hooks\check_engagement_stale_phrases.py --changed --strict
python -B .agents\hooks\check_engagement_stale_phrases.py --live --strict
```

```powershell
python -B .agents\hooks\check_registry_list_sync.py --live
python -B .agents\hooks\check_registry_list_sync.py --live --strict
```

The `--live --strict` registry/list command is expected to exit nonzero if the current live product-doctrine drift is still present; record it as evidence that the checker detects the drift, not as proof the product vocabulary is correct.

```powershell
git diff --check 182ee24c..6fffd769
```

Targeted stale/leakage searches:

```powershell
rg -n "validation|readiness|proof|acceptance|buyer proof|score|scoring|resonance weight|demand proof|auto-promot|ontology|schema|CI|runtime" .agents/hooks/check_dcp_receipt_hygiene.py .agents/hooks/check_registry_list_sync.py .agents/hooks/check_engagement_stale_phrases.py .agents/hooks/README.md
```

```powershell
rg -n "direction_change_propagation|dcp_receipt|stale_language_search|attention-only|engagement-only|score boost|engagement-proof|actor-strategy evidence|competitor-strategy evidence" .agents/hooks/check_dcp_receipt_hygiene.py .agents/hooks/check_registry_list_sync.py .agents/hooks/check_engagement_stale_phrases.py .agents/hooks/README.md
```

## Output Contract

Write the durable report to:

`docs/review-outputs/engagement_resonance_enforcement_p1_p3_adversarial_code_review_v0.md`

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
  report_path: docs/review-outputs/engagement_resonance_enforcement_p1_p3_adversarial_code_review_v0.md
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
