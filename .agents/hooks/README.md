# Agent enforcement hooks — and how to wire them in any harness

These scripts enforce a few Forseti rules at the agent's **tool boundary**. They are
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
| `.codex/hooks/forseti_guard_codex_adapter.py` | Codex **PreToolUse** adapter | Runs `guard_protected_actions.py`, converts guard denials into Codex's native JSON `permissionDecision: deny` response, maps Codex `apply_patch` patch targets through the existing EP-01 protected-path check, blocks writes into registered non-current worktrees, and blocks raw shell durable-write primitives for repo source/docs files. |
| `pre_push_guard.py` | local Git **pre-push** adapter policy | Blocks pushes targeting `main`, branch deletes, non-fast-forward updates, and unverifiable update safety when `.githooks/pre-push` is installed through `core.hooksPath`; for allowed lane pushes it then mirrors selected strict CI gates (`check_map_links.py --strict`, `header_index.py --strict`, `check_review_routing.py --strict`, `check_source_input_hashes.py --strict`; diff-scoped base `origin/main`, same as CI) so durable-doc or source-input hash gate misses fail before push instead of in CI. Bypassable with `--no-verify`; misses GitHub API merges; CI stays the authoritative gate. |
| `check_source_input_hashes.py` | manual + **CI** (`--strict`) + local pre-push | Diff-scoped, forward-only: list-style JSON `source_inputs[]` records with repo-local `source_pointer` + `sha256` must match current file bytes when the artifact or referenced source changed. Provenance freshness only; never semantic validation, generated-artifact completeness, readiness, or source quality. Backlog via `--audit`; `--selftest` present. |
| `check_retrieval_header.py` | **post-tool** (after a write) | Advisory (exit 0): warns if an in-scope artifact is missing its retrieval header. Forward-only; never blocks. |
| `check_dcp_receipt_hygiene.py` | manual / commit / CI candidate | Advisory by default; `--strict` fails on deterministic DCP receipt storage defects in changed durable docs: more than two inline receipts, missing archive pointer, or unauthorized standalone DCP receipt files. Shape only; never receipt truth, validation, readiness, or acceptance. |
| `check_registry_list_sync.py` | manual / commit / CI candidate | Advisory by default; `--strict` fails on explicitly registered vocabulary-list drift. Current binding: Foundation Allowed Signal Uses must be contained by the engagement registry Signal Use Classification list. Shape only; never category correctness or auto-promotion. |
| `check_engagement_stale_phrases.py` | manual / commit / CI candidate | Advisory by default; `--strict` fails on curated stale engagement/resonance doctrine phrases in live doctrine paths. Leakage detection only; default excludes historical prompts/reviews and DCP self-reference noise. |
| `check_review_output_provenance.py` | manual / commit / CI candidate | Advisory by default; `--strict` fails on changed review outputs missing retrieval-header shape, `reviewed_by`, `authored_by`, review-use boundary/non-approval wording, balanced/valid fences, proper `diff` fencing, non-collapsed diffs, observed-check wording, or whitespace hygiene. Shape/integrity only; never reviewer identity verification, de-correlation truth, approval, validation, or review quality. |
| `check_csb_scanning_artifact.py` | manual + **CI** (`--diff origin/main --strict`) | Diff-scoped, forward-only for CSB-first scan artifacts under `docs/research/`: validates minimum receipt shape including capture-request accounting and the Creator Registry preflight block (`not_applicable` for non-social requests; receipt-backed `can_start_new_capture` for new social creator/account capture). Shape only; never scan quality, buyer proof, registry truth, or Capture route authorization. |
| `check_review_routing.py` | **commit-msg** (advisory) + **CI** (`--strict`) | Diff-scoped, forward-only: a change touching code roots (`forseti-harness/`, `.agents/hooks/`) must add a review artifact under `docs/prompts/reviews/`/`docs/review-outputs/` or carry a shape-valid `review_routing_status:` commit-message line (`routed <existing path>` / `blocked -- reason` / `not_needed -- reason`). Disposition presence/shape only; never review quality, reason truth, or whether review should have been recommended. |
| `check_handoff_pointers.py` | **CI** (`--strict`) | Diff-scoped, forward-only: handoff-packet paths (`docs/workflows/*handoff*.md`, `docs/prompts/handoffs/*.md`) referenced in changed durable `.md` files must resolve in the same tree, or the pointer line must carry an explicit pin (`branch` / `PR #N` / `origin/<ref>`) or exemption marker. Pointer shape only; never packet content freshness, pin truth, or source-choice correctness. Backlog via `--audit` (never gated). |
| `check_repo_map_freshness.py` | **post-tool** (after a write) | Reports structural drift vs the repo map as advisory output; exits 2 when the repo map itself is dirty after edit so the next action is an explicit-path commit; has a `--strict` gate for commit/CI use. |
| `check_search_surface_google_route.py` | **post-tool** (after a write) + CI | Advisory on live writes and strict in CI for the checkable Google search-surface route shell: Google Search URLs use `hl=en&gl=us&pws=0`, US-parameterized artifacts carry the physical-locality non-claim, and Google sorry/IP pages are not preserved in durable docs. |
| `remind_sci.py` | **pre-tool** (before a `git commit`) | Advisory (exit 0): when the commit includes durable-artifact changes, re-injects the Smallest Complete Intervention rule (verbatim from AGENTS.md) as a nudge before scope is locked in. Never blocks; silent for code/scratch/config-only commits. |

