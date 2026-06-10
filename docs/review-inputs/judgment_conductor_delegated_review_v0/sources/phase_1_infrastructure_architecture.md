# Orca Phase 1 Infrastructure Architecture v0.14

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness v0.14 spec
scope: Phase 1 harness repository, module, and build-scope architecture for v0.14.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


## Purpose

This document freezes the Phase 1 MVP architecture for the Orca judgement harness.

v0.14 patches v0.12 by adding:

```yaml
v0_14_additions:
  - band input labeling rubric
  - facilitator ledger freeze/hash/disagreement fields
  - failure-event log stub
  - config manifests
  - Makefile / pyproject requirement
  - no LLM imports in scoring/** and reports/**
  - baseline runner collapse into contestant runner
```

## Architecture Freeze

```yaml
status: phase_1_architecture_freeze_candidate
scope: first_30_day_build
not_frozen: later_research_or_product_architecture
```

Changes after this point require an implementation blocker, not a strategy preference.

## Technology Choices

```yaml
language: Python
schema_style: Pydantic_style_typed_models
structured_file_format: YAML
human_readable_packet_format: Markdown
report_format_phase_1: YAML_dump
```

## Repo Layout

```text
orca-harness/
├── docs/
│   └── v0_14/
├── config/
│   ├── contestants.yaml
│   ├── models.yaml
│   └── prompts.yaml
├── schemas/
│   ├── case_models.py
│   ├── judgement_models.py
│   └── scoring_models.py
├── scoring/
│   ├── mapping_table.py
│   ├── band_scorer.py
│   └── evidence_id_checker.py
├── runners/
│   ├── run_case.py
│   ├── run_contestant.py
│   └── run_memorization_probe.py
├── prompts/
│   ├── raw_llm.md
│   ├── strong_single_prompt.md
│   ├── structured_pipeline.md
│   └── orca_harness_interface.md
├── cases/
│   └── plumbing/
│       ├── case_001_ceiling_trap/
│       ├── case_002_underreach_high_conviction/
│       ├── case_003_abstention_required/
│       ├── case_004_escalation_required/
│       └── case_005_unsupported_claim_trap/
├── reports/
│   └── plumbing/
├── memory/
│   └── logs/
│       └── failure_events.yaml
├── tests/
│   ├── unit/
│   │   ├── test_mapping_table.py
│   │   ├── test_schema_validation.py
│   │   ├── test_band_scorer.py
│   │   └── test_evidence_id_checker.py
│   ├── integration/
│   │   └── test_run_case_case001.py
│   └── contract/
│       ├── test_runner_artifacts.py
│       └── test_no_llm_imports_in_scoring.py
├── pyproject.toml
├── Makefile
└── README.md
```

## Entry Points

```yaml
make_targets:
  make_test: run unit/integration/contract tests
  make_run_case: run one case with configured contestants
  make_report: generate YAML report from existing run artifacts
  make_lint: enforce no LLM imports in scoring/** and reports/**
```

## Runner Policy

There is no separate baseline runner.

```yaml
runner_policy:
  single_runner: runners/run_contestant.py
  contestant_manifest: config/contestants.yaml
  reason: baselines are contestants with different prompts/configs
```

`run_baselines.py` is killed as a distinct module to prevent drift between baseline and harness execution paths.

## Phase 1 Contestants

```yaml
phase_1_contestants:
  required:
    raw_frontier_llm:
      role: model-only baseline

    strong_single_prompt:
      role: strongest short prompt baseline
      requirement: frozen_before_orca_specific_prompt_iteration

    fixed_structured_pipeline:
      role: same schema, no memory, no lifecycle

  optional_interface_only:
    orca_harness:
      role: harness candidate interface
      claim_limit: no superiority claim over fixed_structured_pipeline in Phase 1
```

## Phase 1 Build Scope

```yaml
build_now:
  - scoring/mapping_table.py
  - tests/test_mapping_table.py
  - band input labeling rubric
  - facilitator ledger schema with freeze/disagreement fields
  - schema validator
  - scoring/band_scorer.py
  - scoring/evidence_id_checker.py
  - runners/run_contestant.py
  - runners/run_memorization_probe.py
  - reports YAML dump generator
  - memory/logs/failure_events.yaml
  - five plumbing cases

defer:
  - semantic evidence checker
  - memory retrieval
  - rule promotion
  - scaled adversarial review
  - perturbation harness
  - polished dashboards
  - 30-50 case corpus
```

## Deterministic Boundary

```yaml
deterministic:
  - schema validation
  - action band derivation from frozen inputs
  - band scoring
  - evidence ID presence check
  - claim coverage by ID intersection
  - report YAML dump

llm_assisted:
  - contestant generation
  - optional advisory band-input proposal
  - memorization probe
  - later adversarial review

human_operator:
  - primary band input labeling
  - ledger freeze
  - ambiguous memorization probe review
```

## CI Guardrails

```yaml
ci_guardrails:
  no_llm_imports:
    paths:
      - scoring/**
      - reports/**

  mapping_version_pin_required: true
  ledger_freeze_hash_required: true
  scoring_result_must_include_version_hashes: true
```


---

# v0.14 Code-Readiness Patch

## Must Exist Before Coding

```yaml
required_before_code:
  - action_band_mapping_table_numbers.md
  - scorer_formula_spec.md
  - memorization_probe_protocol.md
  - pydantic_schema_reference.md
```

## New First Code Artifact Order

```yaml
first_files:
  1: pyproject.toml
  2: Makefile
  3: tests/contract/test_no_llm_imports.py
  4: schemas/case_models.py
  5: schemas/judgement_models.py
  6: schemas/scoring_models.py
  7: scoring/mapping_table.py
  8: tests/unit/test_mapping_table.py
```
