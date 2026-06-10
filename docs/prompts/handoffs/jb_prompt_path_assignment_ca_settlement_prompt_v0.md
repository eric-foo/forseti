# JB Prompt Path Assignment CA Settlement Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: Handoff prompt for a JB Chief Architect to settle whether JB needs default prompt and report path-assignment behavior.
use_when:
  - Asking a JB Chief Architect to decide whether JB has the same prompt/report path-assignment defect observed in Orca.
  - Preparing a JB-local workflow-overlay or prompt-contract patch route.
  - Preserving cross-project boundary between Orca prompt drafting and JB authority.
authority_boundary: retrieval_only
open_next:
  - C:\Users\vmon7\Desktop\projects\jb\AGENTS.md
  - C:\Users\vmon7\Desktop\projects\jb\docs\workflow-overlay.md
  - .agents/workflow-overlay/prompt-orchestration.md
input_hashes:
  - path: .agents/workflow-overlay/prompt-orchestration.md
    sha256: 9E159E3A7CC933083F56C95EBDDED4E19B2F51D55EE8EF774F3BEC62D566834F
  - path: C:\Users\vmon7\Desktop\projects\jb\AGENTS.md
    sha256: 34406B5BDE0D48221827727CDF32D0FBC5D394FB3F3999DE896D8B94CCEADD70
  - path: C:\Users\vmon7\Desktop\projects\jb\docs\workflow-overlay.md
    sha256: 5F707D6357D1EA27C6C2C2667A1A9FA71C452B5B4E4DA74B78C588521A8D46C4
downstream_consumers:
  - JB Chief Architect prompt-path behavior settlement.
  - Future JB workflow-overlay patch route, if accepted by JB authority.
stale_if:
  - JB AGENTS.md or docs/workflow-overlay.md changes.
  - Orca prompt-orchestration default path-assignment rule changes materially.
  - Owner directly accepts or rejects carrying the behavior into JB before this prompt is used.
```

## Prompt Status

Status: `PROMPT_ARTIFACT_V0`.

Template kind: `handoff`.

Target actor: JB Chief Architect.

Output mode for downstream JB CA: `file-write`.

Downstream output path:
`C:\Users\vmon7\Desktop\projects\jb\docs\workflows\prompt_path_assignment_behavior_settlement_v0.md`

Patch execution: not authorized by this prompt. The JB CA may recommend exact
patch units only. Applying those patches requires a later explicit JB-local
execution turn.

## Problem Frame

Actor / trigger:

The owner observed an Orca prompt-authoring behavior defect: when asked for a
review prompt, the agent initially returned a paste-ready chat prompt instead
of choosing a durable prompt artifact path and the downstream review report
path. The owner noted JB may have the same issue.

Observed friction:

The owner should not have to name routine prompt, handoff, review, or report
paths. When a repo has established artifact folders, the agent should choose
deterministic input and output paths and state them in the prompt.

Why it matters:

If path ownership is ambiguous, downstream review, handoff, and patch threads
can become chat-only, non-durable, or misrouted. In JB, that risk is higher
because numbered GAP work already depends on per-gap prompt, review-input, and
review-output folders.

Desired outcome:

The JB CA should decide whether JB already has sufficient local authority for
agent-assigned prompt/report paths, whether it needs a workflow-overlay patch,
and what exact behavior should be adopted without importing Orca policy as JB
authority.

Constraints and non-goals:

- Do not treat Orca overlay text as JB authority.
- Do not edit JB files from this Orca-authored prompt.
- Do not install, edit, or shadow workflow skills.
- Do not make validation, readiness, lifecycle, deployment, install, resolver,
  push, merge, or review-pass claims.
- Do not collapse numbered GAP routing into flat legacy folders.

Decision this frame enables:

Whether JB should adopt a local rule that agents assign both the prompt input
artifact path and the downstream output artifact path by default, and where
that rule belongs in JB's repo-local authority.

Next eligible lane:

JB-local Chief Architect decision / workflow-overlay settlement.

## Paste-Ready JB CA Prompt

```markdown
# JB Chief Architect - Prompt Path Assignment Behavior Settlement

You are the Chief Architect for `jb` for this run.

Your job is to decide whether `jb` has the same prompt-authoring behavior
defect recently observed in Orca: agents may ask the owner for routine prompt
or report paths, or return chat-only prompts, when the repo should own
deterministic artifact routing.

Do not start by patching. Start by reconstructing the JB-local problem,
authority, current artifact routing rules, and the decision that must be made.

## Workspace Preflight

Workspace:
`C:\Users\vmon7\Desktop\projects\jb`

Expected prompt source:
This handoff prompt was authored from Orca at:
`C:\Users\vmon7\Desktop\projects\orca\docs\prompts\handoffs\jb_prompt_path_assignment_ca_settlement_prompt_v0.md`

Downstream output path to write:
`C:\Users\vmon7\Desktop\projects\jb\docs\workflows\prompt_path_assignment_behavior_settlement_v0.md`

Dirty state:
Allowed. Read current JB files in place. Do not treat unrelated dirty files as
authority. If a dirty source directly affects the prompt-path behavior decision,
name it in the settlement artifact.

Edit permission:
Write one JB-local settlement artifact only:
`docs/workflows/prompt_path_assignment_behavior_settlement_v0.md`

Do not patch `AGENTS.md`, `CLAUDE.md`, `docs/workflow-overlay.md`, prompts,
skills, generated artifacts, source files, tests, or GAP artifacts in this run.
If a source patch is needed, describe exact patch units only.

Output mode:
`file-write`.

If the settlement artifact cannot be written, return
`BLOCKED_JB_PROMPT_PATH_SETTLEMENT_WRITE` in chat with the intended path and the
best available summary. Do not pretend a durable settlement exists.

