# Thin Wrapper Template v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt template
scope: Thin-wrapper template for launching an existing Forseti prompt or source artifact.
use_when:
  - A launch prompt should reference an existing full prompt without restating policy.
authority_boundary: retrieval_only
```

Template target: model-neutral.

This template is prompt-shaping guidance only. It does not recommend, require,
rank, or route runtime model choice.

Output mode: `paste-ready-chat` or `file-write`

Use shared contract:
`docs/prompts/templates/shared/forseti_prompt_behavior_contract_v0.md`

```text
You are launching a Forseti prompt from a thin wrapper.

Workspace:
`C:\Users\vmon7\Desktop\projects\forseti`

Wrapped source:
[FILL_PROMPT_OR_ARTIFACT_PATH]

Wrapped source SHA256:
[FILL_HASH_OR_NOT_APPLICABLE]

Expected branch or revision:
[FILL_BRANCH_OR_REVISION_OR_NOT_BOUND]

Dirty-state allowance:
[FILL_DIRTY_STATE_RULE]

Output mode:
[FILL_EXACTLY_ONE_OUTPUT_MODE]

Edit permission:
[read-only | docs-write | patch-only | not applicable]

Target scope:
[FILL_TARGET_FILES_OR_DIRECTORIES]

Preflight:
Before acting, verify the wrapped source path, hash when supplied, workspace,
target scope, output mode, edit permission, and any launch-specific blocker.
For repo-bound review or delegated-review work, resolve a launch-checkout
mismatch through `.agents/workflow-overlay/prompt-orchestration.md` ->
"Repo-Bound Review Target Resolution" before treating it as a blocker. If a
required binding remains missing, stale, or mismatched after any applicable
resolution, return `BLOCKED_PREFLIGHT` before editing, validating, executing, or
claiming readiness.

Prompt:
Use the wrapped source as the task authority. Preserve its intent. Do not
restate or fork project policy. Return only the output requested by the wrapped
source and this wrapper.

If this wrapper carries a Chief Architect, planning, phase-gate, or routing
decision, state that decision in human-readable prose before any agent-detail
or courier YAML. If the wrapped source or this wrapper only asks for a
paste-ready body or post-artifact receipt, preserve that task-native shape.
```
