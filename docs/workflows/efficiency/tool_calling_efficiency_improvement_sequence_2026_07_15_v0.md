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

Current state: **fix 1 passed; fix 2 is next**. The baseline record is pending on
PR #951 at commit `28168fdfc9d39fbdcf57f64b9c2d56b7aa26aceb`; this
ledger does not imply that PR is merged.

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

## Non-claims

- Not proof of root cause in the external Codex sandbox or process launcher.
- Not approval to normalize elevated shell execution.
- Not repair of the ordinary patch primitive.
- Not evidence that operation counts from different transcript accounting
  schemes are perfectly interchangeable.
- Not completion of fixes 2–5 or the after-five evaluation.
