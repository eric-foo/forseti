# Orca Commission Signal Board Prompt Adjudication Packet v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact (decision-prep / correction packet)
scope: >
  Recasts the temporary backtesting-first Orca commission prompt as a signal
  and evidence board candidate, not a gate, demand check, proof step, or
  classifier. Maps prompt sections to the corrected commission boundary before
  any durable prompt or implementation work.
use_when:
  - Deciding whether to turn the temporary commission prompt into an Orca durable signal-board prompt.
  - Checking which prompt sections are adopted, modified, deferred, or rejected under the evidence/signals-only boundary.
  - Preparing owner sign-off on commission signal-board naming, source-routing, and classifier handoff.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/product/product_lead/orca_demand_scan_gate_adjudication_packet_v0.md
  - docs/product/product_lead/orca_demand_gate_run_commission_criteria_v0.md
  - docs/product/product_lead/orca_buyer_proof_packet_v0.md
stale_if:
  - The owner chooses a different durable name for the commission signal/evidence object.
  - A durable commission signal-board prompt is authored through prompt-orchestration.
  - A demand-classifier handoff contract supersedes this evidence/signals-only boundary.
```

## Start Preflight

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S2 product anchor plus target prompt, adjacent classifier/proof context, and historical gate-named artifacts
  edit_permission: docs-write
  target_scope: product-lead decision-prep artifact; no prompt artifact, no implementation, no runtime authorization
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md, overlay README, source-loading, prompt-orchestration, buyer-proof packet, adjacent demand/gate context artifacts, temporary prompt
```

## Decision Question

Should the temporary file
`C:/Users/vmon7/AppData/Local/Temp/orca_commission_gate_prompt (1).md`
become a durable Level 1 commission prompt, be rewritten through Orca prompt
orchestration, or be deferred?

## Owner Correction

The commission object should not be a **gate**.

The commission object should be a **signal board**: a structured evidence and
signal surface that organizes what is known, where it came from, how strong or
weak the signal coverage is, what contradicts it, and what remains missing.

It should not decide whether demand exists. The demand-classification layer owns
the demand check. Commission should prepare clean evidence and signal inputs for
that layer, not pre-judge them.

This means the commission output should be a board or packet of signals, not an
`admit` / `hold` / `fail` verdict.

## Adjudication

Do **not** install the temporary prompt as-is.

Use it as a strong decision-prep draft for a future signal-board prompt, but
strip out the gate semantics. The valuable parts are source routing, mode/cutoff
discipline, provenance discipline, creator/non-creator separation, redirect
rules, and output shape. The wrong parts are any demand decision, pass/fail
gate, proof claim, or classifier-like judgment.

The recommended direction is:

- Adopt **Commission Signal Board** as the working object name unless the owner
  picks a better noun.
- Commission owns evidence and signals only: collect, route, tag, compare,
  preserve provenance, expose conflicts, and name gaps.
- The demand classifier owns demand judgment.
- Buyer-proof and client-facing claims remain downstream and separately gated.
- Durable prompt authoring still goes through prompt-orchestration.

The temporary prompt is too high-lock-in to adopt wholesale because it mixes
five different objects in one artifact: commission intake, venue playbook,
source registry, forecast-target schema, and graph retrieval schema. Installing
that bundle as authority would silently decide product, Judgment, Data Capture,
and prompt-packaging questions that are not all settled.

## Current Source State

The controlling product thesis says Orca is outside-in consumer-demand decision
intelligence for distinguishing durable demand from transient or manufactured
demand; beauty/personal-care is the first vertical and the engine remains
vertical-portable (`docs/decisions/orca_product_thesis_consumer_demand_v0.md`).

The offer hypothesis narrows the first proof offer to US-market indie/DTC beauty
or personal-care operators facing live 30-90 day consumer-demand allocation
decisions, while preserving Orca's broader offer boundary
(`docs/product/product_lead/orca_offer_hypothesis_v0.md`).

The buyer-proof packet binds proof requirements, not commission-board behavior.
For this commission layer, those requirements are downstream context: they say
why clean signal provenance matters, but they do not turn commission into a
proof or demand-decision surface
(`docs/product/product_lead/orca_buyer_proof_packet_v0.md`).

The current gate-run criteria and demand-scan adjudication packet are adjacent
historical/context artifacts. Under this correction, their gate language should
not be copied into the commission object. Any future durable prompt should
separate signal-board generation from demand classification
(`docs/product/product_lead/orca_demand_gate_run_commission_criteria_v0.md`,
`docs/product/product_lead/orca_demand_scan_gate_adjudication_packet_v0.md`).

Prompt policy requires any durable Orca prompt to be authored through
prompt-orchestration or to apply that contract in full. The temporary prompt is
not yet a durable prompt artifact.

