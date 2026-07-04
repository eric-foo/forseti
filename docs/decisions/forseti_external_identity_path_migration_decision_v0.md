# Forseti External Identity and Path Migration Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Post-audit decision for Forseti repo identity, local folder, path/package, skill, CI, and repo-map migration sequencing.
use_when:
  - Deciding whether to rename the GitHub repo, local checkout folder, or retained Orca compatibility paths.
  - Preparing a later path/package/CI migration lane after the Forseti authority rename.
  - Checking whether a remaining lowercase Orca identifier is a compatibility surface or a current defect.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_rename_migration_policy_v0.md
  - docs/decisions/forseti_compatibility_migration_boundary_v0.md
  - docs/workflows/forseti_rename_stale_reference_audit_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Start Preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write plus bounded metadata-label repair
  target_scope: Forseti external identity and high-lock-in path/package migration decision
  dirty_state_checked: yes
  blocked_if_missing: docs/workflows/forseti_rename_stale_reference_audit_v0.md
workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\forseti-path-migration-plan
branch: codex/forseti-path-migration-plan
base_commit_observed: 0696c641 docs: bound Forseti rename compatibility batches (#649)
output_mode: file-write
```

## Decision

Proceed with a migration lane, but split it by lock-in.

The next executable migration should be **external identity first**: GitHub repo slug, local checkout naming, and any hard-coded repo slug defaults. Internal root/package/CI/skill migrations remain deferred until a moved-path index and validation plan exist.

This means:

- `eric-foo/orca` can become `eric-foo/forseti`, but that is an external owner-gated operation and must be paired with source updates for repo slug assumptions.
- The local checkout folder can become `forseti`, but not by renaming the currently active workspace in-place while worktrees and running sessions depend on it. Prefer a fresh clone or a controlled move after active worktrees are closed.
- `orca/product/`, `orca-harness/`, `orca-product-lead`, `orca_start_preflight`, and `orca-harness-tests` remain compatibility identifiers until their own migration units are planned and validated. The repo-map path has since moved to `docs/workflows/forseti_repo_map_v0.md`, with `docs/workflows/orca_repo_map_v0.md` retained as a compatibility pointer.
- Live human-facing metadata that says Orca is current should be fixed when found. This decision includes one such bounded repair: `orca-harness/pyproject.toml` description now says Forseti while retaining package name `orca-harness`.

## Why

Leaving all repo and folder identity as Orca creates long-term confusion because new operators see the old name in clone URLs, local paths, scripts, and protected-action examples before they see the Forseti authority docs.

But internal path/package migration is materially larger than external identity migration. The observed blast radius is broad enough that a word-match or single-pass path rename would create fake success:

| Surface | Observed evidence | Migration implication |
| --- | ---: | --- |
| Path/name hits | 1488 paths from `rg --files` path/name scan | Requires moved-path index, not text replacement. |
| `orca-harness` tracked files | 1188 files | Root/package/check-name migration is a runtime/CI lane. |
| `orca/product` tracked files | 297 files | Product-tree migration is smaller than harness migration but still touches source hierarchy and gates. |
| `orca-harness` tracked-file content hits | 971 files | Many docs, hooks, CI, fixtures, and map rows depend on this root. |
| `orca/product` tracked-file content hits | 1239 files | Product-source paths are deeply embedded in overlay, hooks, and product artifacts. |
| `docs/workflows/orca_repo_map_v0.md` hits | 474 files | Repo-map path migration needs checker updates and successor routing. |
| `orca_start_preflight` hits | 539 files | Alias retirement needs prompt/hook/history handling, not a blind rewrite. |
| `orca-harness-tests` hits | 34 files | CI/check-name migration affects auto-merge and branch-protection assumptions. |
| `eric-foo/orca` hits | 84 files | Repo slug cutover is feasible but must update protected-action and script defaults. |

## Architecture Result

```yaml
architecture_result: TARGET_RECOMMENDED
recommended_target: split_external_identity_from_internal_compatibility_paths
subagents_launched: none
source_mode: local directional/adversarial/grounding passes over repo-visible sources
non_claims:
  - not validation
  - not readiness
  - not path/package migration
  - not GitHub repo rename execution
```

Directional case: external identity rename gives the largest reduction in long-term operator confusion with the smallest source-change blast radius.

Adversarial case: renaming `orca/product`, `orca-harness`, package names, CI check IDs, or the repo-map path now would change code roots, hook assumptions, map reachability, package installs, and merge automation in one step.

Grounding case: the repo already has a compatibility policy and audit. The correct next architecture is a two-track migration, not a broad replacement.

## Migration Units

| Unit | Target name | Status | Gate before execution |
| --- | --- | --- | --- |
| GitHub repository slug | `eric-foo/forseti` | Recommended next external identity unit. | Owner confirmation and update plan for hard-coded repo slug assumptions. |
| Local checkout folder | `C:\Users\vmon7\Desktop\projects\forseti` | Recommended after or alongside repo slug cutover. | Do not move active workspaces in-place; use fresh clone or close active worktrees first. |
| Remote URL defaults | `https://github.com/eric-foo/forseti.git` | Coupled to repo slug cutover. | Update `origin` after GitHub slug change; verify `git remote -v`. |
| Protected-action repo slug | `eric-foo/forseti` | Coupled to repo slug cutover. | Patch `.agents/hooks/guard_protected_actions.py`; run selftest if available and review-routing gate. |
| Merge script default repo | `eric-foo/forseti` | Coupled to repo slug cutover. | Patch `.github/scripts/merge-when-green.ps1`; verify PR commands. |
| Product tree root | `forseti/product/` or `forseti/product/**` | Deferred. | Moved-path index, repo-map successor/update, overlay/source-loading/checker updates, deletion-evidence handling. |
| Harness root | `forseti-harness/` | Deferred. | Package/import install plan, CI working-directory update, check-name migration, review-routing code-root update, full test run. |
| Package name | `forseti-harness` | Deferred with harness root. | Packaging compatibility plan and downstream install/import check. |
| CI check name | `forseti-harness-tests` | Deferred with harness root or explicit CI lane. | Auto-merge, branch-protection, PR risk router, and docs update. |
| Skill command/path | `forseti-product-lead` | Deferred. | Source and deployment-copy migration, invocation alias/rollback, resolver collision check. |
| Repo map path | `docs/workflows/forseti_repo_map_v0.md` | Executed by `docs/decisions/forseti_repo_map_successor_migration_decision_v0.md`; legacy Orca path retained as a compatibility pointer. | Header index, map freshness checker, source-loading pointers, and live entry references repointed. |
| Start-preflight alias | retire `orca_start_preflight` | Deferred last. | Historical prompt tolerance and hook compatibility decision. |

## What Changes Now

This branch does not rename a root, package, check name, skill ID, repo-map path, remote, or GitHub repo slug.

It does fix one live metadata defect:

| File | Change |
| --- | --- |
| `orca-harness/pyproject.toml` | Description now says the deterministic harness is for Forseti, while package name remains `orca-harness`. |

## Owner Gate For Repo Rename

Renaming the GitHub repository is an outward-facing external operation. It should not be performed by an agent as an incidental source edit.

Smallest complete owner-gated repo-identity lane:

1. Owner confirms target slug `eric-foo/forseti`.
2. Rename repo in GitHub settings or with an explicit owner-authorized `gh repo rename forseti` operation.
3. Update local remotes to `https://github.com/eric-foo/forseti.git`.
4. Patch hard-coded slug surfaces: `.agents/hooks/guard_protected_actions.py`, `.github/scripts/merge-when-green.ps1`, and live workflow/dev docs that are not historical prompts or review outputs.
5. Verify `gh pr view`, protected-action guard behavior, merge script defaults, and CI.

GitHub usually provides repository redirects after a rename, but this decision does not rely on redirects as the long-term operating state.

## Recommended Sequence

1. Land this decision and metadata-label repair.
2. Run an owner-gated external identity cutover for repo slug plus local folder/remotes.
3. After external identity is stable, decide whether internal compatibility paths still cause enough confusion to justify migration.
4. If yes, migrate `orca/product/` before `orca-harness/`; the repo-map path successor is handled by `docs/decisions/forseti_repo_map_successor_migration_decision_v0.md`, while the product tree remains the next authority/navigation root.
5. Migrate `orca-harness/`, package name, and CI check name as one runtime lane only after package/install/test and auto-merge impacts are bound.
6. Migrate `orca-product-lead` and retire `orca_start_preflight` only after the roots and repo-map path settle.

## Rejected Paths

| Path | Reason rejected |
| --- | --- |
| Broad word-match rename | Would rewrite historical provenance and compatibility identifiers while leaving path/package behavior uncertain. |
| Rename `orca-harness/` now because the README says Forseti | The root has 1188 tracked files and CI/package/checker dependencies. The README title is already repaired; the root is a compatibility ID. |
| Rename `orca/product/` now as a docs-only move | Product paths are embedded in overlay, hooks, repo map, source-loading, and product artifacts. It needs moved-path and deletion evidence handling. |
| Rename local active workspace in-place during this session | Running agents, worktrees, remotes, and absolute-path references can break mid-operation. Use fresh clone or controlled shutdown/move. |

## Non-Claims

- This decision is not validation, readiness, implementation authorization, deployment, GitHub repo rename execution, local folder rename execution, or path/package migration.
- This decision does not claim redirects, branch protection, auto-merge, package installs, or skill resolver behavior will work after a repo rename.
- This decision does not prove every remaining Orca hit is valid.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    After the Forseti rename audit, the next migration architecture splits
    external identity from internal compatibility paths: repo slug/local checkout
    identity may be migrated first under owner gate, while orca/product/,
    orca-harness/, repo-map path, skill IDs, start-preflight alias, and CI check
    names remain deferred migration units until moved-path indexes, validation,
    rollback, and dependency impacts are bound.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - architecture_doctrine
    - validation_philosophy
  controlling_sources_updated:
    - docs/decisions/forseti_external_identity_path_migration_decision_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/skill-adoption.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/decisions/forseti_rename_migration_policy_v0.md
    - docs/decisions/forseti_compatibility_migration_boundary_v0.md
    - docs/workflows/forseti_rename_stale_reference_audit_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - repo-structure.yaml
    - .github/workflows/ci.yml
    - .github/workflows/auto-merge.yml
    - .github/scripts/merge-when-green.ps1
    - .agents/hooks/guard_protected_actions.py
    - orca-harness/pyproject.toml
  intentionally_not_updated:
    - path: docs/decisions/forseti_compatibility_migration_boundary_v0.md
      reason: >
        It remains accurate for the already-completed Step 4/5 fused lane and
        explicitly says deeper migration requires a separate accepted plan; this
        new decision is that next-phase planning record, not a replacement edit.
    - path: repo-structure.yaml
      reason: >
        Internal roots remain compatibility paths in this branch; changing the
        machine structure map belongs to a future moved-path migration.
    - path: .github/workflows/ci.yml
      reason: >
        CI check name and working directory remain compatibility identifiers
        until the harness root/package migration is accepted.
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        The GitHub repo slug has not been externally renamed yet; changing the
        protected-action repo slug before the external cutover would make the
        guard disagree with the current repository.
  stale_language_search: >
    git grep -l -F -- orca-harness; git grep -l -F -- orca/product; git grep -l
    -F -- docs/workflows/orca_repo_map_v0.md; git grep -l -F -- eric-foo/orca
  stale_language_search_result: >
    Executed 2026-07-04 in codex/forseti-path-migration-plan. Counts: 971
    tracked files mention orca-harness, 1239 mention orca/product, 474 mention
    docs/workflows/orca_repo_map_v0.md, and 84 mention eric-foo/orca. These are
    migration blast-radius evidence, not defects by themselves.
  non_claims:
    - not validation
    - not readiness
    - not path/package migration
    - not GitHub repo rename execution
```