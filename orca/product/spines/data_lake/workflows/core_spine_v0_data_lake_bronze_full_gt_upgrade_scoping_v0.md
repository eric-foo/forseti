# Core Spine v0 Data Lake Bronze Full-GT Upgrade Scoping v0

```yaml
retrieval_header_version: 1
artifact_role: Data Lake workflow/scoping record
scope: >
  Signal-first scoping record for the Bronze MGT to full-GT upgrade path after
  PR #542, covering batches A-D and the review boundary before any full-GT claim.
use_when:
  - Planning Bronze full-GT work from the post-PR #542 consumer-proof base.
  - Checking which residual each A-D batch is meant to close or defer.
  - Preventing PR #542 or generated Bronze catalog indexes from becoming a full-GT declaration.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/handoffs/bronze_silver_full_gt_promotion_after_pr542_handoff_v0.md
  - docs/workflows/bronze_silver_two_family_consumer_proof_closeout_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/bronze_silver_pr542_two_family_closeout_delegated_adversarial_review_patch_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
branch_or_commit: >
  Authored on codex/bronze-full-gt-scoping as a stacked scoping artifact after
  PR #542 head 89501743dfd6aa0a2b4423e8f1d5fe1042758af7; verify current git state
  and PR #542 state before lifecycle claims.
stale_if:
  - PR #542 is materially rewritten, closed without merge, superseded, or merged with a different proof boundary.
  - Bronze MGT baseline, Data Lake storage, Attachment Record, or Silver Vault contracts are superseded.
  - A later accepted authority declares Bronze full GT or changes the full-GT upgrade path.
```

## Fused Discipline Record

This is the non-runtime artifact exit of a fused turn. The accepted direction is
to finish the A-D success-signal scoping record and then prepare a delegated
review prompt for that authored artifact.

```yaml
fused_discipline_record:
  implementation_scoping:
    status: route_complete_for_artifact_write
    accepted_direction: >
      Write the Data Lake spine scoping artifact for A-D, then route a delegated
      review prompt over the authored artifact.
    touch_points:
      - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_v0.md
      - docs/prompts/reviews/core_spine_v0_data_lake_bronze_full_gt_upgrade_scoping_delegated_adversarial_review_patch_prompt_v0.md
      - docs/workflows/orca_repo_map_v0.md
  spec_writing:
    status: spec_not_needed_ready_for_scoping
    implicit_contract: >
      The artifact names success signals and non-claims for A-D; it does not
      select Manifest, AR layout/backend, retention/lawful-erasure, or CI mechanics.
  assumption_gate:
    status: ready_with_verified_ledger
    gating_fact: >
      A fresh PR read observed PR #542 open, not draft, CI success, mergeStateStatus
      DIRTY, and mergedAt null; this artifact treats PR #542 as a branch-based
      planning base, not landed main proof.
  micro_decision_lock:
    status: locked
    allowed_changes: >
      Write this scoping artifact, the matching delegated review prompt, and
      repo-map pointers only.
    forbidden_changes: >
      No runtime code, tests, manifests, backend selection, AR layout selection,
      retention/lawful-erasure mechanism, CI/lake-doctor implementation, PR #542
      closeout patch, or full-GT declaration.
  review_routing_status: routed_after_artifact_write
```

## Current State Boundary

PR #542 is useful as the current consumer-proof planning base, but this artifact
does not claim it has landed on `main`. A fresh GitHub read during this lane
observed PR #542 as open, not draft, CI success, `mergeStateStatus=DIRTY`, and
`mergedAt=null`.

The proof boundary remains the closeout boundary: PR #542 records consumer proof
over Instagram and YouTube social-media creator-metric surfaces. It does not
prove Bronze full GT, Silver readiness, production lake validation, Manifest v2,
backend/body-store selection, retention/lawful-erasure, migration, final
Attachment Record physicalization, all source families, or all possible
Attachment Record join shapes.

## Success Signals First

Bronze full-GT work is not entered by item count. It is entered when these
signals can be made true without weakening Bronze raw authority or public
consumer surfaces:

- Deterministic discovery accounts for all raw-packet writers and all explicitly
  non-raw-packet lake touchpoints; no writer depends on manual runner memory.
- Manifest v2 or an equivalent packet-index serialization and migration path is
  selected only after discovery has bounded the writer/touchpoint surface, with
  dual-read or replay rules for legacy packet material.
- Attachment Record body physicalization is selected or bounded as a compact
  keyed entry plus immutable, hash-checkable body while preserving public
  Bronze/Silver re-resolution and no private folder inference.
- Retention and lawful-erasure posture are named before body or backend
  physicalization creates lock-in.
- Lake-doctor or CI-owned representative checks can fail, cover representative
  fixture lakes and real lane fixtures, and do not hide repo-wide placement debt
  as a pass.
- The consumer-proof threshold is domain-shape based, not count based: PR #542
  covers two social-media creator-metric AR-join shapes; a third proof is needed
  only when a candidate source family has a materially different raw-body or AR
  join shape that could invalidate the generic model.
- The YouTube ambiguous-AR branch is either test-pinned or explicitly carried as
  code-present but not test-proven.

## A-D To MGT 1-7 Crosswalk

The A-D labels refine, rather than replace, the Bronze MGT declaration's numbered
full-GT upgrade path and the handoff's owner-stated 1-2 / 3 / 4 / 5-6 / 7
batching preference:

| Scoping batch | MGT upgrade item(s) | Crosswalk note |
| --- | --- | --- |
| A | 1-2 | Keeps deterministic writer/touchpoint discovery ahead of Manifest v2 or equivalent migration selection. |
| B | 3, AR body-layout side | Covers Attachment Record body layout/backend posture as a physicalization fork, without selecting layout or backend. |
| C | 3, retention/lawful-erasure/backend lock-in side | Splits the retention, lawful-erasure, and backend lock-in posture out of item 3 so those high-lock-in choices stay visible before physicalization. |
| D | 4-6 | Merges lake-doctor/CI and representative consumer-proof threshold because fail-capable checks and proof breadth must be read together before any future full-GT claim. |

