# Data Lake Spine-First Migration Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Migration plan (Data Lake shared-foundation spine; docs-only)
scope: >
  Prepares the future `orca/product/spines/data_lake/` workspace shape, lane
  marks, move order, pointer strategy, and blocked binding work for Data Lake
  without creating a live `orca/` root or moving files under current binding.
use_when:
  - Preparing a Data Lake move after the spine-first workspace proposal is accepted or amended.
  - Checking which Data Lake files are direct move candidates versus Capture, ECR, Cleaning, Judgment, harness, or global pointers.
  - Drafting the future Data Lake `spine.yaml`, README, moved-path index, or reference-rewrite plan.
authority_boundary: retrieval_only
open_next:
  - docs/migration/data_lake_spine_first_migration_inventory_v0.md
  - docs/decisions/orca_spine_first_target_structure_binding_v0.md
  - docs/decisions/orca_repo_structure_binding_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
  - docs/workflows/orca_repo_map_v0.md
stale_if:
  - The spine-first workspace proposal is accepted, rejected, or materially amended.
  - The Data Lake contract branch lands, rebases, or is superseded.
  - `repo-structure.yaml` adds `orca/product/spines/` as a live root before this plan is applied.
  - Any direct Data Lake contract file moves or changes ownership.
```

- Status: MIGRATION_PLAN_ONLY.
- Structure-branch basis: `codex/commission-spine-structure` at
  `8f34ccd703b79b8787bb8009a5f1e7a783c08419` when this plan was drafted.
- Current binding remains `docs/` plus `orca-harness/`; this file does not make
  `orca/product/spines/data_lake/` live.
- No file moves, runtime storage work, backend choice, queue design,
  implementation work, harness move, test move, or reference rewrite is
  authorized by this plan.
- Existing staged/dirty worktree changes outside Data Lake migration files were
  present during drafting and are out of scope.

## Target Spine Identity

Future root, only after later accepted repo-structure binding:

```text
orca/product/spines/data_lake/
  README.md
  spine.yaml
  authority/
  decisions/
  prompts/
  workflows/
  research/
  cases/
  reviews/
  reports/
  harness/
  tests/
  migrations/
  archive/
```

The Data Lake should be treated as a shared foundation spine:

```yaml
name: data_lake
spine_kind: shared_foundation
future_root: orca/product/spines/data_lake/
producers:
  - capture
consumers:
  - projection
  - ecr
  - signal_statement
  - cleaning
  - judgment
owns:
  - raw packet preservation contract
  - keyed retrievability contract
  - Attachment Record contract
  - passive Availability Index contract
  - append-only derived-result and acknowledgement attachment contract
does_not_own:
  - physical backend or storage engine
  - source capture execution
  - Mechanical Source Projection semantics
  - ECR derivation semantics
  - Signal Statement interpretation
  - Cleaning transforms
  - Judgment interpretation
  - queue, retry, scheduling, or lane orchestration
