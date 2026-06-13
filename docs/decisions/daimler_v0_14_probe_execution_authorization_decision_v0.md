# Daimler v0.14 Probe Execution Authorization Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: Owner decision authorizing only the next bounded Daimler primary-family memorization-probe execution lane.
use_when:
  - Checking whether Daimler probe execution has owner authorization.
  - Preparing a later public-identifiers-only memorization-probe execution prompt or run artifact.
  - Verifying that probe authorization does not authorize blind use, scoring, ledger freeze, fixture admission, or judgment-quality claims.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/memorization_probe_request_prep_v0.md
  - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
  - docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_draft_fixture_pack_adversarial_artifact_review_v0.md
input_hashes:
  docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_draft_fixture_pack_adversarial_artifact_review_v0.md: D26E78306C3BCDAA1DE4168FBA92DA6E1E774382828839BE799977319402764C
  docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/memorization_probe_request_prep_v0.md: 8AB7B3986A930D2E689053C7C347F1EDA4B8ECE3EB08B1FDF82521D8CB93C6A6
  docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md: 96B2EF245E6E92A11024D1BAD3B26C2C18B45283831B5D5C1ED209B30A55AF8A
  docs/research/judgment-spine/harness/v0_14/fixtures/daimler_corporate_structure_vote_2019_v0_14/participant_packet_draft_v0.md: 5CC0D40F8D41F61360B07831B4D7B2BD22BB617BC6D45B7B6F28D62053792A27
branch_or_commit: main @ fb7f1a1cac09
stale_if:
  - Any input hash changes.
  - Target contestant families, exact probe protocol, case ID, decision question, public identifiers, or cutoff change.
  - Any target contestant receives Daimler participant packet or facilitator material outside the authorized probe input.
```

## Decision

Owner instruction `proceed` on 2026-05-31 is accepted as authorization to create this decision record and to authorize the next bounded Daimler memorization-probe execution lane for the primary target family only.

```yaml
decision_id: daimler_v0_14_probe_execution_authorization_decision_v0
decision_status: accepted_for_primary_probe_execution_lane_only
case_id: daimler_corporate_structure_vote_2019_v0_14
authorized_probe_family:
  primary: GPT-5.5
backup_family_status:
  family: Claude Opus
  status: not_authorized_by_this_decision
authorized_action:
  - Prepare and run one public-identifiers-only v0.14 memorization probe for the primary family, in a separate execution lane.
  - Capture the exact resolved model ID or snapshot before or during the run.
  - Capture prompt hash, raw response hash, parsed response, probe result, created_at, and operator-review fields required by the memorization probe protocol.
  - Return the probe artifact or a blocked execution receipt.
```

This decision does not itself run the probe. It authorizes a later bounded execution step, provided every stop condition below is satisfied.

## Authorized Probe Input Boundary

The execution lane may use only the public-identifiers-only probe input from `memorization_probe_request_prep_v0.md` and the prompt template from `memorization_probe_protocol.md`.

Allowed probe input fields:

- `case_id`;
- `decision_question`;
- `public_identifiers_if_any`;
- `decision_date_or_cutoff`;
- `probe_model_family`;
- `probe_model_id`;
- `probe_prompt_template_version`.

For the primary-family run, `probe_model_family` must be GPT-5.5. The exact `probe_model_id` or snapshot remains unresolved and must be filled by the operator before or during the run.

## Stop Conditions

The execution lane must stop and return a blocked receipt if any of these occur:

- exact model ID or snapshot cannot be resolved or captured;
- prompt hash or raw response hash cannot be captured;
- the run would expose participant packet body text, source-manifest rows, source IDs, evidence registry content, facilitator ledger work queue content, review reports, source provenance, final vote result, implementation status, later actions, consulting narrative, outcome metrics, probe result/quarantine state, owner critique, reveal readout, or outcome calibration;
- the operator cannot preserve the same-family boundary;
- the result is ambiguous and requires operator review;
- the run fails before a valid response exists;
- any target contestant has already received Daimler participant packet or facilitator material outside the authorized public-identifiers-only probe input.

## Result Handling

```yaml
if_pass:
  status: primary_family_probe_pass_for_case_pair_only
  next_allowed_decision: owner may consider blind-use entry contract planning
  not_authorized:
    - automatic blind-use exposure
    - participant packet exposure without separate blind-use authorization
    - backup family use
    - model judgment run
    - scoring
    - fixture admission
if_fail:
  status: primary_family_reject_or_quarantine_for_this_case
  next_allowed_decision: owner may decide whether to authorize a fresh backup-family probe
if_ambiguous:
  status: quarantine_until_operator_review
  next_allowed_decision: tighten probe or review ambiguity before any contestant-facing packet exposure
if_blocked_or_not_run:
  status: no_probe_result
  next_allowed_decision: resolve blocker or retire probe lane
```

## Carried Friction

The STEP-7 pack review found two minor advisory findings:

- `PA-MIN-01`: evidence registry `unresolved_fields` retains a stale entry for participant packet conversion source-manifest mapping.
- `PA-MIN-02`: DCSV-E07 `pre_decision_basis` delegates to the safety receipt rather than stating an explicit date-based reason.

These do not block primary-family probe execution authorization. They should be addressed before facilitator ledger freeze planning.

## Non-Claims

- No memorization probe was run by this decision.
- No memorization probe passed.
- No target contestant exposure occurred.
- No blind-use contract was created.
- No participant packet exposure was authorized.
- No backup-family probe was authorized.
- No model judgment run was authorized.
- No scoring readiness.
- No facilitator ledger freeze.
- No schema or runtime implementation.
- No fixture validation.
- No fixture admission.
- No product proof.
- No judgment-quality proof.

Required boundary: plumbing works only; not judgment quality.
