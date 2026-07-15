# Agent enforcement hooks — and how to wire them in any harness

These scripts enforce a few Forseti rules at the agent's **tool boundary**. They are
**self-contained as a directory** — plain stdlib Python (plus PyYAML for the
placement checker) that reads a tool event as JSON on stdin and signals via exit
code; shared helpers live in the sibling `_hooklib.py`, so port the whole
`.agents/hooks/` directory, not single files. That makes them **harness-portable**:
the *logic* runs anywhere; only the *wiring* (how your agent harness invokes them)
is harness-specific.

> **If you are an agent in a harness other than Claude Code:** these hooks are
> **inert until you wire them into your harness's own config.** Read "Wiring per
> harness" below and set up the equivalent. The scripts don't change — only the
> registration does.

## The hooks

| Script | When | Effect |
|---|---|---|
| `guard_protected_actions.py` | **pre-tool** (before a shell/write tool runs) | **HARD-blocks** (exit 2) direct push-to-main, force-push, `reset --hard`, `git clean`, protected external-root writes, explicit rebase starts on a mechanically confirmed published lane, and `gh pr merge --admin`. A direct `gh pr merge <N>` is allowed only for the current lane branch when the PR targets `main`, is same-repo, `CLEAN`, all checks are green, carries `agent-automerge`, and has no `risk/blocked-for-merge-policy` hold. `risk/manual-review-required` keeps the unattended bot out but does not choose a human actor after the resident completion/review and home/Chief Architect adjudication gate closes; that judgment completion is not mechanically certified by the label. Benign lane pushes, published-lane fetch-plus-merge updates, and rebase recovery remain allowed. Fires in **all** permission modes. Non-merge probes fail open on internal error; merge authorization fails closed. |
| `.codex/hooks/forseti_guard_codex_adapter.py` | Codex **PreToolUse** adapter | Runs `guard_protected_actions.py`, converts guard denials into Codex's native JSON `permissionDecision: deny` response, maps Codex `apply_patch` patch targets through the existing EP-01 protected-path check, blocks writes into registered non-current worktrees, and blocks raw shell durable-write primitives for repo source/docs files. |
| `pre_push_guard.py` | local Git **pre-push** adapter policy | Blocks pushes targeting `main`, branch deletes, non-fast-forward updates, and unverifiable update safety when `.githooks/pre-push` is installed through `core.hooksPath`; for allowed lane pushes it mirrors ten selected strict CI gates over local `origin/main...HEAD`, including the conditional harness coupling contracts. CI runs the same gate modes against its exact event base SHA. A gate failure or launch error blocks the push. Bypassable with `--no-verify`; misses GitHub API merges; CI stays authoritative. |
| `check_harness_coupling.py` | manual + **CI** (`--strict`) + local pre-push | Diff-scoped adapter over existing inventory and policy-pin contract tests. It runs only when the outgoing change touches `forseti-harness/**/*.py` or `forseti-harness/data_lake/lake_touchpoint_inventory_v0.json`; an unresolvable diff or unlaunchable test fails closed. Coupling preflight only: not the full harness suite, validation, readiness, or proof that every CI failure is prevented. `--selftest` present. |
| `check_source_input_hashes.py` | manual + **CI** (`--strict`) + local pre-push | Diff-scoped, forward-only: list-style JSON `source_inputs[]` records with repo-local `source_pointer` + `sha256` must match current file bytes (CRLF-normalized), and source-capture packet manifests (top-level `manifest_version`) must have top-level `preserved_files[]` records whose `relative_packet_path` + `sha256` match current raw stored bytes resolved against the manifest's own directory, when the artifact or referenced file changed. Provenance freshness only; never semantic validation, generated-artifact completeness, readiness, or source quality. Backlog via `--audit`; `--selftest` present. |
| `check_retrieval_header.py` | **post-tool** (after a write) | Advisory (exit 0): warns if an in-scope artifact is missing its retrieval header. Forward-only; never blocks. |
| `check_dcp_receipt.py` | **CI** (`--strict`) + manual maintenance | Diff-scoped strict gate validates the shape of real DCP receipts/blockers present in changed Markdown files and reports changed-file/receipt counts. `--audit` is maintenance-only for checker/contract changes or explicit legacy-corpus repair. Shape only; never receipt need, truth, validation, readiness, or acceptance. |
| `check_dcp_receipt_hygiene.py` | manual / commit / CI candidate | Advisory by default; `--strict` fails on deterministic DCP receipt storage defects in changed durable docs: more than two inline receipts or a new unauthorized standalone DCP receipt file. The legacy archive is frozen and pointers are not required. Shape only; never receipt truth, validation, readiness, or acceptance. |
| `check_registry_list_sync.py` | manual / commit / CI candidate | Advisory by default; `--strict` fails on explicitly registered vocabulary-list drift. Current binding: Foundation Allowed Signal Uses must be contained by the engagement registry Signal Use Classification list. Shape only; never category correctness or auto-promotion. |
| `check_engagement_stale_phrases.py` | manual / commit / CI candidate | Advisory by default; `--strict` fails on curated stale engagement/resonance doctrine phrases in live doctrine paths. Leakage detection only; default excludes historical prompts/reviews and DCP self-reference noise. |
| `check_review_output_provenance.py` | manual / commit / CI candidate | Advisory by default; `--strict` fails on changed review outputs missing retrieval-header shape, `reviewed_by`, `authored_by`, review-use boundary/non-approval wording, balanced/valid fences, proper `diff` fencing, non-collapsed diffs, observed-check wording, or whitespace hygiene. Shape/integrity only; never reviewer identity verification, de-correlation truth, approval, validation, or review quality. |
| `check_csb_scanning_artifact.py` | manual + **CI** (`--diff "$FORSETI_DIFF_BASE" --strict`) | Diff-scoped, forward-only for CSB-first scan artifacts under `docs/research/`: validates minimum receipt shape including capture-request accounting and the Creator Registry preflight block (`not_applicable` for non-social requests; receipt-backed `can_start_new_capture` for new social creator/account capture). Shape only; never scan quality, buyer proof, registry truth, or Capture route authorization. |
| `check_review_routing.py` | **commit-msg** (advisory) + **CI** (`--strict`) | Diff-scoped, forward-only: a change touching code roots (`forseti-harness/`, `.agents/hooks/`) must add a review artifact under `docs/prompts/reviews/`/`docs/review-outputs/` or carry a shape-valid `review_routing_status:` commit-message line (`routed <existing path>` / `blocked -- reason` / `not_needed -- reason`). Disposition presence/shape only; never review quality, reason truth, or whether review should have been recommended. |
| `check_handoff_pointers.py` | **CI** (`--strict`) | Diff-scoped, forward-only: handoff-packet paths (`docs/workflows/*handoff*.md`, `docs/prompts/handoffs/*.md`) referenced in changed durable `.md` files must resolve in the same tree, or the pointer line must carry an explicit pin (`branch` / `PR #N` / `origin/<ref>`) or exemption marker. Pointer shape only; never packet content freshness, pin truth, or source-choice correctness. Backlog via `--audit` (never gated). |
| `check_prompt_output_mode.py` | **CI** (`--strict`) | Diff-scoped, forward-only: changed prompt artifacts under `docs/prompts/**` (templates and READMEs excluded) must carry an output-mode declaration naming at least one closed-set token (`chat-only` / `file-write` / `review-report` / `paste-ready-chat` / `patch-queue`). Presence + token shape only; "exactly one, correctly scoped to this artifact" stays resident judgment; never prompt quality or mode correctness. Backlog via `--audit` (never gated). |
| `check_review_summary.py` | **CI** (`--strict`) | Diff-scoped, forward-only over changed `docs/review-outputs/**` files: real `review_summary` blocks must not carry forbidden process keys, `report_path` must resolve on disk, failed-write blocks keep the bound failed shape, and `recommendation` is non-blank when present. Full `recommendation` enum membership is `--audit` advisory only (known extended vocabulary in delegated-review-patch lanes). Shape only; never review quality or truth. Non-overlap: header/provenance/fencing stays with `check_review_output_provenance.py`. |
| `check_hash_pin_freshness.py` | manual + **CI** (`--strict`) + local pre-push | Diff-scoped, forward-only: markdown freshness hash pins (labeled `path:` + `sha256:` bullet pairs; `source_captures/**/receipt.md` preserved-file bullets) must match current CRLF-normalized file bytes when the pin-carrying doc or its target changed. The markdown analog of `check_source_input_hashes.py` (JSON); provenance-style manifest tables and source-read ledgers are deliberately not parsed as pins. Pin freshness only; never semantic validity, source quality, or skill correctness. Backlog via `--audit` (never gated). |
| `check_repo_map_freshness.py` | **post-tool** (after a write) | Reports structural drift vs the repo map as advisory output; exits 2 when the repo map itself is dirty after edit so the next action is an explicit-path commit; has a `--strict` gate for commit/CI use. |
| `check_search_surface_google_route.py` | **post-tool** (after a write) + CI | Advisory on live writes and strict in CI for the checkable Google search-surface route shell: Google Search URLs use `hl=en&gl=us&pws=0`, US-parameterized artifacts carry the physical-locality non-claim, and Google sorry/IP pages are not preserved in durable docs. |
| `remind_sci.py` | **pre-tool** (before a `git commit`) | Advisory (exit 0): when the commit includes durable-artifact changes, re-injects the Smallest Complete Intervention rule (verbatim from AGENTS.md) as a nudge before scope is locked in. Never blocks; silent for code/scratch/config-only commits. |
| `header_index.py` | manual + **CI** (`--strict`) + session capsule | Generates the on-demand retrieval index, advisory health/backlog views, and the diff-scoped forward-only header/orphan gate. Inventory and shape only; never readiness or source authority. |
| `check_map_links.py` | manual + **CI** (`--strict`) | Checks map/submap paths, `open_next` targets, folder reachability, inline path shape, and direct target existence for the Artifact Roles and product-spine Doctrine Index live-router tables. Path existence only; never route truth, currentness, authority, or completeness proof. |
| `check_dcp_receipt.py` | **CI** (diff-scoped `--strict`) | Validates the deterministic shape of changed doctrine-change receipts and blockers. It cannot decide whether a receipt is required or whether listed propagation work actually happened. |
| `check_placement.py` | **post-tool** (after a write) + `--strict` for commit/CI | Advisory WARN when a written path has no declared home in `repo-structure.yaml` (EP-04); `--strict` is the full-tree gate. Placement shape only; never authority, validation, or readiness. |
| `check_full_gt_claims.py` | **post-tool** (after a write) + **CI** (`--changed --strict`) | Flags added `.md` lines whose full-GT claim language is not bounded by ballast wording and does not sit in a claim-owning surface. Shape/placement only; never claim truth. |
| `check_prompt_provenance.py` | **post-tool** (after a write under `docs/prompts/**`) | Advisory (exit 0): injects the Forseti Prompt Preflight checklist. Once-per-session throttle: the full checklist fires on the FIRST in-scope prompt write of a session; later writes get a one-line pointer (fails open to the full checklist). |
| `check_shared_files_dirty.py` | **Stop** (turn end) | Advisory (exit 0): warns when a commit-once-whole shared file (repo map, `.claude/settings.json`, source-of-truth) is left dirty at end of turn. Never blocks, never auto-commits. |
| `check_token_burn.py` | **Stop** (turn end) | Advisory (exit 0): warns when one turn's prompt size crosses a rung (200K warn / 500K alarm, env-overridable); escalation-throttled so it never nags every turn. |
| `session_context_capsule.py` | **SessionStart** | Prints the lane-state capsule (branch, tree dirt, config-surface dirt, doctrine drift, entry points) into session context. Observed git state only; not doctrine or lane authority. |

