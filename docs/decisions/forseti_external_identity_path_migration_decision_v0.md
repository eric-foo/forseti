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

- `eric-foo/orca` can become `eric-foo/forseti` only after the target slug is actually available or an alternate target is chosen; as of 2026-07-04, `eric-foo/Forseti` resolves to a separate public repository (`R_kgDOTMfy1w`), while the live repo remains `eric-foo/orca` (`R_kgDOScCLJQ`).
- The local checkout folder can become `forseti`, but not by renaming the currently active workspace in-place while worktrees and running sessions depend on it. Prefer a fresh clone or a controlled move after active worktrees are closed.
- `forseti/product/`, `orca-harness/`, `orca-product-lead`, `orca_start_preflight`, and `orca-harness-tests` remain compatibility identifiers until their own migration units are planned and validated. The repo-map path has since moved to `docs/workflows/forseti_repo_map_v0.md`, with `docs/workflows/orca_repo_map_v0.md` retained as a compatibility pointer.
- Live human-facing metadata that says Orca is current should be fixed when found. This decision includes one such bounded repair: `orca-harness/pyproject.toml` description now says Forseti while retaining package name `orca-harness`.

## Why

Leaving all repo and folder identity as Orca creates long-term confusion because new operators see the old name in clone URLs, local paths, scripts, and protected-action examples before they see the Forseti authority docs.

## Current External Identity Gate

Observed on 2026-07-04:

```text
gh repo view eric-foo/orca --json name,nameWithOwner,url,id,visibility
{"id":"R_kgDOScCLJQ","name":"orca","nameWithOwner":"eric-foo/orca","url":"https://github.com/eric-foo/orca","visibility":"PUBLIC"}

gh repo view eric-foo/Forseti --json name,nameWithOwner,url,id,visibility
{"id":"R_kgDOTMfy1w","name":"Forseti","nameWithOwner":"eric-foo/Forseti","url":"https://github.com/eric-foo/Forseti","visibility":"PUBLIC"}
```

Status: `BLOCKED_TARGET_SLUG_OCCUPIED` for the named `eric-foo/forseti` target.
Do not update remotes, protected-action repo slug, merge-script defaults, or live
dev docs to `eric-foo/forseti` while the target slug resolves to another
repository. The next owner-gated action is to free `eric-foo/Forseti` or choose
an alternate slug, then re-run the slug probe before any source cutover.

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
| GitHub repository slug | `eric-foo/forseti` | BLOCKED_TARGET_SLUG_OCCUPIED as of 2026-07-04: `gh repo view eric-foo/Forseti` resolves to a separate public repo (`R_kgDOTMfy1w`), while the live repo remains `eric-foo/orca` (`R_kgDOScCLJQ`). | Owner frees `eric-foo/Forseti` or selects another target slug; re-run the GitHub slug probe; then update the hard-coded slug plan. |
| Local checkout folder | `C:\Users\vmon7\Desktop\projects\forseti` | Still recommended, but only as a controlled fresh clone or shutdown/move after active worktrees close; do not rename this active workspace in-place. | Repo slug target selected or deliberately decoupled; active worktrees/sessions closed or a fresh clone path chosen. |
| Remote URL defaults | `https://github.com/eric-foo/forseti.git` | Blocked with repo slug cutover while `eric-foo/Forseti` is occupied. | Update `origin` only after the owner-gated repo rename succeeds; verify `git remote -v`. |
| Protected-action repo slug | `eric-foo/forseti` | Blocked with repo slug cutover; current guard must keep `eric-foo/orca` while that remains the live GitHub repo. | Patch `.agents/hooks/guard_protected_actions.py` only after the external rename succeeds; run selftest and review-routing gate. |
| Merge script default repo | `eric-foo/forseti` | Blocked with repo slug cutover; current script default must keep `eric-foo/orca` while that remains the live GitHub repo. | Patch `.github/scripts/merge-when-green.ps1` only after the external rename succeeds; verify PR commands. |
| Product tree root | `forseti/product/` or `forseti/product/**` | Executed by `docs/decisions/forseti_product_root_migration_decision_v0.md` on the stacked product-root lane. | Moved-path index, repo-map successor/update, overlay/source-loading/checker updates, deletion-evidence handling. |
| Harness root | `forseti-harness/` | Deferred. | Package/import install plan, CI working-directory update, check-name migration, review-routing code-root update, full test run. |
| Package name | `forseti-harness` | Deferred with harness root. | Packaging compatibility plan and downstream install/import check. |
| CI check name | `forseti-harness-tests` | Deferred with harness root or explicit CI lane. | Auto-merge, branch-protection, PR risk router, and docs update. |
| Skill command/path | `forseti-product-lead` | Deferred. | Source and deployment-copy migration, invocation alias/rollback, resolver collision check. |
| Repo map path | `docs/workflows/forseti_repo_map_v0.md` | Executed by `docs/decisions/forseti_repo_map_successor_migration_decision_v0.md`; legacy Orca path retained as a compatibility pointer. | Header index, map freshness checker, source-loading pointers, and live entry references repointed. |
| Start-preflight alias | retire `orca_start_preflight` | Deferred last. | Historical prompt tolerance and hook compatibility decision. |

