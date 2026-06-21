# Orca Data Lake Physicality Architecture Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact (deep-thinking / external architecture reasoning)
scope: >
  Paste-ready prompt for a no-repo ChatGPT Pro architecture pass on Orca Data
  Lake physicality: where raw packets, attachments, availability indexes,
  derived records, acknowledgements, and gold-ready receipts should physically
  live, without authorizing backend, queue, or implementation work.
use_when:
  - Asking an external model with no repo access to reason about Data Lake physical storage shape.
  - Comparing physical homes for raw packets, attachments, indexes, and derived records.
  - Stress-testing by-key discovery, append-only records, rebuildable indexes, and queue deferral.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
  - orca/product/spines/capture/packet_schema/source_capture_tenant_payload_attachment_boundary_v0.md
stale_if:
  - A later owner decision selects storage engine, manifest version, sidecar layout, queue/runtime, or migration path.
  - Data Lake raw/attachment/derived-record ownership changes.
  - The physicalization blockers in the Data Lake contracts are closed or replaced.
```

```yaml
orca_prompt_preflight:
  output_mode: file-write + paste-ready-chat copy
  template_kind: deep-thinking
  edit_permission: docs-write
  target_files:
    - docs/prompts/deep-thinking/orca_data_lake_physicality_architecture_prompt_v0.md
  workspace: C:\tmp\orca-data-lake-mgt-target
  branch: codex/data-lake-mgt-target
  dirty_state: clean before prompt authoring
  reviews: none bound; this is a prompt artifact for external reasoning
  doctrine_change: none; prompt only
  destinations:
    prompt_artifact_path: docs/prompts/deep-thinking/orca_data_lake_physicality_architecture_prompt_v0.md
    downstream_output: chat-only response from ChatGPT Pro
```

```yaml
thread_operating_target_continuity:
  carried_forward: yes
  reason: same_workstream
  changed_from_input: no
  lifecycle_status: active_thread_local
thread_operating_target:
  activation_policy: latest_non_blocked_goal_frame_wins
  lifecycle_status: active_thread_local
  optimize_toward: >
    Establish a thread-local capability target for Orca Data Lake MGT that
    links bronze/silver/gold, admission, tags, lineage, passive availability,
    and visible limitations without selecting implementation.
  output_fit_check: >
    The next produced answer or artifact must clarify physical homes,
    by-key discovery, raw preservation, attachment records, derived result
    attachment, rebuildable indexes, and visible limitations without
    authorizing backend, queue, scheduler, or runtime work.
  drift_guard: >
    Do not convert the MGT goal into implementation planning, backend build,
    queue design, person-dossier design, or artifact completion as a proxy for
    capability fit.
  conflict_behavior: call_out_conflict_before_proceeding
