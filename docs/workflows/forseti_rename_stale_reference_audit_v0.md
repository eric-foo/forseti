# Forseti Rename Stale Reference Audit v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Final classified stale-reference audit for the Forseti rename Step 5 lane.
use_when:
  - Checking what remains after the bounded runtime/tooling rename repair.
  - Deciding whether a remaining Orca hit is a defect or valid residual.
  - Preparing any future high-lock-in compatibility migration.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_rename_migration_policy_v0.md
  - docs/decisions/forseti_compatibility_migration_boundary_v0.md
  - docs/workflows/forseti_rename_residual_inventory_v0.md
```

## Start Preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: implementation-authorized by explicit fused invocation
  target_scope: Forseti rename Step 4 runtime/tooling repair and Step 5 stale-reference audit
  dirty_state_checked: yes
  blocked_if_missing: docs/decisions/forseti_compatibility_migration_boundary_v0.md
workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\forseti-compat-scope
branch: codex/forseti-compat-scope
base_commit_observed: 351fe2ac Rename live project authority to Forseti (#646)
input_handoff: docs/prompts/handoffs/forseti_compatibility_batches_fused_handoff_v0.md
output_mode: file-write
```

## Fused Route

```yaml
fused_status:
  implementation_scoping: ROUTE_COMPLETE
  spec_writing: SPEC_NOT_NEEDED_READY_FOR_SCOPING
  micro_decision_locking: locked
  implementation: completed
review_routing_status: not_needed
review_routing_reason: docs-only harness README compatibility label repair; no code behavior changed
adversarial_review_prompt: not_produced
adversarial_review_reason: >
  The fused change is a bounded documentation/runtime-label repair plus an audit
  record. It does not change code, behavior, validation gates, CI dependencies,
  path/package identifiers, skill IDs, or product doctrine.
```

The existing compatibility boundary already binds the implementation contract:
patch only live human-facing labels that imply Orca remains the current project,
preserve compatibility identifiers, and write the final classified audit. No
new spec artifact was needed because the handoff and boundary decision already
name the allowed and forbidden edits.

## Step 4 Result

Patched:

| File | Change | Classification |
| --- | --- | --- |
| `orca-harness/README.md` | Changed the title from "Orca Harness" to "Forseti Harness" and added a compatibility note for the retained `orca-harness` identifier. | Live human-facing runtime/tooling label repair. |

Intentionally not patched:

| Surface | Reason |
| --- | --- |
| `.github/workflows/ci.yml` | `orca-harness-tests` and `orca-harness` working directory are compatibility identifiers. |
| `.github/workflows/auto-merge.yml` | Depends on the retained `orca-harness-tests` check name. |
| `.github/workflows/pr-risk-router.yml` | Uses retained path/comment compatibility identifiers. |
| `.agents/hooks/**` | Hits are hook names, path checks, fixture references, selftests, or report-mode strings tied to compatibility roots. |
| `.agents/skills/orca-product-lead/SKILL.md` | Skill command/path remains a frozen compatibility identifier. |
| `docs/prompts/**`, `docs/review-inputs/**`, `docs/review-outputs/**` | Historical/provenance artifacts by default; not word-match edited. |
| `docs/_inbox/**` | Scratch/inbox material; leave unless promoted. |

## Step 5 Census

Commands were run from `C:\Users\vmon7\Desktop\projects\orca\worktrees\forseti-compat-scope` after the Step 4 README repair and this audit/map update.

| Question | Command | Observed count |
| --- | --- | ---: |
| Files with content hits in explicit project roots | `rg -l -i "\bOrca\b|\bORCA\b|orca_start_preflight" AGENTS.md README.md CLAUDE.md .agents .github docs orca orca-harness repo-structure.yaml \| Measure-Object` | 2024 |
| Matched content lines in explicit project roots | `rg -n -i "\bOrca\b|\bORCA\b|orca_start_preflight" AGENTS.md README.md CLAUDE.md .agents .github docs orca orca-harness repo-structure.yaml \| Measure-Object` | 28907 |
| Path/name hits | `rg --files \| rg -i "(^|[\\/])(orca|orca-|orca_)|orca-harness|orca-product-lead|orca_repo_map" \| Measure-Object` | 1486 |

