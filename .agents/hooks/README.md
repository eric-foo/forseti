# Agent enforcement hooks — and how to wire them in any harness

These scripts enforce a few Orca rules at the agent's **tool boundary**. They are
**standalone** — plain Python that reads a tool event as JSON on stdin and signals
via exit code — so they are **harness-portable**: the *logic* runs anywhere; only the
*wiring* (how your agent harness invokes them) is harness-specific.

> **If you are an agent in a harness other than Claude Code:** these hooks are
> **inert until you wire them into your harness's own config.** Read "Wiring per
> harness" below and set up the equivalent. The scripts don't change — only the
> registration does.

## The hooks

| Script | When | Effect |
|---|---|---|
| `guard_protected_actions.py` | **pre-tool** (before a shell/write tool runs) | **HARD-blocks** (exit 2) irreversible / main-affecting actions: an agent's `gh pr merge` → main, push-to-main, force-push, `reset --hard`, `git clean`, and writes into protected external roots. **Allows** a benign lane-branch push. Fires in **all** permission modes. **Fails OPEN** on internal error. |
| `pre_push_guard.py` | local Git **pre-push** adapter policy | Blocks pushes targeting `main`, branch deletes, non-fast-forward updates, and unverifiable update safety when `.githooks/pre-push` is installed through `core.hooksPath`. Bypassable with `--no-verify`; misses GitHub API merges. |
| `check_retrieval_header.py` | **post-tool** (after a write) | Advisory (exit 0): warns if an in-scope artifact is missing its retrieval header. Forward-only; never blocks. |
| `check_repo_map_freshness.py` | **post-tool** (after a write) | Advisory (exit 0): reports structural drift vs the repo map; has a `--strict` gate for commit/CI use. |

Each has a `--selftest`. Rule authority lives in the overlay
(`.agents/workflow-overlay/safety-rules.md`, `validation-gates.md`) — the scripts
reference it, they don't restate it.

## The contract (harness-agnostic)

- **Input:** the harness passes the tool event as **JSON on stdin** — at minimum
  `tool_name` and `tool_input` (with `command` for shell tools, `file_path` for writes).
- **Output / exit code:** **`2` = block** the tool call (stderr explains why); **`0` = allow**.
  On any internal error the guard **exits 0 (fails open)** so a hook bug never bricks the agent.
- Any harness that can run a command with the tool event on stdin and honor a
  blocking exit code can use these as-is (adapt field names with a tiny shim if yours differ).

## Wiring per harness

### Claude Code (current)
Register in the repo's tracked `.claude/settings.json`:
```json
"hooks": {
  "PreToolUse":  [ { "matcher": "Bash|PowerShell|Write|Edit|MultiEdit|NotebookEdit",
                     "hooks": [ { "type": "command", "command": "python .agents/hooks/guard_protected_actions.py", "timeout": 10 } ] } ],
  "PostToolUse": [ { "matcher": "Write|Edit",
                     "hooks": [ { "type": "command", "command": "python .agents/hooks/check_retrieval_header.py --hook",   "timeout": 10 },
                                { "type": "command", "command": "python .agents/hooks/check_repo_map_freshness.py --hook", "timeout": 10 } ] } ]
}
```
Hooks load at session start — **restart the session** after editing settings.
Verify: `python .agents/hooks/guard_protected_actions.py --selftest`.

### Another harness (e.g. Codex, or your own runner)
`.claude/settings.json` is **not read** by other harnesses, so:
1. If your harness has a **pre-tool / post-tool command-hook** mechanism, register
   `guard_protected_actions.py` on the pre-tool event for shell + write tools,
   honoring **exit 2 = block**. Register the `--hook` checkers on the post-tool
   event for write tools. Map your harness payload onto `tool_name` /
   `tool_input` on stdin.
2. If your harness has no equivalent hook API, install the tracked local Git
   hook adapters:
   ```powershell
   pwsh .github/scripts/install-local-hooks.ps1
   ```
   This sets `core.hooksPath` to `.githooks`, enabling:
   - `.githooks/pre-push` — blocks pushes targeting `main`, branch deletes, and
     non-fast-forward updates at Git's pre-push boundary.
   - `.githooks/commit-msg` — runs `check_repo_map_freshness.py --commit-msg`.
3. Confirm with:
   ```powershell
   python .agents/hooks/guard_protected_actions.py --selftest
   python .agents/hooks/check_repo_map_freshness.py --selftest
   python .agents/hooks/pre_push_guard.py --selftest
   pwsh .github/scripts/install-local-hooks.ps1 -VerifyOnly
   ```

### If your harness has no hook mechanism
The scripts can't auto-fire, so fall back to **enforcement outside the agent**:
- the tracked Git hooks under `.githooks/`, installed with
  `.github/scripts/install-local-hooks.ps1`, to catch `git push` and commit-time
  repo-map freshness — note they **miss `gh pr merge`** (a GitHub API call) and
  are **bypassable** with `--no-verify`;
- **CI** (already runs the test gate on every PR);
- the **merge-when-green discipline** in `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`.

## Scope boundary (read this)

These hooks enforce **only where they are wired.** A harness without them wired is
**not** protected by them. Two durability notes carry over from the dev-workflow doctrine:
- the **git-lifecycle protection (EP-03** — merge/push-to-main/force/destructive) is
  **portable** — wire it in any harness and it behaves the same;
- the **protected-path protection (EP-01)** is tuned to a machine's external layout, so
  it stays **per-machine** — other clones adjust their own externals.

The only **harness-agnostic, unbypassable** gate is **server-side branch protection**,
which is the deferred target (currently **403-blocked** on this private/free repo; see
the dev-workflow doctrine). Until then, structure-B enforcement is **per-harness**: live
wherever these hooks are wired, absent everywhere else.

---
*Navigation / setup doc only. These are advisory + enforcement tooling, not validation,
readiness, or source-of-truth promotion.*
