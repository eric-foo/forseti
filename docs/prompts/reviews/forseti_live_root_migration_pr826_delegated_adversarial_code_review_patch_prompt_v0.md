# Forseti Live Root Migration PR826 - Delegated Adversarial Code Review-And-Patch Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review-and-patch prompt
scope: >
  Delegated adversarial implementation/code review-and-patch commission for
  PR #826's live Forseti root migration, pinned to migration commit
  f53e6f2ef24df24bb88079453dd6b2383a508dd0.
use_when:
  - Dispatching a de-correlated controller to review and, if needed, patch the PR #826 live-root migration before CA adjudication.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/validation-gates.md
branch_or_commit: codex/forseti-live-root-migration-rebased migration target f53e6f2ef24df24bb88079453dd6b2383a508dd0; base 397b15705a68e22e1400c093d947a0f093d5eec9
stale_if:
  - The base or migration target commit is unavailable in the receiving worktree.
  - The reviewer cannot inspect the pinned range 397b15705a68e22e1400c093d947a0f093d5eec9..f53e6f2ef24df24bb88079453dd6b2383a508dd0.
```

## Commission

Run a de-correlated adversarial implementation/code review-and-patch pass on
PR #826's live Forseti root migration:

```text
PR:     https://github.com/eric-foo/forseti/pull/826
base:   397b15705a68e22e1400c093d947a0f093d5eec9
target: f53e6f2ef24df24bb88079453dd6b2383a508dd0
range:  397b15705a68e22e1400c093d947a0f093d5eec9..f53e6f2ef24df24bb88079453dd6b2383a508dd0
branch: codex/forseti-live-root-migration-rebased
```

The author/home model family is OpenAI/Codex. The reviewing controller must be a
different vendor or family when this is used to satisfy de-correlation. This is
a who-constraint and measurement field, not a runtime model recommendation. If
the runtime is same-vendor or unknown, proceed only as bounded sanity review and
record that the cross-vendor discovery bar was not met.

Your output is decision input for CA adjudication. It is not approval,
readiness, merge authority, or auto-keep authority.

## Route Decision

This request came through `delegate review patch`. The target is a multi-file
implementation/code migration, not a single high-stakes authored artifact. Per
`.agents/workflow-overlay/delegated-review-patch.md`, do not stretch the
single-artifact delegated review-and-patch convention to fit it. Route through
the implementation/code review lane, with bounded patch execution explicitly
authorized for defects inside this PR range.

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/orca_preflight_defaults_v0.md`
v0 - repo constants bound; deltas stated below.

```yaml
orca_start_preflight:
  agents_read: required_yes
  overlay_read: required_yes
  source_pack: custom
  edit_permission: patch-only
  target_scope:
    - pinned range 397b15705a68e22e1400c093d947a0f093d5eec9..f53e6f2ef24df24bb88079453dd6b2383a508dd0
    - files changed in that range, excluding prior prompt/review artifacts unless directly load-bearing
  dirty_state_checked: required_yes
  blocked_if_missing: yes

authorization_basis: current owner request, "delegate review patch", for PR #826 after local and CI validation.
objective: find and patch material bugs, false-success paths, stale root references, route drift, CI breakage, or avoidable bloat in the live Forseti root migration.
intended_decision: whether PR #826 can proceed to CA adjudication as-is, with delegate patch, or with a larger architecture/doctrine pass.
output_mode: review-report
review_report_path: docs/review-outputs/forseti_live_root_migration_pr826_delegated_adversarial_code_review_patch_v0.md
edit_permission: patch-only
patch_execution_authority: bound to material closure patches inside the PR #826 migration range; no commits, pushes, merges, or PR metadata edits.
dirty_state_allowance: begin from a clean worktree or report dirty state before continuing; reviewer-owned patch diffs are allowed after source context is ready.
branch_or_commit_reference: codex/forseti-live-root-migration-rebased target f53e6f2ef24df24bb88079453dd6b2383a508dd0; base 397b15705a68e22e1400c093d947a0f093d5eec9.
doctrine_change_decision: no new doctrine change is authorized; if closure requires doctrine change, return NEEDS_ARCHITECTURE_PASS or off-scope finding.
isolation_decision: use an isolated worktree or branch for patching; do not patch the CA/home lane directly.
validation_gates: run targeted checks after any patch and record exact observed output in the report.
thread_operating_target_continuity:
  carried_forward: yes
  target: PR #826 live Forseti root migration.
```

## Required Method Sequence

