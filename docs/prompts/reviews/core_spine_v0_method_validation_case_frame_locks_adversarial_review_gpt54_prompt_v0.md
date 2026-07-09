# GPT-5.4 High Adversarial Review Prompt: Core Spine v0 Method Validation Case-Frame Locks

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial review prompt for the Core Spine v0 method-validation case-frame lock artifact.
use_when:
  - Preparing or launching the case-frame lock adversarial artifact review.
  - Checking whether the frame-lock review scope, report destination, and non-execution boundaries are pinned.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/review-lanes.md
  - forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_frame_locks_v0.md
input_hashes:
  docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md: B4018996BECC8F79B254BF5A113265B873DCB9C1AE35746DABADAA4D99D4A537
branch_or_commit: main @ 3bf5c45cfa6879ae65c8f822eff9c185dcba8b3c
downstream_consumers:
  - docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v0.md
stale_if: Target artifact hash changes, review-lane output contract changes, or case-frame review scope is expanded beyond read-only artifact review.
```

- Prompt type: Review prompt
- Requested reviewer model: GPT-5.4 high if available
- Output mode: review-report
- Edit permission: read-only
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: `main`
- Expected HEAD at prompt preparation: `3bf5c45cfa6879ae65c8f822eff9c185dcba8b3c`
- Dirty-state allowance: dirty state allowed; untracked Orca docs, prompts, overlay files, and review-output folders may be present and in scope only when listed below or needed to interpret the target artifact
- Target artifact:
  - `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`
- Target artifact SHA256 at prompt preparation:
  - `B4018996BECC8F79B254BF5A113265B873DCB9C1AE35746DABADAA4D99D4A537`
- Report destination:
  - `docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v0.md`

## Objective

Run one narrow adversarial artifact review of the Core Spine v0 method
validation case-frame lock artifact.

The review should answer whether the artifact is safe to use as the immediate
pre-replay lock record before any later evidence replay. Focus on whether it
preserves cutoff discipline, avoids hindsight contamination, keeps
case-study-like detail under control, keeps `NEEDS_VERIFICATION` honest, and
does not authorize work beyond case-frame locking.

Do not run evidence replay, verify external case facts, browse, collect source
pools, patch files, or prepare a patch queue. Write the review report only to
the report destination above.

## Required Skill Invocation

Use `workflow-deep-thinking` first.

Then use `workflow-adversarial-artifact-review`.

The deep-thinking step should frame the boundary problem: the artifact must
contain enough detail to make later validation disciplined, but not enough
case-study narrative or outcome knowledge to bias the at-cutoff replay.

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
- `docs/product/core_spine_v0_information_production_foundation_v0.md`
- `docs/product/core_spine_v0_proof_protocol_v0.md`
- `docs/product/core_spine_v0_first_proof_run_packet_v0.md`
- `docs/product/core_spine_v0_method_validation_rubric_v0.md`
- `docs/product/core_spine_v0_method_validation_case_locks_v0.md`
- `docs/product/core_spine_v0_method_validation_case_frame_lock_contract_v0.md`
- `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`

Also check:

- `git status --short --branch`
- `git log --oneline -6`

## Current Decision Context

The five method-validation case identities are locked:

1. `MV-01` - Intercom Fin pressure on Zendesk.
2. `MV-03` - Stack Overflow response to ChatGPT.
3. `MV-04` - Unity Runtime Fee.
4. `MV-05` - Reddit API and data pricing.
5. `MV-09` - Thomson Reuters / Casetext legal AI response.

The case-frame lock artifact claims:

- all five frames are locked as `LOCKED_WITH_NEEDS_VERIFICATION`;
- none are blocked;
- remaining blockers are verification needs around cutoff/source visibility;
- no evidence replay, source maps, feature planning, or implementation are
  authorized.

The next intended move after review is either:

- accept the case-frame locks as safe input for later evidence replay
  authorization; or
- identify targeted frame-lock patches needed before replay authorization.

Do not decide replay authorization in this review.

## Boundary Problem To Stress-Test

Use this boundary frame as review input, not as a prewritten verdict.

The case-frame artifact must contain enough detail to constrain replay without
pre-populating the replay. Safe detail constrains degrees of freedom: cutoff
windows, source-family boundaries, allowed action verbs, evidence standards,
post-window exclusion rules, and result-label semantics. Dangerous detail
populates the replay: narrative arcs, outcome explanations, causal claims,
moralized judgments, implied recommendations, or reframe paths that simply
mirror known outcomes.

During review, specifically test these risk clusters:

- Enough versus too much. Source-family boundaries are safe when they constrain
  admissible source types; they become risky when they read like search briefs.
  Outcome-comparison windows are safe when they bound calibration; they become
  risky when they name concrete post-window outcome details. Reframe labels are
  safe when they define result semantics; they become risky when they name the
  path the later outcome actually took.
- `MV-01` contamination vector. Check whether naming "Resolution Platform
  material" in the post-window exclusion rule unnecessarily exposes a specific
  post-window Zendesk response. Also check whether the fair-cutoff rationale
  independently explains fairness or merely says the cutoff is before the
  known outcome.
- `MV-03` contamination vector. Check whether the reframe condition around
  verified developer knowledge, trusted-data licensing, and workflow retrieval
  mirrors the known post-announcement direction too closely. Also check whether
  the detailed second-order source boundary functions as a disciplined boundary
  or an overly specific search brief.
- `MV-04` asymmetry vector. Check whether the reverse-case frame makes
  downgrade evidence much easier to find than upgrade evidence, and whether
  that asymmetry is acceptable for a reverse pricing/trust case or should be
  made explicit.
- `MV-05` cutoff and authorization vector. Check whether the provisional
  2023-05-30 cutoff depends on post-window knowledge of app shutdowns and
  protests, whether the outcome-comparison window collapses if the cutoff moves
  into June, whether IPO/data-licensing references prime the reader with
  post-window context, and whether the reframe conditions read like a
  remediation plan rather than neutral result semantics.
- `MV-09` positive-action bias vector. Check whether the positive-action case
  is structurally biased toward caution through a high convergence threshold,
  a long caution-side "not obvious" list, and outcome knowledge from the
  acquisition announcement. If this makes a positive-action result
  structurally unlikely, treat it as a portfolio-level validation risk, not
  mere wording friction.
- `NEEDS_VERIFICATION` propagation. Check whether provisional cutoff or
  source-visibility gaps cascade into downstream fields such as
  outcome-comparison windows, source-family boundaries, or fair-cutoff
  rationales. A field marked `NEEDS_VERIFICATION` must not be used as if
  already confirmed.
- Authorization drift. Check whether Section 10's "before evidence replay"
  verification checklist could be misread as saying that completing
  verification authorizes replay. Verification completion does not itself
  authorize replay.

The review must explicitly resolve these five decision-relevant questions:

1. Does the `MV-09` frame bias make the positive-action case structurally
   unlikely to return a positive-action result?
2. Does the `MV-05` provisional cutoff create a potential blocker rather than
   a routine `NEEDS_VERIFICATION` gap?
3. Do the `MV-03` and `MV-05` reframe conditions describe neutral move
   categories, or do they leak known outcome paths?
4. Should Section 10 include a stronger non-authorization statement after the
   verification checklist?
5. Does naming `Resolution Platform` in `MV-01` contaminate replay, or does the
   exclusion rule adequately quarantine it?

## Dirty State Allowance

Dirty state is allowed. Modified and untracked Orca docs and prompt files may
exist. Do not clean, revert, stage, commit, switch branches, or edit files.

If the workspace is not `C:\Users\vmon7\Desktop\projects\orca`, the reviewer
cannot access the pinned worktree, the target artifact is missing or unreadable,
the target artifact hash differs from the pinned hash, or the artifact conflicts
with the accepted scope above, return a blocked result instead of reviewing a
substitute checkout or reconstructed copy.

Do not require a clean tree. Dirty state is allowed because the target artifact
and several supporting product/prompt artifacts may be untracked during this
docs-first sequence.

## Prompt Validation Gates

Before reviewing, check and record:

- Overlay authority loaded: `AGENTS.md` and `.agents/workflow-overlay/README.md`
  were read.
- Artifact roles bound: review prompt, product artifact, and review report
  roles map to `.agents/workflow-overlay/artifact-roles.md`.
- Source resolution clean: installed skills are runtime copies; `jb` project
  policy is not Orca authority.
- Worktree preflight present: workspace, branch, HEAD, dirty-state allowance,
  target artifact, target hash, edit permission, and report destination are
  explicit.
- Output mode explicit: exactly one output mode is named, `review-report`.
- Required checks named: review can return completed, blocked, reject,
  patch-before-acceptance, accept-with-friction, or accept as recommendation
  labels without claiming owner acceptance.
- Retrieval metadata bounded: the header is retrieval-only and does not create
  authority, validation proof, approval, readiness, lifecycle completion,
  deployment/install/resolver status, or edit permission.
- Leakage gate: the prompt does not import `jb` templates, GAP/CV Engine paths,
  compiler paths, handoff rules, product-lead rules, or repo-local lifecycle
  mechanics.

## Review Scope

Review only these risks:

- cutoff contamination: a cutoff sits after the outcome window, after the
  company move being judged, or after source families that should be
  post-window;
- recommendation leakage: the frame implies what Orca should recommend before
  replay;
- case-study drift: the frame becomes a rich narrative, outcome story, or
  marketing case study instead of a lock record;
- source-boundary looseness: first-order or second-order source-family
  boundaries are too broad to prevent later source fishing;
- `NEEDS_VERIFICATION` misuse: verification gaps are hidden, minimized, or used
  as if already proven;
- authorization leakage: the artifact authorizes evidence replay, source maps,
  source inventories, data spine, feature planning, implementation, or runtime
  tooling;
- portfolio imbalance: positive-action and reverse-case roles are not preserved
  or are framed in a way that pre-biases validation;
- replacement-rule weakness: blocked cases could be replaced with easier cases
  that do not preserve the same validation role.

After correctness findings, optionally note friction only if it affects the
next Chief Architect decision.

## Excluded Scope

Do not verify whether the external source URLs are correct.

Do not judge whether a case will pass, fail, upgrade, downgrade, or validate
Orca.

Do not judge whether Intercom Fin, Stack Overflow, Unity, Reddit, or Thomson
Reuters made good or bad decisions.

Do not review implementation, code, tests, runtime architecture, source
collection systems, dashboards, scrapers, APIs, databases, scoring engines,
automation, feature plans, or commercial willingness to pay.

Do not prepare a patch queue. Suggested remediation may be advisory prose only.

## Output Style

Follow `.agents/workflow-overlay/communication-style.md`.

Use short headers. Use bullets with a small explanation for each bullet. Do not
bold bullet leads by default.

Decision first, scope second, next action third.

## Output Contract

Write the durable review report to:

`docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v0.md`

This prompt uses `review-report` output mode. The human-readable review value
belongs in the durable report above. Chat YAML is courier output only and is
valid only after that report has been successfully written.

The report must contain:

1. Review target and source-read ledger.
2. Dirty sources relied on.
3. Scope and excluded scope.
4. Boundary-problem resolution covering the five decision-relevant questions
   above.
5. Correctness findings first.
6. Friction findings only if material.
7. Not-proven boundaries.
8. Blockers or no-blocking-finding statement.
9. Next authorized step.
10. Review-use boundary.

Finding format:

- `AR-01`: one-sentence finding title.
- Location: file and stable section heading or search key.
- Evidence: quote or short paraphrase from the artifact.
- Why it matters: concrete effect on replay safety, boundary control, or
  Chief Architect sequencing.
- Next action: advisory only; no patch execution.

If there are no blocking findings, say so directly. Do not claim the artifact
is approved, accepted, validated, evidence-replay-ready, feature-ready,
implementation-ready, or committed.

Findings are decision input for the Chief Architect. They are not mandatory
remediation unless separately accepted and authorized.

After successfully writing the report, return only a compact YAML summary in
chat:

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v0.md
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
  summary: "Failed to write required report to docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v0.md."
  findings_count: 0
  blocking_findings: []
  advisory_findings: []
  prior_findings_remediated: []
  next_action: "Resolve the report write failure, then rerun the review-report prompt."
```

Include enough brief human-readable failure detail to route the write failure.
Do not add extra YAML keys.
