# Core Spine v0 Data Lake Physicality Location Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract
scope: >
  Physicality-location contract for Orca's Data Lake: the repo-vs-operational-data
  boundary, the operator-configured external data root (ORCA_DATA_ROOT), the v0
  logical directory grammar (raw/ attachments/ derived/ acknowledgements/ and a
  split indexes/availability + indexes/derived_retrieval), the location invariants
  (raw immutable, derived/ack append-only, indexes rebuildable), durable stored
  record names, fail-closed root resolution, and accepted residuals. This is a
  location and directory-grammar contract, not a storage-engine or backend choice.
use_when:
  - Deciding where Orca operational data physically lives versus what stays in the Git repo.
  - Scoping data-root configuration, fail-closed resolution, or directory placement.
  - Naming a durable Data Lake record and checking it does not leak gold/Judgment/actor semantics.
open_next:
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

`TARGET_PHYSICALITY_LOCATION_CONTRACT_RECORDED_V0`.

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

- Real Orca operational data does not live in the Git repository; it lives under a
  separate operator-configured external data root.
- The pointer is generalized: `ORCA_DATA_ROOT=<operator-configured external data
  root>`. The owner's current local example is `F:\orca-data` (a portable drive);
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

It settles the location boundary and directory grammar. It deliberately does not
settle the storage engine, serialization, manifest version, cache, queue,
scheduler, runtime, or migration mechanics, which remain owned by the Storage
Contract physicalization gate.

## The Boundary In One Screen

```text
The Git repository owns code, schemas, contracts, tests, small fixtures,
example manifests, and config templates.
Real operational data lives under one operator-configured external data root.
The repo points at the root through configuration (ORCA_DATA_ROOT).
The root resolves OUTSIDE the repo working tree, or tools fail closed.
Raw stays immutable; derived and acknowledgement records stay append-only;
indexes stay rebuildable and carry no authority.
```

The lake is strict about where bytes land. It is not smart about what they mean.

## Physical Root Contract

- The boundary is a **location contract**, not a storage-engine choice. A directory
  grammar is acceptable while backend, serialization, and manifest version remain
  deferred to the Storage Contract.
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
<ORCA_DATA_ROOT>/
  raw/                       # Raw Packet Store      — immutable, write-once
  attachments/               # Attachment Record     — immutable, hash-checkable*
  derived/                   # Derived Result Store  — append-only, keyed to raw
  acknowledgements/          # Acknowledgement Log   — append-only, keyed to raw
  indexes/
    availability/            # Availability Index    — content-free committed/
                             #   readable-by-key state; rebuildable; NOT authority
    derived_retrieval/       # lane-owned analytical retrieval aids — rebuildable,
                             #   non-authoritative; NOT truth / actor history / dossier

* attachment bodies may instead live as packet members under raw/<packet_id>/;
  the sibling-file-vs-packet-member placement is deferred to the Attachment Record
  implementation direction.
