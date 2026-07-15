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

Current state: **fixes 1, 2, 4, and 5 passed; fix 3 is product-blocked**. Fix 2
passed after the owner enabled the already-trusted project hook through the
supported CLI `/hooks` screen, a fresh session returned the adopted denial, and
three cold runs passed the unchanged case without an ordinary-shell stall or
shell-route elevation. The baseline record is pending on PR #951 at commit
`28168fdfc9d39fbdcf57f64b9c2d56b7aa26aceb`; this ledger does not imply that PR
is merged.

Fix 2's earlier blocked state and final supported enablement are recorded below.

Artifact merge readiness was separate from operational Fix 2 readiness. The
fail-closed detector and receiver-routing contract in PR #963 may land after its
updated branch diff passes validation and the required independent manual
review. The live `FORSETI_CODEX_HOOK_ADOPTION=NOT_INTERCEPTED` result shows that
the detector identified the then-unresolved desktop product condition; it was
not an adoption pass. The later fresh-session adopted denial and cold trials
closed Fix 2 without changing detector, matcher, trust metadata, or protected-
action semantics.

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

### Supported enablement, fresh adoption, and final Fix 2 dogfood

A fresh read-only hook listing against Codex CLI 0.144.4 isolated the adoption
failure more precisely than the earlier trust-only diagnosis:

- the project `PreToolUse` definition was already `trusted` at current hash
  `sha256:ddca246538f9075cbea674c7585bc527b1088caa8aa60e495f08b8acaaf66c0c`;
- its persisted state was explicitly `enabled: false`, while both project
  `PostToolUse` handlers were trusted and enabled;
- the managed worktree correctly resolved the trusted base-project source at
  `C:\Users\vmon7\Desktop\projects\orca\.codex\hooks.json`; and
- no hook definition, matcher, guard behavior, or trust metadata needed a
  repository change.

The owner opened the CLI in the exact managed worktree, selected `PreToolUse`
in `/hooks`, and changed the single trusted handler from `[ ]` to `[x]`. A fresh
listing then observed the same hash with `trusted` and `enabled: true`. The
already-running desktop task still returned
`FORSETI_CODEX_HOOK_ADOPTION=NOT_INTERCEPTED`, proving that enablement does not
retroactively reload an existing task. One fresh Codex CLI 0.144.4 session,
rooted at this worktree with no command-level workdir override, then ran the
exact canary once and was denied before execution with
`FORSETI_CODEX_HOOK_ADOPTION=ADOPTED`.

Three new isolated snapshots were then created at fixture commit
`5bceef83b877ca37efc9a4f9dec98bb7563bef12`. Before dispatch, each had focused
exit 0, broad exit 1 only from the fixed unrelated failure, and untracked note
SHA-256 `E7025234292F8FD6FF7C0274B14B35A29184DC53186C103EAAA1A54586C40612`.
The three agents received only the unchanged sealed courier.

| Run | Correctness | Tool-call sequence | Retries / fallback / elevation | Observable wall time | Success signal |
| --- | --- | --- | --- | ---: | --- |
| 1 | Correct three-file patch | 3 read/intake commands; 1 edit; focused test; broad test; 2 closeout commands | none / none / none | 74.4 s | **PASS** — ordinary shell completed every command without a stall; focused passed; only the unchanged unrelated broad failure remained |
| 2 | Correct three-file patch | 3 read/intake commands; 1 edit; focused test; broad test; 1 closeout command | none / none / none | 55.8 s | **PASS** — ordinary shell completed every command without a stall; focused passed; only the unchanged unrelated broad failure remained |
| 3 | Correct three-file patch | 3 read/intake commands; 1 edit; focused test; broad test; 1 closeout command | none / none / none | 66.2 s | **PASS** — ordinary shell completed every command without a stall; focused passed; only the unchanged unrelated broad failure remained |

Fresh operator verification observed in all three snapshots:

- exactly `config/vendor_admission.yaml`, `src/vendor_adapter.py`, and
  `tests/test_vendor_adapter.py` changed;
- discovery was enabled, registry remained disabled, and both provenance fields
  were preserved and asserted;
- focused exit was 0, broad exit was 1 only from unchanged
  `tests/test_unrelated_export.py`, and `git diff --check` exited 0; and
- `notes/operator_draft.md` remained untracked at the exact baseline hash.

Decision: **PASS Fix 2 at 3/3.** The smallest complete operational fix was the
owner's supported enable action for the already-trusted handler plus a fresh
session reload. The repository's Windows hook-launch optimization then met its
original gate: three correct runs, no ordinary-shell stall, no shell-route
elevation, no retry, and preserved failure integrity. This result does not
repair or claim the native patch primitive owned by Fix 3.

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

## Definition gate for fixes 3-5

