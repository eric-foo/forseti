# Creator Profile Current Validator Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Repo-bound adversarial code review prompt for the creator_profile_current validator commit on PR #439.
use_when:
  - Commissioning a read-only adversarial code review of the creator profile current validator patch.
  - Checking whether the validator admits misleading creator-profile aggregate metrics or rejects valid current profiles.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
branch_or_commit: codex/creator-metric-source-audit @ da2987c6a3891064a9ba82b152a3b5025f54be52
stale_if:
  - PR #439 head moves past da2987c6a3891064a9ba82b152a3b5025f54be52 before review.
  - Any target file in HEAD^..HEAD changes before review.
```

## Orca Prompt Preflight

- output_mode: `review-report`
- prompt_artifact_path: `docs/prompts/reviews/creator_profile_current_validator_adversarial_code_review_prompt_v0.md`
- durable_review_report_destination: `docs/review-outputs/creator_profile_current_validator_adversarial_code_review_v0.md`
- template_kind: `review`; project template registry has no bound `repo-code-review` template, so this prompt uses the Orca review-prompt contract directly.
- edit_permission: `read-only`; do not edit files, do not apply patches, do not emit `patch_queue_entry`.
- workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\creator-metric-source-audit`
- expected_branch: `codex/creator-metric-source-audit`
- expected_revision: `da2987c6a3891064a9ba82b152a3b5025f54be52`
- target_scope: `HEAD^..HEAD` only.
- dirty_state_allowance: clean worktree required before review; if dirty or at a different revision, return `BLOCKED_WRONG_SOURCE_STATE`.
- source_pack: custom S0 + target patch read pack.
- repo_map_decision: not_needed
- repo_map_reason: target files, branch, commit, review lane, and report destination are already bound.
- controlling_source_state: checked by commissioning lane before filing; receiver must re-check locally before review.
- doctrine_change: none intended; this prompt changes no Orca doctrine.
- source_hierarchy: current user instruction > `AGENTS.md` > `.agents/workflow-overlay/` > Orca docs; explicitly invoked skills are task-local mechanics only.
- external_source_boundary: do not import `jb`, external workflow source, installed skill source, or generic project policy as Orca authority.

## Objective

Run a read-only adversarial code review of the validator commit that added `capture_spine.creator_profile_current`. The core question is whether the code and tests actually protect the current creator-profile aggregate view from misleading identity/metric claims, without overclaiming validation, dashboard readiness, SQLite readiness, or Silver-lake derivation.

This request was routed from a `workflow-delegated-review-patch` invocation, but the target is a multi-file implementation/code diff rather than a single high-stakes authored artifact. Treat this as an adversarial code review, not as patch-execution authority.

## De-Correlation And Provenance

- who_constraint: If the operator wants cross-vendor discovery, paste/run this prompt with a reviewer whose upstream model vendor or lineage differs from the author/home model. This is a who-constraint, not a model recommendation.
- de_correlation_bar: operator_to_fill (`cross_vendor_discovery` | `same_vendor_sanity` | `self_fallback`)
- same_vendor_rationale: operator_to_fill when applicable
- reviewed_by: operator_to_fill or `unrecorded`
- authored_by: operator_to_fill or `unrecorded`

Do not recommend, rank, prescribe, or imply any runtime model. Record observed provenance only.

## Required Method Loading

1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. Read `.agents/workflow-overlay/source-loading.md`.
4. Read `.agents/workflow-overlay/prompt-orchestration.md`.
5. Read `.agents/workflow-overlay/review-lanes.md`.
6. REFERENCE-LOAD `workflow-deep-thinking`. Do not APPLY it yet.
7. REFERENCE-LOAD `workflow-code-review`. Do not APPLY it yet.
8. SOURCE-LOAD the target sources below.
9. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
10. Only after source readiness, APPLY deep-thinking to frame failure modes, then APPLY code review to produce findings.

If `workflow-code-review` is unavailable, return `BLOCKED_REVIEW_LANE_UNAVAILABLE` and do not substitute an inline self-review while claiming the lane ran.

## Target Sources

Review exactly this patch:

```text
git show --stat --oneline --no-renames da2987c6a3891064a9ba82b152a3b5025f54be52
git diff da2987c6a3891064a9ba82b152a3b5025f54be52^..da2987c6a3891064a9ba82b152a3b5025f54be52 -- \
  orca-harness/capture_spine/creator_profile_current/__init__.py \
  orca-harness/capture_spine/creator_profile_current/validation.py \
  orca-harness/tests/unit/test_creator_profile_current_static_view.py
```

Required source reads:

