# Capture Spine IG Creator Migration Inventory v0

```yaml
retrieval_header_version: 1
artifact_role: Migration inventory (spine-first marking; docs-only)
scope: >
  Marks visible creator-momentum and beauty-creator files for a future
  Capture Spine / IG allocation under the proposed spine-first structure,
  without moving files or changing current repo-structure binding.
use_when:
  - Planning the creator-momentum portion of a future spine-first Orca workspace migration.
  - Deciding which IG creator files belong in a future Capture Spine home versus shared IG capture or global product docs.
  - Preparing a later move manifest for the 1,000-creator / creator-momentum lane.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_spine_first_workspace_structure_proposal_v0.md
  - docs/decisions/orca_repo_structure_binding_v0.md
  - docs/hygiene/ig_creator_momentum_lane_handoff_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - docs/workflows/orca_repo_map_v0.md
stale_if:
  - The spine-first workspace proposal is accepted, rejected, or materially amended.
  - Creator-momentum, IG capture, or source-capture files move or are split into a new submap.
  - A later migration manifest supersedes this class-level inventory.
```

- Status: MIGRATION_MARKING_ONLY.
- Branch basis: `codex/commission-spine-structure` at
  `8f34ccd703b79b8787bb8009a5f1e7a783c08419` when this inventory was finalized.
- Current binding remains `docs/` plus `orca-harness/`; this file does not make
  `orca/product/spines/capture/` live.
- No file moves, rewrites, archive decisions, runtime changes, test moves, or
  reference rewrites are authorized by this inventory.

## Boundary

The owner shorthand was "capturespine/IG". Under the proposal's grammar, the
spine is `capture`; `IG creator-momentum` is a sublane inside the role folders,
not a new accepted top-level root and not a reason to start the broader IG lane.

Candidate future namespace, only after a later accepted repo-structure
migration:

```text
orca/product/spines/capture/
  authority/ig_creator_momentum/
  decisions/ig_creator_momentum/
  prompts/ig_creator_momentum/
  workflows/ig_creator_momentum/
  research/ig_creator_momentum/
  reports/ig_creator_momentum/
  harness/ig_creator_momentum/
  tests/ig_creator_momentum/
  migrations/ig_creator_momentum/
  archive/handoffs/ig_creator_momentum/
```

This inventory intentionally does not create a live
`orca/product/spines/capture/ig/` layer. That would amend the proposed spine
grammar and needs a later structure decision if wanted.

## Inventory Method

Searches run from the worktree root:

```powershell
rg --files docs orca-harness | rg -i "beauty.*creator|creator.*beauty|1000.*creator|creator.*roster|creator.*monitor|creator.*pipeline|creator.*momentum"
rg --files docs orca-harness | rg -i "ig_.*calls|ig_calls|call_capture|wind_caller|creator_momentum|creator_roster|creator_discovery|momentum_harvest|ig_projection|metric_observation|ig_at_scale|logged_out_sustainability|sustained_cadence|r_probe|reel_viewcount"
rg -n "beauty creator|beauty creators|1,000 creators|1000 creators|creator roster|creator-momentum|creator momentum" docs/product docs/research docs/prompts docs/workflows docs/decisions docs/hygiene
rg -n "creator-momentum|creator_momentum|1000|1,000|wind-caller|CALLS|ig_creator|IG creator" docs/product/source_capture_toolbox docs/product/data_capture_spine docs/research docs/hygiene docs/workflows orca-harness/source_capture orca-harness/runners orca-harness/tests/unit
```

One read-only `gpt-5.3-codex-spark` explorer was attempted per owner direction,
but the session returned a model-usage-limit error before producing findings.
This inventory therefore uses local filesystem search and direct source reads
only.

Observed candidate counts:

| Surface | Count | Marking strength |
| --- | ---: | --- |
| Direct creator-momentum docs | 7 | Direct future Capture Spine / IG creator candidates. |
| Direct creator-momentum harness files | 6 | Keep in `orca-harness/` now; future pointer or code-root migration only. |
| IG wind-caller / operating-envelope adjacent files | 14 | Adjacent context; do not auto-migrate as creator-owned. |
| Global/shared product and source-capture references | 9 | Reference-only; keep global/shared unless later classified. |

These counts are search-observed, not validation or migration completeness.

## Direct Creator Candidates

These files are creator-momentum or beauty-creator owned enough to mark for the
future Capture Spine / IG creator sublane.