Fresh exact-term search in this worktree found no durable hits for the temporary
prompt's schema names: `commission_gate_brief`, `future_information_policy`,
`graph_family_plan`, `forecast_targets_for_downstream`, `backtesting-first`, or
`evidence_cutoff_at`. Existing code provides lower-level capture/provenance,
cutoff posture, projections, graph-frontier patterns, and action-band Judgment
scoring, but not a commission signal-board schema, runner, or output contract.

## Section Adjudication Matrix

| Prompt section | Decision | Rationale | Owner / next handling |
| --- | --- | --- | --- |
| 3. Required mode contract | Adopt with modification | The `backtest` cutoff and future-information exclusion are directionally right and align with zero-spoiler backtest doctrine. For a board, the mode controls evidence admissibility and chronology, not verdict authority. | Carry into future prompt as required evidence preflight; client-facing mode stays deferred. |
| 4. Intake schema | Modify | The schema is useful, but it should become a signal-board brief: candidate, decision context, time window, source families, known unknowns, and evidence constraints. It should not decide buyer proof or demand. | Rewrite through prompt-orchestration if owner accepts the direction. |
| 5. Gate decision / allocation | Reject gate decision; keep allocation as collection guidance | The 70/20/10 allocation is useful search hygiene, not a gate rule. Commission can allocate evidence effort; it cannot pass or fail demand. | Rename this section in any future prompt to signal-collection allocation. |
| 6. Decision-type playbooks | Adopt as signal-route cards | The playbooks are useful venue-routing cards for fragrance/beauty cases, but they are not proof doctrine or demand-classifier logic. | Keep as route cards that identify likely signal families. |
| 7. Source registry | Adopt with guardrails | The public/repeatable/provenance admission rule fits Orca's public-first posture and Data Capture source-family discipline. | Bind each source family to capture/provenance fields before any implementation. |
| 8. Creator routing | Adopt with guardrails | Manual creator routing is acceptable for v1 and the non-creator confirmation guardrail is important. Creator evidence should be tagged by origin and relation to non-creator signals, not treated as demand proof. | Use as source routing; no algorithmic routing now. |
| 9. Outcome labels | Defer as downstream vocabulary | The labels are valuable for forecast/evaluation design, but the signal board should prepare evidence for downstream evaluation, not score outcomes. | Owner decides whether these labels become a downstream forecast-target registry. |
| 10. Graph-family retrieval plan | Defer as implementation/schema; keep as optional relation map | The graph vocabulary is useful for showing source relationships, duplication, propagation, and conflict. It is not backed by a commission-domain graph schema or runner. | Keep as prompt output ask only; runtime schema requires separate authorization. |
| 11. Redirect and stop rules | Adopt with modification | The rules correctly prevent tunnel vision, weak provenance, campaign-cluster false positives, and unavailable private-data chases. For a board, they control evidence collection quality, not demand outcome. | Carry into future prompt as signal-collection control policy. |
| 12. Required gate output | Replace | The output should be a signal board: source-family coverage, signal units, provenance, chronology/cutoff posture, origin/de-duplication notes, conflicts, gaps, and classifier handoff notes. It should not output `admit`, `hold`, or `fail`. | Future prompt output contract after owner approval. |
| 13. Standalone sufficiency | Accept only as evidence/signal collection sufficiency | The prompt may be standalone enough to generate a first-pass signal board, but not enough for demand classification, buyer proof, runtime implementation, or client-facing use. | Keep the boundary explicit. |

## Owner Decisions Needed

1. Ratify or replace the working name **Commission Signal Board**.
2. Decide the minimum board fields for handoff to the demand classifier:
   source-family coverage, signal units, provenance, chronology, conflicts,
   gaps, and handoff notes are the recommended minimum.
3. Decide whether the temporary prompt's fragrance-specific playbooks are the
   first signal-board satellite or only an example deck for a broader beauty
   signal board.
4. Authorize a durable signal-board prompt artifact through
   prompt-orchestration, or explicitly defer prompt authoring.

## Recommended Owner Sign-Off Option

Recommended: **adopt-as-modified direction under the name Commission Signal
Board, do not adopt-as-is**.

This preserves the valuable parts of the prompt while avoiding four failure
modes:

- calling commission a gate;
- turning signal collection into demand judgment;
- turning search quotas or playbooks into proof rules;
- creating a graph/forecast/runtime contract before the owning lanes accept it.

If the owner accepts this option, the next authorized step is a
prompt-orchestrated durable signal-board prompt that references this packet and
the current classifier/proof boundaries. If the owner does not accept it, no
prompt artifact or implementation should be created from the temp file.

## Non-Claims

- Not owner ratification.
- Not a prompt artifact.
- Not a gate.
- Not a demand classifier.
- Not buyer proof.
- Not validation or readiness.
- Not a scoring engine.
- Not implementation authorization.
- Not authorization to run a scan, capture sources, contact buyers, or produce a client-facing artifact.