Item 7 remains the later de-correlated full Bronze/Silver review and closeout
boundary. That review gate is named here but not entered by A-D scoping.

## Batch A - Discovery Plus Manifest/Eq Migration Fork

**Residual addressed:** manual runner/orchestrator enumeration and the missing
Manifest v2 or equivalent migration decision.

**Success signal:** a deterministic discovery mechanism spec can account for
every current raw-packet writer and every explicitly non-raw lake touchpoint,
and it classifies each touchpoint before any Manifest/equivalent serialization
choice is made. Manifest/equivalent options are named with legacy dual-read or
replay implications.

**Deferred implementation implication:** actual discovery-gate code, actual
Manifest/equivalent serialization selection, dual-read mechanics, replay
triggers, migration tooling, and cutoff timing all require a separately
authorized implementation lane.

**Non-claim:** Batch A does not select Manifest v2, does not authorize
migration, and does not claim deterministic discovery is live.

**Delegated review-patch need:** not needed before scoping. A delegated
review-patch checkpoint becomes appropriate before accepting a concrete
Manifest/equivalent serialization or migration mechanic, because that would
create durable lock-in.

## Batch B - Attachment Record Physicalization Fork

**Residual addressed:** no final Attachment Record body layout or backend
posture.

**Success signal:** Attachment Record physicalization is bounded as a compact
manifest or manifest-equivalent keyed entry pointing to an immutable,
hash-checkable source-family payload body. Packet-member, sidecar, or equivalent
layouts may be compared, but the public contract must preserve body hash
verification, Availability Index rebuildability, public Bronze/Silver
re-resolution, and no private packet-member path inference.

**Deferred implementation implication:** exact packet-member versus sidecar
layout, manifest/index serialization, Manifest v2/versioning mechanics, selected
physical backend or engine, and migration/replay plan for incumbent direct fields
remain future decisions.

**Non-claim:** Batch B does not select a backend, sidecar, packet-member layout,
storage engine, Silver producer, or runtime AR implementation.

**Delegated review-patch need:** not needed before scoping. It should be treated
as a required checkpoint before ratifying a final AR layout/backend posture or
using that posture as implementation input.

## Batch C - Retention, Lawful-Erasure, And Backend Lock-In Posture

**Residual addressed:** retention, lawful-erasure, and backend lock-in are not
yet named strongly enough to prevent physicalization by convenience.

**Success signal:** retention and lawful-erasure constraints are named before
body/backend physicalization creates lock-in, and any backend candidate is
evaluated against Data Lake invariants: raw immutability, append-only
derived/ack records, rebuildable non-authoritative indexes, by-key discovery,
no-smart-lake boundary, and operational data staying outside Git unless a later
physicality-location contract supersedes that model.

**Deferred implementation implication:** WORM behavior, crypto-shredding,
retention mechanics, lawful-erasure mechanics, backend choice, and tests proving
the selected backend preserves lake invariants remain future decisions.

**Non-claim:** Batch C does not select a retention mechanism, lawful-erasure
mechanism, backend, engine, queue, runtime, or compliance posture.

**Delegated review-patch need:** not needed before scoping. This is the most
review-sensitive future selection point; require delegated review-patch before
ratifying any concrete backend, retention, or erasure mechanism.

## Batch D - Lake-Doctor/CI Gate Plus Representative Proof Threshold

**Residual addressed:** representative checks are not yet a fail-capable gate,
and the proof-breadth threshold could be over-read as family count or all-source
coverage.

**Success signal:** lake-doctor or CI checks cover representative fixture lakes
and real lane fixtures with real fail states, while the consumer-proof threshold
stays explicit: PR #542 is two social-media creator-metric surfaces and two
AR-join shapes, not cross-domain or all-source proof. YouTube ambiguous-AR is
test-pinned or carried as code-present but not test-proven. A third proof is
entered only if the candidate has materially different raw-body or AR-join shape
from the existing proofs.

**Deferred implementation implication:** lake-doctor/CI promotion, real-lane
fixture selection, ambiguous-AR test hardening, and any materially different
third proof require separate implementation authorization and validation gates.

**Non-claim:** Batch D does not claim production lake validation, real-lake
completeness, all-source coverage, a mandatory third proof, or that generated
catalog indexes are raw authority.

**Delegated review-patch need:** not needed before scoping. It becomes needed if
the lane rewrites the closeout boundary, adds a new proof artifact, claims
representative coverage, or promotes lake-doctor/CI checks as a gate.

## Cross-Batch Invariants

- Raw packet manifests, preserved bytes, packet refs, hashes, and hash basis
  remain the authority chain. Generated Bronze catalog and availability indexes
  remain rebuildable read state.
- Silver consumes through public Bronze surfaces: source-surface catalog rows,
  Attachment Record rows, `load_attachment_record_body`, and stable query paths.
- Missing Attachment Record stays visible as residual/posture; ambiguous
  Attachment Record states stay visible rather than collapsed into success.
- Source-family fields do not move into lake core merely to satisfy a proof.
- Full GT requires later de-correlated review of the full Bronze/Silver contract
  and code path before any full-GT claim.

## Next Material Move

The next material move is the delegated review prompt filed with this artifact.
That review is a hardening pass over the scoping artifact, not proof that A-D are
implemented or that Bronze is full GT. After review and home-model adjudication,
the owner can choose which A-D batch, if any, should receive a separate
implementation-scoping or `/fused` runtime lane.
