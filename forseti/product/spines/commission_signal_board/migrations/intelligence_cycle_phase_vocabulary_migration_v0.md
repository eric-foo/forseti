# Intelligence Cycle Phase Vocabulary Migration v0 — 2026-08-05

```yaml
retrieval_header_version: 1
artifact_role: Spine migration note (vocabulary mapping)
scope: >
  Preserves the 2026-08-05 phase/turn mapping and points to the current
  Gathering, Consolidation and Delivery identity, so historical seals,
  handoffs and run records remain interpretable without rewriting them.
use_when:
  - Reading a historical seal, handoff, or run record that uses Problem Framing or Deliver-as-turn vocabulary.
  - Verifying which vocabulary a cycle artifact was authored under.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - forseti/product/spines/commission_signal_board/spine.yaml
stale_if:
  - The cycle's phase or turn vocabulary changes again.
```

Owner-directed change (Deliver planning lane, 2026-08-05). Docs-only: the CSB
output validator and the phase-acquisition-seal runner enforce neither the
phase enum nor the turn name, so no executable surface changed.

## Mapping

The current public phases, adopted **2026-09-29**, are **Gathering →
Consolidation → Delivery**. Their meanings and the retained profile/turn
identifiers are owned by the
[operating authority](../authority/forseti_commission_signal_board_prompt_structure_rules_v0.md#forseti-intelligence-cycle-operating-contract).
The table below records the earlier migration; it is not the current phase list.

| Historical vocabulary | Vocabulary adopted 2026-08-05 |
| --- | --- |
| Phase `problem_framing` / "Problem Framing" | Phase `deliver` / "Deliver" |
| Informal phase shorthand "Problem" | Phase `deliver` |
| Turn `deliver` / "Turn B — Deliver" | Turn `synthesize` / "Turn B — Synthesize" |
| "Phase A" (historical) | Understanding phase, Acquire & Seal turn |
| Seal state `SEALED_READY_FOR_DELIVER`, field `deliver_allowed` | Unchanged stable spellings; read as "ready for the Deliver phase / synthesis" |

Problem framing did not disappear: it is the Deliver phase's first synthesis
step (decision frame and target screen) in the Deliver decision-memorandum
method.

## Boundaries

- Historical artifacts are never rewritten to the new vocabulary; changing
  them would falsify provenance. `phase: understanding` in existing seals
  remains valid; a historical `phase: problem_framing` value, if ever
  encountered, reads as `deliver`.
- New commissions use Gathering, Consolidation and Delivery for their public
  phase identity. Existing schema fields keep their compatibility spellings
  under the operating authority; this does not rewrite historical artifacts.
