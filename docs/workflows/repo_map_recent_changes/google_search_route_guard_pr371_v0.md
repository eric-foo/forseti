# Google Search-Surface Route Guard PR 371

```yaml
retrieval_header_version: 1
artifact_role: Repo-map recent-change note
scope: Low-conflict context for the Google search-surface route guard added in PR #371.
use_when:
  - Reconstructing why durable docs are checked for the parameterized Google capture route shell.
  - Checking PR #371 repo-map context without appending chronology to the main repo-map header.
open_next:
  - docs/workflows/orca_repo_map_v0.md
  - docs/decisions/search_surface_google_parameterized_us_capture_route_v0.md
  - .agents/hooks/check_search_surface_google_route.py
authority_boundary: retrieval_only
```

PR #371 adds the Google search-surface route guard:
`.agents/hooks/check_search_surface_google_route.py` enforces the checkable
shell of `docs/decisions/search_surface_google_parameterized_us_capture_route_v0.md`
for changed durable docs — Google Search capture URLs use `hl=en&gl=us&pws=0`,
route-using artifacts carry the physical-locality non-claim, and blocked
Google pages with visible exit-IP content are not preserved in durable docs.
Wired as advisory PostToolUse hooks in `.claude/settings.json` and
`.codex/hooks.json`, plus a diff-scoped CI gate in
`.github/workflows/ci.yml`. Route-shape only: US-parameterized is not
physically US-local, and the guard is not physical-locality proof,
validation, readiness, demand proof, Judgment evidence, or Product Lead
evidence.
