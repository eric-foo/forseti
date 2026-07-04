# Core Spine v0 Data Lake Bronze Full-GT Gate 2 Retention Lawful-Erasure Posture ADR v0

```yaml
retrieval_header_version: 1
artifact_role: Data Lake workflow/decision-request record
scope: >
  Gate 2 ADR for the Bronze full-GT physicalization lane: record the
  retention / lawful-erasure / backend lock-in posture as an explicit
  deferral carrying the full accepted-residual record (residual scope, claim
  ceiling, working unavailability posture, forbidden backend classes and
  operations while deferred, revisit triggers), for owner ratification.
use_when:
  - Adjudicating or ratifying the Gate 2 retention/erasure posture.
  - Checking what any backend candidate is forbidden from carrying while erasure is deferred.
  - Checking the triggers that force a full retention/lawful-erasure ADR.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate1_attachment_record_body_layout_adr_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
stale_if:
  - The owner ratifies, modifies, or rejects this ADR (the ratification block below then governs).
  - Any revisit trigger below fires (the deferral then ends and a full retention/erasure ADR is required).
  - The Storage or Physicality Location contract changes the retention/erasure boundary.
```

## Status

`GATE2_ADR_RATIFIED_V0` (owner-ratified 2026-07-02; see Owner Ratification).

This record was authored as a decision request and is now the accepted Gate 2
posture: an explicit, bounded deferral. It is not a compliance posture, not legal advice, not erasure capability,
not backend selection, not implementation authorization, not validation,
readiness, or a Bronze full-GT claim.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom gate2 pack (brief + storage + physicality contracts, read in full)
  edit_permission: docs-write
  target_scope: Gate 2 posture ADR authoring; no runtime or contract edits.
  dirty_state_checked: yes
  blocked_if_missing: none
```

## Decision In One Screen

```text
Recorded (pending ratification): lawful erasure is DEFERRED as an accepted,
named residual - not solved, not silently ignored. Unavailability is expressed
by append-only tombstone/supersession records (G2-B) while raw bytes remain.
A written claim ceiling caps what Orca may say about deletion. Backend classes
and operations that would carry retention policy implicitly, or make a future
erasure posture irreversible, are forbidden while the deferral stands. Four
revisit triggers end the deferral and force the full retention/erasure ADR.
```

Why deferral is the honest form: the owner has signaled lawful erasure is not
a hard current requirement, current source families capture public-web
material, and inventing an erasure mechanism now would be fake compliance -
exactly the vague-deferral failure the hardened brief forbids. The value of
this record is that the deferral is bounded, visible, and revocable on named
triggers instead of implicit.

## The Accepted-Residual Record (required by the brief)

**1. Residual scope.** What is deferred: byte-level lawful erasure
(destruction of raw content on demand), retention schedules, and any
compliance-grade deletion. Basis for accepting it now: every current source
family (fragrance review sites, Instagram, YouTube, TikTok) captures
public-web material for evidence; no lane currently admits private, tenant, or
consent-gated data into the lake. That basis is part of the residual - if it
stops being true, trigger T2 fires.

**2. Claim ceiling.** While this deferral stands, Orca must not claim: lawful
erasure capability, GDPR/right-to-be-forgotten readiness, retention-policy
compliance, WORM/immutability certification, or Bronze full GT resting on a
"resolved" Gate 2. Public statements about deletion are capped at: "content
can be tombstoned so it no longer serves reads; raw bytes are retained."

**3. Working unavailability posture (G2-B).** "Delete" means an append-only
tombstone/supersession record: a new derived record marks the material
unavailable-for-consumption; public read surfaces honor tombstones; the raw
packet, its hashes, and its history remain intact. This fits every existing
invariant (write-once raw, append-only derived, rebuildable indexes) and
requires no new machinery class.

**4. Backend-native retention.** Not allowed to carry policy while deferred.
No backend's lifecycle rules, expiry, versioning-cleanup, or WORM mode may be
enabled as a de facto retention policy; deterministic tests for any future
backend must prove retention semantics are inert until a ratified Gate 2
decision assigns them.

**5. Forbidden while deferred.** These are hard stops, not advice:

- selecting any backend whose native lifecycle/retention/WORM semantics would
  decide retention implicitly (the G2-D convenience path);
- any backend or layout choice that would make later key-separated erasure
  (G2-C) or tombstone semantics impossible or prohibitively costly to add;
- deleting or mutating pinned raw material as an "erasure" mechanism;
- encoding retention meaning into the directory grammar or record names;
- admitting a private/tenant/consent-gated source family without first firing
  trigger T2 below.

## Revisit Triggers (any one ends the deferral)

- **T1 - owner/legal call.** The owner declares lawful erasure a hard
  requirement.
- **T2 - data-class change.** Any lane proposes admitting private, tenant,
  personal-data-sensitive, or consent-gated material into the lake.
- **T3 - backend ADR opens.** Any backend/engine selection ADR is drafted;
  per the brief, Gate 2 must be answered before backend lock-in, so the
  drafting lane must either re-ratify this deferral against that backend's
  semantics or produce the full erasure ADR first.
- **T4 - external demand.** A real third-party deletion/erasure demand
  arrives against captured material.

When a trigger fires, the required next artifact is a full retention /
lawful-erasure ADR comparing at minimum G2-B (tombstone-only), G2-C
(key-separated encrypted bodies with crypto-shred), and G2-D (deliberate
backend-native controls) against the then-current data classes.

## Named Residuals (accepted if ratified)

- Raw storage grows without bound; no retention schedule exists.
- A tombstone is not erasure; anyone with raw access can still read
  tombstoned bytes. The claim ceiling exists precisely because of this.
- The immutable-history versus erasable-material split (which material could
  ever need G2-C key separation) is not designed; it is deferred with the
  residual.

## Owner Ratification

```yaml
gate2_ratification:
  decision: ratified
  ratified_by: owner (Eric), in-session instruction "2 gates OK"
  date: 2026-07-02
  modifications: none
