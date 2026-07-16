# Handoff Packet — Decompose Three Oversized Functions

```yaml
retrieval_header_version: 1
artifact_role: cold cross-lane handoff packet (continuation artifact, not evidence)
scope: >
  Transfers a behavior-preserving decomposition of the three highest-ranked
  oversized functions (>200 lines) found by the 2026-07-16 slop audit's
  decomposition lens, ranked by length x responsibilities x template risk.
use_when:
  - Verifying decomposition scope, provenance, or per-function test-coverage history.
authority_boundary: retrieval_only
```

- output_mode: `file-write` (receiver implements source changes in its own worktree)

## Disposition (updated 2026-07-17 — packet FULLY EXECUTED, historical)

- ALL THREE functions are DELIVERED behavior-preserving on branch
  `claude/handoffs-decomp-context-97c95b`, PR #1040 to `main`:
  - fn1 `46376ec7`, fn2 `009fc69e` (suites 57/57 and 50/50 unmodified;
    cross-vendor delegated review returned `no_material_defect_found`).
  - fn3 per Open Decision option (a): characterization pins landed FIRST for
    the four untested failure classes (`01e34407`) and the untested
    success-path packet wiring (`7d1e9047`), both verified green against the
    pre-split runner; then the split along the author-marked `# --- N ---`
    seams (`1b8344af`). All 23 price_payload tests green post-split and
    replayed green against the pre-split runner by the delegate; cross-vendor
    delegated review (delegate: OpenAI) returned `NO_PATCH_WARRANTED` with an
    empty diff; adjudicated accepted.
- Do NOT commission any new lane from this packet. All function sections below
  are historical provenance only; check PR #1040 / `main` for the current
  source shape. The behavioral do/don't pins for fn3's failure semantics live
  in `forseti-harness/tests/unit/test_price_payload_failure_paths.py` (module
  docstring).
- This disposition records observed lane outcomes only; it is not validation,
  readiness, or merge status — confirm PR #1040's state on origin before
  relying on it.

## Load Contract

- packet_version: 1
- mode: max
- created_at: 2026-07-17
- created_by_lane: Claude (Anthropic) session "code-slop-examples" — provenance only, not authority
- workspace: C:\Users\vmon7\Desktop\projects\orca (create your OWN worktree off `origin/main`)
- handoff_path: docs/prompts/handoffs/oversized_function_decomposition_handoff_v0.md on branch `claude/handoffs-decomp-and-hooks`
- expected_branch: claude/handoffs-decomp-and-hooks (packet home on origin; authoritative)
- expected_head: the packet commit on that branch (read from origin)
- expected_dirty_state_including_handoff_file: packet branch adds this file + a sibling hooks-audit packet; your work lane starts clean off `origin/main`
- load_rule: confirm-don't-trust; re-derive every line number below against live source before editing — main moves fast (was a52873ca at authoring; refetch)

## Goal Handoff

- long_term_goal: Forseti code is smallest-complete — each unit does one job at a size a reader and reviewer can hold in one pass, with no behavior change smuggled into structural cleanup.
- anchor_goal: split the three named functions into a thin orchestrator + named single-responsibility extracts, behavior-preserving, one commit per function.
- success_signal: each function's own test suite passes UNMODIFIED before and after; no observable output, exit code, receipt byte, exception type, or ordering changes; each extract has one clear responsibility; the top-level function reads as a sequence of named steps; pin bumps carry a "not output-shaping" annotation; nothing pushed to main, no PR merged; completion reported for cross-vendor delegated review per `.agents/workflow-overlay/delegated-review-patch.md`.

## Open Decision / Fork

- decision: whether to decompose function 3 (`run_price_payload_capture`) in this lane at all.
  - options: (a) add characterization tests for its untested failure branches FIRST, then split; (b) split functions 1 and 2 only, and defer function 3 with a note that it needs test scaffolding first; (c) split all three trusting the existing 14 tests.
  - already constrained / off the table: option (c) — the audit measured only 14 tests (`test_price_payload_certification.py` 12, `test_price_payload_retry.py` 2) for 399 lines with many distinct failure-class branches (`page_fetch_failed`, `parser_no_chunks`, `byte_budget_exceeded`, `max_chunks_exhausted`, `anchor_not_found_thin_page/full_page`); splitting untested branches risks a silent behavior change no test would catch.
  - trade-offs: (a) safest but larger scope (characterization tests are net-new test code); (b) smallest-complete for THIS lane, cleanly defers the risky one; (c) fast but violates the behavior-preservation success signal's own safety basis.
  - owner of the call: receiver recommends in its report; Chief Architect (commissioning session) adjudicates.
  - recommendation and why: (b) for the first pass — deliver functions 1 and 2 (both strongly tested, low-risk) complete, and return function 3 as a scoped follow-up with the specific untested branches named. Do NOT silently do (c).

## Drift Guard

