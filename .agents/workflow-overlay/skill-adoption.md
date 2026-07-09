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
- Orca has one accepted Forseti-local candidate skill: `forseti-product-lead`
  (accepted/frozen 2026-06-08; DEPLOYED/ACTIVATED 2026-06-08 for the Claude Code
  runtime, project-scoped — not user-global). See `## Accepted Orca-Local
  Candidate Skills` below. Orca accepts only specific, narrowly scoped local
  candidates like this one.
- Orca has no accepted global skill shadow candidates.
- Orca has no same-name global skill promotions.
- Orca may use resolver-visible workflow skills when explicitly invoked or
  selected by the active resolver. This does not make external workflow source
  documents Forseti authority.
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
  manifest and is not a recognized Orca workflow tool.
- Previous recognized `workflow-compound-planning` entry from plugin cache
  `0.1.3` is stale; use `incremental-planning` for next-move sequencing.
- `workflow-cartographer` is present in the installed plugin package and in the
  active resolver-visible skill list for the current Codex thread. It is not
  present under `C:\Users\vmon7\.codex\skills`, which is an older user-level
  shadow surface and must not be treated as the Agent Workflow plugin inventory.

## Recognized Workflow Tools

| Skill | Advisory use in Orca | Collision status observed 2026-06-05 |
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
is an Orca routing and collision record, not package validation or resolver
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
- Accept an Forseti-local candidate as frozen only when it is specific and narrowly
  scoped to a real Orca lane (like `forseti-product-lead`), defers all Forseti facts to
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

## Accepted Orca-Local Candidate Skills

Orca does accept Forseti-local candidate skills, but only specific, narrowly scoped
ones like the product-lead method below — never broad, generic, or
authority-claiming local skills. Acceptance is a LOCAL FREEZE only: it does not
deploy, activate, or make the skill resolver-visible; that remains a separate
skill-governance action under the Protected Skill Boundary.

- `forseti-product-lead` — accepted/frozen 2026-06-08; refreshed + re-frozen
  2026-06-12 (owner-authorized skill-edit: thesis/wedge citations re-routed
  through the repo-map product-anchor rows after the consumer-demand
  ratification; both copies verified identical; closes ORCA-HYGIENE-019).
  - Source path: `.agents/skills/forseti-product-lead/SKILL.md` (Forseti-local).
  - Source sha256: `37FD65B7833CE80AC251111C6D5E7A1F26C26106E948F2134BE5533340AA3510`
    (re-pinned 2026-06-16 after the product-lead adoption-record route
    reference moved from flat `docs/product/` to `docs/product/product_lead/`;
    prior frozen sha `C8DEAA4DDEC94321ED47BA879D0C85269CACFEEE8D733B3634AB1A1C792634A3`,
    `42EF7C2DCE667CFA09EA6F3F8CE369C7F55D7721D131692CB06C11152E908BB5`)
    (working-tree bytes; updated at deployment 2026-06-08 when the status text was
    added; supersedes the at-acceptance hash 2B011CE8; reread-required if the file
    changes).
    (eol note: checkout filters may materialize CRLF or LF working-tree bytes,
    so the durable identity is the git blob. In this worktree, on-disk
    Get-FileHash reads
    `37FD65B7833CE80AC251111C6D5E7A1F26C26106E948F2134BE5533340AA3510`; git
    content blob is `d88f6cbf24461954b0bfcdc69ecb1d470517d5f3` on both copies,
    identical after the route-reference refresh.)
  - Scope: prepares — does not freeze, run outreach, produce, or build — any Orca
    product decision (value proposition, offer, ICP / first-proof wedge,
    buyer-proof design, positioning / packaging, deliverable shape, pull / kill /
    graduation). A thin router into Orca product authority; defers every fact to
    `AGENTS.md`, the overlay, and the decision records; fails visibly when
    authority is missing.
  - Shadow name: distinct from the resolver-visible jb-scoped `product-lead`.
  - Collision (re-confirmed 2026-06-08): `.agents/skills/` contains only this
    skill (repo-local glob); the shadow name avoids the jb `product-lead`
    collision; resolver-visible activation is NOT proven in-thread (see the
    Activation Caveat above).
  - Overlay loaded at acceptance: README, decision-routing, skill-adoption,
    source-of-truth, project-authority, safety-rules, product-proof,
    artifact-folders, communication-style, validation-gates, source-loading,
    retrieval-metadata.
  - Deployment (2026-06-08): DEPLOYED/ACTIVATED for the Claude Code runtime as a
    project-level copy at `.claude/skills/forseti-product-lead/SKILL.md`
    (byte-identical to source; same sha256). Project scope only — not user-global
    (`~/.claude/skills/`), not plugin, not external. Sync rule: the
    `.agents/skills/` file is source-of-record; on any source change, regenerate
    the `.claude/skills/` copy and re-pin the sha256 here. Activation needs one
    Claude Code restart to begin watching the newly-created `.claude/skills/`
    directory. Invocation: `/forseti-product-lead` (command name from the
    directory), description auto-trigger, or the Skill tool. Codex /
    other-runtime activation is a separate target, not done here.
  - Rollback: delete `.claude/skills/forseti-product-lead/` (deployment copy) and/or
    `.agents/skills/forseti-product-lead/` (source); revert this record, the
    acceptance policy bullet above, and the `.agents/skills/` entry in
    `artifact-folders.md`; no plugin / user-level / installed / external skill
    source is touched.
  - Boundary: not Forseti authority; Forseti-local only; project-scoped (not
    user-global, not plugin, not external).

## Protected Skill Boundary

Do not install, uninstall, rename, rewrite, shadow, or promote global,
user-level, plugin-contributed, installed, or external source skills from
ordinary Orca product work.

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