1. Read this prompt.
2. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
3. Read `.agents/workflow-overlay/review-lanes.md`,
   `.agents/workflow-overlay/prompt-orchestration.md`,
   `.agents/workflow-overlay/delegated-review-patch.md`,
   `.agents/workflow-overlay/source-loading.md`, and
   `.agents/workflow-overlay/validation-gates.md`.
4. REFERENCE-LOAD `workflow-deep-thinking`.
5. REFERENCE-LOAD `workflow-code-review`.
6. Do not APPLY either method yet.
7. SOURCE-LOAD the pinned diff and required source context below.
8. Declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
9. APPLY deep-thinking to frame highest-risk failure modes.
10. APPLY workflow-code-review to produce findings.
11. If a bounded fix is needed, patch only the authorized PR #826 migration scope.
12. Fresh-read changed files and rerun required validation after any patch.
13. Write the review report to the output path before returning a chat summary.

If `workflow-code-review` is unavailable or not applied, return
`BLOCKED_REVIEW_LANE_UNAVAILABLE` or advisory-only findings. Do not emit strict
review claims.

## Source Context

Required reads:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.github/workflows/ci.yml`
- `.agents/hooks/check_map_links.py`
- `.agents/hooks/header_index.py`
- `.agents/hooks/check_deletion_evidence.py`
- `.agents/hooks/check_repo_map_freshness.py`
- `.agents/hooks/check_retrieval_header.py`
- `README.md`
- `AGENTS.md`
- `repo-structure.yaml`
- `docs/workflows/forseti_repo_map_v0.md`
- `forseti/product/README.md`
- `forseti-harness/README.md`
- `docs/hygiene/migrations/moved_paths_index.md`

Inspect the pinned diff with:

```powershell
git diff --stat 397b15705a68e22e1400c093d947a0f093d5eec9..f53e6f2ef24df24bb88079453dd6b2383a508dd0
git diff --name-status 397b15705a68e22e1400c093d947a0f093d5eec9..f53e6f2ef24df24bb88079453dd6b2383a508dd0
git diff 397b15705a68e22e1400c093d947a0f093d5eec9..f53e6f2ef24df24bb88079453dd6b2383a508dd0 -- <selected target paths>
```

Do not review or clean up previous prompts, previous reviews, or stale review
outputs except where one is directly load-bearing to a concrete finding.

## Observed Implementation Context

The migration commit claims to:

- make `forseti/`, `forseti/product/`, and `forseti-harness/` the live roots;
- remove live `orca/`, `orca/product/`, and `orca-harness/` trees;
- rename local product-lead skills to `forseti-product-lead`;
- update docs, repo maps, workflow overlay, CI, hooks, validation gates, and
  moved-path records to route to Forseti roots;
- keep deliberately deferred compatibility strings such as `ORCA_DATA_ROOT` and
  `--report-orca` only where runtime compatibility still depends on them;
- avoid sweeping historical/provenance-only artifacts beyond the migration's
  routing need.

Validation observed before this review commission:

```text
PR #826 CI run 29036172805: success
job forseti-harness-tests: success

Remove-Item Env:ORCA_DATA_ROOT -ErrorAction SilentlyContinue; python -m pytest
1241 passed, 3 skipped, 1 warning

python .agents/hooks/check_map_links.py --strict
OK - 0 findings, 35 annotated nonresolving debt

python .agents/hooks/check_retrieval_header.py --changed --strict
OK

python .agents/hooks/header_index.py --strict --base origin/codex/forseti-identity-d1-closeout
OK - 207 changed durable .md files

python .agents/hooks/check_deletion_evidence.py --strict
OK

python .agents/hooks/check_ontology_ssot.py --strict
OK

python .agents/hooks/check_ontology_tag_validity.py --strict
OK

python .agents/hooks/check_ontology_drift.py --strict
OK

python .agents/hooks/check_repo_map_freshness.py --changed
exit 0 advisory, map/submap updated gate satisfied

git diff --check origin/codex/forseti-identity-d1-closeout...HEAD
OK

