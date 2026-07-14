# Cleaning Spine x Data Lake Representation & Deferral Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Historical architecture decision with a live residual boundary -- the Cleaning spine's Data Lake representation, the v0 deferral, and the remaining cross-packet trigger.
scope: >
  How a cleaned record is represented in the Data Lake and why Cleaning lake-wiring
  is deferred in v0, with the concrete triggers that un-defer it. Cross-spine
  (Cleaning x Data Lake). Planning/recommendation only; does not authorize a build.
use_when:
  - Deciding whether or when to wire the Cleaning spine into the Data Lake.
  - Checking the un-defer triggers before building a Cleaning lake writer or a derived_retrieval view.
  - Confirming the per-packet vs cross-packet representation boundary for cleaned records.
open_next:
  - docs/decisions/cleaning_derived_record_anchor_contract_v0.md
  - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
stale_if:
  - The owner adopts, amends, or rejects this recommendation.
  - A Cleaning transform-ledger / cleaned-record producer or a cross-packet dedupe deriver lands.
  - A governed consumer needs the cross-packet reverse lookup.
authority_boundary: retrieval_only
```

## Direction Change Propagation — 2026-07-14

```yaml
direction_change_propagation:
  doctrine_changed: >
    The original Cleaning-to-lake deferral is now historical for the landed
    source-specific per-packet writers. Basenotes, Fragrantica, and Parfumo may
    persist Cleaning audit packs plus eligible facts through the Silver/Vault
    envelope; audit packs remain processing evidence, not Silver Authority.
    Cross-packet dedupe, similarity, assembly, and derived_retrieval stay deferred.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/cleaning_spine_data_lake_representation_defer_v0.md
    - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
  downstream_surfaces_checked:
    - forseti/product/spines/data_lake/README.md
    - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_mechanics_map_v0.md
    - forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - forseti-harness/cleaning/basenotes_lake.py
    - forseti-harness/cleaning/fragrantica_lake.py
    - forseti-harness/cleaning/parfumo_lake.py
  intentionally_not_updated:
    - path: forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_silver_vault_record_contract_v0.md
      reason: >
        It already states the controlling Silver Authority/audit-pack boundary
        and explicitly excludes Cleaning audit packs from Silver fact records.
  stale_language_search: >
    rg -n "no persisted Cleaning lake writer|cleaning->lake WRITER|Gate 1|derived_retrieval"
    docs/decisions/cleaning_spine_data_lake_representation_defer_v0.md
  stale_language_search_result: >
    Executed 2026-07-14. Remaining no-writer wording is explicitly marked as
    historical; Gate 1 is marked satisfied for the three landed source-specific
    writers; derived_retrieval remains a live deferred residual.
  non_claims:
    - not a universal Cleaning writer claim
    - not cross-packet dedupe or similarity authorization
    - not a derived_retrieval implementation authorization
    - not historical record migration
