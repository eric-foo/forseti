# Judgment Spine Pre-Sale Execution Evidence Tier Policy v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: Pre-sale Judgment Spine model-execution evidence tiers and API-optional routing.
use_when:
  - Choosing subscription/manual/chat versus API or harness execution for pre-sale Judgment Spine work.
  - Interpreting no-case smoke-test and raw-API runner artifacts relative to buyer proof.
  - Deciding whether a model run can support a gate-bearing no-tools or blind-use claim.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
  - docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
  - docs/product/data_capture_spine/data_capture_source_access_method_plan_v0.md
branch_or_commit: main @ 392f7935c029
stale_if:
  - A buyer or owner explicitly requires API-grade execution provenance for the next pre-sale proof step.
  - A later accepted execution surface records no-tools isolation and provenance without raw API.
  - contestant_no_tools_execution_contract_v0.md changes gate-bearing evidence semantics.
```

## Decision

For pre-sale Judgment Spine work, Orca's default model-use posture is
subscription, manual, or chat-based execution where that is adequate for
advisory learning, product demonstration, buyer conversation, scouting, or
owner readback.

Raw API and harness execution remain in-bounds, but they are optional
gate-bearing plumbing, not the default pre-sale sequence. Use them only when an
explicit owner or customer decision needs API-grade execution provenance,
structural no-tools evidence, replayable model metadata, or a gate-bearing
claim.

This decision preserves the raw-API runner and no-case smoke-test work as useful
plumbing. It does not turn that plumbing into a standing requirement for all
pre-sale work.

## Evidence Tiers

```yaml
execution_evidence_tiers:
  tier_advisory_subscription_manual_chat:
    default_for_pre_sale_when_adequate: true
    permitted_uses:
      - product conversation
      - scouting
      - demo narration
      - owner learning
      - non-gate-bearing comparison
    cannot_support_by_itself:
      - clean memorization-probe pass
      - blind-use authorization
      - fixture validation or admission
      - scoring readiness
      - product proof
      - judgment-quality claim

  tier_gate_bearing_execution_evidence:
    default_for_pre_sale_when_adequate: false
    current_accepted_surface: raw API or another later accepted execution surface
    requires:
      - explicit owner or customer agreement for the run
      - exact model family and model ID or snapshot
      - no-tools isolation evidence
      - prompt and response hash binding
      - out-of-band provenance where schema does not yet store it
    may_support_when_all_gates_are_met:
      - clean memorization-probe routing
      - blind-use gate consideration

  tier_no_case_smoke:
    default_for_pre_sale_when_adequate: false
    role: plumbing-only provider/runner check
    permanently_non_gate_clearing: true
```

## Routing Rule

Start pre-sale Judgment Spine work with the lightest evidence tier that matches
the claim being made.

- If the work is advisory, exploratory, demonstrative, or buyer-conversation
  oriented, subscription/manual/chat execution is acceptable unless the owner or
  buyer asks for stricter provenance.
- If the work will claim clean no-tools execution, memorization-probe pass,
  blind-use readiness, fixture validation/admission, product proof, or judgment
  quality, use the gate-bearing evidence tier and follow
  `contestant_no_tools_execution_contract_v0.md`.
- If the work only needs to check runner/provider plumbing, a no-case smoke test
  may be used after separate authorization, but it remains non-gate-clearing.

## Non-Claims

- This decision does not run a model.
- This decision does not authorize a live provider call.
- This decision does not authorize participant packet exposure.
- This decision does not make subscription/manual/chat output gate-clearing.
- This decision does not make raw API mandatory for pre-sale work.
- This decision does not authorize scoring.
- This decision does not freeze a facilitator ledger.
- This decision does not validate or admit a fixture.
- This decision does not prove product readiness.
- This decision does not prove judgment quality.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Pre-sale Judgment Spine model execution now separates advisory
    subscription/manual/chat use from optional gate-bearing API or harness
    execution evidence; raw API is preserved as plumbing, not default sequence.
  trigger: validation_philosophy
  controlling_sources_updated:
    - docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md
    - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
    - docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
    - docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/artifact-roles.md
    - docs/product/data_capture_source_access_method_plan_v0.md
  intentionally_not_updated:
    - path: docs/product/data_capture_source_access_method_plan_v0.md
      reason: >
        It already records the parallel source-access policy: manual,
        subscription, and local-first are pre-sale default; API remains
        in-bounds but requires explicit justification.
    - path: orca-harness/runners/run_memorization_probe_raw_api.py
      reason: >
        Runtime behavior is unchanged; this patch changes routing doctrine, not
        runner implementation.
  stale_language_search: >
    rg -n "API.*default|default.*API|must use API|API.*required|raw-API.*default|subscription.*gate-clearing|manual.*gate-clearing|chat.*gate-clearing|API.*disallowed|API.*prohibited"
    docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md
    docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
    docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
    docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md
    docs/product/data_capture_source_access_method_plan_v0.md
  stale_language_search_result: >
    Executed on 2026-06-01 after adversarial review AR-02. Hits were expected
    non-default, optional-plumbing, and non-gate-clearing statements, plus the
    recorded query itself. No stale API-mandatory/default route, API-ban
    overcorrection, or subscription/manual/chat gate-clearing language was
    found in the checked surfaces.
  non_claims:
    - not validation
    - not readiness
    - not live-call authorization
    - not fixture admission
    - not judgment-quality proof
```

Required boundary: plumbing works only; not judgment quality.
