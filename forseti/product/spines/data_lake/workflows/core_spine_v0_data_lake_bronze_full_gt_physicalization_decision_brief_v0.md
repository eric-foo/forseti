# Core Spine v0 Data Lake Bronze Full-GT Physicalization Decision Brief v0

```yaml
retrieval_header_version: 1
artifact_role: Data Lake workflow/decision-request record
scope: >
  Post-PR-555 physicalization decision brief for the Bronze MGT to full-GT lane:
  decide the Attachment Record body-layout/backend relationship first, then
  retention/lawful-erasure/backend lock-in, before implementation or third-proof
  expansion.
use_when:
  - Continuing Bronze full-GT planning after PR #555 and the next-material-decisions packet.
  - Preparing an ADR or owner decision on Attachment Record physicalization.
  - Checking that backend convenience is not selecting AR layout, retention, lawful erasure, or full-GT posture.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
supersedes:
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md
stale_if:
  - A later accepted authority selects Attachment Record body layout, backend, retention, lawful erasure, Manifest v2, or a full-GT path.
  - The Storage, Attachment Record, Physicality Location, Write-Boundary, Raw Admission, or Derived Layout contract changes the relevant physicalization boundary.
  - Bronze full-GT proof/CI work starts before this brief's two gates are adjudicated or explicitly deferred.
```

## Status

`PHYSICALIZATION_DECISION_BRIEF_RECORDED_V0`.

This is a planning and owner-decision brief. It is not implementation
authorization, validation, readiness, backend selection, storage-engine
selection, Manifest v2 selection, sidecar/member layout selection,
retention/lawful-erasure policy, migration authority, third-proof authority, or
a Bronze full-GT declaration.

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom data_lake physicalization S3
  edit_permission: docs-write
  target_scope: >
    Data Lake Bronze full-GT physicalization planning after PR #555; no runtime
    implementation, backend selection, third proof, or full-GT claim.
  dirty_state_checked: yes
  blocked_if_missing: >
    Re-read the storage, Attachment Record, physicality-location,
    write-boundary, raw-admission, derived-layout, and next-material-decision
    sources before making strict or actionable physicalization claims.
```

## Supersession Boundary

This brief supersedes
`core_spine_v0_data_lake_bronze_full_gt_next_material_decisions_v0.md` as the
active continuation anchor only. The older packet remains useful as historical
source inventory and A-D batching context, but it should not be used to start
runtime implementation, a backend selection, or third-proof work without this
brief's gates.

PR #555 patched the review-returned F1/F2 gaps in the deterministic inventory
test: physicalization-coupled non-raw touchpoints such as `record_path`,
`lane_dir`, `is_record_set_complete`, `inspect_catalog`, and
`catalog_coverage_census` are now included, and inventory enumeration is
tracked-source based rather than scratch-directory based. That closes the test
coverage gap; it does not select a physical architecture.

## Decision In One Screen

The next material decision is not "which storage is easiest to build." It is:

```text
Gate 1: choose or explicitly defer the Attachment Record body relationship.
Gate 2: choose or explicitly defer the retention/lawful-erasure posture before
        any backend creates lock-in.
