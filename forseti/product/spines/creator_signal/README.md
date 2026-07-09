# Creator Signal Spine

```yaml
retrieval_header_version: 1
artifact_role: Spine front-door
scope: Retrieval-only entry point for Forseti Creator Signal and Aphrodite D-1 product records.
use_when:
  - Starting Creator Signal or Aphrodite product-record work.
  - Finding the D-1 derived-claim provenance contract or panel design.
  - Checking whether a creator-signal artifact is product authority or research context.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_repo_map_v0.md
  - docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md
  - forseti/product/spines/creator_signal/aphrodite_derived_claim_provenance_contract_v0.md
  - forseti/product/spines/creator_signal/aphrodite_vetting_sprint_panel_design_v0.md
stale_if:
  - The Creator Signal spine gains a broader accepted operating model.
  - The Aphrodite D-1 recipe or panel design is superseded.
```

## Load Order

1. Open the Forseti repo map for identity and legacy-root posture.
2. Open the Aphrodite D-1 recipe when the work is evidence-lane or rehearsal
   specific.
3. Open the derived-claim provenance contract for claim-state and provenance
   rules.
4. Open the panel design for display/panel projection questions.

## File Classes

| Class | Files | Use |
| --- | --- | --- |
| Recipe context | `docs/research/aphrodite_depth_rehearsal_extraction_recipe_v1.md` | D-1 evidence-lane recipe, inputs, and closeout checklist. |
| Provenance contract | `aphrodite_derived_claim_provenance_contract_v0.md` | Derived-claim state and provenance boundaries. |
| Panel design | `aphrodite_vetting_sprint_panel_design_v0.md` | Five-panel sprint display shape. |

## Boundary

This spine front door does not prove creator-signal validation, buyer proof,
readiness, roster-scale capture, source truth, or product promotion. It only
routes the current live Creator Signal records.
