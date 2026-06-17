# Commission Signal Board Spine Pilot Migration Plan v0

```yaml
retrieval_header_version: 1
artifact_role: Migration plan (Commission Signal Board spine pilot; docs-only)
scope: >
  Inventory current Commission Signal Board artifacts, reconcile the active
  gate-shaped naming residue, and define the lowest-risk future spine pilot
  without creating a live `orca/` root or moving files under current binding.
use_when:
  - Planning the Commission Signal Board spine pilot after reviewing the spine-first workspace proposal.
  - Deciding which current artifacts would move into a future Commission Signal Board spine.
  - Explaining why the current lane can prepare a migration plan but cannot create `orca/product/spines/commission_signal_board/`.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/orca_spine_first_workspace_structure_proposal_v0.md
  - docs/decisions/orca_repo_structure_binding_v0.md
  - .agents/workflow-overlay/artifact-folders.md
  - repo-structure.yaml
  - docs/workflows/orca_repo_map_v0.md
  - docs/workflows/commission_signal_board_playbook_v0.md
stale_if:
  - The spine-first workspace proposal is accepted, rejected, or materially amended.
  - `repo-structure.yaml` adds `orca` as a live top-level root.
  - Commission Signal Board artifacts move, split, or receive a new owning playbook.
  - The Commission Signal Board validator becomes CI, pre-commit, runtime, or product-owned infrastructure.
```

- Status: MIGRATION_PLAN_ONLY.
- Branch basis: `codex/commission-spine-structure` at
  `14ba32adfd3082f069971d2f7a34a7a943c09804` when this plan was drafted.
- PR observation: GitHub PR #239 is open, titled
  `docs: propose spine-first workspace structure`, with head
  `codex/commission-spine-structure` and base `codex/commission-gate`.
- Current binding remains `docs/` plus `orca-harness/`; this file does not make
  `orca/product/spines/commission_signal_board/` live.
- No file moves, runtime work, retrieval, scraping, graph construction, demand
  classification, forecast, buyer-proof claim, hook wiring, CI wiring, or
  validator behavior change is authorized by this plan.

## D1 Start-State Receipt

```yaml
worktree_path: C:/Users/vmon7/Desktop/projects/orca/.codex/worktrees/commission-spine-structure
branch: codex/commission-spine-structure
head_at_draft: 14ba32adfd3082f069971d2f7a34a7a943c09804
merge_base_origin_main: faf91afc43c2d5db3c4a739413c3685d788b0ac3
pr_239:
  observed: yes
  state: OPEN
  title: docs: propose spine-first workspace structure
  url: https://github.com/eric-foo/orca/pull/239
  head: codex/commission-spine-structure
  base: codex/commission-gate
dirty_state_observed_during_work:
  status: dirty
  unrelated_paths_seen:
    - docs/migration/judgment_spine_spine_first_migration_inventory_v0.md
    - docs/migration/data_lake_spine_first_migration_inventory_v0.md
  handling: left untouched and not part of this CSB plan
source_context: SOURCE_CONTEXT_READY
method_application:
  reference_loaded:
    - workflow-deep-thinking
    - workflow-assumption-gate
  source_loaded:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - .agents/workflow-overlay/decision-routing.md
    - .agents/workflow-overlay/source-loading.md
    - .agents/workflow-overlay/source-of-truth.md
    - .agents/workflow-overlay/artifact-folders.md
    - .agents/workflow-overlay/prompt-orchestration.md
    - repo-structure.yaml
    - docs/STRUCTURE.md
    - docs/decisions/orca_repo_structure_binding_v0.md
    - docs/decisions/orca_spine_first_workspace_structure_proposal_v0.md
    - docs/workflows/orca_repo_map_v0.md
    - docs/workflows/commission_signal_board_playbook_v0.md
    - docs/prompts/product-planning/orca_commission_signal_board_prompt_v0.md
    - docs/product/product_lead/orca_commission_signal_board_prompt_adjudication_packet_v0.md
    - .agents/hooks/check_commission_signal_board_output.py
    - orca-harness/tests/unit/test_commission_signal_board_output_validator.py
    - orca-harness/tests/fixtures/commission_signal_board_outputs/
delegated_exploration:
  naming_inventory: complete
  artifact_inventory: complete
  binding_impact: complete
```

