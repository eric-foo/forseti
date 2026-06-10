# Unity Runtime Fee Facilitator Ledger Draft v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: Draft facilitator-ledger surface for the Unity Runtime Fee v0.14 fixture.
use_when:
  - Reviewing draft ledger fields and missing labels before any v0.14 scoring.
  - Separating direct Pydantic FacilitatorLedger fields from protocol fixture metadata.
  - Checking leakage, second-label, and freeze blockers.
authority_boundary: retrieval_only
input_hashes:
  fixture_authoring_prompt: E04DC7C16F733E827709EDEC32CC5BADE6F2F273225916B5F92DC6A3B4FD0E23
  extraction_plan: DC0C9D64312E7A2BC49FA4EE227DD581E43919FBDD93F25AF83E6DFAB9677CE7
  source_packet: FA4F7642ECAFB0488B57076F2DF59F8F4A742AA422331C9E833FA8AF548FFF24
  pydantic_schema_reference: CFFC7BCAC179B752B9A77204ECA6A6399D30DD7CB6B2C52533E3EC0FDC031D8D
  case_construction_protocol: FDEA14A1767D135A8DD56AF073AF0E5E3206B945FB9E603F597491D795889C71
  band_input_labeling_rubric: 0CE6E9584F4F1C4716559A654870AF43EBED3E5D53D3279AB658993B7DE1C2AE
  post_authoring_review: BB1EAD239DF2A1EE5704B888BD5F1F261B0E2DD2D656E5FCB4330708A19C674C
open_next:
  - docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md
  - docs/research/judgment-spine/harness/v0_14/judgement_case_construction_protocol.md
  - docs/research/judgment-spine/harness/v0_14/band_input_labeling_rubric.md
```

- Status: FACILITATOR_LEDGER_DRAFT_NOT_FROZEN
- Case ID: `unity_runtime_fee_2023_v0_14`
- Fixture status: blocked before scoring
- Ledger freeze hash: `NOT_COMPUTED`
- Second-label audit: not performed
- Action band derivation: not performed
- Scoring status: not score-ready

## Direct Pydantic FacilitatorLedger Draft Fields

These fields follow `pydantic_schema_reference.md` and are separate from protocol fixture metadata.

```yaml
case_id: unity_runtime_fee_2023_v0_14
batch_id: unity_runtime_fee_2023_v0_14_draft_pack
labeling_rubric_version: v0_14
mapping_table_version_pin: v0_14_mvp
ledger_authors:
  - TBD_PRIMARY_LABELER
  - TBD_SECOND_LABELER
second_label_diffs: []
frozen_band_inputs: NOT_FROZEN
must_address_items: CANDIDATE_ONLY
underreach_observability:
  present: false
  basis: null
  notes: Financial pressure and option value may be relevant, but the draft packet lacks source-backed evidence for a primary underreach failure. Valid Pydantic basis values are opportunity_cost, window_closure, information_decay, or other.
leakage_audit_notes: DRAFT_ONLY_SEE_LEAKAGE_SECTION
spoiler_inventory: DRAFT_ONLY_SEE_SPOILER_INVENTORY
committed_at: NOT_COMMITTED
ledger_freeze_hash: NOT_COMPUTED
```

This is not a schema-valid frozen ledger because `frozen_band_inputs`, author identities, commitment timestamp, second-label workflow, and freeze hash remain unresolved.

## Protocol Fixture Metadata

These values are required or useful for the v0.14 case-construction and run protocol, but they are not direct current Pydantic `FacilitatorLedger` fields unless a later adapter or schema revision binds them.

```yaml
case_family: platform_pricing_packaging_monetization
case_family_status: CANDIDATE_PROTOCOL_METADATA
decision_shape: ceiling_trap
decision_shape_status: CANDIDATE_PROTOCOL_OR_BLIND_JUDGEMENT_METADATA_NOT_FROZEN
memorization_probe_required: true
memorization_probe_required_status: PROTOCOL_LEAKAGE_INPUT_NOT_DIRECT_PYDANTIC_FIELD
known_fame_risk: elevated
known_fame_risk_status: PROTOCOL_LEAKAGE_INPUT_NOT_DIRECT_PYDANTIC_FIELD
```

`decision_shape` must be frozen before any `BlindJudgement` adaptation or run. `ceiling_trap` is the leading candidate because the Unity case tests whether visible revenue pressure and strategic plausibility should still cap a broad runtime/install-fee commitment. `action_band` is a possible fallback if the operator wants a more general right-sized action fixture.

## Frozen Band Inputs - Candidate Review Table

These values are candidate review aids only. They are not frozen labels, not scoring truth, and not participant-facing material.

| Field | Candidate value | Status | Rationale to review |
| --- | --- | --- | --- |
| `evidence_strength` | `moderate` | CANDIDATE_UNFROZEN | First-order filing evidence supports visible pressure and risk categories, but not broad launch safety. |
| `evidence_independence` | `partially_independent` | CANDIDATE_UNFROZEN | Most evidence comes from S-03; S-07 adds contextual competitor evidence. |
| `reversibility_feasibility` | `low` | CANDIDATE_UNFROZEN | Broad customer-facing monetization changes may be hard to reverse cleanly, but exact contract and rollout design are unknown. |
| `reversibility_cost` | `high` | CANDIDATE_UNFROZEN | Customer confidence, renewal, cancellation, reduced-use, and substitution risks are source-backed categories. |
| `authority` | `partial` | CANDIDATE_UNFROZEN | The role frame assumes senior accountability, but legal, contract, finance, operations, and board constraints are not proven. |
| `authority_acquisition_cost` | `medium` | CANDIDATE_UNFROZEN | Broad policy or pricing changes likely need cross-functional approval, but exact governance is unknown. |
| `capability` | `partial` | CANDIDATE_UNFROZEN | Unity has a platform business, but metering, billing, dispute, support, and communication readiness are not established in the packet. |
| `capability_build_cost` | `high` | CANDIDATE_UNFROZEN | Missing operational and legal readiness fields are material for runtime/install-based monetization. |
| `loss_shape` | `asymmetric_down` | CANDIDATE_UNFROZEN | Customer confidence and substitution risks create downside that may exceed short-term monetization upside. |
| `opportunity_cost` | `moderate` | CANDIDATE_UNFROZEN | Public financial pressure supports monetization exploration, but not an expiring opportunity. |
| `information_decay` | `slow` | CANDIDATE_UNFROZEN | Waiting may improve customer and operational information; no once-only window is established. |
| `option_value` | `moderate` | CANDIDATE_UNFROZEN | Narrow testing or phased packaging could preserve learning and future choices. |
| `upside_shape` | `symmetric` | CANDIDATE_UNFROZEN | Upside exists from monetization exploration, but source packet does not prove asymmetric or convex upside. |
| `urgency` | `low` | CANDIDATE_UNFROZEN | Financial pressure exists, but no critical timing requirement is established from packet-safe evidence. |

Quarantine or review is required if second-labeling creates more than three disagreements, disagreement on evidence strength exceeds one level, loss-shape disagreement includes `ruinous_tail`, information-decay disagreement includes `expiring`, or disagreement cannot be resolved without importing facilitator-only material.

## Second-Label Audit Status

```yaml
second_label_audit:
  status: NOT_PERFORMED
  second_label_diffs: []
  reason: Draft fixture-authoring lane is not authorized to freeze labels or run scoring.
  required_before_scoring: true
