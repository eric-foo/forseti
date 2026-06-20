```yaml
retrieval_header_version: 1
artifact_role: Orca migration note
scope: >
  Phase-2 W3a proposal for the data_lake area (orca/product/spines/data_lake/):
  bloat/deletion candidates with full deletion-evidence records and
  ontology/doc-term findings against the SSOT.
use_when:
  - Owner adjudicating Phase-2 deletion candidates for the data_lake spine.
  - Reviewing ontology/doc-term drift findings for data_lake-area files before a Phase-3 ratchet.
authority_boundary: retrieval_only
open_next:
  - docs/migration/orca_second_pass_consolidation_plan_v0.md
stale_if:
  - Any data_lake-area file is moved, renamed, or deleted after this proposal is written (inbound ref counts change).
  - A successor contract supersedes one of the three authority/ files (re-check inbound refs then).
```

# Phase-2 W3a Proposal — data_lake

## Summary

Files scanned: 5 (README.md + 3 authority/ + 1 workflows/)
Deletion candidates: 0 high / 0 medium / 0 low
Ontology findings: 0

## A. Deletion candidates

None — area is lean.

Every file in `orca/product/spines/data_lake/` carries live, unresolved inbound
references from governed areas outside this spine. The spine was populated by the
R2 data-lake move pass (2026-06-18); all five files are the canonical target
locations for their content. Evidence per file:

**`orca/product/spines/data_lake/README.md`**
Inbound refs (4):
- `.agents/workflow-overlay/artifact-folders.md:365` — listed as spine front-door
- `.agents/workflow-overlay/artifact-folders.md:406` — second listing
- `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md:18` — binding authority pointer
- `docs/migration/repo_structure_data_lake_r2_v0/moved_paths_index.md:17` — move record destination
(Note: `docs/migration/data_lake_spine_first_migration_plan_v0.md:154` is a migration plan
reference, also live.)
Not a deletion candidate: active spine front-door; directly named in overlay and binding decision.

**`orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md`**
Inbound refs (external to this spine):
- `docs/decisions/orca_data_lake_spine_promotion_binding_v0.md:124` — promotion binding cite
- `docs/migration/data_lake_spine_first_migration_plan_v0.md:114` — migration table destination
- `docs/migration/data_lake_spine_first_migration_inventory_v0.md:20` — inventory destination
- `docs/migration/repo_structure_data_lake_r2_v0/moved_paths_index.md:26` — move index destination
- `docs/migration/repo_structure_data_lake_r2_v0/harvest_data_lake.py:37` — harvest script target
(Additional intra-spine refs from storage_contract and attachment_record_implementation_contract.)
Not a deletion candidate: the parent logical lake contract; active external refs; no successor.

**`orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md`**
Inbound refs (external):
- `docs/migration/data_lake_spine_first_migration_plan_v0.md:115` — migration table destination
- `docs/migration/data_lake_spine_first_migration_inventory_v0.md:19` — inventory destination
- `docs/migration/repo_structure_data_lake_r2_v0/moved_paths_index.md:27` — move index destination
- `docs/migration/repo_structure_data_lake_r2_v0/harvest_data_lake.py:38` — harvest script target
(Intra-spine refs from core_contract and attachment_record_implementation_contract.)
Not a deletion candidate: non-selecting storage contract completing the blocker-1/2 directions; active external refs; no successor.

**`orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md`**
Inbound refs (external):
- `docs/migration/data_lake_spine_first_migration_plan_v0.md:116` — migration table destination
- `docs/migration/data_lake_spine_first_migration_inventory_v0.md:107` — inventory destination
- `docs/migration/repo_structure_data_lake_r2_v0/moved_paths_index.md:28` — move index destination
- `docs/migration/repo_structure_data_lake_r2_v0/harvest_data_lake.py:39` — harvest script target
(Intra-spine refs from storage_contract.)
Not a deletion candidate: implementation-facing contract for storage blocker-1; active external refs; no successor.

**`orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md`**
Inbound refs (external):
- `docs/workflows/ecr_spine_submap_v0.md:67,76` — cross-layer mechanics map pointer (2 lines)
- `docs/workflows/data_capture_spine_consolidation_map_v0.md:58,205` — consolidation map (2 lines)
- `docs/migration/orca_second_pass_consolidation_plan_v0.md:135,224,226` — consolidation plan (3 lines)
- `orca/product/spines/capture/core/source_families/retail_pdp/retail_pdp_typed_envelope_probe_v0.md:16` — open_next pointer
- `docs/migration/spine_first_target_move_table_v0.md:257` — move table destination
- `docs/migration/data_lake_spine_first_migration_plan_v0.md:19,117` — migration plan (2 lines)
- `docs/migration/repo_structure_data_lake_r2_v0/moved_paths_index.md:29,30` — move index destinations
- `docs/migration/repo_structure_data_lake_r2_v0/harvest_data_lake.py:40,63,65` — harvest script (3 lines)
- `docs/migration/capture_spine_source_capture_migration_inventory_v0.md:145` — inventory cite
Not a deletion candidate: canonical logical mechanics map; superseded the transitional
`orca/product/shared/data_lake_mechanics/` copy (as noted in the README); heavily referenced
by live workflow submaps in docs/workflows/.

## B. Ontology / doc-term findings

Clean.

Methodology: scanned all 5 `.md` files in `orca/product/spines/data_lake/` for
multi-hump CamelCase tokens per the `check_doc_terms.py` algorithm (>=2 humps,
head-noun matched against SSOT head nouns: Caller, Event, Packet, Unit, Vector).

Tokens found and classification:

- `SourceCapturePacket` — KNOWN alias (runtime_binding for CapturePacket in ontology.yaml). Correct usage.
- `SourceCaptureSlice` — head noun "Slice"; not an ontology head noun; classified IGNORE. Not a finding.
- `FamilyDetailBase` — head nouns "Detail" / "Base"; not ontology head nouns; classified IGNORE. Not a finding.
- `PreservedFile` — head noun "File"; not an ontology head noun; classified IGNORE. Not a finding.

Deprecated / legacy terminology check: The term "typed-envelope" / "typed extension
envelope" appears in these files (storage_contract:65,86,317; core_contract:193,212;
attachment_record_implementation_contract:110; mechanics_map:28,94) as explicitly
acknowledged historical terminology. The storage contract (line 65) directly instructs
"Historical 'typed extension envelope' wording does not become the target storage name;
in this lane, use Attachment Record." These usages are proper citations of the superseded
term — they are not accidental drift and require no fix. The active target term
"Attachment Record" is consistently used.

No new-term candidates, no non-SSOT ontology-shaped coinages, no deprecated terms
used without citation.