## What Changes Now

This earlier branch did not rename a root, package, check name, skill ID, repo-map path, remote, or GitHub repo slug. The later product-root migration executes only the product tree root row.

It does fix one live metadata defect:

| File | Change |
| --- | --- |
| `orca-harness/pyproject.toml` | Description now says the deterministic harness is for Forseti, while package name remains `orca-harness`. |

## Owner Gate For Repo Rename

Renaming the GitHub repository is an outward-facing external operation. It should not be performed by an agent as an incidental source edit.

Smallest complete owner-gated repo-identity lane:

1. Owner frees the occupied `eric-foo/Forseti` slug or chooses an alternate target slug.
2. Re-run the GitHub slug probe and stop if the target still resolves to another repository.
3. Owner confirms the final target slug.
4. Rename repo in GitHub settings or with an explicit owner-authorized `gh repo rename <target>` operation.
5. Update local remotes to the renamed repo URL and verify `git remote -v`.
6. Patch hard-coded slug surfaces: `.agents/hooks/guard_protected_actions.py`, `.github/scripts/merge-when-green.ps1`, and live workflow/dev docs that are not historical prompts or review outputs.
7. Verify `gh pr view`, protected-action guard behavior, merge script defaults, and CI.

GitHub usually provides repository redirects after a rename, but this decision does not rely on redirects as the long-term operating state.

## Recommended Sequence

1. Land this decision, metadata-label repair, and the later target-slug blocker update.
2. Resolve the occupied target slug: owner frees `eric-foo/Forseti` or chooses an alternate, then re-probe GitHub before any rename.
3. Run an owner-gated external identity cutover for repo slug plus local folder/remotes.
4. After external identity is stable, decide whether internal compatibility paths still cause enough confusion to justify migration.
5. If yes, migrate `forseti/product/` before `orca-harness/`; the repo-map path successor is handled by `docs/decisions/forseti_repo_map_successor_migration_decision_v0.md`, while the product tree remains the next authority/navigation root.
6. Migrate `orca-harness/`, package name, and CI check name as one runtime lane only after package/install/test and auto-merge impacts are bound.
7. Migrate `orca-product-lead` and retire `orca_start_preflight` only after the roots and repo-map path settle.

## Rejected Paths

| Path | Reason rejected |
| --- | --- |
| Broad word-match rename | Would rewrite historical provenance and compatibility identifiers while leaving path/package behavior uncertain. |
| Rename `orca-harness/` now because the README says Forseti | The root has 1188 tracked files and CI/package/checker dependencies. The README title is already repaired; the root is a compatibility ID. |
| Rename `forseti/product/` now as a docs-only move | Product paths are embedded in overlay, hooks, repo map, source-loading, and product artifacts. It needs moved-path and deletion evidence handling. |
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
    identity may be migrated first under owner gate, while forseti/product/,
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

```yaml
direction_change_propagation:
  doctrine_changed: >
    External repo identity cutover is now explicitly blocked on target-slug
    availability: `eric-foo/Forseti` resolves to a separate public repository as
    of 2026-07-04, so repo/remotes/protected-action/merge-script cutover must not
    proceed until the owner frees that slug or chooses an alternate and the slug
    probe is re-run.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_external_identity_path_migration_decision_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/forseti_repo_map_v0.md
    - .agents/hooks/guard_protected_actions.py
    - .github/scripts/merge-when-green.ps1
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        The current GitHub repo is still `eric-foo/orca`; changing the guard to
        the occupied target slug before the external rename would make protected
        action checks disagree with reality.
    - path: .github/scripts/merge-when-green.ps1
      reason: >
        The merge helper must keep its current repo default until the owner-gated
        GitHub rename actually succeeds.
    - path: repo-structure.yaml
      reason: >
        No local checkout, top-level root, or runtime path changed in this
        blocker update.
  stale_language_search: >
    rg -n "eric-foo/orca|eric-foo/forseti|eric-foo/Forseti|repo slug|gh repo rename|remote URL|merge-when-green"
    docs/decisions/forseti_external_identity_path_migration_decision_v0.md
    docs/workflows/forseti_repo_map_v0.md .agents/hooks/guard_protected_actions.py
    .github/scripts/merge-when-green.ps1 README.md AGENTS.md
  stale_language_search_result: >
    Executed 2026-07-04 in codex/forseti-external-identity-blocker. The live
    repo slug remains in .agents/hooks/guard_protected_actions.py and
    .github/scripts/merge-when-green.ps1 by design; the decision and repo-map
    entries document the target-slug blocker instead of cutting over to the
    occupied Forseti repository.
  non_claims:
    - not validation
    - not readiness
    - not GitHub repo rename execution
    - not local checkout rename execution
    - not path/package migration
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
