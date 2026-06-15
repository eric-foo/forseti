# Handoff Packet — Demand-Durability Cadence Runner / Scheduler (Step 3)

```yaml
retrieval_header_version: 1
artifact_role: Cold cross-lane handoff packet (continuation artifact, not readiness evidence)
scope: Transfer step 3 of the demand-durability capture rollout (build the cadence runner/scheduler that runs the series over time) to a fresh lane.
authority_boundary: retrieval_only
```

## Load Contract

- packet_version: v0
- mode: max
- created_at: 2026-06-15
- created_by_lane: capture-spine CA thread (provenance only; not an authority claim)
- workspace: C:\Users\vmon7\Desktop\projects\orca
- handoff_path: docs/prompts/handoffs/demand_durability_cadence_runner_step3_handoff_v0.md
- expected_branch: a fresh worktree/branch off `origin/main` (NOT the hot home branch `ecr-sp3-timing-deriver-slice1`)
- expected_head: `origin/main` was `739411f` at handoff; it moves — re-fetch.
- expected_dirty_state_including_handoff_file: this packet is newly created under tracked `docs/prompts/handoffs/` → untracked until committed on its lane.
- load_rule: **confirm-don't-trust** — re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: a trustworthy demand-durability substrate for Orca's beauty-vertical demand-read — capture that does not silently lie about comparability, coverage, tampering, or sampling gaps — **without capture ever scoring or judging demand (INV-1)**.
- anchor_goal: **build the cadence runner / scheduler** — run a *commissioned* demand-durability proxy series OVER TIME (the "real series"): repeated observations across days per the declared cadence, each observation a `SourceCapturePacket` populated by the step-2 durability-series writer.
- success_signal: a commissioned series, tied to a Decision Frame + a fixed SKU/source set, produces an ordered set of observations on the declared cadence; realized timings and any gaps are recorded as visible facts/limitations (a gap is recorded as un-observed, never "no change"); INV-1 preserved; the offline suite stays green.

## Open Decision / Fork

- decision: **the scheduling mechanism**.
  - options: (A) an in-harness runner the operator triggers once per slot (simplest; operator-paced); (B) an OS-level scheduled task / cron that invokes the runner per slot; (C) a long-running queue/loop process.
  - already constrained / off the table: must run a **bounded, commissioned series** (tied to a Decision Frame), not an open crawler; must reuse the step-2 writer + `cadence.py`; must record realized timings + gaps.
  - trade-offs: (A) zero standing infra, honest to the no-standing-capture posture, but operator must trigger each slot; (B) automatic across days, but a scheduled task is closer to "standing" — keep it bounded to the commissioned series' slot_count and retire it when the series completes; (C) most automated, highest standing-infra footprint — least aligned with the no-standing posture.
  - owner of the call: the receiving lane + owner.
  - recommendation: **(A) operator-triggered per-slot runner** for the first real series (smallest standing footprint, honest to commissioned-capture); consider (B) bounded-to-slot_count only if per-slot triggering proves impractical. Avoid (C) for now.
- decision: **first commissioned SKU/source set** — the pilot used Sol de Janeiro Brazilian Bum Bum Cream via `direct_http`; the real series picks the commissioned SKU(s) + Decision Frame (owner input).

## Drift Guard

- **Commissioned capture only**: the series is tied to a Decision Frame and a fixed SKU/source set (obligation contract Ob.1). The scheduler runs a bounded commissioned series — **NOT standing/opportunistic crawling**. Violating this turns capture into an unbounded crawler, breaking the commissioning gate.
- **no-gate-defeat**: anti-bot (honest/anti-blocking UA) OK; **STOP at any auth / CAPTCHA / Cloudflare *challenge***, record the limitation, re-probe (probe-then-pin, distillation A1b). Do not defeat a gate.
- **INV-1**: capture records observed facts + limits, never a demand verdict. The scheduler does not score or rank.
- **A gap is un-observed, never "no change"**: an un-sampled slot (skipped, failed) is recorded as a visible limitation; absence of an observation is NEVER recorded as "the source did not change."
- **Series-diff (Element 3) is STILL DEFERRED**: when enough observations accrue it becomes buildable and bakes in the A1c refinement (diff EXTRACTED demand-relevant values; raw `PreservedFile.sha256` is only a coarse inspect-flag). It is a SEPARATE follow-on, NOT step 3 — do not build change-detection here.
- **Step-2 dependency**: step 3 schedules repeated calls to the step-2 durability-series writer. Do NOT start step 3 until step 2's writer exists (see Inherited Context).