## D2 Naming Reconciliation

The active product object is Commission Signal Board. It is not Commission Gate,
not a demand gate, and not an approval surface.

Patched active wording:

| Path | Change | Reason |
| --- | --- | --- |
| `docs/workflows/commission_signal_board_playbook_v0.md` | `intake gate` -> `intake check` | Active CSB playbook wording made the intake step sound like an approval gate. |
| `docs/prompts/product-planning/orca_commission_signal_board_prompt_v0.md` | Added `legacy-named` before `codex/commission-gate` | Preserves factual branch provenance while warning future agents not to import gate semantics. |
| `docs/workflows/orca_repo_map_v0.md` | Added this migration plan to Product Anchor Files and refreshed the map note | Makes the docs-only plan discoverable from commissioning sources. |

Intentionally preserved language:

| Hit family | Why preserved |
| --- | --- |
| `codex/commission-gate` branch/worktree references | Factual legacy lane provenance, not current product semantics. |
| Handoff prompt references to `commission gate` | The handoff itself names stale language as the thing to reconcile. |
| Adjudication packet temp path and legacy schema references | Historical provenance from the earlier temporary prompt, not current naming authority. |
| Source-capture, data-capture, ECR, Judgment, proof, or validation gates | Separate concepts outside the Commission Signal Board naming decision. |

Searches used for reconciliation:

```powershell
rg -n "commission gate|commission-gate|Commission Gate|commission_gate|commissioning gate" docs .agents orca-harness repo-structure.yaml
rg -n "\bgate\b|\bGate\b" docs\workflows\commission_signal_board_playbook_v0.md docs\prompts\product-planning\orca_commission_signal_board_prompt_v0.md docs\product\product_lead\orca_commission_signal_board_prompt_adjudication_packet_v0.md docs\prompts\handoffs\commission_signal_board_spine_pilot_reconciliation_handoff_prompt_v0.md docs\decisions\orca_spine_first_workspace_structure_proposal_v0.md
rg --files | rg "commission_signal_board|commission-gate|commission_gate|signal_board"
```

## D3 Artifact Inventory

| Current path | Role | Move decision | Proposed future spine target | Reason |
| --- | --- | --- | --- | --- |
| `docs/product/product_lead/orca_commission_signal_board_prompt_adjudication_packet_v0.md` | Product decision-prep and correction packet | Move later, after accepted binding | `orca/product/spines/commission_signal_board/authority/orca_commission_signal_board_prompt_adjudication_packet_v0.md` | Authority-adjacent artifact for why CSB exists and what it is not. |
| `docs/prompts/product-planning/orca_commission_signal_board_prompt_v0.md` | Full CSB prompt artifact | Move later, after accepted binding | `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md` | Product-specific prompt should live with its spine once the spine is live. |
| `docs/workflows/commission_signal_board_playbook_v0.md` | Operating playbook | Move later, after accepted binding | `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md` | Agents need the prompt, validator, and execution sequence in the same product spine. |
| `.agents/hooks/check_commission_signal_board_output.py` | Manual/local validator script | Keep global during pilot; add spine pointer later | `orca/product/spines/commission_signal_board/harness/validator.md` as a pointer first | Current proposal keeps `.agents/hooks` global; product-runtime validator move needs separate authorization. |
| `orca-harness/tests/unit/test_commission_signal_board_output_validator.py` | Validator tests | Keep executable test under `orca-harness` during pilot; add spine pointer later | `orca/product/spines/commission_signal_board/tests/unit/test_commission_signal_board_output_validator.md` as a pointer or moved-path note | Shared harness code remains global until a separate code-root migration exists. |
| `orca-harness/tests/fixtures/commission_signal_board_outputs/` | Validator fixtures | Keep executable fixtures under `orca-harness` during pilot; mirror/index later | `orca/product/spines/commission_signal_board/tests/fixtures/commission_signal_board_outputs/` | Fixtures are CSB-specific but currently bound to the executable harness tests. |
| `docs/prompts/handoffs/commission_signal_board_spine_pilot_reconciliation_handoff_prompt_v0.md` | One-off reconciliation handoff | Preserve in current handoff archive; optionally index later | `orca/product/spines/commission_signal_board/prompts/` or `migrations/` only if owner wants spine-local handoff history | The handoff commissioned this plan; it is not itself runtime CSB authority. |
| `docs/workflows/orca_repo_map_v0.md` | Global navigation map | Keep global | Future `orca/docs/workflows/orca_repo_map_v0.md`, if global docs root is accepted | Repo-wide maps should not become product-spine-local. |
| `docs/decisions/orca_spine_first_workspace_structure_proposal_v0.md` | Proposed structure decision | Keep global | Future `orca/docs/decisions/orca_spine_first_workspace_structure_proposal_v0.md`, if global docs root is accepted | Repo-structure decisions remain global. |
| `docs/migration/commission_signal_board_spine_pilot_migration_plan_v0.md` | This docs-only migration plan | Keep until accepted migration | `orca/product/spines/commission_signal_board/migrations/moved_paths_index.md` plus retained global history if needed | This is planning substrate, not the live spine itself. |

