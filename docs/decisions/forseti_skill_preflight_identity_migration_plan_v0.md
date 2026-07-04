# Forseti Skill and Preflight Identity Migration Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Phased plan for retiring retained Orca skill/preflight compatibility identifiers without breaking existing prompt and skill invocation surfaces.
use_when:
  - Deciding whether to rename or retire `orca_start_preflight`.
  - Deciding whether to rename `orca-product-lead` to `forseti-product-lead`.
  - Scoping a later skill-ID migration after the Forseti authority, repo-map, and runtime root migrations settle.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/skill-adoption.md
  - docs/workflows/forseti_repo_map_v0.md
  - docs/workflows/forseti_rename_residual_inventory_v0.md
```

## Start Preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write
  target_scope: Forseti skill/preflight identity migration plan
  dirty_state_checked: yes
workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\forseti-skill-preflight-migration-plan
branch: codex/forseti-skill-preflight-migration-plan
base_commit_observed: e0c634a5 fix(transcript): classify the two YT probe surfaces out of the ASR lane (#673)
output_mode: file-write
```

## Decision

Do not retire `orca_start_preflight` or rename `orca-product-lead` by word match.

Current rule:

| Surface | Current state | Migration decision |
| --- | --- | --- |
| `forseti_start_preflight` | Primary start-preflight key in `.agents/workflow-overlay/source-loading.md` and prompt orchestration. | Keep as the forward-primary key. |
| `orca_start_preflight` | Accepted legacy alias during the Forseti rename compatibility migration. | Preserve until durable prompt/history tolerance is explicitly retired. |
| `orca-product-lead` | Accepted/frozen Forseti-local compatibility skill command/path. | Preserve until a separate skill-ID migration introduces `forseti-product-lead` with alias, deployment, resolver, and rollback handling. |
| `forseti-product-lead` | Not present as a skill ID on current main. | Do not introduce as a silent replacement; only add through the skill-governance lane below. |

## Assumption Gate

```yaml
assumption_gate:
  status: READY_WITH_VERIFIED_LEDGER
  applies_to: "later skill/preflight ID migration that may retire orca_start_preflight or introduce forseti-product-lead"
  load_bearing_assumptions:
    - assumption: "`orca_start_preflight` is a compatibility alias, not the current primary key."
      why_load_bearing: "If false, the first step would be authority repair; if true, the later migration should preserve alias tolerance and only retire it after prompt/history consumers are classified."
      verify_by: source_read
      verdict: verified_real
      evidence: ".agents/workflow-overlay/source-loading.md defines `forseti_start_preflight` and states `orca_start_preflight` is accepted as a legacy alias; prompt-orchestration references `forseti_start_preflight`."
    - assumption: "`orca-product-lead` cannot be renamed safely without skill-governance mechanics."
      why_load_bearing: "Skill IDs are invocation/deployment surfaces; changing only folder text would desync source, deployment copy, hash pins, and runtime resolver expectations."
      verify_by: source_read
      verdict: verified_real
      evidence: ".agents/workflow-overlay/skill-adoption.md binds `.agents/skills/orca-product-lead/SKILL.md`, `.claude/skills/orca-product-lead/SKILL.md`, source hash, invocation `/orca-product-lead`, and rollback path."
  prerequisites:
    - item: "Repair or consciously supersede current-main source/deployment skill-copy divergence before any skill-ID migration."
      triage: blocker
      owner: agent
      order: 0
      basis: "On current main, Get-FileHash differs between `.agents/skills/orca-product-lead/SKILL.md` and `.claude/skills/orca-product-lead/SKILL.md`; PR #668 or an equivalent lane is the intended repair."
    - item: "Resolver-visible collision check for `forseti-product-lead`."
      triage: blocker
      owner: agent
      order: 1
      basis: "Skill adoption policy requires collision status and rollback planning before adoption/rename."
    - item: "Prompt/history residual classification for `orca_start_preflight`."
      triage: blocker
      owner: agent
      order: 2
      basis: "The legacy alias appears in durable workflow/prompt history; retirement requires classifying current live consumers versus historical provenance."
```

## Phased Migration

1. Land or otherwise supersede the source/deployment skill-copy sync repair
   first. On current main, the `.agents` and `.claude` `orca-product-lead`
   copies have different hashes; a skill-ID migration must not build on a
   desynced deployment copy.
2. Keep `forseti_start_preflight` as the primary receipt key and keep
   `orca_start_preflight` as a documented alias. Update only live authority that
   wrongly presents the legacy alias as primary.
