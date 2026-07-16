# Forseti Technical Difficulties Log v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Chronological observations of material Forseti workflow or tooling difficulties, their verified impact, corrective owner, and code or doctrine pointers.
use_when:
  - A technical difficulty materially delays a lane, repeats, or causes a corrective repository change.
  - Checking whether an observed workflow failure already has a diagnosis, mitigation, or accepted residual.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/validation-gates.md
  - docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md
```

## Use boundary

This is an append-only operational record, not workflow authority. Each entry
records observed evidence, impact, diagnosis, corrective pointers, validation,
and residuals. The linked doctrine or implementation owns the rule and behavior.
Add a later follow-up rather than rewriting a closed entry; factual corrections
may amend the affected entry and must say what changed.

## TD-2026-07-14-001 — Published lane rebase created an unpushable history

- **Observed:** 2026-07-14, Asia/Singapore.
- **Affected lane:** PR #896, `codex/topfrag-silver-analytics`.
- **State at recording:** corrective patch prepared and locally validated on
  `codex/technical-difficulties-published-rebase-guard`; delegated review and
  merge remain pending.
- **User-visible symptom:** conflict work and lifecycle recovery added several
  minutes after the implementation and review changes were already complete.

### Verified timeline

| Event | Observed time | Evidence |
| --- | --- | --- |
| Published branch updated by ordinary push | 01:29:40 +08:00 | remote-tracking reflog for `origin/codex/topfrag-silver-analytics` |
| Rebase onto `origin/main` started | 01:30:36 +08:00 | `HEAD` reflog |
| Rebase finished after conflict resolution | 01:34:28 +08:00 | branch and `HEAD` reflogs |
| Content-neutral ancestry merge restored a pushable graph | 01:37:59 +08:00 | branch and `HEAD` reflogs |
| Reconciled branch published | 01:38:16 +08:00 | remote-tracking reflog |
| Required CI ran green | 01:38:23–01:39:40 +08:00 | GitHub PR #896 check rollup (`forseti-harness-tests`) |
| PR merged | 01:41:44 +08:00 | GitHub PR #896 `mergedAt` readback |

The recovery interval from rebase start to publication of the reconciled branch
was **7 minutes 40 seconds**. Conflict resolution (01:30:36 to 01:34:28) was real
work that a fetch-plus-merge update would also incur; the **avoidable** portion
was the content-neutral ancestry reconciliation and its republish (01:34:28 to
01:38:16, **3 minutes 48 seconds**), which existed only because a published lane
had been rebased under the no-force-push policy. The 77-second CI run was normal
required validation, not the defect.

### Diagnosis

The controlling doctrine said lanes should follow a “rebase cadence” while the
same doctrine, local protected-action guard, pre-push guard, and server branch
protection prohibit force-push. Rebasing an already-published lane rewrote its
commit identities, so its next ordinary push could not fast-forward. Conflict
resolution was real work, but the additional ancestry-reconciliation step existed
only because the documented update route contradicted the no-force-push policy.

This is repeatable. Repository reflogs show the same published-branch rebase
pattern on multiple recent lane branches. Exact conflict count and duration vary
with overlap, but the non-fast-forward outcome follows whenever a published lane
is rebased and its rewritten commits differ from the remote branch.

### Corrective ownership

- **Rule owner:**
  `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md` distinguishes
  unpublished branches (rebase allowed) from published branches (fetch plus merge).
- **Early enforcement:** `.agents/hooks/guard_protected_actions.py` blocks explicit
  `git rebase` and `git pull --rebase` when local Git state proves the current
  same-name branch is already published. Rebase recovery forms remain allowed.
- **Operator documentation:** `.agents/hooks/README.md` names the guard boundary,
  fail-open publication probe, and allowed route.
- **Focused validation observed:** the protected-action guard and Codex adapter
  self-tests returned `OK`; retrieval-header and DCP receipt-shape/hygiene checks
  returned no findings for the changed files; `check_map_links.py --strict`
  returned zero findings; and the full `forseti-harness` pytest suite reached
  100% with exit code 0 (seven skips, warnings only). These are local validation
  signals, not delegated review or merge state.

### Accepted residuals

- A plain `git pull` can still be affected by user Git configuration; doctrine
  therefore requires explicit fetch plus merge, while the guard only blocks
  commands it can identify without guessing.
- Opaque shell scripts, alternate harnesses without the tracked hook wiring, and
  deliberate hook bypass remain outside this local guard. Server-side no-force
  protection still prevents the unsafe publication result.
- Published-branch merges can still conflict. They preserve pushability and make
  the unavoidable conflict work visible; they do not eliminate overlap.
- Sandbox approval latency and required CI time remain separate operating costs.
  Neither was the root cause of this incident.

### Validation-environment note

Two local validation attempts failed before tests ran: `py_compile` was denied
while creating `.agents/hooks/__pycache__`, and pytest-xdist was denied while
creating `C:\tmp\pytest_rebase_guard`. ACL readback showed deny entries on the
hook cache directory, and the temp-root failure reproduced despite `C:\tmp`
being an intended writable root. The successful bounded route was
`PYTHONDONTWRITEBYTECODE=1` plus a fresh pytest `--basetemp` inside the active
worktree. No production or CI code change is justified: GitHub CI runs on Ubuntu,
the repository suite passed through the bounded local route, and changing host
ACLs is outside this repository's ownership.

### Non-claims

- Not a Silver-data, analytics, capture, or runtime defect.
- Not proof that PR #896 content was incorrect; its required CI completed green.
- Not proof that every historical rebase caused delay or conflict.
- Not validation, readiness, or merge approval for the corrective patch.

## TD-2026-07-16-002 — Sandboxed tool completion stalls reopened after interruptions

- **Observed:** 2026-07-16, Asia/Singapore.
- **User-visible symptom:** small patch and read operations remained running for
  roughly 80 to 265 seconds despite 20-second command budgets.
- **Verified contrast:** equivalent read-only commands through per-operation
  escalation completed in 0.3 to 0.6 seconds; same-worktree atomic edits
  completed in 0.4 seconds; the Codex guard adapter self-test completed in 1.7
  seconds.
- **Patch result:** the manually stopped built-in patch changed none of its four
  intended files.

### Diagnosis and correction

The dominant observed delay was the sandboxed tool route or its result-return
lifecycle, not Git, Python, the atomic helper, or the Forseti guard runtime. The
repository cannot repair that host component. A second process defect amplified
the cost: the circuit breaker expired at the end of a turn, so an interruption
or follow-up message reopened a route already observed to be stalled.

`AGENTS.md` now keeps that circuit open for the task/thread and requires later
context to inherit the observed stall. Safe shell work may use the one allowed
per-operation escalated retry and then that working route. After a patch stall,
the same-worktree atomic exact-edit helper remains the bounded fallback. No Luna
or separate worktree is required for ordinary sequential editing.

A related enforcement defect was also corrected: the Codex adapter now inspects
patch text in `tool_input.command`, `.patch`, and `.input`, with focused coverage
for all three forms. This closes a wrong-root guard gap; it does not repair the
host patch executor.

### Accepted residuals

- Built-in `apply_patch` may still stall at the host level and remains outside
  repository control.
- Escalation remains per-operation and is not a standing permission.
- A fresh task without inherited incident context may need one observed stall
  before its circuit opens.

### Validation observed

- Two focused hook-wiring tests passed.
- The Codex adapter self-test passed.
- `git diff --check` passed for the bounded repair files.

### Non-claims

- Not proof of the product-side root cause.
- Not a host-level patch-tool repair.
- Not authority to weaken protected-action or worktree guards.

```yaml
direction_change_propagation:
  doctrine_changed: >
    A confirmed sandboxed tool stall now opens the tool-and-permission-route
    circuit for the whole task/thread, including interruptions and automatic
    continuations, instead of resetting at each turn.
  trigger: workflow_authority
  related_triggers: [lifecycle_boundary]
  controlling_sources_updated:
    - AGENTS.md
  downstream_surfaces_checked:
    - CLAUDE.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/hooks/README.md
    - docs/workflows/efficiency/tool_calling_efficiency_improvement_sequence_2026_07_15_v0.md
  intentionally_not_updated:
    - {path: CLAUDE.md, reason: "It imports AGENTS.md and must not duplicate the circuit rule."}
    - {path: .agents/workflow-overlay/decision-routing.md, reason: "Receiver and writable-root routing are unchanged; the circuit remains owned by AGENTS.md Operating Economy."}
    - {path: .agents/workflow-overlay/validation-gates.md, reason: "Validation and review gates are unchanged."}
    - {path: docs/workflows/efficiency/tool_calling_efficiency_improvement_sequence_2026_07_15_v0.md, reason: "It is a dated evaluation record; rewriting history would obscure the newly observed incident."}
  stale_language_search: >
    rg -n -i "rest of the turn|stop the edit route for the turn|open (a |the )?circuit|sandboxed_tool_stall|atomic_exact_edit"
    AGENTS.md CLAUDE.md .agents/workflow-overlay .agents/hooks/README.md
    docs/workflows/efficiency docs/workflows/technical_difficulties_log_v0.md
  stale_language_search_result: >
    Executed after the correction. No live instruction retained a turn-scoped
    circuit. Remaining atomic-helper hits describe the compatible fallback or
    the dated efficiency record.
  non_claims: [not validation, not readiness, not a host-level tool repair]
