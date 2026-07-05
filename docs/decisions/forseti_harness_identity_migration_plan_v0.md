# Forseti Harness Identity Migration Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Forseti decision record
scope: Plan and execution record for migrating the retained orca-harness compatibility runtime, package distribution label, and CI check identity to Forseti naming.
use_when:
  - Auditing the runtime/tooling lane that renames orca-harness/ and orca-harness-tests.
  - Deciding whether a remaining orca-harness hit is historical provenance, compatibility resolution, or a missed live surface.
  - Scoping validation for the harness root/package/CI migration PR.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/forseti_external_identity_path_migration_decision_v0.md
  - docs/workflows/forseti_post_harness_migration_status_v0.md
  - docs/workflows/forseti_rename_residual_inventory_v0.md
  - docs/workflows/forseti_repo_map_v0.md
```

## Start Preflight

```yaml
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom
  edit_permission: docs-write
  target_scope: Forseti harness identity migration plan
  dirty_state_checked: yes
workspace: C:\Users\vmon7\Desktop\projects\orca\worktrees\forseti-harness-migration-plan
branch: codex/forseti-harness-migration-plan
base_commit_observed: e0c634a5 fix(transcript): classify the two YT probe surfaces out of the ASR lane (#673)
output_mode: file-write
```

## Decision

Migrate `orca-harness/` to Forseti naming as a runtime/tooling lane, but do not
execute it as a broad text replacement or a cosmetic docs pass.

Implementation status: the stacked runtime lane
`codex/forseti-harness-runtime-rename` executes this plan by moving the tracked
root to `forseti-harness/`, renaming the package distribution label and CI check,
updating deterministic path consumers, and adding
`docs/migration/forseti_harness_runtime_migration_v0/moved_paths_index.md` for
historical path resolution. The external GitHub repository slug and local parent
folder remain outside this implementation lane.

Post-merge closeout: PR #675 merged to `main` as `c10f1d7f` on 2026-07-05.
The current tree has no tracked `orca/` or `orca-harness/` roots; it has 312
tracked files under `forseti/` and 1214 under `forseti-harness/`. The live CI
check name is `forseti-harness-tests`.

The target runtime identity is:

| Surface | Current | Target | Migration rule |
| --- | --- | --- | --- |
| Harness root directory | `orca-harness/` | `forseti-harness/` | Execute with `git mv`; update deterministic path consumers in the same PR. |
| Python distribution name | `orca-harness` | `forseti-harness` | Change the distribution label only; do not invent a `forseti_harness` import namespace. |
| CI required check | `orca-harness-tests` | `forseti-harness-tests` | Change with all check-name consumers, not before the merge helper and auto-merge workflow are updated. |
| Runtime import roots | top-level packages such as `source_capture`, `data_lake`, `ecr`, `schemas`, `runners`, plus `harness_utils` | unchanged | Preserve module import names; this plan is not a Python namespace refactor. |

## Assumption Gate

```yaml
assumption_gate:
  status: READY_WITH_VERIFIED_LEDGER
  applies_to: "runtime PR codex/forseti-harness-runtime-rename: orca-harness/ -> forseti-harness/ and orca-harness-tests -> forseti-harness-tests"
  load_bearing_assumptions:
    - assumption: "The harness root is a path/package/CI/checker dependency, not merely a display string."
      why_load_bearing: "If false, a docs-only or word-match rename would be safe; if true, the lane must update CI, hooks, package metadata, and path scanners together."
      verify_by: source_read
      verdict: verified_real
      evidence: ".github/workflows/ci.yml uses job/name orca-harness-tests and working-directory orca-harness; repo-structure.yaml declares orca-harness as a known top-level/tolerated legacy root; multiple .agents/hooks scripts use orca-harness paths."
    - assumption: "The distribution label can change without changing Python import namespaces."
      why_load_bearing: "A mistaken namespace migration would require broad import rewrites and create higher runtime risk than the identity migration needs."
      verify_by: source_read
      verdict: verified_real
      evidence: "orca-harness/pyproject.toml exposes py-modules and top-level packages such as source_capture, data_lake, ecr, schemas, and runners; tests/conftest.py inserts the harness root on sys.path."
  prerequisites:
    - item: "Do not change external GitHub repo slug/remotes in this lane."
      triage: already-decided
      owner: owner
      order: 0
      basis: "External repo identity is owner-gated and separate from internal compatibility paths."
    - item: "Carry a review-routing disposition or review artifact because the later PR touches code roots and hooks."
      triage: blocker
      owner: agent
      order: 1
      basis: ".agents/workflow-overlay/validation-gates.md and .agents/hooks/check_review_routing.py require a disposition for code-root changes."
    - item: "Regenerate or update uv.lock after changing the package distribution name."
      triage: blocker
      owner: agent
      order: 2
      basis: "orca-harness/uv.lock currently records the orca-harness package label."
```

## Live Surfaces To Change

The implementation PR updates these live surfaces as one coherent
runtime/tooling migration:

| Surface | Required change |
| --- | --- |
| `orca-harness/` | `git mv` to `forseti-harness/`; preserve internal package layout. |
| `orca-harness/pyproject.toml` | Change `project.name` to `forseti-harness`; keep top-level module/package exports unchanged. |
| `orca-harness/uv.lock` | Update the locked package name after the distribution label changes. |
| `.github/workflows/ci.yml` | Rename job id/name to `forseti-harness-tests`, set `working-directory: forseti-harness`, and update install-step label. |
| `.github/workflows/auto-merge.yml` | Update `CI_CHECK` to `forseti-harness-tests`. |
| `.github/scripts/merge-when-green.ps1` | Update the default required check name and default repo slug to `eric-foo/forseti` after the owner-gated external repo rename succeeds. |
| `.github/workflows/pr-risk-router.yml` | Update path classification from `orca-harness/` to `forseti-harness/`. |
| `repo-structure.yaml` | Replace the known top-level runtime root and legacy tolerance with `forseti-harness/`; preserve separate compatibility notes for historical references. |
| `.agents/hooks/*.py` | Update deterministic path constants, fixture roots, map-link roots, repo-map freshness rules, placement fixtures, ontology drift harness root, review-routing code roots, silver-lane registry root, and selftest fixtures that point at `orca-harness/`. |
| `.agents/workflow-overlay/*.md` and `docs/workflows/forseti_repo_map_v0.md` | Update live authority/navigation rows that name the current runtime root. |
| `renovate.json` | If present on the implementation base, update package-file matching that points at `orca-harness/youtube_capture`. |

## Phased Implementation

1. Start from the accepted harness-migration-plan branch as a stacked runtime lane;
   do not stack on the external identity blocker or product-lead skill-map PR.
2. Run `git mv orca-harness forseti-harness`.
3. Update package metadata and lockfile for the distribution-label rename only.
   Do not rename import modules to `forseti_harness`.
4. Update CI check identity and every check-name consumer in the same commit.
5. Update `.agents/hooks/`, `repo-structure.yaml`, and live overlay/repo-map
   path consumers that must understand the new runtime root.
6. Update harness-local operator docs that tell agents where to `cd`, install,
   or run package commands. Do not broad-rewrite historical prompts, review
   outputs, archived receipts, or dated migration evidence.
7. Run a targeted residual search for `orca-harness`, `orca_harness`, and
   `orca-harness-tests`. Classify each remaining hit as historical,
   compatibility pointer, or missed live surface before claiming completion.

## Validation

The implementation PR should run at least:

```powershell
git diff --check
Set-Location forseti-harness
python -m pip install -e . "pytest==9.0.3" pyyaml
python -m pytest
Set-Location ..
python .agents/hooks/check_map_links.py --strict
python .agents/hooks/header_index.py --strict
python .agents/hooks/check_repo_map_freshness.py --strict
python .agents/hooks/check_placement.py --strict
python .agents/hooks/check_ontology_ssot.py --strict
python .agents/hooks/check_ontology_tag_validity.py --strict
python .agents/hooks/check_ontology_drift.py --strict
python .agents/hooks/check_deletion_evidence.py --strict
python .agents/hooks/check_review_routing.py --strict
python .agents/hooks/check_review_output_provenance.py --diff origin/main --strict
python .agents/hooks/check_handoff_pointers.py --strict
python .agents/hooks/check_full_gt_claims.py --changed --strict
rg -n "orca-harness|orca_harness|orca-harness-tests" .github .agents repo-structure.yaml renovate.json forseti-harness README.md docs
git status --short --branch
```

Do not run `registration_integrity.py --selftest` for this migration lane.

## Rejected Paths

| Path | Reason rejected |
| --- | --- |
| Broad word-match rename | Would rewrite historical provenance and miss runtime path semantics. |
| CI check rename alone while open old-check PRs still need human landing | It can make the human merge helper look for the new check on old PRs unless those PRs are rebased or landed first. |
| Python namespace rename to `forseti_harness` | Current package layout exposes top-level modules, not an `orca_harness` package namespace. |
| External repo slug change inside this lane | Repo slug/remotes are owner-gated and blocked until the chosen target slug is available. |

## Non-Claims

- This plan is not implementation, validation, readiness, deployment, package publication, branch-protection configuration, GitHub repo rename execution, or local checkout rename execution.
- This plan does not claim every future `orca-harness` residual is invalid; it requires classification before removal.
- This plan does not authorize broad historical prompt, review-output, or archived-receipt rewrites.

## Direction Change Propagation

```yaml
direction_change_propagation:
  doctrine_changed: >
    The retained `orca-harness/` compatibility identifier now has an explicit
    Forseti migration plan: migrate the root, distribution label, CI check name,
    hook path consumers, and live operator docs together, while preserving Python
    import namespaces and historical provenance.
  trigger: lifecycle_boundary
  related_triggers:
    - workflow_authority
    - validation_philosophy
    - architecture_doctrine
  controlling_sources_updated:
    - docs/decisions/forseti_harness_identity_migration_plan_v0.md
    - docs/migration/forseti_harness_runtime_migration_v0/moved_paths_index.md
  downstream_surfaces_checked:
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/source-of-truth.md
    - docs/decisions/forseti_external_identity_path_migration_decision_v0.md
    - docs/workflows/forseti_rename_residual_inventory_v0.md
    - docs/workflows/forseti_repo_map_v0.md
    - .github/workflows/ci.yml
    - .github/workflows/auto-merge.yml
    - .github/scripts/merge-when-green.ps1
    - .github/workflows/pr-risk-router.yml
    - repo-structure.yaml
    - forseti-harness/pyproject.toml
  intentionally_not_updated:
    - path: external GitHub repository slug and local parent checkout folder
      reason: >
        Repo slug/remotes and the parent folder name are owner/external-state
        gated separately from the internal runtime root.
  stale_language_search: >
    rg -n "orca-harness|orca_harness|orca-harness-tests|forseti-harness|forseti_harness|forseti-harness-tests"
    .github .agents repo-structure.yaml README.md docs/workflows docs/decisions forseti-harness
  stale_language_search_result: >
    Re-run by the implementation lane. Remaining old harness hits are expected
    only where they are historical/provenance records, moved-path source terms,
    or residual-audit text; live runtime/tooling surfaces use Forseti naming.
  non_claims:
    - not validation
    - not readiness
    - not implementation
    - not package publication
    - not GitHub repo rename execution
```

Older receipts archived verbatim in `docs/decisions/dcp_receipts_archive_v0.md`.
