# Orca Scorer Formula Spec v0.14

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness v0.14 spec
scope: Band scoring formulas for v0.14 contestant outputs.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


## Purpose

This document freezes the deterministic Phase 1 scorer formulas.

## Band Inclusivity

The action band is inclusive.

```python
in_band = action_floor <= recommended_level <= action_ceiling
```

## Overreach / Underreach

```python
overreach_distance = max(0, recommended_level - action_ceiling)
underreach_distance = max(0, action_floor - recommended_level)
over_band = overreach_distance > 0
under_band = underreach_distance > 0
in_band = not over_band and not under_band
```

## Conflict Escalate

If `band_status == conflict_escalate`, the action band is always:

```yaml
action_floor: 6
action_ceiling: 6
```

So scoring compares recommendation against level 6.

```yaml
recommended_level: 6 -> in_band
recommended_level < 6 -> under_band
recommended_level > 6 -> over_band
```

## Underreach Primary Gate

Underreach is a primary Phase 1 failure only if the facilitator ledger marks:

```yaml
underreach_observability.present: true
```

Otherwise underreach is logged as advisory.

```python
underreach_primary = under_band and ledger.underreach_observability.present
```

## Mapping Version Mismatch

```yaml
if ledger.mapping_table_version_pin != MAPPING_TABLE_VERSION:
  raise MappingVersionMismatchError
```

If `allow_rescore=True`:

```yaml
behavior:
  - write new scoring_result
  - do not overwrite old scoring_result
  - log failure_event:
      failure_type: mapping_version_mismatch
      severity: info
```

## Evidence ID Checks

Phase 1 evidence checks are shallow and deterministic.

```yaml
evidence_id_presence_pass:
  fail_if: any cited evidence_unit_id missing from case evidence registry

pre_decision_status_pass:
  fail_if: any cited evidence has pre_decision_status == excluded
  warn_if: any cited evidence has pre_decision_status == uncertain_timestamp

load_bearing_claim_citation_pass:
  fail_if: claim_role == load_bearing AND evidence_unit_ids is empty

must_address_coverage_pass:
  pass_if: all ledger.must_address_item_ids are listed in blind_judgement.must_address_items_covered
```

## Phase 1 Non-Scores

These may be present in contestant output but are advisory only in Phase 1:

```yaml
advisory_only:
  - judgement_class_probabilities
  - severe_error_assessment
  - reversal_triggers
  - counterfactuals
  - semantic evidence support
```
