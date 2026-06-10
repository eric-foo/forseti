# Orca File-Write Human Summary Behavior CA Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: Chief Architect prompt for resolving Orca file-write closeout behavior when large artifacts carry the detailed value but chat still needs a useful human summary.
use_when:
  - Asking a Chief Architect to decide how Orca prompts should close out substantial file-write artifacts.
  - Preparing a later prompt-structure or overlay patch route for human summary plus path/hash behavior.
  - Checking whether receipt-only file-write closeouts conflict with Orca chat-output topology.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/communication-style.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/validation-gates.md
  - docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
input_hashes:
  - path: .agents/workflow-overlay/communication-style.md
    sha256: 0D7F72216E2791EBB4E986EDF7766F00CF42BAE175B88CF51735ECF886895EEE
  - path: .agents/workflow-overlay/prompt-orchestration.md
    sha256: 9E159E3A7CC933083F56C95EBDDED4E19B2F51D55EE8EF774F3BEC62D566834F
  - path: .agents/workflow-overlay/validation-gates.md
    sha256: 4711210EEBD844C4FD22CBB2EE3B8C424B9BA5A8F1B99DFFF437D24B8156A470
  - path: .agents/workflow-overlay/template-registry.md
    sha256: 00A3E05FC7BC4BEE7DD8AE9ECD8B45C84FADB5581A4E301C45DBF4DC9F8A1CC8
  - path: docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md
    sha256: 1A193C7A813366384DB28F6F8C633E98E3B63CEE52E6954D7D0930C6518C04B5
  - path: docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md
    sha256: A6510BFF8951C7A2A01087133076C7933D1EF922735A6790237B05BBED503E74
  - path: docs/workflows/orca_major_move_folder_integrity_ca_discussion_v0.md
    sha256: 8EC6EA1652DE47DDD54BC232EB43896F93E5F738D7FDFFCB4C1ECB406A09F8EB
downstream_consumers:
  - Orca chat-output behavior Chief Architect discussion.
  - Future prompt-structure or overlay patch route, if accepted.
stale_if:
  - Orca chat-output topology changes.
  - File-write output-mode behavior changes.
  - Shared prompt behavior template changes.
  - Owner accepts or rejects a file-write closeout summary patch before this prompt is used.
```

## Prompt Status

Status: `PROMPT_ARTIFACT_V0`.

Template kind: `handoff`.

Target actor: Orca Chief Architect.

Output mode for downstream CA: `file-write`.

Downstream output path:
`docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`

Edit permission for downstream CA:
Write only the downstream discussion artifact. Do not patch overlay files,
templates, prompts, product docs, review reports, or workflow artifacts other
than the required discussion output.

## Why This Prompt Exists

The immediate failure mode was a file-write closeout for
`docs/workflows/orca_major_move_folder_integrity_ca_discussion_v0.md`.

The closeout reported the artifact path, SHA256, recommendation, patch
implication, and next step, but did not summarize enough of the artifact for
the owner to understand the major decision without opening a large file.

The owner pushed back:

> wait... according to behaviorals werent u supposed to summarise so i can at least understand a huge material portion of this

Then clarified:

> first we'll need to change behaviorals (probaly prompt structure) to reflect this. i thought we already had the yaml thing and human summary. prompt up a new CA

This CA pass should treat that as a real behavioral gap, not a cosmetic
preference. If the owner's "YAML thing" framing is not the best fix, say so
directly and recommend the correct output contract.

## Paste-Ready CA Prompt

```markdown
# Orca Chief Architect - File-Write Human Summary Behavior

You are the Orca Chief Architect for this run.

Your job is to decide how Orca should change prompt behaviorals, prompt
structure, or overlay output rules so substantial `file-write` outputs do not
close with a receipt-only chat response when the owner needs a usable summary
of the material decision.

Do not start by writing a patch. Start by reconstructing the behavioral
collision:

- Orca's general chat topology says human summary first, agent-readable detail
  second, compact courier YAML last when useful or required.
- Orca's `file-write` output-mode exception allows compact path/hash/status
  receipts when the durable artifact carries the human-readable value.
- In the major-move folder-integrity run, that exception was applied too
  narrowly: the chat receipt carried path/hash/recommendation, but not enough
  decision substance for the owner to understand the artifact without opening
  it.

The decision is not "always paste the full artifact into chat." The decision is
what minimum useful human summary belongs in chat after substantial
decision-bearing `file-write` artifacts, while preserving source-heavy economy,
artifact-local detail, review-report exceptions, and compact courier state.

## Workspace Preflight

Workspace:
`C:\Users\vmon7\Desktop\projects\orca`

Expected prompt source:
`docs/prompts/handoffs/orca_file_write_human_summary_behavior_ca_prompt_v0.md`

Expected branch at prompt creation:
`main`

Expected commit at prompt creation:
`a873c9c3ed3b289a65f9c472c63e0aadf880a127`

Dirty state:
Allowed. Read the current Orca overlay and docs in place. Modified and
untracked Orca docs may be relevant because the overlay is currently evolving.
Do not treat unrelated dirty files as authority.

