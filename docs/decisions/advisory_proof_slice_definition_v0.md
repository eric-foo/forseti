# Advisory Proof-Slice Definition v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: Internal advisory proof-slice definition for a non-gate-clearing Daimler Judgment Spine learning pass.
use_when:
  - Deciding whether the next Judgment Spine artifact should be an advisory runbook.
  - Checking the boundary between advisory subscription/manual/chat learning and gate-bearing harness evidence.
  - Preventing Daimler advisory work from being mistaken for fixture admission, validation, or judgment-quality proof.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md
  - docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_draft_fixture_pack_adversarial_artifact_review_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/advisory_proof_slice_definition_adversarial_artifact_review_v0.md
input_hashes:
  .agents/workflow-overlay/product-proof.md: 0EB8A11DAA2A2BE1FC7F610AAA48004D97200A18D11679F9C8D45731EED61F21
  docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md: A257AE82D36216EB9099D269C2EAD0587E9063764B9011C4F45229852678D344
  docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: 3301224649991811D91B8B5932F0DFF18D3E356CB51979619BDBE3494BC9193C
  docs/hygiene/precompact_orca_judgment_harness_first_output_v0.md: 8510A011D008C093BC16C39EDB724DC9584F28E1FEA326FF5705F2317BE812DC
  docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md: 4C7190CE9F12EE712CF08C536D513BB8A25F52C54D6B0A715E874113E524C693
  docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_draft_fixture_pack_adversarial_artifact_review_v0.md: D26E78306C3BCDAA1DE4168FBA92DA6E1E774382828839BE799977319402764C
  docs/review-outputs/adversarial-artifact-reviews/advisory_proof_slice_definition_adversarial_artifact_review_v0.md: 30F6C6B566A7D3E277A556056FCB23D3830C5B80FCA25A075013432164DB0FDA
branch_or_commit: main @ 829bbe0dc954
stale_if:
  - Daimler selected-family probe gate outcome changes.
  - A later accepted execution surface makes subscription/manual/chat runs gate-bearing.
  - Owner reopens the no-buyer-contact-before-full-spine-MVP constraint.
  - Owner selects a different proof slice or case.
  - Advisory proof-slice adversarial review report changes.
```

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: advisory_proof_slice_definition_scoping
  edit_permission: docs-write
  target_scope:
    - docs/decisions/advisory_proof_slice_definition_v0.md
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Decision

```yaml
proof_slice_id: advisory_proof_slice_daimler_internal_v0
case_or_slice: daimler_corporate_structure_vote_2019_v0_14
audience: owner_learning_internal_backtest_narration
execution_tier: tier_advisory_subscription_manual_chat
gate_bearing_status: non_gate_clearing
buyer_contact_status: not_authorized
runbook_status: not_written
model_run_status: not_authorized
judgment_quality_status: not_claimed
```

Daimler is the selected internal advisory proof slice for the next Judgment
Spine planning move.

This artifact contains facilitator-only Daimler routing facts: selected-family
probe-gate outcome and probe caveats. Do not show this artifact, or any
probe-gate or probe-caveat content from it, to GPT-5.5, Claude Opus, or any
future target contestant family.

This selection does not revive Daimler as a clean blind-run candidate for the
current selected model-family set. The selected-family probe gate is already
closed with no selected family cleared: GPT-5.5 is access-blocked with no valid
probe result, and Claude Opus returned a probe result classified as `fail`
under the v0.14 probe protocol. Tool isolation was not structurally proven for
the Claude Opus run because the Agent harness did not capture a tool-call trace;
therefore `failed_memorization_probe` is a conservative gate-routing label, not
verified evidence that the output came from training-data memorization
specifically rather than an unverified Agent-harness access path. Daimler may
therefore be used here only as an internal advisory learning slice unless a
later owner decision selects a new family or otherwise changes the gate state.

## Learning Question

Can a non-gate-clearing advisory run, using the Daimler zero-spoiler packet
shape as an internal substrate, show whether the Judgment Spine proof experience
is understandable, narratable, and decision-useful enough to justify the next
runbook or case-slice investment?

This learning question is about product and proof narration. It is not about
whether any model is good, whether the fixture is admitted, whether the harness
is validated, or whether the Daimler case proves judgment quality.

## Why Daimler

Daimler is the smallest useful slice because its draft fixture pack has already
passed a coherent STEP-7 adversarial artifact review with no critical or major
findings. The pack is useful for advisory learning because it has:

- a zero-spoiler participant packet draft;
- source acquisition and evidence-registry plumbing;
- a facilitator ledger work queue;
- memorization-probe request prep;
- explicit non-claims and gate boundaries;
- a recorded selected-family probe outcome that blocks clean blind use for the
  current family set.

That combination is exactly the point of the advisory slice: the case is rich
enough to test internal narrative and operator understanding, while the closed
probe gate prevents accidental overclaiming.

## Advisory Execution Tier

The only tier in scope for this proof slice is
`tier_advisory_subscription_manual_chat`.

Permitted later uses, if separately authorized:

- owner learning;
- internal readback of the Judgment Spine experience;
- non-gate-bearing comparison of how an advisory answer feels against the
  case packet;
- runbook-shape learning;
- identification of confusing packet, prompt, or narration surfaces.

Not permitted by this artifact:

- clean memorization-probe pass;
- blind-use authorization;
- participant packet exposure to any target contestant;
- model judgment run;
- scoring;
- ledger freeze;
- fixture validation or admission;
- product proof;
- judgment-quality claim;
- buyer-facing proof.

## Zero-Spoiler Lanes

```yaml
definition_touches:
  - docs-only advisory slice definition
  - public proof-boundary status of the Daimler draft pack
  - selected-family probe-gate outcome as a facilitator-only routing constraint

