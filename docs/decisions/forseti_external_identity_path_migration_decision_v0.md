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
  - docs/workflows/forseti_post_harness_migration_status_v0.md
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

## Current Status Note

This decision remains authoritative for sequencing Forseti external identity
and retained compatibility paths. The external GitHub identity gate is now
closed: on 2026-07-05, the separate web repo moved from `eric-foo/Forseti` to
`eric-foo/ForsetiWeb`, and this repository moved from `eric-foo/orca` to
`eric-foo/forseti`.

Observed current state after the owner-authorized rename:

- live repo: `eric-foo/forseti` (`R_kgDOScCLJQ`)
- web repo: `eric-foo/ForsetiWeb` (`R_kgDOTMfy1w`)
- local `origin`: `https://github.com/eric-foo/forseti.git`
- fresh local main-repo clone: `C:\Users\vmon7\Desktop\projects\forseti`
  on `main`, tracking `https://github.com/eric-foo/forseti.git`
- local web-repo checkout: `C:\Users\vmon7\Desktop\projects\ForsetiWeb`,
  tracking `https://github.com/eric-foo/ForsetiWeb.git`
- old GitHub slugs may redirect, but they are no longer canonical.

The legacy active workspace path remains
`C:\Users\vmon7\Desktop\projects\orca` until active worktrees and running
sessions can be closed or deliberately migrated. Its internal
migration-unit table is superseded in part. Since this record landed, the
product root, repo-map path, harness root, harness distribution label, harness
CI check, and product-lead skill identity have all migrated to Forseti naming.
Use `docs/workflows/forseti_post_harness_migration_status_v0.md` for the
current migration status ledger.

## Decision

Proceed with a migration lane, but split it by lock-in.

The external GitHub identity, hard-coded repo slug defaults, product root, repo-map path, harness root, harness distribution label, CI check identity, and product-lead skill identity have now moved to Forseti naming. Remaining high-lock-in or compatibility surfaces should continue by separate bounded lanes, not word-match replacement.

This means:

- `eric-foo/orca` became `eric-foo/forseti` on 2026-07-05 after the occupied target was freed by moving the separate web repo from `eric-foo/Forseti` to `eric-foo/ForsetiWeb`; the old Orca slug is retained only as redirect/provenance.
- The local checkout folder can become `forseti`, but not by renaming the currently active workspace in-place while worktrees and running sessions depend on it. Prefer a fresh clone or a controlled move after active worktrees are closed.
- `forseti/product/`, `docs/workflows/forseti_repo_map_v0.md`, `forseti-harness/`, `forseti-harness`, `forseti-harness-tests`, and `forseti-product-lead` are current live identities. Legacy `docs/workflows/orca_repo_map_v0.md` and `/orca-product-lead` remain compatibility pointers/wrappers; `orca_start_preflight` remains a deferred legacy alias.
- Live human-facing metadata that says Orca is current should be fixed when found, but only inside a classified migration unit with validation evidence.

## Why

Leaving all repo and folder identity as Orca creates long-term confusion because new operators see the old name in clone URLs, local paths, scripts, and protected-action examples before they see the Forseti authority docs.

## External Identity Gate

Historical blocker observed on 2026-07-04:

```text
gh repo view eric-foo/orca --json name,nameWithOwner,url,id,visibility
{"id":"R_kgDOScCLJQ","name":"orca","nameWithOwner":"eric-foo/orca","url":"https://github.com/eric-foo/orca","visibility":"PUBLIC"}

gh repo view eric-foo/Forseti --json name,nameWithOwner,url,id,visibility
{"id":"R_kgDOTMfy1w","name":"Forseti","nameWithOwner":"eric-foo/Forseti","url":"https://github.com/eric-foo/Forseti","visibility":"PUBLIC"}
```

That blocker is superseded by the 2026-07-05 closeout:

```text
gh repo view eric-foo/forseti --json id,name,nameWithOwner,url,visibility
{"id":"R_kgDOScCLJQ","name":"forseti","nameWithOwner":"eric-foo/forseti","url":"https://github.com/eric-foo/forseti","visibility":"PUBLIC"}

gh repo view eric-foo/ForsetiWeb --json id,name,nameWithOwner,url,visibility
{"id":"R_kgDOTMfy1w","name":"ForsetiWeb","nameWithOwner":"eric-foo/ForsetiWeb","url":"https://github.com/eric-foo/ForsetiWeb","visibility":"PUBLIC"}

git remote -v
origin  https://github.com/eric-foo/forseti.git (fetch)
origin  https://github.com/eric-foo/forseti.git (push)
```

Status: `EXECUTED_EXTERNAL_IDENTITY_CUTOVER` for the named
`eric-foo/forseti` target. Live source defaults may now use the new slug.

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

