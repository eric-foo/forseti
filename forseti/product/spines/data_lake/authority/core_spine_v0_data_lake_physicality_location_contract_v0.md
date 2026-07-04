# Core Spine v0 Data Lake Physicality Location Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: >
  Physicality-location contract for Forseti's Data Lake: the repo-vs-operational-data
  boundary, the operator-configured external data root (FORSETI_DATA_ROOT, with legacy ORCA_DATA_ROOT compatibility), the v0
  logical directory grammar (raw/ attachments/ derived/ acknowledgements/ and a
  split indexes/availability + indexes/derived_retrieval), the location invariants
  (raw immutable, derived/ack append-only, indexes rebuildable), durable stored
  record names, fail-closed root resolution, and accepted residuals. This is a
  location and directory-grammar contract, not a storage-engine or backend choice.
use_when:
  - Deciding where Forseti operational data physically lives versus what stays in the Git repo.
  - Scoping data-root configuration, fail-closed resolution, or directory placement.
  - Naming a durable Data Lake record and checking it does not leak gold/Judgment/actor semantics.
open_next:
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_write_boundary_enforcement_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - docs/decisions/orca_mini_god_tier_doctrine_v0.md
downstream_consumers:
  - physical data-lake storage/implementation lane
  - data-root configuration/runtime lane
  - spike alert / source-object movement candidate-record lane
  - decision evidence assembly lane
  - ECR/SCR/Cleaning derived-record lanes
stale_if:
  - A later accepted storage, manifest, sidecar, queue, serialization, or schema decision changes the location boundary.
  - The Data Lake Core, Storage, or Medallion Gold-Readiness contract changes the lake-owned boundary.
  - A later owner decision selects a database/object-store backend that replaces the filesystem-root location model.
  - The owner changes the external-data-root boundary or the fail-closed resolution rule.
authority_boundary: retrieval_only
```

## Status

`TARGET_PHYSICALITY_LOCATION_CONTRACT_RECORDED_V0; GATE1_BODY_HOME_RESOLVED_V0`.

This is a planning and architecture contract. It is not implementation authority,
validation, readiness, backend selection, storage-engine selection, queue design,
serialization, schema finalization, or migration authority.

## v4.1 Forward Epoch Note

This contract records the canonical location boundary and slot semantics. Its
external-root, fail-closed, raw-immutable, append-only-derived, and rebuildable-
index rules carry forward into v4.1.

The v4.1 forward-epoch contract changes the epoch policy and record/ref shape; it
does not replace canonical physical folder names with generic medallion storage
tiers. Medallion terms remain semantic labels.

Forward v4.1 committed slot names remain:

```text
raw/ attachments/ derived/ acknowledgements/ indexes/
```

Operational markers and `.staging/` are specified by the v4.1 forward-epoch
contract. Do not introduce `bronze/`, `silver/`, or `gold/` as generic
data-lake storage folders unless a later accepted physicality contract
explicitly supersedes this rule.
Owner direction recorded 2026-06-21:

- Real Forseti operational data does not live in the Git repository; it lives under a
  separate operator-configured external data root.
- The pointer is generalized: `FORSETI_DATA_ROOT=<operator-configured external data
  root>`. Legacy `ORCA_DATA_ROOT` remains accepted as a compatibility fallback.
  The owner's current local example is `F:\orca-data` (a portable drive);
  the drive letter and medium are deployment choices, not part of the contract.
- The v0 directory grammar is accepted as a logical grammar, with `indexes/` split
  into a content-free `availability/` subslot and a rebuildable, non-authoritative
  `derived_retrieval/` subslot.
- Root resolution is fail-closed.
- Durable record names are deliberately boring and mechanical; no stored record
  carries a `GoldReady` prefix. "Gold-ready" survives only as a prose layer name.
- `DecisionEvidenceAssemblyProfile` is a versioned definition that lives in the Git
  repo; produced records pin the profile version they ran under.

## Purpose

This contract locks **where** Data Lake material physically lives and how the repo
points at it, so later implementation cannot drift the boundary, hard-code a drive,
silently write into the repo, or let a convenience index become lake authority.

It settles the location boundary and directory grammar. It does not itself select
the storage engine, serialization, manifest version, cache, queue, scheduler,
runtime, or migration mechanics. Engine/backend selection now belongs to the
Storage Contract physicalization boundary; if a selected backend replaces the
external-root model, this contract must be explicitly superseded.

## The Boundary In One Screen

```text
The Git repository owns code, schemas, contracts, tests, small fixtures,
example manifests, and config templates.
Real operational data lives under one operator-configured external data root.
The repo points at the root through configuration (FORSETI_DATA_ROOT; legacy ORCA_DATA_ROOT accepted).
The root resolves OUTSIDE the repo working tree, or tools fail closed.
Raw stays immutable; derived and acknowledgement records stay append-only;
indexes stay rebuildable and carry no authority.
```

The lake is strict about where bytes land. It is not smart about what they mean.

## Physical Root Contract

- The boundary is a **location contract**, not itself a storage-engine choice. A
  directory grammar remains acceptable; engine/backend selection is delegated to
  the Storage Contract physicalization boundary.
- A single configured root pointer locates all operational data. The medium
  (internal disk, fixed letter, portable drive, future network path) is an operator
  deployment choice; the contract names no drive letter and requires no HDD.
- Location invariants bound to the root:
  - **raw is immutable / write-once**; raw bytes, hashes, and packet identity are
    never rewritten by derived lanes;
  - **derived and acknowledgement records are append-only** — corrected by writing a
    new record, never by rewriting prior records in place; each epistemic kind stays
    a sibling, not a merged blob;
  - **all of `indexes/` is rebuildable** from committed packet/attachment keys and
    hashes, and carries no authority.
- No semantics in the tree: directory structure encodes no actor/profile/dossier
  shape, cleaned values, canonical identity, gold, or Judgment.

## Directory Grammar (v0 logical)

```text
<FORSETI_DATA_ROOT>/
  raw/                       # Raw Packet Store      — immutable, write-once
  attachments/               # Attachment Record     — immutable, hash-checkable*
  derived/                   # Derived Result Store  — append-only, keyed to raw
  acknowledgements/          # Acknowledgement Log   — append-only, keyed to raw
  indexes/
    availability/            # Availability Index    — content-free committed/
                             #   readable-by-key state; rebuildable; NOT authority
    derived_retrieval/       # lane-owned analytical retrieval aids — rebuildable,
                             #   non-authoritative; NOT truth / actor history / dossier

