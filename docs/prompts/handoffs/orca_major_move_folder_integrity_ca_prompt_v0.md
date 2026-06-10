# Orca Major Move Folder Integrity CA Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: Chief Architect prompt for evaluating whether Orca should introduce major-move folders or another long-term folder integrity pattern.
use_when:
  - Asking a Chief Architect to reason about durable folder topology for major Orca workstreams.
  - Deciding whether ICP, commercial frame, proof, and similar moves need dedicated folders.
  - Preparing a later overlay patch route for artifact-folder rules.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/artifact-folders.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/retrieval-metadata.md
input_hashes:
  - path: .agents/workflow-overlay/artifact-folders.md
    sha256: 53CD58EEE4F22A778A7235F969CE73334EBAAB7D0DC9BF9408B0F7D4FEFB3589
  - path: .agents/workflow-overlay/prompt-orchestration.md
    sha256: 54242C83D83FBA3775738276C0D87F0C1F172849024E6F341D1E61D0851AA049
  - path: .agents/workflow-overlay/retrieval-metadata.md
    sha256: ECE14148E415EF5C9E3E89FD5ACC47DEADDC84B9A4F653FBF1F455AD3C0B90DE
downstream_consumers:
  - Orca folder-integrity Chief Architect discussion.
  - Future artifact-folder overlay patch route, if accepted.
stale_if:
  - Accepted artifact folders change.
  - Prompt path-assignment behavior changes.
  - Owner accepts or rejects major-move folders before this prompt is used.
```

## Prompt Status

Status: `PROMPT_ARTIFACT_V0`.

Template kind: `handoff`.

Target actor: Orca Chief Architect.

Output mode for downstream CA: `file-write`.

Downstream output path:
`docs/workflows/orca_major_move_folder_integrity_ca_discussion_v0.md`

Edit permission for downstream CA:
Write only the downstream discussion artifact. Do not patch overlay files,
move artifacts, create folders, or migrate existing documents in the CA pass.

## Paste-Ready CA Prompt

```markdown
# Orca Chief Architect - Major Move Folder Integrity Discussion

You are the Orca Chief Architect for this run.

Your job is to decide whether Orca should introduce dedicated folders for
major moves, or whether a broader folder-integrity pattern is better for the
long term.

The triggering example is the current ICP / first-wedge work. The owner asked
whether every major move should get its own folder, for example an `ICP` folder,
or whether the folder should be broader than that.

Do not start by proposing a folder name. Start by reconstructing the folder
integrity problem, the current Orca artifact model, and what decision the
folder topology needs to support.

## Workspace Preflight

Workspace:
`C:\Users\vmon7\Desktop\projects\orca`

Expected prompt source:
`docs/prompts/handoffs/orca_major_move_folder_integrity_ca_prompt_v0.md`

Downstream output path:
`docs/workflows/orca_major_move_folder_integrity_ca_discussion_v0.md`

Dirty state:
Allowed. Read the current Orca overlay and docs in place. Do not treat
unrelated dirty files as authority.

Edit permission:
`docs-write` for one workflow discussion artifact only:
`docs/workflows/orca_major_move_folder_integrity_ca_discussion_v0.md`

Do not patch `.agents/workflow-overlay/`, move files, create folders, rename
artifacts, migrate docs, edit prompt files, edit product docs, create skills,
install skills, commit, push, or open PRs.

If the discussion artifact cannot be written, return
`BLOCKED_FOLDER_INTEGRITY_DISCUSSION_WRITE` in chat with the intended path and
the best available summary. Do not pretend a durable discussion artifact
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
policy, or templates as Orca authority.

## Required Reads

