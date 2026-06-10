# No-Case Smoke Test Authorization Checklist v0

```yaml
retrieval_header_version: 1
artifact_role: Judgment Harness v0.14 no-case smoke-test operator checklist
scope: Non-gate-clearing no-case smoke-test inputs, authorization boundary, and provenance capture for raw-API execution plumbing.
use_when:
  - Considering or authorizing a no-case raw-API provider smoke test.
  - Preparing the operator record for a one-shot no-tools smoke test.
  - Checking that a smoke receipt is not being cited as a real case probe pass.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
  - docs/research/judgment-spine/harness/v0_14/memorization_probe_protocol.md
  - docs/review-outputs/no_tools_execution_foundation_blind_spot_adversarial_review_v0.md
downstream_consumers:
  - no-case smoke-test authorization decisions
  - raw-API runner operator closeouts
  - future fresh-case memorization-probe authorization checks
stale_if:
  - judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md changes no-case smoke-test routing.
  - contestant_no_tools_execution_contract_v0.md changes receipt-provenance or gate-clearing semantics.
  - run_memorization_probe_raw_api.py changes its endpoint allow-list, request-shape validation, or receipt fields.
  - MemorizationProbeArtifact records live execution provenance directly in schema.
```

## Purpose

This checklist defines the smallest auditable no-case smoke test for the
v0.14 raw-API no-tools execution path.

A no-case smoke test is a plumbing-only live provider call with synthetic
inputs. It confirms that the runner can submit a no-tools request, receive a
provider response, parse it, hash it, and write or visibly refuse a receipt.
It is not a memorization probe, not a blind judgment run, not a case gate, and
not evidence about any model/case pair.

This checklist does not authorize a live call by itself. A later owner
decision must fill the concrete authorization fields before an operator may
pass `--allow-live-provider-call`.

This checklist is optional plumbing. It should not be selected merely because
pre-sale Judgment Spine work is underway or because the raw-API runner exists.
Use it only when the owner or buyer separately wants a no-case provider/runner
plumbing check; it does not replace subscription/manual/chat as the default
pre-sale advisory path where that path is adequate.

## Synthetic Input Convention

Smoke-test probe inputs must be visibly synthetic and must not name a real
case, real company, real dispute, real transaction, real vote, or real source.

```yaml
case_id: SMOKE_NOCASE_<provider_or_model>_<yyyymmdd>_<short_run_id>
decision_question: "Synthetic no-case plumbing question: should placeholder option A be selected?"
public_identifiers_if_any:
  - SYNTHETIC_NO_CASE_IDENTIFIERS_NONE
decision_date_or_cutoff: SYNTHETIC_NO_CASE_CUTOFF_NOT_A_REAL_CASE
probe_model_family: <authorized provider/model family>
probe_model_id: <authorized exact model id or snapshot>
probe_prompt_template_version: v0.14_no_case_smoke
```

The reserved `SMOKE_NOCASE_` prefix marks the receipt as permanently
non-gate-clearing. It must not be used for a real case folder or a real
memorization-probe run.

## Non-Gate-Clearing Rule

Even if a smoke receipt computes `probe_result: pass`,
`isolation_result: proven`, and `gate_interpretation: pass_valid`, the result
is plumbing confirmation only.

A no-case smoke receipt must never be cited as:

- a clean memorization-probe pass for any model/case pair;
- blind-use authorization;
- participant-packet exposure authorization;
- fixture validation or fixture admission;
- scoring readiness;
- ledger-freeze evidence;
- product proof;
- judgment-quality evidence.

## Required Concrete Authorization Fields

Before any smoke test is run, the owner authorization or operator record must
fill these concrete fields:

```yaml
authorized_provider: <openai_responses | anthropic_messages>
authorized_model_family: <provider family>
authorized_model_id_or_snapshot: <exact model id or snapshot>
authorized_account_or_credential_lane: <account label or API-key environment-variable name only>
authorized_endpoint_url: <exact endpoint URL accepted by the runner>
authorized_runner_path: orca-harness/runners/run_memorization_probe_raw_api.py
authorized_output_path: <intended smoke receipt path>
authorization_scope: one_shot_no_case_smoke_test_only
participant_packet_exposure_authorized: false
real_case_probe_authorized: false
blind_judgment_authorized: false
```

If any field is missing or ambiguous, the smoke test is blocked. Do not infer
provider access, endpoint choice, credential lane, model ID, or output path
from local environment state.

## Out-of-Band Provenance Capture

Because the v0.14 receipt schema does not yet record live execution provenance
directly, the operator must capture a separate provenance record alongside the
smoke receipt.

The provenance record must include:

```yaml
smoke_run_id:
operator:
repo_branch:
repo_head:
runner_path:
provider:
model_id_or_snapshot:
endpoint_url:
api_key_env_name_only:
utc_started_at:
utc_finished_at:
process_exit_status:
command_without_secret_values:
stdout_full:
stderr_full:
receipt_path:
receipt_sha256:
prompt_hash_from_receipt:
raw_response_hash_from_receipt:
live_call_flag_passed: true
participant_packet_exposed: false
real_case_identifiers_used: false
```

The provenance record binds the live execution to the receipt. Without this
record, a smoke receipt is not auditable enough to support even plumbing
closeout.

## Operator Checklist

Before run:

- Confirm the concrete authorization fields are filled by an owner decision or
  equivalent owner-visible authorization record.
- Confirm the probe input uses the `SMOKE_NOCASE_` prefix and synthetic fields.
- Confirm the endpoint URL is one of the runner-accepted standard endpoints.
- Confirm no participant packet, source packet, facilitator ledger, review
  packet, case outcome, or real public identifier is in the prompt input.
- Confirm the planned command includes `--allow-live-provider-call` only for
  this one authorized run.

During run:

- Run only the authorized command.
- Capture full stdout, full stderr, and process exit status.
- Do not retry with a different provider, endpoint, model, prompt, credential
  lane, or output path without a new owner authorization.

After run:

- Fresh-read the receipt if one was written.
- Record the receipt SHA-256, `prompt_hash`, and `raw_response_hash`.
- Store the provenance record beside the smoke receipt or in an owner-named
  operator-record path.
- Close with the non-gate-clearing rule and non-claims below.

## Blocked States

The smoke test is blocked if:

- the owner has not authorized the exact provider, model ID, endpoint, and
  credential lane;
- the input uses a real case, real identifiers, or a non-`SMOKE_NOCASE_`
  `case_id`;
- the endpoint is not accepted by the runner;
- the operator cannot capture stdout, stderr, exit status, receipt hash,
  `prompt_hash`, and `raw_response_hash`;
- the run would expose participant packet, source packet, facilitator ledger,
  case outcome, or real public identifiers.

Blocked or failed smoke attempts are non-gate-clearing. Preserve the error
output in the provenance record; do not convert a failed attempt into a pass.

## Non-Claims

- This checklist does not authorize a live provider call.
- This checklist does not make raw API the default pre-sale model-use path.
- This checklist does not run a smoke test.
- This checklist does not run a memorization probe.
- This checklist does not pass or fail any model family.
- This checklist does not authorize participant packet exposure.
- This checklist does not authorize a blind judgment run.
- This checklist does not authorize scoring.
- This checklist does not freeze a facilitator ledger.
- This checklist does not implement schema or runtime code.
- This checklist does not validate or admit a fixture.
- This checklist does not prove product readiness.
- This checklist does not prove judgment quality.

Required boundary: plumbing works only; not judgment quality.