## Initial Architecture Result

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
| GitHub repository slug | `eric-foo/forseti` | Executed 2026-07-05: repo ID `R_kgDOScCLJQ` now resolves as `eric-foo/forseti`; the separate web repo ID `R_kgDOTMfy1w` now resolves as `eric-foo/ForsetiWeb`. | Use `eric-foo/forseti` in live defaults; keep old slug references only as historical/provenance or redirect-tolerant compatibility. |
| Local checkout folder | `C:\Users\vmon7\Desktop\projects\forseti` | Executed as a controlled fresh clone on 2026-07-05; the legacy active workspace remains under `C:\Users\vmon7\Desktop\projects\orca` while its active worktrees/sessions remain open. | Use the fresh clone for new main-repo sessions; later close or deliberately migrate the legacy workspace. |
| Remote URL defaults | `https://github.com/eric-foo/forseti.git` | Executed for this checkout: `origin` points to `https://github.com/eric-foo/forseti.git`. | Other clones should run `git remote set-url origin https://github.com/eric-foo/forseti.git` and verify `git remote -v`. |
| Protected-action repo slug | `eric-foo/forseti` | Executed in the external-identity source patch: guard default is now `eric-foo/forseti`; `FORSETI_GITHUB_REPOSITORY` remains an override. | Run selftest and review-routing gate. |
| Merge script default repo | `eric-foo/forseti` | Executed in the external-identity source patch: merge helper fallback is now `eric-foo/forseti`; `FORSETI_GITHUB_REPOSITORY` remains an override. | Verify PR command behavior and branch-protection assumptions during normal landing checks. |
| Product tree root | `forseti/product/` or `forseti/product/**` | Executed by `docs/decisions/forseti_product_root_migration_decision_v0.md` on the stacked product-root lane. | Moved-path index, repo-map successor/update, overlay/source-loading/checker updates, deletion-evidence handling. |
| Harness root | `forseti-harness/` | Deferred. | Package/import install plan, CI working-directory update, check-name migration, review-routing code-root update, full test run. |
| Package name | `forseti-harness` | Deferred with harness root. | Packaging compatibility plan and downstream install/import check. |
| CI check name | `forseti-harness-tests` | Deferred with harness root or explicit CI lane. | Auto-merge, branch-protection, PR risk router, and docs update. |
| Skill command/path | `forseti-product-lead` | Executed by the skill identity lane: primary skill source/deployment copies moved to `forseti-product-lead`; `/orca-product-lead` remains a compatibility wrapper. | Keep wrapper for one transition window; resolver activation in already-running sessions is not claimed. |
| Repo map path | `docs/workflows/forseti_repo_map_v0.md` | Executed by `docs/decisions/forseti_repo_map_successor_migration_decision_v0.md`; legacy Orca path retained as a compatibility pointer. | Header index, map freshness checker, source-loading pointers, and live entry references repointed. |
| Start-preflight alias | retire `orca_start_preflight` | Deferred last. | Historical prompt tolerance and hook compatibility decision. |

## What Changes Now

This closeout branch updates external identity source defaults and live docs
only. It does not rename a root, package, check name, skill ID, or start-
preflight alias.

Compatibility prep addendum (2026-07-04) is now promoted: the protected-action
guard and human merge helper default to `eric-foo/forseti` while still accepting
`FORSETI_GITHUB_REPOSITORY` as an override.

The original decision also fixed one live metadata defect:

| File | Change |
| --- | --- |
| `orca-harness/pyproject.toml` | Description now says the deterministic harness is for Forseti, while package name remains `orca-harness`. |

## Owner Gate For Repo Rename

Renaming the GitHub repository is an outward-facing external operation. It
should not be performed by an agent as an incidental source edit. The owner gate
closed on 2026-07-05 by explicit instruction: name the separate web repository
`ForsetiWeb`, then name this repository `forseti`.

Smallest complete owner-gated repo-identity lane status:

1. Free the occupied `eric-foo/Forseti` slug by renaming the separate web repo to `eric-foo/ForsetiWeb`: executed 2026-07-05.
2. Rename this repository from `eric-foo/orca` to `eric-foo/forseti`: executed 2026-07-05.
3. Update local remotes to the renamed repo URL and verify `git remote -v`: executed for this checkout.
4. Patch hard-coded slug surfaces: `.agents/hooks/guard_protected_actions.py`, `.github/scripts/merge-when-green.ps1`, and live workflow/dev docs that are not historical prompts or review outputs: this source patch.
5. Verify `gh pr view`, protected-action guard behavior, merge script defaults, and CI: normal landing checks for this source patch.

GitHub usually provides repository redirects after a rename, but this decision does not rely on redirects as the long-term operating state.

## Recommended Sequence

