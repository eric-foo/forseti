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

## TD-2026-07-15-001 — Cold scratch lanes hang on default shell and patch routes

- **Observed:** 2026-07-15, Asia/Singapore.
- **Affected lanes:** three isolated cold-agent runs of
  `docs/workflows/efficiency/tool_calling_dogfood_case_v0.md`.
- **State at recording:** open; repeatable mitigation observed, root cause and
  durable owner unresolved.
- **User-visible symptom:** all three runs made no filesystem change for several
  minutes until operator interruption; completed routes used 20–23 logical
  rounds versus the case's roughly five-round reference.

### Verified evidence

| Run | Default shell hung | `apply_patch` hung | Logical rounds / invocations | Final integrity |
| --- | --- | --- | ---: | --- |
| 1 | yes | yes | 23 / 41 | correct three-file patch; unrelated state preserved |
| 2 | yes | yes | 22 / 35 | correct three-file patch; unrelated state preserved |
| 3 | yes | yes | 20 / 31 | correct three-file patch; unrelated state preserved |

Trivial and task-specific default shell calls hung against the assigned
`C:\tmp` snapshots. Bounded elevated shell calls completed. The nested patch
helper also hung in every run; elevated launcher or executable attempts failed
with access denial, and all three runs ultimately used `git apply`. Fresh
operator verification confirmed the final diffs, tests, and untracked-note hash.

### Diagnosis

The failure is repeatable across three context-free agents and occurs before
task-specific reasoning can explain the delay. The effective default shell and
patch routes did not match the intended writable-scratch posture. Evidence does
not yet isolate whether the fault belongs to sandbox mediation, process startup,
the shell host, or patch-helper execution.

A secondary agent-efficiency gap compounded the platform failure: runs polled or
varied a hanging route multiple times and each first Git-patch fallback failed
atomically. Ledger review found only two to four otherwise batchable rounds per
run, so read batching was not the dominant cost.

### Corrective ownership and mitigation

- **Observed bounded mitigation:** after one bounded hang, stop the unchanged
  route; a per-operation elevated shell call restored reads and tests. When the
  patch helper remained unavailable, a checked, atomic `git apply` fallback
  completed the edit.
- **Durable owner:** unresolved external tool/harness substrate; no Forseti
  runtime or repository code owner is established by this evidence.
- **Replay source:**
  `docs/workflows/efficiency/tool_calling_dogfood_run_2026_07_15_v0.md` records
  the fixture baseline, three-run results, and rerun trigger.
- **Upgrade trigger:** rerun the unchanged three-trial case after the default
  shell or edit route changes. Do not change the case and the tool path in the
  same comparison.

### Accepted residuals

- Elevation adds approval latency and is not normalized as the default route.
- Hand-authored Git patches are an error-prone fallback; atomic check/failure
  preserved the trees in these runs but does not make the route preferred.
- Root cause remains unknown; this entry records recurrence and impact, not a
  platform fix.

### Non-claims

- Not a Forseti product, capture, data, or runtime defect.
- Not proof that every `C:\tmp` operation or every agent will reproduce the
  failure.
- Not proof that the agents themselves caused the shared initial stalls.
- Not validation or readiness of the external tool substrate.
