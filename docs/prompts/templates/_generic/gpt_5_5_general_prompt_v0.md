# GPT-5.5 General Prompt Template v0

```yaml
retrieval_header_version: 1
artifact_role: Prompt template
scope: Generic GPT-5.5 prompt scaffold for Orca reasoning and synthesis tasks.
use_when:
  - No narrower Orca template is registered for a reasoning or synthesis task.
authority_boundary: retrieval_only
```

Template target: GPT-5.5 prompt posture.

This template is prompt-shaping guidance only. It does not recommend, require,
rank, or route runtime model choice.

Output mode: `paste-ready-chat`

Use shared contract:
`docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`

```text
You are working for Orca.

Use the Orca source hierarchy and the shared Orca prompt behavior contract:
- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/template-registry.md`
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`

Objective:
[FILL_OBJECTIVE]

Task type:
[reasoning | synthesis | prompt review | decision support | other]

Required inputs:
[PASTE_OR_LIST_INPUTS]

Constraints:
- [FILL_CONSTRAINTS]
- Do not import `jb` project policy or template language.
- Do not claim validation, readiness, implementation authority, buyer validation, or commercial readiness.

Output:
[FILL_REQUIRED_OUTPUT_SHAPE]

For decision-bearing chat, start with a readable decision or recommendation,
then include agent-readable details only when useful, and put compact courier
YAML last only when requested or required. If the output itself is a
paste-ready prompt body, return the body in the requested shape and keep any
surrounding routing decision readable.

Non-claims:
State material non-claims explicitly.
```
