# Contestant No-Tools Execution Contract v0

```yaml
retrieval_header_version: 1
artifact_role: Judgment Harness v0.14 local execution contract
scope: No-tools execution evidence and receipt-provenance contract for contestant memorization probes and blind judgment runs.
use_when:
  - Deciding whether a contestant probe or blind judgment execution can clear a gate.
  - Recording whether tool isolation was proven, unproven, or violated.
  - Interpreting Agent-harness or API-harness probe results without laundering live retrieval as model prior knowledge.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md
  - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
  - docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_claude_opus_probe_tool_isolation_adversarial_artifact_review_v0.md
input_hashes:
  docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md: 7862F03D0DA8DB6D845DF47FAA7940D89C2B27C8A27204C41744ECD3AC7B4C61
  docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_claude_opus_probe_tool_isolation_adversarial_artifact_review_v0.md: 2D4E2F304417759FA1EC143486327DF94F8E8FF06F6ABCEA4FC9734138632C93
  docs/review-outputs/adversarial-artifact-reviews/contestant_no_tools_execution_contract_external_adversarial_artifact_review_v0.md: E5BFA4AE34F99E00EB7DD9C626991407746A2057AA914E1374013471A45F90A7
  docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md: 4C7190CE9F12EE712CF08C536D513BB8A25F52C54D6B0A715E874113E524C693
  docs/review-outputs/no_tools_execution_foundation_blind_spot_adversarial_review_v0.md: 9D426F7458653466CE262BC81DC0F178EC22E4F5DDCEFCEE5C523435D5BAF8E9
branch_or_commit: main @ fb7f1a1cac09
downstream_consumers:
  - memorization probe execution receipts
  - blind-use entry contract planning checks
  - contestant-run isolation audits
stale_if:
  - judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md changes pre-sale evidence-tier routing.
  - memorization_probe_protocol.md changes its probe_result semantics.
  - a runtime runner or API wrapper becomes the controlling execution surface.
  - an overlay decision moves contestant execution isolation out of this harness-local contract.
```

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_v0_14_no_tools_execution_contract
  edit_permission: docs-write
  target_scope:
    - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
    - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
    - docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
    - docs/research/judgment-spine/harness/v0_14/index.md
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Purpose

This contract prevents a contestant probe or blind judgment run from being
treated as clean merely because the prompt told the model not to search. A
gate-clearing contestant execution needs structural evidence that web search,
browser tools, filesystem/workspace access, external retrieval, and hidden
context channels were unavailable or disabled.

It also records the receipt-provenance boundary: a computed
`gate_interpretation: pass_valid` or `isolation_result: proven` is not, by
itself, proof that a receipt came from a live isolated provider execution. A
receipt can clear a contestant case gate only when its execution provenance is
bound by an authorized live execution record, or when a later schema/runtime
contract supersedes this docs-only rule.

This contract is docs-only. It does not implement a runner hook, call a model,
authorize a probe, authorize a blind judgment, score an output, freeze a
ledger, admit a fixture, or prove judgment quality.

## Pre-Sale Evidence Tier Boundary

This contract does not make raw API the default model-use path for pre-sale
Judgment Spine work. Subscription, manual, or chat-based execution can be
adequate for advisory learning, product demonstration, buyer conversation,
scouting, or owner readback when no clean gate-bearing claim is made.

Gate-bearing claims still require structural evidence under this contract. Raw
API is the current accepted live execution surface that can satisfy this
evidence when separately authorized, but it is optional plumbing, not a
universal prerequisite for pre-sale work. A later accepted non-API execution
surface may satisfy this contract if it records equivalent no-tools isolation
and provenance.

## Applies To

```yaml
applies_to:
  - public-identifiers-only memorization probes
  - blind judgment contestant runs
  - any future contestant-facing rerun used to clear a harness gate
does_not_apply_to:
  - source acquisition by facilitator lanes
  - adversarial artifact review lanes
  - non-contestant docs-only planning lanes
  - facilitator ledger authoring
```

## Required Execution Fields

Contestant execution receipts that are used for gate decisions must record
these fields or explicitly mark the execution unable to clear the relevant
gate.

```yaml
contestant_execution_isolation:
  tool_access_policy: no_tools | tools_available | unknown
  tool_config_evidence:
  tool_call_trace_status: empty_trace | unavailable | non_empty_trace | not_applicable
  web_search_disabled: true | false | unknown
  browser_tools_disabled: true | false | unknown
  filesystem_workspace_access_disabled: true | false | unknown
  external_retrieval_disabled: true | false | unknown
  hidden_context_boundary:
  isolation_result: proven | not_proven | violated
```

Field meanings:

| Field | Required meaning |
| --- | --- |
| `tool_access_policy` | Whether the contestant was configured with no tools, with tools, or with unknown tool state. |
| `tool_config_evidence` | The concrete evidence source for the tool policy, such as API parameters, runner config, provider trace, or operator-visible harness setting. Prompt text alone is insufficient. |
| `tool_call_trace_status` | Whether the execution has an empty tool-call trace, no available trace, a non-empty trace, or a context where tool traces are structurally not applicable under the rule below. |
| `web_search_disabled` | Whether web search was structurally disabled. |
| `browser_tools_disabled` | Whether browser/navigation tools were structurally disabled. |
| `filesystem_workspace_access_disabled` | Whether the contestant could read local workspace files. |
| `external_retrieval_disabled` | Whether the contestant could call any external retrieval surface. |
| `hidden_context_boundary` | The evidence that the contestant received only the intended prompt context and no facilitator, packet, source, or outcome material. |
| `isolation_result` | The normalized isolation classification used by downstream gate logic. |

Tool trace classification rule:

- `empty_trace` means a tool-call trace was available and showed no tool calls.
- `unavailable` means a tool-call trace could exist for the execution path, but
  was not captured or exposed to the operator.
- `non_empty_trace` means the available trace shows one or more tool calls.
- `not_applicable` is valid only when the execution environment structurally
  cannot invoke tools regardless of configuration, such as a raw API call where
  no tool schema or retrieval channel is supplied. Agent harnesses, browser
  harnesses, API wrappers, or other execution paths where tools could
  theoretically be present must use `unavailable` unless the receipt records
  concrete configuration evidence that no tool schema, tool channel, browser
  tool, filesystem/workspace access, or external retrieval surface was offered.

## Isolation Result Semantics

```yaml
isolation_result:
  proven:
    required_conditions:
      - tool_access_policy == no_tools
      - tool_call_trace_status == empty_trace OR tool_call_trace_status == not_applicable
      - web_search_disabled == true
      - browser_tools_disabled == true
      - filesystem_workspace_access_disabled == true
      - external_retrieval_disabled == true
      - hidden_context_boundary is recorded
    meaning: Structural no-tools execution evidence is present.

  not_proven:
    condition: >
      The execution may have been clean, but one or more required evidence
      fields is unavailable, unknown, or recorded only as prompt instruction or
      model self-report.
    meaning: The execution cannot support a clean gate-clearing pass.

  violated:
    condition: >
      A tool was available and used, a tool-call trace is non-empty, live
      retrieval occurred, workspace files were accessible and used, or hidden
      context outside the authorized prompt was exposed.
    meaning: The execution is invalid for clean contestant gate purposes.
```

## Probe Classification Contract

The v0.14 memorization probe's recognition evaluation still determines whether
the response is behaviorally `pass`, `fail`, or `ambiguous`. This contract adds
the execution-isolation layer needed before a gate consequence is trusted.

```yaml
probe_gate_interpretation:
  pass_valid:
    condition:
      - probe_result == pass
      - isolation_result == proven
    gate_effect: contestant-case pair may proceed to the next separately authorized gate for that same family and model ID.

  fail_gate_closing:
    condition:
      - probe_result == fail
      - isolation_result == proven
    gate_effect: contestant-case pair is rejected or quarantined for that family.
    claim_boundary: may be cited as a clean memorization-probe fail, not as judgment-quality evidence.

  fail_gate_closing_with_caveat:
    condition:
      - probe_result == fail
      - isolation_result == not_proven
    gate_effect: contestant-case pair is rejected or quarantined for that family as a conservative gate-routing outcome.
    claim_boundary: must not be cited as proof of training-data memorization specifically.

  invalid_for_clean_pass:
    condition:
      - probe_result == pass OR probe_result == ambiguous
      - isolation_result == not_proven
    gate_effect: cannot clear the gate; rerun only under separate authorization with structural isolation evidence.

  execution_invalid_tool_violation:
    condition:
      - isolation_result == violated
    gate_effect: cannot clear the gate and cannot be used as a clean memorization-probe result.
```

## Receipt Provenance Boundary

Clean-looking receipt fields are not self-certifying. A receipt that computes
`isolation_result: proven` and `gate_interpretation: pass_valid` can support a
contestant gate only when the run provenance is also auditable.

Raw API is one accepted gate-eligible live execution surface, not a mandate to
use API for all pre-sale model work. When raw API is separately authorized for a
gate-bearing run, its live receipts must have all of the following:

- separate owner authorization for the exact model family, model ID or
  snapshot, account or credential lane, endpoint, and case or smoke-test
  purpose;
- production by the live raw-API runner or a later accepted execution surface
  that satisfies this contract;
- a standard endpoint accepted by the runner's endpoint allow-list;
- an out-of-band operator record binding provider, endpoint URL, UTC run
  timestamp, process exit status, full console output, `prompt_hash`, and
  `raw_response_hash` to the receipt.

Dry-runner receipts, local fixture receipts, manually normalized receipts, and
operator-authored receipts are not gate-clearing live execution evidence even
when their computed gate fields say `pass_valid`. They may be useful as
plumbing checks, but they cannot be cited as a clean memorization-probe pass,
blind-use gate clearance, fixture validation, fixture admission, product proof,
or judgment-quality evidence.

No-case smoke-test receipts are permanently non-gate-clearing. They can confirm
raw-API plumbing only under
`no_case_smoke_test_authorization_checklist_v0.md`; they must not be reused as
evidence for any real model/case pair.

## Blind Judgment Contract

