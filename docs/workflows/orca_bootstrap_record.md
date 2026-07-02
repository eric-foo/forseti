# Orca Bootstrap Record

```yaml
retrieval_header_version: 1
artifact_role: Bootstrap workflow record
scope: Initial Orca docs-first workspace bootstrap state, decisions, source hashes, and rollback notes.
use_when:
  - Reconstructing Orca bootstrap provenance.
  - Checking early workspace initialization decisions.
  - Investigating import queue or branch-casing bootstrap context.
open_next:
  - .agents/workflow-overlay/README.md
  - docs/migration/import_queue.md
authority_boundary: retrieval_only
```

## Bootstrap Metadata

- Bootstrap turn: 06-orca-docs-first-bootstrap
- Bootstrap date: 2026-05-13
- Target path: `C:\Users\vmon7\Desktop\projects\orca`
- Migration authority source: `C:\Users\vmon7\Desktop\projects\jb`
- Implementation authorized this turn: docs-first bootstrap only

## Source Hierarchy And Hashes

| Source | SHA256 | Status |
| --- | --- | --- |
| `docs/prompts/workflows/orca_workflow_kernel_turn_06_orca_bootstrap_prompt.md` | `396EBC1C708395F530A77A701683EAAF6DEAE18163D78EE9BD6A34602AC82AA1` | matched |
| `docs/workflows/orca_workflow_kernel_migration_charter.md` | `EF8C7947FD77D35F7E368AE37CF18E91387CB808C4E26BD6359C93ED5AA019A5` | matched |
| `docs/workflows/orca_workflow_kernel_layer_contract.md` | `8C258610E493A0C2FC7B899B48805B88BF316B61402E5AB1D2714139B3EEBD14` | matched |
| `docs/workflows/orca_workflow_kernel_skill_inventory_matrix.md` | `EAD9B48C29A44DB435474A3E3BE965BE28E974F36206DA991D047D098A982FF4` | matched |
| `docs/workflows/orca_workflow_kernel_agent_workflow_layout.md` | `10BCEC029D9229954F15E6D5360F2FFA1316DBB4AD8999F6C0039345A5840B44` | matched |
| `docs/workflows/orca_workflow_kernel_adoption_protocol.md` | `95C839C472635B22120D03A1E6B9D1A8F723BE44FDB08B876FC82CC1226E6A32` | matched |

## Target Path State Before Edit

- `C:\Users\vmon7\Desktop\projects\orca` existed before edit: no
- Top-level contents before edit: none; path was absent
- Existing Git repo before edit: no
- Safe bootstrap mode: create new docs-first workspace and initialize Git

## Git State

- Git initialized this turn: yes
- Existing Git repo reused: no
- Commit created: no
- Remote configured: no

## Resolver-Visible Skill-Name Snapshot

| Root | Observed names or paths |
| --- | --- |
| `C:\Users\vmon7\Desktop\projects\jb\.agents\skills` | `adversarial-artifact-review`, `architecture`, `code-review`, `deep-thinking`, `documentation-health-check`, `feature-ultraplan`, `gap-final-hygiene`, `porting-check`, `postmortem-review`, `product-lead`, `product-ultraplan`, `prompt_orchestrator`, `repo-context-orchestrator`, `repo-hygiene-cleanup`, `skill-authoring-discipline` |
| `C:\Users\vmon7\.codex\skills` | `.system`, `review` |
| `C:\Users\vmon7\.codex\skills\.system` | `imagegen`, `openai-docs`, `plugin-creator`, `skill-creator`, `skill-installer` |
| `C:\Users\vmon7\.agents\skills` | `pre-compact-checkpoint` |
| plugin-contributed visible skills | `browser-use:browser` from `C:\Users\vmon7\.codex\plugins\cache\openai-bundled\browser-use\0.1.0-alpha2\skills\browser\SKILL.md` |

Direct same-name collision observed for Turn 6 adoption work: none. Semantically adjacent review names still require boundary preservation before any later adoption or promotion work.

## `orca nonrepo` Read-Only Inventory

- Reference path: `C:\Users\vmon7\Desktop\projects\orca nonrepo`
- Existed during preflight: no
- Inventory summary: absent
- Files moved, deleted, or copied from reference path: none

## Files Created Or Updated

