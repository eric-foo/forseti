# Handoff Packet — Wave 5: Author the Slop-Audit Skill from Workstream Lessons

```yaml
retrieval_header_version: 1
artifact_role: cold cross-lane handoff packet (continuation artifact, not evidence)
scope: >
  Transfers the capstone of the 2026-07 code-slop workstream to a fresh lane:
  decide whether the repeatedly-run slop-audit playbook warrants a reusable
  skill, and if so author it smallest-complete from the session's hard-won
  lessons; if not, distill the load-bearing lessons into existing homes.
use_when:
  - A fresh lane is commissioned to make the slop-audit skill (or decide against it).
  - Verifying the lesson corpus and the kill-criterion for a new standing artifact.
authority_boundary: retrieval_only
```

- output_mode: `file-write` (receiver authors a SKILL.md and/or distilled lesson edits in its own worktree)

## Load Contract

- packet_version: 1
- mode: max
- created_at: 2026-07-17
- created_by_lane: Claude (Anthropic) session "code-slop-examples" — provenance only, not authority
- workspace: C:\Users\vmon7\Desktop\projects\orca (create your OWN worktree off `origin/main`)
- handoff_path: docs/prompts/handoffs/slop_audit_skill_authoring_wave5_handoff_v0.md on branch `claude/wave5-skill-handoff`
- expected_branch: claude/wave5-skill-handoff (packet home on origin; authoritative)
- expected_head: the packet commit on that branch (read from origin)
- expected_dirty_state_including_handoff_file: packet branch adds this one file; your work lane starts clean off `origin/main`
- load_rule: confirm-don't-trust; every commit SHA, artifact path, and count below is a hypothesis — re-verify against live `origin/main` before relying on it (main was c981974d at authoring; refetch — it moves).

## Goal Handoff

- long_term_goal: Forseti resists code slop (duplication, bloat, ceremony, drift) by default — the environment teaches the right pattern without every agent re-deriving it, and enforcement stays smallest-complete rather than accreting.
- anchor_goal: convert this workstream's repeated, validated playbook and its hard-won lessons into the SMALLEST COMPLETE reusable form — which may be a new skill, a set of distilled lesson-cells in existing homes, or a mix — after first deciding whether a new standing artifact earns its keep.
- success_signal: a future cold agent facing a slop-audit-shaped task (or about to write a duplicate helper / oversized function / unwired checker) is correctly steered by whatever this lane produces, WITHOUT loading a rigid script that rots; the produced artifact cites real evidence from this workstream; its own recurring toll is named and judged worth paying; it does not duplicate existing workflow-kernel skills; nothing pushed to main, no PR merged; completion reported for cross-vendor delegated review.

## Open Decision / Fork

