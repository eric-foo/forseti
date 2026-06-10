# Orca Judgement Case Construction Protocol v0.14

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness v0.14 spec
scope: Case construction protocol for v0.14 Judgment Harness cases.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


## Purpose

This protocol creates cases for the Phase 1 judgement harness.

v0.14 narrows case construction to five plumbing cases and adds ledger labeling discipline.

## Four-Lane Structure

```yaml
participant_packet:
  visible_to: contestants
  format: Markdown
  purpose: pre-decision evidence and role frame

facilitator_ledger:
  visible_to: scorer/operator only
  format: YAML
  purpose: frozen band inputs, labeling audit, must-address items, leakage notes, scoring labels

blind_judgement:
  produced_by: contestant
  format: YAML
  purpose: schema-validated judgement output

scoring_result:
  produced_by: scorer
  format: YAML
  purpose: mechanical score against frozen ledger and mapping table
```

## Case Folder Contract

```text
cases/<batch>/<case_id>/
├── participant_packet.md
├── facilitator_ledger.yaml
├── evidence/
│   ├── e001.yaml
│   └── ...
├── probes/
├── runs/
└── scores/
```

## Participant Packet Must Include

```yaml
participant_packet_must_include:
  - case_id
  - decision_question
  - decision_date_or_cutoff
  - role_frame
  - authority_constraints
  - capability_constraints
  - evidence_units
  - known_uncertainties
  - source_manifest
  - permitted_assumptions
  - forbidden_information_notice
```

## Participant Packet Must Not Include

```yaml
participant_packet_must_not_include:
  - actual_outcome
  - actual_decision_if_avoidable
  - frozen_band_inputs
  - derived_floor
  - derived_ceiling
  - must_address_items
  - hidden_severe_error_labels
  - decoy_labels
  - post_decision_interpretation
```

## Facilitator Ledger Required Fields

```yaml
facilitator_ledger:
  case_id:
  case_family:
  decision_shape:
  mapping_table_version_pin:
  labeling_rubric_version: v0_14

  ledger_authors:
    primary_labeler:
    second_labeler:
    second_labeler_type:
      - human_operator
      - separate_model_family_advisory

  frozen_band_inputs:
    evidence_strength:
    evidence_independence:
    reversibility_feasibility:
    reversibility_cost:
    authority:
    authority_acquisition_cost:
    capability:
    capability_build_cost:
    loss_shape:
    opportunity_cost:
    information_decay:
    option_value:
    upside_shape:
    urgency:

  second_label_diffs:
    - input_name:
      primary_label:
      second_label:
      final_label:
      resolution_reason:

  must_address_items:
    - must_address_item_id:
      description:
      evidence_unit_ids:

  underreach_observability:
    present: true | false
    basis:
      - opportunity_cost
      - window_closure
      - information_decay
      - option_value_loss
      - other
    evidence_unit_ids:

  leakage_audit:
    memorization_probe_required:
    known_fame_risk:
    spoiler_inventory:

  ledger_freeze_hash:
  committed_at:
```

## Evidence Unit Required Fields

```yaml
evidence_unit:
  evidence_id:
  source:
  source_type:
  timestamp:
  retrieval_timestamp:
  hash:
  pre_decision_status:
    - verified_pre_decision
    - uncertain_timestamp
    - excluded
  pre_decision_basis:
  summary:
```

## First Five Plumbing Cases

```yaml
case_001_ceiling_trap:
  purpose: exercise overreach scorer
  required_fixture:
    - ceiling <= 3
    - participant packet tempts action level 5+
    - correlated or weak evidence appears stronger than it is

case_002_underreach_high_conviction:
  purpose: exercise underreach scorer
  required_fixture:
    - observable opportunity cost or expiring window
    - underreach_observability.present: true
    - participant packet makes action pressure visible but not obvious

case_003_abstention_required:
  purpose: exercise abstention / non-decision path
  required_fixture:
    - weak or missing evidence
    - no serious opportunity cost or information decay
    - must_address_items include what remains justified now

case_004_escalation_required:
  purpose: exercise conflict escalation path
  required_fixture:
    - floor pressure exceeds ceiling constraint
    - conflict_escalate status expected from mapping table

case_005_unsupported_claim_trap:
  purpose: exercise evidence ID checker and claim coverage
  required_fixture:
    - tempting narrative claim unsupported by evidence units
    - must_address_items require substantiation
    - careless output should cite missing/no evidence or skip required item
```

## Optional Sixth Fixture

```yaml
case_006_low_precision_band:
  status: optional
  purpose: exercise low_precision_band path
  build_if: low_precision_band path is not covered by unit tests or existing five cases
```

## Case Acceptance Criteria

```yaml
accept_if:
  - participant packet excludes hidden labels
  - facilitator ledger includes complete frozen band inputs
  - labeling rubric version is present
  - second_label_diffs logged, even if empty
  - ledger_freeze_hash present
  - evidence units have IDs and pre-decision basis
  - mapping_table_version_pin present

reject_or_quarantine_if:
  - more than 3 band input disagreements before resolution
  - disagreement involves ruinous_tail or expiring labels and cannot be resolved
  - memorization probe fails or is ambiguous without operator review
  - underreach case lacks observable opportunity cost/window closure
```


---

# v0.14 Code-Readiness Patch

## Participant Packet Frontmatter

`participant_packet.md` must start with YAML frontmatter containing:

```yaml
case_id:
decision_question:
decision_date_or_cutoff:
role_frame:
authority_constraints:
capability_constraints:
permitted_assumptions:
forbidden_information_notice:
source_manifest:
```

## Ledger Hash

```yaml
ledger_freeze_hash: sha256(canonical_yaml_dump(ledger_minus_hash_field))
```

Canonical dump uses sorted keys, LF line endings, and UTF-8.
