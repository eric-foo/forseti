# Orca Closeout Behavior Findings Closure Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Targeted review prompt for verifying closure of FF-01 through FF-03 from the Orca closeout behavior patch adversarial review.
use_when:
  - Asking a reviewer to verify that PG-01, PG-02, and PG-03 closed the prior advisory findings.
  - Checking whether the closeout behavior patch can move from reviewed-with-friction to accepted or needs one final micro-fix.
  - Avoiding a full broad re-review of the closeout contract after narrow follow-through patches.
authority_boundary: retrieval_only
open_next:
  - docs/review-outputs/adversarial-artifact-reviews/orca_closeout_behavior_patch_adversarial_review_v0.md
  - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
  - docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md
  - docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md
input_hashes:
  - path: .agents/workflow-overlay/communication-style.md
    sha256: D93931D97006C3167059787125857F3FB4107D2E49C1F80E71B50159F94BD3BC
  - path: .agents/workflow-overlay/prompt-orchestration.md
    sha256: 54242C83D83FBA3775738276C0D87F0C1F172849024E6F341D1E61D0851AA049
  - path: .agents/workflow-overlay/validation-gates.md
    sha256: 0DEBE6EA327EAAEBE181902235C4B91D7152C29ACBEFC5AC3466B4D145EF08C7
  - path: docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
    sha256: 125594470EA7123CA2C80F78687464B69FE304C6D3F67166E9A04D9FDE215B9F
  - path: docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md
    sha256: 615FBCA5C3903BE81B1C334B7AF6E1E1250CF51484F8C3DD4B6FC85289180229
  - path: docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md
    sha256: 389CE8FF8F760FEC726A3E3604FB55CD0137F5ADC297FF54EA4825123DE5311D
  - path: docs/review-outputs/adversarial-artifact-reviews/orca_closeout_behavior_patch_adversarial_review_v0.md
    sha256: 967BB1A53FF0911B0539A6F83B272215B233C0325E537D3F2B67A87CEE7DD20D
downstream_consumers:
  - Owner decision on accepting the closeout behavior patch or authorizing one final micro-fix.
  - Future closeout behavior patch cleanup.
stale_if:
  - Any pinned closure input hash changes before review.
  - Additional closeout behavior patches are applied before review.
  - The prior adversarial review report is superseded or corrected before review.
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
`docs/review-outputs/adversarial-artifact-reviews/orca_closeout_behavior_findings_closure_review_v0.md`

Edit permission for downstream reviewer:
Read-only review plus writing the one downstream report artifact. Do not patch overlay files, prompt templates, prompt artifacts, workflow artifacts, skills, implementation code, commits, pushes, or PRs.

## Paste-Ready Review Prompt

````markdown
# Orca Adversarial Artifact Review - Closeout Behavior Findings Closure

You are performing a targeted read-only adversarial artifact review for Orca.

Use `workflow-deep-thinking` first, then use `workflow-adversarial-artifact-review`.

The deep-thinking step should frame the closure problem, failure modes, and decision criteria before findings are listed. It does not widen review scope, authorize patching, or reopen the full closeout behavior decision.

## Workspace Preflight

Workspace:
`C:\Users\vmon7\Desktop\projects\orca`

Expected branch at prompt creation:
`main`

Expected HEAD at prompt creation:
`a873c9c3ed3b289a65f9c472c63e0aadf880a127`

Dirty state:
Required and in scope for the target files below. This review is about the current dirty follow-through patches for FF-01 through FF-03. Do not review a clean checkout as a substitute.

Before reviewing, verify:

- current workspace path is `C:\Users\vmon7\Desktop\projects\orca`;
- target-file dirty state using `git status --short -- <targets>`;
- current hashes for every file under `Pinned Closure Inputs`;
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
- `docs/review-outputs/adversarial-artifact-reviews/orca_closeout_behavior_patch_adversarial_review_v0.md`
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`
- `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`
- `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`

Use targeted searches over the closure target files for:

- `would materially benefit`
- `benefits from compact courier YAML`
- `likely to be handed`
- `HISTORICAL_PATCH_DISCUSSION`
- `superseded_by`
- `conditionally required`
- `FF-01`
- `FF-02`
- `FF-03`
- `PG-01`
- `PG-02`
- `PG-03`

## Pinned Closure Inputs

Prior review report:

- `docs/review-outputs/adversarial-artifact-reviews/orca_closeout_behavior_patch_adversarial_review_v0.md`
  - SHA256 at prompt creation: `967BB1A53FF0911B0539A6F83B272215B233C0325E537D3F2B67A87CEE7DD20D`
  - Git state at prompt creation: untracked but in scope.

Controlling overlay references:

- `.agents/workflow-overlay/communication-style.md`
  - SHA256 at prompt creation: `D93931D97006C3167059787125857F3FB4107D2E49C1F80E71B50159F94BD3BC`
  - Git state at prompt creation: modified.
- `.agents/workflow-overlay/prompt-orchestration.md`
  - SHA256 at prompt creation: `54242C83D83FBA3775738276C0D87F0C1F172849024E6F341D1E61D0851AA049`
  - Git state at prompt creation: modified.
- `.agents/workflow-overlay/validation-gates.md`
  - SHA256 at prompt creation: `0DEBE6EA327EAAEBE181902235C4B91D7152C29ACBEFC5AC3466B4D145EF08C7`
  - Git state at prompt creation: modified.

Closure target files:

- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`
  - SHA256 at prompt creation: `125594470EA7123CA2C80F78687464B69FE304C6D3F67166E9A04D9FDE215B9F`
  - Git state at prompt creation: modified.
  - Closure target: FF-01 / PG-01.
- `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`
  - SHA256 at prompt creation: `615FBCA5C3903BE81B1C334B7AF6E1E1250CF51484F8C3DD4B6FC85289180229`
  - Git state at prompt creation: untracked but in scope.
  - Closure target: FF-02 / PG-02.
- `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`
  - SHA256 at prompt creation: `389CE8FF8F760FEC726A3E3604FB55CD0137F5ADC297FF54EA4825123DE5311D`
  - Git state at prompt creation: untracked but in scope.
  - Closure target: FF-03 / PG-03.

## Review Purpose

Verify whether the three advisory findings from `orca_closeout_behavior_patch_adversarial_review_v0.md` are closed by the follow-through patches:

- FF-01: shared behavior contract used a weaker YAML trigger than the overlay.
- FF-02: major-move CA prompt used a weaker YAML trigger than the overlay.
- FF-03: CA discussion stale_if condition was met but not flagged, leaving historical "conditionally required" YAML language easy to misread.

This is a closure review, not a full second review. Do not reopen accepted non-findings from the prior report unless the follow-through patch created a new contradiction directly tied to FF-01, FF-02, or FF-03.

## Closure Checks

Answer these narrowly:

1. FF-01 closure: does `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md` now use the same threshold as the overlay: `lane switching / handoff routing would materially benefit from compact courier YAML`?
2. FF-01 regression check: did the shared behavior contract remain a template include rather than a second overlay authority?
3. FF-02 closure: does `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md` now require compact courier YAML only when continuation is expected and compact courier YAML would materially benefit that routing?
4. FF-02 regression check: does the prompt still require a headed human-readable closeout and avoid receipt-only chat?
5. FF-03 closure: does `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md` now mark itself as historical or stale after patch application?
6. FF-03 retrieval check: does the CA discussion include `superseded_by` pointers to the controlling overlay/shared-contract sources?
7. FF-03 residual-risk check: does the CA discussion clearly say its "conditionally required" YAML language is historical and superseded by the current overlay threshold?
8. Did any closure patch introduce new validation, readiness, approval, lifecycle, install/deploy/resolver, product-readiness, or implementation-readiness claims?
9. Did any closure patch import `jb` policy or broaden the patch beyond FF-01 through FF-03?