These definitions use PR #951 only as observed evidence. They do not treat its
unmerged files or conclusions as Forseti authority. Fix 2 remains independently
blocked on Codex CLI 0.144.4 and is neither repaired nor counted as passed here.

### Fix 3 — native patch-primitive restoration

- **Observed failure or gain:** the native patch primitive failed on the first
  route in all three baseline trials; the current managed receiver can invoke
  the primitive, but that different task state does not repair or invalidate
  the repeated cold-snapshot failure.
- **Ownership:** Codex-owned. Forseti can contain a stalled route and prescribe
  a fallback, but it does not own native tool launch, sandbox mediation, or the
  patch primitive executable.
- **Smallest complete intervention:** no repository change. A complete fix must
  restore one bounded native patch call in the unchanged cold case without
  elevation, launcher probing, or a repository fallback.
- **Exact success signal:** exactly three fresh cold runs each complete their
  first native patch call without silence, timeout, elevation, or fallback and
  retain the case's correctness and failure-integrity invariants.
- **Correctness and failure integrity:** the three-file oracle patch, focused
  pass, unchanged unrelated failure, and byte-identical untracked note remain
  mandatory; a fallback success cannot be relabeled as native-route success.
- **Dogfood scenario:** the unchanged vendor-admission case, three oracle-free
  snapshots, with the ordinary native patch route attempted once after the edit
  is bound.
- **Semantics:** `PASS` requires 3/3 exact success signals; `FAILED` means a
  claimed Codex repair was exercised and any run missed the signal;
  `PRODUCT_BLOCKED` means no Forseti-owned implementation can restore the
  primitive; `NOT_RUN` means no eligible implementation was available to test.
- **Independence:** Fix 3 does not depend on Fix 2's shell-hook adoption. Fix 4
  begins only after this product boundary is recorded because fallback quality
  is useful precisely when the native route remains unavailable.

Decision: **PRODUCT_BLOCKED**. No repository implementation or cold trial is
attempted for Fix 3; doing so would test containment or fallback behavior, not
the defined native-route repair.

### Fix 4 — first fallback patch reliability

- **Observed failure or gain:** after the native edit route failed, the first
  Git-patch fallback was malformed or context-mismatched in 3/3 baseline runs;
  atomic failure preserved integrity but added serial recovery rounds.
- **Ownership:** mixed. Git and shell execution are external, while Forseti owns
  the operating discipline used to construct and preflight its fallback.
- **Smallest complete intervention:** provide one repository-owned exact-text
  replacement helper and route the existing post-stall fallback to it. The
  caller supplies repeated file/old-text/new-text triples from freshly read
  targets; the helper preflights the whole change before writing and rejects
  ambiguous, stale, escaping, mixed-newline, or no-op input.
- **Exact success signal:** in exactly three fresh cold runs forced past the
  native route, the first fallback patch preflight and apply both succeed, with
  zero fallback reconstruction/retry rounds, while all case correctness and
  failure-integrity invariants hold.
- **Correctness and failure integrity:** preflight must be atomic; failed
  preflight changes no tracked or untracked bytes; final scope, focused and
  unrelated test outcomes, diff check, and note hash must remain visible.
- **Dogfood scenario:** the unchanged vendor-admission case with the native edit
  route declared unavailable after one bounded attempt, so each cold agent must
  discover and use the repository-instructed checked fallback.
- **Semantics:** `PASS` requires 3/3 exact success signals; `FAILED` means any
  attempted run reconstructs/retries the fallback, applies an incorrect patch,
  or loses failure integrity; `PRODUCT_BLOCKED` requires observed inability of
  the tool bridge to execute the prescribed Git preflight/apply route;
  `NOT_RUN` means Fix 3 was neither passed nor explicitly product-blocked, or
  the frozen snapshots could not be prepared.
- **Independence:** independent of Fix 2 because ordinary shell restoration is
  not credited and a bounded executable shell route is sufficient; independent
  of Fix 5 because trial accounting preserves the existing call pattern except
  for fallback construction.

#### Owner-authorized retry candidate B — deterministic exact-edit helper

Candidate A established that more patch-construction prose is insufficient:
all three first Git-patch preflights failed, including CRLF-sensitive context
failures. Candidate B therefore changes the mechanism rather than the wording.

- **Smallest complete intervention:** add one repository-owned helper that
  accepts a versioned exact-replacement plan in memory, preflights every target
  before any write, preserves each file's existing LF or CRLF convention, and
  atomically replaces only the named files. Route the post-primitive-stall
  fallback to that helper from `AGENTS.md`; do not hand-author a Git patch.
- **Exact success signal:** exactly three fresh cold runs forced past the native
  primitive each succeed on their first helper preflight-and-apply invocation,
  with no plan reconstruction, helper retry, Git-patch fallback, or partial
  write, while the existing correctness and failure-integrity invariants hold.
