# No-Case Smoke Test OpenAI GPT-5.4 Mini One-Shot Operator Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: One-shot operator prompt for the authorized no-case smoke-test execution using OpenAI Responses and gpt-5.4-mini.
use_when:
  - Running the exact authorized no-case smoke test after owner authorization.
  - Creating the materialized synthetic probe input, smoke receipt, and operator provenance record for this one run.
  - Preserving the permanent non-gate-clearing boundary for no-case smoke output.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md
  - docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
  - forseti-harness/runners/run_memorization_probe_raw_api.py
input_hashes:
  docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md: 377D834A70F4B38ACD4A419290394DFD1B5C7A2F1957146DEBEE5B29867DB52B
  docs/review-outputs/adversarial-artifact-reviews/no_case_smoke_test_authorization_openai_gpt_5_4_mini_adversarial_artifact_review_v0.md: F883F0EB19B87F4369CE1704BA39D6D727AC27BABC9693ECC7B4042FA8715E7B
  docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md: 7A17255422C546858C54807161A265074FC0A5BD6739AFDE5592A51D94A8B26D
  docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: F46AA6A4003E200C41796826277A6D8074ED84F26E6B6A5DD9E15584BE5EB0F5
  orca-harness/runners/run_memorization_probe_raw_api.py: CD83FDE1960CA503AD0EE39188CB49EB4676426115A54A7A38A888AA2A99A021
branch_or_commit: main @ e004b87b30361b3631adb1f11f936052db8c8bdd
stale_if:
  - Any input hash changes.
  - The smoke receipt path already exists.
  - The smoke provenance path already exists.
  - The authorization record is superseded or withdrawn.
  - The runner changes provider endpoint allow-list, request-shape validation, receipt fields, or live-call flag behavior.
```

## Objective

Run exactly one authorized no-case smoke test for the raw-API memorization-probe runner.

This run exists only to test plumbing: synthetic input materialization, no-tools raw API execution, receipt generation, stdout/stderr/exit capture, and operator provenance capture.

It must not be treated as a real-case probe, blind-use authorization, validation, fixture admission, product proof, or judgment-quality evidence.

## Workspace

Use:

`C:\Users\vmon7\Desktop\projects\orca`

Expected branch/revision at prompt creation:

```yaml
expected_branch: main
expected_head: e004b87b30361b3631adb1f11f936052db8c8bdd
```

Dirty state is allowed. Do not require a clean worktree. Do require the pinned hashes in this prompt to match before running the live provider call.

## Required Preflight

Before any live call:

1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. Read the authorization record:
   - `docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md`
4. Read the no-case checklist:
   - `docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md`
5. Read the no-tools execution contract:
   - `docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md`
6. Read the runner:
   - `orca-harness/runners/run_memorization_probe_raw_api.py`
7. Verify the five pinned hashes in this prompt.
8. Confirm both planned output paths are unused:
   - `docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_receipt_v0.yaml`
   - `docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_provenance_v0.yaml`
9. Confirm `OPENAI_API_KEY` is present without printing, echoing, logging, or hashing its value.
10. If any preflight check fails, stop and report `blocked_or_not_run`. Do not run the provider call.

Record this receipt in the final closeout:

```yaml
orca_start_preflight:
  agents_read: yes/no
  overlay_read: yes/no
  source_pack: no_case_smoke_openai_gpt_5_4_mini_one_shot_execution
  edit_permission: implementation-authorized-for-exact-one-shot-smoke-run-only
  target_scope:
    - docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/
  dirty_state_checked: yes/no
  blocked_if_missing: input hashes, unused output paths, OPENAI_API_KEY presence, exact command scope
```

## Authorization Boundary

The live provider call is authorized only by:

`docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md`

Current pinned authorization SHA-256:

`377D834A70F4B38ACD4A419290394DFD1B5C7A2F1957146DEBEE5B29867DB52B`

You may pass `--allow-live-provider-call` only for the exact command scope below. Do not use another provider, model, endpoint, credential lane, prompt input, output path, provenance path, retry path, or real-case identifier.

If network sandbox escalation is required, request it only for the exact live provider command. The approval question should state that this is one authorized no-case OpenAI smoke-test call. Do not request a standing/broad network rule.

## Materialize the Synthetic Probe Input

Create the smoke-test folder if missing:

`docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/`

Materialize this exact synthetic YAML input at:

`docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_probe_input_v0.yaml`

```yaml
case_id: SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001
decision_question: "Synthetic no-case plumbing question: should placeholder option A be selected?"
public_identifiers_if_any:
  - SYNTHETIC_NO_CASE_IDENTIFIERS_NONE
