# Handoff Packet — Wave-3 Duplication-Class Repairs

```yaml
retrieval_header_version: 1
artifact_role: cold cross-lane handoff packet (continuation artifact, not evidence)
scope: >
  Transfers the three remaining confirmed duplication-class repairs from the
  2026-07-16 slop audits to a fresh lane: ECR test-builder adoption, .github/scripts
  PowerShell helper dedup, and the Codex guard adapter selftest refactor.
use_when:
  - A fresh lane is commissioned to execute wave-3 duplication-class repairs.
  - Verifying what wave-3 covers and what it must not touch.
authority_boundary: retrieval_only
```

- output_mode: `file-write` (the receiving lane implements repo changes in its own worktree; this packet itself is chat-routing state, not a prompt)

## Load Contract

- packet_version: 1
- mode: max
- created_at: 2026-07-16
- created_by_lane: Claude (Anthropic) session "code-slop-examples" — provenance only, not authority
- workspace: C:\Users\vmon7\Desktop\projects\orca (create your OWN worktree off `origin/main`; do not work in the primary checkout or any existing worktree)
- handoff_path: docs/prompts/handoffs/dup_class_repairs_wave3_handoff_v0.md on branch `claude/handoff-dup-class-repairs`
- expected_branch: claude/handoff-dup-class-repairs (packet home; compare target = that branch tip on origin)
- expected_head: the single packet commit on that branch (fetch and read from origin; any local copy of this file is a convenience, the pushed branch is authoritative)
- expected_dirty_state_including_handoff_file: the packet branch contains exactly this one file added; your own work lane starts clean off `origin/main`
- load_rule: confirm-don't-trust; re-verify every load-bearing fact below against its compare target before acting; sender claims are hypotheses, not authority

## Goal Handoff

- long_term_goal: the Forseti codebase stays free of copy-paste drift — one owning home per shared behavior, deliberate divergence explicitly labeled, enforcement carried by clean exemplars plus the mechanical duplication gate.
- anchor_goal: land the three remaining confirmed duplication-class repairs from the 2026-07-16 audits (work items 1–3 below), behavior-preserving, via exemplar repair.
- success_signal: each class has exactly one shared home; every migrated call site is byte-equivalent in behavior (divergent copies stay local with a delta comment); all named validation observed green FOREGROUND; one commit per work item with a `review_routing_status:` trailer; nothing pushed to main and no PR merged; completion reported back to the operator for cross-vendor delegated review per `.agents/workflow-overlay/delegated-review-patch.md`.

## Open Decision / Fork

- decision: shape of the PowerShell helper dedup in `.github/scripts/` (work item 2)
  - options: (a) new dot-sourced `_common.ps1` owning `Stop-WithError` and repo-root resolution; (b) leave duplication in place as below-threshold (~20 lines today, grows per new script).
  - already constrained / off the table: renaming existing script entry points; changing any script's observable output or exit codes; `merge-when-green.ps1`'s "REFUSED:" wording is a deliberate delta from "ABORTED:" (human-facing refusal semantics) — parameterize or keep local, never unify the wording.
  - trade-offs: (a) one home + trivially shared by future scripts vs. one more file and dot-source ceremony; (b) zero churn vs. the exact drift disease this whole effort exists to stop.
  - owner of the call: receiver proposes in its report; Chief Architect (commissioning session) adjudicates before merge.
  - recommendation and why: (a) — the audit showed this directory grows scripts, and the duplicated helper has already forked wording once.

## Drift Guard

