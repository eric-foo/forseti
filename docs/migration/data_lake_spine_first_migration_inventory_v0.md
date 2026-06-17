# Data Lake Spine-First Migration Inventory v0

```yaml
retrieval_header_version: 1
artifact_role: Migration inventory (spine-first marking; docs-only)
scope: >
  Marks visible Data Lake and Data-Lake-adjacent documents for a future
  spine-first migration, without moving files or changing the current
  repo-structure binding.
use_when:
  - Planning the Data Lake phase of a spine-first Orca workspace migration.
  - Deciding which lake documents belong in a future Data Lake workspace versus Capture, ECR, Cleaning, Judgment, harness, or global homes.
  - Preparing a later migration manifest or moved-path index for Data-Lake-related documents.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_spine_first_workspace_structure_proposal_v0.md
  - docs/decisions/orca_repo_structure_binding_v0.md
  - docs/product/core_spine/core_spine_v0_data_lake_storage_contract_v0.md # nonresolving: source branch artifact, not present in this worktree
  - docs/product/core_spine/core_spine_v0_data_lake_core_contract_v0.md # nonresolving: source branch artifact, not present in this worktree
  - docs/workflows/orca_repo_map_v0.md
stale_if:
  - The spine-first workspace proposal is accepted, rejected, or materially amended.
  - The Data Lake contract branch lands, rebases, or is superseded without this inventory being refreshed.
  - Data Lake files move or new lake contracts are added.
  - A later migration manifest supersedes this class-level inventory.
```

- Status: MIGRATION_MARKING_ONLY.
- Structure-branch basis: `codex/commission-spine-structure` at
  `07a42b04c4343c4e3b964eea11b01fc9ebefe705` when this inventory was drafted.
- Data-Lake branch basis: `codex/data-lake-core-contract` at
  `4200b8dd9095a7006dee6e9ae6fa585fe529dd0a` when this inventory was drafted.
- Current binding remains `docs/` plus `orca-harness/`; this file does not make
  `orca/product/`, `orca/product/spines/data_lake/`, or `orca/data-lake/` live.
- No file moves, rewrites, archive decisions, runtime changes, code moves, test
  moves, or reference rewrites are authorized by this inventory.
- The structure worktree had unrelated modified Commission Signal Board files
  while this inventory was drafted; those files are not used as data-lake
  evidence.

## Placement Recommendation

If the spine-first proposal is later accepted in its current shape, prefer this
candidate root:

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

Do not use `orca/data-lake/` from this inventory. A standalone top-level lake
root would require a separate root-layout decision because the current structure
proposal places product workspaces under `orca/product/spines/`, and the current
binding does not allow a top-level `orca/` product subtree at all.

Do not use `orca/product/data-lake/` unless the accepted structure decision
materially amends the proposed `orca/product/spines/<spine>/` grammar.

## Inventory Method

Searches and reads used:

```powershell
rg -l "Data Lake|data lake|data-lake|Attachment Record|Availability Index|Raw Packet Store|Derived Result Store|Acknowledgement Log|lake-owned|lake core|lake boundary" docs orca-harness
rg --files -g "*data_lake*" -g "*lake*" -g "*attachment_record*" -g "*source_capture*" -g "*signal_statement*"
```

Observed direct/current candidate counts:

| Surface | Count | Marking strength |
| --- | ---: | --- |
| Data-Lake branch direct lake contracts/maps under `docs/product/core_spine/` | 4 | Direct Data Lake authority/workflow candidates after branch landing. |
| Structure branch lake-related docs/maps currently visible | 6 | Existing current-branch lake or lake-adjacent candidates. |
| Lake-related route maps | 3 | Keep global or create spine-local pointers; do not auto-move. |
| `orca-harness/` direct `data_lake` hits | 0 | No canonical data-lake package exists yet. Harness surfaces are pointer targets only. |

These counts are search-observed, not validation or migration completeness.

## Direct Data Lake Candidates

These are the cleanest future Data Lake workspace candidates. On the structure
branch, only the mechanics map is currently present; the other three were
observed on the data-lake contract branch and should be refreshed after that
branch lands or is rebased into the structure migration work.

| Current path | Proposed target slot | Migration mark |
| --- | --- | --- |
| `docs/product/core_spine/core_spine_v0_data_lake_core_contract_v0.md` | `authority/` | migrate_later_after_branch_lands |
| `docs/product/core_spine/core_spine_v0_data_lake_storage_contract_v0.md` | `authority/` | migrate_later_after_branch_lands |
| `docs/product/core_spine/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md` | `authority/` | migrate_later_after_branch_lands |
| `docs/product/core_spine/core_spine_v0_data_lake_mechanics_map_v0.md` | `workflows/` or `authority/` | migrate_later |

The future Data Lake workspace should preserve the lake boundary recorded in
these files: raw packet preservation, stable by-key findability, passive
availability facts, source-family Attachment Records, append-only derived or
acknowledgement references, and no Cleaning/ECR/Signal Statement/Judgment
orchestration.

## Lake-Adjacent Boundary And Probe Candidates

These files are data-lake relevant, but they also belong to Capture or
source-family boundary work. Do not auto-move them into the Data Lake workspace
without an ownership decision.

