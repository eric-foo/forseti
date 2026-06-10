# Orca Failure Event Log Spec v0.14

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness v0.14 spec
scope: Phase 1 failure-event log schema and non-promotion policy for v0.14.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


## Purpose

Phase 1 needs failure logging, not rule memory.

The failure-event log records what happened during runs so later infrastructure can inspect repeated failures. It does **not** promote rules or claim compounding.

## Location

```text
memory/logs/failure_events.yaml
```

The `memory/` directory exists only for logs in Phase 1.

Forbidden Phase 1 directories:

```text
memory/rules/
memory/promoted/
memory/retrieval/
memory/judgement_memory/
```

## Allowed Claims

```yaml
allowed:
  - failure events were logged
  - repeated failure classes may be inspected later

forbidden:
  - Orca learned a rule
  - rule promoted
  - memory improved judgement
  - compounding memory demonstrated
```

## Failure Event Schema

```yaml
failure_event:
  event_id:
  created_at:
  harness_version: v0_14
  case_id:
  contestant_id:
  run_id:
  scoring_result_ref:

  failure_type:
    - schema_invalid
    - over_band
    - under_band
    - evidence_id_missing
    - post_decision_evidence_cited
    - must_address_item_missed
    - low_precision_band
    - memorization_probe_failed
    - memorization_probe_ambiguous
    - runner_failure
    - mapping_version_mismatch
    - ledger_label_disagreement
    - other

  severity:
    - info
    - minor
    - material
    - blocking

  mechanical_source:
    - schema_validator
    - mapping_table
    - band_scorer
    - evidence_id_checker
    - memorization_probe
    - runner
    - operator

  details:
    summary:
    related_fields:
    evidence_unit_ids:
    must_address_item_ids:
    recommended_level:
    action_floor:
    action_ceiling:

  not_a_rule: true
  promotion_allowed: false
```

## Logging Rules

```yaml
log_event_if:
  - schema validation fails
  - action recommendation is over_band
  - action recommendation is under_band
  - any cited evidence ID is missing
  - any cited evidence is excluded/post-decision
  - required must_address_item_id is missed
  - memorization probe fails or is ambiguous
  - mapping version mismatch blocks scoring
  - ledger label disagreement caused quarantine or warning
```

## Aggregation Allowed in Phase 1

```yaml
allowed_aggregation:
  - count events by failure_type
  - count events by contestant_id
  - count events by case_id
  - list blocking failures
  - inspect repeated failure types manually

forbidden_aggregation:
  - automatic rule creation
  - rule promotion
  - retrieval augmentation
  - compounding claim
```

## When real memory may begin

```yaml
real_memory_start_condition:
  - five plumbing cases run end-to-end
  - schema/scoring infrastructure stable
  - 30-50 cases in one family exist
  - baseline comparison is stable
  - repeated failure mode appears across cases
  - rule candidate has falsifier and ablation plan
```


---

# v0.14 Code-Readiness Patch

## File Format

```yaml
format: multi_document_yaml_stream
separator: '---'
append_only: true
event_id: ULID
```

Each event is one YAML document. No in-place edits. No deletions.

## Integrity Fields

```yaml
required_or_conditional:
  event_id: ULID
  created_at: ISO_8601_UTC_Z
  scoring_result_ref: ULID_or_null
  scoring_result_hash: sha256_or_null
  batch_id: optional_string
```

Logger must raise if `promotion_allowed` is true.
