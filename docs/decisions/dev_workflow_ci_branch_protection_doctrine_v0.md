# Dev-Workflow CI + Branch-Protection Doctrine v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: Orca developer-workflow doctrine — CI test gate, branch protection on main, per-lane PR flow, auto-merge, and rebase cadence.
use_when:
  - Opening, merging, or gating a change to Orca's main branch.
  - Setting up or changing CI, branch protection, or the per-lane PR workflow.
  - Onboarding a new lane or worktree to the merge process.
authority_boundary: retrieval_only
branch_or_commit: established off main @ a4af372
open_next:
  - .github/workflows/ci.yml
  - .agents/workflow-overlay/safety-rules.md
```

## Status

Accepted 2026-06-09 (owner sign-off, eric-foo); amended 2026-06-09 to record the enforcement outcome.

- **Live:** CI (`.github/workflows/ci.yml`) runs the orca-harness suite on every `pull_request` and
  on `push` to `main`; verified green on both triggers (see Enforcement status).
- **Blocked:** the server-side hard merge gate (branch protection / rulesets) and `allow_auto_merge`
  are **not available** on this repository — it is private on a free plan, and GitHub returns HTTP
  403 ("Upgrade to GitHub Pro or make this repository public") for both classic branch protection
  and rulesets. They are **not applied**.
- **Interim (owner-selected):** keep CI plus a *merge-when-green* flow under **structure B**
  (Decision item 7): agents prep green PRs but do **not** self-merge — a human/authorized action
  lands to `main`. This is now enforced by the enforcement lane's protected-action guard (it blocks
  an agent's `gh pr merge` → `main`), not discipline alone. The server-side hard gate (items 2 and 4)
  is the deferred target end-state, unblocked only by a GitHub Pro/Team upgrade or making the repo
  public.

This record does not assert that any server-side gate is active. It is not.

## Context

- `main` had no CI: nothing validated commits automatically, so a green check could not gate merges.
- PR #1 reconciled a 28-commit, multi-workstream branch (`ecr-sp3-timing-deriver-slice1`) in one
  batch and was **closed unmerged** — too large and conflicting to land safely as one unit.
- Adopted pattern instead: small, focused, **per-lane PRs off `main`**, each merged when green.
- Lanes run concurrently via branches plus git worktrees, with a goal of eventually-unattended
  (overnight) merging.

## Decision

1. **CI.** A GitHub Actions workflow (`.github/workflows/ci.yml`) runs the orca-harness test suite
   on every `pull_request` and on `push` to `main`: Ubuntu, Python 3.12, `pip install -e .`
   (orca-harness core dependencies only) plus a pinned `pytest`, then `python -m pytest` from
   `orca-harness/`. Single target — no version matrix, no path-filter, no dependency caching.
2. **Branch protection on `main`** (TARGET — deferred; blocked on this private+free repo, see
   Status). When enabled it requires:
   - the `orca-harness-tests` status check to pass;
   - a pull request before merging (`required_approving_review_count: 0`; under this *server-gated
     target* a solo lane could self-merge once green — but the current interim uses structure B
     (item 7), where a human lands to `main`);
   - `strict: false` (a branch need not be up-to-date with `main` before merging);
   - `enforce_admins: false` (the owner retains an emergency override).
3. **Per-lane PR flow.** Each lane branches off `main`, works in its own branch/worktree, and opens
   one focused PR. No multi-workstream mega-batches (the PR #1 lesson).
4. **Auto-merge** (TARGET — deferred; blocked on this private+free repo). When available, repo
   `allow_auto_merge` lets a lane set a PR to land the moment CI is green (unattended/overnight).
   `delete_branch_on_merge` **is** enabled now (it is not plan-gated); merged head branches are
   auto-deleted.
5. **Merge method.** Lane PRs squash-merge by default — one tidy commit per lane on `main`. Other
   methods remain available; squash is the documented default.
6. **Rebase cadence.** Each lane keeps its branch reasonably current with `main` (rebase or merge
   `main`) to limit semantic drift before merging. When the hard gate is enabled it will use
   `strict: false`, so this stays a lane responsibility rather than a server requirement.
7. **Interim enforcement — structure B (merge-when-green, human-landed).** Until a server-side gate
   is available, agents **prepare** green PRs — push their own lane branch, open the PR, confirm the
   `orca-harness-tests` check is green — but do **not** self-merge to `main`. A **human or otherwise
   authorized action lands the PR to `main`**, and only when green. This is now **enforced**, not
   discipline alone: the enforcement lane's protected-action guard
   (`.agents/hooks/guard_protected_actions.py`) blocks an agent's `gh pr merge` → `main`, push to
   `main`, and force-push, while allowing a benign lane-branch push — so the human is the gate on the
   one irreversible step. **This supersedes the earlier "a solo lane self-merges once CI is green"
   wording**, written before the guard existed. The helper `.github/scripts/merge-when-green.ps1` is
   the **human's** green-check-then-merge tool (run it to verify green and land); agents must **not**
   use it to self-merge — it wraps `gh pr merge`, so an agent running it would bypass the guard, which
   structure B forbids.

## Why core-only CI (evidence)

main's full suite is green with **no optional extras installed** — a fresh virtualenv holding only
`pydantic` + `PyYAML` + `pytest` (no `playwright`, no `cloakbrowser`):

```
243 passed, 1 skipped in 29.44s   (exit 0)
```

The browser and `cloakbrowser` capture paths are decoupled by design: `*_no_runtime_imports`
contract tests assert the adapters import with no `playwright`/`cloakbrowser`/`requests`/etc., and
the snapshot tests drive fake engines rather than the real backends. So CI needs no extras, and a
path-filter is deliberately avoided (a filtered required check can strand docs-only PRs in a
permanent "pending" state and block merges). `pytest` is pinned (`==9.0.3`, the version verified in
the probe) so an upstream pytest release cannot silently break CI overnight. This evidence is
re-derivable and is re-run by CI on every PR; it is not a self-asserted pass.

## Explicitly not chosen

- **Version matrix** — single supported target (Python 3.12); revisit if Orca supports more runtimes.
- **Path-filter** — would risk a stuck required check on docs-only PRs.
- **Dependency caching** — install plus a ~30s suite is fast enough; add only if runs slow.
- **Extras in CI** — the suite is green without them; if a future lane legitimately needs an extra to
  test something, that is a separate, explicit CI extension (for example, an added job), not a
  silent change to this contract.

## Enforcement status (2026-06-09)

1. **CI — done & verified.** `.github/workflows/ci.yml` merged to `main` (PR #3, squash `2611995`).
   Verified green on both triggers: `pull_request` (run 27150529791) and `push` to `main`
   (run 27151263680); core-only suite 243 passed / 1 skipped.
2. **Hard gate — attempted, blocked.** Classic branch protection
   (`PUT .../branches/main/protection`) and a repository ruleset (`POST .../rulesets`) both returned
   HTTP 403 (private repo on a free plan). `allow_auto_merge` could not be enabled (stayed `false`).
   `delete_branch_on_merge` was enabled. The exact commands are preserved with the lane for re-run
   after an upgrade or visibility change.
3. **Interim adopted.** Owner selected CI + merge-when-green discipline (Decision item 7); the hard
   gate stays the deferred target.

## Non-claims

- CI green is a test-suite signal only — **not** product, runtime, ECR/Cleaning/Judgment, or
  judgment-quality readiness, and not deployment.
- This doctrine does **not** grant any lane blanket commit/push/PR authority; the per-turn or
  accepted-handoff authorization requirement in `.agents/workflow-overlay/safety-rules.md` still
  applies.
- The interim merge-when-green discipline is a process commitment, **not** a server-enforced gate;
  its presence does not prove it is followed or that any merge actually passed CI.
- Not validation, readiness, or acceptance of any lane's content beyond "the test suite passed."

```yaml
direction_change_propagation:
  doctrine_changed: >
    Orca now has a developer-workflow doctrine: CI runs the orca-harness test suite on every PR and
    push to main (live), behind a per-lane PR off main with a squash default and a rebase cadence.
    The server-side hard merge gate (branch protection / rulesets) and auto-merge are the deferred
    target — blocked on this private+free repo (HTTP 403) — so interim enforcement is a
    merge-when-green discipline until a GitHub Pro/Team upgrade or public visibility unblocks the gate.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        Its rule "do not commit, push, configure remotes, or create pull requests unless explicitly
        authorized" is unchanged. This doctrine defines the merge gate and flow for when a lane is
        authorized; it does not grant standing commit/push/PR authority.
    - path: AGENTS.md
      reason: >
        The behavior kernel and authorization boundaries are unchanged; this is a decision record,
        not a kernel rule, and AGENTS.md already routes durable doctrine into docs/decisions and the
        overlay.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The repo map is clean on main but carries uncommitted edits in the concurrent ecr lane;
        adding a pointer now would create a cross-lane merge conflict. The record lives in the
        canonical docs/decisions/ folder and is discoverable there. A one-line pointer can be added
        in a later turn once the repo-map lane settles.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Source hierarchy and the propagation contract are unchanged; this record is a downstream
        decision, not an overlay-authority or hierarchy change. The same cross-lane-dirty caution as
        the repo map applies to its Known Source Documents list.
  stale_language_search: >
    rg -i -n "branch protection|github/workflows|github actions|required status check|auto.?merge|merge gate|continuous integration|enforce_admins|ci\.yml|status check"
    .agents docs   (run against main's content in the worktree before first landing this record)
  stale_language_search_result: >
    Executed 2026-06-09. No prior CI, GitHub Actions, branch-protection, required-status-check,
    auto-merge, or merge-gate doctrine exists in .agents/ or docs/. The only two hits are unrelated:
    a "status check" cell in a fixture-receipt review table and a "status checks" mention meaning
    `git status` in orca_bootstrap_record.md. This confirms the record is additive and forks no
    existing rule. The 2026-06-09 amendment corrects only this record's own enforcement statements
    and adds no doctrine vocabulary that conflicts with another surface.
  non_claims:
    - not validation
    - not readiness
    - not product, runtime, or judgment-quality readiness
    - not deployment
    - not blanket commit/push/PR authorization
    - the interim discipline is not a server-enforced gate
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    The merge-when-green interim is amended to structure B: agents prepare green PRs but do not
    self-merge to main; a human or otherwise authorized action lands to main, now enforced by the
    enforcement lane's protected-action guard (it blocks an agent's gh pr merge -> main and allows a
    benign lane-branch push). This supersedes the prior "a solo lane self-merges once CI is green"
    wording, and re-scopes .github/scripts/merge-when-green.ps1 as the human's check-then-merge tool,
    not an agent self-merge path.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - .github/scripts/merge-when-green.ps1
  downstream_surfaces_checked:
    - .agents/hooks/guard_protected_actions.py
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
    - .agents/workflow-overlay/safety-rules.md
    - AGENTS.md
    - .agents/workflow-overlay/source-of-truth.md
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        The guard is the enforcement lane's surface (frozen, cross-lane). That lane built the
        structure-B re-target; this doctrine records and relies on it, and does not edit it.
    - path: docs/decisions/overlay_enforcement_placement_classification_v0.md
      reason: >
        The enforcement lane owns and updates the EP classification record for the guard; this
        doctrine references the guard's behavior, it does not edit that record.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        Its "do not push/merge unless authorized" rule is unchanged; structure B is the concrete
        enforcement of it for main, and the guard cites safety-rules as its authority.
    - path: AGENTS.md
      reason: >
        The lane-isolation trigger (PR #9) and behavior kernel are unchanged; the who-merges change
        lives in this decision record, not the kernel.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Source hierarchy and the propagation contract are unchanged; this is a downstream decision
        amendment (and the file is coordination-frozen this turn regardless).
  stale_language_search: >
    rg -i -n "self-merge|self-merges|lane .*merges|merge-when-green|gh pr merge"
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md .github/scripts/merge-when-green.ps1
    (run 2026-06-09 in the doctrine-structure-b worktree)
  stale_language_search_result: >
    Executed 2026-06-09. Remaining "self-merge" mentions are the now-explicitly-superseded item 2
    server-gated-target note and this receipt; item 7 and the helper are re-scoped to human-landed.
    No surface still asserts agents self-merge to main as the live interim.
  non_claims:
    - not validation
    - not readiness
    - not an edit to the enforcement lane's guard or its classification record
    - not a claim that the guard is bug-free or that every merge passed CI
    - structure B is a guard-enforced interim, not the deferred server-side gate
```
