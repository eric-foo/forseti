# Core Spine v0 Data Lake Bronze Full GT Declaration v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture declaration
scope: >
  Proposed successor to the Bronze MGT baseline: declares Bronze full God Tier
  for the typed raw-truth retrievability and physicalization slice, at
  fixture-proof tier and under the ratified Gate 2 claim ceiling, pending owner
  ratification in the block at the end of this record.
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

`BRONZE_FULL_GT_PROPOSED_V0` — **pending owner ratification.**

Until the ratification block at the end of this record reads
`decision: ratified`, Bronze's authoritative claim tier remains the MGT
baseline (`core_spine_v0_data_lake_bronze_mgt_baseline_declaration_v0.md`),
and no surface may describe Bronze as full God Tier on the basis of this
proposal.

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
| 6 | Repeat consumer proof across enough source families | **Open — excluded from this claim.** One family is proven through the public helpers; breadth stays consumer-pressure-driven follow-up work, not a Bronze physicalization gap. |
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
- **No Silver-family breadth and no Silver-side de-correlated review** — items
  6 and the Silver half of item 7 above.
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

## On Ratification (fold-in obligations, not performed here)

When (and only when) the owner ratifies below, a fold-in turn must:

1. Annotate the MGT baseline declaration as superseded-for-claim-tier by this
   record (its stale_if #3 fires), leaving it in place as the historical
   baseline record.
2. Carry the `direction_change_propagation` receipt for the claim-tier change
   (this proposal deliberately carries none — no controlling doctrine changes
   until ratification).
3. Register this record in the repo map / data_lake README routing.

## Owner Ratification

```yaml
bronze_full_gt_ratification:
  decision: pending
  ratified_by:
  date:
  notes: >
    Owner fills this block. Until decision reads `ratified`, Bronze's
    authoritative claim tier remains the MGT baseline declaration and no
    surface may cite this record as a full-GT claim.
```

## Non-Claims

- Not validation, not readiness, not proof of any production lake.
- Not implementation authorization for backend, migration, replay, or erasure
  work.
- Not a Silver-tier claim of any kind.
- Not self-ratifying: the status marker above only changes through the owner
  ratification block.