```

This is the structural answer to the shared-use concern: the lake has its own
workspace because it owns hard storage contracts, while other lanes remain
separate producers or consumers.

## Move Classification

| Owner class | Meaning | Future treatment |
| --- | --- | --- |
| `data_lake_owned` | The artifact defines lake-owned responsibility, storage contract, or lake mechanics. | Move into `orca/product/spines/data_lake/` after binding. |
| `pointer_only` | Canonical artifact or code stays elsewhere, but the Data Lake spine should point to it. | Add pointer docs or references after binding. |
| `classify_before_move` | Data-lake relevant, but ownership may belong to Capture/source-family work. | Decide owner before moving. |
| `keep_global` | Repo-wide route, structure, receipt, or governance surface. | Keep global; update references only. |
| `other_spine_owned` | ECR, Signal Statement, Cleaning, Judgment, or Capture-owned artifact. | Do not move into Data Lake; reference only if needed. |

## Direct Move Set

These are the first move candidates once the future root is accepted and the
Data Lake contract branch is merged or rebased into the structure migration
branch.

| Current path | Future path | Owner class | Phase |
| --- | --- | --- | --- |
| `docs/product/core_spine/core_spine_v0_data_lake_core_contract_v0.md` | `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md` | `data_lake_owned` | P1 |
| `docs/product/core_spine/core_spine_v0_data_lake_storage_contract_v0.md` | `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md` | `data_lake_owned` | P1 |
| `docs/product/core_spine/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md` | `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md` | `data_lake_owned` | P1 |
| `docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md` | `orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md` | `data_lake_owned` | P1 |

The mechanics map could also live under `authority/`, but `workflows/` is the
better first target because the plan says `authority/` is for contracts and
invariants while `workflows/` is for route cards and mechanics maps.

## Pointer And Classification Set

These should not be swept into Data Lake during the first move.

| Current path or class | Future treatment | Owner class | Phase |
| --- | --- | --- | --- |
| `docs/product/data_capture_spine/source_capture_tenant_payload_attachment_boundary_v0.md` | Add Data Lake pointer to the controlling Capture payload-boundary source, or classify for later move if owner accepts lake ownership. | `classify_before_move` | P2 |
| `docs/product/data_capture_spine/source_capture_core_payload_split_explainer_v0.md` | Keep Capture explanatory note or index it from Data Lake. | `classify_before_move` | P2 |
| `docs/product/data_capture_spine/retail_pdp_typed_envelope_probe_v0.md` | Keep as Capture/source-family probe unless a later source makes it Data Lake research. | `classify_before_move` | P2 |
| `docs/product/data_capture_spine/orca_capture_projection_storage_spine_architecture_v0.md` | Treat as a Data Lake candidate only if its proposed storage-backbone direction is accepted or superseded into the lake contract set. | `classify_before_move` | P2 |
| `docs/product/data_capture_spine/source_capture_packet_schema_evolution_architecture_v0.md` and `docs/decisions/source_capture_archive_snapshot_typed_timing_decision_v0.md` | Keep Capture-owned packet lifecycle and timing authority; Data Lake points to packet schema/version/timing rules. | `pointer_only` | P2 |
| `docs/product/data_capture_spine/data_capture_harness_operating_model_architecture_v2*.md`, `docs/product/data_capture_spine/data_capture_spine_intake_surface_consolidation_v0.md`, and pressure-test authorization docs | Keep Data Capture-owned MSP helper docs; Data Lake points to projection mechanics only. | `pointer_only` | P2 |
| `docs/product/source_capture_toolbox/retail_pdp_projection_contract_v0.md`, `docs/product/source_capture_toolbox/retail_pdp_projection_playbook_v0.md`, and `docs/product/source_capture_toolbox/retail_pdp_sidecar_operator_playbook_v0.md` | Keep source-family projection/operator docs; Data Lake points to raw/projection references only. | `pointer_only` | P2 |
| Source Capture runner, source-quality, candidate-intake, source-observability, and demand-durability docs | Keep Capture/source-access ownership; Data Lake may cite preserved-file handles and packet/envelope authority by pointer. | `pointer_only` | P2 |
| IG creator momentum, creator monitoring, IG capture-shape, and IG R-probe docs | Split candidate: Data Lake may own projection-store mechanics, while IG/product lanes own monitoring and source-family semantics. | `uncertain` | P2 |
| `docs/product/core_spine_v0_projection_doctrine_v0.md` | Keep core projection doctrine; Data Lake imports by pointer because projection is explicitly not a new lake layer. | `other_spine_owned` | P2 |
| `docs/workflows/orca_repo_map_v0.md` | Keep global and update paths after the move. | `keep_global` | P1 reference update |
| `docs/workflows/data_capture_spine_consolidation_map_v0.md` | Keep Capture/global route map and update lake pointers. | `keep_global` or `other_spine_owned` | P1 reference update |
| `docs/workflows/ecr_spine_submap_v0.md` | Keep ECR/global route map and update lake pointers. | `keep_global` or `other_spine_owned` | P1 reference update |
| `docs/decisions/dcp_receipts_archive_v0.md` | Keep global receipt archive. | `keep_global` | no move |
| `orca-harness/source_capture/**` | Keep canonical runtime/code in `orca-harness`; add Data Lake harness pointer docs later. | `pointer_only` | P3 |
| `orca-harness/ecr/**` | Keep ECR-owned runtime/code; Data Lake references derived-record attachment only. | `pointer_only` | P3 |
| `orca-harness/signal_content/**` or future `orca-harness/signal_statement/**` | Keep Signal Statement runtime/code; Data Lake references keyed attachment only. | `pointer_only` | P3 |
| `orca-harness/cleaning/**` | Keep Cleaning runtime/code; Data Lake references Cleaning ledger attachment only. | `pointer_only` | P3 |
| `orca-harness/evidence_binding/**` | Keep Evidence Binding runtime/code; Data Lake may point to verifier/pointer behavior. | `pointer_only` | P3 |

## Proposed Spine Files To Create After Binding

Create these only after `orca/product/spines/` is accepted as a live root:

```text
orca/product/spines/data_lake/README.md
orca/product/spines/data_lake/spine.yaml
orca/product/spines/data_lake/migrations/moved_paths_index.md
orca/product/spines/data_lake/harness/runtime_pointer_map.md
orca/product/spines/data_lake/tests/test_pointer_map.md
```

`README.md` should say:

- Data Lake is a shared foundation spine.
- It stores and exposes keyed state; it does not orchestrate lanes.
- Capture is the raw producer; Projection, ECR, Signal Statement, Cleaning, and
  Judgment are consumers or derived writers.
- Canonical executable code remains in `orca-harness/` until a separate
  code-root migration is accepted.

`moved_paths_index.md` should map only the direct move set in P1 at first.

## Apply Sequence After Binding

1. Rebase or merge the Data Lake contract branch into the structure migration
   branch so all four direct Data Lake files exist in one tree.
2. Accept or amend the spine-first proposal with `data_lake` as a
   `shared_foundation` spine under `orca/product/spines/`.
3. Update binding surfaces: `docs/decisions/orca_repo_structure_binding_v0.md`,
   `.agents/workflow-overlay/artifact-folders.md`, `repo-structure.yaml`,
   `docs/STRUCTURE.md`, `docs/workflows/orca_repo_map_v0.md`, and placement
   checker expectations if they enforce closed roots.
4. Create the Data Lake spine skeleton and move the four P1 direct files.
5. Add `migrations/moved_paths_index.md` for the four moved files.
6. Rewrite live references in route maps and direct lake docs to the new paths.
7. Add harness/test pointer maps only; do not move `orca-harness` code.
8. Classify P2 Capture/source-family candidates. Move only the ones whose
   accepted owner becomes Data Lake; otherwise create spine-local pointers.
9. Leave ECR/Signal Statement/Cleaning/Judgment adjacent docs in place unless
   separately classified by their owning spine.

## Validation For Future Apply

Run these after a real move:

```powershell
git diff --check
python .agents\hooks\check_retrieval_header.py --changed
python .agents\hooks\check_repo_map_freshness.py --changed
python .agents\hooks\check_placement.py --check
rg -n "docs/product/core_spine/core_spine_v0_data_lake_(core_contract|storage_contract|attachment_record_implementation_contract|mechanics_map)_v0.md" docs orca product .agents
```

Expected after the real move: no live references should require the old paths
except historical review/migration records and the moved-path index.

## Current Blockers

```yaml
live_move_blockers:
  - root `orca/product/spines/` is proposed, not current binding
  - direct Data Lake contract files are split across the structure branch and the data-lake contract branch
  - adjacent Capture/ECR/Cleaning/Judgment ownership must not be collapsed into lake ownership
  - runtime/code movement is separately unauthorized
```

## Non-Claims

This plan is not a move manifest, validation, readiness, acceptance,
source-of-truth promotion, root-layout approval, implementation authorization,
backend selection, queue design, storage-engine selection, or physical storage
selection. It prepares a future move shape and lane marking only.