- DO NOT touch `forseti-harness/runners/**` — an active sibling lane (branch `runner-scaffold`) owns runner scaffolding; touching it guarantees a merge conflict.
- DO NOT touch `forseti-harness/cleaning/**` or `forseti-harness/data_lake/canonical_json.py` — an active bug-fix session (mixed-None ref sorting) plus an unmerged lane (branch `cleaning-dedup`) own that area.
- DO NOT touch `forseti-harness/capture_spine/**` validation files — branch `spine-validators` is under delegated review.
- DO NOT touch `.agents/hooks/guard_protected_actions.py` under any circumstances — its helper duplication is a documented deliberate exception (`.agents/hooks/_hooklib.py` docstring, lines 15–20): an ImportError there would disable the repo's only hard action gate.
- DO NOT weaken the Codex adapter's enforcement paths (work item 3 is selftest-only).
- Do not change test semantics; updating pin-contract tests (`forseti-harness/tests/contract/test_policy_module_version_pins.py`) when you touch a pinned module is allowed and required, with a "not output-shaping" annotation.
- Run ALL validation FOREGROUND with explicit timeouts — background pytest waits stalled four prior lanes in this workstream.
- pytest writes `_scratch/` at the repo root; delete it before any clean-tree assertion.
- Worktrees on this machine have been deleted by an unidentified concurrent process during this workstream. Commit early and often — branches in the shared `.git` are the only durable local store. If your worktree vanishes mid-task, recreate it from your branch; expect committed state to survive, uncommitted state to be lost.
- No push to main, no PR merge, no worktree removal of anything you did not create.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (entry per `AGENTS.md`: read `.agents/workflow-overlay/README.md` before project work)
- targets to enter the ladder: the work-item file sets under "Exact Next Authorized Action"
- already loaded by sender (weak orientation, 2026-07-16, NOT authority): audit findings summarized inline below
- must load first (before strict or actionable steps): the current on-disk content of every file you will edit; `forseti-harness/README.md` ("Shared Helpers" section); `.agents/hooks/README.md` (adoption-rule paragraph)
- load rule: re-run progressive source loading per overlay; this packet's summaries only seed the ladder

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- Adoption rule (as narrowed by adjudicated cross-vendor finding DD-01): before writing a private helper, check the shared home; migrate a stale copy in the same work unit ONLY when the bound change already touches or depends on that helper contract; a deliberately divergent copy stays with a one-line delta comment.
  - decided in: `.agents/hooks/README.md` and `forseti-harness/README.md`
  - compare target: reread-required (quote the current paragraphs before relying on them)
  - verify before: any migration decision
