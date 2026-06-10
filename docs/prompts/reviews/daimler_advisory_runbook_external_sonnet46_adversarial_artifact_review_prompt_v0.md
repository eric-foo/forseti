# Daimler Advisory Runbook External Sonnet 4.6 Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review prompt
scope: Paste-ready prompt for an external adversarial artifact review of daimler_advisory_runbook_v0.md.
use_when:
  - Asking a separate Sonnet 4.6 lane to review the Daimler advisory runbook draft.
  - Preventing the prior self-authored runbook review from becoming review authority.
  - Checking advisory/non-gate-clearing, participant-packet, and facilitator-only boundaries before any advisory use.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/daimler_advisory_runbook_v0.md
  - docs/decisions/advisory_runbook_scope_daimler_v0.md
  - docs/decisions/advisory_proof_slice_definition_v0.md
  - docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md
  - docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md
  - docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md
input_hashes:
  docs/workflows/daimler_advisory_runbook_v0.md: 88BDD19F493D4DB6CA27397B4344478018A15C0FAD62A3A80B7317CB6EE18C81
  docs/decisions/advisory_runbook_scope_daimler_v0.md: 4F9662DBD38A598204926EE12ED1B3A8C1011D45AAAD987A3FBA6DB1F99446B6
  docs/decisions/advisory_proof_slice_definition_v0.md: D758106977180863653E2ED6612082C3E87D9AC228C57F37BB63C5C6C3515119
  docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md: A257AE82D36216EB9099D269C2EAD0587E9063764B9011C4F45229852678D344
  docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: 3301224649991811D91B8B5932F0DFF18D3E356CB51979619BDBE3494BC9193C
  docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md: 4C7190CE9F12EE712CF08C536D513BB8A25F52C54D6B0A715E874113E524C693
branch_or_commit: main @ 829bbe0dc954
downstream_report_path: docs/review-outputs/adversarial-artifact-reviews/daimler_advisory_runbook_external_sonnet46_adversarial_artifact_review_v0.md
stale_if:
  - daimler_advisory_runbook_v0.md changes.
  - Any pinned input hash changes.
  - The downstream report path already exists before review starts.
```

## Paste-Ready Prompt

````markdown
# Daimler Advisory Runbook External Adversarial Artifact Review

You are reviewing an Orca repository artifact in place.

Workspace:
`C:\Users\vmon7\Desktop\projects\orca`

Expected branch:
`main`

Expected HEAD:
`829bbe0dc9545cc34f7174cd7f3058824f5fd331`

Reviewer posture:
- This prompt is intended for a non-contestant review lane, specifically a Claude Sonnet 4.6-style reviewer.
- Runtime model choice is outside this prompt's authority; treat "Sonnet 4.6" as the owner-selected external review posture, not a model recommendation from the prompt.

## Non-Contestant Gate

Before reading task sources, check your runtime identity if available.

If you are GPT-5.5, Claude Opus, or another runtime intentionally selected as a target contestant family for this Daimler blind/advisory case work, stop and return:

```yaml
review_summary:
  status: blocked
  recommendation: blocked_target_contestant_exposure_risk
  summary: "Reviewer appears to be a target contestant family; do not load Daimler advisory or facilitator-routing sources."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Rerun this review on a non-contestant review lane."
```

If you are Claude Sonnet 4.6 or another non-contestant lane, proceed.

## Required Method Sequence

1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. REFERENCE-LOAD `workflow-deep-thinking`. Do not APPLY it yet.
4. REFERENCE-LOAD `workflow-adversarial-artifact-review`. Do not APPLY it yet.
5. SOURCE-LOAD only the required task sources listed below.
6. Verify every required source hash exactly. If any hash mismatches, stop as blocked before reviewing.
7. Declare `SOURCE_CONTEXT_READY` only after all required source files are loaded and hashes verified.
8. APPLY `workflow-deep-thinking` to frame failure modes and decision criteria before findings.
9. APPLY `workflow-adversarial-artifact-review` to perform the read-only artifact review.
10. Write the full durable report to the required output path.
11. Return only a concise human summary plus the courier YAML after the report is written.

Do not APPLY deep-thinking or artifact-review methods before `SOURCE_CONTEXT_READY`.

## Required Sources And Hashes

Read and verify:

```yaml
required_sources:
  AGENTS.md: current workspace instructions; hash not pinned by this prompt
  .agents/workflow-overlay/README.md: overlay entrypoint; hash not pinned by this prompt
  .agents/workflow-overlay/source-of-truth.md: Orca source hierarchy and doctrine-change boundary
  .agents/workflow-overlay/source-loading.md: Orca source-loading and start-preflight rules
  .agents/workflow-overlay/review-lanes.md: adversarial artifact review lane and severity labels
  .agents/workflow-overlay/prompt-orchestration.md: review-report output mode and source-gated method contract
  .agents/workflow-overlay/retrieval-metadata.md: retrieval-header checks
  .agents/workflow-overlay/product-proof.md: product-proof and zero-spoiler boundaries
  .agents/workflow-overlay/communication-style.md: courier YAML shape
  docs/workflows/daimler_advisory_runbook_v0.md: 88BDD19F493D4DB6CA27397B4344478018A15C0FAD62A3A80B7317CB6EE18C81
  docs/decisions/advisory_runbook_scope_daimler_v0.md: 4F9662DBD38A598204926EE12ED1B3A8C1011D45AAAD987A3FBA6DB1F99446B6
  docs/decisions/advisory_proof_slice_definition_v0.md: D758106977180863653E2ED6612082C3E87D9AC228C57F37BB63C5C6C3515119
  docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md: A257AE82D36216EB9099D269C2EAD0587E9063764B9011C4F45229852678D344
  docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: 3301224649991811D91B8B5932F0DFF18D3E356CB51979619BDBE3494BC9193C
  docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md: 4C7190CE9F12EE712CF08C536D513BB8A25F52C54D6B0A715E874113E524C693
