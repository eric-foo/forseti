# Advisory Proof-Slice Definition Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review prompt
scope: Read-only adversarial artifact review prompt for Advisory Proof-Slice Definition v0.
use_when:
  - Launching a formal adversarial artifact review of the advisory proof-slice definition.
  - Checking whether Daimler can safely seed advisory runbook scoping without gate-bearing overclaim.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/advisory_proof_slice_definition_v0.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
input_hashes:
  docs/decisions/advisory_proof_slice_definition_v0.md: 07F180EC5D0C70C401CD11B58E4B6509E9A121679549774819AE1B7EF7B4DB31
  .agents/workflow-overlay/product-proof.md: 0EB8A11DAA2A2BE1FC7F610AAA48004D97200A18D11679F9C8D45731EED61F21
  docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md: A257AE82D36216EB9099D269C2EAD0587E9063764B9011C4F45229852678D344
  docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: 3301224649991811D91B8B5932F0DFF18D3E356CB51979619BDBE3494BC9193C
  docs/hygiene/precompact_orca_judgment_harness_first_output_v0.md: 8510A011D008C093BC16C39EDB724DC9584F28E1FEA326FF5705F2317BE812DC
  docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md: 4C7190CE9F12EE712CF08C536D513BB8A25F52C54D6B0A715E874113E524C693
  docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_draft_fixture_pack_adversarial_artifact_review_v0.md: D26E78306C3BCDAA1DE4168FBA92DA6E1E774382828839BE799977319402764C
branch_or_commit: main @ 392f7935c029
stale_if:
  - advisory_proof_slice_definition_v0.md changes.
  - Daimler selected-family probe gate outcome changes.
  - Review-output path already exists before the review starts.
```

## Paste-Ready Review Commission

You are performing a read-only adversarial artifact review for Orca.

## Non-Contestant Gate

This review may expose facilitator-only Daimler routing facts, including the
selected-family probe gate outcome and probe caveats. Before loading any task
sources, identify the runtime/operator lane you are using.

If this prompt is being run on GPT-5.5, Claude Opus, or any runtime
intentionally selected as a future target contestant family for Daimler or a
Judgment Spine blind run, stop immediately and return:

```yaml
review_summary:
  status: blocked
  review_location: chat_only_current_thread
  recommendation: blocked_target_contestant_exposure_risk
  summary: "Review would expose facilitator-only Daimler routing material to a target contestant family."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Rerun this review on a non-contestant review lane."
```

If the gate passes, proceed. This gate is a safety boundary, not a runtime model
recommendation.

## Commission

Review `docs/decisions/advisory_proof_slice_definition_v0.md` as a
decision-bearing internal proof-slice definition.

The review question is:

```text
Is Advisory Proof-Slice Definition v0 safe and sufficient as decision input for
later advisory runbook scoping, without overclaiming Daimler readiness,
gate-bearing evidence, product proof, buyer validation, or judgment quality?
```

This review is not fixture admission, not validation, not model execution, not
buyer proof, not runbook approval, and not judgment-quality review.

## Required Worktree Preflight

Workspace:

```text
C:\Users\vmon7\Desktop\projects\orca
```

Expected branch and revision:

```yaml
expected_branch: main
expected_head: 392f7935c029e96ae0f1342f37d37026ba66268b
```

Required output path:

```text
docs/review-outputs/adversarial-artifact-reviews/advisory_proof_slice_definition_adversarial_artifact_review_v0.md
```

Preflight requirements:

1. Read `AGENTS.md`.
2. Read `.agents/workflow-overlay/README.md`.
3. Confirm the worktree is accessible.
4. Confirm branch/head. If branch or head differs, report the mismatch and
   continue only if the target artifact and pinned source hashes still match.
5. Confirm the required output path does not already exist. If it exists, stop
   with `FAILED_REVIEW_OUTPUT_COLLISION`.
6. Record dirty state. Broad dirty state is allowed for this review; several
   controlling sources may be modified or untracked. Dirty state does not block
   advisory review, but strict source-of-truth, validation, readiness, approval,
   and proof claims remain not proven.

## Source-Gated Method Contract

Use this sequence exactly:

1. Read authority and operating instructions.
2. REFERENCE-LOAD `workflow-deep-thinking`. Do not APPLY it yet.
3. REFERENCE-LOAD `workflow-adversarial-artifact-review`. Do not APPLY it yet.
4. SOURCE-LOAD the required source pack below.
5. Verify all pinned hashes listed below.
6. Declare `SOURCE_CONTEXT_READY` if all required sources load and hashes match;
   otherwise declare `SOURCE_CONTEXT_INCOMPLETE` and stop with the nearest
   blocker.
7. Only after `SOURCE_CONTEXT_READY`, APPLY `workflow-deep-thinking` to frame
   failure modes and decision criteria.
8. Then APPLY `workflow-adversarial-artifact-review` to produce the report.

If `workflow-adversarial-artifact-review` is unavailable, unresolved, or not
applied after `SOURCE_CONTEXT_READY`, return only a blocked or advisory-only
result. Do not emit formal verdicts, severity authority, blocked/ready status,
validation claims, readiness claims, mandatory remediation, patch queues,
executor-ready handoffs, or alignment-complete claims.

## Required Source Pack

Required authority:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/product-proof.md`

