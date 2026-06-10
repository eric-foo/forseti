# Daimler Facilitator Ledger Work Queue v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact - facilitator-only work queue
scope: Unfrozen facilitator-ledger work queue for the Daimler corporate-structure vote v0.14 fixture candidate.
use_when:
  - Planning Daimler facilitator ledger fields before any ledger freeze or scoring.
  - Separating candidate assessment surfaces from future schema-valid FacilitatorLedger fields.
  - Checking leakage, spoiler, probe, second-label, and freeze blockers before blind-use prep.
authority_boundary: retrieval_only
input_hashes:
  fixture_entry_plan_v0.md: AC2669BFAFEAF44DBFF00DB6486F5214B877333596F629F914084EB69C1F2782
  evidence_registry_draft_v0.md: 2E9FC02E7D19AA21DC9C66E9DF740D53A6798365D70EB76A2D3F213F2DD2FBA5
  participant_packet_draft_v0.md: 5CC0D40F8D41F61360B07831B4D7B2BD22BB617BC6D45B7B6F28D62053792A27
  participant_packet_draft_adversarial_review_v0.md: 6ED3863E0325A331309EA5D9ABAB1CDB93BE13B6BF9627BD3D2B13A7CE7E8056
  safety_receipt_v0.md: CAACA6A9E55B17FFB7AF779ECA7E598BE2A8D2F2D706388CDFFD871E9B5FFAFC
  pydantic_schema_reference.md: CFFC7BCAC179B752B9A77204ECA6A6399D30DD7CB6B2C52533E3EC0FDC031D8D
open_next:
  - docs/research/judgment-spine/harness/v0_14/pydantic_schema_reference.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/evidence_registry_draft_v0.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/participant_packet_draft_v0.md
downstream_consumers:
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/memorization_probe_request_prep_v0.md
  - future unfrozen facilitator ledger draft or freeze candidate
stale_if:
  - Any input hash changes.
  - The v0.14 FacilitatorLedger schema changes.
  - The participant packet or evidence registry changes.
  - Owner changes target contestant families, probe policy, source set, or S7 inclusion.
  - Any value below is treated as frozen, schema-valid, score-ready, or participant-facing.
```

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_daimler_facilitator_ledger_work_queue
  edit_permission: docs-write
  target_scope:
    - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/facilitator_ledger_work_queue_v0.md
  dirty_state_checked: yes
  blocked_if_missing: no
```

- Status: `UNFROZEN_LEDGER_WORK_QUEUE_NOT_FACILITATOR_LEDGER`
- Case ID: `daimler_corporate_structure_vote_2019_v0_14`
- Fixture status: not admitted
- Blind-use status: blocked
- Probe status: not run
- Scoring status: not score-ready
- Ledger freeze hash: `NOT_COMPUTED`
- Participant visibility: facilitator internal only

## Boundary

This artifact is a facilitator-only work queue. It is not a schema-valid frozen `FacilitatorLedger`, not a scoring input, not a participant packet, not a memorization-probe request, not a blind-use contract, not fixture admission, and not proof of judgment quality.

It may mention candidate ledger surfaces and evidence IDs. It must not be copied into participant-facing material, and it must never be shown to GPT-5.5, Claude Opus, or any later target contestant family.

## Required Future FacilitatorLedger Fields

These fields follow `pydantic_schema_reference.md`. Current values are planning statuses only.

| Future field | Current work-queue status | Required before freeze |
| --- | --- | --- |
| `case_id` | Candidate fixed as `daimler_corporate_structure_vote_2019_v0_14`. | Confirm unchanged at freeze. |
| `batch_id` | Pending. Candidate stem: `daimler_corporate_structure_vote_2019_v0_14_draft_pack`. | Owner or fixture operator selects final batch ID. |
| `labeling_rubric_version` | Pending. | Pin the exact rubric version before primary label. |
| `mapping_table_version_pin` | Pending. | Pin the exact mapping table version before action-band derivation. |
| `ledger_authors` | Pending. | Name primary and second labelers; placeholders are not freeze-valid. |
| `second_label_diffs` | Not performed. | Run second-label process and record resolved diffs. |
| `frozen_band_inputs` | `NOT_FROZEN`. | Primary-label, second-label, resolve, and freeze every BandInputs enum. |
| `must_address_items` | Candidate-only list below. | Finalize item IDs and descriptions. |
| `underreach_observability` | Candidate questions below; not finalized. | Resolve `present`, valid `basis`, and notes. |
| `leakage_audit_notes` | Draft notes below. | Finalize after probe result and blind-use boundary checks. |
| `spoiler_inventory` | Draft inventory below. | Finalize before any ledger freeze. |
| `committed_at` | `NOT_COMMITTED`. | Set only at freeze as ISO-8601 UTC timestamp with `Z` suffix. |
| `ledger_freeze_hash` | `NOT_COMPUTED`. | Compute only from canonical frozen ledger minus hash field. |