- **Failure semantics:** any helper rejection, retry, reconstructed plan,
  partial write, wrong patch, or lost unrelated state makes candidate B
  `FAILED`. An inability to execute the repository helper at all is
  `PRODUCT_BLOCKED`. Fix 5 remains `NOT_RUN` unless candidate B passes 3/3.
- **Lock-in boundary:** the helper owns exact byte-safe text replacement only.
  It is not a general patch language, daemon, hook, registry, formatter, or
  substitute for the native patch primitive.

Candidate B decision: **FAILED**. All three first default-shell launches of the
helper stalled without helper output. Runs 1 and 2 then executed the helper
successfully through the single elevated shell retry and produced correct,
failure-integral patches; run 3 obeyed the no-retry rule and made no patch. Two
runs also repaired command-string quoting before launch. The helper's executed
preflight/apply path was 2/2, but the exact end-to-end first-invocation signal
was 0/3. This is not credited as a Fix 4 pass.

#### Owner-authorized retry candidate C — direct JSON on the working route

Candidate C keeps the same helper and edit semantics but removes the observed
plan-construction layer: the helper accepts one single-quoted `--plan-json`
argument directly. The cold scenario starts after both the native-patch and
default-shell circuits are explicitly open and uses the one permitted elevated
shell route for the helper. This isolates fallback edit reliability from Fix
2's independently product-blocked shell launch.

- **Exact success signal:** exactly three fresh cold runs each execute one
  elevated helper `--apply` call with direct JSON; that first call must return
  `PRECHECK=OK` and `APPLY=OK`, with no command reconstruction, plan rebuild,
  helper retry, Git-patch fallback, or partial write. All correctness and
  failure-integrity invariants remain mandatory.
- **Failure semantics:** any pre-launch command correction, helper rejection,
  timeout, retry, incorrect patch, or lost unrelated state is `FAILED`. The
  bounded elevated route is test isolation only and is not a Fix 2 pass or
  permission to normalize elevation for ordinary shell work.

Candidate C decision: **FAILED**. One run passed end to end. One run consumed
its only helper invocation on `--help`; one passed malformed JSON through shell
quoting and the helper rejected it before preflight. No incorrect or partial
write occurred, but exact first-use success was 1/3.

#### Owner-authorized retry candidate D — repeated exact replacements

Candidate D removes serialized plan construction entirely. The same helper
accepts one or more repeated `--replace PATH OLD NEW` triples; `\\n`, `\\t`, and
`\\\\` are decoded by the helper before the unchanged preflight/apply core.
PowerShell callers single-quote each value. Reading source or help is not an
apply attempt; exactly one `--apply` invocation remains the gate.

- **Exact success signal:** exactly three fresh cold runs each complete one
  elevated `--apply` invocation using repeated replacements; the first call
  returns `PRECHECK=OK` and `APPLY=OK`, with no command correction, retry,
  helper rejection, wrong patch, or lost unrelated state.
- **Stop condition:** if candidate D misses any of three signals, remove the
  helper and its workflow-authority/placement routes rather than keep an
  unproven standing tool.

Candidate D decision: **PASS**. All three fresh cold runs completed their only
`--apply` invocation on the first attempt. Each returned `PRECHECK=OK FILES=3`
and `APPLY=OK FILES=3`, produced exactly the expected three-file patch, passed
the focused test and `git diff --check`, preserved the unrelated broad-test
failure, and preserved the untracked note byte-for-byte. Two runs first looked
for an overlay file that was absent from the frozen fixture, and one of those
runs adjusted that read-only lookup. This setup noise was visible but did not
alter, reconstruct, or retry the edit command, so it does not miss the stated
editing signal.

#### Candidate D three-cold-run dogfood

The three disposable repositories were frozen at fixture-local commit
`7d3b7eb530a763bd32b86b9bdf5ee876d8ad8ab7`. The helper and fixture-instruction
hashes were identical before dispatch, and each began with only
`notes/operator_draft.md` untracked at SHA-256
`E7025234292F8FD6FF7C0274B14B35A29184DC53186C103EAAA1A54586C40612`.
The native-patch and default-shell circuits were declared open, isolating the
exact-edit fallback from Fixes 2 and 3. Agents used separate repositories and
had no write access to this lane.

| Run | Correctness | Tool rounds and sequence | Retries / fallback | Observable wall time | Real failures preserved | Success signal |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Exact three-file patch; focused pass; diff check pass | 11: orient -> fixture instructions/status -> source/help -> targets -> one helper apply -> focused/broad tests -> closeout | No edit-command correction or retry; one read-only lookup adjusted after the fixture lacked the overlay path | Not independently instrumented | Broad test failed only in unchanged unrelated export; note hash and untracked state preserved | **PASS** — first and only apply returned both required markers |
| 2 | Exact three-file patch; focused pass; diff check pass | 7: orient/instructions/targets -> one helper apply -> combined verification -> closeout | No edit-command correction, rejection, or retry; an absent-overlay read reported visibly | Not independently instrumented | Same unrelated broad failure and note hash preserved | **PASS** — first and only apply returned both required markers |
| 3 | Exact three-file patch; focused pass; diff check pass | 9: orient/instructions/targets -> source/help -> one helper apply -> focused/broad tests -> closeout | No edit-command correction, rejection, or retry; an absent-overlay read reported visibly | Not independently instrumented | Same unrelated broad failure and note hash preserved | **PASS** — first and only apply returned both required markers |