| Current path | Proposed target slot | Migration mark |
| --- | --- | --- |
| `docs/product/data_capture_spine/orca_creator_momentum_pipeline_architecture_v0.md` | `authority/ig_creator_momentum/` | migrate_later |
| `docs/product/data_capture_spine/orca_creator_monitoring_policy_architecture_v0.md` | `authority/ig_creator_momentum/` or `workflows/ig_creator_momentum/` | migrate_later_classify |
| `docs/product/source_capture_toolbox/ig_creator_roster_frontier_ledger_spec_v0.md` | `authority/ig_creator_momentum/` | migrate_later |
| `docs/product/source_capture_toolbox/ig_creator_discovery_spec_v0.md` | `authority/ig_creator_momentum/` or `workflows/ig_creator_momentum/` | migrate_later_classify |
| `docs/product/source_capture_toolbox/ig_creator_discovery_suggested_accounts_recon_v0.md` | `research/ig_creator_momentum/` | migrate_later |
| `docs/research/creator_momentum_data_landscape_v0.md` | `research/ig_creator_momentum/` | migrate_later |
| `docs/hygiene/ig_creator_momentum_lane_handoff_v0.md` | `archive/handoffs/ig_creator_momentum/` | migrate_later_as_lane_state_archive |

The hygiene handoff is not source authority. It should be preserved as a lane
state checkpoint or archived after the authoritative files above are moved and
indexed.

## Direct Harness Pointers

These are direct creator-momentum implementation/test surfaces, but executable
code remains in `orca-harness/` under current binding. Future spine allocation
should add pointers or a separate accepted code-root migration, not move these
as part of a docs-only migration.

| Current path | Proposed target slot | Migration mark |
| --- | --- | --- |
| `orca-harness/source_capture/ig_momentum_harvest.py` | `harness/ig_creator_momentum/pointers/` | pointer_later_keep_code_root_now |
| `orca-harness/source_capture/ig_projection.py` | `harness/ig_creator_momentum/pointers/` | pointer_later_keep_code_root_now |
| `orca-harness/runners/run_ig_creator_momentum_projection.py` | `harness/ig_creator_momentum/pointers/` | pointer_later_keep_code_root_now |
| `orca-harness/tests/unit/test_ig_momentum_harvest.py` | `tests/ig_creator_momentum/pointers/` | pointer_later_keep_code_root_now |
| `orca-harness/tests/unit/test_source_capture_ig_projection.py` | `tests/ig_creator_momentum/pointers/` | pointer_later_keep_code_root_now |
| `orca-harness/tests/unit/test_source_capture_metric_observation.py` | `tests/ig_creator_momentum/pointers/` | pointer_later_keep_code_root_now |

## Adjacent IG Capture Files

These files mention or enable creator-momentum work, but they are broader IG
capture, wind-caller, sustainability, probe, or operating-envelope materials.
Do not move them as creator-owned files without a later classification pass.

| Current path | Likely future home | Migration mark |
| --- | --- | --- |
| `docs/product/source_capture_toolbox/ig_wind_caller_capture_feasibility_recon_v0.md` | Capture Spine shared IG research or `research/ig_creator_momentum/` | migrate_later_classify |
| `docs/product/source_capture_toolbox/ig_reel_viewcount_capture_feasibility_recon_v0.md` | Capture Spine shared IG research or `research/ig_creator_momentum/` | migrate_later_classify |
| `docs/product/source_capture_toolbox/ig_wind_caller_calls_capture_build_architecture_v0.md` | Capture Spine shared IG authority/harness | migrate_later_classify |
| `docs/product/source_capture_toolbox/ig_capture_findings_consolidated_v0.md` | Capture Spine shared IG research | reference_only_do_not_auto_migrate |
| `docs/product/source_capture_toolbox/ig_at_scale_operating_envelope_v0.md` | Capture Spine shared IG workflows/research | reference_only_do_not_auto_migrate |
| `docs/product/source_capture_toolbox/ig_logged_out_sustainability_probe_plan_v0.md` | Capture Spine shared IG research/reports | reference_only_do_not_auto_migrate |
| `docs/product/source_capture_toolbox/ig_sustained_cadence_r_probe_design_v0.md` | Capture Spine shared IG research/reports | reference_only_do_not_auto_migrate |
| `docs/product/source_capture_toolbox/ig_r_probe_results_v0.md` | Capture Spine shared IG reports | reference_only_do_not_auto_migrate |
| `docs/prompts/handoffs/ig_capture_rate_at_scale_operating_envelope_handoff_v0.md` | Capture Spine shared IG prompts/archive | reference_only_do_not_auto_migrate |
| `orca-harness/source_capture/ig_calls_parse.py` | `harness/` pointer only after IG capture classification | classify_before_pointer |
| `orca-harness/runners/run_source_capture_ig_calls_packet.py` | `harness/` pointer only after IG capture classification | classify_before_pointer |
| `orca-harness/tests/unit/test_ig_calls_parse.py` | `tests/` pointer only after IG capture classification | classify_before_pointer |
| `orca-harness/tests/unit/test_source_capture_ig_calls_packet.py` | `tests/` pointer only after IG capture classification | classify_before_pointer |
| `docs/product/data_capture_spine/data_capture_spine_future_exploration_lanes_v0.md` | shared Capture Spine or global product roadmap | reference_only_do_not_auto_migrate |