```

## Status

`HISTORICAL_DECISION_WITH_LIVE_RESIDUAL`, `PER_PACKET_WRITER_TRIGGER_OBSERVED_2026-07-14`. The original recommendation and its 2026-06-27 input-anchor amendment remain provenance. Current source now contains per-source Cleaning audit-pack and eligible Silver-fact writers, so this record no longer defers those landed paths. Cross-packet dedupe and the generated `derived_retrieval` view remain deferred.

## Decision

**Historical decision:** defer the v0 wiring while locking its representation. **Current residual:** landed per-packet writers are no longer deferred; only cross-packet dedupe/assembly and its governed retrieval view remain behind the trigger below.

## Amendment 2026-07-14 -- per-packet writer trigger observed

Gate 1 has fired in current code: `forseti-harness/cleaning/{basenotes,fragrantica,parfumo}_lake.py` persist per-source Cleaning audit packs and eligible Silver facts. Their audit packs remain processing evidence, not Silver Authority; eligible fact records use the official Silver/Vault envelope. This amendment does not invent a generic Cleaning writer and does not un-defer cross-packet dedupe, similarity, assembly, or `derived_retrieval`.

## Amendment 2026-06-27 -- partial un-defer (cleaning INPUT-anchor for derived records)

The owner un-deferred **only** the cleaning INPUT-anchor for derived records: a first-class `derived_record` Cleaning input anchor for lake-resident derived records that have no preserved-file substrate (the ASR `youtube_audio` -> `transcript_asr` surface), plus the injected `DataLakeRoot` read access the periodic audit + smoke runner need to resolve and re-hash that derived record. This is the read-side input-anchor slice only; its full contract, integrity framing, and acceptance criteria are in `cleaning_derived_record_anchor_contract_v0.md`.

At the time of this 2026-06-27 amendment, the cleaning->lake writer, cross-packet dedupe, and `derived_retrieval` view were still deferred. The 2026-07-14 amendment above records that the per-packet writer trigger later fired; the cross-packet surfaces remain deferred.

## Historical Rationale For Deferral

At the time of the original decision, Cleaning's derivation was dormant in the harness. The following bullets are historical evidence, not current-state claims:

- A projection->handle adapter existed (`forseti-harness/cleaning/projection.py`) but produced raw-keyed handles only; at that point there was **no transform-ledger / cleaned-record producer and no persisted Cleaning lake writer**.
- The only mechanical dedupe (`forseti-harness/cleaning/core.py`) included `packet_id` in the identity key, so it could not group across captures; `indexes/derived_retrieval` population was build-deferred.
- Cross-packet **exact-identity** dedupe was **allowed by contract** (`forseti/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`) but **not implemented**; **similarity / near-match** dedupe was owner-deferred (OD-4, same contract).

At that time, wiring Cleaning in any shape would have persisted near-empty records ("empty-record theatre"): there was no current cleaning value and no consumer. Deferring was the smallest-complete move. The gap was implementation, not doctrine.

## Locked Representation Architecture (the shape, for when un-deferred)

- **Core / keystone:** authoritative cleaned facts are **per-packet, single raw anchor, append-only** -- the same grammar as the wired spines (`derived/<raw-anchor>/<lane>/<record-id>`; `core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md:50`).
- **Satellite (deferred), complementary -- not competing:**
  - **(A) Assembly receipt** -- a durable, append-only `derived/` record whose body references the N raw anchors it grouped (`derived_layout_contract:111`). Needs **no change to `append_record`** (the multi-anchor truth lives in the body); needs a legal synthetic segment for the cluster key. Never a fake single-anchor multi-packet record.
  - **(B) `derived_retrieval` view** -- a non-authoritative, rebuildable reverse-lookup / cluster cache over the per-packet records (`derived_layout_contract:134`); **full-rebuild only** (a new packet can change clusters globally, so incremental update is a fake-success trap).
- **Persistence-boundary implication (AR-02):** the in-memory `CleaningPacket` is **not** the per-packet authoritative object (it can hold handles from multiple packets and carries no packet invariant). The lake writer must **split / validate Cleaning output by raw anchor** to produce per-packet records.
- **Invariants to preserve:** cross-packet artifacts **reference, never restate** per-packet truth; each epistemic kind stays a sibling lane; raw is immutable and re-verified on read.
- **Engagement-context implication:** a future cleaned `engagement_context` fact may enter Silver Authority only through the official envelope, not merely because Cleaning derived it. It is not Gold or a new storage tier. It may preserve source-visible resonance qualifiers such as direction, visible audience-fit basis, baseline context, and discount reasons, but not their Judgment effect. Cross-packet engagement comparisons, resonance-context candidates, or clusters wait for the same assembly / `derived_retrieval` triggers as other cross-packet Cleaning output.

## Un-Defer Triggers (how to "unclear")

Condition-triggered, not date-based. Two independent gates.

**Gate 1 -- per-packet cleaning record (`SATISFIED` for the landed source-specific writers).** A real per-packet producer now exists for Basenotes, Fragrantica, and Parfumo. This does not imply a universal Cleaning writer or cross-source coverage.

**Gate 2 -- cross-packet (A and/or B).** Un-defer when **both** hold:

1. a cross-packet dedupe **semantic** is implemented -- exact-identity-across-packets (contract-allowed; drop `packet_id` from the identity key) or owner authorization of similarity per OD-4; **and**
2. a **governed consumer** needs the cluster / reverse-lookup (the `derived_layout` contract's own `derived_retrieval` trigger).

Building either alone materializes emptiness; require both.

**Mechanism.** On observing a trigger, the owner authorizes the bounded Cleaning build in-turn (separately gated); build the deriver + producer + writer; wire it through this decided lake home. The likely first domino is the decision-evidence / Judgment layer needing dedupe (a pull, not a push).

## Non-Claims / Boundary

- Planning / recommendation only; **does not authorize a Cleaning build**. Cleaning, EvidenceUnit binding, the SP-5 finalizer, and Judgment stay separately gated.
- Not validation, not readiness, not a similarity-dedupe authorization (OD-4 unchanged).
- Actor-retrieval governance is build-deferred and does not by itself trigger Cleaning wiring.

## Provenance

Architecture-planning pass (3 option subagents: A assembly-receipt / B derived_retrieval-view / C per-packet-only) -> home-model synthesis -> de-correlated non-Claude adversarial artifact review (deep-thinking). Review verdict: SOUND. Adjudicated findings folded in: AR-01 (cross-packet exact-identity is contract-allowed but unimplemented), AR-02 (per-packet split required at the lake boundary), AR-03 (a handle adapter exists; the gap is the transform-ledger / cleaned-record / writer producer).

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The v0 "defer wiring the Cleaning spine into the Data Lake" architecture
    decision is partially reversed: the owner un-deferred (2026-06-27) ONLY the
    cleaning INPUT-anchor for derived records -- a first-class `derived_record`
    Cleaning input anchor for lake-resident derived records with no
    preserved-file substrate (ASR youtube_audio -> transcript_asr), plus the
    injected DataLakeRoot lake-READ coupling the periodic audit + smoke runner
    need to resolve and re-hash that record -- while the cleaning->lake WRITER,
    cross-packet dedupe, and derived_retrieval view this doc defers REMAIN
    deferred.
  trigger: architecture_doctrine
  related_triggers:
    - lifecycle_boundary
  controlling_sources_updated:
    - docs/decisions/cleaning_spine_data_lake_representation_defer_v0.md
    - docs/decisions/cleaning_derived_record_anchor_contract_v0.md
  downstream_surfaces_checked:
    - docs/workflows/orca_repo_map_v0.md
    - .agents/workflow-overlay/source-of-truth.md
    - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
  intentionally_not_updated:
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        Not a repo-map event: the change added a manifest ENTRY TYPE
        (`youtube_asr`) and behavior INSIDE the already-mapped runners
        run_capture_ecr_cleaning_smoke.py / run_cleaning_spine_periodic_audit.py,
        plus new audit functions, two new orca-harness/tests/unit/ files, and one
        new docs/decisions/ doc -- no new top-level area and no new
        orca-harness/ runner/adapter FILE (the two mechanical staleness criteria
        the freshness hook checks). The `transcript_asr` derived-record concept
        and both runners are already on the map; new tests + a new decisions doc
        are reachable by convention.
    - path: orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
      reason: >
        The Cleaning foundation contract's anchor/handle semantics are unchanged
        in doctrine; the `derived_record` anchor is an additive implementation
        slice specified in the AO-2 contract doc, not a foundation-contract
        amendment. Cross-packet dedupe (OD-4) is untouched and stays deferred.
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
      reason: >
        The lake's derived layout + append_record write-once contract is
        unchanged; this slice READS existing derived records and adds no lake
        writer or layout change. The named derivation-time-hash enhancement is a
        future shared-lake-contract change, deferred and out of this slice.
  stale_language_search: >
    rg -n "still deferred|build-deferred|no persisted Cleaning lake writer|neither the smoke runner nor the audit has any .DataLakeRoot|REMAIN deferred|un-defer"
    docs/decisions/cleaning_spine_data_lake_representation_defer_v0.md
    docs/decisions/cleaning_derived_record_anchor_contract_v0.md
  stale_language_search_result: >
    Executed 2026-06-27 in worktree asr-ecr-derived-anchor (lane branch). Hits
    were the deferral doc's Why-Defer / Un-Defer-Triggers prose (the WRITER +
    cross-packet machinery that correctly STAYS deferred), this doc's new
    Amendment + receipt naming the bounded un-defer, and the contract doc's
    Problem statement recording the pre-change "neither runner has DataLakeRoot
    access" fact (a historical statement of the gap this slice closes, not a
    live deferral). No surface was left asserting that the derived-record INPUT
    anchor or the audit lake-read coupling is still deferred.
  non_claims:
    - not validation
    - not readiness
    - not acceptance
    - not a cleaning->lake WRITER authorization
    - not a cross-packet dedupe or similarity (OD-4) authorization
    - not a derived_retrieval view authorization
    - not a lake-contract (derivation-time hash) change
```