Review target:

- `docs/decisions/advisory_proof_slice_definition_v0.md`

Controlling context:

- `docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md`
- `docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md`
- `docs/hygiene/precompact_orca_judgment_harness_first_output_v0.md`
- `docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md`
- `docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_draft_fixture_pack_adversarial_artifact_review_v0.md`

Required hash verification:

```yaml
docs/decisions/advisory_proof_slice_definition_v0.md: 07F180EC5D0C70C401CD11B58E4B6509E9A121679549774819AE1B7EF7B4DB31
.agents/workflow-overlay/product-proof.md: 0EB8A11DAA2A2BE1FC7F610AAA48004D97200A18D11679F9C8D45731EED61F21
docs/decisions/judgment_spine_pre_sale_execution_evidence_tier_policy_v0.md: A257AE82D36216EB9099D269C2EAD0587E9063764B9011C4F45229852678D344
docs/research/judgment-spine/harness/v0_14/contestant_no_tools_execution_contract_v0.md: 3301224649991811D91B8B5932F0DFF18D3E356CB51979619BDBE3494BC9193C
docs/hygiene/precompact_orca_judgment_harness_first_output_v0.md: 8510A011D008C093BC16C39EDB724DC9584F28E1FEA326FF5705F2317BE812DC
docs/decisions/daimler_v0_14_selected_family_probe_gate_outcome_decision_v0.md: 4C7190CE9F12EE712CF08C536D513BB8A25F52C54D6B0A715E874113E524C693
docs/review-outputs/adversarial-artifact-reviews/daimler_v0_14_draft_fixture_pack_adversarial_artifact_review_v0.md: D26E78306C3BCDAA1DE4168FBA92DA6E1E774382828839BE799977319402764C
```

If any required hash mismatches, stop with:

```yaml
review_summary:
  status: blocked
  review_location: chat_only_current_thread
  recommendation: blocked_source_hash_mismatch
  summary: "A required source hash did not match the review prompt."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Refresh the review prompt or rerun against the correct artifact revision."
```

## Review Surfaces

Check at least these surfaces:

1. Retrieval metadata and source hierarchy:
   - header present;
   - `authority_boundary: retrieval_only`;
   - no forbidden readiness, validation, approval, lifecycle, or source-of-truth
     authority in the header;
   - `open_next`, `input_hashes`, `branch_or_commit`, and `stale_if` are
     justified by retrieval value.

2. Advisory versus gate-bearing boundary:
   - subscription/manual/chat tier remains advisory only;
   - artifact does not imply clean memorization-probe pass, blind-use
     authorization, fixture admission, validation, scoring readiness, ledger
     freeze, product proof, or judgment-quality proof;
   - raw API/harness remains optional plumbing, not the default pre-sale path.