* attachment bodies land as packet members under raw/<packet_shard>/<packet_id>/
  by default (Gate 1 body-layout ADR, owner-ratified 2026-07-02); the
  attachments/ slot is reserved, usable only through a future ADR on that ADR's
  named reopen trigger (a body that genuinely cannot land inside its packet).
```

These names are **logical slot homes**, not a frozen path schema. `raw/<packet_id>/...`
is the **target raw layout direction**, gated on packet-admission and key-rule
decisions; it is not locked here.

## Directory Slot Contract

| Slot | Owns (lake-side) | Must not become |
| --- | --- | --- |
| `raw/` | Raw Packet Store: immutable `SourceCapturePacket` bundles, stable packet/slice/file handles, `sha256`, `hash_basis`. | Cleaned truth, canonical identity, mutable packet history. |
| `attachments/` | RESERVED (Gate 1 body-layout ADR, 2026-07-02): no default occupant — Attachment Record bodies land as packet members under `raw/`. The slot opens only through a future ADR on the sidecar reopen trigger; any future occupant stays immutable/hash-checkable and keyed to packet/slice/file. | Cleaned values, dedupe/credibility/Judgment labels, downstream-use strength, or a second default body home without a ratified ADR. |
| `derived/` | Derived Result Store: append-only lane-owned derived records keyed to raw; each epistemic kind a sibling. | Second raw source of truth, merged cross-kind blob, rewritten/deleted history. |
| `acknowledgements/` | Acknowledgement Log: append-only lane-owned completion/ack facts keyed to raw. | Lake-consumed control flow for scheduling, gating, retry, or calling a lane. |
| `indexes/availability/` | Availability Index: content-free committed/readable-by-key state with checkable refs; rebuildable. | Analytical reverse index, event bus, scheduler, router, retry gate, priority/success tracker. |
| `indexes/derived_retrieval/` | Rebuildable, non-authoritative lane-owned retrieval aids (e.g., timing/cadence views), always reconstructible from `derived/` + raw. | Source of truth, persistent actor history, dossier, or lake authority. |

## Stored Record Vocabulary

Durable record names are deliberately boring and mechanical so future work cannot
read gold, Judgment, or actor meaning into a storage label. Field-level schema and
physical representation remain deferred.

| Layer / role | User-facing label | Durable stored name | Home |
| --- | --- | --- | --- |
| Pre-gold movement (threshold crossing) | `Spike Alert` / `Movement Alert` | `SourceObjectMovementThresholdCrossingRecord` | `derived/` |
| Decision evidence bundle (transient) | — | `DecisionEvidenceAssemblyView` | computed on demand; cacheable rebuildably under `indexes/derived_retrieval/` |
| Persistent assembly receipt | — | `DecisionEvidenceAssemblyReceipt` | `derived/` (`judgment_status: not_evaluated`) |
| Assembly bounding profile | — | `DecisionEvidenceAssemblyProfile` | Git repo (versioned definition); records pin its version |
| Final gold | — | none — Judgment output only | never lake storage |

Rules:

- `Spike Alert` / `Movement Alert` are user-facing labels only; the stored record is
  `SourceObjectMovementThresholdCrossingRecord` and means only "a source object
  crossed a declared movement threshold under a declared profile/baseline/window/
  cohort/threshold." It carries no actor/person implication.
- "Gold-ready" is a conceptual layer name only. No stored record carries a
  `GoldReady` prefix.
- Gold interpretation appears only as Judgment output, never as lake storage.

## Record Home Mapping

- Raw Packet Store -> `raw/`.
- Attachment Record body -> packet-member under `raw/<packet_shard>/<packet_id>/`
  (ratified default, Gate 1 body-layout ADR 2026-07-02); `attachments/` stays
  reserved behind the sidecar reopen trigger.
- Availability Index -> `indexes/availability/`.
- Derived Result Store -> `derived/`.
- Acknowledgement Log -> `acknowledgements/`.
- `SourceObjectMovementThresholdCrossingRecord` -> `derived/` (non-Judgment,
  append-only, keyed to raw; first candidate class is source-object movement, not an
  actor profile).
- `DecisionEvidenceAssemblyReceipt` -> `derived/`; the transient
  `DecisionEvidenceAssemblyView` is computed on demand and may be cached rebuildably
  under `indexes/derived_retrieval/`.
- Commenter/reviewer timing retrieval -> `indexes/derived_retrieval/`, on-demand,
  exact-identifier-scoped, event-centric, non-dossier; rebuilt from `derived/` + raw;
  gated by access/audit/retention. Never in `indexes/availability/`, never lake
  authority.

What keeps derived retrieval from becoming authority: the `derived_retrieval`
subslot name (marked rebuildable + non-authoritative), the content-free guarantee on
`availability/`, and the rule that these are lane-owned records keyed to raw, not a
second source of truth.

## Configuration Contract

- One required primary resolvable pointer: `FORSETI_DATA_ROOT` -> an external absolute path. Legacy `ORCA_DATA_ROOT` remains accepted as a compatibility fallback during migration.
  The contract names no drive letter; the local example is `F:\orca-data`.
- Resolution precedence (contract shape, not loader implementation): production
  precedence is explicit / per-run override -> environment variable -> optional
  config-file fallback. A test root is injected only in test mode as an explicit test
  input; it is never a production precedence tier or runtime fallback (a test override
  placed after config would be a silent-write hazard). See the write-boundary
  enforcement decision contract.
- **Fail-closed.** Tools refuse to write and surface the failure when the root is:
  unset, unresolvable, **not mounted** (removable media absent), inside the repo
  working tree, or **missing its expected root marker**. There is no silent or
  fallback write.
- Root-identity check: because drive letters are reassignable (especially for
  removable media), resolution must confirm the path is actually the Forseti data root
  before writing, not merely that some path at that letter exists. The marker is a
  per-root identity (a root-local marker carrying a `root_uuid` compared against the
  configured/expected root identity), and writes use atomic write-then-rename that
  fails if the destination already exists. The exact marker mechanism is
  implementation; the per-root-identity intent is contract-level. See the
  write-boundary enforcement decision contract.
- Drive-letter volatility: the configured root's drive letter may change at any time
  (removable media); never rely on the letter. The resolver + per-root marker identify
  the root by identity, not by letter. A stable mount path or volume ID is an acceptable
  operator convenience, not a requirement.
- Config file format, loader, env/file merge mechanics, and validation tooling are
  implementation and remain deferred.

## Git Boundary

- **Stays in repo:** code, schemas, contracts, tests, small fixtures, example
  manifests, config templates (including a `FORSETI_DATA_ROOT` example line and legacy `ORCA_DATA_ROOT` compatibility note), and
  versioned definitions such as `DecisionEvidenceAssemblyProfile`.
- **Never committed:** everything under the data root — `raw/`, `attachments/`,
  `derived/`, `acknowledgements/`, `indexes/` — plus the already-ignored captures,
  test runs, scores, reports, logs, and auth/proxy/credential folders.
- The existing `.gitignore` already treats local/generated operational state as
  non-source-controlled, consistent with this boundary. Because the root resolves
  outside the repo, no new ignore entry is required; one is needed only if an
  operator points the root inside the tree (which fail-closed resolution discourages).

## Portability And Durability

- **Migration is intended to be painless.** Because the pointer is configuration and
  the layout is location-independent (raw immutable, derived append-only, indexes
  rebuildable), moving to a different or fixed drive is: byte-faithful copy of
  `raw/`, `attachments/`, `derived/`, `acknowledgements/` (verify hashes), repoint
  `FORSETI_DATA_ROOT` (or legacy `ORCA_DATA_ROOT` during compatibility), and rebuild `indexes/`. No schema migration, no rewrite.
- **`raw/` and `derived/` are the irreplaceable subtrees.** `raw/` cannot be rebuilt
  if lost; `derived/` is append-only history. `indexes/` is fully rebuildable.
  Operators deploying on removable or single-drive media must maintain an out-of-band
  backup of `raw/` and `derived/`. The backup mechanism is deployment, not this
  contract.

## MGT Accepted Residuals

Owner-invoked Mini God Tier shape (see `docs/decisions/orca_mini_god_tier_doctrine_v0.md`).
This intentionally captures most of the useful physical organization now and names
what it foregoes:

- **No engine selected by this contract.** A filesystem root + config remains
  the incumbent v0 foundation and satisfies by-key discovery. Risk: scan latency
  at scale. Upgrade path: the Storage Contract physicalization lane may choose a
  query/storage/queue/index engine as an optimization over committed state, never
  as authority.
- **Exact raw path grammar unfrozen.** Packet-admission and key rules are undecided.
  Risk: later raw-tree reshape. Mitigated: raw immutable + rebuildable indexes make a
  reshape a replay/rebuild, not a mutation. Upgrade trigger: packet-admission/key-rule
  decision lands.
- **Attachment physical home — resolved 2026-07-02** (was: unfrozen, sibling file
  vs packet member). The Gate 1 body-layout ADR ratified packet-member as the
  default home; `attachments/` stays reserved behind its reopen trigger. Kept
  as a closed-residual record; no longer an accepted residual.
- **`indexes/derived_retrieval/` representation + rebuild command not built.**
  Rebuildable and disposable, so cheap to defer; the medallion contract prefers
  on-demand retrieval. Upgrade trigger: first consumer needs a reverse lookup -> the
  index-rebuild command becomes a blocker.
- **Actor-retrieval access/audit/retention not designed.** No actor-derived lane
  exists; persistent actor histories are deliberately foregone. Upgrade trigger: any
  actor-adjacent derived-retrieval implementation.
- **Config mechanism (file format, loader, precedence, marker) not built.** Only the
  contract shape is fixed. Upgrade trigger: implementation lane.

## Implementation Blockers

Resolution status (updated as blocker-resolution decisions land 2026-06-21):

1. Packet-admission criteria + packet/slice/object/event key rules — **RESOLVED** by
   the raw admission + key grammar decision contract.
2. Attachment Record physical representation — **RESOLVED** in both halves:
   layout (Gate 1 body-layout ADR, owner-ratified 2026-07-02: packet-member
   default, sidecar reserved) and entry serialization (A2 ADR, owner-ratified
   2026-07-03: manifest-equivalent packet index; versioned entry schema plus
   deterministic derivation rule canonical).
3. Enforcement assignment for write-once raw, no-cleaning-in-lake, append-only
   derived/ack, no-new-core-field pressure — **RESOLVED** by the write-boundary
   enforcement decision contract.
4. Physical home + write boundary for projection/ECR/SCR/Cleaning/Judgment derived
   records, acknowledgements, and decision-evidence assembly receipts — **RESOLVED** by
   the derived-layout + index-rebuild decision contract.
5. Index rebuild command + the guarantee that all of `indexes/` rebuilds from
   committed keys/hashes — **RESOLVED** by the derived-layout + index-rebuild decision
   contract (availability now; derived_retrieval rebuild governance-gated/build-deferred).
6. Access/audit/retention guardrails + allowed source-family identifier scopes for
   actor-related on-demand retrieval — **RESOLVED** (owner-adopted actor-retrieval
   governance decision, 2026-06-21); `derived_retrieval` is governance-unblocked but
   build-deferred.
7. Mechanical derivation owner + profile/version contract (baselines, windows,
   cohorts, thresholds) for movement threshold-crossing records — **PARKED** (feature
   gated on data feasibility, not architecture; the foundation preserves on-demand
   derivability — see the derived-layout contract's on-demand analysis section).
8. Migration/replay policy for incumbent direct fields — directional (Storage Contract
   Blocker 2 direction recorded); mechanics build-deferred.
9. Govern SCR `FamilyDetailBase` so it cannot become a competing raw source-family
   payload home — **RESOLVED** by the write-boundary enforcement decision contract.
10. By-key discovery preserved as authority before any queue/event engine —
    **RESOLVED** (affirmed) by the write-boundary enforcement decision contract.
11. Config fail-closed behavior + root-marker identity check + test-mode override —
    **RESOLVED** by the write-boundary enforcement decision contract (test override is
    test-mode-only, not a production fallback).

## What This Does Not Select

- Storage engine or backend inside this contract; engine/backend choice belongs
  to the Storage Contract physicalization boundary.
- Manifest v2 (reserved behind the A2 ADR's revisit triggers). (Sidecar vs
  packet-member layout and entry serialization are now ratified by the Gate 1
  and A2 ADRs respectively — not selected by this contract.)
- Projection cache, runtime queue, or scheduler.
- ECR, SCR, Cleaning, Judgment, or Evidence Unit (EvidenceUnit) schema.
- Field-level schema for any named record.
- Fragrance or other domain ontology.
- Migration mechanics for incumbent fields.
- Validation/readiness/approval claim.

## Hard Boundaries

1. The Data Lake owns raw preservation, by-key findability, attachment references,
   passive availability, and logical derived attachment points. It does not own
   medallion interpretation or Judgment.
2. The Availability Index stays content-free; analytical reverse lookups stay
   lane-owned, rebuildable, and non-authoritative.
3. No physical layout creates a hidden actor/profile/dossier system.
4. Gold interpretation is Judgment-only and never leaks into a pre-Judgment layer,
   path, or stored record name.
5. Physical backend, serialization, manifest version, queue, cache, scheduler,
   persistence, and migration remain outside this contract unless a Storage
   Contract physicalization decision explicitly selects or supersedes them.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Fold-in of the owner-ratified A2 entry-serialization ADR (2026-07-03):
    implementation blocker 2 is now RESOLVED in both halves (Gate 1 layout +
    A2 entry serialization), and the what-this-does-not-select list annotates
    entry serialization as A2-ADR-owned with Manifest v2 reserved behind that
    ADR's revisit triggers.
  trigger: architecture_doctrine
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_a2_attachment_record_entry_serialization_adr_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    - forseti/product/spines/data_lake/README.md
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/README.md
      reason: >
        Its lake-ownership summary carries no serialization-deferral claim;
        checked, no stale language.
  stale_language_search: >
    rg -n "entry serialization|still deferred" forseti/product/spines/data_lake/authority
  stale_language_search_result: >
    Executed 2026-07-03 after edits. Remaining hits are the ratified-state
    statements added by this fold-in and historical receipt text; no live
    surface still says entry serialization is deferred.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization by this contract
    - not backend or storage-engine selection
    - not a Bronze full-GT claim
```

