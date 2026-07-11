# Review-Report Mechanics Runner — Fused Continuation Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Implementation handoff prompt
scope: >
  Cold-lane continuation of the owner-authorized fused implementation for a
  deterministic review-report mechanics runner. The runner automates report
  assembly and mechanical verification only; substantive review judgment stays
  outside the tool.
use_when:
  - Opening the Codex-managed implementation worktree for branch codex/review-report-mechanics.
  - Resuming the already-cleared fused pipeline at the implementation lane.
authority_boundary: retrieval_only
```

**Goal:** prevent repeatable report-assembly and evidence-capture mistakes for
future cold agents without automating review judgment.

**Done looks like:** a cold agent can assemble and verify an exact review-report
diff without hand-copying tool output, while every permission, write, diff,
checker, and readback failure remains visible and the tool emits no finding,
severity, vulnerability, verdict, or remediation judgment. This is the executor
target and later review axis to attack, not a review pass bar.

## Prompt Binding

- Prompt source: `docs/prompts/handoffs/review_report_mechanics_fused_continuation_handoff_v0.md`
- Template kind: `handoff`; bundled generic handoff layout used because the
  Forseti template registry has no registered implementation-handoff template.
  Current owner authorization binds this otherwise-unbound implementation kind.
- Output mode: `file-write` for this durable handoff prompt.
- Receiver output frame: bounded source diff, observed validation evidence,
  post-implementation delegated-review prompt, commit, push, and focused PR.
- Edit permission: `implementation-authorized` for the exact source targets below.
- Model lane: unbound and not required; do not recommend or imply a runtime model.
- Review routing: carry the fused `recommended` advisory to
  `after_all_steps_pre_closeout`; it reviews the runner diff, not the substantive
  reviews the runner will help package.

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: implementation-authorized
  target_scope: ".github review-report mechanics runner, focused tests, and discoverability only"
  dirty_state_checked: yes
  blocked_if_missing: "clean Codex-managed worktree on codex/review-report-mechanics or fresh source contradicting the frozen route"
repo_map_decision: not_needed
repo_map_reason: "Targets and owning overlay surfaces are exhaustive in this prompt."
thread_operating_target_continuity:
  carried_forward: no
  reason: no_visible_active_target
  changed_from_input: no
  lifecycle_status: not_applicable
  if_changed_reason: ""
```

## Load Contract

- Packet mode: `max`, embedded in this durable handoff prompt.
- Source-loading mode: `repo-overlay-bound`.
- Expected repository: the Codex project rooted from
  `C:\Users\vmon7\Desktop\projects\orca`.
- Expected branch: `codex/review-report-mechanics`.
- Baseline compare target: `origin/main` at
  `ed1966a1d65d245f20e6b078157e058516ba3d89` before this handoff is committed.
- Expected start state: clean branch containing this handoff artifact and no
  runner implementation changes.
- Load rule: confirm-don't-trust. Re-read every load-bearing source and compare
  live branch, HEAD, dirty state, and target paths before editing.

## Goal Handoff

- Long-term goal: reduce no-value latency for cold review-and-patch agents while
  preserving every defect-catching and owner-steering boundary.
- Anchor goal: make report assembly and mechanical verification deterministic.
- Success signal: the runner eliminates hand-copied diff truncation, CRLF
  expansion, whitespace drift, and silent checker/readback failures without
  making or changing a substantive review decision.

## Open Decision / Fork

None open. The owner fixed the domain boundary in the commissioning thread:
automate mechanical and technical report operations only; do not automate review
work, vulnerability identification, finding selection, severity, verdicts,
remediation, or patch-content judgment.

## Drift Guard

- Do not add an arbitrary command runner, manifest language, shell evaluation,
  review classifier, patch applier, or vulnerability scanner.
- Do not modify `.agents/hooks/check_review_summary.py` or the active
  `claude/doc-gates-runner` lane. The existing checker remains the sole summary
  semantics owner; the doc-gates runner has a different CI-mirroring purpose.
- Do not claim the runner bypasses the Windows sandbox. Permission denial must
  remain a named environment blocker; a harness approval may rerun one bounded
  operation, but the runner never hides the gate.
- Do not broaden into prompt doctrine, review doctrine, CI wiring, global skills,
  external workflow source, or unrelated cleanup.

## Inherited Context To Re-establish

### Source-loading state