- `README.md`
- `AGENTS.md`
- `.gitignore`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/project-authority.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/safety-rules.md`
- `.agents/workflow-overlay/skill-adoption.md`
- `docs/README.md`
- `docs/decisions/README.md`
- `docs/prompts/README.md`
- `docs/review-inputs/README.md`
- `docs/review-outputs/README.md`
- `docs/workflows/orca_bootstrap_record.md`
- `docs/migration/import_queue.md`

## Decisions

| ID | Status | Decision |
| --- | --- | --- |
| T6-ORCA-01 | PROPOSED_LOCK | Target path was absent, so create a new docs-first Orca workspace and initialize Git without committing. |
| T6-ORCA-02 | PROPOSED_LOCK | Orca is a separate docs-first repo/workspace and does not inherit `jb` project authority. |
| T6-ORCA-03 | PROPOSED_LOCK | Orca project overlay is bound at `.agents/workflow-overlay/`. |
| T6-ORCA-04 | PROPOSED_LOCK | Orca source hierarchy starts with explicit turn instruction, `AGENTS.md`, the overlay, then Orca docs; future `agent-workflow` source owns generic mechanics only. |
| T6-ORCA-05 | PROPOSED_LOCK | Orca artifact folders are docs-first under `docs/decisions`, `docs/prompts`, `docs/review-inputs`, `docs/review-outputs`, `docs/workflows`, and `docs/migration`. |
| T6-ORCA-06 | PROPOSED_LOCK | Orca review lanes distinguish read-only artifact review, patch/executor work, and deferred workflow-kernel adoption review. |
| T6-ORCA-07 | PROPOSED_LOCK | Orca validation gates require file existence, no implementation directories, no inherited `jb` authority, source-hash evidence, skill snapshot evidence, and Git status evidence. |
| T6-ORCA-08 | PROPOSED_LOCK | Orca safety rules require visible failure on missing authority, no external reference mutation, no global skill mutation, and no implementation without explicit authorization. |
| T6-ORCA-09 | PROPOSED_LOCK | `orca nonrepo` was absent; import queue records absence and no files were moved, deleted, or copied. |
| T6-ORCA-10 | PROPOSED_LOCK | Orca workflow-skill adoption status is no global installs, no local reusable kernel source, no shadow skills, and no same-name promotions. |
| T6-ORCA-11 | PROPOSED_LOCK | Rollback for this absent-target bootstrap is removal of the newly created Orca directory only with explicit user approval. |
| T6-ORCA-12 | PROPOSED_LOCK | Turn 7 needs owner input for Orca facts plus canonical `agent-workflow` source bootstrap and first shadow-candidate preparation without global install unless separately authorized. |

## Rollback Instructions

Because the Orca target path was absent before this turn, rollback is removing `C:\Users\vmon7\Desktop\projects\orca` and all files created by this turn. Perform rollback only with explicit user approval. Do not edit `jb`, installed global skills, user-level skills, plugin cache files, or external reference folders during rollback.

## Post-Audit Validation Addendum

Added by the supervising thread after Turn 6 audit.

- Global installed skill roots were not modified by Turn 6.
- User-level skill roots were not modified by Turn 6.
- Plugin-contributed skill roots and plugin cache files were not modified by Turn 6.
- `C:\Users\vmon7\Desktop\projects\orca nonrepo` was absent before and after Turn 6 and was not mutated.
- Orca initial Git branch observed after bootstrap: `Main`.
- Branch casing was not changed by Turn 6 or this addendum.
- Git status warning observed: `unable to access 'C:\Users\vmon7/.config/git/ignore': Permission denied`. This did not block status checks, but Turn 7 should account for it before Git automation.

## Branch Casing Deliberation For Turn 7

Current branch casing is `Main`. The migration has not locked an Orca branch naming policy yet.

Recommendation for Turn 7: decide branch casing before the first Orca commit. Prefer renaming `Main` to `main` unless there is an explicit Orca-specific reason to keep `Main`, because `jb` uses lowercase `main` and matching that convention reduces avoidable cross-repo friction in prompts, scripts, remotes, and future automation. Keeping `Main` is viable only if it is intentionally accepted as Orca policy before any commit or remote setup.

Turn 7 should record one of these decisions before committing Orca bootstrap files:

- Rename `Main` to `main` before the first commit.
- Keep `Main` as the intentional Orca default branch name.
- Defer branch policy again only if Turn 7 remains documentation-only and does not commit or configure remotes.

## Remaining Decisions For Later Turns

- Orca product/domain purpose: UNKNOWN - requires owner input.
- Orca implementation scope and runtime stack: UNKNOWN - requires owner input.
- Orca model lanes and output contracts beyond current docs-first lanes: UNKNOWN - requires owner input.
- Fresh-context Orca independence dry run details: deferred to later validation turn.
- Orca branch casing: current branch is `Main`; Turn 7 should decide before first commit or remote setup.
- `agent-workflow` canonical source bootstrap and shadow-candidate preparation: recommended next turn.

## Turn 7 Branch Casing Decision Addendum

# Turn 07 Branch Casing Decision

- Decision ID: T7-AW-04
- Status: PROPOSED_LOCK
- Decision date: 2026-05-13
- Decision: Orca default branch casing is main.
- Prior branch observed before rename: Main
- Branch observed after rename: main
- Commit state before decision: no commits
- Action: renamed unborn branch Main to main before first commit.
- Rationale: lowercase main avoids avoidable cross-workspace friction in prompts, scripts, remotes, and future automation. No Orca-specific reason to keep Main was identified.
- Publication boundary: no commit, push, remote setup, branch publication, or PR is authorized in this turn.
- Rollback: reverse the branch rename only before the first commit and only with explicit approval.
