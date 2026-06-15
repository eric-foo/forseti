---
retrieval_header_version: 1
artifact_role: Decision proposal (NOT accepted — awaiting owner sign-off)
scope: >
  Proposes enforcing "branch up-to-date with main before merge" across all merge
  paths (not just the auto-merge bot), to stop recurring red-main from cross-file
  breaks that each PR passed individually. Companion to the dev-workflow CI +
  branch-protection doctrine; if accepted it amends items 7/9 or adds a new item.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
  - .github/workflows/auto-merge.yml
  - .github/scripts/merge-when-green.ps1
  - .agents/hooks/guard_protected_actions.py
---

# Proposal — Up-to-Date-Before-Merge Enforcement Across All Merge Paths v0

## Status

**PROPOSAL — not accepted.** Awaiting owner decision. Companion to
`docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`; if accepted it amends Decision
items 7 and 9 (or adds a new item). This document proposes; it changes nothing.

## Problem (observed)

Recurring **red main from cross-file breaks** — two instances in one session (2026-06-15):

1. `demand_durability_capture_pilot_v0.md` `open_next` pointed to renamed (`demand_proxy_*` ->
   `demand_durability_indicator_*`) files (fixed via PR #116).
2. `judgment_spine_c2_ledger_read_contract_v0.md` `open_next` pointed to a deliberately branch-only
   file (`..._demand_read_machinery_architecture_v0.md`).

Each turned `push:main` CI red and blocked every green-gated merge (the bot included) until fixed.

## Root cause

CI runs per-PR as **merge-with-base**, so it *does* test the combined state — but only against the
base **at PR-CI time**. A PR merged while **behind** `main` is never re-tested against *current* main.
The "up-to-date before merge" guarantee is enforced for exactly **one of three** merge paths:

| Merge path | Up-to-date (`behind_by == 0`) enforced? |
|---|---|
| Auto-merge bot (Decision item 9) | **Yes** ✅ |
| In-session agent self-merge (item 7 guard) | **No** — checks CLEAN+green+label only (documented residual) ❌ |
| Human / other-harness `gh pr merge` CLI | **No** — no up-to-date check ❌ |

So two independently-green PRs can still **combine-break** main through the latter two paths.

## What up-to-date enforcement fixes — and what it does not

- **FIXES — Class 1 (combination breaks):** PR-A adds a reference; PR-B renames/removes the target;
  each is green alone. With up-to-date enforcement the second PR must include the first, and its CI
  re-tests the combination → caught. *(The demand_proxy case.)*
- **DOES NOT FIX — Class 2 (intentional forward-refs):** a PR references a file that is deliberately
  branch-only and not yet on main. Up-to-date cannot help (the target is never on main). *(The
  judgment_spine case.)* → needs **annotation discipline** (mark as known-nonresolving debt; the link
  check already tolerates such entries).

## Options

- **O1 — Server-side (complete, harness-agnostic).** Branch protection "require branches up to date"
  + optionally GitHub's merge queue. The real end-state; already the doctrine's deferred target
  (items 2/4). **Blocked:** HTTP 403 on this private+free repo — needs GitHub Pro/Team or making the
  repo public. **Only this** fully prevents a determined raw-CLI bypass.
- **O2 — Interim: close the controllable paths (within current constraints).**
  - **O2a:** add `behind_by == 0` to the in-session guard's self-merge allowance (closes the
    documented residual; covers Claude-Code agent merges). Touches the EP-03 guard
    (`.agents/hooks/guard_protected_actions.py`, enforcement-lane-owned).
  - **O2b:** make the human merge helper (`.github/scripts/merge-when-green.ps1`) refuse/warn when
    `behind_by != 0` (covers disciplined human merges).
  - The bot already enforces it.
  - **Residual:** a raw `gh pr merge` by a human or non-Claude harness still bypasses — only O1 closes that.
- **O3 — Detective backstop (pairs with prevention).** A fast red-main signal (a `push:main`-red
  alert, or the lane-health detector) so breaks that still land are fixed in minutes, not discovered
  by the next lane. Cheap; bounds blast radius rather than preventing.
- **O4 — Reduce the Class-2 sub-case.** Annotation discipline for intentional forward-refs (when to
  annotate as known-nonresolving vs wait for the target to land). Closes the judgment_spine class that
  O1/O2 cannot.

## Recommendation (layered)

1. **Now (cheap, in-constraints):** O2a + O2b (close the agent and disciplined-human paths) + O4
   (forward-ref annotation discipline). Together these eliminate Class-1 combination breaks on the
   controllable paths and the Class-2 forward-ref breaks.
2. **Cheap safety net:** O3 (fast red-main detection).
3. **Deferred end-state:** O1 (server-side require-up-to-date + merge queue) on a plan upgrade or a
   public repo — the only complete, harness-agnostic, unbypassable guarantee.

## Non-claims / honest limits

- No client-side check fully prevents a determined raw `gh pr merge` bypass; the complete guarantee is
  **server-side only** (O1).
- Up-to-date enforcement does **not** catch intentional forward-refs (Class 2) — O4 covers that.
- O2a touches the EP-03 guard (enforcement-lane-owned); adoption requires that lane / owner.
- This is a **proposal**, not accepted; not validation, readiness, or an enforcement change in itself.

## Owner decision needed

Which of O2a / O2b / O3 / O4 to adopt now, and whether to schedule O1 (plan upgrade / public repo).
