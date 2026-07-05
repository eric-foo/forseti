# Forseti Skill and Preflight Identity Migration Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Phased plan and execution record for retiring retained Orca skill/preflight compatibility identifiers without breaking existing prompt and skill invocation surfaces.
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

Do not retire `orca_start_preflight` by word match. The product-lead skill ID is now migrated through the governed skill-identity lane, not by broad replacement.

Current rule:

| Surface | Current state | Migration decision |
| --- | --- | --- |
| `forseti_start_preflight` | Primary start-preflight key in `.agents/workflow-overlay/source-loading.md` and prompt orchestration. | Keep as the forward-primary key. |
| `orca_start_preflight` | Accepted legacy alias during the Forseti rename compatibility migration. | Preserve until durable prompt/history tolerance is explicitly retired. |
| `forseti-product-lead` | Primary accepted/frozen Forseti-local product-lead skill command/path, with source at `.agents/skills/forseti-product-lead/SKILL.md` and deployment copy at `.claude/skills/forseti-product-lead/SKILL.md`. | Use as the forward skill identity after this lane lands. |
| `orca-product-lead` | Legacy compatibility wrapper retained in source and deployment skill roots. | Preserve for one transition window; wrapper loads sibling `forseti-product-lead` and carries no product method of its own. |

## Assumption Gate

```yaml
assumption_gate:
  status: SKILL_ID_EXECUTED_PREFLIGHT_ALIAS_DEFERRED
  applies_to: "skill ID migration executed for forseti-product-lead; orca_start_preflight retirement remains later"
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
      evidence: ".agents/workflow-overlay/skill-adoption.md now binds primary `.agents/skills/forseti-product-lead/SKILL.md`, `.claude/skills/forseti-product-lead/SKILL.md`, wrapper `.agents/.claude` `orca-product-lead` paths, source/wrapper hashes, invocation `/forseti-product-lead`, compatibility `/orca-product-lead`, and rollback path."
  prerequisites:
    - item: "Repair or consciously supersede current-main source/deployment skill-copy divergence before any skill-ID migration."
      triage: verified_resolved
      owner: agent
      order: 0
      basis: "On this lane, Get-FileHash and git diff --no-index verified source/deployment `orca-product-lead` copies were byte-identical before migration; the new `forseti-product-lead` source/deployment copies and old wrappers are also byte-identical by pair."
    - item: "Resolver-visible collision check for `forseti-product-lead`."
      triage: verified_clear_for_project_local_adoption
      owner: agent
      order: 1
      basis: "No repo-local, project-level Claude, user-level Codex, user-level Agents, or user-level Claude skill folder named `forseti-product-lead` was present before this lane; current running-thread resolver activation is not claimed."
    - item: "Prompt/history residual classification for `orca_start_preflight`."
      triage: blocker
      owner: agent
      order: 2
      basis: "The legacy alias appears in durable workflow/prompt history; retirement requires classifying current live consumers versus historical provenance."
```

## Phased Migration

1. Source/deployment copy sync repair is resolved for this lane: the old
   `orca-product-lead` pair matched before migration, and both new primary and
   wrapper pairs match after migration.
2. Keep `forseti_start_preflight` as the primary receipt key and keep
   `orca_start_preflight` as a documented alias. Update only live authority that
   wrongly presents the legacy alias as primary.
3. `forseti-product-lead` is added as the forward skill identity while
   preserving `/orca-product-lead` as a compatibility wrapper for one transition
   window.
4. `.agents/workflow-overlay/skill-adoption.md`,
   `.agents/workflow-overlay/artifact-folders.md`, the hook selftest fixture,
   source skill copy, deployment copy, hash pins, and rollback notes are updated
   together in this lane.
5. Targeted residual searches classify remaining legacy hits as compatibility
   wrapper, explicit legacy alias, historical provenance, or missed live surface;
   `orca_start_preflight` retirement stays deferred.

## Validation

The later implementation PR should run at least:

```powershell
rg -n "orca-product-lead|forseti-product-lead|orca_start_preflight|forseti_start_preflight" AGENTS.md CLAUDE.md README.md .agents .claude docs\decisions docs\workflows docs\prompts
Get-FileHash .agents\skills\forseti-product-lead\SKILL.md -Algorithm SHA256
Get-FileHash .claude\skills\forseti-product-lead\SKILL.md -Algorithm SHA256
Get-FileHash .agents\skills\orca-product-lead\SKILL.md -Algorithm SHA256
Get-FileHash .claude\skills\orca-product-lead\SKILL.md -Algorithm SHA256
git diff --no-index -- .agents\skills\forseti-product-lead\SKILL.md .claude\skills\forseti-product-lead\SKILL.md
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
| Delete `/orca-product-lead` now | The old invocation remains a compatibility wrapper for at least one transition window. |
| Rename the `orca-product-lead` folders only | Folder rename alone would miss skill-adoption pins, deployment copy, invocation compatibility, and resolver collision checks. |
| Replace every durable `orca-product-lead` mention | Historical prompts, review outputs, and prior migration evidence should preserve provenance unless separately promoted. |
| Treat copy divergence as a naming migration | Copy sync is a prerequisite repair, not proof that the compatibility skill ID should be renamed. |

## Non-Claims

- This execution record is not validation, readiness, resolver behavior proof, or activation proof.
- This execution record claims only repo-local source/deployment skill files and hashes after this lane lands; it does not prove the current running thread has reloaded resolver metadata.
- This execution record does not retire `/orca-product-lead` or `orca_start_preflight`.

## Direction Change Propagation

The 2026-07-04 planning receipt below is historical for the pre-implementation split; the 2026-07-05 execution receipt supersedes its skill-ID deferral while preserving the start-preflight alias boundary.

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


```yaml
direction_change_propagation:
  doctrine_changed: >
    The product-lead skill ID migration executed: `forseti-product-lead` is now
    the primary Forseti-local accepted/deployed product-lead skill, while
    `/orca-product-lead` remains as a thin compatibility wrapper for one
    transition window. `forseti_start_preflight` remains primary and
    `orca_start_preflight` remains a deferred legacy alias.
  trigger: workflow_authority
  related_triggers:
    - lifecycle_boundary
    - output_authority
  controlling_sources_updated:
    - docs/decisions/forseti_skill_preflight_identity_migration_plan_v0.md
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
    - docs/decisions/forseti_compatibility_migration_boundary_v0.md
    - docs/decisions/forseti_external_identity_path_migration_decision_v0.md
    - docs/workflows/forseti_post_harness_migration_status_v0.md
    - docs/workflows/forseti_repo_map_v0.md
  intentionally_not_updated:
    - path: docs/prompts/** and docs/review-outputs/** historical artifacts
      reason: >
        Historical prompt/review provenance can keep old `orca-product-lead`
        mentions; the live compatibility wrapper keeps those invocations
        intelligible.
    - path: orca_start_preflight references
      reason: >
        Start-preflight alias retirement remains deferred pending prompt/history
        consumer classification.
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
