# Daimler Memorization Probe Request Prep v0

```yaml
retrieval_header_version: 1
artifact_role: Research artifact - facilitator-only probe request prep
scope: Docs-only memorization-probe request preparation for the Daimler corporate-structure vote v0.14 fixture candidate.
use_when:
  - Preparing a later model-family scoped memorization probe request.
  - Checking pre-probe contamination boundaries before contestant exposure.
  - Reviewing pass, fail, ambiguous, quarantine, and same-family handling before any probe run.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/participant_packet_draft_v0.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/facilitator_ledger_work_queue_v0.md
input_hashes:
  docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md: 96B2EF245E6E92A11024D1BAD3B26C2C18B45283831B5D5C1ED209B30A55AF8A
  docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/fixture_entry_plan_v0.md: AC2669BFAFEAF44DBFF00DB6486F5214B877333596F629F914084EB69C1F2782
  docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/participant_packet_draft_v0.md: 5CC0D40F8D41F61360B07831B4D7B2BD22BB617BC6D45B7B6F28D62053792A27
  docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_participant_packet_draft_adversarial_artifact_review_v0.md: 6ED3863E0325A331309EA5D9ABAB1CDB93BE13B6BF9627BD3D2B13A7CE7E8056
  docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/facilitator_ledger_work_queue_v0.md: B4872A7D3AAF730FFB5D708B4B82CC5AEF5CBA7C54DAE4B10A4BE0A85D377610
  docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_facilitator_ledger_work_queue_post_patch_adversarial_recheck_v0.md: 133B4455378334AD4A22B694134945E46AEA0030B0204DE4845ED487D7F0E65C
branch_or_commit: main @ fe8156efb0f3
downstream_consumers:
  - later authorized memorization probe request or run artifact
  - later draft fixture pack review
  - future blind-use entry contract planning
stale_if:
  - Any input hash changes.
  - The memorization probe protocol changes.
  - The participant packet decision question, cutoff, or public identifiers change.
  - Target contestant families change.
  - Any target contestant family receives Daimler participant packet or facilitator material before a same-family probe pass and blind-use authorization.
```

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom_daimler_memorization_probe_request_prep
  edit_permission: docs-write
  target_scope:
    - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/memorization_probe_request_prep_v0.md
  dirty_state_checked: yes
  blocked_if_missing: no
```

- Status: `PROBE_REQUEST_PREP_ONLY_NOT_PROBE_RUN`
- Case ID: `daimler_corporate_structure_vote_2019_v0_14`
- Fixture status: not admitted
- Blind-use status: blocked
- Probe execution status: not run
- Probe result status: not available
- Target contestant exposure status: blocked
- Participant visibility: facilitator/operator planning only

## Boundary

This artifact prepares the later memorization-probe request surface. It is not a probe run, not a probe result artifact, not a blind-use contract, not a participant packet, not a model-run prompt, not scoring input, not fixture admission, and not proof of judgment quality.

This artifact itself is facilitator/operator planning material. It must not be sent to GPT-5.5, Claude Opus, or any later target contestant family. A later authorized probe may send only the public-identifiers-only probe material defined below through the v0.14 memorization probe template.

## Probe Input Draft

```yaml
probe_input_status: prepared_not_run
probe_targets:
  primary_family: GPT-5.5
  backup_family: Claude Opus
  note: >
    A single probe run uses one family. Before each run, use the corresponding
    per-family probe_input_template below, resolved with the operator-supplied
    probe_model_id. Do not run both families simultaneously. A pass for one
    family does not authorize the other; the backup requires a fresh same-family
    probe.
probe_input_template_primary:
  case_id: daimler_corporate_structure_vote_2019_v0_14
  decision_question: >
    Should Daimler shareholders approve the proposed hive-down of the Cars & Vans
    and Trucks & Buses businesses into legally independent operating entities
    under Daimler AG, or should they condition, defer, or reject the proposal?
  public_identifiers_if_any:
    - Daimler AG
    - corporate-structure / hive-down shareholder vote
    - May 22, 2019 annual shareholder meeting
  decision_date_or_cutoff: 2019-05-21 23:59 CEST
  probe_model_family: GPT-5.5
  probe_model_id: OWNER_OR_OPERATOR_TO_RESOLVE_BEFORE_PROBE_RUN
  model_snapshot_if_available: OWNER_OR_OPERATOR_TO_CAPTURE_BEFORE_OR_DURING_PROBE_RUN
  probe_prompt_template_version: memorization_probe_protocol.md#probe-prompt-template-v0_14
probe_input_template_backup:
  case_id: daimler_corporate_structure_vote_2019_v0_14
  decision_question: >
    Should Daimler shareholders approve the proposed hive-down of the Cars & Vans
    and Trucks & Buses businesses into legally independent operating entities
    under Daimler AG, or should they condition, defer, or reject the proposal?
  public_identifiers_if_any:
    - Daimler AG
    - corporate-structure / hive-down shareholder vote
    - May 22, 2019 annual shareholder meeting
  decision_date_or_cutoff: 2019-05-21 23:59 CEST
  probe_model_family: Claude Opus
  probe_model_id: OWNER_OR_OPERATOR_TO_RESOLVE_BEFORE_PROBE_RUN
  model_snapshot_if_available: OWNER_OR_OPERATOR_TO_CAPTURE_BEFORE_OR_DURING_PROBE_RUN
  probe_prompt_template_version: memorization_probe_protocol.md#probe-prompt-template-v0_14