decision_date_or_cutoff: SYNTHETIC_NO_CASE_CUTOFF_NOT_A_REAL_CASE
probe_model_family: OpenAI GPT-5.4 mini
probe_model_id: gpt-5.4-mini
probe_prompt_template_version: v0.14_no_case_smoke
```

After writing the input, fresh-read it and compute its SHA-256 before execution.

The input must not name Daimler, Canoo, Unity, TR/Casetext, Milwaukee, any real company, real source, real transaction, real vote, real dispute, real case outcome, participant packet, source packet, facilitator ledger, review packet, or other real-case material.

## Exact Authorized Command

Run this exact command once, substituting only the materialized input path shown above for `--probe-input`:

```powershell
python orca-harness/runners/run_memorization_probe_raw_api.py --probe-input docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_probe_input_v0.yaml --output docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_receipt_v0.yaml --provider openai_responses --api-url https://api.openai.com/v1/responses --api-key-env OPENAI_API_KEY --max-tokens 512 --timeout-seconds 60 --reviewed-by-operator --allow-live-provider-call
```

Capture all of the following:

- full stdout;
- full stderr;
- process exit status;
- exact command used;
- start timestamp;
- end timestamp;
- whether sandbox/network escalation was requested and approved;
- whether `OPENAI_API_KEY` was present, without recording its value.

Do not retry with different parameters. If the command fails, preserve the failure visibly and write the provenance record with `status: blocked_or_failed_no_case_smoke`. Do not convert a provider rejection, missing key, timeout, or receipt failure into a pass.

## Required Provenance Record

Write the provenance record to:

`docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_provenance_v0.yaml`

Required fields:

```yaml
provenance_record_version: 1
artifact_role: no_case_smoke_operator_provenance
authority_boundary: plumbing_only_non_gate_clearing
status: completed | blocked_or_failed_no_case_smoke
authorization_record_path: docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md
authorization_record_sha256: 377D834A70F4B38ACD4A419290394DFD1B5C7A2F1957146DEBEE5B29867DB52B
authorization_review_report_path: docs/review-outputs/adversarial-artifact-reviews/no_case_smoke_test_authorization_openai_gpt_5_4_mini_adversarial_artifact_review_v0.md
authorization_review_report_sha256: F883F0EB19B87F4369CE1704BA39D6D727AC27BABC9693ECC7B4042FA8715E7B
probe_input_path_used: docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_probe_input_v0.yaml
probe_input_sha256: "<fill after materialization>"
runner_path: orca-harness/runners/run_memorization_probe_raw_api.py
runner_sha256: CD83FDE1960CA503AD0EE39188CB49EB4676426115A54A7A38A888AA2A99A021
provider: openai_responses
api_url: https://api.openai.com/v1/responses
api_key_env: OPENAI_API_KEY
api_key_present_without_value: true | false
model_source_basis: OpenAI official Models documentation, retrieved 2026-06-01
exact_command: "<single-line command actually run>"
sandbox_or_network_escalation:
  requested: true | false
  approved: true | false | not_applicable
start_timestamp_local: "<ISO-8601 local timestamp>"
end_timestamp_local: "<ISO-8601 local timestamp>"
process_exit_status: "<integer or not_run>"
stdout_full: |-
  <full stdout, or empty>
stderr_full: |-
  <full stderr, or empty>
receipt_path: docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_receipt_v0.yaml
receipt_sha256: "<fill if receipt exists, else NOT_WRITTEN>"
receipt_fresh_read_status: read_ok | not_written | read_failed
receipt_prompt_hash: "<from receipt if present, else NOT_AVAILABLE>"
receipt_raw_response_hash: "<from receipt if present, else NOT_AVAILABLE>"
non_gate_clearing_rule: >
  No-case smoke output is plumbing confirmation only, even if the receipt
  computes pass_valid. It is not a real-case probe pass, blind-use
  authorization, validation, fixture admission, product proof, or
  judgment-quality evidence.
non_claims:
  - no real-case probe
  - no participant packet exposure
  - no blind judgment
  - no scoring
  - no ledger freeze
  - no schema/runtime implementation
  - no validation
  - no fixture admission
  - no product proof
  - no judgment-quality claim
```

After writing the provenance record, fresh-read it and compute its SHA-256.

## Required Closeout

Return a concise human summary plus this YAML:

```yaml
no_case_smoke_execution_summary:
  status: completed | blocked_or_failed_no_case_smoke
  smoke_run_id: SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001
  authorization_record_hash: 377D834A70F4B38ACD4A419290394DFD1B5C7A2F1957146DEBEE5B29867DB52B
  probe_input_path: docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_probe_input_v0.yaml
  probe_input_hash: "<SHA256 or NOT_WRITTEN>"
  receipt_path: docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_receipt_v0.yaml
  receipt_hash: "<SHA256 or NOT_WRITTEN>"
  provenance_path: docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_provenance_v0.yaml
  provenance_hash: "<SHA256 or NOT_WRITTEN>"
  provider_call_attempted: true | false
  provider_call_exit_status: "<integer or not_run>"
  gate_interpretation_from_receipt: "<value if present, else NOT_AVAILABLE>"
  next_action: "<one concrete next action>"
  non_claims:
    - no real-case probe
    - no participant packet exposure
    - no blind judgment
    - no scoring
    - no ledger freeze
    - no validation
    - no fixture admission
    - no product proof
    - no judgment-quality claim
```

Required final line:

`plumbing works only; not judgment quality.`
