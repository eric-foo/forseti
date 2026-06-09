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
  an agent's `gh pr merge` → `main`), not discipline alone — and **now durable on `main`** (the guard + its PreToolUse registration landed
  via PR #15; verified tracked + registered on `origin/main`, so a fresh clone is protected — see
  Decision item 7's liveness note). The server-side hard gate (items 2 and 4)
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
   one irreversible step. **Liveness (durable on `main`):** this guard enforcement is **durable on `main`** — the guard and its
   `.claude/settings.json` PreToolUse registration landed via PR #15 and are **verified tracked +
   registered on `origin/main`**, so a fresh clone, another machine, or CI is protected, not just this
   working tree. The git-lifecycle protection (`gh pr merge` / push-to-`main` / force / destructive —
   EP-03) is portable and durable on every clone; the external-path protection (EP-01) is tuned to a
   machine's layout and stays per-machine, so other clones adjust their own externals. So the doctrine
   now reads: *structure-B merge protection is durable on `main`; external-path protection is
   per-machine.* (This closes the lane-health detector's machine-local flag: A — durable-on-main —
   landed.) **Harness scope:** the protection above is **Claude-Code-scoped** — the guard is a
   `.claude/settings.json` `PreToolUse` hook matching Claude Code tools, so "a fresh clone is
   protected" holds for **Claude Code sessions**. A non-Claude-Code harness (e.g. Codex) on a fresh
   clone is **not** guard-blocked until the same scripts are wired into its own config; the only
   **harness-agnostic, unbypassable** gate remains the deferred server-side branch protection (items 2
   and 4). **This supersedes the earlier "a solo lane self-merges once CI is green"
   wording**, written before the guard existed. The helper `.github/scripts/merge-when-green.ps1` is
   the **human's** green-check-then-merge tool (run it to verify green and land); agents must **not**
   use it to self-merge — it wraps `gh pr merge`, so an agent running it would bypass the guard, which
   structure B forbids.