```

The probe question and identifiers above are the only Daimler case facts prepared for a later target-contestant probe. Do not add participant packet body text, source-manifest rows, source IDs, source titles, URLs, local filenames, source hashes, retrieval timestamps, evidence-registry summaries, facilitator-ledger work items, final vote results, implementation status, consulting narrative, later corporate actions, or outcome metrics to the probe prompt.

## Same-Family Rule

The probe is contestant-case-pair specific.

- A GPT-5.5 probe result applies only to GPT-5.5, using the exact model ID or snapshot captured for that probe.
- A Claude Opus probe result applies only to Claude Opus, using the exact model ID or snapshot captured for that probe.
- A pass for one family does not authorize the other family.
- The later blind judgment, if separately authorized, must use the same family and locked model ID or snapshot that passed the probe.
- If the exact model ID, snapshot, or comparable reproducibility metadata cannot be captured, record the blocker before any participant packet exposure.

## Result Handling

```yaml
probe_result_handling:
  pass:
    condition: recognition_status == unknown OR claimed_outcome is empty/generic/incorrect
    case_status_for_that_family: usable_for_that_model_family_after_owner_blind_use_authorization
    does_not_mean:
      - no memorization is proven
      - blind-use is automatically authorized
      - fixture admission is complete
      - judgment quality is proven
  fail:
    condition: model states the actual outcome, actual decision, or case-specific post-decision interpretation with confidence >= 0.50
    case_status_for_that_family: reject_or_quarantine_for_that_model_family
    required_event:
      failure_type: memorization_probe_failed
      severity: blocking
  ambiguous:
    condition:
      - model partially identifies the case but does not reveal outcome
      - model gives a near-miss outcome
      - model names highly specific entities that imply contamination but no outcome
    case_status_for_that_family: quarantine_until_operator_review
    required_event:
      failure_type: memorization_probe_ambiguous
      severity: material
  blocked_or_not_run:
    condition: probe has not been authorized, model ID is unresolved, metadata capture is unavailable, or execution fails before a valid response exists
    case_status_for_that_family: not_usable_until_resolved
```

If a result is ambiguous, do not expose the participant packet. Tighten the probe or send the ambiguity to owner/operator review before any further contestant-facing step.

If a result fails, do not expose that family to the participant packet for this case. Move to the backup family only through a fresh same-family probe.

## Expected Probe Artifact Metadata

These fields are reserved for a later authorized probe artifact. They are intentionally not filled here.

```yaml
memorization_probe_artifact_slots:
  probe_id: TO_BE_ASSIGNED_BY_LATER_AUTHORIZED_RUN
  case_id: daimler_corporate_structure_vote_2019_v0_14
  probe_model_family: TO_BE_FILLED_BY_LATER_AUTHORIZED_RUN
  probe_model_id: TO_BE_FILLED_BY_LATER_AUTHORIZED_RUN
  model_snapshot_if_available: TO_BE_FILLED_BY_LATER_AUTHORIZED_RUN
  system_fingerprint_if_available: TO_BE_FILLED_BY_LATER_AUTHORIZED_RUN
  seed_if_supported: TO_BE_FILLED_BY_LATER_AUTHORIZED_RUN
  prompt_hash: TO_BE_COMPUTED_BY_LATER_AUTHORIZED_RUN
  raw_response_hash: TO_BE_COMPUTED_BY_LATER_AUTHORIZED_RUN
  parsed_response:
    recognition_status: TO_BE_PARSED_BY_LATER_AUTHORIZED_RUN
    claimed_outcome: TO_BE_PARSED_BY_LATER_AUTHORIZED_RUN
    confidence: TO_BE_PARSED_BY_LATER_AUTHORIZED_RUN
    notes: TO_BE_PARSED_BY_LATER_AUTHORIZED_RUN
  probe_result: TO_BE_FILLED_BY_LATER_AUTHORIZED_RUN
  reviewed_by_operator: false
  operator_review_status: not_started
  operator_review_notes: NOT_APPLICABLE_UNTIL_PROBE_EXISTS
  created_at: TO_BE_SET_BY_LATER_AUTHORIZED_RUN
```

## Exposure Controls

Before a same-family probe pass and separate blind-use authorization, target contestant families must not receive:

- the participant packet body;
- source-manifest rows or source IDs;
- evidence registry content;
- facilitator ledger work queue content, including band inputs, candidate must-address
  items, action band, action floor, action ceiling, and scoring material;
- review reports or review summaries;
- source titles, URLs, local filenames, byte sizes, source hashes, or retrieval timestamps;
- source-origin, outlet residue, or optional canonical source residue for any source
  (including DCSV-S1, DCSV-S4A, and DCSV-S7);
- final vote result, implementation status, later corporate actions, consulting narrative, or outcome metrics;
- memorization-probe result, probe artifact, or model-family quarantine state for this
  case, once any later probe exists;
- owner critique, reveal readout, or outcome calibration, once created.

After a same-family probe pass and separate blind-use authorization, the only intended contestant-facing Daimler artifact is the participant packet draft or its separately authorized successor. Facilitator artifacts remain forbidden to contestants.

## Next Gate

The next docs-only gate is adversarial artifact review of this prep artifact before any probe execution authorization. The review should check:

- protocol-field fidelity;
- public-identifiers-only probe material;
- same-family handling;
- pass/fail/ambiguous quarantine rules;
- metadata slots and hash discipline;
- absence of probe execution, model-run, scoring, ledger-freeze, validation, fixture-admission, blind-use-readiness, or judgment-quality claims.

## Non-Claims

- No memorization probe was run.
- No memorization probe passed.
- No target contestant exposure was authorized.
- No blind-use contract was created.
- No model run was authorized.
- No scoring readiness.
- No facilitator ledger freeze.
- No schema or runtime implementation.
- No fixture validation.
- No fixture admission.
- No product proof.
- No judgment-quality proof.

Required boundary: plumbing works only; not judgment quality.
