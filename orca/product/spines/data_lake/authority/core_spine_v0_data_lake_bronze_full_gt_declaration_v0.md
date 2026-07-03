# Core Spine v0 Data Lake Bronze Full GT Declaration v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture declaration
scope: >
  Owner-ratified successor to the Bronze MGT baseline for claim tier: declares
  Bronze full God Tier for the typed raw-truth retrievability and
  physicalization slice, at fixture-proof tier and under the ratified Gate 2
  claim ceiling, with named exclusions. Ratified 2026-07-03 in the block at
  the end of this record.
use_when:
  - Checking whether Bronze may be described as full God Tier, and under exactly which claim boundary.
  - Tracing the evidence chain (ratified ADRs, proof gates, de-correlated reviews) behind the Bronze full-GT claim.
  - Deciding whether a new Bronze residual re-opens this declaration or lands as a bounded follow-up.
open_next:
  - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_a2_attachment_record_entry_serialization_adr_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_full_gt_physicalization_proof_closeout_v0.md
  - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_a2_implementation_closeout_v0.md
  - docs/review-outputs/bronze_full_gt_closeout_delegated_adversarial_review_v0.md
stale_if:
  - The owner ratification block below changes state.
  - An A2 revisit trigger (T-A2-1..3) or Gate 2 trigger (T1-T4) fires.
  - The serializer, catalog delegation, inventory gate, or proof gate materially changes.
  - A backend/engine ADR is accepted (fires Gate 2 T3 and re-opens the backend exclusion below).
