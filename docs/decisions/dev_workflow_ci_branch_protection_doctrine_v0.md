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
- **Interim (owner-selected):** keep CI plus a *merge-when-green* flow under **structure B′**
  (Decision item 7): agents prep green PRs, and may **self-merge their own PR only when the
  protected-action guard confirms it is `mergeStateStatus == CLEAN` + all CI checks green + carries
  the opt-in `agent-automerge` label**; every other state (non-CLEAN, pending/failing checks, no
  label, missing/ambiguous PR number, the `gh api .../merge` form, foreign repo, or any lookup
  error/timeout) **fails closed to a human merge**, and the guard prints the repo-scoped manual
  command to run. This is enforced by the enforcement lane's protected-action guard, not discipline
  alone (the guard + its PreToolUse registration are durable on `main`; the guard's prior
  block-all-merges form landed via PR #15 — this amendment relaxes it to the CLEAN-gated form, owner-ratified 2026-06-12). The server-side hard gate (items 2 and 4) is the
  deferred target end-state, unblocked only by a GitHub Pro/Team upgrade or making the repo public —
  and remains the only **harness-agnostic** gate (this guard is Claude-Code-scoped).
- **Unattended auto-merge (added 2026-06-14, this lane):** a CI-controlled GitHub Actions workflow
  (`.github/workflows/auto-merge.yml`) now lands a labeled (`agent-automerge`), clean, green, and
  **up-to-date** lane PR with **no agent session** — the unattended extension of structure B′ (Decision
  item 9). It uses an immediate `gh pr merge --squash` that does **not** need the 403-blocked
  `allow_auto_merge`, so it is still **not** the server-side gate. Code-backed and now **proven**
  (2026-06-15): the bot landed PR #121 unattended (merged by `github-actions[bot]`) after the
  `actions: read` permission fix (PR #118); an ineligible PR is still skipped, never mis-merged.
- **Opt-in unattended low-risk merge (workflow-backed):** `auto-merge.yml` may land a PR only when
  the PR carries both `agent-automerge` and the deterministic router label
  `risk/auto-merge-eligible`, has green CI, is mergeable, is up to date with `main`, is same-repo,
  and is not draft. The router (`pr-risk-router.yml`) defaults to
  `risk/manual-review-required` or `risk/blocked-for-merge-policy` for governance, CI, hook,
  overlay, decision, prompt, review, product, harness, large, deleting, fork, draft, or non-main
  PRs. This is not server-side branch protection and not a review/approval claim.

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
     target* a solo lane could self-merge once green — the current interim (structure B′, item 7)
     approximates this locally: the guard allows an agent self-merge only on a CLEAN + CI-green +
     `agent-automerge`-labeled PR, and a human lands every other case);
   - `strict: false` (a branch need not be up-to-date with `main` before merging);
   - `enforce_admins: false` (the owner retains an emergency override).
3. **Per-lane PR flow.** Each lane branches off `main`, works in its own branch/worktree, and opens
   one focused PR. No multi-workstream mega-batches (the PR #1 lesson).
   **Codex/sandboxed lane-start writeability (harness-scoped, not a Claude Code rule).** For Codex or
   any sandboxed harness whose writes are mediated by workspace writable roots, the lane is not ready
   for repo-changing edits until the active worktree is the harness workspace root (or otherwise
   owner-configured as a writable root) and a lane-start write + git-index preflight passes in that
   worktree. The preflight writes a throwaway file, stages it, unstages it, deletes it, and reads
   `git status --short`; failure to create, stage, unstage, or cleanly remove the probe is a stop
   condition: reroot/reopen the harness on the active worktree, or create a new owner-configured
   writable worktree and retry. Escalated writes are a bounded fallback for the current operation only,
   not the normal lane path. This is Codex/sandboxed-harness scoped; it does **not** add a mandatory
   lane-start probe to Claude Code lanes whose harness already writes to their active worktree and
   reports write failures directly. Avoid relying on nested or secondary writable roots for Codex on
   Windows unless this preflight passes.

   **Codex/manual patch discipline.** For Codex `apply_patch`, generated diffs, or manual textual
   replacement flows, a corrupt patch, failed hunk, or expected-text mismatch is a stop-and-reread
   condition: read the live target lines, then patch from observed current text before continuing. Before
   claiming the edit is correct, inspect the changed hunks with `git diff`; `git diff --check` is only
   whitespace/conflict-marker lint and must not be reported as content-correctness evidence. This clause
   mainly binds Codex/manual patching; it does not add a new mandatory step to Claude Code edit flows
   whose tool already requires live file reads, though any missed edit still routes to stop-and-reread.

4. **Auto-merge** (TARGET — deferred; blocked on this private+free repo). When available, repo
   `allow_auto_merge` lets a lane set a PR to land the moment CI is green (unattended/overnight).
   `delete_branch_on_merge` **is** enabled now (it is not plan-gated); merged head branches are
   auto-deleted. (Update 2026-06-14: an **interim** unattended auto-merge that does **not** need the
   403-blocked `allow_auto_merge` is now live via a CI-controlled Actions workflow — see Decision item
   9; the native `allow_auto_merge` + merge-queue path remains the deferred gold-standard target.)
5. **Merge method.** Lane PRs squash-merge by default — one tidy commit per lane on `main`. Other
   methods remain available; squash is the documented default.
6. **Rebase cadence.** Each lane keeps its branch reasonably current with `main` (rebase or merge
   `main`) to limit semantic drift before merging. When the hard gate is enabled it will use
   `strict: false`, so this stays a lane responsibility rather than a server requirement.
7. **Interim enforcement — structure B′ (guard-verified CLEAN self-merge; else human-landed).** Until
   a server-side gate is available, agents **prepare** green PRs — push their own lane branch, open the
   PR, confirm the `orca-harness-tests` check is green. An agent **may self-merge its own PR** with a
   direct `gh pr merge <N>`, but **only when the protected-action guard
   (`.agents/hooks/guard_protected_actions.py`) confirms the PR is `mergeStateStatus == CLEAN`, every
   CI check has completed green, and it carries the opt-in `agent-automerge` label.** Every other case
   — a non-CLEAN state (`UNSTABLE` / `BLOCKED` / `BEHIND` / `DIRTY` / `DRAFT` / `UNKNOWN` / …), pending
   or failing checks, an empty check set, a missing/ambiguous PR number, the no-arg form, the
   lower-level `gh api .../merge` form, a foreign `--repo`, or any lookup error/timeout — **fails
   closed**: the guard blocks (exit 2) and prints the repo-scoped manual command
   (`gh pr merge <N> --squash --delete-branch --repo eric-foo/orca`) for a human to run from anywhere.
   Push to `main`, force-push, and destructive `reset --hard` / `clean` stay hard-blocked; a benign
   lane-branch push stays allowed. **Why CLEAN + green + label, not bare CLEAN:** on this repo branch
   protection is 403-blocked, so no check is *required* and an empty/early check set can read `CLEAN`
   before CI even starts — requiring the rollup present-and-green (plus an explicit opt-in label)
   closes that false-green race and makes self-merge a deliberate, auditable act. The **opt-in label
   is the agent's deliberate marker**; one-time setup `gh label create agent-automerge --repo
   eric-foo/orca` makes it applyable, and absent the label nothing auto-merges. **Liveness (durable on
   `main`):** the guard and its `.claude/settings.json` PreToolUse registration are **durable on
   `main`** — they landed via PR #15 (then in block-all-merges form) and are verified tracked +
   registered on `origin/main`; this amendment relaxes the guard to the CLEAN-gated form, and **a human
   lands this amendment's own PR**, because the pre-amendment guard blocks all `gh pr merge`. The
   git-lifecycle protection (EP-03) is portable and durable on every clone; external-path protection
   (EP-01) stays per-machine. **Harness scope:** the guard is a `.claude/settings.json` `PreToolUse`
   hook matching Claude Code tools, so this protection — and the CLEAN self-merge allowance — holds for
   **Claude Code sessions only**. A non-Claude-Code harness (e.g. Codex) is **not** guard-gated until
   the same script is wired into its own config; the only **harness-agnostic, unbypassable** gate
   remains the deferred server-side branch protection (items 2 and 4). **This supersedes the earlier
   structure-B "agents do not self-merge; a human lands every merge" wording** (and the still-earlier
   target "a solo lane self-merges once CI is green"): self-merge is now allowed but **narrowly,
   guard-verified, and fail-closed**. The helper `.github/scripts/merge-when-green.ps1` remains the
   **human's** check-then-merge tool; agents must **not** use it to self-merge — it wraps `gh pr merge`
   inside a script subprocess the PreToolUse guard does **not** see (hooks fire on the agent's direct
   tool call, not on grandchild processes), so running it would **bypass the CLEAN/label
   verification**. Agents self-merge only via a direct `gh pr merge <N>`, which the guard inspects.

   **GitHub API sandbox-egress classification.** A `gh` / GitHub API failure that names
   `127.0.0.1:9`, or connection-refused to a local proxy/discard port, is sandbox egress refusal,
   not evidence that the repository, PR, branch, or CI state failed. Prefer an available GitHub
   connector for the read/write path; if using `gh`, network escalation is a bounded owner-gated
   fallback for that operation only. Without a connector result or escalated readback, remote state is
   unverified and must not be reported as failed, green, pushed, created, or merged.

8. **Lane-isolation integrity — early detection, not a hard gate.** Lane isolation (the AGENTS.md
   rule, PR #9) is a *judgment* rule, so its integrity mechanism is **early detection**, not another
   hard block. A read-only detector, `.github/scripts/lane-health-check.ps1` (PR #11), surfaces drift
   before it compounds: (a) uncommitted pile-up on a shared base, (b) worktree sprawl, and (c)
   machine-local enforcement — any `.agents/hooks/*.py` present in the working tree but not tracked on
   `origin/main` (a hook that enforces only on this machine). A non-zero exit is a **nudge**
   (operator- or periodic-run), never an unattended block — early detection chosen over a hard
   SessionStart reminder, which was considered and not taken. The detector is read-only with respect
   to the working tree, index, and local branches; `-Fetch` is its only network action.
9. **Unattended auto-merge bot (extends structure B′).** `.github/workflows/auto-merge.yml` is the
   **unattended** extension of item 7: where structure B′ lets the **in-session** agent self-merge a
   CLEAN + green + `agent-automerge`-labeled PR via the guard, this workflow lands the **same** opt-in
   PRs **with no agent session** — triggered on CI completion (`workflow_run` on `ci`), with a 3-hour
   `cron` backstop and `workflow_dispatch`. It runs in Actions (declaring its own `contents` /
   `pull-requests: write`, since the repo default is read-only) and is **not** subject to the PreToolUse
   guard, so it carries its **own** guardrails in code: the `agent-automerge` label, the
   deterministic router label `risk/auto-merge-eligible`, no `risk/manual-review-required` or
   `risk/blocked-for-merge-policy` label, `mergeable == MERGEABLE`, the `orca-harness-tests` check
   green (and no failing/pending check), **`behind_by == 0` (up-to-date with `main`)**, **one merge
   per run** (safe serialization — there is no native merge queue), and squash + delete-branch. The
   up-to-date guard is **stricter than** the in-session guard
   path (which checks CLEAN but not up-to-date); closing that gap in the guard itself is a deferred
   enforcement-lane follow-on. It uses an immediate `gh pr merge --squash`, which needs no
   `allow_auto_merge` (item 4), so it is **not** the server-side gate. **Honest limitation:** a bot
   merge via `GITHUB_TOKEN` does not re-trigger the `push:main` CI run (GitHub's no-recursion rule); the
   PR's own green check plus the up-to-date guard stand in. The EP-03 guard and `merge-when-green.ps1`
   are unchanged. **Liveness — proven 2026-06-15:** the bot's **first unattended merge is proven** — it
   landed PR #121 with no agent session (merged by `github-actions[bot]`), after PR #118 added the
   `actions: read` scope its `statusCheckRollup` eligibility query needs (without it every prior run
   failed GraphQL `Resource not accessible by integration`, so no earlier run had actually merged). An
   ineligible PR is still skipped, never mis-merged. The 2026-06-16 risk-router amendment narrows
   the bot further: `agent-automerge` alone is no longer sufficient for unattended merge.
10. **Lane-start auto-prune — the cleanup complement to item 9.** Item 9's bot closes the *merge* half
   of the agent-fast-creation / human-gated-cleanup velocity mismatch; this standing
   **agent-instruction-only** rule closes the *cleanup* half. At the **start of each new lane** (the
   cleanup rides on the next creation, so no new always-on infrastructure is added), the agent runs a
   bounded, **non-destructive** prune of **merged** residue:
   1. `git fetch --prune origin` — refresh remote-tracking refs and drop stale ones. This prunes only
      `refs/remotes/origin/*`; it never removes a worktree or a local branch.
   2. For every worktree whose branch reads `[gone]` (its squash-merged remote branch auto-deleted under
      item 4's `delete_branch_on_merge` + item 5's squash default) **and** that has **no open PR**:
      `git worktree remove "<path>"` — **non-force only**.
   3. `git branch -D` the `[gone]` branches — covering **both** worktree-bound and branch-only `[gone]`
      branches (the proven backlog sweep did both).
   - **Load-bearing safety guards (the rule is unsafe without them):**
     - **Non-force `git worktree remove` only — never `--force`.** Non-force `remove` *refuses* a worktree
       holding uncommitted/untracked content; that refusal is the safety that makes the rule unable to
       discard unsaved work. A refused worktree is left for the owner, never force-discarded.
     - **Exclude open-PR worktrees.** Re-derive `gh pr list --state open` and skip any worktree/branch
       with an open PR — removing it would disrupt in-flight review/work.
     - **Never prune the seal or any `[ahead]`-with-unpushed-commits worktree.** The seal worktree
       (`orca-seal-wt` / branch `pilot-seal-outcome`) holds the only copy of a firewalled,
       outcome-sensitive result — never prune it and never read its sealed file. Re-derive the live
       `[ahead]` set (`git for-each-ref --format='%(refname:short) %(upstream:track)' refs/heads | rg
       ahead`) and exclude every entry; an `[ahead]` branch has unpushed unique commits.
     - **Glance for closed-unmerged before `-D`.** A closed-unmerged (or manually-deleted-remote) PR's
       branch *also* reads `[gone]` while its work is **not** on `main`; before deleting, glance
       `gh pr list --state all --head <branch>` and keep any closed-unmerged branch.
     - **Re-derive live every time — never act on a cached list.** The repo moves fast (a single session
       has seen the worktree count and `origin/main` shift repeatedly), so re-derive `git worktree list`,
       the `[gone]`/`[ahead]` sets, and the open-PR set at each lane start.
   - **Boundaries (what this rule is *not*):** not a new always-on destructive automation; not a
     `--force` prune of dirty/open-PR worktrees; not a throttle on lane creation (the chosen lever
     automates the cleanup *tail*, it does not slow creation); not an edit to the EP-03 protected-action
     guard (item 7). Wiring the item-8 detector (`.github/scripts/lane-health-check.ps1`) to *perform or
     prompt* the prune is an explicit **optional follow-on**, deliberately deferred so this additive rule
     introduces no destructive script — the detector stays read-only.
   - **Why a lane-start agent rule (not a git hook):** PR merges are server-side, so a client
     `post-merge` hook never fires; the cleanup must ride on the next lane's creation. **Liveness:** this
     is a behavioral/doctrine rule, not code — it is "live" only insofar as agents follow it, and it
     asserts **no** proven long-run bound on worktree/branch count (that outcome is unproven until the
     rule runs across several lanes). Owner-gated; lands via a per-lane PR off `main` (squash).
11. **Standing self-label policy — when the lane author applies the opt-in marker.** Items 7 and 9 keep
   `agent-automerge` an **opt-in marker** and the bot/guard act only on labeled PRs — that mechanism is
   **unchanged**. This item adds the lane author's **standing policy for *when* to apply that marker**: a
   lane author applies `agent-automerge` to its **own** CLEAN + green PR **by default for routine,
   low-risk changes** it judges safe to land unattended, and **withholds** it — leaving the PR for owner
   review — for higher-risk changes. The marker stays a deliberate, per-PR judgment (it is **not**
   auto-applied by path or automation); this item only sets the default *direction* of that judgment, so
   routine work lands unattended while the human gate is preserved exactly where it matters. It shifts
   the routine-work default from "wait for the owner" to "land unattended," not the merge mechanism.
   - **Apply by default (safe to land unattended) when ALL hold:** it is the author's **own** lane work,
     scoped and traceable to the request; CLEAN + green; and a routine low-risk change — additive
     documentation, decisions/prompts/reviews/migration notes the author is confident in, or a small
     scoped code change with clear test coverage — that needs no human diff-review.
   - **Withhold (leave for owner review) when ANY hold:** it touches enforcement/safety surfaces (the
     EP-01/EP-03 guard, hooks, `.claude/settings.json`, CI or auto-merge workflows, this
     branch-protection doctrine), makes a contested doctrine/tradeoff decision, carries high downstream
     lock-in (schema, interface, persisted data shape), the author is uncertain, or the owner asked to
     review it. **When in doubt, withhold.**
   - **Authority unchanged:** this grants **no new merge authority** — item 7's guard (CLEAN + green +
     label, fail-closed) and the per-lane / accepted-handoff authorization required to open the PR at all
     are unchanged. The owner can always remove the label to hold a PR, and can still CLI-merge anything
     directly. Unlabeled, non-CLEAN, or non-green PRs still go to a human (item 7) — unchanged.
   - **Why author judgment, not a path Action:** "safe to land unattended" is a **content judgment**, not
     a mechanically-checkable path fact, so per the overlay's Enforcement Placement principle
     (`.agents/workflow-overlay/decision-routing.md`) it belongs in an actor-carried rule, not a
     deterministic substrate. A path-scoped auto-label Action (deterministic; would apply to every PR,
     including human- or other-harness-opened ones) remains an explicit **optional follow-on**,
     deliberately not taken here.
   - **Liveness / non-claims:** a behavioral/doctrine rule, not code — "live" only insofar as agents
     follow it; it does **not** assert that auto-landed PRs are correct (CI is a test-suite signal only;
     main is not deployed and a bad merge is reversible by a follow-up PR). Owner-gated; lands via a
     per-lane PR off `main` (squash).
12. **Up-to-date-before-merge — adopted MGT (bot-as-default + forward-ref annotation + red-main
   detector).** Recurring red `push:main` CI from **combination breaks** — two independently-green PRs
   that break when combined (e.g. one adds an `open_next` reference, another renames/removes the target).
   **Root cause:** the up-to-date (`behind_by == 0`) check is enforced for **only one of three** merge
   paths — the bot (item 9). The in-session guard (item 7) checks CLEAN+green+label but **not** up-to-date
   (documented residual), and a human / other-harness raw `gh pr merge` checks nothing. CI tests
   merge-with-base **at PR time**, so a PR merged while behind is never re-tested against current `main`.
   Rationale + full option analysis: the up-to-date-merge enforcement proposal (PR #129). This adopts the
   **mini-god-tier** target — most of the complete fix's value at a fraction of its cost, foregone limit
   named:
   - **Bot-as-default merge path.** Routine PRs land via the bot (apply `agent-automerge`; the bot
     enforces `behind_by == 0` + green + mergeable); raw `gh pr merge` is reserved for urgent fixes. This
     puts up-to-date enforcement on the default path **for free** (item 9's bot is proven) and extends
     item 11 (self-label) from agents to the default merge habit.
   - **Forward-ref annotation discipline (closes the class up-to-date cannot).** An `open_next` /
     `derived_from` link to a file **intentionally not yet on `main`** (a branch-only forward-reference)
     MUST carry a trailing `# nonresolving: <reason>` comment, which `.agents/hooks/check_map_links.py`
     exempts from the existence check and counts as annotated debt — so a deliberate forward-ref cannot
     hard-fail `push:main`. (Up-to-date enforcement, and even the server-side gate, cannot catch this
     class: the target never lands on `main`.)
   - **Red-main detector (detective backstop).** `.github/workflows/main-red-alert.yml` opens a single
     deduplicated tracking issue the moment a `push:main` CI run fails and auto-closes it when `main`
     goes green — so a break landed via an unenforced path is fixed in minutes, not discovered by the
     next lane. **Liveness:** code-backed, **not yet proven** on a live red `main` (the first real
     failure proves it). Detective, **not** preventive.
   - **Downgraded (not adopted now):** *O2a* — add `behind_by == 0` to the EP-03 in-session guard's
     self-merge allowance; covers only the rare agent in-session self-merge (agents route through the bot
     by default) at the cost of editing the frozen, enforcement-lane-owned guard. *O2b* — make
     `.github/scripts/merge-when-green.ps1` refuse when behind; a substrate that fires only if the helper
     is used, so a raw `gh pr merge` bypasses it. Revisit either if agents become the primary mergers.
   - **Deferred end-state:** server-side branch protection "require branches up to date" (+ merge queue)
     — the only **complete, harness-agnostic, unbypassable** prevention across all paths. Blocked on this
     private+free repo (HTTP 403, items 2/4); revisit on a GitHub Pro/Team upgrade or a public repo.
   - **Foregone limitation (consciously accepted):** a human or non-Claude-harness raw `gh pr merge` of a
     **behind** PR can still combination-break `main` — **detected fast** by the red-main detector, **not
     prevented**. Closing this residual requires the deferred server-side gate.
13. **PR cadence — major durable point, not every subpoint.** A lane should open a focused PR after
   each **major durable point**: one coherent, owner-reviewable decision or artifact boundary that
   future agents may rely on. Examples include a first customer / ICP target selection, proof-gate
   change, buyer-risk doctrine change, data-spine boundary change, roster-scope implication, or
   implementation-scoping decision. Do **not** split every thought, objection, or supporting
   refinement into its own PR; group subpoints when they change the same durable point, share the same
   controlling sources, and should be reviewed with the same validation and non-claims. If a new major
   point emerges while a lane is already open, either include it only when it is directly coupled to
   the same reviewable decision or split it into a follow-up branch / PR. Each such PR should state:
   what decision changed, why it changed, what stance shifted or was magnified, changed files,
   explicit non-claims, and validation run. This cadence does not grant standing commit, push, or PR
   authority; `.agents/workflow-overlay/safety-rules.md` still requires explicit authorization.

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
- Risk-router labels and merge-packet comments are routing/check signal only — **not** validation,
  approval, review acceptance, readiness, or proof that a PR is safe to merge.
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
    Adds PR cadence guidance: lanes should open a focused PR after each major
    durable point, not after every subpoint; subpoints stay grouped when they
    share the same reviewable decision, controlling sources, validation, and
    non-claims. PR bodies should state the decision change, why, stance shifts,
    changed files, non-claims, and validation.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
    - output_authority
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md already routes landing through this per-lane PR flow. The
        cadence refinement belongs in the flow record, not the root kernel.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The explicit-authorization rule for commit, push, and PR creation is
        unchanged; this cadence applies only after authorization.
    - path: .agents/workflow-overlay/source-of-truth.md
      reason: >
        Source hierarchy and propagation mechanics are unchanged; this is a
        downstream workflow decision amendment.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The repo map already points lane PR flow to this decision record; no
        new routing surface or file owner was added.
  stale_language_search: >
    rg -n "major durable point|every major point|every subpoint|per-lane PR|one focused PR|PR cadence"
    AGENTS.md .agents/workflow-overlay docs/workflows/orca_repo_map_v0.md
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  stale_language_search_result: >
    Executed 2026-06-16 after this patch. Hits are the new item 9 cadence
    language, this receipt, and existing compatible references to per-lane /
    one-focused-PR flow. No checked surface requires a PR for every subpoint or
    grants standing PR authority.
  non_claims:
    - not validation
    - not readiness
    - not blanket commit authorization
    - not blanket push authorization
    - not blanket PR authorization
    - not a merge authorization
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

```yaml
direction_change_propagation:
  doctrine_changed: >
    Relaxes structure B to structure B' (owner-ratified 2026-06-12): an agent MAY self-merge its own
    PR via a direct `gh pr merge <N>`, but ONLY when the protected-action guard confirms the PR is
    mergeStateStatus == CLEAN, every CI check has completed green, and it carries the opt-in
    `agent-automerge` label. Every other state, the no-arg/ambiguous form, the `gh api .../merge`
    form, a foreign `--repo`, or any lookup error/timeout FAILS CLOSED to a human merge, and the guard
    prints the repo-scoped manual command. This supersedes the prior structure-B "agents do not
    self-merge; a human lands every merge" wording and acts on the 2026-06-09 owner flag in the EP
    classification record ("if you intend agent self-merge-when-green, relax the gh pr merge block").
    The bar is CLEAN + green + label (not bare CLEAN) because, with branch protection 403-blocked, no
    check is required and an empty/early check set can read CLEAN before CI starts; the rollup-green +
    label requirements close that false-green race. EP-01 protected paths and EP-03 push-to-main /
    force-push / destructive-clean are UNCHANGED. The guard stays Claude-Code-scoped; the
    harness-agnostic server-side gate remains the deferred end-state.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - .agents/hooks/guard_protected_actions.py
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
  downstream_surfaces_checked:
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
    - .claude/settings.json
    - .github/scripts/merge-when-green.ps1
    - .github/scripts/lane-health-check.ps1
  intentionally_not_updated:
    - path: .claude/settings.json
      reason: >
        The guard's PreToolUse registration and matcher are unchanged; the behavior change is wholly
        inside the guard script. The `ask` rule `Bash/PowerShell(gh pr*)` is left in place as an
        interactive-mode belt-and-suspenders (the human is still prompted in interactive mode; the
        guard is the auto-mode enforcement). The `git commit` ask->allow owner hand-edit is a separate
        classifier-bound change, not this lane's.
    - path: .github/scripts/merge-when-green.ps1
      reason: >
        Still the human's check-then-merge tool; re-scoped in item 7 prose (it wraps `gh pr merge`
        inside a script subprocess the PreToolUse guard does not see, so agents must not use it to
        self-merge), but its content is unchanged.
    - path: .github/scripts/lane-health-check.ps1
      reason: >
        The machine-local-enforcement detector is unaffected; the guard remains tracked on origin/main.
    - path: docs/decisions/overlay_enforcement_placement_classification_v0.md
      reason: >
        The enforcement lane owns the guard's EP record and records this guard change there directly
        (see its 2026-06-12 Update section); this doctrine references that record rather than the
        reverse. (Listed here as a checked downstream surface, not unchanged — it IS updated, in its
        own lane section.)
  verification: >
    Guard `--selftest` 46/46 PASS, exit 0 (CLEAN+green+label -> allow; no-label / non-CLEAN / pending /
    empty-checkset / BLOCKED / unknown-PR / lookup-raises / no-number / gh-api-form / foreign-repo ->
    block; merge-allowed + push-to-main -> block; all pre-existing EP-01 and EP-03 push/force/
    destructive/benign cases unchanged). Live payload render: `gh pr merge` (no number) and the gh-api
    form both exit 2 with the repo-scoped manual command in stderr; `git status` exits 0. CI re-runs
    the orca-harness suite on this PR.
  stale_language_search: >
    grep -rin -E "self-merge|self-merges|human-gated|human-land|do not .*self|structure b"
    AGENTS.md .agents/workflow-overlay
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    docs/decisions/overlay_enforcement_placement_classification_v0.md
    (run 2026-06-12 in the guard-clean-self-merge worktree off origin/main @ b463c3c)
  stale_language_search_result: >
    Executed 2026-06-12. All LIVE surfaces now carry the conditional CLEAN self-merge: AGENTS.md line
    60 (kernel landing clause), safety-rules.md line 25, the doctrine Status interim bullet, Decision
    item 2's server-gated-target parenthetical, and Decision item 7. The remaining "structure B" /
    "human lands every merge" / "agents do not self-merge" hits are the historical DCP receipts above
    (append-only records of prior states, correctly not edited) and the EP record's 2026-06-09 owner
    flag (now acted upon and recorded in that record's 2026-06-12 Update). No live surface still
    asserts that agents never self-merge to main.
  non_claims:
    - not validation, readiness, or acceptance of any lane's content
    - CLEAN + green + label is a CI-and-mergeability signal, NOT a human diff-review; main is not
      deployed and a bad merge is reversible by a follow-up PR
    - EP-01 protected paths and EP-03 push/force/destructive blocks are unchanged
    - the guard is Claude-Code-scoped; a non-Claude-Code harness is neither blocked nor granted
      self-merge until wired
    - not durable on main until this amendment's own PR is landed by a human (the pre-amendment guard
      blocks the agent from self-merging it)
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adds Decision item 9: an unattended GitHub Actions auto-merge bot
    (.github/workflows/auto-merge.yml) that is the unattended extension of structure B' (item 7).
    Where the guard lets the in-session agent self-merge a CLEAN + green + agent-automerge-labeled PR,
    this workflow lands the SAME opt-in PRs with no agent session, triggered on CI completion plus a
    3-hour cron backstop and workflow_dispatch. It carries its own in-code guardrails: the
    agent-automerge label, mergeable == MERGEABLE, orca-harness-tests green (no failing/pending check),
    behind_by == 0 (up-to-date with main), one merge per run, and squash + delete-branch. It uses an
    immediate `gh pr merge --squash` that does NOT need the 403-blocked allow_auto_merge, so it is an
    interim unattended auto-merge, NOT the deferred server-side gate. The EP-03 guard and
    merge-when-green.ps1 are unchanged; the workflow runs in Actions, not through the PreToolUse hook.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - .github/workflows/auto-merge.yml
  downstream_surfaces_checked:
    - .agents/hooks/guard_protected_actions.py
    - .github/workflows/ci.yml
    - .agents/workflow-overlay/safety-rules.md
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        Frozen enforcement-lane surface. The bot runs in Actions (not through the PreToolUse hook) and
        carries its guardrails independently; the in-session guard's lack of an up-to-date check is a
        documented residual and a deferred enforcement-lane follow-on, not closed here.
    - path: .github/workflows/ci.yml
      reason: >
        Referenced by the bot's workflow_run trigger (workflows: [ci]) and as the orca-harness-tests
        green gate; its content is unchanged.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The do-not-push/merge-unless-authorized rule is unchanged; the bot is an Actions actor, not an
        agent lane, and the owner lands this lane's own PR.
  verification: >
    auto-merge.yml parses (python yaml.safe_load OK): workflow name auto-merge, concurrency group
    auto-merge, env AUTOMERGE_LABEL=agent-automerge, permissions contents/pull-requests: write, triggers
    workflow_run[ci] + schedule(0 */3 * * *) + workflow_dispatch. All label references are
    agent-automerge while name/concurrency stay auto-merge; the jq eligibility filters were hand-traced
    (green -> eligible; failing/pending/no-checks -> skip). NOT live-run: jq is not installed locally and
    the workflow cannot run until on main; the first live merge is owner-triggered and fail-safe.
  stale_language_search: >
    rg -i -n "auto.?merge|allow_auto_merge|unattended|overnight"
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    (run 2026-06-14 in the automerge-bot-v0 worktree off origin/main @ 8e54aad)
  stale_language_search_result: >
    Executed 2026-06-14. Item 4 (native auto-merge deferred/blocked) now carries a parenthetical pointer
    to the interim Actions-bot path (item 9); the Status section carries the unattended-auto-merge
    bullet; item 9 is the canonical home. No live surface still implies the human merge is the only
    interim or that no unattended auto-merge exists. The "deferred target" wording for the native
    allow_auto_merge + server gate stays accurate (item 9 is explicitly not that gate).
  non_claims:
    - not validation, readiness, or acceptance of any lane's content
    - the bot is code-backed and logic-checked, NOT a proven unattended merge; the first live run is
      owner-triggered and fail-safe (ineligible PR skipped, never mis-merged)
    - not the server-side branch-protection / native auto-merge gate (still 403-blocked); an interim
      Actions-bot mechanism
    - the in-session guard path still lacks an up-to-date check (documented residual); the guard is
      unchanged this lane
    - the owner lands this lane's own PR
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adds Decision item 10: a lane-start auto-prune standing rule (agent-instruction-only) that is the
    CLEANUP complement to item 9's auto-merge bot. At each new lane's start the agent runs
    `git fetch --prune origin`, then non-force `git worktree remove` of any [gone]-branch worktree with
    no open PR, then `git branch -D` of those [gone] branches (both worktree-bound and branch-only),
    bounded by load-bearing guards: non-force remove only, exclude open-PR worktrees, never the seal or
    any [ahead]-unpushed worktree, glance for closed-unmerged before -D, and re-derive live every time.
    It is NOT a destructive always-on automation, NOT a --force prune, NOT a creation throttle, and NOT
    a guard edit; wiring the item-8 lane-health-check.ps1 detector to perform/prompt the prune is an
    explicit optional follow-on, deliberately deferred (the detector stays read-only).
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - .agents/hooks/guard_protected_actions.py
    - .github/scripts/lane-health-check.ps1
    - .github/workflows/auto-merge.yml
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        The EP-03 guard is the frozen enforcement-lane surface; this is a behavioral/doctrine rule and
        does not edit or weaken it. Non-force worktree remove and branch -D on lane branches are not
        guard-blocked actions; push-to-main / force-push / destructive clean stay hard-blocked.
    - path: .github/scripts/lane-health-check.ps1
      reason: >
        The item-8 detector stays read-only; wiring it to perform or prompt the prune is the explicit
        optional follow-on, intentionally not taken here to avoid introducing a destructive script.
    - path: .github/workflows/auto-merge.yml
      reason: >
        Item 9's bot (the merge half) is unchanged; item 10 is its cleanup complement and composes with
        it (a bot-merged lane's branch reads [gone] and becomes prunable at the next lane start).
    - path: AGENTS.md
      reason: >
        The behavior kernel and authorization boundaries are unchanged; the owner placed this procedural
        git rule in the decision record (not the terse global kernel), co-located with items 8 and 9.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The do-not-push/merge-unless-authorized rule is unchanged; this rule prunes only merged,
        no-open-PR residue at lane start and grants no new push/merge authority.
  verification: >
    Re-verified 2026-06-15 against origin/main before drafting (origin/main advanced 7c804cb -> 5efd405
    during the session; doctrine identical across both, empty diff): items 8 and 9 present and unchanged;
    PR #97 (auto-merge bot) MERGED 2026-06-14T14:36:46Z; auto-merge.yml and lane-health-check.ps1 tracked
    on origin/main. Live state grounding the guards: the only [gone] branch was
    r6-rescan-commission-beautypie (PR #37 MERGED -> a genuine squash-merge, not closed-unmerged); the
    [ahead] set was doctrine-harness-caveat, hooks-readme, judgment-spine-read-machinery-architecture-v0,
    ledger-c2-read-contract-v0; the seal worktree orca-seal-wt [pilot-seal-outcome] present. The prune
    commands are proven by this lane's predecessor backlog sweep (worktrees 53->29, six [gone] branches
    deleted, dirty worktrees correctly refused by non-force remove). NO fresh destructive sweep was run
    as part of authoring this rule.
  stale_language_search: >
    git grep -i -nE "auto.?prune|worktree remove|lane.?start.*prune|sprawl|manual sweep|cleanup.*manual|\[gone\]"
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md AGENTS.md .agents/workflow-overlay
    (run 2026-06-15 in the autoprune-rule worktree off origin/main @ 5efd405)
  stale_language_search_result: >
    Executed 2026-06-15. The only hits are item 8 and its DCP receipt naming "worktree sprawl" as drift
    the read-only detector *surfaces*. No live surface claims cleanup is manual-only, that no prune rule
    exists, or that sprawl is unaddressed, so item 10 forks no existing wording — it is purely additive
    and acts on what item 8 only detects (the two compose: detect, then prune). No surface required an
    edit.
  non_claims:
    - not validation, readiness, or acceptance of any lane's content
    - a behavioral/doctrine rule, NOT code; "live" only insofar as agents follow it
    - asserts no proven long-run bound on worktree/branch count (unproven until run across several lanes)
    - not an edit to the EP-03 guard, the item-8 detector, or the item-9 bot
    - not a destructive always-on automation, a --force prune, or a creation throttle
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adds Decision item 11: a standing self-label policy for WHEN the lane author applies the existing
    opt-in agent-automerge marker. The merge mechanism is unchanged (items 7/9: bot/guard act only on
    labeled PRs); this item sets the agent's default judgment — apply the label to its own CLEAN + green
    PR by default for routine low-risk changes (additive docs, decisions/prompts/reviews the author is
    confident in, or small scoped code with test coverage), and WITHHOLD it (leave for owner review) for
    higher-risk changes: enforcement/safety surfaces (EP-01/EP-03 guard, hooks, settings.json, CI or
    auto-merge workflows, this doctrine), contested doctrine/tradeoff decisions, high downstream lock-in
    (schema/interface/persisted data), author uncertainty, or owner-requested review — when in doubt,
    withhold. This shifts the routine-work default from "wait for the owner" to "land unattended" while
    preserving the human gate where it matters. It grants NO new merge authority and is author judgment,
    not a path Action; a deterministic path-scoped auto-label Action is an explicit deferred follow-on.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - .agents/hooks/guard_protected_actions.py
    - .github/workflows/auto-merge.yml
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        The EP-03 guard is unchanged: self-merge still requires CLEAN + green + label and fails closed.
        Item 11 sets which PRs the author labels, not what the guard allows; no authority is added.
    - path: .github/workflows/auto-merge.yml
      reason: >
        The bot's guardrails (label, mergeable, green, up-to-date, one-per-run, squash+delete) are
        unchanged; item 11 changes only the agent's default policy for applying the label it already reads.
    - path: AGENTS.md
      reason: >
        The behavior kernel and the per-turn / accepted-handoff authorization to open a PR at all are
        unchanged; this is a procedural default in the decision record, co-located with items 7/9/10.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The do-not-push/merge-unless-authorized rule is unchanged; item 11 grants no new authority and
        applies only to a PR the lane was already authorized to open.
  verification: >
    Re-verified 2026-06-15 against origin/main @ f883b68 (item 10 landed via PR #104, MERGED
    2026-06-15T08:05:22Z): items 7 and 9 present; item 7's "the opt-in label is the agent's deliberate
    marker" framing (lines ~100-101) stays accurate — item 11 keeps the marker a deliberate per-PR
    judgment and does not auto-apply it, so that wording is consistent and not edited. Item 7's "a human
    lands every other case" (unlabeled / non-CLEAN / non-green) also stays accurate. All YAML blocks parse.
  stale_language_search: >
    git grep -i -nE "self.?label|opt.?in|deliberate marker|by default.*label|agent-automerge"
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md AGENTS.md .agents/workflow-overlay
    (run 2026-06-15 in the selflabel-default worktree off origin/main @ f883b68)
  stale_language_search_result: >
    Executed 2026-06-15. The agent-automerge / opt-in / deliberate-marker hits are all item 7 and item 9
    MECHANISM wording, which item 11 preserves (the bot/guard still act only on labeled PRs; the marker
    stays a deliberate per-PR judgment). No live surface claims the agent never self-applies the label or
    that every PR must wait for the owner, so item 11 forks no existing rule — it is additive and only
    sets the agent's default direction for applying the existing marker. The other opt-in hits are the
    unrelated delegated-review-patch convention. No surface required an edit.
  non_claims:
    - not validation, readiness, or acceptance of any lane's content
    - a behavioral/doctrine rule, NOT code; "live" only insofar as agents follow it
    - grants no new merge authority; item 7's guard and the per-lane authorization are unchanged
    - does not claim auto-landed PRs are correct (CI is a test-suite signal only; main is not deployed and
      a bad merge is reversible by a follow-up PR)
    - not a path-scoped auto-label automation (that deterministic variant is a deferred optional follow-on)
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Flips the auto-merge bot (Decision item 9) from "code-backed, NOT a proven unattended merge" to
    PROVEN: on 2026-06-15 the bot landed PR #121 with no agent session (merged by github-actions[bot]).
    This was unblocked by PR #118, which added actions:read to the workflow permissions — the scope the
    statusCheckRollup -> checkSuite.workflowRun eligibility query needs; before it, every bot run that
    evaluated a labeled PR failed GraphQL "Resource not accessible by integration", so no earlier run had
    actually merged. Updates the two LIVE surfaces (the Status "Unattended auto-merge" bullet and item 9's
    Liveness line); the fail-safe behavior (ineligible PR skipped, never mis-merged) and the
    not-the-server-side-gate framing are unchanged.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - .github/workflows/auto-merge.yml
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
  intentionally_not_updated:
    - path: .github/workflows/auto-merge.yml
      reason: >
        The actions:read fix already landed via PR #118; this record only flips the liveness claim it
        enables. The workflow logic is unchanged.
    - path: AGENTS.md
      reason: >
        The kernel routes "land via the per-lane PR flow" to this doctrine; the bot's existence (item 9)
        and how to opt a PR in (item 11) live here, so no kernel edit is needed.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        Merge authority is unchanged; proving the bot works grants no new authority.
  verification: >
    Observed 2026-06-15: PR #121 state MERGED, mergedBy.login = "github-actions"; auto-merge run
    27541440896 logged "PR #121 is eligible (labeled, mergeable, green, up-to-date). Merging (squash)."
    then "Merged PR #121 at 0a87d8f8...". Earlier bot run 27534994021 had failed on PR #116 with
    "Resource not accessible by integration (...statusCheckRollup...checkSuite.workflowRun)"; actions:read
    landed via PR #118 (MERGED 2026-06-15). The two live surfaces now read "proven".
  stale_language_search: >
    git grep -inE "first live run|first live merge|not.{0,4}a proven unattended|NOT.{0,4}claim a proven"
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    (run 2026-06-15 in the doctrine-automerge-bot-proven worktree off origin/main @ 9f10a8a7)
  stale_language_search_result: >
    Executed 2026-06-15. The two LIVE surfaces (Status "Unattended auto-merge" bullet, item 9 Liveness)
    now read "proven". The remaining "first live run / first live merge / not a proven" hits are the
    append-only DCP receipts that recorded the bot's addition and its actions:read fix — historical
    records of prior states, correctly NOT edited.
  non_claims:
    - not validation, readiness, or acceptance of any lane's content
    - the proven claim is one observed unattended bot merge (#121); it is NOT the server-side
      branch-protection gate (still 403-blocked) and does not claim the bot is bug-free
    - still fail-safe: an ineligible PR is skipped, never mis-merged
    - the in-session PreToolUse guard is unchanged (and is harness/working-tree-scoped, not the bot)
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Adds Decision item 12: adopts the up-to-date-before-merge MGT after recurring red push:main CI from
    combination breaks (two independently-green PRs that break combined). Root cause: behind_by==0 is
    enforced only for the bot (item 9), not the in-session guard (item 7 residual) or human/CLI merges.
    Adopted: (1) bot-as-default merge path (routine PRs land via the bot, which enforces up-to-date;
    extends item 11); (2) forward-ref annotation discipline (a branch-only open_next/derived_from link
    must carry "# nonresolving: <reason>", which check_map_links already exempts as debt); (3) a red-main
    detector workflow (.github/workflows/main-red-alert.yml) that opens/auto-closes a single tracking
    issue on push:main red/green. Downgraded O2a (guard behind_by check) and O2b (merge-when-green
    refuse-when-behind); deferred the server-side require-up-to-date gate (O1, 403-blocked). Foregone
    limit named: a raw gh pr merge of a behind PR can still break main — detected fast, not prevented.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - .github/workflows/main-red-alert.yml
  downstream_surfaces_checked:
    - .agents/hooks/guard_protected_actions.py
    - .github/scripts/merge-when-green.ps1
    - .agents/hooks/check_map_links.py
    - .github/workflows/auto-merge.yml
    - AGENTS.md
  intentionally_not_updated:
    - path: .agents/hooks/guard_protected_actions.py
      reason: >
        O2a (adding behind_by==0 to the guard's self-merge allowance) is downgraded, not adopted; the
        frozen EP-03 guard is unchanged. Agents route through the bot (which enforces up-to-date) by default.
    - path: .github/scripts/merge-when-green.ps1
      reason: >
        O2b (refuse-when-behind in the helper) is downgraded — a raw gh pr merge bypasses the helper, so
        the substrate gives near-zero coverage of the actual path. Unchanged.
    - path: .agents/hooks/check_map_links.py
      reason: >
        The "# nonresolving:" exemption already exists in the checker; item 12 adopts the DISCIPLINE of
        using it for deliberate forward-refs. No checker change needed.
    - path: .github/workflows/auto-merge.yml
      reason: >
        The bot already enforces behind_by==0; item 12 makes it the default path. The workflow is unchanged.
    - path: AGENTS.md
      reason: >
        The kernel routes "land via the per-lane PR flow" to this doctrine; the bot-as-default habit and
        the disciplines live here. No kernel edit.
  verification: >
    main-red-alert.yml parses (python yaml.safe_load OK): triggers workflow_run[ci] + workflow_dispatch;
    permissions issues:write + actions:read; gated to push:main outcomes; dedup-by-title issue
    open/comment/close. check_map_links --strict OK on the PR tree — item 12's path refs resolve
    (main-red-alert.yml in this PR; check_map_links.py and merge-when-green.ps1 on main; the proposal is
    referenced by PR number, not a path token). Liveness: the detector is code-backed and NOT yet proven
    on a live red main (the first real push:main failure proves it), mirroring item 9's honest non-claim.
  stale_language_search: >
    git grep -inE "up.?to.?date|behind_by|combination break|main.?red|nonresolving"
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    (run 2026-06-15 in the dev-workflow-uptodate-mgt worktree; re-synced onto origin/main after #127/#129)
  stale_language_search_result: >
    Executed 2026-06-15. Item 9 (now flipped to proven by #127) notes the in-session guard "lacks an
    up-to-date check (documented residual)"; item 12 is consistent with and acts on that note (downgrades
    the guard fix O2a, adopts bot-as-default instead). No live surface claims up-to-date is enforced on
    all paths, so item 12 forks no existing rule — it is additive.
  non_claims:
    - not validation, readiness, or acceptance of any lane's content
    - the red-main detector is code-backed, NOT yet proven on a live red main; detective, not preventive
    - up-to-date enforcement is not complete here (the raw-CLI / other-harness path is a named, accepted
      residual); the complete, unbypassable gate remains the deferred server-side option (O1)
    - O2a does not edit the EP-03 guard; O2b does not edit the helper; check_map_links is unchanged
    - mini-god-tier is a capability-target lens, not a validation or readiness claim
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Narrows the proven unattended auto-merge bot with deterministic risk routing:
    `pr-risk-router.yml` labels PRs as auto-merge eligible, manual-review
    required, or blocked; `auto-merge.yml` now requires both `agent-automerge`
    and `risk/auto-merge-eligible` and skips manual/blocked PRs. Higher-risk PRs
    get a deterministic merge packet, not automated approval. This narrows the
    earlier label-only unattended path while preserving the non-claim that this
    is not server-side branch protection.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - .github/workflows/auto-merge.yml
    - .github/workflows/pr-risk-router.yml
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        The behavior kernel and explicit authorization boundaries are unchanged;
        this is a merge-routing workflow doctrine update, not a new global agent
        rule.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        The no-unauthorized commit/push/PR/merge rule is unchanged. The workflows
        define repository automation behavior after explicit PR flow, not blanket
        agent authority.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The existing enforcement-placement and non-self-certification rules
        already cover this shape: deterministic labels are routing/check signal,
        not validation or approval evidence.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The current map already indexes `.github/` as GitHub Actions workflows
        and local operational scripts; no new top-level route is introduced.
  non_claims:
    - not server-side branch protection
    - not native GitHub auto-merge
    - not validation
    - not readiness
    - not review approval
    - not blanket agent merge authority
```
