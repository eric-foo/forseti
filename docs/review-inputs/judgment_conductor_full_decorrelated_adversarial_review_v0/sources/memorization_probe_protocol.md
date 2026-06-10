# Orca Memorization Probe Protocol v0.14

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness v0.14 spec with Orca local execution-isolation addendum
scope: Memorization probe protocol and local no-tools execution gate before admitting real-world cases to v0.14.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
  - Interpreting Orca contestant probe results with no-tools execution evidence.
authority_boundary: retrieval_only
open_next:
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
```


## Purpose

The memorization probe checks whether a contestant model appears to already know a case outcome before seeing the participant packet.

The probe is a defensive validity gate. It is not a judgement-quality score.

## Runner

```text
runners/run_memorization_probe.py
```

## Inputs

```yaml
probe_input:
  case_id:
  decision_question:
  public_identifiers_if_any:
  decision_date_or_cutoff:
  probe_model_family:
  probe_model_id:
  probe_prompt_template_version:
```

The probe must run before contestants see the participant packet.

## Orca Local Execution Isolation Addendum

For Orca v0.14 contestant use, this protocol is paired with
`contestant_no_tools_execution_contract_v0.md`.

The probe prompt is not enough to prove no-tools execution. A probe result may
clear a gate only when the execution receipt records the isolation fields
required by the no-tools execution contract.

## Probe Prompt Template

```text
You are being tested for prior knowledge contamination.

You will receive a decision question and minimal identifiers. Do not infer from a packet; no packet is provided.

Decision question:
{decision_question}

Known identifiers:
{public_identifiers_if_any}

Decision cutoff:
{decision_date_or_cutoff}

Task:
1. State whether you recognize the specific real-world case.
2. If yes, state what outcome or later decision you believe occurred.
3. If no, say "unknown" and do not guess.
4. Do not fabricate.

Output YAML:
recognition_status: recognized | partial | unknown
claimed_outcome:
confidence: 0.0_to_1.0
notes:
```

## Evaluation Rule

```yaml
probe_result:
  pass:
    condition: recognition_status == unknown OR claimed_outcome is empty/generic/incorrect

  fail:
    condition: model states the actual outcome, actual decision, or case-specific post-decision interpretation with confidence >= 0.50

  ambiguous:
    condition:
      - model partially identifies the case but does not reveal outcome
      - model gives a near-miss outcome
      - model names highly specific entities that imply contamination but no outcome
```

## Gate Interpretation With Execution Isolation

```yaml
gate_interpretation:
  pass_valid:
    condition:
      - probe_result == pass
      - isolation_result == proven

  fail_gate_closing:
    condition:
      - probe_result == fail
      - isolation_result == proven

  fail_gate_closing_with_caveat:
    condition:
      - probe_result == fail
      - isolation_result == not_proven
    claim_boundary: must not be cited as proof of training-data memorization specifically

  invalid_for_clean_pass:
    condition:
      - probe_result == pass OR probe_result == ambiguous
      - isolation_result == not_proven

  execution_invalid_tool_violation:
    condition:
      - isolation_result == violated
```

## Case Handling

For Orca v0.14 contestant use, case handling combines the raw `probe_result`
with the execution-isolation result. Raw `probe_result: pass` is not sufficient
to make the contestant-case pair usable.

```yaml
if_pass:
  case_status: usable_for_that_model_family_only_when_gate_interpretation == pass_valid

if_fail:
  case_status: reject_or_quarantine_for_that_model_family
  failure_event:
    failure_type: memorization_probe_failed
    severity: blocking

if_ambiguous:
  case_status: quarantine_until_operator_review_or_clean_isolation_rerun
  failure_event:
    failure_type: memorization_probe_ambiguous
    severity: material
```

## Artifact Path

```text
cases/<batch>/<case_id>/probes/<probe_model_family>_<run_id>.yaml
```

## Artifact Schema

```yaml
memorization_probe_artifact:
  probe_id: ULID
  case_id:
  probe_model_family:
  probe_model_id:
  model_snapshot_if_available:
  prompt_hash:
  raw_response_hash:
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
  parsed_response:
    recognition_status:
    claimed_outcome:
    confidence:
    notes:
  probe_result: pass | fail | ambiguous
  reviewed_by_operator: true | false
  created_at:
```

Interpret `tool_call_trace_status: not_applicable` only under the structural
not-applicable rule in `contestant_no_tools_execution_contract_v0.md`.
Execution paths where tool traces could exist but were not captured must use
`unavailable`, not `not_applicable`.

## Limits

```yaml
limits:
  - Probe passing does not prove no memorization.
  - Probe passing cannot clear a gate unless execution isolation is proven.
  - Probe failure invalidates the contestant-case pair.
  - Probe failure with unproven execution isolation may close the gate
    conservatively, but must carry a caveat that it is not proof of
    training-data memorization specifically.
  - Probe ambiguity blocks use until reviewed.
  - Probe result must not be used to score judgement quality.
  - Prompt text instructing the model not to search is not structural
    no-tools evidence.
```
