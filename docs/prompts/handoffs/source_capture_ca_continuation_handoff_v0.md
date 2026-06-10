# Source Capture CA Continuation Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Handoff prompt
scope: Cold-reader handoff for continuing Source Capture / Data Capture CA activity outside the Source Capture Armory rename lane.
use_when:
  - Starting a fresh CA lane after the Source Capture source-quality lifecycle work.
  - Re-establishing the Source Capture / Data Capture anchor goal and success signals without using thread memory.
  - Avoiding collision with the separate Source Capture Armory naming lane.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - docs/product/source_capture_toolbox/README.md
  - docs/product/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md
  - docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md
stale_if:
  - The Source Capture Armory display-name rename, lifecycle decision, Mini God-Tier profile, Slot 3 closeout, or source-loading rules change materially.
  - The receiving lane is asked to perform the Source Capture Armory rename instead of CA continuation.
```

## Load Contract

- packet_version: `handoff_v0`
- mode: `max`
- created_at: `2026-06-04T03:35:17+08:00`
- created_by_lane: current Codex Source Capture rename/setup lane; provenance only
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- handoff_path: `docs/prompts/handoffs/source_capture_ca_continuation_handoff_v0.md`
- expected_branch: `main`
- expected_head: `aa17aed`
- expected_dirty_state_including_handoff_file: broad dirty state existed before this handoff; Source Capture Armory rename files and this handoff file are dirty/untracked in the working tree. Receiver must rerun `git status --short --branch` before acting.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against current source before acting. This packet is orientation, not authority.

## Goal Handoff

- long_term_goal: Build Orca's Data Capture / Source Capture foundation so bounded source units can be captured, preserved, inspected, and handed forward with Mini God-Tier source-quality discipline before Judgment, Cleaning, ECR, buyer-proof, or commercial-readiness claims.
- anchor_goal: Continue CA activity from the accepted Source Capture lifecycle/source-quality foundation without colliding with the separate Source Capture Armory naming lane. The next CA should decide the next bounded checkpoint only after reloading the current Source Capture Armory product docs, lifecycle decision, and Slot 3 closeout from the repo.
- success_signal: The next CA can answer, from source-loaded documents rather than thread memory, whether a proposed next checkpoint preserves all six lifecycle-use signals:
  1. Lifecycle boundary is source-loadable.
  2. One known source-quality surface is selected.
  3. Each cited packet/source row answers lifecycle questions.
  4. Retention and sensitivity notes travel with packet citations.
  5. Mini God-Tier tokens remain source-quality posture only.
  6. Fresh-agent readability is preserved.

## Open Decision / Fork

- decision: What is the next CA checkpoint after Slot 3 source-quality closeout and packet lifecycle handling?
  - options:
    - Continue source-quality passes over another bounded source unit.
    - Scope the next source-access adapter or source-quality helper only if source-loaded evidence shows a repeated friction.
    - Defer new build activity and consolidate lifecycle/retrieval evidence.
  - already constrained / off the table:
    - Do not perform additional Source Capture Armory rename work in this lane; the display-name patch is isolated in the current rename lane and must be reverified from source if relied on.
    - Do not use this packet as validation, readiness, fixture admission, Judgment evidence, buyer proof, or source-completeness proof.
    - Do not authorize Reddit API, commercial fetch, anti-detect, proxy, production runtime, storage, ECR, Cleaning, or Judgment behavior without a separate current authorization.
  - trade-offs:
    - More source-quality passes improve evidence reuse but can create scratch-output sprawl if lifecycle handling is not explicit.
    - Helper or adapter expansion may reduce future friction but should follow repeated observed friction, not speculative completeness.
  - owner of the call: Orca owner / current user.
  - recommendation: Start with source-loading and a bounded next-checkpoint recommendation, not implementation. Escalate to implementation only if the current user or an accepted handoff explicitly authorizes a narrow build scope.

## Drift Guard

- invariant, non-goal, or scope boundary: Source Capture Armory rename is separate.
  - why it matters: The rename is a product-doctrine/output-authority propagation pass; mixing it with CA continuation would make dirty-state and doctrine receipts ambiguous.
  - what violating it would break: Handoff clarity, DCP receipt auditability, and source-loaded navigation.
- invariant, non-goal, or scope boundary: Mini God-Tier source-quality tokens are posture, not proof.
  - why it matters: The source-quality profile and Slot 3 closeout intentionally preserve visible limitations.
  - what violating it would break: Fixture admission, validation, Judgment-quality, and buyer-proof boundaries.
- invariant, non-goal, or scope boundary: Generated Source Capture Packets remain scratch unless separately admitted.
  - why it matters: The lifecycle decision controls citation, retention, sensitivity, and admission gates.
  - what violating it would break: Retention/sensitivity discipline and future fixture-admission integrity.

## Inherited Context

### Source-loading state to re-establish

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`.
- targets to enter the ladder:
  - `AGENTS.md`
  - `.agents/workflow-overlay/README.md`
  - `.agents/workflow-overlay/source-of-truth.md`
  - `.agents/workflow-overlay/source-loading.md`
  - `docs/product/source_capture_toolbox/README.md`
  - `docs/product/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md`
  - `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`
