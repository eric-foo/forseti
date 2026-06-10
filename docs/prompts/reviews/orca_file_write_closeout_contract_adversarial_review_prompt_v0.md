# Orca File-Write Closeout Contract Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Adversarial artifact review prompt for the Orca file-write closeout contract patch across overlay, shared prompt behavior, and active file-write prompts.
use_when:
  - Asking a reviewer to stress-test the current dirty file-write closeout contract patch.
  - Checking whether the patch preserves review-report, paste-ready-chat, source-heavy economy, and artifact-native table exceptions.
  - Deciding whether the closeout contract patch is ready for owner acceptance, targeted fixes, or rollback.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/communication-style.md
  - .agents/workflow-overlay/validation-gates.md
  - docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md
input_hashes:
  - path: .agents/workflow-overlay/communication-style.md
    sha256: D93931D97006C3167059787125857F3FB4107D2E49C1F80E71B50159F94BD3BC
  - path: .agents/workflow-overlay/prompt-orchestration.md
    sha256: 54242C83D83FBA3775738276C0D87F0C1F172849024E6F341D1E61D0851AA049
  - path: .agents/workflow-overlay/validation-gates.md
    sha256: 0DEBE6EA327EAAEBE181902235C4B91D7152C29ACBEFC5AC3466B4D145EF08C7
  - path: docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
    sha256: CB892EB9ED69E800672C6B32A679517C459C85B17D2C2A6E238D5FBA3015A3B6
  - path: docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md
    sha256: DFCF2865434CC4405846C0842A4789ACBB787477C64C2B6BCF6D518BB5D2626F
  - path: docs/prompts/product-planning/orca_product_lead_ca_first_icp_wedge_prompt_v0.md
    sha256: 27A30BD90590EFC4E9C9DFA36E1228619CC55563E255F0E9BA8CDE1A1A3C5854
  - path: docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md
    sha256: 37E8DFBA790595799354D52ED2875B8A501F103E14E83A2E325A28415AA9620D
downstream_consumers:
  - Orca file-write closeout contract patch acceptance or fix route.
  - Future prompt-policy cleanup if the review finds contract drift.
stale_if:
  - Any target file hash changes before review.
  - The file-write closeout patch is accepted, reverted, or superseded before review.
  - Orca chat-output topology, review-report behavior, or prompt output modes change before review.
```

## Prompt Status

Status: `PROMPT_ARTIFACT_V0`.

Template kind: `review`.

Template source: `docs/prompts/templates/review/adversarial_artifact_review_v0.md` plus Orca review prompt defaults from `.agents/workflow-overlay/prompt-orchestration.md`.

Target actor: Orca adversarial artifact reviewer.

Required skills for downstream reviewer:

1. `workflow-deep-thinking`.
2. `workflow-adversarial-artifact-review`.

Output mode for downstream reviewer: `review-report`.

Downstream report path:
`docs/review-outputs/adversarial-artifact-reviews/orca_file_write_closeout_contract_adversarial_review_v0.md`

Edit permission for downstream reviewer:
Read-only review plus writing the one downstream report artifact. Do not patch overlay files, prompt templates, prompt artifacts, workflow artifacts, skills, implementation code, commits, pushes, or PRs.

## Paste-Ready Review Prompt

````markdown
# Orca Adversarial Artifact Review - File-Write Closeout Contract Patch

You are performing a read-only adversarial artifact review for Orca.

Use `workflow-deep-thinking` first, then use `workflow-adversarial-artifact-review`.

The deep-thinking step should frame the boundary problem, failure modes, and decision criteria before findings are listed. It does not widen review scope, authorize patching, or turn this into product planning.

## Workspace Preflight

Workspace:
`C:\Users\vmon7\Desktop\projects\orca`

Expected branch at prompt creation:
`main`

Expected HEAD at prompt creation:
`a873c9c3ed3b289a65f9c472c63e0aadf880a127`

Dirty state:
Required and in scope for the target files below. This review is about the current dirty file-write closeout contract patch, including untracked active prompt artifacts. Do not review a clean checkout as a substitute.

Before reviewing, run or otherwise verify:

- current workspace path is `C:\Users\vmon7\Desktop\projects\orca`;
- target-file dirty state using `git status --short -- <targets>`;
- current hashes for every target and source artifact listed under `Pinned Review Inputs`;
- tracked-file diffs for tracked targets;
- full file contents for untracked targets.

If a pinned target hash mismatches, return `BLOCKED_STALE_REVIEW_INPUT` unless the owner explicitly authorizes reviewing the changed current state. If the workspace cannot be accessed, return `BLOCKED_MISSING_SOURCE`. If the downstream report cannot be written, return the failed `review_summary` shape defined below and do not pretend a durable report exists.

## Source Hierarchy

Use this source hierarchy:

1. Explicit user instruction in this prompt.
2. Orca `AGENTS.md`.
3. `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with the overlay.
5. Reusable workflow guidance only for generic mechanics, never Orca facts.