3. If the owner accepts a skill-ID migration, add `forseti-product-lead` as the
   forward skill identity while preserving `/orca-product-lead` as a compatibility
   alias or wrapper for at least one transition window.
4. Update `.agents/workflow-overlay/skill-adoption.md`,
   `.agents/workflow-overlay/artifact-folders.md`, hook selftest fixtures, source
   skill copy, deployment copy, hash pins, and rollback notes together.
5. Run targeted residual searches for `orca-product-lead`,
   `forseti-product-lead`, `orca_start_preflight`, and
   `forseti_start_preflight`; classify remaining legacy hits as live alias,
   compatibility wrapper, historical provenance, or missed live surface.

## Validation

The later implementation PR should run at least:

```powershell
rg -n "orca-product-lead|forseti-product-lead|orca_start_preflight|forseti_start_preflight" AGENTS.md CLAUDE.md README.md .agents .claude docs\decisions docs\workflows docs\prompts
Get-FileHash .agents\skills\orca-product-lead\SKILL.md -Algorithm SHA256
Get-FileHash .claude\skills\orca-product-lead\SKILL.md -Algorithm SHA256
git diff --no-index -- .agents\skills\orca-product-lead\SKILL.md .claude\skills\orca-product-lead\SKILL.md
python .agents/hooks/check_map_links.py --strict
python .agents/hooks/header_index.py --strict
python .agents/hooks/check_repo_map_freshness.py --strict
python .agents/hooks/check_dcp_receipt.py --strict
python .agents/hooks/check_review_routing.py --strict
python .agents/hooks/check_full_gt_claims.py --changed --strict
```

Do not run `registration_integrity.py --selftest` for this migration lane.

## Rejected Paths

| Path | Reason rejected |
| --- | --- |
| Delete `orca_start_preflight` now | It remains an accepted legacy alias and durable prompt/history tolerance has not been retired. |
| Rename the `orca-product-lead` folders only | Folder rename alone would miss skill-adoption pins, deployment copy, invocation compatibility, and resolver collision checks. |
| Replace every durable `orca-product-lead` mention | Historical prompts, review outputs, and prior migration evidence should preserve provenance unless separately promoted. |
| Treat copy divergence as a naming migration | Copy sync is a prerequisite repair, not proof that the compatibility skill ID should be renamed. |

## Non-Claims

- This plan is not implementation, validation, readiness, skill deployment, resolver behavior proof, or activation proof.
- This plan does not claim `forseti-product-lead` exists.
- This plan does not retire `/orca-product-lead` or `orca_start_preflight`.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The remaining skill/preflight Orca identifiers are split into forward-primary
    Forseti surfaces and compatibility aliases: `forseti_start_preflight` stays
    primary, `orca_start_preflight` remains an accepted legacy alias, and
    `orca-product-lead` remains a compatibility skill ID until a separate
    skill-governance migration introduces `forseti-product-lead` with alias,
    resolver, deployment-copy, hash-pin, and rollback handling.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
    - validation_philosophy
  controlling_sources_updated:
    - docs/decisions/forseti_skill_preflight_identity_migration_plan_v0.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - .agents/workflow-overlay/skill-adoption.md
    - .agents/workflow-overlay/artifact-folders.md
    - docs/workflows/forseti_repo_map_v0.md
    - docs/workflows/forseti_rename_residual_inventory_v0.md
    - .agents/skills/orca-product-lead/SKILL.md
    - .claude/skills/orca-product-lead/SKILL.md
  intentionally_not_updated:
    - path: .agents/skills/orca-product-lead/
      reason: >
        The skill ID remains the compatibility command/path until a separate
        skill-governance migration is accepted; current-main copy divergence is
        already a prerequisite repair, not a rename.
    - path: .claude/skills/orca-product-lead/
      reason: >
        Deployment-copy sync is owned by the existing skill-map refresh lane or
        an equivalent repair before any skill-ID migration.
    - path: .agents/workflow-overlay/source-loading.md
      reason: >
        It already makes `forseti_start_preflight` primary and preserves
        `orca_start_preflight` as a legacy alias.
  stale_language_search: >
    rg -n "orca-product-lead|forseti-product-lead|orca_start_preflight|forseti_start_preflight"
    AGENTS.md CLAUDE.md README.md .agents .claude docs/decisions docs/workflows docs/prompts
  stale_language_search_result: >
    Executed 2026-07-04 during planning. Hits are expected because the legacy
    alias and compatibility skill ID remain live compatibility surfaces; this
    decision binds the later migration conditions instead of editing them.
  non_claims:
    - not validation
    - not readiness
    - not implementation
    - not skill deployment
    - not resolver behavior proof
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
