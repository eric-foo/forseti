# Dev-Workflow CI + Branch-Protection Doctrine v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Forseti developer-workflow doctrine — CI test gate, branch protection on main, per-lane PR flow, auto-merge, and lane-update cadence.
use_when:
  - Opening, merging, or gating a change to Forseti's main branch.
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

### Current state — 2026-07-11

- **Live CI:** `.github/workflows/ci.yml` runs on every pull request and push to
  `main`; the required job context is `forseti-harness-tests`.
- **Live server gate:** GitHub reports this repository public and classic branch
  protection active on `main`:
  - pull requests required with zero approving reviews;
  - `forseti-harness-tests` required with `strict: true` (the head must be up to date);
  - administrators included;
  - force-push and branch deletion disabled.
- Native `allow_auto_merge` remains off. The custom guarded auto-merge workflow
  remains the opt-in unattended merge actor.
- `auto-merge`, `pr-risk-router`, and `main-red-alert` were observed
  `disabled_manually`, then owner-authorized and read back `active` after the
  server gate was established.
- Agent and local Git guards remain defense in depth; they are no longer the
  only preventive boundary and do not weaken the server gate.

This state is an observed GitHub API readback, not a correctness or readiness claim.

### Historical interim baseline — superseded 2026-07-11

The bullets below record the pre-public, private/free-plan state and are retained as history:

- **Live:** CI (`.github/workflows/ci.yml`) runs the forseti-harness suite on every `pull_request` and
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

At that historical point, this record did not assert that any server-side gate was active; none was.

## Context

- `main` had no CI: nothing validated commits automatically, so a green check could not gate merges.
- PR #1 reconciled a 28-commit, multi-workstream branch (`ecr-sp3-timing-deriver-slice1`) in one
  batch and was **closed unmerged** — too large and conflicting to land safely as one unit.
- Adopted pattern instead: small, focused, **per-lane PRs off `main`**, each merged when green.
- Lanes run concurrently via branches plus git worktrees, with a goal of eventually-unattended
  (overnight) merging.

## Decision

1. **CI.** A GitHub Actions workflow (`.github/workflows/ci.yml`) runs the forseti-harness test suite
   on every `pull_request` and on `push` to `main`: Ubuntu, Python 3.12, `pip install -e .`
   (forseti-harness core dependencies only) plus pinned `pytest` and `pytest-xdist`, then the full
   suite from `forseti-harness/` with slow-test timing and four file-grouped workers. Single target —
   no version matrix, no path-filter, no dependency caching, and no test-selection reduction.
2. **Branch protection on `main` — LIVE.** The server gate requires:
   - the `forseti-harness-tests` status check to pass;
   - a pull request before merging with `required_approving_review_count: 0`;
   - `strict: true`, so a head behind `main` cannot merge until updated and retested;
   - `enforce_admins: true`;
   - force-push and branch deletion disabled.
   Applied and read back through the GitHub API on 2026-07-11 after the repository
   became public. This is the harness-agnostic preventive boundary; local and
   agent guards remain defense in depth.
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

4. **Auto-merge.** Native repository `allow_auto_merge` remains `false`; Forseti
   keeps the custom guarded Actions workflow in item 9 as the opt-in unattended
   merge actor. `delete_branch_on_merge` remains enabled. The workflow was read
   back `active` on 2026-07-11 after the server gate was established. Branch
   protection independently requires the strict CI check and an up-to-date head,
   so the custom router/bot policy supplements rather than substitutes for it.
5. **Merge method.** Lane PRs squash-merge by default — one tidy commit per lane on `main`. Other
   methods remain available; squash is the documented default.
6. **Lane-update cadence.** Each lane keeps its branch reasonably current with
   `main`; the server gate also uses `strict: true`, so a behind head must update
   and rerun CI before merging. Before the lane branch is first pushed, rebase onto
   `origin/main` remains allowed. Once the branch is published or has a PR, do not
   rebase it: fetch `main`, merge `origin/main` into the lane branch, resolve any
   conflicts there, and use an ordinary fast-forwardable lane push. This is the
   only update route compatible with both a stable published branch identity and
   the hard no-force-push rule. Prefer the explicit pair `git fetch origin main`
   then `git merge --no-edit origin/main`; do not rely on a plain `git pull`, whose
   behavior can be changed by local rebase configuration.