```yaml
direction_change_propagation:
  doctrine_changed: >
    Fold-in of the owner-ratified Gate 1 body-layout ADR (2026-07-02): the
    directory-grammar footnote resolves to packet-member under
    raw/<packet_shard>/<packet_id>/, the attachments/ slot is recorded as
    RESERVED behind the sidecar reopen trigger, the record-home mapping drops
    "placement deferred", the "Attachment physical home unfrozen" MGT residual
    closes, and implementation blocker 2's layout half is marked RESOLVED
    (entry serialization stays deferred to A2 behind the A1 deterministic
    inventory).
  trigger: architecture_doctrine
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_raw_admission_key_grammar_contract_v0.md
    - forseti/product/spines/data_lake/README.md
    - docs/workflows/orca_repo_map_v0.md
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/README.md
      reason: >
        Its Attachment Record mentions are ownership language with no
        placement-deferred claim.
  stale_language_search: >
    rg -n "placement deferred|physical home unfrozen"
    forseti/product/spines/data_lake docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-07-02 after edits. The only remaining hits sit inside the
    Gate 1 ADR's own historical receipt text (its pre-fold-in stale-language
    record); no live surface still says the attachment body placement is
    deferred or the physical home unfrozen.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not backend or storage-engine selection
    - not a Bronze full-GT claim
```

Older receipts, when cycled out, are archived in
`docs/decisions/dcp_receipts_archive_v0.md`.

## Non-Claims

Records a location boundary, directory grammar, location invariants, durable record
names, and fail-closed configuration intent only. Authorizes no build and does not
itself select a backend or storage engine, serialization, schema, queue/runtime
design, or migration. Not validation, readiness, proof, or approval for
implementation. Proposed record names are durable naming decisions; their
field-level schemas remain deferred.
