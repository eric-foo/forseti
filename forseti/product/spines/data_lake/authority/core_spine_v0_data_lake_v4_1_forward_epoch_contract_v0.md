# Core Spine v0 Data Lake v4.1 Forward Epoch Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: >
  Forward-only v4.1 data-lake epoch contract: archive or abandon the small
  pre-v4.1 lake rather than compatibility-migrating it, make v4.1 the only
  forward write contract, and keep the canonical raw/derived/indexes physical
  grammar while applying v4.1 Silver Vault record and retrieval shape.
use_when:
  - Initializing a new v4.1 Orca data root.
  - Auditing capture runners for forward lake-write compliance.
  - Deciding whether old lake material should be migrated, archived, or ignored.
  - Resolving confusion between medallion labels and physical folder names.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  - docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md
  - forseti-harness/data_lake/root.py
stale_if:
  - The owner rejects the clean v4.1 epoch reset.
  - A later accepted physicality contract changes the canonical folder grammar.
  - DataLakeRoot or runner implementations land a different canonical write shape.
```

## Status

`V4_1_FORWARD_EPOCH_SELECTED_V0`.

Owner direction recorded 2026-06-28: the current live lake is small enough that
preserving it is not the priority. The priority is a clean long-term shape that
compounds. Therefore v4.1 is a clean forward epoch, not a compatibility migration
of the current lake.

Correction recorded 2026-06-28: medallion terms are semantic labels, not generic
physical storage tiers. The Medallion Gold-Readiness contract explicitly says not
to collapse Orca into generic bronze/silver/gold storage tiers. v4.1 keeps the
canonical physical lake slots.

This is an architecture contract. It is not live-data migration execution,
validation, readiness, implementation completion, backend selection, client launch
approval, or permission to delete/rename an external data root without an explicit
operator action.

## Decision In One Screen

```text
Do not compatibility-migrate the old small lake.

Archive or abandon it as a legacy epoch.
Initialize a clean v4.1 root.
All forward capture packet writers must write v4.1-compatible refs.
All forward Silver/Creator Vault records and read models must use v4.1 shape.

Keep physical folder names canonical:
raw/      = Bronze label, raw evidence packets
attachments/ = optional immutable attachment bodies
derived/  = Silver Authority label, append-only semantic records
acknowledgements/ = append-only lane-owned acknowledgements
indexes/  = rebuildable retrieval, not authority

Do not add generic bronze/ silver/ gold/ storage tiers.
```

## Why This Replaces Compatibility Migration

The previous compatibility idea was useful only if old lake data had enough value
to preserve. The observed current root is small: 241 raw manifests, 343 derived
files, 0 derived-retrieval files, and no metric observations in raw manifests.

That makes a careful migration the wrong optimization. It would spend effort
carrying weak historical shape into the new foundation. The forward move is:

1. freeze or archive the old root;
2. create a new clean v4.1 root with canonical physical slots;
3. make every forward writer target v4.1 record/ref semantics;
4. recapture under the clean contract;
5. use old records only as examples or temporary fixtures when useful.

## v4.1 Physical Folder Grammar

Forward v4.1 roots use this grammar:

```text
<ORCA_DATA_ROOT>/
  .orca-data-root
  .orca-lake-epoch.json
  .staging/

  raw/
    <packet_shard>/<packet_id>/
      manifest.json
      raw/

  attachments/

  derived/
    <anchor_shard>/<raw_anchor>/<lane_namespace>/<record_id>.json
    <anchor_shard>/<raw_anchor>/<lane_namespace>/<record_set_id>.json

  acknowledgements/

  indexes/
    availability/
    derived_retrieval/
      silver_vault/
        core/
          query_tables/
          manifests/
        creator_vault/
          accounts/<platform>/<account_id>/envelope.json
          content/<platform>/<content_kind>/<content_id>/envelope.json
          query_tables/
          manifests/