If reusable workflow guidance conflicts with Orca overlay for Orca facts, the overlay wins. Do not import `jb` rules, paths, handoffs, lifecycle mechanics, GAP policy, validation habits, or prompt templates as Orca authority.

## Required Reads

Read these before deciding:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/template-registry.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`
- `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`
- `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`
- `docs/prompts/product-planning/orca_product_lead_ca_first_icp_wedge_prompt_v0.md`

Use targeted searches over `.agents/workflow-overlay/` and `docs/prompts/` for:

- `file-write`
- `human summary`
- `human-readable`
- `path/hash/status`
- `receipt-only`
- `courier state`
- `courier YAML`
- `lane switching`
- `handoff routing`
- `review-report`
- `paste-ready-chat`
- `source-heavy`
- `artifact-native`
- `validation proof`
- `readiness`

## Pinned Review Inputs

Review the current dirty state of these files exactly as the review target:

- `.agents/workflow-overlay/communication-style.md`
  - SHA256 at prompt creation: `D93931D97006C3167059787125857F3FB4107D2E49C1F80E71B50159F94BD3BC`
  - Git state at prompt creation: modified.
- `.agents/workflow-overlay/prompt-orchestration.md`
  - SHA256 at prompt creation: `54242C83D83FBA3775738276C0D87F0C1F172849024E6F341D1E61D0851AA049`
  - Git state at prompt creation: modified.
- `.agents/workflow-overlay/validation-gates.md`
  - SHA256 at prompt creation: `0DEBE6EA327EAAEBE181902235C4B91D7152C29ACBEFC5AC3466B4D145EF08C7`
  - Git state at prompt creation: modified.
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`
  - SHA256 at prompt creation: `CB892EB9ED69E800672C6B32A679517C459C85B17D2C2A6E238D5FBA3015A3B6`
  - Git state at prompt creation: modified.
- `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`
  - SHA256 at prompt creation: `DFCF2865434CC4405846C0842A4789ACBB787477C64C2B6BCF6D518BB5D2626F`
  - Git state at prompt creation: untracked but in scope.
- `docs/prompts/product-planning/orca_product_lead_ca_first_icp_wedge_prompt_v0.md`
  - SHA256 at prompt creation: `27A30BD90590EFC4E9C9DFA36E1228619CC55563E255F0E9BA8CDE1A1A3C5854`
  - Git state at prompt creation: untracked but in scope.

Use this discussion artifact as the accepted review basis, not as proof that the patch is correct:

- `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`
  - SHA256 at prompt creation: `37E8DFBA790595799354D52ED2875B8A501F103E14E83A2E325A28415AA9620D`
  - Git state at prompt creation: untracked workflow record.

## Review Purpose

Stress-test whether the current file-write closeout contract patch correctly fixes receipt-only closeouts for substantial decision-bearing `file-write` artifacts without creating new contract drift.

The patch intent is:

- substantial decision-bearing `file-write` closeouts require concise headed human summary before artifact path/hash/status receipt;
- "material facts" means decision-critical owner-facing facts, not full artifact pasteback, source ledgers, option tables, or evidence bodies;
- YAML is not default for every closeout, but compact courier YAML is appropriate when requested, required by output mode or contract, or useful for lane switching / handoff routing;
- `prompt-orchestration.md` owns output-mode exceptions;
- `communication-style.md` owns general chat topology and courier shape;
- `validation-gates.md` remains a collision gate, not a checklist of required YAML keys;
- the shared behavior contract inherits the rule without becoming a second overlay;
- active file-write prompts ask for material decision substance without full artifact pasteback;
- `review-report`, `paste-ready-chat`, source-heavy economy, and artifact-native tables remain intact.

## Review Questions

Answer these adversarially:

1. Does the patch preserve the ownership split between `prompt-orchestration.md`, `communication-style.md`, and `validation-gates.md`, or does it create competing authorities?
2. Does the `file-write` rule now clearly distinguish receipt-light writes from substantial decision-bearing artifacts?
3. Does the wording prevent receipt-only closeouts without forcing full artifact pasteback?
4. Does the YAML/courier-state language avoid both extremes: YAML everywhere and no YAML when lane switching needs it?
5. Does the shared behavior contract inherit the rule without over-specifying local overlay behavior?
6. Do the two active prompt closeout clauses require enough material decision substance for the owner to understand the result without opening the artifact?
7. Do the active prompt closeouts preserve artifact-local detail and avoid source-heavy readback?
8. Are `review-report` YAML-only success closeouts still protected and unweakened?
9. Is `paste-ready-chat` still protected from extra prose that would make paste-ready bodies less pasteable?
10. Does `validation-gates.md` remain a validation/collision gate rather than a mandatory output-key checklist?
11. Did the patch accidentally broad-sync stale prompts, import `jb` policy, or create lifecycle/readiness/approval claims?
12. Are there missing active prompts or templates that must be patched before the closeout contract is coherent, or should further propagation remain deferred?

## Findings Standard

List findings first, ordered by severity:

- `critical`: the patch creates a false authority, breaks review-report/paste-ready behavior, or makes the contract unsafe to accept.
- `major`: the patch leaves a meaningful ambiguity that can recreate receipt-only closeouts or YAML ritual.
- `minor`: wording, retrieval, prompt-shape, or hygiene issues that should be corrected but do not invalidate the patch.

For each finding include:

- severity;
- location with file path and tight line reference when possible;
- issue;
- evidence;
- impact;
- recommended correction.

If no issues are found, say so clearly and list residual risks or follow-up checks.

## Required Report Artifact

Write the review report to:

`docs/review-outputs/adversarial-artifact-reviews/orca_file_write_closeout_contract_adversarial_review_v0.md`

The report must include retrieval metadata and these sections:

1. `Review Summary`
   - Recommendation using one of:
     - `accept`
     - `accept_with_friction`
     - `patch_before_acceptance`
     - `reject`
     - `blocked`
   - One-sentence summary.

2. `Scope Reviewed`
   - Files reviewed.
   - Dirty/untracked state reviewed.
   - Hash match or mismatch status.

3. `Decision Criteria`
   - Ownership split.
   - Human-summary sufficiency.
   - Artifact economy.
   - Courier YAML conditionality.
   - Exception preservation.
   - Validation-gate behavior.
   - Prompt propagation boundary.

4. `Findings`
   - Findings first, ordered by severity.

5. `Non-Findings`
   - Important risks checked that did not produce findings.

6. `Residual Risks And Non-Claims`
   - No approval claim.
   - No validation/readiness claim.
   - No lifecycle, commit, merge, install, deploy, resolver, or product-readiness claim.

7. `Exact Next Authorized Step`
   - One concrete next step.

## Chat Closeout

This prompt uses `review-report` output mode. The human-readable review value belongs in the durable report.

After successfully writing the report, return only this compact YAML summary in chat:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/orca_file_write_closeout_contract_adversarial_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  summary: "One sentence describing the review result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "One concrete next step"
```

If the report cannot be written, return this failed blocked summary in chat:

```yaml
review_summary:
  status: failed
  review_location: chat_only_current_thread
  recommendation: blocked
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/orca_file_write_closeout_contract_adversarial_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve the report write failure, then rerun the review-report prompt."
```

Include enough brief human-readable failure detail to route the write failure. Do not add extra YAML keys. Do not use `report_path` for an unwritten report.

## Hard Boundaries

Do not patch files.
Do not stage, commit, push, open PRs, or claim merge safety.
Do not edit overlay, prompt templates, prompts, workflow records, review reports other than the required report, skills, workflow-kernel source, or installed/plugin/user skills.
Do not broaden the review to Orca product proof, customer discovery, implementation systems, runtime work, or unrelated dirty files.
Do not review `jb` prompt/path policy as authority.
Do not claim validation, readiness, approval, lifecycle completion, deployment/install/resolver status, product readiness, feature readiness, implementation readiness, or commercial readiness.
````

## Validation Notes

Prompt validation expectations before use:

- Overlay authority loaded.
- Template kind is `review`.
- Template source is the active Orca adversarial artifact review template.
- Output mode is `review-report`.
- Downstream report destination is under `docs/review-outputs/adversarial-artifact-reviews/`.
- Reviewer edit permission is read-only plus one review report write.
- Required target files and hashes are explicit.
- Dirty/untracked target state is explicitly in scope.
- Prompt asks for adversarial review of the patch, not patch execution.
- The prompt preserves `review-report`, `paste-ready-chat`, source-heavy economy, artifact-native table exceptions, and non-claim boundaries.
- No implementation, runtime, skill, lifecycle, commit, push, PR, or product-proof work is authorized.
