# Ontology object card — `case:beautypie.repricing-2023` (v0)

```yaml
retrieval_header_version: 1
artifact_role: Ontology object card (instance hint — Case)
scope: >
  Object card for the adopted Orca ontology backbone — a dated instance hint for one
  Case. The §2.2 roster in orca_ontology_backbone_architecture_v0.md is the naming
  authority; this card is an instance hint, not authority, and restates no owner-lane
  content (it points). Carries the forward-only ID equivalence (harness_case_id).
authority_boundary: retrieval_only
status: DATED_HINT_2026-06-15
naming_authority: forseti/product/spines/foundation/ontology/orca_ontology_backbone_architecture_v0.md  # §2.2 (type Case) + §2.1 (ID grammar, forward-only convention)
```

> Dated instance hint, fail-soft — **not** a current-state claim, **not** authority;
> restates no batch-ledger / evidence-ladder content (it points). Reserved types get no card.

- **id:** `case:beautypie.repricing-2023` (§2.1 grammar; canonical dotted form)
- **harness_case_id:** `beautypie_repricing_2023_v0` — forward-only **storage alias** under the
  canonical id (§2.1 / §6.1 forward-only convention; **not** a rename). This field is the
  registry seed for the equivalence; both id forms resolve to this entity.
- **type:** `Case` — §2.2 row 12 ("a backtest/proof case: a historical decision with known outcome")
- **instance:** Beauty Pie — £5/month entry-tier elimination, minimum doubled (2023); beauty subscription repricing.
- **key states / dimensions** (per §2.2 row 12 — receipt-backed pointers only, NOT standing fields):
  - `dev/holdout`, `entry_basis`, `claim_tier` are **batch-ledger metadata + receipt-gated outcomes**,
    MAPPED to the owners below — never minted as card state (the AR-01 boundary).
- **links** (drawn from §2.3, not invented):
  - `case:beautypie.repricing-2023 —backtests→ decision:beautypie.repricing-2023`
  - `case:beautypie.repricing-2023 —graded_by→ outcome:beautypie.repricing-2023`
- **backing artifact** (pointer — NOT restated): `orca-harness/cases/product_learning/beautypie_repricing_2023_v0/`
  (resolved via `harness_case_id`).
- **mapped owners** (this card POINTS; it does not restate):
  - dev/holdout split + entry_basis → `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md`
    (batch-1 ledger, case #3 — `dev`, Tier A, owner-confirmed 2026-06-11)
  - claim_tier (receipt-gated outcome, never type-minted) → `forseti/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md`

## Non-Claims

Dated hint only. Restates none of the batch-ledger or evidence-ladder content — points to them.
The `harness_case_id` equivalence is naming/resolution only; it enacts **no** migration and
renames nothing. Not validation, not readiness, not buyer proof, not a registry.
