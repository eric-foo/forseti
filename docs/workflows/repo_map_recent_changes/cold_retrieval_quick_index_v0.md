# Repo Map Change Note — Decisive-File Quick Index (Cold Retrieval)

```yaml
retrieval_header_version: 1
artifact_role: Workflow navigation note (repo-map recent-change context)
scope: >
  Context for the 2026-07-04 repo-map change that added the Decisive-File Quick
  Index (Cold Retrieval) section, sharpened the foundation-spine row's fragrance
  fact path, and added the Aphrodite fragrance sub-ontology row to Workstream
  Status Pointers.
use_when:
  - Investigating why the Decisive-File Quick Index exists or whether to extend it.
  - Diagnosing repo-map churn around 2026-07-04.
open_next:
  - docs/workflows/forseti_repo_map_v0.md
authority_boundary: retrieval_only
stale_if:
  - The Decisive-File Quick Index section is removed or restructured.
  - The cold-lane read budget in .agents/workflow-overlay/source-loading.md changes.
```

## What changed and why

A measured cold-retrieval test (2026-07-04, run against main tip `dc5da157`
after PRs #695/#698) had a fresh agent resolve two fragrances from the standard
entry points. It resolved both correctly with per-fact provenance and no guessed
paths, but used ~9 full-file reads against the ratified cold-lane bar of 4
full + 8 targeted reads (`.agents/workflow-overlay/source-loading.md`,
"budgets are also the ratified cold-lane retrievability bar"). The overage came
from verifying through the doctrine chain (source-of-truth -> ontology backbone
-> exemplar card) before reaching the decisive data file — nothing in the map
told a cautious cold reader that fact lookup may go straight to a
self-describing decisive file.

The fix is additive only: a Quick Index of six fact-lookup shortcut rows near
the top of the map, a sharpened foundation-spine row, and an Aphrodite
workstream status row. No section was moved or removed.

## Considered and rejected

- Extracting the ~430-line "Active Hooks" section to a reference doc: rejected —
  it is a doctrine-wide registration surface (cited by
  `.agents/workflow-overlay/validation-gates.md`, the enforcement-placement
  classification decision, and `check_repo_map_freshness.py`'s own message
  text), and it was not the measured budget cost.
- Full per-domain submap split: rejected — no evidence of need beyond the
  measured case; high contention on a commit-once-whole file.

## Follow-up candidates (not done here)

- Workstream Status Pointers table is dated 2026-06-13; rows other than the new
  Aphrodite row were not re-verified against their owning docs.
- A cold rerun of the retrieval test to observe a within-budget pass before
  claiming the Aphrodite packet's success signal 1 (the reader-discipline half
  of the overage is not fixable by map structure).

Non-claims: navigation context only; not validation, readiness, or proof the
map is complete.