8. **Lane-isolation integrity — early detection, not a hard gate.** Lane isolation (the AGENTS.md
   rule, PR #9) is a *judgment* rule, so its integrity mechanism is **early detection**, not another
   hard block. A read-only detector, `.github/scripts/lane-health-check.ps1` (PR #11), surfaces drift
   before it compounds: (a) uncommitted pile-up on a shared base, (b) worktree sprawl, and (c)
   machine-local enforcement — any `.agents/hooks/*.py` present in the working tree but not tracked on
   `origin/main` (a hook that enforces only on this machine). A non-zero exit is a **nudge**
   (operator- or periodic-run), never an unattended block — early detection chosen over a hard
   SessionStart reminder, which was considered and not taken. The detector is read-only with respect
   to the working tree, index, and local branches; `-Fetch` is its only network action.

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

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adds the lane-isolation integrity mechanism (Decision item 8): lane isolation is a judgment rule,
    so its integrity is maintained by early detection — a read-only detector,
    .github/scripts/lane-health-check.ps1 (PR #11), that flags uncommitted pile-up on a shared base,
    worktree sprawl, and machine-local enforcement (a .agents/hooks/*.py present locally but not
    tracked on origin/main). Detection was chosen over a hard SessionStart reminder; the detector is a
    nudge, not a gate.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - .github/scripts/lane-health-check.ps1
    - AGENTS.md
    - .agents/hooks/guard_protected_actions.py
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        The lane-isolation rule (PR #9) is unchanged; item 8 records the integrity mechanism for that
        rule, not a new or altered kernel rule.
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        Cross-lane, frozen. The detector only observes whether enforcement hooks are tracked on main;
        it does not edit the guard. The guard's own on-main durability is a separate flag already
        raised to the enforcement lane.
  stale_language_search: >
    rg -i -n "lane.?isolation|SessionStart|machine-local|early.detection|health.?check"
    docs AGENTS.md .agents   (run 2026-06-09 in the doctrine-lane-isolation worktree off main @ 583d4f0)
  stale_language_search_result: >
    Executed 2026-06-09. Additive — no surface asserts a lane-isolation integrity mechanism or a
    SessionStart reminder that item 8 would contradict. The only doctrine hit is the prior receipt's
    note that the lane-isolation trigger (PR #9) is unchanged, which item 8 is consistent with. Other
    hits are unrelated (a jb skills inventory in orca_bootstrap_record.md, and the workflow-health-check
    kernel skill in skill-adoption.md).
  non_claims:
    - not validation, readiness, or acceptance of any lane's content
    - the detector is a nudge, not a gate, and not a guarantee of lane hygiene
    - not an edit to the enforcement lane's guard or its on-main durability
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    States the structure-B guard's liveness boundary in Decision item 7 and the Status interim bullet:
    guard enforcement is currently machine-local — the guard and its .claude/settings.json PreToolUse
    registration are not tracked on origin/main, so a fresh clone, another machine, or CI is not yet
    protected. Durable-on-main is the target, pending the guard + its registration landing via the
    coordinator's hooks-cluster PR (a human lands it; the guard blocks an agent from merging its own
    PR). On landing, EP-03 git-lifecycle merge protection becomes durable on every clone while EP-01
    external-path protection stays per-machine. This is the enforcement lane's answer to the
    lane-health detector's machine-local flag: A (durable-on-main) is the target, B (machine-local) is
    the honest interim.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - .agents/hooks/guard_protected_actions.py
    - .claude/settings.json
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        Cross-lane, frozen, verified correct (selftest 32/32). Landing it on main is the coordinator's
        hooks-cluster PR, not this doctrine edit; a human lands it because the guard blocks an agent
        from merging its own PR.
    - path: .claude/settings.json
      reason: >
        Coordinator-owned and frozen; origin/main carries no PreToolUse registration. Its landing
        rides the same coordinated hooks-cluster PR.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Per the enforcement lane, its "Active Hooks" note has the same not-on-main incoherence for the
        retrieval-header hook; that is the repo-map / hook owners' fix, flagged not edited here.
  stale_language_search: >
    rg -i -n "enforc" docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    (run 2026-06-09 in the doctrine-lane-isolation worktree)
  stale_language_search_result: >
    Executed 2026-06-09. Both live "enforced" claims — the Status interim bullet and Decision item 7 —
    now carry the machine-local liveness boundary. The remaining hits are the Enforcement-status
    section, the server-enforced-gate non-claims, and the historical DCP receipts (which accurately
    record prior changes); none present structure-B guard enforcement as durable on main while the
    guard is untracked there.
  non_claims:
    - not validation, readiness, or acceptance
    - structure-B guard enforcement is machine-local until the guard lands on main; this records the
      boundary, it does not land the guard
    - not an edit to the enforcement lane's guard, the coordinator's settings.json, or the repo map
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Flips the structure-B guard liveness from machine-local interim (prior receipt) to DURABLE on main:
    the guard and its .claude/settings.json PreToolUse registration landed via PR #15 and are verified
    tracked + registered on origin/main, so a fresh clone is protected. This supersedes the "currently
    machine-local / durable-on-main is the target, pending" framing in Decision item 7, the Status
    interim bullet, and the prior boundary receipt. EP-03 git-lifecycle merge protection is durable on
    every clone; EP-01 external-path protection stays per-machine. Closes the lane-health detector's
    machine-local flag (Option A landed).
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - .agents/hooks/guard_protected_actions.py
    - .claude/settings.json
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        On main now (via PR #15, enforcement-lane-owned); this records its durable status, it does not
        edit the guard.
    - path: .claude/settings.json
      reason: >
        On main now (via PR #15, coordinator-owned); its guard registration is verified present, not
        edited here.
  verification: >
    Observed 2026-06-09 before the flip: git ls-tree origin/main lists
    .agents/hooks/guard_protected_actions.py, and origin/main:.claude/settings.json registers
    "python .agents/hooks/guard_protected_actions.py" - so a fresh clone carries both the script and
    its registration.
  stale_language_search: >
    rg -i -n "machine-local|not yet|pending|interim|Liveness|durable"
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    (run 2026-06-09 in the doctrine-flip-durable worktree)
  stale_language_search_result: >
    Executed 2026-06-09. The two live guard-liveness claims (Status bullet, Decision item 7) now read
    "durable on main." Remaining interim/machine-local hits are: the structure-B-vs-server-gate
    "interim" (still accurate - structure B remains the interim until the 403-blocked server gate), the
    detector's check-name in item 8, and the historical DCP receipts (which record prior states). No
    live surface still claims the guard is machine-local.
  non_claims:
    - not validation or readiness of any lane's content
    - EP-01 external-path protection is per-machine, not durable-on-main
    - the other two cluster hooks (retrieval-header, repo-map-freshness) landed with the guard for
      registration coherence; their correctness is their owners' concern, not asserted here
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Scopes the structure-B "durable on main" claim in Decision item 7 to its actual reach: the guard is
    a Claude-Code-specific .claude/settings.json PreToolUse hook (matcher = Claude Code tool names), so
    "a fresh clone is protected" holds for Claude Code sessions only. A non-Claude-Code harness (e.g.
    Codex) is not guard-blocked until the same scripts are wired into its own config; the
    harness-agnostic, unbypassable gate remains the deferred server-side branch protection. Corrects a
    potential overstatement (the durable flip read as harness-agnostic).
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - .claude/settings.json
    - .agents/hooks/guard_protected_actions.py
  intentionally_not_updated:
    - path: .claude/settings.json
      reason: >
        The Claude-Code wiring is correct and on main; this records its harness scope, it does not
        change the registration. Wiring other harnesses is per-harness work.
  verification: >
    origin/main:.claude/settings.json registers the guard under hooks.PreToolUse with matcher
    "Bash|PowerShell|Write|Edit|MultiEdit|NotebookEdit" - Claude Code tool names - confirming the
    enforcement is Claude-Code-scoped as wired.
  non_claims:
    - not validation or readiness
    - does not claim any non-Claude-Code harness is protected; states the opposite until wired
    - the harness-agnostic gate (server-side branch protection) remains deferred / 403-blocked
```
