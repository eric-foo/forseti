# Source-Gated Method Contract Upstream And JB Adoption CA Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: Chief Architect prompt for deciding how to adopt the Source-Gated Method Contract across Agent Workflow and JB without using Orca project policy as cross-project authority.
use_when:
  - Asking a Chief Architect to plan the reusable workflow-kernel and JB adoption route for source-gated method sequencing.
  - Preventing prompts from applying workflow methods before task sources are loaded.
  - Comparing whether the fix belongs in prompt-orchestrator source, project overlays, prompt templates, or method skills.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
  - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
stale_if:
  - Agent Workflow prompt-orchestrator source already accepts a source-gated method contract.
  - JB overlay or shared prompt contract already accepts an equivalent source-readiness gate.
  - Orca prompt-orchestration policy changes the Source-Gated Method Contract.
```

## Prompt Status

Status: `PROMPT_ARTIFACT_V0`.

Template kind: `handoff`.

Target actor: Chief Architect for workflow-kernel / JB adoption planning.

Output mode for downstream CA: `chat-only` unless the receiving thread
explicitly authorizes a durable file-write or patch-queue output.

Edit permission for downstream CA:
Read-only planning by default. Do not edit Agent Workflow source, installed
global/user/plugin skills, JB overlay files, Orca overlay files, prompt
templates, or project docs unless the receiving thread explicitly grants patch
authority.

## Why This Prompt Exists

Orca hit the same sequencing defect repeatedly: prompts instructed agents to
"use", "invoke", or "apply" workflow methods before task sources were loaded.
The result is predictable source-free framing, architecture, or review
conclusions with citations attached later.

This is not primarily a `workflow-deep-thinking` defect. It is an
orchestration-contract gap. Methods may be read early as procedural references,
but they must not be applied until task-specific source context is loaded and a
readiness gate is declared.

Orca has adopted a local project-overlay version of the fix. This prompt asks a
fresh CA to determine the best reusable and JB-specific adoption route without
copying Orca policy into other projects.

## Source-Gated Method Contract To Evaluate

Use this as the candidate contract, not as a pre-accepted cross-project rule:

```text
Definitions:
- REFERENCE-LOAD a method = read its instructions and make them available as
  procedural guidance only.
- APPLY a method = use it to analyze, frame, evaluate, synthesize, decide,
  recommend, or produce findings.

Sequence:
1. Read authority and operating instructions.
2. REFERENCE-LOAD required method or skill instructions.
3. Do not APPLY any method yet.
4. SOURCE-LOAD all task-specific source material.
5. Build a source context record: sources read, targeted sections read, missing
   or unavailable sources, excluded sources, and source conflicts.
6. Declare SOURCE_CONTEXT_READY, or SOURCE_CONTEXT_INCOMPLETE with missing
   items and gaps.
7. Only after that declaration, APPLY the methods to the loaded source context.
8. Synthesize and verify against the source context.

Pre-source restriction:
Before SOURCE_CONTEXT_READY, an agent may only prepare neutral source-reading
questions or checklists from method instructions. It must not produce problem
framing, architecture recommendations, critique findings, option rankings,
root-cause claims, verdicts, conclusions, or recommendations unless the method
itself is the source-loading task.

Grounding rule:
Any method-derived conclusion must be traceable to loaded task sources.
Citations added after the fact do not cure a sequencing violation.
```

## Required Source Loading

Follow the Source-Gated Method Contract while running this prompt.

REFERENCE-LOAD method instructions only:

- `workflow-deep-thinking`
- `workflow-problem-framing`
- `workflow-architecture-planning`, standard profile, only if the receiving
  thread is actually comparing adoption architecture options.

Do not APPLY these methods before source readiness.

SOURCE-LOAD only the smallest current sources needed for the receiving
workspace:

- Agent Workflow prompt-orchestrator source or prompt-authoring source.
- Agent Workflow source-loading source, if one exists.
- Agent Workflow architecture/review/deep-thinking method sources only if the
  candidate patch might touch those methods.
- JB `.agents/workflow-overlay/source-loading.md`.
- JB shared prompt behavior contract or prompt template source, if present.
- Any JB workflow overlay or prompt-orchestration source that currently governs
  prompt creation.

If the receiving thread is not rooted in Agent Workflow or JB, report
`SOURCE_CONTEXT_INCOMPLETE` with the missing workspace/source paths instead of
guessing.

Do not load broad prompt histories, old review outputs, hygiene queues, proof
packets, or unrelated product docs by default.

## Decision To Make

Decide the highest-leverage adoption architecture for preventing premature
method application across:

- reusable Agent Workflow prompt authoring;
- project-local overlays such as Orca and JB;
- shared prompt behavior contracts/templates;
- method skills such as deep-thinking, architecture planning, product planning,
  and artifact review.

Do not average. Identify the correct owner layer for the core rule and the
minimal project-local patches needed to make the rule effective.

## Options To Compare

Compare at least:

- Patch Agent Workflow prompt-orchestrator / prompt-authoring guidance only.
- Patch every method skill individually.
- Patch only project overlays such as Orca and JB.
- Patch Agent Workflow prompt-orchestrator plus project overlays/templates.
- Patch a reusable source-loading contract and make prompt-orchestrator point
  to it.
- Do nothing except fix individual prompts as they fail.

You may add a stronger hybrid if source evidence supports it.

## Required Output

Return:

1. Source-readiness declaration: `SOURCE_CONTEXT_READY` or
   `SOURCE_CONTEXT_INCOMPLETE`, with sources read, missing sources, excluded
   sources, and conflicts.
2. Problem frame: what failure is being fixed and what is out of scope.
3. Architecture option comparison.
4. Recommended owner layer for the reusable rule.
5. Recommended JB adoption surface.
6. Whether any method skill should be patched, and if so, with only a tiny
   cross-reference or a substantive contract.
7. Minimal patch queue, with target files and exact intent, but no patch hunks
   unless the receiving thread explicitly asks for patch authoring.
8. Review criteria for future prompts: what should fail or pass.
9. Deferred items and non-claims.

## Hard Boundaries

- Do not edit files unless separately authorized in the receiving thread.
- Do not install, uninstall, rename, promote, shadow, or rewrite global/user or
  plugin skills.
- Do not copy Orca overlay policy into JB or Agent Workflow as authority.
- Do not import JB product, lifecycle, protected-path, or validation policy into
  Agent Workflow.
- Do not claim adoption, validation, readiness, install status, resolver
  behavior, or prompt correctness from this planning pass.
- Do not treat this Orca prompt as authority outside Orca; it is decision input
  for the receiving CA.

## Expected Strong Answer Shape

The likely winning direction is a hybrid:

- reusable Source-Gated Method Contract in Agent Workflow prompt-orchestrator or
  canonical prompt-authoring guidance;
- project-local adoption in JB overlay/template surfaces;
- no broad edits to every method skill;
- at most tiny cross-references inside high-use method skills if source evidence
  shows prompts keep bypassing the prompt-orchestrator layer.

Do not accept that direction without checking the loaded sources. If source
evidence shows a better owner layer, recommend that instead.