- already loaded by sender (weak orientation only): the files above plus `docs/product/source_capture_toolbox/README.md` and the Slot 3 closeout.
- must load first before strict or actionable steps: `AGENTS.md`, overlay README, source-of-truth, source-loading, and the specific Source Capture artifact the CA decision depends on.
- load rule: receiver re-runs progressive source loading per overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors

- decision or convention: Bounded implementation is allowed only when the current turn or accepted handoff explicitly authorizes a named implementation scope.
  - decided in: `AGENTS.md` and `.agents/workflow-overlay/source-loading.md`
  - compare target: reread-required
  - verify before: any implementation, test, runtime, adapter, or generated-output action.
- decision or convention: Source Capture Packet lifecycle defaults to scratch; durable closeouts may cite recorded packet facts without admitting fixtures.
  - decided in: `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`
  - compare target: reread-required
  - verify before: citing packets, retaining packets, or treating packet outputs as candidate evidence or fixtures.
- decision or convention: Slot 3 post-recapture source-quality closeout records three `mini_god_tier_with_visible_limitations` rows and no validation/source-completeness/Judgment claim.
  - decided in: `docs/product/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md`
  - compare target: reread-required
  - verify before: using Slot 3 as source-quality context.

## Active Objective

Continue CA-level Source Capture / Data Capture planning from the current lifecycle/source-quality foundation, with a fresh source-loaded decision about the next bounded checkpoint. Do not perform additional rename work in the CA lane.

## Exact Next Authorized Action

