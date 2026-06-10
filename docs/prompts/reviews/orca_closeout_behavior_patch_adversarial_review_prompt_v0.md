# Orca Closeout Behavior Patch Adversarial Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: Read-only adversarial review prompt for the Orca closeout-behavior patch that changed file-write chat closeouts toward headed human prose plus artifact receipts, with no YAML by default.
use_when:
  - Reviewing the current closeout-behavior patch for policy collisions.
  - Checking whether Orca file-write closeouts now preserve human comprehension without requiring YAML by default.
  - Preparing a durable adversarial artifact review report for the closeout-behavior patch.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/communication-style.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/validation-gates.md
  - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
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
  - path: docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md
    sha256: 37E8DFBA790595799354D52ED2875B8A501F103E14E83A2E325A28415AA9620D
downstream_consumers:
  - Closeout-behavior patch cleanup.
  - Future Orca prompt-orchestration and communication-style patches.
stale_if:
  - Any target file hash changes before review starts.
  - Owner changes the accepted no-YAML-default closeout rule.
  - The closeout-behavior patch is superseded or reverted.
```

## Prompt Status

Status: `PROMPT_ARTIFACT_V0`.

Template kind: `review`.

Template source:
`docs/prompts/templates/review/adversarial_artifact_review_v0.md`

Target review skill sequence:

1. `workflow-deep-thinking`
2. `workflow-adversarial-artifact-review`

Output mode for downstream reviewer:
`review-report`.

Downstream report path:
`docs/review-outputs/adversarial-artifact-reviews/orca_closeout_behavior_patch_adversarial_review_v0.md`

Reviewer edit permission:
Read-only for all source files. The reviewer may write only the downstream
review report at the path above. Do not patch overlay files, prompt templates,
active prompts, workflow records, skills, runtime code, tests, commits, pushes,
or PRs.

## Paste-Ready Review Prompt

```markdown
# Orca Adversarial Artifact Review - Closeout Behavior Patch

You are performing a read-only adversarial artifact review for Orca.

Use `workflow-deep-thinking` first.

Then use `workflow-adversarial-artifact-review`.

The deep-thinking step should frame the boundary problem, failure modes, and
decision criteria before findings are listed. It does not widen review scope,
authorize patching, or turn this into product planning.

## Review Purpose

Review the current Orca closeout-behavior patch for contract consistency.

The accepted owner direction is:

- for short chat-native output without a durable artifact, use clear headed
  formatting with slightly less prose;
- for substantial `file-write` artifacts, use a concise headed human summary
  plus artifact path/hash/status receipt;
- do not require YAML by default;
- YAML may still exist where an output mode explicitly requires it, such as the
  existing `review-report` saved-report courier summary.

The review should determine whether the current patch cleanly implements that
direction, or whether any overlay, validation gate, shared template, active
prompt, or stale discussion artifact still creates ambiguity.

## Workspace Preflight

Workspace:
`C:\Users\vmon7\Desktop\projects\orca`

Expected branch:
`main`

Expected HEAD at prompt creation:
`a873c9c3ed3b289a65f9c472c63e0aadf880a127`

Dirty state:
Allowed and material. This review is specifically about current uncommitted and
untracked Orca docs/overlay changes in this worktree. Review the target files
in place. Do not clone, switch branches, reset, restore, stage, commit, push,
or open a PR.

If launched outside this workspace and the pinned workspace is accessible,
change directory to the pinned workspace before reviewing. If the workspace is
not accessible, return `BLOCKED_REVIEW_WORKTREE_UNAVAILABLE` in the report and
chat summary. Do not review a substitute checkout.

## Source Hierarchy

Use this source hierarchy:

1. Explicit owner direction in this prompt.
2. Orca `AGENTS.md`.
3. `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with overlay.
5. Reusable workflow guidance only for generic mechanics, never Orca facts.

If reusable workflow guidance conflicts with Orca overlay for Orca facts, the
overlay wins. Do not import `jb` rules, paths, handoffs, lifecycle mechanics,
GAP policy, validation habits, prompt templates, or product policy.

## Required Reads

Read these before reviewing:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/template-registry.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`
- `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`
- `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`
- `docs/prompts/reviews/orca_closeout_behavior_patch_adversarial_review_prompt_v0.md`

Use targeted `rg` searches over `.agents/workflow-overlay/` and `docs/prompts/`
for:

- `courier YAML`
- `courier state`
- `YAML is not required`
- `YAML should not be`
- `lane switching`
- `handoff routing`
- `file-write`
- `path/hash/status`
- `receipt-only`
- `headed human`
- `human summary`
- `review-report`
- `paste-ready-chat`
- `Chat Closeout`

Read additional prompt files only if they materially affect whether the patch
surface is internally consistent. Do not broad-sync or review stale prompts by
default.

## Target Files And Prompt-Creation Hashes

If any target hash differs before review starts, report the mismatch and decide
whether it blocks the review or can be reviewed as current dirty-state evidence.
Do not substitute another source for a mismatched controlling source.

- `.agents/workflow-overlay/communication-style.md`:
  `D93931D97006C3167059787125857F3FB4107D2E49C1F80E71B50159F94BD3BC`
- `.agents/workflow-overlay/prompt-orchestration.md`:
  `54242C83D83FBA3775738276C0D87F0C1F172849024E6F341D1E61D0851AA049`