7. **Defense-in-depth enforcement — structure B′ (guard-verified CLEAN self-merge; else human-landed).**
   With the server gate active, agents still prepare green PRs. An agent may self-merge
   its own PR with a direct `gh pr merge <N>`, but **only when the protected-action guard
   (`.agents/hooks/guard_protected_actions.py`) confirms the PR is `mergeStateStatus == CLEAN`, every
   CI check has completed green, and it carries the opt-in `agent-automerge` label.** Every other case
   — a non-CLEAN state (`UNSTABLE` / `BLOCKED` / `BEHIND` / `DIRTY` / `DRAFT` / `UNKNOWN` / …), pending
   or failing checks, an empty check set, a missing/ambiguous PR number, the no-arg form, the
   lower-level `gh api .../merge` form, a foreign `--repo`, or any lookup error/timeout — **fails
   closed**: the guard blocks (exit 2) and prints the repo-scoped manual command
   (`gh pr merge <N> --squash --delete-branch --repo eric-foo/forseti`) for a human to run from anywhere.
   Push to `main`, force-push, destructive `reset --hard` / `clean`, and explicit
   rebase starts on a mechanically confirmed published lane stay hard-blocked; a
   benign lane-branch push, the fetch-plus-merge update route, and rebase recovery
   commands stay allowed. **Why CLEAN + green + label, not bare CLEAN:** the server
   now requires the CI check, while the guard independently requires a present green rollup
   plus explicit opt-in before authorizing an agent merge. That preserves clear local failure,
   closes the empty/early check-set race, and keeps self-merge auditable. The **opt-in label
   is the agent's deliberate marker**; one-time setup `gh label create agent-automerge --repo
   eric-foo/forseti` makes it applyable, and absent the label nothing auto-merges. **Liveness (durable on
   `main`):** the guard and its `.claude/settings.json` PreToolUse registration are **durable on
   `main`** — they landed via PR #15 (then in block-all-merges form) and are verified tracked +
   registered on `origin/main`; this amendment relaxes the guard to the CLEAN-gated form, and **a human
   lands this amendment's own PR**, because the pre-amendment guard blocks all `gh pr merge`. The
   git-lifecycle protection (EP-03) is portable and durable on every clone; external-path protection
   (EP-01) stays per-machine. **Harness scope:** the shared protected-action guard is wired
   through `.claude/settings.json` and the Codex adapter in `.codex/hooks.json`; the tracked
   Git pre-push guard applies to any clone that installs `.githooks`. Other harnesses may lack
   those local layers, so the active branch protection in item 2 is the only harness-agnostic,
   unbypassable merge gate. **This supersedes the earlier
   structure-B "agents do not self-merge; a human lands every merge" wording** (and the still-earlier
   target "a solo lane self-merges once CI is green"): self-merge is now allowed but **narrowly,
   guard-verified, and fail-closed**. The helper `.github/scripts/merge-when-green.ps1` remains the
   **human's** check-then-merge tool; agents must **not** use it to self-merge — it wraps `gh pr merge`
   inside a script subprocess the PreToolUse guard does **not** see (hooks fire on the agent's direct
   tool call, not on grandchild processes), so running it would **bypass the CLEAN/label
   verification**. Agents self-merge only via a direct `gh pr merge <N>`, which the guard inspects.

   **GitHub remote-access and publication routing.** A `gh` / GitHub API failure that names
   `127.0.0.1:9`, or connection-refused to a local proxy/discard port, is sandbox egress refusal,
   not evidence that the repository, PR, branch, or CI state failed. Prefer an available GitHub
   connector for remote readback and GitHub-native PR/issue metadata. For a tracked repository file
   on an existing lane branch with a configured `origin`, the publication route is the ordinary local
   path — edit, commit, then `git push` that lane branch — not a connector file-create/update upload.
   This route choice adds no chat permission gate: commit/push authority remains the work-unit
   completion rule plus the harness permission prompt already named in `AGENTS.md` and
   `.agents/workflow-overlay/safety-rules.md`. A connector's unverified-destination export refusal is
   specific to that attempted connector disclosure; it is not evidence that an ordinary lane push
   needs separate chat approval. Avoid the false block by choosing the local Git route before the
   connector call. Once an export refusal has fired, do not switch tools to achieve the same
   disclosure without the explicit destination approval the refusal requires. If `gh` is needed for
   remote metadata/readback, network escalation is a bounded owner-gated fallback for that operation
   only. Without a connector result, successful lane push, or escalated readback, remote state is
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
   `risk/blocked-for-merge-policy` label, `mergeable == MERGEABLE`, the `forseti-harness-tests` check
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
   - **Server-side end-state adopted 2026-07-11:** classic branch protection now requires
     `forseti-harness-tests` with `strict: true`, requires a PR, includes administrators,
     and disables force-push/deletion. Zero required approvals preserves the accepted
     low-risk solo-lane policy while the router/bot retains its narrower opt-in rules.
   - **Former residual closed:** a human or other harness can no longer merge a behind or
     red PR through the ordinary GitHub merge path; `main-red-alert` remains detective defense in depth.
13. **PR cadence — major durable point, not every subpoint.** A lane should open a focused PR after
   each **major durable point**: one coherent, owner-reviewable decision or artifact boundary that
   future agents may rely on. Examples include a first customer / ICP target selection, proof-gate
   change, buyer-risk doctrine change, data-spine boundary change, roster-scope implication, or an
   implementation-scoping decision that closes its work unit (item 14: a scoping artifact produced
   mid-chain under pre-granted implementation authority rides with its chain, not as its own PR).
   Do **not** split every thought, objection, or supporting
   refinement into its own PR; group subpoints when they change the same durable point, share the same
   controlling sources, and should be reviewed with the same validation and non-claims. If a new major
   point emerges while a lane is already open, either include it only when it is directly coupled to
   the same reviewable decision or split it into a follow-up branch / PR. Each such PR should state:
   what decision changed, why it changed, what stance shifted or was magnified, changed files,
   explicit non-claims, and validation run. This cadence does not grant standing commit, push, or PR
   authority; `.agents/workflow-overlay/safety-rules.md` still requires explicit authorization.
14. **PR boundary — per work unit, fixed at commissioning (owner-directed 2026-07-02).** A lane PR
   is cut per **work unit**, not per pipeline stage. A planning/scoping-only artifact (a route,
   spec, or scoping decision) is not a standalone PR by default: it rides with the work unit that
   produced it, or the chain continues into implementation when authority allows. Where the PR
   boundary sits is decided **at commissioning time** by the commissioning artifact (the handoff
   packet or `/fused` invocation), recorded in the edit-permission grant every such artifact already
   states (the `read-only | docs-write | patch-only | implementation-authorized` preflight field
   owned by `.agents/workflow-overlay/prompt-orchestration.md`):
   - **Pre-granted bounded implementation authority** → the full scope→spec→implement→review chain
     is one work unit landing as **one lane PR**; the owner steers at commissioning time.
   - **Authority deliberately withheld** → the mid-chain owner authorization fork **is** the
     explicit work-unit boundary, and the chain lands as **split PRs**. Withholding is a deliberate
     commissioning choice, never the default drift.
   **Named exceptions — splitting stays correct even with pre-granted authority:** (a) the earlier
   half carries shared-authority doctrine that other concurrent lanes need on `main` promptly
   (example: PR #585 landed the Gate 1/2 contract fold-in together with a read-only scoping route
   while implementation stayed split behind a packet-mandated owner fork); (b) authority is
   deliberately withheld for a mid-chain owner fork (the second bullet above); (c) high-lock-in
   probe-first slicing per the Smallest Complete Intervention rule (`AGENTS.md`).
   **Boundaries:** this rule governs PR *topology*, not merge *authority* — items 7/9/11 and the
   human gate on landing to `main` are unchanged, and pre-granting implementation authority remains
   an owner choice recorded in the commissioning artifact, never an agent default. It is not a
   license for big-bang PRs: item 13's cadence and the Smallest Complete Intervention rule still
   govern work-unit size; this item only fixes where the PR boundary sits relative to the owner
   authorization fork.

## Why core-only CI (evidence)

The original core-only probe was green with **no runtime extras installed** — a fresh virtualenv
holding only `pydantic` + `PyYAML` + `pytest` (no `playwright`, no `cloakbrowser`):

```
243 passed, 1 skipped in 29.44s   (exit 0)
```

That count is historical bootstrap evidence, not a current suite-size claim. The browser and
`cloakbrowser` capture paths are decoupled by design: `*_no_runtime_imports`
contract tests assert the adapters import with no `playwright`/`cloakbrowser`/`requests`/etc., and
the snapshot tests drive fake engines rather than the real backends. CI therefore still needs no
runtime extras; `pytest-xdist==3.8.0` is a test-runner dependency only. A path-filter is deliberately
avoided because a filtered required check can strand docs-only PRs in a permanent "pending" state
and block merges. `pytest==9.0.3` and `pytest-xdist==3.8.0` are pinned so upstream releases cannot
silently change CI overnight. The full suite remains required: `-n 4 --dist=loadfile` matches the
[four-CPU public `ubuntu-latest` runner](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#choosing-github-hosted-runners),
changes only scheduling, keeps every file's tests on one worker, and preserves failures.
`--durations=50 --durations-min=0.25` keeps slow-test evidence visible. PR #876's first parallel
Actions run measured 98.99s for pytest versus 137.17s serial; that observation does not predict the
four-worker plus scan-reuse result before its own live run.

## Explicitly not chosen

- **Version matrix** — single supported target (Python 3.12); revisit if Forseti supports more runtimes.
- **Path-filter** — would risk a stuck required check on docs-only PRs.
- **Dependency caching** — installation is not the measured bottleneck; revisit only if it becomes one.
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

## Enforcement status update (2026-07-11)

1. **Hard gate — active and read back.** `main` requires a pull request and the
   strict `forseti-harness-tests` context, includes administrators, and blocks
   force-push and branch deletion.
2. **Supporting automation — active and read back.** `auto-merge`,
   `pr-risk-router`, and `main-red-alert` were restored after the hard gate.
3. **Native auto-merge — intentionally still off.** The custom opt-in bot remains
   the unattended actor; branch protection is independent of that workflow.

## Non-claims

- CI green is a test-suite signal only — **not** product, runtime, ECR/Cleaning/Judgment, or
  judgment-quality readiness, and not deployment.
- This doctrine does **not** grant any lane blanket commit/push/PR authority; the per-turn or
  accepted-handoff authorization requirement in `.agents/workflow-overlay/safety-rules.md` still
  applies.
- The defense-in-depth merge-when-green discipline complements the server gate; its presence alone
  does not prove it was followed or that any merge actually passed CI.
- Risk-router labels and merge-packet comments are routing/check signal only — **not** validation,
  approval, review acceptance, readiness, or proof that a PR is safe to merge.
- Not validation, readiness, or acceptance of any lane's content beyond "the test suite passed."
```yaml
direction_change_propagation:
  doctrine_changed: >
    Separates GitHub remote readback and native metadata from tracked-file publication: an existing
    lane branch publishes repository files through local edit, commit, and ordinary `git push` to
    its configured origin; connector file uploads are not a push-permission gate, and an export
    refusal is prevented by choosing the correct route before the connector call.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        Already says verified work-unit commit/push/PR preparation proceeds without a typed
        instruction and treats the harness permission prompt as the irreversibility gate; this
        decision now owns the narrower tool route, so duplicating it in the kernel would fork it.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        Already points commit/push policy to this decision and says the workflow proceeds without a
        typed instruction at verified work-unit completion; authorization strength is unchanged.
    - path: .agents/workflow-overlay/prompt-orchestration.md
      reason: >
        Owns prompt artifacts and receiver contracts, not publication tooling for tracked files.
    - path: .agents/workflow-overlay/decision-routing.md
      reason: >
        Owns uncertainty and delegation routing; the publication route is a clear lifecycle rule in
        the existing developer-workflow owner.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        Repository hooks cannot observe or classify an MCP connector call before it happens; this is
        judgment-based route selection, so no fake deterministic gate is added.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: >
        Already indexes the developer-workflow decision at file level; no route or owner moved.
  stale_language_search: >
    rg -n -i "connector for the read/write path|connector.*tracked|tracked.*connector|chat permission gate|unverified-destination" AGENTS.md .agents/workflow-overlay docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  non_claims:
    - not validation
    - not readiness
    - not a bypass of connector export refusals
    - not new commit, push, PR, or merge authority
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Published lane branches now update from main by fetch plus merge, never rebase,
    because force-push is prohibited; the protected-action guard blocks explicit
    published-branch rebase starts before they create an unpushable history.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
    - .agents/hooks/guard_protected_actions.py
    - .agents/hooks/README.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/safety-rules.md
    - .agents/workflow-overlay/validation-gates.md
    - docs/decisions/overlay_enforcement_placement_classification_v0.md
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        The kernel already points lane lifecycle to this decision and separately
        forbids destructive Git; duplicating the update command would fork policy.
    - path: .agents/workflow-overlay/safety-rules.md
      reason: >
        It already delegates commit, push, and pull-request lifecycle policy to
        this decision and names the guard as enforcement.
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        Its enforcement-placement principle already requires mechanically
        checkable lifecycle rules at the tool boundary; no principle changed.
    - path: docs/decisions/overlay_enforcement_placement_classification_v0.md
      reason: >
        EP-03 already classifies Git lifecycle commands as a shell-boundary
        substrate; this change narrows the authorized command route, not placement.
    - path: docs/workflows/forseti_repo_map_v0.md
      reason: >
        It already routes workflow doctrine to the decision and active-hook
        behavior to the hook README; no T1 route moved.
  stale_language_search: >
    rg -n -i "rebase cadence|published.*rebase|rebase.*published|git rebase|pull --rebase"
    AGENTS.md .agents docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  non_claims:
    - not validation or readiness
    - not proof that every harness loads the local guard
    - not prevention of opaque-script or deliberately bypassed rebases
```

Older direction_change_propagation receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