later_runbook_may_reference_after_separate_authorization:
  - participant_packet_draft_v0.md as the advisory packet substrate
  - subscription/manual/chat execution tier as non-gate-clearing
  - owner-learning readback questions

not_touched:
  - facilitator ledger freeze
  - source URLs, source titles, source filenames, hashes, byte sizes, or retrieval timestamps
  - evidence registry locators
  - outcome or reveal material
  - consulting narrative
  - post-cutoff facts
  - buyer contact
  - live provider/API execution
  - model judgment execution
  - scoring
```

If any later runbook exposes the Daimler participant packet to a subscription
or chat model, that exposure must be recorded as advisory and non-gate-clearing.
It must not be back-converted into clean blind-use evidence for that model,
family, account, or execution lane.

## Stop And Continue Criteria

Continue to advisory runbook scoping only if all of these remain true:

- the runbook is explicitly non-gate-clearing;
- the audience remains owner-learning or internal backtest narration;
- any participant-packet exposure is separately authorized;
- facilitator-only material remains excluded from participant-facing prompts;
- the runbook records that Daimler's selected-family gate is closed for the
  current family set;
- the runbook states that subscription/manual/chat output cannot support
  fixture admission, validation, blind-use readiness, or judgment-quality proof.

Stop if any of these occur:

- the artifact or runbook claims product proof, validation, fixture admission,
  blind-use readiness, scoring readiness, or judgment quality;
- the runbook treats subscription/manual/chat output as structurally isolated
  no-tools evidence;
- the runbook hides the Daimler probe-gate closure;
- the runbook proposes buyer contact before full-spine MVP authorization;
- the work starts solving API, runner, architecture, or source-system design
  instead of defining the advisory learning slice.

## Claim Boundary

Supported by this artifact:

- Daimler is selected as the internal advisory proof slice.
- The advisory slice is non-gate-clearing.
- The next appropriate artifact, if accepted, is an advisory runbook or runbook
  scope for owner-learning/internal backtest narration.

Not supported by this artifact:

- buyer validation;
- willingness-to-pay proof;
- repeatability proof;
- product readiness;
- feature readiness;
- implementation readiness;
- commercial readiness;
- Core Spine validation;
- clean memorization-probe pass;
- blind-use authorization;
- fixture validation or admission;
- model-run authorization;
- scoring readiness;
- facilitator ledger freeze;
- judgment-quality proof.

## Deferred Work

- advisory runbook scoping;
- advisory runbook drafting;
- any participant-packet exposure decision for advisory subscription/manual/chat
  use;
- any new target-family selection or probe path for Daimler;
- any gate-bearing API/harness run;
- any buyer-facing memo, deck, or contact;
- any architecture lane for durable advisory execution records.

Required boundary: plumbing works only; not judgment quality.