Each has a `--selftest`. Each script names its own rule authority in its module
header and references that source instead of restating it.

## The contract (harness-agnostic)

- **Input:** the harness passes the tool event as **JSON on stdin** — at minimum
  `tool_name` and `tool_input` (with `command` for shell tools, `file_path` for writes).
- **Output / exit code:** for the raw Forseti guard, **`2` = block** the tool call
  (stderr explains why); **`0` = allow**.
  On any internal error the guard **exits 0 (fails open)** so a hook bug never bricks the agent.
- For the repo-map PostToolUse checker, **`2` = stop and commit the dirty repo
  map explicitly now**; **`0` = advisory or silent**.
- Any harness that can run a command with the tool event on stdin and honor a
  blocking exit code can use these as-is (adapt field names with a tiny shim if yours differ).
- Harnesses with their own denial protocol should use a small adapter rather than
  assuming stderr + exit code is the only blocking contract. Codex uses
  `.codex/hooks/forseti_guard_codex_adapter.py` for that translation.

## Wiring per harness

### Claude Code (current)
Register in the repo's tracked `.claude/settings.json`:
```json
"hooks": {
  "PreToolUse":  [ { "matcher": "Bash|PowerShell|Write|Edit|MultiEdit|NotebookEdit",
                     "hooks": [ { "type": "command", "command": "python .agents/hooks/guard_protected_actions.py", "timeout": 10 } ] } ],
  "PostToolUse": [ { "matcher": "Write|Edit|MultiEdit",
                     "hooks": [ { "type": "command", "command": "python .agents/hooks/check_retrieval_header.py --hook",   "timeout": 10 },
                                { "type": "command", "command": "python .agents/hooks/check_repo_map_freshness.py --hook", "timeout": 10 } ] } ]
}
```
Hooks load at session start — **restart the session** after editing settings.
Verify:
```powershell
python .agents/hooks/guard_protected_actions.py --selftest
python .agents/hooks/check_dcp_receipt_hygiene.py --selftest
python .agents/hooks/check_registry_list_sync.py --selftest
python .agents/hooks/check_engagement_stale_phrases.py --selftest
python .agents/hooks/check_review_output_provenance.py --selftest
python .agents/hooks/check_review_output_provenance.py --diff origin/main --strict
python .agents/hooks/check_review_routing.py --selftest
python .agents/hooks/check_handoff_pointers.py --selftest
python .agents/hooks/check_source_input_hashes.py --selftest
python .agents/hooks/check_source_input_hashes.py --strict
python .agents/hooks/check_repo_map_freshness.py --selftest
python .agents/hooks/check_search_surface_google_route.py --selftest
python .agents/hooks/check_search_surface_google_route.py --strict --base main
```

### Codex (tracked project hook)
Codex does not read `.claude/settings.json`. Forseti wires Codex through the
tracked project-local `.codex/hooks.json`, which registers:

- `PreToolUse` for `Bash|PowerShell|apply_patch|Edit|Write`;
- `.codex/hooks/forseti_guard_codex_adapter.py` as the command hook.
- `.codex/hooks/orca_guard_codex_adapter.py` remains only as a legacy shim for already-loaded Codex hook sessions; active config should use the Forseti path.
- `PostToolUse` for `apply_patch|Edit|Write`;
- `.agents/hooks/check_repo_map_freshness.py --hook` as the repo-map commit interrupt / freshness advisory.
- `.agents/hooks/check_search_surface_google_route.py --hook` as the Google search-surface route policy advisory.

The adapter preserves the shared guard logic but returns Codex's native denial
shape:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "..."
  }
}
```

It also parses Codex `apply_patch` headers (`*** Add/Update/Delete File:` and
`*** Move to:`) and checks those paths through the EP-01 protected-path rule,
because Codex reports patch edits as `tool_name: "apply_patch"` rather than
Claude-style `Write` / `Edit` events.

The adapter additionally blocks Codex write tools when the target is inside a
registered git worktree other than the one running the hook. If a lane needs
that worktree, reroot Codex in the target worktree and rerun the lane-start
writeability preflight; do not edit nested worktrees from the parent checkout.

For `Bash` / `PowerShell`, the adapter blocks raw durable-write primitives when
the command text names repo source/docs file types (`.md`, `.py`, `.yml`,
`.yaml`, `.json`, `.toml`, `.ps1`). This is a prevention guard for the known
failure class, not universal shell-write detection; use `apply_patch` from the
active worktree for source edits.

The repo-map checker also parses Codex `apply_patch` headers in PostToolUse
mode. If the edited target is `docs/workflows/forseti_repo_map_v0.md` and Git still
shows that map dirty, it returns exit code 2 and tells the agent to commit that
file immediately with `git commit --only -- docs/workflows/forseti_repo_map_v0.md`.

Codex only loads project-local hooks after the project `.codex/` layer is
trusted. In a Codex session, open `/hooks` if Codex reports new or changed hooks
that need review.

Verify:
```powershell
python .agents/hooks/guard_protected_actions.py --selftest
python .agents/hooks/check_dcp_receipt_hygiene.py --selftest
python .agents/hooks/check_registry_list_sync.py --selftest
python .agents/hooks/check_engagement_stale_phrases.py --selftest
python .agents/hooks/check_review_output_provenance.py --selftest
python .agents/hooks/check_review_output_provenance.py --diff origin/main --strict
python .agents/hooks/check_review_routing.py --selftest
python .agents/hooks/check_handoff_pointers.py --selftest
python .agents/hooks/check_source_input_hashes.py --selftest
python .agents/hooks/check_source_input_hashes.py --strict
python .agents/hooks/check_repo_map_freshness.py --selftest
python .agents/hooks/check_search_surface_google_route.py --selftest
python .agents/hooks/check_search_surface_google_route.py --strict --base main
python .codex/hooks/forseti_guard_codex_adapter.py --selftest
```

### Another harness
`.claude/settings.json` is **not read** by other harnesses, so:
1. If your harness has a **pre-tool / post-tool command-hook** mechanism, register
   `guard_protected_actions.py` on the pre-tool event for shell + write tools,
   honoring **exit 2 = block**. Register the `--hook` checkers on the post-tool
   event for write tools, including your harness's multi-edit / apply-patch
   equivalent. Map your harness payload onto `tool_name` / `tool_input` on stdin.
   The repo-map checker intentionally exits 2 when the repo map itself remains
   dirty after edit; honor that as a stop-and-commit interrupt if your harness
   supports blocking post-tool hooks.
2. If your harness has no equivalent hook API, install the tracked local Git
   hook adapters:
   ```powershell
   pwsh .github/scripts/install-local-hooks.ps1
   ```
   This sets `core.hooksPath` to `.githooks`, enabling:
   - `.githooks/pre-push` — blocks pushes targeting `main`, branch deletes, and
     non-fast-forward updates at Git's pre-push boundary, then mirrors the
     selected strict CI gates over the outgoing change (see the `pre_push_guard.py`
     row above).
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