```

These names are **logical slot homes**, not a frozen path schema. `raw/<packet_id>/...`
is the **target raw layout direction**, gated on packet-admission and key-rule
decisions; it is not locked here.

## Directory Slot Contract

| Slot | Owns (lake-side) | Must not become |
| --- | --- | --- |
| `raw/` | Raw Packet Store: immutable `SourceCapturePacket` bundles, stable packet/slice/file handles, `sha256`, `hash_basis`. | Cleaned truth, canonical identity, mutable packet history. |
| `attachments/` | Attachment Record bodies: source-family payload bodies, immutable/hash-checkable, keyed to packet/slice/file. | Cleaned values, dedupe/credibility/Judgment labels, downstream-use strength. |
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
- Attachment Record -> `attachments/` or packet-member under `raw/<packet_id>/`
  (placement deferred).
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

- One required resolvable pointer: `ORCA_DATA_ROOT` -> an external absolute path.
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
  removable media), resolution must confirm the path is actually the Orca data root
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
  manifests, config templates (including an `ORCA_DATA_ROOT` example line), and
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
  `ORCA_DATA_ROOT`, and rebuild `indexes/`. No schema migration, no rewrite.
- **`raw/` and `derived/` are the irreplaceable subtrees.** `raw/` cannot be rebuilt
  if lost; `derived/` is append-only history. `indexes/` is fully rebuildable.
  Operators deploying on removable or single-drive media must maintain an out-of-band
  backup of `raw/` and `derived/`. The backup mechanism is deployment, not this
  contract.

## MGT Accepted Residuals

Owner-invoked Mini God Tier shape (see `docs/decisions/orca_mini_god_tier_doctrine_v0.md`).
This intentionally captures most of the useful physical organization now and names
what it foregoes:

- **No storage engine / queue / scheduler / runtime.** A filesystem root + config
  satisfies by-key discovery. Risk: scan latency at scale. Upgrade trigger: by-key
  scan latency becomes unacceptable -> add a queue/index engine as an optimization
  over committed state, never as authority.
- **Exact raw path grammar unfrozen.** Packet-admission and key rules are undecided.
  Risk: later raw-tree reshape. Mitigated: raw immutable + rebuildable indexes make a
  reshape a replay/rebuild, not a mutation. Upgrade trigger: packet-admission/key-rule
  decision lands.
- **Attachment physical home unfrozen** (sibling file vs packet member). Owned by the
  Attachment Record implementation direction. Upgrade trigger: that lane closes.
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
2. Attachment Record physical representation — directional (Attachment Record
   implementation contract); exact layout/serialization build-deferred.
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

- Storage engine or backend.
- Serialization, Manifest v2, or sidecar vs packet-member layout.
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
   persistence, and migration remain outside this contract.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Data Lake Physicality Location Contract v0 records the location boundary:
    operational data lives under one operator-configured external data root
    (ORCA_DATA_ROOT, generalized; example F:\orca-data), separate from the Git
    repo; the v0 directory grammar is raw/ attachments/ derived/ acknowledgements/
    and a split indexes/availability (content-free) plus indexes/derived_retrieval
    (rebuildable, non-authoritative); raw is immutable, derived/ack append-only,
    indexes rebuildable; root resolution is fail-closed including not-mounted and a
    root-marker identity check; durable record names are mechanical
    (SourceObjectMovementThresholdCrossingRecord, DecisionEvidenceAssemblyView,
    DecisionEvidenceAssemblyReceipt, DecisionEvidenceAssemblyProfile) with no
    GoldReady prefix and gold only as Judgment output; storage engine, backend,
    serialization, queue, runtime, and migration remain deferred.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
    - workflow_authority
  controlling_sources_updated:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - forseti/product/spines/data_lake/README.md
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_core_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
    - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - .gitignore
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
      reason: >
        The Storage Contract remains the non-selecting physicalization-blocker owner.
        This contract adds the location boundary and directory grammar without
        reopening storage-slot or blocker ownership.
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
      reason: >
        The medallion contract already defers physical home and names the data lake
        physicality lane as a downstream consumer. This contract is that downstream
        location decision and does not change medallion semantics.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Repo-map registration is a separate hygiene/routing step on the shared map;
        this lane records the contract and its local README pointer without editing
        the shared repo map. Registration is a recommended follow-up.
  stale_language_search: >
    rg -n "ORCA_DATA_ROOT|physicality location|external data root|orca-data|indexes/availability|indexes/derived_retrieval|SourceObjectMovementThresholdCrossingRecord|DecisionEvidenceAssembly"
    forseti/product/spines/data_lake docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    To be executed against the data_lake spine and repo map after landing; this lane
    introduces the ORCA_DATA_ROOT and physicality-location vocabulary, so expected
    hits are this contract and the data_lake README pointer. No prior live data-lake
    source is expected to define a competing data-root location boundary.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not backend or storage-engine selection
    - not serialization, manifest, or schema finalization
    - not queue/runtime design
    - not migration authorization
```

## Non-Claims

Records a location boundary, directory grammar, location invariants, durable record
names, and fail-closed configuration intent only. Authorizes no build, no backend or
storage-engine selection, no serialization or schema finalization, no queue/runtime
design, and no migration. Not validation, readiness, proof, or approval for
implementation. Proposed record names are durable naming decisions; their
field-level schemas remain deferred.