```

## Candidate Must-Address Items

These items are candidate scorer/operator material only. They must not appear in the participant packet.

| ID | Candidate item | Evidence unit references |
| --- | --- | --- |
| MA-01 | Commercial pressure supports monetization exploration but does not by itself authorize broad runtime/install-based launch. | EU-01, EU-02, EU-03 |
| MA-02 | Customer confidence, renewal, cancellation, reduced-use, and substitution risks are decision-critical. | EU-05, EU-06 |
| MA-03 | High-value customer segmentation is plausible, but exposure, contract rights, and churn are not proven. | EU-04, EU-08 |
| MA-04 | Exact pricing, terms, elasticity, legal enforceability, metering, support, dispute handling, and communication readiness remain unknown. | EU-08 |
| MA-05 | Competitor and customer-economics context matters, but does not prove switching behavior or acceptable customer economics. | EU-06, EU-07 |

## Underreach Observability

Direct Pydantic draft:

```yaml
underreach_observability:
  present: false
  basis: null
  notes: >
    Public financial pressure and possible option value are visible, but the draft packet lacks private targets, expiring-window evidence, customer-level economics, or source-backed evidence that inaction would be a primary failure. If a later operator marks underreach observability true, the Pydantic basis must be one of opportunity_cost, window_closure, information_decay, or other. Option-value loss belongs in notes or maps to other.
```

## Leakage Audit Notes

Draft `leakage_audit_notes` should carry:

- Source packet query cap: 6 search queries.
- Source packet page-open cap: 8 unique public URLs opened.
- Source packet snippet-noise existed, but leaked facts were not quoted or preserved.
- Source packet opened no post-cutoff pages.
- Source packet read no prior replay artifacts and no contaminated archive bodies.
- Participant packet draft is restricted to pre-cutoff packet-safe material.
- Facilitator-only materials include the legacy sealed memo, outcome calibration, and reveal readout.
- Protocol leakage input: `memorization_probe_required: true`.
- Protocol leakage input: `known_fame_risk: elevated`.

`memorization_probe_required` and `known_fame_risk` are protocol leakage inputs in this draft, not direct current Pydantic `FacilitatorLedger` fields.

## Spoiler Inventory

Draft advisory `spoiler_inventory`:

- legacy sealed memo recommendation and action ceiling;
- owner blind-read decision;
- post-cutoff public-event material;
- outcome calibration verdict;
- reveal readout lessons and tactical reads;
- product-proof implications;
- facilitator ledger labels;
- candidate must-address items;
- action band, action floor, action ceiling, and scoring material;
- probe result or model-family quarantine state once any later probe exists.

## Ledger Freeze Blocker

```yaml
ledger_freeze_hash: NOT_COMPUTED
ledger_status: NOT_FROZEN
can_support_scoring: false
blocked_until:
  - participant packet is cleaned and hashed
  - evidence registry fields are resolved and hashed
  - band inputs are primary-labeled, second-labeled, diffed, resolved, and frozen
  - must-address items are finalized
  - underreach observability is finalized
  - leakage audit and spoiler inventory are finalized
  - decision_shape is frozen for the run protocol
  - memorization probe passes for the target model family
```

No action band was derived from this draft ledger.
