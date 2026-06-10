# No-Case Smoke Test Authorization - OpenAI GPT-5.4 Mini 2026-06-01 v0

```yaml
retrieval_header_version: 1
artifact_role: Orca decision record
scope: Concrete owner-visible authorization for one later no-case raw-API smoke test using OpenAI Responses and gpt-5.4-mini.
use_when:
  - Checking whether this exact no-case smoke-test execution is authorized.
  - Preparing the operator command and provenance record for this exact one-shot smoke test.
  - Preventing this smoke result from being cited as real-case gate evidence.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md
  - docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
  - docs/decisions/no_case_smoke_test_authorization_pending_parameters_v0.md
  - .agents/workflow-overlay/artifact-folders.md
input_hashes:
  AGENTS.md: 5800D6EC863102DC680A6FDB91199337BC8CAC65A4C820FE3F94610B0AFA82A1
  .agents/workflow-overlay/README.md: 40E28238868A423CD43559C1BE5C312E088439E596ECE8AFD25E73835A62A27F
  docs/research/judgment-spine/harness/v0_14/no_case_smoke_test_authorization_checklist_v0.md: 0EA6D4C180CD36AF6611E42BFEAB92A576C9D0311EE98417CBB5CFFC33776BF5
  docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: 3301224649991811D91B8B5932F0DFF18D3E356CB51979619BDBE3494BC9193C
  docs/decisions/no_case_smoke_test_authorization_pending_parameters_v0.md: 673B72E0EA8971051BAF827F248D0CF23AD70D3C6BD60499E36DD17BA113EB82
  orca-harness/runners/run_memorization_probe_raw_api.py: CD83FDE1960CA503AD0EE39188CB49EB4676426115A54A7A38A888AA2A99A021
  .agents/workflow-overlay/artifact-folders.md: ADD8158798A1A300F81863A45004969CD8AF0EEC5D8A949D78FE46AEA79DD39B
  docs/review-outputs/adversarial-artifact-reviews/no_case_smoke_test_authorization_pending_parameters_post_patch_adversarial_recheck_v0.md: 891C522563EAB94669DB26E3C9278BF56FDB991CE9B24419D7C7F5B972AFE04A
external_model_source:
  source: OpenAI official Models documentation
  url: https://developers.openai.com/api/docs/models
  retrieved_date_local: 2026-06-01
  observed_basis: gpt-5.4-mini listed as available via the Responses API in official OpenAI model documentation.
branch_or_commit: main @ 392f7935c029e96ae0f1342f37d37026ba66268b
downstream_consumers:
  - future no-case smoke-test operator run
  - future no-case smoke-test operator provenance record
stale_if:
  - judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md changes no-case smoke-test routing.
  - Any input hash changes.
  - OpenAI no longer lists gpt-5.4-mini as available for the Responses API.
  - The raw-API runner changes endpoint allow-list, request-shape validation, receipt fields, or live-call flag behavior.
  - The no-case smoke-test checklist changes concrete authorization fields or non-gate-clearing rules.
  - The planned smoke receipt path or provenance path already exists before execution.
```

## Current Task Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: no_case_smoke_test_concrete_authorization_openai_gpt_5_4_mini
  edit_permission: docs-write
  target_scope:
    - docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Owner Instruction Basis

User instruction `proceed with that` on 2026-06-01 is accepted as authorization
to create this concrete no-case smoke-test authorization record, following the
accepted post-patch adversarial recheck for the pending-parameters record:
`docs/review-outputs/adversarial-artifact-reviews/no_case_smoke_test_authorization_pending_parameters_post_patch_adversarial_recheck_v0.md`.

This record authorizes only one later no-case smoke-test execution using the
exact fields below. It does not itself run the smoke test, read or verify an
API key, create the smoke receipt, create the provenance record, authorize a
real-case probe, expose a participant packet, or create gate-clearing evidence.

Patch note: the checklist and contestant-contract input hashes above were
refreshed after the pre-sale execution evidence-tier policy patch. This keeps
the one-shot authorization provenance current without changing its exact
scope, credential lane, endpoint, model ID, non-gate-clearing boundary, or stop
conditions.

## Pre-Sale Default Boundary

This is a bounded optional-plumbing authorization, not the default path for
pre-sale Judgment Spine proof work. It does not require future scouting,
demonstrations, buyer conversations, or owner readbacks to use API. Subscription,
manual, or chat-based execution remains acceptable for advisory pre-sale use
when no clean gate-bearing claim is made.

If a future step needs a clean memorization-probe pass, blind-use gate
consideration, fixture validation/admission, product proof, or judgment-quality
claim, that step must separately satisfy the gate-bearing evidence tier in
`contestant_no_tools_execution_contract_v0.md`.

## Decision Status