## Protocol Metadata Work Items

These values are useful for the run protocol but are not direct current Pydantic `FacilitatorLedger` fields unless a later adapter or schema revision binds them.

```yaml
case_family:
  candidate: public_company_corporate_structure_governance_vote
  status: CANDIDATE_PROTOCOL_METADATA_NOT_FROZEN
decision_shape:
  candidate: action_band
  status: CANDIDATE_PROTOCOL_OR_BLIND_JUDGEMENT_METADATA_NOT_FROZEN
secondary_decision_shape_candidate:
  candidate: governance_approval_with_guardrails
  status: CANDIDATE_PROTOCOL_METADATA_NOT_FROZEN
memorization_probe_required:
  value: true
  status: PROTOCOL_LEAKAGE_INPUT_NOT_DIRECT_PYDANTIC_FIELD
known_fame_risk:
  candidate: lower_than_high_fame_consulting_cases_but_not_zero
  status: PROTOCOL_LEAKAGE_INPUT_NOT_DIRECT_PYDANTIC_FIELD
target_contestant_families_later:
  primary: GPT-5.5
  backup: Claude Opus
  status: CONTESTANT_EXPOSURE_BLOCKED_UNTIL_PROBE_PASS_AND_AUTHORIZATION
```

`decision_shape` must be frozen before any `BlindJudgement` adaptation or model run. `action_band` is the leading candidate because the participant must choose among approve, approve with guardrails, defer, or reject. The secondary lens is guardrail quality within a governance approval decision.

## Candidate Band-Input Work Items

No band input is frozen. The future labeler must review every row against the rubric before any ledger freeze.

| Band input | Candidate work item | Evidence and packet cues to review |
| --- | --- | --- |
| `evidence_strength` | Assess whether pre-cutoff evidence is moderate or strong. | DCSV-E01 through DCSV-E09 cover rationale, proposal mechanics, financial context, legal burden, divisional economics, and market framing, but not full annex-level transfer details. |
| `evidence_independence` | Assess partial independence. | Official company/governance materials dominate S1-S6; S7 adds independent pre-cutoff business-press framing. |
| `reversibility_feasibility` | Assess low to medium feasibility. | Legal entity separation, asset/liability transfers, employee commitments, IT/IP, treasury, and cross-border subsidiary work may be hard to unwind. |
| `reversibility_cost` | Assess high or ruinous only with evidence. | One-time costs, running costs, stakeholder commitments, and governance complexity are visible; ruinous cost is not established by current packet. |
| `authority` | Assess partial or full based on role-frame interpretation. | Participant is advising a large shareholder or board-level decision maker, but exact legal authority is not fully specified. |
| `authority_acquisition_cost` | Assess medium to high. | Shareholder/governance approval, employee representation, treasury, legal, and operational constraints imply multi-stakeholder authority costs. |
| `capability` | Assess partial. | Daimler has scale and management capability, but the packet does not prove execution readiness across all transfer mechanics. |
| `capability_build_cost` | Assess high. | More than 700 subsidiaries, contracts, public-law authorizations, IT/IP, and employee transfers create material execution burden. |
| `loss_shape` | Assess asymmetric_down unless stronger tail evidence appears. | Coordination drag, synergy loss, fixed-cost increase, and execution complexity create downside beyond ordinary reorganization cost. |
| `opportunity_cost` | Assess moderate. | Faster accountability, partnership flexibility, valuation clarity, and strategic optionality are visible, but no expiring window is established. |
| `information_decay` | Assess slow unless vote timing is treated as expiring. | More information may improve execution judgment, but the governance vote itself occurs at a fixed meeting. |
| `option_value` | Assess moderate to high. | Legal separation may increase partnership and capital-market optionality, but effectiveness is not proven. |
| `upside_shape` | Assess asymmetric_up only if optionality evidence is judged strong enough. | Valuation clarity and strategic optionality exist, but synergy risk cuts against broad upside claims. |
| `urgency` | Assess medium only if the shareholder-meeting timing is decision-critical. | Industry transition pressure exists, but current packet does not prove a crisis deadline beyond the vote date. |

Quarantine or review is required if second labeling produces more than three disagreements, any disagreement on `loss_shape` includes `ruinous_tail`, any disagreement on `information_decay` includes `expiring`, or resolution would require post-cutoff facts, source titles, URLs, outlet names, or later outcome material.

## Candidate Must-Address Items

These are candidate facilitator-side items only. They must not appear in the participant packet.

