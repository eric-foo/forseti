# Judgment Spine

```yaml
retrieval_header_version: 1
artifact_role: Spine front-door
scope: Retrieval-only entry point for the legacy Judgment spine product corpus.
use_when:
  - Starting Judgment spine work from the Forseti route map.
  - Routing a judgment-quality, claim-ladder, demand-read, or gate-ownership question.
  - Distinguishing product-spine owners from research harness/case material.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_repo_map_v0.md
  - docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md
  - orca/product/spines/judgment/judgment_current_state_and_decomposition_v0.md
  - orca/product/spines/judgment/conductor/judgment_quality_promotion_operating_model_v0.md
  - orca/product/spines/judgment/conductor/judgment_spine_gate_ownership_map_v0.md
  - orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md
stale_if:
  - The Judgment spine corpus migrates from orca/product/ into forseti/product/.
  - The conductor or claim ladder is superseded.
  - The research consolidation map changes its routing role.
```

## Load Order

1. Open the research consolidation map first when crossing between cases,
   harness specs, prompts, and product-spine owners.
2. Open the current-state decomposition for the local product-spine split.
3. Open the conductor before running or planning gate-sequenced judgment work.
4. Open the gate ownership map before classifying who owns a gate or blocker.
5. Open the evidence ladder before claim-tier, proof-tier, or buyer-proof
   boundary questions.

## File Classes

| Class | Files | Use |
| --- | --- | --- |
| Cross-tree map | `docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md` | One-hop routing across research cases, harness, and product owners. |
| Product state | `judgment_current_state_and_decomposition_v0.md` | Current spine decomposition and boundary context. |
| Conductor | `conductor/*.md` | Gate sequencing, gate ownership, and promotion operation. |
| Claim ladder | `claim_ladder/*.md` | Claim tier, evidence ladder, proof boundary, and buyer-proof boundary. |
| Demand read | `demand_read/**` | Demand-read taxonomy and verdict/action details after conductor routing. |

## Boundary

This is a legacy physical path under `orca/product/`. Forseti is the project
identity, but these Judgment owners remain here until a separate migration moves
them. This README is not validation, judgment-quality evidence, proof, or
implementation authorization.