Fresh operator verification after all agents stopped observed that all three
repositories changed only `config/vendor_admission.yaml`,
`src/vendor_adapter.py`, and `tests/test_vendor_adapter.py`; all passed the
focused test and `git diff --check`; all broad tests failed only at the
unchanged unrelated export assertion; and all note hashes matched the baseline.

#### Candidate D retained implementation and validation

- `.agents/tools/atomic_exact_edit.py`: bounded exact-text replacement helper;
  all-target preflight, path and symlink containment, match-count checks,
  newline preservation, atomic replacement, best-effort rollback, and embedded
  focused self-test.
- `AGENTS.md`: post-patch-stall route to one helper apply, with rejection as a
  visible stop rather than a reconstruction/retry loop.
- `.agents/workflow-overlay/artifact-folders.md` and
  `docs/workflows/forseti_repo_map_v0.md`: authority and routing for the bounded
  `.agents/tools/` home.
- This ledger: candidate definitions, all cold-trial evidence, decision,
  validation, and residual risk.

Observed closeout commands:

| Command | Exit | Actual result |
| --- | --- | --- |
| `python -B .agents/tools/atomic_exact_edit.py --selftest` | 0 | 12 named cases passed; `SELFTEST OK` |
| `git diff --check` | 0 | No whitespace errors; Git emitted only line-ending conversion warnings for four existing text files |
| `python .agents/hooks/check_placement.py --strict` | 0 | 0 violations, 0 freshness findings; 1,251 legacy-tolerated and 109 scratch-excluded files reported |
| `python .agents/hooks/check_dcp_receipt.py --strict` | 0 | 1 real receipt in 1 changed Markdown file was shape-valid |
| `python .agents/hooks/check_map_links.py --strict` | 0 | 0 findings; 36 annotated non-resolving debt entries |
| `python .agents/hooks/check_repo_map_freshness.py --changed` | 0 | No freshness finding emitted |
| `pwsh .github/scripts/run-doc-gates.ps1` | 0 | 22/22 local documentation gates passed |
| `python .agents/hooks/check_dcp_receipt_hygiene.py --changed --strict` | 1 | Existing debt surfaced: the touched `artifact-folders.md` already contains 9 historical inline receipts, above the current limit of 2 |

The receipt-hygiene failure remains visible and was not repaired here: deleting
seven historical receipts is unrelated cleanup, Candidate D added its receipt
to this changed ledger rather than that controlling file, and the owning
diff-scoped receipt-shape gate passes. This is a residual repository-hygiene
risk, not evidence that the exact-edit helper failed.

### Fix 5 — dependency-round consolidation

- **Observed failure or gain:** each baseline ledger contained roughly two to
  four read or verification rounds whose inputs were already independent and
  could have been issued together.
- **Ownership:** Forseti-owned operating discipline; no tool-runtime repair is
  required.
- **Smallest complete intervention:** add one `AGENTS.md` rule to batch
  dependency-independent reads and checks in a single tool round, while keeping
  authority discovery, edit binding, focused validation, and causal closeout in
  their required order.
- **Exact success signal:** exactly three fresh cold runs remain correct and
  failure-integral, contain no identified consolidatable read/verification
  round, and use no more than the case's five latency-bearing dependency rounds;
  underlying call count remains diagnostic rather than a gate.
- **Correctness and failure integrity:** batching must not omit source
  authority, focused validation, unrelated-failure attribution, final diff or
  status, or untracked-note verification; mixed checks must retain individual
  exit/output visibility.
- **Dogfood scenario:** three fresh oracle-free snapshots of the unchanged case
  after Fix 4 passes, with the Fix 5 rule as the only new intervention.
- **Semantics:** `PASS` requires 3/3 exact success signals; `FAILED` means any
  run exceeds five dependency rounds because of an identified consolidatable
  read/check or loses a correctness/integrity invariant; `PRODUCT_BLOCKED`
  requires the tool bridge to prevent independent calls from being issued in
  one round; `NOT_RUN` means Fix 4 has not passed or snapshot/receiver evidence
  is unavailable.
- **Independence:** independent of Fix 2 and native patch restoration; dependent
  on Fix 4 passing only to keep the sequential experiment one-intervention-at-a-
  time and avoid attributing fallback recovery rounds to batching.