## Findings Standard

List findings first, ordered by severity:

- `critical`: a closure patch creates false authority, breaks output-mode topology, or makes the patch unsafe to accept.
- `major`: FF-01, FF-02, or FF-03 remains open or only partially closed.
- `minor`: wording, retrieval, or hygiene issue that does not keep a finding open.

Use finding IDs:

- `FC-01`, `FC-02`, etc. for new closure findings.
- In the finding body, name which original finding remains affected: `FF-01`, `FF-02`, or `FF-03`.

For each finding include:

- severity;
- affected original finding;
- location with file path and tight line reference when possible;
- issue;
- evidence;
- impact;
- recommended correction.

If all three findings are closed, say so clearly and list residual risks or follow-up checks.

## Required Report Artifact

Write the review report to:

`docs/review-outputs/adversarial-artifact-reviews/orca_closeout_behavior_findings_closure_review_v0.md`

The report must include retrieval metadata and these sections:

1. `Review Summary`
   - Recommendation using one of:
     - `accept`
     - `accept_with_friction`
     - `patch_before_acceptance`
     - `reject`
     - `blocked`
   - Closure result using one of:
     - `all_findings_closed`
     - `partially_closed`
     - `findings_still_open`
     - `blocked`
   - One-sentence summary.

2. `Scope Reviewed`
   - Files reviewed.
   - Dirty/untracked state reviewed.
   - Hash match or mismatch status.

3. `Closure Matrix`
   - FF-01 status and evidence.
   - FF-02 status and evidence.
   - FF-03 status and evidence.

4. `Findings`
   - New closure findings only, ordered by severity.

5. `Non-Findings`
   - Important closure risks checked that did not produce findings.

6. `Residual Risks And Non-Claims`
   - No approval claim.
   - No validation/readiness claim.
   - No lifecycle, commit, merge, install, deploy, resolver, implementation-readiness, or product-readiness claim.

7. `Exact Next Authorized Step`
   - One concrete next step.

## Chat Closeout

This prompt uses `review-report` output mode. The human-readable review value belongs in the durable report.

After successfully writing the report, return only this compact YAML summary in chat:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/orca_closeout_behavior_findings_closure_review_v0.md
  recommendation: accept | accept_with_friction | patch_before_acceptance | reject | blocked
  summary: "One sentence describing the closure result."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated:
    - FF-01
    - FF-02
    - FF-03
  next_action: "One concrete next step"
```

If one or more prior findings remain open, list only the closed findings under `prior_findings_remediated` and put the open closure findings under `blocking_findings` or `advisory_findings` as appropriate.

If the report cannot be written, return this failed blocked summary in chat:

```yaml
review_summary:
  status: failed
  review_location: chat_only_current_thread
  recommendation: blocked
  summary: "Failed to write required report to docs/review-outputs/adversarial-artifact-reviews/orca_closeout_behavior_findings_closure_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve the report write failure, then rerun the closure review prompt."
```

Include enough brief human-readable failure detail to route the write failure. Do not add extra YAML keys. Do not use `report_path` for an unwritten report.

## Hard Boundaries

Do not patch files.
Do not stage, commit, push, open PRs, or claim merge safety.
Do not edit overlay, prompt templates, prompts, workflow artifacts, review reports other than the required report, skills, workflow-kernel source, or installed/plugin/user skills.
Do not broaden the review into a full closeout-contract re-review unless one of the closure patches creates a direct contradiction.
Do not review Orca product proof, customer discovery, implementation systems, runtime work, or unrelated dirty files.
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
- Required closure inputs and hashes are explicit.
- Dirty/untracked target state is explicitly in scope.
- Prompt asks for closure review of FF-01 through FF-03, not patch execution.
- The prompt preserves `review-report`, `paste-ready-chat`, source-heavy economy, artifact-native table exceptions, and non-claim boundaries.
- No implementation, runtime, skill, lifecycle, commit, push, PR, or product-proof work is authorized.