```

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Gate 2 is owner-ratified as an explicit deferral carrying the full
    accepted-residual record: lawful erasure is an accepted residual with a
    written claim ceiling; append-only tombstone/supersession is the working
    unavailability posture; the forbidden backend classes/operations while
    deferred and the four revisit triggers (owner call, data-class change,
    any backend ADR opening, external demand) become standing doctrine.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate2_retention_lawful_erasure_posture_adr_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_physicality_location_contract_v0.md
    - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md
    - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_gate_adr_batch_plan_v0.md
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/authority/ (storage, physicality contracts)
      reason: >
        Contract fold-in is the named follow-on lane (see the post-ratification
        handoff packet); their "retention and lawful-erasure remain later
        physicalization constraints" language remains accurate - this ADR is
        that later constraint, now decided as a bounded deferral.
    - path: forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_decision_brief_v0.md
      reason: >
        Its stale_if self-fires on this ratification by design; it becomes
        historical gate framing without an edit.
  stale_language_search: >
    rg -c "lawful[- ]erasure|erasure posture"
    forseti/product/spines/data_lake/authority
  stale_language_search_result: >
    Executed 2026-07-02 after recording ratification. Hits: storage contract
    (1: "retention and lawful-erasure policy remain later physicalization
    constraints" - this ADR is that later constraint, now decided as a bounded
    deferral), AR implementation contract (3: deferred-decision mentions),
    Bronze MGT baseline (1: residual mention). All are deferral language this
    ADR satisfies; fold-in will repoint them explicitly. No live surface
    contradicts the ratified posture.
  non_claims:
    - not erasure capability, retention compliance, or legal advice (the claim
      ceiling in this ADR governs what may be said)
    - not backend/engine selection
    - not implementation authorization
    - not validation, readiness, or Bronze full GT
```

## Non-Claims

- Not erasure capability, retention compliance, WORM certification, or legal
  advice; the claim ceiling above is itself part of the record.
- Not backend, engine, object-store, database, or hybrid selection.
- Not implementation authorization, validation, readiness, third-proof
  authorization, or Bronze full GT.