A blind judgment run must satisfy `isolation_result: proven` before its output
can be treated as a clean blind contestant output. If a blind judgment run has
`isolation_result: not_proven` or `violated`, the run cannot support blind-use
readiness, scoring, validation, fixture admission, or judgment-quality claims.

## Insufficient Evidence

These are not enough to prove no-tools isolation:

- prompt text instructing the model not to browse or search;
- a new thread with memory or shared context disabled;
- model self-report that it did not search;
- absence of citations in the model response;
- absence of visible tool output in chat without a tool-call trace or tool
  configuration evidence;
- operator belief that a harness normally runs without tools.

## Runtime Hook Boundary

This contract names what evidence a future hook, runner, API wrapper, or manual
execution receipt must provide. It does not choose the hook mechanism. Future
implementation may satisfy this contract with API parameters, sandbox policy,
tool-denial launch configuration, provider/tool traces, or another auditable
execution record, but this document does not authorize building any of those
systems.

Subscription, manual, or chat-based runs remain advisory unless a later
accepted execution surface records equivalent no-tools isolation and provenance.
They are not automatically gate-clearing merely because they are useful for
pre-sale work.

## Direction Change Propagation - Receipt Provenance Patch

```yaml
direction_change_propagation:
  doctrine_changed: >
    Gate-clearing contestant receipts now require auditable execution
    provenance; computed pass_valid/proven fields alone are not
    self-certifying live execution evidence.
  trigger: validation_philosophy
  controlling_sources_updated:
    - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
    - docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
    - docs/research/judgment-spine/harness/v0_14/index.md
    - orca-harness/README.md
    - orca-harness/docs/v0_14/README.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/artifact-roles.md
    - .agents/workflow-overlay/retrieval-metadata.md
    - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
    - docs/review-outputs/no_tools_execution_foundation_blind_spot_adversarial_review_v0.md
  intentionally_not_updated:
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The change is a harness-v0.14 local receipt-provenance rule, not a
        project-wide validation gate for every Orca artifact.
    - path: docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
      reason: >
        The existing protocol still owns probe-result semantics; the new rule
        is execution-receipt provenance and belongs in this paired contract plus
        the no-case smoke-test checklist.
  stale_language_search: >
    rg -n "pass_valid|raw_api_no_tools|no-case smoke|smoke test|gate-clearing|gate clearing|self-certifying|execution provenance|raw_response_hash|prompt_hash"
    docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
    docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
    docs/research/judgment-spine/harness/v0_14/index.md
    docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
    orca-harness/README.md
    orca-harness/docs/v0_14/README.md
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not live-call authorization
    - not fixture admission
```

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    v0.14 contestant probe and blind judgment gate clearing now requires
    structural no-tools isolation evidence; prompt-only no-search language is
    insufficient for clean pass semantics.
  trigger: validation_philosophy
  controlling_sources_updated:
    - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
    - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
    - docs/research/judgment-spine/harness/v0_14/index.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/workflow-overlay/review-lanes.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/research/judgment-spine/harness/v0_14/review_prompts/
  intentionally_not_updated:
    - path: .agents/workflow-overlay/validation-gates.md
      reason: >
        The change is harness-v0.14 local execution doctrine, not a project-wide
        overlay gate for all Orca artifacts.
    - path: docs/workflows/orca_repo_map_v0.md
      reason: >
        The existing map already routes Judgment Harness work to the v0_14
        folder; the v0_14 index is the narrower navigation surface for this
        contract.
  stale_language_search: >
    rg -n "prompt.*search|do not search|no-tools|no tools|tool isolation|tool-call|tool_call_trace|failed_memorization_probe|Probe passing|memorization probe|pass_valid|probe_result == pass|usable_for_that_model_family"
    docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
    docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
    docs/research/judgment-spine/harness/v0_14/index.md
    docs/research/judgment-spine/harness/v0_14/review_prompts
    docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md
    docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_claude_opus_probe_tool_isolation_adversarial_artifact_review_v0.md
    docs/workflows/orca_repo_map_v0.md
    .agents/workflow-overlay/validation-gates.md
  stale_language_search_result: >
    Executed on 2026-06-01 after external review AR-02. Harness-local
    review_prompts were included. The only review_prompt hit was
    opus_code_ready_sanity_review_prompt.md naming "memorization probe
    protocol"; no stale prompt-only pass, clean-pass bypass, or old
    probe_result-pass-sufficient language was found there. Hits in Daimler
    decision/review outputs are intentional historical caveats and carried
    friction, not governing clean-pass semantics.
  non_claims:
    - not validation
    - not readiness
    - not implementation authorization
    - not fixture admission
```

## Non-Claims

- This contract does not run a probe.
- This contract does not pass or fail any model family.
- This contract does not authorize participant packet exposure.
- This contract does not authorize model judgment runs.
- This contract does not authorize scoring.
- This contract does not freeze a facilitator ledger.
- This contract does not implement schema or runtime code.
- This contract does not validate a fixture.
- This contract does not admit a fixture.
- This contract does not prove product readiness.
- This contract does not prove judgment quality.

Required boundary: plumbing works only; not judgment quality.