No CSB-specific adversarial review output was found in the targeted inventory.

## D4 Spine Pull-Out Plan

| Option | What it does | Pros | Risks | Decision |
| --- | --- | --- | --- | --- |
| A. Stay fully in current layout | Keep CSB artifacts where they are and only improve map discovery | Lowest churn; respects current binding | CSB remains scattered across product, prompt, workflow, hook, harness, and migration folders | Use as current safe state. |
| B. Create a docs-side CSB grouping | Add another `docs/` grouping and copy/index artifacts there | Better local discoverability without a root change | Creates a second product-spine shape that may conflict with the proposed target | Do not use now. |
| C. Prepare the proposed live spine | Plan for `orca/product/spines/commission_signal_board/` but do not create it | Matches the proposal and keeps the pilot coherent | Blocked until owner/source accepts binding changes | Recommended future move. |
| D. Combine product spine with future `orca/docs/` split now | Move product spine plus global docs into new roots together | Closest to the full proposed target | Too broad for a pilot; high lock-in; not authorized | Defer. |

Recommended route:

```text
Now: docs-only migration plan plus active wording cleanup.
Next: owner accepts or amends the spine-first proposal.
Then: update binding surfaces and create only the CSB pilot spine.
Later: decide whether global docs move to `orca/docs/`.
```

## D5 Pilot Skeleton Or Docs-Only Migration Plan

Live skeleton creation is blocked. The proposed future tree is:

```text
orca/product/spines/commission_signal_board/
  README.md
  spine.yaml
  authority/
    orca_commission_signal_board_prompt_adjudication_packet_v0.md
  prompts/
    orca_commission_signal_board_prompt_v0.md
  workflows/
    commission_signal_board_playbook_v0.md
  harness/
    validator.md
  tests/
    unit/
      test_commission_signal_board_output_validator.md
    fixtures/
      commission_signal_board_outputs/
  migrations/
    moved_paths_index.md
  archive/
```

Required accepted-source updates before the live tree exists:

| Surface | Required update |
| --- | --- |
| `docs/decisions/orca_repo_structure_binding_v0.md` | Accept or amend the spine-first structure and define whether `orca/` is a live top-level root. |
| `.agents/workflow-overlay/artifact-folders.md` | Define the CSB spine home and whether `docs/product/<lane>/` remains allowed, legacy-current, or migration-source. |
| `repo-structure.yaml` | Add `orca` to known top-level dirs and define the allowed path grammar, if the machine map is still the placement router. |
| `docs/STRUCTURE.md` | Explain the new product-spine and global-doc split to human readers. |
| `docs/workflows/orca_repo_map_v0.md` | Route agents to the new CSB spine and moved-path index. |
| `.agents/hooks/check_placement.py` and tests, if needed | Teach placement checks the new `orca/product/spines/<spine>/` shape if they assert the closed root set or deeper grammar. |