## Fix 4 candidate A dogfood — failed instruction-only discipline

The candidate added only the definition-gated fallback-construction sentence to
the fixture's repository instructions. The three oracle-free snapshots were
byte-identical at fixture-local commit
`459845f528081c6485fb8d271d05f596dd22efea`; each began with only
`notes/operator_draft.md` untracked at SHA-256
`E7025234292F8FD6FF7C0274B14B35A29184DC53186C103EAAA1A54586C40612`.
The native patch route was declared unavailable, so the trial measured the
first checked Git fallback only. Agents used separate disposable repositories
and had no write access to this lane.

| Run | Correctness | Reported calls or batches and sequence | Retries / fallback | Observable wall time | Real failures preserved | Success signal |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Correct three-file patch; focused pass | 18: orient -> instructions/status -> authority/targets -> construct -> preflight -> reread/rebuild -> apply -> focused/broad tests -> closeout | Two sandbox-denied patch-file writes; first preflight failed `corrupt patch at ...:50`; one reconstruction then checked/applied | about 25.4 s across reported calls/batches; end-to-end not independently instrumented | Broad test failed only in unchanged unrelated export; note hash and untracked state preserved | **FAIL** — first preflight did not pass; one reconstruction required |
| 2 | No patch; requested behavior absent; focused baseline pass | 13: orient/status -> authority/targets -> construct -> escalated preflight -> reread/rebuild -> EOL diagnosis -> focused/broad tests -> closeout | Initial patch-file write denied; first preflight failed at test line 4; reconstruction failed at line 1; no apply | about 26.3 s across reported calls/batches; end-to-end not independently instrumented | Broad test failed only in unchanged unrelated export; no tracked bytes changed; note preserved | **FAIL** — neither preflight passed; no apply |
| 3 | No patch; requested behavior absent; focused baseline pass | 10: orient/instructions/inventory -> authority/targets -> preflight -> reread/rebuild -> focused/broad tests -> closeout | First preflight failed at test line 4; reconstruction failed at line 4; no apply | about 14.6 s across reported calls/batches; end-to-end not independently instrumented | Broad test failed only in unchanged unrelated export; no tracked bytes changed; note preserved | **FAIL** — neither preflight passed; no apply |

Fresh operator verification after all agents stopped observed:

- run 1 changed only `config/vendor_admission.yaml`,
  `src/vendor_adapter.py`, and `tests/test_vendor_adapter.py`; selected discovery
  only; preserved both provenance fields; passed the focused test and
  `git diff --check`;
- runs 2 and 3 had no tracked diff and therefore did not implement the request;
- all three focused tests passed, all three broad runs failed only in unchanged
  `tests/test_unrelated_export.py`, and all three note hashes remained exactly
  the baseline value above.

Candidate A decision: **FAILED**. Exact first-fallback success was 0/3. The candidate
improved failure discipline but did not make the first fallback reliable; it
was removed from `AGENTS.md` rather than promoted as working workflow authority.
The failures narrow the next design question to deterministic patch-byte
construction across sandboxed Windows paths and CRLF worktrees, but this result
does not authorize a helper, wrapper, or second three-run batch.

## Fix 5 candidate A dogfood — independent-work batching

Candidate A added only the definition-gated independent-work batching rule to
the fixture's repository instructions, on top of the retained Fix 4 exact-edit
fallback. The three oracle-free snapshots were byte-identical at fixture-local
commit `98e9c3d4ea7811c07812982d28effa4ba014febc`; each began with only
`notes/operator_draft.md` untracked at SHA-256
`E7025234292F8FD6FF7C0274B14B35A29184DC53186C103EAAA1A54586C40612`.
The native-patch and ordinary-shell circuits were declared open, so the trials
measured Fix 5 without retesting Fixes 2–4.

| Run | Correctness | Latency-bearing rounds and sequence | Calls / retries | Observable wall time | Real failures preserved | Success signal |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Correct three-file patch; focused pass; diff check pass | 8: instructions+handoff -> authority search -> policy/inventory/status -> target reads/diff/note hash -> one edit -> focused -> broad -> grouped closeout | 8 shell calls plus 1 wait; no edit or command retry; authority search included one visible invalid-path subcheck | Per-round wrapper times about 10.0, 4.7, 3.7, 3.2, 8.4, 3.0, 4.9, and 4.3 s | Broad test failed only in unchanged unrelated export; note hash and untracked state preserved | **FAIL** — exceeded five rounds and kept consolidatable authority/read rounds |
| 2 | Correct three-file patch; focused pass; diff check pass | 7: instructions/inventory/status -> authority discovery -> handoff+policy+targets+helper -> one edit -> focused -> broad -> grouped closeout | 7 shell calls plus 1 wait; no retry | About 34.4 s across reported wrapper rounds | Same unrelated broad failure and note hash preserved | **FAIL** — exceeded five rounds; initial orientation and authority discovery were consolidatable |
| 3 | Correct three-file patch; focused pass; diff check pass | 7: instructions -> handoff/inventory/status -> policy+targets -> one edit -> focused -> broad -> grouped closeout | 16 shell invocations across 7 grouped rounds plus 1 wait; no retry | About 42.0 s across reported wrapper rounds | Same unrelated broad failure and note hash preserved | **FAIL** — exceeded five rounds; instructions and handoff/inventory/status were consolidatable |

