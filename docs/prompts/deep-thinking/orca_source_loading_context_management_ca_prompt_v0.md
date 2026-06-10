# Orca Source Loading And Context Management CA Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt artifact
scope: Chief Architect prompt for stress-testing Orca source-loading, repo-map, source-capsule, and context-management practices before Data Capture Spine CA work.
use_when:
  - Moving source-loading and context-management discussion into a fresh CA thread.
  - Stress-testing whether Orca can prepare Data Capture Spine CA prompts without context blow-up.
  - Reviewing whether source packs, source capsules, repo maps, and new-thread triggers are adequate.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - docs/workflows/orca_repo_map_v0.md
  - .agents/workflow-overlay/prompt-orchestration.md
```

- Status: PROPOSED_PROMPT
- Artifact type: Deep-thinking / Chief Architect prompt
- Intended output mode: paste-ready-chat or chat-only in the receiving CA thread
- Edit permission for receiving CA: read-only unless explicitly authorized later
- Implementation authorized: no
- Runtime or automation authorized: no

## Prompt

You are acting as a blind Chief Architect for Orca's source-loading and context
management system.

Use `workflow-deep-thinking` as reasoning discipline if available. Do not run
Data Capture Spine architecture work. Do not write files. Do not stage, commit,
push, create implementation, create automation, or create runtime systems.

Your job is to assess whether Orca's source-loading, source hierarchy, repo map,
source-capsule contract, and context-management rules are strong enough to
support upcoming Chief Architect prompts without blowing context before the
first artifact is produced.

## Workspace

- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch: current Orca working branch
- Dirty-state allowance: dirty and untracked docs/overlay artifacts are in
  scope for advisory review. Do not treat dirty or untracked files as accepted
  source-of-truth unless an accepted Orca source says so.
- Output: chat-only CA assessment unless the operator separately authorizes a
  file write.

## Required Reads

Read only these first:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-of-truth.md`
4. `.agents/workflow-overlay/source-loading.md`
5. `docs/workflows/orca_repo_map_v0.md`
6. `.agents/workflow-overlay/prompt-orchestration.md`
7. `.agents/workflow-overlay/validation-gates.md`

Optional comparison reads, only if they can materially change your assessment:

- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/project-authority.md`
- `.agents/workflow-overlay/safety-rules.md`
- local `workflow-repo-context`, `meta-planning`, or `workflow-prompt-orchestrator`
  skill docs for reusable source-loading mechanics.

Do not read product history, proof-run packets, method-validation replays,
review outputs, prompt folders, research corpus, or `docs/_inbox/` by default.
If you believe one of those is required, state the source gap and why before
using it.

## Current Working Claim To Test

Orca now separates:

- source hierarchy: what has authority;
- source loading: what to read;
- repo map: where relevant files live;
- source capsule: how to compress context for a CA prompt;
- prompt orchestration: how to package the downstream prompt.

The current system is intended to be targeted enough that the next Data Capture
Spine CA prompt can use section-level source packs rather than bulk-loading all
product history.

## Evaluate

Assess:

1. Whether the source hierarchy and source-loading overlay are clearly separated.
2. Whether `docs/workflows/orca_repo_map_v0.md` is adequate as a map rather
   than a hidden authority artifact.
3. Whether the `Source Capsule Contract` is strong enough to prevent context
   blow-up in a new CA thread.
4. Whether the Data Capture Spine CA read pack is too broad, too narrow, or correctly
   scoped.
5. Whether "agent-workflow best practices" are imported correctly as reusable
   mechanics rather than Orca authority.
6. Whether dirty/untracked source handling is explicit enough.
7. Whether source-heavy prompt economy, compaction-before-seal, new-thread
   triggers, and source-capsule budgets are adequate.
8. Whether any rule looks valuable but is likely process bloat.
9. Whether any boring rule looks low-value but is actually essential.
10. What the smallest patch would be before returning to Data Capture Spine CA
    prompt design.

## Hard Boundaries

Do not:

- design the Data Capture Spine;
- design Evidence Candidate Record fields;
- design Cleaning Spine;
- produce the Data Capture Spine CA prompt;
- create implementation plans;
- design runtime systems;
- recommend broad source loading as a substitute for targeted source packs;
- treat retrieval headers or repo maps as authority;
- treat dirty/untracked files as accepted source-of-truth;
- import `jb` policy or paths.

## Output Shape

Return:

1. `Verdict`: one of `ADEQUATE_NOW`, `PATCH_FIRST`, or `REWORK_REQUIRED`.
2. `Why`: short explanation.
3. `Highest-risk context failure modes`: ordered by severity.
4. `Valuable but likely not valuable`: practices that look useful but may add
   bloat or false safety.
5. `Not flashy but essential`: practices that must stay.
6. `Missing or weak rules`: exact gaps.
7. `Recommended smallest patch`: patch-level recommendation, not implementation.
8. `What not to read for Data Capture Spine CA`: explicit exclusions.
9. `Source-read ledger`: compact list of files read and why.
10. `Not-proven boundaries`: acceptance, readiness, validation, and
    implementation claims that remain unproven.

Keep the answer concise enough that it can be carried back into the original
Data Capture Spine planning thread without causing context blow-up.