| Current path | Proposed target slot | Migration mark |
| --- | --- | --- |
| `docs/product/data_capture_spine/source_capture_tenant_payload_attachment_boundary_v0.md` | Data Lake `authority/` pointer, or Capture `authority/` if Capture remains owner | classify_before_move |
| `docs/product/data_capture_spine/source_capture_core_payload_split_explainer_v0.md` | Data Lake `authority/` pointer or Capture explanatory note | classify_before_move |
| `docs/product/data_capture_spine/retail_pdp_typed_envelope_probe_v0.md` | `research/` or Capture/source-family probe home | classify_before_move |

Default stance: the Data Lake workspace should point to these as controlling or
supporting sources rather than absorb them blindly. They define source-payload
attachment pressure and proof, but they are not themselves storage-engine,
queue, or smart-lake authority.

## Route Maps And Global Indexes

These are route/index surfaces. They should not be treated as Data Lake
workspace artifacts by default.

| Current path | Proposed future treatment | Migration mark |
| --- | --- | --- |
| `docs/workflows/orca_repo_map_v0.md` | Keep global; update paths if a move occurs. | keep_global_update_refs_later |
| `docs/workflows/data_capture_spine_consolidation_map_v0.md` | Keep Capture route map or global map; update lake pointers if a move occurs. | keep_global_or_capture_update_refs_later |
| `docs/workflows/ecr_spine_submap_v0.md` | Keep ECR route map or global map; update lake pointers if a move occurs. | keep_global_or_ecr_update_refs_later |
| `docs/decisions/dcp_receipts_archive_v0.md` | Keep global receipt archive. | keep_global |

## Harness And Test Pointer Candidates

No canonical `orca-harness/data_lake/` package exists at this marking point.
Future Data Lake `harness/` and `tests/` folders should carry pointers or test
plans, not move runtime code out of `orca-harness/` without a separate code-root
migration decision.

Class-level pointer candidates:

| Current path class | Future Data Lake pointer purpose | Migration mark |
| --- | --- | --- |
| `orca-harness/source_capture/models.py` | Raw packet, slice, preserved-file, stable-ID, hash, and pointer integrity model. | keep_harness_add_pointer_later |
| `orca-harness/source_capture/writer.py` | Capture packet materialization and preserved-file metadata write boundary. | keep_harness_add_pointer_later |
| `orca-harness/source_capture/*_projection.py` | Mechanical projection views that carry raw refs and anchors, not replacement source truth. | keep_harness_add_pointer_later |
| `orca-harness/ecr/**` | Derived ECR records keyed to raw; sibling derived lane, not lake core. | keep_harness_add_pointer_later |
| `orca-harness/signal_content/**` or future `orca-harness/signal_statement/**` | Signal Statement/Content records keyed to raw/ECR refs; sibling derived lane, not lake core. | keep_harness_add_pointer_later |
| `orca-harness/evidence_binding/**` | Reference-never-merge evidence binding and verifier surfaces. | keep_harness_add_pointer_later |
| `orca-harness/tests/unit/test_source_capture_packet.py` | Packet/preserved-file reference integrity tests. | keep_harness_add_test_pointer_later |
| `orca-harness/tests/unit/test_ecr_source_side_composition.py` | Derived record keying/composition tests. | keep_harness_add_test_pointer_later |
| `orca-harness/tests/unit/test_signal_content_deriver.py` or future signal-statement equivalent | Signal Statement/Content re-derivation and keyed-reference tests. | keep_harness_add_test_pointer_later |
| `orca-harness/tests/unit/test_evidence_binding.py` | Exact-key binding and anti-laundering tests. | keep_harness_add_test_pointer_later |

## Shared Or Adjacent - Do Not Auto-Migrate

These surfaced during discovery but should not be treated as Data Lake move
targets without owner/source-boundary review:

| Path class | Reason |
| --- | --- |
| Data Capture obligation, observability, source-access, and runner authorization decisions | Capture/source-access ownership; may cite lake constraints but should not be swallowed by the lake. |
| Cleaning foundation documents | Cleaning owns transform and normalization boundaries; lake only stores raw and keyed references. |
| ECR and Signal Statement/Content docs or prompts | Sibling derived-record lanes; data lake stores keyed state but does not own derivation semantics. |
| Judgment review inputs/outputs containing data-boundary source snapshots | Historical review bundles; keep under review/archive rules unless a later review migration says otherwise. |
| Python code under `orca-harness/` | Runtime/code tree; not document migration. |

## Proposed Migration Sequence

1. Do not migrate Data Lake before the root `orca/product/spines/` binding is
   accepted or amended.
2. After the Data Lake contract branch lands or rebases, refresh this inventory
   against the merged file set.
3. Migrate the four direct Data Lake contract/map files first, if the target
   root is accepted.
4. Update global route maps to point at the new paths through a moved-path
   index.
5. Add Data Lake `harness/` and `tests/` pointer notes only after the document
   move target is accepted; leave canonical code and executable tests in
   `orca-harness/`.
6. Classify Capture/ECR/Cleaning/Judgment adjacent files individually rather
   than bulk-moving every file that mentions lake mechanics.

## Non-Claims

This inventory is not a move manifest, validation, readiness, acceptance,
source-of-truth promotion, proof of completeness, root-layout approval,
implementation authorization, backend selection, or physical storage selection.
It marks Data-Lake-related documents and classes for later migration planning
only.