- Policy pointer: `.agents/workflow-overlay/source-loading.md`.
- Must read first: `AGENTS.md`, `.agents/workflow-overlay/README.md`, this prompt,
  `.agents/workflow-overlay/validation-gates.md` -> Current Gates,
  `.agents/workflow-overlay/safety-rules.md`, and the target checker interfaces.
- Target checker interfaces:
  `.agents/hooks/check_review_output_provenance.py` and
  `.agents/hooks/check_review_summary.py`.
- Implementation/lifecycle pointer:
  `docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md` -> per-lane
  PR flow, Codex lane-start writeability, manual patch discipline, and work-unit
  PR boundary.
- Previously loaded source in the sender thread is orientation only. Re-read the
  live branch before actionable use.

### Earlier-decided behavior

- `workflow-assumption-gate` returned `READY_WITH_VERIFIED_LEDGER`: explicit
  paths and Git/checker substrates can preserve the judgment boundary; temp-path
  environment variables do not bypass the sandbox.
- Fused implementation scoping returned `ROUTE_COMPLETE` with a recommended
  post-implementation adversarial review.
- `workflow-spec-writing` returned `SPEC_COMPLETE_READY_FOR_SCOPING`.
- `micro-decision-locking` returned `locked`, `route_ready: true`.
- Verify pointer: this prompt's Frozen Decisions and Implementation Route plus
  live owning sources. Do not trust these summaries if current source conflicts.

## Active Objective

Implement the smallest complete review-report mechanics runner. It consumes a
reviewer-authored draft with one explicit diff token plus explicit worktree,
base, report, and patch paths; it assembles and verifies the report while
preserving all review prose outside the token.

## Exact Next Authorized Action

1. Confirm this handoff against the live branch and return one load outcome:
   `REUSE`, `PARTIAL_REUSE`, `STALE_REREAD_REQUIRED`, `BLOCKED_DRIFT`,
   `BLOCKED_MISSING_PACKET`, or `BLOCKED_UNVERIFIABLE`.
2. REFERENCE-LOAD `fused`; do not redo the cleared assumption, scoping, spec, or
   micro lanes unless fresh source invalidates a frozen route fact.
3. SOURCE-LOAD the named task sources, declare `SOURCE_CONTEXT_READY` or
   `SOURCE_CONTEXT_INCOMPLETE`, then resume fused at the overlay-owned
   implementation lane.
4. Implement, validate, route the carried review advisory, and complete the
   lane's commit/push/PR lifecycle only if every bound gate clears.

## Frozen Decisions

1. The runner may invoke only Git and the two bound report-shape checkers. It
   must not execute arbitrary user commands.
2. It exposes `assemble` and read-only `verify` modes.
3. `assemble` accepts a draft containing exactly one
   `{{REVIEW_MECHANICS_UNIFIED_DIFF}}` token, an explicit report destination,
   an explicit base ref (default `HEAD`), and one or more explicit patch paths.
4. The report path must remain under `docs/review-outputs/`; every selected path
   must resolve inside the supplied worktree.
5. The runner generates per-file `git diff --no-ext-diff --unified=0` output,
   supports explicitly named tracked and untracked patch files, rejects an empty
   aggregate diff, and runs `git diff --check` for tracked changes.
6. The runner replaces only the unique token. Reviewer prose before and after it
   must remain byte-for-byte unchanged.
7. It writes atomically, rereads the final report, verifies the exact generated
   diff block occurs once, runs strict provenance checking, and consumes summary
   findings from the existing checker without reimplementing its predicates.
8. Unknown nonzero exits, internal errors, permission failures, malformed input,
   checker findings in strict buckets, or readback mismatch are `GATE FAIL` and
   produce a nonzero runner exit. Advisory enum drift remains `INFO`.
9. The receipt contains observed paths, hashes, exit codes, and gate buckets
   only. It contains no substantive review conclusion.
10. Replacing an existing report requires an explicit replace flag; a failed
    post-write check remains visible and is not silently deleted or called pass.

## Likely Touch Points

- `.github/scripts/review-report-mechanics.py`
- `.github/scripts/README.md`
- `forseti-harness/tests/unit/test_review_report_mechanics.py`
- A post-implementation delegated adversarial review prompt under
  `docs/prompts/reviews/`, authored only after the completed runner diff exists.

Do not touch `.agents/hooks/README.md`; another active lane already modifies it.

## Implementation Route

- `STEP-01`: confirm the managed worktree passes the lane-start write/index
  probe. Stop if normal source edits are not reliable.