Fresh operator verification observed that all three repositories changed only
`config/vendor_admission.yaml`, `src/vendor_adapter.py`, and
`tests/test_vendor_adapter.py`; all passed the focused test and
`git diff --check`; all broad tests failed only at the unchanged unrelated
export assertion; and all note hashes matched the baseline.

Candidate A decision: **FAILED**. Correctness and failure integrity held 3/3,
but exact efficiency success was 0/3 at 8, 7, and 7 rounds. The rule was removed
from `AGENTS.md`. Diagnosis found a mechanism/target mismatch: independent-work
batching reduces parallel width, while the frozen authority, edit, validation,
and closeout chain requires reducing latency-bearing depth to reach five.

### Owner-authorized Fix 5 candidate B — bounded ordered bundles

Candidate B preserves the original five-round signal rather than relaxing it.

- **Smallest complete intervention:** allow one tool call to execute a bounded,
  predeclared sequence of read-only discovery or validation commands in causal
  order. Each step must print a label, preserve its own output and exit code,
  and obey explicit stop/continue semantics. Mutating edits remain isolated in
  their own call; no hidden retry, omitted check, or concurrent write is allowed.
- **Expected five-round shape:** (1) instructions plus bounded authority chain;
  (2) target reads and edit binding; (3) one exact edit; (4) focused test then
  broader test in one ordered validation call; (5) final diff, status, failure
  attribution, and untracked-state verification.
- **Exact success signal:** unchanged from Fix 5: exactly three fresh cold runs
  must be correct and failure-integral, contain no remaining consolidatable
  read/verification round, and use no more than five latency-bearing rounds.
- **Failure integrity:** the ordered validation call must expose separate focused
  and broad exits and output; a focused failure must prevent the broad test but
  still permit non-mutating closeout evidence; the known unrelated broad failure
  must remain visible and attributable.
- **Stop condition:** any run above five rounds, any hidden/merged exit status,
  any skipped required check, or any incorrect/partial patch makes candidate B
  `FAILED`; remove the rule rather than relax the frozen target after observing
  results.
- **Independence:** candidate B changes only Forseti call composition. It does
  not repair or credit the Fix 2 shell route, Fix 3 native patch primitive, or
  Fix 4 exact-edit fallback.

#### Candidate B observed result

The three fresh snapshots were frozen at fixture-local commit
`ef683eb09aef8ab95a4f081194f77527ffe2f276`, with the same helper and untracked
note hashes used by candidate A.

| Run | Correctness | Rounds | Retries / real failures | Observable wall time | Success signal |
| --- | --- | ---: | --- | --- | --- |
| 1 | No patch; validation not run | 5 before stop | No retry; the only permitted elevated shell route stalled silently during the pre-edit helper/target read and was terminated under the circuit rule | About 283.2 s including the stalled handle | **FAIL** — correctness and required checks absent; five rounds were consumed before mutation |
| 2 | Correct three-file patch; focused pass; unrelated broad failure and note preserved | 7 | No retry; one exact-edit apply | About 31.0 s | **FAIL** — exceeded five rounds |
| 3 | Correct three-file patch; focused pass; unrelated broad failure and note preserved | 10 | No retry; one exact-edit apply | About 37.3 s | **FAIL** — exceeded five rounds |

Fresh operator verification observed no tracked diff in run 1, the exact
three-file scope in runs 2 and 3, clean `git diff --check` in all three, and the
baseline untracked-note hash in all three.

Candidate B decision: **FAILED** at 0/3. The abstract ordered-bundle permission
did not create a stable execution shape: agents still separated instructions,
inventory, authority, target, and helper reads, and one run exhausted five
rounds before the edit. The rule was removed rather than credited for the two
correct but over-budget runs.

### Owner-authorized Fix 5 candidate C — explicit five-phase fast path

Candidate C keeps the unchanged five-round signal but replaces abstract
permission with an explicit eligible-case protocol.

- **Eligibility:** named handoff, safely bounded candidate-authority and target
  set, one edit unit, known focused/broad validation, and no concurrent writer.
- **Five phases:** (1) receiver instructions; (2) one bounded read-only intake
  snapshot containing handoff, all candidate authority, status/inventory,
  likely targets, helper usage, and untracked baseline, followed by authority
  resolution and edit binding in reasoning; (3) one isolated exact edit; (4)
  one ordered focused-then-broad validation call with labeled individual exits
  and focused-failure stop semantics; (5) one read-only closeout with diff,
  status, attribution, and untracked verification.
