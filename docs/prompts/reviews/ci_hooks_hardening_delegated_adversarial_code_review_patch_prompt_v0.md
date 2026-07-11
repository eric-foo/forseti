# CI and Hooks Hardening — Delegated Adversarial Code Review and Patch

```yaml
retrieval_header_version: 1
artifact_role: canonical Forseti delegated adversarial code-review-and-patch commission prompt
scope: adversarial review and bounded patch of the current CI, hooks, workflow-doctrine, and wiring-test diff
use_when:
  - A different-vendor controller reviews the current dirty worktree before the lane is committed or landed.
authority_boundary: retrieval_only
```

## What this is for

**Goal:** Make the CI and local hook system fail earlier and more consistently while preserving real failure visibility and enforcing the protected-main workflow on GitHub.

**Done looks like:** The completed diff is internally consistent, materially correct, bounded to the named files, supported by tests and fresh GitHub readback, and has no unresolved material review finding. Treat this goal as an axis to attack, not a pass-if-conforms review bar.

## Commission and lane binding

- `overlay_status`: `provisional_opt_in`; explicitly commissioned by the owner through the fused implementation checkpoint. This is not a bound or machine-routable Forseti review lane.
- `target_kind`: `delegated_code_review_and_patch`.
- `review_lane`: `workflow-code-review`, with `workflow-deep-thinking` applied after source readiness.
- `mode`: `base-subagent` / single de-correlated controller; do not launch another reviewer.
- `access`: `repo`.
- `operating_contract_pointer`: `.agents/workflow-overlay/delegated-review-patch.md`.
- **Output mode:** review-report.
- `input_prompt_source`: `C:\Users\vmon7\Desktop\projects\orca\docs\prompts\reviews\ci_hooks_hardening_delegated_adversarial_code_review_patch_prompt_v0.md`.
- `review_report_destination`: `C:\Users\vmon7\Desktop\projects\orca\docs\review-outputs\ci_hooks_hardening_delegated_adversarial_code_review_patch_review_v0.md`.
- `edit_permission`: `patch-only`, limited to the named source targets below plus creation/update of the review report destination.
- `workflow_sequence_source`: explicit fused checkpoint plus Forseti overlay.
- `workflow_sequence_status`: bound for this commission; adjudication and any keep decision remain with the home/CA model.
- `template_kind`: review with bounded patch authority; no project template is needed beyond this lane-scoped orchestrated body.
- `model_lane`: unbound and intentionally not recommended. The family difference below is a who-constraint, not runtime-model routing.

### Portable start preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: patch-only
  target_scope: named 16-file CI/hooks/doctrine/test change set plus the exact review-report destination
  dirty_state_checked: yes
  blocked_if_missing: BLOCKED_SOURCE_STATE_MISMATCH or the nearest authority/source/review-lane blocker
repo_map_decision: loaded
repo_map_reason: used to bind active hook, prompt, review-output, and doctrine locations
controlling_source_state:
  modified_in_reviewed_diff:
    - .agents/workflow-overlay/validation-gates.md
    - docs/workflows/forseti_repo_map_v0.md
  added_in_reviewed_diff:
    - docs/prompts/reviews/ci_hooks_hardening_delegated_adversarial_code_review_patch_prompt_v0.md
  other_prompt_review_source_owners: clean_at_pr_head
  strict_status_claims_requested: no
