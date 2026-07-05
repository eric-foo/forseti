# Skill Adoption

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Forseti workflow skill recognition, adoption rules, source/deployment boundaries, and collision checks.
use_when:
  - Deciding whether Forseti may use or adopt workflow skills.
  - Checking resolver-visible skill evidence and skill-name collisions.
  - Preventing installed, user-level, plugin, or external skill source mutation from ordinary Forseti work.
authority_boundary: retrieval_only
```

## Current Status

- Forseti has one accepted Forseti-local primary workflow skill source:
  `forseti-product-lead` (accepted/frozen as the primary product-lead skill ID
  on 2026-07-05; DEPLOYED/ACTIVATED for the Claude Code runtime,
  project-scoped — not user-global). See `## Accepted Forseti-Local Candidate
  Skills` below.
- Forseti retains `orca-product-lead` as a legacy compatibility wrapper for one
  transition window. It is an alias into `forseti-product-lead`, not the primary
  skill identity.
- Forseti has no accepted global skill shadow candidates.
- Forseti has no same-name global skill promotions.
- Forseti may use resolver-visible workflow skills when explicitly invoked or
  selected by the active resolver. This does not make external workflow source
  documents Forseti authority.
- This recognition record does not install, update, validate, promote, or
  activate plugin skills. The current running thread may still expose an older
  skill registry until Codex reloads plugin metadata.
- Future reusable workflow skill adoption requires accepted skill source and
  validated deployment copies.

## Recognized Workflow Skills

These skills may provide task-local mechanics for Forseti work. They do not
provide Forseti project authority, product facts, artifact destinations,
validation gates, acceptance, readiness, resolver behavior, deployment status,
or implementation permission.

Observed on 2026-06-05:

- Marketplace source configured in `C:\Users\vmon7\.codex\config.toml`:
  `C:\Users\vmon7\Desktop\projects\agent-workflow`.
- Source repo HEAD observed: `b78c268`; source worktree was dirty. Treat this
  as source-location evidence only, not clean-source acceptance.
- Source plugin manifest observed:
  `C:\Users\vmon7\Desktop\projects\agent-workflow\plugin\.codex-plugin\plugin.json`.
- Installed plugin cache observed:
  `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.52`.
- Installed package manifest observed:
  `C:\Users\vmon7\.codex\plugins\cache\agent-workflow-local\agent-workflow\0.1.52\skill_manifest_v1.json`.
- Installed plugin version observed: `0.1.52`.
- Package manifest `observed_repo_head_at_manifest_update`: `6c22334`; use the
  manifest's per-skill hashes for provenance, not this overlay file.
- Package-path readback: every `plugin/skills/*/SKILL.md` path listed in the
  `0.1.52` package manifest existed at readback.
- The deleted implementation-gate workflow is absent from the `0.1.52` package
  manifest and is not a recognized Forseti workflow tool.
- Previous recognized `workflow-compound-planning` entry from plugin cache
  `0.1.3` is stale; use `incremental-planning` for next-move sequencing.
- `workflow-cartographer` is present in the installed plugin package and in the
  active resolver-visible skill list for the current Codex thread. It is not
  present under `C:\Users\vmon7\.codex\skills`, which is an older user-level
  shadow surface and must not be treated as the Agent Workflow plugin inventory.

## Recognized Workflow Tools

| Skill | Advisory use in Forseti | Collision status observed 2026-06-05 |
| --- | --- | --- |
| `fused` | Explicit fused implementation turn: scoping, spec writing, micro-decision locking, then bounded implementation. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `incremental-planning` | Next-move sequencing: decide which product, proof, foundation, review, or planning move compounds most from the visible state. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `meta-planning` | Upstream framing: detect when a request starts below the right decision layer and name the missing decision or operating contract. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `micro-decision-locking` | Pre-implementation locking of the few route-critical decisions needed before a bounded source edit. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-adversarial-artifact-review` | Source-backed adversarial review of non-code artifacts. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-architecture-planning` | Target-architecture planning before feature or implementation scoping. | No Forseti-local or user-level same-name collision observed. |
| `workflow-before-after-lens` | Explicit before/after comparison of an original frame against a proposed or actual output, with drift and acceptance-risk surfacing. | No Forseti-local or user-level same-name collision observed. |
| `workflow-branch-completion-report` | Chat-first report for a completed branch or work unit. | No Forseti-local or user-level same-name collision observed. |
| `workflow-cartographer` | Goal-bound route mapping from a stated goal to a starting point and first move. | No Forseti-local or user-level same-name collision observed. |
| `workflow-code-review` | Implementation/code review focused on bugs, regressions, risks, and missing tests. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-deep-thinking` | Deeper reasoning for explicitly requested analysis or workflow skill source behavior. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-delegated-review-patch` | Commissioning and adjudicating a bounded de-correlated review-and-patch hardening pass. | No Forseti-local or user-level same-name collision observed. |
| `workflow-feature-ultraplan` | Planning-only feature exploration before implementation scoping. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-goal-framing` | Compact goal framing across long-term goal, pillar goal, near-term outcome, and success signal. | No Forseti-local or user-level same-name collision observed. |
| `workflow-handoff` | Cold cross-lane handoff packet for a fresh agent, thread, worktree, or session. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-health-check` | Advisory repository/workflow health checks for structure, source boundaries, stale indexes, and drift signals. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-humanise` | Plain-language re-encoding of dense content for a named human reader while preserving facts, uncertainty, and stakes. | No Forseti-local or user-level same-name collision observed. |
| `workflow-implementation-scoping` | Non-executing implementation route for an accepted plan. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-postmortem-review` | Postmortem review of workflow skill behavior or specifically bound postmortem targets. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-precompact` | Manual precompact working packet mechanics when explicitly invoked. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-problem-framing` | Problem framing before product planning, feature planning, prompt orchestration, scoping, review, or execution. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-product-ultraplan` | Planning-only product-direction, product-proof, and product-bet exploration. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-prompt-orchestrator` | Prompt, wrapper, handoff, rerun, patch, and review-prompt orchestration. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-reorient` | Operator-facing state reorientation after handoffs, reviews, compaction, or parallel work. | No Forseti-local or user-level same-name collision observed. |
| `workflow-repo-context` | Compact repository context packets and advisory routing recommendations. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-repo-hygiene` | Repository hygiene closeout after completed work, before handoff, or before branch/worktree cleanup. | No Forseti-local or user-level same-name collision observed. |
| `workflow-skill-authoring-discipline` | Discipline for creating, editing, reviewing, or promoting reusable workflow skills. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |
| `workflow-spec-writing` | Thin binding-actor spec writing before scoping when downstream actors would otherwise invent intent. | Same-name user-level skill exists under `C:\Users\vmon7\.codex\skills`; recheck resolver behavior before strict adoption. |

For strict provenance, open the installed `0.1.52` `skill_manifest_v1.json` and
the relevant `SKILL.md` before relying on any skill behavior. This overlay table
is a Forseti routing and collision record, not package validation or resolver
proof.

## Activation Caveat

A recognition record here reflects the plugin-cache state observed when it was
written; a running thread may still resolve against an older cache. If the
visible skill list looks stale, start a fresh thread or reload before relying on
automatic triggering or absence decisions, and disclose when active resolver
behavior was not proven in-thread.

## Adoption Rules

- Forseti-local candidate skills may be created and iterated only after explicit
  owner authorization for that named candidate.
- Candidate skills must stay Forseti-local until a separate promotion decision.
- Candidate skills are not Forseti authority. They must defer Forseti facts,
  artifact roles, review lanes, output modes, validation gates, and safety
  rules to `AGENTS.md` and `.agents/workflow-overlay/`.
- Candidate skills must record trigger examples, source boundary, collision
  status, rollback path, and validation notes before acceptance.
- Accept a Forseti-local candidate as frozen only when it is specific and narrowly
  scoped to a real Forseti lane (like `forseti-product-lead`), defers all Forseti facts to
  `AGENTS.md` and `.agents/workflow-overlay/`, carries the adoption metadata
  above, and has a re-confirmed collision check plus a pinned source hash. Do not
  accept broad, generic, or authority-claiming local skills. Acceptance is a
  local freeze only; it does not deploy, activate, or make the skill
  resolver-visible — that remains a separate Protected Skill Boundary action.
- Use shadow names before any same-name promotion.
- Re-check repo-local, installed global/system, user-level, plugin-contributed,
  and other resolver-visible skill names before adoption work.
- Record source path, source hash, overlay loaded, collision status, and
  rollback path for any adoption validation.
- Missing overlay authority must fail visibly when a reusable skill requires
  project facts.

## Accepted Forseti-Local Candidate Skills

Forseti does accept Forseti-local candidate skills, but only specific, narrowly scoped
ones like the product-lead method below — never broad, generic, or
authority-claiming local skills. Acceptance is a LOCAL FREEZE only: it does not
deploy, activate, or make the skill resolver-visible; that remains a separate
skill-governance action under the Protected Skill Boundary.

- `forseti-product-lead` — accepted/frozen as the primary Forseti-local
  product-lead skill identity on 2026-07-05 after the Forseti repo/project
  identity cutover. Migrated from the legacy `orca-product-lead` command/path;
  the old command/path remains as a thin compatibility wrapper for one
  transition window.
  - Source path: `.agents/skills/forseti-product-lead/SKILL.md` (Forseti-local).
  - Source sha256: `367867FBA97232B12E33F68C443430869BB9C0793D6494B67C8FA08232671B39`
    (observed with Get-FileHash on 2026-07-05; `.agents` source and `.claude`
    deployment copy are byte-identical; git content blob
    `b3a1077f58c1b018d75564405cde4ccccdcbb2c8` on both copies).
    Reread-required if the file changes.
  - Compatibility wrapper path: `.agents/skills/orca-product-lead/SKILL.md` with
    deployment copy at `.claude/skills/orca-product-lead/SKILL.md`.
  - Compatibility wrapper sha256: `3A7C819477F475761831B05E0A607CC3A8E1A0E97DCD6875438A79BB2706C3E0`
    (observed with Get-FileHash on 2026-07-05; source and deployment wrapper
    copies are byte-identical; git content blob
    `6411b8a9b8abd73386eb64109a85534f40ddf931` on both wrapper copies).
    The wrapper loads the sibling `forseti-product-lead` skill and carries no
    product method of its own.
  - Scope: prepares — does not freeze, run outreach, produce, or build — any
    Forseti product decision (value proposition, offer, ICP / first-proof wedge,
    buyer-proof design, positioning / packaging, deliverable shape, pull / kill /
    graduation). A thin router into Forseti product authority; defers every fact
    to `AGENTS.md`, the overlay, and the decision records; fails visibly when
    authority is missing.
  - Shadow name: distinct from the resolver-visible jb-scoped `product-lead`.
  - Collision (checked 2026-07-05): no repo-local, project-level Claude,
    user-level Codex, user-level Agents, or user-level Claude skill folder named
    `forseti-product-lead`; active in-thread resolver did not expose a
    `forseti-product-lead` skill before this source change. Existing
    `orca-product-lead` remains only as the repo/project compatibility wrapper;
    existing `product-lead` remains jb-scoped and is not imported.
  - Overlay loaded for migration: README, decision-routing, source-of-truth,
    skill-adoption, artifact-folders, validation-gates, source-loading, and the
    skill/preflight identity migration plan.
  - Deployment (2026-07-05): DEPLOYED/ACTIVATED for the Claude Code runtime as a
    project-level copy at `.claude/skills/forseti-product-lead/SKILL.md`
    (byte-identical to source; same sha256). Project scope only — not
    user-global (`~/.claude/skills/`), not plugin, not external. Sync rule: the
    `.agents/skills/forseti-product-lead/` file is source-of-record; on any
    source change, regenerate the `.claude/skills/forseti-product-lead/` copy and
    re-pin the sha256 here. Invocation: `/forseti-product-lead` (command name
    from the directory), description auto-trigger, or the Skill tool. Legacy
    invocation `/orca-product-lead` remains as a wrapper for one transition
    window. Codex / other-runtime activation is a separate target, not claimed by
    this record.
  - Rollback: delete `.agents/skills/forseti-product-lead/` and
    `.claude/skills/forseti-product-lead/`; restore the full-method
    `orca-product-lead` copies from the previous commit; revert this record, the
    `.agents/skills/` entry in `artifact-folders.md`, and the status/repo-map
    rows updated by the migration. Do not edit plugin / user-level / installed /
    external skill source.
  - Boundary: not Forseti authority; Forseti-local only; project-scoped (not
    user-global, not plugin, not external).

## Protected Skill Boundary

Do not install, uninstall, rename, rewrite, shadow, or promote global,
user-level, plugin-contributed, installed, or external source skills from
ordinary Forseti product work.

Those actions require a separate explicit skill-governance authorization after
resolver-visible collision checks and rollback planning. The Forseti-local
candidate lane above does not grant that authority.

## Rollback

Rollback for this overlay recognition update is to remove the `0.1.52`
recognition sections and restore the prior recognized-skill record from Git or
human-approved notes. Rollback must not edit plugin source, installed plugin
cache files, global/user skill roots, or external workflow source.

## Known Snapshots

- The Turn 6 resolver-visible skill snapshot is recorded in
  `docs/workflows/orca_bootstrap_record.md`.
- The 2026-06-05 collision table above is the current recognition check for
  Agent Workflow plugin cache `0.1.52`.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    Product-lead skill identity migrated from compatibility `orca-product-lead`
    to primary `forseti-product-lead`; `/orca-product-lead` remains as a thin
    project-local compatibility wrapper for one transition window, while source,
    deployment copy, hash pins, collision evidence, rollback, and live route docs
    now bind the Forseti-primary skill ID.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
    - output_authority
  controlling_sources_updated:
    - .agents/workflow-overlay/skill-adoption.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/skills/forseti-product-lead/SKILL.md
    - .agents/skills/orca-product-lead/SKILL.md
    - .claude/skills/forseti-product-lead/SKILL.md
    - .claude/skills/orca-product-lead/SKILL.md
  downstream_surfaces_checked:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/validation-gates.md
    - .agents/hooks/guard_protected_actions.py
    - docs/decisions/forseti_skill_preflight_identity_migration_plan_v0.md
    - docs/decisions/forseti_compatibility_migration_boundary_v0.md
    - docs/decisions/forseti_external_identity_path_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: docs/prompts/** and docs/review-outputs/** historical artifacts
      reason: >
        Historical prompts/reviews preserve provenance; legacy
        `orca-product-lead` mentions there are not live skill identity defaults.
    - path: orca_start_preflight references
      reason: >
        Start-preflight alias retirement remains explicitly deferred; this lane
        only migrates the product-lead skill command/path.
  stale_language_search: >
    rg -n "orca-product-lead|forseti-product-lead|orca_start_preflight|forseti_start_preflight"
    AGENTS.md CLAUDE.md README.md .agents .claude docs/decisions docs/workflows docs/prompts
  stale_language_search_result: >
    Executed 2026-07-05 in codex/forseti-product-lead-skill-identity. Counts in
    the checked source set: 13 files mention `forseti-product-lead`, 25 files
    mention `orca-product-lead`, and 180 files mention `orca_start_preflight`.
    Live primary skill identity hits are the new `.agents`/`.claude`
    `forseti-product-lead` copies plus skill-adoption, skill/preflight plan,
    repo-map, post-harness status, external-identity, compatibility-boundary,
    and hook-fixture surfaces. Remaining `orca-product-lead` hits are the thin
    compatibility wrappers, live docs explaining that wrapper, and historical
    prompt/review/workflow/decision provenance. Remaining `orca_start_preflight`
    hits are the explicitly deferred alias and historical prompt/review
    consumers; no start-preflight retirement is claimed. A stale-phrase scan for
    old "frozen compatibility" wording returned only two hits in the older
    stale-reference audit record, treated as superseded provenance.
  non_claims:
    - not validation
    - not readiness
    - not resolver activation proof
    - not start-preflight alias retirement
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
