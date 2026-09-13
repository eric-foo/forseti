# Judgment Harness

```yaml
retrieval_header_version: 1
artifact_role: Judgment Harness navigation artifact
scope: Local allocation point for Judgment Harness specs and adjacent context under Judgment Spine.
use_when:
  - Finding the working Judgment Harness spec.
  - Distinguishing harness specs from Judgment Spine case-learning artifacts.
  - Keeping side context near the harness without making it controlling spec authority.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/judgment_spine_consolidation_map_v0.md   # up: spine-wide entry map
  - docs/research/judgment-spine/harness/v0_14/index.md
  - docs/research/judgment-spine/harness/adjacent-context/README.md
```

## Allocation

`v0_14/` is the working Judgment Harness spec imported from the external v0.14 code-readiness docset.

`adjacent-context/` is nearby context that may inform future harness work, but it is not controlling v0.14 spec authority.

This area does not define Data Capture Spine, Evidence Candidate Record, or Cleaning Spine, and it does not authorize implementation by itself.

- [Coordinator efficiency samples (2026-09-12–13)](coordinator-efficiency-20260912/result.md): the adjudicated cold entry and combined result/accounting route saved 27.604% in one fresh complete caller/coordinator/worker pair (1,604,139 → 1,161,335 tokens), with source quality and 89/39 preservation intact. The earlier 5.558% result, errors and separate study overhead remain recorded. Repeatability and subscription quota impact remain unmeasured; PR #1601 owns publication.