```

Folder rules:

- `raw/` is raw evidence only. It is not organized by creator, product,
  platform account, reel, short, SKU, or review subject.
- `derived/` is append-only Silver authority when the record body is a v4.1
  Silver Vault record. Meaning lives in the record body, not in the path.
- `indexes/availability/` is content-free committed/readable-by-key state.
- `indexes/derived_retrieval/` is rebuildable and non-authoritative. Query
  tables and Creator Vault envelopes live here.
- No `gold/` folder is introduced by the data lake. Gold interpretation is
  Judgment-owned output and must not be created by capture, Silver, or retrieval
  writers.
- `.staging/` is operational scratch for atomic publication. A partial packet or
  record must not appear in committed raw/derived/indexes folders.

## v4.1 Root Markers

Each v4.1 root must carry the existing root marker plus an epoch marker:

```json
{
  "contract_version": "v4.1",
  "created_at": "2026-06-28T00:00:00Z",
  "label": "orca-canonical-v4-1",
  "root_uuid": "01..."
}
```

```json
{
  "lake_epoch": "v4.1",
  "epoch_policy": "clean_forward_epoch",
  "legacy_roots": [],
  "compatibility_migration": false
}
```

The existing `.orca-data-root` marker remains the root identity marker. The epoch
marker records that this root is forward v4.1 and not a compatibility migration.

## Forward Writer Obligations

Every forward Source Capture packet writer that emits a durable packet must:

- resolve an external v4.1 root fail-closed;
- write into `.staging/` first;
- publish raw packet material under `raw/<packet_shard>/<packet_id>/`;
- preserve `manifest.json`, raw files, hashes, and hash basis;
- write or rebuild a content-free availability entry under `indexes/availability/`;
- expose `--data-root` or `ORCA_DATA_ROOT` unless it is intentionally local-only
  and documented as not a lake packet writer;
- reject ambiguous output modes where both local `--output` and lake root are set;
- never write Cleaning, ECR, Judgment, or Creator Vault meaning as part of raw
  packet capture.

Every forward derived/Silver writer must:

- write append-only one-record-per-file records under `derived/`;
- keep `record_kind`, `payload_kind`, source refs, posture/value/reason coupling,
  and coverage windows according to the Silver Vault record contract;
- create correction, supersession, tombstone, and conflict as new records, never
  rewrites;
- generate retrieval views under `indexes/derived_retrieval/`, never as authority.

## Old Lake Handling

The old root should not be compatibility-migrated by default.

Allowed old-root treatments:

- rename or copy it to a legacy path such as
  `F:\orca-data-lake-legacy-20260628`;
- leave it mounted read-only as a reference sample;
- delete it only after explicit operator confirmation and backup decision;
- selectively copy tiny examples into test fixtures if a later implementation
  lane needs them.

Forbidden old-root treatments:

- rewriting old packets in place to look v4.1;
- treating old `indexes/` as forward authority;
- making v4.1 reader code carry permanent compatibility shims for the old small
  root unless a concrete test fixture requires it;
- introducing generic `bronze/`, `silver/`, or `gold/` storage tiers to make the
  folder tree look medallion-shaped.

## Relationship To Existing Contracts

The v0 Physicality Location Contract remains the owner of the external-root,
fail-closed, raw-immutable, append-only-derived, and rebuildable-index rules.
The Derived Layout + Index Rebuild Contract remains the owner of append-only
record addressing and rebuildability. The Medallion Gold-Readiness Contract
remains the owner of medallion semantics.

v4.1 changes the forward epoch and record/ref semantics. It does not replace the
canonical physical slot names.

```text
Physical slot: raw/                     Medallion label: Bronze
Physical slot: derived/                 Medallion label: Silver Authority
Physical slot: indexes/derived_retrieval/silver_vault/  Medallion label: Silver Retrieval / Creator Vault
Judgment-owned output                   Medallion label: Gold
```

## Relationship To Silver Vault

Silver Vault v4.1 authority lives under:

```text
derived/<anchor_shard>/<raw_anchor>/<lane_namespace>/<record_id>.json
```

Creator Vault and query read models live under:

```text
indexes/derived_retrieval/silver_vault/
```

Creator Vault remains generated, public-evidence-only, per-platform, and
non-Gold. Retrieval folders do not make envelopes authoritative; authority still
lives only in the append-only records that generated them.

## Acceptance Criteria

This contract is satisfied when:

1. A new v4.1 root can be initialized with the canonical folder grammar above.
2. The old lake is archived, ignored, or deleted by explicit operator decision,
   not compatibility-migrated by default.
3. Every forward packet writer is audited against v4.1 root behavior.
4. Every forward packet writer that remains in scope can write raw packets and
   content-free availability.
5. Silver Vault records and read models use `derived/` and
   `indexes/derived_retrieval/silver_vault/` respectively.
6. Gold output is impossible to create from capture, Silver, or retrieval writers.
7. Tests no longer assume unqualified legacy `raw/<packet_id>` for v4.1 roots;
   sharding and availability refs are explicit.

## Non-Claims

Not a live archive/delete operation. Not validation, readiness, or implementation
completion. Not a storage backend, queue, scheduler, or graph/vector engine
selection. Not approval to write to or delete `F:\orca-data-lake` without an
explicit operator action. Not a decision that old lake data is useless forever;
it says old data is not worth shaping the forward contract around.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Data Lake v4.1 is selected as a clean forward epoch: old small lake material
    is archived/abandoned rather than compatibility-migrated by default; new
    roots keep canonical raw/attachments/derived/acknowledgements/indexes
    physical slots; medallion names remain semantic labels, not generic
    bronze/silver/gold storage tiers; and every forward capture packet writer
    must be audited for v4.1-compatible lake refs before Silver Vault
    implementation relies on it.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
    - workflow_authority
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_v4_1_forward_epoch_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
    - docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/artifact-folders.md
    - docs/workflows/data_capture_spine_consolidation_map_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  intentionally_not_updated:
    - path: AGENTS.md
      reason: >
        AGENTS.md carries project behavior and routes Orca project facts to the
        overlay/docs; it does not enumerate data-lake folder grammar.
    - path: forseti-harness/data_lake/root.py
      reason: >
        Runtime implementation is intentionally not patched in this docs turn;
        the parallel audit handoff is updated to make v4.1-compatible runner
        writes the next verification target.
  stale_language_search: >
    rg -n "bronze/|silver/|gold/|Do not rename folders|indexes/derived_retrieval/silver_vault"
    forseti/product/spines/data_lake docs/workflows/capture_spine_runner_data_lake_dump_audit_handoff_v0.md
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not live external data-root migration
    - not permission to delete old lake data without explicit operator action
```
