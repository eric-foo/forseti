# Capture Spine — Knowledge De-Fork Commission — Thin Wrapper v0

```yaml
retrieval_header_version: 1
artifact_role: Thin wrapper (courier for a cross-lane commission prompt)
scope: Route the Capture Spine CA to run the knowledge de-fork + equipment-kit + consult-enforcement-design commission.
use_when:
  - Dispatching the capture-knowledge de-fork commission to the Capture Spine CA in a fresh lane/thread.
authority_boundary: retrieval_only
```

## Wrapper

- **Full prompt:** `docs/prompts/handoffs/capture_spine_knowledge_defork_equip_kit_enforcement_commission_prompt_v0.md`
- **Prompt revision:** blob `19534abc7469924c2993c1a97e0819784c8effb3` @ commit `504fa82`, branch `capture-knowledge-defork-commission-v0` (off `origin/main` `ea2c79b`).
- **Receiver:** Capture Spine CA, in its own lane/thread. De-correlation is **not** required (this is design + doc-sync, not a review).
- **Workspace:** a fresh worktree off `origin/main`; clean base required; land via the per-lane PR flow (owner CLI-merges).
- **Target scope:** capture-lane surfaces (`capture_recon_index_v0.md`, `source_capture_playbook_v0.md`, Armory `README.md`) + new Capture Equipment Kit + new map/design notes. The Walker Kit (`orca_vertical_exploration_guide_v0.md`) is **discovery-lane-owned** → coordinate or deliver a proposed pointer only.
- **Output mode / edit permission:** `file-write`, design/findings-first; `docs-write` on capture-lane surfaces, propose-only cross-lane.

## Run delta

Execute the full prompt's commission D1–D4: (D1) knowledge-surface map — one canonical home per lesson, de-fork the Armory ladder to a pointer, make sync structural; (D2) Capture Equipment Kit mirroring the Walker Kit; (D3) consult-enforcement **design** only — equip-at-spawn + advisory fail-open hook + post-run two-axis verdict, each with its foregone limitation (**no hook build**); (D4) evaluate agent profiles (consider, not mandate). No capture run; no merge to main; closeout carries a `direction_change_propagation` receipt.