- BEHAVIOR-PRESERVING ONLY. No logic change, no bug fix, no reordering that changes observable behavior. If you find a bug while splitting, FLAG it — do not fix it in this lane (that is a separate authorized change).
- Do NOT touch any file owned by an unmerged sibling lane: branch `runner-scaffold` (runner scaffolding — it does NOT touch the price_payload runner, so function 3 is clear, but do not import or depend on its unmerged `runners/_scaffold.py`). If `runner-scaffold` has landed by the time you start, you MAY use the scaffold for function 3's packet-assembly extract, but that is optional, not required.
- Do NOT modify any test file except a pin bump in `forseti-harness/tests/contract/test_policy_module_version_pins.py`, and (only under Open-Decision option a) net-new characterization tests for function 3.
- Extracts are private module-level helpers (`_verb_noun(...)`) with precise types; do not create new public API, new classes, or a new module unless a function genuinely needs shared state threaded (prefer a small dataclass return over a god-object).
- Run ALL validation FOREGROUND with explicit timeouts — background pytest waits have stalled lanes in this workstream.
- pytest writes `_scratch/` at the repo root; delete before any clean-tree assertion.
- Commit per function immediately after its suite passes — worktrees on this machine have been deleted mid-run by a concurrent process; branches in the shared `.git` are the only durable local store.
- No push to main, no PR merge, no worktree removal of anything you did not create.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (entry per `AGENTS.md`: read `.agents/workflow-overlay/README.md` before project work)
- targets to enter the ladder: the three function files below + their test files
- already loaded by sender (weak orientation, 2026-07-16 audit, NOT authority): the responsibility breakdowns below
- must load first: the current body of each function (re-derive line numbers), each function's test file, and `forseti-harness/README.md` "Shared Helpers"
- load rule: re-run progressive source loading per overlay; these summaries only seed the ladder

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- Smallest Complete Intervention, updated kernel: `Complete` and `Smallest` are both load-bearing; decomposition is a *smallest-complete refactor*, not a rewrite — split only what the audit named, add nothing speculative.
  - decided in: `AGENTS.md` "Smallest Complete Intervention" (kernel updated ~commit cd046d05; also weighs subtraction equally with addition, and warns on ceremony debt)
  - compare target: reread-required
  - verify before: any judgment call on how far to split
- Behavior-preservation-via-strong-tests is the safety basis: a split is only as safe as the tests that would catch a behavior change. This is WHY function 3 (weak coverage) is gated behind the Open Decision.
  - verify before: starting function 3

## Active Objective

Turn three 200–598-line multi-responsibility functions into thin orchestrators over named single-responsibility extracts, behavior-preserving, one commit each, and report back for cross-vendor review. Do not merge.

## Exact Next Authorized Action

