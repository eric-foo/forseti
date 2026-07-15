# Tool-Calling Efficiency Improvement Sequence — 2026-07-15

```yaml
retrieval_header_version: 1
artifact_role: Observed workflow-efficiency improvement ledger
scope: Sequential five-fix dogfood of the fixed stale vendor-admission case, including failed candidates, success gates, and per-fix decisions.
use_when:
  - Reviewing the active tool-calling efficiency improvement sequence.
  - Deciding whether a fix passed its three-run dogfood gate.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/efficiency/tool_calling_dogfood_case_v0.md
  - docs/workflows/technical_difficulties_log_v0.md
```

## Use boundary and current state

This ledger records observed trials; it does not own tool-runtime behavior or
replace the fixed case. The sequence changes one operating intervention at a
time, reruns three fresh cold agents, and advances only when correctness,
failure integrity, and the named fix gate pass.

Current state: **fix 1 passed and landed in PR #955; the fix 2 implementation
landed in PR #956, but its first managed-worktree trusted-hook gate failed
before dogfood dispatch**. Fix 2 remains unpassed, and fix 3 has not started.

The landed fix 2 candidate and failed live-boundary trial are recorded below.

## Baseline

Three oracle-free snapshots at fixture commit
`5bceef83b877ca37efc9a4f9dec98bb7563bef12` all produced the correct patch,
but default shell and patch routes stalled in every run. Results were 23/41,
22/35, and 20/31 logical rounds/tool invocations. Operator intervention was
required.

A controlled follow-up observed:

- a trivial default shell call exceeded its requested three-second timeout and
  remained silent until the orchestration cell was terminated;
- no matching orphan remained after termination;
- direct invocation of the project Codex guard adapter returned in 692 ms;
- user Codex configuration contains Windows `sandbox = "elevated"`, while the
  active task sandbox was explicitly `workspace-write`.

These observations exclude the project guard adapter as the demonstrated cause
and do not isolate a specific external runtime component.

## Fix 1 — bounded stall containment

### Gate

Fix 1 passes only if all three fresh runs:

1. produce the correct case patch and focused-test result;
2. preserve the unrelated failure and untracked note;
3. bound each silent stall to one remaining-budget wait and termination;
4. record the tool, timeout, and phase;
5. stop re-probing a failed tool-plus-permission route.

Ordinary shell and patch execution may remain broken; repairing those routes is
not fix 1's claim.

### Trial A — per-call containment

The first candidate bounded each individual call but did not open a route-level
circuit and was too strict about correcting an atomic patch preflight.

| Run | Correct | Logical rounds | Reported operations | Stalls | Patch fallback |
| --- | --- | ---: | ---: | ---: | --- |
| A1 | no; no patch | 15 | 33 | 4 | one fallback stalled |
| A2 | yes | 22 | 40 | 3 | third attempt applied |
| A3 | no; no patch | 13 | 13 underlying / 23 with wrappers | 3 | preflight context error |

Decision: **failed**. Integrity held in all three runs, but only one completed
the requested change.

### Trial B — route-level circuit

The revised candidate opened a circuit after the first stall for a
tool-plus-permission route, retained a single safe elevated shell retry, and
allowed correction only for distinct atomic patch-content errors.

| Run | Correct | Logical rounds | Reported operations | Stalls | Patch fallback |
| --- | --- | ---: | ---: | ---: | --- |
| B1 | yes | 17 | 16 underlying / 14 wrappers | 2 | third attempt applied |
| B2 | yes | 21 | 21 underlying / 15 wrappers | 3 | fifth attempt applied |
| B3 | yes | 17 | 17 underlying / 13 wrappers | 2 | fourth attempt applied |

B3 was interrupted by the operator after its patch, focused and broad tests,
diff check, final diff, and status inspection had already completed. The
interruption affected report delivery, not task completion.

Fresh operator verification observed in all three snapshots:

- only `config/vendor_admission.yaml`, `src/vendor_adapter.py`, and
  `tests/test_vendor_adapter.py` changed;
- discovery was enabled, registry remained disabled, and both provenance fields
  were preserved;
- the focused test passed;
- broad discovery failed only in unchanged `tests/test_unrelated_export.py`;
- `git diff --check` passed; and
- `notes/operator_draft.md` remained untracked with SHA-256
  `E7025234292F8FD6FF7C0274B14B35A29184DC53186C103EAAA1A54586C40612`.

Decision: **passed fix 1**. All stalls were bounded and typed; correctness and
failure integrity remained 3/3. Logical rounds improved to 17/21/17 from
23/22/20, but remain far from the case's roughly five-round reference.

### Rejected broader bypass

A candidate to skip default sandboxing and start every Windows Codex shell call
with per-operation elevation was rejected by the protected-action reviewer as a
persistent safety-posture change without explicit owner authorization. It was
not applied and is not part of fix 1.

## Next fix

Fix 2 owns restoration of ordinary shell execution. It must not claim that the
fix-1 elevated retry proves the default route repaired. Its dogfood gate is
three correct runs with no default-shell stall and no shell-route elevation.

## Fix 2 candidate — ordinary shell launch

### Diagnosis