Only after both gates are answered or consciously deferred may implementation
or third-proof expansion proceed.
```

The storage backend must prove the architecture. It must not choose the
architecture.

## Gate 1 - Attachment Record Body Layout / Backend Relationship

Question:

Which physical relationship binds a compact Attachment Record entry to an
immutable, hash-checkable body while preserving public Bronze/Silver
re-resolution and avoiding private packet-path inference?

Already constrained by accepted contracts:

- Attachment Records are compact manifest or manifest-equivalent keyed entries
  pointing to immutable, hash-checkable source-family payload bodies.
- Bodies may later be packet members, hash-pinned sidecars, packet-bundle
  members, or equivalent immutable packet material.
- Loose sidecars, mutable canonical body rows, new lake-core source-family
  fields, and Availability Index authority are rejected shapes.
- Public helper surfaces must still let Silver resolve and hash-check AR-backed
  raw refs without reading private folder semantics.

Minimum Gate 1 output:

1. The body key: packet id, optional slice/file/attachment key, family, kind,
   schema version, replay/version pins, and body reference.
2. The `hash_basis`: exactly which bytes are hashed and how a reader verifies
   them.
3. The physical relationship: packet member, hash-pinned sidecar under the
   external data root, external immutable blob/row, or explicit deferral.
4. The public read surface: how `source_surface_catalog_rows`,
   `load_attachment_record_body`, or successors continue to resolve bodies.
5. The authority split: generated catalog rows, Attachment Record rows, and
   indexes remain rebuildable read surfaces, not raw authority or private
   physical-layout contracts.
6. The rebuild rule: indexes remain rebuildable and non-authoritative.
7. The replay/migration implication: incumbent direct fields stay
   legacy-readable; pinned packets are not mutated in place.
8. The rejected shapes: what future implementers must not infer from this
   decision.

Gate 1 option ledger:

| Option | Shape | Why it may win | Why it may lose |
| --- | --- | --- | --- |
| G1-A Incumbent preserved-body AR posture | Keep generated AR entries over preserved raw packet bodies while layout/backend stay deferred. | Lowest lock-in; matches current Bronze/Silver proof path and MGT posture. | Not full physicalization; generated catalog can be overread as authority. |
| G1-B Packet-member or packet-bundle body | Make AR bodies explicit immutable packet material with compact manifest/index entries. | Strongest raw-authority fit; hash basis and packet identity stay local. | Requires manifest/index serialization and replay/migration design. |
| G1-C Hash-pinned sidecar body under external data root | Keep compact entry separate from immutable body material in `attachments/` or equivalent. | Separates large bodies from compact entries while preserving external-root boundary. | Sidecars become unsafe unless keyed, indexed, and hash-checkable. |
| G1-D External blob/database row as body | Store body in object/database/backend material with immutable hash-checked reference. | May solve scale or operational constraints. | Highest lock-in; unacceptable before Gate 2 proves erasure/retention posture. |

Recommended posture for the next lane:

Carry G1-B/G1-C as the live comparison. Keep G1-A as the current MGT fallback.
Do not select G1-D unless Gate 2 first proves the backend can preserve lake
immutability, append-only history, rebuildability, and lawful-erasure posture.

## Gate 2 - Retention / Lawful-Erasure / Backend Lock-In

Question:

Which retention and lawful-erasure constraints must be true before AR body
layout or backend choice becomes hard to reverse?

Already constrained by accepted contracts:

- Raw packet material is immutable and create-only.
- Derived and acknowledgement records are append-only.
- `indexes/` is rebuildable and non-authoritative.
- By-key discovery is authority before any queue/event runtime.
- The lake does not clean, dedupe, score, judge, schedule, retry, route, or call
  downstream lanes.
- Real operational data lives under an operator-configured external data root
  unless a later backend decision explicitly supersedes that model.
- Retention and lawful erasure cannot be hidden inside storage-engine choice.

Minimum Gate 2 output:

1. Whether lawful erasure is a current hard requirement or an accepted residual.
2. Whether deletion means unavailable/tombstoned, superseded, crypto-shredded,
   backend-native lifecycle deletion, or another owner-approved posture.
3. Which material can remain immutable history and which material may need
   key-separated erasure.
4. Whether backend-native retention controls are allowed to carry policy, and
   what deterministic tests must prove.
5. What backend choices are forbidden because they make the policy impossible
   or too expensive to reverse.
6. If the answer is deferral, the accepted-residual record: residual scope,
   claim ceiling, forbidden backend classes or operations while deferred, and
   revisit triggers that force a retention/lawful-erasure ADR before lock-in.

Gate 2 option ledger:

| Option | Shape | Why it may win | Why it may lose |
| --- | --- | --- | --- |
| G2-A Defer retention/erasure as accepted residual | Keep current immutable/posture-only model and block full-GT physicalization. | Honest if no owner/legal erasure requirement is ready. | Cannot support full-GT physicalization or backend lock-in. |
| G2-B Append-only tombstone/supersession | Express unavailability, correction, or replacement as new records. | Fits current lake invariants and re-derive-not-migrate posture. | Does not satisfy true lawful erasure by itself. |
| G2-C Key-separated encrypted body posture | Put erasure-sensitive body bytes behind explicit key separation and crypto-shred semantics. | Candidate if erasure becomes real while retaining append-only metadata. | High design and backend lock-in; needs owner/legal decision and tests. |
| G2-D Backend-native retention controls | Use object/database/WORM/lifecycle controls deliberately. | Operationally strong when selected with policy up front. | Dangerous if convenience-led; can make architecture irreversible. |

Recommended posture for the next lane:

Do not pick a backend until the owner answers whether lawful erasure is a real
current requirement or an accepted residual. If it is a residual, keep backend
selection below full-GT claim strength. If it is a requirement, require a
separate retention/lawful-erasure ADR before backend implementation.

## Backend Candidate Discipline

Backend candidates are implementation mechanisms, not architecture owners.

| Candidate | Allowed use | Hard stop |
| --- | --- | --- |
| Filesystem external root | Incumbent MGT substrate for raw/attachments/derived/acks/indexes; good for by-key proof and low lock-in. | Do not claim full GT merely because path grammar works. |
| DuckDB or SQL-capable embedded query lens | Rebuildable index/query aid over committed material. | Must not become the canonical raw body store or authority for by-key truth. |
| Object/blob store | Immutable hash-addressed body material if keying, refs, and erasure posture are explicit. | Do not select before Gate 2 if lawful erasure or WORM policy matters. |
| Conventional database | Metadata/index store or immutable-versioned body store only if create-only and hash-checkable. | Reject if mutable rows become the only canonical raw body. |
| Hybrid | Acceptable only if each slot's authority is explicit. | Reject if the split hides which store is authoritative. |

## Decision Request

The next owner call should choose exactly one:

1. **Defer physicalization.** Keep the current MGT posture, acknowledge that
   full GT remains blocked, record the accepted residuals plus forbidden
   choices and revisit triggers, and scope only non-locking CI/lake-doctor work.
2. **Proceed with Gate 1 ADR.** Decide packet-member versus hash-pinned sidecar
   versus explicit deferral while keeping backend unselected until Gate 2.
3. **Proceed with Gate 2 ADR first.** If lawful erasure or retention policy is
   load-bearing, decide that posture before any body/backend layout.
4. **Proceed with a combined physicalization ADR.** Compare body relationship,
   backend, and retention together, but do not implement until the chosen
   option proves every storage-contract invariant.

Recommended next move: option 2 unless the owner says lawful erasure is a hard
current requirement; then option 3 comes first. Option 4 is only warranted if
the owner wants to make an explicit backend call now.

## Proof / CI Boundary

Do not start a third consumer proof as a way to avoid the physicalization
choice. Third-proof work becomes material only after:

- YouTube ambiguous-AR behavior remains test-pinned or explicitly carried as a
  code-present residual.
- The materially different raw-body/AR-join test is defined against the chosen
  or deferred body relationship.
- The proof candidate exercises a different raw-body or AR-join shape, not only
  a different source-family name.

CI/lake-doctor hardening may continue only when it does not select body layout,
backend, retention, or lawful erasure by implementation convenience.

## Full-GT Distance

After PR #555, Bronze is stronger as an MGT / typed raw-truth retrievability
base. It is still not full GT.

Remaining material blockers before any full-GT claim:

- Gate 1 body relationship selected or explicitly deferred with accepted
  residuals.
- Gate 2 retention/lawful-erasure posture selected or explicitly accepted as a
  residual, including forbidden backend operations and revisit triggers.
- Implementation scope proves write-once raw, append-only derived/ack,
  read-by-key, hash verification, public AR body resolution, and index rebuild.
- Third-proof threshold is applied only to a materially different raw-body or
  AR-join shape.
- De-correlated review runs over the final Bronze/Silver contract and code path
  before any full-GT closeout.

## Non-Claims

- Not implementation authorization.
- Not backend, engine, object store, database, DuckDB, or hybrid selection.
- Not Manifest v2, packet-member, sidecar, serialization, replay, migration, or
  cutoff selection.
- Not retention, lawful-erasure, WORM, crypto-shredding, deletion, or compliance
  posture.
- Not CI/lake-doctor implementation.
- Not third-proof authorization.
- Not validation, readiness, Silver readiness, production lake proof,
  all-source coverage, or Bronze full GT.