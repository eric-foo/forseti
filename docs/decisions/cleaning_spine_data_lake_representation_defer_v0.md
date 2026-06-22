# Cleaning Spine x Data Lake Representation & Deferral Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Architecture decision (recommendation pending owner sign-off) -- the Cleaning spine's Data Lake representation, its v0 deferral, and the triggers that un-defer it.
scope: >
  How a cleaned record is represented in the Data Lake and why Cleaning lake-wiring
  is deferred in v0, with the concrete triggers that un-defer it. Cross-spine
  (Cleaning x Data Lake). Planning/recommendation only; does not authorize a build.
use_when:
  - Deciding whether or when to wire the Cleaning spine into the Data Lake.
  - Checking the un-defer triggers before building a Cleaning lake writer or a derived_retrieval view.
  - Confirming the per-packet vs cross-packet representation boundary for cleaned records.
open_next:
  - orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md
stale_if:
  - The owner adopts, amends, or rejects this recommendation.
  - A Cleaning transform-ledger / cleaned-record producer or a cross-packet dedupe deriver lands.
  - A governed consumer needs the cross-packet reverse lookup.
authority_boundary: retrieval_only
```

## Status

`RECOMMENDATION_PENDING_OWNER_SIGNOFF`. Produced by an architecture-planning pass (standard profile, 3 option subagents) and hardened by a de-correlated (non-Claude) adversarial artifact review (verdict: SOUND; findings AR-01/AR-02/AR-03 adjudicated and folded in). Recommends DEFER. Does not authorize any Cleaning build -- Cleaning stays separately gated per `.agents/workflow-overlay/safety-rules.md`.

## Decision

**Defer wiring the Cleaning spine into the Data Lake in v0. Lock the representation architecture now so the lake home is pre-decided, and un-defer on the triggers below.**

## Why Defer

Cleaning's derivation is dormant in the harness:

- A projection->handle adapter exists (`orca-harness/cleaning/projection.py:14`) but produces raw-keyed handles only -- there is **no transform-ledger / cleaned-record producer and no persisted Cleaning lake writer**.
- The only mechanical dedupe (`orca-harness/cleaning/core.py:15`) includes `packet_id` in the identity key, so it cannot group across captures; `indexes/derived_retrieval` population is build-deferred.
- Cross-packet **exact-identity** dedupe is **allowed by contract** (`orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md:269-278`) but **not implemented**; **similarity / near-match** dedupe is owner-deferred (OD-4, same contract :265-283).

Wiring Cleaning now, in any shape, would persist near-empty records ("empty-record theatre"): no current cleaning value and no consumer. Deferring is the smallest-complete move. The gap is implementation, not doctrine.

## Locked Representation Architecture (the shape, for when un-deferred)

- **Core / keystone:** authoritative cleaned facts are **per-packet, single raw anchor, append-only** -- the same grammar as the wired spines (`derived/<raw-anchor>/<lane>/<record-id>`; `core_spine_v0_data_lake_derived_layout_index_rebuild_contract_v0.md:50`).
- **Satellite (deferred), complementary -- not competing:**
  - **(A) Assembly receipt** -- a durable, append-only `derived/` record whose body references the N raw anchors it grouped (`derived_layout_contract:111`). Needs **no change to `append_record`** (the multi-anchor truth lives in the body); needs a legal synthetic segment for the cluster key. Never a fake single-anchor multi-packet record.
  - **(B) `derived_retrieval` view** -- a non-authoritative, rebuildable reverse-lookup / cluster cache over the per-packet records (`derived_layout_contract:134`); **full-rebuild only** (a new packet can change clusters globally, so incremental update is a fake-success trap).
- **Persistence-boundary implication (AR-02):** the in-memory `CleaningPacket` is **not** the per-packet authoritative object (it can hold handles from multiple packets and carries no packet invariant). The lake writer must **split / validate Cleaning output by raw anchor** to produce per-packet records.
- **Invariants to preserve:** cross-packet artifacts **reference, never restate** per-packet truth; each epistemic kind stays a sibling lane; raw is immutable and re-verified on read.

## Un-Defer Triggers (how to "unclear")

Condition-triggered, not date-based. Two independent gates.

**Gate 1 -- per-packet cleaning record.** Un-defer when a real per-packet cleaning producer exists (transform-ledger entries, or within-packet exact-identity). Then: build the deriver + producer -> add `orca-harness/cleaning/lake.py` (splitting by raw anchor) -> `derived/<packet_id>/cleaning/<record-id>.json`, mirroring `orca-harness/ecr/lake.py`.

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