## Build Authorization (owner-granted, bounded — 2026-06-15)

The owner granted **bounded build authorization** for this step in this thread (2026-06-15), carried via the AGENTS.md accepted-handoff path ("implementation/runtime work requires explicit bounded authorization in the current turn **or accepted handoff**"). The receiving lane is authorized to BUILD the demand-durability **cadence runner / scheduler** without re-requesting per-turn authorization, BOUNDED to:

- **only steps 2 and 3 of the demand-durability rollout** (this step = the scheduler; step 2 = the writer). **NOT** broader capture-spine work — no ECR / Cleaning / Judgment derivers, no source-quality scoring, no other lanes.
- the Drift Guard above (commissioned-only, no-gate-defeat, INV-1, gap≠no-change, series-diff deferred).
- build on the lane's own worktree/branch + per-lane PR. **Landing to `main` stays owner-gated** — the receiving lane does not merge to `main` (except self-merging its **own** PR under the protected-action guard's verified exception).

This is a bounded grant for steps 2+3 only; it is **not a standing grant** and does not extend to any other capture-spine lane. Repeated live fetches across the commissioned series are within this grant; unbounded crawling is not.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md` (read `.agents/workflow-overlay/README.md` first, per AGENTS.md).
- targets to enter the ladder: `orca-harness/source_capture/cadence.py` (`build_cadence_plan`, `CadencePlan`, `to_dict()`), the **step-2 writer** (the runner step 2 builds — see dependency), `orca-harness/source_capture/models.py` (`intended_cadence` + the durability fields the writer sets), `docs/product/data_capture_spine/demand_durability_capture_pilot_v0.md` (§3 protocol), `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md` (Ob.1 commissioning gate, Ob.17 durability facts).
- already loaded (weak orientation, freshness-marked; not authority): this packet's claims about the hardened schema + the cadence primitive (sender verified at `origin/main 739411f`).
- must load first: the step-2 writer (must exist) + `cadence.py` + the pilot spec §3.
- load rule: receiver re-runs progressive source loading per overlay; the packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist + verify pointer)

- **Step-2 dependency — the durability-series writer**: step 3 invokes it per observation; it populates the hardened Element 1/2/4 fields. Decided/handed off in: `docs/prompts/handoffs/demand_durability_series_writer_step2_handoff_v0.md` (PR #114, OPEN at this handoff). Compare target: reread-required (confirm step 2's writer has landed before building step 3). Verify before: building the scheduler.
- **Cadence primitive**: `CadencePlan` (modes `fixed`/`bounded_jitter`) + `build_cadence_plan(...)` + `to_dict()` already exist; the pilot declared fixed daily×14. Decided in: `orca-harness/source_capture/cadence.py`. Compare target: reread-required. Verify before: writing scheduling math (reuse the primitive; don't re-invent).
- **Hardened durability fields + Ob.17 (conditional obligation)**: the fields the per-observation writer sets; `intended_cadence` is what the scheduler declares. Decided in: `orca-harness/source_capture/models.py` + obligation contract Ob.17 (PR #113, merged). Compare target: `models.py` sha256 `6b71dbe2b91ce9715f9eb601d390ae19f633be99936bc3616830727cda8cbf5d` at `origin/main 739411f`. Verify before: any field/cadence-population claim.
- **Series-diff deferred + A1c refinement** (diff extracted values, raw hash = inspect-flag): not part of step 3. Decided in: `docs/decisions/distillation_binding_data_capture_v0.md` A1c (PR #107, merged). Compare target: reread-required. Verify before: resisting building change-detection.
- **Pilot proved the per-observation machinery on live data** (SdJ Bum Bum Cream): step 3 repeats it on a cadence. Decided in: `docs/product/data_capture_spine/demand_durability_capture_pilot_v0.md` (PR #108, merged) §2–3.

## Active Objective

Build the demand-durability cadence runner/scheduler (step 3): run a commissioned, Decision-Frame-bound series over time by invoking the step-2 writer per slot on the declared cadence, recording realized timings + gaps, INV-1-preserving, tested, green suite, landed via a per-lane PR off fresh `origin/main`. Build authorization is granted (bounded — see Build Authorization).

## Exact Next Authorized Action

1. **Confirm-don't-trust**: `git fetch origin main`; verify (a) the **step-2 writer has landed** (its PR merged / the durability-population runner exists) — if not, **stop**: step 3 depends on it; (b) `models.py` durability fields + `cadence.py` present.
2. Confirm the commissioned scope with the owner: the SKU/source set + Decision Frame for the first real series (Open Decision).
3. Decide the scheduling mechanism (Open Decision; recommend operator-triggered per-slot).
4. Build the runner/scheduler in a fresh worktree off `origin/main`; reuse the step-2 writer + `cadence.py`; record realized timings + gaps.
5. Add tests (cadence honored; gap recorded as un-observed not no-change); run the full offline suite (baseline 861 passed / 2 skipped); `check_map_links.py --strict` if docs change.
6. Per-lane PR off fresh `origin/main` (push/PR prompts are the owner gate; do not merge to main).

## Authority And Source Ledger

- Repository instructions: `AGENTS.md` + `.agents/workflow-overlay/` (read overlay `README.md` first).
- Overlay authority: source-loading; dev-workflow / per-lane PR (`docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md`); safety / no-gate-defeat + commissioning (`.agents/workflow-overlay/safety-rules.md`, obligation contract Ob.1).
- User constraints: hardening merged; step 2 = writer (handed off, #114); step 3 = this scheduler; **bounded build authorization granted for steps 2+3 only**; confirm-don't-trust; owner takes merges.
- Source-read ledger:
  - `orca-harness/source_capture/cadence.py` — Role: the cadence primitive to reuse. Load-bearing: **yes**. Compare target: `reread-required`. Reuse rule: read before writing scheduling math.
  - step-2 writer (the runner step 2 builds; see #114) — Role: the per-observation populator step 3 invokes. Load-bearing: **yes**. Compare target: `reread-required` (must exist before step 3). Reuse rule: confirm landed first.
  - `orca-harness/source_capture/models.py` — Role: `intended_cadence` + durability fields. Load-bearing: **yes**. Compare target: sha256 `6b71dbe2…` @ `739411f`.
  - `docs/product/data_capture_spine/demand_durability_capture_pilot_v0.md` (§3) — Role: the protocol step 3 automates. Load-bearing: **yes**. Compare target: `reread-required`.
  - `docs/product/data_capture_spine/core_spine_v0_data_capture_spine_obligation_contract_v0.md` (Ob.1, Ob.17) — Role: commissioning gate + durability obligation. Load-bearing: **yes**. Compare target: `reread-required`.
  - `docs/decisions/distillation_binding_data_capture_v0.md` (A1c) — Role: series-diff deferral context. Load-bearing: no. Compare target: `reread-required`.
- Source gaps: the step-2 writer's exact interface is unknown until step 2 lands (it's the dependency).
- Strict-only blockers: step-2 writer must exist before step 3 builds.
- Not-proven boundaries: the scheduler is unbuilt; the real over-time series has not run; series-diff (Element 3) unbuilt.

## Current Task State

- Completed (merged on `origin/main 739411f`): hardening (#113), pilot spec (#108), distill A1c (#107).
- Partially completed: step 2 (writer) handed off (#114, OPEN) — not yet built; step 3 (this scheduler) not started.
- Broken or uncertain: none known.

## Workspace State

- Branch: receiver creates a fresh worktree/branch off `origin/main`.
- Head: `origin/main 739411f` at handoff (moves; re-fetch).
- Dirty/untracked before handoff: home tree carries unrelated untracked files; do not work there.
- Dirty/untracked after writing this handoff file: + this file (untracked under `docs/prompts/handoffs/` until committed on its lane).
- Target files: a new runner/scheduler under `orca-harness/runners/` + a test; reuses `cadence.py` + the step-2 writer.
- Related worktrees/branches: step-2 handoff branch `handoff-durability-series-writer-step2-v0` (PR #114); merged hardening/pilot/distill lanes are prunable.

## Changed / Inspected / Tested Files

- `orca-harness/source_capture/cadence.py`
  - Status: exists (read-only input).
  - Role: `CadencePlan` + `build_cadence_plan` + `to_dict()` — the cadence the scheduler executes.
- (to-build) `orca-harness/runners/run_source_capture_durability_series_*.py` — the scheduler/runner (name + shape per the Open Decision).

## Frozen Decisions

- Bounded build authorization for steps 2+3 only (owner, 2026-06-15). Consequence: build without re-asking, within the bounds; nothing broader.
- Series-diff Element 3 deferred. Consequence: no change-detection in step 3.
- Commissioned capture only (Ob.1) + INV-1. Consequence: bounded series, facts-not-verdicts.

## Mutable Questions

- Scheduling mechanism (A/B/C) — see Open Decision.
- First commissioned SKU/source set + Decision Frame — owner input.
- When to build series-diff (Element 3) — after enough observations accrue; separate lane.

## Superseded / Dangerous-To-Reuse Context

- **"Scopes, does not authorize" (the default handoff posture)** — superseded for steps 2+3 by the owner's bounded Build Authorization above. The receiver does NOT re-request authorization for the step-2/step-3 builds (but still does not merge to main).
- **Pilot's two-observations-minutes-apart** — that was a machinery proof, NOT a real series; step 3 runs the actual over-time cadence. Do not treat the pilot's single window as the series.

## Commands And Verification Evidence

- Confirm step-2 writer landed + schema present:
  ```bash
  git fetch origin main && git log --oneline origin/main | grep -i "durability-series writer\|durability.*writer"
  git show origin/main:orca-harness/source_capture/models.py | grep -E "intended_cadence"
  ```
  Result at handoff: step-2 writer NOT yet built (#114 handoff OPEN); `intended_cadence` present. Re-run target: the receiver confirms the writer exists before building.
- Full offline suite (the green gate after building):
  ```bash
  cd orca-harness && .venv/Scripts/python.exe -m pytest -q
  ```
  Baseline at handoff: 861 passed, 2 skipped.

## Blockers And Risks

- Blocker: **step-2 writer must land first** (step 3 invokes it). Likely next action: confirm step 2 built before starting step 3.
- Risk: a scheduled task (Open Decision B) drifting toward standing capture. Mitigation: bound to the commissioned series' `slot_count`; retire when the series completes.

## Confirm-Don't-Trust Load Checklist

- Re-verify before acting: (1) step-2 writer exists on `origin/main`; (2) `cadence.py` + `models.py intended_cadence` present; (3) `origin/main` HEAD (≥ `739411f`); (4) the bounded Build Authorization above still reflects owner intent.
- Load outcomes: `REUSE` after all re-verify; `STALE_REREAD_REQUIRED` if `origin/main` moved (expected); `BLOCKED_DRIFT` if step-2 writer is absent (then step 3's dependency is unmet — stop).
- Reread on drift: the step-2 writer, `cadence.py`, the pilot spec §3, obligation contract Ob.1/Ob.17.

## Do Not Forget

- **Step 3 depends on step 2** — confirm the writer landed before building.
- **Commissioned, bounded series — not a standing crawler.** Gap ≠ no-change.
- Build authorization is **bounded to steps 2+3**; landing to main stays owner-gated; series-diff Element 3 deferred.