Downstream output path:
`docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`

Edit permission:
`docs-write` for one workflow discussion artifact only:
`docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`

Do not patch `.agents/workflow-overlay/`, `docs/prompts/templates/`, prompt
files, product docs, review reports, workflow records other than the one
required output, skills, workflow-kernel source, or installed/plugin/user
skills. Do not commit, push, or open PRs.

If the discussion artifact cannot be written, return
`BLOCKED_FILE_WRITE_SUMMARY_DISCUSSION_WRITE` in chat with the intended path
and the best available summary. Do not pretend a durable discussion artifact
exists.

## Source Hierarchy

Use this source hierarchy:

1. Explicit user instruction in this prompt.
2. Orca `AGENTS.md`.
3. `.agents/workflow-overlay/`.
4. Orca docs under `docs/`, when they do not conflict with overlay.
5. Reusable workflow guidance only for generic mechanics, never Orca facts.

If reusable guidance conflicts with Orca overlay for Orca facts, the overlay
wins. Do not import `jb` rules, folder habits, lifecycle mechanics, GAP
policy, validation habits, or prompt templates as Orca authority.

## Required Reads

Read these before deciding:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/communication-style.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/template-registry.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`
- `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`
- `docs/workflows/orca_major_move_folder_integrity_ca_discussion_v0.md`

Use targeted `rg` searches over `.agents/workflow-overlay/` and `docs/prompts/`
for:

- `human summary`
- `human-readable`
- `agent-readable`
- `courier YAML`
- `file-write`
- `review-report`
- `paste-ready-chat`
- `path/hash`
- `receipt`
- `Do not paste the full artifact`
- `Chat Closeout`
- `compact`
- `summary`

Read additional prompt templates or active prompts only when they materially
change the recommended patch route.

## Pinned Source Hashes

If a hash mismatch appears for a pinned source, report it in the artifact and
decide whether it blocks the run. Do not substitute another source for a
mismatched controlling source.

- `.agents/workflow-overlay/communication-style.md`:
  `0D7F72216E2791EBB4E986EDF7766F00CF42BAE175B88CF51735ECF886895EEE`
- `.agents/workflow-overlay/prompt-orchestration.md`:
  `9E159E3A7CC933083F56C95EBDDED4E19B2F51D55EE8EF774F3BEC62D566834F`
- `.agents/workflow-overlay/validation-gates.md`:
  `4711210EEBD844C4FD22CBB2EE3B8C424B9BA5A8F1B99DFFF437D24B8156A470`
- `.agents/workflow-overlay/template-registry.md`:
  `00A3E05FC7BC4BEE7DD8AE9ECD8B45C84FADB5581A4E301C45DBF4DC9F8A1CC8`
- `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`:
  `1A193C7A813366384DB28F6F8C633E98E3B63CEE52E6954D7D0930C6518C04B5`
- `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`:
  `A6510BFF8951C7A2A01087133076C7933D1EF922735A6790237B05BBED503E74`
- `docs/workflows/orca_major_move_folder_integrity_ca_discussion_v0.md`:
  `8EC6EA1652DE47DDD54BC232EB43896F93E5F738D7FDFFCB4C1ECB406A09F8EB`

## Problem To Decide

The current rules contain a real ambiguity:

- `communication-style.md` says decision-bearing Orca chat should lead with a
  human summary, then agent-readable detail, then compact courier YAML when
  useful or required.
- `prompt-orchestration.md` says `file-write` may return compact path/hash/status
  receipts after the durable artifact is written when the artifact carries the
  human-readable value.
- Individual prompts can say "Do not paste the full artifact into chat unless
  the write fails," which is correct, but can accidentally steer the closeout
  toward a receipt-only answer.

The owner expected the behavioral contract to produce both a usable human
summary and routable state. The actual closeout included state, but not enough
human summary.

Your task is to decide the smallest durable fix:

- Should the overlay clarify `file-write` closeouts?
- Should prompt templates include a stronger `Chat Closeout` contract?
- Should existing handoff prompts be patched when they ask for substantial
  decision-bearing artifacts?
- Should courier YAML be used for file-write closeouts, or is human prose plus
  path/hash enough?
- What exception boundaries must remain intact for `review-report`,
  `paste-ready-chat`, source-heavy evidence units, and artifact-native tables?

Push back if the best answer is not "add YAML everywhere." The problem is
under-summarized decision-bearing closeout, not YAML absence by itself.

## Options To Compare

Compare at least these options:

1. No patch: rely on existing `communication-style.md` and treat the prior
   closeout as agent error.
2. Patch only `prompt-orchestration.md` to clarify that substantial
   decision-bearing `file-write` outputs require a material human summary
   before path/hash receipts.
3. Patch only `communication-style.md` to sharpen the human-summary rule for
   post-artifact closeouts.
4. Patch the shared prompt behavior contract so future templates inherit a
   closeout rule.
5. Patch individual active prompts that have a weak "do not paste full artifact"
   closeout instruction.
6. Hybrid route: patch overlay output-mode rules plus shared prompt behavior,
   then selectively patch active prompts/templates that generate substantial
   `file-write` CA artifacts.

You may add another option if current Orca sources support it.

## Decision Criteria

Evaluate options against:

- owner comprehension without opening a large artifact;
- preserving artifact-local detail and source-heavy economy;
- avoiding full artifact pasteback;
- preserving `review-report` YAML-only saved-report exception;
- preserving `paste-ready-chat` prompt-body behavior;
- avoiding ritual YAML or extra keys that do not improve routing;
- keeping prompt closeouts short but substantive;
- preventing future CA prompts from specifying receipt-only closeouts;
- compatibility with existing prompt validation gates;
- minimal patch surface;
- no broad patching of stale one-off prompts unless the prompt is active and
  likely to be reused;
- no validation, approval, readiness, lifecycle, install, deploy, resolver,
  merge-safety, product-readiness, or implementation-readiness claim.

## Hard Boundaries

Do not patch files in this CA pass.
Do not create a patch queue that claims execution authority.
Do not edit overlay, template, prompt, product, review, or workflow files other
than the one required discussion artifact.
Do not broad-sync stale prompts.
Do not add YAML-only chat for `file-write` decision closeouts unless you can
defend why human prose would not satisfy the owner need.
Do not weaken `review-report` rules where YAML-only chat is valid only after a
durable report write or explicit/blocking exception.
Do not use retrieval metadata as validation proof, approval, readiness,
lifecycle completion, deployment/install/resolver status, edit permission, or
source-of-truth promotion.
Do not create implementation folders, automation, source systems, packages,
tests, dashboards, skills, commits, pushes, or PRs.

## Required Output Artifact

Write:

`docs/workflows/orca_file_write_human_summary_behavior_ca_discussion_v0.md`

The artifact must include retrieval metadata and these sections:

1. `Status And Recommendation`
   - Use one of:
     - `NO_PATCH_NEEDED_AGENT_ERROR`
     - `PROMPT_ORCHESTRATION_PATCH_RECOMMENDED`
     - `COMMUNICATION_STYLE_PATCH_RECOMMENDED`
     - `SHARED_BEHAVIOR_TEMPLATE_PATCH_RECOMMENDED`
     - `HYBRID_PATCH_ROUTE_RECOMMENDED`
     - `BLOCKED_NEEDS_OWNER_DECISION`
   - One-sentence recommendation.

2. `Problem Frame`
   - Triggering incident.
   - What the owner expected.
   - What the existing rules already say.
   - Where the ambiguity or failure mode lives.

3. `Current Contract Map`
   - `communication-style.md`.
   - `prompt-orchestration.md`.
   - `validation-gates.md`.
   - shared prompt behavior contract.
   - relevant active prompt closeout language.

4. `Options Compared`
   - Compare the options above against the decision criteria.

5. `Recommended Closeout Contract`
   - Minimum human summary requirement for substantial decision-bearing
     `file-write` artifacts.
   - Path/hash/status receipt requirement.
   - Whether courier YAML is required, optional, or discouraged for this case.
   - How much detail is enough.
   - What should stay in the artifact only.

6. `Patch Implications`
   - Whether `.agents/workflow-overlay/communication-style.md` needs a later
     patch.
   - Whether `.agents/workflow-overlay/prompt-orchestration.md` needs a later
     patch.
   - Whether `.agents/workflow-overlay/validation-gates.md` needs a later
     patch.
   - Whether `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md`
     needs a later patch.
   - Whether active prompt artifacts, including
     `docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`,
     need later targeted patches.
   - Conceptual patch units only.

7. `Prompt Structure Guidance`
   - A recommended `Chat Closeout` clause for future substantial `file-write`
     CA prompts.
   - A bad closeout example to avoid.
   - A good closeout shape that is concise but decision-useful.

8. `Risks And Non-Claims`
   - Overlong chat risk.
   - Receipt-only risk.
   - YAML ritual risk.
   - Review-report exception risk.
   - Source-heavy readback risk.
   - No patch acceptance claim.
   - No validation/readiness claim.

9. `Exact Next Authorized Step`
   - One next move.

## Chat Closeout

After writing the artifact, return a compact but substantive human-readable
summary. Do not return a receipt-only closeout.

The closeout must include:

- the recommendation in plain language;
- the behavioral gap and why the fix matters;
- the recommended patch surface;
- what should not change;
- artifact path and SHA256;
- exact next authorized step.

Do not paste the full artifact into chat unless the write fails.
```

## Validation Notes

Prompt validation expectations before use:

- Overlay authority loaded.
- Prompt input path is explicit.
- Downstream output path is explicit.
- Output mode is `file-write`.
- Edit permission is one workflow discussion artifact only.
- The CA is asked to compare behavioral patch routes rather than assume YAML is the fix.
- The prompt preserves `review-report`, `paste-ready-chat`, source-heavy economy, and artifact-native table exceptions.
- Overlay patching, template patching, prompt patching, skill work, implementation, commits, pushes, and PRs are out of scope for the downstream CA pass.