## JB Source Hierarchy

Use JB's own source hierarchy. Start with:

1. Current user instruction in this prompt.
2. `AGENTS.md`.
3. `CLAUDE.md`, if relevant to artifact/output discipline.
4. `docs/workflow-overlay.md`.
5. The latest dated handoff named by `docs/handoff/current_cv_engine_state.md`,
   if relevant.
6. `docs/workflows/gap_iteration_playbook.md`, if numbered GAP prompt/review
   routing is relevant.

Do not import Orca overlay rules as JB authority. Orca is only the observed
analog that exposed the possible behavior defect.

## Required Reads

Read these before deciding:

- `AGENTS.md`
- `docs/workflow-overlay.md`
- `CLAUDE.md`, if present
- `docs/handoff/current_cv_engine_state.md`, if present
- `docs/workflows/gap_iteration_playbook.md`, if present

Use targeted `rg` searches for these terms across `AGENTS.md`, `CLAUDE.md`,
`docs/workflow-overlay.md`, `docs/workflows/`, and `docs/prompts/`:

- `prompt`
- `review-output`
- `review report`
- `output path`
- `artifact`
- `handoff`
- `working/prompts`
- `working/review-outputs`
- `docs/prompts`
- `docs/review-outputs`
- `path`

Read only the additional files needed to decide whether the rule already
exists, is missing, conflicts with GAP routing, or needs a patch.

## Problem To Settle

The owner should not be responsible for naming routine prompt and report paths
when JB already has repo-local artifact folders and routing rules.

Decide whether JB should require agents to assign:

1. the prompt artifact path the downstream model, reviewer, CA, handoff agent,
   or patch agent should treat as the input prompt source; and
2. the downstream output artifact path the receiver should write when the
   output mode produces a durable prompt, review report, patch queue, handoff,
   workflow record, or GAP artifact.

The decision must handle both:

- numbered GAP artifacts, where paths usually belong under
  `docs/gaps/gap-NN/working/prompts/`,
  `docs/gaps/gap-NN/working/review-inputs/`, or
  `docs/gaps/gap-NN/working/review-outputs/`; and
- non-gap/shared/legacy artifacts, where flat paths such as `docs/prompts/`,
  `docs/review-inputs/`, and `docs/review-outputs/` may be valid.

## Decision Questions

Answer directly:

1. Does JB already bind the desired default behavior strongly enough?
2. If yes, where is it bound, and what wording should future agents follow?
3. If no, what exact local behavior should be added?
4. Where should that behavior live: `docs/workflow-overlay.md`,
   `AGENTS.md`, `CLAUDE.md`, `docs/workflows/gap_iteration_playbook.md`, a
   prompt template, or somewhere else?
5. How should the rule choose between numbered GAP paths and flat
   non-gap/shared paths?
6. Should agents choose a next version suffix automatically on collision, ask
   the user, or block?
7. Should reviewers and downstream agents be required to write the durable
   output path named by the prompt, and block visibly if they cannot?
8. What behavior should be forbidden, such as asking the owner for routine
   paths, returning chat-only prompts by default, or writing review value only
   in chat?
9. What exact patch units should a later executor apply, if any?

## Hard Boundaries

Do not patch files in this run.
Do not migrate old artifacts.
Do not edit numbered GAP artifacts.
Do not edit generated artifacts or compiler outputs.
Do not edit `.agents/skills/`, plugin caches, installed skills, workflow-run
artifacts, validation fixtures, deployment records, governance records, or
plugin metadata.
Do not claim validation success, readiness, lifecycle completion, formal
review pass, install/deploy/resolver status, push/merge safety, or publication.
Do not import Orca paths, folders, overlay authority, or artifact roles as JB
authority.

## Required Output Artifact

Write:

`docs/workflows/prompt_path_assignment_behavior_settlement_v0.md`

The artifact must include a retrieval header compatible with JB's retrieval
header boundary and these sections:

1. `Status And Decision`
   - Verdict: `ALREADY_BOUND`, `PATCH_RECOMMENDED`, `BLOCKED_NEEDS_AUTHORITY`,
     or `NO_CHANGE_RECOMMENDED`.
   - One-sentence decision.

2. `Problem Frame`
   - Actor / trigger.
   - Observed friction.
   - Why it matters in JB.
   - Desired behavior.

3. `JB Authority Read`
   - Sources read.
   - Current rules found.
   - Gaps or conflicts.

4. `Path Assignment Rule`
   - Recommended default prompt input path behavior.
   - Recommended downstream output path behavior.
   - Numbered GAP routing.
   - Non-gap/shared routing.
   - Collision/version behavior.
   - Blocking behavior.

5. `Patch Implications`
   - Exact conceptual patch units.
   - Target files.
   - What not to patch.

6. `Non-Claims`
   - No validation success.
   - No readiness.
   - No lifecycle completion.
   - No formal review pass.
   - No deployment/install/resolver/publication status.
   - No generated-artifact permission.
   - No patch execution.

7. `Exact Next Authorized Step`
   - One next move, such as a JB-local patch prompt or patch execution request.

## Chat Closeout

After writing the settlement artifact, return a compact human-readable summary
with:

- artifact path;
- artifact SHA256;
- verdict;
- whether a patch is recommended;
- exact next authorized step.

Do not paste the full artifact into chat unless the write fails.
```

## Validation Notes

Prompt validation expectations before use:

- JB workspace path is explicit.
- JB output artifact path is explicit.
- The prompt distinguishes Orca as observed analog from JB authority.
- The prompt asks the JB CA to use JB's own source hierarchy.
- The prompt assigns a downstream output path.
- Patch execution is out of scope.
- Numbered GAP and flat non-gap/shared artifact routes are both considered.
- Strict claims remain forbidden without JB-local authority and fresh evidence.