- **Exact success signal:** unchanged: 3/3 correct and failure-integral cold
  runs, no remaining consolidatable round, and no more than five latency-bearing
  rounds each.
- **Failure integrity:** reading likely targets in the intake is harmless and
  does not bind the edit before authority is resolved; mutation stays isolated;
  validation and closeout retain individual outputs and real failures.
- **Stop condition:** if any run exceeds five, skips a phase, hides an exit,
  retries invisibly, or loses correctness/integrity, remove the fast path and
  retain Fix 5 as `FAILED`.
- **Independence:** no Fix 2 shell or Fix 3 patch restoration is credited; the
  retained Fix 4 helper remains the isolated mutation mechanism.

#### Candidate C observed result

The final three fresh snapshots were frozen at fixture-local commit
`29aa44b41235aab39cf04a9dc0456fb190b18cb1`, with identical helper and note
hashes and no concurrent writer.

| Run | Correctness | Rounds | Validation / integrity | Observable wall time | Success signal |
| --- | --- | ---: | --- | --- | --- |
| 1 | Correct three-file patch | 5 | Focused passed; unrelated broad failure and final note hash visible; the cold intake scanner missed the starting hash, while the pre-dispatch fixture record and fresh operator closeout proved the same before/after hash | About 25.0 s | **PASS** — actual correctness and integrity held; the missing cold-agent printout was an observability blemish, not a lost invariant |
| 2 | Correct three-file patch | 5 | Focused passed; unrelated broad failure, separate exits, diff/status, and before/after note hashes visible | About 22.5 s | **PASS** — the instructions round contained partial intake, and the single following intake phase completed the bounded evidence without adding a sixth round |
| 3 | Correct three-file patch | 5 | Focused passed; unrelated broad failure, separate exits, exact diff/status, unchanged-failure hash, and matching note hashes visible | About 21.5 s | **PASS** — all five phases and integrity checks held with no retry |

Fresh operator verification observed the exact three-file scope in all three,
focused exit 0, broad exit 1 only from the unchanged unrelated test,
`git diff --check` exit 0, and the baseline note hash in the frozen template and
every final snapshot. The original success semantics require untracked-note
verification, not that one actor independently print both hashes. The
pre-dispatch baseline plus fresh post-trial read is the experiment's independent
verification and was bound before outcomes were known; crediting it changes no
threshold or invariant.

Candidate C decision: **PASS** at 3/3. Every run completed the correct patch in
five latency-bearing rounds, preserved real failure visibility and unrelated
state, and retained individual validation exits. Run 1's missing intake-hash
printout remains recorded as observability noise, but the frozen baseline and
fresh operator hash prove integrity. The five-phase rule is therefore retained
in `AGENTS.md`. No fourth candidate or threshold change was used.

#### Fix 5 retained implementation and closeout validation

- `AGENTS.md`: one eligible-case five-phase fast path; it does not apply when
  authority/target intake cannot be safely bounded before launch.
- This ledger: candidates A–C, all nine cold trials, diagnosis and corrected
  adjudication, exact measurements, residuals, and across-five evaluation.

| Command | Exit | Actual result |
| --- | --- | --- |
| `python -B .agents/tools/atomic_exact_edit.py --selftest` | 0 | 12 named cases passed; `SELFTEST OK` |
| `git diff --check` | 0 | No whitespace errors; Git emitted only configured line-ending conversion warnings |
| `python .agents/hooks/check_placement.py --strict` | 0 | 0 violations, 0 freshness findings; legacy and scratch inventories remained advisory |
| `python .agents/hooks/check_review_routing.py --strict` | 0 | Review routing OK against `origin/main` |
| `python .agents/hooks/check_map_links.py --strict` | 0 | 0 findings; 36 annotated non-resolving debt entries |
| `python .agents/hooks/check_dcp_receipt.py --strict` | 0 | All real receipts in the branch diff were shape-valid |
| `pwsh .github/scripts/run-doc-gates.ps1` | 0 | 22/22 local documentation gates passed |

## Across-five evaluation — 2026-07-16

| Fix | Status | Observed basis |
| --- | --- | --- |
| 1 — bounded stall containment | **PASS** | Preserve the previously verified Trial B result: 3/3 correct, failure-integral runs with bounded typed stalls. |
| 2 — ordinary shell launch | **PASS** | The owner enabled the already-trusted handler through CLI `/hooks`; a fresh Codex CLI 0.144.4 session returned `FORSETI_CODEX_HOOK_ADOPTION=ADOPTED`, then 3/3 unchanged cold runs completed correctly with no ordinary-shell stall, retry, fallback, or elevation. |
| 3 — native patch restoration | **PRODUCT_BLOCKED** | Native tool launch and patch-primitive restoration are Codex-owned; no repository implementation can satisfy the defined signal. |
| 4 — first fallback reliability | **PASS** | Final candidate D completed the first and only exact-edit apply in 3/3 cold trials; each patch was correct and all failure-integrity checks held. |
| 5 — dependency-round consolidation | **PASS** | Candidate C completed the correct, failure-integral case in five rounds in 3/3 trials; independent before/after hashes verify the run 1 note despite its missing intake printout. |