Each has a `--selftest`. Each script names its own rule authority in its module
header and references that source instead of restating it.
## Run the CI hook-gate set locally (before pushing)

CI runs every strict hook command registered in `.github/workflows/ci.yml`.
The local pre-push guard mirrors nine selected strict gates, so CI still has
additional hook commands that can fail after a push. Run the complete CI hook
set locally with:

```powershell
pwsh .github/scripts/run-doc-gates.ps1          # run each registered CI hook command
pwsh .github/scripts/run-doc-gates.ps1 -List    # list the commands derived from ci.yml
```

The runner parses both one-line steps and commands inside multiline `run: |`
blocks directly from `.github/workflows/ci.yml`, so the workflow remains the
command source. It intentionally excludes non-hook steps such as
`python -m pytest` and `.github/scripts/*`; run relevant tests separately when
you touch code. This is convenience tooling, not validation or readiness; CI
remains the authoritative gate.

**Shared helpers:** `_hooklib.py` (same directory) owns the helpers the wired
checkers share -- repo-root/path normalization, tool-event parsing (incl. Codex
`apply_patch` headers), the git wrapper, porcelain parsing, shell-segment
splitting, the durable-docs scope base, and the once-per-session marker. The
scripts pin their own directory onto `sys.path` before importing it, so they
still run from any cwd; a harness port must copy the whole `.agents/hooks/`
directory, not individual scripts. **Deliberate exception:**
`guard_protected_actions.py` stays import-free -- an ImportError in an advisory
checker costs one advisory, but in the hard guard it would disable the gate
(including its fail-closed merge path). Do not refactor the guard onto
`_hooklib`.