- `STEP-02`: implement the stdlib-only runner with `assemble`, `verify`, compact
  JSON receipt output, path containment, exact diff generation, atomic write,
  and fail-visible checker/readback handling.
- `STEP-03`: add focused unit/integration tests and short discoverability docs.
  Tests must prove byte preservation, unique-token enforcement, tracked and
  untracked diffs, empty-diff rejection, outside-root rejection, checker
  failure propagation, readback mismatch detection, and absence of review-domain
  outputs.
- `STEP-04`: run validation, inspect the actual diff, then trigger the carried
  post-implementation review routing before closeout.

## Validation Contract

- Smoke-run any new/custom runner selftest under a 30-second timeout. A timeout
  stops as `VALIDATION_HOOK_TIMEOUT`; do not retry the hung command.
- Run the focused pytest module for the runner.
- Run an integration assembly against a temporary Git repository and the real
  checker interfaces where practical.
- Run `git diff --check` and inspect every changed hunk; do not treat
  `diff --check` as content correctness.
- Run prompt provenance/output-mode checks for this handoff and any generated
  review prompt.
- Run repository gates required by the changed paths. Missing or unknown
  evidence is blocked/not-run, never pass.

## Review Routing Obligation

The carried advisory is:

```yaml
adversarial_review: recommended
highest_value_checkpoint: after_all_steps_pre_closeout
review_target: completed review-report mechanics runner diff
why_this_checkpoint: challenge fake-pass and domain-boundary failures without interrupting implementation
```

After implementation and validation, invoke `workflow-delegated-review-patch`
and `workflow-prompt-orchestrator` to file the paste-ready review prompt. The
implementation commit body must carry exactly one valid
`review_routing_status: routed <prompt-path>` line. If the prompt cannot be
produced, stop as `review_routing_status: blocked -- <reason>` and do not claim
fused closeout.

## Current Task And Workspace State

- Completed: diagnosis; assumption gate; Cynefin routing; fused scoping; spec;
  micro-decision locking; fresh `origin/main` fetch; clean branch creation.
- Not started: runner source, tests, docs, review prompt, validation, commit,
  push, and PR.
- Prior blocker: a manually created `C:\tmp` worktree could not reliably update
  existing files or its Git index under the current thread's restricted token.
  The clean worktree was removed so Codex can recreate the branch as a managed
  writable worktree. Do not reuse the failed manual-write path as evidence that
  the managed destination is blocked.
- Branch before this handoff commit: `codex/review-report-mechanics` at
  `ed1966a1d65d245f20e6b078157e058516ba3d89`, tracking `origin/main`.
- Dirty state before this handoff: clean.

## Mutable Questions

- Exact internal function boundaries and test helper organization are
  agent-owned implementation details, provided they preserve the frozen
  interface and scope.
- If the current summary checker has no stable callable explicit-path surface,
  stop and report the interface gap rather than duplicating its review-summary
  rules or editing that checker in this work unit.

## Superseded / Dangerous-To-Reuse Context

- Superseded: the initial idea that setting `TMPDIR`, `TEMP`, or `TMP` would fix
  the Windows sandbox. Source probes showed those values were honored but
  directory creation still failed with `WinError 5`.
- Dangerous: using size-limited shell-tool output as the source for an embedded
  report diff; it previously truncated the diff to one file.
- Dangerous: `git -c core.autocrlf=false diff` on a CRLF worktree; it previously
  expanded the patch into whole-file diffs.
- Dangerous: default-context diffs inside reports governed by blanket trailing-
  whitespace checks; use the locked zero-context form.
- Dangerous: automating patch application. Patch content and source-changing
  judgment remain outside this runner.

## Confirm-Don't-Trust Checklist

- Verify the prompt path exists and is readable.
- Verify the branch and current HEAD; compare ancestry to baseline
  `ed1966a1d65d245f20e6b078157e058516ba3d89`.
- Verify the worktree is clean except for authorized new work.
- Verify the three likely source targets are unmodified before editing.
- Re-read current checker CLIs/callable surfaces and owning gate boundaries.
- If any load-bearing fact drifted, return the precise load outcome before
  implementation.

## External And Claim Boundaries

- `jb`, external workflow source, installed skills, and plugin-cache copies are
  not Forseti authority and must not be edited.
- This handoff is continuation state and implementation authority only. It is
  not validation, review approval, readiness, source promotion, deployment, or
  evidence that the runner works.
- No runtime-model recommendation is authorized or present.
