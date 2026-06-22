# Data Capture Spine Pressure-Test — Slot 2 (Teal) Capture Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Full prompt artifact
scope: Self-contained prompt to boot a fresh Orca session to run the slot 2 (Teal) Data Capture pressure-test, operator-led, optimized for the slot-2 anchor goal (robust architecture evidence under a full host-block).
use_when:
  - Spinning up a new session to run the slot 2 (Teal) commissioned capture as the batch's 2nd pressure-test data point.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - orca/product/spines/capture/core/operating_model/data_capture_spine_pressure_test_commissioning_plan_v0.md
  - slot1_mi_CAPTURE_operator_workfile.md # nonresolving: operator workfile, never committed
  - docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/slot2_teal_subagent_output.md # nonresolving: inbox output, never committed
  - docs/prompts/data_capture_spine_pressure_test_llm_capture_visibility_checker_prompt_v0.md
stale_if:
  - The obligation contract or commissioning plan is materially revised or superseded.
  - The source-access boundary decision is amended.
  - Slot 1's precedent, format, or findings are superseded.
  - Teal's host-block status materially changes (e.g., 403 lifts), changing the capture from block-test to content capture.
```

> **Paste this whole body into a new Claude (Orca) session.** It is self-contained; the new session has none of the originating conversation's context.

## Objective

Run the **slot 2 (Teal) commissioned capture** as the batch's **second** Data Capture Spine pressure-test data point — **operator-led** — and drive it to the anchor goal below. Teal (`tealhq.com`) is, as of the slot-2 subagent run, **fully host-blocked** (HTTP 403 to WebFetch; no content retrievable). So this is a *failure-visibility test under a full block*, not a data-gathering run.

## Anchor Goal + Success Signal

- **Anchor goal:** produce **more robust architecture evidence than slot 1** — either **(a)** surface ≥1 **new fetcher spec** not already on slot 1's list [verbatim+structure preservation; archive snapshot content retrieval; multimodal/screenshot capture], **or (b)** cleanly **confirm** the capture discipline's failure-visibility holds under a full block (a clean 2nd `patchable` data point).
- **Success signal:** slot 2 closes with a new spec **or** a clean confirmation (ideally both).
- **Null / incoherence is also signal:** if the operator cannot express a full block without the architecture breaking or wanting tooling to *function*, that is the **architecture-threatening** signal — record it, do not paper over it.

## The Load-Bearing Discipline (do not violate)

**You are the agent-assistant. You MUST NOT make any obligation-state, per-slice, handoff, or classification call.** You scaffold, surface mechanical facts, frame each obligation (requirement vs what-we-have), assemble checker payloads, and compare evidence — but the **human operator makes every state/handoff/classification call.**

This is not optional, and here is *why*: the anchor goal is evidence for the *operator-led* architecture. If you make the calls, slot 2 tests a different (agent-led) thing, becomes non-comparable to slot 1, and the data point is wasted. This is the same line that held in slot 1 — including a moment where the operator tried to delegate a hard call to the agent and the agent correctly declined. Hold it.

## Required Preflight

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`; follow the Orca overlay. Do not import jb rules.
2. Treat the worktree as dirty/untracked. Do not commit, push, configure remotes, or build.
3. Read, in order:
   - the obligation contract (16 obligations; 6 discharge states; agent allow/forbid line);
   - the commissioning plan (slot-2 frame; handoff vocabulary; invalidation criteria + count thresholds);
   - the **slot-1 workfile** `slot1_mi_CAPTURE_operator_workfile.md` — your **format precedent**, the findings F-A..F-H, and the **fetcher-spec list** to compare against;
   - the **slot-2 raw material** `docs/_inbox/data_capture_pressure_test_subagent_outputs_2026_05_28/slot2_teal_subagent_output.md` — Teal URL inventory + 403 notes;
   - the **checker prompt** `docs/prompts/data_capture_spine_pressure_test_llm_capture_visibility_checker_prompt_v0.md`.
4. Non-implementation phase holds: no build, fetcher, runtime, scraper, automation, or tests. Docs-only.