1. Create your own worktree off `origin/main` (`git worktree add <fresh path> -b decomp-oversized-fns origin/main` from `C:\Users\vmon7\Desktop\projects\orca`). Re-derive all line numbers (they will have shifted).
2. **Function 1 (HIGHEST template risk, strong tests) — `forseti-harness/source_capture/tiktok/live_batch_probe.py::_run_tiktok_live_batch_probe_with_engine`** (~line 500, ~598 lines). Three responsibilities: input normalization/validation (handle/URL normalization, `capture_route` validation, storage-state resolution, cadence-plan construction); the per-video capture loop (dispatch, 6+ failure-branch classification, row assembly); result aggregation (counts, `grid_result`/`cadence_result` payload). Proposed extracts: `_normalize_and_validate_probe_inputs(...)` → returns a small struct; `_capture_video_cadence_rows(...)` (the loop; may further extract `_process_single_video_capture` as a follow-on); `_build_probe_result_payload(...)`. Template risk is HIGH: the `tiktok/` directory is the repo's reference capture architecture, most likely copied for the next platform. Tests: `forseti-harness/tests/unit/test_tiktok_live_batch_probe.py` (57 tests) — strong; must pass unmodified. Commit.
3. **Function 2 (high template risk, strong tests) — `forseti-harness/source_capture/tiktok/creator_onboarding.py::run_tiktok_creator_onboarding`** (~line 522, ~454 lines). Five responsibilities, already visually delimited by `stage = "..."` markers: input validation; engine acquisition/bootstrap; suggested-accounts→close→grid→freeze→select phase; wait/cadence + grid-overlay deep-capture phase; exception/finally receipt assembly. Proposed extracts: `_validate_onboarding_inputs`, `_acquire_or_reuse_observation_engine`, `_run_suggested_grid_and_selection_phase`, `_run_grid_overlay_deep_capture_phase`, `_build_onboarding_receipt`. Tests: `test_tiktok_creator_onboarding.py` (49 tests) — strong; must pass unmodified. Commit.
4. **Function 3 (very high template risk, WEAK tests) — per the Open Decision** — `forseti-harness/runners/run_source_capture_price_payload_packet.py::run_price_payload_capture` (~line 210, ~399 lines). Seams are already author-marked with `# --- N ---` comments: discovery+retry, extract+certify, effective-signals, packet assembly+write. Proposed extracts map 1:1 onto those comment sections. This is the cleanest mechanical split BUT the weakest tested — do NOT proceed to the split without resolving the Open Decision (default: add characterization tests for the named untested branches first, or defer with a scoped note).
5. Close: full suite `python -m pytest forseti-harness/tests -q -n 4` FOREGROUND (600s) once at the end; `python .agents/hooks/check_shared_helper_duplication.py --strict --base origin/main` must pass; delete `_scratch/`; report per-function verdict + the Open-Decision recommendation with observed evidence. STOP — no push, no PR, no merge.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md`, `CLAUDE.md`; overlay `.agents/workflow-overlay/README.md`; delegated review `.agents/workflow-overlay/delegated-review-patch.md`
- User constraints: behavior-preserving; smallest-complete (updated kernel — no speculative extraction beyond the audited functions); skill authoring explicitly postponed by owner
- Source-read ledger:
  - `forseti-harness/source_capture/tiktok/live_batch_probe.py` — Role: fn1 target · Load-bearing: yes · Compare target: reread-required · Reuse rule: split named fn only, behavior-preserving
  - `forseti-harness/source_capture/tiktok/creator_onboarding.py` — Role: fn2 target · Load-bearing: yes · Compare target: reread-required · Reuse rule: same
  - `forseti-harness/runners/run_source_capture_price_payload_packet.py` — Role: fn3 target · Load-bearing: yes · Compare target: reread-required · Reuse rule: gated behind Open Decision
  - `forseti-harness/tests/contract/test_policy_module_version_pins.py` — Role: pin gate · Load-bearing: yes · Compare target: reread-required · Reuse rule: bump if a touched module is pinned, "not output-shaping"
- Not-proven boundaries: this packet proves nothing about validation, readiness, or acceptance

## Current Task State

- Completed (context): waves 1–3 of the dedup effort merged; wave-4 + runner-scaffold committed and awaiting cross-vendor review.
- Partially completed: nothing in decomposition scope started — all three functions untouched on `origin/main`.
- Broken or uncertain: none in scope.

## Workspace State

- Branch: receiver creates `decomp-oversized-fns` off `origin/main`
- Head: `origin/main` at authoring = a52873ca (2026-07-17); refetch — moves fast
- Related branches DO NOT TOUCH: `runner-scaffold`, `projection-security`, `coercion-topup`, `test-fixture-sugar`, any `agent-*`/`review-*` worktree
- Handoff-file dirty impact: the packet branch adds this file + the hooks-audit packet

## Changed / Inspected / Tested Files

- None changed by this lane yet; all inspection evidence dated 2026-07-16 with approximate line refs — reread before editing.

## Frozen Decisions

- Behavior preservation is the bar; a bug found during splitting is FLAGGED, not fixed here.
  - Evidence: updated SCI kernel + this workstream's review standard.
- Split depth is bounded by the audit's named functions; no speculative "while I'm here" extraction.
  - Evidence: `Smallest` clause of the updated kernel.

## Mutable Questions

- Function 3's scope (see Open Decision).
- Whether function 1's capture loop warrants the further `_process_single_video_capture` sub-extract or reads clearly as one extract — decide from the live body.

## Superseded / Dangerous-To-Reuse Context

- Any line number in this packet — approximate as of 2026-07-16; reread-required.
- "Vanished worktrees were harness auto-cleanup" — superseded: a concurrent process deletes worktrees, including live ones. Replacement: commit per function immediately.

## Commands And Verification Evidence

- Baseline (author-observed, recent main): full suite green (~3,49x passed / 7 skipped across recent runs). Re-run before starting; a red baseline is STOP-and-report, not something to fix here.
- Known flake: `tests/contract/test_runner_artifacts.py` Windows file-lock teardown (WinError 32/5); passes in isolation.

## Blockers And Risks

- Function 3's weak coverage (see Open Decision) — the primary risk; do not split it blind.
- Concurrent worktree deletion — mitigation: commit per function.
- Fast-moving main — mitigation: your files are narrow; refresh from origin/main before the final full-suite run.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: each function still exists at ~the named size (grep its `def`); each test file's current pass count; whether `runner-scaffold` has landed (changes function 3's optional scaffold use).
- Compare target: live source at your lane HEAD.
- Load outcomes: `REUSE` after checks pass; a moved/missing target → `STALE_REREAD_REQUIRED` (re-derive); a Drift-Guard conflict → `BLOCKED_DRIFT`, report back.

## Do Not Forget

- A structural refactor that changes even one effective value is a behavior change wearing cleanup's clothes. The tests are the proof; where the tests are weak (function 3), the proof is weak — which is the whole reason function 3 is gated.
