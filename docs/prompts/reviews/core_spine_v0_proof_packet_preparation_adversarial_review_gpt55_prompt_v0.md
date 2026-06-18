# GPT-5.5 Adversarial Review Prompt: Core Spine v0 Proof Packet Preparation

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial review prompt for Core Spine v0 proof-packet preparation artifacts.
use_when:
  - Preparing or launching the proof-packet preparation adversarial artifact review.
  - Checking whether the proof-prep review scope, report destination, and non-execution boundaries are pinned.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - orca/product/spines/foundation/product_contract/core_spine_v0_proof_packet_preflight_v0.md
  - orca/product/case_families/product_learning/other_verticals/core_spine_v0_first_proof_packet_preparation_v0.md
input_hashes:
  docs/product/core_spine_v0_proof_packet_preflight_v0.md: 557CF083E1341AADF7840F36CB95EC6C0D75A6CF0933377437F8BF61CFA514F7
  docs/product/core_spine_v0_first_proof_packet_preparation_v0.md: 318621B3D32A1086AC21F006F6F030E13D12D7D34D098F09ADE795D2908E314C
branch_or_commit: main @ 3bf5c45cfa6879ae65c8f822eff9c185dcba8b3c
downstream_consumers:
  - docs/review-outputs/proof/core_spine_v0_proof_packet_preparation_adversarial_review_v0.md
stale_if: Target artifact hash changes, review-lane output contract changes, or proof-packet preparation review scope is expanded beyond read-only artifact review.
```

- Prompt type: Review prompt
- Requested reviewer model: GPT-5.5
- Output mode: review-report
- Edit permission: read-only
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Target artifacts:
  - `docs/product/core_spine_v0_proof_packet_preflight_v0.md`
  - `docs/product/core_spine_v0_first_proof_packet_preparation_v0.md`
- Report destination:
  - `docs/review-outputs/proof/core_spine_v0_proof_packet_preparation_adversarial_review_v0.md`

## Objective

Run one narrow adversarial artifact review of the accepted preflight and the
first proof-packet preparation artifact.

The review should answer whether either artifact still creates a blocker around
self-authorization, boundary leakage, `jb` authority leakage, or backtest
leakage. Do not run proof, collect evidence, patch files, or prepare a patch
queue. Write the review report only to the report destination above.

## Required Skill Invocation

Use `workflow-deep-thinking` first.

Then use `workflow-adversarial-artifact-review`.

The deep-thinking step should frame the boundary problem: the review must
stress-test proof-prep safety, self-authorization, boundary leakage, `jb`
authority leakage, and backtest leakage before findings are listed.

## Required Reads

Read first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/project-authority.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/communication-style.md`

Then read:

- `docs/decisions/turn_08_product_thesis_v0.md`
- `docs/product/core_spine_v0_product_contract.md`
- `docs/product/engagement_logic_registry_v0.md`
- `docs/product/core_spine_v0_information_production_foundation_v0.md`
- `docs/product/core_spine_v0_proof_protocol_v0.md`
- `docs/product/core_spine_v0_proof_input_selection_v0.md`
- `docs/product/core_spine_v0_proof_packet_preflight_v0.md`
- `docs/product/core_spine_v0_first_proof_packet_preparation_v0.md`

Also check:

- `git status --short --branch`
- `git log --oneline -5`

## Current Decision Context

The owner accepted the corrected preflight in chat on 2026-05-21 for
proof-packet preparation only.

Accepted scope:

- the preflight defines the proof-prep gate;
- the Information Production Foundation is conditionally accepted as the manual
  proof-prep standard;
- proof execution remains unauthorized;
- evidence collection remains unauthorized;
- feature planning remains unauthorized;
- implementation remains unauthorized.

The first proof-packet preparation artifact was created after that acceptance
and currently carries verdict `READY_FOR_PROOF_PACKET_PREPARATION_REVIEW`.

## Dirty State Allowance

Dirty state is allowed. Modified and untracked Orca docs and overlay files may
exist. Do not clean, revert, stage, commit, or switch branches.

If a required target artifact is missing, unreadable, or conflicts with the
accepted scope above, return a blocked result instead of reviewing a substitute.

## Review Scope

Review only these risks:

- self-authorization: an artifact accepts itself, bypasses owner acceptance, or
  turns a proposed gate into proof authority;
- boundary leakage: an artifact authorizes proof execution, evidence
  collection, source maps, decision memos, feature planning, implementation, or
  tooling;
- `jb` authority leakage: an artifact imports `jb` paths, lifecycle mechanics,
  templates, validation habits, or success logic into Orca or Core Spine;
- backtest leakage: an artifact allows case selection, cutoff choice, or
  post-window evidence to be shaped after outcome knowledge.

After correctness findings, optionally note friction only if it affects the
next Chief Architect decision. Do not expand into broad product critique.

## Excluded Scope

Do not review implementation, code, tests, runtime architecture, source
collection systems, dashboards, scrapers, APIs, databases, scoring engines,
automation, feature plans, or commercial willingness to pay.

Do not judge whether competitor narrative evidence exists or is strong. Do not
judge whether the backtest will pass. Do not claim proof-run readiness.

## Output Style

Follow `.agents/workflow-overlay/communication-style.md`.

Use short headers. Use bullets with a small explanation for each bullet. Do not
bold bullet leads by default.

Decision first, scope second, next action third.

## Output Contract

Write the durable review report to:

`docs/review-outputs/proof/core_spine_v0_proof_packet_preparation_adversarial_review_v0.md`

This prompt uses `review-report` output mode. The human-readable review value
belongs in the durable report above. Chat YAML is courier output only and is
valid only after that report has been successfully written.

The report must contain:

1. Review target and source-read ledger.
2. Dirty sources relied on.
3. Scope and excluded scope.
4. Correctness findings first.
5. Friction findings only if material.
6. Not-proven boundaries.
7. Blockers or no-blocking-finding statement.
8. Next authorized step.
9. Review-use boundary.

Finding format:

- `AR-01`: one-sentence finding title.
- Location: file and stable section heading or search key.
- Evidence: quote or short paraphrase from the artifact.
- Why it matters: concrete effect on acceptance, boundary control, or proof-prep
  safety.
- Next action: advisory only; no patch execution.

If there are no blocking findings, say so directly. Do not claim the artifacts
are approved, accepted, validated, proof-ready, feature-ready, implementation
ready, or committed.

Findings are decision input for the Chief Architect. They are not mandatory
remediation unless separately accepted and authorized.

After successfully writing the report, return only a compact YAML summary in
chat:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/proof/core_spine_v0_proof_packet_preparation_adversarial_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  summary: "One sentence describing the review result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step"
```

If the required report cannot be written after review work starts, do not use
`report_path` and do not treat chat YAML as a substitute report. Return a
failed blocked summary in chat:

```yaml
review_summary:
  status: failed
  review_location: chat_only_current_thread
  recommendation: blocked
  summary: "Failed to write required report to docs/review-outputs/proof/core_spine_v0_proof_packet_preparation_adversarial_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve the report write failure, then rerun the review-report prompt."
```

Include enough brief human-readable failure detail to route the write failure.
Do not add extra YAML keys.
