# Search-lane Migration Runbook

```yaml
retrieval_header_version: 1
artifact_role: Orca migration record
scope: >
  Owner runbook for the search-lane migration: physically move the lane's member
  docs into docs/product/search/ and rewrite the live reference set. Bound by
  docs/decisions/orca_search_product_lane_binding_v0.md.
use_when:
  - Executing or reviewing the search-lane physical move.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_search_product_lane_binding_v0.md
  - docs/migration/repo_structure_search_lane_v0/moves_manifest.csv
  - docs/migration/repo_structure_search_lane_v0/reference_inventory.md
stale_if:
  - The apply has run for all manifest rows (this runbook then documents history).
  - moves_manifest.csv changes.
```

## What this applies

10 tracked file moves into `docs/product/search/`, in two waves:

- Wave 1 (applied): the 4 search/answer-engine-surface docs (AEO probe +
  evidence, the search/AEO source-class spec, the search-interest capture
  profile).
- Wave 2: the 6 demand-signal-method docs (demand-scan core spec, read taxonomy
  + adjudication, scan/gate-adjudication packet, gate-definition closures,
  gate-run commission criteria).

The apply is IDEMPOTENT (already-moved rows are skipped). It rewrites every
full-path live reference (~19 live files for wave 2, across judgment_spine /
data_capture_spine / core_spine / product_lead), preserves git history via
`git mv`, writes `moved_paths_index.md`, and flips `repo-structure.yaml` `search`
planned -> current (idempotent). No moved file's content is edited except
intra-set full-path references; `docs/product/search/README.md` was
hand-restructured separately.

## PRECONDITION GATE

1. **Contended-lane awareness.** Wave 2 touches active lanes (judgment_spine,
   core_spine, product_lead, data_capture_spine). The owner authorized applying
   on the lane branch and committed to not reopening the contended spines during
   the window; git rename-detection auto-resolves most their-edit + our-rename
   merges for those lanes on their next rebase.
2. **Clean commit checkpoint.** Commit (or deliberately exclude) the worktree so
   the tree is clean - `--apply` REFUSES on a dirty tree. This is the rollback
   checkpoint. `--waive-dirty-tree` overrides only if you accept reduced
   rollback safety (not recommended).

## Apply sequence

```text
cd <this search-lane worktree root>
python docs/migration/repo_structure_search_lane_v0/apply_moves.py --dry-run   # expect exit 0
python docs/migration/repo_structure_search_lane_v0/apply_moves.py --apply
python .agents/hooks/check_placement.py --strict                               # expect no search/moved-file violations
# reference-resolution: no stale old-path hits should remain in LIVE docs
git grep -nE "(source_capture_toolbox|data_capture_spine|core_spine|product_lead)/(aeo_capture_feasibility_probe_phase0_v0|demand_search_interest_sourcing_and_gate_delta_spec_v0|demand_durability_indicator_search_interest_capture_profile_v0|orca_demand_scan_core_spec_v0|orca_demand_read_taxonomy_v0|orca_demand_read_taxonomy_adjudication_v0|orca_demand_scan_gate_adjudication_packet_v0|orca_demand_gate_definition_closures_proposal_v0|orca_demand_gate_run_commission_criteria_v0)" -- docs ":!docs/decisions" ":!docs/review-inputs" ":!docs/review-outputs" ":!docs/prompts" ":!docs/research" ":!docs/hygiene" ":!docs/migration"
git diff --stat
```

Then commit (renames + rewritten references + status flip + `moved_paths_index.md`).

## Validation

- `--dry-run` exit 0 (pending sources exist, targets free, no collision).
- `check_placement.py --strict`: no violations for the search lane / moved files
  (remaining strict failures are pre-existing root + `orca-harness/**` legacy).
- reference-resolution grep returns nothing (historical records keep old paths,
  resolved via `moved_paths_index.md`).
- `git log --follow` on a moved file shows history preserved (git mv).

A green check is placement shape only - not validation, readiness, or product
proof.

## Rollback

`apply_moves.py --reverse` restores all moved paths (git mv back). The
live-reference rewrites and the status flip are content edits - revert them via
git from the checkpoint (not undone by `--reverse`).

## Non-claims

Not validation, readiness, or product proof. The apply changes placement and the
reference set only; no artifact's authority, content (beyond intra-set
references), or acceptance state changes. Placing the demand-signal method docs
in `search/` does not narrow their venue-spanning authority.
