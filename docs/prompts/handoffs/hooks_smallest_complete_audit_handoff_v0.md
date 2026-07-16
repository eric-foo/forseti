# Handoff Packet — Smallest-Complete Audit of the Enforcement Hooks

```yaml
retrieval_header_version: 1
artifact_role: cold cross-lane handoff packet (continuation artifact, not evidence)
scope: >
  Transfers a smallest-complete audit of the .agents/hooks enforcement layer
  (38 hooks, ~20,634 py lines, 23 CI gate steps) plus the 27 policy-version
  pins, measured against the updated Smallest Complete Intervention kernel's
  subtraction and ceremony-debt lenses. Analysis-first; execution is bounded to
  behavior-preserving internal simplification, with gate/pin REMOVAL owner-gated.
use_when:
  - A fresh lane is commissioned to audit and smallest-complete the hooks layer.
  - Verifying the analyze-vs-execute boundary on safety infrastructure.
authority_boundary: retrieval_only
```

- output_mode: `file-write` (receiver writes a ranked audit artifact + behavior-preserving hook edits in its own worktree)

## Load Contract

- packet_version: 1
- mode: max
- created_at: 2026-07-17
- created_by_lane: Claude (Anthropic) session "code-slop-examples" — provenance only, not authority
- workspace: C:\Users\vmon7\Desktop\projects\orca (create your OWN worktree off `origin/main`)
- handoff_path: docs/prompts/handoffs/hooks_smallest_complete_audit_handoff_v0.md on branch `claude/handoffs-decomp-and-hooks`
- expected_branch: claude/handoffs-decomp-and-hooks (packet home on origin; authoritative)
- expected_head: the packet commit on that branch (read from origin)
- expected_dirty_state_including_handoff_file: packet branch adds this file + a sibling decomposition packet; your work lane starts clean off `origin/main`
- load_rule: confirm-don't-trust; re-measure every count below against live source before relying on it (main was a52873ca at authoring; refetch)

## Goal Handoff

- long_term_goal: Forseti's enforcement layer is smallest-complete — every hook, gate, and pin pays a recurring toll that a real, still-live defect class justifies; ceremony that no longer catches anything is removed, not carried.
- anchor_goal: produce a ranked, evidence-backed toll-vs-defect ledger for all 38 hooks + 23 CI gate steps + 27 policy pins, and EXECUTE the subset of reductions that are behavior-preserving internal simplifications; SURFACE (do not execute) every gate/pin removal for owner decision.
- success_signal: a durable audit artifact ranks each hook/gate/pin by (recurring toll paid by every future work unit) vs (real defect class it still catches), each row citing evidence; behavior-preserving internal simplifications land with every touched hook's `--selftest` still green and its documented behavior unchanged; no fail-closed path weakened; no gate or pin removed without a recorded owner sign-off; nothing pushed to main, no PR merged; completion reported for cross-vendor delegated review.

## Open Decision / Fork