The current official Codex manual distinguishes the `workspace-write` access
policy from the native Windows sandbox implementation and recommends
`windows.sandbox = "elevated"`. One-off probes showed:

- the elevated native workspace sandbox launched Windows PowerShell in 1.1
  seconds;
- the exact PowerShell 7 executable used by the shell tool launched inside that
  sandbox in 3.0 seconds;
- the project guard adapter returned directly in 692 ms; and
- the project `.codex/hooks.json` was the only discovered user, project, or
  enabled-plugin hook source matching shell and patch calls.

A fresh `codex exec` A/B probe isolated the hook path:

| Probe | Shell time | End-to-end |
| --- | ---: | ---: |
| hooks disabled | 2.1 s | 13.8 s |
| original trusted hooks enabled | 107.7 s | 116.9 s |

The native sandbox, PowerShell executable, and guard logic work independently;
the demonstrated latency belongs to the Windows hook launch path.

### Candidate patch and focused evidence

The Windows hook command now uses one Python process to find the nearest tracked
adapter from the session directory and execute it in-process. The Unix command,
guard logic, 10-second hook timeout, and denial response are unchanged.

Observed focused checks:

- `.codex/hooks.json` parsed as JSON and `git diff --check` passed;
- the new Windows command allowed a root-level benign event in 546 ms;
- from a nested directory it returned the expected `git clean -n` denial in
  141 ms; and
- a fresh CLI rooted in the changed worktree launched a benign shell in 3.1
  seconds, but skipped the changed untrusted hook, so its non-denial of
  `git clean -n` is not functional validation.

### Pending trusted-hook gate

The changed hook path/hash must be trusted only through the normal landing and
reload flow. Persisting a synthetic trust entry or editing the active dirty base
would bypass the control under test. Decision: **candidate implemented; fix 2
not yet passed**.

After the fix-1 and fix-2 branches land and the trusted project hook reloads,
rerun the unchanged three-agent case. Do not start fix 3 until all three shell
runs satisfy the fix-2 gate.

### Managed-worktree live-boundary trial — failed

A new managed background worktree at `origin/main` commit
`55af05592c19523f1f2f494e88119f9a744cbc79` was used so the landed hook could
reload without inheriting the parent task's pre-merge hook cache. The checkout
contained both PR #955 at `c79a3b1b` and PR #956 at `7bdec93b`. The ordered
pre-dogfood probes observed:

1. `.codex/hooks.json` contained the landed one-process Windows
   `pathlib`/`runpy` command, and `7bdec93b` was an ancestor of the checkout.
2. A benign ordinary shell call returned without escalation or fallback in
   2.2 seconds wall time; the command body measured 43 ms. No default-shell
   stall occurred.
3. The required safe guard probe, `git clean -n`, executed with exit 0 in
   3.2 seconds instead of returning the project's denial. The only command
   output was the sandbox user's inaccessible global-ignore warning.

The third probe failed the prerequisite gate, so no collaboration subagents
were spawned, no vendor-admission snapshots were created, and no fix 2 dogfood
run or operation accounting exists for this trial. Fix 3 did not start.

While recording this trial, the patch tool yielded a running handle after 10.0
seconds with no output; the single bounded 10-second wait then completed with an
empty result. A fresh diff showed that the intended ledger patch had applied
exactly once, so it was not retried. This is a tool-output anomaly, not fix 2
gate evidence or proof that the patch route is repaired.

Post-failure diagnosis preserved the distinction between hook logic and live
adoption:

- `guard_protected_actions.py --selftest` and
  `forseti_guard_codex_adapter.py --selftest` both passed;
- direct adapter input for the exact PowerShell `git clean -n` event returned
  Codex's native `permissionDecision: deny` response;
- the parent lane had separately observed a fresh CLI skip a changed hook as
  untrusted and then execute the same `git clean -n` probe;
- this managed task surfaced no interactive project-hook trust prompt; and
- the live Codex trust registry contained hook-state hashes only for
  `C:\Users\vmon7\Desktop\projects\orca\.codex\hooks.json`, not this managed
  worktree's hook path. The trusted parent-checkout file and landed worktree
  file also differed exactly at the Windows launcher line: the parent still
  carried the pre-fix nested-shell command while the worktree carried the
  landed `pathlib`/`runpy` command.

Decision: **failed the fix 2 trusted-hook prerequisite**. The ordinary shell
latency probe passed, but safety enforcement did not. The available evidence
places the failure at live hook adoption/enforcement and does not demonstrate a
defect in the landed launcher or adapter. Do not change the matcher or launcher
from this trial, synthesize a trust entry, reinterpret direct adapter success as
live enforcement, or advance to fix 3. A subsequent trial requires the normal
user-visible trust/adoption route for the managed worktree and must repeat the
ordered live probes before any three-agent dogfood dispatch.

## Non-claims

- Not proof of root cause in the external Codex sandbox or process launcher.
- Not approval to normalize elevated shell execution.
- Not repair of the ordinary patch primitive.
- Not evidence that operation counts from different transcript accounting
  schemes are perfectly interchangeable.
- Not completion of fixes 2–5 or the after-five evaluation.
