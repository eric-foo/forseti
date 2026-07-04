# Core Spine v0 Data Lake A2 Implementation Closeout v0

```yaml
retrieval_header_version: 1
artifact_role: Data Lake workflow/evidence record
scope: >
  Closeout record for fused Lane A (owner-granted 2026-07-03): the A2 contract
  fold-in plus the pinned AttachmentRecordEntry serializer implementation —
  canonical schema + deterministic derivation rule module, centralized
  manifest-version dispatch, catalog delegation, zero-index by-key derivation,
  and PROOF-07 — with validation evidence, residuals, and non-claims.
use_when:
  - Checking what the ratified A2 decision's implementation actually landed and proved.
  - Finding the pinned serializer module and its version pins.
  - Deciding the remaining Bronze full-GT moves (third-proof threshold, final de-correlated review).
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_a2_attachment_record_entry_serialization_adr_v0.md
  - forseti/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_proof_closeout_v0.md
  - forseti/product/spines/data_lake/authority/core_spine_v0_data_lake_attachment_record_implementation_contract_v0.md
stale_if:
  - The serializer module, dispatch registry, or PROOF-07 materially changes.
  - A later accepted decision closes the third-proof threshold or the final de-correlated review.
  - An A2 revisit trigger (T-A2-1..3) fires.
```

## Status

`A2_IMPLEMENTATION_LANDED_V0` — fixture-lake tier, CI-owned, delegated review
pending. Not production-lake validation, backend selection (Gate 2 T3),
retention semantics, readiness, or a Bronze full-GT claim.

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: Lane A pack (ratified A2 ADR + folded contracts + catalog.py internals + proof gate)
  edit_permission: implementation-authorized (owner "fused lane A go", 2026-07-03)
  target_scope: A2 fold-in + pinned serializer + proofs; no backend, no incremental rebuild, no replay tooling.
  dirty_state_checked: yes (branch claude/a2-implementation off origin/main @ 2ed2059c)
  blocked_if_missing: none
```

## What Landed

- **Contract fold-in** (commit-separated, one DCP receipt per contract): the AR
  implementation, storage, and physicality contracts state the ratified A2
  selection; MGT baseline item 2 closed at selection tier; oldest inline
  receipts archived per the two-inline cap.
- **Pinned serializer** `orca-harness/data_lake/attachment_record_entry.py` —
  the ADR's canonical object as code: the versioned `AttachmentRecordEntry`
  schema and deterministic derivation rule, with
  `entry_serialization_version: attachment_record_entry_serialization_v1` and
  `derivation_rule_version: attachment_record_derivation_rule_v1` pins on
  every entry (top-level and in `replay_version_pins`), canonical bytes
  (sorted keys, ASCII, compact separators, newline), and **centralized
  manifest-version dispatch** that fails closed on unknown sealed-packet
  formats (`SUPPORTED_RAW_PACKET_MANIFEST_VERSIONS`; legacy no-version packets
  dispatch through the v1 rule). The hash-derived `attachment_record_id`
  is documented and asserted as a cache/query locator only.
- **Catalog delegation**: `data_lake/catalog.py` AR rows are now exactly the
  canonical entry plus catalog-only decorations (authority note, catalog
  versions, `stable_query_paths`, catalog pin); attachment-record schema
  bumped `_2 -> _3` and catalog schema `_2 -> _3` (additive pins). Public read
  surfaces (`source_surface_catalog_rows`, `load_attachment_record_body`)
  keep their signatures.
- **Zero-index by-key derivation** `derive_entries_by_key(root, packet_id)`:
  shard recompute -> verified raw read -> derivation rule; no index, catalog,
  locator, or queue involved.
- **PROOF-07** in the CI-owned proof gate: clean half — with `indexes/`
  deleted, by-key derivation reproduces the canonical part of the materialized
  rows byte-for-byte; violation half — an unknown manifest version on a sealed
  packet is refused, never coerced. Plus fail-capable serializer tests
  (determinism, pins, dispatch refusal, required-field refusal, canonical
  round-trip, materialized-row equality) in
  `tests/test_data_lake_attachment_record_entry.py`.

## Validation Evidence

- Full suite: `python -m pytest` from `orca-harness/` exits 0 with
  `ORCA_DATA_ROOT` unset (CI-equivalent), 2026-07-03.
- Two Silver-producer tests that hardcoded the old schema literal were
  single-sourced onto `ATTACHMENT_RECORD_SCHEMA_VERSION` (no production code
  pinned the literal — the consumer kill-condition did not fire; producers
  copy pins from rows).
- The checked-in touchpoint inventory stayed byte-identical: the new module
  adds no lake touchpoint calls, so the A1 gate passes unchanged.
- Doctrine changes were carried by the fold-in receipts in the three
  contracts; this closeout adds no doctrine change and therefore carries no
  new `direction_change_propagation` receipt.

## Residuals (unchanged or newly named)

- **Engine under the index / incremental rebuild**: deliberately not built;
  waits for A2 revisit trigger T-A2-1 pressure and a Gate 2 T3-gated backend
  ADR.
- **Replay tooling for legacy/unknown formats**: refusal is implemented;
  hold/replay of a refused packet stays a separate owner-gated decision.
- **Real-lane fixture breadth** (MGT item 4 tail) and the
  **materially-different third proof** threshold: unchanged, still open.
- **Final de-correlated review over finished contracts + code** (Full-GT
  Distance item 5): the next and last full-GT step after this lane's review
  adjudicates.

## Non-Claims

- Not a Bronze full-GT claim; not production-lake validation; not
  backend/engine selection; not retention/erasure semantics (Gate 2 claim
  ceiling governs); not Manifest v2 authoring.
- Delegated review of this lane's diff is commissioned, not completed;
  acceptance is home-model adjudication's call.