| ID | Candidate item | Candidate evidence references |
| --- | --- | --- |
| MA-DCSV-01 | The answer must distinguish legal separation from ordinary internal accountability reform. | DCSV-E01, DCSV-E02, DCSV-E03 |
| MA-DCSV-02 | The answer must weigh strategic focus and optionality against execution burden and synergy loss. | DCSV-E03, DCSV-E04, DCSV-E07, DCSV-E09 |
| MA-DCSV-03 | The answer must address stakeholder, employee, pension, and German investment commitments as both stabilizers and constraints. | DCSV-E04, DCSV-E07 |
| MA-DCSV-04 | The answer must treat treasury, rating, IT/IP, transfer mechanics, and withdrawal conditions as approval guardrail surfaces. | DCSV-E02, DCSV-E07 |
| MA-DCSV-05 | The answer must avoid hindsight from the final vote, later implementation, later corporate actions, consulting narrative, or outcome metrics. | Participant packet draft, safety receipt |

The current Pydantic `MustAddressItem` shape only defines `must_address_item_id` and `description`. Evidence references above are protocol traceability aids and must not be treated as schema-valid fields unless a later adapter binds them.

## Underreach Observability Work Item

Direct Pydantic field is not finalized.

```yaml
underreach_observability_candidate:
  present: TO_BE_LABELED
  valid_basis_values:
    - opportunity_cost
    - window_closure
    - information_decay
    - other
  notes_to_resolve: >
    Opportunity-cost and option-value pressure are visible through speed,
    accountability, partnership flexibility, valuation clarity, and strategic
    optionality. Underreach observability may be present if a defer/reject
    answer ignores the fixed shareholder-vote window or the cost of delaying
    divisional accountability. It may be absent or lower priority if execution
    burden and reversibility risks dominate. This must be resolved during
    primary/second labeling, not in this work queue.
```

## Leakage Audit Notes Draft

Draft `leakage_audit_notes` should carry these items forward:

- Participant packet draft hash: `5CC0D40F8D41F61360B07831B4D7B2BD22BB617BC6D45B7B6F28D62053792A27`.
- Participant packet draft adversarial review hash: `6ED3863E0325A331309EA5D9ABAB1CDB93BE13B6BF9627BD3D2B13A7CE7E8056`.
- Participant packet review found zero findings across frontmatter shape, source-manifest boundary, conversion fidelity, zero-spoiler boundary, S7 handling, and forbidden overclaims.
- Source titles, raw locators, local filenames, outlet names, byte sizes, source-byte hashes, retrieval timestamps, optional canonical residue, and 403 details are facilitator-only.
- S7 remains included as `S7 independent pre-cutoff business press`; original-wire/source-origin residue must not enter participant-facing material.
- Target contestant families later are GPT-5.5 primary and Claude Opus backup; neither may receive participant packet material before a same-family probe passes and blind-use authorization exists.
- `leakage_audit_notes.probe_result_status`: `not_run_or_pending`.
- Optional canonical residue remains facilitator-side only for DCSV-S1-CANONICAL, DCSV-S4A-CANONICAL, and DCSV-S7-ORIGINAL.

## Spoiler Inventory Draft

Draft advisory `spoiler_inventory`:

- final shareholder vote result;
- later implementation status;
- later corporate actions;
- later outcome metrics and market reaction;
- consulting-firm narrative and recommendation/action claims;
- source URLs, source titles, source filenames, outlet names, raw locators, byte sizes, source hashes, and true retrieval timestamps;
- optional canonical or original-source residue for S1, S4A, and S7;
- facilitator evidence registry summaries, band inputs, candidate must-address items, action band, action floor, action ceiling, and scoring material;
- memorization-probe result or model-family quarantine state once any later probe exists;
- owner critique, reveal readout, and outcome calibration once created.

## Freeze Blockers

```yaml
ledger_status: NOT_FROZEN
ledger_freeze_hash: NOT_COMPUTED
can_support_scoring: false
blocked_until:
  - batch_id is finalized
  - labeling_rubric_version is pinned
  - mapping_table_version_pin is pinned
  - primary labeler and second labeler are named
  - every BandInputs field is primary-labeled, second-labeled, diffed, resolved, and frozen
  - must-address items are finalized in schema-valid shape
  - underreach_observability is finalized
  - leakage_audit_notes and spoiler_inventory are finalized after probe handling
  - committed_at is set at freeze time as an ISO-8601 UTC timestamp with Z suffix
  - ledger_freeze_hash is computed from canonical frozen ledger minus the hash field
  - decision_shape is frozen for BlindJudgement adaptation
  - memorization probe passes for the target model family before contestant exposure
  - owner explicitly authorizes any ledger freeze or scoring path
```

## Non-Claims

- No schema-valid frozen FacilitatorLedger.
- No finalized band inputs.
- No finalized must-address items.
- No finalized underreach observability.
- No second-label audit.
- No action band derivation.
- No memorization-probe pass.
- No model run.
- No scoring readiness.
- No facilitator ledger freeze.
- No schema or runtime implementation.
- No fixture validation.
- No fixture admission.
- No product proof.
- No judgment-quality proof.

Required boundary: plumbing works only; not judgment quality.
