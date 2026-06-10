# Daimler v0.14 Selected-Family Probe Gate Outcome Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record - facilitator-only probe gate outcome
scope: Records the selected-family memorization-probe gate outcome for the Daimler v0.14 fixture candidate after GPT-5.5 access blockage and Claude Opus probe failure.
use_when:
  - Checking whether any selected Daimler target family cleared the memorization-probe gate.
  - Deciding whether Daimler can proceed to blind-use entry contract planning for the selected family set.
  - Routing future Daimler fixture work without exposing participant or facilitator material to target contestants.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/daimler_v0_14_probe_execution_authorization_decision_v0.md
  - docs/decisions/daimler_v0_14_backup_probe_authorization_decision_v0.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/probes/claude_opus_backup_memorization_probe_result_v0.yaml
  - docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_claude_opus_probe_tool_isolation_adversarial_artifact_review_v0.md
input_hashes:
  docs/decisions/daimler_v0_14_probe_execution_authorization_decision_v0.md: A4D1B02D50C98A162ACE8ED3653E33BE7861DF2E42CEEE1E232F0C55760BBCF2
  docs/decisions/daimler_v0_14_backup_probe_authorization_decision_v0.md: 8E1C59F1E7E399441D1D67FEA69EDB76A8A006D5848E7A1768F509EC18E4F3FE
  docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/memorization_probe_request_prep_v0.md: 8AB7B3986A930D2E689053C7C347F1EDA4B8ECE3EB08B1FDF82521D8CB93C6A6
  docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md: 96B2EF245E6E92A11024D1BAD3B26C2C18B45283831B5D5C1ED209B30A55AF8A
  docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/probes/gpt_5_5_primary_memorization_probe_blocked_receipt_v0.yaml: 72473157D5E2612003A7F6F67B1B4DAF9DFFAE0813FE568522BABEF85259BB14
  docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/probes/gpt_5_5_primary_access_resolution_blocked_receipt_v0.yaml: 1BFB157851ADA9055819E537E7A7333734B51845DB8F2F4FF8A5408342C528B7
  docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/probes/claude_opus_backup_memorization_probe_result_v0.yaml: 19EBE50E68971117119826B6A66477DF741AC556D771E3B3CFFBABC096F63250
  docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_claude_opus_probe_tool_isolation_adversarial_artifact_review_v0.md: 2D4E2F304417759FA1EC143486327DF94F8E8FF06F6ABCEA4FC9734138632C93
branch_or_commit: main @ fb7f1a1cac09
downstream_consumers:
  - future Daimler fixture routing
  - future target-family selection decisions
  - future blind-use entry contract planning checks
stale_if:
  - Any input hash changes.
  - A valid GPT-5.5 primary-family probe result is later produced under a separately accepted authorization.
  - A new target contestant family is selected and separately authorized for a fresh same-family probe.
  - Any target contestant receives Daimler participant packet or facilitator material outside an authorized public-identifiers-only probe input.
```

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_daimler_selected_family_probe_gate_outcome
  edit_permission: docs-write
  target_scope:
    - docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Decision

```yaml
decision_id: daimler_v0_14_selected_family_probe_gate_outcome_decision_v0
decision_status: selected_family_probe_gate_closed_no_family_cleared
case_id: daimler_corporate_structure_vote_2019_v0_14
selected_family_set:
  primary: GPT-5.5
  backup: Claude Opus
family_outcomes:
  GPT-5.5:
    status: blocked_by_access_no_valid_probe_result
    probe_result: no_valid_probe_result
    participant_packet_exposed: false
    target_contestant_exposure: false
  Claude Opus:
    status: failed_memorization_probe
    status_caveat: gate_routing_label_not_verified_memorization_causality
    probe_model_id: claude-opus-4-8
    probe_result: fail
    tool_isolation_status: agent_harness_tool_isolation_unverified_no_tool_call_trace
    participant_packet_exposed: false
    target_contestant_exposure: public_identifiers_probe_only
gate_outcome:
  selected_family_probe_gate_status: no_selected_family_cleared
  blind_use_entry_contract_status: not_authorized
  participant_packet_exposure_status: not_authorized
  fixture_admission_status: not_admitted
  judgment_quality_status: not_claimed
