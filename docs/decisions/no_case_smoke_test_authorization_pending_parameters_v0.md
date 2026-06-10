# No-Case Smoke Test Authorization Pending Parameters v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: Pending-parameters decision record for a future one-shot no-case raw-API smoke test authorization.
use_when:
  - Preparing the concrete owner authorization for a no-case smoke test.
  - Checking whether a live no-case provider call has already been authorized.
  - Preventing a synthetic smoke receipt from being cited as case-gate evidence.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
  - .agents/workflow-overlay/artifact-folders.md
input_hashes:
  docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md: 7A17255422C546858C54807161A265074FC0A5BD6739AFDE5592A51D94A8B26D
  docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: F46AA6A4003E200C41796826277A6D8074ED84F26E6B6A5DD9E15584BE5EB0F5
  docs/review-outputs/no_tools_execution_foundation_f01_f02_post_patch_adversarial_recheck_v0.md: 01129B39570F629AFF91BEB6631A70D6ABB5DB4F47885C07F083C153ABEAD016
  orca-harness/runners/run_memorization_probe_raw_api.py: CD83FDE1960CA503AD0EE39188CB49EB4676426115A54A7A38A888AA2A99A021
  .agents/workflow-overlay/artifact-folders.md: ADD8158798A1A300F81863A45004969CD8AF0EEC5D8A949D78FE46AEA79DD39B
branch_or_commit: main @ 27cae7b4aec3
downstream_consumers:
  - future no-case smoke-test concrete authorization
  - future no-case smoke-test operator provenance record
stale_if:
  - Any input hash changes.
  - The raw-API runner changes endpoint allow-list, request-shape validation, receipt fields, or live-call flag behavior.
  - The no-case smoke-test checklist changes concrete authorization fields or non-gate-clearing rules.
```

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: no_case_smoke_test_authorization_pending_parameters
  edit_permission: docs-write
  target_scope:
    - docs/decisions/no_case_smoke_test_authorization_pending_parameters_v0.md
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Decision Status

```yaml
decision_id: no_case_smoke_test_authorization_pending_parameters_v0
decision_status: blocked_pending_concrete_owner_parameters
live_provider_call_authorized: false
allow_live_provider_call_flag_authorized: false
authorization_scope: one_shot_no_case_smoke_test_only
participant_packet_exposure_authorized: false
real_case_probe_authorized: false
blind_judgment_authorized: false
```

This record preserves the current stop state for the first no-case smoke-test
authorization lane. It does not authorize a live provider call because the
concrete provider, model ID or snapshot, credential lane, endpoint, receipt
path, and provenance path have not been owner-filled in this record.

## Required Future Authorization Fields

A later concrete authorization decision must replace every `BLOCKED_UNSET`
value below before any operator may pass `--allow-live-provider-call`.

```yaml
authorized_provider: BLOCKED_UNSET_OPENAI_RESPONSES_OR_ANTHROPIC_MESSAGES
authorized_model_family: BLOCKED_UNSET
authorized_model_id_or_snapshot: BLOCKED_UNSET
authorized_account_or_credential_lane: BLOCKED_UNSET_ENV_VAR_NAME_ONLY
authorized_endpoint_url: BLOCKED_UNSET_STANDARD_RUNNER_ENDPOINT
authorized_runner_path: orca-harness/runners/run_memorization_probe_raw_api.py
authorized_output_path: BLOCKED_UNSET_SMOKE_RECEIPT_PATH
authorization_scope: one_shot_no_case_smoke_test_only
participant_packet_exposure_authorized: false
real_case_probe_authorized: false
blind_judgment_authorized: false
```

The later authorization must not infer provider access, endpoint choice,
credential lane, model ID, output path, or provenance path from local
environment state. Those fields must be owner-visible and explicit.

## Synthetic Input Boundary

The future smoke input must use the reserved synthetic case-id convention and
must not name any real case, company, source, vote, transaction, dispute, or
case outcome.

```yaml
case_id_pattern: SMOKE_NOCASE_<provider_or_model>_<yyyymmdd>_<short_run_id>
decision_question: "Synthetic no-case plumbing question: should placeholder option A be selected?"
public_identifiers_if_any:
  - SYNTHETIC_NO_CASE_IDENTIFIERS_NONE