3. Daimler-specific gate handling:
   - artifact correctly records that no selected family cleared the Daimler
     probe gate;
   - GPT-5.5 blockage is access/environmental with no valid probe result, not a
     probe fail;
   - Claude Opus fail is treated as gate-routing with tool-isolation caveat, not
     verified training-data memorization causality;
   - no rerun, new family selection, packet exposure, blind-use planning, or
     participant-facing path is authorized by this artifact.

4. Zero-spoiler and facilitator-material boundary:
   - no source URLs, source titles, filenames, byte hashes, retrieval
     timestamps, evidence registry locators, outcome details, consulting
     narrative, or post-cutoff facts are introduced into participant-facing
     scope;
   - artifact itself is classified tightly enough for facilitator-only routing
     facts it contains;
   - future advisory packet exposure is separately authorized and cannot be
     back-converted into gate-bearing evidence.

5. Product-proof and no-buyer-contact boundary:
   - owner-learning/internal narration audience remains intact;
   - no buyer contact, buyer-facing proof memo, deck, market validation, pull,
     willingness-to-pay, product readiness, or commercial readiness claim is
     implied;
   - no-buyer-contact-before-full-spine-MVP constraint remains intact.

6. Runbook-readiness boundary:
   - artifact is sufficient only to inform later advisory runbook scoping;
   - artifact does not itself become a runbook, execution authorization, or
     model prompt;
   - stop/continue criteria are concrete enough to prevent a later runbook from
     laundering advisory output into gate-clearing evidence.

7. Doctrine-change boundary:
   - artifact applies existing policy rather than silently changing product
     doctrine, review authority, validation philosophy, output authority, or
     lifecycle boundaries;
   - if you find a doctrine change, report whether propagation is missing.

## Severity Contract

Use `critical`, `major`, and `minor` only as finding-priority labels.

- `critical`: a defect that would directly authorize or likely cause unsafe
  target-contestant exposure, false gate-clearing, product-proof/validation
  overclaim, or buyer-facing misuse.
- `major`: a defect that materially weakens advisory/gate-bearing separation,
  runbook scoping safety, Daimler gate-state clarity, or source hierarchy, but
  does not directly create unsafe exposure.
- `minor`: hygiene, clarity, stale wording, retrievability, or local ambiguity
  that should be fixed but does not block using the artifact as decision input.

Optional hardening may be listed only when clearly labeled optional and
non-required.

## Output Mode

Use `review-report` output mode.

Write the full durable report to:

```text
docs/review-outputs/adversarial-artifact-reviews/advisory_proof_slice_definition_adversarial_artifact_review_v0.md
```

The report must include:

- commission, target, authority, and source-read preflight;
- hash verification table;
- deep-thinking failure-mode frame;
- findings first, ordered by severity;
- non-findings that matter;
- not-proven boundaries;
- review-use boundary;
- explicit non-claims.

For each finding include:

- severity;
- location;
- issue;
- evidence;
- impact;
- minimum_closure_condition;
- next_authorized_action;
- recommended correction or advisory remediation direction.

Do not include `patch_queue_entry`. This is a read-only review. Findings are
decision input only and are not approval, validation, mandatory remediation, or
executor-ready patch authority.

After writing the report, fresh-read it and compute its SHA256 hash. Then return
only a short human summary plus this courier YAML in chat:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/advisory_proof_slice_definition_adversarial_artifact_review_v0.md
  report_hash: "<SHA256>"
  reviewed_target: docs/decisions/advisory_proof_slice_definition_v0.md
  reviewed_target_hash: 07F180EC5D0C70C401CD11B58E4B6509E9A121679549774819AE1B7EF7B4DB31
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  summary: "<one sentence>"
  findings_count: <integer>
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "<one concrete next step>"
  non_claims:
    - no advisory runbook created
    - no participant packet exposure
    - no target contestant exposure
    - no model run
    - no API run
    - no scoring
    - no ledger freeze
    - no fixture validation or admission
    - no product proof
    - no buyer validation
    - no judgment-quality claim
```

If the report cannot be written, return `status: failed`,
`review_location: chat_only_current_thread`, and `recommendation: blocked`.
Do not use `report_path` for an unwritten report.

Required closeout line in the report:

```text
plumbing works only; not judgment quality.
```