```

## Paste-Ready Prompt

You are ChatGPT Pro. This is a no-repo source-capsule architecture reasoning pass for Orca. Do not claim source readiness beyond this capsule. Do not invent implementation facts. Do not recommend code, migrations, queue/runtime work, scraper/crawler changes, dashboards, deployment, or validation/readiness. You may compare physical architecture options and recommend an owner decision frame.

## Objective

The owner wants a Data Lake physicality decision frame: where Orca should physically store raw packets, source-family attachments, passive availability facts, append-only derived records, acknowledgement facts, and later gold-ready assembly receipts.

The goal is to decide the smallest complete physical architecture direction that supports Orca's Data Lake MGT target while preserving visible limitations:

- raw truth is preserved;
- all downstream records remain keyed to raw;
- by-key discovery works before any queue;
- indexes are rebuildable;
- derived records are append-only;
- the lake does not become smart about meaning;
- no backend, queue, scheduler, or runtime implementation is authorized by this pass.

## Source Capsule

Use only this source capsule as the repo context.

### Mini-God-Tier And SCI Constraints

Mini-god-tier means an owner-invoked capability target: most of the useful capability of a maximal design at a fraction of its cost and lock-in, with visible limitations named. It is not validation, readiness, production fitness, or a scope-expansion license.

Smallest Complete Intervention means the recommended direction must fully satisfy the current architecture need with the narrowest sufficient commitment. Do not under-specify the parts that determine correctness, but do not choose speculative infrastructure.

### Data Lake Core Contract

The Data Lake is the warehouse and filing system for captured source material. It preserves raw `SourceCapturePacket` bundles, stable IDs, hashes, manifests, and by-key availability. It does not clean, normalize, identify entities, decide source value, or run downstream lanes.

The lake owns:

- raw packet bundle preservation;
- stable handle family: `packet_id`, `slice_id` when slice-scoped, preserved file IDs, `sha256`, and `hash_basis`;
- manifest/reference rules needed to know which raw files and payloads belong to a packet;
- by-key findability for committed packets, slices, files, and attached payload references;
- source-family payload attachment rules at the core boundary;
- logical attachment points for downstream derived results keyed to packet, slice, or file references;
- a content-free availability fact after raw commit.

The lake must not own ECR/SCR semantics, Cleaning, Judgment, canonical identity, cross-packet dedupe, downstream scheduling, retry, routing, or direct calls into downstream lanes.

By-key discovery is contract authority. A queue may later optimize notification, but it is not the source of truth and must not become a lake-owned push/router/caller.

Downstream outputs attach as logical append-only derived records keyed to raw. Their physical home has been deferred, but the logical rule is fixed.

### Storage Contract

The storage contract names five dumb record-kind slots:

1. Raw Packet Store: preserves raw `SourceCapturePacket` bundles, stable packet/slice/file handles, hashes, and hash basis. It must not become cleaned source truth, canonical identity, or mutable packet history.
2. Attachment Record: carries source-family payload body plus packet/slice/file identity, family, kind, schema version, replay pins, and absence/refusal/residual posture. It must not carry cleaned values, dedupe decisions, credibility labels, Judgment labels, or downstream-use strength.
3. Availability Index: records only that packet/slice/file material is committed and readable by stable keys with checkable refs. It must not become an event bus, scheduler, lane router, retry gate, priority system, or success tracker.
4. Derived Result Store: holds append-only lane-owned derived records keyed to raw, including projection receipts, ECR integrity records, SCR content records, Cleaning ledgers, Judgment outputs, and future gold-ready assembly receipts. It must not become a second raw source of truth, merged cross-kind blob, or rewritten/deleted derived history.
5. Acknowledgement Log: holds append-only lane-owned completion or acknowledgement facts keyed to raw. It must not become lake-consumed control flow for scheduling, gating, retrying, or calling another lane.

The contract records a direction for Attachment Records: manifest-indexed immutable attachment bodies. Exact serialization, sidecar/member layout, manifest version, backend, and migration remain deferred. Historical docs call this the logical typed-envelope boundary.

Availability indexes must be rebuildable from committed packet/attachment keys and hashes. Replacing or correcting an Attachment Record writes a new record; old records are not rewritten in place. Retention and lawful-erasure policy remain later physicalization constraints.

### Current Physicalization Gate

Do not implement storage, manifest changes, Attachment Record serialization, projection cache, queue runtime, derived-record persistence, or acknowledgement persistence until these blockers close:

1. Choose the Attachment Record physical representation: manifest child, immutable sidecar, hash-pinned bundle member, or another immutable/checkable form.
2. Preserve the accepted incumbent-field fate: legacy-readable transitional fields do not become precedent for new direct source-family fields.
3. Preserve the no-new-direct-source-family-field direction.
4. Assign enforcement for write-once raw, no-cleaning-in-lake, append-only derived results, and no-new-core-field pressure to deterministic write or tool boundaries where possible.
5. Choose the physical home and write boundary for projection receipts, ECR records, SCR records, Cleaning ledgers, Judgment outputs, future gold-ready assembly receipts, and downstream completion/acknowledgement facts.
6. Preserve by-key discovery as authority before any runtime event or queue engine is built.

This pass may reason about these blockers but must not claim they are closed unless the output explicitly states what owner decision would be needed to close each one.

### Related Medallion Semantics Context

The parallel non-physical lane is the Data Lake Medallion Semantics / Gold-Readiness lane. It is deciding meanings and layer boundaries:

- Bronze: raw captured packets and preserved source material.
- Silver: projection, ECR/SCR, Cleaning, and mechanical derived features.
- Pre-gold or gold-ready: spike alerts, movement alerts, and decision-bounded evidence assemblies.
- Gold: Judgment-owned interpretation only.

Accepted direction so far:

- User-facing simple vocabulary may use `Spike Alert` or `Movement Alert`.
- Strict meaning is "outside usual range" or "usual-range threshold crossed."
- First precomputed candidate class should be source-object movement, such as a video/post/product/review thread spiking outside its usual range.
- Actor/commenter/reviewer timing retrieval is valuable for decision integrity and astroturfing inspection, but must remain on-demand, exact namespace-scoped, non-dossier, and non-Judgment.
- Candidate records must not claim botting, fake review, paid activity, coordination, manipulation, virality, credibility reduction, or exclusion.

This physicality pass should support that lane without deciding its semantics.

## Decision Question

What physical architecture direction should Orca adopt first so that the Data Lake has a real place for raw data, attachments, passive availability, derived records, and gold-ready receipts, while keeping the design MGT and SCI?

## Options To Compare

Compare at least these options, and add a better hybrid only if it is materially better:

1. Current packet directories plus a rebuildable by-key index.
2. A packet_id-addressed canonical root where each admitted packet has a stable directory or object prefix.
3. Raw packet bundle as canonical, with manifest-indexed immutable attachment bodies as child files or bundle members.
4. Sidecar-based attachment and derived-record files beside packet material.
5. Separate object/file homes for raw, attachments, indexes, derived records, and acknowledgements, joined only by stable keys.
6. Database-first storage for metadata/indexes with raw bytes/files in packet/object storage.
7. Any hybrid that preserves raw immutability, append-only derived records, rebuildable indexes, and low lock-in better than the above.

## Questions To Answer

1. What should be the first physical decision Orca makes: admitted packets stay in current packet dirs with a rebuildable by-key index, or introduce a packet_id-addressed canonical root? Evaluate SCI and MGT.
2. Where should raw packet bundles live physically, and what must be immutable/checkable about them?
3. Where should Attachment Records live physically: manifest child, immutable sidecar, hash-pinned bundle member, or another form? What is the smallest complete choice?
4. How should the Availability Index be represented so it is useful but rebuildable and not a queue/router?
5. Where should Derived Result Store records live physically, including projection receipts, ECR/SCR records, Cleaning ledgers, Judgment outputs, spike/movement alerts, gold-ready assembly receipts, and future non-Judgment candidate records?
6. Should derived records share one physical home with typed record kinds, or separate homes by lane/record kind? What reduces lock-in while keeping retrieval practical?
7. Where should Acknowledgement Log facts live physically, and how do we prevent them becoming lake-consumed control flow?
8. What keys, path shapes, or object-prefix patterns are necessary for by-key discovery without choosing a specific backend?
9. What should be materialized now versus deferred? Include manifest version, serialization, storage engine, database, queue, cache, migration, retention, and lawful erasure.
10. How should the physicality decision support the Medallion Semantics lane without importing Judgment or person-dossier behavior?
11. What physicality blockers must close before implementation or fused work?

## Required Output Format

Return these sections:

1. Architecture Read
2. Recommendation
3. Physical Record Homes
4. Current Packet Dirs vs Packet-ID Canonical Root
5. Attachment Record Representation
6. Availability Index Shape
7. Derived Result Store And Gold-Ready Receipts
8. Acknowledgement Log
9. By-Key Discovery And Rebuildability
10. SCI/MGT Tradeoffs
11. Interaction With Medallion Semantics Lane
12. Owner Decisions Before Implementation
13. Visible Limitations

Use the labels `recommended`, `viable-but-risky`, `reject`, `deferred`, and `source-gap` where useful.

Do not write code. Do not choose a concrete backend. Do not authorize queue/runtime work. Do not claim validation, readiness, production fitness, or implementation permission.