## The contract (harness-agnostic)

- **CI diff base:** `.github/workflows/ci.yml` exports `FORSETI_DIFF_BASE`
  as the pull request base SHA or push event `before` SHA, then rejects a
  missing, zero, malformed, or unresolvable value before any policy gate.
  Diff-scoped resolvers prefer that exact SHA, then `$GITHUB_BASE_REF`, an
  explicit CLI base, and finally local `origin/main`. Local pre-push does
  not set the CI variable and retains outgoing `origin/main...HEAD` scope.

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
Register in the repo's tracked `.claude/settings.json`. The live wiring (see
that file for the authoritative registration) is:

- **PreToolUse** `Bash|PowerShell|Write|Edit|MultiEdit|NotebookEdit` →
  `guard_protected_actions.py`; **PreToolUse** `Bash|PowerShell` →
  `remind_sci.py --hook`.
- **PostToolUse** `Write|Edit|MultiEdit` → `check_retrieval_header.py`,
  `check_full_gt_claims.py`, `check_repo_map_freshness.py`,
  `check_placement.py`, `check_prompt_provenance.py`,
  `check_search_surface_google_route.py` (each `--hook`, timeout 10).
  NotebookEdit is deliberately pre-tool-guarded but NOT post-tool-checked:
  the post checkers target `.md`/placement surfaces, not notebooks.