Physical path readback:
orca=False
orca\product=False
orca-harness=False
forseti=True
forseti\product=True
forseti-harness=True
.agents\skills\forseti-product-lead\SKILL.md=True
.claude\skills\forseti-product-lead\SKILL.md=True
```

Treat this validation as context to inspect, not proof to inherit.

## Attack Questions

Find material bugs, false-success paths, authority drift, or bloat. Focus on:

1. Live-root completeness: are live `orca/`, `orca/product/`, and
   `orca-harness/` actually gone, and are `forseti/`, `forseti/product/`, and
   `forseti-harness/` present with coherent contents?
2. CI correctness: does the CI workflow run the intended Forseti harness path,
   and would it fail if the renamed harness path or test invocation were stale?
3. Hook correctness: do validation hooks inspect the Forseti roots and avoid
   stale false greens from hard-coded old paths?
4. Deletion evidence: does the deletion gate prove the old live roots are gone
   without relying on doc claims or secondary reports?
5. Route integrity: do `open_next`, repo-map, README, and overlay references
   route to live Forseti paths without inventing fake compatibility roots?
6. Compatibility boundary: are residual `ORCA_DATA_ROOT`, `--report-orca`, and
   historical/provenance names intentionally deferred and not presented as live
   identity surfaces?
7. Skill and agent routing: do `.agents/skills/` and `.claude/skills/` now expose
   Forseti product-lead identity without stale Orca front-door labels?
8. Bloat and churn: did the migration rewrite historical/provenance material
   that did not need live-route edits, or add duplicate navigation layers that
   increase cold-lane search cost?
9. Path-sensitive runtime behavior: do imports, package discovery, fixture paths,
   generated reports, and data-root defaults still work after the physical move?
10. Validation sufficiency: is there a missing cheap check that would have caught
    realistic stale-root, CI, hook, or packaging regressions?

## Patch Boundary

Editable scope:

- Files changed in the pinned PR #826 migration range when the patch directly
  closes a material finding.
- Adjacent validation files only when needed to make an existing migration gate
  catch the finding.
- The review report output path named below.

Do not edit:

- prior prompts, prior review outputs, or stale historical artifacts merely for
  cleanup;
- external plugin caches, installed skill packages, `.git`, or non-repo files;
- runtime API names such as `ORCA_DATA_ROOT` or `--report-orca` unless the
  current migration creates an actual failing behavior that must be fixed now;
- product, architecture, validation, or review doctrine outside the minimum
  migration closure;
- branch protection, PR metadata, commits, pushes, or merges.

If the correct fix requires a new migration doctrine decision, broad historical
rewrite, API deprecation policy, or compatibility-breaking rename, return
`NEEDS_ARCHITECTURE_PASS` or an off-scope finding instead of patching.

## Required Validation

After any patch, run the narrowest relevant subset and record exact observed
output. At minimum, run:

```powershell
git diff --check 397b15705a68e22e1400c093d947a0f093d5eec9..HEAD
python .agents/hooks/check_retrieval_header.py --changed --strict
python .agents/hooks/check_deletion_evidence.py --strict
python .agents/hooks/check_map_links.py --strict
python .agents/hooks/check_repo_map_freshness.py --changed
```

If code, CI, or harness files are patched, also run:

```powershell
Remove-Item Env:ORCA_DATA_ROOT -ErrorAction SilentlyContinue; Push-Location forseti-harness; python -m pytest; Pop-Location
```

If a command cannot be run, state the exact reason and what risk remains.

## Output Path

Write the durable review report to:

`docs/review-outputs/forseti_live_root_migration_pr826_delegated_adversarial_code_review_patch_v0.md`

## Output Contract

Start with:

```yaml
review_summary:
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  source_context: SOURCE_CONTEXT_READY | SOURCE_CONTEXT_INCOMPLETE
  reviewed_by: operator_to_fill_or_unrecorded
  authored_by: OpenAI/Codex
  de_correlation_bar: cross_vendor_discovery | same_vendor_sanity | self_fallback | unrecorded
  same_vendor_rationale: required_if_same_vendor_sanity
  target_range: 397b15705a68e22e1400c093d947a0f093d5eec9..f53e6f2ef24df24bb88079453dd6b2383a508dd0
  report_path: docs/review-outputs/forseti_live_root_migration_pr826_delegated_adversarial_code_review_patch_v0.md
```

Then include:

1. Findings first, ordered by severity.
2. For each finding: id, severity, affected file/line, evidence, risk, minimum
   closure condition, and whether you patched it.
3. Patch summary, if any.
4. Unified diff for any patch.
5. Fresh-read evidence for changed files.
6. Validation commands and observed output, or not-run reasons.
7. Non-findings / seams that held.
8. Residual risk.
9. Verdict: `PATCHED_FOR_CA_ADJUDICATION`,
   `NO_PATCH_NEEDED_FOR_CA_ADJUDICATION`, `NEEDS_ARCHITECTURE_PASS`, or
   `BLOCKED`.

Findings and patches are CA decision input only. The CA/home model decides what
is kept.