doctrine_change:
  primary_trigger: validation_philosophy
  related_triggers: [workflow_authority, lifecycle_boundary]
  propagation_surfaces: validation-gates, pre-push/CI wiring, dev-workflow doctrine, repo map, DCP receipt archive
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason:
external_source_boundary: external workflow source and jb are read-only and are not Forseti authority
```
### Actor/model-family receipt

- `author_home_model_family`: OpenAI GPT family (GPT-5 Codex).
- `controller_model_family`: `operator_to_fill`; must be a different upstream vendor/model lineage from OpenAI.
- `current_receiving_actor_role`: controller.
- `dispatch_mode`: external-controller-courier.
- `de_correlation_status`: the operator must confirm `satisfied` before review begins.

If you are an OpenAI-family model, if your upstream lineage is unknown, or if the operator cannot confirm that your family differs from the author/home family, return `BLOCKED_CONTROLLER_NOT_DECORRELATED` and do not review or patch. Do not turn this who-constraint into a model recommendation or ranking.

Do not spawn a replacement controller. You are the receiving controller. Do not recurse into unrelated agents.

## Repository preflight

Expected source-of-truth checkout:

- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- branch: `codex/ci-hooks-hardening-primary`
- base: `d6c36acdc64a741863215e1695075ccb466ceb15` (`origin/main` at commission refresh time)
- expected HEAD: operator supplies the current PR-head SHA in the dispatch wrapper; it must be the tip of `codex/ci-hooks-hardening-primary` and contain this prompt path
- expected state before controller edits: tracked tree clean at the supplied PR-head SHA; excluded user-owned/unrelated untracked directories `_test_runs/`, `orca-worktrees/`, and `worktrees/` may exist; inaccessible `_scratch/tmp*` warnings may exist and are out of scope
- this canonical prompt is read-only during the commissioned review and is not a patch target

Start with fresh reads:

```powershell
git rev-parse --abbrev-ref HEAD
git rev-parse HEAD
git rev-parse origin/main
git status --short
git diff --stat HEAD
git diff HEAD -- <named targets below>
```

If branch or HEAD differs, an unnamed source file is modified, or a named target is missing, return `BLOCKED_SOURCE_STATE_MISMATCH`. Do not review a summary, alternate checkout, recreated source, or context pack as a substitute. The named repo/worktree is authoritative for this run.

## Authority and required reads

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. REFERENCE-LOAD, without applying yet:
   - `workflow-deep-thinking`
   - `workflow-code-review`
3. Read the task-specific authority and contracts:
   - `.agents/workflow-overlay/source-loading.md`
   - `.agents/workflow-overlay/prompt-orchestration.md`
   - `.agents/workflow-overlay/delegated-review-patch.md`
   - `.agents/workflow-overlay/review-lanes.md` (code-review and shared output-binding sections)
   - `.agents/workflow-overlay/validation-gates.md`
   - `.agents/workflow-overlay/safety-rules.md`
   - `.agents/workflow-overlay/source-of-truth.md`
   - `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`
4. SOURCE-LOAD the complete named diff and the directly relevant implementation/tests.
5. Declare `SOURCE_CONTEXT_READY`, or `SOURCE_CONTEXT_INCOMPLETE` with missing sources, conflicts, and excluded evidence.
6. Only after readiness, APPLY `workflow-deep-thinking` to frame failure modes and APPLY `workflow-code-review` to the loaded change packet.

Authority order: `AGENTS.md` → Forseti overlay owner files → accepted decision records → changed implementation and tests → comments/summaries. External workflow source and `jb` are read-only and are not Forseti authority.

## Named editable source targets

The controller may patch only these source files, and only to close findings in this commission:

- `[registration-integrity]` `.agents/checks/registration_integrity.py`
- `[hooks-readme]` `.agents/hooks/README.md`
- `[ontology-checker]` `.agents/hooks/check_ontology_tag_validity.py`
- `[protected-action-guard]` `.agents/hooks/guard_protected_actions.py`
- `[prepush-guard]` `.agents/hooks/pre_push_guard.py`
- `[validation-doctrine]` `.agents/workflow-overlay/validation-gates.md`
- `[hook-installer]` `.github/scripts/install-local-hooks.ps1`
- `[merge-helper]` `.github/scripts/merge-when-green.ps1`
- `[auto-merge-workflow]` `.github/workflows/auto-merge.yml`
- `[ci-workflow]` `.github/workflows/ci.yml`
- `[main-red-workflow]` `.github/workflows/main-red-alert.yml`
- `[receipt-archive]` `docs/decisions/dcp_receipts_archive_v0.md`
- `[dev-workflow-doctrine]` `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`
- `[repo-map]` `docs/workflows/forseti_repo_map_v0.md`
- `[renovate]` `renovate.json`
- `[wiring-test]` `forseti-harness/tests/unit/test_ci_hook_wiring.py`

Everything else is read-only and flag-only. The named set cannot silently widen. Do not edit `AGENTS.md`, other overlay files, tests outside the named test, generated/canonical/hash-pinned sources, user-owned untracked directories, installed skills, external references, or GitHub settings. If a correct fix requires another file or an architecture/doctrine decision outside this already commissioned target, return the finding and `NEEDS_ARCHITECTURE_PASS` or request re-commissioning; do not patch it.

Why read-only review is insufficient: the fused checkpoint requires a de-correlated controller to close safe, bounded defects in the same pass so that a material finding does not return as an unactioned recommendation. Patch authority is subordinate to the explicit named scope above and does not create standing implementation authority.

## Review questions

Be maximally adversarial and coverage-first inside the commissioned scope. At minimum, test these claims rather than accepting them:

1. Does ontology strict mode truly inspect only tracked Markdown changed from the correct PR base, including additions, modifications, renames/copies, and deletions, while failing visibly on an infrastructure diff error?
2. Does the local pre-push mirror exactly cover the intended nine gates without weakening CI authority or introducing false-success paths?
3. Does CI preserve the required check name `forseti-harness-tests`, run fast policy gates before pytest, eliminate only the exact duplicate command, cancel only obsolete PR runs, and keep push-to-main runs non-cancelled?
4. Are external Actions genuinely pinned to immutable commit SHAs with useful version comments, and can Renovate maintain those pins without disabling other configured managers?
5. Does the hook installer correctly compare absolute and relative `core.hooksPath` values across Windows path semantics without accepting the wrong hooks directory?
6. Are classic branch-protection assumptions, custom auto-merge behavior, strict/up-to-date semantics, administrator enforcement, force-push/deletion settings, and workflow enablement described consistently across code and doctrine?
7. Were historical doctrine statements preserved as history while all live statements were updated, without DCP receipt loss, duplication, malformed rotation, or fake lifecycle claims?
8. Does the new wiring test prove behavior that matters without merely snapshotting implementation text or allowing a false green?
9. What CI failure classes from the observed history remain intentionally outside this patch, and are residuals named without pretending coverage?
10. Could any change fail differently on pull_request, push-to-main, Windows local hooks, GitHub-hosted Linux runners, renamed files, deleted files, shallow checkout, missing `origin/main`, or an untracked nested worktree?

Report every issue found, including minor and low-confidence candidates. Label severity (`critical`, `major`, `minor`) and confidence (`high`, `medium`, `low`). Steelman and record defeated candidates in `considered_and_defended`; do not silently drop them.

Each actionable finding must include:

- artifact label and tight `file:line` evidence
- failure mechanism and concrete impact
- `minimum_closure_condition` as an end state, not implementation instructions
- `next_authorized_action`
- severity and confidence

Citations must be neutral in tone and decision-sufficient in substance. The argument belongs in the finding/verdict, not the citation.

## Patch and escalation contract

For each accepted finding that is safely closable inside the named target set, patch the working tree directly and do not commit. Prefix each finding, citation, and reported diff section with its target label. Validate the final state after all edits.

The controller's changes, citations, and verdict are claims to adjudicate, not premises to inherit. The home/CA model may accept, modify, or reject every change and owns what is kept.

If a design-level problem cannot be safely closed inside the named scope, return `NEEDS_ARCHITECTURE_PASS`, revert any partial patch for that problem, and return findings only for it. Never leave a partial design workaround in the worktree.

## Existing evidence to inspect, not inherit

Observed before commission:

- focused CI-wiring test: `4 passed`
- ontology checker selftest: `OK`
- ontology strict pre-commit probe: `OK (0 changed markdown files vs origin/main)`; this is only a pre-commit implementation probe, not proof of the eventual committed diff
- pre-push guard selftest: `SELFTEST OK`, including nine launch-failure reasons
- JSON and workflow-YAML parsing: observed successful
- full Forseti suite: `3138 passed, 7 skipped, 66 warnings in 315.34s`
- `git diff --check` and `git diff --cached --check`: observed clean before commission
- GitHub readback observed before commission: main protection required PRs; strict `forseti-harness-tests`; administrators enforced; force pushes and deletion disabled; `auto-merge`, `main-red-alert`, and `pr-risk-router` workflows active; native `allow_auto_merge` remained off

Reinspect the underlying sources and rerun relevant checks. Do not inherit these as truth. GitHub state is read-only evidence: if `gh` access is available, fresh-read it; otherwise mark external-state verification not run.

Minimum post-patch checks:

```powershell
$env:PYTHONDONTWRITEBYTECODE=1
python .agents/hooks/check_ontology_tag_validity.py --selftest
python .agents/hooks/pre_push_guard.py --selftest
python .agents/hooks/check_dcp_receipt_hygiene.py --changed --strict
python -m pytest -p no:cacheprovider -q --basetemp C:\tmp\pytest_ci_hook_review forseti-harness/tests/unit/test_ci_hook_wiring.py
git diff --check
git diff --cached --check
```

Run additional focused tests for any patched behavior. Run the full harness again only if your patch can affect broader behavior; otherwise cite the existing full-suite result as pre-review evidence and state why it was not rerun. A failed check remains visible. Never convert a launch failure, timeout, skipped required check, or unavailable GitHub readback into success.

## Durable output contract

Write the human-readable report to:

`C:\Users\vmon7\Desktop\projects\orca\docs\review-outputs\ci_hooks_hardening_delegated_adversarial_code_review_patch_review_v0.md`

The report must be findings-first and include:

1. `reviewed_by` (operator/tooling-supplied; `unrecorded` if not supplied)
2. `authored_by: OpenAI GPT-5 Codex`
3. preflight receipt and `SOURCE_CONTEXT_READY` / incomplete status
4. findings, including labels, severity, confidence, citations, closure conditions, and next authorized actions
5. patches applied, with a real multiline unified diff grouped by target labels, or `none`
6. validation commands and observed results
7. GitHub external-state readback or explicit not-run status
8. `considered_and_defended`
9. overall advisory verdict and per-target sub-verdicts where materially different
10. residual risks and off-scope flags
11. explicit non-claims: provisional convention; not formal PASS, readiness, approval, merge authority, or proof of correctness
12. an adjudication handoff that points the home/CA model to `.agents/workflow-overlay/communication-style.md` → `Review Adjudication Next Step`

After the final report write, run:

```powershell
python .agents/hooks/check_review_output_provenance.py --strict docs/review-outputs/ci_hooks_hardening_delegated_adversarial_code_review_patch_review_v0.md
```

If the report changes, rerun that gate. Chat output cannot substitute for a failed report write. Return a compact courier with the report path, findings summary, changed source files, validation result, advisory verdict, residual risk, and next authorized action. Do not commit, push, open or merge a PR, change GitHub settings, or decide what is kept.

## Home/CA adjudication contract

The home/CA model must adjudicate the report, findings, diff, verdict, and residuals as claims. It must accept, modify, or reject each material change against citations and intent; close self-closable material issues within its authority and this scope in the same turn; route only issues requiring another review, another lane, architecture, or owner choice; then produce exactly one no-deep-thinking land step for lifecycle/admin work; if a visible active goal, thread operating target, or accepted next objective exists, deep-think 1–5 material moves that best advance it, otherwise record `no_visible_active_goal` and do not invent a roadmap. No delegated change is kept merely because the controller authored it.