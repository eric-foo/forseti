# Capture Source-Family Lane Catalog Note

```yaml
retrieval_header_version: 1
artifact_role: Repo-map recent-change note
scope: >
  Navigation note for the new Capture source-family lane catalog, added so
  cold source-capture tasks can route from the generic playbook/Armory to the
  owning source-family index before searching harness rows.
use_when:
  - Reviewing why the repo map gained a known-source capture-to-lake quick-index row.
  - Maintaining the Data Capture submap or Capture source-family catalog.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_families/README.md
  - docs/workflows/forseti_repo_map_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
stale_if:
  - The Capture source-family lane catalog is removed, renamed, or superseded.
```

The source-capture front door now has a two-step cold route:

1. Source Capture Playbook / Armory: access method, route-catalog discipline,
   shared runner/tooling context.
2. Capture source-family lane catalog: known-family route homes that point to
   the family README, runner, projection, Data Lake, ECR, and Cleaning seams.

The repo map and Data Capture submap point to the catalog for known-source
capture-to-lake questions. Data Lake, ECR, and Cleaning contracts remain in
their owning spines; the catalog is routing-only.

Non-claims: not validation, readiness, source-access permission, lake authority,
ECR/Cleaning authority, runtime authorization, Judgment, or buyer proof.
