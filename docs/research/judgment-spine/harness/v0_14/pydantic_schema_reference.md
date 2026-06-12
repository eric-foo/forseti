# Orca Phase 1 Pydantic Schema Reference v0.14

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness v0.14 spec
scope: Pydantic-ready schema contracts for v0.14.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


## Purpose

This document freezes the minimum Pydantic-ready schema contracts required before coding.

The Python files become implementation source of truth once created:

```text
schemas/case_models.py
schemas/judgement_models.py
schemas/scoring_models.py
```

## Core Types

```python
from enum import StrEnum
from pydantic import BaseModel, Field, model_validator
from typing import Optional, Literal
```

## Participant Packet Frontmatter

`participant_packet.md` must start with YAML frontmatter:

```yaml
---
case_id:
decision_question:
decision_date_or_cutoff:
role_frame:
authority_constraints:
capability_constraints:
permitted_assumptions:
information_boundary:
source_manifest:
  - source_id:
    source:
    retrieval_timestamp:
    hash:
---
```

## EvidenceUnit

```python
class PreDecisionStatus(StrEnum):
    VERIFIED_PRE_DECISION = "verified_pre_decision"
    UNCERTAIN_TIMESTAMP = "uncertain_timestamp"
    EXCLUDED = "excluded"

class EvidenceUnit(BaseModel):
    evidence_id: str
    source_id: str
    source: str
    timestamp: str
    retrieval_timestamp: str
    hash: str
    pre_decision_status: PreDecisionStatus
    pre_decision_basis: str
    summary: str
```

`hash` is `sha256(source_bytes)` when source bytes are available.

## BandInputs

All fields are required enums. No free text is allowed.

```python
class BandInputs(BaseModel):
    evidence_strength: Literal["none", "weak", "moderate", "strong"]
    evidence_independence: Literal["correlated", "partially_independent", "independent"]
    reversibility_feasibility: Literal["low", "medium", "high"]
    reversibility_cost: Literal["low", "medium", "high", "ruinous"]
    authority: Literal["absent", "partial", "full"]
    authority_acquisition_cost: Literal["low", "medium", "high", "impossible"]
    capability: Literal["absent", "partial", "full"]
    capability_build_cost: Literal["low", "medium", "high", "impossible"]
    loss_shape: Literal["symmetric", "asymmetric_down", "ruinous_tail", "unknown"]
    opportunity_cost: Literal["none", "low", "moderate", "severe"]
    information_decay: Literal["none", "slow", "fast", "expiring"]
    option_value: Literal["none", "low", "moderate", "high"]
    upside_shape: Literal["none", "symmetric", "asymmetric_up", "convex", "once_only_window"]
    urgency: Literal["none", "low", "medium", "critical"]
```

## FacilitatorLedger

```python
class SecondLabelDiff(BaseModel):
    input_name: str
    primary_label: str
    second_label: str
    final_label: str
    resolution_reason: str

class MustAddressItem(BaseModel):
    must_address_item_id: str
    description: str

class UnderreachObservability(BaseModel):
    present: bool
    basis: Optional[Literal["opportunity_cost", "window_closure", "information_decay", "other"]] = None
    notes: Optional[str] = None

class FacilitatorLedger(BaseModel):
    case_id: str
    batch_id: str
    labeling_rubric_version: str
    mapping_table_version_pin: str
    ledger_authors: list[str]
    second_label_diffs: list[SecondLabelDiff] = []
    frozen_band_inputs: BandInputs
    must_address_items: list[MustAddressItem] = []
    underreach_observability: UnderreachObservability
    leakage_audit_notes: Optional[str] = None
    spoiler_inventory: Optional[str] = None  # sealed facilitator-only; never enumerated in the ledger body or any participant packet
    committed_at: str  # ISO-8601 UTC, Z suffix
    ledger_freeze_hash: str
```

### Ledger Hash Rule

```yaml
ledger_freeze_hash: sha256(canonical_yaml_dump(ledger_minus_hash_field))
canonical_yaml_dump:
  sort_keys: true
  default_flow_style: false
  allow_unicode: true
  line_endings: LF
```

## Judgement Class to Ladder Mapping

```yaml
judgement_class_ladder_mapping:
  abstain:
    required_level: 0
  wait:
    required_level: 1
  escalate:
    required_level: 6
  irreducible_uncertainty:
    required_level: 0
    requires_must_address_coverage: true
  recommend:
    allowed_levels: [2, 3, 4, 5, 7, 8]
```

Invalid combinations are schema-invalid and create a `schema_invalid` failure event.

Examples:

```yaml
invalid:
  - judgement_class: abstain
    ladder_level: 5
  - judgement_class: recommend
    ladder_level: 6
  - judgement_class: wait
    ladder_level: 3
```

## BlindJudgement

```python
class RecommendedAction(BaseModel):
    ladder_level: int = Field(ge=0, le=8)
    action_label: str
    rationale: str

class EvidenceUsed(BaseModel):
    claim_id: str
    claim_text: str
    claim_role: Literal["load_bearing", "supporting", "contextual"]
    evidence_unit_ids: list[str]

class BlindJudgement(BaseModel):
    case_id: str
    contestant_id: str
    run_id: str
    model_id: str
    model_family: str
    model_snapshot_if_available: Optional[str] = None
    prompt_hash: str
    temperature: float
    seed_if_supported: Optional[int] = None
    harness_version: str
    judgement_class: Literal["recommend", "abstain", "wait", "escalate", "irreducible_uncertainty"]
    decision_shape: str
    recommended_action: RecommendedAction
    evidence_used: list[EvidenceUsed]
    must_address_items_covered: list[str] = []
    advisory_phase_1_fields: dict = {}

    @model_validator(mode="after")
    def validate_judgement_class_ladder(self): ...
```

Phase 1 advisory fields are optional and not used for primary scoring.

## ActionBandResult

```python
class BandStatus(StrEnum):
    NORMAL = "normal"
    LOW_PRECISION_BAND = "low_precision_band"
    CONFLICT_ESCALATE = "conflict_escalate"

class MappingTraceStep(BaseModel):
    step_name: str
    input_name: Optional[str] = None
    input_value: Optional[str] = None
    effect: str

class ActionBandResult(BaseModel):
    mapping_table_version: str
    action_floor: int = Field(ge=0, le=8)
    action_ceiling: int = Field(ge=0, le=8)
    band_status: BandStatus
    band_width: int
    mapping_trace: list[MappingTraceStep]
    warnings: list[str] = []
```

Band is inclusive:

```python
in_band = action_floor <= recommended_level <= action_ceiling
band_width = action_ceiling - action_floor
```

## ScoringResult

```python
class EvidenceIdCheckResult(BaseModel):
    evidence_id_presence_pass: bool
    pre_decision_status_pass: bool
    load_bearing_claim_citation_pass: bool
    missing_evidence_ids: list[str] = []
    excluded_evidence_ids_cited: list[str] = []
    uncertain_timestamp_evidence_ids_cited: list[str] = []

class MustAddressCoverageResult(BaseModel):
    pass_: bool = Field(alias="pass")
    covered_ids: list[str]
    missed_ids: list[str]

class ScoringResult(BaseModel):
    scoring_result_id: str  # ULID
    case_id: str
    contestant_id: str
    run_id: str
    blind_judgement_hash: str
    facilitator_ledger_hash: str
    participant_packet_hash: str
    mapping_table_version: str
    labeling_rubric_version: str
    action_band_result: ActionBandResult
    recommended_level: int
    in_band: bool
    over_band: bool
    under_band: bool
    overreach_distance: int
    underreach_distance: int
    underreach_primary: bool
    evidence_id_check_result: EvidenceIdCheckResult
    must_address_coverage_result: MustAddressCoverageResult
    memorization_probe_result: Literal["pass", "fail", "ambiguous", "not_run"]
    failure_event_ids: list[str] = []
    scored_at: str
    scorer_version: str
```

## CaseReport

```python
class ContestantScoreSummary(BaseModel):
    contestant_id: str
    run_id: str
    scoring_result_id: str
    in_band: bool
    over_band: bool
    under_band: bool
    overreach_distance: int
    underreach_distance: int
    blocking_failures: int

class CaseReport(BaseModel):
    case_id: str
    batch_id: str
    mapping_table_version: str
    facilitator_ledger_hash: str
    contestant_results: list[ContestantScoreSummary]
    failure_event_summary: dict
    generated_at: str
```

## FailureEvent

```python
class FailureEvent(BaseModel):
    event_id: str  # ULID
    created_at: str
    harness_version: str
    batch_id: Optional[str] = None
    case_id: Optional[str] = None
    contestant_id: Optional[str] = None
    run_id: Optional[str] = None
    scoring_result_ref: Optional[str] = None
    scoring_result_hash: Optional[str] = None
    failure_type: str
    severity: Literal["info", "minor", "material", "blocking"]
    mechanical_source: str
    details: dict
    not_a_rule: bool = True
    promotion_allowed: bool = False
```

Logger must raise if `promotion_allowed=True`.