Content hits by top-level root:

| Root | Files |
| --- | ---: |
| `docs` | 1473 |
| `orca` | 285 |
| `orca-harness` | 223 |
| `.agents` | 37 |
| `.github` | 4 |
| `README.md` | 1 |
| `repo-structure.yaml` | 1 |

Docs hits by second-level folder:

| Folder | Files |
| --- | ---: |
| `docs/review-inputs` | 535 |
| `docs/prompts` | 322 |
| `docs/review-outputs` | 258 |
| `docs/research` | 111 |
| `docs/decisions` | 106 |
| `docs/workflows` | 79 |
| `docs/migration` | 35 |
| `docs/hygiene` | 24 |
| `docs/README.md` | 1 |
| `docs/STRUCTURE.md` | 1 |
| `docs/_inbox` | 1 |

Path/name hits by top grouping:

| Group | Paths |
| --- | ---: |
| `orca-harness` | 1186 |
| `orca` | 296 |
| `docs` | 4 |

## Classified Audit

| Class | Status after Step 4 | Default action |
| --- | --- | --- |
| Live human-facing runtime/tooling label | The scoped defect in `orca-harness/README.md` is repaired. No other live defect was identified in the targeted control-surface scan. | Patch if found; otherwise leave compatibility IDs stable. |
| Compatibility identifier | Still present by design: `orca/product/`, `orca-harness/`, `docs/workflows/orca_repo_map_v0.md`, `orca-product-lead`, `orca_start_preflight`, lowercase `orca_*`, and `orca-harness-tests`. | Preserve until a separately accepted migration plan exists. |
| Historical provenance | Still present across old prompts, reviews, DCP receipts, migration notes, and dated records. | Preserve. |
| Explicit legacy alias | Still present where records intentionally name Orca as the prior project name or accepted alias. | Preserve with clarity; new live records prefer Forseti. |
| Scratch/inbox | Still present where material is not promoted to authority. | Leave unless promoted or used as source. |

## Targeted Control-Surface Result

| Surface | Result |
| --- | --- |
| `orca-harness/README.md` | Title now says "Forseti Harness"; remaining hits are compatibility path references. |
| `.github/workflows/*` | Remaining hits are retained check names, working directories, path predicates, or comment markers. |
| `.agents/hooks/**` | Remaining hits are compatibility path constants, report-mode names, fixtures, selftests, and repo slug strings. |
| `.agents/skills/orca-product-lead/SKILL.md` | Remaining hits are the frozen compatibility skill command/path and product-tree paths. |
| `docs/workflows/orca_repo_map_v0.md` | Path remains the compatibility repo-map path; this audit is added as a retrievable row. |

## Residual Queue

```yaml
live_defect_queue: []
deferred_migration_queue:
  - root_or_package_migration: orca/product/
  - root_or_package_migration: orca-harness/
  - skill_id_migration: orca-product-lead
  - ci_check_migration: orca-harness-tests
required_before_deferred_migration:
  - owner-accepted moved-path index
  - rollback notes
  - package/import/reference rewrite plan
  - CI/check-name and branch-protection dependency analysis
  - validation gates and timeouts
forbidden_validation_retry:
  - registration_integrity.py --selftest
```

## Non-Claims

- This audit is not validation, readiness, product proof, path/package migration, or CI/check-name migration.
- This audit is not an exhaustive line-by-line classification of every remaining content hit.
- This audit does not prove every remaining Orca hit is valid; it records that no scoped live defect was identified after the targeted control-surface repair.
- This audit does not block a future migration; it prevents implicit word-match migration.