authority_boundary: retrieval_only
```

## Status

`BRONZE_FULL_GT_RATIFIED_V0` — owner-ratified 2026-07-03 (block at the end of
this record).

This record now owns Bronze's claim tier. The MGT baseline
(`core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md`) is
superseded for claim tier (its stale_if #3 fired) and remains in place as the
historical baseline and upgrade-path provenance. The claim stays exactly as
bounded below — the ratified label never widens the exclusions or the Gate 2
claim ceiling.

## The Claim (exact and bounded)

Bronze is proposed as **full God Tier for typed raw-truth retrievability and
physicalization**, meaning:

1. Raw packet manifests and preserved bytes are the only authority; every
   derived surface (catalog, availability, AR rows) is generated, rebuildable
   read state — proven, not just asserted.
2. The physicalization invariants are CI-owned, fail-capable proofs
   (PROOF-01..07 + the A1 inventory gate), each with a clean half and a
   seeded-violation half through public APIs.
3. The Attachment Record canonical object is the ratified A2 shape — a pinned,
   versioned entry schema plus deterministic derivation rule — implemented as
   the single serializer both the catalog and zero-index by-key reads flow
   through, with fail-closed dispatch on unknown sealed-packet formats.
4. Body layout and retention posture are ratified decisions (Gate 1
   packet-member default; Gate 2 erasure deferral with its claim ceiling), not
   accidents of implementation.
5. The assembled whole — contracts, ADRs, code, proof gates — survived a final
   cross-vendor de-correlated adversarial review with no critical or major
   finding (one minor proof-gate hardening, adjudicated and kept).

**Claim ceiling (binding):** the ratified Gate 2 ADR's claim ceiling governs
all deletion/erasure language — this declaration asserts no erasure
capability. **Claim tier (binding):** every proof named here runs at
deterministic fixture-lake tier; this declaration asserts nothing about any
production lake.

## Evidence Assembly

- **Ratified decisions** (all owner-ratified in their own records):
  - Gate 1 — Attachment Record body layout (packet-member default; sidecar
    reserved), ratified 2026-07-02.
  - Gate 2 — retention/lawful-erasure deferral with claim ceiling and revisit
    triggers T1-T4 (any backend ADR fires T3), ratified 2026-07-02.
  - A2 — entry serialization (packet index; versioned entry schema +
    deterministic derivation rule as the canonical object; Manifest v2
    reserved behind T-A2-1..3; `attachment_record_id` a query locator only),
    ratified 2026-07-03.
- **Proof gates** (CI-owned, fail-capable, fixture tier):
  - A1 deterministic touchpoint inventory gate
    (`orca-harness/data_lake/inventory.py` +
    `orca-harness/tests/contract/test_data_lake_inventory_gate.py`).
  - PROOF-01..07 (`orca-harness/tests/test_data_lake_physicalization_proof.py`):
    write-once raw, append-only derived/ack, read-by-key, hash verification,
    public AR body resolution, byte-identical index rebuild, and zero-index
    canonical derivation with fail-closed version dispatch.
  - Pinned serializer contract tests
    (`orca-harness/tests/test_data_lake_attachment_record_entry.py`), including
    the exact catalog-decoration-envelope proof added by the closeout review.
- **De-correlated reviews** (all cross-vendor: authored_by Anthropic Claude,
  reviewed_by OpenAI GPT-5 Codex; each adjudicated by the commissioning CA
  before keep):
  - `docs/review-outputs/bronze_physicalization_proof_scope_delegated_adversarial_code_review_v0.md`
    (ADV-01..03 accepted).
  - `docs/review-outputs/a2_entry_serializer_delegated_adversarial_code_review_v0.md`
    (F-01/F-02 accepted).
  - `docs/review-outputs/bronze_full_gt_closeout_delegated_adversarial_review_v0.md`
    — the final pass over the assembled whole (five contracts, three ADRs,
    Bronze code path, proof gates): no critical or major findings; one minor
    proof-gate hardening accepted; claim-inflation and index-as-truth sweeps
    returned explicit non-findings.

## MGT Upgrade-Path Disposition

Item-by-item disposition of the MGT baseline's "upgrade Bronze from MGT to
full GT" list:

| # | Baseline item | Disposition |
| --- | --- | --- |
| 1 | Deterministic discovery gate for all lake writers/touchpoints | **Closed** at source-inventory tier (A1 gate; owner-dispositioned unknowns; fail-capable in both directions). |
| 2 | Manifest v2 / packet-index serialization selection | **Closed at selection tier and implemented** (A2 ratified; pinned serializer + PROOF-07 landed). Incumbent-field migration mechanics remain excluded below. |
| 3 | Body layout / backend posture / retention | **Dispositioned by ratified decisions**: Gate 1 selected packet-member; Gate 2 ratified the erasure deferral and claim ceiling; hash verification proven at fixture tier (PROOF-04/05). Backend selection remains excluded below (T3-gated). |
| 4 | CI-owned rebuild/invariant gate over fixture lakes | **Closed at fixture tier** (PROOF-01..07 CI-owned). Real-lane fixture breadth remains excluded below. |
| 5 | One Silver producer consumes Bronze via public helpers with verified `raw_refs` | **Closed at fixture-test tier**: the YouTube Silver metric producer consumes `source_surface_catalog_rows` and upgrades `raw_refs` through Bronze AR rows with explicit missing/ambiguous limitation kinds (`orca-harness/capture_spine/creator_profile_current/youtube_silver_metric_producer.py`). |
| 6 | Repeat consumer proof across enough source families | **Partially closed; remainder excluded from this claim.** Two source-family Silver producers are proven through the public helpers (`docs/workflows/bronze_silver_two_family_consumer_proof_closeout_v0.md`, post-PR #537/#540); whether that breadth is "enough" stays consumer-pressure-driven follow-up work, not a Bronze physicalization gap. |
| 7 | De-correlated review of the full contract + code path before any full GT claim | **Closed for Bronze** (the three adjudicated cross-vendor reviews above, ending with the assembled-whole closeout pass). The Silver-side contract/code path was not in that review's scope and is excluded below. |

## Named Exclusions (what this declaration does NOT claim)

- **No production-lake validation** — all proofs are deterministic fixture
  lakes; live-lake state (including the four known junk packets awaiting owner
  cleanup) is not validated by this record.
- **No all-source coverage / real-lane fixture breadth** — the proof gate runs
  representative fixtures; each lake-interacting lane still proves its own
  consumption path.
- **No backend/engine selection** — deliberately reserved; any backend ADR
  fires Gate 2 T3 and re-opens the relevant exclusions.
- **No incumbent-field migration/replay tooling** — refusal of unknown formats
  is implemented; hold/replay of refused or legacy material stays a separate
  owner-gated decision.
- **No erasure capability** — Gate 2's ratified claim ceiling governs all
  deletion language.
- **No Silver-family breadth beyond the two proven families, and no
  Silver-side de-correlated review** — the open remainder of item 6 and the
  Silver half of item 7 above.
- **Third-proof threshold not fired** — the materially-different third proof
  stays a tripwire (the YouTube ambiguous-AR branch remains
  code-present/not-test-proven); no source shape crossed the brief's threshold
  as of this declaration.

## Erosion Guards

Two erosion pressures are named so future lanes can refuse them explicitly:

- **Index as truth**: no catalog, availability, or AR row surface may be
  treated as authoritative; PROOF-03/06/07 exist to keep every such surface
  rebuildable and deletable. A lane that needs an index to be authoritative is
  proposing a doctrine change, not using this declaration.
- **Claim inflation**: this declaration's claim is exactly the bounded slice in
  "The Claim" above. Citing it for readiness, production validation, erasure,
  backend maturity, or Silver-tier guarantees is a misuse of this record.

## Ratification Fold-In (performed 2026-07-03)

The fold-in obligations named at proposal time were performed in the
ratification lane:

1. The MGT baseline declaration is annotated as superseded-for-claim-tier by
   this record (its stale_if #3 fired), left in place as the historical
   baseline record.
2. The `direction_change_propagation` receipt for the claim-tier change is
   carried below.
3. This record is registered in the data_lake README routing and the repo map.

## Owner Ratification

```yaml
bronze_full_gt_ratification:
  decision: ratified
  ratified_by: owner (Eric), in-session instruction "ratify" after merging PR #612
  date: 2026-07-03
  modifications: >
    One factual strengthening folded in while recording ratification:
    upgrade-path item 6 now cites the two-family Bronze/Silver consumer-proof
    closeout (docs/workflows/bronze_silver_two_family_consumer_proof_closeout_v0.md,
    post-PR #537/#540) instead of understating the proven breadth as one
    family, and the matching exclusion is scoped to "beyond the two proven
    families". No claim, exclusion, or ceiling was widened.
```

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Bronze's claim tier changes: the owner ratified this declaration
    (2026-07-03), so Bronze is full God Tier for the typed raw-truth
    retrievability and physicalization slice — fixture-proof tier, Gate 2
    claim ceiling, named exclusions (production-lake validation, real-lane
    fixture breadth, backend/engine selection, migration/replay tooling,
    erasure capability, Silver-family breadth beyond two proven families,
    Silver-side review). The MGT baseline declaration is superseded for claim
    tier and remains the historical baseline and upgrade-path provenance.
  trigger: architecture_doctrine
  related_triggers:
    - workflow_authority
  controlling_sources_updated:
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_full_gt_declaration_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md
    - orca/product/spines/data_lake/README.md
    - orca/product/spines/data_lake/workflows/core_spine_v0_data_lake_bronze_lake_owner_explainer_v0.md
    - docs/workflows/orca_repo_map_v0.md
  downstream_surfaces_checked:
    - orca-harness/data_lake/catalog.py
    - orca-harness/tests/test_data_lake_catalog.py
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
    - orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
    - docs/decisions/orca_mini_god_tier_doctrine_v0.md
  intentionally_not_updated:
    - path: orca-harness/data_lake/catalog.py
      reason: >
        The runtime marker BRONZE_BASELINE_STATUS ("bronze_mgt_baseline_recorded_v0",
        semantics "not full God Tier") and its test assertion are runtime code,
        outside this docs fold-in's authority; the baseline itself bound the
        marker as additive and non-authoritative, and under-claiming is the
        safe direction. Updating the marker to reflect the ratified tier is a
        named bounded follow-up requiring its own implementation authorization
        (it mints a new runtime status enum value that downstream asserts).
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_medallion_gold_readiness_contract_v0.md
      reason: >
        Layer semantics (bronze/silver/gold-ready/gold) are unchanged by a
        Bronze claim-tier ratification; gold remains Judgment output.
    - path: orca/product/spines/data_lake/authority/core_spine_v0_data_lake_storage_contract_v0.md
      reason: >
        Backend/engine selection remains reserved exactly as the contract
        states; this declaration's backend exclusion defers to it and Gate 2 T3.
    - path: docs/decisions/orca_mini_god_tier_doctrine_v0.md
      reason: >
        The MGT doctrine is an owner-invoked design lens, not a claim registry;
        one artifact graduating from an MGT baseline changes no doctrine text.
  stale_language_search: >
    git grep -n -i -E "not full God Tier|not declared full|bronze_mgt_baseline_recorded|MGT|full GT|God Tier"
    orca/product/spines/data_lake orca-harness/data_lake
    orca-harness/tests/test_data_lake_catalog.py docs/workflows/orca_repo_map_v0.md
  stale_language_search_result: >
    Executed 2026-07-03 after edits. Remaining hits: the annotated historical
    MGT baseline (its supersession note now governs; body text explicitly
    labeled as describing the 2026-06 baseline), the runtime marker in
    catalog.py:37-39 plus its test assertion (dispositioned above as the named
    follow-up), historical workflow/ADR records whose "not a full-GT claim"
    non-claims were true when written and remain true of those records, and
    this declaration's own bounded-claim language. No live routing surface
    (data_lake README, repo map, owner explainer) still asserts Bronze is
    MGT-only or not full God Tier.
  non_claims:
    - not validation or readiness of any production lake
    - not backend, engine, migration, replay, or erasure authorization
    - not a Silver-tier claim
    - not a runtime marker update (named follow-up, separately authorized)
```

## Non-Claims

- Not validation, not readiness, not proof of any production lake.
- Not implementation authorization for backend, migration, replay, or erasure
  work.
- Not a Silver-tier claim of any kind.
- Not self-ratifying: the status marker above only changes through the owner
  ratification block.
