# Skill Adoption

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Orca workflow skill recognition, adoption rules, source/deployment boundaries, and collision checks.
use_when:
  - Deciding whether Orca may use or adopt workflow skills.
  - Checking resolver-visible skill evidence and skill-name collisions.
  - Preventing installed, user-level, plugin, or external skill source mutation from ordinary Orca work.
authority_boundary: retrieval_only
```

## Current Status

- Orca has no local reusable workflow skill source.
- Orca has no accepted Orca-local candidate skills.
- Orca has no accepted global skill shadow candidates.
- Orca has no same-name global skill promotions.
- Orca may use resolver-visible workflow skills when explicitly invoked or
  selected by the active resolver. This does not make external workflow source
  documents Orca authority.
- This recognition record does not install, update, validate, promote, or
  activate plugin skills. The current running thread may still expose an older
  skill registry until Codex reloads plugin metadata.
- Future reusable workflow skill adoption requires accepted skill source and
  validated deployment copies.

## Recognized Workflow Skills

These skills may provide task-local mechanics for Orca work. They do not
provide Orca project authority, product facts, artifact destinations,
validation gates, acceptance, readiness, resolver behavior, deployment status,
or implementation permission.

Observed on 2026-05-26:

- Marketplace source configured in `C:\Users\vmon7\.codex\config.toml`:
  `C:\Users\vmon7\Desktop\projects\agent-workflow`.
- Source repo HEAD observed: `fe95dd6`; source worktree was dirty. Treat this
  as source-location evidence only, not clean-source acceptance.
- Source plugin manifest observed:
  `C:\Users\vmon7\Desktop\projects\agent-workflow\plugin\.codex-plugin\plugin.json`.
- Installed plugin cache observed:
  `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.19`.
- Installed package manifest observed:
  `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.19\skill_manifest_v1.json`.
- Installed plugin version observed: `0.1.19`.
- Package manifest `observed_repo_head_at_manifest_update`: `fe95dd6`; use the
  manifest's per-skill hashes for provenance, not this overlay file.
- Package-path readback: every `plugin/skills/*/SKILL.md` path listed in the
  `0.1.19` package manifest existed at readback.
- The deleted implementation-gate workflow is absent from the `0.1.19` package
  manifest and is not a recognized Orca workflow tool.
- Previous recognized `workflow-compound-planning` entry from plugin cache
  `0.1.3` is stale; use `incremental-planning` for next-move sequencing.

## Recognized Workflow Tools

| Skill | Advisory use in Orca | Collision status observed 2026-05-24 |
| --- | --- | --- |
| `incremental-planning` | Next-move sequencing: decide which product, proof, foundation, review, or planning move compounds most from the visible state. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `meta-planning` | Upstream framing: detect when a request starts below the right decision layer and name the missing decision or operating contract. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-adversarial-artifact-review` | Source-backed adversarial review of non-code artifacts. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-architecture-planning` | Target-architecture planning before feature or implementation scoping. | No Orca-local or user-level same-name collision observed. |
| `workflow-before-after-lens` | Explicit before/after comparison of an original frame against a proposed or actual output, with drift and acceptance-risk surfacing. | No Orca-local or user-level same-name collision observed. |
| `workflow-branch-completion-report` | Chat-first report for a completed branch or work unit. | No Orca-local or user-level same-name collision observed. |
| `workflow-cartographer` | Goal-bound route mapping from a stated goal to a starting point and first move. | No Orca-local or user-level same-name collision observed. |
| `workflow-code-review` | Implementation/code review focused on bugs, regressions, risks, and missing tests. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-deep-thinking` | Deeper reasoning for explicitly requested analysis or workflow skill source behavior. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-feature-ultraplan` | Planning-only feature exploration before implementation scoping. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-goal-framing` | Compact goal framing across long-term goal, pillar goal, near-term outcome, and success signal. | No Orca-local or user-level same-name collision observed. |
| `workflow-health-check` | Advisory repository/workflow health checks for structure, source boundaries, stale indexes, and drift signals. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-implementation-scoping` | Non-executing implementation route for an accepted plan. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-postmortem-review` | Postmortem review of workflow skill behavior or specifically bound postmortem targets. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-precompact` | Manual precompact working packet mechanics when explicitly invoked. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-problem-framing` | Problem framing before product planning, feature planning, prompt orchestration, scoping, review, or execution. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-product-ultraplan` | Planning-only product-direction, product-proof, and product-bet exploration. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-prompt-orchestrator` | Prompt, wrapper, handoff, rerun, patch, and review-prompt orchestration. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-reorient` | Operator-facing state reorientation after handoffs, reviews, compaction, or parallel work. | No Orca-local or user-level same-name collision observed. |
| `workflow-repo-context` | Compact repository context packets and advisory routing recommendations. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |

For strict provenance, open the installed `0.1.19` `skill_manifest_v1.json` and
the relevant `SKILL.md` before relying on any skill behavior. This overlay table
is an Orca routing and collision record, not package validation or resolver
proof.

## Activation Caveat

This Orca overlay records that `0.1.19` exists in the installed plugin cache.
It cannot force the current Codex thread to reload the active skill registry.
If the visible skill list for a running thread still points at plugin cache
`0.1.18`, start a fresh thread or reload Codex before expecting automatic
triggering or absence decisions to reflect `0.1.19`. Until then, manual source
loading from the `0.1.19` cache may be used only with an
explicit disclosure that active resolver behavior was not proven in-thread.

## Adoption Rules

- Orca-local candidate skills may be created and iterated only after explicit
  owner authorization for that named candidate.
- Candidate skills must stay Orca-local until a separate promotion decision.
- Candidate skills are not Orca authority. They must defer Orca facts,
  artifact roles, review lanes, output modes, validation gates, and safety
  rules to `AGENTS.md` and `.agents/workflow-overlay/`.
- Candidate skills must record trigger examples, source boundary, collision
  status, rollback path, and validation notes before acceptance.
- Use shadow names before any same-name promotion.
- Re-check repo-local, installed global/system, user-level, plugin-contributed,
  and other resolver-visible skill names before adoption work.
- Record source path, source hash, overlay loaded, collision status, and
  rollback path for any adoption validation.
- Missing overlay authority must fail visibly when a reusable skill requires
  project facts.

## Protected Skill Boundary

Do not install, uninstall, rename, rewrite, shadow, or promote global,
user-level, plugin-contributed, installed, or external source skills from
ordinary Orca product work.

Those actions require a separate explicit skill-governance authorization after
resolver-visible collision checks and rollback planning. The Orca-local
candidate lane above does not grant that authority.

## Rollback

Rollback for this overlay recognition update is to remove the `0.1.19`
recognition sections and restore the prior recognized-skill record from Git or
human-approved notes. Rollback must not edit plugin source, installed plugin
cache files, global/user skill roots, or external workflow source.

## Known Snapshots

- The Turn 6 resolver-visible skill snapshot is recorded in
  `docs/workflows/orca_bootstrap_record.md`.
- The 2026-05-24 collision check observed no Orca-local `.agents/skills`
  directory, system skills `imagegen`, `openai-docs`, `plugin-creator`,
  `skill-creator`, and `skill-installer`, user-level skill collisions listed
  above, and user-level `pre-compact-checkpoint` under
  `C:\Users\vmon7\.agents\skills`.