```

### Delegated-review addendum — circuit-state continuity (2026-07-16)

A commissioned cross-vendor delegated review confirmed one containment gap:
the inheritance rule still depended on current context reporting the stall, but
no rule required an open circuit's `sandboxed_tool_stall` record to travel in a
precompact or handoff packet. Whenever such a packet is used, a receiving lane
could therefore silently reopen a route already observed to be stalled.
`AGENTS.md` now requires the record in either packet type.

Additional accepted residuals from that review:

- Automatic compaction that drops the stall record can silently close the
  circuit; the bounded cost is one re-observed stall before it reopens.
- The adapter inspects the three known Codex payload fields (`command`, `patch`,
  `input`); an unrecognized or non-string payload shape is skipped rather than
  denied, so a future host payload-schema change would reopen the inspection gap
  until observed and patched.

```yaml
direction_change_propagation:
  doctrine_changed: >
    An open sandboxed-tool-stall circuit is now named lane state: precompact
    and handoff packets must carry the `sandboxed_tool_stall` record so a
    receiving lane inherits the open circuit.
  trigger: workflow_authority
  related_triggers: [lifecycle_boundary]
  controlling_sources_updated:
    - AGENTS.md
  downstream_surfaces_checked:
    - CLAUDE.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - docs/workflows/technical_difficulties_log_v0.md
  intentionally_not_updated:
    - {path: CLAUDE.md, reason: "It imports AGENTS.md and must not duplicate the circuit rule."}
    - {path: .agents/workflow-overlay/source-of-truth.md, reason: "Checkpoint packet mechanics remain compatible; circuit state stays owned by AGENTS.md."}
    - {path: .agents/workflow-overlay/source-loading.md, reason: "Packet routing is unchanged; the packet-content obligation belongs with the circuit rule."}
  stale_language_search: >
    rg -n -i "precompact|handoff packet|sandboxed_tool_stall"
    AGENTS.md CLAUDE.md .agents/workflow-overlay docs/workflows/technical_difficulties_log_v0.md
  stale_language_search_result: >
    Executed 2026-07-16 after home replay. Hits were the live AGENTS.md circuit
    rule, this incident record, and compatible packet-mechanics references; no
    live instruction said a packet continuation resets or discards an open circuit.
  non_claims: [not validation, not readiness, not a host-level tool repair]
```