- `orca-harness/capture_spine/creator_profile_current/__init__.py`
- `orca-harness/capture_spine/creator_profile_current/validation.py`
- `orca-harness/tests/unit/test_creator_profile_current_static_view.py`
- `orca-harness/capture_spine/creator_public_handle_linkage/validation.py`
- `orca-harness/capture_spine/youtube_creator_observation/validation.py`
- `orca-harness/tests/unit/test_youtube_creator_metric_seed.py`
- `orca-harness/pyproject.toml`
- `orca/product/spines/capture/core/source_families/social_media/creator_profile_current_view_v0.json`
- `orca/product/spines/capture/core/source_families/social_media/creator_public_handle_linkage_ledger_v0.json`
- `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_shorts_fragrance_creator_metric_seed_v0.json`

Sources available but out of default scope:

- The rest of PR #439 history.
- SQLite/data-lake physicalization design.
- Dashboard/product-surface implementation.
- Live capture probes and source-capture runtime behavior.

Open an out-of-scope source only if a finding cannot be decided without it; record the reason and keep the finding scoped to the validator patch.

## Review Axes To Attack

Attack these failure modes first:

- False pass: a malformed profile, metric rollup, identity state, source input, or count could pass and make the ledger look more authoritative than it is.
- False fail: a valid current platform-account profile could fail because the validator overfits today’s fixture.
- Metric posture leakage: unavailable engagement, like, comment, cadence, or velocity metrics could be zero-filled or treated as observed.
- Identity stitching leakage: candidate, rejected, or single-platform identities could accidentally produce cross-platform rollups.
- Source-backedness leakage: counts, source-input hashes, observation IDs, or sample-support claims could drift without detection.
- Import/package risk: the new package might not be importable under the harness packaging rules.
- Test adequacy: mutation tests might miss a class-level issue that would matter for creator-profile aggregate claims.

Name non-findings when a scary-looking risk is already covered by code or tests.

## Review Output Contract

Write the durable report to:

`docs/review-outputs/creator_profile_current_validator_adversarial_code_review_v0.md`

The report must start with:

```yaml
review_summary:
  status: completed | blocked | failed
  report_path: docs/review-outputs/creator_profile_current_validator_adversarial_code_review_v0.md
  recommendation: accept | patch_before_merge | blocked
  reviewed_by: operator_to_fill_or_unrecorded
  authored_by: operator_to_fill_or_unrecorded
  de_correlation_bar: operator_to_fill
  same_vendor_rationale: operator_to_fill_or_null
  summary: "One sentence."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step."
```

Then list findings first. For each finding include:

- id: `CPV-01`, `CPV-02`, etc.
- severity: `critical` | `major` | `minor`
- file and line references
- issue
- why it matters for creator-profile aggregate safety
- minimum_closure_condition
- next_authorized_action

Severity contract:

- `critical`: validator can admit a materially false public creator-profile claim, corrupt core identity/metric semantics, or block all valid use.
- `major`: likely false pass/false fail, untested risky branch, packaging/import breakage, or fixture/schema drift that would mislead PR acceptance.
- `minor`: clarity, maintainability, or optional hardening that is not required before merge.

Do not include executor-ready patch instructions or `patch_queue_entry`. Advisory remediation direction is allowed. Review findings are decision input only; they are not approval, validation, readiness, mandatory remediation, or patch authority until the Chief Architect separately accepts or authorizes action.

## Validation Evidence To Inspect

The commissioning lane observed these checks before filing this prompt; verify from source where useful, and rerun only if appropriate for your environment:

```text
python -m pytest orca-harness\tests\unit\test_creator_profile_current_static_view.py orca-harness\tests\unit\test_youtube_creator_metric_seed.py
git diff --check
python .agents\hooks\check_retrieval_header.py --changed --strict
python .agents\hooks\check_map_links.py --strict
python .agents\hooks\check_placement.py --check
```

Observed result from commissioning lane:

- focused pytest: `13 passed`
- `git diff --check`: exit 0, with Windows LF-to-CRLF warnings only
- retrieval header check: exit 0
- map links strict: exit 0, 0 findings
- placement check: exit 0 with pre-existing/advisory placement noise; new harness validator appears as legacy-tolerated

If you rerun checks, report exact commands and outcomes. If you do not rerun, state `not_run` and review the existing evidence instead.

## Hard Boundaries

- Do not edit files.
- Do not commit, push, or open a PR.
- Do not review the entire creator-ledger product architecture unless needed to explain a concrete validator finding.
- Do not make SQLite, dashboard, capture-lane, or Silver-lake producer recommendations unless a validator bug depends on them.
- Do not claim validation, readiness, approval, or merge safety.
- If the source state is wrong or the review lane cannot be loaded, return the nearest blocker rather than reviewing a substitute source pack.