## Global Or Shared References

These files contain creator roster, 1,000-creator, or wind-caller context, but
they are not creator-lane-owned migration candidates.

| Current path | Reason to keep out of creator-only move | Migration mark |
| --- | --- | --- |
| `docs/decisions/wind_caller_calibration_carveout_v0.md` | Cross-lane decision authority for wind-caller calibration boundaries. | global_reference_only |
| `docs/product/data_capture_spine/orca_capture_projection_storage_spine_architecture_v0.md` | Shared storage/projection backbone; creator-momentum is the first consumer, not the only owner. | shared_reference_only |
| `docs/workflows/data_capture_spine_consolidation_map_v0.md` | Data Capture Spine submap and route owner. | global_reference_only |
| `docs/product/source_capture_toolbox/README.md` | Source Capture Toolbox local index. | global_reference_only |
| `docs/product/source_capture_toolbox/source_capture_playbook_v0.md` | General source-capture playbook. | global_reference_only |
| `docs/product/source_capture_toolbox/capture_recon_index_v0.md` | Recon index spanning multiple capture surfaces. | global_reference_only |
| `docs/prompts/product-planning/chatgptpro_beauty_subniche_research_prompt_v0.md` | Product-planning prompt that references the creator roster path; not creator lane authority. | product_shared_reference_only |
| `docs/product/product_lead/orca_demand_read_taxonomy_v0.md` | Demand taxonomy; carries subject-creator boundary as product policy context. | product_shared_reference_only |
| `docs/product/product_lead/orca_demand_read_taxonomy_adjudication_v0.md` | Taxonomy adjudication; carries subject-creator boundary as product policy context. | product_shared_reference_only |

## Explicit Exclusions

Do not treat these as creator-lane files merely because search terms hit them:

| Path class | Reason excluded |
| --- | --- |
| `docs/product/data_capture_spine/data_capture_spine_reddit_graph_frontier_lane_architecture_v0.md` | Reddit graph frontier, not IG creator-momentum. |
| `orca-harness/runners/run_reddit_graph_frontier_register.py` and related tests | Reddit graph frontier implementation, not IG creator-momentum. |
| `orca-harness/runners/run_linkedin_graph_frontier_register.py` and related tests | LinkedIn graph frontier implementation, not IG creator-momentum. |
| `docs/product/product_lead/*consumer_demand*` except rows listed above | Product strategy context, not creator lane ownership. |
| `docs/research/orca_discovery_candidate_scan_beauty_subniche_chatgptpro_v0.md` | Beauty niche/product research that cites the roster spec; not a creator-spine source file. |

## Proposed Migration Sequence

1. Keep current files in place until the spine-first structure proposal is
   accepted or amended.
2. If accepted, create the Capture Spine workspace with role folders first,
   then add an `ig_creator_momentum` migration plan under the spine's
   `migrations/` folder.
3. Move only the direct creator candidates first: pipeline architecture,
   monitoring policy, roster/frontier ledger, discovery spec, discovery recon,
   and data landscape.
4. Preserve `docs/hygiene/ig_creator_momentum_lane_handoff_v0.md` as archive or
   retire it after current-state facts are either superseded or rehomed.
5. Add harness and test pointers for the creator-momentum projection/harvest
   helpers. Do not move executable code until code-root migration is accepted.
6. Run a separate shared-IG classification pass before moving wind-caller,
   CALLS, logged-out sustainability, rate-probe, or operating-envelope files.

## Non-Claims

This inventory is not:

- acceptance of the spine-first proposal;
- authorization to create `orca/product/spines/capture/`;
- authorization to move files;
- an IG capture lane migration;
- validation that the 1,000-creator plan is built, feasible, or current;
- proof that every creator-related reference in the repo has been found.
