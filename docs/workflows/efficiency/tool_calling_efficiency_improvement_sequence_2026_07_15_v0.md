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

Current state: **fix 1 passed; fix 2 is implemented but blocked by the fresh
managed-task project-hook adoption gate**. The baseline record is pending on
PR #951 at commit `28168fdfc9d39fbdcf57f64b9c2d56b7aa26aceb`; this
ledger does not imply that PR is merged.

Fix 2 candidate state and its pending trusted-hook gate are recorded below.

Artifact merge readiness is separate from operational Fix 2 readiness. The
fail-closed detector and receiver-routing contract in PR #963 may land after its
updated branch diff passes validation and the required independent manual
review. The live `FORSETI_CODEX_HOOK_ADOPTION=NOT_INTERCEPTED` result shows that
the detector identifies the unresolved desktop product condition; it is not an
adoption pass. Landing the detector does not pass Fix 2 or release the three-
cold-agent trial or Fix 3. Those gates remain closed until a fresh managed
receiver returns `FORSETI_CODEX_HOOK_ADOPTION=ADOPTED` and completes the bound
protected checks.

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

### Managed-worktree receiver hardening — live adoption blocked

This lane started in Codex's managed worktree
`C:\Users\vmon7\Desktop\projects\forseti-worktrees\c575\orca` with both
`HEAD` and `origin/main` freshly observed at
`55af05592c19523f1f2f494e88119f9a744cbc79`, then created branch
`codex/tool-efficiency-hook-adoption-canary`. The workspace file portion of the
lane-start write/index probe ran normally. Git index mutation required the
harness's per-operation approval because the registered worktree index is
stored under the parent clone's `.git/worktrees` metadata; the stage, unstage,
probe removal, and clean-status read then passed. No shell command used
elevation, fallback, or a command-level workdir override.

Smallest-complete decision and implementation:

- no persisted hook-adoption state, registry, lifecycle utility, wrapper, or
  synthetic trust entry was added; the live probe result itself is the state;
- the exact top-level command
  `python .codex/hooks/forseti_guard_codex_adapter.py --live-adoption-probe`
  is denied by an adopted live hook with
  `FORSETI_CODEX_HOOK_ADOPTION=ADOPTED`, while direct execution exits `3` with
  `FORSETI_CODEX_HOOK_ADOPTION=NOT_INTERCEPTED`;
- fresh-launcher or live protected-gate commissions route to a newly created,
  correctly rooted Codex managed task; a local/base-rooted task plus
  command-level workdir override is explicitly invalid; and
- clean revision policy is explicit: `exact` requires exact `HEAD`, while
  `ancestor` requires the named prerequisite commit to be an ancestor of the
  current clean `HEAD` and is valid only for a commission that permits an
  advancing lane. Existing exact gates remain exact.

Focused evidence observed before the live task gate:

- adapter smoke/selftest completed in 9.2 seconds with `SELFTEST OK` and
  `CODEX ADAPTER SELFTEST OK`, including synthetic adopted denial and direct
  not-intercepted fallback;
- the two focused pytest assertions for hook wiring, live-probe fallback, route
  markers, command shape, workdir rejection, and revision semantics passed,
  then the full `test_ci_hook_wiring.py` file passed all 13 tests;
- the shared protected-action guard selftest passed all 59 command cases and
  three publication-probe cases;
- the complete local CI hook-gate mirror passed 22/22 gates, and changed-file
  DCP receipt hygiene plus review-routing checks passed; and
- `git diff --check` passed after the focused edits.

The exact top-level probe was then run once in the already-running authoring
task and executed directly with
`FORSETI_CODEX_HOOK_ADOPTION=NOT_INTERCEPTED`. This is a failed adoption result,
not evidence against the adapter: the task predates the changed project-hook
lifecycle. It does not satisfy or replace the required newly started task gate.

Exactly one newly started Codex-managed task then ran the decision-bearing live
gate from the committed candidate:

- task `019f6602-0f31-7a73-94a4-95f482c56488` was rooted at
  `C:\Users\vmon7\Desktop\projects\forseti-worktrees\2183\orca`, detached at
  exact `HEAD` `5eb3e3caf10d179bc23bbffb7a666fc016b201e6`, with a clean
  worktree;
- the lane-start probe created, staged, unstaged, and removed
  `.forseti_lane_probe`, then re-observed clean status;
- the ordinary benign shell returned exit 0 with
  `FORSETI_BENIGN_SHELL_OK` in 1.9 seconds (outer tool cell 2.1 seconds), with no
  elevation or fallback;
- the exact unwrapped top-level live probe executed and returned the shell-tool
  exit 1 with exactly `FORSETI_CODEX_HOOK_ADOPTION=NOT_INTERCEPTED`;
- Codex surfaced no normal hook-review, trust, adoption, or reload UI action;
- no command-level workdir override, `git -C`, trust-metadata edit, source edit,
  or second managed-task receiver was used; and
