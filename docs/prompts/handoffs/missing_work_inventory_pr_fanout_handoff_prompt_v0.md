# Missing Work Inventory And PR Fanout Handoff Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Handoff prompt (missing-work inventory and bounded PR fanout commission)
scope: >
  Commission a GPT-5.3-targeted lane to identify local branches, worktrees, and
  untracked artifacts whose wanted work is not present on verified origin/main,
  reconcile apparent misses caused by the Orca-to-Forseti migration, classify
  them, and open small PRs only for coherent safe units.
use_when:
  - Auditing Forseti (formerly Orca) local work against current origin/main after the owner notices no open PRs.
  - Commissioning bounded PR fanout from many branches, worktrees, and untracked files without bulk-importing scratch or stale work.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/decision-routing.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-of-truth.md
  - docs/decisions/forseti_rename_migration_policy_v0.md
  - docs/workflows/forseti_repo_map_v0.md
stale_if:
  - origin/main advances after this prompt is authored.
  - Local branches, worktrees, or untracked files are created, deleted, pruned, or materially changed.
  - Owner changes the PR fanout policy, PR cap, or disposition rules.
  - A Forseti migration policy or moved-path index changes after this prompt is authored.
branch_or_commit: codex/missing-work-pr-fanout-prompt @ 650e0e81 at authoring; execution must re-check current refs.
```

## Runtime Target

Owner-requested execution target: **GPT-5.3**.

If GPT-5.3 is not available in the execution surface, stop and report
`MODEL_TARGET_UNAVAILABLE` unless the owner explicitly authorizes substitution.
This is a one-off owner runtime request, not model-routing doctrine and not a
recommendation to change Forseti prompt templates.

## Prompt Preflight

`preflight_defaults: docs/prompts/templates/shared/orca_preflight_defaults_v0.md v0 - constants bound; deltas stated below.`

```yaml
forseti_start_preflight:
  agents_read: required on intake
  overlay_read: required on intake
  source_pack: custom (repo-state inventory + S1 map + Forseti rename/migration reconciliation + targeted reads from candidate units)
  edit_permission: implementation-authorized for creating PR branches and commits; read-only until a unit is classified ready_for_pr
  target_scope: >
    Identify local work not present on verified origin/main, classify each unit,
    reconcile Orca-to-Forseti migration aliases, write an inventory report, and
    open bounded PRs only for safe coherent units.
  dirty_state_checked: required on intake
  blocked_if_missing: AGENTS.md, overlay README, decision-routing, source-loading, prompt-orchestration, source-of-truth, Forseti rename migration policy, or git metadata
output_mode: file-write
prompt_artifact_path: docs/prompts/handoffs/missing_work_inventory_pr_fanout_handoff_prompt_v0.md
template_kind: handoff
authorization_basis: owner current-turn request to "find everything that isnt in here (use 5.3) and then spam PR it"; corrected to audit-first bounded fanout
target_files_or_dirs:
  - entire repository branch/worktree/ref state for read-only inventory
  - Forseti migration policy and moved-path indexes for read-only reconciliation
  - docs/hygiene/missing_work_inventory_pr_fanout_report_v0.md
  - per-PR files only after each unit is classified ready_for_pr