```

No selected target family cleared the Daimler memorization-probe gate.

The GPT-5.5 primary lane remains access-blocked and produced no valid probe result. This is not a GPT-5.5 probe failure, because no valid GPT-5.5 probe response exists and no GPT-5.5 contestant-facing prompt was sent under the recorded receipts.

The Claude Opus backup lane produced a valid probe response through the authorized public-identifiers-only probe surface. The result artifact classifies the response as `fail` because the target model returned `recognition_status: recognized`, confidence `0.9`, and stated the actual post-cutoff outcome or later decision material. Under the v0.14 memorization-probe protocol, this invalidates the Claude Opus contestant-case pair for this Daimler fixture candidate as a gate-routing outcome.

Tool isolation was not structurally proven for the Claude Opus run because the probe used the Claude Code Agent tool harness and the recorded artifact did not capture a tool-call trace or explicit no-tools configuration. Therefore `failed_memorization_probe` is a conservative gate-routing label, not a verified causal claim that the output specifically came from training-data memorization rather than some unverified Agent-harness access path.

The probe gate therefore closes with no selected family cleared. Daimler must not proceed to blind-use entry contract planning, participant packet exposure, model judgment run, scoring, ledger freeze, validation, fixture admission, or judgment-quality claims for GPT-5.5 or Claude Opus under the current selected-family set.

## Boundary And Exposure State

```yaml
participant_packet_exposed_to_target_contestants: false
facilitator_material_exposed_to_target_contestants: false
source_manifest_or_evidence_registry_exposed_to_target_contestants: false
outcome_or_reveal_material_exposed_via_participant_packet: false
probe_result_material_visibility: facilitator_only
tool_isolation_caveat_visibility: facilitator_only
```

The blind packet boundary remains intact: the participant packet was not exposed to GPT-5.5, Claude Opus, or any other target contestant family. The failed Claude Opus probe does not contaminate the participant packet; it disqualifies the Claude Opus contestant-case pair for this case.

This decision itself is facilitator-only routing material. Do not show this decision, the probe result, probe summaries, quarantine state, or any probe failure rationale to any future target contestant.

## Consequences

```yaml
current_selected_family_consequence:
  GPT-5.5: no_probe_pass_access_blocked
  Claude Opus: reject_or_quarantine_for_this_case
  selected_family_set: closed_no_family_cleared
not_authorized:
  - rerun Claude Opus backup probe as a way to override the observed fail
  - expose participant packet to Claude Opus
  - expose participant packet to GPT-5.5
  - create blind-use entry contract for the selected family set
  - run model judgment
  - score outputs
  - freeze facilitator ledger
  - claim fixture admission
  - claim validation
  - claim judgment quality
possible_future_owner_decisions:
  - retire or park Daimler as a blind-run candidate for the current selected-family set
  - separately authorize a new target-family scouting decision
  - separately authorize a fresh probe only if a new family or a valid GPT-5.5 access path is explicitly selected and bounded
```

A future decision may revisit target-family selection, but this artifact does not authorize that work. Any future selected family must receive only an authorized public-identifiers-only memorization probe before any participant packet exposure.

The Claude Opus result should not be cited as proof of Claude Opus training-data memorization. It may be cited as a conservative gate-closing result from an Agent-harness probe with unverified tool isolation.

## Carried Friction

The tool-isolation adversarial review found that the gate consequence is correct but the label required a caveat:

- `TI-01`: the Agent harness tool set was undocumented and no tool-call trace was captured.
- `TI-02`: `failed_memorization_probe` overstates the causal proof if read as verified training-data memorization.
- `TI-05`: the gate outcome decision needed an explicit isolation caveat for downstream readers.

This patch carries that caveat here. The selected-family gate remains closed with no selected family cleared; no Opus rerun, packet exposure, blind-use entry, scoring, ledger freeze, validation, fixture admission, or judgment-quality claim is authorized.

The draft fixture pack still carries two minor advisory findings from the STEP-7 pack review:

- `PA-MIN-01`: evidence registry `unresolved_fields` retains a stale entry for participant packet conversion source-manifest mapping.
- `PA-MIN-02`: DCSV-E07 `pre_decision_basis` delegates to the safety receipt rather than stating an explicit date-based reason.

These remain deferred. They do not change the selected-family probe gate outcome, and they should not be patched merely to rescue the failed Claude Opus probe.

## Non-Claims

- No selected target family cleared the memorization-probe gate.
- No blind-use authorization.
- No participant packet exposure.
- No model judgment run.
- No scoring readiness.
- No facilitator ledger freeze.
- No schema or runtime implementation.
- No validation.
- No fixture admission.
- No product proof.
- No judgment-quality proof.

Required boundary: plumbing works only; not judgment quality.
