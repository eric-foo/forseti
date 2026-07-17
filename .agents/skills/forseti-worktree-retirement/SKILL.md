---
name: forseti-worktree-retirement
description: "Audit, classify, and safely retire Forseti Git worktrees when the user asks to inspect, reduce, close, delete, drop, or clean up stale, merged, Codex, or Claude worktrees. Use for target lane counts or age thresholds, but treat both only as sorting signals. Do not trigger for ordinary branch cleanup, artifact deletion inside a worktree, implementation landing, or general repository hygiene without a worktree-retirement request."
---

# Forseti Worktree Retirement

## Status and authority

Use this Forseti-local candidate as the project-specific retirement layer over
`workflow-repo-hygiene`. It is not repository authority and does not grant
deletion, branch, remote, merge, validation, readiness, or deployment authority.

Load and obey:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`, especially
  the live worktree-cleanup rule

Use `docs/decisions/deletion_evidence_doctrine_v0.md` only when the proposed
repository diff deletes a governed artifact. Removing a worktree registration
alone is not such an artifact deletion.

## Failure to prevent

Prevent deletion of an active, reused, dirty, unpushed, or uniquely valuable
worktree merely because it is old, related to a merged PR, or above the owner's
desired lane count.

Success is the number safely retired. It is not reaching the requested count.

## Bind authority before classifying

Separate these permissions; never infer one from another:

1. inspect and classify worktrees;
2. remove clean, proven-landed worktrees;
3. discard surfaced dirty or unique payloads;
4. delete named local branches;
5. delete named remote branches.

A request to close worktrees grants neither branch nor remote deletion. A
general target such as "leave ten lanes" does not grant dirty-payload discard.

Protect the current worktree, the integration-base worktree, `main`, named seal
or protected lanes, open-PR lanes, and every known-active or unknown-owner lane.

## Take one fresh live snapshot

1. Resolve the repository root, integration base, current worktree, and allowed
   worktree roots.
2. Reuse the project classifier:

   ```powershell
   pwsh .github/scripts/lane-health-check.ps1 `
     -RepoPath <repo-root> -Fetch -ClassifyWorktrees -Json
   ```

   Treat `cleanupCandidate` as volatile evidence, not deletion authority.
3. Read `git worktree list --porcelain` and the complete staged, unstaged, and
   untracked status of every candidate.
4. Inspect current task/controller state when the runtime exposes it. A task
   using or naming a worktree is a liveness veto until released.
5. Record age only as a prioritization hint.

The classifier deliberately leaves many lanes `unknown`. Resolve only the
bounded candidates needed for the requested cleanup. For detached, renamed, or
squash-merged lanes, use current PR metadata and content evidence. Distinguish:

- exact current HEAD of a merged PR;
- patch/content equivalence to the integration base;
- a commit merely associated with a merged PR;
- a merged base with later working-tree changes;
- an open or closed-unmerged PR;
- unique or conflicting evidence.

Graph ancestry and `git cherry` are insufficient alone under squash merges.
When landing signals conflict, preserve the lane.

## Classify four dimensions independently

For every candidate record:

```yaml
liveness: current | known_active | inactive | unknown
payload: clean | already_landed | superseded | explicitly_rejected | spurious | unique | unknown
integration: graph_merged | patch_equivalent | merged_pr_exact_head | merged_pr_related_only | open_pr | unique | unknown
authority: inspect_only | clean_landed_class | named_dirty_discard | named_local_branch_delete | named_remote_delete
decision: retire | preserve | adjudicate | drifted
```

`merged_pr_related_only` is not landing proof. `not load-bearing` is a conclusion,
not evidence; bind it to `already_landed`, `superseded`,
`explicitly_rejected`, or `spurious` with a cited current source.

Treat every untracked file as authored until provenance or explicit disposition
proves otherwise. A merged base does not cover its dirty working-tree payload.

## Revalidate immediately before mutation

Freshly re-read each exact candidate:

- canonical path and registration;
- branch or detached state and exact HEAD;
- integration-base HEAD;
- staged, unstaged, and untracked status;
- open PR and current-task evidence;
- the evidence class that authorized retirement.

Use these values as the candidate fingerprint. Any change invalidates the
decision: skip it and reclassify from live state. Reused paths are new lanes,
even when the path was previously safe.

## Retire conservatively

- Use non-force `git worktree remove <path>` for clean, proven-disposable
  candidates.
- Treat non-force refusal as evidence. Do not add force merely to overcome a
  lock, dirty state, untracked content, or an ownership ambiguity.
- Use dirty force-removal only after surfacing the exact payload and receiving
  explicit discard authority for the named worktree or the exact adjudicated
  class. Process dirty discards one at a time.
- A clean unique worktree may be removed after explicit named discard, but its
  local branch remains unless local-branch deletion was also authorized.
- Never delete a remote branch without separately named remote authority.
- Never drop or rewrite stashes as worktree cleanup.

If a batch partially mutates before failing, inspect every intended target
before one bounded retry. Do not assume the remaining targets were untouched or
removed.

## Verify registry and filesystem separately

After every removal pass, freshly verify:

1. the worktree registration is absent;
2. the directory is absent, empty-and-locked, or still contains residue;
3. branches and stashes have the authorized final state;
4. the final live worktree count from a new inventory.

An unregistered worktree with a Windows-locked directory is closed in Git but
not deleted from disk. Report the residue exactly. Treat reserved device names
such as `nul` as a Windows filesystem edge case; remove only the exact surfaced
entry, then stop if the empty directory remains locked.

Concurrent tasks may create or reuse worktrees during cleanup. Never derive the
final count arithmetically.

## Return a compact receipt

```yaml
worktree_retirement:
  snapshot:
    base:
    base_head:
    observed_count:
  retired:
    - path:
      evidence_class:
      removal_mode: non_force | explicit_dirty_discard
      registry_absent:
      directory_absent:
      residue:
  preserved:
    - path:
      reason:
  drifted:
    - path:
      changed_field:
  branches:
    local_deleted:
    remote_deleted:
  stashes_changed:
  final_live_count:
  non_claims:
    - not validation
    - not readiness
    - not proof that preserved work should land
```

## Candidate metadata

- Source boundary: Forseti-local `.agents` source only.
- Positive triggers: audit/check worktrees; eliminate stale worktrees; close
  merged worktrees; reduce to a target lane count; drop a named worktree.
- Negative triggers: ordinary branch cleanup, in-worktree artifact deletion,
  implementation landing, or general repository cleanup.
- Collision check: no same-name project, user, plugin-cache, or resolver-visible
  skill observed on 2026-07-18.
- Rollback: remove this candidate source and its entry from
  `.agents/workflow-overlay/skill-adoption.md`; do not modify generic plugin,
  user-level, installed-cache, or external skill source.