Move strategy after acceptance:

1. Create `orca/product/spines/commission_signal_board/README.md` with the current non-goals and source-loading order.
2. Move or copy the three durable CSB docs first: adjudication packet, prompt, and playbook.
3. Add `migrations/moved_paths_index.md` mapping old paths to new paths.
4. Leave executable validator and `orca-harness` tests in place unless separately authorized; add spine-local harness/test pointers instead.
5. Update repo map, playbook paths, prompt metadata, and any validator docs references.
6. Run placement, repo-map freshness, retrieval-header, validator tests if touched, and `git diff --check`.

Rollback strategy:

```text
Because this plan performs no live move, rollback is deleting or superseding this file.
For the future live migration, keep old-path stubs or a moved-path index until all
source-loading prompts and validator docs point to the spine.
```

## Assumption-Gate Ledger

```yaml
accepted_direction: docs-only Commission Signal Board spine-pilot migration plan
gate_status: READY_WITH_VERIFIED_LEDGER
ready_for_docs_only_plan: yes
ready_for_live_spine_creation: no
load_bearing_assumptions:
  - assumption: docs/migration is an accepted home for migration planning artifacts.
    status: verified_real
    basis:
      - docs/migration/ exists.
      - docs/migration/repo_structure_phase2_consolidation_v0/ exists.
  - assumption: current binding does not make `orca/` a live root.
    status: verified_real
    basis:
      - docs/decisions/orca_spine_first_workspace_structure_proposal_v0.md is PROPOSED_TARGET.
      - repo-structure.yaml known top-level dirs omit `orca`.
      - docs/workflows/orca_repo_map_v0.md says the proposal does not make `orca/` live.
  - assumption: CSB validator behavior is out of scope.
    status: verified_real
    basis:
      - docs/workflows/commission_signal_board_playbook_v0.md describes the checker as manual/local.
      - .agents/hooks/check_commission_signal_board_output.py states it does not retrieve, classify, or prove correctness.
blockers_for_live_spine:
  - owner/source acceptance of the spine-first structure proposal
  - binding updates across the required surfaces
  - placement-checker expectation update if the new root/path grammar is enforced
```

## D6 Closeout And Propagation

This plan does not change repo doctrine. It records a blocker for the doctrine
change that would be required before a live CSB spine exists.

```yaml
doctrine_changed_by_this_plan: no
direction_change_propagation_blocker:
  blocked_change: create live `orca/product/spines/commission_signal_board/`
  blocker: no accepted repo-structure source currently binds `orca/` as a live root
  related_triggers:
    - architecture_doctrine
    - workflow_authority
    - output_authority
  verified_sources:
    - docs/decisions/orca_spine_first_workspace_structure_proposal_v0.md
    - docs/decisions/orca_repo_structure_binding_v0.md
    - .agents/workflow-overlay/artifact-folders.md
    - repo-structure.yaml
    - docs/STRUCTURE.md
    - docs/workflows/orca_repo_map_v0.md
  next_authorized_step: owner accepts or amends the spine-first proposal, then a bounded binding patch can create the live CSB pilot root
non_claims:
  - no Commission Signal Board case was run
  - no evidence was retrieved
  - no demand classification happened
  - no forecast, weighting, judgment, graph artifact, or buyer proof was produced
  - no validator behavior was changed
```

Validation for this docs-only plan:

```powershell
python .agents\hooks\check_retrieval_header.py --changed
python .agents\hooks\check_repo_map_freshness.py --changed
python .agents\hooks\check_placement.py --check
git diff --check
```