Evaluation: the five-fix sequence has not passed across all five because Fix 3
remains product-blocked. The sequence delivered verified passes for Fixes 1, 2,
4, and 5. Candidate C reached the frozen five-round target in 3/3 correct,
failure-integral trials and is retained as workflow authority. Ordinary shell
launch is now supported by the fresh adoption plus 3/3 cold result. No native-
patch, general tool-runtime, or all-five pass claim is supportable.

```yaml
direction_change_propagation:
  doctrine_changed: >
    After a stalled native patch primitive, agents use the repository-owned
    atomic exact-text helper as the checked fallback instead of hand-authoring a
    Git patch or temporary serialized plan.
  trigger: workflow_authority
  related_triggers: []
  controlling_sources_updated: [AGENTS.md, .agents/workflow-overlay/artifact-folders.md]
  downstream_surfaces_checked: [CLAUDE.md, .agents/workflow-overlay/README.md, .agents/workflow-overlay/source-loading.md, .agents/workflow-overlay/decision-routing.md, .agents/workflow-overlay/validation-gates.md, docs/workflows/forseti_repo_map_v0.md]
  intentionally_not_updated:
    - {path: CLAUDE.md, reason: "The shim imports AGENTS.md and must not duplicate the fallback rule."}
    - {path: .agents/workflow-overlay/source-loading.md, reason: "The helper is an execution utility rather than a new authority source."}
    - {path: .agents/workflow-overlay/validation-gates.md, reason: "The helper exposes its own focused self-test and introduces no new repository-wide gate class."}
  stale_language_search: 'rg -n -i "atomic_exact_edit|post-primitive-stall|post-stall fallback|hand-author.*git patch|\\.agents/tools" AGENTS.md CLAUDE.md .agents/workflow-overlay docs/workflows/forseti_repo_map_v0.md'
  stale_language_search_result: >
    Executed 2026-07-16 after the patch. Hits were limited to the new AGENTS.md
    rule, the new artifact-folder authority, and the reconciled repo-map route;
    no conflicting live fallback instruction was found.
  non_claims: [not general validation, not readiness, not native patch repair, not Fix 2 repair, not permission to normalize elevated shell execution]
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Eligible bounded repository changes use a five-phase fast path that batches
    the read-only intake and ordered validation while isolating mutation and
    preserving exact closeout and failure visibility.
  trigger: workflow_authority
  related_triggers: []
  controlling_sources_updated: [AGENTS.md]
  downstream_surfaces_checked: [CLAUDE.md, .agents/workflow-overlay/README.md, .agents/workflow-overlay/source-loading.md, .agents/workflow-overlay/decision-routing.md, .agents/workflow-overlay/validation-gates.md, docs/workflows/forseti_repo_map_v0.md, docs/workflows/efficiency/tool_calling_efficiency_improvement_sequence_2026_07_15_v0.md]
  intentionally_not_updated:
    - {path: CLAUDE.md, reason: "The shim imports AGENTS.md and must not duplicate the fast-path rule."}
    - {path: .agents/workflow-overlay/source-loading.md, reason: "The rule composes already-bounded reads and does not change source hierarchy or loading authority."}
    - {path: .agents/workflow-overlay/validation-gates.md, reason: "The rule preserves existing focused, broad, attribution, and closeout gates; it changes call composition, not validation philosophy."}
    - {path: docs/workflows/forseti_repo_map_v0.md, reason: "No path, owner, or navigation route changed."}
  stale_language_search: 'rg -n -i "five-phase fast path|bounded repo changes|latency-bearing tool rounds" AGENTS.md CLAUDE.md .agents/workflow-overlay docs/workflows/forseti_repo_map_v0.md'
  stale_language_search_result: >
    Executed 2026-07-16 after the retained patch. Hits were limited to the new
    AGENTS.md fast-path rule; no competing live instruction or weakened copy was
    found in the shim, overlay, or repository map.
  non_claims: [not general validation, not readiness, not Fix 2 shell repair, not Fix 3 native patch repair, not an all-five pass]
```

## Non-claims

- Not proof of root cause in the external Codex sandbox or process launcher.
- Not approval to normalize elevated shell execution.
- Not repair of the ordinary patch primitive.
- Not evidence that operation counts from different transcript accounting
  schemes are perfectly interchangeable.
- Not repair of Fixes 2 or 3 and not an all-five pass.