1. Landed the initial decision, metadata-label repair, and target-slug blocker update.
2. Executed the owner-gated external GitHub identity cutover on 2026-07-05: web repo to `eric-foo/ForsetiWeb`, this repo to `eric-foo/forseti`.
3. Land this source cutover patch for hard-coded slug defaults and live docs.
4. Fresh local main-repo clone created at `C:\Users\vmon7\Desktop\projects\forseti`; later close or deliberately migrate the legacy active `C:\Users\vmon7\Desktop\projects\orca` workspace when its worktrees/sessions are no longer needed.
5. After external identity is stable, decide whether internal compatibility paths still cause enough confusion to justify migration.
6. If yes, migrate `forseti/product/` before `orca-harness/`; the repo-map path successor is handled by `docs/decisions/forseti_repo_map_successor_migration_decision_v0.md`, while the product tree remains the next authority/navigation root.
7. Migrate `orca-harness/`, package name, and CI check name as one runtime lane only after package/install/test and auto-merge impacts are bound.
8. Product-lead skill ID migrated to `forseti-product-lead`; retire `orca_start_preflight` only after prompt/history consumers are classified.

## Rejected Paths

| Path | Reason rejected |
| --- | --- |
| Broad word-match rename | Would rewrite historical provenance and compatibility identifiers while leaving path/package behavior uncertain. |
| Rename `orca-harness/` now because the README says Forseti | The root has 1188 tracked files and CI/package/checker dependencies. The README title is already repaired; the root is a compatibility ID. |
| Rename `forseti/product/` now as a docs-only move | Product paths are embedded in overlay, hooks, repo map, source-loading, and product artifacts. It needs moved-path and deletion evidence handling. |
| Rename local active workspace in-place during this session | Running agents, worktrees, remotes, and absolute-path references can break mid-operation. Use fresh clone or controlled shutdown/move. |

## Non-Claims

- This closeout records the observed GitHub repo rename and local `origin` cutover, but is not validation, readiness, implementation authorization, deployment, local folder rename execution, or path/package migration.
- This decision does not claim redirects, branch protection, auto-merge, package installs, or skill resolver behavior will work after a repo rename.
- This decision does not prove every remaining Orca hit is valid.

## Direction Change Propagation

The 2026-07-04 blocker receipt below is historical and superseded by the 2026-07-05 external identity closeout receipt.


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
  intentionally_updated_with_compatibility_indirection:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        The current GitHub repo is still `eric-foo/orca`, so the guard keeps that
        default while accepting `FORSETI_GITHUB_REPOSITORY` as the future cutover
        knob after the owner-gated external rename succeeds.
    - path: .github/scripts/merge-when-green.ps1
      reason: >
        The human merge helper keeps the current repo default but can read
        `FORSETI_GITHUB_REPOSITORY`, avoiding a source patch during the rename-day
        operational window.
  intentionally_not_updated:
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

```yaml
direction_change_propagation:
  doctrine_changed: >
    External repo identity cutover executed: the separate web repo moved from
    `eric-foo/Forseti` to `eric-foo/ForsetiWeb`, this repository moved from
    `eric-foo/orca` to `eric-foo/forseti`, local `origin` now uses the Forseti
    URL, and live protected-action/merge-helper defaults now use
    `eric-foo/forseti` while internal compatibility roots remain deferred.
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
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
    - docs/decisions/forseti_harness_identity_migration_plan_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - .agents/hooks/guard_protected_actions.py
    - .github/scripts/merge-when-green.ps1
    - docs/decisions/dcp_receipts_archive_v0.md
  intentionally_not_updated:
    - path: repo-structure.yaml
      reason: >
        No local top-level runtime root or checked-in package path changed in
        this external identity cutover.
    - path: .github/workflows/ci.yml
      reason: >
        CI check-name and harness working-directory migration remain deferred;
        this patch changes only repo slug defaults and docs.
    - path: historical prompts, reviews, and hygiene packets
      reason: >
        Old `eric-foo/orca` references in provenance artifacts are historical
        evidence, not live operating defaults.
  stale_language_search: >
    rg -n "eric-foo/orca|eric-foo/forseti|eric-foo/Forseti|eric-foo/ForsetiWeb|BLOCKED_TARGET_SLUG_OCCUPIED"
    .agents/hooks/guard_protected_actions.py .github/scripts/merge-when-green.ps1
    docs/decisions/forseti_external_identity_path_migration_decision_v0.md
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    docs/decisions/overlay_enforcement_placement_classification_v0.md
    docs/decisions/forseti_harness_identity_migration_plan_v0.md
    docs/workflows/forseti_post_harness_migration_status_v0.md
    docs/workflows/forseti_repo_map_v0.md AGENTS.md README.md
  stale_language_search_result: >
    Executed 2026-07-05 in codex/forseti-external-identity-cutover. Live
    default hits in the checked source surfaces are `eric-foo/forseti` in
    .agents/hooks/guard_protected_actions.py and .github/scripts/merge-when-green.ps1.
    Remaining `eric-foo/orca` and `eric-foo/Forseti` hits are confined to this
    decision's historical/current-status evidence, the superseded 2026-07-04
    blocker receipt, the post-harness status row, and the repo-map execution
    record; no checked live default retained `eric-foo/orca`.
  non_claims:
    - not validation
    - not readiness
    - not local checkout folder rename execution
    - not path/package migration
```
Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