Read these before deciding:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/source-of-truth.md`

Use targeted `rg` searches over `docs/` and `.agents/workflow-overlay/` for:

- `ICP`
- `first wedge`
- `commercial frame`
- `proof`
- `major move`
- `folder`
- `artifact`
- `workflow`
- `decision`
- `review`
- `prompt`

Read additional files only when they materially change the folder-integrity
recommendation.

## Problem To Discuss

Orca has growing clusters of related work: ICP / first wedge, product proof,
commercial frame, review prompts, adversarial reviews, patch routes, and
future product or proof decisions.

Today, artifacts are mostly organized by artifact type:

- prompts under `docs/prompts/...`;
- review reports under `docs/review-outputs/...`;
- product artifacts under `docs/product/`;
- workflow records under `docs/workflows/`;
- decisions under `docs/decisions/`;
- overlay authority under `.agents/workflow-overlay/`.

The owner is considering an alternate or additional pattern:

> Every major move could get its own folder, for example an ICP folder.

Your job is to evaluate whether this would improve long-term retrieval,
reviewability, source loading, and lifecycle clarity, or whether it would
fragment Orca's artifact-role discipline.

## Options To Compare

Compare at least these options:

1. Keep the current artifact-type folder model unchanged.
2. Create dedicated folders by major move, such as `docs/moves/icp/` or
   `docs/product/icp/`.
3. Create broader workstream folders, such as `docs/product/first-proof/`,
   `docs/product/market-selection/`, or `docs/workflows/major-moves/`.
4. Use lightweight index/router artifacts instead of new folders, such as a
   major-move index that points to prompts, product docs, reviews, and patch
   routes across existing folders.
5. Hybrid: keep artifact-type folders as canonical destinations, but add
   per-major-move indexes or manifests that create retrieval cohesion without
   moving artifacts.

You may add other options if current Orca sources support them.

## Decision Criteria

Evaluate options against:

- long-term retrieval clarity;
- artifact-role integrity;
- avoiding duplicated source-of-truth paths;
- low context-loading cost for future agents;
- ability to see all artifacts for one major move;
- prompt and review path determinism;
- review-output routing clarity;
- compatibility with retrieval headers;
- ease of future hygiene and migration;
- resistance to folder sprawl;
- resistance to overly generic buckets;
- ability to support major moves beyond ICP, such as commercial frame,
  product proof, customer discovery, source standards, and feature planning;
- whether the pattern should live in `.agents/workflow-overlay/artifact-folders.md`,
  `docs/STRUCTURE.md`, a workflow index, or another source.

## Hard Boundaries

Do not patch overlay files.
Do not create new folders.
Do not move or rename artifacts.
Do not migrate existing docs.
Do not edit prompt, product, decision, review, or workflow artifacts other than
the one required discussion output.
Do not create implementation folders, packages, tests, automation, source
systems, dashboards, or skills.
Do not claim validation, readiness, lifecycle completion, source-of-truth
promotion, folder acceptance, or migration completion.

## Required Output Artifact

Write:

`docs/workflows/orca_major_move_folder_integrity_ca_discussion_v0.md`

The artifact must include retrieval metadata and these sections:

1. `Status And Recommendation`
   - Use one of:
     - `KEEP_CURRENT_MODEL`
     - `MAJOR_MOVE_FOLDERS_RECOMMENDED`
     - `WORKSTREAM_FOLDERS_RECOMMENDED`
     - `INDEX_MANIFEST_HYBRID_RECOMMENDED`
     - `BLOCKED_NEEDS_OWNER_DECISION`
   - One-sentence recommendation.

2. `Problem Frame`
   - Trigger.
   - Observed risk.
   - Why it matters.
   - Desired folder-integrity outcome.

3. `Current Folder Model`
   - Current accepted folders.
   - What works.
   - What is starting to strain.

4. `Options Compared`
   - Compare the options above against the decision criteria.

5. `Recommended Pattern`
   - Naming pattern.
   - Which artifacts remain in artifact-type folders.
   - Whether indexes/manifests are needed.
   - Whether any new folder class is justified.
   - What should happen for the ICP / first-wedge work specifically.

6. `Patch Implications`
   - Whether `.agents/workflow-overlay/artifact-folders.md` needs a later
     patch.
   - Whether `docs/STRUCTURE.md` or a workflow index needs a later patch.
   - Conceptual patch units only.

7. `Risks And Non-Claims`
   - Folder sprawl risk.
   - Duplicate authority risk.
   - Migration risk.
   - No folder acceptance claim.
   - No migration completion claim.
   - No validation/readiness claim.

8. `Exact Next Authorized Step`
   - One next move.

## Chat Closeout

After writing the artifact, return a compact headed human-readable closeout.
Do not return a receipt-only response.

Include:

- the recommendation in plain language;
- the material decision facts needed to understand the result without opening
  the artifact;
- the main tradeoff, blocker, or deferred item if it changes the next move;
- what should not change or what remains out of scope;
- artifact path and SHA256;
- exact next authorized step;
- compact courier YAML when lane switching, handoff routing, or another agent
  or thread is expected to continue from this result and compact courier YAML
  would materially benefit that routing.

Do not paste the full artifact into chat unless the write fails.
```

## Validation Notes

Prompt validation expectations before use:

- Overlay authority loaded.
- Prompt input path is explicit.
- Downstream output path is explicit.
- Output mode is `file-write`.
- Edit permission is one workflow artifact only.
- The CA is asked to compare folder models rather than assume major-move
  folders are correct.
- Overlay patching, folder creation, migration, and implementation are out of
  scope.