```

## Explicitly Excluded Source

Do not read or rely on this prior self-authored review report:

`docs/review-outputs/adversarial-artifact-reviews/daimler_advisory_runbook_adversarial_artifact_review_v0.md`

Reason: the current request is for an external Sonnet 4.6 review, not a review derived from the same lane that wrote the runbook. If this report appears in `open_next` metadata or filesystem search results, treat that as a possible review-target/routing issue to assess from the runbook metadata, but do not open the report body and do not use its findings, verdict, or summary as evidence.

Also do not load the Daimler participant packet, facilitator ledger, evidence registry, source registry, source acquisition receipt, outcome/reveal material, or raw source artifacts unless you find a concrete reason that the runbook itself cannot be reviewed without them. If you think one of those sources is necessary, stop and return a source-gap blocker rather than opening it.

## Commission

Review target:
`docs/workflows/daimler_advisory_runbook_v0.md`

Review purpose:
Determine whether the runbook is safe and sufficient as an operator-facing, facilitator-only, non-gate-clearing advisory runbook draft before any advisory use.

Review question:

```text
Does the runbook safely describe advisory preparation and review boundaries
without authorizing participant-packet exposure, model/provider selection,
model execution, API execution, buyer contact, scoring, validation, fixture
admission, product proof, blind-use readiness, or judgment-quality claims?
```

## Review Surfaces

Check at minimum:

1. Operator-only versus model-facing separation.
2. Facilitator-only Daimler routing boundary, including target-contestant non-exposure.
3. Participant-packet exposure gate and whether the runbook can be reviewed without loading the packet.
4. Advisory subscription/manual/chat boundary versus gate-bearing no-tools execution evidence.
5. Deferred prompt-assembly section: confirm it is not executable prompt content.
6. Operator checklist: confirm false-by-default fields do not authorize a run.
7. Response capture notes: confirm they do not become schema, execution architecture, validation gate, or receipt provenance.
8. Stop/quarantine conditions: confirm they are concrete and sufficient.
9. Separate authorization gates: confirm participant exposure, model/provider selection, advisory run execution, API/gate-bearing execution, buyer contact, scoring, and ledger freeze remain closed.
10. Retrieval metadata: confirm `authority_boundary: retrieval_only`, justified `open_next`, justified hashes, stale conditions, and no forbidden header authority.
11. Collision with the explicitly excluded self-authored review report path.
12. Overclaim scan: validation, fixture admission, scoring readiness, product proof, buyer validation, blind-use readiness, judgment quality, or readiness.

## Review Authority And Severity

Use Orca's adversarial artifact review lane from `.agents/workflow-overlay/review-lanes.md`.

Severity labels are allowed only as finding-priority labels:
- `critical`
- `major`
- `minor`

They do not create approval, validation, mandatory remediation, readiness, or patch authority.

This is a read-only review. You may write the review report only to the required report path below. Do not patch source files. Do not emit `patch_queue_entry`. Advisory remediation direction is allowed, but executor-ready patch instructions are not.

## Required Output

Output mode:
`review-report`

Required durable report path:
`docs/review-outputs/adversarial-artifact-reviews/daimler_advisory_runbook_external_sonnet46_adversarial_artifact_review_v0.md`

Before reviewing, verify this output path does not already exist. If it exists, stop as blocked before full review.

The durable report should include:

- commission, target, authority, and excluded scope;
- workspace/branch/HEAD preflight;
- source-read ledger and exact hash verification table;
- `SOURCE_CONTEXT_READY` or blocker;
- deep-thinking failure-mode frame;
- findings ordered by severity;
- non-findings that matter;
- not-proven boundaries;
- review-use boundary;
- non-claims.

After writing the report, fresh-read it and compute its SHA256. Then return only:

1. A short human summary.
2. This courier YAML:

```yaml
review_summary:
  status: completed | blocked | failed
  report_path: docs/review-outputs/adversarial-artifact-reviews/daimler_advisory_runbook_external_sonnet46_adversarial_artifact_review_v0.md
  report_hash: "<SHA256 if written, else omit>"
  reviewed_target: docs/workflows/daimler_advisory_runbook_v0.md
  reviewed_target_hash: 88BDD19F493D4DB6CA27397B4344478018A15C0FAD62A3A80B7317CB6EE18C81
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  summary: "<one sentence>"
  findings_count: <integer>
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "<one concrete next step>"
  non_claims:
    - no advisory run
    - no participant packet exposure
    - no target contestant exposure
    - no model/provider selection
    - no model run
    - no API run
    - no scoring
    - no ledger freeze
    - no validation
    - no fixture admission
    - no product proof
    - no buyer validation
    - no judgment-quality claim
```

If the report write fails, do not use `report_path`; return `review_location: chat_only_current_thread`, `status: failed`, `recommendation: blocked`, and explain the write failure.

Close the durable report with:

`Required boundary: plumbing works only; not judgment quality.`
````