1. Run Orca start preflight in the receiving lane: read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Source-load the Source Capture CA read pack named in this handoff.
3. Re-derive the current anchor goal and success signals from source.
4. Recommend the next bounded checkpoint, including non-goals and stop conditions.
5. Do not implement unless the current user gives explicit bounded implementation authorization.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md`
    - Role: top-level Orca agent instruction.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-06-04.
    - Reuse rule: reread before action.
- Overlay authority:
  - `.agents/workflow-overlay/README.md`
    - Role: overlay entrypoint.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-06-04.
    - Reuse rule: reread before action.
  - `.agents/workflow-overlay/source-loading.md`
    - Role: source-loading and read-pack rule.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-06-04.
    - Reuse rule: reread before any source-loaded claim.
- Product and decision sources:
  - `docs/product/source_capture_toolbox/README.md`
    - Role: product-facing Source Capture Armory entrypoint at the historical `source_capture_toolbox` path.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-06-04.
    - Reuse rule: reread; do not rely on old display name after rename lane lands.
  - `docs/product/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md`
    - Role: Slot 3 source-quality closeout and six lifecycle-use success signals.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-06-04.
    - Reuse rule: reread before using Slot 3 closeout.
  - `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`
    - Role: lifecycle, retention, citation, and sensitivity boundary for Source Capture Packets.
    - Load-bearing: yes.
    - Compare target: reread-required.
    - Last checked: 2026-06-04.
    - Reuse rule: reread before citing or retaining packet facts.
- Source gaps:
  - Exact whole-worktree dirty state is broad and must be remeasured by receiver.
  - The Source Capture Armory rename lane may change display names after this packet.
- Strict-only blockers:
  - Missing source-loading readback blocks strict CA recommendations.
  - Any implementation/action request requires current-turn or accepted-handoff authorization.
- Not-proven boundaries:
  - validation, readiness, fixture admission, source completeness, Judgment quality, buyer proof, production readiness, and source-access boundary amendment.

## Current Task State

- Completed:
  - Source Capture packet lifecycle boundary committed at observed HEAD `aa17aed`.
  - Slot 3 source-quality closeout exists as an untracked product artifact in the current working tree and records the six lifecycle-use success signals.
  - Current lane has been reassigned to Source Capture Armory naming.
- Partially completed:
  - Source Capture Armory naming propagation discovery and display-name patch are in the current working tree; receiver must reverify before relying on it.
- Broken or uncertain:
  - Broad dirty state exists across Orca; receiver must recheck current status and not stage or revert unrelated work.

## Workspace State

- Branch: `main`
- Head: `aa17aed`
- Dirty or untracked state before handoff: broad dirty state; receiver must rerun `git status --short --branch`.
- Dirty or untracked state after writing handoff file and rename patch: this file is untracked under `docs/prompts/handoffs/`; Source Capture Armory display-name surfaces are modified in the working tree.
- Target files or artifacts:
  - `docs/product/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md`
  - `docs/decisions/source_capture_packet_fixture_retention_sensitivity_decision_v0.md`
  - `docs/product/source_capture_toolbox/README.md`
- Related worktrees or branches: none supplied.

## Changed / Inspected / Tested Files

- `docs/product/source_capture_toolbox/source_quality_slot3_post_recapture_closeout_v0.md`
  - Status: untracked in current workspace.
  - Role: Slot 3 source-quality closeout; CA receiver should reread before use.
  - Important observations: contains six lifecycle-use success signals and strict non-claims.
- `orca-harness/source_capture/source_quality.py`
  - Status: modified in current workspace.
  - Role: report-skeleton helper touched by the source-quality closeout lane.
  - Important observations: CA receiver should not act on implementation state without current authorization.
- `orca-harness/tests/unit/test_source_quality_report_skeleton.py`
  - Status: modified in current workspace.
  - Role: helper regression tests.
  - Important observations: tests are not CA authority.

## Frozen Decisions

- Decision: Source Capture Armory rename is isolated in the current lane.
  - Evidence: current user instruction on 2026-06-04.
  - Consequence: receiving CA lane should not patch naming surfaces unless separately redirected.
- Decision: Mini God-Tier source quality is the target posture discipline, not a proof claim.
  - Evidence: Source Capture Mini God-Tier profile and Slot 3 closeout.
  - Consequence: preserve visible limitations and non-claims.

## Mutable Questions

- Question: What is the next CA checkpoint after Slot 3 closeout?
  - Why still mutable: the receiver must re-source-load current docs and account for any rename or dirty-state drift.
  - What would resolve it: a fresh CA recommendation tied to source-loaded artifacts.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: Treating “toolkit” and “Source Capture Toolbox” as the same rename target.
  - Why stale or dangerous: Judgment has separate “toolkit” surfaces that should not be renamed in the Source Capture display-name pass.
  - Current replacement: Source Capture display name is being harmonized to Source Capture Armory; Judgment toolkit surfaces stay out of scope unless explicitly authorized.
- Stale instruction, idea, artifact, or finding: Treating scratch Source Capture Packets as admitted fixtures.
  - Why stale or dangerous: violates lifecycle/retention/sensitivity decision.
  - Current replacement: use durable closeouts for recorded facts; separate decision needed for fixture admission.

## Commands And Verification Evidence

- Command:
  ```powershell
  git rev-parse --short HEAD
  ```
  Result:
  - Observed output: `aa17aed`
  - Re-run target: receiver should rerun before acting.
- Command:
  ```powershell
  git status --short --branch
  ```
  Result:
  - Observed: branch `main...origin/main [ahead 2]` with broad dirty/untracked state.
  - Re-run target: receiver should rerun; do not rely on the sender's broad status summary for exact staging decisions.

## Blockers And Risks

- Blocker or risk: Receiver may treat this packet as source authority.
  - Evidence: handoff packets are weak source class under workflow-handoff.
  - Likely next action: rerun source loading and verify all load-bearing claims.
- Blocker or risk: Rename lane changed display names from Toolbox to Armory in the working tree.
  - Evidence: current user instruction and current rename patch.
  - Likely next action: receiver should rely only on current source-loaded names after reading current repo state.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - branch and HEAD;
  - broad dirty/untracked state;
  - source-loading policy;
  - Source Capture Armory README current display name and entrypoint;
  - lifecycle/retention/sensitivity decision;
  - Slot 3 closeout six success signals;
  - any current implementation authorization.
- Compare target for each: rerun relevant reads/commands in the current workspace.
- Load outcomes and what each means:
  - `REUSE`: all source docs and state reverified; continue from exact next authorized action.
  - `PARTIAL_REUSE`: only display-name or non-load-bearing details drifted; rederive and continue.
  - `STALE_REREAD_REQUIRED`: Source Capture docs or dirty state changed materially; reread before deciding.
  - `BLOCKED_DRIFT`: drift conflicts with user constraints, source authority, or target lane.
  - `BLOCKED_UNVERIFIABLE`: load-bearing claim cannot be re-derived.
- Sources that must be reread if drift is detected: `AGENTS.md`, overlay README, source-of-truth, source-loading, Source Capture README, Slot 3 closeout, lifecycle decision.

## Do Not Forget

The receiving lane continues CA activity. Additional Source Capture Armory rename work belongs to the current rename lane unless the owner explicitly reassigns it.