- decision: **what form the reusable artifact takes** — this is the load-bearing call, and the updated SCI kernel makes it non-obvious.
  - options:
    - (a) **New skill** `slop-audit` under `.agents/skills/<name>/SKILL.md` (mirrored to `.claude/skills/`, matching the repo's existing skill shape — see `creator-audience-triangulation`, `forseti-product-lead`): a composition/playbook that orchestrates the existing workflow-kernel skills for the slop-audit case.
    - (b) **Distill into existing homes** via the `workflow-distill` discipline: install 3–5 lesson-cells at their decision nodes (e.g. the exemplar-repair principle into the harness/hooks READMEs' adoption-rule sections; the "unwired ≠ unused" completeness rule into the hooks audit doctrine; the operational lessons into a lane-runner note) — no new skill artifact.
    - (c) **Minimal both**: a thin skill that is mostly pointers to existing skills + the few genuinely novel lessons, plus one or two distilled cells.
  - already constrained / off the table: a large rigid step-by-step playbook skill. This workstream's own hooks audit just cut ~1,183 lines of unwired enforcement and the updated kernel weighs subtraction equally with addition and warns on ceremony debt — a fat new standing skill every agent may load is exactly the surface the kernel says to resist. Also off the table: duplicating capability that already exists as workflow-kernel skills (`workflow-delegated-review-patch`, `workflow-handoff`, `workflow-distill`, `workflow-code-review`) — the slop-audit artifact must ORCHESTRATE or POINT AT these, never re-implement them.
  - trade-offs: (a) is discoverable and nameable but is the heaviest new surface and risks becoming a rotting script; (b) is smallest-total-surface and installs each lesson where it fires, but has no single discoverable "run a slop audit" entry point; (c) balances discoverability against surface but must be disciplined about what earns a place in the skill vs a pointer.
  - owner of the call: the receiver recommends after cataloguing the lessons and running the kill-criterion; the Chief Architect (commissioning session) adjudicates. This is a doctrine-shaped decision (it adds standing agent-governance surface) — treat any new skill or binding as owner-gated, not receiver-final.
  - recommendation and why: run the kill-criterion FIRST (below). Bias toward (c) or (b): the highest-value lessons (exemplar repair, unwired≠unused, subtraction-equally) are principles that belong at their decision nodes, and the orchestration (audit→sweep→cross-vendor review→adjudicate→gate) is already covered by composing existing skills. A new skill earns its place ONLY for the genuinely novel, non-covered glue. Do not default to (a) because "we did a lot of work" — sunk cost is not a keep-criterion.

- kill-criterion (apply before authoring anything): for each candidate lesson or the skill as a whole, ask — (1) is this already covered by an existing workflow-kernel skill or doctrine surface? (point at it, don't re-encode); (2) what does every future agent PAY to have this standing (load cost, maintenance, drift risk)? (3) what specific recurring defect class does it prevent, with evidence it recurs? If (1) is yes, or (3) has no recurrence evidence, it does NOT get new surface — at most a pointer. Record the kill-decision per lesson in the deliverable.

## Drift Guard

- A skill is ceremony debt. Apply the exact lens this workstream's hooks audit applied to the 38 hooks: name the recurring toll, name the defect class caught, and let the owner weigh it. Do not add a rigid playbook.
- Do NOT duplicate existing workflow-kernel skills. `workflow-delegated-review-patch` (cross-vendor review), `workflow-handoff` (cold packets), `workflow-distill` (lesson-cells), `workflow-code-review` already exist and were used heavily this workstream. The slop-audit artifact composes/points at them.
- Route authoring through the `workflow-skill-authoring-discipline` skill (available in the environment) — it owns named-failure, smallest-change, contradiction-scan, overlay-boundary, and promotion-boundary discipline for creating/editing reusable skills. Read it before writing a SKILL.md.
- Match the repo's ACTUAL skill shape: Forseti skills live at `.agents/skills/<name>/SKILL.md` and mirror to `.claude/skills/<name>/SKILL.md` (verify the mirror obligation and any registry/list-sync requirement before adding one — a new skill may itself need registration).
- Cite REAL evidence (verified SHAs / artifact paths from this workstream), never a summary as authority. If a claim can't be tied to a landed artifact, mark it a hypothesis.
- No deployment/install/readiness claims. A drafted skill is a candidate, not an installed capability.
- Run any validation FOREGROUND with explicit timeouts (background waits stalled four lanes in this workstream). Commit early — worktrees on this machine have been deleted mid-run by a concurrent process; branches are the durable store.
- No push to main, no PR merge, no worktree removal you did not create.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (entry per `AGENTS.md`: read `.agents/workflow-overlay/README.md` before project work); skill adoption/registration doctrine: `.agents/workflow-overlay/skill-adoption.md`
- targets to enter the ladder: the existing skills (`.agents/skills/*/SKILL.md`), the `workflow-skill-authoring-discipline` skill, and the landed workstream artifacts below
- already loaded by sender (weak orientation, NOT authority): the lesson corpus below
- must load first: `workflow-skill-authoring-discipline`; `AGENTS.md` updated "Smallest Complete Intervention" kernel; one existing Forseti `SKILL.md` for shape
- load rule: re-run progressive source loading per overlay; the corpus below only seeds the ladder

### The lesson corpus (this workstream's hard-won, evidence-tagged lessons — the raw material)

Each lesson has a one-line gist + where it was proven. The receiver decides per the kill-criterion whether each becomes skill content, a distilled cell, or a pointer to existing doctrine.

1. **"Shared home exists but the copies were never deleted" is the dominant slop signature.** The diagnosis that started it all: helpers duplicated across dozens of files under 5 different names while a shared home existed unused. Proven: the `_utc_now`/`_sha256` epidemic; fixed in #999-lineage sweeps. Note: `harness_utils.py` and `.agents/hooks/_hooklib.py` are the harness/hooks shared homes; `forseti-harness/source_capture/projection_shared.py`, `forseti-harness/cleaning/_shared.py`, `forseti-harness/capture_spine/shared_validation.py`, `forseti-harness/runners/_scaffold.py` were created as new homes this workstream.
2. **Exemplar repair beats exhaustive repair.** Cold agents copy the nearest existing file, so fixing the 3–5 copied-from exemplars redirects all future code at a fraction of the cost of fixing every copy. Proven live: two cold-agent probes (a fresh Sonnet writing a new runner adopted `harness_utils`; a fresh Sonnet writing a new hook adopted `_hooklib`) — NEITHER was told about the convention; the clean exemplars taught it.
3. **A mechanical gate is the durable backstop, one regex row per def-nameable class.** `.agents/hooks/check_shared_helper_duplication.py` (landed #999, extended #1018/#1035) flags added private re-definitions of named shared helpers, with a `helper-delta` comment escape hatch (def line / line above / first body line). It caught a real path-traversal hole in `tiktok/batch_coverage.py` within a day of landing. LIMIT: inline-block duplication (runner scaffold) is NOT def-nameable and must NOT be gated — exemplar repair covers that class.
4. **Behavior-preservation is only as safe as the tests that would catch a change.** Weak coverage gates a refactor: the decomposition lane deferred `run_price_payload_capture` (14 tests / 399 lines) behind characterization tests; strong-coverage functions split freely. For test-fixture refactors, prove byte-identical effective kwargs via a pre/post capture snapshot (test-fixture-sugar lane, #1037).
5. **"Unwired ≠ unused" — the completeness test must include product-workflow consumers, not just harness wiring.** The hooks audit's biggest miss: it flagged `check_commission_signal_board_output.py` (1,264 lines) as an unused cut because no settings/CI/githooks referenced it — but a live pilot spine's playbook required running it by hand, a unit test loaded it, and a product architecture decision explicitly retained it. Cross-vendor review + owner "assess first" caught it; the validator was restored. This is the sharpest lesson: a wiring census is not a usage census.
6. **Cross-vendor delegated review before merge, adjudicated as claims.** Every wave went through a different-vendor (GPT-5) controller under `workflow-delegated-review-patch`; findings were adjudicated as hypotheses (accept/modify/reject), not inherited. It caught real defects the authoring side missed (non-importable commit history; an AST seam-detector false-certification; the CSB deletion).
7. **Subtraction weighs equally with addition; a new gate/skill is ceremony debt.** The updated SCI kernel's two new lenses. The hooks audit itself was a subtraction pass that cut ~1,183 lines of inert enforcement. Any artifact THIS lane produces is subject to the same test — including the skill it might write.
8. **Operational lessons (bake into whatever runs future lanes):** validation runs FOREGROUND with explicit timeouts (background waits idled four lanes to stalls); commit per work-unit immediately (a concurrent process deletes worktrees, including live ones); pin handoffs to BRANCHES not directory paths (two review worktrees vanished mid-review); delete pytest `_scratch/` before clean-tree assertions; pin-contract tests (`test_policy_module_version_pins.py`) are IN-scope to bump when you touch a pinned module; partition file ownership per parallel lane to avoid merge conflicts; the merge treadmill (strict up-to-date branch protection + a busy main) is real — a merge queue is the structural fix.

### Earlier-decided concepts (inline gist + verify pointer)

- Updated Smallest Complete Intervention kernel — subtraction equal to addition; ceremony debt named per change. Decided in: `AGENTS.md` "Smallest Complete Intervention" (~commit cd046d05). Verify before: the kill-criterion and any new-surface decision.
- The adoption rule (narrowed by adjudicated finding DD-01): migrate a stale private copy in the same work unit ONLY when the bound change touches/depends on that helper contract; a divergent copy stays with a one-line delta comment. Decided in: `.agents/hooks/README.md` + `forseti-harness/README.md` adoption-rule sections. Verify before: encoding any migration guidance.

## Active Objective

Decide the smallest-complete reusable form for this workstream's lessons and produce it — a slop-audit skill, distilled lesson-cells, or a disciplined mix — routed through the skill-authoring discipline, cited to real evidence, with its own toll named. Do not merge.

## Exact Next Authorized Action

1. Create your own worktree off `origin/main` (`git worktree add <fresh path> -b wave5-slop-skill origin/main` from `C:\Users\vmon7\Desktop\projects\orca`). Refetch — main moves.
2. Read `workflow-skill-authoring-discipline`, the updated SCI kernel, `.agents/workflow-overlay/skill-adoption.md`, and one existing Forseti `SKILL.md` for shape.
3. Catalogue the eight lessons above against the kill-criterion: for each, mark `existing-skill-covers` (→ pointer), `distill-cell` (→ install at its decision node), or `novel-skill-content` (→ earns a place in a new skill). Record the per-lesson decision + evidence SHA/path in a short deliverable (e.g. `docs/hygiene/slop_audit_skill_scoping_v0.md`, or the lane PR body if the overlay binds no home — ask the overlay).
4. Per the Open Decision outcome, PRODUCE the smallest-complete artifact: a `SKILL.md` (matching repo shape + mirror + any registry obligation) for the novel-glue subset, and/or `workflow-distill` cells for the principle lessons. Keep the skill (if any) a thin orchestrator that points at `workflow-delegated-review-patch`/`workflow-handoff`/`workflow-distill`/`workflow-code-review`, not a re-implementation.
5. Validate FOREGROUND: if a skill is added, confirm its registration/mirror obligations are met and any hook/test that enumerates skills still passes (`pwsh .github/scripts/run-doc-gates.ps1`); `python .agents/hooks/check_shared_helper_duplication.py --strict --base origin/main`; delete `_scratch/`.
6. Close: report the form chosen, the per-lesson kill-decisions with evidence, what was authored vs pointed-at, and the new artifact's named recurring toll. STOP — no push to main, no PR, no merge; the operator routes cross-vendor review of the produced skill/cells.

## Authority And Source Ledger

- Repository instructions: `AGENTS.md`, `CLAUDE.md`; overlay `.agents/workflow-overlay/README.md`; skill adoption `.agents/workflow-overlay/skill-adoption.md`; delegated review `.agents/workflow-overlay/delegated-review-patch.md`
- User constraints: smallest-complete (a skill is ceremony debt — justify or don't build it); do not duplicate existing workflow-kernel skills; cite real evidence; skill authoring routed through `workflow-skill-authoring-discipline`
- Source-read ledger:
  - `.agents/skills/creator-audience-triangulation/SKILL.md` (+ the two product-lead skills) — Role: repo skill shape/mirror precedent · Load-bearing: yes · Compare target: reread-required
  - `.agents/hooks/check_shared_helper_duplication.py` (on main) — Role: the gate lesson-3 artifact · Load-bearing: yes · Compare target: reread-required (blob present on main; landed #999/#1018/#1035)
  - `forseti-harness/source_capture/projection_shared.py` (on main) — Role: a new-shared-home artifact · Load-bearing: yes · Compare target: reread-required
  - `docs/hygiene/hooks_smallest_complete_audit_ledger_v0.md` (on branch `claude/hooks-audit-handoff-context-44c325`, PR #1051 — may be on main by the time you start) — Role: the subtraction-audit + unwired≠unused evidence · Load-bearing: yes · Compare target: reread-required
  - `docs/prompts/handoffs/{dup_class_repairs_wave3,oversized_function_decomposition,hooks_smallest_complete_audit}_handoff_v0.md` — Role: prior packets = the handoff pattern this lane continues · Load-bearing: no (orientation) · Compare target: reread-required
- Not-proven boundaries: this packet proves nothing about validation, readiness, or acceptance; the lesson corpus is this session's experience, authoritative only after the receiver re-verifies each against its cited artifact.

## Current Task State

- Completed (context): waves 1–4 dedup + decomposition merged (#1016/#1017/#1035/#1036/#1037/#1038/#1040 and lineage); the duplication gate is live; the hooks smallest-complete audit is adjudicated and in PR #1051.
- Partially completed: nothing in wave-5 started — no skill or distilled cell exists yet.
- Broken or uncertain: none in scope.

## Workspace State

- Branch: receiver creates `wave5-slop-skill` off `origin/main`
- Head: `origin/main` at authoring = c981974d (2026-07-17); refetch
- Related branches DO NOT TOUCH: `claude/hooks-audit-handoff-context-44c325` (PR #1051, may land) and any `agent-*`/`review-*` worktree
- Handoff-file dirty impact: the packet branch adds this one file

## Changed / Inspected / Tested Files

- None changed by this lane yet; all artifact pointers dated 2026-07-17 — reread before relying on them.

## Frozen Decisions

- A new standing artifact must pass the kill-criterion; sunk cost is not a keep-reason. Evidence: updated SCI kernel + this workstream's own hooks-audit subtraction pass.
- Do not duplicate existing workflow-kernel skills. Evidence: they were used successfully this workstream; re-encoding is pure surface.
- Cross-vendor delegated review adjudicated as claims is the acceptance path for anything this lane produces. Evidence: it caught the CSB miss and three other real defects.

## Mutable Questions

- The artifact form (Open Decision).
- Whether a new skill needs registry/list-sync registration (a hook may enforce it) — resolve from `skill-adoption.md` + any registry hook before adding one.
- Which lessons are genuinely novel vs already-doctrine — resolve per-lesson via the kill-criterion.

## Superseded / Dangerous-To-Reuse Context

- Any SHA / path / count in this packet — dated 2026-07-17; reread-required (main moves; #1051 may land, relocating the ledger to main).
- "Build a slop-audit skill because we ran the playbook five times" — DANGEROUS as a premise: it is the sunk-cost reflex the kill-criterion exists to check. The workstream is evidence the playbook WORKS, not proof a standing skill is the smallest-complete way to carry it.
- "Vanished worktrees were auto-cleanup" — superseded: a concurrent process deletes worktrees; commit early.

## Commands And Verification Evidence

- Cold-agent probe evidence (lesson 2), author-observed 2026-07-16: a fresh Sonnet writing `run_probe_receipt_demo.py` imported `harness_utils.sha256_bytes`/`utc_now_z` unprompted, citing migrated runners as its model; a fresh Sonnet writing `check_demo_placeholder.py` used `from _hooklib import repo_root, to_relposix`. Re-derivable by re-running the probe prompts against current main.
- Baseline: full suite green on recent main (~3,5xx passed / 7 skipped). Re-run before starting; a red baseline is STOP-and-report.

## Blockers And Risks

- The temptation to over-build a fat skill (the sunk-cost reflex) — mitigation: the kill-criterion and the Open Decision recommendation toward (b)/(c).
- A new skill may carry hidden registration/mirror obligations — mitigation: resolve from skill-adoption doctrine before authoring.
- Concurrent worktree deletion; fast-moving main — mitigation: commit early, refresh before final validation.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: the duplication gate still exists on main and its current pattern list; whether PR #1051 (hooks-audit ledger) has landed (relocates the ledger evidence to main); the current set of `.agents/skills/*/SKILL.md` and the mirror/registration obligation; that `workflow-skill-authoring-discipline` is available.
- Compare target: live source at your lane HEAD / current `origin/main`.
- Load outcomes: `REUSE` after checks pass; a moved artifact → `STALE_REREAD_REQUIRED` (re-derive the pointer); any pressure to build a fat skill or duplicate an existing workflow-kernel skill → treat as a `BLOCKED_DRIFT`-class signal, re-apply the kill-criterion and report to the owner.

## Do Not Forget

- The deliverable that matters most is the per-lesson KILL-DECISION with evidence, not the skill file. If the honest answer is "most of this is already doctrine or existing skills; here are the two genuinely novel cells," that is a SUCCESS, not an under-delivery — it is the subtraction lens applied to our own output.
