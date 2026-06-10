# Daimler Advisory Runbook v0

```yaml
retrieval_header_version: 1
artifact_role: Orca workflow record - facilitator-only advisory runbook draft
scope: Operator-facing runbook draft for a non-gate-clearing Daimler advisory learning pass.
use_when:
  - Preparing or reviewing a Daimler advisory learning pass without executing it.
  - Checking the separation between operator-only routing facts and any later model-facing material.
  - Preventing advisory subscription/manual/chat work from being mistaken for gate-bearing evidence.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/advisory_runbook_scope_daimler_v0.md
  - docs/decisions/advisory_proof_slice_definition_v0.md
  - docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md
  - docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/daimler_advisory_runbook_external_sonnet46_adversarial_artifact_review_v0.md
input_hashes:
  docs/decisions/advisory_runbook_scope_daimler_v0.md: 4F9662DBD38A598204926EE12ED1B3A8C1011D45AAAD987A3FBA6DB1F99446B6
  docs/decisions/advisory_proof_slice_definition_v0.md: D758106977180863653E2ED6612082C3E87D9AC228C57F37BB63C5C6C3515119
  docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md: A257AE82D36216EB9099D269C2EAD0587E9063764B9011C4F45229852678D344
  docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: 3301224649991811D91B8B5932F0DFF18D3E356CB51979619BDBE3494BC9193C
  docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md: 4C7190CE9F12EE712CF08C536D513BB8A25F52C54D6B0A715E874113E524C693
  docs/review-outputs/adversarial-artifact-reviews/daimler_advisory_runbook_external_sonnet46_adversarial_artifact_review_v0.md: 1D72CB24E0952E9E389008131AF5B102DF62B90AF4DD54440EC670C3E5E90E3A
branch_or_commit: main @ 829bbe0dc954
downstream_consumers:
  - future Daimler advisory run authorization decision
  - future runbook adversarial artifact review
stale_if:
  - advisory_runbook_scope_daimler_v0.md changes.
  - advisory_proof_slice_definition_v0.md changes.
  - judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md changes.
  - Daimler selected-family probe gate outcome changes.
  - Owner authorizes participant-packet exposure, model execution, buyer contact, API execution, or gate-bearing use.
  - This runbook has not received adversarial artifact review before use.
```

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_daimler_advisory_runbook_draft
  edit_permission: docs-write
  target_scope:
    - docs/workflows/daimler_advisory_runbook_v0.md
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Operator-Only Warning

This runbook is facilitator-only operator material. It contains Daimler routing
facts and selected-family gate status that must not be shown to GPT-5.5,
Claude Opus, or any future target contestant family.

Do not paste this runbook, the upstream proof-slice definition, the runbook
scope, the selected-family gate outcome decision, probe results, probe
caveats, facilitator-ledger material, source registry material, or review
reports into any model-facing or participant-facing context.

## Purpose And Advisory Boundary

This runbook describes how an operator would prepare and record a
non-gate-clearing Daimler advisory learning pass for owner/internal readback.
It is meant to clarify what the Judgment Spine proof experience feels like,
where the operator friction appears, and what later artifacts would be needed
before any real run.

This runbook does not authorize the advisory pass itself. It does not authorize
participant-packet exposure, model execution, API execution, buyer contact,
scoring, ledger freeze, fixture validation, fixture admission, product proof,
blind-use readiness, or judgment-quality claims.

The advisory tier in scope is subscription/manual/chat only. That tier can be
useful for owner learning and product narration, but it cannot by itself clear
a memorization probe, authorize blind use, validate a fixture, admit a fixture,
prove product value, or prove judgment quality.

## Source And Slice Prerequisites

Before a later operator asks for any real advisory run authorization, load or
fresh-check these sources:

- `docs/decisions/advisory_runbook_scope_daimler_v0.md`
- `docs/decisions/advisory_proof_slice_definition_v0.md`
- `docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md`
- `docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md`
- `docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md`
- the adversarial artifact review report for this runbook, once it exists

Do not open the Daimler participant packet unless the owner has separately
authorized participant-packet exposure for a specific advisory run. Do not open
facilitator-ledger, evidence-registry, source-locator, outcome, reveal, or
calibration material for model-facing prompt construction.

## Participant-Safe Input Boundary

A later advisory run may use the Daimler participant packet draft only after
separate owner authorization for that exact exposure. Until that authorization
exists, the participant packet is a referenced substrate, not an input to be
opened, pasted, summarized, transformed, or executed.

Any later model-facing material must exclude:

- selected-family probe gate outcome;
- GPT-5.5 access blockage;
- Claude Opus probe result, caveats, or failure rationale;
- probe summaries, quarantine state, or gate routing;
- facilitator ledger work queue material;
- evidence registry locators;
- source URLs, titles, filenames, hashes, byte sizes, or retrieval timestamps;
- outcome, reveal, implementation, consulting, or post-cutoff material;
- this runbook's operator-only warning and non-claim discussion.

If an operator cannot separate model-facing material from operator-only
material, stop and do not run the advisory pass.

## Operator Setup Checklist

Use this checklist only for preparing an authorization request. It is not
permission to run anything.

```yaml
advisory_setup_checklist:
  run_purpose_named: false
  owner_authorized_specific_advisory_run: false
  participant_packet_exposure_authorized: false
  model_or_provider_selection_authorized: false
  model_facing_prompt_material_separated_from_operator_material: false
  facilitator_only_material_excluded_from_model_context: false
  output_capture_location_named: false
  non_gate_clearing_label_ready: false
  stop_conditions_rechecked: false
```