```yaml
decision_id: no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0
decision_status: accepted_for_later_one_shot_no_case_smoke_execution_only
live_provider_call_authorized: true_for_exact_later_no_case_smoke_command_only
allow_live_provider_call_flag_authorized: true_for_exact_later_no_case_smoke_command_only
authorization_scope: one_shot_no_case_smoke_test_only
relationship_to_pre_sale_default: optional_plumbing_not_default_path
participant_packet_exposure_authorized: false
real_case_probe_authorized: false
blind_judgment_authorized: false
```

## Concrete Authorization Fields

```yaml
authorized_provider: openai_responses
authorized_model_family: OpenAI GPT-5.4 mini
authorized_model_id_or_snapshot: gpt-5.4-mini
authorized_account_or_credential_lane: OPENAI_API_KEY
authorized_endpoint_url: https://api.openai.com/v1/responses
authorized_runner_path: orca-harness/runners/run_memorization_probe_raw_api.py
authorized_smoke_run_id: SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001
authorized_output_path: docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_receipt_v0.yaml
authorized_provenance_record_path: docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_provenance_v0.yaml
authorization_scope: one_shot_no_case_smoke_test_only
participant_packet_exposure_authorized: false
real_case_probe_authorized: false
blind_judgment_authorized: false
```

Credential note: this record names the environment-variable lane only. It does
not assert that `OPENAI_API_KEY` exists, is valid, has access to
`gpt-5.4-mini`, or has sufficient quota. If the environment variable is absent
or the provider rejects the call, the attempt must fail visibly and remain
non-gate-clearing.

## Authorized Synthetic Probe Input

The later operator must provide the runner with a YAML probe input containing
exactly these semantic values:

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

The probe input must not name Daimler, Canoo, Unity, TR/Casetext, Milwaukee, any
real company, real source, real transaction, real vote, real dispute, real case
outcome, participant packet, source packet, facilitator ledger, or review packet.

This authorization record does not create the probe input file. If the operator
materializes a transient probe input file for the runner, the provenance record
must name the path used and include a SHA-256 hash of the materialized input.

## Exact Later Command Shape

The later operator may pass `--allow-live-provider-call` only for this exact
provider/model/input/output/provenance scope:

```powershell
python orca-harness/runners/run_memorization_probe_raw_api.py --probe-input <materialized_probe_input_yaml_for_SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001> --output docs/research/judgment-spine/harness/v0_14/smoke_tests/SMOKE_NOCASE_openai_gpt_5_4_mini_20260601_001/no_case_smoke_receipt_v0.yaml --provider openai_responses --api-url https://api.openai.com/v1/responses --api-key-env OPENAI_API_KEY --max-tokens 512 --timeout-seconds 60 --reviewed-by-operator --allow-live-provider-call
```

No retry with a different provider, model, endpoint, credential lane, prompt
input, output path, or provenance path is authorized by this record.

## Required Provenance Record Additions

In addition to the checklist-required provenance fields, the later operator
must include these fields in the provenance record for this run:

```yaml
authorization_record_path: docs/decisions/no_case_smoke_test_authorization_openai_gpt_5_4_mini_20260601_v0.md
authorization_record_sha256:
probe_input_path_used:
probe_input_sha256:
model_source_basis: OpenAI official Models documentation, retrieved 2026-06-01
```

The provenance record must still include all fields required by
`no_case_smoke_test_authorization_checklist_v0.md`, including full stdout, full
stderr, process exit status, receipt path, receipt SHA-256, prompt hash, and
raw response hash.

## Stop Conditions

Do not run the smoke test if any condition below is true:

- `OPENAI_API_KEY` is absent from the operator environment.
- The output receipt path already exists.
- The provenance path already exists.
- The materialized probe input differs semantically from the Authorized
  Synthetic Probe Input above.
- The planned prompt contains any real case identifier or participant/facilitator
  material.
- The command differs from the exact provider/model/endpoint/output/provenance
  scope authorized above.
- The operator cannot capture full stdout, full stderr, process exit status,
  receipt hash, `prompt_hash`, `raw_response_hash`, input path, and input hash.

If a stop condition fires, write or report a blocked attempt instead of running
the provider call. Do not convert a failed or blocked attempt into a pass.

## Non-Gate-Clearing Rule

Even if the future smoke receipt computes `probe_result: pass`,
`isolation_result: proven`, and `gate_interpretation: pass_valid`, the result
is plumbing confirmation only. It must never be cited as a clean
memorization-probe pass, blind-use authorization, participant-packet exposure
authorization, fixture validation or admission, scoring readiness,
ledger-freeze evidence, product proof, or judgment-quality evidence.

## Non-Claims

- This decision does not run a live provider call.
- This decision does not make raw API the default pre-sale model-use path.
- This decision does not read, print, validate, or test any API key.
- This decision does not create a probe input file.
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