branch_or_commit_reference: execution must verify origin/main at start; authoring observed origin/main 650e0e81 and active root 63694997 on codex/ig-reels-capture-spine
dirty_state_allowance: dirty and untracked files are in scope for inventory only; they are not in write scope until classified
controlling_source_state: re-check on intake; authoring lane was clean
repo_map_decision: loaded
repo_map_reason: whole-repo branch/worktree inventory needs current repo navigation and artifact placement rules
doctrine_change_decision: none authorized; any proposed policy/workflow change is owner-gated and must route separately
isolation_decision: use a fresh worktree/branch off verified origin/main for each PR unit; never commit from a dirty source worktree
validation_gates: per-unit checks named below plus fresh durable reads before claiming commit, push, or PR state
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: new_commission
```

## Cynefin Routing

Smallest complete outcome: produce a source-backed inventory of work not present
on verified `origin/main`, classify each candidate, open PRs only for safe
coherent units, and report everything not PR'd with a reason.

Regime: **Mixed / chaotic at intake**.

Why: no open PRs does not prove main contains all work; local main can lag
remote main, local worktrees can contain merged, stale, scratch, or live-lane
work, and the active checkout may be dirty.

Decomposition: **stabilize first, then split and classify**.

Current bottleneck: distinguishing wanted durable work from stale, duplicated,
scratch, protected, generated, already-merged work, or rename/path migration
fallout.

Riskiest assumption: every local delta not on `origin/main` is still desired and
safe to PR.

Secondary risky assumption: a legacy `Orca`, `orca/product`, `docs/product`,
`orca-harness`, `orca_start_preflight`, or lowercase `orca_*` reference is
missing work rather than an intentional compatibility alias, historical
provenance, or already-landed Forseti migration successor.

Stop or pivot condition: a candidate unit cannot be tied to an owning branch,
source path, authoring context, validation path, or safe artifact role; remote
state cannot be verified; a protected path would be touched; or the same change
already appears on main, a closed/merged PR, or a Forseti migration successor.

Allowed next move: non-destructive inventory, classification, report write, then
bounded PR fanout for `ready_for_pr` units only.

Disallowed next move: bulk PR unclassified deltas, merge to main, rewrite
history, delete/prune worktrees, import `_scratch` wholesale, commit generated
data blobs, touch protected/installed skill/plugin roots, or claim PR/push/merge
state without a fresh read.

## Context Observed At Authoring

These are orientation facts only. Re-check them before acting.

- Source workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Prompt authoring worktree: `C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\missing-work-pr-fanout-prompt`
- Prompt authoring branch: `codex/missing-work-pr-fanout-prompt`
- Authoring observed `origin/main`: `650e0e81 docs: migrate ontology filenames to Forseti (#758)`
- Authoring observed active root branch: `codex/ig-reels-capture-spine`
- Authoring observed active root HEAD: `63694997`
- Authoring observed local `main`: `01b20308`, apparently behind `origin/main`
- Authoring observed active root dirty state: many untracked files, including `_scratch/`, `docs/hygiene/**`, `docs/prompts/**`, `docs/research/aphrodite_*`, `docs/workflows/**`, and `worktrees/**`

Interpretation: "no open PRs" can coexist with updated `origin/main` because
PRs may have already merged and closed, another lane may have pushed/merged, or
local `main` may simply be stale relative to `origin/main`.

Migration interpretation: apparent missing work may be caused by the Orca-to-
Forseti rename and path migrations rather than unfinished branches. Treat legacy
Orca names and paths as aliases to reconcile first, not as automatic PR material.

## Required Intake Reads

Read these before classification:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/decision-routing.md`
4. `.agents/workflow-overlay/source-loading.md`
5. `.agents/workflow-overlay/prompt-orchestration.md`
6. `.agents/workflow-overlay/source-of-truth.md`
7. `.agents/workflow-overlay/artifact-folders.md`
8. `docs/decisions/forseti_rename_migration_policy_v0.md`
9. `docs/workflows/forseti_repo_map_v0.md`
10. Conditional migration indexes when a candidate path or diff touches the relevant legacy surface:
    - `docs/migration/repo_structure_spine_first_v0/moved_paths_index.md` for `docs/product/` -> `orca/product/`.
    - `docs/migration/forseti_product_root_migration_v0/moved_paths_index.md` for `orca/product/` -> `forseti/product/`.
    - `docs/migration/forseti_harness_runtime_migration_v0/moved_paths_index.md` for `orca-harness/` -> `forseti-harness/`.
    - `docs/migration/forseti_ontology_filename_migration_v0/moved_paths_index.md` for ontology `orca_*` filename successors.
11. Any candidate unit's nearest owning decision, prompt, review, report, or product source before classifying that unit as PR-ready.

Declare `SOURCE_CONTEXT_READY` only after these reads plus the repo-state
inventory below are complete. If any controlling source is missing, declare
`SOURCE_CONTEXT_INCOMPLETE` and continue only with classifications that do not
depend on the missing source.

## Repo-State Inventory

Run non-destructive commands first. If network is available, start with a remote
refresh; if it is blocked, report `REMOTE_STATE_STALE` and do not open PRs until
remote state is verified or the owner accepts the stale-ref risk.

Suggested commands:

```powershell
git fetch --prune --all
git status --short --branch
git rev-parse --short HEAD
git rev-parse --short origin/main
git log --oneline --decorate -12 --all --simplify-by-decoration
git worktree list --porcelain
git branch --all --no-merged origin/main
git for-each-ref --format="%(refname:short) %(objectname:short) %(committerdate:iso8601) %(subject)" refs/heads refs/remotes/origin
```

For each linked worktree and each local branch that is not merged into verified
`origin/main`, collect:

```powershell
git -C <path> status --short --branch
git -C <path> rev-parse --short HEAD
git -C <path> merge-base --is-ancestor HEAD origin/main
git -C <path> diff --name-status origin/main...HEAD
git -C <path> diff --name-status --find-renames=70% origin/main...HEAD
git -C <path> status --porcelain=v1 --untracked-files=all
```

For the source workspace root, also collect:

```powershell
git status --porcelain=v1 --untracked-files=all
```

If GitHub CLI/app access is available, check closed and merged PR state before
classifying a branch as missing:

```powershell
gh pr list --state all --limit 200 --json number,title,state,headRefName,baseRefName,mergeCommit,updatedAt,url
```

Do not assume "no open PRs" means "no merged PRs" or "all local work is missing."

## Migration-Aware Reconciliation

Before classifying any unit as `ready_for_pr`, run the Forseti migration lens
over its candidate paths and visible prose:

1. Read `docs/decisions/forseti_rename_migration_policy_v0.md` and classify
   legacy references by rename class: live authority/doctrine, current route,
   current product/architecture, compatibility name, historical provenance, or
   scratch/inbox.
2. For any candidate path under `docs/product/`, `orca/product/`,
   `orca-harness/`, `forseti/product/`, `forseti-harness/`, or ontology
   `orca_*` filenames, resolve the path through the relevant moved-path index
   before deciding it is absent from main.
3. If the candidate is only an old path/name and the successor exists on
   verified `origin/main` with equivalent content, classify it as
   `already_on_main_or_closed` or `superseded_or_duplicate`. Do not open a PR.
4. If the old path and successor both exist but differ materially, classify it
   as `needs_source_reconciliation`, name the old/new path pair, and do not PR
   either version until the owning source says which one should survive.
5. Preserve historical provenance and explicit compatibility names by default.
   Do not mass-rename old prompt/review bodies, dated DCP receipts,
   `orca_start_preflight`, `orca_preflight_defaults_v0.md`, lowercase legacy
   filenames, package/import names, or runtime compatibility identifiers unless
   the candidate's owning source explicitly authorizes that compatibility batch.
6. Treat a live authority/doctrine surface that still uses stale Orca language
   as a narrow `needs_source_reconciliation` or `ready_for_pr` candidate only
   after the rename policy says that surface belongs to the live rename class.

## Classification Schema

Write the inventory report to:

`docs/hygiene/missing_work_inventory_pr_fanout_report_v0.md`

Include one row per unit with these fields:

```text
unit_id:
source_kind: branch | worktree | untracked-root | remote-ref | mixed
source_path:
branch:
head:
base_ref:
candidate_paths:
migration_reconciliation:
topic:
classification:
reason:
owner_decision_needed:
pr_plan:
validation_required:
blocked_by:
evidence:
  - command/result or file:line
```

Allowed classifications:

- `ready_for_pr`: coherent, current, source-backed, validation path known, safe to isolate on a new branch from verified `origin/main`.
- `needs_owner_decision`: likely useful but scope, ownership, or desired disposition is ambiguous.
- `needs_source_reconciliation`: candidate conflicts with current source hierarchy, repo map, prompt policy, migration policy, moved-path indexes, or product/doctrine state.
- `superseded_or_duplicate`: already represented on main, in a merged/closed PR, by a newer artifact, or by a Forseti migration successor.
- `scratch_or_non_authoritative`: `_scratch`, `docs/_inbox`, temporary notes, generated experiments, or unowned parked material.
- `unsafe_or_protected`: protected path, installed skill/plugin source, external root, secrets, credentials, destructive migration, or hard-to-reverse action.
- `generated_data_excluded`: raw capture/data-lake/cache/build output that should not be PR'd without a separate data policy decision.
- `already_on_main_or_closed`: verified present on current main, already landed through a closed/merged PR, or present at a migration successor path on verified main.

## PR Fanout Rules

"Spam PR" means move quickly through safe independent units. It does not mean
opening noise PRs.

Initial fanout cap: **5 PRs** in the first execution round. After opening 5, stop
and return the report plus the remaining prioritized `ready_for_pr` queue so the
owner can raise the cap or redirect.

For each `ready_for_pr` unit:

1. Create a fresh branch/worktree off verified `origin/main`.
2. Apply only the files belonging to that coherent unit. Prefer git-native
   patch/cherry-pick when the source is a branch; copy individual files only
   when the source is untracked and the artifact role is clear.
3. Do not mix unrelated worktrees, topics, or artifact families in one PR.
4. Run the unit's validation before commit. At minimum:
   - `python .agents/hooks/check_retrieval_header.py --strict` when adding or materially touching durable docs.
   - `python .agents/hooks/check_prompt_provenance.py <prompt-path>` when adding or materially touching prompt artifacts.
   - `python .agents/hooks/check_placement.py --strict` when adding/moving docs.
   - Any target-specific hook named by the owning source or nearby artifacts.
5. Commit only after validation or a clearly reported validation blocker.
6. Push and open a draft PR unless every required validation is clean and the unit
   is low risk; use a ready PR only when the validation evidence supports it.
7. Before reporting a commit, push, or PR, perform a fresh read of the durable
   target and include the observed branch, commit SHA, PR URL, and validation
   output in the report.

Do not open PRs for:

- Whole `_scratch/`, `docs/_inbox/`, caches, temporary folders, or generated output.
- Raw data-lake blobs, captured media, browser caches, local credentials, or large generated files.
- `.git`, `worktrees/**` as a folder, `.codex/plugins/**`, installed global skills, plugin caches, or external roots.
- Files whose authority would change product, architecture, workflow, validation, review, output, or lifecycle doctrine without an accepted doctrine-change route.
- A branch/worktree whose diff is already on `origin/main` or a merged/closed PR.
- Legacy Orca references or paths that are historical provenance, explicit
  compatibility aliases, or already resolved by a Forseti moved-path index.

## Output Contract

Return a concise chat summary and leave the full durable detail in
`docs/hygiene/missing_work_inventory_pr_fanout_report_v0.md`.

The chat summary must include:

```text
remote_state:
origin_main:
inventory_counts:
  ready_for_pr:
  needs_owner_decision:
  needs_source_reconciliation:
  superseded_or_duplicate:
  scratch_or_non_authoritative:
  unsafe_or_protected:
  generated_data_excluded:
  already_on_main_or_closed:
migration_reconciliation:
  checked_indexes:
  alias_only_or_already_migrated:
  needs_source_reconciliation:
prs_opened:
  - url:
    branch:
    source_unit:
    commit:
    validation:
not_prd_reason:
  - unit_id: reason
next_owner_decision:
```

If no PRs are opened, say so directly and name the blocking class. Do not
substitute a green-sounding closeout for a blocked or stale remote state.

## Non-Claims

This commission does not prove the work is correct, current, merged, accepted,
validated, legally cleared, or product-ready. It only classifies local missing
work against verified main, opens bounded PRs where safe, and records evidence
for anything left out. It does not complete or validate the Orca-to-Forseti
migration; it only prevents migration aliases from being mistaken for PR-ready
missing work.