- the adapter/shared-guard selftests and protected `git clean -n` dry-run were
  not attempted because the mandatory adoption stop fired first.

Decision: **Fix 2 remains blocked at the upstream Codex product boundary.** The
Forseti canary correctly distinguished an unloaded live hook from adoption, but
Forseti cannot make a managed/existing-worktree task trust or load the tracked
project hook and the managed desktop task exposed no user action that could
complete that state.

Current-product follow-up narrowed that boundary without passing the gate:

- the installed CLI identifies itself as `codex-cli 0.128.0`;
- the current official Codex manual says project-local hooks load only when the
  project `.codex` layer is trusted, and new or changed non-managed command
  hooks are skipped until the exact current hook definition is reviewed and
  trusted;
- the documented manual review mechanism is `/hooks` in the Codex CLI, while
  the manual desktop commands and settings surfaces expose no equivalent hook
  review command or setting;
- the fresh managed desktop task above exposed no review, trust, adoption, or
  reload action and returned `FORSETI_CODEX_HOOK_ADOPTION=NOT_INTERCEPTED`;
- a filtered local configuration read observed the base project path
  `C:\Users\vmon7\Desktop\projects\orca` as trusted but observed no
  managed-worktree-specific project trust entry; no trust metadata was edited
  or dumped; and
- the installed package is binary-only, so it provided no stronger local
  implementation source for the desktop-versus-CLI behavior.

The next admissible experiment is therefore an owner-reviewed, supported CLI
`/hooks` trust action launched in the exact managed worktree and reviewing the
exact current hook definition. That action is manual, not automatic, and this
documented path does not yet satisfy Fix 2. Do not start the three-cold-agent
dogfood or Fix 3; after that supported review succeeds, rerun this same live
gate without editing trust metadata.

### Managed-receiver commission confirmation turn

A later implementation-authorized commission exposed a separate receiver-
routing waste: after planning and scoping, its route/status output labeled the
current turn `read_only_scoping_only`. When the current Codex task then proved
invalid as a repo-changing receiver, the commission had not itself explicitly
requested task creation, so the agent correctly could not use Codex's
user-request-only task-creation tool and asked the owner for a second-turn
confirmation phrase.

Decision: implementation authorization survives planning and scoping unless the
owner or an accepted handoff explicitly removes it. A durable implementation
commission selecting a not-yet-verified Codex managed receiver now carries one
commission-local request to create exactly one fresh managed-worktree task at
the bound revision, submit the frozen commission as its initial prompt, and
dispatch it immediately when the current task fails receiver preflight. This is
not standing permission: read-only, scoping-only, and review-only commissions
must not carry the block, a missing block remains `receiver_to_bind`, and a
failed created receiver does not authorize a second task. The contract edit
itself used the already-rooted branch/task and created no receiver.

The commission contract then received one faithful live dogfood:

- source task `019f6652-5909-7e83-9854-ab3b89f38b94` was intentionally rooted
  at the local/base project and received a visible commission-local request to
  create exactly one managed-worktree receiver immediately if it was not the
  valid receiver;
- the source task ran no shell or Git preflight, requested no additional owner
  confirmation, and created exactly one receiver through queue id
  `client-new-thread:20b16545-a6d9-48fe-806a-535e02ea2f49`;
- that queue materialized receiver task
  `019f6653-2794-7f00-9691-576e75dd08e0` at
  `C:/Users/vmon7/Desktop/projects/forseti-worktrees/cdf2/orca`;
- the receiver freshly observed a clean detached `HEAD` exactly at
  `6f4bd992a0777086acf7a8b5b0f8f42e8ec5dace`;
- it created transient probe
  `.codex_receiver_write_probe_019f6653_2794_7f00_9691_576e75dd08e0.tmp`,
  freshly observed that file in the receiver root, removed it, and freshly
  observed it absent;
- final status was clean with no tracked changes; Git emitted only a user-level
  ignore-file permission warning and made no worktree change; and
- owner turn requested: no; receivers created: exactly one.

An earlier attempt in task `019f664e-63e6-7752-8cf7-e14979732a26` is excluded
from this result because its dogfood prompt incorrectly added a source-task Git
preflight before creation. That was a test-harness overconstraint, not behavior
required by the committed contract.

Result: **PASS for the receiver-creation confirmation-turn fix.** The original
implementation commission supplied the explicit user request Codex requires,
the invalid source task dispatched the one bound receiver without a second
owner turn, and the receiver proved exact identity, cleanliness, and write
capability. This narrow pass does not establish project-hook adoption, pass Fix
2, authorize another receiver, or release the three-cold-agent/Fix 3 gates.

## Non-claims

- Not proof of root cause in the external Codex sandbox or process launcher.
- Not approval to normalize elevated shell execution.
- Not repair of the ordinary patch primitive.
- Not evidence that operation counts from different transcript accounting
  schemes are perfectly interchangeable.
- Not completion of fixes 2–5 or the after-five evaluation.