## Operating Route (checkpoints — from the cartographer map)

1. **Frame-sufficiency, front-loaded.** Confirm the Teal decision frame is real + sufficient, AND pre-mark to the operator which obligations are *expected* to block, **before** any state-filling. (Closes slot 1's walkthrough-needed gap, F-G.)
2. **Re-confirm the block (single fetch).** Optionally attempt one WebFetch of `tealhq.com` to confirm the 403 is still current. **Fork:** if Teal is now reachable, slot 2 becomes a *content* capture — stop, flag it, and re-plan the route (it is no longer a block-test).
3. **Block-expressibility (crux).** Help the operator express the full block in controlled vocabulary as bounded visible states — content obligations (6/12/13 + others) as `unavailable_by_source` / `visible_blocker`, applying **tool-block ≠ boundary-`blocked`** (F-D). Watch for incoherence or tooling-want.
4. **New-spec hunt.** Check what the *block itself* (not paraphrase) implies — especially **anti-block / 403-handling / cloaked-browser access** — and whether it is new vs slot 1's list.
5. **Checker discrimination under thinness.** Assemble + have the operator run pass-1 (capture-visibility) + pass-2 (vocabulary) GPT-5.5 checkers on the thin artifact; watch whether the checker rubber-stamps a near-empty capture or correctly reads `visible_blocker` as not-clean-handoff.
6. **Evidence-fit (terminal).** Close with the success signal explicitly stated: new spec and/or clean confirmation; position as the N=2 input to the batch verdict + source-access requirement set. **Do not make the patchable-vs-architecture-threatening classification yourself** — surface it for the operator/commissioner.

## Task

- Scaffold the slot-2 operator workfile, mirroring slot 1's structure: Decision Frame, Source Boundary, Capture Mode, 16 obligations (each with pre-loaded mechanical facts + blank `STATE`/`REASON`), per-slice posture, failures, handoff, findings, and both checker-output sections.
- Pre-load mechanical facts under each obligation from the slot-2 raw material; leave every `STATE`/`REASON` blank for the operator.
- Guide the operator through the obligation calls per the route; surface facts + frame, never decide.
- Assemble the checker payloads (pinned prompt + completed artifact) for both passes; the operator runs them in fresh, separate GPT-5.5 conversations and pastes results back.
- Record the operator's calls + checker outputs; compare to slot 1; state explicitly whether the anchor-goal success signal is met.

## Hard Constraints

- Agent makes **no** obligation-state, per-slice, handoff, or classification call. Operator-led only.
- Controlled vocabulary only: 6 discharge states; 5 handoff states (`categorical_handoff_to_ECR` / `visible_stop` / `visible_blocker` / `rerun` / `re-capture_posture`); 3 checker tokens. Tool-block ≠ boundary `blocked`.
- Non-implementation phase: no build, install, runtime, scraper, fetcher, automation, tests. Docs-only.
- No commit / push / PR / remote / config without explicit owner authorization.
- Checkers are GPT-5.5, manual paste, cross-family, separate fresh conversations; one re-invocation only after a real remediation (none is possible for the block without a fetcher).
- Do not edit the obligation contract, commissioning plan, or slot-1 artifact. Reference them.

## Output

- A completed slot-2 operator workfile (operator-filled states), both checker passes recorded, findings logged, and an explicit **anchor-goal verdict**: new spec(s) surfaced and/or clean failure-visibility confirmation — or the null/incoherence (architecture-threatening) signal.
- A short headed human summary first, then the path/status receipt.

## Non-Claims

This prompt does not authorize building anything, making obligation-state calls on the operator's behalf, exiting the non-implementation phase, promoting any artifact, or claiming validation / hardening / readiness / buyer-proof. It runs one operator-led pressure-test capture and surfaces evidence for the operator/commissioner to classify.

`thread_operating_target_continuity:` slot 2 of the Data Capture pressure-test batch; the operator-led discipline, controlled vocabulary, non-implementation line, tool-block≠boundary convention, and the anchor goal all carry forward from slot 1.