- decision: the boundary between what the receiver EXECUTES vs what it only PROPOSES.
  - options: (a) execute only strictly-internal, behavior-preserving simplifications (shrink a hook's body while its selftest and documented I/O contract stay identical), propose everything else; (b) also execute removal of a hook/gate/pin the audit finds catches nothing, without waiting for owner sign-off; (c) analysis-only, execute nothing.
  - already constrained / off the table: (b) — this is safety infrastructure; removing a gate or pin changes what CAN reach main. A wrong removal is high-lock-in and only discovered when a real defect slips through. Removal is an owner decision.
  - trade-offs: (a) delivers real reduction now while keeping the irreversible calls with the owner; (c) is safe but under-delivers the "smallest-complete their ass" ask; (b) is the recoverability violation the updated kernel's "prefer reversible, fails-loud" rule forbids for infra.
  - owner of the call: Chief Architect (commissioning session) sets the boundary; default below unless overridden.
  - recommendation and why: (a). Execute behavior-preserving internal simplification (highest-value, lowest-risk: e.g. a 1,560-line hook whose real check is "contains one of five strings" can shed chassis without changing its verdict). Rank gate/pin REMOVALS in the artifact with a clear kept/cut recommendation each, and let the owner adjudicate those in one pass.

## Drift Guard

- `.agents/hooks/guard_protected_actions.py` is UNTOUCHABLE. It is the deliberately import-free hard EP-03/EP-01 gate; an ImportError or logic slip there disables the repo's only hard action gate (including its fail-CLOSED merge path). Do not simplify, dedup, or import it. Its duplication is a documented deliberate exception (`_hooklib.py` docstring lines 15–20).
- NEVER weaken a fail-closed path. Advisory hooks fail OPEN by design (a bug costs one advisory); gating hooks (`--strict`, merge auth) fail CLOSED by design (a bug blocks, never silently passes). A "simplification" that flips either asymmetry is a defect, not a reduction — flag, never make it.
- Behavior-preserving means: same stdin→verdict→exit-code contract, same documented behavior in `.agents/hooks/README.md`, same `--selftest` result, same CLI flag surface (`--hook`/`--strict`/`--selftest`/`--diff`/`--audit`/`--changed`/etc. are wired externally in `.claude/settings.json`, `ci.yml`, `.githooks/`, `run-doc-gates.ps1` — renaming one ripples through all of them; do not rename).
- Do NOT remove any hook, CI gate step, or policy pin in this lane — those are owner-gated (Open Decision). Propose them in the artifact.
- The duplication gate `check_shared_helper_duplication.py` was added THIS workstream (2026-07-16); it is in scope for the toll-vs-defect ledger like any other hook — assess it honestly (its defense: it caught a real path-traversal hole in `tiktok/batch_coverage` that a human audit missed), but do not exempt it from the same standard.
- Run ALL validation FOREGROUND. Commit per hook (or per small batch) immediately — worktrees on this machine have been deleted mid-run by a concurrent process; branches are the durable store.
- No push to main, no PR merge, no worktree removal you did not create. `--selftest` on every touched hook AND `_hooklib.py` must pass before each commit; run `pwsh .github/scripts/run-doc-gates.ps1` (the full CI hook-gate set) before the final report.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`; hook wiring authority: `.agents/hooks/README.md`; validation-gate registry: `.agents/workflow-overlay/validation-gates.md`; CI wiring: `.github/workflows/ci.yml`; pin gate: `forseti-harness/tests/contract/test_policy_module_version_pins.py`
- targets to enter the ladder: `.agents/hooks/*.py`, `.agents/hooks/README.md`, the four wiring surfaces above
- already loaded by sender (weak orientation, measured 2026-07-17 on main, NOT authority): 38 hook .py files totalling ~20,634 lines; 23 hook gate-steps in `ci.yml`; 27 policy-pinned modules; biggest hooks `check_prompt_output_mode.py` ~1,560, `check_csb_scanning_artifact.py` ~1,394, `check_map_links.py` ~1,322; the overlay it enforces is ~6,999 lines across 19 files
- must load first: the actual body + docstring (each hook names its own rule authority) of every hook before judging its toll; `AGENTS.md` "Smallest Complete Intervention" (updated kernel)
- load rule: re-run progressive source loading per overlay; these counts only seed the ladder

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- Updated Smallest Complete Intervention kernel adds two lenses this audit is built on: (1) **weigh subtraction equally with addition** — removing a rule/step/gate has the same standing as adding one, and when both satisfy the request prefer the smaller total surface; (2) **ceremony debt** — a change small in diff can install a large recurring toll (a required step, gate, pin, receipt, field every future work unit pays); name what each future unit pays and what defect class it catches so the owner can weigh it.
  - decided in: `AGENTS.md` "Smallest Complete Intervention" (updated ~commit cd046d05)
  - compare target: reread-required
  - verify before: every toll-vs-defect judgment
- Hooks are harness-portable as a WHOLE directory (stdlib-only, copied together); `_hooklib.py` is the shared helper home; a hook's I/O contract is documented in `.agents/hooks/README.md` and its behavior is externally wired. These constraints bound what "simplify" may touch.
  - decided in: `.agents/hooks/README.md` + `_hooklib.py` docstring
  - verify before: any structural edit

## Active Objective

Rank the entire enforcement surface by recurring-toll vs live-defect-caught, execute the behavior-preserving internal simplifications, and hand the owner a clean kept/cut decision list for every gate/pin whose removal is the actual reduction. Do not merge.

## Exact Next Authorized Action

1. Create your own worktree off `origin/main` (`git worktree add <fresh path> -b hooks-smallest-complete origin/main` from `C:\Users\vmon7\Desktop\projects\orca`). Re-measure the counts above.
2. Build the ledger: for EACH of the 38 hooks, each of the 23 CI gate steps, and each of the 27 policy pins, record: (i) what it enforces, in one line; (ii) the recurring toll every future work unit pays (a required trailer? a pin bump on every touch? a doc-convention lint? a per-write advisory?); (iii) the real, still-live defect class it catches, with evidence it still fires (search git history / receipts for a real catch, or mark `no-evidence-of-catch`); (iv) a verdict: `keep-as-is` / `simplify-internal` / `propose-remove` / `propose-merge-with <X>`. Write it to a durable artifact (ask the overlay where audit artifacts live — likely `docs/hygiene/` or `docs/review-outputs/`; if unbound, put it in the lane PR body and say so).
3. EXECUTE the `simplify-internal` set only: shrink each such hook's body while its `--selftest`, documented I/O contract, flag surface, and fail-open/closed asymmetry stay identical. Prime candidates from the sender's survey (RE-VERIFY each): `check_prompt_output_mode.py` (~1,560 lines whose core check is `token in TOKENS` over five strings — enormous chassis-to-logic ratio); the ~34 hooks each carrying a private inline `selftest()` PASS/FAIL printer and a stdin→verdict→fail-open `__main__` scaffold that could move to `_hooklib` (this is itself a dedup — behavior-preserving, and the duplication gate should stay green through it). Commit per hook or small batch; `--selftest` green before each commit.
4. Do NOT execute any `propose-remove` or `propose-merge`. Leave those as the artifact's kept/cut recommendation list for owner adjudication.
5. Close: `pwsh .github/scripts/run-doc-gates.ps1` (full CI hook-gate set) green; every touched hook + `_hooklib.py` `--selftest` green; `check_shared_helper_duplication.py --strict --base origin/main` green; delete `_scratch/`; report the ledger, what was executed vs proposed, and observed evidence. STOP — no push, no PR, no merge, no gate/pin removal.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md`, `CLAUDE.md`; hook wiring `.agents/hooks/README.md`; validation-gate registry `.agents/workflow-overlay/validation-gates.md`; CI `.github/workflows/ci.yml`; delegated review `.agents/workflow-overlay/delegated-review-patch.md`
- User constraints: smallest-complete the hooks (updated kernel, subtraction + ceremony-debt lenses); execution bounded to behavior-preserving internal simplification; gate/pin removal owner-gated; skill authoring postponed
- Source-read ledger:
  - `.agents/hooks/*.py` (38 files) — Role: audit targets · Load-bearing: yes · Compare target: reread-required · Reuse rule: simplify-internal only, per-hook selftest green; guard_protected_actions.py untouchable
  - `.agents/hooks/_hooklib.py` — Role: shared home for extracted scaffold · Load-bearing: yes · Compare target: reread-required · Reuse rule: may GAIN shared scaffold; its own selftest must stay green
  - `.agents/hooks/README.md` — Role: each hook's documented I/O contract (the behavior-preservation spec) · Load-bearing: yes · Compare target: reread-required
  - `.github/workflows/ci.yml`, `.claude/settings.json`, `.githooks/`, `.github/scripts/run-doc-gates.ps1` — Role: external wiring (flag names are a contract) · Load-bearing: yes · Compare target: reread-required · Reuse rule: do not rename flags
  - `forseti-harness/tests/contract/test_policy_module_version_pins.py` — Role: the 27-pin gate · Load-bearing: yes · Compare target: reread-required · Reuse rule: audit/propose only, no removal
- Not-proven boundaries: this packet proves nothing about validation, readiness, or acceptance; the audit's "no-evidence-of-catch" mark is a search result, not proof a hook is useless — the owner weighs it.

## Current Task State

- Completed (context): waves 1–4 of the dedup effort merged or committed-under-review; the duplication gate (hook #39 relative to this audit's 38-count if already merged — re-count) is live.
- Partially completed: nothing in this audit started.
- Broken or uncertain: none.

## Workspace State

- Branch: receiver creates `hooks-smallest-complete` off `origin/main`
- Head: `origin/main` at authoring = a52873ca (2026-07-17); refetch
- Related branches DO NOT TOUCH: all `agent-*`/`review-*` worktrees and the unmerged lane branches
- Handoff-file dirty impact: packet branch adds this file + the decomposition packet

## Changed / Inspected / Tested Files

- None changed yet; all counts measured 2026-07-17 on main — re-measure before relying on them.

## Frozen Decisions

- guard_protected_actions.py is never touched. Evidence: `_hooklib.py` docstring lines 15–20; it is the only hard gate.
- Gate/pin removal is owner-gated, not receiver-executed. Evidence: updated kernel's "prefer reversible/contained; surface irreversible high-lock-in tradeoffs" — infra removal is exactly that.
- Advisory-fail-open / gating-fail-closed asymmetry is invariant. Evidence: `.agents/hooks/README.md` contract section.

## Mutable Questions

- The execute-vs-propose boundary (Open Decision).
- Whether the shared selftest/main-scaffold extraction into `_hooklib` is worth it or itself adds coupling — decide from how uniform the 34 copies actually are.

## Superseded / Dangerous-To-Reuse Context

- Any count in this packet — measured 2026-07-17; re-measure (the hook count changes as this workstream's gate lands).
- "Add a gate per audit" as a reflex — the updated kernel explicitly warns this is how ceremony debt accrues; this audit exists partly to counter it, so do not resolve a finding by adding yet another hook.
- "Vanished worktrees were auto-cleanup" — superseded: a concurrent process deletes worktrees; commit per hook.

## Commands And Verification Evidence

- Sender-measured (2026-07-17, main): `.agents/hooks/*.py` = ~20,634 lines / 38 files; `ci.yml` hook gate-steps = 23; policy pins = 27; overlay = ~6,999 lines / 19 files. Re-run: `wc -l .agents/hooks/*.py`, `grep -cE 'agents/hooks/.*\.py' .github/workflows/ci.yml`, count `"...\.py":` entries in the pin file.
- Re-run target for every executed simplification: that hook's `--selftest` + `run-doc-gates.ps1`.

## Blockers And Risks

- This is the repo's safety infrastructure — the highest-risk surface to edit. Mitigation: the analyze-vs-execute boundary (Open Decision) keeps every irreversible call with the owner.
- Flag-rename ripple across four wiring surfaces — mitigation: do not rename; simplify bodies only.
- Concurrent worktree deletion; fast-moving main — mitigation: commit per hook, refresh before final gate run.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: the live hook count and line total; that `guard_protected_actions.py` is still import-free (never touch it regardless); each candidate hook's `--selftest` passes at baseline; the fail-open vs fail-closed intent of each hook you touch (read its `__main__`).
- Compare target: live source at your lane HEAD.
- Load outcomes: `REUSE` after checks pass; a changed count → `STALE_REREAD_REQUIRED` (re-measure); any pressure to remove a gate/pin or touch the guard → `BLOCKED_DRIFT`, report to owner rather than proceeding.

## Do Not Forget

- The reduction that actually shrinks the surface is usually a REMOVAL (a gate/pin that no longer catches anything), and that one is the owner's call — so the artifact's kept/cut list is the highest-value deliverable, not the lines you personally delete. Under-deliver the removals into a clean decision list rather than executing them.