- `.agents/workflow-overlay/validation-gates.md`:
  `0DEBE6EA327EAAEBE181902235C4B91D7152C29ACBEFC5AC3466B4D145EF08C7`
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`:
  `CB892EB9ED69E800672C6B32A679517C459C85B17D2C2A6E238D5FBA3015A3B6`
- `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`:
  `DFCF2865434CC4405846C0842A4789ACBB787477C64C2B6BCF6D518BB5D2626F`
- `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`:
  `37E8DFBA790595799354D52ED2875B8A501F103E14E83A2E325A28415AA9620D`

## Known Risk To Test

The patch was intended to remove YAML-by-default behavior. Review especially
whether any language still reintroduces YAML by default through loose wording
such as:

- YAML when lane switching would materially benefit;
- YAML when handoff routing would materially benefit;
- courier YAML being treated as the normal third layer rather than an explicit
  exception;
- validation gates allowing broader YAML usage than `communication-style.md`
  and `prompt-orchestration.md`.

Do not assume these are defects merely because they are listed here. Treat them
as review hypotheses and decide from the sources.

## Review Questions

Answer these in the report:

1. Does the patch clearly establish headed human prose as the default closeout
   shape?
2. Does the patch clearly avoid requiring YAML by default?
3. Are substantial decision-bearing `file-write` artifacts required to include
   a concise human summary before path/hash/status receipt?
4. Do `communication-style.md`, `prompt-orchestration.md`,
   `validation-gates.md`, and the shared behavior contract agree with each
   other?
5. Does the major-move CA prompt now prevent receipt-only closeout without
   causing full artifact pasteback?
6. Does the older CA discussion artifact remain useful historical context, or
   does it now risk misleading future agents by recommending more YAML than the
   owner accepted?
7. Are `review-report` YAML-only saved-report behavior and `paste-ready-chat`
   prompt-body behavior preserved?
8. Are source-heavy economy and artifact-native table exceptions preserved?
9. Did the patch introduce any overclaim, validation/readiness claim,
   lifecycle claim, resolver claim, implementation authorization, or imported
   `jb` policy?
10. Is the prompt-creation hash pinning coherent, especially for active prompts
    that pin patched overlay inputs?

## Findings Bar

Prioritize issues that would cause future Orca agents to:

- return YAML by default despite the owner rejecting that default;
- return receipt-only chat for substantial decision artifacts;
- paste full artifacts or source-heavy evidence into chat;
- weaken `review-report` or `paste-ready-chat` exceptions;
- treat historical CA discussion text as current authority over the overlay;
- spread the rule into stale prompts without owner authorization;
- claim validation, readiness, approval, lifecycle completion, resolver status,
  implementation readiness, or product readiness.

Do not list stylistic preferences as findings unless they create a real routing
or behavior risk.

## Output Mode And Report Contract

Use output mode: `review-report`.

Write the durable report to:
`docs/review-outputs/adversarial-artifact-reviews/orca_closeout_behavior_patch_adversarial_review_v0.md`

The report must include retrieval metadata and these sections:

1. `Review Summary`
   - Recommendation: `accept`, `accept_with_friction`,
     `patch_before_acceptance`, `reject`, or `blocked`.
   - One-sentence summary.

2. `Scope And Sources`
   - Target files reviewed.
   - Hash mismatch status.
   - Dirty-state handling.

3. `Decision Contract Under Review`
   - The accepted no-YAML-default closeout behavior.
   - The preserved output-mode exceptions.

4. `Findings`
   - Findings first, ordered by severity.
   - Use IDs such as `FF-01`.
   - For each finding include severity, location, issue, evidence, impact, and
     recommended correction.

5. `Non-Findings`
   - Important risks checked that did not fail.

6. `Stale Or Historical Artifact Risk`
   - Whether `docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`
     should be treated as historical, stale, misleading, or still useful.

7. `Patch Guidance`
   - Conceptual patch guidance only.
   - Do not create patch queues or apply patches.

8. `Non-Claims`
   - No approval, validation, readiness, lifecycle, resolver, deployment,
     install, implementation, product-readiness, or merge-safety claim.

9. `Exact Next Authorized Step`
   - One next move.

After the report is successfully written, return only the compact
`review_summary` YAML shape from `.agents/workflow-overlay/communication-style.md`
in chat, with `status: completed` and `report_path` pointing to the written
report. The YAML is valid here because `review-report` explicitly owns that
saved-report exception.

If the report cannot be written, do not use `report_path`. Return the failed
`review_summary` shape with `status: failed`,
`review_location: chat_only_current_thread`, and `recommendation: blocked`.
Name the failed path and include enough human-readable routing detail in
`summary` or `next_action` to route the failure. Do not add extra YAML keys.

## Hard Boundaries

Do not patch files.
Do not create a patch queue.
Do not edit overlay files, prompt templates, active prompts, workflow records,
skills, workflow-kernel source, installed/user/plugin skills, product docs,
runtime code, tests, packages, automation, commits, pushes, or PRs.
Do not import `jb` rules or templates.
Do not claim approval, validation, readiness, lifecycle completion, resolver
behavior, deployment/install status, implementation readiness, product
readiness, or merge safety.
```

## Prompt Validation Notes

- Overlay authority loaded.
- Template kind is `review`.
- Template source is the Orca adversarial artifact review template.
- Output mode is `review-report`.
- Downstream report destination is bound under
  `docs/review-outputs/adversarial-artifact-reviews/`.
- Reviewer edit permission is read-only except for the report write.
- The prompt explicitly triggers `workflow-deep-thinking` before
  `workflow-adversarial-artifact-review`.
- The prompt targets the no-YAML-default closeout behavior and preserves the
  `review-report` saved-report YAML exception.
- No patch execution, staging, commit, push, PR, lifecycle, resolver, install,
  deploy, implementation, or readiness authority is granted.