decision_date_or_cutoff: SYNTHETIC_NO_CASE_CUTOFF_NOT_A_REAL_CASE
probe_model_family: BLOCKED_UNSET
probe_model_id: BLOCKED_UNSET
probe_prompt_template_version: v0.14_no_case_smoke
```

The placeholder pattern above is not itself executable authorization. The
actual `case_id` must be concretely filled in a later owner authorization
record.

## Future Receipt And Provenance Paths

The later concrete authorization must bind exact paths. Until then, only this
path pattern is reserved:

```yaml
future_smoke_run_id_pattern: SMOKE_NOCASE_<provider_or_model>_<yyyymmdd>_<short_run_id>
future_smoke_receipt_path_pattern: docs/research/judgment-spine/harness/v0_14/smoke_tests/<future_smoke_run_id>/no_case_smoke_receipt_v0.yaml
future_provenance_record_path_pattern: docs/research/judgment-spine/harness/v0_14/smoke_tests/<future_smoke_run_id>/no_case_smoke_provenance_v0.yaml
```

No smoke receipt or provenance record is created by this decision.
The `smoke_tests/` folder is accepted only for no-case smoke-test receipts and
operator provenance records under `.agents/workflow-overlay/artifact-folders.md`.
That folder location does not make any smoke artifact gate-clearing evidence.

## Required Provenance Record Fields

The future provenance record must bind the live execution to the receipt with
all fields below:

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

Without this provenance record, a smoke receipt is not auditable enough to
support even plumbing closeout.

## Blocked States

The no-case smoke test remains blocked while any of these conditions is true:

- exact provider is not owner-filled;
- authorized model family is not owner-filled;
- exact model ID or snapshot is not owner-filled;
- credential lane is not owner-filled as an environment-variable name only;
- endpoint URL is not owner-filled and accepted by the runner;
- smoke receipt path or provenance path is not owner-filled;
- synthetic `SMOKE_NOCASE_` case ID is not owner-filled;
- the planned prompt contains any real case identifier, participant packet,
  source packet, facilitator ledger, review packet, case outcome, or real
  public identifier;
- the operator cannot capture stdout, stderr, exit status, receipt hash,
  `prompt_hash`, and `raw_response_hash`.

Blocked or failed smoke attempts are permanently non-gate-clearing. Do not
convert a failed attempt into a pass.

## Non-Gate-Clearing Rule

Even if a future smoke receipt computes `probe_result: pass`,
`isolation_result: proven`, and `gate_interpretation: pass_valid`, the result
is plumbing confirmation only. It must never be cited as a clean
memorization-probe pass, blind-use authorization, participant-packet exposure
authorization, fixture validation or admission, scoring readiness,
ledger-freeze evidence, product proof, or judgment-quality evidence.

## Non-Claims

- This decision does not authorize a live provider call.
- This decision does not authorize passing `--allow-live-provider-call`.
- This decision does not run a no-case smoke test.
- This decision does not create a smoke receipt.
- This decision does not create a provenance record.
- This decision does not run a memorization probe.
- This decision does not pass or fail any model family.
- This decision does not authorize participant packet exposure.
- This decision does not authorize real case identifiers.
- This decision does not authorize a blind judgment run.
- This decision does not authorize scoring.
- This decision does not freeze a facilitator ledger.
- This decision does not implement schema or runtime code.
- This decision does not validate or admit a fixture.
- This decision does not prove product readiness.
- This decision does not prove judgment quality.

Required boundary: plumbing works only; not judgment quality.