- Duplication gate: `.agents/hooks/check_shared_helper_duplication.py` — diff-scoped CI gate over added private re-definitions of named shared helpers in `forseti-harness/**` (tests excluded) and `.agents/hooks/*`; suppression = a comment containing `harness_utils`, `_hooklib`, or `helper-delta` on the def line, the line above, or the first body line.
  - compare target: reread-required (the file's docstring is current authority for patterns/scope)
  - verify before: deciding whether work item 4 needs a gate row
- Exemplar-repair principle (validated twice by cold-agent probes in this workstream): new authors copy the nearest existing file, so repairing the copied-from exemplars redirects all future code without exhaustive migration.
  - decided in: operational practice this workstream; no doctrine file owns it yet (a skill proposal is deferred by owner decision)
  - verify before: nothing — orientation only

## Active Objective

Execute three bounded, behavior-preserving duplication-class repairs (ECR test builders, PowerShell script helpers, Codex adapter selftest) in one fresh lane, one commit per item, and report back for cross-vendor review. Do not merge.

## Exact Next Authorized Action

1. Create your own worktree off `origin/main` (`git worktree add <fresh path> -b wave3-dup-repairs origin/main` from the primary checkout `C:\Users\vmon7\Desktop\projects\orca`).
2. Work item 1 — ECR test-builder adoption: `forseti-harness/tests/unit/test_ecr_identity_deriver.py` (~lines 19–86), `test_ecr_inspectability_deriver.py` (~21–90), `test_ecr_timing_deriver.py` (~23–91) each re-implement `_timing()`/`_slice()`/`_packet()` builders (~209 lines total) that `forseti-harness/tests/unit/_ecr_builders.py` already provides and documents itself as the shared home for (six sibling files already import it). Migrate the three files onto `_ecr_builders`; where a local builder's defaults genuinely differ from the shared one, keep the local piece with a delta comment rather than changing test behavior. Validation: `python -m pytest forseti-harness/tests/unit/test_ecr_identity_deriver.py forseti-harness/tests/unit/test_ecr_inspectability_deriver.py forseti-harness/tests/unit/test_ecr_timing_deriver.py -q` plus the six existing importer test files — identical pass counts before and after.
3. Work item 2 — PowerShell helpers per the Open Decision: `Stop-WithError` duplicated at `install-local-hooks.ps1:~25` and `spin-up-lane.ps1:~49`; `Stop-WithRefusal` variant at `merge-when-green.ps1:~56`; repo-root resolution repeated in those plus `lane-health-check.ps1:~450`. Validation: `pwsh .github/scripts/install-local-hooks.ps1 -VerifyOnly` and a `-DryRun` of `merge-when-green.ps1` against any open PR, outputs byte-compared to pre-change runs.
4. Work item 3 — Codex adapter selftest refactor: `.codex/hooks/forseti_guard_codex_adapter.py` `_selftest` (~lines 204–431) repeats a subprocess→json→assert block ~10 times with `except Exception: ok = False` swallowing real crashes. Factor `_expect_denied(...)`/`_expect_allowed(...)` helpers; preserve the fail-safe verdict semantics (an unexpected exception must still fail the selftest, and may additionally print what it was); DO NOT touch anything outside `_selftest`. Validation: `python .codex/hooks/forseti_guard_codex_adapter.py --selftest` passes; `python -m py_compile` clean; confirm zero diff outside the selftest region (`git diff` review).
5. Work item 4 — gate decision: after items 1–3, decide whether any new class is def-nameable inside the gate's scope (`forseti-harness/**` non-test Python, `.agents/hooks/*`). Sender's assessment: none qualifies (tests are excluded from gate scope; `.ps1` is not Python; `.codex/hooks/` is outside gate scope) — if you concur, record the decision in your report instead of forcing a gate row.
6. Close: one commit per work item, each with a `review_routing_status: not_needed -- <one-line reason>` trailer; full suite `python -m pytest forseti-harness/tests -q -n 4` FOREGROUND (600s timeout) once at the end; `python .agents/hooks/check_shared_helper_duplication.py --strict --base origin/main` must pass; delete `_scratch/`; report completion with observed evidence. STOP — no push to main, no PR, no merge; the operator routes cross-vendor review.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` (root), `CLAUDE.md` → loads AGENTS.md
- Overlay authority: `.agents/workflow-overlay/README.md` and the files it routes to; delegated review convention: `.agents/workflow-overlay/delegated-review-patch.md`
- User constraints: behavior-preserving only; exemplar repair over exhaustive repair; skill authoring explicitly postponed by owner — do not draft skills
- Source-read ledger:
  - `forseti-harness/tests/unit/_ecr_builders.py`
    - Role: shared home for work item 1
    - Load-bearing: yes
    - Compare target: reread-required
    - Last checked: 2026-07-16 (audit, line refs approximate)
    - Reuse rule: import; do not modify unless a migrated file needs a genuinely shared new default, and then behavior-preserving only
  - `forseti-harness/tests/unit/test_ecr_{identity,inspectability,timing}_deriver.py`
    - Role: migration targets, work item 1
    - Load-bearing: yes
    - Compare target: reread-required
    - Last checked: 2026-07-16
    - Reuse rule: migrate builders; assertions untouched
  - `.github/scripts/{install-local-hooks,spin-up-lane,merge-when-green,lane-health-check}.ps1`
    - Role: migration targets, work item 2
    - Load-bearing: yes
    - Compare target: reread-required
    - Last checked: 2026-07-16
    - Reuse rule: outputs and exit codes byte-stable; REFUSED/ABORTED wording delta preserved
  - `.codex/hooks/forseti_guard_codex_adapter.py`
    - Role: migration target, work item 3 — SAFETY INFRASTRUCTURE, selftest region only
    - Load-bearing: yes
    - Compare target: reread-required
    - Last checked: 2026-07-16
    - Reuse rule: `_selftest` only; enforcement untouched
  - `.agents/hooks/check_shared_helper_duplication.py`
    - Role: gate authority for work item 4 decision
    - Load-bearing: yes
    - Compare target: reread-required
    - Last checked: 2026-07-16
    - Reuse rule: read; extend only if a def-nameable in-scope class emerges
- Source gaps: none known beyond reread-required markers
- Strict-only blockers: none
- Not-proven boundaries: this packet is a continuation artifact — it proves nothing about validation, readiness, or acceptance

## Current Task State

- Completed (other lanes, context only): waves 1–2 of the dedup effort are merged or committed-and-under-review; the duplication gate is live in CI.
- Partially completed: nothing in wave-3 scope has been started — all three work items are untouched on `origin/main`.
- Broken or uncertain: none in scope.

## Workspace State

- Branch: receiver creates `wave3-dup-repairs` off `origin/main`
- Head: `origin/main` at commission time = e489e75ffae43fde148516b6e5d43ef78537e3f2 (2026-07-16); refetch — main moves fast on this repo
- Dirty or untracked state before handoff: receiver lane starts clean
- Dirty or untracked state after writing the handoff file: the packet branch `claude/handoff-dup-class-repairs` adds exactly this file
- Target files or artifacts: listed per work item above
- Related worktrees or branches (DO NOT TOUCH): `runner-scaffold`, `cleaning-dedup`, `coercion-sweep`, `spine-validators`, `small-fixes`, and any `agent-*`/`review-*` worktree under `.claude/worktrees/`

## Changed / Inspected / Tested Files

- None changed by wave-3 yet; inspection evidence for every target is dated 2026-07-16 with approximate line refs — reread before editing.

## Frozen Decisions

- Exemplar repair over exhaustive repair.
  - Evidence: two cold-agent probes (2026-07-16) showed fresh agents copy the nearest exemplar and adopted shared homes unprompted.
  - Consequence: fix the copied-from files and the shared home; do not chase every copy.
- Behavior preservation is the bar; strictness changes are findings, not fixes.
  - Evidence: wave-2 review standard; spine-validators lane preserved per-lane scanner behavior via parameters.
  - Consequence: byte-stable outputs, exit codes, and messages unless a delta comment marks deliberate divergence.
- Delegated cross-vendor review before merge for every wave.
  - Evidence: `.agents/workflow-overlay/delegated-review-patch.md` (provisional convention, invoked by owner each wave so far).
  - Consequence: the receiver's job ends at "committed + reported"; landing is the commissioning session's.

## Mutable Questions

- PowerShell dedup shape (see Open Decision).
- Whether `_ecr_builders.py` needs one new shared default to absorb the three files' variants, or the variants stay local with delta comments.
  - What would resolve it: the per-file diff during work item 1.

## Superseded / Dangerous-To-Reuse Context

- "Vanished worktrees were harness auto-cleanup after agent sessions ended" — superseded: an unidentified concurrent process on this machine deletes worktrees, including a live session's. Current replacement: the drift-guard rule (commit early; branches are the durable store).
- The pre-DD-01 adoption-rule wording ("migrate whenever the containing file is touched") — superseded by the narrowed rule now printed in both READMEs; do not enforce the old wording.
- Any line-number reference in this packet — approximate as of 2026-07-16; reread-required before edits.

## Commands And Verification Evidence

- Sender-observed baseline (2026-07-16): full suite `python -m pytest forseti-harness/tests -q -n 4` green at `origin/main` ancestors (3,457–3,468 passed across recent runs); gate `--strict` green on clean trees.
  - Re-run target: both commands, in your fresh worktree, before starting — a red baseline is a STOP-and-report, not something to fix in this lane.
- Known flake: `tests/contract/test_runner_artifacts.py` Windows file-lock teardown (WinError 32); passes in isolation; rerun alone before treating as a finding.

## Blockers And Risks

- Concurrent worktree deletion (see Drift Guard) — mitigation: commit per work item immediately.
- Main moves frequently (5+ merges during the sender's session) — mitigation: your lane is docs/tests/scripts-scoped; refresh from origin/main just before your final full-suite run.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: the three ECR test files still carry local builders (grep `def _packet`); the PowerShell helpers still duplicated (grep `Stop-WithError`); the adapter `_selftest` still has the repeated block (grep `except Exception:` count in that region); gate scope/docstring current; both README rule paragraphs current.
- Compare target for each: the live file at your lane's HEAD.
- Load outcomes: `REUSE` only after all checks pass; a missing/changed target → `STALE_REREAD_REQUIRED` (re-derive scope) or report the delta; anything conflicting with the Drift Guard → `BLOCKED_DRIFT`, report back instead of proceeding.
- Sources to reread on drift: the target files themselves plus both READMEs.

## Do Not Forget

- Your report must include observed command outputs (counts, exit codes), not claims — the commissioning session independently re-runs them before adjudication.