- **Stop** (no matcher) → `check_shared_files_dirty.py --hook`,
  `check_token_burn.py`.
- **SessionStart** (no matcher) → `session_context_capsule.py --hook`.

Entry shape per hook:
```json
{ "type": "command",
  "command": "python \"$CLAUDE_PROJECT_DIR/.agents/hooks/<script>.py\" --hook",
  "timeout": 10 }
```
Hooks load at session start — **restart the session** after editing settings.
Verify:
```powershell
python .agents/hooks/_hooklib.py --selftest
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
python .agents/hooks/check_prompt_output_mode.py --selftest
python .agents/hooks/check_review_summary.py --selftest
python .agents/hooks/check_hash_pin_freshness.py --selftest
python .agents/hooks/check_hash_pin_freshness.py --strict
python .agents/hooks/check_repo_map_freshness.py --selftest
python .agents/hooks/check_search_surface_google_route.py --selftest
python .agents/hooks/check_search_surface_google_route.py --strict --base main
python .agents/hooks/check_retrieval_header.py --selftest
python .agents/hooks/check_placement.py --selftest
python .agents/hooks/check_full_gt_claims.py --selftest
python .agents/hooks/check_prompt_provenance.py --selftest
python .agents/hooks/check_shared_files_dirty.py --selftest
python .agents/hooks/check_token_burn.py --selftest
python .agents/hooks/session_context_capsule.py --selftest
python .agents/hooks/remind_sci.py --selftest
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
Registering, discovering, or naming another worktree does not change the
running receiver's root, and this adapter does not reroot collaboration
subagents. Select a receiver actually rooted in the target before repo-changing
dispatch under `.agents/workflow-overlay/decision-routing.md`; the adapter is
the later deterministic denial boundary, not the receiver selector.

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
python .agents/hooks/check_prompt_output_mode.py --selftest
python .agents/hooks/check_review_summary.py --selftest
python .agents/hooks/check_hash_pin_freshness.py --selftest
python .agents/hooks/check_hash_pin_freshness.py --strict
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
   This sets the effective `core.hooksPath` to `.githooks` in the active
   worktree's config when `extensions.worktreeConfig` is enabled, otherwise in
   clone-local config. Verification reads the effective value, so a foreign
   higher-precedence worktree binding fails with both roots named. It enables:
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

The only **harness-agnostic, unbypassable** gate is the active **server-side branch
protection** on main (see the dev-workflow doctrine). Per-harness and local Git hooks
remain defense in depth: they fail earlier and cover destructive local actions, but they
do not weaken or replace the server gate.

---
*Navigation / setup doc only. These are advisory + enforcement tooling, not validation,
readiness, or source-of-truth promotion.*