All fields must be true in a later authorization record before a real advisory
run may occur. This runbook does not flip any field to true.

## Advisory Prompt Assembly - Deferred Placeholder

Model-facing prompt assembly is deferred. This runbook intentionally does not
provide executable prompt text, runtime-model selection, provider selection,
packet text, source excerpts, scoring rubric text, or copy-ready instructions
for a model.

A later prompt assembly artifact, if separately authorized, must be a distinct
artifact or clearly separated section that contains only participant-safe
material. It must not carry the facilitator-only routing facts in this runbook.

Minimum later prompt-assembly requirements:

- cite the separate authorization decision that permits participant-packet
  exposure for the specific advisory run;
- name the input artifact without pasting it into operator-only context;
- mark the run as advisory and non-gate-clearing before any task instruction;
- omit all facilitator-only probe, source, ledger, outcome, reveal, and review
  material;
- record that subscription/manual/chat output cannot become clean no-tools
  execution evidence.

## Response Capture Notes

If a later advisory run is separately authorized and completed, capture only
operator-facing advisory notes unless the authorization record names a more
specific capture artifact.

The following are non-binding capture considerations, not a schema, template,
receipt, or required field list:

- run identifier;
- authorization artifact;
- operator;
- run date and time;
- advisory execution tier;
- participant-packet exposure authorization;
- model or provider, only if separately authorized;
- model-facing material hash or location, only if separately authorized;
- response location;
- operator readback notes;
- owner readback notes;
- stop or quarantine events;
- non-gate-clearing label.

These considerations do not create an execution record architecture, schema
requirement, validation gate, or gate-bearing receipt.

## Owner Readback Questions

After a later advisory run, the owner readback should stay focused on learning,
not proof.

- Was the packet experience understandable without source/provenance help?
- Where did the operator feel tempted to explain facilitator-only context?
- Which parts of the advisory answer felt useful, confusing, or overconfident?
- Did the answer make the Judgment Spine product experience easier to narrate?
- What artifact would have reduced the most operator friction?
- What would need to be true before a buyer-facing proof artifact could be
  considered?
- What must remain impossible to claim from this advisory run?

## Stop And Quarantine Conditions

Stop immediately and quarantine the draft or run notes if any of these occur:

- this runbook or any upstream facilitator-only artifact is pasted into a
  model-facing context;
- the participant packet is opened, pasted, summarized, transformed, or run
  before separate authorization;
- any target contestant receives probe-gate, probe-caveat, source-registry,
  facilitator-ledger, outcome, reveal, implementation, consulting, or
  post-cutoff material;
- the operator starts choosing a runtime model, model family, provider, or API
  path without separate authorization;
- the output content, label, storage location, summary, citation, or downstream
  use treats advisory material as validation, scoring readiness, fixture
  admission, product proof, blind-use readiness, clean no-tools evidence, or
  judgment quality;
- the runbook starts designing durable execution-record architecture instead of
  documenting advisory operation;
- buyer-facing memo, deck, or contact enters scope.

Quarantined material may be kept as operator scratch, but it must not be used
as participant-facing material, gate-bearing evidence, product proof, or
judgment-quality evidence.

## Separate Authorization Gates

These gates remain separate and closed unless a later owner decision opens
them explicitly:

```yaml
authorization_gates:
  adversarial_review_before_use:
    status: closed_by_this_runbook
    required_later_artifact: adversarial artifact review for the current runbook version before use
  participant_packet_exposure:
    status: closed_by_this_runbook
    required_later_artifact: specific owner authorization for the advisory run
  model_or_provider_selection:
    status: closed_by_this_runbook
    required_later_artifact: specific owner authorization naming the advisory execution path
  advisory_run_execution:
    status: closed_by_this_runbook
    required_later_artifact: advisory run authorization record
  response_capture_artifact_creation:
    status: closed_by_this_runbook
    required_later_artifact: advisory run authorization record that names the capture artifact scope
  api_or_gate_bearing_execution:
    status: closed_by_this_runbook
    required_later_artifact: gate-bearing execution authorization under contestant_no_tools_execution_contract_v0.md
  buyer_contact_or_buyer_facing_artifact:
    status: closed_by_this_runbook
    required_later_artifact: buyer-facing proof or discovery authorization
  scoring_or_ledger_freeze:
    status: closed_by_this_runbook
    required_later_artifact: separate harness authorization
```

## Review Requirement Before Use

This runbook draft must receive adversarial artifact review before it is used
as an operator instruction source for a real advisory run. The review should
check:

- operator-only versus model-facing separation;
- participant-packet exposure gate;
- advisory versus gate-bearing boundary;
- facilitator-only Daimler routing boundary;
- no buyer-contact and no product-proof boundary;
- stop/quarantine conditions;
- retrieval metadata and stale-source handling.

## Non-Claims

- No advisory run is authorized.
- No participant packet is exposed.
- No target contestant is exposed.
- No model or provider is selected.
- No model run is authorized or performed.
- No API run is authorized or performed.
- No response capture artifact is created.
- No scoring.
- No facilitator ledger freeze.
- No schema or runtime implementation.
- No validation.
- No fixture admission.
- No blind-use readiness.
- No product proof.
- No buyer validation.
- No buyer-facing memo, deck, or contact.
- No judgment-quality claim.

## Residual Questions

- What exact owner authorization shape should open a later advisory run, if any?
- Should the later advisory run use a fresh case instead of Daimler to avoid
  selected-family routing baggage?
- What capture artifact is sufficient for owner learning without becoming an
  execution-record architecture?
- What, if anything, from an advisory answer would justify returning to
  gate-bearing harness work?

Required boundary: plumbing works only; not judgment quality.
